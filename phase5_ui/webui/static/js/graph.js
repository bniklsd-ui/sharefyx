"use strict";

// -- Verknuepfungs-Graph (Phase 8 Block D D2, Plan §5 D2, P8-D/P8-E) -----------------------
//
// Handgerollter Canvas-Force-Graph auf `GET /api/v1/graph` (B3, ACL-gefiltert, kein
// zusaetzlicher Server-Round-Trip). Daten-Layer liefert nur die expliziten Kanten (Frontmatter-
// `links:` plus `itm_…`-Body-Referenzen, beide als `kind: frontmatter|body`). Implizite Kanten
// (gleicher Tag / gleicher Ordner) werden HIER berechnet -- kein Server-Round-Trip dafuer,
// keine zweite Graph-Endpoint-Variante.
//
// **Bewusst NICHT verwendet:** D3 / PixiJS / cytoscape -- der Plan verlangt handgerollt, das
// Graph-Modul ist nicht gross genug, um eine Bibliotheks-Abhaengigkeit zu rechtfertigen.
// Kein LLM, keine Semantik -- reine Geometrie auf den schon ACL-gefilterten Knoten.
//
// **Bewusst NICHT gemacht:** persistent layout (kein Save der Positionen zwischen Reloads),
// WebWorker-Simulation (Datenmenge ist klein genug fuer requestAnimationFrame, 200 Knoten
// erreichen Ruhe in <3s auf einem normalen Browser, Plan P8-22), Mobile-Pinch-Zoom
// (Step 7b-W Desktop-first).

import { api, reportUnexpectedError } from "./api.js";
import { spaceCategory } from "./state.js";

var nodes = [];
var explicitEdges = [];   // {src, dst, kind} -- vom Server (frontmatter|body)
var implicitEdges = [];   // {src, dst, kind} -- vom Client (tag|folder)
var nodeById = Object.create(null);

var canvasEl = null;
var ctx = null;
var cssWidth = 0;
var cssHeight = 0;
var dpr = 1;

var zoom = 1;
var panX = 0;
var panY = 0;

var dragNode = null;       // Knoten, der gerade gezogen wird
var panStart = null;        // Pan-Geste: {startX, startY, origPanX, origPanY}
var hoverId = null;
var reducedMotion = false;

var tagsEnabled = false;    // Default aus (Plan §5 D2: "Default zeigt nur explizite Kanten")
var foldersEnabled = false;

const REPULSION_STRENGTH = 800;   // ~ Coulomb-Konstante (willkuerlich, durch Augenschein justiert)
const SPRING_LENGTH = 60;          // Ruhelaenge in CSS-Pixeln
const SPRING_STRENGTH = 0.05;
const CENTER_GRAVITY = 0.012;
const DAMPING = 0.85;
const ALPHA_START = 1;
const ALPHA_MIN = 0.005;
const ALPHA_DECAY = 0.985;
const ALPHA_REHEAT = 0.3;          // Drag-Eingriff
const MAX_TICKS_REDUCED = 300;     // Plan §5 D2: ~300 Ticks synchron fuer reduced-motion
const NODE_RADIUS_BASE = 4;
const NODE_RADIUS_PER_LOG = 2;
const NODE_RADIUS_MAX = 12;
const ZOOM_MIN = 0.5;
const ZOOM_MAX = 2.5;
const ZOOM_LABEL_THRESHOLD = 1.2;  // Plan §5 D2: Labels nur bei Zoom > 1.2 oder Hover-Nachbarschaft
const DIM_ALPHA = 0.15;            // Nicht-Nachbarn auf 15% Alpha (Plan §5 D2)
const HOVER_HIT_RADIUS = 14;       // Klick-Toleranz ueber den sichtbaren Radius hinaus
const TAG_CLIQUE_LIMIT = 15;       // Plan §5 D2: Tags auf >15 Knoten erzeugen keine Clique

const COLORS = Object.freeze({
  bg: "#0B0D10",          // wird nicht gezeichnet -- Canvas ist transparent, darunter die .surface
  edge: "#7E8A98",        // explizite Kanten -- gedämpftes Slate
  edgeImplicit: "#7E8A98",// Tag/Ordner-Kanten -- dieselbe Linienfarbe, nur Strichstil
  label: "#C4CDD8",
  spaceOwn: "#4A93F0",
  spaceShared: "#2EB8A6",
  spaceForeign: "#8B93A1",
});

