#!/usr/bin/env python3
"""Phase 8.5 P8.5-19 -- Radiogruppe-Probe gegen die laufende 200-Knoten-Wegwerf (Port 18772).

Prueft C4-1 aus SICHTPRUEFUNG_WALKTHROUGH.md: der Link-Picker-Modus-Umschalter ist eine
Radiogruppe (`<input type="radio" name="link-picker-mode">`), nicht ein `<select>`; die
Auswahl bleibt nach dem Modus-Wechsel als `localStorage["sfx:linkpicker:mode"]` erhalten
(P8.5-19-Commit `14dcc3c`, `dialogs.js`/`app.html`).

Standing-Permission-Rahmen: liest nur die bereits laufende Wegwerf-Instanz, kein Setup/
Teardown hier, kein Service-Touch.
"""
from __future__ import annotations

import asyncio
import json
import urllib.parse
from pathlib import Path

import pyotp
from playwright.async_api import async_playwright

REPO_ROOT = Path(__file__).resolve().parents[2]
SCREENSHOT_DIR = REPO_ROOT / "docs" / "screenshots"
CREDS_PATH = Path("/tmp/opencode/sharefyx-wegwerf-200knoten/credentials.json")
PORT = 18772
BASE_URL = f"http://127.0.0.1:{PORT}"


def _read_creds() -> dict:
    creds = json.loads(CREDS_PATH.read_text())
    secret_b32 = urllib.parse.unquote(creds["otpauth_uri"].split("secret=")[1].split("&")[0])
    creds["_secret_b32"] = secret_b32
    return creds


async def _login(page, space: str, password: str, secret_b32: str) -> None:
    await page.goto(f"{BASE_URL}/ui/login")
    await page.fill('input[name="space"]', space)
    await page.fill('input[name="password"]', password)
    await page.fill('input[name="totp"]', pyotp.TOTP(secret_b32).now())
    async with page.expect_navigation(timeout=10_000):
        await page.click('button[type="submit"]')
    await page.wait_for_url(lambda url: "/ui/login" not in url, timeout=10_000)


async def _probe() -> dict:
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    creds = _read_creds()
    result: dict = {}

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await ctx.new_page()

        await _login(page, creds["space"], creds["password"], creds["_secret_b32"])
        await page.goto(f"{BASE_URL}/ui/")

        # Eingeloggt als alpha -- ein eigenes alpha-Item in der Liste oeffnet den Editor
        # direkt (eigene Items sind schreibbar, kein Readonly-Zwischenschritt noetig).
        await page.wait_for_selector(".list__rows button.list__row", timeout=15_000)
        await page.locator(".list__rows button.list__row").first.click()
        await page.wait_for_selector("#field-title", timeout=10_000)

        # Kopfdaten-Panel ist ein <details> und standardmaessig zugeklappt -- erst
        # aufklappen, sonst ist der Link-Picker-Knopf im DOM, aber nicht sichtbar.
        await page.click("#meta-panel summary")
        await page.wait_for_selector("#link-picker-button", state="visible", timeout=5_000)

        # Link-Picker oeffnen (Lupe, #i-search, `link-picker-button` im Kopfdaten-Panel).
        await page.click("#link-picker-button")
        await page.wait_for_selector('fieldset.link-picker-modes', timeout=10_000)

        radios = page.locator('input[name="link-picker-mode"]')
        result["radio_count"] = await radios.count()
        result["is_select_element"] = await page.locator("#link-picker-mode").count()

        values = []
        checked = []
        for i in range(await radios.count()):
            radios_i = radios.nth(i)
            values.append(await radios_i.get_attribute("value"))
            checked.append(await radios_i.is_checked())
        result["values"] = values
        result["checked_before"] = checked

        await page.screenshot(
            path=str(SCREENSHOT_DIR / "c4_p8519_01_radiogruppe_im_dialog.png"),
            full_page=False,
        )

        # Modus wechseln: klicke die aktuell NICHT markierte Option.
        target_index = checked.index(False) if False in checked else 1
        await radios.nth(target_index).click()

        ls_value = await page.evaluate("localStorage.getItem('sfx:linkpicker:mode')")
        result["localStorage_after_switch"] = ls_value
        result["switched_to_value"] = values[target_index]

        # Dialog schliessen + wieder oeffnen -- Persistenz pruefen.
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(200)
        await page.click("#link-picker-button")
        await page.wait_for_selector('fieldset.link-picker-modes', timeout=10_000)
        checked_after_reopen = []
        for i in range(await radios.count()):
            checked_after_reopen.append(await radios.nth(i).is_checked())
        result["checked_after_reopen"] = checked_after_reopen

        await ctx.close()
        await browser.close()

    return result


def _verdict(result: dict) -> tuple[bool, list[str]]:
    lines = []
    ok = True

    if result["is_select_element"] != 0:
        ok = False
        lines.append("[FAIL] #link-picker-mode <select> existiert noch -- Radio-Tausch nicht aktiv")
    else:
        lines.append("[OK]   kein <select id=\"link-picker-mode\"> mehr im DOM")

    if result["radio_count"] != 2:
        ok = False
        lines.append(f"[FAIL] {result['radio_count']} Radios gefunden, erwartet genau 2")
    else:
        lines.append(f"[OK]   genau 2 Radios: values={result['values']}")

    if sum(result["checked_before"]) != 1:
        ok = False
        lines.append(f"[FAIL] {sum(result['checked_before'])} Radios markiert vor dem Wechsel, erwartet 1")
    else:
        lines.append("[OK]   genau eine Option initial markiert")

    if result["localStorage_after_switch"] != result["switched_to_value"]:
        ok = False
        lines.append(
            f"[FAIL] localStorage nach Wechsel = {result['localStorage_after_switch']!r}, "
            f"erwartet {result['switched_to_value']!r}"
        )
    else:
        lines.append(
            f"[OK]   localStorage['sfx:linkpicker:mode'] = {result['localStorage_after_switch']!r} "
            f"nach dem Wechsel"
        )

    target_idx = result["values"].index(result["switched_to_value"])
    if not result["checked_after_reopen"][target_idx] or sum(result["checked_after_reopen"]) != 1:
        ok = False
        lines.append(
            f"[FAIL] nach Schliessen+Wiederoeffnen ist die Auswahl nicht erhalten: "
            f"{result['checked_after_reopen']}"
        )
    else:
        lines.append("[OK]   Auswahl bleibt nach Schliessen+Wiederoeffnen erhalten (Persistenz)")

    return ok, lines


async def _async_main() -> int:
    result = await _probe()
    print(json.dumps(result, indent=2))
    ok, lines = _verdict(result)
    print()
    for line in lines:
        print(line)
    print()
    print(f"P8.5-19-Bilanz: {'BESTANDEN' if ok else 'FEHLGESCHLAGEN'}")
    return 0 if ok else 1


def main() -> int:
    return asyncio.run(_async_main())


if __name__ == "__main__":
    raise SystemExit(main())
