"""TOTP (RFC 6238) über HOTP (RFC 4226), stdlib only (Plan §2.5, Entscheidung P4-G). Kein
Drittanbieter-Paket — die Korrektheit ist gegen die RFC-6238-Appendix-B-Testvektoren beweisbar,
nicht gegen Vertrauen in eine Bibliothek.

Replay-Schutz ist **hier nicht gespeichert** — `verify()` ist zustandslos und bekommt den
zuletzt akzeptierten Zähler injiziert (`last_counter`), genau wie `now_fn` in P1. Die
Persistenz des Zählers je Space lebt in `store.py` (Step 3).
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import struct
from urllib.parse import quote

_ALGOS = {"SHA1": hashlib.sha1, "SHA256": hashlib.sha256, "SHA512": hashlib.sha512}


def generate_secret(nbytes: int = 20) -> str:
    """160 Bit Zufall, Base32 ohne Padding (P4-G)."""
    import secrets as _secrets

    return base64.b32encode(_secrets.token_bytes(nbytes)).rstrip(b"=").decode("ascii")


def _hotp(key: bytes, counter: int, *, digits: int, algo) -> str:
    msg = struct.pack(">Q", counter)
    digest = hmac.new(key, msg, algo).digest()
    offset = digest[-1] & 0x0F
    truncated = int.from_bytes(digest[offset : offset + 4], "big") & 0x7FFFFFFF
    code = truncated % (10**digits)
    return str(code).zfill(digits)


def totp_at(secret: str, counter: int, *, digits: int = 6, algo: str = "SHA1") -> str:
    if algo not in _ALGOS:
        raise ValueError(f"unbekannter TOTP-Algorithmus: {algo!r}")
    padded = secret + "=" * (-len(secret) % 8)
    key = base64.b32decode(padded, casefold=True)
    return _hotp(key, counter, digits=digits, algo=_ALGOS[algo])


def verify(
    secret: str,
    code: str,
    *,
    now: float,
    window: int = 1,
    last_counter: int | None = None,
    digits: int = 6,
    algo: str = "SHA1",
    step_s: int = 30,
) -> int | None:
    """Prüft `code` gegen die Zähler `[now/step - window, now/step + window]`. Zähler
    `<= last_counter` werden übersprungen (Replay). Gibt den akzeptierten Zähler zurück, sonst
    `None` — nie eine Ausnahme bei einem falschen Code, **auch nicht bei einer kaputten
    Nutzerakte** (Step 5: `algo` unbekannt oder `secret` kein valides Base32 wären sonst ein
    unbehandelter `ValueError` aus `totp_at`/`b32decode` — 500 statt "Anmeldung fehlgeschlagen.",
    spiegelt `passwords.verify_password`s Nie-wirft-Vertrag)."""
    if algo not in _ALGOS:
        return None
    try:
        padded = secret + "=" * (-len(secret) % 8)
        key = base64.b32decode(padded, casefold=True)
    except ValueError:
        return None
    current = int(now // step_s)
    for counter in range(current - window, current + window + 1):
        if last_counter is not None and counter <= last_counter:
            continue
        candidate = _hotp(key, counter, digits=digits, algo=_ALGOS[algo])
        if hmac.compare_digest(candidate, code):
            return counter
    return None


def provisioning_uri(
    secret: str, *, space: str, issuer: str, algo: str = "SHA1", digits: int = 6
) -> str:
    """`algo`/`digits` müssen zum `totp_alg`/den `digits` passen, mit denen der Server später
    `verify()` aufruft (P4-G: `totp_alg` ist je Nutzerakte konfigurierbar) — sonst zeigt die
    Authenticator-App Codes, die der Server nie akzeptiert.
    """
    label = quote(f"{issuer}:{space}")
    return (
        f"otpauth://totp/{label}?secret={secret}&issuer={quote(issuer)}"
        f"&algorithm={algo}&digits={digits}&period=30"
    )
