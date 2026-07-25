"""`Permissions`-Protokoll + P2-Policy (Plan §2.2). Zwei getrennte Seams (`auth.py` beantwortet
*wer bin ich*, dieses Modul *wer darf was*) — eine spätere `PolicyPermissions` mit echten
Lese-Regeln zwischen Spaces ist ein Konstruktor-Austausch, kein Umbau.
"""
from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol


class Permissions(Protocol):
    def can_read(self, actor: str, target: str) -> bool: ...
    def can_write(self, actor: str, target: str) -> bool: ...
    def visible_spaces(self, actor: str, all_spaces: Sequence[str]) -> list[str]: ...


class OwnSpaceWritable:
    """P2-Policy: alles lesbar, nur der eigene Space schreibbar. `can_read` gibt heute immer
    `True` zurück, wird aber schon von jedem Lesepfad aufgerufen — der Seam für spätere
    Lese-Rechte zwischen Spaces existiert damit ab Tag 1 (siehe ROADMAP „Zurückgestellt aus P2").
    """

    def can_read(self, actor: str, target: str) -> bool:
        return True

    def can_write(self, actor: str, target: str) -> bool:
        return actor == target

    def visible_spaces(self, actor: str, all_spaces: Sequence[str]) -> list[str]:
        return [space for space in all_spaces if self.can_read(actor, space)]
