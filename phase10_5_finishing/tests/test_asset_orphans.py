"""Tests für `phase10_5_finishing/scripts/asset_orphans.py` (LG-7, P10.5 Block 3, Schritt 3.4).

**Was hier geprüft wird.** `Store.trash()` verschiebt ein Item nach `DATA_ROOT/._trash/<space>/`,
aber die **Bilddateien bleiben liegen** — bewusst (`store.py`, Docstring von `trash()`: ein
zweiter Move würde aus einer atomaren Operation zwei halbe machen). Übrig bleibt ein Ordner
`<space>/_assets/<item_id>/`, zu dem es kein Item mehr gibt. Dieses Skript findet ihn und
verschiebt ihn **nur auf Wunsch** in den Papierkorb.

**Der Plan sagt „im Index", der Code prüft gegen die Dateien** (Hard Rule 2: Dateien sind die
Wahrheit, der Index ist Ableitung). Der Unterschied ist nicht kosmetisch: ein veralteter
Index würde die Assets **lebender** Items als verwaist melden — und `--move` würde sie in den
Papierkorb schieben. Der Test `test_a_live_item_is_never_reported` sichert genau das ab.

**Kein echter DATA_ROOT:** jeder Test baut sein eigenes Wurzelverzeichnis (`tmp_path`).
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

from sharefyx_image_bytes import png_bytes
from storage.store import Store

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "phase10_5_finishing" / "scripts" / "asset_orphans.py"


def _load_script():
    """Lädt das Skript per Pfad — es liegt in keinem Python-Paket (dasselbe Muster wie
    `phase4_auth/tests/test_users.py :: _load_script`)."""
    spec = importlib.util.spec_from_file_location("asset_orphans", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    # Das Modul muss in `sys.modules` stehen, bevor es ausgeführt wird: das Skript benutzt
    # `@dataclass`, und `dataclasses` holt sich die Annotationen über
    # `sys.modules[cls.__module__]` — ohne Eintrag ist das `None` (Fund beim ersten Lauf).
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def asset_orphans():
    return _load_script()


@pytest.fixture
def data_root(tmp_path) -> Path:
    """Ein Datenverzeichnis mit Git-Repo, einem Item mit Bild und einem gepaperten Item."""
    root = tmp_path / "data"
    root.mkdir()
    store = Store(root, git=True)
    lebendig = store.create("alpha", type="note", title="Lebendig")
    store.put_asset(lebendig.id, data=png_bytes())
    tot = store.create("alpha", type="note", title="Papierkorb")
    store.put_asset(tot.id, data=png_bytes())
    store.trash(tot.id, version=tot.version)
    return root


def _git_log_count(root: Path) -> int:
    result = subprocess.run(
        ["git", "-C", str(root), "rev-list", "--count", "HEAD"],
        capture_output=True, text=True, check=True,
    )
    return int(result.stdout.strip())


def test_report_finds_the_orphaned_asset_folder(asset_orphans, data_root, capsys):
    """Der Papierkorb-Fall: das Item ist weg, sein Bild-Ordner liegt noch."""
    orphans = asset_orphans.find_orphans(data_root)

    assert len(orphans) == 1
    orphan = orphans[0]
    assert orphan.space == "alpha"
    assert orphan.files == 1
    assert orphan.bytes > 0

    code = asset_orphans.main(["--data-root", str(data_root), "--report"])
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert len(payload["orphans"]) == 1
    assert payload["total_bytes"] == orphan.bytes


def test_a_live_item_is_never_reported(asset_orphans, data_root):
    """**Gegenlauf:** die Assets eines lebenden Items stehen nicht im Bericht — sie sind keine
    Waisen. (Genau hier wäre ein veralteter Index gefährlich: er würde sie melden.)"""
    lebendig_id = next(
        path.name.split("__", 1)[0]
        for path in (data_root / "alpha").rglob("*.md")
        if "._trash" not in path.parts
    )

    orphans = asset_orphans.find_orphans(data_root)

    assert len(orphans) == 1
    assert lebendig_id not in {o.item_id for o in orphans}


def test_move_moves_the_folder_and_commits_exactly_once(asset_orphans, data_root, capsys):
    """`--move` verschiebt in den Papierkorb (nicht ins Nirgendwo) und macht **einen**
    Commit — nicht einen je Ordner."""
    before = _git_log_count(data_root)

    code = asset_orphans.main(["--data-root", str(data_root), "--move"])

    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert len(payload["moved"]) == 1
    moved = payload["moved"][0]

    quelle = data_root / moved["space"] / "_assets" / moved["item_id"]
    ziel = data_root / "._trash" / moved["space"] / "_assets" / moved["item_id"]
    assert not quelle.exists()
    assert ziel.is_dir()
    assert len(list(ziel.iterdir())) == 1
    assert _git_log_count(data_root) == before + 1


def test_move_leaves_the_assets_of_live_items_untouched(asset_orphans, data_root):
    """**Gegenlauf** zu `test_move_moves_the_folder_and_commits_exactly_once`: die Assets des
    **lebenden** Items stehen danach noch genau dort, wo sie waren — verschoben wird nur,
    was wirklich verwaist ist."""
    # Das lebende Item ist das einzige, dessen Datei **nicht** im Papierkorb liegt.
    lebendig_id = next(
        path.name.split("__", 1)[0]
        for path in (data_root / "alpha").rglob("*.md")
        if "._trash" not in path.parts
    )
    live_dir = data_root / "alpha" / "_assets" / lebendig_id
    assert live_dir.is_dir()

    asset_orphans.main(["--data-root", str(data_root), "--move"])

    assert live_dir.is_dir()
    assert len(list(live_dir.iterdir())) == 1
    assert len(list((data_root / "alpha" / "_assets").iterdir())) == 1


def test_move_without_a_git_repository_moves_nothing(asset_orphans, tmp_path):
    """Ohne Git-Repo gäbe es keinen Commit — die Ordner wären trotzdem verschoben, der
    Zustand also halb. Lieber gar nichts."""
    root = tmp_path / "ohne-git"
    (root / "alpha" / "_assets" / "itm_00000000").mkdir(parents=True)
    (root / "alpha" / "_assets" / "itm_00000000" / "ast_00000000.png").write_bytes(b"x")

    assert asset_orphans.main(["--data-root", str(root), "--move"]) != 0
    assert (root / "alpha" / "_assets" / "itm_00000000").is_dir()


def test_a_missing_data_root_argument_is_an_error(asset_orphans):
    """`--data-root` ist **Pflicht** (kein Default, kein stiller Fallback ins
    Arbeitsverzeichnis) — ohne die Angabe bricht das Skript ab."""
    with pytest.raises(SystemExit) as exc:
        asset_orphans.main(["--report"])
    assert exc.value.code != 0


def test_a_missing_data_root_directory_is_an_error(asset_orphans, tmp_path, capsys):
    assert asset_orphans.main(["--data-root", str(tmp_path / "gibtsnicht")]) != 0
