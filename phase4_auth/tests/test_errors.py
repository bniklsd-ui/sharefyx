import pytest

from authserver.errors import OAUTH_ERROR_CODES, OAuthError


def test_oauth_error_accepts_known_code():
    err = OAuthError("invalid_grant")
    assert err.code == "invalid_grant"


def test_oauth_error_rejects_unknown_code():
    with pytest.raises(ValueError):
        OAuthError("not_a_real_code")


def test_oauth_error_codes_are_rfc6749():
    assert "invalid_request" in OAUTH_ERROR_CODES
    assert "invalid_grant" in OAUTH_ERROR_CODES
