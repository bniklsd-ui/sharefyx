"""Tests für `backup_data_root.sh` und `restore_check.sh` (Plan §4 Step 5). Alle gegen
Wegwerf-Git-Repos unter `tmp_path` — nie gegen den echten `DATA_ROOT`.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
BACKUP_SCRIPT = REPO_ROOT / "phase3_edge" / "scripts" / "backup_data_root.sh"
RESTORE_SCRIPT = REPO_ROOT / "phase3_edge" / "scripts" / "restore_check.sh"


def _init_repo_with_commit(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    subprocess.run(["git", "-C", str(path), "config", "user.email", "test@example.com"], check=True)
    subprocess.run(["git", "-C", str(path), "config", "user.name", "Test"], check=True)
    (path / "item.md").write_text("---\nid: itm_test\n---\nInhalt\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(path), "add", "."], check=True)
    subprocess.run(["git", "-C", str(path), "commit", "-q", "-m", "initial"], check=True)


def _run_backup(data_root: Path, backup_dir: Path, keep: str | None = None) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env["SHAREFYX_DATA_ROOT"] = str(data_root)
    env["SHAREFYX_BACKUP_DIR"] = str(backup_dir)
    if keep is not None:
        env["SHAREFYX_BACKUP_KEEP"] = keep
    return subprocess.run(["bash", str(BACKUP_SCRIPT)], capture_output=True, text=True, env=env)


def _run_restore(data_root: Path, backup_dir: Path) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env["SHAREFYX_DATA_ROOT"] = str(data_root)
    env["SHAREFYX_BACKUP_DIR"] = str(backup_dir)
    return subprocess.run(["bash", str(RESTORE_SCRIPT)], capture_output=True, text=True, env=env)


@pytest.fixture
def data_root(tmp_path) -> Path:
    path = tmp_path / "data"
    _init_repo_with_commit(path)
    return path


def test_backup_creates_verifiable_bundle(tmp_path, data_root):
    backup_dir = tmp_path / "backups"

    result = _run_backup(data_root, backup_dir)

    assert result.returncode == 0, result.stderr
    bundles = list(backup_dir.glob("sharefyx-data-*.bundle"))
    assert len(bundles) == 1
    verify = subprocess.run(
        ["git", "bundle", "verify", str(bundles[0])], capture_output=True, text=True
    )
    assert verify.returncode == 0


def test_backup_emits_single_json_line_on_stdout(tmp_path, data_root):
    backup_dir = tmp_path / "backups"

    result = _run_backup(data_root, backup_dir)

    lines = [line for line in result.stdout.splitlines() if line.strip()]
    assert len(lines) == 1
    payload = json.loads(lines[0])
    assert set(payload.keys()) == {"ts", "bundle", "bytes"}
    assert payload["bytes"] > 0


def test_backup_retention_keeps_newest_n(tmp_path, data_root):
    backup_dir = tmp_path / "backups"
    backup_dir.mkdir()
    # Fünf vorgelegte Fake-Bundles mit distinktem, sortierbarem Namen — kein echter Skriptlauf
    # in einer Schleife, das wäre derselbe Zeitstempel-Kollisionsfehler wie bei mcp_smoke.py in
    # P2 (SESSIONS_ARCHIVE.md, Step 7). Der Inhalt ist für die Retention-Logik irrelevant, sie
    # sortiert und löscht nur nach Dateiname.
    for i in range(5):
        (backup_dir / f"sharefyx-data-2026010{i}T000000.000000Z.bundle").write_text("fake")

    result = _run_backup(data_root, backup_dir, keep="3")

    assert result.returncode == 0, result.stderr
    remaining = sorted(p.name for p in backup_dir.glob("sharefyx-data-*.bundle"))
    assert len(remaining) == 3
    # Die drei jüngsten bleiben: die beiden letzten Fakes + das gerade erzeugte echte Bundle.
    assert remaining[0].startswith("sharefyx-data-20260103")
    assert remaining[1].startswith("sharefyx-data-20260104")


def test_backup_fails_and_cleans_up_on_corrupt_bundle(tmp_path, data_root):
    backup_dir = tmp_path / "backups"

    fake_bin = tmp_path / "fakebin"
    fake_bin.mkdir()
    real_git_path = shutil.which("git")
    fake_git = fake_bin / "git"
    fake_git.write_text(
        "#!/usr/bin/env bash\n"
        'if [[ "$1" == "bundle" && "$2" == "verify" ]]; then\n'
        "  exit 1\n"
        "fi\n"
        f'exec "{real_git_path}" "$@"\n'
    )
    fake_git.chmod(0o755)

    env = dict(os.environ)
    env["SHAREFYX_DATA_ROOT"] = str(data_root)
    env["SHAREFYX_BACKUP_DIR"] = str(backup_dir)
    env["PATH"] = f"{fake_bin}:{env['PATH']}"

    result = subprocess.run(["bash", str(BACKUP_SCRIPT)], capture_output=True, text=True, env=env)

    assert result.returncode != 0
    assert list(backup_dir.glob("*.bundle")) == []


def test_restore_check_matches_head_and_tree(tmp_path, data_root):
    backup_dir = tmp_path / "backups"
    backup_result = _run_backup(data_root, backup_dir)
    assert backup_result.returncode == 0, backup_result.stderr

    result = _run_restore(data_root, backup_dir)

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout.strip())
    assert payload["ok"] is True
    expected_head = subprocess.run(
        ["git", "-C", str(data_root), "rev-parse", "HEAD"], capture_output=True, text=True
    ).stdout.strip()
    assert payload["head"] == expected_head


def test_restore_check_detects_divergence(tmp_path, data_root):
    backup_dir = tmp_path / "backups"
    backup_result = _run_backup(data_root, backup_dir)
    assert backup_result.returncode == 0, backup_result.stderr

    # Divergenz erzeugen: ein weiterer Commit NACH dem Backup, ohne neuen Bundle-Lauf.
    (data_root / "new.md").write_text("nach dem Backup", encoding="utf-8")
    subprocess.run(["git", "-C", str(data_root), "add", "."], check=True)
    subprocess.run(["git", "-C", str(data_root), "commit", "-q", "-m", "divergenz"], check=True)

    result = _run_restore(data_root, backup_dir)

    assert result.returncode != 0


def test_scripts_have_no_hardcoded_paths():
    for script in (BACKUP_SCRIPT, RESTORE_SCRIPT):
        text = script.read_text(encoding="utf-8")
        assert "/home/savefyx" not in text, script.name
