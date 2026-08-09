"""Request-Log (Plan §3, P3 Step 2) — das einzige neue Modul dieser Phase in `mcpserver/`.

Drei Ereignisarten auf einem eigenen, nicht propagierenden Logger (`sharefyx.request`):
`ev="tool"` (`ToolCallLogMiddleware`, FastMCP-Tool-Ebene), `ev="http"` (`AccessLogASGI`,
Starlette-Wurzel-Ebene) und `ev="oauth"` (`OAuthLogASGI`, P4 Step 6b, gleiche Wurzel-Ebene, nur
`/oauth/*`). Alle drei sind eingebaut in `scripts/serve.py`, nicht in `app.py :: create_app()` —
damit `test_app.py` unverändert gegen die nackte App läuft. Alle drei schreiben ausschließlich
über `log_event()`, das die Feld-Whitelist erzwingt.

**Feld-Whitelist** (Plan §3.1, erweitert P4 §4, P6 Step 2): `ts` · `ev` · `tool` · `space` · `ms` ·
`ok` · `err` · `method` · `path` · `status` · `stage` · `client_id` · `grant` · `ua`. Alles andere
wird von `log_event()` stillschweigend verworfen — insbesondere
darf hier **nie** ein Token, ein Item-Titel/Body/Snippet, eine Item-ID oder eine rohe
Fehlermeldung landen (`map_storage_error()`-Texte wie `conflict: itm_… wurde geändert (…)`
enthalten IDs und potenziell Titel). Deshalb geht in `err` nur die **Klasse**
(`classify_error()`), nie `str(exc)`.

**`ua` (P6 Step 2, Client-Surface-Logging, V42):** der `User-Agent`-Header von
`AccessLogASGI`, gekürzt auf 120 Zeichen — das erste **externe, frei wählbare** Feld auf dieser
Log-Zeile, jedes andere ist entweder server-generiert (`ts`, `ms`, `ok`), bereits redigiert
(`path`) oder eine server-ausgestellte opake ID (`client_id`). Zwei Verteidigungen, nicht eine:
die 120-Zeichen-Kürzung hier UND `logging_setup.py :: TokenScrubbingFilter`, das (seit der P3-
Erweiterung dort) auch String-**Werte innerhalb** des Feld-Dicts scrubbt, nicht nur
`record.msg` als Ganzes — läuft vor `JsonLineFormatter.format()`, trifft `ua` also genauso wie
jedes andere Feld. Nie im Tool-Log (`ev="tool"`): `ToolCallLogMiddleware` hat keinen ASGI-Scope-
Zugriff, und `context.py` steht nicht auf P6 Step 2s Berührungsliste — ein Zusammenführen mit
`ev="http"` über den gemeinsamen Zeitstempel reicht für V42 (welche Oberfläche stellte diese
Anfrage), ohne die Tool-Schicht anzufassen.

**Warum `classify_error()` den Nachrichtentext parst statt den Exception-Typ zu prüfen:**
Bis diese Middleware eine Exception sieht, hat `tools.py :: map_storage_error()` sie bereits in
eine `fastmcp.exceptions.ToolError` mit Präfix-Text (`"conflict: …"`, `"item_not_found: …"`, …)
übersetzt — verifiziert gegen den echten Ausführungspfad in `fastmcp==3.4.4`
(`FastMCP.call_tool()`: die Middleware-Kette ruft die Kernlogik über `call_next()` auf, und jede
dort erhobene `FastMCPError`/`ToolError` wird unverändert weitergereicht, nicht erneut
verpackt). Der ursprüngliche `storage`-Exception-Typ (`ConflictError`, `ItemNotFound`, …) ist an
dieser Stelle nicht mehr sichtbar — ein `dict[type[Exception], str]` würde hier immer denselben
einen Typ (`ToolError`) treffen. Die Klassifikation läuft deshalb über den Nachrichten-Präfix vor
dem ersten `":"`, den `map_storage_error()` selbst festlegt.
"""
from __future__ import annotations

import json
import logging
import time
from datetime import datetime, timezone
from typing import Any
from urllib.parse import parse_qs

from fastmcp.server.middleware import CallNext, Middleware, MiddlewareContext

from .auth import AuthError
from .context import current_principal
from .logging_setup import _TOKEN_SEGMENT_RE

LOGGER_NAME = "sharefyx.request"

# Feld-Whitelist — einzige Stelle, die entscheidet, was in eine Logzeile darf (siehe Moduldocstring).
# `stage`/`client_id`/`grant` sind P4 Step 6b (Plan §4) — die Whitelist ERLAUBT alle drei, aber
# `OAuthLogASGI` (unten) füllt nur `stage` und `client_id`; siehe dessen Docstring, warum `err`,
# `grant` und `space` dort nie gesetzt werden (bräuchten einen Body-Read).
_ALLOWED_FIELDS = frozenset(
    {
        "ts", "ev", "tool", "space", "ms", "ok", "err", "method", "path", "status",
        "stage", "client_id", "grant", "ua",
    }
)

