#!/usr/bin/env python3
"""Operator-Werkzeug gegen die echte Auth-SQLite (Plan §5 Step 7, erweitert Step 4 um
Selbstverwaltungs-Notausgänge, Plan §5 Step 4) — dünne Unterbefehle, je einer über eine bereits
vorhandene `AuthStore`-Methode. Kein `/oauth/revoke`-Endpunkt (Plan §2.1: "Ein Client-Endpunkt
dafür wäre toter Code") — Widerruf läuft ausschließlich hier, eine SSH-Sitzung entfernt
(`ratelimit.py`-Docstring).

**`revoke` kennt nur `--family-id`**, keinen `--space`-Sammelwiderruf: `revoke_family()` nimmt
genau eine `family_id` entgegen, und ein Bulk-Widerruf lässt sich aus `list-tokens --space NAME`
+ mehreren `revoke --family-id` zusammensetzen. Absichtlich keine zweite Fläche dafür — wird der
Bedarf real, ist das ein eigener Fund, keine vorgezogene Annahme. **`revoke-sessions`/
`disable-user` dürfen dagegen sammeln** (`revoke_sessions_for_space()`/`revoke_families_for_space()`,
P5 Step 4): eine Sitzung/Familie ist kein Betreiber-Werkzeug wie ein DCR-Client, sondern genau
der Notausgang, den Plan §5 Step 4 für `disable-user`/`revoke-sessions` verlangt.

DB-Pfad über `authserver.config.resolve_db_path()` (nur `SPACE_AUTH_DB`/`STATE_DIRECTORY`, nicht
das volle `load_auth_settings()` — dieses Werkzeug braucht für die meisten Unterbefehle weder
`SPACE_AUTH_MODE` noch `SPACE_PUBLIC_BASE_URL`). **Ausnahme: `invite`** liest zusätzlich
`SPACE_PUBLIC_BASE_URL` direkt (nicht über `load_auth_settings()`, das noch mehr verlangen würde,
was `invite` nicht braucht), um den vollen Einladungslink auszugeben.

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


def _cmd_invite(store: AuthStore, args: argparse.Namespace, env: dict[str, str]) -> int:
    base_url = env.get("SPACE_PUBLIC_BASE_URL")
    if not base_url:
        print("ABBRUCH: SPACE_PUBLIC_BASE_URL ist für 'invite' Pflicht.", file=sys.stderr)
        return 1
    db_path = resolve_db_path(env)
    token = store.create_invite(space=args.space, purpose=args.purpose, ttl_s=args.ttl)
    # Klartext-Link EIN einziges Mal auf stdout — dieselbe Disziplin wie provision_user.py für
    # TOTP-Seeds: kein zweiter Ort, an dem er stehen bleibt.
    print(f"{base_url}/ui/invite/{token}")

    # [2026-08-06] Diese vier Zeilen kosten den Nikinger sonst eine Stunde, live passiert:
    # der Token wird in DIE DATENBANK geschrieben, auf die `STATE_DIRECTORY`/`SPACE_AUTH_DB`
    # zeigt — der Link dagegen aus `SPACE_PUBLIC_BASE_URL` gebaut. Zwischen beiden gibt es
    # KEINE Verbindung. Wer eine Staging-Einladung erzeugt und dabei die Produktiv-Basis-URL
    # in der Umgebung stehen hat, bekommt einen Link, der auf der falschen Instanz `404
    # Einladung ungültig oder abgelaufen` liefert — was sich liest wie „Konto existiert
    # bereits" und in eine ganz andere Richtung führt. Genau so geschehen am 2026-08-06.
    #
    # Das Werkzeug kann NICHT wissen, unter welcher URL die Instanz zu dieser Datenbank
    # ausgeliefert wird (dazu müsste der Dienst sie hinterlegen — siehe Phase-Head, als
    # möglicher späterer Ausbau notiert). Was es sicher weiß, ist die Datenbank. Also nennt es
    # beides nebeneinander und überlässt den Abgleich dem Menschen, statt eine Heuristik zu
    # raten, die in der Hälfte der Fälle falsch liegt.
    instanz = "STAGING" if "staging" in str(db_path).lower() else "PRODUKTIV"
    print(f"(Space '{args.space}', Zweck '{args.purpose}', gültig {args.ttl}s)", file=sys.stderr)
    print(f"  Datenbank:  {db_path}   [{instanz}]", file=sys.stderr)
    print(f"  Link zeigt: {base_url}", file=sys.stderr)
    print(
        f"  ⚠ Prüfen: gehört die URL zur {instanz}-Instanz? Der Token gilt NUR dort — "
        "auf jeder anderen Instanz erscheint „Einladung ungültig oder abgelaufen\".",
        file=sys.stderr,
    )
    return 0


def _cmd_list_users(store: AuthStore, args: argparse.Namespace) -> int:
    users = store.list_users()
    if not users:
        print("Keine Nutzerakten.")
        return 0
    for u in users:
        changed = u.password_changed_at.isoformat() if u.password_changed_at is not None else "nie"
        unused_codes = store.count_unused_recovery_codes(u.space)
        print(
            f"{u.space}  status={u.status!r}  totp_confirmed={u.totp_confirmed_at is not None}  "
            f"password_changed={changed}  offene_recovery_codes={unused_codes}"
        )
    return 0


def _cmd_disable_user(store: AuthStore, args: argparse.Namespace) -> int:
    store.set_user_status(args.space, "disabled")
    sessions_killed = store.revoke_sessions_for_space(args.space, except_session_id=None, reason="disabled")
    families_killed = store.revoke_families_for_space(args.space, "disabled")
    # Advisor-Fund: eine noch nicht eingelöste Einladung würde sonst über `upsert_user(...,
    # status="active")` in `_invite_post` die Sperre umgehen (neue, aktive Nutzerakte).
    invites_killed = store.revoke_invites_for_space(args.space)
    print(
        f"Space '{args.space}': deaktiviert, {sessions_killed} Sitzung(en), "
        f"{families_killed} Token-Familie(n) und {invites_killed} Einladung(en) widerrufen."
    )
    return 0


def _cmd_enable_user(store: AuthStore, args: argparse.Namespace) -> int:
    store.set_user_status(args.space, "active")
    print(f"Space '{args.space}': aktiviert.")
    return 0


def _cmd_list_sessions(store: AuthStore, args: argparse.Namespace) -> int:
    rows = store.list_sessions(args.space)
    if not rows:
        print("Keine Sitzungen.")
        return 0
    for row in rows:
        status = f"widerrufen ({row.revoked_reason}, {row.revoked_at.isoformat()})" if row.revoked_at else "aktiv"
        print(
            f"created={row.created_at.isoformat()}  last_seen={row.last_seen_at.isoformat()}  "
            f"expires={row.absolute_expires_at.isoformat()}  status={status}"
        )
    return 0


def _cmd_revoke_sessions(store: AuthStore, args: argparse.Namespace) -> int:
    killed = store.revoke_sessions_for_space(args.space, except_session_id=None, reason="authctl")
    print(f"Space '{args.space}': {killed} Sitzung(en) widerrufen.")
    return 0


def main(argv: list[str] | None = None, *, env: dict[str, str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="authctl",
        description="Operator-Werkzeug gegen die echte Auth-SQLite — list-clients, list-tokens, "
        "revoke, unlock, purge-expired, invite, list-users, disable-user, enable-user, "
        "list-sessions, revoke-sessions.",
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

    p_invite = sub.add_parser("invite", help="Einladung erzeugen, Link genau einmal ausgeben")
    p_invite.add_argument("space", metavar="SPACE")
    p_invite.add_argument("--purpose", choices=["initial", "reset"], default="initial")
    p_invite.add_argument("--ttl", type=int, default=3600, metavar="SEKUNDEN")

    sub.add_parser("list-users", help="Nutzerakten auflisten (keine Hashes, keine Seeds)")

    p_disable = sub.add_parser(
        "disable-user", help="Nutzerkonto sperren, alle Sitzungen und Token-Familien widerrufen"
    )
    p_disable.add_argument("--space", metavar="NAME", required=True)

    p_enable = sub.add_parser("enable-user", help="Nutzerkonto reaktivieren")
    p_enable.add_argument("--space", metavar="NAME", required=True)

    p_lsessions = sub.add_parser("list-sessions", help="UI-Sitzungen eines Space auflisten")
    p_lsessions.add_argument("--space", metavar="NAME", required=True)

    p_rsessions = sub.add_parser("revoke-sessions", help="alle UI-Sitzungen eines Space widerrufen")
    p_rsessions.add_argument("--space", metavar="NAME", required=True)

    args = parser.parse_args(argv)
    resolved_env = env if env is not None else dict(os.environ)

    try:
        store = _open_store(resolved_env)
    except ValueError as exc:
        print(f"ABBRUCH: {exc}", file=sys.stderr)
        return 1

    handlers = {
        "list-clients": _cmd_list_clients,
        "list-tokens": _cmd_list_tokens,
        "revoke": _cmd_revoke,
        "unlock": _cmd_unlock,
        "purge-expired": _cmd_purge_expired,
        "invite": lambda s, a: _cmd_invite(s, a, resolved_env),
        "list-users": _cmd_list_users,
        "disable-user": _cmd_disable_user,
        "enable-user": _cmd_enable_user,
        "list-sessions": _cmd_list_sessions,
        "revoke-sessions": _cmd_revoke_sessions,
    }
    return handlers[args.command](store, args)


if __name__ == "__main__":
    raise SystemExit(main())
