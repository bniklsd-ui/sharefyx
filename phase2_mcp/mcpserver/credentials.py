"""Keyring-Zugriff, Token-Hashing, Token-Erzeugung (Plan §2.3). `keyring` wird **nur** hier
importiert — alles darüber (`auth.py`) bekommt Funktionen injiziert, damit Unit-Tests nie den
echten Keyring anfassen müssen.

Im Keyring liegt kein umkehrbares Geheimnis: gespeichert wird ausschließlich
`{sha256-hex(token): space}`. Ein Token entsteht nur über `issue()`, wird einmal zurückgegeben
und ist danach nirgends mehr abrufbar — der Server muss ein Token nur *wiedererkennen*, nie
*vorzeigen*.
"""
from __future__ import annotations

import hashlib
import json
import secrets

import keyring

KEYRING_SERVICE = "nikinger-space"
KEYRING_KEY_SPACES = "spaces"


def generate_token() -> str:
    """256 Bit Entropie, URL-sicher (Plan §2.3)."""
    return secrets.token_urlsafe(32)


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def load_space_map() -> dict[str, str]:
    """`{sha256(token): space}`. Leeres Dict, wenn noch nie etwas gespeichert wurde."""
    raw = keyring.get_password(KEYRING_SERVICE, KEYRING_KEY_SPACES)
    if raw is None:
        return {}
    return json.loads(raw)


def save_space_map(mapping: dict[str, str]) -> None:
    keyring.set_password(KEYRING_SERVICE, KEYRING_KEY_SPACES, json.dumps(mapping))


def issue(space: str) -> str:
    """Erzeugt ein neues Token für `space`, speichert nur dessen Hash, gibt das Token EINMAL
    zurück. Bestehende Tokens für andere Spaces bleiben unangetastet.
    """
    token = generate_token()
    mapping = load_space_map()
    mapping[hash_token(token)] = space
    save_space_map(mapping)
    return token


def revoke(space: str) -> int:
    """Entfernt alle Hashes, die auf `space` zeigen. Gibt die Anzahl entfernter Einträge zurück."""
    mapping = load_space_map()
    remaining = {h: s for h, s in mapping.items() if s != space}
    removed = len(mapping) - len(remaining)
    if removed:
        save_space_map(remaining)
    return removed
