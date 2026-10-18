#!/usr/bin/env python3
"""p10_overview_bench.py — M2 (P10-Plan §4, Register PF-1/PF-2): was kostet
`GET /api/v1/overview` serverseitig bei Live-ähnlicher Last?

**Warum dieses eigene Instrument, wenn `ui_budget.py :: _measure_latency()` bereits eine
Overview-Latenz misst:** `ui_budget.py` sät **einen** Space („alpha", 220 Items) — der
Messprincipal sieht also genau einen Space, und `_overview()` macht einen Durchgang statt
sechs. Die reale Last (P9-15, Handover §4.3) ist **4 Spaces / 197 Items bei ~2,4 s
Serverarbeit**, und `_overview()` (`phase5_ui/webui/api.py`) macht **je sichtbarem Space**
fünf Bucket-Zählungen plus eine Liste — jeder dieser sechs Aufrufe liest jede indizierte
Datei (`Store.search()`, P6-S). Ein Ein-Space-Bestand unterzeichnet die Kosten also rund
um den Faktor der Space-Zahl — genau die Messlatte, die PF-2 als „falsch" verwerfen lässt.
Dieses Instrument sät deshalb **4 Spaces × 50 Items** und legt dem Principal die fremden
drei Spaces per `.share.yml`-`read:` (bzw. `read:`+`write:` für einen) vor — dieselbe
Sichtbarkeitsquelle wie live (`SharePolicy.visible_spaces`, P6 Step 5).

**Gegen die volle App, nicht gegen `api_routes()` allein:** gemessen wird
`mcpserver.app :: create_app()` — derselbe Stack wie live (Mounts, Middleware, Lifespan),
damit die Zahl als P10.5-Abnahme für PF-1 taugt (Plan §4 M2: „dasselbe Instrument wird die
P10.5-Abnahme von PF-1"). In-process über `httpx.ASGITransport`, kein Port, kein Netz,
niemals gegen den echten `DATA_ROOT` (Wegwerf-`tempfile`, wie `ui_budget.py`).

**Ablauf:** 1 verworfener Aufwärmlauf (Routen-Setup, erster Indexaufbau im Cache — dieselbe
Begründung wie `ui_budget.py`s Advisor-Fund 2026-08-09), dann 5 gemessene Läufe. Geprüft
wird vor der Messung, dass der Principal **alle vier** Spaces sieht — sonst wäre die Messung
still das alte, zu niedrige Ein-Space-Bild (der Fall, vor dem PF-2 ausdrücklich warnt).
**Kein Git:** `Store(data_root, git=False)` — die Messung interessiert die Lesekosten der
Overview, nicht Commit-Dauer je Seed-Item (dieselbe Abwägung wie `ui_budget.py` Zeile ~159).

**Ausgabe:** genau ein JSON-Objekt auf stdout (Hard Rule 7), Logs auf stderr. Kein
Zeitstempel im JSON — identischer Bestand ⇒ identische Struktur, die Datierung übernimmt
die Registerzeile, nicht das Instrument. P10-5 (Plan §5) prüft die Reproduzierbarkeit über
**drei** aufeinanderfolgende Instrument-Läufe: ihre `median_ms`-Werte müssen innerhalb
±10 % des Medians liegen — das misst der Aufrufer, nicht dieses Skript.

**Bewusst nicht gemessen hier:** M1 (Mensch, beide Eingänge, Browser des Nikingers) und der
Netz-/Tunnel-Anteil — in-process über den ASGI-Transport gibt es weder TLS noch Relay, die
Zahl ist ausschließlich Serverarbeit, genau die Frage von M2.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import logging
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

import httpx
from authserver.config import AuthSettings
from authserver.store import AuthStore
from authserver.userdir import UserDirectory
from mcpserver.app import OAuthConfig, create_app
from mcpserver.config import Settings as McpSettings
from storage.acl import add_member, create_space
from storage.store import Store
from webui.config import COOKIE_NAME, UiSettings

logger = logging.getLogger("p10_overview_bench")

HOME_SPACE = "alpha"
TEAM_SPACES = ("bravo", "charlie", "delta")
WRITABLE_TEAM_SPACE = "delta"  # ein Space mit `write:`, damit beide `writable`-Zweige von
# `_overview()` gemessen werden — live ist mindestens ein Team-Space schreibbar (P9-BP).
ITEMS_PER_SPACE = 50  # Plan §4 M2: 4 Spaces × 50 Items
WARMUP_RUNS = 1
MEASURED_RUNS = 5
OVERVIEW_PATH = "/api/v1/overview"


def _synthetic_body(index: int, space: str) -> str:
    """Realistisch langer Text statt `x` * n — dieselbe Begründung wie `ui_budget.py`:
    eine Wiederholung eines Zeichens würde gzip- und Snippet-Kosten schöner rechnen, als sie
    sind, und `Store.search()` liest jede Datei komplett (P6-S), nicht nur den Kopf."""
    return (
        f"## {space.title()} — Notiz {index:03d}\n\n"
        "Kurze Notiz mit ein paar Zeilen Fließtext, wie sie im Alltag entsteht: "
        "Stichpunkte, ein Link, eine Entscheidung mit Begründung.\n\n"
        f"- erster Punkt zu Vorgang {index * 7 % 97}\n"
        f"- zweiter Punkt, nachgerechnet am {index % 28 + 1}. des Monats\n"
        "- dritter Punkt, offen\n\n"
        "Verweis auf das zugehörige Meeting und eine kurze Einschatzung, warum der Weg "
        "so eingeschlagen wurde und nicht der andere.\n"
    )


def _seed(data_root: Path, items_per_space: int) -> Store:
    """4 Spaces × N Items, Bestand über alle fünf `_BUCKETS` verteilt (open/doing/done/note/
    archived) — sonst zählt ein Bucket permanent 0 und die Messung sähe eine Filterkostenstelle
    nicht, die sie im Live-Bestand hat."""
    for name in (HOME_SPACE, *TEAM_SPACES):
        create_space(data_root, name)
    for name in TEAM_SPACES:
        add_member(
            data_root, name, HOME_SPACE, write=(name == WRITABLE_TEAM_SPACE),
        )
    store = Store(data_root, git=False)
    for name in (HOME_SPACE, *TEAM_SPACES):
        for i in range(items_per_space):
            if i % 10 == 9:  # ~10 % archiviert, gemischt über Typen
                item_type, status = ("note", "archived") if i % 20 == 9 else ("task", "archived")
            elif i % 5 == 4:  # ~20 % Aufgaben-Rest, über open/doing/done laufend
                item_type = "task"
                status = ("open", "doing", "done")[i % 3]
            else:
                item_type, status = "note", "active"
            store.create(
                name,
                type=item_type,
                status=status,
                title=f"{name.title()} Item {i:03d} mit einem realistisch langen Titel",
                body=_synthetic_body(i, name),
                tags=["bench", f"gruppe-{i % 8}"],
            )
    return store


def _build_app(data_root: Path, store: Store) -> tuple[object, str]:
    """Volle `create_app()`-Verdrahtung + direkt gemintete UI-Session (kein Einladungs-/Login-
    Umweg — dieselbe Abwägung wie `ui_budget.py :: _measure_latency()`: `create_session()`
    braucht keine `users`-Zeile, reine Lesemessung)."""
    auth_settings = AuthSettings(
        base_url="https://p10-bench.local", db_path=data_root / "_bench_auth.sqlite3"
    )
    auth_store = AuthStore(auth_settings.db_path, now_fn=lambda: datetime.now(timezone.utc))
    oauth = OAuthConfig(
        settings=auth_settings,
        store=auth_store,
        users=UserDirectory(auth_store, dek=None),
    )
    app = create_app(
        settings=McpSettings(data_root=data_root), store=store, oauth=oauth,
    )
    ui_settings = UiSettings(base_url=auth_settings.base_url)
    session_id, _csrf = auth_store.create_session(
        space=HOME_SPACE, idle_ttl_s=ui_settings.idle_ttl_s,
        absolute_ttl_s=ui_settings.absolute_ttl_s,
    )
    return app, session_id


async def _measure(data_root: Path, *, items_per_space: int = ITEMS_PER_SPACE) -> dict:
    store = _seed(data_root, items_per_space)
    assert sum(store.list_spaces()[i].item_count for i in range(4)) == 4 * items_per_space
    app, session_id = _build_app(data_root, store)

    runs_ms: list[float] = []
    response_bytes = 0
    spaces_seen = 0

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="https://p10-bench.local",
        cookies={COOKIE_NAME: session_id},
    ) as client:
        async with app.router.lifespan_context(app):
            for run in range(WARMUP_RUNS + MEASURED_RUNS):
                start = time.perf_counter()
                response = await client.get(OVERVIEW_PATH)
                ms = (time.perf_counter() - start) * 1000
                assert response.status_code == 200, response.status_code
                payload = response.json()
                assert isinstance(payload, list) and len(payload) == 4, (
                    f"Principal sieht {len(payload)} Space(s) statt 4 — Share-Setup kaputt, "
                    "Messung ware still das alte Ein-Space-Bild (PF-2)."
                )
                if run >= WARMUP_RUNS:
                    runs_ms.append(ms)
                    response_bytes = len(response.content)
                    spaces_seen = len(payload)

    runs_sorted = sorted(runs_ms)
    median = runs_sorted[len(runs_sorted) // 2]
    return {
        "probe": "p10_overview_bench",
        "path": OVERVIEW_PATH,
        "spaces": [HOME_SPACE, *TEAM_SPACES],
        "items_per_space": items_per_space,
        "items_total": 4 * items_per_space,
        "spaces_seen": spaces_seen,
        "warmup_runs": WARMUP_RUNS,
        "measured_runs": MEASURED_RUNS,
        "runs_ms": [round(ms, 1) for ms in runs_ms],
        "median_ms": round(median, 1),
        "min_ms": round(min(runs_ms), 1),
        "max_ms": round(max(runs_ms), 1),
        "spread_pct": round((max(runs_ms) - min(runs_ms)) / median * 100, 1),
        "response_bytes": response_bytes,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--json", action="store_true", help="(Default) Ergebnis als JSON auf stdout")
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.INFO, stream=sys.stderr, format="%(levelname)s %(name)s: %(message)s"
    )

    with tempfile.TemporaryDirectory(prefix="sharefyx-p10-bench-") as tmp:
        result = asyncio.run(_measure(Path(tmp)))
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
