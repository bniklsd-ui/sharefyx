"""`create_app()` — Starlette-Wurzel-App: `/health` (unauthentifiziert) + `Mount("/mcp")` mit
`BearerAuthASGI` davor (Plan §1.1, §4 Step 5, §3.3). Kennt alles (`config`, `auth`,
`permissions`, `server`, `asgi`) — das ist die einzige Stelle, die alle Seams zusammensteckt.

**`OwnSpaceWritable()` wird hier instanziiert, nicht injiziert** (Plan §2.2 Erweiterungspfad):
eine spätere `PolicyPermissions` mit echten Lese-Regeln zwischen Spaces ist damit ein
Konstruktor-Austausch an dieser einen Stelle, kein Umbau von `tools.py`/`server.py`.

**Schnitt, 2026-07-30 (Runbook-Schritt 8):** `oauth: OAuthConfig` ist jetzt **Pflicht**, nicht
mehr optional — `TokenPathASGI`/`AuthModeASGI` (P4 Step 6a) und damit der `oauth=None`-Pfad
(P3-Verhalten) sind entfernt, beide Pfad-Token live widerrufen. Der `resolver`-Parameter
(`SpaceResolver`, P2-D) entfällt ersatzlos aus dieser Funktion — er diente ausschließlich dem
Bau von `TokenPathASGI`.

**[2026-08-02 Korrektur, P5 Step 0 A]:** `issue_token.py`/`export_space_map.py`/
`KeyringTokenResolver` sind inzwischen ebenfalls entfernt (`docs/concepts/
PHASE4_CLOSEOUT_HANDOVER.md` §4.5) — `mcpserver/auth.py :: SpaceResolver` bleibt nur noch als
Protokoll stehen, `create_app()` brauchte es ohnehin schon seit dem Schnitt nicht mehr.
"""
from __future__ import annotations

import time
from dataclasses import dataclass

from authserver.config import AuthSettings
from authserver.resolver import OAuthTokenResolver
from authserver.routes import oauth_routes
from authserver.store import AuthStore
from authserver.userdir import UserDirectory
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Mount, Route

from storage.store import Store

from . import __version__
from .asgi import BearerAuthASGI
from .config import Settings
from .permissions import OwnSpaceWritable
from .request_log import ToolCallLogMiddleware
from .server import build_mcp


@dataclass(frozen=True, kw_only=True)
class OAuthConfig:
    """Bündelt, was `oauth_routes()` und die Bearer-Auflösung brauchen, in EINEM Parameter
    (Plan §3.3) statt drei einzelnen."""

    settings: AuthSettings
    store: AuthStore
    users: UserDirectory


def _bearer_challenge(auth_settings: AuthSettings) -> str:
    """Einmal gebaut, nicht pro Request (Plan §3.1)."""
    resource_metadata = f"{auth_settings.base_url}/.well-known/oauth-protected-resource/mcp"
    return (
        'Bearer error="invalid_token", error_description="Authentication required", '
        f'resource_metadata="{resource_metadata}", scope="space"'
    )


async def _health(request: Request) -> JSONResponse:
    # Unauthentifiziert (Plan §4 Step 5, P3-I) — deshalb bewusst keine Space-Namen, keine Pfade,
    # keine Item-Zahlen in dieser Antwort. `uptime_s` (P3-I, einziges neues Feld in P3) erlaubt
    # dem Disconnected-Runbook (Step 6), von außen "Dienst läuft durch" von "Dienst ist gerade
    # neu gestartet" zu unterscheiden, ohne SSH.
    uptime_s = int(time.monotonic() - request.app.state.start_time)
    return JSONResponse(
        {
            "status": "ok",
            "service": "sharefyx-mcp",
            "version": __version__,
            "uptime_s": uptime_s,
        }
    )


def create_app(
    *,
    settings: Settings,
    store: Store,
    oauth: OAuthConfig,
    allowed_hosts: list[str] | None = None,
) -> Starlette:
    """`allowed_hosts` ist optional und Standardmäßig `None` (FastMCPs eigener Default greift,
    d. h. `localhost`/`127.0.0.1`). Wird von `scripts/serve.py --allowed-host` durchgereicht —
    ohne diesen Schalter scheitert die Quick-Tunnel-Probe in Step 7 an FastMCPs
    DNS-Rebinding-Schutz, weil der Host hinter einem Tunnel nicht localhost ist.

    Fällt der explizite Parameter leer aus, greift `settings.allowed_hosts`
    (`SPACE_ALLOWED_HOSTS`, P3-C) — die systemd-Unit pflegt eine `Environment=`-Zeile, keine
    Argumentliste. Der explizite Parameter gewinnt, wenn gesetzt; danach die Settings; sonst
    FastMCPs eigener Default.

    `Mount("/mcp")` bekommt `BearerAuthASGI` direkt, `oauth_routes()` wird der Routenliste
    vorangestellt (Plan §3.3), und die Wurzel-App bekommt `TrustedHostMiddleware` mit denselben
    `allowed_hosts` wie die FastMCP-App (P4-P) — sie trägt öffentliche Auth-Routen. Nur gesetzt,
    wenn `hosts` nicht `None` ist: sonst würde ein Betrieb ohne `SPACE_ALLOWED_HOSTS`
    (Discovery über den Tailscale-Funnel-Hostnamen) durch die Middleware selbst blockiert."""
    mcp = build_mcp(store, OwnSpaceWritable())
    mcp.add_middleware(ToolCallLogMiddleware())
    hosts = list(allowed_hosts) if allowed_hosts else (list(settings.allowed_hosts) or None)
    mcp_app = mcp.http_app(path="/", stateless_http=True, allowed_hosts=hosts)

    oauth_resolver = OAuthTokenResolver(oauth.store, expected_resource=oauth.settings.resource)
    bearer = BearerAuthASGI(
        mcp_app, resolver=oauth_resolver, challenge=_bearer_challenge(oauth.settings)
    )

    routes: list[Route | Mount] = list(oauth_routes(oauth.settings, oauth.store, oauth.users))
    middleware: list[Middleware] = []
    if hosts is not None:
        middleware.append(Middleware(TrustedHostMiddleware, allowed_hosts=hosts))

    routes.append(Route("/health", _health, methods=["GET"]))
    routes.append(Mount("/mcp", app=bearer))

    app = Starlette(
        routes=routes,
        middleware=middleware,
        # PFLICHT: ohne die durchgereichte Lifespan initialisiert FastMCPs
        # Streamable-HTTP-Session-Manager nie (Plan §4 Step 5).
        lifespan=mcp_app.lifespan,
    )
    # Pro App-Instanz, nicht Modulebene — sonst würden mehrere `create_app()`-Aufrufe (z. B. in
    # Tests) sich einen Startzeitpunkt teilen.
    app.state.start_time = time.monotonic()
    return app
