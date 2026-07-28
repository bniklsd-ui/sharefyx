import logging

import pytest

from mcpserver.logging_setup import TokenScrubbingFilter


def test_scrubbing_filter_redacts_token_in_message():
    record = logging.LogRecord(
        name="test", level=logging.INFO, pathname=__file__, lineno=1,
        msg="request to /mcp/supersecrettoken123 failed", args=(), exc_info=None,
    )

    TokenScrubbingFilter().filter(record)

    assert "supersecrettoken123" not in record.msg
    assert "/mcp/<redacted>" in record.msg


def test_scrubbing_filter_redacts_token_in_dict_message():
    """P3-Erweiterung (`request_log.py`): `record.msg` ist beim Request-Log ein Feld-Dict, kein
    String — derselbe Filter muss auch dort greifen, sonst wäre er auf diesem Pfad ein No-op."""
    record = logging.LogRecord(
        name="test", level=logging.INFO, pathname=__file__, lineno=1,
        msg={"ev": "http", "path": "/mcp/supersecrettoken123", "ms": 1}, args=(), exc_info=None,
    )

    TokenScrubbingFilter().filter(record)

    assert record.msg["path"] == "/mcp/<redacted>"
    assert record.msg["ms"] == 1


@pytest.mark.parametrize(
    "message,secret",
    [
        ("redirect to /cb?code=s3cr3t-code&state=x", "s3cr3t-code"),
        ('{"access_token": "s3cr3t-access"}', "s3cr3t-access"),
        ('{"refresh_token": "s3cr3t-refresh"}', "s3cr3t-refresh"),
        ("password=hunter2", "hunter2"),
        ("totp=123456", "123456"),
        ("Authorization: Bearer s3cr3t-bearer-tok", "s3cr3t-bearer-tok"),
    ],
)
def test_scrubbing_filter_redacts_oauth_secrets(message, secret):
    """P4 Step 6b (Plan §4): `_SECRET_PATTERNS`-Erweiterung — Verteidigung in der Tiefe, falls
    je eine rohe Fehlermeldung oder ein Header-Wert eines dieser Muster durch dieses Modul
    laufen sollte (`OAuthLogASGI` selbst liest weder Body noch Header, siehe `request_log.py`)."""
    record = logging.LogRecord(
        name="test", level=logging.INFO, pathname=__file__, lineno=1, msg=message, args=(),
        exc_info=None,
    )

    TokenScrubbingFilter().filter(record)

    assert "<redacted>" in record.msg
    assert secret not in record.msg
