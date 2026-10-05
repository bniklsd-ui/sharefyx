"""Tests für den Reload-Overload der Karte — P9-Plan §7.4 (Step E).

Vier Tests, die Abnahmezeilen P9-33/P9-34/P9-35 und V118:

  1. test_load_graph_skips_the_refetch_when_the_signature_is_unchanged   (P9-33)
  2. test_known_nodes_keep_their_position_across_reentry                 (P9-34)
  3. test_the_drop_point_is_off_the_seed_ring          (Kontrollmessung zu 2)
  4. test_own_writes_reload_the_graph_immediately                        (P9-35)
  5. test_the_token_format_has_a_single_owner          (Eigentums-Wächter)
  6. test_graph_module_does_not_touch_the_api_contract  (P9-M / §7.2)
  7. test_a_tag_edge_beside_an_explicit_edge_draws_one_line              (V118 / P9-36)

**Warum ein Node-Prozess und kein reiner Text-Test:** `graph.js` ist ein ES-Modul ohne
Build-Schritt (P5-T). Ob der zweite Eintritt in die Übersicht wirklich *keinen* `/graph`-Abruf
auslöst und ob ein bekannter Knoten seine Position behält, ist nur an einem echten Lauf des
Moduls prüfbar — beides sind Zusicherungen über das Zeitverhalten einer Promise-Kette, nicht
über eine Codeform. Der Harness `phase9_hardening/scripts/graph_reload_probe.mjs` lädt das echte
Modul mit einem minimalen DOM-Shim (Canvas-Box, 2d-Context als Strichzähler, `matchMedia`,
`requestAnimationFrame`), zählt die `fetch`-Aufrufe und gibt JSON aus. Er läuft einmal pro
Test-Sitzung (Modul-Fixture), jeder Test liest seinen Ausschnitt.

**Gegenprobe, kein blindes Vertrauen:** derselbe Harness gegen die vier JS-Dateien aus HEAD
(`git stash push -- phase5_ui/webui/static/js/`) lässt fünf von acht Prüfungen rot, gemessen
2026-09-26: `state_module_exposes_the_token_builder`, `p9_33_no_second_fetch` (2 Abrufe statt 1),
`p9_34_reentry_does_not_restart_the_simulation`,
`p9_34_known_nodes_keep_their_position` (Knoten springt **467,6 px** zurück auf den Seed-Ring
statt 0) und `p9_35_own_write_is_visible_immediately`. Die beiden ausgenommenen Prüfungen sind
Absicht: die Kontrollmessung misst einen Punkt des Messaufbaus, und der V118-Test hat am
2026-10-05 eine **Datumsumkehr** erfahren (die Zwillingskante wurde zur einen Linie) — die
Gegenprobe-Liste hier beschreibt also den Stand **vor** diesem Tag; der V118-Eintrag ist seit
dem settings-Block die **umgedrehte** Fassung desselben Gedankens.

Kein Netz, kein Browser, kein DATA_ROOT, kein Dienst. Node muss vorhanden sein (das Repo prüft
schon `node --check` in seiner Selbstprüf-Liste); fehlt es, werden die drei Laufzeit-Tests
übersprungen, Test 3 läuft immer.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
PROBE = REPO_ROOT / "phase9_hardening" / "scripts" / "graph_reload_probe.mjs"
GRAPH_JS = REPO_ROOT / "phase5_ui" / "webui" / "static" / "js" / "graph.js"

needs_node = pytest.mark.skipif(shutil.which("node") is None, reason="node fehlt (P5-T: kein Build)")


@pytest.fixture(scope="module")
def probe() -> dict:
    """Ein Lauf des Node-Harnesses, Ergebnis als dict. Bricht bei Exit != 0 hart ab."""
    proc = subprocess.run(
        ["node", str(PROBE)],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert proc.returncode == 0, (
        f"graph_reload_probe.mjs endete mit {proc.returncode}\n"
        f"--- stdout ---\n{proc.stdout}\n--- stderr ---\n{proc.stderr}"
    )
    return json.loads(proc.stdout)


@needs_node
def test_load_graph_skips_the_refetch_when_the_signature_is_unchanged(probe: dict) -> None:
    """P9-33: ein zweiter Eintritt ohne Datenänderung erzeugt keinen zweiten `/graph`-Abruf."""
    result = probe["p9_33_no_second_fetch"]
    assert result["ok"], result
    assert result["fetches_first_entry"] == 1, result
    assert result["fetches_total_after_second_entry"] == 1, (
        "Zweiter Eintritt hat erneut abgerufen — der Mechanismus aus Plan §7.2(a) greift nicht"
    )
    # Und er startet auch keine neue Simulation: das wäre der Rest des Sprungs (P9-34).
    assert result["frames_queued_after_reentry"] == 0, result


@needs_node
def test_known_nodes_keep_their_position_across_reentry(probe: dict) -> None:
    """P9-34: ein bekannter Knoten behält x/y über einen Refetch hinweg.

    Gemessen wird über den echten Drag-Pfad: der Knoten wird an (123, 456) gezogen (weit
    außerhalb des Seed-Rings um die Canvas-Mitte), danach wird das Neuladen erzwungen und nach
    genau einem Simulations-Tick gemessen, wie weit er von der Ablegestelle entfernt ist.
    """
    result = probe["p9_34_known_nodes_keep_their_position"]
    assert result["refetch_happened"], "Der Refetch lief nicht — der Test hätte nichts geprüft"
    assert result["ok"], result
    # Ein Tick bewegt einen Knoten um wenige Pixel; der Sprung zurück auf den Seed-Ring wäre bei
    # 800x600 Canvas (Mitte 400/300, Radius ~150) zweistellig über hundert Pixel.
    assert result["distance_after_refetch"] <= 25, result


@needs_node
def test_own_writes_reload_the_graph_immediately(probe: dict) -> None:
    """P9-35, zweite Hälfte: der **eigene** Schreibvorgang darf nicht bis zum 20s-Poll warten.

    Das ist der Weg, den die erste Verdrahtung dieser Session kaputt gemacht hätte: ein Token,
    das nur im Poll und beim Bootstrap gesetzt wird, lässt den gerade selbst gespeicherten Titel
    erst nach dem nächsten Poll im Graphen auftauchen. Im Produktivcode setzt
    `list.js :: loadOverview()` das Token, und jeder Schreibpfad (afterWrite, Archivieren,
    Ordner, Space anlegen/entfernen) läuft durch genau diese Funktion.
    """
    result = probe["p9_35_own_write_is_visible_immediately"]
    assert result["ok"], result
    assert result["refetched_after_the_write"] == 1, result
    assert result["refetched_on_reentry"] == 0, result


@needs_node
def test_the_token_format_has_a_single_owner(probe: dict) -> None:
    """`state.js :: overviewToken()` ist die einzige Stelle, die das Signatur-Format kennt.

    Erzeuger (`list.js`) und Verbraucher (`graph.js`) importieren sich nicht — `graph.js`
    importiert `editor.js`, `editor.js` importiert `list.js`. Deshalb liegt das Format im
    Blatt-Modul `state.js`. Ohne diesen Wächter könnte das Format wandern und der Mechanismus
    fiele stillschweigend auf "immer neu laden" zurück, ohne dass ein Test rot wird.
    """
    assert probe["state_module_exposes_the_token_builder"]["ok"], probe


@needs_node
def test_the_drop_point_is_off_the_seed_ring(probe: dict) -> None:
    """Kontrollmessung zu Test 2: die Ablegestelle liegt weit weg vom Seed-Ring.

    Ohne diese Gegenprobe wäre „25 px Abstand nach dem Refetch" eine Aussage über einen Punkt,
    der möglicherweise zufällig auf dem Ring liegt — der Test wäre dann grün, ohne etwas zu
    prüfen. Sie ist Teil von Test 2s Beweiskette und deshalb ein eigener Test.
    """
    result = probe["p9_34_control_drop_point_is_off_the_ring"]
    assert result["ok"], result
    assert result["distance_before_drag"] > 100, result


def test_graph_module_does_not_touch_the_api_contract() -> None:
    """P9-M / Plan §7.2: dieser Step fasst `/api/v1/graph` nicht an.

    Geprüft wird statisch und in beide Richtungen: `graph.js` ruft genau **einen** Endpunkt auf
    (unverändert `"/graph"`), und es taucht kein wörtliches `/api/v1/...` im Modul auf — eine
    zweite Route oder eine Routereihe wäre eine Contract-Öffnung, die Step F (P9-G) gehört.
    """
    source = GRAPH_JS.read_text(encoding="utf-8")
    # Kommentare raus: das Modul dokumentiert die Feldnamen des Knoten-Payloads im Klartext, ein
    # auskommentiertes `api("/…")` darf nicht als Aufruf zählen. Zeilenweise vorgenüglich genügt
    # hier, weil keine Zeile der Datei einen `//` **innerhalb** eines Strings trägt.
    code = "\n".join(
        line for line in source.splitlines() if not line.lstrip().startswith("//")
    )
    calls = set(re.findall(r'api\(\s*"([^"]+)"', code))
    assert calls == {"/graph"}, f"Unerwartete API-Aufrufe in graph.js: {sorted(calls)}"

    # Zweite Richtung, präziser als ein Textvergleich: **String-Literale**, die eine absolute
    # Route nennen. Ein Kommentar darf `/api/v1/overview` erwähnen (er tut es, zu Recht), ein
    # String-Literal im Code nicht — die Basis legt `api.js` fest.
    literals = re.findall(r'"((?:[^"\\]|\\.)*)"', code)
    absolute_routes = [lit for lit in literals if lit.startswith("/api/")]
    assert not absolute_routes, (
        f"Absolute Routen in graph.js: {absolute_routes} — der Präfix gehört api.js"
    )


@needs_node
def test_a_tag_edge_beside_an_explicit_edge_draws_one_line(probe: dict) -> None:
    """V118 (P9-36), **zweite Lesart, mit Datum in beide Richtungen.**

    ***2026-09-26, erste Lesart (gemessen, vom Code eingefroren):*** eine Tag-Kante UND eine
    explizite Kante zwischen denselben zwei Knoten ergaben **zwei Linien**, von denen eine
    gestrichelt war — `dedupeEdges()` fasste nur die Expliziten zusammen, `buildTagEdges()`
    nur die Tag-Kanten, und `drawEdges()` führte beides ohne Dedup zusammen.

    ***2026-10-05, zweite Lesart (Nikinger):*** **eine Linie.** *„Wenn A auf B verlinkt, ist B
    für A automatisch relevant."* Die explizite Kante gewinnt und bleibt durchgezogen; die
    implizite Kante desselben Paares entfällt bereits bei der Übernahme in
    `rebuildImplicitEdges()` — nicht erst in `drawEdges()`, damit die Gradzählung
    (`recomputeDegrees()`, davon die Knotengröße) dasselbe Bild zeigt. Dasselbe Argument wie
    bei `dedupeEdges()` (P8.6-N).

    **Der Testname wurde umgedreht, nicht der Test gelöscht:** ein Name, der das Gegenteil
    behauptet, wäre eine Lüge. Der Docstring nennt beide Lesarten mit Datum, damit ein
    späterer Leser nicht denkt, die Zwillingskante sei nie gemessen gewesen.
    """
    result = probe["v118_tag_edge_beside_explicit_edge"]
    assert result["ok"], result
    assert result["segments_in_last_frame"] == 1, result
    assert result["duplicate_segments"] == 0, (
        "Erwartet: genau eine Linie für das Paar, keine doppelt gezeichnete Strecke"
    )
    assert result["a_solid_line_was_drawn"], (
        "Die durchgezogene Linie muss bleiben — der Test darf nicht grün werden, indem die "
        "Kante einfach verschwindet"
    )
    assert not result["a_dashed_line_was_drawn"], (
        "Es darf keine gestrichelte Linie mehr im Bild sein: die implizite Kante wird "
        "gebaut und bei der Übernahme verworfen, nicht erst beim Zeichnen"
    )
