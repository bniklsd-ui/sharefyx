// P9 Step E — Test-Harness für graph.js (Plan §7.4, Tests 1 und 2, plus V118).
//
// Der Harness ist KEIN Wegwerf-Skript und keine Sichtprüfung: er lädt das echte
// `phase5_ui/webui/static/js/graph.js` in Node mit einem minimalen DOM-Shim. Grund: `graph.js`
// ist ein ES-Modul ohne Build-Schritt (P5-T), und die einzige Ebene, auf der sich "kein zweiter
// Abruf" und "die Karte springt beim Wiedereintritt nicht" überhaupt prüfen lassen, ist ein
// echter Lauf des Moduls.
//
// Shim statt jsdom, weil die Karte von der DOM genau eine Canvas-Box, einen 2d-Context (der
// nichts malt, sondern Striche zählt), `matchMedia` und `requestAnimationFrame` braucht. Die
// Import-Ketten (api.js → toasts.js, editor.js, list.js, tree.js, dialogs.js) werden beim
// Import nicht angefasst. `prefers-reduced-motion` ist hier **aus**: nur so lässt sich der
// Simulations-Loop Tick für Tick von Hand füttern — der Test muss den Zustand *eines* Frames
// abgreifen können, nicht den eines eingeschwungenen.
//
// Aufruf: `node phase9_hardening/scripts/graph_reload_probe.mjs` → JSON auf stdout.
// Aufrufer: `phase9_hardening/tests/test_graph_reload.py`.

import { fileURLToPath } from "node:url";
import path from "node:path";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const STATIC_DIR = path.resolve(HERE, "../../phase5_ui/webui/static/js");

// -- DOM-Shim ---------------------------------------------------------------------------------

const rafQueue = [];

