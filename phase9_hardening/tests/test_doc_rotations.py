"""Gate/Z-Doku-Pflege (2026-10-02) — die zwei Sektions-Rotationen sind kein Deko-Schritt.

Beide Rotationen (`phase1_storage` §Geerbte Contracts, `phase5_ui` §Abnahmestand) haben dieselbe
Zusicherung in zwei Hälften: **im Head steht, was jemand zum Entscheiden braucht, im Archiv steht
wortgleich, was vorher im Head stand.** Genau diese zwei Hälften halten diese Tests fest — sie
werden rot, wenn jemand später im Archiv kürzt (eine Zusicherung über den Contract verschwindet
wortlos) oder im Head auf den Zeiger verzichtet (der Abschnitt zeigt dann nichts mehr, was auf das
Archiv führt).

Sie prüfen nicht die Bytezahl: die wächst und schrumpft mit jedem Session-Block. `doc_health.py`
prüft die Bytezahl (`test_oversize_clean`), diese Tests prüfen den *Inhalt*.

**Warum `_flat()`:** die Sätze, auf die es ankommt, sind im Markdown über Zeilenumbrüche
umbrochen. Ein Test, der den Satzanfang wörtlich mit Zeilenumbruch sucht, ist rot, sobald jemand
neu umbricht — und wird dann umgangen, statt die Aussage zu prüfen.
"""
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

P1_HEAD = REPO_ROOT / "phase1_storage" / "CLAUDE.md"
P1_ARCHIVE = REPO_ROOT / "phase1_storage" / "CONTRACTS_ARCHIVE.md"
P5_HEAD = REPO_ROOT / "phase5_ui" / "CLAUDE.md"
P5_ARCHIVE = REPO_ROOT / "phase5_ui" / "ABNAHME_MATRIX_ARCHIVE.md"
INDEX = REPO_ROOT / "docs" / "INDEX.md"


def _flat(path: Path) -> str:
    return re.sub(r"\s+", " ", path.read_text(encoding="utf-8"))


# Die datierten Überschriften, unter denen die P1-Contract-Öffnungen stehen. Bewusst als Liste
# abgetippt statt aus der Datei gelesen: ein Test, der seine Erwartung aus dem subject bildet,
# prüft nichts.
P1_OPENINGS = [
    "**[2026-07-25, P2 Step 2]",
    "**[2026-08-09, P6 Step 1]",
    "**[2026-08-12, P6 Step 4]",
    "**[2026-08-17, P6 Step 7b Commit 1/3]",
    "**[2026-08-20, Phase 6.5 Step 0]",
    "**[2026-08-20, Phase 6.5 Step B1]",
    "**[2026-08-23, Phase 7 Step 0]",
    "**[2026-08-23, P7 Step A8.5]",  # im Archiv unter Phase 7 Step 0 datiert, nicht Step A8.5
    "**[2026-08-25, P7 Step C1]",
    "**[2026-08-25, P7 Step C4]",
    "**[2026-08-28, P7 Step Z]",
    "**[2026-09-01, Phase 8 Block B Step B1]",
    "**[2026-09-02, Phase 8 Step Z]",
    "**[2026-09-30, P9 Step F]",
    "**[2026-09-30, P9 Step G]",
    "**[2026-10-02, P9 Block trace]",
]

# Die Zusicherung, die wörtlich in beiden Hälften stehen muss.
P1_GUARANTEE = "Eine Änderung daran nach Phasenabschluss ist eine Scope-Änderung"
P5_STAND = "20 von 20 Abnahmezeilen ✅ live bestanden"

# Was die P5-Rotation gerettet hat. Die **vier** Nachträge der Zeile 20 stehen nicht in diesem
# Abschnitt, sondern im Session-Block darunter — das ist der Grund, warum diese Anker hier so
# genau benannt sind und nicht "die vier Nachträge".
P5_ANCHORS = [
    "| 20 | Reboot: UI, Connector, Timer kommen ohne Handgriff zurück | ✅ |",
    "Kurz:** 20 von 20 live bestanden, 0 teilweise, 0 offen.",
    "**[2026-10-02, P9 Block trace] Nachvollziehbarkeit in der Oberfläche**",
    "**[2026-08-13 Korrektur, Nikinger-Feedback aus echtem Betrieb, außerhalb eines Plan-Steps]:**",
    "Cutover auf Release-Verzeichnisse vollzogen (2026-08-05 20:37, Nikinger)",
]


