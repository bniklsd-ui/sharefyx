"""P9 Step 0 — pin the doc_health scan as a test (plan §2.3).

Runs against the real repo tree (read-only, no writes, no network — same spirit as every
other doc-hygiene check in this project) plus two synthetic cases for the oversize logic's
named-exception path, since that path can't be exercised by the real repo alone.
"""
import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "doc_health.py"

spec = importlib.util.spec_from_file_location("doc_health", SCRIPT)
doc_health = importlib.util.module_from_spec(spec)
sys.modules["doc_health"] = doc_health
spec.loader.exec_module(doc_health)


@pytest.fixture(scope="module")
def report():
    return doc_health.run(REPO_ROOT)


def test_index_lines_clean(report):
    assert report["index_lines"] == []


def test_header_cards_clean(report):
    assert report["header_cards"] == []


def test_updown_links_clean(report):
    assert report["updown_links"] == []


def test_oversize_clean(report):
    assert report["oversize"] == []


def test_named_size_is_current_accepts_exact_bytes():
    line = "- [x](x) — 📗 ~43KB · foo. 43.190 B, benannt statt versteckt (P8-P)"
    assert doc_health._named_size_is_current(line, 43190) is True


def test_named_size_is_current_accepts_rounded_kb_within_tolerance():
    line = "- [x](x) — 📗 ~41KB · foo. benannt statt versteckt (P8-P)"
    assert doc_health._named_size_is_current(line, 41032) is True


def test_named_size_is_current_rejects_stale_number():
    # The real defect fixed in this session: INDEX claimed ~22KB for a 64KB file.
    line = "- [x](x) — 📗 ~22KB · foo. benannt statt versteckt (P8-P)"
    assert doc_health._named_size_is_current(line, 64401) is False


def test_oversize_finds_an_unnamed_oversize_file(tmp_path):
    repo = tmp_path
    (repo / "docs").mkdir()
    (repo / "docs" / "INDEX.md").write_text(
        "---\nstatus: live\n---\n"
        "- [big.md](../big.md) — 📗 ~50KB · nothing said about the size here\n",
        encoding="utf-8",
    )
    (repo / "big.md").write_text(
        "---\nstatus: live\npurpose: x\nread-when: x\ndetail: L2\n---\n" + ("x" * 42000),
        encoding="utf-8",
    )
    index_text = (repo / "docs" / "INDEX.md").read_text(encoding="utf-8")
    findings = doc_health.check_oversize(repo, index_text)
    assert len(findings) == 1
    assert "big.md" in findings[0]


def test_oversize_accepts_a_snapshot_glyph_regardless_of_size(tmp_path):
    repo = tmp_path
    (repo / "docs").mkdir()
    (repo / "docs" / "INDEX.md").write_text(
        "---\nstatus: live\n---\n"
        "- [snap.md](../snap.md) — 📕 ~50KB · frozen snapshot\n",
        encoding="utf-8",
    )
    (repo / "snap.md").write_text(
        "---\nstatus: snapshot\npurpose: x\nread-when: x\ndetail: L2\n---\n" + ("x" * 42000),
        encoding="utf-8",
    )
    index_text = (repo / "docs" / "INDEX.md").read_text(encoding="utf-8")
    findings = doc_health.check_oversize(repo, index_text)
    assert findings == []
