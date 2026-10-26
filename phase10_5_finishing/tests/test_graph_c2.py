"""Wächter für die Gehirnkarte C2 — P10.5 Block 8 (Plan §Block 8, Schritt 8.1–8.7).

`graph.js` ist ein ES-Modul ohne Build-Schritt (P5-T). Was die Karte **zeichnet** — Lappen,
Furchen, Bahnen, Zellen, Ringe, Beschriftungen — ist nur an einem echten Lauf des Moduls
prüfbar. Der Harness `phase10_5_finishing/probes/p105_b8_c2_probe.mjs` lädt das echte Modul in
Node mit einem minimalen DOM-Shim und misst die Zeichenbefehle. Er schreibt seine Rohwerte
nach `p105_b8_c2_probe.json` (neben der Probe).

**Acht Messungen, acht Gegenläufe.** Ein Wächter ohne Gegenlauf beweist nichts: eine Messung,
die die falsche Sache misst, ist grün und falsch zugleich (die Fehlerklasse, die dieser
Ordner zweimal gesehen hat). Jeder Gegenlauf patcht **eine** Regel in einer Kopie von
`graph.js` und muss **genau die** zugehörige Messung rot machen:

| Messung | Plan | Gegenlauf | Der Fehler |
|---|---|---|---|
| `lappen` | 8.1 | `lappen` | die Lappen werden nicht gezeichnet |
| `furche` | 8.1 | `furche` | die Furche entfällt, die Lappen wachsen ineinander |
| `bahnen` | 8.2 | `bahnen` | die Bahnen werden gerade statt geschwungen |
| `zellen` | 8.3 | `zellen` | die Fortsätze werden zufällig statt deterministisch |
| `aktivierung` | 8.4 | `aktivierung` | die Abdunklung bleibt auf dem P8-Wert 0,15 |
| `layout` | 8.5 | `layout` | die gemerkte Position wird nicht festgehalten |
| `filter` | 8.6 | `filter` | der Filter lässt alles durch |
| `reducedmotion` | 8.7 | `reducedmotion` | der reduced-motion-Pfad läuft über rAF |

Kein Netz, kein Browser, kein DATA_ROOT, kein Dienst. Node muss vorhanden sein; fehlt es,
überspringt die Laufzeitprüfung (die Testdateien laufen trotzdem).

**Datierte Änderung am Eingang (2026-10-26, Schritt 14.2).** Die Probe setzt die Knoten
**fest** (über die Ablage, `pinned`): der Wächter misst die **Zeichenregel** (Schritt 8.1),
nicht das **Layout**. Grund: bis 14.2 hing die Furche-Messung an einem Unfall — die
Zentrums-Gravitation zog alle Spaces in einen Klumpen, die Lappen stiessen aneinander, und
die Furche trennte sie. Mit der neuen L4 (Anker-Gravitation, Querfedern) rücken die Spaces
auseinander, die Furche hat **keinen Gegenstand** mehr (**gemessen**: 62 Zellen vorher, **0**
nachher) ⇒ der Gegenlauf „`furche` aus" wäre **grün** geblieben, ohne dass der Fehler
wiederhergestellt war. Der feste Eingang (zwei Spaces **berühren** sich) macht den
Gegenlauf wieder scharf. Das Layout misst der Browser-Wächter
(`p105_b14_layout_probe.py`), nicht dieser.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
PROBE = REPO_ROOT / "phase10_5_finishing" / "probes" / "p105_b8_c2_probe.mjs"
JSON_OUT = PROBE.with_suffix(".json")

needs_node = pytest.mark.skipif(shutil.which("node") is None, reason="node fehlt (P5-T: kein Build)")

# Die Messungen und ihre Gegenläufe. Der Name des Gegenlaufs muss in der Probe stehen -- ein
# Tippfehler im Wächter waere sonst ein Gegenlauf, der nichts tut (und trotzdem "grün" meldet).
MESSUNGEN = [
    ("lappen", "lappen"),
    ("furche", "furche"),
    ("bahnen", "bahnen"),
    ("zellen", "zellen"),
    ("aktivierung", "aktivierung"),
    ("layout", "layout"),
    ("filter", "filter"),
    ("reducedmotion", "reducedmotion"),
]


def _run(gegenlauf: str | None = None) -> dict:
    cmd = ["node", str(PROBE)]
    if gegenlauf:
        cmd += ["--gegenlauf", gegenlauf]
    proc = subprocess.run(
        cmd, cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=180,
    )
    assert proc.returncode == 0, (
        f"p105_b8_c2_probe.mjs endete mit {proc.returncode}\n"
        f"--- stdout ---\n{proc.stdout}\n--- stderr ---\n{proc.stderr}"
    )
    return json.loads(proc.stdout)


@pytest.fixture(scope="module")
def messung() -> dict:
    """Der Normalfall: alle acht Messungen muessen gruen sein."""
    return _run()


@needs_node
def test_alle_messungen_sind_gruen(messung: dict) -> None:
    """Der Normalfall — jede Messung traegt ihr eigenes `ok`."""
    rot = [name for name, _ in MESSUNGEN if not messung[name].get("ok")]
    assert not rot, f"Rote Messungen: {rot}\n{messung}"


@needs_node
def test_die_lappen_werden_je_space_gezeichnet(messung: dict) -> None:
    """8.1: je Space ein Lappen, die Flaeche leise (5%), die Kontur halb deckend (55%),
    die innere Linie als **feste Farbe** (kein Alpha, P8 §0.3 Nr. 6)."""
    m = messung["lappen"]
    assert m["lobe_fills"] >= 2, m
    assert len(m["lobe_fill_colors"]) >= 2, m
    assert m["fill_alpha"] == [0.05], m
    assert 0.55 in m["contour_alpha"], m
    assert m["inner_contours"] >= 1, m


@needs_node
def test_die_furche_trennt_die_lappen(messung: dict) -> None:
    """8.1: die Konturen zweier Spaces duerfen sich nicht beruehren.

    Und (datierte Ergaenzung, 2026-10-26, Schritt 14.2): die Regel muss einen **Gegenstand**
    haben — die Zahl der Furche-Zellen muss groesser als null sein. Ohne diese Zelle waere
    der Abstand allein gemessen — und ein Abstand, den es gar nicht gibt (die Spaces stehen
    weit auseinander), waere auch "gemessen".
    """
    m = messung["furche"]
    assert m["contours_compared"] >= 2, m
    assert m["separation_px"] > 0, m
    assert m["furrow_cells"] > 0, m


@needs_node
def test_die_bahnen_sind_geschwungen_und_ihre_breite_follows_grad(messung: dict) -> None:
    """8.2: die Breite ist 1 + log2(1 + min(deg(a), deg(b))) -- zwei Stufen im Bild."""
    m = messung["bahnen"]
    assert m["edges_drawn"] == 5, m
    assert len(m["widths"]) >= 2, m
    assert all(1.99 <= w <= 2.59 for w in m["widths"]), m


@needs_node
def test_die_zellen_haben_fortsaetze_und_sind_deterministisch(messung: dict) -> None:
    """8.3: 2-4 Fortsaetze je Zelle, aus dem Hash der Item-ID -- gleiche Zeichnung je Laden."""
    m = messung["zellen"]
    assert m["cells"] == 6, m
    assert 12 <= m["process_segments"] <= 24, m
    assert m["deterministic"], m


@needs_node
def test_die_aktivierung_hat_drei_stufen(messung: dict) -> None:
    """8.4: in Ruhe alles voll deckend; mit Fokus 1 / 0,5 / 0,45."""
    m = messung["aktivierung"]
    assert m["alphas_at_rest"] == [1], m
    assert set(m["alphas_with_focus"]) == {1, 0.5, 0.45}, m


@needs_node
def test_das_layout_ueberlebt_das_neuladen(messung: dict) -> None:
    """8.5: der Zug des Menschen ueberlebt das Neuladen -- die Position bleibt (≤ 1 px,
    weil die Ablage auf ganze Pixel rundet)."""
    m = messung["layout"]
    assert m["stored_version"] == 1, m
    assert m["stored_entries"] == 6, m
    assert m["deviation_px"] is not None and m["deviation_px"] <= 1, m


@needs_node
def test_suche_und_filter_wirken(messung: dict) -> None:
    """8.6: die Suche dimmt die Nicht-Treffer und zaehlt sie; der Filter blendet Knoten
    **und** Bahnen aus."""
    m = messung["filter"]
    assert 1 in m["search_alphas"] and 0.45 in m["search_alphas"], m
    assert "Treffer" in m["hit_counter"], m
    assert m["cells_with_type_filter"] == 3, m
    assert m["edges_with_type_filter"] == 1, m


@needs_node
def test_reduced_motion_ist_statisch_und_hat_null_frames(messung: dict) -> None:
    """8.7 (Abnahme P10.5-40): kein einziges requestAnimationFrame, aber ein gemaltes Bild."""
    m = messung["reducedmotion"]
    assert m["raf_calls"] == 0, m
    assert m["painted_nodes"] > 0, m


@needs_node
@pytest.mark.parametrize("messung_name,gegenlauf", MESSUNGEN)
def test_der_gegenlauf_macht_die_messung_rot(messung_name: str, gegenlauf: str) -> None:
    """Jeder Gegenlauf muss **genau seine** Messung rot machen.

    Das ist der Teil, der die Messung ueberhaupt erst traegt: eine gruene Messung ohne
    Gegenlauf beweist, dass der Wächter laeuft -- nicht, dass er die richtige Sache misst.
    """
    daten = _run(gegenlauf)
    assert not daten[messung_name].get("ok"), (
        f"Der Gegenlauf '{gegenlauf}' hat die Messung '{messung_name}' NICHT rot gemacht — "
        f"der Anker griff nicht oder die Messung prueft das Falsche: {daten[messung_name]}"
    )


@needs_node
def test_die_rohwerte_liegen_neben_der_probe() -> None:
    """Plan §2.3: die Rohwerte als JSON neben der Probe (nicht nur auf stdout)."""
    assert JSON_OUT.exists(), f"{JSON_OUT} fehlt — der Normalfall muss seine Werte ablegen"
    daten = json.loads(JSON_OUT.read_text(encoding="utf-8"))
    assert daten["ausfuehrer"]["gegenlauf"] is None, "die abgelegten Werte muessen der Normalfall sein"
    assert daten["lappen"]["ok"], daten["lappen"]


# ============================================================================================
# Die drei Korrekturen, die erst der **Browser** gefunden hat (2026-10-24, Wegwerf-Instanz)
# ============================================================================================
#
# Der Node-Harness (`p105_b8_c2_probe.mjs`) sieht die Zeichenbefehle, aber keinen echten
# Zeiger und keine echte Zeit. Drei Fehler hat erst die Browser-Probe
# (`probes/p105_b8_karte_probe.py`) gezeigt -- die Wächter unten halten sie fest. Die Anker
# sind die **Regeln**, nicht die Werte: ein Gegenlauf, der einen Kommentar antrifft, beweist
# nichts (diese Fehlerklasse hat der Ordner zweimal gesehen).

GRAPH_JS = REPO_ROOT / "phase5_ui" / "webui" / "static" / "js" / "graph.js"
APP_HTML = REPO_ROOT / "phase5_ui" / "webui" / "static" / "app.html"


def test_der_gezogene_knoten_wird_gepinnt_und_nicht_wieder_freigegeben() -> None:
    """Der Zug des Menschen muss **stehen bleiben** — sonst zieht die Simulation ihn zurück
    und die Ablage speichert die zurückgezogene Position (KA-2 wäre nicht erfüllt).

    Gemessen 2026-10-24 an der Wegwerf-Instanz: der Browser-Gegenlauf `layout` (der gemerkte
    Knoten wird nicht festgehalten) lässt den Knoten nach dem Neuladen **verschwunden**
    (0 Kernpixel am Ziel statt 106).
    """
    quelle = GRAPH_JS.read_text(encoding="utf-8")
    assert "dragNode.pinned = true;" in quelle, (
        "der gezogene Knoten wird nicht gepinnt — die Simulation zieht ihn zurück"
    )
    assert "pinnedIds[dragNode.id] = true;" in quelle, (
        "der gezogene Knoten steht nicht in `pinnedIds` — der Reset raeumt ihn sonst nicht ab"
    )


def test_der_fokus_endet_mit_dem_zeiger() -> None:
    """Verlaesst der Zeiger das Canvas, endet der Fokus (und mit ihm das Abdunkeln).

    Plan 8.4: „Ruhezustand ohne Fokus: alles voll deckend." Gemessen 2026-10-24: die Karte
    blieb abgedunkelt (26164 statt 13989 Kernpixel im Vergleichsbild), bis der Zeiger
    wieder ueber sie fuhr.
    """
    quelle = GRAPH_JS.read_text(encoding="utf-8")
    verlassen = quelle.split("function onMouseLeave", 1)[1].split("\n}", 1)[0]
    assert "hoverId = null;" in verlassen, (
        "`onMouseLeave()` raeumt den Fokus nicht ab — die Karte bleibt abgedunkelt"
    )


def test_die_trefferzahl_hat_ihr_eigenes_feld() -> None:
    """Die Trefferzahl der Suche steht in einem **eigenen** Feld.

    Vorher stand sie in der Statuszeile — und der Layout-Hinweis („Layout gemerkt", der 1 s
    nach dem Speichern kommt) hat sie ueberschrieben: die Zahl war weg, obwohl die Suche lief.
    Gemessen 2026-10-24: die Statuszeile trug „Layout gemerkt" statt „10 Treffer".
    """
    html = APP_HTML.read_text(encoding="utf-8")
    assert 'id="overview-graph-hits"' in html, "das Feld fuer die Trefferzahl fehlt im Markup"
    quelle = GRAPH_JS.read_text(encoding="utf-8")
    assert 'document.getElementById("overview-graph-hits")' in quelle, (
        "die Trefferzahl wird nicht in das eigene Feld geschrieben"
    )
    # Die Statuszeile darf die Trefferzahl nicht mehr setzen.
    treffer = quelle.split("function updateHitCount", 1)[1].split("\n}", 1)[0]
    assert "statusEl" not in treffer, (
        "`updateHitCount()` schreibt noch in die Statuszeile — der Layout-Hinweis loescht sie"
    )
