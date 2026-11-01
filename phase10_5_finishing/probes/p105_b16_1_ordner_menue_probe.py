#!/usr/bin/env python3
"""P10.5 16.1 — Fund beim Filmen: „Umbenennen“ im Ordner-Kontextmenü öffnete nie den Dialog.

**Ursache (`js/tree.js`, seit Block 9.2 / `763e068`):** der Capture-Listener „Klick daneben
schließt das Menü“ lief **vor** dem Klick auf „Umbenennen“, leerte `folderMenuTarget`, und der
Handler brach bei `if (!target) return` ab. Das Menü ist der **einzige** UI-Weg zum Umbenennen.

**Wegwerf:** die Film-Instanz `neu` (`film/wegwerf.py`, Port 8811, tmp-`DATA_ROOT`, Stopp nur
über die PID-Datei). Die Statik wird je Anfrage aus dem Arbeitsbaum gelesen — der Gegenlauf
tauscht `tree.js` gegen `HEAD~` und fährt dieselbe Probe.

**Zellen:** `dialog_offen` (Rechtsklick → „Umbenennen“ ⇒ Dialog sichtbar) · `umbenannt` (neuer
Name in der Leiste, alter weg, Ordner auf der Platte) · `zurueck` (dasselbe rückwärts — die
Saat bleibt für den Film unverändert).

Aufruf: `~/.claude-code-tools/film-venv/bin/python p105_b16_1_ordner_menue_probe.py [--out x.json]`.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

FILM = Path(__file__).resolve().parents[1] / "film"
sys.path.insert(0, str(FILM))
import capture  # noqa: E402

DATA = Path("/tmp/opencode/sharefyx-film-neu/data/studio")


def _umbenennen(p, alt: str, neu: str) -> bool:
    p.locator("#rail-tree").get_by_text(alt, exact=True).first.click(button="right")
    p.wait_for_timeout(400)
    p.locator("#folder-context-rename").click()
    p.wait_for_timeout(600)
    if not p.locator("#rename-folder-name-input").is_visible():
        return False
    p.fill("#rename-folder-name-input", neu)
    p.locator("#rename-folder-submit").click()
    p.wait_for_timeout(2000)
    return True


def main() -> int:
    from playwright.sync_api import sync_playwright

    out = Path(sys.argv[sys.argv.index("--out") + 1]) if "--out" in sys.argv else \
        Path(__file__).with_name("p105_b16_1_ordner_menue.json")
    cells: dict[str, dict] = {}
    with sync_playwright() as pw:
        k = capture.Kamera(pw, "neu")
        k.login()
        p = k.page
        p.goto(k.base + "/ui/", wait_until="networkidle")
        p.wait_for_timeout(1000)
        offen = _umbenennen(p, "eingang", "eingang-neu")
        cells["dialog_offen"] = {"ok": offen}
        leiste = p.locator("#rail-tree").inner_text()
        cells["umbenannt"] = {"ok": offen and "eingang-neu" in leiste
                              and "\neingang\n" not in f"\n{leiste}\n"
                              and (DATA / "eingang-neu").is_dir()}
        zurueck = offen and _umbenennen(p, "eingang-neu", "eingang")
        cells["zurueck"] = {"ok": bool(zurueck) and (DATA / "eingang").is_dir()
                            and not (DATA / "eingang-neu").exists()}
        cells["seitenfehler"] = {"ok": not k.fehler, "fehler": k.fehler}
        k.close()
    result = {"cells": cells, "alle_gruen": all(c["ok"] for c in cells.values())}
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["alle_gruen"] else 1


if __name__ == "__main__":
    sys.exit(main())
