#!/usr/bin/env python3
"""P9 Step D — Wegwerf-Instanz **mit Ordnerinhalt** (Port 18781).

**Warum eine dritte Instanz und nicht die von Step G (Port 18775).** Step G hat eine
wiederverwendbare Begründung, die auch hier gilt — `require_csrf` vergleicht den `Origin`-Header
mit `SPACE_PUBLIC_BASE_URL`, also muss die Instanz unter genau der URL laufen, unter der der
Browser sie aufruft, und das wiederum über TLS. Die *Daten* brauchen sie aber nicht: Step G sät
drei Items an der **Space-Wurzel** (`store.create(...)` ohne `folder=`), und der Schritt, den
hier geprüft wird, ist ein Zug **aus einem Ordner** heraus. Eine Instanz, deren Fixture den
Gegenstand des Tests nicht enthält, wäre kein Wegwerf-Setup, sondern eine Fehlermeldung, die man
durch Lesen nicht sieht. Also eigener Datenbestand, eigener Port, sonst dasselbe Muster.

**Was dieses Skript sät** (Immer neu, nicht nur beim ersten Mal — derselbe Grund wie in Step G:
das Selbstprüfungs-Skript verschiebt ein Item, ein zweiter Lauf fände die Liste leer):

  - Ordner **Rechnungen** mit zwei Items: `Rechnung September` (die Quelle des Zugs) und
    `Steuern 2026` (Quelle für den Leerlauf-Guard, `tree.js:139`).
  - `Wurzel-Notiz` an der Space-Wurzel (Kontrolle: die Wurzel ist nicht leer, und die
    Gegenrichtung — Wurzel **in** den Ordner — bleibt prüfbar).

Eigener Port, eigenes `DATA_ROOT`, eigene `auth.sqlite3`, eigenes Keyring — die echte
`DATA_ROOT`/`auth.sqlite3`/der OS-Keyring werden von hier nicht berührt (Hard Rule 9 und die
Standing-Permission). Gestoppt wird ausschließlich über die PID-Datei, nie per `pkill -f`.

    python phase9_hardening/scripts/p9_step_d_wegwerf.py start
    python phase9_hardening/scripts/p9_step_d_wegwerf.py stop
"""
from __future__ import annotations

import base64
import datetime
import json
import os
import secrets
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ROOT = Path("/tmp/opencode/p9-step-d-wegwerf")
DATA_ROOT = ROOT / "data"
AUTH_DB = ROOT / "auth.sqlite3"
DEK_FILE = ROOT / "auth-dek"
KEYRING_FILE = ROOT / "keyring"
CREDS_FILE = ROOT / "credentials.json"
SERVE_PID = ROOT / "serve.pid"
SERVE_LOG = ROOT / "serve.log"
PORT = 18781
BASE_URL = f"https://127.0.0.1:{PORT}"
PUBLIC_BASE_URL = BASE_URL
TLS_KEY = ROOT / "key.pem"
TLS_CERT = ROOT / "cert.pem"

ORDNER = "Rechnungen"
# Fest verdrahtete Titel, weil das Selbstprüfungs-Skript sie braucht: es sucht die Zeile über den
# Titel und prüft den Toast-Text. Bei einem zufälligen Namen wäre die Prüfung eine Zufallsprobe.
SAAT = [
    ("Rechnung September", ORDNER),
    ("Steuern 2026", ORDNER),
    ("Wurzel-Notiz", ""),
]

# Dieselbe App wie `phase2_mcp/scripts/serve.py`, plus TLS. **Kopie der Verdrahtung, kein Import:**
# `serve.py`s `main()` ruft `uvicorn.run()` ohne `ssl_*`, und einen Produktparameter nur für einen
# Testharness zu ergänzen wäre die Scope-Ausweitung, die P9-K gerade vermeiden soll (identische
# Begründung und identische Lösung wie bei Step G — die Kopie ist hier Absicht, nicht Faulheit).
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


def _install_keyring() -> None:
    """Dasselbe Datei-Keyring-Backend wie in `p9_step_g_wegwerf.py` — `keyring.backends.file` aus
    der Standardbibliothek existiert nicht, die Klasse ist also kopiert statt importiert (sie
    gehört zu einer anderen Phase und würde deren Modulkonstanten mitschleppen)."""
    import keyring
    import keyring.backend
    import keyring.compat

    class FileBackend(keyring.backend.KeyringBackend):  # type: ignore[misc]
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


def _leere_datenbestand() -> None:
    """**Vor** dem Säen leeren, nicht danach.

    `store.create()` hängt an, es leert nicht: ein zweiter `start` auf demselben `DATA_ROOT` hätte
    die Item-Liste des ersten Laufs behalten (gemessen — der zweite Lauf sah `Wurzel-Notiz` zweimal
    und der Zug fand die Zeile nicht mehr, weil der vorherige Lauf sie schon verschoben hatte).
    Ein Wegwerf-Bestand, der über Läufe hinweg wächst, ist keiner; deshalb wird hier gelöscht.

    Die Schranke ist eine feste Vorbedingung, keine Absicht: gelöscht wird **nur** dieses eine
    Verzeichnis unter `/tmp/opencode`, und `ROOT` muss zusätzlich auf den hier definierten Namen
    enden. Damit kann diese Funktion auch bei einem verkannten Aufruf nicht die echte `DATA_ROOT`
    erreichen (Hard Rule 9) — `rmtree` auf einem falsch zusammengesetzten Pfad wäre der teuerste
    Fehler, den ein Wegwerf-Harness machen kann.
    """
    import shutil

    if ROOT.parent != Path("/tmp/opencode") or not ROOT.name.startswith("p9-step-d-wegwerf"):
        raise SystemExit(f"Abbruch: DATA_ROOT-Wurzel ist nicht die Wegwerf-Instanz: {ROOT}")
    shutil.rmtree(DATA_ROOT, ignore_errors=True)
    DATA_ROOT.mkdir(parents=True, exist_ok=True)


def _start() -> int:
    for d in (ROOT,):
        d.mkdir(parents=True, exist_ok=True)
    _leere_datenbestand()
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
    for titel, ordner in SAAT:
        store.create("alpha", type="task", title=titel, body="Probe-Item für Step D.",
                     folder=ordner)
    store.rebuild_index()

    space = "alpha"
    password = "p9-step-d-" + secrets.token_urlsafe(8)
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
