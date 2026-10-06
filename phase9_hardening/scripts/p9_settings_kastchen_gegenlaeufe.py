#!/usr/bin/env python3
"""Gegenläufe G13–G18 für den Block „Kästchen enger" (Plan §12.1, Abnahme P9-116 – P9-119).

**Vier Mutationen am Stylesheet, eine am Messgerät, eine als Reproduktion des eigenen Fehlers.**
Der Aufbau ist derselbe wie bei G7–G12 (Snapshot → Mutation → Probelauf → **sofort** zurücksetzen →
am Ende byteweise prüfen), mit zwei Ergänzungen:

* **G17 mutiert die Probe, nicht das Produkt.** Die Abnahme P9-119 („Bild 07 zeigt die neu angelegte
  Zeile aufgerollt") ist eine Aussage über das **Belegwerk**, nicht über das Stylesheet — eine
  Produktmutation könnte sie nicht falsch machen. Der Gegenlauf läuft deshalb gegen eine **Kopie der
  Probe in /tmp**, in der **beide** `scrollIntoView` entfernt sind; das Arbeitsblatt (`app.css`,
  `app.html`) bleibt unberührt.
* **G18 reproduziert den eigenen Fehler dieses Blocks**: `min-width: 288px` statt `338px`, also
  die Verwechslung von **Rahmen**- und **Inhaltsbreite** (`box-sizing: border-box`).

**Und der Fehler, den dieses Skript am 2026-10-06 selbst hatte — er steht deshalb im Code.** Die
erste Fassel zählte `returncode != 0` als „die Mutation wurde bemerkt". **Ein Probelauf, der am
Login scheitert, endet mit Exit 2 und sah damit wie ein Erfolg aus** — in einem Lauf waren fünf der
sechs Mutationen so „wirksam", ohne dass eine einzige Station gelaufen war. Jetzt gilt: **eine
Mutation gilt nur als bemerkt, wenn die erwartete Station in der Probe-JSON rot steht.** Der
Exit-Code wird nur noch als Text mitgeführt, und **fehlt die JSON**, wird das stderr-Ende ausgegeben —
vorher hat das Skript die Fehlerursache weggeworfen und damit die Diagnose mit (dieselbe
Fehlerklasse wie G11: der Beleg, den man prüft, ist nicht der, den man hat).

    python phase9_hardening/scripts/p9_settings_kastchen_gegenlaeufe.py
"""
from __future__ import annotations

import filecmp
import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CSS = REPO / "phase5_ui/webui/static/app.css"
HTML = REPO / "phase5_ui/webui/static/app.html"
PROBE = REPO / "phase9_hardening/scripts/p9_settings_kastchen_probe.py"
PROBES = REPO / "phase9_hardening/probes"
SNAP = Path("/tmp/opencode/p9-kastchen-gegenlaeufe")
E2E = Path.home() / ".claude-code-tools/e2e-venv/bin/python"


def _rote_stationen(sfx: str) -> tuple[list[str], Path | None]:
    """Die roten Stationen des Laufs `sfx` — aus der **JSON**, nicht aus dem Exit-Code.

    Zwei mögliche Dateinamen, weil die Probe bei einem roten Lauf `_gegenprobe` anhängt
    (`test_committed_probe_evidence.py` verlangt genau diese Benennung). Fehlt **beide**, ist der
    Lauf gar nicht bis zu den Stationen gekommen — meist am Login, und dann ist der Exit-Code 2.
    """
    for name in (f"p9_settings_kastchen_probe_{sfx}_gegenprobe.json",
                 f"p9_settings_kastchen_probe_{sfx}.json"):
        pfad = PROBES / name
        if pfad.exists():
            bericht = json.loads(pfad.read_text(encoding="utf-8"))
            return [b["pruefung"] for b in bericht.get("befunde", []) if not b.get("ok")], pfad
    return [], None


