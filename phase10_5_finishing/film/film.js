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
// 16.8 (Sichtung 1: „wie eine Diashow“): die Kachel füllt das Bild nicht mehr — sie steht auf
// einer Seite (≈ 60 % der Breite), leicht im Raum gedreht, und rückt während des Halts heran; die
// andere Seite trägt den Text der Szene.
export const Z_KACHEL = 0.72;
export const SEITE_PX = 300; // Abstand der Kachelmitte von der Bildmitte; −1 = Kachel links

// Die Zeitleiste ist **relativ**: je Kachel ein Halt und die Fahrt danach (in Bildern); alle
// Ereignisse einer Kachel (Streif, Bildfolge, Wechsel, Terminal) zählen ab ihrem Halt. Wer eine
// Dauer ändert, verschiebt nichts von Hand — `HALTE` und die absoluten Marken folgen.
// Kacheln: Zelle [Spalte, Zeile], Bild (neu), optional alt (Lichtstreif), Bildfolge, Wechsel.
// `text`: Titel + eine Zeile, erscheint mit dem Streif (jede Kachel hat einen — bei den drei alten
// macht er die UI neu, bei den anderen ist er nur Licht). `fokus`: Kachelpunkt, auf den die Kamera
// im Halt heranfährt (Suche: die Treffer, 16.8 (d); gemessen an den Aufnahmen, Anmerkungen 16.8).
const FAHRT = [
  { id: "s1", halt: 130, reise: 45, zelle: [2, 0], bild: "neu/s1__uebersicht", alt: "alt/s1__uebersicht", streif: [20, 85], kippVon: 70,
    text: ["Sharefyx 4.0.0", "Neu, von der Leiste bis zur Karte."] },
  { id: "s2", halt: 150, reise: 45, zelle: [1, 1], folge: { prefix: "neu/s2__t", n: 107, von: 10, bis: 135 },
    text: ["Schreiben, wie es aussieht.", "Markdown formt sich beim Tippen."] },
  { id: "s3", halt: 100, reise: 45, zelle: [0.6, 2], bild: "neu/s3__kaestchen", alt: "alt/s2__fertig", streif: [8, 60],
    text: ["Abhaken im Text.", "Ein Klick speichert — mit Version."] },
  { id: "s4", halt: 110, reise: 45, zelle: [0.2, 3], bild: "neu/s4__rot", danach: { bild: "neu/s4__gross", ab: 55 },
    text: ["Farbe und Größe.", "Direkt im Text, mit einer klaren Knopfleiste."] },
  { id: "s5", halt: 115, reise: 40, zelle: [0, 4], bild: "neu/s5__ganz", alt: "alt/s5__ganz", streif: [10, 75], karte: true,
    text: ["Alles verbunden.", "Die Karte als ein Gebilde — jeder Space ein Bereich."] },
  { id: "s5b", halt: 120, reise: 40, zelle: [1, 4], bild: "neu/s5__suche", karte: true, fokus: { x: 1106, y: 400, zoom: 1.8 },
    text: ["Suchen in der Karte.", "Die Treffer leuchten auf."] },
  { id: "s6", halt: 95, reise: 40, zelle: [2, 4], bild: "neu/s6__in_arbeit", karte: true,
    text: ["Was gerade läuft.", "Aufgaben „In Arbeit“ hervorgehoben."] },
  { id: "s7", halt: 105, reise: 55, zelle: [3, 4], bild: "neu/s7__dialog", danach: { bild: "neu/s7__danach", ab: 55 },
    text: ["Ordner umbenennen.", "Die Notizen ziehen mit."] },
  { id: "s8", halt: 95, reise: 45, zelle: [2, 1], bild: "neu/s8__zugewiesen",
    text: ["Filter „Zugewiesen“.", "Sehen, wer woran arbeitet."] },
  { id: "s9", halt: 200, reise: 45, zelle: [2, 2], terminal: { von: 10, bis: 185 },
    text: ["Für Menschen und Maschinen.", "Drei Notizen, ein Aufruf — jede mit eigener Version."] },
  { id: "s10", halt: 95, reise: 45, zelle: [2, 3], bild: "neu/s10__laedt", danach: { bild: "neu/s10__geladen", ab: 45 },
    text: ["Schneller.", "Die Übersicht in einem Durchgang."] },
  { id: "s11", halt: 120, reise: 45, zelle: [2, 5], bild: "neu/s11__suche", fokus: { x: 483, y: 200, zoom: 1.8 },
    text: ["Robuster.", "Eine kaputte Notiz legt die Suche nicht lahm."] },
  { id: "s12", halt: 95, reise: 0, zelle: [2, 6], bild: "neu/s12__fehlerseite",
    text: ["Bis ins Detail.", "Eigene Fehlerseite, der Tab-Titel folgt der Ansicht."] },
];// Der Auftakt (16.6, Sichtung 1: „wie ein Urknall“): ein Lichtpunkt auf Schwarz, der Knall, die
// Punkte fliegen auseinander und sammeln sich zur **ganzen** Marke (Zeichen, Name, Version) in der
// Bildmitte — dieselbe Punktsprache wie das Finale. Die Ziffern rollen 3.1.6 → 4.0.0, dann landet
// die Marke in der Leiste der ersten Kachel (alte UI); der Streif macht sie neu.
export const AUFTAKT = {
  funke: [10, 40],     // der Punkt glimmt auf
  knall: 40,           // Blitz, Punkte fliegen auseinander
  flug: [40, 100],     // Ausdehnung (ease-out)
  sammeln: [86, 160],  // zu den Zielpunkten der Marke
  marke: [146, 176],   // die gesetzte Marke blendet auf, die Punkte ab
  rolle: [182, 220],   // 3.1.6 → 4.0.0
  landen: [230, 290],  // die Marke fliegt in die Leiste von s1, die Kacheln blenden auf
};
export const MARKE_GROSS = 7; // Maßstab der Marke in der Bildmitte (Name + Version ≈ 900 px breit)
const START = AUFTAKT.landen[1]; // Bild, an dem der erste Halt beginnt

