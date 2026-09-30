#!/usr/bin/env python3
"""P9 Step G — Wegwerf-Instanz **mit schreibfähigem CSRF-Origin** (Port 18774).

**Warum es eine zweite Instanz braucht.** Die vorhandene Wegwerf-Instanz (Port 18773,
`wegwerf_setup_v3ritt.py`) setzt `SPACE_PUBLIC_BASE_URL=https://wegwerf-v3ritt.invalid` —
**absichtlich**, damit kein Browser-Schreibvorgang sie verändern kann. `security.py :: require_csrf`
vergleicht den `Origin`-Header des Browsers (`http://127.0.0.1:18773`) mit `settings.base_url`, und
das schlägt bei **jedem** Schreibvorgang fehl — der Kommentar im Setup-Skript (Zeile 341) nennt das
selbst einen „Befund für Block D / Step Z, kein Ritt-Fix". Für einen Smoke, der **nur liest**, ist
das richtig; für Step G ist es blindmachend: der Löschpfad ist der erste, der im Browser wirklich
schreibt, und sein clientseitiger Teil wäre sonst nur statisch belegt.

Diese Instanz setzt deshalb `SPACE_PUBLIC_BASE_URL` auf **genau** die URL, unter der der Browser
sie aufruft. Sonst ändert sich am Produktivcode nichts — es ist eine Konfiguration, keine
Sonderlocke: derselbe CSRF-Vergleich läuft, er passiert nur.

Eigener Port, eigenes `DATA_ROOT`, eigene `auth.sqlite3`, eigenes Keyring — die echte
`DATA_ROOT`/`auth.sqlite3`/den OS-Keyring berührt hier nichts (Hard Rule 9 und die
Standing-Permission). Gestoppt wird ausschließlich über die PID-Datei, nie per `pkill -f`.

    python phase9_hardening/scripts/p9_step_g_wegwerf.py start
    python phase9_hardening/scripts/p9_step_g_wegwerf.py stop
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
ROOT = Path("/tmp/opencode/p9-step-g-wegwerf")
DATA_ROOT = ROOT / "data"
AUTH_DB = ROOT / "auth.sqlite3"
DEK_FILE = ROOT / "auth-dek"
KEYRING_FILE = ROOT / "keyring"
CREDS_FILE = ROOT / "credentials.json"
SERVE_PID = ROOT / "serve.pid"
SERVE_LOG = ROOT / "serve.log"
PORT = 18775
BASE_URL = f"https://127.0.0.1:{PORT}"
PUBLIC_BASE_URL = BASE_URL
# **TLS ist hier keine Kosmetik, sondern die Voraussetzung für einen Schreibvorgang.**
# `require_csrf` (security.py:79-95) hat drei Schichten: `Origin` muss **exakt**
# `settings.base_url` entsprechen; fehlt `Origin`, muss `sec-fetch-site: same-origin` kommen; und
# `X-CSRF-Token` muss zum Sitzungs-Hash passen. `settings.base_url` ist in
# `mcpserver/app.py:204` genau `oauth.settings.base_url`, also `SPACE_PUBLIC_BASE_URL`, und das
# muss laut `authserver/config.py:87` zwingend `https://` sein (Rolle als OAuth-Issuer).
# Ein Browser auf `http://127.0.0.1:18773` kann die Prüfung also **strukturell nie** erfüllen —
# und `Origin` lässt sich nicht entfernen (verbotener Header, `page.route()` bleibt wirkungslos,
# gemessen). Deshalb ein selbstsigniertes Zertifikat für `IP:127.0.0.1` und ein Harness-Launcher,
# der dieselbe App wie `serve.py` baut, nur mit `ssl_keyfile`/`ssl_certfile`. `serve.py` selbst
# zu ändern wäre eine Produktänderung für einen Testzweck — das wäre die_scope-Ausweitung, die
# P9-K gerade vermeiden soll.
# Harness-Launcher als Konstante: er liegt unter /tmp (Wegwerf-Wurzel), wird aber aus dem Repo
# erzeugt, damit die Instanz ohne loses Nebenskript reproduzierbar bleibt. Inhalt siehe
# `SERVE_TLS_LAUNCHER` unten — bewusst eine Kopie der `serve.py`-Verdrahtung, NICHT ein Import
# von `serve.py` (dessen `main()` ruft `uvicorn.run()` ohne `ssl_*`, und ein Produkt-Parameter
# nur für einen Testharness wäre die Scope-Ausweitung aus P9-K).
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
PROBE_TITEL = ("Löschen in Probe", "Nachbar bleibt", "Dritte Aufgabe")
TLS_KEY = ROOT / "key.pem"
TLS_CERT = ROOT / "cert.pem"


def _install_keyring() -> None:
    """Dasselbe Datei-Keyring-Backend wie `wegwerf_setup_v3ritt.py` (Zeile 175) — **nicht**
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
    for d in (ROOT, DATA_ROOT):
        d.mkdir(parents=True, exist_ok=True)
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
    # **Immer neu säen, nicht nur beim ersten Mal.** Das Selbstprüfungs-Skript löscht pro Lauf
    # ein Item, und der Papierkorb unsichtbar zu halten heißt gerade, dass er sich nicht
    # zurücksetzen lässt: ein zweiter Lauf fände eine leere Liste und prüfte nichts mehr. Drei
    # Items mit festen Titeln (einer davon heißt "Nachbar bleibt", weil die Prüfungen darauf
    # prüfen) — ein frischer Lauf ist damit von jedem vorherigen unabhängig.
    for titel in PROBE_TITEL:
        store.create("alpha", type="task", title=titel, body="Probe-Item für Step G.")
    store.rebuild_index()

    space = "alpha"
    password = "p9-step-g-" + secrets.token_urlsafe(8)
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
        # **Der** Unterschied zum 18773er Setup: der Wert, gegen den `require_csrf` vergleicht,
        # ist exakt die URL, die der Browser aufruft. Sonst kein Schreibvorgang möglich.
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
