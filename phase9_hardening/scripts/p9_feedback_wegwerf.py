#!/usr/bin/env python3
"""P9 Block feedback (Kopie der trace-Instanz) — Wegwerf-Instanz mit **zwei Principals** und Git-Historie (Port 18778).

**Kopie von `p9_doing_wegwerf.py` mit geänderten Konstanten, kein Import** — dieselbe
Begründung wie dort: ein Import würde dessen Modulkonstanten (Port 18776) mitziehen und die
Kopie wäre stillschweigend ein zweiter Aufruf derselben Instanz.

**Warum diese Instanz zwei Dinge hat, die `p9_doing_wegwerf.py` nicht hat:**

1. **Zwei Konten** (`alpha` und `beta`) in einem gemeinsamen Space `team` mit
   `.share.yml` (`read`/`write` fuer beide). Der ganze Block ist eine Aussage ueber *zwei
   Personen*: `updated_by` muss wechseln, `assignee` darf es nicht. Mit einem einzigen
   eingeloggten Menschen waere genau der haeufigste Fehler unsichtbar — beide Felder wuerden
   denselben Wert tragen und der Test waere gruen.
2. **`git=True`.** Station **S6** liest `git log --format=%an` im `DATA_ROOT` — der
   Git-Autor ist eine eigene Zusage (P9-AC) neben dem Frontmatter-Feld, und ein Test, der nur
   das Feld prueft, wuerde eine Implementierung bestehen lassen, die den Autor vergisst. Die
   Instanz braucht also echte Commits, und die Committer-Identitaet wird wie in jedem echten
   Betrieb von `history.ensure_repo()` gesetzt (`Space Server`).

**Seed bei jedem Start neu** (frisches `DATA_ROOT`): die Stationen S1/S4/S5 **verbrauchen**
Zustand (ein `open` wird `doing`, ein Titel wird geaendert). Ein zweiter Lauf auf derselben
Instanz wuerde dieselben Stationen als bestanden melden, ohne etwas geprueft zu haben.

**Der Legacy-Item** (`Ohne updated_by`) wird von Hand in die Datei geschrieben, **nach** dem
Seed, damit er garantiert kein Feld traegt — ein per `store.create()` angelegter Item haette
nach dem Block-Deploy ein `updated_by`. Genau das ist der Fall S7 prueft.

Eigener Port, eigenes `DATA_ROOT`, eigene `auth.sqlite3`, eigenes Keyring — die echte
`DATA_ROOT`/`auth.sqlite3`/den OS-Keyring beruehrt hier nichts (Hard Rule 9,
Standing-Permission). Gestoppt wird ausschliesslich ueber die PID-Datei, nie per `pkill -f`.

    python phase9_hardening/scripts/p9_feedback_wegwerf.py start
    ~/.claude-code-tools/e2e-venv/bin/python phase9_hardening/scripts/p9_feedback_self_check.py
    python phase9_hardening/scripts/p9_feedback_wegwerf.py stop
"""
from __future__ import annotations

import base64
import datetime
import json
import os
import secrets
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ROOT = Path("/tmp/opencode/p9-feedback-wegwerf")   # eigener Wurzel-Ordner, V175
DATA_ROOT = ROOT / "data"
AUTH_DB = ROOT / "auth.sqlite3"
DEK_FILE = ROOT / "auth-dek"
KEYRING_FILE = ROOT / "keyring"
CREDS_FILE = ROOT / "credentials.json"
SERVE_PID = ROOT / "serve.pid"
SERVE_LOG = ROOT / "serve.log"
PORT = 18778                                     # V175: 18778: eigener Port des feedback-Blocks
BASE_URL = f"https://127.0.0.1:{PORT}"
PUBLIC_BASE_URL = BASE_URL

PRINCIPALS = ("alpha", "beta")
TEAM_SPACE = "team"

