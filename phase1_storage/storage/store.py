"""`Store` — die öffentliche API des Pakets (Plan §2). Bindet `files.py`, `frontmatter.py`,
`index.py` und `models.py` zusammen. Kein Netz, kein MCP — Phase 1 ist vollständig offline
testbar (siehe Phase-Mission in `phase1_storage/CLAUDE.md`).
"""
from __future__ import annotations

import fcntl
import json
import logging
import os
import sqlite3
import threading
from collections.abc import Sequence
from contextlib import contextmanager
from dataclasses import replace
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Callable

from . import files, history, index
from .acl import ACL_FILENAME, AclDecision, AclReader
from .errors import ConflictError, ItemNotFound, ValidationError
from .frontmatter import normalize_item_fields
from .frontmatter import parse as parse_frontmatter
from .frontmatter import serialize as serialize_frontmatter
from .linkscan import ITEM_REF_RE, extract_item_refs
from .models import (
    DEFAULT_VISIBILITY,
    VISIBILITY_VALUES,
    AssetInfo,
    IndexStats,
    Item,
    ItemSummary,
    SearchResult,
    SpaceInfo,
    STATUS_VALUES,
    valid_statuses,
)
from .patch import PatchResult, TextEdit, apply_edits

logger = logging.getLogger(__name__)

# P9 Step G (P9-I/J): Ziel des „Löschens" — **Verschieben, nie `unlink`**. Der Punkt-Praefix ist
# keine Kosmetik, sondern die ganze Unsichtbarkeit, und er ist **gemessen** (Plan §9.1 behauptete
# sie, §9.2/.3 legten den Ort ohne den Punkt fest):
#   - `._trash` auf DATA_ROOT-Ebene: `rebuild_index()` iteriert `data_root.iterdir()` und
#     `list_spaces()` ebenso, beide ueberspringen Punkt-Verzeichnisse — ein hier abgelegtes Item
#     ist nachweislich unsichtbar (kein Index-Eintrag, `get()` → ItemNotFound, kein Rail-Ordner),
#     und **kein** P1-Code muss sich ädern.
#   - `<space>/_trash` (die Fassung im Plan): `rebuild_index()` macht `space_dir.rglob("*.md")`
#     OHNE Skip — das Item taucht beim naechsten Neuaufbau mit `folder="_trash"` wieder auf, und
#     `_trash` wird von `list_spaces()` sogar als **Phantom-Space** gefuehrt. Dagegen braucht es
#     Aenderungen an `index.py` UND `files.py`, also eine **zehnte** P1-Contract-Oeffnung, die
#     niemand angekuendigt hat (P9-G kuendigt nur die neunte, fuer Step F).
# Layout `._trash/<space>/<id>__<slug>.md` statt flach: der Space-Name bleibt im Pfad lesbar, und
# ein spaeteres Aufraeumen kann je Space entscheiden, ohne die Dateinamen zu rueckschreiben.
TRASH_DIR = "._trash"

_KNOWN_FIELDS = {
    "id", "space", "type", "title", "status", "due", "tags", "links",
    "created", "updated", "version", "visibility", "share_read", "share_write",
    # P9 Step F (F4): ohne diesen Eintrag landet `assignee` in `Item.extra` — und damit wäre
    # es ein unbekanntes Feld im Round-Trip statt eines Felds mit Default und Index-Spalte.
    "assignee",
    # P9 Block trace: ohne diesen Eintrag landet `updated_by` in `Item.extra` — dieselbe
    # Konsequenz wie bei `assignee` zwei Zeilen darüber (F4).
    "updated_by",
    # P10.5 Block 9 (RE-7): ohne diesen Eintrag landet `created_by` in `Item.extra` — dieselbe
    # Konsequenz, dritte Wiederholung derselben Falle. Ein Feld in `extra` überlebt zwar den
    # Round-Trip, hat aber **keinen** Default, **keine** Index-Spalte und **keinen** Platz im
    # `ItemSummary` — es wäre ein Feld, das nur beim Lesen existiert.
    "created_by",
}
_DEFAULT_STATUS = {"task": "open", "note": "active"}
# Vom Store selbst verwaltet — dürfen nie über **fields/**changes hereinkommen, sonst
# überschreibt `Item.extra` beim Schreiben (`fields.update(item.extra)`) die berechneten Werte.
#
# P9 Block trace: `updated_by` steht ab hier mit drin (P9-AA). Es ist damit **über keinen
# Kanal setzbar** — weder `create(updated_by=…)` noch `update(updated_by=…)` kommen durch
# (beide werfen `ValidationError`), und die Adapter (MCP, REST) geben es gar nicht erst
# weiter. Gesetzt wird es aus dem `actor`-Argument, das die aufrufende Schicht aus dem
# authentifizierten Principal fuellt. Das ist dieselbe Klasse wie `updated`: ein Feld, dessen
# Wert die Identitaet behauptet, die der Server kennt, nicht die der Client behauptet.
#
# P10.5 Block 9 (RE-7): `created_by` steht ab hier mit drin — **zweite** Oeffnung derselben
# Art. `create(created_by=…)` wirft damit `ValidationError`, `update(created_by=…)` ebenfalls,
# und die Adapter geben es nicht weiter (die REST-Whitelist `_PATCH_FIELDS` kennt es nicht,
# der POST filtert es weg). Der Wert kommt allein aus dem `actor` des Anlegevorgangs.
_SYSTEM_MANAGED_FIELDS = {"id", "space", "created", "updated", "version", "updated_by", "created_by"}



def _default_now() -> datetime:
    return datetime.now(timezone.utc)


def _coerce_due(value: Any) -> date | None:
    if value is None:
        return None
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        return date.fromisoformat(value)
    raise ValidationError(f"'due' muss date, ISO-String oder None sein, nicht {type(value)!r}")


def _coerce_assignee(value: Any) -> str:
    """P9 Step F (V160): `assignee` ist ein **Space-Name** als freier String — validiert wird
    nur der Typ, nie der Inhalt. Die Typprüfung ist kein Widerspruch zu "ohne Validierung":
    sie verhindert, dass `assignee: 42` als Zahl im Frontmatter landet, und greift für jeden
    Adapter (REST, MCP, CLI) an einer Stelle, statt in jedem neu.

    **Warum keine Prüfung gegen die Space-Liste** (Plan §8.4, V160): der Server müsste dafür
    den Space anlegen oder auflösen, mit dem ein Item in einem fremden Space belegt sein
    könnte — das ist eine zweite Contract-Öffnung, die P9-G nicht ankündigt, und ein
    Verzeichnis-Scan pro Schreibvorgang. Ein toter Space-Name ist ein Anzeigefehler, kein
    Datenverlust; ein *erfundener* Zweiter Space wäre es.
    """
    if value is None:
        return ""
    if not isinstance(value, str):
        raise ValidationError(f"'assignee' muss ein String (Space-Name) sein, nicht {type(value)!r}")
    return value.strip()


def _parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _format_dt(value: datetime) -> str:
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _item_from_text(
    text: str, *, version_override: int | None = None, folder_override: str = "", source=None,
) -> Item:
    fields, body = parse_frontmatter(text)
    # 15.3 (B5): Lesen ist nachsichtig · 15.3b (E5): `source` nennt die Datei in der Warnung
    fields = normalize_item_fields(fields, source=source)
    extra = {k: v for k, v in fields.items() if k not in _KNOWN_FIELDS}
    return Item(
        id=fields["id"],
        space=fields["space"],
        type=fields["type"],
        title=fields["title"],
        status=fields["status"],
        body=body,
        due=date.fromisoformat(fields["due"]) if fields.get("due") else None,
        tags=list(fields.get("tags", []) or []),
        links=list(fields.get("links", []) or []),
        created=_parse_dt(fields["created"]),
        updated=_parse_dt(fields["updated"]),
        version=version_override if version_override is not None else fields["version"],
        folder=folder_override,
        visibility=fields.get("visibility", DEFAULT_VISIBILITY),
        share_read=list(fields.get("share_read", []) or []),
        share_write=list(fields.get("share_write", []) or []),
        # P9 Step F: fehlt das Feld (jeder Altbestand-Item), gilt der Default — siehe F6, warum
        # genau deshalb nie ein leeres `assignee:` in eine bestehende Datei geschrieben wird.
        assignee=str(fields.get("assignee", "") or ""),
        # P9 Block trace (P9-AB): fehlt das Feld — jeder Altbestand-Item, und nach dem Deploy
        # praktisch jedes vorhandene Item —, gilt der Default. `str(... or "")` faengt dazu
        # ein `updated_by:` mit leerem Wert ab, das jemand von Hand eingetragen hat.
        updated_by=str(fields.get("updated_by", "") or ""),
        # P10.5 Block 9 (RE-7): dasselbe Muster ein drittes Mal — fehlt das Feld (jeder
        # Altbestand-Item, und nach dem Deploy praktisch jedes vorhandene Item), gilt der
        # Default. `str(... or "")` faengt dazu ein `created_by:` mit leerem Wert ab, das
        # jemand von Hand eingetragen hat. **Kein Backfill** (P10.5-W): der Wert wird nie
        # nachtraeglich erfunden.
        created_by=str(fields.get("created_by", "") or ""),
        extra=extra,
    )


def _item_to_text(item: Item) -> str:
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
    # P6 Step 4: nur schreiben, wenn vom Default abweichend (Plan §2.1: "leer = nicht
    # vorhanden") -- sonst bekäme jedes bestehende Item beim nächsten Write ein stilles
    # `visibility: private`, obwohl das explizit Aufgabe von `migrate_visibility.py` (Step 6)
    # ist, nicht ein Nebeneffekt dieses Schritts. `folder` erscheint hier nie -- abgeleitet,
    # nie Frontmatter.
    if item.visibility != DEFAULT_VISIBILITY:
        fields["visibility"] = item.visibility
    if item.share_read:
        fields["share_read"] = list(item.share_read)
    if item.share_write:
        fields["share_write"] = list(item.share_write)
    # P9 Step F (F6): **nur bei nicht-leer**, exakt nach dem Muster von `visibility`/`share_*`
    # direkt darüber, und aus demselben Grund. Ohne diese Bedingung bekäme *jedes* bestehende
    # Item beim nächsten beliebigen Write ein stilles `assignee: ""` — ein Frontmatter-Diff,
    # den niemand bestellt hat, in jedem einzelnen Altbestand-Item (P9-42).
    if item.assignee:
        fields["assignee"] = item.assignee
    # P9 Block trace (P9-AB): dieselbe Bedingung ein drittes Mal, aus demselben Grund wie
    # `visibility`/`share_*`/`assignee`. Ohne sie bekaeme jeder Altbestand-Item beim naechsten
    # beliebigen Write ein stilles `updated_by: ""` — und das waere hier schlimmer als bei den
    # anderen, denn die UI **liest** dieses Feld als "zuletzt geaendert von" (eine leere Zeile
    # waere eine leere Anzeige an prominenter Stelle, kein unauffaelliger Diff).
    if item.updated_by:
        fields["updated_by"] = item.updated_by
    # P10.5 Block 9 (RE-7): **direkt nach `updated_by`**, dieselbe Bedingung (nur bei
    # nicht-leerem Wert), derselbe Grund. Ohne sie bekaeme jeder Altbestand-Item beim
    # naechsten beliebigen Write ein stilles `created_by: ""` — ein Frontmatter-Diff, den
    # niemand bestellt hat, in jedem einzelnen Altbestand-Item (P9-42, dieselbe Lehre).
    # **Kein Backfill** (P10.5-W): die Reihenfolge im Dict ist damit auch die Reihenfolge
    # im Frontmatter — `created_by` steht hinter `updated_by`, nicht davor.
    if item.created_by:
        fields["created_by"] = item.created_by
    fields.update(item.extra)
    return serialize_frontmatter(fields, item.body)


