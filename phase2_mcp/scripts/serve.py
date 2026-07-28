#!/usr/bin/env python3
"""CLI-Einstieg: liest `Settings`, baut `Store` + `KeyringTokenResolver`, startet uvicorn ohne
Access-Log (Plan §4 Step 5). Noch kein Tunnel (P3) — `--allowed-host` existiert schon, damit
Step 7s Quick-Tunnel-Probe nicht an FastMCPs DNS-Rebinding-Schutz scheitert.

**P4 Step 6b — `SPACE_AUTH_MODE`-Gate (Nikinger-Entscheidung 2026-07-28, vor dieser Session
gelockt, siehe `phase4_auth/CLAUDE.md`):** zwei unabhängige Weichen, nicht eine. Ob überhaupt ein
`OAuthConfig`-Bündel gebaut wird, entscheidet die **rohe Env-Var-Anwesenheit**
`"SPACE_AUTH_MODE" in os.environ` — nicht der bereits gedefaultete Rückgabewert von
`load_auth_settings()`. Fehlt sie: `oauth=None`, exakt der heutige P3-Pfad, kein `AuthSettings`-
Aufruf, keine neue Anforderung an einen lokalen Testlauf ohne jede Absicht, P4 zu prüfen. Ist sie
gesetzt (jeder der drei Werte `token`/`both`/`oauth`): `load_auth_settings()` läuft echt und
**ungefangen** — ein Konfigurationsfehler (z. B. fehlendes `SPACE_PUBLIC_BASE_URL`) stirbt laut,
kein `try/except`, das wäre ein stiller Fallback auf schwächere Auth genau dort, wo P4 das
verhindern soll. Welchen der drei Werte `SPACE_AUTH_MODE` trägt, entscheidet danach ausschließlich
`AuthModeASGI` (P4-N) über `load_auth_settings()`s eigene, längst vorhandene Validierung.
"""
from __future__ import annotations

import argparse
import os
from datetime import datetime, timezone

import uvicorn

from authserver.config import load_auth_settings
from authserver.store import AuthStore
from authserver.users import load_users

from storage.store import Store

from mcpserver.app import OAuthConfig, create_app
from mcpserver.auth import KeyringTokenResolver
from mcpserver.config import load_settings
from mcpserver.logging_setup import configure_logging
from mcpserver.request_log import AccessLogASGI, OAuthLogASGI


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Sharefyx MCP-Server (lokal, ohne Tunnel)")
    parser.add_argument(
        "--allowed-host",
        action="append",
        dest="allowed_hosts",
        default=None,
        metavar="HOST",
        help="Zusätzlicher erlaubter Host/Origin (mehrfach angebbar) — für den Tunnel-Betrieb "
        "ab P3/Step 7, hier schon verdrahtet.",
    )
    args = parser.parse_args(argv)

    settings = load_settings()
    configure_logging(settings.log_level)

    oauth: OAuthConfig | None = None
    if "SPACE_AUTH_MODE" in os.environ:
        auth_settings = load_auth_settings()
        auth_store = AuthStore(auth_settings.db_path, now_fn=lambda: datetime.now(timezone.utc))
        oauth = OAuthConfig(settings=auth_settings, store=auth_store, users=load_users())

    store = Store(settings.data_root)
    resolver = KeyringTokenResolver()
    app = create_app(
        settings=settings,
        resolver=resolver,
        store=store,
        allowed_hosts=args.allowed_hosts,
        oauth=oauth,
    )
    # AccessLogASGI/OAuthLogASGI hier und nicht in create_app() (Plan §3.3): test_app.py läuft
    # damit unverändert gegen die nackte App. OAuthLogASGI wird UNBEDINGT verdrahtet, nicht nur
    # wenn `oauth is not None` — ohne `/oauth/*`-Routen ist es ein reiner No-op (siehe dessen
    # Docstring: prüft `scope["path"]` selbst), und der Dev- (`oauth=None`) und der Prod-Pfad
    # bleiben damit strukturell gleich verdrahtet, statt einer dritten Fallunterscheidung hier.
    app = AccessLogASGI(OAuthLogASGI(app))

    # uvicorns eigenes access_log=False bleibt bestehen (Hard Rule, §8 Risiko 3 aus P2): dessen
    # Access-Log schreibt die komplette URL inklusive Token. AccessLogASGI ersetzt es durch die
    # token-redigierte, whitelist-begrenzte Variante aus request_log.py.
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        access_log=False,
        log_level=settings.log_level.lower(),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
