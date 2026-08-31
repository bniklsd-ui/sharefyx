"""Tests für `phase6_shares/scripts/spacectl.py` (Plan §4 Step 6) — CLI, immer gegen ein
Wegwerf-`tmp_path`, nie gegen den echten `DATA_ROOT`. `main(argv, env=...)` nimmt ein
injiziertes Environment entgegen (gleiches Muster wie `authctl.py`) — kein Test hier liest
`os.environ` direkt.
"""
from __future__ import annotations

import importlib.util
import os
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]


def _load_script(name: str):
    """Lädt ein Skript aus `phase6_shares/scripts/` per Pfad — dieselbe Begründung wie
    `phase4_auth/tests/test_authctl.py :: _load_script`: die Skripte liegen in keinem
    Python-Paket."""
    script_path = REPO_ROOT / "phase6_shares" / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


spacectl = _load_script("spacectl")


def _clean_environ() -> dict[str, str]:
    """Umgebung ohne `SHAREFYX_*`/`SFX_*` des Aufrufers (P5-Lehre: ein exportierter Wert hat
    einmal die Produktivsuite dazu gebracht, den Dienst 52x neu zu starten — dieses Skript
    startet zwar nichts über systemd, dieselbe Disziplin gilt trotzdem für jede Umgebung, die
    an `main()` gereicht wird)."""
    return {
        k: v for k, v in os.environ.items()
        if not k.startswith("SHAREFYX_") and not k.startswith("SFX_")
    }


@pytest.fixture
def data_root(tmp_path) -> Path:
    return tmp_path / "data"


@pytest.fixture
def env(data_root) -> dict[str, str]:
    e = _clean_environ()
    e["SPACE_DATA_ROOT"] = str(data_root)
    return e


def _share_yml(space_dir: Path) -> dict:
    return yaml.safe_load((space_dir / ".share.yml").read_text(encoding="utf-8"))


# -- DATA_ROOT-Auflösung ------------------------------------------------------------------


def test_missing_data_root_aborts_with_named_variable(capsys):
    env_without = {k: v for k, v in _clean_environ().items() if k != "SPACE_DATA_ROOT"}
    code = spacectl.main(["list-spaces"], env=env_without)
    assert code == spacectl.EXIT_ERROR
    err = capsys.readouterr().err
    assert "SPACE_DATA_ROOT" in err


def test_data_root_flag_overrides_env(tmp_path, env):
    other_root = tmp_path / "other"
    other_root.mkdir()
    code = spacectl.main(["--data-root", str(other_root), "create-space", "team"], env=env)
    assert code == spacectl.EXIT_OK
    assert (other_root / "team").is_dir()


# -- create-space / list-spaces / show ----------------------------------------------------


def test_create_space_then_appears_in_list_with_zero_items(data_root, env, capsys):
    data_root.mkdir()
    assert spacectl.main(["create-space", "dritter"], env=env) == spacectl.EXIT_OK
    assert (data_root / "dritter").is_dir()
    capsys.readouterr()
    assert spacectl.main(["list-spaces", "--json"], env=env) == spacectl.EXIT_OK
    out = capsys.readouterr().out
    assert '"name": "dritter"' in out
    assert '"item_count": 0' in out


def test_create_space_rejects_duplicate(data_root, env, capsys):
    data_root.mkdir()
    spacectl.main(["create-space", "dritter"], env=env)
    capsys.readouterr()
    code = spacectl.main(["create-space", "dritter"], env=env)
    assert code == spacectl.EXIT_ERROR
    assert "existiert bereits" in capsys.readouterr().err


def test_create_space_rejects_path_traversal_name(data_root, env, capsys):
    data_root.mkdir()
    code = spacectl.main(["create-space", "../escape"], env=env)
    assert code == spacectl.EXIT_ERROR
    assert not (data_root.parent / "escape").exists()


def test_show_on_unknown_space_reports_absent_directory(data_root, env, capsys):
    data_root.mkdir()
    assert spacectl.main(["show", "nirgends"], env=env) == spacectl.EXIT_OK
    out = capsys.readouterr().out
    assert "Verzeichnis vorhanden: False" in out


# -- add-member / remove-member ------------------------------------------------------------


def test_add_member_write_implies_read_without_duplication(data_root, env):
    data_root.mkdir()
    spacectl.main(["create-space", "niklas"], env=env)
    spacectl.main(["create-space", "fabian"], env=env)
    code = spacectl.main(["add-member", "niklas", "fabian", "--write"], env=env)
    assert code == spacectl.EXIT_OK
    data = _share_yml(data_root / "niklas")
    assert data["write"] == ["fabian"]
    assert "read" not in data  # write impliziert read (Plan §1.2.2) -- keine Dopplung