# (Kuerzel, Datei, Beschreibung, Ersetzung-alt, Ersetzung-neu, erwartete rote Station)
MUTATIONEN = [
    ("g13", CSS, "P9-BB: das eigene vertikale Polster des Menuepunkts raus (hoehe 31,69 -> 35,69)",
     """  padding-left: var(--space);
  padding-block: calc(var(--space) * 0.5);""",
     """  padding-left: var(--space);""", "S1/P9-116"),
    ("g14", CSS, "P9-BC: die Zeilen wieder linksbuendig statt auf ihre Beschriftung",
     """  align-items: flex-start;
}
/* Und `max-width: 100%`""",
     """}
/* Und `max-width: 100%`""", "S5/P9-117"),
    ("g15", CSS, "P9-BC: `width: auto` an der Space-Zeile raus (die Sammelregel streckt wieder)",
     """.settings-space-row { width: auto; max-width: 100%; }""",
     """.settings-space-row { max-width: 100%; }""", "S5/P9-117"),
    # **G19 ist der neue Lock P9-BF als Mutation**: `padding-left` zurueck auf `0` laesst die
    # Beschriftung wieder an der linken Kastenkante kleben (innen 1 px gegen 9 px) — und **nur** das
    # Polster zu aendern reicht als Gegenprobe, weil die Kopplung an den negativen Aussenabstand
    # im Wächter (`test_the_space_rows_keep_the_standard_gap_inside_on_both_sides`) haengt: die
    # Formel `margin-left == -(padding-left)` ist beim Bauen dieser Regel entstanden und wird
    # dadurch von beiden Seiten geprueft.
    ("g19", CSS, "P9-BF: das linke Polster der Space-Zeile zurueck auf 0 (Kasten klebt wieder)",
     """  padding-left: var(--space);
  margin-left: calc(var(--space) * -1);""",
     """  padding-left: 0;
  margin-left: calc(var(--space) * -1);""", "S5/P9-120"),
    ("g16", CSS, "P9-BE: das Spaces-Fenster auf die alte Breite zurueck",
     """  min-width: 338px;
  max-width: 338px;""",
     """  min-width: 0;
  max-width: none;""", "S5/P9-118"),
    # **G18 ist der eigene Fehler dieses Blocks als Mutation.** `min-width`/`max-width` sind bei
    # `box-sizing: border-box` die Breite **des Rahmens** — 288 px im Stylesheet ergaben 288 px
    # gesamt und **240 px Inhalt** (Feld 88 px = 37 %). Die Station „schmaler als der Schatten" war
    # damit grün; erst der Feldanteil (≥ 45 %) macht den Fehler rot. Ein Gegenlauf, der den
    # **eigenen** Fehler reproduziert, ist die billigste Form von „der Wächter beißt".
    ("g18", CSS, "P9-BE: der border-box-Fehler der ersten Fassung (288 statt 338 px Rahmenbreite)",
     """  min-width: 338px;
  max-width: 338px;""",
     """  min-width: 288px;
  max-width: 288px;""", "S5/P9-118"),
]

# **G17: die Messgerät-Mutation.** Sie lebt nicht in dieser Liste, weil sie keine Datei im Arbeitsblatt
# anfasst — siehe `PROBE_MUTATION` unten.
PROBE_MUTATION = (
    "g17",
    PROBE,
    "P9-119: beide `scrollIntoView` aus der Probe entfernt — die Zeile bleibt unterhalb des "
    "Sichtbereichs",
    """                     const anlegen = document.querySelector(
                       '#settings-spaces .overlay__actions:has(#space-create-name-input)');
                     if (anlegen) anlegen.scrollIntoView({ block: 'end', inline: 'nearest' });""",
    """                     const anlegen = document.querySelector(
                       '#settings-spaces .overlay__actions:has(#space-create-name-input)');
                     /* Gegenlauf G17: kein Aufrollen, weder der Zeile noch der Anlegezeile */""",
    "S8/P9-119",
)


