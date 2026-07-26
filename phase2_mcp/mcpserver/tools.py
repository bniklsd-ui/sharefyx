"""Die sechs MCP-Tools (Plan §3). Registrierung über `register(mcp, store=..., permissions=...)`,
damit `server.py :: build_mcp()` `tools.py` kennt, aber `tools.py` selbst weder HTTP noch Token
kennt — nur einen Principal (`context.py`) und eine Policy (`permissions.py`), siehe Plan §1.2.

**Step 6 (dieser Stand):** alle sechs Tools sind vollständig implementiert (§3.2/§3.4/§3.5/§3.6).
`list_spaces` war bereits seit Step 5 fertig (Voraussetzung für den End-to-End-Isolationstest in
`test_app.py`); die übrigen fünf lösen hier ihre `NotImplementedError`-Platzhalter ab.

**`item_to_filetext()` dupliziert bewusst die Feldreihenfolge von `storage.store._item_to_text`**
statt eine neue Store-Methode zu verlangen: der P1-Contract ist seit Step 2 "wieder zu" (siehe
`phase1_storage/CLAUDE.md`), eine weitere einmalige Erweiterung wäre keine mehr. Der MCP-Adapter
baut den Dateitext deshalb selbst aus `Item` + `storage.frontmatter.serialize` — dieselbe
öffentliche Funktion, die `store.py` intern auch benutzt.
"""
from __future__ import annotations

import json
import logging
from collections.abc import Callable
from dataclasses import replace
from datetime import date, datetime, timezone
from typing import Any

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

from storage.errors import ConflictError, ItemNotFound, SpaceNotFound, ValidationError
from storage.frontmatter import serialize as serialize_frontmatter
from storage.models import Item, ItemSummary, SpaceInfo
from storage.store import Store

from . import context
from .auth import AuthError
from .permissions import Permissions

logger = logging.getLogger(__name__)

# Token-Budget (Plan P2-J) — Modulkonstanten, keine verstreuten Literale. `Store.search()`
# selbst bleibt bei `limit=50` im Kern (P1); diese Konstanten gelten nur für den MCP-Adapter.
DEFAULT_LIMIT = 20
MAX_LIMIT = 100
DEFAULT_INCLUDE_ARCHIVED = False

UNTRUSTED_OPEN = '<untrusted_content space="{space}">'
UNTRUSTED_CLOSE = "</untrusted_content>"

# [SEAM] Bekannte Grenze wie D6 (Plan §2.2, ROADMAP „Zurückgestellt aus P2"): `Store.search()`
# filtert nicht nach einer Statusliste (nur exakter Match), deshalb holt der Adapter hier alles
# bis zu dieser Grenze und filtert/paginiert `include_archived`/`offset`/`limit` selbst. Store
# scannt ohnehin jede indizierte Datei pro Aufruf (kein SQL-Filter) — diese Konstante ändert an
# der Kostenstruktur nichts, deckt aber den heutigen Datenumfang (Zwei-Personen-Space-Server)
# um Größenordnungen ab. Steigt das Volumen darüber, gehört die Filterung in den Store, nicht
# in eine höhere Konstante hier.
_STORE_FETCH_LIMIT = 5000


class PermissionDenied(Exception):
    """P2-eigen (kein `storage`-Fehlertyp) — `can_read`/`can_write` verweigert (Plan §3.6)."""

    def __init__(self, space: str) -> None:
        super().__init__(f"kein Zugriff auf Space {space!r}")
        self.space = space


def wrap_untrusted(text: str, *, space: str) -> str:
    """Plan §3.5, wörtlich. Ohne das Escaping ist der Wrap ausbrechbar: eine fremde Notiz mit
    einem eigenen Closing-Tag würde den Block vorzeitig schließen und alles danach als
    vertrauenswürdigen Servertext erscheinen lassen — die Prompt-Injection, gegen die Rule 4
    überhaupt existiert."""
    safe = text.replace("</untrusted_content", "</untrusted_ content")
    return f"{UNTRUSTED_OPEN.format(space=space)}\n{safe}\n{UNTRUSTED_CLOSE}"


def compact_json(payload: Any) -> str:
    """Entscheidung I: kompaktes JSON als Text-Content, keine ASCII-Escapes."""
    return json.dumps(payload, separators=(",", ":"), ensure_ascii=False)


