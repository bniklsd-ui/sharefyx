"""`verify_reauth()` — Passwort + TOTP-Code in einem Schritt (P5-P, Plan §2.7). Verlangt für
Passwortwechsel, TOTP-Neueinrichtung, Recovery-Code-Neuausgabe, Beenden fremder Sessions und
Connector-Widerruf. **Nur TOTP, kein Recovery-Code** — anders als der UI-/OAuth-Login (P5-N
erlaubt dort einen Recovery-Code als TOTP-Ersatz): Plan-Wortlaut P5-P nennt explizit „Passwort
UND TOTP-Code", Re-Auth für sicherheitsrelevante Änderungen ist bewusst der stärkere Weg, kein
Ersatzfaktor.

Benutzt dieselbe `LoginThrottle`/`login_attempts`-Tabelle wie der OAuth-Consent- und der
UI-Login — eine Sperre gilt damit für ALLE Anmeldewege gleichzeitig (sonst wäre Re-Auth ein
Schlupfloch um die Bremse herum).

**Phase 8 / P8-A — `ReauthGrantStore`:** kurzlebiges Re-Auth-Grant, schließt P7-24. Ein
`POST /api/v1/reauth` löst mit Passwort+TOTP ein opakes, session-gebundenes Grant aus (TTL
90 s, in-memory). Batch-PATCHes reichen das Grant statt der Rohcredentials durch und umgehen
damit den P7-24-Replay-Schutz, OHNE ihn aufzuweichen — der TOTP-Code wird weiterhin genau
einmal verbraucht (durch `verify_reauth()` selbst), das Grant ist nur ein session-gebundenes
Ticket, kein zweiter Faktor. Niemals persistiert, niemals geloggt; stirbt mit dem Prozess
(die TTL macht das irrelevant — kein Tombstone-Sweep nötig, lazy purge bei jedem `check()`).
"""
from __future__ import annotations

import secrets
from dataclasses import dataclass

from authserver import passwords, totp
from authserver.ratelimit import LoginThrottle
from authserver.store import AuthStore
from authserver.userdir import UserDirectory


# P8-A: TTL des Re-Auth-Grants — großzügig genug für einen Batch mit N Items + UX-Pausen,
# kurz genug, dass ein abgefangenes Token nach Verlassen des Tabs wertlos ist.
REAUTH_GRANT_TTL_S = 90.0


@dataclass(frozen=True)
class ReauthGrant:
    session_id: str
    expires_at: float


class ReauthGrantStore:
    """In-Memory-Speicher für Reauth-Grants. Pro Prozess eine Instanz (App-Factory,
    `api_routes()`-lokal neben `LoginThrottle`). Der `now`-Parameter ist bewusst durchgereicht
    (nicht intern aus `time.time()` gezogen) — Tests fahren mit fester Zeit, der einzige
    Produktivaufrufer reicht `auth_store.now().timestamp()` durch, derselbe Takt wie der Rest."""

    def __init__(self) -> None:
        self._grants: dict[str, ReauthGrant] = {}

    def issue(self, session_id: str, *, now: float) -> str:
        """Mintet ein neues Grant für `session_id`, läuft in `REAUTH_GRANT_TTL_S` Sekunden ab.
        Kollisionen sind bei 32 URL-safe-Zufallsbytes (~256 Bit Entropie) ausgeschlossen —
        kein Retry, kein Re-Issue."""
        token = secrets.token_urlsafe(32)
        self._grants[token] = ReauthGrant(
            session_id=session_id, expires_at=now + REAUTH_GRANT_TTL_S,
        )
        return token

    def check(self, token: str, session_id: str, *, now: float) -> bool:
        """Wahr, wenn `token` zu `session_id` gehört und noch nicht abgelaufen ist. Lazy-Purge
        abgelaufener Grants beim Aufruf — bei der erwarteten Kardinalität (≤ 1 pro aktiver
        Session) ist das billiger als ein Hintergrund-Sweep und hält den Store selbst-begrenzend.
        Ein Grants verbraucht sich NICHT durch `check()` — bewusst wiederverwendbar innerhalb
        der TTL, genau das ist der Sinn des Grants für den Batch-Fall (P7-24)."""
        self._purge_expired(now)
        grant = self._grants.get(token)
        if grant is None:
            return False
        if grant.session_id != session_id or grant.expires_at <= now:
            # Falsche Session oder abgelaufen — Grant verwerfen, kein erneutes Akzeptieren.
            self._grants.pop(token, None)
            return False
        return True

    def _purge_expired(self, now: float) -> None:
        expired = [t for t, g in self._grants.items() if g.expires_at <= now]
        for t in expired:
            self._grants.pop(t, None)


def verify_reauth(
    userdir: UserDirectory,
    throttle: LoginThrottle,
    store: AuthStore,
    *,
    space: str,
    password: str,
    second_factor: str,
    now: float,
) -> bool:
    remaining = throttle.check(space)
    if remaining is not None:
        return False

    record = userdir.get(space)
    stored_hash = record.password_hash if record is not None else passwords.DUMMY_HASH
    password_ok = passwords.verify_password(stored_hash, password)

    totp_ok = False
    accepted_counter: int | None = None
    if record is not None:
        accepted_counter = totp.verify(
            record.totp_secret or "",
            second_factor,
            now=now,
            last_counter=store.get_totp_counter(space),
            algo=record.totp_alg,
        )
        totp_ok = accepted_counter is not None

    if not (password_ok and totp_ok):
        throttle.register_failure(space)
        return False

    throttle.reset(space)
    if accepted_counter is not None:
        store.set_totp_counter(space, accepted_counter)
    return True