def _snippet(body: str, *, length: int = 160) -> str:
    text = " ".join(body.split())
    if len(text) <= length:
        return text
    cut = text.rfind(" ", 0, length)
    if cut <= 0:
        cut = length
    return text[:cut] + "…"


def _check_type_and_status(item_type: str, status: str) -> None:
    """Wirft `ValidationError` bei unbekanntem `type` oder einem `status`, der laut
    `models.STATUS_VALUES` für diesen `type` nicht erlaubt ist (Entscheidung D2). Einmal hier
    statt in jedem Adapter (CLI, MCP) neu — die CLI hielt das bisher nur über `argparse choices`
    ab, was ein zweiter Eingang (MCP) umgangen hätte.
    """
    _require_str("type", item_type)
    _require_str("status", status)
    allowed = valid_statuses(item_type)
    if not allowed:
        raise ValidationError(f"Unbekannter type {item_type!r} — erlaubt: {sorted(STATUS_VALUES)}")
    if status not in allowed:
        raise ValidationError(
            f"Status {status!r} nicht erlaubt für type {item_type!r} — erlaubt: {sorted(allowed)}"
        )


# P10.5 Block 15.3 (Ultra-Review B5/B8): **Schreiben ist streng** — das Gegenstueck zu
# `frontmatter.normalize_item_fields()` (Lesen ist nachsichtig). Hier, im Kern, deckt die Pruefung
# REST, MCP und CLI an einer Stelle; vorher nahm REST `tags: [1, 2]` mit 201 an (und vergiftete
# danach die Suche), machte aus `tags: "abc"` drei Tags und schrieb `body: 5` auf die Platte,
# bevor etwas warf.
_STR_FIELDS = ("title", "body")
_STR_LIST_FIELDS = ("tags", "links", "share_read", "share_write")


def _require_str(name: str, value: Any) -> None:
    if not isinstance(value, str):
        raise ValidationError(f"'{name}' muss ein String sein, nicht {type(value).__name__}")


def _require_str_list(name: str, value: Any) -> None:
    if not isinstance(value, (list, tuple)) or not all(isinstance(v, str) for v in value):
        raise ValidationError(f"'{name}' muss eine Liste von Strings sein")


# P10.5 15.5 (E3, Nikinger 2026-10-30: 256): der Titel erreicht den Pfad nicht mehr (der Slug ist in
# `files.item_filename()` gekürzt) — das Limit ist eine Produktregel, in **Zeichen**. Live gemessen:
# längster Titel 89 Zeichen bei 263 Items.
MAX_TITLE_CHARS = 256


def _check_title_length(title: str) -> None:
    if len(title) > MAX_TITLE_CHARS:
        raise ValidationError(
            f"Der Titel ist {len(title)} Zeichen lang — erlaubt sind höchstens {MAX_TITLE_CHARS}."
        )


def _check_write_types(values: dict[str, Any]) -> None:
    for name in _STR_FIELDS:
        if name in values:
            _require_str(name, values[name])
    for name in _STR_LIST_FIELDS:
        if name in values:
            _require_str_list(name, values[name])


def _summary(item: Item) -> ItemSummary:
    return ItemSummary(
        id=item.id, space=item.space, type=item.type, title=item.title, status=item.status,
        due=item.due, tags=list(item.tags), links=list(item.links),
        created=item.created, updated=item.updated, version=item.version,
        snippet=_snippet(item.body),
        folder=item.folder, visibility=item.visibility,
        share_read=list(item.share_read), share_write=list(item.share_write),
        # P9 Step F (F10): **nicht im Plan §8.2 genannt und trotzdem Pflicht.** `ItemSummary` zu
        # erweitern (F3) ohne diese Zeile wäre ein totes Feld: `_summary()` ist die einzige
        # Stelle, die eine Trefferzeile baut, und sie bekommt ein `Item` — ohne hier durchzureichen
        # stünde in jeder Liste und jeder Suchtrefferliste dauerhaft `assignee: ""`, während
        # `get()` den echten Wert liefert. Genau die Klasse Drift, die F4 (_KNOWN_FIELDS) verhindert.
        assignee=item.assignee,
        # P9 Block trace: **wieder** die Pflichtstelle, die der Plan nicht nennt und ohne die
        # es ein totes Feld waere — exakt F10 aus P9 Step F, jetzt fuer `updated_by`. `search()`
        # ist der Weg, ueber den ein Agent (und die UI-Liste) merkt, dass jemand anderes
        # geschrieben hat. Ohne diese Zeile stuende dort dauerhaft `""`, waehrend `get()` den
        # echten Wert lieferte.
        updated_by=item.updated_by,
        # P10.5 Block 9 (RE-7): die Pflichtstelle, die der Plan nicht nennt und ohne die es ein
        # totes Feld waere — exakt F10 aus P9 Step F, jetzt fuer `created_by`. `search()` ist der
        # Weg, ueber den ein Agent sieht, **wer** etwas angelegt hat; ohne diese Zeile stuende
        # dort dauerhaft `""`, waehrend `get()` den echten Wert lieferte.
        created_by=item.created_by,
    )


# -- P10.5 Block 9 (RE-4/RE-3): Umbenennen mit Absturzsicherheit -----------------------------
#
# **Warum es überhaupt einen Marker gibt.** Ein Umbenennen ist die erste Operation in diesem
# System, die **zwei** Dinge anfasst: ein Verzeichnis (oder ein Space-Verzeichnis) **und** die
# Item-Dateien darin. Ein Absturz dazwischen hinterlässt einen Zwischenstand, den kein
# Einzelschritt zurücknehmen kann — und der Index (Hard Rule 2: reine Ableitung) waere dann
# stale. Der Marker beantwortet die einzige Frage, die nach einem Absturz zaehlt: **was war
# gerade in Bewegung?**
#
# Der Marker liegt unter `DATA_ROOT` mit **Punkt-Praefix** — derselbe Trick wie `._trash`
# (P9 Step G): `rebuild_index()` iteriert `data_root.iterdir()` und ueberspringt Punkt-Verzeichnisse,
# `list_spaces()` ebenso. Der Marker ist damit fuer beide Scans unsichtbar, ohne dass ein
# P1-Code sich aendern muss.
#
# **Er wird nie committet.** Die `.gitignore` im `DATA_ROOT` (geschrieben von
# `history.ensure_repo()`) bekommt eine Zeile dafuer — sonst wuerde `git add -A` den Marker
# mitnehmen, und die Historie zeigte bei jedem Rename eine Datei, die es nicht mehr gibt.
RENAME_MARKER = ".rename-pending.json"
_RENAME_MARKER_IGNORE = ".rename-pending.json"


