#!/usr/bin/env python3
"""P10.5 Block 18, Schritt 18.0 — die **Basislinie** der trägen Karte und des Ausreißers.

Plan: `docs/concepts/phase10_5_block18_live_fixes_plan.md` (§2 Befunde K1–K4/A1–A3, §3 Schritt 18.0,
§5 die Tabelle, die diese Probe füllt). Nikinger 2026-11-01: „die Karte ist **sehr träge**, sobald
Ordner und/oder Tags an sind · ein oder wenige Punkte liegen **weit weg**".

**Diese Probe misst, sie schaltet nichts ab.** Sie baut nichts im Produktcode um: das Messpflaster
(`GRAPH_PATCH_EXTRA`, Muster `p105_b14_layout_probe.py`) hängt eine Hilfsschnittstelle an eine
**Kopie** von `graph.js`; der Arbeitsbaum bleibt unberührt.

**Wegwerf-Instanz** (Root-`CLAUDE.md`, Working style): eigener Port, tmp-`DATA_ROOT`, tmp-
`auth.sqlite3`, TLS, bereinigte Umgebung, Stopp nur über die PID-Datei (Hard Rule 9). Server, Konto und
Stopp kommen aus der Block-14-Probe (`p105_b14_layout_probe.py`, als Modul geladen — **eine** Quelle
für die Wegwerf-Mechanik, keine Kopie); der Browser-Teil nutzt deren Hilfen (`login`, `settle`,
`RAF_PROBE`, …) als **Textauszug** und hängt sein eigenes `main()` an.

**Die Saat (Nikinger 2026-11-01: „ungefähr 5" Spaces, Plan-Maß für Ordner/Tags, Items 263 laut
Durchsicht vom 2026-10-30):** 5 Spaces mit 100/80/50/32/**1** Items = 263; drei große Ordner mit
80/60/40 Items (+ ein kleiner mit 12); ~40 Tags mit 3–15 Knoten (Tags über 15 erzeugen keine Kanten —
`TAG_CLIQUE_LIMIT`); Verknüpfungen: jedes 4. Item auf das nächste im Space, jedes 10. quer. Der Ein-Item-
Space `epsilon` hat **keine** Verknüpfung (der schlimmste Fall: keine Kante zieht ihn heran). **Annahmen
(nicht vom Nikinger gemessen):** Tag-Verteilung und Verknüpfungsdichte — die Zahlen stehen im Beleg.

**Warum die Kantenzahlen im Beleg gegengerechnet werden:** ein Messhaken, der `implicitEdges.length`
liest, beweist nichts, solange man nicht weiß, was *herauskommen müsste*. Die Probe spiegelt
`buildTagEdges`/`buildFolderEdges` in Python **aus der Saat** (nicht aus der Seite) und vergleicht.

Aufruf:   `.venv/bin/python phase10_5_finishing/probes/p105_b18_karte_messung.py`
Ergebnis: `phase10_5_finishing/probes/p105_b18_karte_messung.json`
"""
from __future__ import annotations

import importlib.util
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

HIER = Path(__file__).resolve().parent
RESULT = HIER / "p105_b18_karte_messung.json"   # der Normalfall (18.1/18.2 nach dem Umbau)

# -- die Block-14-Probe als Modul laden (ohne ihre Kommandozeile zu erben) ------------------------
_argv = sys.argv
sys.argv = [_argv[0]]
_spec = importlib.util.spec_from_file_location("p105_b14_layout_probe", HIER / "p105_b14_layout_probe.py")
b14 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(b14)
sys.argv = _argv

REPO_ROOT = b14.REPO_ROOT

# -- die Saat ---------------------------------------------------------------------------------
SPACES = ["alpha", "beta", "gamma", "delta", "epsilon"]          # alpha = der eigene Space (Login)
ANZAHL = {"alpha": 100, "beta": 80, "gamma": 50, "delta": 32, "epsilon": 1}
GROSSER_ORDNER = {"alpha": ("projekt-a", 80), "beta": ("projekt-b", 60),
                  "gamma": ("projekt-c", 40), "delta": ("ordner-d", 12)}
TAG_POOL = 40
TAG_CLIQUE_LIMIT = 15           # graph.js :: TAG_CLIQUE_LIMIT -- die Probe prueft, dass die Konstante so steht


def spec() -> list[dict]:
    """Die Saat als Liste -- **eine** Quelle fuer das Anlegen und fuer die Gegenrechnung."""
    items = []
    g = 0
    for sp in SPACES:
        ordner, ordner_n = GROSSER_ORDNER.get(sp, ("", 0))
        for i in range(ANZAHL[sp]):
            tags = ["tag-%02d" % (g % TAG_POOL)]
            if g % 2 == 0:
                tags.append("tag-%02d" % ((g * 7 + 3) % TAG_POOL))
            tags = sorted(set(tags))
            items.append({"k": g, "space": sp, "i": i, "folder": ordner if i < ordner_n else "",
                          "tags": tags, "links": []})
            g += 1
    index = {(it["space"], it["i"]): it["k"] for it in items}
    for it in items:
        n = ANZAHL[it["space"]]
        if n > 1 and it["i"] % 4 == 0:
            it["links"].append(index[(it["space"], (it["i"] + 1) % n)])
        if it["space"] != "epsilon" and it["i"] % 10 == 0:
            nxt = SPACES[(SPACES.index(it["space"]) + 1) % (len(SPACES) - 1)]   # nie epsilon
            it["links"].append(index[(nxt, it["i"] % ANZAHL[nxt])])
    return items


