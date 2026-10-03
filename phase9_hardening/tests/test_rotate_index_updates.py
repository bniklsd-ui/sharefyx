"""P9 Step 0 (P9-L) — rotate_index_updates.sh against a synthetic tmp_path fixture.

Not run against the real docs/INDEX.md: its `updated:` chain was already drained by hand on
2026-09-19 (the script's own docstring said it "carries one entry", true that day). **[2026-10-02
correction]** it carries three again, and the first real run found a defect the fixture had never
asked about — see `test_a_second_updated_prefix_aborts_instead_of_rotating_half_the_chain`.
The fixture below carries a synthetic multi-entry chain, including a ' | ' inside an entry's
own text, so the ISO-date-anchored split is actually exercised.

**[2026-10-03, P9-Gate/Z]** The script grew an explicit target/archive pair (default unchanged:
docs/INDEX.md). The last block carries that extension and its two traps — a hardcoded pointer
(here unprovable by a naive `in`-check, by construction) and a target equal to its own archive.
"""
import re
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "rotate_index_updates.sh"

INDEX_FIXTURE = """---
status: live
purpose: test
read-when: test
detail: L0
up: ../CLAUDE.md
updated: 2026-09-20 (neuester Eintrag, mit | Pipe im Text) | 2026-09-19 (P9 aufgenommen) | 2026-09-13 (alter Eintrag)
---
# Body
Some content here.
"""

ARCHIVE_FIXTURE = """---
status: live
purpose: archive
read-when: test
detail: L3
up: ./INDEX.md
updated: 2026-09-19 (Archiv angelegt)
---
# Archive
"""


@pytest.fixture
def repo(tmp_path):
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "INDEX.md").write_text(INDEX_FIXTURE, encoding="utf-8")
    (tmp_path / "docs" / "INDEX_UPDATES_ARCHIVE.md").write_text(ARCHIVE_FIXTURE, encoding="utf-8")
    return tmp_path


def run_script(repo_root):
    return subprocess.run(
        [str(SCRIPT), str(repo_root)],
        capture_output=True,
        text=True,
    )


def test_rotate_moves_older_entries_and_keeps_the_newest(repo):
    result = run_script(repo)
    assert result.returncode == 0, result.stderr

    index_text = (repo / "docs" / "INDEX.md").read_text(encoding="utf-8")
    updated_lines = [l for l in index_text.splitlines() if l.startswith("updated: ")]
    assert len(updated_lines) == 1
    assert "2026-09-20 (neuester Eintrag, mit | Pipe im Text)" in updated_lines[0]
    assert "2026-09-19 (P9 aufgenommen)" not in updated_lines[0]
    assert "ältere Einträge: docs/INDEX_UPDATES_ARCHIVE.md" in updated_lines[0]

    # Body is untouched byte-for-byte apart from the one frontmatter line.
    assert "# Body\nSome content here.\n" in index_text
    assert index_text.count("# Body") == 1

    # Frontmatter closer stays on its own line.
    fm_lines = index_text.splitlines()
    closer_positions = [i for i, l in enumerate(fm_lines) if l == "---"]
    assert len(closer_positions) == 2


def test_rotated_entries_land_in_the_archive_byte_identical(repo):
    run_script(repo)
    archive_text = (repo / "docs" / "INDEX_UPDATES_ARCHIVE.md").read_text(encoding="utf-8")
    assert "- 2026-09-19 (P9 aufgenommen)" in archive_text
    assert "- 2026-09-13 (alter Eintrag)" in archive_text
    # newest-first: the 09-19 entry appears before the 09-13 entry
    assert archive_text.index("2026-09-19 (P9 aufgenommen)") < archive_text.index(
        "2026-09-13 (alter Eintrag)"
    )


def test_second_run_is_a_noop_exit_2(repo):
    first = run_script(repo)
    assert first.returncode == 0
    second = run_script(repo)
    assert second.returncode == 2
    assert "Bereits konform" in second.stdout


def test_missing_archive_aborts_without_touching_index(repo):
    (repo / "docs" / "INDEX_UPDATES_ARCHIVE.md").unlink()
    original = (repo / "docs" / "INDEX.md").read_text(encoding="utf-8")
    result = run_script(repo)
    assert result.returncode == 1
    assert (repo / "docs" / "INDEX.md").read_text(encoding="utf-8") == original


