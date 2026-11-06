"""Editor 4.1, Schritt S0: der **Beleg** der Darstellungs-Probe (`probes/p105_ed41_darstellung_probe.py`).

Die Probe startet eine Wegwerf-Instanz und zwei Browser (rund zwei Minuten je Lauf) und laeuft deshalb
nicht in der Suite. Dieser Waechter prueft die **Belegdateien** und den **Korpus** im Repo, ohne Browser
(Muster `test_b18_live_zeilen_probe.py`):

- die Basislinie ist in **beiden** Browsern genau so rot/gruen, wie `p105_ed41_spec.ZELLEN` es erwartet
  (Plan S0: „Basislinie rot in den erwarteten Zellen — das ist der Befund");
- jeder Gegenlauf dreht gegenueber der Basislinie **genau** seine Zellen um, in beiden Browsern;
- jeder Gegenlauf-Anker steht **genau einmal** in den heutigen statischen Dateien bzw. im Katalog
  (Falle aus 18.2b: ein doppelter oder verschwundener Anker beisst still nicht);
- die Fixtures auf der Platte = Woerterbuch = Manifest (SHA-256), ≥ 22 Fixtures, M7 unveraendert;
- die Kontrollen der Probe stimmen (der Entwurf kann ueberleben; die Tastenmessung hinterlaesst nichts);
- kein Geheimnis im Beleg.

Laeuft die Probe nach einem Editor-Schritt (S1, S2, …) neu, drehen sich Zellen absichtlich um: dann
wird `ZELLEN[...]["basis"]` in `p105_ed41_spec.py` **bewusst** nachgezogen — nie dieser Waechter gelockert.

**[2026-11-06, S1]** Statt `basis` nachzuziehen, hat jeder Stand seinen eigenen Beleg
(`spec.BELEG_JE_STAND`, `spec.ERWARTET[stand]`): die S0-Basislinie bleibt eingefroren, der S1-Beleg
`p105_ed41_darstellung_s1.json` weicht von ihr in **genau** den drei Entwurfszellen ab. Ein Gegenlauf
vergleicht mit dem Beleg, gegen den er gelaufen ist (`referenz`; fehlt das Feld: die S0-Basislinie).

**[2026-11-06, S2]** Das Tabellen-Widget bringt fuenf **neue** Zellen (`ab: "S2"`); die Belege von S0/S1
tragen sie nicht und werden gegen ihren eigenen Zellensatz geprueft (`spec.zellen_fuer(stand)`). Der S2-Beleg
`p105_ed41_darstellung_s2.json` weicht vom S1-Beleg in **genau** `tabelle_widget` ab; die Tastenkosten
(inkl. Abgleich) bleiben unter S1-Basis + 2 ms.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
PROBES = REPO_ROOT / "phase10_5_finishing" / "probes"
STATIC = REPO_ROOT / "phase5_ui" / "webui" / "static"
sys.path.insert(0, str(PROBES))
import p105_ed41_spec as spec  # noqa: E402

BROWSER = ("chromium", "firefox")
BELEG = PROBES / "p105_ed41_darstellung.json"
BELEG_S1 = PROBES / "p105_ed41_darstellung_s1.json"
BELEG_S2 = PROBES / "p105_ed41_darstellung_s2.json"
S1_ZELLEN = ["oeffnen_schreibt_keinen_entwurf", "entwurf_ueberlebt_neuladen", "kein_stilles_zurueck"]
S2_NEU = ["klick_zelle", "pfeil_erste_zeile", "pfeil_letzte_zeile", "undo", "kopieren_quelle"]


def _laden(pfad: Path) -> dict:
    assert pfad.exists(), "Beleg fehlt: %s" % pfad.name
    return json.loads(pfad.read_text(encoding="utf-8"))


def _gegenlauf(name: str) -> Path:
    return PROBES / ("p105_ed41_darstellung_gegenlauf_%s.json" % name)


# -- Basislinie ------------------------------------------------------------------------------------

def test_the_baseline_was_measured_in_both_browsers_without_a_counter_run():
    beleg = _laden(BELEG)
    assert beleg["gegenlauf"] is None
    assert set(beleg["browser"]) == set(BROWSER)
    assert beleg["fixtures"] >= 22


@pytest.mark.parametrize("browser", BROWSER)
def test_the_baseline_is_red_exactly_where_the_plan_expects_it(browser):
    roh = _laden(BELEG)["browser"][browser]
    assert list(roh["zellen"]) == spec.zellen_fuer("S0"), "Zellnamen weichen von der Spec ab"
    abweichend = {n: v for n, v in roh["zellen"].items() if v != spec.ERWARTET_BASIS[n]}
    assert not abweichend, "Zellen weichen von der erwarteten Basislinie ab: %s" % abweichend
    assert roh["abweichungen"] == []
    assert not roh["seitenfehler"], roh["seitenfehler"]


def test_the_cells_named_in_the_plan_s0_row_are_red_today():
    """Plan §5 S0: rot in Editor-Tabelle, Listenzeichen, Entwurf, F4a–f, Kontrast."""
    s0 = ["tabelle_widget", "listenzeichen", "kontrast", "oeffnen_schreibt_keinen_entwurf",
          "entwurf_ueberlebt_neuladen", "kein_stilles_zurueck"] + [n for n in spec.ZELLEN if n.startswith("konflikt_")]
    assert len(s0) == 12
    for browser in BROWSER:
        zellen = _laden(BELEG)["browser"][browser]["zellen"]
        assert [n for n in s0 if zellen[n]] == [], browser


@pytest.mark.parametrize("browser", BROWSER)
def test_the_contrast_failures_are_the_vendored_token_colours_of_a9(browser):
    klassen = _laden(BELEG)["browser"][browser]["kontrast"]["klassen"]
    rot = {k for k, v in klassen.items() if v["kontrast"] < 4.5}
    einzel = {t for k in rot for t in k.split()}
    assert {"cm-keyword", "cm-tag", "cm-attribute", "cm-string"} <= einzel
    assert klassen["cm-keyword"]["kontrast"] == pytest.approx(1.94, abs=0.01)


@pytest.mark.parametrize("browser", BROWSER)
def test_the_probe_controls_hold(browser):
    roh = _laden(BELEG)["browser"][browser]
    # der Entwurf **kann** ueberleben (A zuerst) -- die rote Zelle ist kein Messfehler
    assert roh["entwurf"]["kontrolle_a_zuerst"] == {"dialog": True, "editor_hat_entwurf": True}
    # die Tastenmessung hinterlaesst den Text unveraendert; Rohdaten 2 Zeilen x 3 Laeufe
    assert roh["tastenkosten_sauber_danach"] is True and roh["tastenkosten"]["text_wie_vorher"] is True
    for zeile in ("absatzzeile", "tabellenzeile"):
        assert len(roh["tastenkosten"][zeile]) == 3
    # die XSS-Liste hat kein aktives Element und keinen nativen Dialog ausgeloest
    assert roh["aktive"]["boese"] == [] and roh["aktive"]["attrs"] == [] and roh["aktive"]["dialoge_nativ"] == []
    # Saat-Treue: nur die CRLF-Fixture weicht im API-Body ab (der Server liefert LF, Plan F8)
    abweichend = sorted(n for n, t in roh["saat_treue"].items() if not t["api_gleich_fixture"])
    assert abweichend == ["26_crlf"]
    assert all(t["datei_gleich_fixture"] for t in roh["saat_treue"].values())


# -- S1: Entwurfsschutz (Plan §5 S1, V7) ----------------------------------------------------------

def test_the_s1_evidence_is_the_current_stand_in_both_browsers():
    assert spec.BELEG_JE_STAND["S1"] == BELEG_S1.name
    beleg = _laden(BELEG_S1)
    assert beleg["stand"] == "S1" and beleg["gegenlauf"] is None and beleg["referenz"] == BELEG_S1.name
    assert set(beleg["browser"]) == set(BROWSER)


@pytest.mark.parametrize("browser", BROWSER)
def test_s1_turns_exactly_the_three_draft_cells_green(browser):
    neu = _laden(BELEG_S1)["browser"][browser]
    alt = _laden(BELEG)["browser"][browser]["zellen"]
    assert list(neu["zellen"]) == spec.zellen_fuer("S1")
    assert neu["abweichungen"] == [] and not neu["seitenfehler"], (neu["abweichungen"], neu["seitenfehler"])
    assert {n: v for n, v in neu["zellen"].items() if v != spec.ERWARTET["S1"][n]} == {}
    assert sorted(n for n in neu["zellen"] if neu["zellen"][n] != alt[n]) == sorted(S1_ZELLEN)
    assert all(neu["zellen"][n] for n in S1_ZELLEN)


@pytest.mark.parametrize("browser", BROWSER)
def test_the_stale_draft_was_really_offered_not_just_absent(browser):
    """A13.7: gruen zaehlt nur, wenn der veraltete Entwurf angeboten wurde -- Dialog mit beiden
    Versionen, Fokus im Dialog, Strg+S laeuft in den Konflikt, „als neues Item anlegen" bewahrt ihn."""
    roh = _laden(BELEG_S1)["browser"][browser]
    k = roh["entwurf"]["kein_stilles_zurueck"]
    assert k["konflikt_dialog"] is True and k["dialog"] is False
    assert "Entwurf zu v%d, aktuell v%d" % (k["fremd"]["alt"], k["fremd"]["version"]) in k["konflikt_text"]
    assert k["konflikt_fokus"] == "conflict-cancel"
    assert k["editor_hat_entwurf"] is True and k["konflikt_nach_speichern"] is True
    assert k["neu"] == {"anders": True, "hat_entwurf": True, "version": 1}
    assert k["fremde_fassung_steht"] is True and k["server_hat_entwurf"] is False
    assert k["entwurf_nach_entscheidung"] is False
    u = roh["entwurf"]["ueberlebt"]
    assert u["entwurf_waehrend_dialog"] is True and u["editor_hat_entwurf"] is True
    assert roh["entwurf"]["kontrolle_a_zuerst"] == {"dialog": True, "editor_hat_entwurf": True}
    assert roh["entwurf"]["oeffnen"] == {"schluessel_nach_oeffnen": False}


