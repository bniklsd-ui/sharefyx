"""Block 18 (18.0–18.3): der **Beleg** der Karten-Messung (`probes/p105_b18_karte_messung.py`).

Die Probe fährt gegen eine Wegwerf-Instanz (rund drei Minuten je Lauf) und kann deshalb nicht in der
Suite laufen — der Wächter prüft die **Belegdateien** im Repo und bindet sie an den Code, so wie
`test_b14_layout_probe.py` es für Block 14 tut. Er ist ein Schloss auf den Stand, kein Urteil:
wird eine Zelle rot, steht genau das im Diff dieser Datei.

| Beleg | Inhalt |
|---|---|
| `p105_b18_basislinie.json` | 18.0, **vor** dem Umbau: `draw()` 309 ms bei „beide an", ein Knoten mit 28.104 px/Bild |
| `p105_b18_karte_messung.json` | **nach** 18.1–18.3 (Stern, Mindestdistanz, Zwischenspeicher, zwei Schritte je Bild, V4): alle Zellen grün **außer** `ausreisser` (A1, offen) |
| `p105_b18_karte_messung_dpr2.json` | dieselbe Probe bei Geräte-Dichte 2 (Retina): Ruhe/Pan ≤ 6,2 ms; das Einschwingen „beide" braucht 2,6 s (> 2,5 s) |
| `p105_b18_gegenlauf_*.json` | je Gegenlauf: **seine** Zelle wird rot, die übrigen bleiben (Tabelle `GEGENLAEUFE18` im Probe-Kopf) |
| `p105_b18_gegenlauf_buendel.json` | **verworfene** Teilmaßnahme 18.1 (b): die Kanten je Stil bündeln war **langsamer** |

**Offen und ausdrücklich rot:** `ausreisser` (Ein-Item-Space im Zustand „Ordner" 125 px = 3,1 × `REGION_GAP`, Ziel ≤ 2 ×) —
das ist A1 (Ankerabstand), im Plan §5.5 ausdrücklich nicht gebaut. Wird sie grün, muss **diese** Datei geändert werden.

**Zwei ehrliche Einschränkungen** (beide im Plan §5.7): der Gegenlauf `schleuder` (`MAX_SPEED` allein) bleibt unter der
Mindestdistanz **grün** — die Grenze greift auf keiner gemessenen Saat mehr (Spitze ≤ 244 px/Bild, Addon Insel §4.4) —,
und `kein_schutz` (beide Gurte aus) färbt **zwei** Zellen rot (`schleuder`, `insel`).
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

ALLE_ZELLEN = {"kanten", "bildzeit_ruhe", "sim_dauer", "zwischenspeicher", "strichbild", "insel", "schleuder",
               "ausreisser"}
#: Im Normalfall grün — `ausreisser` ist A1 und steht ausdrücklich rot.
NORMAL_GRUEN = ALLE_ZELLEN - {"ausreisser"}


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


def test_after_state_is_green_except_the_open_a1_cell() -> None:
    n = _laden("p105_b18_karte_messung.json")
    assert set(n["zellen"]) == ALLE_ZELLEN
    assert {z for z, ok in n["zellen"].items() if ok} == NORMAL_GRUEN
    assert n["zellen"]["ausreisser"] is False
    for z in n["zustaende"].values():
        assert z["kanten_gegenrechnung"]["ok"] and z["kanten_gegenrechnung"]["paare_gleich"]
        assert z["geometrie"]["koerper_komponenten"] == 1                      # 18.2b: kein Insel-Tritt
    # der Stern: 188 Ordner-Kanten statt 5.728, 480 statt 7.326 bei „beide"
    assert n["zustaende"]["ordner"]["draw"]["kanten"]["implicit"] == 188
    assert n["zustaende"]["beide"]["draw"]["kanten"]["implicit"] == 480


def test_the_performance_numbers_stand() -> None:
    n = _laden("p105_b18_karte_messung.json")
    beide = n["zustaende"]["beide"]
    assert beide["draw"]["pan_ms"] <= 16.7                      # V1: 34,5 -> ~2,3 ms
    assert beide["simulation"]["dauer_ms"] <= 2500              # V3: 55 s -> ~1,6 s
    assert beide["simulation"]["frames"] == 65                  # zwei Schritte je Bild (129 Schritte)
    assert n["strichbild"]["verstoesse"] == 0 and n["strichbild"]["geschlossene_luecke"] > 0   # V4
    assert all(s["abweichende_pixel"] == 0 for s in n["zwischenspeicher"])                     # V1: Cache == frisch
    assert {"ruhe", "pan", "zoom", "drag", "drag_ende", "schalter_tags", "schalter_ordner"} <= {
        s["name"] for s in n["zwischenspeicher"]}
    # nur berichtet, keine Schwelle: der Hover-Wechsel und das Bild mit Signaturwechsel kosten weiter ein volles Bild
    assert n["info"]["hover_wechsel_ms"] > 20


def test_dpr2_evidence_rest_and_pan_hold_settling_does_not() -> None:
    n = _laden("p105_b18_karte_messung_dpr2.json")
    assert n["browser"]["dpr"] == 2
    assert n["zellen"]["bildzeit_ruhe"] is True and n["zellen"]["zwischenspeicher"] is True
    # ehrlich: bei Dichte 2 braucht das Einschwingen „beide" mehr als 2,5 s (Software-Rasterung)
    assert n["zellen"]["sim_dauer"] is False


#: Gegenlauf -> die Zellen, die rot werden müssen. Alle übrigen Zellen des Normalfalls bleiben grün.
GEGENLAEUFE_ROT = {
    "clique": {"kanten", "sim_dauer"},        # die Clique ist auch das alte Einschwingen (Sekunden statt 1,6 s)
    "tritt": {"insel"},
    "kein_schutz": {"schleuder", "insel"},    # zwei Zellen -- beide Gurte aus
    "schleuder": set(),                        # ZAHNLOS unter der Mindestdistanz (Addon Insel §4.4, Weg 1)
    "veraltet": {"zwischenspeicher"},
    "ohne_speicher": {"bildzeit_ruhe"},
    "ein_schritt": {"sim_dauer"},
    "v4_aus": {"strichbild"},
}


@pytest.mark.parametrize("gegenlauf", sorted(GEGENLAEUFE_ROT))
def test_each_counter_run_turns_exactly_its_cells_red(gegenlauf: str) -> None:
    g = _laden("p105_b18_gegenlauf_%s.json" % gegenlauf)
    assert g["gegenlauf"] == gegenlauf
    rot = {z for z, ok in g["zellen"].items() if not ok} - {"ausreisser"}
    assert rot == GEGENLAEUFE_ROT[gegenlauf], "Gegenlauf %s färbt %s rot" % (gegenlauf, sorted(rot))


def test_clique_counter_run_is_the_old_cost_scene() -> None:
    g = _laden("p105_b18_gegenlauf_clique.json")
    assert g["zustaende"]["ordner"]["draw"]["kanten"]["implicit"] == 5728


def test_rejected_bundling_is_documented_as_slower() -> None:
    """18.1 (b): ein Pfad je Stil war langsamer als ein `stroke()` je Kante — Beleg im Repo, der
    Code zeichnet je Kante (kein `styleKey`/`groups` mehr in `drawEdges()`)."""
    b = _laden("p105_b18_gegenlauf_buendel.json")
    assert b["zustaende"]["beide"]["draw"]["draw_nur_kanten_ms"] > 25     # gebündelt: 29 ms Kantenzeit
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
    assert js.count(mod.PFLASTER_ANKER) == 1 and js.count(mod.BODY_ANKER) == 1
    assert set(mod.GEGENLAEUFE18) == set(GEGENLAEUFE_ROT)


def test_the_rules_stand_in_the_code() -> None:
    js = GRAPH_JS.read_text(encoding="utf-8")
    assert "const MAX_SPEED = 600;" in js
    assert "const REPULSION_MIN_DIST = 6;" in js
    assert "Math.max(dx * dx + dy * dy + 0.01, REPULSION_MIN_DIST * REPULSION_MIN_DIST)" in js
    assert "const SIM_STEPS_PER_FRAME = 2;" in js
    assert "function blitLayer(shown, rings)" in js and "function layerSignature(shown)" in js
    assert "if (dash && dash[1] <= edgeWidth) dash = null;" in js
    # die Mitte des Sterns ist das zuletzt geaenderte Item (`updated`), bei Gleichstand die kleinere ID
    assert "function starHub(group)" in js and "a > b || (a === b && n.id < hub.id)" in js
    # die Signatur kennt die Positionen und Grade (ein vergessener Ausloeser waere ein veraltetes Bild)
    assert "Math.round(n.x * 8)" in js and "n.deg" in js.split("function layerSignature")[1].split("}")[0]
