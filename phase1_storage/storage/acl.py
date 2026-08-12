"""Auflösung von `.share.yml`-Freigaben (Plan §1.2). Kennt keine Items, keine Frontmatter — nur
Verzeichnisse und die Textdateien darin. Fail-closed: eine fehlende, kaputte oder unbekannte
Angabe gibt nie mehr Rechte — sie loggt höchstens `critical` und liefert eine leere `Grant`.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)

ACL_FILENAME = ".share.yml"


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

    def members_of_space(self, space: str) -> frozenset[str]:
        """Write-Mitglieder der Space-Wurzel-`.share.yml` — nicht die Vereinigung über den
        ganzen Baum (das ist `grants_for_dir`s Job für ein konkretes Item)."""
        return self._read_one(self._data_root / space / ACL_FILENAME).write
