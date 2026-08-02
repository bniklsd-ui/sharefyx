"""`OAuthTokenResolver` — erfüllt `mcpserver.auth.SpaceResolver` strukturell, ohne es zu
importieren (Plan §1.3: die eine Ausnahme von P4-A/C). Löst ein Bearer-Credential gegen
`AuthStore` auf und gibt ein Objekt mit den Feldern `space`/`token_hash` zurück — kein
`mcpserver.auth.Principal` (das wäre der verbotene Import), die Konstruktion des echten
`Principal` passiert in `mcpserver/asgi.py`, das umgekehrt `authserver` importieren darf.

**S3/S4 (Sicherheits-Review 2026-07-29):** vorher wurde weder die `resource` (RFC 8707
Audience-Bindung) noch der `scope` (muss `space` enthalten, sonst kein Tool-Zugriff) beim
tatsächlichen Zugriff geprüft — beide wurden nur bei `/oauth/authorize` validiert und dann nie
wieder angesehen. Ein Token für eine andere Ressource oder mit ausschließlich
`offline_access`-Scope hätte trotzdem vollen `/mcp`-Zugriff bekommen.
"""
from __future__ import annotations

from dataclasses import dataclass

from . import crypto
from .store import AuthStore

REQUIRED_MCP_SCOPE = "space"


class ResolveError(Exception):
    """Kein, unbekanntes, abgelaufenes oder widerrufenes Bearer-Token — oder eines, das auf eine
    andere Ressource ausgestellt wurde oder keinen `space`-Scope trägt. Trägt bewusst keine
    Detailinformation — spiegelt `mcpserver.auth.AuthError`, ohne es zu importieren."""


@dataclass(frozen=True, kw_only=True)
class ResolvedPrincipal:
    """Erfüllt das Attributpaar, das `mcpserver.auth.Principal` ebenfalls trägt — strukturell,
    kein Vererbungszwang (Plan §1.3)."""

    space: str
    token_hash: str


class OAuthTokenResolver:
    def __init__(self, store: AuthStore, *, expected_resource: str) -> None:
        self._store = store
        self._expected_resource = expected_resource

    def resolve(self, credential: str) -> ResolvedPrincipal:
        if not credential:
            raise ResolveError("kein Credential")
        record = self._store.lookup_access_token(credential)
        if record is None:
            raise ResolveError("unbekanntes, abgelaufenes oder widerrufenes Token")
        if record.resource != self._expected_resource:
            raise ResolveError("Token für eine andere Ressource ausgestellt")
        if REQUIRED_MCP_SCOPE not in record.scope.split():
            raise ResolveError(f"Token trägt keinen {REQUIRED_MCP_SCOPE!r}-Scope")
        return ResolvedPrincipal(space=record.space, token_hash=crypto.hash_secret(credential))
