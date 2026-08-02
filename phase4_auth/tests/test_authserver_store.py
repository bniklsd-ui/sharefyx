import hashlib
from datetime import datetime, timedelta, timezone

import pytest

from authserver.store import AuthStore


@pytest.fixture
def clock():
    state = {"now": datetime(2026, 7, 28, 12, 0, 0, tzinfo=timezone.utc)}

    def now_fn():
        return state["now"]

    def advance(seconds=1):
        state["now"] += timedelta(seconds=seconds)

    now_fn.advance = advance
    return now_fn


@pytest.fixture
def store(tmp_path, clock):
    return AuthStore(tmp_path / "auth.sqlite3", now_fn=clock)


def _family(store, *, space="niklas"):
    return store.create_family(space=space, client_id="c1", scope="space", resource="https://x/mcp")


def _code(store, family_id):
    return store.issue_code(
        family_id=family_id, client_id="c1", redirect_uri="https://claude.ai/cb",
        code_challenge="chal", ttl_s=60,
    )


def test_schema_is_created_and_versioned(store, tmp_path):
    import sqlite3

    conn = sqlite3.connect(tmp_path / "auth.sqlite3")
    tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    expected = {
        "schema_meta", "clients", "auth_requests", "token_families", "auth_codes",
        "access_tokens", "refresh_tokens", "login_attempts", "totp_replay", "register_attempts",
    }
    assert expected <= tables
    row = conn.execute("SELECT value FROM schema_meta WHERE key = 'schema_version'").fetchone()
    assert row[0] == "1"
    conn.close()


def test_reopen_is_idempotent(tmp_path, clock):
    path = tmp_path / "auth.sqlite3"
    store1 = AuthStore(path, now_fn=clock)
    client = store1.create_client(
        client_name="c", application_type="web", redirect_uris=["https://claude.ai/cb"]
    )

    store2 = AuthStore(path, now_fn=clock)
    store2.initialise()  # erneuter Aufruf, nicht nur Reconnect — muss ebenfalls klaglos bleiben
    assert store2.get_client(client.client_id) is not None


def test_auth_request_is_single_use(store):
    request_id = store.create_auth_request(
        client_id="c1", redirect_uri="https://claude.ai/cb", state="xyz",
        code_challenge="chal", scope="space", resource="https://x/mcp", ttl_s=600,
    )
    pending = store.consume_auth_request(request_id)
    assert pending is not None
    assert pending.client_id == "c1"
    assert pending.redirect_uri == "https://claude.ai/cb"
    assert store.consume_auth_request(request_id) is None


def test_auth_request_expires(store, clock):
    request_id = store.create_auth_request(
        client_id="c1", redirect_uri="https://claude.ai/cb", state=None,
        code_challenge="chal", scope="space", resource=None, ttl_s=600,
    )
    clock.advance(601)
    assert store.consume_auth_request(request_id) is None


def test_code_is_single_use(store):
    family_id = _family(store)
    code = _code(store, family_id)

    data, replay = store.consume_code(code)
    assert data is not None
    assert replay is False

    data2, _replay2 = store.consume_code(code)
    assert data2 is None


def test_second_code_use_reports_replay(store):
    family_id = _family(store)
    code = _code(store, family_id)
    store.consume_code(code)
    access, _refresh = store.issue_token_pair(family_id, access_ttl_s=3600, refresh_ttl_s=2_592_000)

    data, replay = store.consume_code(code)
    assert data is None
    assert replay is True
    # RFC 9700: der Replay tötet nicht nur den Code, sondern die ganze Familie.
    assert store.lookup_access_token(access) is None


def test_refresh_rotation_returns_new_pair(store):
    family_id = _family(store)
    access, refresh = store.issue_token_pair(family_id, access_ttl_s=3600, refresh_ttl_s=2_592_000)

    result = store.rotate_refresh(refresh, client_id="c1", access_ttl_s=3600, refresh_ttl_s=2_592_000)
    assert result is not None
    new_access, new_refresh = result
    assert new_access != access
    assert new_refresh != refresh
    assert store.lookup_access_token(new_access) is not None


