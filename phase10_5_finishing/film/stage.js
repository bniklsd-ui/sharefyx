// P10.5 Block 16 — Bühne des Launch-Films. Jedes Bild ist eine reine Funktion seiner Nummer:
// `renderFrame(n)` setzt Kamera, Kacheln, Tafeln und Körnung **nur** aus `n` — keine
// CSS-Transitions, kein requestAnimationFrame, keine Uhr, kein Netz (Plan §3.1). Die echte UI
// läuft hier nicht; sie kommt als vorher aufgenommene Bilder (16.1).

export const W = 1920;
export const H = 1080;

export const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
export const lerp = (a, b, t) => a + (b - a) * t;
export const easeInOut = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
// Fortschritt eines Abschnitts [f0, f1] bei Bild n, geglättet.
export const phase = (n, f0, f1) => easeInOut(clamp((n - f0) / (f1 - f0)));

// Deterministischer PRNG (mulberry32) — gleicher Seed, gleiche Folge, in jedem Lauf.
export function prng(seed) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

// Kamera: Weltpunkt (cx, cy) in die Bildmitte, Zoom z.
export function cameraTransform(cx, cy, z) {
  return `translate(${W / 2}px, ${H / 2}px) scale(${z}) translate(${-cx}px, ${-cy}px)`;
}

// Körnung gegen Banding auf dunklen Flächen (8 Bit): ±amp/255, Seed = Bildnummer.
export function drawGrain(canvas, n, amp = 3) {
  const ctx = canvas.getContext("2d");
  const img = ctx.createImageData(canvas.width, canvas.height);
  const rnd = prng(0x5fa1 ^ n);
  for (let i = 0; i < img.data.length; i += 4) {
    const v = 128 + Math.round((rnd() * 2 - 1) * amp);
    img.data[i] = img.data[i + 1] = img.data[i + 2] = v;
    img.data[i + 3] = 255;
  }
  ctx.putImageData(img, 0, 0);
}
