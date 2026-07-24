"""Fehlertypen des `storage`-Pakets (Plan §1)."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import Item


class SpaceError(Exception):
    """Basis aller Storage-Fehler."""


class ItemNotFound(SpaceError):
    def __init__(self, item_id: str):
        super().__init__(f"Item nicht gefunden: {item_id}")
        self.item_id = item_id


class SpaceNotFound(SpaceError):
    def __init__(self, space: str):
        super().__init__(f"Space nicht gefunden: {space}")
        self.space = space


class ConflictError(SpaceError):
    """Trägt das aktuelle Item (Entscheidung C) — Client kann ohne Zusatz-Roundtrip mergen."""

    def __init__(self, item_id: str, *, expected_version: int, current: "Item"):
        super().__init__(
            f"Konflikt bei {item_id}: erwartete Version {expected_version}, "
            f"aktuell {current.version}"
        )
        self.item_id = item_id
        self.expected_version = expected_version
        self.current = current


class ValidationError(SpaceError):
    pass


class IndexCorrupt(SpaceError):
    """Ersetzt den im Plan vorgeschlagenen Namen `IndexError_` — kollidiert mit dem
    Python-Builtin `IndexError`. Bislang nicht geworfen (`index.connect()` heilt Korruption
    still statt zu eskalieren); reserviert für einen Aufrufer, der das sichtbar machen will.
    """
