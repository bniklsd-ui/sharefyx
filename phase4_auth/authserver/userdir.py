"""`UserDirectory` — liest Nutzerakten live aus `auth.sqlite3`, entschlüsselt TOTP-Seeds on the
fly (Plan §2.5, P5-L). **Cacht nichts.** Das ist der ganze Punkt: O1 (`scripts/serve.py` las
Nutzerakten bisher genau einmal beim Start, eine Provisionierung wirkte erst nach Restart) ist
damit geschlossen, sobald `flows.py`/`app.py` auf dieses Modul umgestellt sind — zwei Nutzer und
ein SQLite-Lesevorgang je Login sind kein Performanceproblem, ein Cache wäre genau der Zustand,
der O1 erzeugt hat.

`UserRecord.totp_secret` ist Klartext-Base32 — **nur im Speicher**, nie zurückgeschrieben.
"""
from __future__ import annotations

import logging
import secrets as _secrets
from dataclasses import dataclass

from . import passwords, totp
from .secretbox import SecretBoxError, open_, seal
from .store import AuthStore

logger = logging.getLogger(__name__)

RECOVERY_CODE_LEN = 11  # "XXXX-XXXX-X" — vier Zeichen, Bindestrich, vier Zeichen, Bindestrich, ein Zeichen
_RECOVERY_CODE_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"  # ohne 0/O/1/I/L — Verwechslungsgefahr
_RECOVERY_CODE_COUNT = 10


def looks_like_recovery_code(value: str) -> bool:
    """Einzige Stelle, die die Recovery-Code-Form definiert (Länge 11, enthält einen
    Bindestrich) — `flows.py` fragt hier statt eine zweite, eigene Prüfung mitzuführen (Plan
    §2.5: „ein Wert mit Bindestrich und Länge 11 wird als Recovery-Code geprüft")."""
    return len(value) == RECOVERY_CODE_LEN and "-" in value


def _generate_recovery_code() -> str:
    chars = [_secrets.choice(_RECOVERY_CODE_ALPHABET) for _ in range(9)]
    code = f"{''.join(chars[:4])}-{''.join(chars[4:8])}-{chars[8]}"
    assert looks_like_recovery_code(code)  # Formgarantie, kein Laufzeitfall
    return code


@dataclass(frozen=True, kw_only=True)
class UserRecord:
    space: str
    password_hash: str
    totp_secret: str | None  # Klartext-Base32, NUR im Speicher
    totp_alg: str
    totp_confirmed: bool
    status: str


class UserDirectory:
    def __init__(self, store: AuthStore, *, dek: bytes | None) -> None:
        self._store = store
        self._dek = dek
        # Plan §2.4: „Fehlt beides UND ist die users-Tabelle nicht leer → Start scheitert
        # laut." Hier statt in config.py geprüft — das ist die Stelle, die tatsächlich
        # entschlüsseln muss, und sie läuft bei jedem Prozessstart genau einmal.
        if dek is None and self._store.list_users():
            raise ValueError(
                "Kein Data-Encryption-Key geladen, aber die users-Tabelle ist nicht leer — "
                "TOTP-Seeds könnten nicht entschlüsselt werden. Kein stiller Klartextbetrieb."
            )

    def get(self, space: str) -> UserRecord | None:
        row = self._store.get_user(space)
        if row is None:
            return None

        totp_secret: str | None = None
        if row.totp_secret_enc is not None:
            if self._dek is None:
                logger.warning(
                    "Space %r hat einen verschlüsselten TOTP-Seed, aber es ist kein DEK "
                    "geladen — TOTP bleibt für diesen Login unbenutzbar.", space,
                )
            else:
                try:
                    plaintext = open_(row.totp_secret_enc, key=self._dek, aad=space.encode("utf-8"))
                    totp_secret = plaintext.decode("ascii")
                except SecretBoxError:
                    logger.warning(
                        "TOTP-Seed für Space %r konnte nicht entschlüsselt werden (falscher "
                        "Schlüssel oder manipulierter Blob) — TOTP bleibt unbenutzbar.", space,
                    )

        return UserRecord(
            space=row.space,
            password_hash=row.password_hash,
            totp_secret=totp_secret,
            totp_alg=row.totp_alg,
            totp_confirmed=row.totp_confirmed_at is not None,
            status=row.status,
        )

    def spaces(self) -> list[str]:
        return [row.space for row in self._store.list_users()]

    def set_password(self, space: str, password: str) -> None:
        self._store.set_password_hash(space, passwords.hash_password(password))

    def begin_totp_enrollment(self, space: str) -> str:
        """Erzeugt einen neuen, UNBESTÄTIGTEN Seed (`totp_confirmed_at` wird von `store.py ::
        set_totp()` auf NULL gesetzt) — ein alter, bestätigter Seed wird damit sofort ersetzt,
        nicht erst nach `confirm_totp_enrollment()`."""
        if self._dek is None:
            raise ValueError("Kein DEK geladen — TOTP-Enrollment ist ohne Schlüssel nicht möglich")
        secret = totp.generate_secret()
        blob = seal(secret.encode("ascii"), key=self._dek, aad=space.encode("utf-8"))
        self._store.set_totp(space, secret_enc=blob, alg="SHA1")
        return secret

    def confirm_totp_enrollment(self, space: str, code: str, *, now: float) -> bool:
        record = self.get(space)
        if record is None or record.totp_secret is None or record.totp_confirmed:
            return False
        accepted = totp.verify(
            record.totp_secret, code, now=now, last_counter=None, algo=record.totp_alg,
        )
        if accepted is None:
            return False
        self._store.confirm_totp(space)
        return True

    def issue_recovery_codes(self, space: str) -> list[str]:
        """Klartext genau einmal — danach steht nur noch der Hash in `recovery_codes`."""
        codes = [_generate_recovery_code() for _ in range(_RECOVERY_CODE_COUNT)]
        self._store.replace_recovery_codes(space, codes)
        return codes

    def consume_recovery_code(self, space: str, code: str) -> bool:
        return self._store.consume_recovery_code(space, code)