def erwartet(items: list[dict]) -> dict:
    """Spiegel von `buildTagEdges`/`buildFolderEdges`/`rebuildImplicitEdges` (Stern, Block 18.1) --
    aus der Saat. Die Mitte einer Gruppe ist ihr Item mit dem groessten `k` (= `updated`)."""
    def key(a, b):
        return (a, b) if a < b else (b, a)

    explizit = {key(it["k"], z) for it in items for z in it["links"] if z != it["k"]}
    je_tag: dict = {}
    for it in items:
        for t in it["tags"]:
            je_tag.setdefault(t, []).append(it["k"])
    tag_kanten, gesehen = [], set()
    for t, ids in je_tag.items():
        if len(ids) > TAG_CLIQUE_LIMIT:
            continue
        hub = max(ids)
        for k_ in ids:
            if k_ == hub:
                continue
            k = key(hub, k_)
            if k in gesehen:
                continue
            gesehen.add(k)
            tag_kanten.append(k)
    je_ordner: dict = {}
    for it in items:
        if it["folder"]:
            je_ordner.setdefault((it["space"], it["folder"]), []).append(it["k"])
    ordner_kanten = [key(max(ids), k_) for ids in je_ordner.values() if len(ids) >= 2
                     for k_ in ids if k_ != max(ids)]

    def implizit(*listen):
        # (Art, Paar) -- wie der Seitenhaken sie liefert; eine explizite Kante streicht die implizite
        return sorted("%s:%d-%d" % (art, a, b)
                      for art, liste in listen for (a, b) in liste if (a, b) not in explizit)

    zustaende = {
        "aus": [],
        "tags": implizit(("tag", tag_kanten)),
        "ordner": implizit(("folder", ordner_kanten)),
        "beide": implizit(("tag", tag_kanten), ("folder", ordner_kanten)),
    }
    return {
        "explizit": len(explizit),
        "tag_kanten": len(tag_kanten),
        "ordner_kanten": len(ordner_kanten),
        "tags_gesamt": len(je_tag),
        "tags_ueber_limit": len([t for t, ids in je_tag.items() if len(ids) > TAG_CLIQUE_LIMIT]),
        "tag_max_knoten": max(len(v) for v in je_tag.values()),
        "implizit": {z: len(v) for z, v in zustaende.items()},
        "paare": zustaende,
    }


def seed(items: list[dict]) -> None:
    """Die Saat auf die Platte (Muster `p105_b14_layout_probe.py :: _seed`, feste IDs, feste Uhr)."""
    import shutil
    shutil.rmtree(b14.DATA_ROOT, ignore_errors=True)
    b14.DATA_ROOT.mkdir(parents=True, exist_ok=True)
    code = (
        "import sys, json; sys.path.insert(0, 'phase1_storage')\n"
        "from pathlib import Path\n"
        "from datetime import datetime, timezone\n"
        "import storage.files as sfiles\n"
        "from storage.store import Store\n"
        "from storage.acl import create_space, add_member\n"
        "_z = [0]\n"
        "def _feste_id():\n"
        "    _z[0] += 1\n"
        "    return 'itm_%08x' % _z[0]\n"
        "sfiles.generate_id = _feste_id\n"
        f"root = Path({str(b14.DATA_ROOT)!r})\n"
        f"spaces = {SPACES!r}\n"
        f"items = json.loads({json.dumps(json.dumps(items))})\n"
        "for sp in spaces: create_space(root, sp)\n"
        "for sp in spaces[1:]: add_member(root, sp, 'alpha', write=True)\n"
        # **Die Uhr laeuft je Item eine Sekunde weiter** (Block 18.1): der Stern haengt am zuletzt
        # geaenderten Item, `updated` ist auf die Sekunde genau -- gleiche Zeitstempel waeren lauter
        # Gleichstaende, und die Probe prueft die Wahl der Mitte nicht. Item k hat `updated` = k s.
        "tick = [0]\n"
        "s = Store(root, git=False,\n"
        "          now_fn=lambda: datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)\n"
        "                         + __import__('datetime').timedelta(seconds=tick[0]))\n"
        "def _id(k): return 'itm_%08x' % (k + 1)      # die festen IDs: Item k hat die ID k + 1\n"
        "for it in items:\n"
        "    tick[0] = it['k']\n"
        "    kw = dict(type='task' if it['k'] % 3 == 0 else 'note',\n"
        "              title='%s %03d' % (it['space'].title(), it['i'] + 1), tags=it['tags'],\n"
        "              links=[_id(z) for z in dict.fromkeys(it['links'])])\n"
        "    if kw['type'] == 'task': kw['status'] = 'open'\n"
        "    if it['folder']: kw['folder'] = it['folder']\n"
        "    made = s.create(it['space'], **kw)\n"
        "    assert made.id == _id(it['k']), (made.id, it['k'])\n"
        "s.rebuild_index()\n"
        "print('geseedet:', len(items))\n"
    )
    subprocess.run([".venv/bin/python", "-c", code], check=True, cwd=str(REPO_ROOT),
                   env={**b14._saubere_umgebung(), "PYTHONPATH": str(REPO_ROOT / "phase1_storage")})


