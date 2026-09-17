"""Token-Erzeugung/-Hashing, konstantzeitiger Vergleich, PKCE (Plan §1.3, Entscheidung P4-D).
Opake Token: `secrets.token_urlsafe`, gespeichert wird ausschließlich `sha256`-Hex — kein JWT,
kein Signing-Key. `hash_secret` ist für Token, NICHT für Passwörter (dafür `passwords.py`,
Argon2id — ein 256-Bit-Zufallswert ist nicht ratbar, ein Passwort schon).
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import secrets


def new_secret(nbytes: int = 32) -> str:
    return secrets.token_urlsafe(nbytes)


def new_public_id(nbytes: int = 16) -> str:
    """Wie `new_secret`, aber nie mit `-` beginnend.

    IDs, die ein Mensch auf einer Kommandozeile weiterreicht (`authctl revoke --family-id
    <ID>`), duerfen nicht wie eine Option aussehen -- `argparse` bricht sonst mit
    "expected one argument" ab. Gemessen 2026-09-13: `secrets.token_urlsafe` liefert in
    1,569 % der Faelle ein fuehrendes `-`. Rejection-Sampling statt Umkodierung, damit
    Alphabet und Laenge identisch zu `new_secret` bleiben; der Entropieverlust ist der
    eines verworfenen 64stel.
    """
    while True:
        value = secrets.token_urlsafe(nbytes)
        if not value.startswith("-"):
            return value


def hash_secret(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def secrets_equal(a: str, b: str) -> bool:
    return hmac.compare_digest(a, b)


def pkce_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def verify_pkce(verifier: str, challenge: str) -> bool:
    return secrets_equal(pkce_challenge(verifier), challenge)
