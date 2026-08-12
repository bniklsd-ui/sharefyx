"""Charakterisierungstests (P6-D, Plan §4 Step 4): frieren das Verhalten des `storage`-Kerns
GEGEN DEN HEUTIGEN CODE ein, bevor der P6-Step-4-Umbau beginnt (folder/visibility/share_*).
Golden Files unter `golden/`, byte-verglichen — kein Step-Abschluss in Block B ohne grüne
Charakterisierung. Das ist P6s Ersatz für den Seam-Beweis (der leere `git diff` auf `storage/`
ist mit P6-C aufgehoben).

Nur die vier reinen Datei-Fälle (Round-Trip, Drift-Repair, Archiv) sind Golden-File-Vergleiche —
`ConflictError.current` und die vier Commit-Messages sind Verhalten ohne eigenen Dateiinhalt,
dafür genügen direkte Assertions wie in `phase1_storage/tests/test_store.py` bereits üblich.
"""
from __future__ import annotations

import os
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from storage import files
from storage.errors import ConflictError
from storage.store import Store

GOLDEN_DIR = Path(__file__).parent / "golden"


@pytest.fixture
def clock():
    state = {"now": datetime(2026, 8, 12, 9, 0, 0, tzinfo=timezone.utc)}

    def now_fn():
        return state["now"]

    now_fn.advance = lambda seconds=1: state.__setitem__("now", state["now"] + timedelta(seconds=seconds))
    return now_fn


@pytest.fixture
def deterministic_ids(monkeypatch):
    """`generate_id()` benutzt `secrets.token_hex(4)` — Goldens brauchen eine feste ID-Folge
    statt echten Zufalls, sonst weicht jeder Testlauf vom eingecheckten Golden ab."""
    counter = iter(range(1, 1000))
    monkeypatch.setattr(files, "generate_id", lambda: f"itm_{next(counter):08x}")


@pytest.fixture
def store(tmp_path, clock, deterministic_ids):
    return Store(tmp_path, now_fn=clock, git=False)


@pytest.fixture
def store_git(tmp_path, clock, deterministic_ids):
    return Store(tmp_path, now_fn=clock, git=True)


def _git_log(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(root), "log", "--format=%s"],
        capture_output=True, text=True, check=True,
    )
    return result.stdout.strip().splitlines()


def _item_path(root: Path, space: str, item) -> Path:
    return root / space / f"{item.id}__{files.slugify(item.title)}.md"


def _assert_matches_golden(name: str, actual: bytes) -> None:
    golden = GOLDEN_DIR / name
    assert golden.exists(), f"Golden fehlt: {golden}"
    assert actual == golden.read_bytes(), (
        f"{name} weicht vom eingecheckten Golden ab — byte-identisch erwartet (P6-D). "
        f"Ein Diff hier heißt: der Umbau hat bestehendes Verhalten verändert, nicht nur erweitert."
    )


def test_roundtrip_create_with_unknown_field_umlauts_and_crlf_matches_golden(store, tmp_path):
    """Unbekanntes Feld überlebt (Entscheidung A), Umlaute bleiben unquotiert-lesbar
    (`allow_unicode=True`), CRLF im Body wird beim Schreiben NICHT normalisiert — `atomic_write`
    öffnet die Datei im Textmodus mit `newline=None`, der unter POSIX nur `\\n` übersetzt
    (No-op, weil `os.linesep == "\\n"`), `\\r` bleibt unangetastet stehen."""
    item = store.create(
        "nikinger", type="note", title="Umlaut Cafe",
        body="Zeile eins\r\nZeile zwei mit Übung\r\n",
        custom_field="wert mit Umlaut äöü",
    )
    path = _item_path(tmp_path, "nikinger", item)
    _assert_matches_golden("roundtrip_create.md", path.read_bytes())

    # Charakterisierter Wart, nicht behoben: `store.get()` liest über `path.read_text()`
    # (Universal-Newlines, übersetzt CRLF -> LF), während `index.row_from_file()` für den
    # sha256 `read_bytes()` benutzt (rohe CRLF). Body und Datei-Bytes sind bewusst NICHT
    # dieselbe Normalform.
    assert store.get(item.id).body == "Zeile eins\nZeile zwei mit Übung\n"


def test_drift_repair_rewrites_only_version_and_matches_golden(store_git, tmp_path):
    item = store_git.create("nikinger", type="note", title="Einkaufsliste", body="Milch\n")
    path = _item_path(tmp_path, "nikinger", item)

    original = path.read_text()
    path.write_text(original.replace("Milch", "Milch, Butter"))
    later = path.stat().st_mtime + 5
    os.utime(path, (later, later))

    fetched = store_git.get(item.id)
    assert fetched.version == item.version + 1
    _assert_matches_golden("drift_repaired.md", path.read_bytes())
    assert _git_log(tmp_path)[0] == f"drift {item.id} [nikinger]"


def test_conflict_error_carries_current_item_not_a_diff(store):
    item = store.create("nikinger", type="task", title="Original")
    updated = store.update(item.id, version=item.version, title="Geaendert")

    with pytest.raises(ConflictError) as exc_info:
        store.update(item.id, version=item.version, title="Sollte scheitern")

    err = exc_info.value
    assert err.item_id == item.id
    assert err.expected_version == item.version
    assert err.current.version == updated.version
    assert err.current.title == "Geaendert"


def test_archive_path_and_all_four_commit_messages_match_golden(store_git, tmp_path):
    item = store_git.create("nikinger", type="task", title="Vier Schritte")
    updated = store_git.update(item.id, version=item.version, title="Vier Schritte v2")
    appended = store_git.append(item.id, version=updated.version, text="Angehaengt")
    archived = store_git.archive(item.id, version=appended.version)

    slug = files.slugify(archived.title)
    archive_path = tmp_path / "nikinger" / "_archive" / f"{item.id}__{slug}.md"
    old_path = tmp_path / "nikinger" / f"{item.id}__{slug}.md"
    assert archive_path.exists()
    assert not old_path.exists()
    _assert_matches_golden("archived.md", archive_path.read_bytes())

    log = _git_log(tmp_path)  # newest-first
    assert log == [
        f"archive {item.id} [nikinger]",
        f"append {item.id} [nikinger]",
        f"update {item.id} [nikinger]",
        f"create {item.id} [nikinger]",
    ]
