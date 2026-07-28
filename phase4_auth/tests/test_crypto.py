from authserver.crypto import (
    hash_secret,
    new_secret,
    pkce_challenge,
    secrets_equal,
    verify_pkce,
)

# RFC 7636 Appendix B — the published example, not a self-computed value. A test that computes
# both sides with our own pkce_challenge() would only prove internal consistency, not RFC
# conformance.
RFC7636_VERIFIER = "dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk"
RFC7636_CHALLENGE = "E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM"


def test_new_secret_has_expected_entropy():
    token = new_secret()
    # secrets.token_urlsafe(32) -> ceil(32*4/3) == 43 base64url chars, no padding.
    assert len(token) == 43
    assert new_secret() != new_secret()


def test_hash_secret_is_stable_and_hex():
    digest = hash_secret("some-token-value")
    assert digest == hash_secret("some-token-value")
    assert len(digest) == 64
    int(digest, 16)  # raises ValueError if not hex


def test_pkce_challenge_matches_rfc7636_appendix_b():
    assert pkce_challenge(RFC7636_VERIFIER) == RFC7636_CHALLENGE


def test_verify_pkce_rejects_mismatch():
    assert verify_pkce(RFC7636_VERIFIER, RFC7636_CHALLENGE) is True
    assert verify_pkce(RFC7636_VERIFIER, "wrong-challenge") is False


def test_secrets_equal_is_constant_time_api():
    assert secrets_equal("abc", "abc") is True
    assert secrets_equal("abc", "abd") is False
