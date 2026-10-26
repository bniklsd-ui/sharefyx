// P10.5 Block 14, Schritt 14.1 — der Wächter-Harness für den **Seed** des Kartenlayouts.
//
// **Was gemessen wird:** die reine Geometrie des neuen Seeds — die Welt, die
// `graph.js :: computeRegions()` erzeugt, bevor die Kraftsimulation ueberhaupt anfaengt.
//
// Plan: `docs/concepts/phase10_5_block14_kartenlayout_plan.md` §1–§2 (die vier Schichten) und
// §5 (P10.5-65/66/68). **Der Seed wird gemessen, nicht die Karte:** die Simulation (Schritt
// 14.2) zerlegt den Seed heute noch (die Zentrums-Gravitation zieht alle Spaces auf einen
// Punkt) — die Browser-Probe `p105_b14_layout_probe.py` misst deshalb bis Schritt 14.2 nur
// den **Seed** als das, was sie messen kann: die Determinismus-Zelle (P10.5-65).
//
// **Muster:** `p105_b8_c2_probe.mjs` — das echte `graph.js` wird in Node geladen (mit einem
// minimalen DOM-Shim), nicht nachgebaut. `computeRegions()` und `hashString()` sind darum
// **exportiert** (kein Testhaken: rechnende Funktionen ohne Zustand und ohne DOM).
//
// **Fünf Messungen, fünf Gegenläufe.** Ein Wächter ohne Gegenlauf beweist nichts: eine
// Messung, die die falsche Sache misst, ist grün und falsch zugleich (diese Fehlerklasse hat
// dieser Ordner zweimal gesehen). Jeder Gegenlauf patcht **eine** Regel in einer Kopie von
// `graph.js` und muss **genau die** zugehörige Messung rot machen:
//
// | Messung | Regel | Gegenlauf | Der Fehler |
// |---|---|---|---|
// | `regionen` | §2.1 L1 — eine Region je Space | `anker` | alle Anker liegen auf einem Punkt |
// | `inseln` | §2.2 L2 — die Ordner bilden eigene Inseln | `inselabstand` | alle Inseln liegen auf dem Anker |
// | `spiralen` | §2.3 L3 — die Items liegen auf einer Goldwinkel-Spirale | `itemradius` | alle Items liegen auf einem Kreis |
// | `stabilitaet` | §2.1 — ein neues Item verschiebt die Anker **nur**, wenn es den groessten Space vergroessert | `slot` | `SLOT` haengt an der Item-Zahl |
// | `determinismus` | §1 — der Zufall ist der Hash, nicht der Zufallsgenerator | `jitter` | der Jitter kommt aus `Math.random()` |
//
// Aufruf:  `node phase10_5_finishing/probes/p105_b14_layout_probe.mjs [--gegenlauf NAME]`
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

// -- Die Gegenläufe: je einer ein eingebauter Fehler, der genau eine Messung rot macht -------
//
// **Die Anker sind eindeutig** (Regel + Nachbarzeile, nicht nur ein Wert) — sonst patcht der
// Gegenlauf den Kommentar ueber der Regel statt der Regel (diese Fehlerklasse hat die
// C2-Probe einmal gemacht).
const GEGENLAEUFE = {
  // Die Anker liegen alle auf einem Punkt: die Spaces fallen uebereinander.
  anker: [
    ["    var abstand = k === 0 ? 0 : slot * Math.sqrt(k);",
     "    var abstand = 0;"],
  ],
  // Alle Ordner-Inseln liegen auf dem Anker: die Ordner fallen uebereinander.
  inselabstand: [
    ["      var jabstand = space.radius * ISLAND_FACTOR * Math.sqrt((j + 1) / F);",
     "      var jabstand = 0;"],
  ],
  // Alle Items einer Insel liegen auf einem Kreis: es ist keine Spirale.
  itemradius: [
    ["        var irad = ITEM_STEP * Math.sqrt(t);",
     "        var irad = ITEM_STEP;"],
  ],
  // `SLOT` haengt an der Item-Zahl: jedes neue Item verschiebt alle Anker.
  slot: [
    ["  var slot = 2 * maxR + REGION_GAP;",
     "  var slot = 2 * maxR + REGION_GAP + nodeList.length;"],
  ],
  // Der Jitter kommt aus dem Zufallsgenerator: die Karte ist zwischen zwei Laeufen anders.
  jitter: [
    ["          insel.x + Math.cos(iwinkel) * irad + seedJitter(item.id, 1) * ITEM_JITTER_PX,",
     "          insel.x + Math.cos(iwinkel) * irad + (Math.random() - 0.5) * ITEM_JITTER_PX,"],
  ],
};

