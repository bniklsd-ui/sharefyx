"""Oversize-Fix (2026-10-07, Nikinger: „let's find a fix for the oversize docs") — die Wächter.

Drei lebende Phase-9-Dokumente lagen über dem 40-KiB-Softcap und waren nur **benannt** (P8-P):
Abnahmematrix 98.782 B, settings-Mini-Plan 64.996 B, Step-A-Runbook 62.021 B. Der Fix ist
`scripts/move_sections.py`: Abschnitte wandern **verbatim**, die Überschrift bleibt mit Zeiger
stehen. Zwei Formen, und der Unterschied ist der Punkt:

* **Archiv (L3, 📦)** für Abgeschlossenes — die ausgeführten Plan-Nachträge §10–§12.1 und die
  erledigten Runbook-Schritte §0, A1–A7.
* **Teilung (L2, 📗)** für die Matrix — ihre Zeilen ändern sich noch (P9-11 am 2026-10-07) und tragen
  Bytezahlen, die `test_acceptance_numbers.py` bei jedem Lauf nachmisst. Ein Archiv, das ein Test
  aktuell halten muss, ist keins.

Diese Tests halten fest, was ohne sie still zurückwächst: **harte** Größe je lebendem Teil (nicht
„benannt") und die Zeiger an den Überschriften, auf die andere Dokumente verweisen.
"""
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SOFTCAP_BYTES = 40 * 1024
POINTER = "> **Verbatim verschoben** nach "

P9 = REPO_ROOT / "phase9_hardening"
PLAN = REPO_ROOT / "docs" / "concepts" / "phase9_hardening_block_settings_plan.md"

# Lebende Dokumente, die der Fix unter den Cap gebracht hat — hart, ohne Benennungs-Ausweg.
LIVE_UNDER_CAP = (
    P9 / "ABNAHME_MATRIX.md",
    P9 / "ABNAHME_MATRIX_STEPS.md",
    P9 / "ABNAHME_MATRIX_BLOECKE.md",
    P9 / "ABNAHME_MATRIX_VERIFY.md",
    PLAN,
    P9 / "step_a" / "RUNBOOK_STEP_A.md",
)

# (Quelle, Ziel, Überschriften-Anfänge) — abgetippt, nicht aus der Datei gelesen.
MOVES = (
    (PLAN, PLAN.with_name("phase9_hardening_block_settings_plan_ARCHIVE.md"),
     ("## §10 ", "## §11 ", "## §12 ", "## §12.1 ")),
    (P9 / "step_a" / "RUNBOOK_STEP_A.md", P9 / "step_a" / "RUNBOOK_STEP_A_ARCHIVE.md",
     ("## §0 ", "### A1 ", "### A2 ", "### A3 ", "### Feld für Feld", "### A0b ", "### A4 ", "### A5 ",
      "### A6 ", "### A7 ")),
    (P9 / "ABNAHME_MATRIX.md", P9 / "ABNAHME_MATRIX_STEPS.md",
     ("## Step 0 ", "## Step A ", "## Step D ", "## Step H ", "## Phasenweit ")),
    (P9 / "ABNAHME_MATRIX.md", P9 / "ABNAHME_MATRIX_BLOECKE.md",
     ("## Block doing", "## Block trace", "## Dritte Bildsichtung")),
    (P9 / "ABNAHME_MATRIX.md", P9 / "ABNAHME_MATRIX_VERIFY.md", ("## Stand je Eintrag",)),
)


def test_the_live_documents_are_under_the_softcap_without_a_naming_escape():
    for path in LIVE_UNDER_CAP:
        size = path.stat().st_size
        assert size <= SOFTCAP_BYTES, (
            f"{path.relative_to(REPO_ROOT)} ist {size} B, über dem Softcap. Nicht benennen, sondern "
            "verschieben: `scripts/move_sections.py` (Abgeschlossenes nach L3, Matrix-Blöcke in einen neuen Teil)"
        )


def test_every_moved_heading_keeps_its_pointer_and_lands_in_its_target():
    for src, dst, prefixes in MOVES:
        src_lines = src.read_text(encoding="utf-8").split("\n")
        dst_text = dst.read_text(encoding="utf-8")
        for prefix in prefixes:
            hits = [i for i, l in enumerate(src_lines) if l.startswith(prefix)]
            assert len(hits) == 1, f"{src.name}: Überschrift {prefix!r} {len(hits)}× statt 1×"
            assert src_lines[hits[0] + 1].startswith(POINTER + f"`{dst.name}`") or \
                src_lines[hits[0] + 1].startswith(POINTER) and dst.name in src_lines[hits[0] + 1], (
                f"{src.name}: unter {prefix!r} fehlt der Zeiger auf {dst.name}"
            )
            assert re.search(rf"^{re.escape(src_lines[hits[0]])}$", dst_text, re.M), (
                f"{dst.name}: die Überschrift {src_lines[hits[0]]!r} fehlt im Ziel"
            )


def test_the_runbook_pointer_still_names_the_ten_findings():
    """Andere Dokumente und Tests zitieren „Runbook §0 Befund N" — die Überschriften müssen im Archiv stehen."""
    archive = (P9 / "step_a" / "RUNBOOK_STEP_A_ARCHIVE.md").read_text(encoding="utf-8")
    for n in range(1, 11):
        assert re.search(rf"^### Befund {n} — ", archive, re.M), f"Befund {n} fehlt im Runbook-Archiv"


def test_the_matrix_parts_do_not_carry_the_abnahme_balance():
    """Die Bilanz-Überschrift gehört dem Hub. Ein Teil, der sie wiederholt, wäre die zweite Kopie."""
    for name in ("ABNAHME_MATRIX_STEPS.md", "ABNAHME_MATRIX_BLOECKE.md", "ABNAHME_MATRIX_VERIFY.md"):
        assert "Tabellenzeilen für" not in (P9 / name).read_text(encoding="utf-8"), name
