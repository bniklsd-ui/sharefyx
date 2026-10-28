"""Der **Beleg** der Kartenbilder-Probe (Schritt 14.5/14.6.0): `p105_b14_karte_bilder.json`
steht im Repo, die drei Bilder stehen in `docs/screenshots/`.

**Die Zelle `koerper` (Schritt 14.6.0, 2026-10-28).** Der Plan
`docs/concepts/phase10_5_block14_6_plan.md` will aus den **fünf Inseln** **einen Körper**
machen. Die Inseln sind **gemessen**: die Körpermaske reicht `LOBE_REACH` = 48 px um jeden
Knoten, das Layout aus Block 14 stellt die Spaces weit auseinander — die Lappen berühren sich
nie, es gibt **0** Furche-Zellen, und der Körper besteht aus **5** Komponenten. Das ist der
**Befund**, an dem die Zelle hängt: **an der Basislinie ist sie rot** (Plan 14.6 §4,
Schritt 14.6.0: „`koerper` ist **rot** an der Basislinie: **5** Komponenten, **0**
Furche-Zellen").

**Die Zwei-Durchgänge-Regel.** Die Bilder und der Rand kommen aus dem **ungepatchten**
Durchgang, die `koerper`-Zahlen und die Zeit aus dem **gepatchten** (ein Messpflaster in einer
**Kopie** von `graph.js` — kein Haken im Produktcode). Die Bilder im Repo zeigen deshalb
**Produktcode** — und das ist hier **gemessen**: der Lauf vom 2026-10-28 hat die drei Bilder
**byteweise identisch** wieder erzeugt (der Messpflaster-Durchgang ändert das Bild nicht).

**Was der Schritt beweist.** Die drei Bilder zeigen **die** Karte, die in
`p105_b14_layout_probe.json` gemessen wurde (derselbe Saat, dieselbe Wegwerf-Instanz, dieselbe
Ruhe) — und die Messung des **Rand-Falls** aus Plan §2.5 steht daneben: die **Lappen-Kontur**
reicht über den äußersten Knoten hinaus, und die Kamera muss sie **mit** einpassen.

**Der Fall, den dieser Wächter zusätzlich schließt.** Die Kamera-Zelle (P10.5-67) misst den
**Umriss der sichtbaren Knoten** — der Plan §2.5 sagt genau das („Umriss der sichtbaren Knoten
plus `FIT_MARGIN`"). Die **gezeichnete** Kontur der Lappen reicht weiter (bis `LOBE_REACH` =
48 px über dem äußersten Knoten). **Gemessen** (Schritt 14.5, vor der Korrektur): mit einem Rand
von 40 px stand die Kontur **3,8 px über dem Leinwandrand** — die Karte war **beschnitten**,
und keine Zelle hätte es gemerkt. Der Rand ist deshalb **56 px** (die 8 px Luft über der
theoretischen Grenze; der Plan §2.5 nennt diesen Wert). Dieser Wächter prüft beides: dass der
**gezeichnete** Inhalt jetzt **innen** liegt **und** dass die Bilder den **heutigen** Code zeigen.

**Warum die Bilder selbst geprüft werden.** Ein Bild im Repo ist ein Beleg — aber nur, wenn es
das Bild ist, das der Beleg beschreibt. Der Wächter prüft die **Dateien** (Größe, PNG-Format,
Pixelmaße gegen die gemessene Leinwand) und den **gemessenen** Rand.

**Die Gegenproben:** derselbe Wächter muss an einem **manipulierten** Beleg rot werden — die
Gegenprobe ruft **dieselbe** Testfunktion auf (nicht eine nachgebaute Logik: ein Wächter, der
etwas anderes prüft als er behauptet, ist die Fehlerklasse, die dieser Ordner zweimal gesehen
hat).
"""
from __future__ import annotations

import json
import re
import struct
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
BELEG = REPO_ROOT / "phase10_5_finishing" / "probes" / "p105_b14_karte_bilder.json"
BILDER = REPO_ROOT / "docs" / "screenshots"
GRAPH_JS = REPO_ROOT / "phase5_ui" / "webui" / "static" / "js" / "graph.js"

#: Der **Stand**, den der Beleg traegt.
STAND = "14.6.0"

