#!/usr/bin/env python3
"""P9 Block „Kästchen enger" (Plan §12.1, Locks P9-BB/BC/BD/BE, Abnahme P9-116 – P9-119).

**Und warum auch dieses wieder ein eigenes Skript ist** (V187, hier zum zweiten Mal): der Lauf vom
2026-10-06 ist der Beleg für P9-BB *(b)* nicht, sondern die **widerrufene** Lesart — er maß
Menüpunkte von **35,69 px** Höhe und Space-Zeilen von **330 px** Breite. Ein umgebauter Lauf
würde beides zugleich behaupten. (`p9_settings_chain_probe.py` trägt zusätzlich den
Baumzeilen-Vergleich aus S1, der durch P9-BB seine Gültigkeit verliert — dort steht die
Umkehr mit beiden Lesarten im Docstring, gemessen wird hier.)

**Was hier gemessen wird — und warum nicht die Deklaration:**

1. **Flächen werden *berechnet* verglichen, nicht die Token gelesen** (unverändert aus §11).
2. **Textkanten mit einem `Range`**, nicht mit der Elementbox (unverändert).
3. **Der Vergleichspunkt für die Panelbreite ist ein geklonter Schatten** desselben Panels **ohne**
   die neue Klasse: dieselbe Technik wie bei den Flächen, aus demselben Grund — eine Breite, die
   man aus dem Stylesheet liest, ist die Absicht, nicht die Wirkung (P9-BE, S5/P9-118).
4. **Bild 07 rollt die neue Zeile auf** (`scrollIntoView`), weil das Panel scrollt: am 2026-10-06
   war die Zeile gemessen da und im Bild unsichtbar (1417 px Inhalt bei 834 px Höhe) — *„I
   honestly don't see that"*. **Die Station prüft die Sichtbarkeit im Panel-Rechteck**, nicht die
   Existenz der Zeile; das ist genau der Unterschied, der damals unterging.

Aufruf (Hard Rule 9: Stopp ausschließlich über die PID-Datei des Wegwerf-Skripts):
    python phase9_hardening/scripts/p9_step_g_wegwerf.py start
    ~/.claude-code-tools/e2e-venv/bin/python phase9_hardening/scripts/p9_settings_kastchen_probe.py
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


# --- Die Messmaschinen dieses Blocks -----------------------------------------------------------

# **Space-Zeilen: Kästchen gegen Beschriftung.** P9-BC verlangt, dass das Kästchen sein eigenes
# Label umklammert — das ist eine Aussage über **zwei** Kanten (rechts ist nichts mehr frei) und
# über **eine** Randbedingung (links bleibt die Beschriftung, wo P9-AX sie hingelegt hat).
# `leer` ist deshalb der Abstand von der Beschriftungskante bis zur Kästchenkante, und `padR`
# wird **mitgemessen** statt abgetippt: der Sollwert ist „Polster plus 1 px Rahmen", und beide
# Hälsen kommen aus dem laufenden Layout.
ZEILEN = r"""
() => {
  const r2 = (v) => Math.round(v * 100) / 100;
  const liste = document.getElementById('space-admin-list');
  const zeilen = [...liste.querySelectorAll('.settings-space-row')].map((z) => {
    const b = z.getBoundingClientRect();
    const w = document.createTreeWalker(z, NodeFilter.SHOW_TEXT);
    let n = null; while ((n = w.nextNode())) { if (n.nodeValue.trim()) break; }
    const rg = document.createRange(); rg.selectNodeContents(n);
    const tb = rg.getBoundingClientRect();
    const cs = getComputedStyle(z);
    return { box: r2(b.width), label: r2(tb.width), leer: r2(b.right - tb.right),
             text_l: r2(tb.left), padR: parseFloat(cs.paddingRight),
             alignSelf: cs.alignSelf, maxWidth: cs.maxWidth,
             txt: n.nodeValue.trim().slice(0, 24) };
  });
  return zeilen;
}
"""

# **Die Panelbreite gegen einen geklonten Schatten ohne die neue Klasse.** Eine Breite aus dem
# Stylesheet gelesen wäre die Absicht, nicht die Wirkung; geklot wird dasselbe Panel **ohne**
# `settings-panel--list`, hidden entfernt und aus dem Fluss genommen, damit es nichts verschiebt.
PANEL_SCHATTEN = r"""
() => {
  const p = document.getElementById('settings-spaces');
  const klon = p.cloneNode(true);
  klon.id = '__vergleichspanel__';
  klon.className = 'overlay__panel settings-panel';
  klon.removeAttribute('hidden');
  klon.style.position = 'absolute';
  klon.style.visibility = 'hidden';
  klon.style.left = '0'; klon.style.top = '0';
  document.body.appendChild(klon);
  const b = klon.getBoundingClientRect();
  const cs = getComputedStyle(klon);
  const r2 = (v) => Math.round(v * 100) / 100;
  const aus = { w: r2(b.width), inhalt: r2(b.width - parseFloat(cs.paddingLeft)
                    - parseFloat(cs.paddingRight) - parseFloat(cs.borderLeftWidth)
                    - parseFloat(cs.borderRightWidth)) };
  klon.remove();
  return aus;
}
"""

PANEL_IST = r"""
() => {
  const p = document.getElementById('settings-spaces');
  const b = p.getBoundingClientRect();
  const cs = getComputedStyle(p);
  const r2 = (v) => Math.round(v * 100) / 100;
  return { w: r2(b.width), l: r2(b.left),
           inhalt: r2(b.width - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight)
                         - parseFloat(cs.borderLeftWidth) - parseFloat(cs.borderRightWidth)),
           min_w: parseFloat(cs.minWidth), max_w: parseFloat(cs.maxWidth) };
}
"""

# **Sichtbarkeit im scrollenden Panel** — der Unterschied, der am 2026-10-06 unterging. Die Zeile
# existierte, war messbar vorhanden und stand **unterhalb** des Sichtbereichs.
#
# **Zwei Stufen, und die strenge zählt:** `sichtbar` heißt „das Rechteck überlappt den Panelbereich"
# (das genügte am 2026-10-06 und ist zu lax — ein halb sichtbares Kästchen zählt in einem Bild nicht
# als „zu sehen"), `sichtbar_voll` heißt „das ganze Kästchen liegt im Panel". Die Station prüft
# `sichtbar_voll`; beide Zahlen stehen im Detail, damit der Unterschied sichtbar bleibt.
SICHTBAR = r"""
(neuer_name) => {
  const r2 = (v) => Math.round(v * 100) / 100;
  const panel = document.getElementById('settings-spaces');
  const pb = panel.getBoundingClientRect();
  const zeile = [...document.querySelectorAll('#space-admin-list .settings-space-row')]
    .find((z) => z.textContent.includes(neuer_name));
  if (!zeile) return { gefunden: false };
  const zb = zeile.getBoundingClientRect();
  const oben = Math.max(zb.top, pb.top), unten = Math.min(zb.bottom, pb.bottom);
  return { gefunden: true, sichtbar: unten > oben,
           sichtbar_voll: zb.top >= pb.top - 0.5 && zb.bottom <= pb.bottom + 0.5,
           sichtbar_px: r2(Math.max(0, unten - oben)),
           zeile_t: r2(zb.top), zeile_b: r2(zb.bottom),
           panel_t: r2(pb.top), panel_b: r2(pb.bottom),
           scrollTop: r2(panel.scrollTop), scrollHeight: r2(panel.scrollHeight),
           clientHeight: r2(panel.clientHeight) };
}
"""


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

            # --- P9-116: die Punkte sind **flacher**, nicht schmaler. Gemessen vorher 35,69 px,
            #     alle drei gleich (Polster 6 px aus der Sammelregel), im Bild war **nichts**
            #     ausgewählt — es gab also keinen Zustand, der die Höhe erklärt.
            pad_oben, pad_unten = [], []
            for i in range(knoepfe.count()):
                cs = page.evaluate(
                    "(sel) => { const c = getComputedStyle(document.querySelector(sel));"
                    " return [c.paddingTop, c.paddingBottom]; }",
                    f"#settings-menu .settings-menu__item:nth-of-type({i + 1})")
                pad_oben.append(cs[0])
                pad_unten.append(cs[1])
            pruefe("S1/P9-116 alle drei Punkte tragen 4 px Polster oben/unten",
                   all(p == "4px" for p in pad_oben) and all(p == "4px" for p in pad_unten),
                   f"oben {pad_oben}, unten {pad_unten} (vorher 6px/6px)")
            hoehen = [round(b["height"], 2) for b in boxen]
            pruefe("S1/P9-116 die Höhe ist bei allen drei gleich und kleiner als 35,69 px",
                   len(set(hoehen)) == 1 and 31.0 < hoehen[0] < 32.5, f"{hoehen} px")
            # **Und die Breite ist unverändert** — P9-BA („Kästchen enger" bei den Menüpunkten)
            # ist am 2026-10-06 auf „nur bei Spaces verwalten" eingeschränkt worden. Ohne diese
            # Station könnte ein Revert still durchgehen und wieder 19 px Leerraum je Seite
            # entstehen lassen, ohne dass irgendetwas rot wird.
            breiten = [round(b["width"], 2) for b in boxen]
            pruefe("S1/P9-116 die Breite ist unverändert gestreckt (P9-BA eingeschränkt)",
                   len(set(breiten)) == 1 and breiten[0] >= 100,
                   f"{breiten} px (Beschriftungen 106/113/77 px — gleiche Fläche für alle drei)")
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

            # --- P9-117: die Zeile umklammert ihr **eigenes** Label. Gemessen vorher: Kästchen
            #     330 px, Beschriftungen 84–137 px, also 192–245 px Leerraum rechts.
            zeilen = page.evaluate(ZEILEN)
            zu_fett = [z for z in zeilen
                       if abs((z["box"] - z["label"]) - (z["padR"] + 2)) > 1]
            pruefe("S5/P9-117 jedes Kästchen ist Label + rechtes Polster + 2 px Rahmen",
                   zeilen and not zu_fett,
                   f"{len(zeilen)} Zeilen, breiteste {max((z['box'] for z in zeilen), default=0)} px "
                   f"(vorher 330 px für alle)"
                   + (f", zu fett: {[z['txt'] for z in zu_fett]}" if zu_fett else ""))
            leer_rechts = [z["leer"] for z in zeilen]
            pruefe("S5/P9-117 rechts ist nur noch das Polster frei",
                   zeilen and max(leer_rechts) <= zeilen[0]["padR"] + 2,
                   f"max {max(leer_rechts, default=0)} px bei Polster "
                   f"{zeilen[0]['padR'] if zeilen else '?'} px (vorher 192–245 px)")
            # Und die Beschriftung steht **unverändert** links (P9-AX) — sonst hätte das Kästchen
            # seinen Text mitverschoben, und genau das wollte er nicht.
            versatz2 = [round(z["text_l"] - titel_box["text"]["l"], 2) for z in zeilen]
            pruefe("S5/P9-117 die Beschriftung steht unverändert bündig mit dem Titel",
                   all(abs(v) <= 1 for v in versatz2), f"{sorted(set(versatz2))} px Versatz")

            # --- P9-118: **nur dieses** Fenster ist schmaler. Verglichen wird gegen einen
            #     geklonten Schatten ohne die neue Klasse (siehe `PANEL_SCHATTEN`).
            panel_ist = page.evaluate(PANEL_IST)
            panel_schatten = page.evaluate(PANEL_SCHATTEN)
            pruefe("S5/P9-118 das Spaces-Fenster ist schmaler als dasselbe Fenster ohne P9-BE",
                   panel_ist["w"] < panel_schatten["w"],
                   f"ist {panel_ist['w']} px, ohne die Klasse {panel_schatten['w']} px "
                   f"(Differenz {round(panel_schatten['w'] - panel_ist['w'], 2)} px)")
            pruefe("S5/P9-118 min und max stehen auf demselben Wert (eine Entscheidung, eine Stelle)",
                   panel_ist["min_w"] == panel_ist["max_w"],
                   f"min {panel_ist['min_w']}, max {panel_ist['max_w']}")
            pruefe("S5/P9-118 die Anlegezeile bleibt auf einer Zeile und der Knopf behält seine Größe",
                   abs(feld["t"] - anlegen["t"]) <= 1 and abs(anlegen["w"] - natuerlich) <= 1,
                   f"Feld {feld['w']} px (vorher 180 px), Knopf {anlegen['w']} px == Eigenbreite")
            # **Und der Anteil, nicht die Breite.** Die erste Fassung dieser Station verglich nur
            # „schmaler als der Schatten" — damit blieb der **eigene** Fehler dieses Blocks grün:
            # 288 px im `min-width` (border-box ⇒ 288 px **gesamt**, Inhalt 240 px, Feld 88 px =
            # 37 %) ist schmaler als 380 px und damit „erfüllt". Der Wächter muss also die
            # **Ableitung** prüfen, nicht die Richtung: das Anlegefeld behält mindestens 45 % des
            # Panelinhalts (gemessen 138 von 288 px = **48 %**).
            anteil = feld["w"] / panel_ist["inhalt"] if panel_ist["inhalt"] else 0
            pruefe("S5/P9-118 das Anlegefeld behält mindestens 45 % des Panelinhalts",
                   anteil >= 0.45,
                   f"Feld {feld['w']} px von {panel_ist['inhalt']} px Inhalt = "
                   f"{round(anteil * 100)} % (bei 288 px Inhalt waeren es 37 %)")
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

            # --- P9-114: Bild 04 muss die Hinzufügen-Optionen **zeigen können**, und das Kriterium
            #     muss sagen, wo. Gemessen wird deshalb nicht nur „sichtbar", sondern **wo**.
            #     **Und die erste Fassung dieser Station maß die falsche Kante**: sie nahm den
            #     Abstand vom Hinweistext zum *Knopf* und kam auf 64,8 px — das ist aber die
            #     **zweite Rasterzeile** von P9-AY (Name-Feld über Auswahl + „Hinzufügen"), der
            #     Abstand des Knopfes zum Feld beträgt 48,79 px. Gemessen wird deshalb die
            #     Aktions**zeile** (deren Oberkante direkt am Hinweis hängt) und *protokolliert*
            #     die Knopfkante für das Kriterium. Ein Bild, dessen Aussage an einer falschen
            #     Kante gemessen wird, ist derselbe Fehler wie ein Wächter am falschen Ort.
            mitglieder_bedienung = page.evaluate(
                """() => {
                  const r2 = (v) => Math.round(v * 100) / 100;
                  const p = document.getElementById('settings-space-detail');
                  const pb = p.getBoundingClientRect();
                  const zeile = document.querySelector(
                    '#settings-space-detail .overlay__actions:has(#space-member-name-input)');
                  const zb = zeile.getBoundingClientRect();
                  const knopf = document.getElementById('space-member-add-submit');
                  const kb = knopf.getBoundingClientRect();
                  const hinweis = document.getElementById('space-detail-home-hint');
                  const hb = hinweis.getBoundingClientRect();
                  const liste = document.getElementById('space-member-list');
                  const lb = liste.getBoundingClientRect();
                  return { hinweis_sichtbar: getComputedStyle(hinweis).display !== 'none',
                           zeile_t: r2(zb.top), abstand_hinweis: r2(zb.top - hb.bottom),
                           knopf_t: r2(kb.top), knopf_b: r2(kb.bottom),
                           abstand_zeile_knopf: r2(kb.top - zb.bottom),
                           mitglieder_hoehe: r2(lb.height),
                           panel_t: r2(pb.top), panel_b: r2(pb.bottom),
                           im_panel: zb.top >= pb.top && kb.bottom <= pb.bottom };
                }""")
            pruefe("S5/P9-114 die Bedienzeile steht im Panel, im Sichtbereich",
                   mitglieder_bedienung["im_panel"],
                   f"Aktionszeile y {mitglieder_bedienung['zeile_t']}, Panel y "
                   f"{mitglieder_bedienung['panel_t']}..{mitglieder_bedienung['panel_b']}")
            pruefe("S5/P9-114 sie steht **oben**, direkt unter dem Hinweistext",
                   mitglieder_bedienung["hinweis_sichtbar"]
                   and 0 <= mitglieder_bedienung["abstand_hinweis"] <= 24
                   and mitglieder_bedienung["mitglieder_hoehe"] == 0,
                   f"Aktionszeile {mitglieder_bedienung['abstand_hinweis']} px unter dem Hinweis, "
                   f"Mitgliederbereich {mitglieder_bedienung['mitglieder_hoehe']} px hoch; "
                   f"Knopf y {mitglieder_bedienung['knopf_t']}..{mitglieder_bedienung['knopf_b']} "
                   f"({mitglieder_bedienung['abstand_zeile_knopf']} px unter der Zeile — das ist "
                   "die zweite Rasterzeile aus P9-AY, kein Abstand zum Hinweis)")
            page.screenshot(path=str(OUT_DIR / f"p9_settings_{sfx}04_drei_panels_1440.png"))
            messwerte["P9-104_flaeche"] = {"menuepunkt": inaktiv, "standard": standard}
            messwerte["P9-105_auswahl"] = {"menuepunkt": aktiv, "hauptknopf": haupt}
            messwerte["P9-106_passwort"] = {"aendern": aendern, "vorsicht": vorsicht}
            messwerte["P9-107_versatz_speisezilen_px"] = versatz
            messwerte["P9-108_member_feld"] = {"name": name, "auswahl": auswahl, "hinzu": hinzu}
            messwerte["P9-109_anlegezeile"] = {"feld": feld, "knopf": anlegen,
                                               "innen_l": innen_l, "innen_r": innen_r,
                                               "knopf_eigenbreite": natuerlich}
            messwerte["P9-117_zeilen"] = zeilen
            messwerte["P9-118_panel"] = {"ist": panel_ist, "schatten": panel_schatten}
            messwerte["P9-114_mitglieder_bedienung"] = mitglieder_bedienung

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
            # --- P9-118, zweite Hälfte: die feste Breite ist **nur** für den breiten Modus. Ohne
            #     die Rücknahme im Schmal-Modus gewönne die Klassenregel gegen `flex: 1`, und das
            #     Panel stünde starr bei 338 px in einem 1024-px-Fenster. Zurück über den
            #     „Zurück"-Knopf, denn das Menü ist in diesem Zustand ausgeblendet (P9-AI).
            page.locator("#settings-back-space-detail").click()
            time.sleep(0.6)
            schmal_da = warte_bis(
                lambda: page.locator("#settings-spaces:not([hidden])").count() > 0, 20.0)
            panel_1024 = page.evaluate(PANEL_IST)
            pruefe("S6/P9-118 bei 1024 ist die feste Breite zurückgenommen (das Panel flext)",
                   schmal_da and panel_1024["w"] > 400,
                   f"{panel_1024['w']} px statt 338 px im breiten Modus (min/max "
                   f"{panel_1024['min_w']}/{panel_1024['max_w']})")
            messwerte["P9-118_bei_1024"] = panel_1024
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
            # **Der Name entscheidet die Position, und deshalb steht hier ein `zz-`.** Die Liste
            # kommt sortiert aus `api.py` (`store.list_spaces()`, B1/Nachbarregel), also landet
            # `zz-…` **als letzte Zeile** — und damit bei 29 Zeilen **unterhalb des Sichtbereichs**.
            # Das ist der Zustand, um den es bei P9-119 geht. Ohne das `zz-` hing die Position von
            # der Zahl der Spaces ab: beim ersten Lauf dieses Blocks landete die neue Zeile
            # zufällig **oben** (y 152), der Gegenlauf G17 blieb deshalb **grün**, und ein
            # grüner Gegenlauf ist ein Befund — die Station beweist die *Voraussetzung* nicht.
            neuer_name = "zz-" + datetime.datetime.now().strftime("%H%M%S")
            page.locator("#space-create-name-input").fill(neuer_name)
            page.locator("#space-create-submit").click()
            da = warte_bis(lambda: page.locator("#space-admin-list .settings-space-row",
                                               has_text=neuer_name).count() == 1)
            nachher = page.locator("#space-admin-list .settings-space-row").count()
            pruefe("S8 Space anlegen: eine Zeile mehr", da and nachher == vorher + 1,
                   f"{vorher} -> {nachher}")
            # **Und sie steht als LETZTE** — die Voraussetzung dafür, dass Bild 07 den Fall zeigt,
            # um den es geht (eine neu angelegte Zeile unterhalb des Sichtbereichs). Diese Station
            # steht **vor** dem Aufrollen und ist damit die Voraussetzung der nächsten: fiele sie
            # aus, wäre der Sichtbarkeitsnachweis von P9-119 wertlos (genau das war der Befund vom
            # 2026-10-06 — die Zeile war messbar da und im Bild unsichtbar).
            position = page.evaluate(
                """(name) => { const z = [...document.querySelectorAll(
                     '#space-admin-list .settings-space-row')];
                     const i = z.findIndex((e) => e.textContent.includes(name));
                     return { index: i, gesamt: z.length, letzte: i === z.length - 1 }; }""",
                neuer_name)
            pruefe("S8/P9-119 die neue Zeile steht als letzte in der Liste",
                   position["letzte"],
                   f"Position {position['index'] + 1} von {position['gesamt']}")
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

            # --- P9-119: Bild 07 muss die neue Zeile **zeigen**. *„I honestly don't see that"*
            #     war kein Bündigkeitsfehler, sondern ein Sichtbarkeitsfehler: das Panel scrollt,
            #     und ein neu angelegter Eintrag landet darunter. **Die Ausgangslage wird hier
            #     ausdrücklich hergestellt** — Liste nach oben (`scrollTop = 0`) —, weil sie sonst
            #     vom Zustand des Panels abhing: beim ersten Lauf stand es zufällig schon auf 503,
            #     und der Gegenlauf G17 blieb deshalb grün. Jetzt ist „Zeile ist nicht sichtbar"
            #     der **gemessene Ausgangszustand**, und der Gegenlauf beißt.
            page.evaluate(
                "() => { document.getElementById('settings-spaces').scrollTop = 0; }")
            time.sleep(0.3)
            vorher_sichtbar = page.evaluate(SICHTBAR, neuer_name)
            page.evaluate(
                """(name) => {
                     const panel = document.getElementById('settings-spaces');
                     const z = [...document.querySelectorAll('#space-admin-list .settings-space-row')]
                       .find((e) => e.textContent.includes(name));
                     // **Erst die neue Zeile** — das ist der Lock (P9-119).
                     if (z) z.scrollIntoView({ block: 'nearest', inline: 'nearest' });
                     // **Dann die Anlegezeile an den unteren Rand** — sie folgt unmittelbar auf
                     // die letzte Zeile und kommt so **mit** ins Bild. Grund: das Panel ist mit 34
                     // Spaces 1679 px hoch, die Anlegezeile stand dadurch in **keinem** Bild
                     // mehr, und ausgerechnet P9-AZ (Feld + „Space anlegen" auf einer Zeile) ist
                     // durch die Verschmalung (P9-BE) **interessanter** geworden: das Feld misst
                     // jetzt 138 px statt 180 px und der Platzhalter ist abgeschnitten. Ein Bild,
                     // das die Aussage nicht zeigt, ist der Kriteriumfehler vom 2026-10-06.
                     const anlegen = document.querySelector(
                       '#settings-spaces .overlay__actions:has(#space-create-name-input)');
                     if (anlegen) anlegen.scrollIntoView({ block: 'end', inline: 'nearest' });
                   }""",
                neuer_name)
            time.sleep(0.5)
            nachher_sichtbar = page.evaluate(SICHTBAR, neuer_name)
            anlege_zeile = page.evaluate(
                """() => { const r2 = (v) => Math.round(v * 100) / 100;
                     const p = document.getElementById('settings-spaces');
                     const pb = p.getBoundingClientRect();
                     const a = document.querySelector(
                       '#settings-spaces .overlay__actions:has(#space-create-name-input)');
                     const ab = a.getBoundingClientRect();
                     const f = document.getElementById('space-create-name-input').getBoundingClientRect();
                     const k = document.getElementById('space-create-submit').getBoundingClientRect();
                     return { t: r2(ab.top), b: r2(ab.bottom),
                              voll: ab.top >= pb.top - 0.5 && ab.bottom <= pb.bottom + 0.5,
                              feld: r2(f.width), knopf: r2(k.width),
                              eine_zeile: Math.abs(f.top - k.top) <= 1 }; }""")
            pruefe("S8/P9-119 die Anlegezeile ist mit im Bild (Feld und Knopf auf einer Zeile)",
                   anlege_zeile["voll"] and anlege_zeile["eine_zeile"],
                   f"y {anlege_zeile['t']}..{anlege_zeile['b']}, Feld {anlege_zeile['feld']} px, "
                   f"Knopf {anlege_zeile['knopf']} px")
            pruefe("S8/P9-119 der Ausgangszustand ist gemessen: die neue Zeile ist NICHT sichtbar",
                   vorher_sichtbar["gefunden"] and not vorher_sichtbar["sichtbar_voll"],
                   f"Zeile y {vorher_sichtbar.get('zeile_t')}..{vorher_sichtbar.get('zeile_b')} "
                   f"bei scrollTop {vorher_sichtbar.get('scrollTop')} "
                   f"({vorher_sichtbar.get('scrollHeight')} px Inhalt bei "
                   f"{vorher_sichtbar.get('clientHeight')} px Höhe)")
            pruefe("S8/P9-119 nach dem Aufrollen liegt die neue Zeile vollständig im Panel",
                   nachher_sichtbar["gefunden"] and nachher_sichtbar["sichtbar_voll"],
                   f"nachher {nachher_sichtbar.get('sichtbar_px')} px sichtbar bei scrollTop "
                   f"{nachher_sichtbar.get('scrollTop')} (Zeile y "
                   f"{nachher_sichtbar.get('zeile_t')}..{nachher_sichtbar.get('zeile_b')}, Panel y "
                   f"{nachher_sichtbar.get('panel_t')}..{nachher_sichtbar.get('panel_b')})")
            messwerte["P9-119_zeile07"] = {"vorher": vorher_sichtbar, "nachher": nachher_sichtbar}
            # **Was Bild 07 NICHT zeigt, steht hier, weil das Kriterium es sagen muss:** der Titel
            # und die Anlegezeile sind **nicht** im Bild (die Liste ist unten aufgerollt). Die
            # Bündigkeit mit dem Titel ist Bild 04 und 08 zu sehen — und genau das war der
            # Kriteriumfehler vom 2026-10-06, als *„I honestly don't see that"* zwei verschiedene
            # Aussagen in einem Bild verlangt hat.
            sicht_07 = page.evaluate(
                """() => { const r2 = (v) => Math.round(v * 100) / 100;
                     const t = document.querySelector('#settings-spaces h2').getBoundingClientRect();
                     const p = document.getElementById('settings-spaces').getBoundingClientRect();
                     return { titel_sichtbar: t.top >= p.top && t.bottom <= p.bottom,
                              titel_y: r2(t.top), panel_y: r2(p.top) }; }""")
            pruefe("S8/P9-119 Bild 07 zeigt die neue Zeile **und nicht** den Titel",
                   not sicht_07["titel_sichtbar"],
                   f"Titel y {sicht_07['titel_y']} bei Panel-Oberkante {sicht_07['panel_y']} — "
                   "die Bündigkeit mit dem Titel zeigen Bild 04 und 08")
            page.screenshot(path=str(OUT_DIR / f"p9_settings_{sfx}07_space_angelegt.png"))

            # ============================ 08: Rückmeldung =================================
            # **Bild 08 ist die Ansicht, aus der seine Worte kamen** (Bild 08 vom 2026-10-05
            # zeigte Menü + Spaces verwalten mit den 330-px-Kästchen). Deshalb steht hier
            # derselbe Zustand: Liste **oben**, damit Titel und Zeilen gemeinsam im Bild sind.
            #
            # **Das kostet zwei Schritte und ist nicht Kosmetik:** nach Bild 07 steht die Liste
            # unten (die neue Zeile ist aufgerollt), und ein einfaches ESC schließt dann das
            # *letzte* Panel — die Liste — und übrig bliebe nur das Menü (das war der Stand des
            # ersten Laufs dieses Blocks, ohne ESS-Beleg und ohne den geforderten Vergleich).
            # Also: erst eine Zeile anklicken (Detail öffnet), dann ESC (Detail schließt, die
            # Liste bleibt), dann `scrollTop = 0`.
            page.locator("#space-admin-list .settings-space-row").first.click()
            # **Auf die Bedingung warten, nicht auf die Uhr** — zum dritten Mal in diesem
            # Block, und hier hätte die Uhr das Gegenteil gemeldet: `selectSpace()` holt erst die
            # Items (`openSpaceDetail()` läuft **nach** dem API-Aufruf, damit das Panel nicht mit
            # leerem Inhalt aufblitzt), und das kostet bei 34 Spaces gut eine Sekunde. Mit einer
            # festen Pause war das Detail beim ESC **noch zu**, der ESC schloss stattdessen die
            # Liste, und die Station meldete `['settings-menu']`.
            detail_auf = warte_bis(
                lambda: page.locator("#settings-space-detail:not([hidden])").count() == 1, 20.0)
            page.keyboard.press("Escape")
            time.sleep(0.5)
            zurueck = sichtbare_panels(page)
            pruefe("S8 ESC schließt das Detail, die Liste bleibt offen",
                   detail_auf and "settings-space-detail" not in zurueck
                   and "settings-spaces" in zurueck,
                   f"Detail offen: {detail_auf}, sichtbar danach: {zurueck}")
            page.evaluate("() => { document.getElementById('settings-spaces').scrollTop = 0; }")
            time.sleep(0.4)
            page.screenshot(path=str(OUT_DIR / f"p9_settings_{sfx}08_rueckmeldung_1440.png"))

        except Exception as exc:  # ein Absturz darf den Beleg nicht fressen
            pruefe("Stationen ohne Absturz", False, f"{type(exc).__name__}: {exc}"[:300])
        finally:
            browser.close()

    report = {
        "base_url": args.base_url,
        "plan": "docs/concepts/phase9_hardening_block_settings_plan.md §12.1",
        "messwerte": messwerte or None,
        "befunde": befunde,
        "alle_ok": all(b["ok"] for b in befunde),
    }
    teile = ["p9_settings_kastchen_probe"]
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