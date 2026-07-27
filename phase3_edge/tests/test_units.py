"""Tests für die systemd-Units und `install_units.sh` (Plan §4 Step 4). Reines Textparsen für
die Unit-Datei — kein systemd nötig. `install_units.sh` läuft nur in seinem Abbruchpfad (fehlende
`local.env`), nie bis zu `systemctl`/`/etc` — die echte Installation ist Step 7, Sache des
Nikingers.
"""
from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
UNIT_PATH = REPO_ROOT / "phase3_edge" / "systemd" / "sharefyx-mcp.service"
INSTALL_SCRIPT = REPO_ROOT / "phase3_edge" / "scripts" / "install_units.sh"
ALL_UNIT_PATHS = sorted((REPO_ROOT / "phase3_edge" / "systemd").glob("*.service")) + sorted(
    (REPO_ROOT / "phase3_edge" / "systemd").glob("*.timer")
)


def _unit_text() -> str:
    return UNIT_PATH.read_text(encoding="utf-8")


def _environment_values(text: str) -> list[str]:
    return [line.split("=", 1)[1] for line in text.splitlines() if line.startswith("Environment=")]


def test_unit_restarts_on_failure():
    text = _unit_text()
    assert "Restart=on-failure" in text
    assert "RestartSec=" in text


def test_unit_loads_credential_encrypted():
    text = _unit_text()
    assert "LoadCredentialEncrypted=spaces:/etc/sharefyx/spaces.cred" in text


def test_unit_binds_loopback_only():
    text = _unit_text()
    assert "Environment=SPACE_HOST=127.0.0.1" in text
    assert "0.0.0.0" not in text


def test_unit_has_no_secret_shaped_value():
    """Regex-Versicherung gegen den Token-Klartext-Vorfall aus P2 (zweimal passiert): kein
    `Environment=`-Wert sieht wie ein Token/Secret aus. Platzhalter (`__REPO_ROOT__`, 13 Zeichen)
    und Pfade fallen nicht darunter, ein versehentlich eingetragenes 256-Bit-Token schon."""
    secret_shaped = re.compile(r"[A-Za-z0-9_-]{32,}")
    for value in _environment_values(_unit_text()):
        assert not secret_shaped.search(value), f"sieht wie ein Secret aus: {value!r}"


def test_unit_placeholders_are_unresolved_in_repo():
    text = _unit_text()
    for placeholder in ("__REPO_ROOT__", "__DATA_ROOT__", "__VENV__", "__ALLOWED_HOSTS__"):
        assert placeholder in text


def test_all_units_have_no_secret_shaped_value():
    """Wie `test_unit_has_no_secret_shaped_value`, aber über **alle** Unit-Dateien in
    `phase3_edge/systemd/` — Step 5 (Backup) fügt zwei weitere hinzu, ohne dass diese
    Versicherung stillschweigend nur für die MCP-Unit gilt."""
    secret_shaped = re.compile(r"[A-Za-z0-9_-]{32,}")
    assert len(ALL_UNIT_PATHS) >= 3, "erwartet mindestens sharefyx-mcp + sharefyx-backup(.timer)"
    for path in ALL_UNIT_PATHS:
        for value in _environment_values(path.read_text(encoding="utf-8")):
            assert not secret_shaped.search(value), f"{path.name}: sieht wie ein Secret aus: {value!r}"


def test_all_units_have_no_hardcoded_machine_paths():
    """Kein `/home/savefyx`/`/home/<user>`-Pfad in einer committeten Unit — Maschinenzustand
    gehört über `local.env` eingesetzt, nicht ins Repo (Plan §5 Akzeptanzkriterium 8)."""
    for path in ALL_UNIT_PATHS:
        assert "/home/savefyx" not in path.read_text(encoding="utf-8"), path.name


def test_install_script_refuses_without_local_env(tmp_path):
    """Kopiert `scripts/` + `systemd/` in ein Wegwerf-Verzeichnis OHNE `local.env` und ruft das
    Skript von dort auf — hermetisch, unabhängig davon, ob auf dieser Maschine zufällig ein
    echtes `phase3_edge/local.env` existiert. Der Abbruch passiert vor jedem `/etc`- oder
    `systemctl`-Zugriff."""
    phase_copy = tmp_path / "phase3_edge"
    shutil.copytree(REPO_ROOT / "phase3_edge" / "scripts", phase_copy / "scripts")
    shutil.copytree(REPO_ROOT / "phase3_edge" / "systemd", phase_copy / "systemd")

    result = subprocess.run(
        ["bash", str(phase_copy / "scripts" / "install_units.sh")],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "local.env" in result.stderr
