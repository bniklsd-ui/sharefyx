"""Tests für die vier Space-Verwaltungs-Routen aus P7 Step C2 (`docs/concepts/
phase7_spaces_admin_plan.md` §4.C2) — `POST /api/v1/spaces`, `GET/POST .../members`,
`DELETE .../members/{name}`. `DELETE /api/v1/spaces/{space}` (Entfernen) ist bewusst NICHT
hier — sein Vorlauf/Durchlauf-Algorithmus ist Step C4.

Eigene Fixtures statt `phase5_ui/tests/conftest.py`s `full_app_items` & Co.: `conftest.py`-
Dateien werden nur entlang des Verzeichnisbaums des Testfiles selbst eingesammelt,
`phase7_spaces_admin/tests/` ist kein Nachfahre von `phase5_ui/tests/` — dieselbe Isolation wie
`test_acl_write.py`/`test_testcred.py`, hier auf eine echte In-Process-App angewendet statt auf
`storage.acl` direkt. Fixtures/Helfer sind absichtlich eine Teilmenge von `phase5_ui/tests/
conftest.py` + `test_api.py`s Modul-Helfern (`_client`/`_login`/`_headers`), nicht neu erfunden.
"""
from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone

import httpx
import pytest
from authserver import passwords, totp
from authserver.ratelimit import LoginThrottle
from authserver.secretbox import KEY_LEN, seal
from authserver.store import AuthStore
from authserver.userdir import UserDirectory
from mcpserver.permissions import SharePolicy
from starlette.applications import Starlette
from storage.store import Store

from webui.api import api_routes
from webui.config import UiSettings
from webui.routes_auth import ui_auth_routes
from webui.sessions import SessionManager

BASE_URL = "https://space.example.ts.net"
SPACE = "niklas"
PASSWORD = "correct horse battery staple"
TOTP_SECRET = totp.generate_secret()

_CSRF_RE = re.compile(r'name="csrf" value="([^"]+)"')


def _client(app) -> httpx.AsyncClient:
    return httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=BASE_URL)


async def _login(client: httpx.AsyncClient, totp_code) -> str:
    response = await client.post(
        "/ui/login", data={"space": SPACE, "password": PASSWORD, "totp": totp_code()},
    )
    assert response.status_code == 200
    return _CSRF_RE.search(response.text).group(1)


def _headers(csrf: str) -> dict[str, str]:
    return {"Origin": BASE_URL, "X-CSRF-Token": csrf}


@pytest.fixture
def clock():
    state = {"now": datetime(2026, 8, 25, 9, 0, 0, tzinfo=timezone.utc)}

    def now_fn():
        return state["now"]

    def advance(seconds=1):
        state["now"] += timedelta(seconds=seconds)

    now_fn.advance = advance
    return now_fn


@pytest.fixture
def auth_store(tmp_path, clock) -> AuthStore:
    return AuthStore(tmp_path / "auth.sqlite3", now_fn=clock)


@pytest.fixture
def ui_settings() -> UiSettings:
    return UiSettings(base_url=BASE_URL, space_admin_enabled=True)


@pytest.fixture
def dek() -> bytes:
    return bytes([0x5A]) * KEY_LEN


@pytest.fixture
def confirmed_users(auth_store, dek) -> UserDirectory:
    auth_store.upsert_user(
        SPACE,
        password_hash=passwords.hash_password(PASSWORD),
        totp_secret_enc=seal(TOTP_SECRET.encode("ascii"), key=dek, aad=SPACE.encode("utf-8")),
        totp_alg="SHA1",
        totp_confirmed_at=None,
        status="active",
    )
    auth_store.confirm_totp(SPACE)
    return UserDirectory(auth_store, dek=dek)


@pytest.fixture
def sessions(auth_store, ui_settings) -> SessionManager:
    return SessionManager(auth_store, settings=ui_settings)


@pytest.fixture
def item_store(tmp_path) -> Store:
    data_root = tmp_path / "data"
    data_root.mkdir()
    (data_root / SPACE).mkdir()
    return Store(data_root, git=False)


@pytest.fixture
def permissions(item_store) -> SharePolicy:
    return SharePolicy(item_store.acl_reader)


@pytest.fixture
def app(ui_settings, auth_store, confirmed_users, sessions, item_store, permissions) -> Starlette:
    routes = ui_auth_routes(ui_settings, auth_store, confirmed_users, sessions) + api_routes(
        ui_settings, item_store, sessions, permissions, auth_store, confirmed_users,
    )
    return Starlette(routes=routes)


