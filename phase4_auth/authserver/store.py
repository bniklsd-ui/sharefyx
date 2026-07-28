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
from .models import AccessTokenRecord, AuthorizationCode, Client, LoginAttempt, PendingAuthRequest

SCHEMA_VERSION = "1"

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
            self._conn.execute(
                "INSERT OR IGNORE INTO schema_meta (key, value) VALUES ('schema_version', ?)",
                (SCHEMA_VERSION,),
            )

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
        self, refresh_token: str, *, access_ttl_s: int, refresh_ttl_s: int
    ) -> tuple[str, str] | None:
        """Abweichung vom Plan-Skelett: nimmt `access_ttl_s`/`refresh_ttl_s` entgegen statt sie
        aus vorhandenen Zeilen abzuleiten. Eine Ableitung aus dem jüngsten Access-Token der
        Familie bricht am echten Betriebspfad: `purge_expired()` (auch über `authctl.py
        purge-expired`) löscht abgelaufene Access-Tokens; ein Client, der erst nach Ablauf des
        Access-Tokens (60 min) aber innerhalb der Refresh-Gültigkeit (30 d) rotiert, träfe dann
        auf keine Zeile und die Ableitung würde crashen — kein Randfall, der Normalpfad einer
        langlebigen Session. Explizite Parameter sind kleinere Drift als dieser Absturzmodus.
        """
        token_hash = crypto.hash_secret(refresh_token)
        now = self._now_fn()
        with self._transaction() as conn:
            row = conn.execute(
                "SELECT r.*, f.revoked_at AS family_revoked_at, f.space AS space, "
                "f.scope AS scope, f.resource AS resource FROM refresh_tokens r "
                "JOIN token_families f ON f.family_id = r.family_id WHERE r.token_hash = ?",
                (token_hash,),
            ).fetchone()
            if row is None or row["family_revoked_at"] is not None:
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
        now_s = _format_dt(self._now_fn())
        with self._transaction() as conn:
            counts = {}
            # Tabellennamen kommen aus dem festen Tupel oben, nicht aus Nutzereingabe — sicher
            # zu interpolieren, nur der Zeitwert selbst ist ein gebundener Parameter.
            for table in ("auth_requests", "auth_codes", "access_tokens", "refresh_tokens"):
                cur = conn.execute(f"DELETE FROM {table} WHERE expires_at <= ?", (now_s,))
                counts[table] = cur.rowcount
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
