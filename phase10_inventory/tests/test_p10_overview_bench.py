"""Wächter für das M2-Instrument `phase10_inventory/probes/p10_overview_bench.py`
(P10-Plan §4 M2, Register PF-1/PF-2).

P10-H erlaubt ausdrücklich „Proben und Messskripte unter `phase10_inventory/` samt Tests
dafür". Diese Tests sind absichtlich klein (12 Items im HTTP-Pfad) — sie prüfen die
**Struktur und die Fallen**, nicht die Latenz: eine Zeitbehauptung in einem Unit-Test wäre
auf einer ausgelasteten VM ein Flake, die Latenz selbst messen die echten Läufe (Register).

Das Laden folgt dem Muster aus `phase9_hardening/tests/test_doc_health.py` — das Probe-
Skript ist kein installiertes Paket, also per `spec_from_file_location`. Die wichtigste
Assertion ist dieselbe, die das Instrument beim Lauf selbst stellt: der Principal muss
**alle vier** Spaces sehen. Genau daran wäre das Messbild still das alte, zu niedrige
Ein-Space-Bild (PF-2, `ui_budget.py` misst 3,3× zu niedrig) — ein Wächter, der das nicht
meldet, würde die eine Messung grün lassen, die PF-1s Größe falsch ausweist.
"""
from __future__ import annotations

import asyncio
import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "phase10_inventory" / "probes" / "p10_overview_bench.py"

spec = importlib.util.spec_from_file_location("p10_overview_bench", SCRIPT)
bench = importlib.util.module_from_spec(spec)
sys.modules["p10_overview_bench"] = bench
spec.loader.exec_module(bench)

# Dieselbe Bucket-Tabelle wie `webui/api.py :: _BUCKETS` (P9 doing-Block) — hier nochmal,
# weil der Test sie gegen den Seed halten will und `webui` eine volle App-Importkette zieht.
_BUCKETS = {
    "open": {"type": "task", "status": "open"},
    "doing": {"type": "task", "status": "doing"},
    "done": {"type": "task", "status": "done"},
    "note": {"type": "note", "status": "active"},
    "archived": {"status": "archived"},
}


def _run(coro):
    return asyncio.run(coro)


def test_seed_distributes_across_all_five_buckets(tmp_path: Path) -> None:
    """Ein Bestand, in dem ein Bucket permanent 0 ist, hätte `_overview()`s Filterkostenstelle
    nicht im Bild. Erwartung aus der Verteilungsformel im Seed (i % 10 == 9 → archived,
    i % 5 == 4 → Task, sonst Note): open 1 · doing 2 · done 2 · note 40 · archived 5."""
    store = bench._seed(tmp_path, items_per_space=50)
    expected = {"open": 1, "doing": 2, "done": 2, "note": 40, "archived": 5}
    for bucket, filters in _BUCKETS.items():
        found = store.search(space=bench.HOME_SPACE, limit=1, offset=0, **filters).total
        assert found == expected[bucket], (bucket, found, expected[bucket])


def test_principal_sees_all_four_spaces(tmp_path: Path) -> None:
    """Die PF-2-Falle: sieht der Principal nur einen Space, ist die Messung still 4× zu
    niedrig — genau die Verzerrung, vor der PF-2 das ui_budget-Instrument warnt."""
    result = _run(bench._measure(tmp_path, items_per_space=3))
    assert result["spaces_seen"] == 4
    assert result["items_total"] == 12
    assert result["measured_runs"] == bench.MEASURED_RUNS
    assert len(result["runs_ms"]) == bench.MEASURED_RUNS
    assert result["min_ms"] <= result["median_ms"] <= result["max_ms"]


def test_overview_payload_shape_and_writable_branches(tmp_path: Path) -> None:
    """Form der gemessenen Antwort, nicht ihrer Dauer: 4 Einträge in der Reihenfolge der
    Spaces, Zähler summieren sich zum Bestand, und `writable` ist nur auf dem eigenen und
    dem `write:`-Team-Space wahr (`delta` trägt `write:`, `bravo` nur `read:`)."""
    import httpx
    from webui.config import COOKIE_NAME

    store = bench._seed(tmp_path, items_per_space=3)
    app, session_id = bench._build_app(tmp_path, store)

    async def _fetch():
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(
            transport=transport, base_url="https://p10-bench.local",
            cookies={COOKIE_NAME: session_id},
        ) as client:
            async with app.router.lifespan_context(app):
                return await client.get(bench.OVERVIEW_PATH)

    response = _run(_fetch())
    assert response.status_code == 200
    payload = response.json()
    assert [row["name"] for row in payload] == [bench.HOME_SPACE, *bench.TEAM_SPACES]
    assert sum(row["item_count"] for row in payload) == 12
    assert sum(sum(row["counts"].values()) for row in payload) == 12
    writable = {row["name"]: row["writable"] for row in payload}
    assert writable == {
        bench.HOME_SPACE: True,
        "bravo": False,
        "charlie": False,
        bench.WRITABLE_TEAM_SPACE: True,
    }
