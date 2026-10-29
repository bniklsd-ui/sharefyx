"""Die Anker-Regel des Hexagonalgitters (Plan `docs/concepts/phase10_5_block14_7_plan.md` §2.1,
H1–H5) — gemessen von `probes/p105_b14_7_hex_probe.mjs` am **echten** `computeRegions()`.

H1 der k-te Platz hängt nur von k ab · H2 kein Ankerpaar näher als `slot` · H3 ein Item im
kleineren Space bewegt keinen Anker · H4 `"spirale"` ist bitgleich zu Block 14 · H5 Determinismus.
**Gegenlauf `ring`** (gleichmäßiger Ring, 2π/(Spaces−1)) muss H1 **und** H2 rot machen.
"""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

PROBE = Path(__file__).resolve().parents[1] / "probes" / "p105_b14_7_hex_probe.mjs"
needs_node = pytest.mark.skipif(shutil.which("node") is None, reason="node fehlt")


def _lauf(*args: str) -> dict:
    proc = subprocess.run(["node", str(PROBE), *args], capture_output=True, text=True, timeout=120)
    assert proc.returncode == 0, proc.stderr[-2000:]
    return json.loads(proc.stdout)


@needs_node
def test_the_hex_rule_holds_h1_to_h5():
    r = _lauf()
    assert r["H4"]["ok"], f"spirale ist nicht bitgleich zu Block 14: {r['H4']}"
    for ordnung, z in r["ordnungen"].items():
        for h in ("H1", "H2", "H3", "H5"):
            assert z[h]["ok"], f"{ordnung} {h}: {z[h]}"
    assert r["alle_ok"] is True


@needs_node
def test_an_even_ring_breaks_h1_and_h2():
    r = _lauf("--gegenlauf=ring")
    for ordnung, z in r["ordnungen"].items():
        assert not z["H1"]["ok"], f"{ordnung}: H1 haette rot werden muessen"
        assert not z["H2"]["ok"], f"{ordnung}: H2 haette rot werden muessen"
        assert z["H3"]["ok"] and z["H5"]["ok"], f"{ordnung}: nur H1/H2 duerfen rot werden"
    assert r["alle_ok"] is False
