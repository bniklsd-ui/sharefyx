// P10.5 Block 8 — Wächter-Harness für die Gehirnkarte C2 (Plan §Block 8, Schritt 8.1–8.7).
//
// **Was gemessen wird:** das echte `phase5_ui/webui/static/js/graph.js`, im Browser nicht
// nachgebaut, sondern in Node mit einem minimalen DOM-Shim geladen (Muster aus
// `phase9_hardening/scripts/graph_reload_probe.mjs`, dessen Shim hier um die neuen
// Zeichenbefehle erweitert ist: `quadraticCurveTo`, `closePath` und die Stile je Operation).
//
// Die Messung ist **schwarzkaestig**: der Harness sieht nur, was der Graph *zeichnet* —
// Lappenflaechen, Konturen, Bahnen, Zellen, Ringe, Beschriftungen. Kein internes Feld wird
// gelesen, es gibt keinen Testhaken im Produktivcode.
//
// **Gegenlauf:** `--gegenlauf <name>` patcht eine **Kopie** von `graph.js` (die Kopie liegt in
// `/tmp`, ihre Importe zeigen auf die echten Nachbarmodule) und muss dieselbe Messung **rot**
// machen. Ohne diesen Lauf beweist die grüne Messung nichts — die Fehlerklasse, die dieser
// Ordner zweimal gesehen hat ("ein Messgerät, das die falsche Sache misst, ist grün und
// falsch zugleich").
//
// Aufruf:  `node phase10_5_finishing/probes/p105_b8_c2_probe.mjs [--gegenlauf NAME]`
// Ergebnis: JSON auf stdout (der pytest-Wächter liest es).

import { fileURLToPath, pathToFileURL } from "node:url";
import path from "node:path";
import fs from "node:fs";
import os from "node:os";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.resolve(HERE, "../..");
const STATIC_DIR = path.join(REPO, "phase5_ui/webui/static/js");
const GRAPH_JS = path.join(STATIC_DIR, "graph.js");

// -- Argumente -----------------------------------------------------------------------------------

const args = process.argv.slice(2);
function argValue(name) {
  const i = args.indexOf(name);
  return i >= 0 && i + 1 < args.length ? args[i + 1] : null;
}
const gegenlauf = argValue("--gegenlauf");

// -- Die Gegenläufe: je einer ein eingebauter Fehler, der genau eine Messung rot macht ------
//
// **Die Anker sind eindeutig** (Regel + Nachbarzeile, nicht nur ein Wert): sonst patcht der
// Gegenlauf den Kommentar über der Regel statt der Regel — die erste Fassung der Probe
// p105_b7_sichtung hat genau diesen Fehler gemacht (dort stand `margin-right: .2em;` auch im
// Kommentar) und war danach grün, ohne dass der Defekt wiederhergestellt war.
const GEGENLAEUFE = {
  // Die Lappen fallen aus: die Karte zeigt nur noch Bahnen und Zellen.
  lappen: [
    ["  drawLobes(shown);", "  /* drawLobes(shown); */"],
  ],
  // Die Furche faellt aus: die Lappen zweier Spaces wachsen ineinander.
  furche: [
    ["      if (different) furrow[fi] = 1;", "      if (different) furrow[fi] = 0;"],
  ],
  // Die Bahnen werden gerade statt geschwungen.
  bahnen: [
    ["    ctx.quadraticCurveTo(geo.cx, geo.cy, b.x, b.y);",
     "    ctx.lineTo(b.x, b.y);"],
  ],
  // Die Fortsaetze der Zelle werden zufaellig statt deterministisch.
  zellen: [
    ["  var count = 2 + Math.floor(Math.abs(seedJitter(id, 20)) * 3);   // 2, 3 oder 4",
     "  var count = 2 + Math.floor(Math.random() * 3);   // 2, 3 oder 4"],
  ],
  // Die Abdunklung auf den P8-Wert 0,15 (D-1b: 0,45).
  aktivierung: [
    ["const DIM_ALPHA = 0.45;", "const DIM_ALPHA = 0.15;"],
  ],
  // Die gemerkte Position wird nicht festgehalten: die Karte "fliegt" beim Neuladen.
  layout: [
    ["      n.pinned = true;", "      n.pinned = false;"],
  ],
  // Der Filter laesst alles durch.
  filter: [
    ["    if (filterType && n.type !== filterType) continue;",
     "    if (false && filterType && n.type !== filterType) continue;"],
    ["    if (filterStatus && n.status !== filterStatus) continue;",
     "    if (false && filterStatus && n.status !== filterStatus) continue;"],
  ],
  // Der reduced-motion-Pfad laeuft wieder ueber requestAnimationFrame.
  reducedmotion: [
    ["    if (reducedMotion) {\n      resize();",
     "    if (false && reducedMotion) {\n      resize();"],
  ],
};

