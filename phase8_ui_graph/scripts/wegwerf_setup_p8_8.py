#!/usr/bin/env python3
"""Phase 8 P8-8 -- Wegwerf-Instanz mit ZWEI echten, unabhaengigen Principals.

Alle bisherigen Wegwerf-Setups (`wegwerf_setup_d2.py`, `_200knoten.py`, etc.) provisionieren
genau EINEN loggbaren Nutzer; weitere "Spaces" wie `beta`/`gamma` sind nur Ziele mit
`add-member`-Freigabe, keine eigenen Accounts. P8-8 ("nicht-lesbares Item weder als Knoten noch
als Kantenende, Zweitnutzer") braucht aber zwei EIGENSTAENDIGE, unabhaengig einloggbare
Identitaeten -- genau wie die reale Nikinger/Fabian-Konstellation, nur synthetisch. Dieses
Setup provisioniert `testuser1` UND `testuser2` (zwei `_provision_user()`-Aufrufe statt einem)
und legt zwei Items unter `testuser1` an: eines bleibt privat, eines wird vom Probe-Skript zur
Laufzeit per `update_item(share_read=["testuser2"])` freigegeben (Sharing ist ein Feld, das nur
ueber die MCP-`update_item`/Webui-API gesetzt wird, `space_cli.py` kennt es nicht -- deshalb
hier NICHT im Setup, sondern im Probe-Skript, wo ohnehin ein echter authentifizierter
`update_item`-Aufruf laeuft).

Standing-Permission-Rahmen: eigener Port, tmp `DATA_ROOT`/`auth.sqlite3`/File-Keyring, kein
Service-Touch, kein `pkill -f`.
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
import keyring.compat

WEGWERF_ROOT = Path("/tmp/opencode/sharefyx-wegwerf-p8-8")
DATA_ROOT = WEGWERF_ROOT / "data"
AUTH_DB = WEGWERF_ROOT / "auth.sqlite3"
KEYRING_FILE = WEGWERF_ROOT / "keyring.json"
DEK_FILE = WEGWERF_ROOT / "auth-dek"
CREDS_FILE = WEGWERF_ROOT / "credentials.json"
IDS_FILE = WEGWERF_ROOT / "ids.json"
SERVE_PID = WEGWERF_ROOT / "serve.pid"
SERVE_LOG = WEGWERF_ROOT / "serve.log"
PORT = 18780
USER_A = "testuser1"
USER_B = "testuser2"

REPO_ROOT = Path(__file__).resolve().parents[2]


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
    from authserver import passwords, totp
    from authserver.config import decode_data_encryption_key
    from authserver.secretbox import seal
    from authserver.store import AuthStore

    password = "wegwerf-p88-" + secrets.token_urlsafe(8)
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


def _run_cli_json(*args: str) -> dict:
    env = os.environ.copy()
    env["SPACE_DATA_ROOT"] = str(DATA_ROOT)
    proc = subprocess.run(
        [".venv/bin/python", "phase1_storage/scripts/space_cli.py",
         "--data-root", str(DATA_ROOT), *args, "--json"],
        check=True, env=env, cwd=str(REPO_ROOT),
        stdout=subprocess.PIPE, text=True,
    )
    return json.loads(proc.stdout)


def _run_cli(*args: str) -> None:
    env = os.environ.copy()
    env["SPACE_DATA_ROOT"] = str(DATA_ROOT)
    subprocess.run(
        [".venv/bin/python", "phase1_storage/scripts/space_cli.py",
         "--data-root", str(DATA_ROOT), *args],
        check=True, env=env, cwd=str(REPO_ROOT), stdout=subprocess.DEVNULL,
    )


def _seed_items() -> dict[str, str]:
    ids: dict[str, str] = {}
    private = _run_cli_json(
        "create", USER_A, "--type", "note", "--title", "Private Notiz testuser1",
    )
    ids["private"] = private["id"]
    shared = _run_cli_json(
        "create", USER_A, "--type", "note", "--title", "Geteilte Notiz testuser1 -> testuser2",
    )
    ids["shared"] = shared["id"]
    _run_cli("reindex")

    # `share_read`/`share_write` sind ueber KEIN MCP-Tool setzbar (tools.py :: update_item()
    # weist das explizit ab, "das geht nur ein Mensch in der UI") -- die MCP-Restriktion sitzt
    # in der Tool-Schicht, nicht im Storage-Kern. Direkter `Store.update()`-Aufruf hier ist
    # Fixture-Setup auf der eigenen Wegwerf-DATA_ROOT, keine Umgehung von irgendetwas Echtem.
    import sys
    sys.path.insert(0, str(REPO_ROOT))
    from storage.store import Store

    store = Store(str(DATA_ROOT))
    store.update(ids["shared"], version=1, share_read=[USER_B])

    return ids


def _serve_alive(pid: int) -> bool:
    return Path(f"/proc/{pid}").exists()


def cmd_setup(args: argparse.Namespace) -> int:
    _setup_root()
    _install_keyring()
    creds_a = _provision_user(USER_A)
    creds_b = _provision_user(USER_B)
    CREDS_FILE.write_text(json.dumps({USER_A: creds_a, USER_B: creds_b}, indent=2))
    os.chmod(CREDS_FILE, 0o600)
    sys.stderr.write(
        f"Wegwerf-Setup: root={WEGWERF_ROOT}, users={USER_A}+{USER_B}, creds -> {CREDS_FILE}\n"
    )
    return 0


def cmd_seed_items(args: argparse.Namespace) -> int:
    _install_keyring()
    ids = _seed_items()
    IDS_FILE.write_text(json.dumps(ids, indent=2))
    print(f"Items angelegt: {ids}")
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
    env["SPACE_PUBLIC_BASE_URL"] = "https://wegwerf-p8-8.invalid"
    env["SPACE_PORT"] = str(PORT)
    env["CREDENTIALS_DIRECTORY"] = str(WEGWERF_ROOT)
    env["PYTHONPATH"] = str(REPO_ROOT)

    log = SERVE_LOG.open("ab")
    proc = subprocess.Popen(
        [".venv/bin/python", "phase2_mcp/scripts/serve.py",
         "--allowed-host", "127.0.0.1",
         "--allowed-host", "wegwerf-p8-8.invalid"],
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Wegwerf-Instanz P8-8 (zwei Principals)")
    sub = parser.add_subparsers(dest="cmd", required=True)
    for name in ("setup", "seed-items", "start", "stop", "cleanup"):
        sub.add_parser(name)
    args = parser.parse_args(argv)
    return {
        "setup": cmd_setup,
        "seed-items": cmd_seed_items,
        "start": cmd_start,
        "stop": cmd_stop,
        "cleanup": cmd_cleanup,
    }[args.cmd](args)


if __name__ == "__main__":
    raise SystemExit(main())
