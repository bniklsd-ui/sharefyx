"""Auflösung von `.share.yml`-Freigaben (Plan §1.2). Kennt keine Items, keine Frontmatter — nur
Verzeichnisse und die Textdateien darin. Fail-closed: eine fehlende, kaputte oder unbekannte
Angabe gibt nie mehr Rechte — sie loggt höchstens `critical` und liefert eine leere `Grant`.
"""
from __future__ import annotations

import fcntl
import logging
import shutil
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from . import files, history

logger = logging.getLogger(__name__)

ACL_FILENAME = ".share.yml"


class AclWriteError(ValueError):
    """Ungültiger Space-Name oder sonstiger Abbruch beim Schreiben einer `.share.yml`/eines
    Space-Verzeichnisses. Entspricht den ABBRUCH-Fällen, die `spacectl.py` bisher als
    stderr-Text + Exit-Code meldete — hier als Exception, `spacectl.py` fängt sie und formt
    daraus wieder Text + Exit-Code (Ausgabe muss byte-identisch bleiben, P7-P)."""


@dataclass(frozen=True, kw_only=True)
class Grant:
    read: frozenset[str] = field(default_factory=frozenset)
    write: frozenset[str] = field(default_factory=frozenset)


@dataclass(frozen=True, kw_only=True)
class AclDecision:
    space: str
    folder: str
    visibility: str
    read: frozenset[str]
    write: frozenset[str]
    # Rohe Item-Freigaben, UNGEMISCHT mit der `.share.yml`-Vereinigung in `read`/`write` (Step 7
    # Commit 5, `webui/shares.py :: ShareState`) — Defaults, damit bestehende
    # `AclDecision(...)`-Konstruktionsstellen (Tests) ohne die zwei neuen Felder weiterlaufen,
    # derselbe Kompatibilitäts-Trick wie `Grant`s Defaults oben in dieser Datei.
    share_read: frozenset[str] = field(default_factory=frozenset)
    share_write: frozenset[str] = field(default_factory=frozenset)


class AclReader:
    """Liest `.share.yml`-Dateien unter `data_root`, mit `stat()`-invalidiertem Cache (kein
    TTL, kein Hintergrund-Thread — Plan §1.2.3 Regel 4).

    Namen in `read:`/`write:` sind Principal-Namen (== Space-Namen in diesem System), keine
    freien Strings. Ein Tippfehler dort referenziert schlicht keinen echten Principal und ist
    damit automatisch wirkungslos — `AclReader` validiert das nicht extra (das wäre eine
    zweite, redundante Fehlerquelle); `diagnose.sh` meldet verwaiste Namen operational (Step 6,
    außerhalb dieses Moduls).
    """

    def __init__(self, data_root: Path) -> None:
        self._data_root = Path(data_root)
        self._cache: dict[tuple[Path, float, int], Grant] = {}

    def invalidate(self) -> None:
        self._cache.clear()

    def _read_one(self, share_file: Path) -> Grant:
        try:
            stat = share_file.stat()
        except OSError:
            return Grant()
        key = (share_file, stat.st_mtime, stat.st_size)
        cached = self._cache.get(key)
        if cached is not None:
            return cached
        grant = self._parse(share_file)
        self._cache[key] = grant
        return grant

    def _parse(self, share_file: Path) -> Grant:
        try:
            raw = share_file.read_text(encoding="utf-8")
            data = yaml.safe_load(raw)
        except (OSError, yaml.YAMLError) as exc:
            logger.critical("%s ist nicht lesbar/parsebar, gewaehrt nichts: %s", share_file, exc)
            return Grant()
        if data is None:
            return Grant()
        if not isinstance(data, dict):
            logger.critical("%s ist kein YAML-Mapping, gewaehrt nichts", share_file)
            return Grant()
        write = self._names(data.get("write"))
        read = self._names(data.get("read")) | write  # write impliziert read (Plan §1.2.2)
        return Grant(read=read, write=write)

    @staticmethod
    def _names(value: object) -> frozenset[str]:
        if not isinstance(value, list):
            return frozenset()
        return frozenset(v for v in value if isinstance(v, str))

    def grants_for_dir(self, directory: Path) -> Grant:
        """Vereinigung aller `.share.yml` vom Space-Wurzelverzeichnis bis `directory`
        (Plan §1.2.3 Regel 1) — Vereinigung, nicht "nächster gewinnt". `directory` muss unter
        `data_root` liegen (Aufrufer-Vertrag, wie bei `Path.relative_to`).
        """
        rel = Path(directory).relative_to(self._data_root)
        read: set[str] = set()
        write: set[str] = set()
        current = self._data_root
        for part in rel.parts:
            current = current / part
            grant = self._read_one(current / ACL_FILENAME)
            read |= grant.read
            write |= grant.write
        return Grant(read=frozenset(read), write=frozenset(write))

    def grants_for_space(self, space: str) -> Grant:
        """Grant der Space-Wurzel-`.share.yml` allein (kein Vereinigungs-Walk — die Space-Wurzel
        IST der ganze Walk für sich selbst). Basis für `SharePolicy`s space-level `can_read`/
        `can_write` (P6 Step 5) und für `members_of_space()`."""
        return self._read_one(self._data_root / space / ACL_FILENAME)

    def members_of_space(self, space: str) -> frozenset[str]:
        """Write-Mitglieder der Space-Wurzel-`.share.yml` — nicht die Vereinigung über den
        ganzen Baum (das ist `grants_for_dir`s Job für ein konkretes Item)."""
        return self.grants_for_space(space).write

    def decision_for(
        self, *, space: str, folder: str, visibility: str,
        share_read: Iterable[str], share_write: Iterable[str],
    ) -> AclDecision:
        """Baut eine `AclDecision` aus bereits bekannten Item-Feldern (P6 Step 5) — dieselbe
        Vereinigungslogik, die `Store.acl_of()` sonst inline berechnet hätte, hier einmal
        implementiert, damit `Store.acl_of()` sie aufrufen kann UND ein Aufrufer, der schon eine
        `ItemSummary` aus `search()` in der Hand hat (z. B. `mcpserver.tools.search_items`),
        keinen zweiten Index-Roundtrip pro Zeile braucht."""
        directory = self._data_root / space / folder if folder else self._data_root / space
        grant = self.grants_for_dir(directory)
        item_read = frozenset(share_read)
        item_write = frozenset(share_write)
        return AclDecision(
            space=space, folder=folder, visibility=visibility,
            read=grant.read | item_read | item_write, write=grant.write | item_write,
            share_read=item_read, share_write=item_write,
        )