// -- Die Messpflaster: sie machen sichtbar, was die Regel tut (Verhalten unveraendert) ----------
//
// Die Zahl der **Furche-Zellen** ist der Gegenstand der Regel: ohne sie waere die Messung
// "die Lappen beruehren sich nicht" nur ein Abstand. Mit dem neuen Layout (Schritt 14.2)
// ruecken die Spaces auseinander und die Regel hat **keinen Gegenstand** mehr — die Zahl
// macht genau das sichtbar (siehe `FESTE_POSITIONEN`).
const MESS_PFLASTER = [
  ["return { key: lobeKey(shown), lobes: lobes };",
   "globalThis.__furrowCells = 0; for (var fi2 = 0; fi2 < furrow.length; fi2++) globalThis.__furrowCells += furrow[fi2]; return { key: lobeKey(shown), lobes: lobes };"],
];

// -- Die Kamera steht still (Schritt 14.3, 2026-10-26) --------------------------------------------
//
// **Dieselbe Art von Eingangs-Fixierung wie die festen Positionen** (siehe `FESTE_POSITIONEN`):
// diese Probe misst die **Zeichenregel** (Lappen, Furche, Bahnen, Zellen, Abdunklung) — nicht
// die Kamera. Seit 14.3 passt sich die Kamera nach dem Einschwingen ein (Zoom ≠ 100 %, Pan ≠
// 0), und der **Zeiger** der Probe (`mousemove` auf die Position eines Knotens) traegt den
// Knoten dann nicht mehr: die Weltposition ist nicht mehr die Bildschirmposition.
//
// **Die Kamera wird deshalb auf 100 % / Pan 0 festgenagelt** (`fitView()` ist aus). Die
// **Kamera selbst** misst der Browser-Waechter (`p105_b14_layout_probe.py`, Zelle `kamera`,
// Abnahme P10.5-67) — dort ist sie die Regel, hier ist sie nur der Bildausschnitt.
//
// Der Anker ist dieselbe Zeile wie im Gegenlauf `fitview` der Browser-Probe: fehlt sie, bricht
// die Probe **laut** ab (kein stilles Weiterarbeiten mit falscher Kamera).
const KAMERA_STEHT_STILL = [
  ["  if (nodes.length === 0 || cssWidth <= 0 || cssHeight <= 0) return;",
   "  return;  // C2-Probe: die Kamera steht still (Schritt 14.3)"],
];

// -- Modul laden (mit Patch) --------------------------------------------------------------------

let moduleCounter = 0;
function loadGraphModule(patch, suffix) {
  let source = fs.readFileSync(GRAPH_JS, "utf8");
  // **Die Kamera steht still** (Schritt 14.3) — immer, auch im Gegenlauf: die Kamera ist nicht
  // der Gegenstand dieser Probe (siehe `KAMERA_STEHT_STILL`).
  for (const [oldText, newText] of KAMERA_STEHT_STILL) {
    if (!source.includes(oldText)) {
      throw new Error("Kamera-Anker nicht gefunden: " + JSON.stringify(oldText.slice(0, 60)));
    }
    source = source.replace(oldText, newText);
  }
  if (patch) {
    for (const [oldText, newText] of patch) {
      if (!source.includes(oldText)) {
        throw new Error("Gegenlauf-Anker nicht gefunden: " + JSON.stringify(oldText.slice(0, 60)));
      }
      source = source.replace(oldText, newText);
    }
  }
  // Die Kopie liegt in /tmp; ihre Importe zeigen auf die **echten** Nachbarmodule (absolute
  // Datei-URL), damit die Kopie dasselbe Verhalten hat wie das Original.
  source = source.replace(/from "\.\/([a-z_]+\.js)"/g,
    (m, name) => 'from "' + pathToFileURL(path.join(STATIC_DIR, name)).href + '"');
  // **Die Messpflaster:** die Zahl der Furche-Zellen (das ist der **Gegenstand** der Regel) und
  // der Abstand der Lappen-Aussenkonturen. Sie aendern das Verhalten nicht, sie machen nur
  // sichtbar, was die Regel tut. Der Anker ist so gewaehlt, dass ein Fehlen **laut** wird
  // (derselbe Mechanismus wie bei den Gegenlaeufen).
  for (const [oldText, newText] of MESS_PFLASTER) {
    if (!source.includes(oldText)) {
      throw new Error("Messpflaster-Anker nicht gefunden: " + JSON.stringify(oldText.slice(0, 60)));
    }
    source = source.replace(oldText, newText);
  }
  moduleCounter += 1;
  const tmp = path.join(os.tmpdir(), "p105_b8_probe_" + suffix + "_" + moduleCounter + ".mjs");
  fs.writeFileSync(tmp, source, "utf8");
  return import(pathToFileURL(tmp).href);
}