# P6 Step 2 (V42): maximale Länge des `ua`-Felds — ein Header ist Client-kontrolliert und damit
# beliebig lang; die Kürzung ist keine Stilfrage, sondern eine Grenze gegen eine überlange
# Logzeile aus unauthentifizierter (bzw. bei `/mcp` erst nach Bearer-Prüfung authentifizierter,
# aber immer noch client-gewählter) Eingabe.
_UA_MAX_LEN = 120

# Bekannte Fehlerklassen, wie von `tools.py :: map_storage_error()` als Nachrichten-Präfix
# festgelegt. Alles Unbekannte (inklusive `auth_error`, `space_not_found`, `internal_error`)
# wird `internal` — die Whitelist ist bewusst eng, nicht vollständig (Plan §3.1).
_KNOWN_ERROR_CLASSES = frozenset({"conflict", "item_not_found", "write_denied", "invalid"})


def classify_error(exc: BaseException) -> str:
    """Nachrichtenpräfix vor dem ersten `":"` — siehe Moduldocstring, warum nicht der Typ."""
    prefix = str(exc).split(":", 1)[0]
    return prefix if prefix in _KNOWN_ERROR_CLASSES else "internal"


def _now_iso() -> str:
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%dT%H:%M:%S.") + f"{now.microsecond // 1000:03d}Z"


class JsonLineFormatter(logging.Formatter):
    """`record.msg` ist bereits ein Feld-Dict (von `log_event()` übergeben) — hier wird nur noch
    kompakt serialisiert, keine `%`-Interpolation, kein `record.getMessage()`."""

    def format(self, record: logging.LogRecord) -> str:
        return json.dumps(record.msg, separators=(",", ":"), ensure_ascii=False)


def log_event(**fields: Any) -> None:
    """Schreibt eine Zeile auf `sharefyx.request`. Erzwingt die Feld-Whitelist (unbekannte
    Schlüssel werden verworfen, nicht durchgereicht) und darf selbst **nie** werfen — ein
    Logging-Fehler darf einen Tool- oder HTTP-Aufruf nicht zum Scheitern bringen."""
    record = {"ts": _now_iso()}
    for key, value in fields.items():
        if key in _ALLOWED_FIELDS:
            record[key] = value
    try:
        logging.getLogger(LOGGER_NAME).info(record)
    except Exception:  # noqa: BLE001 - Logging darf den Aufrufer nie stören
        pass


def _current_space() -> str | None:
    """Der **authentifizierte Aufrufer**, nicht der Zielraum des Tool-Aufrufs — `Principal.space`
    ist immer der eigene Space (siehe `auth.py`). Bei `get_item`/`update_item` gegen einen
    fremden Space steht hier also weiterhin der eigene Space, nicht `beta`. Beantwortet Plan
    §3.4 Frage 2 ("ist es mein Account oder der des Kollegen?") — für Rule-4-Nachweise (wer hat
    wohin geschrieben) ist das Log bewusst nicht die Quelle; das ist Aufgabe der
    Tool-Fehlerklasse (`write_denied`) und der Tests in `test_tools.py`/`test_app.py`.

    Defensiv: `AuthError` darf im regulären Pfad nicht auftreten, aber die Logzeile soll bei
    einem verbleibenden Restrisiko `space: null` zeigen statt abzustürzen."""
    try:
        return current_principal().space
    except AuthError:
        return None


class ToolCallLogMiddleware(Middleware):
    """Misst Dauer und Ergebnis jedes Tool-Aufrufs. Kennt keine Argumente und keine Ergebnisse —
    nur Name (`context.message.name`), Space, Dauer, Erfolg, Fehlerklasse."""

    async def on_call_tool(self, context: MiddlewareContext, call_next: CallNext) -> Any:
        tool_name = getattr(context.message, "name", None)
        start = time.perf_counter()
        error_class: str | None = None
        try:
            return await call_next(context)
        except BaseException as exc:
            error_class = classify_error(exc)
            raise
        finally:
            ms = round((time.perf_counter() - start) * 1000)
            fields: dict[str, Any] = {
                "ev": "tool",
                "tool": tool_name,
                "space": _current_space(),
                "ms": ms,
                "ok": error_class is None,
            }
            if error_class is not None:
                fields["err"] = error_class
            log_event(**fields)


class AccessLogASGI:
    """Umschließt die Wurzel-App (`scripts/serve.py`, nicht `create_app()`). Misst Dauer, fängt
    den Status aus dem `http.response.start`-Event ab, loggt Methode, Pfad (token-redacted) und
    Status. Kein Body. **Seit P6 Step 2 genau ein Header:** `User-Agent`, für `ua` (siehe
    Moduldocstring) — sonst weiterhin keine Header."""

    def __init__(self, app: Any) -> None:
        self._app = app

    async def __call__(self, scope: Any, receive: Any, send: Any) -> None:
        if scope["type"] != "http":
            await self._app(scope, receive, send)
            return

        start = time.perf_counter()
        status_holder: dict[str, int] = {}
        headers = dict(scope.get("headers") or [])
        raw_ua = headers.get(b"user-agent")
        ua = raw_ua.decode("utf-8", errors="replace")[:_UA_MAX_LEN] if raw_ua else None

        async def _send(message: dict[str, Any]) -> None:
            if message["type"] == "http.response.start":
                status_holder["status"] = message["status"]
            await send(message)

        try:
            await self._app(scope, receive, _send)
        finally:
            ms = round((time.perf_counter() - start) * 1000)
            path = _TOKEN_SEGMENT_RE.sub(r"\1<redacted>", scope.get("path", ""))
            fields: dict[str, Any] = {
                "ev": "http",
                "method": scope.get("method"),
                "path": path,
                "status": status_holder.get("status"),
                "ms": ms,
            }
            if ua is not None:
                fields["ua"] = ua
            log_event(**fields)


# (method, path) -> stage (Plan §4). `/oauth/token` bedient sowohl `authorization_code` als auch
# `refresh_token` — die Unterscheidung steht nur im Formular-Body (`grant_type`), den
# `OAuthLogASGI` bewusst nie liest (siehe Klassen-Docstring). `stage="token"` (ohne
# Grant-Unterscheidung) ist deshalb der akzeptierte Kompromiss (P4 Step 6b, Advisor-Vorgabe) —
# dokumentiert statt still auf `token_code`/`token_refresh` „geraten".
_STAGE_BY_ROUTE: dict[tuple[str, str], str] = {
    ("POST", "/oauth/register"): "register",
    ("GET", "/oauth/authorize"): "authorize_get",
    ("POST", "/oauth/authorize"): "authorize_post",
    ("POST", "/oauth/token"): "token",
}


class OAuthLogASGI:
    """Umschließt die Wurzel-App wie `AccessLogASGI` (`scripts/serve.py`, nicht `create_app()`
    — Plan §3.3s Begründung gilt gleich: `test_app.py` läuft damit unverändert gegen die nackte
    App). Loggt **nur** `/oauth/*`-Anfragen (`ev="oauth"`) — Discovery (`/.well-known/*`),
    `/health` und `/mcp` bekommen weiterhin ausschließlich `AccessLogASGI`s `ev="http"`-Zeile,
    keine doppelte Protokollierung derselben Anfrage.

    **Kein Body-, kein Header-Read.** `stage` kommt ausschließlich aus Methode+Pfad
    (`_STAGE_BY_ROUTE`), `client_id` ausschließlich aus dem Query-String von `GET
    /oauth/authorize` (dort ein Klartext-Parameter, keine Kopie eines Geheimnisses). Damit
    fallen `err`, `grant` und `space` aus Plan §4s Beispielzeilen bewusst weg — jedes der drei
    bräuchte einen Formular- oder JSON-Body-Read (`space`/`password`/`totp` auf
    `authorize_post`, `grant_type` auf `token`), und ein Body-Read hier wäre genau die Umkehrung
    der Regel, die `stage`s Body-Freiheit erst sicher macht (Advisor-Vorgabe, P4 Step 6b). Die
    Whitelist in `_ALLOWED_FIELDS` erlaubt alle drei Felder trotzdem (Plan §4 wörtlich), nur
    füllt sie hier niemand.

    **`ok` ist HTTP-Status-Ebene, nicht Fluss-Ebene:** ein abgelehntes Consent (`action=deny`)
    liefert einen 302-Redirect mit `error=access_denied` — das ist aus Sicht dieser Klasse ein
    **Erfolg** (`ok=True`), weil die Anfrage selbst korrekt beantwortet wurde. Wer wissen will,
    ob der *Fluss* erfolgreich war, braucht die Redirect-Query, nicht dieses Log."""

    def __init__(self, app: Any) -> None:
        self._app = app

    async def __call__(self, scope: Any, receive: Any, send: Any) -> None:
        path = scope.get("path", "") if scope.get("type") == "http" else ""
        if scope.get("type") != "http" or not path.startswith("/oauth/"):
            await self._app(scope, receive, send)
            return

        stage = _STAGE_BY_ROUTE.get((scope.get("method"), path))
        client_id: str | None = None
        if stage == "authorize_get":
            query = parse_qs(scope.get("query_string", b"").decode("utf-8"))
            values = query.get("client_id")
            client_id = values[0] if values else None

        start = time.perf_counter()
        status_holder: dict[str, int] = {}

        async def _send(message: dict[str, Any]) -> None:
            if message["type"] == "http.response.start":
                status_holder["status"] = message["status"]
            await send(message)

        try:
            await self._app(scope, receive, _send)
        finally:
            ms = round((time.perf_counter() - start) * 1000)
            status = status_holder.get("status")
            fields: dict[str, Any] = {
                "ev": "oauth", "ms": ms, "ok": bool(status) and status < 400,
            }
            # `stage` bleibt weg statt `null` zu loggen, wenn Methode+Pfad nicht auf eine der
            # vier bekannten Routen passen (z. B. GET /oauth/token) — hält den Feldwert innerhalb
            # von Plan §4s Enum, keinen fünften Wert einführen.
            if stage is not None:
                fields["stage"] = stage
            if client_id is not None:
                fields["client_id"] = client_id
            log_event(**fields)