# -- Schreibseite (P7 Step C1, sechste benannte Contract-Öffnung) -------------------------
#
# Extraktion aus `phase6_shares/scripts/spacectl.py` (Referenz: Zeilen 90-107/113-127/
# 133-148/185-242 zum Zeitpunkt der Extraktion) — kein neues Verhalten, nur eine neue
# Adresse dafür. `spacectl.py` ruft ab diesem Step diese Funktionen auf, statt seine eigenen
# Kopien zu pflegen; Ausgabetexte und Exit-Codes des Skripts bleiben byte-identisch.
#
# Jede Funktion hier nimmt den `.write.lock`-Flock SELBST und gibt ihn vor der Rückkehr
# wieder frei. Kein Aufrufer darf diesen Lock über mehrere Aufrufe hinweg halten, und keine
# dieser Funktionen ruft eine `Store`-Methode auf: `Store._file_write_lock()` und dieser Lock
# hier sperren dieselbe Datei `<data_root>/.write.lock` über verschiedene Open File
# Descriptions. `flock` hängt an der OFD, nicht am Prozess — ein zweites `open()` +
# `flock(LOCK_EX)` im selben Prozess blockiert auf dem ersten, das sich selbst nie wieder
# freigibt (empirisch geprüft in der P7-Planungssession). In einem einprozessig-async
# laufenden Server friert das den ganzen Dienst ein, nicht nur den Request (P7-M).


def _lock_path(data_root: Path) -> Path:
    return data_root / ".write.lock"


class _WriteLock:
    """Wie `spacectl.py`s bisherige `_DataRootLock` — hier die einzige verbleibende Kopie."""

    def __init__(self, data_root: Path) -> None:
        self._lock_path = _lock_path(data_root)
        self._fh = None

    def __enter__(self) -> "_WriteLock":
        self._lock_path.touch(exist_ok=True)
        self._fh = open(self._lock_path, "r+")
        fcntl.flock(self._fh, fcntl.LOCK_EX)
        history.ensure_repo(self._lock_path.parent)
        return self

    def __exit__(self, *exc_info: object) -> None:
        fcntl.flock(self._fh, fcntl.LOCK_UN)
        self._fh.close()


def read_share_file(data_root: Path, space: str) -> dict[str, list[str]]:
    """Wie `AclReader._parse`, aber laut statt fail-closed — wer eine `.share.yml` gerade
    bearbeitet, soll einen kaputten Bestand sofort sehen, nicht stillschweigend überschreiben.
    Fehlt die Datei, liefert das ein leeres Mapping."""
    path = data_root / space / ACL_FILENAME
    if not path.exists():
        return {}
    raw = path.read_text(encoding="utf-8")
    data = yaml.safe_load(raw)
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise AclWriteError(f"{path} ist kein YAML-Mapping")
    return data


