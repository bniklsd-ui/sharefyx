#!/usr/bin/env python3
"""Operator-Werkzeug gegen die echte Auth-SQLite (Plan §5 Step 7) — fünf dünne Unterbefehle,
je einer über eine bereits vorhandene `AuthStore`-Methode. Kein `/oauth/revoke`-Endpunkt (Plan
§2.1: "Ein Client-Endpunkt dafür wäre toter Code") — Widerruf läuft ausschließlich hier, eine
SSH-Sitzung entfernt (`ratelimit.py`-Docstring).

**`revoke` kennt nur `--family-id`**, keinen `--space`-Sammelwiderruf: `revoke_family()` nimmt
genau eine `family_id` entgegen, und ein Bulk-Widerruf lässt sich aus `list-tokens --space NAME`
+ mehreren `revoke --family-id` zusammensetzen. Absichtlich keine zweite Fläche dafür — wird der
Bedarf real, ist das ein eigener Fund, keine vorgezogene Annahme.

DB-Pfad über `authserver.config.resolve_db_path()` (nur `SPACE_AUTH_DB`/`STATE_DIRECTORY`, nicht
das volle `load_auth_settings()` — dieses Werkzeug braucht weder `SPACE_AUTH_MODE` noch
`SPACE_PUBLIC_BASE_URL`).

Ausgabe: Text auf stdout, Logs/Fehler auf stderr (Hard Rule 7).
"""
from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timezone

from authserver.config import resolve_db_path
from authserver.ratelimit import LoginThrottle
from authserver.store import AuthStore


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _open_store(env: dict[str, str]) -> AuthStore:
    db_path = resolve_db_path(env)
    return AuthStore(db_path, now_fn=_now)


def _cmd_list_clients(store: AuthStore, args: argparse.Namespace) -> int:
    clients = store.list_clients()
    if not clients:
        print("Keine registrierten Clients.")
        return 0
    for c in clients:
        last_used = c.last_used_at.isoformat() if c.last_used_at is not None else "nie"
        print(
            f"{c.client_id}  name={c.client_name!r}  type={c.application_type!r}  "
            f"redirect_uris={list(c.redirect_uris)}  created={c.created_at.isoformat()}  "
            f"last_used={last_used}"
        )
    return 0


def _cmd_list_tokens(store: AuthStore, args: argparse.Namespace) -> int:
    families = store.list_families(space=args.space)
    if not families:
        print("Keine Token-Familien.")
        return 0
    for f in families:
        status = f"widerrufen ({f.revoked_reason}, {f.revoked_at.isoformat()})" if f.revoked_at else "aktiv"
        print(
            f"{f.family_id}  space={f.space!r}  client={f.client_id}  scope={f.scope!r}  "
            f"created={f.created_at.isoformat()}  status={status}"
        )
    return 0


def _cmd_revoke(store: AuthStore, args: argparse.Namespace) -> int:
    killed = store.revoke_family(args.family_id, "authctl")
    print(f"Familie {args.family_id}: {killed} Token(s) widerrufen.")
    return 0


def _cmd_unlock(store: AuthStore, args: argparse.Namespace) -> int:
    LoginThrottle(store, now_fn=_now).reset(args.space)
    print(f"Space '{args.space}': Sperre aufgehoben, Fehlversuchszähler zurückgesetzt.")
    return 0


def _cmd_purge_expired(store: AuthStore, args: argparse.Namespace) -> int:
    counts = store.purge_expired()
    total = sum(counts.values())
    print(f"{total} abgelaufene Zeile(n) entfernt: {counts}")
    return 0


def main(argv: list[str] | None = None, *, env: dict[str, str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="authctl",
        description="Operator-Werkzeug gegen die echte Auth-SQLite — list-clients, list-tokens, "
        "revoke, unlock, purge-expired.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list-clients", help="alle registrierten DCR-Clients auflisten")

    p_tokens = sub.add_parser("list-tokens", help="Token-Familien auflisten")
    p_tokens.add_argument("--space", metavar="NAME", default=None, help="nur diesen Space zeigen")

    p_revoke = sub.add_parser("revoke", help="eine Token-Familie widerrufen")
    p_revoke.add_argument("--family-id", metavar="ID", required=True)

    p_unlock = sub.add_parser("unlock", help="Fehlversuchssperre eines Space aufheben")
    p_unlock.add_argument("--space", metavar="NAME", required=True)

    sub.add_parser("purge-expired", help="abgelaufene Codes/Token/Requests entfernen")

    args = parser.parse_args(argv)

    try:
        store = _open_store(env if env is not None else dict(os.environ))
    except ValueError as exc:
        print(f"ABBRUCH: {exc}", file=sys.stderr)
        return 1

    handlers = {
        "list-clients": _cmd_list_clients,
        "list-tokens": _cmd_list_tokens,
        "revoke": _cmd_revoke,
        "unlock": _cmd_unlock,
        "purge-expired": _cmd_purge_expired,
    }
    return handlers[args.command](store, args)


if __name__ == "__main__":
    raise SystemExit(main())
