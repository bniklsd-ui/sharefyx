import re
from pathlib import Path

import pytest

from authserver import config
from authserver.config import (
    DEK_LEN,
    decode_data_encryption_key,
    encode_data_encryption_key,
    generate_data_encryption_key,
    load_auth_settings,
    load_data_encryption_key,
)

_FORBIDDEN_IMPORT = re.compile(r"^\s*(import|from)\s+(mcpserver|storage)\b", re.MULTILINE)


def test_authserver_does_not_import_mcpserver():
    """P4-A/P4-C, „nicht verhandelbar" (Phase-Head, Harte Regeln): `authserver` kennt weder
    `mcpserver` noch `storage`. Referenziert seit Step 1 im Phase-Head, aber nie geschrieben —
    Lücke geschlossen in Step 4, als drei neue Dateien (`clients.py`, `metadata.py`,
    `routes.py`) unter dieselbe Regel fielen. Grep über den Quellcode (nicht nur Docstrings:
    `re.MULTILINE`-Anker auf Zeilenanfang schließt Erwähnungen in Prosa aus, echte
    `import`/`from`-Statements stehen immer am Zeilenanfang)."""
    authserver_dir = Path(__file__).resolve().parent.parent / "authserver"
    offenders = [
        f"{path.name}: {match.group(0).strip()}"
        for path in sorted(authserver_dir.glob("*.py"))
        for match in _FORBIDDEN_IMPORT.finditer(path.read_text(encoding="utf-8"))
    ]
    assert offenders == [], f"authserver importiert mcpserver/storage: {offenders}"


def test_load_auth_settings_requires_base_url_in_oauth_mode():
    with pytest.raises(ValueError):
        load_auth_settings({"SPACE_AUTH_DB": "/tmp/auth.sqlite3"})


def test_load_auth_settings_rejects_non_https_base_url():
    with pytest.raises(ValueError):
        load_auth_settings(
            {"SPACE_PUBLIC_BASE_URL": "http://example.ts.net", "SPACE_AUTH_DB": "/tmp/auth.sqlite3"}
        )


def test_load_auth_settings_rejects_trailing_slash():
    with pytest.raises(ValueError):
        load_auth_settings(
            {
                "SPACE_PUBLIC_BASE_URL": "https://example.ts.net/",
                "SPACE_AUTH_DB": "/tmp/auth.sqlite3",
            }
        )


def test_load_auth_settings_rejects_query_or_fragment():
    with pytest.raises(ValueError):
        load_auth_settings(
            {
                "SPACE_PUBLIC_BASE_URL": "https://example.ts.net?x=1",
                "SPACE_AUTH_DB": "/tmp/auth.sqlite3",
            }
        )


def test_load_auth_settings_requires_db_path_or_state_directory():
    with pytest.raises(ValueError):
        load_auth_settings({"SPACE_PUBLIC_BASE_URL": "https://example.ts.net"})


def test_load_auth_settings_db_path_falls_back_to_state_directory():
    settings = load_auth_settings(
        {"SPACE_PUBLIC_BASE_URL": "https://example.ts.net", "STATE_DIRECTORY": "/var/lib/sharefyx"}
    )
    assert settings.db_path == Path("/var/lib/sharefyx/auth.sqlite3")


def test_load_auth_settings_defaults():
    settings = load_auth_settings(
        {"SPACE_PUBLIC_BASE_URL": "https://example.ts.net", "SPACE_AUTH_DB": "/tmp/auth.sqlite3"}
    )
    assert settings.mode == "oauth"
    assert settings.allowed_redirect_origins == ("https://claude.ai", "https://claude.com")
    assert settings.access_ttl_s == 3600
    assert settings.refresh_ttl_s == 2592000
    assert settings.code_ttl_s == 60
    assert settings.request_ttl_s == 600
    assert settings.hsts is True
    assert settings.issuer == "https://example.ts.net"
    assert settings.resource == "https://example.ts.net/mcp"


def test_load_auth_settings_rejects_unknown_mode():
    with pytest.raises(ValueError):
        load_auth_settings(
            {
                "SPACE_AUTH_MODE": "bogus",
                "SPACE_PUBLIC_BASE_URL": "https://example.ts.net",
                "SPACE_AUTH_DB": "/tmp/auth.sqlite3",
            }
        )


