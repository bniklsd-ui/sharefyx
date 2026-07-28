"""`TokenPathASGI` — Pfadsegment → Principal → ContextVar → Delegation (Plan §1.1, §2.4, §4
Step 4). Schneidet das erste verbleibende Pfadsegment als Credential ab, löst es auf, setzt den
Principal im ContextVar und delegiert an die innere MCP-App. Fehlendes oder unbekanntes
Credential → HTTP 401 ohne Body — die beiden Fälle dürfen von außen nicht unterscheidbar sein
(P2-N).

**P4 Step 6 (additiv, siehe `phase4_auth/CLAUDE.md`):** `BearerAuthASGI` (Authorization-Header
statt Pfadsegment, löst über `authserver.resolver.OAuthTokenResolver` auf) und `AuthModeASGI`
(Übergangsweiche `SPACE_AUTH_MODE`, P4-N) kamen dazu. Beide setzen denselben
`scope["state"]["token_hash"]`-Slot mit derselben `sha256`-Funktion wie `TokenPathASGI`
(`authserver.crypto.hash_secret` ist byte-identisch mit `credentials.hash_token`) — deshalb
brauchte `context.py :: assert_principal_matches_request()` **keine** Änderung, obwohl Plan §3.2
eine ankündigt (dort ohne frischen Repo-Zugriff geschrieben, siehe Plan-Kopf). Details/Beleg:
Phase-4-Head, Session-Block Step 6a.
"""
from __future__ import annotations

from typing import Any

from authserver.resolver import ResolveError

from .auth import AuthError, Principal, SpaceResolver
from .context import reset_principal, set_principal

Scope = dict[str, Any]
Receive = Any
Send = Any


def _credential_from_path(scope: Scope) -> tuple[str, str, str]:
    """`(credential, root_path, rest)` — die Segment-Zerlegung, geteilt zwischen `TokenPathASGI`
    und `AuthModeASGI`s `both`-Weiche, damit beide garantiert dieselbe Vorstellung von "ist ein
    Pfad-Token vorhanden" haben."""
    path = scope["path"]
    root_path = scope.get("root_path", "")
    route_path = path[len(root_path):]
    credential, _, rest = route_path.lstrip("/").partition("/")
    return credential, root_path, rest


class TokenPathASGI:
    def __init__(self, app, *, resolver: SpaceResolver) -> None:
        self.app = app
        self.resolver = resolver

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        credential, root_path, rest = _credential_from_path(scope)

        if not credential:
            await _send_401(send)
            return

        try:
            principal = self.resolver.resolve(credential)
        except AuthError:
            await _send_401(send)
            return

        # Pfad für die innere App auf "root_path + rest" kürzen — das Credential-Segment darf
        # FastMCPs eigenes Routing nie sehen. `raw_path` bleibt mit `path` konsistent, sonst
        # widersprechen sich beide für Code, das `raw_path` direkt liest.
        new_path = root_path + "/" + rest if rest else root_path + "/"
        inner_scope = dict(scope)
        inner_scope["path"] = new_path
        inner_scope["raw_path"] = new_path.encode("utf-8")
        # `token_hash` in scope["state"] hinterlegen — das ist, was der Guard in `context.py`
        # später gegen den ContextVar-Principal vergleicht (siehe context.py-Docstring für die
        # Begründung, warum das Token selbst dafür nicht mehr aus dem Pfad lesbar ist).
        inner_scope["state"] = {**scope.get("state", {}), "token_hash": principal.token_hash}

        context_token = set_principal(principal)
        try:
            await self.app(inner_scope, receive, send)
        finally:
            reset_principal(context_token)


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


class AuthModeASGI:
    """Übergangsweiche für `SPACE_AUTH_MODE` (P4-N). Entfällt vollständig in Step 7.

    `mode='oauth'` → immer `BearerAuthASGI`.
    `mode='token'` → immer `TokenPathASGI` (P2-Verhalten, exakt — ignoriert einen mitgesendeten
    `Authorization`-Header vollständig).
    `mode='both'`  → nichtleeres erstes Pfadsegment vorhanden? dann `TokenPathASGI` (Pfad-Token
    hat Vorrang), sonst `BearerAuthASGI`. Ein leeres Segment (`POST /mcp/` ohne Token) zählt als
    "nicht vorhanden" — sonst würde `both` einen reinen Bearer-Aufruf nie erreichen.
    """

    def __init__(self, *, mode: str, bearer: BearerAuthASGI, token_path: TokenPathASGI) -> None:
        self._mode = mode
        self._bearer = bearer
        self._token_path = token_path

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if self._mode == "token":
            await self._token_path(scope, receive, send)
            return
        if self._mode == "oauth":
            await self._bearer(scope, receive, send)
            return
        if scope["type"] == "http":
            credential, _, _ = _credential_from_path(scope)
            if credential:
                await self._token_path(scope, receive, send)
                return
        await self._bearer(scope, receive, send)


async def _send_401(send: Send) -> None:
    await send({"type": "http.response.start", "status": 401, "headers": []})
    await send({"type": "http.response.body", "body": b""})


async def _send_401_challenge(send: Send, *, challenge: str) -> None:
    await send(
        {
            "type": "http.response.start",
            "status": 401,
            "headers": [(b"www-authenticate", challenge.encode("utf-8"))],
        }
    )
    await send({"type": "http.response.body", "body": b""})
