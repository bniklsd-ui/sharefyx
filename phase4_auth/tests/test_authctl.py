"""Tests für `scripts/authctl.py` (Plan §5 Step 7) — fünf dünne Unterbefehle gegen eine echte,
temporäre `AuthStore` (nie den echten Auth-DB-Pfad). `main(argv, env=...)` nimmt ein injiziertes
Environment entgegen (gleiches Muster wie `now_fn`/`load_map` anderswo im Repo) — kein Test hier
liest `os.environ`.
"""
from __future__ import annotations

import importlib.util
from datetime import datetime, timezone
from pathlib import Path

import pytest

from authserver.ratelimit import LoginThrottle, MAX_FAILURES
from authserver.store import AuthStore

REPO_ROOT = Path(__file__).resolve().parents[2]


def _load_script(name: str):
    """Lädt ein Skript aus `phase4_auth/scripts/` per Pfad — dieselbe Begründung wie
    `test_users.py :: _load_script`: die Skripte liegen in keinem Python-Paket."""
    script_path = REPO_ROOT / "phase4_auth" / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


authctl = _load_script("authctl")


@pytest.fixture
def db_path(tmp_path) -> Path:
    return tmp_path / "auth.sqlite3"


@pytest.fixture
def env(db_path) -> dict[str, str]:
    return {"SPACE_AUTH_DB": str(db_path)}


@pytest.fixture
def store(db_path) -> AuthStore:
    """Eine zweite `AuthStore`-Verbindung auf dieselbe Datei — zum Seeden vor bzw. Verifizieren
    nach einem `authctl.main()`-Aufruf, echte Zeit (kein eingefrorener Clock nötig für diese
    einfachen CRUD-Prüfungen)."""
    return AuthStore(db_path, now_fn=lambda: datetime.now(timezone.utc))


def test_missing_db_path_aborts_with_message(capsys):
    rc = authctl.main(["list-clients"], env={})
    assert rc == 1
    assert "SPACE_AUTH_DB" in capsys.readouterr().err


def test_list_clients_empty_store(env, capsys):
    rc = authctl.main(["list-clients"], env=env)
    assert rc == 0
    assert "Keine registrierten Clients." in capsys.readouterr().out


def test_list_clients_reports_registered_client(env, store, capsys):
    client = store.create_client(
        client_name="oauth_smoke", application_type="web", redirect_uris=["https://claude.ai/cb"]
    )

    rc = authctl.main(["list-clients"], env=env)

    out = capsys.readouterr().out
    assert rc == 0
    assert client.client_id in out
    assert "oauth_smoke" in out


def test_list_tokens_filters_by_space(env, store, capsys):
    store.create_family(space="niklas", client_id="c1", scope="space", resource="https://x/mcp")
    store.create_family(space="fabian", client_id="c1", scope="space", resource="https://x/mcp")

    rc = authctl.main(["list-tokens", "--space", "niklas"], env=env)

    out = capsys.readouterr().out
    assert rc == 0
    assert "niklas" in out
    assert "fabian" not in out


def test_list_tokens_shows_revoked_status(env, store, capsys):
    family_id = store.create_family(
        space="niklas", client_id="c1", scope="space", resource="https://x/mcp"
    )
    store.revoke_family(family_id, "incident")

    rc = authctl.main(["list-tokens"], env=env)

    out = capsys.readouterr().out
    assert rc == 0
    assert "widerrufen" in out
    assert "incident" in out


def test_revoke_kills_the_family(env, store, capsys):
    family_id = store.create_family(
        space="niklas", client_id="c1", scope="space", resource="https://x/mcp"
    )
    access, _refresh = store.issue_token_pair(family_id, access_ttl_s=3600, refresh_ttl_s=2_592_000)

    rc = authctl.main(["revoke", "--family-id", family_id], env=env)

    out = capsys.readouterr().out
    assert rc == 0
    assert "2 Token(s) widerrufen" in out
    assert store.lookup_access_token(access) is None


def test_revoke_unknown_family_is_a_no_op(env, capsys):
    rc = authctl.main(["revoke", "--family-id", "does-not-exist"], env=env)

    out = capsys.readouterr().out
    assert rc == 0
    assert "0 Token(s) widerrufen" in out


def test_unlock_clears_an_active_lockout(env, store, capsys):
    throttle = LoginThrottle(store, now_fn=lambda: datetime.now(timezone.utc))
    for _ in range(MAX_FAILURES):
        throttle.register_failure("niklas")
    assert throttle.check("niklas") is not None  # sanity: wirklich gesperrt

    rc = authctl.main(["unlock", "--space", "niklas"], env=env)

    assert rc == 0
    assert "aufgehoben" in capsys.readouterr().out
    assert throttle.check("niklas") is None


def test_purge_expired_reports_a_count(env, capsys):
    # Ein abgelaufener Auth-Request, mit einem eingefrorenen Clock in der Vergangenheit angelegt
    # — echte Zeit beim `authctl`-Aufruf sieht ihn dadurch garantiert als abgelaufen.
    past = datetime(2020, 1, 1, tzinfo=timezone.utc)
    seed_store = AuthStore(
        Path(env["SPACE_AUTH_DB"]), now_fn=lambda: past
    )
    seed_store.create_auth_request(
        client_id="c1", redirect_uri="https://claude.ai/cb", state=None,
        code_challenge="chal", scope="space", resource=None, ttl_s=60,
    )

    rc = authctl.main(["purge-expired"], env=env)

    out = capsys.readouterr().out
    assert rc == 0
    assert "abgelaufene Zeile(n) entfernt" in out
    assert "auth_requests" in out
