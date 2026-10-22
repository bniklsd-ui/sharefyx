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

**P10.5, Block 2 (2026-10-22):** die Policy kennt jetzt auch **Home-Spaces** (ein Space, der
einem Nutzer gehört) und **Team-Spaces** (ein geteilter Space, der niemandem gehört) — vorher
kannte nur die Web-Oberfläche diese Unterscheidung, die Agentenfläche gar nicht. Der
Home-Space comes from the Auth-DB, deshalb bekommt die Policy ein Prädikat
(`is_home_space`); die vier neuen Methoden `is_home_space()`/`is_team_space()`/
`manages_space()`/`may_move_between()` sind die **eine** Regel für Web und MCP (RE-1, RE-2,
P10-I, P10.5-N).
"""
from __future__ import annotations

from collections.abc import Callable, Sequence
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
    def can_write_item(self, actor: str, acl: AclDecision, *, surface: Surface) -> bool: ...
    def visible_spaces(self, actor: str, all_spaces: Sequence[str]) -> list[str]: ...


class SharePolicy:
    """Ersetzt `OwnSpaceWritable`. Braucht den `AclReader`, sonst kennt sie keine
    Mitgliedschaft — `mcpserver/app.py` baut genau eine Instanz und teilt sie mit dem `Store`
    (`store.acl_reader`), damit `AclReader`s `stat()`-invalidierter Cache nicht zweimal
    unabhängig veraltet (Plan §1.2.3 Regel 4).

    **Home-Spaces (P10.5, Block 2):** „ein Space, der niemandem gehört" (Team-Space) und „ein
    Space, der einem Nutzer gehört" (Home-Space) sind zwei verschiedene Dinge, und nur die
    Auth-DB weiß, welches ist. Deshalb bekommt die Policy ein **Prädikat**
    (`is_home_space`, gesetzt in `mcpserver/app.py :: create_app()` aus
    `oauth.store.get_user(space) is not None` — die Zeilenabfrage ohne TOTP-Entschlüsselung).
    **Ohne Prädikat kennt die Policy keinen Home-Space**, und sie behandelt dann fail-closed:
    `is_team_space()` ist `False` (keine Team-Rechte), `manages_space()` nur „der eigene Space".
    Wer eine Policy ohne Prädikat baut, bekommt also **weniger** Rechte, nicht mehr — das ist die
    sichere Richtung; der Produktivpfad setzt das Prädikat immer."""

    def __init__(
        self,
        acl: AclReader,
        *,
        is_home_space: Callable[[str], bool] | None = None,
    ) -> None:
        self._acl = acl
        self._is_home_space = is_home_space

    def can_read(self, actor: str, target: str) -> bool:
        if actor == target:
            return True
        return actor in self._acl.grants_for_space(target).read

    def can_write(self, actor: str, target: str) -> bool:
        if actor == target:
            return True
        return actor in self._acl.grants_for_space(target).write

    # -- Home-Spaces und Team-Spaces (P10.5, Block 2: RE-1, RE-2, P10-I/P10.5-N) --------------
    #
    # Diese vier Methoden sind die **eine** Regel für Web und MCP (D-17, Lock P10.5-N): vorher
    # kannte die Web-Oberfläche „Team-Space" über die Auth-DB (REST-Adapter, `api.py ::
    # _is_team_space`) und die Agentenfläche gar nicht — zwei Wege, zwei Regeln.

    def is_home_space(self, space: str) -> bool:
        """Gehört `space` einem Nutzer? Ohne Prädikat **immer `False`** — die Policy kennt
        dann keinen Home-Space (siehe Klassen-Docstring)."""
        if self._is_home_space is None:
            return False
        return bool(self._is_home_space(space))

    def is_team_space(self, space: str) -> bool:
        """Gehört `space` niemandem, sondern ist ein geteilter Space?

        **Fail-closed (Plan Block 2):** ohne Home-Space-Prädikat ist die Antwort `False` — ein
        Space ohne Prädikat ist *kein belegter* Team-Space, und Team-Rechte gibt es nur dort, wo
        der Space niemandem gehört. Wer kein Prädikat liefert, sperrt sich also selbst, statt
        Rechte zu erfinden."""
        if self._is_home_space is None:
            return False
        return not self._is_home_space(space)

    def manages_space(self, actor: str, space: str) -> bool:
        """Darf `actor` in `space` wie der Eigentümer handeln (Ordner anlegen, Items
        verschieben)? Zwei Fälle:

        * `actor == space` — der eigene Space, immer.
        * `space` ist ein **Team-Space** und `actor` hat dort **space-level** Schreibrecht
          (`write:` in der `.share.yml` des Space-Wurzelverzeichnisses). Ein `share_write` auf
          einem einzelnen Item reicht nicht (P9-BP).

        Fremde **Home**-Spaces sind nie „verwaltbar" — dort bleibt es beim Eigentümer
        (P10-I/P10.5-N)."""
        if actor == space:
            return True
        return self.is_team_space(space) and self.can_write(actor, space)

    def may_move_between(self, actor: str, source: str, target: str) -> bool:
        """Darf ein Item von `source` nach `target` wandern? Zwei Sperren, beide aus der
        Nikinger-Entscheidung vom 2026-10-20/21 (P10-I, P10.5-N):

        * **P10-I:** nichts wandert **in** den Home-Space eines anderen. Ein Item im fremden
          Home-Space zu haben ist dort eine Lücke; hineinzuschieben wäre genauso.
        * **P10.5-N:** nichts wandert **aus** dem Home-Space eines anderen heraus — das wäre
          dort ein Löschen (P9-K sperrt Löschen in fremden Home-Spaces).

        Der eigene Space des Akteurs ist in **beiden** Richtungen frei (er ist dessen
        Home-Space). Team-Spaces sind frei — sie gehören niemandem.

        **Ohne Prädikat** (kein Home-Space bekannt) kann die Policy keine der beiden Sperren
        anwenden und gibt `True` zurück; das ist der einzige Weg, an dem diese Regel fehlen
        kann — der Produktivpfad setzt das Prädikat immer (`create_app()`), und die Adapter
        rufen zusätzlich `can_write()` auf Quelle **und** Ziel (P6-AE)."""
        if target != actor and self.is_home_space(target):
            return False
        if source != actor and self.is_home_space(source):
            return False
        return True

    def can_read_item(self, actor: str, acl: AclDecision, *, surface: Surface) -> bool:
        # P6-P: `visibility: human` existiert für die Agentenfläche vollständig nicht — sticht
        # jede andere Freigabe, auch für den Eigentümer-Space selbst wäre die Frage hier gar
        # nicht relevant (der Eigentümer ruft nie can_read_item auf eigene Items auf).
        if surface is Surface.AGENT and acl.visibility == "human":
            return False
        if actor == acl.space:
            return True
        return actor in acl.read

    def can_write_item(self, actor: str, acl: AclDecision, *, surface: Surface) -> bool:
        # **Fix, 2026-08-12, Advisor-Fund nach dem ersten Step-5-Commit:** `can_write_item`
        # hatte ursprünglich (wie der Plan-Snippet in §1.2.4) keinen `surface`-Parameter — ein
        # `visibility: human`-Item war damit für die Agentenfläche zwar unlesbar, aber weiterhin
        # voll beschreibbar über den eigenen Space-Token (append/update erreichten `store.
        # append()`/`update()`, ein Versionskonflikt hätte sogar Version/Zeitstempel des
        # angeblich "vollständig nicht existenten" Items in der Fehlermeldung preisgegeben).
        # Dieselbe Sperre wie `can_read_item` schließt das: kann die Agentenfläche es nicht
        # lesen, darf sie es erst recht nicht schreiben.
        if surface is Surface.AGENT and acl.visibility == "human":
            return False
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

    def can_write_item_as_human(self, actor: str, acl: AclDecision) -> bool:
        """Bequemlichkeitsmethode, Zwilling zu `can_read_item_as_human()` — gleicher Grund
        (P5-B, kein zweiter `mcpserver`-Import im REST-Adapter, anderes Paket)."""
        return self.can_write_item(actor, acl, surface=Surface.HUMAN)

    def visible_spaces(self, actor: str, all_spaces: Sequence[str]) -> list[str]:
        return [space for space in all_spaces if self.can_read(actor, space)]
