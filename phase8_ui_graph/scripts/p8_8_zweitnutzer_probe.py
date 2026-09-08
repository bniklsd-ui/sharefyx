#!/usr/bin/env python3
"""Phase 8 P8-8 -- echter Zweitnutzer-Pass-Through-Nachweis ueber zwei unabhaengige,
authentifizierte OAuth+MCP-Principals gegen die Wegwerf-Instanz aus `wegwerf_setup_p8_8.py`
(Port 18780, `testuser1`/`testuser2`).

Reproduziert die fuenf Punkte aus SICHTPRUEFUNG_WALKTHROUGH.md C5-2 / phase8_ui_graph_plan §7
P8-8 -- nur mit zwei synthetischen Principals statt Nikinger+Fabian. Nutzt denselben rohen
OAuth-Discovery/DCR/PKCE-Ablauf wie `phase4_auth/scripts/oauth_smoke.py :: _run_checks()`
(dort nicht direkt importierbar, weil an dessen `Check`-Buchfuehrung + Refresh/Replay-Runden
gekoppelt -- hier schlanker nachgebaut, nur bis zum ersten Access-Token) und denselben
Fehlersignatur-Pattern wie `phase2_mcp/scripts/mcp_smoke.py` (`<untrusted_content`-Wrapping,
`raise_on_error=False` + `write_denied`-Text fuer den erwarteten Deny-Fall).

Fuenf Assertions:
  1. testuser2 sucht in testuser1s Space -> das PRIVATE Item taucht NICHT auf.
  2. testuser2 sucht in testuser1s Space -> das GETEILTE Item taucht auf (nach dem Share).
  3. testuser2 liest das geteilte Item -> Body vorhanden, `<untrusted_content>`-gewrappt.
  4. testuser2 liest das private Item -> abgelehnt (nicht sichtbar/nicht lesbar).
  5. testuser2 versucht das geteilte Item zu schreiben (nur `share_read`, kein `share_write`)
     -> abgelehnt mit `write_denied`.
"""
from __future__ import annotations

import asyncio
import json
import time
import urllib.parse
from pathlib import Path

import httpx
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

from authserver import crypto, totp

WEGWERF_ROOT = Path("/tmp/opencode/sharefyx-wegwerf-p8-8")
CREDS_FILE = WEGWERF_ROOT / "credentials.json"
IDS_FILE = WEGWERF_ROOT / "ids.json"
PORT = 18780
BASE_URL = f"http://127.0.0.1:{PORT}"
REDIRECT_URI = "https://claude.ai/callback"


def _totp_secret(otpauth_uri: str) -> str:
    return urllib.parse.unquote(otpauth_uri.split("secret=")[1].split("&")[0])


async def _get_access_token(client: httpx.AsyncClient, *, space: str, password: str,
                             totp_secret: str, counter_offset: int = 0) -> str:
    """Schlanker OAuth-Dance bis zum ersten Access-Token: Discovery -> DCR -> Authorize
    (GET+POST) -> Token-Tausch. Kein Refresh/Replay -- das ist P4-Territorium, hier reicht
    ein gueltiges Bearer-Token fuer die ACL-Probe."""
    prm = (await client.get("/.well-known/oauth-protected-resource")).json()
    resource = prm["resource"]

    register = await client.post(
        "/oauth/register",
        json={"client_name": "p8_8_probe", "application_type": "web",
              "redirect_uris": [REDIRECT_URI]},
    )
    client_id = register.json()["client_id"]

    verifier = crypto.pkce_verifier() if hasattr(crypto, "pkce_verifier") else None
    if verifier is None:
        import secrets
        verifier = secrets.token_urlsafe(64)[:64]
    challenge = crypto.pkce_challenge(verifier)
    state = f"state-{space}"

    get_resp = await client.get(
        "/oauth/authorize",
        params={
            "client_id": client_id, "redirect_uri": REDIRECT_URI, "response_type": "code",
            "state": state, "code_challenge": challenge, "code_challenge_method": "S256",
            "scope": "space", "resource": resource,
        },
    )
    assert get_resp.status_code == 200, f"authorize GET -> {get_resp.status_code}"
    import re
    m = re.search(r'name="request_id" value="([^"]+)"', get_resp.text)
    assert m, "kein request_id im Formular"
    request_id = m.group(1)

    counter = int(time.time() // 30) + counter_offset
    totp_code = totp.totp_at(totp_secret, counter)

    post_resp = await client.post(
        "/oauth/authorize",
        data={"request_id": request_id, "space": space, "password": password,
              "totp": totp_code, "action": "allow"},
        follow_redirects=False,
    )
    assert post_resp.status_code == 302, f"authorize POST -> {post_resp.status_code}: {post_resp.text[:200]}"
    location = post_resp.headers["location"]
    query = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(location).query))
    code = query["code"]

    token_resp = await client.post(
        "/oauth/token",
        data={"grant_type": "authorization_code", "code": code, "redirect_uri": REDIRECT_URI,
              "client_id": client_id, "code_verifier": verifier},
    )
    assert token_resp.status_code == 200, f"token exchange -> {token_resp.status_code}: {token_resp.text[:200]}"
    return token_resp.json()["access_token"]


