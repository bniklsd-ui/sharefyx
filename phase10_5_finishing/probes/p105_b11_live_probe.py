#!/usr/bin/env python3
"""P10.5 Block 11, Schritt 11.4 — die Live-Darstellung an der Wegwerf-Instanz.

**Wegwerf (Plan §2.3):** Port **18811** (eigener Port), eigene Wurzel
`/tmp/opencode/sharefyx-wegwerf-p105-b11`, tmp-`DATA_ROOT`, tmp-`auth.sqlite3`, File-Keyring,
Umgebung ohne `SHAREFYX_*`/`SFX_*`, Stopp **nur** über die PID-Datei (Hard Rule 9).

**Was gemessen wird (Abnahme P10.5-51, ED-1):**

| # | Zelle | Erwartung |
|---|---|---|
| 1 | **Cursorposition nach Klick** | der Cursor landet **auf dem geklickten Zeichen** — nicht daneben |
| 2 | Formatierungszeichen | auf der Cursorzeile **sichtbar**, auf der anderen Zeile **unsichtbar** |
| 3 | Cursorzeile | **genau eine** Zeile trägt `sfx-active-line` |
| 4 | **Rohmodus** (ED-5) | der Schalter „Rohtext" zeigt **jedes** Zeichen |
| 5 | Notausgang | ohne CodeMirror (der Nachlader scheitert) bleibt die Textarea und **alles** funktioniert |

**Die erste Zelle ist das Kriterium des Plans (§Block 11, Schritt 11.4, `[VERIFY V211]`):**
„`display:none` gegen `font-size:0` — der Ausführer prüft beide, Kriterium ist die korrekte
Cursorposition nach Klick".

**Wie gemessen wird (und warum nicht anders).** Der Cursorindex kommt **nicht** aus CodeMirror —
sonst prüft die Probe CodeMirror gegen sich selbst. Er kommt aus dem **DOM**: der Textbaum der
Zeile wird durchlaufen, die **versteckten** Formatierungszeichen werden **mitgezählt** (sie stehen
im Textbaum, nur ohne Breite), und der Browser selbst liefert die Position des Zielbuchstabens
(`Range`-Rechteck). Beides sind unabhängige Größen, und ihr **Unterschied** ist der Befund.

**Drei Fehler des Messgeräts, alle gefunden und behoben (2026-10-24):**

1. **Die CSP blockierte die Messung.** Die erste Fassung schob die CSS-Variante per
   `document.createElement('style')` in den Kopf — das ist ein Inline-Style, und die UI-CSP
   (`style-src 'self'`, **ohne** `'unsafe-inline'`) lässt ihn nicht zu. Die Folge war schlimmer
   als ein Fehlschlag: die drei Varianten maßen **alle dasselbe** (die unveränderte `app.css`)
   und meldeten „gleich" — **grün, ohne etwas gemessen zu haben**. Jetzt wird die Variante über
   `page.route()` **same-origin** ausgeliefert (die CSS-Datei selbst wird geändert und als
   Antwort auf `/ui/static/app.css` geliefert) — das ist `style-src 'self'` erlaubt.
2. **Die Auslieferung war nicht belegt.** Auch die neue Fassung maß zunächst drei gleiche
   Werte. Grund: das Kennzeichen der ausgelieferten CSS kam als **Text** an (Escaping), also
   war die Route wirkungslos. Jetzt trägt jede ausgelieferte CSS eine **Kennung**
   (`--p105-variante`), und der Browser **liest sie zurück** — ohne diesen Beleg ist jede
   Varianten-Zahl wertlos.
3. **Das Flag-Protokoll war verdreht** (aus Block 10 übernommen und hier nicht wiederholt).

Aufruf: `.venv/bin/python phase10_5_finishing/probes/p105_b11_live_probe.py`
Ergebnis: `phase10_5_finishing/probes/p105_b11_live.json`
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import secrets
import shutil
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
WEGWERF_ROOT = Path("/tmp/opencode/sharefyx-wegwerf-p105-b11")
DATA_ROOT = WEGWERF_ROOT / "data"
AUTH_DB = WEGWERF_ROOT / "auth.sqlite3"
DEK_FILE = WEGWERF_ROOT / "auth-dek"
SERVE_PID = WEGWERF_ROOT / "serve.pid"
SERVE_LOG = WEGWERF_ROOT / "serve.log"
PORT = 18811
BASE = f"https://127.0.0.1:{PORT}"
TLS_KEY = WEGWERF_ROOT / "key.pem"
TLS_CERT = WEGWERF_ROOT / "cert.pem"
SPACE = "alpha"
RESULT = Path(__file__).with_name("p105_b11_live.json")

#: Der Text, an dem der Klick-Test misst: die Klickstelle muss **genau** hier landen.
KLICK_TEXT = "WortmitMarke"
#: Das Zielzeichen **innerhalb** des Wortes: das "M" aus "Marke". Das ist Absicht: es steht
#: **hinter** den `**`-Formatierungszeichen, deren Verbergung den Text verschieben würde —
#: dort zeigt sich ein Fehler der Zuordnung zuerst.
KLICK_ZEICHEN = "Marke"
#: Die Zeile, in der gemessen wird (die mit den `**`).
KLICK_ZEILE = "Ein Satz mit"


def log(text: str) -> None:
    print(text, file=sys.stderr, flush=True)


SERVE_TLS_LAUNCHER = '''"""Dieselbe App wie phase2_mcp/scripts/serve.py, plus TLS."""
import os, sys
sys.path.insert(0, os.environ["REPO_ROOT"])
import uvicorn
from phase2_mcp.scripts import serve

_orig_run = uvicorn.run


def _run(*args, **kwargs):
    kwargs["ssl_keyfile"] = os.environ["TLS_KEY"]
    kwargs["ssl_certfile"] = os.environ["TLS_CERT"]
    return _orig_run(*args, **kwargs)


uvicorn.run = _run
serve.main(["--allowed-host", "127.0.0.1"])
'''


#: Die **Browser-Seite** der Probe. Sie laeuft im e2e-venv (Playwright), nicht im Dev-venv.
#:
#: **Wichtig:** hier wird **kein** `\\n` in einen JS-String geschrieben — der Text kommt aus der
#: Datei, die der Server liefert. (In der ersten Fassung stand ein `setValue` mit Newlines hier,
#: und die Escapes des doppelten Quoting haben das Browser-Skript in einen Syntaxfehler und
#: damit in einen leeren Befund geschickt.)
BROWSER_SKILL = '''import json, sys, time, hmac, hashlib, struct, base64, re
from pathlib import Path

base, space, password, secret, workdir, wort, zeichen, zeile = sys.argv[1:9]
work = Path(workdir)

#: Die **drei Klickstellen** — alle **im Wort**, denn das Wort steht direkt **nach** dem
#: versteckten `**`: dort ist die Zuordnung am feinsten (ein Versatz um die Zahl der
#: verdeckten Zeichen schlaegt sofort auf). Von links nach rechts: das erste Zeichen
#: (Index 0 des Wortes), eines in der Mitte und das letzte.
ZIELE = ["W", "t", "e"]

#: Die **drei Verbergungs-Arten** (Plan §Block 11, Schritt 11.4, `[VERIFY V211]`).
#: Jede Art besteht aus **zwei** Regeln: die eine blendet die Formatierungszeichen
#: **auf allen Zeilen** aus, die andere macht sie auf der **Cursorzeile** wieder sichtbar.
#:
#: - `visibility:hidden` laesst den Marker **seinen Platz behalten** -- die Zeile springt nicht.
#: - `display:none` und `font-size:0` **nehmen dem Marker den Platz** -- die Zeile rueckt
#:   zusammen, sobald der Cursor hineinwechselt (Obsidian-artig).
#:
#: Die **Anker** sind die beiden Regeln, die `app.css` heute traegt. Sie werden per Regex
#: gesucht, nicht woertlich -- sonst muesste die Probe an jede Aenderung der CSS-Datei
#: angepasst werden.
VARIANTEN = {
    "visibility": (
        ".CodeMirror .cm-formatting { visibility: hidden; }",
        ".CodeMirror .sfx-active-line .cm-formatting { visibility: visible; }",
    ),
    "display": (
        ".CodeMirror .cm-formatting { display: none; }",
        ".CodeMirror .sfx-active-line .cm-formatting { display: inline; }",
    ),
    "fontsize": (
        ".CodeMirror .cm-formatting { font-size: 0; }",
        ".CodeMirror .sfx-active-line .cm-formatting { font-size: 1em; }",
    ),
}

#: Die **aktive** Variante. Sie wird von `css_route` **beim Ausliefern** gelesen -- der
#: Browser laedt die Seite nach jedem Wechsel neu, deshalb passt der Wert immer.
AKTIVE_VARIANTE = "visibility"


def totp_now(secret_b32):
    key = base64.b32decode(secret_b32 + "=" * (-len(secret_b32) % 8))
    counter = int(time.time() // 30)
    digest = hmac.new(key, struct.pack(">q", counter), hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    code = (struct.unpack(">I", digest[offset:offset + 4])[0] & 0x7FFFFFFF) % 1000000
    return f"{code:06d}"


from playwright.sync_api import sync_playwright

#: Das **DOM-Skript**: findet das Zielzeichen, misst seine Rechtecke und rechnet den
#: Zeichenindex **im Dokument** -- unabhaengig von CodeMirror.
ZIEL_SKRIPT = """(args) => {
  const wort = args.wort, zeichen = args.zeichen, zeile = args.zeile;
  const ziele = args.ziele;
  const linien = Array.from(document.querySelectorAll('.CodeMirror-line'));
  const nummer = linien.findIndex(function (z) { return z.textContent.indexOf(zeile) >= 0; });
  const linie = linien[nummer];
  if (!linie) return null;
  const lauf = document.createTreeWalker(linie, NodeFilter.SHOW_TEXT);
  let knoten = null, versatz = -1;
  let n;
  while ((n = lauf.nextNode())) {
    const i = n.nodeValue.indexOf(wort);
    if (i >= 0) { knoten = n; versatz = i; break; }
  }
  if (!knoten) return null;
  // Der Zeichenindex **im Zeilentext**: alle Textknoten der Zeile, auch die der
  // versteckten Formatierungszeichen (sie stehen im Textbaum, nur ohne Breite).
  let anfang = 0;
  const zaehler = document.createTreeWalker(linie, NodeFilter.SHOW_TEXT);
  let m;
  while ((m = zaehler.nextNode())) {
    if (m === knoten) { anfang += versatz; break; }
    anfang += m.nodeValue.length;
  }
  // Die **Ziele**: je ein Zeichen an drei Stellen der Zeile.
  const zeilen_index = anfang;
  const messungen = [];
  for (const z of ziele) {
    const ziel = versatz + wort.indexOf(z);
    const bereich = document.createRange();
    bereich.setStart(knoten, ziel);
    bereich.setEnd(knoten, ziel + 1);
    const rechteck = bereich.getBoundingClientRect();
    // Die **linke Kante**: CM5 setzt den Cursor **vor** das Zeichen (es rundet auf die
    // naechste Zeichengrenze), der Cursor ist ein 2-px-Balken links davon.
    const kante = document.createRange();
    kante.setStart(knoten, ziel);
    kante.setEnd(knoten, ziel);
    const kanten_rechteck = kante.getBoundingClientRect();
    messungen.push({
      zeichen: z,
      index: anfang + (ziel - versatz),
      x: rechteck.left + rechteck.width / 2,
      kante_x: kanten_rechteck.left,
      y: rechteck.top + rechteck.height / 2,
    });
  }
  const erstes = messungen[0];
  // Der **Dokument-Index**: die Zeilen davor, jede mit ihrem Zeilenumbruch.
  let dokument = 0;
  for (let i = 0; i < nummer; i++) dokument += linien[i].textContent.length + 1;
  return {
    index: zeilen_index,
    dokument_index: dokument + zeilen_index,
    linien_nummer: nummer,
    messungen: messungen,
    x: erstes.x,
    kante_x: erstes.kante_x,
    y: erstes.y,
    text: linie.textContent,
  };
}"""


def messung_klick(page):
    """Ein Klick auf das Zielzeichen -- und danach **drei** unabhaengige Groessen:

    * **Zeilenindex** -- der Cursorindex aus CodeMirror gegen den Index, den das **DOM**
      ergibt (die Formatierungszeichen mitgezaehlt, sie stehen im Textbaum).
    * **Bildschirmposition** -- wo der Cursor **sichtbar** steht, gegen die linke Kante
      des geklickten Zeichens **nach** dem Neuzeichnen. Das ist der Unterschied zwischen
      den Verbergungs-Arten: bei `display:none` und `font-size:0` ruecken die Marker
      zusammen, und die Zeile **springt**, sobald der Cursor hineinwechselt.
    * **Das getippte Zeichen** -- landet es an der geklickten Stelle?

    **Drei Klickstellen**, weil die Empfindlichkeit verschieden ist: direkt **nach**
    einem versteckten Marker (`**`) ist die Zuordnung am feinsten -- dort schlaegt ein
    Versatz um die Zahl der verdeckten Zeichen sofort auf.
    """
    ziel = page.evaluate(ZIEL_SKRIPT, {"wort": wort, "zeichen": zeichen, "zeile": zeile,
                                       "ziele": ZIELE})
    if not ziel:
        return {"fehler": "Zielzeichen nicht gefunden"}
    # Der **Wert vor** dem Tippen: er enthaelt die Zeile als Teilstring. Der
    # Dokument-Index wird daraus gebildet -- nicht aus der Summe der DOM-Zeilenlaengen
    # (die zaehlen die **versteckten** Formatierungszeichen mit und wichen dadurch vom
    # Dokument ab; gemessen am 2026-10-24: zwei Zeichen daneben).
    wert_vorher = page.evaluate("""() => {
      const w = document.querySelector('.CodeMirror');
      return w && w.CodeMirror ? w.CodeMirror.getValue() : null;
    }""")
    zeilen_text = ziel["text"]
    fund = (wert_vorher or "").find(zeilen_text)

    stellen = []
    for stelle in ziel["messungen"]:
        document_index = fund + stelle["index"] if fund >= 0 else None
        page.mouse.click(stelle["x"], stelle["y"])
        page.wait_for_timeout(350)
        cursor = page.evaluate("""() => {
          const w = document.querySelector('.CodeMirror');
          if (!w || !w.CodeMirror) return null;
          const c = w.CodeMirror.getCursor();
          return { line: c.line, ch: c.ch };
        }""")
        cursor_x = page.evaluate("""() => {
          const alle = Array.from(document.querySelectorAll('.CodeMirror-cursor'));
          const sichtbar = alle.find(function (c) { return c.offsetParent !== null; });
          if (!sichtbar) return null;
          return sichtbar.getBoundingClientRect().left;
        }""")
        # **Nach** dem Klick: wo steht das geklickte Zeichen jetzt? (Bei `display:none`
        # rutscht die Zeile zusammen, sobald der Cursor hineinwechselt.)
        nachher = page.evaluate(ZIEL_SKRIPT, {"wort": wort, "zeichen": zeichen,
                                              "zeile": zeile, "ziele": ZIELE})
        # Die **passende** Stelle -- nicht die erste (die ist eine andere).
        nachher_stelle = None
        if nachher:
            for s in nachher["messungen"]:
                if s["zeichen"] == stelle["zeichen"]:
                    nachher_stelle = s
                    break
        page.keyboard.type("X")
        page.wait_for_timeout(350)
        wert = page.evaluate("""() => {
          const w = document.querySelector('.CodeMirror');
          return w && w.CodeMirror ? w.CodeMirror.getValue() : null;
        }""")
        # Das X **zuruecknehmen** -- die naechste Stelle soll auf demselben Text
        # gemessen werden, sonst wandert der Text mit.
        page.keyboard.press("Backspace")
        page.wait_for_timeout(250)
        zeichen_x = (nachher_stelle or {}).get("kante_x")
        stellen.append({
            "zeichen": stelle["zeichen"],
            "erwarteter_index": stelle["index"],
            "erwarteter_dokument_index": document_index,
            "cursor": cursor,
            "cursor_x": cursor_x,
            "zeichen_x": zeichen_x,
            "sprung": (cursor_x - stelle["kante_x"]) if cursor_x is not None else None,
            "cursor_auf_dem_zeichen": (cursor or {}).get("ch") == stelle["index"],
            "cursor_bleibt_stehen": (
                cursor_x is not None and zeichen_x is not None
                and abs(cursor_x - zeichen_x) <= 3
            ),
            "x_ist_das_zeichen": (
                document_index is not None and (wert or "")[document_index] == "X"
            ),
        })

    return {
        "variante_ausgeliefert": page.evaluate(
            "() => getComputedStyle(document.documentElement)"
            ".getPropertyValue('--p105-variante').trim().replace(/'/g, '')"
        ),
        "erwarteter_index": ziel["index"],
        "zeile_im_wert_gefunden": fund >= 0,
        "cursor": stellen[0]["cursor"] if stellen else None,
        "cursor_x": stellen[0]["cursor_x"] if stellen else None,
        "zeichen_x": stellen[0]["zeichen_x"] if stellen else None,
        "kante_vorher": ziel["kante_x"],
        "sprung": stellen[0]["sprung"] if stellen else None,
        "wert": wert_vorher,
        "x_ist_das_zeichen": all(s["x_ist_das_zeichen"] for s in stellen),
        "cursor_auf_dem_zeichen": all(s["cursor_auf_dem_zeichen"] for s in stellen),
        "cursor_bleibt_stehen": all(s["cursor_bleibt_stehen"] for s in stellen),
        "stellen": stellen,
        "geklickter_text": zeilen_text,
    }


def formatierung_messen(page):
    """Die Formatierungszeichen je Zeile -- **zwei** Groessen, nicht eine.

    `visibility: hidden` laesst das Element **platzhaltend** (Breite > 0) und unsichtbar;
    `display: none` laesst `visibility` **unveraendert "visible"** und die Breite **null**.
    Nur die **Geometrie** trennt die drei Arten:

    * `sichtbar` = visibility "visible" UND Breite > 0
    * `platz`    = Breite > 0 (beansprucht der Marker Platz?)
    """
    return page.evaluate("""() => {
      const zeilen = Array.from(document.querySelectorAll('.CodeMirror-line'));
      const aktive = document.querySelector('.CodeMirror .sfx-active-line');
      return zeilen.map(function (z) {
        const sichtbar = Array.from(z.querySelectorAll('.cm-formatting')).map(function (f) {
          const r = f.getBoundingClientRect();
          return {
            sichtbar: getComputedStyle(f).visibility === "visible" && r.width > 0,
            platz: r.width > 0,
            breite: r.width,
          };
        });
        const istCursorzeile = !!aktive && aktive.contains(z);
        return { istCursorzeile: istCursorzeile, formatierung: sichtbar };
      });
    }""")


def css_route(route):
    """Liefert `app.css` mit der gewaehlten **Verbergungs-Art** -- same-origin, also
    CSP-konform (`style-src 'self'`). Der Wegwerf-Server liefert die Originaldatei."""
    try:
        antwort = route.fetch()
        text = antwort.text()
    except Exception:
        route.continue_()
        return
    basis, aktiv = VARIANTEN[AKTIVE_VARIANTE]
    # **Deklarations**spezifisch, nicht selektorspezifisch: `.CodeMirror .cm-formatting`
    # kommt in `app.css` **zweimal** (die Farb-Regel und die Verbergungs-Regel). Der
    # erste Treffer war die Farb-Regel -- die Verbergung blieb unberuehrt, und alle drei
    # Varianten massen dasselbe (gemessen am 2026-10-24).
    text, n_basis = re.subn(
        r"\\.CodeMirror \\.cm-formatting \\{[^}]*visibility: hidden[^}]*\\}", basis, text, count=1
    )
    text, n_aktiv = re.subn(
        r"\\.CodeMirror \\.sfx-active-line \\.cm-formatting \\{[^}]*visibility: visible[^}]*\\}",
        aktiv, text, count=1
    )
    if n_basis != 1 or n_aktiv != 1:
        route.fulfill(status=500, body="Anker fehlt: " + str(n_basis) + "/" + str(n_aktiv))
        return
    # Die **Kennung**: ohne sie ist die Probe blind. Der Browser liest sie zurueck --
    # so ist belegt, dass die Variante **wirklich** ausgeliefert wurde.
    text = text + " :root{--p105-variante:'" + AKTIVE_VARIANTE + "'}"
    route.fulfill(response=antwort, body=text)


out = {}
with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(ignore_https_errors=True, viewport={"width": 1400, "height": 900})
    page = context.new_page()
    fehler = []
    page.on("pageerror", lambda exc: fehler.append(str(exc)))

    # -- Anmeldung ---------------------------------------------------------------
    page.goto(base + "/ui/login", wait_until="domcontentloaded")
    page.fill('input[name="space"]', space)
    page.fill('input[name="password"]', password)
    page.fill('input[name="totp"]', totp_now(secret))
    page.click('form[action="/ui/login"] button[type="submit"]')
    page.wait_for_selector("#shell", timeout=30000)

    def entwurf_loeschen():
        # Der Entwurf liegt im **sessionStorage** (editor.js, Entwurfsschutz). Nach dem
        # Neuladen fragt der Dialog "Ungespeicherter Entwurf?" -- und der Dialog liegt
        # **ueber** dem Schalter und blockiert jeden weiteren Klick. Fuer die Messung der
        # Darstellung ist der Entwurf irrelevant, also wird er hier geloescht.
        try:
            page.evaluate("() => { window.sessionStorage.clear(); }")
        except Exception:
            pass

    def item_oeffnen():
        page.wait_for_timeout(1200)
        page.wait_for_selector(".overview__space-open", timeout=20000)
        page.locator(".overview__space-open").first.click()
        page.wait_for_timeout(1200)
        page.locator(".list__row", has_text="Mess-Item").first.click()
        page.wait_for_timeout(1500)
        try:
            page.wait_for_selector(".CodeMirror", timeout=30000)
            return True
        except Exception:
            return False

    def editor_schliessen():
        """Den Editor schliessen (der **X**-Knopf) -- der Weg, den ein Mensch geht.

        Der Editor verdeckt die Liste (`.shell[data-view="detail"] .list { display: none; }`),
        und `clearDetail()` setzt `cm` **nicht** auf null: der Editor bleibt fuer das
        naechste Item geladen. Genau deshalb greift beim **Itemwechsel** der Pfad
        `setBody` -> `cm.setValue` -- und genau da verliert der Cursorzeile ihre Markierung.
        """
        knopf = page.locator("#close-button")
        if knopf.count() and knopf.first.is_visible():
            knopf.first.click()
            page.wait_for_timeout(900)
        page.wait_for_selector(".list__row", state="visible", timeout=15000)

    def item_klicken(titel):
        zeile = page.locator(".list__row", has_text=titel).first
        zeile.scroll_into_view_if_needed()
        zeile.click()
        page.wait_for_timeout(1600)

    # -- Zelle 1: die Cursorposition -- **je Verbergungs-Art** ------------------------
    # Jede Art braucht eine **eigene Seite**: die CSS wird beim Laden ausgeliefert.
    out["varianten"] = {}
    for name in ["visibility", "display", "fontsize"]:
        AKTIVE_VARIANTE = name
        page.unroute("**/ui/static/app.css")
        page.route("**/ui/static/app.css", css_route)
        entwurf_loeschen()
        page.reload(wait_until="domcontentloaded")
        page.wait_for_selector("#shell", timeout=30000)
        if not item_oeffnen():
            out["varianten"][name] = {"fehler": "Editor kam nach dem Neuladen nicht"}
            continue
        out["live_editor_da"] = True
        # Der Marker **sofort** nach dem Oeffnen -- **ohne** dass der Cursor gewandert
        # ist. Das ist die Regression des `setValue`-Fixes in `editor.js`: `setValue`
        # ersetzt das ganze Dokument und nimmt die Zeilenklassen mit, und CM5 feuert
        # dabei **kein** `cursorActivity`. Gemessen am 2026-10-24: die Cursorzeile war
        # nach dem Laden **nicht** markiert.
        ergebnis = messung_klick(page)
        ergebnis["cursorzeilen_beim_oeffnen"] = page.evaluate("""() => {
          return document.querySelectorAll('.CodeMirror .sfx-active-line').length;
        }""")
        # Der **Wechsel** auf ein zweites Item: `clearDetail()` setzt `cm` **nicht** auf
        # null, der Editor bleibt geladen -- und `setBody` setzt ihn jetzt ueber
        # `cm.setValue`. `setValue` ersetzt das ganze Dokument und nimmt die Zeilenklassen
        # mit; CM5 feuert dabei **kein** `cursorActivity`. Steht der Cursor dabei auf
        # Zeile 0 (so ist es direkt nach dem Oeffnen), greift die Kurzpruefung in
        # `_cursorZeileSetzen()` (`cmCursorZeile === zeile`) -- und die Cursorzeile bleibt
        # **unmarkiert**. Genau das ist der Fehler, den der Fix in `editor.js` behebt.
        # Gemessen am 2026-10-24 an der Wegwerf-Instanz.
        editor_schliessen()
        item_klicken("Zweites Item")
        ergebnis["cursorzeilen_nach_itemwechsel"] = page.evaluate("""() => {
          return document.querySelectorAll('.CodeMirror .sfx-active-line').length;
        }""")
        # Und **zurueck** auf das erste Item -- der Weg muss auch rueckwaerts tragen.
        editor_schliessen()
        item_klicken("Mess-Item")
        ergebnis["cursorzeilen_nach_zurueck"] = page.evaluate("""() => {
          return document.querySelectorAll('.CodeMirror .sfx-active-line').length;
        }""")
        # Zelle 3 (die Cursorzeile) und Zelle 2 (die Formatierungszeichen) **nach** dem
        # Klick messen: der Cursor steht dann in der Zeile mit den `**`, und **dort**
        # muessen die Formatierungszeichen sichtbar sein -- auf der Ueberschrift
        # unsichtbar. Vorher stuende der Cursor woanders, und die Aussage waere ueber
        # eine andere Zeile gemacht.
        ergebnis["cursorzeilen"] = page.evaluate("""() => {
          return document.querySelectorAll('.CodeMirror .sfx-active-line').length;
        }""")
        ergebnis["formatierung_auf_zeilen"] = formatierung_messen(page)
        out["varianten"][name] = ergebnis

    # Der Rohmodus (ED-5) und der Notausgang (ED-5) messen die **ausgelieferte**
    # Variante "visibility" -- das ist die, die `app.css` heute traegt.
    AKTIVE_VARIANTE = "visibility"
    entwurf_loeschen()
    page.reload(wait_until="domcontentloaded")
    page.wait_for_selector("#shell", timeout=30000)
    item_oeffnen()

    # -- Zelle 4: der Rohmodus (ED-5) ----------------------------------------------
    out["schalter_text"] = page.locator("#toggle-preview").inner_text()
    page.click("#toggle-preview")
    page.wait_for_timeout(700)
    out["formatierung_im_rohmodus"] = page.evaluate("""() => {
      const f = document.querySelectorAll('.CodeMirror .cm-formatting');
      if (!f.length) return "keine Formatierungszeichen (Modus aus)";
      var unsichtbar = 0;
      f.forEach(function (e) {
        const r = e.getBoundingClientRect();
        if (getComputedStyle(e).visibility === "hidden" || r.width === 0) unsichtbar++;
      });
      return unsichtbar;
    }""")
    out["rohmodus_klasse"] = page.evaluate("""() => {
      const w = document.querySelector('.CodeMirror');
      return w ? w.classList.contains('is-raw') : null;
    }""")
    out["schalter_text_nachher"] = page.locator("#toggle-preview").inner_text()
    page.click("#toggle-preview")
    page.wait_for_timeout(500)

    # -- Zelle 5: der Notausgang (ED-5) -------------------------------------------
    # Der Nachlader scheitert: die Vendor-Datei fehlt (404). Die Textarea muss bleiben
    # und **alles** muss weiter funktionieren.
    page.unroute("**/ui/static/vendor/codemirror/codemirror.min.js")
    page.route("**/ui/static/vendor/codemirror/codemirror.min.js",
               lambda r: r.fulfill(status=404, body="nicht da"))
    entwurf_loeschen()
    page.reload(wait_until="domcontentloaded")
    page.wait_for_selector("#shell", timeout=30000)
    item_oeffnen()
    out["notausgang"] = page.evaluate("""() => {
      const ta = document.querySelector('#editor-textarea');
      return {
        editor_da: !!document.querySelector('.CodeMirror'),
        textarea_da: !!ta,
        text: ta ? ta.value : null,
      };
    }""")
    if out["notausgang"].get("textarea_da"):
        page.fill("#editor-textarea", "")
        page.type("#editor-textarea", "Notausgang")
        page.wait_for_timeout(300)
        out["notausgang"]["nach_tippen"] = page.evaluate("""() => {
          const ta = document.querySelector('#editor-textarea');
          return ta ? ta.value : null;
        }""")

    out["seitenfehler"] = fehler
    print(json.dumps(out, ensure_ascii=False))
    browser.close()
'''


def _provision(space: str) -> dict:
    from authserver import passwords, totp
    from authserver.config import decode_data_encryption_key
    from authserver.secretbox import seal
    from authserver.store import AuthStore

    password = "wegwerf-b11-" + secrets.token_urlsafe(8)
    secret_b32 = totp.generate_secret()
    dek = decode_data_encryption_key(DEK_FILE.read_text().strip(), origin=str(DEK_FILE))
    store = AuthStore(str(AUTH_DB), now_fn=lambda: datetime.now(timezone.utc))
    store.upsert_user(
        space=space,
        password_hash=passwords.hash_password(password),
        totp_secret_enc=seal(secret_b32.encode("ascii"), key=dek, aad=space.encode("utf-8")),
        totp_alg="SHA1",
        totp_confirmed_at=datetime.now(timezone.utc),
        status="active",
    )
    return {"space": space, "password": password, "secret": secret_b32}


def _setup() -> dict:
    shutil.rmtree(WEGWERF_ROOT, ignore_errors=True)
    WEGWERF_ROOT.mkdir(parents=True, exist_ok=True)
    DATA_ROOT.mkdir(parents=True, exist_ok=True)
    raw = secrets.token_bytes(32)
    DEK_FILE.write_text(base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii") + "\n")
    os.chmod(DEK_FILE, 0o600)
    alpha = _provision(SPACE)
    # Der Seed: **zwei** Zeilen mit dem Mess-Wort (die erste ist die Ueberschrift) und
    # Formatierungszeichen auf beiden Zeilen.
    code = (
        "import sys; sys.path.insert(0, 'phase1_storage')\n"
        "from storage.store import Store\n"
        f"s = Store({str(DATA_ROOT)!r}, git=True)\n"
        # **task/open** — der Listenfilter zeigt standardmaessig nur offene Aufgaben
        # (das ist der Grund, warum der 10.5-Seed auch task/open sein muss).
        f"s.create({SPACE!r}, type='task', title='Mess-Item',"
        f" body='# {KLICK_TEXT}\\n\\nEin Satz mit **{KLICK_TEXT}** und mehr Text.\\n')\n"
        # Das **zweite** Item: nur beim **Wechsel** auf ein zweites Item greift der
        # `setValue`-Pfad in `setBody` (beim ersten Item ist der Editor noch nicht
        # geladen, da schreibt `setBody` in die Textarea -- der Notausgang).
        f"s.create({SPACE!r}, type='task', title='Zweites Item', body='Nur ein Text.\\n')\n"
    )
    subprocess.run(
        [".venv/bin/python", "-c", code], check=True, cwd=str(REPO_ROOT),
        env={**os.environ, "PYTHONPATH": str(REPO_ROOT / "phase1_storage")},
    )
    return alpha


def _serve() -> subprocess.Popen:
    env = os.environ.copy()
    for name in list(env):
        if name.startswith("SHAREFYX_") or name.startswith("SFX_"):
            env.pop(name)
    env["SPACE_DATA_ROOT"] = str(DATA_ROOT)
    env["SPACE_AUTH_DB"] = str(AUTH_DB)
    env["SPACE_PUBLIC_BASE_URL"] = BASE
    env["SPACE_PORT"] = str(PORT)
    env["CREDENTIALS_DIRECTORY"] = str(WEGWERF_ROOT)
    env["PYTHONPATH"] = str(REPO_ROOT)
    env["REPO_ROOT"] = str(REPO_ROOT)
    env["TLS_KEY"] = str(TLS_KEY)
    env["TLS_CERT"] = str(TLS_CERT)
    if not (TLS_KEY.exists() and TLS_CERT.exists()):
        subprocess.run(
            ["openssl", "req", "-x509", "-newkey", "rsa:2048", "-keyout", str(TLS_KEY),
             "-out", str(TLS_CERT), "-days", "2", "-nodes", "-subj", "/CN=127.0.0.1",
             "-addext", "subjectAltName=IP:127.0.0.1"],
            check=True, capture_output=True,
        )
    launcher = WEGWERF_ROOT / "serve_tls.py"
    launcher.write_text(SERVE_TLS_LAUNCHER, encoding="utf-8")
    log_file = SERVE_LOG.open("ab")
    proc = subprocess.Popen(
        [".venv/bin/python", str(launcher)],
        env=env, cwd=str(REPO_ROOT), stdout=log_file, stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    SERVE_PID.write_text(str(proc.pid))
    import ssl
    import urllib.request

    ctx = ssl._create_unverified_context()
    for _ in range(80):
        try:
            urllib.request.urlopen(f"{BASE}/health", timeout=1, context=ctx).read()
            return proc
        except Exception:
            time.sleep(0.25)
    raise SystemExit("Wegwerf-Server wurde nicht gesund.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args(argv)

    alpha = _setup()
    server = _serve()
    proc = None
    try:
        skript = WEGWERF_ROOT / "browser_check.py"
        skript.write_text(BROWSER_SKILL, encoding="utf-8")
        e2e = Path.home() / ".claude-code-tools/e2e-venv/bin/python"
        out_file = (WEGWERF_ROOT / "browser.out").open("wb")
        err_file = (WEGWERF_ROOT / "browser.err").open("wb")
        proc = subprocess.Popen(
            [str(e2e), str(skript), BASE, alpha["space"], alpha["password"], alpha["secret"],
             str(WEGWERF_ROOT), KLICK_TEXT, KLICK_ZEICHEN, KLICK_ZEILE],
            cwd=str(REPO_ROOT), stdout=out_file, stderr=err_file,
        )
        try:
            proc.wait(timeout=300)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=10)
        # Die Ausgabe steht in **Dateien** (stdout/stderr gehen dorthin, nicht in Pipes).
        text = (WEGWERF_ROOT / "browser.out").read_text(encoding="utf-8", errors="replace").strip()
        if not text:
            log("Browser-Fehler:\n" + (WEGWERF_ROOT / "browser.err").read_text(
                encoding="utf-8", errors="replace")[-3000:])
            raise SystemExit("Der Browser hat nichts gemeldet.")
        messung = json.loads(text.splitlines()[-1])

        varianten = messung.get("varianten") or {}
        # Die **Belege der Varianten** (V211). Ohne den Bogen "die Variante wurde
        # wirklich ausgeliefert" waere die Messung blind -- das ist der Befund vom
        # 2026-10-24 (die erste Fassung mass drei gleiche Werte und meldete "gleich").
        #
        # **Drei Kriterien je Variante:**
        # 1. `cursor_auf_dem_zeichen` -- der Cursorindex aus CM5 == der Index aus dem DOM.
        # 2. `cursor_bleibt_stehen` -- der **sichtbare** Cursor steht auf dem geklickten
        #    Zeichen (nicht daneben).
        # 3. `getipptes_zeichen_an_der_stelle` -- das getippte X landet an der
        #    geklickten Stelle.
        varianten_belege = {}
        for name, v in varianten.items():
            varianten_belege[name] = {
                "ausgeliefert": v.get("variante_ausgeliefert"),
                "ausgeliefert_ist_die_variante": v.get("variante_ausgeliefert") == name,
                "cursor_auf_dem_zeichen": bool(v.get("cursor_auf_dem_zeichen")),
                "cursor_bleibt_stehen": bool(v.get("cursor_bleibt_stehen")),
                "getipptes_zeichen_an_der_stelle": bool(v.get("x_ist_das_zeichen")),
                "cursorzeilen": v.get("cursorzeilen"),
                "fehler": v.get("fehler"),
            }
        # Die **ausgelieferte** Variante (die, die `app.css` heute traegt) traegt die
        # Abnahme-Zeilen: ihre Cursorzeile, ihre Formatierungszeichen.
        heute = varianten.get("visibility") or {}
        zeilen = heute.get("formatierung_auf_zeilen") or []

        befund = {
            "live_editor_geladen": messung.get("live_editor_da") is True,
            "cursor_auf_das_geklickte_zeichen": bool(
                varianten_belege.get("visibility", {}).get("cursor_auf_dem_zeichen")
            ),
            "cursor_bleibt_auf_dem_zeichen_stehen": bool(
                varianten_belege.get("visibility", {}).get("cursor_bleibt_stehen")
            ),
            "getipptes_zeichen_an_der_geklickten_stelle": bool(
                varianten_belege.get("visibility", {}).get("getipptes_zeichen_an_der_stelle")
            ),
            "cursorzeile_markiert": (heute.get("cursorzeilen") or 0) == 1,
            # Der Marker **direkt nach dem Oeffnen** (ohne Cursorbewegung).
            "cursorzeile_markiert_beim_oeffnen": (
                (heute.get("cursorzeilen_beim_oeffnen") or 0) == 1
            ),
            # Der Marker **nach dem Wechsel** auf ein zweites Item -- der Pfad, in dem
            # `setBody` den Editor setzt (`cm.setValue`) und die Zeilenklassen
            # mitverliert. Ohne den Fix: 0.
            "cursorzeile_markiert_nach_itemwechsel": (
                (heute.get("cursorzeilen_nach_itemwechsel") or 0) == 1
            ),
            "cursorzeile_markiert_nach_zurueck": (
                (heute.get("cursorzeilen_nach_zurueck") or 0) == 1
            ),
            "formatierung_auf_der_cursorzeile_sichtbar": any(
                z["formatierung"] and all(v["sichtbar"] for v in z["formatierung"])
                for z in zeilen if z.get("istCursorzeile")
            ),
            "formatierung_auf_anderen_zeilen_unsichtbar": any(
                z["formatierung"] and all(not v["sichtbar"] for v in z["formatierung"])
                for z in zeilen if not z.get("istCursorzeile")
            ),
            # Der Rohmodus: **kein** Zeichen ist unsichtbar. Im Live-Modus gibt es
            # `.cm-formatting` gar nicht (der Modus faellt weg) -- dann ist die Aussage
            # "jedes Zeichen sichtbar" ebenfalls erfuellt, aber der Befund nennt das
            # ausdruecklich, statt es zu verschweigen.
            "rohmodus_zeigt_alle_zeichen": messung.get("formatierung_im_rohmodus") in (
                0, "keine Formatierungszeichen (Modus aus)",
            ),
            "rohmodus_klasse_gesetzt": messung.get("rohmodus_klasse") is True,
            "notausgang_ohne_editor": (
                (messung.get("notausgang") or {}).get("editor_da") is False
                and (messung.get("notausgang") or {}).get("textarea_da") is True
                and "Notausgang" in ((messung.get("notausgang") or {}).get("nach_tippen") or "")
            ),
            "keine_seitenfehler": not messung.get("seitenfehler"),
            # Jede Variante muss **wirklich** ausgeliefert worden sein -- sonst waeren
            # die drei Zahlen ohne Beleg.
            "alle_varianten_ausgeliefert": (
                len(varianten_belege) == 3
                and all(b["ausgeliefert_ist_die_variante"] for b in varianten_belege.values())
            ),
        }
        befund["varianten_belege"] = varianten_belege
        ok = all(v for v in befund.values() if isinstance(v, bool))
        ergebnis = {
            "probe": "p105_b11_live",
            "instanz": {"basis": BASE, "pid": server.pid, "wegwerf": True},
            "befund": befund,
            "messung": messung,
            "alle_kriterien_erfuellt": ok,
        }
        RESULT.write_text(
            json.dumps(ergebnis, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(json.dumps(ergebnis, indent=2, ensure_ascii=False))
        return 0 if ok else 1
    finally:
        if proc is not None and proc.poll() is None:
            proc.kill()
        if server.poll() is None:
            try:
                os.kill(server.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            try:
                server.wait(timeout=12)
            except subprocess.TimeoutExpired:
                try:
                    os.kill(server.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
        SERVE_PID.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
