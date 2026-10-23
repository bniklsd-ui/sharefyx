"""P10.5 Block 5, Schritt 5.6 — Protokoll-Probe: beide Ären in-process gegen `create_app()`.

Vorlage: `~/.claude-code-tools/p105/proto_probe.py` (Planungssession 2026-10-20, Tabelle §1.2 des Plans).
Hier neu geschrieben und erweitert um die Abnahme-Zeilen P10.5-20/21: je Ära `list_spaces`,
die Annotations aus `tools/list`, die elf Werkzeugnamen und ein `append_to_items`-Teilerfolg;
dazu der Gegenlauf (Anfrage mit unbekannter Protokollversion → Fehler).

In-process (`httpx.ASGITransport`), `tmp`-`DATA_ROOT`, `tmp`-Auth-DB, kein Netz, kein Port, nie der
echte `DATA_ROOT`/Keyring. Ausgabe: JSON auf stdout (Hard Rule 7), `--out <datei>` schreibt zusätzlich
die Rohwerte. Aufruf: `.venv/bin/python phase10_5_finishing/probes/p105_b5_protocol_probe.py`.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import tempfile
import warnings
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import httpx
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

from authserver.config import AuthSettings
from authserver.store import AuthStore
from authserver.userdir import UserDirectory
from mcpserver.app import OAuthConfig, create_app
from mcpserver.config import Settings
from storage.store import Store

BASE = "http://probe.local"
ERA_OF_MODE = {"legacy": "2025-11-25", "auto": "2026-07-28"}


def _build() -> tuple[Any, str]:
    tmp = Path(tempfile.mkdtemp(prefix="p105b5_"))
    settings = AuthSettings(base_url="https://probe.local", db_path=tmp / "_a.sqlite3")
    auth = AuthStore(settings.db_path, now_fn=lambda: datetime.now(timezone.utc))
    family = auth.create_family(space="alpha", client_id="probe", scope="space", resource=settings.resource)
    token, _ = auth.issue_token_pair(family, access_ttl_s=3600, refresh_ttl_s=3600)
    store = Store(tmp, git=False)
    store.create("alpha", type="note", title="Ausgangspunkt", body="x")
    app = create_app(
        settings=Settings(data_root=tmp), store=store,
        oauth=OAuthConfig(settings=settings, store=auth, users=UserDirectory(auth, dek=None)),
    )
    return app, token


async def _one_era(app: Any, token: str, mode: str) -> dict[str, Any]:
    def factory(**kw: Any) -> httpx.AsyncClient:
        return httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=BASE, **kw)

    transport = StreamableHttpTransport(
        url=f"{BASE}/mcp/", headers={"Authorization": f"Bearer {token}"}, httpx_client_factory=factory
    )
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        async with Client(transport, mode=mode) as client:
            spaces = json.loads((await client.call_tool("list_spaces", {})).data)
            tools = await client.list_tools()
            made = [
                json.loads((await client.call_tool("create_item", {"type": "note", "title": f"P{n}"})).data)
                for n in (1, 2)
            ]
            many = json.loads(
                (
                    await client.call_tool(
                        "append_to_items",
                        {"entries": [
                            {"item_id": made[0]["id"], "version": made[0]["version"], "text": "a"},
                            {"item_id": made[1]["id"], "version": made[1]["version"] + 99, "text": "b"},
                        ]},
                    )
                ).data
            )
            return {
                "protocol_version": client.protocol_version,
                "list_spaces": [s["name"] for s in spaces],
                "tool_names": sorted(t.name for t in tools),
                "annotations_complete": all(
                    t.annotations is not None
                    and None not in (
                        t.annotations.read_only_hint, t.annotations.destructive_hint,
                        t.annotations.idempotent_hint, t.annotations.open_world_hint,
                    )
                    for t in tools
                ),
                "append_to_items": {"ok": many["ok"], "failed": many["failed"]},
                "deprecation_warnings": sorted(
                    {str(w.message)[:120] for w in caught if "eprecat" in type(w.message).__name__ + str(w.message)}
                ),
            }


async def _unknown_version(app: Any, token: str) -> dict[str, Any]:
    """Gegenlauf (P10.5-20), zwei Wege — beide gemessen, nicht angenommen (Block 5, 2026-10-22):

    * `initialize` (Handshake-Ära): ein Server antwortet mit **seiner** höchsten Version statt mit einem
      Fehler (so verlangt es die Handshake-Aushandlung) — er darf sie nie zurückspiegeln.
    * `tools/list` mit Header + Envelope der neuen Ära (zustandslos, kein Handshake): JSON-RPC-Fehler
      `-32022 Unsupported protocol version`, `data.supported == ["2026-07-28"]`.
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json, text/event-stream",
        "Content-Type": "application/json",
    }
    init = {
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"protocolVersion": "1999-01-01", "capabilities": {},
                   "clientInfo": {"name": "raw", "version": "0"}},
    }
    stateless = {
        "jsonrpc": "2.0", "id": 2, "method": "tools/list",
        "params": {"_meta": {
            "io.modelcontextprotocol/protocolVersion": "1999-01-01",
            "io.modelcontextprotocol/clientCapabilities": {},
        }},
    }
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=BASE) as http:
        r_init = await http.post("/mcp/", json=init, headers=headers)
        r_new = await http.post(
            "/mcp/", json=stateless,
            headers={**headers, "MCP-Protocol-Version": "1999-01-01", "Mcp-Method": "tools/list"},
        )
    answered = r_init.text.split('"protocolVersion"')[-1][:40]
    error = r_new.json().get("error", {})
    return {
        "initialize": {
            "status": r_init.status_code,
            "echoes_unknown_version": "1999-01-01" in answered,
            "answers_with_own_version": "2025-11-25" in answered,
        },
        "stateless_tools_list": {
            "status": r_new.status_code,
            "error_code": error.get("code"),
            "error_message": error.get("message"),
            "supported": (error.get("data") or {}).get("supported"),
        },
    }


async def run() -> dict[str, Any]:
    app, token = _build()
    out: dict[str, Any] = {}
    async with app.router.lifespan_context(app):
        for mode in ("legacy", "auto"):
            out[mode] = await _one_era(app, token, mode)
            out[mode]["expected_era"] = ERA_OF_MODE[mode]
        out["unknown_version"] = await _unknown_version(app, token)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, help="Rohwerte zusätzlich in diese JSON-Datei schreiben")
    args = parser.parse_args()
    result = asyncio.run(run())
    text = json.dumps(result, indent=2, ensure_ascii=False)
    if args.out:
        args.out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
