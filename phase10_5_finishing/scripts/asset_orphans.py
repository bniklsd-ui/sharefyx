#!/usr/bin/env python3
"""asset_orphans.py — verwaiste Asset-Ordner finden und **nur auf Wunsch** in den Papierkorb
verschieben (P10.5, Block 3, Schritt 3.3; LG-7).

**Wozu.** `Store.trash()` verschiebt ein Item nach `DATA_ROOT/._trash/<space>/`, aber **die
Bilddateien bleiben liegen** (bewusst, nicht vergessen — `store.py`, Docstring von `trash()`:
ein zweiter Move würde aus einer atomaren Operation zwei halbe machen). Ergebnis: unter
`<space>/_assets/<item_id>/` liegt ein Ordner, zu dem es **kein** Item mehr gibt. Das ist
der Aufräum-Posten, den V162 benannt, aber nicht gebaut hat.

**Was „verwaist" bedeutet — und warum der Plan hier vom Code abweicht.** Der Plan (Block 3,
Schritt 3.3) sagt „zu dem es im **Index** keine Item-Zeile in diesem Space gibt". Der Code
gewinnt (Hard Rule 2: *Dateien sind die Wahrheit, der Index ist Ableitung*): geprüft wird
gegen die **Dateien**. Grund: ein veralteter Index (Rebuild steht aus, ein Item wurde von
Hand verschoben) würde die Assets **lebender** Items als verwaist melden — und `--move` würde
sie in den Papierkorb schieben. Das ist der einzige Unterschied zum Plan, und er ist
bewusst (datierte Notiz im Phase-Head, 2026-10-22).

**Zwei Modi, und der Default ist der harmlose:**
* `--report` (Default) — **nur lesen**: JSON auf stdout, `[{space, item_id, files, bytes}]`
  plus Summe. Schreibt nichts, committet nichts.
* `--move` — verschiebt jeden gefundenen Ordner mit `files.move_asset_dir()` nach
  `DATA_ROOT/._trash/<space>/_assets/<item_id>/` und macht **einen** Commit über
  `storage.history.commit()`. Es wird **nie gelöscht** (LG-5: der Papierkorb wird nicht
  geleert) — der Ordner landet im Papierkorb, nicht im Nirgendwo.

**`--data-root` ist Pflicht**, es gibt keinen Default und keinen stillen Fallback ins
Arbeitsverzeichnis (dieselbe Haltung wie `spacectl.py`): dieses Werkzeug zeigt auf fremde
Daten und schreibt in fremde Daten — der Pfad muss ausdrücklich genannt sein.

**Der Live-Lauf ist Nikinger-Arbeit** (Plan: „zuerst nur `--report`"). Das Skript greift in
den echten `DATA_ROOT` nur, wenn der Pfad ausdrücklich übergeben wird.

Aufruf:  phase10_5_finishing/scripts/asset_orphans.py --data-root <pfad> [--report | --move]
                [--author <name>]
Exit:   0 = ok (Report erzeugt bzw. Ordner verschoben) · 1 = Fehler (nichts verschoben)
"""
from __future__ import annotations

import argparse
import fcntl
import json
import logging
import os
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from storage import files, history
from storage.store import TRASH_DIR

logger = logging.getLogger("asset_orphans")

EXIT_OK = 0
EXIT_ERROR = 1

# Die Item-ID steht im Dateinamen (`<id>__<slug>.md`) — der Kern schreibt sie dort und sucht
# nie über den Namen (Entscheidung F). Für die Waisen-Suche ist der Ordnername unter
# `_assets/` aber genau diese ID, deshalb wird er gegen dasselbe Muster geprüft: ein fremder
# Verzeichnisname ist nicht unser Bestand und wird nicht angefasst.
ITEM_IDS = files.ITEM_ID_RE


@dataclass
class Orphan:
    """Ein verwaister Asset-Ordner —_space/_assets/item_id/."""

    space: str
    item_id: str
    files: int
    bytes: int


def _space_dirs(data_root: Path) -> list[Path]:
    """Die Space-Verzeichnisse unter `DATA_ROOT` — ohne Punkt-Verzeichnisse.

    `._trash` (der Papierkorb auf DATA_ROOT-Ebene) und `.index.sqlite3` & Co. fallen damit
    weg; ein Space-Ordner ist ein Verzeichnis **ohne** Punkt am Anfang."""
    if not data_root.is_dir():
        raise FileNotFoundError(f"DATA_ROOT existiert nicht: {data_root}")
    return sorted(
        path for path in data_root.iterdir()
        if path.is_dir() and not path.name.startswith(".") and path.name != TRASH_DIR
    )


def _live_item_ids(space_dir: Path) -> set[str]:
    """Die IDs der Items, die es in diesem Space **wirklich** gibt — aus den Dateien.

    Ein durchgestrichener `_archive/`-Ordner zählt mit: ein archiviertes Item existiert
    noch, seine Bilder sind keine Waisen. Der Name einer Item-Datei ist `<id>__<slug>.md`,
    die ID steht also vor dem ersten `__` (Entscheidung F)."""
    ids: set[str] = set()
    for path in space_dir.rglob("*.md"):
        name = path.name
        if "__" not in name:
            continue
        ids.add(name.split("__", 1)[0])
    return ids