def test_the_contract_section_keeps_its_name_and_its_guarantee_in_the_head():
    head = _flat(P1_HEAD)
    assert "## Geerbte Contracts" in head, "der Abschnittsname muss im Head bleiben — mehrere Pläne verweisen wörtlich darauf"
    assert P1_GUARANTEE in head, "die Abschluss-Zusicherung steht im Head, nicht nur im Archiv"


def test_the_contract_archive_holds_every_opening_verbatim():
    archive = _flat(P1_ARCHIVE)
    assert "## Geerbte Contracts" in archive
    missing = [o for o in P1_OPENINGS if o not in archive]
    assert not missing, f"im Archiv fehlen datierte Öffnungen: {missing}"


def test_the_contract_archive_carries_the_guarantee_too():
    assert P1_GUARANTEE in _flat(P1_ARCHIVE), (
        "das Archiv muss die Zusicherung ebenfalls tragen — die Rotation darf keine "
        "Zusicherung über den Contract im Head-Monopol gelassen haben"
    )


def test_the_contract_head_points_at_its_archive():
    # Der Zeiger muss *im Abschnitt* stehen, nicht nur irgendwo in der Datei: der `down:`-Eintrag
    # der L1-Card nennt das Archiv ebenfalls, und eine Suche über die ganze Datei hätte einen
    # Abschnitt ohne Zeiger als erledigt gemeldet (Gegenprobe dazu: 2026-10-02, ein eingebauter
    # Verstoss blieb zunächst unentdeckt).
    section = P1_HEAD.read_text(encoding="utf-8").split("## Geerbte Contracts", 1)[1]
    assert "CONTRACTS_ARCHIVE.md" in section, "der Abschnitt selbst muss auf sein Archiv zeigen"
    assert P1_ARCHIVE.is_file()


def test_the_abnahmestand_keeps_its_stand_in_the_head_and_its_matrix_in_the_archive():
    assert P5_STAND in _flat(P5_HEAD), "der Stand 20/20 bleibt im Head lesbar, ohne ins Archiv zu steigen"
    archive = _flat(P5_ARCHIVE)
    assert "## Abnahmestand (Plan §6) — Stand 2026-08-09" in archive
    missing = [a for a in P5_ANCHORS if a not in archive]
    assert not missing, f"im Archiv fehlen Abschnitte der Abnahmestand-Sektion: {missing}"


def test_the_abnahme_head_points_at_its_archive():
    section = P5_HEAD.read_text(encoding="utf-8").split("## Abnahmestand", 1)[1]
    assert "ABNAHME_MATRIX_ARCHIVE.md" in section, "der Abschnitt selbst muss auf sein Archiv zeigen"
    assert P5_ARCHIVE.is_file()


def test_both_archives_stand_exactly_once():
    """Gegenprobe gegen die eigene Art von Fehler: ein zweiter Schreibvorgang auf dieselbe
    Datei hatte den P5-Abschnitt im Archiv einmal doppelt abgelegt (2026-10-02, gefunden beim
    Nachlesen statt beim Suchen). Genau das darf nicht unbemerkt bleiben."""
    assert P5_ARCHIVE.read_text(encoding="utf-8").count("## Abnahmestand (Plan §6)") == 1
    assert P1_ARCHIVE.read_text(encoding="utf-8").count("## Geerbte Contracts") == 1


def test_both_archives_have_an_index_line():
    index = INDEX.read_text(encoding="utf-8")
    for rel in ("phase1_storage/CONTRACTS_ARCHIVE.md", "phase5_ui/ABNAHME_MATRIX_ARCHIVE.md"):
        assert f"](../{rel})" in index, f"{rel} fehlt in docs/INDEX.md (neue .md ⇒ INDEX-Zeile im selben Commit)"
