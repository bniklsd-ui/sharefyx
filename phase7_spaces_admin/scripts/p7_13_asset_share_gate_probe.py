#!/usr/bin/env python3
"""P6.5-13/P7-13-Teilprobe: `testnutzer-p7` ruft `get_item_asset` über den echten OAuth-Fluss auf
ein fremdes Bild ab — einmal mit reinem `share_read` (erwartet: nur Metadaten, `bytes_available:
false`), einmal nach Erweiterung auf `share_write` (erwartet: echte Bytes). Gleiche Bauart wie
`p7_10_write_probe.py` (echtes Netz, kein `ASGITransport`, DCR-Client frisch je Lauf).

Grund für dieses Skript: P6.5-13 war im ursprünglichen Plan an Fabian gebunden (kein
verfügbarer zweiter Principal zum Testzeitpunkt). `testnutzer-p7` ist die vom Nikinger
gebilligte Substitution (P7-Plan §A8.1) — dieselbe serverseitige Rechteprüfung
(`mcpserver/tools.py :: get_item_asset()`, P6.5-M: Bytes nur bei eigenem Space ODER
Schreibrecht, nie bei reinem Leserecht), ein anderer Principal-Name ändert daran nichts.

Voraussetzung: `p7_13_asset_fixture.py <item_id>` lief bereits (Asset existiert),
`p7_11_setup_fixture.py <item_id> --version <n>` hat `share_read: [testnutzer-p7]` gesetzt.
"""
from __future__ import annotations

import argparse
import asyncio
import importlib.util
import json
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
    import re

    match = re.search(r'name="request_id" value="([^"]+)"', html)
    if match is None:
        raise AssertionError("kein request_id im Login-Formular gefunden")
    return match.group(1)


async def _get_access_token(client: httpx.AsyncClient, testcred) -> str:
    creds = testcred._load()
    if creds is None:
        raise SystemExit("ABBRUCH: kein testcred-Eintrag — erst 'testcred.py store' laufen lassen.")
    password = creds["password"]
    totp_secret = creds["totp_secret"]

    verifier = crypto.new_secret()
    challenge = crypto.pkce_challenge(verifier)

    prm = (await client.get("/.well-known/oauth-protected-resource")).json()
    resource = prm["resource"]

    register_resp = await client.post(
        "/oauth/register",
        headers={"Content-Type": "application/json"},
        json={
            "client_name": "p7_13_asset_share_gate_probe",
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
            "state": "p7-13-probe",
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
            f"POST /oauth/authorize -> {consent_resp.status_code}: {consent_resp.text[:300]!r}"
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


async def run(testcred, item_id: str, asset_id: str) -> dict:
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=15.0) as client:
        access_token = await _get_access_token(client, testcred)

    headers = {"Authorization": f"Bearer {access_token}"}
    transport = StreamableHttpTransport(url=f"{BASE_URL}/mcp/", headers=headers)
    async with Client(transport) as mcp:
        result = await mcp.call_tool("get_item_asset", {"item_id": item_id, "asset_id": asset_id})
        # Bei Schreibrecht liefert das Tool ein Image-Content-Objekt (Bytes), kein JSON-Text —
        # bei reinem Leserecht kommt kompaktes JSON mit bytes_available:false zurück (P6.5-M).
        content = result.content[0]
        if content.type == "text":
            payload = json.loads(content.text)
            return {"kind": "json", "payload": payload}
        return {"kind": "image", "mime_type": getattr(content, "mimeType", None)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="p7_13_asset_share_gate_probe",
        description="testnutzer-p7 ruft get_item_asset auf ein fremdes Bild ab.",
    )
    parser.add_argument("item_id")
    parser.add_argument("asset_id")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    testcred = _load_testcred()
    result = asyncio.run(run(testcred, args.item_id, args.asset_id))

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"kind: {result['kind']}")
        if result["kind"] == "json":
            print(f"bytes_available: {result['payload'].get('bytes_available')}")
        else:
            print(f"mime_type: {result.get('mime_type')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
