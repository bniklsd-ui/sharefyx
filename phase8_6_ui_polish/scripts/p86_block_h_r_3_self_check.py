#!/usr/bin/env python3
"""Phase 8.6 Block H-R-3 -- Selbst-Screenshots + Probe fuer H-R.6/H-R.7/H-R.8.

Vier Bilder, ein Probe-JSON. Login/TOTP-Helfer entliehen aus
p86_block_h_r_part2_self_check.py (identische Wegwerf-Instanz v3ritt, Port 18773).

  01_1440_editor_open           -- 1440 px, Item offen: Listen-Slot weg (H-R.8),
                                    Rail bleibt (kein H-R.7 bei Desktop-Breite).
  02_1024_list_only             -- 1024 px, Uebersicht: keine Karte mehr (H-R.6).
  03_1024_editor_fullview       -- 1024 px, Item offen: Rail + Liste weg,
                                    Editor fuellt den Viewport (H-R.7).
  04_1200_editor_open           -- 1200 px Kontrolle, Item offen: wie 1440 --
                                    H-R.7 darf bei 1200 NICHT greifen.

Probe: `getComputedStyle` auf .rail/.list/.detail__graph + `dataset.view` pro
Screenshot, geschrieben nach probes/h_r_3_probe.json.
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
PROBE_DIR = REPO_ROOT / "phase8_6_ui_polish" / "probes"
PROBE_DIR.mkdir(parents=True, exist_ok=True)

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


def open_first_item(page: Page) -> bool:
    page.goto(f"{BASE_URL}/ui/", wait_until="domcontentloaded")
    page.wait_for_load_state("networkidle", timeout=5000)
    time.sleep(0.5)
    try:
        page.locator(".tree__scope").first.click()
    except Exception:
        page.locator("#home-button").click()
        time.sleep(0.5)
        page.locator(".tree__scope").first.click()
    page.wait_for_load_state("networkidle", timeout=5000)
    time.sleep(0.4)
    first_row = page.locator(".list__row").first
    if first_row.count() == 0:
        print("ABBRUCH: kein Item in der Liste gefunden.", file=sys.stderr)
        return False
    first_row.click()
    page.wait_for_load_state("networkidle", timeout=5000)
    time.sleep(0.4)
    return True


def probe_layout(page: Page) -> dict:
    return page.evaluate(
        """() => {
            const shell = document.querySelector('.shell');
            const rail = document.querySelector('.rail');
            const list = document.querySelector('.list');
            const graph = document.querySelector('.detail__graph');
            const cs = el => el ? getComputedStyle(el).display : null;
            return {
                dataset_view: shell ? shell.dataset.view : null,
                rail_display: cs(rail),
                list_display: cs(list),
                detail_graph_display: cs(graph),
                shell_grid_template_columns: shell ? getComputedStyle(shell).gridTemplateColumns : null,
                viewport: {width: window.innerWidth, height: window.innerHeight},
            };
        }"""
    )


def shot(page: Page, name: str) -> Path:
    path = OUT_DIR / name
    page.screenshot(path=str(path))
    print(f"  shot: {path.name}", file=sys.stderr)
    return path


def main() -> int:
    creds = json.loads(CREDS_PATH.read_text())
    results: dict[str, object] = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "probes": {},
        "screenshots": [],
    }

    with sync_playwright() as p:
        browser = p.chromium.launch()

        # === 1440 px: editor open, list slot must be gone (H-R.8) ==============
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        status, note = login(page, creds["password"], creds["otpauth_uri"])
        if status not in (200, 303):
            print(f"ABBRUCH login 1440: status={status}, note={note}", file=sys.stderr)
            return 1
        _dismiss_update_banner(page)
        if not open_first_item(page):
            return 1
        results["probes"]["1440_editor_open"] = probe_layout(page)
        print(f"  1440 editor open: {json.dumps(results['probes']['1440_editor_open'])}",
              file=sys.stderr)
        path = shot(page, "p86_block_h_r_3_01_1440_editor_open.png")
        results["screenshots"].append(str(path.relative_to(REPO_ROOT)))
        ctx.close()

        # === 1200 px control: editor open, same as 1440 (H-R.7 must NOT leak) ==
        ctx = browser.new_context(viewport={"width": 1200, "height": 900})
        page = ctx.new_page()
        status, note = login(page, creds["password"], creds["otpauth_uri"])
        if status not in (200, 303):
            print(f"ABBRUCH login 1200: status={status}, note={note}", file=sys.stderr)
            return 1
        _dismiss_update_banner(page)
        if not open_first_item(page):
            return 1
        results["probes"]["1200_editor_open"] = probe_layout(page)
        print(f"  1200 editor open: {json.dumps(results['probes']['1200_editor_open'])}",
              file=sys.stderr)
        path = shot(page, "p86_block_h_r_3_04_1200_editor_open.png")
        results["screenshots"].append(str(path.relative_to(REPO_ROOT)))
        ctx.close()

        # === 1024x768: list-only (no map, H-R.6) + editor fullview (H-R.7) =====
        ctx = browser.new_context(viewport={"width": 1024, "height": 768})
        page = ctx.new_page()
        status, note = login(page, creds["password"], creds["otpauth_uri"])
        if status not in (200, 303):
            print(f"ABBRUCH login 1024: status={status}, note={note}", file=sys.stderr)
            return 1
        _dismiss_update_banner(page)

        page.goto(f"{BASE_URL}/ui/", wait_until="domcontentloaded")
        page.wait_for_load_state("networkidle", timeout=5000)
        time.sleep(0.5)
        results["probes"]["1024_list_only"] = probe_layout(page)
        print(f"  1024 list-only: {json.dumps(results['probes']['1024_list_only'])}",
              file=sys.stderr)
        path = shot(page, "p86_block_h_r_3_02_1024_list_only.png")
        results["screenshots"].append(str(path.relative_to(REPO_ROOT)))

        if not open_first_item(page):
            return 1
        results["probes"]["1024_editor_fullview"] = probe_layout(page)
        print(f"  1024 editor fullview: {json.dumps(results['probes']['1024_editor_fullview'])}",
              file=sys.stderr)
        path = shot(page, "p86_block_h_r_3_03_1024_editor_fullview.png")
        results["screenshots"].append(str(path.relative_to(REPO_ROOT)))
        ctx.close()

        browser.close()

    out_path = PROBE_DIR / "h_r_3_probe.json"
    out_path.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"\nProbe-JSON: {out_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
