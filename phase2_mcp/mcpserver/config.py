from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765
DEFAULT_LOG_LEVEL = "INFO"
LEGACY_UNTIL_OPEN = "open"


@dataclass(frozen=True, kw_only=True)
class Settings:
    data_root: Path
    host: str = DEFAULT_HOST
    port: int = DEFAULT_PORT
    log_level: str = DEFAULT_LOG_LEVEL
    allowed_hosts: tuple[str, ...] = ()
    # P9 Step A (2026-10-01): Übergangsfenster der alten Web-UI-Adresse, siehe
    # `webui.config.UiSettings.legacy_origin`. Beide oder keins.
    ui_legacy_origin: str | None = None
    ui_legacy_until: date | None = None


def _parse_allowed_hosts(raw: str | None) -> tuple[str, ...]:
    if not raw:
        return ()
    return tuple(host for host in (part.strip() for part in raw.split(",")) if host)


def _parse_legacy_window(
    origin_raw: str | None, until_raw: str | None
) -> tuple[str | None, date | None]:
    """Fail-closed: ein halb oder falsch gesetztes Fenster ist ein Startfehler, kein stiller
    Fallback. Die Origin wird als exakter String verglichen (`security.py`), deshalb hier dieselbe
    Form erzwingen, die ein Browser im `Origin`-Header schickt: `https://host[:port]`, nichts dahinter."""
    origin_raw = (origin_raw or "").strip()
    until_raw = (until_raw or "").strip()
    if not origin_raw and not until_raw:
        return None, None
    if not origin_raw or not until_raw:
        raise ValueError("SPACE_UI_LEGACY_ORIGIN und SPACE_UI_LEGACY_UNTIL nur gemeinsam setzen")
    parts = urlsplit(origin_raw)
    if parts.scheme != "https" or not parts.netloc or origin_raw != f"https://{parts.netloc}":
        raise ValueError(
            f"SPACE_UI_LEGACY_ORIGIN muss die Form https://host sein (ohne Pfad, ohne /), war: {origin_raw!r}"
        )
    # Nikinger-Entscheidung 2026-10-05: unbefristet, bis die neue Adresse aus jedem Netz belegt
    # erreichbar ist (Firmen-VPN). Nur dieses ausdrückliche Wort öffnet es, leer bleibt ein Fehler;
    # `date.max` lässt `UiSettings.legacy_writable()` unverändert.
    if until_raw == LEGACY_UNTIL_OPEN:
        return origin_raw, date.max
    try:
        until = date.fromisoformat(until_raw)
    except ValueError as exc:
        raise ValueError(
            f"SPACE_UI_LEGACY_UNTIL muss JJJJ-MM-TT oder {LEGACY_UNTIL_OPEN!r} sein, war: {until_raw!r}"
        ) from exc
    return origin_raw, until


def load_settings(env: Mapping[str, str] | None = None) -> Settings:
    """Liest Settings aus Umgebungsvariablen. Kein Secret hier — Tokens leben im Keyring."""
    source = env if env is not None else os.environ

    data_root = source.get("SPACE_DATA_ROOT")
    if not data_root:
        raise ValueError("SPACE_DATA_ROOT ist Pflicht (kein Default auf den echten Pfad)")

    port_raw = source.get("SPACE_PORT")
    if port_raw is None:
        port = DEFAULT_PORT
    else:
        try:
            port = int(port_raw)
        except ValueError as exc:
            raise ValueError(f"SPACE_PORT muss eine Ganzzahl sein, war: {port_raw!r}") from exc

    legacy_origin, legacy_until = _parse_legacy_window(
        source.get("SPACE_UI_LEGACY_ORIGIN"), source.get("SPACE_UI_LEGACY_UNTIL")
    )

    return Settings(
        data_root=Path(data_root),
        host=source.get("SPACE_HOST", DEFAULT_HOST),
        port=port,
        log_level=source.get("SPACE_LOG_LEVEL", DEFAULT_LOG_LEVEL),
        allowed_hosts=_parse_allowed_hosts(source.get("SPACE_ALLOWED_HOSTS")),
        ui_legacy_origin=legacy_origin,
        ui_legacy_until=legacy_until,
    )
