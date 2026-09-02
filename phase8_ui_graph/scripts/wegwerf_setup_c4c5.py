#!/usr/bin/env python3
"""Phase 8 Block C C4+C5 -- Wegwerf-Instanz aufsetzen, starten, stoppen, aufraeumen.

Steht im Standing-Permission-Rahmen der Phase (CLAUDE.md Wurzel + Phase 8 §0.0):
eigener Port (18770), tmp-DATA_ROOT, File-Keyring-Backend statt `nikinger-space`,
User direkt in auth.sqlite3 provisioniert (kein provision_user.py, kein
keyring.set_password). Cleanup per `kill -TERM $(cat serve.pid)` -- kein
`pkill -f` mit Regex (Hard Rule 9).

Datenlage ist absichtlich klein (5 eigene Items + 2 fremde = 7 Items ueber zwei
Spaces): der Smoke-Lauf prueft strukturell, ob die C4/C5-Verbauungen greifen
(Glass auf Liste-Kopf/Dialog/Toast/Update-Banner, 3px-Akzentkante auf ausgewaehlter
Zeile, 72ch-zentrierter Editor-Body, ::selection-Styling). Visuelle Feinjustierung
macht die Nikinger-Sichtpruefung 3 am echten Geraet, nicht dieser Lauf.

Hinweis zu Folder-Support: wir nutzen fuer C4C5 bewusst KEINE folders (anders als
D1/D2/Sichtpruefung2) -- C4/C5 ist ein reiner Design-Schritt, keine Graph-Aenderung.
Die Spaces dienen nur dazu, dass die foreign-Zeile in der Overview sichtbar wird.
"""
from __future__ import annotations

import argparse
import json
import os
import secrets
import signal
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import keyring
import keyring.backend

WEGWERF_ROOT = Path("/tmp/opencode/sharefyx-wegwerf-c4c5")
DATA_ROOT = WEGWERF_ROOT / "data"
AUTH_DB = WEGWERF_ROOT / "auth.sqlite3"
KEYRING_FILE = WEGWERF_ROOT / "keyring.json"
DEK_FILE = WEGWERF_ROOT / "auth-dek"
CREDS_FILE = WEGWERF_ROOT / "credentials.json"
SERVE_PID = WEGWERF_ROOT / "serve.pid"
SERVE_LOG = WEGWERF_ROOT / "serve.log"
PORT = 18770
OWN_SPACE = "alpha"
FOREIGN_SPACE = "beta"

REPO_ROOT = Path(__file__).resolve().parents[2]


class FileBackend(keyring.backend.KeyringBackend):
    """Trivial file-backed Keyring -- nichts mit dem echten `nikinger-space`-Service
    zu tun, ausschliesslich fuer diese Wegwerf-Instanz."""

    def __init__(self, path: Path):
        self._path = path
        if path.exists():
            self._data = json.loads(path.read_text())
        else:
            self._data = {}

    def _save(self) -> None:
        self._path.write_text(json.dumps(self._data))
        os.chmod(self._path, 0o600)

    def get_password(self, service: str, username: str) -> str | None:
        return self._data.get(service, {}).get(username)

    def set_password(self, service: str, username: str, password: str) -> None:
        self._data.setdefault(service, {})[username] = password
        self._save()

    def delete_password(self, service: str, username: str) -> str | None:
        return self._data.get(service, {}).pop(username, None)


def _install_keyring() -> None:
    keyring.set_keyring(FileBackend(KEYRING_FILE))


def _setup_root() -> None:
    import base64
    WEGWERF_ROOT.mkdir(parents=True, exist_ok=True)
    DATA_ROOT.mkdir(parents=True, exist_ok=True)
    if not DEK_FILE.exists():
        raw = secrets.token_bytes(32)
        encoded = base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")
        DEK_FILE.write_text(encoded + "\n")
        os.chmod(DEK_FILE, 0o600)


def _provision_user(space: str) -> dict[str, str]:
    """Direkt in auth.sqlite3 provisionieren -- kein Keyring, kein provision_user.py."""
    from authserver import passwords, totp
    from authserver.config import decode_data_encryption_key
    from authserver.secretbox import seal
    from authserver.store import AuthStore

    password = "wegwerf-c4c5-" + secrets.token_urlsafe(8)
    secret_b32 = totp.generate_secret()
    dek_raw = DEK_FILE.read_text().strip()
    dek = decode_data_encryption_key(dek_raw, origin=str(DEK_FILE))
    secret_enc = seal(secret_b32.encode("ascii"), key=dek, aad=space.encode("utf-8"))

    store = AuthStore(str(AUTH_DB), now_fn=lambda: datetime.now(timezone.utc))
    now = datetime.now(timezone.utc)
    store.upsert_user(
        space=space,
        password_hash=passwords.hash_password(password),
        totp_secret_enc=secret_enc,
        totp_alg="SHA1",
        totp_confirmed_at=now,
        status="active",
    )

    uri = totp.provisioning_uri(secret_b32, space=space, issuer="sharefyx", algo="SHA1")
    return {"space": space, "password": password, "otpauth_uri": uri}


def _seed_items(space: str, titles: list[tuple[str, str]]) -> None:
    env = os.environ.copy()
    env["SPACE_DATA_ROOT"] = str(DATA_ROOT)
    for title, kind in titles:
        subprocess.run(
            [".venv/bin/python", "phase1_storage/scripts/space_cli.py",
             "--data-root", str(DATA_ROOT),
             "create", space,
             "--type", kind, "--title", title],
            check=True, env=env, cwd=str(REPO_ROOT), stdout=subprocess.DEVNULL,
        )


