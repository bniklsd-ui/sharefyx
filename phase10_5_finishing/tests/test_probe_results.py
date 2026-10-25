"""Die committen Belege der Block-10.5-Probe müssen grün sein — und der Gegenlauf muss genau
die eine Zelle brechen, die er brechen soll.

**Warum ein Test und nicht nur eine Notiz.** Die Probe fährt gegen eine Wegwerf-Instanz; ihr
Ergebnis landet als JSON im Repo. Eine JSON-Datei im Repo ist aber nur so viel wert wie die
Aussage, die man über sie macht — und die Aussage „11 von 11 Zellen grün" steht nirgends im
Code, sie steht in einer Commit-Nachricht und in einer Doku-Tabelle. Ein Test bindet beides
zusammen: **die Zählung in der Doku** (der Abnahmestand des Phase-Heads) und **die Messdatei**
müssen dieselbe Zahl tragen.

**Der Gegenlauf hat eine eigene Datei** (`p105_b10_realtime_gegenlauf.json`), genau wie in
`phase9_hardening/tests/test_committed_probe_evidence.py`: der Gegenlauf **darf** rot sein,
das ist sein Zweck — und er darf den grünen Beleg nicht überschreiben. Die erste Fassung der
Probe schrieb beide Läufe in dieselbe Datei; das ist hier festgehalten, damit es nicht wieder
passiert.

**Der Gegenlauf muss genau eine Zelle brechen.** Bricht er keine, misst er nichts (der Filter
wäre wirkungslos). Bricht er mehrere, ist er unpräzise — er darf nicht nebenbei etwas anderes
kaputtmachen, was dann als „der Gegenlauf war wirksam" im Aktentasche landet.
"""
from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PROBE_DIR = REPO_ROOT / "phase10_5_finishing" / "probes"
GRUEN = PROBE_DIR / "p105_b10_realtime.json"
GEGENLAUF = PROBE_DIR / "p105_b10_realtime_gegenlauf.json"
HEAD = REPO_ROOT / "phase10_5_finishing" / "CLAUDE.md"
#: Die **geschlossenen** Abnahmezeilen stehen seit 2026-10-25 (Block 11.8) im L3-Archiv --
#: der Head trägt nur die offenen Zeilen (Softcap-Schnitt, siehe `test_head_rules.py`).
ABNAHME_ARCHIV = REPO_ROOT / "phase10_5_finishing" / "ABNAHME_ARCHIVE.md"

#: Die Fristen aus der Abnahme (P10.5-46 und P10.5-48).
LATENZ_MAX_MS = 2000
SHUTDOWN_MAX_S = 10

#: Die Zelle, die der Gegenlauf brechen muss: der Ereignis-Filter in `api.py`.
GEGENLAUF_ZELLE = "unsichtbarer_space_kein_ereignis"


def _befund(datei: Path) -> dict:
    assert datei.exists(), f"der Beleg fehlt: {datei}"
    return json.loads(datei.read_text(encoding="utf-8"))


def _zellen(befund: dict) -> dict[str, bool]:
    """Nur die **booleschen** Zellen — `latenz_ms` und `shutdown_s` sind Messwerte, keine
    Zellen (sie würden sonst als „falsch" gezählt)."""
    return {k: v for k, v in befund.items() if isinstance(v, bool)}


def test_the_green_report_has_all_cells_green():
    bericht = _befund(GRUEN)
    assert bericht.get("alle_kriterien_erfuellt") is True, (
        "der grüne Beleg meldet nicht 'alle Kriterien erfüllt' — die Datei ist kein Beleg"
    )
    rot = [k for k, v in _zellen(bericht["befund"]).items() if not v]
    assert not rot, f"rote Zellen im grünen Beleg: {rot}"


def test_the_green_report_meets_the_two_deadlines():
    befund = _befund(GRUEN)["befund"]
    assert befund["latenz_ms"] is not None, "die Latenz wurde nicht gemessen"
    assert befund["latenz_ms"] <= LATENZ_MAX_MS, (
        f"die Latenz war {befund['latenz_ms']:.1f} ms — die Frist der Abnahme P10.5-46 "
        f"ist {LATENZ_MAX_MS} ms"
    )
    assert befund["shutdown_s"] <= SHUTDOWN_MAX_S, (
        f"der Shutdown brauchte {befund['shutdown_s']} s — die Frist der Abnahme P10.5-48 "
        f"ist {SHUTDOWN_MAX_S} s"
    )


def test_the_gegenlauf_report_is_red_in_exactly_one_cell():
    bericht = _befund(GEGENLAUF)
    assert bericht.get("gegenlauf") is True, "die Gegenlauf-Datei ist kein Gegenlauf-Lauf"
    rot = [k for k, v in _zellen(bericht["befund"]).items() if not v]
    assert rot == [GEGENLAUF_ZELLE], (
        f"der Gegenlauf muss genau die Zelle {GEGENLAUF_ZELLE!r} brechen, gebrochen wurde: {rot}"
    )
    assert bericht.get("gegenlauf_erwartet_rot") is True


def test_the_two_reports_are_different_files():
    """Der Gegenlauf darf den grünen Beleg nicht überschreiben — das war der Fehler, den
    `phase9_hardening/tests/test_committed_probe_evidence.py` am 2026-10-02 aufgedeckt hat."""
    assert GRUEN != GEGENLAUF
    assert GRUEN.read_text(encoding="utf-8") != GEGENLAUF.read_text(encoding="utf-8")
    assert "gegenlauf" not in json.loads(GRUEN.read_text(encoding="utf-8"))


def test_the_head_counts_the_probe_cells_in_its_acceptance_table():
    """Die Doku und der Beleg müssen dieselbe Zahl tragen: der Abnahmestand nennt P10.5-45,
    46, 47 und 48 als erfüllt — das sind genau die vier Abnahmezeilen, die diese Probe belegt
    (plus die Ereignis-Zelle der Zeile 46)."""
    # **Head und Archiv**: die geschlossenen Zeilen stehen seit Block 11.8 im Archiv.
    tabellen = [HEAD.read_text(encoding="utf-8"), ABNAHME_ARCHIV.read_text(encoding="utf-8")]
    for nummer in ("P10.5-45", "P10.5-46", "P10.5-47", "P10.5-48"):
        zeile = [z for tabelle in tabellen for z in tabelle.splitlines()
                 if z.startswith(f"| {nummer} |")]
        assert zeile, f"{nummer} steht in keiner der beiden Abnahmetabellen"
        assert "| ✅ |" in zeile[0], f"{nummer} ist nicht als erfüllt markiert"
