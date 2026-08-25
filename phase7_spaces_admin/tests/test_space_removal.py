"""Tests für den zweiphasigen Space-Entfernen-Algorithmus (P7 Step C4, `docs/concepts/
phase7_spaces_admin_plan.md` §4.C4) — `DELETE /api/v1/spaces/{space}`.

Eigene Fixtures statt geteiltem `conftest.py`, dieselbe Isolationsdisziplin wie
`test_space_admin_api.py`/`test_acl_write.py` (`phase7_spaces_admin/tests/` ist kein Nachfahre
von `phase5_ui/tests/conftest.py`). `item_store` läuft hier bewusst mit `git=True` (anders als
`test_space_admin_api.py`s `git=False`) — die Abnahmezeilen dieses Steps hängen an der Anzahl
und Reihenfolge der Git-Commits (zwei je Item, genau ein `remove-space`-Commit, P7-O).
"""
from __future__ import annotations

import subprocess
from datetime import datetime, timedelta, timezone

import httpx
import pytest
from authserver import passwords, totp
from authserver.secretbox import KEY_LEN, seal
from authserver.store import AuthStore
from authserver.userdir import UserDirectory
from mcpserver.permissions import SharePolicy
from starlette.applications import Starlette
from storage.store import ConflictError, Store

from webui.api import api_routes
from webui.config import UiSettings
from webui.routes_auth import ui_auth_routes
from webui.sessions import SessionManager

BASE_URL = "https://space.example.ts.net"
SPACE = "niklas"
PASSWORD = "correct horse battery staple"
TOTP_SECRET = totp.generate_secret()

import re

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


def _commit_subjects(data_root) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(data_root), "log", "--format=%s", "--reverse"],
        capture_output=True, text=True,
    )
    return result.stdout.splitlines()


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
    return Store(data_root, git=True)


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


def _team_space(item_store):
    """Ein per `.share.yml` an `SPACE` freigegebener, aber selbst kein Principal -- der einzige
    Space-Typ, den `SPACE` (P7-K: Home-Spaces sind ausgenommen) laut Plan überhaupt entfernen
    darf."""
    from storage import acl
    (item_store.data_root / "team").mkdir()
    acl.add_member(item_store.data_root, "team", SPACE, write=True)
    return "team"


async def _remove_space(client, csrf, space, *, totp_code=None, confirm=None):
    body = {}
    if confirm is not None:
        body["confirm"] = confirm
    if totp_code is not None:
        body.update({"password": PASSWORD, "totp": totp_code()})
    return await client.request(
        "DELETE", f"/api/v1/spaces/{space}", json=body, headers=_headers(csrf),
    )


@pytest.mark.asyncio
async def test_removal_blocked_by_one_unwritable_item_moves_nothing(
    app, item_store, permissions, totp_code, clock, monkeypatch,
):
    # Unter der aktuellen Union-ACL-Semantik (`AclReader.grants_for_dir()`) macht ein
    # Space-Root-Write-Grant automatisch jedes Item darin schreibbar — der P7-L-Gate allein
    # kann diesen Fall also nie live erzeugen. Der Vorlauf-Check ist trotzdem kein toter Code:
    # er ist die zweite, unabhängige Absicherung gegen genau die Divergenz, die N9 fürchtet
    # (Gate und Vorlauf-Scan könnten künftig auseinanderlaufen). Hier direkt simuliert, statt
    # eine mit den bestehenden ACL-Primitiven ohnehin unerreichbare Datenlage nachzubauen.
    _team_space(item_store)
    a = item_store.create("team", type="note", title="A")
    b = item_store.create("team", type="note", title="B")

    original = permissions.can_write_item_as_human

    def _deny_first(actor, acl_decision):
        if acl_decision.space == "team" and _deny_first.first:
            _deny_first.first = False
            return False
        return original(actor, acl_decision)
    _deny_first.first = True
    monkeypatch.setattr(permissions, "can_write_item_as_human", _deny_first)

    async with _client(app) as client:
        csrf = await _login(client, totp_code)
        clock.advance(31)
        response = await _remove_space(
            client, csrf, "team", totp_code=totp_code, confirm="team",
        )
    assert response.status_code == 403
    assert len(response.json()["detail"]["blockers"]) == 1
    assert (item_store.data_root / "team").is_dir()
    assert item_store.get(a.id).space == "team"
    assert item_store.get(b.id).space == "team"


@pytest.mark.asyncio
async def test_removal_blocked_by_an_already_archived_item_moves_nothing(app, item_store, totp_code, clock):
    # Empirischer Advisor-Fund: `store.search()` zählt archivierte Items mit (`total` schließt sie
    # ein), aber `store.move()` verbietet sie explizit ("ist archiviert — move verboten").
    # Ohne diesen Riegel hätte ein `ValidationError` mitten im Durchlauf einen unbehandelten
    # 500 ausgelöst -- nach bereits verschobenen Items, ohne den von N9 verlangten Bericht.
    # Fail-closed VOR jedem Schreibvorgang ist die einzige Option, solange der Store keine
    # Move-Variante für archivierte Items kennt (Nikinger-Entscheidung offen, siehe Kommentar
    # in `_spaces_delete`).
    _team_space(item_store)
    active = item_store.create("team", type="note", title="Aktiv")
    old = item_store.create("team", type="note", title="Alt")
    item_store.archive(old.id, version=old.version)

    async with _client(app) as client:
        csrf = await _login(client, totp_code)
        clock.advance(31)
        response = await _remove_space(
            client, csrf, "team", totp_code=totp_code, confirm="team",
        )
    assert response.status_code == 403
    assert response.json()["detail"]["archived_blockers"] == [old.id]
    assert (item_store.data_root / "team").is_dir()
    assert item_store.get(active.id).space == "team"
    assert item_store.get(old.id).space == "team"


