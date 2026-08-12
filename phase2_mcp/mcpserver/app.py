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

**[2026-08-03, P5 Step 4 Nachtrag — `/ui/*` vorgezogen verdrahtet, WAS/WO/WARUM:**

*WAS:* `webui.routes_auth :: ui_auth_routes()` und `webui.account :: account_routes()` (beide
seit P5 Step 3/4 fertig und getestet, aber bis hierhin nie in den echten Prozess gemountet)
hängen jetzt in der Routenliste, direkt hinter `oauth_routes()` und vor `/health`/`Mount("/mcp")`
— exakt die Reihenfolge, die Plan §1.5s Route-Landkarte für das dortige `webui_routes(...)`
vorzeichnet. Keine neuen Parameter an `create_app()`: `UiSettings`/`SessionManager` werden hier
intern aus dem bereits vorhandenen `oauth`-Bündel gebaut (`oauth.settings.base_url`,
`oauth.store`, `oauth.users`) — dieselbe `AuthStore`/`UserDirectory`-Instanz, die auch die
OAuth-Seite bedient, kein zweiter DB-Handle.

*WARUM JETZT, nicht erst in Step 5 wie geplant:* Block A live-abzunehmen (Plan §6, Zeilen 1–9)
verlangt einen echten Browser gegen `/ui/login`/`/ui/invite/{token}` — die gab es im laufenden
Dienst schlicht nicht, `create_app()` kannte bis zu diesem Nachtrag nur `oauth_routes()` und
`Mount("/mcp")`. Live-Fund des Nikingers: `invite`-Link → `404`. Plan §5 Step 5 listet die
Verdrahtung offiziell erst dort auf ("Verdrahtung in `mcpserver/app.py`
(`webui_routes(...)` in die Routenliste, vor `Mount("/mcp")`)") — aber Step 5 selbst ist laut
Plan **hinter** dem Block-A-Gate verriegelt, der wiederum genau diese Route braucht. Ein Zirkel
im Plan-Text, keine Interpretationsfrage. Dem Nikinger vorgelegt, Entscheidung: die minimale
Verdrahtung jetzt vorziehen (nur `ui_auth_routes()`+`account_routes()`, **nicht** `webui/api.py`
— das existiert noch gar nicht, ist echter Step-5-Scope), damit der Gate überhaupt durchführbar
wird.

*WARUM DAS EINEN GELOCKTEN PLAN-WIDERSPRUCH AUFLÖST, NICHT NUR EINE LÜCKE FÜLLT:* Plan §1.2s
Paketgrenzen-Tabelle verbietet `mcpserver` ausdrücklich den Import von `webui`
("`mcpserver` … darf **nicht** importieren: `webui`"), aber §1.5s eigene Route-Landkarte zeigt
`create_app()` beim Aufruf von `webui_routes(...)` — genau das. Beide Stellen stehen im selben
📕-Plandokument, das Nikinger-Entscheidungen P5-A–P5-AE trägt; §1.2 ist keine der benannten,
einzeln gelockten Entscheidungen, sondern eine Ableitungstabelle, die mit der ebenso im Plan
stehenden Architektur nicht zusammenpasst. **Nicht** stillschweigend nach einer Seite
aufgelöst — dem Nikinger vorgelegt (`phase5_ui/CLAUDE.md`-Nachtrag unten trägt die
Entscheidung), hier nur die Umsetzung.

*WARUM DAS KEINEN Zirkelimport ERZEUGT* (das eigentliche Risiko hinter dem §1.2-Verbot):
`webui` importiert heute noch **nichts** aus `mcpserver` — das eine erlaubte Symbol
(`permissions.OwnSpaceWritable`, P5-B) ist erst für `webui/api.py` in Step 5 vorgesehen, diese
Datei existiert noch nicht. `mcpserver/permissions.py` selbst importiert nur `collections.abc`/
`typing` — kein Pfad zurück zu `mcpserver.app` oder zu `webui`. Selbst wenn Step 5 `webui/api.py`
baut und von dort `mcpserver.permissions` importiert, bleibt der Graph azyklisch: Python lädt
`mcpserver.permissions` als eigenständiges Submodul, unabhängig davon, dass `mcpserver.app`
(der ursprüngliche Importeinstieg) noch nicht fertig geladen ist — ein Zyklus entstünde nur,
wenn `mcpserver.permissions` selbst wieder `mcpserver.app` oder `webui` importierte, was es
nicht tut. Test `test_create_app_mounts_ui_routes_without_import_cycle`
(`phase2_mcp/tests/test_app.py`) hält diese Prämisse fest, nicht nur behauptet.

**[2026-08-05, P5 Step 5]:** `webui/api.py` existiert jetzt (der Absatz oben sprach noch von
„diese Datei existiert noch nicht" — das ist damit überholt) und ist als `api_routes(ui_settings,
store, ui_sessions, own_space_writable)` in die Routenliste gemountet, hinter `account_routes()`
und vor `/health`/`Mount("/mcp")`. `store: Store` bediente bis hierhin ausschließlich
`build_mcp()`; dieselbe Instanz läuft jetzt zusätzlich durch die REST-API, kein zweiter
`Store`-Handle. `OwnSpaceWritable()` wird jetzt in einer lokalen Variablen gehalten
(`own_space_writable`) statt zweimal instanziiert — beide Verwendungsstellen teilen sich dieselbe
(zustandslose) Instanz. Die Zirkelfreiheit von oben gilt unverändert: der zusätzliche Import ist
exakt der eine vorhergesagte (`mcpserver.permissions.OwnSpaceWritable`), kein zweites Symbol.

**[2026-08-05, P5 Step 6]:** `webui/static_routes.py` existiert jetzt (`GET /ui/` — die echte
App-Shell, sitzungsgated — und `GET /ui/static/{path}`) und ist als `static_routes(ui_settings,
ui_sessions)` gemountet, direkt hinter `ui_auth_routes()` (beide sind `/ui/*`-Belange) und vor
`account_routes()`/`api_routes()`. Kein neuer `create_app()`-Parameter — `static_routes()`
braucht nur, was hier ohnehin schon für `ui_auth_routes()` gebaut wird.

**[2026-08-09, P6 Step 3]:** `api_routes()` bekommt hier ein fünftes Argument, `oauth.store`
(`AuthStore`) — Update-Log-Banner (Plan §1.8) braucht `users.seen_update_id` (Schema 3), das
lebt in derselben `AuthStore`-Instanz, die `account_routes()`/`ui_auth_routes()` schon bekommen,
kein zweiter DB-Handle. **Dokumentierte Ein-Zeilen-Abweichung** von Step 3s Plan-Dateiliste (die
nur `webui/api.py` nennt, nicht diese Datei) — Begründung im Moduldocstring von `webui/api.py`,
gleiche Kategorie wie P6 Step 1/2s dokumentierte Abweichungen dort.

**[2026-08-12, P6 Step 5]:** `OwnSpaceWritable()` ist entfernt. `SharePolicy(store.acl_reader)`
tritt an ihre Stelle (Variable heißt jetzt `permissions`, nicht mehr `own_space_writable`) —
die frühere Begründung oben ("ein Konstruktor-Austausch an dieser einen Stelle, kein Umbau von
`tools.py`/`server.py`") war die Vorhersage für genau diesen Schnitt und hat gehalten:
`build_mcp()`/`api_routes()` bekommen weiterhin nur ein `Permissions`-Objekt durchgereicht,
keine Signaturänderung. `store.acl_reader` (neu, `storage/store.py`) gibt denselben
`AclReader` zurück, den `Store.__init__` schon für `list_spaces()`/`acl_of()` baut — ein
Handle, kein zweiter, siehe `permissions.py`s Moduldocstring.
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
from webui.account import account_routes
from webui.api import api_routes
from webui.config import UiSettings
from webui.routes_auth import ui_auth_routes
from webui.sessions import SessionManager
from webui.static_routes import static_routes

from . import __version__
from .asgi import BearerAuthASGI
from .config import Settings
from .permissions import SharePolicy
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
    # P6 Step 5: `SharePolicy` statt `OwnSpaceWritable` — gebaut aus `store.acl_reader`, damit
    # `Store` und die Rechteprüfung sich denselben `AclReader`-Cache teilen (ein Handle, kein
    # zweiter, siehe `permissions.py`s Moduldocstring).
    permissions = SharePolicy(store.acl_reader)
    mcp = build_mcp(store, permissions)
    mcp.add_middleware(ToolCallLogMiddleware())
    hosts = list(allowed_hosts) if allowed_hosts else (list(settings.allowed_hosts) or None)
    mcp_app = mcp.http_app(path="/", stateless_http=True, allowed_hosts=hosts)

    oauth_resolver = OAuthTokenResolver(oauth.store, expected_resource=oauth.settings.resource)
    bearer = BearerAuthASGI(
        mcp_app, resolver=oauth_resolver, challenge=_bearer_challenge(oauth.settings)
    )

    # `/ui/*` vorgezogen aus P5 Step 5 (siehe Moduldocstring oben, Nachtrag 2026-08-03) — kein
    # zweiter DB-Handle: `UiSettings`/`SessionManager` laufen über dieselbe `oauth.store`/
    # `oauth.users`-Instanz, die auch `oauth_routes()` bedient.
    ui_settings = UiSettings(base_url=oauth.settings.base_url)
    ui_sessions = SessionManager(oauth.store, settings=ui_settings)

    routes: list[Route | Mount] = list(oauth_routes(oauth.settings, oauth.store, oauth.users))
    routes += ui_auth_routes(ui_settings, oauth.store, oauth.users, ui_sessions)
    routes += static_routes(ui_settings, ui_sessions)
    routes += account_routes(ui_settings, oauth.store, oauth.users, ui_sessions)
    routes += api_routes(ui_settings, store, ui_sessions, permissions, oauth.store)
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