# Inhaltlich identisch mit `p9_doing_wegwerf.py :: SERVE_TLS_LAUNCHER` — dieselbe App wie
# `phase2_mcp/scripts/serve.py`, nur mit TLS. Bewusst kopiert statt importiert, Begründung dort.
SERVE_TLS_LAUNCHER = '''"""Dieselbe App wie phase2_mcp/scripts/serve.py, plus TLS."""
import os, sys
sys.path.insert(0, os.environ["REPO_ROOT"])
from datetime import datetime, timezone
import uvicorn
from authserver.config import load_auth_settings, load_data_encryption_key
from authserver.store import AuthStore
from authserver.userdir import UserDirectory
from storage.store import Store
from mcpserver.app import OAuthConfig, create_app
from mcpserver.config import load_settings
from mcpserver.logging_setup import configure_logging
from mcpserver.request_log import AccessLogASGI, OAuthLogASGI

settings = load_settings()
configure_logging(settings.log_level)
auth_settings = load_auth_settings()
auth_store = AuthStore(auth_settings.db_path, now_fn=lambda: datetime.now(timezone.utc))
users = UserDirectory(auth_store, dek=load_data_encryption_key())
oauth = OAuthConfig(settings=auth_settings, store=auth_store, users=users)
app = create_app(settings=settings, store=Store(settings.data_root),
                 allowed_hosts=["127.0.0.1"], oauth=oauth)
app = AccessLogASGI(OAuthLogASGI(app))
uvicorn.run(app, host=settings.host, port=settings.port, access_log=False,
            log_level=settings.log_level.lower(),
            ssl_keyfile=os.environ["TLS_KEY"], ssl_certfile=os.environ["TLS_CERT"])
'''

# Drei Items im geteilten Space. **`actor` bewusst nur beim ersten** — so traegt der
# Legacy-Item (S7) garantiert kein Feld, und der zweite traegt `assignee: alpha`, damit S5
# die P9-Z-Regel an einem **fremd zugewiesenen** Item prueft (der harte Fall: B zieht A's
# Aufgabe in Arbeit und darf sie nicht uebernehmen).
PROBE_ITEMS = (
    {"type": "task", "title": "Angebot schreiben", "status": "open", "actor": "alpha"},
    {"type": "task", "title": "Kabel suchen", "status": "open", "assignee": "alpha"},
    {"type": "note", "title": "Legacy-Notiz", "status": "active", "actor": "alpha"},
)
LEGACY_TITLE = "Legacy-Notiz"
E1A_ITEMS = (
    {"type": "task", "title": "E1a Loeschen", "status": "open", "actor": "beta"},
    {"type": "task", "title": "E1a Ziehen", "status": "open", "actor": "beta"},
)

TLS_KEY = ROOT / "key.pem"
TLS_CERT = ROOT / "cert.pem"


def _install_keyring() -> None:
    """Dasselbe Datei-Keyring-Backend wie `p9_doing_wegwerf.py` — **nicht**
    `keyring.backends.file` aus der Standardbibliothek, das existiert nicht. Die Klasse ist
    absichtlich kopiert statt importiert: sie gehoert zu einer anderen Phase, und ein Import
    wuerde deren Modulkonstanten mitziehen."""
    import keyring
    import keyring.backend
    import keyring.compat

    class FileBackend(keyring.backend.KeyringBackend):
        @keyring.compat.properties.classproperty
        def priority(cls) -> float:  # type: ignore[override]
            return 1

        def __init__(self, path: Path) -> None:
            keyring.backend.KeyringBackend.__init__(self)
            self.path = path
            self._data = json.loads(path.read_text()) if path.exists() else {}

        def _save(self) -> None:
            self.path.write_text(json.dumps(self._data))

        def set_password(self, service: str, username: str, password: str) -> None:
            self._data.setdefault(service, {})[username] = password
            self._save()

        def get_password(self, service: str, username: str) -> str | None:
            return self._data.get(service, {}).get(username)

        def delete_password(self, service: str, username: str) -> None:
            self._data.get(service, {}).pop(username, None)

    keyring.set_keyring(FileBackend(KEYRING_FILE))


