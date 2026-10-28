#!/usr/bin/env python3
"""P10.5 Block 14, Schritt 14.5 — die **drei Kartenbilder** (P10.5-70) und der Rand-Fall
aus Plan §2.5 (der Lappen am Leinwandrand).

**Was der Schritt liefert.** (a) Die drei Bilder, die der Nikinger sehen will: die ganze Karte,
die Karte im Fokus, die Seite. (b) Die **Messung** des Rand-Falls, den der Plan §2.5 für 14.5
offen gelassen hat: „`FIT_MARGIN` ist 40 px, die Lappen-Kontur reicht aber **48 px**
(`LOBE_REACH`) plus eine Rasterzelle (8 px) über den äußersten Knoten — auf der **begrenzenden**
Achse können bis zu **16 px** der Kontur am Leinwandrand abgeschnitten werden."

**Derselbe Datensatz wie die Abnahme.** Die Bilder sollen **die Karte** zeigen, die in
`p105_b14_layout_probe.json` gemessen wurde — sonst wären sie ein anderes Bild als der Beleg.
Deshalb benutzt diese Probe **denselben Saat** (5 Spaces, 30/32/30/30/30 = 152 Items,
**eingefrorene IDs und Uhr**), **denselben** Wegwerf-Aufbau (TLS, freier Port je Lauf, eigener
Datenwurzelbaum und eigene `auth.sqlite3` je Lauf, Stopp **nur** über die PID-Datei) und
**denselben** Ruhe-Warte Mechanismus (`requestAnimationFrame` **aus** `graph.js` — der
Canvas-Hash taugt nicht, siehe Plan §0).

**Ohne die 16 Radschritte.** Das B15-Skript (`p105_b15_screens.py`) fuhr 16 Radstufen, weil es
keine Kamera-Anpassung gab (Plan §0, Befund B5). Seit 14.3 passt sich die Karte selbst ein
(`fitView()`) — die Radschritte **verkleinerten** sie nur (Plan §0, datierte Korrektur). Dieser
Schritt fährt deshalb **ohne** Rad.

**Wie gemessen wird — an der *gezeichneten* Kontur, nicht an den Konstanten.** Der Plan §2.5 hat
den Rand-Fall „aus den Konstanten gerechnet, nicht gemessen" in die Ecke gestellt. Gemessen wird
er am **Recorder**: ein Haken an der **Leinwand-API** des Browsers (kein Haken im Produktcode,
Plan §4) zeichnet jeden **Strich** mit seinem Pfad und seiner Transformation mit. Die
Lappen-Kontur ist der Strich mit `globalAlpha = 0.55` und `lineWidth = 1.1`
(`graph.js :: drawLobes()`); der Recorder filtert genau diese und **weist nach**, dass kein
anderer Strich dieselben beiden Werte trägt (sonst wäre die Messung nicht eindeutig). Die
gezeichneten **Kurven** werden abgetastet (die quadratische Kurve liegt in der Huehl-Kurve der
Punkte), die Punkte mit der **Transformation des Strichs** in Bild-Koordinaten gerechnet und
gegen den **Leinwandrand** gehalten.

**Die Rechnung, die der Recorder ersetzt:** `fitView()` stellt den **Umriss der sichtbaren
Knoten** in die Mitte und gibt `FIT_MARGIN` Rand — der **Umriss der Knoten**, nicht der Umriss
der **Lappen**. Die Kamera-Zelle (P10.5-67) misst bisher genau das: „der Inhalt passt in die
Leinwand". Ob der **gezeichnete** Inhalt passt, stand in keiner Zelle — das ist die Lücke, die
dieser Schritt schliesst.

Aufruf:  `.venv/bin/python phase10_5_finishing/probes/p105_b14_karte_bilder.py`
Ergebnis: `phase10_5_finishing/probes/p105_b14_karte_bilder.json`
Bilder:  `docs/screenshots/p105_b14_karte_0{1,2,3}_*.png`

**Optionen** (beide sind *Messvarianten*, keine Gegenlaeufe — sie aendern den Arbeitsbaum nie):

| Option | Wirkung |
|---|---|
| `--konstante=NAME=WERT` | die Konstante in einer **Kopie** der statischen Dateien patchen (Muster: `p105_b14_startwerte.py`) — der Beleg landet in einer **eigenen** Datei |
| `--bilder=VERZEICHNIS` | die Bilder in ein anderes Verzeichnis schreiben (die A/B-Vergleiche gehoeren nicht ins Repo) |
"""
from __future__ import annotations

