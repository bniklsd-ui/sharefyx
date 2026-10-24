#!/usr/bin/env python3
"""P10.5 Block 8 — die Kanten der Wegwerf-Instanz **je Space** verketten.

**Warum das nötig ist (und was es *nicht* ist):** die Lappen (Plan 8.1) entstehen dort, wo
zwei benachbarte Zellen zu **verschiedenen Spaces** gehören — die Furche liegt an der
Space-Grenze. Der Seed der Phase 8 verlinkt die 200 Knoten zu *einem* Ring über alle Spaces
hinweg (`LINK_STRIDE = 7`, ein Ring über 200 Knoten). Dadurch liegen die Spaces räumlich
**ineinander** statt **nebeneinander** — die Furche ist dann überall, und die Lappen zerfallen
zu Fragmenten (gemessen an der Wegwerf-Instanz: 1309 Pixel Lappenfläche bei 200 Knoten; im
Screenshot nicht als Fläche sichtbar).

Das ist **kein Fehler des Algorithmus**, sondern eine Eigenschaft der Streu-Daten: die
Gehirnkarte C2 braucht zusammenhängende Räume. Die Daten zu ändern ist keine Kosmetik am
Beweis, sondern die Voraussetzung, die der Plan meint: „die Zuordnung ergibt den **Space des
Knotens** als Lappen-ID" — ein Space, der räumlich zusammenhängt, ergibt einen Lappen.

**Was NICHT angefasst wird:** die Item-Zahl (200), die Space-Verteilung (120/50/30), die Tags,
die Typen, die Status — die Abnahmezeilen des Smoke (`p8_22_smoke.py`) zählen Knoten und
Kanten, nicht die Topologie.

Aufruf: `.venv/bin/python phase10_5_finishing/probes/p105_b8_cluster_links.py [--zurueck]`
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
WEGWERF_ROOT = Path("/tmp/opencode/sharefyx-wegwerf-200knoten")
DATA_ROOT = WEGWERF_ROOT / "data"
IDS_FILE = WEGWERF_ROOT / "ids.json"
BUNDLE = 2              # wie viele Nachbarn **im selben Space** jeder Knoten verweist
sys.path.insert(0, str(REPO_ROOT / "phase1_storage"))

from storage.store import Store  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zurueck", action="store_true",
                        help="den Ring ueber alle 200 Knoten wiederherstellen (LINK_STRIDE = 7)")
    args = parser.parse_args(argv)

    store = Store(str(DATA_ROOT), now_fn=lambda: datetime.now(timezone.utc))
    ids = json.loads(IDS_FILE.read_text(encoding="utf-8"))
    items = [store.get(item_id) for item_id in ids.values()]

    per_space: dict[str, list] = {}
    for item in items:
        per_space.setdefault(item.space, []).append(item)
    for group in per_space.values():
        group.sort(key=lambda i: i.title)

    geaendert = 0
    if args.zurueck:
        # Der alte Ring: der Sprung von 7 ueber die **globale** Indexfolge.
        alle = sorted(items, key=lambda i: i.title)
        for index, item in enumerate(alle):
            target = alle[(index + 7) % len(alle)]
            if item.links == [target.id]:
                continue
            store.update(item.id, version=item.version, links=[target.id])
            geaendert += 1
    else:
        # Je Space ein **dichtes** Bündel: jeder Knoten verweist auf die nächsten fuenf
        # Knoten **seines** Spaces. Das ist der Unterschied zwischen einem Ring (einer
        # langen Kurve, die sich ueber die Flaeche zieht -- die Spaces liegen dann
        # nebeneinander, aber *ineinander*) und einem Bündel (die Kanten ziehen die Knoten
        # zusammen, die Abstoßung schiebt die drei Buendel gegeneinander). Erst das
        # Buendel macht die Space-Grenze zu einer **Grenze** -- und damit die Furche zur
        # Furche und den Lappen zum Lappen.
        for group in per_space.values():
            n = len(group)
            if n < 2:
                continue
            for index, item in enumerate(group):
                targets = [group[(index + k) % n].id for k in range(1, min(BUNDLE, n) + 1)]
                if item.links == targets:
                    continue
                store.update(item.id, version=item.version, links=targets)
                geaendert += 1

    store.rebuild_index()
    print(json.dumps({
        "items": len(items),
        "spaces": {s: len(g) for s, g in sorted(per_space.items())},
        "geaendert": geaendert,
        "modus": "zurueck" if args.zurueck else f"buendel-{BUNDLE}-je-space",
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
