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
SYSTEMD_DIRS = (
    REPO_ROOT / "phase3_edge" / "systemd",
    REPO_ROOT / "phase4_auth" / "systemd",
    REPO_ROOT / "phase5_ui" / "systemd",  # P5 Step 1 (S7): sharefyx-purge.{service,timer}
)
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
    """**[2026-08-02 Korrektur, P5 Step 0 A]:** die zweite `LoadCredentialEncrypted`-Zeile
    (`spaces:/etc/sharefyx/spaces.cred`, reine Token-Hashes aus P2/P3) ist mit dem P5-Rückbau
    entfernt (`docs/concepts/PHASE4_CLOSEOUT_HANDOVER.md` §4.5) — die Unit braucht nur noch das
    Credential für die echten, umkehrbaren Nutzerakten-Geheimnisse (TOTP-Seeds)."""
    text = _unit_text()
    assert "LoadCredentialEncrypted=auth-users:/etc/sharefyx/auth-users.cred" in text
    assert "spaces:/etc/sharefyx/spaces.cred" not in text


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
    `phase3_edge/systemd/`, `phase4_auth/systemd/` (P4 Step 7) **und** `phase5_ui/systemd/`
    (P5 Step 1, S7-Purge-Timer) — jede neue Unit fügt sich automatisch hinzu, ohne dass diese
    Versicherung stillschweigend nur für die MCP-Unit gilt."""
    secret_shaped = re.compile(r"[A-Za-z0-9_-]{32,}")
    assert len(ALL_UNIT_PATHS) >= 5, "erwartet sharefyx-mcp + backup(.timer) + purge(.timer)"
    for path in ALL_UNIT_PATHS:
        for value in _environment_values(path.read_text(encoding="utf-8")):
            assert not secret_shaped.search(value), f"{path.name}: sieht wie ein Secret aus: {value!r}"


def test_all_units_have_no_hardcoded_machine_paths():
    """Kein `/home/savefyx`/`/home/<user>`-Pfad in einer committeten Unit — Maschinenzustand
    gehört über `local.env` eingesetzt, nicht ins Repo (Plan §5 Akzeptanzkriterium 8)."""
    for path in ALL_UNIT_PATHS:
        assert "/home/savefyx" not in path.read_text(encoding="utf-8"), path.name


def test_purge_service_is_oneshot_calling_authctl():
    """S7 (Sicherheits-Review 2026-07-29): `purge_expired()` lief bisher nur manuell über
    `authctl.py` — kein Timer, abgelaufene Zeilen verschwanden nie von selbst."""
    text = (REPO_ROOT / "phase5_ui" / "systemd" / "sharefyx-purge.service").read_text(encoding="utf-8")
    assert "Type=oneshot" in text
    assert "authctl.py purge-expired" in text
    assert "StateDirectory=sharefyx" in text
    assert "User=savefyx" in text


def test_purge_timer_runs_daily_and_persistent():
    text = (REPO_ROOT / "phase5_ui" / "systemd" / "sharefyx-purge.timer").read_text(encoding="utf-8")
    assert "OnCalendar=daily" in text
    assert "Persistent=true" in text


def test_install_script_reads_phase5_ui_systemd_dir():
    """Ein Timer, den `install_units.sh` nie installiert, ist totes Gewicht — die
    `SYSTEMD_SRCS`-Liste muss `phase5_ui/systemd` tatsächlich enthalten, nicht nur die Unit
    muss existieren."""
    text = INSTALL_SCRIPT.read_text(encoding="utf-8")
    assert "phase5_ui/systemd" in text


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
    """P4 Step 7 (2026-07-29): ohne `127.0.0.1` in `ALLOWED_HOSTS` antwortet der Dienst auf
    **jede** lokale Anfrage mit `400 Invalid host header` — das `TrustedHostMiddleware` der
    Wurzel-App bekommt genau diese Liste (`mcpserver/app.py :: create_app()`). Genau daran
    scheiterte Runbook-Schritt 4 (`oauth_smoke.py --base-url http://127.0.0.1:8765` → 4/4
    Prüfungen mit `status=400`) live beim Nikinger. **[2026-07-31, P4 Schnitt]:** ursprünglich
    stand hier „unter `AUTH_MODE=both|oauth`" — seit `TokenPathASGI`/`AuthModeASGI` entfernt sind
    (`phase4_auth/CLAUDE.md`), ist die Middleware unconditional aktiv, der Mode-Qualifier war nur
    noch für den Fixture-Wert unten (`AUTH_MODE=both`) relevant, den `install_units.sh` selbst
    unverändert nur als Platzhalterwert behandelt (kein Python-seitiges `_VALID_MODES`).

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


def test_install_script_refuses_world_writable_env(tmp_path):
    """S8 (Sicherheits-Review 2026-07-29): `local.env` gehört `savefyx`, wird aber unter `sudo`
    als root gelesen. Vorher lief das über `source` — jede Zeile, die kein `KEY=VALUE` ist
    (Shell-Metazeichen, ein zweiter Befehl), wäre als root ausgeführt worden. Der neue Parser
    liest strikt `KEY=VALUE`, führt nie Code aus — belegt hier über eine Zeile, die unter dem
    alten `source`-Verhalten eine Datei angelegt hätte."""
    phase_copy = tmp_path / "phase3_edge"
    shutil.copytree(REPO_ROOT / "phase3_edge" / "scripts", phase_copy / "scripts")
    shutil.copytree(REPO_ROOT / "phase3_edge" / "systemd", phase_copy / "systemd")
    marker = tmp_path / "PWNED"
    (phase_copy / "local.env").write_text(
        "REPO_ROOT=/tmp/repo\nDATA_ROOT=/tmp/data\nVENV=/tmp/repo/.venv\n"
        "ALLOWED_HOSTS=node.tailnet.ts.net,127.0.0.1\nAUTH_MODE=oauth\n"
        "PUBLIC_BASE_URL=https://node.tailnet.ts.net\n"
        f"touch {marker}\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        ["bash", str(phase_copy / "scripts" / "install_units.sh")],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "KEY=VALUE" in result.stderr
    assert not marker.exists()


def test_install_script_ignores_comments_and_blank_lines(tmp_path):
    """Gegenprobe: ein `local.env` im echten `local.env.example`-Stil (Kommentarblöcke,
    Leerzeilen zwischen den sechs Werten) muss weiterhin klaglos geparst werden — sonst wäre der
    strikte Parser aus dem Test oben zu strikt für den realen Anwendungsfall."""
    phase_copy = tmp_path / "phase3_edge"
    shutil.copytree(REPO_ROOT / "phase3_edge" / "scripts", phase_copy / "scripts")
    shutil.copytree(REPO_ROOT / "phase3_edge" / "systemd", phase_copy / "systemd")
    (phase_copy / "local.env").write_text(
        "# Kommentar\n\nREPO_ROOT=/tmp/repo\n\n# noch ein Kommentar\nDATA_ROOT=/tmp/data\n"
        "VENV=/tmp/repo/.venv\nALLOWED_HOSTS=node.tailnet.ts.net,127.0.0.1\nAUTH_MODE=oauth\n\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        ["bash", str(phase_copy / "scripts" / "install_units.sh")],
        capture_output=True,
        text=True,
    )

    # Kommt bis zum Pflichtfeld-Check für PUBLIC_BASE_URL durch (nicht schon an einer
    # Kommentar-/Leerzeile) — dieselbe Belegart wie die beiden Tests oben.
    assert "PUBLIC_BASE_URL ist in" in result.stderr
    assert "KEY=VALUE" not in result.stderr