def test_refresh_rejects_wrong_client_id(store):
    """S2 (Sicherheits-Review 2026-07-29): RFC 6749 §6/RFC 9700 verlangen eine
    Client-Identifikation auch beim Refresh — `rotate_refresh()` prüfte `client_id` bisher gar
    nicht."""
    family_id = _family(store)  # client_id="c1"
    _access, refresh = store.issue_token_pair(family_id, access_ttl_s=3600, refresh_ttl_s=2_592_000)

    result = store.rotate_refresh(
        refresh, client_id="other-client", access_ttl_s=3600, refresh_ttl_s=2_592_000
    )
    assert result is None


def test_refresh_wrong_client_id_does_not_revoke_family(store):
    """Die wichtigere Hälfte von S2 (Plan-Wortlaut): ein falscher `client_id` ist kein Replay —
    die Familie muss intakt bleiben, sonst wird der neue Check selbst zu einem Fernauslöser, der
    eine fremde, legitime Familie töten kann."""
    family_id = _family(store)  # client_id="c1"
    _access, refresh = store.issue_token_pair(family_id, access_ttl_s=3600, refresh_ttl_s=2_592_000)

    store.rotate_refresh(refresh, client_id="other-client", access_ttl_s=3600, refresh_ttl_s=2_592_000)

    # Die Familie lebt weiter — der ECHTE Client kann noch normal rotieren.
    result = store.rotate_refresh(refresh, client_id="c1", access_ttl_s=3600, refresh_ttl_s=2_592_000)
    assert result is not None


def test_reused_refresh_reports_replay(store):
    family_id = _family(store)
    _access, refresh = store.issue_token_pair(family_id, access_ttl_s=3600, refresh_ttl_s=2_592_000)

    first = store.rotate_refresh(refresh, client_id="c1", access_ttl_s=3600, refresh_ttl_s=2_592_000)
    assert first is not None
    new_access, _new_refresh = first

    replay_result = store.rotate_refresh(refresh, client_id="c1", access_ttl_s=3600, refresh_ttl_s=2_592_000)
    assert replay_result is None
    # Familie ist jetzt tot — auch der frisch rotierte Access-Token ist weg.
    assert store.lookup_access_token(new_access) is None


def test_revoke_family_kills_access_and_refresh_tokens(store):
    family_id = _family(store)
    access, refresh = store.issue_token_pair(family_id, access_ttl_s=3600, refresh_ttl_s=2_592_000)

    killed = store.revoke_family(family_id, "operator")
    assert killed == 2
    assert store.lookup_access_token(access) is None
    assert store.rotate_refresh(refresh, client_id="c1", access_ttl_s=3600, refresh_ttl_s=2_592_000) is None


def test_list_clients_returns_all_registered_clients(store):
    c1 = store.create_client(client_name="a", application_type="web", redirect_uris=["https://x/cb"])
    c2 = store.create_client(client_name="b", application_type="web", redirect_uris=["https://y/cb"])

    listed = store.list_clients()

    assert {c.client_id for c in listed} == {c1.client_id, c2.client_id}


def test_list_clients_empty_store_returns_empty_list(store):
    assert store.list_clients() == []


def test_list_families_returns_all_by_default(store):
    f1 = _family(store, space="niklas")
    f2 = _family(store, space="fabian")

    listed = store.list_families()

    assert {f.family_id for f in listed} == {f1, f2}


def test_list_families_filters_by_space(store):
    f1 = _family(store, space="niklas")
    _family(store, space="fabian")

    listed = store.list_families(space="niklas")

    assert [f.family_id for f in listed] == [f1]


