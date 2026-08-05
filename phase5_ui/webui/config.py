"""`UiSettings` — Cookie-Name, Session-TTLs (Plan §2.7, P5-E). Getrennt von
`authserver.config.AuthSettings`: die UI braucht keine Redirect-Origins und kein
`form-action`-Ziel für Claude — eine gemeinsame Settings-Klasse würde beide Seiten unnötig
koppeln.

`idle_ttl_s`/`absolute_ttl_s` sind hier bewusst KEINE Umgebungsvariablen (anders als
`AuthSettings.access_ttl_s`): P5-E legt 12 h/7 d fest, ohne einen Live-Testbedarf wie
`SPACE_OAUTH_ACCESS_TTL_S` in P4 zu nennen — ein ungenutzter Konfigurationshaken ist eine
Fläche mehr, die falsch gesetzt werden kann.

Bewusst OHNE Env-Loader (anders als `authserver.config.load_auth_settings()`): dieser Step
verdrahtet `UiSettings` nirgends gegen `scripts/serve.py`/echte Umgebungsvariablen — das
entscheidet sich erst in Step 5/6, wenn `/ui` real in den Prozess gemountet wird. Ein
ungetesteter, unaufgerufener Loader wäre totes Gewicht (Hard Rule 7).

`static_dir` (Step 6, `webui/static_routes.py`): Default `Path(__file__).resolve().parent /
"static"` — das ist immer `phase5_ui/webui/static/`, unabhängig vom aktuellen Arbeitsverzeichnis
des Prozesses (systemd startet nicht notwendig aus dem Repo-Root). Keine Umgebungsvariable aus
demselben Grund wie `idle_ttl_s`/`absolute_ttl_s` oben: kein Live-Testbedarf, der einen zweiten
Wert je bräuchte.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

COOKIE_NAME = "__Host-sfx_session"
IDLE_TTL_S = 12 * 3600  # P5-E
ABSOLUTE_TTL_S = 7 * 24 * 3600  # P5-E
DEFAULT_STATIC_DIR = Path(__file__).resolve().parent / "static"


@dataclass(frozen=True, kw_only=True)
class UiSettings:
    base_url: str
    idle_ttl_s: int = IDLE_TTL_S
    absolute_ttl_s: int = ABSOLUTE_TTL_S
    hsts: bool = True
    static_dir: Path = field(default=DEFAULT_STATIC_DIR)