// Kamerahalte: [ankommen, abfahren, Kachel-ID]. Dazwischen gleitet sie mit einem Zoom-Knick.
export const HALTE = [];
export const KACHELN = [];
{
  let an = START;
  FAHRT.forEach((f, i) => {
    const { halt, reise, ...k } = f;
    k.seite = i % 2 === 0 ? -1 : 1;
    k.streif = (k.streif || [8, 55]).map((x) => an + x);
    k.kipp = [an + (k.kippVon ?? -40), an + halt];
    delete k.kippVon;
    if (k.folge) k.folge = { ...k.folge, von: an + k.folge.von, bis: an + k.folge.bis };
    if (k.danach) k.danach = { ...k.danach, ab: an + k.danach.ab };
    if (k.terminal) k.terminal = { von: an + k.terminal.von, bis: an + k.terminal.bis };
    HALTE.push([an, an + halt, k.id]);
    KACHELN.push(k);
    an += halt + reise;
  });
}
const FAHRT_ENDE = HALTE[HALTE.length - 1][1];
export const ZOOM_AUS = [FAHRT_ENDE, FAHRT_ENDE + 140]; // heraus zur großen 4, dabei ordnen
export const MORPH = [ZOOM_AUS[1] + 40, ZOOM_AUS[1] + 220]; // Kacheln → Punkte → Glyphe
export const FRAMES = MORPH[1] + 190;
export const ENDE = [MORPH[1], FRAMES];   // Schrift steht, Endtafel

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

// Halt: die Kachel (mit ihrem Versatz) steht auf ihrer Seite, mittig in der Höhe.
function kameraHalt(id) {
  const i = KACHELN.findIndex((k) => k.id === id), k = KACHELN[i], v = versatz(k, i), [mx, my] = mitte(k);
  return { cx: mx + v.dx - (k.seite * SEITE_PX) / Z_KACHEL, cy: my + v.dy, z: Z_KACHEL };
}

