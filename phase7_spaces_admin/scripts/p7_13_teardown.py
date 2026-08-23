#!/usr/bin/env python3
"""Rückbau der P6.5-8/13-Teilprobe (A8): entfernt das Test-Asset von `itm_3d0ac2b3`, direkt über
`storage.store.Store.delete_asset()` — gleiche Bauart wie die übrigen `p7_13_*`-Fixtures, kein
neuer Serverpfad. `share_read`/`share_write` sind bereits über `p7_13_share_write_fixture.py
--clear --clear-read` zurückgenommen (Version 5) — dieses Skript schließt nur noch das Asset
selbst, den dritten Punkt aus dem Teardown-Ledger in `phase7_spaces_admin/CLAUDE.md`.
"""
from __future__ import annotations

import argparse
import json
import sys

from storage.store import Store

DATA_ROOT = "/home/savefyx/savefyx-data"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="p7_13_teardown")
    parser.add_argument("item_id")
    parser.add_argument("asset_id")
    args = parser.parse_args(argv)

    store = Store(DATA_ROOT)
    store.delete_asset(args.item_id, args.asset_id)
    remaining = store.list_assets(args.item_id)
    print(json.dumps({"deleted": args.asset_id, "remaining": [a.id for a in remaining]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
