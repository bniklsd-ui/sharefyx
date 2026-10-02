#!/usr/bin/env python3
"""P9 Block doing — Browser-Selbstprüfung des fünften Eimers (Mini-Plan §6, P9-59 – P9-65).

**Kopie der Login-/API-Teile von `p9_step_g_self_check.py`, kein Import** — dieselbe Begründung
wie beim Wegwerf-Skript: die Step-G-Skripte hängen an Modulkonstanten, ein Import würde sie
verbiegen.

**Warum ein Browser und nicht nur Tests.** Kein statischer Test beweist, dass ein Rail-Zähler im
Browser umspringt, wenn der Editor etwas speichert. Der Kernbeleg des ganzen Blocks ist genau das
(Station **S6**): `afterWrite()` → `loadOverview()` (`editor.js`) muss die Übersicht neu laden,
damit `renderRail()` die neuen Zahlen zeichnet. Ein Test, der nur `_overview()` fragt, prüft
diese Kette nicht — er fragt den Server, der die ganze Zeit richtig war.

Stationen (Mini-Plan §6):

  1  Übersicht: die Zeile `alpha` trägt den Chip „1 In Arbeit"
  2  Rail: **fünf** Eimer in der Reihenfolge `open, doing, done, note, archived`, alle mit
     deutschem Label
  3  Zähler: `offen` = 1, `in Arbeit` = 1
  4  Ordner „In Arbeit": genau `Laufende Probe`, Brotkrumen `alpha › In Arbeit`
  5  **Schreibpfad**: `Offene Probe` öffnen, `#meta-panel` aufklappen, `#field-status` auf
     `doing`, speichern — Toast „Gespeichert"
  6  **ohne Reload** neu lesen: `offen` = 0, `in Arbeit` = 2
  7  API-Gegenprobe mit derselben Sitzung: die Rail-Texte sind die Serverzahlen
  8  Das umgeschaltete Item: `status == "doing"` **und** `assignee == "alpha"` — das UI-Speichern
     hat die Zuweisung nicht verloren (P9-W)

S6 ist die Station, für die es den Browser braucht; S8 die, für die es die API-Gegenprobe
braucht, weil ein Rail-Zähler niemals `assignee` anzeigt.

Aufruf (Hard Rule 9: Stopp ausschließlich über die PID-Datei des Wegwerf-Skripts):
    python phase9_hardening/scripts/p9_doing_wegwerf.py start
    ~/.claude-code-tools/e2e-venv/bin/python phase9_hardening/scripts/p9_doing_self_check.py
    python phase9_hardening/scripts/p9_doing_wegwerf.py stop
"""
from __future__ import annotations

import argparse
import base64
import datetime
import hashlib
import hmac
import json
import struct
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from playwright.sync_api import Page, sync_playwright

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = REPO_ROOT / "docs" / "screenshots"
PROBE_DIR = REPO_ROOT / "phase9_hardening" / "probes"
DEFAULT_BASE_URL = "https://127.0.0.1:18776"   # eigene TLS-Instanz, siehe Wegwerf-Docstring
DEFAULT_CREDS = Path("/tmp/opencode/p9-doing-wegwerf/credentials.json")

# S2/S3 erwarten genau diese Reihenfolge (P9-X). Als Konstante im Test, nicht im Skript
# erfunden — sonst prüfte der Browser die Skriptannahme statt der Entscheidung.
ERWARTETE_EIMER = ["open", "doing", "done", "note", "archived"]
ERWARTETE_LABELS = ["Offen", "In Arbeit", "Erledigt", "Notizen", "Archiv"]

befunde: list[dict] = []


def pruefe(name: str, ok: bool, detail: str = "") -> None:
    befunde.append({"pruefung": name, "ok": bool(ok), "detail": detail})
    print(f"  [{'OK ' if ok else 'FEHLER'}] {name}" + (f" — {detail}" if detail else ""),
          file=sys.stderr)


# --- TOTP/Login (entliehen aus p9_step_g_self_check.py) --------------------------------------


