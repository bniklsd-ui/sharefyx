"""`/api/v1/{me,spaces,items,items/{id},items/{id}/append,items/{id}/archive}` (Plan §3.1–§3.3,
§5 Step 5). JSON durchgehend, dieselbe Struktur wie `webui/account.py`: Sitzung laden → CSRF
(nur bei state-ändernden Routen) → Body parsen → Store aufrufen → `ApiError` (falls einer der
Schritte scheitert) über `_catch()` in eine JSON-Fehlerantwort übersetzt.

**Reihenfolge bei jedem Item-Endpunkt, wörtlich aus dem Plan, nicht verhandelbar:** erst
`store.space_of(item_id)` (index-only, schreibt nichts, liest keine Datei — sicher aufzurufen
BEVOR feststeht, ob der Zugriff erlaubt ist), dann die Rechteprüfung, erst danach ein
Store-Aufruf, der tatsächlich liest/schreibt. Ein Rechtefehler darf `store.get()`/`update()`/
`append()`/`archive()` nie erreichen — dieselbe Reihenfolge, die `mcpserver/tools.py` für die
sechs MCP-Tools durchsetzt (P2 Rule 4), hier für die REST-Seite wiederholt, nicht neu erfunden.

**Ausnahme `archive`:** `storage.store.Store.archive()` hat anders als `update()`/`append()`
keinen Schutz gegen ein bereits archiviertes Item (kein Bug — `storage/` ist für diese Phase
tabu, P5-B; ein Fix dort wäre eine Scope-Änderung). Diese Datei holt deshalb NACH der
Rechteprüfung (also sicher, kein fremder Dateizugriff) den aktuellen Stand einmal per
`store.get()` und lehnt ein zweites Archivieren mit `422 validation_failed` ab — sonst würde ein
wiederholter Klick auf „Archivieren" bei jedem Aufruf stillschweigend die Version hochzählen,
ohne dass sich am Zustand semantisch etwas ändert.

**`webui` darf genau EIN Symbol aus `mcpserver` importieren** (P5-B): `OwnSpaceWritable`. Kein
zweiter Import aus `mcpserver` — auch nicht das `Permissions`-Protokoll selbst, das läge im
selben Modul und wäre ein zweites Symbol. Der Parameter unten ist deshalb konkret auf
`OwnSpaceWritable` typisiert, nicht auf ein Protokoll.
"""
from __future__ import annotations

import json
from datetime import date
from typing import Any

from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route

from mcpserver.permissions import OwnSpaceWritable
from storage.errors import ConflictError, ItemNotFound, ValidationError
from storage.models import SearchResult, SpaceInfo
from storage.store import Store

from .config import UiSettings
from .errors import ApiError, CsrfError
from .security import require_csrf
from .serializers import item_to_json, search_to_json, space_to_json
from .sessions import SessionManager

DEFAULT_LIMIT = 50
MAX_LIMIT = 200
MAX_BODY_BYTES = 1 * 1024 * 1024  # Plan §3.1

# [SEAM] Wie `mcpserver/tools.py :: _STORE_FETCH_LIMIT` (dieselbe Kostenabwägung, hier erneut
# definiert statt importiert — ein Import aus `mcpserver.tools` wäre ein zweites `mcpserver`-
# Symbol und P5-B verbietet das): `Store.search()` kennt nur einen einzelnen `space`-Filter,
# keine Menge „sichtbarer Spaces". Die Sichtbarkeitsprüfung (`permissions.visible_spaces`) muss
# deshalb NACH dem Store-Aufruf laufen, und danach paginiert diese Datei selbst — sonst würde
# `total`/`offset` verfälscht, sobald ein unsichtbarer Space existierte. Diese Konstante deckt
# den heutigen Datenumfang (Zwei-Personen-Space-Server) um Größenordnungen ab.
_STORE_FETCH_LIMIT = 5000


