"""`ContextVar` für den aktuellen Principal + Guard gegen einen stale Request-Kontext
(Plan §2.4, §8 Risiko 1).

**Abweichung vom Plan-Wortlaut, empirisch begründet (P2 Step 4):** §2.4 beschreibt den Guard
als "zieht das Token-Segment aus dessen Pfad" — das ist nicht umsetzbar, weil `TokenPathASGI`
das Token-Segment aus dem Pfad entfernen MUSS, bevor es an die innere FastMCP-App delegiert
(sonst würde FastMCPs eigenes Routing das Segment als Teil des MCP-Pfads sehen). Ein Tool, das
während seiner Ausführung `get_http_request().url.path` aufruft, sieht deshalb nur noch den
bereits bereinigten Pfad — empirisch verifiziert gegen echtes `fastmcp==3.4.4` +
`starlette` (Testprobe: `get_http_request().url.path` lieferte `"/mcp/"`, nicht den Token).

Stattdessen: die ASGI-Auth-Schicht hinterlegt `token_hash` in `scope["state"]`, bevor sie an die
innere App delegiert. `scope["state"]` überlebt die Weiterleitung an die innere App unverändert
(dieselbe Testprobe bestätigte `request.state.token_hash` korrekt gesetzt) — Starlettes
offizieller Mechanismus für genau diesen Zweck (Zustand über die ASGI-Kette hinweg mitgeben).
Die Sicherheitseigenschaft ist identisch: der Guard vergleicht "was hat unsere eigene ASGI-
Schicht für DIESEN Request aufgelöst" gegen "was liefert `get_http_request()` gerade zurück" und
schlägt bei jeder Abweichung laut fehl.

**Schnitt, 2026-07-30:** `TokenPathASGI` (P2) ist entfernt, `BearerAuthASGI` (P4) ist seither die
einzige ASGI-Auth-Schicht — sie hinterlegt denselben Slot, dieser Guard brauchte auch dafür keine
Änderung (siehe `asgi.py`-Moduldocstring).
"""
from __future__ import annotations

from contextvars import ContextVar, Token

from .auth import AuthError, Principal

_principal_var: ContextVar[Principal] = ContextVar("principal")


def set_principal(principal: Principal) -> Token:
    """Von `BearerAuthASGI` benutzt (bis 2026-07-30 auch von `TokenPathASGI`, seither entfernt
    — siehe `asgi.py`-Moduldocstring). Gibt das Token für den späteren `reset_principal()`
    zurück."""
    return _principal_var.set(principal)


def reset_principal(token: Token) -> None:
    _principal_var.reset(token)


def current_principal() -> Principal:
    """Wirft `AuthError`, wenn kein Principal im aktuellen Kontext gesetzt ist — es gibt keinen
    Aufrufpfad, der ohne Principal auskommen darf (fail-closed)."""
    try:
        return _principal_var.get()
    except LookupError as exc:
        raise AuthError("kein Principal im aktuellen Request-Kontext gesetzt") from exc


def assert_principal_matches_request() -> None:
    """Guard: vergleicht `current_principal().token_hash` gegen den `token_hash`, den
    `TokenPathASGI` für das aktuelle ASGI-Scope hinterlegt hat. `stateless_http=True` (P2-B)
    verhindert die Ursache eines stale Request-Kontexts; dieser Guard macht ein verbleibendes
    Restrisiko zu einem lauten Fehler statt einer falschen Antwort (§8 Risiko 1).
    """
    from fastmcp.server.dependencies import get_http_request

    principal = current_principal()
    request = get_http_request()
    request_hash = getattr(request.state, "token_hash", None)
    if request_hash != principal.token_hash:
        raise AuthError("Request-Kontext passt nicht zum aufgelösten Principal")
