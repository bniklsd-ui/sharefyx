"""Minimal — nicht im Plan gefordert (Step 4 listet keinen test_context.py), aber
`current_principal()`/`set_principal()`/`reset_principal()` sind hier eigenständige Logik ohne
Netzabhängigkeit. `assert_principal_matches_request()` braucht einen echten HTTP-Request-
Kontext und wird deshalb erst in Step 5 (test_app.py::test_principal_isolation_under_concurrency)
end-to-end geprüft, nicht hier.
"""
import pytest

from mcpserver.auth import AuthError, Principal
from mcpserver.context import current_principal, reset_principal, set_principal


def test_current_principal_raises_when_unset():
    with pytest.raises(AuthError):
        current_principal()


def test_set_get_reset_roundtrip():
    principal = Principal(space="nikinger", token_hash="deadbeef")
    token = set_principal(principal)
    try:
        assert current_principal() == principal
    finally:
        reset_principal(token)

    with pytest.raises(AuthError):
        current_principal()
