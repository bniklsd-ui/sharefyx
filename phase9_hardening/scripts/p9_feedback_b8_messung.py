#!/usr/bin/env python3
"""P9 Block feedback B8 (V190, P9-132): was fordert ein Space-Wechsel an, wie lange dauert er?

Import statt Kopie von `p9_feedback_self_check.py` (derselbe Block, dieselbe Instanz, dieselben
Konstanten — der Kopie-Grund aus den Nachbarskripten greift hier nicht). Misst im echten Browser:
alle `/api/`-Anfragen zwischen Klick auf den Rail-Eintrag und dem Verstummen des Netzes, plus die
Zeit bis die Listenzeilen des Ziel-Spaces stehen. Drei Laeufe je Richtung. Lokale Wegwerf-Instanz:
die Zahlen sagen **was** angefordert wird, nicht wie langsam die Funnel-Strecke ist (P9-15: ~3,1 s).
"""
from __future__ import annotations

import datetime
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from playwright.sync_api import sync_playwright  # noqa: E402

import p9_feedback_self_check as sc  # noqa: E402

ZIEL = sc.PROBE_DIR / "p9_feedback_b8_messung.json"


def main() -> int:
    creds = json.loads(sc.DEFAULT_CREDS.read_text())
    laeufe = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1440, "height": 900}, ignore_https_errors=True)
        page = ctx.new_page()
        page.goto(f"{sc.DEFAULT_BASE_URL}/ui/login", wait_until="domcontentloaded")
        time.sleep(32 - (datetime.datetime.now().second % 30))
        if not sc.login(page, sc.DEFAULT_BASE_URL, "alpha", creds["alpha"]["password"],
                        creds["alpha"]["otpauth_uri"]):
            print("Login fehlgeschlagen", file=sys.stderr)
            return 2
        time.sleep(3)
        log: list[dict] = []
        t0 = [0.0]
        page.on("requestfinished", lambda r: log.append(
            {"url": r.url.split("/api/v1")[-1] if "/api/" in r.url else None,
             "t": round((time.time() - t0[0]) * 1000), "dauer_ms": round(
                 (r.timing["responseEnd"] - r.timing["requestStart"]), 1) if r.timing else None}))
        for lauf in range(3):
            for ziel in ("team", "alpha"):
                page.locator("#home-button").click()
                time.sleep(1.5)
                log.clear()
                zeile = page.locator(".overview__space-open").filter(
                    has=page.locator(f'.overview__space-name-label:text-is("{ziel}")'))
                t0[0] = time.time()
                zeile.first.click()
                page.wait_for_function(
                    "() => document.querySelector('.list__rows') && !document.querySelector('.list__rows').hidden",
                    timeout=10000)
                sichtbar = round((time.time() - t0[0]) * 1000)
                time.sleep(2.0)  # Nachzuegler (Graph, Poll) sollen mitgemessen werden
                api = [e for e in log if e["url"]]
                laeufe.append({"lauf": lauf + 1, "ziel": ziel, "bis_liste_ms": sichtbar,
                               "anfragen": api})
                print(f"lauf {lauf + 1} -> {ziel}: Liste nach {sichtbar} ms, Anfragen: "
                      + ", ".join(f"{e['url'].split('?')[0]}@{e['t']}ms({e['dauer_ms']})" for e in api),
                      file=sys.stderr)
        browser.close()
    ZIEL.write_text(json.dumps({"laeufe": laeufe}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
