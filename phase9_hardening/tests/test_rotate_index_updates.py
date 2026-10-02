"""P9 Step 0 (P9-L) — rotate_index_updates.sh against a synthetic tmp_path fixture.

Not run against the real docs/INDEX.md: its `updated:` chain was already drained by hand on
2026-09-19 (the script's own docstring said it "carries one entry", true that day). **[2026-10-02
correction]** it carries three again, and the first real run found a defect the fixture had never
asked about — see `test_a_second_updated_prefix_aborts_instead_of_rotating_half_the_chain`.
The fixture below carries a synthetic multi-entry chain, including a ' | ' inside an entry's
own text, so the ISO-date-anchored split is actually exercised.
"""
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
    assert "zweites 'updated: '-Praefix" in result.stderr
    assert index.read_text(encoding="utf-8") == original
    assert (repo / "docs" / "INDEX_UPDATES_ARCHIVE.md").read_text(encoding="utf-8") == archive_original


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
