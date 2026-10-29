"""Die Lappen-Kontur bleibt **geschlossen**, auch wenn die Zellgröße **krumm** wird (Plan
`docs/concepts/phase10_5_block14_7_plan.md`, Fund 14.7.2, 2026-10-29).

**Der Fund.** `computeLobes()` deckelt das Raster bei `LOBE_MAX_CELLS` je Achse; eine breitere
Karte bekommt dann eine Zellgröße wie 8,37 px. `traceContour()` rechnete die Zellecken in
**Weltkoordinaten** (`x1 = x0 + cell`), `chainEdges()` verkettet über die Endpunkte als
Text-Schlüssel — und `x0 + cell` ist nicht bitgleich zu `minX + (gx + 1) * cell`. Die Kontur
zerfiel in Bruchstücke mit Sehnen, der Körper verschwand fast ganz (im Raster 14.7.2 an
`spirale_s1.25` und `hexf_s1.25` gesehen; isoliert: eine Kreisscheibe → **4** Schleifen bei
8,37 px). Behoben durch Verketten in **ganzzahligen** Gitterkoordinaten.

**Gegenprobe:** derselbe Lauf an einer Kopie mit der alten Rechnung muss **zerfallen**.
"""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

GRAPH_JS = Path(__file__).resolve().parents[2] / "phase5_ui" / "webui" / "static" / "js" / "graph.js"
needs_node = pytest.mark.skipif(shutil.which("node") is None, reason="node fehlt")

ALT = [
    ("    var x0 = gx;\n    var y0 = gy;\n    var x1 = gx + 1;\n    var y1 = gy + 1;\n",
     "    var x0 = minX + gx * cell;\n    var y0 = minY + gy * cell;\n"
     "    var x1 = x0 + cell;\n    var y1 = y0 + cell;\n"),
    ("[minX + p[0] * cell, minY + p[1] * cell]", "[p[0], p[1]]"),
]

LAUF = r"""
const src = require("fs").readFileSync(0, "utf8");
function grab(n) {
  const i = src.indexOf("function " + n + "(");
  if (i < 0) throw new Error("fehlt: " + n);
  let d = 0;
  for (let k = src.indexOf("{", i); k < src.length; k++) {
    if (src[k] === "{") d++;
    else if (src[k] === "}" && --d === 0) return src.slice(i, k + 1);
  }
}
const passes = Number(/const LOBE_SMOOTH_PASSES = (\d+)/.exec(src)[1]);
const trace = new Function("const LOBE_SMOOTH_PASSES = " + passes + ";\n" +
  ["traceContour", "chainEdges", "smoothLoop", "simplifyLoop"].map(grab).join("\n") +
  "; return traceContour;")();
const out = {};
for (const cell of [8, 8.37, 9.123456]) {
  const R = 10, cols = 2 * R, m = {}, min = -123.456;
  for (let gy = 0; gy < cols; gy++) for (let gx = 0; gx < cols; gx++) {
    const x = gx - R + 0.5, y = gy - R + 0.5;
    if (x * x + y * y <= R * R) m[gy * cols + gx] = true;
  }
  out[cell] = (trace(m, cols, cols, cell, min, min) || []).length;
}
console.log(JSON.stringify(out));
"""


def _schleifen(quelle: str) -> dict:
    proc = subprocess.run(["node", "-e", LAUF], input=quelle, capture_output=True, text=True,
                          check=True, timeout=60)
    return json.loads(proc.stdout)


@needs_node
def test_a_disc_stays_one_loop_at_any_cell_size():
    r = _schleifen(GRAPH_JS.read_text(encoding="utf-8"))
    assert r == {"8": 1, "8.37": 1, "9.123456": 1}, f"die Kontur zerfaellt: {r}"


@needs_node
def test_gegenprobe_the_world_coordinate_chaining_breaks():
    quelle = GRAPH_JS.read_text(encoding="utf-8")
    for neu, alt in ALT:
        assert neu in quelle, f"Anker fehlt: {neu[:40]!r}"
        quelle = quelle.replace(neu, alt)
    r = _schleifen(quelle)
    assert r["8.37"] > 1 and r["9.123456"] > 1, f"die alte Rechnung haette zerfallen muessen: {r}"
