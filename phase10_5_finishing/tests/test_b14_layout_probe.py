"""Der **Beleg** der Block-14-Probe: `p105_b14_layout_probe.json` steht im Repo, und die
Zellen tragen den **Stand des Schritts 14.0** (die Basislinie).

**Warum ein Wächter und nicht nur eine Notiz.** Die Probe fährt gegen eine Wegwerf-Instanz;
was sie misst, landet als JSON im Repo. Eine JSON-Datei im Repo ist aber nur so viel wert wie
die Aussage, die man über sie macht — und die Aussage („Regionen und Kamera sind rot, der
Determinismus und das Budget sind grün") steht sonst nirgends im Code. Dieser Wächter bindet
sie an den Plan: **welche Zelle ab welchem Schritt grün sein muss**, steht in
`docs/concepts/phase10_5_block14_kartenlayout_plan.md` §4.

**Der Wächter ist ein Schloss auf den Fortschritt, kein Urteil.** Er sagt: „Stand 14.0 =
diese Zellen sind rot, diese sind grün." Wird eine Zelle im nächsten Schritt grün, wird
**hier** die Menge der roten Zellen kleiner — und genau diese Änderung steht im Diff. Wäre
der Wächter statisch, würde ein Schritt, der eine Zelle kaputtmacht, unauffällig durchrutschen.

| Schritt (Plan §4) | was grün werden muss |
|---|---|
| 14.0 (Basislinie) | `determinismus`, `budget` — die anderen vier sind **rot** (Basislinie) |
| 14.1 (**dieser Stand**) | `determinismus` bleibt grün (L1–L3) — die vier roten Zellen bleiben rot, **aber ihre Zahlen wandern**: die Regionen von 57,2 % auf 82,2 %, das neue Item liegt jetzt **in** der Region seines Space |
| 14.2 | `regionen` **und** `stabilitaet` werden grün (L4: Anker-Gravitation) |
| 14.3 | `kamera` wird grün (`fitView()`) |
| 14.35 | `beschriftungen` wird grün (§2.7) |
| 14.4 | **alle** grün + jeder Gegenlauf rot an genau seiner Zelle |

**Die Zahlen sind mitgeprueft, nicht nur die `ok`-Flags** (der Test
`test_the_measured_numbers_are_the_ones_the_cells_stand_on`): ein Schritt, der eine Zelle
kaputtmacht, muss die Zahlen mitnehmen — sonst wuerde der Wächter die Bewegung der Zahlen
uebersehen. Die Zahlen der Basislinie (14.0) und des Stands 14.1 stehen beide im Diff
dieser Datei — **datiert**, weil sich der Code geaendert hat.

**Gegenprobe:** derselbe Wächter muss an einem **manipulierten** Beleg rot werden — und die
Gegenprobe ruft **dieselbe Testfunktion** auf (nicht eine nachgebaute Logik: ein Wächter, der
etwas anderes prüft als er behauptet, ist die Fehlerklasse, die hier verhindert wird).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
BELEG = REPO_ROOT / "phase10_5_finishing" / "probes" / "p105_b14_layout_probe.json"

#: Die Zellen der Probe (Plan §5, Abnahme P10.5-65–71).
ZELLEN = {
    "determinismus": "P10.5-65",
    "regionen": "P10.5-66",
    "kamera": "P10.5-67",
    "stabilitaet": "P10.5-68",
    "budget": "P10.5-69",
    "beschriftungen": "P10.5-71",
}

#: **Stand 14.0** — die Basislinie. Rot: die Zellen, die der Bau (14.1–14.35) grün macht.
ROT = {"regionen", "kamera", "stabilitaet", "beschriftungen"}
GRUEN = {"determinismus", "budget"}

#: Der **Datensatz** der Basislinie (Plan §5, datierte Abweichung vom 5x30-Seed: `beta` hat
#: 32 Items, damit „der nicht-größte Space" eindeutig ist).
SEED_ITEMS = {"alpha": 30, "beta": 32, "gamma": 30, "delta": 30, "epsilon": 30}
SEED_SUMME = 152


def _beleg() -> dict:
    assert BELEG.exists(), f"der Beleg fehlt: {BELEG}"
    return json.loads(BELEG.read_text(encoding="utf-8"))


def _zellen(beleg: dict) -> dict[str, bool]:
    messungen = beleg["messungen"]
    return {name: bool(messungen[name].get("ok")) for name in ZELLEN}


def test_the_beleg_has_every_cell():
    """Jede Zelle aus §5 muss im Beleg stehen — eine fehlende Zelle ist keine grüne Zelle,
    sondern eine **nicht gemessene**."""
    messungen = _beleg()["messungen"]
    fehlend = [name for name in ZELLEN if name not in messungen]
    assert not fehlend, f"im Beleg fehlen die Zellen: {fehlend}"


def test_the_baseline_is_red_in_exactly_these_cells():
    """**Das ist die Aussage des Schritts 14.0:** die Basislinie ist in `regionen`, `kamera`,
    `stabilitaet` und `beschriftungen` **rot** — das ist der Beleg, dass die Zellen messen.
    `determinismus` und `budget` sind grün (der heutige Code ist deterministisch und bleibt
    im 3-s-Budget)."""
    zellen = _zellen(_beleg())
    rot = {name for name, ok in zellen.items() if not ok}
    gruen = {name for name, ok in zellen.items() if ok}
    assert rot == ROT, f"die Basislinie ist rot in {sorted(rot)}, erwartet {sorted(ROT)}"
    assert gruen == GRUEN, f"die Basislinie ist gruen in {sorted(gruen)}, erwartet {sorted(GRUEN)}"


def test_the_beleg_records_the_seed_and_the_measured_numbers():
    """Der Beleg muss den **Datensatz** und die Zahlen nennen, aus denen die Zellen gingen —
    ohne sie ist „grün" eine Behauptung."""
    beleg = _beleg()
    assert beleg["schritt"] == "14.0", f"der Beleg ist Schritt {beleg['schritt']}"
    assert beleg["seed"]["spaces"] == 5, "fünf Spaces (der 5x30-Seed des Plans)"
    assert beleg["seed"]["items"] == SEED_SUMME, "152 Items (30/32/30/30/30 — siehe Plan §5)"
    assert beleg["seed"]["items_pro_space"] == SEED_ITEMS, "die Aufteilung je Space"
    determinismus = beleg["messungen"]["determinismus"]
    assert determinismus["max_abweichung_px"] <= 1.0, "der Determinismus ist ≤ 1 px"
    assert determinismus["knoten"] > 0, "der Determinismus misst echte Knoten"
    budget = beleg["messungen"]["budget"]
    assert budget["knoten"] >= 200, "die Budget-Zelle misst 200 Knoten"
    assert budget["ruhe_ms"] <= 3000, "die Karte kommt in 3 s zur Ruhe"
    assert budget["raf_calls_reduced_motion"] == 0, "reduced motion: 0 Frames"
    assert budget["kern_pixel_reduced_motion"] > 0, "die Karte ist auch ohne Frame gemalt"


