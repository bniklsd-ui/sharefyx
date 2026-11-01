// P10.5 Block 16 — der Launch-Film (Plan §3.5). Jedes Bild ist eine reine Funktion seiner Nummer.
//
// Die Szenen liegen als Kacheln auf **einer** Fläche, entlang der Striche einer „4“ (Raster 4 × 7:
// Abstrich schräg — Spalten 1,0 → 0,6 → 0,2, damit er als Schräge liest, nicht als Treppe —,
// Querstrich Zeile 4, senkrechter Strich Spalte 2). Die Kamera fährt ohne Schnitt
// von Kachel zu Kachel; am Ende zoomt sie heraus, alle Kacheln ordnen sich gleichzeitig zur
// sauberen 4, zerfallen in Punkte und die Punkte bilden die gesetzte Schrift „4.0.0“ (N1).
// Drei Kacheln kommen im Aussehen von v3.1.6 an und werden per Lichtstreif neu (N2, „3 → 4“).
//
// `zustand(n, geo)` ist **rein** (kein DOM, keine Uhr) — die Wächter rechnen es in Node nach.
// `geo` sind die einmal beim Laden gemessenen Größen (Lage der Glyphe, Zielpunkte der Punkte).

import { W, H, clamp, lerp, easeInOut, phase, prng } from "./stage.js";

export const FPS = 60;
export const FRAMES = 3300; // 55 s
export const TILE_W = 1600, TILE_H = 1000, CELL_W = 1800, CELL_H = 1200;
export const Z_KACHEL = 0.85; // eine Kachel füllt das Bild, unten bleibt Platz für die Tafel

// Kacheln: Zelle [Spalte, Zeile], Bild (neu), optional alt (Lichtstreif), Bildfolge, Wechsel.
export const KACHELN = [
  { id: "s1", zelle: [2, 0], bild: "neu/s1__uebersicht", alt: "alt/s1__uebersicht", streif: [250, 300] },
  { id: "s2", zelle: [1, 1], folge: { prefix: "neu/s2__t", n: 107, von: 380, bis: 560 } },
  { id: "s3", zelle: [0.6, 2], bild: "neu/s3__kaestchen", alt: "alt/s2__fertig", streif: [670, 740] },
  { id: "s4", zelle: [0.2, 3], bild: "neu/s4__rot", danach: { bild: "neu/s4__gross", ab: 885 } },
  { id: "s5", zelle: [0, 4], bild: "neu/s5__ganz", alt: "alt/s5__ganz", streif: [1020, 1110], karte: true },
  { id: "s5b", zelle: [1, 4], bild: "neu/s5__suche", karte: true },
  { id: "s6", zelle: [2, 4], bild: "neu/s6__in_arbeit", karte: true },
  { id: "s7", zelle: [3, 4], bild: "neu/s7__dialog", danach: { bild: "neu/s7__danach", ab: 1565 } },
  { id: "s8", zelle: [2, 1], bild: "neu/s8__zugewiesen" },
  { id: "s9", zelle: [2, 2], terminal: { von: 1880, bis: 2140 } },
  { id: "s10", zelle: [2, 3], bild: "neu/s10__laedt", danach: { bild: "neu/s10__geladen", ab: 2275 } },
  { id: "s11", zelle: [2, 5], bild: "neu/s11__suche" },
  { id: "s12", zelle: [2, 6], bild: "neu/s12__fehlerseite" },
];

// Kamerahalte: [ankommen, abfahren, Kachel-ID]. Dazwischen gleitet sie mit einem Zoom-Knick.
export const HALTE = [
  [0, 300, "s1"], [360, 600, "s2"], [660, 760, "s3"], [820, 940, "s4"], [1000, 1150, "s5"],
  [1200, 1300, "s5b"], [1350, 1450, "s6"], [1500, 1620, "s7"], [1700, 1800, "s8"],
  [1860, 2160, "s9"], [2220, 2320, "s10"], [2380, 2480, "s11"], [2540, 2620, "s12"],
];
export const ZOOM_AUS = [2620, 2800]; // heraus zur großen 4, dabei ordnen; Halt bis zum Morph
export const MORPH = [2860, 3060];    // Kacheln → Punkte → Glyphe
export const ENDE = [3060, FRAMES];   // Schrift steht, Endtafel

export const TAFELN = [
  [330, 760, "Schreiben, wie es aussieht."],
  [800, 1640, "Alles verbunden."],
  [1840, 2180, "Für Menschen und Maschinen."],
  [2200, 2620, "Schneller. Robuster."],
];

export function kachel(id) { return KACHELN.find((k) => k.id === id); }

export function mitte(k) {
  return [k.zelle[0] * CELL_W + TILE_W / 2, k.zelle[1] * CELL_H + TILE_H / 2];
}

// Unordnung während der Fahrt (fester Seed je Kachel), die im Zoom-Heraus auf 0 geht.
export function versatz(k, i) {
  const r = prng(0x4a11 + i * 97);
  return { dx: (r() * 2 - 1) * 140, dy: (r() * 2 - 1) * 110, rot: (r() * 2 - 1) * 3.2 };
}

// Der Umriss der Kachel-4 in Weltkoordinaten.
export const VIER_BOX = { x: 0, y: 0, w: 3 * CELL_W + TILE_W, h: 6 * CELL_H + TILE_H };

function kameraHalt(id) {
  const [cx, cy] = mitte(kachel(id));
  return { cx, cy, z: Z_KACHEL };
}

