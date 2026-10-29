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
// WebWorker-Simulation (Datenmenge ist klein genug fuer requestAnimationFrame), Mobile-Pinch-
// Zoom (Step 7b-W Desktop-first). Seit P9 Step E (b) überleben die Positionen immerhin den
// Wiedereintritt in die Übersicht innerhalb einer Sitzung -- der Seed ist ohnehin deterministisch
// (P8.6-D2), nur die Simulation begann nach jedem Eintritt von vorn.
//
// **Settle-Zeit bei 200 Knoten (Fix A, Plan §9.4.6 Befund A, 2026-09-02):** mit den
// urspruenglichen Konstanten (ALPHA_DECAY 0.985 / ALPHA_MIN 0.005) kam die Simulation
// **gemessen 5.95 s** zur Ruhe (351 Ticks, p8_22_smoke.py gegen den 200-Knoten-Wegwerf) --
// der damalige Kommentar hier "200 Knoten erreichen Ruhe in <3s" war damit widerlegt, nicht nur
// ungenau. Konstanten danach auf ALPHA_DECAY 0.97 / ALPHA_MIN 0.01 gesetzt: ticks =
// ln(ALPHA_MIN)/ln(ALPHA_DECAY) = ln(0.01)/ln(0.97) ≈ 151 Ticks ≈ 2.52 s bei 60 fps -- mit
// Marge unter dem 3s-Budget (der Plan-Vorschlag ALPHA_DECAY 0.97 allein, ALPHA_MIN bei 0.005
// belassen, waere 174 Ticks ≈ 2.90 s gewesen: ~40 ms Marge auf einem Kriterium, das gerade erst
// gerissen war -- deshalb beide Konstanten, Nikinger-Entscheidung 2026-09-02, Option (a) mit
// Marge). Erneut mit `p8_22_smoke.py` gegen den 200-Knoten-Wegwerf gemessen, nicht nur
// gerechnet -- Zahl steht im Phase-Head-Session-Block und in Plan §9.4.6.

import { api, reportUnexpectedError } from "./api.js";
import { spaceCategory, state, TYPE_LABELS } from "./state.js";
import { selectItem } from "./editor.js";
import { withLoading } from "./loading.js";

// P10.5 Block 8, Schritt 8.6 (KA-3): die deutschen Bezeichnungen fuer Typ und Status der
// Karte. `TYPE_LABELS` kommt aus `state.js` (dieselbe Tabelle wie der Anlegen-Dialog),
// die Statuse kommen aus `BUCKET_LABELS` -- plus "aktiv", die Notiz-Status, die es nur beim
// Typ Notiz gibt.
var STATUS_LABELS = {
  active: "Aktiv",
  open: "Offen",
  doing: "In Arbeit",
  done: "Erledigt",
  archived: "Archiv",
};

var nodes = [];
var explicitEdges = [];   // {src, dst, kind} -- vom Server (frontmatter|body)
var implicitEdges = [];   // {src, dst, kind} -- vom Client (tag|folder)
var nodeById = Object.create(null);
// P10.5 Block 14, Schritt 14.2: die **Regionen** (das Ergebnis von `computeRegions()`).
// Die Gravitation zieht jeden Knoten zu dem Anker **seines** Space -- ohne diese Karte wuesste
// die Kraftsimulation nicht, wohin. Sie wird beim Saeen gesetzt und beim Laden neu berechnet.
var spaceRegions = null;

var canvasEl = null;
var ctx = null;
// P10.5, Block 4 (2026-10-22, Z4): der Container der Karte traegt den Ladezustand.
var graphEl = null;
var cssWidth = 0;
var cssHeight = 0;
var dpr = 1;

var zoom = 1;
var panX = 0;
var panY = 0;
// P10.5 Block 14, Schritt 14.3 (Plan §2.5): die Kamera passt sich **einmal** je Kartenaufbau
// ein (nach dem Einschwingen, nicht nach einem Drag). `viewFitted` merkt, dass das schon
// geschehen ist; `viewTouchedByUser` merkt, dass der Nutzer **selbst** gezoomt oder verschoben
// hat -- **seine Ansicht gewinnt** (Plan §2.5: "Hat der Nutzer in dieser Sitzung schon gezoomt
// oder verschoben, passt die Karte nicht neu ein").
var viewFitted = false;
var viewTouchedByUser = false;

var dragNode = null;       // Knoten, der gerade gezogen wird
var panStart = null;        // Pan-Geste: {startX, startY, origPanX, origPanY}
var hoverId = null;
var reducedMotion = false;
// Fix C (Plan §9.4.6 Befund C, 2026-09-02): {x, y, node} vom mousedown -- node ist null bei
// einem Hintergrund-Press. onMouseUp vergleicht die Pointer-Position dagegen (CLICK_SLOP) und
// oeffnet das Item nur, wenn sich der Pointer kaum bewegt hat -- ein Drag ist kein Klick.
var pressStart = null;

var tagsEnabled = false;    // Default aus (Plan §5 D2: "Default zeigt nur explizite Kanten")
var foldersEnabled = false;

// -- P10.5 Block 8: Zustand der Karte (C2) ----------------------------------------------------
var lobeCache = null;        // {lobes: [{space, color, outer: [[x,y]…], inner: [[x,y]…]|null}]}
                              // -- **Punkte, kein Path2D**: ein `Path2D` lässt sich im Testharness
                              // nicht messen, Punkte schon (und der Aufbau ist der teure Teil).
var layoutSavePending = false;  // Plan 8.5: das Drosseln des Speicherns
var pendingReducedStart = false;  // Schritt 8.7: der reduced-motion-Aufbau wartet auf die Box
var pinnedIds = Object.create(null);  // Plan 8.5: Knoten mit gemerkter Position -- sie werden
                                      // beim nächsten Laden nicht wieder auseinandergeschoben
var searchQuery = "";        // Plan 8.6 (KA-3): die Suche im Titel
var filterType = "";         // Plan 8.6: "" = alle Typen, sonst "note"/"task"
var filterStatus = "";       // Plan 8.6: "" = alle Status, sonst "open"/"doing"/"done"
var statusEl = null;         // die Statuszeile der Werkzeugleiste (Plan 8.5/8.6)
var hitsEl = null;           // die Trefferzahl der Suche -- **eigenes** Feld (Plan 8.6)

// -- P9 Step E: Reload-Overload (Plan §7.2a, Abnahme P9-33) ----------------------------------
//
// `loadGraph()` wurde bei **jedem** Aufruf zu einem vollen `api("/graph")`-Abruf. Aufrufer sind
// `app.js` (Home-Knopf, Refresh-Knopf, Bootstrap) -- seit P8.6 N.8 kommt ESC dazu, der Weg in die
// Übersicht wird also häufiger gegangen, nicht seltener. Das ist der gemeldete "Reload-Overload"
// (`p8x_ui_polish_notes.md` §2.1).
//
// **Die Korrektur am Plan-Vorschlag, datiert 2026-09-26 (Code schlägt Plan, wie Hard Rule der
// Working style verlangt):** Plan §7.2(a) wollte die Signatur aus "Knotenzahl + Kantenzahl +
// höchstem `updated`" bilden und nennt als Quelle ausdrücklich den Graph-Payload. Der
// `/api/v1/graph`-Knoten hat aber **genau neun Felder** (`api.py :: _graph_get`, Z. 698-708) und
// **kein `updated`, kein `version`** -- die Signatur ließe sich dort gar nicht bilden, und ein
// zehntes Feld wäre eine API-Contract-Öffnung, die ausdrücklich nicht zu diesem Step gehört
// (P9-M, §7.2 "Was dieser Step ausdrücklich nicht anfasst").
//
// **Was stattdessen trägt, ohne eine einzige neue Server-Antwort:** das `/api/v1/overview`-
// Payload, das der Client ohnehin holt -- beim Bootstrap, alle 20 s im Zähler-Poll, bei
// Fokus/Sichtbarkeit (`app.js :: pollCounters`) und nach jedem Schreibvorgang. Reduziert auf eine
// Signatur liegt es in `state.js :: overviewToken()`, gesetzt in `list.js :: loadOverview()`,
// gelesen hier. Warum die Signatur dort und nicht hier: siehe das Feld `state.graphToken`.
//
// **Bekannte, benannte Grenze** (aus `state.js :: overviewToken()`): ändert ein Item nur seine
// Tags und ist es in seinem Space nicht mehr unter den fünf zuletzt geänderten Items, bleibt
// der Graph bis zum manuellen Refresh stehen -- dieses Item ist dann aber auch in der
// Übersicht daneben nicht zu sehen.
var tokenAtFetch = null;       // Signatur, die der letzte /graph-Abruf abgedeckt hat

const REPULSION_STRENGTH = 800;   // ~ Coulomb-Konstante (willkuerlich, durch Augenschein justiert)
const SPRING_LENGTH = 60;          // Ruhelaenge in CSS-Pixeln
const SPRING_STRENGTH = 0.05;
const DAMPING = 0.85;
// **P10.5 Block 14, Schritt 14.2:** `CENTER_GRAVITY` (0,012) und `ALPHA_START` (1) sind
// **weg** -- ersetzt, nicht zusaetzlich (Plan §2.4): die Gravitation zieht jetzt zum **eigenen
// Space-Anker** (`ANCHOR_GRAVITY`), und die Startenergie ist die **gesaete** (`ALPHA_START_SEEDED`).
// Die beiden Konstanten stehen im 14.2-Block weiter unten.
// Fix A (Plan §9.4.6 Befund A, 2026-09-02): 0.005/0.985 brauchten 351 Ticks (gemessen 5.95 s
// bei 200 Knoten, siehe Modul-Header oben) -- 0.01/0.97 brauchen ln(0.01)/ln(0.97) ≈ 151 Ticks
// ≈ 2.52 s, mit Marge unter dem 3s-Budget.
const ALPHA_MIN = 0.01;
const ALPHA_DECAY = 0.97;
const ALPHA_REHEAT = 0.3;          // Drag-Eingriff
// MAX_TICKS_REDUCED bleibt 300 (Plan §5 D2), ist aber seit Fix A nicht mehr die bindende
// Grenze fuer prefers-reduced-motion -- die Schleife endet jetzt schon nach ~151 Ticks am
// ALPHA_MIN-Abbruch (siehe runSimulation()), 300 wird nie erreicht. Konstante unveraendert
// gelassen (Plan §9.4.6 Befund A nennt nur ALPHA_DECAY/ALPHA_MIN, nicht diese), der
// Seiteneffekt ist in Plan §5 D2 vermerkt, nicht stillschweigend.
const MAX_TICKS_REDUCED = 300;     // Plan §5 D2: ~300 Ticks synchron fuer reduced-motion
const NODE_RADIUS_BASE = 4;
const NODE_RADIUS_PER_LOG = 2;
const NODE_RADIUS_MAX = 12;
const ZOOM_MIN = 0.5;
const ZOOM_MAX = 2.5;
const ZOOM_LABEL_THRESHOLD = 1.2;  // Plan §5 D2: Labels nur bei Zoom > 1.2 oder Hover-Nachbarschaft
// P10.5 Block 8, Schritt 8.4 (D-1b): der Plan setzt 0,15 auf 0,45 -- "Abdunkeln nur bei Hover
// oder Treffer", der Ruhezustand ohne Fokus bleibt **voll deckend**. Die alte 0,15 war der
// P8-Wert und make-die-Karte-zur-Asche.
const DIM_ALPHA = 0.45;            // Nicht-Nachbarn auf 45% Alpha (Plan §Block 8, Schritt 8.4)
const HALF_ALPHA = 0.5;            // der zweite Ring um den Fokus (Plan §Block 8, Schritt 8.4)
const HOVER_HIT_RADIUS = 14;       // Klick-Toleranz ueber den sichtbaren Radius hinaus
const TAG_CLIQUE_LIMIT = 15;       // Plan §5 D2: Tags auf >15 Knoten erzeugen keine Clique
// Fix C (Plan §9.4.6 Befund C, 2026-09-02): maximale Pointer-Bewegung zwischen mousedown und
// mouseup, die noch als Klick (nicht Drag) zaehlt -- Klick oeffnet das Item.
const CLICK_SLOP = 4;

// -- P10.5 Block 8: Gehirnkarte C2 (Plan §Block 8, Schritt 8.1-8.7) --------------------------------
//
// Der Stil C2 ("Nervenbahnen", Vorlage `docs/concepts/phase10_karte_c_stil_2.svg`) hat vier
// Teile: **Lappen** (der Koerper, in Space-Gruppen geteilt), **Furchen** (die Grenze zwischen
// zwei Lappen), **Bahnen** (geschwungene Kanten) und **Zellen** (die Knoten). Die Zahlen
// unten sind die Vorgaben aus dem Plan, nicht Schaetzwerte.
const LOBE_CELL_PX = 8;        // Zellgröße des Lappen-Rasters (Plan 8.1)
const LOBE_REACH = 48;         // Radius der Körpermaske um den nächsten Knoten (Plan 8.1)
const LOBE_MAX_CELLS = 200;    // Deckel je Achse -- ein weit auseinandergezogenes Layout darf
                               // das Raster nicht unbegrenzt wachsen lassen
