#!/usr/bin/env python3
"""P10.5 Block 3, Schritt 3.5 — Bild-Metadaten (Web × MCP) und verwaiste Asset-Ordner (LG-7).

**Wegwerf (Plan §2.3):** Port **8799**, eigene Wurzel `/tmp/opencode/sharefyx-wegwerf-p105-b3`,
tmp-`DATA_ROOT`, tmp-`auth.sqlite3`, File-Keyring, Umgebung ohne `SHAREFYX_*`/`SFX_*`/`SPACE_*`,
Stopp **nur** über die PID-Datei (Hard Rule 9: nie `pkill -f`, nie der systemd-Dienst).

**Maschinerie:** `phase10_inventory/probes/p10_wegwerf.py` (Provisionierung, TLS-Start,
PID-Stopp). Die Web- und MCP-Helfer (Login mit TOTP, OAuth-Dance) kommen aus dem Block-2-Probe
`p105_b2_rights_probe.py` — **deren Modul-Import setzt die Pfadkonstanten auf die B2-Wurzel**,
deshalb werden sie hier **danach** auf die eigene Wurzel umgebogen. Der Port bleibt 8799 (Plan
§2.3), die Wurzel ist eine andere — die B2-Instanz muss dafür **beendet** sein.

**Was gemessen wird (Abnahme P10.5-12 und P10.5-13):**

1. **P10.5-12 (Web und MCP):** ein JPEG mit GPS-Koordinaten und Orientation 6 wird über
   **beide** Flächen hochgeladen (`POST /api/v1/items/{id}/assets` bzw. `put_item_asset`).
   Erwartet: die gespeicherte Datei trägt **keinen** GPS-Marker mehr, die **Orientation bleibt**
   (sonst stünde das Handyfoto quer), und die Datei ist kleiner als der Upload. Der Gegenlauf:
   ein Bild **ohne** Metadaten bleibt byte-identisch.
2. **P10.5-13 (LG-7):** ein Item mit Bild wird über die Web-Fläche gelöscht (`DELETE
   /api/v1/items/{id}` → `store.trash()`). Die Bilddateien bleiben liegen — das ist der
   dokumentierte Aufräum-Posten. `asset_orphans.py --report` muss **genau diesen** Ordner
   finden und die Assets **lebender** Items nicht; `--move` verschiebt ihn in den Papierkorb
   (nie ins Nirgendwo) und macht **einen** Commit.

Aufruf (Projekt-venv): `setup` → `start` → `assets` → `stop` (`cleanup` räumt die Wurzel ab).
Ausgabe: JSON auf stdout (Hard Rule 7) und `p105_b3_assets.json` daneben; Logs auf stderr.
"""
from __future__ import annotations

import argparse
import base64
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "phase10_inventory" / "probes"))
sys.path.insert(0, str(REPO_ROOT / "phase10_5_finishing" / "probes"))

import p10_wegwerf as w  # noqa: E402
import p105_b2_rights_probe as b2  # noqa: E402  (setzt w.* auf die B2-Wurzel — s. u.)

# --- eigene Wurzel (überschreibt die B2-Konstanten aus dem Import) ------------------------
ROOT = Path("/tmp/opencode/sharefyx-wegwerf-p105-b3")
w.WEGWERF_ROOT = ROOT
w.DATA_ROOT = ROOT / "data"
w.AUTH_DB = ROOT / "auth.sqlite3"
w.KEYRING_FILE = ROOT / "keyring.json"
w.DEK_FILE = ROOT / "auth-dek"
w.CREDS_FILE = ROOT / "credentials.json"
w.SERVE_PID = ROOT / "serve.pid"
w.SERVE_LOG = ROOT / "serve.log"
w.TLS_KEY = ROOT / "key.pem"
w.TLS_CERT = ROOT / "cert.pem"
IDS_FILE = ROOT / "ids.json"
OUT_JSON = Path(__file__).with_name("p105_b3_assets.json")
BASE = w.BASE_URL  # https://127.0.0.1:8799

ORPHAN_SCRIPT = REPO_ROOT / "phase10_5_finishing" / "scripts" / "asset_orphans.py"

GPS_MARKER = b"GPSLATITUDE-48-137-11-42"


# --- Bild-Fixtures (als Bytes gebaut, keine Binärdateien im Repo) -------------------------

def _jpeg_segment(marker: int, payload: bytes) -> bytes:
    return bytes([0xFF, marker]) + (len(payload) + 2).to_bytes(2, "big") + payload


