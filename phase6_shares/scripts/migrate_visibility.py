#!/usr/bin/env python3
"""Migriert den Bestand auf explizites `visibility: private` (Plan §4 Step 6, §2.3) — ein
einmaliger Schnitt vor der Sichtbarkeits-Umstellung, kein Dauerwerkzeug.

Schreibt AUSSCHLIESSLICH das fehlende `visibility`-Feld, rührt Bodies nicht an. **Kein
`version`-Sprung, bewusst:** ein fehlendes `visibility`-Feld hat schon vor diesem Lauf den
Default `private` (`storage/models.py :: DEFAULT_VISIBILITY`, Frontmatter-Vertrag §2.1 — "Fehlende
Felder ⇒ Defaults") — diese Migration macht nur explizit, was implizit längst gilt, nichts
Beobachtbares ändert sich. Ein `version`-Sprung wäre hier sachlich falsch UND schädlich: jede
`version`, die eine laufende Claude-Instanz gerade in der Hand hält, würde beim nächsten
`update_item`/`patch_item` einen `ConflictError` auslösen, der keiner ist — potenziell genau am
Tag des Cutovers, an dem Abnahmezeile 8 getestet wird.

**Kein Index-Rebuild danach nötig, geprüft statt angenommen:** `storage/index.py ::
row_from_file()` gibt einem fehlenden `visibility`-Feld schon denselben Default (`"private"`,
Zeile `fields.get("visibility", "private")`) — Datei und Index sagen vor UND nach diesem Lauf
für jedes Item dasselbe.

Deshalb ruft dieses Skript nicht `Store.update()` auf (das würde pro Item einen eigenen
Git-Commit erzeugen) — es schreibt über den bestehenden atomaren Pfad direkt
(`storage.files.atomic_write`) und committet danach **einmal je Space**, nicht je Item (200
Commits wären Lärm, Plan §2.3). Ein `.write.lock`-Flock (dieselbe Datei wie
`Store._file_write_lock()`) wird für den GESAMTEN `--apply`-Lauf gehalten, nicht je Datei — ein
mit einem parallel schreibenden Dienst interleaved halbmigrierter Zustand wäre schwerer zu
erklären als ein kurzzeitig blockierter Dienst.

`--dry-run` ist der Default; erst `--apply` schreibt wirklich. Report: JSON, eine Zeile je
migriertem Item, auf stdout (Hard Rule 7), am Ende eine Summenzeile.
"""
from __future__ import annotations

import argparse
import fcntl
import json
import os
import sys
from pathlib import Path

from storage import files, frontmatter, history
from storage.models import DEFAULT_VISIBILITY

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


class _DataRootLock:
    """Flock auf `<data_root>/.write.lock` — dieselbe Datei wie `Store._file_write_lock()`,
    hier für den gesamten Migrationslauf gehalten (siehe Moduldocstring)."""

    def __init__(self, data_root: Path) -> None:
        self._lock_path = data_root / ".write.lock"
        self._fh = None

    def __enter__(self) -> "_DataRootLock":
        self._lock_path.touch(exist_ok=True)
        self._fh = open(self._lock_path, "r+")
        fcntl.flock(self._fh, fcntl.LOCK_EX)
        return self

    def __exit__(self, *exc_info: object) -> None:
        fcntl.flock(self._fh, fcntl.LOCK_UN)
        self._fh.close()


def _iter_item_files(data_root: Path):
    """Dieselbe Verzeichnis-Reihenfolge wie `index.rebuild_index()`: sortierte Spaces, sortierte
    `*.md`-Dateien je Space, inklusive `_archive/` (Archivierte Items brauchen `visibility`
    genauso — nur `folder` gilt dort nie, das betrifft diese Migration nicht)."""
    for space_dir in sorted(p for p in data_root.iterdir() if p.is_dir() and not p.name.startswith(".")):
        yield from sorted(space_dir.rglob("*.md"))


def scan(data_root: Path) -> list[dict]:
    """Liest jedes Item, meldet nur die, denen `visibility` fehlt. Kein Schreibzugriff."""
    report = []
    for path in _iter_item_files(data_root):
        raw = path.read_text(encoding="utf-8")
        fields, _body = frontmatter.parse(raw)
        if "visibility" in fields:
            continue
        space = path.relative_to(data_root).parts[0]
        report.append({
            "id": fields.get("id"), "space": space,
            "path": str(path.relative_to(data_root)),
            "before": None, "after": DEFAULT_VISIBILITY,
        })
    return report


def apply(data_root: Path, report: list[dict]) -> None:
    """Schreibt `visibility: private` in jede in `report` genannte Datei, dann ein Commit je
    Space. Erwartet, unter `_DataRootLock` zu laufen (Aufrufer-Vertrag, wie `history.commit`)."""
    # Idempotent wie in `Store.__init__` -- auf dem echten DATA_ROOT läuft das ohnehin schon
    # laufend über den Dienst, aber dieses Skript darf nicht davon abhängen, dass irgendwann
    # vorher schon ein `Store` instanziiert wurde (z. B. gegen ein frisches `tmp_path` in Tests).
    history.ensure_repo(data_root)
    by_space: dict[str, list[str]] = {}
    for row in report:
        by_space.setdefault(row["space"], []).append(row["path"])

    for space, paths in by_space.items():
        for rel_path in paths:
            path = data_root / rel_path
            raw = path.read_text(encoding="utf-8")
            fields, body = frontmatter.parse(raw)
            if "visibility" in fields:
                continue  # zwischen scan() und apply() von anderswo gesetzt -- nicht überschreiben
            # Position ist rein kosmetisch (YAML-Mapping, keine Semantik) -- der nächste
            # `Store`-Write auf dieses Item baut die Feldreihenfolge ohnehin komplett neu
            # (`_item_to_text()`), diese Migration muss sie nicht vorwegnehmen.
            fields["visibility"] = DEFAULT_VISIBILITY
            files.atomic_write(path, frontmatter.serialize(fields, body))
        history.commit(data_root, f"migrate visibility [{space}]")


def main(argv: list[str] | None = None, *, env: dict[str, str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="migrate_visibility",
        description="Schreibt fehlendes `visibility: private` in den Bestand (Plan §4 Step 6).",
    )
    parser.add_argument("--data-root", metavar="PATH", default=None, help="überschreibt SPACE_DATA_ROOT")
    parser.add_argument("--apply", action="store_true", help="wirklich schreiben (Default: --dry-run)")
    args = parser.parse_args(argv)
    resolved_env = env if env is not None else dict(os.environ)

    try:
        data_root = _resolve_data_root(args.data_root, resolved_env)
    except ValueError as exc:
        print(f"ABBRUCH: {exc}", file=sys.stderr)
        return EXIT_ERROR

    if args.apply:
        with _DataRootLock(data_root):
            report = scan(data_root)
            for row in report:
                print(json.dumps(row, ensure_ascii=False))
            apply(data_root, report)
    else:
        report = scan(data_root)
        for row in report:
            print(json.dumps(row, ensure_ascii=False))

    spaces_touched = sorted({row["space"] for row in report})
    summary = {
        "summary": True, "dry_run": not args.apply,
        "items_migrated": len(report), "spaces_touched": spaces_touched,
    }
    print(json.dumps(summary, ensure_ascii=False))
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