import importlib.util
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PROBES = Path(__file__).resolve().parent
#: **Ein eigener Wurzelbaum** je Lauf — die Wegwerf-Instanz der Layout-Probe und diese Probe
#: duerfen sich nicht in die Daten (und den Port) teilen.
WEGWERF_ROOT = Path("/tmp/opencode/sharefyx-wegwerf-b14bilder")
PID = os.getpid()
RESULT = PROBES / "p105_b14_karte_bilder.json"
BILDER = REPO_ROOT / "docs" / "screenshots"
AUFTRAG_DATEI = WEGWERF_ROOT / ("auftrag-%d.json" % PID)

# -- Der Baustein: die Wegwerf-Instanz und der Saat der Layout-Probe --------------------------
#
# Die Probe **baut** nichts nach: sie importiert `p105_b14_layout_probe.py` und benutzt dessen
# `_setup()`, `_seed()`, `_serve()` und `_stop()`. Damit ist der **Datensatz identisch** mit dem
# der Abnahme (5 Spaces, 30/32/30/30/30, feste IDs, feste Uhr) — die Bilder zeigen **die**
# gemessene Karte. Die Pfade der Wegwerf-Instanz werden auf einen **eigenen** Baum je Lauf
# gesetzt (sonst wuerden zwei Laeufe um denselben Port und dieselben Dateien streiten).
_spec = importlib.util.spec_from_file_location(
    "p105_b14_layout_probe", PROBES / "p105_b14_layout_probe.py")
L = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(L)

L.DATA_ROOT = WEGWERF_ROOT / ("data-%d" % PID)
L.AUTH_DB = WEGWERF_ROOT / ("auth-%d.sqlite3" % PID)
L.CRED_DIR = WEGWERF_ROOT / ("cred-%d" % PID)
L.DEK_FILE = L.CRED_DIR / "auth-dek"
L.SERVE_PID = WEGWERF_ROOT / ("serve-%d.pid" % PID)
L.SERVE_LOG = WEGWERF_ROOT / ("serve-%d.log" % PID)
L.TLS_KEY = WEGWERF_ROOT / ("key-%d.pem" % PID)
L.TLS_CERT = WEGWERF_ROOT / ("cert-%d.pem" % PID)

#: Die **Optionen** dieser Probe. `--konstante=` wird von der Layout-Probe gelesen (sie hat den
#: Mechanismus schon: der Wert wird in einer Kopie der statischen Dateien gepatcht, der
#: Arbeitsbaum bleibt unberuehrt) — diese Probe reicht sie nur durch.
BILDER_VERZEICHNIS = None
for _arg in sys.argv[1:]:
    if _arg.startswith("--bilder="):
        BILDER_VERZEICHNIS = _arg.split("=", 1)[1].strip()
    elif _arg.startswith("--konstante="):
        pass                      # die Layout-Probe liest es (sie parst dieselbe argv)
    elif _arg.startswith("--label="):
        pass
    else:
        raise SystemExit("unbekannte Option: " + _arg)

if L.KONSTANTEN:
    RESULT = PROBES / ("p105_b14_karte_bilder_konstante_%s.json" % L.LABEL)