const LOBE_INNER_CELLS = 3;    // Erosionstiefe der inneren Kontur (3 Zellen = 24 px)
// P10.5 Block 14, Schritt 14.6 (Plan `docs/concepts/phase10_5_block14_6_plan.md` §2.1):
// der **Schließ-Radius** der Körpermaske. Das Layout aus Block 14 stellt die Spaces weit
// auseinander — die Lappen zweier Spaces berühren sich **nie** (gemessen: 5 Inseln, 0
// Furche-Zellen). `LOBE_CLOSE_PX > 0` **schließt** die Maske: erst um `D` **wachsen**, dann
// um `D` **schrumpfen**. Die Lücken zwischen den Inseln füllen sich, der **äußere** Rand
// bleibt (fast) wo er ist -- und **kein Knoten bewegt sich**.
// `0` = die Inseln von Block 14 (der Stand vor dem Schließen). Der Wert wird **gemessen**
// (Plan §3, Entscheidung E1), nicht gesetzt.
const LOBE_CLOSE_PX = 0;
const EDGE_CURVE = 0.24;       // Krümmung der Bahn: Kontrollpunkt = Mitte + 0,24·(−dy, dx)
const EDGE_WIDTH_BASE = 1;     // Plan 8.2: Breite = 1 + log2(1 + min(deg(a), deg(b)))
const CANVAS_SURFACE = "#14181D";  // `--surface` -- die Fläche unter dem Canvas; Mix-Ziel für
                                   // den dunkleren Ton der inneren Kontur (Plan 8.1)
const LAYOUT_KEY_PREFIX = "sfx:graph:layout:v1:";  // Plan 8.5 (KA-2)
const LAYOUT_MAX_ENTRIES = 2000;                    // Plan 8.5
const LAYOUT_SAVE_DELAY_MS = 1000;                  // Plan 8.5: gedrosselt 1 s

// -- P10.5 Block 14, Schritt 14.1: das Kartenlayout als Weltgenerator ----------------------------
//
// Drei Schichten, wie ein Weltgenerator (Plan
// `docs/concepts/phase10_5_block14_kartenlayout_plan.md` §1): der **Seed** bestimmt zuerst die
// groben Regionen, darin die Strukturen, darin das Detail -- "zufaellig, aber geordnet".
//
//   L1  eine **Region je Space**     -- der eigene Space in der Mitte, die anderen auf einer
//                                       Goldwinkel-Spirale darum; die **Reihenfolge** ist der
//                                       Hash des Space-Namens (nicht die Item-Zahl: die
//                                       Item-Zahl waechst mit jedem neuen Item, der Hash nicht)
//   L2  **Ordner-Inseln** je Region  -- die Ordner auf einer kleinen Spirale um den Anker,
//                                       der Hash des Ordnernamens entscheidet die Reihenfolge
//   L3  **Items** in der Insel        -- Goldwinkel-Spirale (Sonnenblumenmuster: dicht, ohne
//                                       Ueberlappung), Reihenfolge = Hash der Item-ID
//
// Der **Zufall** ist `seedJitter()` (FNV-1a ueber die ID) -- **kein** `Math.random()`
// (P8.6-D2: die Karte darf beim Oeffnen nicht "fliegen").
//
// **Alle Zahlen sind Startwerte**, justiert durch Messung in Schritt 14.4 (Plan §2.1) --
// nicht geschaetzt uebernommen.
//
// **P10.5 Block 14, Schritt 14.4: sie sind gemessen.** Der Treiber
// `phase10_5_finishing/probes/p105_b14_startwerte.py` faehrt die Browser-Probe je Wert
// (5 Spaces, 152 Items) und vergleicht die Zellen; die Rohdaten stehen in
// `phase10_5_finishing/probes/p105_b14_startwerte_messung.json`.
//
// **Die Regel der Wahl (Schritt 14.4):** der Wert bleibt, wenn er die **Stabilitaet** haelt
// (Median <= 2 px **und** Maximum <= 3 px) *und* die groesste **Trennungs-Marge** hat (der
// kleinste Abstand "eigener Space-Schwerpunkt minus naechster fremder" ueber alle Knoten --
// 0 hiesse: die Zelle kippt beim naechsten Item). Jeder Wert in beide Richtungen ist
// gemessen: der Nachbarwert ist jeweils schlechter.
const REGION_ITEM_STEP = 22;    // gemessen in 14.4 -- der Radius je Item (30 => Stabilitaet rot)
const REGION_PAD = 30;          // gemessen in 14.4 -- der Grundradius je Region (50 => Maximum 23,8 px)
const REGION_GAP = 40;          // gemessen in 14.4 -- der Abstand zweier Regionen (0 => Maximum 28,3 px)
const ISLAND_FACTOR = 0.55;     // gemessen in 14.4 -- der Anteil der Region, den die
                                //   Ordner-Inseln einnehmen (0,35 => Stabilitaet rot)
const ITEM_STEP = 14;           // gemessen in 14.4 -- der Abstand der Items in der Insel
const ITEM_JITTER_PX = 8;       // gemessen in 14.4 -- die Amplitude des Item-Jitters
const GOLDEN_ANGLE = 2.399963229728653;  // 137,50776405003785 Grad in Radiant

// -- P10.5 Block 14, Schritt 14.2: L4 -- die Entspannung ---------------------------------------
//
// Die vierte Schicht (Plan §2.4): nach dem Seed zieht jeder Knoten zu **seinem** Space-Anker
// (vorher: zur Leinwandmitte -- das zog alle Spaces auf einen Punkt und liess die Regionen
// verschmelzen), und die Federn **quer** zwischen zwei Spaces sind **schwach und lang** (eine
// Querverbindung soll zwei Spaces nicht ineinander ziehen).
//
// **Die Startenergie ist kleiner:** der Seed liegt schon nah am Ziel, also reichen weniger
// Ticks (`ALPHA_START_SEEDED` 0,5 statt `ALPHA_START` 1 -- die Zahl der Ticks ist
// `ln(ALPHA_MIN / ALPHA_START) / ln(ALPHA_DECAY)`).
//
// **Schritt 14.4: die vier Werte sind gemessen, nicht gesetzt** (Plan §2.4: "in 14.4 werden
// sie **gemessen** (nicht gesetzt)"). Dieselbe Regel wie oben: die Stabilitaet muss halten
// (Median <= 2 px **und** Maximum <= 3 px), und die Trennungs-Marge muss die groesste sein.
const ANCHOR_GRAVITY = 0.02;           // gemessen in 14.4 -- der Zug zum eigenen Anker
                                        //   (0,04 => Maximum 18,8 px; 0,08 => Median 3,2 px: rot)
const CROSS_SPRING_FACTOR = 0.15;      // gemessen in 14.4 -- die Staerke der Querfeder
                                        //   (0,3 => Median 5,0 px: rot; 0 => die Welt waechst auf 1334 px)
const CROSS_SPRING_LENGTH_FACTOR = 3;  // gemessen in 14.4 -- die Laenge der Querfeder
                                        //   (der einzige Wert, bei dem Median **und** Maximum halten)
const ALPHA_START_SEEDED = 0.5;        // gemessen in 14.4 -- die Startenergie
                                        //   (0,75 => Median 77,0 px: rot; 0,25 => 1769 ms, Welt 1214 px)

// -- P10.5 Block 14, Schritt 14.35: die Beschriftungen ohne Ueberlappung -------------------------
//
// Plan §2.7: die Beschriftungs-Rechtecke (Breite aus `ctx.measureText`, Hoehe = die Schrift)
// in der Reihenfolge des **Vorrangs** sammeln; ueberlappt ein Rechteck ein schon gezeichnetes,
// wird es **nicht** gezeichnet. Reihenfolge = Fokus → erster Ring → Suchtreffer → Rest nach Grad
// absteigend. Der Fokus-Knoten verliert seine Beschriftung **nie**.
//
// **Reine Zeichenlogik:** die Positionen der Knoten aendern sich nicht.
const LABEL_FONT_SIZE = 12;   // die Schrift der Beschriftung (px) -- Plan 8.6
const LABEL_FONT = LABEL_FONT_SIZE + 'px "IBM Plex Sans Var", system-ui, sans-serif';
const LABEL_HEIGHT = LABEL_FONT_SIZE;  // die Hoehe des Beschriftungs-Rechtecks (px)
const LABEL_OFFSET = 6;       // der Abstand zwischen Knotenrand und Text (px)

// -- P10.5 Block 14, Schritt 14.3: die Kamera einpassen ----------------------------------------
//
// Plan §2.5: nach dem **ersten** Einschwingen je `loadGraph()` (nicht nach einem Drag) passt
// die Kamera den Inhalt ein -- Umriss der sichtbaren Knoten plus `FIT_MARGIN`, Zoom so, dass
// der Inhalt **in** die Leinwand passt, Pan auf die **Mitte** des Umrisses.
//
// **Nie ueber 100 %:** eine kleine Karte wird nicht aufgeblasen (Plan §2.5). Der Unterwert ist
// `ZOOM_MIN` (E3: der Ausfuehrer senkt ihn, wenn 200 Knoten bei 0,5 nicht passen -- der
// gemessene Wert steht im Bericht zu 14.3).
// Der Rand um den Inhalt -- **56 px, gemessen in 14.5** (Plan §2.5; der Wert 40 px war der
// Startwert des Plans).
//
// **Warum nicht 40 px (gemessen, Schritt 14.5, `probes/p105_b14_karte_bilder.json`):** die
// Kamera passt den **Umriss der sichtbaren Knoten** ein -- die **Lappen-Kontur** reicht aber
// bis zu `LOBE_REACH` (48 px) ueber den aeussersten Knoten (das Raster beginnt genau dort).
// Mit 40 px Rand stand die Kontur auf der **begrenzenden** Achse **3,8 px ueber dem
// Leinwandrand** (links und rechts; die senkrechte Achse hatte 115 px Luft). 56 px sind die
// **8 px Luft ueber der theoretischen Grenze** (48 px) und der Wert, den der Plan §2.5 dafuer
// nennt. **Die Kosten (gemessen):** der Fuellgrad faellt von 93,6 % auf 91,1 %, der Zoom von
// 92 % auf 90 % -- beides weit ueber der 60-%-Schwelle der Abnahme P10.5-67.
const FIT_MARGIN = 56;

const COLORS = Object.freeze({
  bg: "#0B0D10",          // wird nicht gezeichnet -- Canvas ist transparent, darunter die .surface
  edge: "#7E8A98",        // explizite Kanten -- gedämpftes Slate
  edgeImplicit: "#7E8A98",// Tag/Ordner-Kanten -- dieselbe Linienfarbe, nur Strichstil
  label: "#C4CDD8",
  spaceOwn: "#4A93F0",
  spaceShared: "#2EB8A6",
  spaceForeign: "#8B93A1",
  doing: "#3E8DF3",       // P10.5 7.7 (KA-5): statischer Ring um "doing"-Knoten, Wert von --accent (nicht spaceOwn: ein eigener Knoten wäre sonst farbgleich zum Ring)
  accent: "#3E8DF3",     // P10.5 Block 8 (8.4): der Fokus und seine Bahnen -- `--accent`
});

