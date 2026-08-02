"""Tests für `scripts/import_users_to_db.py` (Plan §2.6/§5 Step 2) — gegen eine echte, temporäre
`AuthStore` und einen In-Memory-Keyring-Double, nie den echten Keyring oder die echte
`auth.sqlite3`.
"""
from __future__ import annotations

import importlib.util
from datetime import datetime, timezone
from pathlib import Path

import pytest

from authserver import config, users
from authserver.config import encode_data_encryption_key
from authserver.secretbox import open_
from authserver.store import AuthStore


def _now() -> datetime:
    return datetime.now(timezone.utc)


REPO_ROOT = Path(__file__).resolve().parents[2]


def _load_script(name: str):
    script_path = REPO_ROOT / "phase4_auth" / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


import_users_to_db = _load_script("import_users_to_db")


@pytest.fixture
def fake_keyring(monkeypatch):
    """Ein einziges In-Memory-Dict für BEIDE Keyring-Nutzer (`authserver.users` für die
    Nutzerakten, `authserver.config` für den DEK) — dieselbe `(service, username)`-Adressierung
    wie der echte Keyring, deshalb kollidieren die beiden Schlüssel (`auth-users`/`auth-dek`)
    nicht."""
    store: dict[tuple[str, str], str] = {}

    def fake_get_password(service, username):
        return store.get((service, username))

    def fake_set_password(service, username, password):
        store[(service, username)] = password

    monkeypatch.setattr(users.keyring, "get_password", fake_get_password)
    monkeypatch.setattr(users.keyring, "set_password", fake_set_password)
    monkeypatch.setattr(config.keyring, "get_password", fake_get_password)
    monkeypatch.setattr(config.keyring, "set_password", fake_set_password)
    return store


@pytest.fixture
def dek(fake_keyring) -> bytes:
    key = config.generate_data_encryption_key()
    fake_keyring[("nikinger-space", "auth-dek")] = encode_data_encryption_key(key)
    return key


@pytest.fixture
def db_path(tmp_path) -> Path:
    return tmp_path / "auth.sqlite3"


@pytest.fixture
def env(db_path) -> dict[str, str]:
    return {"SPACE_AUTH_DB": str(db_path)}


def _put_legacy_user(space: str, *, pwd: str = "$argon2id$fake$hash", totp: str = "JBSWY3DPEHPK3PXP") -> None:
    mapping = users.load_users_from_keyring()
    mapping[space] = {
        "pwd": pwd, "totp": totp, "totp_alg": "SHA1", "created_at": "2026-07-28T12:00:00Z",
    }
    users.save_users(mapping)


def test_dry_run_writes_nothing(fake_keyring, dek, env, db_path, capsys):
    _put_legacy_user("niklas")

    rc = import_users_to_db.main([], env=env)

    assert rc == 0
    store = AuthStore(db_path, now_fn=_now)
    assert store.get_user("niklas") is None
    out = capsys.readouterr()
    assert "würde angelegt" in out.out


def test_apply_writes_the_row(fake_keyring, dek, env, db_path):
    _put_legacy_user("niklas")

    rc = import_users_to_db.main(["--apply"], env=env)

    assert rc == 0
    store = AuthStore(db_path, now_fn=_now)
    row = store.get_user("niklas")
    assert row is not None
    assert row.password_hash == "$argon2id$fake$hash"
    assert row.totp_confirmed_at is not None  # aus created_at übernommen
    plaintext = open_(row.totp_secret_enc, key=dek, aad=b"niklas")
    assert plaintext == b"JBSWY3DPEHPK3PXP"


def test_import_skips_existing_rows_without_force(fake_keyring, dek, env, db_path):
    _put_legacy_user("niklas", pwd="$argon2id$old")
    import_users_to_db.main(["--apply"], env=env)

    _put_legacy_user("niklas", pwd="$argon2id$new")  # Keyring geändert
    rc = import_users_to_db.main(["--apply"], env=env)

    assert rc == 0
    store = AuthStore(db_path, now_fn=_now)
    assert store.get_user("niklas").password_hash == "$argon2id$old"  # unverändert


def test_import_force_overwrites_existing_row(fake_keyring, dek, env, db_path):
    _put_legacy_user("niklas", pwd="$argon2id$old")
    import_users_to_db.main(["--apply"], env=env)

    _put_legacy_user("niklas", pwd="$argon2id$new")
    rc = import_users_to_db.main(["--apply", "--force"], env=env)

    assert rc == 0
    store = AuthStore(db_path, now_fn=_now)
    assert store.get_user("niklas").password_hash == "$argon2id$new"


def test_import_prints_no_secret_material(fake_keyring, dek, env, capsys):
    _put_legacy_user("niklas", pwd="$argon2id$super-secret-hash", totp="JBSWY3DPEHPK3PXP")

    import_users_to_db.main(["--apply"], env=env)

    out = capsys.readouterr()
    combined = out.out + out.err
    assert "super-secret-hash" not in combined
    assert "JBSWY3DPEHPK3PXP" not in combined


def test_import_aborts_loudly_without_dek(fake_keyring, env):
    _put_legacy_user("niklas")  # kein DEK im Keyring hinterlegt (dek-Fixture nicht benutzt)

    rc = import_users_to_db.main(["--apply"], env=env)

    assert rc == 1


def test_import_with_empty_keyring_is_a_noop(fake_keyring, env):
    rc = import_users_to_db.main([], env=env)
    assert rc == 0
