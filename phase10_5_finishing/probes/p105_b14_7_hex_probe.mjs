// P10.5 Block 14.7, Schritt 14.7.1 — die Pflichteigenschaften der Anker-Regel (Plan
// `docs/concepts/phase10_5_block14_7_plan.md` §2.1, H1–H5), gemessen am **echten**
// `graph.js :: computeRegions()` — nicht nachgebaut.
//
// Die Konstanten `ANCHOR_LAYOUT`/`ANCHOR_HEX_ORDER`/`LOBE_SCALE` werden in einer **Kopie** von
// `graph.js` gesetzt (der Arbeitsbaum bleibt unberuehrt) — derselbe Weg wie die Gegenlaeufe von
// `p105_b14_layout_probe.mjs`, dessen Lader und DOM-Shim hier im Kleinen wiederholt sind.
//
// Aufruf:  node p105_b14_7_hex_probe.mjs [--gegenlauf=ring]
// Ausgabe: JSON auf stdout — je Eigenschaft `{ok, ...}`.
//
// Gegenlauf `ring`: die Plaetze werden **gleichmaessig** auf einen Ring verteilt (2π/(Spaces−1))
// — der Fall, den H1 ausschliessen soll (der Platz haengt dann an der Zahl der Spaces).

import { fileURLToPath, pathToFileURL } from "node:url";
import path from "node:path";
import fs from "node:fs";
import os from "node:os";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.resolve(HERE, "../..");
const STATIC_DIR = path.join(REPO, "phase5_ui/webui/static/js");
const GRAPH_JS = path.join(STATIC_DIR, "graph.js");
const gegenlauf = (process.argv.find((a) => a.startsWith("--gegenlauf=")) || "").split("=")[1] || null;

let zaehlerModul = 0;
async function lade(konstanten, patch) {
  let q = fs.readFileSync(GRAPH_JS, "utf8");
  for (const [name, wert] of Object.entries(konstanten)) {
    const re = new RegExp("^const " + name + " = [^;]+;", "m");
    if (!re.test(q)) throw new Error("Konstante fehlt: " + name);
    q = q.replace(re, "const " + name + " = " + wert + ";");
  }
  for (const [alt, neu] of patch || []) {
    if (!q.includes(alt)) throw new Error("Gegenlauf-Anker nicht gefunden: " + alt.slice(0, 60));
    q = q.replace(alt, neu);
  }
  q = q.replace(/from "\.\/([a-z_]+\.js)"/g,
    (m, n) => 'from "' + pathToFileURL(path.join(STATIC_DIR, n)).href + '"');
  zaehlerModul += 1;
  const tmp = path.join(os.tmpdir(), "p105_b14_7_hex_" + process.pid + "_" + zaehlerModul + ".mjs");
  fs.writeFileSync(tmp, q, "utf8");
  return import(pathToFileURL(tmp).href);
}

const el = () => ({ value: "", textContent: "", attributes: {}, options: [], getAttribute() { return null; },
  setAttribute() {}, removeAttribute() {}, addEventListener() {}, appendChild() {}, removeChild() {} });
globalThis.document = { getElementById: () => null, addEventListener() {}, querySelectorAll: () => [], createElement: el };
globalThis.window = { devicePixelRatio: 1, matchMedia: () => ({ matches: false }), addEventListener() {},
  setInterval() {}, localStorage: { getItem: () => null, setItem() {}, removeItem() {}, clear() {} },
  setTimeout: (fn) => { fn(); return 0; }, clearTimeout() {} };
globalThis.sessionStorage = { getItem: () => null, setItem() {}, removeItem() {} };
globalThis.requestAnimationFrame = () => 0;
globalThis.cancelAnimationFrame = () => {};
globalThis.fetch = () => Promise.reject(new Error("kein Netz"));

// derselbe Fixture wie `p105_b14_layout_probe.mjs` (5 Spaces, 152 Items, 4 Ordner)
const SPACES = ["alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta"];
const PRO = { alpha: 30, beta: 32, gamma: 30, delta: 30, epsilon: 30, zeta: 30, eta: 30, theta: 30 };
function fixture(anzahlSpaces, extra) {
  const nodes = [];
  let z = 0;
  for (const sp of SPACES.slice(0, anzahlSpaces)) {
    const n = PRO[sp] + ((extra && extra[sp]) || 0);
    for (let i = 0; i < n; i++) {
      z += 1;
      nodes.push({ id: "itm_" + z.toString(16).padStart(8, "0"), space: sp, folder: "ordner-" + ((i % 4) + 1) });
    }
  }
  return nodes;
}
const CX = 567, CY = 530.5, OWN = "alpha";
const d = (a, b) => Math.hypot(a.x - b.x, a.y - b.y);

const GEGEN = {
  ring: [["      var platz = hexPlatz(k, ANCHOR_HEX_ORDER);",
          "      var platz = [Math.cos(2 * Math.PI * k / (reihenfolge.length - 1)), Math.sin(2 * Math.PI * k / (reihenfolge.length - 1))];"]],
};

const ergebnis = { probe: "p105_b14_7_hex_probe", gegenlauf, ordnungen: {} };

