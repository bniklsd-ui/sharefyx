"""Wächter für `phase10_5_finishing/scripts/register_bilanz.py` (P10.5-59, Block 12).

1. Im echten Register trägt jede P10.5-Zeile einen Marker (✅ / ⚠️ / ⬜).
2. Gegenprobe: eine P10.5-Zeile ohne Marker wird gefunden und lässt das Skript scheitern.
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "phase10_5_finishing" / "scripts" / "register_bilanz.py"

_spec = importlib.util.spec_from_file_location("register_bilanz", SCRIPT)
register_bilanz = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(register_bilanz)


def test_every_p105_row_in_the_real_register_carries_a_marker():
    report = register_bilanz.bilanz(REPO_ROOT)
    assert report["ohne_marker"] == []
    assert report["p105_zeilen"] == report["✅"] + report["⚠️"] + report["⬜"]
    assert report["p105_zeilen"] > 0


def _fake_repo(tmp_path: Path, ziel: str) -> Path:
    (tmp_path / "phase10_inventory").mkdir()
    (tmp_path / "phase10_inventory" / "BAUSTELLENREGISTER.md").write_text(
        "| ID | Posten | Herkunft | Befund | Gr. | Risiko | Entsch. | Ziel |\n|---|---|---|---|---|---|---|---|\n"
        f"| XX-1 | Posten | Quelle | Befund | S | S | nein | {ziel} |\n",
        encoding="utf-8")
    return tmp_path


def test_a_p105_row_without_marker_is_found_and_the_script_fails(tmp_path):
    root = _fake_repo(tmp_path, "P10.5 (Doku-Block)")
    assert register_bilanz.bilanz(root)["ohne_marker"] == ["XX-1"]
    result = subprocess.run([sys.executable, str(SCRIPT), str(root)], capture_output=True, text=True)
    assert result.returncode == 1


def test_a_marked_row_passes(tmp_path):
    root = _fake_repo(tmp_path, "✅ 10-57 (B12) · P10.5 (Doku-Block)")
    report = register_bilanz.bilanz(root)
    assert report["ohne_marker"] == [] and report["✅"] == 1
