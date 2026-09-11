"""Phase 8.6 Block B — Self-Sichtprüfung der neuen Hover-Sprache + Vorsicht-Kategorie.

Schiesst drei Screenshots gegen die laufende Wegwerf-Instanz auf Port 18773:
  1. Rail-Uebersicht (logout-Knopf in Vorsicht-Farbe sichtbar)
  2. Liste mit Hover ueber einer Zeile (neue quiet-Selektion pruefbar)
  3. Editor geoeffnet (Archivieren-Knopf in Vorsicht-Farbe sichtbar)
  4. Konto-Dialog (Einstellungen-Knopf als Navigation, nicht Knopf-Plastik)

Die Screenshots werden nach docs/screenshots/ geschrieben und am Ende der Session mit dem
eingebauten `read`-Tool gelesen + beschrieben. Hard Rule 9: Stop nur ueber PID-Datei.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

CREDS_PATH = Path("/tmp/opencode/sharefyx-wegwerf-v3ritt/credentials.json")
BASE = "http://127.0.0.1:18773"
OUT_DIR = Path("docs/screenshots")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def _read_creds() -> dict[str, str]:
    return json.loads(CREDS_PATH.read_text())


def _login(page, password: str, otpauth_uri: str) -> None:
    page.goto(f"{BASE}/ui/login", wait_until="domcontentloaded")
    page.locator('input[name="space"]').fill("alpha")
    page.locator('input[name="password"]').fill(password)
    # TOTP-Code aus dem otpauth-URI ueber die System-Bibliothek berechnen
    import base64
    import hashlib
    import hmac
    import struct
    import time as t
    import urllib.parse
    parsed = urllib.parse.urlparse(otpauth_uri)
    qs = urllib.parse.parse_qs(parsed.query)
    secret_b32 = qs["secret"][0]
    key = base64.b32decode(secret_b32 + "=" * (-len(secret_b32) % 8))
    counter = int(t.time() // 30)
    msg = struct.pack(">Q", counter)
    hmac_digest = hmac.new(key, msg, hashlib.sha1).digest()
    offset = hmac_digest[-1] & 0x0F
    code_int = (struct.unpack(">I", hmac_digest[offset:offset + 4])[0] & 0x7FFFFFFF) % 1000000
    totp_code = f"{code_int:06d}"
    page.locator('input[name="totp"]').fill(totp_code)
    page.locator('button[type="submit"]').click()
    page.wait_for_url(f"{BASE}/ui/", timeout=10000)


def main() -> int:
    creds = _read_creds()
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()
        _login(page, creds["password"], creds["otpauth_uri"])
        page.wait_for_load_state("networkidle")
        time.sleep(0.5)

        # Screenshot 1: Uebersicht (Rail + Logout-Vorsicht-Farbe sichtbar)
        page.screenshot(path=str(OUT_DIR / "p86_block_b_01_overview.png"))
        print("OK 01 Uebersicht -- Rail + Logout sichtbar")

        # Screenshot 2: Liste mit Hover -- quiet-Selektion sichtbar
        page.locator(".list__row").first.hover()
        time.sleep(0.3)
        page.screenshot(path=str(OUT_DIR / "p86_block_b_02_list_hover.png"))
        print("OK 02 Liste-Hover -- quiet-Selektion pruefbar")

        # Screenshot 3: Editor geoeffnet -- Archivieren in Vorsicht-Farbe
        page.locator(".list__row").first.click()
        page.wait_for_load_state("networkidle")
        time.sleep(0.5)
        page.screenshot(path=str(OUT_DIR / "p86_block_b_03_editor.png"))
        print("OK 03 Editor -- Archivieren-Vorsicht sichtbar")

        # Screenshot 4: Konto-Dialog -- Update-Log + Spaces-verwalten als Navigation
        page.locator("#account-button").click()
        page.wait_for_selector("#account-dialog:not([hidden])", timeout=3000)
        time.sleep(0.3)
        page.screenshot(path=str(OUT_DIR / "p86_block_b_04_account_dialog.png"))
        print("OK 04 Konto-Dialog -- Navigation sichtbar")

        browser.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
