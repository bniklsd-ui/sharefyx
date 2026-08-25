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

`update_log_path` (P6 Step 3, `webui/updates.py`): Default `.../phase5_ui/webui/config.py`s
Großeltern-Verzeichnis `/ docs / UPDATE_LOG.md` — bei einem `deploy.sh`-Release ist das
`$release/docs/UPDATE_LOG.md`, derselbe Checkout, den `deploy.sh`s eigenes Gate liest, nie die
Arbeitskopie eines anderen Prozesses. Gleiches Feld-statt-Konstante-Muster wie `static_dir`:
Tests injizieren einen `tmp_path`-Pfad, kein Live-Testbedarf für eine echte Env-Var.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

COOKIE_NAME = "__Host-sfx_session"
IDLE_TTL_S = 12 * 3600  # P5-E
ABSOLUTE_TTL_S = 7 * 24 * 3600  # P5-E
DEFAULT_STATIC_DIR = Path(__file__).resolve().parent / "static"
DEFAULT_UPDATE_LOG_PATH = Path(__file__).resolve().parents[2] / "docs" / "UPDATE_LOG.md"


@dataclass(frozen=True, kw_only=True)
class UiSettings:
    base_url: str
    idle_ttl_s: int = IDLE_TTL_S
    absolute_ttl_s: int = ABSOLUTE_TTL_S
    hsts: bool = True
    static_dir: Path = field(default=DEFAULT_STATIC_DIR)
    update_log_path: Path = field(default=DEFAULT_UPDATE_LOG_PATH)
    # Kill-Switch für die Space-Verwaltung (P7 Step C3, P7-R) — war bis Phase 7 ein Seam ohne
    # Implementierung (Step 7 Commit 6, P6-Plan). Jetzt scharf: `False` lässt alle fünf
    # `/api/v1/spaces*`-Routen `404` antworten und blendet den Menüpunkt in `app.html` aus.
    # Default `True`, weil die Fläche jetzt live gebaut ist — kein Grund mehr, sie ausgeliefert
    # aber abgeschaltet zu lassen.
    space_admin_enabled: bool = True