def _map_store_error(exc: Exception) -> ApiError:
    if isinstance(exc, ItemNotFound):
        return ApiError("not_found", f"Item nicht gefunden: {exc.item_id}")
    if isinstance(exc, ConflictError):
        current = exc.current
        return ApiError(
            "conflict",
            f"Konflikt bei {exc.item_id}: erwartete Version {exc.expected_version}, "
            f"aktuell {current.version}.",
            detail={"current": item_to_json(current, readonly=False)},
        )
    if isinstance(exc, (ValidationError, ValueError)):
        # `storage.store._coerce_due()` wirft bei einem falsch formatierten `due`-String ein
        # rohes `ValueError` (`date.fromisoformat`), keine `ValidationError` — Fund dieser
        # Session, nicht in `storage/` behebbar (P5-B: `storage/` ist tabu). Beide landen hier
        # auf demselben `422 validation_failed`, aus Sicht eines API-Clients ist es derselbe
        # Fehlerfall.
        return ApiError("validation_failed", str(exc))
    raise exc  # pragma: no cover - Programmfehler, kein erwarteter Store-Fehlerpfad


def _parse_due(value: Any) -> date | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ApiError("validation_failed", "'due' muss ein ISO-Datum (YYYY-MM-DD) sein.")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ApiError("validation_failed", "'due' muss ein ISO-Datum (YYYY-MM-DD) sein.") from exc


def _parse_int(value: str | None, *, default: int) -> int:
    if value is None:
        return default
    try:
        return int(value)
    except ValueError as exc:
        raise ApiError("validation_failed", f"'{value}' ist keine gültige Ganzzahl.") from exc


