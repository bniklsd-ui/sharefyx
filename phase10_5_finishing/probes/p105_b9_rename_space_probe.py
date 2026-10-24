#!/usr/bin/env python3
"""P10.5 Block 9, Schritt 9.3 — RE-3 `rename_space` über die Web-API (P1-Öffnung 14).

**Wegwerf (Plan §2.3):** Port **8799**, eigene Wurzel `/tmp/opencode/sharefyx-wegwerf-p105-b9s`,
tmp-`DATA_ROOT`, tmp-`auth.sqlite3`, File-Keyring, Umgebung ohne `SHAREFYX_*`/`SFX_*`/`SPACE_*`,
Stopp **nur** über die PID-Datei (Hard Rule 9: nie `pkill -f`, nie der systemd-Dienst).

**Maschinerie:** `phase10_inventory/probes/p10_wegwerf.py` (Provisionierung, TLS-Start,
PID-Stopp) und der Web-Helfer aus dem Block-2-Probe `p105_b2_rights_probe.py` — **deren
Modul-Import setzt die Pfadkonstanten auf die B2-Wurzel**, deshalb werden sie hier **danach**
auf die eigene Wurzel umgebogen. Der Port bleibt 8799 (Plan §2.3), die Wurzel ist eine andere.

**Was gemessen wird (Abnahme P10.5-43):** ein **Team-Space** lässt sich umbenennen — Verzeichnis
**und** Frontmatter sagen danach den neuen Namen, die Version springt einmal, es ist **ein**
Commit — und die **Gegenläufe** gelten: ein **Home-Space** wird abgelehnt (P10.5-M), ein
existierender Zielname wird abgelehnt, und **nichts** bewegt.

| # | Zelle | Erwartung |
|---|---|---|
| 1 | Web-Rename eines Team-Spaces | HTTP 200, `from`/`to`/`items` |
| 2 | Das Verzeichnis steht unter dem neuen Namen | alt weg, neu da |
| 3 | Das **Frontmatter** sagt den neuen Space | `space: team-neu` in der Datei |
| 4 | Die **Version** springt genau einmal | `version: 1` → `version: 2` |
| 5 | **Ein Commit** | genau eine Meldung `rename-space team→team-neu` |
| 6 | Der Index stimmt | das Item meldet `space == "team-neu"` |
| 7 | Fremdverweise werden **gemeldet** | `orphan_refs` und `assignee_refs` sind gefüllt |
| 8 | **Gegenlauf**: Home-Space | **403**, nichts bewegt |
| 9 | **Gegenlauf**: existierender Zielname | **422**, nichts bewegt |

Die Unit-Ebene trägt die Regel-Gegenläufe (`phase1_storage/tests/test_store.py`), die Probe
trägt das **Zusammenspiel** von HTTP-Route, Kern und Platte.

Aufruf (Projekt-venv): `setup` → `start` → `probe` → `stop` (`cleanup` räumt die Wurzel ab).
Ausgabe: JSON auf stdout (Hard Rule 7) und `p105_b9_rename_space.json` daneben; Logs auf stderr.
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
ROOT = Path("/tmp/opencode/sharefyx-wegwerf-p105-b9s")
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
OUT_JSON = Path(__file__).with_name("p105_b9_rename_space.json")
BASE = w.BASE_URL  # https://127.0.0.1:8799

TEAM_ALT = "team"
TEAM_NEU = "team-neu"


# --- Setup --------------------------------------------------------------------------------

def cmd_setup(_args: argparse.Namespace) -> int:
    w.cmd_setup(_args)  # zwei Principale alpha + beta in der tmp-auth.sqlite3
    w._install_keyring()
    w._spacectl("create-space", "alpha")

    from storage.acl import create_space, write_share_file
    from storage.store import Store

    # Der **Team-Space**: er gehoert niemandem, sein Name steht in keiner Auth-Zeile.
    create_space(w.DATA_ROOT, TEAM_ALT)
    write_share_file(w.DATA_ROOT, TEAM_ALT, {"write": ["alpha"]})

    store = Store(str(w.DATA_ROOT), now_fn=lambda: datetime.now(timezone.utc), git=False)
    ids = {}
    ids["team"] = store.create(
        TEAM_ALT, type="note", title="Team-Notiz", body="Wegwerf P10.5 B9.3.",
        assignee=TEAM_ALT,
    ).id
    # Eine **fremde** `.share.yml`, die den Team-Space nennt — sie darf beim Umbenennen
    # **nicht** angefasst werden, nur gemeldet.
    fremd = w.DATA_ROOT / "alpha" / "fremd"
    fremd.mkdir(parents=True, exist_ok=True)
    (fremd / ".share.yml").write_text(f"read: [{TEAM_ALT}]\n", encoding="utf-8")
    store.rebuild_index()
    IDS_FILE.write_text(json.dumps(ids, indent=2))
    b2.log(f"Seed: Team-Space {TEAM_ALT} mit {len(ids)} Item(s) -> {IDS_FILE}")
    return 0


# --- Messung ------------------------------------------------------------------------------

RESULTS: list[dict] = []


def cell(name: str, ok: bool, detail: str) -> None:
    RESULTS.append({"name": name, "ok": bool(ok), "detail": detail})
    b2.log(("  OK  " if ok else "  FEHL") + f" {name}: {detail}")


def _find_item(item_id: str) -> Path | None:
    treffer = sorted((w.DATA_ROOT).rglob(f"{item_id}__*.md"))
    return treffer[0] if treffer else None


def _feld(text: str, feld: str) -> str:
    for zeile in text.splitlines():
        if zeile.startswith(feld + ":"):
            return zeile.split(":", 1)[1].strip()
    return ""


def _git_log(limit: int = 5) -> list[str]:
    """Die Commit-Meldungen des Datenverzeichnisses — **read-only**."""
    try:
        res = subprocess.run(
            ["git", "-C", str(w.DATA_ROOT), "log", f"-{limit}", "--pretty=%s"],
            capture_output=True, text=True, timeout=30, check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:  # pragma: no cover
        b2.log(f"git log fehlgeschlagen: {exc}")
        return []
    return [z for z in res.stdout.splitlines() if z.strip()]


def cmd_probe(_args: argparse.Namespace) -> int:
    ids = json.loads(IDS_FILE.read_text())
    alpha = json.loads(w.CREDS_FILE.read_text())["users"][0]
    assert alpha["space"] == "alpha"

    web = b2.Web(alpha)
    web.login()

    datei_vorher = _find_item(ids["team"])
    text_vorher = datei_vorher.read_text(encoding="utf-8") if datei_vorher else ""
    version_vorher = _feld(text_vorher, "version")
    b2.log(f"Vorher: {datei_vorher} (space={_feld(text_vorher, 'space')}, version={version_vorher})")

    # -- 1. Web-Rename des Team-Spaces ----------------------------------------------------
    r = web.c.patch(
        f"/api/v1/spaces/{TEAM_ALT}",
        headers={**web._h(), "Content-Type": "application/json"},
        json={"name": TEAM_NEU},
    )
    body = r.json() if r.status_code == 200 else {}
    cell("Web-Rename: HTTP 200", r.status_code == 200, f"HTTP {r.status_code} {r.text[:160]}")
    cell("Web-Rename: die Antwort nennt alt und neu",
         body.get("from") == TEAM_ALT and body.get("to") == TEAM_NEU,
         f"from={body.get('from')!r}, to={body.get('to')!r}")
    cell("Web-Rename: die Antwort nennt die Zahl der Items",
         body.get("items") == 1, f"items={body.get('items')!r} (erwartet 1)")

    # -- 2. Das Verzeichnis ist gewandert --------------------------------------------------
    cell("Das Verzeichnis steht unter dem neuen Namen",
         (w.DATA_ROOT / TEAM_NEU).is_dir() and not (w.DATA_ROOT / TEAM_ALT).exists(),
         f"neu={(w.DATA_ROOT / TEAM_NEU).is_dir()}, alt={(w.DATA_ROOT / TEAM_ALT).exists()}")

    # -- 3./4. Frontmatter und Version -----------------------------------------------------
    datei_nachher = _find_item(ids["team"])
    text_nachher = datei_nachher.read_text(encoding="utf-8") if datei_nachher else ""
    cell("Das Frontmatter nennt den neuen Space",
         _feld(text_nachher, "space") == TEAM_NEU,
         f"space={_feld(text_nachher, 'space')!r} (erwartet {TEAM_NEU!r})")
    version_nachher = _feld(text_nachher, "version")
    cell("Die Version springt genau einmal",
         version_vorher == "1" and version_nachher == "2",
         f"version {version_vorher!r} -> {version_nachher!r}")

    # -- 5. Ein Commit ---------------------------------------------------------------------
    log = _git_log(5)
    rename_commits = [z for z in log if z.startswith("rename-space ")]
    cell("Ein Commit für das Umbenennen",
         len(rename_commits) == 1 and f"{TEAM_ALT}→{TEAM_NEU}" in rename_commits[0],
         f"Commit-Meldungen: {log[:4]}")

    # -- 6. Der Index stimmt ---------------------------------------------------------------
    items = web.c.get("/api/v1/items", params={"space": TEAM_NEU})
    treffer = [i for i in items.json().get("items", []) if i.get("id") == ids["team"]]
    cell("Der Index meldet den neuen Space",
         len(treffer) == 1 and treffer[0].get("space") == TEAM_NEU,
         f"space={treffer[0].get('space')!r} (erwartet {TEAM_NEU!r})" if treffer
         else "Item nicht im Index")

    # -- 7. Fremdverweise werden gemeldet, nicht angefasst ----------------------------------
    fremd = w.DATA_ROOT / "alpha" / "fremd" / ".share.yml"
    cell("Die fremde .share.yml wird gemeldet",
         bool(body.get("orphan_refs")), f"orphan_refs={body.get('orphan_refs')!r}")
    cell("Die fremde .share.yml wird nicht angefasst",
         fremd.is_file() and TEAM_ALT in fremd.read_text(encoding="utf-8"),
         f"{fremd} unveraendert")
    cell("Das Item mit `assignee` wird gemeldet",
         body.get("assignee_refs") == [ids["team"]],
         f"assignee_refs={body.get('assignee_refs')!r}")

    # -- 8. Gegenlauf: ein Home-Space ------------------------------------------------------
    r2 = web.c.patch(
        "/api/v1/spaces/alpha",
        headers={**web._h(), "Content-Type": "application/json"},
        json={"name": "alpha-neu"},
    )
    cell("Gegenlauf: ein Home-Space wird abgelehnt",
         r2.status_code == 403, f"HTTP {r2.status_code} {r2.text[:120]}")
    cell("Gegenlauf: der Home-Space steht noch",
         (w.DATA_ROOT / "alpha").is_dir() and not (w.DATA_ROOT / "alpha-neu").exists(),
         f"alpha={(w.DATA_ROOT / 'alpha').is_dir()}, alpha-neu={(w.DATA_ROOT / 'alpha-neu').exists()}")

    # -- 9. Gegenlauf: der Zielname ist vergeben -------------------------------------------
    r3 = web.c.patch(
        f"/api/v1/spaces/{TEAM_NEU}",
        headers={**web._h(), "Content-Type": "application/json"},
        json={"name": "alpha"},
    )
    cell("Gegenlauf: ein vergebener Zielname wird abgelehnt",
         r3.status_code == 422, f"HTTP {r3.status_code} {r3.text[:120]}")
    cell("Gegenlauf: nichts bewegt",
         (w.DATA_ROOT / TEAM_NEU).is_dir() and not (w.DATA_ROOT / "alpha-neu").exists(),
         f"{TEAM_NEU} steht")

    # -- Ausgabe --------------------------------------------------------------------------
    ok = all(c["ok"] for c in RESULTS)
    payload = {
        "probe": "p105_b9_rename_space",
        "date": datetime.now(timezone.utc).isoformat(),
        "all_ok": ok,
        "zellen": len(RESULTS),
        "cells": RESULTS,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False))
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="P10.5 B9 `rename_space` (Wegwerf 8799)")
    p.add_argument("cmd", choices=["setup", "start", "stop", "cleanup", "health", "probe"])
    args = p.parse_args(argv)
    return {
        "setup": cmd_setup, "start": w.cmd_start, "stop": w.cmd_stop,
        "cleanup": w.cmd_cleanup, "health": w.cmd_health, "probe": cmd_probe,
    }[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
