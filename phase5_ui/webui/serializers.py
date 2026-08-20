"""`Item`/`ItemSummary`/`SearchResult`/`SpaceInfo` → JSON (Plan §3.2, §5 Step 5). Reine
Übersetzungsschicht, keine Store-Aufrufe hier — die gehören nach `api.py`.

`item_to_json()`s `body` ist immer reiner Text, nie gerendert (P5-Y — Rendering/Sanitizing
passiert ausschließlich im Browser, `app.js`). `format` wird aus `item.extra` gelesen und als
eigenes Feld ausgegeben; `extra` selbst wird vollständig mitgeliefert, damit ein Roundtrip durch
die UI kein unbekanntes Frontmatter-Feld verliert (P5-Z, der ganze Format-Seam — keine Zeile in
`storage/`).

**P6 Step 5:** `folder`/`visibility`/`share_read`/`share_write`/`shared` sind neu auf jedem
Item/jeder Summary. `readonly` bekommt hier weiterhin nur einen bool — die eigentliche
`can_write_item()`-Auflösung (braucht `store.acl_reader`, also einen Store-Aufruf) bleibt
`api.py`s Job, genau wie vorher; nur WAS `api.py` jetzt hineinreicht, hat sich geändert (ACL-
basiert statt reiner Space-Identität). `shared` bleibt reine Space-Identität (`item.space !=
own_space`) — das ist eine andere Frage als `readonly` (ein geteiltes Item mit `share_write`
ist `shared=True` UND `readonly=False` zugleich)."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from storage.models import AssetInfo, Item, ItemSummary, SpaceInfo


def _iso(value: datetime) -> str:
    """Dasselbe Format wie `storage.store._format_dt` — Item-JSON und Dateitext zeigen
    identische Zeitstempel."""
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def asset_to_json(asset: AssetInfo) -> dict[str, Any]:
    return {
        "id": asset.id, "mime": asset.mime, "bytes": asset.bytes,
        "filename": asset.filename, "created": _iso(asset.created),
    }


def item_to_json(
    item: Item, *, readonly: bool, own_space: str, assets: list[AssetInfo] | None = None,
) -> dict[str, Any]:
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
        "folder": item.folder,
        "visibility": item.visibility,
        "share_read": list(item.share_read),
        "share_write": list(item.share_write),
        "shared": item.space != own_space,
        "readonly": readonly,
        "assets": [asset_to_json(a) for a in assets] if assets is not None else [],
    }


def summary_to_json(
    s: ItemSummary, *, own_space: str, readonly: bool, include_snippet: bool = True
) -> dict[str, Any]:
    row = {
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
        "folder": s.folder,
        "visibility": s.visibility,
        "share_read": list(s.share_read),
        "share_write": list(s.share_write),
        "shared": s.space != own_space,
        "readonly": readonly,
    }
    if not include_snippet:
        row.pop("snippet")
    return row


def overview_row_to_json(s: ItemSummary, *, own_space: str) -> dict[str, Any]:
    """Zeile für `GET /api/v1/overview` — `summary_to_json()` **ohne** `snippet` (Step 7b).

    Der Grund ist Rule 4 dem Geiste nach, nicht dem Buchstaben: ein `snippet` ist Fließtext aus
    einem fremden Space. Die Übersichtsseite ist die erste Fläche, die Inhalte mehrerer Spaces
    nebeneinander zeigt, ohne dass man vorher bewusst „in einen fremden Space gewechselt" hat —
    dort gehört fremder Fließtext nicht hin. Titel und Metadaten reichen für den Zweck der Seite
    („was war zuletzt los"), und sie landen in `app.js` ausschließlich über `textContent`.

    **P6 Step 5:** `readonly` bleibt hier bewusst bei der alten, günstigeren Space-Identitäts-
    Näherung (`s.space != own_space`) statt einer echten `can_write_item()`-Auflösung — dieser
    Endpunkt iteriert bereits mehrere `store.search()`-Aufrufe je sichtbarem Space (Plan-Kosten
    schon bei 438-453 ms gemessen, `phase5_ui/CLAUDE.md` P6-Step-2-Ergänzung) und ist nicht Teil
    von Step 5s Aufgabenliste. Eine ACL-genaue Übersicht ist ein späterer, eigener Schnitt."""
    row = summary_to_json(s, own_space=own_space, readonly=s.space != own_space)
    row.pop("snippet")
    return row


def search_to_json(items: list[dict[str, Any]], *, total: int, limit: int, offset: int) -> dict[str, Any]:
    """Dünne Hülle um bereits fertig serialisierte Zeilen (P6 Step 5) — `readonly` je Zeile
    braucht jetzt eine `AclDecision` (`store.acl_reader`), die `serializers.py` bewusst nicht
    selbst auflöst (kein Store-Aufruf hier, siehe Moduldocstring); `api.py` baut jede Zeile
    deshalb selbst über `summary_to_json()`, während die ACL-Entscheidung ohnehin schon in der
    Hand ist, und reicht nur noch die fertige Liste herein."""
    return {"items": items, "total": total, "limit": limit, "offset": offset}


def space_to_json(s: SpaceInfo, *, own_space: str, writable: bool) -> dict[str, Any]:
    return {
        "name": s.name,
        "item_count": s.item_count,
        "own": s.name == own_space,
        "writable": writable,
        "members": list(s.members),
        "folders": list(s.folders),
    }
