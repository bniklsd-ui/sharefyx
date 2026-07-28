from pathlib import Path

import pytest

from authserver.config import load_auth_settings


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


def test_load_auth_settings_token_mode_does_not_require_base_url():
    settings = load_auth_settings({"SPACE_AUTH_MODE": "token", "SPACE_AUTH_DB": "/tmp/auth.sqlite3"})
    assert settings.mode == "token"
    assert settings.base_url == ""


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