def _create_foreign_space(space: str) -> None:
    """Legt einen zweiten Space `beta` an und gibt `alpha` Leserecht -- so erscheint
    `beta` in `alpha`s Overview als foreign (Kategoriepunkt foreign, slate) -- und
    ermoeglicht die Sichtpruefung der Space-Farblegende aus C3 im selben Lauf."""
    env = os.environ.copy()
    env["SPACE_DATA_ROOT"] = str(DATA_ROOT)
    subprocess.run(
        [".venv/bin/python", "phase6_shares/scripts/spacectl.py",
         "--data-root", str(DATA_ROOT),
         "create-space", space],
        check=True, env=env, cwd=str(REPO_ROOT), stdout=subprocess.DEVNULL,
    )
    subprocess.run(
        [".venv/bin/python", "phase6_shares/scripts/spacectl.py",
         "--data-root", str(DATA_ROOT),
         "add-member", "--read", space, OWN_SPACE],
        check=True, env=env, cwd=str(REPO_ROOT), stdout=subprocess.DEVNULL,
    )


def _serve_alive(pid: int) -> bool:
    return Path(f"/proc/{pid}").exists()


def cmd_setup(args: argparse.Namespace) -> int:
    _setup_root()
    _install_keyring()
    creds = _provision_user(OWN_SPACE)
    CREDS_FILE.write_text(json.dumps(creds, indent=2))
    os.chmod(CREDS_FILE, 0o600)
    sys.stderr.write(
        f"Wegwerf-Setup: root={WEGWERF_ROOT}, user={creds['space']}, "
        f"creds -> {CREDS_FILE}\n"
    )
    return 0


def cmd_seed_items(args: argparse.Namespace) -> int:
    _install_keyring()
    _create_foreign_space(FOREIGN_SPACE)
    _seed_items(OWN_SPACE, [
        ("Erste Notiz", "note"),
        ("Aufgabe fuer morgen", "task"),
        ("Bezug zu Phase 8", "note"),
        ("Logbuch Montag", "note"),
        ("Tagesnotizen", "note"),
    ])
    _seed_items(FOREIGN_SPACE, [
        ("Geteilte Notiz eins", "note"),
        ("Geteilte Notiz zwei", "note"),
    ])
    print(f"Items + Spaces angelegt (own={OWN_SPACE}, foreign={FOREIGN_SPACE}).")
    return 0


def cmd_start(args: argparse.Namespace) -> int:
    if SERVE_PID.exists():
        pid = int(SERVE_PID.read_text().strip())
        if _serve_alive(pid):
            print(f"Bereits aktiv (PID {pid}).")
            return 0
        SERVE_PID.unlink()

    env = os.environ.copy()
    env["SPACE_DATA_ROOT"] = str(DATA_ROOT)
    env["SPACE_AUTH_DB"] = str(AUTH_DB)
    env["SPACE_PUBLIC_BASE_URL"] = "https://wegwerf-c4c5.invalid"
    env["SPACE_PORT"] = str(PORT)
    env["CREDENTIALS_DIRECTORY"] = str(WEGWERF_ROOT)
    env["PYTHONPATH"] = str(REPO_ROOT)

    log = SERVE_LOG.open("ab")
    proc = subprocess.Popen(
        [".venv/bin/python", "phase2_mcp/scripts/serve.py",
         "--allowed-host", "127.0.0.1",
         "--allowed-host", "wegwerf-c4c5.invalid"],
        env=env, cwd=str(REPO_ROOT),
        stdout=log, stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    SERVE_PID.write_text(str(proc.pid))
    print(f"PID {proc.pid} -> {SERVE_PID}")

    base = f"http://127.0.0.1:{PORT}"
    for i in range(40):
        try:
            urllib.request.urlopen(f"{base}/health", timeout=1).read()
            print(f"Wegwerf-Server gesund nach {i*0.25:.1f}s.")
            return 0
        except Exception:
            time.sleep(0.25)
    print("Server wurde nicht gesund.", file=sys.stderr)
    return 1


def cmd_stop(args: argparse.Namespace) -> int:
    if not SERVE_PID.exists():
        print("Kein serve.pid -- nichts zu stoppen.")
        return 0
    pid = int(SERVE_PID.read_text().strip())
    if _serve_alive(pid):
        os.kill(pid, signal.SIGTERM)
        for _ in range(20):
            if not _serve_alive(pid):
                break
            time.sleep(0.25)
        if _serve_alive(pid):
            os.kill(pid, signal.SIGKILL)
            print(f"PID {pid} mit SIGKILL beendet.")
        else:
            print(f"PID {pid} sauber beendet.")
    SERVE_PID.unlink(missing_ok=True)
    return 0


def cmd_cleanup(args: argparse.Namespace) -> int:
    cmd_stop(args)
    import shutil
    if WEGWERF_ROOT.exists():
        shutil.rmtree(WEGWERF_ROOT)
        print(f"aufgeräumt: {WEGWERF_ROOT}")
    return 0


def cmd_health(args: argparse.Namespace) -> int:
    base = f"http://127.0.0.1:{PORT}"
    try:
        body = urllib.request.urlopen(f"{base}/health", timeout=2).read().decode()
        print(f"OK: {body}")
        return 0
    except Exception as e:
        print(f"FAIL: {e}", file=sys.stderr)
        return 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Wegwerf-Instanz Phase 8 C4+C5")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("setup")
    sub.add_parser("seed-items")
    sub.add_parser("start")
    sub.add_parser("stop")
    sub.add_parser("cleanup")
    sub.add_parser("health")
    args = parser.parse_args(argv)
    return {
        "setup": cmd_setup,
        "seed-items": cmd_seed_items,
        "start": cmd_start,
        "stop": cmd_stop,
        "cleanup": cmd_cleanup,
        "health": cmd_health,
    }[args.cmd](args)


if __name__ == "__main__":
    raise SystemExit(main())
