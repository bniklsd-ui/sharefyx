#!/usr/bin/env python3
"""P10.5 Block 14.7, Schritt 14.7.2 — **das Raster** (Plan
`docs/concepts/phase10_5_block14_7_plan.md` §4): Anordnung der Anker × `LOBE_SCALE`, je Variante
die Layout-Probe (alle Abnahmezellen 65–69, 71) **und** die Bilder-Probe (`koerper`, Rand, Form,
Bilder). Treiber nach dem Muster `p105_b14_startwerte.py`.

**Kein Bewertungsurteil im Skript** — die Tabelle sind Rohdaten; die Wahl (E1) trifft der Nikinger.
Einzige Vorsortierung, vom Plan verlangt (§3): `stabil` = Median ≤ 2 px **und** Maximum ≤ 3 px
(die Regel aus 14.4) — eine Variante ohne `stabil` wird nicht zur Wahl gestellt.

**Nacheinander, nicht parallel:** parallele Läufe der Layout-Probe teilen den Wegwerf-Ordner und
scheitern (Fund 14.7.0 (b)). Bilder je Variante unter `~/p105_b14_7_varianten/<label>/`
(**außerhalb** des Repos); die Rohbelege je Variante werden nach dem Lesen gelöscht.

Aufruf:  `.venv/bin/python phase10_5_finishing/probes/p105_b14_7_raster.py [--nur=label,label]`
Ergebnis: `phase10_5_finishing/probes/p105_b14_7_raster.json`
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PROBES = Path(__file__).resolve().parent
PYTHON = REPO_ROOT / ".venv" / "bin" / "python"
ERGEBNIS = PROBES / "p105_b14_7_raster.json"
BILDER_WURZEL = Path.home() / "p105_b14_7_varianten"

ANORDNUNGEN = [
    ("spirale", {"ANCHOR_LAYOUT": '"spirale"'}),
    ("hexf", {"ANCHOR_LAYOUT": '"hex"', "ANCHOR_HEX_ORDER": '"fortlaufend"'}),
    ("hexg", {"ANCHOR_LAYOUT": '"hex"', "ANCHOR_HEX_ORDER": '"gegenueber"'}),
]
SKALEN = ["1", "1.25", "1.5"]
VARIANTEN = [("%s_s%s" % (a, sk), dict(k, LOBE_SCALE=sk)) for a, k in ANORDNUNGEN for sk in SKALEN]
#: **Die Glaettung** (Plan §3 E2, am selben STOPP wie E1): nur die Bilder-Probe — die
#: Knotenpositionen haengen nicht an der Glaettung (sie wirkt nur in `chainEdges()`). Gemessen an
#: jeder Anordnung bei `LOBE_SCALE` 1,5 und an der Basislinie.
GLAETTUNG = [("%s_s1.5_glatt%d" % (a, p), dict(k, LOBE_SCALE="1.5", LOBE_SMOOTH_PASSES=str(p)))
             for a, k in ANORDNUNGEN for p in (2, 4, 6)] + [
            ("spirale_s1_glatt%d" % p, {"LOBE_SMOOTH_PASSES": str(p)}) for p in (2, 4, 6)]


def _lauf(skript: str, label: str, konstanten: dict, extra: list) -> dict:
    args = [str(PYTHON), str(PROBES / skript), "--label=" + label] + [
        "--konstante=%s=%s" % (n, w) for n, w in konstanten.items()] + extra
    t0 = time.time()
    proc = subprocess.run(args, cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=1500)
    if proc.returncode != 0:
        return {"fehler": proc.stderr.strip()[-1500:], "sekunden": round(time.time() - t0)}
    return {"sekunden": round(time.time() - t0)}


def _layout(label: str) -> dict:
    datei = PROBES / ("p105_b14_layout_probe_konstante_%s.json" % label)
    d = json.loads(datei.read_text(encoding="utf-8"))
    datei.unlink()
    m = d["messungen"]
    st = m["stabilitaet"]
    return {
        "zellen": {k: v.get("ok") for k, v in m.items()},
        "stabil": bool(st.get("median_verschiebung_px") is not None
                       and st["median_verschiebung_px"] <= 2.0
                       and st.get("max_verschiebung_px") is not None
                       and st["max_verschiebung_px"] <= 3.0),
        "stabilitaet_median_px": st.get("median_verschiebung_px"),
        "stabilitaet_max_px": st.get("max_verschiebung_px"),
        "regionen_anteil": m["regionen"].get("anteil"),
        "regionen_marge_min_px": m["regionen"].get("marge_min_px"),
        "kamera_fuellgrad": m["kamera"].get("fuellgrad"),
        "kamera_zoom": m["kamera"].get("zoom"),
        "budget_ruhe_ms": m["budget"].get("ruhe_ms"),
        "beschriftungen_gezeichnet": m["beschriftungen"].get("gezeichnet"),
        "konstanten_gesendet": d.get("konstanten_gesendet"),
        "alle_kriterien_erfuellt": d.get("alle_kriterien_erfuellt"),
    }


def _bilder(label: str) -> dict:
    datei = PROBES / ("p105_b14_karte_bilder_konstante_%s.json" % label)
    d = json.loads(datei.read_text(encoding="utf-8"))
    datei.unlink()
    k, f = d["koerper"], d["form"]
    return {
        "koerper_ok": k["ok"], "koerper_grund": k["grund"],
        "komponenten": k["abnahme"]["komponenten"],
        "lappen_je_space": k["abnahme"]["lappen_je_space"],
        "furche_zellen": k["abnahme"]["furche_zellen"], "paare": k["abnahme"]["paare_zahl"],
        "reach_px": k["reach_welt_px"], "luft_px": k["luft_px"],
        "compute_lobes_ms_201": k["zeit"].get("zeit_ms"),
        "soliditaet": f["fuelle"]["soliditaet"],
        "nn_median_px": f["verteilung"]["nn_median_px"],
        "zusatzkruemmung": f["welligkeit"]["zusatzkruemmung_rad_je_100px"],
        "kontur_abstand_px": f["kontur_abstand"]["min_px"],
        "kanten_aussen": f["kanten_aussen"]["anteil"],
        "form_zellen": f["zellen"],
    }


def main() -> int:
    nur = None
    for a in sys.argv[1:]:
        if a.startswith("--nur="):
            nur = set(a.split("=", 1)[1].split(","))
    alt = json.loads(ERGEBNIS.read_text(encoding="utf-8")) if ERGEBNIS.exists() and nur else {}
    tabelle = alt.get("varianten", {})
    for label, konst in VARIANTEN + GLAETTUNG:
        if nur and label not in nur:
            continue
        zeile = {"konstanten": konst}
        if "LOBE_SMOOTH_PASSES" not in konst:
            lauf = _lauf("p105_b14_layout_probe.py", label, konst, [])
            zeile["layout_lauf"] = lauf
            if "fehler" not in lauf:
                zeile["layout"] = _layout(label)
        bild = BILDER_WURZEL / label
        bild.mkdir(parents=True, exist_ok=True)
        lauf = _lauf("p105_b14_karte_bilder.py", label, konst, ["--bilder=%s" % bild])
        zeile["bilder_lauf"] = lauf
        if "fehler" not in lauf:
            zeile["bilder"] = _bilder(label)
            zeile["bilder_verzeichnis"] = str(bild)
        tabelle[label] = zeile
        ERGEBNIS.write_text(json.dumps({"probe": "p105_b14_7_raster", "schritt": "14.7.2",
                                        "varianten": tabelle}, ensure_ascii=False, indent=2)
                            + "\n", encoding="utf-8")
        print(label, json.dumps({k: zeile.get(k) for k in ("layout", "bilder")},
                                ensure_ascii=False)[:400], flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