#: Der **Datensatz** (Plan §5, datierte Abweichung vom 5x30-Seed: `beta` hat 32 Items, damit
#: „der nicht-größte Space" eindeutig ist) — derselbe wie in der Layout-Probe.
SEED_ITEMS = {"alpha": 30, "beta": 32, "gamma": 30, "delta": 30, "epsilon": 30}
SEED_SUMME = 152

#: Die **drei** Bilder des Schritts (P10.5-70).
BILDNAMEN = ("p105_b14_karte_01_ganz.png", "p105_b14_karte_02_fokus.png",
             "p105_b14_karte_03_seite.png")

#: Das **Fenster**, in dem die Bilder aufgenommen wurden (das Fenster des Nikingers, 1920 × 1200).
FENSTER = (1920, 1200)

#: Die **Zahl der Inseln an der Basislinie** (Plan 14.6 §0 und §4, Schritt 14.6.0: „**5**
#: Komponenten, **0** Furche-Zellen — das ist der gemessene Befund").
INSELN_BASISLINIE = 5
FURCHE_BASISLINIE = 0

#: Die **Zeitgrenze** fuer `computeLobes()` (Plan 14.6 §2.5: ≤ 50 ms bei 201 Knoten).
ZEITGRENZE_MS = 50.0

#: Die **Knoten**, bei denen die Zeitgrenze gilt.
KNOTEN_FUER_DIE_ZEIT = 201


def _fit_margin() -> float:
    """`FIT_MARGIN` aus dem **echten** `graph.js` — nicht hier wiederholt: eine Dublette wäre
    eine stille Abweichung (derselbe Grund wie bei `ZOOM_MIN`)."""
    quelle = GRAPH_JS.read_text(encoding="utf-8")
    treffer = re.search(r"const FIT_MARGIN = ([0-9.]+);", quelle)
    assert treffer, "FIT_MARGIN steht nicht mehr in graph.js"
    return float(treffer.group(1))


def _beleg() -> dict:
    assert BELEG.exists(), f"der Beleg fehlt: {BELEG}"
    return json.loads(BELEG.read_text(encoding="utf-8"))


def _png_groesse(datei: Path) -> tuple[int, int]:
    """Die **Pixelmaße** eines PNG (der IHDR-Kopf) — ohne Bildbibliothek."""
    kopf = datei.read_bytes()[:24]
    assert kopf[:8] == b"\x89PNG\r\n\x1a\n", f"kein PNG: {datei}"
    return struct.unpack(">II", kopf[16:24])


def test_the_beleg_is_the_stand_14_6_0():
    """**Der Beleg** muss den Schritt, den **Datensatz** und die **Messung** nennen — ohne sie
    ist „grün" eine Behauptung.

    **[Datierte Änderung 2026-10-28, Schritt 14.6.0]** der Beleg traegt jetzt **zwei** Zellen:
    `bilder` (die Bilder und der Rand — grün) und `koerper` (der Koerper — **rot an der
    Basislinie**, Plan 14.6 §4). `alle_kriterien_erfuellt` ist deshalb **false** — und das ist
    die **Aussage**, nicht ein Fehler: der Koerper ist noch nicht gebaut."""
    beleg = _beleg()
    assert beleg["schritt"] == STAND, f"der Beleg ist Schritt {beleg['schritt']}"
    assert beleg["seitenfehler"] == [], f"der Beleg traegt Seitenfehler: {beleg['seitenfehler']}"
    assert beleg["zellen"]["bilder"] is True, "die Bilder-Zelle ist rot — das darf nicht sein"
    assert beleg["zellen"]["koerper"] is False, (
        "die koerper-Zelle ist gruen — die Basislinie ist fuenf Inseln (Plan 14.6 §0)")
    assert beleg["alle_kriterien_erfuellt"] is False, (
        "die Gesamtsumme muss false sein, solange die koerper-Zelle rot ist")
    assert beleg["seed"]["spaces"] == 5, "fuenf Spaces (der 5x30-Seed des Plans)"
    assert beleg["seed"]["items"] == SEED_SUMME, "152 Items (30/32/30/30/30 — siehe Plan §5)"
    assert beleg["seed"]["items_pro_space"] == SEED_ITEMS, "die Aufteilung je Space"
    assert beleg["knoten"]["anzahl"] == SEED_SUMME, "die Karte zeigt alle 152 Knoten"


