"""`security.py` direkt getestet: Header-Inhalt + `require_csrf()` als reine Funktion, ohne
HTTP-Roundtrip (Plan §5 Step 3)."""
from __future__ import annotations

from datetime import datetime, timezone

import pytest
from authserver import crypto
from authserver.models import SessionRow
from starlette.requests import Request

from webui.config import UiSettings
from webui.errors import CsrfError
from webui.security import require_csrf, ui_security_headers

BASE_URL = "https://space.example.ts.net"


def _settings() -> UiSettings:
    return UiSettings(base_url=BASE_URL)


def _session(csrf_token: str) -> SessionRow:
    now = datetime(2026, 8, 3, 9, 0, 0, tzinfo=timezone.utc)
    return SessionRow(
        session_hash="irrelevant",
        space="niklas",
        csrf_hash=crypto.hash_secret(csrf_token),
        created_at=now,
        last_seen_at=now,
        absolute_expires_at=now,
        revoked_at=None,
        revoked_reason=None,
    )


def _request(*, method: str, headers: list[tuple[bytes, bytes]]) -> Request:
    return Request({"type": "http", "method": method, "headers": headers})


def test_csrf_get_needs_no_token():
    request = _request(method="GET", headers=[])
    require_csrf(request, _session("tok"), settings=_settings())  # wirft nicht


def test_csrf_missing_token_is_403():
    request = _request(
        method="POST",
        headers=[(b"origin", BASE_URL.encode())],
    )
    with pytest.raises(CsrfError):
        require_csrf(request, _session("tok"), settings=_settings())


def test_csrf_wrong_token_is_403():
    request = _request(
        method="POST",
        headers=[(b"origin", BASE_URL.encode()), (b"x-csrf-token", b"falscher-wert")],
    )
    with pytest.raises(CsrfError):
        require_csrf(request, _session("tok"), settings=_settings())


def test_csrf_foreign_origin_is_403():
    request = _request(
        method="POST",
        headers=[
            (b"origin", b"https://boese.example"),
            (b"x-csrf-token", b"tok"),
        ],
    )
    with pytest.raises(CsrfError):
        require_csrf(request, _session("tok"), settings=_settings())


def test_csrf_absent_origin_with_same_site_header_passes():
    request = _request(
        method="POST",
        headers=[(b"sec-fetch-site", b"same-origin"), (b"x-csrf-token", b"tok")],
    )
    require_csrf(request, _session("tok"), settings=_settings())  # wirft nicht


def test_ui_csp_has_no_unsafe_inline():
    headers = ui_security_headers(_settings())
    csp = headers["Content-Security-Policy"]
    assert "unsafe-inline" not in csp


def test_ui_csp_form_action_is_self_only():
    """Belegt, dass die UI-Header **nicht** die OAuth-Header sind (Plan §5 Step 3): die
    OAuth-Seite trägt `https://claude.ai`/`https://claude.com` in `form-action`
    (`authserver/config.py :: csp_form_action`), die UI nicht."""
    headers = ui_security_headers(_settings())
    csp = headers["Content-Security-Policy"]
    assert "form-action 'self';" in csp
    assert "claude.ai" not in csp
    assert "claude.com" not in csp
