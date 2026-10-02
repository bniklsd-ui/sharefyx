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

# P9 Block trace (P9-AC): der Autor geht als **eigenes argv-Element** an `--author`, deshalb
# braucht es hier keine Shell-Quoting. Verboten sind genau die Zeichen, die die Form
# `Name <mail>` zerlegen oder einen zweiten Commit-Parameter einschleusen koennten. Ein Name
# mit einem davon ist ein Datenfehler, kein Schreibfehler: der Commit laeuft trotzdem, nur eben
# mit der Default-Identitaet (`Space Server`) — History geht immer, Auth-Buchhaltung nie auf
# Kosten der Historie.
_AUTHOR_FORBIDDEN = ("<", ">", "\n", "\r")


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

    # Unconditional (nicht nur beim frischen Init): ein von Hand angelegtes oder aus einem
    # Backup wiederhergestelltes DATA_ROOT-Repo hätte sonst nie eine .gitignore und der erste
    # commit() würde .index.sqlite3 (+ WAL/SHM) und .write.lock einchecken — Verstoß gegen
    # Entscheidung A.
    gitignore = data_root / ".gitignore"
    if not gitignore.exists():
        gitignore.write_text(_GITIGNORE_CONTENT, encoding="utf-8")

    identity_check = _run_git(data_root, "config", "--local", "user.email")
    if identity_check is not None and identity_check.returncode != 0:
        _run_git(data_root, "config", "--local", "user.name", "Space Server")
        _run_git(data_root, "config", "--local", "user.email", "space-server@localhost")


def _author_args(author: str) -> list[str]:
    """P9-AC: `--author`-Argumente fuer `author` — leer, wenn kein Akteur bekannt ist (P9-AB:
    lieber der alte `updated_by` als ein erfundener) oder wenn der Name die Form
    `Name <mail>` sprengen wuerde. Der Adress-teil ist bewusst `.invalid` (RFC 2606): es gibt
    keine Mail-Zustellung, die E-Mail-Adresse steht nur, damit Git eine syntaktisch gueltige
    Identitaet hat — `git log --format=%an` und `git blame` lesen den **Namen** davor."""
    if not author:
        return []
    if any(ch in author for ch in _AUTHOR_FORBIDDEN):
        logger.warning(
            "Git-Autor %r verworfen (enthaelt eines von %r) — der Commit laeuft mit der "
            "Default-Identitaet, der Inhalt ist unberuehrt",
            author, _AUTHOR_FORBIDDEN,
        )
        return []
    return ["--author", f"{author} <{author}@sharefyx.invalid>"]


def commit(data_root: Path, message: str, author: str = "") -> None:
    """`git add -A` + `git commit -m message` in `data_root`. Muss vom Aufrufer bereits unter
    `Store._file_write_lock()` gehalten werden — serialisiert Git-Aufrufe auch über
    Prozessgrenzen hinweg und verhindert, dass zwei gleichzeitige `git commit`-Prozesse sich
    über `.git/index.lock` in die Quere kommen.

    `author` (P9-AC) setzt `--author`; der **Committer** bleibt `Space Server`. Das ist
    Absicht: Committer ist die Maschine ("welcher Prozess"), Autor der Mensch bzw. dessen
    Space ("wer hat es gewollt") — dieselbe Unterscheidung, die `git log` seit jeher zeigt und
    die ein Zugriff auf fremde Commits nicht verauscht.
    """
    add_result = _run_git(data_root, "add", "-A")
    if add_result is None or add_result.returncode != 0:
        logger.critical(
            "git add in %s fehlgeschlagen: %s", data_root, add_result.stderr if add_result else ""
        )
        return

    author_args = _author_args(author)
    commit_result = _run_git(data_root, "commit", "-m", message, *author_args)
    if commit_result is None or commit_result.returncode != 0:
        logger.critical(
            "git commit in %s fehlgeschlagen (Message %r, Autor %r): %s",
            data_root,
            message,
            author or None,
            commit_result.stderr if commit_result else "",
        )

