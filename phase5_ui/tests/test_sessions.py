"""`SessionManager` direkt getestet, ohne HTTP (Plan §5 Step 3) — Login/Logout über echtes
HTTP steht in `test_routes_auth.py`."""
from __future__ import annotations

import sqlite3

from starlette.requests import Request
from starlette.responses import Response

from webui.config import COOKIE_NAME

SPACE = "niklas"  # dieselbe Konstante wie in conftest.py — Muster wie test_flows.py/test_routes.py


def _request_with_cookie(session_id: str | None) -> Request:
    headers = [(b"cookie", f"{COOKIE_NAME}={session_id}".encode())] if session_id else []
    return Request({"type": "http", "method": "GET", "headers": headers})


def test_session_cookie_has_host_prefix_and_all_flags(sessions):
    response = Response()
    sessions.issue(response, space=SPACE)

    set_cookie = response.headers["set-cookie"]
    assert set_cookie.startswith(f"{COOKIE_NAME}=")
    assert COOKIE_NAME.startswith("__Host-")
    assert "Path=/" in set_cookie
    assert "; Secure" in set_cookie
    assert "HttpOnly" in set_cookie
    assert "samesite=strict" in set_cookie.lower()


def test_session_cookie_has_no_domain_attribute(sessions):
    response = Response()
    sessions.issue(response, space=SPACE)

    assert "domain=" not in response.headers["set-cookie"].lower()


def test_session_id_is_never_stored_in_plaintext(sessions, tmp_path):
    response = Response()
    csrf_token = sessions.issue(response, space=SPACE)
    session_id = response.headers["set-cookie"].split(";")[0].split("=", 1)[1]

    db_files = list(tmp_path.glob("*.sqlite3"))
    assert len(db_files) == 1
    conn = sqlite3.connect(db_files[0])
    try:
        rows = conn.execute("SELECT session_hash, csrf_hash FROM ui_sessions").fetchall()
    finally:
        conn.close()

    assert len(rows) == 1
    session_hash, csrf_hash = rows[0]
    assert session_id != session_hash
    assert session_id not in session_hash
    assert csrf_token != csrf_hash
    assert csrf_token not in csrf_hash


def test_idle_timeout_expires_session(sessions, clock):
    response = Response()
    sessions.issue(response, space=SPACE)
    session_id = response.headers["set-cookie"].split(";")[0].split("=", 1)[1]

    clock.advance(12 * 3600 + 1)  # eine Sekunde über dem Idle-Timeout (P5-E: 12h)
    assert sessions.load(_request_with_cookie(session_id)) is None


def test_absolute_timeout_expires_session_despite_activity(sessions, clock):
    response = Response()
    sessions.issue(response, space=SPACE)
    session_id = response.headers["set-cookie"].split(";")[0].split("=", 1)[1]

    # Aktivität alle 6 Stunden — bleibt unter dem Idle-Timeout (12h), überschreitet aber das
    # Absolut-Timeout (7d, P5-E). Kein Idle-Timeout darf das je verhindern.
    step = 6 * 3600
    elapsed = 0
    session = None
    while elapsed < 7 * 24 * 3600 + step:
        clock.advance(step)
        elapsed += step
        session = sessions.load(_request_with_cookie(session_id))
        if session is None:
            break

    assert session is None
