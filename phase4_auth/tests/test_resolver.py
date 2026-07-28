from datetime import datetime, timedelta, timezone

import pytest

from authserver import crypto
from authserver.resolver import OAuthTokenResolver, ResolveError, ResolvedPrincipal
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


@pytest.fixture
def resolver(store):
    return OAuthTokenResolver(store)


def _issue_access_token(store, *, space="niklas") -> str:
    family_id = store.create_family(
        space=space, client_id="c1", scope="space", resource="https://x/mcp"
    )
    access_token, _refresh_token = store.issue_token_pair(
        family_id, access_ttl_s=3600, refresh_ttl_s=2592000
    )
    return access_token


def test_resolve_valid_token_returns_space_and_hash(store, resolver):
    token = _issue_access_token(store, space="niklas")
    result = resolver.resolve(token)
    assert isinstance(result, ResolvedPrincipal)
    assert result.space == "niklas"
    assert result.token_hash == crypto.hash_secret(token)


def test_resolve_empty_credential_raises(resolver):
    with pytest.raises(ResolveError):
        resolver.resolve("")


def test_resolve_unknown_token_raises(resolver):
    with pytest.raises(ResolveError):
        resolver.resolve("never-issued-token")


def test_resolve_expired_token_raises(store, resolver, clock):
    family_id = store.create_family(
        space="niklas", client_id="c1", scope="space", resource="https://x/mcp"
    )
    access_token, _ = store.issue_token_pair(family_id, access_ttl_s=1, refresh_ttl_s=2592000)
    clock.advance(2)
    with pytest.raises(ResolveError):
        resolver.resolve(access_token)


def test_resolve_revoked_family_token_raises(store, resolver):
    family_id = store.create_family(
        space="niklas", client_id="c1", scope="space", resource="https://x/mcp"
    )
    access_token, _ = store.issue_token_pair(family_id, access_ttl_s=3600, refresh_ttl_s=2592000)
    store.revoke_family(family_id, "code_replay")
    with pytest.raises(ResolveError):
        resolver.resolve(access_token)


def test_resolve_does_not_return_mcpserver_principal_type(store, resolver):
    """§1.3: `resolver.py` importiert nichts aus `mcpserver` — das Rückgabeobjekt kann also gar
    kein `mcpserver.auth.Principal` sein, nur ein strukturell gleichwertiges. Belegt die
    Abhängigkeitsrichtung über das Rückgabeobjekt, nicht nur über den Import-Grep."""
    token = _issue_access_token(store)
    result = resolver.resolve(token)
    assert type(result).__module__ == "authserver.resolver"
