"""`verify_reauth()` — Passwort + TOTP-Code in einem Schritt (P5-P, Plan §2.7). Verlangt für
Passwortwechsel, TOTP-Neueinrichtung, Recovery-Code-Neuausgabe, Beenden fremder Sessions und
Connector-Widerruf. **Nur TOTP, kein Recovery-Code** — anders als der UI-/OAuth-Login (P5-N
erlaubt dort einen Recovery-Code als TOTP-Ersatz): Plan-Wortlaut P5-P nennt explizit „Passwort
UND TOTP-Code", Re-Auth für sicherheitsrelevante Änderungen ist bewusst der stärkere Weg, kein
Ersatzfaktor.

Benutzt dieselbe `LoginThrottle`/`login_attempts`-Tabelle wie der OAuth-Consent- und der
UI-Login — eine Sperre gilt damit für ALLE Anmeldewege gleichzeitig (sonst wäre Re-Auth ein
Schlupfloch um die Bremse herum).
"""
from __future__ import annotations

from authserver import passwords, totp
from authserver.ratelimit import LoginThrottle
from authserver.store import AuthStore
from authserver.userdir import UserDirectory


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
