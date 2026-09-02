#!/usr/bin/env python3
"""Phase 8 Sichtpruefung 2 -- Wegwerf-Instanz mit realistischen Daten.

30+ Items verteilt ueber 3 Spaces (1 eigener + 2 fremde-readable), gemischte Kategorien,
Frontmatter-Links, Body-Referenzen, gemeinsame Tags UND gemeinsamer Ordner -- damit der
Graph alle vier Kantenarten gleichzeitig zeigen kann (Frontmatter/Body/Tag/Ordner).

Eigener Port (18769, frisch -- 18765/18766/18767/18768 sind durch C3/D1/D2 belegt), File-
Keyring-Backend statt nikinger-space, User direkt in auth.sqlite3 provisioniert. Cleanup per
`kill -TERM $(cat serve.pid)` -- kein `pkill -f` (Hard Rule 9).

Items-Layout (12 alpha + 6 beta + 8 gamma = 26 Knoten, mit Folder- und Tag-Edges):
  alpha (eigener Space):
    Projekte/Backend/
      itm_a1  Auth-Service refactoren     tags:[backend, wichtig]  link: a3
      itm_a2  DB-Migration skript          tags:[backend, infra]    link: a1
      itm_a3  Logging standardisieren      tags:[backend]           link: a8
      itm_a4  Smoke-Tests ausbauen         tags:[backend, qa]      folder: Projekte/Backend
    Projekte/Frontend/
      itm_a5  Komponenten-Bibliothek       tags:[frontend, wichtig] link: a6
      itm_a6  Storybook einrichten         tags:[frontend, qa]      link: a5
      itm_a7  Styleguide pflegen            tags:[frontend, design]
    Projekte/
      itm_a8  Sprint-Planning               tags:[planung]           body-ref a3
      itm_a9  Retro-Notizen                 tags:[retro]             link: a8
    Notizen/
      itm_a10 Buecherliste Q4               tags:[lesen]             link: a11
      itm_a11 Empfehlungen Nikinger        tags:[lesen]             link: a10
    Logbuch/
      itm_a12 Tagesnotizen                 tags:[log]
  beta (fremd-readable, share_read von alpha):
    Notizen/
      itm_b1  Pair-Programming Erfahrungen  tags:[wissen, lesen]     link: a6
      itm_b2  Konferenz 2026                tags:[wissen]
    Projekte/
      itm_b3  Externe Bibliothek            tags:[frontend]          body-ref a5
      itm_b4  Design-Reviews                tags:[design, frontend]  link: b3
    Logbuch/
      itm_b5  Wochennotizen                 tags:[log]
      itm_b6  Geteilte Notizen              tags:[log, wissen]
  gamma (fremd-readable, share_read von alpha):
    Projekte/Backend/
      itm_g1  Performance-Audit             tags:[backend, infra]    link: a1
      itm_g2  Cache-Strategie               tags:[backend, infra]
      itm_g3  DB-Indizes                    tags:[backend]
    Notizen/
      itm_g4  IT-Sekus Meeting              tags:[meeting]           link: a9
      itm_g5  Beschluesse                   tags:[meeting, planung]  link: g4
    Projekte/Frontend/
      itm_g6  Performance-Optimierungen     tags:[frontend]          link: a5
    Logbuch/
      itm_g7  Infra-Incidents               tags:[log, infra]
      itm_g8  Monitoring-Setup              tags:[infra]

Damit entstehen:
  - explizite Frontmatter-Kanten: 14 (alle --link-Eintraege)
  - explizite Body-Kanten: 2 (a8 -> a3, b3 -> a5)
  - Tag-Edges (mit Toggle): mehrere Cluster -- backend (5), frontend (5), log (5), lesen (3), planung (2), infra (5), meeting (2), design (2), wissen (3), wichtig (2), qa (2)
  - Ordner-Edges (mit Toggle): Alpha/Projekte/Backend (4 Knoten), Alpha/Projekte/Frontend (3), Alpha/Projekte (2), Alpha/Notizen (2), Alpha/Logbuch (1), Beta/Notizen (2), Beta/Projekte (2), Beta/Logbuch (2), Gamma/Projekte/Backend (3), Gamma/Notizen (2), Gamma/Projekte/Frontend (1), Gamma/Logbuch (2) -- jeweils 4+3+1=8 Paare etc.

Das reicht fuer eine echte Sichtpruefung: Cluster sollten sich klar trennen, Toggles
messenbar mehr Kanten erzeugen, Knoten-Klick oeffnet das Item.
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

WEGWERF_ROOT = Path("/tmp/opencode/sharefyx-wegwerf-sichtpruefung2")
DATA_ROOT = WEGWERF_ROOT / "data"
AUTH_DB = WEGWERF_ROOT / "auth.sqlite3"
KEYRING_FILE = WEGWERF_ROOT / "keyring.json"
DEK_FILE = WEGWERF_ROOT / "auth-dek"
CREDS_FILE = WEGWERF_ROOT / "credentials.json"
SERVE_PID = WEGWERF_ROOT / "serve.pid"
SERVE_LOG = WEGWERF_ROOT / "serve.log"
PORT = 18769
OWN_SPACE = "alpha"
FOREIGN_SPACES = ["beta", "gamma"]

REPO_ROOT = Path(__file__).resolve().parents[2]


class FileBackend(keyring.backend.KeyringBackend):
    """File-Keyring-Backend (C3/D1/D2)."""

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

    password = "wegwerf-sp2-" + secrets.token_urlsafe(8)
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


# Item-Konfiguration: (space, title, type, tags, folder, body_ref_id_or_None, link_id_or_None)
ALPHA_ITEMS = [
    # Projekte/Backend
    ("alpha", "Auth-Service refactoren",   "task", ["backend", "wichtig"], "Projekte/Backend", None, "a3"),
    ("alpha", "DB-Migration skript",        "task", ["backend", "infra"],   "Projekte/Backend", None, "a1"),
    ("alpha", "Logging standardisieren",    "task", ["backend"],            "Projekte/Backend", None, "a8"),
    ("alpha", "Smoke-Tests ausbauen",       "task", ["backend", "qa"],       "Projekte/Backend", None, None),
    # Projekte/Frontend
    ("alpha", "Komponenten-Bibliothek",     "note", ["frontend", "wichtig"], "Projekte/Frontend", None, "a6"),
    ("alpha", "Storybook einrichten",       "task", ["frontend", "qa"],      "Projekte/Frontend", None, "a5"),
    ("alpha", "Styleguide pflegen",         "note", ["frontend", "design"],  "Projekte/Frontend", None, None),
    # Projekte (direkt unter Projekte, nicht in einem Unterordner)
    ("alpha", "Sprint-Planning",            "note", ["planung"],             "Projekte",          "a3",  "a9"),
    ("alpha", "Retro-Notizen",              "note", ["retro"],               "Projekte",          None,  "a8"),
    # Notizen
    ("alpha", "Buecherliste Q4",            "note", ["lesen"],               "Notizen",           None,  "a11"),
    ("alpha", "Empfehlungen Nikinger",      "note", ["lesen"],               "Notizen",           None,  "a10"),
    # Logbuch
    ("alpha", "Tagesnotizen",               "note", ["log"],                 "Logbuch",           None,  None),
]
BETA_ITEMS = [
    ("beta", "Pair-Programming Erfahrungen", "note", ["wissen", "lesen"],    "Notizen",       None, "a6"),
    ("beta", "Konferenz 2026",               "note", ["wissen"],             "Notizen",       None, None),
    ("beta", "Externe Bibliothek",           "note", ["frontend"],           "Projekte",      "a5", None),
    ("beta", "Design-Reviews",               "note", ["design", "frontend"], "Projekte",      None, "b3"),
    ("beta", "Wochennotizen",                "note", ["log"],                "Logbuch",       None, None),
    ("beta", "Geteilte Notizen",             "note", ["log", "wissen"],      "Logbuch",       None, None),
]
GAMMA_ITEMS = [
    ("gamma", "Performance-Audit",          "task", ["backend", "infra"], "Projekte/Backend",  None, "a1"),
    ("gamma", "Cache-Strategie",            "task", ["backend", "infra"], "Projekte/Backend",  None, None),
    ("gamma", "DB-Indizes",                  "task", ["backend"],          "Projekte/Backend",  None, None),
    ("gamma", "IT-Sekus Meeting",            "note", ["meeting"],          "Notizen",           None, "a9"),
    ("gamma", "Beschluesse",                 "note", ["meeting", "planung"], "Notizen",        None, "g4"),
    ("gamma", "Performance-Optimierungen",   "task", ["frontend"],         "Projekte/Frontend", None, "a5"),
    ("gamma", "Infra-Incidents",             "note", ["log", "infra"],     "Logbuch",           None, None),
    ("gamma", "Monitoring-Setup",            "note", ["infra"],            "Logbuch",           None, None),
]


def _seed_items() -> dict[str, str]:
    """Legt alle Items ueber die Store-API direkt an (folder-faehig), dann Frontmatter-Links."""
    sys.path.insert(0, str(REPO_ROOT))
    from storage.store import Store
    from storage.index import INDEX_SCHEMA_VERSION  # type: ignore

    store = Store(str(DATA_ROOT), now_fn=lambda: datetime.now(timezone.utc))
    ids: dict[str, str] = {}

    def _add(space: str, title: str, kind: str, tags: list[str], folder: str) -> str:
        item = store.create(space, type=kind, title=title, tags=tags, folder=folder)
        return item.id

    for space, title, kind, tags, folder, _body_ref, _link in ALPHA_ITEMS:
        ids[f"{space}:{title}"] = _add(space, title, kind, tags, folder)

    for space, title, kind, tags, folder, _body_ref, _link in BETA_ITEMS:
        ids[f"{space}:{title}"] = _add(space, title, kind, tags, folder)

    for space, title, kind, tags, folder, _body_ref, _link in GAMMA_ITEMS:
        ids[f"{space}:{title}"] = _add(space, title, kind, tags, folder)

    # Body-Referenzen (zwei Stueck) -- wir patchen den Body via store.update
    def _patch_body(space: str, title: str, target_key: str) -> None:
        item_id = ids[f"{space}:{title}"]
        ref_id = ids[target_key]
        body = (f"Siehe Notiz {ref_id} fuer mehr Kontext.")
        # Aktuelle Version lesen
        current = store.get(item_id)
        store.update(item_id, version=current.version, body=body)

    _patch_body("alpha", "Sprint-Planning",       "alpha:Logging standardisieren")
    _patch_body("beta",  "Externe Bibliothek",   "alpha:Komponenten-Bibliothek")

    # Frontmatter-Links -- map von Kurz-IDs (a3, b3, g4) auf vollstaendige "space:title"-Keys.
    # Wir muessen ZUERST alle Items anlegen (ist oben schon passiert), DANN die Links setzen
    # (sonst kennen wir die Ziel-IDs noch nicht).
    link_targets = {
        # Alpha-Items, die von anderen referenziert werden
        "a1":  "alpha:Auth-Service refactoren",
        "a3":  "alpha:Logging standardisieren",
        "a5":  "alpha:Komponenten-Bibliothek",
        "a6":  "alpha:Storybook einrichten",
        "a8":  "alpha:Sprint-Planning",
        "a9":  "alpha:Retro-Notizen",
        "a10": "alpha:Empfehlungen Nikinger",
        "a11": "alpha:Buecherliste Q4",
        # Beta-Items
        "b3":  "beta:Externe Bibliothek",
        # Gamma-Items
        "g4":  "gamma:IT-Sekus Meeting",
    }

    def _set_link(space: str, title: str, target_key: str) -> None:
        item_id = ids[f"{space}:{title}"]
        target_id = ids[target_key]
        current = store.get(item_id)
        store.update(item_id, version=current.version, links=[target_id])

    for space, title, _kind, _tags, _folder, _body, link in ALPHA_ITEMS + BETA_ITEMS + GAMMA_ITEMS:
        if link is None:
            continue
        target_key = link_targets.get(link)
        if target_key is None:
            raise ValueError(f"Unknown link target '{link}' in {space}:{title}")
        _set_link(space, title, target_key)

    # Reindex (Hard Rule 2)
    store.rebuild_index()
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
    # Erst die fremden Spaces anlegen -- create_space() kommt vor dem ersten Item darin.
    for name in FOREIGN_SPACES:
        _create_foreign_space(name)
    # Dann die Items ueber die Store-API (mit folder-Support, den space_cli nicht hat).
    ids = _seed_items()
    (WEGWERF_ROOT / "ids.json").write_text(json.dumps(ids, indent=2))
    print(f"Items angelegt: {len(ids)} insgesamt (alpha={len(ALPHA_ITEMS)}, "
          f"beta={len(BETA_ITEMS)}, gamma={len(GAMMA_ITEMS)}). "
          f"IDs nach {WEGWERF_ROOT / 'ids.json'}.")
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
    env["SPACE_PUBLIC_BASE_URL"] = "https://wegwerf-sp2.invalid"
    env["SPACE_PORT"] = str(PORT)
    env["CREDENTIALS_DIRECTORY"] = str(WEGWERF_ROOT)
    env["PYTHONPATH"] = str(REPO_ROOT)

    log = SERVE_LOG.open("ab")
    proc = subprocess.Popen(
        [".venv/bin/python", "phase2_mcp/scripts/serve.py",
         "--allowed-host", "127.0.0.1",
         "--allowed-host", "wegwerf-sp2.invalid"],
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
    parser = argparse.ArgumentParser(description="Wegwerf-Instanz Sichtpruefung 2")
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