// -- DOM-Shim ------------------------------------------------------------------------------------

const rafQueue = [];
let rafCalls = 0;

function makeCtx() {
  return {
    strokes: [],   // {alpha, strokeStyle, lineWidth, path, quads}
    fills: [],     // {alpha, fillStyle, path, quads}
    arcs: [],      // {x, y, r, alpha, fillStyle, strokeStyle, lineWidth}
    texts: [],     // {text, x, y, alpha}
    dashes: [],
    _path: [],
    _quads: 0,
    _x: 0,
    _y: 0,
    globalAlpha: 1,
    fillStyle: "",
    strokeStyle: "",
    lineWidth: 1,
    setTransform() {},
    clearRect() {},
    save() {},
    restore() {},
    translate() {},
    scale() {},
    beginPath() { this._x = 0; this._y = 0; this._quads = 0; this._path = []; },
    moveTo(x, y) { this._x = x; this._y = y; },
    lineTo(x, y) {
      this._path.push([this._x, this._y, x, y]);
      this._x = x; this._y = y;
    },
    quadraticCurveTo(cx, cy, x, y) {
      this._quads += 1;
      this._path.push([this._x, this._y, x, y]);
      this._x = x; this._y = y;
    },
    closePath() {},
    stroke() {
      this.strokes.push({
        alpha: this.globalAlpha, strokeStyle: this.strokeStyle, lineWidth: this.lineWidth,
        path: this._path.slice(), quads: this._quads,
      });
      this._path = [];
    },
    arc(x, y, r, a0, a1) {
      this.arcs.push({
        x: x, y: y, r: r, alpha: this.globalAlpha, fillStyle: this.fillStyle,
        strokeStyle: this.strokeStyle, lineWidth: this.lineWidth,
      });
      this._x = x; this._y = y;
    },
    fill() {
      this.fills.push({
        alpha: this.globalAlpha, fillStyle: this.fillStyle,
        path: this._path.slice(), quads: this._quads,
      });
      this._path = [];
    },
    fillText(text, x, y) {
      this.texts.push({ text: text, x: x, y: y, alpha: this.globalAlpha });
    },
    setLineDash(d) { this.dashes.push(d.slice()); },
  };
}

const canvasCtx = makeCtx();
const canvasListeners = {};

const canvasEl = {
  width: 0,
  height: 0,
  isConnected: true,
  getContext: () => canvasCtx,
  getBoundingClientRect: () => ({ width: 800, height: 600, left: 0, top: 0 }),
  addEventListener(type, fn) { (canvasListeners[type] = canvasListeners[type] || []).push(fn); },
};

function fireCanvas(type, event) {
  (canvasListeners[type] || []).forEach((fn) => fn(event));
}

// Der localStorage als echter Speicher (der Harness soll das Layout wirklich merken können).
const store = new Map();
const localStorage = {
  getItem: (k) => (store.has(k) ? store.get(k) : null),
  setItem: (k, v) => { store.set(k, String(v)); },
  removeItem: (k) => { store.delete(k); },
  clear: () => { store.clear(); },
};

const emptyStateEl = { hidden: false };
const zoomReadoutEl = { textContent: "" };
const tagsToggleEl = { checked: false, addEventListener() {} };
const foldersToggleEl = { checked: false, addEventListener() {} };
const tagsHandlers = [];
const foldersHandlers = [];
tagsToggleEl.addEventListener = (type, fn) => { if (type === "change") tagsHandlers.push(fn); };
foldersToggleEl.addEventListener = (type, fn) => { if (type === "change") foldersHandlers.push(fn); };

// Die neuen Bedienelemente (Schritt 8.5/8.6): Suchfeld, zwei Auswahllisten, Reset-Knopf,
// Statuszeile. Der Harness traegt sie als echte Elemente, damit der Produktivcode unabhaengig
// vom Testgeruest arbeitet.
function makeElement(extra) {
  const el = {
    value: "",
    textContent: "",
    attributes: {},
    listeners: {},
    options: [],
    getAttribute(k) { return this.attributes[k] || null; },
    setAttribute(k, v) { this.attributes[k] = v; },
    removeAttribute(k) { delete this.attributes[k]; },
    addEventListener(t, fn) { this.listeners[t] = fn; },
    appendChild(child) { this.options.push(child); },
    // **Das Kind muss wirklich verschwinden**: `pruneSelect()` leert die Liste in einer
    // Schleife (`while (el.options.length) el.removeChild(el.options[0])`) -- ein Shims-
    // `removeChild`, das nichts tut, haengt dort **endlos** (gemessen 2026-10-24: der erste
    // Probelauf blieb ohne Ausgabe stehen).
    removeChild(child) {
      const i = this.options.indexOf(child);
      if (i >= 0) this.options.splice(i, 1);
    },
  };
  return Object.assign(el, extra || {});
}

