import hashlib
import sqlite3
from datetime import datetime, timedelta, timezone

import pytest

from authserver.store import _SCHEMA, RETENTION_AFTER_REVOKE_OR_CONSUME_S, AuthStore


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
        "users", "invites", "recovery_codes", "ui_sessions",
    }
    assert expected <= tables
    row = conn.execute("SELECT value FROM schema_meta WHERE key = 'schema_version'").fetchone()
    assert row[0] == "2"
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


def test_revoke_families_for_space_kills_all_active_ones(store):
    """P5-Q (Plan §0.5): ein Passwortwechsel widerruft ALLE Token-Familien des Space —
    Gegenstück zu `revoke_sessions_for_space()`."""
    f1 = _family(store, space="niklas")
    f2 = _family(store, space="niklas")
    foreign = _family(store, space="fabian")

    killed = store.revoke_families_for_space("niklas", "password_changed")

    assert killed == 2
    by_id = {f.family_id: f for f in store.list_families()}
    assert by_id[f1].revoked_at is not None
    assert by_id[f1].revoked_reason == "password_changed"
    assert by_id[f2].revoked_at is not None
    assert by_id[foreign].revoked_at is None


def test_revoke_families_for_space_skips_already_revoked(store):
    """Zweiter Aufruf widerruft nichts mehr — dieselbe `revoked_at IS NULL`-Disziplin wie
    `revoke_family()` (ein zweiter Widerruf überschreibt nicht den ursprünglichen Grund)."""
    _family(store, space="niklas")
    store.revoke_families_for_space("niklas", "password_changed")

    killed_again = store.revoke_families_for_space("niklas", "second_call")

    assert killed_again == 0


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


# -- Schema 2 (P5 Step 2) --------------------------------------------------------------------


