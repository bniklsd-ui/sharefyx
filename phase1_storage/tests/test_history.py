import logging
import subprocess

import pytest

from storage import history


def _log(path) -> str:
    return subprocess.run(
        ["git", "-C", str(path), "log", "--format=%s"],
        capture_output=True, text=True, check=True,
    ).stdout


def test_ensure_repo_creates_git_dir_and_gitignore(tmp_path):
    history.ensure_repo(tmp_path)

    assert (tmp_path / ".git").is_dir()
    gitignore = (tmp_path / ".gitignore").read_text()
    assert ".index.sqlite3*" in gitignore
    assert ".write.lock" in gitignore


def test_ensure_repo_is_idempotent(tmp_path):
    history.ensure_repo(tmp_path)
    marker = tmp_path / ".gitignore"
    original = marker.read_text()

    history.ensure_repo(tmp_path)  # zweiter Aufruf darf nicht re-initialisieren

    assert marker.read_text() == original


def test_ensure_repo_sets_identity_when_missing(tmp_path):
    history.ensure_repo(tmp_path)

    name = subprocess.run(
        ["git", "-C", str(tmp_path), "config", "--local", "user.name"],
        capture_output=True, text=True,
    ).stdout.strip()
    email = subprocess.run(
        ["git", "-C", str(tmp_path), "config", "--local", "user.email"],
        capture_output=True, text=True,
    ).stdout.strip()

    assert name
    assert email


def test_ensure_repo_does_not_overwrite_existing_identity(tmp_path):
    subprocess.run(["git", "-C", str(tmp_path), "init"], capture_output=True, check=True)
    subprocess.run(
        ["git", "-C", str(tmp_path), "config", "--local", "user.name", "Custom"],
        capture_output=True, check=True,
    )
    subprocess.run(
        ["git", "-C", str(tmp_path), "config", "--local", "user.email", "custom@example.com"],
        capture_output=True, check=True,
    )

    history.ensure_repo(tmp_path)

    name = subprocess.run(
        ["git", "-C", str(tmp_path), "config", "--local", "user.name"],
        capture_output=True, text=True,
    ).stdout.strip()
    assert name == "Custom"
    # Diskriminierender Teil: ein von Hand angelegtes Repo (kein Init-Zweig durchlaufen) muss
    # trotzdem eine .gitignore bekommen, sonst versioniert der erste commit() den Index mit.
    assert (tmp_path / ".gitignore").exists()


def test_commit_creates_commit_with_exact_message(tmp_path):
    history.ensure_repo(tmp_path)
    (tmp_path / "nikinger").mkdir()
    (tmp_path / "nikinger" / "itm_a1b2c3d4__test.md").write_text("Inhalt\n")

    history.commit(tmp_path, "create itm_a1b2c3d4 [nikinger]")

    log = _log(tmp_path)
    assert log.strip() == "create itm_a1b2c3d4 [nikinger]"


def test_commit_against_missing_repo_logs_critical_and_does_not_raise(tmp_path, caplog):
    # kein ensure_repo() vorher -- kein .git in tmp_path
    with caplog.at_level(logging.CRITICAL, logger="storage.history"):
        history.commit(tmp_path, "create itm_a1b2c3d4 [nikinger]")

    critical_records = [r for r in caplog.records if r.levelno == logging.CRITICAL]
    assert len(critical_records) >= 1


def test_commit_with_missing_git_binary_logs_critical_and_does_not_raise(
    tmp_path, monkeypatch, caplog
):
    history.ensure_repo(tmp_path)

    def boom(*args, **kwargs):
        raise OSError("git binary not found")

    monkeypatch.setattr(subprocess, "run", boom)

    with caplog.at_level(logging.CRITICAL, logger="storage.history"):
        history.commit(tmp_path, "create itm_a1b2c3d4 [nikinger]")

    critical_records = [r for r in caplog.records if r.levelno == logging.CRITICAL]
    assert len(critical_records) >= 1