const searchEl = makeElement();
const typeSelectEl = makeElement({ options: [{ value: "" }, { value: "note" }, { value: "task" }] });
const statusSelectEl = makeElement({
  options: [{ value: "" }, { value: "active" }, { value: "open" },
            { value: "doing" }, { value: "done" }],
});
const resetEl = makeElement();
const statusTextEl = makeElement();
// **Die Trefferzahl hat ihr eigenes Feld** (`#overview-graph-hits`) -- der Layout-Hinweis
// ("Layout gemerkt") hat sie vorher ueberschrieben (Block 8, Schritt 8.6).
const hitsTextEl = makeElement();

globalThis.document = {
  getElementById(id) {
    if (id === "overview-graph-canvas") return canvasEl;
    if (id === "overview-graph-empty") return emptyStateEl;
    if (id === "overview-graph-zoom") return zoomReadoutEl;
    if (id === "overview-graph-toggle-tags") return tagsToggleEl;
    if (id === "overview-graph-toggle-folders") return foldersToggleEl;
    if (id === "overview-graph-search") return searchEl;
    if (id === "overview-graph-filter-type") return typeSelectEl;
    if (id === "overview-graph-filter-status") return statusSelectEl;
    if (id === "overview-graph-reset-layout") return resetEl;
    if (id === "overview-graph-status") return statusTextEl;
    if (id === "overview-graph-hits") return hitsTextEl;
    return null;
  },
  addEventListener() {},
  querySelectorAll: () => [],
  createElement: () => makeElement(),
};

globalThis.window = {
  devicePixelRatio: 1,
  matchMedia: () => ({ matches: false }),
  addEventListener() {},
  setInterval() {},
  localStorage: localStorage,
  setTimeout: (fn) => { fn(); return 0; },
  clearTimeout() {},
};

globalThis.sessionStorage = { getItem: () => null, setItem() {}, removeItem() {} };
globalThis.requestAnimationFrame = (cb) => { rafCalls += 1; rafQueue.push(cb); return rafQueue.length; };
globalThis.cancelAnimationFrame = () => { rafQueue.length = 0; };

function flushOneFrame() {
  const queue = rafQueue.splice(0, rafQueue.length);
  queue.forEach((cb) => cb());
  return queue.length;
}

function runTicks(n) {
  for (let i = 0; i < n; i++) {
    if (flushOneFrame() === 0) return i;
  }
  return n;
}

// -- Die Daten (ein Fixture, kein Zufall) ---------------------------------------------------------
//
// Drei Spaces (alle drei Farbkategorien), sechs Knoten, fuenf Kanten. Der Weg a1 -> a2 -> a3
// und der Weg a1 -> b1 -> b2 -> g1 geben **drei Ringe** um a1: der erste Ring {a2, b1}, der
// zweite {a3, b2}, der Rest {g1} -- genau die drei Stufen aus Plan 8.4.

function node(id, space, own, writable, type, status, title) {
  return {
    id: id, title: title || ("Item " + id), space: space, own: own, writable: writable,
    type: type, status: status, folder: "", tags: [],
  };
}

const NODES = [
  node("itm_a1", "alpha", true, true, "note", "active", "Alpha Notiz"),
  node("itm_a2", "alpha", true, true, "task", "open", "Alpha Aufgabe"),
  node("itm_a3", "alpha", true, true, "task", "doing", "Alpha in Arbeit"),
  node("itm_b1", "beta", false, true, "task", "open", "Beta Aufgabe"),
  node("itm_b2", "beta", false, true, "note", "active", "Beta Notiz"),
  node("itm_g1", "gamma", false, false, "note", "active", "Gamma fremd"),
];

const EDGES = [
  { src: "itm_a1", dst: "itm_a2", kind: "frontmatter" },
  { src: "itm_a2", dst: "itm_a3", kind: "frontmatter" },
  { src: "itm_a1", dst: "itm_b1", kind: "frontmatter" },
  { src: "itm_b1", dst: "itm_b2", kind: "body" },
  { src: "itm_b2", dst: "itm_g1", kind: "frontmatter" },
];

const PAYLOAD = { nodes: NODES, edges: EDGES };

