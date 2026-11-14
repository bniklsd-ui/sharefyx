"""Wächter für die Anker des P11-Plans (Lock P11-W) und für den Phase-11-Head (Lock P11-T).

**Anker.** Jede Edit-Stelle des Plans steht als wörtlicher String in `phase11_editor/anker.json`.
Solange ein Schritt `offen` ist, muss jeder seiner Anker **genau einmal** in seiner Datei
vorkommen — null Funde heißt „ein früherer Schritt hat den String geändert" (dann zieht dieser
Schritt die Datei nach), zwei Funde heißt „ein Patch auf diesen Anker beißt still nicht".

**Head.** Genau ein `## Session stopped`-Block, höchstens 4096 UTF-8-Bytes; der Head höchstens
40.960 B.

**Die Gegenproben stehen in derselben Datei** — ein Wächter, der nur am echten Stand grün ist,
beweist nichts.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
HEAD = REPO_ROOT / "phase11_editor" / "CLAUDE.md"
MARKER = "## Session stopped"
SESSION_LIMIT = 4096
HEAD_LIMIT = 40960

_spec = importlib.util.spec_from_file_location(
    "plan_anker", REPO_ROOT / "phase11_editor" / "scripts" / "plan_anker.py")
plan_anker = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(plan_anker)

DATEN = plan_anker.lade()
OFFEN = sorted(s for s, e in DATEN.items() if e["status"] == "offen")


def test_every_step_has_a_known_status():
    for schritt, eintrag in DATEN.items():
        assert eintrag["status"] in ("offen", "erledigt"), schritt


@pytest.mark.parametrize("schritt", OFFEN)
def test_each_anchor_of_an_open_step_occurs_exactly_once(schritt):
    for fund in plan_anker.pruefe(schritt, DATEN[schritt]):
        assert len(fund["zeilen_heute"]) == 1, (
            f"{schritt}: Anker in {fund['datei']} hat {len(fund['zeilen_heute'])} Funde "
            f"{fund['zeilen_heute']}: {fund['text'][:80]!r} — anker.json nachziehen (P11-W)"
        )


def test_the_anchor_guard_bites_on_a_missing_and_on_a_doubled_anchor(tmp_path, monkeypatch):
    """Gegenprobe: derselbe Prüfer meldet 0 Funde und 2 Funde."""
    (tmp_path / "a.txt").write_text("eins\nzwei\nzwei\n", encoding="utf-8")
    monkeypatch.setattr(plan_anker, "REPO_ROOT", tmp_path)
    eintrag = {"status": "offen", "anker": [
        {"datei": "a.txt", "text": "eins", "zeile": 1},
        {"datei": "a.txt", "text": "drei", "zeile": 9},
        {"datei": "a.txt", "text": "zwei", "zeile": 2},
    ]}
    funde = [len(f["zeilen_heute"]) for f in plan_anker.pruefe("X", eintrag)]
    assert funde == [1, 0, 2]


def _session_blocks(text: str) -> list[str]:
    teile = text.split("\n" + MARKER)
    return [MARKER + t.split("\n## ", 1)[0] for t in teile[1:]]


def test_the_head_carries_exactly_one_session_block_within_4_kib():
    bloecke = _session_blocks(HEAD.read_text(encoding="utf-8"))
    assert len(bloecke) == 1, f"{len(bloecke)} Session-Blöcke im Head — scripts/rotate_session_block.sh phase11_editor"
    groesse = len(bloecke[0].encode("utf-8"))
    assert groesse <= SESSION_LIMIT, f"Session-Block {groesse} B > {SESSION_LIMIT} B (P11-T)"


def test_the_head_stays_under_the_softcap():
    assert HEAD.stat().st_size <= HEAD_LIMIT, f"Head {HEAD.stat().st_size} B > {HEAD_LIMIT} B"


def test_the_session_block_guard_bites_on_an_oversized_and_on_a_second_block():
    gross = "# Kopf\n\n" + MARKER + " — x\n" + ("ä" * 2100) + "\n"
    assert len(_session_blocks(gross)[0].encode("utf-8")) > SESSION_LIMIT
    zwei = "# Kopf\n\n" + MARKER + " — a\nText\n\n" + MARKER + " — b\nText\n"
    assert len(_session_blocks(zwei)) == 2


def test_the_anchor_file_is_valid_json_with_plan_line_numbers():
    roh = json.loads((REPO_ROOT / "phase11_editor" / "anker.json").read_text(encoding="utf-8"))
    for schritt, eintrag in roh.items():
        for a in eintrag["anker"]:
            assert set(a) == {"datei", "text", "zeile"}, schritt
            assert isinstance(a["zeile"], int) and a["zeile"] > 0, (schritt, a["text"][:40])