def test_list_families_reflects_revocation(store):
    """Der Aufrufer (`authctl.py list-tokens`) muss zwischen aktiven und widerrufenen Familien
    unterscheiden können, ohne eine zweite Abfrage zu bauen — `revoked_at`/`revoked_reason` sind
    deshalb Teil des zurückgegebenen `TokenFamily`, nicht nur intern in `store.py` genutzt."""
    family_id = _family(store)
    store.revoke_family(family_id, "operator")

    (listed,) = store.list_families()

    assert listed.revoked_at is not None
    assert listed.revoked_reason == "operator"


def test_lookup_access_token_rejects_expired(store, clock):
    family_id = _family(store)
    access, _refresh = store.issue_token_pair(family_id, access_ttl_s=60, refresh_ttl_s=2_592_000)
    assert store.lookup_access_token(access) is not None
    clock.advance(61)
    assert store.lookup_access_token(access) is None


def test_lookup_access_token_rejects_revoked_family(store):
    family_id = _family(store)
    access, _refresh = store.issue_token_pair(family_id, access_ttl_s=3600, refresh_ttl_s=2_592_000)
    store.revoke_family(family_id, "operator")
    assert store.lookup_access_token(access) is None


def test_no_plaintext_secret_in_database(store, tmp_path):
    request_id = store.create_auth_request(
        client_id="c1", redirect_uri="https://claude.ai/cb", state=None,
        code_challenge="chal", scope="space", resource=None, ttl_s=600,
    )
    store.consume_auth_request(request_id)
    family_id = _family(store)
    code = _code(store, family_id)
    store.consume_code(code)
    access, refresh = store.issue_token_pair(family_id, access_ttl_s=3600, refresh_ttl_s=2_592_000)

    path = tmp_path / "auth.sqlite3"
    raw = path.read_bytes()
    wal_path = tmp_path / "auth.sqlite3-wal"
    if wal_path.exists():
        raw += wal_path.read_bytes()

    for secret in (request_id, code, access, refresh):
        assert secret.encode("ascii") not in raw

    # Positivprobe: der Hash mindestens eines Geheimnisses steht tatsächlich drin — eine reine
    # Abwesenheitsprüfung würde auch bei einem still no-op-gebliebenen Fluss grün laufen.
    assert hashlib.sha256(access.encode("utf-8")).hexdigest().encode("ascii") in raw


def test_purge_expired_leaves_valid_rows(store, clock):
    request_id = store.create_auth_request(
        client_id="c1", redirect_uri="https://claude.ai/cb", state=None,
        code_challenge="chal", scope="space", resource=None, ttl_s=60,
    )
    family_id = _family(store)
    _code(store, family_id)  # abgelaufen lassen, nie konsumiert
    _access, refresh = store.issue_token_pair(family_id, access_ttl_s=60, refresh_ttl_s=120)

    clock.advance(90)  # request/code/access abgelaufen, refresh (120s) noch nicht

    counts = store.purge_expired()
    assert counts["auth_requests"] == 1
    assert counts["auth_codes"] == 1
    assert counts["access_tokens"] == 1
    assert counts["refresh_tokens"] == 0

    assert store.consume_auth_request(request_id) is None  # bereits weg, nicht nur abgelaufen
    assert store.rotate_refresh(refresh, client_id="c1", access_ttl_s=60, refresh_ttl_s=120) is not None


def test_rotate_refresh_after_access_token_purged(store, clock):
    """Regressionstest für den in der Advisor-Review dieser Session gefundenen Absturzmodus:
    `rotate_refresh` darf nicht von einer noch vorhandenen Access-Token-Zeile abhängen. Ein
    Client, der erst nach Ablauf des Access-Tokens (60 min) aber innerhalb der
    Refresh-Gültigkeit (30 d) rotiert, ist der Normalpfad, kein Randfall.
    """
    family_id = _family(store)
    _access, refresh = store.issue_token_pair(family_id, access_ttl_s=60, refresh_ttl_s=2_592_000)
    clock.advance(120)
    store.purge_expired()  # löscht die abgelaufene access_tokens-Zeile
    result = store.rotate_refresh(refresh, client_id="c1", access_ttl_s=3600, refresh_ttl_s=2_592_000)
    assert result is not None
