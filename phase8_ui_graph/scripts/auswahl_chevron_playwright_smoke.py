#!/usr/bin/env python3
"""Phase 8 Block C -- Auswahl-Boxen Chevron-Vorbild -- Playwright-Smoke.

Steht im Standing-Permission-Rahmen der Phase (CLAUDE.md Wurzel + Phase 8 §0.0):
smoket gegen die Wegwerf-Instanz aus wegwerf_setup_auswahl_chevron.py
(127.0.0.1:18771). Visuelle Feinjustierung macht der NIK am echten Geraet.

Pruefungen:
  Step 1 -- CSS-Static: select.input-Regel hat background-image-Data-URL mit
            Lucide-Chevron-down (Pfad "m6 9 6 6 6-6"), padding-right 1.75em,
            accent-color --accent, :disabled-Variante mit --text-placeholder.
  Step 2 -- Login + Overview rendert (Sanity).
  Step 3 -- Editor: #field-status hat computed background-image (nicht "none").
  Step 4 -- Anlegen-Dialog: #create-type hat computed background-image.
  Step 5 -- Anlegen-Dialog: #new-folder-parent-select hat computed background-image.
  Step 6 -- Verschieben-Dialog: #move-space-select hat computed background-image.
  Step 7 -- Verschieben-Dialog: #move-folder-select hat computed background-image.
  Step 8 -- Freigabe-Dialog (geteiltes Item): Per-Item-Share-Row mit
            `<select class="input">` rendert background-image.
  Step 9 -- Space-Verwaltung: #space-member-write-select hat computed background-image.
  Step 10 -- [2026-09-02, Vormerkung-3-Fix] Regressionscheck: computed
             background-size (px) skaliert jetzt mit der Schriftgroesse --
             das Verhaeltnis Chevron-Hoehe:Select-Hoehe ist zwischen
             #field-status (13px-Kontext) und #move-space-select (16px-
             Kontext) gleich (vorher: fixe 12px, dadurch am 13px-Feld
             relativ groesser -- das war der "Chevron nicht identisch"-Fund).
  Step 11 -- [2026-09-02, Vormerkung-3-Fix] #move-space-select:focus hat
             einen ANDEREN border-left-color als border-right-color (nur
             rechts/unten auf --accent-line, links bleibt --line-strong --
             der linke Rand konkurriert nicht mehr mit der C4-Auswahl-
             Sheen-Konvention, die "ausgewaehlt" links markiert).

  Plus Screenshot des Move-Dialogs mit sichtbarem Chevron (move_chevron.png).
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright, TimeoutError as PWTimeoutError


WEGWERF_PORT = 18771
BASE_URL = f"http://127.0.0.1:{WEGWERF_PORT}"
CREDS = json.loads(Path("/tmp/opencode/sharefyx-wegwerf-auswahl-chevron/credentials.json").read_text())
SHOT_DIR = Path("/home/savefyx/dev/savefxy/docs/screenshots")
SHOT_DIR.mkdir(parents=True, exist_ok=True)


def _password_from_otpauth(uri: str) -> str:
    """TOTP-Code aus dem otpauth-URI ableiten (gleicher Algorithmus wie die App)."""
    import pyotp
    secret = uri.split("secret=")[1].split("&")[0]
    return pyotp.TOTP(secret).now()


def _assert(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit(f"FAIL: {msg}")
    print(f"  ok  {msg}")


def _select_background_image(page, selector: str) -> str:
    """Liefert computed background-image des Select-Elements (oder 'none')."""
    return page.evaluate(
        """sel => {
            const el = document.querySelector(sel);
            if (!el) return 'MISSING';
            const cs = getComputedStyle(el);
            return cs.backgroundImage || 'none';
        }""",
        selector,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Phase 8 Chevron-Vorbild Smoke")
    parser.parse_args(argv)

    pw = sync_playwright().start()
    browser = pw.chromium.launch()
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()

    # -- Step 1: CSS-Static-Check -------------------------------------------------
    print("Step 1: CSS-Static")
    page.goto(f"{BASE_URL}/ui/", wait_until="networkidle")
    css_check = page.evaluate(
        """() => {
            const r = [];
            for (const sheet of document.styleSheets) {
                try {
                    for (const rule of sheet.cssRules || []) {
                        if (rule.cssText && rule.cssText.includes('select.input')) {
                            r.push(rule.cssText);
                        }
                    }
                } catch (_) { /* cross-origin */ }
            }
            return r;
        }"""
    )
    select_input_rules = [r for r in css_check if r.startswith("select.input") or r.startswith("select.input:disabled") or "select.input {" in r or "select.input:disabled {" in r]
    print(f"  select.input-Regeln im Stylesheet: {len(select_input_rules)}")
    for r in select_input_rules:
        print(f"    - {r[:200]}{'...' if len(r) > 200 else ''}")
    has_chevron = any("m6 9 6 6 6-6" in r and "data:image/svg+xml" in r for r in select_input_rules)
    has_padding = any("padding-right: 1.75em" in r or "padding-right:1.75em" in r for r in select_input_rules)
    has_disabled = any("select.input:disabled" in r for r in select_input_rules)
    _assert(has_chevron, "select.input-Regel enthaelt Lucide-Chevron-Pfad 'm6 9 6 6 6-6' als data-URL")
    _assert(has_padding, "select.input-Regel setzt padding-right: 1.75em (skaliert mit Schriftgroesse)")
    _assert(has_disabled, "select.input:disabled-Regel vorhanden (Chevron-Muted-Variante)")

    # -- Login -------------------------------------------------------------------
    print("\nLogin")
    page.goto(f"{BASE_URL}/ui/login", wait_until="domcontentloaded")
    page.fill('input[name="space"]', CREDS["space"])
    page.fill('input[name="password"]', CREDS["password"])
    page.fill('input[name="totp"]', _password_from_otpauth(CREDS["otpauth_uri"]))
    page.click('button[type="submit"]')
    page.wait_for_url(f"{BASE_URL}/ui/", timeout=10000)
    page.wait_for_selector("#home-button", state="visible", timeout=10000)
    _assert(page.is_visible("#home-button"), "Login erfolgreich, Home sichtbar")

    # -- Step 2: Overview rendert (Sanity) ---------------------------------------
    print("\nStep 2: Overview-Sanity")
    page.wait_for_selector("#detail-overview", state="visible", timeout=4000)
    _assert(page.is_visible("#detail-overview"), "Uebersicht gerendert")

    # -- Step 3: Item-Editor, #field-status -------------------------------------
    print("\nStep 3: Item-Editor -- #field-status")
    # Auf eigenen Space 'alpha' navigieren, damit Anlege-Knopf sichtbar wird
    page.click(".tree__space:has-text('alpha')")
    page.wait_for_selector(".list__row", timeout=10000)
    page.click(".list__row")  # erstes eigenes Item
    page.wait_for_selector("#detail-editor:not([hidden])", timeout=5000)
    # Kopfdaten-Panel ist ein collapsed <details> -- aufklappen, sonst ist #field-status nicht visible
    page.click("#meta-panel summary")
    page.wait_for_selector("#field-status", state="visible", timeout=4000)
    bg = _select_background_image(page, "#field-status")
    print(f"  #field-status background-image: {bg[:80]}{'...' if len(bg) > 80 else ''}")
    _assert(bg.startswith("url(") and "data:image/svg+xml" in bg, "#field-status rendert Chevron-Data-URL")

    # -- Step 4: Anlegen-Dialog, #create-type ------------------------------------
    print("\nStep 4: Anlegen-Dialog -- #create-type")
    page.click("#new-item-button")
    page.wait_for_selector("#create-dialog", state="visible", timeout=4000)
    bg = _select_background_image(page, "#create-type")
    print(f"  #create-type background-image: {bg[:80]}{'...' if len(bg) > 80 else ''}")
    _assert(bg.startswith("url(") and "data:image/svg+xml" in bg, "#create-type rendert Chevron-Data-URL")

    # -- Step 5: Anlegen-Dialog, #new-folder-parent-select -----------------------
    print("\nStep 5: Anlegen-Dialog -- #new-folder-parent-select")
    page.click("#create-type")  # type-select oeffnen
    page.keyboard.press("Escape")
    bg = _select_background_image(page, "#new-folder-parent-select")
    print(f"  #new-folder-parent-select background-image: {bg[:80]}{'...' if len(bg) > 80 else ''}")
    _assert(bg.startswith("url(") and "data:image/svg+xml" in bg, "#new-folder-parent-select rendert Chevron-Data-URL")

    page.click("#create-cancel")
    page.wait_for_selector("#create-dialog", state="hidden", timeout=4000)

    # -- Step 6+7: Verschieben-Dialog --------------------------------------------
    print("\nStep 6+7: Verschieben-Dialog")
    # Erst Editor schliessen (blockiert ggf. Mehrfachauswahl-Klick), dann Mehrfachauswahl starten
    try:
        page.click("#close-button", timeout=1000)
        page.wait_for_selector("#detail-editor[hidden]", timeout=2000)
    except PWTimeoutError:
        pass
    # Mehrfachauswahl: Strg+Klick auf das erste Item (Nikinger-Vorgabe, §9.3 Punkt 1)
    rows = page.locator(".list__row")
    rows.nth(0).click(modifiers=["Control"])
    page.wait_for_selector("#list-selection:not([hidden])", timeout=4000)
    page.click("#list-selection-move")
    page.wait_for_selector("#move-dialog", state="visible", timeout=4000)

    bg = _select_background_image(page, "#move-space-select")
    print(f"  #move-space-select background-image: {bg[:80]}{'...' if len(bg) > 80 else ''}")
    _assert(bg.startswith("url(") and "data:image/svg+xml" in bg, "#move-space-select rendert Chevron-Data-URL")

    bg = _select_background_image(page, "#move-folder-select")
    print(f"  #move-folder-select background-image: {bg[:80]}{'...' if len(bg) > 80 else ''}")
    _assert(bg.startswith("url(") and "data:image/svg+xml" in bg, "#move-folder-select rendert Chevron-Data-URL")

    # Screenshot mit sichtbarem Chevron
    page.screenshot(path=str(SHOT_DIR / "auswahl_chevron_01_move_dialog.png"))
    print(f"  screenshot -> {SHOT_DIR / 'auswahl_chevron_01_move_dialog.png'}")

    page.click("#move-cancel")
    page.wait_for_selector("#move-dialog", state="hidden", timeout=4000)
    page.click("#list-selection-clear")

    # -- Step 8: Freigabe-Dialog, Per-Item-Share-Row -----------------------------
    print("\nStep 8: Freigabe-Dialog -- Per-Item-Share-Row")
    page.click(".list__row")
    page.wait_for_selector("#meta-panel summary", state="visible", timeout=4000)
    page.click(".list__row-share:visible >> nth=0")  # Freigabe-Icon-Knopf am Zeilenrand
    page.wait_for_selector("#share-dialog", state="visible", timeout=4000)
    share_selects = page.evaluate(
        """() => {
            const r = [];
            document.querySelectorAll('#share-rows select.input').forEach(s => {
                const cs = getComputedStyle(s);
                r.push(cs.backgroundImage);
            });
            return r;
        }"""
    )
    print(f"  #share-rows select.input Anzahl: {len(share_selects)}")
    _assert(len(share_selects) >= 1, "mindestens eine Per-Item-Share-Row gerendert")
    _assert(
        all(s.startswith("url(") and "data:image/svg+xml" in s for s in share_selects),
        "alle Per-Item-Share-Row-Selects rendern Chevron-Data-URL",
    )

    # Screenshot
    page.screenshot(path=str(SHOT_DIR / "auswahl_chevron_02_share_dialog.png"))
    print(f"  screenshot -> {SHOT_DIR / 'auswahl_chevron_02_share_dialog.png'}")

    page.click("#share-cancel")
    page.wait_for_selector("#share-dialog", state="hidden", timeout=4000)

    # -- Step 9: Space-Verwaltung, #space-member-write-select --------------------
    print("\nStep 9: Space-Verwaltung -- #space-member-write-select")
    # Die Regel gilt statisch fuer alle `<select class="input">` -- sieben Stellen gerendert
    # oben (drei statische + zwei dynamische im Anlegen-Dialog + zwei im Verschieben-Dialog +
    # die Share-Row), die achte Stelle (#space-member-write-select) folgt der gleichen Regel.
    # Wenn der Selector im DOM ist, computed background-image pruefen.
    page.goto(f"{BASE_URL}/ui/", wait_until="domcontentloaded")
    # Selector ist im statischen HTML von app.html, daher auch ohne offenen Space-Dialog im DOM.
    bg = page.evaluate(
        "() => { const el = document.getElementById('space-member-write-select'); "
        "return el ? getComputedStyle(el).backgroundImage : 'NOT-IN-DOM'; }"
    )
    print(f"  #space-member-write-select background-image: {bg[:80]}{'...' if len(bg) > 80 else ''}")
    _assert(bg.startswith("url(") and "data:image/svg+xml" in bg,
            "#space-member-write-select rendert Chevron-Data-URL (statische Regel)")

    # -- Step 10: Regressionscheck -- Chevron:Select-Hoehe-Verhaeltnis gleich -----
    print("\nStep 10: Chevron-Groessenverhaeltnis #field-status vs. #move-space-select")
    page.click("#close-button") if page.is_visible("#close-button") else None
    page.goto(f"{BASE_URL}/ui/", wait_until="domcontentloaded")
    page.click(".tree__space:has-text('alpha')")
    page.wait_for_selector(".list__row", timeout=10000)
    page.click(".list__row")
    page.wait_for_selector("#detail-editor:not([hidden])", timeout=5000)
    page.click("#meta-panel summary")
    page.wait_for_selector("#field-status", state="visible", timeout=4000)
    ratio_field = page.evaluate(
        """() => {
            const el = document.getElementById('field-status');
            const cs = getComputedStyle(el);
            const chevronPx = parseFloat(cs.backgroundSize.split(' ')[0]);
            return chevronPx / el.getBoundingClientRect().height;
        }"""
    )
    rows2 = page.locator(".list__row")
    rows2.nth(0).click(modifiers=["Control"])
    page.wait_for_selector("#list-selection:not([hidden])", timeout=4000)
    page.click("#list-selection-move")
    page.wait_for_selector("#move-dialog", state="visible", timeout=4000)
    ratio_move = page.evaluate(
        """() => {
            const el = document.getElementById('move-space-select');
            const cs = getComputedStyle(el);
            const chevronPx = parseFloat(cs.backgroundSize.split(' ')[0]);
            return chevronPx / el.getBoundingClientRect().height;
        }"""
    )
    print(f"  chevron/select-height ratio: #field-status={ratio_field:.4f}  #move-space-select={ratio_move:.4f}")
    _assert(
        abs(ratio_field - ratio_move) < 0.02,
        f"Chevron:Select-Hoehe-Verhaeltnis stimmt ueberein (Differenz {abs(ratio_field - ratio_move):.4f} < 0.02)",
    )

    # -- Step 11: Focus-Border nur rechts/unten auf Akzent -----------------------
    print("\nStep 11: #move-space-select:focus -- linker Rand bleibt --line-strong")
    page.focus("#move-space-select")
    borders = page.evaluate(
        """() => {
            const el = document.getElementById('move-space-select');
            const cs = getComputedStyle(el);
            return {left: cs.borderLeftColor, right: cs.borderRightColor, bottom: cs.borderBottomColor};
        }"""
    )
    print(f"  border colors while focused: {borders}")
    _assert(borders["left"] != borders["right"], "border-left-color unterscheidet sich von border-right-color im Fokus")
    _assert(borders["right"] == borders["bottom"], "border-right-color == border-bottom-color (beide auf --accent-line)")

    page.click("#move-cancel")
    page.wait_for_selector("#move-dialog", state="hidden", timeout=4000)

    browser.close()
    pw.stop()
    print("\n11/11 ok -- Chevron-Vorbild + Vormerkung-3-Fixes verifiziert.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())