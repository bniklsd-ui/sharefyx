"""Der Autorisierungsfluss (Plan §2.4/§5 Step 5) — ausschließlich über `flows.py`-Funktionen,
kein HTTP. Das ist der Punkt von `flows.py`: `routes.py` bleibt dünn, der Fluss selbst ist ohne
Starlette testbar (siehe Modul-Docstring dort). HTTP-Verdrahtung (Header, Cookies,
Content-Type) lebt in `test_routes.py`.
"""
from datetime import datetime, timedelta, timezone

import pytest

from authserver import flows, passwords, totp
from authserver.config import AuthSettings
from authserver.crypto import pkce_challenge
from authserver.errors import OAuthError
from authserver.ratelimit import MAX_FAILURES, LoginThrottle
from authserver.store import AuthStore

REDIRECT_URI = "https://claude.ai/api/mcp/auth_callback"
SPACE = "niklas"
PASSWORD = "correct horse battery staple"
TOTP_SECRET = totp.generate_secret()
VERIFIER = "a" * 64
CODE_CHALLENGE = pkce_challenge(VERIFIER)


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


@pytest.fixture
def settings(tmp_path):
    return AuthSettings(base_url="https://space.example.ts.net", db_path=tmp_path / "unused.sqlite3")


@pytest.fixture
def throttle(store, clock):
    return LoginThrottle(store, now_fn=clock)


@pytest.fixture
def users():
    return {
        SPACE: {
            "pwd": passwords.hash_password(PASSWORD),
            "totp": TOTP_SECRET,
            "totp_alg": "SHA1",
        }
    }


@pytest.fixture
def client(store):
    return store.create_client(
        client_name="Claude", application_type=None, redirect_uris=[REDIRECT_URI]
    )


