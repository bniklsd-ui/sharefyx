#!/usr/bin/env python3
"""Operator-Werkzeug für Spaces und Freigaben (Plan §4 Step 6) — dünne Unterbefehle direkt auf
dem Dateisystem unter DATA_ROOT, gleiche Bauart wie `phase4_auth/scripts/authctl.py`: ein
Unterbefehl, eine bereits vorhandene Grundoperation, kein neuer Layer darüber. Freigaben sind
Daten auf der Platte, nicht Code (Hard Rule 4, P6-T) — dieses Skript ist der eine vorgesehene
Weg, sie zu ändern, neben der (aktuell abgeschalteten, P6-V) UI. Kein MCP-Tool kann `.share.yml`
je berühren (P6-M).

DATA_ROOT: `--data-root` hat Vorrang, sonst `SPACE_DATA_ROOT` (Pflicht, kein stiller Fallback
ins Arbeitsverzeichnis) — dieselbe Haltung wie `authserver.config.resolve_db_path()` für
`authctl.py`, nur für ein Verzeichnis statt eine SQLite-Datei. **Plan-Korrektur, dieser Commit:**
der Plan-Satz „STATE_DIRECTORY-Konvention wie authctl.py" ist wörtlich genommen unpassend —
`STATE_DIRECTORY` trägt in der echten Unit nur die Auth-DB (`phase4_auth/systemd/
sharefyx-mcp.service :: StateDirectory=sharefyx`), DATA_ROOT kommt dort über eine eigene, direkt
gesetzte `Environment=SPACE_DATA_ROOT=...`-Zeile, ganz unabhängig von `StateDirectory`. Gemeint
war die Haltung („aus der Umgebung auflösen, kein stiller Fallback"), nicht die wörtliche
Variable — hier entsprechend mit `SPACE_DATA_ROOT` umgesetzt.

Schreibende Unterbefehle (`create-space`/`add-member`/`remove-member`/`remove-space`) rufen seit
P7 Step C1 `storage.acl`s Schreibfunktionen auf (`read_share_file`/`add_member`/`remove_member`/
`create_space`/`remove_space_dir`/`spaces_referencing`) — dieses Skript hält den `.write.lock`
selbst nicht mehr, `acl.py` nimmt ihn je Aufruf selbst und gibt ihn vor der Rückkehr wieder frei
(P7-M: zwei `open()` auf dieselbe Lock-Datei im selben Prozess blockieren einander). Das
serialisiert diese Schreibvorgänge weiterhin gegen einen parallel laufenden Dienst über
Prozessgrenzen hinweg, exakt wie `history.commit()`s Docstring es verlangt.

Ausgabe: Text auf stdout (Unterbefehle mit `--json` liefern zusätzlich maschinenlesbares JSON),
Logs/Fehler auf stderr (Hard Rule 7).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import yaml

from storage import acl
from storage.acl import ACL_FILENAME
from storage.store import Store

EXIT_OK = 0
EXIT_ERROR = 1


def _resolve_data_root(args_value: str | None, env: dict[str, str]) -> Path:
    if args_value:
        return Path(args_value)
    raw = env.get("SPACE_DATA_ROOT")
    if not raw:
        raise ValueError(
            "DATA_ROOT fehlt: weder --data-root übergeben noch SPACE_DATA_ROOT gesetzt "
            "(kein stiller Fallback ins Arbeitsverzeichnis)"
        )
    return Path(raw)


def _is_known_space(data_root: Path, name: str) -> bool:
    return (data_root / name).is_dir()


def _load_share_file(path: Path) -> dict:
    """Wie `AclReader._parse`, aber laut statt fail-closed — ein Operator, der gerade eine
    `.share.yml` bearbeitet, soll einen kaputten Bestand sofort sehen, nicht stillschweigend
    überschreiben."""
    if not path.exists():
        return {}
    raw = path.read_text(encoding="utf-8")
    data = yaml.safe_load(raw)
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError(f"{path} ist kein YAML-Mapping")
    return data


def _find_share_files(data_root: Path):
    yield from sorted(data_root.rglob(ACL_FILENAME))


# -- Unterbefehle -------------------------------------------------------------------------
#
# create-space/add-member/remove-member/remove-space rufen ab hier `storage.acl`s
# Schreibfunktionen auf (P7 Step C1, sechste Contract-Öffnung) statt eigener Kopien — reine
# Extraktion, Ausgabetexte und Exit-Codes bleiben byte-identisch (Bedingung für die 20
# bestehenden Tests dieser Datei als Regressionsbeweis).


def _cmd_create_space(data_root: Path, args: argparse.Namespace) -> int:
    name = args.name
    try:
        space_dir = acl.create_space(data_root, name)
    except acl.AclWriteError as exc:
        print(f"ABBRUCH: {exc}", file=sys.stderr)
        return EXIT_ERROR
    print(f"Space '{name}' angelegt: {space_dir}")
    return EXIT_OK


def _cmd_list_spaces(data_root: Path, args: argparse.Namespace) -> int:
    store = Store(data_root)
    spaces = store.list_spaces()
    if args.json:
        print(json.dumps(
            [{"name": s.name, "item_count": s.item_count, "members": list(s.members),
              "folders": list(s.folders)} for s in spaces],
            ensure_ascii=False, indent=2,
        ))
        return EXIT_OK
    if not spaces:
        print("Keine Spaces.")
        return EXIT_OK
    for s in spaces:
        print(f"{s.name}: {s.item_count} Item(s)  Mitglieder(write)={list(s.members)}  "
              f"Ordner={list(s.folders)}")
    return EXIT_OK


def _cmd_show(data_root: Path, args: argparse.Namespace) -> int:
    store = Store(data_root)
    space = args.space
    info = next((s for s in store.list_spaces() if s.name == space), None)
    grant = store.acl_reader.grants_for_space(space)
    exists = _is_known_space(data_root, space)
    print(f"Space: {space}")
    print(f"  Verzeichnis vorhanden: {exists}")
    print(f"  Items: {info.item_count if info else 0}")
    print(f"  Ordner: {list(info.folders) if info else []}")
    print(f"  Lesen erlaubt für: {sorted(grant.read)}")
    print(f"  Schreiben erlaubt für: {sorted(grant.write)}")
    return EXIT_OK


def _cmd_add_member(data_root: Path, args: argparse.Namespace) -> int:
    space, user = args.space, args.user
    if not _is_known_space(data_root, space):
        print(f"ABBRUCH: Space '{space}' existiert nicht unter {data_root}.", file=sys.stderr)
        return EXIT_ERROR
    if not _is_known_space(data_root, user):
        print(
            f"WARNUNG: '{user}' ist kein bekannter Space-Name unter {data_root} — die Freigabe "
            "bleibt wirkungslos (unbekannte Namen werden fail-closed ignoriert, Plan §1.2.2), "
            "bis ein gleichnamiger Space existiert.",
            file=sys.stderr,
        )
    key = "write" if args.write else "read"
    added = acl.add_member(data_root, space, user, write=args.write)
    if not added:
        print(f"'{user}' ist bereits in '{key}' für Space '{space}'.")
        return EXIT_OK
    print(f"Space '{space}': '{user}' zu '{key}' hinzugefügt.")
    return EXIT_OK


def _cmd_remove_member(data_root: Path, args: argparse.Namespace) -> int:
    space, user = args.space, args.user
    if not _is_known_space(data_root, space):
        print(f"ABBRUCH: Space '{space}' existiert nicht unter {data_root}.", file=sys.stderr)
        return EXIT_ERROR
    removed = acl.remove_member(data_root, space, user)
    if not removed:
        print(f"'{user}' war in keiner Liste von Space '{space}'.")
        return EXIT_OK
    print(f"Space '{space}': '{user}' entfernt aus {removed}.")
    return EXIT_OK


def _cmd_remove_space(data_root: Path, args: argparse.Namespace) -> int:
    name = args.name
    space_dir = data_root / name
    if not space_dir.is_dir():
        print(f"ABBRUCH: Space '{name}' existiert nicht.", file=sys.stderr)
        return EXIT_ERROR
    print(
        f"WARNUNG: Das entfernt nur die Arbeitskopie unter {space_dir}. Git-Historie "
        f"({data_root}) und jedes gezogene Backup (`git bundle`) behalten den Inhalt von "
        f"'{name}' weiterhin — kein echtes Löschen (root-CLAUDE.md Hard Rule 4 / Phase-6-Scope "
        "F2).",
        file=sys.stderr,
    )
    orphans = acl.spaces_referencing(data_root, name, exclude=space_dir / ACL_FILENAME)
    if orphans:
        print(
            f"WARNUNG: '{name}' wird nach dieser Aktion noch referenziert in: {orphans} — "
            "diese Freigaben verwaisen (fail-closed, kein Recht, aber `diagnose.sh`/`spacectl.py "
            "check` melden sie).",
            file=sys.stderr,
        )
    if not args.force:
        print("Trockenlauf — kein --force übergeben, nichts gelöscht.")
        return EXIT_OK
    acl.remove_space_dir(data_root, name)
    print(f"Space '{name}' entfernt.")
    return EXIT_OK


def _cmd_check(data_root: Path, args: argparse.Namespace) -> int:
    """Verwaiste `.share.yml`-Referenzen — Plan §4 Step 6 DoD, gefüttert an
    `phase3_edge/scripts/diagnose.sh`. Rein lesend, kein Abbruchkriterium für sich selbst."""
    known = {
        p.name for p in data_root.iterdir() if p.is_dir() and not p.name.startswith(".")
    }
    orphans: list[dict[str, str]] = []
    broken: list[str] = []
    for share_path in _find_share_files(data_root):
        rel = str(share_path.relative_to(data_root))
        try:
            data = _load_share_file(share_path)
        except (ValueError, yaml.YAMLError):
            broken.append(rel)
            continue
        names = set(data.get("read") or []) | set(data.get("write") or [])
        for name in sorted(names):
            if name not in known:
                orphans.append({"file": rel, "name": name})
    result = {
        "orphan_count": len(orphans), "orphans": orphans,
        "broken_count": len(broken), "broken": broken,
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if not orphans and not broken:
            print("Keine verwaisten oder kaputten .share.yml-Referenzen.")
        for o in orphans:
            print(f"VERWAIST  {o['file']}: '{o['name']}' ist kein bekannter Space")
        for b in broken:
            print(f"KAPUTT    {b}: nicht parsebares YAML")
    return EXIT_OK


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="spacectl",
        description="Operator-Werkzeug für Spaces und Freigaben — create-space, list-spaces, "
        "show, add-member, remove-member, remove-space, check.",
    )
    parser.add_argument("--data-root", metavar="PATH", default=None, help="überschreibt SPACE_DATA_ROOT")
    sub = parser.add_subparsers(dest="command", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--json", action="store_true", help="maschinenlesbare Ausgabe auf stdout")

    p_create = sub.add_parser("create-space")
    p_create.add_argument("name")

    sub.add_parser("list-spaces", parents=[common])

    p_show = sub.add_parser("show")
    p_show.add_argument("space")

    p_add = sub.add_parser("add-member")
    p_add.add_argument("space")
    p_add.add_argument("user")
    group = p_add.add_mutually_exclusive_group(required=True)
    group.add_argument("--read", action="store_true")
    group.add_argument("--write", action="store_true")

    p_remove_member = sub.add_parser("remove-member")
    p_remove_member.add_argument("space")
    p_remove_member.add_argument("user")

    p_remove_space = sub.add_parser("remove-space")
    p_remove_space.add_argument("name")
    p_remove_space.add_argument("--force", action="store_true")

    sub.add_parser("check", parents=[common])

    return parser


def main(argv: list[str] | None = None, *, env: dict[str, str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    resolved_env = env if env is not None else dict(os.environ)

    try:
        data_root = _resolve_data_root(args.data_root, resolved_env)
    except ValueError as exc:
        print(f"ABBRUCH: {exc}", file=sys.stderr)
        return EXIT_ERROR

    handlers = {
        "create-space": _cmd_create_space,
        "list-spaces": _cmd_list_spaces,
        "show": _cmd_show,
        "add-member": _cmd_add_member,
        "remove-member": _cmd_remove_member,
        "remove-space": _cmd_remove_space,
        "check": _cmd_check,
    }
    return handlers[args.command](data_root, args)


if __name__ == "__main__":
    sys.exit(main())