// -- Modul laden (mit Patch) --------------------------------------------------------------------

let moduleCounter = 0;
function loadGraphModule(patch, suffix) {
  let source = fs.readFileSync(GRAPH_JS, "utf8");
  if (patch) {
    for (const [oldText, newText] of patch) {
      if (!source.includes(oldText)) {
        throw new Error("Gegenlauf-Anker nicht gefunden: " + JSON.stringify(oldText.slice(0, 60)));
      }
      source = source.replace(oldText, newText);
    }
  }
  // Die Kopie liegt in /tmp; ihre Importe zeigen auf die **echten** Nachbarmodule.
  source = source.replace(/from "\.\/([a-z_]+\.js)"/g,
    (m, name) => 'from "' + pathToFileURL(path.join(STATIC_DIR, name)).href + '"');
  moduleCounter += 1;
  const tmp = path.join(os.tmpdir(), "p105_b14_seed_" + suffix + "_" + moduleCounter + ".mjs");
  fs.writeFileSync(tmp, source, "utf8");
  return import(pathToFileURL(tmp).href);
}

// -- DOM-Shim ------------------------------------------------------------------------------------
//
// Nur so viel, wie der **Import** braucht: `graph.js` selbst greift im Modulkoerper nicht
// auf das DOM zu (alles laeuft in `init()`), aber die Nachbarmodule (`editor.js`,
// `loading.js`) werden beim Import geladen. Muster: `p105_b8_c2_probe.mjs`.

function makeElement(extra) {
  return Object.assign({
    value: "", textContent: "", attributes: {}, listeners: {}, options: [],
    getAttribute(k) { return this.attributes[k] || null; },
    setAttribute(k, v) { this.attributes[k] = v; },
    removeAttribute(k) { delete this.attributes[k]; },
    addEventListener(t, fn) { this.listeners[t] = fn; },
    appendChild(child) { this.options.push(child); },
    removeChild(child) {
      const i = this.options.indexOf(child);
      if (i >= 0) this.options.splice(i, 1);
    },
  }, extra || {});
}

globalThis.document = {
  getElementById() { return null; },
  addEventListener() {},
  querySelectorAll: () => [],
  createElement: () => makeElement(),
};
globalThis.window = {
  devicePixelRatio: 1,
  matchMedia: () => ({ matches: false }),
  addEventListener() {},
  setInterval() {},
  localStorage: {
    getItem: () => null,
    setItem() {},
    removeItem() {},
    clear() {},
  },
  setTimeout: (fn) => { fn(); return 0; },
  clearTimeout() {},
};
globalThis.sessionStorage = { getItem: () => null, setItem() {}, removeItem() {} };
globalThis.requestAnimationFrame = () => 0;
globalThis.cancelAnimationFrame = () => {};
globalThis.fetch = () => Promise.reject(new Error("der Harness ruft die API nicht auf"));

// -- Die Daten (derselbe Fixture wie die Browser-Probe) -----------------------------------------
//
// **Fuenf Spaces, 152 Items (30/32/30/30/30)**, vier Ordner je Space, deterministische IDs
// (`itm_%08x` — dieselbe Zaehlung wie `p105_b14_layout_probe.py :: _seed()`). Der `beta`-Space
// hat **32** Items, damit "der groesste Space" eindeutig ist (Plan §2.1 / Abnahme P10.5-68).
//
// **Keine Wurzel-Items** (`folder: ""`) — derselbe Fixture wie die Browser-Probe. Die Messung
// `inseln` vergleicht einen Item mit dem Mittelpunkt **seiner** Insel; bei Wurzel-Items am
// Anker liegen die Inseln mit den Startwerten (Plan §2.2) so nah beieinander, dass sich die
// Kreise ueberlappen — das ist eine **Konstantenfrage** (Schritt 14.4 misst sie), keine
// Regelfrage, und der Wächter soll die **Regel** pruefen.

