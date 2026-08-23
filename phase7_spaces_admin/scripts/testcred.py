#!/usr/bin/env python3
"""P7-W/A7b: macht die Zugangsdaten des dritten Testnutzers `testnutzer-p7` über den Keyring
für Claude Code nutzbar, ohne dass der Nikinger für jeden Abnahmeschritt danebensitzt.

Hart auf `testnutzer-p7` verdrahtet — kein `--space`, kein `--key`, kein `--service`. Das Skript
kann strukturell nur diesen einen Eintrag lesen/schreiben. `authserver/totp.py` wird nur
importiert, nicht geändert (bleibt tabu, §0.3) — eine zweite TOTP-Implementierung neben der
getesteten wäre der klassische Weg, wie ein Krypto-Primitiv still auseinanderläuft.

Schreibt/liest NIE eine Datei, NIE stderr/ein Log (Hard Rule 7: stdout trägt das Ergebnis,
stderr nur Fehlermeldungen ohne Geheimnis). `store` liest ausschließlich stdin — Argumente
stehen in der Prozessliste und in der Shell-History, ein Geheimnis gehört da nie hinein.
"""
from __future__ import annotations

import argparse
import json
import sys
import time

import keyring

from authserver.totp import totp_at

ALLOWED_SPACE = "testnutzer-p7"
KEYRING_SERVICE = "nikinger-space"
KEYRING_KEY = "p7-testcred"


def _load() -> dict[str, str] | None:
    raw = keyring.get_password(KEYRING_SERVICE, KEYRING_KEY)
    if raw is None:
        return None
    return json.loads(raw)


def cmd_store(argv: list[str]) -> int:
    raw = sys.stdin.read()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        print("ABBRUCH: stdin ist kein gültiges JSON.", file=sys.stderr)
        return 1
    if data.get("space") != ALLOWED_SPACE:
        print(f"ABBRUCH: space muss {ALLOWED_SPACE!r} sein.", file=sys.stderr)
        return 1
    for key in ("password", "totp_secret"):
        if not isinstance(data.get(key), str) or not data[key]:
            print(f"ABBRUCH: '{key}' fehlt oder ist kein nicht-leerer String.", file=sys.stderr)
            return 1
    keyring.set_password(
        KEYRING_SERVICE, KEYRING_KEY,
        json.dumps({"space": ALLOWED_SPACE, "password": data["password"], "totp_secret": data["totp_secret"]}),
    )
    print("gespeichert")
    return 0


def cmd_password(argv: list[str]) -> int:
    data = _load()
    if data is None:
        print("ABBRUCH: kein gespeicherter Eintrag.", file=sys.stderr)
        return 1
    print(data["password"])
    return 0


def cmd_totp(argv: list[str]) -> int:
    data = _load()
    if data is None:
        print("ABBRUCH: kein gespeicherter Eintrag.", file=sys.stderr)
        return 1
    print(totp_at(data["totp_secret"], int(time.time()) // 30))
    return 0


def cmd_purge(argv: list[str]) -> int:
    try:
        keyring.delete_password(KEYRING_SERVICE, KEYRING_KEY)
    except keyring.errors.PasswordDeleteError:
        pass
    print("entfernt")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="testcred")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("store", help="Zugangsdaten von stdin lesen und im Keyring ablegen")
    sub.add_parser("password", help="Passwort auf stdout")
    sub.add_parser("totp", help="aktueller TOTP-Code auf stdout")
    sub.add_parser("purge", help="Keyring-Eintrag entfernen")
    args = parser.parse_args(argv)

    handlers = {
        "store": cmd_store, "password": cmd_password, "totp": cmd_totp, "purge": cmd_purge,
    }
    return handlers[args.command]([])


if __name__ == "__main__":
    raise SystemExit(main())