def _seed() -> None:
    """Space `team` mit `.share.yml`, drei Items mit Akteur, dann der Legacy-Item von Hand.

    Die Item-Reihenfolge ist der Grund fuer zwei getrennte Schritte: `store.create()` im
    neuen Code setzt `updated_by` aus dem `actor` — der Legacy-Item **darf** das nicht
    tragen. Ihn also nach dem Seed per Dateizugriff zu strippen waere anfaellig (ein
    `store`-Aufruf koennte es wieder zurueckschreiben), deshalb wird er von vornherein ohne
    das Feld angelegt und danach **einmalig** per `sed` die Zeile entfernt, mit anschliessender
    Index-Neuaufbau."""
    from authserver import passwords, totp
    from authserver.config import decode_data_encryption_key
    from authserver.secretbox import seal
    from authserver.store import AuthStore
    from storage.store import Store

    (DATA_ROOT / TEAM_SPACE).mkdir(parents=True, exist_ok=True)
    (DATA_ROOT / TEAM_SPACE / ".share.yml").write_text(
        f"read: [{', '.join(PRINCIPALS)}]\nwrite: [{', '.join(PRINCIPALS)}]\n", encoding="utf-8"
    )
    # `git=True` — S6 liest `git log --format=%an` im DATA_ROOT (P9-AC).
    store = Store(DATA_ROOT, git=True)
    for eintrag in PROBE_ITEMS:
        store.create(TEAM_SPACE, body="Probe-Item fuer den trace-Block.", **eintrag)
    # E1a (P9-BP/BQ, 2026-10-08): zwei Items, die **beta** angelegt hat — alpha loescht und zieht
    # sie in der Probe. Ein Item von alpha selbst wuerde „auch fremde Items" nicht pruefen.
    store.ensure_folder(TEAM_SPACE, "ablage")
    for eintrag in E1A_ITEMS:
        store.create(TEAM_SPACE, body="Probe-Item fuer E1a.", **eintrag)
    store.rebuild_index()

    dek = decode_data_encryption_key(DEK_FILE.read_text().strip(), origin=str(DEK_FILE))
    auth = AuthStore(str(AUTH_DB), now_fn=lambda: datetime.datetime.now(datetime.timezone.utc))
    now = datetime.datetime.now(datetime.timezone.utc)
    creds: dict[str, dict] = {}
    for space in PRINCIPALS:
        password = f"p9-trace-{secrets.token_urlsafe(8)}"
        secret_b32 = totp.generate_secret()
        auth.upsert_user(
            space=space,
            password_hash=passwords.hash_password(password),
            totp_secret_enc=seal(secret_b32.encode(), key=dek, aad=space.encode()),
            totp_alg="SHA1",
            totp_confirmed_at=now,
            status="active",
        )
        creds[space] = {
            "space": space, "password": password,
            "otpauth_uri": totp.provisioning_uri(
                secret_b32, space=space, issuer="sharefyx", algo="SHA1"
            ),
        }
    CREDS_FILE.write_text(json.dumps(creds, indent=2))
    os.chmod(CREDS_FILE, 0o600)


def _strip_updated_by_from_legacy_item() -> None:
    """Der Legacy-Item verliert `updated_by` **nach** dem Seed — und der Index wird danach
    neu aufgebaut, damit die Zeile auf der Platte und die im Index uebereinstimmen. Wuerde
    der Index nicht neu aufgebaut, wuerde der naechste `get()` die Datei lesen (der Wert
    waere korrekt) und die Trefferliste trotzdem `updated_by: "alpha"` zeigen — eine
    Divergenz, die S3/S7 dann als echter Fehler melden wuerde."""
    (treffer,) = list((DATA_ROOT / TEAM_SPACE).glob("*__legacy-notiz.md"))
    text = treffer.read_text(encoding="utf-8")
    zeilen = [z for z in text.splitlines(keepends=True) if not z.startswith("updated_by:")]
    treffer.write_text("".join(zeilen), encoding="utf-8")

    from storage.store import Store

    Store(DATA_ROOT, git=True).rebuild_index()


