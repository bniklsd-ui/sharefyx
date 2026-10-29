"""Der **Beleg** der Block-14-Probe: `p105_b14_layout_probe.json` steht im Repo, und die
Zellen tragen den **Stand des Schritts 14.35** (die Beschriftungen).

**Warum ein Wächter und nicht nur eine Notiz.** Die Probe fährt gegen eine Wegwerf-Instanz;
was sie misst, landet als JSON im Repo. Eine JSON-Datei im Repo ist aber nur so viel wert wie
die Aussage, die man über sie macht — und die Aussage („die Regionen sind getrennt, die
Stabilität hält, das Budget reißt nicht, die Beschriftungen überlappen sich nicht") steht
sonst nirgends im Code. Dieser Wächter bindet sie an den Plan: **welche Zelle ab welchem
Schritt grün sein muss**, steht in
`docs/concepts/phase10_5_block14_kartenlayout_plan.md` §4.

**Der Wächter ist ein Schloss auf den Fortschritt, kein Urteil.** Er sagt: „Stand 14.35 =
diese Zellen sind grün." Wird eine Zelle im nächsten Schritt rot, wird **hier** die Menge der
roten Zellen größer — und genau diese Änderung steht im Diff. Wäre der Wächter statisch,
würde ein Schritt, der eine Zelle kaputtmacht, unauffällig durchrutschen.

| Schritt (Plan §4) | was grün werden muss |
|---|---|
| 14.0 (Basislinie) | `determinismus`, `budget` — die anderen vier sind **rot** (Basislinie) |
| 14.1 | `determinismus` bleibt grün (L1–L3) — die vier roten Zellen bleiben rot, **aber ihre Zahlen wandern** |
| 14.2 | `regionen` **und** `stabilitaet` werden grün (L4: Anker-Gravitation, Querfedern, `ALPHA_START_SEEDED`) — `kamera` (14.3) und `beschriftungen` (14.35) bleiben rot |
| 14.3 | `kamera` wird grün (`fitView()`) — `beschriftungen` bleibt rot (14.35) |
| **14.35 (dieser Stand)** | `beschriftungen` wird grün (§2.7: die Kollisionsprüfung) — **alle sechs Zellen grün** |
| 14.4 | alle Zellen grün + jeder Gegenlauf rot an genau seiner Zelle |

**Die Zahlen sind mitgeprüft, nicht nur die `ok`-Flags** (der Test
`test_the_measured_numbers_are_the_ones_the_cells_stand_on`): ein Schritt, der eine Zelle
kaputtmacht, muss die Zahlen mitnehmen — sonst würde der Wächter die Bewegung der Zahlen
übersehen. Die Zahlen der Basislinie (14.0), des Stands 14.1, 14.2, 14.3 und 14.35 stehen
alle im Diff dieser Datei — **datiert**, weil sich der Code geändert hat.

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

#: **Stand 14.4** — die **Startwerte gemessen** (Plan §2.1/§2.4: "Startwerte, durch Messung in
#: 14.4 justiert", "in 14.4 werden sie **gemessen** (nicht gesetzt)"). **Alle sechs Zellen sind
#: grün**, und der **fehlende Gegenlauf** für die Regions-Zelle ist geschlossen (`region`).
ROT = set()
GRUEN = {"determinismus", "regionen", "kamera", "stabilitaet", "budget", "beschriftungen"}

#: **Datierter Stand** — die Basislinie (14.0) war rot in `regionen`, `kamera`, `stabilitaet`
#: und `beschriftungen`; 14.1 hat nur die Zahlen bewegt; **14.2** hat `regionen` (57,2 % → 82,2 %
#: → **100 %**) und `stabilitaet` (Median 327,9 px → 233 px → **0,0 px**) gruen gemacht;
#: **14.3** hat `kamera` gruen gemacht (Füllgrad **93,6 %**, Versatz **32,3 px → 0,42 px** —
#: **[datierte Änderung 2026-10-28, Schritt 14.5: der Rand ist von 40 auf 56 px gewachsen**
#: (die Lappen-Kontur stand sonst **3,8 px** über dem Leinwandrand), damit sind es jetzt
#: **91,1 %** und **0,49 px**);
#: **14.35** hat `beschriftungen` gruen gemacht (**5** ueberlappende Paare → **0**, **3** von
#: **13** Beschriftungen weggelassen); **14.4** hat die **Startwerte gemessen** (alle vier
#: bestätigt) und den **Gegenlauf** `region` gebracht.
STAND = "14.4"


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
#: | `beschriftung` | `beschriftungen` | die **Kollisionsprüfung** der Beschriftungen (§2.7) |
#: | `region` | `regionen` | **eine Region je Space** (§2.1 L1) — der zweite Space bekommt keine eigene |
#:
#: **`zentrum` macht keine Zelle rot** — das ist ein *Befund*, kein Fehler des Beleugs: die
#: Anker-Gravitation ist **nicht** die Regel, die die Regionen-Zelle misst (sie misst die
#: **Trennung** der Regionen; die trennen schon die Querfedern). Ihre messbare Wirkung ist die
#: **Weltgröße**: die Welt ist **779 px** breit statt 1148 px, und der Füllgrad der Kamera
#: fällt von **91,1 %** auf **68,8 %** (der Wert 93,6 % galt mit dem Rand von 40 px —
#: **[datiert 2026-10-28, Schritt 14.5]**). Die Zuordnung im Plan §5 ("`ANCHOR_GRAVITY` →
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
#:
#: **[Datierte Ergänzung 2026-10-27, Schritt 14.35] `beschriftung` (neu).** Der Gegenlauf
#: patcht die **Kollisionsprüfung** (`graph.js :: labelRectOverlaps()`) — nicht ihren Aufrufer.
#: **Gemessen:** **13** Beschriftungen gezeichnet, **0** weggelassen, **5** überlappende Paare —
#: das ist der Stand von 14.2 (und von 14.3), die Zelle `beschriftungen` ist **rot**, alle
#: anderen bleiben grün. Der Pixel-Vergleich des Standes 14.2 fand **4** Paare — er zählte
#: eines nicht mit (zwei überlappende Rechtecke teilen sich ihre Pixel); der Recorder zählt
#: die Paare **aus den Rechtecken**, nicht aus den Pixeln.
#:
#: **[Datierte Ergänzung 2026-10-27, Schritt 14.4] `region` (neu) — der Gegenlauf, der die
#: Lücke schließt.** Der Plan §5 nannte für **P10.5-66** den Gegenlauf "`ANCHOR_GRAVITY` →
#: Leinwandmitte" — **gemessen** lässt der keine Zelle rot werden (er wirkt auf die
#: **Weltgröße**). `region` bricht die Regel, die die Zelle tatsächlich misst: **eine Region je
#: Space** (§2.1 L1) — alle Anker liegen auf **einem** Punkt, es gibt nur noch **eine**
#: Region (derselbe Gegenlauf wie im Seed-Harness `anker`).
#:
#: **Er macht *drei* Zellen rot** — und das ist **gemessen und begründet**: der Fehler ist der
#: **Stand von 14.0** (die Spaces haben keine eigenen Regionen), und der bringt genau die drei
#: roten Zellen der Basislinie zurück: `regionen` (92,1 % statt 95 %), `kamera` (die Welt ist
#: ein **642 × 485 px** großer Klumpen ⇒ Füllgrad **56,6 %** < 60 %) und `stabilitaet` (Median
#: **278 px** — ein Klumpen ist wackelig). Die **Beschriftungs**-Zelle bleibt grün: die
#: Kollisionsprüfung (14.35) wirkt auch im Klumpen.
#:
#: **Warum nicht *ein* Space (gemessen, Schritt 14.4):** die Browser-Probe misst die
#: **entspannte** Karte, und die Anker-Gravitation **repariert** eine verschobene Region — der
#: verschobene Cluster wird von der Repulsion wieder herausgeschoben. Gemessen: der zweite
#: Space bekommt den Anker des eigenen ⇒ die Zelle bleibt bei **100 %** grün (der Cluster liegt
#: **205 px** daneben); verschiebt man nur die Ordner-Inseln, bleiben **97,4 %** bzw. **98,7 %**
#: grün. **Erst wenn kein Space einen eigenen Anker hat, bleiben die Items ineinander.**
#:
#: **[Datierte Änderung 2026-10-29, Plan 14.7.3 — die Karte ist kompakt (Hexgitter, `LOBE_SCALE`
#: 1,5, vom Nikinger abgenommen)]** Die Spaces liegen jetzt **dicht**; jede Störung, die sie
#: zusammenschiebt, kippt die Regionen-Zelle, und die Stabilität ist empfindlicher (Max 9,1 px).
#: Gemessen: `querfeder` → `regionen` + `stabilitaet` (die Kamera bleibt grün, 63,9 %);
#: `zentrum` → `regionen` (93,4 %) + `stabilitaet` — der Gegenlauf, der vorher **keine** Zelle
#: umdrehte, trifft jetzt die Zelle, die der Plan §5 ihm ursprünglich zugedacht hatte.
#: **`region` und `beschriftung` sind neu gebaut** (Nikinger: Befund B (b), „der ehrlichere
#: Test"): der alte `region` sprengte die Karte (±7000 px — Regionen trivial getrennt, Zelle
#: grün), der alte `beschriftung` fand im verteilten Bild keine Überlappung (13 von 13
#: gezeichnet). Der neue `region` vergibt die Regionen per Index-Permutation statt nach Space
#: (57,9 %); `beschriftung` wird in der **Zoomszene** gemessen (Zoom 1,21 — 57 Paare
#: überlappen ohne die Regel, 0 mit ihr; 40 von 152 weggelassen).
GEGENLAEUFE = {
    "querfeder": ("regionen", "stabilitaet"),
    "alpha": ("budget", "stabilitaet"),
    "zentrum": ("regionen", "stabilitaet"),
    "fitview": ("kamera",),
    "beschriftung": ("beschriftungen",),
    "region": ("regionen", "stabilitaet"),
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
    """**Das ist die Aussage des Schritts 14.35:** `beschriftungen` ist grün geworden — alle
    sechs Zellen sind grün."""
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
    # **[Neu, 2026-10-27, Schritt 14.4] Die **Marge** — der Spielraum der Trennung.** Die
    # Zelle prüft nur, ob der eigene Schwerpunkt der *nächste* ist; die Marge sagt, **wie
    # viel** Spielraum die Trennung hat (der kleinste Abstand „eigener Schwerpunkt minus
    # nächster fremder" über alle Knoten). Ohne sie wäre die Zelle grün, obwohl die Regionen
    # sich schon fast berühren — und die Wahl der Startwerte (§2.1) stünde auf keinem
    # Boden. Der Gegenlauf `region` dreht sie ins Negative (das ist der Beweis, dass sie
    # misst).
    # **[Datierte Änderung 2026-10-29, Plan 14.7.3 — Befund A, vom Nikinger akzeptiert]**
    # vorher `> 100 px` (Block 14: 171,8 px). Die kompakte Karte legt die Lappen aneinander,
    # die Marge ist **21,8 px** — der Tausch Marge gegen Kompaktheit ist abgenommen; der
    # Wächter verlangt jetzt nur noch eine **positive** Marge (die Regionen sind getrennt).
    assert reg["marge_min_px"] > 0.0, (
        "die Regionen sind nicht mehr getrennt — ein Knoten liegt naeher am fremden Space")
    assert reg["marge_median_px"] > reg["marge_min_px"], "die Marge ist nicht monoton"
    # **Die Dichte** (Schritt 14.4): die Items liegen **dicht, aber nicht uebereinander**
    # (Plan §2.3) — der kleinste Abstand zwischen zwei Knoten und die Zahl der Paare, deren
    # Kreise sich ueberlappen.
    assert reg["engster_abstand_px"] > 8.0, "zwei Items liegen zu dicht beieinander"
    assert reg["ueberlappende_paare"] <= 5, (
        "zu viele Item-Kreise ueberlappen sich — der Seed ist zu eng")

    # Stabilitaet (P10.5-68): die Knoten **anderer** Spaces stehen still, und das neue Item
    # liegt in der Region seines Space.
    # **[Datierte Korrektur 2026-10-26, Schritt 14.2]:** die Basislinie (14.0) trug einen
    # Median von **327,9 px**, der Stand 14.1 noch **233 px** — jetzt **0,0 px** (max. 2,24 px).
    stab = m["stabilitaet"]
    assert stab["median_verschiebung_px"] <= 2.0
    # **[Datierte Änderung 2026-10-29, Plan 14.7.3 — E1, vom Nikinger mit dem Bild
    # abgenommen]** vorher `<= 3,0` (Block 14: 2,2 px); die kompakte Karte misst **9,1 px**.
    # Die Abnahmezeile P10.5-68 verlangt nur den Median; die Obergrenze hier hält den
    # abgenommenen Stand fest, damit eine weitere Verschlechterung auffällt.
    assert stab["max_verschiebung_px"] <= 10.0
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
    # Umriss **32,3 px** neben der Mitte (Zoom 100 %) — jetzt sind es **0,49 px** (Zoom 90 %).
    # **[Datierte Änderung 2026-10-28, Schritt 14.5]:** mit dem Rand von 56 px (vorher 40 px)
    # sind es **0,49 px** bei **90 %** Zoom statt **0,42 px** bei **92 %** — der Rand ist
    # gewachsen, weil die **Lappen-Kontur** mit eingepasst werden muss (Plan §2.5).
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

    # Beschriftungen (P10.5-71): **keine** zwei gezeichneten Rechtecke ueberlappen sich, die
    # Fokus-Beschriftung ist **da** (am Pixel bewiesen) — und die Regel hat **wirklich**
    # gewirkt: es wurde eine Beschriftung weggelassen.
    # **[Datierte Aenderung 2026-10-26, Schritt 14.35]:** vorher stand hier `len(...) >= 1`
    # (die Basislinie hatte Ueberlappungen). Jetzt sind es **null** — und der Beleg muss
    # **zeigen**, dass die Regel gegriffen hat: ohne weggelassene Beschriftung waere die Zelle
    # auch ohne die Regel gruen (der Gegenlauf `beschriftung` beweist das Gegenteil).
    bes = m["beschriftungen"]
    assert bes["fokus_beschriftung"] is True, "die Fokus-Beschriftung fehlt"
    assert bes["fokus_pixel"] > 0, "die Fokus-Beschriftung steht nicht auf der Leinwand"
    assert bes["gezeichnet"] >= 2, "es sind genug Beschriftungen gezeichnet worden"
    assert len(bes["ueberlappungen"]) == 0, (
        f"gezeichnete Beschriftungen ueberlappen sich: {bes['ueberlappungen']}")
    # **[Datierte Änderung 2026-10-29, Plan 14.7.3 — Befund B (b)]** In der Fokusszene der
    # verteilten Karte überlappt **nichts** (13 von 13 gezeichnet) — die Regel hätte dort
    # nichts zu tun. Bewiesen wird sie in der **Zoomszene** (Zoom ≥ 1,2: jeder Knoten ist
    # Kandidat, gezeichnet werden alle Titel — also ist die Zahl der Kandidaten die Knotenzahl).
    zs = bes["zoomszene"]
    assert zs["zoom"] is not None and zs["zoom"] >= 1.2, "die Zoomszene liegt unter der Schwelle"
    assert zs["ueberlappende_paare"] == 0, (
        f"in der Zoomszene ueberlappen sich Beschriftungen: {zs['ueberlappungen']}")
    assert zs["gezeichnet"] >= 2, "in der Zoomszene sind zu wenige Beschriftungen gezeichnet"
    assert SEED_SUMME - zs["gezeichnet"] >= 1, (
        "es wurde **keine** Beschriftung weggelassen — die Kollisionspruefung hat nicht "
        "gegriffen, die Zelle waere auch ohne die Regel gruen")
    assert bes["kandidaten"] == bes["gezeichnet"] + bes["unterdrueckt"], (
        "die Zahl der Kandidaten passt nicht zu den gezeichneten und den weggelassenen")
    assert bes["nachbarn"] >= 5, "der Fokus-Knoten hat mindestens fuenf Nachbarn (Plan §5)"

    # Budget (P10.5-69): 200 Knoten, 3 s, 0 Frames, die Karte ist gemalt
    bud = m["budget"]
    assert bud["knoten"] >= 200
    assert bud["ruhe_ms"] <= 3000
    assert bud["raf_calls_reduced_motion"] == 0
    assert bud["kern_pixel_reduced_motion"] > 0

    # **kein** Seitenfehler: ein Fehler im Graph-Code wuerde die Zellen stumm verfaelschen
    assert beleg["seitenfehler"] == [], f"der Beleg traegt Seitenfehler: {beleg['seitenfehler']}"
    assert beleg["alle_kriterien_erfuellt"] is True, (
        "der Stand 14.35 erfuellt alle Kriterien — wenn hier 'false' steht, traegt der Beleg "
        "eine rote Zelle, die die Bilanz oben nicht zeigt")


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
        # **Stand 14.35: keine Zelle ist ohnehin rot** — der Gegenlauf muss also *genau*
        # seine Zelle treffen, ohne eine andere mitzunehmen.
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
    1148 px, **und** der Füllgrad sinkt von **91,1 %** auf **68,8 %** (die kleinere Welt passt
    auch bei 100 % Zoom nicht mehr ganz in die Leinwand). Vor 14.3 war nur der Füllgrad zu
    sehen (101,2 % → 68,7 %), weil die Kamera nicht einpasste.

    Die Zuordnung im Plan §5 ("`ANCHOR_GRAVITY` → Leinwandmitte" als Gegenlauf der Abnahme
    P10.5-66) ist damit **datiert berichtigt** (2026-10-26)."""
    # **[Datierte Änderung 2026-10-29, Plan 14.7.3]** In der kompakten Karte zieht die
    # Zentrums-Gravitation die Spaces **ineinander**: die Regionen-Zelle kippt (93,4 %), die
    # Welt wird schmaler (717 statt 887 px). Vorher (Block 14, weit gestreute Spaces) blieb
    # jede Zelle grün und nur die Weltgröße zeigte die Wirkung.
    normal = _beleg()["messungen"]
    gegen = _gegenlauf_beleg("zentrum")["messungen"]
    assert gegen["regionen"]["anteil"] < 0.95, (
        "mit der Zentrums-Gravitation liegen Knoten im fremden Space (das ist die Wirkung)")
    breite_normal = normal["kamera"]["welt"]["x1"] - normal["kamera"]["welt"]["x0"]
    breite_gegen = gegen["kamera"]["welt"]["x1"] - gegen["kamera"]["welt"]["x0"]
    assert breite_gegen < breite_normal * 0.85, (
        "mit der Zentrums-Gravitation ist die Welt schmaler (das ist die Wirkung der Regel)")


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


