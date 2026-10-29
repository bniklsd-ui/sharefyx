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

**Die Zelle `koerper` (Schritt 14.6.0, 2026-10-28).** Die Bilder zeigen **fuenf Inseln**
(Plan `docs/concepts/phase10_5_block14_6_plan.md` §0): die Koerpermaske ist nur `LOBE_REACH`
= 48 px um jeden Knoten, und das Layout aus Block 14 stellt die Spaces weit auseinander — die
Lappen beruehren sich nie, es gibt **0** Furche-Zellen, und der Plan 14.6 will aus den Inseln
**einen Koerper** machen.

Die Zelle misst das **an der Raster-Menge**, nicht an den Bildern: die **Komponenten** des
Koerpers (4-zusammenhaengend, **mit** den Furche-Zellen), die **Lappen je Space** (ueber die
Zellen **ohne** Furche), die **Furche-Zellen** und die **Paare**, zwischen denen eine Furche
liegt. Gemessen wird ueber ein **Messpflaster in einer Kopie** von `graph.js` (Muster:
`p105_b8_c2_probe.mjs`, `globalThis.__furrowCells`) — **kein Haken im Produktcode**.

**Zwei Durchgaenge je Lauf.** (a) Die **Bilder** und der Rand (Reach/Luft) aus den
**ungepatchten** Dateien — die Bilder im Repo zeigen **Produktcode** (`test_b14_karte_bilder.py`
prueft das). (b) Die **`koerper`-Zahlen** und die **Zeit** von `computeLobes()` aus einem
**eigenen**, gepatchten Durchgang: das Pflaster misst nur, es veraendert nichts — aber die
Bilder sollen den Produktcode zeigen, und das ist mit einem Pflaster in der ausgelieferten
Datei nicht mehr der Fall. Die Zeit wird **um den Aufruf** in `settle()` gemessen
(`performance.now()`, im Pflaster, nicht im Produktcode) — einmal nach dem Einschwingen, bei
**152** und bei **201** Knoten (Plan 14.6 §2.5: die Zeitgrenze gilt bei 201 Knoten).

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
# Das Messpflaster (Schritt 14.6.0) — es macht sichtbar, was die Karte im Inneren rechnet
# ============================================================================================
#
# **Kein Haken im Produktcode** (Plan 14.6 §4): das Pflaster patcht eine **Kopie** der
# statischen Dateien (derselbe Weg wie die Messvariante `--konstante=`; der Arbeitsbaum bleibt
# unberuehrt). Es baut **keinen Fehler** ein — es legt nur die Zahlen offen, die
# `computeLobes()` im Inneren berechnet.
#
# (1) `globalThis.__koerper` -- das Raster und die Mengen:
#       `cols`, `rows`, `cell`, `minX`, `minY` -- die Geometrie des Rasters
#       `koerper` -- **1** fuer jede Koerperzelle (0 sonst)
#       `space`  -- der Space je Zelle (null ausserhalb des Koerpers)
#       `furrow` -- **1** fuer jede Furche-Zelle
#       `knoten` -- die Knoten (x, y, Space) -- fuer den kleinsten Abstand zweier Spaces
# (2) `globalThis.__koerperZeit` -- die Zeit des **ersten** Aufrufs von `computeLobes()` in
#     `settle()` -- und `globalThis.__koerperZeiten` mit **fuenf** Messungen. **Ein einzelner
#     Aufruf ist verrauscht** (JIT, GC, Last des Rechners): gemessen am 2026-10-28 lagen die
#     Varianten 80 und 160 (Raster 178x147 und 198x167) bei **26,6 ms** und **50,7 ms**, die
#     groessere Variante 200 (Raster 200x171) aber bei **29,8 ms** -- das ist **kein** Trend,
#     das ist Rauschen. Die **Entscheidung** (Plan §2.5: die Grenze von 50 ms bei 201 Knoten)
#     traegt deshalb der **Median** aus fuenf Aufrufen. Die **fuenf** Aufrufe kommen **nach**
#     dem gezeichneten Zustand: der Cache haelt das Ergebnis des **ersten** Aufrufs, das Bild
#     ist also unveraendert.
#
# **Die Anker sind eindeutig** (Regel + Nachbarzeile, nicht nur ein Wert) -- sonst patcht das
# Pflaster den Kommentar ueber der Regel statt der Regel (diese Fehlerklasse hat dieser
# Ordner zweimal gesehen).
MESS_PFLASTER = {
    "  return { key: lobeKey(shown), lobes: lobes };": (
        "  var __koerper = new Uint8Array(cols * rows);\n"
        "  for (var __ki = 0; __ki < cols * rows; __ki++) {\n"
        "    __koerper[__ki] = assign[__ki] >= 0 ? 1 : 0;\n"
        "  }\n"
        "  var __knoten = [];\n"
        "  for (var __kk = 0; __kk < list.length; __kk++) {\n"
        "    __knoten.push([list[__kk].x, list[__kk].y, list[__kk].space]);\n"
        "  }\n"
        "  globalThis.__koerper = { cols: cols, rows: rows, cell: cell,\n"
        "    minX: minX, minY: minY, koerper: Array.prototype.slice.call(__koerper),\n"
        "    space: spaceOf, furrow: Array.prototype.slice.call(furrow),\n"
        "    knoten: __knoten,\n"
        "    konturen: lobes.map(function (l) { return { space: l.space, outer: l.outer }; }),\n"
        "    kanten: (function () {\n"
        "      var out = [];\n"
        "      var alle = explicitEdges.concat(implicitEdges);\n"
        "      for (var i = 0; i < alle.length; i++) {\n"
        "        var a = nodeById[alle[i].src], b = nodeById[alle[i].dst];\n"
        "        if (!a || !b) continue;\n"
        "        var g = edgeGeometry(a, b);\n"
        "        out.push([a.x, a.y, g.cx, g.cy, b.x, b.y, a.space !== b.space ? 1 : 0]);\n"
        "      }\n"
        "      return out;\n"
        "    })() };\n"
        "  return { key: lobeKey(shown), lobes: lobes };"
    ),
    "  function settle() {\n    lobeCache = computeLobes(visibleNodes());": (
        "  function settle() {\n"
        "    var __t0 = performance.now();\n"
        "    lobeCache = computeLobes(visibleNodes());\n"
        "    var __t1 = performance.now();\n"
        "    globalThis.__koerperZeit = __t1 - __t0;\n"
        "    var __zeiten = [__t1 - __t0];\n"
        "    for (var __i = 0; __i < 4; __i++) {\n"
        "      var __s = performance.now();\n"
        "      computeLobes(visibleNodes());\n"
        "      __zeiten.push(performance.now() - __s);\n"
        "    }\n"
        "    globalThis.__koerperZeiten = __zeiten;"
    ),
}