def _totp_code(clock, secret=TOTP_SECRET):
    counter = int(clock().timestamp() // 30)
    return totp.totp_at(secret, counter, algo="SHA1")


def _start(store, settings, client, *, code_challenge=CODE_CHALLENGE, code_challenge_method="S256",
           response_type="code", scope=None, resource=None, state="xyz",
           redirect_uri=REDIRECT_URI, client_id=None):
    return flows.start_authorize(
        store=store,
        settings=settings,
        client_id=client_id if client_id is not None else client.client_id,
        redirect_uri=redirect_uri,
        response_type=response_type,
        state=state,
        code_challenge=code_challenge,
        code_challenge_method=code_challenge_method,
        scope=scope,
        resource=resource,
    )


def _pending_request_id(store, settings, client, **kwargs):
    result = _start(store, settings, client, **kwargs)
    assert isinstance(result, flows.RenderForm), result
    return result.request_id


def _issue_code(store, settings, users, throttle, clock, client, *, code_challenge=CODE_CHALLENGE):
    # Jeder Login-Erfolg setzt den TOTP-Zähler (Replay-Schutz) hoch — ohne Zeitfortschritt würde
    # ein zweiter Aufruf in DERSELBEN Sekunde denselben Zähler liefern und als Replay gelten.
    clock.advance(30)
    request_id = _pending_request_id(store, settings, client, code_challenge=code_challenge)
    result = flows.submit_consent(
        store=store, settings=settings, users=users, throttle=throttle, now_fn=clock,
        request_id=request_id, space=SPACE, password=PASSWORD, totp_code=_totp_code(clock),
        action="allow",
    )
    assert isinstance(result, flows.RedirectSuccess), result
    return result.code


# -- GET /oauth/authorize ---------------------------------------------------------------


def test_authorize_rejects_unknown_client_without_redirect(store, settings, client):
    result = _start(store, settings, client, client_id="ghost-client")
    assert isinstance(result, flows.ErrorPage)


def test_authorize_rejects_unregistered_redirect_uri_without_redirect(store, settings, client):
    result = _start(store, settings, client, redirect_uri="https://claude.ai/other-callback")
    assert isinstance(result, flows.ErrorPage)


def test_authorize_rejects_plain_pkce(store, settings, client):
    result = _start(store, settings, client, code_challenge_method="plain")
    assert isinstance(result, flows.RedirectError)
    assert result.error == "invalid_request"


def test_authorize_rejects_missing_code_challenge(store, settings, client):
    """Andere Verzweigung als der plain-Test: `code_challenge` fehlt komplett statt eine
    falsche Methode zu tragen — beide führen zu `invalid_request`, aber über verschiedene
    Bedingungen in derselben `if`-Zeile."""
    result = _start(store, settings, client, code_challenge="")
    assert isinstance(result, flows.RedirectError)
    assert result.error == "invalid_request"


def test_authorize_rejects_scope_outside_allowlist(store, settings, client):
    result = _start(store, settings, client, scope="space admin")
    assert isinstance(result, flows.RedirectError)
    assert result.error == "invalid_scope"


def test_authorize_redirect_error_carries_state_and_iss(store, settings, client):
    result = _start(store, settings, client, response_type="token", state="abc123")
    assert isinstance(result, flows.RedirectError)
    assert result.state == "abc123"
    assert result.iss == settings.issuer
    assert result.redirect_uri == REDIRECT_URI


def test_authorize_rejects_foreign_resource_parameter(store, settings, client):
    result = _start(store, settings, client, resource="https://evil.example/mcp")
    assert isinstance(result, flows.RedirectError)
    assert result.error == "invalid_target"


# -- POST /oauth/authorize (Consent) -----------------------------------------------------


def test_consent_requires_password_and_totp(store, settings, users, throttle, clock, client):
    request_id = _pending_request_id(store, settings, client)
    result = flows.submit_consent(
        store=store, settings=settings, users=users, throttle=throttle, now_fn=clock,
        request_id=request_id, space=SPACE, password="wrong", totp_code="000000", action="allow",
    )
    assert isinstance(result, flows.ErrorPage)


def test_wrong_password_and_unknown_space_give_identical_response(
    store, settings, users, clock, client, monkeypatch
):
    calls: list[str] = []
    original = passwords.verify_password

    def counting_verify(stored, password):
        calls.append(stored)
        return original(stored, password)

    monkeypatch.setattr(flows.passwords, "verify_password", counting_verify)

    request_id_a = _pending_request_id(store, settings, client)
    result_a = flows.submit_consent(
        store=store, settings=settings, users=users, throttle=LoginThrottle(store, now_fn=clock),
        now_fn=clock, request_id=request_id_a, space=SPACE, password="wrong-password",
        totp_code="000000", action="allow",
    )

    request_id_b = _pending_request_id(store, settings, client)
    result_b = flows.submit_consent(
        store=store, settings=settings, users=users, throttle=LoginThrottle(store, now_fn=clock),
        now_fn=clock, request_id=request_id_b, space="ghost-space", password="whatever",
        totp_code="000000", action="allow",
    )

    assert result_a == result_b
    assert len(calls) == 2  # verify_password lief in BEIDEN Fällen — kein Timing-Orakel


def test_login_failure_increments_throttle(store, settings, users, throttle, clock, client):
    request_id = _pending_request_id(store, settings, client)
    flows.submit_consent(
        store=store, settings=settings, users=users, throttle=throttle, now_fn=clock,
        request_id=request_id, space=SPACE, password="wrong", totp_code="000000", action="allow",
    )
    attempt = store.get_login_attempt(SPACE)
    assert attempt is not None
    assert attempt.failures == 1


def test_locked_account_skips_password_check(
    store, settings, users, throttle, clock, client, monkeypatch
):
    for _ in range(MAX_FAILURES):
        throttle.register_failure(SPACE)
    assert throttle.check(SPACE) is not None  # gesperrt

    calls: list[str] = []
    monkeypatch.setattr(
        flows.passwords, "verify_password", lambda *a, **k: calls.append(1) or False
    )

    request_id = _pending_request_id(store, settings, client)
    result = flows.submit_consent(
        store=store, settings=settings, users=users, throttle=throttle, now_fn=clock,
        request_id=request_id, space=SPACE, password=PASSWORD, totp_code=_totp_code(clock),
        action="allow",
    )
    assert isinstance(result, flows.ErrorPage)
    assert calls == []


def test_form_is_single_use(store, settings, users, throttle, clock, client):
    request_id = _pending_request_id(store, settings, client)
    flows.submit_consent(
        store=store, settings=settings, users=users, throttle=throttle, now_fn=clock,
        request_id=request_id, space=SPACE, password="wrong", totp_code="000000", action="allow",
    )
    second = flows.submit_consent(
        store=store, settings=settings, users=users, throttle=throttle, now_fn=clock,
        request_id=request_id, space=SPACE, password=PASSWORD, totp_code=_totp_code(clock),
        action="allow",
    )
    assert isinstance(second, flows.ErrorPage)


def test_totp_replay_is_rejected_without_burning_the_stored_counter(
    store, settings, users, throttle, clock, client
):
    """§2.4 POST-Schritt 6, bisher ohne Test: derselbe TOTP-Code darf kein zweites Mal
    akzeptiert werden. Zwei getrennte `AuthRequest`s (das Formular ist ohnehin Einmalgebrauch),
    aber derselbe Code, ohne die Uhr vorzurücken."""
    code_at_now = _totp_code(clock)

    request_id_1 = _pending_request_id(store, settings, client)
    first = flows.submit_consent(
        store=store, settings=settings, users=users, throttle=throttle, now_fn=clock,
        request_id=request_id_1, space=SPACE, password=PASSWORD, totp_code=code_at_now,
        action="allow",
    )
    assert isinstance(first, flows.RedirectSuccess)
    counter_after_success = store.get_totp_counter(SPACE)
    assert counter_after_success is not None

    request_id_2 = _pending_request_id(store, settings, client)
    second = flows.submit_consent(
        store=store, settings=settings, users=users, throttle=throttle, now_fn=clock,
        request_id=request_id_2, space=SPACE, password=PASSWORD, totp_code=code_at_now,
        action="allow",
    )
    assert isinstance(second, flows.ErrorPage)
    assert store.get_totp_counter(SPACE) == counter_after_success  # unverändert, kein Vorrücken


def test_consent_deny_redirects_with_access_denied(store, settings, users, throttle, clock, client):
    request_id = _pending_request_id(store, settings, client, state="xyz")
    result = flows.submit_consent(
        store=store, settings=settings, users=users, throttle=throttle, now_fn=clock,
        request_id=request_id, space=SPACE, password="", totp_code="", action="deny",
    )
    assert isinstance(result, flows.RedirectError)
    assert result.error == "access_denied"
    assert result.state == "xyz"


# -- POST /oauth/token --------------------------------------------------------------------


def test_code_exchange_happy_path(store, settings, users, throttle, clock, client):
    code = _issue_code(store, settings, users, throttle, clock, client)
    result = flows.issue_token(
        store=store, settings=settings, grant_type="authorization_code",
        code=code, redirect_uri=REDIRECT_URI, client_id=client.client_id, code_verifier=VERIFIER,
    )
    assert isinstance(result, flows.TokenSuccess)
    assert result.access_token
    assert result.refresh_token
    assert result.scope == "space"


def test_authorize_success_redirect_carries_iss(store, settings, users, throttle, clock, client):
    """RFC 9207: die AS-Metadaten werben `authorization_response_iss_parameter_supported`, ein
    Client darf sich also darauf verlassen — auch auf dem Erfolgspfad, nicht nur bei Fehlern
    (die bereits in `test_authorize_redirect_error_carries_state_and_iss` geprüft sind)."""
    request_id = _pending_request_id(store, settings, client)
    result = flows.submit_consent(
        store=store, settings=settings, users=users, throttle=throttle, now_fn=clock,
        request_id=request_id, space=SPACE, password=PASSWORD, totp_code=_totp_code(clock),
        action="allow",
    )
    assert isinstance(result, flows.RedirectSuccess)
    assert result.iss == settings.issuer


def test_code_exchange_rejects_wrong_verifier(store, settings, users, throttle, clock, client):
    code = _issue_code(store, settings, users, throttle, clock, client)
    with pytest.raises(OAuthError) as exc_info:
        flows.issue_token(
            store=store, settings=settings, grant_type="authorization_code",
            code=code, redirect_uri=REDIRECT_URI, client_id=client.client_id,
            code_verifier="wrong-verifier",
        )
    assert exc_info.value.code == "invalid_grant"


def test_code_exchange_rejects_mismatched_redirect_uri(store, settings, users, throttle, clock, client):
    code = _issue_code(store, settings, users, throttle, clock, client)
    with pytest.raises(OAuthError) as exc_info:
        flows.issue_token(
            store=store, settings=settings, grant_type="authorization_code",
            code=code, redirect_uri="https://claude.ai/wrong-callback",
            client_id=client.client_id, code_verifier=VERIFIER,
        )
    assert exc_info.value.code == "invalid_grant"


def test_code_replay_revokes_family(store, settings, users, throttle, clock, client):
    code = _issue_code(store, settings, users, throttle, clock, client)
    first = flows.issue_token(
        store=store, settings=settings, grant_type="authorization_code",
        code=code, redirect_uri=REDIRECT_URI, client_id=client.client_id, code_verifier=VERIFIER,
    )
    with pytest.raises(OAuthError) as exc_info:
        flows.issue_token(
            store=store, settings=settings, grant_type="authorization_code",
            code=code, redirect_uri=REDIRECT_URI, client_id=client.client_id, code_verifier=VERIFIER,
        )
    assert exc_info.value.code == "invalid_grant"
    assert store.lookup_access_token(first.access_token) is None


def test_refresh_rotates_and_returns_new_refresh(store, settings, users, throttle, clock, client):
    code = _issue_code(store, settings, users, throttle, clock, client)
    first = flows.issue_token(
        store=store, settings=settings, grant_type="authorization_code",
        code=code, redirect_uri=REDIRECT_URI, client_id=client.client_id, code_verifier=VERIFIER,
    )
    second = flows.issue_token(
        store=store, settings=settings, grant_type="refresh_token",
        refresh_token=first.refresh_token,
    )
    assert second.access_token != first.access_token
    assert second.refresh_token != first.refresh_token


def test_refresh_replay_revokes_family(store, settings, users, throttle, clock, client):
    code = _issue_code(store, settings, users, throttle, clock, client)
    first = flows.issue_token(
        store=store, settings=settings, grant_type="authorization_code",
        code=code, redirect_uri=REDIRECT_URI, client_id=client.client_id, code_verifier=VERIFIER,
    )
    second = flows.issue_token(
        store=store, settings=settings, grant_type="refresh_token",
        refresh_token=first.refresh_token,
    )
    with pytest.raises(OAuthError) as exc_info:
        flows.issue_token(
            store=store, settings=settings, grant_type="refresh_token",
            refresh_token=first.refresh_token,
        )
    assert exc_info.value.code == "invalid_grant"
    assert store.lookup_access_token(second.access_token) is None


def test_all_token_errors_use_invalid_grant(store, settings, users, throttle, clock, client):
    # Jeder Fall bekommt seinen eigenen frischen Code, unmittelbar vor seinem eigenen
    # `pytest.raises`-Block ausgestellt (nicht vorab in einer Liste) — `code_ttl_s` ist 60s,
    # `_issue_code` rückt die Uhr pro Aufruf 30s vor; ein vorab gebauter Vorrat aus drei Codes
    # würde den ältesten exakt an seiner `expires_at`-Grenze antreffen und über "abgelaufen"
    # grün werden, nicht über die eigentlich geprüfte Fehlerart (Advisor-Fund dieser Session).
    with pytest.raises(OAuthError) as exc_info:
        flows.issue_token(
            store=store, settings=settings, grant_type="authorization_code",
            code="never-issued-code", redirect_uri=REDIRECT_URI, client_id=client.client_id,
            code_verifier=VERIFIER,
        )
    assert exc_info.value.code == "invalid_grant"

    with pytest.raises(OAuthError) as exc_info:
        flows.issue_token(
            store=store, settings=settings, grant_type="authorization_code",
            code=_issue_code(store, settings, users, throttle, clock, client),
            redirect_uri=REDIRECT_URI, client_id="wrong-client-id", code_verifier=VERIFIER,
        )
    assert exc_info.value.code == "invalid_grant"

    with pytest.raises(OAuthError) as exc_info:
        flows.issue_token(
            store=store, settings=settings, grant_type="authorization_code",
            code=_issue_code(store, settings, users, throttle, clock, client),
            redirect_uri="https://claude.ai/wrong-callback", client_id=client.client_id,
            code_verifier=VERIFIER,
        )
    assert exc_info.value.code == "invalid_grant"

    with pytest.raises(OAuthError) as exc_info:
        flows.issue_token(
            store=store, settings=settings, grant_type="authorization_code",
            code=_issue_code(store, settings, users, throttle, clock, client),
            redirect_uri=REDIRECT_URI, client_id=client.client_id, code_verifier="wrong-verifier",
        )
    assert exc_info.value.code == "invalid_grant"

    with pytest.raises(OAuthError) as exc_info:
        flows.issue_token(
            store=store, settings=settings, grant_type="refresh_token",
            refresh_token="never-issued-refresh-token",
        )
    assert exc_info.value.code == "invalid_grant"

    # Strukturelle Fehler (grant_type selbst, fehlendes Pflichtfeld) behalten ihren eigenen Code.
    with pytest.raises(OAuthError) as exc_info:
        flows.issue_token(store=store, settings=settings, grant_type="carrier_pigeon")
    assert exc_info.value.code == "unsupported_grant_type"

    with pytest.raises(OAuthError) as exc_info:
        flows.issue_token(store=store, settings=settings, grant_type="authorization_code")
    assert exc_info.value.code == "invalid_request"