def test_a_second_updated_prefix_aborts_instead_of_rotating_half_the_chain(repo):
    """Der Fund vom 2026-10-02: ein Faden mit 'updated: '-Praefix ist fuer den Split-Anker
    ' | ' + ISO-Datum kein Kettenanfang. Ohne Gegenprobe rotierte der erste echte Lauf 1 von 3
    Eintraegen und meldete dabei 'verlustfrei' — die Kette sah danach konform aus und niemand
    sah nach. Also: Abbruch, kein Teil-Erfolg."""
    index = repo / "docs" / "INDEX.md"
    index.write_text(
        INDEX_FIXTURE.replace(
            " | 2026-09-19 (P9 aufgenommen) |",
            " | updated: 2026-09-19 (P9 aufgenommen) |",
        ),
        encoding="utf-8",
    )
    original = index.read_text(encoding="utf-8")
    archive_original = (repo / "docs" / "INDEX_UPDATES_ARCHIVE.md").read_text(encoding="utf-8")

    result = run_script(repo)
    assert result.returncode == 1
    assert "Faden, der mit 'updated: ' beginnt" in result.stderr
    assert index.read_text(encoding="utf-8") == original
    assert (repo / "docs" / "INDEX_UPDATES_ARCHIVE.md").read_text(encoding="utf-8") == archive_original


def test_a_chain_may_mention_the_prefix_in_its_own_prose(repo):
    """Gegenprobe zur Probe oben, und die kam einen Tag später als echter Lauf: der
    INDEX-`updated:`-Eintrag vom 2026-10-02 *beschreibt* den Defekt und nennt dabei die Zeichenkette
    ``updated: ``. Die erste Fassung der Gegenprobe suchte das nackte `updated: ` und hat den Skript
    genau daran blockiert — ein Wächter, der blinder ist als seine Behauptung. Geprueft wird darum
    nur der Fadenanfang `` | updated: <ISO>``."""
    index = repo / "docs" / "INDEX.md"
    index.write_text(
        INDEX_FIXTURE.replace(
            " | 2026-09-19 (P9 aufgenommen) |",
            " | 2026-09-19 (rotierte 1 von 3, weil ein Faden mit `updated: `-Praefix durchging) |",
        ),
        encoding="utf-8",
    )
    result = run_script(repo)
    assert result.returncode == 0, result.stderr
    assert "Kein Faden der Kette beginnt mit 'updated: '" in result.stdout
    # Der Eintrag mit der Erwaehnung ist der aeltere von zweien — er wandert ins Archiv, und genau
    # dort muss der Hinweis landen (die Erklaerung des Defekts geht nicht verloren, nur aus der Kette).
    archive_text = (repo / "docs" / "INDEX_UPDATES_ARCHIVE.md").read_text(encoding="utf-8")
    assert "rotierte 1 von 3" in archive_text
    assert "rotierte 1 von 3" not in index.read_text(encoding="utf-8")


def test_a_clean_three_entry_chain_rotates_but_the_newest(repo):
    """Gegenprobe zur Probe oben: derselbe Lauf ohne den Defekt rotiert **alle** älteren Fäden
    (hier drei von vier, denn das Fixture trägt einen vierten). Ohne diesen Test könnte (e) auch
    alles ablehnen und niemand merkte es."""
    index = repo / "docs" / "INDEX.md"
    index.write_text(
        INDEX_FIXTURE.replace(
            "updated: 2026-09-20 (neuester Eintrag, mit | Pipe im Text) | 2026-09-19 (P9 aufgenommen) |",
            "updated: 2026-09-20 (neuester) | 2026-09-19 (mittel) | 2026-09-18 (dritter) |",
        ),
        encoding="utf-8",
    )
    result = run_script(repo)
    assert result.returncode == 0, result.stderr
    assert "3 rotierte(r) Eintrag/Einträge" in result.stdout

    archive_text = (repo / "docs" / "INDEX_UPDATES_ARCHIVE.md").read_text(encoding="utf-8")
    assert "- 2026-09-19 (mittel)" in archive_text
    assert "- 2026-09-18 (dritter)" in archive_text
    assert "- 2026-09-13 (alter Eintrag)" in archive_text
    # Der jüngste Faden bleibt im Index und wandert NICHT ins Archiv.
    assert "2026-09-20 (neuester)" not in archive_text
    assert "2026-09-20 (neuester)" in index.read_text(encoding="utf-8")


