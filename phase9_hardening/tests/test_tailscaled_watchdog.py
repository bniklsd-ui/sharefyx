"""Tests for phase3_edge/scripts/tailscaled_watchdog.sh — P9-Plan §4.3.

Fünf Tests, einer pro Zeile der §4.3-Tabelle:

  1. test_online_node_triggers_no_restart
  2. test_offline_node_triggers_restart
  3. test_restart_is_rate_limited_to_once_per_15_minutes
  4. test_netcheck_is_only_called_when_status_is_not_clearly_online
  5. test_unit_file_has_the_three_hardening_directives

Mock-Mechanik: ein tmp `bin/`-Verzeichnis mit Stub-Skripten für `tailscale`,
`systemctl`, `date`, `timeout`. Das tmp-Bin wird in PATH vorne angehängt; das
Skript selbst ruft nichts Subprozess-Spezifisches ohne PATH-Lookup. `python3`
(nur für die JSON-Auswertung in Stufe 1) bleibt ungerührt — es ist im
Test-PATH vorhanden, der venv-pytest-PATH erbt die System-PATH.

Kein Netz, kein echter Dienst, kein root. Die `STATE_FILE` zeigen wir auf eine
tmp-Datei, die `RuntimeDirectory=`-Konvention des Units spielt hier keine Rolle.

V152-Antwort (separat): Tailscale hat kein eigenes Watchdog-Feature ohne
kommerzielles Add-on — Eigenbau ist nötig. V153 (Polkit vs. sudoers) ist
Empfehlung im Plan §4.2-Body, kein Testgegenstand (Polkit-Konfiguration lebt
außerhalb des Repos unter /etc/polkit-1/rules.d/).
"""

from __future__ import annotations

import os
import re
import stat
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
WATCHDOG_SCRIPT = REPO_ROOT / "phase3_edge" / "scripts" / "tailscaled_watchdog.sh"
WATCHDOG_SERVICE = REPO_ROOT / "phase3_edge" / "systemd" / "tailscaled-watchdog.service"
WATCHDOG_TIMER = REPO_ROOT / "phase3_edge" / "systemd" / "tailscaled-watchdog.timer"


