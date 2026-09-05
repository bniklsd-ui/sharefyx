#!/usr/bin/env python3
"""Phase 8.5 Block C -- Wegwerf-Instanz fuer den v3-Vorabritt (Plan §4.1).

Standing-Permission-Rahmen (Wurzel-CLAUDE.md + Phase-8.5 §0.0): eigener Port (18773,
V98 -- 18766-18772 waren Phase 8), tmp-DATA_ROOT, File-Keyring-Backend statt
`nikinger-space`, User direkt in auth.sqlite3 provisioniert (kein provision_user.py,
kein keyring.set_password). Cleanup per `kill -TERM $(cat serve.pid)` -- kein
`pkill -f` mit Regex (Hard Rule 9).

Datenlage (Plan §4.1, exakt):
  - drei Spaces: alpha (eigen), beta (geteilt, write), gamma (fremd, nur read)
  - ~30 Items, davon >= 6 in Ordnern, 1 archiviert, 1 mit item-level `share_read`
    (der Deploy-Blocker-Fall aus P6 §35-39)
  - >= 6 explizite Kanten: 3 ueber `links:`, 3 ueber `itm_`-Referenzen im Body
  - >= 2 Tags, die mehrere Items teilen (fuer den Tag-Toggle)
  - 1 Item mit Bild-Asset (P6.5 Block B, `put_asset()` -> `_assets/<item>/<ast_...>.png`,
    Body-Referenz `![Alt](asset:ast_...)`)

Item-Layout (12 alpha + 10 beta + 8 gamma = 30 Items):
  alpha (eigener Space):
    Projekte/Backend/
      itm_a1  Auth-Service refactoren     tags:[backend, wichtig]  link: b1
      itm_a2  DB-Migration skript          tags:[backend, infra]    link: b2
      itm_a3  Logging standardisieren      tags:[backend]           body: g1
      itm_a4  Smoke-Tests ausbauen         tags:[backend, qa]      link: a5
    Projekte/Frontend/
      itm_a5  Komponenten-Bibliothek       tags:[frontend, wichtig] link: b3
      itm_a6  Storybook einrichten         tags:[frontend, qa]      body: g2
      itm_a7  Styleguide pflegen           tags:[frontend, design]  body: b3
    Notizen/
      itm_a8  Buecherliste Q4              tags:[lesen]             link: a9
      itm_a9  Empfehlungen Nikinger        tags:[lesen]             archive-Status:
                                                                  -- dieses Item
                                                                  traegt item-level
                                                                  share_read=[gamma]
      itm_a10 Tagesnotizen                 tags:[log]               ASSET: 1x1 PNG,
                                                                  Body `![Skizze]
                                                                  (asset:ast_...)`
    (root)
      itm_a11 Sprint-Planning              tags:[planung]
      itm_a12 Retro-Notizen                tags:[retro]             -- archiviert
  beta (fremd-readable+writeable fuer alpha):
    Projekte/
      itm_b1  Pair-Programming Erfahrungen  tags:[wissen, lesen]   link: a6
      itm_b2  Konferenz 2026                tags:[wissen]
      itm_b3  Externe Bibliothek            tags:[frontend]         body: a7
      itm_b4  Design-Reviews                tags:[design, frontend] link: b3
    Logbuch/
      itm_b5  Wochennotizen                 tags:[log]
      itm_b6  Geteilte Notizen              tags:[log, wissen]
    Notizen/
      itm_b7  Sprint-Sync                   tags:[planung]
      itm_b8  Sprint-Retro                  tags:[retro]
    (root)
      itm_b9  Pair-Setup                    tags:[wissen]
      itm_b10 Onboarding                    tags:[wissen]
  gamma (fremd-readable fuer alpha, ueber space-level grant, plus item-level
  share_read auf a9 -- der Deploy-Blocker-Fall):
    Projekte/Backend/
      itm_g1  Performance-Audit             tags:[backend, infra]
      itm_g2  Cache-Strategie               tags:[backend, infra]   body: a6
    Notizen/
      itm_g3  IT-Sekus Meeting              tags:[meeting]
    Projekte/Frontend/
      itm_g4  Performance-Optimierungen     tags:[frontend]
    Logbuch/
      itm_g5  Infra-Incidents               tags:[log, infra]
    (root)
      itm_g6  Monitoring-Setup              tags:[infra]
      itm_g7  Backup-Strategie              tags:[infra]
      itm_g8  Test-Datenraum                tags:[infra]

Damit entstehen:
  - explizite Frontmatter-Kanten (links:): 6 Stueck (alle --link-Eintraege)
  - explizite Body-Kanten (itm_...): 3 Stueck (a3->g1, a6->g2, a7->b3, b3->a7 -- drei
    Stueck, weil die Body-Referenzen in beide Richtungen gehen)
  - Tag-Edges: backend (4), frontend (4), infra (5), wissen (4), log (3), lesen (2),
    design (2), qa (2), planung (2), retro (2), wichtig (2), meeting (1)
  - Ordner-Edges: Projekte/Backend in alpha (4), Projekte/Frontend in alpha (3),
    Notizen in alpha (3), Logbuch in alpha (1); je 1-3 in beta/gamma
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

WEGWERF_ROOT = Path("/tmp/opencode/sharefyx-wegwerf-v3ritt")
DATA_ROOT = WEGWERF_ROOT / "data"
AUTH_DB = WEGWERF_ROOT / "auth.sqlite3"
KEYRING_FILE = WEGWERF_ROOT / "keyring.json"
DEK_FILE = WEGWERF_ROOT / "auth-dek"
CREDS_FILE = WEGWERF_ROOT / "credentials.json"
SERVE_PID = WEGWERF_ROOT / "serve.pid"
SERVE_LOG = WEGWERF_ROOT / "serve.log"
PORT = 18773
OWN_SPACE = "alpha"
SHARED_WRITE_SPACE = "beta"
FOREIGN_READ_SPACE = "gamma"

REPO_ROOT = Path(__file__).resolve().parents[2]

# Item-Konfiguration: (title, type, tags, folder, body_ref_short_key_or_None,
#                      link_short_key_or_None, status_or_None, item_share_read_or_None,
#                      has_asset_or_None)
ALPHA_ITEMS = [
    ("Auth-Service refactoren",     "task", ["backend", "wichtig"],  "Projekte/Backend",   None,  "b1",  None, None, None),
    ("DB-Migration skript",         "task", ["backend", "infra"],    "Projekte/Backend",   None,  "b2",  None, None, None),
    ("Logging standardisieren",     "task", ["backend"],             "Projekte/Backend",   "g1",  None,  None, None, None),
    ("Smoke-Tests ausbauen",        "task", ["backend", "qa"],       "Projekte/Backend",   None,  "a5",  None, None, None),
    ("Komponenten-Bibliothek",      "note", ["frontend", "wichtig"], "Projekte/Frontend",  None,  "b3",  None, None, None),
    ("Storybook einrichten",        "task", ["frontend", "qa"],      "Projekte/Frontend",  "g2",  None,  None, None, None),
    ("Styleguide pflegen",          "note", ["frontend", "design"],  "Projekte/Frontend",  "b3",  None,  None, None, None),
    ("Buecherliste Q4",             "note", ["lesen"],               "Notizen",            None,  "a9",  None, None, None),
    ("Empfehlungen Nikinger",       "note", ["lesen"],               "Notizen",            None,  None,  None, ["gamma"], None),
    ("Tagesnotizen",                "note", ["log"],                 "Notizen",            None,  None,  None, None, True),
    ("Sprint-Planning",             "note", ["planung"],             "",                   None,  None,  None, None, None),
    ("Retro-Notizen",               "note", ["retro"],               "",                   None,  None,  "archived", None, None),
]
BETA_ITEMS = [
    ("Pair-Programming Erfahrungen", "note", ["wissen", "lesen"],    "Projekte",           None,  "a6",  None, None, None),
    ("Konferenz 2026",               "note", ["wissen"],             "Projekte",           None,  None,  None, None, None),
    ("Externe Bibliothek",           "note", ["frontend"],           "Projekte",           "a7",  None,  None, None, None),
    ("Design-Reviews",               "note", ["design", "frontend"], "Projekte",           None,  "b3",  None, None, None),
    ("Wochennotizen",                "note", ["log"],                "Logbuch",            None,  None,  None, None, None),
    ("Geteilte Notizen",             "note", ["log", "wissen"],      "Logbuch",            None,  None,  None, None, None),
    ("Sprint-Sync",                  "note", ["planung"],            "Notizen",            None,  None,  None, None, None),
    ("Sprint-Retro",                 "note", ["retro"],              "Notizen",            None,  None,  None, None, None),
    ("Pair-Setup",                   "note", ["wissen"],             "",                   None,  None,  None, None, None),
    ("Onboarding",                   "note", ["wissen"],             "",                   None,  None,  None, None, None),
]
GAMMA_ITEMS = [
    ("Performance-Audit",            "task", ["backend", "infra"],   "Projekte/Backend",   None,  None,  None, None, None),
    ("Cache-Strategie",              "task", ["backend", "infra"],   "Projekte/Backend",   None,  None,  None, None, None),
    ("IT-Sekus Meeting",             "note", ["meeting"],            "Notizen",            None,  None,  None, None, None),
    ("Performance-Optimierungen",    "task", ["frontend"],           "Projekte/Frontend",  None,  None,  None, None, None),
    ("Infra-Incidents",              "note", ["log", "infra"],       "Logbuch",            None,  None,  None, None, None),
    ("Monitoring-Setup",             "note", ["infra"],              "",                   None,  None,  None, None, None),
    ("Backup-Strategie",             "note", ["infra"],              "",                   None,  None,  None, None, None),
    ("Test-Datenraum",               "note", ["infra"],              "",                   None,  None,  None, None, None),
]

# Aufloesung Kurzname -> "space:title"-Key
SHORT_KEY_TO_INDEX = {
    # alpha
    "a1":  ("alpha", "Auth-Service refactoren"),
    "a3":  ("alpha", "Logging standardisieren"),
    "a5":  ("alpha", "Komponenten-Bibliothek"),
    "a6":  ("alpha", "Storybook einrichten"),
    "a7":  ("alpha", "Styleguide pflegen"),
    "a9":  ("alpha", "Empfehlungen Nikinger"),
    # beta
    "b1":  ("beta",  "Pair-Programming Erfahrungen"),
    "b2":  ("beta",  "Konferenz 2026"),
    "b3":  ("beta",  "Externe Bibliothek"),
    # gamma
    "g1":  ("gamma", "Performance-Audit"),
    "g2":  ("gamma", "Cache-Strategie"),
}


class FileBackend(keyring.backend.KeyringBackend):
    """File-Keyring-Backend (Phase 8 + 6.5 + 7 + 8.5 -- jede Phase ihr eigenes)."""

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

    password = "wegwerf-v3ritt-" + secrets.token_urlsafe(8)
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


def _create_shared_space(name: str, write: bool) -> None:
    """Legt einen zweiten/dritten Space an und gibt `alpha` Lese- oder Schreibzugriff.

    `spacectl.py add-member` aktualisiert `<space>/.share.yml` und macht den Space
    damit in `state.spaces` von alpha sichtbar (mit `writable: True/False`)."""
    env = os.environ.copy()
    env["SPACE_DATA_ROOT"] = str(DATA_ROOT)
    subprocess.run(
        [".venv/bin/python", "phase6_shares/scripts/spacectl.py",
         "--data-root", str(DATA_ROOT),
         "create-space", name],
        check=True, env=env, cwd=str(REPO_ROOT), stdout=subprocess.DEVNULL,
    )
    flag = "--write" if write else "--read"
    subprocess.run(
        [".venv/bin/python", "phase6_shares/scripts/spacectl.py",
         "--data-root", str(DATA_ROOT),
         "add-member", flag, name, OWN_SPACE],
        check=True, env=env, cwd=str(REPO_ROOT), stdout=subprocess.DEVNULL,
    )


def _seed_items() -> dict[str, str]:
    """Legt alle Items ueber die Store-API direkt an (folder-faehig, mit archivierten
    Items und item-level share_read), dann Body-Refs, Frontmatter-Links, Asset-Upload.

    Die Reihenfolge ist wichtig:
      1. Alle Items anlegen (auch das mit Body-Refs -- die koennen erst danach gepatcht
         werden, sobald die Ziel-IDs bekannt sind).
      2. Item-level share_read fuer ein Item setzen (zusaetzlich zum space-level grant).
      3. Body-Refs einsetzen (store.update mit dem fertigen Body).
      4. Frontmatter-Links setzen.
      5. Asset-Upload (P6.5), Body bekommt die `![Alt](asset:ast_...)`-Referenz.
      6. rebuild_index().
    """
    sys.path.insert(0, str(REPO_ROOT))
    from storage.store import Store

    store = Store(str(DATA_ROOT), now_fn=lambda: datetime.now(timezone.utc))
    ids: dict[str, str] = {}

    def _add(space: str, title: str, kind: str, tags: list[str], folder: str,
             *, status: str | None = None, share_read: list[str] | None = None) -> str:
        kwargs = {"status": status} if status else {}
        if share_read:
            kwargs["share_read"] = list(share_read)
        item = store.create(space, type=kind, title=title, tags=tags, folder=folder, **kwargs)
        return item.id

    for space, items in (("alpha", ALPHA_ITEMS), ("beta", BETA_ITEMS), ("gamma", GAMMA_ITEMS)):
        for (title, kind, tags, folder, _body_ref, _link, status, share_read, _has_asset) in items:
            key = f"{space}:{title}"
            ids[key] = _add(space, title, kind, tags, folder,
                            status=status, share_read=share_read)

    # Body-Refs (3 Stueck) -- wir patchen den Body via store.update. Die Body-Referenzen
    # duerfen erst gesetzt werden, NACHDEM alle Items angelegt sind (sonst kennen wir die
    # Ziel-IDs noch nicht). Reihenfolge: a3->g1, a6->g2, a7->b3.
    def _patch_body(src_key: str, target_short: str, intro: str) -> None:
        target_space, target_title = SHORT_KEY_TO_INDEX[target_short]
        src_id = ids[src_key]
        target_id = ids[f"{target_space}:{target_title}"]
        body = (
            f"{intro}\n\n"
            f"Siehe auch Notiz {target_id} fuer mehr Kontext.\n"
            f"Direkter Verweis: [Detail](#item/{target_id})."
        )
        current = store.get(src_id)
        store.update(src_id, version=current.version, body=body)

    _patch_body("alpha:Logging standardisieren", "g1",
                "## Hintergrund\n\nDas Backend wird komplett auf strukturiertes Logging umgestellt.")
    _patch_body("alpha:Storybook einrichten",   "g2",
                "## Plan\n\nStorybook deckt die Komponenten-Bibliothek ab.")
    _patch_body("alpha:Styleguide pflegen",     "b3",
                "## Stand\n\nDokumentation der Patterns.")

    # Frontmatter-Links -- map von Kurz-IDs auf vollstaendige "space:title"-Keys.
    def _set_link(src_key: str, target_short: str) -> None:
        target_space, target_title = SHORT_KEY_TO_INDEX[target_short]
        src_id = ids[src_key]
        target_id = ids[f"{target_space}:{target_title}"]
        current = store.get(src_id)
        store.update(src_id, version=current.version, links=[target_id])

    all_items = ALPHA_ITEMS + BETA_ITEMS + GAMMA_ITEMS
    for space, items in (("alpha", ALPHA_ITEMS), ("beta", BETA_ITEMS), ("gamma", GAMMA_ITEMS)):
        for (title, _kind, _tags, _folder, _body_ref, link, *_rest) in items:
            if link is None:
                continue
            _set_link(f"{space}:{title}", link)

    # V102-Hilfspräparat: "Buecherliste Q4" (alpha) bekommt zusätzlich zu seinem
    # Frontmatter-Link (auf a9 = "Empfehlungen Nikinger") einen Body-Ref auf dasselbe
    # Ziel. Damit gibt es zwischen den beiden Knoten zwei Kanten (eine frontmatter, eine
    # body), ohne dass die UI im Smoke etwas speichern muss -- Plan §4.3 V102 ist
    # "zeichnet der Graph eine oder zwei Linien?" und braucht eine echte Quelle, nicht
    # einen UI-Test, der selbst am CSRF scheitert (Wegwerf hat
    # SPACE_PUBLIC_BASE_URL=`https://...invalid`, der Browser sendet Origin=`http://127.0.0.1`,
    # CSRF lehnt ab -- das ist ein Befund fuer Block D / Step Z, kein Ritt-fix).
    _twintarget_space, _twintarget_title = SHORT_KEY_TO_INDEX["a9"]
    _twintarget_id = ids[f"{_twintarget_space}:{_twintarget_title}"]
    _twin_src_id = ids["alpha:Buecherliste Q4"]
    current = store.get(_twin_src_id)
    store.update(
        _twin_src_id,
        version=current.version,
        body=(
            "## Verwandt\n\n"
            "Siehe auch Notiz " + _twintarget_id + " fuer mehr Kontext.\n"
            "Direkter Verweis: [Detail](#item/" + _twintarget_id + ")."
        ),
    )

    # Asset-Upload -- 1x1 transparentes PNG (67 Bytes). Wir koennen den Alpha-Wert auf 0
    # setzen, dann ist das Bild komplett unsichtbar -- Smoke muss nur pruefen, dass die
    # `![Alt](asset:ast_...)`-Referenz im Body ueberlebt und dass `GET /api/v1/items/<id>/assets`
    # `ast_xxxxxxxx` zurueckgibt. Sniff-Erkennung erwartet PNG-Header (89 50 4E 47).
    asset_id = _upload_minimal_png(store, ids["alpha:Tagesnotizen"])

    # Body des Asset-Items um die Markdown-Referenz erweitern.
    asset_item_id = ids["alpha:Tagesnotizen"]
    current = store.get(asset_item_id)
    asset_body = (
        "## Tagesplan\n\n"
        "Siehe Skizze: ![Skizze](asset:" + asset_id + ")\n\n"
        "Notizen zum Tagesplan folgen."
    )
    store.update(asset_item_id, version=current.version, body=asset_body)

    # Reindex (Hard Rule 2: Index jederzeit rekonstruierbar).
    store.rebuild_index()
    return ids, asset_id


def _upload_minimal_png(store, item_id: str) -> str:
    """Schreibt ein 1x1-PNG unter `<space>/_assets/<item_id>/` und gibt die Asset-ID zurueck."""
    import struct
    import zlib

    def _chunk(tag: bytes, data: bytes) -> bytes:
        return (struct.pack(">I", len(data)) + tag + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))

    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", 1, 1, 8, 6, 0, 0, 0)
    raw = b"\x00" + b"\x00\x00\x00\x00"  # filter byte + RGBA(0,0,0,0) = 1x1 transparent
    idat = zlib.compress(raw)
    png = sig + _chunk(b"IHDR", ihdr) + _chunk(b"IDAT", idat) + _chunk(b"IEND", b"")

    asset = store.put_asset(item_id, data=png, filename="skizze.png")
    return asset.id


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
    _create_shared_space(SHARED_WRITE_SPACE, write=True)
    _create_shared_space(FOREIGN_READ_SPACE, write=False)
    ids, asset_id = _seed_items()
    (WEGWERF_ROOT / "ids.json").write_text(json.dumps(
        {"ids": ids, "asset_id": asset_id,
         "shared_write_space": SHARED_WRITE_SPACE,
         "foreign_read_space": FOREIGN_READ_SPACE}, indent=2))
    print(
        f"Items + Spaces angelegt: {len(ids)} insgesamt "
        f"(alpha={len(ALPHA_ITEMS)}, beta={len(BETA_ITEMS)}, gamma={len(GAMMA_ITEMS)}); "
        f"Asset-ID {asset_id}. IDs nach {WEGWERF_ROOT / 'ids.json'}."
    )
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
    env["SPACE_PUBLIC_BASE_URL"] = "https://wegwerf-v3ritt.invalid"
    env["SPACE_PORT"] = str(PORT)
    env["CREDENTIALS_DIRECTORY"] = str(WEGWERF_ROOT)
    env["PYTHONPATH"] = str(REPO_ROOT)

    log = SERVE_LOG.open("ab")
    proc = subprocess.Popen(
        [".venv/bin/python", "phase2_mcp/scripts/serve.py",
         "--allowed-host", "127.0.0.1",
         "--allowed-host", "wegwerf-v3ritt.invalid"],
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
    parser = argparse.ArgumentParser(description="Wegwerf-Instanz Phase 8.5 v3-Vorabritt")
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
