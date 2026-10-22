"""DO-3-Wächter für den Phase-10.5-Head (P10.5 Block 0, Schritt 0.3).

**Was DO-3 ist.** Registerzeile DO-3: „Ausführlichkeit der Session-Blöcke (10–17 KB, P9-Archiv
396 KB) — Kostenfaktor jeder Lesesitzung." Der Nikinger hat am 2026-10-18 entschieden (D-17): ein
Session-Block **höchstens 4 KiB** (Lock P10.5-T). Der Session-Block ist der Abschnitt, den jede
Lesesitzung zuerst liest — deshalb ist er der erste, dem eine Obergrenze gesetzt wird.

**Zwei Zusicherungen, und die zweite ist die wichtigere:**

1. Der Head trägt **genau einen** `## Session stopped`-Block (Doc-Layers-Konvention, Rotationsregel
   ab Tag 1; zwei Blöcke im Head sind der Zustand, den `scripts/rotate_session_block.sh` behebt).
2. Dieser Block ist **höchstens 4096 UTF-8-Bytes** — vom `## Session stopped`-Kopf bis zum nächsten
   `## ` oder Dateiende.

**Die Gegenprobe steckt in derselben Datei** (Plan, Abnahme P10.5-3: „ein 5-KiB-Block (Fixture)
macht ihn rot"). Ein Wächter, der nur am echten Head grün ist, beweist nichts: er könnte die
Grenze prüfen und sie falsch berechnen, und niemand merkt es. Der Test baut deshalb einen Head mit
absichtlich zu großem Block und verlangt, dass **dieselbe** Prüfung daran rot wird.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
HEAD = REPO_ROOT / "phase10_5_finishing" / "CLAUDE.md"
MARKER = "## Session stopped"
LIMIT_BYTES = 4096


def _session_block_bytes(text: str) -> int:
    """UTF-8-Bytes des Session-Blocks: vom `## Session stopped`-Kopf bis zum nächsten `## ` oder EOF.

    **Der Block endet an der nächsten Überschrift, nicht am nächsten Absatz** — sonst würde ein
    langer Fließtext unter dem Block mitgezählt und die Obergrenze prüfte die falsche Größe.
    """
    start = text.find(MARKER)
    if start < 0:
        return 0
    rest = text[start + len(MARKER):]
    match = re.search(r"^## ", rest, re.M)
    end = start + len(MARKER) + match.start() if match else len(text)
    return len(text[start:end].encode("utf-8"))


def _assert_block_fits(text: str) -> None:
    size = _session_block_bytes(text)
    assert size <= LIMIT_BYTES, (
        f"der Session-Block ist {size} B und damit über der Obergrenze von {LIMIT_BYTES} B "
        f"(Lock P10.5-T, DO-3) — kürzen, nicht die Grenze heben"
    )


def test_the_head_carries_exactly_one_session_block():
    """Zwei Blöcke im Head sind der Zustand, den `scripts/rotate_session_block.sh` behebt — und
    der Grund, warum der Wächter existiert, bevor der erste Block rotiert ist."""
    head = HEAD.read_text(encoding="utf-8")
    count = head.count(MARKER)
    assert count == 1, f"der Head trägt {count} '## Session stopped'-Blöcke, erwartet genau 1"


def test_the_session_block_is_at_most_4_kib():
    _assert_block_fits(HEAD.read_text(encoding="utf-8"))


def test_a_five_kib_block_would_be_rejected():
    """Die Gegenprobe (Abnahme P10.5-3): derselbe Prüfer, derselbe Head — nur mit einem Block,
    der 5 KiB groß ist. Er muss **rot** werden; bliebe er grün, prüfte der Wächter nichts."""
    oversized = HEAD.read_text(encoding="utf-8").replace(
        MARKER, MARKER + "\n\n" + ("x" * 5000), 1)
    with pytest.raises(AssertionError):
        _assert_block_fits(oversized)


def test_the_block_measurement_ends_at_the_next_heading():
    """Der Zähler muss am **nächsten `## `** enden, nicht am nächsten Absatz: sonst zählt der
    Text unter dem Block mit, und die Obergrenze würde die falsche Größe prüfen."""
    text = "## Session stopped — 2026-10-22\n\nkurz\n\n## Nächster Abschnitt\n\nviel Text\n"
    assert _session_block_bytes(text) == len("## Session stopped — 2026-10-22\n\nkurz\n\n".encode("utf-8"))

def test_the_acceptance_sum_matches_the_table():
    """Die **Summe-Zeile** muss zur Abnahmetabelle gehören — und wird sonst von Hand gepflegt.

    **Warum es diesen Wächter gibt (2026-10-22, Block 6):** die Zeile stand auf „21 ✅ · 0 ⚠️ ·
    40 ⬜", die Tabelle trug **20** ✅ — der Zähler war schon vor diesem Block falsch (Block 5 hat
    eine Zeile auf ✅ gezogen und die Summe nicht nachgezogen). Wer die Summe im Kopf pflegt,
    pflegt zwei Zahlen an zwei Orten; das ist die Fehlerklasse, die dieser Wächter beendet.
    """
    head = HEAD.read_text(encoding="utf-8")
    rows = [line for line in head.split("\n") if re.match(r"^\| P10\.5-\d+ \|", line)]
    assert len(rows) == 61, f"die Abnahmetabelle hat {len(rows)} Zeilen, erwartet 61"
    counted = {
        "✅": sum(1 for line in rows if "| ✅ |" in line),
        "⚠️": sum(1 for line in rows if "| ⚠️ |" in line),
        "⬜": sum(1 for line in rows if "| ⬜ |" in line),
    }
    match = re.search(r"\*\*Summe:\*\* (\d+) ✅ · (\d+) ⚠️ · (\d+) ⬜", head)
    assert match, "der Head trägt keine '**Summe:** … ✅ · … ⚠️ · … ⬜'-Zeile"
    claimed = tuple(int(value) for value in match.groups())
    assert claimed == (counted["✅"], counted["⚠️"], counted["⬜"]), (
        f"die Summe-Zeile behauptet {claimed}, die Tabelle trägt "
        f"({counted['✅']}, {counted['⚠️']}, {counted['⬜']}) — eine Zeile abhaken heißt auch, "
        f"die Summe nachzuziehen"
    )
