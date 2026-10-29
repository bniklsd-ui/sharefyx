"""Die **Form** der Karte (Plan `docs/concepts/phase10_5_block14_7_plan.md` §5, Abnahme
P10.5-73/74) im Beleg der Kartenbilder-Probe (`p105_b14_karte_bilder.json` → `form`).

**Was dieser Wächter prüft.** Nicht die Zahlen eines bestimmten Stands — die ändern sich mit
jedem Schritt von Block 14.7 —, sondern dass der Beleg **gemessen** ist und dass seine Zellen
**zu seinen eigenen Zahlen passen**: eine Zelle, die grün sagt, obwohl ihre Zahl die Schwelle
reißt, ist die Fehlerklasse „Wächter prüft etwas anderes, als er behauptet".

**Schritt 14.7.0 (Basislinie, 2026-10-29):** `fuelle` 0,497, `verteilung` 25,1 px,
`kontur_welligkeit` 11,10 rad/100 px — alle drei **rot**, das ist der Befund, kein Fehler;
`kontur_abstand` 8,0 px grün.

**Die Gegenproben** rufen **dieselbe** Prüffunktion an einem manipulierten Beleg auf.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
PROBE = REPO_ROOT / "phase10_5_finishing" / "probes" / "p105_b14_karte_bilder.py"
BELEG = REPO_ROOT / "phase10_5_finishing" / "probes" / "p105_b14_karte_bilder.json"


def _schwellen_aus_der_probe() -> dict:
    """Die Schwellen aus der **Probe** gelesen (Quelltext, nicht importiert — die Probe startet
    beim Import nichts, liest aber `sys.argv`), nicht hier wiederholt."""
    werte = {}
    for zeile in PROBE.read_text(encoding="utf-8").splitlines():
        for name in ("FUELLE_MIN", "VERTEILUNG_FAKTOR", "VERTEILUNG_BASIS_PX",
                     "WELLIGKEIT_ANTEIL", "WELLIGKEIT_BASIS"):
            if zeile.startswith(name + " = "):
                roh = zeile.split("=", 1)[1].split("#", 1)[0].strip()
                werte[name] = None if roh == "None" else float(roh)
    return werte


def pruefe_form(beleg: dict) -> None:
    form = beleg.get("form")
    assert form, "der Beleg traegt keine Form-Messung (Schritt 14.7.0)"
    s = form["schwellen"]
    q = _schwellen_aus_der_probe()
    assert s["fuelle_min"] == q["FUELLE_MIN"], "Schwelle fuelle weicht von der Probe ab"
    assert s["verteilung_basis_px"] == q["VERTEILUNG_BASIS_PX"], "Basis verteilung weicht ab"
    assert s["welligkeit_basis"] == q["WELLIGKEIT_BASIS"], "Basis welligkeit weicht ab"
    sol = form["fuelle"]["soliditaet"]
    nn = form["verteilung"]["nn_median_px"]
    wel = form["welligkeit"]["zusatzkruemmung_rad_je_100px"]
    assert sol is not None and 0 < sol <= 1, f"Soliditaet nicht gemessen: {sol}"
    assert nn is not None and nn > 0, f"Nachbarabstand nicht gemessen: {nn}"
    assert wel is not None and wel >= 0, f"Welligkeit nicht gemessen: {wel}"
    z = form["zellen"]
    assert z["fuelle"] == (sol >= s["fuelle_min"]), "Zelle fuelle passt nicht zu ihrer Zahl"
    assert z["verteilung"] == (nn >= s["verteilung_faktor"] * s["verteilung_basis_px"]), (
        "Zelle verteilung passt nicht zu ihrer Zahl")
    assert z["kontur_welligkeit"] == (wel <= s["welligkeit_anteil"] * s["welligkeit_basis"]), (
        "Zelle kontur_welligkeit passt nicht zu ihrer Zahl")
    mn = form["kontur_abstand"]["min_px"]
    assert z["kontur_abstand"] == (mn is None or mn > 0), "Zelle kontur_abstand passt nicht"
    assert form["p10_5_73"] == (z["fuelle"] and z["verteilung"]), "Summe P10.5-73 falsch"
    assert form["p10_5_74"] == (z["kontur_welligkeit"] and z["kontur_abstand"]), (
        "Summe P10.5-74 falsch")


def _beleg() -> dict:
    return json.loads(BELEG.read_text(encoding="utf-8"))


def test_the_form_is_measured_and_consistent():
    pruefe_form(_beleg())


def test_the_baselines_are_set():
    q = _schwellen_aus_der_probe()
    assert q["VERTEILUNG_BASIS_PX"] == 25.1, "Basislinie 14.7.0: 25,1 px"
    assert q["WELLIGKEIT_BASIS"] == 11.096, "Basislinie 14.7.0: 11,096 rad/100 px"


@pytest.mark.parametrize("feld,wert", [
    (("zellen", "fuelle"), None),             # Zelle umgedreht
    (("zellen", "verteilung"), None),
    (("zellen", "kontur_welligkeit"), None),
    (("p10_5_73",), None),
])
def test_a_flipped_cell_would_be_rejected(feld, wert):
    beleg = copy.deepcopy(_beleg())
    ziel = beleg["form"]
    for k in feld[:-1]:
        ziel = ziel[k]
    ziel[feld[-1]] = not ziel[feld[-1]]
    with pytest.raises(AssertionError):
        pruefe_form(beleg)


def test_a_beleg_without_form_would_be_rejected():
    beleg = copy.deepcopy(_beleg())
    del beleg["form"]
    with pytest.raises(AssertionError):
        pruefe_form(beleg)



#: **Die Gegenläufe der Form** (Plan 14.7 §5, Schritt 14.7.3, 2026-10-29) — je ein Hebel auf
#: seinen Nullwert, gemessen mit der Bilder-Probe (`--konstante=`). **Gemessen:** `anker` und
#: `glatt` machen **genau** ihre Zelle rot; `spreizung` macht `verteilung` **und** `fuelle` rot
#: (ohne Streckung füllen die Lappen ihr Gitter nicht — Solidität 0,731); festgehalten wie
#: gemessen, nicht geschönt.
FORM_GEGENLAEUFE = {
    "anker": {"fuelle"},
    "spreizung": {"verteilung", "fuelle"},
    "glatt": {"kontur_welligkeit"},
}


@pytest.mark.parametrize("name,rot", sorted(FORM_GEGENLAEUFE.items()))
def test_each_form_gegenlauf_turns_exactly_its_cells_red(name, rot):
    datei = BELEG.with_name("p105_b14_karte_bilder_konstante_gegenlauf_%s.json" % name)
    beleg = json.loads(datei.read_text(encoding="utf-8"))
    pruefe_form(beleg)
    gemessen = {k for k, v in beleg["form"]["zellen"].items() if not v}
    assert gemessen == rot, f"Gegenlauf {name}: rot {sorted(gemessen)}, erwartet {sorted(rot)}"


def test_the_chosen_state_turns_the_form_green():
    """Seit 14.7.3 (gewählt vom Nikinger am 2026-10-29) sind P10.5-73 und P10.5-74 grün."""
    form = _beleg()["form"]
    assert form["p10_5_73"] is True and form["p10_5_74"] is True, form["zellen"]
