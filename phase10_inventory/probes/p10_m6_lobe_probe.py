#!/usr/bin/env python3
"""M6, zweiter Teil (P10-Plan §4, Register KA-1): was kostet die Lappen-Berechnung des
Stils C2 „Nervenbahnen"?

Der Basisteil (Settle-Ticks, Settle-Zeit, Zeichenzeit je Frame) läuft über den vorhandenen
`phase8_ui_graph/scripts/p8_22_smoke.py` gegen dieselbe 200-Knoten-Wegwerf-Instanz — sein
Ergebnis liegt als Text daneben (`messung/M6_p8_22_200knoten.txt`). Dieser Probe beantwortet
die zweite M6-Frage: der geplante Karten-Umbau (KA-1, Stil C2) erzeugt die „Lappen" im Browser
aus den Knotenpositionen — **Raster × nächster Knoten, Erosion als Furche, Konturverfahren**.
Die Größe „M–L" von KA-1 hängt daran, ob diese Pipeline einmal nach dem Einschwingen reicht
(Positionen ändern sich nicht mehr) oder je Frame laufen muss (Simulation bewegt sich noch).

Gemessen wird im echten Chromium gegen den eingeschwungenen 200-Knoten-Graphen, in-page,
ohne den Produktionscode anzufassen:
1. Knotenmittelpunkte aus den Canvas-Pixeln (dasselbe Clusterverfahren wie `p8_22_smoke.py ::
   NODE_CENTERS` — die Simulation exportiert ihren Zustand bewusst nicht).
2. Pipeline je Zellgröße (6/8/12 px): Zuordnung (je Rasterzelle der nächste Knoten, O(Zellen ×
   Knoten)), Erosion (Zelle fällt, wenn ein 4-Nachbar fremd ist — die Furche), Kontur (Zellen
   mit fremdem 8-Nachbar nach der Erosion).
3. Einmal nach dem Einschwingen UND 30 Wiederholungen → Median je Stufe; davon hängt die
   Lesart „einmal beim Settle" (billig) oder „je Frame" (Budget 16,7 ms) ab.

Ausgabe: JSON auf stdout (Hard Rule 7) + `p10_m6_lobe.json` neben diesem Skript.
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
import urllib.parse
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO_ROOT = Path(__file__).resolve().parents[2]
BASE = "http://127.0.0.1:18772"
CREDS_FILE = Path("/tmp/opencode/sharefyx-wegwerf-200knoten/credentials.json")
SHOT_DIR = REPO_ROOT / "docs" / "screenshots"
OUT_JSON = REPO_ROOT / "phase10_inventory" / "probes" / "p10_m6_lobe.json"

CELL_SIZES = (6, 8, 12)
REPEATS = 30

# Dieselbe Erkennung wie p8_22_smoke :: CANVAS_HASH — Ruhe = Hash zweimal hintereinander
# gleich, Canvas bebildert.
CANVAS_HASH = """
() => {
  const c = document.getElementById('overview-graph-canvas');
  if (!c) return null;
  const d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data;
  let h = 0x811c9dc5, painted = 0;
  for (let i = 0; i < d.length; i += 64) {
    h ^= d[i] + d[i + 1] + d[i + 2] + d[i + 3];
    h = (h * 16777619) >>> 0;
    if (d[i + 3] !== 0) painted += 1;
  }
  return { hash: h, painted: painted, width: c.width, height: c.height };
}
"""

NODE_CENTERS = """
() => {
  const c = document.getElementById('overview-graph-canvas');
  const rect = c.getBoundingClientRect();
  const sx = rect.width / c.width, sy = rect.height / c.height;
  const d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data;
  const want = [[74,147,240],[46,184,166],[139,147,161]];
  const hit = [];
  for (let y = 0; y < c.height; y += 2) {
    for (let x = 0; x < c.width; x += 2) {
      const i = (y * c.width + x) * 4;
      if (d[i + 3] < 250) continue;
      for (const w of want) {
        if (d[i] === w[0] && d[i + 1] === w[1] && d[i + 2] === w[2]) { hit.push([x, y]); break; }
      }
    }
  }
  const clusters = [];
  for (const [x, y] of hit) {
    let found = null;
    for (const cl of clusters) {
      if (Math.abs(cl.x / cl.n - x) < 14 && Math.abs(cl.y / cl.n - x * 0 - y) < 14) { found = cl; break; }
    }
    if (found) { found.x += x; found.y += y; found.n += 1; }
    else clusters.push({ x: x, y: y, n: 1 });
  }
  return {
    rect: { w: rect.width, h: rect.height, deviceW: c.width, deviceH: c.height },
    centers: clusters.filter(cl => cl.n >= 3)
      .map(cl => ({ x: (cl.x / cl.n) * sx, y: (cl.y / cl.n) * sy })),
  };
}
"""

# Die Pipeline selbst: reines JS, kein Produktionscode-Berührung. Bewusst einfache Bäume
# weggelassen — der Prototyp soll die BRÜTTKosten der ersten Fassung messen (Plan: „Raster ×
# nächster Knoten, Erosion, Kontur"), nicht eine optimierte Endfassung schönrechnen.
LOBE_PIPELINE = """
(args) => {
  const { centers, width, height, cell, repeats } = args;
  const cols = Math.ceil(width / cell), rows = Math.ceil(height / cell);
  const assign = new Int32Array(cols * rows);

  function pipelineOnce() {
    const t0 = performance.now();
    // 1) Zuordnung: nächste Knoten je Zelle.
    for (let gy = 0; gy < rows; gy++) {
      const cy = gy * cell + cell / 2;
      for (let gx = 0; gx < cols; gx++) {
        const cx = gx * cell + cell / 2;
        let best = -1, bestD = Infinity;
        for (let k = 0; k < centers.length; k++) {
          const dx = centers[k].x - cx, dy = centers[k].y - cy;
          const d = dx * dx + dy * dy;
          if (d < bestD) { bestD = d; best = k; }
        }
        assign[gy * cols + gx] = best;
      }
    }
    const t1 = performance.now();
    // 2) Erosion: eine Zelle fällt in die Furche, wenn ein 4-Nachbar einem fremden Lappen
    //    gehört (einfache erste Fassung des „Furchen"-Schritts, Stil C2).
    const eroded = new Uint8Array(cols * rows);
    for (let gy = 0; gy < rows; gy++) {
      for (let gx = 0; gx < cols; gx++) {
        const i = gy * cols + gx;
        const mine = assign[i];
        if ((gx > 0 && assign[i - 1] !== mine)
            || (gx < cols - 1 && assign[i + 1] !== mine)
            || (gy > 0 && assign[i - cols] !== mine)
            || (gy < rows - 1 && assign[i + cols] !== mine)) {
          eroded[i] = 1;
        }
      }
    }
    const t2 = performance.now();
    // 3) Kontur: erodierte Zellen mit mindestens einem 8-Nachbar, der NICHT erodiert ist,
    //    sind Konturkandidaten (Zeichensatz für die „Membran"-Linie).
    let contour = 0;
    for (let gy = 0; gy < rows; gy++) {
      for (let gx = 0; gx < cols; gx++) {
        const i = gy * cols + gx;
        if (!eroded[i]) continue;
        const n = (gx > 0 && !eroded[i - 1]) || (gx < cols - 1 && !eroded[i + 1])
          || (gy > 0 && !eroded[i - cols]) || (gy < rows - 1 && !eroded[i + cols]);
        if (n) contour += 1;
      }
    }
    const t3 = performance.now();
    return { assign_ms: t1 - t0, erode_ms: t2 - t1, contour_ms: t3 - t2,
             total_ms: t3 - t0, contour_cells: contour };
  }

  pipelineOnce();  // Aufwärmlauf (JIT), verworfen
  const runs = [];
  for (let r = 0; r < repeats; r++) runs.push(pipelineOnce());
  const med = (key) => statistics_unused_placeholder;
  return { cols, rows, cells: cols * rows, runs };
}
"""


def login(page, creds) -> None:
    import base64, hashlib, hmac, struct
    qs = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(creds["otpauth_uri"]).query))
    key = __import__("base64").b32decode(qs["secret"] + "=" * (-len(qs["secret"]) % 8))
    def totp() -> str:
        counter = int(time.time() // 30)
        digest = hmac.new(key, struct.pack(">q", counter), hashlib.sha1).digest()
        off = digest[-1] & 0x0F
        return f"{(struct.unpack('>I', digest[off:off + 4])[0] & 0x7FFFFFFF) % 1000000:06d}"
    last = totp()
    page.goto(f"{BASE}/ui/login", wait_until="domcontentloaded")
    page.fill('input[name="space"]', creds["space"])
    page.fill('input[name="password"]', creds["password"])
    page.fill('input[name="totp"]', last)
    page.click('button[type="submit"]')
    page.wait_for_url(f"{BASE}/ui/", timeout=15000)
    page.wait_for_selector(".overview__graph canvas", state="visible", timeout=15000)


def wait_settle(page) -> dict:
    last, stable_at, elapsed = None, None, 0
    while elapsed <= 12000:
        snap = page.evaluate(CANVAS_HASH)
        assert snap is not None, "Canvas fehlt"
        if snap["painted"] > 0 and snap["hash"] == last:
            stable_at = stable_at or snap
            if elapsed - (stable_at.get("_t") or 0) >= 100:
                return snap
            stable_at.setdefault("_t", elapsed)
        else:
            stable_at = None
        last = snap["hash"]
        page.wait_for_timeout(100)
        elapsed += 100
    raise RuntimeError("Graph kam in 12 s nicht zur Ruhe")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.parse_args(argv)
    creds = json.loads(CREDS_FILE.read_text())

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_context(viewport={"width": 1280, "height": 900}).new_page()
        login(page, creds)
        settled = wait_settle(page)
        info = page.evaluate(NODE_CENTERS)
        # Der Force-Layout überlappt Knoten — p8_22_smoke sah an diesem Datensatz dieselben
        # 66 sichtbaren Cluster. Gemessen wird deshalb doppelt: die REAL sichtbaren Cluster
        # und eine synthetische Obergrenze mit 200 verteilten Punkten (deterministisch,
        # Raster + Jitter), damit die KA-1-Größe auch für den Fall „alle 200 trennen sich"
        # belastbar ist.
        detected = info["centers"]
        assert len(detected) >= 50, (
            f"nur {len(detected)} Knotenmittelpunkte — Clustering versagt"
        )
        page.screenshot(path=str(SHOT_DIR / "p10_m6_lobe_basis.png"))

        import random
        rng = random.Random(20261018)
        w, h = info["rect"]["w"], info["rect"]["h"]
        synthetic = [
            {"x": 20 + (i % 20) * (w - 40) / 19 + rng.uniform(-14, 14),
             "y": 20 + (i // 20) * (h - 40) / 9 + rng.uniform(-14, 14)}
            for i in range(200)
        ]

        results = []
        for label, centers in (("real_detected", detected), ("synthetic_200", synthetic)):
            for cell in CELL_SIZES:
                out = page.evaluate(LOBE_PIPELINE, {
                    "centers": centers, "width": w,
                    "height": h, "cell": cell, "repeats": REPEATS,
                })
                runs = out.pop("runs")
                for key in ("assign_ms", "erode_ms", "contour_ms", "total_ms"):
                    values = [r[key] for r in runs]
                    out[key + "_median"] = round(statistics.median(values), 2)
                    out[key + "_max"] = round(max(values), 1)
                out["cell_px"] = cell
                out["variant"] = label
                out["nodes"] = len(centers)
                out["frame_budget_60fps"] = 16.7
                out["per_frame_feasible"] = out["total_ms_median"] < 16.7
                results.append(out)
        browser.close()

    result = {
        "probe": "p10_m6_lobe",
        "nodes_detected": len(detected),
        "canvas": info["rect"],
        "settled": {"painted": settled["painted"]},
        "repeats": REPEATS,
        "variants": results,
        "lesart": {
            "einmal_nach_settle": "Pipeline einmal nach dem Einschwingen — Kosten egal, "
                                  "Positionen ändern sich danach nicht (P9 Step E trägt "
                                  "Positionen über Reload)",
            "je_frame": "nur relevant, während die Simulation läuft; entscheidet die "
                        "total_ms_median gegen das 60-fps-Budget (16,7 ms)",
        },
    }
    print(json.dumps(result, ensure_ascii=False, indent=1))
    OUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
