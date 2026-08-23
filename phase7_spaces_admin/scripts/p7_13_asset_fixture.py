#!/usr/bin/env python3
"""Einmaliges Setup für P6.5-13/P7-13-Teilprobe: legt ein echtes PNG-Asset auf einem Item ab,
direkt über `storage.store.Store.put_asset()` (echter Git-Commit) — gleiche Bauart wie
`p7_11_setup_fixture.py`, kein neuer Serverpfad.

Grund für den direkten Store-Aufruf statt Upload über die Web-UI/MCP: das Ziel-Item
(`itm_3d0ac2b3`, niklas' Space, `share_read: [testnutzer-p7]` seit P7-11) gehört `niklas`, dessen
UI-Session/Passwort/TOTP dieser Sitzung nicht zur Verfügung stehen — dieselbe Einschränkung wie
bei `p7_11_setup_fixture.py`. `put_asset()` selbst kennt kein Rechtemodell (das sitzt eine Schicht
höher, in `mcpserver/tools.py :: put_item_asset()`/`webui/api.py`), ein direkter Store-Aufruf ist
also kein Rechte-Bypass, nur derselbe Kürzungsweg wie beim Setzen von `share_read`.

**Bild ist ein von PIL erzeugtes echtes PNG, kein Hex-Handbau** (P6.5-5-Lehre: ein
handgetipptes PNG war beim ersten Upload-Versuch korrupt).

**Abbau nicht vergessen (P7-12-Ledger):** das erzeugte Asset liegt unter
`niklas/_assets/itm_3d0ac2b3/` — verwaist nach `spacectl.py remove-space testnutzer-p7`, weil
das Item niklas gehört, nicht testnutzer-p7. Vor P7-12 entweder das Asset löschen
(`store.delete_asset()`) oder das ganze Fixture-Item archivieren.
"""
from __future__ import annotations

import argparse
import io
import json
import sys

from PIL import Image

from storage.store import Store

DATA_ROOT = "/home/savefyx/savefyx-data"


def _png_bytes() -> bytes:
    img = Image.new("RGB", (4, 4), color=(30, 144, 255))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="p7_13_asset_fixture",
        description="Legt ein PIL-PNG als Asset auf einem Item ab, direkt über den Store.",
    )
    parser.add_argument("item_id")
    args = parser.parse_args(argv)

    store = Store(DATA_ROOT)
    asset = store.put_asset(args.item_id, data=_png_bytes(), filename="p7-13-fixture.png")
    print(json.dumps({
        "item_id": args.item_id, "asset_id": asset.id, "mime": asset.mime, "bytes": asset.bytes,
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