def test_the_gegenlauf_beschriftung_makes_the_labels_red_and_nothing_else():
    """**Der Gegenlauf zu P10.5-71:** die **Kollisionspruefung** der Beschriftungen ist aus —
    die ueberlappenden Beschriftungen werden wieder **alle** gezeichnet.

    Ohne diesen Gegenlauf waere die Beschriftungs-Zelle ein Wächter, der nichts prueft: die
    Zelle waere auch dann gruen, wenn die Regel gar nicht existierte (die Kandidaten der
    Probe ueberlappen sich in dieser Karte von Natur aus). Der Gegenlauf stellt **genau die**
    Zelle rot — die anderen fuenf bleiben gruen."""
    beleg = _gegenlauf_beleg("beschriftung")
    zellen = _zellen(beleg)
    rot = {zelle for zelle, ok in zellen.items() if not ok}
    neu_rot = rot - ROT
    assert neu_rot == {"beschriftungen"}, (
        f"der Gegenlauf `beschriftung` macht {sorted(neu_rot)} neu rot — erwartet "
        "['beschriftungen']")
    bes = beleg["messungen"]["beschriftungen"]
    # **Die Zahlen**: ohne die Regel werden **alle** Kandidaten gezeichnet (keiner weggelassen)
    # und die Rechtecke ueberlappen sich wieder.
    assert bes["unterdrueckt"] == 0, "ohne die Kollisionspruefung wurde nichts weggelassen"
    assert bes["gezeichnet"] == bes["kandidaten"], (
        "ohne die Kollisionspruefung wurde nicht jede Beschriftung gezeichnet")
    # **[2026-10-29, Plan 14.7.3]** der Fehler zeigt sich in der **Zoomszene** (die Fokusszene
    # der verteilten Karte hat nichts zu kollidieren): ohne die Regel ueberlappen **57** Paare.
    assert bes["zoomszene"]["ueberlappende_paare"] >= 1, (
        "ohne die Kollisionspruefung ueberlappen sich die Rechtecke nicht — der Gegenlauf "
        "stellt den Fehler nicht wieder her")


