"""`/api/v1/{me,spaces,meta,items,items/{id},items/{id}/append,items/{id}/archive}` (Plan
§3.1–§3.3, §5 Step 5/7). JSON durchgehend, dieselbe Struktur wie `webui/account.py`: Sitzung
laden → CSRF (nur bei state-ändernden Routen) → Body parsen → Store aufrufen → `ApiError` (falls
einer der Schritte scheitert) über `_catch()` in eine JSON-Fehlerantwort übersetzt.

**`GET /api/v1/meta` (Step 7, in keiner Plan-Tabelle spezifiziert):** Step 7s eigener Testname
(`test_status_values_endpoint_matches_storage_models`) verlangt einen Endpunkt, den §1.5s
Routentabelle nicht listet — dieselbe Kategorie kleiner, autonom geschlossener Lücke wie Step 6s
`/ui/`-Sitzungsprüfung. Liefert `{"status_values": {...}}` direkt aus `storage.models.
STATUS_VALUES`, damit `app.js` das Statusvokabular pro Typ nicht dupliziert (P5-U/§7: „`type`
ist nach dem Anlegen nicht änderbar in der UI"). **Step 7b** ergänzt `{"buckets": {...}}` — siehe
`_BUCKETS` unten.

**`GET /api/v1/overview` (Step 7b, ebenfalls in keiner Plan-Tabelle):** speist die neue
Übersichtsseite und die Zähler-Plaketten im Navigationsbaum (Nikinger-Entscheidung 2026-08-05,
revidiert §4.3). Liefert je sichtbarem Space die drei Bucket-Zähler und die fünf zuletzt
geänderten Items. Die Arbeit liegt bewusst hier statt in `app.js`: der Plan lässt JavaScript
ungetestet, Python nicht — was hier steht, ist mit `pytest` prüfbar. Kein LLM, keine Deutung,
nur Zählen und Sortieren (Kernprinzip „der Server ist dumm" bleibt gewahrt).

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

**`webui` darf genau EIN Symbol aus `mcpserver` importieren** (P5-B): `SharePolicy` seit P6
Step 5 (vorher `OwnSpaceWritable` — `mcpserver.permissions.SharePolicy` ist jetzt der einzige
erlaubte Name, `test_webui_imports_exactly_one_mcpserver_symbol` prüft ihn über den echten
Quelltext, nicht über eine Behauptung). **`Surface` wird bewusst NICHT importiert** — ein
zweiter Name aus demselben Modul wäre trotzdem ein zweites Symbol, der Test zählt tatsächlich
importierte Namen, kein Sonderfall für "gleiches Modul". `SharePolicy.can_read_item_as_human()`
(neu, P6 Step 5) kapselt `surface=Surface.HUMAN` innerhalb von `mcpserver/permissions.py` — eine
`SharePolicy`-eigene Bequemlichkeitsmethode, nicht Teil des `Permissions`-Protokolls (das
`tools.py` mit dem expliziten `surface=`-Parameter benutzt, weil es innerhalb desselben Pakets
liegt und keiner Importbeschränkung unterliegt). `AuthStore` (`authserver.store`) ist von P5-B
unberührt — dieselbe Bibliothek, die `account.py`/`sessions.py` bereits importieren, P5-B
beschränkt nur `mcpserver`.

**`GET /api/v1/updates`/`POST /api/v1/updates/seen` (P6 Step 3, Plan §1.8):** speist Banner +
Einstellungsabschnitt „Update-Log". `api_routes()` bekommt dafür einen fünften Parameter,
`auth_store: AuthStore` — der gesehen-Zustand (`users.seen_update_id`, Schema 3) lebt in der
Auth-SQLite, nicht im `storage`-Kern; dieselbe `AuthStore`-Instanz, die `account_routes()` schon
bekommt (`oauth.store` in `mcpserver/app.py`), kein zweiter DB-Handle. **Dokumentierte
Abweichung vom Plan-Dateiwortlaut** (der für Step 3 nur `webui/api.py` nennt, nicht
`mcpserver/app.py`): der Aufrufer muss den neuen Parameter mitgeben, `mcpserver/app.py`s
`api_routes(...)`-Aufruf zieht deshalb im selben Commit nach (`oauth.store` als fünftes
Argument) — dieselbe Kategorie wie P6 Step 1/2s dokumentierte Ein-Zeilen-Abweichungen. `POST
.../seen` schreibt den vom Server aus dem Log berechneten `latest_id`, nie eine vom Client
mitgeschickte ID — eine Client-ID wäre eine unnötige Validierungsfläche und ein Stale-Client-
Rennen ohne Nutzen.

**Re-Auth-Gate auf `PATCH /api/v1/items/{id}` (Step 7 Commit 5a, `shares.py`):** `api_routes()`
bekommt einen sechsten Parameter, `users: UserDirectory` — `shares.py :: require_share_reauth()`
braucht ihn für dieselbe `reauth.verify_reauth()`-Prüfung, die `account.py`s Passwortwechsel
schon nutzt. `LoginThrottle` wird lokal aus `auth_store` gebaut (keine geteilte Instanz nötig,
zustandslos gegenüber der DB-Tabelle). **Dokumentierte Abweichung vom Ausführungsplan**
(`serialized-seeking-aurora.md`, Commit 5): die dort vorgeschlagene UI-Hälfte (Freigabe-Dialog,
Re-Auth-Mini-Formular in `dialogs.js`/`app.html`) ist auf einen eigenen Commit 5b verschoben —
Backend-Gate und Frontend-Dialog haben unterschiedliche Verifikationswege (`pytest` deterministisch
hier, nur Screenshot dort) und würden als ein Commit den bisherigen Atomar-Rhythmus dieses Steps
brechen. `mcpserver/app.py`s `api_routes(...)`-Aufruf zieht im selben Commit nach (`oauth.users`
als sechstes Argument).
"""
from __future__ import annotations

