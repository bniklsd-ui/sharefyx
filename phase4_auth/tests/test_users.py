import importlib.util
import json
import logging
from pathlib import Path

import pytest

from authserver import users

REPO_ROOT = Path(__file__).resolve().parents[2]


def _load_script(name: str):
    """Lädt ein Skript aus `phase4_auth/scripts/` per Pfad — die Skripte liegen in keinem
    Python-Paket, ein normaler Import über `sys.path` funktioniert deshalb nicht (gleiches
    Muster wie `phase2_mcp/tests/test_credentials.py :: _load_export_module`)."""
    script_path = REPO_ROOT / "phase4_auth" / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def fake_keyring(monkeypatch):
    """Ersetzt die beiden `keyring`-Funktionen, die `users.py` aufruft, durch ein In-Memory-Dict.
    Kein Test in dieser Datei fasst den echten Keyring an."""
    store: dict[tuple[str, str], str] = {}

    def fake_get_password(service, username):
        return store.get((service, username))

    def fake_set_password(service, username, password):
        store[(service, username)] = password

    monkeypatch.setattr(users.keyring, "get_password", fake_get_password)
    monkeypatch.setattr(users.keyring, "set_password", fake_set_password)
    return store


def test_load_users_from_keyring_missing_key_returns_empty(fake_keyring):
    assert users.load_users_from_keyring() == {}


def test_save_load_roundtrip_with_fake_backend(fake_keyring):
    record = {"pwd": "$argon2id$...", "totp": "SEED", "totp_alg": "SHA1", "created_at": "2026-07-28T00:00:00Z"}
    users.save_users({"niklas": record})
    assert users.load_users_from_keyring() == {"niklas": record}


def test_load_users_prefers_credentials_dir(tmp_path, monkeypatch, fake_keyring):
    monkeypatch.setenv("CREDENTIALS_DIRECTORY", str(tmp_path))
    (tmp_path / users.CREDENTIAL_NAME).write_text(
        json.dumps({"fromfile": {"pwd": "x"}}), encoding="utf-8"
    )
    users.save_users({"fromkeyring": {"pwd": "y"}})  # muss ignoriert werden

    assert users.load_users() == {"fromfile": {"pwd": "x"}}


def test_load_users_falls_back_to_keyring(monkeypatch, fake_keyring):
    monkeypatch.delenv("CREDENTIALS_DIRECTORY", raising=False)
    users.save_users({"fromkeyring": {"pwd": "y"}})

    assert users.load_users() == {"fromkeyring": {"pwd": "y"}}


def test_load_users_warns_and_falls_back_when_file_missing(tmp_path, monkeypatch, fake_keyring, caplog):
    monkeypatch.setenv("CREDENTIALS_DIRECTORY", str(tmp_path))  # Datei existiert bewusst nicht
    users.save_users({"fromkeyring": {"pwd": "y"}})

    with caplog.at_level(logging.WARNING):
        result = users.load_users()

    assert result == {"fromkeyring": {"pwd": "y"}}
    assert "fehlt" in caplog.text


def test_load_users_raises_on_malformed_content(tmp_path, monkeypatch, fake_keyring):
    monkeypatch.setenv("CREDENTIALS_DIRECTORY", str(tmp_path))
    (tmp_path / users.CREDENTIAL_NAME).write_text("nicht-json", encoding="utf-8")

    with pytest.raises(ValueError):
        users.load_users()


def test_load_users_raises_on_wrong_shape(tmp_path, monkeypatch, fake_keyring):
    monkeypatch.setenv("CREDENTIALS_DIRECTORY", str(tmp_path))
    (tmp_path / users.CREDENTIAL_NAME).write_text(json.dumps({"niklas": "not-a-dict"}), encoding="utf-8")

    with pytest.raises(ValueError):
        users.load_users()


# --- Skripte: provision_user.py, export_auth_users.py ---


def test_provision_prints_secret_once_and_never_writes_a_file(fake_keyring, capsys, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)  # falls das Skript je versehentlich relativ schriebe, fällt es hier auf
    provision_user = _load_script("provision_user")
    passwords_seen = iter(["neues-passwort", "neues-passwort"])

    exit_code = provision_user.main(["--space", "niklas"], get_password=lambda prompt: next(passwords_seen))
    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out.count("otpauth://totp/") == 1
    assert list(tmp_path.iterdir()) == []  # kein Datei-Nebeneffekt

    stored = users.load_users_from_keyring()["niklas"]
    assert stored["totp"] in captured.out  # der Seed im URI muss zum gespeicherten passen
    assert "neues-passwort" not in captured.out
    assert "neues-passwort" not in captured.err


def test_provision_aborts_on_password_mismatch(fake_keyring, capsys):
    provision_user = _load_script("provision_user")
    passwords_seen = iter(["a", "b"])

    exit_code = provision_user.main(["--space", "niklas"], get_password=lambda prompt: next(passwords_seen))

    assert exit_code == 1
    assert users.load_users_from_keyring() == {}


def test_export_contains_no_password_plaintext(fake_keyring, capsys):
    provision_user = _load_script("provision_user")
    passwords_seen = iter(["mein-geheimes-passwort", "mein-geheimes-passwort"])
    provision_user.main(["--space", "niklas"], get_password=lambda prompt: next(passwords_seen))
    capsys.readouterr()  # provision_user's Ausgabe verwerfen

    export_auth_users = _load_script("export_auth_users")
    export_auth_users.main([])
    captured = capsys.readouterr()

    assert "mein-geheimes-passwort" not in captured.out
    assert "mein-geheimes-passwort" not in captured.err
    payload = json.loads(captured.out)
    assert payload["niklas"]["pwd"].startswith("$argon2id$")
