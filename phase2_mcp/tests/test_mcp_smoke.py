"""Testet `scripts/mcp_smoke.py` als echten Subprozess — dieselbe Begründung wie
`phase1_storage/tests/test_space_cli.py`: eine realistische Prüfung, keine In-Process-
Simulation, und das Skript ist bewusst kein Teil des `mcpserver`-Pakets. `mcp_smoke.py` baut
sein eigenes temporäres `DATA_ROOT` selbst (kein `--data-root`-Flag, siehe Skript-Docstring) —
dieser Test übergibt deshalb keins; „kein echter `DATA_ROOT`" ist hier durch das Skript selbst
garantiert, nicht durch `tmp_path`.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

SMOKE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "mcp_smoke.py"


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SMOKE_PATH), *args], capture_output=True, text=True, timeout=30
    )


def test_smoke_json_all_checks_pass():
    # Zählt nicht mit, wie viele Prüfungen es gerade gibt (Advisor-Review, Step 7) — der
    # Exit-Code trägt bereits das Pass/Fail-Signal; ein hartkodiertes `len(checks) == N` würde
    # bei jeder künftigen zusätzlichen Prüfung unnötig brechen.
    result = _run("--json")
    assert result.returncode == 0
    checks = json.loads(result.stdout)
    assert checks
    assert all(c["ok"] for c in checks), [c for c in checks if not c["ok"]]


def test_smoke_text_report_reads_all_green():
    result = _run()
    assert result.returncode == 0
    assert "fehlgeschlagen" not in result.stdout
    assert re.search(r"Alle \d+ Prüfungen grün\.", result.stdout)


def test_smoke_script_does_not_import_keyring_directly():
    """Regressionstest für die im Skript-Docstring versprochene Eigenschaft: `mcp_smoke.py`
    darf den echten Keyring nie anfassen — es benutzt ausschließlich reine Funktionen
    (`generate_token`/`hash_token`) und ein injiziertes `load_map`."""
    source = SMOKE_PATH.read_text()
    assert "import keyring" not in source
    assert "load_space_map" not in source
