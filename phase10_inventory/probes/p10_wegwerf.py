#!/usr/bin/env python3
"""Wegwerf-Instanz für P10 Step 2 (M4/M5) — Plan §4: eigener Port **8799**, tmp-`DATA_ROOT`,
tmp-`auth.sqlite3`, Umgebung **ohne** `SHAREFYX_*`/`SFX_*`, Stopp nur über die PID-Datei
(Hard Rule 9: nie `pkill -f`, nie der systemd-Dienst).

Gebaut nach dem Muster von `phase8_5_picker_release/scripts/wegwerf_setup_v3ritt.py`
(File-Keyring-Backend statt `nikinger-space`, User direkt in `auth.sqlite3` provisioniert,
Cleanup per `kill -TERM $(cat serve.pid)`) und Technik 4 aus
`docs/concepts/sichtpruefung_automation_conventions.md`: **zwei Principals** (`alpha` und
`beta`, je eigenes Passwort + TOTP) — M5 (BG-2, P9-124 Konfliktkopie) braucht zwei
unabhängig einloggbare Identitäten, und keine bestehende Wegwerf-Vorlage hatte zwei.

Datenlage:
  - `alpha` — Home-Space von Principal A, ein paar Items (M4 braucht nur Zähler, M5 den
    Konfliktkandidaten: das Item, das A öffnet und bearbeitet, während B es ändert)
  - `beta` — Home-Space von Principal B, mit `.share.yml` `read: [alpha]` (A sieht den
    Space) und einem Item für den Konflikt
  - `gamma` — Team-Space mit `read:` + `write:` für `alpha` (M4-Gegenlauf: die
    „Spaces verwalten"-Liste zeigt alpha + gamma = 2 Zeilen; auch das Widen-Ziel
    für Re-Auth-Stationen in M5)

Konflikt-Item: `alpha`-Item „Konfliktkandidat" — A hat es im Editor offen, B ändert es
direkt über `store.update()` (Wegwerf-`DATA_ROOT`, kein Trick gegen Echtes), A speichert →
409 → Konflikt-Dialog → „Als neues Item anlegen".
"""
from __future__ import annotations

import argparse
import base64
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

REPO_ROOT = Path(__file__).resolve().parents[2]

WEGWERF_ROOT = Path("/tmp/opencode/sharefyx-wegwerf-p10")
DATA_ROOT = WEGWERF_ROOT / "data"
AUTH_DB = WEGWERF_ROOT / "auth.sqlite3"
KEYRING_FILE = WEGWERF_ROOT / "keyring.json"
DEK_FILE = WEGWERF_ROOT / "auth-dek"
CREDS_FILE = WEGWERF_ROOT / "credentials.json"
SERVE_PID = WEGWERF_ROOT / "serve.pid"
SERVE_LOG = WEGWERF_ROOT / "serve.log"
PORT = 8799  # Plan §4: P10-Wegwerf-Port

SPACE_A = "alpha"
SPACE_B = "beta"
SPACE_TEAM = "gamma"
CONFLICT_TITLE = "Konfliktkandidat"


class FileBackend(keyring.backend.KeyringBackend):
    """File-Keyring-Backend (dieselbe Kategorie wie in P6.5/7/8/8.5 — jede Phase ihr eigenes)."""

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


def _clean_env() -> dict[str, str]:
    """Umgebung ohne `SHAREFYX_*`/`SFX_*` (Plan §4, Memory „test harness never inherits env")
    — sonst würde eine z. B. in der Login-Shell stehende `SPACE_DATA_ROOT`-Zeile die
    Wegwerf-Instanz still gegen den echten DATA_ROOT laufen lassen."""
    env = os.environ.copy()
    for name in list(env):
        if name.startswith("SHAREFYX_") or name.startswith("SFX_"):
            env.pop(name)
    return env


def _setup_root() -> None:
    WEGWERF_ROOT.mkdir(parents=True, exist_ok=True)
    DATA_ROOT.mkdir(parents=True, exist_ok=True)
    if not DEK_FILE.exists():
        raw = secrets.token_bytes(32)
        encoded = base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")
        DEK_FILE.write_text(encoded + "\n")
        os.chmod(DEK_FILE, 0o600)


def _provision_user(space: str) -> dict[str, str]:
    """Direkt in auth.sqlite3 — Technik 4 (zwei Principals), einmal je Space aufgerufen."""
    from authserver import passwords, totp
    from authserver.config import decode_data_encryption_key
    from authserver.secretbox import seal
    from authserver.store import AuthStore

    password = "wegwerf-p10-" + secrets.token_urlsafe(8)
    secret_b32 = totp.generate_secret()
    dek = decode_data_encryption_key(DEK_FILE.read_text().strip(), origin=str(DEK_FILE))
    secret_enc = seal(secret_b32.encode("ascii"), key=dek, aad=space.encode("utf-8"))

    store = AuthStore(str(AUTH_DB), now_fn=lambda: datetime.now(timezone.utc))
    store.upsert_user(
        space=space,
        password_hash=passwords.hash_password(password),
        totp_secret_enc=secret_enc,
        totp_alg="SHA1",
        totp_confirmed_at=datetime.now(timezone.utc),
        status="active",
    )
    uri = totp.provisioning_uri(secret_b32, space=space, issuer="sharefyx", algo="SHA1")
    return {"space": space, "password": password, "otpauth_uri": uri}


def _spacectl(*args: str) -> None:
    env = _clean_env()
    env["SPACE_DATA_ROOT"] = str(DATA_ROOT)
    subprocess.run(
        [".venv/bin/python", "phase6_shares/scripts/spacectl.py",
         "--data-root", str(DATA_ROOT), *args],
        check=True, env=env, cwd=str(REPO_ROOT), stdout=subprocess.DEVNULL,
    )


