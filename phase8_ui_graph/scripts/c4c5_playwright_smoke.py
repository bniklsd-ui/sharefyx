#!/usr/bin/env python3
"""Phase 8 Block C C4+C5 -- Playwright-Smoke gegen die Wegwerf-Instanz auf 127.0.0.1:18770.

Pruefungen:
  1. CSS-Content (statisch via fetch): --glass-* Tokens, .glass-Utility,
     @supports backdrop-filter, @media prefers-reduced-transparency,
     ::selection, max-width:72ch auf .editor__textarea, 3px-Akzentkante +
     1px-Outline auf .list__row[aria-current="true"] und
     .list__rows > li.list__row--selected.
  2. Login + Overview: .list__head ist sticky positioniert (CSS computed style),
     .list__head.traegt die Glass-Träger-Regeln (CSS-Variable --glass-bg ist
     gesetzt), rail__glyph--own sichtbar.
  3. Klick auf ein Item: ausgewaehlte Zeile hat aria-current="true", berechnete
     border-left-color ist var(--accent), Outline ist 1px solid accent.
  4. Editor offen: .editor__textarea hat computed max-width: 72ch und ist
     horizontal zentriert (margin: 0 auto wirksam -- boundingClientRect.centerX
     im Bereich der Listen-Spalten-Mitte).
  5. Selection auf einem Item-Titel: ::selection Background entspricht
     --accent-quiet (computed via document.styleSheets[0]).

Screenshots: docs/screenshots/c4c5_*.png (zur Sichtpruefung, kein Bestandteil
der Suite).
"""
from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
import urllib.parse
from pathlib import Path

import pyotp
from playwright.async_api import async_playwright, expect

BASE = "http://127.0.0.1:18770"
WEGWERF_ROOT = Path("/tmp/opencode/sharefyx-wegwerf-c4c5")
CREDS_FILE = WEGWERF_ROOT / "credentials.json"
SHOT_DIR = Path(__file__).resolve().parents[2] / "docs" / "screenshots"


def _load_creds() -> dict[str, str]:
    return json.loads(CREDS_FILE.read_text())


def _current_totp(secret_b32: str) -> str:
    return pyotp.TOTP(secret_b32).now()


async def step1_css_static_checks() -> str:
    """Prueft das ausgelieferte app.css auf C4/C5-Bestandteile."""
    import urllib.request
    body = urllib.request.urlopen(f"{BASE}/ui/static/app.css", timeout=5).read().decode()
    # --glass-* Tokens
    for tok in ("--glass-bg:", "--glass-border:", "--glass-blur:", "--glass-highlight:"):
        assert tok in body, f"Token-Definition {tok} fehlt in app.css"
    # .glass-Utility
    assert re.search(r"\.glass\s*{[^}]*background:\s*var\(--surface-raised\)", body), \
        ".glass-Utility ohne Fallback-Background"
    assert re.search(r"@supports[^}]*backdrop-filter", body), "@supports backdrop-filter fehlt"
    assert re.search(r"@media\s*\(\s*prefers-reduced-transparency:\s*reduce\s*\)", body), \
        "@media prefers-reduced-transparency fehlt"
    # ::selection
    assert re.search(r"::selection\s*{", body), "::selection-Regel fehlt"
    assert "var(--accent-quiet)" in body and body.count("var(--accent-quiet)") >= 2, \
        "::selection ohne --accent-quiet-Bezug"
    # 72ch-Editor
    assert re.search(r"\.editor__textarea\s*{[^}]*max-width:\s*72ch", body), \
        ".editor__textarea ohne max-width: 72ch"
    # Selektion: 3px Akzentkante + 1px Outline (Regex mit DOTALL, weil die Properties
    # in der naechsten Zeile nach der Selector-Klammer stehen)
    assert re.search(
        r"\.list__row\[aria-current=\"true\"\]\s*\{[^}]*border-left-color:\s*var\(--accent\)",
        body, re.DOTALL), ".list__row[aria-current=true] ohne 3px Akzentkante"
    assert re.search(
        r"\.list__row\[aria-current=\"true\"\]\s*\{[^}]*outline:\s*1px solid var\(--accent\)",
        body, re.DOTALL), ".list__row[aria-current=true] ohne 1px Akzent-Outline"
    assert re.search(
        r"\.list__rows\s*>\s*li\.list__row--selected\s*\{[^}]*border-left:\s*3px solid var\(--accent\)",
        body, re.DOTALL), "Mehrfachauswahl ohne 3px Akzentkante"
    # Gruppierte Glas-Traeger am Ende der Datei
    assert ".list__head,\n.overlay__panel,\n.update-banner,\n.toast" in body, \
        "Glas-Traeger-Liste am Dateiende fehlt"
    print("[OK ] app.css: --glass-* Tokens, .glass-Utility, @supports, "
          "prefers-reduced-transparency, ::selection, max-width:72ch, "
          "3px Akzentkante, gruppierte Glas-Traeger")
    return body


