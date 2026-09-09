#!/usr/bin/env python3
"""P8.5-6 Bracket-Pfad Mini-Smoke (Sichtung-Brake 2026-09-09).

Fährt einen Mini-Smoke gegen den laufenden v3ritt-Wegwerf und nimmt **zwei** Screenshots:
1. Edit-Ansicht mit eingefügtem Link auf das Bracket-titled Item "Vercel [Hosting]"
2. Vorschau-Panel-sichtbar mit demselben Link

Voraussetzungen:
- v3ritt-Wegwerf läuft auf Port 18773 (von wegwerf_setup_v3ritt.py setup,seed-items,start)
- Item "Vercel [Hosting]" wurde via Store.create im alpha-Space angelegt
- Pflicht-Screenshot-Konvention (siehe docs/concepts/sichtpruefung_automation_conventions.md §1)

Nutzung:  ~/.claude-code-tools/e2e-venv/bin/python phase8_5_picker_release/scripts/p856_bracket_mini_smoke.py
"""
import json
import sys
import time
from pathlib import Path
from urllib.parse import urlparse, parse_qs

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

import pyotp
from playwright.sync_api import sync_playwright

CREDS_FILE = Path("/tmp/opencode/sharefyx-wegwerf-v3ritt/credentials.json")
BASE = "http://127.0.0.1:18773"
SHOT_DIR = REPO_ROOT / "docs" / "screenshots"

# Login-Helfer (Pattern aus den Cluster-Smokes)
def _login(page) -> None:
    creds = json.loads(CREDS_FILE.read_text())
    secret = parse_qs(urlparse(creds["otpauth_uri"]).query)["secret"][0]
    code = pyotp.TOTP(secret).now()
    page.goto(f"{BASE}/ui/login", wait_until="domcontentloaded")
    page.fill('input[name="space"]', creds["space"])
    page.fill('input[name="password"]', creds["password"])
    page.fill('input[name="totp"]', code)
    page.click('button[type="submit"]')
    page.wait_for_url(lambda u: "/ui/login" not in u, timeout=10000)


def _go_home(page) -> None:
    """Klick auf Home-Button, dismisset ggf. Dirty-Prompt, bringt Übersicht zurück.
    Dann Buecherliste Q4 suchen und öffnen (gleicher Pattern wie die Smoke-Stations)."""
    page.click("#home-button")
    page.wait_for_timeout(800)
    confirm = page.locator("#confirm-dialog:not([hidden])")
    if confirm.count():
        page.click("#confirm-discard")
        page.wait_for_timeout(500)
    # Buecherliste Q4 in der Liste finden + klicken
    page.locator(".list__row", has_text="Buecherliste Q4").first.click()
    page.locator("#detail-editor:visible").wait_for(state="visible", timeout=10000)


def _ensure_edit_mode(page) -> None:
    """Editor öffnet standardmäßig im Preview-Modus. Wir schalten auf Edit um.
    Klappt das Meta-Panel auf, weil der Link-Picker-Knopf darin liegt.
    Idempotent (siehe v3_ritt_playwright_smoke.py)."""
    toggle = page.locator("#toggle-preview")
    if toggle.count():
        btn_text = toggle.inner_text().strip()
        if btn_text == "Bearbeiten":
            toggle.click()
            page.wait_for_timeout(300)
    page.locator("#editor-textarea:visible").wait_for(state="visible", timeout=10000)
    # Meta-Panel (Kopfdaten) aufklappen -- Link-Picker-Knopf liegt darin.
    meta = page.locator("#meta-panel")
    if meta.count():
        is_open = meta.evaluate("el => el.open")
        if not is_open:
            meta.locator("summary").click()
            page.wait_for_timeout(300)


def main() -> int:
    SHOT_DIR.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context()
        page = ctx.new_page()
        # Login
        _login(page)
        # Buecherliste Q4 öffnen
        _go_home(page)
        # Edit-Modus einschalten (Editor öffnet standardmäßig im Preview-Modus)
        _ensure_edit_mode(page)
        textarea = page.locator("#editor-textarea")
        textarea.click()
        # Cursor an Position 0 setzen
        page.evaluate(
            "() => { const t = document.getElementById('editor-textarea');"
            "t.setSelectionRange(0, 0); t.focus(); }"
        )
        # Link-Picker öffnen
        page.click("#link-picker-button")
        page.wait_for_selector("#link-picker-dialog:not([hidden])", timeout=5000)
        # Nach "Hosting" suchen — matcht "Vercel [Hosting]"
        page.fill("#link-picker-search", "Hosting")
        page.wait_for_timeout(500)
        # Ersten Treffer klicken (sollte der Bracket-Titel sein)
        page.locator("#link-picker-results li").first.click()
        page.wait_for_timeout(500)
        # Editor ist im Edit-Modus, Body enthält jetzt [Vercel \[Hosting\](#item/itm_b8b989a1)...
        # Screenshot 1: Edit-Ansicht
        edit_shot = SHOT_DIR / "p856_bracket_edit_view.png"
        page.screenshot(path=str(edit_shot), full_page=False)
        print(f"[OK ] Edit-Ansicht -> {edit_shot} ({edit_shot.stat().st_size} B)")
        # Vorschau-Panel einschalten (Toggle-Button — `editor.js:239` wechselt zwischen Preview und Edit)
        toggle = page.locator("#toggle-preview")
        if toggle.count() and "Vorschau" in toggle.inner_text():
            toggle.click()
            page.wait_for_timeout(500)
        else:
            print(f"[WARN] toggle-preview Text war nicht 'Vorschau', Inhalt: {toggle.inner_text()!r}")
        preview_shot = SHOT_DIR / "p856_bracket_preview.png"
        page.screenshot(path=str(preview_shot), full_page=False)
        print(f"[OK ] Vorschau-Panel -> {preview_shot} ({preview_shot.stat().st_size} B)")
        # Zur Sicherheit: Body + DOM inspizieren, damit wir wissen ob der Link korrekt gerendert ist
        body_after = textarea.input_value()
        # Im Preview-Modus: das gerenderte HTML im preview-Element lesen (id="editor-preview" oder aehnlich)
        preview_html = page.evaluate(
            "() => { const el = document.querySelector('#editor-preview, .editor-preview, [data-preview], #preview-pane');"
            "return el ? el.innerHTML : '(kein Preview-Element gefunden)'; }"
        )
        # Link im Preview-HTML suchen
        import re
        has_bracket_link = bool(
            re.search(r'<a[^>]+href="#item/itm_b8b989a1"[^>]*>Vercel \[Hosting\]</a>', preview_html)
        )
        print(f"[INFO] Body (Anfang 200 Zeichen): {body_after[:200]!r}")
        print(f"[INFO] Preview-HTML enthält klickbaren Bracket-Link: {has_bracket_link}")
        if not has_bracket_link:
            # Fallback: alle <a>-Tags im Preview ausgeben
            all_links = page.evaluate(
                "() => Array.from(document.querySelectorAll('#editor-preview a, .editor-preview a'))"
                ".map(a => ({href: a.getAttribute('href'), text: a.textContent}))"
            )
            print(f"[INFO] Alle <a>-Tags im Preview: {all_links}")
        browser.close()
        return 0 if has_bracket_link else 2


if __name__ == "__main__":
    sys.exit(main())
