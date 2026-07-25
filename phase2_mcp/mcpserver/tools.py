"""Die sechs MCP-Tools (Plan §3). Registrierung über `register(mcp, store=..., permissions=...)`,
damit `server.py :: build_mcp()` `tools.py` kennt, aber `tools.py` selbst weder HTTP noch Token
kennt — nur einen Principal (`context.py`) und eine Policy (`permissions.py`), siehe Plan §1.2.

**Umfang Step 5 vs. Step 6:** `list_spaces` ist ab Step 5 vollständig implementiert — Step 5
braucht ein echtes, funktionierendes Tool, um `TokenPathASGI` + den Guard end-to-end gegen eine
laufende FastMCP-App zu beweisen (`test_app.py::test_principal_isolation_under_concurrency`,
die wichtigste Zusicherung der Phase). Die übrigen fünf Tools sind mit finaler Signatur, Titel,
Beschreibung und Annotations registriert (das macht `tools/list` bereits jetzt korrekt), werfen
aber bewusst `NotImplementedError` — ihre Semantik (Wrapping, Fehlerabbildung, Token-Budget)
ist Step 6 (Plan §3.2, §3.5, §3.6), nicht vorgezogen (Plan §7: „Vorziehen der nächsten Phase
versenkt die aktuelle").
"""
from __future__ import annotations

import json

from fastmcp import FastMCP

from storage.store import Store

from . import context
from .permissions import Permissions

# Token-Budget (Plan P2-J) — Modulkonstanten, keine verstreuten Literale. `Store.search()`
# selbst bleibt bei `limit=50` im Kern (P1); diese Konstanten gelten nur für den MCP-Adapter.
DEFAULT_LIMIT = 20
MAX_LIMIT = 100


def register(mcp: FastMCP, *, store: Store, permissions: Permissions) -> None:
    """Registriert alle sechs Tools auf `mcp`. Reihenfolge in jedem Tool-Body wie Plan §3.3:
    `current_principal()` → Guard → Zielraum → Rechte → Store → Formatieren."""

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
        principal = context.current_principal()
        context.assert_principal_matches_request()
        spaces = store.list_spaces()
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
        return json.dumps(payload, separators=(",", ":"), ensure_ascii=False)

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
        include_archived: bool = False,
    ) -> str:
        raise NotImplementedError("search_items folgt in Step 6 (Plan §3.2/§3.5/§3.6)")

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
        raise NotImplementedError("get_item folgt in Step 6 (Plan §3.4)")

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
        raise NotImplementedError("create_item folgt in Step 6 (Plan §3.2)")

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
        raise NotImplementedError("update_item folgt in Step 6 (Plan §3.2)")

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
        raise NotImplementedError("append_to_item folgt in Step 6 (Plan §3.2)")