export function init() {
  canvasEl = document.getElementById("overview-graph-canvas");
  if (!canvasEl) return;        // /ui/ ist session-gated -- /ui/login rendert ohne #detail-overview
  ctx = canvasEl.getContext("2d");
  if (!ctx) return;             // Headless / kein Canvas-Support -- Smoke-Skripte müssen abfangen

  dpr = Math.max(1, Math.min(2, window.devicePixelRatio || 1));
  reducedMotion =
    window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var tagsToggle = document.getElementById("overview-graph-toggle-tags");
  var foldersToggle = document.getElementById("overview-graph-toggle-folders");
  if (tagsToggle) tagsToggle.addEventListener("change", function () {
    tagsEnabled = tagsToggle.checked;
    rebuildImplicitEdges();
    draw();
  });
  if (foldersToggle) foldersToggle.addEventListener("change", function () {
    foldersEnabled = foldersToggle.checked;
    rebuildImplicitEdges();
    draw();
  });

  canvasEl.addEventListener("mousedown", onMouseDown);
  canvasEl.addEventListener("mousemove", onMouseMove);
  canvasEl.addEventListener("mouseup", onMouseUp);
  canvasEl.addEventListener("mouseleave", onMouseUp);
  canvasEl.addEventListener("wheel", onWheel, { passive: false });
  canvasEl.addEventListener("dblclick", onDoubleClick);

  // Reagiere auf Spalten-Resize: das Panel wächst, der Canvas muss mitwachsen, sonst
  // verzerren die Knoten. resize() liest die neue CSS-Box und resettet die DPR-Skalierung.
  if (typeof ResizeObserver !== "undefined") {
    var ro = new ResizeObserver(function () { resize(); });
    ro.observe(canvasEl.parentNode || canvasEl);
  } else {
    window.addEventListener("resize", resize);
  }

  resize();
}

export function loadGraph() {
  if (!canvasEl) return Promise.resolve();
  return api("/graph").then(function (data) {
    nodes = (data.nodes || []).map(function (n) {
      return Object.assign({}, n, { x: 0, y: 0, vx: 0, vy: 0, deg: 0 });
    });
    explicitEdges = data.edges || [];
    nodeById = Object.create(null);
    nodes.forEach(function (n) { nodeById[n.id] = n; });
    rebuildImplicitEdges();
    updateEmptyState();
    updateZoomReadout();
    if (nodes.length === 0) {
      // Kein Knoten -- keine Simulation noetig, einfach zeichnen (zeigt ggf. Empty-Hint).
      draw();
      return;
    }
    seedInitialPositions();
    runSimulation();
  }).catch(reportUnexpectedError);
}

function rebuildImplicitEdges() {
  // Tag-/Ordner-Kanten sind reine Client-Ableitungen -- bei jedem Toggle-Wechsel neu
  // berechnen (P8-21: >15-Knoten-Tags erzeugen keine Clique).
  implicitEdges = [];
  if (tagsEnabled) implicitEdges = implicitEdges.concat(buildTagEdges(nodes));
  if (foldersEnabled) implicitEdges = implicitEdges.concat(buildFolderEdges(nodes));
  recomputeDegrees();
}

function recomputeDegrees() {
  var adj = Object.create(null);
  var all = explicitEdges.concat(implicitEdges);
  for (var i = 0; i < all.length; i++) {
    var e = all[i];
    (adj[e.src] = adj[e.src] || Object.create(null))[e.dst] = true;
    (adj[e.dst] = adj[e.dst] || Object.create(null))[e.src] = true;
  }
  for (var j = 0; j < nodes.length; j++) {
    var n = nodes[j];
    n.deg = adj[n.id] ? Object.keys(adj[n.id]).length : 0;
  }
}

function buildTagEdges(nodeList) {
  // Sammelt je Tag die Liste der Knoten-IDs, bildet dann alle ungerichteten Paare.
  // Ein Tag, der auf > TAG_CLIQUE_LIMIT Knoten liegt, wird uebersprungen (P8-21).
  var byTag = Object.create(null);
  for (var i = 0; i < nodeList.length; i++) {
    var n = nodeList[i];
    var tags = n.tags || [];
    for (var t = 0; t < tags.length; t++) {
      (byTag[tags[t]] = byTag[tags[t]] || []).push(n.id);
    }
  }
  var edges = [];
  var seen = Object.create(null);
  Object.keys(byTag).forEach(function (tag) {
    var ids = byTag[tag];
    if (ids.length > TAG_CLIQUE_LIMIT) return;
    for (var a = 0; a < ids.length; a++) {
      for (var b = a + 1; b < ids.length; b++) {
        var lo = ids[a] < ids[b] ? ids[a] : ids[b];
        var hi = ids[a] < ids[b] ? ids[b] : ids[a];
        var key = lo + "|" + hi;
        if (seen[key]) continue;
        seen[key] = true;
        edges.push({ src: ids[a], dst: ids[b], kind: "tag" });
      }
    }
  });
  return edges;
}