def write_share_file(data_root: Path, space: str, data: dict) -> None:
    """Schreibt oder entfernt die `.share.yml` eines Space — leer = nicht vorhanden, dieselbe
    Disziplin wie im Frontmatter (Plan §2.1). Nimmt den Lock selbst, erzeugt **keinen** Commit
    (das bleibt Aufgabe der aufrufenden `add_member`/`remove_member`, die den Betreff kennen)."""
    path = data_root / space / ACL_FILENAME
    with _WriteLock(data_root):
        if data:
            files.atomic_write(path, yaml.safe_dump(
                data, sort_keys=False, allow_unicode=True, default_flow_style=False,
            ))
        elif path.exists():
            path.unlink()


def add_member(data_root: Path, space: str, name: str, *, write: bool) -> bool:
    """Fügt `name` zu `read:` oder `write:` von `space` hinzu. Liefert `True`, wenn dadurch
    etwas geändert wurde, `False` bei einem No-op (Name war bereits in der Liste) — `spacectl.py`
    formt daraus seine bisherige Textmeldung."""
    key = "write" if write else "read"
    path = data_root / space / ACL_FILENAME
    with _WriteLock(data_root):
        data = read_share_file(data_root, space)
        names = set(data.get(key) or [])
        if name in names:
            return False
        names.add(name)
        data[key] = sorted(names)
        files.atomic_write(path, yaml.safe_dump(
            data, sort_keys=False, allow_unicode=True, default_flow_style=False,
        ))
        history.commit(data_root, f"share {space} {key}+={name}")
    return True


def remove_member(data_root: Path, space: str, name: str) -> list[str]:
    """Entfernt `name` aus `read:` UND `write:` von `space`. Liefert die Liste der Listen
    (`["read"]`/`["write"]`/beide), aus denen tatsächlich entfernt wurde — leer, wenn `name`
    in keiner stand (No-op, kein Commit)."""
    path = data_root / space / ACL_FILENAME
    with _WriteLock(data_root):
        data = read_share_file(data_root, space)
        removed: list[str] = []
        for key in ("read", "write"):
            names = set(data.get(key) or [])
            if name in names:
                names.discard(name)
                data[key] = sorted(names)
                removed.append(key)
        if not removed:
            return []
        for key in ("read", "write"):
            if key in data and not data[key]:
                del data[key]
        if data:
            files.atomic_write(path, yaml.safe_dump(
                data, sort_keys=False, allow_unicode=True, default_flow_style=False,
            ))
        elif path.exists():
            path.unlink()
        history.commit(data_root, f"unshare {space} {name}")
    return removed


def create_space(data_root: Path, name: str) -> Path:
    """Legt ein leeres Space-Verzeichnis an. Kein `history.commit()` hier — ein leeres
    Verzeichnis hat für Git nichts zu committen, der erste Item-Write erzeugt den ersten
    echten Commit für diesen Space (wie bisher in `spacectl.py`)."""
    if "/" in name or name.startswith(".") or name in files.RESERVED_DIR_NAMES:
        raise AclWriteError(f"'{name}' ist kein gültiger Space-Name.")
    space_dir = data_root / name
    with _WriteLock(data_root):
        if space_dir.exists():
            raise AclWriteError(f"Space '{name}' existiert bereits.")
        space_dir.mkdir(parents=True)
    return space_dir


def remove_space_dir(data_root: Path, name: str) -> None:
    """Entfernt ein Space-Verzeichnis vollständig (`rmtree`) und committet das. Kein Vorlauf,
    keine Item-Migration hier — das ist Aufgabe der Orchestrierung eine Schicht höher (Block C4,
    `webui/api.py :: _spaces_delete`), die alle Items vorher verschoben/archiviert haben muss.
    Diese Funktion tut nur den letzten, unwiderruflichen Schritt."""
    space_dir = data_root / name
    if not space_dir.is_dir():
        raise AclWriteError(f"Space '{name}' existiert nicht.")
    with _WriteLock(data_root):
        shutil.rmtree(space_dir)
        history.commit(data_root, f"remove-space {name}")


def spaces_referencing(data_root: Path, name: str, *, exclude: Path | None = None) -> list[str]:
    """Alle `.share.yml`-Dateien (außer `exclude`), die `name` in `read:`/`write:` nennen —
    Basis für `remove-space`s Verwaisungswarnung und `spacectl.py check`s Diagnose."""
    hits = []
    for share_path in sorted(data_root.rglob(ACL_FILENAME)):
        if exclude is not None and share_path == exclude:
            continue
        try:
            raw = share_path.read_text(encoding="utf-8")
            data = yaml.safe_load(raw)
        except (OSError, yaml.YAMLError):
            continue  # kaputte Datei ist `check`s Befund, nicht dieser Warnung Aufgabe
        if not isinstance(data, dict):
            continue
        names = set(data.get("read") or []) | set(data.get("write") or [])
        if name in names:
            hits.append(str(share_path.relative_to(data_root)))
    return sorted(hits)
