"""Phase 8.6 Block C -- Self-Sichtpruefung (Plan §5, C1-C5 + D3-Nachzug).

Schiesst sechs Screenshots gegen die laufende Wegwerf-Instanz auf Port 18773:
  1. Uebersicht (Einstellungen oben, Abmelden unten, "Alle Items" unter den Spaces,
     Karte als rechte Spalte voller Hoehe, klickbare Space-Zeile mit Folder-Zaehler)
  2. Detail-Ansicht nach Klick auf Space-Zeile (space-navigation funktioniert)
  3. Hover auf Space-Zeile in der Uebersicht (quiet-Selektion sichtbar)
  4. Liste im "Alle Items"-Modus (zeigt Folder-Zaehler an echten Ordnern)
  5. Editor geoeffnet (Archivieren in Vorsicht-Farbe -- Regression-Test aus Block B)
  6. Karte allein (rechte Spalte, kein Abschneiden mehr -- V112-Gegenprobe)

Die Screenshots werden nach docs/screenshots/ geschrieben und am Ende der Session mit
dem eingebauten `read`-Tool gelesen + beschrieben. Hard Rule 9: Stop nur ueber PID-Datei.

TOTP-Generierung NEU VOR jedem Login-Versuch (nicht vorgeneriert). Bei 401 (TOTP
verbraucht durch vorherigen Versuch) wird 35s auf das naechste 30-Sek-Fenster
gewartet -- der Server lehnt denselben Code in derselben Periode ab (TOTP-Replay-
Schutz, RFC 6238). Bei 429 (Rate-Limit) 65s warten.
"""
from __future__ import annotations

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

CREDS_PATH = Path("/tmp/opencode/sharefyx-wegwerf-v3ritt/credentials.json")
BASE = "http://127.0.0.1:18773"
OUT_DIR = Path("docs/screenshots")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def _read_creds() -> dict[str, str]:
    return json.loads(CREDS_PATH.read_text())


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