function buildFolderEdges(nodeList) {
  // Kante zwischen Knoten im selben (space, folder)-Bucket -- folder != "" (Plan §5 D2).
  // Das ist KEIN Space-Space-Kantenquerverweis -- nur Ordner-interna Struktur.
  var byBucket = Object.create(null);
  for (var i = 0; i < nodeList.length; i++) {
    var n = nodeList[i];
    if (!n.folder) continue;
    var key = n.space + "\u0001" + n.folder;
    (byBucket[key] = byBucket[key] || []).push(n.id);
  }
  var edges = [];
  Object.keys(byBucket).forEach(function (k) {
    var ids = byBucket[k];
    if (ids.length < 2) return;
    for (var a = 0; a < ids.length; a++) {
      for (var b = a + 1; b < ids.length; b++) {
        edges.push({ src: ids[a], dst: ids[b], kind: "folder" });
      }
    }
  });
  return edges;
}

function seedInitialPositions() {
  // Streuung um den Canvas-Mittelpunkt -- Pseudo-Zufall reicht fuer die Startlage, die
  // Simulation laeuft sie ohnehin zusammen.
  var cx = cssWidth / 2;
  var cy = cssHeight / 2;
  var spread = Math.min(cssWidth, cssHeight) / 4;
  for (var i = 0; i < nodes.length; i++) {
    var n = nodes[i];
    if (n.x === 0 && n.y === 0) {
      var angle = (i / Math.max(1, nodes.length)) * 2 * Math.PI;
      n.x = cx + Math.cos(angle) * spread + (Math.random() - 0.5) * 30;
      n.y = cy + Math.sin(angle) * spread + (Math.random() - 0.5) * 30;
    }
    n.vx = 0;
    n.vy = 0;
  }
}

function runSimulation() {
  var alpha = ALPHA_START;
  var rafId = null;

  function tick() {
    if (alpha < ALPHA_MIN) return;
    applyForces(alpha);
    integrate(alpha);
    alpha *= ALPHA_DECAY;
    draw();
    if (alpha >= ALPHA_MIN) {
      rafId = requestAnimationFrame(tick);
    }
  }

  if (reducedMotion) {
    // Plan §5 D2: "Simulation synchron zu Ende rechnen (~300 Ticks), statisch rendern".
    for (var t = 0; t < MAX_TICKS_REDUCED && alpha >= ALPHA_MIN; t++) {
      applyForces(alpha);
      integrate(alpha);
      alpha *= ALPHA_DECAY;
    }
    draw();
  } else {
    rafId = requestAnimationFrame(tick);
  }
}

function applyForces(alpha) {
  // 1. Repulsion paarweise (Plan §5 D2: O(n²), Cutoff-Distanz nicht noetig -- 200 Knoten
  //    reichen nicht an die Komplexitaets-Grenze, und ein Cutoff wuerde nahe Knoten seltsam
  //    behandeln).
  for (var i = 0; i < nodes.length; i++) {
    var a = nodes[i];
    for (var j = i + 1; j < nodes.length; j++) {
      var b = nodes[j];
      var dx = a.x - b.x;
      var dy = a.y - b.y;
      var dist2 = dx * dx + dy * dy + 0.01;
      var dist = Math.sqrt(dist2);
      var force = REPULSION_STRENGTH / dist2;
      var fx = (dx / dist) * force;
      var fy = (dy / dist) * force;
      a.vx += fx;
      a.vy += fy;
      b.vx -= fx;
      b.vy -= fy;
    }
  }

  // 2. Federkraft je Kante -- explizite und implizite gleich behandelt (Plan §5 D2:
  //    "explizit solide (frontmatter/body ununterschieden)" bezieht sich auf den Render-Stil,
  //    nicht die Federstaerke; eine staerkere Frontmatter-Feder waere eine staillschweigend
  //    eingefuehrte Semantik).
  var all = explicitEdges.concat(implicitEdges);
  var cx = cssWidth / 2;
  var cy = cssHeight / 2;
  for (var k = 0; k < all.length; k++) {
    var e = all[k];
    var aa = nodeById[e.src];
    var bb = nodeById[e.dst];
    if (!aa || !bb) continue;
    var ddx = bb.x - aa.x;
    var ddy = bb.y - aa.y;
    var d = Math.sqrt(ddx * ddx + ddy * ddy) + 0.01;
    var stretch = d - SPRING_LENGTH;
    var f = stretch * SPRING_STRENGTH;
    var ffx = (ddx / d) * f;
    var ffy = (ddy / d) * f;
    aa.vx += ffx;
    aa.vy += ffy;
    bb.vx -= ffx;
    bb.vy -= ffy;
  }

  // 3. Zentrums-Gravitation -- haelt den Graphen in der Panel-Mitte, auch wenn der Grossteil
  //    der Knoten am Rand landen wuerde.
  for (var n = 0; n < nodes.length; n++) {
    var node = nodes[n];
    node.vx += (cx - node.x) * CENTER_GRAVITY * alpha;
    node.vy += (cy - node.y) * CENTER_GRAVITY * alpha;
  }
}