def test_add_member_read_only_does_not_grant_write(data_root, env):
    data_root.mkdir()
    spacectl.main(["create-space", "niklas"], env=env)
    spacectl.main(["create-space", "fabian"], env=env)
    spacectl.main(["add-member", "niklas", "fabian", "--read"], env=env)
    data = _share_yml(data_root / "niklas")
    assert data["read"] == ["fabian"]
    assert "write" not in data


def test_add_member_creates_exactly_one_git_commit(data_root, env):
    data_root.mkdir()
    spacectl.main(["create-space", "niklas"], env=env)
    spacectl.main(["add-member", "niklas", "fabian", "--write"], env=env)
    log = _git_log(data_root)
    assert sum(1 for line in log if "share niklas write+=fabian" in line) == 1


def test_add_member_unknown_target_space_warns_but_still_writes(data_root, env, capsys):
    data_root.mkdir()
    spacectl.main(["create-space", "niklas"], env=env)
    capsys.readouterr()
    code = spacectl.main(["add-member", "niklas", "trudy", "--read"], env=env)
    assert code == spacectl.EXIT_OK
    assert "WARNUNG" in capsys.readouterr().err
    assert _share_yml(data_root / "niklas")["read"] == ["trudy"]


def test_add_member_on_unknown_source_space_aborts(data_root, env, capsys):
    data_root.mkdir()
    code = spacectl.main(["add-member", "nirgends", "fabian", "--write"], env=env)
    assert code == spacectl.EXIT_ERROR
    assert not (data_root / "nirgends").exists()


def test_remove_member_drops_empty_lists_and_file(data_root, env):
    data_root.mkdir()
    spacectl.main(["create-space", "niklas"], env=env)
    spacectl.main(["add-member", "niklas", "fabian", "--write"], env=env)
    code = spacectl.main(["remove-member", "niklas", "fabian"], env=env)
    assert code == spacectl.EXIT_OK
    assert not (data_root / "niklas" / ".share.yml").exists()


def test_remove_member_on_unknown_space_aborts_instead_of_false_success(data_root, env, capsys):
    data_root.mkdir()
    code = spacectl.main(["remove-member", "nirgends", "fabian"], env=env)
    assert code == spacectl.EXIT_ERROR
    assert "existiert nicht" in capsys.readouterr().err


def test_remove_member_on_absent_share_file_is_a_noop(data_root, env, capsys):
    data_root.mkdir()
    spacectl.main(["create-space", "niklas"], env=env)
    capsys.readouterr()
    code = spacectl.main(["remove-member", "niklas", "fabian"], env=env)
    assert code == spacectl.EXIT_OK
    assert "war in keiner Liste" in capsys.readouterr().out


# -- remove-space ---------------------------------------------------------------------------


def test_remove_space_without_force_is_a_dry_run(data_root, env, capsys):
    data_root.mkdir()
    spacectl.main(["create-space", "dritter"], env=env)
    capsys.readouterr()
    code = spacectl.main(["remove-space", "dritter"], env=env)
    assert code == spacectl.EXIT_OK
    assert (data_root / "dritter").is_dir()
    assert "Trockenlauf" in capsys.readouterr().out


def test_remove_space_with_force_deletes_and_commits(data_root, env):
    data_root.mkdir()
    spacectl.main(["create-space", "dritter"], env=env)
    (data_root / "dritter" / "file.md").write_text("x", encoding="utf-8")
    code = spacectl.main(["remove-space", "dritter", "--force"], env=env)
    assert code == spacectl.EXIT_OK
    assert not (data_root / "dritter").exists()
    log = _git_log(data_root)
    assert any("remove-space dritter" in line for line in log)


def test_remove_space_warns_about_orphaning_references(data_root, env, capsys):
    data_root.mkdir()
    spacectl.main(["create-space", "niklas"], env=env)
    spacectl.main(["create-space", "dritter"], env=env)
    spacectl.main(["add-member", "niklas", "dritter", "--write"], env=env)
    capsys.readouterr()
    spacectl.main(["remove-space", "dritter"], env=env)
    err = capsys.readouterr().err
    assert "niklas" in err and "verwaisen" in err


