"""Reine Funktionstests für `webui.updates :: parse_update_log()`/`load_update_log()` (Plan §4
Step 3, §5 Testliste `phase6_shares/tests/test_updates.py`) — kein Store, kein Prozess, direkt
aufrufbar. Gleiche Begründung wie `phase6_shares/tests/test_patch.py`s Moduldocstring: der
Parser ist reine Funktionslogik, unabhängig davon, dass das Modul selbst unter `phase5_ui/`
liegt (`webui`-Paket ist editable im ganzen venv installiert, keine zweite Kopie nötig)."""
from __future__ import annotations

from pathlib import Path

from webui.updates import UpdateEntry, load_update_log, parse_update_log


def test_parse_empty_text_returns_no_entries():
    assert parse_update_log("") == []


def test_parse_ignores_lines_before_the_first_heading():
    text = "Kein Eintrag hier.\n- Auch keine Zeile.\n## 2026-08-09\n- Erste echte Zeile.\n"
    entries = parse_update_log(text)
    assert entries == [UpdateEntry(id="2026-08-09#1", date="2026-08-09", lines=["Erste echte Zeile."])]


def test_parse_ignores_malformed_lines_and_headings():
    text = (
        "## 2026-08-09\n"
        "- gueltige Zeile\n"
        "kein Bindestrich, wird ignoriert\n"
        "### 2026-08-09 (drei Rauten, keine Ueberschrift)\n"
        "## nicht-iso-datum\n"
        "- diese Zeile gehoert noch zum ersten Eintrag\n"
    )
    entries = parse_update_log(text)
    assert len(entries) == 1
    assert entries[0].lines == ["gueltige Zeile", "diese Zeile gehoert noch zum ersten Eintrag"]


def test_parse_preserves_file_order_newest_first():
    text = "## 2026-08-12\n- neu\n## 2026-08-10\n- alt\n"
    entries = parse_update_log(text)
    assert [e.id for e in entries] == ["2026-08-12#1", "2026-08-10#1"]


def test_parse_assigns_sequential_ids_within_the_same_date():
    text = "## 2026-08-09\n- erster Block\n## 2026-08-09\n- zweiter Block\n"
    entries = parse_update_log(text)
    assert [e.id for e in entries] == ["2026-08-09#1", "2026-08-09#2"]
    assert entries[1].lines == ["zweiter Block"]


def test_load_update_log_returns_empty_list_for_missing_file(tmp_path):
    assert load_update_log(tmp_path / "does-not-exist.md") == []


def test_load_update_log_reads_a_real_file(tmp_path):
    path = tmp_path / "UPDATE_LOG.md"
    path.write_text("## 2026-08-09\n- Text.\n", encoding="utf-8")
    entries = load_update_log(path)
    assert entries == [UpdateEntry(id="2026-08-09#1", date="2026-08-09", lines=["Text."])]


def test_real_update_log_has_no_swallowed_continuation_lines():
    """Regressionstest gegen einen echten Live-Fund (2026-08-10): ein Eintrag in
    `docs/UPDATE_LOG.md` war als weich umgebrochener Fließtext geschrieben (mehrere physische
    Zeilen ohne eigenes führendes `- `) — der Parser ignoriert per Spezifikation (§2.4) jede
    Zeile, die nicht mit `## `/`- ` beginnt, also verschluckte er die Fortsetzungszeilen
    stillschweigend. Das Banner zeigte nur den ersten, mitten im Satz abgeschnittenen Teil.
    Kein Parser-Bug (der tut exakt, was `test_parse_ignores_malformed_lines_and_headings` oben
    verlangt) — ein Content-Bug, den nichts in dieser Suite bis dahin fangen konnte, weil kein
    Test je die REALE Datei gelesen hat. Erlaubt: Leerzeilen, ein `<!-- ... -->`-Kommentarblock
    (mehrzeilig, keine Zeile darin beginnt mit `## `/`- `)."""
    path = Path(__file__).resolve().parents[2] / "docs" / "UPDATE_LOG.md"
    text = path.read_text(encoding="utf-8")
    in_comment = False
    for lineno, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.rstrip()
        if not line:
            continue
        if line.startswith("<!--"):
            in_comment = True
        if in_comment:
            if "-->" in line:
                in_comment = False
            continue
        assert line.startswith("## ") or line.startswith("- "), (
            f"docs/UPDATE_LOG.md:{lineno} beginnt weder mit '## ' noch mit '- ' — der Parser "
            f"würde diese Zeile stillschweigend verschlucken: {line!r}"
        )
