import base64

import pytest

from authserver.totp import generate_secret, provisioning_uri, totp_at, verify

# RFC 6238 Appendix B — the published test vectors, not values our own totp_at() produces.
_SEED_SHA1 = base64.b32encode(b"12345678901234567890").decode().rstrip("=")
_SEED_SHA256 = base64.b32encode(b"12345678901234567890123456789012").decode().rstrip("=")
_SEED_SHA512 = base64.b32encode(
    b"1234567890123456789012345678901234567890123456789012345678901234"
).decode().rstrip("=")

RFC6238_VECTORS = [
    (59, "SHA1", _SEED_SHA1, "94287082"),
    (59, "SHA256", _SEED_SHA256, "46119246"),
    (59, "SHA512", _SEED_SHA512, "90693936"),
    (1111111109, "SHA1", _SEED_SHA1, "07081804"),
    (1111111109, "SHA256", _SEED_SHA256, "68084774"),
    (1111111109, "SHA512", _SEED_SHA512, "25091201"),
    (1111111111, "SHA1", _SEED_SHA1, "14050471"),
    (1111111111, "SHA256", _SEED_SHA256, "67062674"),
    (1111111111, "SHA512", _SEED_SHA512, "99943326"),
    (1234567890, "SHA1", _SEED_SHA1, "89005924"),
    (1234567890, "SHA256", _SEED_SHA256, "91819424"),
    (1234567890, "SHA512", _SEED_SHA512, "93441116"),
    (2000000000, "SHA1", _SEED_SHA1, "69279037"),
    (2000000000, "SHA256", _SEED_SHA256, "90698825"),
    (2000000000, "SHA512", _SEED_SHA512, "38618901"),
]


@pytest.mark.parametrize("t,algo,seed,expected", RFC6238_VECTORS)
def test_totp_matches_rfc6238_test_vectors(t, algo, seed, expected):
    counter = t // 30
    assert totp_at(seed, counter, digits=8, algo=algo) == expected


def test_totp_accepts_previous_and_next_step():
    secret = generate_secret()
    now = 1_700_000_000.0
    counter = int(now // 30)

    previous_code = totp_at(secret, counter - 1)
    assert verify(secret, previous_code, now=now, window=1) == counter - 1

    next_code = totp_at(secret, counter + 1)
    assert verify(secret, next_code, now=now, window=1) == counter + 1


def test_totp_rejects_replayed_counter():
    secret = generate_secret()
    now = 1_700_000_000.0
    counter = int(now // 30)
    code = totp_at(secret, counter)

    accepted = verify(secret, code, now=now, last_counter=None)
    assert accepted == counter

    replayed = verify(secret, code, now=now, last_counter=accepted)
    assert replayed is None


def test_verify_rejects_wrong_code():
    secret = generate_secret()
    now = 1_700_000_000.0
    counter = int(now // 30)
    good = totp_at(secret, counter)
    bad = "0" * 6 if good != "0" * 6 else "1" * 6
    assert verify(secret, bad, now=now) is None


def test_generate_secret_has_no_padding_and_is_base32():
    secret = generate_secret()
    assert "=" not in secret
    base64.b32decode(secret + "=" * (-len(secret) % 8))  # raises if not valid base32


def test_provisioning_uri_is_wellformed():
    uri = provisioning_uri("JBSWY3DPEHPK3PXP", space="niklas", issuer="sharefyx")
    assert uri.startswith("otpauth://totp/")
    assert "secret=JBSWY3DPEHPK3PXP" in uri
    assert "issuer=sharefyx" in uri
    assert "algorithm=SHA1" in uri
    assert "digits=6" in uri
    assert "period=30" in uri


def test_provisioning_uri_reflects_non_default_algo():
    uri = provisioning_uri("JBSWY3DPEHPK3PXP", space="niklas", issuer="sharefyx", algo="SHA256")
    assert "algorithm=SHA256" in uri
