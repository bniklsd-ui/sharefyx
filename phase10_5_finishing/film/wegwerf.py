#!/usr/bin/env python3
"""P10.5 Block 16 — die Wegwerf-Instanzen des Launch-Films (Plan §4/§5, Hard Rule 9).

Zwei Instanzen mit **derselben** Saat: `neu` (HEAD, Port 8811) und `alt` (`v3.1.6` aus einem
`git worktree` auf `e5c834e`, Port 8812 — Plan §3.5 „3 → 4“). Jede hat ihren eigenen Baum unter
`/tmp/opencode/sharefyx-film-<name>/` (tmp-`DATA_ROOT`, tmp-`auth.sqlite3`, DEK-Datei als
`CREDENTIALS_DIRECTORY`), läuft mit TLS auf 127.0.0.1 (der CSRF-Origin-Vergleich verlangt https,
`p10_wegwerf.py`) und wird **nur** über ihre PID-Datei gestoppt.

**Code-Wurzel je Instanz.** Die Pakete stecken im `.venv` als *editable* (Meta-Path-Finder, die
**hinter** dem Pfad-Finder stehen) — ein `PYTHONPATH` auf die Phasenordner des Worktrees gewinnt
also, und die alte Instanz läuft mit **altem** Code aus demselben `.venv`. `status` prüft das an
der ausgelieferten Versionsangabe.

**Saat (Plan §4):** erfundene, neutrale Namen — kein Mensch, kein Host, kein Token im Bild. Feste
IDs und feste Uhr, damit die Karte in jedem Lauf dasselbe Bild ergibt (Muster
`probes/p105_b14_layout_probe.py`). Der angemeldete Principal heißt `studio`.

Aufruf (`.venv/bin/python`): `wegwerf.py <neu|alt> <setup|start|stop|status|cleanup>`.
Ausgabe JSON auf stdout; die Zugangsdaten der Wegwerf-Instanz liegen **nur** in ihrem tmp-Baum.
"""
from __future__ import annotations

import base64
import json
import os
import secrets
import signal
import ssl
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ALT_SHA = "e5c834e"
ALT_TREE = Path("/tmp/opencode/sharefyx-film-worktree-v316")
INSTANZEN = {"neu": {"port": 8811, "code": REPO_ROOT},
             "alt": {"port": 8812, "code": ALT_TREE}}
PHASEN = ["phase1_storage", "phase2_mcp", "phase4_auth", "phase5_ui", "phase6_shares"]
AKTEUR = "studio"

LAUNCHER = '''"""Dieselbe App wie phase2_mcp/scripts/serve.py, plus TLS (Muster p10_wegwerf.py)."""
import os
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

# Die Saat: Spaces mit erfundenem, neutralem Inhalt. Je Space Titel-Wörter, Ordner, Tags.
SAAT = '''
import sys
from pathlib import Path
from datetime import datetime, timezone
import storage.files as sfiles
from storage.store import Store
from storage.acl import create_space, add_member

_n = [0]
def _feste_id():
    _n[0] += 1
    return "itm_%08x" % (0xf1100000 + _n[0])
sfiles.generate_id = _feste_id

root = Path(sys.argv[1])
SPACES = {
  "studio":    (["Wochenplan", "Ideen", "Leseliste", "Notizen", "Skizzen", "Gedanken"], ["eingang", "projekte", "privat"]),
  "website":   (["Startseite", "Navigation", "Texte", "Bilder", "Formular", "Impressum"], ["entwurf", "inhalte", "technik"]),
  "recherche": (["Quelle", "Zitat", "Studie", "Interview", "Vergleich", "Befund"], ["material", "auswertung", "offen"]),
  "reise":     (["Route", "Unterkunft", "Packliste", "Budget", "Etappe", "Fahrplan"], ["planung", "buchungen", "unterwegs"]),
  "werkstatt": (["Prototyp", "Bauteil", "Messung", "Werkzeug", "Skizze", "Test"], ["bau", "teile", "protokolle"]),
}
COUNTS = {"studio": 32, "website": 30, "recherche": 30, "reise": 28, "werkstatt": 28}
TYPEN = [("task", "open"), ("note", "active"), ("task", "doing"), ("note", "active"), ("task", "done")]
for sp in SPACES:
    create_space(root, sp)
for sp in list(SPACES)[1:]:
    add_member(root, sp, "studio", write=True)
