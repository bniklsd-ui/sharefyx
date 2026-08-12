"""Tests für `phase6_shares/scripts/migrate_visibility.py` (Plan §4 Step 6, §2.3) — immer gegen
ein Wegwerf-`tmp_path`, nie gegen den echten `DATA_ROOT`.
"""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]


def _load_script(name: str):
    script_path = REPO_ROOT / "phase6_shares" / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


migrate_visibility = _load_script("migrate_visibility")


def _clean_environ() -> dict[str, str]:
    return {
        k: v for k, v in os.environ.items()
        if not k.startswith("SHAREFYX_") and not k.startswith("SFX_")
    }


_ITEM_TEXT = """---
id: itm_aaaaaaaa
space: niklas
type: note
title: Alt
status: active
tags: []
links: []
created: '2026-01-01T00:00:00Z'
updated: '2026-01-01T00:00:00Z'
version: 3
---
Body-Inhalt, unveraendert.
"""

_ITEM_TEXT_ALREADY_HUMAN = """---
id: itm_bbbbbbbb
space: niklas
type: note
title: Schon gesetzt
status: active
visibility: human
tags: []
links: []
created: '2026-01-01T00:00:00Z'
updated: '2026-01-01T00:00:00Z'
version: 1
---
Body zwei.
"""


@pytest.fixture
def data_root(tmp_path) -> Path:
    root = tmp_path / "data"
    (root / "niklas").mkdir(parents=True)
    (root / "niklas" / "itm_aaaaaaaa__alt.md").write_text(_ITEM_TEXT, encoding="utf-8")
    (root / "niklas" / "itm_bbbbbbbb__schon-gesetzt.md").write_text(
        _ITEM_TEXT_ALREADY_HUMAN, encoding="utf-8"
    )
    return root


@pytest.fixture
def env(data_root) -> dict[str, str]:
    e = _clean_environ()
    e["SPACE_DATA_ROOT"] = str(data_root)
    return e


def _git_log(data_root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(data_root), "log", "--oneline"], capture_output=True, text=True,
    )
    return result.stdout.splitlines()


def test_dry_run_is_default_and_writes_nothing(data_root, env, capsys):
    original = (data_root / "niklas" / "itm_aaaaaaaa__alt.md").read_text(encoding="utf-8")
    code = migrate_visibility.main([], env=env)  # kein --apply
    assert code == migrate_visibility.EXIT_OK
    assert (data_root / "niklas" / "itm_aaaaaaaa__alt.md").read_text(encoding="utf-8") == original
    assert not (data_root / ".git").exists()  # kein ensure_repo, kein Commit im Dry-Run


def test_dry_run_report_names_only_the_item_missing_visibility(data_root, env, capsys):
    migrate_visibility.main([], env=env)
    out = capsys.readouterr().out
    lines = [json.loads(line) for line in out.splitlines()]
    rows = [row for row in lines if not row.get("summary")]
    assert len(rows) == 1
    assert rows[0]["id"] == "itm_aaaaaaaa"
    assert rows[0]["before"] is None
    assert rows[0]["after"] == "private"
    summary = [row for row in lines if row.get("summary")][0]
    assert summary["dry_run"] is True
    assert summary["items_migrated"] == 1
    assert summary["spaces_touched"] == ["niklas"]


def test_apply_writes_visibility_private_and_preserves_version_and_body(data_root, env):
    migrate_visibility.main(["--apply"], env=env)
    text = (data_root / "niklas" / "itm_aaaaaaaa__alt.md").read_text(encoding="utf-8")
    assert "visibility: private" in text
    assert "version: 3" in text  # kein Versionssprung (Moduldocstring)
    assert "Body-Inhalt, unveraendert." in text


def test_apply_does_not_touch_an_item_that_already_has_visibility(data_root, env):
    original = (data_root / "niklas" / "itm_bbbbbbbb__schon-gesetzt.md").read_text(encoding="utf-8")
    migrate_visibility.main(["--apply"], env=env)
    after = (data_root / "niklas" / "itm_bbbbbbbb__schon-gesetzt.md").read_text(encoding="utf-8")
    assert after == original
    assert "visibility: human" in after


def test_apply_creates_exactly_one_commit_per_space_not_per_item(data_root, env):
    (data_root / "niklas" / "itm_cccccccc__drittes.md").write_text(
        _ITEM_TEXT.replace("itm_aaaaaaaa", "itm_cccccccc"), encoding="utf-8"
    )
    migrate_visibility.main(["--apply"], env=env)
    log = _git_log(data_root)
    migrate_commits = [line for line in log if "migrate visibility [niklas]" in line]
    assert len(migrate_commits) == 1


def test_apply_across_two_spaces_produces_two_commits(data_root, env):
    (data_root / "fabian").mkdir()
    (data_root / "fabian" / "itm_dddddddd__viertes.md").write_text(
        _ITEM_TEXT.replace("itm_aaaaaaaa", "itm_dddddddd").replace("space: niklas", "space: fabian"),
        encoding="utf-8",
    )
    migrate_visibility.main(["--apply"], env=env)
    log = _git_log(data_root)
    assert any("migrate visibility [niklas]" in line for line in log)
    assert any("migrate visibility [fabian]" in line for line in log)


def test_missing_data_root_aborts_with_named_variable(capsys):
    env_without = {k: v for k, v in _clean_environ().items() if k != "SPACE_DATA_ROOT"}
    code = migrate_visibility.main([], env=env_without)
    assert code == migrate_visibility.EXIT_ERROR
    assert "SPACE_DATA_ROOT" in capsys.readouterr().err


def test_data_root_flag_overrides_env(tmp_path, env, data_root):
    other_root = tmp_path / "other"
    (other_root / "solo").mkdir(parents=True)
    (other_root / "solo" / "itm_eeeeeeee__x.md").write_text(
        _ITEM_TEXT.replace("itm_aaaaaaaa", "itm_eeeeeeee").replace("space: niklas", "space: solo"),
        encoding="utf-8",
    )
    migrate_visibility.main(["--data-root", str(other_root), "--apply"], env=env)
    text = (other_root / "solo" / "itm_eeeeeeee__x.md").read_text(encoding="utf-8")
    assert "visibility: private" in text
    # der env-DATA_ROOT (niklas) blieb unberührt
    original = (data_root / "niklas" / "itm_aaaaaaaa__alt.md").read_text(encoding="utf-8")
    assert "visibility: private" not in original
