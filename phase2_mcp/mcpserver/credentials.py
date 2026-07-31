"""Keyring-Zugriff, Token-Hashing, Token-Erzeugung (Plan §2.3). `keyring` wird **nur** hier
importiert — alles darüber (`auth.py`) bekommt Funktionen injiziert, damit Unit-Tests nie den
echten Keyring anfassen müssen.

Im Keyring liegt kein umkehrbares Geheimnis: gespeichert wird ausschließlich
`{sha256-hex(token): space}`. Ein Token entsteht nur über `issue()`, wird einmal zurückgegeben
und ist danach nirgends mehr abrufbar — der Server muss ein Token nur *wiedererkennen*, nie
*vorzeigen*.

**P3-F (Step 3):** `load_space_map()` liest jetzt zuerst ein von systemd bereitgestelltes
`LoadCredentialEncrypted`-Verzeichnis, der Keyring bleibt Fallback. Die reine
Keyring-Lesefunktion wurde dafür in `load_space_map_from_keyring()` ausgelagert.
`issue()`/`revoke()` bleiben **unverändert** (Plan-Vorgabe) und rufen weiterhin `load_space_map()`
auf — das ist unschädlich, weil `$CREDENTIALS_DIRECTORY` in ihrem einzigen realen Aufrufkontext
(`issue_token.py`, interaktiv vom Nikinger) nie gesetzt ist, `load_space_map()` dort also immer
auf `load_space_map_from_keyring()` zurückfällt. `phase3_edge/scripts/export_space_map.py` ruft
`load_space_map_from_keyring()` dagegen **direkt** auf (Plan §2.3) — explizit, nicht über die
Verzweigung, sonst würde das Skript im Dienstkontext sich selbst exportieren."""
from __future__ import annotations

import hashlib
import json
import logging
import os
import secrets
from pathlib import Path

import keyring

logger = logging.getLogger(__name__)

KEYRING_SERVICE = "nikinger-space"
KEYRING_KEY_SPACES = "spaces"
CREDENTIAL_NAME = "spaces"


def generate_token() -> str:
    """256 Bit Entropie, URL-sicher (Plan §2.3)."""
    return secrets.token_urlsafe(32)


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def load_space_map_from_keyring() -> dict[str, str]:
    """`{sha256(token): space}` direkt aus dem Keyring. Leeres Dict, wenn noch nie etwas
    gespeichert wurde. Quelle der Wahrheit für `issue()`/`revoke()` und für
    `export_space_map.py` — beide wollen explizit den Keyring, nie die Credentials-Verzweigung."""
    raw = keyring.get_password(KEYRING_SERVICE, KEYRING_KEY_SPACES)
    if raw is None:
        return {}
    return json.loads(raw)


def credential_path() -> Path | None:
    """Pfad der von systemd bereitgestellten Space-Map, oder `None` außerhalb eines Dienstes.

    systemd setzt `$CREDENTIALS_DIRECTORY` nur für Units mit `LoadCredential*`; im
    interaktiven Betrieb (`issue_token.py`, Tests, `mcp_smoke.py`) ist die Variable nicht
    gesetzt und der Keyring bleibt der Weg."""
    credentials_dir = os.environ.get("CREDENTIALS_DIRECTORY")
    if not credentials_dir:
        return None
    return Path(credentials_dir) / CREDENTIAL_NAME


def load_space_map() -> dict[str, str]:
    """Credentials-Verzeichnis zuerst (P3-F, `systemd LoadCredentialEncrypted`), Keyring als
    Fallback.

    **[2026-07-31 Korrektur, P4 Schnitt]:** bis `TokenPathASGI` (P4 Step 7, Runbook-Schritt 8)
    war dies die Funktion, die der laufende Dienst über `auth.py :: KeyringTokenResolver` beim
    Auflösen eines Tokens pro Request benutzte. Seit dem Schnitt löst der Dienst ausschließlich
    über OAuth-Bearer-Token auf (`authserver.resolver.OAuthTokenResolver`); `load_space_map()`
    bleibt als eigenständiges Bestandswerkzeug bestehen (`issue_token.py`,
    `export_space_map.py`), ist aber nicht mehr Teil des Live-Request-Pfads."""
    path = credential_path()
    if path is None:
        return load_space_map_from_keyring()

    if not path.exists():
        # Deployment-Fehler (Datei fehlt trotz gesetztem Verzeichnis) darf den Dienst nicht
        # starten lassen — ein Dienst, der 401 liefert und es loggt, ist leichter zu
        # diagnostizieren als einer, der gar nicht hochkommt (Plan §2.2).
        logger.warning(
            "CREDENTIALS_DIRECTORY gesetzt, aber %s fehlt — falle auf Keyring zurück", path
        )
        return load_space_map_from_keyring()

    raw = path.read_text(encoding="utf-8")
    try:
        mapping = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Space-Map in {path} ist kein gültiges JSON") from exc

    if not isinstance(mapping, dict) or not all(
        isinstance(key, str) and isinstance(value, str) for key, value in mapping.items()
    ):
        raise ValueError(f"Space-Map in {path} ist kein dict[str, str]")

    return mapping


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
