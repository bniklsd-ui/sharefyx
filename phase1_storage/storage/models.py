"""Dataclasses des `storage`-Pakets. Felder folgen dem Frontmatter-Schema aus
docs/concepts/phase1_storage_plan.md §1/§2. Wird mit Phasenabschluss zum
Contract für P2 — Änderungen danach sind eine Scope-Änderung.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any


@dataclass(kw_only=True)
class Item:
    """Ein Note- oder Task-Item. `type` unterscheidet die Bedeutung, keine Subklasse (Entscheidung B)."""

    id: str
    space: str
    type: str  # "note" | "task"
    title: str
    status: str
    body: str = ""
    due: date | None = None
    tags: list[str] = field(default_factory=list)
    links: list[str] = field(default_factory=list)
    created: datetime
    updated: datetime
    version: int
    # Unbekannte Frontmatter-Felder — überleben Round-Trips unangetastet (Entscheidung A).
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass(kw_only=True)
class SpaceInfo:
    """Ein Eintrag in `Store.list_spaces()`."""

    name: str
    item_count: int


@dataclass(kw_only=True)
class ItemSummary:
    """Eine Trefferzeile in `SearchResult` — Frontmatter plus Snippet, nie der volle Body."""

    id: str
    space: str
    type: str
    title: str
    status: str
    due: date | None = None
    tags: list[str] = field(default_factory=list)
    links: list[str] = field(default_factory=list)
    created: datetime
    updated: datetime
    version: int
    snippet: str


@dataclass(kw_only=True)
class SearchResult:
    """Ergebnis von `Store.search()`."""

    items: list[ItemSummary]
    total: int
    limit: int
    offset: int


@dataclass(kw_only=True)
class IndexStats:
    """Ergebnis von `Store.rebuild_index()`."""

    items_indexed: int
    duration_seconds: float
