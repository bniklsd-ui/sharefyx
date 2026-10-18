#!/usr/bin/env python3
"""M4 (P10-Plan §4, Register BG-1, [VERIFY] V202): reproduziert BG-1 in `v3.1.4`?

**BG-1:** die „Spaces verwalten"-Liste bleibt leer, wenn das Panel geöffnet wird, bevor
`loadOverview()` geliefert hat. Mechanik im Code: `renderSpaceList()` (`spaces.js:54`)
rendert `state.spaces.filter(writable)`, und `state.spaces` füllt **nur**
`list.js :: loadOverview()` (:191); `prepareSpacesPanel()` (:128) ruft es nicht — der
einzige Pfad, der nachlädt, ist der Space-Neuanlage-Handler (`spaces.js:214`). Der Nikinger
meldete das 2026-10-05 aus der P9-Bildsichtung („Produktbefund gemeldet, nicht gebaut").

**Probe (Wegwerf, Port 8799, `p10_wegwerf.py`):** Chromium meldet sich als `alpha` an;
Playwright verzögert `/api/v1/overview` per Route um 4 s, die Seite lädt frisch, sofort
werden `#account-button` → `#account-manage-spaces` geklickt und `#space-admin-list`
gezählt — **dreimal**: beim Öffnen (Erwartung: 0, der Befund), nachdem die verzögerte
Antwort geliefert hat (Erwartung: weiterhin 0 — die Liste wird nicht nachgezogen), und
nach Schließen + erneutes Öffnen des Panels (Erwartung: 2 — alpha + gamma; der Datensatz
existiert, nur das Rendern fehlte).

**Gegenlauf:** derselbe Ablauf ohne Verzögerung — `overview` abwarten, dann öffnen
(Erwartung: 2). Ohne sie wäre „0 beim sofortigen Öffnen" auch die Erklärung „der Space hat
keine schreibbaren Spaces" — die Gegenlauf-2 beweist, dass die Messanordnung die Daten
vorfindet und nur die Reihenfolge den Unterschied macht.

Ausgabe: JSON auf stdout (Hard Rule 7), Logs auf stderr; Screenshots nach
`docs/screenshots/p10_m4_bg1_{leer,gegenlauf}.png` (Build-Belege, reine
Konsolen-/DOM-Messung — kein Sichtungs-Bild, deshalb bewusst **nicht** in
`screenshots_latest/`).
"""
from __future__ import annotations

import argparse
import base64
import datetime
import hashlib
import hmac
import json
import struct
import sys
import time
import urllib.parse
from pathlib import Path

from playwright.sync_api import Page, sync_playwright

REPO_ROOT = Path(__file__).resolve().parents[2]
CREDS_FILE = Path("/tmp/opencode/sharefyx-wegwerf-p10/credentials.json")
BASE_URL = "http://127.0.0.1:8799"
DELAY_S = 4.0
SHOT_DIR = REPO_ROOT / "docs" / "screenshots"
OUT_JSON = REPO_ROOT / "phase10_inventory" / "probes" / "p10_m4_bg1.json"

EXPECTED_WRITABLE = 2  # alpha (eigen) + gamma (Team-Space mit write:); beta ist nur lesbar


