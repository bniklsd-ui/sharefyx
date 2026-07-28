#!/usr/bin/env python3
"""oauth_smoke.py — Gegenstück zu `mcp_smoke.py` (P2) für den OAuth-Fluss (Plan §5 Step 6):
fährt **ohne Browser** den vollständigen Fluss gegen ein in-process gestartetes
`create_app(oauth=...)` (kein echter Port, kein Netz — `httpx.ASGITransport`, dasselbe Muster
wie `mcp_smoke.py`). Baut ein temporäres `DATA_ROOT` **und** eine temporäre `auth.sqlite3` (nie
die echten).

**Kein echter Keyring, kein `load_users()`/`load_auth_settings()`.** Beide lesen echten Zustand
(Keyring bzw. echte Umgebungsvariablen) — dieses Skript baut seine `AuthSettings` direkt und
seine eine Nutzerakte über `passwords.hash_password()`/`totp.generate_secret()` (reine
Funktionen), genau wie `mcp_smoke.py` seine Tokens über `credentials.generate_token()`/
`hash_token()` baut statt den echten Keyring anzufassen. Ein TOTP-Seed ist ein echtes,
umkehrbares Geheimnis (anders als ein Token-Hash) — ein Grund mehr, hier nie die echten
Nutzerakten zu lesen.

Ablauf: Discovery (PRM + AS-Metadaten) → DCR → `GET /oauth/authorize` → Formular-`POST`
(Passwort + errechneter TOTP-Code) → Code → Token → echter Tool-Aufruf mit Bearer → Refresh →
Reuse des alten Refresh-Tokens (muss `invalid_grant` liefern und die Token-Familie töten) → eine
**zweite, unabhängige** Authorize-Runde nur für den Code-Replay-Nachweis (die erste Familie ist
nach dem Refresh-Replay bereits tot, kann also nicht auch noch den Code-Replay beweisen).
**11 Prüfungen** (Plan §6, Abnahmezeilen 10/11: Refresh- **und** Code-Replay, beide über dieses
Skript). Die zweite Runde bündelt Formular + Code-Tausch in einer Prüfung, sonst wären es zwölf
— bewusste Zählungsentscheidung, hier dokumentiert statt still abweichend.

Markerwerte (für `test_oauth_log_never_contains_secrets`, P4 Step 6b): Werte, die dieses Skript
selbst wählt (Passwort, `state`, PKCE-`code_verifier`), tragen ein `ZZZ-`-Präfix und stehen in
`MARKER_SECRETS`. Serverseitig erzeugte Geheimnisse (Autorisierungscode, Access-/Refresh-Token,
der errechnete TOTP-Code) sind echte Zufallswerte — die kann man nicht vorab markieren; `_run()`
sammelt sie in `observed_secrets`, damit ein Aufrufer sie gegen einen Logpuffer prüfen kann.

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
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import httpx
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

from authserver import crypto, passwords, totp
from authserver.config import AuthSettings
from authserver.store import AuthStore

from mcpserver.app import OAuthConfig, create_app
from mcpserver.auth import KeyringTokenResolver
from mcpserver.config import Settings
from mcpserver.request_log import AccessLogASGI, OAuthLogASGI
from storage.store import Store

logger = logging.getLogger("oauth_smoke")

# Fixture-Space, kein Nikinger-typischer Name (gleiche Begründung wie mcp_smoke.py SPACE_OWN).
SPACE = "alpha"
REDIRECT_URI = "https://claude.ai/callback"

PASSWORD_MARKER = "ZZZ-PASSWORD"
STATE_MARKER_R1 = "ZZZ-STATE-1"
STATE_MARKER_R2 = "ZZZ-STATE-2"
VERIFIER_MARKER_R1 = "ZZZ-VERIFIER-1-" + "A" * 40
VERIFIER_MARKER_R2 = "ZZZ-VERIFIER-2-" + "B" * 40

# Client-kontrollierte Werte — dürfen laut Plan §4 ebenfalls nie in einer Logzeile stehen.
MARKER_SECRETS: tuple[str, ...] = (
    PASSWORD_MARKER,
    STATE_MARKER_R1,
    STATE_MARKER_R2,
    VERIFIER_MARKER_R1,
    VERIFIER_MARKER_R2,
)

EXIT_OK = 0
EXIT_FAILED = 1


@dataclass
class Check:
    name: str
    ok: bool
    detail: str


def _redirect_query(location: str) -> dict[str, str]:
    parsed = parse_qs(urlsplit(location).query)
    return {k: v[0] for k, v in parsed.items()}


def _extract_request_id(html: str) -> str | None:
    match = re.search(r'name="request_id" value="([^"]+)"', html)
    return match.group(1) if match else None


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


async def _bearer_status(client: httpx.AsyncClient, token: str) -> int:
    """Roher Statuscode einer `/mcp/`-Anfrage mit gegebenem Bearer-Token — `BearerAuthASGI`
    entscheidet vor jedem FastMCP-Handshake, ein echtes MCP-Protokoll-Payload ist für den
    Nachweis "Familie tot -> 401" nicht nötig (siehe `asgi.py :: BearerAuthASGI.__call__`,
    sendet 401 bevor die innere App überhaupt aufgerufen wird)."""
    resp = await client.post(
        "/mcp/", headers={"Authorization": f"Bearer {token}"}, json={}
    )
    return resp.status_code


async def _run(
    data_root: Path, checks: list[Check], observed_secrets: list[str]
) -> None:
    auth_settings = AuthSettings(
        base_url="https://space.example.ts.net", db_path=data_root / "auth.sqlite3"
    )
    auth_store = AuthStore(auth_settings.db_path, now_fn=lambda: datetime.now(timezone.utc))

    totp_secret = totp.generate_secret()
    users = {
        SPACE: {
            "pwd": passwords.hash_password(PASSWORD_MARKER),
            "totp": totp_secret,
            "totp_alg": "SHA1",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
    }

    notes_root = data_root / "notes"
    notes_root.mkdir()
    store = Store(notes_root, git=False)
    settings = Settings(data_root=notes_root)
    # Leere Map: der Pfad-Weg wird unter `mode="oauth"` (Default) nie angefragt
    # (`AuthModeASGI.mode == "oauth"` dispatcht immer an `BearerAuthASGI`), reine Vollständigkeit
    # des Parameters — kein echter Keyring-Zugriff (`load_map` injiziert, wie in `mcp_smoke.py`).
    path_resolver = KeyringTokenResolver(load_map=lambda: {})

    raw_app = create_app(
        settings=settings,
        resolver=path_resolver,
        store=store,
        oauth=OAuthConfig(settings=auth_settings, store=auth_store, users=users),
    )
    # Dieselbe Verdrahtung wie `scripts/serve.py` (P4 Step 6b): `AccessLogASGI` außen,
    # `OAuthLogASGI` innen — beide außerhalb von `create_app()`, damit `test_app.py` unverändert
    # bleibt. `raw_app` bleibt für die Lifespan nötig (`AccessLogASGI`/`OAuthLogASGI` sind
    # einfache Callables ohne `.router`).
    app = AccessLogASGI(OAuthLogASGI(raw_app))

    async with raw_app.router.lifespan_context(raw_app):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url=auth_settings.base_url
        ) as client:
            # 1. Protected Resource Metadata (RFC 9728).
            prm_resp = await client.get("/.well-known/oauth-protected-resource")
            prm = prm_resp.json() if prm_resp.status_code == 200 else {}
            checks.append(
                Check(
                    "discovery_protected_resource",
                    prm_resp.status_code == 200
                    and prm.get("resource") == auth_settings.resource
                    and prm.get("authorization_servers") == [auth_settings.issuer],
                    f"status={prm_resp.status_code}, resource={prm.get('resource')!r}",
                )
            )

            # 2. Authorization Server Metadata (RFC 8414).
            as_resp = await client.get("/.well-known/oauth-authorization-server")
            as_meta = as_resp.json() if as_resp.status_code == 200 else {}
            checks.append(
                Check(
                    "discovery_authorization_server",
                    as_resp.status_code == 200
                    and as_meta.get("issuer") == auth_settings.issuer
                    and as_meta.get("token_endpoint") == f"{auth_settings.issuer}/oauth/token",
                    f"status={as_resp.status_code}, issuer={as_meta.get('issuer')!r}",
                )
            )

            # 3. Dynamic Client Registration (RFC 7591).
            register_resp = await client.post(
                "/oauth/register",
                headers={"Content-Type": "application/json"},
                json={
                    "client_name": "oauth_smoke",
                    "application_type": "web",
                    "redirect_uris": [REDIRECT_URI],
                },
            )
            register_body = register_resp.json() if register_resp.status_code == 201 else {}
            client_id = register_body.get("client_id")
            checks.append(
                Check(
                    "register_client",
                    register_resp.status_code == 201 and client_id is not None,
                    f"status={register_resp.status_code}, client_id={client_id!r}",
                )
            )

            async def _authorize_get(*, verifier: str, state: str) -> str:
                """`GET /oauth/authorize` — gibt die `request_id` aus dem gerenderten
                Consent-Formular zurück. Wirft `AssertionError` bei jeder Abweichung."""
                challenge = crypto.pkce_challenge(verifier)
                get_resp = await client.get(
                    "/oauth/authorize",
                    params={
                        "client_id": client_id,
                        "redirect_uri": REDIRECT_URI,
                        "response_type": "code",
                        "state": state,
                        "code_challenge": challenge,
                        "code_challenge_method": "S256",
                        "scope": "space",
                        "resource": auth_settings.resource,
                    },
                )
                if get_resp.status_code != 200:
                    raise AssertionError(f"GET /oauth/authorize -> {get_resp.status_code}")
                request_id = _extract_request_id(get_resp.text)
                if request_id is None:
                    raise AssertionError("kein request_id im Formular gefunden")
                return request_id

            async def _authorize_post(
                *, request_id: str, counter_offset: int = 0
            ) -> tuple[str, str, str]:
                """`POST /oauth/authorize` (Formular-Submit) — gibt
                `(auth_code, returned_state, iss)` aus dem Redirect zurück. Wirft
                `AssertionError` bei jeder Abweichung.

                `counter_offset` schiebt den errechneten TOTP-Zähler nach vorn (Runde 2 braucht
                `+1`): `totp.verify()` verlangt einen Zähler **größer** als der zuletzt akzeptierte
                (Replay-Schutz, `store.py :: get_totp_counter`) — läuft Runde 2 im selben
                30-Sekunden-Fenster wie Runde 1 (üblich bei einem Skript, kein Warten dazwischen),
                wäre der „aktuelle" Zähler sonst identisch zu Runde 1s bereits verbrauchtem und
                würde als Replay abgelehnt, nicht weil der Fluss falsch wäre."""
                counter = int(time.time() // 30) + counter_offset
                totp_code = totp.totp_at(totp_secret, counter)
                observed_secrets.append(totp_code)

                post_resp = await client.post(
                    "/oauth/authorize",
                    data={
                        "request_id": request_id,
                        "space": SPACE,
                        "password": PASSWORD_MARKER,
                        "totp": totp_code,
                        "action": "allow",
                    },
                    follow_redirects=False,
                )
                if post_resp.status_code != 302:
                    raise AssertionError(
                        f"POST /oauth/authorize -> {post_resp.status_code} (erwartet 302), "
                        f"Body: {post_resp.text[:200]!r}"
                    )
                query = _redirect_query(post_resp.headers["location"])
                code = query.get("code")
                if code is None:
                    raise AssertionError(f"keine 'code' im Redirect: {query}")
                observed_secrets.append(code)
                return code, query.get("state", ""), query.get("iss", "")

            # 4. Erste Runde, Schritt 1: Formular rendern.
            try:
                request_id_r1 = await _authorize_get(
                    verifier=VERIFIER_MARKER_R1, state=STATE_MARKER_R1
                )
                checks.append(Check("authorize_get", True, f"request_id={request_id_r1!r}"))
            except AssertionError as exc:
                checks.append(Check("authorize_get", False, str(exc)))
                return

            # 5. Erste Runde, Schritt 2: Login-Formular absenden, inklusive
            # RFC-9207-`iss`-Prüfung.
            try:
                code_r1, returned_state_r1, iss_r1 = await _authorize_post(
                    request_id=request_id_r1
                )
                checks.append(
                    Check(
                        "authorize_post",
                        returned_state_r1 == STATE_MARKER_R1 and iss_r1 == auth_settings.issuer,
                        f"state={returned_state_r1!r}, iss={iss_r1!r}",
                    )
                )
            except AssertionError as exc:
                checks.append(Check("authorize_post", False, str(exc)))
                return

            # 6. Code -> Token (erste Runde).
            token_resp = await client.post(
                "/oauth/token",
                data={
                    "grant_type": "authorization_code",
                    "code": code_r1,
                    "redirect_uri": REDIRECT_URI,
                    "client_id": client_id,
                    "code_verifier": VERIFIER_MARKER_R1,
                },
            )
            token_body = token_resp.json() if token_resp.status_code == 200 else {}
            access_r1 = token_body.get("access_token")
            refresh_r1 = token_body.get("refresh_token")
            if access_r1:
                observed_secrets.append(access_r1)
            if refresh_r1:
                observed_secrets.append(refresh_r1)
            checks.append(
                Check(
                    "token_code_exchange",
                    token_resp.status_code == 200
                    and access_r1 is not None
                    and refresh_r1 is not None,
                    f"status={token_resp.status_code}",
                )
            )

            # 7. Echter Tool-Aufruf mit Bearer — kein Fake, voller Stack bis list_spaces.
            async with _mcp_client(app, access_r1) as mcp:
                result = await mcp.call_tool("list_spaces", {})
            spaces = {entry["name"] for entry in json.loads(result.data)}
            checks.append(
                Check(
                    "tool_call_with_bearer",
                    SPACE in spaces,
                    f"spaces={sorted(spaces)}",
                )
            )

            # 8. Refresh — rotiert, neues Paar.
            refresh_resp = await client.post(
                "/oauth/token", data={"grant_type": "refresh_token", "refresh_token": refresh_r1}
            )
            refresh_body = refresh_resp.json() if refresh_resp.status_code == 200 else {}
            access_r1b = refresh_body.get("access_token")
            refresh_r1b = refresh_body.get("refresh_token")
            if access_r1b:
                observed_secrets.append(access_r1b)
            if refresh_r1b:
                observed_secrets.append(refresh_r1b)
            checks.append(
                Check(
                    "token_refresh",
                    refresh_resp.status_code == 200
                    and access_r1b is not None
                    and refresh_r1b is not None
                    and refresh_r1b != refresh_r1,
                    f"status={refresh_resp.status_code}",
                )
            )

            # 9. Refresh-Replay mit dem ALTEN Refresh-Token — muss invalid_grant liefern UND die
            # Familie töten (RFC 9700). Beleg für "Familie tot": der frisch rotierte Access-Token
            # aus Schritt 8 funktioniert danach ebenfalls nicht mehr.
            replay_resp = await client.post(
                "/oauth/token", data={"grant_type": "refresh_token", "refresh_token": refresh_r1}
            )
            replay_body = replay_resp.json() if replay_resp.status_code == 400 else {}
            family_dead_status = (
                await _bearer_status(client, access_r1b) if access_r1b else None
            )
            checks.append(
                Check(
                    "refresh_replay_kills_family",
                    replay_resp.status_code == 400
                    and replay_body.get("error") == "invalid_grant"
                    and family_dead_status == 401,
                    f"replay_status={replay_resp.status_code}, error={replay_body.get('error')!r}, "
                    f"post_replay_access_status={family_dead_status}",
                )
            )

            # 10. Zweite, unabhängige Runde — die erste Familie ist jetzt tot, der Code-Replay-
            # Nachweis (Zeile 11) braucht eine frische. Bündelt GET+POST+Token-Tausch in EINE
            # Prüfung (anders als Runde 1, die aus Schritten 4/5 einzeln besteht) — sonst wären
            # es zwölf Prüfungen statt der elf aus Plan §6/§5 Step 6; Runde 2 dient nur als
            # Vorbereitung für den Code-Replay-Nachweis, nicht als eigener Beweisschritt.
            try:
                request_id_r2 = await _authorize_get(
                    verifier=VERIFIER_MARKER_R2, state=STATE_MARKER_R2
                )
                code_r2, returned_state_r2, iss_r2 = await _authorize_post(
                    request_id=request_id_r2, counter_offset=1
                )
                token_resp_2 = await client.post(
                    "/oauth/token",
                    data={
                        "grant_type": "authorization_code",
                        "code": code_r2,
                        "redirect_uri": REDIRECT_URI,
                        "client_id": client_id,
                        "code_verifier": VERIFIER_MARKER_R2,
                    },
                )
                token_body_2 = token_resp_2.json() if token_resp_2.status_code == 200 else {}
                access_r2 = token_body_2.get("access_token")
                refresh_r2 = token_body_2.get("refresh_token")
                if access_r2:
                    observed_secrets.append(access_r2)
                if refresh_r2:
                    observed_secrets.append(refresh_r2)
                checks.append(
                    Check(
                        "second_authorize_round",
                        returned_state_r2 == STATE_MARKER_R2
                        and iss_r2 == auth_settings.issuer
                        and token_resp_2.status_code == 200
                        and access_r2 is not None,
                        f"state={returned_state_r2!r}, token_status={token_resp_2.status_code}",
                    )
                )
            except AssertionError as exc:
                checks.append(Check("second_authorize_round", False, str(exc)))
                return

            # 11. Code-Replay — derselbe Code aus Runde 2 ein zweites Mal einlösen: muss
            # invalid_grant liefern UND die (zweite) Familie töten.
            code_replay_resp = await client.post(
                "/oauth/token",
                data={
                    "grant_type": "authorization_code",
                    "code": code_r2,
                    "redirect_uri": REDIRECT_URI,
                    "client_id": client_id,
                    "code_verifier": VERIFIER_MARKER_R2,
                },
            )
            code_replay_body = (
                code_replay_resp.json() if code_replay_resp.status_code == 400 else {}
            )
            family_dead_status_2 = (
                await _bearer_status(client, access_r2) if access_r2 else None
            )
            checks.append(
                Check(
                    "code_replay_kills_family",
                    code_replay_resp.status_code == 400
                    and code_replay_body.get("error") == "invalid_grant"
                    and family_dead_status_2 == 401,
                    f"replay_status={code_replay_resp.status_code}, "
                    f"error={code_replay_body.get('error')!r}, "
                    f"post_replay_access_status={family_dead_status_2}",
                )
            )


def _print_report(checks: list[Check]) -> None:
    name_width = max(len(c.name) for c in checks)
    print("Sharefyx OAuth — Smoke-Test\n")
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
        prog="oauth_smoke",
        description="End-to-End-Smoke-Test des OAuth-Flusses gegen ein temporäres DATA_ROOT/"
        "auth.sqlite3 (nie die echten). Kein echter Port, kein Netz, kein Keyring.",
    )
    parser.add_argument(
        "--json", action="store_true", help="Maschinenlesbare Ausgabe auf stdout statt Text"
    )
    args = parser.parse_args(argv)

    checks: list[Check] = []
    observed_secrets: list[str] = []
    with tempfile.TemporaryDirectory(prefix="oauth_smoke_") as tmp:
        logger.info("temporäres DATA_ROOT/auth.sqlite3 unter: %s", tmp)
        asyncio.run(_run(Path(tmp), checks, observed_secrets))

    if args.json:
        print(json.dumps([asdict(c) for c in checks], ensure_ascii=False, indent=2))
    else:
        _print_report(checks)

    return EXIT_OK if checks and all(c.ok for c in checks) else EXIT_FAILED


if __name__ == "__main__":
    sys.exit(main())
