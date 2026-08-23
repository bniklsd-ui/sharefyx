#!/usr/bin/env python3
"""P7-11: `testnutzer-p7` sieht ein NUR item-level freigegebenes Item — und nur dieses
(P6-Zeilen 36/37).

Voraussetzung, von einem Menschen einmalig zu schaffen (item-level `share_read` geht laut
`webui/api.py`/`mcpserver/tools.py` bewusst über kein MCP-Tool, nur über die UI — kein
Umgehungspfad hier): ein Item in einem fremden Space (z. B. `niklas`) trägt
`share_read: [testnutzer-p7]`, OHNE dass `testnutzer-p7` in diesem Space irgendeinen
space-level Grant hat (kein Eintrag in `<space>/.share.yml`). Die Item-ID kommt als Argument —
dieses Skript legt nichts an, es prüft nur.

Eigenständig wie `p7_10_write_probe.py` (bewusst kein gemeinsames Auth-Modul zwischen den P7-
Testskripten — jedes Skript ist für sich lauffähig und lesbar, Duplikation hier ist der Preis
für Reproduzierbarkeit ohne versteckte Abhängigkeit zwischen Testläufen).

Prüfung: `search_items()` OHNE `space=`-Filter (die globale, ACL-gefilterte Suche aus
`GLOBAL_SEARCH_PLAN.md`) muss genau die erwartete ID enthalten UND darf keine weitere ID aus
einem fremden Space zeigen (eigene `testnutzer-p7`-Items sind erwartungsgemäß mit dabei, kein
Fehlerfall).

Ausgabe: Text (Standard) oder `--json` auf stdout; Logs/TOTP-Codes NIE auf stdout (Hard Rule 7).
"""
from __future__ import annotations

import argparse
import asyncio
import importlib.util
import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import httpx
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

from authserver import crypto
from authserver import totp as totp_mod

BASE_URL = "https://savefyx-vmware-virtual-platform.tail89fc2a.ts.net"
SPACE = "testnutzer-p7"
REDIRECT_URI = "https://claude.ai/api/mcp/auth_callback"


def _load_testcred():
    script_path = Path(__file__).with_name("testcred.py")
    spec = importlib.util.spec_from_file_location("testcred", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _redirect_query(location: str) -> dict[str, str]:
    parsed = parse_qs(urlsplit(location).query)
    return {k: v[0] for k, v in parsed.items()}


def _extract_request_id(html: str) -> str:
    match = re.search(r'name="request_id" value="([^"]+)"', html)
    if match is None:
        raise AssertionError("kein request_id im Login-Formular gefunden")
    return match.group(1)


async def _login(client: httpx.AsyncClient, testcred) -> str:
    """Voller OAuth-Fluss, gibt den Access-Token zurück. Identisch zu
    `p7_10_write_probe.py :: run()`s Login-Teil — bewusst dupliziert, siehe Modul-Docstring."""
    creds = testcred._load()
    if creds is None:
        raise SystemExit("ABBRUCH: kein testcred-Eintrag — erst 'testcred.py store' laufen lassen.")
    password = creds["password"]
    totp_secret = creds["totp_secret"]

    verifier = crypto.new_secret()
    challenge = crypto.pkce_challenge(verifier)

    resource = (await client.get("/.well-known/oauth-protected-resource")).json()["resource"]

    register_resp = await client.post(
        "/oauth/register",
        headers={"Content-Type": "application/json"},
        json={
            "client_name": "p7_11_visibility_probe",
            "application_type": "web",
            "redirect_uris": [REDIRECT_URI],
        },
    )
    register_resp.raise_for_status()
    client_id = register_resp.json()["client_id"]

    authorize_resp = await client.get(
        "/oauth/authorize",
        params={
            "client_id": client_id,
            "redirect_uri": REDIRECT_URI,
            "response_type": "code",
            "state": "p7-11-probe",
            "code_challenge": challenge,
            "code_challenge_method": "S256",
            "scope": "space offline_access",
            "resource": resource,
        },
    )
    authorize_resp.raise_for_status()
    request_id = _extract_request_id(authorize_resp.text)

    totp_code = totp_mod.totp_at(totp_secret, int(time.time()) // 30)

    consent_resp = await client.post(
        "/oauth/authorize",
        data={
            "request_id": request_id,
            "space": SPACE,
            "password": password,
            "totp": totp_code,
            "action": "allow",
        },
        follow_redirects=False,
    )
    if consent_resp.status_code != 302:
        raise AssertionError(
            f"POST /oauth/authorize -> {consent_resp.status_code}: "
            f"{consent_resp.text[:300]!r}"
        )
    code = _redirect_query(consent_resp.headers["location"])["code"]

    token_resp = await client.post(
        "/oauth/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "client_id": client_id,
            "code_verifier": verifier,
        },
    )
    token_resp.raise_for_status()
    return token_resp.json()["access_token"]


async def run(testcred, expected_item_id: str) -> dict:
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=15.0) as client:
        access_token = await _login(client, testcred)

    headers = {"Authorization": f"Bearer {access_token}"}
    transport = StreamableHttpTransport(url=f"{BASE_URL}/mcp/", headers=headers)
    async with Client(transport) as mcp:
        # Kein space=-Filter: die globale, ACL-gefilterte Suche (GLOBAL_SEARCH_PLAN.md).
        search_result = await mcp.call_tool("search_items", {"limit": 100})
    payload = json.loads(search_result.data)
    items = payload["items"]

    own_ids = {i["id"] for i in items if i.get("space") == SPACE}
    foreign_ids = {i["id"] for i in items} - own_ids

    return {
        "expected_item_id": expected_item_id,
        "expected_item_visible": expected_item_id in {i["id"] for i in items},
        "own_ids": sorted(own_ids),
        "foreign_ids": sorted(foreign_ids),
        "foreign_ids_are_exactly_expected": foreign_ids == {expected_item_id},
        "total": payload["total"],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="p7_11_visibility_probe",
        description=(
            "P7-11: testnutzer-p7 sieht ein nur item-level freigegebenes Item, und nur dieses."
        ),
    )
    parser.add_argument(
        "item_id",
        help="ID des Items mit item-level share_read fuer testnutzer-p7 (von einem Menschen "
        "vorab in der Web-UI gesetzt).",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    testcred = _load_testcred()
    result = asyncio.run(run(testcred, args.item_id))

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"expected_item_visible: {result['expected_item_visible']}")
        print(f"own_ids (testnutzer-p7): {result['own_ids']}")
        print(f"foreign_ids (sollte nur die erwartete ID sein): {result['foreign_ids']}")
        print(f"foreign_ids_are_exactly_expected: {result['foreign_ids_are_exactly_expected']}")

    ok = result["expected_item_visible"] and result["foreign_ids_are_exactly_expected"]
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