def test_the_gegenlauf_region_makes_the_regionen_cell_red():
    """**Der Gegenlauf zu P10.5-66** (Schritt 14.4): alle Anker liegen auf **einem** Punkt —
    es gibt **nur noch eine Region** statt einer je Space.

    **Das ist der Gegenlauf, der die Lücke schließt.** Der Plan §5 nannte für P10.5-66 den
    Gegenlauf "`ANCHOR_GRAVITY` → Leinwandmitte" — **gemessen** lässt der *keine* Zelle rot
    werden (er wirkt auf die Weltgröße). Ohne einen wirksamen Gegenlauf wäre die
    Regions-Zelle ein Wächter, der nichts prüft: sie wäre auch dann grün, wenn die Regel
    „eine Region je Space" gar nicht existierte.

    **Er macht *drei* Zellen rot — und das ist gemessen und begründet:** der Fehler ist der
    **Stand von 14.0** (keine eigenen Regionen), und der bringt die drei roten Zellen der
    Basislinie zurück: `regionen`, `kamera` (die Welt ist ein Klumpen ⇒ Füllgrad < 60 %) und
    `stabilitaet` (ein Klumpen ist wackelig). Die **Beschriftungs**-Zelle bleibt grün — die
    Kollisionsprüfung wirkt auch im Klumpen."""
    beleg = _gegenlauf_beleg("region")
    zellen = _zellen(beleg)
    rot = {zelle for zelle, ok in zellen.items() if not ok}
    neu_rot = rot - ROT
    # **[2026-10-29, Plan 14.7.3]** neuer Gegenlauf (Regionen per Index-Permutation statt nach
    # Space): **kein Klumpen** mehr — die Kamera bleibt grün (75,2 %), es kippen die Regionen
    # und (als Folge der gemischten Regionen) die Stabilität.
    assert neu_rot == {"regionen", "stabilitaet"}, (
        f"der Gegenlauf `region` macht {sorted(neu_rot)} neu rot — erwartet "
        "['regionen', 'stabilitaet']")
    reg = beleg["messungen"]["regionen"]
    # **Die Zahlen**: die Items liegen ineinander -- ihr Anteil am richtigen Schwerpunkt bricht
    # ein, und die **Marge** (der Spielraum der Trennung) ist negativ: die Regionen sind nicht
    # mehr getrennt.
    assert reg["anteil"] < 0.95, (
        "ohne eigene Regionen liegt ein Space nicht mehr bei seinem eigenen Schwerpunkt")
    assert reg["richtig"] < reg["knoten"], "es muss Knoten geben, die im fremden Space liegen"
    assert reg["marge_min_px"] < 0, (
        "die Trennung der Regionen ist nicht mehr da — die Marge muss negativ sein")
    assert len(reg.get("beispiele_falsch") or []) >= 1, (
        "der Beleg muss zeigen, welche Knoten im fremden Space liegen")
    # **Die beiden Folge-Zellen** sind Konsequenzen desselben Fehlers (der Klumpen) — sie
    # werden hier festgehalten, damit eine Änderung an ihnen auffällt.
    stab = beleg["messungen"]["stabilitaet"]
    assert stab["median_verschiebung_px"] > 2.0, "gemischte Regionen sind wackelig"



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


