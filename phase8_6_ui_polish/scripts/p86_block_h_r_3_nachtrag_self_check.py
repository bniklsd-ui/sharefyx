#!/usr/bin/env python3
"""Phase 8.6 Block H-R-3 Nachtrag -- Rail-Exklusivitaet Uebersicht vs. Space/Eimer.

Nikinger-Fund 2026-09-17 (aus dem 03_1024_ohne_karte.png-Screenshot): beim Wechsel in die
Uebersicht blieb ein zuvor besuchter Eimer (z.B. "alpha -> Offen") im Rail weiterhin
`aria-current="true"` -- zwei "aktuelle" Rail-Eintraege fuer zwei verschiedene Aktionen
gleichzeitig. Ursache: `renderFolders()`/`folderButton()`/`homeButtonEl`s aria-current-Logik
in tree.js pruefte nie `state.overview`.

Reproduktion + Beweis-Screenshot: in die Uebersicht wechseln, "alpha" aufklappen, "Offen"
anklicken (state.activeSpace="alpha", state.filter="open", state.overview=false), dann
"Uebersicht" anklicken (state.overview=true) -- vorher waere "Offen" weiterhin markiert
geblieben.
"""
from __future__ import annotations

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
OUT_DIR = REPO_ROOT / "docs" / "screenshots"
OUT_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "http://127.0.0.1:18773"
CREDS_PATH = Path("/tmp/opencode/sharefyx-wegwerf-v3ritt/credentials.json")


def _generate_totp(otpauth_uri: str) -> str:
    parsed = urllib.parse.urlparse(otpauth_uri)
    qs = urllib.parse.parse_qs(parsed.query)
    secret_b32 = qs["secret"][0]
    key = base64.b32decode(secret_b32 + "=" * (-len(secret_b32) % 8))
    counter = int(time.time() // 30)
    msg = struct.pack(">q", counter)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    offset = h[-1] & 0x0F
    code_int = (struct.unpack(">I", h[offset:offset + 4])[0] & 0x7FFFFFFF) % 1000000
    return f"{code_int:06d}"


def login(page: Page, password: str, otpauth_uri: str) -> tuple[int, str]:
    secs_into = datetime.datetime.now().second
    wait = 35 - (secs_into % 30)
    print(f"Login: warte {wait}s auf frisches TOTP-Fenster ...", file=sys.stderr)
    time.sleep(wait)
    for window in range(2):
        page.goto(f"{BASE_URL}/ui/login", wait_until="domcontentloaded")
        page.locator('input[name="space"]').fill("alpha")
        page.locator('input[name="password"]').fill(password)
        totp_code = _generate_totp(otpauth_uri)
        print(f"  Fenster {window + 1}: TOTP {totp_code}", file=sys.stderr)
        page.locator('input[name="totp"]').fill(totp_code)
        with page.expect_response("**/ui/login**") as resp_info:
            page.locator('button[type="submit"]').click()
        resp = resp_info.value
        print(f"  Fenster {window + 1}: HTTP {resp.status}", file=sys.stderr)
        if resp.status in (200, 303):
            time.sleep(3.0)
            if not page.url.startswith(f"{BASE_URL}/ui/"):
                page.goto(f"{BASE_URL}/ui/", wait_until="domcontentloaded")
            return resp.status, "ok"
        if resp.status == 401:
            print("  TOTP verbraucht, warte 35s auf naechstes Fenster...", file=sys.stderr)
            time.sleep(35)
            continue
        return resp.status, f"http_{resp.status}"
    return 0, "tries_exhausted"


def _dismiss_update_banner(page: Page) -> None:
    try:
        dismiss = page.locator("#update-banner-dismiss")
        if dismiss.is_visible(timeout=1000):
            dismiss.click()
            time.sleep(0.3)
    except Exception:
        pass


def probe_current(page: Page) -> dict:
    return page.evaluate(
        """() => {
            const cur = el => el ? el.getAttribute('aria-current') : null;
            const home = document.querySelector('#home-button');
            const offen = Array.from(document.querySelectorAll('.tree__folder'))
                .find(b => b.textContent.includes('Offen'));
            const allItems = document.querySelector('.tree__scope');
            return {
                home_aria_current: cur(home),
                offen_aria_current: cur(offen),
                all_items_aria_current: cur(allItems),
            };
        }"""
    )


def main() -> int:
    creds = json.loads(CREDS_PATH.read_text())

    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1024, "height": 768})
        page = ctx.new_page()
        status, note = login(page, creds["password"], creds["otpauth_uri"])
        if status not in (200, 303):
            print(f"ABBRUCH login: status={status}, note={note}", file=sys.stderr)
            return 1
        _dismiss_update_banner(page)

        page.goto(f"{BASE_URL}/ui/", wait_until="domcontentloaded")
        page.wait_for_load_state("networkidle", timeout=5000)
        time.sleep(0.5)

        # alpha aufklappen, "Offen" anklicken -- state.activeSpace="alpha", filter="open"
        page.locator(".tree__space", has_text="alpha").first.click()
        time.sleep(0.3)
        page.locator(".tree__folder", has_text="Offen").first.click()
        page.wait_for_load_state("networkidle", timeout=5000)
        time.sleep(0.4)
        pre = probe_current(page)
        print(f"  nach 'Offen'-Klick: {json.dumps(pre)}", file=sys.stderr)

        # zurueck in die Uebersicht
        page.locator("#home-button").click()
        page.wait_for_load_state("networkidle", timeout=5000)
        time.sleep(0.5)
        post = probe_current(page)
        print(f"  nach 'Uebersicht'-Klick: {json.dumps(post)}", file=sys.stderr)

        path = OUT_DIR / "p86_block_h_r_3_nachtrag_uebersicht_exklusiv.png"
        page.screenshot(path=str(path))
        print(f"  shot: {path.name}", file=sys.stderr)

        ok = (
            post["home_aria_current"] == "true"
            and post["offen_aria_current"] != "true"
            and post["all_items_aria_current"] != "true"
        )
        print(f"\nErgebnis: {'OK -- exklusiv' if ok else 'FEHLER -- doppelt markiert'}",
              file=sys.stderr)

        ctx.close()
        browser.close()

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