def api_routes(
    settings: UiSettings, store: Store, sessions: SessionManager, permissions: OwnSpaceWritable,
) -> list[Route]:
    async def _require_session(request: Request):
        session = sessions.load(request)
        if session is None:
            raise ApiError("unauthenticated", "Keine gültige Sitzung.")
        return session

    async def _require_csrf_json(request: Request, session) -> None:
        try:
            require_csrf(request, session, settings=settings, form_token=None)
        except CsrfError as exc:
            raise ApiError("csrf_failed", exc.message) from exc

    async def _json_body(request: Request) -> dict[str, Any]:
        # Bewusst einfach (Plan §3.1: 1 MiB reicht für einen Zwei-Personen-Space-Server) — der
        # ganze Body landet ohnehin im Speicher, ein Streaming-Cutoff wäre hier Overengineering.
        raw = await request.body()
        if len(raw) > MAX_BODY_BYTES:
            raise ApiError("payload_too_large", "Anfrage überschreitet 1 MiB.")
        try:
            body = json.loads(raw) if raw else {}
        except ValueError as exc:
            raise ApiError("validation_failed", "Ungültiges JSON.") from exc
        if not isinstance(body, dict):
            raise ApiError("validation_failed", "Body muss ein JSON-Objekt sein.")
        return body

    def _visible_spaces(actor: str, names: list[str]) -> set[str]:
        return set(permissions.visible_spaces(actor, names))

    async def _me(request: Request) -> Response:
        session = await _require_session(request)
        return JSONResponse({"space": session.space}, headers={"Cache-Control": "no-store"})

    async def _spaces(request: Request) -> Response:
        session = await _require_session(request)
        spaces = store.list_spaces()
        # Gleicher Fund wie `tools.py :: list_spaces()` (B1, P2-Adapter-Abnahme): ein Space ohne
        # ein einziges Item taucht in `list_spaces()` sonst gar nicht auf.
        if session.space not in {s.name for s in spaces}:
            spaces = sorted(
                [*spaces, SpaceInfo(name=session.space, item_count=0)], key=lambda s: s.name
            )
        # Sichtbarkeit aus DIESER (ggf. um den leeren eigenen Space ergänzten) Liste berechnen,
        # nicht aus einem frischen `store.list_spaces()` — sonst würde ein eigener Space ohne
        # Items nie als sichtbar erkannt (derselbe Fund wie B1, nur eine Zeile weiter unten).
        visible = _visible_spaces(session.space, [s.name for s in spaces])
        payload = [space_to_json(s, own_space=session.space) for s in spaces if s.name in visible]
        return JSONResponse(payload, headers={"Cache-Control": "no-store"})

    async def _items_get(request: Request) -> Response:
        session = await _require_session(request)
        q = request.query_params
        limit = max(1, min(_parse_int(q.get("limit"), default=DEFAULT_LIMIT), MAX_LIMIT))
        offset = max(0, _parse_int(q.get("offset"), default=0))
        due_before = _parse_due(q.get("due_before"))

        try:
            result = store.search(
                q.get("query"),
                space=q.get("space"),
                type=q.get("type"),
                status=q.get("status"),
                tag=q.get("tag"),
                due_before=due_before,
                limit=_STORE_FETCH_LIMIT,
                offset=0,
            )
        except (ValidationError, ValueError) as exc:
            raise _map_store_error(exc) from exc

        visible = _visible_spaces(session.space, [s.name for s in store.list_spaces()])
        items = [i for i in result.items if i.space in visible]
        total = len(items)
        page = items[offset : offset + limit]
        payload = search_to_json(
            SearchResult(items=page, total=total, limit=limit, offset=offset),
            own_space=session.space,
        )
        return JSONResponse(payload, headers={"Cache-Control": "no-store"})

    async def _items_post(request: Request) -> Response:
        session = await _require_session(request)
        await _require_csrf_json(request, session)
        body = await _json_body(request)

        item_type = body.get("type")
        title = body.get("title")
        if not isinstance(item_type, str) or not isinstance(title, str):
            raise ApiError("validation_failed", "'type' und 'title' sind Pflichtfelder.")
        item_body = body.get("body", "")
        if not isinstance(item_body, str):
            raise ApiError("validation_failed", "'body' muss ein String sein.")

        # Kein `space`-Feld gelesen — Rule 4 architektonisch (P5-A): der Ziel-Space ist immer die
        # Sitzung, ein evtl. mitgeschicktes `space` im Body wird stillschweigend ignoriert,
        # niemals ausgewertet.
        kwargs: dict[str, Any] = {
            key: value
            for key, value in body.items()
            if key in {"status", "due", "tags", "links", "format"}
        }
        try:
            item = store.create(session.space, type=item_type, title=title, body=item_body, **kwargs)
        except (ValidationError, ValueError) as exc:
            raise _map_store_error(exc) from exc
        return JSONResponse(
            item_to_json(item, readonly=False), status_code=201, headers={"Cache-Control": "no-store"}
        )

    async def _items_get_one(request: Request) -> Response:
        session = await _require_session(request)
        item_id = request.path_params["item_id"]
        try:
            target_space = store.space_of(item_id)
        except ItemNotFound as exc:
            raise _map_store_error(exc) from exc
        if not permissions.can_read(session.space, target_space):
            raise ApiError("forbidden", "Kein Lesezugriff auf diesen Space.")
        own = permissions.can_write(session.space, target_space)
        item = store.get(item_id, repair_drift=own)  # fremd ⇒ kein Dateischreibzugriff (Rule 4)
        return JSONResponse(item_to_json(item, readonly=not own), headers={"Cache-Control": "no-store"})

    async def _items_patch(request: Request) -> Response:
        session = await _require_session(request)
        await _require_csrf_json(request, session)
        body = await _json_body(request)
        item_id = request.path_params["item_id"]

        version = body.get("version")
        if not isinstance(version, int):
            raise ApiError("validation_failed", "'version' ist Pflichtfeld (int).")

        try:
            target_space = store.space_of(item_id)
        except ItemNotFound as exc:
            raise _map_store_error(exc) from exc
        if not permissions.can_write(session.space, target_space):
            raise ApiError("forbidden", "Kein Schreibzugriff auf diesen Space.")

        changes = {key: value for key, value in body.items() if key != "version"}
        try:
            item = store.update(item_id, version=version, **changes)
        except (ItemNotFound, ConflictError, ValidationError, ValueError) as exc:
            raise _map_store_error(exc) from exc
        return JSONResponse(item_to_json(item, readonly=False), headers={"Cache-Control": "no-store"})

    async def _items_append(request: Request) -> Response:
        session = await _require_session(request)
        await _require_csrf_json(request, session)
        body = await _json_body(request)
        item_id = request.path_params["item_id"]

        version = body.get("version")
        text = body.get("text")
        if not isinstance(version, int) or not isinstance(text, str):
            raise ApiError("validation_failed", "'version' (int) und 'text' (str) sind Pflichtfelder.")

        try:
            target_space = store.space_of(item_id)
        except ItemNotFound as exc:
            raise _map_store_error(exc) from exc
        if not permissions.can_write(session.space, target_space):
            raise ApiError("forbidden", "Kein Schreibzugriff auf diesen Space.")

        try:
            item = store.append(item_id, version=version, text=text)
        except (ItemNotFound, ConflictError, ValidationError, ValueError) as exc:
            raise _map_store_error(exc) from exc
        return JSONResponse(item_to_json(item, readonly=False), headers={"Cache-Control": "no-store"})

    async def _items_archive(request: Request) -> Response:
        session = await _require_session(request)
        await _require_csrf_json(request, session)
        body = await _json_body(request)
        item_id = request.path_params["item_id"]

        version = body.get("version")
        if not isinstance(version, int):
            raise ApiError("validation_failed", "'version' ist Pflichtfeld (int).")

        try:
            target_space = store.space_of(item_id)
        except ItemNotFound as exc:
            raise _map_store_error(exc) from exc
        if not permissions.can_write(session.space, target_space):
            raise ApiError("forbidden", "Kein Schreibzugriff auf diesen Space.")

        # Siehe Moduldocstring: `store.archive()` hat keinen eigenen Schutz gegen ein bereits
        # archiviertes Item — dieser Check läuft NACH der Rechteprüfung, also sicher (eigener
        # Space, kein Rule-4-Risiko).
        try:
            current = store.get(item_id, repair_drift=True)
        except ItemNotFound as exc:
            raise _map_store_error(exc) from exc
        if current.status == "archived":
            raise ApiError("validation_failed", "Item ist bereits archiviert.")

        try:
            item = store.archive(item_id, version=version)
        except (ItemNotFound, ConflictError) as exc:
            raise _map_store_error(exc) from exc
        return JSONResponse(item_to_json(item, readonly=False), headers={"Cache-Control": "no-store"})

    def _catch(handler):
        """Dasselbe Muster wie `webui/account.py :: _catch()` — vor dem `Route(...)`-Konstruktor
        angewendet, nicht danach (siehe dortiger Docstring für die Begründung)."""
        async def _inner(request: Request) -> Response:
            try:
                return await handler(request)
            except ApiError as exc:
                return JSONResponse(
                    exc.to_json(), status_code=exc.status_code, headers={"Cache-Control": "no-store"}
                )
        return _inner

    return [
        Route("/api/v1/me", _catch(_me), methods=["GET"]),
        Route("/api/v1/spaces", _catch(_spaces), methods=["GET"]),
        Route("/api/v1/items", _catch(_items_get), methods=["GET"]),
        Route("/api/v1/items", _catch(_items_post), methods=["POST"]),
        Route("/api/v1/items/{item_id}", _catch(_items_get_one), methods=["GET"]),
        Route("/api/v1/items/{item_id}", _catch(_items_patch), methods=["PATCH"]),
        Route("/api/v1/items/{item_id}/append", _catch(_items_append), methods=["POST"]),
        Route("/api/v1/items/{item_id}/archive", _catch(_items_archive), methods=["POST"]),
    ]
