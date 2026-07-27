import logging

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