def test_load_auth_settings_rejects_token_mode_after_the_cut():
    """Schnitt, 2026-07-30 (Runbook-Schritt 8): `token`/`both` sind mit `TokenPathASGI`/
    `AuthModeASGI` entfernt — `_VALID_MODES` lässt nur noch `oauth` zu, siehe `config.py`."""
    with pytest.raises(ValueError):
        load_auth_settings(
            {
                "SPACE_AUTH_MODE": "token",
                "SPACE_PUBLIC_BASE_URL": "https://example.ts.net",
                "SPACE_AUTH_DB": "/tmp/auth.sqlite3",
            }
        )


def test_load_auth_settings_hsts_can_be_disabled():
    settings = load_auth_settings(
        {
            "SPACE_PUBLIC_BASE_URL": "https://example.ts.net",
            "SPACE_AUTH_DB": "/tmp/auth.sqlite3",
            "SPACE_OAUTH_HSTS": "off",
        }
    )
    assert settings.hsts is False


def test_load_auth_settings_parses_redirect_origins():
    settings = load_auth_settings(
        {
            "SPACE_PUBLIC_BASE_URL": "https://example.ts.net",
            "SPACE_AUTH_DB": "/tmp/auth.sqlite3",
            "SPACE_OAUTH_ALLOWED_REDIRECT_ORIGINS": "https://a.example, https://b.example",
        }
    )
    assert settings.allowed_redirect_origins == ("https://a.example", "https://b.example")


def test_load_auth_settings_invalid_ttl_raises():
    with pytest.raises(ValueError):
        load_auth_settings(
            {
                "SPACE_PUBLIC_BASE_URL": "https://example.ts.net",
                "SPACE_AUTH_DB": "/tmp/auth.sqlite3",
                "SPACE_OAUTH_ACCESS_TTL_S": "not-a-number",
            }
        )


# -- load_data_encryption_key (Plan §2.4, P5-J) --------------------------------------------


@pytest.fixture
def fake_keyring(monkeypatch):
    """Wie `test_users.py`s gleichnamige Fixture, hier gegen `config.keyring` statt
    `users.keyring` — zwei Module importieren `keyring` jetzt (siehe Docstring-Korrektur in
    `users.py`), jedes über sein eigenes In-Memory-Double."""
    store: dict[tuple[str, str], str] = {}

    def fake_get_password(service, username):
        return store.get((service, username))

    def fake_set_password(service, username, password):
        store[(service, username)] = password

    monkeypatch.setattr(config.keyring, "get_password", fake_get_password)
    monkeypatch.setattr(config.keyring, "set_password", fake_set_password)
    return store


def test_generate_encode_decode_roundtrip():
    key = generate_data_encryption_key()
    assert len(key) == DEK_LEN
    encoded = encode_data_encryption_key(key)
    assert decode_data_encryption_key(encoded, origin="test") == key


def test_encode_rejects_wrong_length():
    with pytest.raises(ValueError):
        encode_data_encryption_key(b"too-short")


def test_decode_rejects_wrong_length():
    with pytest.raises(ValueError):
        decode_data_encryption_key(encode_data_encryption_key(b"x" * 16), origin="test")


def test_decode_rejects_invalid_base64():
    with pytest.raises(ValueError):
        decode_data_encryption_key("not base64 at all!!", origin="test")


def test_load_dek_returns_none_when_absent(fake_keyring):
    assert load_data_encryption_key({}) is None


def test_load_dek_prefers_credentials_dir(tmp_path, fake_keyring):
    key = generate_data_encryption_key()
    (tmp_path / "auth-dek").write_text(encode_data_encryption_key(key), encoding="utf-8")
    fake_keyring[("nikinger-space", "auth-dek")] = encode_data_encryption_key(
        generate_data_encryption_key()
    )  # muss ignoriert werden

    result = load_data_encryption_key({"CREDENTIALS_DIRECTORY": str(tmp_path)})
    assert result == key


def test_load_dek_falls_back_to_keyring(tmp_path, fake_keyring):
    key = generate_data_encryption_key()
    fake_keyring[("nikinger-space", "auth-dek")] = encode_data_encryption_key(key)

    result = load_data_encryption_key({"CREDENTIALS_DIRECTORY": str(tmp_path)})  # Datei fehlt
    assert result == key


def test_load_dek_raises_on_malformed_credential_file(tmp_path, fake_keyring):
    (tmp_path / "auth-dek").write_text("not-valid-base64!!", encoding="utf-8")
    with pytest.raises(ValueError):
        load_data_encryption_key({"CREDENTIALS_DIRECTORY": str(tmp_path)})
