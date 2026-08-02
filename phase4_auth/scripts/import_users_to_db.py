#!/usr/bin/env python3
"""Importiert Nutzerakten aus dem Keyring (P4-Format: Passwort-Hash + TOTP-Seed im Klartext,
`authserver/users.py`) in `auth.sqlite3` (Schema 2, P5 Step 2) — der Einmal-Übergang von
Credential-JSON/Keyring als Quelle der Wahrheit zur Auth-SQLite (P5-I).

**Immer `users.load_users_from_keyring()`, nie `load_users()`** — genau wie
`export_auth_users.py`: der Keyring, nicht das ggf. veraltete Credential-Snapshot, ist die Quelle
der Wahrheit für die Provisionierung.

**`--dry-run` ist Standard, Schreiben nur mit `--apply`.** Vorhandene Zeilen werden nicht
überschrieben, außer mit `--force`. Kein Seed, kein Hash auf stdout — nur je Space `angelegt`
oder `übersprungen`, plus eine Gesamtzahl (Hard Rule 7: Logs/Status, keine Geheimnisse).

**Reihenfolge im Betrieb** (Nikinger-Aktion, Runbook im Phase-Head): Backup → `--dry-run` →
`--apply` → `systemctl restart sharefyx-mcp` → beide Nutzer melden sich am Connector **und** an
der UI an → **erst danach** `LoadCredentialEncrypted=auth-users` aus der Unit entfernen und den
Keyring-Eintrag löschen. Nicht vorher — `spaces.cred` hat gezeigt, was passiert, wenn eine
Credential-Zeile und die Realität auseinanderlaufen.
"""
from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timezone

from authserver import users as legacy_users
from authserver.config import load_data_encryption_key, resolve_db_path
from authserver.secretbox import seal
from authserver.store import AuthStore


def _parse_created_at(raw: str) -> datetime:
    return datetime.strptime(raw, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def main(argv: list[str] | None = None, *, env: dict[str, str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Importiert Nutzerakten aus dem Keyring in auth.sqlite3 (Schema 2). "
        "Standard: --dry-run, kein Schreibzugriff. Vorhandene Zeilen bleiben ohne --force "
        "unangetastet."
    )
    parser.add_argument("--apply", action="store_true", help="tatsächlich schreiben")
    parser.add_argument(
        "--force", action="store_true", help="vorhandene Zeilen überschreiben"
    )
    args = parser.parse_args(argv)

    source = env if env is not None else dict(os.environ)

    mapping = legacy_users.load_users_from_keyring()
    if not mapping:
        print("Keine Nutzerakten im Keyring gefunden — nichts zu importieren.", file=sys.stderr)
        return 0

    dek = load_data_encryption_key(source)
    if dek is None:
        print(
            "ABBRUCH: kein Data-Encryption-Key geladen (weder CREDENTIALS_DIRECTORY/auth-dek "
            "noch Keyring nikinger-space/auth-dek) — TOTP-Seeds könnten nicht verschlüsselt "
            "werden. Erst den DEK provisionieren, siehe phase5_ui/CLAUDE.md-Runbook.",
            file=sys.stderr,
        )
        return 1

    db_path = resolve_db_path(source)
    store = AuthStore(db_path, now_fn=lambda: datetime.now(timezone.utc))

    created = 0
    skipped = 0
    for space, record in mapping.items():
        if store.get_user(space) is not None and not args.force:
            print(f"{space}: übersprungen (bereits vorhanden, --force fehlt)")
            skipped += 1
            continue

        totp_secret = record.get("totp")
        totp_secret_enc = (
            seal(totp_secret.encode("ascii"), key=dek, aad=space.encode("utf-8"))
            if totp_secret
            else None
        )
        created_at_raw = record.get("created_at")
        # Die bestehenden Seeds sind live bewiesen (P4-Abnahme) — `totp_confirmed_at` bekommt
        # deshalb den ursprünglichen `created_at`-Zeitpunkt, keinen neuen "unconfirmed"-Zustand.
        totp_confirmed_at = _parse_created_at(created_at_raw) if created_at_raw else None

        if args.apply:
            store.upsert_user(
                space,
                password_hash=record["pwd"],
                totp_secret_enc=totp_secret_enc,
                totp_alg=record.get("totp_alg", "SHA1"),
                totp_confirmed_at=totp_confirmed_at,
                status="active",
            )
            print(f"{space}: angelegt")
        else:
            print(f"{space}: würde angelegt (Probelauf — --apply fehlt)")
        created += 1

    print(
        f"{created} angelegt/würde-angelegt, {skipped} übersprungen, {len(mapping)} gesamt.",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