def test_the_three_images_are_in_the_repo():
    """Die **drei** Bilder des Schritts (P10.5-70) — mit den Pixelmaßen, die der Beleg nennt:
    die zwei Kartenbilder sind die **Leinwand**, das Seitenbild das **Fenster**."""
    beleg = _beleg()
    assert [b["datei"] for b in beleg["bilder"]] == list(BILDNAMEN), (
        "die Bilder des Belegs sind nicht die drei des Schritts")
    leinwand = beleg["leinwand"]
    for bild in beleg["bilder"]:
        datei = BILDER / bild["datei"]
        assert datei.exists(), f"das Bild fehlt im Repo: {datei}"
        assert datei.stat().st_size == bild["bytes"], "die Bildgroesse weicht vom Beleg ab"
        assert bild["bytes"] > 10000, "das Bild ist zu klein (eine leere Flaeche?)"
        breite, hoehe = _png_groesse(datei)
        if bild["datei"].endswith("_seite.png"):
            assert (breite, hoehe) == FENSTER, (
                f"das Seitenbild ist {breite}x{hoehe}, erwartet {FENSTER[0]}x{FENSTER[1]}")
        else:
            assert abs(breite - leinwand["breite"]) <= 1, (
                f"das Kartenbild ist {breite} px breit, die gemessene Leinwand "
                f"{leinwand['breite']}")
            assert abs(hoehe - leinwand["hoehe"]) <= 1, (
                f"das Kartenbild ist {hoehe} px hoch, die gemessene Leinwand "
                f"{leinwand['hoehe']}")


def test_the_drawn_content_is_not_cut_off():
    """**Der Kern des Schritts 14.5:** der **gezeichnete** Inhalt (die Lappen-Kontur) liegt
    **innen**.

    **[Datierte Korrektur 2026-10-28, Schritt 14.5]** die Kamera passt den **Umriss der
    sichtbaren Knoten** ein (Plan §2.5) — die **Lappen-Kontur** reicht aber über den äußersten
    Knoten hinaus (bis `LOBE_REACH` = 48 px). **Gemessen** mit dem alten Rand (40 px): die
    Kontur stand **3,74 px** über dem Leinwandrand (links) und **3,81 px** (rechts) — die
    Karte war **beschnitten**, und die Kamera-Zelle (P10.5-67) hätte es nicht gemerkt. Der Rand
    ist jetzt **56 px** (die 8 px Luft über der theoretischen Grenze)."""
    beleg = _beleg()
    lappen = beleg["lappen"]
    assert lappen["anzahl"] == 5, "es sind nicht fuenf Lappen gezeichnet worden"
    # **Der Filter muss eindeutig sein:** kein *anderer* Strich darf dieselben Werte tragen
    # (Alpha 0,55 / Breite 1,1) — sonst waere "die Lappen-Kontur" nicht gemessen, sondern
    # geraten.
    assert lappen["filter_eindeutig"] is True
    assert lappen["mit_alpha"] == lappen["anzahl"], "ein anderer Strich traegt Alpha 0,55"
    assert lappen["mit_breite"] == lappen["anzahl"], "ein anderer Strich traegt die Breite 1,1"
    # **Der Reach muss gemessen sein** — sonst waere "kein Beschnitt" eine leere Aussage
    # (eine Karte ohne Lappen waere natuerlich unbeschnitten).
    reach = lappen["reach_welt_px"]
    assert max(reach.values()) > 20.0, (
        "die Kontur reicht nicht ueber die Knoten hinaus — der Reach ist nicht gemessen")
    assert min(reach.values()) > 0.0, "die Kontur liegt innerhalb der Knoten — unmoeglich"
    # **Kein Beschnitt:** alle vier Seiten muessen frei sein.
    beschnitt = beleg["beschnitt"]
    assert beschnitt["ja"] is False, f"der gezeichnete Inhalt ist beschnitten: {beschnitt}"
    for seite in ("links", "rechts", "oben", "unten"):
        assert beschnitt[seite] == 0.0, f"die Kontur steht {beschnitt[seite]} px ueber dem Rand"


