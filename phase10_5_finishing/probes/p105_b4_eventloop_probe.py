#!/usr/bin/env python3
"""P10.5, Block 4, Schritt 4.6 — die Event-Loop-Probe (Z2, Abnahme P10.5-16).

**Die Frage:** wartet ein Request hinter `/overview`, oder antwortet der Server sofort?

Der Befund aus P10 (M1, 2026-10-20): `/overview` brauchte 4,8 s und **blockierte dabei den
gesamten Event-Loop** — ein parallel gestartetes `/health` kam erst nach ~T zurück, ein zweites
`/overview` erst nach ~2T. Die Ursache war doppelt: `api.py :: _overview()` rief `store.search()`
**synchron** in einer `async def` auf (der Store liest jede indizierte Datei), und sie rief es
**sechsmal** (fünf Eimer + die „zuletzt benutzt"-Liste, je sichtbarem Space).

**Was Block 4 geändert hat:** ein einziger Durchgang (P10.5-G) und `asyncio.to_thread`
(Plan §4.2). Der Store liest jetzt in einem Worker-Thread — der Event-Loop antwortet
währenddessen.

**Die Messung** (Logik übernommen aus `phase10_inventory/probes/p10_pf_eventloop_probe.py`,
Probe (a) — das Skript ist eine **eigene** Datei: `phase10_inventory/probes/` ist für Block 4
nicht freigegeben, P10-Artefakte werden nicht angefasst):
  1. Baseline: `/health`, `/api/v1/spaces`, `/api/v1/overview` einzeln, frei.
  2. Drei Läufe: `/overview` starten, 100 ms später `/health`, `/api/v1/spaces` und ein
     zweites `/overview` starten.
  3. **Blockade** = die Zusatz-Anfragen kommen erst nach ~T zurück. Ohne Blockade: ms.

**Die Abnahme-Zeile (P10.5-16):** `/health` hinter `/overview` ≤ **200 ms**. Der alte Zustand
war 4,757 s (P10-Messung) — das ist der Vergleichslauf, kein neuer Wert.

**Sitzung:** die Messung braucht eine **gültige Cookie-Sitzung**, sonst beantwortet
`/api/v1/overview` sofort mit 401 — und die Rechteprüfung steht **vor** dem Store-Aufruf, ein
401 ließe also genau die Arbeit weg, die gemessen werden soll. Die Sitzung holt der
Playwright-Teil (Login als `alpha`, dieselbe Rechnung wie in P10), gemessen wird danach über
`urllib` mit dem Cookie.

**Ausgabe:** genau ein JSON-Objekt auf stdout (Hard Rule 7), Logs auf stderr. Kein Netz gegen
den echten `DATA_ROOT` — nur die Wegwerf-Instanz auf Port 8799 mit tmp-`DATA_ROOT`.
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
OUT = Path(__file__).with_name("p105_b4_eventloop.json")

# Abnahme P10.5-16: `/health` hinter `/overview` darf höchstens 200 ms warten.
GRENZE_HEALTH_MS = 200


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
    req = urllib.request.Request(BASE + path, headers={"Cookie": ctx["cookie"]})
    try:
        code = urllib.request.urlopen(req, timeout=60, context=ctx["ssl"]).status
    except Exception as exc:  # noqa: BLE001 — eine Probe protokolliert den Fehler mit
        code = repr(exc)
    out[key] = {
        "status": code,
        "start_s": round(s - t0, 3),
        "dauer_s": round(time.perf_counter() - s, 3),
    }


def probe_a(cookie: str) -> dict:
    ctx = {"cookie": cookie, "ssl": ssl._create_unverified_context()}
    res: dict = {}
    for key, path in (
        ("health_frei", "/health"),
        ("spaces_frei", "/api/v1/spaces"),
        ("overview_frei", "/api/v1/overview"),
    ):
        timed_get(ctx, path, time.perf_counter(), res, key)

    runs = []
    for _ in range(3):
        out: dict = {}
        t0 = time.perf_counter()
        threads = [
            threading.Thread(target=timed_get, args=(ctx, "/api/v1/overview", t0, out, "overview_1"))
        ]
        threads[0].start()
        time.sleep(0.1)
        for key, path in (
            ("health", "/health"),
            ("spaces", "/api/v1/spaces"),
            ("overview_2", "/api/v1/overview"),
        ):
            th = threading.Thread(target=timed_get, args=(ctx, path, t0, out, key))
            th.start()
            threads.append(th)
        for th in threads:
            th.join()
        runs.append(out)

    res["parallel_runs"] = runs
    t_overview = res["overview_frei"]["dauer_s"]
    res["T_overview_s"] = t_overview
    # **Dieselbe Kennzahl wie in P10** (dort: `health` wartet > 0,5 · T): die Zusatz-Anfrage
    # wartet nicht mehr hinter dem `/overview`.
    res["blockade_health"] = all(r["health"]["dauer_s"] > 0.5 * t_overview for r in runs)
    res["overview_2_serialisiert"] = all(
        r["overview_2"]["dauer_s"] > 1.5 * t_overview - 0.1 for r in runs
    )
    # **Die Abnahme-Zeile (P10.5-16):** die Wartezeit von `/health` hinter `/overview`.
    wartezeiten_ms = [round(r["health"]["dauer_s"] * 1000, 1) for r in runs]
    res["health_wartezeit_ms"] = wartezeiten_ms
    res["health_wartezeit_max_ms"] = max(wartezeiten_ms)
    res["grenze_ms"] = GRENZE_HEALTH_MS
    res["p10_5_16_erfuellt"] = max(wartezeiten_ms) <= GRENZE_HEALTH_MS
    return res


def main() -> int:
    creds = json.loads((ROOT / "credentials.json").read_text())["users"][0]
    result: dict = {
        "probe": "p105_b4_eventloop",
        "datum": time.strftime("%Y-%m-%d"),
        "basis": "phase10_inventory/probes/p10_pf_eventloop_probe.py :: probe_a (Logik uebernommen)",
        "vergleich_p10": {
            "quelle": "phase10_inventory/probes/p10_pf_eventloop.json",
            "health_dauer_s": 4.757,
            "T_overview_s": 4.733,
            "blockade_health": True,
        },
    }
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        ctx = browser.new_context(
            viewport={"width": 1440, "height": 900}, ignore_https_errors=True
        )
        page = ctx.new_page()
        login(page, creds)
        cookie = "; ".join(f"{c['name']}={c['value']}" for c in ctx.cookies())
        browser.close()
    result["a_eventloop"] = probe_a(cookie)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
