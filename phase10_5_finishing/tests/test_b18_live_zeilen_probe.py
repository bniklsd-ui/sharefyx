"""Block 18, Schritt 18.5: der **Beleg** der Live-Zeilen-Probe (`probes/p105_b18_live_zeilen_probe.py`).

Die Probe startet eine Wegwerf-Instanz, einen lokalen Caddy 2.6.2 und Chromium (rund eine Minute je
Lauf) und kann deshalb nicht in der Suite laufen. Dieser Waechter prueft die **Belegdateien** im Repo
(Muster `test_b18_karte_messung.py`): der Normalfall ist an **beiden** Eingaengen gruen, jeder
Gegenlauf macht **seine** Zelle rot und nur die, die er soll.

| Beleg | Inhalt |
|---|---|
| `p105_b18_live_zeilen.json` | Normalfall, Eingaenge `direkt` und `caddy` (Caddy 2.6.2): `waiting`, `wechsel`, `ereignis` gruen |
| `p105_b18_live_zeilen_gegenlauf_poll.json` | Stau von 600 ms auf `/overview`: `waiting` und `wechsel` rot |
| `p105_b18_live_zeilen_gegenlauf_stream.json` | Verzug von 3 s im Ereignis-Stream: **nur** `ereignis` rot |
| `p105_b18_live_zeilen_gegenlauf_caddy_puffer.json` | Caddy `buffer_responses`: am Eingang `caddy` kommt kein Ereignis an (nur dieser Eingang gelaufen) |
"""
from __future__ import annotations

import json
from pathlib import Path

PROBES = Path(__file__).resolve().parents[1] / "probes"


def _laden(name: str) -> dict:
    return json.loads((PROBES / name).read_text(encoding="utf-8"))


def test_the_normal_run_is_green_at_both_entrances():
    beleg = _laden("p105_b18_live_zeilen.json")
    assert beleg["caddy_version"] == "v2.6.2"      # die Live-Version (V199)
    assert beleg["zellen"] == {"waiting": True, "wechsel": True, "ereignis": True}
    assert set(beleg["eingaenge"]) == {"direkt", "caddy"}
    for roh in beleg["eingaenge"].values():
        assert max(roh["waiting_ms"]) <= 300
        assert max(roh["wechsel_ms"]) <= 1000
        assert len(roh["ereignisse"]) == 5 and all(e["angekommen"] for e in roh["ereignisse"])


def test_the_poll_counter_run_turns_waiting_and_wechsel_red():
    beleg = _laden("p105_b18_live_zeilen_gegenlauf_poll.json")
    assert beleg["gegenlauf"] == "poll"
    assert beleg["zellen"]["waiting"] is False and beleg["zellen"]["wechsel"] is False


def test_the_stream_counter_run_turns_only_ereignis_red():
    beleg = _laden("p105_b18_live_zeilen_gegenlauf_stream.json")
    assert beleg["gegenlauf"] == "stream"
    assert beleg["zellen"] == {"waiting": True, "wechsel": True, "ereignis": False}
    for roh in beleg["eingaenge"].values():       # an **beiden** Eingaengen gemessen
        assert all(e["ereignis_ms"] > 2000 for e in roh["ereignisse"])


def test_the_caddy_buffer_counter_run_loses_the_events_at_the_proxy():
    beleg = _laden("p105_b18_live_zeilen_gegenlauf_caddy_puffer.json")
    assert beleg["gegenlauf"] == "caddy_puffer"
    assert set(beleg["eingaenge"]) == {"caddy"}
    assert beleg["zellen"]["ereignis"] is False
    assert all(e["ereignis_ms"] is None for e in beleg["eingaenge"]["caddy"]["ereignisse"])