def test_the_camera_gives_the_margin_it_promises():
    """Die **Kamera** muss den Rand geben, den der Code verspricht — und die Bilder müssen den
    **heutigen** Code zeigen.

    **[Datiert 2026-10-28, Schritt 14.5]** der Rand ist **56 px** (Plan §2.5; der Startwert 40 px
    war der Rand **ohne** die Lappen). Die Prüfung rechnet den Rand aus dem **echten**
    `graph.js` nach (`FIT_MARGIN` × Zoom) — eine Dublette hier wäre eine stille Abweichung."""
    beleg = _beleg()
    margin = _fit_margin()
    zoom = beleg["leinwand"]["zoom"]
    raender = beleg["raender"]
    # **Der kleinste Knoten-Rand** ist der Rand der **begrenzenden** Achse — er muss der
    # versprochene sein (die Ablage rundet auf ganze Pixel: der Messfehler ist ≤ 0,5 px).
    knoten_raender = [raender["knoten_links"], raender["knoten_rechts"],
                      raender["knoten_oben"], raender["knoten_unten"]]
    engster = min(knoten_raender)
    assert abs(engster - margin * zoom) < 1.5, (
        f"der kleinste Knoten-Rand ist {engster:.2f} px, erwartet {margin * zoom:.2f} px "
        f"({margin} px Rand bei Zoom {zoom:.4f})")
    # **Der Lappen-Rand** muss **kleiner** sein als der Knoten-Rand (die Kontur reicht ueber
    # die Knoten hinaus) — **und positiv** (sie liegt innen).
    lappen_raender = [raender["lappen_links"], raender["lappen_rechts"],
                      raender["lappen_oben"], raender["lappen_unten"]]
    assert min(lappen_raender) > 0.0, "die Lappen-Kontur steht ueber dem Leinwandrand"
    assert min(lappen_raender) < engster, (
        "die Lappen-Kontur liegt **innerhalb** des Knoten-Umrisses — der Reach waere nicht "
        "gemessen")
    # **Der Beleg muss den Code nennen, mit dem gemessen wurde** — sonst waeren die Bilder
    # Bilder eines anderen Stands.
    gesendet = beleg["konstanten_gesendet"]
    assert gesendet["FIT_MARGIN"] == str(margin).rstrip("0").rstrip("."), (
        f"der Beleg hat mit FIT_MARGIN {gesendet['FIT_MARGIN']} gemessen, im Code steht {margin}")


def test_a_manipulated_beleg_would_be_rejected(tmp_path, monkeypatch):
    """Die erste Gegenprobe: **derselbe** Wächter (also die Testfunktion von oben, nicht eine
    nachgebaute Logik) muss an einem manipulierten Beleg rot werden — sonst prüfte er nichts."""
    beleg = _beleg()
    beleg["beschnitt"]["ja"] = True
    beleg["beschnitt"]["links"] = 3.7
    gefaelscht = tmp_path / "p105_b14_karte_bilder.json"
    gefaelscht.write_text(json.dumps(beleg), encoding="utf-8")
    monkeypatch.setattr(sys.modules[__name__], "BELEG", gefaelscht)
    with pytest.raises(AssertionError):
        test_the_drawn_content_is_not_cut_off()


def test_a_beleg_without_measured_reach_would_be_rejected(tmp_path, monkeypatch):
    """Die zweite Gegenprobe: ein Beleg **ohne gemessenen Reach** (die Kontur reicht nicht
    ueber die Knoten hinaus) muss rot machen — sonst waere „kein Beschnitt" eine leere Aussage
    (eine Karte ohne Lappen waere natuerlich unbeschnitten)."""
    beleg = _beleg()
    beleg["lappen"]["reach_welt_px"] = {"links": 0.0, "rechts": 0.0, "oben": 0.0, "unten": 0.0}
    gefaelscht = tmp_path / "p105_b14_karte_bilder.json"
    gefaelscht.write_text(json.dumps(beleg), encoding="utf-8")
    monkeypatch.setattr(sys.modules[__name__], "BELEG", gefaelscht)
    with pytest.raises(AssertionError):
        test_the_drawn_content_is_not_cut_off()


def test_a_beleg_with_an_ambiguous_filter_would_be_rejected(tmp_path, monkeypatch):
    """Die dritte Gegenprobe: ein Beleg, in dem **ein anderer** Strich dieselben Werte traegt
    (der Filter ist nicht eindeutig), muss rot machen — sonst waere die Messung nicht die
    Lappen-Kontur, sondern irgendein Strich."""
    beleg = _beleg()
    beleg["lappen"]["filter_eindeutig"] = False
    beleg["lappen"]["mit_alpha"] = 9
    gefaelscht = tmp_path / "p105_b14_karte_bilder.json"
    gefaelscht.write_text(json.dumps(beleg), encoding="utf-8")
    monkeypatch.setattr(sys.modules[__name__], "BELEG", gefaelscht)
    with pytest.raises(AssertionError):
        test_the_drawn_content_is_not_cut_off()


