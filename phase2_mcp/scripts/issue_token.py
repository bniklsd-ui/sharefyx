#!/usr/bin/env python3
"""Token ausgeben, widerrufen, auflisten (Plan §2.3). Das Token selbst ist das EINZIGE, was auf
stdout landet — und nur beim Ausgeben (`--space`), genau einmal. Alles andere (Hinweise,
`--revoke`, `--list`) geht auf stderr (Hard Rule 7): stdout bleibt reserviert für das eine
Geheimnis, das dieses Skript je herausgibt.
"""
from __future__ import annotations

import argparse
import sys

from mcpserver import credentials


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Space-Tokens ausgeben, widerrufen, auflisten")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--space", metavar="NAME", help="neues Token für diesen Space ausgeben")
    group.add_argument("--revoke", metavar="NAME", help="alle Tokens dieses Space widerrufen")
    group.add_argument(
        "--list", action="store_true", help="Spaces + gekürzte Hashes anzeigen, nie Tokens"
    )
    args = parser.parse_args(argv)

    if args.space:
        token = credentials.issue(args.space)
        print(token)  # das einzige stdout dieses Skripts
        print(
            f"Token für Space '{args.space}' oben ausgegeben — es wird JETZT UND NIE WIEDER "
            "angezeigt, der Keyring speichert nur den Hash. Sicher speichern. Verloren? Neu "
            "ausgeben (--space), alten Hash mit --revoke entfernen, Connector-URL in Claude "
            "aktualisieren.",
            file=sys.stderr,
        )
        return 0

    if args.revoke:
        removed = credentials.revoke(args.revoke)
        print(f"{removed} Token(s) für Space '{args.revoke}' widerrufen.", file=sys.stderr)
        return 0

    mapping = credentials.load_space_map()
    if not mapping:
        print("Keine Tokens gespeichert.", file=sys.stderr)
        return 0
    for token_hash, space in sorted(mapping.items(), key=lambda kv: kv[1]):
        print(f"{space}: {token_hash[:8]}…", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
