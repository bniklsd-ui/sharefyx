"""Tests für die systemd-Units und `install_units.sh` (Plan §4 Step 4). Reines Textparsen für
die Unit-Datei — kein systemd nötig. `install_units.sh` läuft nur in seinem Abbruchpfad (fehlende
`local.env`), nie bis zu `systemctl`/`/etc` — die echte Installation ist Step 7, Sache des
Nikingers.

**[2026-07-29 Korrektur, P4 Step 7]:** `sharefyx-mcp.service` zog nach `phase4_auth/systemd/`
um (Plan §5 Step 7: „ERSETZT die P3-Fassung" — inhaltlich jetzt eine P4-Unit, StateDirectory +
zweites Credential). `install_units.sh` bleibt P3-Eigentum, liest aber jetzt aus zwei
Verzeichnissen; `UNIT_PATH`/`ALL_UNIT_PATHS` unten folgen dem, kein Test-Verhalten geändert,
nur der Quellpfad.
"""
from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
UNIT_PATH = REPO_ROOT / "phase4_auth" / "systemd" / "sharefyx-mcp.service"
INSTALL_SCRIPT = REPO_ROOT / "phase3_edge" / "scripts" / "install_units.sh"
SYSTEMD_DIRS = (REPO_ROOT / "phase3_edge" / "systemd", REPO_ROOT / "phase4_auth" / "systemd")
ALL_UNIT_PATHS = sorted(
    path for d in SYSTEMD_DIRS for path in (*d.glob("*.service"), *d.glob("*.timer"))
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
    # P4 Step 7: zweites Credential für die Nutzerakten (TOTP-Seeds, echte umkehrbare Geheimnisse
    # — anders als die reinen Token-Hashes hinter "spaces").
    assert "LoadCredentialEncrypted=auth-users:/etc/sharefyx/auth-users.cred" in text


def test_unit_declares_state_directory():
    """P4 Step 7: `StateDirectory=sharefyx` liefert `$STATE_DIRECTORY` (`/var/lib/sharefyx`),
    genau das, was `authserver/config.py :: load_auth_settings()` für die Auth-SQLite liest —
    kein zusätzliches `Environment=SPACE_AUTH_DB=` nötig, systemd exportiert die Variable
    selbst."""
    text = _unit_text()
    assert "StateDirectory=sharefyx" in text
    assert "StateDirectoryMode=0700" in text


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
    for placeholder in (
        "__REPO_ROOT__", "__DATA_ROOT__", "__VENV__", "__ALLOWED_HOSTS__",
        "__AUTH_MODE__", "__PUBLIC_BASE_URL__",  # P4 Step 7
    ):
        assert placeholder in text


def test_all_units_have_no_secret_shaped_value():
    """Wie `test_unit_has_no_secret_shaped_value`, aber über **alle** Unit-Dateien in
    `phase3_edge/systemd/` **und** `phase4_auth/systemd/` (P4 Step 7) — Step 5 (Backup) fügt
    zwei weitere hinzu, ohne dass diese Versicherung stillschweigend nur für die MCP-Unit gilt."""
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
    `systemctl`-Zugriff — noch vor dem Zwei-Verzeichnis-Glob (P4 Step 7), `phase4_auth/systemd/`
    muss deshalb in dieser hermetischen Kopie nicht existieren, um diesen Pfad zu beweisen."""
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


def test_install_script_warns_when_allowed_hosts_lacks_loopback(tmp_path):
    """P4 Step 7 (2026-07-29): ohne `127.0.0.1` in `ALLOWED_HOSTS` antwortet der Dienst unter
    `AUTH_MODE=both|oauth` auf **jede** lokale Anfrage mit `400 Invalid host header` — das
    `TrustedHostMiddleware` der Wurzel-App bekommt genau diese Liste (`mcpserver/app.py ::
    create_app()`). Genau daran scheiterte Runbook-Schritt 4 (`oauth_smoke.py --base-url
    http://127.0.0.1:8765` → 4/4 Prüfungen mit `status=400`) live beim Nikinger.

    Hermetisch wie der Test darüber: die `local.env` lässt `PUBLIC_BASE_URL` weg, damit das
    Skript nach der Warnung am Pflichtfeld-Check abbricht — die Warnung ist damit belegt, ohne
    dass das Skript je `/etc` oder `systemctl` erreicht.
    """
    phase_copy = tmp_path / "phase3_edge"
    shutil.copytree(REPO_ROOT / "phase3_edge" / "scripts", phase_copy / "scripts")
    shutil.copytree(REPO_ROOT / "phase3_edge" / "systemd", phase_copy / "systemd")
    (phase_copy / "local.env").write_text(
        "REPO_ROOT=/tmp/repo\nDATA_ROOT=/tmp/data\nVENV=/tmp/repo/.venv\n"
        "ALLOWED_HOSTS=node.tailnet.ts.net\nAUTH_MODE=both\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        ["bash", str(phase_copy / "scripts" / "install_units.sh")],
        capture_output=True,
        text=True,
    )

    assert "WARNUNG" in result.stderr and "127.0.0.1" in result.stderr
    assert result.returncode != 0
    assert "PUBLIC_BASE_URL" in result.stderr


def test_install_script_stays_quiet_when_loopback_present(tmp_path):
    """Gegenprobe zum Test darüber: mit `127.0.0.1` in der Liste erscheint die Warnung nicht.
    Ohne diese Hälfte würde ein Skript, das *immer* warnt, den Test oben ebenfalls bestehen."""
    phase_copy = tmp_path / "phase3_edge"
    shutil.copytree(REPO_ROOT / "phase3_edge" / "scripts", phase_copy / "scripts")
    shutil.copytree(REPO_ROOT / "phase3_edge" / "systemd", phase_copy / "systemd")
    (phase_copy / "local.env").write_text(
        "REPO_ROOT=/tmp/repo\nDATA_ROOT=/tmp/data\nVENV=/tmp/repo/.venv\n"
        "ALLOWED_HOSTS=node.tailnet.ts.net,127.0.0.1\nAUTH_MODE=both\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        ["bash", str(phase_copy / "scripts" / "install_units.sh")],
        capture_output=True,
        text=True,
    )

    assert "WARNUNG" not in result.stderr
    assert result.returncode != 0  # bricht weiterhin an PUBLIC_BASE_URL ab
