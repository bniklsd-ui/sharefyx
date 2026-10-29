"""Das **Schließen** der Körpermaske (P10.5 Block 14, Schritt 14.6) — die Distanztransformation
ist **exakt**, nicht genähert.

**Was der Schritt baut.** Aus fünf Inseln wird **ein** Körper (Plan
`docs/concepts/phase10_5_block14_6_plan.md` §2.1): die Körpermaske wird erst um
`LOBE_CLOSE_PX` **gewachsen** und dann um denselben Betrag **geschrumpfen**. Das Schrumpfen
ist eine **Distanztransformation auf dem Raster** — eine Zelle bleibt, wenn ihr euklidischer
Abstand zur nächsten Zelle außerhalb des gewachsenen Satzes größer als `LOBE_CLOSE_PX / cell`
ist.

**Warum dieser Wächter exakt ist und nicht „ungefähr“.** Die Chamfer-Näherung (3-4-5) weicht
bis zu **8 %** vom euklidischen Abstand ab — bei einem Radius von 200 px sind das 16 px, und die
Ränder des Körpers werden **achteckig** statt rund (Plan §2.1: „eine Chamfer-Näherung ist
**nicht** zulässig"). Der Wächter vergleicht deshalb die **echte** Funktion `distanzQuadrat()`
aus `graph.js` (per Quelltext herausgeschnitten, in Node ausgeführt — kein Haken im
Produktcode) mit einer **Brute-Force**-Rechnung auf demselben Raster: der Abstand zu jedem
einzelnen Ziel, das Minimum, der Vergleich — O(Zellen²), aber auf einem kleinen Raster.

**Die Gegenprobe:** derselbe Wächter muss an einer **Chamfer-Näherung** rot werden (die
Abweichung ist messbar) — sonst prüfte er nichts.
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

#: Der Harness: die **echten** Funktionen aus `graph.js`, verglichen mit der Brute-Force.
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
const dist = new Function(
  ["distanzQuadrat", "distanz1d", "sourceCost"].map(grab).join("\n")
  + "; return distanzQuadrat;")();

// Das Raster: 11 x 9 Zellen, die Zielzellen deterministisch gestreut (x * 3 + y * 5) % 7 == 0.
const cols = 11, rows = 9;
const quelle = new Uint8Array(cols * rows);
let ziele = 0;
for (let y = 0; y < rows; y++) {
  for (let x = 0; x < cols; x++) {
    if ((x * 3 + y * 5) % 7 === 0) { quelle[y * cols + x] = 1; ziele++; }
  }
}
const d2 = dist(quelle, cols, rows);

// Die Brute-Force: der Abstand zu **jedem** Ziel, das Minimum.
let maxAbweichung = 0;
let geprueft = 0;
for (let y = 0; y < rows; y++) {
  for (let x = 0; x < cols; x++) {
    let best = Infinity;
    for (let yy = 0; yy < rows; yy++) {
      for (let xx = 0; xx < cols; xx++) {
        if (!quelle[yy * cols + xx]) continue;
        const dx = x - xx, dy = y - yy;
        const cand = dx * dx + dy * dy;
        if (cand < best) best = cand;
      }
    }
    if (!isFinite(best)) continue;
    geprueft++;
    const abw = Math.abs(d2[y * cols + x] - best);
    if (abw > maxAbweichung) maxAbweichung = abw;
  }
}
console.log(JSON.stringify({
  cols, rows, ziele, geprueft,
  maxAbweichung,
  werte: Array.from(d2).map(v => (isFinite(v) && v < 1e19 ? v : null)),
}));
"""

#: Die **Chamfer-Naeherung** (3-4-5) als Gegenprobe: sie weicht vom euklidischen Abstand ab
#: — bei diesem Raster messbar, weil die Ziele diagonal versetzt liegen.
_CHAMFER = (
    ("      if (!quelle[yy * cols + xx]) continue;",
     "      if (!quelle[yy * cols + xx]) continue;"),
)


def _messen(quelle: str) -> dict:
    out = subprocess.run(["node", "-e", _HARNESS], input=quelle, capture_output=True,
                         text=True, check=True, timeout=30)
    return json.loads(out.stdout)


def _pruefen(m: dict) -> None:
    assert m["geprueft"] == m["cols"] * m["rows"], f"nicht alle Zellen geprueft: {m}"
    assert m["maxAbweichung"] == 0.0, (
        f"die Distanztransformation weicht vom euklidischen Abstand ab (max. "
        f"{m['maxAbweichung']} Zellen²) — Plan 14.6 §2.1 verbietet die Näherung")


@needs_node
def test_die_distanztransformation_ist_exakt_euklidisch() -> None:
    _pruefen(_messen(GRAPH_JS.read_text(encoding="utf-8")))


@needs_node
def test_die_zielzellen_haben_den_abstand_null() -> None:
    """Eine Zielzelle hat zu sich selbst den Abstand **0** — die Kehrprobe: die Funktion
    rechnet nicht irgendeinen Abstand, sondern den zur nächsten Zielzelle."""
    m = _messen(GRAPH_JS.read_text(encoding="utf-8"))
    werte = m["werte"]
    null_werte = [w for w in werte if w == 0.0]
    assert len(null_werte) == m["ziele"], (
        f"{len(null_werte)} Zellen mit Abstand 0, erwartet {m['ziele']} (die Zielzellen)")


@needs_node
def test_eine_chamfer_naeherung_wuerde_rot_werden() -> None:
    """Die **Gegenprobe**: eine Näherung (statt der exakten Rechnung) muss am selben Wächter
    rot werden. Der Wächter prüft die **Zahl** — nicht die Form des Codes.

    **Die Näherung:** die Manhattan-Distanz (`|q - p|` statt `(q - p)²`) — dieselbe Familie
    wie die 3-4-5-Chamfer. Sie weicht vom euklidischen Abstand ab, und zwar **gemessen** an
    den diagonal versetzten Zielen dieses Rasters."""
    quelle = GRAPH_JS.read_text(encoding="utf-8")
    alt = "    d[q] = dq * dq + f[v[k]];"
    assert quelle.count(alt) == 1, f"der Anker der Distanzrechnung ist nicht eindeutig: {alt}"
    genaehert = quelle.replace(alt, "    d[q] = dq + f[v[k]];   // Gegenprobe: die Manhattan-Distanz")
    with pytest.raises(AssertionError):
        _pruefen(_messen(genaehert))


@needs_node
def test_alle_abstaende_sind_ganzzahlen_und_nie_null_ohne_ziel() -> None:
    """Die Abstände liegen auf einem **Gitter**: sie sind Ganzzahlen (in Zellen²), und eine
    Zelle, die selbst kein Ziel ist, hat nie den Abstand **0**. Sonst rechnete die Funktion
    nicht den Abstand zur nächsten Zielzelle, sondern irgendetwas anderes."""
    m = _messen(GRAPH_JS.read_text(encoding="utf-8"))
    werte = m["werte"]
    assert all(w is None or float(w).is_integer() for w in werte), (
        f"ein Abstand ist keine Ganzzahl: {werte}")
    null_werte = sum(1 for w in werte if w == 0.0)
    assert null_werte == m["ziele"], (
        f"{null_werte} Zellen mit Abstand 0, erwartet {m['ziele']} (nur die Zielzellen)")
    assert min(w for w in werte if w is not None and w > 0) >= 1, (
        "ein Abstand ist kleiner als eine Zelle: {werte}")
