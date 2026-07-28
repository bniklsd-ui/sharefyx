"""OAuth-Fehlerantworten, einheitlich (Plan §2.4). Ausschließlich RFC-6749-Codes — niemals ein
eigener Code, niemals eine Beschreibung, die zwischen „unbekannt", „abgelaufen" und „widerrufen"
unterscheidet. Response-Bau (JSON vs. Redirect) folgt in Step 5 (`flows.py`/`routes.py`).

**Additiv, Step 4:** `DCR_ERROR_CODES`/`DCRError` — RFC-7591-Fehlercodes für `/oauth/register`,
bewusst als **eigenes** Set und eigene Exception, nicht in `OAUTH_ERROR_CODES`/`OAuthError`
gemischt. Eine Vermischung würde `invalid_redirect_uri`/`invalid_client_metadata` fälschlich
auch aus `/oauth/authorize` oder `/oauth/token` als gültige Antworten erscheinen lassen, wo sie
laut RFC 6749 nicht hingehören (relevant für Step 5s `test_all_token_errors_use_invalid_grant`).
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


DCR_ERROR_CODES: frozenset[str] = frozenset(
    {
        "invalid_redirect_uri",
        "invalid_client_metadata",
        "invalid_software_statement",
        "unapproved_software_statement",
    }
)


class DCRError(Exception):
    """Trägt ausschließlich einen RFC-7591-Fehlercode (nur für `/oauth/register`)."""

    def __init__(self, code: str) -> None:
        if code not in DCR_ERROR_CODES:
            raise ValueError(f"kein gültiger RFC-7591-Fehlercode: {code!r}")
        super().__init__(code)
        self.code = code
