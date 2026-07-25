"""stderr-Logging + Token-Scrubbing (Plan §4 Step 4, §8 Risiko 3). Uvicorn-Access-Log wird
separat in `app.py`/`scripts/serve.py` über `access_log=False` abgeschaltet — das Access-Log
schreibt die komplette URL inklusive Token, dieser Filter allein wäre dagegen kein Schutz.
"""
from __future__ import annotations

import logging
import re
import sys

_TOKEN_SEGMENT_RE = re.compile(r"(/mcp/)[^\s\"'/]+")


class TokenScrubbingFilter(logging.Filter):
    """Ersetzt `/mcp/<segment>` durch `/mcp/<redacted>` in jeder Log-Message — ein Pfad-Token
    darf nie in eine Logdatei gelangen (P2-D, R5)."""

    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            record.msg = _TOKEN_SEGMENT_RE.sub(r"\1<redacted>", record.msg)
        if record.args:
            record.args = tuple(
                _TOKEN_SEGMENT_RE.sub(r"\1<redacted>", arg) if isinstance(arg, str) else arg
                for arg in record.args
            )
        return True


def configure_logging(level: str) -> None:
    """Root-Logger auf `level`, genau ein Handler auf stderr mit `TokenScrubbingFilter`.
    Kein Handler auf stdout — stdout bleibt für maschinenlesbares JSON reserviert (Hard Rule 7).
    """
    root = logging.getLogger()
    root.setLevel(level)
    for existing in list(root.handlers):
        root.removeHandler(existing)
    handler = logging.StreamHandler(stream=sys.stderr)
    handler.addFilter(TokenScrubbingFilter())
    root.addHandler(handler)
