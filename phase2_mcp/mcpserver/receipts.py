"""Kompakte Schreib-Quittungen statt Volltext (P6-H/§1.5.3) — Standardrückgabe aller vier
Schreib-Tools (`create_item`/`update_item`/`append_to_item`/`patch_item`); `return_body=True`
liefert weiterhin den vollen Dateitext (`tools.py :: item_to_filetext()`), unverändert.

**Deferred, nicht vergessen:** die Plan-Beispielquittung (§1.5.3) nennt ein `folder`-Feld —
`Item.folder` existiert erst ab P6 Step 4 (P6-Q). Bis dahin liefert diese Funktion die Quittung
ohne `folder`; das Feld kommt mit Step 4 dazu, kein Ad-hoc-Vorgriff auf ein Modellfeld, das noch
nicht existiert.

Eigene, kleine `_format_dt`/`_compact_json` statt Import aus `tools.py`: `tools.py` wird künftig
`write_receipt()` aufrufen, ein Rückimport hierher wäre ein Zirkelbezug. Dieselbe bewusste
Duplikation wie `tools.py :: item_to_filetext()` gegenüber `storage.store._item_to_text()`
(siehe dortiger Moduldocstring) — zwei Zeilen Dopplung sind billiger als eine neue Kopplung.
"""
from __future__ import annotations

import json
from collections.abc import Sequence
from datetime import datetime, timezone
from typing import Any

from storage.models import Item


def _format_dt(value: datetime) -> str:
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _compact_json(payload: Any) -> str:
    return json.dumps(payload, separators=(",", ":"), ensure_ascii=False)


def write_receipt(
    item: Item,
    *,
    op: str,
    replacements: int | None = None,
    lines: Sequence[int] = (),
    bytes_before: int | None = None,
    bytes_after: int | None = None,
    appended_bytes: int | None = None,
) -> str:
    """`op` ∈ `create|update|append|patch` — deckt sich mit den vier Schreib-Tools, nicht mit
    `Store`s internen Commit-Op-Namen (die Store-Ebene kennt zusätzlich `"archive"`/`"drift"";
    Archivieren läuft über `update_item(status="archived")`, die Quittung dazu bleibt `op="update"`).
    `replacements`/`lines`/`bytes` erscheinen nur, wenn übergeben (praktisch: nur bei `patch`).
    `appended_bytes` nur bei `append` — die Länge des angehängten Texts, keine Body-Kopie.
    **Nie Body-Inhalt**, auch nicht ausschnittsweise.
    """
    payload: dict[str, Any] = {
        "op": op,
        "id": item.id,
        "space": item.space,
        "title": item.title,
        "version": item.version,
        "updated": _format_dt(item.updated),
    }
    if replacements is not None:
        payload["replacements"] = replacements
        payload["lines"] = list(lines)
    if bytes_before is not None and bytes_after is not None:
        payload["bytes"] = {"before": bytes_before, "after": bytes_after}
    if appended_bytes is not None:
        payload["appended_bytes"] = appended_bytes
    return _compact_json(payload)
