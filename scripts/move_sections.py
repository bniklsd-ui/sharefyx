#!/usr/bin/env python3
"""move_sections.py — Abschnitte eines Markdown-Dokuments **verbatim** in ein zweites verschieben.

Der Hebel gegen den 40-KiB-Softcap, wenn ein lebendes Dokument an Abschnittsgrenzen wächst
(ausgeführte Plan-Nachträge, erledigte Runbook-Schritte, Abnahmeblöcke). Nikinger-Auftrag
2026-10-07: „let's find a fix for the oversize docs". Dieselben Zusicherungen wie
`rotate_session_block.sh` — nichts wird abgetippt, alles wird gegengelesen, bei jeder Abweichung
wird **nichts** geschrieben:

1. Ein Abschnitt reicht von seiner Überschrift bis vor die nächste Überschrift **gleicher oder
   höherer** Ebene. Zeilen in ```-Blöcken zählen nie als Überschrift (Runbooks tragen `# Kommentar`
   in Shell-Blöcken).
2. Im Quelldokument bleibt die **Überschrift** stehen, darunter eine Zeigerzeile — Querverweise
   wie „Plan §11.1" oder „Runbook §0 Befund 3" landen weiter auf einer Überschrift.
3. Gegenprobe (a): Quelle-neu, Zeiger zurück durch die Abschnittskörper ersetzt, ist **byte-gleich**
   mit dem Original. Gegenprobe (b): jeder bewegte Abschnitt steht im Ziel byte-gleich. Gegenprobe
   (c): der Altbestand des Ziels ist unverändert sein Präfix.
4. Geschrieben wird atomar (`tmp` + `os.replace`), Ziel zuerst, Quelle danach.

Aufruf:
    scripts/move_sections.py <quelle.md> <ziel.md> "<Überschriftzeile, exakter Anfang>" [...]

Das Ziel muss existieren (mit L1-Karte — die schreibt ein Mensch, kein Skript). Die bewegten
Abschnitte werden in **Dokumentreihenfolge** angehängt.

Exit: 0 = verschoben · 1 = Abbruch, nichts geändert (auch: Abschnitt schon verschoben)
"""
import os
import re
import sys
from pathlib import Path

HEADING = re.compile(r"^(#{1,6}) ")
FENCE = re.compile(r"^\s*```")


def die(msg: str) -> None:
    print(f"ABBRUCH: {msg}", file=sys.stderr)
    sys.exit(1)


def heading_levels(lines: list[str]) -> list[int]:
    """Ebene je Zeile (0 = keine Überschrift), Code-Blöcke ausgenommen."""
    out, fenced = [], False
    for line in lines:
        if FENCE.match(line):
            fenced = not fenced
            out.append(0)
            continue
        m = None if fenced else HEADING.match(line)
        out.append(len(m.group(1)) if m else 0)
    return out


def section_range(lines: list[str], levels: list[int], prefix: str) -> tuple[int, int]:
    hits = [i for i, l in enumerate(lines) if levels[i] and l.startswith(prefix)]
    if len(hits) != 1:
        die(f"genau eine Überschrift mit Anfang {prefix!r} erwartet, gefunden {len(hits)}")
    start = hits[0]
    end = next((j for j in range(start + 1, len(lines)) if levels[j] and levels[j] <= levels[start]), len(lines))
    return start, end


def atomic_write(path: Path, text: str) -> None:
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    with open(tmp, "rb") as fh:
        os.fsync(fh.fileno())
    os.replace(tmp, path)


def main(argv: list[str]) -> int:
    if len(argv) < 4:
        print(__doc__, file=sys.stderr)
        return 1
    src, dst, prefixes = Path(argv[1]), Path(argv[2]), argv[3:]
    if not src.is_file() or not dst.is_file():
        die(f"Quelle oder Ziel fehlt: {src} / {dst}")
    original = src.read_text(encoding="utf-8")
    dst_old = dst.read_text(encoding="utf-8")
    lines = original.split("\n")
    levels = heading_levels(lines)

    ranges = sorted(section_range(lines, levels, p) for p in prefixes)
    for (a0, a1), (b0, _) in zip(ranges, ranges[1:]):
        if b0 < a1:
            die(f"Abschnitte überlappen (Zeilen {a0 + 1}–{a1} und ab {b0 + 1})")

    pointer = f"> **Verbatim verschoben** nach `{os.path.relpath(dst, src.parent)}` (`scripts/move_sections.py`) — dort unter derselben Überschrift."
    new_lines, blocks, cursor = [], [], 0
    for start, end in ranges:
        body = lines[start + 1:end]
        if body and body[0].startswith("> **Verbatim verschoben**"):
            die(f"Abschnitt Zeile {start + 1} ist bereits verschoben")
        new_lines += lines[cursor:start + 1] + [pointer, ""]
        blocks.append("\n".join(lines[start:end]))
        cursor = end
    new_lines += lines[cursor:]
    new_src = "\n".join(new_lines)

    # Gegenprobe (a): Reassemblierung — jeder Zeiger (plus Leerzeile) zurück durch seinen Körper.
    rebuilt, it = [], iter(blocks)
    skip = False
    for line in new_lines:
        if skip:
            skip = False
            continue
        if line == pointer:
            rebuilt += next(it).split("\n")[1:]
            skip = True
            continue
        rebuilt.append(line)
    if "\n".join(rebuilt) != original:
        die("Reassemblierung != Original — Schnitt nicht verlustfrei, nichts geschrieben")

    sep = "" if dst_old.endswith("\n\n") else ("\n" if dst_old.endswith("\n") else "\n\n")
    new_dst = dst_old + sep + "\n\n".join(blocks).rstrip("\n") + "\n"
    # Gegenprobe (b) und (c)
    if not new_dst.startswith(dst_old):
        die("Altbestand des Ziels verändert")
    for b in blocks:
        # rstrip: ein Abschnitt am Dateiende traegt die abschliessenden Leerzeilen der Quelle mit,
        # die beim Anhaengen (oben) bewusst abgeschnitten werden — gefunden 2026-10-08 (E1a-Vorlauf),
        # da brach das Skript bei genau diesem Fall ab, ohne etwas geschrieben zu haben.
        if b.rstrip("\n") not in new_dst:
            die("ein bewegter Abschnitt steht nicht byte-gleich im Ziel")

    atomic_write(dst, new_dst)
    if dst.read_text(encoding="utf-8") != new_dst:
        die("Ziel nach dem Schreiben nicht gleich dem Geprüften — Quelle NICHT angefasst")
    atomic_write(src, new_src)
    moved = sum(len(b.encode()) for b in blocks)
    print(f"OK  {len(blocks)} Abschnitt(e), {moved} B verbatim: {src} → {dst}")
    print(f"OK  Quelle {len(original.encode())} B → {len(new_src.encode())} B · Ziel {len(dst_old.encode())} B → {len(new_dst.encode())} B")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