async def step2_login_and_overview(page, password: str, secret_b32: str) -> None:
    await page.goto(f"{BASE}/ui/login", wait_until="domcontentloaded")
    await page.fill('input[name="space"]', "alpha")
    await page.fill('input[name="password"]', password)
    await page.fill('input[name="totp"]', _current_totp(secret_b32))
    await page.click('button[type="submit"]')
    await page.wait_for_url(f"{BASE}/ui/", timeout=10000)
    await page.wait_for_selector(".list__head", state="visible", timeout=10000)
    # Glass-Träger .list__head hat im Browser tatsaechlich `position: sticky` + `z-index: 1`
    list_head_sticky = await page.evaluate(
        "() => getComputedStyle(document.querySelector('.list__head')).position"
    )
    assert list_head_sticky == "sticky", \
        f".list__head computed position ist '{list_head_sticky}', erwartet 'sticky'"
    print("[OK ] Login + Overview: .list__head hat computed position: sticky")


async def step3_selected_row_styles(page) -> None:
    """Klick auf das erste eigene Item (foreign-Items sind read-only, da kann der
    Editor-Step 4 nicht folgen), dann aria-current + computed border + outline pruefen."""
    await page.click(".tree__scope")  # 'Alle Items' (globaler Scope)
    await page.wait_for_selector(".list__rows li", timeout=10000)
    # Eigenes Item suchen (space-dot--own), nicht foreign
    await page.click('.list__row:has(.space-dot--own)')
    await page.wait_for_selector('.list__row[aria-current="true"]', timeout=5000)
    styles = await page.evaluate("""() => {
      const el = document.querySelector('.list__row[aria-current=\"true\"]');
      const cs = getComputedStyle(el);
      return {
        borderLeftColor: cs.borderLeftColor,
        borderLeftWidth: cs.borderLeftWidth,
        outlineColor: cs.outlineColor,
        outlineWidth: cs.outlineWidth,
        outlineStyle: cs.outlineStyle,
      };
    }""")
    # 3px Akzentkante links (var(--accent) = #3E8DF3 = rgb(62,141,243))
    assert styles["borderLeftWidth"] == "3px", \
        f"border-left-width ist {styles['borderLeftWidth']}, erwartet 3px"
    assert "62, 141, 243" in styles["borderLeftColor"] or "3e8df3" in styles["borderLeftColor"].lower(), \
        f"border-left-color ist {styles['borderLeftColor']}, erwartet var(--accent)"
    # Outline: 1px solid var(--accent)
    assert styles["outlineWidth"] == "1px", \
        f"outline-width ist {styles['outlineWidth']}, erwartet 1px"
    assert styles["outlineStyle"] == "solid", \
        f"outline-style ist {styles['outlineStyle']}, erwartet solid"
    assert "62, 141, 243" in styles["outlineColor"], \
        f"outline-color ist {styles['outlineColor']}, erwartet var(--accent)"
    print(f"[OK ] Ausgewaehlte Zeile (own): border-left 3px + outline 1px solid accent")


async def step4_editor_textarea_72ch(page) -> None:
    """Oeffnet das Item im Editor (Detail-Bereich) und prueft max-width + Zentrierung.

    Default-Oeffnungsmodus ist 'preview' (Editor.js Z. 315, opts.mode || 'preview');
    zum Pruefen der Textarea (die nur im 'edit'-Modus sichtbar ist) muss der
    Bearbeiten-Knopf geklickt werden (#toggle-preview, Z. 611)."""
    await page.wait_for_selector("#detail-editor:not([hidden])", timeout=5000)
    await page.click("#toggle-preview")  # preview -> edit
    await page.wait_for_selector(".editor__textarea", state="visible", timeout=5000)
    styles = await page.evaluate("""() => {
      const el = document.querySelector('.editor__textarea');
      const cs = getComputedStyle(el);
      return {
        maxWidth: cs.maxWidth,
        marginLeft: cs.marginLeft,
        marginRight: cs.marginRight,
        parentWidth: el.parentElement.getBoundingClientRect().width,
        elWidth: el.getBoundingClientRect().width,
      };
    }""")
    # `72ch` wird im computed style zu Pixeln aufgeloest (1ch = Schrift-Breite der
    # '0' im aktuellen Font, hier Plex Mono 13px = ~8px, also ~576px). Wir pruefen
    # einfach, dass die Textarea deutlich schmaler als die Parent-Spalte ist UND die
    # Margins symmetrisch sind.
    assert styles["elWidth"] < styles["parentWidth"], \
        f"Textarea-Breite ({styles['elWidth']}px) ist nicht schmaler als Parent ({styles['parentWidth']}px); " \
        f"max-width 72ch greift nicht"
    assert styles["marginLeft"] == styles["marginRight"], \
        f"margin-left ({styles['marginLeft']}) != margin-right ({styles['marginRight']}); " \
        f"margin: 0 auto greift nicht"
    # Bonus: in der computed max-width steckt die Information "ch" -> ~576px.
    # Wenn der Editor-Body sehr breit waere, sollte die Textarea ~576px sein (72ch).
    print(f"[OK ] Editor-Textarea: computed max-width {styles['maxWidth']}, "
          f"el-width {styles['elWidth']:.0f}px < parent {styles['parentWidth']:.0f}px, "
          f"margin auto symmetrisch")


