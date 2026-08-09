#!/usr/bin/env python3
"""ui_budget.py — misst die vier Größen aus Plan §5 Step 8 / P5-AD gegen eine **temporäre**
Instanz mit synthetischem Bestand (≥ 200 Items). Nie gegen den echten `DATA_ROOT`, nie gegen
einen laufenden Dienst: gebaut wie `ui_smoke.py`, in-process über `httpx.ASGITransport`, kein
Port, kein Netz.

**Warum messen statt schätzen (P5-AD):** `[VERIFY]` V10 stand seit P1 offen als „die Nutzlast
sollte klein genug sein". Eine Zahl, die niemand gemessen hat, ist eine Meinung. Dieses Skript
liefert vier Zahlen, und der Phase-Head trägt sie ein — **auch wenn sie den Zielkorridor
reißen.** Eine Überschreitung wird dokumentiert und bekommt einen Befund, nicht einen
nachträglich großzügiger gefassten Korridor.

Die vier Korridore (Plan §5 Step 8):

| Messgröße                                   | Ziel                    |
|---------------------------------------------|-------------------------|
| `GET /api/v1/items?limit=50` roh / gzip      | < 64 KB / < 12 KB       |
| `GET /api/v1/items/{id}` typisch             | < 8 KB                  |
| `app.js` + `app.css` + Font, gzip            | < 250 KB gesamt         |
| Erstaufruf `/ui/` bis interaktiv, Bytes ges. | < 400 KB                |

„Bis interaktiv" heißt hier konkret: alles, was ein frischer Browser laden muss, bevor die Shell
etwas anzeigen kann — `app.html` + `app.css` + `app.js` + Font (gzip, statische Dateien) plus die
drei Bootstrap-Antworten `/api/v1/{me,meta,overview}`, die `app.js :: init()` in genau dieser
Reihenfolge holt. Das ist eine Nachbildung, kein Browser-Messwert: Verbindungsaufbau,
TLS-Handshake und HTTP-Header sind nicht enthalten. Der Phase-Head sagt das dazu, damit die Zahl
nicht als etwas gelesen wird, das sie nicht ist.

**P6 Step 2 (P6-I/P6-S) — Latenzmessung, getrennt von den vier Größen-`Metric`s oben:**
`_measure_latency()` misst `search_items`/`get_item` (echter `mcpserver.app :: create_app()`,
gleicher `fastmcp.Client`/`StreamableHttpTransport`-Stack wie `phase2_mcp/scripts/
mcp_smoke.py`) und `GET /api/v1/overview`. **Eigene `LatencyMetric`-Dataclass, ohne `budget_bytes`/
`ok`** — würde Millisekunden in `Metric` gepresst, wäre `main()`s Exit-Code plötzlich
zeitabhängig, und der ist ein live-verifiziertes Abnahme-Artefakt (P5 Zeile 15, Nikinger
2026-08-07): eine ausgelastete VM dürfte einen bestehenden grünen Lauf nicht rot färben, für eine
Messung, die laut P6-I/P6-S ohnehin nur Zahlen für die nächste Entscheidung liefern soll, kein
Budget ist. Läuft NACH `_measure()`, gegen denselben `data_root` (die dort gesäten 220 Items
werden wiederverwendet — Hard Rule 2: ein frischer `Store` rekonstruiert seinen Index immer aus
den Dateien, kein erneutes Seeding nötig), aber mit einer eigenen `AuthStore`-Datei je Fläche
(MCP-Bearer-Token, UI-Session) statt `_measure()`s Auth-Zustand mitzubenutzen — hält beide
Messungen unabhängig voneinander nachvollziehbar. **Jede der drei Messungen macht einen
verworfenen Aufwärmlauf vor dem gemessenen Aufruf** (Advisor-Fund): ein einzelner kalter Aufruf
gegen eine gerade erst gebaute App/Verbindung trägt Routen-Setup, ersten Import bzw. (bei den
MCP-Tools) die Session-Verhandlung mit — genau die Frage, die P6-I/P6-S beantworten sollen
(„ist die Werkzeug-/API-Fläche selbst zu langsam"), würde sonst mit einer Frage beantwortet, die
niemand gestellt hat („wie lange dauert ein Kaltstart").

Ausgabe: Text (Standard) oder `--json` auf stdout; Logs auf stderr (Hard Rule 7).
"""
from __future__ import annotations

