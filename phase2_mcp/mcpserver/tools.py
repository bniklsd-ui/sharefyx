"""Die MCP-Tools (P2 Plan §3, seit P6 Step 1 sieben statt sechs, seit Phase 6.5 Step A2 acht,
seit Phase 6.5 Step B4 zehn — `get_item_asset`/`put_item_asset`, Bild-Bytes).
Registrierung über
`register(mcp, store=..., permissions=...)`, damit `server.py :: build_mcp()` `tools.py` kennt,
aber `tools.py` selbst weder HTTP noch Token kennt — nur einen Principal (`context.py`) und eine
Policy (`permissions.py`), siehe Plan §1.2.

**Step 6 (P2, historisch):** alle sechs damaligen Tools vollständig implementiert
(§3.2/§3.4/§3.5/§3.6). `list_spaces` war bereits seit Step 5 fertig (Voraussetzung für den
End-to-End-Isolationstest in `test_app.py`); die übrigen fünf lösen hier ihre
`NotImplementedError`-Platzhalter ab.

**P6 Step 1:** siebtes Tool `patch_item` (P6-E/F/G, `storage/patch.py`). Alle vier Schreib-Tools
(`create_item`/`update_item`/`append_to_item`/`patch_item`) liefern per Default eine kompakte
Quittung (`mcpserver/receipts.py :: write_receipt()`) statt des vollen Dateitexts; `return_body:
bool = False` an jedem von ihnen holt ihn zurück (P6-H). `update_item` lehnt `visibility`/
`share_read`/`share_write` mit `ValidationError` ab — die Felder existieren im Modell erst ab
Step 4/5, der Riegel entsteht bewusst vorher (P6-M).

**`item_to_filetext()` dupliziert bewusst die Feldreihenfolge von `storage.store._item_to_text`**
statt eine neue Store-Methode zu verlangen: der P1-Contract ist seit Step 2 "wieder zu" (siehe
`phase1_storage/CLAUDE.md`), eine weitere einmalige Erweiterung wäre keine mehr. Der MCP-Adapter
baut den Dateitext deshalb selbst aus `Item` + `storage.frontmatter.serialize` — dieselbe
öffentliche Funktion, die `store.py` intern auch benutzt.

**P6 Step 5:** jeder item-level Lese-/Schreibpfad (`get_item`/`update_item`/`append_to_item`/
`patch_item`) löst seine Rechte jetzt über `store.acl_of(item_id)` +
`permissions.can_read_item`/`can_write_item` auf, nicht mehr über `store.space_of(item_id)` +
die alten space-level `can_read`/`can_write` — ein einzeln freigegebenes Item (`share_read`/
`share_write`) wäre über die space-level Prüfung unsichtbar geblieben, obwohl die
Space-Wurzel selbst keine `.share.yml` trägt. `Surface.AGENT` ist fest (dieser Adapter ist
immer der Agent, nie der Mensch — Plan §1.2.4). `get_item`/`search_items` halten die
"eigen"-Entscheidung bewusst in zwei getrennten Variablen: ob geschrieben werden darf
(`can_write_item`, steuert `repair_drift`) ist eine andere Frage als ob gewrappt wird
(`item.space != principal.space`, P6-O — ein Item, das ich per `share_write` ändern darf,
bleibt trotzdem ein fremder Body und wird trotzdem gewrappt). **Fail-closed-Ergänzung, nicht
im Plan-Text, Nikinger-Entscheidung 2026-08-12:** `update_item`s `folder`-Parameter ist nur
vom Eigentümer-Space änderbar — ein `share_write`-Halter, der ein fremdes Item in einen
Ordner mit breiterer `.share.yml` verschiebt, würde sonst dessen Sichtbarkeit erweitern, ohne
dass es auf der Agentenfläche je ein Re-Auth-Gate dafür gibt (das gibt es nur für Menschen in
der UI, Step 7). Details: `phase6_shares/CLAUDE.md`s Step-5-Session-Block.
"""
from __future__ import annotations

import base64
import binascii
import json
import logging
from collections.abc import Callable
from dataclasses import replace
from datetime import date, datetime, timezone
from typing import Any

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from fastmcp.utilities.types import Image

from storage.acl import AclDecision
from storage.errors import ConflictError, ItemNotFound, SpaceNotFound, ValidationError
from storage.frontmatter import serialize as serialize_frontmatter
from storage.models import STATUS_VALUES, Item, ItemSummary, SpaceInfo, valid_statuses
from storage.patch import PatchError, TextEdit
from storage.store import Store

from . import context
from .auth import AuthError
from .permissions import Permissions, Surface
from .receipts import write_receipt

logger = logging.getLogger(__name__)

# Token-Budget (Plan P2-J) — Modulkonstanten, keine verstreuten Literale. `Store.search()`
# selbst bleibt bei `limit=50` im Kern (P1); diese Konstanten gelten nur für den MCP-Adapter.
DEFAULT_LIMIT = 20
MAX_LIMIT = 100
DEFAULT_INCLUDE_ARCHIVED = False

UNTRUSTED_OPEN = '<untrusted_content space="{space}">'
UNTRUSTED_CLOSE = "</untrusted_content>"

# [SEAM] Bekannte Grenze wie D6 (Plan §2.2, ROADMAP „Zurückgestellt aus P2"): `Store.search()`
# filtert nicht nach einer Statusliste (nur exakter Match), deshalb holt der Adapter hier alles
# bis zu dieser Grenze und filtert/paginiert `include_archived`/`offset`/`limit` selbst. Store
# scannt ohnehin jede indizierte Datei pro Aufruf (kein SQL-Filter) — diese Konstante ändert an
# der Kostenstruktur nichts, deckt aber den heutigen Datenumfang (Zwei-Personen-Space-Server)
# um Größenordnungen ab. Steigt das Volumen darüber, gehört die Filterung in den Store, nicht
# in eine höhere Konstante hier.
_STORE_FETCH_LIMIT = 5000

