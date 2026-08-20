"""Dataclasses des `storage`-Pakets. Felder folgen dem Frontmatter-Schema aus
docs/concepts/phase1_storage_plan.md §1/§2. Wird mit Phasenabschluss zum
Contract für P2 — Änderungen danach sind eine Scope-Änderung.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any


VISIBILITY_VALUES: frozenset[str] = frozenset({"private", "human"})
DEFAULT_VISIBILITY = "private"


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
    # P6 Step 4 (Plan §1.4): `folder` ist abgeleitet aus dem Dateipfad, NIE Frontmatter.
    folder: str = ""
    visibility: str = DEFAULT_VISIBILITY
    share_read: list[str] = field(default_factory=list)
    share_write: list[str] = field(default_factory=list)
    # Unbekannte Frontmatter-Felder — überleben Round-Trips unangetastet (Entscheidung A).
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass(kw_only=True)
class SpaceInfo:
    """Ein Eintrag in `Store.list_spaces()`."""

    name: str
    item_count: int
    # P6 Step 4: write-Mitglieder der Space-Wurzel-`.share.yml` bzw. vorhandene Ordner, sortiert.
    members: tuple[str, ...] = ()
    folders: tuple[str, ...] = ()


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
    folder: str = ""
    visibility: str = DEFAULT_VISIBILITY
    share_read: list[str] = field(default_factory=list)
    share_write: list[str] = field(default_factory=list)


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


@dataclass(kw_only=True)
class AssetInfo:
    """Ein Bild unter `<space>/_assets/<item_id>/` (Phase 6.5 Block B, fünfte, benannte
    P1-Contract-Öffnung, P6.5-T). Kein Index-Eintrag (P6-AY) — `Store.list_assets()` liest
    das Verzeichnis direkt."""

    id: str  # ast_<8hex>
    mime: str  # image/png|image/jpeg|image/gif|image/webp
    bytes: int
    filename: str  # bereinigt, rein kosmetisch — NIE für die Pfadbildung
    created: datetime


# Statusvokabular je `type` (P2 Step 2, Entscheidung D2). Die CLI hielt ungültige Werte bisher
# nur über `argparse choices` ab — ein zweiter Adapter (MCP) wäre daran vorbeigelaufen. Deshalb
# einmal im Kern statt in jedem Adapter neu.
STATUS_VALUES: dict[str, frozenset[str]] = {
    "note": frozenset({"active", "archived"}),
    "task": frozenset({"open", "done", "archived"}),
}


def valid_statuses(item_type: str) -> frozenset[str]:
    """Erlaubte Statuswerte für `item_type`. Leeres Frozenset bei unbekanntem Typ — der
    Aufrufer unterscheidet damit explizit zwischen "Typ unbekannt" und "Status unbekannt"
    (siehe `store.py` `create()`/`update()`)."""
    return STATUS_VALUES.get(item_type, frozenset())
