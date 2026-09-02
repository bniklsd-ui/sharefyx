#!/usr/bin/env python3
"""Phase 8 D2 -- Wegwerf-Instanz aufsetzen, starten, stoppen, aufraeumen.

Erbt alles vom D1-Setup (eigener Port, File-Keyring-Backend, User-Provisionierung in
auth.sqlite3, Stand-Alone-Cleanup ohne `pkill -f`). Erweitert die Datenlage so, dass der
Graph sinnvoll aussieht: explizite Kanten ueber Frontmatter-`links:` UND `itm_…`-Body-
Referenzen, gemeinsame Tags (fuer das Toggle), gemeinsamer Ordner (fuer das andere Toggle).

Items-Layout (10 alpha + 4 beta = 14 Knoten):
  alpha:
    itm_alpha_1 Erste Notiz             tags: [phase, intro]      link: itm_alpha_3
    itm_alpha_2 Zweite Notiz            tags: [intro]              body: itm_alpha_1
    itm_alpha_3 Bezug zu Phase 8        tags: [phase, wichtig]    link: itm_alpha_1
    itm_alpha_4 Aufgabe fuer morgen     tags: [wichtig]            folder: Projekte
    itm_alpha_5 Aufgabe spaeter         tags: [phase]             folder: Projekte
    itm_alpha_6 Geteilte Notiz eins     tags: [extern]            link: itm_beta_1
    itm_alpha_7 Geteilte Notiz zwei     tags: [extern]            link: itm_beta_2
    itm_alpha_8 Logbuch                 tags: [log]
    itm_alpha_9 Meeting Notizen         tags: [meeting]           folder: Projekte
    itm_alpha_10 Tagebuch               tags: [log, intro]
  beta:
    itm_beta_1 Beta Notiz eins          tags: [extern]            link: itm_alpha_7
    itm_beta_2 Beta Notiz zwei          tags: [extern]            body: itm_alpha_6
    itm_beta_3 Beta Aufgabe             tags: [extern, wichtig]
    itm_beta_4 Beta Log                 tags: [log]

Damit entstehen (ohne Toggles):
  - explizite Frontmatter-Kanten: alpha_1<->alpha_3, alpha_6<->beta_1, alpha_7<->beta_1,
    alpha_7<->beta_2
  - explizite Body-Kanten: alpha_2 -> alpha_1, beta_2 -> alpha_6

Mit Toggle "Tags" (Limit 15 nicht relevant bei <11 Knoten/Tag):
  - Tag "intro": alpha_1, alpha_2, alpha_10
  - Tag "phase": alpha_1, alpha_3, alpha_5
  - Tag "wichtig": alpha_3, alpha_4, beta_3
  - Tag "extern": alpha_6, alpha_7, beta_1, beta_2, beta_3, beta_4
  - Tag "log": alpha_8, alpha_10, beta_4

Mit Toggle "Ordner" (alpha/Projekte):
  - alpha_4, alpha_5, alpha_9

Wegwerf-Beleg nicht so umfangreich wie eine echte Sichtpruefung -- der Smoke-Lauf prueft
strukturell: Knoten gezeichnet, Kanten gezeichnet (explizit/Tags/Ordner), Knoten-Klick
oeffnet das Item, Leerzustand ist erreichbar (durch Deaktivieren des /graph-Endpoints --
nicht noetig, der Default ist 'so viel wie der Server liefert'). Phase 8 Sichtpruefung 2
macht die echte Sichtpruefung gegen einen realistischeren Datensatz, nicht diese Wegwerf.
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

WEGWERF_ROOT = Path("/tmp/opencode/sharefyx-wegwerf-d2")
DATA_ROOT = WEGWERF_ROOT / "data"
AUTH_DB = WEGWERF_ROOT / "auth.sqlite3"
KEYRING_FILE = WEGWERF_ROOT / "keyring.json"
DEK_FILE = WEGWERF_ROOT / "auth-dek"
CREDS_FILE = WEGWERF_ROOT / "credentials.json"
SERVE_PID = WEGWERF_ROOT / "serve.pid"
SERVE_LOG = WEGWERF_ROOT / "serve.log"
PORT = 18768
OWN_SPACE = "alpha"
FOREIGN_SPACE = "beta"

REPO_ROOT = Path(__file__).resolve().parents[2]


class FileBackend(keyring.backend.KeyringBackend):
    """File-Keyring-Backend (siehe wegwerf_setup_c3.py / d1)."""

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

    password = "wegwerf-d2-" + secrets.token_urlsafe(8)
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


# Item-Konfiguration: Reihenfolge bestimmt die IDs (space_cli vergibt sie fortlaufend).
# Wir legen alle Items erstmal ohne Links an, sammeln die IDs, dann ein zweiter Pass fuer
# die Frontmatter-Links.
# Bewusst OHNE --folder: space_cli unterstuetzt kein --folder auf `create`, und ein
# expliziter Move wuerde zwei Versionen pro Item bedeuten (create=1, move=2), was die
# Smoke-Assertions verraet. Folder-Edges bleiben damit fuer Phase-8-Sichtpruefung 2
# uebrig (groesserer Datensatz, manuelle Pruefung), nicht fuer den Smoke.
ALPHA_ITEMS = [
    # (title, type, tags, link_id_offset_to_other_alpha)
    ("Erste Notiz",          "note", ["phase", "intro"],     None),
    ("Zweite Notiz",         "note", ["intro"],              None),  # body_ref -> alpha_1
    ("Bezug zu Phase 8",     "note", ["phase", "wichtig"],   "itm_alpha_1"),
    ("Aufgabe fuer morgen",  "task", ["wichtig"],            None),
    ("Aufgabe spaeter",      "task", ["phase"],              None),
    ("Geteilte Notiz eins",  "note", ["extern"],             "itm_beta_1"),
    ("Geteilte Notiz zwei",  "note", ["extern"],             "itm_beta_2"),
    ("Logbuch",              "note", ["log"],                None),
    ("Meeting Notizen",      "note", ["meeting"],            None),
    ("Tagebuch",             "note", ["log", "intro"],       None),
]
BETA_ITEMS = [
    ("Beta Notiz eins",      "note", ["extern"],              "itm_alpha_7"),
    ("Beta Notiz zwei",      "note", ["extern"],              None),  # body_ref -> alpha_6
    ("Beta Aufgabe",         "task", ["extern", "wichtig"],   None),
    ("Beta Log",             "note", ["log"],                 None),
]


def _run_cli(*args: str) -> None:
    env = os.environ.copy()
    env["SPACE_DATA_ROOT"] = str(DATA_ROOT)
    subprocess.run(
        [".venv/bin/python", "phase1_storage/scripts/space_cli.py",
         "--data-root", str(DATA_ROOT), *args],
        check=True, env=env, cwd=str(REPO_ROOT), stdout=subprocess.DEVNULL,
    )


def _run_cli_json(*args: str) -> dict:
    """`--json` muss nach dem Subcommand-Positional stehen (bei `create` nach `space`,
    bei `update` nach `item_id`). Wir haengen es hier ans Ende -- Aufrufer muessen die
    Positional-Argumente entsprechend setzen."""
    env = os.environ.copy()
    env["SPACE_DATA_ROOT"] = str(DATA_ROOT)
    proc = subprocess.run(
        [".venv/bin/python", "phase1_storage/scripts/space_cli.py",
         "--data-root", str(DATA_ROOT), *args, "--json"],
        check=True, env=env, cwd=str(REPO_ROOT),
        stdout=subprocess.PIPE, text=True,
    )
    return json.loads(proc.stdout)


def _create_foreign_space(name: str) -> None:
    env = os.environ.copy()
    env["SPACE_DATA_ROOT"] = str(DATA_ROOT)
    subprocess.run(
        [".venv/bin/python", "phase6_shares/scripts/spacectl.py",
         "--data-root", str(DATA_ROOT), "create-space", name],
        check=True, env=env, cwd=str(REPO_ROOT), stdout=subprocess.DEVNULL,
    )
    subprocess.run(
        [".venv/bin/python", "phase6_shares/scripts/spacectl.py",
         "--data-root", str(DATA_ROOT), "add-member", "--read", name, OWN_SPACE],
        check=True, env=env, cwd=str(REPO_ROOT), stdout=subprocess.DEVNULL,
    )


def _seed_items() -> dict[str, str]:
    """Legt alle Items an, sammelt die IDs nach space+title-Key."""
    ids: dict[str, str] = {}

    for title, kind, tags, _link in ALPHA_ITEMS:
        args = ["create", OWN_SPACE, "--type", kind, "--title", title,
                "--tag", ",".join(tags)]
        out = _run_cli_json(*args)
        ids["alpha:" + title] = out["id"]

    for title, kind, tags, _link in BETA_ITEMS:
        args = ["create", FOREIGN_SPACE, "--type", kind, "--title", title,
                "--tag", ",".join(tags)]
        out = _run_cli_json(*args)
        ids["beta:" + title] = out["id"]

    # Pass 2: Body-Referenzen + Frontmatter-Links.
    # Body-Referenzen: einfach die itm_…-ID in den Body schreiben.
    if True:
        ref_id = ids["alpha:Erste Notiz"]
        body = ("Siehe Notiz " + ref_id + " fuer mehr Kontext.")
        _run_cli("update", ids["alpha:Zweite Notiz"], "--version", "1", "--body", body)

    ref_id = ids["alpha:Geteilte Notiz eins"]
    body = ("Querverweis: " + ref_id)
    _run_cli("update", ids["beta:Beta Notiz zwei"], "--version", "1", "--body", body)

    # Frontmatter-Links: per --link item_id
    for title, _kind, _tags, link in ALPHA_ITEMS:
        if link is None:
            continue
        if link.startswith("itm_beta_"):
            target_name = {"itm_beta_1": "Beta Notiz eins", "itm_beta_2": "Beta Notiz zwei"}[link]
            target_id = ids["beta:" + target_name]
        else:
            target_id = ids["alpha:" + {
                "itm_alpha_1": "Erste Notiz",
                "itm_alpha_3": "Bezug zu Phase 8",
            }[link]]
        _run_cli("update", ids["alpha:" + title], "--version", "1", "--link", target_id)

    for title, _kind, _tags, link in BETA_ITEMS:
        if link is None:
            continue
        target_id = ids["alpha:" + {"itm_alpha_7": "Geteilte Notiz zwei"}[link]]
        _run_cli("update", ids["beta:" + title], "--version", "1", "--link", target_id)

    # Reindex, damit die item_links-Tabelle fuer die Graph-Endpoint-Query konsistent ist
    # (Hard Rule 2: Index jederzeit aus Files rekonstruierbar).
    _run_cli("reindex")

    return ids


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
    ids = _seed_items()
    # IDs nachschreiben -- nuetzlich fuer den Smoke-Lauf, falls er sie braucht.
    (WEGWERF_ROOT / "ids.json").write_text(json.dumps(ids, indent=2))
    print(f"Items angelegt: {len(ids)} insgesamt (alpha={len(ALPHA_ITEMS)}, "
          f"beta={len(BETA_ITEMS)}). IDs nach {WEGWERF_ROOT / 'ids.json'}.")
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
    env["SPACE_PUBLIC_BASE_URL"] = "https://wegwerf-d2.invalid"
    env["SPACE_PORT"] = str(PORT)
    env["CREDENTIALS_DIRECTORY"] = str(WEGWERF_ROOT)
    env["PYTHONPATH"] = str(REPO_ROOT)

    log = SERVE_LOG.open("ab")
    proc = subprocess.Popen(
        [".venv/bin/python", "phase2_mcp/scripts/serve.py",
         "--allowed-host", "127.0.0.1",
         "--allowed-host", "wegwerf-d2.invalid"],
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
    parser = argparse.ArgumentParser(description="Wegwerf-Instanz D2")
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
