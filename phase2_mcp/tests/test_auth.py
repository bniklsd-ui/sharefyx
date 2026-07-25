import pytest

from mcpserver import credentials
from mcpserver.auth import AuthError, KeyringTokenResolver, Principal


def test_resolve_known_token():
    token = "supersecret-test-token"
    token_hash = credentials.hash_token(token)
    resolver = KeyringTokenResolver(load_map=lambda: {token_hash: "nikinger"})

    principal = resolver.resolve(token)

    assert principal.space == "nikinger"
    assert principal.token_hash == token_hash


def test_resolve_unknown_raises():
    resolver = KeyringTokenResolver(load_map=lambda: {})
    with pytest.raises(AuthError):
        resolver.resolve("nicht-im-keyring")


def test_resolve_empty_raises():
    resolver = KeyringTokenResolver(load_map=lambda: {})
    with pytest.raises(AuthError):
        resolver.resolve("")


def test_principal_repr_hides_token():
    principal = Principal(space="nikinger", token_hash="0123456789abcdef")
    text = repr(principal)
    assert "0123456789abcdef" not in text
    assert "01234567" in text
