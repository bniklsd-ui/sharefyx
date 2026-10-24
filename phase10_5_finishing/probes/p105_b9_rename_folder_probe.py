#!/usr/bin/env python3
"""P10.5 Block 9, Schritt 9.2 — RE-4 `rename_folder` über die Web-API (P1-Öffnung 13).

**Wegwerf (Plan §2.3):** Port **8799**, eigene Wurzel `/tmp/opencode/sharefyx-wegwerf-p105-b9r`,
tmp-`DATA_ROOT`, tmp-`auth.sqlite3`, File-Keyring, Umgebung ohne `SHAREFYX_*`/`SFX_*`/`SPACE_*`,
Stopp **nur** über die PID-Datei (Hard Rule 9: nie `pkill -f`, nie der systemd-Dienst).

**Maschinerie:** `phase10_inventory/probes/p10_wegwerf.py` (Provisionierung, TLS-Start,
PID-Stopp) und der Web-Helfer aus dem Block-2-Probe `p105_b2_rights_probe.py` — **deren
Modul-Import setzt die Pfadkonstanten auf die B2-Wurzel**, deshalb werden sie hier **danach**
auf die eigene Wurzel umgebogen. Der Port bleibt 8799 (Plan §2.3), die Wurzel ist eine andere.

**Was gemessen wird (Abnahme P10.5-42):** das Umbenennen ist **atomar** — ein Commit, die
Versionen bleiben, die Freigabe wandert mit — und der **Gegenlauf** gilt: ein existierendes
Ziel wird abgelehnt und **nichts** bewegt.

| # | Zelle | Erwartung |
|---|---|---|
| 1 | Web-Rename | HTTP 200, `items` nennt die Zahl der betroffenen Items |
| 2 | Die Datei liegt am **neuen** Pfad | alte Datei weg, neue Datei da |
| 3 | Die **Version** ist unverändert | `version:` in der Datei wie vorher |
| 4 | Die **Freigabe wandert mit** | `.share.yml` im neuen Ordner, alte weg |
| 5 | **Ein Commit** | genau eine Meldung `rename-folder alpha:projekte→vorhaben` |
| 6 | Der Index stimmt | das Item meldet `folder == "vorhaben"` |
| 7 | **Gegenlauf**: Ziel existiert | **422**, **nichts** bewegt |
| 8 | Ablehnung: Ziel **unter** dem alten Ordner | **422**, nichts bewegt |
| 9 | **CSRF-Pflicht** | ohne Token **403**, nichts bewegt |

Die Unit-Ebene trägt die Regel-Gegenläufe (`phase1_storage/tests/test_store.py`), die Probe
trägt das **Zusammenspiel** von HTTP-Route, Kern und Platte.

Aufruf (Projekt-venv): `setup` → `start` → `probe` → `stop` (`cleanup` räumt die Wurzel ab).
Ausgabe: JSON auf stdout (Hard Rule 7) und `p105_b9_rename_folder.json` daneben; Logs auf stderr.
"""
from __future__ import annotations

import argparse
import json
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
ROOT = Path("/tmp/opencode/sharefyx-wegwerf-p105-b9r")
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
OUT_JSON = Path(__file__).with_name("p105_b9_rename_folder.json")
BASE = w.BASE_URL  # https://127.0.0.1:8799

ORDNER_ALT = "projekte"
ORDNER_NEU = "vorhaben"
ORDNER_BELEGT = "belegt"


# --- Setup --------------------------------------------------------------------------------

def cmd_setup(_args: argparse.Namespace) -> int:
    w.cmd_setup(_args)  # zwei Principale alpha + beta in der tmp-auth.sqlite3
    w._install_keyring()
    w._spacectl("create-space", "alpha")

    from storage.store import Store
    store = Store(str(w.DATA_ROOT), now_fn=lambda: datetime.now(timezone.utc), git=False)
    ids = {}
    # Ein Item **im** Ordner `projekte` und eines im **belegten** Ordner (Gegenlauf-Ziel).
    ids["projekt"] = store.create(
        "alpha", type="note", title="Projekt", body="Wegwerf P10.5 B9.2.", folder=ORDNER_ALT
    ).id
    ids["belegt"] = store.create(
        "alpha", type="note", title="Belegt", body="Wegwerf.", folder=ORDNER_BELEGT
    ).id
    # Eine **Freigabe** im Ordner `projekte` — sie muss mit dem Ordner wandern (RE-4).
    ordner = w.DATA_ROOT / "alpha" / ORDNER_ALT
    ordner.mkdir(parents=True, exist_ok=True)
    (ordner / ".share.yml").write_text(
        "write:\n  - beta\n", encoding="utf-8"
    )
    store.rebuild_index()
    IDS_FILE.write_text(json.dumps(ids, indent=2))
    b2.log(f"Seed: {len(ids)} Items in alpha -> {IDS_FILE}")
    return 0


