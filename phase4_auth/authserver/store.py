"""SQLite-Persistenz des Authorization Servers (Plan §2.3, §5 Step 3). `AuthStore` kapselt
**jede** SQL-Anweisung dieses Pakets — kein SQL außerhalb dieser Datei (Grep-Beleg im
Session-Block). Schema-Version in `schema_meta`, damit ein späteres Feld kein Rätsel wird.
`now_fn` injiziert (P1-Konvention), alle Zeitstempel ISO-8601-UTC-Strings. Mehrschrittige
Zustandsänderungen (Code einlösen, Refresh rotieren, Familie widerrufen) laufen in einer
`BEGIN IMMEDIATE`-Transaktion — ein Fluss, der zur Hälfte gilt, ist schlimmer als einer, der
scheitert.

**Abweichungen vom Plan-Methodenskelett** (dokumentiert, siehe Phase-Head Session-Block):
`create_family` sowie die drei `*_login_attempt`-Methoden stehen nicht in der "fix"-Liste des
Plans, sind aber durch das Schema erzwungen (FK `auth_codes.family_id`, `login_attempts`-Tabelle
für `ratelimit.py`, das selbst kein SQL führen darf). `rotate_refresh` nimmt zusätzlich
`access_ttl_s`/`refresh_ttl_s` entgegen statt sie aus dem Bestand abzuleiten — die
Bestands-Ableitung hat eine echte Absturzstelle nach `purge_expired()` (kein Access-Token mehr
in der Familie), siehe Advisor-Review dieser Session.
"""
from __future__ import annotations

import json
import sqlite3
import threading
from collections.abc import Callable, Iterable
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path

from . import crypto
from .models import (
    AccessTokenRecord,
    AuthorizationCode,
    Client,
    InviteRow,
    LoginAttempt,
    PendingAuthRequest,
    SessionRow,
    TokenFamily,
    UserRow,
)

SCHEMA_VERSION = "2"

# S7-Ergänzung (P5 Step 2): wie lange eine widerrufene `ui_sessions`-Zeile bzw. eine konsumierte
# `invites`-Zeile nach dem Ereignis noch existiert, bevor `purge_expired()` sie entfernt — genug
# Zeit für ein Audit ("wer hat wann welche Sitzung beendet"), aber kein unbegrenztes Wachstum.
RETENTION_AFTER_REVOKE_OR_CONSUME_S = 7 * 86400

_SCHEMA = """
CREATE TABLE IF NOT EXISTS schema_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);

CREATE TABLE IF NOT EXISTS clients (
  client_id        TEXT PRIMARY KEY,
  client_name      TEXT,
  application_type TEXT,
  redirect_uris    TEXT NOT NULL,
  created_at       TEXT NOT NULL,
  last_used_at     TEXT);

CREATE TABLE IF NOT EXISTS auth_requests (
  request_id_hash  TEXT PRIMARY KEY,
  client_id        TEXT NOT NULL,
  redirect_uri     TEXT NOT NULL,
  state            TEXT,
  code_challenge   TEXT NOT NULL,
  scope            TEXT NOT NULL,
  resource         TEXT,
  created_at       TEXT NOT NULL,
  expires_at       TEXT NOT NULL,
  consumed_at      TEXT);

CREATE TABLE IF NOT EXISTS token_families (
  family_id        TEXT PRIMARY KEY,
  space            TEXT NOT NULL,
  client_id        TEXT NOT NULL,
  scope            TEXT NOT NULL,
  resource         TEXT NOT NULL,
  created_at       TEXT NOT NULL,
  revoked_at       TEXT,
  revoked_reason   TEXT);

CREATE TABLE IF NOT EXISTS auth_codes (
  code_hash        TEXT PRIMARY KEY,
  family_id        TEXT NOT NULL REFERENCES token_families(family_id),
  client_id        TEXT NOT NULL,
  redirect_uri     TEXT NOT NULL,
  code_challenge   TEXT NOT NULL,
  created_at       TEXT NOT NULL,
  expires_at       TEXT NOT NULL,
  consumed_at      TEXT);

CREATE TABLE IF NOT EXISTS access_tokens (
  token_hash       TEXT PRIMARY KEY,
  family_id        TEXT NOT NULL REFERENCES token_families(family_id),
  space            TEXT NOT NULL,
  scope            TEXT NOT NULL,
  resource         TEXT NOT NULL,
  created_at       TEXT NOT NULL,
  expires_at       TEXT NOT NULL);

CREATE TABLE IF NOT EXISTS refresh_tokens (
  token_hash       TEXT PRIMARY KEY,
  family_id        TEXT NOT NULL REFERENCES token_families(family_id),
  created_at       TEXT NOT NULL,
  expires_at       TEXT NOT NULL,
  rotated_at       TEXT,
  successor_hash   TEXT);

CREATE TABLE IF NOT EXISTS login_attempts (
  space            TEXT PRIMARY KEY,
  failures         INTEGER NOT NULL DEFAULT 0,
  first_failure_at TEXT,
  locked_until     TEXT);

CREATE TABLE IF NOT EXISTS totp_replay (
  space            TEXT PRIMARY KEY,
  last_counter     INTEGER NOT NULL);

CREATE TABLE IF NOT EXISTS register_attempts (
  window_start     TEXT PRIMARY KEY,
  count            INTEGER NOT NULL);

CREATE INDEX IF NOT EXISTS ix_access_family  ON access_tokens(family_id);
CREATE INDEX IF NOT EXISTS ix_refresh_family ON refresh_tokens(family_id);
CREATE INDEX IF NOT EXISTS ix_access_exp     ON access_tokens(expires_at);
"""

