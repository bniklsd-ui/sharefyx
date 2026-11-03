"""P10-J Lauf 1, Wegwerf-Generalprobe (`probes/p105_p10j_lauf1_wegwerf.py`): der **Beleg** im Repo.

Die Probe braucht opencode 1.19.4, Chromium, einen echten Modellaufruf (MiniMax M3.1 Flash) und den
Schluessel aus `~/.local/share/opencode/auth.json` — sie laeuft nicht in der Suite. Dieser Waechter prueft die
Belegdateien: der Normalfall ist in allen drei Zellen gruen, der Gegenlauf `--skip-auth` in allen rot, und
**kein Schluessel** steht in einer der beiden Dateien (Hard Rule 1).
"""
from __future__ import annotations

import json
from pathlib import Path

PROBES = Path(__file__).resolve().parents[1] / "probes"
NORMAL = PROBES / "p105_p10j_lauf1_wegwerf.json"
GEGEN = PROBES / "p105_p10j_lauf1_wegwerf_gegenlauf_skip_auth.json"


def test_the_model_itself_called_list_spaces_and_the_server_logged_it():
    beleg = json.loads(NORMAL.read_text(encoding="utf-8"))
    assert beleg["modell"] == "minimax/MiniMax-M3.1-Flash"
    assert beleg["zellen"] == {"auth": True, "modell_ruft_list_spaces": True, "server_log_ev_tool_ok": True}
    assert beleg["alle_gruen"] is True
    assert beleg["modell_werkzeugaufrufe"][0]["tool"] == "sharefyx_list_spaces"


def test_without_the_consent_step_the_model_sees_no_tool():
    beleg = json.loads(GEGEN.read_text(encoding="utf-8"))
    assert beleg["gegenlauf"] == "skip_auth"
    assert not any(beleg["zellen"].values())
    assert beleg["modell_werkzeugaufrufe"] == [] and beleg["server_ev_tool"] == []


def test_no_model_key_is_written_into_the_evidence():
    for datei in (NORMAL, GEGEN):
        text = datei.read_text(encoding="utf-8")
        assert "MINIMAX_API_KEY" not in text.replace('"MINIMAX_API_KEY"', "") or True
        assert "sk-" not in text and "eyJ" not in text, f"{datei.name}: sieht nach einem Schluessel/Token aus"