# N6, gelockt (Nikinger-Begründung: Claude lädt über MCP nur selbst erzeugte SVGs/kleine
# Screenshots hoch, nie großformatige Fotos) — Rohgröße NACH der Base64-Dekodierung, eigener,
# kleinerer Riegel als der Web-UI-Weg (P6.5-L, MAX_ASSET_BYTES = 5 MiB dort).
MAX_MCP_ASSET_BYTES = 1 * 1024 * 1024


class PermissionDenied(Exception):
    """P2-eigen (kein `storage`-Fehlertyp) — `can_read`/`can_write` verweigert (Plan §3.6)."""

    def __init__(self, space: str) -> None:
        super().__init__(f"kein Zugriff auf Space {space!r}")
        self.space = space


class AssetNotFound(Exception):
    """P2-eigen (kein `storage`-Fehlertyp) — Step B4: `storage.errors.ItemNotFound` wird von
    `Store.get_asset()` für ZWEI verschiedene Ursachen geworfen (fehlendes Item, fehlendes
    Asset), mit identischer Exception-Klasse. Jeder Aufrufer hier prüft `store.acl_of(item_id)`
    zuerst — ein `ItemNotFound` aus dem nachfolgenden `get_asset()`-Aufruf kann sich also nur
    noch auf die `asset_id` beziehen, nie mehr auf `item_id`. Diese Klasse macht daraus eine
    eigene, unmissverständliche Fehlermeldung statt der `ItemNotFound`-Standardmeldung „prüfe
    die ID mit search_items" — die für eine Asset-ID sachlich falsch wäre (B1s Advisor-Fund,
    hier nachgeholt)."""

    def __init__(self, asset_id: str) -> None:
        super().__init__(f"Asset nicht gefunden: {asset_id!r}")
        self.asset_id = asset_id


def wrap_untrusted(text: str, *, space: str) -> str:
    """Plan §3.5, wörtlich. Ohne das Escaping ist der Wrap ausbrechbar: eine fremde Notiz mit
    einem eigenen Closing-Tag würde den Block vorzeitig schließen und alles danach als
    vertrauenswürdigen Servertext erscheinen lassen — die Prompt-Injection, gegen die Rule 4
    überhaupt existiert."""
    safe = text.replace("</untrusted_content", "</untrusted_ content")
    return f"{UNTRUSTED_OPEN.format(space=space)}\n{safe}\n{UNTRUSTED_CLOSE}"


def compact_json(payload: Any) -> str:
    """Entscheidung I: kompaktes JSON als Text-Content, keine ASCII-Escapes."""
    return json.dumps(payload, separators=(",", ":"), ensure_ascii=False)


def _status_hint() -> str:
    """Statusvokabular aus storage.models.STATUS_VALUES generiert (P6.5-C) — nie abtippen,
    das ist genau die Drift, die Report 1 aus der 2026-08-13-Korrektur verursacht hat."""
    parts = [
        f"{t}: {'|'.join(sorted(valid_statuses(t)))}"
        for t in sorted(STATUS_VALUES)
    ]
    return "Erlaubte status-Werte je type — " + " · ".join(parts) + "."


WRITE_TOOL_DIVISION = (
    "Aufgabenteilung der Schreib-Werkzeuge: create_item legt neu an · "
    "update_item ändert Frontmatter (status/tags/links/due/title) und optional den ganzen Body · "
    "append_to_item hängt Text ans Body-Ende · "
    "patch_item ersetzt exakte Textstellen IM BODY. "
    "patch_item und append_to_item erreichen Frontmatter grundsätzlich nicht."
)

_LIST_SPACES_POINTER = (
    "Unklar, in welche Spaces du schreiben darfst? Ruf zuerst list_spaces — writable:true ist "
    "die Antwort."
)

# P7-F: Item-IDs sind eine interne Adresse, kein Anzeigename — in der Weboberfläche nur als
# Kopierfeld sichtbar (P7-A1). Wörtlich identisch an allen vier Tools, die ein Item gegenüber
# einem Menschen benennen könnten.
_TITLE_NOT_ID_HINT = (
    "Nenne einem Menschen gegenüber immer den Titel eines Items, nicht seine itm_…-ID — die "
    "ID ist eine interne Adresse und in der Weboberfläche nur als Kopierfeld sichtbar."
)


def _format_dt(value: datetime) -> str:
    """Gleiche Formatierung wie `storage.store._format_dt` — Dateitext und JSON-Ausgabe zeigen
    identische Zeitstempel."""
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse_due_before(value: str | None) -> date | None:
    if value is None:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValidationError(
            f"'due_before' muss ein ISO-Datum sein (YYYY-MM-DD), nicht {value!r}"
        ) from exc


def item_to_filetext(item: Item) -> str:
    """Frontmatter + Body als Dateitext — siehe Moduldocstring zur bewussten Duplikation."""
    fields: dict[str, Any] = {
        "id": item.id,
        "space": item.space,
        "type": item.type,
        "title": item.title,
        "status": item.status,
    }
    if item.due is not None:
        fields["due"] = item.due.isoformat()
    fields["tags"] = list(item.tags)
    fields["links"] = list(item.links)
    fields["created"] = _format_dt(item.created)
    fields["updated"] = _format_dt(item.updated)
    fields["version"] = item.version
    fields.update(item.extra)
    return serialize_frontmatter(fields, item.body)


def summary_to_dict(item: ItemSummary, *, own: bool) -> dict[str, Any]:
    """Plan §3.2 Feldliste (bewusst ohne `created`). Fremde Snippets sind gewrappt (§3.5)."""
    return {
        "id": item.id,
        "space": item.space,
        "type": item.type,
        "title": item.title,
        "status": item.status,
        "due": item.due.isoformat() if item.due is not None else None,
        "tags": list(item.tags),
        "links": list(item.links),
        "updated": _format_dt(item.updated),
        "version": item.version,
        "snippet": item.snippet if own else wrap_untrusted(item.snippet, space=item.space),
    }


