"""Argon2id-Passwort-Hashing (Plan §2.5, Entscheidung P4-F). Parameter aus OWASP Password
Storage Cheat Sheet + BSI TR-02102-1 (2026-01) — nicht `hashlib.scrypt`, obwohl das ohne neue
Abhängigkeit ginge: OWASP nennt scrypt nur für den Fall, dass Argon2id nicht verfügbar ist; in
CPython ist es verfügbar.

`[VERIFY]` V17, gemessen auf dieser VM (2026-07-28, Step 2): `t=2` (Plan-Default) lag bei
**~15 ms** — deutlich unter dem Zielkorridor 50–250 ms. Plan-Vorgabe bei Unterschreitung: `t`
erhöhen, gemessenen Wert dokumentieren statt raten. `t=8` misst **~55 ms**, `m`/`p` unverändert.
"""
from __future__ import annotations

from argon2 import PasswordHasher
from argon2.exceptions import Argon2Error, InvalidHashError

ARGON2_TIME_COST = 8  # V17: t=2 maß ~15ms (zu schnell), t=8 misst ~55ms auf dieser VM
ARGON2_MEMORY_KIB = 19456  # 19 MiB — OWASP-Mindestkonfiguration
ARGON2_PARALLELISM = 1
ARGON2_HASH_LEN = 32
ARGON2_SALT_LEN = 16

_hasher = PasswordHasher(
    time_cost=ARGON2_TIME_COST,
    memory_cost=ARGON2_MEMORY_KIB,
    parallelism=ARGON2_PARALLELISM,
    hash_len=ARGON2_HASH_LEN,
    salt_len=ARGON2_SALT_LEN,
)


def hash_password(password: str) -> str:
    return _hasher.hash(password)


def verify_password(stored: str, password: str) -> bool:
    """Wirft nie — ein kaputter/fremder Hash oder ein falsches Passwort ergeben beide `False`,
    ununterscheidbar von außen (Enumerationsschutz, Plan §2.4 Schritt 4).
    """
    try:
        return _hasher.verify(stored, password)
    except (Argon2Error, InvalidHashError):
        # InvalidHashError erbt von ValueError, nicht von Argon2Error — beide müssen hier
        # abgefangen werden, sonst wirft ein kaputter/fremder Hash statt False zurückzugeben.
        return False


def needs_rehash(stored: str) -> bool:
    return _hasher.check_needs_rehash(stored)


# Fester Dummy-Hash für den Enumerationsschutz: ein nicht existierender Space durchläuft
# trotzdem einen vollen Argon2id-Verify, damit die Antwortzeit nicht verrät, ob das Konto
# existiert. Einmal beim Modul-Import berechnet, nicht bei jedem Login neu gehasht.
DUMMY_HASH: str = hash_password("enumeration-resistance-dummy-password")