import argparse
import asyncio
import gzip
import json
import logging
import re
import sys
import tempfile
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

import httpx
from authserver.config import AuthSettings
from authserver.store import AuthStore
from authserver.userdir import UserDirectory
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport
from mcpserver.app import OAuthConfig, create_app
from mcpserver.config import Settings as McpSettings
from mcpserver.permissions import OwnSpaceWritable
from starlette.applications import Starlette
from storage.store import Store

from webui.account import account_routes
from webui.api import api_routes
from webui.config import COOKIE_NAME, DEFAULT_STATIC_DIR, UiSettings
from webui.routes_auth import ui_auth_routes
from webui.sessions import SessionManager
from webui.static_routes import static_routes

logger = logging.getLogger("ui_budget")

SPACE = "alpha"
PASSWORD = "correct horse battery staple budget"
ITEM_COUNT = 220          # Plan verlangt ≥ 200
KB = 1024

EXIT_OK = 0
EXIT_OVER_BUDGET = 1

_CSRF_RE = re.compile(r'name="csrf" value="([^"]+)"')


@dataclass
class Metric:
    name: str
    value_bytes: int
    budget_bytes: int
    detail: str

    @property
    def ok(self) -> bool:
        return self.value_bytes < self.budget_bytes


@dataclass
class LatencyMetric:
    """P6 Step 2 (P6-I/P6-S) — bewusst kein `budget_bytes`/`ok`, siehe Moduldocstring: eine
    Zeitmessung ist hier informativ, kein Gate."""
    name: str
    ms: float
    response_bytes: int
    detail: str


def _kb(value: int) -> str:
    return f"{value / KB:.1f} KB"


def _gz(payload: bytes) -> int:
    """gzip-Größe wie ein Server sie ausliefern würde. `mtime=0`, damit derselbe Inhalt immer
    dieselbe Zahl ergibt — sonst wäre die Messung nicht wiederholbar."""
    return len(gzip.compress(payload, compresslevel=9, mtime=0))


def _client_factory(app: Starlette) -> httpx.AsyncClient:
    return httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="https://ui-budget.local"
    )


def _synthetic_body(index: int) -> str:
    """Ein realistisch langer Notiztext, nicht 'x' * n: die Messung soll etwas über echte Inhalte
    aussagen, und gzip komprimiert eine Wiederholung eines einzelnen Zeichens fast auf null —
    eine Attrappe würde die gzip-Zahl schöner machen als sie ist."""
    return (
        f"## Abschnitt {index}\n\n"
        "Kurze Notiz mit ein paar Zeilen Fließtext, wie sie im Alltag entsteht — "
        "Stichpunkte, ein Link, etwas Struktur.\n\n"
        "- erster Punkt\n- zweiter Punkt\n- dritter Punkt\n\n"
        f"Verweis auf Vorgang {index * 7 % 97} und eine kurze Begründung, warum das so "
        "entschieden wurde.\n"
    )


