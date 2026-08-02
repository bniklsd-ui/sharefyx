"""Meta-Test (Plan §5 Step 1 „Done when"): die Sicherheitsbefund-Tabelle S2–S8 in
`phase4_auth/CLAUDE.md` muss nach P5 Step 1 zeigen, dass keiner der sieben Befunde mehr offen
ist. Parst die Markdown-Tabelle direkt aus dem Kopf statt eine zweite, separat gepflegte
Datenquelle einzuführen — genau die Tabelle, die ein Mensch beim Lesen des Kopfes auch sieht.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PHASE4_HEAD = REPO_ROOT / "phase4_auth" / "CLAUDE.md"

FINDING_IDS = ("S2", "S3", "S4", "S5", "S6", "S7", "S8")


def _finding_rows() -> dict[str, str]:
    """`{Befund-ID: komplette Tabellenzeile}` aus der `## Sicherheits-Review ... — offene
    Befunde S2–S8`-Tabelle."""
    text = PHASE4_HEAD.read_text(encoding="utf-8")
    rows: dict[str, str] = {}
    for line in text.splitlines():
        match = re.match(r"\|\s*(S\d)\s*\|", line)
        if match:
            rows[match.group(1)] = line
    return rows


def test_security_review_register_is_empty():
    """Kein S2–S8-Befund darf mehr ohne ein ✅ in seiner Tabellenzeile stehen — sonst hätte
    P5 Step 1 einen der sieben Fixe stillschweigend nicht abgeschlossen."""
    rows = _finding_rows()
    assert set(FINDING_IDS) <= set(rows), f"erwartet S2..S8, gefunden: {sorted(rows)}"
    for finding_id in FINDING_IDS:
        row = rows[finding_id]
        assert "✅" in row, f"{finding_id} ist nicht als geschlossen markiert: {row!r}"


def test_no_finding_still_says_it_is_unfixed():
    """Regressionsschutz gegen den Satz, der genau das bisher behauptete (`**Keiner von S2–S8
    ist gefixt.**`) — ein Zurückrudern auf diesen Satz, ohne die Tabelle nachzuziehen, wäre
    stille Drift."""
    text = PHASE4_HEAD.read_text(encoding="utf-8")
    assert "Keiner von S2–S8 ist gefixt." not in text
