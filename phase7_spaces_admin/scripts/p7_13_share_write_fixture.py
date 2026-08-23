#!/usr/bin/env python3
"""Zweiter Halbschritt der P6.5-13-Teilprobe: erweitert ein bereits `share_read`-freigegebenes
Item auf `share_write`, direkt über `storage.store.Store.update()` — gleiche Bauart und gleiche
Einschränkung wie `p7_11_setup_fixture.py` (kein Re-Auth-Gate aus P6-N, weil kein Web-UI-Request).

**Abbau-Ledger:** hebt `share_write` zusätzlich zu `share_read` auf `itm_3d0ac2b3` — beides vor
P7-12 zurücknehmen oder das Item archivieren (siehe `p7_11_setup_fixture.py`s Docstring).
"""
from __future__ import annotations

import argparse
import json
import sys

from storage.store import Store

DATA_ROOT = "/home/savefyx/savefyx-data"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="p7_13_share_write_fixture",
        description="Erweitert share_read auf share_write für ein Item, direkt über den Store.",
    )
    parser.add_argument("item_id")
    parser.add_argument("--version", type=int, required=True)
    parser.add_argument("--principal", default="testnutzer-p7")
    parser.add_argument(
        "--clear", action="store_true",
        help="share_write leeren statt setzen (Rueckbau-Halbschritt, kein neuer Serverpfad)",
    )
    parser.add_argument(
        "--clear-read", action="store_true",
        help="zusaetzlich share_read leeren (vollstaendiger Rueckbau in einem Aufruf)",
    )
    args = parser.parse_args(argv)

    store = Store(DATA_ROOT)
    kwargs = {"share_write": [] if args.clear else [args.principal]}
    if args.clear_read:
        kwargs["share_read"] = []
    item = store.update(args.item_id, version=args.version, **kwargs)
    print(json.dumps({
        "id": item.id, "version": item.version,
        "share_read": item.share_read, "share_write": item.share_write,
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
