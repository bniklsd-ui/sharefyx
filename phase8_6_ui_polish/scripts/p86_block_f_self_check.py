#!/usr/bin/env python3
"""Phase 8.6 Block F -- Self-Screenshots nach Plan §3.5 + §5-Konvention.

Zwei Bilder, die zeigen, dass die Kopfdaten-Linie nicht mehr warn-getönt ist:
  p86_block_f_01_editor_meta_open.png  -- Editor mit geoeffnetem Meta-Panel
                                         (zeigt die Linie zwischen Head und Feldern)
  p86_block_f_02_editor_append_row.png -- Editor mit Fokus auf der 'Zeile anhaengen'-
                                         Zeile (eigene Flaeche, Oberkante).

Checkkriterium fuer beide Bilder (ein Satz): "das Meta-Panel zeigt eine kuehle
Layer-2-Flaeche (--surface = #14181D), die vorher warm-getoent war -- Befund 8
ist weg."
"""
from __future__ import annotations

import argparse
import base64
import datetime
import hashlib
import hmac
import json
import os
import re
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
    parser = argparse.ArgumentParser(description="Block F self-check screenshots")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--creds", default=str(DEFAULT_CREDS))
    args = parser.parse_args(argv)

    creds = _read_creds(Path(args.creds))
    base = args.base_url

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        status, note = login(page, base, creds["password"], creds["otpauth_uri"])
        if status not in (200, 303):
            print(f"ABBRUCH login: status={status}, note={note}", file=sys.stderr)
            return 1

        # Open the first item in alpha (read-only editor default).
        page.goto(f"{base}/ui/", wait_until="domcontentloaded")
        page.wait_for_load_state("networkidle", timeout=5000)
        page.locator(".list__row").first.click()
        page.wait_for_load_state("networkidle", timeout=5000)
        time.sleep(0.5)

        # Screenshot 01: read-only editor, meta-panel collapsed to head row,
        # the linie zwischen Head und Feldern ist jetzt die Standard-Haarlinie
        # (var(--line)) statt warn-getönt.
        shot1 = OUT_DIR / "p86_block_f_01_editor_meta_open.png"
        page.screenshot(path=str(shot1))
        print(f"OK 01: {shot1.name}", file=sys.stderr)

        # Screenshot 02: in den Edit-Modus wechseln (klick auf "Bearbeiten"), damit
        # die .editor__append-Zeile sichtbar wird -- die ist Layer 2 ueber Layer 3
        # (Body), nicht "irgendwo im Layer".
        edit_btn = page.locator("button:has-text('Bearbeiten')")
        if edit_btn.count() > 0:
            edit_btn.first.click()
            page.wait_for_load_state("networkidle", timeout=3000)
            time.sleep(0.5)
        # Sicherstellen, dass die Append-Zeile sichtbar ist.
        append_row = page.locator(".editor__append")
        if append_row.count() > 0:
            append_row.first.scroll_into_view_if_needed()
            time.sleep(0.3)
        shot2 = OUT_DIR / "p86_block_f_02_editor_append_row.png"
        page.screenshot(path=str(shot2))
        print(f"OK 02: {shot2.name}", file=sys.stderr)

        browser.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
