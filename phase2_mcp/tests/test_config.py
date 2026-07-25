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
