import os

import pytest

from authserver.secretbox import KEY_LEN, SecretBoxError, open_, seal


def _key(byte: int = 0x42) -> bytes:
    return bytes([byte]) * KEY_LEN


def test_seal_open_roundtrip():
    key = _key()
    blob = seal(b"top-secret-totp-seed", key=key, aad=b"niklas")
    assert open_(blob, key=key, aad=b"niklas") == b"top-secret-totp-seed"


def test_open_fails_with_wrong_key():
    blob = seal(b"secret", key=_key(0x11), aad=b"niklas")
    with pytest.raises(SecretBoxError):
        open_(blob, key=_key(0x22), aad=b"niklas")


def test_open_fails_with_wrong_aad():
    """Der Test, der die Seed-Vertauschung ausschließt: derselbe Schlüssel, aber ein Seed, der
    unter dem AAD einer anderen Zeile versiegelt wurde, darf hier nicht aufgehen."""
    key = _key()
    blob = seal(b"niklas-secret", key=key, aad=b"niklas")
    with pytest.raises(SecretBoxError):
        open_(blob, key=key, aad=b"fabian")


def test_open_fails_on_tampered_ciphertext():
    key = _key()
    blob = seal(b"secret", key=key, aad=b"niklas")
    tampered = blob[:-1] + bytes([blob[-1] ^ 0xFF])
    with pytest.raises(SecretBoxError):
        open_(tampered, key=key, aad=b"niklas")


def test_nonce_is_unique_across_seals():
    key = _key()
    blob_a = seal(b"same-plaintext", key=key, aad=b"niklas")
    blob_b = seal(b"same-plaintext", key=key, aad=b"niklas")
    assert blob_a[:12] != blob_b[:12]
    assert blob_a != blob_b


def test_seal_rejects_wrong_key_length():
    with pytest.raises(SecretBoxError):
        seal(b"secret", key=os.urandom(16), aad=b"niklas")


def test_open_rejects_blob_shorter_than_nonce():
    with pytest.raises(SecretBoxError):
        open_(b"short", key=_key(), aad=b"niklas")
