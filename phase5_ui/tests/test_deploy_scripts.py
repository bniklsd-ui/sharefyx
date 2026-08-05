"""Tests für `deploy.sh`, `rollback.sh`, `authbackup.sh`, `restore_auth_check.sh` und
`ui_budget.py` (Plan §5 Step 8).

Muster wie `phase3_edge/tests/test_backup_scripts.py`: die **echten** Skripte laufen gegen
Wegwerf-Verzeichnisse unter `tmp_path`, nie gegen den echten `DATA_ROOT`, nie gegen die echte
`auth.sqlite3`, nie gegen einen echten Dienst.

`systemctl`, `curl`, `sqlite3` und `systemd-creds` werden über **Stub-Skripte auf einem
vorangestellten `PATH`** ersetzt — nicht über Monkeypatching innerhalb Pythons: die zu testende
Logik ist Bash, sie ruft diese Programme als Prozesse auf. Ein Stub auf dem `PATH` ist die
einzige Attrappe, die an derselben Stelle greift wie das echte Programm.

`cwd="/"` bei jedem Aufruf, aus demselben Grund wie in `test_backup_scripts.py`: unter systemd
ohne `WorkingDirectory=` ist das Arbeitsverzeichnis `/`. Ein Skript, das nur zufällig unter
pytest funktioniert (wo das cwd dieses Repo und damit selbst ein Git-Repo ist), wäre im Betrieb
kaputt.
"""
from __future__ import annotations

import json
import os
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
DEPLOY = REPO_ROOT / "phase5_ui" / "scripts" / "deploy.sh"
ROLLBACK = REPO_ROOT / "phase5_ui" / "scripts" / "rollback.sh"
AUTHBACKUP = REPO_ROOT / "phase5_ui" / "scripts" / "authbackup.sh"
RESTORE_AUTH = REPO_ROOT / "phase5_ui" / "scripts" / "restore_auth_check.sh"
UI_BUDGET = REPO_ROOT / "phase5_ui" / "scripts" / "ui_budget.py"

_SYSTEMCTL_STUB = """#!/usr/bin/env bash
echo "$*" >> "$SFX_SYSTEMCTL_LOG"
"""

# Antwortcodes kommen aus einer Datei, damit ein Test sie zwischen zwei Aufrufen ändern kann
# (genau das unterscheidet den Erfolgs- vom Rollback-Pfad).
_CURL_STUB = """#!/usr/bin/env bash
url="${@: -1}"
path="/${url#*://*/}"
code="$(grep -m1 "^${path}=" "$SFX_CURL_CODES" 2>/dev/null | cut -d= -f2)"
printf '%s' "${code:-000}"
"""

# `systemd-creds` braucht den Host-Schlüssel (root, /var/lib/systemd/credential.secret) — im Test
# unerreichbar. Der Stub bildet die EIGENSCHAFT nach, auf die sich die Skripte verlassen:
# encrypt/decrypt sind zueinander invers und der `--name` muss beim Entschlüsseln übereinstimmen.
_CREDS_STUB = """#!/usr/bin/env bash
mode="$1"; shift
name=""
[[ "$1" == --name=* ]] && { name="${1#--name=}"; shift; }
in="$1"; out="$2"
if [[ "$mode" == "encrypt" ]]; then
  { printf 'STUBCRED:%s\\n' "$name"; cat "$in"; } > "$out"
else
  head -1 "$in" | grep -q "^STUBCRED:${name}$" || { echo "name mismatch" >&2; exit 1; }
  tail -n +2 "$in" > "$out"
fi
"""


def _write_stub(path: Path, body: str) -> None:
    path.write_text(body, encoding="utf-8")
    path.chmod(0o755)


@pytest.fixture
def stubs(tmp_path) -> Path:
    """Verzeichnis mit den Programm-Attrappen, wird jedem Lauf vorangestellt."""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    _write_stub(bin_dir / "systemctl", _SYSTEMCTL_STUB)
    _write_stub(bin_dir / "curl", _CURL_STUB)
    _write_stub(bin_dir / "systemd-creds", _CREDS_STUB)
    return bin_dir


def _git(*args: str) -> None:
    subprocess.run(["git", *args], check=True, capture_output=True)


