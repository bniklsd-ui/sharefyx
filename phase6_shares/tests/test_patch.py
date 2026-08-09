"""Reine Funktionstests für `storage.patch.apply_edits()` (P6-E/F, Plan §4 Step 1) — kennt
weder `Store` noch das Dateisystem, deshalb ohne Fixtures direkt aufrufbar. Die Store-Integration
(Lock, Version, Git-Commit) steht in `phase1_storage/tests/test_store.py`, nicht hier — siehe
`phase6_shares/CLAUDE.md`s Session-Block für die Begründung (Plan nennt `test_store_patch.py`,
`phase1_storage/tests/conftest.py` ist aber leer, alle Fixtures leben lokal in `test_store.py`)."""
from __future__ import annotations

import pytest

from storage.patch import PatchError, apply_edits


def test_apply_edits_replaces_each_anchor_once():
    body = "Zeile 1\nZeile 2\nZeile 3\n"
    edits = [
        {"old_text": "Zeile 1", "new_text": "Erste Zeile"},
        {"old_text": "Zeile 3", "new_text": "Dritte Zeile"},
    ]

    new_body, lines = apply_edits(body, edits)

    assert new_body == "Erste Zeile\nZeile 2\nDritte Zeile\n"
    assert lines == (1, 3)


def test_apply_edits_rejects_zero_matches_and_writes_nothing():
    body = "Nur dieser Text.\n"

    with pytest.raises(PatchError) as exc_info:
        apply_edits(body, [{"old_text": "Nicht vorhanden", "new_text": "X"}])

    err = exc_info.value
    assert err.index == 0
    assert err.found == 0
    assert err.lines == []


def test_apply_edits_rejects_multiple_matches_and_names_the_lines():
    body = "wieder\nwieder\nwieder\n"

    with pytest.raises(PatchError) as exc_info:
        apply_edits(body, [{"old_text": "wieder", "new_text": "X"}])

    err = exc_info.value
    assert err.index == 0
    assert err.found == 3
    assert err.lines == [1, 2]  # gedeckelt auf die ersten zwei Fundstellen (P6-F)


def test_edits_are_applied_in_order_and_may_depend_on_each_other():
    body = "Status: offen\n"
    edits = [
        {"old_text": "Status: offen", "new_text": "Status: in Arbeit"},
        {"old_text": "Status: in Arbeit", "new_text": "Status: erledigt"},
    ]

    new_body, lines = apply_edits(body, edits)

    assert new_body == "Status: erledigt\n"
    assert lines == (1, 1)


def test_apply_edits_failing_edit_reports_its_own_index_not_always_zero():
    body = "A\nB\n"
    edits = [
        {"old_text": "A", "new_text": "AA"},
        {"old_text": "nicht da", "new_text": "X"},
    ]

    with pytest.raises(PatchError) as exc_info:
        apply_edits(body, edits)

    assert exc_info.value.index == 1
