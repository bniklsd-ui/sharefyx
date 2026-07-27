from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765
DEFAULT_LOG_LEVEL = "INFO"


@dataclass(frozen=True, kw_only=True)
class Settings:
    data_root: Path
    host: str = DEFAULT_HOST
    port: int = DEFAULT_PORT
    log_level: str = DEFAULT_LOG_LEVEL
    allowed_hosts: tuple[str, ...] = ()


def _parse_allowed_hosts(raw: str | None) -> tuple[str, ...]:
    if not raw:
        return ()
    return tuple(host for host in (part.strip() for part in raw.split(",")) if host)


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

    return Settings(
        data_root=Path(data_root),
        host=source.get("SPACE_HOST", DEFAULT_HOST),
        port=port,
        log_level=source.get("SPACE_LOG_LEVEL", DEFAULT_LOG_LEVEL),
        allowed_hosts=_parse_allowed_hosts(source.get("SPACE_ALLOWED_HOSTS")),
    )