def test_a_beleg_with_overlapping_labels_would_be_rejected(tmp_path, monkeypatch):
    """Die **sechste** Gegenprobe (2026-10-26, Schritt 14.35): ein Beleg, in dem die
    gezeichneten Beschriftungs-Rechtecke sich wieder **ueberlappen** (ohne das `ok`-Feld zu
    beruehren), muss den Wächter rot machen.

    Das ist die Fehlerklasse, die dieser Ordner schon zweimal getroffen hat: das `ok`-Flag
    wird umgeschaltet, die **Zahl** bleibt stehen. Der Wächter prueft die Zahlen — ein Beleg
    mit `ueberlappungen: []` und einem Paar waere ein Witz."""
    beleg = _beleg()
    beleg["messungen"]["beschriftungen"]["ueberlappungen"] = [["Gamma Plan 01", "Gamma Frage 04"]]
    gefaelscht = tmp_path / "p105_b14_layout_probe.json"
    gefaelscht.write_text(json.dumps(beleg), encoding="utf-8")
    monkeypatch.setattr(sys.modules[__name__], "BELEG", gefaelscht)
    with pytest.raises(AssertionError):
        test_the_measured_numbers_are_the_ones_the_cells_stand_on()


def test_a_beleg_without_a_suppressed_label_would_be_rejected(tmp_path, monkeypatch):
    """Die **siebte** Gegenprobe (2026-10-26, Schritt 14.35): ein Beleg, in dem **keine**
    Beschriftung weggelassen wurde, muss den Wächter rot machen.

    Sonst waere die Zelle auch dann gruen, wenn die Kollisionspruefung gar nicht existierte —
    die Zelle wuerde die Regel nicht messen, sondern nur behaupten. Der Gegenlauf
    `beschriftung` beweist die Regel von der anderen Seite; diese Gegenprobe beweist, dass
    der Waechter sie von der Belegseite her prueft."""
    beleg = _beleg()
    # [2026-10-29, Plan 14.7.3] die Regel wird in der **Zoomszene** bewiesen — gefaelscht wird
    # dort: alle 152 Titel gezeichnet, keiner weggelassen.
    beleg["messungen"]["beschriftungen"]["zoomszene"]["gezeichnet"] = SEED_SUMME
    gefaelscht = tmp_path / "p105_b14_layout_probe.json"
    gefaelscht.write_text(json.dumps(beleg), encoding="utf-8")
    monkeypatch.setattr(sys.modules[__name__], "BELEG", gefaelscht)
    with pytest.raises(AssertionError):
        test_the_measured_numbers_are_the_ones_the_cells_stand_on()
