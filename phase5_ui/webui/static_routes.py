"""`GET /ui/` (App-Shell) und `GET /ui/static/{path}` (Plan §1.5, §5 Step 6). Getrennt von
`routes_auth.py`: das dort sind Auth-*Flüsse* (Login, Einladung), das hier ist reines
Dateiausliefern + ein Sitzungs-Gate — zwei verschiedene Verantwortlichkeiten, ein gemeinsames
Modul hätte beide unnötig gekoppelt.

**`GET /ui/` verlangt eine gültige Sitzung — Korrektur zu Plan §1.5s Routentabelle**, die dort
"keine" einträgt. Der im selben Plan-Abschnitt (§5 Step 6) verlangte Testname
`test_index_route_requires_session` widerspricht der Tabellenzelle direkt; aufgelöst zugunsten
des spezifischeren Testnamens, nicht der Tabelle (dieselbe Kategorie Plan-Selbstwiderspruch wie
der `mcpserver→webui`-Zirkel aus P5 Step 4, dort ebenfalls zugunsten des konkreteren Textes
aufgelöst). Datierte Korrekturnotiz: `phase5_ui/CLAUDE.md`, Session-Block 2026-08-05.

**Cache-Header-Regel (Plan §3.4: "`no-store` außer für `/ui/static` mit gehashtem Namen"):**
`_HASHED_NAME_RE` erkennt einen Kurzhash unmittelbar vor der Dateiendung
(`InterVariable-subset.<hash8>.woff2`, erzeugt von `scripts/build_font_subset.sh`) — nur solche
Dateien bekommen `immutable`. `app.html`/`app.css`/`app.js` tragen bewusst KEINEN Hash (kein
Build-Step, P5-T — sie werden von Hand editiert, ein `immutable`-Cache auf einem unveränderten
Dateinamen wäre nach der nächsten Änderung ein tagelang stiller Bug) und bekommen deshalb das
Standard-`no-store` aus `ui_security_headers()`.
"""
from __future__ import annotations

import re
from pathlib import Path

from starlette.requests import Request
from starlette.responses import RedirectResponse, Response
from starlette.routing import Route

from .config import UiSettings
from .security import ui_security_headers
from .sessions import SessionManager

_CONTENT_TYPES: dict[str, str] = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".woff2": "font/woff2",
    ".txt": "text/plain; charset=utf-8",
}
_DEFAULT_CONTENT_TYPE = "application/octet-stream"

# Matcht "<name>.<hash>.<ext>" oder "<name>-<hash>.<ext>" mit mindestens 8 Hex-Ziffern
# unmittelbar vor der Endung — `build_font_subset.sh` erzeugt z. B.
# "InterVariable-subset.2fa9d1dc.woff2" (Punkt-getrennt).
_HASHED_NAME_RE = re.compile(r"[.-][0-9a-f]{8,}\.[A-Za-z0-9]+$")

_IMMUTABLE_CACHE = "public, max-age=31536000, immutable"


def _content_type(path: Path) -> str:
    return _CONTENT_TYPES.get(path.suffix.lower(), _DEFAULT_CONTENT_TYPE)


def _resolve_static_path(static_dir: Path, requested: str) -> Path | None:
    """`None`, wenn der Pfad nicht existiert, keine Datei ist, oder außerhalb von `static_dir`
    landet (Pfad-Traversal — `..`-Segmente oder ein führender `/`, der `Path.__truediv__` dazu
    bringen würde, `static_dir` zu verwerfen und absolut zu werden)."""
    if requested.startswith("/") or ".." in Path(requested).parts:
        return None
    candidate = (static_dir / requested).resolve()
    base = static_dir.resolve()
    try:
        candidate.relative_to(base)
    except ValueError:
        return None
    if not candidate.is_file():
        return None
    return candidate


def static_routes(settings: UiSettings, sessions: SessionManager) -> list[Route]:
    async def _index(request: Request) -> Response:
        headers = ui_security_headers(settings)
        session = sessions.load(request)
        if session is None:
            return RedirectResponse("/ui/login", status_code=303, headers=headers)
        app_html = settings.static_dir / "app.html"
        return Response(app_html.read_bytes(), media_type=_content_type(app_html), headers=headers)

    async def _static(request: Request) -> Response:
        headers = ui_security_headers(settings)
        requested = request.path_params["path"]
        found = _resolve_static_path(settings.static_dir, requested)
        if found is None:
            return Response("Nicht gefunden.", status_code=404, media_type="text/plain", headers=headers)
        if _HASHED_NAME_RE.search(found.name):
            headers["Cache-Control"] = _IMMUTABLE_CACHE
        return Response(found.read_bytes(), media_type=_content_type(found), headers=headers)

    return [
        Route("/ui/", _index, methods=["GET"]),
        Route("/ui/static/{path:path}", _static, methods=["GET"]),
    ]
