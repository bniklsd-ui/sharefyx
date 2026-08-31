"""`POST /api/v1/reauth` und das Reauth-Grant (P8-A, schließt P7-24).

Acht Testfälle aus Plan §A1:
1. Grant-Ausgabe mit korrekten Credentials → 200 + Token.
2. Falscher TOTP → 403, Throttle zählt.
3. Batch: 14 rechteerweiternde PATCHes mit demselben Grant → alle 200 (P7-24-Kernfall,
   N=14 entspricht dem Live-Fall, mit dem der Nikinger am 2026-08-31 die
   `LoginThrottle`-Sperre ausgelöst hat).
4. Abgelaufenes Grant (Zeit vorgespult) → Re-Auth-Fehler wie bisher.
5. Grant einer fremden Session → abgelehnt.
6. Regression: derselbe rohe TOTP-Code zweimal → zweiter Request scheitert
   (Anti-Replay unverändert).
7. `reauth_grant` als Feld passiert die `_PATCH_FIELDS`-Whitelist; ein sonstiges unbekanntes
   Feld weiterhin 422.
8. Ohne Session → 401.

Bewusst KEIN Test „dasselbe Grant zweimal benutzen ist OK" — das ist der Zweck des Grants
und wird im Batch-Test (3) implizit mitbewiesen. Tests (3)/(5) zusammen decken die Session-
Bindung ab. Throttle-Counter-Invarianz (Plan §A1, nach 2026-08-31-Nachtrag): der Throttle
wird in `_reauth_post()` EINMAL pro Grant-Ausstellung geprüft — die 14 PATCHes laufen über
`require_share_reauth()`, das den Throttle gar nicht anfasst; Test (3) deckt die
Rate-Limit-Regression implizit mit, weil ein 14-fach-403/429 in einem einzigen Testlauf
unmöglich zu übersehen wäre.
"""
from __future__ import annotations

import re

import httpx
import pytest
from authserver.ratelimit import MAX_FAILURES
from starlette.applications import Starlette

from webui.api import api_routes
from webui.routes_auth import ui_auth_routes

BASE_URL = "https://space.example.ts.net"
SPACE = "niklas"
OTHER_SPACE = "fabian"
PASSWORD = "correct horse battery staple"

_CSRF_RE = re.compile(r'name="csrf" value="([^"]+)"')


def _client(app) -> httpx.AsyncClient:
    return httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=BASE_URL)


async def _login(client: httpx.AsyncClient, totp_code) -> str:
    response = await client.post(
        "/ui/login", data={"space": SPACE, "password": PASSWORD, "totp": totp_code()},
    )
    assert response.status_code == 200, response.text
    return _CSRF_RE.search(response.text).group(1)


def _headers(csrf: str) -> dict[str, str]:
    return {"Origin": BASE_URL, "X-CSRF-Token": csrf}


# ---------------------------------------------------------------------------------------------
# 1) Grant-Ausgabe mit korrekten Credentials → 200 + Token.
# ---------------------------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_reauth_with_correct_credentials_returns_a_grant_token(
    full_app_items, totp_code, clock,
):
    async with _client(full_app_items) as client:
        csrf = await _login(client, totp_code)
        clock.advance(31)  # neues TOTP-Fenster, sonst Anti-Replay vom Login
        response = await client.post(
            "/api/v1/reauth",
            json={"password": PASSWORD, "totp": totp_code()},
            headers=_headers(csrf),
        )
    assert response.status_code == 200, response.text
    body = response.json()
    assert isinstance(body["grant"], str) and len(body["grant"]) > 20
    assert body["expires_in"] == 90


# ---------------------------------------------------------------------------------------------
# 2) Falscher TOTP → 403, Throttle zählt.
# ---------------------------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_reauth_with_wrong_totp_fails_and_counts_against_the_throttle(
    full_app_items, totp_code, clock,
):
    async with _client(full_app_items) as client:
        csrf = await _login(client, totp_code)
        clock.advance(31)
        # MAX_FAILURES Fehlversuche gehen alle als 403 durch, der MAX_FAILURES+1-te wird
        # gesperrt. Die Zählung teilt sich mit dem UI-/OAuth-Login — derselbe Throttle.
        for i in range(MAX_FAILURES):
            response = await client.post(
                "/api/v1/reauth",
                json={"password": PASSWORD, "totp": "000000"},
                headers=_headers(csrf),
            )
            assert response.status_code == 403, (i, response.text)
        # Ein Versuch mehr → 429.
        response = await client.post(
            "/api/v1/reauth",
            json={"password": PASSWORD, "totp": "000000"},
            headers=_headers(csrf),
        )
        assert response.status_code == 429


