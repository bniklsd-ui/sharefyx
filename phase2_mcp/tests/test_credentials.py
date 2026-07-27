import importlib.util
import json
import logging
from pathlib import Path

import pytest

from mcpserver import credentials

REPO_ROOT = Path(__file__).resolve().parents[2]


def _load_export_module():
    """Lädt `phase3_edge/scripts/export_space_map.py` per Pfad — das Skript liegt in keinem
    Python-Paket (Plan §1.2: `phase3_edge/` ist bewusst kein Paket), ein normaler Import über
    `sys.path` funktioniert deshalb nicht."""
    script_path = REPO_ROOT / "phase3_edge" / "scripts" / "export_space_map.py"
    spec = importlib.util.spec_from_file_location("export_space_map", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def fake_keyring(monkeypatch):
    """Ersetzt die beiden `keyring`-Funktionen, die `credentials.py` aufruft, durch ein
    In-Memory-Dict. Kein Test in dieser Datei fasst den echten Keyring an.
    """
    store: dict[tuple[str, str], str] = {}

    def fake_get_password(service, username):
        return store.get((service, username))

    def fake_set_password(service, username, password):
        store[(service, username)] = password

    monkeypatch.setattr(credentials.keyring, "get_password", fake_get_password)
    monkeypatch.setattr(credentials.keyring, "set_password", fake_set_password)
    return store


def test_hash_token_is_stable_hex64():
    token = "irgendein-token-wert"
    first = credentials.hash_token(token)
    second = credentials.hash_token(token)
    assert first == second
    assert len(first) == 64
    assert all(c in "0123456789abcdef" for c in first)


def test_generate_token_length_and_uniqueness():
    tokens = {credentials.generate_token() for _ in range(50)}
    assert len(tokens) == 50
    assert all(len(t) >= 32 for t in tokens)


def test_load_space_map_missing_key_returns_empty(fake_keyring):
    assert credentials.load_space_map() == {}


def test_save_load_roundtrip_with_fake_backend(fake_keyring):
    credentials.save_space_map({"deadbeef": "nikinger"})
    assert credentials.load_space_map() == {"deadbeef": "nikinger"}


def test_issue_stores_only_hash(fake_keyring):
    token = credentials.issue("nikinger")

    mapping = credentials.load_space_map()
    assert token not in mapping
    assert token not in mapping.values()
    assert mapping[credentials.hash_token(token)] == "nikinger"


def test_revoke_removes_all_hashes_of_space(fake_keyring):
    first = credentials.issue("nikinger")
    second = credentials.issue("nikinger")
    other = credentials.issue("kollege")

    removed = credentials.revoke("nikinger")

    assert removed == 2
    mapping = credentials.load_space_map()
    assert credentials.hash_token(first) not in mapping
    assert credentials.hash_token(second) not in mapping
    assert credentials.hash_token(other) in mapping


# --- P3 Step 3: load_space_map() Credentials-Verzeichnis zuerst, Keyring als Fallback ---


def test_load_space_map_prefers_credentials_dir(tmp_path, monkeypatch, fake_keyring):
    monkeypatch.setenv("CREDENTIALS_DIRECTORY", str(tmp_path))
    (tmp_path / credentials.CREDENTIAL_NAME).write_text(
        json.dumps({"fromfile": "niklas"}), encoding="utf-8"
    )
    credentials.save_space_map({"fromkeyring": "fabian"})  # muss ignoriert werden

    assert credentials.load_space_map() == {"fromfile": "niklas"}


def test_load_space_map_falls_back_when_credentials_dir_unset(monkeypatch, fake_keyring):
    monkeypatch.delenv("CREDENTIALS_DIRECTORY", raising=False)
    credentials.save_space_map({"fromkeyring": "fabian"})

    assert credentials.load_space_map() == {"fromkeyring": "fabian"}


def test_load_space_map_falls_back_when_credential_file_missing(
    tmp_path, monkeypatch, fake_keyring, caplog
):
    monkeypatch.setenv("CREDENTIALS_DIRECTORY", str(tmp_path))  # Datei existiert bewusst nicht
    credentials.save_space_map({"fromkeyring": "fabian"})

    with caplog.at_level(logging.WARNING):
        result = credentials.load_space_map()

    assert result == {"fromkeyring": "fabian"}
    assert "fehlt" in caplog.text


def test_load_space_map_raises_on_malformed_credential(tmp_path, monkeypatch, fake_keyring):
    monkeypatch.setenv("CREDENTIALS_DIRECTORY", str(tmp_path))
    (tmp_path / credentials.CREDENTIAL_NAME).write_text("nicht-json", encoding="utf-8")

    with pytest.raises(ValueError):
        credentials.load_space_map()


# --- P3 Step 3: export_space_map.py — liest explizit den Keyring, nie die Verzweigung ---


def test_export_writes_json_to_stdout_and_note_to_stderr(fake_keyring, capsys):
    credentials.issue("niklas")
    export_space_map = _load_export_module()

    exit_code = export_space_map.main([])
    captured = capsys.readouterr()

    assert exit_code == 0
    payload = json.loads(captured.out)
    assert len(payload) == 1
    assert "Einträge exportiert" in captured.err
    assert "keine Tokens" in captured.err


def test_export_contains_no_plaintext_token(fake_keyring, capsys):
    token = credentials.issue("niklas")
    export_space_map = _load_export_module()

    export_space_map.main([])
    captured = capsys.readouterr()

    assert token not in captured.out
    assert token not in captured.err