# -- Aufruf: Beleg-Datei und Gegenlaeufe ---------------------------------------------------------
# `--out=NAME` schreibt `p105_b18_NAME.json` (der Beleg von 18.0 heisst `basislinie` und bleibt
# unangetastet). `--gegenlauf=NAME` bricht **eine** Regel in der Kopie von `graph.js` und schreibt in
# `p105_b18_gegenlauf_NAME.json` -- ein Gegenlauf darf nie einen Normalfall-Beleg ueberschreiben.
# Jeder Gegenlauf muss **genau die** zugehoerige Zelle rot machen (Memory: ehrliche Gegenlaeufe).
#
# | Gegenlauf | Regel | Zelle | der Fehler |
# |---|---|---|---|
# | `clique` | 18.1 (a) -- Ordner/Tags sind ein **Stern** | `kanten` | die Gruppe wird wieder zur Clique |
# | `tritt` | 18.2b -- die Abstossung hat eine **Mindestdistanz** | `insel` | `dist2` ohne Untergrenze (= HEAD von 18.2) |
# | `kein_schutz` | 18.2/18.2b -- Mindestdistanz **und** `MAX_SPEED` | `schleuder` **und** `insel` | beide Gurte aus (zwei Zellen -- ehrlich benannt) |
# | `schleuder` | 18.2 -- `MAX_SPEED` allein | **keine** (zahnlos unter der Mindestdistanz, Addon Insel §4.4) | die Grenze ist aus |
# | `veraltet` | 18.3 V1 -- die Signatur **kennt die Positionen** | `zwischenspeicher` | nach einem Drag bleibt das alte Bild |
# | `ohne_speicher` | 18.3 V1 -- der Zwischenspeicher wird **gebaut** | `bildzeit_ruhe` | nie gebaut: jedes Pan-Bild direkt |
# | `ein_schritt` | 18.3 V3 -- **zwei** Schritte je Bild | `sim_dauer` | ein Schritt je Bild (129 Bilder) |
# | `v4_aus` | 18.3 V4 -- geschlossene Luecke **durchgezogen** | `strichbild` | volle Strichelung trotz geschlossener Luecke |
# (18.1 (b), Kanten je Stil **buendeln**, ist gemessen und **verworfen**: mit dem Buendel waren die Kanten bei
# 480 + 93 Kanten **langsamer** (37,6 statt 29,1 ms) -- der Wert steht in `p105_b18_gegenlauf_buendel.json`)
# | `schleuder` | 18.2 (N1) -- die Geschwindigkeit ist **begrenzt** | `schleuder` | die Grenze ist aus |
# (die Anker der Gegenlaeufe 18.2 stehen in `GEGENLAEUFE18`, sobald die Regel im Code steht)
GEGENLAEUFE18: dict = {
    "clique": {
        "function starEdges(group, kind, seen, edges) {\n  var hub = starHub(group);":
            "function starEdges(group, kind, seen, edges) {\n"
            "  for (var a = 0; a < group.length; a++) for (var b = a + 1; b < group.length; b++)\n"
            "    edges.push({ src: group[a].id, dst: group[b].id, kind: kind });\n"
            "  return;  // Gegenlauf: die Clique\n  var hub = starHub(group);",
    },
    # 18.2 (N1): `MAX_SPEED` allein. **Unter der Mindestdistanz (18.2b) zahnlos** -- die Grenze greift auf
    # keiner gemessenen Saat mehr (Spitze <= 326 px/Bild, Addon Insel §4.4); der Beleg zeigt das (Zelle bleibt gruen).
    "schleuder": {
        "const MAX_SPEED = 600;": "const MAX_SPEED = 1e9;   // Gegenlauf: keine Grenze",
    },
    # 18.2b: die Mindestdistanz der Abstossung (Addon Insel) -- ohne sie ist HEAD von 18.2: der Einzelpunkt-Tritt
    "tritt": {
        "      var dist2 = Math.max(dx * dx + dy * dy + 0.01, REPULSION_MIN_DIST * REPULSION_MIN_DIST);":
            "      var dist2 = dx * dx + dy * dy + 0.01;   // Gegenlauf: keine Mindestdistanz",
    },
    # beide Gurte aus: die Schleuder (N1) kehrt zurueck -- `schleuder` UND `insel` werden rot
    "kein_schutz": {
        "      var dist2 = Math.max(dx * dx + dy * dy + 0.01, REPULSION_MIN_DIST * REPULSION_MIN_DIST);":
            "      var dist2 = dx * dx + dy * dy + 0.01;   // Gegenlauf: keine Mindestdistanz",
        "const MAX_SPEED = 600;": "const MAX_SPEED = 1e9;   // Gegenlauf: keine Grenze",
    },
    # 18.3 V1: die Signatur kennt die Knotenpositionen nicht -- nach einem Drag steht ein **veraltetes** Bild
    "veraltet": {
        "    h = Math.imul(h ^ Math.round(n.x * 8), 16777619);\n    h = Math.imul(h ^ Math.round(n.y * 8), 16777619);\n": "",
    },
    # 18.3 V1: der Zwischenspeicher wird nie gebaut
    "ohne_speicher": {
        "    layer = buildLayer(shown);\n    if (!layer) return false;":
            "    layer = null;\n    return false;   // Gegenlauf: nie bauen",
    },
    # 18.3 V3: ein Simulationsschritt je Bild
    "ein_schritt": {
        "const SIM_STEPS_PER_FRAME = 2;": "const SIM_STEPS_PER_FRAME = 1;",
    },
    # 18.3 V4: die geschlossene Luecke bekommt wieder die volle Strichelung
    "v4_aus": {
        "    if (dash && dash[1] <= edgeWidth) dash = null;": "    // Gegenlauf: V4 aus",
    },
}
ARGS = {a.split("=", 1)[0]: (a.split("=", 1)[1] if "=" in a else "1") for a in _argv[1:]}
GEGENLAUF = ARGS.get("--gegenlauf")
if GEGENLAUF is not None and GEGENLAUF not in GEGENLAEUFE18:
    raise SystemExit("unbekannter Gegenlauf: %s (bekannt: %s)" % (GEGENLAUF, ", ".join(sorted(GEGENLAEUFE18))))
DPR = int(ARGS.get("--dpr", "1"))      # Geraetedichte des Browsers (Retina = 2)
if GEGENLAUF:
    RESULT = HIER / ("p105_b18_gegenlauf_%s.json" % GEGENLAUF)
elif ARGS.get("--out"):
    RESULT = HIER / ("p105_b18_%s.json" % ARGS["--out"])
elif DPR != 1:
    RESULT = HIER / ("p105_b18_karte_messung_dpr%d.json" % DPR)


# -- das Messpflaster ---------------------------------------------------------------------------
# Haengt eine Hilfsschnittstelle an eine **Kopie** von `graph.js` (Anker: die erste Zeile von
# `fitView()`, eindeutig). Der Patch aendert **keine** Regel -- er legt nur offen, was die Karte
# im Inneren hat, und ruft vorhandene Funktionen auf.
BODY_ANKER = "  return { key: lobeKey(shown), lobes: lobes };"
BODY_NEU = ("  globalThis.__body = { koerper: koerper, spaceOf: spaceOf, furrow: furrow, cols: cols, rows: rows, cell: cell, minX: minX, minY: minY };\n"
            "  return { key: lobeKey(shown), lobes: lobes };")