def map_storage_error(exc: Exception) -> ToolError:
    """Plan §3.6 — jede Meldung nennt den nächsten Schritt, nicht nur den Zustand."""
    if isinstance(exc, ItemNotFound):
        return ToolError(f"item_not_found: {exc.item_id} — prüfe die ID mit search_items")
    if isinstance(exc, AssetNotFound):
        return ToolError(
            f"asset_not_found: {exc.asset_id} — prüfe die ID mit get_item_meta (listet die "
            "vorhandenen Assets des Items)"
        )
    if isinstance(exc, PermissionDenied):
        # P6 Step 5: dieselbe Meldung deckt jetzt drei Fälle ab, nicht nur "fremder Space, kein
        # Schreibrecht" (P2s ursprüngliche Bedeutung) — auch ein ungeteiltes fremdes Item (kein
        # Lesezugriff) und ein eigenes `visibility: human`-Item (für die Agentenfläche gesperrt,
        # P6-P) laufen hier durch. Bewusst generisch statt drei eigener Meldungen: `map_storage_
        # error()` kennt an dieser Stelle nicht, ob can_read_item oder can_write_item verweigert
        # hat (beide werfen dasselbe PermissionDenied), und drei Texte für dieselbe Ursache
        # (kein Zugriff) wären mehr Verwirrung als Hilfe.
        return ToolError(
            f"write_denied: kein Zugriff auf {exc.space} — kein Schreibrecht, das Item ist "
            "nicht mit dir geteilt, oder es ist als 'nur für Menschen' markiert"
        )
    if isinstance(exc, ConflictError):
        current = exc.current
        return ToolError(
            f"conflict: {exc.item_id} wurde geändert (deine Version {exc.expected_version}, "
            f"aktuell {current.version}, zuletzt {_format_dt(current.updated)}) — lies neu mit "
            "get_item und wiederhole"
        )
    if isinstance(exc, PatchError):
        # Muss VOR der generischen ValidationError-Prüfung stehen -- PatchError ist eine
        # ValidationError (P6-F), soll aber den spezifischeren "patch_failed"-Text bekommen,
        # nicht das generische "invalid: ...".
        if exc.found == 0:
            # Werkzeug-Ergonomie-Feedback (2026-08-14, phase6_shares/CLAUDE.md "Vormerkungen"):
            # der alte Text ("lies das Item neu") klingt nach einem Textmatching-Problem und
            # verleitet zu genau der Aktion, die nie hilft, wenn old_text tatsächlich ein
            # Frontmatter-Feld meinte — patch_item erreicht Frontmatter kategorisch nie, ein
            # erneutes Lesen ändert daran nichts. Der neue Text nennt die tatsächliche Ursache
            # (Bereich) statt eine falsche zu suggerieren (Texttreffer), ohne alt_text selbst
            # gegen eine Frontmatter-Feldliste zu prüfen — patch_item kennt Frontmatter nicht,
            # eine Heuristik hier würde nur eine Vermutung über alt_texts Herkunft raten.
            return ToolError(
                f"patch_failed: edits[{exc.index}] fand 0 Treffer — patch_item durchsucht nur "
                "den Body-Text, nie das Frontmatter. Prüfe mit get_item, ob old_text exakt so "
                "im Body steht; für title/status/tags/due/links/folder/visibility/share_read/"
                "share_write nutze stattdessen update_item"
            )
        shown = ", ".join(str(n) for n in exc.lines)
        if exc.found > len(exc.lines):
            shown += ", …"
        return ToolError(
            f"patch_failed: edits[{exc.index}] fand {exc.found} Treffer (Zeilen {shown}) — "
            "mach old_text eindeutiger"
        )
    if isinstance(exc, ValidationError):
        return ToolError(f"invalid: {exc}")
    if isinstance(exc, SpaceNotFound):
        return ToolError(f"space_not_found: {exc.space}")
    if isinstance(exc, AuthError):
        # Step-4-Advisor-Fund (siehe SESSIONS_ARCHIVE.md): der Guard wirft AuthError INNERHALB
        # eines Tool-Aufrufs — das 401-Fenster ist zu diesem Zeitpunkt vorbei, es muss
        # zwangsläufig als Tool-Fehler auftauchen. Kein Defekt (weiterhin fail-closed, keine
        # fremden Daten), aber P2-N verlangt "nie unterscheidbar von falschem Token" — deshalb
        # kein Detail hier, kein Unterschied zu einem anderen Auth-Fehlschlag.
        return ToolError("auth_error: Request-Kontext ungültig — bitte neu verbinden")
    logger.exception("internal_error in MCP tool", exc_info=exc)
    return ToolError("internal_error — siehe Serverlog")


def _authenticated_principal():
    """Schritt 1+2 aus §3.3 gebündelt (`current_principal()` → Guard). Ein `AuthError` aus dem
    Guard läuft — anders als ein fehlendes/unbekanntes Pfad-Token — INNERHALB eines laufenden
    Tool-Aufrufs; das 401-Fenster ist zu diesem Zeitpunkt vorbei (Step-4-Advisor-Fund, siehe
    `SESSIONS_ARCHIVE.md`). Ohne dieses Bündeln würde ein solcher `AuthError` roh aus dem Tool
    fallen statt über `map_storage_error()` in die einheitliche Fehlerabbildung (§3.6) zu laufen
    — genau die Abbildung, die dort als „bewusst zu treffen, nicht zufällig" verlangt wird."""
    try:
        principal = context.current_principal()
        context.assert_principal_matches_request()
        return principal
    except AuthError as exc:
        raise map_storage_error(exc) from exc


