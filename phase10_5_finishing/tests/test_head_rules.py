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
#: Das L3-Archiv der **geschlossenen** Abnahmezeilen (der Head trägt die offenen).
ABNAHME_ARCHIV = REPO_ROOT / "phase10_5_finishing" / "ABNAHME_ARCHIVE.md"
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

def _abnahme_zeilen() -> list[str]:
    """Die Abnahmezeilen aus dem Head **und** aus dem Archiv.

    **Seit 2026-10-25 (Block 11.8) sind sie geteilt:** die geschlossenen Zeilen (✅/⚠️)
    stehen **verbatim** im L3-Archiv `ABNAHME_ARCHIVE.md` (der Head stand über dem
    Softcap), die offenen (⬜) im Head. Der Plan §5 zählt die Zeilen — das Zählen
    läuft deshalb über **beide** Dateien.

    **Die Zahl ist nicht festgemacht, sie ist eine Zusage über den Plan:** Block 13 hat
    drei Zeilen (62/63/64) hinzugefügt, der Plan §5 sagt seither „64 Zeilen". Wer eine
    Zeile hinzufügt, muss **hier und im Plan** dieselbe Zahl schreiben — sonst prüft der
    Wächter eine andere Menge als die, die der Plan verspricht.
    """
    zeilen: list[str] = []
    for datei in (HEAD, ABNAHME_ARCHIV):
        if not datei.exists():
            continue
        for line in datei.read_text(encoding="utf-8").split("\n"):
            if re.match(r"^\| P10\.5-\d+ \|", line):
                zeilen.append(line)
    return zeilen


def test_the_acceptance_sum_matches_the_table():
    """Die **Summe-Zeile** muss zur Abnahmetabelle gehören — und wird sonst von Hand gepflegt.

    **Warum es diesen Wächter gibt (2026-10-22, Block 6):** die Zeile stand auf „21 ✅ · 0 ⚠️ ·
    40 ⬜", die Tabelle trug **20** ✅ — der Zähler war schon vor diesem Block falsch (Block 5 hat
    eine Zeile auf ✅ gezogen und die Summe nicht nachgezogen). Wer die Summe im Kopf pflegt,
    pflegt zwei Zahlen an zwei Orten; das ist die Fehlerklasse, die dieser Wächter beendet.

    **Seit 2026-10-25 (Block 11.8)** zählt der Wächter über **beide** Dateien: die
    geschlossenen Zeilen stehen im L3-Archiv `ABNAHME_ARCHIVE.md`.
    """
    rows = _abnahme_zeilen()
    assert len(rows) == 64, f"die Abnahmetabelle hat {len(rows)} Zeilen, erwartet 64"
    counted = {
        "✅": sum(1 for line in rows if "| ✅ |" in line),
        "⚠️": sum(1 for line in rows if "| ⚠️ |" in line),
        "⬜": sum(1 for line in rows if "| ⬜ |" in line),
    }
    head = HEAD.read_text(encoding="utf-8")
    match = re.search(r"\*\*Summe:\*\* (\d+) ✅ · (\d+) ⚠️ · (\d+) ⬜", head)
    assert match, "der Head trägt keine '**Summe:** … ✅ · … ⚠️ · … ⬜'-Zeile"
    claimed = tuple(int(value) for value in match.groups())
    assert claimed == (counted["✅"], counted["⚠️"], counted["⬜"]), (
        f"die Summe-Zeile behauptet {claimed}, die Tabelle trägt "
        f"({counted['✅']}, {counted['⚠️']}, {counted['⬜']}) — eine Zeile abhaken heißt auch, "
        "die Summe nachzuziehen"
    )