PFLASTER_ANKER = "function fitView() {\n"
PFLASTER = """globalThis.__sfx18 = {
  draw: function () { draw(); },
  setHover: function (id) { hoverId = id; },
  flush: function () { return ctx.getImageData(0, 0, 1, 1).data[0]; },
  edges: function () { return {explicit: explicitEdges.length, implicit: implicitEdges.length}; },
  implicitList: function () {      // "Art:k1-k2" -- k = laufende Nummer der Saat (ID = k + 1)
    return implicitEdges.map(function (e) {
      var x = parseInt(e.src.slice(4), 16) - 1, y = parseInt(e.dst.slice(4), 16) - 1;
      return e.kind + ":" + Math.min(x, y) + "-" + Math.max(x, y);
    }).sort();
  },
  hub: function () {
    var best = null;
    for (var i = 0; i < nodes.length; i++) if (!best || nodes[i].deg > best.deg) best = nodes[i];
    return best ? best.id : null;
  },
  forces: function () { applyForces(1e-9); },   // alpha ~ 0: rechnet alles, bewegt (fast) nichts
  rings: function (id) { return neighborRings(id, explicitEdges.concat(implicitEdges)); },
  edgesOnly: function () {
    ctx.save(); ctx.translate(panX, panY); ctx.scale(zoom, zoom);
    drawEdges(explicitEdges.concat(implicitEdges), null, visibleNodes());
    ctx.restore();
  },
  edgesNoDash: function () {     // Zerlegung: dieselben Kanten, **ohne** Strichelung
    var o = ctx.setLineDash;
    ctx.setLineDash = function () { o.call(ctx, []); };
    try { globalThis.__sfx18.edgesOnly(); } finally { ctx.setLineDash = o; }
  },
  drawNoDash: function () {      // das **ganze** Bild ohne Strichelung (Option fuer den Nikinger)
    var o = ctx.setLineDash;
    ctx.setLineDash = function () { o.call(ctx, []); };
    try { draw(); } finally { ctx.setLineDash = o; }
  },
  edgesLongDash: function () {   // Zerlegung: Striche **3 x laenger** (weniger Striche je Strecke)
    var o = ctx.setLineDash;
    ctx.setLineDash = function (a) { o.call(ctx, a.map(function (x) { return x * 3; })); };
    try { globalThis.__sfx18.edgesOnly(); } finally { ctx.setLineDash = o; }
  },
  implicitLength: function () {   // Summe der Sehnenlaengen der impliziten Kanten (Welt-px)
    var sum = 0;
    for (var i = 0; i < implicitEdges.length; i++) {
      var a = nodeById[implicitEdges[i].src], b = nodeById[implicitEdges[i].dst];
      if (a && b) sum += Math.sqrt((a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y));
    }
    return sum;
  },
  layerStats: function () { return {builds: layerStats.builds, hits: layerStats.hits, direct: layerStats.direct}; },
  layerDrop: function () { layer = null; layerKeySeen = null; },
  setView: function (z, px, py) { zoom = z; panX = px; panY = py; },
  moveNode: function (id, dx, dy) { var n = nodeById[id]; n.x += dx; n.y += dy; },   // wie ein Drag: Lappen bleiben stehen
  recomputeLobes: function () { lobeCache = computeLobes(visibleNodes()); },
  snap: function () { globalThis.__snap = ctx.getImageData(0, 0, canvasEl.width, canvasEl.height).data; },
  diff: function () {
    var d = ctx.getImageData(0, 0, canvasEl.width, canvasEl.height).data, s = globalThis.__snap, n = 0;
    for (var i = 0; i < d.length; i += 4) {
      if (d[i] !== s[i] || d[i + 1] !== s[i + 1] || d[i + 2] !== s[i + 2] || d[i + 3] !== s[i + 3]) n++;
    }
    return n;
  },
  dashAudit: function () {          // Strichbild (V4): hat **jede** Kante das Muster, das die Regel verlangt?
    var calls = [];
    var o = ctx.setLineDash;
    ctx.setLineDash = function (p) { calls.push(p.length); o.call(ctx, p); };
    try { globalThis.__sfx18.edgesOnly(); } finally { ctx.setLineDash = o; }
    calls.pop();                     // der Abschluss `setLineDash([])` nach der Schleife
    var shown = visibleNodes(), all = explicitEdges.concat(implicitEdges);
    var idx = 0, viol = 0, dashed = 0, closed = 0, solid = 0;
    for (var i = 0; i < all.length; i++) {
      var a = nodeById[all[i].src], b = nodeById[all[i].dst];
      if (!a || !b || !shown[a.id] || !shown[b.id]) continue;
      var w = EDGE_WIDTH_BASE + Math.log2(1 + Math.min(a.deg, b.deg));
      var gap = all[i].kind === "tag" ? DASH_TAG[1] : (all[i].kind === "folder" ? DASH_FOLDER[1] : 0);
      var expectDash = gap > 0 && gap > w;
      var gotDash = calls[idx++] > 0;
      if (gotDash !== expectDash) viol++;
      if (gotDash) dashed++; else solid++;
      if (gap > 0 && !expectDash) closed++;
    }
    return {kanten: idx, gestrichelt: dashed, durchgezogen: solid, geschlossene_luecke: closed,
            verstoesse: viol, aufrufe: calls.length};
  },
  positions: function () {
    return nodes.map(function (n) { return [n.id, n.x, n.y, n.space, n.deg]; });
  },
  regions: function () {
    if (!spaceRegions) return null;
    var out = {};
    Object.keys(spaceRegions.spaces).forEach(function (k) {
      var s = spaceRegions.spaces[k];
      out[k] = {x: s.x, y: s.y, radius: s.radius};
    });
    return {order: spaceRegions.order, spaces: out};
  },
  lobes: function () {
    if (!lobeCache) return null;
    return lobeCache.lobes.map(function (l) { return {space: l.space, outer: l.outer}; });
  },
  view: function () { return {zoom: zoom, panX: panX, panY: panY, cssWidth: cssWidth, cssHeight: cssHeight}; },
};
globalThis.__sfx18trace = [];
globalThis.__insel = function () {       // die Koerpermaske: genau **eine** Komponente? (Addon Insel §5)
  var B = globalThis.__body; if (!B) return null;
  var cols = B.cols, rows = B.rows, lab = new Int32Array(cols * rows).fill(-1), n = 0, st = [];
  for (var s = 0; s < cols * rows; s++) {
    if (lab[s] >= 0 || B.koerper[s] !== 1) continue;
    lab[s] = n; st.push(s);
    while (st.length) { var c = st.pop(), x = c % cols, y = (c / cols) | 0;
      var nb = [[x - 1, y], [x + 1, y], [x, y - 1], [x, y + 1]];
      for (var q = 0; q < 4; q++) { var nx = nb[q][0], ny = nb[q][1];
        if (nx < 0 || ny < 0 || nx >= cols || ny >= rows) continue;
        var k = ny * cols + nx; if (lab[k] < 0 && B.koerper[k] === 1) { lab[k] = n; st.push(k); } } }
    n++;
  }
  var comp = nodes.map(function (nd) { return lab[Math.floor((nd.y - B.minY) / B.cell) * cols + Math.floor((nd.x - B.minX) / B.cell)]; });
  var cnt = {}; comp.forEach(function (c) { cnt[c] = (cnt[c] || 0) + 1; });
  var main = Object.keys(cnt).sort(function (a, b) { return cnt[b] - cnt[a]; })[0] | 0;
  var isles = {};
  nodes.forEach(function (nd, i) { if (comp[i] === main) return;
    var g = Infinity; nodes.forEach(function (m, j) { if (comp[j] === main) g = Math.min(g, Math.hypot(nd.x - m.x, nd.y - m.y)); });
    var I = isles[comp[i]] = isles[comp[i]] || {n: 0, gap: Infinity, ids: []};
    I.n++; I.gap = Math.min(I.gap, g); I.ids.push(nd.id); });
  return {body: n, isles: Object.keys(isles).map(function (k) { return isles[k]; }).sort(function (a, b) { return b.gap - a.gap; })};
};

var __integrate18 = integrate;
integrate = function (alpha) {      // Messpflaster: ruft die echte Funktion, notiert danach nur mit
  __integrate18(alpha);
  var mv = 0, far = 0, fid = null;
  for (var i = 0; i < nodes.length; i++) {
    var n = nodes[i];
    var s = Math.sqrt(n.vx * n.vx + n.vy * n.vy);
    if (s > mv) mv = s;
    var d = Math.sqrt(n.x * n.x + n.y * n.y);
    if (d > far) { far = d; fid = n.id; }
  }
  globalThis.__sfx18trace.push([alpha, mv, far, fid]);
};
function fitView() {
"""


