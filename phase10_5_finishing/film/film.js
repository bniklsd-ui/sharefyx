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
export const TILE_W = 1600, TILE_H = 1000, CELL_W = 1800, CELL_H = 1200;
export const Z_KACHEL = 0.85; // eine Kachel füllt das Bild, unten bleibt Platz für die Tafel

// Die Zeitleiste ist **relativ**: je Kachel ein Halt und die Fahrt danach (in Bildern); alle
// Ereignisse einer Kachel (Streif, Bildfolge, Wechsel, Terminal) zählen ab ihrem Halt. Wer eine
// Dauer ändert, verschiebt nichts von Hand — `HALTE` und die absoluten Marken folgen.
// Kacheln: Zelle [Spalte, Zeile], Bild (neu), optional alt (Lichtstreif), Bildfolge, Wechsel.
const FAHRT = [
  { id: "s1", halt: 110, reise: 60, zelle: [2, 0], bild: "neu/s1__uebersicht", alt: "alt/s1__uebersicht", streif: [20, 90] },
  { id: "s2", halt: 240, reise: 60, zelle: [1, 1], folge: { prefix: "neu/s2__t", n: 107, von: 20, bis: 200 } },
  { id: "s3", halt: 100, reise: 60, zelle: [0.6, 2], bild: "neu/s3__kaestchen", alt: "alt/s2__fertig", streif: [10, 80] },
  { id: "s4", halt: 120, reise: 60, zelle: [0.2, 3], bild: "neu/s4__rot", danach: { bild: "neu/s4__gross", ab: 65 } },
  { id: "s5", halt: 150, reise: 50, zelle: [0, 4], bild: "neu/s5__ganz", alt: "alt/s5__ganz", streif: [20, 110], karte: true },
  { id: "s5b", halt: 100, reise: 50, zelle: [1, 4], bild: "neu/s5__suche", karte: true },
  { id: "s6", halt: 100, reise: 50, zelle: [2, 4], bild: "neu/s6__in_arbeit", karte: true },
  { id: "s7", halt: 120, reise: 80, zelle: [3, 4], bild: "neu/s7__dialog", danach: { bild: "neu/s7__danach", ab: 65 } },
  { id: "s8", halt: 100, reise: 60, zelle: [2, 1], bild: "neu/s8__zugewiesen" },
  { id: "s9", halt: 300, reise: 60, zelle: [2, 2], terminal: { von: 20, bis: 280 } },
  { id: "s10", halt: 100, reise: 60, zelle: [2, 3], bild: "neu/s10__laedt", danach: { bild: "neu/s10__geladen", ab: 55 } },
  { id: "s11", halt: 100, reise: 60, zelle: [2, 5], bild: "neu/s11__suche" },
  { id: "s12", halt: 80, reise: 0, zelle: [2, 6], bild: "neu/s12__fehlerseite" },
];
// Der Auftakt (16.6, Sichtung 1: „wie ein Urknall“): ein Lichtpunkt auf Schwarz, der Knall, die
// Punkte fliegen auseinander und sammeln sich zur **ganzen** Marke (Zeichen, Name, Version) in der
// Bildmitte — dieselbe Punktsprache wie das Finale. Die Ziffern rollen 3.1.6 → 4.0.0, dann landet
// die Marke in der Leiste der ersten Kachel (alte UI); der Streif macht sie neu.
export const AUFTAKT = {
  funke: [10, 46],     // der Punkt glimmt auf
  knall: 46,           // Blitz, Punkte fliegen auseinander
  flug: [46, 112],     // Ausdehnung (ease-out)
  sammeln: [96, 178],  // zu den Zielpunkten der Marke
  marke: [160, 192],   // die gesetzte Marke blendet auf, die Punkte ab
  rolle: [198, 240],   // 3.1.6 → 4.0.0
  landen: [252, 322],  // die Marke fliegt in die Leiste von s1, die Kacheln blenden auf
};
export const MARKE_GROSS = 7; // Maßstab der Marke in der Bildmitte (Name + Version ≈ 900 px breit)
const START = AUFTAKT.landen[1]; // Bild, an dem der erste Halt beginnt

// Kamerahalte: [ankommen, abfahren, Kachel-ID]. Dazwischen gleitet sie mit einem Zoom-Knick.
export const HALTE = [];
export const KACHELN = [];
{
  let an = START;
  for (const f of FAHRT) {
    const { halt, reise, ...k } = f;
    if (k.streif) k.streif = k.streif.map((x) => an + x);
    if (k.folge) k.folge = { ...k.folge, von: an + k.folge.von, bis: an + k.folge.bis };
    if (k.danach) k.danach = { ...k.danach, ab: an + k.danach.ab };
    if (k.terminal) k.terminal = { von: an + k.terminal.von, bis: an + k.terminal.bis };
    HALTE.push([an, an + halt, k.id]);
    KACHELN.push(k);
    an += halt + reise;
  }
}
const FAHRT_ENDE = HALTE[HALTE.length - 1][1];
export const ZOOM_AUS = [FAHRT_ENDE, FAHRT_ENDE + 180]; // heraus zur großen 4, dabei ordnen
export const MORPH = [ZOOM_AUS[1] + 60, ZOOM_AUS[1] + 260]; // Kacheln → Punkte → Glyphe
export const FRAMES = MORPH[1] + 240;
export const ENDE = [MORPH[1], FRAMES];   // Schrift steht, Endtafel

