#!/usr/bin/env python3
"""PF-1 / PF-4 (P10-Plan §4, Handover 2026-10-20 Schritt 2): zwei Proben gegen die Wegwerf-Instanz.

**Probe (a) — Event-Loop-Blockade (PF-1):** `api.py :: _overview` ist `async def` mit
synchronem `store.search()` (kein `to_thread`). Ist das die Ursache fuer "spaces/items warten
hinter overview" (M1), dann blockiert ein laufendes `/overview` den gesamten Loop — auch ein
trivialer `/health`. Messung: `/overview` allein (T), dann `/overview` + 100 ms spaeter
`/health` und `/api/v1/spaces`; ein zweites paralleles `/overview`. Blockade = die Zusatz-
Anfragen kommen erst nach ~T zurueck; keine Blockade = ms.

**Probe (b) — Mitlauf-`overview` (PF-4):** zaehlt `/api/v1/overview`-Requests im Browser
(Playwright, `page.on("request")`) fuer: Seite laden und ruhen; ein Item oeffnen ohne
Fokuswechsel; Item oeffnen + `window.focus`-Event (Rueckkehr aus dem Inspektor / Tab).

Ausgabe: JSON auf stdout (Hard Rule 7), Logs auf stderr, Kopie nach p10_pf_eventloop.json.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import ssl
import struct
import sys
import threading
import time
import urllib.parse
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path("/tmp/opencode/sharefyx-wegwerf-p10")
BASE = "https://127.0.0.1:8799"
OUT = Path(__file__).with_name("p10_pf_eventloop.json")


def totp(uri: str) -> str:
    sec = urllib.parse.parse_qs(urllib.parse.urlparse(uri).query)["secret"][0]
    key = base64.b32decode(sec + "=" * (-len(sec) % 8))
    d = hmac.new(key, struct.pack(">q", int(time.time() // 30)), hashlib.sha1).digest()
    o = d[-1] & 15
    return f"{(struct.unpack('>I', d[o:o + 4])[0] & 0x7FFFFFFF) % 10**6:06d}"


def login(page, creds) -> None:
    wait = 31 - (int(time.time()) % 30)
    time.sleep(wait)  # frisches TOTP-Fenster
    page.goto(f"{BASE}/ui/login", wait_until="domcontentloaded")
    page.fill('input[name="space"]', creds["space"])
    page.fill('input[name="password"]', creds["password"])
    page.fill('input[name="totp"]', totp(creds["otpauth_uri"]))
    with page.expect_response("**/ui/login**") as r:
        page.click('button[type="submit"]')
    assert r.value.status in (200, 303), r.value.status
    time.sleep(1.5)


def timed_get(ctx, path: str, t0: float, out: dict, key: str) -> None:
    s = time.perf_counter()
    resp = urllib.request.Request(BASE + path, headers={"Cookie": ctx["cookie"]})
    try:
        code = urllib.request.urlopen(resp, timeout=60, context=ctx["ssl"]).status
    except Exception as e:  # noqa: BLE001 - Probe, Fehler wird mitprotokolliert
        code = repr(e)
    out[key] = {"status": code, "start_s": round(s - t0, 3), "dauer_s": round(time.perf_counter() - s, 3)}


def probe_a(cookie: str) -> dict:
    ctx = {"cookie": cookie, "ssl": ssl._create_unverified_context()}
    res: dict = {}
    # Baseline: was kosten die Zusatz-Anfragen frei?
    for key, path in (("health_frei", "/health"), ("spaces_frei", "/api/v1/spaces"), ("overview_frei", "/api/v1/overview")):
        timed_get(ctx, path, time.perf_counter(), res, key)
    runs = []
    for _ in range(3):
        out: dict = {}
        t0 = time.perf_counter()
        ths = [threading.Thread(target=timed_get, args=(ctx, "/api/v1/overview", t0, out, "overview_1"))]
        ths[0].start()
        time.sleep(0.1)
        for key, path in (("health", "/health"), ("spaces", "/api/v1/spaces"), ("overview_2", "/api/v1/overview")):
            th = threading.Thread(target=timed_get, args=(ctx, path, t0, out, key))
            th.start()
            ths.append(th)
        for th in ths:
            th.join()
        runs.append(out)
    res["parallel_runs"] = runs
    T = res["overview_frei"]["dauer_s"]
    res["T_overview_s"] = T
    # Blockade: health/spaces enden erst nach ~T (statt ms), overview_2 serialisiert (~2T).
    res["blockade_health"] = all(r["health"]["dauer_s"] > 0.5 * T for r in runs)
    res["overview_2_serialisiert"] = all(r["overview_2"]["dauer_s"] > 1.5 * T - 0.1 for r in runs)
    return res


def probe_b(page) -> dict:
    counts = {"n": 0}
    page.on("request", lambda rq: counts.__setitem__("n", counts["n"] + 1) if rq.url.endswith("/api/v1/overview") else None)
    page.goto(f"{BASE}/ui/", wait_until="domcontentloaded")
    page.wait_for_selector("button.tree__folder[data-space='alpha']", timeout=60000)
    time.sleep(3)
    res = {"laden_und_ruhen_3s": counts["n"]}
    # Liste oeffnen: erster Bucket-Ordner von alpha (tree.js:59-62)
    counts["n"] = 0
    page.locator("button.tree__folder[data-space='alpha'][data-bucket]").first.click()
    page.wait_for_selector("button.list__row[data-id]", timeout=120000)
    time.sleep(6)
    res["liste_oeffnen_6s"] = counts["n"]
    # Zeilen-Selektor ermitteln (Probe-Beobachtung, im Befund festgehalten)
    sel = "button.list__row[data-id]"  # list.js:413
    res["zeilen_selektor"] = sel
    if not sel:
        res["fehler"] = "kein Listenzeilen-Selektor gefunden"
        return res
    rows = page.locator(sel)
    res["zeilen"] = rows.count()
    # (1) Item oeffnen ohne Fokuswechsel
    counts["n"] = 0
    rows.nth(0).evaluate("e => e.click()")
    time.sleep(8)
    res["item_oeffnen_ohne_fokus_8s"] = counts["n"]
    # (2) zurueck + zweites Item + Fokuswechsel-Event
    counts["n"] = 0
    rows.nth(1).evaluate("e => e.click()")
    time.sleep(1)
    page.evaluate("window.dispatchEvent(new Event('focus'))")
    time.sleep(8)
    res["item_oeffnen_mit_focus_event_9s"] = counts["n"]
    return res


def main() -> int:
    creds = json.loads((ROOT / "credentials.json").read_text())["users"][0]
    result: dict = {"probe": "p10_pf_eventloop", "datum": time.strftime("%Y-%m-%d")}
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        ctx = br.new_context(viewport={"width": 1440, "height": 900}, ignore_https_errors=True)
        page = ctx.new_page()
        login(page, creds)
        cookie = "; ".join(f"{c['name']}={c['value']}" for c in ctx.cookies())
        result["a_eventloop"] = probe_a(cookie)
        OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
        result["b_mitlauf"] = probe_b(page)
        br.close()
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