# ---------------------------------------------------------------------------------------------
# 3) Batch: 14 rechteerweiternde PATCHes mit demselben Grant → alle 200 (P7-24-Kernfall,
#    N=14 entspricht dem Live-Fall).
# ---------------------------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_fourteen_widening_patches_with_one_grant_all_succeed(
    full_app_items, item_store, totp_code, clock,
):
    """Genau P7-24: vor dem Fix brauchte der User N verschiedene TOTP-Codes für N Items;
    mit dem Grant reicht EIN Code für alle N, derselbe TOTP wird durch das Grant nicht
    erneut verbraucht (Anti-Replay bleibt intakt — siehe Test 6).

    N=14 ist nicht willkürlich: am 2026-08-31 hat der Nikinger genau diesen Versuch live
    ausgelöst und dabei die `LoginThrottle`-Sperre getriggert (Rapid-Fire-Folge
    unterschiedlicher TOTP-Codes). Der Test mit N=14 ist die direkte Regressionsprobe —
    die hier nicht durch 14 verschiedene TOTP-Codes läuft, sondern durch EIN Grant für
    14 PATCHes, also genau das Verhalten, das der Fix herstellt. Ein 14-fach-Fehler in
    diesem einen Test wäre sofort sichtbar."""
    items = [
        item_store.create(SPACE, type="note", title=f"Original {i}") for i in range(14)
    ]
    async with _client(full_app_items) as client:
        csrf = await _login(client, totp_code)
        clock.advance(31)
        # TOTP-Code einmal holen, EINMAL für /api/v1/reauth verbrauchen.
        code = totp_code()
        grant_response = await client.post(
            "/api/v1/reauth",
            json={"password": PASSWORD, "totp": code},
            headers=_headers(csrf),
        )
        assert grant_response.status_code == 200, grant_response.text
        grant = grant_response.json()["grant"]

        for item in items:
            response = await client.patch(
                f"/api/v1/items/{item.id}",
                json={"version": item.version, "share_write": [OTHER_SPACE], "reauth_grant": grant},
                headers=_headers(csrf),
            )
            assert response.status_code == 200, (item.id, response.text)
            assert response.json()["share_write"] == [OTHER_SPACE]


# ---------------------------------------------------------------------------------------------
# 4) Abgelaufenes Grant (Zeit vorgespult) → Re-Auth-Fehler wie bisher.
# ---------------------------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_expired_grant_returns_reauth_required(
    full_app_items, item_store, totp_code, clock,
):
    item = item_store.create(SPACE, type="note", title="Original")
    async with _client(full_app_items) as client:
        csrf = await _login(client, totp_code)
        clock.advance(31)
        grant_response = await client.post(
            "/api/v1/reauth",
            json={"password": PASSWORD, "totp": totp_code()},
            headers=_headers(csrf),
        )
        grant = grant_response.json()["grant"]
        # Grant-TTL ist 90 s — sicher über die 90 hinaus vorspulen.
        clock.advance(120)
        response = await client.patch(
            f"/api/v1/items/{item.id}",
            json={"version": item.version, "share_write": [OTHER_SPACE], "reauth_grant": grant},
            headers=_headers(csrf),
        )
    assert response.status_code == 403
    assert response.json()["error"] == "reauth_required"
    assert item_store.get(item.id).version == item.version  # kein stiller Teil-Schreibvorgang