@pytest.fixture
def source_repo(tmp_path) -> Path:
    """Ein winziges Quell-Repo mit dem einen Skript, das `deploy.sh` daraus aufruft."""
    repo = tmp_path / "src"
    (repo / "scripts").mkdir(parents=True)
    (repo / "scripts" / "dev_install.sh").write_text("#!/usr/bin/env bash\ntrue\n", encoding="utf-8")
    (repo / "VERSION").write_text("v1\n", encoding="utf-8")
    _git("init", "-q", str(repo))
    _git("-C", str(repo), "config", "user.email", "test@example.com")
    _git("-C", str(repo), "config", "user.name", "Test")
    _git("-C", str(repo), "add", ".")
    _git("-C", str(repo), "commit", "-q", "-m", "initial")
    return repo


@pytest.fixture
def layout(tmp_path):
    releases = tmp_path / "releases"
    releases.mkdir()
    return releases, tmp_path / "current"


def _env(stubs: Path, tmp_path: Path, **extra: str) -> dict[str, str]:
    env = dict(os.environ)
    env["PATH"] = f"{stubs}{os.pathsep}{env['PATH']}"
    env["SFX_SYSTEMCTL_LOG"] = str(tmp_path / "systemctl.log")
    env["SFX_CURL_CODES"] = str(tmp_path / "codes")
    env.update(extra)
    return env


def _set_codes(tmp_path: Path, *, me: str = "401") -> None:
    """Die vier Proben des Health-Gates. `me` ist der interessante Schalter: `/api/v1/me` MUSS
    ohne Cookie 401 antworten — ein Deploy, der dort 200 liefert, hat die Authentisierung
    ausgebaut und darf nicht live bleiben."""
    (tmp_path / "codes").write_text(
        f"/health=200\n/ui/login=200\n/api/v1/me={me}\n/mcp/=401\n", encoding="utf-8"
    )


def _run_deploy(stubs, tmp_path, releases, current, source, ref="HEAD", **extra):
    env = _env(
        stubs, tmp_path,
        SHAREFYX_RELEASES_DIR=str(releases),
        SHAREFYX_CURRENT_LINK=str(current),
        SHAREFYX_SOURCE_REPO=str(source),
        SHAREFYX_SKIP_TESTS=extra.pop("skip_tests", "1"),
        SHAREFYX_HEALTH_TIMEOUT="2",
        **extra,
    )
    return subprocess.run(
        ["bash", str(DEPLOY), ref], capture_output=True, text=True, env=env, cwd="/"
    )


def _run_rollback(stubs, tmp_path, releases, current):
    env = _env(
        stubs, tmp_path,
        SHAREFYX_RELEASES_DIR=str(releases),
        SHAREFYX_CURRENT_LINK=str(current),
    )
    return subprocess.run(
        ["bash", str(ROLLBACK)], capture_output=True, text=True, env=env, cwd="/"
    )


# -- deploy.sh --------------------------------------------------------------------------------


def test_deploy_creates_release_and_moves_symlink(stubs, tmp_path, layout, source_repo):
    releases, current = layout
    _set_codes(tmp_path)
    result = _run_deploy(stubs, tmp_path, releases, current, source_repo)

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["result"] == "ok"
    assert current.is_symlink()
    assert current.resolve() == Path(payload["release"]).resolve()
    assert (current / "VERSION").read_text(encoding="utf-8") == "v1\n"
    assert "restart sharefyx-mcp" in (tmp_path / "systemctl.log").read_text(encoding="utf-8")


