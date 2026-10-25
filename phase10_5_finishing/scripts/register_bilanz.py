#!/usr/bin/env python3
"""register_bilanz.py — die Register-Bilanz der Phase 10.5 per Skript (P10.5-59, Muster P10-3).

Zählt die Ziel-Spalte des Baustellenregisters (`phase10_inventory/BAUSTELLENREGISTER.md`; das
Archiv trägt dieselben IDs und wird nicht doppelt gezählt). Eine Zeile ist eine **P10.5-Zeile**,
wenn ihre Ziel-Spalte `P10.5` nennt oder mit einem Marker und einer Abnahmenummer (`✅ 10-5`)
beginnt. Jede P10.5-Zeile muss mit einem Marker beginnen — ✅ erfüllt · ⚠️ erfüllt in anderer
Form · ⬜ offen (mit Beleg, wer es schließt). Eine Zeile ohne Marker ist ein Befund.

Aufruf: scripts/register_bilanz.py [repo_root]   — JSON auf stdout, Log auf stderr
Exit:   0 = jede P10.5-Zeile trägt einen Marker · 1 = mindestens eine nicht
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARKERS = ("✅", "⚠️", "⬜")
_ROW = re.compile(r"^\| ([A-Z]{2}-\d+) \|")
_NUMBERED = re.compile(r"^(✅|⚠️|⬜|🟡) (10(\.5)?-\d|B\d)")


def rows(path: Path) -> dict[str, str]:
    """ID → Ziel-Spalte, aus den Tabellen des Registers."""
    out: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").split("\n"):
        m = _ROW.match(line)
        if m and line.rstrip().endswith("|"):
            out[m.group(1)] = line.rstrip()[:-1].rsplit(" | ", 1)[-1].strip()
    return out


def bilanz(repo_root: Path) -> dict:
    ziele = rows(repo_root / "phase10_inventory" / "BAUSTELLENREGISTER.md")
    counted = {m: [] for m in MARKERS}
    ohne_marker: list[str] = []
    for kennung, ziel in ziele.items():
        if "P10.5" not in ziel and not _NUMBERED.match(ziel):
            continue
        marker = next((m for m in MARKERS if ziel.startswith(m)), None)
        if marker is None:
            ohne_marker.append(kennung)
        else:
            counted[marker].append(kennung)
    return {
        "zeilen_gesamt": len(ziele),
        "p105_zeilen": sum(len(v) for v in counted.values()) + len(ohne_marker),
        "✅": len(counted["✅"]), "⚠️": len(counted["⚠️"]), "⬜": len(counted["⬜"]),
        "offen": counted["⬜"],
        "ohne_marker": ohne_marker,
    }


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2]
    report = bilanz(root)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"register_bilanz: {len(report['ohne_marker'])} Zeile(n) ohne Marker", file=sys.stderr)
    return 1 if report["ohne_marker"] else 0


if __name__ == "__main__":
    sys.exit(main())
