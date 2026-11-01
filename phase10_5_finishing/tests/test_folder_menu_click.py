"""P10.5 16.1 — Fund beim Filmen: der Klick auf „Umbenennen“ im Ordner-Kontextmenü darf das Menü
nicht vorher als „Klick daneben“ schließen (`js/tree.js`, seit Block 9.2).

Der Verhaltensbeleg ist die Browser-Probe `probes/p105_b16_1_ordner_menue_probe.py` (Fix 4/4
grün, Gegenlauf 3 rot). Dieser Wächter hält die Stelle im Quelltext fest, ohne Browser: der
Capture-Listener am `document` muss einen Klick **im** Menü durchlassen.
"""
from __future__ import annotations

import re
from pathlib import Path

TREE_JS = (Path(__file__).resolve().parents[2]
           / "phase5_ui" / "webui" / "static" / "js" / "tree.js")


def _capture_listener() -> str:
    text = TREE_JS.read_text(encoding="utf-8")
    m = re.search(r'document\.addEventListener\("click", function \((\w*)\) \{(.*?)\}, true\);',
                  text, re.S)
    assert m, "der Capture-Klick-Listener für das Ordner-Menü fehlt in tree.js"
    return m.group(2)


def test_click_inside_the_folder_menu_does_not_count_as_outside():
    body = _capture_listener()
    guard = body.find("folderMenuEl.contains(event.target)")
    hide = body.find("hideFolderMenu()")
    assert guard != -1, "Klick im Menü wird nicht ausgenommen — „Umbenennen“ öffnet nie den Dialog"
    assert guard < hide, "die Ausnahme muss vor dem Schließen stehen"


def test_rename_handler_still_reads_the_target_before_hiding():
    text = TREE_JS.read_text(encoding="utf-8")
    m = re.search(r'folderMenuRenameEl\.addEventListener\("click", function \(\) \{(.*?)\}\);',
                  text, re.S)
    assert m
    body = m.group(1)
    assert body.find("var target = folderMenuTarget") < body.find("hideFolderMenu()")