# --------------------------------------------------------------------- Zieldatei/Archiv (2026-10-03)
# Vorher war das Skript auf docs/INDEX.md festgenagelt, obwohl jeder lebende Head dieselbe Kette
# trägt (phase9_hardening/CLAUDE.md: 19.488 B Kette in 57.873 B Datei). Die folgenden Tests tragen
# die Erweiterung — und die beiden Fallen, die eine naive Form davon nicht fände.

HEAD_FIXTURE = """---
status: live
purpose: test-head
read-when: test
detail: L2
up: ../CLAUDE.md
updated: 2026-10-03 (neuester, nennt selbst docs/INDEX_UPDATES_ARCHIVE.md im Text) | 2026-10-02 (zweiter) | 2026-10-01 (dritter)
---
# Head
Body bleibt unangetastet.
"""

HEAD_ARCHIVE_FIXTURE = """---
status: archive
purpose: test-archive
read-when: test
detail: L3
up: ./CLAUDE.md
updated: 2026-10-03 (Archiv angelegt)
---
"""


@pytest.fixture
def head_repo(tmp_path):
    phase = tmp_path / "phase9_hardening"
    phase.mkdir()
    (phase / "CLAUDE.md").write_text(HEAD_FIXTURE, encoding="utf-8")
    (phase / "UPDATES_ARCHIVE.md").write_text(HEAD_ARCHIVE_FIXTURE, encoding="utf-8")
    return tmp_path


def run_head_script(repo_root):
    return subprocess.run(
        [str(SCRIPT), str(repo_root), "phase9_hardening/CLAUDE.md",
         "phase9_hardening/UPDATES_ARCHIVE.md"],
        capture_output=True,
        text=True,
    )


def test_an_explicit_target_and_archive_rotate_a_living_head(head_repo):
    result = run_head_script(head_repo)
    assert result.returncode == 0, result.stderr

    head_text = (head_repo / "phase9_hardening" / "CLAUDE.md").read_text(encoding="utf-8")
    updated = [l for l in head_text.splitlines() if l.startswith("updated: ")]
    assert len(updated) == 1
    assert "2026-10-03 (neuester" in updated[0]
    assert "2026-10-02 (zweiter)" not in updated[0]
    assert "2026-10-01 (dritter)" not in updated[0]
    # Body und Frontmatter-Rahmen unangetastet
    assert head_text.count("# Head") == 1
    assert "Body bleibt unangetastet." in head_text
    assert head_text.count("---") == 2  # der Frontmatter-Rahmen des Heads, unveraendert

    archive_text = (head_repo / "phase9_hardening" / "UPDATES_ARCHIVE.md").read_text(encoding="utf-8")
    assert "- 2026-10-02 (zweiter)" in archive_text
    assert "- 2026-10-01 (dritter)" in archive_text
    assert "2026-10-03 (neuester" not in archive_text


def test_the_pointer_names_the_given_archive_not_the_index_one(head_repo):
    """Die Falle dieser Erweiterung: ein **hartkodierter** Zeiger auf `docs/INDEX_UPDATES_ARCHIVE.md`
    wäre für jeden anderen Head eine stille Lüge — die Kette zeigt dann auf ein Archiv, in dem
    ihre Einträge nicht stehen.

    Der Test ist absichtlich so gebaut, dass eine `in`-Prüfung auf `docs/INDEX_UPDATES_ARCHIVE.md`
    **nicht** grün werden kann: der jüngste Faden des Fixtures nennt diese Zeichenkette selbst im
    eigenen Text, und er bleibt stehen. Wer den Zeiger wieder hartkodiert, bekommt darum einen
    **roten** Test statt eines grünen — dieselbe Falle wie bei (e) am 2026-10-02."""
    run_head_script(head_repo)
    head_text = (head_repo / "phase9_hardening" / "CLAUDE.md").read_text(encoding="utf-8")
    updated = [l for l in head_text.splitlines() if l.startswith("updated: ")][0]
    assert "ältere Einträge: phase9_hardening/UPDATES_ARCHIVE.md" in updated
    assert updated.count("docs/INDEX_UPDATES_ARCHIVE.md") == 1  # nur die Erwähnung im Faden-Text
    # Und der Zeiger löst von der Zieldatei aus wirklich auf:
    pointer = updated.split("ältere Einträge: ")[1]
    assert (head_repo / pointer).is_file()


