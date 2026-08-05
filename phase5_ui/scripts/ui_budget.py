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
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

import httpx
from authserver.config import AuthSettings
from authserver.store import AuthStore
from authserver.userdir import UserDirectory
from mcpserver.permissions import OwnSpaceWritable
from starlette.applications import Starlette
from storage.store import Store

from webui.account import account_routes
from webui.api import api_routes
from webui.config import DEFAULT_STATIC_DIR, UiSettings
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
        + api_routes(ui_settings, item_store, sessions, OwnSpaceWritable())
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--json", action="store_true", help="Ergebnis als JSON auf stdout")
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.INFO, stream=sys.stderr, format="%(levelname)s %(name)s: %(message)s"
    )

    with tempfile.TemporaryDirectory(prefix="sharefyx-budget-") as tmp:
        metrics = asyncio.run(_measure(Path(tmp)))

    if args.json:
        print(json.dumps(
            {"metrics": [asdict(m) | {"ok": m.ok} for m in metrics],
             "all_within_budget": all(m.ok for m in metrics)},
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

    return EXIT_OK if all(m.ok for m in metrics) else EXIT_OVER_BUDGET


if __name__ == "__main__":
    sys.exit(main())
