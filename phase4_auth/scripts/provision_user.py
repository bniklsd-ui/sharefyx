#!/usr/bin/env python3
"""Passwort setzen, TOTP-Seed erzeugen (Plan §2.5). Der `otpauth://`-URI ist das EINZIGE, was
auf stdout landet — und nur einmal. Alles andere (Bestätigung, Warnhinweis) geht auf stderr
(Hard Rule 7): dieses Skript hantiert mit echten, umkehrbaren Geheimnissen (P4 — anders als der
reine Token-Hash aus P2/P3).

**Niemals in eine Datei umleiten.** Der URI enthält den TOTP-Seed im Klartext — wer ihn
speichert, legt ein Dauer-Geheimnis außerhalb des Keyrings ab.
"""
from __future__ import annotations

import argparse
import getpass
import sys
from datetime import datetime, timezone

from authserver import passwords, totp, users

ISSUER = "sharefyx"


def main(argv: list[str] | None = None, *, get_password=getpass.getpass) -> int:
    parser = argparse.ArgumentParser(
        description="Passwort setzen und TOTP-Seed für einen Space erzeugen — überschreibt "
        "eine bestehende Akte für diesen Space vollständig."
    )
    parser.add_argument("--space", metavar="NAME", required=True)
    args = parser.parse_args(argv)

    password = get_password(f"Neues Passwort für '{args.space}': ")
    confirm = get_password("Nochmal: ")
    if password != confirm:
        print("Passwörter stimmen nicht überein — abgebrochen.", file=sys.stderr)
        return 1

    secret = totp.generate_secret()
    totp_alg = "SHA1"  # muss mit provisioning_uri()s algo übereinstimmen, sonst Codes, die der
    # Server nie akzeptiert (P4-G: totp_alg ist je Nutzerakte konfigurierbar)
    mapping = users.load_users_from_keyring()
    mapping[args.space] = {
        "pwd": passwords.hash_password(password),
        "totp": secret,
        "totp_alg": totp_alg,
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    users.save_users(mapping)

    print(
        totp.provisioning_uri(secret, space=args.space, issuer=ISSUER, algo=totp_alg)
    )  # einziges stdout
    print(
        f"Nutzerakte für '{args.space}' gespeichert. Der otpauth://-URI oben wird JETZT UND NIE "
        "WIEDER angezeigt — in eine Authenticator-App scannen/einfügen, NICHT in eine Datei "
        "ablegen. Verloren? Erneut ausführen (überschreibt Passwort + Seed).",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
