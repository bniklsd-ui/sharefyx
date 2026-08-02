from datetime import datetime, timedelta, timezone

import pytest

from authserver import totp
from authserver.secretbox import KEY_LEN, seal
from authserver.store import AuthStore
from authserver.userdir import RECOVERY_CODE_LEN, UserDirectory, looks_like_recovery_code


@pytest.fixture
def clock():
    state = {"now": datetime(2026, 8, 2, 12, 0, 0, tzinfo=timezone.utc)}

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
def dek() -> bytes:
    return bytes([0x7A]) * KEY_LEN


@pytest.fixture
def userdir(store, dek) -> UserDirectory:
    return UserDirectory(store, dek=dek)


def test_get_returns_none_for_unknown_space(userdir):
    assert userdir.get("ghost") is None


def test_get_decrypts_the_totp_secret(store, dek, userdir, clock):
    secret = totp.generate_secret()
    blob = seal(secret.encode("ascii"), key=dek, aad=b"niklas")
    store.upsert_user(
        "niklas", password_hash="h", totp_secret_enc=blob, totp_alg="SHA1",
        totp_confirmed_at=clock(), status="active",
    )
    record = userdir.get("niklas")
    assert record is not None
    assert record.password_hash == "h"
    assert record.totp_secret == secret
    assert record.totp_confirmed is True
    assert record.status == "active"


def test_userdirectory_reads_fresh_after_external_update(store, dek, userdir):
    """P5-L, schließt O1: kein Cache — eine externe Änderung (z. B. `provision_user`-Äquivalent
    via `set_password`) muss ohne Neustart/neue `UserDirectory`-Instanz sichtbar sein."""
    store.upsert_user(
        "niklas", password_hash="old", totp_secret_enc=None, totp_alg="SHA1",
        totp_confirmed_at=None, status="active",
    )
    assert userdir.get("niklas").password_hash == "old"

    userdir.set_password("niklas", "new-password")

    assert userdir.get("niklas").password_hash != "old"
    import authserver.passwords as passwords

    assert passwords.verify_password(userdir.get("niklas").password_hash, "new-password")


def test_userdirectory_returns_none_for_broken_record(userdir):
    """S6, jetzt strukturell statt per `dict.get()`-Fallback: `store.get_user()` liefert für
    einen unbekannten Space `None`, nie einen Datensatz mit fehlenden Feldern."""
    assert userdir.get("never-provisioned") is None


def test_userdirectory_never_returns_encrypted_seed(store, dek, userdir):
    blob = seal(b"plaintext-seed-value", key=dek, aad=b"niklas")
    store.upsert_user(
        "niklas", password_hash="h", totp_secret_enc=blob, totp_alg="SHA1",
        totp_confirmed_at=None, status="active",
    )
    record = userdir.get("niklas")
    assert record.totp_secret != blob
    assert isinstance(record.totp_secret, str)


def test_get_logs_and_hides_totp_when_dek_missing(store, dek, caplog):
    blob = seal(b"secret", key=dek, aad=b"niklas")
    store.upsert_user(
        "niklas", password_hash="h", totp_secret_enc=blob, totp_alg="SHA1",
        totp_confirmed_at=None, status="active",
    )
    # __init__ selbst würde hier abbrechen (siehe test_init_raises_without_dek_and_nonempty_users
    # unten) — dieser Test prüft gezielt `get()`s Verhalten, konstruiert also am Konstruktor
    # vorbei, statt eine zweite, künstlich leere Store-Instanz zu bauen.
    directory_without_dek = UserDirectory.__new__(UserDirectory)
    directory_without_dek._store = store
    directory_without_dek._dek = None

    record = directory_without_dek.get("niklas")
    assert record is not None
    assert record.totp_secret is None
    assert "kein DEK" in caplog.text or "DEK" in caplog.text


def test_init_raises_without_dek_and_nonempty_users(store):
    store.upsert_user(
        "niklas", password_hash="h", totp_secret_enc=None, totp_alg="SHA1",
        totp_confirmed_at=None, status="active",
    )
    with pytest.raises(ValueError):
        UserDirectory(store, dek=None)


def test_init_allows_missing_dek_with_empty_users(store):
    UserDirectory(store, dek=None)  # keine Nutzerakten -> kein Widerspruch


def test_spaces_lists_all_provisioned_spaces(store, userdir):
    store.upsert_user(
        "niklas", password_hash="h", totp_secret_enc=None, totp_alg="SHA1",
        totp_confirmed_at=None, status="active",
    )
    store.upsert_user(
        "fabian", password_hash="h", totp_secret_enc=None, totp_alg="SHA1",
        totp_confirmed_at=None, status="active",
    )
    assert set(userdir.spaces()) == {"niklas", "fabian"}


def test_totp_enrollment_roundtrip(store, userdir, clock):
    store.upsert_user(
        "niklas", password_hash="h", totp_secret_enc=None, totp_alg="SHA1",
        totp_confirmed_at=None, status="active",
    )
    secret = userdir.begin_totp_enrollment("niklas")
    assert userdir.get("niklas").totp_confirmed is False

    counter = int(clock().timestamp() // 30)
    code = totp.totp_at(secret, counter)
    assert userdir.confirm_totp_enrollment("niklas", code, now=clock().timestamp()) is True
    assert userdir.get("niklas").totp_confirmed is True


def test_confirm_totp_enrollment_rejects_wrong_code(store, userdir, clock):
    store.upsert_user(
        "niklas", password_hash="h", totp_secret_enc=None, totp_alg="SHA1",
        totp_confirmed_at=None, status="active",
    )
    userdir.begin_totp_enrollment("niklas")
    assert userdir.confirm_totp_enrollment("niklas", "000000", now=clock().timestamp()) is False
    assert userdir.get("niklas").totp_confirmed is False


def test_recovery_codes_roundtrip(store, userdir):
    store.upsert_user(
        "niklas", password_hash="h", totp_secret_enc=None, totp_alg="SHA1",
        totp_confirmed_at=None, status="active",
    )
    codes = userdir.issue_recovery_codes("niklas")
    assert len(codes) == 10
    assert all(looks_like_recovery_code(c) for c in codes)
    assert len(set(codes)) == 10  # keine Duplikate

    assert userdir.consume_recovery_code("niklas", codes[0]) is True
    assert userdir.consume_recovery_code("niklas", codes[0]) is False  # schon verbraucht


def test_looks_like_recovery_code_shape():
    assert looks_like_recovery_code("ABCD-EFGH-J") is True
    assert len("ABCD-EFGH-J") == RECOVERY_CODE_LEN
    assert looks_like_recovery_code("123456") is False  # kein Bindestrich, falsche Länge
    assert looks_like_recovery_code("ABCDEFGHIJK") is False  # Länge 11, aber kein Bindestrich