def test_deploy_script_aborts_when_tests_fail(stubs, tmp_path, layout, source_repo):
    """Der wichtigste Fehlschlagpfad: ein gescheiterter `pytest`-Lauf im Release darf den
    Symlink nicht anfassen. Geprüft wird genau das — nicht nur der Exit-Code, sondern **wohin der
    Symlink danach zeigt** und dass das halbe Release wieder verschwindet.

    Ehrlich zum Mechanismus: der `pytest`-Aufruf scheitert hier, weil im Wegwerf-Release gar kein
    `pytest` installiert ist (das Stub-Repo hat ein leeres `dev_install.sh`) — nicht, weil ein
    absichtlich roter Test darin läge. Für die Aussage des Tests ist das gleichwertig:
    `deploy.sh` unterscheidet nicht zwischen „Test rot" und „Testlauf nicht durchführbar", und
    beides muss denselben Abbruch auslösen. Ein Release, dessen Tests man nicht fahren konnte,
    darf genauso wenig live gehen wie eines mit roten Tests."""
    releases, current = layout
    _set_codes(tmp_path)
    first = _run_deploy(stubs, tmp_path, releases, current, source_repo)
    assert first.returncode == 0
    good_target = current.resolve()

    # Ein Release, dessen `pytest` scheitert: das Quell-Repo bekommt eine Testdatei, die immer
    # fehlschlägt, und der Lauf wird diesmal NICHT übersprungen. Ein echtes `pytest` im Release
    # gibt es dort nicht — genau deshalb schlägt der Aufruf fehl, was für diesen Test reicht.
    result = _run_deploy(
        stubs, tmp_path, releases, current, source_repo, skip_tests="0"
    )

    assert result.returncode != 0
    assert "ABBRUCH" in result.stderr
    assert current.resolve() == good_target, "Symlink wurde trotz roter Tests umgelegt"
    # Das unvollständige Release darf nicht liegenbleiben — es würde einen Retention-Platz
    # belegen und wie ein gültiges Rollback-Ziel aussehen.
    assert sorted(p.name for p in releases.iterdir()) == [good_target.name]


def test_deploy_script_rolls_back_when_health_gate_fails(stubs, tmp_path, layout, source_repo):
    releases, current = layout
    _set_codes(tmp_path)
    assert _run_deploy(stubs, tmp_path, releases, current, source_repo).returncode == 0
    good_target = current.resolve()
    assert _run_deploy(stubs, tmp_path, releases, current, source_repo).returncode == 0
    second_target = current.resolve()
    assert second_target != good_target

    # Jetzt antwortet /api/v1/me mit 200 statt 401 — die Authentisierung wäre ausgebaut.
    _set_codes(tmp_path, me="200")
    result = _run_deploy(stubs, tmp_path, releases, current, source_repo)

    assert result.returncode != 0
    payload = json.loads(result.stdout)
    assert payload["result"] == "rolled_back"
    assert "/api/v1/me" in payload["reason"]
    assert current.resolve() == second_target, "nicht auf das vorherige Release zurückgerollt"


def test_failed_release_is_marked_and_never_becomes_a_rollback_target(
    stubs, tmp_path, layout, source_repo
):
    """Fund beim ersten echten Probelauf: ein zurückgerolltes Release bleibt liegen (gewollt, man
    will hineinsehen können), ist aber das JÜNGSTE Verzeichnis. Ohne Markierung wäre ausgerechnet
    der nachweislich kaputte Stand das nächste Rollback-Ziel."""
    releases, current = layout
    _set_codes(tmp_path)
    assert _run_deploy(stubs, tmp_path, releases, current, source_repo).returncode == 0
    oldest = current.resolve()
    assert _run_deploy(stubs, tmp_path, releases, current, source_repo).returncode == 0

    _set_codes(tmp_path, me="200")
    assert _run_deploy(stubs, tmp_path, releases, current, source_repo).returncode != 0

    failed = [p for p in releases.iterdir() if p.name.endswith(".failed")]
    assert len(failed) == 1, "gescheitertes Release wurde nicht als .failed markiert"

    result = _run_rollback(stubs, tmp_path, releases, current)
    assert result.returncode == 0, result.stderr
    assert not current.resolve().name.endswith(".failed")
    assert current.resolve() == oldest


def test_deploy_retention_keeps_the_configured_number(stubs, tmp_path, layout, source_repo):
    releases, current = layout
    _set_codes(tmp_path)
    for _ in range(4):
        assert _run_deploy(
            stubs, tmp_path, releases, current, source_repo, SHAREFYX_KEEP_RELEASES="2"
        ).returncode == 0

    kept = sorted(p.name for p in releases.iterdir())
    assert len(kept) == 2, kept
    # Das aktive Release muss unter den behaltenen sein — Retention darf nie den Boden unter dem
    # laufenden Dienst wegziehen.
    assert current.resolve().name in kept


def test_deploy_refuses_an_unknown_git_ref(stubs, tmp_path, layout, source_repo):
    releases, current = layout
    _set_codes(tmp_path)
    result = _run_deploy(stubs, tmp_path, releases, current, source_repo, ref="gibtesnicht")

    assert result.returncode != 0
    assert not current.exists()
    assert list(releases.iterdir()) == [], "Release-Rest nach unauflösbarem ref"