# -- S2: Tabellen-Widget (Plan §5 S2) ------------------------------------------------------------

def test_the_s2_evidence_is_the_current_stand_in_both_browsers():
    assert spec.STAND == "S2" and spec.BELEG_JE_STAND["S2"] == BELEG_S2.name
    beleg = _laden(BELEG_S2)
    assert beleg["stand"] == "S2" and beleg["gegenlauf"] is None and beleg["referenz"] == BELEG_S2.name
    assert set(beleg["browser"]) == set(BROWSER)
    assert sorted(spec.ZELLEN[n]["ab"] for n in S2_NEU) == ["S2"] * 5


@pytest.mark.parametrize("browser", BROWSER)
def test_s2_turns_the_table_cells_green_and_leaves_the_rest(browser):
    """`tabelle_widget` rot -> gruen, die fuenf neuen Zellen gruen, jede S1-Zelle unveraendert."""
    neu = _laden(BELEG_S2)["browser"][browser]
    alt = _laden(BELEG_S1)["browser"][browser]["zellen"]
    assert list(neu["zellen"]) == spec.zellen_fuer("S2") == list(spec.ZELLEN)
    assert neu["abweichungen"] == [] and not neu["seitenfehler"], (neu["abweichungen"], neu["seitenfehler"])
    assert {n: v for n, v in neu["zellen"].items() if v != spec.ERWARTET["S2"][n]} == {}
    assert sorted(n for n in alt if neu["zellen"][n] != alt[n]) == ["tabelle_widget"]
    assert all(neu["zellen"][n] for n in S2_NEU + ["tabelle_widget", "bytes_gleich", "bytes_zelle", "bytes_ohne_newline"])


