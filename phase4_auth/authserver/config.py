from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

DEFAULT_MODE = "oauth"
DEFAULT_ALLOWED_REDIRECT_ORIGINS: tuple[str, ...] = ("https://claude.ai", "https://claude.com")
DEFAULT_ACCESS_TTL_S = 3600
DEFAULT_REFRESH_TTL_S = 2592000
DEFAULT_CODE_TTL_S = 60
DEFAULT_REQUEST_TTL_S = 600

_VALID_MODES = ("token", "both", "oauth")


@dataclass(frozen=True, kw_only=True)
class AuthSettings:
    base_url: str
    db_path: Path
    mode: str = DEFAULT_MODE
    allowed_redirect_origins: tuple[str, ...] = DEFAULT_ALLOWED_REDIRECT_ORIGINS
    access_ttl_s: int = DEFAULT_ACCESS_TTL_S
    refresh_ttl_s: int = DEFAULT_REFRESH_TTL_S
    code_ttl_s: int = DEFAULT_CODE_TTL_S
    request_ttl_s: int = DEFAULT_REQUEST_TTL_S
    hsts: bool = True

    @property
    def issuer(self) -> str:
        return self.base_url

    @property
    def resource(self) -> str:
        return f"{self.base_url}/mcp"

    @property
    def csp_form_action(self) -> str:
        """`form-action`-Direktivenwert für `routes.py :: _security_headers()` — hier statt
        dort gebaut, damit `allowed_redirect_origins` außerhalb von `config.py`/`clients.py`
        weiterhin nicht auftaucht (`test_redirect_uri_allowed_is_the_only_matching_path`, Plan
        §2.6 [SEAM]). Kein Widerspruch zu diesem Seam: hier wird nichts gegen eine Redirect-URI
        verglichen, die Liste wird nur in einen Header-Wert übersetzt — trotzdem an der Stelle
        gebaut, an der `allowed_redirect_origins` schon lesbar ist, statt eine zweite Stelle zu
        öffnen."""
        return " ".join(("'self'", *self.allowed_redirect_origins))


def _parse_redirect_origins(raw: str | None) -> tuple[str, ...]:
    if not raw:
        return DEFAULT_ALLOWED_REDIRECT_ORIGINS
    return tuple(origin for origin in (part.strip() for part in raw.split(",")) if origin)


def _parse_int(raw: str | None, *, default: int, var_name: str) -> int:
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError as exc:
        raise ValueError(f"{var_name} muss eine Ganzzahl sein, war: {raw!r}") from exc


def _parse_bool(raw: str | None, *, default: bool) -> bool:
    if raw is None:
        return default
    return raw.strip().lower() not in ("off", "false", "0", "")


def _validate_base_url(base_url: str) -> None:
    if not base_url.startswith("https://"):
        raise ValueError(f"SPACE_PUBLIC_BASE_URL muss mit https:// beginnen, war: {base_url!r}")
    if base_url.endswith("/"):
        raise ValueError("SPACE_PUBLIC_BASE_URL darf nicht mit / enden")
    if "?" in base_url or "#" in base_url:
        raise ValueError("SPACE_PUBLIC_BASE_URL darf keine Query/Fragment enthalten")


def resolve_db_path(source: Mapping[str, str]) -> Path:
    """`SPACE_AUTH_DB` zuerst, sonst `STATE_DIRECTORY`/`auth.sqlite3` — kein stiller Fallback
    ins Arbeitsverzeichnis. Ausgelagert aus `load_auth_settings()` (P4 Step 7): `authctl.py`
    braucht nur den DB-Pfad, nicht `SPACE_AUTH_MODE`/`SPACE_PUBLIC_BASE_URL` — ein Operator-
    Werkzeug, das für „eine Familie widerrufen" plötzlich eine öffentliche Basis-URL verlangt,
    wäre eine unnötige Hürde für eine SSH-Sitzung (`ratelimit.py`-Docstring: „eine SSH-Sitzung
    entfernt")."""
    db_path_raw = source.get("SPACE_AUTH_DB")
    if db_path_raw:
        return Path(db_path_raw)
    state_dir = source.get("STATE_DIRECTORY")
    if not state_dir:
        raise ValueError(
            "SPACE_AUTH_DB fehlt und STATE_DIRECTORY ist nicht gesetzt — kein stiller "
            "Fallback ins Arbeitsverzeichnis"
        )
    return Path(state_dir) / "auth.sqlite3"


def load_auth_settings(env: Mapping[str, str] | None = None) -> AuthSettings:
    """Liest AuthSettings aus Umgebungsvariablen. Kein Secret hier — Passwort-/TOTP-Nutzerakten
    kommen über `users.py` aus systemd-Credential/Keyring, nicht aus dieser Funktion.
    """
    source = env if env is not None else os.environ

    mode = source.get("SPACE_AUTH_MODE", DEFAULT_MODE)
    if mode not in _VALID_MODES:
        raise ValueError(f"SPACE_AUTH_MODE muss einer von {_VALID_MODES} sein, war: {mode!r}")

    base_url = source.get("SPACE_PUBLIC_BASE_URL")
    if mode in ("oauth", "both"):
        if not base_url:
            raise ValueError("SPACE_PUBLIC_BASE_URL ist Pflicht bei SPACE_AUTH_MODE=oauth|both")
        _validate_base_url(base_url)
    else:
        base_url = base_url or ""

    db_path = resolve_db_path(source)

    return AuthSettings(
        base_url=base_url,
        db_path=db_path,
        mode=mode,
        allowed_redirect_origins=_parse_redirect_origins(
            source.get("SPACE_OAUTH_ALLOWED_REDIRECT_ORIGINS")
        ),
        access_ttl_s=_parse_int(
            source.get("SPACE_OAUTH_ACCESS_TTL_S"),
            default=DEFAULT_ACCESS_TTL_S,
            var_name="SPACE_OAUTH_ACCESS_TTL_S",
        ),
        refresh_ttl_s=_parse_int(
            source.get("SPACE_OAUTH_REFRESH_TTL_S"),
            default=DEFAULT_REFRESH_TTL_S,
            var_name="SPACE_OAUTH_REFRESH_TTL_S",
        ),
        code_ttl_s=_parse_int(
            source.get("SPACE_OAUTH_CODE_TTL_S"),
            default=DEFAULT_CODE_TTL_S,
            var_name="SPACE_OAUTH_CODE_TTL_S",
        ),
        request_ttl_s=_parse_int(
            source.get("SPACE_OAUTH_REQUEST_TTL_S"),
            default=DEFAULT_REQUEST_TTL_S,
            var_name="SPACE_OAUTH_REQUEST_TTL_S",
        ),
        hsts=_parse_bool(source.get("SPACE_OAUTH_HSTS"), default=True),
    )
