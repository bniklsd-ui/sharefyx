"""Tests für `phase7_spaces_admin/scripts/testcred.py` (P7-W/A7b) — `keyring` wird
durchgehend gemockt, kein Test hier fasst den echten Keyring an. Meta-Tests halten Regeln fest
(dieselbe Kategorie wie `phase5_ui/tests/test_security_review_register.py`), nicht Verhalten.
"""
from __future__ import annotations

import importlib.util
import io
import time
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]


def _load_script(name: str):
    script_path = REPO_ROOT / "phase7_spaces_admin" / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


testcred = _load_script("testcred")


@pytest.fixture
def fake_keyring(monkeypatch):
    store: dict[tuple[str, str], str] = {}

    def fake_get_password(service, username):
        return store.get((service, username))

    def fake_set_password(service, username, password):
        store[(service, username)] = password

    def fake_delete_password(service, username):
        if (service, username) not in store:
            raise testcred.keyring.errors.PasswordDeleteError()
        del store[(service, username)]

    monkeypatch.setattr(testcred.keyring, "get_password", fake_get_password)
    monkeypatch.setattr(testcred.keyring, "set_password", fake_set_password)
    monkeypatch.setattr(testcred.keyring, "delete_password", fake_delete_password)
    return store


def _run(monkeypatch, capsys, args, stdin=""):
    monkeypatch.setattr("sys.stdin", io.StringIO(stdin))
    code = testcred.main(args)
    return code, capsys.readouterr()


def test_store_rejects_a_foreign_space(fake_keyring, monkeypatch, capsys):
    code, out = _run(
        monkeypatch, capsys, ["store"],
        stdin='{"space": "niklas", "password": "x", "totp_secret": "y"}',
    )
    assert code == 1
    assert fake_keyring == {}


def test_store_reads_only_stdin_never_argv(fake_keyring, monkeypatch, capsys):
    """`store` nimmt keine Optionen entgegen — ein Geheimnis über `argv` ist strukturell
    unmöglich, `argparse` selbst weist unbekannte Argumente ab."""
    with pytest.raises(SystemExit):
        testcred.main(["store", "--password", "x"])


def test_store_then_password_and_totp_roundtrip(fake_keyring, monkeypatch, capsys):
    from authserver.totp import generate_secret, verify

    secret = generate_secret()
    code, _ = _run(
        monkeypatch, capsys, ["store"],
        stdin=f'{{"space": "testnutzer-p7", "password": "geheim123", "totp_secret": "{secret}"}}',
    )
    assert code == 0

    code, out = _run(monkeypatch, capsys, ["password"])
    assert code == 0
    assert out.out.strip() == "geheim123"

    code, out = _run(monkeypatch, capsys, ["totp"])
    assert code == 0
    totp_code = out.out.strip()
    assert verify(secret, totp_code, now=time.time()) is not None


def test_password_and_totp_output_nothing_but_the_value(fake_keyring, monkeypatch, capsys):
    from authserver.totp import generate_secret

    secret = generate_secret()
    _run(
        monkeypatch, capsys, ["store"],
        stdin=f'{{"space": "testnutzer-p7", "password": "pw", "totp_secret": "{secret}"}}',
    )
    _, out = _run(monkeypatch, capsys, ["password"])
    assert out.out == "pw\n"
    assert out.err == ""


def test_purge_removes_the_entry(fake_keyring, monkeypatch, capsys):
    from authserver.totp import generate_secret

    secret = generate_secret()
    _run(
        monkeypatch, capsys, ["store"],
        stdin=f'{{"space": "testnutzer-p7", "password": "pw", "totp_secret": "{secret}"}}',
    )
    assert fake_keyring
    code, _ = _run(monkeypatch, capsys, ["purge"])
    assert code == 0
    assert fake_keyring == {}
    code, _ = _run(monkeypatch, capsys, ["password"])
    assert code == 1


def test_module_never_names_auth_users_or_auth_dek():
    source = (REPO_ROOT / "phase7_spaces_admin" / "scripts" / "testcred.py").read_text()
    assert "auth-users" not in source
    assert "auth-dek" not in source


def test_allowed_space_is_a_hardcoded_constant_no_space_key_service_flags():
    source = (REPO_ROOT / "phase7_spaces_admin" / "scripts" / "testcred.py").read_text()
    assert 'ALLOWED_SPACE = "testnutzer-p7"' in source
    assert testcred.ALLOWED_SPACE == "testnutzer-p7"
    assert 'add_argument("--space"' not in source
    assert 'add_argument("--key"' not in source
    assert 'add_argument("--service"' not in source