# Schema 2 (P5 Step 2, Plan §2.2) — rein additiv, keine Änderung an _SCHEMA. Nutzerakten wandern
# hier aus dem Keyring/Credential-JSON (P4) in die Auth-SQLite (P5-I); `totp_secret_enc` ist ein
# AES-256-GCM-Blob, entschlüsselt wird ausschließlich in `userdir.py`.
_SCHEMA_V2 = """
CREATE TABLE IF NOT EXISTS users (
  space               TEXT PRIMARY KEY,
  password_hash       TEXT NOT NULL,
  password_changed_at TEXT,
  totp_secret_enc     BLOB,
  totp_alg            TEXT NOT NULL DEFAULT 'SHA1',
  totp_confirmed_at   TEXT,
  status              TEXT NOT NULL DEFAULT 'active',
  created_at          TEXT NOT NULL);

CREATE TABLE IF NOT EXISTS invites (
  token_hash  TEXT PRIMARY KEY,
  space       TEXT NOT NULL,
  purpose     TEXT NOT NULL,
  created_at  TEXT NOT NULL,
  expires_at  TEXT NOT NULL,
  consumed_at TEXT);

CREATE TABLE IF NOT EXISTS recovery_codes (
  code_hash  TEXT PRIMARY KEY,
  space      TEXT NOT NULL,
  created_at TEXT NOT NULL,
  used_at    TEXT);

CREATE TABLE IF NOT EXISTS ui_sessions (
  session_hash        TEXT PRIMARY KEY,
  space               TEXT NOT NULL,
  csrf_hash           TEXT NOT NULL,
  created_at          TEXT NOT NULL,
  last_seen_at        TEXT NOT NULL,
  absolute_expires_at TEXT NOT NULL,
  revoked_at          TEXT,
  revoked_reason      TEXT);

CREATE INDEX IF NOT EXISTS ix_sessions_space  ON ui_sessions(space);
CREATE INDEX IF NOT EXISTS ix_recovery_space  ON recovery_codes(space);
CREATE INDEX IF NOT EXISTS ix_invites_space   ON invites(space);
"""