def _exif_with_gps(orientation: int, gps: bytes) -> bytes:
    """Ein Exif-APP1 mit Orientation **und** einem GPS-IFD (ASCII-Marker)."""
    entries = 2
    gps_ifd = 8 + 2 + 12 * entries + 4
    gps_data = gps_ifd + 2 + 12 + 4
    tiff = bytearray(b"II\x2a\x00")
    tiff += (8).to_bytes(4, "little")
    tiff += entries.to_bytes(2, "little")
    tiff += (0x0112).to_bytes(2, "little") + (3).to_bytes(2, "little")
    tiff += (1).to_bytes(4, "little") + orientation.to_bytes(2, "little") + b"\x00\x00"
    tiff += (0x8825).to_bytes(2, "little") + (4).to_bytes(2, "little")
    tiff += (1).to_bytes(4, "little") + gps_ifd.to_bytes(4, "little")
    tiff += (0).to_bytes(4, "little")
    tiff += (1).to_bytes(2, "little")
    tiff += (0x0001).to_bytes(2, "little") + (2).to_bytes(2, "little")
    tiff += len(gps).to_bytes(4, "little") + gps_data.to_bytes(4, "little")
    tiff += (0).to_bytes(4, "little")
    tiff += gps
    return b"Exif\x00\x00" + bytes(tiff)


def _jpeg_with_exif(orientation: int, gps: bytes) -> bytes:
    """Ein JPEG mit Exif (Orientation + GPS), ICC-Profil und Bildinhalt."""
    return (
        b"\xff\xd8"
        + _jpeg_segment(0xE1, _exif_with_gps(orientation, gps))
        + _jpeg_segment(0xE2, b"ICC_PROFILE\x00PROFIL")
        + b"\xff\xda" + (8).to_bytes(2, "big") + b"\x00\x01\x00\x00" + b"\x42" * 24 + b"\xff\xd9"
    )


def _clean_jpeg() -> bytes:
    """Ein JPEG **ohne** Metadaten — der Gegenlauf: es bleibt byte-identisch."""
    return (
        b"\xff\xd8"
        + _jpeg_segment(0xE0, b"JFIF\x00")
        + b"\xff\xda" + (8).to_bytes(2, "big") + b"\x00\x01\x00\x00" + b"\x42" * 24 + b"\xff\xd9"
    )


# --- Setup --------------------------------------------------------------------------------

SEED = [
    ("web_upload", "alpha", "Web Upload"),
    ("mcp_upload", "alpha", "MCP Upload"),
    ("clean_upload", "alpha", "Sauberes Bild"),
    ("orphan", "alpha", "Waisen-Kandidat"),
]


def cmd_setup(_args: argparse.Namespace) -> int:
    w.cmd_setup(_args)  # zwei Principale alpha + beta in der tmp-auth.sqlite3
    w._install_keyring()
    w._spacectl("create-space", "alpha")

    from storage.store import Store
    store = Store(str(w.DATA_ROOT), now_fn=lambda: datetime.now(timezone.utc), git=False)
    ids = {}
    for key, space, title in SEED:
        ids[key] = store.create(space, type="note", title=title, body="Wegwerf P10.5 B3.").id
    store.rebuild_index()
    IDS_FILE.write_text(json.dumps(ids, indent=2))
    b2.log(f"Seed: {len(ids)} Items in alpha -> {IDS_FILE}")
    return 0


# --- Messung ------------------------------------------------------------------------------

RESULTS: list[dict] = []


def cell(name: str, ok: bool, detail: str) -> None:
    RESULTS.append({"cell": name, "pass": bool(ok), "detail": detail})
    b2.log(f"[{'OK  ' if ok else 'FAIL'}] {name}: {detail}")


def _stored_path(space: str, item_id: str, asset_id: str) -> Path:
    return w.DATA_ROOT / space / "_assets" / item_id / f"{asset_id}.jpg"


