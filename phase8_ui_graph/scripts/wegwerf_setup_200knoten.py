#!/usr/bin/env python3
"""Phase 8 P8-22 -- Wegwerf-Instanz mit 200 Knoten fuer den Graph-Lastfall.

Abnahmezeile P8-22 (Plan §7): "200-Knoten-Wegwerf-Datensatz: Simulation kommt < 3 s zur Ruhe,
Interaktion ohne Hakeln; `prefers-reduced-motion` rendert statisch." Die bisherigen
Graph-Wegwerf-Instanzen sind zu klein dafuer (D2 = 14 Knoten, Sichtpruefung 2 = 26 Knoten) --
dieses Setup ist der Datensatz, gegen den `p8_22_smoke.py` messen kann.

Eigener Port (18772 -- 18765/18766 = C3, 18767 = D1, 18768 = D2, 18769 = Sichtpruefung 2,
18770 = C4/C5, 18771 = Auswahl/Chevron), File-Keyring-Backend statt `nikinger-space`, User
direkt in einer eigenen `auth.sqlite3` provisioniert, Stopp ueber die PID-Datei (Hard Rule 9 --
niemals `pkill -f` mit Regex).

**Datenlage (deterministisch generiert, kein Zufall -- die Messung soll reproduzierbar sein):**

| Space | Kategorie (`spaceCategory()`) | Items |
|---|---|---|
| `alpha` | own (Home-Space des Logins) | 120 |
| `beta`  | shared (Mitglied mit `--write`) | 50 |
| `gamma` | foreign (Mitglied mit `--read`) | 30 |

Zusammen **200 Knoten** -- alle drei Farbkategorien aus C3 gleichzeitig im Bild.

- **Explizite Kanten:** jedes Item traegt genau einen Frontmatter-`links:`-Eintrag auf das
  Item `(i + 7) % 200` der globalen Anlege-Reihenfolge. Das ergibt 200 gerichtete Kanten in
  einem einzigen Ring der Laenge 200 (ggT(7, 200) = 1) -- also einen zusammenhaengenden
  Graphen ohne isolierte Inseln, gut fuer den Lastfall und dennoch keine Clique.
- **Tag-Kanten (Toggle "Tags"):** drei Sorten bewusst gemischt, damit der >15-Knoten-Riegel
  (`TAG_CLIQUE_LIMIT = 15` in `js/graph.js`, P8-21) empirisch pruefbar wird:
  `last-200` liegt auf **allen 200** Knoten (muss uebersprungen werden, sonst waeren es
  19 900 Kanten), `gruppe-NN` auf je ~16-17 Knoten (12 Gruppen -- knapp ueber dem Riegel,
  ebenfalls uebersprungen), `spitze` auf genau **5** Knoten (10 Paare, muss durchkommen).
- **Ordner-Kanten (Toggle "Ordner"):** vier Ordner in `alpha`, zwei in `beta`, zwei in
  `gamma`, plus Items in der Space-Wurzel (`folder == ""`, erzeugen laut `buildFolderEdges()`
  bewusst keine Kante).

**Was dieses Setup NICHT ist:** keine realistische Notizsammlung (die Titel sind generiert,
die Bodies leer bis auf die Body-Referenz-Handvoll) -- das ist Sichtpruefung 2s Aufgabe
(`wegwerf_setup_sichtpruefung2.py`). Hier zaehlt ausschliesslich die Knotenzahl.

Aufrufreihenfolge:
    setup -> seed-items -> start -> (p8_22_smoke.py) -> cleanup
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

WEGWERF_ROOT = Path("/tmp/opencode/sharefyx-wegwerf-200knoten")
DATA_ROOT = WEGWERF_ROOT / "data"
AUTH_DB = WEGWERF_ROOT / "auth.sqlite3"
KEYRING_FILE = WEGWERF_ROOT / "keyring.json"
DEK_FILE = WEGWERF_ROOT / "auth-dek"
CREDS_FILE = WEGWERF_ROOT / "credentials.json"
SERVE_PID = WEGWERF_ROOT / "serve.pid"
SERVE_LOG = WEGWERF_ROOT / "serve.log"
PORT = 18772
OWN_SPACE = "alpha"
SHARED_SPACE = "beta"
FOREIGN_SPACE = "gamma"

# Verteilung der 200 Knoten (Summe muss 200 sein -- eine Assertion haelt das fest).
COUNTS = {OWN_SPACE: 120, SHARED_SPACE: 50, FOREIGN_SPACE: 30}
TOTAL_NODES = 200
LINK_STRIDE = 7          # ggT(7, 200) = 1 -> ein einziger Ring ueber alle 200 Knoten
SPITZE_TAG_SIZE = 5      # <= TAG_CLIQUE_LIMIT (15) -- muss Tag-Kanten erzeugen
TAG_GROUPS = 12          # 200/12 ~ 16-17 Knoten pro Gruppe -> ueber dem Riegel
BODY_REF_COUNT = 6       # Handvoll Body-Referenzen zusaetzlich zu den Frontmatter-Links

FOLDERS = {
    OWN_SPACE: ["Projekte/Backend", "Projekte/Frontend", "Notizen", "Logbuch", ""],
    SHARED_SPACE: ["Projekte", "Notizen", ""],
    FOREIGN_SPACE: ["Logbuch", ""],
}

REPO_ROOT = Path(__file__).resolve().parents[2]


class FileBackend(keyring.backend.KeyringBackend):
    """File-Keyring-Backend (identisch zu C3/D1/D2/Sichtpruefung 2)."""

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

    password = "wegwerf-200k-" + secrets.token_urlsafe(8)
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


def _create_member_space(name: str, mode: str) -> None:
    """`mode` ist `--read` oder `--write` -- daraus folgt die C3-Farbkategorie im Graphen
    (`--write` -> shared/tuerkis, `--read` -> foreign/grau)."""
    env = os.environ.copy()
    env["SPACE_DATA_ROOT"] = str(DATA_ROOT)
    subprocess.run(
        [".venv/bin/python", "phase6_shares/scripts/spacectl.py",
         "--data-root", str(DATA_ROOT), "create-space", name],
        check=True, env=env, cwd=str(REPO_ROOT), stdout=subprocess.DEVNULL,
    )
    subprocess.run(
        [".venv/bin/python", "phase6_shares/scripts/spacectl.py",
         "--data-root", str(DATA_ROOT), "add-member", mode, name, OWN_SPACE],
        check=True, env=env, cwd=str(REPO_ROOT), stdout=subprocess.DEVNULL,
    )


def _plan_items() -> list[dict]:
    """Baut die 200 Item-Beschreibungen (rein rechnerisch, kein I/O)."""
    plan: list[dict] = []
    index = 0
    for space, count in COUNTS.items():
        folders = FOLDERS[space]
        for k in range(count):
            tags = [f"gruppe-{index % TAG_GROUPS:02d}", "last-200"]
            if index % (TOTAL_NODES // SPITZE_TAG_SIZE) == 0:
                tags.append("spitze")
            plan.append({
                "space": space,
                "title": f"Knoten {index:03d} {space}",
                "type": "note" if index % 3 else "task",
                "tags": tags,
                "folder": folders[k % len(folders)],
                "index": index,
            })
            index += 1
    assert len(plan) == TOTAL_NODES, f"Plan hat {len(plan)} Items, erwartet {TOTAL_NODES}"
    spitze = sum(1 for p in plan if "spitze" in p["tags"])
    assert spitze == SPITZE_TAG_SIZE, f"'spitze' liegt auf {spitze} Knoten, erwartet {SPITZE_TAG_SIZE}"
    return plan


def _seed_items() -> dict[str, str]:
    """Legt die 200 Items ueber die Store-API an (zwei Durchgaenge -- IDs vergibt der Store,
    die `links:`-Ziele sind also erst nach dem ersten Durchgang bekannt)."""
    sys.path.insert(0, str(REPO_ROOT))
    from storage.store import Store

    store = Store(str(DATA_ROOT), now_fn=lambda: datetime.now(timezone.utc))
    plan = _plan_items()
    ids: list[str] = []

    t0 = time.monotonic()
    for entry in plan:
        item = store.create(
            entry["space"], type=entry["type"], title=entry["title"],
            tags=entry["tags"], folder=entry["folder"],
        )
        ids.append(item.id)
    t_create = time.monotonic() - t0

    # Durchgang 2: Frontmatter-Links (Ring mit Schrittweite LINK_STRIDE) + eine Handvoll
    # Body-Referenzen. Beides landet ueber `store.update` in derselben Datei -- der Store
    # zieht `item_links` bei jedem Schreibpfad selbst nach (B2).
    t0 = time.monotonic()
    for i, item_id in enumerate(ids):
        target = ids[(i + LINK_STRIDE) % TOTAL_NODES]
        body = ""
        if i < BODY_REF_COUNT:
            # Body-Referenz auf einen ANDEREN Knoten als das Frontmatter-Ziel, damit beide
            # Kantenquellen (frontmatter|body) unterscheidbar im Payload auftauchen.
            body = f"Querverweis im Text: {ids[(i + 1) % TOTAL_NODES]}\n"
        current = store.get(item_id)
        store.update(current.id, version=current.version, links=[target], body=body)
    t_link = time.monotonic() - t0

    store.rebuild_index()   # Hard Rule 2 -- Index ist Ableitung, Dateien sind die Wahrheit
    print(f"Anlegen: {t_create:.1f}s fuer {len(ids)} Items, Verlinken: {t_link:.1f}s")
    return {plan[i]["title"]: ids[i] for i in range(TOTAL_NODES)}


def _serve_alive(pid: int) -> bool:
    return Path(f"/proc/{pid}").exists()


def cmd_setup(args: argparse.Namespace) -> int:
    _setup_root()
    _install_keyring()
    creds = _provision_user(OWN_SPACE)
    CREDS_FILE.write_text(json.dumps(creds, indent=2))
    os.chmod(CREDS_FILE, 0o600)
    sys.stderr.write(
        f"Wegwerf-Setup: root={WEGWERF_ROOT}, user={creds['space']}, creds -> {CREDS_FILE}\n"
    )
    return 0


def cmd_seed_items(args: argparse.Namespace) -> int:
    _install_keyring()
    _create_member_space(SHARED_SPACE, "--write")
    _create_member_space(FOREIGN_SPACE, "--read")
    ids = _seed_items()
    (WEGWERF_ROOT / "ids.json").write_text(json.dumps(ids, indent=2))
    print(f"Items angelegt: {len(ids)} ({COUNTS}). IDs nach {WEGWERF_ROOT / 'ids.json'}.")
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
    env["SPACE_PUBLIC_BASE_URL"] = "https://wegwerf-200k.invalid"
    env["SPACE_PORT"] = str(PORT)
    env["CREDENTIALS_DIRECTORY"] = str(WEGWERF_ROOT)
    env["PYTHONPATH"] = str(REPO_ROOT)

    log = SERVE_LOG.open("ab")
    proc = subprocess.Popen(
        [".venv/bin/python", "phase2_mcp/scripts/serve.py",
         "--allowed-host", "127.0.0.1",
         "--allowed-host", "wegwerf-200k.invalid"],
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
    parser = argparse.ArgumentParser(description="Wegwerf-Instanz 200 Knoten (P8-22)")
    sub = parser.add_subparsers(dest="cmd", required=True)
    for name in ("setup", "seed-items", "start", "stop", "cleanup", "health"):
        sub.add_parser(name)
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
