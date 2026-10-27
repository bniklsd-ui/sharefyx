"""**Die Startwert-Messung** (P10.5 Block 14, Schritt 14.4): die Zahlen des Kartenlayouts sind
**gemessen, nicht gesetzt** (Plan §2.1/§2.4: "Startwerte, durch Messung in 14.4 justiert",
"in 14.4 werden sie **gemessen** (nicht gesetzt)").

**Was dieser Wächter prüft.** Die Tabelle `probes/p105_b14_startwerte_messung.json` ist der
Beleg: je Startwert die **gemessenen** Zellen (5 Spaces, 152 Items, 201 Knoten in der
Budget-Zelle). Die **Regel der Wahl** steht in der Tabelle selbst:

> Der Wert bleibt, wenn er die **Stabilität** hält (Median ≤ 2 px **und** Maximum ≤ 3 px)
> *und* die größte **Trennungs-Marge** hat (der kleinste Abstand „eigener Space-Schwerpunkt
> minus nächster fremder" über alle Knoten — 0 hieße: die Zelle kippt beim nächsten Item).

Der Wächter prüft **drei** Dinge:

1. **Der Wert im Code ist der gemessene.** Für jede der zehn Block-14-Konstanten muss der
   Wert in `graph.js` **genau der** sein, den die Regel aus der Tabelle auswählt — sonst wäre
   der Kommentar „gemessen in 14.4" eine Behauptung.
2. **Die Messung unterscheidet.** Jeder *andere* gemessene Wert derselben Konstante ist
   entweder **nicht stabil** (Median > 2 px oder Maximum > 3 px) oder hat eine **kleinere**
   Marge. Ohne diese Prüfung könnte die Tabelle auch dann „beweisen", wenn alle Werte
   gleich gemessen wären.
3. **Der Beleg nennt seine Randbedingung.** Die Tabelle trägt die Regel und die
   **Startwerte des Codes**; der Normalfall-Beleg der Browser-Probe trägt die Werte, die der
   Server **tatsächlich** ausgeliefert hat (`konstanten_gesendet`) — sie müssen mit dem Code
   übereinstimmen.

**Kein Test-Haken im Produktcode:** der Wächter liest die Messdatei und den echten
`graph.js` — er fährt keine Probe (die Browser-Probe ist zu langsam für die Testsuite).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
MESSUNG = (REPO_ROOT / "phase10_5_finishing" / "probes"
           / "p105_b14_startwerte_messung.json")
BELEG = REPO_ROOT / "phase10_5_finishing" / "probes" / "p105_b14_layout_probe.json"
GRAPH_JS = REPO_ROOT / "phase5_ui" / "webui" / "static" / "js" / "graph.js"

#: Die **Schwellen der Abnahme** (Plan §5, Abnahme P10.5-68): der Median der Verschiebung
#: und (der Wächter der Browser-Probe) das Maximum.
MEDIAN_MAX = 2.0
MAXIMUM_MAX = 3.0

#: Die zehn Block-14-Konstanten, die in 14.4 gemessen wurden (Plan §2.1–§2.4).
KONSTANTEN = [
    "REGION_ITEM_STEP", "REGION_PAD", "REGION_GAP", "ISLAND_FACTOR", "ITEM_STEP",
    "ITEM_JITTER_PX", "ANCHOR_GRAVITY", "CROSS_SPRING_FACTOR", "CROSS_SPRING_LENGTH_FACTOR",
    "ALPHA_START_SEEDED",
]


def _messung() -> dict:
    assert MESSUNG.exists(), f"die Messung fehlt: {MESSUNG}"
    return json.loads(MESSUNG.read_text(encoding="utf-8"))


def _konstante_aus_graph(name: str) -> str:
    """Der Wert der Konstante in der **echten** `graph.js` — nicht hier wiederholt: eine
    Dublette wäre die stille Abweichung, die dieser Ordner zweimal getroffen hat."""
    quelle = GRAPH_JS.read_text(encoding="utf-8")
    treffer = re.search(r"^const %s = ([^;]+);" % re.escape(name), quelle, re.M)
    assert treffer, f"die Konstante {name} steht nicht mehr in graph.js"
    return treffer.group(1).strip()


def _zellen(eintrag: dict) -> dict:
    return eintrag["zellen"]


def _stabil(eintrag: dict) -> bool:
    """Hält der Wert die **Stabilität**? (Median ≤ 2 px **und** Maximum ≤ 3 px.)"""
    zellen = _zellen(eintrag)
    return (zellen["stabilitaet_median_px"] is not None
            and zellen["stabilitaet_max_px"] is not None
            and zellen["stabilitaet_median_px"] <= MEDIAN_MAX
            and zellen["stabilitaet_max_px"] <= MAXIMUM_MAX)


def _varianten_je_konstante(messung: dict) -> dict:
    gruppen: dict[str, dict[str, dict]] = {}
    for eintrag in messung["varianten"].values():
        for name, wert in (eintrag.get("konstanten") or {}).items():
            gruppen.setdefault(name, {})[wert] = eintrag
    return gruppen


def test_the_messung_names_its_rule_and_its_startwerte():
    """Die Tabelle muss **sagen**, nach welcher Regel sie ausgewertet wurde — sonst ist sie
    eine Zahlenliste, und die Wahl steckt im Kopf des Ausführers."""
    messung = _messung()
    assert messung["schritt"] == "14.4", "die Messung ist nicht der Schritt 14.4"
    assert messung.get("regel"), "die Tabelle trägt keine Regel der Wahl"
    assert "Stabilitaet" in messung["regel"], "die Regel nennt die Stabilitaet nicht"
    assert "Marge" in messung["regel"], "die Regel nennt die Trennungs-Marge nicht"
    startwerte = messung.get("startwerte") or {}
    for name in KONSTANTEN:
        assert name in startwerte, f"die Tabelle nennt den Startwert von {name} nicht"
        assert startwerte[name] == _konstante_aus_graph(name), (
            f"der Startwert von {name} in der Tabelle ({startwerte[name]}) weicht vom Code ab "
            f"({_konstante_aus_graph(name)})")


def test_every_constant_has_been_measured():
    """Jede der zehn Konstanten braucht **mehrere** gemessene Werte — ein einzelner Messwert
    ist keine Messung, sondern ein Befund."""
    gruppen = _varianten_je_konstante(_messung())
    for name in KONSTANTEN:
        assert name in gruppen, f"die Konstante {name} wurde nicht gemessen"
        assert len(gruppen[name]) >= 3, (
            f"die Konstante {name} hat nur {len(gruppen[name])} gemessene Werte")


def test_the_value_in_the_code_is_the_one_the_measurement_picks():
    """**Der Wert im Code ist der gemessene.** Für jede Konstante wählt die Regel aus der
    Tabelle genau einen Wert aus — und dieser muss der sein, der in `graph.js` steht."""
    messung = _messung()
    gruppen = _varianten_je_konstante(messung)
    for name in KONSTANTEN:
        code_wert = _konstante_aus_graph(name)
        werte = gruppen[name]
        assert code_wert in werte, (
            f"der Wert {code_wert} der Konstante {name} steht nicht in der Messung")
        stabil = {w: e for w, e in werte.items() if _stabil(e)}
        assert stabil, f"kein gemessener Wert der Konstante {name} hält die Stabilitaet"
        best = max(stabil.values(),
                   key=lambda e: _zellen(e)["regionen_marge_min_px"])
        assert best["konstanten"][name] == code_wert, (
            f"die Regel wählt für {name} den Wert {best['konstanten'][name]}, im Code steht "
            f"{code_wert} — der Kommentar 'gemessen in 14.4' wäre eine Behauptung")


def test_every_other_value_is_measurably_worse():
    """**Die Messung unterscheidet.** Jeder *andere* gemessene Wert derselben Konstante ist
    entweder **nicht stabil** oder hat eine **kleinere** Marge.

    Ohne diese Prüfung könnte die Tabelle auch dann „beweisen", wenn alle Werte gleich
    gemessen wären — das wäre kein Beleg, sondern eine Zufallsübereinstimmung."""
    messung = _messung()
    gruppen = _varianten_je_konstante(messung)
    for name in KONSTANTEN:
        code_wert = _konstante_aus_graph(name)
        werte = gruppen[name]
        marge_best = _zellen(werte[code_wert])["regionen_marge_min_px"]
        for wert, eintrag in werte.items():
            if wert == code_wert:
                continue
            if _stabil(eintrag):
                assert _zellen(eintrag)["regionen_marge_min_px"] < marge_best, (
                    f"der Wert {wert} der Konstante {name} ist stabil und hat die gleiche oder "
                    f"eine groessere Marge ({_zellen(eintrag)['regionen_marge_min_px']} gegen "
                    f"{marge_best}) — der gewaehlte Wert ist dann nicht gemessen, sondern geraten")
            else:
                assert True, (  # pragma: no cover — der Zweig ist der Beweis
                    f"der Wert {wert} der Konstante {name} haelt die Stabilitaet nicht "
                    f"(Median {_zellen(eintrag)['stabilitaet_median_px']} px, Maximum "
                    f"{_zellen(eintrag)['stabilitaet_max_px']} px)")


def test_the_measured_values_are_the_ones_the_server_served():
    """**Der Beweis, dass der Patch gewirkt hat:** für jede Variante nennt die Tabelle den
    Wert, den der Server **tatsächlich** ausgeliefert hat (`gesendet`). Er muss der
    gepatchte sein — sonst hätte die Messung den *ungepatchten* Code gemessen."""
    messung = _messung()
    for label, eintrag in messung["varianten"].items():
        gesendet = eintrag.get("gesendet") or {}
        for name, wert in (eintrag.get("konstanten") or {}).items():
            assert gesendet.get(name) == wert, (
                f"die Variante {label} sollte {name}={wert} ausliefern, hat aber "
                f"{gesendet.get(name)} serviert")


def test_the_normalfall_beleg_names_the_constants_that_were_served():
    """Der **Normalfall-Beleg** der Browser-Probe nennt die ausgelieferten Werte — sie
    müssen mit dem Code übereinstimmen. Das ist die Brücke zwischen der Messung und dem
    Produktcode: ohne sie wäre die Tabelle eine Behauptung über einen Zustand, den niemand
    gesehen hat."""
    assert BELEG.exists(), f"der Beleg fehlt: {BELEG}"
    beleg = json.loads(BELEG.read_text(encoding="utf-8"))
    gesendet = beleg.get("konstanten_gesendet") or {}
    assert gesendet, "der Normalfall-Beleg nennt keine ausgelieferten Konstanten"
    for name in KONSTANTEN:
        assert gesendet.get(name) == _konstante_aus_graph(name), (
            f"der Beleg hat {name}={gesendet.get(name)} ausgeliefert, im Code steht "
            f"{_konstante_aus_graph(name)}")