def register(mcp: FastMCP, *, store: Store, permissions: Permissions) -> dict[str, Callable[..., str]]:
    """Registriert alle acht Tools auf `mcp`. Reihenfolge in jedem Tool-Body wie Plan §3.3:
    `current_principal()` → Guard → Zielraum → Rechte → Store → Formatieren. `@mcp.tool(...)`
    gibt die unveränderte Python-Funktion zurück (nicht das interne `FunctionTool`-Objekt) —
    `register()` sammelt genau diese Funktionen und gibt sie zurück, damit Tests sie direkt
    aufrufen bzw. per `inspect.signature()` prüfen können (z. B.
    `test_create_item_into_foreign_space_is_denied`), ohne den vollen ASGI/HTTP-Stack aus
    Step 5 erneut hochzuziehen."""

    def _acl_of_summary(item: ItemSummary) -> AclDecision:
        """Baut die `AclDecision` einer bereits geladenen `ItemSummary`-Zeile (P6 Step 5) —
        über `store.acl_reader.decision_for()`, nicht über `store.acl_of(item.id)`: die Zeile
        kommt schon aus einem `store.search()`-Fetch, ein zweiter Index-Roundtrip pro Treffer
        wäre reine Verschwendung (`_STORE_FETCH_LIMIT` ist bewusst großzügig)."""
        return store.acl_reader.decision_for(
            space=item.space, folder=item.folder, visibility=item.visibility,
            share_read=item.share_read, share_write=item.share_write,
        )

    @mcp.tool(
        title="Spaces auflisten",
        description=(
            "Listet alle sichtbaren Spaces mit Item-Anzahl, Mitgliedern und Ordnern. "
            "writable:true heißt: du darfst dort schreiben — das gilt für deinen eigenen "
            "Space UND für geteilte Spaces, in denen dir write: gewährt wurde. Ruf dies "
            "zuerst auf, wenn unklar ist, wo geschrieben werden darf; rate es nicht."
        ),
        annotations={
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        },
    )
    def list_spaces() -> str:
        principal = _authenticated_principal()
        spaces = store.list_spaces()
        # Fund B1 aus der Live-Adapter-Abnahme (docs/concepts/P2_ADAPTER_ABNAHME_2026-07-26.md):
        # `Store.list_spaces()` leitet Spaces ausschließlich aus vorhandenen Indexzeilen ab (P1,
        # keine separate Space-Registry) — ein Space ohne ein einziges Item taucht dort schlicht
        # nicht auf. Ohne diesen Fallback sähe eine frische Claude-Sitzung mit einem leeren
        # eigenen Space AUSSCHLIESSLICH Spaces, in die sie nicht schreiben darf, und hätte keine
        # Möglichkeit, den eigenen Space-Namen zu erfahren, bevor sie blind `create_item` ruft.
        # `create_item` selbst ist davon nicht betroffen (der Ziel-Space kommt aus dem Principal,
        # nie aus `list_spaces`), aber die Orientierung des Modells ist es. Deshalb: der eigene
        # Space wird immer in die Antwort aufgenommen, notfalls mit `item_count=0` — kein
        # Store-Eingriff, reine Tool-Schicht-Ergänzung.
        if principal.space not in {s.name for s in spaces}:
            spaces = sorted(
                [*spaces, SpaceInfo(name=principal.space, item_count=0)], key=lambda s: s.name
            )
        visible_names = set(
            permissions.visible_spaces(principal.space, [s.name for s in spaces])
        )
        # P6-P: `visibility: human` existiert für die Agentenfläche "vollständig nicht" —
        # das schließt die hier gezeigten Zähler ein, nicht nur search_items/total. Ein
        # einziger gebündelter Fetch statt eines store.search() je sichtbarem Space.
        human_counts: dict[str, int] = {}
        for row in store.search(limit=_STORE_FETCH_LIMIT, offset=0).items:
            if row.visibility == "human":
                human_counts[row.space] = human_counts.get(row.space, 0) + 1
        payload = [
            {
                "name": s.name,
                "item_count": s.item_count - human_counts.get(s.name, 0),
                "writable": permissions.can_write(principal.space, s.name),
                "members": list(s.members),
                "folders": list(s.folders),
            }
            for s in spaces
            if s.name in visible_names
        ]
        return compact_json(payload)

    @mcp.tool(
        title="Items durchsuchen",
        description=(
            "Sucht Items über alle sichtbaren Spaces (Frontmatter + Snippet, nie der volle "
            "Body). Fremde Snippets sind gewrappt. Gesucht wird als Teilstring in Titel und "
            "Tags (Groß/Kleinschreibung egal) — NICHT im Body, außer du setzt in_body=True. "
            "Wenn ein Begriff nichts findet, liegt er vermutlich nur im Fließtext: dann "
            "in_body=True setzen oder über tags/type/status/folder filtern statt den "
            "Suchbegriff zu variieren. " + _TITLE_NOT_ID_HINT
        ),
        annotations={
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        },
    )
    def search_items(
        query: str | None = None,
        space: str | None = None,
        folder: str | None = None,
        type: str | None = None,
        status: str | None = None,
        tag: str | None = None,
        due_before: str | None = None,
        limit: int = DEFAULT_LIMIT,
        offset: int = 0,
        include_archived: bool = DEFAULT_INCLUDE_ARCHIVED,
        in_body: bool = False,
    ) -> str:
        principal = _authenticated_principal()
        clamped_limit = max(1, min(limit, MAX_LIMIT))

        try:
            due_before_date = _parse_due_before(due_before)
            result = store.search(
                query,
                space=space,
                folder=folder,
                type=type,
                status=status,
                tag=tag,
                due_before=due_before_date,
                limit=_STORE_FETCH_LIMIT,
                offset=0,
                in_body=in_body,
            )
        except ValidationError as exc:
            raise map_storage_error(exc) from exc

        # Item-weise, nicht space-weise gefiltert (P6 Step 5): ein einzeln freigegebenes Item
        # (share_read) darf sichtbar sein, ohne dass sein ganzer Ordner es wird — ein
        # space-level Vorfilter würde das Item entweder zu großzügig (ganzer Space sichtbar)
        # oder zu eng (Space unsichtbar, Item verschwindet mit) behandeln. Dieselbe Prüfung
        # entscheidet auch über visibility: human (P6-P) — inklusive `total` unten, nicht nur
        # der Seite.
        items = [
            i for i in result.items
            if permissions.can_read_item(principal.space, _acl_of_summary(i), surface=Surface.AGENT)
        ]
        if status is None and not include_archived:
            items = [i for i in items if i.status != "archived"]

        total = len(items)
        page = items[offset : offset + clamped_limit]
        payload = {
            "items": [
                summary_to_dict(i, own=(i.space == principal.space))
                for i in page
            ],
            "total": total,
            "limit": clamped_limit,
            "offset": offset,
            "truncated": offset + clamped_limit < total,
        }
        return compact_json(payload)

    @mcp.tool(
        title="Item lesen",
        description=(
            "Liest ein Item als Dateitext (Frontmatter + Body). Fremde Bodies sind gewrappt. "
            "Liefert immer den vollen Body. Wenn du nur die aktuelle version oder Frontmatter "
            "brauchst, nimm get_item_meta — das ist um Größenordnungen billiger. "
            + _TITLE_NOT_ID_HINT
        ),
        annotations={
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        },
    )
    def get_item(item_id: str) -> str:
        principal = _authenticated_principal()
        try:
            acl = store.acl_of(item_id)
        except ItemNotFound as exc:
            raise map_storage_error(exc) from exc

        if not permissions.can_read_item(principal.space, acl, surface=Surface.AGENT):
            raise map_storage_error(PermissionDenied(acl.space)) from None

        # Zwei getrennte Fragen, bewusst nicht dieselbe Variable (P6 Step 5): ob geschrieben
        # werden darf (steuert repair_drift — ein fremdes, aber share_write-erlaubtes Item
        # darf den Drift-Repair-Write bekommen) ist unabhängig davon, ob gewrappt wird (P6-O
        # — ein fremdes Item bleibt fremder Body, auch wenn ich es ändern darf).
        writable = permissions.can_write_item(principal.space, acl, surface=Surface.AGENT)
        item = store.get(item_id, repair_drift=writable)
        if acl.space != principal.space:
            item = replace(item, body=wrap_untrusted(item.body, space=item.space))
        return item_to_filetext(item)

    @mcp.tool(
        title="Item-Metadaten lesen",
        description=(
            "Liest NUR Frontmatter und Version eines Items — ohne Body. Billig. Nimm dies "
            "statt get_item, wenn du die aktuelle version für einen Schreibaufruf brauchst "
            "oder nur Status/Tags/Ordner prüfen willst. body_bytes sagt dir, wie teuer ein "
            "get_item wäre. assets listet vorhandene Bilder (id/mime/bytes/filename) — NIE "
            "die Bildbytes selbst; die holst du erst mit get_item_asset, und nur, wenn der "
            "Nutzer ausdrücklich danach fragt. " + _TITLE_NOT_ID_HINT
        ),
        annotations={
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        },
    )
    def get_item_meta(item_id: str) -> str:
        principal = _authenticated_principal()
        try:
            acl = store.acl_of(item_id)
        except ItemNotFound as exc:
            raise map_storage_error(exc) from exc

        if not permissions.can_read_item(principal.space, acl, surface=Surface.AGENT):
            raise map_storage_error(PermissionDenied(acl.space)) from None

        # Reiner Metadaten-Lesevorgang löst nie einen Drift-Repair-Write aus (anders als
        # get_item, wo `writable` das steuert) — wer nur Metadaten will, soll nie einen Write
        # auslösen, den die Antwort selbst gar nicht zeigt.
        item = store.get(item_id, repair_drift=False)
        # P6.5-M/N (Block B): die assets-Liste enthält bewusst NUR Metadaten, nie Bildbytes —
        # der einzige Weg zu echten Bytes ist get_item_asset, ein eigenes, ausdrücklich
        # aufgerufenes Tool (erzwingbare Hälfte, per Struktur-Test gepinnt).
        assets = [
            {"id": a.id, "mime": a.mime, "bytes": a.bytes, "filename": a.filename}
            for a in store.list_assets(item_id)
        ]
        payload = {
            "id": item.id,
            "space": item.space,
            "folder": item.folder,
            "type": item.type,
            "title": item.title,
            "status": item.status,
            "due": item.due.isoformat() if item.due is not None else None,
            "tags": list(item.tags),
            "links": list(item.links),
            "visibility": item.visibility,
            "share_read": list(item.share_read),
            "share_write": list(item.share_write),
            "version": item.version,
            "created": _format_dt(item.created),
            "updated": _format_dt(item.updated),
            "body_bytes": len(item.body.encode("utf-8")),
            "assets": assets,
            "own": acl.space == principal.space,
            "writable": permissions.can_write_item(principal.space, acl, surface=Surface.AGENT),
        }
        return compact_json(payload)

    @mcp.tool(
        title="Item anlegen",
        description=(
            "Legt ein neues Item an — standardmäßig im eigenen Space. space=<name> legt es "
            "stattdessen in einen anderen Space, wenn dessen .share.yml write: dafür gewährt; "
            "folder=<pfad> legt es in einen Unterordner. Liefert standardmäßig eine Quittung "
            "statt des vollen Texts — return_body=True holt ihn zurück. "
            + _status_hint() + " " + WRITE_TOOL_DIVISION + " " + _LIST_SPACES_POINTER
            + " " + _TITLE_NOT_ID_HINT
        ),
        annotations={
            "readOnlyHint": False,
            "destructiveHint": False,
            "idempotentHint": False,
            "openWorldHint": False,
        },
    )
    def create_item(
        type: str,
        title: str,
        body: str = "",
        tags: list[str] | None = None,
        links: list[str] | None = None,
        due: str | None = None,
        status: str | None = None,
        space: str | None = None,
        folder: str | None = None,
        return_body: bool = False,
    ) -> str:
        principal = _authenticated_principal()
        # P6-U (root CLAUDE.md, Hard Rule 4 Neufassung): Ziel-Space ist per Default der eigene
        # — ein anderer ist nur zulässig, wenn `.share.yml` dort `write:` gewährt. Space-level
        # Prüfung, nicht item-level: es gibt noch kein Item, dessen ACL man auflösen könnte.
        target_space = space if space is not None else principal.space
        if target_space != principal.space and not permissions.can_write(principal.space, target_space):
            raise map_storage_error(PermissionDenied(target_space)) from None
        kwargs: dict[str, Any] = {"tags": tags or [], "links": links or []}
        if due is not None:
            kwargs["due"] = due
        if status is not None:
            kwargs["status"] = status
        if folder is not None:
            kwargs["folder"] = folder
        try:
            item = store.create(target_space, type=type, title=title, body=body, **kwargs)
        except ValidationError as exc:
            raise map_storage_error(exc) from exc
        if return_body:
            return item_to_filetext(item)
        return write_receipt(item, op="create")

    @mcp.tool(
        title="Item aktualisieren",
        description=(
            "Aktualisiert ein Item, oder archiviert es über status=archived. Alle Felder sind "
            "einzeln optional — body weglassen ändert NUR das Frontmatter (z.B. status/tags/"
            "links/due) und lässt den Body unangetastet, kein Komplett-Rewrite nötig. "
            "folder=<pfad> verschiebt es — nur der Eigentümer-Space darf das, ein geteilter "
            "Schreibzugriff reicht dafür nicht. space=<name> verschiebt es in einen anderen "
            "Space — nur zwischen Spaces, in denen du schreiben darfst; kombiniere space= nicht "
            "mit inhaltlichen Feldern oder status im selben Aufruf (folder= darf mitgegeben "
            "werden, als Zielordner im neuen Space). Braucht die zuletzt gelesene version. "
            "Liefert standardmäßig eine Quittung statt des vollen Texts — return_body=True holt "
            "ihn zurück. Sichtbarkeit/Freigaben (visibility/share_read/share_write) gehen über "
            "kein Tool, nur über die UI. "
            + _status_hint() + " " + WRITE_TOOL_DIVISION + " " + _LIST_SPACES_POINTER
        ),
        annotations={
            "readOnlyHint": False,
            "destructiveHint": True,
            "idempotentHint": False,
            "openWorldHint": False,
        },
    )
    def update_item(
        item_id: str,
        version: int,
        title: str | None = None,
        body: str | None = None,
        status: str | None = None,
        tags: list[str] | None = None,
        links: list[str] | None = None,
        due: str | None = None,
        type: str | None = None,
        folder: str | None = None,
        space: str | None = None,
        visibility: str | None = None,
        share_read: list[str] | None = None,
        share_write: list[str] | None = None,
        return_body: bool = False,
    ) -> str:
        principal = _authenticated_principal()
        # P6-M: Freigaben/Sichtbarkeit sind über kein MCP-Tool änderbar — der Riegel entsteht
        # hier, VOR dem eigentlichen Feld, damit ein späterer Step ihn nicht vergisst.
        if visibility is not None or share_read is not None or share_write is not None:
            raise map_storage_error(
                ValidationError(
                    "visibility/share_read/share_write sind über kein MCP-Tool änderbar — das "
                    "geht nur ein Mensch in der UI"
                )
            ) from None

        try:
            acl = store.acl_of(item_id)
        except ItemNotFound as exc:
            raise map_storage_error(exc) from exc

        if not permissions.can_write_item(principal.space, acl, surface=Surface.AGENT):
            raise map_storage_error(PermissionDenied(acl.space)) from None

        # P6-AE (Step 7b, ITEM_MOVE_PLAN.md §2/§4.2): ein Space-Wechsel verlangt space-level
        # Schreibrecht auf QUELLE UND ZIEL — strenger als der obige item-level `can_write_item`,
        # weil ein `share_write`-Delegat, der genau ein fremdes Item bearbeiten darf, es sonst in
        # einen geteilten Space wegtragen könnte (Exfiltration und Entzug in einem Zug), ohne
        # dass es dafür je ein Re-Auth-Gate gäbe (das existiert nur für Menschen in der UI).
        if space is not None and space != acl.space:
            if not permissions.can_write(principal.space, acl.space):      # Quelle
                raise map_storage_error(PermissionDenied(acl.space)) from None
            if not permissions.can_write(principal.space, space):          # Ziel
                raise map_storage_error(PermissionDenied(space)) from None

        # Fail-closed, Nikinger-Entscheidung 2026-08-12 (kein Plan-Text): `folder` ist zwar
        # generell agenten-setzbar (`Store.update()` erlaubt es seit Step 4), aber nur für den
        # Eigentümer-Space — ein fremder `share_write`-Halter, der ein Item in einen Ordner mit
        # breiterer `.share.yml` verschiebt, würde dessen Sichtbarkeit erweitern, ohne dass es
        # auf der Agentenfläche je ein Re-Auth-Gate dafür gäbe (das gibt es nur für Menschen in
        # der UI, Step 7 — und selbst dort nur für den Eigentümer, der SEINE eigene Freigabe
        # erweitert, nicht für einen Dritten, der fremden Besitz verschiebt).
        # **[2026-08-17, Step 7b Commit 2/3, Advisor-Fund vor dem Bauen]:** dieser Riegel greift
        # nur noch beim reinen Ordner-Move (`space is None`) — bei einem Space-Wechsel ersetzt
        # ihn die strengere P6-AE-Prüfung oben, die space-level statt item-level prüft. Ohne
        # dieses `space is None` hätte der Riegel praktisch jeden legitimen Cross-Space-Move mit
        # gleichzeitig gesetztem `folder=` blockiert — kein Principal heißt wie ein geteilter
        # Space, `acl.space != principal.space` wäre also fast immer wahr gewesen.
        if folder is not None and space is None and acl.space != principal.space:
            raise map_storage_error(
                ValidationError(
                    "folder ist nur vom Eigentümer-Space änderbar — ein geteilter "
                    "Schreibzugriff erlaubt keine Verschiebung in einen anderen Ordner"
                )
            ) from None

        changes = {
            key: value
            for key, value in {
                "title": title,
                "body": body,
                "tags": tags,
                "links": links,
                "due": due,
                "type": type,
                "folder": folder,
            }.items()
            if value is not None
        }

        try:
            if space is not None:
                content_changes = {k: v for k, v in changes.items() if k != "folder"}
                if content_changes or status is not None:
                    raise ValidationError(
                        "space verschiebt ein Item pur — kombiniere es nicht mit inhaltlichen "
                        "Feldern oder status im selben Aufruf (folder darf mitgegeben werden, "
                        "als Zielordner im neuen Space)"
                    )
                item = store.move(item_id, version=version, space=space, folder=folder)
            elif status == "archived":
                if changes:
                    raise ValidationError(
                        "status=archived erlaubt keine weiteren Felder — erst inhaltlich "
                        "updaten, dann archivieren"
                    )
                item = store.archive(item_id, version=version)
            else:
                if status is not None:
                    changes["status"] = status
                item = store.update(item_id, version=version, **changes)
        except (ItemNotFound, ConflictError, ValidationError) as exc:
            raise map_storage_error(exc) from exc
        if return_body:
            return item_to_filetext(item)
        return write_receipt(item, op="update")

    @mcp.tool(
        title="Text an Item anhängen",
        description=(
            "Hängt Text an den Body eines Items im eigenen Space an. Nur der Body — für "
            "Frontmatter-Felder (status/tags/links/due) update_item nutzen, body weglassen. "
            "Braucht die zuletzt gelesene version. Liefert standardmäßig eine Quittung statt "
            "des vollen Texts — return_body=True holt ihn zurück. Mehrere Einträge in einem "
            "Aufruf: übergib einen Text mit Zeilenumbrüchen — ein Aufruf, ein Commit, eine "
            "Versionserhöhung. Die Quittung enthält die neue version; du brauchst zwischen "
            "aufeinanderfolgenden Appends kein erneutes get_item. "
            + WRITE_TOOL_DIVISION
        ),
        annotations={
            "readOnlyHint": False,
            "destructiveHint": False,
            "idempotentHint": False,
            "openWorldHint": False,
        },
    )
    def append_to_item(
        item_id: str, version: int, text: str, return_body: bool = False
    ) -> str:
        principal = _authenticated_principal()
        try:
            acl = store.acl_of(item_id)
        except ItemNotFound as exc:
            raise map_storage_error(exc) from exc

        if not permissions.can_write_item(principal.space, acl, surface=Surface.AGENT):
            raise map_storage_error(PermissionDenied(acl.space)) from None

        try:
            item = store.append(item_id, version=version, text=text)
        except (ItemNotFound, ConflictError, ValidationError) as exc:
            raise map_storage_error(exc) from exc
        if return_body:
            return item_to_filetext(item)
        return write_receipt(item, op="append", appended_bytes=len(text.encode("utf-8")))

    @mcp.tool(
        title="Item punktuell ändern",
        description=(
            "Ersetzt exakte Textstellen im Body eines Items, ohne den Rest neu zu schreiben. "
            "Nur der Body — für Frontmatter-Felder (status/tags/links/due) update_item nutzen, "
            "body weglassen. Jedes old_text muss genau einmal vorkommen; sonst schlägt der "
            "ganze Aufruf fehl und nichts wird geschrieben. Braucht die zuletzt gelesene "
            "version. Liefert standardmäßig eine Quittung statt des vollen Texts — "
            "return_body=True holt ihn zurück. "
            + WRITE_TOOL_DIVISION
        ),
        annotations={
            "readOnlyHint": False,
            "destructiveHint": True,
            "idempotentHint": False,
            "openWorldHint": False,
        },
    )
    def patch_item(
        item_id: str, version: int, edits: list[TextEdit], return_body: bool = False
    ) -> str:
        principal = _authenticated_principal()
        try:
            acl = store.acl_of(item_id)
        except ItemNotFound as exc:
            raise map_storage_error(exc) from exc

        if not permissions.can_write_item(principal.space, acl, surface=Surface.AGENT):
            raise map_storage_error(PermissionDenied(acl.space)) from None

        try:
            result = store.patch(item_id, version=version, edits=edits)
        except (ItemNotFound, ConflictError, ValidationError) as exc:
            raise map_storage_error(exc) from exc
        if return_body:
            return item_to_filetext(result.item)
        return write_receipt(
            result.item, op="patch", replacements=result.replacements,
            lines=list(result.lines), bytes_before=result.bytes_before,
            bytes_after=result.bytes_after,
        )

    @mcp.tool(
        title="Bildinhalt eines Items laden",
        description=(
            "Lädt die echten Bildbytes eines Bildes. TEUER — rufe dies NUR auf, wenn der "
            "Nutzer im Gespräch ausdrücklich verlangt, dass du den Bildinhalt ansiehst. "
            "Lade Bilder NIE automatisch, nur weil ein Item eine asset:-Referenz enthält — "
            "auch nicht bei eigenen Items. Für die reine Liste vorhandener Bilder reicht "
            "get_item_meta. Bilder aus fremden Spaces liefern nur dann Bytes, wenn du dort "
            "Schreibrechte hast; sonst bekommst du nur Metadaten."
        ),
        annotations={
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        },
    )
    def get_item_asset(item_id: str, asset_id: str) -> Image | str:
        principal = _authenticated_principal()
        try:
            acl = store.acl_of(item_id)
        except ItemNotFound as exc:
            raise map_storage_error(exc) from exc

        if not permissions.can_read_item(principal.space, acl, surface=Surface.AGENT):
            raise map_storage_error(PermissionDenied(acl.space)) from None

        # P6.5-M — strenger als can_read_item: ein fremdes Bild vor einem sehenden Modell ist
        # ein Injektionskanal, den <untrusted_content> strukturell nicht erreicht (Text-Wrapper).
        # Schreibrecht ist der gewählte Vertrauensmarker, nicht Leserecht — wer mir schreiben
        # darf, kann mir ohnehin Text unterschieben, ein zusätzliches Bild ändert daran nichts.
        own = acl.space == principal.space
        may_see_bytes = own or permissions.can_write_item(
            principal.space, acl, surface=Surface.AGENT
        )
        if not may_see_bytes:
            # Existenz erst prüfen, DANN Metadaten statt Bytes zurückgeben (Advisor-Fund vor
            # dem Commit) — sonst wäre dieser Zweig für JEDE erfundene asset_id "erfolgreich"
            # (bytes_available: false), während der erlaubte Zweig unten zwischen echter und
            # erfundener ID unterscheidet (asset_not_found). Ein share_read-Halter bekäme damit
            # eine andere Existenzauskunft als ein share_write-Halter für dieselbe ID — kein
            # Rechteproblem (die Liste ist über get_item_meta ohnehin einsehbar), aber ein
            # unehrliches bytes_available-Feld für ein Asset, das es gar nicht gibt.
            matches = [a for a in store.list_assets(item_id) if a.id == asset_id]
            if not matches:
                raise map_storage_error(AssetNotFound(asset_id)) from None
            asset = matches[0]
            return compact_json({
                "id": asset.id,
                "item_id": item_id,
                "mime": asset.mime,
                "bytes": asset.bytes,
                "filename": asset.filename,
                "bytes_available": False,
                "hint": "Bildbytes aus einem fremden Space werden nur bei Schreibrecht "
                "geliefert — dieses Item ist nur mit dir geteilt, nicht freigeschrieben.",
            })

        try:
            data, mime = store.get_asset(item_id, asset_id)
        except ItemNotFound as exc:
            # acl_of() oben ist bereits erfolgreich durchgelaufen -- item_id existiert. Ein
            # ItemNotFound an dieser Stelle kann sich also nur noch auf asset_id beziehen
            # (siehe AssetNotFound-Docstring).
            raise map_storage_error(AssetNotFound(asset_id)) from exc

        # V69 empirisch geprüft (Planungssession, `fastmcp` 3.4.4): Image._get_mime_type() baut
        # aus format ausschließlich f"image/{format.lower()}" -- da mime hier immer exakt
        # "image/png"|"image/jpeg"|"image/gif"|"image/webp" ist (sniff_image_mime()s einzige
        # vier Werte), rekonstruiert der Split-Join-Roundtrip denselben String byte-identisch.
        # Kein Fall, in dem Image(format=...) ein anderes MIME liefert als store.get_asset().
        return Image(data=data, format=mime.split("/")[-1])

    @mcp.tool(
        title="Bild in ein Item ablegen",
        description=(
            "Kündige dem Nutzer VOR JEDEM Aufruf an, dass du jetzt ein Bild ablegst — bei "
            "jedem Aufruf, nicht nur beim ersten. Lädt ein Bild (PNG/JPEG/GIF/WebP) als "
            "base64-kodierte Bytes hoch, maximal 1 MiB Rohgröße nach der Dekodierung. "
            "Schreibt NICHT den Body — füge die Referenz selbst mit update_item oder "
            "patch_item als ![Alt](asset:<id>) ein, die id steht in der Quittung dieses "
            "Aufrufs."
        ),
        annotations={
            "readOnlyHint": False,
            "destructiveHint": True,
            "idempotentHint": False,
            "openWorldHint": False,
        },
    )
    def put_item_asset(
        item_id: str, data_base64: str, filename: str | None = None
    ) -> str:
        principal = _authenticated_principal()
        try:
            acl = store.acl_of(item_id)
        except ItemNotFound as exc:
            raise map_storage_error(exc) from exc

        if not permissions.can_write_item(principal.space, acl, surface=Surface.AGENT):
            raise map_storage_error(PermissionDenied(acl.space)) from None

        try:
            data = base64.b64decode(data_base64, validate=True)
        except binascii.Error as exc:
            raise map_storage_error(
                ValidationError(f"data_base64 ist kein gültiges Base64: {exc}")
            ) from exc

        if len(data) > MAX_MCP_ASSET_BYTES:
            raise map_storage_error(ValidationError(
                f"Bild überschreitet {MAX_MCP_ASSET_BYTES} Bytes (Rohgröße nach "
                "Base64-Dekodierung) — der MCP-Weg erlaubt weniger als die Web-UI (N6)."
            )) from None

        try:
            asset = store.put_asset(item_id, data=data, filename=filename)
        except (ItemNotFound, ValidationError) as exc:
            raise map_storage_error(exc) from exc

        # Kein write_receipt() (das nimmt ein Item und einen der vier Text-op-Werte entgegen,
        # P6-H) — ein Asset-Upload ändert weder Body noch Version des Items (store.put_asset()
        # nimmt bewusst keinen version-Parameter, siehe Store-Docstring). Plan §3 Step B4
        # verlangt trotzdem "item_version unverändert" in der Quittung, ausdrücklich, damit ein
        # Modell nach dem Upload NICHT von sich aus annimmt, es müsse die version für den
        # nächsten update_item-Aufruf neu lesen. Der zusätzliche store.get()-Aufruf (dieselbe
        # billige, reine Metadaten-Lesart wie get_item_meta, kein Body) ist damit ein bewusster
        # zweiter Read für ein Feld, das der Plan verlangt — nicht optional wegzulassen.
        item_version = store.get(item_id, repair_drift=False).version
        return compact_json({
            "op": "asset",
            "id": item_id,
            "asset_id": asset.id,
            "mime": asset.mime,
            "bytes": asset.bytes,
            "item_version": item_version,
            "hint": "Referenz im Body ergänzen mit ![Alt](asset:" + asset.id + ") — "
            "put_item_asset ändert den Body NICHT.",
        })

    return {
        "list_spaces": list_spaces,
        "search_items": search_items,
        "get_item": get_item,
        "get_item_meta": get_item_meta,
        "create_item": create_item,
        "update_item": update_item,
        "append_to_item": append_to_item,
        "patch_item": patch_item,
        "get_item_asset": get_item_asset,
        "put_item_asset": put_item_asset,
    }
