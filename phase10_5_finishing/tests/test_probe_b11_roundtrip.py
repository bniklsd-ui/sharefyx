"""Die committen Belege der Block-11.8-Probe: der Roundtrip (V201-Rest).

**Was gemessen wird (Abnahme P10.5-52).** Die **zehn** M7-Fixtures (Frontmatter, Listen,
Tabelle, Code, Links, `itm_…`-Referenzen, Taskliste, Zitat, Unicode/Tabs, Whitespace) als
Items in der Wegwerf-Instanz. Je Item: **öffnen** → der Editor zeigt byte-identisch den
Body, `isDirty()` ist **false** und der Speicher-Knopf ist deaktiviert → ein Zeichen tippen
und wieder löschen → `isDirty()` ist wieder **false**. Dazu (im Python-Teil der Probe) der
**Plattenvergleich**: die Item-Dateien sind vor dem Lauf und nach dem Lauf **byte-identisch**.

**Warum die Fixtures jetzt im Repo liegen.** Die M7-Messung lief im Scratchpad
(`~/.claude-code-tools/m7`), die Fixtures lagen dort — ein Beleg, den niemand wiederholen
kann, ist kein Beleg. Die zehn Dateien liegen jetzt **byte-identisch** in
`phase10_5_finishing/probes/fixtures_m7/`, und dieser Wächter vergleicht ihre Bytezahlen mit
dem Beleg: stimmt eine Zahl nicht, ist der Beleg zu einem anderen Bestand gemessen.

**Was dieser Wächter zusätzlich festhält.** Die Zahl der Fixtures (zehn) und die
Byte-Identität **jedes** Textes (`text == body`) — nicht nur die Gesamtzahl der grünen
Zellen. Ein Beleg, der „zehn Items geprüft" meldet, aber bei neun Items denselben Text
trägt, wäre grün und falsch.
"""
from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PROBE_DIR = REPO_ROOT / "phase10_5_finishing" / "probes"
FIXTURE_DIR = PROBE_DIR / "fixtures_m7"
BELEG = PROBE_DIR / "p105_b11_roundtrip.json"
HEAD = REPO_ROOT / "phase10_5_finishing" / "CLAUDE.md"

#: Die **zehn** Fixtures der M7-Messung (`phase10_inventory/messung/M7_editor.md`).
ANZAHL_FIXTURES = 10


def _beleg() -> dict:
    assert BELEG.exists(), f"der Beleg fehlt: {BELEG}"
    return json.loads(BELEG.read_text(encoding="utf-8"))


def _zellen(befund: dict) -> dict[str, bool]:
    return {k: v for k, v in befund.items() if isinstance(v, bool)}


def test_the_report_has_all_cells_green():
    bericht = _beleg()
    assert bericht.get("alle_kriterien_erfuellt") is True, (
        "der Beleg meldet nicht 'alle Kriterien erfüllt' — die Datei ist kein Beleg"
    )
    rot = [k for k, v in _zellen(bericht["befund"]).items() if not v]
    assert not rot, f"rote Zellen im Beleg: {rot}"


def test_all_ten_fixtures_were_measured():
    bericht = _beleg()
    einzel = bericht.get("einzel") or []
    assert len(einzel) == ANZAHL_FIXTURES, (
        f"der Beleg trägt {len(einzel)} Einzelwerte, erwartet {ANZAHL_FIXTURES}"
    )
    assert len({e["datei"] for e in einzel}) == ANZAHL_FIXTURES, (
        "dieselbe Fixture wurde zweimal gemessen — es sind nicht zehn verschiedene"
    )


def test_the_fixtures_in_the_repo_are_the_measured_ones():
    """**Der Beleg muss zum Bestand im Repo passen.** Die Bytezahlen der Fixtures im
    Beleg müssen den Dateien im Repo entsprechen — sonst wurde ein **anderer** Bestand
    gemessen und der Beleg beweist nichts."""
    einzel = _beleg()["einzel"]
    for eintrag in einzel:
        pfad = FIXTURE_DIR / eintrag["datei"]
        assert pfad.exists(), f"die Fixture fehlt im Repo: {pfad}"
        groesse = len(pfad.read_bytes())
        assert groesse == eintrag["bytes"], (
            f"{eintrag['datei']}: im Beleg {eintrag['bytes']} B, im Repo {groesse} B — "
            "der Beleg wurde gegen einen anderen Bestand gemessen"
        )


def test_every_item_is_byte_identical_and_clean():
    """**Je Item**, nicht in der Summe: der Text ist byte-identisch mit dem Body, das
    Öffnen macht den Editor **nicht** geändert, und nach dem Löschen ist er wieder sauber."""
    for eintrag in _beleg()["einzel"]:
        assert eintrag["text_gleich_body"] is True, (
            f"{eintrag['datei']}: der Editor zeigt einen anderen Text als der Server"
        )
        assert eintrag["dirty_beim_oeffnen"] is False, (
            f"{eintrag['datei']}: das Öffnen macht den Editor geändert"
        )
        assert eintrag["dirty_nach_tippen"] is True, (
            f"{eintrag['datei']}: ein getipptes Zeichen wird nicht als Änderung erkannt"
        )
        assert eintrag["dirty_nach_loeschen"] is False, (
            f"{eintrag['datei']}: nach dem Löschen ist der Editor noch geändert"
        )
        assert eintrag["knopf_deaktiviert"] is True, (
            f"{eintrag['datei']}: der Speicher-Knopf ist aktiv, obwohl nichts geändert wurde"
        )


def test_the_raw_mode_shows_every_character():
    """**ED-5 (Abnahme P10.5-55).** Im Rohtext ist **kein** Zeichen unsichtbar."""
    for eintrag in _beleg()["einzel"]:
        assert eintrag["rohmodus_text_gleich_text"] is True, (
            f"{eintrag['datei']}: im Rohtext fehlt ein Zeichen (oder es kam eines dazu)"
        )


def test_the_head_names_the_step():
    head = HEAD.read_text(encoding="utf-8")
    assert "11.8" in head, "der Phase-Head nennt 11.8 nicht"
    assert "Roundtrip" in head, "der Phase-Head nennt den Roundtrip nicht"
