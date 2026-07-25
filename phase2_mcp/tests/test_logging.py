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
