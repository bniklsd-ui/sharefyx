#!/usr/bin/env python3
"""Phase 8 C3 -- Playwright-Smoke gegen die Wegwerf-Instanz auf 127.0.0.1:18766.

Pruefungen:
  1. /ui/ enthaelt das statische .legend-Element mit drei .legend__dot-Varianten
     (HTML-Snapshot, KEIN Login noetig -- das ist app.html direkt).
  2. Login als User `alpha`, Overview zeigt das .legend + das .rail__glyph--own im Baum.
  3. Klick auf "Alle Items", Item-Liste rendert .space-dot--own in der Metazeile.

Screenshots: docs/screenshots/c3_*.png (zur Sichtpruefung, kein Bestandteil der Suite).
"""
from __future__ import annotations

import argparse
import asyncio
import base64
import json
import sys
import urllib.parse
from pathlib import Path

import pyotp
from playwright.async_api import async_playwright, expect

BASE = "http://127.0.0.1:18766"
WEGWERF_ROOT = Path("/tmp/opencode/sharefyx-wegwerf-c3")
CREDS_FILE = WEGWERF_ROOT / "credentials.json"
SHOT_DIR = Path(__file__).resolve().parents[2] / "docs" / "screenshots"


def _load_creds() -> dict[str, str]:
    return json.loads(CREDS_FILE.read_text())


def _current_totp(secret_b32: str) -> str:
    return pyotp.TOTP(secret_b32).now()


async def step1_legend_in_app_html() -> None:
    """Statische .legend in app.html -- das Markup liegt als Datei vor, ohne Server-Round-Trip.
    /ui/ ist session-gated (303 -> /ui/login), also testen wir die Quelle direkt, das Markup
    kommt nach dem Login unverändert aus der Datei."""
    body = (Path(__file__).resolve().parents[2] / "phase5_ui" / "webui" / "static" / "app.html").read_text()
    assert "legend__dot legend__dot--own" in body, ".legend__dot--own nicht in app.html"
    assert "legend__dot legend__dot--shared" in body, ".legend__dot--shared nicht in app.html"
    assert "legend__dot legend__dot--foreign" in body, ".legend__dot--foreign nicht in app.html"
    assert "Eigener Space" in body and "Geteilter Space" in body and "Fremder Space" in body, \
        "Legend-Labels unvollstaendig"
    print("[OK ] app.html enthaelt .legend mit drei .legend__dot-{own,shared,foreign} + Labels")


async def step2_login_and_overview(page, password: str, secret_b32: str) -> None:
    await page.goto(f"{BASE}/ui/login", wait_until="domcontentloaded")
    # Login ist ein-Schrittig: Space + Passwort + TOTP in einem Form-POST.
    await page.fill('input[name="space"]', "alpha")
    await page.fill('input[name="password"]', password)
    await page.fill('input[name="totp"]', _current_totp(secret_b32))
    await page.click('button[type="submit"]')
    await page.wait_for_url(f"{BASE}/ui/", timeout=10000)
    # Nach Login: Overview ist sichtbar, .legend darin
    await page.wait_for_selector(".overview .legend", state="visible", timeout=10000)
    # Rail enthaelt .rail__glyph--own fuer den eigenen Space
    await expect(page.locator(".tree__space .rail__glyph--own").first).to_be_visible()
    # Auch die zwei weiteren Klassen muessen als CSS-Regeln existieren (sonst waere
    # spaeteres Rendering fuer shared/foreign ohne Style). Wir laden das CSS und suchen.
    css_body = await page.evaluate(
        "async () => (await fetch('/ui/static/app.css')).text()"
    )
    for cls in ("rail__glyph--own", "rail__glyph--shared", "rail__glyph--foreign",
                "space-dot--own", "space-dot--shared", "space-dot--foreign",
                "legend__dot--own", "legend__dot--shared", "legend__dot--foreign"):
        assert cls in css_body, f"CSS-Regel .{cls} fehlt"
    # Tokens vorhanden
    for tok in ("--space-own", "--space-shared", "--space-foreign"):
        assert tok in css_body, f"Token {tok} fehlt in app.css"
    print("[OK ] Login + Overview: .legend + .rail__glyph--own sichtbar, alle CSS-Regeln + Tokens")


async def step3_global_scope_dot(page, secret_b32: str) -> None:
    """Klick auf 'Alle Items' -- das Item soll .space-dot--own in der Metazeile haben."""
    # Wir muessen nach dem Login moeglicherweise neu TOTP eingeben -- die UI-Session hat
    # eine eigene Lifetime, sollte aber hier noch offen sein.
    await page.click(".tree__scope")
    await page.wait_for_selector(".list__rows li", timeout=10000)
    # Mindestens ein Item mit .space-dot--own in der Metazeile
    await expect(page.locator(".list__row .space-dot--own").first).to_be_visible()
    print("[OK ] Global-Scope: .space-dot--own in der Item-Metazeile sichtbar")


async def step4_screenshot(page, name: str) -> None:
    SHOT_DIR.mkdir(parents=True, exist_ok=True)
    path = SHOT_DIR / name
    await page.screenshot(path=str(path), full_page=True)
    print(f"[OK ] Screenshot -> {path}")


async def main() -> int:
    creds = _load_creds()
    password = creds["password"]
    uri = creds["otpauth_uri"]
    secret_b32 = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(uri).query))["secret"]

    # Step 1 ist eine reine HTTP-Pruefung -- kein Browser noetig.
    await step1_legend_in_app_html()

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(viewport={"width": 1280, "height": 900})
        page = await ctx.new_page()

        try:
            await step2_login_and_overview(page, password, secret_b32)
            await step4_screenshot(page, "c3_01_overview_with_legend.png")
            await step3_global_scope_dot(page, secret_b32)
            await step4_screenshot(page, "c3_02_global_scope_dot.png")
        finally:
            await browser.close()

    print("Alle C3-Checks bestanden.")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