@pytest.mark.parametrize("browser", BROWSER)
def test_s2_cells_measured_what_they_claim(browser):
    roh = _laden(BELEG_S2)["browser"][browser]
    s2 = roh["s2"]
    assert s2["editor_gleich_api"] is True
    assert s2["pfeil_ab"] == {"widget_vorher": 1, "cursor": [2, 0], "widget_nachher": 0}
    assert s2["pfeil_auf"] == {"widget_vorher": 1, "cursor": [6, 0], "widget_nachher": 0}
    assert s2["klick"]["cursor"] == s2["klick"]["soll"] == [5, 14]
    assert s2["undo"]["historie_nach_wechseln"] == s2["undo"]["historie_vorher"]
    assert s2["kopieren"]["widget_waehrend_auswahl"] == 1
    # Katalog: 2 Widgets = 2 oberste Tabellen der Lesesicht (die im Zitat bleibt in beiden roh)
    assert roh["editor"]["__widget_marken"] == roh["lesesicht"]["__tabellen_oben"] == 2
    # Randfaelle: jedes Widget = die oberste Tabelle der Lesesicht; Seite waechst nicht seitwaerts
    r = roh["s2_rand"]
    assert r["anlegen"] == 201 and r["widgets"] == r["lesesicht_oben"] == 7 and r["gleich_lesesicht"] is True
    assert r["editor_gleich_api"] and r["sauber"] and r["editor_gleich_api_danach"]
    assert r["seite_breiter_als_fenster"] is False and r["breites_widget_scrollt"] is True
    assert r["ende_pfeil_cursor"] == r["ende_pfeil_soll"]