for (const ordnung of ["fortlaufend", "gegenueber"]) {
  const g = await lade({ ANCHOR_LAYOUT: '"hex"', ANCHOR_HEX_ORDER: '"' + ordnung + '"' }, gegenlauf ? GEGEN[gegenlauf] : null);
  const r = {};
  // H1 — der k-te **Platz** haengt nur von k ab, nie von der Zahl der Spaces (Plan §2.1,
  // datierte Korrektur 2026-10-29: "ein neuer Space verschiebt keinen vorhandenen Anker" gilt
  // schon in Block 14 nicht — die Spaces sind nach dem **Hash** ihres Namens sortiert, ein neuer
  // kann sich in die Reihe schieben; bei 5 → 6 Spaces tut `zeta` genau das). Gemessen: Platz k
  // bei 5 und bei 6 Spaces (`maxR` gleich, `beta` bleibt der groesste).
  const w5 = g.computeRegions(fixture(5), CX, CY, OWN);
  const w6 = g.computeRegions(fixture(6), CX, CY, OWN);
  let maxVersatz = 0;
  for (let k = 0; k < w5.order.length; k++)
    maxVersatz = Math.max(maxVersatz, d(w5.spaces[w5.order[k]], w6.spaces[w6.order[k]]));
  r.H1 = { reihenfolge_5: w5.order, reihenfolge_6: w6.order,
           max_versatz_platz_px: +maxVersatz.toFixed(6), ok: maxVersatz < 1e-9 };
  // H2 — kein Ankerpaar naeher als `slot` (bei 8 Spaces, zwei Ringe)
  const w8 = g.computeRegions(fixture(8), CX, CY, OWN);
  let maxR = 0;
  for (const n of w8.order) maxR = Math.max(maxR, w8.spaces[n].radius);
  const slot = 2 * maxR + 40;
  let minPaar = Infinity;
  for (let i = 0; i < w8.order.length; i++)
    for (let j = i + 1; j < w8.order.length; j++)
      minPaar = Math.min(minPaar, d(w8.spaces[w8.order[i]], w8.spaces[w8.order[j]]));
  r.H2 = { slot_px: slot, min_paar_px: +minPaar.toFixed(4), ok: minPaar >= slot - 1e-6 };
  // H3 — ein Item in einem **kleineren** Space bewegt keinen Anker
  const wPlus = g.computeRegions(fixture(5, { epsilon: 1 }), CX, CY, OWN);
  let m3 = 0;
  for (const n of w5.order) m3 = Math.max(m3, d(w5.spaces[n], wPlus.spaces[n]));
  r.H3 = { max_versatz_px: m3, ok: m3 === 0 };
  // H5 — Determinismus
  const w5b = g.computeRegions(fixture(5), CX, CY, OWN);
  let m5 = 0;
  for (const id of Object.keys(w5.pos)) m5 = Math.max(m5, Math.hypot(w5.pos[id][0] - w5b.pos[id][0], w5.pos[id][1] - w5b.pos[id][1]));
  r.H5 = { max_px: m5, ok: m5 === 0 };
  ergebnis.ordnungen[ordnung] = r;
}

// H4 — die Nullwerte (`"spirale"`, `LOBE_SCALE = 1`) ergeben **bitgleich** Block 14. Die Referenz
// ist Block 14 selbst: dieselbe `graph.js` **ohne** die 14.7-Zeilen (Hex-Zweig und die beiden
// `*= LOBE_SCALE`). [2026-10-29, 14.7.3: vorher war die Referenz der Arbeitsbaum — der traegt
// seit 14.7.3 die gewaehlten Werte, nicht mehr die Nullwerte.]
const BLOCK14 = [
  ['    if (ANCHOR_LAYOUT === "hex" && k > 0) {', '    if (false) {'],
  ["      jabstand *= LOBE_SCALE;", ""],
  ["        irad *= LOBE_SCALE;", ""],
];
const heute = await lade({}, BLOCK14);
const null_ = await lade({ ANCHOR_LAYOUT: '"spirale"', LOBE_SCALE: "1" }, null);
const a = heute.computeRegions(fixture(5), CX, CY, OWN);
const b = null_.computeRegions(fixture(5), CX, CY, OWN);
let gleich = true;
for (const id of Object.keys(a.pos)) if (a.pos[id][0] !== b.pos[id][0] || a.pos[id][1] !== b.pos[id][1]) gleich = false;
let maxR5 = 0;
for (const n of b.order) maxR5 = Math.max(maxR5, b.spaces[n].radius);
const slot5 = 2 * maxR5 + 40;
let spiraleOk = true;
b.order.forEach((n, k) => {
  const soll = k === 0 ? 0 : slot5 * Math.sqrt(k);
  if (Math.abs(Math.hypot(b.spaces[n].x - CX, b.spaces[n].y - CY) - soll) > 1e-9) spiraleOk = false;
});
ergebnis.H4 = { bitgleich: gleich, spirale_sqrt_k: spiraleOk, ok: gleich && spiraleOk };

ergebnis.alle_ok = ergebnis.H4.ok && Object.values(ergebnis.ordnungen).every(
  (r) => r.H1.ok && r.H2.ok && r.H3.ok && r.H5.ok);
process.stdout.write(JSON.stringify(ergebnis, null, 2) + "\n");
