#!/usr/bin/env python3
"""Phase 8.6 Block E -- CDP-Viewport-Probe (Plan §2.2, messen nicht bauen).

Erhebt pro Breite (1024/1200/1440 px) fuer die uebersichtsseite der laufenden
Sharefyx-Instanz:

  rects    -- getBoundingClientRect() fuer die ausgewaehlten Selektoren
  styles   -- getComputedStyle() -> overflow, overflowY, height, display,
              gridTemplateRows, flex fuer die Uebersichts-Container
  clipped  -- scrollHeight > clientHeight && overflowY === "hidden"
              (kein Scroll-Container -- der eigentliche Vorwurf von Befund 9b)
  reachable -- document.elementFromPoint(cx, cy) auf jeden button:
              true genau dann, wenn der Treffer der Knopf selbst oder ein
              Nachfahre ist. Beweist "nicht mehr klickbar", statt es zu behaupten.
  offscreen -- rect.bottom > innerHeight || rect.top < 0
              (unterscheidet "verdeckt" von "außerhalb")

Ausgabe: JSON auf stdout (Hard Rule 7 -- Logging nach stderr), plus ein
Screenshot pro Breite nach docs/screenshots/p86_probe_<label>_<width>.png.

Zwei Aufrufe (Plan §2.3):
  E2a: gegen die Wegwerf-Instanz auf Port 18773 (voller Zugriff)
  E2b: lesend gegen die Produktion <SPACE_PUBLIC_BASE_URL> (kein POST,
        kein Schreiben, kein systemctl; CSRF-Login-Scheitern wird gemeldet,
        nicht erzwungen)

Dieser Block aendert keine einzige Zeile Produktcode. Sein Ergebnis ist
ein Messprotokoll im Phase-Head plus dieses Skript.
"""
from __future__ import annotations

import argparse
import base64
import datetime
import hashlib
import hmac
import json
import os
import struct
import sys
import time
import urllib.parse
from datetime import timezone
from pathlib import Path

from playwright.sync_api import Page, sync_playwright

# --- Pfade / Defaults ---------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = REPO_ROOT / "docs" / "screenshots"
OUT_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_CREDS = Path("/tmp/opencode/sharefyx-wegwerf-v3ritt/credentials.json")
DEFAULT_BASE_URL = "http://127.0.0.1:18773"
DEFAULT_WIDTHS = (1024, 1200, 1440)
DEFAULT_HEIGHT = 900
DEFAULT_LABEL = "main"

# Selektoren, die Plan §2.2 vorschreibt. Reihenfolge ist auch die
# Reihenfolge der `rects`/`styles`-Schluessel im JSON.
SELECTORS_RECT = (
    "#shell",
    "#list",
    "#detail",
    "#detail-overview",
    ".overview__col-left",
    ".overview__col-right",
    "#overview-graph",
    "#overview-refresh",
    ".rail__account",
)

# Diese Container interessieren fuer `clipped` und `styles`.
STYLE_CONTAINERS = (
    "#detail",
    "#detail-overview",
    ".overview__col-left",
    ".overview__col-right",
)

STYLE_PROPS = (
    "overflow",
    "overflowY",
    "height",
    "display",
    "gridTemplateRows",
    "flex",
)


# --- Login (TOTP, entliehen aus p86_block_c_self_check.py) -------------------


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


def _dismiss_update_banner(page: Page) -> None:
    """Wenn das Update-Banner sichtbar ist, einmal 'Verstanden' anklicken.

    Das Update-Banner ist ein transientes UI-Element am oberen Bildschirmrand;
    es blockiert darunter liegende Rail-Knoepfe. Wer misst, was das **Layout**
    blockiert, schickt das Banner vorher weg. Der Befund 'vom dismissable
    Banner blockiert' steht ohnehin im ersten Lauf (siehe `unreachable_details`).
    """
    # Selektor-Versuche in Reihenfolge der Wahrscheinlichkeit. Wir
    # versuchen nicht zu erraten, sondern lassen die Seite sprechen.
    selectors = (
        "#update-banner-dismiss",
        "[data-dismiss='update-banner']",
        "button.update-banner__dismiss",
        "button:has-text('Verstanden')",
    )
    for sel in selectors:
        try:
            loc = page.locator(sel)
            if loc.count() > 0 and loc.first.is_visible():
                loc.first.click()
                page.wait_for_load_state("networkidle", timeout=3000)
                print(f"Update-Banner weggeklickt ({sel}).", file=sys.stderr)
                return
        except Exception as exc:  # noqa: BLE001 -- best-effort
            print(f"  Banner-Dismiss {sel}: {exc}", file=sys.stderr)
    print("Update-Banner nicht gefunden oder schon weg.", file=sys.stderr)


