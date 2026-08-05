"""`Item`/`ItemSummary`/`SearchResult`/`SpaceInfo` → JSON (Plan §3.2, §5 Step 5). Reine
Übersetzungsschicht, keine Store-Aufrufe hier — die gehören nach `api.py`.

`item_to_json()`s `body` ist immer reiner Text, nie gerendert (P5-Y — Rendering/Sanitizing
passiert ausschließlich im Browser, `app.js`). `format` wird aus `item.extra` gelesen und als
eigenes Feld ausgegeben; `extra` selbst wird vollständig mitgeliefert, damit ein Roundtrip durch
die UI kein unbekanntes Frontmatter-Feld verliert (P5-Z, der ganze Format-Seam — keine Zeile in
`storage/`).
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from storage.models import Item, ItemSummary, SearchResult, SpaceInfo


def _iso(value: datetime) -> str:
    """Dasselbe Format wie `storage.store._format_dt` — Item-JSON und Dateitext zeigen
    identische Zeitstempel."""
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def item_to_json(item: Item, *, readonly: bool) -> dict[str, Any]:
    return {
        "id": item.id,
        "space": item.space,
        "type": item.type,
        "title": item.title,
        "status": item.status,
        "body": item.body,
        "due": item.due.isoformat() if item.due is not None else None,
        "tags": list(item.tags),
        "links": list(item.links),
        "created": _iso(item.created),
        "updated": _iso(item.updated),
        "version": item.version,
        "format": item.extra.get("format", "markdown"),
        "extra": dict(item.extra),
        "readonly": readonly,
    }


def summary_to_json(s: ItemSummary) -> dict[str, Any]:
    """Ohne `readonly` — das kennt erst der Aufrufer (`own_space` steht hier nicht zur
    Verfügung). `search_to_json()` ergänzt es je Zeile."""
    return {
        "id": s.id,
        "space": s.space,
        "type": s.type,
        "title": s.title,
        "status": s.status,
        "due": s.due.isoformat() if s.due is not None else None,
        "tags": list(s.tags),
        "links": list(s.links),
        "created": _iso(s.created),
        "updated": _iso(s.updated),
        "version": s.version,
        "snippet": s.snippet,
    }


def overview_row_to_json(s: ItemSummary, *, own_space: str) -> dict[str, Any]:
    """Zeile für `GET /api/v1/overview` — `summary_to_json()` **ohne** `snippet` (Step 7b).

    Der Grund ist Rule 4 dem Geiste nach, nicht dem Buchstaben: ein `snippet` ist Fließtext aus
    einem fremden Space. Die Übersichtsseite ist die erste Fläche, die Inhalte mehrerer Spaces
    nebeneinander zeigt, ohne dass man vorher bewusst „in einen fremden Space gewechselt" hat —
    dort gehört fremder Fließtext nicht hin. Titel und Metadaten reichen für den Zweck der Seite
    („was war zuletzt los"), und sie landen in `app.js` ausschließlich über `textContent`.
    """
    row = summary_to_json(s)
    row.pop("snippet")
    row["readonly"] = s.space != own_space
    return row


def search_to_json(r: SearchResult, *, own_space: str) -> dict[str, Any]:
    return {
        "items": [
            {**summary_to_json(s), "readonly": s.space != own_space}
            for s in r.items
        ],
        "total": r.total,
        "limit": r.limit,
        "offset": r.offset,
    }


def space_to_json(s: SpaceInfo, *, own_space: str) -> dict[str, Any]:
    return {"name": s.name, "item_count": s.item_count, "own": s.name == own_space}
