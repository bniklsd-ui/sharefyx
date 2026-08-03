"""Gemeinsame Fixtures für die Step-3-Tests (Sessions, CSRF, Login/Logout) — Muster wie
`phase4_auth/tests/test_flows.py`: eine injizierbare Uhr, eine temporäre `AuthStore`, ein
provisionierter Nutzer. `base_url` ist bewusst `https://…` (nicht `http://testserver` wie in
`phase2_mcp/tests/test_app.py`s Bearer-Tests): `__Host-`-Cookies verlangen `Secure`, httpx sendet
ein `Secure`-Cookie nicht über `http://` zurück — ohne `https://` würden die Session-Tests grün
aussehen, ohne dass das Cookie je tatsächlich zurückreist.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from authserver import passwords, totp
from authserver.secretbox import KEY_LEN, seal
from authserver.store import AuthStore
from authserver.userdir import UserDirectory
from starlette.applications import Starlette

from webui.config import UiSettings
from webui.routes_auth import ui_auth_routes
from webui.sessions import SessionManager

BASE_URL = "https://space.example.ts.net"
SPACE = "niklas"
PASSWORD = "correct horse battery staple"
TOTP_SECRET = totp.generate_secret()


@pytest.fixture
def clock():
    state = {"now": datetime(2026, 8, 3, 9, 0, 0, tzinfo=timezone.utc)}

    def now_fn():
        return state["now"]

    def advance(seconds=1):
        state["now"] += timedelta(seconds=seconds)

    now_fn.advance = advance
    return now_fn


@pytest.fixture
def store(tmp_path, clock) -> AuthStore:
    return AuthStore(tmp_path / "auth.sqlite3", now_fn=clock)


@pytest.fixture
def ui_settings() -> UiSettings:
    return UiSettings(base_url=BASE_URL)


@pytest.fixture
def dek() -> bytes:
    return bytes([0x5A]) * KEY_LEN


@pytest.fixture
def users(store, dek) -> UserDirectory:
    store.upsert_user(
        SPACE,
        password_hash=passwords.hash_password(PASSWORD),
        totp_secret_enc=seal(TOTP_SECRET.encode("ascii"), key=dek, aad=SPACE.encode("utf-8")),
        totp_alg="SHA1",
        totp_confirmed_at=None,
        status="active",
    )
    return UserDirectory(store, dek=dek)


@pytest.fixture
def sessions(store, ui_settings) -> SessionManager:
    return SessionManager(store, settings=ui_settings)


@pytest.fixture
def app(ui_settings, store, users, sessions) -> Starlette:
    return Starlette(routes=ui_auth_routes(ui_settings, store, users, sessions))


@pytest.fixture
def totp_code(clock):
    """Fixture statt Modulfunktion (anders als `test_flows.py`s freie `_totp_code()`): `users`
    provisioniert `TOTP_SECRET` einmal zentral hier in `conftest.py`, mehrere Testdateien
    brauchen einen passenden Code dazu — ein Import des Secrets über Dateigrenzen hinweg wäre
    genau die Kopplung, die dieses Repo bei Test-Konstanten sonst vermeidet (siehe
    Moduldocstring); die Fixture liefert stattdessen eine aufrufbare Closure, kein Secret."""
    def _make(secret: str = TOTP_SECRET) -> str:
        counter = int(clock().timestamp() // 30)
        return totp.totp_at(secret, counter, algo="SHA1")
    return _make