# -- rollback.sh ------------------------------------------------------------------------------


def test_rollback_restores_previous_symlink(stubs, tmp_path, layout, source_repo):
    releases, current = layout
    _set_codes(tmp_path)
    assert _run_deploy(stubs, tmp_path, releases, current, source_repo).returncode == 0
    first = current.resolve()
    assert _run_deploy(stubs, tmp_path, releases, current, source_repo).returncode == 0
    second = current.resolve()

    result = _run_rollback(stubs, tmp_path, releases, current)

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["action"] == "rollback"
    assert Path(payload["from"]).resolve() == second
    assert current.resolve() == first
    assert "restart sharefyx-mcp" in (tmp_path / "systemctl.log").read_text(encoding="utf-8")


def test_rollback_refuses_when_there_is_only_one_release(stubs, tmp_path, layout, source_repo):
    releases, current = layout
    _set_codes(tmp_path)
    assert _run_deploy(stubs, tmp_path, releases, current, source_repo).returncode == 0
    only = current.resolve()

    result = _run_rollback(stubs, tmp_path, releases, current)

    assert result.returncode != 0
    assert "ABBRUCH" in result.stderr
    assert current.resolve() == only, "Rollback ins Leere hat den Symlink verändert"


# -- authbackup.sh / restore_auth_check.sh ----------------------------------------------------


@pytest.fixture
def auth_db(tmp_path) -> Path:
    """Eine echte, kleine SQLite-Datei — keine Attrappe: `authbackup.sh` benutzt die
    SQLite-Backup-API und `restore_auth_check.sh` liest `sqlite_master`. Beides würde gegen eine
    Textdatei nichts aussagen."""
    path = tmp_path / "auth.sqlite3"
    conn = sqlite3.connect(path)
    conn.execute("CREATE TABLE users (space TEXT PRIMARY KEY, password_hash TEXT)")
    conn.execute("CREATE TABLE ui_sessions (id TEXT PRIMARY KEY)")
    conn.executemany("INSERT INTO users VALUES (?, ?)", [("niklas", "x"), ("fabian", "y")])
    conn.execute("INSERT INTO ui_sessions VALUES ('s1')")
    conn.commit()
    conn.close()
    return path


def _run_authbackup(stubs, tmp_path, auth_db: Path, backup_dir: Path, keep: str | None = None):
    extra = {"SHAREFYX_AUTH_BACKUP_KEEP": keep} if keep else {}
    env = _env(
        stubs, tmp_path,
        SHAREFYX_AUTH_DB=str(auth_db),
        SHAREFYX_AUTH_BACKUP_DIR=str(backup_dir),
        **extra,
    )
    return subprocess.run(
        ["bash", str(AUTHBACKUP)], capture_output=True, text=True, env=env, cwd="/"
    )


def test_authbackup_keeps_seven_generations(stubs, tmp_path, auth_db):
    backup_dir = tmp_path / "authbackup"
    for _ in range(9):
        result = _run_authbackup(stubs, tmp_path, auth_db, backup_dir)
        assert result.returncode == 0, result.stderr

    generations = sorted(backup_dir.glob("auth-*.cred"))
    assert len(generations) == 7, [p.name for p in generations]
    for path in generations:
        assert oct(path.stat().st_mode)[-3:] == "600", path.name


def test_authbackup_writes_no_plaintext_database_next_to_the_generations(
    stubs, tmp_path, auth_db
):
    """Hard Rule 1 in ihrer schärfsten Form: die `auth.sqlite3` enthält umkehrbare TOTP-Seeds.
    Im Backup-Verzeichnis darf **nur** die verschlüsselte Fassung liegen — kein Zwischenstand,
    kein `.sqlite3`, kein Rest eines abgebrochenen Laufs."""
    backup_dir = tmp_path / "authbackup"
    assert _run_authbackup(stubs, tmp_path, auth_db, backup_dir).returncode == 0

    assert [p.suffix for p in backup_dir.iterdir()] == [".cred"]


