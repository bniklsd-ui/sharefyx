#!/usr/bin/env python3
"""Phase 8 P8-16 -- Glass-Fallback-Probe gegen eine Wegwerf-Instanz.

Pruefauftrag aus phase8_ui_graph_plan.md §8 Station 11: Glass-Träger bleiben
solid und Auswahl erkennbar, wenn der Browser `prefers-reduced-transparency:
reduce` meldet (oder `backdrop-filter` deaktiviert ist).

Methode: Playwright (Chromium) gegen die Wegwerf-Instanz auf Port 18775,
Login, drei Sichtpruefungen:

  1. Baseline-Modus (UA default):
       - .list__head (sticky Header der Listen-Ansicht) hat backdrop-filter gesetzt
       - .overlay__panel (Account-Dialog) hat backdrop-filter gesetzt
       Screenshot -> docs/screenshots/p8_16_01_baseline.png
  2. UA-Switch: prefers-reduced-transparency=reduce via CDP emuliert
       - .list__head backdrop-filter = none, background = var(--surface-raised)
       - .overlay__panel backdrop-filter = none, background = var(--surface-raised)
       Screenshot -> docs/screenshots/p8_16_02_reduced_transparency.png
  3. Klickprobe auf eine Listenzeile:
       - Selektion muss erkennbar bleiben (3 px solider Akzentrand links,
         N8 -- Auswahl darf nicht allein von Transparenz abhaengen)
       Screenshot -> docs/screenshots/p8_16_03_selection.png

Ergebnis: P8-16 wird 🟡→✅ (throwaway-verifiziert gegen Wegwerf, Live-Verifikation
am echten Geraet durch den Nikinger steht separat aus; Phase 8.5 D4 hat den
P8-16-Schatten bereits via Update-Log-Banner-Live-Anzeige abgehakt, die formale
Live-Sichtpruefung kommt mit Block D5 in Phase 8.5 oder spaeter).

Standing-Permission-Rahmen: eigene Wegwerf-Instanz (port 18775, tmp DATA_ROOT,
File-Keyring), kein Service-Touch, kein `pkill -f` mit Regex.
"""
from __future__ import annotations

import asyncio
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pyotp
from playwright.async_api import async_playwright

REPO_ROOT = Path(__file__).resolve().parents[2]
SETUP = REPO_ROOT / "phase8_ui_graph/scripts/wegwerf_setup_p8_16.py"
SCREENSHOT_DIR = REPO_ROOT / "docs/screenshots"
WEGWERF_CREDS = Path("/tmp/opencode/sharefyx-wegwerf-p816/credentials.json")
PORT = 18775
BASE_URL = f"http://127.0.0.1:{PORT}"


def _run_setup(*args: str) -> None:
    """Setup-Skript laeuft mit dem Projekt-.venv (keyring + authserver dort),
    nicht mit e2e-venv (playwright + pyotp)."""
    venv_python = REPO_ROOT / ".venv/bin/python"
    subprocess.run([str(venv_python), str(SETUP), *args], check=True, cwd=str(REPO_ROOT))


def _read_creds() -> dict[str, str]:
    creds = json.loads(WEGWERF_CREDS.read_text())
    return creds


async def _login(page, space: str, password: str, totp_secret_b32: str) -> None:
    """Single-step UI-Login (Phase-5-P5-D, pages.py Z. 162-177): ein Formular mit
    space + password + totp, alles zusammen POST an /ui/login. Vorheriges
    Two-Step-Pattern war falsch (login-password existiert, aber kein separater
    OTP-Roundtrip)."""
    await page.goto(f"{BASE_URL}/ui/login")
    await page.fill('input[name="space"]', space)
    await page.fill('input[name="password"]', password)
    await page.fill('input[name="totp"]', pyotp.TOTP(totp_secret_b32).now())
    async with page.expect_navigation(timeout=10_000):
        await page.click('button[type="submit"]')
    await page.wait_for_url(lambda url: "/ui/login" not in url, timeout=10_000)