class Store:
    def __init__(
        self,
        data_root: Path,
        *,
        now_fn: Callable[[], datetime] = _default_now,
        git: bool = True,
    ) -> None:
        self._data_root = Path(data_root)
        self._now_fn = now_fn
        self._git_enabled = git
        self._lock = threading.RLock()
        self._db_path = self._data_root / ".index.sqlite3"
        self._conn, rebuilt = index.connect(self._db_path)
        self._acl = AclReader(self._data_root)
        if self._git_enabled:
            history.ensure_repo(self._data_root)
        # P10.5 Block 9 (9.4): ein unterbrochener Rename wird **hier** zu Ende gefuehrt — nach
        # dem Index-Verbinden (die Wiederaufnahme schreibt Index-Zeilen) und vor dem ersten
        # Zugriff. Ohne diesen Aufruf bliebe ein halb umbenannter Ordner fuer immer halb.
        self._resume_pending_rename()
        if rebuilt:
            # Das Schema wurde gerade leer (neu) angelegt (V46-Fix, siehe index.connect()) --
            # ohne diesen Aufruf bliebe ein echter Dienst-Neustart nach einem Schema-Sprung
            # dauerhaft mit leerem Index laufen, weil `serve.py` `rebuild_index()` sonst nie
            # aufruft. Dateien sind die Wahrheit (Hard Rule 2), das hier ist billig.
            self.rebuild_index()

    # -- Sperren -----------------------------------------------------------------

    @contextmanager
    def _file_write_lock(self):
        """`flock` auf `<DATA_ROOT>/.write.lock` — schützt gegen andere Prozesse (nicht gegen
        den Menschen im Editor, siehe Plan §3.2). Nur um den eigentlichen Dateischreibvorgang.
        """
        lock_path = self._data_root / ".write.lock"
        lock_path.touch(exist_ok=True)
        with open(lock_path, "r+") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)

    def _commit(self, op: str, item_id: str, space: str, actor: str = "") -> None:
        """Git-Commit nach einem erfolgreichen Write (Entscheidung E), Message `<op> <id>
        [<space>]`. Wird ausschließlich aus Aufrufern heraus benutzt, die bereits
        `self._file_write_lock()` halten — das serialisiert die Git-Aufrufe auch über
        Prozessgrenzen hinweg (siehe `history.commit`-Docstring). Nie fatal: `history.commit`
        loggt selbst `critical` und wirft nie.

        `actor` (P9-AC) ist der optionale Git-**Autor**; der Committer bleibt `Space Server`.
        Leer heißt "unbekannter Schreiber" (Operator-Skripte, Tests, Drift-Abgleich) — dann
        laeuft der Commit mit der Default-Identitaet, statt einen zu erfinden.
        """
        if self._git_enabled:
            history.commit(self._data_root, f"{op} {item_id} [{space}]", author=actor)

    # -- Interne Helfer ------------------------------------------------------------

    def _row_to_item(self, row: sqlite3.Row) -> Item:
        path = self._data_root / row["path"]
        # `folder` wird aus dem Pfad NEU abgeleitet, nicht aus `row["folder"]` übernommen: die
        # Index-Spalte ist reine Ableitung (Hard Rule 2), kein autoritativer Wert. Würde ein
        # veralteter/falscher Index-Wert hier direkt durchgereicht, würde ihn `update()` beim
        # nächsten Schreibvorgang über `_write_item_file`s Zielpfad-Berechnung ungefragt zur
        # Wahrheit machen und die Datei verschieben — "ein Index-Fehler fasst nie eine Datei an"
        # (`phase1_storage/CLAUDE.md`) gilt auch hier.
        return _item_from_text(
            path.read_text(encoding="utf-8"),
            version_override=row["version"],
            folder_override=files.folder_from_path(self._data_root, row["space"], path),
            source=path,
        )

    def _reconcile_and_get_row(self, item_id: str, *, repair_drift: bool = True) -> sqlite3.Row:
        """Liest die Indexzeile, erkennt externe Edits (Entscheidung D) und reindiziert bei
        Bedarf. Bei echter Inhaltsänderung wird die gebumpte Version **ins Frontmatter
        zurückgeschrieben** — sonst würde ein `rebuild_index()` (Entscheidung A, jederzeit
        erlaubt, läuft laut Plan G beim Start) die Version wieder auf den alten Dateistand
        zurücksetzen und das Konfliktschutz-Fenster lautlos wieder öffnen (Nikinger-Entscheidung
        2026-07-24, siehe Session-stopped-Block).

        `repair_drift=False` (P2 Step 2, Entscheidung D3): bei erkannter Inhaltsänderung wird
        **nicht** ins Frontmatter zurückgeschrieben und **kein** Git-Commit erzeugt — nur der
        Index wird nachgezogen (reine Ableitung, kein Cross-Space-Write). Für fremde Spaces:
        ein Lesezugriff dort fasst keine Datei an (Rule 4); `version` ist dort informativ, nicht
        autoritativ, weil es dort per Architektur keine Writes gibt.

        Muss unter `self._lock` **und** `self._file_write_lock()` aufgerufen werden — diese
        Methode kann schreiben (deshalb keine eigene Lock-Verwaltung: verschachteltes `flock`
        auf demselben Lockfile würde sich selbst blockieren, wenn `update`/`append`/`archive`
        den Write-Lock bereits halten und intern hierher reinlaufen).
        """
        row = index.get_item_row(self._conn, item_id)
        if row is None:
            raise ItemNotFound(item_id)
        path = self._data_root / row["path"]
        if not path.exists():
            raise ItemNotFound(item_id)
        stat = path.stat()
        if stat.st_mtime != row["mtime"] or stat.st_size != row["size"]:
            fresh = index.row_from_file(self._data_root, path)
            if fresh["sha256"] != row["sha256"]:
                if repair_drift:
                    new_version = row["version"] + 1
                    self._rewrite_version_in_file(path, new_version)
                    # P9 Block trace: **kein** `actor`. Eine Fremdänderung hat per Definition
                    # keinen Akteur durch diesen Prozess — der auslösende Aufrufer repariert
                    # nur die Versionsnummer, er hat den Inhalt nicht geschrieben. Ihm den
                    # Akteur des aufrufenden Schreibvorgangs zu geben (es ist dieselbe Methode,
                    # derselbe Prozess) würde `git blame` eine Zeile zuschreiben, die niemand
                    # geschrieben hat — die genaue Sorte Zuschreibung, die P9-AB vermeiden will.
                    self._commit("drift", item_id, row["space"])
                    fresh = index.row_from_file(self._data_root, path)
                # sonst: `fresh["version"]` trägt bereits die Version aus der Datei selbst
                # (der Mensch hat sie nie angefasst) — nichts weiter zu tun.
            else:
                fresh["version"] = row["version"]
            index.upsert_item(self._conn, fresh)
            # Phase 8 Block B Step B2 (P8-M): auch `item_links` an die neue Body-Realitaet
            # anpassen -- ein Drift-Repair (Body vom Menschen editiert) kann itm_...-Refs
            # hinzugefuegt oder entfernt haben. Frontmatter-Refs sind `row_from_file()`s
            # `links_json`-Spalte entnommen, die schon in `fresh` steht.
            frontmatter_refs = [
                ref for ref in json.loads(fresh["links_json"]) if ITEM_REF_RE.fullmatch(ref)
            ]
            rows = (
                [(ref, "frontmatter") for ref in frontmatter_refs]
                + [(ref, "body") for ref in fresh["body_refs"]]
            )
            index.replace_item_links(self._conn, item_id, rows)
            row = index.get_item_row(self._conn, item_id)
        return row

    def _rewrite_version_in_file(self, path: Path, new_version: int) -> None:
        """Schreibt nur das `version`-Feld neu — sonst nichts. Minimaler Fußabdruck: die Datei
        bleibt bis auf dieses eine Feld exakt so, wie der Mensch sie hinterlassen hat.
        """
        text = path.read_text(encoding="utf-8")
        fields, body = parse_frontmatter(text)
        fields["version"] = new_version
        files.atomic_write(path, serialize_frontmatter(fields, body))

    def _link_rows(self, item: Item) -> list[tuple[str, str]]:
        """Phase 8 Block B Step B2 (P8-M): die Kantenmenge eines Items.
        **[P10.5 15.3]:** rechnet nur noch (vorher `_replace_links_for_item`, rechnete und
        schrieb) — `_write_item_file` ruft es **vor** dem Datei-Write, damit ein Fehler hier
        nie eine geschriebene Datei ohne Commit hinterlaesst (Ultra-Review B8).

        `frontmatter_refs` = `item.links`-Eintraege, die `ITEM_REF_RE.fullmatch` passieren
        (beliebige Strings im `links:`-Feld bleiben erlaubt und werden keine Kante, Plan §3
        B2). `body_refs` = `extract_item_refs(item.body)`. Beide werden zu einer Liste
        `[(dst_id, kind), ...]` zusammengefuehrt; `replace_item_links(conn, src_id, rows)`
        loescht alles Vorhandene und fuegt neu ein -- idempotent, darf mehrfach in einer
        Schreiboperation aufgerufen werden. Setzt KEINEN eigenen Git-Commit, weil der Aufrufer
        (`_write_item_file`) bereits committet.

        Voraussetzung: `self._lock` UND `self._file_write_lock()` werden vom Aufrufer gehalten,
        genau wie bei `index.upsert_item`.
        """
        frontmatter_refs = [ref for ref in item.links if ITEM_REF_RE.fullmatch(ref)]
        body_refs = extract_item_refs(item.body)
        return (
            [(ref, "frontmatter") for ref in frontmatter_refs]
            + [(ref, "body") for ref in body_refs]
        )

    def _write_item_file(
        self, item: Item, *, old_path: Path | None, op: str, actor: str = ""
    ) -> Path:
        """Schreibt `item` an den (ggf. neuen) Pfad, benennt bei Titeländerung um, aktualisiert
        den Index und committet (`op` benennt den Git-Commit, z.B. "create"/"update"/"append").
        Muss unter `self._lock` **und** `self._file_write_lock()` aufgerufen werden.

        Phase 8 Block B Step B2 (P8-M): nach `index.upsert_item` schreibt diese Methode auch
        die Kanten (`_link_rows`, seit 15.3 vor dem Write gerechnet) -- damit JEDER Schreibpfad
        (`create`/`update`/`patch`/`append`/`move`/`archive`) genau einmal pro Operation die `item_links`-Tabelle
        aktualisiert, ohne dass jede Store-Methode das selbst tun muss.

        `actor` (P9 Block trace) wandert nur an `_commit()` — `updated_by` steht bereits im
        `item`, weil jede aufrufende Methode es vorher gesetzt hat. Hier noch einmal setzen
        waere eine zweite Wahrheit; genau die Divergenz, die F11 in `update()` aufgedeckt hat.
        """
        slug = files.slugify(item.title)
        if item.status == "archived":
            # `move()`s siebte Contract-Öffnung (P7 Step C4): ein archiviertes Item lebt
            # physisch immer unter `_archive/`, unabhängig vom (stets leeren) `folder`-Feld —
            # `files.item_path()` kennt diesen Sonderfall nicht, nur `archive()` selbst kannte
            # ihn bisher (eigene, separate Pfad-Berechnung dort). Hierher gezogen, damit `move()`
            # ein archiviertes Item korrekt im Ziel-`_archive/` ablegt statt an der Space-Wurzel.
            target_path = self._data_root / item.space / "_archive" / files.item_filename(item.id, slug)
        else:
            target_path = files.item_path(self._data_root, item.space, item.id, slug, folder=item.folder)
        write_path = old_path if old_path is not None else target_path
        # P10.5 Block 15.3 (Ultra-Review B8): Text und Kanten **vor** dem Write rechnen — ein
        # Fehler kommt nie nach `atomic_write`. Vorher schrieb `body: 5` Datei und Index und warf
        # erst in der Link-Extraktion: kein Commit, Client sah 500, das Item stand auf v+1.
        text = _item_to_text(item)
        link_rows = self._link_rows(item)
        write_path.parent.mkdir(parents=True, exist_ok=True)
        files.atomic_write(write_path, text)
        if old_path is not None and old_path != target_path:
            files.move_file(write_path, target_path)
        row = index.row_from_file(self._data_root, target_path)
        index.upsert_item(self._conn, row)
        index.replace_item_links(self._conn, item.id, link_rows)
        self._commit(op, item.id, item.space, actor)
        return target_path

    # -- Öffentliche API (Plan §2) ---------------------------------------------------

    def list_spaces(self) -> list[SpaceInfo]:
        """Vereinigung aus Verzeichnissen unter `data_root` und Indexzeilen (P6 Step 4, Plan
        §1.4) — ein frisch angelegter geteilter Space ohne Item wäre sonst unsichtbar (derselbe
        Fund wie B1 aus der P2-Adapter-Abnahme, eine Ebene höher). `members` kommt aus der
        Space-Wurzel-`.share.yml`, `folders` aus einem sortierten Verzeichnis-Walk ohne
        `RESERVED_DIR_NAMES`.
        """
        with self._lock:
            counts: dict[str, int] = {}
            for row in index.all_rows(self._conn):
                counts[row["space"]] = counts.get(row["space"], 0) + 1
            disk_spaces = {
                p.name for p in self._data_root.iterdir()
                if p.is_dir() and not p.name.startswith(".")
            }
            names = sorted(set(counts) | disk_spaces)
            result = []
            for name in names:
                space_dir = self._data_root / name
                members = tuple(sorted(self._acl.members_of_space(name)))
                folders: tuple[str, ...] = ()
                if space_dir.is_dir():
                    folders = tuple(sorted(
                        d.relative_to(space_dir).as_posix()
                        for d in space_dir.rglob("*")
                        if d.is_dir()
                        and not any(part in files.RESERVED_DIR_NAMES for part in d.relative_to(space_dir).parts)
                    ))
                result.append(SpaceInfo(
                    name=name, item_count=counts.get(name, 0), members=members, folders=folders,
                ))
            return result

    def ensure_folder(self, space: str, folder: str) -> str:
        """Legt einen leeren Ordner an (Step 7 Commit 3, K4) — reine Verzeichnisoperation, kein
        Content-Write: kein Git-Commit, kein eigener Index-Eintrag nötig, `list_spaces()`s
        `rglob`-Walk findet ein `mkdir`'tes Verzeichnis genauso wie eines, das durch ein Item
        entstanden ist. Idempotent (`exist_ok=True`) — ein bereits vorhandener Ordner ist kein
        Fehler, derselbe Nutzer könnte sonst durch einen Doppelklick eine Fehlermeldung sehen,
        obwohl am Ergebnis nichts falsch ist.
        """
        with self._lock:
            folder = files.validate_folder(folder)
            if not folder:
                raise ValidationError("Ordnername darf nicht leer sein")
            (self._data_root / space / folder).mkdir(parents=True, exist_ok=True)
            return folder

    def rename_folder(self, space: str, old: str, new: str, *, actor: str = "") -> int:
        """**RE-4 (P1-Öffnung 13):** benennt einen Ordner im Space um und gibt die Zahl der
        betroffenen Items zurück.

        **Warum das so harmlos ist:** Ordner stehen **nicht** im Frontmatter, sie werden aus dem
        Pfad abgeleitet (P6 Step 4, `files.folder_from_path()`). Ein Ordner-Umbenennen ist
        deshalb ein **reines Verzeichnis-Rename** — es wird **keine** Item-Datei umgeschrieben und
        **keine** `version` erhöht. Der Inhalt der Dateien bleibt byte-identisch; was sich ändert,
        ist ihr Pfad.

        **Was trotzdem passiert (und warum es nicht-trivial ist):**
        - Die `.share.yml` im Ordner **wandert mit** — das ist der eigentliche Fund aus P8.6
          §0.4.1 (die „billige Frontend-Fassung" ließ die Freigabe eines geteilten Ordners
          zurück, und der Ordner war danach eine Sackgasse: sichtbar, aber nicht mehr teilbar).
        - Die **Index-Zeilen** der betroffenen Items tragen `folder` und `path` — beide müssen
          nachziehen. Der Index ist Ableitung (Hard Rule 2), also wird er aus den **Dateien**
          neu gelesen (`index.row_from_file()`), nicht gerechnet.
        - `AclReader`s `stat()`-Cache: der Cache-Schlüssel ist `(Pfad, mtime, size)` — der
          **Pfad** ist Teil des Schlüssels, die verschobene `.share.yml` wird also am neuen Pfad
          **frisch** gelesen. (Der alte Cache-Eintrag ist harmlos: `stat()` auf dem alten Pfad
          schlägt fehl, `_read_one()` liefert dann eine leere `Grant`.)

        **Ein Commit** für das ganze Umbenennen (`rename-folder <space>:<old>→<new>`) — derselbe
        Autor wie bei jedem anderen Schreibvorgang (`actor`).

        **Absturzsicherheit (9.4):** vor dem ersten Verzeichniswechsel wird der Marker
        `.rename-pending.json` geschrieben; `Store.__init__` führt ihn zu Ende, falls der Prozess
        dazwischen stirbt.

        Autorisierung passiert **nicht** hier (wie überall im Store) — der Aufrufer prüft die
        Rechte VOR diesem Call (die Web-Fläche: `permissions.manages_space()`)."""
        with self._lock, self._file_write_lock():
            alt = files.validate_folder(old)
            neu = files.validate_folder(new)
            if not alt or not neu:
                raise ValidationError("Ordnername darf nicht leer sein")
            if alt == neu:
                raise ValidationError(
                    f"Der neue Name ist der alte — der Ordner '{alt}' heisst bereits so."
                )
            if neu.startswith(alt + "/"):
                # Sonst wuerde der Ordner in sich selbst hineinrennen (`os.rename()` auf ein
                # Verzeichnis in sich selbst ist ein `EINVAL` — der Fehler waere da, aber nicht
                # mit einer lesbaren Meldung).
                raise ValidationError(
                    f"Der neue Name '{neu}' liegt unter dem alten '{alt}' — das ist nicht möglich."
                )
            alt_dir = self._data_root / space / alt
            neu_dir = self._data_root / space / neu
            if not alt_dir.is_dir():
                raise ValidationError(f"Ordner '{alt}' existiert im Space '{space}' nicht.")
            if neu_dir.exists():
                raise ValidationError(
                    f"Ordner '{neu}' existiert im Space '{space}' bereits — es wurde nichts "
                    "bewegt."
                )
            if not (self._data_root / space).is_dir():
                raise ValidationError(f"Space '{space}' existiert nicht.")
            self._refuse_while_rename_pending()

            self._ensure_rename_marker_ignored()
            self._write_rename_marker({
                "kind": "folder", "space": space, "old": alt, "new": neu,
                "actor": actor, "started": _format_dt(self._now_fn()),
            })
            try:
                # 15.2 (Ultra-Review B2): `archiv/projekte` bei fehlendem `archiv/` — verschachtelte
                # Zielnamen sind erlaubt, also wird der Elternordner angelegt (wie `files.move_file()`
                # es fuer Dateien tut). Vorher: `FileNotFoundError`, Marker blieb, jeder Start scheiterte.
                neu_dir.parent.mkdir(parents=True, exist_ok=True)
                self._rename_directory(alt_dir, neu_dir)
                betroffen = self._reindex_moved_folder(space, alt, neu)
            except BaseException:
                # Der Marker bleibt liegen: `Store.__init__` führt den Rename zu Ende. Ohne ihn
                # waere ein Absturz mitten im Rename ein halb umbenannter Ordner ohne jede
                # Spur — die schlimmste Variante, weil niemand merkt, dass etwas halb ist.
                self._clear_marker_if_nothing_moved(alt_dir, neu_dir)
                raise
            self._commit_rename(f"rename-folder {space}:{alt}→{neu}", actor)
            self._clear_rename_marker()
            return betroffen

    def rename_space(self, old: str, new: str, *, actor: str = "") -> int:
        """**RE-3 (P1-Öffnung 14):** benennt einen Space um und gibt die Zahl der betroffenen
        Items zurück.

        **Warum das aufwendiger ist als ein Ordner-Umbenennen:** der Space-Namen steht **im
        Frontmatter** jeder Item-Datei (§1.5) — er ist also **keine** abgeleitete Größe wie der
        Ordner (RE-4). Verzeichnis und Frontmatter dürfen nie auseinanderlaufen (B2-Schutz), also
        gilt hier die Semantik von `move()`: jedes Item des Spaces bekommt `space=new`,
        `version+1`, `updated=now` und `updated_by=actor` (oder den bisherigen Wert, wenn kein
        Actor genannt ist).

        **Was passiert (unter beiden Locks):**
        - Der neue Name wird nach **derselben Regel** geprüft wie beim Anlegen eines Spaces
          (`files.is_valid_space_name()`, seit 15.5 die eine Regel für Anlegen, Umbenennen
          und Item-Writes).
        - **Marker** schreiben (9.4) → `os.rename(DATA_ROOT/<old>, DATA_ROOT/<new>)` (atomar,
          gleiches Dateisystem) + `fsync` des Elternverzeichnisses.
        - Jede Item-Datei unter dem neuen Verzeichnis (inkl. `_archive/`) wird mit `space: new`
          neu geschrieben — **atomar je Datei**, **ohne** Einzel-Commit.
        - `._trash/<old>` → `._trash/<new>`, falls vorhanden (die Dateien dort bleiben
          **unverändert**: sie sind Historie, und `._trash` wird von keinem Scan gelesen).
        - Die Index-Zeilen werden aus den **Dateien** neu gelesen (`index.row_from_file()`) — der
          Index ist Ableitung (Hard Rule 2), er wird nie gerechnet.
        - **Ein** Commit `rename-space <old>→<new>` → Marker löschen.

        **Fremdverweise werden nicht angefasst.** Eine fremde `.share.yml`, die den alten Namen
        nennt, und Items mit `assignee == old` bleiben, wie sie sind — sie zu „reparieren" wäre
        eine stille Rechteänderung. Sie werden **gemeldet** (die Web-Fläche macht das vor dem
        Aufruf, wie `_spaces_delete` es mit `orphan_refs` macht).

        Autorisierung passiert **nicht** hier (wie überall im Store) — der Aufrufer prüft die
        Rechte VOR diesem Call (die Web-Fläche: `permissions.is_team_space()` +
        `permissions.manages_space()`; P10.5-M: **nur Team-Spaces**)."""
        with self._lock, self._file_write_lock():
            if not files.is_valid_space_name(new):
                raise ValidationError(f"'{new}' ist kein gültiger Space-Name.")
            if old == new:
                raise ValidationError(
                    f"Der neue Name ist der alte — der Space '{old}' heisst bereits so."
                )
            alt_dir = self._data_root / old
            neu_dir = self._data_root / new
            if not alt_dir.is_dir():
                raise ValidationError(f"Space '{old}' existiert nicht.")
            if neu_dir.exists():
                raise ValidationError(
                    f"Space '{new}' existiert bereits — es wurde nichts bewegt."
                )
            self._refuse_while_rename_pending()

            self._ensure_rename_marker_ignored()
            self._write_rename_marker({
                "kind": "space", "old": old, "new": new,
                "actor": actor, "started": _format_dt(self._now_fn()),
            })
            try:
                self._rename_directory(alt_dir, neu_dir)
                betroffen = self._rewrite_space_frontmatter(old, new, actor)
                self._move_trash_dir(old, new)
            except BaseException:
                # Der Marker bleibt liegen: `Store.__init__` führt den Rename zu Ende (9.4).
                self._clear_marker_if_nothing_moved(alt_dir, neu_dir)
                raise
            self._commit_rename(f"rename-space {old}→{new}", actor)
            self._clear_rename_marker()
            return betroffen

    def _rewrite_space_frontmatter(self, old: str, new: str, actor: str) -> int:
        """Schreibt **jede** Item-Datei des (bereits verschobenen) Space-Verzeichnisses mit
        `space: new` neu. **Atomar je Datei, ohne Einzel-Commit** — der eine Commit des
        Umbenennens kommt am Ende (Plan §9.3).

        **Idempotent:** eine Datei, deren Frontmatter **nicht** mehr `old` sagt, wird **nicht**
        angefasst. Das ist die Grundlage der Wiederaufnahme nach einem Absturz (9.4): die bereits
        umgeschriebenen Dateien bekommen **keinen** zweiten Versionssprung.

        Die Datei wird **an ihren Platz** geschrieben (`files.atomic_write()`), nicht umbenannt:
        der Dateiname trägt die Item-ID und den Titel-Slug, und der Titel ändert sich nicht.
        """
        neu_dir = self._data_root / new
        jetzt = self._now_fn()
        betroffen = 0
        for path in sorted(neu_dir.rglob("*.md")):
            if path.name.startswith("."):
                continue
            try:
                item = _item_from_text(path.read_text(encoding="utf-8"), source=path)
            except (OSError, ValueError, KeyError) as exc:
                # Eine kaputte Datei darf den Rename nicht abbrechen — aber sie wird **nicht**
                # stillschweigend übergangen: `logger.critical`, und der Index zählt sie nicht.
                logger.critical(
                    "Space-Umbenennung: %s ist unlesbar (%s) — die Datei bleibt, wie sie ist.",
                    path, exc,
                )
                continue
            if item.space != old:
                continue
            neu_item = replace(
                item, space=new, version=item.version + 1, updated=jetzt,
                updated_by=actor or item.updated_by,
            )
            files.atomic_write(path, _item_to_text(neu_item))
            index.upsert_item(self._conn, index.row_from_file(self._data_root, path))
            betroffen += 1
        return betroffen

    def _move_trash_dir(self, old: str, new: str) -> None:
        """`._trash/<old>` → `._trash/<new>`. Die Dateien darin bleiben **unverändert** — sie
        sind Historie (ein gelöschtes Item trägt weiter sein altes `space:` im Frontmatter, und
        das ist genau richtig: es war im alten Space).

        Existiert **beide**, wird **nicht** zusammengeführt: ein Merge wäre ein Datenumbau ohne
        Commit und ohne Index — und der Müll wird von keinem Scan gelesen. Der Fall wird
        geloggt, nicht stillschweigend entschieden."""
        trash_alt = self._data_root / TRASH_DIR / old
        trash_neu = self._data_root / TRASH_DIR / new
        if not trash_alt.is_dir():
            return
        if trash_neu.exists():
            logger.critical(
                "Space-Umbenennung: %s und %s existieren beide — der Müll wird nicht "
                "zusammengefuehrt.", trash_alt, trash_neu,
            )
            return
        trash_neu.parent.mkdir(parents=True, exist_ok=True)
        self._rename_directory(trash_alt, trash_neu)

    def _reindex_moved_folder(self, space: str, alt: str, neu: str) -> int:
        """Zieht die Index-Zeilen der verschobenen Items nach. **Aus den Dateien**, nicht
        gerechnet: `index.row_from_file()` liest die Item-Datei am neuen Pfad und liefert
        `path`, `folder`, `mtime`, `size` und `sha256` — genau die Spalten, die sich geändert
        haben. `version` kommt aus dem Frontmatter der Datei und ist damit **unverändert**
        (RE-4 hebt keine Version an).

        Betroffen ist ein Item, dessen Ordner **gleich** `alt` ist oder **unterhalb** von `alt`
        beginnt (verschachtelte Ordner). `folder` ist der aus dem Pfad abgeleitete Relative-Pfad
        innerhalb des Spaces (`""` = Space-Wurzel, `_archive` = nie ein Ordner)."""
        betroffen = 0
        alt_rel = Path(space) / alt
        for row in index.all_rows(self._conn):
            folder = row["folder"]
            if folder != alt and not folder.startswith(alt + "/"):
                continue
            alter_pfad = Path(row["path"])
            try:
                relativer = alter_pfad.relative_to(alt_rel)
            except ValueError:  # pragma: no cover - der Ordner steht im Pfad, also passt es
                continue
            neuer_pfad = self._data_root / space / neu / relativer
            if not neuer_pfad.is_file():
                # Die Datei ist weg (externer Eingriff zwischen Rename und Index). Der Index
                # darf dann keine Zeile erfinden — `rebuild_index()` ist die Wahrheit.
                continue
            index.upsert_item(self._conn, index.row_from_file(self._data_root, neuer_pfad))
            betroffen += 1
        return betroffen

    def _resume_pending_rename(self) -> None:
        """**9.4: Absturzsicherheit.** Wird aus `Store.__init__` aufgerufen, **nach** dem
        Index-Verbinden und **vor** dem ersten Zugriff.

        Der Ablauf ist der des Plan-Abschnitts 9.4: der Rename wird **idempotent** zu Ende
        gefuehrt (das Verzeichnis wandert **nur**, wenn `old` noch existiert — ein bereits
        umbenannter Ordner wird nicht noch einmal umbenannt), danach `rebuild_index()` (Hard
        Rule 2: der Index ist ableitbar, ein halb umbenannter Index wird nie zur Wahrheit), ein
        Commit, und zuletzt wird der Marker geloescht.

        **Ein unbekannter `kind` loescht den Marker NICHT.** Ein Marker, den niemand versteht,
        bleibt liegen und wird geloggt — ein stilles Wegwerfen waere genau die Fehlerklasse, die
        dieser ganze Abschnitt verhindern soll."""
        marker = self._read_rename_marker()
        if marker is None:
            return
        kind = marker.get("kind")
        with self._lock, self._file_write_lock():
            try:
                if kind == "folder":
                    self._resume_folder_rename(marker)
                elif kind == "space":
                    self._resume_space_rename(marker)
                else:
                    logger.critical(
                        "Rename-Marker mit unbekannter Art %r — der Marker bleibt liegen, "
                        "bis ein Mensch ihn prueft: %s", kind, marker,
                    )
                    return
            except Exception:
                # 15.2 (Ultra-Review B2): die Wiederaufnahme darf den Start **nie** verhindern —
                # vorher war ein Fehler hier unter systemd eine Crash-Schleife. Der Marker bleibt
                # (er ist die einzige Spur des halben Renames, `_refuse_while_rename_pending()`
                # schuetzt ihn), der Index wird aus dem tatsaechlichen Plattenstand neu gebaut.
                logger.critical(
                    "Rename-Wiederaufnahme gescheitert — der Dienst startet trotzdem, der Marker "
                    "bleibt liegen, bis ein Mensch ihn prueft: %s", marker, exc_info=True,
                )
                self.rebuild_index()

    def _resume_folder_rename(self, marker: dict[str, Any]) -> None:
        """Setzt einen unterbrochenen Ordner-Rename zu Ende. Idempotent: das Verzeichnis
        wandert **nur**, wenn `old` noch existiert und `new` noch nicht."""
        space = str(marker.get("space", ""))
        alt = str(marker.get("old", ""))
        neu = str(marker.get("new", ""))
        actor = str(marker.get("actor", ""))
        alt_dir = self._data_root / space / alt
        neu_dir = self._data_root / space / neu
        if alt_dir.is_dir() and not neu_dir.exists():
            neu_dir.parent.mkdir(parents=True, exist_ok=True)
            self._rename_directory(alt_dir, neu_dir)
        elif not neu_dir.is_dir():
            logger.critical(
                "Rename-Wiederaufnahme: weder '%s' noch '%s' existiert — der Ordner ist weg.",
                alt_dir, neu_dir,
            )
            return
        self._reindex_moved_folder(space, alt, neu)
        self.rebuild_index()
        self._commit_rename(f"rename-folder {space}:{alt}→{neu}", actor)
        self._clear_rename_marker()

    def _resume_space_rename(self, marker: dict[str, Any]) -> None:
        """Setzt einen unterbrochenen Space-Rename zu Ende. Idempotent auf drei Ebenen:

        - Das Verzeichnis wandert **nur**, wenn `old` noch existiert und `new` noch nicht.
        - Das Frontmatter wird **nur** dort umgeschrieben, wo es noch `old` sagt — eine bereits
          umgeschriebene Datei bekommt **keinen** zweiten Versionssprung.
        - Der Müll wandert **nur**, wenn `old` noch da ist.

        Danach `rebuild_index()` (Hard Rule 2: der Index ist ableitbar — ein halb umbenannter
        Index wird nie zur Wahrheit), ein Commit, und zuletzt wird der Marker gelöscht."""
        old = str(marker.get("old", ""))
        new = str(marker.get("new", ""))
        actor = str(marker.get("actor", ""))
        alt_dir = self._data_root / old
        neu_dir = self._data_root / new
        if alt_dir.is_dir() and not neu_dir.exists():
            self._rename_directory(alt_dir, neu_dir)
        elif not neu_dir.is_dir():
            logger.critical(
                "Rename-Wiederaufnahme: weder '%s' noch '%s' existiert — der Space ist weg.",
                alt_dir, neu_dir,
            )
            return
        self._rewrite_space_frontmatter(old, new, actor)
        self._move_trash_dir(old, new)
        self.rebuild_index()
        self._commit_rename(f"rename-space {old}→{new}", actor)
        self._clear_rename_marker()

    @property
    def data_root(self) -> Path:
        """Roher `DATA_ROOT`-Pfad (P7 Step C2) — für Aufrufer, die `storage.acl`s Schreibseite
        (C1) direkt benutzen wollen, statt eine neue `Store`-Methode je Space-Verwaltungs-
        operation zu bekommen (dieselbe Zurückhaltung wie `spacectl.py`s eigener Docstring zur
        `Store`-Fläche)."""
        return self._data_root

    # -- P10.5 Block 9: Umbenennen (RE-4/RE-3) + Absturzsicherheit (9.4) --------------------

    def _rename_marker_path(self) -> Path:
        return self._data_root / RENAME_MARKER

    def _write_rename_marker(self, payload: dict[str, Any]) -> None:
        """Schreibt den Marker **atomar** (`files.atomic_write()` — dieselbe Mechanik wie bei
        einer Item-Datei). Er wird geschrieben, **bevor** das erste Verzeichnis wandert: ein
        Marker, der nach dem Umbenennen entsteht, kann den entscheidenden Absturz nicht mehr
        abdecken."""
        files.atomic_write(
            self._rename_marker_path(),
            json.dumps(payload, ensure_ascii=False, sort_keys=True),
        )

    def _read_rename_marker(self) -> dict[str, Any] | None:
        """Liest den Marker. `None` heisst „kein Rename in Bewegung" — auch dann, wenn die Datei
        kaputt ist: eine kaputte Markerdatei darf keinen Start blockieren, sie muss aber
        **sichtbar** sein (`logger.critical`, wie überall im Kern)."""
        path = self._rename_marker_path()
        if not path.is_file():
            return None
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            logger.critical("Rename-Marker %s ist unlesbar: %s", path, exc)
            return None
        if not isinstance(data, dict):
            logger.critical("Rename-Marker %s ist kein JSON-Objekt — ignoriert", path)
            return None
        return data

    def _refuse_while_rename_pending(self) -> None:
        """15.2: solange ein Marker liegt (eine gescheiterte Wiederaufnahme, siehe
        `_resume_pending_rename()`), wird kein neuer Rename begonnen — er wuerde den Marker
        ueberschreiben und damit die einzige Spur des halben Renames loeschen."""
        if self._rename_marker_path().exists():
            raise ValidationError(
                "Ein frueheres Umbenennen ist nicht abgeschlossen (Marker "
                f"{RENAME_MARKER} im Datenverzeichnis) — erst pruefen, dann erneut versuchen."
            )

    def _clear_marker_if_nothing_moved(self, alt_dir: Path, neu_dir: Path) -> None:
        """15.2 (Ultra-Review B2): der Rename ist gescheitert, **bevor** etwas gewandert ist
        (`alt` steht noch, `neu` gibt es nicht) — dann beschreibt der Marker nichts Halbes, und
        er muss weg: sonst fuehrte der naechste Start einen Rename aus, den der Aufrufer als
        Fehler gesehen hat. Entschieden wird am **Plattenstand**, nicht daran, welcher Aufruf
        warf."""
        if alt_dir.is_dir() and not neu_dir.exists():
            self._clear_rename_marker()

    def _clear_rename_marker(self) -> None:
        try:
            self._rename_marker_path().unlink()
        except FileNotFoundError:
            pass

    def _ensure_rename_marker_ignored(self) -> None:
        """Sorgt dafuer, dass der Marker **nie** in die Git-Historie wandert.

        `history.commit()` macht `git add -A` — und der Marker existiert in genau dem Moment, in
        dem der Rename committet wird (Plan §9.2: „ein Commit → Marker löschen"). Ohne diese
        Zeile stuende in der Historie jedes Renames eine Datei, die es nicht mehr gibt.

        Die `.gitignore` im `DATA_ROOT` schreibt `history.ensure_repo()` — **hier** wird sie nur
        **ergänzt**, nie überschrieben: `ensure_repo()` fasst eine vorhandene Datei nicht an, und
        das bleibt so (sonst würde ein spaeterer `ensure_repo()`-Aufruf die Zeile wieder
        wegschreiben)."""
        gitignore = self._data_root / ".gitignore"
        try:
            inhalt = gitignore.read_text(encoding="utf-8") if gitignore.is_file() else ""
        except OSError:
            return
        if _RENAME_MARKER_IGNORE in inhalt.split("\n"):
            return
        try:
            with open(gitignore, "a", encoding="utf-8") as f:
                if inhalt and not inhalt.endswith("\n"):
                    f.write("\n")
                f.write(_RENAME_MARKER_IGNORE + "\n")
        except OSError as exc:  # pragma: no cover - der Commit laeuft auch ohne die Zeile
            logger.critical(".gitignore im DATA_ROOT nicht ergaenzbar: %s", exc)

    @staticmethod
    def _rename_directory(old_dir: Path, new_dir: Path) -> None:
        """`os.rename()` fuer **Verzeichnisse** + `fsync` des Elternverzeichnisses.

        Warum nicht `files.move_file()`: das benutzt `os.replace()` und ist fuer **Dateien**
        gedacht (es macht `new_path.parent.mkdir()`). `os.replace()` auf ein nicht leeres
        Zielverzeichnis schlaegt fehl — und ein Ordner, der beim Umbenennen atomar verschwinden
        soll, darf nicht erst kopiert und dann geloescht werden. `os.rename()` auf ein
        Verzeichnis ist der eine Syscall, der genau das tut.

        Das `fsync` auf dem Elternverzeichnis ist derselbe Schritt wie bei `files.atomic_write()`:
        ohne ihn kann ein Absturz den Verzeichniseintrag zurueckrollen, obwohl `rename()`
        zurueckgemeldet wurde."""
        os.rename(old_dir, new_dir)
        dir_fd = os.open(old_dir.parent, os.O_RDONLY)
        try:
            os.fsync(dir_fd)
        finally:
            os.close(dir_fd)

    def _commit_rename(self, message: str, actor: str = "") -> None:
        """**Ein** Commit fuer das ganze Umbenennen (Plan §9.2/§9.3: „ein Commit"). Die
        `_commit()`-Hilfe baut ihre Message aus `op`/`item_id`/`space` — fuer ein Rename passt
        das nicht (ein Ordner hat keine Item-ID, ein Space-Umbenennen keinen einzelnen Space-Namen
        im Klammern-Feld). Deshalb direkt `history.commit()` mit der Message, die der Plan
        vorschreibt: `rename-folder <space>:<old>→<new>` bzw. `rename-space <old>→<new>`.

        Wie `_commit()` ist der Aufruf **nie fatal**: `history.commit()` loggt selbst `critical`
        und wirft nie."""
        if self._git_enabled:
            history.commit(self._data_root, message, author=actor)

    @property
    def acl_reader(self) -> AclReader:
        """Der eine `AclReader`, den dieser `Store` selbst benutzt (P6 Step 5) — Aufrufer, die
        eine `AclDecision` außerhalb von `acl_of()` bauen müssen (z. B. `mcpserver.tools
        .search_items` für eine ganze Seite `ItemSummary`-Zeilen), teilen sich damit denselben
        `stat()`-invalidierten Cache statt einen zweiten, unabhängig veraltenden `AclReader`
        zu instanziieren."""
        return self._acl

    def acl_of(self, item_id: str) -> AclDecision:
        """Rechte eines Items, ausschließlich aus dem Index — liest die Item-DATEI NICHT
        (gleiche Eigenschaft wie `space_of()`, P2: sicher aufrufbar, BEVOR feststeht, ob der
        Zugriff überhaupt erlaubt ist).
        """
        with self._lock:
            row = index.get_item_row(self._conn, item_id)
        if row is None:
            raise ItemNotFound(item_id)
        space = row["space"]
        # Wie in `_row_to_item()`: aus dem Pfad abgeleitet, nicht aus `row["folder"]`
        # übernommen — reine Pfad-Arithmetik, kein Datei-Lesezugriff, verletzt also nicht den
        # "liest die Item-DATEI NICHT"-Vertrag oben.
        folder = files.folder_from_path(self._data_root, space, self._data_root / row["path"])
        return self._acl.decision_for(
            space=space, folder=folder, visibility=row["visibility"],
            share_read=json.loads(row["share_read_json"]),
            share_write=json.loads(row["share_write_json"]),
        )

    def space_of(self, item_id: str) -> str:
        """Space eines Items, ausschließlich über den Index. Schreibt nichts, liest keine Datei.
        Wird von der Autorisierungsschicht (P2) gebraucht, BEVOR entschieden ist, ob ein
        Zugriff überhaupt erlaubt ist — ein Rechtefehler darf den Store sonst nicht erreichen.
        """
        with self._lock:
            row = index.get_item_row(self._conn, item_id)
        if row is None:
            raise ItemNotFound(item_id)
        return row["space"]

    def links_all(self) -> list[tuple[str, str, str]]:
        """Phase 8 Block B Step B2 (P8-M): alle Item-Kanten aus dem Index.

        Liefert `[(src_id, dst_id, kind), ...]` für ALLE Items, ohne ACL-Filterung --
        der Aufrufer (`webui/api.py :: _graph_get`, Phase 8 Step B3) filtert die
        sichtbare Knotenmenge gegen `can_read_item_as_human` und blendet Kanten aus,
        deren Endpunkte unsichtbar sind (Plan §3 B3 ACL-Leck-Riegel). Sortierung:
        (src_id, kind, dst_id), deterministisch.

        Dangling `dst_id`-Eintraege (Notiz nennt eine ID, die nicht existiert) bleiben
        enthalten; dieselbe Filterung oben schneidet sie mit raus.
        """
        with self._lock:
            return [(r["src_id"], r["dst_id"], r["kind"]) for r in index.all_links(self._conn)]

    def search(
        self,
        query: str | None = None,
        *,
        space: str | None = None,
        spaces: list[str] | None = None,
        folder: str | None = None,
        type: str | None = None,
        status: str | None = None,
        tag: str | None = None,
        due_before: date | None = None,
        limit: int = 50,
        offset: int = 0,
        in_body: bool = False,
    ) -> SearchResult:
        with self._lock:
            rows = index.all_rows(self._conn)

        def read(row: sqlite3.Row) -> Item | None:
            # P10.5 15.6 (Fund B3′): eine von Hand kaputt editierte Datei (YAML, Kodierung,
            # Rechte) fehlt in der Suche, statt sie für alle zu sprengen — dieselbe Menge wie
            # `index._FILE_ERRORS` beim Neuaufbau, und wie dort mit `CRITICAL` und Pfad.
            try:
                return self._row_to_item(row)
            except FileNotFoundError:
                raise
            except (OSError, ValueError, KeyError, TypeError) as exc:
                # `exc.__class__`, nicht `type(exc)`: `type` ist hier der Filter-Parameter.
                logger.critical(
                    "Suche: %s uebersprungen — %s: %s", row["path"], exc.__class__.__name__, exc
                )
                return None

        items = []
        for r in rows:
            # P10.5 15.6 (Ultra-Review B10): die Dateien werden **nach** dem Lock gelesen — ein
            # paralleles Titel-Update benennt die Datei um, `trash()` verschiebt sie. Dann die
            # Zeile unter dem Lock neu holen: umbenannt ⇒ neuer Pfad, gelöscht ⇒ keine Zeile.
            # Das Lock über alle Lesezugriffe zu halten, sperrte jeden Writer für eine ganze
            # Suche — und eine von Hand gelöschte Datei hält sich ohnehin an kein Lock.
            try:
                item = read(r)
            except FileNotFoundError:
                with self._lock:
                    fresh = index.get_item_row(self._conn, r["id"])
                    try:
                        item = read(fresh) if fresh is not None else None
                    except FileNotFoundError:
                        item = None
            if item is not None:
                items.append(item)

        def matches(item: Item) -> bool:
            if space is not None and item.space != space:
                return False
            if spaces is not None and item.space not in spaces:
                return False
            if folder is not None and item.folder != folder:
                return False
            if type is not None and item.type != type:
                return False
            if status is not None and item.status != status:
                return False
            if tag is not None and tag not in item.tags:
                return False
            if due_before is not None and (item.due is None or item.due >= due_before):
                return False
            if query:
                # P6.5-N4: Body nur bei explizitem in_body=True — item.body ist über
                # _row_to_item() ohnehin schon geladen, kein zusätzlicher Datei-Zugriff.
                haystack = f"{item.title} {' '.join(item.tags)}"
                if in_body:
                    haystack += " " + item.body
                if query.lower() not in haystack.lower():
                    return False
            return True

        filtered = [i for i in items if matches(i)]
        filtered.sort(
            key=lambda i: (
                i.status != "open" and i.status != "active",
                i.due or date.max,
                -(i.updated.timestamp()),
            )
        )
        total = len(filtered)
        page = filtered[offset : offset + limit]
        return SearchResult(
            items=[_summary(i) for i in page], total=total, limit=limit, offset=offset,
        )

    def get(self, item_id: str, *, repair_drift: bool = True) -> Item:
        with self._lock, self._file_write_lock():
            row = self._reconcile_and_get_row(item_id, repair_drift=repair_drift)
            return self._row_to_item(row)

    def create(
        self,
        space: str,
        *,
        type: str,
        title: str,
        body: str = "",
        folder: str = "",
        # P9 Block trace (P9-AA/AD): der Akteur, aus dem `updated_by` und der Git-Autor
        # entstehen. **Optional** mit Default `""` — 294 Testaufrufe von `create()` ohne
        # Akteur bleiben sonst rot, und P9-AD hat genau das entschieden. Der Schutz gegen eine
        # vergessene Aufrufstelle ist ein Waechter ueber die Adapter (Plan §4 T7), nicht der Typ.
        actor: str = "",
        **fields,
    ) -> Item:

        with self._lock, self._file_write_lock():
            reserved = _SYSTEM_MANAGED_FIELDS & fields.keys()
            if reserved:
                raise ValidationError(f"Felder {sorted(reserved)} sind vom Store verwaltet")
            if not files.is_valid_space_name(space):
                # P10.5 15.5 (Ultra-Review B6): vorher schrieb `space="team/"` nach `team/`
                # mit `space: team/` im Frontmatter — das eigene Item galt danach als fremd.
                raise ValidationError(f"{space!r} ist kein gültiger Space-Name.")
            _check_write_types({"title": title, "body": body, **fields})
            _check_title_length(title)
            folder = files.validate_folder(folder)
            now = self._now_fn()
            status = fields.pop("status", _DEFAULT_STATUS.get(type, "active"))
            _check_type_and_status(type, status)
            if status == "archived":
                # Siebte Contract-Öffnung (P7 Step C4): `_write_item_file()` legt ein
                # archiviertes Item jetzt immer unter `_archive/` ab, unabhängig davon, ob es
                # `archive()` oder direkt `create(status="archived")` (z. B. `POST /api/v1/items`)
                # dorthin geschickt hat — dieselbe Zurücksetzung, die `archive()` selbst seit je
                # her vornimmt (`folder=""`), hier vorgezogen, damit das zurückgegebene `Item`
                # nie einen `folder`-Wert trägt, den der nächste `get()` ohnehin verwirft
                # (`folder` wird immer aus dem realen Pfad abgeleitet, nie aus dem Frontmatter).
                folder = ""
            due = _coerce_due(fields.pop("due", None))
            tags = fields.pop("tags", [])
            links = fields.pop("links", [])
            visibility = fields.pop("visibility", DEFAULT_VISIBILITY)
            if visibility not in VISIBILITY_VALUES:
                raise ValidationError(
                    f"Unbekannte visibility {visibility!r} — erlaubt: {sorted(VISIBILITY_VALUES)}"
                )
            share_read = fields.pop("share_read", [])
            share_write = fields.pop("share_write", [])
            # P9 Step F (F5): aus `fields` **heraus**poppen, damit es nicht zugleich in
            # `extra=fields` landet — sonst hätte das Item den Wert zweimal, einmal im Feld
            # und einmal im unbekannten-Schlüssel-Sack, und `_item_to_text` schriebe den
            # Extra-Wert über den Feld-Wert hinweg (`fields.update(item.extra)`).
            assignee = _coerce_assignee(fields.pop("assignee", ""))
            item = Item(
                id=files.generate_id(), space=space, type=type, title=title, status=status,
                body=body, due=due, tags=list(tags), links=list(links),
                created=now, updated=now, version=1, folder=folder,
                visibility=visibility, share_read=list(share_read), share_write=list(share_write),
                assignee=assignee,
                # P9 Block trace: das Anlegen **ist** der erste Schreibvorgang, es gibt keinen
                # Vorgaenger, dessen `updated_by` bleiben koennte — der Wert kommt allein aus
                # dem Akteur (leer = unbekannt, dann steht das Feld gar nicht in der Datei).
                updated_by=actor,
                # P10.5 Block 9 (RE-7): das Anlegen ist der einzige Moment, in dem es einen
                # "Ersteller" gibt — danach aendert sich der Wert **nie** (kein Schreibweg
                # aendert ihn: `update`/`append`/`patch`/`move`/`archive`/`trash` benutzen alle
                # `replace(current, ...)`, das den alten Wert mitnimmt). Leer heisst
                # "unbekannt" (Operator-Skript ohne Akteur) — dann steht das Feld **gar nicht**
                # in der Datei (P10.5-W: kein erfundenes Leerfeld).
                created_by=actor,
                extra=fields,
            )
            self._write_item_file(item, old_path=None, op="create", actor=actor)
            return item

    def update(self, item_id: str, *, version: int, actor: str = "", **changes) -> Item:
        """**`actor` (P9 Block trace) ist ein reservierter Name**, kein Frontmatter-Feld: wer
        `update(id, version=1, actor="x")` ruft, setzt `updated_by` und legt **kein** Feld `actor`
        in die Datei an. Ein Item mit einem echten, von Hand gesetzten Frontmatter-Feld `actor`
        kann damit nicht mehr geschrieben werden — der Trade-off ist bewusst (P9-AD, gleiche
        Form wie der Langzeit-Default bei `now_fn`) und betrifft kein Feld, das je in diesem
        Repo verwendet wurde. `create()` hat dieselbe Eigenschaft mit `**fields`."""

        with self._lock, self._file_write_lock():
            row = self._reconcile_and_get_row(item_id)
            current = self._row_to_item(row)
            if current.version != version:
                raise ConflictError(item_id, expected_version=version, current=current)
            if current.status == "archived":
                raise ValidationError(f"Item {item_id} ist archiviert — update verboten")

            old_path = self._data_root / row["path"]
            updated_extra = dict(current.extra)
            known_updatable = {"type", "title", "status", "body", "due", "tags", "links"}
            _check_write_types(changes)
            if "title" in changes and changes["title"] != current.title:
                # Nur ein **geänderter** Titel: die UI schickt ihn bei jedem Speichern mit, ein
                # von Hand verlängerter Titel bliebe sonst unspeicherbar.
                _check_title_length(changes["title"])
            kwargs: dict[str, Any] = {}
            for key, value in changes.items():
                if key in _SYSTEM_MANAGED_FIELDS:
                    raise ValidationError(f"Feld '{key}' ist vom Store verwaltet, nicht änderbar")
                if key == "due":
                    kwargs["due"] = _coerce_due(value)
                elif key == "folder":
                    # `Store.update()` erlaubt das Setzen -- die Sperre für Agenten
                    # (visibility/share_read/share_write) sitzt eine Schicht höher in
                    # `mcpserver.tools.update_item` (P6-M), nicht hier (`folder` selbst ist
                    # nicht gesperrt, Agenten dürfen Items in Ordner verschieben).
                    kwargs["folder"] = files.validate_folder(value)
                elif key == "visibility":
                    if value not in VISIBILITY_VALUES:
                        raise ValidationError(
                            f"Unbekannte visibility {value!r} — erlaubt: {sorted(VISIBILITY_VALUES)}"
                        )
                    kwargs["visibility"] = value
                elif key in ("share_read", "share_write"):
                    kwargs[key] = list(value)
                elif key == "assignee":
                    # P9 Step F (F11): **nicht im Plan §8.2 genannt und trotzdem Pflicht.**
                    # `assignee` steht nicht in `known_updatable`, also *würde* es ohne diese
                    # Zweig in den `else`-Zweig fallen und damit in `updated_extra` — es ginge
                    # über `fields.update(item.extra)` trotzdem in die Datei, aber `item.assignee`
                    # bliebe dabei auf "" stehen. Zwei Quellen für ein Feld, von denen eine
                    # schweigt: F6 (`if item.assignee`) feuierte nie, `get()` und `search()`
                    # widersprächen sich. Der Zweig ist der Grund, warum "es funktioniert" hier
                    # kein ausreichender Beweis war — der Wert landete ja scheinbar richtig.
                    kwargs["assignee"] = _coerce_assignee(value)
                elif key in known_updatable:
                    kwargs[key] = value
                else:
                    updated_extra[key] = value

            _check_type_and_status(
                kwargs.get("type", current.type), kwargs.get("status", current.status)
            )

            new_item = replace(
                current,
                **kwargs,
                extra=updated_extra,
                version=current.version + 1,
                updated=self._now_fn(),
                # P9 Block trace (P9-AB): **leerer Akteur heisst unveraendert, nicht leer.**
                # Genau die Entscheidung, die einen erfundenen (falschen) Eintrag in der
                # Historie verhindert — ein Item, das ein Operator-Skript ohne Akteur anfasst,
                # behaelt den Namen des letzten *bekannten* Editors. Und weil
                # `_item_to_text()` nur bei nicht-leerem Wert schreibt, entsteht fuer einen
                # Altbestand-Item ohne Feld dadurch auch **keine** leere Zeile (Test 4).
                updated_by=actor or current.updated_by,
            )
            self._write_item_file(new_item, old_path=old_path, op="update", actor=actor)
            return new_item

    def append(self, item_id: str, *, version: int, text: str, actor: str = "") -> Item:
        with self._lock, self._file_write_lock():
            row = self._reconcile_and_get_row(item_id)
            current = self._row_to_item(row)
            if current.version != version:
                raise ConflictError(item_id, expected_version=version, current=current)
            if current.status == "archived":
                raise ValidationError(f"Item {item_id} ist archiviert — append verboten")

            old_path = self._data_root / row["path"]
            separator = "\n" if current.body and not current.body.endswith("\n") else ""
            new_item = replace(
                current,
                body=current.body + separator + text,
                version=current.version + 1,
                updated=self._now_fn(),
                updated_by=actor or current.updated_by,
            )
            self._write_item_file(new_item, old_path=old_path, op="append", actor=actor)
            return new_item

    def patch(
        self, item_id: str, *, version: int, edits: Sequence[TextEdit], actor: str = ""
    ) -> PatchResult:
        """Ersetzt exakte Textstellen im Body, ohne ihn komplett neu zu schreiben (P6-E).
        Reihenfolge wie `update`/`append`, mit einem zusätzlichen Schritt: `apply_edits()`
        läuft auf einer Kopie des Bodys, **bevor** irgendetwas geschrieben wird — ein
        `PatchError` (Treffer ≠ 1) verlässt diese Methode, ohne dass Datei, Index oder Version
        angefasst wurden.
        """
        with self._lock, self._file_write_lock():
            row = self._reconcile_and_get_row(item_id)
            current = self._row_to_item(row)
            if current.version != version:
                raise ConflictError(item_id, expected_version=version, current=current)
            if current.status == "archived":
                raise ValidationError(f"Item {item_id} ist archiviert — patch verboten")

            old_path = self._data_root / row["path"]
            bytes_before = len(current.body.encode("utf-8"))
            new_body, lines = apply_edits(current.body, edits)
            bytes_after = len(new_body.encode("utf-8"))

            new_item = replace(
                current, body=new_body, version=current.version + 1, updated=self._now_fn(),
                updated_by=actor or current.updated_by,
            )
            self._write_item_file(new_item, old_path=old_path, op="patch", actor=actor)
            return PatchResult(
                item=new_item, replacements=len(edits), lines=lines,
                bytes_before=bytes_before, bytes_after=bytes_after,
            )

    def archive(self, item_id: str, *, version: int, actor: str = "") -> Item:
        with self._lock, self._file_write_lock():
            row = self._reconcile_and_get_row(item_id)
            current = self._row_to_item(row)
            if current.version != version:
                raise ConflictError(item_id, expected_version=version, current=current)

            old_path = self._data_root / row["path"]
            new_item = replace(
                current, status="archived", folder="",
                version=current.version + 1, updated=self._now_fn(),
                updated_by=actor or current.updated_by,
            )
            slug = files.slugify(new_item.title)
            archive_path = (
                self._data_root / new_item.space / "_archive" / files.item_filename(new_item.id, slug)
            )
            files.atomic_write(old_path, _item_to_text(new_item))
            files.move_file(old_path, archive_path)
            row2 = index.row_from_file(self._data_root, archive_path)
            index.upsert_item(self._conn, row2)
            self._commit("archive", new_item.id, new_item.space, actor)
            return new_item

    def move(
        self,
        item_id: str,
        *,
        version: int,
        space: str | None = None,
        folder: str | None = None,
        actor: str = "",
    ) -> Item:
        """Verschiebt ein Item in einen anderen Space und/oder Ordner (P6-AD,
        `phase6_shares/ITEM_MOVE_PLAN.md` §4.1). Eigene Methode statt eines `space=`-Feldes an
        `update()` — `space` bleibt in `_SYSTEM_MANAGED_FIELDS`, derselbe Schutz, der den
        Divergenz-Fund B2 der P2-Adapter-Abnahme (Verzeichnis sagt `niklas`, Frontmatter sagt
        `nikinger`) verhindert. Genau ein Git-Commit (`move <id> [<ziel-space>]` über
        `_write_item_file()`s bestehenden `_commit()`-Aufruf), genau ein Versionssprung.
        Autorisierung passiert NICHT hier (wie überall im Store) — Aufrufer prüfen Rechte VOR
        diesem Call (P6-AE: Schreibrecht auf Quelle UND Ziel).

        **P7 Step C4, siebte Contract-Öffnung:** ein archiviertes Item darf per Space-Wechsel
        bewegt werden (kein `folder=` außer `""`) — `_write_item_file()` legt es dabei ins
        Ziel-`_archive/`, nicht an die Space-Wurzel. Ein echter Ordner-Wechsel bleibt für
        archivierte Items verboten (ihr `folder` ist immer `""`).
        """
        with self._lock, self._file_write_lock():
            row = self._reconcile_and_get_row(item_id)
            current = self._row_to_item(row)
            if current.version != version:
                raise ConflictError(item_id, expected_version=version, current=current)
            if current.status == "archived" and folder not in (None, ""):
                # Siebte Contract-Öffnung (P7 Step C4, N8): ein archiviertes Item bleibt ein
                # reiner Space-Wechsel-Kandidat — sein `folder` ist immer "" (archive() erzwingt
                # das), ein ECHTER Ordner-Wechsel ergibt für ein Item ohne Ordnerposition keinen
                # Sinn und bleibt verboten. Ein reiner Space-Move (kein `folder=`, oder explizit
                # `folder=""`) ist dagegen ab jetzt erlaubt — vorher unterschiedslos verboten,
                # was einen Space mit Historie (`_archive/`-Inhalt) strukturell unentfernbar
                # machte (P7-20-Fund, `docs/concepts/phase7_spaces_admin_plan.md` §4.C4).
                raise ValidationError(
                    f"Item {item_id} ist archiviert — Ordner-Wechsel verboten (Space-Wechsel "
                    "erlaubt)"
                )

            old_path = self._data_root / row["path"]
            target_space = current.space
            if space is not None:
                if not files.is_valid_space_name(space):
                    # P10.5 15.5 (B6): `(root / "team/").is_dir()` ist wahr — die Existenzprüfung
                    # darunter hält `team/` allein nicht auf.
                    raise ValidationError(f"{space!r} ist kein gültiger Space-Name.")
                # Explizite Prüfung statt `_write_item_file()`s `mkdir(parents=True)` beiläufig
                # entscheiden zu lassen — sonst macht ein Tippfehler im Zielnamen aus Versehen
                # einen neuen, rechtefreien Space (§4.1 Punkt 2).
                if not (self._data_root / space).is_dir():
                    raise ValidationError(
                        f"Ziel-Space {space!r} existiert nicht — move legt keinen neuen Space an"
                    )
                target_space = space

            if folder is not None:
                target_folder = files.validate_folder(folder)
            elif space is not None:
                # Space-Wechsel ohne folder=: Ziel ist die Space-Wurzel, NICHT der gleichnamige
                # Ordner im Zielspace — ein Ordnername bedeutet dort etwas anderes und trägt
                # potenziell eine andere `.share.yml` (§4.1 Punkt 3).
                target_folder = ""
            else:
                target_folder = current.folder

            new_item = replace(
                current, space=target_space, folder=target_folder,
                version=current.version + 1, updated=self._now_fn(),
                updated_by=actor or current.updated_by,
            )
            # P6.5-T: das Asset-Verzeichnis zieht mit, BEVOR `_write_item_file()` committet —
            # ein Move erzeugt weiterhin genau einen Git-Commit (P6-Abnahmezeile 26s Mechanik).
            files.move_asset_dir(
                files.asset_dir(self._data_root, current.space, current.id),
                files.asset_dir(self._data_root, target_space, current.id),
            )
            self._write_item_file(new_item, old_path=old_path, op="move", actor=actor)
            self._cleanup_emptied_folders(old_path.parent, current.space)
            return new_item

    def _cleanup_emptied_folders(self, folder_dir: Path, space: str) -> None:
        """P6-AF: nach einem Move leer gewordene Quellordner aufräumen, aufwärts bis maximal zur
        Space-Wurzel. Abbruch bei einer `.share.yml` (eine bewusste Freigabe eines Menschen ist
        kein Rest — sie wegzuräumen würde eine Rechteeinstellung als Nebenwirkung eines Moves
        löschen) oder einem nicht-leeren Verzeichnis. Reine Aufräum-Nebenwirkung ohne eigenen
        Git-Commit, dieselbe Kategorie wie `ensure_folder()`.
        """
        space_root = self._data_root / space
        current = folder_dir
        while space_root in current.parents:
            if (current / ACL_FILENAME).exists():
                break
            try:
                if any(current.iterdir()):
                    break
                current.rmdir()
            except OSError:
                break
            current = current.parent

    def put_asset(
        self, item_id: str, *, data: bytes, filename: str | None = None, actor: str = ""
    ) -> AssetInfo:
        """Legt ein Bild unter `<space>/_assets/<item_id>/` ab (P6.5-T, fünfte Contract-
        Öffnung). Kein `version`-Parameter — Assets sind nicht Teil der Item-Versionierung,
        ein Upload konkurriert nie mit einem Text-Write um dieselbe `version`.

        `actor` (P9 Block trace) wandert **ausschließlich** an den Git-Autor. Ein Bild-Upload
        fasst den Item-Text nicht an und setzt `updated_by` deshalb **nicht** — die Versions-
        und Frontmatter-Wahrheit des Items bleibt die des letzten echten Text-Writes. Wer ein
        Bild hochlaedt, will im Git-Log stehen, nicht im Item-Header."""
        with self._lock, self._file_write_lock():
            row = self._reconcile_and_get_row(item_id, repair_drift=False)
            space = row["space"]
            sniffed = files.sniff_image_mime(data)
            if sniffed is None:
                raise ValidationError(
                    "Unbekanntes oder nicht unterstütztes Bildformat — erlaubt: "
                    "PNG/JPEG/GIF/WebP"
                )
            mime, ext = sniffed
            # **P10.5, Block 3 (LG-8, P1-Öffnung 15):** die Metadaten fliegen raus, **bevor**
            # die Datei auf die Platte kommt (GPS, Kameratyp, XMP, IPTC, PNG-Textfelder). Reine
            # Byte-Chirurgie in `files.strip_image_metadata()` — kein Bild wird neu kodiert, ein
            # Bild ohne Metadaten bleibt byte-identisch. Die Orientation bleibt erhalten, sonst
            # stünden Handyfotos nach dem Hochladen quer.
            # **Eine** Stelle für beide Flächen: Web-Upload (`webui/api.py :: _assets_post()`)
            # und `put_item_asset` laufen beide hier durch — kein zweiter Pfad, der die
            # Bereinigung vergessen könnte.
            # Fail-closed: eine Struktur, die der Stripper nicht versteht, ergibt
            # `ValidationError` — **vor** dem Schreiben, nie danach.
            data = files.strip_image_metadata(data, mime)
            asset_id = files.new_asset_id()
            target_dir = files.asset_dir(self._data_root, space, item_id)
            target_dir.mkdir(parents=True, exist_ok=True)
            path = files.asset_path(self._data_root, space, item_id, asset_id, ext)
            files.atomic_write_bytes(path, data)
            self._commit("asset", item_id, space, actor)
            # `created` kommt aus der Datei-mtime, nicht aus `self._now_fn()` — nichts
            # persistiert den Upload-Zeitpunkt separat, also muss put_asset() dieselbe Quelle
            # liefern, die list_assets() beim nächsten Listing sieht (Advisor-Fund, sonst
            # zeigen dieselbe Asset zwei verschiedene `created`-Werte).
            created = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
            return AssetInfo(
                id=asset_id, mime=mime, bytes=len(data),
                filename=filename or "", created=created,
            )

    def list_assets(self, item_id: str) -> list[AssetInfo]:
        """Kein Index-Eintrag für Assets (P6-AY) — direktes Verzeichnis-Listing.
        `_trash/` wird übersprungen (verschobene, „entfernte" Assets, N5)."""
        with self._lock, self._file_write_lock():
            row = self._reconcile_and_get_row(item_id, repair_drift=False)
            target_dir = files.asset_dir(self._data_root, row["space"], item_id)
            if not target_dir.is_dir():
                return []
            result = []
            for path in sorted(target_dir.iterdir()):
                if path.name == "_trash" or not path.is_file():
                    continue
                asset_id = path.stem
                if not files.ASSET_ID_RE.match(asset_id):
                    continue
                # Nur die für sniff_image_mime() nötigen ersten 12 Bytes lesen (WebPs
                # Offset-8-Prüfung ist der längste Fall) — ein Listing darf nicht jedes Bild
                # vollständig einlesen, das widerspräche get_item_metas eigenem Versprechen
                # "um Größenordnungen billiger" (Advisor-Fund).
                with path.open("rb") as f:
                    sniffed = files.sniff_image_mime(f.read(12))
                mime = sniffed[0] if sniffed is not None else ""
                stat = path.stat()
                result.append(AssetInfo(
                    id=asset_id, mime=mime, bytes=stat.st_size, filename="",
                    created=datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc),
                ))
            return result

    @staticmethod
    def _asset_matches(target_dir: Path, asset_id: str) -> list[Path]:
        """Die EINE Stelle, an der eine `asset_id` zu Dateien wird (Ultra-Review B1/B15,
        2026-10-30). Ohne die Formprüfung ging die ID roh in `Path.glob()`: `..` ist dort ein
        normales Segment (Lesen/Verschieben beliebiger Dateien des Dienstnutzers), `*` liefert
        das erste Asset. Eine **formfalsche** ID ist hier schlicht „nicht gefunden" — dieselbe
        `ItemNotFound`-Antwort wie bei einer unbekannten, die Adapter bilden sie unverändert auf
        `asset_not_found` / 404 ab, und es gibt kein Orakel, das beide Fälle unterscheidet.
        Nach der Prüfung enthält die ID kein Glob-Metazeichen und kein Pfadtrennzeichen mehr."""
        if not files.ASSET_ID_RE.match(asset_id):
            raise ItemNotFound(asset_id)
        return list(target_dir.glob(f"{asset_id}.*")) if target_dir.is_dir() else []

    def get_asset(self, item_id: str, asset_id: str) -> tuple[bytes, str]:
        """Bytes + MIME — die MIME kommt erneut aus den Magic Bytes, nicht aus der
        Dateiendung (dieselbe Nie-der-Endung-vertrauen-Regel wie beim Upload)."""
        with self._lock, self._file_write_lock():
            row = self._reconcile_and_get_row(item_id, repair_drift=False)
            target_dir = files.asset_dir(self._data_root, row["space"], item_id)
            matches = self._asset_matches(target_dir, asset_id)
            if not matches:
                raise ItemNotFound(asset_id)
            data = matches[0].read_bytes()
            sniffed = files.sniff_image_mime(data)
            mime = sniffed[0] if sniffed is not None else "application/octet-stream"
            return data, mime

    def delete_asset(self, item_id: str, asset_id: str, actor: str = "") -> None:
        """„Verschieben statt Entfernen" (N5, gelockt): das Bild landet in `_trash/`,
        Entscheidung H (kein Hard-Delete im Kern-API) bleibt formal unangetastet. Die
        Body-Referenz läuft danach ins Leere und rendert als Alt-Text — kein Rewrite des
        Bodys hier, das ist Aufgabe der aufrufenden Schicht, falls gewünscht. Wie `put_asset()`
        nur Git-Autor, kein `updated_by` (P9 Block trace)."""
        with self._lock, self._file_write_lock():
            row = self._reconcile_and_get_row(item_id, repair_drift=False)
            space = row["space"]
            target_dir = files.asset_dir(self._data_root, space, item_id)
            matches = self._asset_matches(target_dir, asset_id)
            if not matches:
                raise ItemNotFound(asset_id)
            trash_dir = target_dir / "_trash"
            trash_dir.mkdir(parents=True, exist_ok=True)
            files.move_file(matches[0], trash_dir / matches[0].name)
            self._commit("asset_trash", item_id, space, actor)

    def trash(self, item_id: str, *, version: int, actor: str = "") -> None:
        """P9 Step G (P9-I, P9-J, P9-K): **Löschen heißt Verschieben nach `._trash/`, nie
        `unlink`** — derselbe Präzedenzfall wie `delete_asset()` (N5), mit dem Unterschied, dass
        dort die Unsichtbarkeit aus einem expliziten `if path.name == "_trash"` im Asset-Listing
        kommt und hier aus dem Punkt-Präfix am DATA_ROOT (siehe `TRASH_DIR`).

        **`version` ist Pflicht** (Hard Rule 3): Löschen ist der Write, bei dem ein verlorener
        Konflikt am teuersten ist — der Kalender-`If-Match` schützt nur Felder, hier schützt er
        die Entscheidung „das wollte ich löschen, in dieser Fassung". Genau wie `archive()`.

        Zurück kommt **nichts** (`-> None`, im Gegensatz zu `archive()`): es gibt keinen
        wiederherstellbaren Zustand, das Item existiert danach nicht mehr — P9-J nennt das
        ausdrücklich („kein API-Endpunkt, der `_trash/` listet, keine Wiederherstellung in der
        UI"). Wer es zurückholen will, geht über Git bzw. das Dateisystem.

        **Die Asset-Dateien des Items wandern nicht mit.** Bewusst, nicht vergessen: sie liegen
        danach unerreichbar unter `<space>/_assets/<item_id>/` (ohne Index-Zeile findet
        `list_assets()` sie nicht mehr), und ein zweiter Move würde aus einer atomaren Operation
        zwei halbe machen. Der Aufräum-Posten dafür ist benannt (V162), nicht gebaut.

        Autorisierung passiert **nicht** hier, wie überall im Store — der Aufrufer prüft Rechte
        VOR dem Aufruf (`api.py :: _items_delete`, P9-K: nur eigene, schreibbare Items).

        **`actor` (P9 Block trace) setzt `updated_by` nicht** — die Datei wird hier nicht neu
        geschrieben, sie wandert nur. Im Papierkorb steht deshalb der letzte Editor des Items,
        waehrend der Loeschende als Git-Autor auftaucht. Das ist die eine Stelle, an der die
        beiden Spuren auseinanderlaufen, und es ist so gewollt: `updated_by` ist eine Aussage
        ueber den **Inhalt**, und der Inhalt wurde hier von niemandem geaendert. Nicht
        nachbessern.
        """
        with self._lock, self._file_write_lock():
            row = self._reconcile_and_get_row(item_id)
            current = self._row_to_item(row)
            if current.version != version:
                raise ConflictError(item_id, expected_version=version, current=current)

            old_path = self._data_root / row["path"]
            trash_path = (
                self._data_root / TRASH_DIR / current.space
                / files.item_filename(current.id, files.slugify(current.title))
            )
            # Reihenfolge ist die ganze Fehlerklasse: erst der atomare Move, dann der Index.
            # Umgekehrt gäbe es ein Fenster, in dem die Datei im Papierkorb liegt, der Index aber
            # noch ein Item führt — `get()` fände eine Datei, die es nicht mehr gibt. `move_file`
            # macht `os.replace` + Verzeichnis-fsync auf Quelle **und** Ziel (Hard Rule 5).
            files.move_file(old_path, trash_path)
            # `delete_item()` räumt auch die ausgehenden `item_links`-Zeilen mit dieser `src_id`
            # auf. **Eingehende** Kanten (`dst_id` == dieses Item) bleiben als dangling stehen —
            # dieselbe Entscheidung wie bei Assets und bei `delete_item()`s Docstring: die API
            # filtert sie beim Lesen, `_graph_get` verlangt für eine Kante, dass **beide**
            # Endpunkte in der sichtbaren Knotenmenge sind, und die kommt aus `search()`.
            index.delete_item(self._conn, item_id)
            self._commit("trash", item_id, current.space, actor)

    def rebuild_index(self) -> IndexStats:
        with self._lock:
            return index.rebuild_index(self._data_root, self._conn)
