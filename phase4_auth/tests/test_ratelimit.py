from datetime import datetime, timedelta, timezone

import pytest

from authserver.ratelimit import (
    BASE_LOCKOUT_S,
    MAX_FAILURES,
    MAX_LOCKOUT_S,
    MAX_SPACE_LEN,
    LoginThrottle,
)
from authserver.store import AuthStore


@pytest.fixture
def clock():
    state = {"now": datetime(2026, 7, 28, 12, 0, 0, tzinfo=timezone.utc)}

    def now_fn():
        return state["now"]

    def advance(seconds=1):
        state["now"] += timedelta(seconds=seconds)

    now_fn.advance = advance
    return now_fn


@pytest.fixture
def store(tmp_path, clock):
    return AuthStore(tmp_path / "auth.sqlite3", now_fn=clock)


@pytest.fixture
def throttle(store, clock):
    return LoginThrottle(store, now_fn=clock)


def test_lockout_after_five_failures(throttle):
    assert throttle.check("niklas") is None
    for _ in range(MAX_FAILURES - 1):
        throttle.register_failure("niklas")
        assert throttle.check("niklas") is None
    throttle.register_failure("niklas")
    assert throttle.check("niklas") == BASE_LOCKOUT_S


def test_lockout_doubles(throttle, clock):
    for _ in range(MAX_FAILURES):
        throttle.register_failure("niklas")
    first_lockout = throttle.check("niklas")
    assert first_lockout == BASE_LOCKOUT_S

    clock.advance(first_lockout + 1)  # erste Sperre abgelaufen
    assert throttle.check("niklas") is None

    for _ in range(MAX_FAILURES):
        throttle.register_failure("niklas")
    second_lockout = throttle.check("niklas")
    assert second_lockout == 2 * BASE_LOCKOUT_S


def test_lockout_capped_at_24h(throttle, clock):
    remaining = None
    for _ in range(8):  # Runde 8: 900 * 2**7 = 115200s, muss auf 86400s gedeckelt werden
        for _ in range(MAX_FAILURES):
            throttle.register_failure("niklas")
        remaining = throttle.check("niklas")
        clock.advance(remaining + 1)
    assert remaining == MAX_LOCKOUT_S


def test_success_resets_counter(throttle):
    for _ in range(MAX_FAILURES):
        throttle.register_failure("niklas")
    assert throttle.check("niklas") is not None

    throttle.reset("niklas")
    assert throttle.check("niklas") is None

    # nach dem Reset zählt es wieder bei 1 los, keine Resteskalation aus dem alten Streak.
    for _ in range(MAX_FAILURES - 1):
        throttle.register_failure("niklas")
    assert throttle.check("niklas") is None


def test_register_failure_ignores_oversized_space(throttle, store):
    """S7 (Sicherheits-Review 2026-07-29): `space` kommt unauthentifiziert aus dem Formular und
    landet als PRIMARY KEY in `login_attempts` — ohne Längenbegrenzung ein Disk-DoS-Vektor."""
    huge_space = "x" * (MAX_SPACE_LEN + 1)
    throttle.register_failure(huge_space)
    assert store.get_login_attempt(huge_space) is None
    assert throttle.check(huge_space) is None


def test_register_failure_accepts_space_at_the_limit(throttle, store):
    boundary_space = "x" * MAX_SPACE_LEN
    throttle.register_failure(boundary_space)
    assert store.get_login_attempt(boundary_space) is not None


def test_check_is_readonly(throttle, store):
    for _ in range(MAX_FAILURES):
        throttle.register_failure("niklas")
    before = store.get_login_attempt("niklas")

    throttle.check("niklas")
    throttle.check("niklas")

    after = store.get_login_attempt("niklas")
    assert after == before