// -- Die **festen** Positionen (datierte Aenderung, 2026-10-26, Schritt 14.2) --------------------
//
// **Der Wächter misst die Zeichenregel, nicht das Layout.** Bis Schritt 14.2 hing die
// Furche-Messung an einem **Unfall**: die Zentrums-Gravitation zog alle drei Spaces in einen
// Klumpen, die Lappen zweier Spaces stiessen aneinander, und die Furche war das, was sie
// trennte. Mit der neuen L4 (Anker-Gravitation, Querfedern — Schritt 14.2) ruecken die Spaces
// **auseinander**: die Lappen beruehren sich nicht mehr, die Furche hat **keinen Gegenstand**
// mehr — **gemessen**: 62 Furche-Zellen vorher, **0** nachher. Der Gegenlauf "`furche` aus"
// blieb dadurch **gruen**, ohne dass der Fehler wiederhergestellt war (der Wächter meldete
// genau das: „der Anker griff nicht oder die Messung prueft das Falsche").
//
// **Die Reparatur:** die Positionen werden **fest vorgegeben** (zwei Spaces beruehren sich
// dort, wo die Furche etwas zu trennen hat) und ueber die **Ablage** (`localStorage`) gesetzt —
// der Produktivcode haelt sie fest (`pinned`, Plan 8.5). Damit misst die Probe die
// **Zeichenregel** an einem **festen** Eingang, unabhaengig vom Layout — und der Gegenlauf
// beisst wieder. Das Layout gehoert zum Browser-Waechter (`p105_b14_layout_probe.py`).
//
// Die Positionen: alpha und beta **beruehren** sich (30 px Abstand, der Reach-Radius des
// Koerpermaske ist 48 px, die Rasterzelle 8 px) => die Zellen zwischen ihnen sind die Furche;
// gamma steht abseits.
const FESTE_POSITIONEN = {
  itm_a1: [300, 300], itm_a2: [300, 340], itm_a3: [300, 380],
  itm_b1: [330, 300], itm_b2: [330, 340],
  itm_g1: [200, 500],
};

const fetchLog = [];
globalThis.fetch = function (url) {
  fetchLog.push(url);
  return Promise.resolve({
    status: 200, ok: true, statusText: "OK",
    json: () => Promise.resolve(PAYLOAD),
  });
};

// -- Die Messungen ---------------------------------------------------------------------------------

const results = {};

// Die Knotenpositionen: der Kern und der Membranring eines Knotens teilen den Mittelpunkt, der
// Ring eines "doing"-Knotens auch -- die eindeutigen Positionen in Zeichenreihenfolge sind
// also die Knoten in Payload-Reihenfolge.
function cellPositions() {
  const seen = new Map();
  for (const a of canvasCtx.arcs) {
    const key = a.x.toFixed(3) + "|" + a.y.toFixed(3);
    if (!seen.has(key)) seen.set(key, [a.x, a.y]);
  }
  return [...seen.values()];
}

function lobeFills() { return canvasCtx.fills.filter((f) => f.quads >= 3); }
function lobeStrokes() { return canvasCtx.strokes.filter((s) => s.quads >= 3); }
function edgeStrokes() { return canvasCtx.strokes.filter((s) => s.quads === 1); }
function processStrokes() { return canvasCtx.strokes.filter((s) => s.quads === 0 && s.path.length >= 2); }

// 0) Der normale Lauf ------------------------------------------------------------------------------
const graph = await loadGraphModule(gegenlauf ? GEGENLAEUFE[gegenlauf] : null, "normal");
const { state } = await import(pathToFileURL(path.join(STATIC_DIR, "state.js")).href);
state.ownSpace = "alpha";
state.graphToken = null;

// Die **festen** Positionen vor dem ersten Laden in die Ablage legen (siehe
// `FESTE_POSITIONEN`): der Produktivcode haelt sie fest (`pinned`) — der Eingang der Probe ist
// damit **fest** und nicht mehr vom Layout abhaengig (datierte Aenderung, 2026-10-26, 14.2).
store.set("sfx:graph:layout:v1:alpha", JSON.stringify({ v: 1, pos: FESTE_POSITIONEN }));

graph.init();
await graph.loadGraph();
flushOneFrame();               // resize() + Saat + Simulation
const ticks = runTicks(400);    // die Simulation auslaufen lassen

// **Ein Frame, nicht 152.** Die Simulation zeichnet jeden Tick; die Messung liest sonst den
// ganzen Verlauf (156 Lappenflaechen statt drei, 770 Bahnen statt fuenf). Also: nach dem
// Einschwingen die Aufzeichnung leeren und **einen** Frame zeichnen.
function resetRecording() {
  canvasCtx.strokes = [];
  canvasCtx.fills = [];
  canvasCtx.arcs = [];
  canvasCtx.texts = [];
  canvasCtx.dashes = [];
}
function redraw() {
  // Das Suchfeld loest bei jeder Eingabe ein `draw()` aus -- auch bei leerem Wert.
  searchEl.value = "";
  searchEl.listeners.input({ target: searchEl });
}
resetRecording();
redraw();