// Die Kamera als reine Funktion. `geo.ziel` = Kamera, unter der die Kachel-4 auf der Glyphe „4“
// liegt (beim Laden aus der gesetzten Schrift gemessen).
export function kamera(n, geo) {
  if (n < HALTE[0][1]) {
    // Anfang: aus der Versionsangabe in der Leiste heraus (Weltpunkt der Marke in Kachel s1).
    const k1 = kachel("s1");
    const bx = k1.zelle[0] * CELL_W + geo.marke.x, by = k1.zelle[1] * CELL_H + geo.marke.y;
    const halt = kameraHalt("s1");
    const t = phase(n, 110, 250);
    const zStart = 34, zEnd = halt.z;
    // logarithmisch zoomen wirkt gleichmäßig
    const z = Math.exp(lerp(Math.log(zStart), Math.log(zEnd), t));
    return { cx: lerp(bx, halt.cx, t), cy: lerp(by, halt.cy, t), z };
  }
  for (let i = 0; i < HALTE.length; i++) {
    const [an, ab, id] = HALTE[i];
    if (n >= an && n < ab) return kameraHalt(id);
    const naechster = HALTE[i + 1];
    if (naechster && n >= ab && n < naechster[0]) {
      const a = kameraHalt(id), b = kameraHalt(naechster[2]);
      const t = phase(n, ab, naechster[0]);
      const dip = 1 - 0.38 * Math.sin(Math.PI * t);
      return { cx: lerp(a.cx, b.cx, t), cy: lerp(a.cy, b.cy, t), z: lerp(a.z, b.z, t) * dip };
    }
  }
  // Heraus zur **großen** 4 (Mitte, 88 % der Bildhöhe) — dort ordnen sich die Kacheln; im
  // Morph gleitet die Kamera dann auf die Lage der Glyphe „4“ (`geo.ziel`).
  const letzter = kameraHalt(HALTE[HALTE.length - 1][2]);
  const gross = { cx: VIER_BOX.w / 2, cy: VIER_BOX.h / 2, z: (0.88 * H) / VIER_BOX.h };
  if (n < MORPH[0]) {
    const t = phase(n, ZOOM_AUS[0], ZOOM_AUS[1]);
    const z = Math.exp(lerp(Math.log(letzter.z), Math.log(gross.z), t));
    return { cx: lerp(letzter.cx, gross.cx, t), cy: lerp(letzter.cy, gross.cy, t), z };
  }
  const t = phase(n, MORPH[0], MORPH[0] + 140);
  return { cx: lerp(gross.cx, geo.ziel.cx, t), cy: lerp(gross.cy, geo.ziel.cy, t),
           z: Math.exp(lerp(Math.log(gross.z), Math.log(geo.ziel.z), t)) };
}

export function welt2bild(cam, x, y) {
  return [W / 2 + (x - cam.cx) * cam.z, H / 2 + (y - cam.cy) * cam.z];
}

// Der ganze Zustand eines Bildes — nur Daten.
export function zustand(n, geo) {
  const cam = kamera(n, geo);
  const ordnen = phase(n, ZOOM_AUS[0] + 60, ZOOM_AUS[1] + 20);   // 0 = Unordnung, 1 = Raster
  // Anfang: die Kacheln erst unter 3× Zoom einblenden (die Aufnahme ist 2× — darüber wäre sie
  // weich); bis dahin steht die Vektor-Marke allein auf Schwarz.
  const einblend = n < HALTE[0][1] ? clamp((3 - cam.z) / (3 - 1.8)) : 1;
  const zerfall = phase(n, MORPH[0], MORPH[0] + 70);         // Kacheln blenden in Punkte über
  const flug = phase(n, MORPH[0] + 30, MORPH[1]);            // Punkte fliegen zur Glyphe
  const schrift = phase(n, MORPH[1] - 40, MORPH[1] + 40);    // gesetzte Schrift blendet auf
  const kacheln = KACHELN.map((k, i) => {
    const v = versatz(k, i);
    const f = 1 - ordnen;
    const s = { id: k.id, x: k.zelle[0] * CELL_W + v.dx * f, y: k.zelle[1] * CELL_H + v.dy * f,
                rot: v.rot * f, deckkraft: (1 - zerfall) * einblend, rand: ordnen, bild: k.bild, alt: k.alt || null, streif: 1 };
    if (k.alt) {
      // 0 = ganz alt, 1 = ganz neu; der Streif läuft von links nach rechts.
      s.streif = easeInOut(clamp((n - k.streif[0]) / (k.streif[1] - k.streif[0])));
    }
    if (k.folge) {
      const t = clamp((n - k.folge.von) / (k.folge.bis - k.folge.von));
      s.bild = k.folge.prefix + String(Math.round(t * (k.folge.n - 1))).padStart(3, "0");
    }
    if (k.danach && n >= k.danach.ab) s.bild = k.danach.bild;
    if (k.terminal) s.terminal = clamp((n - k.terminal.von) / (k.terminal.bis - k.terminal.von));
    return s;
  });
  const tafel = TAFELN.map(([a, b, text]) => ({ text, deck: Math.min(phase(n, a, a + 40), 1 - phase(n, b - 40, b)) }))
    .filter((t) => t.deck > 0)[0] || null;
  // Die Marke am Anfang: Vektor, so lange der Zoom groß ist; die Ziffern rollen 3.1.6 → 4.0.0.
  const marke = { deck: 1 - phase(n, 240, 280), roll: phase(n, 40, 110) };
  const ende = phase(n, ENDE[0] + 30, ENDE[0] + 110);
  return { n, cam, kacheln, tafel, marke, zerfall, flug, schrift, ende };
}