# ============================================================================================
# Der Browser-Teil. Playwright liegt im e2e-venv, nicht im Projekt-venv — deshalb ein **eigenes**
# Skript, das seinen Auftrag ueber eine Datei bekommt (kein `.format()` auf einem Quelltext, in
# dem JavaScript steht).
# ============================================================================================
BROWSER_SKILL = r'''"""Der Browser-Teil der Kartenbilder-Probe (Playwright, e2e-venv)."""
import base64, hashlib, hmac, json, math, struct, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

AUFTRAG = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
BASE = AUFTRAG["base"]
SPACE = AUFTRAG["space"]
RESULT = Path(AUFTRAG["result"])
REPO_ROOT = AUFTRAG["repo_root"]
AUTH_DB = AUFTRAG["auth_db"]
BILDER = Path(AUFTRAG["bilder"])
PREFIX = AUFTRAG["prefix"]


def totp_now(secret_b32):
    key = base64.b32decode(secret_b32 + "=" * (-len(secret_b32) % 8))
    counter = int(time.time() // 30)
    digest = hmac.new(key, struct.pack(">q", counter), hashlib.sha1).digest()
    # Das LETZTE Byte des Digests (RFC 4226, §5.3) — `digest[0]` ist der falsche Offset.
    offset = digest[-1] & 0x0F
    code = (struct.unpack(">I", digest[offset:offset + 4])[0] & 0x7FFFFFFF) % 1000000
    return f"{code:06d}"


def totp_zuruecksetzen():
    """Jeder Login **verbraucht** einen TOTP-Schritt — ein zweiter Login im selben
    30-Sekunden-Fenster schlaegt sonst mit 401 fehl (Muster aus der Layout-Probe)."""
    code = (
        "from datetime import datetime, timezone\n"
        "from authserver.store import AuthStore\n"
        f"store = AuthStore({AUTH_DB!r}, now_fn=lambda: datetime.now(timezone.utc))\n"
        f"store.set_totp_counter({SPACE!r}, 0)\n"
    )
    subprocess.run([str(Path(REPO_ROOT) / ".venv" / "bin" / "python"), "-c", code], check=True)


# -- Der Recorder der gezeichneten Lappen-Konturen --------------------------------------------
#
# **Kein Haken im Produktcode** (Plan §4): die Probe haengt sich an die **Leinwand-API** des
# Browsers. `clearRect` beginnt jeden Zeichendurchgang (`graph.js :: draw()` loescht am Anfang
# die Leinwand) — was zwischen dem letzten `clearRect` und dem Ende des Durchgangs **gestrichen**
# wurde, ist die **gezeichnete Menge des letzten Bildes**.
#
# Die **Lappen-Kontur** ist der Strich mit `globalAlpha = 0.55` und `lineWidth = 1.1`
# (`graph.js :: drawLobes()`: die Flaeche fuellt mit 0,05, die Kontur strickt mit 0,55 und 1,1 px,
# die innere Linie mit 1,0 und 1 px). Der Recorder **weist nach**, dass kein anderer Strich
# dieselben beiden Werte traegt — sonst waere die Messung nicht eindeutig.
REZORDER = r"""
(() => {
  const proto = CanvasRenderingContext2D.prototype;
  const orig = {
    beginPath: proto.beginPath, clearRect: proto.clearRect, moveTo: proto.moveTo,
    lineTo: proto.lineTo, quadraticCurveTo: proto.quadraticCurveTo,
    bezierCurveTo: proto.bezierCurveTo, arc: proto.arc, closePath: proto.closePath,
    stroke: proto.stroke,
  };
  const zustand = {pfad: [], filter: [], gesamt: [], frames: 0};
  window.__lappen = zustand;
  const leinwand = (c) => c && c.canvas && c.canvas.id === 'overview-graph-canvas';
  proto.clearRect = function (x, y, w, h) {
    if (leinwand(this)) { zustand.filter = []; zustand.gesamt = []; zustand.frames += 1; }
    return orig.clearRect.call(this, x, y, w, h);
  };
  proto.beginPath = function () { zustand.pfad = []; return orig.beginPath.call(this); };
  proto.moveTo = function (x, y) {
    zustand.pfad.push(['m', x, y]); return orig.moveTo.call(this, x, y);
  };
  proto.lineTo = function (x, y) {
    zustand.pfad.push(['l', x, y]); return orig.lineTo.call(this, x, y);
  };
  proto.quadraticCurveTo = function (cx, cy, x, y) {
    zustand.pfad.push(['q', cx, cy, x, y]); return orig.quadraticCurveTo.call(this, cx, cy, x, y);
  };
  proto.bezierCurveTo = function (a1, b1, a2, b2, x, y) {
    zustand.pfad.push(['b', a1, b1, a2, b2, x, y]);
    return orig.bezierCurveTo.call(this, a1, b1, a2, b2, x, y);
  };
  proto.arc = function (x, y, r, s, e, cc) {
    zustand.pfad.push(['a', x, y, r]); return orig.arc.call(this, x, y, r, s, e, cc);
  };
  proto.closePath = function () { return orig.closePath.call(this); };
  proto.stroke = function () {
    if (leinwand(this)) {
      const m = this.getTransform();
      const eintrag = {
        alpha: this.globalAlpha, breite: this.lineWidth, stil: String(this.strokeStyle),
        m: [m.a, m.b, m.c, m.d, m.e, m.f], pfad: zustand.pfad.slice(),
      };
      zustand.gesamt.push({alpha: eintrag.alpha, breite: eintrag.breite, stil: eintrag.stil});
      // **Die Toleranz:** `lineWidth` ist ein `float32` — 1,1 kommt als 1,100000023841858
      // zurueck. Die Toleranz muss groesser als das Rauschen sein, sonst findet der Filter
      // **nichts** (gemessen: der erste Lauf fand 0 Striche und meldete die Klassenleere).
      const ist_filter = Math.abs(this.globalAlpha - 0.55) < 1e-6
                         && Math.abs(this.lineWidth - 1.1) < 1e-6;
      if (ist_filter) zustand.filter.push(eintrag);
    }
    return orig.stroke.call(this);
  };
})();
"""

# Die **gezeichneten Lappen-Konturen** in Bild-Koordinaten (CSS-Pixel).
#
# Die Pfadpunkte stehen in **Welt-Koordinaten** (die Welt-Transformation war beim Zeichnen
# aktiv: `ctx.translate(panX, panY); ctx.scale(zoom, zoom)`). Die Transformation des Strichs
# (`getTransform()`) rechnet sie in **Geraete-Pixel**; geteilt durch `dpr` sind es CSS-Pixel —
# dieselben, in denen die Leinwand liegt.
LAPPEN = r"""() => {
  const z = window.__lappen;
  if (!z) return null;
  const c = document.getElementById('overview-graph-canvas');
  const r = c.getBoundingClientRect();
  const dpr = c.width / r.width;
  const lappen = [];
  for (const s of z.filter) {
    const m = s.m;
    let minx = Infinity, miny = Infinity, maxx = -Infinity, maxy = -Infinity;
    let cur = null;
    let punkte = 0;
    const put = (x, y) => {
      const sx = (m[0] * x + m[2] * y + m[4]) / dpr;
      const sy = (m[1] * x + m[3] * y + m[5]) / dpr;
      if (sx < minx) minx = sx;
      if (sy < miny) miny = sy;
      if (sx > maxx) maxx = sx;
      if (sy > maxy) maxy = sy;
      punkte += 1;
    };
    for (const p of s.pfad) {
      if (p[0] === 'm' || p[0] === 'l') { cur = [p[1], p[2]]; put(cur[0], cur[1]); }
      else if (p[0] === 'q') {
        const c1 = [p[1], p[2]], e = [p[3], p[4]];
        for (let t = 0; t <= 1.0001; t += 0.05) {
          const u = 1 - t;
          put(u * u * cur[0] + 2 * u * t * c1[0] + t * t * e[0],
              u * u * cur[1] + 2 * u * t * c1[1] + t * t * e[1]);
        }
        cur = e;
      }
    }
    lappen.push({
      x0: minx, y0: miny, x1: maxx, y1: maxy, punkte: punkte,
      alpha: s.alpha, breite: s.breite, stil: s.stil, m: s.m,
    });
  }
  // **Die Eindeutigkeit des Filters:** kein *anderer* Strich darf dieselben beiden Werte
  // (0,55 / 1,1) tragen — sonst waere die Messung "die Lappen-Kontur" nicht eindeutig.
  const mit_alpha = z.gesamt.filter(s => Math.abs(s.alpha - 0.55) < 1e-6).length;
  const mit_breite = z.gesamt.filter(s => Math.abs(s.breite - 1.1) < 1e-6).length;
  // Das **Histogramm** der Striche (Alpha x Breite) — die Diagnose, wenn der Filter leer bleibt.
  const histo = {};
  for (const s of z.gesamt) {
    const k = String(s.alpha) + 'x' + String(s.breite);
    histo[k] = (histo[k] || 0) + 1;
  }
  return {
    frames: z.frames, strokes: z.gesamt.length, lappen: lappen,
    mit_alpha: mit_alpha, mit_breite: mit_breite, histogramm: histo,
    eindeutig: mit_alpha === lappen.length && mit_breite === lappen.length,
  };
}"""

KASTEN = r"""() => {
  const c = document.getElementById('overview-graph-canvas');
  if (!c) return null;
  const r = c.getBoundingClientRect();
  return {left: r.left, top: r.top, width: r.width, height: r.height,
          dw: c.width, dh: c.height, dpr: c.width / r.width};
}"""

ABLAGE = r"""() => {
  const ks = Object.keys(localStorage).filter(k => k.startsWith('sfx:graph:layout'));
  if (!ks.length) return null;
  const v = JSON.parse(localStorage.getItem(ks[0]));
  return {key: ks[0], v: v.v, pos: v.pos || {}};
}"""

GRAFIK = r"""async () => (await fetch('/api/v1/graph')).json()"""

ZOOM = r"""() => {
  const el = document.getElementById('overview-graph-zoom');
  if (!el) return null;
  const m = /(-?\d+)\s*%/.exec(el.textContent || '');
  return m ? parseInt(m[1], 10) / 100 : null;
}"""

# Die Karte ist **gemalt** (irgendetwas steht im Canvas) — die Vorbedingung der Ruhe-Messung.
GEPAINTET = """() => {
  const c = document.getElementById('overview-graph-canvas');
  if (!c) return false;
  const d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data;
  for (let i = 3; i < d.length; i += 400) if (d[i] !== 0) return true;
  return false;
}"""

# Zaehlt die Animationsframes, die **aus graph.js** kommen (der Stack entscheidet).
RAF_PROBE = """
(() => {
  const log = {count: 0, other: 0, stamps: []};
  window.__rafLog = log;
  const orig = window.requestAnimationFrame.bind(window);
  window.requestAnimationFrame = function (cb) {
    const fromGraph = String(new Error().stack || '').includes('graph.js');
    return orig(function (t) {
      if (fromGraph) { log.count += 1; log.stamps.push(performance.now()); }
      else { log.other += 1; }
      return cb(t);
    });
  };
})();
"""


def login(page):
    totp_zuruecksetzen()
    page.goto(BASE + "/ui/login", wait_until="domcontentloaded")
    page.fill('input[name="space"]', SPACE)
    page.fill('input[name="password"]', AUFTRAG["password"])
    page.fill('input[name="totp"]', totp_now(AUFTRAG["secret"]))
    page.click('form[action="/ui/login"] button[type="submit"]')
    page.wait_for_selector("#shell", timeout=30000)
    page.wait_for_selector(".overview__graph canvas", state="visible", timeout=20000)


def settle(page, budget_ms=60000):
    """Warten, bis die Simulation **keine Frames mehr anfordert** (der Canvas-Hash taugt dafuer
    nicht — Plan §0: die Karte wird zuerst zweimal unveraendert gezeichnet)."""
    page.wait_for_function(GEPAINTET, timeout=30000)
    last = -1
    still = 0
    elapsed = 0
    while elapsed <= budget_ms:
        n = page.evaluate("() => window.__rafLog.count")
        if n == last:
            still += 1
            if still >= 4 and (n > 0 or elapsed > 4000):
                return
        else:
            still = 0
        last = n
        page.wait_for_timeout(100)
        elapsed += 100
    raise RuntimeError("die Simulation kam nicht zur Ruhe")


def nachbarn_je_knoten(grafik):
    nachbarn = {}
    for e in grafik["edges"]:
        nachbarn.setdefault(e["src"], set()).add(e["dst"])
        nachbarn.setdefault(e["dst"], set()).add(e["src"])
    return nachbarn


def main():
    fehler = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1920, "height": 1200},
                                  ignore_https_errors=True)
        page = ctx.new_page()
        page.add_init_script(RAF_PROBE)
        page.add_init_script(REZORDER)
        page.on("pageerror", lambda e: fehler.append(str(e)))
        login(page)

        # ---- der frische Lauf (leerer Speicher) -------------------------------------------
        page.evaluate("() => { localStorage.clear(); }")
        page.reload(wait_until="domcontentloaded")
        page.wait_for_selector(".overview__graph canvas", state="visible", timeout=20000)
        settle(page)
        page.wait_for_timeout(1600)          # das Merken ist gedrosselt (1 s)

        kasten = page.evaluate(KASTEN)
        ablage = page.evaluate(ABLAGE)
        grafik = page.evaluate(GRAFIK)
        zoom_anzeige = page.evaluate(ZOOM)
        if not ablage or not ablage["pos"]:
            raise RuntimeError("keine Ablage im localStorage (das Layout wurde nicht gemerkt)")
        pos = ablage["pos"]

        # ---- 1) das Bild 1: die ganze Karte (ohne Rad, ohne Fokus) --------------------------
        BILDER.mkdir(parents=True, exist_ok=True)
        bilder = []

        def bild(name, take):
            ziel = BILDER / name
            take(ziel)
            bilder.append({"datei": name, "bytes": ziel.stat().st_size})

        def canvas_shot(ziel):
            page.locator("#overview-graph-canvas").screenshot(path=str(ziel))

        bild("%s_01_ganz.png" % PREFIX, canvas_shot)

        # ---- 2) die Messung: die gezeichnete Lappen-Kontur gegen den Leinwandrand ----------
        lappen = page.evaluate(LAPPEN)
        if not lappen or not lappen["lappen"]:
            raise RuntimeError(
                "die Lappen-Kontur wurde nicht aufgezeichnet: " + json.dumps(lappen)
                + " Seitenfehler: " + json.dumps(fehler))
        # Die Kamera-Transformation aus der **gezeichneten** Kontur (exakt, nicht geschaetzt):
        # die Matrix ist `zoom * dpr` und `pan * dpr`.
        m = lappen["lappen"][0]["m"]
        zoom = m[0] / kasten["dpr"]
        pan_x = m[4] / kasten["dpr"]
        pan_y = m[5] / kasten["dpr"]

        def nach_bild(x, y):
            return (zoom * x + pan_x, zoom * y + pan_y)

        xs = [p[0] for p in pos.values()]
        ys = [p[1] for p in pos.values()]
        knoten_welt = {"x0": min(xs), "y0": min(ys), "x1": max(xs), "y1": max(ys)}
        e0 = nach_bild(knoten_welt["x0"], knoten_welt["y0"])
        e1 = nach_bild(knoten_welt["x1"], knoten_welt["y1"])
        knoten_bild = {"x0": e0[0], "y0": e0[1], "x1": e1[0], "y1": e1[1]}

        lappen_bild = {"x0": min(l["x0"] for l in lappen["lappen"]),
                       "y0": min(l["y0"] for l in lappen["lappen"]),
                       "x1": max(l["x1"] for l in lappen["lappen"]),
                       "y1": max(l["y1"] for l in lappen["lappen"])}
        # **Der Beschnitt:** wie viel der gezeichneten Kontur liegt **ausserhalb** der Leinwand?
        beschnitt = {
            "links": max(0.0, -lappen_bild["x0"]),
            "rechts": max(0.0, lappen_bild["x1"] - kasten["width"]),
            "oben": max(0.0, -lappen_bild["y0"]),
            "unten": max(0.0, lappen_bild["y1"] - kasten["height"]),
        }
        beschnitt["ja"] = any(v > 0.5 for v in (beschnitt["links"], beschnitt["rechts"],
                                               beschnitt["oben"], beschnitt["unten"]))
        # **Die Raender:** der Abstand vom Leinwandrand zum **Umriss der Knoten** (das ist der
        # `FIT_MARGIN`, den die Kamera gibt) und zum **Umriss der Lappen** (das ist der gezeichnete
        # Inhalt).
        raender = {
            "knoten_links": knoten_bild["x0"],
            "knoten_rechts": kasten["width"] - knoten_bild["x1"],
            "knoten_oben": knoten_bild["y0"],
            "knoten_unten": kasten["height"] - knoten_bild["y1"],
            "lappen_links": lappen_bild["x0"],
            "lappen_rechts": kasten["width"] - lappen_bild["x1"],
            "lappen_oben": lappen_bild["y0"],
            "lappen_unten": kasten["height"] - lappen_bild["y1"],
        }
        # **Der Reach der Kontur ueber den aeussersten Knoten** (Welt-Pixel) — die Zahl, die der
        # Plan §2.5 aus den Konstanten gerechnet hat ("48 px plus eine Rasterzelle"). Die
        # Transformation ist eine reine Skalierung plus Verschiebung, also laesst sie sich
        # zurueckrechnen.
        lappen_welt = {
            "x0": (lappen_bild["x0"] - pan_x) / zoom,
            "y0": (lappen_bild["y0"] - pan_y) / zoom,
            "x1": (lappen_bild["x1"] - pan_x) / zoom,
            "y1": (lappen_bild["y1"] - pan_y) / zoom,
        }
        reach = {
            "links": knoten_welt["x0"] - lappen_welt["x0"],
            "rechts": lappen_welt["x1"] - knoten_welt["x1"],
            "oben": knoten_welt["y0"] - lappen_welt["y0"],
            "unten": lappen_welt["y1"] - knoten_welt["y1"],
        }

        # ---- 3) das Bild 2: die Karte im Fokus ---------------------------------------------
        nachbarn = nachbarn_je_knoten(grafik)
        raum_von = {n["id"]: n["space"] for n in grafik["nodes"]}
        kandidaten = [(nid, len(nb)) for nid, nb in nachbarn.items() if len(nb) >= 5]
        fokus = None
        for nid, _deg in sorted(kandidaten, key=lambda k: -k[1]):
            xy = pos.get(nid)
            if not xy:
                continue
            sx, sy = nach_bild(xy[0], xy[1])
            if 0 <= sx <= kasten["width"] and 0 <= sy <= kasten["height"]:
                fokus = {"id": nid, "nachbarn": len(nachbarn[nid]), "x": sx, "y": sy}
                break
        if fokus is None:
            raise RuntimeError("kein Fokus-Knoten mit >= 5 Nachbarn im Bild")
        page.mouse.move(kasten["left"] + fokus["x"], kasten["top"] + fokus["y"])
        page.wait_for_timeout(700)
        bild("%s_02_fokus.png" % PREFIX, canvas_shot)

        # ---- 4) das Bild 3: die Seite (der Fokus muss weg, sonst ist die Karte gedimmt) -----
        page.mouse.move(4, 4)
        page.wait_for_timeout(700)
        bild("%s_03_seite.png" % PREFIX, lambda ziel: page.screenshot(path=str(ziel)))

        ctx.close()
        browser.close()

    bericht = {
        "probe": "p105_b14_karte_bilder",
        "schritt": "14.5",
        "zeit": datetime.now(timezone.utc).isoformat(),
        "seed": AUFTRAG["seed"],
        "konstanten_varianten": AUFTRAG.get("konstanten_varianten") or {},
        "konstanten_gesendet": AUFTRAG.get("konstanten_gesendet") or {},
        "leinwand": {"breite": kasten["width"], "hoehe": kasten["height"],
                     "dpr": kasten["dpr"], "zoom": zoom, "pan": [pan_x, pan_y],
                     "zoom_anzeige": zoom_anzeige},
        "knoten": {"anzahl": len(pos), "welt": knoten_welt, "bild": knoten_bild},
        "lappen": {"anzahl": len(lappen["lappen"]), "bild": lappen_bild, "welt": lappen_welt,
                   "reach_welt_px": reach,
                   "je_lappe": [{"x0": l["x0"], "y0": l["y0"], "x1": l["x1"], "y1": l["y1"],
                                 "stil": l["stil"], "punkte": l["punkte"]}
                                for l in lappen["lappen"]],
                   "filter_eindeutig": lappen["eindeutig"],
                   "strokes_gesamt": lappen["strokes"],
                   "mit_alpha": lappen["mit_alpha"], "mit_breite": lappen["mit_breite"]},
        "raender": raender,
        "beschnitt": beschnitt,
        "fokus": fokus,
        "bilder": bilder,
        "seitenfehler": fehler,
    }
    bericht["alle_kriterien_erfuellt"] = bool(
        not fehler
        and lappen["eindeutig"]
        and len(bilder) == 3
        and all(b["bytes"] > 10000 for b in bilder)
        and bericht["knoten"]["anzahl"] == AUFTRAG["seed"]["items"]
    )
    RESULT.write_text(json.dumps(bericht, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(bericht, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''


def main() -> int:
    global RESULT, BILDER
    if BILDER_VERZEICHNIS:
        BILDER = Path(BILDER_VERZEICHNIS)
        if not BILDER.is_absolute():
            BILDER = REPO_ROOT / BILDER
    L.PORT = L._freier_port()
    L.BASE = f"https://127.0.0.1:{L.PORT}"
    creds = L._setup()
    L._seed()
    try:
        L._serve()
        auftrag = {
            "base": L.BASE,
            "space": L.SPACE,
            "password": creds["password"],
            "secret": creds["secret"],
            "repo_root": str(REPO_ROOT),
            "auth_db": str(L.AUTH_DB),
            "result": str(RESULT),
            "bilder": str(BILDER),
            "prefix": "p105_b14_karte",
            "konstanten_varianten": L.KONSTANTEN,
            "konstanten_gesendet": L._konstanten_werte(
                L._graph_text() if not L.KONSTANTEN else
                _mit_varianten(L._graph_text(), L._konstanten_patch())),
            "seed": {"spaces": len(L.SPACES), "items": sum(L.ITEMS_PRO_SPACE.values()),
                     "items_pro_space": L.ITEMS_PRO_SPACE},
        }
        AUFTRAG_DATEI.parent.mkdir(parents=True, exist_ok=True)
        AUFTRAG_DATEI.write_text(json.dumps(auftrag), encoding="utf-8")
        skript = WEGWERF_ROOT / ("browser_bilder_%d.py" % PID)
        skript.parent.mkdir(parents=True, exist_ok=True)
        skript.write_text(BROWSER_SKILL, encoding="utf-8")
        e2e = Path.home() / ".claude-code-tools/e2e-venv/bin/python"
        proc = subprocess.run(
            [str(e2e), str(skript), str(AUFTRAG_DATEI)],
            cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=900,
        )
        print(proc.stdout.strip()[-8000:])
        if proc.returncode != 0:
            print(proc.stderr.strip()[-8000:], file=sys.stderr)
            return 1
    finally:
        # **jeder** Ausgang stoppt den Wegwerf-Server — ueber die PID-Datei (Hard Rule 9)
        L._stop()
    return 0


def _mit_varianten(text: str, patch: dict) -> str:
    """Der Quelltext **mit** den gepatchten Werten (der Beleg muss sagen, **womit** gemessen
    wurde)."""
    for alt, neu in patch.items():
        text = text.replace(alt, neu)
    return text


if __name__ == "__main__":
    raise SystemExit(main())