# -- der Browser-Teil -----------------------------------------------------------------------------
BROWSER_MAIN = r'''

# ===== Block 18, Schritt 18.0: die Messung (haengt an den Hilfen der Block-14-Probe) ==============

ZEIT = r"""(n) => {
  const h = globalThis.__sfx18;
  const out = {};
  // **Pro Bild ein Flush** (`getImageData`): jedes `draw()` beginnt mit `clearRect` -- ohne Flush
  // verwirft Chromium die noch nicht gerasterten Befehle der vorigen Bilder, und die Messung
  // zaehlt nur das letzte (gemessen: 9,9 ms ohne, siehe Beleg-Vorlauf). Der Flush erzwingt das
  // Rastern, wie es ein sichtbares Bild braucht.
  const zeit = (f) => { f(); h.flush(); const t0 = performance.now();
                        for (let i = 0; i < n; i++) { f(); h.flush(); }
                        return (performance.now() - t0) / n; };
  h.setHover(null);
  h.layerDrop(); h.draw(); h.draw(); h.draw();           // direkt, Bau, Treffer
  out.draw_ms = zeit(() => h.draw());                    // Ruhe: der Zwischenspeicher (V1)
  const v0 = h.view();
  out.pan_ms = zeit(() => { const v = h.view(); h.setView(v.zoom, v.panX + 1, v.panY); h.draw(); });
  h.setView(v0.zoom, v0.panX, v0.panY);
  out.stats_nach_pan = h.layerStats();
  out.draw_direkt_ms = zeit(() => { h.layerDrop(); h.draw(); });   // das Bild **mit** Signaturwechsel: wie vor V1
  h.draw(); h.draw();
  out.draw_nur_kanten_ms = zeit(() => h.edgesOnly());
  out.kanten_ohne_strichelung_ms = zeit(() => h.edgesNoDash());
  out.kanten_lange_striche_ms = zeit(() => h.edgesLongDash());
  out.implizite_laenge_px = h.implicitLength();
  const hub = h.hub();
  out.hub = hub;
  h.setHover(hub);
  out.draw_hover_ms = zeit(() => h.draw());
  const t0 = performance.now();
  for (let i = 0; i < n; i++) h.rings(hub);
  out.ringe_ms = (performance.now() - t0) / n;
  h.setHover(null);
  const tf = performance.now();
  for (let i = 0; i < 5; i++) h.forces();
  out.kraefte_ms = (performance.now() - tf) / 5;
  h.draw();
  out.kanten = h.edges();
  return out;
}"""

ZWISCHEN = r"""() => {
  const h = globalThis.__sfx18;
  const out = [];
  const frames = () => { h.draw(); h.draw(); h.draw(); };      // direkt, Bau, Treffer
  const pruefe = (name) => {
    h.setHover(null); frames(); h.snap();                      // A: das Bild, das der Nutzer sieht
    const s = h.layerStats();
    h.layerDrop(); h.draw(); h.draw();                         // B: frisch gebauter Zwischenspeicher
    out.push({name: name, abweichende_pixel: h.diff(), treffer: s.hits});
  };
  const ansicht = h.view();
  pruefe('ruhe');
  h.setView(ansicht.zoom, ansicht.panX + 37, ansicht.panY - 21); pruefe('pan');
  h.setView(ansicht.zoom * 0.8, ansicht.panX + 37, ansicht.panY - 21); pruefe('zoom');
  const hub = h.hub();
  h.moveNode(hub, 60, -40); pruefe('drag');                    // wie ein Drag: die Lappen bleiben stehen
  h.recomputeLobes(); pruefe('drag_ende');                     // Drag-Ende: die Lappen werden neu berechnet
  const set = (id, v) => { const el = document.getElementById(id); el.checked = v; el.dispatchEvent(new Event('change', {bubbles: true})); };
  set('overview-graph-toggle-tags', false); pruefe('schalter_tags');
  set('overview-graph-toggle-folders', false); pruefe('schalter_ordner');
  const sel = document.getElementById('overview-graph-filter-type');
  if (sel && sel.options.length > 1) { sel.value = sel.options[1].value; sel.dispatchEvent(new Event('change', {bubbles: true})); pruefe('filter'); }
  return out;
}"""

ZUSTAND = r"""(a) => {
  const set = (id, v) => { const el = document.getElementById(id);
                           if (el.checked !== v) { el.checked = v; el.dispatchEvent(new Event('change', {bubbles: true})); } };
  set('overview-graph-toggle-tags', a.tags);
  set('overview-graph-toggle-folders', a.ordner);
}"""


def zustand(page, tags, ordner):
    page.evaluate(ZUSTAND, {"tags": tags, "ordner": ordner})
    page.wait_for_timeout(200)


def simulation(page):
    """'Layout zuruecksetzen' -> die Simulation laeuft neu; Dauer = erster bis letzter Frame.
    Dazu die **Spur** (Hook um `integrate()`): hoechste Geschwindigkeit, groesster Schritt und wann
    ein Knoten weiter als 1500 px vom Ursprung steht (N1, Plan §5.3)."""
    page.evaluate("() => { window.__rafLog.count = 0; window.__rafLog.stamps.length = 0;"
                  " globalThis.__sfx18trace.length = 0; }")
    page.click("#overview-graph-reset-layout")
    settle(page)
    st = page.evaluate("() => window.__rafLog.stamps")
    spur = page.evaluate("() => globalThis.__sfx18trace")
    ivs = [b - a for a, b in zip(st, st[1:])]
    erste = next((i for i, s in enumerate(spur) if s[2] > 1500), None)
    schnellste = max(range(len(spur)), key=lambda i: spur[i][1]) if spur else None
    return {"frames": len(st), "dauer_ms": (st[-1] - st[0]) if len(st) > 1 else 0.0,
            "intervall_mittel_ms": (sum(ivs) / len(ivs)) if ivs else 0.0,
            "intervall_max_ms": max(ivs) if ivs else 0.0,
            "spur": {"ticks": len(spur),
                     "hoechste_geschwindigkeit_px_pro_tick": spur[schnellste][1] if spur else None,
                     "schnellster_tick": schnellste,
                     "groesster_schritt_px": max((s[0] * s[1] for s in spur), default=None),
                     "erster_tick_ueber_1500px_vom_ursprung": erste,
                     "weitester_abstand_vom_ursprung_am_ende_px": spur[-1][2] if spur else None,
                     "abstand_je_10_ticks": [round(spur[i][2]) for i in range(0, len(spur), 10)]}}


def geometrie(page, fit_margin, zoom_min, region_gap):
    """Wo steht jeder Space, wie weit draussen sitzt der kleinste, was macht er mit dem Zoom?"""
    pos = page.evaluate("() => globalThis.__sfx18.positions()")
    ansicht = page.evaluate("() => globalThis.__sfx18.view()")
    zoom_readout = page.evaluate(ZOOM)
    je_raum = {}
    for nid, x, y, sp, deg in pos:
        je_raum.setdefault(sp, []).append((nid, x, y))

    def abstand(p, q):
        return ((p[1] - q[1]) ** 2 + (p[2] - q[2]) ** 2) ** 0.5

    luecke = {}   # kleinster Knotenabstand zu irgendeinem Knoten eines anderen Space
    for sp, liste in je_raum.items():
        best = None
        for p in liste:
            for sp2, liste2 in je_raum.items():
                if sp2 == sp:
                    continue
                for q in liste2:
                    d = abstand(p, q)
                    if best is None or d < best:
                        best = d
        luecke[sp] = best

    def zoom_fuer(punkte):
        xs = [p[1] for p in punkte]
        ys = [p[2] for p in punkte]
        bw = (max(xs) - min(xs)) + fit_margin * 2
        bh = (max(ys) - min(ys)) + fit_margin * 2
        z = min(ansicht["cssWidth"] / bw, ansicht["cssHeight"] / bh)
        return max(zoom_min, min(1.0, z)), (max(xs) - min(xs), max(ys) - min(ys))

    alle = [p for liste in je_raum.values() for p in liste]
    ohne = [p for sp, liste in je_raum.items() if sp != "epsilon" for p in liste]
    z_alle, box_alle = zoom_fuer(alle)
    z_ohne, box_ohne = zoom_fuer(ohne)
    # die drei am weitesten vom Median-Mittelpunkt entfernten Knoten (A2: ein Ausreisser
    # druckt den Zoom) und der Zoom, den die Karte OHNE sie haette
    xs_s = sorted(p[1] for p in alle)
    ys_s = sorted(p[2] for p in alle)
    mx, my = xs_s[len(xs_s) // 2], ys_s[len(ys_s) // 2]
    deg = {n[0]: n[4] for n in pos}
    raum_von = {n[0]: n[3] for n in pos}
    fern = sorted(alle, key=lambda p: -abstand(p, (None, mx, my)))
    weiteste = [{"id": p[0], "space": raum_von[p[0]], "deg": deg[p[0]],
                 "abstand_vom_median_px": round(abstand(p, (None, mx, my)), 1)} for p in fern[:3]]
    z_ohne3, box_ohne3 = zoom_fuer(fern[3:])
    # Abstand zum naechsten **Umriss** eines anderen Space (der Massstab von Plan 18.2)
    lobes = page.evaluate("() => globalThis.__sfx18.lobes()") or []
    je_umriss = {}
    for l in lobes:
        # `outer` ist ein Ring [[x, y], ...] **oder** eine Liste von Ringen -- beides flachdruecken
        ringe = l["outer"] if l["outer"] and isinstance(l["outer"][0][0], list) else [l["outer"]]
        for ring in ringe:
            je_umriss.setdefault(l["space"], []).extend(ring)
    umriss_luecke = {}
    for sp, liste in je_raum.items():
        best = None
        for p in liste:
            for sp2, kontur in je_umriss.items():
                if sp2 == sp:
                    continue
                for q in kontur:
                    d = ((p[1] - q[0]) ** 2 + (p[2] - q[1]) ** 2) ** 0.5
                    if best is None or d < best:
                        best = d
        umriss_luecke[sp] = best
    return {
        "luecke_zum_naechsten_fremden_knoten_px": luecke,
        "luecke_zum_naechsten_fremden_umriss_px": umriss_luecke,
        "ausreisser_umriss_luecke_px": umriss_luecke.get("epsilon"),
        "ausreisser_umriss_luecke_in_region_gap": (umriss_luecke.get("epsilon") or 0) / region_gap,
        "weiteste_knoten": weiteste,
        "zoom_ohne_die_3_weitesten_nachgerechnet": z_ohne3,
        "welt_ohne_die_3_weitesten_px": box_ohne3,
        "ausreisser_luecke_px": luecke.get("epsilon"),
        "ausreisser_luecke_in_region_gap": (luecke.get("epsilon") or 0) / region_gap,
        "zoom_anzeige": zoom_readout,
        "zoom_aus_fitview_nachgerechnet": z_alle,
        "zoom_ohne_ausreisser_nachgerechnet": z_ohne,
        "welt_mit_ausreisser_px": box_alle,
        "welt_ohne_ausreisser_px": box_ohne,
        "regionen": page.evaluate("() => globalThis.__sfx18.regions()"),
    }


def main():
    fehler = []
    text = (Path(AUFTRAG["repo_root"]) / "phase5_ui/webui/static/js/graph.js").read_text(encoding="utf-8")
    konst = {n: float(re.search(r"^const %s = ([0-9.]+);" % n, text, re.M).group(1))
             for n in ("FIT_MARGIN", "ZOOM_MIN", "REGION_GAP", "REGION_ITEM_STEP", "REGION_PAD", "TAG_CLIQUE_LIMIT")}
    out = {"konstanten": konst, "zustaende": {}}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1920, "height": 1200}, ignore_https_errors=True,
                                  device_scale_factor=AUFTRAG.get("dpr", 1))
        page = ctx.new_page()
        page.add_init_script("localStorage.setItem('sfx:film:gesehen','4.0.0')")
        page.add_init_script(RAF_PROBE)
        page.on("pageerror", lambda e: fehler.append(str(e)))
        login(page)
        out["browser"] = {"version": browser.version, "user_agent": page.evaluate("() => navigator.userAgent"),
                          "viewport": "1920x1200", "kopfloser_chromium": True, "dpr": AUFTRAG.get("dpr", 1)}
        # Basislauf: leere Ablage, alles aus -> der Ausreisser-Zustand der Wegwerf-Instanz (A1)
        lauf = frischer_lauf(page)
        out["pinned_beim_start"] = lauf["pinned_beim_start"]
        out["knoten"] = len(lauf["grafik"]["nodes"])
        zustaende = [("aus", False, False), ("tags", True, False), ("ordner", False, True), ("beide", True, True)]
        for name, tags, ordner in zustaende:
            zustand(page, tags, ordner)
            sim = simulation(page)
            page.wait_for_timeout(400)
            messung = page.evaluate(ZEIT, AUFTRAG["n_bilder"])
            geo = geometrie(page, konst["FIT_MARGIN"], konst["ZOOM_MIN"], konst["REGION_GAP"])
            paare = page.evaluate("() => globalThis.__sfx18.implicitList()")
            messung["paare_sha256"] = hashlib.sha256("\n".join(paare).encode()).hexdigest()
            ins = page.evaluate("() => globalThis.__insel()")
            geo["koerper_komponenten"] = ins["body"] if ins else None
            geo["inseln"] = ins["isles"] if ins else None
            out["zustaende"][name] = {"simulation": sim, "draw": messung, "geometrie": geo}
            if AUFTRAG.get("bilder_dir"):
                page.locator("#overview-graph-canvas").screenshot(
                    path=str(Path(AUFTRAG["bilder_dir"]) / ("b18_1_%s.png" % name)))
                if name == "beide":
                    page.evaluate("() => globalThis.__sfx18.drawNoDash()")
                    page.locator("#overview-graph-canvas").screenshot(
                        path=str(Path(AUFTRAG["bilder_dir"]) / "b18_1_beide_ohne_strichelung.png"))
                    page.evaluate("() => globalThis.__sfx18.draw()")
        # V1: ist der Zwischenspeicher nach jedem Ausloeser **gleich** einem frisch gebauten? (Zustand "beide")
        zustand(page, True, True)
        simulation(page)
        page.wait_for_timeout(400)
        out["strichbild"] = page.evaluate("() => globalThis.__sfx18.dashAudit()")
        out["zwischenspeicher"] = page.evaluate(ZWISCHEN)
        # A3-Gegenprobe: 'Layout zuruecksetzen' auf der frischen Instanz aendert die Karte nicht
        # (es gibt dort keine gemerkte Ablage) -- die Ursache A3 laesst sich hier NICHT zeigen.
        out["fehler_in_der_seite"] = fehler
        browser.close()
    Path(AUFTRAG["result"]).write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({z: {"edges": v["draw"]["kanten"], "draw_ms": round(v["draw"]["draw_ms"], 2),
                          "draw_hover_ms": round(v["draw"]["draw_hover_ms"], 2),
                          "kanten_ms": round(v["draw"]["draw_nur_kanten_ms"], 2),
                          "ohne_strichelung_ms": round(v["draw"]["kanten_ohne_strichelung_ms"], 2),
                          "laenge_px": round(v["draw"]["implizite_laenge_px"]),
                          "kraefte_ms": round(v["draw"]["kraefte_ms"], 2),
                          "ringe_ms": round(v["draw"]["ringe_ms"], 2),
                          "sim_ms": round(v["simulation"]["dauer_ms"]),
                          "frames": v["simulation"]["frames"],
                          "ausreisser_px": round(v["geometrie"]["ausreisser_luecke_px"] or 0),
                          "ausreisser_umriss_px": round(v["geometrie"]["ausreisser_umriss_luecke_px"] or 0),
                          "welt": [round(x) for x in v["geometrie"]["welt_mit_ausreisser_px"]],
                          "welt_ohne3": [round(x) for x in v["geometrie"]["welt_ohne_die_3_weitesten_px"]],
                          "weiteste": v["geometrie"]["weiteste_knoten"][0],
                          "zoom": v["geometrie"]["zoom_anzeige"]}
                      for z, v in out["zustaende"].items()}, indent=1))
    return 1 if fehler else 0


if __name__ == "__main__":
    raise SystemExit(main())
'''


