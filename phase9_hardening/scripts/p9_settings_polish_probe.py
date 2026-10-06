#!/usr/bin/env python3
"""P9 Block „zweite Bildsichtung" (Plan §11, Locks P9-AU–P9-AZ, Abnahme P9-103 – P9-111).

**Warum ein eigenes Skript und kein Umbau von `p9_settings_chain_probe.py`:** V187 hat die
Regel formuliert — *ein umgebauter historischer Beleg beweist nichts mehr über den Block, für den
er steht*. Der §10-Lauf ist der Beleg für P9-AN (Eingabefeld-Fläche), und P9-AV hat diese Fläche
am selben Tag **widerrufen**. Ein umgebauter Lauf hätte also beides beweisen wollen.

**Was hier gemessen wird — und warum nicht die Deklaration:**

1. **Flächen werden *berechnet* verglichen, nicht die Token gelesen.** Die Abnahmezeile P9-104
   verlangt „un ausgewählter Menüpunkt: berechneter Hintergrund == der `.btn`-Regel". Ein
   *Vergleichspunkt* im selben Fenster wird deshalb **kurzzeitig eingefügt** (`.btn` bzw.
   `.btn-primary` bzw. `.btn.action--caution`) und danach wieder entfernt. Grund: die
   Vergleichsfläche muss **berechnet** sein — `#archive-button` (Vorsicht) und `#account-submit`
   (Vorsicht) sind nie gleichzeitig sichtbar, und eine Regel aus dem Quelltext zu lesen wäre die
   zweite Kopie der Aussage. Das ist dasselbe Muster wie in `test_settings_chain.py`.
2. **Textkanten mit einem `Range`, nicht mit der Elementbox.** P9-107 vergleicht *Beschriftungen*;
   `getBoundingClientRect()` des Elements misst die Box (bei den Space-Zeilen 33 px daneben).
3. **Bündigkeit wird an beiden Kanten geprüft.** „Bündig" heißt zwei Kanten; eine Prüfung, die nur
   die linke misst, wäre die Hälfte der Aussage.
4. **Die Bilder sind mit ihren Zeilen benannt** — dieselbe Regel wie im §10-Lauf (ein Bild ohne
   zugehörige Zeile `alle_ok` ist wertlos), und die Dateinamen folgen **dem Ergebnis**: ein roter
   Lauf bekommt `_gegenprobe` im Namen (Wächter `test_committed_probe_evidence.py`).

Aufruf (Hard Rule 9: Stopp ausschließlich über die PID-Datei des Wegwerf-Skripts):
    python phase9_hardening/scripts/p9_step_g_wegwerf.py start
    ~/.claude-code-tools/e2e-venv/bin/python phase9_hardening/scripts/p9_settings_polish_probe.py
    python phase9_hardening/scripts/p9_step_g_wegwerf.py stop
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
import time
from pathlib import Path

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


# --- TOTP/Login (entliehen, mit Vermerk) -------------------------------------------------------

import base64  # noqa: E402
import hashlib  # noqa: E402
import hmac  # noqa: E402
import struct  # noqa: E402
import urllib.parse  # noqa: E402


def _generate_totp(otpauth_uri: str) -> str:
    qs = urllib.parse.parse_qs(urllib.parse.urlparse(otpauth_uri).query)
    secret_b32 = qs["secret"][0]
    key = base64.b32decode(secret_b32 + "=" * (-len(secret_b32) % 8))
    msg = struct.pack(">q", int(time.time() // 30))
    digest = hmac.new(key, msg, hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    return f"{(struct.unpack('>I', digest[offset:offset + 4])[0] & 0x7FFFFFFF) % 1000000:06d}"


def login(page, base_url: str, password: str, otpauth_uri: str) -> bool:
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


def warte_bis(bedingung, timeout_s: float = 30.0, takt_s: float = 0.5) -> bool:
    """Auf die Bedingung warten, nicht auf eine Uhr — die Lehre aus S7/P9-15 (§10-Lauf)."""
    ende = time.time() + timeout_s
    while time.time() < ende:
        if bedingung():
            return True
        time.sleep(takt_s)
    return False


# --- Die zwei Messmaschinen ---------------------------------------------------------------------

# **Eine** Maschine für beide Fragen des Blocks. Sie liest Box **und** Textkante, und sie rechnet
# nichts selbst — sie gibt Rohwerte zurück, und der Vergleich bleibt im Python sichtbar.
MESS = r"""
(sel) => {
  const r2 = (v) => Math.round(v * 100) / 100;
  const el = typeof sel === 'string' ? document.querySelector(sel) : sel;
  if (!el) return null;
  const b = el.getBoundingClientRect();
  const w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
  let n = null; while ((n = w.nextNode())) { if (n.nodeValue.trim()) break; }
  let text = null;
  if (n) { const rg = document.createRange(); rg.selectNodeContents(n);
           const tb = rg.getBoundingClientRect();
           text = { l: r2(tb.left), r: r2(tb.right), mid: r2((tb.left + tb.right) / 2),
                    txt: n.nodeValue.trim().slice(0, 40) }; }
  const cs = getComputedStyle(el);
  return { l: r2(b.left), r: r2(b.right), w: r2(b.width), t: r2(b.top), h: r2(b.height),
           background: cs.backgroundColor, backgroundImage: cs.backgroundImage,
           borderColor: cs.borderColor, color: cs.color, boxShadow: cs.boxShadow,
           justify: cs.justifyContent, textAlign: cs.textAlign,
           padL: cs.paddingLeft, padR: cs.paddingRight, text };
}
"""

# Der **Vergleichspunkt**: ein Element mit derselben Klasse wird kurzzeitig in das offene Panel
# gehaengt, berechnet und wieder entfernt. Ohne das gaelte es nur den Quelltext zu lesen — und
# eine Deklaration ist die Absicht, nicht die Wirkung.
REFERENZ = r"""
(klassen) => {
  const alt = document.querySelector('#settings-menu');
  const h = document.createElement('button');
  h.className = klassen; h.id = '__vergleichspunkt__'; h.textContent = 'x';
  alt.appendChild(h);
  const cs = getComputedStyle(h);
  const aus = { background: cs.backgroundColor, backgroundImage: cs.backgroundImage,
                borderColor: cs.borderColor, color: cs.color, boxShadow: cs.boxShadow };
  h.remove();
  return aus;
}
"""


def ref(page, klassen: str) -> dict:
    return page.evaluate(REFERENZ, klassen)


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
    messwerte: dict = {}

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
            # **`loadOverview()` abwarten.** `renderSpaceList()` rendert aus `state.spaces`, und
            # das steht erst danach fest — sonst zeigt das Spaces-Panel nichts und S5/S6 messen
            # gegen eine leere Liste (der Produktbefund vom 2026-10-05, P10-Liste).
            uebersicht = warte_bis(lambda: page.locator(".rail .tree__space").count() > 0, 60.0)
            pruefe("Vorbereitung Übersicht geladen", uebersicht,
                   f"{page.locator('.rail .tree__space').count()} Spaces in der Rail")
            time.sleep(0.8)

            # ============================ 01: das Menü ======================================
            page.locator("#account-button").click()
            time.sleep(0.8)
            knoepfe = page.locator("#settings-menu .settings-menu__item")
            boxen = [knoepfe.nth(i).bounding_box() for i in range(knoepfe.count())]
            abstaende = [round(boxen[i + 1]["y"] - (boxen[i]["y"] + boxen[i]["height"]), 2)
                         for i in range(len(boxen) - 1)]
            pruefe("S1/P9-103 zwei Abstaende zwischen den drei Punkten",
                   len(abstaende) == 2 and all(a > 0 for a in abstaende), f"{abstaende} px")
            # **Derselbe Wert wie die Space-Liste** — nicht „gr��ßer als 0".
            listen_gap = page.evaluate(
                "() => getComputedStyle(document.getElementById('space-admin-list')).rowGap")
            pruefe("S1/P9-103 Abstand == der der Space-Zeilen",
                   all(abs(a - float(listen_gap.replace("px", ""))) <= 0.01 for a in abstaende),
                   f"Menü {abstaende} px, Liste {listen_gap}")

            # Flächen: berechnet, gegen einen **eingefügten** Vergleichspunkt derselben Klasse.
            inaktiv = page.evaluate(MESS, "#settings-open-password")
            standard = ref(page, "btn")
            pruefe("S2/P9-104 unausgewählter Menüpunkt == Standardknopf (Fläche)",
                   inaktiv["backgroundImage"] == standard["backgroundImage"]
                   and inaktiv["borderColor"] == standard["borderColor"],
                   f"{inaktiv['backgroundImage'][:44]!r} vs {standard['backgroundImage'][:44]!r}")
            pruefe("S2/P9-104 auch der Innenschatten ist derselbe",
                   inaktiv["boxShadow"] == standard["boxShadow"],
                   f"{inaktiv['boxShadow'][:44]!r}")

            # Beschriftung mittig (P9-99, unverändert) — der Textknoten, nicht die Box.
            mitte_text = page.evaluate(MESS, "#settings-open-password")["text"]["mid"]
            mitte_knopf = round(boxen[0]["x"] + boxen[0]["width"] / 2, 2)
            pruefe("S2/P9-99 Beschriftung weiterhin mittig", abs(mitte_text - mitte_knopf) <= 1,
                   f"Textmitte {mitte_text}, Knopfmitte {mitte_knopf}")

            # Titelabstand (P9-96, unverändert): 24 px.
            titel = page.locator("#settings-menu h2").bounding_box()
            pruefe("S1/P9-96 Titelabstand unverändert 24 px",
                   abs((boxen[0]["y"] - (titel["y"] + titel["height"])) - 24) <= 1,
                   f"{round(boxen[0]['y'] - (titel['y'] + titel['height']), 2)} px")
            page.screenshot(path=str(OUT_DIR / f"p9_settings_{sfx}01_menue_1440.png"))

            # ============================ 02: Passwort =====================================
            page.locator("#settings-open-password").click()
            time.sleep(0.8)
            aktiv = page.evaluate(MESS, "#settings-open-password")
            haupt = ref(page, "btn-primary")
            pruefe("S3/P9-105 ausgewählter Menüpunkt == Akzentfläche wie .btn-primary",
                   aktiv["backgroundImage"] == haupt["backgroundImage"],
                   f"{aktiv['backgroundImage'][:52]!r} vs {haupt['backgroundImage'][:52]!r}")
            pruefe("S3/P9-105 die Kante auch",
                   aktiv["borderColor"] == haupt["borderColor"],
                   f"{aktiv['borderColor']} vs {haupt['borderColor']}")

            aendern = page.evaluate(MESS, "#account-submit")
            vorsicht = ref(page, "btn action--caution")
            pruefe("S4/P9-106 der Knopf Ändern trägt die Vorsichtsfarbe",
                   aendern["color"] == vorsicht["color"],
                   f"{aendern['color']} vs {vorsicht['color']}")
            pruefe("S4/P9-106 und die Standardfläche, keine gefüllte rote",
                   aendern["backgroundImage"] == vorsicht["backgroundImage"],
                   f"{aendern['backgroundImage'][:44]!r}")
            panel_text = page.locator("#settings-password").inner_text()
            pruefe("S4/P9-106 Abbrechen ist weg, Schließen da",
                   "Abbrechen" not in panel_text and "Schließen" in panel_text,
                   f"{panel_text.splitlines()[0]!r} …")
            page.screenshot(path=str(OUT_DIR / f"p9_settings_{sfx}02_passwort_1440.png"))

            # ============================ 03: Update-Log ====================================
            page.locator("#account-show-updates").click()
            time.sleep(0.8)
            pruefe("S3/P9-105 genau ein Punkt trägt aria-current=true",
                   page.locator('#settings-menu [aria-current="true"]').count() == 1)
            page.screenshot(path=str(OUT_DIR / f"p9_settings_{sfx}03_updatelog_1440.png"))

            # ============================ 04: die Kette in voller Breite =====================
            page.locator("#account-manage-spaces").click()
            liste_da = warte_bis(
                lambda: page.locator("#space-admin-list .settings-space-row").count() > 0, 30.0)
            pruefe("S5 Spaces als Stufe 2", liste_da,
                   f"{page.locator('#space-admin-list .settings-space-row').count()} Zeilen")
            # **P9-107: Beschriftung gegen Titel, mit `Range`.** Die Elementbox liegt 0 px auf der
            # Inhaltskante — gemessen wird die *Beschriftung*, sonst wäre der Test grün und der
            # Versatz stünde weiter im Bild.
            titel_box = page.evaluate(MESS, "#settings-spaces h2")
            zeile = page.evaluate(MESS, "#space-admin-list .settings-space-row")
            versatz = round(zeile["text"]["l"] - titel_box["text"]["l"], 2)
            pruefe("S5/P9-107 Space-Zeilen-Beschriftung == Titel (links)",
                   abs(versatz) <= 1, f"{versatz} px Versatz")
            # **P9-AZ: eine Zeile, an beiden Kanten bündig.**
            feld = page.evaluate(MESS, "#space-create-name-input")
            anlegen = page.evaluate(MESS, "#space-create-submit")
            panel_cs = page.evaluate(
                """() => { const p = document.getElementById('settings-spaces');
                     const cs = getComputedStyle(p); const b = p.getBoundingClientRect();
                     return { l: b.left, r: b.right, padL: parseFloat(cs.paddingLeft),
                              padR: parseFloat(cs.paddingRight) }; }""")
            innen_l, innen_r = panel_cs["l"] + panel_cs["padL"], panel_cs["r"] - panel_cs["padR"]
            pruefe("S5/P9-109 Feld und Knopf auf einer Zeile", abs(feld["t"] - anlegen["t"]) <= 1,
                   f"Feld top {feld['t']}, Knopf top {anlegen['t']}")
            pruefe("S5/P9-109 Feld bündig links mit dem Panelinhalt",
                   abs(feld["l"] - innen_l) <= 1, f"Feld {feld['l']}, Inhalt {round(innen_l, 2)}")
            pruefe("S5/P9-109 Knopf bündig rechts mit dem Panelinhalt",
                   abs(anlegen["r"] - innen_r) <= 1, f"Knopf {anlegen['r']}, Inhalt {round(innen_r, 2)}")
            # **Die zweite Hälfte des Locks, und sie ist beim ersten Gegenlauf aufgefallen.**
            # Der Nikinger sagte wörtlich: *"Space anlegen in seiner Größe gleich zu lassen und
            # nur das Eingabefeld in seiner Größe zu ändern"* — die Stationen oben prüfen nur die
            # **Kanten**, und die Kanten kann ein **geschrumpfter** Knopf ebenfalls halten: ohne
            # `flex: 1` bekommt das Feld seine Eigenbreite (194,89 px statt 180), der Knopf
            # schrumpft auf 127,11 px, und die Paarbreite ist wieder exakt die Inhaltsbreite —
            # G11 blieb deshalb **grün**, ohne dass der Lock gebaut wäre.
            #
            # **Die Eigenbreite wird an einer Kopie desselben Knopfes gemessen**, die außerhalb
            # der Flex-Zeile hängt (`inline-block`, also Inhaltsbreite). Dieselbe Technik wie der
            # Vergleichspunkt bei den Flächen: nicht die Deklaration lesen, sondern die Wirkung
            # an einem zweiten Element derselben Art.
            natuerlich = page.evaluate(
                r"""() => {
                     const vorlage = document.getElementById('space-create-submit');
                     const klon = vorlage.cloneNode(true);
                     klon.id = '__eigenbreite__';
                     klon.style.position = 'absolute';
                     klon.style.visibility = 'hidden';
                     vorlage.closest('.settings-panel').appendChild(klon);
                     const b = klon.getBoundingClientRect();
                     klon.remove();
                     return Math.round(b.width * 100) / 100;
                   }""")
            pruefe("S5/P9-109 der Knopf Space anlegen behält seine eigene Größe",
                   abs(anlegen["w"] - natuerlich) <= 1,
                   f"in der Zeile {anlegen['w']} px, an einer Kopie außerhalb {natuerlich} px")
            page.locator("#space-admin-list .settings-space-row").first.click()
            detail_da = warte_bis(
                lambda: page.locator("#settings-space-detail:not([hidden])").count() > 0, 20.0)
            pruefe("S5 Detail offen", detail_da, f"sichtbar: {sichtbare_panels(page)}")
            # **P9-AY: beidseitig bündig mit der Zeile darunter.**
            name = page.evaluate(MESS, "#space-member-name-input")
            auswahl = page.evaluate(MESS, "#space-member-write-select")
            hinzu = page.evaluate(MESS, "#space-member-add-submit")
            pruefe("S5/P9-108 Namensfeld == Auswahl-Knopf (links)",
                   abs(name["l"] - auswahl["l"]) <= 1,
                   f"Feld {name['l']}, Auswahl {auswahl['l']} (Differenz "
                   f"{round(auswahl['l'] - name['l'], 2)} px)")
            pruefe("S5/P9-108 Namensfeld == Aktion rechts",
                   abs(name["r"] - hinzu["r"]) <= 1, f"Feld {name['r']}, Knopf {hinzu['r']}")
            pruefe("S5/P9-AY das Feld ist NICHT über die Panelbreite hinaus gewachsen",
                   name["w"] <= (innen_r - innen_l) + 1, f"{name['w']} px breit")
            # Titelabstand im Detail (P9-101/P9-AR, unverändert): derselbe Wert wie im Menü.
            d_titel = page.locator("#settings-space-detail h2").bounding_box()
            erster = page.evaluate(
                """() => { const p = document.getElementById('settings-space-detail');
                     const k = [...p.children].find((e) => !['H2'].includes(e.tagName)
                       && e.getBoundingClientRect().height > 0);
                     return k ? k.getBoundingClientRect().top : null; }""")
            pruefe("S5/P9-101 Detail-Titelabstand == Menü-Titelabstand",
                   erster is not None and abs((erster - (d_titel["y"] + d_titel["height"])) - 24) <= 1,
                   f"{round(erster - (d_titel['y'] + d_titel['height']), 2) if erster else None} px")
            page.screenshot(path=str(OUT_DIR / f"p9_settings_{sfx}04_drei_panels_1440.png"))
            messwerte["P9-104_flaeche"] = {"menuepunkt": inaktiv, "standard": standard}
            messwerte["P9-105_auswahl"] = {"menuepunkt": aktiv, "hauptknopf": haupt}
            messwerte["P9-106_passwort"] = {"aendern": aendern, "vorsicht": vorsicht}
            messwerte["P9-107_versatz_speisezilen_px"] = versatz
            messwerte["P9-108_member_feld"] = {"name": name, "auswahl": auswahl, "hinzu": hinzu}
            messwerte["P9-109_anlegezeile"] = {"feld": feld, "knopf": anlegen,
                                               "innen_l": innen_l, "innen_r": innen_r,
                                               "knopf_eigenbreite": natuerlich}

            # ============================ 05: Schmal-Modus 1024 ===========================
            page.set_viewport_size({"width": 1024, "height": 768})
            time.sleep(1.0)
            pruefe("S6/P9-AI genau ein Panel sichtbar",
                   sichtbare_panels(page) == ["settings-space-detail"],
                   f"{sichtbare_panels(page)}")
            name1024 = page.evaluate(MESS, "#space-member-name-input")
            auswahl1024 = page.evaluate(MESS, "#space-member-write-select")
            hinzu1024 = page.evaluate(MESS, "#space-member-add-submit")
            pruefe("S6/P9-108 auch bei 1024 beidseitig bündig",
                   abs(name1024["l"] - auswahl1024["l"]) <= 1
                   and abs(name1024["r"] - hinzu1024["r"]) <= 1,
                   f"links {round(auswahl1024['l'] - name1024['l'], 2)} px, "
                   f"rechts {round(name1024['r'] - hinzu1024['r'], 2)} px")
            messwerte["P9-108_bei_1024"] = {"name": name1024, "auswahl": auswahl1024,
                                             "hinzu": hinzu1024}
            page.screenshot(path=str(OUT_DIR / f"p9_settings_{sfx}05_schmal_1024.png"))
            page.set_viewport_size({"width": 1440, "height": 900})
            time.sleep(0.8)

            # ============================ 06/07: die zwei Handgriffe ======================
            page.keyboard.press("Escape")
            time.sleep(0.4)
            page.locator("#settings-open-password").click()
            time.sleep(0.6)
            neues = "p9-polish-" + datetime.datetime.now().strftime("%H%M%S")
            page.locator("#account-current").fill(creds["password"])
            page.locator("#account-new").fill(neues)
            page.locator("#account-repeat").fill(neues)
            time.sleep(32 - (datetime.datetime.now().second % 30))
            page.locator("#account-totp").fill(_generate_totp(creds["otpauth_uri"]))
            with page.expect_response("**/api/v1/account/password") as info:
                page.locator("#account-submit").click()
            antwort = info.value
            time.sleep(1.2)
            pruefe("S7 Passwortwechsel HTTP 200", antwort.status == 200, f"HTTP {antwort.status}")
            page.screenshot(path=str(OUT_DIR / f"p9_settings_{sfx}06_passwort_gewechselt.png"))
            if antwort.status == 200:
                creds["password"] = neues
                args.creds.write_text(json.dumps(creds, indent=2))

            page.locator("#account-manage-spaces").click()
            warte_bis(lambda: page.locator("#space-admin-list .settings-space-row").count() > 0, 30.0)
            vorher = page.locator("#space-admin-list .settings-space-row").count()
            neuer_name = "polish-" + datetime.datetime.now().strftime("%H%M%S")
            page.locator("#space-create-name-input").fill(neuer_name)
            page.locator("#space-create-submit").click()
            da = warte_bis(lambda: page.locator("#space-admin-list .settings-space-row",
                                               has_text=neuer_name).count() == 1)
            nachher = page.locator("#space-admin-list .settings-space-row").count()
            pruefe("S8 Space anlegen: eine Zeile mehr", da and nachher == vorher + 1,
                   f"{vorher} -> {nachher}")
            # **Und die neue Zeile steht bündig mit dem Titel** — P9-107 an einem *frischen*
            # Eintrag, nicht nur an den vorhandenen.
            neu_text = page.evaluate(
                """(name) => { const el = [...document.querySelectorAll(
                     '#space-admin-list .settings-space-row')].find((e) => e.textContent.includes(name));
                     if (!el) return null;
                     const w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
                     let n = null; while ((n = w.nextNode())) { if (n.nodeValue.trim()) break; }
                     const rg = document.createRange(); rg.selectNodeContents(n);
                     return rg.getBoundingClientRect().left; }""", neuer_name)
            titel_text = page.evaluate(MESS, "#settings-spaces h2")["text"]["l"]
            pruefe("S8/P9-107 auch die neue Zeile bündig",
                   neu_text is not None and abs(neu_text - titel_text) <= 1,
                   f"neu {neu_text if neu_text is None else round(neu_text, 2)}, "
                   f"Titel {titel_text}")
            page.locator("#space-admin-list .settings-space-row").first.click()
            time.sleep(1.0)
            page.screenshot(path=str(OUT_DIR / f"p9_settings_{sfx}07_space_angelegt.png"))

            # ============================ 08: Rückmeldung =================================
            page.keyboard.press("Escape")
            time.sleep(0.5)
            page.screenshot(path=str(OUT_DIR / f"p9_settings_{sfx}08_rueckmeldung_1440.png"))

        except Exception as exc:  # ein Absturz darf den Beleg nicht fressen
            pruefe("Stationen ohne Absturz", False, f"{type(exc).__name__}: {exc}"[:300])
        finally:
            browser.close()

    report = {
        "base_url": args.base_url,
        "plan": "docs/concepts/phase9_hardening_block_settings_plan.md §11",
        "messwerte": messwerte or None,
        "befunde": befunde,
        "alle_ok": all(b["ok"] for b in befunde),
    }
    teile = ["p9_settings_polish_probe"]
    if sfx:
        teile.append(sfx)
    if not report["alle_ok"]:
        teile.append("gegenprobe")
    ziel = PROBE_DIR / ("_".join(teile) + ".json")
    ziel.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    if not report["alle_ok"]:
        print(f"ROTER Lauf -> {ziel.name} ( Gegenlauf; ueberschreibt keinen Beleg )",
              file=sys.stderr)
    else:
        print(f"Beleg -> {ziel.name}", file=sys.stderr)
    print(f"\n{sum(b['ok'] for b in befunde)}/{len(befunde)} Pruefungen gruen", file=sys.stderr)
    return 0 if report["alle_ok"] else 1


def sichtbare_panels(page) -> list[str]:
    return page.evaluate(
        """() => ['settings-menu', 'settings-password', 'settings-spaces',
                   'settings-space-detail', 'settings-updates']
             .filter((id) => { const el = document.getElementById(id); if (!el) return false;
                               const r = el.getBoundingClientRect();
                               return r.width > 0 && r.height > 0; })"""
    )


if __name__ == "__main__":
    from playwright.sync_api import sync_playwright  # noqa: E402
    raise SystemExit(main())