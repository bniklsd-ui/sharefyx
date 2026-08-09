"""Punktuelle Textersetzung im Item-Body (Plan §1.5.2/§4 Step 1, P6-E/F/G). `apply_edits()`
kennt weder `Store` noch das Dateisystem und wirft `PatchError` bei jedem Treffer ≠ 1 — "alles
oder nichts" ist damit eine Aufrufreihenfolge in `Store.patch()` (Anwenden vor dem Schreiben),
keine eigene Transaktionslogik.
"""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, TypedDict

from .errors import ValidationError

if TYPE_CHECKING:
    from .models import Item


class TextEdit(TypedDict):
    old_text: str
    new_text: str


class PatchError(ValidationError):
    """Trägt Index/Trefferzahl/Zeilennummern (P6-F) — der handlungsfähige Fehlertext entsteht
    im Adapter (`mcpserver/tools.py :: map_storage_error`), wie bei `ConflictError` auch.
    `lines` ist auf die ersten zwei Fundstellen gedeckelt (reicht für die Fehlermeldung
    „Zeilen 12, 40, …"); `found` trägt die tatsächliche Gesamtzahl.
    """

    def __init__(self, *, index: int, found: int, lines: list[int]) -> None:
        super().__init__(f"edits[{index}] fand {found} Treffer, erwartet genau 1")
        self.index = index
        self.found = found
        self.lines = lines


@dataclass(frozen=True, kw_only=True)
class PatchResult:
    item: "Item"
    replacements: int
    lines: tuple[int, ...]  # 1-basierte Zeilennummern der angewandten Ersetzungen
    # Bytes des Bodys (nicht der Datei) vor/nach dem Patch — dieselbe Größe, die die Quittung
    # als "bytes" ausliefert (mcpserver/receipts.py).
    bytes_before: int
    bytes_after: int


def _line_number(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def _find_all(text: str, needle: str) -> list[int]:
    """Alle (auch überlappenden) Fundstellen — ein leeres `old_text` liefert dadurch weit mehr
    als eine Fundstelle und schlägt über den normalen `found != 1`-Pfad fehl, keine eigene
    Sonderbehandlung nötig."""
    positions = []
    start = 0
    while True:
        pos = text.find(needle, start)
        if pos == -1:
            break
        positions.append(pos)
        start = pos + 1
    return positions


def apply_edits(body: str, edits: Sequence[TextEdit]) -> tuple[str, tuple[int, ...]]:
    """Wendet `edits` sequenziell auf `body` an — jede folgende Ersetzung sieht bereits das
    Ergebnis der vorherigen (spätere Anker dürfen von früheren Ersetzungen abhängen). Jedes
    `old_text` muss zum Zeitpunkt seiner Anwendung genau einmal vorkommen, sonst wirft diese
    Funktion `PatchError` und lässt `body` unverändert — sie schreibt nichts, ändert nichts
    außerhalb ihres eigenen lokalen `text`.
    """
    text = body
    applied_lines: list[int] = []
    for index, edit in enumerate(edits):
        old_text = edit["old_text"]
        new_text = edit["new_text"]
        positions = _find_all(text, old_text)
        if len(positions) != 1:
            raise PatchError(
                index=index, found=len(positions),
                lines=[_line_number(text, p) for p in positions[:2]],
            )
        pos = positions[0]
        applied_lines.append(_line_number(text, pos))
        text = text[:pos] + new_text + text[pos + len(old_text):]
    return text, tuple(applied_lines)
