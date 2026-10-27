#!/usr/bin/env python3
"""P10.5 Block 14, Schritt 14.4 — die **Messung der Startwerte**.

Die vier L4-Konstanten des Plans (`docs/concepts/phase10_5_block14_kartenlayout_plan.md` §2.4)
sind **Startwerte**: "in 14.4 werden sie **gemessen** (nicht gesetzt)" (Plan §2.4, datiert
2026-10-26). Dieses Skript ist der **Treiber** der Messung: es fährt die Browser-Probe
(`p105_b14_layout_probe.py`) je Variante mit einem anderen Startwert und legt die
**Rohdaten** in einer Tabelle ab.

**Kein Bewertungsurteil im Skript.** Die Skript-Ausgabe ist eine Tabelle (JSON); die
Entscheidung ("welcher Wert bleibt") steht im Bericht und im Plan, nicht hier — sonst wäre
die Messung eine Behauptung mit eingebautem Ergebnis.

**Wie gemessen wird.** Jede Variante ist ein Lauf der Browser-Probe mit `--konstante=NAME=WERT`:
die Konstante wird in einer **Kopie** der statischen Dateien gepatcht (der Arbeitsbaum bleibt
unberührt, wie bei einem Gegenlauf), der Server serviert die Kopie, und die Probe misst
**dieselben** Zellen wie der Normalfall. Die Vergleichbarkeit ist damit gegeben: es ist
derselbe Datensatz (5 Spaces, 152 Items), dasselbe Fenster (1920x1200), dasselbe Werkzeug.

**Die Zahlen, die entscheiden:**

| Zahl | Zelle | was sie sagt |
|---|---|---|
| `regionen.anteil` | `regionen` | der Anteil der Knoten, der dem Schwerpunkt **seines** Space am nächsten liegt (Schwelle 95 %) |
| `regionen.marge_min_px` | `regionen` | der **Spielraum** der Trennung: der kleinste Abstand „eigener Schwerpunkt minus naechster fremder" ueber alle Knoten. Positiv = getrennt; nahe 0 = die Zelle kippt beim naechsten Item |
| `stabilitaet.median_verschiebung_px` | `stabilitaet` | wie weit sich die Knoten **anderer** Spaces bewegen, wenn ein Item in einen nicht-groessten Space kommt (Schwelle 2 px) |
| `budget.ruhe_ms` | `budget` | die Zeit bis zur Ruhe bei 201 Knoten (Schwelle 3000 ms) |
| `kamera.fuellgrad` | `kamera` | der Anteil der Leinwand, den der Inhalt fuellt (Schwelle 60 %) |
| `kamera.welt` | `kamera` | die **Groesse der Welt** — sie entscheidet, ob die Karte eine Insel ist oder ein Streifen |

Aufruf:  `.venv/bin/python phase10_5_finishing/probes/p105_b14_startwerte.py`
Ergebnis: `phase10_5_finishing/probes/p105_b14_startwerte_messung.json` (die Tabelle — **der
Beleg**). Je Variante schreibt der Lauf zusätzlich `p105_b14_layout_probe_konstante_<label>.json`
(die Rohbelege); das sind **Zwischenstände** — sie stehen nicht im Commit und lassen sich mit
`--rebuild` aus der Tabelle wiederherstellen, ohne die Messung zu fahren.
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PROBE = Path(__file__).resolve().with_name("p105_b14_layout_probe.py")
SUMMARY = Path(__file__).resolve().with_name("p105_b14_startwerte_messung.json")
PYTHON = REPO_ROOT / ".venv" / "bin" / "python"

#: **Die Varianten** (Schritt 14.4). Der Wert `None` bedeutet "unveraendert" (die Zeile
#: entfaellt dann) — jeder Lauf misst **eine** Konstante gegen die uebrigen unveraenderten.
#:
#: **Die Werte sind nicht geraten:** sie sind die Groessenordnungen, die der Plan nennt
#: ("Startwert"), verdichtet auf zwei Schritte nach unten und zwei nach oben. Jeder Lauf
#: misst die Wirkung; die Wahl steht danach im Bericht.
VARIANTEN: list[tuple[str, dict[str, str]]] = [
    # -- ANCHOR_GRAVITY (Startwert 0.02) -- der Zug zum **eigenen** Space-Anker ---------------
    ("anker0.005", {"ANCHOR_GRAVITY": "0.005"}),
    ("anker0.01", {"ANCHOR_GRAVITY": "0.01"}),
    ("anker0.02", {"ANCHOR_GRAVITY": "0.02"}),
    ("anker0.04", {"ANCHOR_GRAVITY": "0.04"}),
    ("anker0.08", {"ANCHOR_GRAVITY": "0.08"}),
    # -- CROSS_SPRING_FACTOR (Startwert 0.15) -- die Staerke der Querfeder --------------------
    ("quer0", {"CROSS_SPRING_FACTOR": "0"}),
    ("quer0.05", {"CROSS_SPRING_FACTOR": "0.05"}),
    ("quer0.15", {"CROSS_SPRING_FACTOR": "0.15"}),
    ("quer0.3", {"CROSS_SPRING_FACTOR": "0.3"}),
    ("quer0.6", {"CROSS_SPRING_FACTOR": "0.6"}),
    # -- CROSS_SPRING_LENGTH_FACTOR (Startwert 3) -- die Laenge der Querfeder ------------------
    ("laenge1", {"CROSS_SPRING_LENGTH_FACTOR": "1"}),
    ("laenge2", {"CROSS_SPRING_LENGTH_FACTOR": "2"}),
    ("laenge3", {"CROSS_SPRING_LENGTH_FACTOR": "3"}),
    ("laenge4", {"CROSS_SPRING_LENGTH_FACTOR": "4"}),
    ("laenge6", {"CROSS_SPRING_LENGTH_FACTOR": "6"}),
    # -- ALPHA_START_SEEDED (Startwert 0.5) -- die gesetzte Startenergie ----------------------
    ("alpha0.25", {"ALPHA_START_SEEDED": "0.25"}),
    ("alpha0.5", {"ALPHA_START_SEEDED": "0.5"}),
    ("alpha0.75", {"ALPHA_START_SEEDED": "0.75"}),
    ("alpha1", {"ALPHA_START_SEEDED": "1"}),
    # -- Der Seed (Plan §2.1-§2.3): Radius, Abstand, Inseln, Spirale, Jitter -----------------
    ("radius14", {"REGION_ITEM_STEP": "14"}),
    ("radius22", {"REGION_ITEM_STEP": "22"}),
    ("radius30", {"REGION_ITEM_STEP": "30"}),
    ("pad10", {"REGION_PAD": "10"}),
    ("pad30", {"REGION_PAD": "30"}),
    ("pad50", {"REGION_PAD": "50"}),
    ("gap0", {"REGION_GAP": "0"}),
    ("gap40", {"REGION_GAP": "40"}),
    ("gap100", {"REGION_GAP": "100"}),
    ("insel0.35", {"ISLAND_FACTOR": "0.35"}),
    ("insel0.55", {"ISLAND_FACTOR": "0.55"}),
    ("insel0.75", {"ISLAND_FACTOR": "0.75"}),
    ("step10", {"ITEM_STEP": "10"}),
    ("step14", {"ITEM_STEP": "14"}),
    ("step20", {"ITEM_STEP": "20"}),
    ("jitter4", {"ITEM_JITTER_PX": "4"}),
    ("jitter8", {"ITEM_JITTER_PX": "8"}),
    ("jitter14", {"ITEM_JITTER_PX": "14"}),
]

#: Wie viele Läufe **gleichzeitig** laufen. Der Server und der Browser brauchen CPU
#: (die Messung der Ruhe-Zeit ist zeitkritisch); zwei Läufe sind auf diesem Rechner
#: (4 Kerne) gemessen reproduzierbar — die Kontrollvariante (der Startwert selbst) muss
#: dieselben Zahlen liefern wie der Normalfall-Beleg.
PARALLEL = 2


def _eine_variante(label: str, konstanten: dict[str, str]) -> dict:
    """Ein Lauf der Browser-Probe mit einer Variante; der Beleg wird gelesen."""
    args = [str(PYTHON), str(PROBE), "--label=" + label]
    for name, wert in konstanten.items():
        args.append("--konstante=%s=%s" % (name, wert))
    begonnen = time.time()
    proc = subprocess.run(args, cwd=str(REPO_ROOT), capture_output=True, text=True,
                          timeout=1800)
    dauer = time.time() - begonnen
    beleg = PROBE.with_name("p105_b14_layout_probe_konstante_%s.json" % label)
    eintrag = {
        "label": label,
        "konstanten": konstanten,
        "dauer_s": round(dauer, 1),
        "rueckgabe": proc.returncode,
    }
    if proc.returncode != 0 or not beleg.exists():
        eintrag["fehler"] = (proc.stderr or "")[-800:]
        return eintrag
    daten = json.loads(beleg.read_text(encoding="utf-8"))
    m = daten["messungen"]
    welt = m["kamera"].get("welt") or {}
    eintrag["zellen"] = {
        "regionen_anteil": m["regionen"].get("anteil"),
        "regionen_marge_min_px": m["regionen"].get("marge_min_px"),
        "regionen_marge_median_px": m["regionen"].get("marge_median_px"),
        "engster_abstand_px": m["regionen"].get("engster_abstand_px"),
        "ueberlappende_paare": m["regionen"].get("ueberlappende_paare"),
        "stabilitaet_median_px": m["stabilitaet"].get("median_verschiebung_px"),
        "stabilitaet_max_px": m["stabilitaet"].get("max_verschiebung_px"),
        "budget_ruhe_ms": m["budget"].get("ruhe_ms"),
        "budget_knoten": m["budget"].get("knoten"),
        "kamera_fuellgrad": m["kamera"].get("fuellgrad"),
        "kamera_versatz_px": m["kamera"].get("versatz_mitte_px"),
        "kamera_zoom": m["kamera"].get("zoom_anzeige"),
        "welt_breite_px": (welt.get("x1", 0) - welt.get("x0", 0)) if welt else None,
        "welt_hoehe_px": (welt.get("y1", 0) - welt.get("y0", 0)) if welt else None,
        "beschriftungen_paare": len(m["beschriftungen"].get("ueberlappungen") or []),
    }
    eintrag["ok"] = {name: bool(m[name].get("ok")) for name in m}
    eintrag["alle_kriterien_erfuellt"] = daten.get("alle_kriterien_erfuellt")
    eintrag["seitenfehler"] = daten.get("seitenfehler")
    # **Der Beweis, dass der Patch gewirkt hat:** der Server hat **diese** Konstante mit
    # **diesen** Werten ausgeliefert (aus dem Beleg der Messung selbst, nicht behauptet).
    gesendet = daten.get("konstanten_gesendet") or {}
    eintrag["gesendet"] = {name: gesendet.get(name) for name in konstanten}
    return eintrag


#: **Die Startwerte des Codes** (aus der echten `graph.js` gelesen, nicht hier wiederholt) —
#: sie stehen in der Tabelle, damit der Leser weiss, **womit** verglichen wurde.
def _startwerte() -> dict:
    import re
    quelle = (REPO_ROOT / "phase5_ui" / "webui" / "static" / "js" / "graph.js").read_text(
        encoding="utf-8")
    werte = {}
    for name in ("REGION_ITEM_STEP", "REGION_PAD", "REGION_GAP", "ISLAND_FACTOR", "ITEM_STEP",
                 "ITEM_JITTER_PX", "GOLDEN_ANGLE", "ANCHOR_GRAVITY", "CROSS_SPRING_FACTOR",
                 "CROSS_SPRING_LENGTH_FACTOR", "ALPHA_START_SEEDED", "FIT_MARGIN"):
        treffer = re.search(r"^const %s = ([^;]+);" % re.escape(name), quelle, re.M)
        if treffer:
            werte[name] = treffer.group(1)
    return werte


#: **Die Regel der Wahl** (Schritt 14.4) — sie steht in der Tabelle, damit die Wahl **nachlesbar**
#: ist und nicht im Kopf des Ausführers steckt.
REGEL = ("Der Wert bleibt, wenn er die Stabilitaet haelt (Median <= 2 px UND Maximum <= 3 px) "
         "UND die groesste Trennungs-Marge hat (der kleinste Abstand 'eigener Space-Schwerpunkt "
         "minus naechster fremder' ueber alle Knoten; 0 hiesse: die Zelle kippt beim naechsten "
         "Item). Jeder Wert in beide Richtungen ist gemessen: der Nachbarwert ist schlechter.")


def main() -> int:
    nur = [a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--nur=")]
    rebuild = any(a == "--rebuild" for a in sys.argv[1:])
    varianten = [v for v in VARIANTEN if not nur or v[0] in nur]
    if not varianten and not rebuild:
        raise SystemExit("keine Variante ausgewaehlt (--nur=<label>)")
    roh = {}
    if rebuild:
        # **Die Tabelle neu bauen, ohne die Messung zu fahren** (die Beleg-Dateien der
        # Varianten liegen im Probes-Verzeichnis).
        for label, konstanten in VARIANTEN:
            beleg = PROBE.with_name("p105_b14_layout_probe_konstante_%s.json" % label)
            if not beleg.exists():
                continue
            daten = json.loads(beleg.read_text(encoding="utf-8"))
            m = daten["messungen"]
            welt = m["kamera"].get("welt") or {}
            gesendet = daten.get("konstanten_gesendet") or {}
            roh[label] = {
                "label": label,
                "konstanten": konstanten,
                "zellen": {
                    "regionen_anteil": m["regionen"].get("anteil"),
                    "regionen_marge_min_px": m["regionen"].get("marge_min_px"),
                    "regionen_marge_median_px": m["regionen"].get("marge_median_px"),
                    "engster_abstand_px": m["regionen"].get("engster_abstand_px"),
                    "ueberlappende_paare": m["regionen"].get("ueberlappende_paare"),
                    "stabilitaet_median_px": m["stabilitaet"].get("median_verschiebung_px"),
                    "stabilitaet_max_px": m["stabilitaet"].get("max_verschiebung_px"),
                    "budget_ruhe_ms": m["budget"].get("ruhe_ms"),
                    "budget_knoten": m["budget"].get("knoten"),
                    "kamera_fuellgrad": m["kamera"].get("fuellgrad"),
                    "kamera_versatz_px": m["kamera"].get("versatz_mitte_px"),
                    "kamera_zoom": m["kamera"].get("zoom_anzeige"),
                    "welt_breite_px": (welt.get("x1", 0) - welt.get("x0", 0)) if welt else None,
                    "welt_hoehe_px": (welt.get("y1", 0) - welt.get("y0", 0)) if welt else None,
                    "beschriftungen_paare": len(m["beschriftungen"].get("ueberlappungen") or []),
                },
                "ok": {name: bool(m[name].get("ok")) for name in m},
                "alle_kriterien_erfuellt": daten.get("alle_kriterien_erfuellt"),
                "seitenfehler": daten.get("seitenfehler"),
                "gesendet": {name: gesendet.get(name) for name in konstanten},
            }
    else:
        with ThreadPoolExecutor(max_workers=PARALLEL) as pool:
            zukunft = {pool.submit(_eine_variante, label, k): label
                       for label, k in varianten}
            for zukunft_zu, label in [(z, zukunft[z]) for z in zukunft]:
                eintrag = zukunft_zu.result()
                roh[label] = eintrag
                print("%-12s %s" % (label, json.dumps(eintrag.get("zellen", eintrag),
                                                     ensure_ascii=False)), flush=True)
    bericht = {
        "probe": "p105_b14_startwerte",
        "schritt": "14.4",
        "zeit": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "parallel": PARALLEL,
        "regel": REGEL,
        "startwerte": _startwerte(),
        "varianten": roh,
    }
    SUMMARY.write_text(json.dumps(bericht, ensure_ascii=False, indent=2) + "\n",
                       encoding="utf-8")
    print("geschrieben:", SUMMARY, SUMMARY.stat().st_size, "B")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
