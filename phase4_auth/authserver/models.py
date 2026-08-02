"""Frozen dataclasses für die Persistenzschicht (Plan §2.3/§5 Step 3). Reine Datencontainer,
keine Logik und kein SQL — das lebt ausschließlich in `store.py`. Felder folgen dem
SQLite-Schema aus Plan §2.3; `LoginAttempt` ist eine additive Erweiterung für `ratelimit.py`
(nicht im Plan-Schema-Kommentar benannt, aber dieselbe `login_attempts`-Tabelle).
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, kw_only=True)
class Client:
    client_id: str
    client_name: str | None
    application_type: str | None
    redirect_uris: tuple[str, ...]
    created_at: datetime
    last_used_at: datetime | None


@dataclass(frozen=True, kw_only=True)
class PendingAuthRequest:
    client_id: str
    redirect_uri: str
    state: str | None
    code_challenge: str
    scope: str
    resource: str | None
    created_at: datetime
    expires_at: datetime


@dataclass(frozen=True, kw_only=True)
class AuthorizationCode:
    family_id: str
    client_id: str
    redirect_uri: str
    code_challenge: str
    created_at: datetime
    expires_at: datetime


@dataclass(frozen=True, kw_only=True)
class AccessTokenRecord:
    family_id: str
    space: str
    scope: str
    resource: str
    created_at: datetime
    expires_at: datetime


@dataclass(frozen=True, kw_only=True)
class LoginAttempt:
    space: str
    failures: int
    first_failure_at: datetime | None
    locked_until: datetime | None


@dataclass(frozen=True, kw_only=True)
class TokenFamily:
    """P4 Step 7: Lesezugriff auf `token_families` für `authctl.py list-tokens`/`revoke`.
    Additiv wie `LoginAttempt` — nicht im Plan-Schema-Kommentar benannt, dieselbe Tabelle."""

    family_id: str
    space: str
    client_id: str
    scope: str
    resource: str
    created_at: datetime
    revoked_at: datetime | None
    revoked_reason: str | None


# -- Schema 2 (P5 Step 2, Plan §2.2/§2.3) --------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class UserRow:
    """Rohzeile aus `users` — `totp_secret_enc` ist **verschlüsselt** (AES-256-GCM-Blob);
    entschlüsselt wird ausschließlich in `userdir.py`, nie hier und nie in `store.py`."""

    space: str
    password_hash: str
    password_changed_at: datetime | None
    totp_secret_enc: bytes | None
    totp_alg: str
    totp_confirmed_at: datetime | None
    status: str
    created_at: datetime


@dataclass(frozen=True, kw_only=True)
class InviteRow:
    space: str
    purpose: str
    created_at: datetime
    expires_at: datetime
    consumed_at: datetime | None


@dataclass(frozen=True, kw_only=True)
class SessionRow:
    """`session_hash`/`csrf_hash` — wie bei Token/Codes wird nur der Hash gespeichert (P5-K),
    das Klartext-Cookiepaar existiert nur im Moment von `create_session()`s Rückgabe. `csrf_hash`
    ist trotzdem Teil der Zeile: die Double-Submit-Prüfung (Step 3) vergleicht
    `hash_secret(eingereichter_wert) == csrf_hash`, ohne den Klartext je zu speichern."""

    session_hash: str
    space: str
    csrf_hash: str
    created_at: datetime
    last_seen_at: datetime
    absolute_expires_at: datetime
    revoked_at: datetime | None
    revoked_reason: str | None