def _asset_dirs(space_dir: Path) -> list[Path]:
    """Die Asset-Ordner eines Spaces (`_assets/<item_id>/`), alphabetisch."""
    assets_root = space_dir / "_assets"
    if not assets_root.is_dir():
        return []
    return sorted(
        path for path in assets_root.iterdir()
        if path.is_dir() and ITEM_IDS.match(path.name)
    )


def _measure(directory: Path) -> tuple[int, int]:
    """(Dateien, Bytes) unterhalb `directory` — rekursiv, ohne Symlink-Follow."""
    count = 0
    size = 0
    for root, _dirs, names in os.walk(directory):
        for name in names:
            path = Path(root) / name
            try:
                size += path.stat().st_size
            except OSError as exc:  # pragma: no cover - unlesbare Datei
                logger.warning("Konnte %s nicht messen: %s", path, exc)
                continue
            count += 1
    return count, size


def find_orphans(data_root: Path) -> list[Orphan]:
    """Alle verwaisten Asset-Ordner unter `data_root` — **lesend**."""
    orphans: list[Orphan] = []
    for space_dir in _space_dirs(data_root):
        live = _live_item_ids(space_dir)
        for asset_dir in _asset_dirs(space_dir):
            if asset_dir.name in live:
                continue
            count, size = _measure(asset_dir)
            orphans.append(Orphan(
                space=space_dir.name, item_id=asset_dir.name, files=count, bytes=size,
            ))
    return orphans


def move_orphans(data_root: Path, orphans: list[Orphan], *, author: str = "") -> None:
    """Verschiebt jeden verwaisten Ordner in den Papierkorb — **ein** Commit für alle.

    Der Commit ist ein Commit (Hard Rule 5: jeder erfolgreiche Write erzeugt einen), nicht
    einer je Ordner: der Aufräumvorgang ist eine Handlung, keine Serie. Verschoben wird mit
    `files.move_asset_dir()` (atomarer Verzeichnis-Move mit `fsync`), **gelöscht** wird nie
    (LG-5)."""
    if not (data_root / ".git").exists():
        # Ohne Git-Repo gäbe es keinen Commit — die Ordner wären trotzdem verschoben, der
        # Zustand also halb. Das ist genau der Fall, den die Regel „atomar oder gar nicht"
        # verbietet: lieber gar nichts verschieben.
        raise NotADirectoryError(
            f"{data_root} ist kein Git-Repository — ohne Commit kein Verschieben."
        )
    lock_path = data_root / ".write.lock"
    lock_path.touch(exist_ok=True)
    with open(lock_path, "r+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        try:
            for orphan in orphans:
                src = files.asset_dir(data_root, orphan.space, orphan.item_id)
                dst = data_root / TRASH_DIR / orphan.space / "_assets" / orphan.item_id
                files.move_asset_dir(src, dst)
                logger.info("Verschoben: %s/%s -> %s", orphan.space, orphan.item_id, dst)
            history.commit(
                data_root, f"asset-orphans: {len(orphans)} Ordner", author=author,
            )
        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument(
        "--data-root", metavar="PATH", required=True,
        help="Pflicht: das Datenverzeichnis, das geprüft (und bei --move verändert) wird.",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--report", action="store_true",
        help="nur lesen: JSON auf stdout (Default).",
    )
    group.add_argument(
        "--move", action="store_true",
        help="die gefundenen Ordner in den Papierkorb verschieben (ein Commit).",
    )
    parser.add_argument(
        "--author", default="",
        help="Git-Autor des Move-Commits (leer = Default-Identität des Datenverzeichnisses).",
    )
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.INFO, stream=sys.stderr, format="%(levelname)s %(name)s: %(message)s"
    )

    data_root = Path(args.data_root)
    try:
        orphans = find_orphans(data_root)
    except (FileNotFoundError, OSError) as exc:
        logger.error("%s", exc)
        return EXIT_ERROR

    if args.move:
        if not orphans:
            print(json.dumps({"orphans": [], "total_files": 0, "total_bytes": 0},
                             ensure_ascii=False, indent=2))
            return EXIT_OK
        try:
            move_orphans(data_root, orphans, author=args.author)
        except (OSError, NotADirectoryError) as exc:
            logger.error("Verschieben abgebrochen: %s", exc)
            return EXIT_ERROR
        print(json.dumps(
            {
                "moved": [asdict(o) for o in orphans],
                "total_files": sum(o.files for o in orphans),
                "total_bytes": sum(o.bytes for o in orphans),
            },
            ensure_ascii=False, indent=2,
        ))
        return EXIT_OK

    print(json.dumps(
        {
            "orphans": [asdict(o) for o in orphans],
            "total_files": sum(o.files for o in orphans),
            "total_bytes": sum(o.bytes for o in orphans),
        },
        ensure_ascii=False, indent=2,
    ))
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
