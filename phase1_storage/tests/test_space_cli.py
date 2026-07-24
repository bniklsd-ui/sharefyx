"""Testet `scripts/space_cli.py` als echten Subprozess -- die CLI ist kein Teil des `storage`-
Pakets (bewusst kein `packages=["scripts"]` in pyproject.toml, siehe Kommentar im Skript und
Session-Block: Namenskollision über künftige Phasen hinweg), deshalb per `sys.executable` +
Skriptpfad statt Import. Das ist zugleich die realistischste Prüfung für "die CLI als Beweis"
(Plan §4 Step 7) -- ein echter Aufruf, keine In-Process-Simulation.

Jeder Test bekommt sein `--data-root` ausschließlich über pytest's `tmp_path` -- nie den echten
DATA_ROOT (Hard Rule).
"""
import json
import subprocess
import sys
from pathlib import Path

CLI_PATH = Path(__file__).resolve().parents[1] / "scripts" / "space_cli.py"


def _run(tmp_path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CLI_PATH), "--data-root", str(tmp_path), *args],
        capture_output=True, text=True,
    )


def test_create_and_show_text_output(tmp_path):
    # Setup über --json (robust), geprüft wird die Text-Ausgabe von "show" -- das ist der
    # eigentliche Testgegenstand. Nicht die ID aus dem Text-Format herausparsen (koppelt den
    # Test an die genaue Zeilenform von `_print_item_text`, statt an ihr Verhalten).
    created = _run(tmp_path, "create", "nikinger", "--type", "task", "--title", "Testaufgabe", "--json")
    assert created.returncode == 0
    item_id = json.loads(created.stdout)["id"]

    shown = _run(tmp_path, "show", item_id)
    assert shown.returncode == 0
    assert item_id in shown.stdout
    assert "Testaufgabe" in shown.stdout
    assert "task" in shown.stdout


def test_create_and_search_json_output(tmp_path):
    _run(tmp_path, "create", "nikinger", "--type", "note", "--title", "Notiz", "--tag", "infra")

    result = _run(tmp_path, "search", "--json")
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["total"] == 1
    assert payload["items"][0]["title"] == "Notiz"
    assert payload["items"][0]["tags"] == ["infra"]
    assert "body" not in payload["items"][0]


def test_list_shows_space_counts(tmp_path):
    _run(tmp_path, "create", "nikinger", "--type", "task", "--title", "A")
    _run(tmp_path, "create", "nikinger", "--type", "task", "--title", "B")
    _run(tmp_path, "create", "kollege", "--type", "note", "--title", "C")

    result = _run(tmp_path, "list", "--json")
    assert result.returncode == 0
    spaces = {s["name"]: s["item_count"] for s in json.loads(result.stdout)}
    assert spaces == {"nikinger": 2, "kollege": 1}


def test_update_bumps_version(tmp_path):
    created = _run(tmp_path, "create", "nikinger", "--type", "task", "--title", "Alt", "--json")
    item = json.loads(created.stdout)

    updated = _run(
        tmp_path, "update", item["id"], "--version", str(item["version"]),
        "--title", "Neu", "--json",
    )
    assert updated.returncode == 0
    payload = json.loads(updated.stdout)
    assert payload["title"] == "Neu"
    assert payload["version"] == item["version"] + 1


def test_archive_sets_status(tmp_path):
    created = _run(tmp_path, "create", "nikinger", "--type", "note", "--title", "X", "--json")
    item = json.loads(created.stdout)

    archived = _run(tmp_path, "archive", item["id"], "--version", str(item["version"]), "--json")
    assert archived.returncode == 0
    payload = json.loads(archived.stdout)
    assert payload["status"] == "archived"


def test_reindex_reports_stats(tmp_path):
    _run(tmp_path, "create", "nikinger", "--type", "task", "--title", "A")
    _run(tmp_path, "create", "nikinger", "--type", "task", "--title", "B")

    result = _run(tmp_path, "reindex", "--json")
    assert result.returncode == 0
    stats = json.loads(result.stdout)
    assert stats["items_indexed"] == 2


def test_conflict_returns_exit_code_2_with_comprehensible_message(tmp_path):
    created = _run(tmp_path, "create", "nikinger", "--type", "task", "--title", "Original", "--json")
    item = json.loads(created.stdout)
    _run(tmp_path, "update", item["id"], "--version", str(item["version"]), "--title", "Geändert")

    stale = _run(tmp_path, "update", item["id"], "--version", str(item["version"]), "--title", "Nochmal")

    assert stale.returncode == 2
    assert item["id"] in stale.stderr
    assert "Geändert" in stale.stderr  # der aktuelle Titel steckt in der Konflikt-Meldung
    assert stale.stdout == ""


def test_item_not_found_returns_exit_code_1(tmp_path):
    result = _run(tmp_path, "show", "itm_deadbeef")

    assert result.returncode == 1
    assert "itm_deadbeef" in result.stderr
    assert result.stdout == ""


def test_json_flag_works_after_subcommand(tmp_path):
    """Regressionsschutz: der erste Wurf des Skripts erlaubte `--json` nur *vor* dem Subcommand
    (globaler Parser-Flag) -- `search --json` scheiterte mit 'unrecognized arguments'. Gefunden
    beim manuellen Smoke-Test, gefixt über `parents=[common]` auf jedem Subparser.
    """
    _run(tmp_path, "create", "nikinger", "--type", "task", "--title", "A")

    result = _run(tmp_path, "search", "--json")

    assert result.returncode == 0
    json.loads(result.stdout)  # wirft nicht