def _start() -> int:
    if SERVE_PID.exists():
        print("Es laeuft bereits eine Instanz (serve.pid vorhanden) — erst `stop` aufrufen.",
              file=sys.stderr)
        return 1
    ROOT.mkdir(parents=True, exist_ok=True)
    if DATA_ROOT.exists():
        shutil.rmtree(DATA_ROOT)
    DATA_ROOT.mkdir(parents=True)
    if AUTH_DB.exists():
        AUTH_DB.unlink()
    if not DEK_FILE.exists():
        DEK_FILE.write_text(base64.urlsafe_b64encode(secrets.token_bytes(32)).decode() + "\n")
        os.chmod(DEK_FILE, 0o600)
    _install_keyring()
    _seed()
    _strip_updated_by_from_legacy_item()

    env = os.environ.copy()
    env.update({
        "SPACE_DATA_ROOT": str(DATA_ROOT),
        "SPACE_AUTH_DB": str(AUTH_DB),
        # Der Wert, gegen den `require_csrf` vergleicht, ist exakt die URL, die der Browser
        # aufruft. Sonst kein Schreibvorgang moeglich.
        "SPACE_PUBLIC_BASE_URL": PUBLIC_BASE_URL,
        "SPACE_PORT": str(PORT),
        "CREDENTIALS_DIRECTORY": str(ROOT),
        "PYTHONPATH": str(REPO_ROOT),
        "REPO_ROOT": str(REPO_ROOT),
        "TLS_KEY": str(TLS_KEY),
        "TLS_CERT": str(TLS_CERT),
    })
    launcher = ROOT / "serve_tls.py"
    if not launcher.exists():
        launcher.write_text(SERVE_TLS_LAUNCHER, encoding="utf-8")
    if not (TLS_KEY.exists() and TLS_CERT.exists()):
        subprocess.run(
            ["openssl", "req", "-x509", "-newkey", "rsa:2048", "-keyout", str(TLS_KEY),
             "-out", str(TLS_CERT), "-days", "2", "-nodes", "-subj", "/CN=127.0.0.1",
             "-addext", "subjectAltName=IP:127.0.0.1"],
            check=True, capture_output=True,
        )
    log = SERVE_LOG.open("ab")
    proc = subprocess.Popen(
        [".venv/bin/python", str(ROOT / "serve_tls.py")],
        env=env, cwd=str(REPO_ROOT), stdout=log, stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    SERVE_PID.write_text(str(proc.pid))
    import ssl
    ctx = ssl._create_unverified_context()
    for i in range(60):
        try:
            urllib.request.urlopen(f"{BASE_URL}/health", timeout=1, context=ctx).read()
            print(f"PID {proc.pid} -> {SERVE_PID} | gesund nach {i * 0.25:.1f}s | Base {BASE_URL}")
            print(f"Credentials -> {CREDS_FILE}")
            return 0
        except Exception:
            time.sleep(0.25)
    print("Server wurde nicht gesund — siehe serve.log", file=sys.stderr)
    return 1


def _stop() -> int:
    if not SERVE_PID.exists():
        print("Kein serve.pid — nichts zu stoppen.")
        return 0
    pid = int(SERVE_PID.read_text().strip())
    # ausschliesslich die eigene PID aus der eigenen PID-Datei (Hard Rule 9)
    os.kill(pid, 15)
    for _ in range(40):
        try:
            os.kill(pid, 0)
        except OSError:
            SERVE_PID.unlink()
            print(f"PID {pid} gestoppt (PID-Datei entfernt).")
            return 0
        time.sleep(0.25)
    print(f"PID {pid} reagiert nicht auf SIGTERM.", file=sys.stderr)
    return 1


def _git_autoren() -> list[str]:
    """`git log --format=%an` newest-first im Wegwerf-`DATA_ROOT` — der Beleg fuer S6."""
    result = subprocess.run(
        ["git", "-C", str(DATA_ROOT), "log", "--format=%an"],
        capture_output=True, text=True, check=True,
    )
    return result.stdout.strip().splitlines()


if __name__ == "__main__":
    befehl = sys.argv[1] if len(sys.argv) > 1 else "start"
    raise SystemExit({"start": _start, "stop": _stop}[befehl]())
