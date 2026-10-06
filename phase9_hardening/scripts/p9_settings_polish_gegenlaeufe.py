#!/usr/bin/env python3
"""Gegenläufe G7–G12 für den Block „zweite Bildsichtung" (Plan §11).

**Was das Skript tut und warum es eines ist:** sechs Mutationen am Stylesheet (bzw. eine am
Markup), jede gefolgt von einem Probelauf, dessen **Stationen rot werden müssen**. Der Aufbau
ist derselbe wie bei den Gegenläufen G1–G6 im §10-Block — der Unterschied ist der, dass hier
**sechs** Mutationen nacheinander laufen und jede ihren eigenen Beleg bekommt.

**Der Snapshot ist hier die heikelste Stelle** (ein `git checkout` auf `app.css`/`app.html` würde
den ganzen Bau verwerfen, denn beide Dateien sind unverändert eingecheckt und tragen die neuen
Regeln). Deshalb: vorher **kopieren**, nachher **zurückkopieren**, und am Ende byteweise prüfen,
dass beide Dateien wieder genau den Zustand vor dem ersten Lauf haben.

    python phase9_hardening/scripts/p9_settings_polish_gegenlaeufe.py
"""
from __future__ import annotations

import filecmp
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CSS = REPO / "phase5_ui/webui/static/app.css"
HTML = REPO / "phase5_ui/webui/static/app.html"
SNAP = Path("/tmp/opencode/p9-polish-gegenlaeufe")
PROBE = REPO / "phase9_hardening/scripts/p9_settings_polish_probe.py"
E2E = Path.home() / ".claude-code-tools/e2e-venv/bin/python"

# (Kuerzel, Datei, Beschreibung, Ersetzung-alt, Ersetzung-neu, erwartete rote Station)
# **Nur G11 wird wiederholt** (2026-10-06): die Mutation blieb beim ersten Durchlauf unbemerkt,
# weil die Station nur die **Kanten** der Anlegezeile prüfte — ein geschrumpfter Knopf hält
# dieselben Kanten. Die Station misst jetzt zusätzlich die Eigenbreite des Knopfes, und genau
# **diese** eine Mutation muss jetzt rot werden. Die übrigen fünf sind bereits als wirksam
# belegt (`*_gegenprobe.json` im Repo).
MUTATIONEN = [
    ("g11", CSS, "P9-AZ: flex: 1 auf dem Anlege-Feld raus",
     """#space-create-name-input { flex: 1; min-width: 0; }""",
     """#space-create-name-input { min-width: 0; }""", "S5/P9-109"),
    ("g12", CSS, "P9-AX: die Buendigkeit der Space-Zeilen raus",
     """.settings-panel .settings-space-row { padding-left: 0; }""",
     """.settings-panel .settings-space-row { padding-left: var(--space); }""", "S5/P9-107"),
]


def main() -> int:
    SNAP.mkdir(parents=True, exist_ok=True)
    shutil.copy2(CSS, SNAP / "app.css")
    shutil.copy2(HTML, SNAP / "app.html")
    ergebnisse: list[tuple[str, str, int, bool]] = []
    try:
        for kuerzel, datei, beschreibung, alt, neu, station in MUTATIONEN:
            quelle = SNAP / datei.name
            text = quelle.read_text(encoding="utf-8")
            assert text.count(alt) == 1, (
                f"{kuerzel}: die Stelle, die ersetzt werden sollte, kam "
                f"{text.count(alt)}x vor -- die Mutation waere stillschweigend wirkungslos"
            )
            datei.write_text(text.replace(alt, neu, 1), encoding="utf-8")
            print(f"\n=== {kuerzel}: {beschreibung} ===", file=sys.stderr, flush=True)
            lauf = subprocess.run(
                [str(E2E), str(PROBE), "--suffix", kuerzel],
                capture_output=True, text=True, timeout=900)
            rot = lauf.returncode != 0
            zeilen = [ln for ln in lauf.stderr.splitlines() if ln.strip().startswith("[")]
            print("\n".join(zeilen), file=sys.stderr)
            ergebnis_wort = "ROT (wie erwartet)" if rot else "GRUEN — die Mutation blieb unbemerkt"
            print(f"--- {kuerzel}: {ergebnis_wort} | erwartete Station: {station}",
                  file=sys.stderr, flush=True)
            ergebnisse.append((kuerzel, station, lauf.returncode, rot))
            # **Sofort zuruecksetzen** -- nicht am Ende. Ein Absturz mitten in der Liste darf
            # nicht sechs Mutationen gleichzeitig im Arbeitsbaum hinterlassen.
            shutil.copy2(quelle, datei)
    finally:
        shutil.copy2(SNAP / "app.css", CSS)
        shutil.copy2(SNAP / "app.html", HTML)
        for datei, original in ((CSS, SNAP / "app.css"), (HTML, SNAP / "app.html")):
            assert filecmp.cmp(datei, original, shallow=False), (
                f"{datei.name} ist nach den Gegenlaeufen nicht byteweise auf dem Ausgangsstand"
            )
        print("\nArbeitsbaum byteweise auf dem Ausgangsstand (app.css, app.html).",
              file=sys.stderr)

    print("\n===== BILANZ =====", file=sys.stderr)
    alle_erkannt = True
    for kuerzel, station, code, rot in ergebnisse:
        print(f"  {kuerzel}: {'rot' if rot else 'GRUEN'} (exit {code}), erwartet rot bei {station}",
              file=sys.stderr)
        alle_erkannt &= rot
    print(f"\n{sum(1 for *_, rot in ergebnisse if rot)}/{len(ergebnisse)} Mutationen wurden bemerkt",
          file=sys.stderr)
    return 0 if alle_erkannt else 1


if __name__ == "__main__":
    raise SystemExit(main())