"""`Permissions`-Protokoll + `SharePolicy` (Plan §1.2.4, P6 Step 5). Zwei getrennte Seams
(`auth.py` beantwortet *wer bin ich*, dieses Modul *wer darf was*).

**P6 Step 5:** `OwnSpaceWritable` (P2) ist entfernt, nicht danebengestellt — "zwei Policies,
von denen eine tot ist, sind eine Falle für `grep`" (Plan §1.2.4). `SharePolicy` braucht einen
`storage.acl.AclReader`, um Mitgliedschaft (`.share.yml`) und Item-Freigaben aufzulösen; sie
kennt selbst keine Items, nur die vier Quellen aus Plan §1.2.1. `can_read`/`can_write` bleiben
space-level (für `list_spaces`/`visible_spaces` und `create_item`s "darf ich in diesen anderen
Space schreiben"-Frage, bevor ein Item existiert); `can_read_item`/`can_write_item` sind die
neuen item-level Entscheidungen, gebaut aus einer bereits aufgelösten `AclDecision`
(`Store.acl_of()` oder `AclReader.decision_for()`, storage/acl.py).
"""
from __future__ import annotations

from collections.abc import Sequence
from enum import Enum
from typing import Protocol

from storage.acl import AclDecision, AclReader


class Surface(str, Enum):
    """Welcher Adapter fragt — an genau einer Stelle je Adapter gesetzt, nie aus dem Request
    abgeleitet (Plan §1.2.4): `tools.py` immer `AGENT`, der REST-Adapter (`api.py`, anderes
    Paket) immer `HUMAN`. Dieselbe architektonische Trennung wie P5-D/F, eine Schicht tiefer."""

    AGENT = "agent"
    HUMAN = "human"


class Permissions(Protocol):
    def can_read(self, actor: str, target: str) -> bool: ...
    def can_write(self, actor: str, target: str) -> bool: ...
    def can_read_item(self, actor: str, acl: AclDecision, *, surface: Surface) -> bool: ...
    def can_write_item(self, actor: str, acl: AclDecision) -> bool: ...
    def visible_spaces(self, actor: str, all_spaces: Sequence[str]) -> list[str]: ...


class SharePolicy:
    """Ersetzt `OwnSpaceWritable`. Braucht den `AclReader`, sonst kennt sie keine
    Mitgliedschaft — `mcpserver/app.py` baut genau eine Instanz und teilt sie mit dem `Store`
    (`store.acl_reader`), damit `AclReader`s `stat()`-invalidierter Cache nicht zweimal
    unabhängig veraltet (Plan §1.2.3 Regel 4)."""

    def __init__(self, acl: AclReader) -> None:
        self._acl = acl

    def can_read(self, actor: str, target: str) -> bool:
        if actor == target:
            return True
        return actor in self._acl.grants_for_space(target).read

    def can_write(self, actor: str, target: str) -> bool:
        if actor == target:
            return True
        return actor in self._acl.grants_for_space(target).write

    def can_read_item(self, actor: str, acl: AclDecision, *, surface: Surface) -> bool:
        # P6-P: `visibility: human` existiert für die Agentenfläche vollständig nicht — sticht
        # jede andere Freigabe, auch für den Eigentümer-Space selbst wäre die Frage hier gar
        # nicht relevant (der Eigentümer ruft nie can_read_item auf eigene Items auf).
        if surface is Surface.AGENT and acl.visibility == "human":
            return False
        if actor == acl.space:
            return True
        return actor in acl.read

    def can_write_item(self, actor: str, acl: AclDecision) -> bool:
        if actor == acl.space:
            return True
        return actor in acl.write

    def can_read_item_as_human(self, actor: str, acl: AclDecision) -> bool:
        """Bequemlichkeitsmethode für den REST-Adapter (`api.py`, anderes Paket), nicht Teil
        des `Permissions`-Protokolls: P5-B erlaubt diesem Paket genau EIN Symbol aus
        `mcpserver` (`SharePolicy` selbst) — ein zusätzlicher `Surface`-Import wäre ein
        zweites. Äquivalent zu `can_read_item(actor, acl, surface=Surface.HUMAN)`. `tools.py`
        liegt dagegen im selben Paket wie `Surface` und benutzt die allgemeine Methode direkt
        (Plan §1.2.4)."""
        return self.can_read_item(actor, acl, surface=Surface.HUMAN)

    def visible_spaces(self, actor: str, all_spaces: Sequence[str]) -> list[str]:
        return [space for space in all_spaces if self.can_read(actor, space)]