// Heranfahren auf den Fokus (Suche): der Fokuspunkt wandert vom Bild seiner Kachel auf den Ankerpunkt
// der Seite, der Zoom steigt auf `fokus.zoom` (Schärfe: die Aufnahme ist 2× — z ≤ 2 auf dem Bild).
export function fokusFortschritt(n, k) {
  const [an, ab] = HALTE.find((h) => h[2] === k.id);
  return k.fokus ? phase(n, an + 30, ab + 10) : 0;
}
function kameraFokus(n, id, cam) {
  const i = KACHELN.findIndex((k) => k.id === id), k = KACHELN[i];
  const e = fokusFortschritt(n, k);
  if (!e) return cam;
  const v = versatz(k, i);
  const s = { x: k.zelle[0] * CELL_W + v.dx, y: k.zelle[1] * CELL_H + v.dy, rot: v.rot };
  const [px, py] = kachelPunkt(s, k.fokus.x, k.fokus.y), [p0x, p0y] = welt2bild(cam, px, py);
  const ax = W / 2 + k.seite * SEITE_PX, ay = H / 2;
  const z = cam.z * lerp(1, k.fokus.zoom, e);
  return { z, cx: px - (lerp(p0x, ax, e) - W / 2) / z, cy: py - (lerp(p0y, ay, e) - H / 2) / z };
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
    if (n >= an && n < ab) return kameraFokus(n, id, kameraHalt(id));
    const naechster = HALTE[i + 1];
    if (naechster && n >= ab && n < naechster[0]) {
      const a = kameraFokus(ab, id, kameraHalt(id)), b = kameraHalt(naechster[2]);
      const t = phase(n, ab, naechster[0]);
      const dip = 1 - 0.38 * Math.sin(Math.PI * t);
      return { cx: lerp(a.cx, b.cx, t), cy: lerp(a.cy, b.cy, t), z: lerp(a.z, b.z, t) * dip };
    }
  }
  // Heraus zur **großen** 4 (Mitte, 88 % der Bildhöhe) — dort ordnen sich die Kacheln; im
  // Morph gleitet die Kamera dann auf die Lage der Glyphe „4“ (`geo.ziel`).
  const letzter = kameraFokus(ZOOM_AUS[0], HALTE[HALTE.length - 1][2], kameraHalt(HALTE[HALTE.length - 1][2]));
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

// Das Raster im Hintergrund (16.7, Sichtung 1: „Schwarz wirkt unfertig“): eine Ebene **hinter**
// der Welt — sie zieht mit der halben Kamera (Parallaxe). Damit es beim Herauszoomen nicht zu Brei
// wird, hält es die Dichte: der Abstand auf dem Bild bleibt in [80, 160) px; die feinen Linien
// blenden mit `fein` ein, an jeder Stufe ist der Übergang stetig (vorher: alle 160 px voll, danach:
// alle 160 px voll, feine bei 0).
export const RASTER_PARALLAXE = 0.5, RASTER_WELT = 200, RASTER_MIN = 80;
export function raster(cam) {
  const roh = RASTER_WELT * RASTER_PARALLAXE * cam.z, L = Math.log2(roh / RASTER_MIN), k = Math.floor(L);
  const abstand = roh / 2 ** k;
  // Bildposition des Weltursprungs der Ebene — Linie m liegt bei ursprung + m * abstand.
  const zg = RASTER_PARALLAXE * cam.z;
  return { abstand, fein: L - k, ux: W / 2 - cam.cx * zg, uy: H / 2 - cam.cy * zg };
}