// 1) Die Lappen (Schritt 8.1) ------------------------------------------------------------------------
const lobeFillColors = [...new Set(lobeFills().map((f) => f.fillStyle))].sort();
const lobeStrokeColors = [...new Set(lobeStrokes().map((s) => s.strokeStyle))].sort();

results.lappen = {
  lobe_fills: lobeFills().length,
  lobe_fill_colors: lobeFillColors,
  lobe_contour_colors: lobeStrokeColors,
  inner_contours: lobeStrokes().filter((s) => s.alpha === 1 && String(s.strokeStyle).startsWith("rgb(")).length,
  fill_alpha: [...new Set(lobeFills().map((f) => f.alpha))],
  contour_alpha: [...new Set(lobeStrokes().map((s) => s.alpha))],
  // Mindestens zwei Lappen (zwei Spaces), die Flaeche leise (5%), die Kontur halb deckend (55%)
  // und die innere Linie als **feste Farbe** (rgb(...)), nicht als Alpha.
  ok: lobeFills().length >= 2
      && lobeFillColors.length >= 2
      && lobeFills().every((f) => Math.abs(f.alpha - 0.05) < 1e-9)
      && lobeStrokes().some((s) => Math.abs(s.alpha - 0.55) < 1e-9)
      && lobeStrokes().some((s) => s.alpha === 1 && String(s.strokeStyle).startsWith("rgb(")),
};

// 2) Die Furche (Schritt 8.1) -------------------------------------------------------------------------
// Zwei Lappen verschiedener Spaces duerfen sich **nicht** beruehren: die Zellen, deren
// 4-Nachbar einem anderen Space gehoert, sind die Furche.
function contourPointsByColor(strokes) {
  const byColor = new Map();
  for (const s of strokes) {
    if (!byColor.has(s.strokeStyle)) byColor.set(s.strokeStyle, []);
    for (const p of s.path) byColor.get(s.strokeStyle).push(p);
  }
  return byColor;
}
function minDistance(a, b) {
  let best = Infinity;
  for (const p of a) for (const q of b) {
    const d = Math.hypot(p[0] - q[0], p[1] - q[1]);
    if (d < best) best = d;
  }
  return best;
}
const contourGroups = [...contourPointsByColor(lobeStrokes().filter((s) => s.alpha === 0.55)).values()];
let lobeSeparation = Infinity;
for (let i = 0; i < contourGroups.length; i++) {
  for (let j = i + 1; j < contourGroups.length; j++) {
    lobeSeparation = Math.min(lobeSeparation, minDistance(contourGroups[i], contourGroups[j]));
  }
}
results.furche = {
  // Die Zahl der Furche-Zellen: der **Gegenstand** der Regel. Sie muss groesser als null
  // sein -- sonst gibt es nichts, was die Regel trennt (das war der Befund aus Schritt 14.2:
  // mit dem neuen Layout bleiben die Spaces auseinander, die Furche hat keinen Gegenstand).
  furrow_cells: globalThis.__furrowCells,
  contours_compared: contourGroups.length,
  separation_px: Math.round(lobeSeparation * 10) / 10,
  ok: globalThis.__furrowCells > 0
      && contourGroups.length >= 2 && Number.isFinite(lobeSeparation) && lobeSeparation > 0,
};

// 3) Die Bahnen (Schritt 8.2) ------------------------------------------------------------------------
const edges = edgeStrokes();
const widths = [...new Set(edges.map((s) => Math.round(s.lineWidth * 100) / 100))].sort();
results.bahnen = {
  edges_drawn: edges.length,
  widths: widths,
  // Die Breite folgt dem Grad: 1 + log2(1 + min(deg(a), deg(b))). Bei Grad 1 sind das 2,0,
  // bei Grad 2 rund 2,58 -- die Kanten tragen also **zwei** verschiedene Breiten.
  ok: edges.length === EDGES.length
      && widths.length >= 2
      && widths.every((w) => w >= 1.99 && w <= 2.59),
};

// 4) Die Zellen (Schritt 8.3) ------------------------------------------------------------------------
const cells = cellPositions();
const processes = processStrokes();
// Die Fortsaetze werden je Knoten in **einem** Strich gezeichnet (ein Pfad mit 2-4 Strecken) --
// gezaehlt werden deshalb die Strecken, nicht die Strichaufrufe. Eine Strecke ist ein
// `lineTo` -- der `moveTo` des Fortsatzes ist kein Stueck des Pfades.
const processSegments = processes.reduce((sum, s) => sum + s.path.length, 0);

