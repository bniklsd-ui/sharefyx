#!/usr/bin/env python3
"""ui_smoke.py — Gegenstück zu `mcp_smoke.py`/`oauth_smoke.py` (Plan §5 Step 5 Done-when). Baut
ein **temporäres** `DATA_ROOT` und eine **temporäre** `AuthStore` (nie das echte), mountet
`ui_auth_routes()` + `account_routes()` + `api_routes()` in-process (kein echter Port, kein Netz
— `httpx.ASGITransport`) und fährt einen vollständigen Web-UI-Durchlauf: Einladung einlösen,
TOTP einrichten, einloggen, `/api/v1/me`+`/spaces` lesen, ein Item anlegen/lesen/ändern/
anhängen/archivieren, einen Versionskonflikt auslösen, einen fremden Space nur lesend sehen.

Bewusst **ohne** `--base-url`-Option (anders als `oauth_smoke.py`) — Step 5s Done-when verlangt
nur den In-Process-Lauf; ein Live-Modus gegen einen echten Prozess ist erst mit einem
Live-Abnahme-Runbook sinnvoll (siehe `docs/concepts/phase5_ui_plan.md` §5 Step 9), kein Bedarf,
der heute schon besteht.

Ausgabe: Text (Standard) oder `--json` auf stdout; Logs auf stderr (Hard Rule 7).
"""
from __future__ import annotations

import argparse
import asyncio
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
from webui.config import UiSettings
from webui.routes_auth import ui_auth_routes
from webui.sessions import SessionManager

logger = logging.getLogger("ui_smoke")

# Fixture-Namen, keine Nikinger-typischen Spacenamen (gleiche Disziplin wie `mcp_smoke.py`).
SPACE_OWN = "alpha"
SPACE_FOREIGN = "beta"
PASSWORD = "correct horse battery staple smoke"

EXIT_OK = 0
EXIT_FAILED = 1

_CSRF_RE = re.compile(r'name="csrf" value="([^"]+)"')


@dataclass
class Check:
    name: str
    ok: bool
    detail: str


def _client_factory(app: Starlette) -> httpx.AsyncClient:
    return httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="https://ui-smoke.local"
    )


