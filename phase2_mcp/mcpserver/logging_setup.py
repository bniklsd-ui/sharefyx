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
    darf nie in eine Logdatei gelangen (P2-D, R5).

    **P3-Erweiterung:** `record.msg` ist beim Request-Log (`sharefyx.request`, `request_log.py`)
    ein Feld-Dict, kein String — derselbe Filter läuft auch dort (Plan §3.1: „beide laufen durch
    TokenScrubbingFilter"), deshalb scrubbt der Filter jetzt auch String-Werte innerhalb eines
    Dicts, nicht nur `record.msg` selbst. Praktisch bereits redundant (`AccessLogASGI` redigiert
    den Pfad vor dem Aufruf von `log_event()`), aber echte Verteidigung in der Tiefe statt eines
    stillen No-ops auf Dict-Payloads."""

    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            record.msg = _TOKEN_SEGMENT_RE.sub(r"\1<redacted>", record.msg)
        elif isinstance(record.msg, dict):
            record.msg = {
                key: (
                    _TOKEN_SEGMENT_RE.sub(r"\1<redacted>", value)
                    if isinstance(value, str)
                    else value
                )
                for key, value in record.msg.items()
            }
        if record.args:
            record.args = tuple(
                _TOKEN_SEGMENT_RE.sub(r"\1<redacted>", arg) if isinstance(arg, str) else arg
                for arg in record.args
            )
        return True


def configure_logging(level: str) -> None:
    """Root-Logger auf `level`, genau ein Handler auf stderr mit `TokenScrubbingFilter`.
    Kein Handler auf stdout — stdout bleibt für maschinenlesbares JSON reserviert (Hard Rule 7).
    Richtet danach den separaten `sharefyx.request`-Logger ein (P3 Step 2).
    """
    root = logging.getLogger()
    root.setLevel(level)
    for existing in list(root.handlers):
        root.removeHandler(existing)
    handler = logging.StreamHandler(stream=sys.stderr)
    handler.addFilter(TokenScrubbingFilter())
    root.addHandler(handler)

    _configure_request_logger(level)


def _configure_request_logger(level: str) -> None:
    """Eigener Logger `sharefyx.request` (P3 Step 2, Plan §3.1): `JsonLineFormatter` statt
    Text, `TokenScrubbingFilter` (derselbe Filter, keine Kopie), `propagate = False` — die
    Menschen-Logs auf dem Root-Logger bleiben unberührt.

    **Lazy Import, bewusst:** `request_log.py` importiert `_TOKEN_SEGMENT_RE` aus diesem Modul
    auf Top-Level; ein Top-Level-Import von `request_log` hier würde einen Zirkelimport öffnen.
    Zum Zeitpunkt dieses Funktionsaufrufs ist `logging_setup` bereits vollständig geladen, der
    Lazy-Import ist deshalb sicher.
    """
    from .request_log import LOGGER_NAME, JsonLineFormatter

    request_logger = logging.getLogger(LOGGER_NAME)
    for existing in list(request_logger.handlers):
        request_logger.removeHandler(existing)
    request_logger.setLevel(level)
    request_logger.propagate = False

    handler = logging.StreamHandler(stream=sys.stderr)
    handler.setFormatter(JsonLineFormatter())
    handler.addFilter(TokenScrubbingFilter())
    request_logger.addHandler(handler)