def test_a_beleg_from_another_stand_would_be_rejected(tmp_path, monkeypatch):
    """Die vierte Gegenprobe: ein Beleg, der mit einem **anderen** `FIT_MARGIN` gemessen wurde
    (die Bilder zeigen nicht den heutigen Code), muss rot machen."""
    beleg = _beleg()
    beleg["konstanten_gesendet"]["FIT_MARGIN"] = "40"
    gefaelscht = tmp_path / "p105_b14_karte_bilder.json"
    gefaelscht.write_text(json.dumps(beleg), encoding="utf-8")
    monkeypatch.setattr(sys.modules[__name__], "BELEG", gefaelscht)
    with pytest.raises(AssertionError):
        test_the_camera_gives_the_margin_it_promises()


def test_a_beleg_with_a_page_error_would_be_rejected(tmp_path, monkeypatch):
    """Die fuenfte Gegenprobe: ein **Seitenfehler** im Graph-Code (er wuerde die Messung stumm
    verfaelschen) muss den Wächter rot machen."""
    beleg = _beleg()
    beleg["seitenfehler"] = ["TypeError: n.x is not a function"]
    gefaelscht = tmp_path / "p105_b14_karte_bilder.json"
    gefaelscht.write_text(json.dumps(beleg), encoding="utf-8")
    monkeypatch.setattr(sys.modules[__name__], "BELEG", gefaelscht)
    with pytest.raises(AssertionError):
        test_the_beleg_is_the_stand_14_6_0()


# ============================================================================================
# Die Zelle `koerper` (Schritt 14.6.0) — die Basislinie: **fuenf Inseln**
# ============================================================================================


def test_the_body_is_five_islands_at_the_baseline():
    """**Der gemessene Befund** (Plan 14.6 §0): die Karte ist **fuenf Inseln**, keine Furche.

    Der Koerper besteht aus **5** 4-zusammenhaengenden Komponenten (die Spaces beruehren
    sich nicht), es gibt **0** Furche-Zellen (die Regel hat keinen Gegenstand), und **kein**
    Paar von Spaces liegt an einer Furche. Genau das ist der Befund, an dem die Zelle haengt —
    und genau das macht sie **rot**."""
    koerper = _beleg()["koerper"]
    abnahme = koerper["abnahme"]
    assert abnahme["komponenten"] == INSELN_BASISLINIE, (
        f"der Koerper hat {abnahme['komponenten']} Komponenten — an der Basislinie sind es "
        f"{INSELN_BASISLINIE} (Plan 14.6 §0)")
    assert abnahme["furche_zellen"] == FURCHE_BASISLINIE, (
        f"es gibt {abnahme['furche_zellen']} Furche-Zellen — an der Basislinie gibt es keine")
    assert abnahme["paare_zahl"] == 0, "an der Basislinie beruehren sich keine zwei Spaces"
    assert koerper["ok"] is False, "die koerper-Zelle muss an der Basislinie rot sein"


def test_every_space_has_one_lobe_at_the_baseline():
    """Jeder Space hat **genau einen** Lappen (seine Zellen **ohne** Furche) — auch an der
    Basislinie. Das ist die *andere* Haelfte des Befunds: die Inseln sind **je Space eine**
    (die Zuordnung stimmt), nur der **Koerper** zerfaellt in fuenf Teile."""
    abnahme = _beleg()["koerper"]["abnahme"]
    assert len(abnahme["lappen_je_space"]) == 5, abnahme["lappen_je_space"]
    assert all(v == 1 for v in abnahme["lappen_je_space"].values()), abnahme["lappen_je_space"]