export function init() {
  graphEl = document.getElementById("overview-graph");
  canvasEl = document.getElementById("overview-graph-canvas");
  if (!canvasEl) return;        // /ui/ ist session-gated -- /ui/login rendert ohne #detail-graph
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

  // -- P10.5 Block 8, Schritt 8.5/8.6 (KA-2/KA-3): die Werkzeugleiste der Karte ----------
  // Suche (Titel-Teilstring), Typ- und Statusauswahl, der Knopf "Layout zurücksetzen" und
  // die Statuszeile. Alles **optional**: fehlt ein Element (alte Markup-Version, Testharness),
  // läuft die Karte weiter -- kein harter Fehler, kein halber Zustand.
  var searchInput = document.getElementById("overview-graph-search");
  if (searchInput) searchInput.addEventListener("input", function () {
    searchQuery = (searchInput.value || "").trim().toLowerCase();
    updateHitCount();
    draw();
  });
  var typeSelect = document.getElementById("overview-graph-filter-type");
  if (typeSelect) typeSelect.addEventListener("change", function () {
    filterType = typeSelect.value || "";
    draw();
  });
  var statusSelect = document.getElementById("overview-graph-filter-status");
  if (statusSelect) statusSelect.addEventListener("change", function () {
    filterStatus = statusSelect.value || "";
    draw();
  });
  var resetLayout = document.getElementById("overview-graph-reset-layout");
  if (resetLayout) resetLayout.addEventListener("click", function () {
    clearStoredLayout();
    setGraphStatus("Layout zurückgesetzt");
    draw();
  });
  statusEl = document.getElementById("overview-graph-status");
  hitsEl = document.getElementById("overview-graph-hits");

  canvasEl.addEventListener("mousedown", onMouseDown);
  canvasEl.addEventListener("mousemove", onMouseMove);
  canvasEl.addEventListener("mouseup", onMouseUp);
  // Fix C (Plan §9.4.6 Befund C, 2026-09-02): eigener Handler statt weiterhin `onMouseUp` --
  // ein Pointer, der das Canvas waehrend eines Press verlaesst, ist nie ein Klick. Vorher
  // teilten sich "mouseup" und "mouseleave" denselben Handler; das war unproblematisch, solange
  // der Handler nur Drag/Pan zuruecksetzte, waere aber mit der neuen Klick-Erkennung in
  // `onMouseUp` zur Falle geworden (Drag-off-canvas haette sonst eine Selektion ausgeloest).
  canvasEl.addEventListener("mouseleave", onMouseLeave);
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

// `opts.force` holt die Daten unbedingt neu -- nur der **explizite** Refresh-Knopf benutzt das
// (der Knopf heißt "aktualisieren"; der Home-Knopf ist der Weg, den P9-33 misst). Der
// Bootstrap-Aufruf braucht es nicht: `tokenAtFetch === null` heißt "noch nie geholt".
export function loadGraph(opts) {
  if (!canvasEl) return Promise.resolve();
  var force = !!(opts && opts.force);
  if (!force && tokenAtFetch !== null && state.graphToken !== null
      && state.graphToken === tokenAtFetch) {
    // (a) Nichts geändert -- kein Abruf, kein Neuaufbau, keine Simulation neu (P9-34: die Karte
    // springt beim Wiedereintritt nicht). `resize()` zieht die Canvas-Box neu ein, falls der
    // Editor den Detail-Slot in der Zwischenzeit belegt hatte, und zeichnet selbst.
    redrawAfterReentry();
    return Promise.resolve();
  }
  // P10.5, Block 4 (2026-10-22, Z4): der Ladezustand ab 200 ms — die Karte holt ihre
  // Knoten in einem Abruf, der auf der langsamen Strecke (M1) Sekunden braucht.
  return withLoading(graphEl, api("/graph")).then(function (data) {
    var previousById = nodeById;
    nodes = (data.nodes || []).map(function (n) {
      // (b) P9-34: eine bekannte ID behält x/y. Vorher bekam **jeder** Knoten `x: 0, y: 0`, und
      // `seedInitialPositions()` verteilte daraufhin den ganzen Ring neu -- der Sprung beim
      // Wiedereintritt kam also nicht aus dem Jitter (der ist seit P8.6-D2 deterministisch),
      // sondern daraus, dass die Simulation nach jedem Eintritt von vorn begann. Nur neue
      // Knoten bleiben bei 0/0 und werden gesät.
      var prev = previousById[n.id];
      return prev
        ? Object.assign({}, n, { x: prev.x, y: prev.y, vx: 0, vy: 0, deg: 0 })
        : Object.assign({}, n, { x: 0, y: 0, vx: 0, vy: 0, deg: 0 });
    });
    explicitEdges = dedupeEdges(data.edges || []);
    nodeById = Object.create(null);
    nodes.forEach(function (n) { nodeById[n.id] = n; });
    rebuildImplicitEdges();
    populateFilters();
    updateEmptyState();
    updateZoomReadout();
    // Die Signatur wird NACH dem Abruf gesetzt, nicht davor: ein /overview, das während des
    // laufenden Abrufs eintrifft, soll den nächsten Eintritt neu laden lassen, nicht diesen.
    tokenAtFetch = state.graphToken;
    // Phase 8.6 Block C C3 / [VERIFY] V115: der ResizeObserver (`init()` Z. 141-142) feuert
    // zwar beim ersten `observe()`, aber zu diesem Zeitpunkt ist `.overview__graph` im neuen
    // Grid möglicherweise 0x0 -- das Grid rendert erst nach dem CSS-Layout-Pass, und der
    // Observer feuert genau einmal beim observe() (Spec: https://www.w3.org/TR/resize-observer/).
    // Ohne den expliziten resize() hier würde `seedInitialPositions()` mit der 0x0-Box
    // rechnen und die Knoten auf einen Punkt in der oberen linken Ecke legen. requestAnimationFrame
    // garantiert, dass resize() nach dem nächsten Layout-Pass läuft (Browser hat das Grid dann
    // committed). [VERIFY] V115: gemessen, dass der ResizeObserver allein beim ersten Mount
    // nicht ausreicht -- der Fix ist drei Zeilen, kein neuer Mechanismus.
    //
    // **P10.5 Block 8, Schritt 8.7 (reduced motion, Abnahme P10.5-40):** im reduced-motion-Pfad
    // läuft der Aufbau **ohne** requestAnimationFrame -- 0 Animationsframes aus `graph.js`.
    // Vorher stand auch dieser Aufbau in einem rAF, und die Abnahme verlangt 0. Der Canvas kann
    // beim ersten Laden noch 0x0 sein; dann wartet der Aufbau auf den ResizeObserver
    // (`resize()`), ebenfalls ohne rAF.
    if (reducedMotion) {
      resize();
      if (cssWidth > 0 && cssHeight > 0) {
        startLayout();
      } else {
        pendingReducedStart = true;   // `resize()` startet den Aufbau, sobald die Box steht
      }
      return;
    }
    requestAnimationFrame(function () {
      if (canvasEl && !canvasEl.isConnected) return;
      resize();
      if (nodes.length === 0) {
        // Kein Knoten -- keine Simulation noetig, einfach zeichnen (zeigt ggf. Empty-Hint).
        draw();
        return;
      }
      startLayout();
    });
  }).catch(reportUnexpectedError);
}

// Wiedereintritt ohne Datenabruf. Gleiches rAF-Fenster wie der Abruf-Pfad oben, damit die Box
// nach dem Layout-Pass stimmt -- der Canvas war während eines offenen Editors 0x0 groß.
function redrawAfterReentry() {
  requestAnimationFrame(function () {
    if (!canvasEl || !canvasEl.isConnected) return;
    // `resize()` zeichnet selbst, aber nur wenn die Box von 0x0 gewachsen ist. Der zweite
    // `draw()` deckt den Fall ab, in dem der Canvas noch 0x0 ist (Editor weiterhin offen) --
    // der ResizeObserver würde das beim Wiedereinblenden zwar auch holen, sein Fallback ohne
    // Observer (`window.addEventListener("resize", …)`) aber nicht.
    resize();
    draw();
  });
}

// P8.6-D1 (P8.6-N): dieselbe Beziehung -- einmal als Body-Link und einmal als
// Frontmatter-Eintrag -- liefert zwei Kanten aus `store.links_all()` (api.py:712).
// Der Server dedupliziert bewusst nicht (kein Cross-`kind`-Dedup in
// `index.py :: replace_item_links`). Hier zusammenfassen und nicht dort: eine
// neunte P1-Contract-Oeffnung waere das teuerste Mittel fuer einen Zeichenfehler
// (Nikinger-Entscheidung 2026-09-09, Plan P8.6-N). `kind` des ersten Treffers
// gewinnt. Bei der Uebernahme deduplizieren, **nicht** erst in `drawEdges()` --
// dann waere die Doppelkante aus dem Bild, aber in der Kanten-Zaehlung stuende
// sie weiterhin.
function dedupeEdges(edges) {
  var seen = Object.create(null);
  var out = [];
  for (var i = 0; i < edges.length; i++) {
    var e = edges[i];
    var key = e.src < e.dst ? e.src + "|" + e.dst : e.dst + "|" + e.src;
    if (seen[key]) continue;
    seen[key] = true;
    out.push(e);
  }
  return out;
}

function rebuildImplicitEdges() {
  // Tag-/Ordner-Kanten sind reine Client-Ableitungen -- bei jedem Toggle-Wechsel neu
  // berechnen (P8-21: >15-Knoten-Tags erzeugen keine Clique).
  implicitEdges = [];
  if (tagsEnabled) implicitEdges = implicitEdges.concat(buildTagEdges(nodes));
  if (foldersEnabled) implicitEdges = implicitEdges.concat(buildFolderEdges(nodes));
  // P9 Step E / P9-36, **[VERIFY] V118 vom Nikinger beantwortet 2026-10-05: eine Linie.**
  // *"Wenn A auf B verlinkt, ist B für A automatisch relevant."* Die **explizite** Kante
  // gewinnt und bleibt durchgezogen; die implizite Tag-/Ordner-Kante desselben Paares
  // entfaellt -- durchgezogen und gestrichelt ueberlagern sich sonst genau auf derselben
  // Strecke und lesen sich als zwei Beziehungen, obwohl es eine ist.
  //
  // **Warum hier und nicht in `drawEdges()`:** dort waere nur das Bild richtig. Die Grad-
  // und Nachbarzaehlung (`recomputeDegrees()`) laeuft ueber `explicitEdges.concat(
  // implicitEdges)` und wuerde die Zwillingskante weiter mitzaehlen -- ein Knoten saehe
  // verknuepfter aus, als er ist, und `drawNodes()` skaaliert seinen Radius danach. Dasselbe
  // Argument wie bei `dedupeEdges()` eine Zeile weiter oben: **bei der Uebernahme**
  // zusammenfassen, nicht erst beim Zeichnen (P8.6-N).
  //
  // Der Test `test_a_tag_edge_and_an_explicit_edge_draw_two_lines` hat dieses Verhalten
  // eingefroren und ist mit Datum umgedreht und umbenannt --
  // `test_a_tag_edge_beside_an_explicit_edge_draws_one_line`.
  if (explicitEdges.length) {
    var explicitPairs = Object.create(null);
    for (var i = 0; i < explicitEdges.length; i++) {
      var x = explicitEdges[i];
      explicitPairs[x.src < x.dst ? x.src + "|" + x.dst : x.dst + "|" + x.src] = true;
    }
    implicitEdges = implicitEdges.filter(function (e) {
      return !explicitPairs[e.src < e.dst ? e.src + "|" + e.dst : e.dst + "|" + e.src];
    });
  }
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

// -- P10.5 Block 14, Schritt 14.1: die Welt-Geometrie (L1 Regionen, L2 Inseln, L3 Spiralen) ----
//
// **Die Regionen (L1).** Je Space eine Region um einen **Anker**: der eigene Space in der
// Mitte der Leinwand, die anderen auf einer **Goldwinkel-Spirale** darum. Der Radius einer
// Region waechst mit der Wurzel der Item-Zahl (`REGION_ITEM_STEP * sqrt(n) + REGION_PAD`).
//
// **Die Ordner-Inseln (L2).** Innerhalb der Region liegen die Ordner auf einer kleinen
// Spirale: der Ordner `j` sitzt im Winkel `137,5078 Grad * j` vom Anker, im Abstand
// `ISLAND_FACTOR * Radius * sqrt(j / F)`. Die **Wurzel** (`folder: ""`) ist die Insel **am
// Anker** selbst.
//
// **Die Items (L3).** Innerhalb einer Insel liegen die Items auf einer Goldwinkel-Spirale:
// der Item `i` (nach Hash der ID sortiert) im Winkel `137,5078 Grad * i`, im Abstand
// `ITEM_STEP * sqrt(i)`, plus dem Jitter aus dem Hash der ID.
//
// **Der Zufall ist der Hash, nicht der Zufallsgenerator** (P8.6-D2): dieselbe ID ergibt
// dieselbe Position, immer -- auf jedem Rechner, in jeder Sitzung.
//
// **Exportiert**, damit der Wächter-Harness (`probes/p105_b14_layout_probe.mjs`, Node) die
// reine Geometrie **ohne Browser** messen kann -- dieselbe Rolle, die `state.js`s `state`
// fuer den C2-Harness hat. Es ist kein Testhaken: die Funktion ist rechnend und tut nichts
// ausser der Geometrie.
export function computeRegions(nodeList, cx, cy, ownSpace) {
  // -- 1) die Knoten je Space -------------------------------------------------------------------
  var bySpace = Object.create(null);
  var i;
  for (i = 0; i < nodeList.length; i++) {
    var node = nodeList[i];
    var name = node.space || "";
    if (!bySpace[name]) bySpace[name] = [];
    bySpace[name].push(node);
  }

  // -- 2) die Reihenfolge der Anker -------------------------------------------------------------
  // Der **eigene** Space ist Index 0 (sein Anker ist der Ursprung), die anderen folgen nach
  // dem **Hash ihres Namens** -- nicht nach der Item-Zahl: die Item-Zahl aendert sich mit
  // jedem neuen Item, der Hash nicht (Plan §2.1). Das ist die halbe Stabilitaet von
  // Abnahme P10.5-68.
  //
  // **Der eigene Space belegt Index 0 auch dann, wenn er noch keine Items hat** -- sonst
  // wuerde das erste Item im eigenen Space alle Anker verschieben.
  var namen = Object.keys(bySpace);
  var eigen = ownSpace ? ownSpace : null;
  var fremde = [];
  for (i = 0; i < namen.length; i++) {
    if (namen[i] !== eigen) fremde.push(namen[i]);
  }
  fremde.sort(byHash);
  var reihenfolge = eigen ? [eigen].concat(fremde) : fremde;

  // -- 3) die Radien und der Abstand der Anker -------------------------------------------------
  var radien = Object.create(null);
  var maxR = 0;
  for (i = 0; i < reihenfolge.length; i++) {
    var rName = reihenfolge[i];
    var anzahl = bySpace[rName] ? bySpace[rName].length : 0;
    var radius = REGION_ITEM_STEP * Math.sqrt(anzahl) + REGION_PAD;
    radien[rName] = radius;
    if (radius > maxR) maxR = radius;
  }
  // `SLOT` haengt **nur** am groessten Space: ein neues Item in einem kleineren Space
  // aendert ihn nicht -- die Anker bleiben byte-gleich (Abnahme P10.5-68). Nur ein Item im
  // groessten Space vergroessert ihn (und verschiebt damit alle Anker).
  var slot = 2 * maxR + REGION_GAP;

  // -- 4) die Anker -----------------------------------------------------------------------------
  // Der eigene Space in der Mitte, die anderen auf der Goldwinkel-Spirale: der Winkelabstand
  // ist immer derselbe, der Abstand waechst mit sqrt(k) -- so liegt kein Space auf einem
  // anderen. `theta0` kommt aus dem Hash des eigenen Space: **jede Person sieht "ihre" Welt**,
  // und immer dieselbe.
  var theta0 = (hashString(ownSpace || "") >>> 0) / 4294967296 * 2 * Math.PI;
  var spaces = Object.create(null);
  var pos = Object.create(null);
  for (var k = 0; k < reihenfolge.length; k++) {
    var spaceName = reihenfolge[k];
    var winkel = k === 0 ? theta0 : theta0 + k * GOLDEN_ANGLE;
    var abstand = k === 0 ? 0 : slot * Math.sqrt(k);
    var ax = cx + Math.cos(winkel) * abstand;
    var ay = cy + Math.sin(winkel) * abstand;
    var space = {
      name: spaceName,
      x: ax,
      y: ay,
      radius: radien[spaceName],
      angle: winkel,
      folders: Object.create(null),
    };
    spaces[spaceName] = space;

    // -- 5) die Ordner-Inseln (L2) --------------------------------------------------------------
    var mitte = Object.create(null);
    var knoten = bySpace[spaceName] || [];
    for (i = 0; i < knoten.length; i++) {
      var ordner = knoten[i].folder || "";
      if (!mitte[ordner]) mitte[ordner] = [];
      mitte[ordner].push(knoten[i]);
    }
    var ordnerNamen = [];
    for (var key in mitte) {
      if (!Object.prototype.hasOwnProperty.call(mitte, key)) continue;
      if (key !== "") ordnerNamen.push(key);
    }
    ordnerNamen.sort(byHash);
    var F = ordnerNamen.length;
    var inseln = [{ name: "", x: ax, y: ay, angle: winkel }];
    for (var j = 0; j < F; j++) {
      var jwinkel = winkel + (j + 1) * GOLDEN_ANGLE;
      var jabstand = space.radius * ISLAND_FACTOR * Math.sqrt((j + 1) / F);
      inseln.push({
        name: ordnerNamen[j],
        x: ax + Math.cos(jwinkel) * jabstand,
        y: ay + Math.sin(jwinkel) * jabstand,
        angle: jwinkel,
      });
    }

    // -- 6) die Items je Insel (L3) --------------------------------------------------------------
    for (var ins = 0; ins < inseln.length; ins++) {
      var insel = inseln[ins];
      var liste = (mitte[insel.name] || []).slice().sort(byIdHash);
      var ids = [];
      for (var t = 0; t < liste.length; t++) {
        var item = liste[t];
        var iwinkel = insel.angle + t * GOLDEN_ANGLE;
        var irad = ITEM_STEP * Math.sqrt(t);
        pos[item.id] = [
          insel.x + Math.cos(iwinkel) * irad + seedJitter(item.id, 1) * ITEM_JITTER_PX,
          insel.y + Math.sin(iwinkel) * irad + seedJitter(item.id, 2) * ITEM_JITTER_PX,
        ];
        ids.push(item.id);
      }
      space.folders[insel.name] = {
        name: insel.name,
        x: insel.x,
        y: insel.y,
        angle: insel.angle,
        items: ids,
      };
    }
  }
  return { order: reihenfolge, spaces: spaces, pos: pos };
}

// Die Sortierung **nach Hash**: aufsteigend; bei einem Gleichstand entscheidet der Name --
// der Hash kann kollidieren, und die Reihenfolge muss trotzdem eindeutig sein (sonst waere
// die Karte zwischen zwei Laeufen eine andere).
function byHash(a, b) {
  var ha = hashString(a);
  var hb = hashString(b);
  if (ha !== hb) return ha - hb;
  return a < b ? -1 : (a > b ? 1 : 0);
}

// Die Sortierung der **Items** nach dem Hash ihrer ID (L3).
function byIdHash(a, b) {
  var ha = hashString(a.id);
  var hb = hashString(b.id);
  if (ha !== hb) return ha - hb;
  return a.id < b.id ? -1 : (a.id > b.id ? 1 : 0);
}

function seedInitialPositions() {
  // **Der Seed** (Plan §2): die Welt-Geometrie aus `computeRegions()` -- eine Region je Space,
  // darin die Ordner-Inseln, darin die Items auf einer Goldwinkel-Spirale.
  //
  // **P10.5 Block 8, Schritt 8.5 (KA-2):** zuerst die **gemerkten** Positionen (Plan 8.5);
  // unbekannte IDs werden ignoriert.
  //
  // **Datierte Entscheidung (2026-10-24, Abweichung vom Plan-Wortlaut, Code schlaegt Plan):**
  // ein gemerkter Knoten wird **festgehalten** (`pinned`), nicht nur gesaet -- sonst schiebt
  // die Simulation die gemerkte Karte beim naechsten Oeffnen wieder auseinander und KA-2
  // waere nicht erfuellt. Belegt von `probes/p105_b8_karte_probe.py` (Neuladen haelt die
  // Position) und `probes/p105_b8_c2_probe.mjs`.
  //
  // **Ein Knoten, der heute schon eine Position hat** (P9-34: die Karte springt beim
  // Wiedereintritt nicht), bleibt, wo er ist -- gesaet wird nur, wer noch nirgends war.
  var stored = loadStoredLayout();
  var cx = cssWidth / 2;
  var cy = cssHeight / 2;
  var regionen = computeRegions(nodes, cx, cy, state.ownSpace);
  // **Die Regionen merken** (Schritt 14.2): die Gravitation zieht jeden Knoten zu dem Anker
  // **seines** Space. Der Anker kommt aus derselben Rechnung wie der Seed -- damit zieht die
  // Entspannung an **genau** die Stelle, an der der Seed gebaut wurde.
  spaceRegions = regionen;
  for (var i = 0; i < nodes.length; i++) {
    var n = nodes[i];
    var pos = stored[n.id];
    if (pos && typeof pos[0] === "number" && typeof pos[1] === "number") {
      n.x = pos[0];
      n.y = pos[1];
      n.pinned = true;
      pinnedIds[n.id] = true;
    } else if (n.x === 0 && n.y === 0) {
      var ziel = regionen.pos[n.id];
      if (ziel) {
        n.x = ziel[0];
        n.y = ziel[1];
      }
    }
    n.vx = 0;
    n.vy = 0;
  }
}

// Aufbau nach dem Laden: säen und simulieren. Steht als eigene Funktion, weil der
// reduced-motion-Pfad (Schritt 8.7) sie **synchron** braucht und der normale Pfad sie im
// requestAnimationFrame aufruft.
function startLayout() {
  if (nodes.length === 0) {
    draw();
    return;
  }
  seedInitialPositions();
  runSimulation();
}

// FNV-1a, 32 Bit. Zweck ist nicht Kryptographie, sondern Reproduzierbarkeit:
// dieselbe Item-ID muss ueber Reloads hinweg denselben Jitter ergeben, sonst
// "fliegt" die Karte bei jedem Oeffnen neu (Nikinger 2026-09-06, Notizen §2.4).
// Acht Zeilen, `Math.imul` ist exakt 32-Bit, und benachbarte IDs ergeben
// unkorrelierte Werte -- genau das, was ein Jitter braucht. Ein
// `Math.sin(seed)*10000 % 1`-Trick korreliert bei aehnlichen Eingaben, und
// `itm_…`-IDs sind einander aehnlich.
//
// **P10.5 Block 14, Schritt 14.1:** die Rechnung selbst liegt jetzt in `hashString()` --
// Plan §2.1 ("dieselbe Funktion wie `seedJitter`, als `hashString()` herausgezogen"). Die
// Reihenfolge bleibt: erst der Hash, **dann** der Salt. Die Werte sind **bitidentisch** zu
// den vorigen (der C2-Waechter `probes/p105_b8_c2_probe.mjs` misst die Fortsaetze der
// Zellen -- sie haengen an genau diesem Hash).
export function hashString(str) {
  var h = 2166136261;
  var s = String(str);
  for (var i = 0; i < s.length; i++) {
    h ^= s.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
}

// Der **Jitter** aus dem Hash: -0.5 .. +0.5, wie (Math.random() - 0.5).
function seedJitter(id, salt) {
  var h = hashString(id) ^ salt;
  return ((h >>> 0) / 4294967295) - 0.5;   // -0.5 .. +0.5, wie (Math.random() - 0.5)
}

function runSimulation() {
  // P10.5 Block 14, Schritt 14.2: `ALPHA_START_SEEDED` (0,5) statt `ALPHA_START` (1) -- der
  // Seed liegt schon nah am Ziel, also reichen weniger Ticks (Plan §2.4).
  var alpha = ALPHA_START_SEEDED;

  // P10.5 Block 14, Schritt 14.3: ein neuer Aufbau darf sich **einmal** wieder einpassen
  // (Plan §2.5: "nach dem ersten Einschwingen je `loadGraph()`"). Das gilt auch fuer den Knopf
  // "Layout zuruecksetzen" -- der baut die Karte neu auf.
  viewFitted = false;

  // P8.6-D4 (Plan §6.4): jede Wiederholung von `loadGraphPanel()` (Klick auf
  // Uebersicht, Refresh) startete bisher eine **zusaetzliche**
  // `requestAnimationFrame`-Schleife. Solange die vorige noch ueber ALPHA_MIN
  // lag, liefen zwei `tick()`-Schleifen gleichzeitig, beide riefen `draw()` --
  // die direkte Ursache dafuer, dass §2.4 ("die Karte fliegt") sich beim
  // wiederholten Oeffnen verschlimmerte. Der Abbruch war schon halb da
  // (`var rafId` lokal angelegt + zugewiesen in Z. 277 und Z. 290, aber nie
  // gelesen); nur `cancelAnimationFrame` fehlt. Drei Zeilen Fix, benannte
  // Scope-Erweiterung -- wenn der Nikinger es in der Sichtpruefung anders
  // sieht, ist es streichbar (P8.6-§6.4).
  if (!reducedMotion && activeRafId !== null) {
    cancelAnimationFrame(activeRafId);
  }

  // Die Karte ist zur Ruhe gekommen: jetzt werden die Lappen berechnet (Plan 8.1: "Berechnet
  // wird einmal nach dem Einschwingen und nach dem Drag-Ende, nicht je Frame") und die
  // Positionen gemerkt (Plan 8.5). Eigene Funktion, weil **zwei** Wege hierher fuehren:
  // das Ende der Tick-Kette und der reduced-motion-Pfad.
  function settle() {
    lobeCache = computeLobes(visibleNodes());
    // P10.5 Block 14, Schritt 14.3 (Plan §2.5): die Kamera passt sich **einmal** ein -- nach
    // dem Einschwingen, nicht nach einem Drag. Hat der Nutzer in dieser Sitzung schon
    // gezoomt oder verschoben, **gewinnt seine Ansicht**: dann passst sich nichts neu ein.
    if (!viewFitted) {
      viewFitted = true;
      if (!viewTouchedByUser) fitView();
    }
    scheduleLayoutSave();
    draw();
  }

  function tick() {
    if (alpha < ALPHA_MIN) {
      activeRafId = null;
      settle();
      return;
    }
    applyForces(alpha);
    integrate(alpha);
    alpha *= ALPHA_DECAY;
    draw();
    if (alpha >= ALPHA_MIN) {
      activeRafId = requestAnimationFrame(tick);
    } else {
      activeRafId = null;
      settle();
    }
  }

  if (reducedMotion) {
    // Plan §5 D2: "Simulation synchron zu Ende rechnen (~300 Ticks), statisch rendern".
    for (var t = 0; t < MAX_TICKS_REDUCED && alpha >= ALPHA_MIN; t++) {
      applyForces(alpha);
      integrate(alpha);
      alpha *= ALPHA_DECAY;
    }
    // P10.5 Block 8, Schritt 8.7: dasselbe Bild, **ohne** Animationsframe.
    settle();
    activeRafId = null;
  } else {
    activeRafId = requestAnimationFrame(tick);
  }
}

// Modul-Ebene (P8.6-D4): damit `runSimulation()` den vorherigen Loop abbrechen kann.
var activeRafId = null;

// -- P10.5 Block 14, Schritt 14.2: die Entspannung (L4) ------------------------------------------
//
// Die vierte Schicht (Plan §2.4) sitzt in **drei** Kraften: die Gravitation zieht zum
// **eigenen Space-Anker** statt zur Leinwandmitte, die Federn **quer** zwischen zwei Spaces
// sind schwach und lang, und die Startenergie ist die **gesaete** (der Seed liegt schon nah
// am Ziel).
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
      // P10.5 Block 8, Schritt 8.5: ein **festgehaltener** Knoten bewegt sich nicht, aber er
      // drueckt weiter. Vorher war `fixed` (aus dem Drag) ein wirkungsloses Feld -- es wurde
      // gesetzt, aber nie gelesen; die Simulation hat den gezogenen Knoten wieder weggezogen.
      // `pinned` ist der neue Partner: die gemerkte Position (KA-2).
      if (!isHeld(a)) { a.vx += fx; a.vy += fy; }
      if (!isHeld(b)) { b.vx -= fx; b.vy -= fy; }
    }
  }

  // 2. Federkraft je Kante -- explizite und implizite gleich behandelt (Plan §5 D2:
  //    "explizit solide (frontmatter/body ununterschieden)" bezieht sich auf den Render-Stil,
  //    nicht die Federstaerke; eine staerkere Frontmatter-Feder waere eine staillschweigend
  //    eingefuehrte Semantik).
  //
  // **P10.5 Block 14, Schritt 14.2 (Plan §2.4): die Querfeder.** Eine Kante **zwischen zwei
  // Spaces** ist **schwach und lang**: sonst zieht sie zwei Spaces ineinander -- der Grund, warum
  // die Regionen vorher verschmolzen sind. Der Space jedes Endpunkts kommt aus dem Knoten
  // (der Server liefert `space` mit).
  var all = explicitEdges.concat(implicitEdges);
  for (var k = 0; k < all.length; k++) {
    var e = all[k];
    var aa = nodeById[e.src];
    var bb = nodeById[e.dst];
    if (!aa || !bb) continue;
    var quer = aa.space !== bb.space;
    var laenge = quer ? SPRING_LENGTH * CROSS_SPRING_LENGTH_FACTOR : SPRING_LENGTH;
    var staerke = quer ? SPRING_STRENGTH * CROSS_SPRING_FACTOR : SPRING_STRENGTH;
    var ddx = bb.x - aa.x;
    var ddy = bb.y - aa.y;
    var d = Math.sqrt(ddx * ddx + ddy * ddy) + 0.01;
    var stretch = d - laenge;
    var f = stretch * staerke;
    var ffx = (ddx / d) * f;
    var ffy = (ddy / d) * f;
    if (!isHeld(aa)) { aa.vx += ffx; aa.vy += ffy; }
    if (!isHeld(bb)) { bb.vx -= ffx; bb.vy -= ffy; }
  }

  // 3. **Anker-Gravitation** (Plan §2.4) -- jeder Knoten zieht zu dem Anker **seines** Space.
  //    Vorher zog eine **Zentrums-Gravitation** alle Knoten zur Leinwandmitte: das zog die
  //    Spaces auf einen Punkt und liess die Regionen verschmelzen (Befund B2 des Plans).
  //    Der Anker kommt aus `computeRegions()` -- der eigene Space in der Mitte, die anderen auf
  //    der Goldwinkel-Spirale.
  for (var n = 0; n < nodes.length; n++) {
    var node = nodes[n];
    if (isHeld(node)) continue;
    var anker = spaceRegions && spaceRegions.spaces ? spaceRegions.spaces[node.space] : null;
    if (!anker) continue;      // ohne Anker (unbekannter Space) zieht nichts -- der Knoten bleibt, wo er ist
    node.vx += (anker.x - node.x) * ANCHOR_GRAVITY * alpha;
    node.vy += (anker.y - node.y) * ANCHOR_GRAVITY * alpha;
  }
}

