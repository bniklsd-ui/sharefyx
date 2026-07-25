"""`Principal`, `SpaceResolver`-Protokoll, `KeyringTokenResolver`, `AuthError` (Plan §2.1).
Auflösung ist ein Dict-Lookup über `sha256(credential)`, kein String-Vergleich über das
Klartext-Token — kein Timing-Kanal über die Tokenlänge, kein Klartext-Geheimnis im Speicher.
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Protocol

from . import credentials


@dataclass(frozen=True, kw_only=True)
class Principal:
    space: str  # der eigene Space — Ziel aller Schreiboperationen
    token_hash: str  # sha256-Hex; nur für Guard und gekürzte Logs, nie vollständig geloggt

    def __repr__(self) -> str:
        return f"Principal(space={self.space!r}, token_hash={self.token_hash[:8]!r}…)"


class AuthError(Exception):
    """Kein oder unbekanntes Credential. Trägt bewusst keine Detailinformation."""


class SpaceResolver(Protocol):
    def resolve(self, credential: str) -> Principal: ...


class KeyringTokenResolver:
    """Löst ein Pfad-Credential gegen die im Keyring gespeicherte Token→Space-Map auf.
    `load_map` ist injiziert — genau wie `now_fn` in P1 — Unit-Tests reichen ein Dict herein
    und fassen nie einen echten Keyring an.
    """

    def __init__(
        self, *, load_map: Callable[[], dict[str, str]] = credentials.load_space_map
    ) -> None:
        self._load_map = load_map
        self._map: dict[str, str] = {}
        self.reload()

    def reload(self) -> None:
        """Lädt die Map neu. Wird beim Start einmal aufgerufen (Konstruktor); ein späterer
        `issue`/`revoke` während der Serverlaufzeit wird erst nach einem Neustart sichtbar —
        das ist für P2 bewusst so (kein Hot-Reload-Feature im Scope).
        """
        self._map = self._load_map()

    def resolve(self, credential: str) -> Principal:
        if not credential:
            raise AuthError("kein Credential")
        token_hash = credentials.hash_token(credential)
        space = self._map.get(token_hash)
        if space is None:
            raise AuthError("unbekanntes Credential")
        return Principal(space=space, token_hash=token_hash)
