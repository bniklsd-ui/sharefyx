"""Nutzerakten (Passwort-Hash, TOTP-Seed) — spiegelt `mcpserver/credentials.py ::
load_space_map()` bewusst (Plan §2.5): Credentials-Verzeichnis zuerst (systemd
`LoadCredentialEncrypted`), Keyring als Fallback, `warning` statt Ausnahme bei fehlender Datei,
Ausnahme bei kaputtem Inhalt. `keyring` wird **nur** hier importiert — `authserver` importiert
nichts aus `mcpserver` (P4-C), deshalb ist das eine bewusste Duplikation des Musters, kein
Re-Use des P2-Moduls.

Format je Space (Klartext-Struktur, das Geheimnis selbst ist der Argon2id-Hash + TOTP-Seed):
`{"<space>": {"pwd": "$argon2id$...", "totp": "<BASE32-SEED>", "totp_alg": "SHA1",
"created_at": "<ISO-8601>"}}`. **Der TOTP-Seed ist ein echtes, umkehrbares Geheimnis** — anders
als die reine Token-Hash-Map aus P2/P3 ist diese Datei bei Kompromittierung nicht wertlos für
einen Angreifer.
"""
from __future__ import annotations

import json
import logging
import os
from pathlib import Path

import keyring

logger = logging.getLogger(__name__)

KEYRING_SERVICE = "nikinger-space"
KEYRING_KEY_USERS = "auth-users"
CREDENTIAL_NAME = "auth-users"


def credential_path() -> Path | None:
    """Pfad der von systemd bereitgestellten Nutzerakten, oder `None` außerhalb eines Dienstes."""
    credentials_dir = os.environ.get("CREDENTIALS_DIRECTORY")
    if not credentials_dir:
        return None
    return Path(credentials_dir) / CREDENTIAL_NAME


def load_users_from_keyring() -> dict[str, dict[str, str]]:
    """Direkt aus dem Keyring — Quelle der Wahrheit für `provision_user.py`/
    `export_auth_users.py`, die beide explizit den Keyring wollen, nie die Credentials-Verzweigung.
    """
    raw = keyring.get_password(KEYRING_SERVICE, KEYRING_KEY_USERS)
    if raw is None:
        return {}
    return json.loads(raw)


def save_users(mapping: dict[str, dict[str, str]]) -> None:
    keyring.set_password(KEYRING_SERVICE, KEYRING_KEY_USERS, json.dumps(mapping))


def load_users() -> dict[str, dict[str, str]]:
    """Credentials-Verzeichnis zuerst (systemd `LoadCredentialEncrypted`), Keyring als Fallback.
    Das ist die Funktion, die der laufende Dienst (`flows.py`) beim Login benutzt.
    """
    path = credential_path()
    if path is None:
        return load_users_from_keyring()

    if not path.exists():
        logger.warning(
            "CREDENTIALS_DIRECTORY gesetzt, aber %s fehlt — falle auf Keyring zurück", path
        )
        return load_users_from_keyring()

    raw = path.read_text(encoding="utf-8")
    try:
        mapping = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Nutzerakten in {path} sind kein gültiges JSON") from exc

    if not isinstance(mapping, dict) or not all(
        isinstance(key, str) and isinstance(value, dict) for key, value in mapping.items()
    ):
        raise ValueError(f"Nutzerakten in {path} sind kein dict[str, dict]")

    return mapping
