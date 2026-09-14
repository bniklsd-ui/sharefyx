#!/usr/bin/env python3
"""Phase 8.6 Block G -- Self-Screenshots nach Plan §4.9 + §5-Konvention.

Sechs Bilder, die den Layout-Umbau zeigen:
  p86_block_g_01_1440_uebersicht.png        -- 1440 px, Übersicht im Listen-Slot, Karte im Detail-Slot
  p86_block_g_02_1440_space_geoeffnet.png   -- 1440 px, nach Klick auf eine Space-Zeile in der Übersicht
                                              (zeigt, dass die ganze Zeile inkl. Chip-Leiste klickbar ist)
  p86_block_g_03_1440_editor_offen.png      -- 1440 px, Editor offen in der Karte (Editor ersetzt die Karte)
  p86_block_g_04_1440_editor_nach_esc.png   -- 1440 px, nach ESC im Editor (Karte ist zurück)
  p86_block_g_05_1200_uebersicht.png        -- 1200 px, Übersicht (Grid kollabiert unter 1280px weg -- Befund 9b)
  p86_block_g_06_1024_uebersicht.png        -- 1024 px, Übersicht (zweispaltig .shell wird eingeschoben)

Checkkriterium fuer alle Bilder (ein Satz): ".shell ist 240/480/1fr, die Uebersicht
(Spaces + Zuletzt benutzt) lebt im Listen-Slot, die Karte hat den Detail-Slot allein --
Befund 5 ist weg."
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Block G self-check screenshots")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--creds", default=str(DEFAULT_CREDS))
    args = parser.parse_args(argv)

    creds = _read_creds(Path(args.creds))
    base = args.base_url

    with sync_playwright() as p:
        browser = p.chromium.launch()

        # --- 1440 px ---
        ctx1440 = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx1440.new_page()
        status, note = login(page, base, creds["password"], creds["otpauth_uri"])
        if status not in (200, 303):
            print(f"ABBRUCH login: status={status}, note={note}", file=sys.stderr)
            return 1

        # 01: Übersicht (Startzustand nach Login).
        page.goto(f"{base}/ui/", wait_until="domcontentloaded")
        page.wait_for_load_state("networkidle", timeout=5000)
        time.sleep(0.5)
        shot1 = OUT_DIR / "p86_block_g_01_1440_uebersicht.png"
        page.screenshot(path=str(shot1))
        print(f"OK 01: {shot1.name}", file=sys.stderr)

        # 02: Eine Space-Zeile in der Übersicht klicken -- wechselt in den Space und zeigt die
        # Item-Liste im Listen-Slot, die Karte weiterhin im Detail-Slot.
        # Die Space-Zeile ist ein Button .overview__space-open, darin der erste Space (alpha,
        # der eigene, ganz oben).
        page.locator(".overview__space-open").first.click()
        page.wait_for_load_state("networkidle", timeout=5000)
        time.sleep(0.5)
        shot2 = OUT_DIR / "p86_block_g_02_1440_space_geoeffnet.png"
        page.screenshot(path=str(shot2))
        print(f"OK 02: {shot2.name}", file=sys.stderr)

        # 03: Ein Item öffnen -- Editor ersetzt die Karte im Detail-Slot. ESC bringt die
        # Karte zurück (04).
        page.locator(".list__row").first.click()
        page.wait_for_load_state("networkidle", timeout=5000)
        time.sleep(0.5)
        shot3 = OUT_DIR / "p86_block_g_03_1440_editor_offen.png"
        page.screenshot(path=str(shot3))
        print(f"OK 03: {shot3.name}", file=sys.stderr)

        # 04: ESC im Editor -- die Karte (Detail-Graph) kommt zurück, Editor verschwindet.
        page.keyboard.press("Escape")
        time.sleep(0.5)
        shot4 = OUT_DIR / "p86_block_g_04_1440_editor_nach_esc.png"
        page.screenshot(path=str(shot4))
        print(f"OK 04: {shot4.name}", file=sys.stderr)

        ctx1440.close()

        # --- 1200 px (unter dem 1280-px-Breakpoint: Rail-Labels verschwinden, .shell bleibt 3-spaltig) ---
        ctx1200 = browser.new_context(viewport={"width": 1200, "height": 900})
        page = ctx1200.new_page()
        status, note = login(page, base, creds["password"], creds["otpauth_uri"])
        if status not in (200, 303):
            print(f"ABBRUCH login 1200: status={status}, note={note}", file=sys.stderr)
            return 1
        page.wait_for_load_state("networkidle", timeout=5000)
        time.sleep(0.5)
        shot5 = OUT_DIR / "p86_block_g_05_1200_uebersicht.png"
        page.screenshot(path=str(shot5))
        print(f"OK 05: {shot5.name}", file=sys.stderr)
        ctx1200.close()

        # --- 1024 px (zweispaltig: .shell[data-view=list] versteckt .detail) ---
        ctx1024 = browser.new_context(viewport={"width": 1024, "height": 900})
        page = ctx1024.new_page()
        status, note = login(page, base, creds["password"], creds["otpauth_uri"])
        if status not in (200, 303):
            print(f"ABBRUCH login 1024: status={status}, note={note}", file=sys.stderr)
            return 1
        page.wait_for_load_state("networkidle", timeout=5000)
        time.sleep(0.5)
        shot6 = OUT_DIR / "p86_block_g_06_1024_uebersicht.png"
        page.screenshot(path=str(shot6))
        print(f"OK 06: {shot6.name}", file=sys.stderr)
        ctx1024.close()

        browser.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
