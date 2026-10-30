#!/usr/bin/env python3
"""P10.5 Block 15.5b — der Space-Dialog zeigt Hinzufügen/Entfernen nur, wer den Space verwaltet.

**Wegwerf:** Port 8799, eigene Wurzel `/tmp/opencode/sharefyx-wegwerf-p105-b155b`, tmp-`DATA_ROOT`,
tmp-`auth.sqlite3`, File-Keyring, Umgebung ohne `SHAREFYX_*`/`SFX_*`; Stopp nur über die
PID-Datei (Hard Rule 9). Maschinerie aus `phase10_inventory/probes/p10_wegwerf.py`.

**Datenlage (Akteur `alpha`):** `beta` = Home-Space von B, `read:`+`write: [alpha]`, `read: [carol]`
(fremder Home-Space mit Schreibrecht — dort verwaltet `alpha` **nicht**, 15.4) · `gamma` =
Team-Space, `write: [alpha]`, `read: [carol]` (dort verwaltet `alpha`).

**Zellen:** `gast_formular` (beta: Hinzufügen versteckt) · `gast_knoepfe` (beta: nur `alpha` hat
„Entfernen“) · `team_verwalten` (gamma: Formular und alle Knöpfe da) · `austragen` (beta: Klick
auf den eigenen Knopf ⇒ Toast „Ausgetragen“, Detail zu, `beta` weg aus der Liste, `alpha` weg aus
`beta/.share.yml`).

Aufruf: `setup` · `start` · `stop` · `cleanup` mit `.venv/bin/python`; `browser` mit
`~/.claude-code-tools/e2e-venv/bin/python`. Ausgabe JSON auf stdout und
`p105_b15_5b_gast_knoepfe.json` daneben.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

PROBE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PROBE_DIR.parents[1]
ROOT = Path("/tmp/opencode/sharefyx-wegwerf-p105-b155b")
OUT_JSON = PROBE_DIR / "p105_b15_5b_gast_knoepfe.json"
BASE = "https://127.0.0.1:8799"


def _w():
    sys.path.insert(0, str(REPO_ROOT / "phase10_inventory" / "probes"))
    import p10_wegwerf as w

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
    return w


def cmd_setup(args) -> int:
    w = _w()
    w.cmd_setup(args)  # Principale alpha + beta
    for space in ("alpha", "beta", "carol", "gamma"):
        w._spacectl("create-space", space)
    for grant in (("--read", "beta", "alpha"), ("--write", "beta", "alpha"),
                  ("--read", "beta", "carol"), ("--write", "gamma", "alpha"),
                  ("--read", "gamma", "carol")):
        w._spacectl("add-member", *grant)
    return 0


def _login(page) -> None:
    sys.path.insert(0, str(REPO_ROOT / "phase10_inventory" / "probes"))
    from p10_m4_bg1_probe import login

    creds = json.loads((ROOT / "credentials.json").read_text())
    user = next(u for u in creds["users"] if u["space"] == "alpha")
    login(page, BASE, "alpha", user["password"], user["otpauth_uri"])


def _open_space(page, name: str) -> None:
    page.locator(f'.settings-space-row[data-space="{name}"]').click()
    page.wait_for_function(
        "n => document.getElementById('space-detail-name').textContent === n", arg=name
    )
    time.sleep(0.3)


def _rows(page) -> dict[str, bool]:
    return page.evaluate(
        """() => Object.fromEntries([...document.querySelectorAll('#space-member-list li')]
             .map(li => [li.querySelector('span').textContent.split(' ')[0],
                         !!li.querySelector('button')]))"""
    )


def cmd_browser(_args) -> int:
    from playwright.sync_api import sync_playwright

    cells: dict[str, dict] = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_context(ignore_https_errors=True,
                                   viewport={"width": 1600, "height": 1000}).new_page()
        _login(page)
        page.goto(f"{BASE}/ui/", wait_until="networkidle")
        sys.path.insert(0, str(REPO_ROOT / "phase10_inventory" / "probes"))
        from p10_m4_bg1_probe import _dismiss_banner, _open_spaces_panel
        _dismiss_banner(page)
        _open_spaces_panel(page)
        time.sleep(1.0)

        _open_space(page, "beta")
        # Der Knopf, nicht der neue Container: den gibt es auch im alten Markup — sonst wäre die
        # Zelle im Gegenlauf grün, weil ein fehlendes Element als „versteckt“ zählt.
        hidden = not page.locator("#space-member-add-submit").is_visible()
        cells["gast_formular"] = {"ok": hidden, "hinzufuegen_versteckt": hidden}
        rows = _rows(page)
        cells["gast_knoepfe"] = {"ok": rows == {"alpha": True, "carol": False}, "zeilen": rows}

        _open_space(page, "gamma")
        visible = page.locator("#space-member-add-submit").is_visible()
        rows = _rows(page)
        cells["team_verwalten"] = {
            "ok": visible and rows == {"alpha": True, "carol": True},
            "hinzufuegen_sichtbar": visible, "zeilen": rows,
        }

        _open_space(page, "beta")
        page.locator("#space-member-list li", has_text="alpha").locator("button").click()
        time.sleep(2.0)
        toast = page.locator("text=Ausgetragen · beta").count() > 0
        detail_zu = page.locator("#settings-space-detail").is_hidden()
        beta_in_liste = page.locator('.settings-space-row[data-space="beta"]').count()
        share = (ROOT / "data" / "beta" / ".share.yml").read_text()
        cells["austragen"] = {
            "ok": toast and detail_zu and beta_in_liste == 0 and "alpha" not in share,
            "toast": toast, "detail_zu": detail_zu, "beta_zeilen": beta_in_liste,
            "share_yml": share,
        }
        page.screenshot(path=str(ROOT / "nach_austragen.png"))
        browser.close()

    result = {"cells": cells, "alle_gruen": all(c["ok"] for c in cells.values())}
    OUT_JSON.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["alle_gruen"] else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd", choices=["setup", "start", "stop", "cleanup", "browser"])
    args = parser.parse_args()
    if args.cmd in ("start", "stop", "cleanup"):
        return getattr(_w(), f"cmd_{args.cmd}")(args)
    return {"setup": cmd_setup, "browser": cmd_browser}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