def login(page: Page, base_url: str, password: str, otpauth_uri: str) -> tuple[int, str]:
    """Login mit TOTP.

    Strategie: vor dem ersten Versuch warten, bis ein frisches 30-Sek-Fenster
    beginnt (max 35s), dann EIN Login-Versuch. Bei 401 (TOTP verbraucht) oder
    429 (Rate-Limit) ein Retry nach 35s bzw. 65s im naechsten Fenster.

    Returns (status, note): status ist HTTP-Status; note beschreibt, was die
    Funktion erreicht hat ("ok", "csrf_origin_rejected", "rate_limit", ...).
    """
    secs_into = datetime.datetime.now().second
    wait = 35 - (secs_into % 30)
    print(
        f"Login: warte {wait}s auf frisches TOTP-Fenster (base={base_url})...",
        file=sys.stderr,
    )
    time.sleep(wait)

    for window in range(2):
        page.goto(f"{base_url}/ui/login", wait_until="domcontentloaded")
        page.locator('input[name="space"]').fill("alpha")
        page.locator('input[name="password"]').fill(password)
        totp_code = _generate_totp(otpauth_uri)
        counter = int(time.time() // 30)
        print(
            f"  Fenster {window + 1}: TOTP {totp_code} (counter {counter})",
            file=sys.stderr,
        )
        page.locator('input[name="totp"]').fill(totp_code)
        with page.expect_response("**/ui/login**") as resp_info:
            page.locator('button[type="submit"]').click()
        resp = resp_info.value
        print(f"  Fenster {window + 1}: HTTP {resp.status}", file=sys.stderr)
        if resp.status in (200, 303):
            # JS-Redirect ueber bootstrapCsrf-IIFE, nicht HTTP-Redirect.
            time.sleep(3.0)
            if not page.url.startswith(f"{base_url}/ui/"):
                page.goto(f"{base_url}/ui/", wait_until="domcontentloaded")
                page.wait_for_load_state("domcontentloaded", timeout=5000)
            return resp.status, "ok"
        if resp.status == 401:
            print("  TOTP verbraucht, warte 35s auf naechstes Fenster...", file=sys.stderr)
            time.sleep(35)
            continue
        if resp.status == 429:
            print("  Rate-Limit aktiv, warte 65s...", file=sys.stderr)
            time.sleep(65)
            continue
        # Alles andere (403 CSRF, 5xx, ...) ist ein Befund, kein Retry.
        return resp.status, f"http_{resp.status}"
    return 0, "tries_exhausted"


# --- Probe-Kern --------------------------------------------------------------


def _eval_rects(page: Page) -> dict[str, dict[str, float] | None]:
    """getBoundingClientRect pro Selektor. None, wenn der Selektor fehlt."""
    out: dict[str, dict[str, float] | None] = {}
    for sel in SELECTORS_RECT:
        loc = page.locator(sel)
        if loc.count() == 0:
            out[sel] = None
            continue
        rect = loc.first.evaluate(
            """el => {
                const r = el.getBoundingClientRect();
                return {
                    x: r.x, y: r.y, width: r.width, height: r.height,
                    bottom: r.bottom, top: r.top, right: r.right, left: r.left
                };
            }"""
        )
        out[sel] = rect
    return out


def _eval_styles(page: Page) -> dict[str, dict[str, str] | None]:
    """getComputedStyle pro Container. None, wenn der Selektor fehlt."""
    out: dict[str, dict[str, str] | None] = {}
    for sel in STYLE_CONTAINERS:
        loc = page.locator(sel)
        if loc.count() == 0:
            out[sel] = None
            continue
        style = loc.first.evaluate(
            """(el, props) => {
                const cs = getComputedStyle(el);
                const out = {};
                for (const p of props) out[p] = cs[p];
                return out;
            }""",
            list(STYLE_PROPS),
        )
        out[sel] = style
    return out


def _eval_clipped(page: Page) -> dict[str, bool | None]:
    """scrollHeight > clientHeight && overflowY === 'hidden' pro Container."""
    out: dict[str, bool | None] = {}
    for sel in STYLE_CONTAINERS:
        loc = page.locator(sel)
        if loc.count() == 0:
            out[sel] = None
            continue
        clipped = loc.first.evaluate(
            """el => {
                const cs = getComputedStyle(el);
                return el.scrollHeight > el.clientHeight && cs.overflowY === 'hidden';
            }"""
        )
        out[sel] = bool(clipped)
    return out


def _eval_buttons(page: Page) -> list[dict[str, object]]:
    """Pro <button>: rect, reachable (elementFromPoint), offscreen."""
    return page.evaluate(
        """() => {
            const btns = Array.from(document.querySelectorAll('button'));
            return btns.map(b => {
                const r = b.getBoundingClientRect();
                const cx = r.left + r.width / 2;
                const cy = r.top + r.height / 2;
                let hit = null;
                try {
                    const el = document.elementFromPoint(cx, cy);
                    hit = el ? (el === b || b.contains(el) ? 'self' : (el.id || el.tagName + (el.className ? '.' + el.className : ''))) : null;
                } catch (e) {
                    hit = 'error:' + e.message;
                }
                const offscreen = (r.bottom > window.innerHeight || r.top < 0);
                return {
                    id: b.id || null,
                    classes: b.className || null,
                    text: (b.textContent || '').trim().slice(0, 80) || null,
                    rect: { x: r.x, y: r.y, width: r.width, height: r.height,
                            bottom: r.bottom, top: r.top },
                    cx, cy,
                    reachable: hit === 'self',
                    hit_at_center: hit,
                    offscreen,
                };
            });
        }"""
    )


def probe(page: Page, width: int, height: int = DEFAULT_HEIGHT, *, dismiss_banner: bool = False) -> dict:
    """Eine Breite, ein Dictsatz."""
    page.set_viewport_size({"width": width, "height": height})
    # /ui/ ist die Uebersichtsseite (Home-Button -> navigateAll()).
    page.goto(f"{page.url.split('/ui/')[0]}/ui/", wait_until="domcontentloaded")
    page.wait_for_load_state("networkidle")
    if dismiss_banner:
        _dismiss_update_banner(page)
    time.sleep(0.6)

    rects = _eval_rects(page)
    styles = _eval_styles(page)
    clipped = _eval_clipped(page)
    buttons = _eval_buttons(page)

    inner_height = page.evaluate("window.innerHeight")
    unreachable = [
        b for b in buttons
        if not b["reachable"] and not b["offscreen"]
    ]
    return {
        "width": width,
        "height": height,
        "innerHeight": inner_height,
        "url": page.url,
        "rects": rects,
        "styles": styles,
        "clipped": clipped,
        "buttons_total": len(buttons),
        "buttons_unreachable": len(unreachable),
        "buttons_offscreen": sum(1 for b in buttons if b["offscreen"]),
        "unreachable_details": unreachable,
    }


# --- Main --------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Phase 8.6 Block E -- Viewport-Probe (messen, nicht bauen)"
    )
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL,
                        help=f"Sharefyx-Basis-URL (default: {DEFAULT_BASE_URL})")
    parser.add_argument("--widths", default=",".join(str(w) for w in DEFAULT_WIDTHS),
                        help="Komma-getrennte Breiten (default: 1024,1200,1440)")
    parser.add_argument("--label", default=DEFAULT_LABEL,
                        help="Label fuer Screenshots + JSON-Top-Key (z.B. 'main' / 'production')")
    parser.add_argument("--out", default="-",
                        help="JSON-Ausgabe: '-' = stdout, sonst Pfad zur Datei")
    parser.add_argument("--creds", default=str(DEFAULT_CREDS),
                        help=f"Pfad zu credentials.json (default: {DEFAULT_CREDS})")
    parser.add_argument("--no-login", action="store_true",
                        help="Login ueberspringen (fuer manuelle Cookie-Sessions)")
    parser.add_argument("--dismiss-banner", action="store_true",
                        help="Update-Banner wegklicken, falls sichtbar (default: aus). "
                             "Trennt 'vom dismissable Banner blockiert' von "
                             "'vom Layout ueberdeckt'.")
    args = parser.parse_args(argv)

    creds_path = Path(args.creds)
    if not creds_path.exists():
        print(f"ABBRUCH: credentials nicht gefunden: {creds_path}", file=sys.stderr)
        return 2

    creds = _read_creds(creds_path)
    widths = [int(w) for w in args.widths.split(",") if w.strip()]
    print(
        f"Probe: base={args.base_url}, label={args.label}, "
        f"widths={widths}, height={DEFAULT_HEIGHT}",
        file=sys.stderr,
    )

    results: dict[str, object] = {
        "label": args.label,
        "base_url": args.base_url,
        "timestamp": datetime.datetime.now(timezone.utc).isoformat(),
        "widths": widths,
        "results": [],
        "login": {"attempted": True, "status": None, "note": None},
    }

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": widths[0], "height": DEFAULT_HEIGHT})
        page = context.new_page()

        if not args.no_login:
            status, note = login(page, args.base_url, creds["password"], creds["otpauth_uri"])
            results["login"] = {"attempted": True, "status": status, "note": note}
            if status not in (200, 303):
                # CSRF oder sonstiges Scheitern -- sauber abbrechen, nicht erzwungen.
                print(
                    f"ABBRUCH: login fehlgeschlagen (status={status}, note={note}). "
                    f"Probe wird nicht ausgefuehrt -- das ist ein Befund, kein Fehler.",
                    file=sys.stderr,
                )
                results["aborted_reason"] = f"login_failed:{note}"
                browser.close()
                _write_json(results, args.out)
                return 3
        else:
            results["login"]["attempted"] = False

        if args.dismiss_banner:
            _dismiss_update_banner(page)

        for width in widths:
            print(f"-- Breite {width} px --", file=sys.stderr)
            r = probe(page, width, dismiss_banner=args.dismiss_banner)
            results["results"].append(r)
            shot = OUT_DIR / f"p86_probe_{args.label}_{width}.png"
            page.screenshot(path=str(shot))
            print(f"   Screenshot: {shot.name}", file=sys.stderr)

        browser.close()

    _write_json(results, args.out)
    return 0


def _write_json(results: dict, out: str) -> None:
    if out == "-":
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        Path(out).write_text(json.dumps(results, indent=2, ensure_ascii=False))
        print(f"JSON geschrieben: {out}", file=sys.stderr)


if __name__ == "__main__":
    sys.exit(main())
