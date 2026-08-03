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
ungetesteter, unaufgerufener Loader wäre totes Gewicht (Hard Rule 7); `static_dir` fehlt aus
demselben Grund (§1.3s Modulkarte nennt es als Teil der finalen Form, nicht als Step-3-Bedarf).
"""
from __future__ import annotations

from dataclasses import dataclass

COOKIE_NAME = "__Host-sfx_session"
IDLE_TTL_S = 12 * 3600  # P5-E
ABSOLUTE_TTL_S = 7 * 24 * 3600  # P5-E


@dataclass(frozen=True, kw_only=True)
class UiSettings:
    base_url: str
    idle_ttl_s: int = IDLE_TTL_S
    absolute_ttl_s: int = ABSOLUTE_TTL_S
    hsts: bool = True