async def _measure(data_root: Path) -> list[Metric]:
    auth_settings = AuthSettings(
        base_url="https://ui-budget.local", db_path=data_root / "_budget_auth.sqlite3"
    )
    auth_store = AuthStore(auth_settings.db_path, now_fn=lambda: datetime.now(timezone.utc))
    users = UserDirectory(auth_store, dek=bytes([0x5A]) * 32)
    ui_settings = UiSettings(base_url=auth_settings.base_url)
    sessions = SessionManager(auth_store, settings=ui_settings)

    # git=False: die Messung interessiert die Nutzlast, nicht die Commit-Dauer — und ein
    # Git-Commit je Item bei 220 Items würde den Lauf ohne Erkenntnisgewinn strecken.
    item_store = Store(data_root, git=False)
    logger.info("lege %d synthetische Items an", ITEM_COUNT)
    for i in range(ITEM_COUNT):
        item_store.create(
            SPACE,
            type="note" if i % 3 else "task",
            title=f"Synthetisches Item {i:03d} mit einem realistisch langen Titel",
            body=_synthetic_body(i),
            tags=["mess", f"gruppe-{i % 8}"],
        )

    routes = (
        ui_auth_routes(ui_settings, auth_store, users, sessions)
        + account_routes(ui_settings, auth_store, users, sessions)
        + api_routes(ui_settings, item_store, sessions, OwnSpaceWritable(), auth_store)
        + static_routes(ui_settings, sessions)
    )
    app = Starlette(routes=routes)

    from authserver import totp as totp_module

    invite_token = auth_store.create_invite(space=SPACE, purpose="initial", ttl_s=3600)
    metrics: list[Metric] = []

    async with _client_factory(app) as client:
        invite = await client.post(f"/ui/invite/{invite_token}", data={"password": PASSWORD})
        secret = re.search(
            r'<code class="auth__seed">([A-Z2-7 ]+)</code>', invite.text
        ).group(1).replace(" ", "")
        enroll_csrf = _CSRF_RE.search(invite.text).group(1)
        code = totp_module.totp_at(
            secret, int(datetime.now(timezone.utc).timestamp() // 30), algo="SHA1"
        )
        await client.post(
            "/ui/enroll/confirm",
            data={"code": code, "csrf": enroll_csrf},
            headers={"Origin": ui_settings.base_url},
        )
        login = await client.post(
            "/ui/login",
            data={
                "space": SPACE,
                "password": PASSWORD,
                "totp": totp_module.totp_at(
                    secret, int(datetime.now(timezone.utc).timestamp() // 30), algo="SHA1"
                ),
            },
        )
        assert login.status_code == 200, login.status_code

        # 1) Trefferliste, 50 Zeilen.
        listing = await client.get("/api/v1/items", params={"limit": 50})
        assert listing.status_code == 200, listing.status_code
        raw = listing.content
        metrics.append(Metric(
            "GET /api/v1/items?limit=50 (roh)", len(raw), 64 * KB,
            f"{len(listing.json()['items'])} Zeilen von {listing.json()['total']}",
        ))
        metrics.append(Metric(
            "GET /api/v1/items?limit=50 (gzip)", _gz(raw), 12 * KB, "compresslevel=9",
        ))

        # 2) Ein typisches Einzelitem.
        one_id = listing.json()["items"][0]["id"]
        single = await client.get(f"/api/v1/items/{one_id}")
        assert single.status_code == 200, single.status_code
        metrics.append(Metric(
            "GET /api/v1/items/{id} (typisch)", len(single.content), 8 * KB, one_id,
        ))

        # 3) Statische Nutzlast: app.js + app.css + Font, gzip.
        #    Die Font-Datei wird NICHT noch einmal gzippt gezählt — woff2 ist bereits komprimiert,
        #    ein zweiter Durchlauf macht sie minimal größer, nicht kleiner. Sie zählt roh, genau
        #    wie ein Server sie ausliefert.
        static_total = 0
        static_parts = []
        for name in ("app.js", "app.css"):
            payload = (DEFAULT_STATIC_DIR / name).read_bytes()
            size = _gz(payload)
            static_total += size
            static_parts.append(f"{name} {_kb(size)}")
        fonts = sorted((DEFAULT_STATIC_DIR / "fonts").glob("*.woff2"))
        for font in fonts:
            size = font.stat().st_size
            static_total += size
            static_parts.append(f"{font.name} {_kb(size)} (bereits komprimiert)")
        metrics.append(Metric(
            "app.js + app.css + Font (gzip)", static_total, 250 * KB, ", ".join(static_parts),
        ))

        # 4) Erstaufruf /ui/ bis interaktiv.
        shell = await client.get("/ui/")
        assert shell.status_code == 200, shell.status_code
        first_load = _gz(shell.content) + static_total
        bootstrap_parts = []
        for path in ("/api/v1/me", "/api/v1/meta", "/api/v1/overview"):
            response = await client.get(path)
            assert response.status_code == 200, (path, response.status_code)
            size = _gz(response.content)
            first_load += size
            bootstrap_parts.append(f"{path} {_kb(size)}")
        metrics.append(Metric(
            "Erstaufruf /ui/ bis interaktiv (gesamt)", first_load, 400 * KB,
            "app.html + statische Dateien + " + ", ".join(bootstrap_parts),
        ))

    return metrics


async def _measure_latency(data_root: Path) -> list[LatencyMetric]:
    """P6 Step 2 (P6-I/P6-S) — siehe Moduldocstring für die Begründung, warum das eine eigene
    Funktion mit eigener Dataclass ist, kein Umbau von `_measure()`. Läuft gegen denselben
    `data_root`, den `_measure()` bereits mit 220 Items gefüllt hat, mit eigenen, unabhängigen
    `AuthStore`-Dateien für die MCP- und die REST-Fläche."""
    item_store = Store(data_root, git=False)

    latency: list[LatencyMetric] = []

    # -- MCP-Tool-Fläche: search_items, get_item — echter mcpserver.app::create_app(), gleicher
    #    Client/Transport-Stack wie phase2_mcp/scripts/mcp_smoke.py (bewusst dieselbe, bereits
    #    live-verifizierte Verdrahtung, kein Nachbau).
    mcp_auth_settings = AuthSettings(
        base_url="https://ui-budget.local", db_path=data_root / "_budget_mcp_auth.sqlite3"
    )
    mcp_auth_store = AuthStore(mcp_auth_settings.db_path, now_fn=lambda: datetime.now(timezone.utc))
    family_id = mcp_auth_store.create_family(
        space=SPACE, client_id="ui_budget", scope="space", resource=mcp_auth_settings.resource
    )
    access_token, _refresh = mcp_auth_store.issue_token_pair(
        family_id, access_ttl_s=3600, refresh_ttl_s=2_592_000
    )
    mcp_oauth = OAuthConfig(
        settings=mcp_auth_settings, store=mcp_auth_store,
        users=UserDirectory(mcp_auth_store, dek=None),
    )
    mcp_app = create_app(settings=McpSettings(data_root=data_root), store=item_store, oauth=mcp_oauth)

    def _mcp_client_factory(app: object) -> object:
        transport = httpx.ASGITransport(app=app)

        def factory(**kwargs: object) -> httpx.AsyncClient:
            return httpx.AsyncClient(
                transport=transport, base_url="https://ui-budget.local", **kwargs
            )

        return factory

    mcp_transport = StreamableHttpTransport(
        url="https://ui-budget.local/mcp/",
        headers={"Authorization": f"Bearer {access_token}"},
        httpx_client_factory=_mcp_client_factory(mcp_app),
    )

    async with mcp_app.router.lifespan_context(mcp_app):
        async with Client(mcp_transport) as mcp_client:
            # Aufwärmlauf, siehe Docstring — verworfen. Der erste Aufruf über einen frischen
            # `Client` trägt die MCP-Session-Verhandlung (`initialize` + `ListTools`, im
            # Server-Log als eigene Requests sichtbar) mit, kein realistischer Wert für "wie
            # schnell ist DIESES Tool", sondern nur "wie schnell ist eine kalte Verbindung".
            await mcp_client.call_tool("search_items", {"limit": 1})
            start = time.perf_counter()
            search_result = await mcp_client.call_tool("search_items", {"limit": 50})
            ms = (time.perf_counter() - start) * 1000
            search_payload = json.loads(search_result.data)
            latency.append(LatencyMetric(
                "search_items (MCP, limit=50)", ms, len(search_result.data.encode("utf-8")),
                f"{len(search_payload['items'])} von {search_payload['total']} Treffern",
            ))

            item_id = search_payload["items"][0]["id"]
            start = time.perf_counter()
            get_result = await mcp_client.call_tool("get_item", {"item_id": item_id})
            ms = (time.perf_counter() - start) * 1000
            latency.append(LatencyMetric(
                "get_item (MCP)", ms, len(get_result.data.encode("utf-8")), item_id,
            ))

    # -- REST-Fläche: GET /api/v1/overview — Session-Cookie direkt gemintet (`create_session()`
    #    braucht keine `users`-Zeile, `authserver/store.py:961-983`), kein Einladung/Enrollment/
    #    Login-Umweg nötig für eine reine Lesemessung.
    ui_auth_settings = AuthSettings(
        base_url="https://ui-budget.local", db_path=data_root / "_budget_ui_auth.sqlite3"
    )
    ui_auth_store = AuthStore(ui_auth_settings.db_path, now_fn=lambda: datetime.now(timezone.utc))
    ui_settings = UiSettings(base_url=ui_auth_settings.base_url)
    session_id, _csrf = ui_auth_store.create_session(
        space=SPACE, idle_ttl_s=ui_settings.idle_ttl_s, absolute_ttl_s=ui_settings.absolute_ttl_s,
    )
    sessions = SessionManager(ui_auth_store, settings=ui_settings)
    rest_app = Starlette(
        routes=api_routes(ui_settings, item_store, sessions, OwnSpaceWritable(), ui_auth_store)
    )

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=rest_app), base_url="https://ui-budget.local",
        cookies={COOKIE_NAME: session_id},
    ) as client:
        await client.get("/api/v1/overview")  # Aufwärmlauf, siehe Docstring — verworfen
        start = time.perf_counter()
        overview = await client.get("/api/v1/overview")
        ms = (time.perf_counter() - start) * 1000
        assert overview.status_code == 200, overview.status_code
        latency.append(LatencyMetric(
            "GET /api/v1/overview", ms, len(overview.content), "",
        ))

    return latency


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--json", action="store_true", help="Ergebnis als JSON auf stdout")
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.INFO, stream=sys.stderr, format="%(levelname)s %(name)s: %(message)s"
    )

    with tempfile.TemporaryDirectory(prefix="sharefyx-budget-") as tmp:
        metrics = asyncio.run(_measure(Path(tmp)))
        latency = asyncio.run(_measure_latency(Path(tmp)))

    if args.json:
        print(json.dumps(
            {"metrics": [asdict(m) | {"ok": m.ok} for m in metrics],
             "all_within_budget": all(m.ok for m in metrics),
             "latency": [asdict(m) for m in latency]},
            ensure_ascii=False,
        ))
    else:
        print("Sharefyx UI — Messung (P5-AD)\n")
        for metric in metrics:
            mark = "OK  " if metric.ok else "ÜBER"
            print(
                f"[{mark}] {metric.name:<44} {_kb(metric.value_bytes):>10}"
                f"  (Ziel < {_kb(metric.budget_bytes)})"
            )
            print(f"         {metric.detail}")
        over = [m for m in metrics if not m.ok]
        print()
        if over:
            # Kein stilles Anheben des Korridors: eine Überschreitung ist ein Befund für den
            # Phase-Head (P5-AD, „Messung statt Schätzung").
            print(f"{len(over)} von {len(metrics)} Messgrößen ÜBER dem Zielkorridor.")
        else:
            print(f"Alle {len(metrics)} Messgrößen im Zielkorridor.")

        # P6 Step 2 (P6-I/P6-S): rein informativ, siehe Moduldocstring — kein Einfluss auf den
        # Exit-Code unten, der bewusst ausschließlich von `metrics` abhängt.
        print("\nLatenz- und Größenmessung Werkzeug-/API-Fläche (P6-I/P6-S, informativ):\n")
        for m in latency:
            print(f"[INFO] {m.name:<32} {m.ms:>8.1f} ms   {_kb(m.response_bytes):>10}")
            if m.detail:
                print(f"         {m.detail}")

    return EXIT_OK if all(m.ok for m in metrics) else EXIT_OVER_BUDGET


if __name__ == "__main__":
    sys.exit(main())
