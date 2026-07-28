"""stderr-Logging + Token-Scrubbing (Plan §4 Step 4, §8 Risiko 3). Uvicorn-Access-Log wird
separat in `app.py`/`scripts/serve.py` über `access_log=False` abgeschaltet — das Access-Log
schreibt die komplette URL inklusive Token, dieser Filter allein wäre dagegen kein Schutz.
"""
from __future__ import annotations

import logging
import re
import sys

_TOKEN_SEGMENT_RE = re.compile(r"(/mcp/)[^\s\"'/]+")

# P4 Step 6b (Plan §4): Verteidigung in der Tiefe für OAuth-Geheimnisse. Praktisch redundant zur
# eigentlichen Sicherung — `OAuthLogASGI`/`log_event()`s Feld-Whitelist lassen Passwort, TOTP-
# Code, Authorization-Code, `code_verifier` und Access-/Refresh-Token gar nicht erst in eine
# Logzeile hinein (kein Body-, kein Header-Read in `OAuthLogASGI`) — genau wie `_TOKEN_SEGMENT_RE`
# oben für den Pfad-Token bereits redundant zu `AccessLogASGI`s eigener Redaktion ist. Trotzdem
# hier ergänzt, falls je ein Aufrufer eine rohe Fehlermeldung oder einen Header-Wert durch dieses
# Modul schickt, der eines dieser Muster enthält.
#
# `_kv_pattern` deckt sowohl Form-Encoding (`code=…`, `password=…`) als auch JSON (`"access_
# token": "…"`) ab — dieselbe Geheimnis-Klasse taucht in diesem Protokoll in beiden Formen auf
# (Token-Antwort ist JSON, Formular-POST und Redirect-Query sind `x-www-form-urlencoded`). Ein
# optionales schließendes Anführungszeichen zwischen Feldname und Trenner (`"?`) reicht, um beide
# Formen mit einem Muster zu treffen.
#
# `_kv_pattern("code")` trifft NICHT auf `code_verifier=…` (der `_` bricht den Anschluss an
# `[:=]`) — exakt Plan §4s Liste, die `code=` nennt, nicht `code_verifier`. Ein PKCE-`code_
# verifier` ist deshalb ausschließlich durch die Feld-Whitelist/`OAuthLogASGI`s Body-Freiheit
# geschützt, nicht durch diesen Filter — kein Zufall, aber auch keine Lücke: dieser Filter ist
# ohnehin nur Verteidigung in der Tiefe (siehe oben), die primäre Sicherung liegt woanders.
def _kv_pattern(field: str) -> re.Pattern[str]:
    return re.compile(rf'({field}"?\s*[:=]\s*"?)[^"&\s,}}]+', re.IGNORECASE)


_SECRET_PATTERNS: tuple[re.Pattern[str], ...] = (
    _TOKEN_SEGMENT_RE,
    _kv_pattern("code"),
    _kv_pattern("access_token"),
    _kv_pattern("refresh_token"),
    _kv_pattern("password"),
    _kv_pattern("totp"),
    re.compile(r"(Authorization:\s*Bearer\s+)\S+", re.IGNORECASE),
)


def _scrub(text: str) -> str:
    for pattern in _SECRET_PATTERNS:
        text = pattern.sub(r"\1<redacted>", text)
    return text


class TokenScrubbingFilter(logging.Filter):
    """Ersetzt jedes Muster aus `_SECRET_PATTERNS` (Pfad-Token, `code=`, Access-/Refresh-Token,
    Passwort, TOTP, `Authorization: Bearer …`) durch `<redacted>` in jeder Log-Message — ein
    Geheimnis darf nie in eine Logdatei gelangen (P2-D, R5, P4 Step 6b).

    **P3-Erweiterung:** `record.msg` ist beim Request-Log (`sharefyx.request`, `request_log.py`)
    ein Feld-Dict, kein String — derselbe Filter läuft auch dort (Plan §3.1: „beide laufen durch
    TokenScrubbingFilter"), deshalb scrubbt der Filter jetzt auch String-Werte innerhalb eines
    Dicts, nicht nur `record.msg` selbst. Praktisch bereits redundant (`AccessLogASGI`/
    `OAuthLogASGI` redigieren vor dem Aufruf von `log_event()`), aber echte Verteidigung in der
    Tiefe statt eines stillen No-ops auf Dict-Payloads."""

    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            record.msg = _scrub(record.msg)
        elif isinstance(record.msg, dict):
            record.msg = {
                key: (_scrub(value) if isinstance(value, str) else value)
                for key, value in record.msg.items()
            }
        if record.args:
            record.args = tuple(
                _scrub(arg) if isinstance(arg, str) else arg for arg in record.args
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