def test_the_measured_numbers_are_the_ones_the_cells_stand_on():
    """Die **Zahlen** hinter den Zellen, nicht nur die booleschen `ok`-Felder: ein Beleg mit
    `regionen.ok = false` und einem Anteil von 99 % waere ein Witz. Jede Zelle wird an dem
    Wert geprueft, aus dem sie entschieden wurde."""
    beleg = _beleg()
    m = beleg["messungen"]

    # Determinismus (P10.5-65): beide Laeufe mit derselben Knotenmenge, Abweichung ≤ 1 px
    det = m["determinismus"]
    assert det["gemeinsam"] == det["knoten"] == det["knoten_lauf1"] == SEED_SUMME, (
        "die beiden Laeufe muessen dieselbe Knotenmenge gehabt haben")
    assert det["max_abweichung_px"] <= 1.0

    # Regionen (P10.5-66): **125** von 152 Knoten liegen beim Schwerpunkt ihres Space.
    # **[Datierte Korrektur 2026-10-26, Schritt 14.1]:** die Basislinie (14.0) trug **87**
    # (57,2 %) — mit dem **neuen Seed** (L1–L3: eine Region je Space, Ordner-Inseln,
    # Item-Spirale) sind es **125** (82,2 %). Die Zelle bleibt **rot** (unter 95 %): die
    # Zentrums-Gravitation zieht die Regionen noch zusammen — das ist die Aufgabe von 14.2.
    reg = m["regionen"]
    assert reg["knoten"] == SEED_SUMME
    assert reg["richtig"] == 125
    assert reg["anteil"] == pytest.approx(125 / SEED_SUMME, abs=1e-9)
    assert reg["anteil"] < 0.95, "die Regionen sind noch nicht getrennt (14.2)"

    # Kamera (P10.5-67): fuellt, passt — der Umriss sitzt aber weit ausserhalb der Mitte
    kam = m["kamera"]
    assert kam["passt"] is True
    assert kam["fuellgrad"] >= 0.60
    assert kam["versatz_mitte_px"] > 3.0, "die Karte steht nicht in der Mitte"
    assert kam["unsicherheit_px"] < kam["versatz_mitte_px"], (
        "die Unsicherheit der Kamerabestimmung traegt die Aussage nicht")

    # Beschriftungen (P10.5-71): es ueberlappen sich welche, der Fokus ist beschriftet
    bes = m["beschriftungen"]
    assert bes["fokus_beschriftung"] is True
    assert bes["gezeichnet"] >= 2, "es sind genug Beschriftungen gezeichnet worden"
    assert len(bes["ueberlappungen"]) >= 1, "die Basislinie hat Ueberlappungen"

    # Stabilitaet (P10.5-68): die anderen Spaces haben sich weit mehr als 2 px bewegt.
    # **[Datierte Korrektur 2026-10-26, Schritt 14.1]:** das neue Item liegt jetzt **in der
    # Region seines Space** (der Seed legt es dorthin — in der Basislinie 14.0 lag es noch
    # 118 px von einem fremden Space entfernt). Die Zelle bleibt **rot**, weil die **Verschiebung
    # der anderen Spaces** noch 233 px betraegt — das ist die Zentrums-Gravitation (14.2).
    stab = m["stabilitaet"]
    assert stab["median_verschiebung_px"] > 2.0
    assert stab["in_eigener_region"] is True, "das neue Item gehoert in die Region seines Space"

    # Budget (P10.5-69): 200 Knoten, 3 s, 0 Frames, die Karte ist gemalt
    bud = m["budget"]
    assert bud["knoten"] >= 200
    assert bud["ruhe_ms"] <= 3000
    assert bud["raf_calls_reduced_motion"] == 0
    assert bud["kern_pixel_reduced_motion"] > 0

    # **kein** Seitenfehler: ein Fehler im Graph-Code wuerde die Zellen stumm verfaelschen
    assert beleg["seitenfehler"] == [], f"der Beleg traegt Seitenfehler: {beleg['seitenfehler']}"
    assert beleg["alle_kriterien_erfuellt"] is False, (
        "die Basislinie kann nicht alle Kriterien erfuellen — das ist der Beleg, dass die "
        "Zellen messen")


