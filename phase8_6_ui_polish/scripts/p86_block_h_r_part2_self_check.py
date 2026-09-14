#!/usr/bin/env python3
"""Phase 8.6 Block H-R Teil 2 -- CDP-Probe + Self-Screenshots.

V142/V143/V144 sind Mess-Vor-Bau-Schritte (Block-E-Methodik, Plan §3-§5).
Erst messen, dann fixen, dann re-messen.

Proben:

  V142 -- Editor-YAML-Buendigkeit zur Suchzeile
         boundingBox fuer .list__head und .editor__head bei 1440 und 1200 px
         (Editor offen). Bottom-Edges sollen gleich sein (Toleranz <= 2 px,
         H-R.3-A Abnahmekriterium).

  V143 -- 1024-er Map-Overlap
         boundingBox fuer .detail__graph, .list, .rail bei 1024x768
         (Uebersicht + Editor-Modus). Welche Lesart zutrifft (Hoehenkette /
         Padding-sprengt-Slot / Read-only-Modus-Overlap) wird durch die
         Rechteck-Schnittmenge sichtbar.

  V144 -- 1024-er Editor-Modus voll bedienbar
         elementFromPoint(cx, cy) pro Editor-Knopf bei 1024x768:
           #archive-button, #save-button, #close-button (im .editor__head)
           #toggle-preview (in .editor__toolbar)
           #append-button (in .editor__append)
           format-toolbar-Knoepfe (data-md="bold/italic/code/link/h/quote/ul/ol/hr/image")

Self-Screenshots (5 Bilder analog H-R Plan §11):

  p86_block_h_r_01_1440_uebersicht.png   -- Rail + Liste + Karte auf schwarzem Grund
  p86_block_h_r_02_1200_uebersicht.png   -- gleiches Layout, kein Kollaps
  p86_block_h_r_03_1440_editor_offen.png -- Editor offen, sticky-Header buendig
  p86_block_h_r_04_1024_uebersicht.png   -- Stapel: Liste oben, Karte unten
  p86_block_h_r_05_1024_editor_offen.png -- Editor im unteren Slot

Probe-JSON: phase8_6_ui_polish/probes/v142_v143_v144_pre_fix.json
            phase8_6_ui_polish/probes/v142_v143_v144_post_fix.json (zweiter Lauf)
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
PROBE_DIR = REPO_ROOT / "phase8_6_ui_polish" / "probes"
PROBE_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_BASE_URL = "http://127.0.0.1:18773"
DEFAULT_CREDS = Path("/tmp/opencode/sharefyx-wegwerf-v3ritt/credentials.json")


# --- Login (entliehen aus p86_block_h_r_self_check.py + p86_viewport_probe.py) --------


def _read_creds(path: Path) -> dict[str, str]:
    return json.loads(path.read_text())


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
            print("  TOTP verbraucht, warte 35s auf naechstes Fenster...", file=sys.stderr)
            time.sleep(35)
            continue
        return resp.status, f"http_{resp.status}"
    return 0, "tries_exhausted"


def _dismiss_update_banner(page: Page) -> None:
    """Update-Banner wegklicken, falls sichtbar -- sonst blockiert es Knöpfe."""
    try:
        dismiss = page.locator("#update-banner-dismiss")
        if dismiss.is_visible(timeout=1000):
            dismiss.click()
            time.sleep(0.3)
    except Exception:
        pass


# --- Probe-Funktionen ---------------------------------------------------------


def probe_v142(page: Page) -> dict:
    """V142 -- Editor-YAML-Buendigkeit.

    Liefert boundingBox von .list__head und .editor__head (Editor offen).
    Beide bottom-Edges sollen gleich sein (Toleranz <= 2 px).
    """
    out: dict[str, object] = {}
    for sel in (".list__head", ".editor__head"):
        loc = page.locator(sel)
        if loc.count() == 0:
            out[sel] = None
            continue
        rect = loc.first.evaluate(
            """el => {
                const r = el.getBoundingClientRect();
                const cs = getComputedStyle(el);
                return {
                    x: r.x, y: r.y, width: r.width, height: r.height,
                    bottom: r.bottom, top: r.top,
                    paddingTop: cs.paddingTop, paddingBottom: cs.paddingBottom,
                };
            }"""
        )
        out[sel] = rect

    if out[".list__head"] and out[".editor__head"]:
        lh = out[".list__head"]
        eh = out[".editor__head"]
        out["diff_bottom_px"] = abs(lh["bottom"] - eh["bottom"])
        out["diff_top_px"] = abs(lh["top"] - eh["top"])
        out["tolerance_ok"] = out["diff_bottom_px"] <= 2.0
    return out


def probe_v143(page: Page) -> dict:
    """V143 -- 1024-er Map-Overlap.

    Liefert boundingBox von .detail__graph, .list, .rail.
    Prueft paarweise Rechteck-Schnittmenge (overlap > 0 == Problem).
    """
    rects: dict[str, dict | None] = {}
    for sel in (".detail__graph", ".list", ".rail", ".overview__graph"):
        loc = page.locator(sel)
        if loc.count() == 0:
            rects[sel] = None
            continue
        rect = loc.first.evaluate(
            """el => {
                const r = el.getBoundingClientRect();
                return {x: r.x, y: r.y, width: r.width, height: r.height,
                        bottom: r.bottom, top: r.top, right: r.right, left: r.left};
            }"""
        )
        rects[sel] = rect

    def overlap(a: dict, b: dict) -> float:
        if not a or not b:
            return 0.0
        x_overlap = max(0.0, min(a["right"], b["right"]) - max(a["left"], b["left"]))
        y_overlap = max(0.0, min(a["bottom"], b["bottom"]) - max(a["top"], b["top"]))
        return x_overlap * y_overlap

    out = {
        "rects": rects,
        "overlap_list_x_detail_graph": overlap(rects.get(".list"), rects.get(".detail__graph")),
        "overlap_rail_x_detail_graph": overlap(rects.get(".rail"), rects.get(".detail__graph")),
        "overlap_rail_x_list": overlap(rects.get(".rail"), rects.get(".list")),
    }
    # any overlap > 0 means overlap problem
    out["any_overlap"] = any(v > 0 for v in [
        out["overlap_list_x_detail_graph"],
        out["overlap_rail_x_detail_graph"],
        out["overlap_rail_x_list"],
    ])
    return out


def probe_v144(page: Page) -> dict:
    """V144 -- 1024-er Editor voll bedienbar.

    elementFromPoint(cx, cy) pro Knopf:
      .editor__head-actions: #archive-button, #save-button, #close-button
      .editor__toolbar: format-Knoepfe + #toggle-preview
      .editor__append: #append-button
    """
    return page.evaluate(
        """() => {
            const sels = [
                '#archive-button', '#save-button', '#close-button',
                '[data-md=\"bold\"]', '[data-md=\"italic\"]', '[data-md=\"code\"]',
                '[data-md=\"link\"]', '[data-md=\"h\"]', '[data-md=\"quote\"]',
                '[data-md=\"ul\"]', '[data-md=\"ol\"]', '[data-md=\"hr\"]',
                '#insert-image-button', '#toggle-preview',
                '#append-button', '#append-input',
            ];
            return sels.map(sel => {
                const b = document.querySelector(sel);
                if (!b) return {selector: sel, present: false};
                const r = b.getBoundingClientRect();
                const cx = r.left + r.width / 2;
                const cy = r.top + r.height / 2;
                let hit = null;
                let hitTag = null;
                try {
                    const el = document.elementFromPoint(cx, cy);
                    hit = el ? (el === b || b.contains(el) ? 'self' : (el.id || el.tagName + (el.className ? '.' + el.className : ''))) : null;
                    hitTag = el ? el.tagName : null;
                } catch (e) {
                    hit = 'error:' + e.message;
                }
                const offscreen = (r.bottom > window.innerHeight || r.top < 0 || r.right > window.innerWidth || r.left < 0);
                return {
                    selector: sel,
                    present: true,
                    rect: {x: r.x, y: r.y, width: r.width, height: r.height,
                           bottom: r.bottom, top: r.top},
                    reachable: hit === 'self',
                    hit_at_center: hit,
                    hit_tag: hitTag,
                    offscreen,
                };
            });
        }"""
    )


# --- Screenshot-Helfer ---------------------------------------------------------


def screenshot_overview(page: Page, name: str) -> Path:
    page.goto(f"{DEFAULT_BASE_URL}/ui/", wait_until="domcontentloaded")
    page.wait_for_load_state("networkidle", timeout=5000)
    time.sleep(0.5)
    path = OUT_DIR / name
    page.screenshot(path=str(path))
    print(f"  shot: {path.name}", file=sys.stderr)
    return path


def open_first_item_editor(page: Page) -> bool:
    """Oeffnet das erste Item in der Liste und stellt sicher, dass der Editor sichtbar ist."""
    page.goto(f"{DEFAULT_BASE_URL}/ui/", wait_until="domcontentloaded")
    page.wait_for_load_state("networkidle", timeout=5000)
    time.sleep(0.5)
    # Wechsle in die Item-Liste (nicht Uebersicht) durch Klick auf "Alle Items"
    try:
        page.locator(".tree__scope").first.click()
    except Exception:
        page.locator("#home-button").click()
        time.sleep(0.5)
        page.locator(".tree__scope").first.click()
    page.wait_for_load_state("networkidle", timeout=5000)
    time.sleep(0.4)
    # erstes Item in der Liste anklicken
    first_row = page.locator(".list__row").first
    if first_row.count() == 0:
        print("ABBRUCH: kein Item in der Liste gefunden.", file=sys.stderr)
        return False
    first_row.click()
    page.wait_for_load_state("networkidle", timeout=5000)
    time.sleep(0.4)
    # Sicher ist der Editor sichtbar (nicht nur Read-only)
    editor_visible = page.locator("#detail-editor").is_visible()
    if not editor_visible:
        # Im Read-only-Modus koennten wir nicht editieren -- aber fuer V142 brauchen wir
        # nur die Bounds, Read-only reicht. Wir loggen es aber.
        print("  Hinweis: Editor nicht sichtbar (Read-only? / fremder Space?)", file=sys.stderr)
    return True


def screenshot_editor(page: Page, name: str) -> Path:
    path = OUT_DIR / name
    page.screenshot(path=str(path))
    print(f"  shot: {path.name}", file=sys.stderr)
    return path


# --- Main ---------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Block H-R Teil 2: V142/V143/V144 + screenshots")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--creds", default=str(DEFAULT_CREDS))
    parser.add_argument("--label", default="pre_fix",
                        help="JSON-Label (pre_fix / post_fix / final)")
    args = parser.parse_args(argv)

    creds = _read_creds(Path(args.creds))
    base = args.base_url

    results: dict[str, object] = {
        "label": args.label,
        "base_url": base,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "v142": {},
        "v143": {},
        "v144": {},
        "screenshots": [],
    }

    with sync_playwright() as p:
        browser = p.chromium.launch()

        # === 1440 px: V142 + V143 + Uebersicht + Editor-Screenshots ============
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        status, note = login(page, base, creds["password"], creds["otpauth_uri"])
        if status not in (200, 303):
            print(f"ABBRUCH login 1440: status={status}, note={note}", file=sys.stderr)
            return 1
        _dismiss_update_banner(page)

        # --- V142 bei 1440 ---
        # Screenshot 01: Uebersicht
        shot = screenshot_overview(page, "p86_block_h_r_01_1440_uebersicht.png")
        results["screenshots"].append(str(shot.relative_to(REPO_ROOT)))

        # Editor oeffnen
        if open_first_item_editor(page):
            # V142 messen
            results["v142"]["1440"] = probe_v142(page)
            print(f"  V142 1440: {json.dumps(results['v142']['1440'])}", file=sys.stderr)
            # Screenshot 03: Editor offen bei 1440
            shot = screenshot_editor(page, "p86_block_h_r_03_1440_editor_offen.png")
            results["screenshots"].append(str(shot.relative_to(REPO_ROOT)))

        ctx.close()

        # === 1200 px: V142 + Uebersicht-Screenshot ============================
        ctx = browser.new_context(viewport={"width": 1200, "height": 900})
        page = ctx.new_page()
        status, note = login(page, base, creds["password"], creds["otpauth_uri"])
        if status not in (200, 303):
            print(f"ABBRUCH login 1200: status={status}, note={note}", file=sys.stderr)
            return 1
        _dismiss_update_banner(page)

        # Screenshot 02: Uebersicht bei 1200 (H-R.1 Akzent-Fill auf .account-nav
        # war bei 1200 schon in H-R-Teil-1 gezeigt; hier ohne Konto-Dialog)
        shot = screenshot_overview(page, "p86_block_h_r_02_1200_uebersicht.png")
        results["screenshots"].append(str(shot.relative_to(REPO_ROOT)))

        # V142 bei 1200 -- Editor offen
        if open_first_item_editor(page):
            results["v142"]["1200"] = probe_v142(page)
            print(f"  V142 1200: {json.dumps(results['v142']['1200'])}", file=sys.stderr)

        ctx.close()

        # === 1024x768: V143 + V144 + 2 Screenshots ==========================
        ctx = browser.new_context(viewport={"width": 1024, "height": 768})
        page = ctx.new_page()
        status, note = login(page, base, creds["password"], creds["otpauth_uri"])
        if status not in (200, 303):
            print(f"ABBRUCH login 1024: status={status}, note={note}", file=sys.stderr)
            return 1
        _dismiss_update_banner(page)

        # --- V143 / Uebersicht ---
        # Screenshot 04: Uebersicht 1024
        shot = screenshot_overview(page, "p86_block_h_r_04_1024_uebersicht.png")
        results["screenshots"].append(str(shot.relative_to(REPO_ROOT)))
        # V143 messen (Uebersicht-Modus)
        results["v143"]["1024_overview"] = probe_v143(page)
        print(f"  V143 1024 overview: {json.dumps(results['v143']['1024_overview'])}",
              file=sys.stderr)

        # --- V143 / V144 / Editor ---
        if open_first_item_editor(page):
            results["v143"]["1024_editor"] = probe_v143(page)
            print(f"  V143 1024 editor: {json.dumps(results['v143']['1024_editor'])}",
                  file=sys.stderr)
            results["v144"]["1024"] = probe_v144(page)
            print(f"  V144 1024: {json.dumps(results['v144']['1024'])}", file=sys.stderr)
            # Screenshot 05: Editor 1024
            shot = screenshot_editor(page, "p86_block_h_r_05_1024_editor_offen.png")
            results["screenshots"].append(str(shot.relative_to(REPO_ROOT)))

        ctx.close()
        browser.close()

    # JSON schreiben
    out_path = PROBE_DIR / f"v142_v143_v144_{args.label}.json"
    out_path.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"\nProbe-JSON: {out_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())