def _seed_items() -> dict[str, object]:
    sys.path.insert(0, str(REPO_ROOT))
    from storage.store import Store

    # beta lesbar für alpha (B bleibt Home von B); gamma Team-Space mit Schreibrecht.
    # alpha zuerst anlegen, damit die add-member-Grants keinen fail-closed-Warnlauf
    # erzeugen (der Space muss bei der Grant-Zeit bekannt sein).
    _spacectl("create-space", SPACE_A)
    _spacectl("create-space", SPACE_B)
    _spacectl("add-member", "--read", SPACE_B, SPACE_A)
    _spacectl("create-space", SPACE_TEAM)
    _spacectl("add-member", "--write", SPACE_TEAM, SPACE_A)

    store = Store(str(DATA_ROOT), now_fn=lambda: datetime.now(timezone.utc), git=False)
    ids: dict[str, str] = {}
    plan = [
        (SPACE_A, CONFLICT_TITLE, "task", ["konflikt"], ""),
        (SPACE_A, "Alpha Notiz Eins", "note", ["bench"], "Notizen"),
        (SPACE_A, "Alpha Notiz Zwei", "note", ["bench"], "Notizen"),
        (SPACE_A, "Alpha Aufgabe offen", "task", ["bench"], ""),
        (SPACE_B, "Beta Notiz fuer den Konflikt", "note", ["bench"], ""),
        (SPACE_TEAM, "Team Aufgabe", "task", ["bench"], ""),
    ]
    for space, title, kind, tags, folder in plan:
        item = store.create(space, type=kind, title=title, tags=tags, folder=folder)
        ids[f"{space}:{title}"] = item.id
    store.rebuild_index()
    meta = {
        "ids": ids,
        "conflict_item": ids[f"{SPACE_A}:{CONFLICT_TITLE}"],
        "spaces": [SPACE_A, SPACE_B, SPACE_TEAM],
    }
    (WEGWERF_ROOT / "ids.json").write_text(json.dumps(meta, indent=2))
    return meta


def _serve_alive(pid: int) -> bool:
    return Path(f"/proc/{pid}").exists()


def cmd_setup(_args: argparse.Namespace) -> int:
    _setup_root()
    _install_keyring()
    creds = {"users": [_provision_user(SPACE_A), _provision_user(SPACE_B)]}
    CREDS_FILE.write_text(json.dumps(creds, indent=2))
    os.chmod(CREDS_FILE, 0o600)
    sys.stderr.write(
        f"Wegwerf-Setup: root={WEGWERF_ROOT}, users={[u['space'] for u in creds['users']]}, "
        f"creds -> {CREDS_FILE}\n"
    )
    return 0


def cmd_seed(_args: argparse.Namespace) -> int:
    _install_keyring()
    meta = _seed_items()
    print(f"Seed fertig: {meta['conflict_item']}")
    return 0


def cmd_start(_args: argparse.Namespace) -> int:
    if SERVE_PID.exists():
        pid = int(SERVE_PID.read_text().strip())
        if _serve_alive(pid):
            print(f"Bereits aktiv (PID {pid}).")
            return 0
        SERVE_PID.unlink()

    env = _clean_env()
    env["SPACE_DATA_ROOT"] = str(DATA_ROOT)
    env["SPACE_AUTH_DB"] = str(AUTH_DB)
    env["SPACE_PUBLIC_BASE_URL"] = "https://wegwerf-p10.invalid"
    env["SPACE_PORT"] = str(PORT)
    env["CREDENTIALS_DIRECTORY"] = str(WEGWERF_ROOT)
    env["PYTHONPATH"] = str(REPO_ROOT)

    log = SERVE_LOG.open("ab")
    proc = subprocess.Popen(
        [".venv/bin/python", "phase2_mcp/scripts/serve.py",
         "--allowed-host", "127.0.0.1",
         "--allowed-host", "wegwerf-p10.invalid"],
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
            print(f"Wegwerf-Server gesund nach {i * 0.25:.1f}s.")
            return 0
        except Exception:
            time.sleep(0.25)
    print("Server wurde nicht gesund.", file=sys.stderr)
    return 1


def cmd_stop(_args: argparse.Namespace) -> int:
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


def cmd_cleanup(_args: argparse.Namespace) -> int:
    cmd_stop(_args)
    import shutil
    if WEGWERF_ROOT.exists():
        shutil.rmtree(WEGWERF_ROOT)
        print(f"aufgeräumt: {WEGWERF_ROOT}")
    return 0


def cmd_health(_args: argparse.Namespace) -> int:
    base = f"http://127.0.0.1:{PORT}"
    try:
        body = urllib.request.urlopen(f"{base}/health", timeout=2).read().decode()
        print(f"OK: {body}")
        return 0
    except Exception as e:
        print(f"FAIL: {e}", file=sys.stderr)
        return 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Wegwerf-Instanz P10 (Port 8799, zwei Principals)")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("setup")
    sub.add_parser("seed")
    sub.add_parser("start")
    sub.add_parser("stop")
    sub.add_parser("cleanup")
    sub.add_parser("health")
    args = parser.parse_args(argv)
    return {
        "setup": cmd_setup,
        "seed": cmd_seed,
        "start": cmd_start,
        "stop": cmd_stop,
        "cleanup": cmd_cleanup,
        "health": cmd_health,
    }[args.cmd](args)


if __name__ == "__main__":
    raise SystemExit(main())