def test_a_manipulated_beleg_would_be_rejected(tmp_path, monkeypatch):
    """Die Gegenprobe: **derselbe Wächter** (also die Testfunktion von oben, nicht eine
    nachgebaute Logik) muss an einem manipulierten Beleg rot werden — sonst prüfte er nichts.
    Der Beleg wird nicht am Objekt verändert, sondern **untergeschoben**: der Wächter liest
    seinen Beleg beim Aufruf."""
    beleg = _beleg()
    beleg["messungen"]["regionen"]["ok"] = True
    gefaelscht = tmp_path / "p105_b14_layout_probe.json"
    gefaelscht.write_text(json.dumps(beleg), encoding="utf-8")
    monkeypatch.setattr(sys.modules[__name__], "BELEG", gefaelscht)
    with pytest.raises(AssertionError):
        test_the_baseline_is_red_in_exactly_these_cells()


def test_a_beleg_with_a_broken_measurement_would_be_rejected(tmp_path, monkeypatch):
    """Die zweite Gegenprobe: nicht nur ein umgeschaltetes `ok`, sondern ein **manipulierter
    Messwert** muss auffallen. `regionen.anteil` auf 99 % zu setzen, ohne `ok` zu beruehren,
    muss den Wächter rot machen — er prueft die Zahlen, nicht die Flags."""
    beleg = _beleg()
    beleg["messungen"]["regionen"]["anteil"] = 0.99
    beleg["messungen"]["regionen"]["richtig"] = 150
    gefaelscht = tmp_path / "p105_b14_layout_probe.json"
    gefaelscht.write_text(json.dumps(beleg), encoding="utf-8")
    monkeypatch.setattr(sys.modules[__name__], "BELEG", gefaelscht)
    with pytest.raises(AssertionError):
        test_the_measured_numbers_are_the_ones_the_cells_stand_on()


def test_a_beleg_with_a_page_error_would_be_rejected(tmp_path, monkeypatch):
    """Die dritte Gegenprobe: ein **Seitenfehler** im Graph-Code (der die Zellen stumm
    verfaelschen wuerde) muss den Wächter rot machen."""
    beleg = _beleg()
    beleg["seitenfehler"] = ["TypeError: n.x is not a function"]
    gefaelscht = tmp_path / "p105_b14_layout_probe.json"
    gefaelscht.write_text(json.dumps(beleg), encoding="utf-8")
    monkeypatch.setattr(sys.modules[__name__], "BELEG", gefaelscht)
    with pytest.raises(AssertionError):
        test_the_measured_numbers_are_the_ones_the_cells_stand_on()