def _mcp_client(token: str) -> Client:
    transport = StreamableHttpTransport(
        url=f"{BASE_URL}/mcp/", headers={"Authorization": f"Bearer {token}"}
    )
    return Client(transport)


async def _probe() -> dict:
    creds = json.loads(CREDS_FILE.read_text())
    ids = json.loads(IDS_FILE.read_text())
    result: dict = {"checks": []}

    def check(name: str, ok: bool, detail: str) -> None:
        result["checks"].append({"name": name, "ok": ok, "detail": detail})

    async with httpx.AsyncClient(base_url=BASE_URL, timeout=10.0) as http:
        token_a = await _get_access_token(
            http, space="testuser1", password=creds["testuser1"]["password"],
            totp_secret=_totp_secret(creds["testuser1"]["otpauth_uri"]),
        )
        # counter_offset=1: testuser2s Runde faellt moeglicherweise ins selbe 30s-Fenster wie
        # testuser1s Runde -- ein identischer Zaehlerwert waere ein TOTP-Replay auf server-
        # seitig unabhaengigem State, aber Vorsicht kostet nichts (siehe oauth_smoke.py-Kommentar).
        token_b = await _get_access_token(
            http, space="testuser2", password=creds["testuser2"]["password"],
            totp_secret=_totp_secret(creds["testuser2"]["otpauth_uri"]), counter_offset=1,
        )

    private_id = ids["private"]
    shared_id = ids["shared"]
    # share_read wurde bereits im Setup-Skript per direktem Store.update() gesetzt --
    # `update_item` lehnt share_read/share_write kategorisch ab ("das geht nur ein Mensch in
    # der UI", tools.py), ein MCP-Aufruf koennte es hier nicht nachholen. token_a wird nur
    # noch fuer die Symmetrie im Log gehalten, nicht mehr fuer einen Tool-Call gebraucht.
    _ = token_a

    async with _mcp_client(token_b) as b:
        # 1+2: search_items in testuser1s Space.
        search = json.loads(
            (await b.call_tool("search_items", {"space": "testuser1", "limit": 50})).data
        )
        found_ids = {item["id"] for item in search["items"]}
        check("1_private_not_in_search", private_id not in found_ids,
              f"private_id={private_id} in results={sorted(found_ids)}")
        check("2_shared_in_search", shared_id in found_ids,
              f"shared_id={shared_id} in results={sorted(found_ids)}")

        # 3: get_item auf das geteilte Item -> Body + <untrusted_content>-Wrapping.
        shared_text = (await b.call_tool("get_item", {"item_id": shared_id})).data
        check("3_shared_readable_and_wrapped",
              "<untrusted_content" in shared_text and 'space="testuser1"' in shared_text,
              shared_text[:150])

        # 4: get_item auf das PRIVATE Item -> abgelehnt.
        denial_read = await b.call_tool(
            "get_item", {"item_id": private_id}, raise_on_error=False
        )
        denial_read_text = denial_read.content[0].text if denial_read.content else ""
        check("4_private_read_denied", denial_read.is_error, denial_read_text[:150])

        # 5: update_item auf das geteilte Item (nur share_read, kein share_write) -> denied.
        denial_write = await b.call_tool(
            "update_item", {"item_id": shared_id, "version": 1, "title": "Fremdzugriff"},
            raise_on_error=False,
        )
        denial_write_text = denial_write.content[0].text if denial_write.content else ""
        check("5_shared_write_denied",
              denial_write.is_error and "write_denied" in denial_write_text,
              denial_write_text[:150])

    return result


def main() -> int:
    result = asyncio.run(_probe())
    print(json.dumps(result, indent=2, ensure_ascii=False))
    ok = all(c["ok"] for c in result["checks"])
    print()
    for c in result["checks"]:
        print(f"[{'OK' if c['ok'] else 'FAIL'}] {c['name']}: {c['detail']}")
    print()
    print(f"P8-8-Bilanz: {'BESTANDEN' if ok else 'FEHLGESCHLAGEN'} "
          f"({sum(c['ok'] for c in result['checks'])}/{len(result['checks'])})")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