const TD = HALTE[1][0] - 360; // die Tafeln standen absolut; sie folgen dem Halt von s2
export const TAFELN = [
  [330, 760, "Schreiben, wie es aussieht."],
  [800, 1640, "Alles verbunden."],
  [1840, 2180, "Für Menschen und Maschinen."],
  [2200, 2620, "Schneller. Robuster."],
].map(([a, b, t]) => [a + TD, b + TD, t]);

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
  if (n < START) {
    // Auftakt: die Kamera steht schon über s1 und rückt beim Landen leicht heran.
    const halt = kameraHalt("s1");
    return { ...halt, z: halt.z * lerp(0.82, 1, phase(n, AUFTAKT.landen[0], AUFTAKT.landen[1])) };
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

// Weltpunkt eines Punkts (px, py) **in** Kachel k (Kachelkoordinaten), mit Versatz und Drehung um
// die Kachelmitte — so, wie die Bühne die Kachel setzt.
export function kachelPunkt(s, px, py) {
  const r = (s.rot * Math.PI) / 180, ux = px - TILE_W / 2, uy = py - TILE_H / 2;
  return [s.x + TILE_W / 2 + ux * Math.cos(r) - uy * Math.sin(r),
          s.y + TILE_H / 2 + ux * Math.sin(r) + uy * Math.cos(r)];
}

// Lage der Marke auf dem Bild (linke obere Ecke, Maßstab, Drehung). Groß: Tinte mittig. Gelandet:
// genau über der Marke der Leiste in s1 (Kachelpunkt (0, 8), 16.2 gemessen).
export function markePose(n, cam, s1, geo) {
  const gs = MARKE_GROSS, b = geo.markeBox;
  const gross = { x: W / 2 - (b.ix + b.iw / 2) * gs, y: 520 - (b.iy + b.ih / 2) * gs, s: gs, rot: 0 };
  const [wx, wy] = kachelPunkt(s1, 0, 8), [lx, ly] = welt2bild(cam, wx, wy);
  const t = phase(n, AUFTAKT.landen[0], AUFTAKT.landen[1]);
  return { x: lerp(gross.x, lx, t), y: lerp(gross.y, ly, t),
           s: Math.exp(lerp(Math.log(gs), Math.log(cam.z), t)), rot: lerp(0, s1.rot, t) };
}

// Der ganze Zustand eines Bildes — nur Daten.
export function zustand(n, geo) {
  const cam = kamera(n, geo);
  const ordnen = phase(n, ZOOM_AUS[0] + 60, ZOOM_AUS[1] + 20);   // 0 = Unordnung, 1 = Raster
  // Auftakt: die Kacheln blenden erst auf, wenn die Marke zur Leiste fliegt.
  const einblend = phase(n, AUFTAKT.landen[0], AUFTAKT.landen[0] + 50);
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
  // Der Auftakt: Funke, Knall, Punkte (Ausdehnung, Sammeln), die gesetzte Marke, die Ziffernrolle.
  // Gelandet bleibt die Marke (mit dem Hintergrund der Leiste) über der alten Aufnahme, bis der
  // Streif von s1 sie überholt — darunter steht dann dieselbe Marke in der neuen UI.
  const A = AUFTAKT, s1 = kacheln[0];
  const auftakt = {
    funke: n < A.knall ? phase(n, A.funke[0], A.funke[1]) : 0,
    blitz: n >= A.knall ? Math.exp(-(n - A.knall) / 9) : 0,
    flug: clamp((n - A.flug[0]) / (A.flug[1] - A.flug[0])),
    sammeln: phase(n, A.sammeln[0], A.sammeln[1]),
    punkte: n >= A.knall ? 1 - phase(n, A.marke[0], A.marke[1]) : 0,
  };
  const marke = {
    deck: phase(n, A.marke[0], A.marke[1]) * (1 - clamp(s1.streif / 0.12)),
    roll: phase(n, A.rolle[0], A.rolle[1]),
    hg: phase(n, A.landen[0] + 30, A.landen[1]),
    pose: markePose(n, cam, s1, geo),
  };
  const ende = phase(n, ENDE[0] + 30, ENDE[0] + 110);
  return { n, cam, kacheln, tafel, auftakt, marke, zerfall, flug, schrift, ende };
}