@pytest.mark.asyncio
async def test_removal_clean_run_moves_and_archives_every_item(app, item_store, totp_code, clock):
    _team_space(item_store)
    a = item_store.create("team", type="note", title="A")
    b = item_store.create("team", type="note", title="B")

    async with _client(app) as client:
        csrf = await _login(client, totp_code)
        clock.advance(31)
        response = await _remove_space(
            client, csrf, "team", totp_code=totp_code, confirm="team",
        )
    assert response.status_code == 200
    assert response.json() == {"removed": "team", "archived": 2, "orphan_refs": []}
    for item in (a, b):
        moved = item_store.get(item.id)
        assert moved.space == SPACE
        assert moved.status == "archived"
        archived_path = item_store.data_root / SPACE / "_archive"
        assert any(archived_path.glob(f"{item.id}__*"))


@pytest.mark.asyncio
async def test_removal_moves_the_asset_directory_along(app, item_store, totp_code, clock):
    _team_space(item_store)
    item = item_store.create("team", type="note", title="Mit Bild")
    item_store.put_asset(item.id, filename="pic.png", data=b"\x89PNG\r\n\x1a\n" + b"0" * 20)

    async with _client(app) as client:
        csrf = await _login(client, totp_code)
        clock.advance(31)
        response = await _remove_space(
            client, csrf, "team", totp_code=totp_code, confirm="team",
        )
    assert response.status_code == 200
    assets = item_store.list_assets(item.id)
    assert len(assets) == 1
    assert item_store.get(item.id).space == SPACE


@pytest.mark.asyncio
async def test_removal_produces_two_commits_per_item_and_one_removal_commit(app, item_store, totp_code, clock):
    _team_space(item_store)
    item_store.create("team", type="note", title="A")
    item_store.create("team", type="note", title="B")

    async with _client(app) as client:
        csrf = await _login(client, totp_code)
        clock.advance(31)
        response = await _remove_space(
            client, csrf, "team", totp_code=totp_code, confirm="team",
        )
    assert response.status_code == 200
    subjects = _commit_subjects(item_store.data_root)
    move_commits = [s for s in subjects if s.startswith("move ")]
    archive_commits = [s for s in subjects if s.startswith("archive ")]
    remove_commits = [s for s in subjects if s == "remove-space team"]
    assert len(move_commits) == 2
    assert len(archive_commits) == 2
    assert len(remove_commits) == 1


@pytest.mark.asyncio
async def test_removal_deletes_the_space_directory(app, item_store, totp_code, clock):
    _team_space(item_store)
    item_store.create("team", type="note", title="A")

    async with _client(app) as client:
        csrf = await _login(client, totp_code)
        clock.advance(31)
        response = await _remove_space(
            client, csrf, "team", totp_code=totp_code, confirm="team",
        )
    assert response.status_code == 200
    assert not (item_store.data_root / "team").exists()


@pytest.mark.asyncio
async def test_removal_aborts_on_conflict_mid_run_space_stays(app, item_store, totp_code, clock, monkeypatch):
    _team_space(item_store)
    a = item_store.create("team", type="note", title="A")
    b = item_store.create("team", type="note", title="B")

    # `store.search()`s Reihenfolge (newest-first o. Ä.) ist kein für diesen Test relevanter
    # Contract — der zweite in der tatsächlichen Verarbeitungsreihenfolge bekommt den
    # simulierten Konflikt, statt eine Insert-Reihenfolge anzunehmen, die `_spaces_delete`
    # nirgends verspricht.
    processing_order = [item.id for item in item_store.search(space="team").items]
    first_id, second_id = processing_order

    original_move = item_store.move

    def _move_with_conflict(item_id, *, version, space=None, folder=None):
        if item_id == second_id:
            raise ConflictError(second_id, expected_version=version, current=item_store.get(second_id))
        return original_move(item_id, version=version, space=space, folder=folder)

    monkeypatch.setattr(item_store, "move", _move_with_conflict)

    async with _client(app) as client:
        csrf = await _login(client, totp_code)
        clock.advance(31)
        response = await _remove_space(
            client, csrf, "team", totp_code=totp_code, confirm="team",
        )
    assert response.status_code == 409
    detail = response.json()["detail"]
    assert detail["moved"] == [first_id]
    assert detail["remaining"] == [second_id]
    assert (item_store.data_root / "team").is_dir()
    assert item_store.get(first_id).status == "archived"
    assert item_store.get(second_id).status != "archived"


@pytest.mark.asyncio
async def test_home_space_cannot_be_removed(app, totp_code, clock):
    async with _client(app) as client:
        csrf = await _login(client, totp_code)
        clock.advance(31)
        response = await _remove_space(
            client, csrf, SPACE, totp_code=totp_code, confirm=SPACE,
        )
    assert response.status_code == 403
    assert response.json()["error"] == "forbidden"


@pytest.mark.asyncio
async def test_removal_requires_reauth_and_typed_confirmation(app, item_store, totp_code, clock):
    from storage import acl
    (item_store.data_root / "fremd").mkdir()
    acl.add_member(item_store.data_root, "fremd", SPACE, write=True)

    async with _client(app) as client:
        csrf = await _login(client, totp_code)
        no_creds = await _remove_space(client, csrf, "fremd", confirm="fremd")
        assert no_creds.status_code == 403
        assert no_creds.json()["error"] == "reauth_required"

        clock.advance(31)
        wrong_confirm = await _remove_space(
            client, csrf, "fremd", totp_code=totp_code, confirm="not-the-name",
        )
        assert wrong_confirm.status_code == 422
    assert (item_store.data_root / "fremd").is_dir()
