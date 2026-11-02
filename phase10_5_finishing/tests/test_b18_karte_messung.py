"""Block 18 (18.0–18.2): der **Beleg** der Karten-Messung (`probes/p105_b18_karte_messung.py`).

Die Probe fährt gegen eine Wegwerf-Instanz (rund drei Minuten je Lauf) und kann deshalb nicht in der
Suite laufen — der Wächter prüft die **Belegdateien** im Repo und bindet sie an den Code, so wie
`test_b14_layout_probe.py` es für Block 14 tut. Er ist ein Schloss auf den Stand, kein Urteil:
wird eine Zelle rot, steht genau das im Diff dieser Datei.

| Beleg | Inhalt |
|---|---|
| `p105_b18_basislinie.json` | 18.0, **vor** dem Umbau: `draw()` 309 ms bei „beide an", ein Knoten mit 28.104 px/Bild |
| `p105_b18_karte_messung.json` | **nach** 18.1/18.2 (Stern, Geschwindigkeitsgrenze): Zellen `kanten` und `schleuder` grün |
| `p105_b18_gegenlauf_clique.json` | die Clique statt des Sterns: **nur** `kanten` wird rot |
| `p105_b18_gegenlauf_schleuder.json` | keine Geschwindigkeitsgrenze: **nur** `schleuder` wird rot |
| `p105_b18_gegenlauf_buendel.json` | **verworfene** Teilmaßnahme 18.1 (b): die Kanten je Stil bündeln war **langsamer** |

**Offen und ausdrücklich rot:** `bildzeit` (≤ 16 ms bei „beide an") und `ausreisser` (≤ 2 × `REGION_GAP`
im Zustand „Ordner"). Beide stehen im Beleg als `false`; ihre Entscheidung liegt beim Nikinger (Plan
`docs/concepts/phase10_5_block18_live_fixes_plan.md` §5.5). Der Wächter hält das fest — wird eine der
beiden grün, muss **diese** Datei geändert werden.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
PROBES = REPO_ROOT / "phase10_5_finishing" / "probes"
GRAPH_JS = REPO_ROOT / "phase5_ui" / "webui" / "static" / "js" / "graph.js"


def _laden(name: str) -> dict:
    return json.loads((PROBES / name).read_text(encoding="utf-8"))


def _probe_modul():
    argv = sys.argv
    sys.argv = [argv[0]]
    try:
        spec = importlib.util.spec_from_file_location(
            "p105_b18_karte_messung_test", PROBES / "p105_b18_karte_messung.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    finally:
        sys.argv = argv
    return mod


def test_baseline_shows_the_measured_cost_and_the_throw() -> None:
    b = _laden("p105_b18_basislinie.json")
    zs = b["zustaende"]
    assert zs["beide"]["draw"]["draw_ms"] > 300          # 309 ms je Bild, vor dem Umbau
    assert zs["beide"]["simulation"]["dauer_ms"] > 50_000
    # K3/K4 sind als Kostenquelle widerlegt (Plan §5.2)
    assert zs["beide"]["draw"]["ringe_ms"] < 1 and zs["beide"]["draw"]["kraefte_ms"] < 1
    assert b["tags_spur"]["hoechste_geschwindigkeit_px_pro_tick"] > 20_000    # N1


def test_after_state_has_star_edges_and_no_throw() -> None:
    n = _laden("p105_b18_karte_messung.json")
    assert n["zellen"]["kanten"] is True
    assert n["zellen"]["schleuder"] is True
    for z in n["zustaende"].values():
        assert z["kanten_gegenrechnung"]["ok"] and z["kanten_gegenrechnung"]["paare_gleich"]
        assert z["simulation"]["spur"]["hoechste_geschwindigkeit_px_pro_tick"] <= 600
    # der Stern: 188 Ordner-Kanten statt 5.728, 480 statt 7.326 bei „beide"
    assert n["zustaende"]["ordner"]["draw"]["kanten"]["implicit"] == 188
    assert n["zustaende"]["beide"]["draw"]["kanten"]["implicit"] == 480
    # der ruhige Zustand ist **unberuehrt** (das Layout aus Block 14 bleibt byte-gleich)
    b = _laden("p105_b18_basislinie.json")
    assert n["zustaende"]["aus"]["geometrie"]["welt_mit_ausreisser_px"] == pytest.approx(
        b["zustaende"]["aus"]["geometrie"]["welt_mit_ausreisser_px"], abs=1e-3)


def test_open_cells_are_stated_red_until_the_nikinger_decides() -> None:
    n = _laden("p105_b18_karte_messung.json")
    assert n["zellen"]["bildzeit"] is False      # 34 ms bei „beide", Ziel 16 ms — Strichelung (Plan §5.5)
    assert n["zellen"]["ausreisser"] is False    # 121 px = 3,0 x REGION_GAP im Zustand „Ordner"


@pytest.mark.parametrize("gegenlauf,rot,gruen", [
    ("clique", "kanten", ["schleuder"]),
    ("schleuder", "schleuder", ["kanten"]),
])
def test_each_counter_run_turns_its_own_cell_red(gegenlauf: str, rot: str, gruen: list) -> None:
    g = _laden("p105_b18_gegenlauf_%s.json" % gegenlauf)
    assert g["gegenlauf"] == gegenlauf
    assert g["zellen"][rot] is False
    for z in gruen:
        assert g["zellen"][z] is True, "der Gegenlauf darf nur seine eigene Zelle rot machen"


def test_clique_counter_run_is_the_old_cost_scene() -> None:
    g = _laden("p105_b18_gegenlauf_clique.json")
    assert g["zustaende"]["ordner"]["draw"]["kanten"]["implicit"] == 5728
    assert g["zustaende"]["beide"]["draw"]["draw_ms"] > 300


def test_rejected_bundling_is_documented_as_slower() -> None:
    """18.1 (b): ein Pfad je Stil war langsamer als ein `stroke()` je Kante — Beleg im Repo, der
    Code zeichnet je Kante (kein `styleKey`/`groups` mehr in `drawEdges()`)."""
    b = _laden("p105_b18_gegenlauf_buendel.json")
    n = _laden("p105_b18_karte_messung.json")
    assert b["zustaende"]["beide"]["draw"]["draw_nur_kanten_ms"] \
        < n["zustaende"]["beide"]["draw"]["draw_nur_kanten_ms"] + 12   # ohne Buendel nicht schlechter
    js = GRAPH_JS.read_text(encoding="utf-8")
    assert "styleKey" not in js and "groups.push" not in js


def test_counter_run_anchors_exist_exactly_once_in_graph_js() -> None:
    """Ein Gegenlauf, dessen Anker im Code nicht mehr steht, patcht nichts und bleibt gruen —
    die Fehlerklasse, die dieser Ordner mehrfach gesehen hat (Memory: ehrliche Gegenlaeufe)."""
    mod = _probe_modul()
    js = GRAPH_JS.read_text(encoding="utf-8")
    for name, patch in mod.GEGENLAEUFE18.items():
        for anker in patch:
            assert js.count(anker) == 1, "Gegenlauf %s: Anker %r steht %dx in graph.js" % (
                name, anker[:50], js.count(anker))
    assert mod.PFLASTER_ANKER in js and js.count(mod.PFLASTER_ANKER) == 1


def test_the_rules_stand_in_the_code() -> None:
    js = GRAPH_JS.read_text(encoding="utf-8")
    assert "const MAX_SPEED = 600;" in js
    assert "function starHub(group)" in js and "function starEdges(" in js
    # die Mitte ist das zuletzt geaenderte Item (`updated`), bei Gleichstand die kleinere ID
    assert "a > b || (a === b && n.id < hub.id)" in js
