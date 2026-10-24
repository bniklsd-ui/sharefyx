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

**[2026-10-22, P10.5 Block 6, Schritt 6.3]:** `/mcp` wird jetzt **ohne** Slash exakt bedient
(`Route("/mcp", ...)` vor `Mount("/mcp", ...)`) - vorher schickte Starlette jeden Request auf
`/mcp` mit 307 auf `/mcp/` (P10-C nennt die Abnahme-URL ohne Slash, und ein Client, der der
Umleitung nicht folgt, scheitert). Die Klasse `_ExactMcpMount` baut dafuer genau den Scope, den
Starlettes `Mount` baut - die innere FastMCP-App sieht dieselbe Route wie zuvor.
"""
from __future__ import annotations

import contextlib
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
from starlette.responses import JSONResponse, Response
from starlette.routing import Mount, Route

from storage.store import Store
from webui.account import account_routes
from webui.api import api_routes
from webui.config import UiSettings
from webui.events import ChangeFeed
from webui.pages import render_not_found_page
from webui.routes_auth import ui_auth_routes
from webui.security import ui_security_headers
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


class _ExactMcpMount:
    """`/mcp` **ohne** Slash - exakt bedient, ohne 307 (P10.5 Block 6, Schritt 6.3).

    Starlettes Router schickt einen Request auf `/mcp` mit **307** auf `/mcp/`, wenn keine Route
    exakt passt (`redirect_slashes`). `Mount("/mcp")` deckt nur `/mcp/...` ab, also war `/mcp`
    bisher eine Umleitung - und ein Client, der ihr nicht folgt (etwa `httpx` mit
    `follow_redirects=False`), scheitert. Die Abnahme-URL aus P10-C steht **ohne** Slash.

    **[VERIFY, 2026-10-22]** gegen das, was `Mount` in der installierten Starlette-Version
    (1.9.0) in den `scope` schreibt: `Mount.matches()` setzt `root_path` auf
    `root_path + matched_path` (hier `/mcp`), laesst `path` aber auf `/mcp/` stehen - die innere
    App rechnet `path` minus `root_path` (`get_route_path()`) und sieht so die Route `/`.
    Diese Klasse stellt **denselben** Scope her, mit `path = "/"`: `get_route_path()` liefert
    dann ebenfalls `/`, die innere FastMCP-App sieht also exakt dieselbe Route wie beim Mount.
    `raw_path` bleibt unveraendert (der echte Requestpfad), `app_root_path` wie beim Mount.
    """

    def __init__(self, app) -> None:
        self._app = app

    async def __call__(self, scope, receive, send) -> None:
        scope = dict(
            scope,
            path="/",
            root_path=scope.get("root_path", "") + "/mcp",
            app_root_path=scope.get("app_root_path", scope.get("root_path", "")),
        )
        await self._app(scope, receive, send)


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
    #
    # **P10.5, Block 2 (2026-10-22):** das Home-Space-Prädikat kommt dazu — nur die Auth-DB
    # weiß, ob ein Space einem Nutzer gehört (ein Team-Space gehört niemandem). `get_user()`
    # ist die **Zeilenabfrage ohne TOTP-Entschlüsselung** (`authserver/store.py :: get_user()`),
    # dieselbe Begründung wie in `webui/api.py :: _is_team_space()` (2026-10-08, Advisor-Fund):
    # ein Seed ist das schärfere Geheimnis (Hard Rule 1, Nachtrag 2026-07-30), und hier wird
    # nur gefragt „gibt es einen Nutzer mit diesem Space?".
    permissions = SharePolicy(
        store.acl_reader,
        is_home_space=lambda space: oauth.store.get_user(space) is not None,
    )
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
    ui_settings = UiSettings(
        base_url=oauth.settings.base_url,
        legacy_origin=settings.ui_legacy_origin,
        legacy_until=settings.ui_legacy_until,
    )
    ui_sessions = SessionManager(oauth.store, settings=ui_settings)

    routes: list[Route | Mount] = list(oauth_routes(oauth.settings, oauth.store, oauth.users))
    routes += ui_auth_routes(ui_settings, oauth.store, oauth.users, ui_sessions)
    routes += static_routes(ui_settings, ui_sessions)
    routes += account_routes(ui_settings, oauth.store, oauth.users, ui_sessions)
    # [2026-10-24, P10.5 Block 10, Schritt 10.2 -- LG-2, Lock P10.5-L] Der Ereignis-Feed der
    # App: EIN Feed je App (nicht je Route), er pollt den Git-HEAD des DATA_ROOT und meldet
    # die geaenderten Space-Namen. Die Quelle ist der HEAD, weil Hard Rule 5 aus jedem
    # erfolgreichen Write einen Commit macht -- Web, MCP und Hand-Edit gleichermassen, ohne
    # Eingriff in einen Schreibpfad.
    #
    # **Er wird hier gebaut, nicht in `api_routes()`** -- die App muss ihn beim Shutdown
    # schliessen (`await feed.aclose()`, Plan §Block 10, Schritt 10.2), und die Route kann das
    # nicht: sie kennt die App nicht.
    events = ChangeFeed(store.data_root)
    routes += api_routes(
        ui_settings, store, ui_sessions, permissions, oauth.store, oauth.users, events=events,
    )

    # [2026-10-23, P10.5 Block 7, Schritt 7.1 — UI-1] HTML-404 für unbekannte `/ui`-Pfade.
    #
    # **Die Position ist die halbe Aufgabe:** die Route hängt **nach** allen bekannten
    # `/ui`-Routen (`ui_auth_routes` = `/ui/login`, `/ui/logout`, `/ui/invite/{token}`,
    # `/ui/enroll/confirm`; `static_routes` = `/ui/`, `/ui/static/{path}`), sonst überdeckt
    # der Fänger bestehende Pfade. Starlette prüft die Routenliste **in Reihenfolge** — der
    # erste Treffer gewinnt, deshalb steht der Fänger hinten.
    #
    # **Was der Fänger nicht fasst:** `/ui/static/<fehlt>` bleibt Klartext (eigene Route
    # davor, `static_routes.py:86`), `/api/v1/...` und `/mcp` haben andere Präfixe und
    # antworten wie bisher (JSON bzw. das MCP-Protokoll). Der Präfix `/ui/` ist damit die
    # ganze Reichweite des Fängers — kein globales 404.
    async def _ui_not_found(request: Request) -> Response:
        return Response(
            render_not_found_page(),
            status_code=404,
            media_type="text/html",
            headers=ui_security_headers(ui_settings),
        )

    routes.append(Route("/ui/{rest:path}", _ui_not_found, methods=["GET"]))

    middleware: list[Middleware] = []
    if hosts is not None:
        middleware.append(Middleware(TrustedHostMiddleware, allowed_hosts=hosts))

    routes.append(Route("/health", _health, methods=["GET"]))
    # [2026-10-22, P10.5 Block 6, Schritt 6.3] `/mcp` **ohne** Slash: die exakte Route kommt
    # **vor** dem Mount, sonst schickt Starlette den Request mit 307 auf `/mcp/`. Beide Zeilen
    # bedienen dieselbe innere App (`_ExactMcpMount` baut denselben Scope, den der Mount baut).
    routes.append(Route("/mcp", endpoint=_ExactMcpMount(bearer), methods=["GET", "POST", "DELETE"]))
    routes.append(Mount("/mcp", app=bearer))

    # [2026-10-24, P10.5 Block 10, Schritt 10.2 -- LG-2] Die Lifespan wird **umhuellt**:
    # FastMCPs eigene bleibt unveraendert drin (sie ist PFLICHT -- ohne sie initialisiert der
    # Streamable-HTTP-Session-Manager nie, Plan §4 Step 5), danach wird der Ereignis-Feed
    # geschlossen. Ohne das bliebe der Poll-Task nach dem Shutdown haengen.
    @contextlib.asynccontextmanager
    async def lifespan(app):
        async with mcp_app.lifespan(app):
            yield
        await events.aclose()

    app = Starlette(
        routes=routes,
        middleware=middleware,
        lifespan=lifespan,
    )
    # Pro App-Instanz, nicht Modulebene — sonst würden mehrere `create_app()`-Aufrufe (z. B. in
    # Tests) sich einen Startzeitpunkt teilen.
    app.state.start_time = time.monotonic()
    # [P10-10-24, P10.5 Block 10, Schritt 10.2] Der Feed liegt auf `app.state`, damit ein
    # Test (und ein Diagnose-Weg) ihn erreichen kann — die App besitzt genau einen.
    app.state.events_feed = events
    return app