def main() -> int:
    SNAP.mkdir(parents=True, exist_ok=True)
    shutil.copy2(CSS, SNAP / "app.css")
    shutil.copy2(HTML, SNAP / "app.html")
    shutil.copy2(PROBE, SNAP / "p9_settings_kastchen_probe.py")
    ergebnisse: list[tuple[str, str, int, bool]] = []
    try:
        for kuerzel, datei, beschreibung, alt, neu, station in (
                MUTATIONEN + [PROBE_MUTATION]):
            quelle = SNAP / datei.name
            text = quelle.read_text(encoding="utf-8")
            assert text.count(alt) == 1, (
                f"{kuerzel}: die Stelle, die ersetzt werden sollte, kam "
                f"{text.count(alt)}x vor -- die Mutation waere stillschweigend wirkungslos"
            )
            datei.write_text(text.replace(alt, neu, 1), encoding="utf-8")
            print(f"\n=== {kuerzel}: {beschreibung} ===", file=sys.stderr, flush=True)
            # **Ausgeführt wird immer die Probe, mutiert wird `datei`.** Das steht hier, weil es
            # der vierte eigene Fehler dieses Rig war: die Fassung vom 2026-10-06 reichte
            # `str(datei)` als Skript weiter, und für die vier CSS-Mutationen startete damit
            # `python app.css` — SyntaxError, Exit 1, und der alte Zähler (`returncode != 0`)
            # meldete „Mutation bemerkt". Fünf der sechs Mutationen waren so **nie gelaufen**, und
            # zwei Wächter prüften den Lauf nicht. Die Gegenprobe dazu ist die Zeile darunter.
            assert str(datei).endswith(".py") or datei in (CSS, HTML), (
                "die mutierte Datei ist weder Skript noch CSS/HTML — die Liste unten ist falsch")
            lauf = subprocess.run(
                [str(E2E), str(PROBE), "--suffix", kuerzel],
                capture_output=True, text=True, timeout=900)
            zeilen = [ln for ln in lauf.stderr.splitlines() if ln.strip().startswith("[")]
            print("\n".join(zeilen), file=sys.stderr)
            rote, pfad = _rote_stationen(kuerzel)
            if pfad is None:
                print(f"--- {kuerzel}: **KEIN BELEG** — der Lauf kam nicht bis zu den Stationen "
                      f"(exit {lauf.returncode}). Das stderr-Ende, weil die Ursache sonst verloren "
                      f"geht:", file=sys.stderr)
                print("\n".join(lauf.stderr.splitlines()[-12:]), file=sys.stderr)
                ergebnisse.append((kuerzel, station, lauf.returncode, False))
                shutil.copy2(quelle, datei)
                continue
            # **Die Station, nicht der Exit-Code.** Der Exit-Code kann auch 1 sein, weil der Lauf
            # am Login gescheitert ist — das war der Fehler vom 2026-10-06.
            erwartet_rot = [name for name in rote if name.startswith(station)]
            bemerkt = bool(erwartet_rot)
            wort = "ROT (wie erwartet)" if bemerkt else (
                "GRUEN — die Mutation blieb unbemerkt" if rote else
                "die erwartete Station ist gruen, andere sind rot")
            print(f"--- {kuerzel}: {wort} | erwartete Station: {station} | Beleg: {pfad.name}",
                  file=sys.stderr)
            if rote:
                print(f"    rote Stationen: {rote}", file=sys.stderr)
            ergebnisse.append((kuerzel, station, lauf.returncode, bemerkt))
            # **Sofort zuruecksetzen** -- nicht am Ende. Ein Absturz mitten in der Liste darf
            # nicht mehrere Mutationen gleichzeitig im Arbeitsbaum hinterlassen.
            shutil.copy2(quelle, datei)
    finally:
        shutil.copy2(SNAP / "app.css", CSS)
        shutil.copy2(SNAP / "app.html", HTML)
        shutil.copy2(SNAP / "p9_settings_kastchen_probe.py", PROBE)
        for datei, original in ((CSS, SNAP / "app.css"), (HTML, SNAP / "app.html"),
                                (PROBE, SNAP / "p9_settings_kastchen_probe.py")):
            assert filecmp.cmp(datei, original, shallow=False), (
                f"{datei.name} ist nach den Gegenlaeufen nicht byteweise auf dem Ausgangsstand"
            )
        print("\nArbeitsbaum byteweise auf dem Ausgangsstand "
              "(app.css, app.html, p9_settings_kastchen_probe.py).", file=sys.stderr)

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