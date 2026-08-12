#!/usr/bin/env python3
"""mcp_smoke.py — Gegenstück zu `space_cli.py` aus P1 (Plan §4 Step 7). Baut ein **temporäres**
`DATA_ROOT` (nie das echte), zwei Fixture-Spaces, startet `create_app()` in-process (kein
echter Port, kein Netz — `httpx.ASGITransport`, dasselbe Muster wie `test_app.py`) und fährt
die sieben Tools einmal vollständig durch: `list_spaces`, `create_item` ×3, `search_items`,
`get_item` eigen/fremd, ein `update_item`-Konflikt, `append_to_item`, `patch_item`,
`update_item(status=archived)`, ein `update_item` auf einen fremden Space. Am Ende eine
Größenmessung (Bytes je Antwort) als Tabelle.

**P6 Step 1:** `create_item`/`append_to_item`/`update_item`/`patch_item` liefern seither per
Default eine Quittung statt Dateitext (P6-H) — die betroffenen Prüfungen unten lesen die
Quittungsfelder direkt, keine Frontmatter-Regex mehr auf diesen vier Antworten. Der ambiguous-
old_text-Fehlversuch von `patch_item` ist bewusst nicht hier, sondern Teil der Live-Abnahme
(Gate A→B #1) — dieses Skript beweist den Erfolgspfad, kein zweiter Fehlerpfad-Katalog neben
`test_tools.py`.

**Schnitt, 2026-07-30 (Runbook-Schritt 8):** `create_app()` verlangt seither immer ein
`OAuthConfig` (`TokenPathASGI`/`AuthModeASGI` sind entfernt) — die beiden Fixture-Tokens hier
entstehen deshalb nicht mehr über `credentials.generate_token()`/einen `KeyringTokenResolver`,
sondern als echte, opake OAuth-Access-Token direkt gegen eine **temporäre** `AuthStore`
(`create_family()` + `issue_token_pair()`, dasselbe Muster wie in `test_asgi_bearer.py`) — kein
Login-Flow nötig, kein echter Keyring, keine echten Nutzerakten. `SPACE_PUBLIC_BASE_URL` ist ein
Platzhalter (`https://smoke.local`), er wird nie kontaktiert.

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
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

from authserver.config import AuthSettings
from authserver.store import AuthStore
from authserver.userdir import UserDirectory

from mcpserver.app import OAuthConfig, create_app
from mcpserver.config import Settings
from storage.store import Store

logger = logging.getLogger("mcp_smoke")

# Fixture-Namen, keine Nikinger-typischen Spacenamen (Plan §2.2 Erweiterungspfad).
SPACE_OWN = "alpha"
SPACE_FOREIGN = "beta"

EXIT_OK = 0
EXIT_FAILED = 1


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    response_bytes: int | None = None


def _issue_smoke_token(auth_store: AuthStore, *, space: str, resource: str) -> str:
    family_id = auth_store.create_family(
        space=space, client_id="mcp_smoke", scope="space", resource=resource
    )
    access_token, _refresh_token = auth_store.issue_token_pair(
        family_id, access_ttl_s=3600, refresh_ttl_s=2592000
    )
    return access_token


def _client_factory(app):
    transport = httpx.ASGITransport(app=app)

    def factory(**kwargs) -> httpx.AsyncClient:
        return httpx.AsyncClient(transport=transport, base_url="http://smoke.local", **kwargs)

    return factory


def _mcp_client(app, token: str) -> Client:
    transport = StreamableHttpTransport(
        url="http://smoke.local/mcp/",
        headers={"Authorization": f"Bearer {token}"},
        httpx_client_factory=_client_factory(app),
    )
    return Client(transport)


def _extract_field(filetext: str, field: str) -> str | None:
    """Liest einen Frontmatter-Wert (`id: itm_...`, `version: 2`, …) aus dem von den Tools
    zurückgegebenen Dateitext — kein YAML-Parser nötig für ein Smoke-Skript, das nur wenige
    bekannte Felder ausliest. Sucht über den gesamten Dateitext (Frontmatter + Body), nicht nur
    den Frontmatter-Block: sicher, weil `re.search` den ERSTEN Treffer nimmt und das Frontmatter
    immer vor dem Body steht — ein Body mit einer zufällig gleichlautenden Zeile (z. B. eine
    Notiz über "version: 2") würde sonst mit einer strikteren Grenze verwechselt, hier aber
    nie gewinnen, weil das Frontmatter-Feld immer zuerst auftaucht."""
    match = re.search(rf"^{field}: (.+)$", filetext, re.MULTILINE)
    return match.group(1).strip() if match else None


async def _run(data_root: Path, checks: list[Check]) -> None:
    # Zwei Token (auch wenn dieses Skript nur mit dem eigenen verbindet) — bewiesen bereits in
    # test_app.py über echte parallele Requests; hier geht es um den Tool-Ablauf aus EINER
    # Principal-Sicht (own), gegen einen Space, der ihr selbst gehört (alpha) und einen, der es
    # nicht tut (beta).
    auth_settings = AuthSettings(
        base_url="https://smoke.local", db_path=data_root / "_smoke_auth.sqlite3"
    )
    auth_store = AuthStore(auth_settings.db_path, now_fn=lambda: datetime.now(timezone.utc))
    own_token = _issue_smoke_token(auth_store, space=SPACE_OWN, resource=auth_settings.resource)
    _issue_smoke_token(auth_store, space=SPACE_FOREIGN, resource=auth_settings.resource)

    store = Store(data_root, git=False)
    # `Store.list_spaces()` leitet Spaces ausschließlich aus vorhandenen Items ab (P1, keine
    # separate Space-Registry) — ohne diesen Seed-Eintrag wäre `alpha` beim ersten `list_spaces`-
    # Aufruf (Schritt 1, vor jedem `create_item`) unsichtbar, weil noch leer.
    store.create(SPACE_OWN, type="note", title="Ausgangspunkt", body="Anfangszustand.")
    store.create(SPACE_FOREIGN, type="note", title="Fremde Notiz", body="Fremder Inhalt.")
    # P6 Step 5: ohne Freigabe wäre `SPACE_FOREIGN` für `SPACE_OWN` seit P6-U unsichtbar
    # (`test_foreign_space_is_invisible_without_share`) — dieses Skript demonstriert
    # ausdrücklich den Lese-Pfad in einen fremden, geteilten Space (Schritte 1 und 4 unten),
    # deshalb hier bewusst geteilt, nicht ungeteilt gelassen.
    (data_root / SPACE_FOREIGN / ".share.yml").write_text(f"read: [{SPACE_OWN}]\n", encoding="utf-8")
    # Auffüllen auf eine echte Default-Listing-Größe (§5 Kriterium 5: 20 Items < 12 KB) — ohne
    # das würde die Größenmessung für `search_items` nur 5 Treffer zeigen und die eigentliche
    # Frage ("hält das Token-Budget bei einem vollen Default-Listing") gar nicht beantworten
    # (Advisor-Review, Step 7). Realistische Body-Länge wie in
    # `test_tools.py::test_search_result_size_budget` — ein leerer Body macht jedes Snippet
    # trivial und würde die Messung schönen. Vor `create_item` #1–3, damit diese (als jüngste
    # Items) sicher im ersten 20er-Fenster landen, nicht die Füll-Items selbst.
    filler_body = (
        "Realistischer Notizinhalt für die Größenmessung, lang genug für ein volles "
        "160-Zeichen-Snippet statt eines trivialen leeren Bodys. " * 2
    )
    for i in range(17):
        store.create(SPACE_OWN, type="note", title=f"Füll-Item {i + 1}", body=filler_body)

    settings = Settings(data_root=data_root)
    oauth = OAuthConfig(
        settings=auth_settings, store=auth_store, users=UserDirectory(auth_store, dek=None)
    )
    app = create_app(settings=settings, store=store, oauth=oauth)

    async with app.router.lifespan_context(app):
        async with _mcp_client(app, own_token) as own:
            # 1. list_spaces — beide Spaces sichtbar, genau einer writable.
            spaces_text = (await own.call_tool("list_spaces", {})).data
            spaces = json.loads(spaces_text)
            by_name = {s["name"]: s for s in spaces}
            writable = [s["name"] for s in spaces if s["writable"]]
            checks.append(
                Check(
                    "list_spaces",
                    set(by_name) == {SPACE_OWN, SPACE_FOREIGN} and writable == [SPACE_OWN],
                    f"Spaces={sorted(by_name)}, writable={writable}",
                    len(spaces_text.encode("utf-8")),
                )
            )

            # 2. create_item x3 im eigenen Space. Seit P6 Step 1 liefert create_item per Default
            # eine Quittung (JSON), keinen Dateitext mehr (P6-H) — _extract_field() (Frontmatter-
            # Regex) passt hier nicht mehr, die Prüfung liest die Quittungsfelder direkt.
            created_ids: list[str] = []
            for i in range(3):
                text = (
                    await own.call_tool(
                        "create_item", {"type": "task", "title": f"Smoke-Item {i + 1}"}
                    )
                ).data
                receipt = json.loads(text)
                item_id = receipt.get("id")
                if item_id:
                    created_ids.append(item_id)
                checks.append(
                    Check(
                        f"create_item #{i + 1}",
                        item_id is not None
                        and receipt.get("space") == SPACE_OWN
                        and receipt.get("op") == "create",
                        item_id or "keine id in der Quittung gefunden",
                        len(text.encode("utf-8")),
                    )
                )

            # 3. search_items — Default-Limit, keine archivierten, Größenmessung.
            # Bewusst OHNE Prüfung "sind die drei create_item-Treffer in dieser Seite" — bei
            # 20+ Items im Space sortiert Store.search() nach Aktualität, und dieses Skript
            # legt alle Items in einer engen Schleife über die reale Systemuhr an (kein
            # injizierter now_fn wie in den Unit-Tests). Auf einer schnellen VM können mehrere
            # Items denselben `updated`-Zeitstempel bekommen; unter dieser Bindung entscheidet
            # die stabile Sortierung über die Indexreihenfolge, nicht über die Anlegereihenfolge
            # — das drückte gelegentlich eines der drei `create_item`-Items aus der Top-20-Seite
            # heraus. Kein Bug in `tools.py`/`store.py`, sondern eine reale Zeitstempel-Kollision
            # dieses Smoke-Skripts. Die Fundbarkeit wird stattdessen unten über eine gezielte
            # Suche geprüft (kleines, eindeutiges Ergebnis, unabhängig von der Seitengröße).
            search_text = (await own.call_tool("search_items", {})).data
            search_payload = json.loads(search_text)
            checks.append(
                Check(
                    "search_items (Default-Listing)",
                    search_payload["limit"] == 20
                    and not any(e["status"] == "archived" for e in search_payload["items"]),
                    f"total={search_payload['total']}, limit={search_payload['limit']}",
                    len(search_text.encode("utf-8")),
                )
            )

            targeted_text = (
                await own.call_tool("search_items", {"query": "Smoke-Item"})
            ).data
            targeted_ids = {entry["id"] for entry in json.loads(targeted_text)["items"]}
            checks.append(
                Check(
                    "search_items (eigene Items auffindbar)",
                    all(i in targeted_ids for i in created_ids),
                    f"{len(targeted_ids)} Treffer für 'Smoke-Item'",
                    len(targeted_text.encode("utf-8")),
                )
            )

            # 4. get_item eigen -> Klartext; fremd -> gewrappt.
            own_text = (await own.call_tool("get_item", {"item_id": created_ids[0]})).data
            checks.append(
                Check(
                    "get_item (eigen)",
                    "<untrusted_content" not in own_text,
                    "Klartext ohne Wrap",
                    len(own_text.encode("utf-8")),
                )
            )

            foreign_search = json.loads(
                (await own.call_tool("search_items", {"space": SPACE_FOREIGN})).data
            )
            foreign_id = foreign_search["items"][0]["id"]
            foreign_text = (await own.call_tool("get_item", {"item_id": foreign_id})).data
            checks.append(
                Check(
                    "get_item (fremd)",
                    "<untrusted_content" in foreign_text and f'space="{SPACE_FOREIGN}"' in foreign_text,
                    "Body gewrappt",
                    len(foreign_text.encode("utf-8")),
                )
            )

            # 5. update_item mit falscher Version -> lesbarer Konflikt.
            conflict = await own.call_tool(
                "update_item",
                {"item_id": created_ids[0], "version": 999, "title": "Sollte scheitern"},
                raise_on_error=False,
            )
            conflict_text = conflict.content[0].text if conflict.content else ""
            checks.append(
                Check(
                    "update_item (falsche Version)",
                    conflict.is_error and "conflict" in conflict_text and "999" in conflict_text,
                    conflict_text,
                    len(conflict_text.encode("utf-8")),
                )
            )

            # 6. append_to_item -> Version +1. Seit P6 Step 1 eine Quittung statt Dateitext
            # (P6-H); Body-Inhalt gehört nie in eine Quittung (Regressionsschutz für genau das
            # unten), deshalb keine "Angehängt."-Textsuche mehr — `appended_bytes` beweist die
            # Länge des tatsächlich angehängten Texts.
            appended_text = (
                await own.call_tool(
                    "append_to_item",
                    {"item_id": created_ids[0], "version": 1, "text": "Angehängt."},
                )
            ).data
            appended = json.loads(appended_text)
            checks.append(
                Check(
                    "append_to_item",
                    appended.get("version") == 2
                    and appended.get("appended_bytes") == len("Angehängt.".encode("utf-8"))
                    and "Angehängt." not in appended_text,
                    f"version={appended.get('version')}, appended_bytes={appended.get('appended_bytes')}",
                    len(appended_text.encode("utf-8")),
                )
            )

            # 6b. patch_item -- punktuelle Ersetzung statt Komplett-Rewrite (P6-E), die Mission
            # dieser Phase. Ambiguous-old_text-Fehlversuch ist Teil der LIVE-Abnahme (Gate A→B
            # #1, `docs/concepts/phase6_shares_plan.md` §6 Zeile 2), nicht dieses Smoke-Skripts.
            patched_text = (
                await own.call_tool(
                    "patch_item",
                    {
                        "item_id": created_ids[0], "version": 2,
                        "edits": [
                            {"old_text": "Angehängt.", "new_text": "Angehängt. Gepatcht."}
                        ],
                    },
                )
            ).data
            patched = json.loads(patched_text)
            checks.append(
                Check(
                    "patch_item",
                    patched.get("version") == 3
                    and patched.get("replacements") == 1
                    and patched.get("lines") == [1]
                    and "Gepatcht." not in patched_text,
                    f"version={patched.get('version')}, replacements={patched.get('replacements')}, "
                    f"lines={patched.get('lines')}",
                    len(patched_text.encode("utf-8")),
                )
            )

            # 7. update_item(status=archived) -> Datei in _archive/. Version jetzt 3 (nach
            # append + patch), Quittung statt Dateitext -- Datei-Ortsprüfung trägt den Beweis.
            archived_text = (
                await own.call_tool(
                    "update_item",
                    {"item_id": created_ids[0], "version": 3, "status": "archived"},
                )
            ).data
            archive_dir = data_root / SPACE_OWN / "_archive"
            file_moved = any(p.name.startswith(created_ids[0]) for p in archive_dir.glob("*.md"))
            checks.append(
                Check(
                    "update_item (archivieren)",
                    file_moved,
                    "Datei liegt in _archive/" if file_moved else "Datei NICHT in _archive/ gefunden",
                    len(archived_text.encode("utf-8")),
                )
            )

            # 8. update_item auf ein fremdes Item -> write_denied.
            denial = await own.call_tool(
                "update_item",
                {"item_id": foreign_id, "version": 1, "title": "Fremdzugriff"},
                raise_on_error=False,
            )
            denial_text = denial.content[0].text if denial.content else ""
            checks.append(
                Check(
                    "update_item (fremder Space)",
                    denial.is_error and "write_denied" in denial_text,
                    denial_text,
                    len(denial_text.encode("utf-8")),
                )
            )


def _print_report(checks: list[Check]) -> None:
    name_width = max(len(c.name) for c in checks)
    print("Sharefyx MCP — Smoke-Test\n")
    for c in checks:
        status = "OK  " if c.ok else "FAIL"
        print(f"[{status}] {c.name.ljust(name_width)}  {c.detail}")

    print("\nGrößenmessung (Bytes je Antwort):")
    for c in checks:
        size = f"{c.response_bytes} B" if c.response_bytes is not None else "—"
        print(f"  {c.name.ljust(name_width)}  {size}")

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
        prog="mcp_smoke",
        description="End-to-End-Smoke-Test der sechs MCP-Tools gegen ein temporäres DATA_ROOT "
        "(nie das echte). Kein echter Port, kein Netz, kein Keyring.",
    )
    parser.add_argument(
        "--json", action="store_true", help="Maschinenlesbare Ausgabe auf stdout statt Text"
    )
    args = parser.parse_args(argv)

    checks: list[Check] = []
    with tempfile.TemporaryDirectory(prefix="mcp_smoke_") as tmp:
        logger.info("temporäres DATA_ROOT: %s", tmp)
        asyncio.run(_run(Path(tmp), checks))

    if args.json:
        print(json.dumps([asdict(c) for c in checks], ensure_ascii=False, indent=2))
    else:
        _print_report(checks)

    return EXIT_OK if all(c.ok for c in checks) else EXIT_FAILED


if __name__ == "__main__":
    sys.exit(main())
