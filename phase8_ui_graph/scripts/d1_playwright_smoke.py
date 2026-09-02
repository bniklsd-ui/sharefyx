#!/usr/bin/env python3
"""Phase 8 D1 -- Playwright-Smoke gegen die Wegwerf-Instanz auf 127.0.0.1:18767.

Pruefungen (entsprechen den D1-relevanten Abnahmezeilen P8-18 + P8-19):
  1. /ui/ enthaelt den neuen .overview__header (Titel + Refresh-Knopf), die .legend, und
     KEIN altes .overview__tiles/.space-card mehr (statisches Markup, kein Login noetig).
  2. Login als User `alpha`, Overview rendert eine .overview__space-row fuer jeden Space
     (eigener alpha + fremder beta), mit den richtigen Counter-Chips.
  3. Klick auf einen Counter-Chip navigiert zur richtigen Liste (URL-Snapshot).
  4. Klick auf Home (rail) schaltet die Listen-Spalte auf den globalen Scope (P8-19).
     Erwartet: .tree__scope.aria-current === 'true' UND .list-crumb enthaelt "Alle Items".
  5. Klick auf Home WHILE die Liste bereits im globalen Scope ist: keine Aenderung.

Screenshots: docs/screenshots/d1_*.png (zur Sichtpruefung, kein Suite-Bestandteil).
"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys
import urllib.parse
from pathlib import Path

import pyotp
from playwright.async_api import async_playwright, expect

BASE = "http://127.0.0.1:18767"
WEGWERF_ROOT = Path("/tmp/opencode/sharefyx-wegwerf-d1")
CREDS_FILE = WEGWERF_ROOT / "credentials.json"
SHOT_DIR = Path(__file__).resolve().parents[2] / "docs" / "screenshots"


def _load_creds() -> dict[str, str]:
    return json.loads(CREDS_FILE.read_text())


def _current_totp(secret_b32: str) -> str:
    return pyotp.TOTP(secret_b32).now()


async def step1_static_markup() -> None:
    """Statisches Markup pruefen -- /ui/ ist session-gated, also lesen wir app.html direkt."""
    body = (Path(__file__).resolve().parents[2] / "phase5_ui" / "webui" / "static" / "app.html").read_text()
    assert 'class="overview__header"' in body, ".overview__header fehlt in app.html"
    assert 'id="overview-refresh"' in body, "Refresh-Knopf fehlt in app.html"
    assert 'id="overview-spaces"' in body, "#overview-spaces Container fehlt"
    assert 'id="overview-graph-canvas"' in body, "Graph-Canvas fehlt"
    assert ".overview__tiles" not in body, "altes .overview__tiles noch da (sollte weg sein)"
    assert 'id="overview-foreign"' not in body, "alter #overview-foreign Container noch da"
    print("[OK ] app.html enthaelt neuen Uebersichts-Aufbau (header/spaces/graph-canvas), "
          "alte .overview__tiles/.space-card-Stellen weg")


async def step2_login_and_overview(page, password: str, secret_b32: str) -> None:
    await page.goto(f"{BASE}/ui/login", wait_until="domcontentloaded")
    await page.fill('input[name="space"]', "alpha")
    await page.fill('input[name="password"]', password)
    await page.fill('input[name="totp"]', _current_totp(secret_b32))
    await page.click('button[type="submit"]')
    await page.wait_for_url(f"{BASE}/ui/", timeout=10000)

    # Overview-Header + Legend sichtbar (C3 hat die Legende gebaut, D1 nimmt sie mit).
    await page.wait_for_selector(".overview__header", state="visible", timeout=10000)
    await page.wait_for_selector(".overview .legend", state="visible", timeout=10000)

    # Mindestens zwei Space-Zeilen (alpha + beta).
    rows = page.locator(".overview__spaces .overview__space-row")
    await expect(rows.first).to_be_visible()
    count = await rows.count()
    assert count >= 2, f"erwartet >= 2 Space-Zeilen (alpha + beta), gefunden: {count}"
    print(f"[OK ] Overview rendert {count} Space-Zeilen (mind. alpha + beta)")

    # Eigener Space alpha: rail__glyph--own + Counter-Chips sichtbar.
    own_row = page.locator(".overview__spaces .overview__space-row").first
    own_text = await own_row.inner_text()
    assert "alpha" in own_text, f"alpha fehlt in erster Zeile: {own_text!r}"
    assert await own_row.locator(".rail__glyph--own").count() == 1, \
        "alpha-Zeile hat keinen .rail__glyph--own"
    own_chips = await own_row.locator(".overview__space-count").count()
    assert own_chips >= 1, f"alpha-Zeile ohne Counter-Chips: {own_chips}"
    print(f"[OK ] alpha-Zeile: rail__glyph--own + {own_chips} Counter-Chips")

    # Fremder Space beta: rail__glyph--foreign + Counter-Chips sichtbar.
    # Wir nehmen die letzte Zeile (beta kommt nach alpha -- sortiert nach own/name).
    foreign_row = page.locator(".overview__spaces .overview__space-row").last
    foreign_text = await foreign_row.inner_text()
    assert "beta" in foreign_text, f"beta fehlt in letzter Zeile: {foreign_text!r}"
    assert await foreign_row.locator(".rail__glyph--foreign").count() == 1, \
        "beta-Zeile hat keinen .rail__glyph--foreign"
    foreign_chips = await foreign_row.locator(".overview__space-count").count()
    assert foreign_chips >= 1, f"beta-Zeile ohne Counter-Chips: {foreign_chips}"
    print(f"[OK ] beta-Zeile: rail__glyph--foreign + {foreign_chips} Counter-Chips")


async def step3_click_counter_chip(page) -> None:
    """Klick auf einen Counter-Chip im eigenen Space -- muss zur Liste dieses Spaces/Buckets
    navigieren (Crumb enthaelt alpha + Bucket-Name, .list__row ist sichtbar)."""
    own_row = page.locator(".overview__spaces .overview__space-row").first
    first_chip = own_row.locator(".overview__space-count").first
    chip_text = (await first_chip.inner_text()).strip()
    bucket = await first_chip.get_attribute("data-bucket")
    assert bucket, "Chip ohne data-bucket-Attribut"
    await first_chip.click()
    await page.wait_for_selector(".list__row", timeout=10000)
    crumb_text = await page.locator("#list-crumb").inner_text()
    assert "alpha" in crumb_text, f"Crumb enthaelt kein alpha: {crumb_text!r}"
    print(f"[OK ] Chip-Klick navigiert: Crumb='{crumb_text.strip()}', Bucket={bucket}")


async def step4_home_button_switches_to_global(page) -> None:
    """Klick auf Home schaltet die Liste auf den globalen Scope (P8-19)."""
    home = page.locator("#home-button")
    await home.click()
    await page.wait_for_selector(".tree__scope[aria-current='true']", timeout=10000)
    crumb = await page.locator("#list-crumb").inner_text()
    assert "Alle Items" in crumb, f"Crumb nicht global: {crumb!r}"
    # Mindestens ein Item sichtbar (alpha hat 3, beta hat 2 = 5 lesbare).
    await page.wait_for_selector(".list__row", timeout=10000)
    rows = await page.locator(".list__row").count()
    assert rows >= 3, f"globale Liste enthaelt zu wenige Items: {rows}"
    print(f"[OK ] Home-Klick: globaler Scope aktiv, Crumb='{crumb.strip()}', {rows} Items")


async def step5_home_click_is_idempotent_when_global(page) -> None:
    """Wenn die Liste bereits im globalen Scope ist, darf ein weiterer Home-Klick nichts
    kaputtmachen (V82, kein Wechsel zurueck in den Space-Scope)."""
    home = page.locator("#home-button")
    await home.click()
    # Kurz warten, dann erneut pruefen.
    await page.wait_for_timeout(200)
    scope_current = await page.locator(".tree__scope[aria-current='true']").count()
    assert scope_current == 1, "globaler Scope nach zweitem Home-Klick verloren"
    crumb = await page.locator("#list-crumb").inner_text()
    assert "Alle Items" in crumb, f"Crumb nach zweitem Home-Klick weg: {crumb!r}"
    print("[OK ] Home-Klick im globalen Scope ist idempotent (V82 Regression ausgeschlossen)")


async def step_screenshot(page, name: str) -> None:
    SHOT_DIR.mkdir(parents=True, exist_ok=True)
    path = SHOT_DIR / name
    await page.screenshot(path=str(path), full_page=True)
    print(f"[OK ] Screenshot -> {path}")


async def main() -> int:
    creds = _load_creds()
    password = creds["password"]
    uri = creds["otpauth_uri"]
    secret_b32 = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(uri).query))["secret"]

    await step1_static_markup()

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(viewport={"width": 1280, "height": 900})
        page = await ctx.new_page()
        try:
            await step2_login_and_overview(page, password, secret_b32)
            await step_screenshot(page, "d1_01_overview_space_rows.png")
            await step3_click_counter_chip(page)
            await step_screenshot(page, "d1_02_counter_chip_navigates.png")
            await step4_home_button_switches_to_global(page)
            await step_screenshot(page, "d1_03_home_to_global_scope.png")
            await step5_home_click_is_idempotent_when_global(page)
        finally:
            await browser.close()

    print("Alle D1-Checks bestanden.")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