def test_the_closed_rows_are_in_the_archive_and_the_open_ones_in_the_head():
    """**Die Teilung ist eine Zusage.** Die geschlossenen Zeilen stehen **im Archiv**, die
    offenen **im Head** — und keine Zeile steht in beiden (das wäre doppelt gezählt)."""
    head_zeilen = [z for z in HEAD.read_text(encoding="utf-8").split("\n")
                   if re.match(r"^\| P10\.5-\d+ \|", z)]
    archiv_zeilen = [z for z in ABNAHME_ARCHIV.read_text(encoding="utf-8").split("\n")
                      if re.match(r"^\| P10\.5-\d+ \|", z)]
    assert all("| ⬜ |" in z for z in head_zeilen), (
        "der Head traegt eine geschlossene Zeile — die gehoert ins Archiv"
    )
    assert all(("| ✅ |" in z) or ("| ⚠️ |" in z) for z in archiv_zeilen), (
        "das Archiv traegt eine offene Zeile — die gehoert in den Head"
    )
    nummern_head = {z.split("|")[1].strip() for z in head_zeilen}
    nummern_archiv = {z.split("|")[1].strip() for z in archiv_zeilen}
    assert not (nummern_head & nummern_archiv), (
        f"diese Zeilen stehen in beiden Listen: {sorted(nummern_head & nummern_archiv)}"
    )
    assert len(nummern_head | nummern_archiv) == 64, (
        f"zusammen tragen die beiden Listen {len(nummern_head | nummern_archiv)} Zeilen, "
        "erwartet 64"
    )


#: Das L3-Archiv, in das die ausführlichen Statusspalten der geschlossenen Blöcke wanderten.
MODULSTATUS_ARCHIV = REPO_ROOT / "phase10_5_finishing" / "MODULSTATUS_ARCHIVE.md"


def _modulstatus_zeilen(text: str) -> dict[str, list[str]]:
    """Die Modulstatus-Zeilen je Block.

    Gesucht wird **an der Tabellenkopfzeile** (`| Block | Inhalt (Register) |`), nicht an einer
    Überschrift: das L3-Archiv trägt die Kopfzeile in der L1-Karte und im Fließtext, aber keine
    `##`-Überschrift mit dem Wort „Modulstatus" — und der Head hat mehrere Tabellen.
    """
    zeilen: dict[str, list[str]] = {}
    gefunden = False
    for line in text.split("\n"):
        if line.startswith("| Block | Inhalt (Register) |"):
            gefunden = True
            continue
        if not gefunden:
            continue
        if not line.startswith("|"):
            break
        spalten = [s.strip() for s in line.split("|")]
        # Die Block-Kennung ist eine Zahl **oder** „Z" (der Closeout-Block) — nur Ziffern
        # zu pruefen wuerde genau diese eine Zeile verschleiern.
        if len(spalten) < 6 or not re.fullmatch(r"[0-9]+|Z", spalten[1]):
            continue
        zeilen.setdefault(spalten[1], []).append(line)
    return zeilen


def test_the_modulstatus_short_rows_and_the_archive_agree():
    """**Der Kurzstand im Head und die Vollzeilen im Archiv sind derselbe Stand** — in
    **beiden** Richtungen.

    * Jede Zeile des **Archivs** hat im Head eine Zeile, und die vier Spalten, die der Head
      noch traegt (Block, Inhalt, Wer, Deploy), sind **byte-gleich**.
    * Jede Zeile des **Heads**, die nicht im Archiv steht, traegt ihren **vollstaendigen**
      Stand — die aktiven Bloecke (11, 12, Z) gehoeren nicht ins Archiv.

    **Zwei Richtungen, weil zwei Listen es sind.** Der erste Wächter (2026-10-24) pruefte nur
    „das Archiv hat eine Zeile, der Head auch" — und bemerkte deshalb nicht, dass beim
    Aufteilen die Zeilen der **aktiven** Bloecke 11, 12 und Z aus **beiden** Listen
    verschwunden waren. `test_the_modulstatus_carries_every_block` schliesst diese Luecke.
    """
    head = HEAD.read_text(encoding="utf-8")
    assert MODULSTATUS_ARCHIV.exists(), f"das Archiv fehlt: {MODULSTATUS_ARCHIV}"
    archiv = MODULSTATUS_ARCHIV.read_text(encoding="utf-8")

    kurz_zeilen = _modulstatus_zeilen(head)
    voll_zeilen = _modulstatus_zeilen(archiv)
    assert kurz_zeilen, "der Modulstatus des Heads traegt keine Block-Zeilen"
    assert voll_zeilen, "das Archiv traegt keine Block-Zeilen"

    for nummer, zeilen in voll_zeilen.items():
        assert nummer in kurz_zeilen, (
            f"der Block {nummer} steht im Archiv, aber nicht im Head — der Kurzstand traegt "
            "ihn nicht"
        )
        kurz = kurz_zeilen[nummer][0]
        voll = zeilen[0]
        for spalte in range(1, 5):     # Block, Inhalt, Wer, Deploy
            assert kurz.split("|")[spalte] == voll.split("|")[spalte], (
                f"Block {nummer}: Spalte {spalte} weicht zwischen Head und Archiv ab — "
                f"{kurz.split('|')[spalte]!r} != {voll.split('|')[spalte]!r}"
            )
        assert len(kurz) <= len(voll), (
            f"Block {nummer}: die Kurzzeile im Head ist laenger als die Vollzeile im Archiv — "
            "dann ist nichts verschoben worden"
        )

    # Die aktiven Bloecke stehen **nur** im Head — und dort mit ihrem vollen Stand.
    for nummer, zeilen in kurz_zeilen.items():
        if nummer in voll_zeilen:
            continue
        status = zeilen[0].split("|")[5]
        assert any(marker in status for marker in ("✅", "🔄", "⬜")), (
            f"der Block {nummer} steht nur im Head, traegt aber **keinen** Status "
            f"({status!r}) — die aktiven Bloecke gehoeren nicht ins Archiv"
        )


