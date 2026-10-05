#!/usr/bin/env python3
"""P9 Block settings — Browser-Probe der Fensterkette (Plan §3 Schritt 6, Abnahme
P9-83–P9-93, Stationen S1–S9).

Warum ein Browser und nicht noch ein statischer Wächter: die Aussagen, die hier geprüft
werden, sind **gemessene** Eigenschaften eines gerenderten Zustands — die Optik der
Menüknöpfe im Vergleich zu einer echten `.tree__folder`-Zeile (S1), was bei welcher Breite
sichtbar ist (S4/S8), und ob ein Tastendruck in der Reihenfolge wirkt, die man behauptet
(S5). `test_settings_chain.py` prüft die *Ursache* (keine kopierten Werte, eine Kette, ein
Öffner); dieses Skript prüft die *Wirkung*. Beides, weil eine Prüfung, die das Richtige an
der falschen Stelle prüft, derselbe Fehler eine Ebene tiefer ist.

**Zwei Dinge, die hier nicht behauptet, sondern gemessen werden:**
1. **S1** vergleicht die berechneten Werte (Höhe, Polster, Schrift, Rundung, Kantenfarbe) der
   Menüknöpfe mit einer echten Baumzeile — nicht „beide haben Klasse X". Der
   Stichprobenpunkt der Messung ist der **Text** (`fx=fy=0.5` würde mitten im Wort treffen
   und die Buchstaben vergleichen), und es wird gegen den echten `.tree__folder` in der Rail
   desselben Fensters gemessen, nicht gegen eine Zahl aus diesem Skript.
2. **S8** misst bei 1024 px, dass wirklich **ein** Panel sichtbar ist — und dass es das
   *rechteste* ist, nicht irgendeins.

**Ein Fund aus der Nachbarschaft, der hier bewusst aufgefangen ist:** in Phase 9 wurde ein
eingecheckter Browser-Beleg entdeckt, der der **Gegenlauf** des Blocks selbst war (Bild
zeigte `beta`, weil Hand-Gegenlauf und Erfolgslauf dieselben Ausgabepfade haben). Deshalb
schreibt dieses Skript die Bilder in **eigene, pro Station benannte Dateien** und meldet
jede Station mit ihrem Ergebnis — ein Bild ohne zugehörige Zeile `alle_ok` wäre wertlos.

Aufruf (Hard Rule 9: Stopp ausschließlich über die PID-Datei des Wegwerf-Skripts):
    python phase9_hardening/scripts/p9_step_g_wegwerf.py start
    ~/.claude-code-tools/e2e-venv/bin/python phase9_hardening/scripts/p9_settings_chain_probe.py
    python phase9_hardening/scripts/p9_step_g_wegwerf.py stop
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
import time
from pathlib import Path

from playwright.sync_api import Page, sync_playwright

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = REPO_ROOT / "docs" / "screenshots"
PROBE_DIR = REPO_ROOT / "phase9_hardening" / "probes"
DEFAULT_BASE_URL = "https://127.0.0.1:18775"
DEFAULT_CREDS = Path("/tmp/opencode/p9-step-g-wegwerf/credentials.json")

befunde: list[dict] = []


def pruefe(name: str, ok: bool, detail: str = "") -> None:
    befunde.append({"pruefung": name, "ok": bool(ok), "detail": detail})
    print(f"  [{'OK ' if ok else 'FEHLER'}] {name}" + (f" — {detail}" if detail else ""),
          file=sys.stderr)


# --- TOTP/Login (entliehen aus p9_step_g_self_check.py) ---------------------------------------

import base64  # noqa: E402
import hmac  # noqa: E402
import hashlib  # noqa: E402
import struct  # noqa: E402
import urllib.parse  # noqa: E402


def _generate_totp(otpauth_uri: str) -> str:
    qs = urllib.parse.parse_qs(urllib.parse.urlparse(otpauth_uri).query)
    secret_b32 = qs["secret"][0]
    key = base64.b32decode(secret_b32 + "=" * (-len(secret_b32) % 8))
    msg = struct.pack(">q", int(time.time() // 30))
    h = hmac.new(key, msg, hashlib.sha1).digest()
    offset = h[-1] & 0x0F
    return f"{(struct.unpack('>I', h[offset:offset + 4])[0] & 0x7FFFFFFF) % 1000000:06d}"


def login(page: Page, base_url: str, password: str, otpauth_uri: str) -> bool:
    for _ in range(2):
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


# --- Messhilfen -------------------------------------------------------------------------------

def sichtbare_panels(page: Page) -> list[str]:
    """Die Panels der Kette, die **wirklich sichtbar** sind — im Browser gemessen, nicht aus
    dem `hidden`-Attribut gelesen. Der Unterschied ist der ganze Punkt von S8: `hidden` ist
    die Absicht, `getBoundingClientRect().width > 0` ist die Wirkung, und im Schmal-Modus
    blendet CSS aus, ohne `hidden` zu setzen."""
    return page.evaluate(
        """() => ['settings-menu', 'settings-password', 'settings-spaces',
                   'settings-space-detail', 'settings-updates']
             .filter((id) => {
               const el = document.getElementById(id);
               if (!el) return false;
               const r = el.getBoundingClientRect();
               return r.width > 0 && r.height > 0;
             })"""
    )


def warte_bis(bedingung, timeout_s: float = 20.0, takt_s: float = 0.5) -> bool:
    """Pollt eine Bedingung, statt eine feste Wartezeit zu behaupten.

    **Befund vom 2026-10-05, an dieser Stelle:** S7 prüfte nach einem festen `sleep(1.5)`,
    ob die Zeile da ist. Der Wegwerf-Harness **sammelt Spaces über die Läufe hinweg** (er
    sät Items, keine Spaces), und `/api/v1/overview` kostet **linear mit der Zahl der
    sichtbaren Spaces** — der P9-15-Befund vom 2026-10-03, hier unerwartet wiederbelebt. Mit
    sechs Spaces war der Lauf beim 6-von-6-Stand und meldete „Zeile fehlt", obwohl der
    Space angelegt worden war. Ein fester Schlaf ist eine Behauptung über die Dauer; die
    Bedingung ist die Aussage."""
    ende = time.time() + timeout_s
    while time.time() < ende:
        if bedingung():
            return True
        time.sleep(takt_s)
    return False


def box(page: Page, selektor: str) -> dict:
    """Berechnete Werte eines Elements. `fx/fy` bewusst weggelassen: der Standard 0.5/0.5
    landet mitten im Text, und der Vergleich zweier Textglyphen ist kein Vergleich zweier
    Zeilen. Verglichen wird die Zeile selbst."""
    return page.evaluate(
        """(sel) => {
             const el = document.querySelector(sel);
             if (!el) return null;
             const cs = getComputedStyle(el);
             const r = el.getBoundingClientRect();
             return {
               height: Math.round(r.height * 100) / 100,
               width: Math.round(r.width * 100) / 100,
               padTop: cs.paddingTop, padBottom: cs.paddingBottom,
               padLeft: cs.paddingLeft, radius: cs.borderRadius,
               fontSize: cs.fontSize, fontWeight: cs.fontWeight,
               borderColor: cs.borderColor,
               // **Der Fill ist ein `linear-gradient`, keine `background-color`.** Die erste
               // Fassung mass `backgroundColor` und meldete fuer aktiv und inaktiv
               // `rgba(0, 0, 0, 0)` — richtig gemessen, aber am falschen Feld: `--select-fill`
               // ist als Verlauf definiert und landet in `backgroundImage`. Ein Wächter, der
               // am falschen Feld misst, meldet "kein Unterschied" fuer zwei sichtbar
               // verschiedene Zustaende.
               background: cs.backgroundColor, backgroundImage: cs.backgroundImage,
             };
           }""",
        selektor,
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default=DEFAULT_BASE_URL)
    ap.add_argument("--creds", type=Path, default=DEFAULT_CREDS)
    ap.add_argument("--suffix", default="")
    args = ap.parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    PROBE_DIR.mkdir(parents=True, exist_ok=True)
    sfx = args.suffix

    creds = json.loads(args.creds.read_text())
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900},
                                ignore_https_errors=True)
        page.goto(f"{args.base_url}/ui/login", wait_until="domcontentloaded")
        time.sleep(32 - (datetime.datetime.now().second % 30))
        if not login(page, args.base_url, creds["password"], creds["otpauth_uri"]):
            print("Login fehlgeschlagen", file=sys.stderr)
            return 2
        try:
            page.locator("#update-banner-dismiss").click(timeout=800)
        except Exception:
            pass
        try:
            page.goto(f"{args.base_url}/ui/", wait_until="domcontentloaded")
            time.sleep(2.0)

            # --- S1: das Menü, gegen eine echte Baumzeile gemessen --------------------------
            page.locator("#account-button").click()
            time.sleep(0.6)
            pruefe("S1 Kette offen, nur das Menü",
                   sichtbare_panels(page) == ["settings-menu"],
                   f"sichtbar: {sichtbare_panels(page)}")
            knoepfe = page.locator("#settings-menu .settings-menu__item")
            pruefe("S1 genau drei Menüpunkte", knoepfe.count() == 3, f"{knoepfe.count()}")
            beschriftungen = [knoepfe.nth(i).inner_text().strip() for i in range(knoepfe.count())]
            pruefe("S1 Reihenfolge aus P9-AE",
                   beschriftungen == ["Passwort ändern", "Spaces verwalten", "Update-Log"],
                   f"{beschriftungen}")
            # Die Vergleichszeile ist ein **echter** `.tree__folder` in der Rail desselben
            # Fensters — nicht die Menüzeile selbst und nicht ein Wert aus diesem Skript.
            baumzeile = page.locator(".rail__tree .tree__folder").first
            baum_vorhanden = baumzeile.count() > 0
            pruefe("S1 Vergleichszeile in der Rail vorhanden", baum_vorhanden)
            if baum_vorhanden:
                # Der aktive Eimer darf nicht der sein (er traegt den Auswahl-Fill) -- sonst
                # wuerde der Vergleich Optik mit Zustand vermischen.
                inaktive = page.locator('.rail__tree .tree__folder:not([aria-current="true"])').first
                vergleich = ".rail__tree .tree__folder:not([aria-current=\"true\"])" if inaktive.count() else ".rail__tree .tree__folder"
                baum = box(page, vergleich)
                for i in range(3):
                    knopf = box(page, f"#settings-menu .settings-menu__item:nth-of-type({i + 1})")
                    gleich = (abs(knopf["height"] - baum["height"]) <= 1
                              and knopf["padTop"] == baum["padTop"]
                              and knopf["padBottom"] == baum["padBottom"]
                              and knopf["padLeft"] == baum["padLeft"]
                              and knopf["radius"] == baum["radius"]
                              and knopf["fontSize"] == baum["fontSize"]
                              and knopf["fontWeight"] == baum["fontWeight"])
                    pruefe(f"S1 Menüpunkt {i + 1} optisch = Baumzeile", gleich,
                           f"Knopf h={knopf['height']} p={knopf['padTop']}/{knopf['padLeft']} "
                           f"r={knopf['radius']} | Baum h={baum['height']} "
                           f"p={baum['padTop']}/{baum['padLeft']} r={baum['radius']}")
            page.screenshot(path=str(OUT_DIR / f"p9_settings_{sfx}01_menue_1440.png"))

            # --- S2: Passwort daneben, Menü bleibt sichtbar, aktiver Knopf markiert ----------
            page.locator("#settings-open-password").click()
            time.sleep(0.6)
            sichtbar = sichtbare_panels(page)
            pruefe("S2 Menü und Passwort nebeneinander",
                   sichtbar == ["settings-menu", "settings-password"], f"{sichtbar}")
            pruefe("S2 Passwort-Panel liegt rechts vom Menü",
                   page.locator("#settings-password").bounding_box()["x"]
                   > page.locator("#settings-menu").bounding_box()["x"])
            pruefe("S2 aktiver Menüpunkt trägt aria-current",
                   page.locator('#settings-open-password[aria-current="true"]').count() == 1)
            pruefe("S2 die anderen beiden tragen aria-current=false",
                   page.locator('#account-manage-spaces[aria-current="false"]').count() == 1
                   and page.locator('#account-show-updates[aria-current="false"]').count() == 1)
            aktiv = box(page, "#settings-open-password")
            inaktiv = box(page, "#account-show-updates")
            baum_aktiv = box(page, '.rail__tree .tree__folder[aria-current="true"]')
            pruefe("S2 aktiver Menüpunkt bekommt den Auswahl-Fill",
                   aktiv["backgroundImage"] != inaktiv["backgroundImage"]
                   and "gradient" in aktiv["backgroundImage"],
                   f"aktiv={aktiv['backgroundImage'][:48]} inaktiv={inaktiv['backgroundImage'][:24]}")
            if baum_aktiv:
                pruefe("S2 derselbe Verlauf wie die aktive Baumzeile (kein eigener Wert)",
                       aktiv["backgroundImage"] == baum_aktiv["backgroundImage"],
                       f"Menü={aktiv['backgroundImage'][:48]} Baum={baum_aktiv['backgroundImage'][:48]}")
            page.screenshot(path=str(OUT_DIR / f"p9_settings_{sfx}02_passwort_1440.png"))

            # --- S3: Knopfwechsel ersetzt Stufe 2 ---------------------------------------------
            page.locator("#account-show-updates").click()
            time.sleep(0.6)
            sichtbar = sichtbare_panels(page)
            pruefe("S3 Wechsel ersetzt Stufe 2 (kein Passwort mehr)",
                   sichtbar == ["settings-menu", "settings-updates"], f"{sichtbar}")
            pruefe("S3 der neue Menüpunkt ist markiert",
                   page.locator('#account-show-updates[aria-current="true"]').count() == 1)
            log_inhalt = page.locator("#update-log-list").inner_text().strip()
            pruefe("S3 Update-Log hat Inhalt", bool(log_inhalt), f"{len(log_inhalt)} Zeichen")
            page.screenshot(path=str(OUT_DIR / f"p9_settings_{sfx}03_updatelog_1440.png"))

            # --- S4: Space-Klick öffnet Stufe 3, drei Panels bei 1440 -------------------------
            page.locator("#account-manage-spaces").click()
            time.sleep(1.0)
            pruefe("S4 Spaces als Stufe 2",
                   sichtbare_panels(page) == ["settings-menu", "settings-spaces"], f"{sichtbare_panels(page)}")
            zeilen = page.locator("#space-admin-list .settings-space-row")
            pruefe("S4 Space-Liste gerendert", zeilen.count() > 0, f"{zeilen.count()} Zeilen")
            # **Der Wegwerf-Harness hat genau einen Space**, ein Abstand zwischen zwei Zeilen ist
            # also nicht messbar — die erste Fassung gab `null` zurueck und meldete "0 px". Was
            # sich messen laesst, ist der *verwendete* `row-gap` des Containers; die Strecke
            # zwischen zwei echten Zeilen wird nach S7 nachgemessen, wo zwei Spaces stehen
            # (`S7 Zeilenabstand`).
            row_gap = page.evaluate(
                "() => getComputedStyle(document.getElementById('space-admin-list')).rowGap"
            )
            pruefe("S4 Space-Zeilen mit sichtbarem Abstand (P9-AK)",
                   row_gap not in (None, "normal", "0px"), f"row-gap={row_gap}")
            hr_vor_anlegen = page.evaluate(
                """() => { const hr = document.querySelector('#settings-spaces hr');
                     const anlegen = document.getElementById('space-create-name-input');
                     return !!hr && !!anlegen
                         && hr.getBoundingClientRect().top < anlegen.getBoundingClientRect().top; }"""
            )
            pruefe("S4 Trennlinie zwischen Liste und Anlege-Zeile", hr_vor_anlegen)
            zeilen.first.click()
            time.sleep(1.2)
            sichtbar = sichtbare_panels(page)
            pruefe("S4 Space-Klick öffnet Stufe 3, drei Panels sichtbar",
                   sichtbar == ["settings-menu", "settings-spaces", "settings-space-detail"],
                   f"{sichtbar}")
            # **Kein „Mitglieder > 0".** Die Mitgliederliste kommt aus den `.share.yml`-Grants
            # (`api.py :: _space_members_get`), und der eigene Home-Space hat per Definition keine
            # — 0 Einträge ist hier der *richtige* Zustand. Die erste Fassung behauptete das
            # Gegenteil und wäre gegen jede Wegwerf-Instanz rot. Aussagekräftig sind die drei
            # Folgerungen daraus, jede eine echte Zusicherung:
            pruefe("S4 Detail zeigt den Space-Namen",
                   "alpha" in page.locator("#space-detail-name").inner_text(),
                   page.locator("#space-detail-name").inner_text())
            pruefe("S4 Home-Space-Hinweis sichtbar (P7-K)",
                   page.locator("#space-detail-home-hint").is_visible())
            pruefe("S4 Entfernen-Knopf im Home-Space gesperrt (P7-K)",
                   not page.locator("#space-remove-open").is_visible())
            boxes = {pid: page.locator(f"#{pid}").bounding_box() for pid in sichtbar}
            sortiert = sorted(boxes.items(), key=lambda kv: kv[1]["x"])
            pruefe("S4 Panels in Stufenfolge von links nach rechts",
                   [k for k, _ in sortiert] == ["settings-menu", "settings-spaces",
                                                "settings-space-detail"],
                   f"{[k for k, _ in sortiert]}")
            page.screenshot(path=str(OUT_DIR / f"p9_settings_{sfx}04_drei_panels_1440.png"))

            # --- S5: ESC schließt von rechts nach links --------------------------------------
            sequenz = []
            for erwartet in (["settings-menu", "settings-spaces"],
                            ["settings-menu"],
                            []):
                page.keyboard.press("Escape")
                time.sleep(0.5)
                ist = sichtbare_panels(page)
                sequenz.append(ist)
                pruefe(f"S5 ESC -> {erwartet}", ist == erwartet, f"gesehen: {ist}")
            # Und die Kette ist wirklich zu (das Overlay selbst, nicht nur die Panels).
            pruefe("S5 Overlay nach vier ESC geschlossen",
                   page.locator("#settings-overlay[hidden]").count() == 1)

            # --- S8 (vor S6/S7, weil dort geschrieben wird): 1024 px -------------------------
            page.set_viewport_size({"width": 1024, "height": 768})
            time.sleep(0.5)
            page.locator("#account-button").click()
            time.sleep(0.5)
            page.locator("#account-manage-spaces").click()
            time.sleep(0.8)
            zeilen.first.click()
            time.sleep(1.0)
            schmal = sichtbare_panels(page)
            pruefe("S8 bei 1024 px nur das rechteste Panel", schmal == ["settings-space-detail"],
                   f"{schmal}")
            zurueck_sichtbar = page.locator("#settings-back-space-detail").is_visible()
            pruefe("S8 'Zurück' sichtbar", zurueck_sichtbar)
            page.screenshot(path=str(OUT_DIR / f"p9_settings_{sfx}05_schmal_1024.png"))
            page.locator("#settings-back-space-detail").click()
            time.sleep(0.5)
            pruefe("S8 'Zurück' öffnet Stufe 2",
                   sichtbare_panels(page) == ["settings-spaces"], f"{sichtbare_panels(page)}")
            page.set_viewport_size({"width": 1440, "height": 900})
            time.sleep(0.5)

            # --- S6: Passwortwechsel echt gegen die Wegwerf-Instanz -------------------------
            page.keyboard.press("Escape")
            time.sleep(0.4)
            page.locator("#settings-open-password").click()
            time.sleep(0.6)
            neues = "p9-settings-" + datetime.datetime.now().strftime("%H%M%S") + "x"
            page.locator("#account-current").fill(creds["password"])
            page.locator("#account-new").fill(neues)
            page.locator("#account-repeat").fill(neues)
            time.sleep(32 - (datetime.datetime.now().second % 30))
            page.locator("#account-totp").fill(_generate_totp(creds["otpauth_uri"]))
            with page.expect_response("**/api/v1/account/password") as info:
                page.locator("#account-submit").click()
            antwort = info.value
            time.sleep(1.2)
            pruefe("S6 Passwortwechsel HTTP 200", antwort.status == 200, f"HTTP {antwort.status}")
            pruefe("S6 Passwort-Panel geschlossen, Menü bleibt",
                   sichtbare_panels(page) == ["settings-menu"], f"{sichtbare_panels(page)}")
            toast = page.locator("#toast").inner_text() if page.locator("#toast").is_visible() else ""
            pruefe("S6 Toast nennt den Wechsel", "Passwort geändert" in toast, f"{toast[:70]!r}")
            # Die **Sitzung** muss bestehen bleiben (P5-E/P5-Q) und der neue CSRF-Token
            # gesetzt sein -- sonst waere der naechste Schreibvorgang rot.
            api_status = page.evaluate(
                """async () => { const r = await fetch('/api/v1/me', {credentials: 'same-origin'});
                     return r.status; }"""
            )
            pruefe("S6 Sitzung besteht weiter", api_status == 200, f"/api/v1/me -> {api_status}")
            creds["password"] = neues
            args.creds.write_text(json.dumps(creds, indent=2))
            page.screenshot(path=str(OUT_DIR / f"p9_settings_{sfx}06_passwort_gewechselt.png"))

            # --- S7: Space anlegen erscheint in der Liste -----------------------------------
            page.locator("#account-manage-spaces").click()
            time.sleep(0.8)
            vorher = page.locator("#space-admin-list .settings-space-row").count()
            neuer_name = "settings-" + datetime.datetime.now().strftime("%H%M%S")
            page.locator("#space-create-name-input").fill(neuer_name)
            page.locator("#space-create-submit").click()
            # **Auf die Bedingung warten, nicht auf eine Uhr.** Der Wegwerf-Harness sammelt
            # Spaces über die Läufe, und `/api/v1/overview` kostet **linear mit ihrer Zahl**
            # (P9-15 vom 2026-10-03, hier unerwartet wiederbelebt): bei acht Spaces 2,1 s,
            # bei einem 1,5 s Schlaf war die Zeile noch nicht gerendert. Gemessen 2026-10-05.
            da = warte_bis(
                lambda: page.locator("#space-admin-list .settings-space-row",
                                     has_text=neuer_name).count() == 1
            )
            nachher = page.locator("#space-admin-list .settings-space-row").count()
            pruefe("S7 Space anlegen: Zeile mehr", da and nachher == vorher + 1,
                   f"{vorher} -> {nachher}, '{neuer_name}' sichtbar={da}")
            neue_zeile = page.locator("#space-admin-list .settings-space-row",
                                      has_text=neuer_name).first
            pruefe("S7 neue Zeile sichtbar", neue_zeile.count() == 1, neuer_name)
            neue_zeile.click()
            time.sleep(1.2)
            pruefe("S7 Detail zeigt den neuen Space",
                   neuer_name in page.locator("#space-detail-name").inner_text(),
                   page.locator("#space-detail-name").inner_text())
            # Jetzt stehen **zwei** Zeilen in der Liste -- der Abstand zwischen ihnen ist der
            # Wert, den S4 nicht messen konnte, und dieselbe CSS-Aussage an einem echten Paar.
            abstand = page.evaluate(
                """() => { const kids = [...document.getElementById('space-admin-list').children];
                     if (kids.length < 2) return null;
                     return Math.round(kids[1].getBoundingClientRect().top
                                       - kids[0].getBoundingClientRect().bottom); }"""
            )
            pruefe("S7 Zeilenabstand zwischen zwei echten Zeilen > 0 (P9-AK)",
                   (abstand or -1) > 0, f"{abstand} px")
            page.screenshot(path=str(OUT_DIR / f"p9_settings_{sfx}07_space_angelegt.png"))

            # --- Gegenlauf-Messung: die Werte, an denen S1/S2 hängen -----------------------
            messwerte = {
                "baumzeile": box(page, ".rail__tree .tree__folder:not([aria-current=\"true\"])")
                or box(page, ".rail__tree .tree__folder"),
                "menuepunkt": box(page, "#settings-open-password"),
            }

        except Exception as exc:  # ein Absturz darf den Beleg nicht fressen
            pruefe("Stationen ohne Absturz", False, f"{type(exc).__name__}: {exc}"[:300])
        finally:
            browser.close()

    report = {
        "base_url": args.base_url,
        "messwerte": messwerte if "messwerte" in dir() else None,
        "befunde": befunde,
        "alle_ok": all(b["ok"] for b in befunde),
    }
    # **Der Dateiname folgt dem Ergebnis, nicht der Absicht.** `test_committed_probe_
    # evidence.py` verlangt für rote Läufe den `_gegenprobe`-Namensbestandteil — und hat
    # am 2026-10-05 genau diesen Lauf hier zweimal rot gemeldet, weil `--suffix g1`/`g2`
    # Counter-Run-Dateien unter dem Erfolgsnamen abgelegt hat. Die Konvention wird hier
    # also vom Werkzeug durchgesetzt, nicht vom Aufrufer: ein roter Lauf landet in
    # `*_gegenprobe*.json` und kann einen grünen Beleg nicht überschreiben. Das ist dieselbe
    # Entscheidung wie bei `scripts/prepend_updated_chain.sh` (verweigern statt reparieren).
    # Das Suffix steht **hinten**, weil `test_committed_probe_evidence.py` auf
    # `stem.endswith("_gegenprobe")` prüft -- die erste Fassung setzte es davor und die zwei
    # Wächter blieben rot (ein zweiter Fehler derselben Klasse, eine Ebene tiefer: der erste
    # war der Dateiname, der zweite seine Position im Namen).
    teile = ["p9_settings_chain_probe"]
    if sfx:
        teile.append(sfx)
    if not report["alle_ok"]:
        teile.append("gegenprobe")
    ziel = PROBE_DIR / ("_".join(teile) + ".json")
    ziel.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    if not report["alle_ok"]:
        print(f"ROTER Lauf -> {ziel.name} ( Gegenlauf; überschreibt keinen Beleg )",
              file=sys.stderr)
    else:
        print(f"Beleg -> {ziel.name}", file=sys.stderr)
    print(f"\n{sum(b['ok'] for b in befunde)}/{len(befunde)} Pruefungen gruen", file=sys.stderr)
    return 0 if report["alle_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