def _format_dt(value: datetime) -> str:
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse_dt(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def _parse_dt_opt(value: str | None) -> datetime | None:
    return _parse_dt(value) if value is not None else None


def _client_from_row(row: sqlite3.Row) -> Client:
    return Client(
        client_id=row["client_id"],
        client_name=row["client_name"],
        application_type=row["application_type"],
        redirect_uris=tuple(json.loads(row["redirect_uris"])),
        created_at=_parse_dt(row["created_at"]),
        last_used_at=_parse_dt_opt(row["last_used_at"]),
    )


def _family_from_row(row: sqlite3.Row) -> TokenFamily:
    return TokenFamily(
        family_id=row["family_id"],
        space=row["space"],
        client_id=row["client_id"],
        scope=row["scope"],
        resource=row["resource"],
        created_at=_parse_dt(row["created_at"]),
        revoked_at=_parse_dt_opt(row["revoked_at"]),
        revoked_reason=row["revoked_reason"],
    )


class AuthStore:
    def __init__(self, path: Path, *, now_fn: Callable[[], datetime]) -> None:
        self._path = Path(path)
        self._now_fn = now_fn
        self._lock = threading.RLock()
        # check_same_thread=False: jeder Zugriff läuft durch self._lock serialisiert (wie
        # storage.index/storage.store, Plan-Konvention aus P1). isolation_level=None schaltet
        # den impliziten Autocommit-Mechanismus von sqlite3 ab — Transaktionsgrenzen werden hier
        # explizit über BEGIN IMMEDIATE/COMMIT/ROLLBACK gesetzt, nicht geraten.
        self._conn = sqlite3.connect(self._path, check_same_thread=False, isolation_level=None)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA foreign_keys=ON")
        self.initialise()

    def initialise(self) -> None:
        with self._lock:
            self._conn.executescript(_SCHEMA)
            self._conn.executescript(_SCHEMA_V2)
            self._conn.execute(
                "INSERT INTO schema_meta (key, value) VALUES ('schema_version', ?) "
                "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                (SCHEMA_VERSION,),
            )

    def now(self) -> datetime:
        """Additiv (Step 5): exponiert die injizierte Uhr für Aufrufer, die dieselbe Uhr wie
        der Store brauchen (`ratelimit.LoginThrottle`, `totp.verify` in `flows.py`) statt eine
        zweite, potenziell abweichende `now_fn` zu injizieren (Advisor-Fund dieser Session:
        "ein Clock, nicht zwei" — sonst driftet ein eingefrorener Test-Clock gegen echte Zeit)."""
        return self._now_fn()

    @contextmanager
    def _transaction(self):
        with self._lock:
            self._conn.execute("BEGIN IMMEDIATE")
            try:
                yield self._conn
            except Exception:
                self._conn.execute("ROLLBACK")
                raise
            else:
                self._conn.execute("COMMIT")

    # -- Clients -------------------------------------------------------------------

    def create_client(
        self,
        *,
        client_name: str | None,
        application_type: str | None,
        redirect_uris: Iterable[str],
    ) -> Client:
        client_id = crypto.new_secret(16)
        redirect_list = list(redirect_uris)
        now = self._now_fn()
        with self._lock:
            self._conn.execute(
                "INSERT INTO clients (client_id, client_name, application_type, "
                "redirect_uris, created_at, last_used_at) VALUES (?, ?, ?, ?, ?, NULL)",
                (client_id, client_name, application_type, json.dumps(redirect_list), _format_dt(now)),
            )
        return Client(
            client_id=client_id,
            client_name=client_name,
            application_type=application_type,
            redirect_uris=tuple(redirect_list),
            created_at=now,
            last_used_at=None,
        )

    def get_client(self, client_id: str) -> Client | None:
        with self._lock:
            row = self._conn.execute(
                "SELECT * FROM clients WHERE client_id = ?", (client_id,)
            ).fetchone()
        return _client_from_row(row) if row is not None else None

    def list_clients(self) -> list[Client]:
        """P4 Step 7: `authctl.py list-clients`. Reine Lesehilfe, kein Plan-Skelett-Eintrag —
        additiv wie `create_family` (siehe Moduldocstring)."""
        with self._lock:
            rows = self._conn.execute("SELECT * FROM clients ORDER BY created_at").fetchall()
        return [_client_from_row(row) for row in rows]

    # -- Auth-Requests ---------------------------------------------------------------

    def create_auth_request(
        self,
        *,
        client_id: str,
        redirect_uri: str,
        state: str | None,
        code_challenge: str,
        scope: str,
        resource: str | None,
        ttl_s: int,
    ) -> str:
        request_id = crypto.new_secret(32)
        now = self._now_fn()
        expires_at = now + timedelta(seconds=ttl_s)
        with self._lock:
            self._conn.execute(
                "INSERT INTO auth_requests (request_id_hash, client_id, redirect_uri, state, "
                "code_challenge, scope, resource, created_at, expires_at, consumed_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, NULL)",
                (
                    crypto.hash_secret(request_id), client_id, redirect_uri, state,
                    code_challenge, scope, resource, _format_dt(now), _format_dt(expires_at),
                ),
            )
        return request_id

    def consume_auth_request(self, request_id: str) -> PendingAuthRequest | None:
        """Einmalig: markiert sofort als konsumiert, sobald ein gültiger (nicht abgelaufener,
        noch nicht konsumierter) Datensatz gefunden wird — unabhängig davon, ob der
        anschließende Login-Versuch (Aufrufer, `flows.py` in Step 5) gelingt. Ein Formular, ein
        Versuch (Plan §2.4, POST /oauth/authorize Schritt 1).
        """
        request_hash = crypto.hash_secret(request_id)
        now = self._now_fn()
        with self._lock:
            row = self._conn.execute(
                "SELECT * FROM auth_requests WHERE request_id_hash = ?", (request_hash,)
            ).fetchone()
            if row is None or row["consumed_at"] is not None:
                return None
            if _parse_dt(row["expires_at"]) <= now:
                return None
            self._conn.execute(
                "UPDATE auth_requests SET consumed_at = ? WHERE request_id_hash = ?",
                (_format_dt(now), request_hash),
            )
        return PendingAuthRequest(
            client_id=row["client_id"],
            redirect_uri=row["redirect_uri"],
            state=row["state"],
            code_challenge=row["code_challenge"],
            scope=row["scope"],
            resource=row["resource"],
            created_at=_parse_dt(row["created_at"]),
            expires_at=_parse_dt(row["expires_at"]),
        )

    # -- Token-Familien ----------------------------------------------------------------

    def create_family(self, *, space: str, client_id: str, scope: str, resource: str) -> str:
        """Nicht in der Plan-"fix"-Methodenliste, aber durch die FK `auth_codes.family_id`
        erzwungen: eine Familie muss existieren, bevor `issue_code` einen Code an sie binden
        kann (Plan §2.4 POST /oauth/authorize Schritt 8: "token_families-Zeile anlegen,
        Authorization-Code erzeugen" — zwei Schritte, zwei Aufrufe).
        """
        family_id = crypto.new_secret(16)
        now = self._now_fn()
        with self._lock:
            self._conn.execute(
                "INSERT INTO token_families (family_id, space, client_id, scope, resource, "
                "created_at, revoked_at, revoked_reason) VALUES (?, ?, ?, ?, ?, ?, NULL, NULL)",
                (family_id, space, client_id, scope, resource, _format_dt(now)),
            )
        return family_id

    def revoke_family(self, family_id: str, reason: str) -> int:
        with self._transaction() as conn:
            return self._revoke_family_locked(conn, family_id, reason, self._now_fn())

    def _revoke_family_locked(
        self, conn: sqlite3.Connection, family_id: str, reason: str, now: datetime
    ) -> int:
        # "AND revoked_at IS NULL": ein zweiter Widerruf (z. B. Operator-Revoke nach einem
        # bereits erkannten code_replay) überschreibt nicht den ursprünglichen Grund.
        conn.execute(
            "UPDATE token_families SET revoked_at = ?, revoked_reason = ? "
            "WHERE family_id = ? AND revoked_at IS NULL",
            (_format_dt(now), reason, family_id),
        )
        access_cur = conn.execute("DELETE FROM access_tokens WHERE family_id = ?", (family_id,))
        refresh_cur = conn.execute("DELETE FROM refresh_tokens WHERE family_id = ?", (family_id,))
        return access_cur.rowcount + refresh_cur.rowcount

    def revoke_families_for_space(self, space: str, reason: str) -> int:
        """P5-Q (Plan §0.5): ein Passwortwechsel widerruft ALLE Token-Familien des Space, nicht
        nur eine — Gegenstück zu `revoke_sessions_for_space()`. Gibt die Anzahl widerrufener
        FAMILIEN zurück (nicht gelöschter Token, anders als `_revoke_family_locked()`s
        Rückgabewert — derselbe Zählvertrag wie `revoke_sessions_for_space()`, das ebenfalls
        Sitzungen zählt, nicht Datenbankzeilen). Läuft in einer Transaktion, damit ein
        teilweiser Widerruf (manche Familien tot, manche noch aktiv) nicht als Zwischenstand
        sichtbar wird."""
        with self._transaction() as conn:
            rows = conn.execute(
                "SELECT family_id FROM token_families WHERE space = ? AND revoked_at IS NULL",
                (space,),
            ).fetchall()
            now = self._now_fn()
            for row in rows:
                self._revoke_family_locked(conn, row["family_id"], reason, now)
            return len(rows)

    def list_families(self, *, space: str | None = None) -> list[TokenFamily]:
        """P4 Step 7: `authctl.py list-tokens`/`revoke` (die Familie ist die Widerrufseinheit,
        Plan §2.1 — `revoke --family-id` nimmt genau die `family_id` entgegen, die diese Methode
        zurückgibt). Additiv, kein Plan-Skelett-Eintrag."""
        with self._lock:
            if space is None:
                rows = self._conn.execute(
                    "SELECT * FROM token_families ORDER BY created_at"
                ).fetchall()
            else:
                rows = self._conn.execute(
                    "SELECT * FROM token_families WHERE space = ? ORDER BY created_at", (space,)
                ).fetchall()
        return [_family_from_row(row) for row in rows]

    # -- Codes und Token ------------------------------------------------------------

    def issue_code(
        self,
        *,
        family_id: str,
        client_id: str,
        redirect_uri: str,
        code_challenge: str,
        ttl_s: int,
    ) -> str:
        code = crypto.new_secret(32)
        now = self._now_fn()
        expires_at = now + timedelta(seconds=ttl_s)
        with self._lock:
            self._conn.execute(
                "INSERT INTO auth_codes (code_hash, family_id, client_id, redirect_uri, "
                "code_challenge, created_at, expires_at, consumed_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, NULL)",
                (
                    crypto.hash_secret(code), family_id, client_id, redirect_uri,
                    code_challenge, _format_dt(now), _format_dt(expires_at),
                ),
            )
        return code

    def consume_code(self, code: str) -> tuple[AuthorizationCode | None, bool]:
        """`(code_daten, war_replay)`. Abgelaufen zählt NICHT als Replay (Plan §2.4 Token-Schritt
        1: unbekannt/abgelaufen → einfach `invalid_grant`, keine Familien-Aktion) — nur ein
        bereits konsumierter, noch gültiger Code ist ein Replay und widerruft die Familie
        (Schritt 2, RFC 9700). Beide Prüfungen und der Widerruf laufen in einer Transaktion.
        """
        code_hash = crypto.hash_secret(code)
        now = self._now_fn()
        with self._transaction() as conn:
            row = conn.execute(
                "SELECT * FROM auth_codes WHERE code_hash = ?", (code_hash,)
            ).fetchone()
            if row is None or _parse_dt(row["expires_at"]) <= now:
                return None, False
            if row["consumed_at"] is not None:
                self._revoke_family_locked(conn, row["family_id"], "code_replay", now)
                return None, True
            conn.execute(
                "UPDATE auth_codes SET consumed_at = ? WHERE code_hash = ?",
                (_format_dt(now), code_hash),
            )
            return (
                AuthorizationCode(
                    family_id=row["family_id"],
                    client_id=row["client_id"],
                    redirect_uri=row["redirect_uri"],
                    code_challenge=row["code_challenge"],
                    created_at=_parse_dt(row["created_at"]),
                    expires_at=_parse_dt(row["expires_at"]),
                ),
                False,
            )

    def issue_token_pair(
        self, family_id: str, *, access_ttl_s: int, refresh_ttl_s: int
    ) -> tuple[str, str]:
        access_token = crypto.new_secret(32)
        refresh_token = crypto.new_secret(32)
        now = self._now_fn()
        access_expires = now + timedelta(seconds=access_ttl_s)
        refresh_expires = now + timedelta(seconds=refresh_ttl_s)
        with self._transaction() as conn:
            row = conn.execute(
                "SELECT space, scope, resource FROM token_families WHERE family_id = ?",
                (family_id,),
            ).fetchone()
            conn.execute(
                "INSERT INTO access_tokens (token_hash, family_id, space, scope, resource, "
                "created_at, expires_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    crypto.hash_secret(access_token), family_id, row["space"], row["scope"],
                    row["resource"], _format_dt(now), _format_dt(access_expires),
                ),
            )
            conn.execute(
                "INSERT INTO refresh_tokens (token_hash, family_id, created_at, expires_at, "
                "rotated_at, successor_hash) VALUES (?, ?, ?, ?, NULL, NULL)",
                (crypto.hash_secret(refresh_token), family_id, _format_dt(now), _format_dt(refresh_expires)),
            )
        return access_token, refresh_token

    def rotate_refresh(
        self, refresh_token: str, *, client_id: str, access_ttl_s: int, refresh_ttl_s: int
    ) -> tuple[str, str] | None:
        """Abweichung vom Plan-Skelett: nimmt `access_ttl_s`/`refresh_ttl_s` entgegen statt sie
        aus vorhandenen Zeilen abzuleiten. Eine Ableitung aus dem jüngsten Access-Token der
        Familie bricht am echten Betriebspfad: `purge_expired()` (auch über `authctl.py
        purge-expired`) löscht abgelaufene Access-Tokens; ein Client, der erst nach Ablauf des
        Access-Tokens (60 min) aber innerhalb der Refresh-Gültigkeit (30 d) rotiert, träfe dann
        auf keine Zeile und die Ableitung würde crashen — kein Randfall, der Normalpfad einer
        langlebigen Session. Explizite Parameter sind kleinere Drift als dieser Absturzmodus.

        **S2 (Sicherheits-Review 2026-07-29):** `client_id` wird jetzt gegen
        `token_families.client_id` geprüft. Ein Mismatch ist ein früher `return None`
        (`invalid_grant`, ununterscheidbar von einem unbekannten Token) — **kein**
        Familienwiderruf, ein falscher `client_id` ist kein Replay (anders als `rotated_at is
        not None` unten).
        """
        token_hash = crypto.hash_secret(refresh_token)
        now = self._now_fn()
        with self._transaction() as conn:
            row = conn.execute(
                "SELECT r.*, f.revoked_at AS family_revoked_at, f.space AS space, "
                "f.client_id AS client_id, f.scope AS scope, f.resource AS resource "
                "FROM refresh_tokens r "
                "JOIN token_families f ON f.family_id = r.family_id WHERE r.token_hash = ?",
                (token_hash,),
            ).fetchone()
            if row is None or row["family_revoked_at"] is not None:
                return None
            if row["client_id"] != client_id:
                return None
            if _parse_dt(row["expires_at"]) <= now:
                return None
            if row["rotated_at"] is not None:
                self._revoke_family_locked(conn, row["family_id"], "refresh_replay", now)
                return None

            new_access = crypto.new_secret(32)
            new_refresh = crypto.new_secret(32)
            new_refresh_hash = crypto.hash_secret(new_refresh)

            conn.execute(
                "UPDATE refresh_tokens SET rotated_at = ?, successor_hash = ? WHERE token_hash = ?",
                (_format_dt(now), new_refresh_hash, token_hash),
            )
            conn.execute(
                "INSERT INTO refresh_tokens (token_hash, family_id, created_at, expires_at, "
                "rotated_at, successor_hash) VALUES (?, ?, ?, ?, NULL, NULL)",
                (new_refresh_hash, row["family_id"], _format_dt(now), _format_dt(now + timedelta(seconds=refresh_ttl_s))),
            )
            conn.execute(
                "INSERT INTO access_tokens (token_hash, family_id, space, scope, resource, "
                "created_at, expires_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    crypto.hash_secret(new_access), row["family_id"], row["space"], row["scope"],
                    row["resource"], _format_dt(now), _format_dt(now + timedelta(seconds=access_ttl_s)),
                ),
            )
        return new_access, new_refresh

    def lookup_access_token(self, token: str) -> AccessTokenRecord | None:
        token_hash = crypto.hash_secret(token)
        now = self._now_fn()
        with self._lock:
            row = self._conn.execute(
                "SELECT a.*, f.revoked_at AS family_revoked_at FROM access_tokens a "
                "JOIN token_families f ON f.family_id = a.family_id WHERE a.token_hash = ?",
                (token_hash,),
            ).fetchone()
        if row is None or row["family_revoked_at"] is not None:
            return None
        if _parse_dt(row["expires_at"]) <= now:
            return None
        return AccessTokenRecord(
            family_id=row["family_id"],
            space=row["space"],
            scope=row["scope"],
            resource=row["resource"],
            created_at=_parse_dt(row["created_at"]),
            expires_at=_parse_dt(row["expires_at"]),
        )

    def purge_expired(self) -> dict[str, int]:
        """**S7-Ergänzung (P5 Step 2):** `ui_sessions`/`invites` waren beim ersten S7-Fix (Step
        1) noch nicht möglich — die Tabellen existierten nicht (Schema 1). Jetzt mit dabei:
        `ui_sessions` absolut abgelaufen ODER länger als `RETENTION_AFTER_REVOKE_OR_CONSUME_S`
        widerrufen; `invites` abgelaufen ODER länger als dieselbe Frist konsumiert."""
        now = self._now_fn()
        now_s = _format_dt(now)
        retention_cutoff_s = _format_dt(
            now - timedelta(seconds=RETENTION_AFTER_REVOKE_OR_CONSUME_S)
        )
        with self._transaction() as conn:
            counts = {}
            # Tabellennamen kommen aus dem festen Tupel oben, nicht aus Nutzereingabe — sicher
            # zu interpolieren, nur der Zeitwert selbst ist ein gebundener Parameter.
            for table in ("auth_requests", "auth_codes", "access_tokens", "refresh_tokens"):
                cur = conn.execute(f"DELETE FROM {table} WHERE expires_at <= ?", (now_s,))
                counts[table] = cur.rowcount

            cur = conn.execute(
                "DELETE FROM ui_sessions WHERE absolute_expires_at <= ? "
                "OR (revoked_at IS NOT NULL AND revoked_at <= ?)",
                (now_s, retention_cutoff_s),
            )
            counts["ui_sessions"] = cur.rowcount

            cur = conn.execute(
                "DELETE FROM invites WHERE expires_at <= ? "
                "OR (consumed_at IS NOT NULL AND consumed_at <= ?)",
                (now_s, retention_cutoff_s),
            )
            counts["invites"] = cur.rowcount
        return counts

    # -- Login-Fehlversuche (für ratelimit.py — kein SQL dort) ------------------------

    def get_login_attempt(self, space: str) -> LoginAttempt | None:
        with self._lock:
            row = self._conn.execute(
                "SELECT * FROM login_attempts WHERE space = ?", (space,)
            ).fetchone()
        if row is None:
            return None
        return LoginAttempt(
            space=row["space"],
            failures=row["failures"],
            first_failure_at=_parse_dt_opt(row["first_failure_at"]),
            locked_until=_parse_dt_opt(row["locked_until"]),
        )

    def upsert_login_attempt(
        self,
        space: str,
        *,
        failures: int,
        first_failure_at: datetime | None,
        locked_until: datetime | None,
    ) -> None:
        with self._lock:
            self._conn.execute(
                "INSERT INTO login_attempts (space, failures, first_failure_at, locked_until) "
                "VALUES (?, ?, ?, ?) ON CONFLICT(space) DO UPDATE SET "
                "failures = excluded.failures, first_failure_at = excluded.first_failure_at, "
                "locked_until = excluded.locked_until",
                (
                    space, failures,
                    _format_dt(first_failure_at) if first_failure_at is not None else None,
                    _format_dt(locked_until) if locked_until is not None else None,
                ),
            )

    def clear_login_attempt(self, space: str) -> None:
        with self._lock:
            self._conn.execute("DELETE FROM login_attempts WHERE space = ?", (space,))

    # -- TOTP-Replay-Zähler (für flows.py — kein SQL dort) -----------------------------

    def get_totp_counter(self, space: str) -> int | None:
        """Additiv (Step 5), nicht in der Plan-"fix"-Liste — die Tabelle `totp_replay` existiert
        seit Step 3, aber ohne Zugriffsmethode (gleiches Muster wie `increment_register_window`
        in Step 4)."""
        with self._lock:
            row = self._conn.execute(
                "SELECT last_counter FROM totp_replay WHERE space = ?", (space,)
            ).fetchone()
        return row["last_counter"] if row is not None else None

    def set_totp_counter(self, space: str, counter: int) -> None:
        with self._lock:
            self._conn.execute(
                "INSERT INTO totp_replay (space, last_counter) VALUES (?, ?) "
                "ON CONFLICT(space) DO UPDATE SET last_counter = excluded.last_counter",
                (space, counter),
            )

    # -- Registrierungsbremse (für clients.py — kein SQL dort) -------------------------

    def increment_register_window(self) -> int:
        """Additiv (Step 4), nicht in der Plan-"fix"-Liste. Grobe, globale Bremse für
        `/oauth/register` (Plan §2.7: 20 pro Stunde insgesamt) — stündliches, epoch-
        ausgerichtetes Fenster (Minute/Sekunde/Mikrosekunde der aktuellen Zeit gekappt). Anders
        als `login_attempts` gibt es hier kein `reset()`: jede Registrierung zählt gegen das
        Kontingent, unabhängig vom Ausgang; das Fenster verfällt von selbst zur nächsten vollen
        Stunde. Gibt den neuen Zähler dieses Fensters zurück."""
        now = self._now_fn()
        window_start = now.replace(minute=0, second=0, microsecond=0)
        window_key = _format_dt(window_start)
        with self._transaction() as conn:
            conn.execute(
                "INSERT INTO register_attempts (window_start, count) VALUES (?, 1) "
                "ON CONFLICT(window_start) DO UPDATE SET count = count + 1",
                (window_key,),
            )
            row = conn.execute(
                "SELECT count FROM register_attempts WHERE window_start = ?", (window_key,)
            ).fetchone()
            return row["count"]

    # -- Nutzerakten (Schema 2, P5 Step 2, Plan §2.3) -----------------------------------

    def _user_from_row(self, row: sqlite3.Row) -> UserRow:
        return UserRow(
            space=row["space"],
            password_hash=row["password_hash"],
            password_changed_at=_parse_dt_opt(row["password_changed_at"]),
            totp_secret_enc=row["totp_secret_enc"],
            totp_alg=row["totp_alg"],
            totp_confirmed_at=_parse_dt_opt(row["totp_confirmed_at"]),
            status=row["status"],
            created_at=_parse_dt(row["created_at"]),
        )

    def get_user(self, space: str) -> UserRow | None:
        with self._lock:
            row = self._conn.execute(
                "SELECT * FROM users WHERE space = ?", (space,)
            ).fetchone()
        return self._user_from_row(row) if row is not None else None

    def list_users(self) -> list[UserRow]:
        with self._lock:
            rows = self._conn.execute("SELECT * FROM users ORDER BY created_at").fetchall()
        return [self._user_from_row(row) for row in rows]

    def upsert_user(
        self,
        space: str,
        *,
        password_hash: str,
        totp_secret_enc: bytes | None,
        totp_alg: str,
        totp_confirmed_at: datetime | None,
        status: str,
    ) -> None:
        """Legt an oder überschreibt vollständig (bis auf `created_at`, das beim ersten Insert
        gesetzt und danach nie mehr verändert wird, und `password_changed_at`, das ausschließlich
        `set_password_hash()` gehört — ein `upsert_user()`-Aufruf ist keine Passwortänderung im
        Sinne von P5-P/Q, sondern eine Bestandsübernahme, z. B. aus `import_users_to_db.py`)."""
        now = self._now_fn()
        with self._lock:
            self._conn.execute(
                "INSERT INTO users (space, password_hash, password_changed_at, "
                "totp_secret_enc, totp_alg, totp_confirmed_at, status, created_at) "
                "VALUES (?, ?, NULL, ?, ?, ?, ?, ?) "
                "ON CONFLICT(space) DO UPDATE SET password_hash = excluded.password_hash, "
                "totp_secret_enc = excluded.totp_secret_enc, totp_alg = excluded.totp_alg, "
                "totp_confirmed_at = excluded.totp_confirmed_at, status = excluded.status",
                (
                    space, password_hash, totp_secret_enc, totp_alg,
                    _format_dt(totp_confirmed_at) if totp_confirmed_at is not None else None,
                    status, _format_dt(now),
                ),
            )

    def set_password_hash(self, space: str, password_hash: str) -> None:
        now = self._now_fn()
        with self._lock:
            self._conn.execute(
                "UPDATE users SET password_hash = ?, password_changed_at = ? WHERE space = ?",
                (password_hash, _format_dt(now), space),
            )

    def set_totp(self, space: str, *, secret_enc: bytes, alg: str) -> None:
        with self._lock:
            self._conn.execute(
                "UPDATE users SET totp_secret_enc = ?, totp_alg = ?, totp_confirmed_at = NULL "
                "WHERE space = ?",
                (secret_enc, alg, space),
            )

    def confirm_totp(self, space: str) -> None:
        now = self._now_fn()
        with self._lock:
            self._conn.execute(
                "UPDATE users SET totp_confirmed_at = ? WHERE space = ?",
                (_format_dt(now), space),
            )

    def set_user_status(self, space: str, status: str) -> None:
        with self._lock:
            self._conn.execute("UPDATE users SET status = ? WHERE space = ?", (status, space))

    # -- Einladungen (Schema 2, P5 Step 2) -----------------------------------------------

    def _invite_from_row(self, row: sqlite3.Row, *, consumed_at: datetime | None = None) -> InviteRow:
        return InviteRow(
            space=row["space"],
            purpose=row["purpose"],
            created_at=_parse_dt(row["created_at"]),
            expires_at=_parse_dt(row["expires_at"]),
            consumed_at=consumed_at if consumed_at is not None else _parse_dt_opt(row["consumed_at"]),
        )

    def create_invite(self, *, space: str, purpose: str, ttl_s: int) -> str:
        token = crypto.new_secret(32)
        now = self._now_fn()
        expires_at = now + timedelta(seconds=ttl_s)
        with self._lock:
            self._conn.execute(
                "INSERT INTO invites (token_hash, space, purpose, created_at, expires_at, "
                "consumed_at) VALUES (?, ?, ?, ?, ?, NULL)",
                (
                    crypto.hash_secret(token), space, purpose, _format_dt(now),
                    _format_dt(expires_at),
                ),
            )
        return token

    def peek_invite(self, token: str) -> InviteRow | None:
        """Rein lesend, für GET — zeigt z. B. eine Einladungsseite an, ohne sie zu verbrauchen."""
        token_hash = crypto.hash_secret(token)
        now = self._now_fn()
        with self._lock:
            row = self._conn.execute(
                "SELECT * FROM invites WHERE token_hash = ?", (token_hash,)
            ).fetchone()
        if row is None or row["consumed_at"] is not None:
            return None
        if _parse_dt(row["expires_at"]) <= now:
            return None
        return self._invite_from_row(row)

    def consume_invite(self, token: str) -> InviteRow | None:
        """Einmalig, für POST — analog zu `consume_auth_request()`."""
        token_hash = crypto.hash_secret(token)
        now = self._now_fn()
        with self._transaction() as conn:
            row = conn.execute(
                "SELECT * FROM invites WHERE token_hash = ?", (token_hash,)
            ).fetchone()
            if row is None or row["consumed_at"] is not None:
                return None
            if _parse_dt(row["expires_at"]) <= now:
                return None
            conn.execute(
                "UPDATE invites SET consumed_at = ? WHERE token_hash = ?",
                (_format_dt(now), token_hash),
            )
        return self._invite_from_row(row, consumed_at=now)

    def revoke_invites_for_space(self, space: str) -> int:
        """P5 Step 4 (Advisor-Fund): `authctl.py disable-user` widerruft Sitzungen und
        Token-Familien, aber ohne diese Methode blieb eine noch nicht eingelöste Einladung für
        denselben Space gültig — `_invite_post` legt über `upsert_user(..., status="active")`
        anschließend einfach eine neue, aktive Nutzerakte an und hebt die Sperre damit auf.
        Markiert alle noch nicht eingelösten Einladungen als eingelöst (`consumed_at = jetzt`) —
        **inklusive bereits abgelaufener**, kein `expires_at`-Filter: eine abgelaufene Zeile wäre
        über `peek_invite()`/`consume_invite()` ohnehin schon ungültig, der Filter würde nur die
        zurückgegebene Zählung verkleinern, nicht das Ergebnis ändern. Kein eigenes „revoked"-Feld
        nötig, `peek_invite()`/`consume_invite()` behandeln ein gesetztes `consumed_at` ohnehin
        als ungültig. Gibt die Anzahl betroffener Zeilen zurück (kann daher höher liegen als die
        Anzahl der zum Zeitpunkt des Aufrufs noch tatsächlich einlösbaren Einladungen), gleiche
        Grundidee wie `revoke_sessions_for_space()`/`revoke_families_for_space()`, aber ohne
        deren Live/Tot-Unterscheidung."""
        with self._transaction() as conn:
            now = self._now_fn()
            cur = conn.execute(
                "UPDATE invites SET consumed_at = ? WHERE space = ? AND consumed_at IS NULL",
                (_format_dt(now), space),
            )
            return cur.rowcount

    # -- Recovery-Codes (Schema 2, P5 Step 2) --------------------------------------------

    def replace_recovery_codes(self, space: str, codes: Iterable[str]) -> None:
        now = self._now_fn()
        with self._transaction() as conn:
            conn.execute("DELETE FROM recovery_codes WHERE space = ?", (space,))
            conn.executemany(
                "INSERT INTO recovery_codes (code_hash, space, created_at, used_at) "
                "VALUES (?, ?, ?, NULL)",
                [(crypto.hash_secret(code), space, _format_dt(now)) for code in codes],
            )

    def consume_recovery_code(self, space: str, code: str) -> bool:
        code_hash = crypto.hash_secret(code)
        now = self._now_fn()
        with self._transaction() as conn:
            row = conn.execute(
                "SELECT used_at FROM recovery_codes WHERE code_hash = ? AND space = ?",
                (code_hash, space),
            ).fetchone()
            if row is None or row["used_at"] is not None:
                return False
            conn.execute(
                "UPDATE recovery_codes SET used_at = ? WHERE code_hash = ?",
                (_format_dt(now), code_hash),
            )
        return True

    def count_unused_recovery_codes(self, space: str) -> int:
        with self._lock:
            row = self._conn.execute(
                "SELECT COUNT(*) AS n FROM recovery_codes WHERE space = ? AND used_at IS NULL",
                (space,),
            ).fetchone()
        return row["n"]

    # -- UI-Sessions (Schema 2, P5 Step 2) ------------------------------------------------

    def create_session(
        self, *, space: str, idle_ttl_s: int, absolute_ttl_s: int
    ) -> tuple[str, str]:
        """`idle_ttl_s` steht im Signatur-Vertrag (Plan §2.3), wird hier aber nicht ausgewertet:
        die Idle-Grenze wird erst bei `touch_session()` gegen `last_seen_at` geprüft, nie beim
        Anlegen selbst (`last_seen_at` ist beim Anlegen immer `now`, kann also nie schon
        abgelaufen sein). Der Parameter existiert für eine einheitliche Aufrufer-Signatur —
        `SessionManager` (Step 3) reicht dieselben zwei TTLs an beide Methoden durch."""
        session_id = crypto.new_secret(32)
        csrf_token = crypto.new_secret(32)
        now = self._now_fn()
        absolute_expires_at = now + timedelta(seconds=absolute_ttl_s)
        with self._lock:
            self._conn.execute(
                "INSERT INTO ui_sessions (session_hash, space, csrf_hash, created_at, "
                "last_seen_at, absolute_expires_at, revoked_at, revoked_reason) "
                "VALUES (?, ?, ?, ?, ?, ?, NULL, NULL)",
                (
                    crypto.hash_secret(session_id), space, crypto.hash_secret(csrf_token),
                    _format_dt(now), _format_dt(now), _format_dt(absolute_expires_at),
                ),
            )
        return session_id, csrf_token

    def touch_session(self, session_id: str, *, idle_ttl_s: int) -> SessionRow | None:
        """Einziger Lesepfad einer Sitzung (Plan §2.3): prüfen (nicht widerrufen, nicht absolut
        abgelaufen, `last_seen_at` nicht älter als `idle_ttl_s`), `last_seen_at` aktualisieren,
        Zeile zurückgeben — alles in einer Transaktion, damit keine Route „gültig" liest,
        während eine andere „abgelaufen" sähe."""
        session_hash = crypto.hash_secret(session_id)
        now = self._now_fn()
        with self._transaction() as conn:
            row = conn.execute(
                "SELECT * FROM ui_sessions WHERE session_hash = ?", (session_hash,)
            ).fetchone()
            if row is None or row["revoked_at"] is not None:
                return None
            if _parse_dt(row["absolute_expires_at"]) <= now:
                return None
            if (now - _parse_dt(row["last_seen_at"])).total_seconds() > idle_ttl_s:
                return None
            conn.execute(
                "UPDATE ui_sessions SET last_seen_at = ? WHERE session_hash = ?",
                (_format_dt(now), session_hash),
            )
        return SessionRow(
            session_hash=session_hash,
            space=row["space"],
            csrf_hash=row["csrf_hash"],
            created_at=_parse_dt(row["created_at"]),
            last_seen_at=now,
            absolute_expires_at=_parse_dt(row["absolute_expires_at"]),
            revoked_at=None,
            revoked_reason=None,
        )

    def revoke_session(self, session_id: str, reason: str) -> None:
        session_hash = crypto.hash_secret(session_id)
        now = self._now_fn()
        with self._lock:
            self._conn.execute(
                "UPDATE ui_sessions SET revoked_at = ?, revoked_reason = ? "
                "WHERE session_hash = ? AND revoked_at IS NULL",
                (_format_dt(now), reason, session_hash),
            )

    def revoke_sessions_for_space(
        self, space: str, *, except_session_id: str | None, reason: str
    ) -> int:
        now = self._now_fn()
        except_hash = (
            crypto.hash_secret(except_session_id) if except_session_id is not None else None
        )
        with self._lock:
            if except_hash is not None:
                cur = self._conn.execute(
                    "UPDATE ui_sessions SET revoked_at = ?, revoked_reason = ? "
                    "WHERE space = ? AND revoked_at IS NULL AND session_hash != ?",
                    (_format_dt(now), reason, space, except_hash),
                )
            else:
                cur = self._conn.execute(
                    "UPDATE ui_sessions SET revoked_at = ?, revoked_reason = ? "
                    "WHERE space = ? AND revoked_at IS NULL",
                    (_format_dt(now), reason, space),
                )
        return cur.rowcount

    def list_sessions(self, space: str) -> list[SessionRow]:
        with self._lock:
            rows = self._conn.execute(
                "SELECT * FROM ui_sessions WHERE space = ? ORDER BY created_at", (space,)
            ).fetchall()
        return [
            SessionRow(
                session_hash=row["session_hash"],
                space=row["space"],
                csrf_hash=row["csrf_hash"],
                created_at=_parse_dt(row["created_at"]),
                last_seen_at=_parse_dt(row["last_seen_at"]),
                absolute_expires_at=_parse_dt(row["absolute_expires_at"]),
                revoked_at=_parse_dt_opt(row["revoked_at"]),
                revoked_reason=row["revoked_reason"],
            )
            for row in rows
        ]
