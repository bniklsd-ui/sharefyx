"""Fehlversuchsbremse für den Login (Plan §2.7). Pro Space, nicht pro IP — der Login läuft im
Browser des Menschen, dessen IP wechselt, während der Angreifer seine wechseln kann. Bewusst
akzeptierter Preis: ein Aussperr-DoS gegen einen der beiden Nutzer; Gegenmittel ist
`authctl.py unlock`, eine SSH-Sitzung entfernt. Führt selbst **kein SQL** — jeder Zugriff auf
`login_attempts` läuft über `AuthStore` (Step-3-Regel: SQL nur in `store.py`).

**Eskalationsformel** (vom Plan nur als Konstanten vorgegeben, hier festgelegt): `failures`
zählt monoton hoch, sooft sie ein Vielfaches von `MAX_FAILURES` erreichen, wird eine neue Sperre
gesetzt, deren Dauer sich gegenüber der vorherigen verdoppelt (`BASE_LOCKOUT_S * 2**(n-1)`,
gedeckelt bei `MAX_LOCKOUT_S`). Das `WINDOW_S`-Vergessen sparsamer Fehlversuche greift nur,
solange es **noch nie** zu einer Sperre für diesen Space kam (`locked_until IS NULL`) — danach
ist das Zeitfenster für diesen Space bewusst tot, bis ein Login gelingt (`reset()`). Grund: die
erste Sperrdauer (900 s) liegt in derselben Größenordnung wie `WINDOW_S` selbst; ein
Fenster-Reset nach Ablauf einer Sperre würde die Eskalation bei jedem erneuten Versuch auf
Stufe 1 zurückwerfen, statt sie hochzuzählen.
"""
from __future__ import annotations

from collections.abc import Callable
from datetime import datetime, timedelta

from .store import AuthStore

MAX_FAILURES = 5
WINDOW_S = 900  # 15 min
BASE_LOCKOUT_S = 900  # 15 min, verdoppelt je weiterer Sperre
MAX_LOCKOUT_S = 86400  # 24 h Deckel


class LoginThrottle:
    def __init__(self, store: AuthStore, *, now_fn: Callable[[], datetime]) -> None:
        self._store = store
        self._now_fn = now_fn

    def check(self, space: str) -> int | None:
        """Restsperre in Sekunden, oder `None` wenn nicht gesperrt. Rein lesend — keine
        Zustandsänderung, auch nicht beim Zurücksetzen einer abgelaufenen Sperre (das
        übernimmt der nächste `register_failure`/`reset`-Aufruf)."""
        attempt = self._store.get_login_attempt(space)
        if attempt is None or attempt.locked_until is None:
            return None
        remaining = (attempt.locked_until - self._now_fn()).total_seconds()
        return int(remaining) if remaining > 0 else None

    def register_failure(self, space: str) -> None:
        now = self._now_fn()
        attempt = self._store.get_login_attempt(space)

        if attempt is None or (
            attempt.locked_until is None
            and (now - attempt.first_failure_at).total_seconds() > WINDOW_S
        ):
            failures = 1
            first_failure_at = now
        else:
            failures = attempt.failures + 1
            first_failure_at = attempt.first_failure_at

        locked_until = attempt.locked_until if attempt is not None else None
        if failures % MAX_FAILURES == 0:
            lockout_number = failures // MAX_FAILURES
            duration_s = min(BASE_LOCKOUT_S * (2 ** (lockout_number - 1)), MAX_LOCKOUT_S)
            locked_until = now + timedelta(seconds=duration_s)

        self._store.upsert_login_attempt(
            space, failures=failures, first_failure_at=first_failure_at, locked_until=locked_until,
        )

    def reset(self, space: str) -> None:
        self._store.clear_login_attempt(space)
