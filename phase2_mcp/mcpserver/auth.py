"""`Principal`, `SpaceResolver`-Protokoll, `AuthError` (Plan §2.1).

**[2026-08-02 Korrektur, P5 Step 0 A]:** `KeyringTokenResolver` (die Pfad-Token-Implementierung
von `SpaceResolver`) ist entfernt — ihr einziger Aufrufer war `create_app()`s `TokenPathASGI`-Bau,
selbst schon seit dem P4-Schnitt (2026-07-30) tot, siehe `mcpserver/app.py`. `SpaceResolver`
bleibt als Protokoll stehen: `authserver.resolver.OAuthTokenResolver` erfüllt es strukturell,
ohne es zu importieren (Plan §1.2), und dokumentiert damit weiter, welche Form jeder Resolver
haben muss."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


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