const SPACES = ["alpha", "beta", "gamma", "delta", "epsilon"];
const ITEMS_PRO_SPACE = { alpha: 30, beta: 32, gamma: 30, delta: 30, epsilon: 30 };
const ORDNER = ["ordner-1", "ordner-2", "ordner-3", "ordner-4"];
const OWN_SPACE = "alpha";
const CX = 567;
const CY = 530.5;

function buildFixture() {
  const nodes = [];
  let zaehler = 0;
  for (const space of SPACES) {
    for (let i = 0; i < ITEMS_PRO_SPACE[space]; i++) {
      zaehler += 1;
      nodes.push({
        id: "itm_" + zaehler.toString(16).padStart(8, "0"),
        title: space + " Item " + (i + 1),
        space: space,
        folder: ORDNER[i % ORDNER.length],
        own: space === OWN_SPACE,
        writable: true,
        type: "note",
        status: "active",
        tags: [],
      });
    }
  }
  return nodes;
}

// -- Die Rechenhilfen ----------------------------------------------------------------------------

function centroid(points) {
  let sx = 0;
  let sy = 0;
  for (const p of points) {
    sx += p[0];
    sy += p[1];
  }
  return [sx / points.length, sy / points.length];
}

function dist(a, b) {
  return Math.hypot(a[0] - b[0], a[1] - b[1]);
}

/** Der Abstand zum naechsten Mittelpunkt — und der Abstand zum naechsten **anderen**. */
function nearest(xy, centers, own) {
  let best = Infinity;
  let bestName = null;
  let bestOther = Infinity;
  let bestOtherName = null;
  for (const [name, c] of centers) {
    const d = dist(xy, c);
    if (name === own) continue;
    if (d < bestOther) { bestOther = d; bestOtherName = name; }
  }
  for (const [name, c] of centers) {
    const d = dist(xy, c);
    if (d < best) { best = d; bestName = name; }
  }
  return { name: bestName, d: best, other: bestOther, otherName: bestOtherName };
}

/** Der Winkelabstand zweier Punkte um ihren Mittelpunkt (0..360 Grad). */
function winkelAbstand(a, b, center) {
  const a1 = Math.atan2(a[1] - center[1], a[0] - center[0]);
  const a2 = Math.atan2(b[1] - center[1], b[0] - center[0]);
  let d = Math.abs(a1 - a2) * 180 / Math.PI;
  if (d > 180) d = 360 - d;
  return d;
}

// -- Die Messungen --------------------------------------------------------------------------------

const graph = await loadGraphModule(gegenlauf ? GEGENLAEUFE[gegenlauf] : null, "normal");
const { computeRegions } = graph;

const nodes = buildFixture();
const welt = computeRegions(nodes, CX, CY, OWN_SPACE);

// **1) Die Regionen (L1)** — der Item liegt seinem **eigenen** Space am naechsten.
const schwerpunkte = [];
for (const name of SPACES) {
  const punkte = [];
  for (const n of nodes) {
    if (n.space !== name) continue;
    const p = welt.pos[n.id];
    if (p) punkte.push(p);
  }
  schwerpunkte.push([name, centroid(punkte)]);
}
let richtig = 0;
const falscheBeispiele = [];
let engsterAbstand = Infinity;
for (const n of nodes) {
  const p = welt.pos[n.id];
  if (!p) continue;
  const near = nearest(p, schwerpunkte, n.space);
  const eigenAbstand = dist(p, schwerpunkte.find((s) => s[0] === n.space)[1]);
  const fremdAbstand = near.other;
  engsterAbstand = Math.min(engsterAbstand, fremdAbstand - eigenAbstand);
  if (near.name === n.space) richtig += 1;
  else if (falscheBeispiele.length < 5) {
    falscheBeispiele.push({ id: n.id, space: n.space, naechster: near.name });
  }
}
const regionen = {
  knoten: nodes.length,
  richtig: richtig,
  anteil: richtig / nodes.length,
  engster_abstand_px: engsterAbstand,
  schwerpunkte: Object.fromEntries(schwerpunkte.map((s) => [s[0], s[1]])),
  anker: Object.fromEntries(Object.keys(welt.spaces).map((k) => [k, [welt.spaces[k].x, welt.spaces[k].y]])),
  beispiele_falsch: falscheBeispiele,
  ok: richtig / nodes.length >= 0.95,
};

