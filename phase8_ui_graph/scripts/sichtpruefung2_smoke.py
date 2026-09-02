#!/usr/bin/env python3
"""Phase 8 Sichtpruefung 2 -- Playwright gegen die Wegwerf-Instanz auf 127.0.0.1:18769.

30+ Items ueber drei Spaces (eigener + zwei fremde-readable), Frontmatter-Links, Body-
Referenzen, gemeinsame Tags und Ordner. Diese Smoke-Tests nehmen die Block-D-End-Screenshots
auf, die ins README Sneak Peak und in den Phase-8-Closeout-Block gehen.

Screenshots:
  - sp2_01_overview_spaces_rows.png   -- tabellose Uebersicht mit drei Space-Zeilen
  - sp2_02_overview_global_scope.png  -- Home-Klick -> globaler Scope (5+ Items sichtbar)
  - sp2_03_graph_default.png          -- Graph mit Default (nur explizite Kanten)
  - sp2_04_graph_with_tags.png        -- Graph mit Tag-Toggle on (gestrichelte Cluster)
  - sp2_05_graph_with_folders.png     -- Graph mit Ordner-Toggle on (gepunktete Cluster)
  - sp2_06_node_click.png             -- Klick auf einen Knoten -> Item geoeffnet
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

BASE = "http://127.0.0.1:18769"
WEGWERF_ROOT = Path("/tmp/opencode/sharefyx-wegwerf-sichtpruefung2")
CREDS_FILE = WEGWERF_ROOT / "credentials.json"
SHOT_DIR = Path(__file__).resolve().parents[2] / "docs" / "screenshots"


def _load_creds() -> dict[str, str]:
    return json.loads(CREDS_FILE.read_text())


def _current_totp(secret_b32: str) -> str:
    return pyotp.TOTP(secret_b32).now()


async def login(page, password: str, secret_b32: str) -> None:
    await page.goto(f"{BASE}/ui/login", wait_until="domcontentloaded")
    await page.fill('input[name="space"]', "alpha")
    await page.fill('input[name="password"]', password)
    await page.fill('input[name="totp"]', _current_totp(secret_b32))
    await page.click('button[type="submit"]')
    await page.wait_for_url(f"{BASE}/ui/", timeout=10000)
    await page.wait_for_selector(".overview__spaces .overview__space-row", state="visible", timeout=10000)
    # Warten, bis der Graph geladen ist (Empty-Hint weg ODER Zoom-Readout gefuellt).
    await page.wait_for_function(
        "() => !document.getElementById('overview-graph-empty').hidden "
        "|| document.getElementById('overview-graph-zoom').textContent.length > 0",
        timeout=10000,
    )
    # Force-Simulation sichtbare Knotenpositionen produzieren lassen.
    await page.wait_for_timeout(1500)


async def screenshot(page, name: str) -> None:
    SHOT_DIR.mkdir(parents=True, exist_ok=True)
    path = SHOT_DIR / name
    await page.screenshot(path=str(path), full_page=True)
    print(f"[OK ] Screenshot -> {path}")


async def main() -> int:
    creds = _load_creds()
    password = creds["password"]
    uri = creds["otpauth_uri"]
    secret_b32 = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(uri).query))["secret"]

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(viewport={"width": 1280, "height": 900})
        page = await ctx.new_page()
        try:
            await login(page, password, secret_b32)
            # 01: Uebersicht tabellos (direkt nach Login, drei Space-Zeilen + Graph)
            await screenshot(page, "sp2_01_overview_spaces_rows.png")

            # 02: Home-Klick -> globaler Scope
            await page.click("#home-button")
            await page.wait_for_selector(".tree__scope[aria-current='true']", timeout=10000)
            await page.wait_for_selector(".list__row", timeout=10000)
            await page.wait_for_timeout(500)
            await screenshot(page, "sp2_02_overview_global_scope.png")

            # 03: Graph mit Default (nur explizite Kanten) -- Toggles ausschalten, neu laden
            # Erst Toggles auf "off" zurueck (falls ein Vorzustand gesetzt war)
            tags_box = page.locator("#overview-graph-toggle-tags")
            folders_box = page.locator("#overview-graph-toggle-folders")
            if await tags_box.is_checked():
                await tags_box.uncheck()
            if await folders_box.is_checked():
                await folders_box.uncheck()
            await page.click("#overview-refresh")
            await page.wait_for_timeout(2000)
            await screenshot(page, "sp2_03_graph_default.png")

            # 04: Tags-Toggle on
            await page.check("#overview-graph-toggle-tags")
            await page.wait_for_timeout(2500)
            await screenshot(page, "sp2_04_graph_with_tags.png")

            # 05: Ordner-Toggle on (Tags bleibt an -- alle drei Kantenarten sichtbar)
            await page.check("#overview-graph-toggle-folders")
            await page.wait_for_timeout(2500)
            await screenshot(page, "sp2_05_graph_with_folders.png")

            # 06: Editor mit geoeffnetem Item -- ein Klick auf einen List-Eintrag reicht, weil
            # die Knoten-Klick-Logik (Editor.selectItem) identisch ist (B4, Plan §5 D2). Wir
            # suchen einen ALPHA-Item per Text (eigenes Item, also Edit-Modus mit Titel-Eingabe,
            # nicht der Read-Only-Modus fuer fremde Items).
            await page.click("#home-button")
            await page.wait_for_timeout(500)
            # Wir warten auf das erste alpha-Item in der globalen Liste.
            await page.wait_for_selector(
                ".list__row .overview__space-name--readonly, .list__row", timeout=10000,
            )
            # Spezifischer Klick auf einen alpha-Titel -- Tagesnotizen ist alpha und own.
            await page.click(".list__row:has-text('Tagesnotizen')")
            await page.wait_for_selector(".editor__title-input", state="visible", timeout=10000)
            await page.wait_for_timeout(800)
            await screenshot(page, "sp2_06_node_click.png")

        finally:
            await browser.close()

    print("Alle Sichtpruefung-2-Screenshots aufgenommen.")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