# ---------------------------------------------------------------------------------------------
# 5) Grant einer fremden Session → abgelehnt.
# ---------------------------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_grant_from_a_different_session_is_rejected(
    full_app_items, item_store, totp_code, clock,
):
    """Login in zwei getrennten Clients = zwei verschiedene Session-Hashes. Ein in Client A
    ausgestelltes Grant darf in Client B nicht funktionieren — sonst wäre die
    Session-Bindung wertlos."""
    app = full_app_items
    item = item_store.create(SPACE, type="note", title="Original")

    async with _client(app) as client_a, _client(app) as client_b:
        csrf_a = await _login(client_a, totp_code)
        # zweites Login braucht ein neues TOTP-Fenster (sonst Replay-Ablehnung am Server)
        clock.advance(31)
        csrf_b = await _login(client_b, totp_code)
        clock.advance(31)

        grant_response = await client_a.post(
            "/api/v1/reauth",
            json={"password": PASSWORD, "totp": totp_code()},
            headers=_headers(csrf_a),
        )
        grant = grant_response.json()["grant"]

        # Grant aus Client A an Item-PATCH in Client B → muss abgelehnt werden.
        response = await client_b.patch(
            f"/api/v1/items/{item.id}",
            json={"version": item.version, "share_write": [OTHER_SPACE], "reauth_grant": grant},
            headers=_headers(csrf_b),
        )
    assert response.status_code == 403
    assert response.json()["error"] == "reauth_required"
    assert item_store.get(item.id).version == item.version


# ---------------------------------------------------------------------------------------------
# 6) Regression: derselbe rohe TOTP-Code zweimal → zweiter Request scheitert
#    (Anti-Replay unverändert).
# ---------------------------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_same_totp_code_twice_via_reauth_endpoint_still_replays(
    full_app_items, totp_code, clock,
):
    """/api/v1/reauth teilt sich `verify_reauth()` mit allen anderen Pfaden — ein zweiter
    Aufruf mit demselben TOTP-Code muss vom Anti-Replay-Schutz genau wie der UI-Login
    abgelehnt werden. Das ist der entscheidende Unterschied zu „ein Grant, viele PATCHes":
    das GRANT darf wiederverwendet werden, der TOTP-Code nicht."""
    async with _client(full_app_items) as client:
        csrf = await _login(client, totp_code)
        clock.advance(31)
        code = totp_code()
        first = await client.post(
            "/api/v1/reauth",
            json={"password": PASSWORD, "totp": code},
            headers=_headers(csrf),
        )
        second = await client.post(
            "/api/v1/reauth",
            json={"password": PASSWORD, "totp": code},
            headers=_headers(csrf),
        )
    assert first.status_code == 200
    assert second.status_code == 403
    assert second.json()["error"] == "reauth_required"


# ---------------------------------------------------------------------------------------------
# 7) `reauth_grant` als Feld passiert die `_PATCH_FIELDS`-Whitelist; ein sonstiges unbekanntes
#    Feld weiterhin 422.
# ---------------------------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_reauth_grant_field_passes_the_patch_whitelist(
    full_app_items, item_store, totp_code, clock,
):
    item = item_store.create(SPACE, type="note", title="Original")
    async with _client(full_app_items) as client:
        csrf = await _login(client, totp_code)
        clock.advance(31)
        grant_response = await client.post(
            "/api/v1/reauth",
            json={"password": PASSWORD, "totp": totp_code()},
            headers=_headers(csrf),
        )
        grant = grant_response.json()["grant"]
        # Whitelist-Test: ein PATCH mit `reauth_grant` als einzigem ungewöhnlichen Feld ist OK
        # (kein 422). Die Änderung ist hier nur `title` — keine Rechteerweiterung, das Grant
        # wird gar nicht gebraucht, der Test zielt nur auf die Whitelist.
        ok = await client.patch(
            f"/api/v1/items/{item.id}",
            json={"version": item.version, "title": "Neu", "reauth_grant": grant},
            headers=_headers(csrf),
        )
        # Beliebiges anderes Feld → 422 wie bisher (kein Aufweichen der O6-Whitelist).
        bad = await client.patch(
            f"/api/v1/items/{item.id}",
            json={"version": item.version, "irgendwas_anderes": 42},
            headers=_headers(csrf),
        )
    assert ok.status_code == 200, ok.text
    assert bad.status_code == 422
    assert bad.json()["error"] == "validation_failed"


# ---------------------------------------------------------------------------------------------
# 8) Ohne Session → 401.
# ---------------------------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_reauth_without_session_is_unauthorized(full_app_items):
    async with _client(full_app_items) as client:
        response = await client.post(
            "/api/v1/reauth",
            json={"password": PASSWORD, "totp": "000000"},
            headers={"Origin": BASE_URL, "X-CSRF-Token": "egal"},
        )
    assert response.status_code == 401
    assert response.json()["error"] == "unauthenticated"