import json
from datetime import date
from typing import Any

from authserver.ratelimit import LoginThrottle
from authserver.store import AuthStore
from authserver.userdir import UserDirectory
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route

from mcpserver.permissions import SharePolicy
from storage.errors import ConflictError, ItemNotFound, ValidationError
from storage.files import ITEM_ID_RE, validate_folder
from storage.models import STATUS_VALUES, SpaceInfo
from storage.store import Store

from .config import UiSettings
from .errors import ApiError, CsrfError
from .security import require_csrf
from .serializers import (
    asset_to_json, item_to_json, overview_row_to_json, search_to_json, space_to_json,
    summary_to_json,
)
from .sessions import SessionManager
from .shares import ShareState, require_share_reauth
from .updates import load_update_log

DEFAULT_LIMIT = 50
MAX_LIMIT = 200
MAX_BODY_BYTES = 1 * 1024 * 1024  # Plan §3.1
# Eigene Konstante statt MAX_BODY_BYTES (P6.5-L): ein Bild-Upload ist rohe Bildbytes, kein
# JSON — 1 MiB wäre für ein reales Foto/Screenshot zu eng, während MAX_BODY_BYTES bewusst eng
# gehalten ist, weil ein JSON-Body sonst ohnehin nie so groß werden sollte (Plan §3.1). Zwei
# unterschiedliche Grenzen für zwei unterschiedliche Datenarten, keine gemeinsame Zahl.
MAX_ASSET_BYTES = 5 * 1024 * 1024

# Die drei Ordner des Navigationsbaums, einmal definiert (Step 7b). Vorher standen dieselben drei
# Filterkombinationen ausschließlich in `app.js :: filterParams()` — die Übersichtszähler hätten
# sie ein zweites Mal gebraucht, und zwei Kopien einer Filterdefinition driften. `GET
# /api/v1/meta` gibt sie deshalb an `app.js` heraus, `_overview()` zählt mit denselben Werten.
# „archived" ist bewusst typunabhängig: eine archivierte Aufgabe gehört ins Archiv, nicht unter
# „Offen". Die Reihenfolge ist bedeutsam — `app.js :: bucketFor()` nimmt den ERSTEN passenden
# Eintrag, und eine archivierte Aufgabe passt sowohl auf „archived" als auch (bis auf den Status)
# auf „open"; „archived" steht deshalb zuletzt.
#
# „done" ist ein Fund dieses Steps, nicht aus dem Plan: die drei Ordner des Mockups (Offen,
# Notizen, Archiv) decken `STATUS_VALUES["task"]` nicht vollständig ab — eine auf `done` gesetzte
# Aufgabe fiel durch alle drei und war in der Oberfläche nirgends mehr auffindbar, bis sie jemand
# archivierte. Vier Ordner statt drei schließen das Loch.
_BUCKETS: dict[str, dict[str, str]] = {
    "open": {"type": "task", "status": "open"},
    "done": {"type": "task", "status": "done"},
    "note": {"type": "note", "status": "active"},
    "archived": {"status": "archived"},
}

# Zeilen unter „Zuletzt benutzt" je Space. Bewusst klein: die Übersicht soll orientieren, nicht
# die Liste ersetzen.
_RECENT_LIMIT = 5

