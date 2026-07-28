from authserver.passwords import (
    ARGON2_MEMORY_KIB,
    ARGON2_PARALLELISM,
    ARGON2_TIME_COST,
    DUMMY_HASH,
    hash_password,
    needs_rehash,
    verify_password,
)


def test_argon2_roundtrip():
    stored = hash_password("correct horse battery staple")
    assert verify_password(stored, "correct horse battery staple") is True


def test_verify_rejects_wrong_password():
    stored = hash_password("correct horse battery staple")
    assert verify_password(stored, "wrong password") is False


def test_verify_returns_false_on_garbage_hash():
    # wirft nie — ein kaputter/fremder Hash ist ununterscheidbar von einem falschen Passwort
    assert verify_password("not-an-argon2-hash", "anything") is False
    assert verify_password("", "anything") is False


def test_parameters_match_owasp_minimum():
    stored = hash_password("some-password")
    # liest die Parameter aus dem erzeugten Hash-String zurück, statt die Konstanten gegen
    # sich selbst zu prüfen
    assert f"m={ARGON2_MEMORY_KIB}" in stored
    assert f"t={ARGON2_TIME_COST}" in stored
    assert f"p={ARGON2_PARALLELISM}" in stored
    assert stored.startswith("$argon2id$")


def test_needs_rehash_false_for_current_parameters():
    stored = hash_password("some-password")
    assert needs_rehash(stored) is False


def test_dummy_hash_is_a_real_argon2_hash_verifiable_against_itself():
    assert DUMMY_HASH.startswith("$argon2id$")
    assert verify_password(DUMMY_HASH, "enumeration-resistance-dummy-password") is True
    assert verify_password(DUMMY_HASH, "anything-else") is False
