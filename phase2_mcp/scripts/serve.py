#!/usr/bin/env python3
"""CLI-Einstieg: liest `Settings`, baut `Store` + `KeyringTokenResolver`, startet uvicorn ohne
Access-Log (Plan §4 Step 5). Noch kein Tunnel (P3) — `--allowed-host` existiert schon, damit
Step 7s Quick-Tunnel-Probe nicht an FastMCPs DNS-Rebinding-Schutz scheitert.
"""
from __future__ import annotations

import argparse

import uvicorn

from storage.store import Store

from mcpserver.app import create_app
from mcpserver.auth import KeyringTokenResolver
from mcpserver.config import load_settings
from mcpserver.logging_setup import configure_logging


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

    store = Store(settings.data_root)
    resolver = KeyringTokenResolver()
    app = create_app(
        settings=settings,
        resolver=resolver,
        store=store,
        allowed_hosts=args.allowed_hosts,
    )

    # access_log=False (Hard Rule, §8 Risiko 3): das Access-Log schreibt die komplette URL
    # inklusive Token — der wahrscheinlichste Weg, wie dieses Projekt sein Geheimnis verliert.
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