async def _run(data_root: Path, checks: list[Check]) -> None:
    auth_settings = AuthSettings(
        base_url="https://ui-smoke.local", db_path=data_root / "_smoke_auth.sqlite3"
    )
    auth_store = AuthStore(auth_settings.db_path, now_fn=lambda: datetime.now(timezone.utc))
    users = UserDirectory(auth_store, dek=bytes([0x5A]) * 32)
    ui_settings = UiSettings(base_url=auth_settings.base_url)
    sessions = SessionManager(auth_store, settings=ui_settings)

    item_store = Store(data_root, git=False)
    # Wie `mcp_smoke.py`: ohne einen Seed-Eintrag wäre der fremde Space beim ersten
    # `/api/v1/spaces`-Aufruf unsichtbar (`Store.list_spaces()` leitet Spaces ausschließlich aus
    # vorhandenen Items ab, keine separate Registry).
    item_store.create(SPACE_FOREIGN, type="note", title="Fremde Notiz", body="Fremder Inhalt.")

    routes = (
        ui_auth_routes(ui_settings, auth_store, users, sessions)
        + account_routes(ui_settings, auth_store, users, sessions)
        + api_routes(ui_settings, item_store, sessions, OwnSpaceWritable(), auth_store)
    )
    app = Starlette(routes=routes)

    invite_token = auth_store.create_invite(space=SPACE_OWN, purpose="initial", ttl_s=3600)

    async with _client_factory(app) as client:
        # 1. Einladung einlösen -> Passwort gesetzt, Enrollment-Seite mit Secret+CSRF.
        invite_response = await client.post(
            f"/ui/invite/{invite_token}", data={"password": PASSWORD},
        )
        # [2026-08-05, Step 7b] `pages.py` hat Klassen-Markup bekommen; der Seed steht seither in
        # `<code class="auth__seed">` (siehe dieselbe Anpassung in `tests/test_invite_enroll.py`).
        secret_match = re.search(
            r'<code class="auth__seed">([A-Z2-7 ]+)</code>', invite_response.text
        )
        enroll_csrf = _CSRF_RE.search(invite_response.text)
        secret = secret_match.group(1).replace(" ", "") if secret_match else None
        checks.append(
            Check(
                "invite -> Konto aktiv",
                invite_response.status_code == 200 and secret is not None and enroll_csrf is not None,
                f"status={invite_response.status_code}, secret_gefunden={secret is not None}",
            )
        )

        # 2. TOTP bestätigen -> Recovery-Codes-Seite.
        from authserver import totp as totp_module

        code = totp_module.totp_at(
            secret, int(datetime.now(timezone.utc).timestamp() // 30), algo="SHA1"
        )
        confirm_response = await client.post(
            "/ui/enroll/confirm",
            data={"code": code, "csrf": enroll_csrf.group(1)},
            headers={"Origin": auth_settings.base_url},
        )
        checks.append(
            Check(
                "TOTP-Enrollment bestätigt",
                confirm_response.status_code == 200 and "Recovery" in confirm_response.text,
                f"status={confirm_response.status_code}",
            )
        )

        # 3. Neu einloggen (die Enrollment-Sitzung reicht, aber ein echter Login-Roundtrip
        #    beweist mehr: Passwort + frischer TOTP-Code, nicht nur die bestehende Sitzung).
        login_response = await client.post(
            "/ui/login", data={"space": SPACE_OWN, "password": PASSWORD, "totp": code},
        )
        login_csrf = _CSRF_RE.search(login_response.text)
        checks.append(
            Check(
                "Login (Passwort + TOTP)",
                login_response.status_code == 200 and login_csrf is not None,
                f"status={login_response.status_code}",
            )
        )
        csrf = login_csrf.group(1)
        headers = {"Origin": auth_settings.base_url, "X-CSRF-Token": csrf}

        # 4. /api/v1/me, /api/v1/spaces.
        me = await client.get("/api/v1/me")
        checks.append(
            Check("/api/v1/me", me.status_code == 200 and me.json()["space"] == SPACE_OWN, me.text)
        )

        spaces = await client.get("/api/v1/spaces")
        by_name = {s["name"]: s for s in spaces.json()} if spaces.status_code == 200 else {}
        checks.append(
            Check(
                "/api/v1/spaces (eigen vs. fremd)",
                by_name.get(SPACE_OWN, {}).get("own") is True
                and by_name.get(SPACE_FOREIGN, {}).get("own") is False,
                f"spaces={sorted(by_name)}",
            )
        )

        # 5. Item anlegen, lesen, ändern, anhängen, archivieren.
        created = await client.post(
            "/api/v1/items", json={"type": "task", "title": "Smoke-Item"}, headers=headers,
        )
        item_id = created.json().get("id") if created.status_code == 201 else None
        checks.append(
            Check("POST /api/v1/items", created.status_code == 201 and item_id is not None, created.text)
        )

        read_own = await client.get(f"/api/v1/items/{item_id}")
        checks.append(
            Check(
                "GET /api/v1/items/{id} (eigen)",
                read_own.status_code == 200 and read_own.json()["readonly"] is False,
                read_own.text,
            )
        )

        patched = await client.patch(
            f"/api/v1/items/{item_id}", json={"version": 1, "title": "Smoke-Item geändert"},
            headers=headers,
        )
        checks.append(
            Check(
                "PATCH /api/v1/items/{id}",
                patched.status_code == 200 and patched.json()["title"] == "Smoke-Item geändert",
                patched.text,
            )
        )

        conflict = await client.patch(
            f"/api/v1/items/{item_id}", json={"version": 1, "title": "Sollte scheitern"},
            headers=headers,
        )
        checks.append(
            Check(
                "PATCH /api/v1/items/{id} (Versionskonflikt)",
                conflict.status_code == 409 and "current" in conflict.json().get("detail", {}),
                f"status={conflict.status_code}",
            )
        )

        appended = await client.post(
            f"/api/v1/items/{item_id}/append", json={"version": 2, "text": "Angehängt."},
            headers=headers,
        )
        checks.append(
            Check(
                "POST /api/v1/items/{id}/append",
                appended.status_code == 200 and "Angehängt." in appended.json().get("body", ""),
                appended.text,
            )
        )

        archived = await client.post(
            f"/api/v1/items/{item_id}/archive", json={"version": 3}, headers=headers,
        )
        checks.append(
            Check(
                "POST /api/v1/items/{id}/archive",
                archived.status_code == 200 and archived.json().get("status") == "archived",
                archived.text,
            )
        )

        # 6. Fremder Space: sichtbar, readonly.
        foreign_search = await client.get("/api/v1/items", params={"space": SPACE_FOREIGN})
        foreign_items = foreign_search.json().get("items", []) if foreign_search.status_code == 200 else []
        checks.append(
            Check(
                "GET /api/v1/items?space=fremd (readonly)",
                len(foreign_items) == 1 and foreign_items[0]["readonly"] is True,
                f"{len(foreign_items)} Treffer",
            )
        )


def _print_report(checks: list[Check]) -> None:
    name_width = max(len(c.name) for c in checks)
    print("Sharefyx UI/API — Smoke-Test\n")
    for c in checks:
        status = "OK  " if c.ok else "FAIL"
        print(f"[{status}] {c.name.ljust(name_width)}  {c.detail}")

    failed = [c for c in checks if not c.ok]
    print()
    if failed:
        print(f"{len(failed)} von {len(checks)} Prüfung(en) fehlgeschlagen.", file=sys.stderr)
    else:
        print(f"Alle {len(checks)} Prüfungen grün.")


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(
        stream=sys.stderr, level=logging.INFO, format="%(levelname)s %(name)s: %(message)s"
    )
    parser = argparse.ArgumentParser(
        prog="ui_smoke",
        description="End-to-End-Smoke-Test der Web-UI/REST-API gegen ein temporäres DATA_ROOT "
        "(nie das echte). Kein echter Port, kein Netz, kein Keyring.",
    )
    parser.add_argument(
        "--json", action="store_true", help="Maschinenlesbare Ausgabe auf stdout statt Text"
    )
    args = parser.parse_args(argv)

    checks: list[Check] = []
    with tempfile.TemporaryDirectory(prefix="ui_smoke_") as tmp:
        logger.info("temporäres DATA_ROOT: %s", tmp)
        asyncio.run(_run(Path(tmp), checks))

    if args.json:
        print(json.dumps([asdict(c) for c in checks], ensure_ascii=False, indent=2))
    else:
        _print_report(checks)

    return EXIT_OK if all(c.ok for c in checks) else EXIT_FAILED


if __name__ == "__main__":
    sys.exit(main())
