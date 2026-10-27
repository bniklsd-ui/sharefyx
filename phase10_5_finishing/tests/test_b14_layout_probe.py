"""Der **Beleg** der Block-14-Probe: `p105_b14_layout_probe.json` steht im Repo, und die
Zellen tragen den **Stand des Schritts 14.3** (die Kamera).

**Warum ein Wächter und nicht nur eine Notiz.** Die Probe fährt gegen eine Wegwerf-Instanz;
was sie misst, landet als JSON im Repo. Eine JSON-Datei im Repo ist aber nur so viel wert wie
die Aussage, die man über sie macht — und die Aussage („die Regionen sind getrennt, die
Stabilität hält, das Budget reißt nicht") steht sonst nirgends im Code. Dieser Wächter bindet
sie an den Plan: **welche Zelle ab welchem Schritt grün sein muss**, steht in
`docs/concepts/phase10_5_block14_kartenlayout_plan.md` §4.

**Der Wächter ist ein Schloss auf den Fortschritt, kein Urteil.** Er sagt: „Stand 14.2 =
diese Zellen sind grün, diese sind rot." Wird eine Zelle im nächsten Schritt grün, wird
**hier** die Menge der roten Zellen kleiner — und genau diese Änderung steht im Diff. Wäre
der Wächter statisch, würde ein Schritt, der eine Zelle kaputtmacht, unauffällig durchrutschen.

| Schritt (Plan §4) | was grün werden muss |
|---|---|
| 14.0 (Basislinie) | `determinismus`, `budget` — die anderen vier sind **rot** (Basislinie) |
| 14.1 | `determinismus` bleibt grün (L1–L3) — die vier roten Zellen bleiben rot, **aber ihre Zahlen wandern** |
| 14.2 | `regionen` **und** `stabilitaet` werden grün (L4: Anker-Gravitation, Querfedern, `ALPHA_START_SEEDED`) — `kamera` (14.3) und `beschriftungen` (14.35) bleiben rot |
| **14.3 (dieser Stand)** | `kamera` wird grün (`fitView()`) — `beschriftungen` bleibt rot (14.35) |
| 14.35 | `beschriftungen` wird grün (§2.7) |
| 14.4 | **alle** grün + jeder Gegenlauf rot an genau seiner Zelle |

**Die Zahlen sind mitgeprüft, nicht nur die `ok`-Flags** (der Test
`test_the_measured_numbers_are_the_ones_the_cells_stand_on`): ein Schritt, der eine Zelle
kaputtmacht, muss die Zahlen mitnehmen — sonst würde der Wächter die Bewegung der Zahlen
übersehen. Die Zahlen der Basislinie (14.0), des Stands 14.1, 14.2 und 14.3 stehen alle
im Diff dieser Datei — **datiert**, weil sich der Code geändert hat.

**Die Gegenläufe sind Belege im Repo** (`p105_b14_layout_probe_gegenlauf_*.json`): die
Browser-Probe ist zu langsam für die Testsuite (rund eine Minute je Lauf), also fährt sie
**hier nicht** — der Wächter prüft die **Belegdateien**. Jeder Gegenlauf patcht **eine**
Regel in einer **Kopie** der statischen Dateien (der Arbeitsbaum bleibt unberührt) und muss
**genau die** zugehörige Zelle rot machen.

**Gegenprobe:** derselbe Wächter muss an einem **manipulierten** Beleg rot werden — und die
Gegenprobe ruft **dieselbe Testfunktion** auf (nicht eine nachgebaute Logik: ein Wächter, der
etwas anderes prüft als er behauptet, ist die Fehlerklasse, die hier verhindert wird).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
BELEG = REPO_ROOT / "phase10_5_finishing" / "probes" / "p105_b14_layout_probe.json"
GRAPH_JS = REPO_ROOT / "phase5_ui" / "webui" / "static" / "js" / "graph.js"

#: Die Zellen der Probe (Plan §5, Abnahme P10.5-65–71).
ZELLEN = {
    "determinismus": "P10.5-65",
    "regionen": "P10.5-66",
    "kamera": "P10.5-67",
    "stabilitaet": "P10.5-68",
    "budget": "P10.5-69",
    "beschriftungen": "P10.5-71",
}

#: **Stand 14.3** — die Kamera. Grün: `determinismus`, `regionen`, `kamera`, `stabilitaet`,
#: `budget`. Rot: `beschriftungen` (das ist 14.35).
ROT = {"beschriftungen"}
GRUEN = {"determinismus", "regionen", "kamera", "stabilitaet", "budget"}

#: **Datierter Stand** — die Basislinie (14.0) war rot in `regionen`, `kamera`, `stabilitaet`
#: und `beschriftungen`; 14.1 hat nur die Zahlen bewegt; **14.2** hat `regionen` (57,2 % → 82,2 %
#: → **100 %**) und `stabilitaet` (Median 327,9 px → 233 px → **0,0 px**) gruen gemacht;
#: **14.3** hat `kamera` gruen gemacht (Füllgrad **93,6 %**, Versatz **32,3 px → 0,42 px**).
STAND = "14.3"


#: Der **Datensatz** (Plan §5, datierte Abweichung vom 5x30-Seed: `beta` hat 32 Items, damit
#: „der nicht-größte Space" eindeutig ist).
SEED_ITEMS = {"alpha": 30, "beta": 32, "gamma": 30, "delta": 30, "epsilon": 30}
SEED_SUMME = 152

#: Die Gegenläufe und die Zelle, die sie rot machen müssen (Plan §5). **Gemessen** am
#: 2026-10-26 — die Belege stehen als JSON im Repo.
#:
#: | Gegenlauf | Zelle | Regel |
#: |---|---|---|
#: | `querfeder` | `stabilitaet` | die Querfeder ist **schwach und lang** (§2.4) |
#: | `alpha` | `budget` | die Startenergie ist die **gesäte** (§2.4) |
#: | `zentrum` | — | die Gravitation zieht zur Leinwandmitte statt zum eigenen Anker (§2.4) |
#: | `fitview` | `kamera` | die Kamera **passt sich ein** (§2.5) |
#:
#: **`zentrum` macht keine Zelle rot** — das ist ein *Befund*, kein Fehler des Beleugs: die
#: Anker-Gravitation ist **nicht** die Regel, die die Regionen-Zelle misst (sie misst die
#: **Trennung** der Regionen; die trennen schon die Querfedern). Ihre messbare Wirkung ist die
#: **Weltgröße**: die Welt ist **779 px** breit statt 1148 px, und der Füllgrad der Kamera
#: fällt von **93,6 %** auf **68,8 %**. Die Zuordnung im Plan §5 ("`ANCHOR_GRAVITY` →
#: Leinwandmitte" als Gegenlauf der Abnahme P10.5-66) ist damit **datiert berichtigt**
#: (Plan §5, 2026-10-26).
#:
#: **[Datierte Ergänzung 2026-10-26, Schritt 14.3] `querfeder` macht jetzt *zwei* Zellen rot.**
#: Die Querfeder auf „so stark und kurz wie die Feder im Space" zu stellen, lässt die Spaces
#: **zusammenlaufen**: die Welt wird **676 px** breit (statt 1148 px), der Einpass-Zoom ist auf
#: **100 % abgeklemmt** (die Welt passt auch bei 100 % nicht in die Leinwand), und der Füllgrad
#: sinkt auf **59,6 %** — unter die 60-%-Schwelle der Abnahme P10.5-67. Die Kamera-Zelle folgt
#: damit **ihrer** Regel: sie misst, ob die Karte die Leinwand füllt. Das ist **kein** Fehler
#: des Gegenlaufs, sondern eine **zweite, echte** Folge — und die Erwartung hier ist die
#: **Dokumentation** davon.
GEGENLAEUFE = {
    "querfeder": ("stabilitaet", "kamera"),
    "alpha": ("budget", "stabilitaet"),
    "zentrum": (),
    "fitview": ("kamera",),
}


def _zoom_min() -> float:
    """`ZOOM_MIN` aus dem **echten** `graph.js` — nicht hier wiederholt: eine Dublette wäre
    eine stille Abweichung (E3: der Ausführer senkt den Wert, wenn 200 Knoten nicht passen)."""
    quelle = GRAPH_JS.read_text(encoding="utf-8")
    treffer = re.search(r"const ZOOM_MIN = ([0-9.]+);", quelle)
    assert treffer, "ZOOM_MIN steht nicht mehr in graph.js"
    return float(treffer.group(1))


def _beleg() -> dict:
    assert BELEG.exists(), f"der Beleg fehlt: {BELEG}"
    return json.loads(BELEG.read_text(encoding="utf-8"))


def _gegenlauf_beleg(name: str) -> dict:
    pfad = (REPO_ROOT / "phase10_5_finishing" / "probes"
            / ("p105_b14_layout_probe_gegenlauf_%s.json" % name))
    assert pfad.exists(), f"der Gegenlauf-Beleg fehlt: {pfad}"
    return json.loads(pfad.read_text(encoding="utf-8"))


def _zellen(beleg: dict) -> dict[str, bool]:
    messungen = beleg["messungen"]
    return {name: bool(messungen[name].get("ok")) for name in ZELLEN}


def test_the_beleg_has_every_cell():
    """Jede Zelle aus §5 muss im Beleg stehen — eine fehlende Zelle ist keine grüne Zelle,
    sondern eine **nicht gemessene**."""
    messungen = _beleg()["messungen"]
    fehlend = [name for name in ZELLEN if name not in messungen]
    assert not fehlend, f"im Beleg fehlen die Zellen: {fehlend}"


def test_the_stand_is_green_in_exactly_these_cells():
    """**Das ist die Aussage des Schritts 14.3:** `kamera` ist grün geworden, `beschriftungen`
    bleibt rot (das ist 14.35)."""
    zellen = _zellen(_beleg())
    rot = {name for name, ok in zellen.items() if not ok}
    gruen = {name for name, ok in zellen.items() if ok}
    assert rot == ROT, f"der Stand {STAND} ist rot in {sorted(rot)}, erwartet {sorted(ROT)}"
    assert gruen == GRUEN, f"der Stand {STAND} ist gruen in {sorted(gruen)}, erwartet {sorted(GRUEN)}"


def test_the_beleg_records_the_seed_and_the_measured_numbers():
    """Der Beleg muss den **Datensatz** und die Zahlen nennen, aus denen die Zellen gingen —
    ohne sie ist „grün" eine Behauptung."""
    beleg = _beleg()
    assert beleg["schritt"] == STAND, f"der Beleg ist Schritt {beleg['schritt']}"
    assert beleg["gegenlauf"] is None, "der Normalfall-Beleg traegt keinen Gegenlauf"
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
    `regionen.ok = false` und einem Anteil von 99 % wäre ein Witz. Jede Zelle wird an dem
    Wert geprüft, aus dem sie entschieden wurde."""
    beleg = _beleg()
    m = beleg["messungen"]

    # Determinismus (P10.5-65): beide Laeufe mit derselben Knotenmenge, Abweichung ≤ 1 px
    det = m["determinismus"]
    assert det["gemeinsam"] == det["knoten"] == det["knoten_lauf1"] == SEED_SUMME, (
        "die beiden Laeufe muessen dieselbe Knotenmenge gehabt haben")
    assert det["max_abweichung_px"] <= 1.0

    # Regionen (P10.5-66): **alle** 152 Knoten liegen beim Schwerpunkt ihres Space.
    # **[Datierte Korrektur 2026-10-26, Schritt 14.2]:** die Basislinie (14.0) trug **87**
    # (57,2 %), der Stand 14.1 **125** (82,2 %) — mit der **Anker-Gravitation** (14.2) sind es
    # **152** (100 %).
    reg = m["regionen"]
    assert reg["knoten"] == SEED_SUMME
    assert reg["richtig"] == SEED_SUMME, "jeder Knoten liegt seinem eigenen Space am naechsten"
    assert reg["anteil"] == pytest.approx(1.0, abs=1e-9)

    # Stabilitaet (P10.5-68): die Knoten **anderer** Spaces stehen still, und das neue Item
    # liegt in der Region seines Space.
    # **[Datierte Korrektur 2026-10-26, Schritt 14.2]:** die Basislinie (14.0) trug einen
    # Median von **327,9 px**, der Stand 14.1 noch **233 px** — jetzt **0,0 px** (max. 2,24 px).
    stab = m["stabilitaet"]
    assert stab["median_verschiebung_px"] <= 2.0
    assert stab["max_verschiebung_px"] <= 3.0
    assert stab["in_eigener_region"] is True, "das neue Item gehoert in die Region seines Space"
    assert stab["andere_spaces"] == 122, "122 Knoten der vier anderen Spaces wurden verglichen"
    # **Die beiden Karten muessen verschieden sein** — sonst vergleicht die Zelle eine Karte
    # mit sich (und waere zwangslaufig gruen).
    assert stab["pruefsumme_vorher"] != stab["pruefsumme_nachher"], (
        "die beiden Laeufe haben dieselbe Karte erzeugt — der Vergleich waere sinnlos")

    # **Der frische Lauf muss wirklich frisch sein** (2026-10-26, Schritt 14.2): stand die
    # Ablage schon **vor** der Simulation da, war der Lauf **gepinnt** — die Knoten standen
    # fest, und die Zelle waere zwangslaufig gruen (ein Fehlgruen ohne Aussage). Die Probe
    # liest den Ablage-Zustand unmittelbar nach dem Neuladen und meldet ihn.
    assert stab["pinned_beim_start"] == 0, "der frische Lauf war gepinnt — die Zelle misst nichts"

    # Kamera (P10.5-67): der Inhalt fuellt die Leinwand, passt **in** sie und sitzt in der
    # Mitte. **[Datierte Ergänzung 2026-10-26, Schritt 14.3]:** vor `fitView()` sass der
    # Umriss **32,3 px** neben der Mitte (Zoom 100 %) — jetzt sind es **0,42 px** (Zoom 92 %).
    kam = m["kamera"]
    assert kam["passt"] is True, "der Inhalt passt nicht in die Leinwand"
    assert kam["fuellgrad"] >= 0.60, "der Inhalt fuellt die Leinwand nicht"
    assert kam["zentriert"] is True, "der Umriss sitzt nicht in der Mitte"
    assert kam["versatz_mitte_px"] <= 3.0, "der Umriss sitzt mehr als 3 px neben der Mitte"
    # **Die Messung muss die Aussage tragen koennen:** die Unsicherheit der Kamerabestimmung
    # (Streuung der Pan-Kandidaten + Zoom-Rasterfehler) muss kleiner sein als die Schwelle,
    # auf die geprueft wird — sonst waere „zentriert" eine Behauptung.
    assert kam["unsicherheit_px"] < 3.0, (
        "die Unsicherheit der Kamerabestimmung ist groesser als die 3-px-Schwelle — die "
        "Messung kann die Aussage nicht tragen")
    # **E3 (Plan §2.5):** `ZOOM_MIN` reicht bei 200 Knoten? Der Einpass-Zoom bei **201 Knoten**
    # steht in der Budget-Zelle (`kamera_200_knoten`). Wuerde der Zoom auf `ZOOM_MIN`
    # **abgeklemmt**, stuende er genau auf dem Grenzwert **und** der Inhalt passte nicht mehr
    # in die Leinwand — beides wird hier geprueft.
    kam200 = m["budget"]["kamera_200_knoten"]
    assert kam200["messbar"] is True, "die Kamera bei 200 Knoten liess sich nicht bestimmen"
    assert kam200["passt"] is True, "bei 200 Knoten passt der Inhalt nicht in die Leinwand"
    assert kam200["zentriert"] is True, "bei 200 Knoten sitzt der Umriss nicht in der Mitte"
    assert kam200["zoom"] > _zoom_min(), (
        "der Einpass-Zoom bei 200 Knoten liegt auf `ZOOM_MIN` — der Wert muss gesenkt werden "
        "(E3)")

    # Beschriftungen (P10.5-71): es ueberlappen sich welche, der Fokus ist beschriftet (14.35)
    bes = m["beschriftungen"]
    assert bes["fokus_beschriftung"] is True
    assert bes["gezeichnet"] >= 2, "es sind genug Beschriftungen gezeichnet worden"
    assert len(bes["ueberlappungen"]) >= 1, "die Basislinie hat Ueberlappungen"

    # Budget (P10.5-69): 200 Knoten, 3 s, 0 Frames, die Karte ist gemalt
    bud = m["budget"]
    assert bud["knoten"] >= 200
    assert bud["ruhe_ms"] <= 3000
    assert bud["raf_calls_reduced_motion"] == 0
    assert bud["kern_pixel_reduced_motion"] > 0

    # **kein** Seitenfehler: ein Fehler im Graph-Code wuerde die Zellen stumm verfaelschen
    assert beleg["seitenfehler"] == [], f"der Beleg traegt Seitenfehler: {beleg['seitenfehler']}"
    assert beleg["alle_kriterien_erfuellt"] is False, (
        "der Stand kann noch nicht alle Kriterien erfuellen — `beschriftungen` ist die Aufgabe "
        "von 14.35")


def test_each_gegenlauf_makes_exactly_its_cell_red():
    """**Jeder Gegenlauf macht genau seine Zelle rot** — seine.

    Ein Wächter ohne Gegenlauf beweist nichts: eine Messung, die die falsche Sache misst, ist
    grün und falsch zugleich (diese Fehlerklasse hat dieser Ordner zweimal gesehen). Die
    Erwartung steht je Gegenlauf fest (die Liste ist der Beleg, nicht die Rechnung)."""
    for name, erwartet_rot in GEGENLAEUFE.items():
        beleg = _gegenlauf_beleg(name)
        assert beleg["gegenlauf"] == name, f"der Beleg {name} nennt einen anderen Gegenlauf"
        zellen = _zellen(beleg)
        rot = {zelle for zelle, ok in zellen.items() if not ok}
        # Die Zellen, die **ohnehin** rot sind (die Aufgaben von 14.3 und 14.35), sind kein
        # Fehler des Gegenlaufs -- sie stehen auch im Normalfall rot.
        neu_rot = rot - ROT
        assert neu_rot == set(erwartet_rot), (
            f"der Gegenlauf {name!r} macht {sorted(neu_rot)} neu rot — erwartet "
            f"{sorted(erwartet_rot)}")


def test_the_gegenlauf_zentrum_shows_the_effect_of_the_anchor_gravity():
    """**Der Sonderfall:** der Gegenlauf `zentrum` (die Gravitation zieht zur Leinwandmitte
    statt zum eigenen Space-Anker) macht **keine** Zelle rot — und das ist ein *Befund*, kein
    Fehler des Beleugs.

    Die Anker-Gravitation ist **nicht** die Regel, die die Regionen-Zelle misst: die Zelle
    misst die **Trennung** der Regionen, und die trennen schon die Querfedern (der Gegenlauf
    `querfeder` beweist das an der Stabilitaets-Zelle). Ihre messbare Wirkung ist die
    **Weltgroesse**.

    **[Datierte Ergänzung 2026-10-26, Schritt 14.3]:** seit dem Einpassen der Kamera ist die
    Wirkung an **zwei** Zahlen zu sehen, nicht an einer: die Welt wird **779 px** breit statt
    1148 px, **und** der Füllgrad sinkt von **93,6 %** auf **68,8 %** (die kleinere Welt passt
    auch bei 100 % Zoom nicht mehr ganz in die Leinwand). Vor 14.3 war nur der Füllgrad zu
    sehen (101,2 % → 68,7 %), weil die Kamera nicht einpasste.

    Die Zuordnung im Plan §5 ("`ANCHOR_GRAVITY` → Leinwandmitte" als Gegenlauf der Abnahme
    P10.5-66) ist damit **datiert berichtigt** (2026-10-26)."""
    normal = _beleg()["messungen"]["kamera"]
    gegen = _gegenlauf_beleg("zentrum")["messungen"]["kamera"]
    # **Die eingepasste Kamera** fuellt die Leinwand bis auf den Rand von 40 px (Plan §2.5):
    # `bw / (bw + 2 · FIT_MARGIN)` = 1148 / 1228 = **93,6 %**.
    assert normal["fuellgrad"] > 0.90, "mit der Anker-Gravitation fuellt die Karte die Leinwand"
    assert gegen["fuellgrad"] < normal["fuellgrad"] - 0.2, (
        "mit der Zentrums-Gravitation ist die Welt kleiner (das ist die Wirkung der Regel)")
    breite_normal = normal["welt"]["x1"] - normal["welt"]["x0"]
    breite_gegen = gegen["welt"]["x1"] - gegen["welt"]["x0"]
    assert breite_gegen < breite_normal * 0.8, (
        "mit der Zentrums-Gravitation ist die Welt schmaler (das ist die Wirkung der Regel)")
    assert _zellen(_gegenlauf_beleg("zentrum")) == _zellen(_beleg()), (
        "der Gegenlauf `zentrum` darf keine Zelle umdrehen — er belegt die Wirkung ueber die "
        "Zahlen der Kamera-Zelle")


def test_the_gegenlauf_fitview_makes_the_camera_red_and_nothing_else():
    """**Der Gegenlauf zu P10.5-67:** `fitView()` ist aus — die Kamera passt sich nicht ein.

    Der Beleg muss **genau** die Kamera-Zelle rot machen: die anderen fuenf Zellen bleiben
    gruen. Ohne diesen Gegenlauf waere die Kamera-Zelle ein Wächter, der nichts prueft (eine
    Zelle, die auch ohne die Regel grün waere)."""
    beleg = _gegenlauf_beleg("fitview")
    zellen = _zellen(beleg)
    rot = {zelle for zelle, ok in zellen.items() if not ok}
    neu_rot = rot - ROT
    assert neu_rot == {"kamera"}, (
        f"der Gegenlauf `fitview` macht {sorted(neu_rot)} neu rot — erwartet ['kamera']")
    # **Die Zahlen**: ohne den Einpass sitzt der Umriss wieder **32,3 px** neben der Mitte —
    # der Stand von 14.2. Genau das ist der Fehler, den der Gegenlauf wiederherstellt.
    kam = beleg["messungen"]["kamera"]
    assert kam["versatz_mitte_px"] > 3.0, "der Umriss sitzt nicht mehr neben der Mitte"
    assert kam["zentriert"] is False
    assert kam["zoom_anzeige"] == 1, "ohne den Einpass bleibt der Zoom bei 100 %"


def test_a_manipulated_beleg_would_be_rejected(tmp_path, monkeypatch):
    """Die Gegenprobe: **derselbe Wächter** (also die Testfunktion von oben, nicht eine
    nachgebaute Logik) muss an einem manipulierten Beleg rot werden — sonst prüfte er nichts.
    Der Beleg wird nicht am Objekt verändert, sondern **untergeschoben**: der Wächter liest
    seinen Beleg beim Aufruf."""
    beleg = _beleg()
    beleg["messungen"]["regionen"]["ok"] = False
    gefaelscht = tmp_path / "p105_b14_layout_probe.json"
    gefaelscht.write_text(json.dumps(beleg), encoding="utf-8")
    monkeypatch.setattr(sys.modules[__name__], "BELEG", gefaelscht)
    with pytest.raises(AssertionError):
        test_the_stand_is_green_in_exactly_these_cells()


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


def test_a_pinned_fresh_run_would_be_rejected(tmp_path, monkeypatch):
    """Die vierte Gegenprobe — die **neue** Falle (2026-10-26, Schritt 14.2): ein Beleg, in
    dem der frische Lauf **gepinnt** war (die Ablage stand schon vor der Simulation da), muss
    den Wächter rot machen. Ein gepinnter Lauf bewegt **nichts** — die Stabilitaets-Zelle waere
    zwangslaufig gruen und waere ein Fehlgruen ohne Aussage."""
    beleg = _beleg()
    beleg["messungen"]["stabilitaet"]["pinned_beim_start"] = 152
    gefaelscht = tmp_path / "p105_b14_layout_probe.json"
    gefaelscht.write_text(json.dumps(beleg), encoding="utf-8")
    monkeypatch.setattr(sys.modules[__name__], "BELEG", gefaelscht)
    with pytest.raises(AssertionError):
        test_the_measured_numbers_are_the_ones_the_cells_stand_on()


def test_a_beleg_with_a_shifted_camera_would_be_rejected(tmp_path, monkeypatch):
    """Die fuenfte Gegenprobe (2026-10-26, Schritt 14.3): ein Beleg, in dem der Umriss **nicht
    mehr in der Mitte** sitzt (der Versatz auf 40 px gesetzt, ohne das `ok`-Feld zu beruehren),
    muss den Wächter rot machen.

    Der Versatz ist die **Zahl**, aus der die Zentrierung entschieden wird — ein Beleg mit
    `zentriert: true` und 40 px Versatz waere ein Witz. Genau das hat diese Fehlerklasse in
    diesem Ordner zweimal getroffen."""
    beleg = _beleg()
    beleg["messungen"]["kamera"]["versatz_mitte_px"] = 40.0
    gefaelscht = tmp_path / "p105_b14_layout_probe.json"
    gefaelscht.write_text(json.dumps(beleg), encoding="utf-8")
    monkeypatch.setattr(sys.modules[__name__], "BELEG", gefaelscht)
    with pytest.raises(AssertionError):
        test_the_measured_numbers_are_the_ones_the_cells_stand_on()