def test_schema_migrates_from_v1_to_v2_without_data_loss(tmp_path, clock):
    """Baut eine echte Schema-1-Datenbank von Hand (nur `_SCHEMA`, kein `_SCHEMA_V2`, wie eine
    reale P4-Instanz sie hinterlassen hätte), füllt eine Zeile, öffnet sie danach über den
    normalen `AuthStore`-Konstruktor (führt beide Schemata + den Versions-Bump aus) und prüft:
    die alte Zeile lebt weiter, die vier neuen Tabellen existieren, `schema_version` steht auf
    `"2"`."""
    path = tmp_path / "auth.sqlite3"
    conn = sqlite3.connect(path)
    conn.executescript(_SCHEMA)
    conn.execute(
        "INSERT OR IGNORE INTO schema_meta (key, value) VALUES ('schema_version', '1')"
    )
    conn.execute(
        "INSERT INTO clients (client_id, client_name, application_type, redirect_uris, "
        "created_at, last_used_at) VALUES ('c1', 'Alt-Client', 'web', '[\"https://x/cb\"]', "
        "'2026-01-01T00:00:00Z', NULL)"
    )
    conn.commit()
    conn.close()

    store = AuthStore(path, now_fn=clock)

    assert store.get_client("c1") is not None
    assert store.get_client("c1").client_name == "Alt-Client"

    conn2 = sqlite3.connect(path)
    tables = {row[0] for row in conn2.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert {"users", "invites", "recovery_codes", "ui_sessions"} <= tables
    version = conn2.execute(
        "SELECT value FROM schema_meta WHERE key = 'schema_version'"
    ).fetchone()[0]
    assert version == "2"
    conn2.close()


def test_schema_version_is_two_after_initialise(store, tmp_path):
    conn = sqlite3.connect(tmp_path / "auth.sqlite3")
    version = conn.execute(
        "SELECT value FROM schema_meta WHERE key = 'schema_version'"
    ).fetchone()[0]
    assert version == "2"
    conn.close()


def test_upsert_and_get_user_roundtrip(store, clock):
    assert store.get_user("niklas") is None
    store.upsert_user(
        "niklas", password_hash="$argon2id$...", totp_secret_enc=b"\x01\x02",
        totp_alg="SHA1", totp_confirmed_at=clock(), status="active",
    )
    row = store.get_user("niklas")
    assert row is not None
    assert row.password_hash == "$argon2id$..."
    assert row.totp_secret_enc == b"\x01\x02"
    assert row.totp_alg == "SHA1"
    assert row.totp_confirmed_at == clock()
    assert row.status == "active"
    assert row.password_changed_at is None  # upsert_user setzt es bewusst nicht


def test_upsert_user_preserves_created_at_on_conflict(store, clock):
    store.upsert_user(
        "niklas", password_hash="h1", totp_secret_enc=None, totp_alg="SHA1",
        totp_confirmed_at=None, status="active",
    )
    first_created_at = store.get_user("niklas").created_at

    clock.advance(3600)
    store.upsert_user(
        "niklas", password_hash="h2", totp_secret_enc=b"\x99", totp_alg="SHA1",
        totp_confirmed_at=None, status="active",
    )
    row = store.get_user("niklas")
    assert row.password_hash == "h2"
    assert row.created_at == first_created_at


def test_list_users_returns_all(store):
    store.upsert_user(
        "niklas", password_hash="h1", totp_secret_enc=None, totp_alg="SHA1",
        totp_confirmed_at=None, status="active",
    )
    store.upsert_user(
        "fabian", password_hash="h2", totp_secret_enc=None, totp_alg="SHA1",
        totp_confirmed_at=None, status="active",
    )
    assert {row.space for row in store.list_users()} == {"niklas", "fabian"}


def test_set_password_updates_password_changed_at(store, clock):
    store.upsert_user(
        "niklas", password_hash="old", totp_secret_enc=None, totp_alg="SHA1",
        totp_confirmed_at=None, status="active",
    )
    assert store.get_user("niklas").password_changed_at is None

    store.set_password_hash("niklas", "new")
    row = store.get_user("niklas")
    assert row.password_hash == "new"
    assert row.password_changed_at == clock()


def test_set_totp_clears_confirmed_at(store, clock):
    store.upsert_user(
        "niklas", password_hash="h", totp_secret_enc=b"\x01", totp_alg="SHA1",
        totp_confirmed_at=clock(), status="active",
    )
    store.set_totp("niklas", secret_enc=b"\x02\x02", alg="SHA256")
    row = store.get_user("niklas")
    assert row.totp_secret_enc == b"\x02\x02"
    assert row.totp_alg == "SHA256"
    assert row.totp_confirmed_at is None


def test_confirm_totp_sets_timestamp(store, clock):
    store.upsert_user(
        "niklas", password_hash="h", totp_secret_enc=b"\x01", totp_alg="SHA1",
        totp_confirmed_at=None, status="active",
    )
    store.confirm_totp("niklas")
    assert store.get_user("niklas").totp_confirmed_at == clock()


def test_set_user_status(store):
    store.upsert_user(
        "niklas", password_hash="h", totp_secret_enc=None, totp_alg="SHA1",
        totp_confirmed_at=None, status="active",
    )
    store.set_user_status("niklas", "disabled")
    assert store.get_user("niklas").status == "disabled"


def test_invite_is_single_use(store):
    token = store.create_invite(space="niklas", purpose="initial", ttl_s=3600)
    peeked = store.peek_invite(token)
    assert peeked is not None
    assert peeked.space == "niklas"
    assert peeked.purpose == "initial"
    assert peeked.consumed_at is None

    consumed = store.consume_invite(token)
    assert consumed is not None
    assert consumed.consumed_at is not None

    assert store.peek_invite(token) is None
    assert store.consume_invite(token) is None


def test_invite_expires(store, clock):
    token = store.create_invite(space="niklas", purpose="reset", ttl_s=60)
    clock.advance(61)
    assert store.peek_invite(token) is None
    assert store.consume_invite(token) is None


def test_revoke_invites_for_space_only_touches_own_unconsumed_ones(store):
    own_pending = store.create_invite(space="niklas", purpose="reset", ttl_s=3600)
    own_consumed = store.create_invite(space="niklas", purpose="reset", ttl_s=3600)
    store.consume_invite(own_consumed)
    foreign = store.create_invite(space="fabian", purpose="reset", ttl_s=3600)

    killed = store.revoke_invites_for_space("niklas")

    assert killed == 1  # nur der eine noch offene, nicht der bereits konsumierte
    assert store.peek_invite(own_pending) is None
    assert store.peek_invite(foreign) is not None


def test_recovery_codes_replace_and_consume(store):
    store.replace_recovery_codes("niklas", ["aaaa-bbbb-c", "dddd-eeee-f"])
    assert store.count_unused_recovery_codes("niklas") == 2

    assert store.consume_recovery_code("niklas", "aaaa-bbbb-c") is True
    assert store.count_unused_recovery_codes("niklas") == 1
    # ein zweites Mal derselbe Code: schon verbraucht
    assert store.consume_recovery_code("niklas", "aaaa-bbbb-c") is False


def test_recovery_code_is_scoped_to_its_space(store):
    store.replace_recovery_codes("niklas", ["niklas-code-1"])
    store.replace_recovery_codes("fabian", ["fabian-code-1"])
    # niklas' Code funktioniert nicht für fabians Space, obwohl die Zeile existiert.
    assert store.consume_recovery_code("fabian", "niklas-code-1") is False
    assert store.consume_recovery_code("niklas", "niklas-code-1") is True


def test_replace_recovery_codes_deletes_old_ones(store):
    store.replace_recovery_codes("niklas", ["code-a"])
    store.replace_recovery_codes("niklas", ["code-b"])
    assert store.consume_recovery_code("niklas", "code-a") is False
    assert store.consume_recovery_code("niklas", "code-b") is True


def test_create_and_touch_session(store, clock):
    session_id, csrf_token = store.create_session(space="niklas", idle_ttl_s=3600, absolute_ttl_s=604800)
    row = store.touch_session(session_id, idle_ttl_s=3600)
    assert row is not None
    assert row.space == "niklas"
    assert row.csrf_hash == hashlib.sha256(csrf_token.encode("utf-8")).hexdigest()


def test_touch_session_rejects_idle_timeout(store, clock):
    session_id, _csrf = store.create_session(space="niklas", idle_ttl_s=60, absolute_ttl_s=604800)
    clock.advance(61)
    assert store.touch_session(session_id, idle_ttl_s=60) is None


def test_touch_session_rejects_absolute_timeout(store, clock):
    session_id, _csrf = store.create_session(space="niklas", idle_ttl_s=3600, absolute_ttl_s=60)
    clock.advance(61)
    assert store.touch_session(session_id, idle_ttl_s=3600) is None


def test_touch_session_rejects_revoked(store, clock):
    session_id, _csrf = store.create_session(space="niklas", idle_ttl_s=3600, absolute_ttl_s=604800)
    store.revoke_session(session_id, "logout")
    assert store.touch_session(session_id, idle_ttl_s=3600) is None


def test_touch_session_updates_last_seen(store, clock):
    session_id, _csrf = store.create_session(space="niklas", idle_ttl_s=3600, absolute_ttl_s=604800)
    clock.advance(30)
    row = store.touch_session(session_id, idle_ttl_s=3600)
    assert row.last_seen_at == clock()


def test_revoke_sessions_for_space_keeps_the_excepted_one(store, clock):
    keep_id, _ = store.create_session(space="niklas", idle_ttl_s=3600, absolute_ttl_s=604800)
    other_id, _ = store.create_session(space="niklas", idle_ttl_s=3600, absolute_ttl_s=604800)

    killed = store.revoke_sessions_for_space("niklas", except_session_id=keep_id, reason="password_change")
    assert killed == 1
    assert store.touch_session(keep_id, idle_ttl_s=3600) is not None
    assert store.touch_session(other_id, idle_ttl_s=3600) is None


def test_revoke_sessions_for_space_without_exception_kills_all(store, clock):
    a_id, _ = store.create_session(space="niklas", idle_ttl_s=3600, absolute_ttl_s=604800)
    b_id, _ = store.create_session(space="niklas", idle_ttl_s=3600, absolute_ttl_s=604800)

    killed = store.revoke_sessions_for_space("niklas", except_session_id=None, reason="password_change")
    assert killed == 2
    assert store.touch_session(a_id, idle_ttl_s=3600) is None
    assert store.touch_session(b_id, idle_ttl_s=3600) is None


def test_list_sessions_returns_only_the_given_space(store, clock):
    store.create_session(space="niklas", idle_ttl_s=3600, absolute_ttl_s=604800)
    store.create_session(space="fabian", idle_ttl_s=3600, absolute_ttl_s=604800)
    listed = store.list_sessions("niklas")
    assert len(listed) == 1
    assert listed[0].space == "niklas"


def test_purge_removes_expired_sessions_and_invites(store, clock):
    """S7-Ergänzung (P5 Step 2 — im Plan als Nachtrag zu Step 1 vorgesehen): `ui_sessions`
    absolut abgelaufen oder lang genug widerrufen, `invites` abgelaufen oder lang genug
    konsumiert, verschwinden über `purge_expired()`."""
    expired_session_id, _ = store.create_session(space="niklas", idle_ttl_s=3600, absolute_ttl_s=60)
    kept_session_id, _ = store.create_session(space="niklas", idle_ttl_s=3600, absolute_ttl_s=2_592_000)
    revoked_session_id, _ = store.create_session(space="niklas", idle_ttl_s=3600, absolute_ttl_s=604800)
    store.revoke_session(revoked_session_id, "logout")

    expired_invite = store.create_invite(space="niklas", purpose="reset", ttl_s=60)
    kept_invite = store.create_invite(space="niklas", purpose="reset", ttl_s=2_592_000)
    consumed_invite = store.create_invite(space="niklas", purpose="reset", ttl_s=604800)
    store.consume_invite(consumed_invite)

    clock.advance(61)  # expired_session/expired_invite abgelaufen; revoked noch innerhalb der Frist
    counts = store.purge_expired()
    assert counts["ui_sessions"] == 1  # nur die absolut abgelaufene
    assert counts["invites"] == 1  # nur die abgelaufene, nicht die frisch konsumierte

    clock.advance(RETENTION_AFTER_REVOKE_OR_CONSUME_S + 1)
    counts = store.purge_expired()
    assert counts["ui_sessions"] == 1  # jetzt die widerrufene (Frist überschritten)
    assert counts["invites"] == 1  # jetzt die konsumierte (Frist überschritten)

    # großzügiges idle_ttl_s: dieser Check gilt der PURGE (existiert die Zeile noch?), nicht der
    # Idle-Gültigkeit, die mit den vielen `clock.advance()`-Sprüngen dieses Tests längst abgelaufen wäre.
    assert store.touch_session(kept_session_id, idle_ttl_s=RETENTION_AFTER_REVOKE_OR_CONSUME_S * 10) is not None
    assert store.peek_invite(kept_invite) is not None
