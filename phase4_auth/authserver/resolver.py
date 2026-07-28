"""`OAuthTokenResolver` — erfüllt `mcpserver.auth.SpaceResolver` strukturell, ohne es zu
importieren (Plan §1.3: die eine Ausnahme von P4-A/C). Löst ein Bearer-Credential gegen
`AuthStore` auf und gibt ein Objekt mit den Feldern `space`/`token_hash` zurück — kein
`mcpserver.auth.Principal` (das wäre der verbotene Import), die Konstruktion des echten
`Principal` passiert in `mcpserver/asgi.py`, das umgekehrt `authserver` importieren darf.
"""
from __future__ import annotations

from dataclasses import dataclass

from . import crypto
from .store import AuthStore


class ResolveError(Exception):
    """Kein, unbekanntes, abgelaufenes oder widerrufenes Bearer-Token. Trägt bewusst keine
    Detailinformation — spiegelt `mcpserver.auth.AuthError`, ohne es zu importieren."""


@dataclass(frozen=True, kw_only=True)
class ResolvedPrincipal:
    """Erfüllt das Attributpaar, das `mcpserver.auth.Principal` ebenfalls trägt — strukturell,
    kein Vererbungszwang (Plan §1.3)."""

    space: str
    token_hash: str


class OAuthTokenResolver:
    def __init__(self, store: AuthStore) -> None:
        self._store = store

    def resolve(self, credential: str) -> ResolvedPrincipal:
        if not credential:
            raise ResolveError("kein Credential")
        record = self._store.lookup_access_token(credential)
        if record is None:
            raise ResolveError("unbekanntes, abgelaufenes oder widerrufenes Token")
        return ResolvedPrincipal(space=record.space, token_hash=crypto.hash_secret(credential))