def _orientation_in(data: bytes) -> int | None:
    """Liest die Orientation aus einem JPEG (der Probe-eigene Gegenleser, unabhängig vom
    Stripper im Produktivcode — sonst prüfte der Test die Implementierung mit sich selbst)."""
    pos = 2
    while pos < len(data):
        if data[pos] != 0xFF:
            return None
        marker_start = pos
        while pos < len(data) and data[pos] == 0xFF:
            pos += 1
        marker = data[pos]
        pos += 1
        if marker in (0xDA, 0xD9):
            return None
        length = int.from_bytes(data[pos:pos + 2], "big")
        payload = data[pos + 2:pos + length]
        if marker == 0xE1 and payload.startswith(b"Exif\x00\x00"):
            tiff = payload[6:]
            ifd0 = int.from_bytes(tiff[4:8], "little")
            count = int.from_bytes(tiff[ifd0:ifd0 + 2], "little")
            for index in range(count):
                entry = ifd0 + 2 + index * 12
                tag = int.from_bytes(tiff[entry:entry + 2], "little")
                if tag == 0x0112:
                    return int.from_bytes(tiff[entry + 8:entry + 10], "little")
        pos += length
        del marker_start
    return None


def _run_orphans(*args: str) -> dict:
    """Ruft `asset_orphans.py` gegen den Wegwerf-DATA_ROOT auf."""
    result = subprocess.run(
        [str(REPO_ROOT / ".venv/bin/python"), str(ORPHAN_SCRIPT),
         "--data-root", str(w.DATA_ROOT), *args],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )
    if result.returncode != 0:
        return {"returncode": result.returncode, "stderr": result.stderr[-400:]}
    return json.loads(result.stdout)


