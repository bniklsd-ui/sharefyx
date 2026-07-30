"""`BearerAuthASGI` — Authorization-Header → Principal → ContextVar → Delegation (Plan §3.1).
Löst über `authserver.resolver.OAuthTokenResolver` auf. Fehlender oder unbekannter/abgelaufener/
widerrufener Token → HTTP 401 mit `WWW-Authenticate` — kein Lazy-Auth, alle sechs Tools sind
geschützt.

**Schnitt, 2026-07-30 (Runbook-Schritt 8, Plan §5 Step 7 Punkt 8):** `TokenPathASGI` (Pfad-
Segment → `SpaceResolver`, P2) und `AuthModeASGI` (Übergangsweiche `SPACE_AUTH_MODE ∈
{token, oauth, both}`, P4-N) sind entfernt — beide Pfad-Token sind live widerrufen, der Dienst
läuft nur noch mit `SPACE_AUTH_MODE=oauth`. `BearerAuthASGI` setzt denselben
`scope["state"]["token_hash"]`-Slot mit derselben `sha256`-Funktion, die vorher `TokenPathASGI`
benutzte (`authserver.crypto.hash_secret` ist byte-identisch mit `credentials.hash_token`) —
deshalb brauchte `context.py :: assert_principal_matches_request()` auch nach dieser
Vereinfachung keine Änderung.
"""
from __future__ import annotations

from typing import Any

from authserver.resolver import ResolveError

from .auth import Principal
from .context import reset_principal, set_principal

Scope = dict[str, Any]
Receive = Any
Send = Any


def _bearer_credential(scope: Scope) -> str | None:
    headers = dict(scope.get("headers") or [])
    raw = headers.get(b"authorization")
    if raw is None:
        return None
    scheme, _, token = raw.decode("latin-1").partition(" ")
    if scheme.lower() != "bearer" or not token:
        return None
    return token


class BearerAuthASGI:
    """Liest `Authorization: Bearer <token>`, löst über einen Resolver auf, der ein Objekt mit
    `space`/`token_hash` liefert (strukturell wie `SpaceResolver.resolve()`, hier aber
    `authserver.resolver.OAuthTokenResolver` — siehe Moduldocstring, warum dessen
    `ResolveError` bewusst separat von `AuthError` bleibt, statt beide auf einen gemeinsamen
    Basistyp zu ziehen: `authserver` darf `mcpserver.auth` nicht importieren, P4-A/C). Fehlt der
    Header oder ist der Token unbekannt/abgelaufen/widerrufen: 401 mit `WWW-Authenticate`. Der
    Body ist beratend, das Signal ist Status + Header — kein Lazy-Auth, alle sechs Tools sind
    geschützt (Plan §3.1).
    """

    def __init__(self, app, *, resolver, challenge: str) -> None:
        self.app = app
        self.resolver = resolver
        self.challenge = challenge

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        credential = _bearer_credential(scope)
        if credential is None:
            await _send_401_challenge(send, challenge=self.challenge)
            return

        try:
            resolved = self.resolver.resolve(credential)
        except ResolveError:
            await _send_401_challenge(send, challenge=self.challenge)
            return

        principal = Principal(space=resolved.space, token_hash=resolved.token_hash)
        inner_scope = dict(scope)
        inner_scope["state"] = {**scope.get("state", {}), "token_hash": principal.token_hash}

        context_token = set_principal(principal)
        try:
            await self.app(inner_scope, receive, send)
        finally:
            reset_principal(context_token)


async def _send_401_challenge(send: Send, *, challenge: str) -> None:
    await send(
        {
            "type": "http.response.start",
            "status": 401,
            "headers": [(b"www-authenticate", challenge.encode("utf-8"))],
        }
    )
    await send({"type": "http.response.body", "body": b""})