// Die Signatur der Fortsaetze: je Knoten die Liste aus (Winkel, Laenge) -- **nicht** die
// Pixelpositionen (die aendern sich mit der Simulation). Plan 8.3: "deterministisch aus dem
// Hash der Item-ID (gleiche Zeichnung bei jedem Laden)" -- also muss die Signatur bei zwei
// Zeichnungen **identisch** sein.
function processSignature(procList) {
  const perCell = cells.map(() => []);
  for (const s of procList) {
    if (!s.path.length) continue;
    const start = s.path[0];
    let best = -1;
    let bestD = Infinity;
    for (let i = 0; i < cells.length; i++) {
      const d = Math.hypot(start[0] - cells[i][0], start[1] - cells[i][1]);
      if (d < bestD) { bestD = d; best = i; }
    }
    if (best < 0 || bestD > 40) continue;
    for (const seg of s.path) {
      const angle = Math.atan2(seg[1] - cells[best][1], seg[0] - cells[best][0]);
      const len = Math.hypot(seg[2] - seg[0], seg[3] - seg[1]);
      perCell[best].push(Math.round(angle * 1000) + ":" + Math.round(len * 100));
    }
  }
  return perCell.map((list) => list.sort().join(",")).join("|");
}
const signatureA = processSignature(processes);
resetRecording();
redraw();
const signatureB = processSignature(processStrokes());
results.zellen = {
  cells: cells.length,
  arcs: canvasCtx.arcs.length,
  process_strokes: processes.length,
  process_segments: processSegments,
  // Die Signatur bei zwei Zeichnungen: identisch (deterministisch) -- mit zufaelligen
  // Fortsaetzen waere sie es nicht.
  deterministic: signatureA === signatureB,
  ok: cells.length === NODES.length
      && processSegments >= NODES.length * 2
      && processSegments <= NODES.length * 4
      && signatureA === signatureB,
};

// 5) Die Aktivierung (Schritt 8.4) -------------------------------------------------------------------
// Im Ruhezustand (ohne Fokus) ist **alles** voll deckend; mit Fokus gibt es drei Stufen:
// Fokus und erster Ring 1, zweiter Ring 0,5, der Rest 0,45.
const alphaAtRest = [...new Set(canvasCtx.arcs.map((a) => a.alpha))].sort();
resetRecording();
fireCanvas("mousemove", { clientX: cells[0][0], clientY: cells[0][1] });
const alphaWithFocus = [...new Set(canvasCtx.arcs.map((a) => a.alpha))].sort();
results.aktivierung = {
  alphas_at_rest: alphaAtRest,
  alphas_with_focus: alphaWithFocus,
  ok: alphaAtRest.length === 1 && alphaAtRest[0] === 1
      && alphaWithFocus.includes(1)
      && alphaWithFocus.includes(0.5)
      && alphaWithFocus.includes(0.45),
};

// 6) KA-2 — das Layout merken (Schritt 8.5) ---------------------------------------------------------
//
// **Der Knoten wird erst gezogen.** Ohne den Zug liegt die gemerkte Position auf dem
// Gleichgewicht der Simulation -- und die Simulation laeuft nach dem Neuladen wieder in
// dasselbe Gleichgewicht, ob der Knoten festgehalten wird oder nicht. Der Unterschied wird
// erst sichtbar, wenn der Mensch die Position **veraendert** hat: dann muss die Karte die
// neue Position behalten (mit Festhalten) oder auf das Gleichgewicht zurueckfallen (ohne).
const LAYOUT_KEY = "sfx:graph:layout:v1:alpha";
const DRAG_X = 123;
const DRAG_Y = 456;
fireCanvas("mousedown", { button: 0, clientX: cells[0][0], clientY: cells[0][1] });
fireCanvas("mousemove", { clientX: DRAG_X, clientY: DRAG_Y });
fireCanvas("mouseup", { clientX: DRAG_X, clientY: DRAG_Y });

const stored = store.get(LAYOUT_KEY);
let storedParsed = null;
try { storedParsed = stored ? JSON.parse(stored) : null; } catch (e) { storedParsed = null; }
const storedCount = storedParsed && storedParsed.pos ? Object.keys(storedParsed.pos).length : 0;
const draggedStored = storedParsed && storedParsed.pos ? storedParsed.pos[NODES[0].id] : null;