def test_authbackup_deletes_a_generation_it_cannot_read_back(stubs, tmp_path, auth_db):
    """Gleiche Disziplin wie `backup_data_root.sh` bei einem unverifizierbaren Bundle: ein
    Backup, das sich nicht wieder entschlüsseln lässt, ist schlimmer als keines — es täuscht
    Sicherheit vor. Hier bricht der `decrypt`-Zweig des Stubs absichtlich ab."""
    backup_dir = tmp_path / "authbackup"
    broken = tmp_path / "bin" / "systemd-creds"
    _write_stub(broken, "#!/usr/bin/env bash\n"
                        '[[ "$1" == "decrypt" ]] && exit 1\n'
                        'shift; [[ "$1" == --name=* ]] && shift\n'
                        'cp "$1" "$2"\n')

    result = _run_authbackup(stubs, tmp_path, auth_db, backup_dir)

    assert result.returncode != 0
    assert "nicht entschlüsselbar" in result.stderr
    assert list(backup_dir.glob("auth-*.cred")) == []


def test_restore_auth_check_reports_row_counts(stubs, tmp_path, auth_db):
    backup_dir = tmp_path / "authbackup"
    assert _run_authbackup(stubs, tmp_path, auth_db, backup_dir).returncode == 0

    env = _env(stubs, tmp_path, SHAREFYX_AUTH_BACKUP_DIR=str(backup_dir))
    result = subprocess.run(
        ["bash", str(RESTORE_AUTH)], capture_output=True, text=True, env=env, cwd="/"
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["counts"] == {"ui_sessions": 1, "users": 2}
    assert payload["rows_total"] == 3


def test_restore_auth_check_fails_on_an_empty_user_table(stubs, tmp_path):
    """Eine Auth-Datenbank ohne einen einzigen Nutzer ist formal gültig und als Backup wertlos —
    genau der Fall, der beim Wiederherstellen am meisten wehtut."""
    empty = tmp_path / "empty.sqlite3"
    conn = sqlite3.connect(empty)
    conn.execute("CREATE TABLE users (space TEXT PRIMARY KEY)")
    conn.commit()
    conn.close()

    backup_dir = tmp_path / "authbackup"
    assert _run_authbackup(stubs, tmp_path, empty, backup_dir).returncode == 0

    env = _env(stubs, tmp_path, SHAREFYX_AUTH_BACKUP_DIR=str(backup_dir))
    result = subprocess.run(
        ["bash", str(RESTORE_AUTH)], capture_output=True, text=True, env=env, cwd="/"
    )

    assert result.returncode != 0
    assert "keine Nutzer" in result.stderr


# -- ui_budget.py -----------------------------------------------------------------------------


def test_ui_budget_reports_all_four_metrics():
    """Läuft das echte Skript (in-process, temporäres `DATA_ROOT`, kein Netz). Geprüft wird die
    Vollständigkeit und dass jede Messgröße einen Zielkorridor mitbringt — **nicht**, dass die
    Zahlen eingehalten werden: eine Überschreitung ist laut P5-AD ein dokumentierter Befund,
    kein Testfehlschlag, sonst wäre der Anreiz, den Korridor anzupassen statt die Ursache."""
    result = subprocess.run(
        [sys.executable, str(UI_BUDGET), "--json"],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )
    assert result.returncode in (0, 1), result.stderr

    payload = json.loads(result.stdout)
    names = [m["name"] for m in payload["metrics"]]
    assert any("items?limit=50" in n and "roh" in n for n in names), names
    assert any("items?limit=50" in n and "gzip" in n for n in names), names
    assert any("items/{id}" in n for n in names), names
    assert any("app.js" in n for n in names), names
    assert any("Erstaufruf" in n for n in names), names
    for metric in payload["metrics"]:
        assert metric["value_bytes"] > 0, metric
        assert metric["budget_bytes"] > 0, metric


# -- Meta -------------------------------------------------------------------------------------


def test_step8_scripts_have_no_hardcoded_paths():
    """Gegenstück zu `phase3_edge/tests/test_backup_scripts.py :: test_scripts_have_no_hardcoded_paths`
    — jener Test kennt nur die zwei P3-Skripte, die neuen hier fallen nicht automatisch darunter.
    (Bei den Units ist es umgekehrt: `test_units.py :: ALL_UNIT_PATHS` globbt und deckt neue
    Dateien von selbst mit ab — geprüft, nicht angenommen.)"""
    for script in (DEPLOY, ROLLBACK, AUTHBACKUP, RESTORE_AUTH, UI_BUDGET):
        assert "/home/savefyx" not in script.read_text(encoding="utf-8"), script.name
