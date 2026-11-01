#!/usr/bin/env python3
"""P10.5 Block 16.1 — die KI-Szene (S9): ein **echter** MCP-Client gegen die Wegwerf-Instanz.

Plan §3.2: ein echter Lauf, aufgezeichnet und in der Bühne wiedergegeben — echte Daten, eine
deterministische Darstellung, kein Modellaufruf je Render. Der Client ist der FastMCP-Client über
HTTPS auf 127.0.0.1:8811 (`neu`, `wegwerf.py`) mit einem Bearer-Token, das dieser Lauf direkt im
tmp-`auth.sqlite3` ausstellt (Muster `phase2_mcp/scripts/mcp_smoke.py`). Das Token lebt nur im
Speicher dieses Prozesses; das Transkript wird vor dem Schreiben **geprüft**: kein Token, keine
URL, kein Host, kein `Bearer` (Plan §4).

Aufruf: `.venv/bin/python ki_lauf.py` — der Lauf startet sich selbst neu in der Umgebung der
Instanz (`wegwerf._env("neu")`). Ausgabe: `~/sharefyx-film/ki_lauf.json` + JSON auf stdout.
"""
from __future__ import annotations

import asyncio
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

FILM = Path(__file__).resolve().parent
OUT = Path.home() / "sharefyx-film" / "ki_lauf.json"


def _aussen() -> int:
    sys.path.insert(0, str(FILM))
    import wegwerf

    env = {**wegwerf._env("neu"), "FILM_KI_INNEN": "1"}
    return subprocess.run([str(wegwerf.REPO_ROOT / ".venv/bin/python"), __file__], env=env).returncode


async def _innen() -> dict:
    import httpx
    from authserver.config import load_auth_settings
    from authserver.store import AuthStore
    from fastmcp import Client
    from fastmcp.client.transports import StreamableHttpTransport

    settings = load_auth_settings()
    store = AuthStore(settings.db_path, now_fn=lambda: datetime.now(timezone.utc))
    family = store.create_family(space="studio", client_id="film_ki", scope="space",
                                 resource=settings.resource)
    token, _refresh = store.issue_token_pair(family, access_ttl_s=600, refresh_ttl_s=600)
    port = os.environ["SPACE_PORT"]
    transport = StreamableHttpTransport(
        url=f"https://127.0.0.1:{port}/mcp/", headers={"Authorization": f"Bearer {token}"},
        httpx_client_factory=lambda **kw: httpx.AsyncClient(verify=False, **kw))
    schritte: list[dict] = []

    def text(res) -> str:
        return "".join(getattr(c, "text", "") for c in res.content)

    async with Client(transport) as client:
        r = await client.call_tool("list_spaces", {})
        spaces = json.loads(text(r))
        schritte.append({"tool": "list_spaces", "args": {}, "ergebnis": spaces})
        r = await client.call_tool("search_items", {"query": "Wochenplan", "limit": 3})
        treffer = json.loads(text(r))
        schritte.append({"tool": "search_items", "args": {"query": "Wochenplan", "limit": 3},
                         "ergebnis": treffer})
        items = treffer.get("items", treffer.get("results", []))[:3]
        entries = [{"item_id": it["id"], "version": it["version"],
                    "text": "- Termin mit dem Team bestätigt"} for it in items]
        r = await client.call_tool("append_to_items", {"entries": entries})
        schritte.append({"tool": "append_to_items",
                         "args": {"entries": [{**e, "titel": it.get("title")}
                                              for e, it in zip(entries, items)]},
                         "ergebnis": json.loads(text(r))})
    store.revoke_family(family, reason="film_ki_fertig")
    roh = json.dumps(schritte, ensure_ascii=False)
    for verboten in (token, _refresh, "127.0.0.1", "Bearer", "https://", f":{port}"):
        if verboten in roh:
            raise SystemExit("Transkript enthält Verbotenes — nichts geschrieben")
    return {"client": "FastMCP-Client (Python)", "schritte": schritte}


def main() -> int:
    if os.environ.get("FILM_KI_INNEN") != "1":
        return _aussen()
    lauf = asyncio.run(_innen())
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(lauf, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"datei": str(OUT), "schritte": [s["tool"] for s in lauf["schritte"]]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
