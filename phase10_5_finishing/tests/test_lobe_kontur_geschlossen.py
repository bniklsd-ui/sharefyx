"""Die Lappen-Kontur ist **geschlossen**, auch am Rasterrand (2026-10-28, Sichtung der Bilder 14.5).

**Der Fund.** Das Lappen-Raster beginnt genau bei `Knoten − LOBE_REACH` — die Zellen des
äußersten Knotens liegen also **am Rasterrand**. `traceContour()` liess dort die Randkante
**weg** (`gx > 0`-Wächter statt „Rand ist draussen"): die Kontur blieb offen, `chainEdges()`
machte daraus Bruchstücke, und jedes wurde beim Zeichnen mit einer **Sehne** geschlossen.
Sichtbar in `p105_b14_karte_01_ganz.png` (Stand `f419835`) als schräge Linie und Naht am
linken Lappen (gamma). Kein Wächter merkte es: die C2-Probe zählt Konturen je Space, nicht ob
eine Kontur **eine** geschlossene Linie ist.

**Was gemessen wird:** die **echten** Funktionen `traceContour`/`chainEdges`/`simplifyLoop` aus
`graph.js` (per Quelltext herausgeschnitten, in Node ausgeführt — kein Haken im Produktcode),
an **einem** Knoten mit genau dem Raster von `computeLobes()`. Erwartet: **eine** Kontur, die
**symmetrisch** ±`LOBE_REACH` reicht. **Gegenprobe:** derselbe Lauf an einer Kopie mit dem
alten Wächter muss rot werden (drei Bruchstücke, rechts nur 32 px).
"""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
GRAPH_JS = REPO_ROOT / "phase5_ui" / "webui" / "static" / "js" / "graph.js"

needs_node = pytest.mark.skipif(shutil.which("node") is None, reason="node fehlt (P5-T: kein Build)")

#: Ein Knoten bei (0, 0), das Raster wie in `computeLobes()`: Beginn bei −REACH, Zelle 8 px.
_HARNESS = r"""
const src = require("fs").readFileSync(0, "utf8");
function grab(name) {
  const i = src.indexOf("function " + name + "(");
  if (i < 0) throw new Error("fehlt: " + name);
  let depth = 0;
  for (let k = src.indexOf("{", i); k < src.length; k++) {
    if (src[k] === "{") depth++;
    else if (src[k] === "}" && --depth === 0) return src.slice(i, k + 1);
  }
}
const reach = Number(/const LOBE_REACH = (\d+)/.exec(src)[1]);
const cell = Number(/const LOBE_CELL_PX = (\d+)/.exec(src)[1]);
// [2026-10-29, Plan 14.7.1] `chainEdges()` glaettet vor dem Vereinfachen (`smoothLoop()` mit
// `LOBE_SMOOTH_PASSES`) — beides kommt **mit** aus dem echten Quelltext, gemessen wird also
// mit dem eingestellten Glaettungswert.
const passes = Number(/const LOBE_SMOOTH_PASSES = (\d+)/.exec(src)[1]);
const trace = new Function(
  "const LOBE_SMOOTH_PASSES = " + passes + ";\n" +
  ["traceContour", "chainEdges", "smoothLoop", "simplifyLoop"].map(grab).join("\n") + "; return traceContour;")();
const min = -reach, cols = Math.ceil(2 * reach / cell), rows = cols, member = {};
for (let gy = 0; gy < rows; gy++) for (let gx = 0; gx < cols; gx++) {
  const cx = min + gx * cell + cell / 2, cy = min + gy * cell + cell / 2;
  if (cx * cx + cy * cy <= reach * reach) member[gy * cols + gx] = true;
}
const loops = trace(member, cols, rows, cell, min, min) || [];
const pts = loops.flat();
console.log(JSON.stringify({
  reach, loops: loops.length,
  x0: Math.min(...pts.map(p => p[0])), x1: Math.max(...pts.map(p => p[0])),
  y0: Math.min(...pts.map(p => p[1])), y1: Math.max(...pts.map(p => p[1])),
}));
"""

#: Der alte Wächter (Stand bis 2026-10-28) — die Gegenprobe setzt ihn wieder ein.
_ALT = (
    ("if (gy === 0 || !member[idx - cols])", "if (!member[idx - cols] && gy > 0)"),
    ("if (gx === 0 || !member[idx - 1])", "if (!member[idx - 1] && gx > 0)"),
    ("if (gy === rows - 1 || !member[idx + cols])", "if (!member[idx + cols] && gy < rows - 1)"),
    ("if (gx === cols - 1 || !member[idx + 1])", "if (!member[idx + 1] && gx < cols - 1)"),
)


def _messen(quelle: str) -> dict:
    out = subprocess.run(["node", "-e", _HARNESS], input=quelle, capture_output=True,
                         text=True, check=True, timeout=30)
    return json.loads(out.stdout)


def _pruefen(m: dict) -> None:
    assert m["loops"] == 1, f"die Kontur zerfällt in {m['loops']} Bruchstücke"
    r = m["reach"]
    assert (m["x0"], m["x1"], m["y0"], m["y1"]) == (-r, r, -r, r), f"Kontur nicht symmetrisch: {m}"


@needs_node
def test_die_kontur_eines_randknotens_ist_eine_geschlossene_linie() -> None:
    _pruefen(_messen(GRAPH_JS.read_text(encoding="utf-8")))


@needs_node
def test_gegenprobe_der_alte_randwaechter_wird_rot() -> None:
    quelle = GRAPH_JS.read_text(encoding="utf-8")
    for neu, alt in _ALT:
        assert quelle.count(neu) == 1, f"Anker nicht eindeutig: {neu}"
        quelle = quelle.replace(neu, alt)
    with pytest.raises(AssertionError):
        _pruefen(_messen(quelle))