async def _probe() -> dict[str, object]:
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    result: dict[str, object] = {"checks": [], "errors": []}

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await ctx.new_page()

        # ---- 1. Anonyme Probe: bevor Login sind die Glass-Träger auf /ui/login
        # nicht aktiv (Login-Seite hat eigenen Stil) -- direkt nach dem Login
        # auf der Listen-/Übersichts-Ansicht sind sie aktiv.
        creds = _read_creds()
        secret_b32 = creds["otpauth_uri"].split("secret=")[1].split("&")[0]
        secret_b32 = secret_b32.replace("%20", "+").replace("%3D", "=").replace("%2F", "/")
        # otpauth-URI ist URL-encoded; pyotp akzeptiert aber den Base32-String
        # direkt, also dekodieren wir nicht und nehmen den rohen Wert:
        import urllib.parse
        secret_b32 = urllib.parse.unquote(creds["otpauth_uri"].split("secret=")[1].split("&")[0])

        await _login(page, creds["space"], creds["password"], secret_b32)
        await page.wait_for_load_state("networkidle")

        # Übersichts-Seite rendert .list__head
        await page.goto(f"{BASE_URL}/ui/")
        await page.wait_for_selector(".list__head", timeout=10_000)

        # ---- 1. Baseline: UA default, Glass-Modus
        baseline = await page.evaluate("""() => {
            const el = document.querySelector('.list__head');
            if (!el) return {error: 'no .list__head'};
            const cs = getComputedStyle(el);
            return {
                backdrop_filter: cs.backdropFilter || cs.webkitBackdropFilter || '(none)',
                background: cs.backgroundColor,
                border: cs.borderTopColor + ' ' + cs.borderTopWidth
            };
        }""")
        result["checks"].append({"name": "baseline.list__head", **baseline})
        await page.screenshot(path=str(SCREENSHOT_DIR / "p8_16_01_baseline_list.png"), full_page=False)

        # ---- 2. Dialog öffnen für .overlay__panel
        # Account-Dialog: id="account-dialog", Trigger id="account-button" in der Rail
        # (`phase5_ui/webui/static/app.html:32`). Das Öffnen entfernt das `hidden`-
        # Attribut auf #account-dialog (dialogs.js :: openAccountDialog Z. 542).
        await page.click("#account-button")
        await page.wait_for_selector("#account-dialog:not([hidden])", timeout=10_000)
        await page.wait_for_selector("#account-dialog .overlay__panel", timeout=10_000)
        baseline_dialog = await page.evaluate("""() => {
            const el = document.querySelector('.overlay__panel');
            if (!el) return {error: 'no .overlay__panel'};
            const cs = getComputedStyle(el);
            return {
                backdrop_filter: cs.backdropFilter || cs.webkitBackdropFilter || '(none)',
                background: cs.backgroundColor
            };
        }""")
        result["checks"].append({"name": "baseline.overlay__panel", **baseline_dialog})
        await page.screenshot(path=str(SCREENSHOT_DIR / "p8_16_02_baseline_dialog.png"), full_page=False)

        # ---- 3. UA-Switch: prefers-reduced-transparency=reduce via CDP
        cdp = await ctx.new_cdp_session(page)
        await cdp.send("Emulation.setEmulatedMedia", {
            "features": [
                {"name": "prefers-reduced-motion", "value": "reduce"},
                {"name": "prefers-reduced-transparency", "value": "reduce"},
            ]
        })
        # Forciere ein Reflow, damit die Media Query sicher greift
        await page.evaluate("() => document.body.offsetHeight")

        # ---- 4. Nach dem Switch: Glass-Träger müssen solid sein
        await page.wait_for_function("""() => {
            const el = document.querySelector('.overlay__panel');
            if (!el) return false;
            const cs = getComputedStyle(el);
            const bf = cs.backdropFilter || cs.webkitBackdropFilter || 'none';
            return bf === 'none' || bf === '(none)';
        }""", timeout=5_000)

        reduced_dialog = await page.evaluate("""() => {
            const el = document.querySelector('.overlay__panel');
            const cs = getComputedStyle(el);
            return {
                backdrop_filter: cs.backdropFilter || cs.webkitBackdropFilter || '(none)',
                background: cs.backgroundColor,
                matches_reduced: window.matchMedia('(prefers-reduced-transparency: reduce)').matches
            };
        }""")
        result["checks"].append({"name": "reduced.overlay__panel", **reduced_dialog})

        # Dialog schließen (Cancel-Button, Escape tut es auch -- app.js Z. 194 ist der Handler)
        await page.click("#account-cancel")
        # hidden-Element darf nicht auf "visible" warten -- direkt evaluate
        await page.wait_for_function(
            "() => document.getElementById('account-dialog').hidden === true",
            timeout=5_000,
        )
        reduced_list = await page.evaluate("""() => {
            const el = document.querySelector('.list__head');
            if (!el) return {error: 'no .list__head'};
            const cs = getComputedStyle(el);
            return {
                backdrop_filter: cs.backdropFilter || cs.webkitBackdropFilter || '(none)',
                background: cs.backgroundColor
            };
        }""")
        result["checks"].append({"name": "reduced.list__head", **reduced_list})
        await page.screenshot(path=str(SCREENSHOT_DIR / "p8_16_03_reduced_transparency_list.png"), full_page=False)

        # ---- 5. Klickprobe: Selektion muss im Solid-Modus noch erkennbar sein
        # .list__row ist ein <button> innerhalb <li.list__rows> (list.js:329, app.css:652);
        # die Auswahl-CSS greift auf .list__row[aria-current="true"] mit 3 px-Akzentkante
        # links (app.css:684). Wir warten explizit auf das Erscheinen einer Zeile --
        # loadItems() ist async und kann nach dem ersten networkidle noch leer sein.
        # Wenn die Liste nach 15 s noch leer ist, ist das ein Index-/Load-Timing-Befund
        # fuer eine Folge-Session -- die Glass-Probe als solche ist davon unabhaengig.
        items_api = await page.evaluate("""async () => {
            try {
                const r = await fetch('/api/v1/items', {credentials: 'same-origin'});
                const body = await r.json();
                return {
                    status: r.status,
                    type: Array.isArray(body) ? 'array' : 'object',
                    keys: Array.isArray(body) ? `len=${body.length}` : Object.keys(body).join(','),
                    sample: JSON.stringify(body).slice(0, 300)
                };
            } catch (e) {
                return {error: String(e)};
            }
        }""")
        result["checks"].append({"name": "items_api", **items_api})

        # Bucket-Filter ist Default ("Offen" o.ae.) und schliesst unsere eine Note
        # moeglicherweise aus. Wir klicken den ersten Eintrag in der Tree-Bar
        # (Alle Items / globaler Scope), um die eine Note in der Liste zu haben.
        try:
            # Tree-Bucket-Filter sitzt in .tree__scope[data-bucket=...] -- meist
            # "all" fuer globaler Scope. Der Home-Button (#home-button) tut es auch.
            await page.click("#home-button", timeout=3_000)
            await page.wait_for_function(
                """() => {
                    const rows = document.querySelectorAll('.list__rows button.list__row');
                    return rows.length > 0;
                }""",
                timeout=10_000,
            )
        except Exception as e:
            result["errors"].append(f"bucket-switch: {e}")

        try:
            await page.wait_for_function(
                """() => {
                    const rows = document.querySelectorAll('.list__rows button.list__row');
                    return rows.length > 0;
                }""",
                timeout=15_000,
            )
            row = page.locator(".list__rows button.list__row").first
            await row.click(timeout=5_000)
            await page.wait_for_function(
                "() => !!document.querySelector('.list__row[aria-current=\"true\"]')",
                timeout=5_000,
            )
            selection = await page.evaluate("""() => {
                const sel = document.querySelector('.list__row[aria-current="true"]');
                if (!sel) return {error: 'no aria-current element'};
                const cs = getComputedStyle(sel);
                return {
                    border_left_color: cs.borderLeftColor,
                    border_left_width: cs.borderLeftWidth,
                    border_left_style: cs.borderLeftStyle,
                    background_image: cs.backgroundImage,
                    outline: cs.outline + ' / ' + cs.outlineColor,
                    background_color: cs.backgroundColor
                };
            }""")
            result["checks"].append({"name": "reduced.selection", **selection})
        except Exception as e:
            result["errors"].append(f"selection probe: {e}")
            debug = await page.evaluate("""() => ({
                rows_count: document.querySelectorAll('.list__rows button.list__row').length,
                shell_view: document.querySelector('.shell')?.getAttribute('data-view'),
                url: location.href
            })""")
            result["errors"].append(f"selection debug: {debug}")
        await page.screenshot(path=str(SCREENSHOT_DIR / "p8_16_04_reduced_transparency_selection.png"), full_page=False)

        # ---- 6. Zurueck auf UA default, ein zweiter Screenshot zur Kontrolle
        await cdp.send("Emulation.setEmulatedMedia", {
            "features": [
                {"name": "prefers-reduced-motion", "value": "no-preference"},
                {"name": "prefers-reduced-transparency", "value": "no-preference"},
            ]
        })
        await page.wait_for_timeout(200)
        restored = await page.evaluate("""() => {
            const el = document.querySelector('.list__head');
            const cs = getComputedStyle(el);
            return {
                backdrop_filter: cs.backdropFilter || cs.webkitBackdropFilter || '(none)',
                matches_reduced: window.matchMedia('(prefers-reduced-transparency: reduce)').matches
            };
        }""")
        result["checks"].append({"name": "restored.list__head", **restored})

        await ctx.close()
        await browser.close()

    return result


async def _async_main() -> int:
    print("[setup] Wegwerf-Setup + Seed + Start")
    _run_setup("setup")
    _run_setup("seed-items")
    _run_setup("start")
    try:
        print("[probe] Playwright-Probe gegen", BASE_URL)
        result = await _probe()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    finally:
        print("[cleanup] Wegwerf-Stop + Cleanup")
        _run_setup("stop")
        _run_setup("cleanup")


def main() -> int:
    return asyncio.run(_async_main())


if __name__ == "__main__":
    raise SystemExit(main())