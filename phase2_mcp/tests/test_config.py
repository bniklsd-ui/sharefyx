from pathlib import Path

import pytest

from mcpserver.config import load_settings


def test_load_settings_requires_data_root():
    with pytest.raises(ValueError):
        load_settings({})


def test_load_settings_defaults():
    settings = load_settings({"SPACE_DATA_ROOT": "/tmp/space-data"})
    assert settings.data_root == Path("/tmp/space-data")
    assert settings.host == "127.0.0.1"
    assert settings.port == 8765
    assert settings.log_level == "INFO"


def test_load_settings_port_invalid_raises():
    with pytest.raises(ValueError):
        load_settings({"SPACE_DATA_ROOT": "/tmp/space-data", "SPACE_PORT": "not-a-number"})


def test_allowed_hosts_defaults_to_empty():
    settings = load_settings({"SPACE_DATA_ROOT": "/tmp/space-data"})
    assert settings.allowed_hosts == ()


def test_allowed_hosts_parses_comma_list():
    settings = load_settings(
        {
            "SPACE_DATA_ROOT": "/tmp/space-data",
            "SPACE_ALLOWED_HOSTS": "one.example,two.example",
        }
    )
    assert settings.allowed_hosts == ("one.example", "two.example")


def test_allowed_hosts_strips_whitespace_and_drops_empties():
    settings = load_settings(
        {
            "SPACE_DATA_ROOT": "/tmp/space-data",
            "SPACE_ALLOWED_HOSTS": " one.example ,, two.example ,",
        }
    )
    assert settings.allowed_hosts == ("one.example", "two.example")
