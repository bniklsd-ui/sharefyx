#!/usr/bin/env python3
"""Einmaliges Setup für P7-11: setzt item-level `share_read` auf ein Item, direkt über
`storage.store.Store` (echter Git-Commit, echte Versionierung) — nicht über die Web-UI.

Grund: die `Freigeben`-Dialogbox (`dialogs.js :: openShareDialog()`) listet ausdrücklich nur
`state.spaces` — Spaces, die der Actor bereits über ein bestehendes `.share.yml`
kennt (dokumentierter, bewusster Scope-Schnitt aus Step 7 Commit 5b, siehe dortigen Kommentar).
Ein brandneuer Principal ohne jede vorherige Beziehung zu diesem Space taucht dort nicht auf —
genau der Fall, den P7-11 (P6-Zeilen 36/37) prüfen soll, ist über die UI aktuell nicht
herstellbar. Kein Bug: `mcpserver/tools.py :: update_item()` UND `webui/api.py :: _items_patch`
erlauben `share_read`/`share_write` beide bereits serverseitig (P6-M erlaubt Menschen den
Zugriff, nur MCP-Tools sind gesperrt) — dieses Skript nutzt denselben `Store.update()`-Aufruf,
den `_items_patch` intern auch macht, **aber ohne das Re-Auth-Gate aus P6-N**
(`webui/shares.py :: require_share_reauth()`), das `_items_patch` einer Freigabe-Erweiterung
davorschaltet. Kein Sicherheitsproblem — wer `DATA_ROOT`-Schreibzugriff hat, kann ohnehin alles
—, aber deshalb Fixture-Setup für einen Testlauf, kein allgemeines Freigabe-Werkzeug.

**Abbau nicht vergessen:** `spacectl.py check` prüft nur `.share.yml` (space-level), nie
item-level `share_read`/`share_write` in Frontmatter — nach `spacectl.py remove-space
testnutzer-p7` bliebe `share_read: [testnutzer-p7]` auf diesem Item sonst eine verwaiste
Freigabe, die kein Werkzeug meldet. Vor dem Abbau (P7-12) diese Fixture-Freigabe zurücknehmen
oder das Item archivieren.

Läuft direkt gegen den echten `DATA_ROOT` (kein `--dry-run`, im Gegensatz zu
`migrate_visibility.py` — eine einzelne, gezielte Item-Änderung braucht keine Vorschau-Stufe).
"""
from __future__ import annotations

import argparse
import json
import sys

from storage.store import Store

DATA_ROOT = "/home/savefyx/savefyx-data"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="p7_11_setup_fixture",
        description="Setzt share_read=[principal] auf ein Item, direkt über den Store.",
    )
    parser.add_argument("item_id")
    parser.add_argument("--version", type=int, required=True)
    parser.add_argument("--principal", default="testnutzer-p7")
    args = parser.parse_args(argv)

    store = Store(DATA_ROOT)
    item = store.update(args.item_id, version=args.version, share_read=[args.principal])
    print(json.dumps({"id": item.id, "version": item.version, "share_read": item.share_read}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