// **2) Die Ordner-Inseln (L2)** — die Items einer Insel bilden eine **Gruppe**: der mittlere
// Abstand zweier Items **derselben** Insel ist deutlich kleiner als der mittlere Abstand
// zweier Items **verschiedener** Inseln desselben Spaces.
//
// **Warum nicht "das naechste Inselzentrum"?** Das war die erste Fassung -- und sie ist an
// der **Klinge** gescheitert: der Item `itm_0000008b` lag 35,95 px von seinem eigenen
// Inselzentrum und 36,44 px von einem fremden (der Zufalls-Jitter von 4 px hat die Reihenfolge
// gekippt). Der Grund ist der **Goldwinkel**: die Inseln 1 und 4 liegen nur 52,5 Grad
// auseinander (3 · 137,5 Grad mod 360), ihre Zentren deshalb 66 px auseinander -- mit den
// Startwerten des Plans (14.4 justiert sie) ist der *Abstand* zwischen zwei Inselzentren
// keine verlaessliche Groesse. Die **Gruppenbildung** dagegen ist es: sie ist um eine
// Groessenordnung klarer als der_Zufall_ (Faktor ~3 gegen ~1).
//
// Und die Inselmitten sind **verschieden** (keine zwei Inseln auf demselben Punkt).
const inselRoh = [];
let inselRichtig = 0;
let inselGeprueft = 0;
const inselBeispiele = [];
for (const name of SPACES) {
  const space = welt.spaces[name];
  if (!space) continue;
  const zentren = [];
  for (const key of Object.keys(space.folders)) {
    const f = space.folders[key];
    if (!f.items.length) continue;      // die leere Wurzel traegt nichts bei
    zentren.push([key, [f.x, f.y]]);
  }
  // (a) die Inselmitten sind verschieden
  let kleinsterMittenabstand = Infinity;
  for (let i = 0; i < zentren.length; i++) {
    for (let j = i + 1; j < zentren.length; j++) {
      kleinsterMittenabstand = Math.min(kleinsterMittenabstand, dist(zentren[i][1], zentren[j][1]));
    }
  }
  // (b) die Gruppenbildung: der mittlere Abstand **innerhalb** einer Insel gegen den mittleren
  // Abstand **zwischen** zwei Inseln
  let innerhalbSumme = 0;
  let innerhalbAnzahl = 0;
  let zwischenSumme = 0;
  let zwischenAnzahl = 0;
  for (let i = 0; i < zentren.length; i++) {
    const itemsA = space.folders[zentren[i][0]].items;
    for (let a = 0; a < itemsA.length; a++) {
      for (let b = a + 1; b < itemsA.length; b++) {
        innerhalbSumme += dist(welt.pos[itemsA[a]], welt.pos[itemsA[b]]);
        innerhalbAnzahl += 1;
      }
    }
    for (let j = i + 1; j < zentren.length; j++) {
      const itemsB = space.folders[zentren[j][0]].items;
      for (const ia of itemsA) {
        for (const ib of itemsB) {
          zwischenSumme += dist(welt.pos[ia], welt.pos[ib]);
          zwischenAnzahl += 1;
        }
      }
    }
  }
  const innerhalb = innerhalbAnzahl ? innerhalbSumme / innerhalbAnzahl : 0;
  const zwischen = zwischenAnzahl ? zwischenSumme / zwischenAnzahl : 0;
  const faktor = innerhalb > 0 ? zwischen / innerhalb : 0;
  inselGeprueft += 1;
  const gut = kleinsterMittenabstand > 1 && innerhalb > 0 && faktor >= 1.8;
  if (gut) inselRichtig += 1;
  else if (inselBeispiele.length < 5) {
    inselBeispiele.push({
      space: name, innerhalb: innerhalb, zwischen: zwischen, faktor: faktor,
      kleinster_mittenabstand: kleinsterMittenabstand,
    });
  }
  inselRoh.push({ space: name, innerhalb: innerhalb, zwischen: zwischen, faktor: faktor,
                  kleinster_mittenabstand: kleinsterMittenabstand });
}
const inseln = {
  spaces_geprueft: inselGeprueft,
  spaces_ok: inselRichtig,
  roh: inselRoh,
  beispiele_falsch: inselBeispiele,
  ok: inselGeprueft > 0 && inselRichtig === inselGeprueft,
};

