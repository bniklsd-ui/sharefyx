"""Wächter für `phase10_5_finishing/probes/p105_b5_protocol_probe.py` (P10.5 Block 5, Schritt 5.6).

Die Probe fährt `create_app()` in-process in **beiden** MCP-Protokoll-Ären (P10.5-P):
`legacy` = Handshake `2025-11-25` (so verbindet sich claude.ai heute), `auto` = zustandslos
`2026-07-28`. Dieser Test ruft sie auf und hält die Abnahmezeilen P10.5-20/21 fest, damit ein
späteres Anheben von `fastmcp` nicht still eine Ära verliert. Kein Netz, `tmp`-`DATA_ROOT`.
"""
from __future__ import annotations

import asyncio
import importlib.util
from pathlib import Path

import pytest

PROBE = Path(__file__).resolve().parents[1] / "probes" / "p105_b5_protocol_probe.py"


@pytest.fixture(scope="module")
def result() -> dict:
    spec = importlib.util.spec_from_file_location("p105_b5_protocol_probe", PROBE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return asyncio.run(module.run())


@pytest.mark.parametrize("mode,era", [("legacy", "2025-11-25"), ("auto", "2026-07-28")])
def test_each_era_negotiates_its_own_version_and_serves_list_spaces(result, mode, era):
    assert result[mode]["protocol_version"] == era
    assert result[mode]["list_spaces"] == ["alpha"]


@pytest.mark.parametrize("mode", ["legacy", "auto"])
def test_each_era_carries_annotations_and_the_new_tool(result, mode):
    assert result[mode]["annotations_complete"] is True
    assert len(result[mode]["tool_names"]) == 11
    assert "append_to_items" in result[mode]["tool_names"]
    assert result[mode]["append_to_items"] == {"ok": 1, "failed": 1}


@pytest.mark.parametrize("mode", ["legacy", "auto"])
def test_neither_era_raises_a_deprecation_warning(result, mode):
    assert result[mode]["deprecation_warnings"] == []


def test_an_unknown_protocol_version_is_never_echoed_back(result):
    init = result["unknown_version"]["initialize"]
    assert init["echoes_unknown_version"] is False and init["answers_with_own_version"] is True


def test_the_stateless_era_rejects_an_unknown_version_with_32022(result):
    err = result["unknown_version"]["stateless_tools_list"]
    assert err["status"] == 400 and err["error_code"] == -32022
    assert err["supported"] == ["2026-07-28"]