s = Store(root, git=False, now_fn=lambda: datetime(2026, 10, 30, 9, 0, 0, tzinfo=timezone.utc))
ids = {}
for sp, (worte, ordner) in SPACES.items():
    ids[sp] = []
    for i in range(COUNTS[sp]):
        typ, st = TYPEN[i % 5]
        extra = {"assignee": "studio"} if st == "doing" and i % 2 == 0 else {}
        it = s.create(sp, type=typ, status=st,
                      title="%s %d" % (worte[i % len(worte)], i // len(worte) + 1),
                      folder=ordner[i % len(ordner)],
                      tags=["%s" % ordner[(i + 1) % len(ordner)]],
                      body="Kurze Notiz zu %s." % worte[i % len(worte)], **extra)
        ids[sp].append(it.id)
namen = list(SPACES)
for k, sp in enumerate(namen):
    eigene = ids[sp]; n = len(eigene)
    nachbar = ids[namen[(k + 1) % len(namen)]]
    for j, ziel in enumerate(eigene):
        kand = [eigene[(j + 1) % n], eigene[(j + 7) % n]]
        if j % 5 == 0: kand.append(nachbar[j % len(nachbar)])
        if j == 0: kand += eigene[1:7]
        links = []
        for x in kand:
            if x not in links: links.append(x)
        s.update(ziel, version=1, links=links)
# Die Notiz der Editor-Szene (S2–S4): ein Anfang, den die Aufnahme weiterschreibt.
s.create("studio", type="note", title="Sommerfest", folder="projekte", tags=["planung"],
         body="Erste Ideen fuer das Sommerfest im Hof.\\n\\n")
s.rebuild_index()
print({sp: len(v) for sp, v in ids.items()})
'''


def _baum(name: str) -> Path:
    return Path(f"/tmp/opencode/sharefyx-film-{name}")


def _env(name: str) -> dict[str, str]:
    """Umgebung **gebaut**, nicht geerbt (Memory: test harness never inherits env)."""
    baum, inst = _baum(name), INSTANZEN[name]
    code = inst["code"]
    return {
        "HOME": os.environ.get("HOME", "/tmp"), "PATH": "/usr/bin:/bin", "LANG": "C.UTF-8",
        "PYTHONPATH": os.pathsep.join(str(code / p) for p in PHASEN),
        "SPACE_DATA_ROOT": str(baum / "data"), "SPACE_AUTH_DB": str(baum / "auth.sqlite3"),
        "SPACE_PUBLIC_BASE_URL": f"https://127.0.0.1:{inst['port']}",
        "SPACE_PORT": str(inst["port"]), "CREDENTIALS_DIRECTORY": str(baum / "cred"),
        "TLS_KEY": str(baum / "key.pem"), "TLS_CERT": str(baum / "cert.pem"),
    }


def _py(name: str, *args: str) -> subprocess.CompletedProcess:
    proc = subprocess.run([str(REPO_ROOT / ".venv/bin/python"), *args], env=_env(name),
                          cwd=str(_baum(name)), capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit(f"{name}: Unterprozess gescheitert:\n{proc.stderr[-2000:]}")
    return proc


def setup(name: str) -> dict:
    if name == "alt" and not ALT_TREE.exists():
        subprocess.run(["git", "-C", str(REPO_ROOT), "worktree", "add", "--detach",
                        str(ALT_TREE), ALT_SHA], check=True, capture_output=True)
    baum = _baum(name)
    (baum / "cred").mkdir(parents=True, exist_ok=True)
    (baum / "data").mkdir(parents=True, exist_ok=True)
    dek = baum / "cred" / "auth-dek"
    dek.write_text(base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b"=").decode() + "\n")
    os.chmod(dek, 0o600)
    passwort = "film-" + secrets.token_urlsafe(10)
    konto = _py(name, "-c", (
        "import sys, json\n"
        "from datetime import datetime, timezone\n"
        "from authserver import passwords, totp\n"
        "from authserver.config import decode_data_encryption_key\n"
        "from authserver.secretbox import seal\n"
        "from authserver.store import AuthStore\n"
        "space, pw, dekpfad, db = sys.argv[1:5]\n"
        "sec = totp.generate_secret()\n"
        "dek = decode_data_encryption_key(open(dekpfad).read().strip(), origin=dekpfad)\n"
        "st = AuthStore(db, now_fn=lambda: datetime.now(timezone.utc))\n"
        "st.upsert_user(space=space, password_hash=passwords.hash_password(pw),\n"
        "    totp_secret_enc=seal(sec.encode('ascii'), key=dek, aad=space.encode()),\n"
        "    totp_alg='SHA1', totp_confirmed_at=datetime.now(timezone.utc), status='active')\n"
        "print(json.dumps({'secret': sec}))\n"
    ), AKTEUR, passwort, str(dek), str(baum / "auth.sqlite3"))
    zugang = {"space": AKTEUR, "password": passwort, **json.loads(konto.stdout)}
    (baum / "zugang.json").write_text(json.dumps(zugang))
    os.chmod(baum / "zugang.json", 0o600)
    saat = _py(name, "-c", SAAT, str(baum / "data"))
    subprocess.run(["openssl", "req", "-x509", "-newkey", "rsa:2048", "-keyout",
                    str(baum / "key.pem"), "-out", str(baum / "cert.pem"), "-days", "3",
                    "-nodes", "-subj", "/CN=127.0.0.1", "-addext", "subjectAltName=IP:127.0.0.1"],
                   check=True, capture_output=True)
    (baum / "serve_tls.py").write_text(LAUNCHER, encoding="utf-8")
    return {"instanz": name, "baum": str(baum), "saat": saat.stdout.strip()}


def _lebt(pid: int) -> bool:
    return Path(f"/proc/{pid}").exists()


def _gesund(name: str, versuche: int = 60) -> bool:
    ctx = ssl._create_unverified_context()
    for _ in range(versuche):
        try:
            urllib.request.urlopen(f"https://127.0.0.1:{INSTANZEN[name]['port']}/health",
                                   timeout=1, context=ctx).read()
            return True
        except Exception:
            time.sleep(0.25)
    return False


def start(name: str) -> dict:
    baum = _baum(name)
    pidfile = baum / "serve.pid"
    if pidfile.exists() and _lebt(int(pidfile.read_text())):
        return {"instanz": name, "pid": int(pidfile.read_text()), "schon_aktiv": True}
    log = (baum / "serve.log").open("ab")
    proc = subprocess.Popen([str(REPO_ROOT / ".venv/bin/python"), str(baum / "serve_tls.py")],
                            env=_env(name), cwd=str(baum), stdout=log, stderr=subprocess.STDOUT,
                            start_new_session=True)
    pidfile.write_text(str(proc.pid))
    return {"instanz": name, "pid": proc.pid, "gesund": _gesund(name)}


def stop(name: str) -> dict:
    """Nur über die eigene PID-Datei (Hard Rule 9) — nie über ein Muster im Cmdline."""
    pidfile = _baum(name) / "serve.pid"
    if not pidfile.exists():
        return {"instanz": name, "gestoppt": False, "grund": "keine PID-Datei"}
    pid = int(pidfile.read_text())
    if _lebt(pid):
        os.kill(pid, signal.SIGTERM)
        for _ in range(20):
            if not _lebt(pid):
                break
            time.sleep(0.25)
        if _lebt(pid):
            os.kill(pid, signal.SIGKILL)
    pidfile.unlink()
    return {"instanz": name, "gestoppt": True, "pid": pid}


def status(name: str) -> dict:
    ctx = ssl._create_unverified_context()
    port = INSTANZEN[name]["port"]
    html = urllib.request.urlopen(f"https://127.0.0.1:{port}/ui/login", timeout=3,
                                  context=ctx).read().decode()
    return {"instanz": name, "gesund": _gesund(name, 4), "login_bytes": len(html)}


def cleanup(name: str) -> dict:
    import shutil
    out = stop(name)
    shutil.rmtree(_baum(name), ignore_errors=True)
    if name == "alt" and ALT_TREE.exists():
        subprocess.run(["git", "-C", str(REPO_ROOT), "worktree", "remove", "--force",
                        str(ALT_TREE)], check=True, capture_output=True)
    return {**out, "aufgeraeumt": True}


def main() -> int:
    name, cmd = sys.argv[1], sys.argv[2]
    if name not in INSTANZEN:
        raise SystemExit(f"unbekannte Instanz {name!r}")
    print(json.dumps({"setup": setup, "start": start, "stop": stop, "status": status,
                      "cleanup": cleanup}[cmd](name), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