// **3) Die Itemspirale (L3)** — der Radius waechst mit dem Rang (Hash der ID), und der
// Winkelabstand zweier Nachbarn ist der **Goldwinkel** (137,5078 Grad).
const goldwinkel = 137.50776405003785;
let spiralenGeprueft = 0;
let spiralenOk = 0;
const spiralenBeispiele = [];
for (const name of SPACES) {
  const space = welt.spaces[name];
  if (!space) continue;
  for (const key of Object.keys(space.folders)) {
    const f = space.folders[key];
    if (f.items.length < 4) continue;
    const center = [f.x, f.y];
    const radien = f.items.map((id) => dist(welt.pos[id], center));
    const mitte = radien.length / 2;
    const unten = radien.slice(0, Math.floor(mitte)).reduce((a, b) => a + b, 0) / Math.floor(mitte);
    const oben = radien.slice(Math.ceil(mitte)).reduce((a, b) => a + b, 0) / (radien.length - Math.ceil(mitte));
    // der Winkelabstand: nur zwischen Paaren, deren Radius gross genug ist, dass der Jitter
    // den Winkel nicht dominiert (Amplitude 4 px -> bei 12 px Radius sind das ~18 Grad)
    const winkel = [];
    for (let i = 0; i + 1 < f.items.length; i++) {
      const r0 = radien[i];
      const r1 = radien[i + 1];
      if (r0 < 12 || r1 < 12) continue;
      winkel.push(winkelAbstand(welt.pos[f.items[i]], welt.pos[f.items[i + 1]], center));
    }
    const mittlererWinkel = winkel.length
      ? winkel.reduce((a, b) => a + b, 0) / winkel.length : null;
    spiralenGeprueft += 1;
    const gut = oben > unten + 4
      && mittlererWinkel !== null
      && mittlererWinkel > 100 && mittlererWinkel < 175;
    if (gut) spiralenOk += 1;
    else if (spiralenBeispiele.length < 5) {
      spiralenBeispiele.push({
        space: name, ordner: key, radius_unten: unten, radius_oben: oben,
        winkel: mittlererWinkel,
      });
    }
  }
}
const spiralen = {
  inseln_geprueft: spiralenGeprueft,
  inseln_ok: spiralenOk,
  beispiele_falsch: spiralenBeispiele,
  ok: spiralenGeprueft > 0 && spiralenOk === spiralenGeprueft,
};

