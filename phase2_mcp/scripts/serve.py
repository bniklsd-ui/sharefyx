#!/usr/bin/env python3
"""CLI-Einstieg: liest `Settings`, baut `Store` + die OAuth-Bündelung, startet uvicorn ohne
Access-Log (Plan §4 Step 5). Noch kein Tunnel (P3) — `--allowed-host` existiert schon, damit
Step 7s Quick-Tunnel-Probe nicht an FastMCPs DNS-Rebinding-Schutz scheitert.

**Schnitt, 2026-07-30 (Runbook-Schritt 8):** das `SPACE_AUTH_MODE`-Gate aus P4 Step 6b
(Nikinger-Entscheidung 2026-07-28) ist gefallen — `create_app()` verlangt `oauth` jetzt immer
(`TokenPathASGI`/`AuthModeASGI` sind entfernt, es gibt keinen `oauth=None`-Pfad mehr). Jeder
Start von `serve.py`, auch lokal ohne Tunnel, ruft `load_auth_settings()` **ungefangen** auf —
ein Konfigurationsfehler (z. B. fehlendes `SPACE_PUBLIC_BASE_URL`) stirbt laut beim Start, kein
`try/except`. Konsequenz für lokale Testläufe: `SPACE_PUBLIC_BASE_URL` (ein beliebiger
`https://`-Platzhalter reicht, er wird nicht kontaktiert) ist jetzt Pflicht, siehe README.md
„MCP-Server smoke-testen".
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone

import uvicorn

from authserver.config import load_auth_settings, load_data_encryption_key
from authserver.store import AuthStore
from authserver.userdir import UserDirectory

from storage.store import Store

from mcpserver.app import OAuthConfig, create_app
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

    auth_settings = load_auth_settings()
    auth_store = AuthStore(auth_settings.db_path, now_fn=lambda: datetime.now(timezone.utc))
    # P5 Step 2: `UserDirectory` liest live aus `auth.sqlite3` statt einmalig aus dem
    # Keyring/Credential-JSON (P4) — schließt O1 (Provisionierung wirkte bisher erst nach einem
    # Restart). `UserDirectory.__init__` scheitert laut, wenn kein DEK geladen werden kann, aber
    # die `users`-Tabelle nicht leer ist (Plan §2.4) — bewusst ungefangen, wie
    # `load_auth_settings()` direkt darüber.
    users = UserDirectory(auth_store, dek=load_data_encryption_key())
    oauth = OAuthConfig(settings=auth_settings, store=auth_store, users=users)

    store = Store(settings.data_root)
    app = create_app(
        settings=settings,
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