// P10.5 Block 8, Schritt 8.5: steht der Knoten fest? `fixed` = beim Drag (P9, bisher ohne
// Wirkung -- siehe `applyForces()`), `pinned` = gemerkte Position aus dem localStorage (KA-2).
function isHeld(n) {
  return n.fixed === true || n.pinned === true;
}

function integrate(alpha) {
  for (var i = 0; i < nodes.length; i++) {
    var n = nodes[i];
    if (isHeld(n)) { n.vx = 0; n.vy = 0; continue; }
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
  // P10.5 Block 8, Schritt 8.4: statt "der Fokus und seine Nachbarn hell, der Rest gedimmt"
  // gibt es jetzt **drei** Stufen: Fokus, erster Ring, zweiter Ring, Rest.
  var rings = hoverId ? neighborRings(hoverId, all) : null;
  // P10.5 Block 8, Schritt 8.6 (KA-3): der Filter blendet Knoten **und** Bahnen aus.
  var shown = visibleNodes();
  var hits = searchQuery ? searchHits(shown) : null;

  drawLobes(shown);
  drawEdges(all, rings, shown);
  drawNodes(rings, shown, hits);

  ctx.restore();

  // Labels werden in CSS-Koordinaten gerendert (nach restore), damit sie nicht mit-skaliert
  // werden -- ein 12px-Label bei Zoom 0.5 wuerde sonst 6px winzig werden.
  drawLabels(rings, shown, hits);
}

// P10.5 Block 8, Schritt 8.6 (KA-3): welche Knoten ueberleben den Filter? Typ (alle/Notiz/
// Aufgabe) und Status (alle/offen/in Arbeit/erledigt). Leerer Wert = "alle".
function visibleNodes() {
  var out = Object.create(null);
  for (var i = 0; i < nodes.length; i++) {
    var n = nodes[i];
    if (filterType && n.type !== filterType) continue;
    if (filterStatus && n.status !== filterStatus) continue;
    out[n.id] = true;
  }
  return out;
}

// Die Suche (KA-3): Titel-Teilstring, ohne Gross/Klein. Treffer hell, der Rest gedimmt --
// und die Zahl der Treffer steht in der Statuszeile.
function searchHits(shown) {
  var hits = Object.create(null);
  var count = 0;
  for (var i = 0; i < nodes.length; i++) {
    var n = nodes[i];
    if (!shown[n.id]) continue;
    var title = (n.title || "").toLowerCase();
    if (title.indexOf(searchQuery) >= 0) {
      hits[n.id] = true;
      count += 1;
    }
  }
  updateHitCount(count);
  return hits;
}

function updateHitCount(count) {
  // **Die Trefferzahl hat ihr eigenes Feld** (`#overview-graph-hits`). Vorher stand sie in
  // der Statuszeile — und der Layout-Hinweis ("Layout gemerkt", der 1 s nach dem Speichern
  // kommt) hat sie ueberschrieben: die Zahl war dann weg, obwohl die Suche lief. Gemessen
  // an der Wegwerf-Instanz am 2026-10-24 (Probe `p105_b8_karte_probe.py`).
  if (!hitsEl) return;
  if (!searchQuery) {
    hitsEl.textContent = "";
    hitsEl.removeAttribute("data-kind");
    return;
  }
  if (count === undefined) {
    // Ohne Knotenmenge laesst sich die Zahl nicht bestimmen -- der Aufrufer setzt sie.
    return;
  }
  hitsEl.setAttribute("data-kind", "hits");
  hitsEl.textContent = count + (count === 1 ? " Treffer" : " Treffer");
}

function setGraphStatus(text) {
  if (!statusEl) return;
  statusEl.textContent = text;
  statusEl.removeAttribute("data-kind");
}

function drawEdges(all, rings, shown) {
  // **V118, zwei Lesarten, beide datiert:**
  //  *2026-09-26 (Antwort des Nikingers auf P9 Step E):* eine Tag-Kante UND eine explizite
  //  Kante zwischen denselben zwei Knoten ergeben **zwei Linien** (solid + gestrichelt), weil
  //  `dedupeEdges()` nur die expliziten Kanten zusammenfasst und `buildTagEdges()` nur die
  //  Tag-Kanten -- die Zusammenführung beider Listen passiert erst hier, ohne Dedup.
  //  *2026-10-05 (zweite Antwort, P9-36):* **eine Linie.** *"Wenn A auf B verlinkt, ist B für A
  //  automatisch relevant."* Die explizite Kante gewinnt, die implizite entfällt -- gefiltert
  //  wird bei der Übernahme in `rebuildImplicitEdges()`, nicht erst hier, damit die Gradzählung
  //  dasselbe Bild zeigt (P8.6-N). `drawEdges()` zeichnet nur noch, wonach es gefragt wird.
  //  Der alte Kommentarstand wurde **ersetzt**, nicht ergänzt: eine Notiz, die beides behauptet,
  //  erklärt gar nichts.
  //
  // **P10.5 Block 8, Schritt 8.2 (Bahnen):** die Kante ist jetzt eine **quadratische Bézier**
  // (Plan: "der Kontrollpunkt liegt senkrecht zur Mitte und wächst mit der Länge"), die Breite
  // folgt dem Grad (`1 + log2(1 + min(deg(a), deg(b)))`), und die Kanten des Fokus tragen den
  // Akzentton (Vorlage C2).
  ctx.lineCap = "round";
  for (var i = 0; i < all.length; i++) {
    var e = all[i];
    var a = nodeById[e.src];
    var b = nodeById[e.dst];
    if (!a || !b) continue;
    // KA-3: ein ausgeblendeter Knoten nimmt seine Bahnen mit.
    if (!shown[a.id] || !shown[b.id]) continue;
    var focusEdge = rings && (a.id === rings.focus || b.id === rings.focus);
    ctx.globalAlpha = edgeAlpha(a, b, rings);
    ctx.strokeStyle = focusEdge ? COLORS.accent : COLORS.edge;
    ctx.lineWidth = EDGE_WIDTH_BASE + Math.log2(1 + Math.min(a.deg, b.deg));
    if (e.kind === "tag") {
      ctx.setLineDash([4, 4]);
    } else if (e.kind === "folder") {
      ctx.setLineDash([1.5, 3]);
    } else {
      ctx.setLineDash([]);
    }
    var geo = edgeGeometry(a, b);
    ctx.beginPath();
    ctx.moveTo(a.x, a.y);
    ctx.quadraticCurveTo(geo.cx, geo.cy, b.x, b.y);
    ctx.stroke();
  }
  ctx.setLineDash([]);
  ctx.globalAlpha = 1;
}

// Die Bahn-Geometrie (Plan 8.2): Kontrollpunkt senkrecht zur Mitte, waechst mit der Laenge.
// Die **Richtung** ist kanonisch (nach ID sortiert), damit dieselbe Kante immer dieselbe
// Krümmung hat -- sonst hinge die Form davon ab, in welcher Reihenfolge der Server sie
// geliefert hat.
function edgeGeometry(a, b) {
  var p = a;
  var q = b;
  if (String(a.id) > String(b.id)) { p = b; q = a; }
  var dx = q.x - p.x;
  var dy = q.y - p.y;
  return {
    cx: (p.x + q.x) / 2 - dy * EDGE_CURVE,
    cy: (p.y + q.y) / 2 + dx * EDGE_CURVE,
  };
}

// Die Helligkeit einer Bahn (Plan 8.4): Fokus und erster Ring voll, zweiter Ring halb,
// der Rest gedimmt. Ohne Fokus (Ruhezustand) ist **alles** voll deckend.
function edgeAlpha(a, b, rings) {
  if (!rings) return 1;
  if (a.id === rings.focus || b.id === rings.focus) return 1;
  if (rings.first.has(a.id) || rings.first.has(b.id)) return 1;
  if (rings.second.has(a.id) || rings.second.has(b.id)) return HALF_ALPHA;
  return DIM_ALPHA;
}

// Die Helligkeit eines Knotens (Plan 8.4) -- dieselbe Stufenfolge wie bei den Bahnen.
function nodeAlpha(id, rings, hits) {
  if (hits) return hits[id] ? 1 : DIM_ALPHA;
  if (!rings) return 1;
  if (id === rings.focus) return 1;
  if (rings.first.has(id)) return 1;
  if (rings.second.has(id)) return HALF_ALPHA;
  return DIM_ALPHA;
}

function nodeRadius(n) {
  return Math.min(NODE_RADIUS_MAX, NODE_RADIUS_BASE + NODE_RADIUS_PER_LOG * Math.log2(1 + n.deg));
}

function drawNodes(rings, shown, hits) {
  for (var i = 0; i < nodes.length; i++) {
    var n = nodes[i];
    if (!shown[n.id]) continue;
    var r = nodeRadius(n);
    var alpha = nodeAlpha(n.id, rings, hits);
    var isFocus = rings && n.id === rings.focus;
    var color = isFocus ? COLORS.accent : nodeColor(n);
    ctx.globalAlpha = alpha;

    // -- P10.5 Block 8, Schritt 8.3 (Zellen): die Zelle ist ein **Kern** (gefuellt), ein
    //    **Membranring** (2 px, Space-Farbe) und 2-4 kurze **Fortsaetze** -- deterministisch
    //    aus dem Hash der Item-ID, damit dieselbe Item bei jedem Laden gleich aussieht.
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(n.x, n.y, Math.max(2.5, r * 0.55), 0, 2 * Math.PI);
    ctx.fill();

    ctx.strokeStyle = color;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(n.x, n.y, r, 0, 2 * Math.PI);
    ctx.stroke();

    ctx.lineWidth = 1;
    ctx.beginPath();
    var procs = cellProcesses(n.id);
    for (var p = 0; p < procs.length; p++) {
      var pr = procs[p];
      var ca = Math.cos(pr.angle);
      var sa = Math.sin(pr.angle);
      ctx.moveTo(n.x + ca * r, n.y + sa * r);
      ctx.lineTo(n.x + ca * (r + pr.len), n.y + sa * (r + pr.len));
    }
    ctx.stroke();

    if (n.status === "doing") {
      // P10.5 7.7 (KA-5): statischer Akzentring, bewusst ohne Animation.
      ctx.strokeStyle = COLORS.doing;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(n.x, n.y, r + 3, 0, 2 * Math.PI);
      ctx.stroke();
    }
    if (isFocus) {
      // P10.5 Block 8 (8.4): der Fokus bekommt den hellen Ring der Vorlage C2.
      ctx.strokeStyle = COLORS.accent;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(n.x, n.y, r + 6, 0, 2 * Math.PI);
      ctx.stroke();
    }
  }
  ctx.globalAlpha = 1;
}

// Die Fortsaetze der Zelle (Plan 8.3): 2-4 kurze Striche, Winkel und Laenge aus dem Hash
// der Item-ID -- derselbe Hash, den schon `seedJitter()` benutzt (FNV-1a, 32 Bit).
function cellProcesses(id) {
  var count = 2 + Math.floor(Math.abs(seedJitter(id, 20)) * 3);   // 2, 3 oder 4
  var base = seedJitter(id, 21) * Math.PI * 2;
  var out = [];
  for (var i = 0; i < count; i++) {
    out.push({
      angle: base + i * (Math.PI * 2 / count) + seedJitter(id, 30 + i) * 0.5,
      len: 4 + Math.abs(seedJitter(id, 40 + i)) * 4,
    });
  }
  return out;
}

function drawLabels(rings, shown, hits) {
  // Plan 8.6: "Titel: Fokus + erster Ring immer, sonst weiter ab ZOOM_LABEL_THRESHOLD".
  var zoomedIn = zoom >= ZOOM_LABEL_THRESHOLD;
  if (!rings && !zoomedIn) return;
  ctx.fillStyle = COLORS.label;
  ctx.font = LABEL_FONT;
  ctx.textBaseline = "middle";
  // P10.5 Block 14, Schritt 14.35 (Plan §2.7): die Rechtecke der **gezeichneten**
  // Beschriftungen sammeln; ein Rechteck, das ein schon gezeichnetes ueberlappt, wird
  // **nicht** gezeichnet. Der Fokus verliert seine Beschriftung **nie**.
  var belegt = [];
  var kandidaten = labelCandidates(rings, shown, hits, zoomedIn);
  for (var i = 0; i < kandidaten.length; i++) {
    var k = kandidaten[i];
    var text = truncate(k.node.title, 28);
    // **Ein leerer Titel belegt keine Flaeche:** ein Rechteck der Breite 0 wuerde sonst die
    // Nachbarbeschriftung wegdruecken (die Kollisionspruefung sieht die Rechtecke, nicht die
    // Buchstaben) -- ohne dass es etwas zu zeichnen gaebe.
    if (!text) continue;
    // Position in CSS-Koordinaten (nach pan/zoom-Transform).
    var sx = k.node.x * zoom + panX;
    var sy = k.node.y * zoom + panY;
    var x0 = sx + k.radius + LABEL_OFFSET;
    var rect = {
      x0: x0, y0: sy - LABEL_HEIGHT / 2,
      x1: x0 + ctx.measureText(text).width, y1: sy + LABEL_HEIGHT / 2,
    };
    if (!k.focus && labelRectOverlaps(rect, belegt)) continue;
    // Die Beschriftung folgt derselben Helligkeit wie der Knoten -- sonst leuchtet der Titel
    // eines getroffenen Knotens weiter, obwohl der Knoten selbst gedimmt ist.
    ctx.globalAlpha = nodeAlpha(k.node.id, rings, hits);
    ctx.fillText(text, x0, sy);
    belegt.push(rect);
  }
  ctx.globalAlpha = 1;
}

// Die **Reihenfolge** der Beschriftungen ist der Vorrang (Plan §2.7): Fokus → erster Ring →
// Suchtreffer → Rest nach Grad absteigend. Innerhalb einer Stufe entscheidet der Grad
// (der groesste zuerst) -- damit ist die Reihenfolge eindeutig und die Karte sieht bei
// gleicher Lage immer gleich aus.
//
// **Die Menge der beschrifteten Knoten aendert sich nicht** (Plan 8.6): Fokus und erster Ring
// immer, sonst erst ab `ZOOM_LABEL_THRESHOLD`. Die Suchtreffer sind eine *Stufe* der
// Reihenfolge, kein eigener Anlass -- wer sucht, zoomt ohnehin.
function labelCandidates(rings, shown, hits, zoomedIn) {
  var out = [];
  for (var i = 0; i < nodes.length; i++) {
    var n = nodes[i];
    if (!shown[n.id]) continue;
    var focus = !!(rings && n.id === rings.focus);
    var first = !!(rings && rings.first.has(n.id));
    if (!focus && !first && !zoomedIn) continue;
    var rang = 3;
    if (focus) rang = 0;
    else if (first) rang = 1;
    else if (hits && hits[n.id]) rang = 2;
    out.push({node: n, focus: focus, rang: rang, radius: nodeRadius(n)});
  }
  out.sort(function (a, b) {
    if (a.rang !== b.rang) return a.rang - b.rang;
    return b.node.deg - a.node.deg;
  });
  return out;
}

// Ueberlappt das Rechteck eine der schon gezeichneten Beschriftungen? (Plan §2.7)
function labelRectOverlaps(rect, belegt) {
  for (var i = 0; i < belegt.length; i++) {
    var b = belegt[i];
    if (rect.x0 < b.x1 && b.x0 < rect.x1 && rect.y0 < b.y1 && b.y0 < rect.y1) return true;
  }
  return false;
}


function nodeColor(n) {
  // Fix B (Plan §9.4.6 Befund B, 2026-09-02): der Knoten traegt jetzt own/writable in exakt
  // derselben Form wie eine /api/v1/spaces-Zeile (webui/api.py :: _graph_get -> _writable()),
  // deshalb dieselbe spaceCategory()-Funktion wie tree.js/list.js -- der Graph faerbt sich
  // dadurch per Konstruktion identisch zur Rail (P8-15), keine zweite Kategorie-Logik hier.
  // Vorher stand hier `writable: n.shared`, das Feld hiess `shared` und war tatsaechlich
  // `space != own_space` -- jeder fremde Knoten kam als "shared" (tuerkis) heraus, die dritte
  // Farbe --space-foreign war strukturell unerreichbar (P8-22-Smoke-Nebenfund, 2026-09-02).
  var cat = spaceCategory({ own: n.own, writable: n.writable });
  if (cat === "own") return COLORS.spaceOwn;
  if (cat === "shared") return COLORS.spaceShared;
  return COLORS.spaceForeign;
}

function truncate(s, n) {
  if (!s) return "";
  return s.length <= n ? s : s.slice(0, n - 1) + "\u2026";
}

// P10.5 Block 8, Schritt 8.4: die Nachbarschaft als **Ringe**. `first` = die direkt
// verbundenen Knoten, `second` = deren Nachbarn (ohne Fokus und ohne ersten Ring).
// Vorher gab es nur `neighborSet` (ein flacher Kreis um den Fokus) -- der zweite Ring ist neu.
function neighborRings(id, all) {
  var first = new Set();
  var second = new Set();
  for (var i = 0; i < all.length; i++) {
    var e = all[i];
    if (e.src === id) first.add(e.dst);
    if (e.dst === id) first.add(e.src);
  }
  for (var j = 0; j < all.length; j++) {
    var f = all[j];
    var other = null;
    if (first.has(f.src)) other = f.dst;
    else if (first.has(f.dst)) other = f.src;
    if (other && other !== id && !first.has(other)) second.add(other);
  }
  return { focus: id, first: first, second: second };
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
  // P10.5 Block 8, Schritt 8.7: im reduced-motion-Pfad wartet der Aufbau auf die erste Box
  // mit echter Groesse -- auch das ohne requestAnimationFrame (0 Frames, Abnahme P10.5-40).
  if (pendingReducedStart) {
    pendingReducedStart = false;
    startLayout();
    return;
  }
  draw();
}

// P10.5 Block 8, Schritt 8.6 (KA-3): die Auswahllisten tragen nur, was **im Bild** vorkommt.
// Grund: eine Auswahl "Erledigt", die keine erledigte Aufgabe enthaelt, wuerde die Karte
// leerzeichnen -- und der Nutzer wuerde nicht wissen, ob die Karte leer ist oder der Filter
// zu streng. Die Werte selbst kommen aus den neun Feldern des Graph-Knotens (`type`,
// `status`) -- **kein** zehntes Feld, keine API-Oeffnung (P10-D).
function populateFilters() {
  var types = Object.create(null);
  var statuses = Object.create(null);
  for (var i = 0; i < nodes.length; i++) {
    if (nodes[i].type) types[nodes[i].type] = true;
    if (nodes[i].status) statuses[nodes[i].status] = true;
  }
  pruneSelect(document.getElementById("overview-graph-filter-type"), types);
  pruneSelect(document.getElementById("overview-graph-filter-status"), statuses);
}

function pruneSelect(el, present) {
  if (!el || !el.options || typeof document === "undefined" || !document.createElement) return;
  var keep = [];
  for (var i = 0; i < el.options.length; i++) {
    var opt = el.options[i];
    if (!opt.value || present[opt.value]) keep.push(opt.value);
  }
  var current = el.value;
  while (el.options.length) el.removeChild(el.options[0]);
  for (var k = 0; k < keep.length; k++) {
    var value = keep[k];
    var option = document.createElement("option");
    option.value = value;
    option.textContent = value ? filterLabel(value) : "alle";
    el.appendChild(option);
  }
  el.value = (keep.indexOf(current) >= 0) ? current : "";
}

// Die Beschriftung eines Filterwerts: Typen aus `TYPE_LABELS`, Statuse aus `STATUS_LABELS`.
function filterLabel(value) {
  if (TYPE_LABELS[value]) return TYPE_LABELS[value];
  if (STATUS_LABELS[value]) return STATUS_LABELS[value];
  return value;
}

// ============================================================================================
// P10.5 Block 8, Schritt 8.1 — die Lappen (der Körper der Gehirnkarte)
// ============================================================================================
//
// Die Pipeline ist die aus M6 (`phase10_inventory/probes/p10_m6_lobe_probe.py :: LOBE_PIPELINE`)
// mit den zwei Aenderungen aus Plan 8.1: (a) die Zuordnung "naechster Knoten" ergibt den
// **Space** des Knotens als Lappen-ID, und die **Furche** liegt dort, wo ein 4-Nachbar einem
// anderen Space gehoert; (b) die Koerpermaske sind die Zellen innerhalb von `LOBE_REACH` um
// den naechsten Knoten. Die Kontur ist eine Gittertreppe und wird ueber die Kantenmittelpunkte
// geglaettet gezeichnet (organische Raender wie in der Vorlage C2). Kosten laut M6: 0,2-1,9 ms
// je Lauf bei 200 Knoten -- **einmal** nach dem Einschwingen und nach dem Drag-Ende, nie je
// Frame (Plan 8.1). Die Herleitung steht in `phase10_5_finishing/CLAUDE.md`.

// Der Lappen-Zustand: {key, lobes: [{space, color, outer: [[x,y]…], inner: [[x,y]…]|null}]}.
// `key` haelt fest, fuer welche Knotenmenge (Filter) er berechnet wurde.
function computeLobes(shown) {
  var list = [];
  for (var i = 0; i < nodes.length; i++) {
    if (!shown || shown[nodes[i].id]) list.push(nodes[i]);
  }
  if (!list.length) return null;

  // -- Weltbereich: die Knoten plus der Reach-Radius -------------------------------------------------
  var nodeMinX = Infinity, nodeMinY = Infinity, nodeMaxX = -Infinity, nodeMaxY = -Infinity;
  for (var j = 0; j < list.length; j++) {
    var n = list[j];
    if (n.x < nodeMinX) nodeMinX = n.x;
    if (n.y < nodeMinY) nodeMinY = n.y;
    if (n.x > nodeMaxX) nodeMaxX = n.x;
    if (n.y > nodeMaxY) nodeMaxY = n.y;
  }

  // **Das Polster (Plan 14.6 §2.1, Schritt 1):** `LOBE_REACH` + `LOBE_CLOSE_PX` + **eine
  // Zelle**. Die eine Zelle ist der Puffer, damit das **Schrumpfen** (Schritt 3) den Rand
  // des aeussersten Lappens nicht abschneidet -- das Raster muss dort **eine Zelle weiter**
  // reichen als die Koerpermaske.
  var reach = LOBE_REACH + LOBE_CLOSE_PX;
  var spanX = (nodeMaxX - nodeMinX) + 2 * reach;
  var spanY = (nodeMaxY - nodeMinY) + 2 * reach;
  // Zellgroesse: 8 px (Plan), aber gedeckelt, damit ein weit auseinandergezogenes Layout
  // das Raster nicht explodieren laesst (Deckel LOBE_MAX_CELLS je Achse). **Der Deckel gilt
  // fuer die gesamte Spanne -- auch fuer das Zell-Polster** (Plan 14.6 §2.5): sonst wueschse
  // das Raster um zwei Zellen darueber hinaus. Bei `LOBE_CLOSE_PX = 0` ist die Zellgroesse
  // damit **unveraendert** (das Polster ist genau eine Zelle).
  var cell = LOBE_CELL_PX;
  var maxCells = LOBE_MAX_CELLS - 2;
  if (spanX / cell > maxCells) cell = spanX / maxCells;
  if (spanY / cell > maxCells) cell = Math.max(cell, spanY / maxCells);
  var cols = Math.max(1, Math.ceil((spanX + 2 * cell) / cell));
  var rows = Math.max(1, Math.ceil((spanY + 2 * cell) / cell));
  var minX = nodeMinX - reach - cell;
  var minY = nodeMinY - reach - cell;

  // -- 1) Zuordnung: je Zelle der naechste Knoten (und damit sein Space) ----------------------
  var assign = new Int32Array(cols * rows);      // Index des naechsten Knoten, -1 = ausserhalb
  var spaceOf = new Array(cols * rows);           // der Space-Name (oder null)
  var mask = new Uint8Array(cols * rows);         // 1 = Zelle der **heutigen** Maske (Reach 48)
  var reachSq = LOBE_REACH * LOBE_REACH;
  var growSq = reach * reach;
  for (var gy = 0; gy < rows; gy++) {
    var cy = minY + gy * cell + cell / 2;
    for (var gx = 0; gx < cols; gx++) {
      var cx = minX + gx * cell + cell / 2;
      var best = -1;
      var bestD = Infinity;
      for (var k = 0; k < list.length; k++) {
        var dx = list[k].x - cx;
        var dy = list[k].y - cy;
        var d = dx * dx + dy * dy;
        if (d < bestD) { bestD = d; best = k; }
      }
      var idx = gy * cols + gx;
      // (b) die **gewachsene** Koerpermaske: die Zellen innerhalb von `LOBE_REACH +
      // LOBE_CLOSE_PX` vom naechsten Knoten. **Dieselbe** Schleife wie bisher -- nur die
      // Schwelle ist groesser (Plan 14.6 §2.1, Schritt 2).
      if (best < 0 || bestD > growSq) { assign[idx] = -1; spaceOf[idx] = null; continue; }
      assign[idx] = best;
      spaceOf[idx] = list[best].space || "";
      if (bestD <= reachSq) mask[idx] = 1;
    }
  }

  // -- 2) Das Schliessen (Plan 14.6 §2.1, Schritt 3 und 4) ----------------------------------
  //
  // **Schrumpfen:** eine Zelle bleibt, wenn ihr euklidischer Abstand (in Zellen) zur
  // naechsten Zelle **ausserhalb** des gewachsenen Satzes groesser als
  // `LOBE_CLOSE_PX / cell` ist. Die Distanz ist die **exakte** euklidische
  // (Felzenszwalb-Huttenlocher) -- eine Chamfer-Naeherung wiche bis ~8 % ab und machte die
  // Raender **achteckig** statt rund.
  //
  // **Der Koerper** = der geschlossene Satz **∪** die heutige Maske: die Vereinigung
  // faengt die Rasterungs-Kante ab (ohne sie koennte das Schliessen eine Zelle der heutigen
  // Maske verlieren). Bei `LOBE_CLOSE_PX = 0` ist das Schrumpfen die Identitaet (der Abstand
  // jeder Zelle zum Satz ausserhalb ist mindestens eine Zelle) -- der Koerper ist damit
  // **exakt** die heutige Maske (Plan 14.6 §2.2: die Regressionsprobe).
  var ausserhalb = new Uint8Array(cols * rows);
  for (var q = 0; q < cols * rows; q++) ausserhalb[q] = assign[q] < 0 ? 1 : 0;
  var dist2 = distanzQuadrat(ausserhalb, cols, rows);
  var grenze = LOBE_CLOSE_PX * LOBE_CLOSE_PX;
  var koerper = new Uint8Array(cols * rows);
  for (var w = 0; w < cols * rows; w++) {
    if (assign[w] < 0) continue;
    if (dist2[w] * cell * cell > grenze) koerper[w] = 1;
    if (mask[w]) koerper[w] = 1;                 // die heutige Maske bleibt (Schritt 4)
    if (!koerper[w]) { spaceOf[w] = null; assign[w] = -1; }
  }

  // -- 2) Furche: ein 4-Nachbar aus einem anderen Space macht die Zelle zur Furche ----------
  var furrow = new Uint8Array(cols * rows);
  for (var fy = 0; fy < rows; fy++) {
    for (var fx = 0; fx < cols; fx++) {
      var fi = fy * cols + fx;
      var mine = spaceOf[fi];
      if (mine === null || mine === undefined) continue;
      var different = false;
      if (fx > 0 && spaceOf[fi - 1] !== null && spaceOf[fi - 1] !== undefined && spaceOf[fi - 1] !== mine) different = true;
      if (!different && fx < cols - 1 && spaceOf[fi + 1] !== null && spaceOf[fi + 1] !== undefined && spaceOf[fi + 1] !== mine) different = true;
      if (!different && fy > 0 && spaceOf[fi - cols] !== null && spaceOf[fi - cols] !== undefined && spaceOf[fi - cols] !== mine) different = true;
      if (!different && fy < rows - 1 && spaceOf[fi + cols] !== null && spaceOf[fi + cols] !== undefined && spaceOf[fi + cols] !== mine) different = true;
      if (different) furrow[fi] = 1;
    }
  }

  // -- 3) Kontur je Space ----------------------------------------------------------------------
  var spaces = Object.create(null);
  for (var s = 0; s < list.length; s++) {
    var sp = list[s].space || "";
    if (!spaces[sp]) spaces[sp] = { name: sp, color: nodeColor(list[s]), cells: [] };
  }
  for (var ci = 0; ci < cols * rows; ci++) {
    var space = spaceOf[ci];
    if (space === null || space === undefined) continue;
    if (furrow[ci]) continue;                 // die Furche gehoert zu keinem Lappen
    if (!spaces[space]) continue;
    spaces[space].cells.push(ci);
  }

  var lobes = [];
  for (var key in spaces) {
    if (!Object.prototype.hasOwnProperty.call(spaces, key)) continue;
    var entry = spaces[key];
    if (!entry.cells.length) continue;
    var member = Object.create(null);
    for (var m = 0; m < entry.cells.length; m++) member[entry.cells[m]] = true;
    var outer = traceContour(member, cols, rows, cell, minX, minY);
    if (!outer || !outer.length) continue;
    // Die innere Kontur: dieselbe Zellmenge, dreimal erodiert (3 Zellen = 24 px) -- die
    // "leise zweite Linie" der Vorlage C2.
    var inner = traceContour(erode(member, cols, rows, LOBE_INNER_CELLS), cols, rows, cell, minX, minY);
    lobes.push({ space: entry.name, color: entry.color, outer: outer, inner: inner && inner.length ? inner : null });

  }
  return { key: lobeKey(shown), lobes: lobes };
}

// Der Schluessel des Lappen-Zustands: welcher Filter stand bei der Berechnung.
function lobeKey(shown) {
  return filterType + "|" + filterStatus + "|" + (shown ? Object.keys(shown).length : 0);
}

// Die **exakte** euklidische Distanztransformation auf dem Raster (Felzenszwalb & Huttenlocher,
// 2012): je Zelle das **quadrierte** Abstand zur naechsten **Zielzelle** (deren Marke gesetzt
// ist). Zwei 1-D-Durchlaenge (einer je Zeile, einer je Spalte), O(Zellen).
//
// **Warum exakt und nicht Chamfer:** die Chamfer-Naeherung (3-4-5) weicht bis zu ~8 % vom
// euklidischen Abstand ab -- bei einem Radius von 200 px sind das 16 px, und die Raender des
// Koerpers werden **achteckig** statt rund. Der Abstand ist die *Form* der Karte (Plan 14.6
// §2.1: "eine Chamfer-Naeherung ist **nicht** zulaessig").
//
// `quelle` = 1 fuer die Zielzellen. Das Ergebnis ist in **Zellen** squared (die Umrechnung in
// Pixel macht der Aufrufer: `dist2 * cell * cell`).
function distanzQuadrat(quelle, cols, rows) {
  var n = Math.max(cols, rows);
  var f = new Float64Array(n);
  var d = new Float64Array(n);
  var v = new Int32Array(n);
  var z = new Float64Array(n + 1);
  var out = new Float64Array(cols * rows);
  var x, y, q;
  // die Zeilen
  for (y = 0; y < rows; y++) {
    for (x = 0; x < cols; x++) f[x] = sourceCost(quelle[y * cols + x]);
    distanz1d(f, d, v, z, cols);
    for (x = 0; x < cols; x++) out[y * cols + x] = d[x];
  }
  // die Spalten
  for (x = 0; x < cols; x++) {
    for (y = 0; y < rows; y++) f[y] = out[y * cols + x];
    distanz1d(f, d, v, z, rows);
    for (y = 0; y < rows; y++) out[y * cols + x] = d[y];
  }
  return out;
}

// Die Kosten einer Zelle fuer den 1-D-Durchlauf: 0 fuer die Zielzellen, sonst ein **grosser
// endlicher** Wert. `Infinity` waere falsch: die Trennlinie der Parabeln waere dann `Infinity`
// und die Huelle kaeme nicht voran (der Durchlauf muesste mit `k` unter null laufen). Mit dem
// grossen Wert ist die Grenzlinie die **Winkelhalbierende** -- das ist das richtige Grenzverhalten
// fuer eine Zelle, die nie die kleinste sein wird.
function sourceCost(istZiel) {
  return istZiel ? 0 : 1e20;
}

// Der 1-D-Durchlauf der quadratischen Distanztransformation:
// `d[q] = min_p ((q - p)^2 + f[p])` -- die untere Huelle der Parabeln (Felzenszwalb 2012).
function distanz1d(f, d, v, z, n) {
  var k = 0;
  var q, s, dq;
  v[0] = 0;
  z[0] = -Infinity;
  z[1] = Infinity;
  for (q = 1; q < n; q++) {
    s = ((f[q] + q * q) - (f[v[k]] + v[k] * v[k])) / (2 * q - 2 * v[k]);
    while (s <= z[k]) {
      k--;
      s = ((f[q] + q * q) - (f[v[k]] + v[k] * v[k])) / (2 * q - 2 * v[k]);
    }
    k++;
    v[k] = q;
    z[k] = s;
    z[k + 1] = Infinity;
  }
  k = 0;
  for (q = 0; q < n; q++) {
    while (z[k + 1] < q) k++;
    dq = q - v[k];
    d[q] = dq * dq + f[v[k]];
  }
}

// Erosion: Zellen, deren 4-Nachbarn alle zur Menge gehoeren. `times` Schritte.
function erode(member, cols, rows, times) {
  var current = member;
  for (var t = 0; t < times; t++) {
    var next = Object.create(null);
    for (var key in current) {
      if (!Object.prototype.hasOwnProperty.call(current, key)) continue;
      var idx = Number(key);
      var gx = idx % cols;
      var gy = Math.floor(idx / cols);
      if (gx === 0 || gy === 0 || gx === cols - 1 || gy === rows - 1) continue;
      if (!current[idx - 1] || !current[idx + 1] || !current[idx - cols] || !current[idx + cols]) continue;
      next[idx] = true;
    }
    current = next;
  }
  return current;
}

// Die Kontur einer Zellmenge: die Randkanten (Zelle drin, Nachbar draussen) als gerichtete
// Kanten sammeln und zu geschlossenen Konturen verketten.
//
// **Es kann mehrere Konturen geben** -- bei 200 verstreuten Knoten ist die Region eines
// Spaces nicht ein Fleck, sondern viele (der Reach-Radius um jeden Knoten). Frueher (2026-10-24,
// derselbe Tag) wurde **nur die groesste** Kontur gezeichnet: die uebrigen Flecken des Spaces
// fehlten im Bild, und die Karte zeigte bei 200 Knoten fast keine Lappen (gemessen an den
// Kontur-Pixeln im Screenshot: 144 statt 509). Jetzt werden **alle** Konturen gezeichnet.
function traceContour(member, cols, rows, cell, minX, minY) {
  var edges = [];
  for (var key in member) {
    if (!Object.prototype.hasOwnProperty.call(member, key)) continue;
    var idx = Number(key);
    var gx = idx % cols;
    var gy = Math.floor(idx / cols);
    var x0 = minX + gx * cell;
    var y0 = minY + gy * cell;
    var x1 = x0 + cell;
    var y1 = y0 + cell;
    // Orientierung im Uhrzeigersinn (y nach unten): oben (x1→x0), links (y0→y1),
    // unten (x0→x1), rechts (y1→y0). So laeuft die Kontur geschlossen um die Menge.
    // **Der Rasterrand ist "draussen"** (2026-10-28): vorher fiel die Kante dort *weg* -- die
    // Kontur des aeussersten Knotens (das Raster beginnt genau bei Knoten − LOBE_REACH) blieb
    // offen, zerfiel in Bruchstuecke, und jedes wurde mit einer Sehne geschlossen (sichtbar als
    // schraege Linie am linken Lappen der Kartenbilder 14.5). `gx === 0` statt `idx - 1`: am
    // linken Rand ist `idx - 1` die letzte Zelle der Zeile darueber.
    if (gy === 0 || !member[idx - cols]) edges.push([x1, y0, x0, y0]);
    if (gx === 0 || !member[idx - 1]) edges.push([x0, y0, x0, y1]);
    if (gy === rows - 1 || !member[idx + cols]) edges.push([x0, y1, x1, y1]);
    if (gx === cols - 1 || !member[idx + 1]) edges.push([x1, y1, x1, y0]);
  }
  if (!edges.length) return null;
  return chainEdges(edges);
}

// Die Kanten zu Konturen verketten: eine Kante beginnt dort, wo die vorige endet.
function chainEdges(edges) {
  var byStart = Object.create(null);
  for (var i = 0; i < edges.length; i++) {
    var k = edges[i][0] + "," + edges[i][1];
    if (!byStart[k]) byStart[k] = [];
    byStart[k].push(i);
  }
  var used = new Uint8Array(edges.length);
  var loops = [];
  for (var e = 0; e < edges.length; e++) {
    if (used[e]) continue;
    var startIdx = e;
    var loop = [];
    var current = e;
    var guard = 0;
    while (guard <= edges.length) {
      guard += 1;
      var edge = edges[current];
      used[current] = 1;
      loop.push([edge[0], edge[1]]);
      var bucket = byStart[edge[2] + "," + edge[3]];
      var next = -1;
      if (bucket) {
        for (var b = 0; b < bucket.length; b++) {
          if (!used[bucket[b]]) { next = bucket[b]; break; }
        }
      }
      if (next < 0) break;
      current = next;
      if (current === startIdx) break;
    }
    if (loop.length >= 3) loops.push(loop);
  }
  if (!loops.length) return null;
  // Die Konturen sind alle gleich orientiert (die Randkanten sind gleich gerichtet), also
  // fuellt die Non-Zero-Regel ihre Vereinigung -- und jede einzelne wird fuer sich gestrichen.
  return loops.map(function (l) { return simplifyLoop(l); }).filter(function (l) { return l.length >= 3; });
}

// Gerade Kanten zusammenfassen: ein Punkt, der auf der Linie der beiden Nachbarn liegt,
// traegt nichts zur Form bei.
function simplifyLoop(pts) {
  var out = [];
  var n = pts.length;
  for (var i = 0; i < n; i++) {
    var prev = pts[(i - 1 + n) % n];
    var cur = pts[i];
    var next = pts[(i + 1) % n];
    var cross = (cur[0] - prev[0]) * (next[1] - prev[1]) - (cur[1] - prev[1]) * (next[0] - prev[0]);
    if (Math.abs(cross) < 1e-9) continue;
    out.push(cur);
  }
  return out.length >= 3 ? out : pts;
}

// Die Kontur zeichnen: eine weiche Kurve durch die Mittelpunkte der Kanten (quadratische
// Kurve mit den Originalpunkten als Kontrollpunkten). Das ist die Form der Vorlage C2 --
// organische Raender statt einer Pixeltreppe.
function traceSmooth(ctx, pts) {
  var n = pts.length;
  if (n < 3) return;
  var mx = (pts[n - 1][0] + pts[0][0]) / 2;
  var my = (pts[n - 1][1] + pts[0][1]) / 2;
  ctx.moveTo(mx, my);
  for (var i = 0; i < n; i++) {
    var p = pts[i];
    var q = pts[(i + 1) % n];
    ctx.quadraticCurveTo(p[0], p[1], (p[0] + q[0]) / 2, (p[1] + q[1]) / 2);
  }
  ctx.closePath();
}

// Die Lappen zeichnen (Plan 8.1): die Kontur in der Space-Farbe, innen eine leise zweite
// Linie in einem **dunkleren Ton desselben Tokens** (nicht ueber Alpha, P8 §0.3 Nr. 6).
function drawLobes(shown) {
  if (!lobeCache || lobeCache.key !== lobeKey(shown)) {
    lobeCache = computeLobes(shown);
  }
  if (!lobeCache || !lobeCache.lobes.length) return;
  for (var i = 0; i < lobeCache.lobes.length; i++) {
    var lobe = lobeCache.lobes[i];
    // Die Flaeche: derselbe Ton, sehr leise (die Vorlage C2 nutzt 5% Fuellung). Alle
    // Konturen des Lappens liegen in **einem** Pfad -- die Non-Zero-Regel fuellt ihre
    // Vereinigung (die Konturen sind gleich orientiert).
    ctx.globalAlpha = 0.05;
    ctx.fillStyle = lobe.color;
    ctx.beginPath();
    for (var o = 0; o < lobe.outer.length; o++) traceSmooth(ctx, lobe.outer[o]);
    ctx.fill();
    // Die Kontur: der Space-Ton, halb deckend (die Vorlage C2 nutzt 55%).
    ctx.globalAlpha = 0.55;
    ctx.strokeStyle = lobe.color;
    ctx.lineWidth = 1.1;
    ctx.lineJoin = "round";
    ctx.beginPath();
    for (var s = 0; s < lobe.outer.length; s++) traceSmooth(ctx, lobe.outer[s]);
    ctx.stroke();
    if (lobe.inner) {
      // Die innere Linie: ein **dunklerer Ton** desselben Tokens -- als feste Farbe
      // gerechnet, nicht als Alpha ueber dem Grund.
      ctx.globalAlpha = 1;
      ctx.strokeStyle = mixTone(lobe.color, CANVAS_SURFACE, 0.42);
      ctx.lineWidth = 1;
      ctx.beginPath();
      for (var n = 0; n < lobe.inner.length; n++) traceSmooth(ctx, lobe.inner[n]);
      ctx.stroke();
    }
  }
  ctx.globalAlpha = 1;
}

// Zwei Farben mischen (feste Farbe, kein Alpha): `ratio` ist der Anteil der ersten Farbe.
function mixTone(hex, bg, ratio) {
  var a = hexToRgb(hex);
  var b = hexToRgb(bg);
  var r = Math.round(a[0] * ratio + b[0] * (1 - ratio));
  var g = Math.round(a[1] * ratio + b[1] * (1 - ratio));
  var bl = Math.round(a[2] * ratio + b[2] * (1 - ratio));
  return "rgb(" + r + "," + g + "," + bl + ")";
}

function hexToRgb(hex) {
  var h = String(hex).replace("#", "");
  if (h.length === 3) h = h[0] + h[0] + h[1] + h[1] + h[2] + h[2];
  var v = parseInt(h, 16);
  return [(v >> 16) & 255, (v >> 8) & 255, v & 255];
}

// ============================================================================================
// P10.5 Block 8, Schritt 8.5 — das Layout merken (KA-2)
// ============================================================================================
//
// Kein Serverzustand: der Ablageort ist der `localStorage` des Browsers, der Schluessel
// `sfx:graph:layout:v1:<eigener Space>` (Plan 8.5), der Wert `{"v":1,"pos":{"<id>":[x,y]}}`
// mit hoechstens 2000 Eintraegen. Gespeichert wird nach dem Einschwingen und nach dem
// Drag-Ende (gedrosselt 1 s).

function layoutKey() {
  var space = state.ownSpace || "default";
  return LAYOUT_KEY_PREFIX + space;
}

function loadStoredLayout() {
  try {
    if (typeof window === "undefined" || !window.localStorage) return {};
    var raw = window.localStorage.getItem(layoutKey());
    if (!raw) return {};
    var data = JSON.parse(raw);
    if (!data || data.v !== 1 || !data.pos) return {};
    return data.pos;
  } catch (e) {
    return {};
  }
}

function saveLayout() {
  try {
    if (typeof window === "undefined" || !window.localStorage) return;
    var pos = {};
    var count = 0;
    for (var i = 0; i < nodes.length && count < LAYOUT_MAX_ENTRIES; i++) {
      var n = nodes[i];
      pos[n.id] = [Math.round(n.x), Math.round(n.y)];
      count += 1;
    }
    window.localStorage.setItem(layoutKey(), JSON.stringify({ v: 1, pos: pos }));
    setGraphStatus("Layout gemerkt");
  } catch (e) {
    // localStorage kann gesperrt oder voll sein -- die Karte lebt weiter, nur die
    // Erinnerung faellt aus. Kein Fehler nach oben: der Nutzer muss nichts merken.
  }
}

// Gedrosselt: der erste Wunsch stellt den Timer, weitere werden nicht nachgestellt -- der
// laufende Timer speichert ohnehin den dann aktuellen Stand. Das Flag statt der Timer-Nummer:
// manche Testumgebungen fuehren `setTimeout` **synchron** aus, dann bliebe eine Timer-Nummer
// stehen und das Drosseln wuerde stillstehen.
function scheduleLayoutSave() {
  if (layoutSavePending) return;
  if (typeof window === "undefined" || !window.setTimeout) return;
  layoutSavePending = true;
  window.setTimeout(function () {
    layoutSavePending = false;
    saveLayout();
  }, LAYOUT_SAVE_DELAY_MS);
}

// "Layout zurücksetzen": die Ablage loeschen **und** die sichtbare Karte auf den
// deterministischen Seed zuruecksetzen -- sonst waere der Knopf eine Täuschung (der
// Speicher waere leer, das Bild aber die alte Karte).
function clearStoredLayout() {
  try {
    if (typeof window !== "undefined" && window.localStorage) {
      window.localStorage.removeItem(layoutKey());
    }
  } catch (e) {
    // siehe saveLayout()
  }
  pinnedIds = Object.create(null);
  for (var i = 0; i < nodes.length; i++) {
    nodes[i].pinned = false;
    nodes[i].x = 0;
    nodes[i].y = 0;
  }
  seedInitialPositions();
  lobeCache = computeLobes(visibleNodes());
  runSimulation();
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

// P10.5 Block 14, Schritt 14.3 (Plan §2.5): die **Kamera einpassen**.
//
// Nach dem Einschwingen (nicht nach einem Drag) passt die Kamera den Inhalt ein: der Umriss
// der **sichtbaren** Knoten plus `FIT_MARGIN` ergibt die Soll-Groesse; der Zoom ist so gewaehlt,
// dass der Inhalt **in** die Leinwand passt (nie ueber 100 % -- eine kleine Karte wird nicht
// aufgeblasen), und der Pan legt die **Mitte des Umrisses** in die Leinwandmitte.
//
// **Nicht** auf den Ursprung gezentriert: der Ursprung ist der Anker des **eigenen** Space
// (Plan §2.1) -- die Mitte der Welt liegt woanders. Genau das war der Fehler, den die Kamera-
// Zelle gemessen hat: der Umriss saß 32,3 px neben der Mitte (Stand 14.2).
function fitView() {
  if (nodes.length === 0 || cssWidth <= 0 || cssHeight <= 0) return;
  var shown = visibleNodes();
  var x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
  var anzahl = 0;
  for (var i = 0; i < nodes.length; i++) {
    var n = nodes[i];
    if (!shown[n.id]) continue;
    anzahl += 1;
    if (n.x < x0) x0 = n.x;
    if (n.x > x1) x1 = n.x;
    if (n.y < y0) y0 = n.y;
    if (n.y > y1) y1 = n.y;
  }
  if (!anzahl) return;
  // Der Umriss **plus** der Rand: der Inhalt soll mit Luft in der Leinwand stehen.
  var bw = (x1 - x0) + FIT_MARGIN * 2;
  var bh = (y1 - y0) + FIT_MARGIN * 2;
  // `clamp(min(w/bw, h/bh), ZOOM_MIN, 1)` -- die **beide** Grenzen: `ZOOM_MIN` unten (E3),
  // **1** oben (nie ueber 100 %).
  var z = Math.min(cssWidth / bw, cssHeight / bh);
  zoom = Math.max(ZOOM_MIN, Math.min(1, z));
  // Der Pan auf die **Mitte des Umrisses** (nicht auf den Ursprung).
  panX = cssWidth / 2 - ((x0 + x1) / 2) * zoom;
  panY = cssHeight / 2 - ((y0 + y1) / 2) * zoom;
  updateZoomReadout();
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
  // Fix C (Plan §9.4.6 Befund C, 2026-09-02): merkt sich Press-Position + getroffenen Knoten
  // (null bei einem Hintergrund-Press) -- onMouseUp entscheidet anhand der Pointer-Bewegung,
  // ob daraus ein Klick (Item oeffnen) oder nur ein abgeschlossenes Drag/Pan wird.
  pressStart = { x: e.clientX, y: e.clientY, node: hit };
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
    // P10.5 Block 14, Schritt 14.3 (Plan §2.5): der Nutzer hat die Ansicht **selbst**
    // verschoben -- seine Ansicht gewinnt, die Karte passt sich nicht neu ein.
    viewTouchedByUser = true;
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

function onMouseUp(e) {
  // Fix C (Plan §9.4.6 Befund C, 2026-09-02): ein Press, der auf einem Knoten begann und sich
  // seither um weniger als CLICK_SLOP Pixel bewegt hat, zaehlt als Klick -- Item oeffnen, kein
  // neuer ID-Lookup noetig, `selectItem` uebernimmt das (derselbe Pfad wie `#item/`-Klicks aus
  // B4). Traegt `pressStart.node` nicht (Hintergrund-Press) oder war die Bewegung groesser,
  // war es ein Drag/Pan -- das Zuruecksetzen unten laeuft in jedem Fall.
  if (pressStart && pressStart.node) {
    var dx = e.clientX - pressStart.x;
    var dy = e.clientY - pressStart.y;
    if (Math.sqrt(dx * dx + dy * dy) < CLICK_SLOP) {
      selectItem(pressStart.node.id).catch(reportUnexpectedError);
    }
  }
  if (dragNode) {
    // P10.5 Block 8: nach dem Drag-Ende werden die Lappen neu berechnet (Plan 8.1: "Berechnet
    // wird einmal nach dem Einschwingen und nach dem Drag-Ende") und die Positionen gemerkt
    // (Plan 8.5, gedrosselt 1 s).
    lobeCache = computeLobes(visibleNodes());
    // **Korrektur 2026-10-24 (an der Wegwerf-Instanz gemessen, Browser-Probe
    // `p105_b8_karte_probe.py`):** der gezogene Knoten wird **gepinnt**, nicht wieder
    // freigegeben. Vorher setzte `onMouseUp()` `fixed = false` -- der Knoten fiel damit
    // zurueck in die Simulation, und die Ablage speicherte die **zurueckgezogene**
    // Position: der Zug des Menschen war beim naechsten Oeffnen weg. (Die Simulation laeuft
    // beim Zug in der Regel noch: das Ziehen dauert laenger als das Einschwingen.) Der
    // Nutzer hat die Position **gewuellt** -- sie zu merken ist genau KA-2, und derselbe
    // Weg wie bei der gemerkten Position (`seedInitialPositions()` setzt `pinned`).
    dragNode.pinned = true;
    pinnedIds[dragNode.id] = true;
    scheduleLayoutSave();
    dragNode.fixed = false;
    dragNode = null;
  }
  panStart = null;
  pressStart = null;
}

function onMouseLeave() {
  // Fix C (Plan §9.4.6 Befund C, 2026-09-02): eigener Handler statt weiterhin `onMouseUp` --
  // der Pointer hat das Canvas verlassen, das ist nie ein Klick, egal wie klein die Bewegung
  // seit dem Press war. Reset ist identisch zum bisherigen `onMouseUp`-Verhalten.
  if (dragNode) {
    dragNode.fixed = false;
    dragNode = null;
  }
  panStart = null;
  pressStart = null;
  // **P10.5 Block 8, Korrektur 2026-10-24 (an der Wegwerf-Instanz gemessen, Browser-Probe
  // `p105_b8_karte_probe.py`):** der Fokus gehoert zum Zeiger. Verlaesst der Zeiger das
  // Canvas, endet der Fokus -- und mit ihm das Abdunkeln (Plan 8.4: "Ruhezustand ohne
  // Fokus: alles voll deckend"). Vorher blieb `hoverId` stehen: die Karte blieb
  // abgedunkelt, bis der Zeiger wieder ueber sie fuhr.
  if (hoverId !== null) {
    hoverId = null;
    draw();
  }
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
  // P10.5 Block 14, Schritt 14.3 (Plan §2.5): der Nutzer hat **selbst** gezoomt -- seine
  // Ansicht gewinnt, die Karte passt sich danach nicht mehr neu ein.
  viewTouchedByUser = true;
  updateZoomReadout();
  draw();
}

function onDoubleClick() {
  // P10.5 Block 14, Schritt 14.3 (Plan §2.5): der Doppelklick **passt die Kamera ein**. Vorher
  // war er "Ansicht zurueck" (Zoom 1, Pan 0) -- das ist die Sicht **ohne** Einpassen, also
  // genau das, was die Kamera-Zelle als rot gemessen hat (der Umriss 32,3 px neben der Mitte).
  //
  // Der Doppelklick zaehlt **nicht** als "der Nutzer hat die Ansicht selbst gewaehlt": er **ist**
  // die gewaehlte Ansicht. Er setzt `viewTouchedByUser` deshalb nicht.
  fitView();
  draw();
}