def test_target_and_archive_may_not_be_the_same_file(head_repo):
    """Selbst-Rotation wäre Datenverlust **ohne** Fehlermeldung: beide Schreibziele wären dieselbe
    Datei, und das zweite `cp` überschriebe den gerade gedrehten Rest der Kette."""
    head = head_repo / "phase9_hardening" / "CLAUDE.md"
    original = head.read_text(encoding="utf-8")
    result = subprocess.run(
        [str(SCRIPT), str(head_repo), "phase9_hardening/CLAUDE.md", "phase9_hardening/CLAUDE.md"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert "dieselbe Datei" in result.stderr
    assert head.read_text(encoding="utf-8") == original


def test_an_absolute_or_dotdot_path_aborts_before_writing(head_repo):
    """Der Zeiger in der neuen Zeile ist der übergebene Archivpfad wörtlich. Ein absoluter Pfad
    oder ein `..` würde dort etwas hinschreiben, das in keinem Dokument auflösbar ist."""
    head = head_repo / "phase9_hardening" / "CLAUDE.md"
    original = head.read_text(encoding="utf-8")
    for bad in ("/tmp/x.md", "../docs/INDEX_UPDATES_ARCHIVE.md"):
        result = subprocess.run(
            [str(SCRIPT), str(head_repo), "phase9_hardening/CLAUDE.md", bad],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 1, bad
        assert "repo-root-relativ" in result.stderr
    assert head.read_text(encoding="utf-8") == original


def test_a_missing_target_under_an_explicit_path_names_that_path(tmp_path):
    """Die Fehlermeldung muss den **übergebenen** Pfad nennen, nicht mehr 'Index' — sonst sucht
    jemand den Index, während das Skript an einem ganz anderen File hängengeblieben ist."""
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "INDEX_UPDATES_ARCHIVE.md").write_text(ARCHIVE_FIXTURE, encoding="utf-8")
    result = subprocess.run(
        [str(SCRIPT), str(tmp_path), "phase9_hardening/CLAUDE.md",
         "docs/INDEX_UPDATES_ARCHIVE.md"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert "phase9_hardening/CLAUDE.md" in result.stderr


def test_every_thread_of_a_living_head_chain_is_separated():
    """Fund vom 2026-10-03 — die dritte Ausprägung derselben Fehlerklasse.

    `scripts/rotate_index_updates.sh` meldete für `phase9_hardening/CLAUDE.md` **„Bereits konform:
    die 'updated:'-Kette hat nur einen Eintrag"** (exit 2), und das war *wahr* und zugleich das
    Problem: die Kette trug **zwei** Fäden, die ohne den Trenner ` | ` aneinandergeklebt waren.
    Der Split-Anker ist ` | ` + ISO-Datum, ein fehlender Trenner ist für ihn nicht von einem
    einzigen sehr langen Eintrag zu unterscheiden — und (e) kann nicht helfen, weil es das
    *Split-Ergebnis* prüft und hier nichts zu splitten ist.

    Also muss der Zustand vor dem Skript geprüft werden. Die Regel ist eng genug, um keine
    Falsch-positive zu produzieren: ein Faden **beginnt** mit `YYYY-MM-DD (**`, und eine
    Datumsnennung im Fließtext eines Fadens steht nie direkt vor `(**`.
    """
    for rel in ("CLAUDE.md", "phase9_hardening/CLAUDE.md", "phase8_6_ui_polish/CLAUDE.md"):
        body = re.search(r"^updated: (.*)$", (REPO_ROOT / rel).read_text(encoding="utf-8"), re.M).group(1)
        starts = [m.start() for m in re.finditer(r"\d{4}-\d{2}-\d{2} \(\*\*", body)]
        glued = [i for i in starts if i != 0 and not body[:i].endswith(" | ")]
        assert not glued, (
            f"{rel}: {len(glued)} Faden/Fäden ohne ' | '-Trenner (Position {glued}) — die Kette sieht für "
            f"das Skript wie ein Eintrag aus und rotiert erst beim nächsten Lauf als Ganzes ins Archiv"
        )
