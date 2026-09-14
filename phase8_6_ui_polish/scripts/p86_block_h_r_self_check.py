#!/usr/bin/env python3
"""Phase 8.6 Block H-R -- Self-Screenshots nach Sichtungs-Revision von Block H.

Drei Bilder, die H-R.1 (OLED-BLACK fuer die drei Slots) und H-R.2 (account-nav
Akzent-Farbe) belegen:

  p86_block_h_r_01_1440_uebersicht.png       -- 1440 px, Rail + Liste + Karte auf
                                                 schwarzem Grund; Karte "schwebt"
                                                 sichtbar (Layer 3 vs Layer 0)
  p86_block_h_r_02_1200_uebersicht.png       -- 1200 px, gleiches Layout, kein
                                                 Kollaps (N.13 gilt fuer alle
                                                 Breakpoints)
  p86_block_h_r_03_1440_konto_dialog.png     -- 1440 px, Konto-Dialog offen --
                                                 beide .account-nav-Knoepfe mit
                                                 Akzent-Fill + ring-border +
                                                 3-px-Akzentkante links +
                                                 Akzent-Chevron rechts (N.14
                                                 Spezialfall)

H-R.3/.4/.5 (Editor-YAML-Buendigkeit + 1024-er-Stapel-Reparaturen) sind in dieser
Session nicht gebaut -- ihre Screenshots kommen mit dem Folge-Block. Der
Drei-Bilder-Satz hier deckt nur den heutigen Bau ab.

Checkkriterium fuer alle drei Bilder (ein Satz, Konvention §5): "die drei Slots
(.rail/.list/.detail) tragen echtes OLED-BLACK, die Karte schwebt sichtbar als
--surface-Flaeche darauf; die .account-nav-Knoepfe im Konto-Dialog tragen
Akzent-Fill und sind sofort als wichtig erkennbar -- Einstellungen+Abmelden unten
in der Rail sind unveraendert."
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
OUT_DIR = REPO_ROOT / "docs" / "screenshots"
OUT_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_BASE_URL = "http://127.0.0.1:18773"
DEFAULT_CREDS = Path("/tmp/opencode/sharefyx-wegwerf-v3ritt/credentials.json")


def _read_creds(path: Path) -> dict[str, str]:
    return json.loads(path.read_text())


def _generate_totp(otpauth_uri: str) -> str:
    parsed = urllib.parse.urlparse(otpauth_uri)
    qs = urllib.parse.parse_qs(parsed.query)
    secret_b32 = qs["secret"][0]
    key = base64.b32decode(secret_b32 + "=" * (-len(secret_b32) % 8))
    counter = int(time.time() // 30)
    msg = struct.pack(">Q", counter)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    offset = h[-1] & 0x0F
    code_int = (struct.unpack(">I", h[offset:offset + 4])[0] & 0x7FFFFFFF) % 1000000
    return f"{code_int:06d}"


def login(page: Page, base_url: str, password: str, otpauth_uri: str) -> tuple[int, str]:
    secs_into = datetime.datetime.now().second
    wait = 35 - (secs_into % 30)
    print(f"Login: warte {wait}s auf frisches TOTP-Fenster ...", file=sys.stderr)
    time.sleep(wait)

    for window in range(2):
        page.goto(f"{base_url}/ui/login", wait_until="domcontentloaded")
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
            if not page.url.startswith(f"{base_url}/ui/"):
                page.goto(f"{base_url}/ui/", wait_until="domcontentloaded")
            return resp.status, "ok"
        if resp.status == 401:
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Block H-R self-check screenshots")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--creds", default=str(DEFAULT_CREDS))
    args = parser.parse_args(argv)

    creds = _read_creds(Path(args.creds))
    base = args.base_url

    with sync_playwright() as p:
        browser = p.chromium.launch()

        # --- 1440 px: Uebersicht (01) + Konto-Dialog (03) ---
        ctx1440 = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx1440.new_page()
        status, note = login(page, base, creds["password"], creds["otpauth_uri"])
        if status not in (200, 303):
            print(f"ABBRUCH login 1440: status={status}, note={note}", file=sys.stderr)
            return 1

        _dismiss_update_banner(page)

        # 01: Uebersicht bei 1440 -- schwarze Slots, Karte schwebt.
        page.goto(f"{base}/ui/", wait_until="domcontentloaded")
        page.wait_for_load_state("networkidle", timeout=5000)
        time.sleep(0.5)
        shot1 = OUT_DIR / "p86_block_h_r_01_1440_uebersicht.png"
        page.screenshot(path=str(shot1))
        print(f"OK 01: {shot1.name}", file=sys.stderr)

        # 03: Konto-Dialog offen -- Akzent-Fill auf beiden Knoepfen.
        page.locator("#account-button").click()
        page.wait_for_load_state("networkidle", timeout=5000)
        time.sleep(0.5)
        shot3 = OUT_DIR / "p86_block_h_r_03_1440_konto_dialog.png"
        page.screenshot(path=str(shot3))
        print(f"OK 03: {shot3.name}", file=sys.stderr)

        ctx1440.close()

        # --- 1200 px: Uebersicht (02) -- gleiches Layout, kein Kollaps ---
        ctx1200 = browser.new_context(viewport={"width": 1200, "height": 900})
        page = ctx1200.new_page()
        status, note = login(page, base, creds["password"], creds["otpauth_uri"])
        if status not in (200, 303):
            print(f"ABBRUCH login 1200: status={status}, note={note}", file=sys.stderr)
            return 1

        _dismiss_update_banner(page)

        # 02: Uebersicht bei 1200 -- schwarze Slots, kein Kollaps (P8.6-AH).
        page.goto(f"{base}/ui/", wait_until="domcontentloaded")
        page.wait_for_load_state("networkidle", timeout=5000)
        time.sleep(0.5)
        shot2 = OUT_DIR / "p86_block_h_r_02_1200_uebersicht.png"
        page.screenshot(path=str(shot2))
        print(f"OK 02: {shot2.name}", file=sys.stderr)

        ctx1200.close()

        browser.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
