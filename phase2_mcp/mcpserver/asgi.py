"""`TokenPathASGI` — Pfadsegment → Principal → ContextVar → Delegation (Plan §1.1, §2.4, §4
Step 4). Schneidet das erste verbleibende Pfadsegment als Credential ab, löst es auf, setzt den
Principal im ContextVar und delegiert an die innere MCP-App. Fehlendes oder unbekanntes
Credential → HTTP 401 ohne Body — die beiden Fälle dürfen von außen nicht unterscheidbar sein
(P2-N).
"""
from __future__ import annotations

from typing import Any

from .auth import AuthError, SpaceResolver
from .context import reset_principal, set_principal

Scope = dict[str, Any]
Receive = Any
Send = Any


class TokenPathASGI:
    def __init__(self, app, *, resolver: SpaceResolver) -> None:
        self.app = app
        self.resolver = resolver

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        path = scope["path"]
        root_path = scope.get("root_path", "")
        route_path = path[len(root_path):]
        credential, _, rest = route_path.lstrip("/").partition("/")

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


async def _send_401(send: Send) -> None:
    await send({"type": "http.response.start", "status": 401, "headers": []})
    await send({"type": "http.response.body", "body": b""})
