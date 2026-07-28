"""OAuth-Fehlerantworten, einheitlich (Plan §2.4). Ausschließlich RFC-6749-Codes — niemals ein
eigener Code, niemals eine Beschreibung, die zwischen „unbekannt", „abgelaufen" und „widerrufen"
unterscheidet. Response-Bau (JSON vs. Redirect) folgt in Step 5 (`flows.py`/`routes.py`).
"""
from __future__ import annotations

OAUTH_ERROR_CODES: frozenset[str] = frozenset(
    {
        "invalid_request",
        "invalid_client",
        "invalid_grant",
        "unauthorized_client",
        "unsupported_grant_type",
        "unsupported_response_type",
        "invalid_scope",
        "invalid_target",
        "access_denied",
    }
)


class OAuthError(Exception):
    """Trägt ausschließlich einen RFC-6749-Code, keine unterscheidbare Detailbeschreibung."""

    def __init__(self, code: str) -> None:
        if code not in OAUTH_ERROR_CODES:
            raise ValueError(f"kein gültiger RFC-6749-Fehlercode: {code!r}")
        super().__init__(code)
        self.code = code