def _generate_totp(otpauth_uri: str) -> str:
    qs = urllib.parse.parse_qs(urllib.parse.urlparse(otpauth_uri).query)
    secret_b32 = qs["secret"][0]
    key = base64.b32decode(secret_b32 + "=" * (-len(secret_b32) % 8))
    msg = struct.pack(">q", int(time.time() // 30))
    h = hmac.new(key, msg, hashlib.sha1).digest()
    offset = h[-1] & 0x0F
    return f"{(struct.unpack('>I', h[offset:offset + 4])[0] & 0x7FFFFFFF) % 1000000:06d}"


def login(page: Page, base_url: str, password: str, otpauth_uri: str) -> bool:
    for _fenster in range(2):
        page.goto(f"{base_url}/ui/login", wait_until="domcontentloaded")
        page.locator('input[name="space"]').fill("alpha")
        page.locator('input[name="password"]').fill(password)
        page.locator('input[name="totp"]').fill(_generate_totp(otpauth_uri))
        with page.expect_response("**/ui/login**") as info:
            page.locator('button[type="submit"]').click()
        if info.value.status in (200, 303):
            time.sleep(2.0)
            if not page.url.startswith(f"{base_url}/ui/"):
                page.goto(f"{base_url}/ui/", wait_until="domcontentloaded")
            return True
        time.sleep(35)
    return False


def _api(base_url: str, path: str, *, cookie: str, method: str = "GET", body: str = "") -> tuple:
    """Rohzugriff auf die eigene API — dieselbe Sitzung wie der Browser. `unverified` betrifft
    nur das selbstsignierte Harness-Zertifikat (dieselbe Ausnahme wie `ignore_https_errors` im
    Browser); am Server ändert das nichts — CSRF und Sitzung laufen durch den Browser, nicht
    durch diesen Aufruf. Deshalb wird für **GET**-Gegenproben benutzt und nie für einen
    Schreibvorgang."""
    import ssl

    req = urllib.request.Request(f"{base_url}{path}", data=body.encode() or None, method=method)
    req.add_header("Cookie", cookie)
    if body:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, context=ssl._create_unverified_context()) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()


def _ziffer(locator) -> str:
    return locator.inner_text().strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default=DEFAULT_BASE_URL)
    ap.add_argument("--creds", type=Path, default=DEFAULT_CREDS)
    args = ap.parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    PROBE_DIR.mkdir(parents=True, exist_ok=True)

    creds = json.loads(args.creds.read_text())
    with sync_playwright() as pw:
        # `ignore_https_errors` nur für das **selbstsignierte** Harness-Zertifikat. Sonst nichts:
        # Sitzung, CSRF, Origin und die TLS-Prüfung des Servers laufen normal.
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900},
                                ignore_https_errors=True)
        page.goto(f"{args.base_url}/ui/login", wait_until="domcontentloaded")
        # TOTP-Fenster abwarten, statt ein verbrauchtes zu senden (Login-Rate-Limit!).
        time.sleep(32 - (datetime.datetime.now().second % 30))
        if not login(page, args.base_url, creds["password"], creds["otpauth_uri"]):
            print("Login fehlgeschlagen", file=sys.stderr)
            return 2
        try:
            page.locator("#update-banner-dismiss").click(timeout=800)
        except Exception:
            pass

        # --- S1: der Chip auf der Uebersicht --------------------------------------------
        chip = page.locator('.overview__space-count[data-space="alpha"][data-bucket="doing"]')
        chip_text = _ziffer(chip.first) if chip.count() else ""
        pruefe("S1 Uebersicht: Chip '1 In Arbeit' bei alpha",
               chip.count() == 1 and chip_text == "1 In Arbeit", repr(chip_text))
        page.screenshot(path=str(OUT_DIR / "p9_doing_01_uebersicht_chip.png"))

        # --- S2: fuenf Rail-Eimer in Reihenfolge, alle uebersetzt -----------------------
        # `[data-bucket]` als Selektor-Bestandteil ist Absicht: `.tree__folder` traegt auch die
        # **echten** Ordner (`bindFolderDropTarget`/`navigateFolder`), die mitgezaehlt werden
        # wuerden und die Zahl (=5) verfaelschen wuerden.
        page.locator('.overview__space-open[data-space="alpha"], .overview__space-open').filter(
            has_text="alpha").first.click()
        time.sleep(2.0)
        ordner = page.locator('.tree__folder[data-space="alpha"][data-bucket]')
        gefundene = [ordner.nth(i).get_attribute("data-bucket") for i in range(ordner.count())]
        labels = [ordner.nth(i).locator(".rail__label").inner_text() for i in range(ordner.count())]
        pruefe("S2 Rail: fuenf Eimer in Reihenfolge open, doing, done, note, archived",
               gefundene == ERWARTETE_EIMER, f"{gefundene}")
        pruefe("S2 Rail: alle fuenf Labels deutsch, keines roh 'doing'",
               labels == ERWARTETE_LABELS, f"{labels}")
        # und der Count-Text: `0` ist erlaubt (ein Rail-Ordner existiert immer), `doing` als
        # Text waere der unuebersetzte Rueckfall `BUCKET_LABELS[b] || b`.
        zaehler = {gefundene[i]: _ziffer(ordner.nth(i).locator(".tree__count"))
                   for i in range(ordner.count())}
        page.screenshot(path=str(OUT_DIR / "p9_doing_02_rail_fuenf_ordner.png"))

        # --- S3: die Zaehler vor dem Schreibvorgang -------------------------------------
        pruefe("S3 Zaehler: Offen=1, In Arbeit=1",
               zaehler.get("open") == "1" and zaehler.get("doing") == "1", f"{zaehler}")

        # --- S4: der Ordner 'In Arbeit' zeigt genau die laufende Aufgabe ---------------
        # **Weiche Navigation.** Ein `click()` auf einen Ordner, den es nicht gibt, ist kein
        # roter Befund, sondern ein Absturz mit einem 30-Sekunden-Timeout — und der
        # Gegenlauf (nur D1/D2 zurückgenommen) braucht genau diesen Fall. Deshalb wird vorher
        # auf Existenz geprüft und jede Station meldet sich selbst rot, statt die Folge zu
        # blockieren: ein Skript, das beim Beweis des Lochs stirbt, beweist nichts.
        in_arbeit = ordner.filter(has=page.locator('.rail__label:text-is("In Arbeit")'))
        if in_arbeit.count() == 0:
            pruefe("S4 Liste 'In Arbeit' enthaelt genau die laufende Aufgabe", False,
                   "der Ordner 'In Arbeit' existiert nicht — kein Klick moeglich")
            pruefe("S4 Brotkrumen zeigen 'In Arbeit', nicht 'doing'", False,
                   "uebersprungen: S4 konnte nicht navigieren")
        else:
            in_arbeit.first.click()
            time.sleep(2.0)
            titel = [page.locator(".list__rows > li .list__row-title").nth(i).inner_text()
                     for i in range(page.locator(".list__rows > li").count())]
            brotkrume = page.locator("#list-crumb").inner_text().replace("\n", " ")
            pruefe("S4 Liste 'In Arbeit' enthaelt genau die laufende Aufgabe",
                   titel == ["Laufende Probe"], f"{titel}")
            pruefe("S4 Brotkrumen zeigen 'In Arbeit', nicht 'doing'",
                   "In Arbeit" in brotkrume and "doing" not in brotkrume, repr(brotkrume))
            page.screenshot(path=str(OUT_DIR / "p9_doing_03_liste_in_arbeit.png"))

        # --- S5: der Schreibpfad (das ist der Punkt der ganzen Instanz) -----------------
        ordner = page.locator('.tree__folder[data-space="alpha"][data-bucket]')
        offen_ordner = ordner.filter(has=page.locator('.rail__label:text-is("Offen")'))
        if offen_ordner.count() == 0:
            pruefe("S5 Editor: Status auf 'doing' gesetzt und gespeichert (Toast)", False,
                   "der Ordner 'Offen' existiert nicht — kein Schreibpfad pruefbar")
            item_id = None
        else:
            offen_ordner.first.click()
            time.sleep(2.0)
            zeile = page.locator(".list__rows > li", has_text="Offene Probe").first
            item_id = zeile.locator(".list__row").get_attribute("data-id")
            zeile.click()
            time.sleep(1.5)
            # `#meta-panel` ist ein `<details>`; es klappt sich beim Editor-Öffnen nicht zu,
            # aber ein späterer Reload-Sprung könnte es zufallen. Deshalb explizit aufklappen:
            # fehlt das, liefe `select_option` ins Leere und der Fehler läge scheinbar am Status.
            try:
                page.locator("#meta-panel:not([open]) summary").click(timeout=1500)
            except Exception:
                pass
            time.sleep(0.5)
            offen = page.locator("#meta-panel[open]").count() == 1
            # Der Wert kommt **roh** aus `state.meta.status_values` (P9-W) — `select_option` mit
            # dem Wert, den die Option wirklich trägt, nicht mit dem Rail-Label.
            page.locator("#field-status").select_option("doing")
            time.sleep(0.4)
            page.locator("#save-button").click()
            time.sleep(2.5)
            toast_sichtbar = page.locator(".toast").count() > 0
            toast_text = _ziffer(page.locator(".toast").first) if toast_sichtbar else ""
            pruefe("S5 Editor: Status auf 'doing' gesetzt und gespeichert (Toast)",
                   offen and toast_sichtbar and "Gespeichert" in toast_text,
                   f"meta-panel offen={offen} Toast={toast_text!r}")

        # --- S6: OHNE Reload neu lesen — der Kernbeleg ----------------------------------
        ordner = page.locator('.tree__folder[data-space="alpha"][data-bucket]')
        nach = {ordner.nth(i).get_attribute("data-bucket"):
                _ziffer(ordner.nth(i).locator(".tree__count")) for i in range(ordner.count())}
        pruefe("S6 ohne Reload: Offen 1->0, In Arbeit 1->2",
               nach.get("open") == "0" and nach.get("doing") == "2",
               f"vorher={zaehler} nachher={nach}")
        if "doing" in nach:
            page.screenshot(path=str(OUT_DIR / "p9_doing_04_nach_statuswechsel.png"))

        # --- S7: die Rail-Zahlen sind die Serverzahlen -----------------------------------
        cookies = {c["name"]: c["value"] for c in page.context.cookies()}
        cookie_header = "; ".join(f"{k}={v}" for k, v in cookies.items())
        status, raw = _api(args.base_url, "/api/v1/overview", cookie=cookie_header)
        try:
            overview = json.loads(raw)
        except ValueError:
            overview = []
        alpha = next((e for e in overview if e["name"] == "alpha"), {})
        server_counts = {k: str(v) for k, v in (alpha.get("counts") or {}).items()}
        pruefe("S7 API: /overview liefert genau die Rail-Zahlen (offen=0, doing=2)",
               status == 200 and server_counts == nach, f"HTTP {status} {server_counts} vs {nach}")
        status, raw = _api(
            args.base_url, "/api/v1/items?type=task&status=doing&space=alpha", cookie=cookie_header,
        )
        treffer = json.loads(raw).get("items", []) if status == 200 else []
        pruefe("S7 API: /items?type=task&status=doing liefert total=2",
               status == 200 and json.loads(raw).get("total") == 2,
               f"HTTP {status} {sorted(i['title'] for i in treffer)}")

        # --- S8: Maschinenebene roh, assignee erhalten (P9-W) ---------------------------
        if item_id is None:
            pruefe("S8 API: Item meldet status='doing' und assignee='alpha' unveraendert", False,
                   "uebersprungen: S5 lieferte keine Item-ID")
        else:
            status, raw = _api(args.base_url, f"/api/v1/items/{item_id}", cookie=cookie_header)
            item = json.loads(raw) if status == 200 else {}
            pruefe("S8 API: Item meldet status='doing' und assignee='alpha' unveraendert",
                   status == 200 and item.get("status") == "doing"
                   and item.get("assignee") == "alpha",
                   f"HTTP {status} status={item.get('status')!r} assignee={item.get('assignee')!r}")
        browser.close()

    report = {
        "base_url": args.base_url,
        "item_id": item_id,
        "befunde": befunde,
        "alle_ok": all(b["ok"] for b in befunde),
    }
    (PROBE_DIR / "p9_doing_probe.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False))
    print(f"\n{sum(b['ok'] for b in befunde)}/{len(befunde)} Pruefungen gruen", file=sys.stderr)
    return 0 if report["alle_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