def test_the_compute_lobes_time_is_within_the_limit():
    """**Die Zeitgrenze** (Plan 14.6 §2.5): `computeLobes()` braucht ≤ 50 ms bei 201 Knoten.

    **Gemessen an der Basislinie:** 20,1 ms bei 152 Knoten und **35,0 ms** bei 201 — die
    Grenze ist also kein Selbstgeschaetz: der **heutige** Stand liegt bei zwei Dritteln, und
    das Schliessen kommt **obendrauf** (die Distanztransformation kostet zwei Durchgaenge
    ueber das Raster)."""
    koerper = _beleg()["koerper"]
    zeit = koerper["zeit"]
    assert zeit["knoten"] == KNOTEN_FUER_DIE_ZEIT, (
        "die Zeit wurde bei der falschen Knotenzahl gemessen")
    assert zeit["zeit_ms"] is not None and zeit["zeit_ms"] <= ZEITGRENZE_MS, (
        f"computeLobes() braucht {zeit['zeit_ms']} ms bei {zeit['knoten']} Knoten — die Grenze "
        f"ist {ZEITGRENZE_MS} ms")
    assert koerper["abnahme"]["zeit_ms"] is not None, "die Zeit bei 152 Knoten fehlt"


def test_the_grid_and_the_min_distance_are_measured():
    """Die Zahlen, aus denen sich der **Schliess-Radius** rechnet (Plan 14.6 §3, E1).

    Der kleinste Abstand zweier Knoten verschiedener Spaces ist **gemessen** (183,0 px bei 152
    Knoten): die gewachsenen Masken ueberlappen erst, wenn `2 · (LOBE_REACH + D) >= d` — bei
    diesem Abstand also ab `D` = 43,5 px. Ohne diese Zahl waere die Wahl des
    `LOBE_CLOSE_PX` eine Augenentscheidung."""
    abnahme = _beleg()["koerper"]["abnahme"]
    assert abnahme["min_abstand_zwei_spaces_px"] is not None, (
        "der kleinste Abstand zweier Spaces ist nicht gemessen")
    assert abnahme["min_abstand_zwei_spaces_px"] > 0
    assert abnahme["zellgroesse_px"] == 8, "die Rasterzelle ist 8 px (LOBE_CELL_PX)"
    assert abnahme["raster"]["cols"] > 0 and abnahme["raster"]["rows"] > 0


def test_a_beleg_with_a_green_koerper_cell_would_be_rejected(tmp_path, monkeypatch):
    """Die erste Gegenprobe der koerper-Zelle: ein Beleg, in dem die koerper-Zelle **gruen**
    ist, muss den Wächter rot machen — an der Basislinie ist sie rot (fuenf Inseln)."""
    beleg = _beleg()
    beleg["zellen"]["koerper"] = True
    beleg["koerper"]["ok"] = True
    gefaelscht = tmp_path / "p105_b14_karte_bilder.json"
    gefaelscht.write_text(json.dumps(beleg), encoding="utf-8")
    monkeypatch.setattr(sys.modules[__name__], "BELEG", gefaelscht)
    with pytest.raises(AssertionError):
        test_the_beleg_is_the_stand_14_6_0()


def test_a_beleg_with_one_island_would_be_rejected(tmp_path, monkeypatch):
    """Die zweite Gegenprobe: ein Beleg mit **einer** Komponente (statt fuenf) muss rot
    machen — sonst waere die Basislinie eine Behauptung."""
    beleg = _beleg()
    beleg["koerper"]["abnahme"]["komponenten"] = 1
    gefaelscht = tmp_path / "p105_b14_karte_bilder.json"
    gefaelscht.write_text(json.dumps(beleg), encoding="utf-8")
    monkeypatch.setattr(sys.modules[__name__], "BELEG", gefaelscht)
    with pytest.raises(AssertionError):
        test_the_body_is_five_islands_at_the_baseline()


def test_a_beleg_with_a_slow_compute_lobes_would_be_rejected(tmp_path, monkeypatch):
    """Die dritte Gegenprobe: eine `computeLobes()`-Zeit **ueber** der Grenze muss rot
    machen — der Wächter prueft die **Zahl**, nicht das `ok`-Feld."""
    beleg = _beleg()
    beleg["koerper"]["zeit"]["zeit_ms"] = 80.0
    gefaelscht = tmp_path / "p105_b14_karte_bilder.json"
    gefaelscht.write_text(json.dumps(beleg), encoding="utf-8")
    monkeypatch.setattr(sys.modules[__name__], "BELEG", gefaelscht)
    with pytest.raises(AssertionError):
        test_the_compute_lobes_time_is_within_the_limit()