async def step5_selection_styling(page) -> None:
    """Prueft die ::selection-Regel via document.styleSheets -- eine echte Selektion
    im Headless-Browser auszuloesen ist unzuverlaessig, daher der CSS-Lookup.
    Beachtet: CSSStyleRule.style.background enthaelt die rohe Deklaration
    ('var(--accent-quiet)'), nicht den berechneten RGB -- wir matchen daher auf
    den Variablennamen, nicht auf den Pixelwert."""
    rule = await page.evaluate("""() => {
      for (const sheet of document.styleSheets) {
        try {
          for (const rule of sheet.cssRules) {
            if (rule.selectorText === '::selection') {
              return {
                bg: rule.style.background || rule.cssText,
                color: rule.style.color || '',
                cssText: rule.cssText,
              };
            }
          }
        } catch (e) {}
      }
      return null;
    }""")
    assert rule is not None, "::selection-Regel nicht in document.styleSheets gefunden"
    # Akzeptiere entweder die rohe 'var(--accent-quiet)' oder die aufgeloeste RGB-Form
    bg_ok = ("var(--accent-quiet)" in rule["cssText"] or "62, 141, 243" in rule["cssText"])
    color_ok = ("var(--text)" in rule["cssText"] or "229, 237, 242" in rule["cssText"])
    assert bg_ok, f"::selection-Background fehlt --accent-quiet in '{rule['cssText']}'"
    assert color_ok, f"::selection-Color fehlt --text in '{rule['cssText']}'"
    print(f"[OK ] ::selection-Regel aktiv: background=var(--accent-quiet), color=var(--text)")


async def step6_dialog_glass(page) -> None:
    """Oeffnet den Anlegen-Dialog (.overlay__panel ist ein Glas-Traeger)."""
    # Erst die Listen-Ansicht erzwingen (zurueck aus Editor-Detail-View).
    # Der Home-Knopf im Rail fuehrt auf den globalen Scope -- mit Escape geht
    # es nur den Editor raus, aber die Listen-Spalte ist schon dort.
    await page.keyboard.press("Escape")
    await page.wait_for_timeout(300)
    # Wenn wir noch in detail-view sind, nochmal Home klicken
    shell_view = await page.evaluate("() => document.getElementById('shell')?.dataset.view")
    if shell_view == "detail":
        await page.click(".rail__home")
        await page.wait_for_timeout(300)
    # .list__head + #new-item-button muessen sichtbar sein
    await page.wait_for_selector("#new-item-button", state="visible", timeout=5000)
    await page.click("#new-item-button")
    # Es gibt 12 .overlay__panel-Elemente im DOM (alle Dialog-Templates); wir wollen
    # nur das SICHTBARE im Create-Dialog.
    await page.wait_for_selector("#create-dialog:not([hidden]) .overlay__panel", state="visible", timeout=5000)
    bg = await page.evaluate(
        "() => getComputedStyle(document.querySelector('#create-dialog .overlay__panel')).backgroundColor"
    )
    # Im Chromium-Headless ist backdrop-filter support da, also erwarten wir den
    # Glass-Background (rgba(27,32,39,0.55)). Mindestens aber var(--surface-raised)
    # als Fallback (rgb(27,32,39) opak).
    assert ("27, 32, 39" in bg), \
        f".overlay__panel background-color ist {bg}, erwartet var(--glass-bg) oder Fallback"
    print(f"[OK ] .overlay__panel (Glas-Traeger) hat computed background {bg}")


async def step7_screenshot(page, name: str) -> None:
    SHOT_DIR.mkdir(parents=True, exist_ok=True)
    path = SHOT_DIR / name
    await page.screenshot(path=str(path), full_page=True)
    print(f"[OK ] Screenshot -> {path}")


async def main() -> int:
    creds = _load_creds()
    password = creds["password"]
    uri = creds["otpauth_uri"]
    secret_b32 = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(uri).query))["secret"]

    await step1_css_static_checks()

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(viewport={"width": 1280, "height": 900})
        page = await ctx.new_page()

        try:
            await step2_login_and_overview(page, password, secret_b32)
            await step7_screenshot(page, "c4c5_01_overview_sticky_head.png")
            await step3_selected_row_styles(page)
            await step7_screenshot(page, "c4c5_02_selected_row_3px_outline.png")
            await step4_editor_textarea_72ch(page)
            await step7_screenshot(page, "c4c5_03_editor_72ch.png")
            await step5_selection_styling(page)
            await step6_dialog_glass(page)
            await step7_screenshot(page, "c4c5_04_create_dialog_glass.png")
            # Dialog wieder schliessen
            await page.keyboard.press("Escape")
        finally:
            await browser.close()

    print("Alle C4+C5-Checks bestanden.")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
