#!/usr/bin/env python3
"""P10.5 Block 9, Schritt 9.1 — RE-7 `created_by` über Web und MCP (P1-Öffnung 12).

**Wegwerf (Plan §2.3):** Port **8799**, eigene Wurzel `/tmp/opencode/sharefyx-wegwerf-p105-b9`,
tmp-`DATA_ROOT`, tmp-`auth.sqlite3`, File-Keyring, Umgebung ohne `SHAREFYX_*`/`SFX_*`/`SPACE_*`,
Stopp **nur** über die PID-Datei (Hard Rule 9: nie `pkill -f`, nie der systemd-Dienst).

**Maschinerie:** `phase10_inventory/probes/p10_wegwerf.py` (Provisionierung, TLS-Start,
PID-Stopp). Die Web- und MCP-Helfer (Login mit TOTP, OAuth-Dance) kommen aus dem Block-2-Probe
`p105_b2_rights_probe.py` — **deren Modul-Import setzt die Pfadkonstanten auf die B2-Wurzel**,
deshalb werden sie hier **danach** auf die eigene Wurzel umgebogen. Der Port bleibt 8799 (Plan
§2.3), die Wurzel ist eine andere — die B2- und B3-Instanzen müssen dafür **beendet** sein.

**Was gemessen wird (Abnahme P10.5-41):** `created_by` ist auf neuen Items **über Web und über
MCP** sichtbar, und der Altbestand zeigt **nichts** — es wird nichts erfunden (Lock P10.5-W).

| # | Zelle | Erwartung |
|---|---|---|
| 1 | Web-Anlage: die Antwort nennt den Anleger | `created_by == "alpha"` |
| 2 | Web-Anlage: die Datei auf der Platte nennt ihn | `created_by: alpha` in der Datei |
| 3 | MCP-Anlage: `get_item_meta` nennt ihn | `created_by == "alpha"` |
| 4 | MCP-Anlage: die Datei auf der Platte nennt ihn | `created_by: alpha` in der Datei |
| 5 | **Altbestand**: ohne Feld | `created_by == ""` **und** keine Zeile in der Datei |
| 6 | **Altbestand nach einem Write** | keine Zeile in der Datei (nichts erfunden) |
| 7 | Fälschung per PATCH | **422**, die Datei bleibt unberührt |
| 8 | Fälschung per POST | der Wert bleibt `alpha` (der POST filtert das Feld weg) |

Der **Gegenlauf** zu diesem Block liegt nicht hier, sondern in der Unit-Ebene:
`phase10_5_finishing/tests/test_created_by_rules.py` patcht **je eine Regel** im echten Code
und muss **genau die** zugehörige Zelle rot machen — ein Wächter ohne Gegenlauf beweist nichts.

Aufruf (Projekt-venv): `setup` → `start` → `probe` → `stop` (`cleanup` räumt die Wurzel ab).
Ausgabe: JSON auf stdout (Hard Rule 7) und `p105_b9_created_by.json` daneben; Logs auf stderr.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "phase10_inventory" / "probes"))
sys.path.insert(0, str(REPO_ROOT / "phase10_5_finishing" / "probes"))

import p10_wegwerf as w  # noqa: E402
import p105_b2_rights_probe as b2  # noqa: E402  (setzt w.* auf die B2-Wurzel — s. u.)

# --- eigene Wurzel (überschreibt die B2-Konstanten aus dem Import) ------------------------
ROOT = Path("/tmp/opencode/sharefyx-wegwerf-p105-b9")
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
OUT_JSON = Path(__file__).with_name("p105_b9_created_by.json")
BASE = w.BASE_URL  # https://127.0.0.1:8799

# --- Setup --------------------------------------------------------------------------------

SEED = [
    # Der **Altbestand**: ohne Akteur angelegt — das Item bekommt das Feld nie (P10.5-W, kein
    # Backfill). Genau so sieht ein Item aus, das vor dem Deploy existierte.
    ("altbestand", "alpha", "Altbestand"),
    # Ein Item **mit** Akteur: der Kern setzt `created_by` daraus.
    ("mit_akteur", "alpha", "Mit Akteur"),
]


def cmd_setup(_args: argparse.Namespace) -> int:
    w.cmd_setup(_args)  # zwei Principale alpha + beta in der tmp-auth.sqlite3
    w._install_keyring()
    w._spacectl("create-space", "alpha")

    from storage.store import Store
    store = Store(str(w.DATA_ROOT), now_fn=lambda: datetime.now(timezone.utc), git=False)
    ids = {}
    for key, space, title in SEED:
        # **ohne** `actor` — der Altbestand-Zustand. Der Kern schreibt dann kein Feld in die
        # Datei, und genau das ist die Aussage, die Zelle 5 und 6 belegen.
        ids[key] = store.create(space, type="note", title=title, body="Wegwerf P10.5 B9.").id
    store.rebuild_index()
    IDS_FILE.write_text(json.dumps(ids, indent=2))
    b2.log(f"Seed: {len(ids)} Items in alpha -> {IDS_FILE}")
    return 0


# --- Messung ------------------------------------------------------------------------------

RESULTS: list[dict] = []


def cell(name: str, ok: bool, detail: str) -> None:
    RESULTS.append({"name": name, "ok": bool(ok), "detail": detail})
    b2.log(("  OK  " if ok else "  FEHL") + f" {name}: {detail}")


def _item_file(space: str, item_id: str) -> Path:
    """Die Item-Datei auf der Platte — **über die ID im Dateinamen**, nicht geraten: der
    Dateiname traegt zusaetzlich den Slug des Titels, und ein hart kodierter Name waere still
    falsch (der Slug aendert sich beim Titelwechsel). Das `rglob` findet die Datei auch in
    Unterordnern."""
    treffer = sorted((w.DATA_ROOT / space).rglob(f"{item_id}__*.md"))
    return treffer[0] if treffer else ROOT / "gibtsnicht.md"


def cmd_probe(_args: argparse.Namespace) -> int:
    ids = json.loads(IDS_FILE.read_text())
    alpha = json.loads(w.CREDS_FILE.read_text())["users"][0]
    assert alpha["space"] == "alpha"

    web = b2.Web(alpha)
    web.login()
    mcp = b2.Mcp(alpha)
    mcp.oauth()

    # -- 1./2. Web-Anlage ------------------------------------------------------------------
    r = web.c.post(
        "/api/v1/items",
        headers={**web._h(), "Content-Type": "application/json"},
        json={"type": "task", "title": "Web-Anlage"},
    )
    web_body = r.json() if r.status_code == 201 else {}
    cell("Web-Anlage: HTTP 201", r.status_code == 201, f"HTTP {r.status_code}")
    cell("Web-Anlage: die Antwort nennt den Anleger",
         web_body.get("created_by") == "alpha",
         f"created_by={web_body.get('created_by')!r} (erwartet 'alpha')")
    web_file = _item_file("alpha", web_body.get("id", ""))
    web_text = web_file.read_text(encoding="utf-8") if web_file.is_file() else ""
    cell("Web-Anlage: die Datei auf der Platte nennt ihn",
         "created_by: alpha" in web_text,
         f"Datei {web_file.name}, {len(web_text)} B")

    # -- 3./4. MCP-Anlage ------------------------------------------------------------------
    out = mcp.tool("create_item", type="task", title="MCP-Anlage", body="Wegwerf.")
    mcp_id = ""
    try:
        quittung = json.loads(out["text"])
        mcp_id = quittung.get("id", "")
    except (ValueError, TypeError):
        mcp_id = ""
    cell("MCP-Anlage: die Quittung nennt eine ID", bool(mcp_id),
         f"is_error={out['is_error']}, id={mcp_id or '—'}")
    meta = mcp.tool("get_item_meta", item_id=mcp_id) if mcp_id else {"text": "", "is_error": True}
    try:
        meta_json = json.loads(meta["text"])
    except (ValueError, TypeError):
        meta_json = {}
    cell("MCP-Anlage: `get_item_meta` nennt den Anleger",
         meta_json.get("created_by") == "alpha",
         f"created_by={meta_json.get('created_by')!r} (erwartet 'alpha')")
    mcp_file = _item_file("alpha", mcp_id)
    mcp_text = mcp_file.read_text(encoding="utf-8") if mcp_file.is_file() else ""
    cell("MCP-Anlage: die Datei auf der Platte nennt ihn",
         "created_by: alpha" in mcp_text,
         f"Datei {mcp_file.name}, {len(mcp_text)} B")

    # -- 5./6. Der Altbestand: nichts erfunden ---------------------------------------------
    alt_id = ids["altbestand"]
    alt_meta = mcp.tool("get_item_meta", item_id=alt_id)
    try:
        alt_json = json.loads(alt_meta["text"])
    except (ValueError, TypeError):
        alt_json = {}
    cell("Altbestand: `get_item_meta` nennt keinen Anleger",
         alt_json.get("created_by") == "",
         f"created_by={alt_json.get('created_by')!r} (erwartet '')")
    alt_file = _item_file("alpha", alt_id)
    alt_text = alt_file.read_text(encoding="utf-8") if alt_file.is_file() else ""
    cell("Altbestand: die Datei trägt keine Zeile", bool(alt_text) and "created_by" not in alt_text,
         f"Datei {alt_file.name}, {len(alt_text)} B")
    # Und jetzt ein schreibender Zugriff: es darf **keine** leere Zeile entstehen.
    # **Der Pfad wird neu geholt** — der Titelwechsel benennt die Datei um (Slug!), ein zwischengespeicherter
    # Pfad zeigte danach ins Leere, und „`created_by` nicht in ''" waere ein **vakuoser** Treffer
    # (dieselbe Falle, die der B3-Probe beim Asset-Pfad den leeren Treffer ersetzte).
    patch = web.patch(alt_id, title="Altbestand (neu)")
    alt_file2 = _item_file("alpha", alt_id)
    alt_text2 = alt_file2.read_text(encoding="utf-8") if alt_file2.is_file() else ""
    cell("Altbestand: nach einem Write immer noch keine Zeile",
         bool(alt_text2) and "created_by" not in alt_text2 and patch["status"] == 200,
         f"HTTP {patch['status']}, Datei {alt_file2.name}, {len(alt_text2)} B")

    # -- 7./8. Fälschung ------------------------------------------------------------------
    forged = web.patch(web_body.get("id", ""), created_by="beta")
    forged_body = json.loads(forged["body"]) if forged["body"].startswith("{") else {}
    cell("Fälschung per PATCH: 422", forged["status"] == 422,
         f"HTTP {forged['status']}, error={forged_body.get('error')!r}")
    web_text2 = web_file.read_text(encoding="utf-8") if web_file.is_file() else ""
    cell("Fälschung per PATCH: die Datei bleibt unberührt",
         "created_by: beta" not in web_text2 and "created_by: alpha" in web_text2,
         f"Datei {web_file.name}")

    r = web.c.post(
        "/api/v1/items",
        headers={**web._h(), "Content-Type": "application/json"},
        json={"type": "task", "title": "Erfunden", "created_by": "beta"},
    )
    gefaelscht = r.json() if r.status_code == 201 else {}
    cell("Fälschung per POST: der Wert bleibt der eingeloggte Mensch",
         gefaelscht.get("created_by") == "alpha",
         f"created_by={gefaelscht.get('created_by')!r} (erwartet 'alpha')")

    # -- Ausgabe --------------------------------------------------------------------------
    ok = all(c["ok"] for c in RESULTS)
    payload = {
        "probe": "p105_b9_created_by",
        "date": datetime.now(timezone.utc).isoformat(),
        "all_ok": ok,
        "zellen": len(RESULTS),
        "cells": RESULTS,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False))
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="P10.5 B9 `created_by` (Wegwerf 8799)")
    p.add_argument("cmd", choices=["setup", "start", "stop", "cleanup", "health", "probe"])
    args = p.parse_args(argv)
    return {
        "setup": cmd_setup, "start": w.cmd_start, "stop": w.cmd_stop,
        "cleanup": w.cmd_cleanup, "health": w.cmd_health, "probe": cmd_probe,
    }[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