def _format_dt(value: datetime) -> str:
    """Gleiche Formatierung wie `storage.store._format_dt` — Dateitext und JSON-Ausgabe zeigen
    identische Zeitstempel."""
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse_due_before(value: str | None) -> date | None:
    if value is None:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValidationError(
            f"'due_before' muss ein ISO-Datum sein (YYYY-MM-DD), nicht {value!r}"
        ) from exc


def item_to_filetext(item: Item) -> str:
    """Frontmatter + Body als Dateitext — siehe Moduldocstring zur bewussten Duplikation."""
    fields: dict[str, Any] = {
        "id": item.id,
        "space": item.space,
        "type": item.type,
        "title": item.title,
        "status": item.status,
    }
    if item.due is not None:
        fields["due"] = item.due.isoformat()
    fields["tags"] = list(item.tags)
    fields["links"] = list(item.links)
    fields["created"] = _format_dt(item.created)
    fields["updated"] = _format_dt(item.updated)
    fields["version"] = item.version
    fields.update(item.extra)
    return serialize_frontmatter(fields, item.body)


def summary_to_dict(item: ItemSummary, *, own: bool) -> dict[str, Any]:
    """Plan §3.2 Feldliste (bewusst ohne `created`). Fremde Snippets sind gewrappt (§3.5)."""
    return {
        "id": item.id,
        "space": item.space,
        "type": item.type,
        "title": item.title,
        "status": item.status,
        "due": item.due.isoformat() if item.due is not None else None,
        "tags": list(item.tags),
        "links": list(item.links),
        "updated": _format_dt(item.updated),
        "version": item.version,
        "snippet": item.snippet if own else wrap_untrusted(item.snippet, space=item.space),
    }


def map_storage_error(exc: Exception) -> ToolError:
    """Plan §3.6 — jede Meldung nennt den nächsten Schritt, nicht nur den Zustand."""
    if isinstance(exc, ItemNotFound):
        return ToolError(f"item_not_found: {exc.item_id} — prüfe die ID mit search_items")
    if isinstance(exc, PermissionDenied):
        return ToolError(f"write_denied: {exc.space} ist nicht dein Space; du kannst dort nur lesen")
    if isinstance(exc, ConflictError):
        current = exc.current
        return ToolError(
            f"conflict: {exc.item_id} wurde geändert (deine Version {exc.expected_version}, "
            f"aktuell {current.version}, zuletzt {_format_dt(current.updated)}) — lies neu mit "
            "get_item und wiederhole"
        )
    if isinstance(exc, ValidationError):
        return ToolError(f"invalid: {exc}")
    if isinstance(exc, SpaceNotFound):
        return ToolError(f"space_not_found: {exc.space}")
    if isinstance(exc, AuthError):
        # Step-4-Advisor-Fund (siehe SESSIONS_ARCHIVE.md): der Guard wirft AuthError INNERHALB
        # eines Tool-Aufrufs — das 401-Fenster ist zu diesem Zeitpunkt vorbei, es muss
        # zwangsläufig als Tool-Fehler auftauchen. Kein Defekt (weiterhin fail-closed, keine
        # fremden Daten), aber P2-N verlangt "nie unterscheidbar von falschem Token" — deshalb
        # kein Detail hier, kein Unterschied zu einem anderen Auth-Fehlschlag.
        return ToolError("auth_error: Request-Kontext ungültig — bitte neu verbinden")
    logger.exception("internal_error in MCP tool", exc_info=exc)
    return ToolError("internal_error — siehe Serverlog")


def _authenticated_principal():
    """Schritt 1+2 aus §3.3 gebündelt (`current_principal()` → Guard). Ein `AuthError` aus dem
    Guard läuft — anders als ein fehlendes/unbekanntes Pfad-Token — INNERHALB eines laufenden
    Tool-Aufrufs; das 401-Fenster ist zu diesem Zeitpunkt vorbei (Step-4-Advisor-Fund, siehe
    `SESSIONS_ARCHIVE.md`). Ohne dieses Bündeln würde ein solcher `AuthError` roh aus dem Tool
    fallen statt über `map_storage_error()` in die einheitliche Fehlerabbildung (§3.6) zu laufen
    — genau die Abbildung, die dort als „bewusst zu treffen, nicht zufällig" verlangt wird."""
    try:
        principal = context.current_principal()
        context.assert_principal_matches_request()
        return principal
    except AuthError as exc:
        raise map_storage_error(exc) from exc