def _write_executable(path: Path, body: str) -> Path:
    path.write_text(body)
    current = path.stat().st_mode
    path.chmod(current | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return path


def _make_mock_bin(
    base: Path,
    *,
    online: str = "true",          # "true" | "false" | "unclear"
    json_status_rc: int = 0,       # Exit-Code von `tailscale status --json`
    netcheck_rc: int = 0,          # Exit-Code von `tailscale netcheck`
) -> tuple[Path, Path]:
    """Baut ein tmp bin/-Verzeichnis mit Mock-Binaries.

    Rückgabe: (bin_dir, calls_log). `calls_log` sammelt alle systemctl- und
    netcheck-Aufrufe zeilenweise — Tests assertieren darauf.
    """
    bin_dir = base / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    calls_log = base / "calls.log"
    calls_log.touch()
    calls_log.touch()

    if online == "true":
        json_body = '\'{"Self":{"Online":true}}\''
    elif online == "false":
        json_body = '\'{"Self":{"Online":false}}\''
    else:
        json_body = '"this-is-not-json"'

    tailscale_mock = f"""#!/usr/bin/env bash
case "$1" in
    status)
        if [ "$2" = "--json" ]; then
            echo {json_body}
            exit {json_status_rc}
        fi
        ;;
    netcheck)
        echo "netcheck $*" >> "{calls_log}"
        exit {netcheck_rc}
        ;;
esac
exit 1
"""
    _write_executable(bin_dir / "tailscale", tailscale_mock)

    systemctl_mock = f"""#!/usr/bin/env bash
echo "systemctl $*" >> "{calls_log}"
"""
    _write_executable(bin_dir / "systemctl", systemctl_mock)

    date_mock = """#!/usr/bin/env bash
case "$1" in
    +%s)
        echo "${TAILSCALED_WATCHDOG_TEST_EPOCH:-1000}"
        ;;
    -u)
        shift
        /bin/date -u "$@" 2>/dev/null || echo "1970-01-01T00:00:00Z"
        ;;
    *)
        exec /bin/date "$@"
        ;;
esac
exit 0
"""
    _write_executable(bin_dir / "date", date_mock)

    timeout_mock = """#!/usr/bin/env bash
# Erstes Argument ist die Timeout-Dauer — wegwerfen, Rest ausführen.
shift
exec "$@"
"""
    _write_executable(bin_dir / "timeout", timeout_mock)

    return bin_dir, calls_log


def _run_watchdog(
    bin_dir: Path,
    state_file: Path,
    *,
    epoch: int = 1000,
    rate_limit: int = 900,
) -> subprocess.CompletedProcess:
    """Startet das Watchdog-Skript mit PATH=bin_dir:... und Test-State."""
    env = os.environ.copy()
    env["PATH"] = f"{bin_dir}:{env.get('PATH', '')}"
    env["TAILSCALED_WATCHDOG_STATE_FILE"] = str(state_file)
    env["TAILSCALED_WATCHDOG_RATE_LIMIT"] = str(rate_limit)
    env["TAILSCALED_WATCHDOG_NETCHECK_TIMEOUT"] = "30"
    env["TAILSCALED_WATCHDOG_TEST_EPOCH"] = str(epoch)
    return subprocess.run(
        ["bash", str(WATCHDOG_SCRIPT)],
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
    )


def _parse_calls(calls_log: Path) -> tuple[list[str], list[str]]:
    """Gibt (systemctl_calls, netcheck_calls) aus dem Mock-Log zurück."""
    if not calls_log.exists():
        return [], []
    lines = calls_log.read_text().splitlines()
    systemctl = [l[len("systemctl "):] for l in lines if l.startswith("systemctl ")]
    netcheck = [l[len("netcheck "):] for l in lines if l.startswith("netcheck ")]
    return systemctl, netcheck


# --- Test 1 -----------------------------------------------------------------

def test_online_node_triggers_no_restart(tmp_path):
    """Online=true → kein Restart, kein netcheck (Stufe 1 entscheidet)."""
    bin_dir, calls_log = _make_mock_bin(tmp_path, online="true")
    state = tmp_path / "state"
    state.touch()

    result = _run_watchdog(bin_dir, state)

    systemctl_calls, netcheck_calls = _parse_calls(calls_log)
    assert result.returncode == 0, f"unexpected exit: {result.returncode}\nstderr: {result.stderr}"
    assert "healthy" in result.stdout, f"missing 'healthy' in: {result.stdout!r}"
    assert systemctl_calls == [], f"expected 0 restarts, got: {systemctl_calls}"
    assert netcheck_calls == [], f"expected 0 netcheck (Online=true is decisive), got: {netcheck_calls}"


# --- Test 2 -----------------------------------------------------------------

def test_offline_node_triggers_restart(tmp_path):
    """Online=false → genau 1 Restart (Stufe 1 entscheidet, Stufe 2 entfällt)."""
    bin_dir, calls_log = _make_mock_bin(tmp_path, online="false")
    state = tmp_path / "state"
    # Netcheck ist im Mock auf "fail" gesetzt — das ist hier irrelevant, weil
    # der Plan §4.2 Netcheck nur bei unklarer Stufe 1 ruft. Wir setzen den
    # Mock-Wert trotzdem explizit (für Lesbarkeit des Test-Namens) und
    # assertieren unten, dass netcheck NICHT gerufen wurde.
    state.touch()

    result = _run_watchdog(bin_dir, state)

    systemctl_calls, netcheck_calls = _parse_calls(calls_log)
    assert result.returncode == 0, f"unexpected exit: {result.returncode}\nstderr: {result.stderr}"
    assert "unhealthy" in result.stdout, f"missing 'unhealthy' in: {result.stdout!r}"
    assert len(systemctl_calls) == 1, f"expected exactly 1 restart, got: {systemctl_calls}"
    assert "restart tailscaled.service" in systemctl_calls[0], \
        f"wrong systemctl verb/unit: {systemctl_calls[0]!r}"
    assert state.read_text().strip() != "", "state file should hold the timestamp after restart"
    assert netcheck_calls == [], \
        f"netcheck must NOT be called when Online=false (Stufung §4.2), got: {netcheck_calls}"


# --- Test 3 -----------------------------------------------------------------

def test_restart_is_rate_limited_to_once_per_15_minutes(tmp_path):
    """Zwei Ausfälle innerhalb des 15-min-Fensters → 1 Restart, 1 Rate-Limit."""
    bin_dir, calls_log = _make_mock_bin(tmp_path, online="false")
    state = tmp_path / "state"

    # Erster Lauf: Restart (kein vorheriger State).
    r1 = _run_watchdog(bin_dir, state, epoch=1000, rate_limit=900)
    # Zweiter Lauf 300 s später — innerhalb des Fensters.
    r2 = _run_watchdog(bin_dir, state, epoch=1300, rate_limit=900)

    systemctl_calls, _ = _parse_calls(calls_log)
    assert len(systemctl_calls) == 1, \
        f"rate limit failed: expected exactly 1 restart, got: {systemctl_calls}"
    assert "rate-limited" in r2.stdout, \
        f"second run should report rate-limit, got: {r2.stdout!r}"
    assert "unhealthy" in r1.stdout and "tailscaled restarted" in r1.stdout, \
        f"first run should have restarted, got: {r1.stdout!r}"


# --- Test 4 -----------------------------------------------------------------

def test_netcheck_is_only_called_when_status_is_not_clearly_online(tmp_path):
    """Stufung aus §4.2: netcheck NUR bei unclear. Online=true/-false: kein netcheck."""
    # Sub-Case A: Online=true — netcheck entfällt.
    base_a = tmp_path / "a"
    bin_a, calls_a = _make_mock_bin(base_a, online="true")
    _run_watchdog(bin_a, base_a / "state")
    _, net_a = _parse_calls(calls_a)
    assert net_a == [], f"Online=true should not trigger netcheck, got: {net_a}"

    # Sub-Case B: Online=false — netcheck entfällt (definitive Aussage, direkt zu Stufe 3).
    base_b = tmp_path / "b"
    bin_b, calls_b = _make_mock_bin(base_b, online="false", netcheck_rc=1)
    _run_watchdog(bin_b, base_b / "state")
    _, net_b = _parse_calls(calls_b)
    assert net_b == [], f"Online=false should skip netcheck (Stufung §4.2), got: {net_b}"

    # Sub-Case C: status unclear — netcheck WIRD gerufen.
    base_c = tmp_path / "c"
    bin_c, calls_c = _make_mock_bin(base_c, online="unclear", netcheck_rc=1)
    _run_watchdog(bin_c, base_c / "state")
    _, net_c = _parse_calls(calls_c)
    assert len(net_c) == 1, f"unclear should trigger exactly 1 netcheck, got: {net_c}"


# --- Test 5 -----------------------------------------------------------------

def test_unit_file_has_the_three_hardening_directives():
    """Statischer Wächter auf die .service-Unit: User=, NoNewPrivileges, ProtectSystem."""
    content = WATCHDOG_SERVICE.read_text()

    # Plan §4.2 nennt drei Härtungs-Direktiven wörtlich: `User=`, `NoNewPrivileges=true`,
    # `ProtectSystem=strict`. `User=savefyx` ist hier die Konkretisierung.
    assert re.search(r"^User=savefyx\s*$", content, re.MULTILINE), \
        "expected `User=savefyx` in the unit"
    assert re.search(r"^NoNewPrivileges=true\s*$", content, re.MULTILINE), \
        "expected `NoNewPrivileges=true` in the unit"
    assert re.search(r"^ProtectSystem=strict\s*$", content, re.MULTILINE), \
        "expected `ProtectSystem=strict` in the unit"

    # Sanity: Timer existiert und hat OnUnitActiveSec (sonst ist die ganze Übung sinnlos).
    timer_content = WATCHDOG_TIMER.read_text()
    assert re.search(r"^OnUnitActiveSec=\S+", timer_content, re.MULTILINE), \
        "timer missing OnUnitActiveSec — watchdog wouldn't actually fire"
    assert re.search(r"^Unit=tailscaled-watchdog\.service\s*$", timer_content, re.MULTILINE), \
        "timer must reference tailscaled-watchdog.service"


# --- Tests 6-9: die polkit-Regel (P9 Step B, V153, 2026-09-30) --------------------
#
# Warum es diese vier überhaupt braucht: der Watchdog läuft als `User=savefyx` und darf
# `systemctl restart tailscaled.service` — dafür braucht er eine Autorisierung, und auf
# dieser Box (systemd 255) ist die passende Aktion die **grobe**
# `org.freedesktop.systemd1.manage-units`, nicht `manager.restart-unit`. Ein XML-`<defaults>`
# kann danach nicht filtern; nur eine JS-Regel kann, über `action.lookup("unit")`.
# Ohne Wächter wandert der Unit-Abgleich bei der nächsten Politur weg und `savefyx` kann
# plötzlich **alle** Units der Maschine verwalten — von `sharefyx-mcp` aus.
#
# Alle vier Wächter lesen **nur Codezeilen**: die Regel enthält dieselben Begriffe in ihren
# Kommentaren (Befund-Notizen), und ein Test, der Kommentare mitliest, prüft meine
# Formulierung statt der Absicht. Dieselbe Falle wie in P8.6 Block H und P9 Step G.

POLKIT_RULE = REPO_ROOT / "phase3_edge" / "polkit" / "49-tailscaled-watchdog-restart.rules"
PROBE_RULE = REPO_ROOT / "phase9_hardening" / "step_b" / "99-tailscaled-watchdog-probe.rules"
PROBE_UNIT = REPO_ROOT / "phase9_hardening" / "step_b" / "sharefyx-watchdog-probe.service"

# Die Nachbar-Aktionen desselben systemd-255-Aktionssatzes. Quelle: die lokal installierte
# /usr/share/polkit-1/actions/org.freedesktop.systemd1.policy und der Manpage-Abschnitt
# "Security" in org.freedesktop.systemd1(5) (gelesen 2026-09-30).
NEIGHBOUR_ACTIONS = (
    "org.freedesktop.systemd1.manage-unit-files",
    "org.freedesktop.systemd1.set-environment",
    "org.freedesktop.systemd1.reload-daemon",
    "org.freedesktop.systemd1.bypass-dump-ratelimit",
)


def _code_only(path: Path) -> str:
    """Der Datei-Inhalt ohne Kommentarzeilen.

    `//` für die beiden polkit-Regeln, `#` für die systemd-Unit. Zeilenweise gefiltert
    statt per Regex über den ganzen Text — ein `//` in einem Pfad darf keine Zeile
    verschlucken.
    """
    kept = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("//") or stripped.startswith("#"):
            continue
        kept.append(line)
    return "\n".join(kept)


def _add_rule_blocks(code: str) -> list[str]:
    """Die Rümpfe jeder `polkit.addRule(...)`-Funktion, ohne Kommentare."""
    blocks = re.split(r"polkit\.addRule\(", code)
    return [b for b in blocks[1:] if "return" in b]


# --- Test 6 -----------------------------------------------------------------

def test_the_polkit_rule_grants_exactly_one_action_one_unit_one_user():
    """Jeder addRule-Block prüft Aktion, Unit und User — und sonst nichts.

    Die Reihenfolge ist zusätzlich Teil der Zusicherung: der Unit-Abgleich steht vor dem
    `return YES`. Ein Block, der `YES` zurückgibt, ohne vorher `unit` und `subject.user`
    geprüft zu haben, ist genau die Rechteausweitung, die hier nicht gebaut wird.
    """
    code = _code_only(POLKIT_RULE)
    blocks = _add_rule_blocks(code)
    assert len(blocks) == 2, f"erwartet: die Aktionen dieser Box und die eines neuen systemd, gefunden: {len(blocks)}"

    for block in blocks:
        aktion = re.search(r'action\.id\s*!==\s*"([^"]+)"', block)
        unit = re.search(r'action\.lookup\("unit"\)\s*!==\s*"([^"]+)"', block)
        user = re.search(r'subject\.user\s*!==\s*"([^"]+)"', block)
        assert aktion and unit and user, f"Block prüft nicht Aktion+Unit+User: {block.strip()[:200]}"
        assert unit.group(1) == "tailscaled.service", f"Rule grants unit {unit.group(1)!r}"
        assert user.group(1) == "savefyx", f"Rule grants user {user.group(1)!r}"

        # Jeder Ausgang ist YES oder DEFAULT, es gibt genau ein YES, und es ist der letzte:
        # ein früher `return YES` vor den Prüfungen wäre die Ausnahme, gegen die der Test da ist.
        returns = re.findall(r"return (polkit\.Result\.\w+);", block)
        assert set(returns) <= {"polkit.Result.YES", "polkit.Result.DEFAULT"}, \
            f"unbekannter Ausgang: {returns}"
        assert returns.count("polkit.Result.YES") == 1, f"mehr als ein YES-Ausgang: {returns}"
        assert returns[-1] == "polkit.Result.YES", \
            f"das YES muss der letzte Ausgang sein, ist es aber nicht: {returns}"


# --- Test 7 -----------------------------------------------------------------

def test_the_polkit_rule_and_the_watchdog_name_the_same_unit_and_user():
    """Regel und Skript/Unit dürfen nicht auseinanderlaufen.

    Der historische Nachbar dieser Wächter ist der Port-Test beim tail-proxy („der Port darf
    nicht auseinanderlaufen"). Hier sind es drei Namen: das Skript startet eine Unit, die
    Unit läuft als ein User, und die Regel nennt Unit und User. Wird eines davon umbenannt,
    greift die Regel ins Leere und der Watchdog kann seinen einzigen Zweck nicht erfüllen —
    still, weil Stufe 1 im gesunden Fall nie weiterläuft.
    """
    code = _code_only(POLKIT_RULE)
    units = set(re.findall(r'action\.lookup\("unit"\)\s*!==\s*"([^"]+)"', code))
    users = set(re.findall(r'subject\.user\s*!==\s*"([^"]+)"', code))
    assert units == {"tailscaled.service"}, f"die Regel muss genau eine Unit nennen, nennt: {units}"
    assert users == {"savefyx"}, f"die Regel muss genau einen User nennen, nennt: {users}"

    # Was das Skript wirklich aufruft — der Name, den die Regel treffen muss.
    script = _code_only(WATCHDOG_SCRIPT)
    restarts = re.findall(r"systemctl restart ([\w.-]+)", script)
    assert restarts == ["tailscaled.service"], f"Skript startet andere Units: {restarts}"

    # Und der User aus der Unit, gegen den die Regel prüft.
    unit_user = re.search(r"^User=(\S+)\s*$", _code_only(WATCHDOG_SERVICE), re.MULTILINE)
    assert unit_user and unit_user.group(1) in users, \
        f"die Unit laeuft als {unit_user and unit_user.group(1)!r}, die Regel kennt {users}"


# --- Test 8 -----------------------------------------------------------------

def test_the_polkit_rule_does_not_touch_the_neighbour_actions():
    """Die drei anderen Unit-Aktionen dieses systemd bleiben unberührt.

    Wer `manage-units` freigibt, hat nicht nur Restart im Kopf — derselbe Aufrufkanal
    kann Units anhalten, maskieren, die Environment des Managers setzen oder den Daemon
    reloaden. Diese Namen dürfen deshalb **nicht** im Code der Regel vorkommen (in den
    Kommentaren schon: dort steht, warum sie ausgepartet bleiben).
    """
    code = _code_only(POLKIT_RULE)
    for action in NEIGHBOUR_ACTIONS:
        assert action not in code, f"die Regel fasst {action} an — das ist nicht der Auftrag"


# --- Test 9 -----------------------------------------------------------------

def test_the_probe_never_names_the_real_unit():
    """Die V153-Probe darf tailscaled nicht nennen — sonst wäre sie die Sache, vor der sie warnt.

    Die Probe beweist an `ExecStart=/bin/true`, ob systemd der polkit-Aktion das
    `unit`-Attribut mitgibt. Würde sie `tailscaled.service` nennen, hinge an ihr genau der
    Neustart, den sie vermeiden soll. Der Test liest wieder nur Code, nicht die Warnung
    im Kommentar darüber.
    """
    for path in (PROBE_RULE, PROBE_UNIT):
        code = _code_only(path)
        assert "tailscaled" not in code.replace("tailscaled-watchdog", ""), \
            f"{path.name} nennt tailscaled im Code — die Probe muss folgenlos sein"
        assert path.exists(), f"{path} fehlt — ohne sie ist die V153-Frage nicht entscheidbar"
    # Und sie muss die Wegwerf-Unit auch wirklich benennen, sonst prüft sie nichts.
    assert "sharefyx-watchdog-probe.service" in _code_only(PROBE_RULE)
    assert re.search(r"^ExecStart=/bin/true\s*$", _code_only(PROBE_UNIT), re.MULTILINE), \
        "die Probe-Unit muss etwas folgenloses tun"