def _login(page: Page, password: str, otpauth_uri: str) -> None:
    """Login mit TOTP.

    Strategie: vor dem ersten Versuch warten, bis ein frisches 30-Sek-Fenster
    beginnt (max 35s), dann EIN Login-Versuch. Bei 401 (TOTP verbraucht) oder
    429 (Rate-Limit) ein Retry nach 35s bzw. 65s im naechsten Fenster.
    """
    secs_into = datetime.datetime.now().second
    wait = 35 - (secs_into % 30)
    print(f"Login: warte {wait}s auf frisches TOTP-Fenster...")
    time.sleep(wait)

    for window in range(2):
        page.goto(f"{BASE}/ui/login", wait_until="domcontentloaded")
        page.locator('input[name="space"]').fill("alpha")
        page.locator('input[name="password"]').fill(password)
        totp_code = _generate_totp(otpauth_uri)
        counter = int(time.time() // 30)
        print(f"  Fenster {window + 1}: TOTP {totp_code} (counter {counter})")
        page.locator('input[name="totp"]').fill(totp_code)
        with page.expect_response("**/ui/login**") as resp_info:
            page.locator('button[type="submit"]').click()
        resp = resp_info.value
        print(f"  Fenster {window + 1}: HTTP {resp.status}")
        if resp.status in (200, 303):
            # Login erfolgreich -- aber der Server redirect't NICHT auf /ui/ per HTTP,
            # sondern gibt eine "Angemeldet"-Bootstrap-Seite zurueck (pages.py ::
            # render_logged_in_page()), die via JS (`location.replace("/ui/")` in app.js's
            # bootstrapCsrf-IIFE) auf /ui/ springt. Das ist ein JS-Redirect, kein
            # HTTP-Redirect -- `wait_for_url` erwischt es nicht zuverlaessig. Pragmatisch:
            # einfach 3s warten, dann ist der Redirect durch, und die App ist geladen.
            time.sleep(3.0)
            # Sanity-Check: sind wir wirklich auf /ui/ ?
            if not page.url.startswith(f"{BASE}/ui/"):
                # Falls nicht, manuell navigieren
                page.goto(f"{BASE}/ui/", wait_until="domcontentloaded")
                page.wait_for_load_state("domcontentloaded", timeout=5000)
            return
        if resp.status == 401:
            print(f"  TOTP verbraucht, warte 35s auf naechstes Fenster...")
            time.sleep(35)
            continue
        if resp.status == 429:
            print(f"  Rate-Limit aktiv, warte 65s...")
            time.sleep(65)
            continue
        raise RuntimeError(f"unexpected login status {resp.status}")
    raise RuntimeError("login failed in 2 fresh windows (manual check needed)")


def _screenshot(page: Page, name: str, note: str) -> None:
    """Screenshot + stdout-Ausgabe mit Dateiname + visuellem Checkkriterium.

    Konvention (Phase-Head §Vormerkungen "screenshots_latest/", 2026-09-11): wenn M3
    einen Screenshot fuer eine Sichtpruefung aufnimmt, sagt es (a) Dateiname und
    (b) kurzes Checkkriterium. Hier gibt (note) das Checkkriterium als String mit;
    das eigentliche "Sehen" passiert durch M3 nach dem Schreiben ueber das `read`-Tool.
    """
    path = OUT_DIR / name
    page.screenshot(path=str(path))
    print(f"OK {name} -- {note}")


def main() -> int:
    creds = _read_creds()
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()
        _login(page, creds["password"], creds["otpauth_uri"])
        page.wait_for_load_state("networkidle")
        time.sleep(0.5)

        # Screenshot 01: Uebersicht (alle Block-C-Aspekte in einem Bild)
        # C1: Einstellungen oben + Logout am Rail-Ende
        # C2: "Alle Items" mit "Alles"-Trenner UNTER den Spaces (am Rail-Ende)
        # C3: Karte als rechte Spalte, volle Hoehe (V112-Gegenprobe -- nicht abgeschnitten)
        # C4: Space-Zeilen klickbar (hover sichtbar)
        _screenshot(
            page, "p86_block_c_01_overview.png",
            "Einstellungen oben, Abmelden unten, Alle Items am Rail-Ende, Karte rechts voller Hoehe, "
            "Space-Zeilen klickbar",
        )

        # Screenshot 02: Detail nach Klick auf eine Space-Zeile (zeigt, dass C4 funktioniert)
        page.locator(".overview__space-open").first.click()
        page.wait_for_load_state("networkidle")
        time.sleep(0.5)
        _screenshot(
            page, "p86_block_c_02_after_space_click.png",
            "Nach Klick auf alpha-Space-Zeile -- Liste mit alpha-Items statt Uebersicht",
        )

        # Screenshot 03: Hover ueber einer Space-Zeile (quiet-Selektion sichtbar)
        page.goto(f"{BASE}/ui/", wait_until="domcontentloaded")
        page.wait_for_load_state("networkidle")
        time.sleep(0.5)
        page.locator(".overview__space-open").first.hover()
        time.sleep(0.3)
        _screenshot(
            page, "p86_block_c_03_space_hover.png",
            "Hover ueber Space-Zeile -- quiet-Selektion (B1-Hover, nicht Voll-Fuellung)",
        )

        # Screenshot 04: Im "Alle Items"-Modus -- Folder-Zaehler aus C5 sichtbar
        # Erst expandieren wir den alpha-Space (zeigt die echten Ordner mit Zaehler)
        page.goto(f"{BASE}/ui/", wait_until="domcontentloaded")
        page.wait_for_load_state("networkidle")
        time.sleep(0.5)
        page.locator(".tree__space").first.click()
        time.sleep(0.3)
        page.locator(".tree__scope").click()
        page.wait_for_load_state("networkidle")
        time.sleep(0.5)
        _screenshot(
            page, "p86_block_c_04_alle_items_with_folder_counts.png",
            "Alle Items-Modus -- rail__scope aktiv, Folder-Zaehler an echten Ordnern sichtbar",
        )

        # Screenshot 05: Zurueck zur Uebersicht und Editor oeffnen -- Vorsicht-Farbe
        # Regression-Check (Block B)
        page.goto(f"{BASE}/ui/", wait_until="domcontentloaded")
        page.wait_for_load_state("networkidle")
        time.sleep(0.5)
        page.locator(".list__row").first.click()
        page.wait_for_load_state("networkidle")
        time.sleep(0.5)
        _screenshot(
            page, "p86_block_c_05_editor_caution_regression.png",
            "Editor geoeffnet -- Archivieren-Knopf in Vorsicht-Farbe (B4-Regression-Check)",
        )

        # Screenshot 06: Karte allein -- unter 1280px kollabiert das Grid, Karte unter Liste
        page.goto(f"{BASE}/ui/", wait_until="domcontentloaded")
        page.wait_for_load_state("networkidle")
        time.sleep(0.5)
        page.set_viewport_size({"width": 1200, "height": 900})
        time.sleep(0.3)
        _screenshot(
            page, "p86_block_c_06_karte_unter_liste_1200px.png",
            "Unter 1280px kollabiert das Grid -- Karte UNTER der Liste, kein Abschneiden",
        )

        browser.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())