function integrate(alpha) {
  for (var i = 0; i < nodes.length; i++) {
    var n = nodes[i];
    n.x += n.vx * alpha;
    n.y += n.vy * alpha;
    n.vx *= DAMPING;
    n.vy *= DAMPING;
  }
}

function draw() {
  if (!ctx) return;
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.clearRect(0, 0, canvasEl.width, canvasEl.height);
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

  if (nodes.length === 0) {
    updateEmptyState();
    return;
  }

  ctx.save();
  ctx.translate(panX, panY);
  ctx.scale(zoom, zoom);

  var all = explicitEdges.concat(implicitEdges);
  var neighbors = hoverId ? neighborSet(hoverId, all) : null;
  var dim = function (id) { return neighbors && !neighbors[id]; };

  drawEdges(all, dim);
  drawNodes(dim);

  ctx.restore();

  // Labels werden in CSS-Koordinaten gerendert (nach restore), damit sie nicht mit-skaliert
  // werden -- ein 12px-Label bei Zoom 0.5 wuerde sonst 6px winzig werden.
  drawLabels(neighbors);
}

function drawEdges(all, dim) {
  ctx.lineWidth = 1;
  ctx.strokeStyle = COLORS.edge;
  for (var i = 0; i < all.length; i++) {
    var e = all[i];
    var a = nodeById[e.src];
    var b = nodeById[e.dst];
    if (!a || !b) continue;
    var isDim = dim(a.id) || dim(b.id);
    ctx.globalAlpha = isDim ? DIM_ALPHA : 1;
    if (e.kind === "tag") {
      ctx.setLineDash([4, 4]);
    } else if (e.kind === "folder") {
      ctx.setLineDash([1.5, 3]);
    } else {
      ctx.setLineDash([]);
    }
    ctx.beginPath();
    ctx.moveTo(a.x, a.y);
    ctx.lineTo(b.x, b.y);
    ctx.stroke();
  }
  ctx.setLineDash([]);
  ctx.globalAlpha = 1;
}

function drawNodes(dim) {
  for (var i = 0; i < nodes.length; i++) {
    var n = nodes[i];
    var r = Math.min(NODE_RADIUS_MAX, NODE_RADIUS_BASE + NODE_RADIUS_PER_LOG * Math.log2(1 + n.deg));
    ctx.globalAlpha = dim(n.id) ? DIM_ALPHA : 1;
    ctx.fillStyle = nodeColor(n);
    ctx.beginPath();
    ctx.arc(n.x, n.y, r, 0, 2 * Math.PI);
    ctx.fill();
  }
  ctx.globalAlpha = 1;
}

function drawLabels(neighbors) {
  if (zoom < ZOOM_LABEL_THRESHOLD && !hoverId) return;
  ctx.fillStyle = COLORS.label;
  ctx.font = '12px "IBM Plex Sans Var", system-ui, sans-serif';
  ctx.textBaseline = "middle";
  for (var i = 0; i < nodes.length; i++) {
    var n = nodes[i];
    if (neighbors && !neighbors[n.id]) continue;
    var r = Math.min(NODE_RADIUS_MAX, NODE_RADIUS_BASE + NODE_RADIUS_PER_LOG * Math.log2(1 + n.deg));
    // Position in CSS-Koordinaten (nach pan/zoom-Transform).
    var sx = n.x * zoom + panX;
    var sy = n.y * zoom + panY;
    ctx.fillText(truncate(n.title, 28), sx + r + 6, sy);
  }
}

function nodeColor(n) {
  // spaceCategory() wuerde hier funktionieren, aber das ist dieselbe Logik wie in tree.js
  // und list.js -- direkt auf den Knoten-Feldern arbeitet es einen Tick schneller und macht
  // die Abhaengigkeit von state.js ueberfluessig (graph.js laedt sich auch ohne State-Init).
  var cat = spaceCategory({ own: n.own, writable: n.shared });
  if (cat === "own") return COLORS.spaceOwn;
  if (cat === "shared") return COLORS.spaceShared;
  return COLORS.spaceForeign;
}