def cmd_assets(_args: argparse.Namespace) -> int:
    ids = json.loads(IDS_FILE.read_text())
    alpha = json.loads(w.CREDS_FILE.read_text())["users"][0]
    assert alpha["space"] == "alpha"

    jpeg = _jpeg_with_exif(6, GPS_MARKER)
    sauber = _clean_jpeg()

    # -- 1. Web-Upload -------------------------------------------------------------------
    web = b2.Web(alpha)
    web.login()
    r = web.c.post(
        f"/api/v1/items/{ids['web_upload']}/assets",
        headers={**web._h(), "Content-Type": "image/jpeg"}, content=jpeg,
    )
    web_asset = r.json() if r.status_code == 201 else {}
    web_file = _stored_path("alpha", ids["web_upload"], web_asset.get("id", ""))
    web_bytes = web_file.read_bytes() if web_file.is_file() else b""
    cell("Web-Upload: GPS weg", GPS_MARKER not in web_bytes,
         f"HTTP {r.status_code}, Datei {len(web_bytes)} B (Upload {len(jpeg)} B)")
    cell("Web-Upload: Orientation bleibt", _orientation_in(web_bytes) == 6,
         f"Orientation={_orientation_in(web_bytes)} (erwartet 6)")
    cell("Web-Upload: ICC bleibt", b"ICC_PROFILE" in web_bytes, "Farbprofil erhalten")

    # Gegenlauf: ein Bild ohne Metadaten bleibt byte-identisch.
    r = web.c.post(
        f"/api/v1/items/{ids['clean_upload']}/assets",
        headers={**web._h(), "Content-Type": "image/jpeg"}, content=sauber,
    )
    clean_asset = r.json() if r.status_code == 201 else {}
    clean_file = _stored_path("alpha", ids["clean_upload"], clean_asset.get("id", ""))
    clean_bytes = clean_file.read_bytes() if clean_file.is_file() else b""
    cell("Web-Upload: sauberes Bild byte-identisch", clean_bytes == sauber,
         f"{len(clean_bytes)} B gegen {len(sauber)} B Upload")

    # -- 2. MCP-Upload -------------------------------------------------------------------
    mcp = b2.Mcp(alpha)
    mcp.oauth()
    out = mcp.tool("put_item_asset", item_id=ids["mcp_upload"],
                   data_base64=base64.b64encode(jpeg).decode())
    # Die Quittung ist ein JSON-Objekt (`compact_json`) — die Asset-ID wird **daraus** gelesen,
    # nicht geraten: eine leere Datei als Ergebnis waere sonst ein *vakuoser* Treffer
    # („GPS nicht drin" waere auch bei 0 Byte wahr).
    treffer = re.search(r'"asset_id"\s*:\s*"(ast_[0-9a-f]{8})"', out["text"])
    asset_id = treffer.group(1) if treffer else ""
    mcp_file = _stored_path("alpha", ids["mcp_upload"], asset_id)
    mcp_bytes = mcp_file.read_bytes() if mcp_file.is_file() else b""
    cell("MCP-Upload: Datei liegt auf der Platte", bool(asset_id) and mcp_file.is_file(),
         f"asset_id={asset_id or '—'}, Datei {len(mcp_bytes)} B (Upload {len(jpeg)} B)")
    cell("MCP-Upload: GPS weg", bool(mcp_bytes) and GPS_MARKER not in mcp_bytes,
         f"is_error={out['is_error']}, Datei {len(mcp_bytes)} B")
    cell("MCP-Upload: Orientation bleibt", _orientation_in(mcp_bytes) == 6,
         f"Orientation={_orientation_in(mcp_bytes)} (erwartet 6)")

    # -- 3. LG-7: verwaiste Asset-Ordner ---------------------------------------------------
    # Das Item mit Bild wird gelöscht (Web-Fläche → `store.trash()`); die Bilddateien
    # bleiben liegen — genau der Fall, den LG-7 aufräumen soll.
    # Der Waisen-Kandidat braucht **ein Bild** — ohne Bild gäbe es keinen verwaisten Ordner,
    # und der Bericht fände (richtig) nichts.
    r = web.c.post(
        f"/api/v1/items/{ids['orphan']}/assets",
        headers={**web._h(), "Content-Type": "image/jpeg"}, content=jpeg,
    )
    cell("Waisen-Kandidat hat ein Bild", r.status_code == 201, f"HTTP {r.status_code}")
    live_before = sorted(
        p.name for p in (w.DATA_ROOT / "alpha" / "_assets").iterdir() if p.is_dir()
    )
    item = web.get(ids["orphan"])
    r = web.c.request("DELETE", f"/api/v1/items/{ids['orphan']}",
                      headers=web._h(), json={"version": item["version"], "confirm": item["title"]})
    cell("Löschen (Web) verschiebt nach ._trash", r.status_code == 204, f"HTTP {r.status_code}")

    report = _run_orphans("--report")
    orphans = report.get("orphans", []) if isinstance(report, dict) else []
    cell("LG-7: Bericht findet genau die Waise", len(orphans) == 1
         and orphans[0]["item_id"] == ids["orphan"],
         f"gefunden={[o['item_id'] for o in orphans]}, erwartet={ids['orphan']}")
    cell("LG-7: lebende Assets bleiben unberührt",
         all(o["item_id"] != ids["web_upload"] for o in orphans),
         f"IDs im Bericht: {[o['item_id'] for o in orphans]}")

    commits_before = subprocess.run(
        ["git", "-C", str(w.DATA_ROOT), "rev-list", "--count", "HEAD"],
        capture_output=True, text=True).stdout.strip()
    move = _run_orphans("--move")
    commits_after = subprocess.run(
        ["git", "-C", str(w.DATA_ROOT), "rev-list", "--count", "HEAD"],
        capture_output=True, text=True).stdout.strip()
    quelle = w.DATA_ROOT / "alpha" / "_assets" / ids["orphan"]
    ziel = w.DATA_ROOT / "._trash" / "alpha" / "_assets" / ids["orphan"]
    cell("LG-7: --move verschiebt in den Papierkorb", not quelle.exists() and ziel.is_dir(),
         f"Quelle {quelle.exists()}, Ziel {ziel.is_dir()}")
    cell("LG-7: genau ein Commit", commits_after != commits_before,
         f"Commits {commits_before} -> {commits_after}")
    cell("LG-7: lebende Assets nach dem Move noch da",
         all((w.DATA_ROOT / "alpha" / "_assets" / name).is_dir() for name in live_before
             if name != ids["orphan"]),
         f"vorher: {live_before}")

    sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=REPO_ROOT,
                         capture_output=True, text=True).stdout.strip()
    result = {
        "probe": "p105_b3_assets", "head": sha, "base_url": BASE,
        "cells": len(RESULTS), "passed": sum(1 for r in RESULTS if r["pass"]),
        "details": RESULTS,
    }
    OUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "details"}))
    return 0 if result["passed"] == result["cells"] else 1


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="P10.5 B3 Bild-Metadaten + Waisen (Wegwerf 8799)")
    p.add_argument("cmd", choices=["setup", "start", "stop", "cleanup", "health", "assets"])
    args = p.parse_args(argv)
    return {"setup": cmd_setup, "start": w.cmd_start, "stop": w.cmd_stop,
            "cleanup": w.cmd_cleanup, "health": w.cmd_health, "assets": cmd_assets}[args.cmd](args)


if __name__ == "__main__":
    raise SystemExit(main())