@pytest.mark.parametrize("browser", BROWSER)
def test_s2_typing_cost_stays_within_baseline_plus_2ms(browser):
    """Plan S2: Tastenkosten in der 2.000-Zeilen-Notiz <= Basis + 2 ms (Median von 3 x 20). Basis = der
    S1-Beleg (A13.5/A14.3); gemessen je Taste **inklusive** Abgleich des Widgets."""
    basis = _laden(BELEG_S1)["browser"][browser]["tastenkosten"]["absatzzeile"]
    roh = _laden(BELEG_S2)["browser"][browser]
    med = lambda laeufe: sorted(x["median"] for x in laeufe)[1]
    grenze = med(basis) + 2.0
    a = roh["tastenkosten_abgleich"]
    assert a["modul"] is True and a["absatzzeile_widgets"] == 1 and a["tabellenzeile_widgets"] == 0
    assert med(a["absatzzeile"]) <= grenze and med(a["tabellenzeile"]) <= grenze, (a, grenze)
    assert med(roh["tastenkosten"]["absatzzeile"]) <= grenze
    assert a["text_wie_vorher"] and roh["tastenkosten_abgleich_sauber_danach"]


# -- Gegenlaeufe -----------------------------------------------------------------------------------

@pytest.mark.parametrize("name", sorted(spec.GEGENLAEUFE))
def test_each_counter_run_flips_exactly_its_own_cells_in_both_browsers(name):
    beleg = _laden(_gegenlauf(name))
    basis = _laden(PROBES / beleg.get("referenz", BELEG.name))
    ab = spec.GEGENLAEUFE[name].get("ab", "S0")
    assert basis.get("stand", "S0") == beleg.get("stand", "S0")
    assert spec.STAENDE.index(beleg.get("stand", "S0")) >= spec.STAENDE.index(ab)
    soll = sorted(spec.GEGENLAEUFE[name]["kippt"])
    assert beleg["gegenlauf"] == name and beleg["kippt_soll"] == soll and beleg["kippt_genau"] is True
    assert set(beleg["browser"]) == set(BROWSER)
    for browser in BROWSER:
        neu, alt = beleg["browser"][browser]["zellen"], basis["browser"][browser]["zellen"]
        assert sorted(n for n in neu if neu[n] != alt[n]) == soll, browser


def test_there_is_a_counter_run_in_each_direction():
    """Gruen -> rot (die Zelle kann brechen) und rot -> gruen (die rote Zelle kann heilen)."""
    richtung = {"gruen_nach_rot": 0, "rot_nach_gruen": 0}
    for gl in spec.GEGENLAEUFE.values():
        erwartet = spec.ERWARTET[gl.get("ab", "S0")]
        for n in gl["kippt"]:
            richtung["gruen_nach_rot" if erwartet[n] else "rot_nach_gruen"] += 1
    assert all(richtung.values()), richtung