# --- Messung ------------------------------------------------------------------------------

RESULTS: list[dict] = []


def cell(name: str, ok: bool, detail: str) -> None:
    RESULTS.append({"name": name, "ok": bool(ok), "detail": detail})
    b2.log(("  OK  " if ok else "  FEHL") + f" {name}: {detail}")


def _item_files(space: str) -> list[Path]:
    return sorted((w.DATA_ROOT / space).rglob("*.md"))


def _find_item(item_id: str) -> Path | None:
    treffer = sorted((w.DATA_ROOT / "alpha").rglob(f"{item_id}__*.md"))
    return treffer[0] if treffer else None


def _version_in(path: Path | None) -> str:
    if path is None or not path.is_file():
        return ""
    for zeile in path.read_text(encoding="utf-8").splitlines():
        if zeile.startswith("version:"):
            return zeile.split(":", 1)[1].strip()
    return ""


def _git_log(limit: int = 5) -> list[str]:
    """Die Commit-Meldungen des Datenverzeichnisses — **read-only** (`git log`, kein Schreiben).
    Der Wegwerf-Datenbestand ist ein Git-Repo (der Server committet jeden Write)."""
    try:
        res = subprocess.run(
            ["git", "-C", str(w.DATA_ROOT), "log", f"-{limit}", "--pretty=%s"],
            capture_output=True, text=True, timeout=30, check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:  # pragma: no cover - Werkzeugfehler
        b2.log(f"git log fehlgeschlagen: {exc}")
        return []
    return [z for z in res.stdout.splitlines() if z.strip()]


def cmd_probe(_args: argparse.Namespace) -> int:
    ids = json.loads(IDS_FILE.read_text())
    alpha = json.loads(w.CREDS_FILE.read_text())["users"][0]
    assert alpha["space"] == "alpha"

    web = b2.Web(alpha)
    web.login()

    alt_datei = _find_item(ids["projekt"])
    version_vorher = _version_in(alt_datei)
    b2.log(f"Vorher: {alt_datei} (version={version_vorher})")

    # -- 1. Web-Rename --------------------------------------------------------------------
    r = web.c.patch(
        f"/api/v1/spaces/alpha/folders",
        headers={**web._h(), "Content-Type": "application/json"},
        json={"from": ORDNER_ALT, "to": ORDNER_NEU},
    )
    body = r.json() if r.status_code == 200 else {}
    cell("Web-Rename: HTTP 200", r.status_code == 200, f"HTTP {r.status_code} {r.text[:160]}")
    cell("Web-Rename: die Antwort nennt die Zahl der Items",
         body.get("items") == 1, f"items={body.get('items')!r} (erwartet 1)")

    # -- 2. Die Datei liegt am neuen Pfad -------------------------------------------------
    neu_datei = _find_item(ids["projekt"])
    cell("Die Datei liegt am neuen Pfad",
         neu_datei is not None and neu_datei.parent.name == ORDNER_NEU,
         f"neu={neu_datei}, alt={alt_datei}")
    cell("Der alte Ordner ist weg",
         not (w.DATA_ROOT / "alpha" / ORDNER_ALT).exists(),
         f"alt={(w.DATA_ROOT / 'alpha' / ORDNER_ALT)} existiert={(
             w.DATA_ROOT / 'alpha' / ORDNER_ALT).exists()}")

    # -- 3. Die Version ist unverändert ---------------------------------------------------
    version_nachher = _version_in(neu_datei)
    cell("Die Version ist unverändert",
         version_vorher == version_nachher and version_vorher != "",
         f"version={version_vorher!r} -> {version_nachher!r}")

    # -- 4. Die Freigabe wandert mit -------------------------------------------------------
    neu_share = w.DATA_ROOT / "alpha" / ORDNER_NEU / ".share.yml"
    alt_share = w.DATA_ROOT / "alpha" / ORDNER_ALT / ".share.yml"
    cell("Die Freigabe wandert mit",
         neu_share.is_file() and not alt_share.exists(),
         f"neu={neu_share.is_file()}, alt={alt_share.exists()}")

    # -- 5. Ein Commit --------------------------------------------------------------------
    log = _git_log(5)
    rename_commits = [z for z in log if z.startswith("rename-folder ")]
    cell("Ein Commit für das Umbenennen",
         len(rename_commits) == 1 and f"{ORDNER_ALT}→{ORDNER_NEU}" in rename_commits[0],
         f"Commit-Meldungen: {log[:4]}")

    # -- 6. Der Index stimmt ---------------------------------------------------------------
    items = web.c.get("/api/v1/items", params={"space": "alpha"})
    treffer = [i for i in items.json().get("items", []) if i.get("id") == ids["projekt"]]
    cell("Der Index meldet den neuen Ordner",
         len(treffer) == 1 and treffer[0].get("folder") == ORDNER_NEU,
         f"folder={treffer[0].get('folder')!r} (erwartet {ORDNER_NEU!r})" if treffer
         else "Item nicht im Index")

    # -- 7. Gegenlauf: das Ziel existiert --------------------------------------------------
    vorher = _find_item(ids["belegt"])
    r2 = web.c.patch(
        "/api/v1/spaces/alpha/folders",
        headers={**web._h(), "Content-Type": "application/json"},
        json={"from": ORDNER_BELEGT, "to": ORDNER_NEU},
    )
    body2 = r2.json() if r2.status_code != 200 else {}
    cell("Gegenlauf: ein existierendes Ziel wird abgelehnt",
         r2.status_code == 422, f"HTTP {r2.status_code}, error={body2.get('error')!r}")
    nachher = _find_item(ids["belegt"])
    cell("Gegenlauf: nichts bewegt",
         vorher is not None and nachher is not None and vorher == nachher
         and (w.DATA_ROOT / "alpha" / ORDNER_BELEGT).is_dir(),
         f"Datei {nachher}, Ordner {(w.DATA_ROOT / 'alpha' / ORDNER_BELEGT).is_dir()}")

    # -- 8. Ablehnung: das Ziel liegt unter dem alten Ordner ------------------------------
    r3 = web.c.patch(
        "/api/v1/spaces/alpha/folders",
        headers={**web._h(), "Content-Type": "application/json"},
        json={"from": ORDNER_NEU, "to": f"{ORDNER_NEU}/tiefer"},
    )
    cell("Ablehnung: das Ziel darf nicht unter dem alten Ordner liegen",
         r3.status_code == 422, f"HTTP {r3.status_code} {r3.text[:120]}")

    # -- 9. CSRF-Pflicht -------------------------------------------------------------------
    r4 = web.c.patch(
        "/api/v1/spaces/alpha/folders",
        headers={"Origin": BASE, "Content-Type": "application/json"},
        json={"from": ORDNER_NEU, "to": "anders"},
    )
    cell("Ohne CSRF-Token: 403",
         r4.status_code == 403, f"HTTP {r4.status_code}")
    cell("Ohne CSRF-Token: nichts bewegt",
         (w.DATA_ROOT / "alpha" / ORDNER_NEU).is_dir()
         and not (w.DATA_ROOT / "alpha" / "anders").exists(),
         f"{ORDNER_NEU} steht, 'anders' steht nicht")

    # -- Ausgabe --------------------------------------------------------------------------
    ok = all(c["ok"] for c in RESULTS)
    payload = {
        "probe": "p105_b9_rename_folder",
        "date": datetime.now(timezone.utc).isoformat(),
        "all_ok": ok,
        "zellen": len(RESULTS),
        "cells": RESULTS,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False))
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="P10.5 B9 `rename_folder` (Wegwerf 8799)")
    p.add_argument("cmd", choices=["setup", "start", "stop", "cleanup", "health", "probe"])
    args = p.parse_args(argv)
    return {
        "setup": cmd_setup, "start": w.cmd_start, "stop": w.cmd_stop,
        "cleanup": w.cmd_cleanup, "health": w.cmd_health, "probe": cmd_probe,
    }[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