def _generate_totp(otpauth_uri: str) -> str:
    parsed = urllib.parse.urlparse(otpauth_uri)
    qs = urllib.parse.parse_qs(parsed.query)
    secret_b32 = qs["secret"][0]
    key = base64.b32decode(secret_b32 + "=" * (-len(secret_b32) % 8))
    counter = int(time.time() // 30)
    msg = struct.pack(">q", counter)
    digest = hmac.new(key, msg, hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    code_int = (struct.unpack(">I", digest[offset:offset + 4])[0] & 0x7FFFFFFF) % 1000000
    return f"{code_int:06d}"


def login(page: Page, base_url: str, space: str, password: str, otpauth_uri: str) -> None:
    secs_into = datetime.datetime.now().second
    wait = 35 - (secs_into % 30)
    print(f"Login: warte {wait}s auf frisches TOTP-Fenster ...", file=sys.stderr)
    time.sleep(wait)
    for window in range(2):
        page.goto(f"{base_url}/ui/login", wait_until="domcontentloaded")
        page.locator('input[name="space"]').fill(space)
        page.locator('input[name="password"]').fill(password)
        code = _generate_totp(otpauth_uri)
        print(f"  Fenster {window + 1}: TOTP {code}", file=sys.stderr)
        page.locator('input[name="totp"]').fill(code)
        with page.expect_response("**/ui/login**") as resp_info:
            page.locator('button[type="submit"]').click()
        resp = resp_info.value
        print(f"  Fenster {window + 1}: HTTP {resp.status}", file=sys.stderr)
        if resp.status in (200, 303):
            time.sleep(2.0)
            return
        if resp.status == 401:
            time.sleep(35)
            continue
        raise RuntimeError(f"Login fehlgeschlagen: HTTP {resp.status}")
    raise RuntimeError("Login: TOTP-Fenster erschöpft")


def _dismiss_banner(page: Page) -> None:
    try:
        dismiss = page.locator("#update-banner-dismiss")
        if dismiss.is_visible(timeout=1000):
            dismiss.click()
            time.sleep(0.3)
    except Exception:
        pass


def _open_spaces_panel(page: Page) -> None:
    page.locator("#account-button").click()
    page.locator("#account-manage-spaces").click()


def _row_count(page: Page) -> int:
    return page.evaluate(
        "document.getElementById('space-admin-list')"
        "  ? document.getElementById('space-admin-list').children.length : -1"
    )


def _wait_overview_settled(page: Page, extra_s: float = 0.0) -> None:
    time.sleep(DELAY_S + 1.5 + extra_s)


def run_delayed(page: Page) -> dict:
    """Befund-Pfad: /overview um 4 s verzögert, Panel sofort geöffnet."""
    page.route(
        "**/api/v1/overview",
        lambda route: (time.sleep(DELAY_S), route.continue_()),
    )
    page.goto(f"{BASE_URL}/ui/", wait_until="domcontentloaded")
    _open_spaces_panel(page)
    count_open = _row_count(page)
    page.screenshot(path=str(SHOT_DIR / "p10_m4_bg1_leer.png"))
    _wait_overview_settled(page)
    count_after_delay = _row_count(page)
    # Panel zu und wieder auf (Toggle im Menüknopf): jetzt rendert prepareSpacesPanel()
    # den inzwischen gefüllten state.spaces.
    page.locator("#account-manage-spaces").click()  # zu (openStage === 'spaces')
    page.locator("#account-manage-spaces").click()  # wieder auf
    count_reopened = _row_count(page)
    page.unroute("**/api/v1/overview")
    return {
        "count_on_open": count_open,
        "count_after_delay_resolved": count_after_delay,
        "count_after_reopen": count_reopened,
    }


def run_immediate(page: Page) -> dict:
    """Gegenlauf: ohne Verzögerung — overview abwarten, dann öffnen."""
    with page.expect_response("**/api/v1/overview"):
        page.goto(f"{BASE_URL}/ui/", wait_until="domcontentloaded")
    time.sleep(0.5)
    _open_spaces_panel(page)
    count = _row_count(page)
    page.screenshot(path=str(SHOT_DIR / "p10_m4_bg1_gegenlauf.png"))
    return {"count_on_open": count}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.parse_args(argv)

    creds = json.loads(CREDS_FILE.read_text())["users"][0]
    assert creds["space"] == "alpha"

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()
        login(page, BASE_URL, creds["space"], creds["password"], creds["otpauth_uri"])

        delayed = run_delayed(page)
        immediate = run_immediate(page)

        browser.close()

    result = {
        "probe": "p10_m4_bg1",
        "expected_writable_spaces": EXPECTED_WRITABLE,
        "delayed_path": delayed,
        "immediate_path": immediate,
        "bg1_reproduced": (
            delayed["count_on_open"] == 0
            and delayed["count_after_delay_resolved"] == 0
            and delayed["count_after_reopen"] == EXPECTED_WRITABLE
            and immediate["count_on_open"] == EXPECTED_WRITABLE
        ),
    }
    print(json.dumps(result, ensure_ascii=False))
    OUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
