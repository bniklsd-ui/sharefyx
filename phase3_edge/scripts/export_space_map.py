#!/usr/bin/env python3
"""Exportiert die Space-Map aus dem Keyring als kompaktes JSON auf stdout — für
`systemd-creds encrypt --name=spaces - /etc/sharefyx/spaces.cred` (Plan §2.1/§2.3). Kein
Schreibzugriff, keine Datei, kein `--out` — der Klartext soll nie auf der Platte entstehen,
sondern nur durch die Pipe laufen.

Ruft `credentials.load_space_map_from_keyring()` **explizit** auf, nicht die neue
`load_space_map()`-Verzweigung aus Step 3 — sonst würde das Skript, liefe es zufällig im
Dienstkontext (`$CREDENTIALS_DIRECTORY` gesetzt), die bereits exportierte Datei erneut
exportieren statt die Quelle der Wahrheit (Keyring) zu lesen.
"""
from __future__ import annotations

import argparse
import json
import sys

from mcpserver import credentials


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Exportiert die Space-Map aus dem Keyring als JSON auf stdout — für "
        "systemd-creds encrypt. Enthält ausschließlich Token-Hashes, keine Tokens im Klartext."
    )
    parser.parse_args(argv)

    mapping = credentials.load_space_map_from_keyring()
    print(json.dumps(mapping, separators=(",", ":"), ensure_ascii=False))
    print(f"{len(mapping)} Einträge exportiert, keine Tokens enthalten", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
