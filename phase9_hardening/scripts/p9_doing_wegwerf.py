#!/usr/bin/env python3
"""P9 Block doing — Wegwerf-Instanz **mit schreibfähigem CSRF-Origin** (Port 18776).

**Kopie von `p9_step_g_wegwerf.py` mit geänderten Konstanten, kein Import.** Die Step-G-Skripte
hängen an ihren Modulkonstanten (`ROOT`, `PORT`, `PROBE_TITEL`); ein Import würde sie verbiegen
und die Kopie wäre stillschweigend ein zweiter Aufruf derselben Instanz. Dieselbe Begründung
wie bei `p9e_reload_probe.py` / `p9a_legacy_probe.py`.

**Warum überhaupt eine eigene Instanz** — dieselbe Begründung wie in Step G, in Kurzform und
ohne Wiederholung der Herleitung: `security.py :: require_csrf` vergleicht den `Origin`-Header
des Browsers **exakt** mit `settings.base_url`, und das ist `SPACE_PUBLIC_BASE_URL`, das wegen
seiner Rolle als OAuth-Issuer zwingend `https://` sein muss (`authserver/config.py:87`). Ein
lokaler Plain-HTTP-Server kann die Prüfung also strukturell nie erfüllen, und `Origin` lässt
sich als verbotener Header nicht entfernen. Deshalb selbstsigniertes Zertifikat + Harness-
Launcher mit `ssl_keyfile`/`ssl_certfile`; `serve.py` selbst bleibt unberührt (ein
Produktparameter nur für einen Testharness wäre die Scope-Ausweitung aus P9-K).

Für diesen Block ist Schreibfähigkeit **kein Nebenschritt, sondern die Abnahme**: Station S5
schaltet im Editor den Status einer Aufgabe von `open` auf `doing`, und Station S6 liest
danach **ohne Reload** die Rail-Zähler. Genau dieser Pfad ist P9-64.

**Der Seed wird bei jedem Start neu angelegt** (frisches `DATA_ROOT`), nicht nur beim ersten
Mal — und das ist hier mehr als Hygiene: S5 **verbraucht** den Zustand (eine offene Aufgabe wird
zu einer laufenden). Ein zweiter Lauf auf derselben Instanz fände `open=0, doing=2` vor und
würde exakt dieselben Stationen noch einmal als „bestanden" melden, ohne etwas geprüft zu haben.

Eigener Port, eigenes `DATA_ROOT`, eigene `auth.sqlite3`, eigenes Keyring — die echte
`DATA_ROOT`/`auth.sqlite3`/den OS-Keyring berührt hier nichts (Hard Rule 9, Standing-Permission).
Gestoppt wird ausschließlich über die PID-Datei, nie per `pkill -f`.

    python phase9_hardening/scripts/p9_doing_wegwerf.py start
    ~/.claude-code-tools/e2e-venv/bin/python phase9_hardening/scripts/p9_doing_self_check.py
    python phase9_hardening/scripts/p9_doing_wegwerf.py stop
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
ROOT = Path("/tmp/opencode/p9-doing-wegwerf")   # eigener Wurzel-Ordner, V175
DATA_ROOT = ROOT / "data"
AUTH_DB = ROOT / "auth.sqlite3"
DEK_FILE = ROOT / "auth-dek"
KEYRING_FILE = ROOT / "keyring"
CREDS_FILE = ROOT / "credentials.json"
SERVE_PID = ROOT / "serve.pid"
SERVE_LOG = ROOT / "serve.log"
PORT = 18776                                     # V175: 18770-18779 waren am 2026-10-02 frei
BASE_URL = f"https://127.0.0.1:{PORT}"
PUBLIC_BASE_URL = BASE_URL
# Inhaltlich identisch mit `p9_step_g_wegwerf.py :: SERVE_TLS_LAUNCHER` — dieselbe App wie
# `phase2_mcp/scripts/serve.py`, nur mit TLS. Bewusst kopiert statt importiert: die Begründung
# steht im Docstring von `p9_step_g_wegwerf.py`, und ein Import würde dessen Modulkonstanten
# (Port 18775!) mitziehen.
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
# Vier Items in Space `alpha`, **einer je Statuswert**, damit die Rail-Zähler für „Offen" und
# „In Arbeit" beide 1 sind und der Sprung in S6 (1/1 -> 0/2) eindeutig ist. `assignee` ist an
# den beiden Aufgaben gesetzt, damit S8 prüfen kann, ob das UI-Speichern die Zuweisung verliert
# (P9-W) — die Maschinenebene soll `assignee` weiter durchreichen.
PROBE_ITEMS = (
    {"type": "task", "title": "Offene Probe", "status": "open", "assignee": "alpha"},
    {"type": "task", "title": "Laufende Probe", "status": "doing", "assignee": "alpha"},
    {"type": "task", "title": "Erledigte Probe", "status": "done"},
    {"type": "note", "title": "Probe-Notiz", "status": "active"},
)
TLS_KEY = ROOT / "key.pem"
TLS_CERT = ROOT / "cert.pem"


def _install_keyring() -> None:
    """Dasselbe Datei-Keyring-Backend wie `p9_step_g_wegwerf.py` (Zeile 98) — **nicht**
    `keyring.backends.file` aus der Standardbibliothek, das existiert nicht. Die Klasse ist
    absichtlich kopiert statt importiert: sie gehört zu einer anderen Phase, und ein Import
    würde deren Modulkonstanten (Port 18773!) mitziehen."""
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

        def delete_password(self, service: str, username: str) -> str | None:
            return self._data.get(service, {}).pop(username, None)

    keyring.set_keyring(FileBackend(KEYRING_FILE))


def _start() -> int:
    if SERVE_PID.exists():
        print("Es läuft bereits eine Instanz (serve.pid vorhanden) — erst `stop` aufrufen.",
              file=sys.stderr)
        return 1
    ROOT.mkdir(parents=True, exist_ok=True)
    # **Frisches `DATA_ROOT` bei jedem Start.** S5 verbraucht den Zustand; ohne dieses Löschen
    # wäre ein zweiter Lauf eine Wiederholung mit demselben Ergebnis und prüfte nichts mehr.
    if DATA_ROOT.exists():
        shutil.rmtree(DATA_ROOT)
    DATA_ROOT.mkdir(parents=True)
    if AUTH_DB.exists():
        AUTH_DB.unlink()
    if not DEK_FILE.exists():
        DEK_FILE.write_text(base64.urlsafe_b64encode(secrets.token_bytes(32)).decode() + "\n")
        os.chmod(DEK_FILE, 0o600)
    _install_keyring()

    from authserver import passwords, totp
    from authserver.config import decode_data_encryption_key
    from authserver.secretbox import seal
    from authserver.store import AuthStore
    from storage.store import Store

    store = Store(DATA_ROOT, git=False)
    for eintrag in PROBE_ITEMS:
        store.create("alpha", body="Probe-Item für den doing-Block.", **eintrag)
    store.rebuild_index()

    space = "alpha"
    password = "p9-doing-" + secrets.token_urlsafe(8)
    secret_b32 = totp.generate_secret()
    dek = decode_data_encryption_key(DEK_FILE.read_text().strip(), origin=str(DEK_FILE))
    auth = AuthStore(str(AUTH_DB), now_fn=lambda: datetime.datetime.now(datetime.timezone.utc))
    now = datetime.datetime.now(datetime.timezone.utc)
    auth.upsert_user(
        space=space,
        password_hash=passwords.hash_password(password),
        totp_secret_enc=seal(secret_b32.encode(), key=dek, aad=space.encode()),
        totp_alg="SHA1",
        totp_confirmed_at=now,
        status="active",
    )
    creds = {
        "space": space, "password": password,
        "otpauth_uri": totp.provisioning_uri(secret_b32, space=space, issuer="sharefyx",
                                             algo="SHA1"),
    }
    CREDS_FILE.write_text(json.dumps(creds, indent=2))
    os.chmod(CREDS_FILE, 0o600)

    env = os.environ.copy()
    env.update({
        "SPACE_DATA_ROOT": str(DATA_ROOT),
        "SPACE_AUTH_DB": str(AUTH_DB),
        # Der Wert, gegen den `require_csrf` vergleicht, ist exakt die URL, die der Browser
        # aufruft. Sonst kein Schreibvorgang möglich.
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
    # ausschließlich die eigene PID aus der eigenen PID-Datei (Hard Rule 9)
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


if __name__ == "__main__":
    befehl = sys.argv[1] if len(sys.argv) > 1 else "start"
    raise SystemExit({"start": _start, "stop": _stop}[befehl]())
