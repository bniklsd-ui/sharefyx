#!/usr/bin/env python3
"""P7-10: `testnutzer-p7` hat Konto, Space, einen eigenen OAuth-Client und schreibt einmal.

Fährt den vollen OAuth-2.1+PKCE-Fluss direkt gegen den echten, laufenden Server (kein
`ASGITransport`, echtes Netz) — dasselbe Muster wie `phase4_auth/scripts/oauth_smoke.py`s
`--base-url`-Modus, aber ohne `getpass()`: `testnutzer-p7` ist ein rein skriptgesteuerter
Principal (P7-W), Passwort/TOTP kommen aus `testcred.py`, nie von einer Tastatur.

Grund für dieses eigene Skript statt eines claude.ai-Custom-Connectors (Session vom 2026-08-23):
claude.ai dedupliziert Custom Connectors organisationsweit nach Server-URL — ein zweiter,
eigener Connector für `testnutzer-p7` auf demselben Account wie der bestehende `sharefyx`-
Connector ist strukturell nicht möglich. Der eigentliche Nachweis (Konto+Space+Connector+Write)
läuft eine Ebene tiefer: derselbe OAuth-Server, den auch claude.ai anspricht.

DCR-Client wird jeder Lauf frisch registriert (kein persistierter `client_id`, wie
`oauth_smoke.py`) — der Server räumt verwaiste Registrierungen selbst ab (O2,
`purge_expired()`). Schreibt genau EIN Item in `testnutzer-p7`s eigenem Space (kein
`space=`-Override) und lässt es stehen — P7-12s Abbau-Checkliste entfernt den ganzen Space
ohnehin am Ende von Block A.

Ausgabe: Text (Standard) oder `--json` auf stdout; Logs/TOTP-Codes NIE auf stdout (Hard Rule 7).
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


async def run(testcred) -> dict:
    creds = testcred._load()
    if creds is None:
        raise SystemExit("ABBRUCH: kein testcred-Eintrag — erst 'testcred.py store' laufen lassen.")
    password = creds["password"]
    totp_secret = creds["totp_secret"]

    verifier = crypto.new_secret()
    challenge = crypto.pkce_challenge(verifier)

    async with httpx.AsyncClient(base_url=BASE_URL, timeout=15.0) as client:
        prm = (await client.get("/.well-known/oauth-protected-resource")).json()
        resource = prm["resource"]

        register_resp = await client.post(
            "/oauth/register",
            headers={"Content-Type": "application/json"},
            json={
                "client_name": "p7_10_write_probe",
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
                "state": "p7-10-probe",
                "code_challenge": challenge,
                "code_challenge_method": "S256",
                "scope": "space offline_access",
                "resource": resource,
            },
        )
        authorize_resp.raise_for_status()
        request_id = _extract_request_id(authorize_resp.text)

        # TOTP unmittelbar vor dem Absenden ziehen (30s-Fenster, kein Vorrat).
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
        access_token = token_resp.json()["access_token"]

        headers = {"Authorization": f"Bearer {access_token}"}
        transport = StreamableHttpTransport(url=f"{BASE_URL}/mcp/", headers=headers)
        async with Client(transport) as mcp:
            spaces_result = await mcp.call_tool("list_spaces", {})
            spaces = {entry["name"] for entry in json.loads(spaces_result.data)}

            write_result = await mcp.call_tool(
                "create_item",
                {
                    "type": "note",
                    "title": "P7-10 Schreibprobe",
                    "body": (
                        "Automatischer Schreib-Nachweis fuer P7-10 "
                        "(phase7_spaces_admin/scripts/p7_10_write_probe.py)."
                    ),
                },
            )
            receipt = json.loads(write_result.data)

        return {
            "own_space_visible": SPACE in spaces,
            "spaces": sorted(spaces),
            "write_receipt": receipt,
        }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="p7_10_write_probe",
        description="P7-10: testnutzer-p7 loggt sich per OAuth ein und schreibt einmal.",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    testcred = _load_testcred()
    result = asyncio.run(run(testcred))

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"own_space_visible: {result['own_space_visible']}")
        print(f"spaces: {result['spaces']}")
        print(f"write_receipt: {result['write_receipt']}")

    ok = result["own_space_visible"] and result["write_receipt"].get("id")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
