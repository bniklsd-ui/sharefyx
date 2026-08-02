#!/usr/bin/env python3
"""Exportiert die Nutzerakten aus dem Keyring als kompaktes JSON auf stdout — für
`systemd-creds encrypt --name=auth-users - /etc/sharefyx/auth-users.cred` (Plan §2.5). Kein
Schreibzugriff, keine Datei, kein `--out`.

**Ausgabe enthält TOTP-Seeds im Klartext.** Nur in eine Pipe, nie in eine Datei — anders als das
frühere `phase3_edge/scripts/export_space_map.py` (P3, nur Token-Hashes exportiert, seit dem
P5-Rückbau gelöscht, `docs/concepts/PHASE4_CLOSEOUT_HANDOVER.md` §4.5), ist dieser Export ein
echtes, umkehrbares Geheimnis.
"""
from __future__ import annotations

import argparse
import json
import sys

from authserver import users


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Exportiert die Nutzerakten aus dem Keyring als JSON auf stdout — für "
        "systemd-creds encrypt. ACHTUNG: enthält TOTP-Seeds im Klartext, nur in eine Pipe."
    )
    parser.parse_args(argv)

    mapping = users.load_users_from_keyring()
    print(json.dumps(mapping, separators=(",", ":"), ensure_ascii=False))
    print(
        f"{len(mapping)} Nutzerakte(n) exportiert. ACHTUNG: enthält TOTP-Seeds im Klartext — "
        "nur in eine Pipe, nie in eine Datei.",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