def test_remove_space_with_force_rebuilds_the_index_so_no_stale_rows_remain(
    data_root, env, capsys,
):
    """P8-B: ohne Reindex verwaist jede `search`-/`GET /api/v1/items`-Antwort mit Zeilen aus
    dem gerade entfernten Space — derselbe Live-Incident vom 2026-08-27 nach
    `testnutzer-p7 remove-space` (`phase7_spaces_admin/CLAUDE.md`, e2c908a). Hier wird das
    Verhalten BEWIESEN, nicht nur die Warnung dokumentiert — `Store.search(space=name)` vor
    dem Lauf darf das Item noch finden, nach dem `--force`-Lauf darf sie es nicht mehr."""
    from storage.store import Store

    data_root.mkdir()
    spacectl.main(["create-space", "opfer"], env=env)
    spacectl.main(["create-space", "zeuge"], env=env)
    # Ein Item direkt ins Opfer-Verzeichnis schreiben — der schnellste Weg, einen
    # indexierten Eintrag zu erzeugen, ohne die volle `Store`-API durchzuspielen.
    (data_root / "opfer" / "itm_aaaaaaaa__demo.md").write_text(
        "---\nid: itm_aaaaaaaa\nspace: opfer\ntype: note\ntitle: Demo\nstatus: active\n"
        "version: 1\ncreated: 2026-08-31T00:00:00Z\nupdated: 2026-08-31T00:00:00Z\n"
        "tags: []\nlinks: []\n---\n\nBody.\n",
        encoding="utf-8",
    )
    # Zeuge-Space bleibt unverändert (sicherheitshalber — der Test darf nicht den falschen
    # Space treffen).
    (data_root / "zeuge" / "itm_bbbbbbbb__andere.md").write_text(
        "---\nid: itm_bbbbbbbb\nspace: zeuge\ntype: note\ntitle: Andere\nstatus: active\n"
        "version: 1\ncreated: 2026-08-31T00:00:00Z\nupdated: 2026-08-31T00:00:00Z\n"
        "tags: []\nlinks: []\n---\n\nAnderer Body.\n",
        encoding="utf-8",
    )
    pre = Store(data_root, git=False)
    pre.rebuild_index()  # die Welt in den definierten Ausgangszustand bringen
    assert any(i.id == "itm_aaaaaaaa" for i in pre.search(space="opfer").items)
    assert any(i.id == "itm_bbbbbbbb" for i in pre.search(space="zeuge").items)

    capsys.readouterr()
    code = spacectl.main(["remove-space", "opfer", "--force"], env=env)
    out = capsys.readouterr().out
    assert code == spacectl.EXIT_OK
    assert "Index neu" in out  # die neue Statuszeile, der eigentliche Mechanismus-Beweis

    post = Store(data_root, git=False)
    # Opfer-Item darf nirgends mehr auftauchen — weder im space-gefilterten noch im globalen
    # Suchlauf (Hard Rule 2: keine Karteileichen im Index, jemals).
    assert not any(i.id == "itm_aaaaaaaa" for i in post.search(space="opfer").items)
    assert not any(i.id == "itm_aaaaaaaa" for i in post.search().items)
    # Zeuge-Item bleibt sichtbar — der Reindex ist `data_root`-weit, kein Kollateralschaden.
    assert any(i.id == "itm_bbbbbbbb" for i in post.search(space="zeuge").items)


# -- check ------------------------------------------------------------------------------


def test_check_reports_no_orphans_on_a_clean_bestand(data_root, env, capsys):
    data_root.mkdir()
    spacectl.main(["create-space", "niklas"], env=env)
    spacectl.main(["create-space", "fabian"], env=env)
    spacectl.main(["add-member", "niklas", "fabian", "--write"], env=env)
    capsys.readouterr()
    assert spacectl.main(["check", "--json"], env=env) == spacectl.EXIT_OK
    out = capsys.readouterr().out
    assert '"orphan_count": 0' in out


def test_check_finds_a_share_reference_to_a_removed_space(data_root, env, capsys):
    data_root.mkdir()
    spacectl.main(["create-space", "niklas"], env=env)
    spacectl.main(["create-space", "dritter"], env=env)
    spacectl.main(["add-member", "niklas", "dritter", "--write"], env=env)
    import shutil
    shutil.rmtree(data_root / "dritter")
    capsys.readouterr()
    assert spacectl.main(["check", "--json"], env=env) == spacectl.EXIT_OK
    out = capsys.readouterr().out
    assert '"orphan_count": 1' in out
    assert '"dritter"' in out


def test_check_reports_broken_share_yaml_without_crashing(data_root, env, capsys):
    data_root.mkdir()
    spacectl.main(["create-space", "niklas"], env=env)
    (data_root / "niklas" / ".share.yml").write_text("read: [unterminated", encoding="utf-8")
    capsys.readouterr()
    assert spacectl.main(["check", "--json"], env=env) == spacectl.EXIT_OK
    out = capsys.readouterr().out
    assert '"broken_count": 1' in out


def _git_log(data_root: Path) -> list[str]:
    import subprocess
    result = subprocess.run(
        ["git", "-C", str(data_root), "log", "--oneline"],
        capture_output=True, text=True,
    )
    return result.stdout.splitlines()
