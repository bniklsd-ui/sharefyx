import logging
import subprocess

import pytest

from storage import history


def _log(text: str, path) -> str:
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


def test_commit_creates_commit_with_exact_message(tmp_path):
    history.ensure_repo(tmp_path)
    (tmp_path / "nikinger").mkdir()
    (tmp_path / "nikinger" / "itm_a1b2c3d4__test.md").write_text("Inhalt\n")

    history.commit(tmp_path, "create itm_a1b2c3d4 [nikinger]")

    log = _log("create", tmp_path)
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
