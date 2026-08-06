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


def test_invite_requires_base_url(env, capsys):
    rc = authctl.main(["invite", "niklas"], env=env)  # env hat kein SPACE_PUBLIC_BASE_URL
    assert rc == 1
    assert "SPACE_PUBLIC_BASE_URL" in capsys.readouterr().err


def test_invite_prints_the_link_once(env, store, capsys):
    env = {**env, "SPACE_PUBLIC_BASE_URL": "https://space.example.ts.net"}
    rc = authctl.main(["invite", "niklas"], env=env)

    out = capsys.readouterr().out
    assert rc == 0
    links = [line for line in out.splitlines() if "/ui/invite/" in line]
    assert len(links) == 1
    assert links[0].startswith("https://space.example.ts.net/ui/invite/")


def test_invite_names_the_database_it_wrote_and_the_url_it_built(env, store, capsys, tmp_path):
    """**[2026-08-06, live gelernt]** Der Token landet in der Datenbank aus `STATE_DIRECTORY`,
    der Link entsteht aus `SPACE_PUBLIC_BASE_URL` — zwischen beiden gibt es keine Verbindung.
    Wer eine Staging-Einladung mit der Produktiv-Basis-URL in der Umgebung erzeugt, bekommt einen
    Link, der auf der falschen Instanz „Einladung ungültig oder abgelaufen" liefert; das liest
    sich wie „Konto existiert bereits" und führt in eine völlig andere Richtung. Genau so
    geschehen. Die Ausgabe muss beides nebeneinander nennen, damit der Mensch es abgleichen kann.

    Der Link selbst bleibt auf stdout (Hard Rule 7), die Einordnung geht auf stderr."""
    env = {**env, "SPACE_PUBLIC_BASE_URL": "https://space.example.ts.net"}
    rc = authctl.main(["invite", "niklas"], env=env)

    err = capsys.readouterr().err
    assert rc == 0
    assert env["SPACE_AUTH_DB"] in err, "Datenbankpfad fehlt in der Ausgabe"
    assert "https://space.example.ts.net" in err, "Ziel-URL fehlt in der Ausgabe"
    assert "PRODUKTIV" in err


def test_invite_labels_a_staging_database_as_such(env, capsys, tmp_path):
    """Die Kennzeichnung hängt am Datenbankpfad, nicht an der URL: welche URL zu einer Instanz
    gehört, kann `authctl` nicht wissen (der Dienst hinterlegt sie nirgends) — welche Datenbank
    es gerade beschrieben hat, weiß es sicher. Lieber die sichere Hälfte klar benennen als eine
    Heuristik raten, die bei einer Staging-URL ohne das Wort „staging" danebenliegt."""
    state = tmp_path / "sharefyx-staging"
    state.mkdir()
    env = {
        "SPACE_AUTH_DB": str(state / "auth.sqlite3"),
        "SPACE_PUBLIC_BASE_URL": "https://space.example.ts.net:8766",
    }
    rc = authctl.main(["invite", "niklas"], env=env)

    err = capsys.readouterr().err
    assert rc == 0
    assert "STAGING" in err
    assert "PRODUKTIV" not in err


def test_list_users_reports_status_and_recovery_code_count(env, store, capsys):
    store.upsert_user(
        "niklas", password_hash="x", totp_secret_enc=None, totp_alg="SHA1",
        totp_confirmed_at=None, status="active",
    )
    store.replace_recovery_codes("niklas", ["a-code-1", "a-code-2"])

    rc = authctl.main(["list-users"], env=env)

    out = capsys.readouterr().out
    assert rc == 0
    assert "niklas" in out
    assert "status='active'" in out
    assert "offene_recovery_codes=2" in out
    assert "x" not in out.split("niklas", 1)[1].split()[0]  # kein Passwort-Hash in der Ausgabe


def test_disable_user_revokes_sessions_and_families(env, store, capsys):
    store.upsert_user(
        "niklas", password_hash="x", totp_secret_enc=None, totp_alg="SHA1",
        totp_confirmed_at=None, status="active",
    )
    session_id, _ = store.create_session(space="niklas", idle_ttl_s=3600, absolute_ttl_s=604800)
    family_id = store.create_family(space="niklas", client_id="c1", scope="space", resource="https://x/mcp")

    rc = authctl.main(["disable-user", "--space", "niklas"], env=env)

    out = capsys.readouterr().out
    assert rc == 0
    assert "deaktiviert" in out
    assert store.get_user("niklas").status == "disabled"
    assert store.touch_session(session_id, idle_ttl_s=3600) is None
    (family,) = store.list_families(space="niklas")
    assert family.family_id == family_id
    assert family.revoked_at is not None


def test_disable_user_also_revokes_outstanding_invites(env, store, capsys):
    """Advisor-Fund: ohne dies bliebe eine noch nicht eingelöste Einladung gültig und würde
    über `webui/routes_auth.py :: _invite_post`s `upsert_user(..., status="active")` die
    Sperre umgehen."""
    store.upsert_user(
        "niklas", password_hash="x", totp_secret_enc=None, totp_alg="SHA1",
        totp_confirmed_at=None, status="active",
    )
    token = store.create_invite(space="niklas", purpose="reset", ttl_s=3600)

    rc = authctl.main(["disable-user", "--space", "niklas"], env=env)

    out = capsys.readouterr().out
    assert rc == 0
    assert "1 Einladung(en) widerrufen" in out
    assert store.peek_invite(token) is None


def test_enable_user_reactivates(env, store, capsys):
    store.upsert_user(
        "niklas", password_hash="x", totp_secret_enc=None, totp_alg="SHA1",
        totp_confirmed_at=None, status="disabled",
    )

    rc = authctl.main(["enable-user", "--space", "niklas"], env=env)

    assert rc == 0
    assert "aktiviert" in capsys.readouterr().out
    assert store.get_user("niklas").status == "active"


def test_list_sessions_shows_active_and_revoked(env, store, capsys):
    store.create_session(space="niklas", idle_ttl_s=3600, absolute_ttl_s=604800)

    rc = authctl.main(["list-sessions", "--space", "niklas"], env=env)

    out = capsys.readouterr().out
    assert rc == 0
    assert "status=aktiv" in out


def test_revoke_sessions_kills_all_of_a_space(env, store, capsys):
    store.create_session(space="niklas", idle_ttl_s=3600, absolute_ttl_s=604800)
    store.create_session(space="niklas", idle_ttl_s=3600, absolute_ttl_s=604800)

    rc = authctl.main(["revoke-sessions", "--space", "niklas"], env=env)

    out = capsys.readouterr().out
    assert rc == 0
    assert "2 Sitzung(en) widerrufen" in out