@pytest.fixture
def totp_code(clock):
    def _make(secret: str = TOTP_SECRET) -> str:
        counter = int(clock().timestamp() // 30)
        return totp.totp_at(secret, counter, algo="SHA1")
    return _make


@pytest.fixture
def disabled_app(auth_store, confirmed_users, sessions, item_store, permissions) -> Starlette:
    """Wie `app`, aber `space_admin_enabled=False` — die vier Routen dieses Steps müssen alle
    `404` liefern, solange C3 den Kill-Switch nicht auf `True` dreht (P7-R)."""
    disabled_settings = UiSettings(base_url=BASE_URL, space_admin_enabled=False)
    routes = ui_auth_routes(disabled_settings, auth_store, confirmed_users, sessions) + api_routes(
        disabled_settings, item_store, sessions, permissions, auth_store, confirmed_users,
    )
    return Starlette(routes=routes)


def _share_yml(data_root, space) -> dict:
    import yaml
    path = data_root / space / ".share.yml"
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8"))


# -- Kill-Switch (P7-R), alle vier Routen dieses Steps ---------------------------------------


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "method,path,body",
    [
        ("POST", "/api/v1/spaces", {"name": "dritter"}),
        ("GET", f"/api/v1/spaces/{SPACE}/members", None),
        ("POST", f"/api/v1/spaces/{SPACE}/members", {"name": "fabian"}),
        ("DELETE", f"/api/v1/spaces/{SPACE}/members/fabian", None),
    ],
)
async def test_all_four_routes_404_when_space_admin_disabled(disabled_app, totp_code, method, path, body):
    async with _client(disabled_app) as client:
        csrf = await _login(client, totp_code)
        response = await client.request(method, path, json=body, headers=_headers(csrf))
    assert response.status_code == 404


# -- POST /api/v1/spaces --------------------------------------------------------------------


@pytest.mark.asyncio
async def test_create_space_succeeds(app, item_store, totp_code):
    async with _client(app) as client:
        csrf = await _login(client, totp_code)
        response = await client.post(
            "/api/v1/spaces", json={"name": "dritter"}, headers=_headers(csrf),
        )
    assert response.status_code == 201
    assert (item_store.data_root / "dritter").is_dir()


@pytest.mark.asyncio
async def test_create_space_seeds_the_creator_as_a_write_member(app, item_store, totp_code):
    # Advisor-Fund: ohne diesen Seed war ein frisch angelegter Space für niemanden sichtbar
    # oder verwaltbar -- P7-16 scheiterte genau daran.
    async with _client(app) as client:
        csrf = await _login(client, totp_code)
        await client.post("/api/v1/spaces", json={"name": "dritter"}, headers=_headers(csrf))
    assert _share_yml(item_store.data_root, "dritter") == {"write": [SPACE]}


@pytest.mark.asyncio
async def test_create_space_then_appears_in_the_visible_list_and_is_manageable(app, totp_code):
    async with _client(app) as client:
        csrf = await _login(client, totp_code)
        await client.post("/api/v1/spaces", json={"name": "dritter"}, headers=_headers(csrf))
        spaces_response = await client.get("/api/v1/spaces", headers=_headers(csrf))
        members_response = await client.get("/api/v1/spaces/dritter/members", headers=_headers(csrf))
    assert "dritter" in {s["name"] for s in spaces_response.json()}
    assert members_response.status_code == 200
    assert members_response.json()["manageable"] is True


@pytest.mark.asyncio
async def test_create_space_rejects_known_principal_name(app, confirmed_users, totp_code):
    async with _client(app) as client:
        csrf = await _login(client, totp_code)
        response = await client.post(
            "/api/v1/spaces", json={"name": SPACE}, headers=_headers(csrf),
        )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_space_rejects_reserved_name(app, totp_code):
    async with _client(app) as client:
        csrf = await _login(client, totp_code)
        response = await client.post(
            "/api/v1/spaces", json={"name": "_archive"}, headers=_headers(csrf),
        )
    assert response.status_code == 422


# -- GET .../members --------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_members_reports_manageable_for_a_write_member(app, item_store, totp_code):
    (item_store.data_root / "fremd").mkdir()
    (item_store.data_root / "fremd" / ".share.yml").write_text(f"write: [{SPACE}]\n", encoding="utf-8")
    async with _client(app) as client:
        csrf = await _login(client, totp_code)
        response = await client.get("/api/v1/spaces/fremd/members", headers=_headers(csrf))
    assert response.status_code == 200
    body = response.json()
    assert body["write"] == [SPACE]
    assert body["manageable"] is True
    assert body["home"] is False


@pytest.mark.asyncio
async def test_get_members_reports_not_manageable_with_read_only_grant(app, item_store, totp_code):
    (item_store.data_root / "fremd").mkdir()
    (item_store.data_root / "fremd" / ".share.yml").write_text(f"read: [{SPACE}]\n", encoding="utf-8")
    async with _client(app) as client:
        csrf = await _login(client, totp_code)
        response = await client.get("/api/v1/spaces/fremd/members", headers=_headers(csrf))
    assert response.status_code == 200
    body = response.json()
    assert body["manageable"] is False
    assert body["orphans"] == []


