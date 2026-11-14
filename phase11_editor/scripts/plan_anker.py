#!/usr/bin/env python3
"""plan_anker.py — die Anker des P11-Plans gegen den Arbeitsbaum prüfen (Lock P11-W).

**Der String ist der Anker, die Zeilennummer die Abkürzung.** Schritte verschieben einander die
Zeilen; dieses Skript nennt für jeden Anker eines Schritts die **heutige** Zeile und meldet, wenn
ein Anker nicht **genau einmal** vorkommt (ein doppelter Anker beißt still nicht — Falle 18.2b).

Quelle: `phase11_editor/anker.json`. Je Schritt `{"status": "offen"|"erledigt", "anker": [...]}`,
je Anker `{"datei", "text", "zeile"}` — `zeile` ist die Zeile vom Tag der Planung (2026-11-13,
`main@1128fdb`) und wird nie nachgezogen; sie ist nur die Abkürzung aus dem Plan.

Aufruf:  .venv/bin/python phase11_editor/scripts/plan_anker.py [<Schritt> ...]   (ohne Argument: alle offenen)
Exit:    0 = jeder geprüfte Anker kommt genau einmal vor · 1 = mindestens einer nicht
Ausgabe: je Anker eine Zeile auf stdout (Hard Rule 7 gilt für Dienste; dies ist ein Werkzeug für Menschen und Agenten).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ANKER_DATEI = REPO_ROOT / "phase11_editor" / "anker.json"


def lade() -> dict:
    return json.loads(ANKER_DATEI.read_text(encoding="utf-8"))


def pruefe(schritt: str, eintrag: dict) -> list[dict]:
    """Je Anker: `{datei, text, zeile_plan, zeilen_heute}` — `zeilen_heute` ist die Liste aller Fundzeilen."""
    out = []
    for a in eintrag["anker"]:
        inhalt = (REPO_ROOT / a["datei"]).read_text(encoding="utf-8")
        funde, start = [], 0
        while True:
            i = inhalt.find(a["text"], start)
            if i < 0:
                break
            funde.append(inhalt.count("\n", 0, i) + 1)
            start = i + 1
        out.append({"schritt": schritt, "datei": a["datei"], "text": a["text"],
                    "zeile_plan": a["zeile"], "zeilen_heute": funde})
    return out


def main(argv: list[str]) -> int:
    daten = lade()
    schritte = argv or [s for s, e in daten.items() if e["status"] == "offen"]
    fehler = 0
    for s in schritte:
        if s not in daten:
            print(f"{s}: unbekannter Schritt (bekannt: {', '.join(daten)})")
            fehler += 1
            continue
        for r in pruefe(s, daten[s]):
            kurz = r["text"].splitlines()[0][:70]
            if len(r["zeilen_heute"]) == 1:
                print(f"{s}  {r['datei']}:{r['zeilen_heute'][0]}  (Plan: {r['zeile_plan']})  {kurz}")
            else:
                fehler += 1
                print(f"{s}  {r['datei']}  FEHLER: {len(r['zeilen_heute'])} Funde {r['zeilen_heute']}  {kurz}")
    return 1 if fehler else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
