"""`create_app()` — Starlette-Wurzel-App: `/health` (unauthentifiziert) + `Mount("/mcp")` mit
`TokenPathASGI` davor (Plan §1.1, §4 Step 5). Kennt alles (`config`, `auth`, `permissions`,
`server`, `asgi`) — das ist die einzige Stelle, die alle Seams zusammensteckt.

**`OwnSpaceWritable()` wird hier instanziiert, nicht injiziert** (Plan §2.2 Erweiterungspfad):
eine spätere `PolicyPermissions` mit echten Lese-Regeln zwischen Spaces ist damit ein
Konstruktor-Austausch an dieser einen Stelle, kein Umbau von `tools.py`/`server.py`.
"""
from __future__ import annotations

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Mount, Route

from storage.store import Store

from . import __version__
from .asgi import TokenPathASGI
from .auth import SpaceResolver
from .config import Settings
from .permissions import OwnSpaceWritable
from .request_log import ToolCallLogMiddleware
from .server import build_mcp


async def _health(request: Request) -> JSONResponse:
    # Unauthentifiziert (Plan §4 Step 5) — deshalb bewusst keine Space-Namen, keine Pfade,
    # keine Item-Zahlen in dieser Antwort.
    return JSONResponse({"status": "ok", "service": "sharefyx-mcp", "version": __version__})


def create_app(
    *,
    settings: Settings,
    resolver: SpaceResolver,
    store: Store,
    allowed_hosts: list[str] | None = None,
) -> Starlette:
    """`allowed_hosts` ist optional und Standardmäßig `None` (FastMCPs eigener Default greift,
    d. h. `localhost`/`127.0.0.1`). Wird von `scripts/serve.py --allowed-host` durchgereicht —
    ohne diesen Schalter scheitert die Quick-Tunnel-Probe in Step 7 an FastMCPs
    DNS-Rebinding-Schutz, weil der Host hinter einem Tunnel nicht localhost ist.

    Fällt der explizite Parameter leer aus, greift `settings.allowed_hosts`
    (`SPACE_ALLOWED_HOSTS`, P3-C) — die systemd-Unit pflegt eine `Environment=`-Zeile, keine
    Argumentliste. Der explizite Parameter gewinnt, wenn gesetzt; danach die Settings; sonst
    FastMCPs eigener Default."""
    mcp = build_mcp(store, OwnSpaceWritable())
    mcp.add_middleware(ToolCallLogMiddleware())
    hosts = list(allowed_hosts) if allowed_hosts else (list(settings.allowed_hosts) or None)
    mcp_app = mcp.http_app(path="/", stateless_http=True, allowed_hosts=hosts)
    return Starlette(
        routes=[
            Route("/health", _health, methods=["GET"]),
            Mount("/mcp", app=TokenPathASGI(mcp_app, resolver=resolver)),
        ],
        # PFLICHT: ohne die durchgereichte Lifespan initialisiert FastMCPs
        # Streamable-HTTP-Session-Manager nie (Plan §4 Step 5).
        lifespan=mcp_app.lifespan,
    )