# [SEAM] Wie `mcpserver/tools.py :: _STORE_FETCH_LIMIT` (dieselbe Kostenabwägung, hier erneut
# definiert statt importiert — ein Import aus `mcpserver.tools` wäre ein zweites `mcpserver`-
# Symbol und P5-B verbietet das): `Store.search()` kennt nur einen einzelnen `space`-Filter,
# keine Menge „sichtbarer Spaces". Die Sichtbarkeitsprüfung (`permissions.visible_spaces`) muss
# deshalb NACH dem Store-Aufruf laufen, und danach paginiert diese Datei selbst — sonst würde
# `total`/`offset` verfälscht, sobald ein unsichtbarer Space existierte. Diese Konstante deckt
# den heutigen Datenumfang (Zwei-Personen-Space-Server) um Größenordnungen ab.
_STORE_FETCH_LIMIT = 5000


def _map_store_error(exc: Exception, *, own_space: str) -> ApiError:
    if isinstance(exc, ItemNotFound):
        return ApiError("not_found", f"Item nicht gefunden: {exc.item_id}")
    if isinstance(exc, ConflictError):
        current = exc.current
        return ApiError(
            "conflict",
            f"Konflikt bei {exc.item_id}: erwartete Version {exc.expected_version}, "
            f"aktuell {current.version}.",
            detail={"current": item_to_json(current, readonly=False, own_space=own_space)},
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
    settings: UiSettings,
    store: Store,
    sessions: SessionManager,
    permissions: SharePolicy,
    auth_store: AuthStore,
    users: UserDirectory,
) -> list[Route]:
    # Re-Auth-Gate (Step 7 Commit 5a, `shares.py :: require_share_reauth()`) braucht dieselben
    # drei Bausteine wie `account.py :: _require_reauth()` — `throttle` wird hier genauso lokal
    # gebaut wie dort (`account_routes()`), kein geteilter Zustand nötig, `LoginThrottle` ist
    # zustandslos gegenüber der `auth_store`-Tabelle, die die eigentliche Bremse trägt.
    throttle = LoginThrottle(auth_store, now_fn=auth_store.now)

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

    async def _raw_body(request: Request) -> bytes:
        """Gegenstück zu `_json_body()` für den Bild-Upload — rohe Bytes, kein JSON-Parsing,
        eigene (großzügigere) Grenze `MAX_ASSET_BYTES`. Der `Content-Type` des Clients wird
        nirgends gelesen (P6-AZ) — was ein Bild ist, entscheidet ausschließlich
        `sniff_image_mime()` auf den tatsächlichen Bytes."""
        raw = await request.body()
        if len(raw) > MAX_ASSET_BYTES:
            raise ApiError("payload_too_large", "Bild überschreitet 5 MiB.")
        return raw

    def _visible_spaces(actor: str, names: list[str]) -> set[str]:
        return set(permissions.visible_spaces(actor, names))

    def _acl_for_summary(item):
        """Baut die `AclDecision` einer bereits geladenen `ItemSummary`-Zeile (P6 Step 5) —
        über `store.acl_reader.decision_for()`, kein zweiter Index-Roundtrip pro Treffer.
        Dasselbe Muster wie `mcpserver.tools._acl_of_summary`, hier separat gehalten statt
        importiert (P5-B: kein zweiter `mcpserver`-Import über `SharePolicy` hinaus)."""
        return store.acl_reader.decision_for(
            space=item.space, folder=item.folder, visibility=item.visibility,
            share_read=item.share_read, share_write=item.share_write,
        )

    async def _me(request: Request) -> Response:
        session = await _require_session(request)
        return JSONResponse({"space": session.space}, headers={"Cache-Control": "no-store"})

    async def _meta(request: Request) -> Response:
        await _require_session(request)
        status_values = {kind: sorted(values) for kind, values in STATUS_VALUES.items()}
        return JSONResponse(
            {"status_values": status_values, "buckets": _BUCKETS},
            headers={"Cache-Control": "no-store"},
        )

    def _visible_space_infos(own_space: str) -> list[SpaceInfo]:
        """Sichtbare Spaces inklusive des B1-Sonderfalls — geteilt von `_spaces()` und
        `_overview()` (Step 7b; vorher stand das nur in `_spaces()`)."""
        spaces = store.list_spaces()
        # Gleicher Fund wie `tools.py :: list_spaces()` (B1, P2-Adapter-Abnahme): ein Space ohne
        # ein einziges Item taucht in `list_spaces()` sonst gar nicht auf.
        if own_space not in {s.name for s in spaces}:
            spaces = sorted(
                [*spaces, SpaceInfo(name=own_space, item_count=0)], key=lambda s: s.name
            )
        # Sichtbarkeit aus DIESER (ggf. um den leeren eigenen Space ergänzten) Liste berechnen,
        # nicht aus einem frischen `store.list_spaces()` — sonst würde ein eigener Space ohne
        # Items nie als sichtbar erkannt (derselbe Fund wie B1, nur eine Zeile weiter unten).
        visible = _visible_spaces(own_space, [s.name for s in spaces])
        return [s for s in spaces if s.name in visible]

    async def _spaces(request: Request) -> Response:
        session = await _require_session(request)
        payload = [
            space_to_json(
                s, own_space=session.space,
                writable=permissions.can_write(session.space, s.name),
            )
            for s in _visible_space_infos(session.space)
        ]
        return JSONResponse(payload, headers={"Cache-Control": "no-store"})

    async def _spaces_create_folder(request: Request) -> Response:
        # Eigentümer-Space-Beschränkung wie `_items_patch`s `folder`-Riegel oben — ein geteilter
        # Schreibzugriff auf EIN Item erlaubt keinen leeren, per Konstruktion einladenden neuen
        # Ordner in einem fremden Space.
        session = await _require_session(request)
        await _require_csrf_json(request, session)
        space = request.path_params["space"]
        if space != session.space:
            raise ApiError("forbidden", "Ordner können nur im eigenen Space angelegt werden.")
        body = await _json_body(request)
        folder = body.get("folder")
        if not isinstance(folder, str) or not folder:
            raise ApiError("validation_failed", "'folder' ist Pflichtfeld (nicht-leerer str).")
        try:
            created = store.ensure_folder(space, folder)
        except (ValidationError, ValueError) as exc:
            raise _map_store_error(exc, own_space=session.space) from exc
        return JSONResponse(
            {"folder": created}, status_code=201, headers={"Cache-Control": "no-store"},
        )

    async def _overview(request: Request) -> Response:
        session = await _require_session(request)
        payload = []
        for space in _visible_space_infos(session.space):
            # Je Bucket ein eigener `store.search()`-Aufruf statt einer selbst geschriebenen
            # Zählschleife: die Zähler sind dadurch per Konstruktion identisch mit dem, was die
            # Liste beim Klick auf denselben Ordner zeigt. Das kostet einen Indexdurchlauf je
            # Bucket — bei einem Zwei-Personen-Space-Server irrelevant, und eine nachgebaute
            # Filterlogik, die von `search()` abdriftet, wäre teurer als jeder Scan.
            counts = {
                bucket: store.search(space=space.name, limit=1, offset=0, **filters).total
                for bucket, filters in _BUCKETS.items()
            }
            # `search()` sortiert nach (offen zuerst, Fälligkeit, zuletzt geändert) — für „zuletzt
            # benutzt" ist nur das dritte Kriterium gemeint, deshalb hier nachsortieren statt
            # `storage/` anzufassen (P5-B: tabu).
            newest = sorted(
                store.search(space=space.name, limit=_STORE_FETCH_LIMIT, offset=0).items,
                key=lambda i: i.updated,
                reverse=True,
            )[:_RECENT_LIMIT]
            payload.append({
                "name": space.name,
                "own": space.name == session.space,
                "writable": permissions.can_write(session.space, space.name),
                "item_count": space.item_count,
                "counts": counts,
                "recent": [overview_row_to_json(i, own_space=session.space) for i in newest],
            })
        return JSONResponse(payload, headers={"Cache-Control": "no-store"})

    async def _items_get(request: Request) -> Response:
        session = await _require_session(request)
        q = request.query_params
        limit = max(1, min(_parse_int(q.get("limit"), default=DEFAULT_LIMIT), MAX_LIMIT))
        offset = max(0, _parse_int(q.get("offset"), default=0))
        due_before = _parse_due(q.get("due_before"))
        raw_query = q.get("query")
        query = raw_query.strip() if isinstance(raw_query, str) else None
        # P7-D: eine ID gehört an diese API-Fläche, nicht in `store.search()`s Haystack — die
        # ID-Suche muss space-/ordnerübergreifend treffen, ein Textfilter im Store würde das
        # nur mit einem Sonderfall dort erreichen.
        id_lookup = bool(query and ITEM_ID_RE.fullmatch(query))
        # P7-E: eine ID-Suche ignoriert Space- und Ordnerfilter — wer die ID hat, weiß nicht,
        # wo das Item liegt.
        global_scope = q.get("space") is None or id_lookup

        try:
            result = store.search(
                None if id_lookup else query,
                space=None if id_lookup else q.get("space"),
                folder=None if id_lookup else q.get("folder"),
                type=q.get("type"),
                status=q.get("status"),
                tag=q.get("tag"),
                due_before=due_before,
                limit=_STORE_FETCH_LIMIT,
                offset=0,
            )
        except (ValidationError, ValueError) as exc:
            raise _map_store_error(exc, own_space=session.space) from exc

        # Item-weise, nicht space-weise gefiltert (P6 Step 5, dieselbe Begründung wie
        # `mcpserver.tools.search_items`): ein einzeln freigegebenes Item darf sichtbar sein,
        # ohne dass sein ganzer Ordner es wird. `visibility: human` bleibt hier sichtbar
        # (Surface.HUMAN) — anders als auf der Agentenfläche, P6-P.
        items = [
            i for i in result.items
            if permissions.can_read_item_as_human(session.space, _acl_for_summary(i))
        ]
        if id_lookup:
            # Kein Existenz-Orakel: eine ID ohne Leserecht liefert eine leere Liste, nie 403/404
            # (derselbe Grundsatz wie `permissions.can_read_item_as_human` oben).
            items = [i for i in items if i.id == query]
        total = len(items)
        page = items[offset : offset + limit]
        item_dicts = [
            summary_to_json(
                i, own_space=session.space,
                readonly=not permissions.can_write_item_as_human(session.space, _acl_for_summary(i)),
                include_snippet=not (global_scope and i.space != session.space),
            )
            for i in page
        ]
        payload = search_to_json(item_dicts, total=total, limit=limit, offset=offset)
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
        # "folder" seit Step 7 Commit 3 (K4-Fix) dabei — `store.create()` validiert/slugifiziert
        # ihn selbst (`files.validate_folder()`), kein Zusatzcheck hier nötig.
        kwargs: dict[str, Any] = {
            key: value
            for key, value in body.items()
            if key in {"status", "due", "tags", "links", "format", "folder"}
        }
        try:
            item = store.create(session.space, type=item_type, title=title, body=item_body, **kwargs)
        except (ValidationError, ValueError) as exc:
            raise _map_store_error(exc, own_space=session.space) from exc
        return JSONResponse(
            item_to_json(item, readonly=False, own_space=session.space),
            status_code=201, headers={"Cache-Control": "no-store"},
        )

    async def _items_get_one(request: Request) -> Response:
        session = await _require_session(request)
        item_id = request.path_params["item_id"]
        try:
            acl = store.acl_of(item_id)
        except ItemNotFound as exc:
            raise _map_store_error(exc, own_space=session.space) from exc
        if not permissions.can_read_item_as_human(session.space, acl):
            raise ApiError("forbidden", "Kein Lesezugriff auf dieses Item.")
        writable = permissions.can_write_item_as_human(session.space, acl)
        item = store.get(item_id, repair_drift=writable)  # fremd ⇒ kein Dateischreibzugriff (Rule 4)
        assets = store.list_assets(item_id)
        return JSONResponse(
            item_to_json(item, readonly=not writable, own_space=session.space, assets=assets),
            headers={"Cache-Control": "no-store"},
        )

    async def _items_patch(request: Request) -> Response:
        session = await _require_session(request)
        await _require_csrf_json(request, session)
        body = await _json_body(request)
        item_id = request.path_params["item_id"]

        version = body.get("version")
        if not isinstance(version, int):
            raise ApiError("validation_failed", "'version' ist Pflichtfeld (int).")

        try:
            acl = store.acl_of(item_id)
        except ItemNotFound as exc:
            raise _map_store_error(exc, own_space=session.space) from exc
        if not permissions.can_write_item_as_human(session.space, acl):
            raise ApiError("forbidden", "Kein Schreibzugriff auf dieses Item.")

        target_space = body.get("space")
        if target_space is not None and not isinstance(target_space, str):
            raise ApiError("validation_failed", "'space' muss ein String sein.")

        # P6-AE (Step 7b, ITEM_MOVE_PLAN.md Sec2/Sec4.3): ein Space-Wechsel verlangt space-level
        # Schreibrecht auf QUELLE UND ZIEL — strenger als der item-level Check oben, weil ein
        # `share_write`-Halter, der genau ein fremdes Item bearbeiten darf, es sonst in einen
        # geteilten Space wegtragen koennte (Exfiltration und Entzug in einem Zug).
        if target_space is not None and target_space != acl.space:
            if not permissions.can_write(session.space, acl.space):
                raise ApiError("forbidden", "Kein Schreibzugriff auf den Quell-Space.")
            if not permissions.can_write(session.space, target_space):
                raise ApiError("forbidden", "Kein Schreibzugriff auf den Ziel-Space.")

        # Fail-closed, Nikinger-Entscheidung 2026-08-12 (kein Plan-Text, siehe
        # `mcpserver/tools.py::update_item`s gleichnamige Begründung): `folder` ist nur vom
        # Eigentümer-Space änderbar — ein `share_write`-Halter könnte sonst ein fremdes Item in
        # einen Ordner mit breiterer `.share.yml` verschieben und dessen Sichtbarkeit
        # erweitern, ohne dass `widens()`/Re-Auth (Step 7) das je sieht (das gilt nur für den
        # Eigentümer, der seine eigene Freigabe erweitert, nicht für einen Dritten).
        # **[2026-08-17, Step 7b, Advisor-Fund vor dem Bauen]:** greift nur noch beim reinen
        # Ordner-Move (`target_space is None`) — bei einem Space-Wechsel ersetzt ihn die
        # strengere P6-AE-Prüfung oben, sonst hätte dieser Riegel praktisch jeden legitimen
        # Cross-Space-Move mit gleichzeitig gesetztem `folder` blockiert.
        if "folder" in body and target_space is None and acl.space != session.space:
            raise ApiError(
                "forbidden",
                "folder ist nur vom Eigentümer-Space änderbar — ein geteilter Schreibzugriff "
                "erlaubt keine Verschiebung in einen anderen Ordner.",
            )

        # Re-Auth-Gate (Step 7 Commit 5a, P6-N) — MUSS vor `store.update()`/`store.move()`
        # laufen, sonst wäre die Erweiterung schon geschehen, bevor irgendetwas sie sieht.
        # `before` kommt vollständig aus `acl` (Index-only, kein zweiter Dateizugriff —
        # `AclDecision` trägt seit diesem Commit die rohen `share_read`/`share_write` genau
        # dafür). `after` übernimmt jedes im Body genannte Feld, sonst unverändert den
        # `before`-Wert — derselbe "nur was da ist, ändert sich"-Vertrag wie `store.update()`s
        # eigener `changes`-Mechanismus. `validate_folder()` läuft hier ein zweites Mal (auch
        # `store.update()`/`store.move()` ruft sie intern auf) — eine reine, günstige Funktion,
        # kein Doppelschreiben; ohne diese Normalisierung könnte ein roher `folder`-String mit
        # `..`-Segmenten `AclReader.grants_for_dir()` einen Pfad außerhalb des Space bauen
        # lassen, bevor der Store ihn je sieht.
        try:
            if "folder" in body:
                new_folder = validate_folder(body["folder"])
            elif target_space is not None:
                # Space-Wechsel ohne folder=: Ziel ist die Space-Wurzel, NICHT der gleichnamige
                # Ordner im Zielspace — ein Ordnername bedeutet dort etwas anderes und trägt
                # potenziell eine andere `.share.yml` (ITEM_MOVE_PLAN.md Sec4.1 Punkt 3).
                new_folder = ""
            else:
                new_folder = acl.folder
        except ValidationError as exc:
            raise _map_store_error(exc, own_space=session.space) from exc
        before_state = ShareState(
            visibility=acl.visibility, share_read=acl.share_read, share_write=acl.share_write,
            space=acl.space, folder=acl.folder,
        )
        after_state = ShareState(
            visibility=body.get("visibility", before_state.visibility),
            share_read=(
                frozenset(body["share_read"]) if "share_read" in body else before_state.share_read
            ),
            share_write=(
                frozenset(body["share_write"]) if "share_write" in body else before_state.share_write
            ),
            space=target_space if target_space is not None else before_state.space,
            folder=new_folder,
        )
        require_share_reauth(
            session, body, before=before_state, after=after_state, acl=store.acl_reader,
            userdir=users, throttle=throttle, auth_store=auth_store,
        )

        # `password`/`totp` dienen ausschließlich dem Re-Auth-Gate oben — landen sonst als
        # Frontmatter-Feld in `extra` (Advisor-Fund vor diesem Commit: `store.update()`s
        # `else: updated_extra[key] = value`-Zweig kennt keine Feld-Whitelist) und damit als
        # Klartext auf der Platte UND in einem Git-Commit (Hard Rule 1). Deshalb NIE an
        # `store.update()`/`store.move()` weitergereicht, unabhängig davon, ob das Gate
        # überhaupt auslöste.
        changes = {
            key: value for key, value in body.items()
            if key not in {"version", "password", "totp", "space"}
        }
        try:
            if target_space is not None:
                # Wie `mcpserver/tools.py::update_item` (Step 7b, Sec4.2): ein Move ist pur —
                # nicht mit inhaltlichen Feldern in demselben Aufruf kombinierbar. `folder`
                # gehört zum Move dazu (Zielordner im neuen Space), alles andere nicht.
                if set(changes) - {"folder"}:
                    raise ApiError(
                        "validation_failed",
                        "space verschiebt ein Item pur — kombiniere es nicht mit anderen "
                        "Feldern im selben Aufruf.",
                    )
                item = store.move(item_id, version=version, space=target_space, folder=new_folder)
            else:
                item = store.update(item_id, version=version, **changes)
        except (ItemNotFound, ConflictError, ValidationError, ValueError) as exc:
            raise _map_store_error(exc, own_space=session.space) from exc
        return JSONResponse(
            item_to_json(
                item, readonly=False, own_space=session.space,
                assets=store.list_assets(item.id),
            ),
            headers={"Cache-Control": "no-store"},
        )

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
            acl = store.acl_of(item_id)
        except ItemNotFound as exc:
            raise _map_store_error(exc, own_space=session.space) from exc
        if not permissions.can_write_item_as_human(session.space, acl):
            raise ApiError("forbidden", "Kein Schreibzugriff auf dieses Item.")

        try:
            item = store.append(item_id, version=version, text=text)
        except (ItemNotFound, ConflictError, ValidationError, ValueError) as exc:
            raise _map_store_error(exc, own_space=session.space) from exc
        return JSONResponse(
            item_to_json(
                item, readonly=False, own_space=session.space,
                assets=store.list_assets(item.id),
            ),
            headers={"Cache-Control": "no-store"},
        )

    async def _items_archive(request: Request) -> Response:
        session = await _require_session(request)
        await _require_csrf_json(request, session)
        body = await _json_body(request)
        item_id = request.path_params["item_id"]

        version = body.get("version")
        if not isinstance(version, int):
            raise ApiError("validation_failed", "'version' ist Pflichtfeld (int).")

        try:
            acl = store.acl_of(item_id)
        except ItemNotFound as exc:
            raise _map_store_error(exc, own_space=session.space) from exc
        if not permissions.can_write_item_as_human(session.space, acl):
            raise ApiError("forbidden", "Kein Schreibzugriff auf dieses Item.")

        # Siehe Moduldocstring: `store.archive()` hat keinen eigenen Schutz gegen ein bereits
        # archiviertes Item — dieser Check läuft NACH der Rechteprüfung, also sicher.
        # `repair_drift=True` ist hier korrekt, nicht weil es "der eigene Space" ist (das gilt
        # seit P6 Step 5 nicht mehr generell), sondern weil `can_write_item()` oben bereits
        # bestätigt hat, dass dieser Actor schreiben darf.
        try:
            current = store.get(item_id, repair_drift=True)
        except ItemNotFound as exc:
            raise _map_store_error(exc, own_space=session.space) from exc
        if current.status == "archived":
            raise ApiError("validation_failed", "Item ist bereits archiviert.")

        try:
            item = store.archive(item_id, version=version)
        except (ItemNotFound, ConflictError) as exc:
            raise _map_store_error(exc, own_space=session.space) from exc
        return JSONResponse(
            item_to_json(
                item, readonly=False, own_space=session.space,
                assets=store.list_assets(item.id),
            ),
            headers={"Cache-Control": "no-store"},
        )

    async def _assets_post(request: Request) -> Response:
        session = await _require_session(request)
        await _require_csrf_json(request, session)  # keine JSON-Content-Type-Abhängigkeit (V66)
        item_id = request.path_params["item_id"]
        try:
            acl = store.acl_of(item_id)
        except ItemNotFound as exc:
            raise _map_store_error(exc, own_space=session.space) from exc
        if not permissions.can_write_item_as_human(session.space, acl):
            raise ApiError("forbidden", "Kein Schreibzugriff auf dieses Item.")

        # Kein `filename` an `put_asset()` -- der Plan spezifiziert rohe Bytes, kein Multipart-
        # Formularfeld (Z. 401f.), es gibt hier also nichts zu lesen. `asset_to_json()` liefert
        # deshalb `filename=""` für jedes über diese Route hochgeladene Bild (B1s Advisor-Punkt
        # 4, ausdrücklich für B2/B4 vorgemerkt) -- weiterhin unbehoben, jetzt zum zweiten Mal
        # bewusst re-vertagt statt still verschluckt: B3 (Editor-Upload) kennt den echten
        # Dateinamen aus der `<input type="file">`-Auswahl und ist der frühestmögliche Ort, an
        # dem eine Entscheidung (Persistenz vs. Parameter streichen) etwas zu tragen hätte.
        data = await _raw_body(request)
        try:
            asset = store.put_asset(item_id, data=data)
        except (ItemNotFound, ValidationError) as exc:
            raise _map_store_error(exc, own_space=session.space) from exc
        return JSONResponse(
            asset_to_json(asset), status_code=201, headers={"Cache-Control": "no-store"},
        )

    async def _assets_get_list(request: Request) -> Response:
        session = await _require_session(request)
        item_id = request.path_params["item_id"]
        try:
            acl = store.acl_of(item_id)
        except ItemNotFound as exc:
            raise _map_store_error(exc, own_space=session.space) from exc
        if not permissions.can_read_item_as_human(session.space, acl):
            raise ApiError("forbidden", "Kein Lesezugriff auf dieses Item.")
        assets = store.list_assets(item_id)
        return JSONResponse(
            [asset_to_json(a) for a in assets], headers={"Cache-Control": "no-store"},
        )

    async def _assets_get_one(request: Request) -> Response:
        session = await _require_session(request)
        item_id = request.path_params["item_id"]
        asset_id = request.path_params["asset_id"]
        try:
            acl = store.acl_of(item_id)
        except ItemNotFound as exc:
            raise _map_store_error(exc, own_space=session.space) from exc
        if not permissions.can_read_item_as_human(session.space, acl):
            raise ApiError("forbidden", "Kein Lesezugriff auf dieses Item.")
        try:
            data, mime = store.get_asset(item_id, asset_id)
        except ItemNotFound as exc:
            raise _map_store_error(exc, own_space=session.space) from exc
        return Response(
            data,
            media_type=mime,
            headers={
                "Content-Disposition": "inline",
                "Cache-Control": "no-store",
                # V67 geschlossen: `ui_security_headers()` läuft nur auf `/ui/*`-HTML-Seiten
                # (`routes_auth.py`/`static_routes.py`), nicht auf `/api/v1/**` — für eine
                # rohe Bild-Antwort deshalb hier explizit, statt sich auf eine Annahme zu
                # verlassen, die der Plan als bereits gegeben unterstellte.
                "X-Content-Type-Options": "nosniff",
            },
        )

    async def _assets_delete(request: Request) -> Response:
        session = await _require_session(request)
        await _require_csrf_json(request, session)
        item_id = request.path_params["item_id"]
        asset_id = request.path_params["asset_id"]
        try:
            acl = store.acl_of(item_id)
        except ItemNotFound as exc:
            raise _map_store_error(exc, own_space=session.space) from exc
        if not permissions.can_write_item_as_human(session.space, acl):
            raise ApiError("forbidden", "Kein Schreibzugriff auf dieses Item.")
        try:
            store.delete_asset(item_id, asset_id)
        except ItemNotFound as exc:
            raise _map_store_error(exc, own_space=session.space) from exc
        return JSONResponse({"ok": True}, headers={"Cache-Control": "no-store"})

    async def _updates_get(request: Request) -> Response:
        session = await _require_session(request)
        entries = load_update_log(settings.update_log_path)
        latest_id = entries[0].id if entries else None
        payload = {
            "entries": [{"id": e.id, "date": e.date, "lines": e.lines} for e in entries],
            "latest_id": latest_id,
            "seen_update_id": auth_store.get_seen_update_id(session.space),
        }
        return JSONResponse(payload, headers={"Cache-Control": "no-store"})

    async def _updates_seen(request: Request) -> Response:
        session = await _require_session(request)
        await _require_csrf_json(request, session)
        entries = load_update_log(settings.update_log_path)
        if entries:
            auth_store.set_seen_update_id(session.space, entries[0].id)
        return JSONResponse({"ok": True}, headers={"Cache-Control": "no-store"})

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
        Route("/api/v1/spaces/{space}/folders", _catch(_spaces_create_folder), methods=["POST"]),
        Route("/api/v1/meta", _catch(_meta), methods=["GET"]),
        Route("/api/v1/overview", _catch(_overview), methods=["GET"]),
        Route("/api/v1/updates", _catch(_updates_get), methods=["GET"]),
        Route("/api/v1/updates/seen", _catch(_updates_seen), methods=["POST"]),
        Route("/api/v1/items", _catch(_items_get), methods=["GET"]),
        Route("/api/v1/items", _catch(_items_post), methods=["POST"]),
        Route("/api/v1/items/{item_id}", _catch(_items_get_one), methods=["GET"]),
        Route("/api/v1/items/{item_id}", _catch(_items_patch), methods=["PATCH"]),
        Route("/api/v1/items/{item_id}/append", _catch(_items_append), methods=["POST"]),
        Route("/api/v1/items/{item_id}/archive", _catch(_items_archive), methods=["POST"]),
        Route("/api/v1/items/{item_id}/assets", _catch(_assets_post), methods=["POST"]),
        Route("/api/v1/items/{item_id}/assets", _catch(_assets_get_list), methods=["GET"]),
        Route(
            "/api/v1/items/{item_id}/assets/{asset_id}", _catch(_assets_get_one), methods=["GET"],
        ),
        Route(
            "/api/v1/items/{item_id}/assets/{asset_id}", _catch(_assets_delete),
            methods=["DELETE"],
        ),
    ]