function truncate(s, n) {
  if (!s) return "";
  return s.length <= n ? s : s.slice(0, n - 1) + "\u2026";
}

function neighborSet(id, all) {
  var set = Object.create(null);
  set[id] = true;
  for (var i = 0; i < all.length; i++) {
    var e = all[i];
    if (e.src === id) set[e.dst] = true;
    if (e.dst === id) set[e.src] = true;
  }
  return set;
}

function resize() {
  if (!canvasEl) return;
  var rect = canvasEl.getBoundingClientRect();
  if (rect.width === 0 || rect.height === 0) return;
  cssWidth = rect.width;
  cssHeight = rect.height;
  canvasEl.width = Math.floor(cssWidth * dpr);
  canvasEl.height = Math.floor(cssHeight * dpr);
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  draw();
}

function updateEmptyState() {
  var empty = document.getElementById("overview-graph-empty");
  if (!empty) return;
  var all = explicitEdges.concat(implicitEdges);
  // P8-21: "kein Knoten mit Kante" -- wenn es Knoten gibt, aber keiner eine Kante hat,
  // bleibt der Hinweistext sichtbar (Plan §5 D2).
  var hasAnyEdge = all.length > 0;
  empty.hidden = hasAnyEdge;
}

function updateZoomReadout() {
  var readout = document.getElementById("overview-graph-zoom");
  if (!readout) return;
  readout.textContent = (zoom * 100).toFixed(0) + "%";
}

function graphCoordsFromEvent(e) {
  var rect = canvasEl.getBoundingClientRect();
  var sx = e.clientX - rect.left;
  var sy = e.clientY - rect.top;
  // Rueckgaengig von pan/zoom: world = (screen - pan) / zoom.
  return { x: (sx - panX) / zoom, y: (sy - panY) / zoom };
}

function hitTest(world) {
  for (var i = 0; i < nodes.length; i++) {
    var n = nodes[i];
    var r = Math.min(NODE_RADIUS_MAX, NODE_RADIUS_BASE + NODE_RADIUS_PER_LOG * Math.log2(1 + n.deg));
    var dx = world.x - n.x;
    var dy = world.y - n.y;
    if (dx * dx + dy * dy <= Math.max(r, HOVER_HIT_RADIUS) * Math.max(r, HOVER_HIT_RADIUS)) return n;
  }
  return null;
}

function onMouseDown(e) {
  if (e.button !== 0) return;
  var world = graphCoordsFromEvent(e);
  var hit = hitTest(world);
  if (hit) {
    dragNode = hit;
    dragNode.fixed = true;
  } else {
    panStart = { x: e.clientX, y: e.clientY, panX: panX, panY: panY };
  }
}

function onMouseMove(e) {
  var world = graphCoordsFromEvent(e);
  if (dragNode) {
    dragNode.x = world.x;
    dragNode.y = world.y;
    dragNode.vx = 0;
    dragNode.vy = 0;
    draw();
    return;
  }
  if (panStart) {
    panX = panStart.panX + (e.clientX - panStart.x);
    panY = panStart.panY + (e.clientY - panStart.y);
    draw();
    return;
  }
  var hit = hitTest(world);
  var newHover = hit ? hit.id : null;
  if (newHover !== hoverId) {
    hoverId = newHover;
    draw();
  }
}

function onMouseUp() {
  if (dragNode) {
    dragNode.fixed = false;
    dragNode = null;
  }
  panStart = null;
}

function onWheel(e) {
  e.preventDefault();
  var factor = e.deltaY < 0 ? 1.1 : 1 / 1.1;
  var newZoom = Math.max(ZOOM_MIN, Math.min(ZOOM_MAX, zoom * factor));
  // Zoom um den Maus-Punkt herum -- Bildausschnitt soll beim Zoomen stabil bleiben.
  var rect = canvasEl.getBoundingClientRect();
  var sx = e.clientX - rect.left;
  var sy = e.clientY - rect.top;
  panX = sx - (sx - panX) * (newZoom / zoom);
  panY = sy - (sy - panY) * (newZoom / zoom);
  zoom = newZoom;
  updateZoomReadout();
  draw();
}

function onDoubleClick() {
  // Plan §5 D2: Doppelklick auf Hintergrund setzt Ansicht zurueck.
  zoom = 1;
  panX = 0;
  panY = 0;
  updateZoomReadout();
  draw();
}