// Ein Neuladen: die Positionen muessen die gemerkten sein (die Knoten stehen fest; die
// datierte Entscheidung in `seedInitialPositions()`). Die Ablage rundet auf ganze Pixel
// (`Math.round`), deshalb ist die zulaessige Abweichung 0,71 px (die Ecken eines Pixels).
canvasCtx.arcs = [];
await graph.loadGraph({ force: true });
flushOneFrame();
runTicks(400);
// **Ein Frame, nicht 152** (wie oben): die Positionen nach dem Neuladen sind die des
// **letzten** Frames -- der erste Frame zeigt noch die Startpositionen.
resetRecording();
redraw();
const positionsAfter = cellPositions();
let maxDeviation = 0;
for (let i = 0; i < NODES.length; i++) {
  const gespeichert = storedParsed && storedParsed.pos ? storedParsed.pos[NODES[i].id] : null;
  if (!gespeichert || i >= positionsAfter.length) { maxDeviation = Infinity; break; }
  maxDeviation = Math.max(maxDeviation,
    Math.hypot(positionsAfter[i][0] - gespeichert[0], positionsAfter[i][1] - gespeichert[1]));
}
results.layout = {
  key: LAYOUT_KEY,
  stored_entries: storedCount,
  stored_version: storedParsed ? storedParsed.v : null,
  dragged_to: draggedStored,
  deviation_px: Number.isFinite(maxDeviation) ? Math.round(maxDeviation * 100) / 100 : null,
  ok: storedParsed !== null && storedParsed.v === 1 && storedCount === NODES.length
      && draggedStored !== null
      && Math.hypot(draggedStored[0] - DRAG_X, draggedStored[1] - DRAG_Y) <= 1
      && maxDeviation <= 1,
};

// 7) KA-3 — Suche und Filter (Schritt 8.6) ---------------------------------------------------------
// Die Suche dimmt die Nicht-Treffer und zaehlt sie; der Filter blendet Knoten **und** Bahnen aus.
canvasCtx.arcs = [];
canvasCtx.strokes = [];
searchEl.value = "alpha";
searchEl.listeners.input({ target: searchEl });
const searchAlphas = [...new Set(canvasCtx.arcs.map((a) => a.alpha))].sort();
const hitsText = hitsTextEl.textContent;
const statusText = statusTextEl.textContent;

searchEl.value = "";
searchEl.listeners.input({ target: searchEl });
canvasCtx.arcs = [];
canvasCtx.strokes = [];
typeSelectEl.value = "note";
typeSelectEl.listeners.change({ target: typeSelectEl });
const filteredCells = cellPositions().length;
const filteredEdges = edgeStrokes().length;
results.filter = {
  search_alphas: searchAlphas,
  hit_counter: hitsText,
  status_text: statusText,
  cells_without_filter: NODES.length,
  cells_with_type_filter: filteredCells,
  edges_without_filter: EDGES.length,
  edges_with_type_filter: filteredEdges,
  // Suche: die Treffer hell (1), der Rest gedimmt (0,45), und die Zahl steht in der Statuszeile.
  // Filter: nur die Notizen bleiben (3 Knoten), und nur die Kante zwischen zwei Notizen bleibt.
  ok: searchAlphas.includes(1) && searchAlphas.includes(0.45) && /Treffer/.test(hitsText)
      && filteredCells === 3 && filteredEdges === 1,
};

// 8) Reduced motion (Schritt 8.7) -------------------------------------------------------------------
// Ein **zweiter** Modul-**Zustand** (eine eigene Kopie): `matchMedia` meldet reduced motion,
// und der Zaehler der rAF-Aufrufe muss **0** sein (Abnahme P10.5-40).
//
// **Der Gegenlauf `reducedmotion` patcht genau diese Kopie** -- nicht die normale: sonst wuerde
// der Gegenlauf an der falschen Stelle greifen und die Messung bliebe gruen.
const rmGraph = await loadGraphModule(
  gegenlauf === "reducedmotion" ? GEGENLAEUFE.reducedmotion : null, "reducedmotion");
globalThis.window.matchMedia = () => ({ matches: true });
rafCalls = 0;
canvasCtx.arcs = [];
rmGraph.init();
await rmGraph.loadGraph();
const rafCallsAfterLoad = rafCalls;
const rmArcs = canvasCtx.arcs.length;
results.reducedmotion = {
  raf_calls: rafCallsAfterLoad,
  painted_nodes: rmArcs,
  // 0 Frames: das erste Bild wird synchron gezeichnet (Plan 8.7, Abnahme P10.5-40) -- und es
  // ist **kein** leeres Bild (der Plan verlangt "statisch", nicht "leer").
  ok: rafCallsAfterLoad === 0 && rmArcs > 0,
};

results.ausfuehrer = {
  ticks: ticks,
  fetch_calls: fetchLog.length,
  gegenlauf: gegenlauf || null,
};

const json = JSON.stringify(results, null, 2) + "\n";
// Die Rohwerte liegen **neben** der Probe (Plan §2.3: "Rohwerte als JSON daneben") -- aber nur
// der Normalfall: die acht Gegenlaeufe schreiben nach /tmp, sonst liegen neun JSON-Dateien im
// Repo, von denen acht einen Fehler zeigen.
const jsonPath = gegenlauf
  ? path.join(os.tmpdir(), "p105_b8_c2_probe_gegenlauf_" + gegenlauf + ".json")
  : path.join(HERE, "p105_b8_c2_probe.json");
fs.writeFileSync(jsonPath, json, "utf8");
process.stdout.write(json);
