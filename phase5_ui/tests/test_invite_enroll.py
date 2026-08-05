"""Einladungs-/Enrollment-Flow (Plan §2.8, §5 Step 4): `GET`/`POST /ui/invite/{token}` →
`POST /ui/enroll/confirm`, gegen eine echte In-Process-`Starlette`-App (nur `ui_auth_routes()` —
der Flow braucht `account_routes()` nicht)."""
from __future__ import annotations

import re
import sqlite3

import httpx
import pytest
from authserver import totp

BASE_URL = "https://space.example.ts.net"
SPACE = "niklas"
NEW_PASSWORD = "correct horse battery staple"

# [2026-08-05, Step 7b] Der Seed steht jetzt in `<code class="auth__seed">` statt in einem
# nackten `<code>` (`pages.py` bekam Klassen-Markup, damit die Auth-Seiten überhaupt gestaltet
# sind). Der Ausdruck ist bewusst weiterhin an das Seed-Element gebunden und nicht an „irgendein
# `<code>`": auf der Recovery-Seite stehen zehn weitere `<code>`-Elemente, und die Aussage
# „genau EINMAL angezeigt" (Zeile 103) wäre mit einem lockereren Ausdruck nicht mehr die
# Aussage, die der Test zu prüfen behauptet.
_SECRET_RE = re.compile(r'<code class="auth__seed">([A-Z0-9 ]+)</code>')
_CSRF_RE = re.compile(r'name="csrf" value="([^"]+)"')
_RECOVERY_CODE_RE = re.compile(r"<code>([A-Za-z0-9-]+)</code>")


def _client(app) -> httpx.AsyncClient:
    return httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=BASE_URL)


@pytest.mark.asyncio
async def test_invite_is_single_use(app, store):
    token = store.create_invite(space=SPACE, purpose="initial", ttl_s=3600)
    async with _client(app) as client:
        first = await client.post(
            f"/ui/invite/{token}", data={"password": NEW_PASSWORD}, headers={"Origin": BASE_URL}
        )
        assert first.status_code == 200

        second = await client.get(f"/ui/invite/{token}")
        assert second.status_code == 404


@pytest.mark.asyncio
async def test_invite_expires(app, store, clock):
    token = store.create_invite(space=SPACE, purpose="initial", ttl_s=60)
    clock.advance(61)
    async with _client(app) as client:
        response = await client.get(f"/ui/invite/{token}")
    assert response.status_code == 404


def test_invite_link_is_printed_once_and_not_stored_plaintext(store, tmp_path, capsys):
    import importlib.util
    from pathlib import Path

    repo_root = Path(__file__).resolve().parents[2]
    spec = importlib.util.spec_from_file_location(
        "authctl", repo_root / "phase4_auth" / "scripts" / "authctl.py"
    )
    authctl = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(authctl)

    db_path = tmp_path / "auth.sqlite3"
    env = {"SPACE_AUTH_DB": str(db_path), "SPACE_PUBLIC_BASE_URL": BASE_URL}
    rc = authctl.main(["invite", SPACE], env=env)
    assert rc == 0

    out = capsys.readouterr().out
    links = [line for line in out.splitlines() if "/ui/invite/" in line]
    assert len(links) == 1
    token = links[0].rsplit("/", 1)[-1]

    conn = sqlite3.connect(db_path)
    try:
        rows = conn.execute("SELECT token_hash FROM invites").fetchall()
    finally:
        conn.close()
    assert len(rows) == 1
    assert token != rows[0][0]
    assert token not in rows[0][0]


@pytest.mark.asyncio
async def test_invite_flow_sets_password_and_starts_totp(app, store, users):
    token = store.create_invite(space=SPACE, purpose="initial", ttl_s=3600)
    async with _client(app) as client:
        response = await client.post(
            f"/ui/invite/{token}", data={"password": NEW_PASSWORD}, headers={"Origin": BASE_URL}
        )
    assert response.status_code == 200

    record = users.get(SPACE)
    assert record is not None
    assert record.totp_secret is not None
    assert record.totp_confirmed is False
    from authserver import passwords
    assert passwords.verify_password(record.password_hash, NEW_PASSWORD)


@pytest.mark.asyncio
async def test_totp_secret_is_shown_exactly_once(app, store):
    token = store.create_invite(space=SPACE, purpose="initial", ttl_s=3600)
    async with _client(app) as client:
        response = await client.post(
            f"/ui/invite/{token}", data={"password": NEW_PASSWORD}, headers={"Origin": BASE_URL}
        )
        assert len(_SECRET_RE.findall(response.text)) == 1

        # Der Token ist jetzt verbraucht — kein zweiter Weg zeigt denselben Klartext-Seed erneut.
        again = await client.get(f"/ui/invite/{token}")
        assert again.status_code == 404


