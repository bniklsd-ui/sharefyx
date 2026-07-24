"""Git-Anbindung des `DATA_ROOT` (Plan §4 Step 5, Entscheidung E). Ein Commit je erfolgreichem
Write, damit kein Write unwiederbringlich ist. Beide Funktionen sind **nie fatal** — jeder
Fehler (fehlendes Git-Binary, kaputtes Repo, fehlgeschlagener Commit) wird abgefangen und als
`logger.critical` sichtbar gemacht, aber nie als Exception nach außen gereicht. Ein Write darf
nie an Git scheitern.
"""
from __future__ import annotations

import logging
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)

_GITIGNORE_CONTENT = ".index.sqlite3*\n.write.lock\n"


def _run_git(data_root: Path, *args: str) -> subprocess.CompletedProcess[str] | None:
    try:
        return subprocess.run(
            ["git", "-C", str(data_root), *args],
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        logger.critical("git-Aufruf fehlgeschlagen (Binary evtl. nicht installiert): %s", exc)
        return None


def ensure_repo(data_root: Path) -> None:
    """`git init` in `data_root`, falls `.git` fehlt; schreibt dabei eine `.gitignore`
    (`.index.sqlite3*` inkl. WAL-/SHM-Sidecars, `.write.lock`) — sonst landet der derivierte
    Index (Entscheidung A) im ersten Commit. Setzt eine lokale Commit-Identity, wenn **keine**
    existiert (auch wenn `.git` schon von Hand angelegt wurde) — sonst schlägt jeder Commit für
    immer fehl, da auf dieser Maschine keine globale Git-Identity konfiguriert ist. Überschreibt
    nie eine vorhandene Identity. Idempotent, nie fatal.
    """
    if not (data_root / ".git").is_dir():
        result = _run_git(data_root, "init")
        if result is None or result.returncode != 0:
            logger.critical(
                "git init in %s fehlgeschlagen: %s", data_root, result.stderr if result else ""
            )
            return
        gitignore = data_root / ".gitignore"
        if not gitignore.exists():
            gitignore.write_text(_GITIGNORE_CONTENT, encoding="utf-8")

    identity_check = _run_git(data_root, "config", "--local", "user.email")
    if identity_check is not None and identity_check.returncode != 0:
        _run_git(data_root, "config", "--local", "user.name", "Space Server")
        _run_git(data_root, "config", "--local", "user.email", "space-server@localhost")


def commit(data_root: Path, message: str) -> None:
    """`git add -A` + `git commit -m message` in `data_root`. Muss vom Aufrufer bereits unter
    `Store._file_write_lock()` gehalten werden — serialisiert Git-Aufrufe auch über
    Prozessgrenzen hinweg und verhindert, dass zwei gleichzeitige `git commit`-Prozesse sich
    über `.git/index.lock` in die Quere kommen.
    """
    add_result = _run_git(data_root, "add", "-A")
    if add_result is None or add_result.returncode != 0:
        logger.critical(
            "git add in %s fehlgeschlagen: %s", data_root, add_result.stderr if add_result else ""
        )
        return

    commit_result = _run_git(data_root, "commit", "-m", message)
    if commit_result is None or commit_result.returncode != 0:
        logger.critical(
            "git commit in %s fehlgeschlagen (Message %r): %s",
            data_root,
            message,
            commit_result.stderr if commit_result else "",
        )
