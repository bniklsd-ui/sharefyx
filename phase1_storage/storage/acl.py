"""Auflösung von `.share.yml`-Freigaben (Plan §1.2). Kennt keine Items, keine Frontmatter — nur
Verzeichnisse und die Textdateien darin. Fail-closed: eine fehlende, kaputte oder unbekannte
Angabe gibt nie mehr Rechte — sie loggt höchstens `critical` und liefert eine leere `Grant`.
"""
from __future__ import annotations

import logging
from collections.abc import Iterable
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
