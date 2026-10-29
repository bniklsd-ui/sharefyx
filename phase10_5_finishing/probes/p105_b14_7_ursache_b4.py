#!/usr/bin/env python3
"""P10.5 Block 14.7, Schritt 14.7.0 (b) — die **Ursache von B4**: warum reisst jeder
Verteilungs-Hebel die Stabilitaet (P10.5-68)?

Plan `docs/concepts/phase10_5_block14_7_plan.md` §0 nennt zwei Kandidaten:
(i) **Ueberlauf** — die Knoten ragen nach der Entspannung ueber ihre Region und koppeln an den
Nachbar-Space; (ii) **Chaos** — die Entspannung sortiert einen Lappen **innen** um, ohne dass
Spaces einander beruehren.

**Wie gemessen wird.** Die Layout-Probe (`p105_b14_layout_probe.py`) legt bei jeder Stabilitaets-
messung die Positionen **beider** Laeufe ab (`/tmp/opencode/p105_b14_stab_<pid>.json`: `vorher`
= Abnahme-Seed, `nachher` = frischer Lauf nach +1 Item in `epsilon`). Dieses Skript liest drei
solche Ablagen — Basislinie, `ITEM_STEP=20`, `ISLAND_FACTOR=0.75` (die beiden staerksten Brueche
aus 14.4) — und zerlegt die Bewegung je Space in **Verschiebung des Schwerpunkts** (der Lappen
wandert — Kandidat i) und **Rest** (der Lappen sortiert sich innen um — Kandidat ii).

**Die Zuordnung Knoten → Space** folgt den Saat-IDs: die Saat legt die Spaces nacheinander an
(alpha 30, beta 32, gamma 30, delta 30, epsilon 30) mit fortlaufenden IDs. Gegengeprueft: die
daraus gerechneten Schwerpunkte sind **identisch** mit `messungen.regionen.schwerpunkte` der Probe.

Aufruf:  `python3 p105_b14_7_ursache_b4.py <basis.json> <step20.json> <insel075.json>`
Ergebnis: `p105_b14_7_ursache_b4.json` (der Beleg; die Ablagen selbst sind Arbeitsmittel).
"""
from __future__ import annotations

import json
import math
import statistics as st
import sys
from pathlib import Path

ERGEBNIS = Path(__file__).resolve().with_name("p105_b14_7_ursache_b4.json")
SAAT = [("alpha", 30), ("beta", 32), ("gamma", 30), ("delta", 30), ("epsilon", 30)]
WACHSER = "epsilon"
LABELS = ["basis", "ITEM_STEP=20", "ISLAND_FACTOR=0.75"]


def _spaces(vorher: dict) -> dict:
    ids = sorted(vorher)
    out, k = {}, 0
    for name, n in SAAT:
        for i in ids[k:k + n]:
            out[i] = name
        k += n
    return out


def _mitte(pos: dict, ids: list) -> tuple:
    return (st.mean(pos[i][0] for i in ids), st.mean(pos[i][1] for i in ids))


def analyse(ablage: dict) -> dict:
    v, n = ablage["vorher"], ablage["nachher"]
    sp = _spaces(v)
    je_space = {}
    for name, _ in SAAT:
        ids = [i for i in v if sp.get(i) == name and i in n]
        cv, cn = _mitte(v, ids), _mitte(n, ids)
        rest = [math.dist((v[i][0] - cv[0], v[i][1] - cv[1]), (n[i][0] - cn[0], n[i][1] - cn[1]))
                for i in ids]
        je_space[name] = {
            "schwerpunkt_verschiebung_px": round(math.dist(cv, cn), 1),
            "rest_median_px": round(st.median(rest), 1),
            "radius_px": round(max(math.dist(v[i], cv) for i in ids), 1),
        }
    # die groessten Springer der **anderen** Spaces: wo sitzen sie?
    mitten = {name: _mitte(v, [i for i in v if sp.get(i) == name]) for name, _ in SAAT}
    springer = []
    for i in v:
        if sp.get(i) in (None, WACHSER) or i not in n:
            continue
        fremd = min(math.dist(v[i], v[j]) for j in v if sp.get(j) != sp[i])
        springer.append({"verschiebung_px": round(math.dist(v[i], n[i]), 1), "space": sp[i],
                         "abstand_eigener_schwerpunkt_px": round(math.dist(v[i], mitten[sp[i]]), 1),
                         "abstand_naechster_fremder_px": round(fremd, 1)})
    springer.sort(key=lambda s: -s["verschiebung_px"])
    schritte = sorted(s["verschiebung_px"] for s in springer)
    return {
        "median_verschiebung_px": schritte[len(schritte) // 2],
        "max_verschiebung_px": schritte[-1],
        "knoten_ueber_3px": sum(1 for s in schritte if s > 3),
        "knoten_andere_spaces": len(schritte),
        "je_space": je_space,
        "groesste_springer": springer[:5],
    }


def main(pfade: list) -> int:
    ergebnis = {"probe": "p105_b14_7_ursache_b4", "schritt": "14.7.0 (b)", "laeufe": {}}
    for label, pfad in zip(LABELS, pfade):
        ergebnis["laeufe"][label] = analyse(json.loads(Path(pfad).read_text(encoding="utf-8")))
    ERGEBNIS.write_text(json.dumps(ergebnis, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(ergebnis, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:4]))
