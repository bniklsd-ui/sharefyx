#!/usr/bin/env python3
"""Space-CLI — Plan §4 Step 7, "die CLI als Beweis". Dünner Aufruf-Wrapper um `storage.Store`,
komplett offline (kein Netz, kein MCP — das ist Phase 2). Logging nach stderr; Ausgabe wahlweise
Text (Standard) oder `--json` auf stdout.

Kein Contract für spätere Phasen — anders als `storage`s öffentliche API (Plan §2) ist dieses
Skript reine Präsentationsschicht und darf sich jederzeit ändern, ohne dass das eine
Scope-Änderung wäre.
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
from dataclasses import asdict
from datetime import date, datetime, timezone
from pathlib import Path

from storage import errors
from storage.models import IndexStats, Item, SearchResult, SpaceInfo
from storage.store import Store

# Exit-Codes: 0 Erfolg, 1 sonstiger Store-Fehler, 2 Konflikt (unterscheidbar, damit ein
# aufrufendes Skript "stale, neu lesen und retry" von "kein solches Item" trennen kann).
EXIT_OK = 0
EXIT_ERROR = 1
EXIT_CONFLICT = 2


def _json_default(value):
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if isinstance(value, date):
        return value.isoformat()
    raise TypeError(f"Nicht JSON-serialisierbar: {type(value)!r}")


def _dump_json(obj) -> str:
    return json.dumps(asdict(obj), default=_json_default, ensure_ascii=False, indent=2)


# -- Text-Ausgabe ---------------------------------------------------------------------------


def _print_item_text(item: Item) -> None:
    print(f"{item.id}  [{item.space}]  {item.type}  v{item.version}  status={item.status}")
    print(f"  Titel: {item.title}")
    if item.due is not None:
        print(f"  Fällig: {item.due.isoformat()}")
    if item.tags:
        print(f"  Tags: {', '.join(item.tags)}")
    if item.links:
        print(f"  Links: {', '.join(item.links)}")
    print(f"  Aktualisiert: {item.updated.isoformat()}")
    if item.body:
        print("  ---")
        print(item.body)


def _print_spaces_text(spaces: list[SpaceInfo]) -> None:
    if not spaces:
        print("Keine Spaces.")
        return
    for space in spaces:
        print(f"{space.name}: {space.item_count} Item(s)")


def _print_search_text(result: SearchResult) -> None:
    print(f"{result.total} Treffer (zeige {len(result.items)}, offset={result.offset}, limit={result.limit})")
    for summary in result.items:
        due = f"  fällig={summary.due.isoformat()}" if summary.due is not None else ""
        tags = f"  tags={','.join(summary.tags)}" if summary.tags else ""
        print(f"  {summary.id}  [{summary.space}]  {summary.status}{due}{tags}  {summary.title}")
        if summary.snippet:
            print(f"    {summary.snippet}")


def _print_stats_text(stats: IndexStats) -> None:
    print(f"Reindiziert: {stats.items_indexed} Item(s) in {stats.duration_seconds:.3f}s")


def _print_conflict(exc: errors.ConflictError) -> None:
    print(
        f"Konflikt bei {exc.item_id}: erwartete Version {exc.expected_version}, "
        f"aktuell {exc.current.version}",
        file=sys.stderr,
    )
    print(f"  Aktueller Titel:      {exc.current.title!r}", file=sys.stderr)
    print(f"  Aktueller Status:     {exc.current.status}", file=sys.stderr)
    print(f"  Zuletzt aktualisiert: {exc.current.updated.isoformat()}", file=sys.stderr)


# -- Argumente --------------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="space_cli", description="Manuelles CLI-Werkzeug für den Storage-Kern (Phase 1)."
    )
    parser.add_argument("--data-root", required=True, type=Path, help="DATA_ROOT-Verzeichnis")
    sub = parser.add_subparsers(dest="command", required=True)

    # `--json` lebt nur auf den Subcommand-Parsern (nicht zusätzlich auf dem Top-Level-Parser)
    # -- sonst würde argparse beim Subparsing seinen eigenen Default erneut in den gemeinsamen
    # Namespace schreiben und einen vor dem Subcommand übergebenen `--json` stumm zurücksetzen.
    # Das erlaubt `search --json` (natürliche Position, wie bei den meisten CLIs), nicht nur
    # `--json search` (davor, wie beim ersten Wurf hier -- per manuellem Smoke-Test gefunden).
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        "--json", action="store_true", help="Maschinenlesbare Ausgabe auf stdout statt Text"
    )

    p_create = sub.add_parser("create", parents=[common])
    p_create.add_argument("space")
    p_create.add_argument("--type", required=True, choices=["note", "task"])
    p_create.add_argument("--title", required=True)
    p_create.add_argument("--body", default="")
    p_create.add_argument("--tag", action="append", dest="tags", default=[])
    p_create.add_argument("--due")
    p_create.add_argument("--link", action="append", dest="links", default=[])

    sub.add_parser("list", parents=[common])

    p_search = sub.add_parser("search", parents=[common])
    p_search.add_argument("query", nargs="?")
    p_search.add_argument("--space")
    p_search.add_argument("--type")
    p_search.add_argument("--status")
    p_search.add_argument("--tag")
    p_search.add_argument("--due-before")
    p_search.add_argument("--limit", type=int, default=50)
    p_search.add_argument("--offset", type=int, default=0)

    p_show = sub.add_parser("show", parents=[common])
    p_show.add_argument("item_id")

    # Statusübergänge sind auf CLI-Ebene bewusst auf bekannte Werte begrenzt. `Store.update()`
    # selbst validiert `status` nicht (Plan §2 kennt keine Statuswert-Prüfung) -- ohne `choices`
    # hier würde die CLI zum Einfallstor für z.B. `status: bogus`, das die Sortierung in
    # `search()` dann still als "nicht offen" einsortiert. Eine echte Store-seitige Validierung
    # wäre eine §2-Contract-Änderung und damit Nikinger-Sache, hier nur vermerkt, nicht gefixt.
    _status_choices = ["open", "done", "active", "archived"]

    p_update = sub.add_parser("update", parents=[common])
    p_update.add_argument("item_id")
    p_update.add_argument("--version", required=True, type=int)
    p_update.add_argument("--title")
    p_update.add_argument("--status", choices=_status_choices)
    p_update.add_argument("--body")
    p_update.add_argument("--due")
    p_update.add_argument("--tag", action="append", dest="tags")
    p_update.add_argument("--link", action="append", dest="links")

    p_archive = sub.add_parser("archive", parents=[common])
    p_archive.add_argument("item_id")
    p_archive.add_argument("--version", required=True, type=int)

    sub.add_parser("reindex", parents=[common])

    return parser


def _parse_due_before(value: str | None) -> date | None:
    return date.fromisoformat(value) if value else None


# -- Dispatch ---------------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(stream=sys.stderr, level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    args = build_parser().parse_args(argv)
    store = Store(args.data_root)

    try:
        if args.command == "create":
            item = store.create(
                args.space, type=args.type, title=args.title, body=args.body,
                tags=args.tags or [], links=args.links or [], due=args.due,
            )
            if args.json:
                print(_dump_json(item))
            else:
                _print_item_text(item)

        elif args.command == "list":
            spaces = store.list_spaces()
            if args.json:
                print(json.dumps([asdict(s) for s in spaces], ensure_ascii=False, indent=2))
            else:
                _print_spaces_text(spaces)

        elif args.command == "search":
            result = store.search(
                args.query, space=args.space, type=args.type, status=args.status,
                tag=args.tag, due_before=_parse_due_before(args.due_before),
                limit=args.limit, offset=args.offset,
            )
            if args.json:
                print(_dump_json(result))
            else:
                _print_search_text(result)

        elif args.command == "show":
            item = store.get(args.item_id)
            if args.json:
                print(_dump_json(item))
            else:
                _print_item_text(item)

        elif args.command == "update":
            changes = {
                key: value
                for key, value in {
                    "title": args.title, "status": args.status, "body": args.body,
                    "due": args.due, "tags": args.tags, "links": args.links,
                }.items()
                if value is not None
            }
            item = store.update(args.item_id, version=args.version, **changes)
            if args.json:
                print(_dump_json(item))
            else:
                _print_item_text(item)

        elif args.command == "archive":
            item = store.archive(args.item_id, version=args.version)
            if args.json:
                print(_dump_json(item))
            else:
                _print_item_text(item)

        elif args.command == "reindex":
            stats = store.rebuild_index()
            if args.json:
                print(_dump_json(stats))
            else:
                _print_stats_text(stats)

    except errors.ConflictError as exc:
        _print_conflict(exc)
        return EXIT_CONFLICT
    except errors.SpaceError as exc:
        print(f"Fehler: {exc}", file=sys.stderr)
        return EXIT_ERROR

    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