#: Die **Knoten**, bei denen die Zeitgrenze gilt (Plan 14.6 §2.5: „bei **201** Knoten").
KNOTEN_FUER_DIE_ZEIT = 201


def _nachbarn(idx: int, cols: int, rows: int) -> list:
    """Die vier Nachbarn einer Zelle (ohne die Randzellen, die keinen haben)."""
    gx = idx % cols
    gy = idx // cols
    out = []
    if gx > 0:
        out.append(idx - 1)
    if gx < cols - 1:
        out.append(idx + 1)
    if gy > 0:
        out.append(idx - cols)
    if gy < rows - 1:
        out.append(idx + cols)
    return out


def _analyse_raster(raster: dict) -> dict:
    """Die Zahlen der Zelle `koerper` aus dem Raster (Plan 14.6 §5).

    **Der Koerper** = alle Zellen mit `koerper == 1` — **mit** den Furche-Zellen (die
    gehoeren zum Koerper, nur zu keinem Lappen; ohne sie zerfiele der Koerper bei *jedem*
    Wert in fuenf Teile und die Zelle waere nie gruen).
    **Der Lappen** eines Spaces = seine Zellen **ohne** Furche, je Space gezaehlt.
    """
    cols = raster["cols"]
    rows = raster["rows"]
    koerper = raster["koerper"]
    space = raster["space"]
    furrow = raster["furrow"]
    raeume = raster["raeume"]
    n = cols * rows

    # -- 1) die Komponenten des Koerpers (4-zusammenhaengend) ---------------------------------
    besucht = bytearray(n)
    komponenten = 0
    groessen = []
    for start in range(n):
        if not koerper[start] or besucht[start]:
            continue
        komponenten += 1
        groesse = 0
        besucht[start] = 1
        stapel = [start]
        while stapel:
            i = stapel.pop()
            groesse += 1
            for j in _nachbarn(i, cols, rows):
                if koerper[j] and not besucht[j]:
                    besucht[j] = 1
                    stapel.append(j)
        groessen.append(groesse)

    # -- 2) die Lappen je Space (die Zellen ohne Furche) --------------------------------------
    lobe_besucht = bytearray(n)
    lappen = {}
    zellen_je_space = {}
    for start in range(n):
        if not koerper[start]:
            continue
        sp = space[start]
        name = raeume[sp] if 0 <= sp < len(raeume) else "?"
        zellen_je_space[name] = zellen_je_space.get(name, 0) + 1
        if furrow[start] or lobe_besucht[start]:
            continue
        lappen[name] = lappen.get(name, 0) + 1
        lobe_besucht[start] = 1
        stapel = [start]
        while stapel:
            i = stapel.pop()
            for j in _nachbarn(i, cols, rows):
                if koerper[j] and not furrow[j] and not lobe_besucht[j]:
                    lobe_besucht[j] = 1
                    stapel.append(j)

    # -- 3) die Furche: die Paare, zwischen denen sie liegt -----------------------------------
    paare = {}
    furche_zellen = 0
    for i in range(n):
        if not koerper[i]:
            continue
        if furrow[i]:
            furche_zellen += 1
            eigene = space[i]
            fremde = set()
            for j in _nachbarn(i, cols, rows):
                if koerper[j] and space[j] != eigene:
                    fremde.add(space[j])
            for f in fremde:
                a = raeume[eigene] if 0 <= eigene < len(raeume) else "?"
                b = raeume[f] if 0 <= f < len(raeume) else "?"
                key = "|".join(sorted((a, b)))
                paare[key] = paare.get(key, 0) + 1

    # -- 4) der kleinste Abstand zweier Knoten verschiedener Spaces --------------------------
    # (die Zahl, aus der sich der noetige Schliess-Radius rechnet: die gewachsenen Masken
    # ueberlappen erst, wenn `2 · (LOBE_REACH + D) >= d`)
    knoten = raster.get("knoten") or []
    min_abstand = None
    for a in range(len(knoten)):
        for b in range(a + 1, len(knoten)):
            if knoten[a][2] == knoten[b][2]:
                continue
            d = ((knoten[a][0] - knoten[b][0]) ** 2 + (knoten[a][1] - knoten[b][1]) ** 2) ** 0.5
            if min_abstand is None or d < min_abstand:
                min_abstand = d

    zeiten = raster.get("zeiten") or []
    if len(zeiten) >= 3:
        sortiert = sorted(zeiten)
        zeit_ms = sortiert[len(sortiert) // 2]
    else:
        zeit_ms = raster.get("zeit_ms")

    return {
        "zeit_ms": zeit_ms,
        "zeit_ms_erster": raster.get("zeit_ms"),
        "zeit_messungen": zeiten,
        "komponenten": komponenten,
        "komponenten_groessen": sorted(groessen, reverse=True)[:10],
        "lappen_je_space": lappen,
        "zellen_je_space": zellen_je_space,
        "koerper_zellen": sum(1 for v in koerper if v),
        "furche_zellen": furche_zellen,
        "paare": paare,
        "paare_zahl": len(paare),
        "zellgroesse_px": raster["cell"],
        "raster": {"cols": cols, "rows": rows, "cell": raster["cell"],
                   "minX": raster["minX"], "minY": raster["minY"]},
        "knoten": len(knoten),
        "min_abstand_zwei_spaces_px": (round(min_abstand, 2)
                                       if min_abstand is not None else None),
    }


# ============================================================================================
# Die Form der Karte (Plan 14.7 §5, Schritt 14.7.0 (a)) — Abnahme P10.5-73/74
# ============================================================================================
#
# Gemessen an **denselben** Daten wie `koerper` (Messpflaster, gepatchter Durchgang): dem
# Raster, den Knoten, den **berechneten** Konturen (`lobe.outer` — die Punkte, durch die
# `traceSmooth()` die Kurve legt) und den Bahnen (`edgeGeometry()`).

#: **Solidität** (P10.5-73): Körperzellen ÷ Zellen der konvexen Hülle des Körpers. **Startwert**
#: 0,75 (Plan 14.7 §5) — bestätigt oder geändert bei E1, **nach** der Basislinie.
FUELLE_MIN = 0.75
#: **Verteilung** (P10.5-73): der Median des Nächster-Nachbar-Abstands **innerhalb** eines
#: Space muss mindestens das 1,25-Fache der **Basislinie** sein (Plan 14.7 §5). Die Basislinie
#: ist die Zahl aus 14.7.0 — `None` heißt: noch nicht gemessen, die Zelle ist dann rot.
VERTEILUNG_FAKTOR = 1.25
VERTEILUNG_BASIS_PX = 25.1     # gemessen 14.7.0 (2026-10-29), Median aller Spaces
#: **Welligkeit** (P10.5-74): die **Zusatzkrümmung** der Kontur je 100 px — höchstens 50 % der
#: Basislinie. `None` heißt: noch nicht gemessen.
WELLIGKEIT_ANTEIL = 0.5
WELLIGKEIT_BASIS = 11.096       # gemessen 14.7.0 (2026-10-29), rad je 100 px


def _huelle(punkte: list) -> list:
    """Die konvexe Hülle (Andrew, monotone Kette), gegen den Uhrzeigersinn."""
    pts = sorted(set(punkte))
    if len(pts) < 3:
        return pts

    def kreuz(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    unten, oben = [], []
    for p in pts:
        while len(unten) >= 2 and kreuz(unten[-2], unten[-1], p) <= 0:
            unten.pop()
        unten.append(p)
    for p in reversed(pts):
        while len(oben) >= 2 and kreuz(oben[-2], oben[-1], p) <= 0:
            oben.pop()
        oben.append(p)
    return unten[:-1] + oben[:-1]


def _in_huelle(huelle: list, x: float, y: float) -> bool:
    n = len(huelle)
    for i in range(n):
        a, b = huelle[i], huelle[(i + 1) % n]
        if (b[0] - a[0]) * (y - a[1]) - (b[1] - a[1]) * (x - a[0]) < 0:
            return False
    return True


def _fuelle(raster: dict) -> dict:
    cols, rows = raster["cols"], raster["rows"]
    koerper = raster["koerper"]
    zellen = [(i % cols, i // cols) for i, v in enumerate(koerper) if v]
    # die Hülle über die **Ecken** der Zellen — sonst fiele die Randreihe halb heraus
    ecken = []
    for gx, gy in zellen:
        ecken += [(gx, gy), (gx + 1, gy), (gx, gy + 1), (gx + 1, gy + 1)]
    huelle = _huelle(ecken)
    xs = [p[0] for p in huelle]
    ys = [p[1] for p in huelle]
    in_huelle = 0
    for gy in range(max(0, int(min(ys))), min(rows, int(max(ys)) + 1)):
        for gx in range(max(0, int(min(xs))), min(cols, int(max(xs)) + 1)):
            if _in_huelle(huelle, gx + 0.5, gy + 0.5):
                in_huelle += 1
    return {"koerper_zellen": len(zellen), "huelle_zellen": in_huelle,
            "soliditaet": round(len(zellen) / in_huelle, 4) if in_huelle else None}


def _verteilung(knoten: list) -> dict:
    je_space = {}
    alle = []
    for i, a in enumerate(knoten):
        best = None
        for j, b in enumerate(knoten):
            if i == j or a[2] != b[2]:
                continue
            d = ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5
            if best is None or d < best:
                best = d
        if best is not None:
            je_space.setdefault(a[2], []).append(best)
            alle.append(best)

    def median(v):
        v = sorted(v)
        return round(v[len(v) // 2], 2) if v else None

    return {"nn_median_px": median(alle),
            "nn_median_je_space_px": {k: median(v) for k, v in sorted(je_space.items())}}


def _welligkeit(konturen: list) -> dict:
    """**Zusatzkrümmung** je 100 px: (Σ|Knickwinkel| − |ΣKnickwinkel|) ÷ Umfang × 100, über
    alle äußeren Konturschleifen. Eine glatte konvexe Schleife hat **0** (sie dreht genau
    einmal), jede Treppenstufe kostet 2 × 90°. **Nicht** „Vorzeichenwechsel je 100 px" (Plan
    §5 erster Entwurf): das zählt nach dem Glätten auch winzige Restwellen voll — die
    Zusatzkrümmung wiegt sie nach ihrer Stärke (datierte Änderung im Plan, 14.7.0)."""
    import math
    gesamt_abs = gesamt_netto = umfang = 0.0
    schleifen = 0
    for kontur in konturen or []:
        for schleife in kontur.get("outer") or []:
            n = len(schleife)
            if n < 3:
                continue
            schleifen += 1
            summe = summe_abs = 0.0
            for i in range(n):
                a, b, c = schleife[i - 1], schleife[i], schleife[(i + 1) % n]
                w1 = math.atan2(b[1] - a[1], b[0] - a[0])
                w2 = math.atan2(c[1] - b[1], c[0] - b[0])
                d = (w2 - w1 + math.pi) % (2 * math.pi) - math.pi
                summe += d
                summe_abs += abs(d)
                umfang += math.dist(b, c)
            gesamt_abs += summe_abs
            gesamt_netto += abs(summe)
    wert = (gesamt_abs - gesamt_netto) / umfang * 100 if umfang else None
    return {"zusatzkruemmung_rad_je_100px": round(wert, 3) if wert is not None else None,
            "schleifen": schleifen, "umfang_px": round(umfang, 1)}


def _kontur_abstand(konturen: list) -> dict:
    """Der kleinste Abstand zweier Konturen **verschiedener** Lappen (Punkt–Strecke, über ein
    16-px-Gitter vorsortiert)."""
    import math
    zelle = 16.0
    gitter = {}
    for li, kontur in enumerate(konturen or []):
        for schleife in kontur.get("outer") or []:
            n = len(schleife)
            for i in range(n):
                a, b = schleife[i], schleife[(i + 1) % n]
                for gx in range(int(min(a[0], b[0]) // zelle) - 1, int(max(a[0], b[0]) // zelle) + 2):
                    for gy in range(int(min(a[1], b[1]) // zelle) - 1, int(max(a[1], b[1]) // zelle) + 2):
                        gitter.setdefault((gx, gy), []).append((li, a, b))
    best = None
    paar = None
    for li, kontur in enumerate(konturen or []):
        for schleife in kontur.get("outer") or []:
            for p in schleife:
                for (lj, a, b) in gitter.get((int(p[0] // zelle), int(p[1] // zelle)), []):
                    if lj == li:
                        continue
                    dx, dy = b[0] - a[0], b[1] - a[1]
                    ll = dx * dx + dy * dy
                    t = 0.0 if ll == 0 else max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / ll))
                    d = math.dist(p, (a[0] + t * dx, a[1] + t * dy))
                    if best is None or d < best:
                        best = d
                        paar = sorted((konturen[li]["space"], konturen[lj]["space"]))
    return {"min_px": round(best, 2) if best is not None else None, "paar": paar,
            "hinweis": None if best is not None else "keine zwei Konturen naeher als 16 px"}


def _kanten_aussen(raster: dict) -> dict:
    """Der Anteil der **Querbahnen** (zwei Spaces), der **außerhalb** des Körpers verläuft —
    21 Stützpunkte je quadratischer Bahn (nur berichtet, kein Tor, Plan §5)."""
    cols, rows, cell = raster["cols"], raster["rows"], raster["cell"]
    koerper = raster["koerper"]
    aussen = gesamt = 0
    for ax, ay, cx, cy, bx, by, quer in raster.get("kanten") or []:
        if not quer:
            continue
        for k in range(21):
            t = k / 20
            x = (1 - t) ** 2 * ax + 2 * (1 - t) * t * cx + t * t * bx
            y = (1 - t) ** 2 * ay + 2 * (1 - t) * t * cy + t * t * by
            gx = int((x - raster["minX"]) // cell)
            gy = int((y - raster["minY"]) // cell)
            gesamt += 1
            if not (0 <= gx < cols and 0 <= gy < rows and koerper[gy * cols + gx]):
                aussen += 1
    return {"anteil": round(aussen / gesamt, 4) if gesamt else None, "stuetzpunkte": gesamt}


def _form(koerper_roh: dict) -> dict:
    """Die Form-Zellen (Plan 14.7 §5) am Abnahme-Seed (152 Knoten)."""
    raster = koerper_roh["messungen"][0]
    fuelle = _fuelle(raster)
    verteilung = _verteilung(raster.get("knoten") or [])
    welligkeit = _welligkeit(raster.get("konturen"))
    abstand = _kontur_abstand(raster.get("konturen"))
    kanten = _kanten_aussen(raster)
    zellen = {
        "fuelle": bool(fuelle["soliditaet"] is not None and fuelle["soliditaet"] >= FUELLE_MIN),
        "verteilung": bool(VERTEILUNG_BASIS_PX is not None and verteilung["nn_median_px"]
                           is not None and verteilung["nn_median_px"]
                           >= VERTEILUNG_FAKTOR * VERTEILUNG_BASIS_PX),
        "kontur_welligkeit": bool(WELLIGKEIT_BASIS is not None
                                  and welligkeit["zusatzkruemmung_rad_je_100px"] is not None
                                  and welligkeit["zusatzkruemmung_rad_je_100px"]
                                  <= WELLIGKEIT_ANTEIL * WELLIGKEIT_BASIS),
        # **kein** Paar näher als 16 px ⇒ es gibt keinen Berührpunkt — das ist grün
        "kontur_abstand": bool(abstand["min_px"] is None or abstand["min_px"] > 0.0),
    }
    return {
        "fuelle": fuelle, "verteilung": verteilung, "welligkeit": welligkeit,
        "kontur_abstand": abstand, "kanten_aussen": kanten,
        "schwellen": {"fuelle_min": FUELLE_MIN, "verteilung_faktor": VERTEILUNG_FAKTOR,
                      "verteilung_basis_px": VERTEILUNG_BASIS_PX,
                      "welligkeit_anteil": WELLIGKEIT_ANTEIL, "welligkeit_basis": WELLIGKEIT_BASIS},
        "zellen": zellen,
        "p10_5_73": bool(zellen["fuelle"] and zellen["verteilung"]),
        "p10_5_74": bool(zellen["kontur_welligkeit"] and zellen["kontur_abstand"]),
    }


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
#: **Der Durchgang** dieses Laufs: "bilder" (die Bilder und der Rand) oder "koerper" (die
#: Rasterzahlen und die Zeit). Die beiden Durchgaenge laufen **nacheinander** in **zwei**
#: Wegwerf-Instanzen (Plan 14.6 §4) — die Bilder zeigen den Produktcode, die Zahlen kommen
#: aus dem gepatchten Durchgang.
DURCHGAENG = AUFTRAG["durchgang"]
SPACES = AUFTRAG["spaces"]


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

# Das **Raster** aus dem Messpflaster (Schritt 14.6.0). Die **Spaces** kommen als **Indizes**
# (die Namen stehen einmal im Bericht, nicht je Zelle) — sonst waeren es 20 000 Strings
# durch die Leitung.
KOERPER = r"""() => {
  const k = window.__koerper;
  if (!k) return null;
  const index = {};
  const raeume = [];
  const space = [];
  for (let i = 0; i < k.space.length; i++) {
    const s = k.space[i];
    if (s === null || s === undefined) { space.push(-1); continue; }
    if (!(s in index)) { index[s] = raeume.length; raeume.push(s); }
    space.push(index[s]);
  }
  return {
    cols: k.cols, rows: k.rows, cell: k.cell, minX: k.minX, minY: k.minY,
    koerper: k.koerper, space: space, furrow: k.furrow, knoten: k.knoten,
    raeume: raeume, konturen: k.konturen || null, kanten: k.kanten || null,
    zeit_ms: (typeof window.__koerperZeit === 'number') ? window.__koerperZeit : null,
    zeiten: window.__koerperZeiten || null,
  };
}"""

# Ein Item anlegen (fuer den zweiten Messpunkt: die Zeitgrenze gilt bei **201** Knoten).
# Muster: `p105_b14_layout_probe.py :: NEUES_ITEM`.
NEUES_ITEM = r"""async (args) => {
  const tok = (document.getElementById('bootstrap-csrf') || {}).value
           || sessionStorage.getItem('sfx:csrf');
  const r = await fetch('/api/v1/items', {
    method: 'POST',
    headers: {'Content-Type': 'application/json', 'x-csrf-token': tok},
    body: JSON.stringify(args.body),
  });
  const text = await r.text();
  if (!r.ok) throw new Error('POST /api/v1/items -> ' + r.status + ' ' + text);
  return JSON.parse(text);
}"""

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


def koerper_durchgang(page):
    """Der Durchgang **"koerper"** (Schritt 14.6.0): die Rasterzahlen und die Zeit von
    `computeLobes()`.

    **Zwei Messpunkte:** der **Abnahme-Seed** (5 Spaces, 152 Items) und die **201 Knoten**, bei
    denen die Zeitgrenze gilt (Plan §2.5). Fuer den zweiten Messpunkt kommen Items dazu — der
    Feed muss einpendeln, sonst laeuft die App mit der alten Karte weiter (derselbe Grund wie
    in der Layout-Probe).
    """
    messungen = []
    start = AUFTRAG["seed"]["items"]
    for ziel in (start, AUFTRAG["knoten_fuer_die_zeit"]):
        if ziel > start:
            for i in range(ziel - start):
                sp = SPACES[i % len(SPACES)]
                page.evaluate(NEUES_ITEM, {"body": {
                    "type": "note", "status": "active",
                    "title": "Probe Koerper %02d" % (i + 1), "space": sp, "folder": "ordner-2"}})
            # **Der Feed einpendeln lassen:** das Ereignis kommt bis zu ~1 s spaeter, die App
            # legt dann neu (und merkt die Karte) — sonst misst der folgende Lauf die alte.
            page.wait_for_timeout(2500)
        page.evaluate("() => { localStorage.clear(); }")
        page.reload(wait_until="domcontentloaded")
        page.wait_for_selector(".overview__graph canvas", state="visible", timeout=20000)
        settle(page)
        page.wait_for_timeout(1600)          # das Merken ist gedrosselt (1 s)
        raster = page.evaluate(KOERPER)
        if not raster:
            raise RuntimeError(
                "das Messpflaster hat keine Zahlen geliefert (globalThis.__koerper fehlt) — "
                "der Anker griff nicht")
        messungen.append(raster)
    return messungen


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

        # ---- der Durchgang "koerper" (Schritt 14.6.0) ----------------------------------------
        if DURCHGAENG == "koerper":
            messungen = koerper_durchgang(page)
            ctx.close()
            browser.close()
            bericht = {"durchgang": "koerper", "messungen": messungen, "seitenfehler": fehler}
            RESULT.write_text(json.dumps(bericht, ensure_ascii=False, indent=2) + "\n",
                              encoding="utf-8")
            print(json.dumps({"durchgang": "koerper",
                              "messungen": [{"cols": m["cols"], "rows": m["rows"],
                                              "zeit_ms": m["zeit_ms"],
                                              "knoten": len(m["knoten"] or [])}
                                             for m in messungen]},
                             ensure_ascii=False, indent=2))
            return 0

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
    creds = L._setup()
    L._seed()
    berichte = {}
    try:
        # **Zwei Durchgaenge** (Plan 14.6 §4): die Bilder und der Rand aus dem **ungepatchten**
        # Produktcode, die `koerper`-Zahlen und die Zeit aus dem **gepatchten**. Beide laufen
        # **nacheinander** — jeder mit einem **eigenen Port** und einer **eigenen** Instanz.
        for durchgang in ("bilder", "koerper"):
            L.PORT = L._freier_port()
            L.BASE = f"https://127.0.0.1:{L.PORT}"
            # **Das Messpflaster nur im zweiten Durchgang:** die Bilder im Repo zeigen den
            # **Produktcode** — mit dem Pflaster in der ausgelieferten Datei waere das nicht
            # mehr der Fall (und der Beleg muesste es sagen).
            L.GRAPH_PATCH_EXTRA = MESS_PFLASTER if durchgang == "koerper" else {}
            L._serve()
            try:
                berichte[durchgang] = _durchgang(durchgang, creds)
            finally:
                # **jeder** Ausgang stoppt den Wegwerf-Server — ueber die PID-Datei (Hard Rule 9)
                L._stop()
    finally:
        L._stop()
    bericht = _merge(berichte)
    RESULT.write_text(json.dumps(bericht, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(bericht, ensure_ascii=False, indent=2))
    return 0


def _durchgang(durchgang: str, creds: dict) -> dict:
    """Ein Durchgang: die Wegwerf-Instanz steht, der Browser laeuft, der Bericht kommt
    zurueck (in eine **eigene** Datei — der Beleg entsteht erst aus beiden Durchgaengen)."""
    ziel = WEGWERF_ROOT / ("bericht-%s-%d.json" % (durchgang, PID))
    auftrag = {
        "base": L.BASE,
        "space": L.SPACE,
        "password": creds["password"],
        "secret": creds["secret"],
        "repo_root": str(REPO_ROOT),
        "auth_db": str(L.AUTH_DB),
        "result": str(ziel),
        "bilder": str(BILDER),
        "prefix": "p105_b14_karte",
        "durchgang": durchgang,
        "knoten_fuer_die_zeit": KNOTEN_FUER_DIE_ZEIT,
        "spaces": list(L.SPACES),
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
        raise RuntimeError("der Durchgang %r ist gescheitert" % durchgang)
    return json.loads(ziel.read_text(encoding="utf-8"))


def _merge(berichte: dict) -> dict:
    """Die beiden Durchgaenge zu **einem** Beleg.

    Der Beleg traegt **beide** Durchgaenge: die Bilder und der Rand (ungepatcht) **und** die
    `koerper`-Zahlen und die Zeit (gepatcht). Die Zelle `koerper` ist **rot** an der
    Basislinie (Schritt 14.6.0) — das ist der gemessene Befund (Plan 14.6 §0), kein Fehler.
    """
    bilder = berichte["bilder"]
    bericht = dict(bilder)
    bericht["schritt"] = "14.6.0"
    # Die **Pruefsumme** der Positionen (die Rechnung sitzt **einmal** in der Layout-Probe):
    # sie vergleicht diese Karte mit der der Layout-Probe — dieselbe Karte, derselbe Saat.
    bericht["koerper"] = _koerper_zelle(bilder, berichte["koerper"])
    bilder_ok = bool(
        not bilder["seitenfehler"]
        and bilder["lappen"]["filter_eindeutig"]
        and len(bilder["bilder"]) == 3
        and all(b["bytes"] > 10000 for b in bilder["bilder"])
        and bilder["knoten"]["anzahl"] == bilder["seed"]["items"])
    bericht["zellen"] = {"bilder": bilder_ok, "koerper": bericht["koerper"]["ok"]}
    bericht["alle_kriterien_erfuellt"] = bool(bilder_ok and bericht["koerper"]["ok"])
    # **Die Form** (Plan 14.7, Schritt 14.7.0): eigene Zellen, eigene Summe — sie gehören zu
    # P10.5-73/74, nicht zu P10.5-72 (`alle_kriterien_erfuellt` bleibt die Summe von 72).
    bericht["form"] = _form(berichte["koerper"])
    return bericht


def _koerper_zelle(bilder: dict, koerper_roh: dict) -> dict:
    """Die Zelle `koerper` (Plan 14.6 §5) — gemessen an der **Rastermenge**, nicht am Bild.

    **Die Kriterien (wortgleich aus dem Plan §5):**
    - die Koerperzellen aller Spaces bilden **eine** 4-zusammenhaengende Komponente — gezaehlt
      **mit** den Furche-Zellen (sie gehoeren zum Koerper, nur zu keinem Lappen);
    - jeder Space hat **genau einen** Lappen — gezaehlt ueber seine Zellen **ohne** Furche;
    - zwischen je zwei Spaces, deren Lappen sich beruehren, liegt eine Furche (> 0 Zellen), und
      mindestens **4** solcher Paare existieren;
    - die Kontur reicht <= 52 px ueber den aeussersten Knoten, mit Luft > 0 px zur Leinwand;
    - die Knotenpositionen sind gleich zum Stand 14.5 — **das prueft die Layout-Probe**
      (Plan 14.6 §4, Schritt 14.6.3: "die Knotenpositionen sind gleich zu
      `p105_b14_layout_probe.json`"), nicht diese Probe: sie zeichnet kein Layout, sie
      misst den Koerper;
    - `computeLobes()` braucht <= 50 ms bei 201 Knoten.
    """
    messungen = koerper_roh["messungen"]
    abnahme = _analyse_raster(messungen[0])
    zeit = _analyse_raster(messungen[1]) if len(messungen) > 1 else {}
    reach = bilder["lappen"]["reach_welt_px"]
    luft = {k: bilder["raender"]["lappen_" + k] for k in ("links", "rechts", "oben", "unten")}

    ein_koerper = abnahme["komponenten"] == 1
    ein_lappen = bool(abnahme["lappen_je_space"]) and all(
        v == 1 for v in abnahme["lappen_je_space"].values()) and (
        len(abnahme["lappen_je_space"]) == len(abnahme["zellen_je_space"]))
    furche = abnahme["furche_zellen"] > 0 and abnahme["paare_zahl"] >= 4 and all(
        v > 0 for v in abnahme["paare"].values())
    rand_ok = bool(reach) and max(reach.values()) <= 52.0 and min(luft.values()) > 0.0
    zeit_ok = (zeit.get("zeit_ms") is not None and zeit["zeit_ms"] <= 50.0)

    grund = []
    if not ein_koerper:
        grund.append("%d Komponenten (statt 1)" % abnahme["komponenten"])
    if not ein_lappen:
        grund.append("Lappen je Space: %s" % abnahme["lappen_je_space"])
    if not furche:
        grund.append("%d Furche-Zellen, %d Paare" % (abnahme["furche_zellen"],
                                                      abnahme["paare_zahl"]))
    if not rand_ok:
        grund.append("Reach %s / Luft %s" % (reach, luft))
    if not zeit_ok:
        grund.append("computeLobes(): %s ms bei %s Knoten" % (
            zeit.get("zeit_ms"), zeit.get("knoten")))

    return {
        "ok": bool(ein_koerper and ein_lappen and furche and rand_ok and zeit_ok),
        "grund": "; ".join(grund) if grund else "alle Kriterien erfuellt",
        "abnahme": abnahme,
        "zeit": zeit,
        "reach_welt_px": reach,
        "luft_px": luft,
        "zeitgrenze_ms": 50,
    }


def _mit_varianten(text: str, patch: dict) -> str:
    """Der Quelltext **mit** den gepatchten Werten (der Beleg muss sagen, **womit** gemessen
    wurde)."""
    for alt, neu in patch.items():
        text = text.replace(alt, neu)
    return text


if __name__ == "__main__":
    raise SystemExit(main())