def register(mcp: FastMCP, *, store: Store, permissions: Permissions) -> dict[str, Callable[..., str]]:
    """Registriert alle sechs Tools auf `mcp`. Reihenfolge in jedem Tool-Body wie Plan §3.3:
    `current_principal()` → Guard → Zielraum → Rechte → Store → Formatieren. `@mcp.tool(...)`
    gibt die unveränderte Python-Funktion zurück (nicht das interne `FunctionTool`-Objekt) —
    `register()` sammelt genau diese Funktionen und gibt sie zurück, damit Tests sie direkt
    aufrufen bzw. per `inspect.signature()` prüfen können (z. B.
    `test_create_item_has_no_space_parameter`), ohne den vollen ASGI/HTTP-Stack aus Step 5
    erneut hochzuziehen."""

    @mcp.tool(
        title="Spaces auflisten",
        description=(
            "Listet alle sichtbaren Spaces mit Item-Anzahl. `writable` ist nur für den "
            "eigenen Space true."
        ),
        annotations={
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        },
    )
    def list_spaces() -> str:
        principal = _authenticated_principal()
        spaces = store.list_spaces()
        # Fund B1 aus der Live-Adapter-Abnahme (docs/concepts/P2_ADAPTER_ABNAHME_2026-07-26.md):
        # `Store.list_spaces()` leitet Spaces ausschließlich aus vorhandenen Indexzeilen ab (P1,
        # keine separate Space-Registry) — ein Space ohne ein einziges Item taucht dort schlicht
        # nicht auf. Ohne diesen Fallback sähe eine frische Claude-Sitzung mit einem leeren
        # eigenen Space AUSSCHLIESSLICH Spaces, in die sie nicht schreiben darf, und hätte keine
        # Möglichkeit, den eigenen Space-Namen zu erfahren, bevor sie blind `create_item` ruft.
        # `create_item` selbst ist davon nicht betroffen (der Ziel-Space kommt aus dem Principal,
        # nie aus `list_spaces`), aber die Orientierung des Modells ist es. Deshalb: der eigene
        # Space wird immer in die Antwort aufgenommen, notfalls mit `item_count=0` — kein
        # Store-Eingriff, reine Tool-Schicht-Ergänzung.
        if principal.space not in {s.name for s in spaces}:
            spaces = sorted(
                [*spaces, SpaceInfo(name=principal.space, item_count=0)], key=lambda s: s.name
            )
        visible_names = set(
            permissions.visible_spaces(principal.space, [s.name for s in spaces])
        )
        payload = [
            {
                "name": s.name,
                "item_count": s.item_count,
                "writable": permissions.can_write(principal.space, s.name),
            }
            for s in spaces
            if s.name in visible_names
        ]
        return compact_json(payload)

    @mcp.tool(
        title="Items durchsuchen",
        description=(
            "Sucht Items über alle sichtbaren Spaces (Frontmatter + Snippet, nie der volle "
            "Body). Fremde Snippets sind gewrappt."
        ),
        annotations={
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        },
    )
    def search_items(
        query: str | None = None,
        space: str | None = None,
        type: str | None = None,
        status: str | None = None,
        tag: str | None = None,
        due_before: str | None = None,
        limit: int = DEFAULT_LIMIT,
        offset: int = 0,
        include_archived: bool = DEFAULT_INCLUDE_ARCHIVED,
    ) -> str:
        principal = _authenticated_principal()
        clamped_limit = max(1, min(limit, MAX_LIMIT))

        try:
            due_before_date = _parse_due_before(due_before)
            result = store.search(
                query,
                space=space,
                type=type,
                status=status,
                tag=tag,
                due_before=due_before_date,
                limit=_STORE_FETCH_LIMIT,
                offset=0,
            )
        except ValidationError as exc:
            raise map_storage_error(exc) from exc

        visible_names = set(
            permissions.visible_spaces(principal.space, [s.name for s in store.list_spaces()])
        )
        items = [i for i in result.items if i.space in visible_names]
        if status is None and not include_archived:
            items = [i for i in items if i.status != "archived"]

        total = len(items)
        page = items[offset : offset + clamped_limit]
        payload = {
            "items": [
                summary_to_dict(i, own=permissions.can_write(principal.space, i.space))
                for i in page
            ],
            "total": total,
            "limit": clamped_limit,
            "offset": offset,
            "truncated": offset + clamped_limit < total,
        }
        return compact_json(payload)

    @mcp.tool(
        title="Item lesen",
        description="Liest ein Item als Dateitext (Frontmatter + Body). Fremde Bodies sind gewrappt.",
        annotations={
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        },
    )
    def get_item(item_id: str) -> str:
        principal = _authenticated_principal()
        try:
            space = store.space_of(item_id)
        except ItemNotFound as exc:
            raise map_storage_error(exc) from exc

        if not permissions.can_read(principal.space, space):
            # Heute unerreichbar (`OwnSpaceWritable.can_read` ist immer True) — der Seam ist
            # trotzdem verdrahtet, damit eine spätere Policy hier nicht nachgerüstet werden muss
            # (Plan §2.2 Erweiterungspfad).
            raise map_storage_error(PermissionDenied(space)) from None

        own = permissions.can_write(principal.space, space)
        item = store.get(item_id, repair_drift=own)  # fremd ⇒ kein Dateischreibzugriff (Rule 4)
        if not own:
            item = replace(item, body=wrap_untrusted(item.body, space=item.space))
        return item_to_filetext(item)

    @mcp.tool(
        title="Item anlegen",
        description="Legt ein neues Item im eigenen Space an — der Ziel-Space ist immer der Principal.",
        annotations={
            "readOnlyHint": False,
            "destructiveHint": False,
            "idempotentHint": False,
            "openWorldHint": False,
        },
    )
    def create_item(
        type: str,
        title: str,
        body: str = "",
        tags: list[str] | None = None,
        links: list[str] | None = None,
        due: str | None = None,
        status: str | None = None,
    ) -> str:
        principal = _authenticated_principal()
        # Keine Rechteprüfung nötig — es gibt keinen `space`-Parameter (P2-G, Rule 4
        # architektonisch statt per `if`), der Ziel-Space ist immer `principal.space`.
        kwargs: dict[str, Any] = {"tags": tags or [], "links": links or []}
        if due is not None:
            kwargs["due"] = due
        if status is not None:
            kwargs["status"] = status
        try:
            item = store.create(principal.space, type=type, title=title, body=body, **kwargs)
        except ValidationError as exc:
            raise map_storage_error(exc) from exc
        return item_to_filetext(item)

    @mcp.tool(
        title="Item aktualisieren",
        description=(
            "Aktualisiert ein Item im eigenen Space, oder archiviert es über status=archived. "
            "Braucht die zuletzt gelesene version."
        ),
        annotations={
            "readOnlyHint": False,
            "destructiveHint": True,
            "idempotentHint": False,
            "openWorldHint": False,
        },
    )
    def update_item(
        item_id: str,
        version: int,
        title: str | None = None,
        body: str | None = None,
        status: str | None = None,
        tags: list[str] | None = None,
        links: list[str] | None = None,
        due: str | None = None,
        type: str | None = None,
    ) -> str:
        principal = _authenticated_principal()
        try:
            target_space = store.space_of(item_id)
        except ItemNotFound as exc:
            raise map_storage_error(exc) from exc

        if not permissions.can_write(principal.space, target_space):
            raise map_storage_error(PermissionDenied(target_space)) from None

        changes = {
            key: value
            for key, value in {
                "title": title,
                "body": body,
                "tags": tags,
                "links": links,
                "due": due,
                "type": type,
            }.items()
            if value is not None
        }

        try:
            if status == "archived":
                if changes:
                    raise ValidationError(
                        "status=archived erlaubt keine weiteren Felder — erst inhaltlich "
                        "updaten, dann archivieren"
                    )
                item = store.archive(item_id, version=version)
            else:
                if status is not None:
                    changes["status"] = status
                item = store.update(item_id, version=version, **changes)
        except (ItemNotFound, ConflictError, ValidationError) as exc:
            raise map_storage_error(exc) from exc
        return item_to_filetext(item)

    @mcp.tool(
        title="Text an Item anhängen",
        description="Hängt Text an den Body eines Items im eigenen Space an. Braucht die zuletzt gelesene version.",
        annotations={
            "readOnlyHint": False,
            "destructiveHint": False,
            "idempotentHint": False,
            "openWorldHint": False,
        },
    )
    def append_to_item(item_id: str, version: int, text: str) -> str:
        principal = _authenticated_principal()
        try:
            target_space = store.space_of(item_id)
        except ItemNotFound as exc:
            raise map_storage_error(exc) from exc

        if not permissions.can_write(principal.space, target_space):
            raise map_storage_error(PermissionDenied(target_space)) from None

        try:
            item = store.append(item_id, version=version, text=text)
        except (ItemNotFound, ConflictError, ValidationError) as exc:
            raise map_storage_error(exc) from exc
        return item_to_filetext(item)

    return {
        "list_spaces": list_spaces,
        "search_items": search_items,
        "get_item": get_item,
        "create_item": create_item,
        "update_item": update_item,
        "append_to_item": append_to_item,
    }