@pytest.mark.asyncio
async def test_get_members_without_any_grant_is_forbidden(app, totp_code):
    async with _client(app) as client:
        csrf = await _login(client, totp_code)
        response = await client.get("/api/v1/spaces/fremd/members", headers=_headers(csrf))
    assert response.status_code == 403
    assert response.json()["error"] == "forbidden"


@pytest.mark.asyncio
async def test_get_members_marks_a_known_principal_as_home(app, totp_code):
    async with _client(app) as client:
        csrf = await _login(client, totp_code)
        response = await client.get(f"/api/v1/spaces/{SPACE}/members", headers=_headers(csrf))
    assert response.status_code == 200
    assert response.json()["home"] is True


@pytest.mark.asyncio
async def test_get_members_reports_a_typo_in_the_share_file_as_orphan(app, item_store, totp_code):
    # Advisor-Fund: `orphans` heißt "Name in read:/write:, der auf kein Space-Verzeichnis mehr
    # zeigt" (spacectl.py check-Semantik), NICHT "wer verweist auf mich" (acl.spaces_referencing).
    (item_store.data_root / SPACE / ".share.yml").write_text("read: [tpyo]\n", encoding="utf-8")
    async with _client(app) as client:
        csrf = await _login(client, totp_code)
        response = await client.get(f"/api/v1/spaces/{SPACE}/members", headers=_headers(csrf))
    assert response.status_code == 200
    assert response.json()["orphans"] == ["tpyo"]


# -- POST .../members (widening, Re-Auth) -----------------------------------------------------


@pytest.mark.asyncio
async def test_add_member_without_credentials_returns_reauth_required(app, totp_code):
    async with _client(app) as client:
        csrf = await _login(client, totp_code)
        response = await client.post(
            f"/api/v1/spaces/{SPACE}/members", json={"name": "fabian"}, headers=_headers(csrf),
        )
    assert response.status_code == 403
    assert response.json()["error"] == "reauth_required"


@pytest.mark.asyncio
async def test_add_member_with_correct_credentials_succeeds_and_writes_the_file(app, item_store, totp_code, clock):
    async with _client(app) as client:
        csrf = await _login(client, totp_code)
        clock.advance(31)
        response = await client.post(
            f"/api/v1/spaces/{SPACE}/members",
            json={"name": "fabian", "write": True, "password": PASSWORD, "totp": totp_code()},
            headers=_headers(csrf),
        )
    assert response.status_code == 200
    assert _share_yml(item_store.data_root, SPACE) == {"write": ["fabian"]}


@pytest.mark.asyncio
async def test_add_member_credentials_never_land_in_the_share_file(app, item_store, totp_code, clock):
    async with _client(app) as client:
        csrf = await _login(client, totp_code)
        clock.advance(31)
        await client.post(
            f"/api/v1/spaces/{SPACE}/members",
            json={"name": "fabian", "password": PASSWORD, "totp": totp_code()},
            headers=_headers(csrf),
        )
    data = _share_yml(item_store.data_root, SPACE)
    assert "password" not in str(data)
    assert PASSWORD not in str(data)


@pytest.mark.asyncio
async def test_add_member_without_write_grant_is_forbidden(app, totp_code):
    async with _client(app) as client:
        csrf = await _login(client, totp_code)
        response = await client.post(
            "/api/v1/spaces/fremd/members", json={"name": "fabian"}, headers=_headers(csrf),
        )
    assert response.status_code == 403
    assert response.json()["error"] == "forbidden"


@pytest.mark.asyncio
async def test_add_member_without_csrf_is_rejected(app, totp_code):
    async with _client(app) as client:
        await _login(client, totp_code)
        response = await client.post(
            f"/api/v1/spaces/{SPACE}/members", json={"name": "fabian"},
        )
    assert response.status_code == 403
    assert response.json()["error"] == "csrf_failed"


@pytest.mark.asyncio
# -- DELETE .../members/{name} (narrowing, kein Re-Auth, P7-N) --------------------------------


@pytest.mark.asyncio
async def test_remove_member_succeeds_without_reauth(app, item_store, totp_code):
    from storage import acl
    acl.add_member(item_store.data_root, SPACE, "fabian", write=False)
    async with _client(app) as client:
        csrf = await _login(client, totp_code)
        response = await client.delete(
            f"/api/v1/spaces/{SPACE}/members/fabian", headers=_headers(csrf),
        )
    assert response.status_code == 200
    assert _share_yml(item_store.data_root, SPACE) == {}


@pytest.mark.asyncio
async def test_remove_member_without_write_grant_is_forbidden(app, item_store, totp_code):
    from storage import acl
    (item_store.data_root / "fremd").mkdir()
    acl.add_member(item_store.data_root, "fremd", "fabian", write=False)
    async with _client(app) as client:
        csrf = await _login(client, totp_code)
        response = await client.delete(
            "/api/v1/spaces/fremd/members/fabian", headers=_headers(csrf),
        )
    assert response.status_code == 403