#: Die Bloecke, die der Modulstatus **alle** tragen muss (Plan §0.2: „eine Zeile je Block
#: 0–12/Z mit Status-Spalte" — **Block 13** kam am 2026-10-25 als datierter Nachtrag dazu:
#: die vier Auftraege des Nikingers).
ERWARTETE_BLOECKE = [str(n) for n in range(0, 14)] + ["Z"]


def test_the_modulstatus_carries_every_block():
    """**Jeder** Block 0–12 und Z braucht eine Zeile — der Modulstatus ist die Karte der
    Phase, keine Auswahl.

    **Wie dieser Fehler passieren konnte (2026-10-24, Block 11.4):** beim Aufteilen des
    Modulstatus (Kurzstand in den Head, ausführliche Statusspalten in das L3-Archiv) sind die
    Zeilen der **aktiven** Blöcke 11, 12 und Z verloren gegangen — der Head zeigte danach nur
    die geschlossenen Blöcke 0–10. Der Wächter, der die Aufteilung band (Zeile fuer Zeile
    gegen das Archiv), prüfte nur die Richtung „Archiv → Head" und merkte es **nicht**: die
    drei Zeilen fehlten in **beiden** Listen, also war fuer sie niemand zustaendig.
    """
    head = HEAD.read_text(encoding="utf-8")
    zeilen = _modulstatus_zeilen(head)
    fehlend = [b for b in ERWARTETE_BLOECKE if b not in zeilen]
    assert not fehlend, (
        f"der Modulstatus traegt keine Zeile fuer den Block {fehlend} — der Plan verlangt eine "
        "Zeile je Block 0–12/Z"
    )


def test_the_head_stays_under_the_softcap():
    """**Der Softcap ist eine Obergrenze, kein Ziel** — und der Head muss sie **halten**.

    **Der Weg, den der Head nahm (2026-10-24, Block 11.4):** beim Bau von Block 11.4 stand er
    bei **43.183 B** — über der Grenze (40.960 B). Die ausführlichen Statusspalten der
    geschlossenen Blöcke wandern in `MODULSTATUS_ARCHIVE.md` (L3), der Head trägt den
    Kurzstand; er steht seitdem bei ~37 KB, also mit Reserve für die nächsten Blöcke.

    **Der Wächter stand im Arbeitsbaum vom 2026-10-25 ohne Grund auf der Streichliste** — die
    Datei erfüllte die Grenze, der Wächter war grün, und trotzdem wurde er entfernt. Ein
    Wächter, der fällt, weil jemand ihn gelöscht hat, ist kein Wächter mehr: der nächste
    Block, der den Head über die Grenze schiebt, fällt dann **ohne rote Zeile** durch.
    Deshalb steht er wieder hier — mit der Grenze **nicht** angehoben, sondern eingehalten.
    """
    groesse = len(HEAD.read_bytes())
    assert groesse <= 40 * 1024, (
        f"der Phase-Head ist {groesse} B und damit über dem Softcap (40.960 B) — "
        "einen Abschnitt verbatim in ein L3-Archiv verschieben, nicht die Grenze heben"
    )