// **4) Die Stabilitaet (Abnahme P10.5-68, auf der Seed-Ebene)** — ein neues Item in einem
// **nicht groessten** Space laesst die **Anker** byte-gleich (Plan §2.1: "ein neues Item
// verschiebt die Anker **nur**, wenn es den **groessten** Space vergroessert").
//
// **Warum der Anker das Kriterium ist und nicht die Item-Positionen:** die Item-Positionen
// *sind* eine **Differenz zweier Aufrufe** — und damit auch eine Determinismus-Messung. Ein
// Gegenlauf, der den Jitter zufaellig macht (die Determinismus-Zelle), wuerde sie mit
// rotmachen: der Zufalls-Jitter verschiebt jedes Item zwischen zwei Aufrufen um bis zu 8 px.
// Der Anker haengt **nicht** am Jitter (er haengt am Hash des Space-Namens und an `SLOT`),
// er ist damit die Groesse, die die Regel des Plans traegt. Die Item-Positionen stehen als
// Rohwert daneben (im Normalfall: 0).
//
// **Der wachsende Space selbst darf sich bewegen** -- seine Region waechst mit (der Radius
// folgt der Wurzel der Item-Zahl), seine Inseln ruecken also nach aussen (gemessen: 1,1 px
// bei 30 -> 31 Items). Das ist die gewollte Wirkung, nicht der Fehler; die Abnahme zaehlt
// ausdruecklich die Knoten **anderer** Spaces.
const wachser = "epsilon";                    // 30 Items — `beta` (32) ist der groesste
const vorher = computeRegions(nodes, CX, CY, OWN_SPACE);
const mitNeuem = nodes.concat([{
  id: "itm_00000901", title: "Probe Stabilitaet", space: wachser,
  folder: ORDNER[0], own: false, writable: true, type: "note", status: "active", tags: [],
}]);
const nachher = computeRegions(mitNeuem, CX, CY, OWN_SPACE);
let ankerVerschoben = 0;
let positionenVerschoben = 0;
let eigeneVerschoben = 0;
let groessterVersatz = 0;
let eigenerVersatz = 0;
for (const name of Object.keys(vorher.spaces)) {
  const a = vorher.spaces[name];
  const b = nachher.spaces[name];
  if (!b) continue;
  if (a.x !== b.x || a.y !== b.y) {
    ankerVerschoben += 1;
    groessterVersatz = Math.max(groessterVersatz, dist([a.x, a.y], [b.x, b.y]));
  }
  for (const key of Object.keys(a.folders)) {
    for (const id of a.folders[key].items) {
      const p = vorher.pos[id];
      const q = nachher.pos[id];
      if (!p || !q) continue;
      const d = dist(p, q);
      if (p[0] === q[0] && p[1] === q[1]) continue;
      if (name === wachser) {
        eigeneVerschoben += 1;
        eigenerVersatz = Math.max(eigenerVersatz, d);
      } else {
        positionenVerschoben += 1;
        groessterVersatz = Math.max(groessterVersatz, d);
      }
    }
  }
}
const stabilitaet = {
  wachser_space: wachser,
  groesster_space: Object.entries(ITEMS_PRO_SPACE).sort((a, b) => b[1] - a[1])[0][0],
  anker_verschoben: ankerVerschoben,
  groesster_anker_versatz_px: groessterVersatz,
  ok: ankerVerschoben === 0,
  // Rohwerte (nicht Teil des Kriteriums, siehe die Begruendung oben)
  positionen_verschoben: positionenVerschoben,
  groesster_versatz_px: groessterVersatz,
  eigene_positionen_verschoben: eigeneVerschoben,
  eigener_versatz_px: eigenerVersatz,
};

// **5) Der Determinismus (Abnahme P10.5-65)** — dieselbe Eingabe ergibt dieselbe Ausgabe.
const wieder = computeRegions(buildFixture(), CX, CY, OWN_SPACE);
let abweichung = 0;
let verglichen = 0;
for (const id of Object.keys(welt.pos)) {
  const p = welt.pos[id];
  const q = wieder.pos[id];
  if (!q) continue;
  verglichen += 1;
  abweichung = Math.max(abweichung, Math.abs(p[0] - q[0]), Math.abs(p[1] - q[1]));
}
const determinismus = {
  knoten: Object.keys(welt.pos).length,
  verglichen: verglichen,
  max_abweichung_px: abweichung,
  ok: verglichen === Object.keys(welt.pos).length && abweichung <= 1.0 && verglichen > 0,
};

const messungen = { regionen, inseln, spiralen, stabilitaet, determinismus };

const bericht = {
  probe: "p105_b14_layout_probe",
  schritt: "14.1",
  fixture: {
    spaces: SPACES.length,
    items: nodes.length,
    items_pro_space: ITEMS_PRO_SPACE,
    own_space: OWN_SPACE,
    ordner: ORDNER.length,
    leinwand: [CX, CY],
  },
  reihenfolge: welt.order,
  messungen,
  alle_kriterien_erfuellt: Object.values(messungen).every((m) => m.ok),
  gegenlauf: gegenlauf || null,
};
process.stdout.write(JSON.stringify(bericht, null, 2) + "\n");