// Der Text einer Szene (16.8 (b)): Titel und Zeile Wort für Wort, gekoppelt an den Streif — jedes
// Wort erscheint, wenn der Streif „bei ihm“ ist (Titel zuerst, die Zeile folgt), und steigt dabei
// 14 px auf. Er geht mit der Abfahrt. Nur Daten: Wörter, Deckkraft, Versatz, Seite.
export function textZustand(n) {
  for (let i = 0; i < KACHELN.length; i++) {
    const k = KACHELN[i], [an, ab] = HALTE[i];
    if (!k.text || n < k.streif[0] || n >= ab + 30) continue;
    const dauer = k.streif[1] - k.streif[0], aus = phase(n, ab - 5, ab + 25);
    const woerter = [];
    k.text.forEach((zeile, z) => zeile.split(" ").forEach((wort) => woerter.push({ wort, zeile: z })));
    woerter.forEach((w, j) => {
      const ein = clamp((n - k.streif[0] - (j / woerter.length) * dauer * 0.9 - (w.zeile ? 6 : 0)) / 18);
      w.deck = easeInOut(ein) * (1 - aus);
      w.dy = (1 - easeInOut(ein)) * 14 - aus * 10;
      w.glanz = Math.sin(Math.PI * ein) * (1 - aus); // ein kurzes Aufleuchten beim Erscheinen
    });
    return { id: k.id, seite: -k.seite, woerter, schleier: fokusFortschritt(n, k) * (1 - aus) };
  }
  return null;
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
  // Wer gerade spielt: um ihren Halt herum ist eine Kachel „aktiv“; die übrigen treten auf 35 %
  // zurück — der Blick bleibt bei der Szene, und die Nachbarn liegen nicht unter dem Text (16.8,
  // Vorschau: sie ragten in die Textseite). In der Fahrt sind alle wieder hell.
  const aktiv = HALTE.map(([an, ab]) => phase(n, an - 30, an + 10) * (1 - phase(n, ab - 10, ab + 30)));
  const kacheln = KACHELN.map((k, i) => {
    const v = versatz(k, i);
    const andere = Math.max(0, ...aktiv.filter((_, j) => j !== i));
    const zurueck = 1 - 0.65 * andere * (1 - aktiv[i]);
    const f = 1 - ordnen;
    // Im Raum: um den Halt herum dreht sich die Kachel leicht zur Textseite und rückt heran; die
    // Drehung driftet während des Halts zurück (die Aufnahme „lebt“). Außerhalb flach.
    const w = phase(n, k.kipp[0], k.kipp[0] + 50) * (1 - phase(n, k.kipp[1] - 10, k.kipp[1] + 40));
    const t = clamp((n - k.kipp[0]) / (k.kipp[1] - k.kipp[0]));
    const ruhig = 1 - 0.7 * fokusFortschritt(n, k); // beim Heranfahren auf den Fokus wird sie flacher
    const kipp = { ry: -k.seite * lerp(13, 6, t) * w * ruhig, rx: lerp(5, 2, t) * w * ruhig, push: 1 + 0.06 * t * w };
    const s = { id: k.id, x: k.zelle[0] * CELL_W + v.dx * f, y: k.zelle[1] * CELL_H + v.dy * f,
                rot: v.rot * f * (1 - 0.8 * w), deckkraft: (1 - zerfall) * einblend * zurueck, rand: ordnen, bild: k.bild, alt: k.alt || null,
                kipp, streif: easeInOut(clamp((n - k.streif[0]) / (k.streif[1] - k.streif[0]))) };
    if (k.folge) {
      const t = clamp((n - k.folge.von) / (k.folge.bis - k.folge.von));
      s.bild = k.folge.prefix + String(Math.round(t * (k.folge.n - 1))).padStart(3, "0");
    }
    if (k.danach && n >= k.danach.ab) s.bild = k.danach.bild;
    if (k.terminal) s.terminal = clamp((n - k.terminal.von) / (k.terminal.bis - k.terminal.von));
    return s;
  });
  const text = textZustand(n);
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
  // Das Raster erscheint mit dem Knall (eine Welle läuft von der Mitte nach außen) und tritt im
  // Morph zurück, damit die Punkte der 4.0.0 sauber stehen.
  const nachKnall = n - A.knall;
  const rasterZ = { ...raster(cam),
    deck: phase(n, A.knall + 10, A.knall + 90) * (1 - 0.75 * phase(n, MORPH[0], MORPH[0] + 60)),
    welle: nachKnall >= 0 && nachKnall < 120 ? { r: nachKnall * 26, deck: 1 - nachKnall / 120 } : null };
  return { raster: rasterZ, n, cam, kacheln, text, auftakt, marke, zerfall, flug, schrift, ende };
}
