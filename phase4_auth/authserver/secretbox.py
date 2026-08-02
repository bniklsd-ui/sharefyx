"""AES-256-GCM-Versiegelung für TOTP-Seeds in `auth.sqlite3` (Plan §2.4, Entscheidung P5-J).
BSI TR-02102-1 nennt AES-GCM als empfohlenes AEAD-Verfahren. `nonce || ciphertext_mit_tag` wird
als ein `bytes`-Blob gespeichert (`users.totp_secret_enc`) — kein zweites Feld für den Nonce,
der Blob trägt alles, was `open_()` braucht.

**AAD = der Space-Name.** Ein Seed, der aus einer anderen Zeile kopiert (oder per SQL-Fehler
vertauscht) wird, entschlüsselt dann mit einem *falschen* AAD-Wert und `open_()` wirft —
still eine fremde Zeile lesen ist damit ausgeschlossen, nicht nur unwahrscheinlich.
"""
from __future__ import annotations

import secrets

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

NONCE_LEN = 12
KEY_LEN = 32


class SecretBoxError(Exception):
    """Falscher Schlüssel, falsche AAD, manipulierter Ciphertext oder ein zu kurzer Blob —
    bewusst ein einziger Fehlertyp, keine Unterscheidung nach Ursache (dieselbe
    Enumerationsschutz-Logik wie `passwords.verify_password`/`totp.verify`: eine
    Unterscheidung nach außen wäre ein Orakel)."""


def seal(plaintext: bytes, *, key: bytes, aad: bytes) -> bytes:
    if len(key) != KEY_LEN:
        raise SecretBoxError(f"Schlüssel muss {KEY_LEN} Byte lang sein, war {len(key)}")
    nonce = secrets.token_bytes(NONCE_LEN)
    ciphertext = AESGCM(key).encrypt(nonce, plaintext, aad)
    return nonce + ciphertext


def open_(blob: bytes, *, key: bytes, aad: bytes) -> bytes:
    if len(key) != KEY_LEN:
        raise SecretBoxError(f"Schlüssel muss {KEY_LEN} Byte lang sein, war {len(key)}")
    if len(blob) < NONCE_LEN:
        raise SecretBoxError("Blob ist kürzer als ein Nonce — kein gültiger secretbox-Blob")
    nonce, ciphertext = blob[:NONCE_LEN], blob[NONCE_LEN:]
    try:
        return AESGCM(key).decrypt(nonce, ciphertext, aad)
    except InvalidTag as exc:
        raise SecretBoxError(
            "Entschlüsselung fehlgeschlagen — falscher Schlüssel, falsche AAD oder "
            "manipulierter Ciphertext"
        ) from exc