@pytest.mark.parametrize("name", sorted(spec.GEGENLAEUFE))
def test_each_counter_run_anchor_occurs_exactly_once_today(name):
    gl = spec.GEGENLAEUFE[name]
    for rel, patches in gl.get("static", {}).items():
        text = (STATIC / rel).read_text(encoding="utf-8")
        for alt, _neu in patches:
            assert text.count(alt) == 1, "%s: Anker %r kommt %d-mal vor" % (rel, alt[:50], text.count(alt))
    for fixture, patches in gl.get("fixture", {}).items():
        text = spec.NEUE_FIXTURES[fixture]
        for alt, _neu in patches:
            assert text.count(alt) == 1, "%s: Anker %r" % (fixture, alt)


# -- Korpus ----------------------------------------------------------------------------------------

def test_the_corpus_on_disk_matches_dictionary_and_manifest():
    manifest = json.loads(spec.MANIFEST.read_text(encoding="utf-8"))
    assert manifest == spec.manifest_soll(), "Manifest veraltet: p105_ed41_spec.py neu ausfuehren (nur gewollt)"
    platte = spec.fixtures_von_platte()          # prueft jede Datei gegen das Manifest (fail-closed)
    assert platte == spec.alle_fixtures()
    assert len(platte) >= 22
    assert sum(1 for n in platte if n.startswith("m7_")) == 10
    txt = sorted(p.name for p in spec.FIXTURE_DIR.glob("*.txt"))
    assert txt == sorted(n + ".txt" for n in spec.NEUE_FIXTURES), "unerwartete Datei in fixtures_ed41/"


def test_the_corpus_carries_the_byte_traps_of_the_plan():
    f = spec.NEUE_FIXTURES
    assert not f["22_ohne_newline"].endswith("\n")
    assert "\t" in f["23_tabs"] and "  \n" in f["24_doppel_leerzeichen"]
    assert f["25_unicode"].startswith("﻿") and " " in f["25_unicode"]
    assert "\r\n" in f["26_crlf"]
    gross = f["27_gross"].splitlines()
    assert len(gross) == 2000 and sum(1 for z in gross if z.startswith("| ")) >= 200
    for teil in ("1. [ ]", "[x]{.rot}", "~~~", "\\|", "<br>", "::: {.warnung}", "::: {.zentriert}",
                 "[^1]", "=====", "##### ", "###### ", "    - ", "  - ", spec.ASSET_ID):
        assert teil in f["28_katalog"], teil


def test_the_katalog_editor_anchors_are_unique_lines():
    probe = (PROBES / "p105_ed41_darstellung_probe.py").read_text(encoding="utf-8")
    anker = re.search(r"^ANKER = \[(.*?)^\]", probe, re.S | re.M).group(1)
    zeilen = spec.NEUE_FIXTURES["28_katalog"].split("\n")
    gefunden = re.findall(r'"([^"]+)"', anker)
    assert len(gefunden) >= 20
    for a in gefunden:
        # die Probe nimmt die **erste** Zeile mit dem Anker -- eindeutig nur, wenn es genau eine gibt
        assert sum(1 for z in zeilen if a in z) == 1, a


# -- Geheimnisse -----------------------------------------------------------------------------------

@pytest.mark.parametrize("datei", sorted(spec.BELEG_JE_STAND.values())
                         + ["p105_ed41_darstellung_gegenlauf_%s.json" % n for n in sorted(spec.GEGENLAEUFE)])
def test_no_secret_in_the_evidence(datei):
    text = (PROBES / datei).read_text(encoding="utf-8")
    for muster in (r"wegwerf-b14-", r'"password"', r'"secret"', r"sfx_session", r"csrf", r"\b[A-Z2-7]{32}\b"):
        assert not re.search(muster, text, re.I if muster == r"csrf" else 0), "%s: %s" % (datei, muster)


def test_the_m7_fixtures_are_referenced_not_copied():
    manifest = json.loads(spec.MANIFEST.read_text(encoding="utf-8"))["dateien"]
    m7 = {rel: e for rel, e in manifest.items() if rel.startswith("../fixtures_m7/")}
    assert len(m7) == 10
    for rel, e in m7.items():
        assert hashlib.sha256((spec.FIXTURE_DIR / rel).read_bytes()).hexdigest() == e["sha256"]
    assert not list(spec.FIXTURE_DIR.glob("*.md")), "keine .md in fixtures_ed41/ (doc_health)"
