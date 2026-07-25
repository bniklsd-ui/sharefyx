"""Isolierte ASGI-Tests für `TokenPathASGI` — keine echte FastMCP-App, keine echte HTTP-
Verbindung. Ein Fake-Resolver und eine Fake-Innen-App reichen, um Pfad-Rewrite, 401-Verhalten
und ContextVar-Lifecycle zu prüfen (das ist genau die Schicht, die `TokenPathASGI` selbst
verantwortet — die reale FastMCP-Integration wird in Step 5 end-to-end getestet).
"""
import pytest

from mcpserver import context
from mcpserver.asgi import TokenPathASGI
from mcpserver.auth import AuthError, Principal


class _FakeResolver:
    def __init__(self, mapping: dict[str, Principal]) -> None:
        self._mapping = mapping

    def resolve(self, credential: str) -> Principal:
        principal = self._mapping.get(credential)
        if principal is None:
            raise AuthError("unbekannt")
        return principal


def _http_scope(path: str) -> dict:
    return {
        "type": "http",
        "method": "POST",
        "path": path,
        "raw_path": path.encode("utf-8"),
        "root_path": "",
        "headers": [],
        "query_string": b"",
    }


async def _run(app, scope) -> list[dict]:
    sent: list[dict] = []

    async def receive():
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(message):
        sent.append(message)

    await app(scope, receive, send)
    return sent


@pytest.mark.asyncio
async def test_missing_token_401():
    async def inner(scope, receive, send):
        raise AssertionError("darf bei fehlendem Token nie aufgerufen werden")

    app = TokenPathASGI(inner, resolver=_FakeResolver({}))
    sent = await _run(app, _http_scope("/"))

    assert sent[0]["type"] == "http.response.start"
    assert sent[0]["status"] == 401
    assert sent[-1]["body"] == b""


@pytest.mark.asyncio
async def test_unknown_token_401():
    async def inner(scope, receive, send):
        raise AssertionError("darf bei unbekanntem Token nie aufgerufen werden")

    app = TokenPathASGI(inner, resolver=_FakeResolver({}))
    sent = await _run(app, _http_scope("/nope"))

    assert sent[0]["status"] == 401


@pytest.mark.asyncio
async def test_path_is_rewritten_for_inner_app():
    principal = Principal(space="nikinger", token_hash="deadbeef")
    seen_scope: dict = {}

    async def inner(scope, receive, send):
        seen_scope.update(scope)
        await send({"type": "http.response.start", "status": 200, "headers": []})
        await send({"type": "http.response.body", "body": b""})

    app = TokenPathASGI(inner, resolver=_FakeResolver({"tok123": principal}))
    await _run(app, _http_scope("/tok123/rest/of/path"))

    assert seen_scope["path"] == "/rest/of/path"
    assert seen_scope["raw_path"] == b"/rest/of/path"
    assert seen_scope["state"]["token_hash"] == "deadbeef"


@pytest.mark.asyncio
async def test_principal_reset_after_request():
    principal = Principal(space="nikinger", token_hash="deadbeef")
    seen_inside: dict = {}

    async def inner(scope, receive, send):
        seen_inside["principal"] = context.current_principal()
        await send({"type": "http.response.start", "status": 200, "headers": []})
        await send({"type": "http.response.body", "body": b""})

    app = TokenPathASGI(inner, resolver=_FakeResolver({"tok123": principal}))
    await _run(app, _http_scope("/tok123"))

    assert seen_inside["principal"] == principal
    with pytest.raises(AuthError):
        context.current_principal()