@pytest.mark.asyncio
async def test_totp_confirm_requires_valid_code(app, store, clock):
    token = store.create_invite(space=SPACE, purpose="initial", ttl_s=3600)
    async with _client(app) as client:
        invite_response = await client.post(
            f"/ui/invite/{token}", data={"password": NEW_PASSWORD}, headers={"Origin": BASE_URL}
        )
        secret = _SECRET_RE.search(invite_response.text).group(1).replace(" ", "")
        csrf = _CSRF_RE.search(invite_response.text).group(1)

        wrong = await client.post(
            "/ui/enroll/confirm", data={"code": "000000", "csrf": csrf},
            headers={"Origin": BASE_URL},
        )
        assert wrong.status_code == 422

        counter = int(clock().timestamp() // 30)
        code = totp.totp_at(secret, counter, algo="SHA1")
        right = await client.post(
            "/ui/enroll/confirm", data={"code": code, "csrf": csrf}, headers={"Origin": BASE_URL},
        )
        assert right.status_code == 200


@pytest.mark.asyncio
async def test_enroll_confirm_csrf_failure_offers_a_retry_not_a_dead_end(app, store, clock):
    """Live-Fund des Nikingers, 2026-08-03: ein `require_csrf()`-Fehlschlag (z. B. „Herkunft
    (Origin) stimmt nicht") landete bisher auf `pages.render_error_page()` — einer Sackgasse
    ohne Formular, ohne Zurück; der einzige Ausweg wäre eine neue Einladung gewesen, aber die
    war ja schon verbraucht (Einmal-Token). Jetzt: dieselbe Enrollment-Seite mit Fehlermeldung,
    derselbe QR/Secret, derselbe CSRF-Token bleibt gültig — ein echter zweiter Versuch."""
    token = store.create_invite(space=SPACE, purpose="initial", ttl_s=3600)
    async with _client(app) as client:
        invite_response = await client.post(
            f"/ui/invite/{token}", data={"password": NEW_PASSWORD}, headers={"Origin": BASE_URL}
        )
        secret = _SECRET_RE.search(invite_response.text).group(1).replace(" ", "")
        csrf = _CSRF_RE.search(invite_response.text).group(1)

        wrong_origin = await client.post(
            "/ui/enroll/confirm", data={"code": "000000", "csrf": csrf},
            headers={"Origin": "https://boese.example"},
        )
        assert wrong_origin.status_code == 403
        assert 'action="/ui/enroll/confirm"' in wrong_origin.text
        retry_secret = _SECRET_RE.search(wrong_origin.text)
        assert retry_secret is not None
        assert retry_secret.group(1).replace(" ", "") == secret

        # Derselbe CSRF-Token, jetzt mit korrekter Origin und korrektem Code — muss noch gültig
        # sein, die Sitzung wurde vom CSRF-Fehlschlag nicht widerrufen.
        counter = int(clock().timestamp() // 30)
        code = totp.totp_at(secret, counter, algo="SHA1")
        right = await client.post(
            "/ui/enroll/confirm", data={"code": code, "csrf": csrf}, headers={"Origin": BASE_URL},
        )
        assert right.status_code == 200


@pytest.mark.asyncio
async def test_recovery_codes_are_shown_exactly_once(app, store, clock, users):
    token = store.create_invite(space=SPACE, purpose="initial", ttl_s=3600)
    async with _client(app) as client:
        invite_response = await client.post(
            f"/ui/invite/{token}", data={"password": NEW_PASSWORD}, headers={"Origin": BASE_URL}
        )
        secret = _SECRET_RE.search(invite_response.text).group(1).replace(" ", "")
        csrf = _CSRF_RE.search(invite_response.text).group(1)
        counter = int(clock().timestamp() // 30)
        code = totp.totp_at(secret, counter, algo="SHA1")

        confirm_response = await client.post(
            "/ui/enroll/confirm", data={"code": code, "csrf": csrf}, headers={"Origin": BASE_URL},
        )
    codes = _RECOVERY_CODE_RE.findall(confirm_response.text)
    assert len(codes) == 10
    assert len(set(codes)) == 10
    assert store.count_unused_recovery_codes(SPACE) == 10