def browser_skript() -> str:
    """Die Hilfen der Block-14-Probe (alles vor ihrem `main()`) + das eigene `main()`."""
    kopf = b14.BROWSER_SKILL.split("\ndef main():\n", 1)[0]
    return kopf + BROWSER_MAIN


def main() -> int:
    items = spec()
    soll = erwartet(items)
    if soll["tags_ueber_limit"]:
        print("WARNUNG: %d Tags ueber dem Limit -- die Saat bildet sie nicht ab" % soll["tags_ueber_limit"],
              file=sys.stderr)
    b14.PORT = b14._freier_port()
    b14.BASE = "https://127.0.0.1:%d" % b14.PORT
    creds = b14._setup()
    seed(items)
    b14.GRAPH_PATCH_EXTRA[PFLASTER_ANKER] = PFLASTER
    b14.GRAPH_PATCH_EXTRA[BODY_ANKER] = BODY_NEU
    if GEGENLAUF:
        b14.GRAPH_PATCH_EXTRA.update(GEGENLAEUFE18[GEGENLAUF])
    resultat = RESULT
    try:
        b14._serve()
        auftrag = {
            "base": b14.BASE, "space": b14.SPACE, "password": creds["password"], "secret": creds["secret"],
            "repo_root": str(REPO_ROOT), "auth_db": str(b14.AUTH_DB), "result": str(resultat),
            "wachser_space": "epsilon", "extra_items": 0, "pid": b14.PID, "spaces": SPACES,
            "n_bilder": 30, "bilder_dir": str(b14.WEGWERF_ROOT), "dpr": DPR,
        }
        b14.AUFTRAG_DATEI.write_text(json.dumps(auftrag), encoding="utf-8")
        skript = b14.WEGWERF_ROOT / ("browser18_%d.py" % b14.PID)
        skript.write_text(browser_skript(), encoding="utf-8")
        e2e = Path.home() / ".claude-code-tools/e2e-venv/bin/python"
        proc = subprocess.run([str(e2e), str(skript), str(b14.AUFTRAG_DATEI)], cwd=str(REPO_ROOT),
                              capture_output=True, text=True, timeout=1500)
        print(proc.stdout.strip()[-8000:])
        if proc.returncode != 0:
            print(proc.stderr.strip()[-6000:], file=sys.stderr)
            return 1
    finally:
        b14._stop()          # jeder Ausgang stoppt den Wegwerf-Server -- ueber die PID-Datei
    beleg = json.loads(resultat.read_text(encoding="utf-8"))
    beleg["saat"] = {"spaces": ANZAHL, "items": len(items), "grosse_ordner": GROSSER_ORDNER,
                     "tag_pool": TAG_POOL, "erwartet": {k: v for k, v in soll.items() if k != "paare"}}
    beleg["gegenlauf"] = GEGENLAUF
    for name, z in beleg["zustaende"].items():
        soll_hash = hashlib.sha256("\n".join(soll["paare"][name]).encode()).hexdigest()
        z["kanten_gegenrechnung"] = {
            "seite_implizit": z["draw"]["kanten"]["implicit"], "saat_implizit": soll["implizit"][name],
            "seite_explizit": z["draw"]["kanten"]["explicit"], "saat_explizit": soll["explizit"],
            "paare_gleich": z["draw"]["paare_sha256"] == soll_hash}
        z["kanten_gegenrechnung"]["ok"] = (
            z["kanten_gegenrechnung"]["seite_implizit"] == soll["implizit"][name]
            and z["kanten_gegenrechnung"]["seite_explizit"] == soll["explizit"]
            and z["kanten_gegenrechnung"]["paare_gleich"])
    zs = beleg["zustaende"]
    gap = beleg["konstanten"]["REGION_GAP"]
    beleg["zellen"] = {
        # 18.1: Kanten = Stern der Saat (Menge **und** Paare), Bildzeit "beide an" <= 16 ms
        "kanten": all(z["kanten_gegenrechnung"]["ok"] for z in zs.values()),
        # 18.3 V1/V3/V4 (Addon Render): Bildzeit in Ruhe/Pan <= 16,7 ms, Einschwingen <= 2,5 s, Strichbild, Cache gleich frisch
        "bildzeit_ruhe": zs["beide"]["draw"]["pan_ms"] <= 16.7,
        "sim_dauer": zs["beide"]["simulation"]["dauer_ms"] <= 2500,
        "zwischenspeicher": all(s["abweichende_pixel"] == 0 for s in beleg["zwischenspeicher"]),
        "strichbild": beleg["strichbild"]["verstoesse"] == 0 and beleg["strichbild"]["geschlossene_luecke"] > 0,
        # 18.2b (Addon Insel): die Koerpermaske ist in **jedem** Zustand genau eine Komponente
        "insel": all(z["geometrie"]["koerper_komponenten"] == 1 for z in zs.values()),
        # 18.2 (N1): kein Knoten weiter als 1300 px vom Median-Mittelpunkt (vorher 2790 im Tag-Zustand)
        "schleuder": all(z["geometrie"]["weiteste_knoten"][0]["abstand_vom_median_px"] <= 1300
                         for z in zs.values()),
        # 18.2 (A1): der Ein-Item-Space liegt <= 2 x REGION_GAP vom naechsten fremden Umriss
        "ausreisser": all((z["geometrie"]["ausreisser_umriss_luecke_px"] or 0) <= 2 * gap
                          for z in zs.values()),
    }
    # **Nur berichtet, keine Schwelle** (Addon Render §4 V2): der Hover-Wechsel kostet ein volles Bild
    beleg["info"] = {"hover_wechsel_ms": zs["beide"]["draw"]["draw_hover_ms"],
                     "bild_mit_signaturwechsel_ms": zs["beide"]["draw"]["draw_direkt_ms"],
                     "einschwingen_je_bild_ms": zs["beide"]["simulation"]["intervall_mittel_ms"]}
    resultat.write_text(json.dumps(beleg, indent=1, ensure_ascii=False), encoding="utf-8")
    print("Gegenrechnung der Kanten:",
          {n: z["kanten_gegenrechnung"]["ok"] for n, z in beleg["zustaende"].items()})
    print("ZELLEN:", beleg["zellen"], "| Gegenlauf:", GEGENLAUF)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