# -- P9 Block trace: `commit(author=…)` (P9-AC, T6) ------------------------------------------


def _identitaet(path) -> tuple[str, str]:
    """`(Autor, Committer)` des letzten Commits, wie `git log` sie zeigt. Genau diese beiden
    Felder sind die Aussage von P9-AC: der **Autor** ist der Schreiber, der **Committer**
    bleibt die Maschine."""
    out = subprocess.run(
        ["git", "-C", str(path), "log", "-1", "--format=%an%n%cn"],
        capture_output=True, text=True, check=True,
    ).stdout.splitlines()
    return out[0], out[1]


def _commit_eine_datei(tmp_path, name: str) -> None:
    (tmp_path / name).write_text("x", encoding="utf-8")


def test_commit_sets_the_author_and_leaves_the_committer_at_the_default(tmp_path):
    """Der Kern von P9-AC: `git log --format=%an` (und `git blame`) nennen den Menschen, dessen
    Space geschrieben hat. Wuerde stattdessen der Committer wechseln, wuerde jede spaetere
    Reihenfolge-Aussage ueber Commits eine Aussage ueber Maschinen sein."""
    history.ensure_repo(tmp_path)
    _commit_eine_datei(tmp_path, "a.md")

    history.commit(tmp_path, "update itm_x [sp]", author="niklas")

    autor, committer = _identitaet(tmp_path)
    assert autor == "niklas"
    assert committer == "Space Server"
    assert "sharefyx.invalid" in subprocess.run(
        ["git", "-C", str(tmp_path), "log", "-1", "--format=%ae"],
        capture_output=True, text=True, check=True,
    ).stdout


def test_commit_without_an_author_uses_the_default_identity(tmp_path):
    """Ohne Akteur (P9-AB: Operator-Skripte, Drift-Abgleich, Tests) bleibt alles wie vorher —
    der Block darf keinen Bestandseintrag umschreiben, nur weil er einen Default traegt."""
    history.ensure_repo(tmp_path)
    _commit_eine_datei(tmp_path, "a.md")

    history.commit(tmp_path, "update itm_x [sp]")

    assert _identitaet(tmp_path) == ("Space Server", "Space Server")


def test_commit_with_a_broken_author_still_commits_and_warns(tmp_path, caplog):
    """P9-AC im Fehlerfall: ein Name mit `<`, `>` oder Zeilenumbruch wuerde die Form
    `Name <mail>` sprengen (bzw. einen zweiten Parameter einschleusen). Der Commit laeuft
    **trotzdem** — `history.py`s Vertrag ist „ein Write scheitert nie an Git" (Entscheidung E),
    und dieser Vertrag hat Vorrang vor einer hübscheren Zuschreibung. Geprüft werden beide
    Haelften: Warnung **und** Commit."""
    history.ensure_repo(tmp_path)
    _commit_eine_datei(tmp_path, "a.md")

    with caplog.at_level(logging.WARNING, logger="storage.history"):
        history.commit(tmp_path, "update itm_x [sp]", author="a<b")

    assert _identitaet(tmp_path) == ("Space Server", "Space Server")
    assert "verworfen" in caplog.text
    assert "update itm_x [sp]" in _log(tmp_path)


def test_a_name_starting_with_a_dash_survives_as_an_author(tmp_path):
    """V179: `create_space()` verbietet `/`, fuehrenden `.` und reservierte Namen — einen
    fuehrenden `-` **nicht**. Der Wert geht als eigenes argv-Element an `--author`, deshalb ist
    er unkritisch; der Test sagt das messbar, statt es zu behaupten (die Git-Historie hat
    schon einmal bewiesen, dass so ein Wert in einer Command-Zeile als Option gelesen wird —
    Phase-8-Block-J, `authctl revoke --family-id <ID>`)."""
    history.ensure_repo(tmp_path)
    _commit_eine_datei(tmp_path, "a.md")

    history.commit(tmp_path, "update itm_x [sp]", author="-dash")

    assert _identitaet(tmp_path)[0] == "-dash"