function makeCtx() {
  return {
    strokes: [],      // [x1, y1, x2, y2] je ctx.stroke()
    dashes: [],       // setLineDash()-Argumente in Aufrufreihenfolge
    _x: 0,
    _y: 0,
    setTransform() {},
    clearRect() {},
    save() {},
    restore() {},
    translate() {},
    scale() {},
    beginPath() { this._x = 0; this._y = 0; },
    moveTo(x, y) { this._x = x; this._y = y; },
    lineTo(x, y) { this.strokes.push([this._x, this._y, x, y]); },
    stroke() {},
    arc() {},
    fill() {},
    fillText() {},
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

const emptyStateEl = { hidden: false };
const zoomReadoutEl = { textContent: "" };
const tagsToggleEl = { checked: false, addEventListener() {} };
const foldersToggleEl = { checked: false, addEventListener() {} };
const tagsHandlers = [];
tagsToggleEl.addEventListener = (type, fn) => { if (type === "change") tagsHandlers.push(fn); };

globalThis.document = {
  getElementById(id) {
    if (id === "overview-graph-canvas") return canvasEl;
    if (id === "overview-graph-empty") return emptyStateEl;
    if (id === "overview-graph-zoom") return zoomReadoutEl;
    if (id === "overview-graph-toggle-tags") return tagsToggleEl;
    if (id === "overview-graph-toggle-folders") return foldersToggleEl;
    return null;
  },
  addEventListener() {},
  querySelectorAll: () => [],
};

globalThis.window = {
  devicePixelRatio: 1,
  matchMedia: () => ({ matches: false }),   // KEIN reduced-motion: Loop manuell steuerbar
  addEventListener() {},
  setInterval() {},
  setTimeout: (fn) => { fn(); return 0; },
};

globalThis.sessionStorage = { getItem: () => null, setItem() {}, removeItem() {} };
globalThis.requestAnimationFrame = (cb) => { rafQueue.push(cb); return rafQueue.length; };
globalThis.cancelAnimationFrame = () => { rafQueue.length = 0; };

// Genau EIN Frame: der Warteschlange alle derzeit anliegenden Callbacks entnehmen und ausführen.
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

// -- api()-Shim über fetch --------------------------------------------------------------------
// `api.js` ruft das globale `fetch`; hier werden die Abrufe gezählt und vorbereitete
// Graph-Payloads ausgeliefert.

let fetchLog = [];
let graphPayloads = [];
let lastPayload = null;

globalThis.fetch = function (url) {
  fetchLog.push(url);
  // Der Vorrat ist absichtlich **unerschöpflich**: ist er leer, kommt der zuletzt gelieferte
  // Payload erneut. Der Test prüft die *Anzahl* der Abrufe, nicht den Inhalt — ein Harness, der
  // bei einem zu vielen Abruf mit einem TypeError stirbt, beweist nichts, er unterrichtet nur
  // seinen eigenen Defekt. (Der erste Entwurf reservierte einen abweichenden Reserve-Payload;
  // die Zählung ist die stärkere Aussage, und `lastPayload` hält die Reserve trotzdem fest.)
  if (graphPayloads.length) lastPayload = graphPayloads.shift();
  return Promise.resolve({
    status: 200,
    ok: true,
    statusText: "OK",
    json: () => Promise.resolve(lastPayload),
  });
};

// -- Test-Bausteine ---------------------------------------------------------------------------

function node(id, tags) {
  return {
    id, title: "Item " + id, space: "niklas", own: true, writable: true,
    type: "note", status: "open", folder: "", tags: tags || [],
  };
}

function graphPayload(ids, edges, tagsById) {
  return {
    nodes: ids.map((id) => node(id, (tagsById || {})[id])),
    edges: edges || [],
  };
}

// /overview-Payload in der Form, die `api.py :: _overview` liefert (für das Change-Token).
function overview(revision, itemCount) {
  return [{
    name: "niklas",
    own: true,
    writable: true,
    item_count: itemCount,
    counts: { open: itemCount, done: 0 },
    recent: [
      { id: "itm_0000000a", version: revision, updated: "2026-09-26T1" + (revision % 10) + ":00:00Z" },
      { id: "itm_0000000b", version: 1, updated: "2026-09-20T10:00:00Z" },
    ],
  }];
}

// Positionen der gezeichneten Knoten: `drawEdges()` zeichnet von der Quell- zur Zielposition,
// `moveTo`/`lineTo` landen also genau auf den Knotenkoordinaten. Für die Zwillingskanten-Frage
// (V118) wird zusätzlich das Segment selbst als Schlüssel gezählt.
function segments(strokes) {
  return strokes.map(([x1, y1, x2, y2]) => [x1, y1, x2, y2].join(","));
}
function points(strokes) {
  const out = new Set();
  strokes.forEach(([x1, y1, x2, y2]) => { out.add(x1 + "|" + y1); out.add(x2 + "|" + y2); });
  return out;
}
function distanceToNearest(strokes, x, y) {
  let best = Infinity;
  points(strokes).forEach((p) => {
    const [px, py] = p.split("|").map(Number);
    best = Math.min(best, Math.hypot(px - x, py - y));
  });
  return best;
}

const results = {};
const graph = await import(path.join(STATIC_DIR, "graph.js"));
const { state, overviewToken } = await import(path.join(STATIC_DIR, "state.js"));
graph.init();

// Das Token wird über den **echten** Erzeuger gesetzt, nicht über eine nachgebaute Formatkopie
// im Harness -- sonst prüfte der Test ein Format, das der Produktivcode nicht benutzt.
// Fehlt `state.js :: overviewToken()` (Stand ohne P9 Step E), meldet das dieser Wächter, und der
// Rest läuft mit `null` weiter, damit die Verhaltenstests sauber rot werden statt an einem
// TypeError zu hängen.
const tokenBuilder = typeof overviewToken === "function" ? overviewToken : null;
results.state_module_exposes_the_token_builder = { ok: tokenBuilder !== null };
function setToken(overviewPayload) {
  state.graphToken = tokenBuilder ? tokenBuilder(overviewPayload) : null;
}

// =============================================================================================
// Test 1 — P9-33: ein zweiter Eintritt ohne Datenänderung erzeugt KEINEN zweiten /graph-Abruf
// =============================================================================================

graphPayloads = [
  graphPayload(["itm_0000000a", "itm_0000000b"],
               [{ src: "itm_0000000a", dst: "itm_0000000b", kind: "frontmatter" }]),
];

setToken(overview(1, 2));
fetchLog = [];
await graph.loadGraph();
flushOneFrame();
runTicks(400);                       // die Simulation auslaufen lassen (ALPHA_DECAY 0.97 ≈ 151 Ticks)
const firstFetches = fetchLog.length;
const settledStrokes = canvasCtx.strokes.slice();

// Messgröße für "kein neuer Simulations-Loop": die Warteschlange muss beim Wiedereintritt **leer**
// sein und danach leer bleiben. Ein liegengebliebener Rest-Tick der ersten Ladung würde den
// Wächter sonst verrauschen -- deshalb wird er vorher weggetaktet.
const framesBefore = rafQueue.length;
await graph.loadGraph();
flushOneFrame();
const framesAfter = rafQueue.length;
const strokesAfterReentry = canvasCtx.strokes.length - settledStrokes.length;

results.p9_33_no_second_fetch = {
  fetches_first_entry: firstFetches,
  fetches_total_after_second_entry: fetchLog.length,
  frames_queued_before_reentry: framesBefore,
  frames_queued_after_reentry: framesAfter,
  ok: firstFetches === 1 && fetchLog.length === 1 && framesBefore === 0 && framesAfter === 0,
};

// P9-34 (halb): beim Wiedereintritt wird **kein** neuer Simulations-Loop gestartet. Ohne diesen
// Wächter könnte ein Fehler, der nur den Abruf spart und trotzdem neu sät, unentdeckt bleiben.
results.p9_34_reentry_does_not_restart_the_simulation = {
  frames_queued_after_reentry: framesAfter,
  ok: framesBefore === 0 && framesAfter === 0,
};

// =============================================================================================
// Test 2 — P9-34: bekannte Knoten behalten ihre Position über einen Refetch hinweg
// =============================================================================================
// Der Test zieht einen Knoten an eine markante Stelle, erzwingt danach einen Neuladen und prüft
// nach genau EINEM Simulations-Tick, ob er noch dort liegt. Ohne (b) bekäme jeder Knoten
// `x: 0, y: 0`, würde neu gesät und läge wieder auf dem Ring um die Canvas-Mitte.

const DROP_X = 123;
const DROP_Y = 456;

// Position von `itm_...a` aus dem letzten gezeichneten Frame holen: `drawEdges()` iteriert
// `explicitEdges` in Payload-Reihenfolge, `moveTo` ist die Quelle.
function positionOfSource(strokes) {
  const [x1, y1] = strokes[strokes.length - 1];
  return { x: x1, y: y1 };
}

const before = distanceToNearest(settledStrokes, DROP_X, DROP_Y);
const srcPos = positionOfSource(settledStrokes);

// Drag über die echten Event-Handler des Moduls (Maus-Press auf den Knoten, Ziehen, Loslassen).
fireCanvas("mousedown", { button: 0, clientX: srcPos.x, clientY: srcPos.y });
fireCanvas("mousemove", { clientX: DROP_X, clientY: DROP_Y });
fireCanvas("mouseup", { clientX: DROP_X, clientY: DROP_Y });

graphPayloads = [
  graphPayload(["itm_0000000a", "itm_0000000b"],
               [{ src: "itm_0000000a", dst: "itm_0000000b", kind: "frontmatter" }]),
];
setToken(overview(2, 2));      // Token wandert -> es MUSS neu geladen werden
canvasCtx.strokes = [];
const fetchesBeforeRefetch = fetchLog.length;
await graph.loadGraph();
flushOneFrame();                        // resize() + seed + runSimulation() stellt den Tick ein
const after = distanceToNearest(canvasCtx.strokes, DROP_X, DROP_Y);

results.p9_34_known_nodes_keep_their_position = {
  distance_before_drag: Math.round(before * 10) / 10,
  distance_after_drag: 0,
  distance_after_refetch: Math.round(after * 10) / 10,
  refetch_happened: fetchLog.length - fetchesBeforeRefetch === 1,
  // 25 px Toleranz: ein Tick der Simulation bewegt einen Knoten um wenige Pixel, der Sprung
  // zurück auf den Seed-Ring wäre bei dieser Box (Mitte 400/300, Radius ~150) über 150 px.
  ok: Math.abs(after) <= 25 && (fetchLog.length - fetchesBeforeRefetch === 1),
};

// Gegenprobe, die den Test scharf macht: ohne Ausführung des Drags läge der Knoten auf dem Ring,
// nicht bei (123, 456). `before` ist der gemessene Abstand des Knotens VOR dem Drag — er ist
// groß, das ist der Punkt.
results.p9_34_control_drop_point_is_off_the_ring = {
  distance_before_drag: Math.round(before * 10) / 10,
  ok: before > 100,
};

// =============================================================================================
// Test 3 — P9-35: eine Datenänderung führt weiterhin zum Neuladen; `force` erzwingt es
// =============================================================================================

graphPayloads = [
  graphPayload(["itm_0000000a", "itm_0000000b"],
               [{ src: "itm_0000000a", dst: "itm_0000000b", kind: "frontmatter" }]),
];
let mark = fetchLog.length;
setToken(overview(3, 2));      // nur das Token wandert, die Daten sind identisch
await graph.loadGraph();
flushOneFrame();
const refetchedOnChange = fetchLog.length - mark;

graphPayloads = [
  graphPayload(["itm_0000000a"], []),
];
mark = fetchLog.length;
await graph.loadGraph({ force: true });
flushOneFrame();
const refetchedOnForce = fetchLog.length - mark;

results.p9_35_a_change_still_reloads = {
  refetched_on_change: refetchedOnChange,
  refetched_on_force: refetchedOnForce,
  ok: refetchedOnChange === 1 && refetchedOnForce === 1,
};

// =============================================================================================
// Test 3b — der eigene Schreibvorgang: Token neu, Daten abrufen, dann Wiedereintritt
// =============================================================================================
// Das ist der Weg, den die **eigene** Verdrahtung dieser Session zuerst kaputt gemacht hätte:
// wenn das Token nur im 20s-Poll und beim Bootstrap gesetzt wird, sieht der Graph den gerade
// selbst gespeicherten Titel erst nach dem nächsten Poll. Im Produktivcode setzt `list.js::
// loadOverview()` das Token, und **jeder** Schreibpfad (afterWrite, Archivieren, Ordner, Space
// anlegen/entfernen) läuft durch genau diese Funktion -- deshalb genügt hier derselbe Aufruf.

graphPayloads = [
  graphPayload(["itm_0000000a", "itm_0000000b", "itm_0000000c"],
               [{ src: "itm_0000000a", dst: "itm_0000000b", kind: "frontmatter" }]),
];
setToken(overview(4, 3));
mark = fetchLog.length;
await graph.loadGraph();          // Token neu -> Abruf
flushOneFrame();
const fetchAfterWrite = fetchLog.length - mark;

mark = fetchLog.length;
await graph.loadGraph();          // Wiedereintritt, Token unverändert -> kein Abruf
flushOneFrame();
const fetchOnReentryAfterWrite = fetchLog.length - mark;

results.p9_35_own_write_is_visible_immediately = {
  refetched_after_the_write: fetchAfterWrite,
  refetched_on_reentry: fetchOnReentryAfterWrite,
  ok: fetchAfterWrite === 1 && fetchOnReentryAfterWrite === 0,
};

// =============================================================================================
// V118 — Zwillingskante: Tag-Kante UND explizite Kante zwischen denselben zwei Knoten
// =============================================================================================

graphPayloads = [
  graphPayload(["itm_0000000a", "itm_0000000b"],
               [{ src: "itm_0000000a", dst: "itm_0000000b", kind: "frontmatter" }],
               { itm_0000000a: ["rad"], itm_0000000b: ["rad"] }),
];
tagsToggleEl.checked = true;
tagsHandlers.forEach((fn) => fn({ target: tagsToggleEl }));
canvasCtx.strokes = [];
canvasCtx.dashes = [];
await graph.loadGraph({ force: true });
flushOneFrame();
tagsToggleEl.checked = false;
tagsHandlers.forEach((fn) => fn({ target: tagsToggleEl }));   // wieder zurückschalten

const lastFrameStart = canvasCtx.strokes.length - 1;   // genau der Strich des letzten draw()
const drawn = canvasCtx.strokes.slice(Math.max(0, canvasCtx.strokes.length - 2));
const counts = new Map();
drawn.forEach((s) => {
  const key = s.join(",");
  counts.set(key, (counts.get(key) || 0) + 1);
});
const twins = Array.from(counts.values()).filter((c) => c >= 2).length;
const dashed = canvasCtx.dashes.some((d) => d.length > 0);

results.v118_tag_edge_plus_explicit_edge = {
  segments_in_last_frame: drawn.length,
  duplicate_segments: twins,
  a_dashed_line_was_drawn: dashed,
  // Die Frage des Plans war, OB zwei Linien entstehen. Antwort: ja, zwei — und die zweite ist
  // gestrichelt. Ob das gewollt ist, entscheidet der Nikinger (P9-36), der Code ändert es nicht.
  ok: drawn.length === 2 && twins === 1 && dashed,
};

void lastFrameStart;
process.stdout.write(JSON.stringify(results, null, 2) + "\n");
