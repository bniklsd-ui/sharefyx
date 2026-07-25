import pytest

from mcpserver import credentials


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
