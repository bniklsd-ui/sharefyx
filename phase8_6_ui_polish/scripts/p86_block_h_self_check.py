#!/usr/bin/env python3
"""Phase 8.6 Block H -- Self-Screenshots nach Sichtung der Plan-2-§5-Fixes.

Drei Bilder, die die zwei Fixes aus Block H belegen:
  p86_block_h_01_1440_rail.png         -- 1440 px, Rail mit Einstellungen+Abmelden am Ende (Befund 7b)
  p86_block_h_02_1200_rail.png         -- 1200 px, gleiches Rail-Layout, kein Kollaps (P8.6-AH: Konto-Dialog-Knöpfe
                                          müssen auch im schmalen Viewport sichtbar bleiben)
  p86_block_h_03_1440_konto_dialog.png -- 1440 px, Konto-Dialog offen -- beide .account-nav-Knöpfe mit
                                          linker Akzentkante + Chevron rechts (Befund 2)

Checkkriterium fuer alle Bilder (ein Satz, Konvention §5): ".rail__account trägt jetzt
beide Knöpfe (Einstellungen oben, Abmelden unten, Abmelden ist der äußerste Knopf im
Rail), und die .account-nav-Knöpfe im Konto-Dialog sind durch linke Akzentkante +
rechtes Chevron-Icon sichtbar als bedienbar erkennbar".
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
        if resp.status == 429:
            time.sleep(65)
            continue
        return resp.status, f"http_{resp.status}"
    return 0, "tries_exhausted"


def _dismiss_update_banner(page: Page) -> None:
    """Update-Banner wegklicken, damit der nicht in allen Screenshots dasselbe ist."""
    try:
        dismiss = page.locator("#update-banner-dismiss")
        if dismiss.is_visible(timeout=1000):
            dismiss.click()
            time.sleep(0.3)
    except Exception:
        pass


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Block H self-check screenshots")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--creds", default=str(DEFAULT_CREDS))
    args = parser.parse_args(argv)

    creds = _read_creds(Path(args.creds))
    base = args.base_url

    with sync_playwright() as p:
        browser = p.chromium.launch()

        # --- 1440 px: Rail (01) + Konto-Dialog (03) ---
        ctx1440 = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx1440.new_page()
        status, note = login(page, base, creds["password"], creds["otpauth_uri"])
        if status not in (200, 303):
            print(f"ABBRUCH login 1440: status={status}, note={note}", file=sys.stderr)
            return 1

        _dismiss_update_banner(page)

        # 01: Rail mit beiden Knöpfen unten (Einstellungen vor Abmelden, Abmelden ist letztes).
        page.goto(f"{base}/ui/", wait_until="domcontentloaded")
        page.wait_for_load_state("networkidle", timeout=5000)
        time.sleep(0.5)
        shot1 = OUT_DIR / "p86_block_h_01_1440_rail.png"
        page.screenshot(path=str(shot1))
        print(f"OK 01: {shot1.name}", file=sys.stderr)

        # 03: Konto-Dialog offen -- beide .account-nav-Knöpfe mit Akzentkante + Chevron.
        page.locator("#account-button").click()
        page.wait_for_load_state("networkidle", timeout=5000)
        time.sleep(0.5)
        shot3 = OUT_DIR / "p86_block_h_03_1440_konto_dialog.png"
        page.screenshot(path=str(shot3))
        print(f"OK 03: {shot3.name}", file=sys.stderr)

        ctx1440.close()

        # --- 1200 px: Rail (02) -- gleiches Layout, kein Kollaps ---
        ctx1200 = browser.new_context(viewport={"width": 1200, "height": 900})
        page = ctx1200.new_page()
        status, note = login(page, base, creds["password"], creds["otpauth_uri"])
        if status not in (200, 303):
            print(f"ABBRUCH login 1200: status={status}, note={note}", file=sys.stderr)
            return 1

        _dismiss_update_banner(page)

        # 02: Rail bei 1200 -- Rail 240 bleibt, beide Knöpfe unten, kein Kollaps.
        page.goto(f"{base}/ui/", wait_until="domcontentloaded")
        page.wait_for_load_state("networkidle", timeout=5000)
        time.sleep(0.5)
        shot2 = OUT_DIR / "p86_block_h_02_1200_rail.png"
        page.screenshot(path=str(shot2))
        print(f"OK 02: {shot2.name}", file=sys.stderr)

        ctx1200.close()

        browser.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())