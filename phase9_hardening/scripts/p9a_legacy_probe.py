#!/usr/bin/env python3
"""P9 Step A — Browser-Probe des Übergangsfensters der alten Adresse (2026-10-01).

Baut auf der TLS-Wegwerf-Instanz aus Step G auf (`p9_step_g_wegwerf.py`, Port 18775, eigene
DATA_ROOT/auth.sqlite3/Keyring unter /tmp) und dreht nur zwei Dinge: `SPACE_PUBLIC_BASE_URL`
zeigt auf eine **andere** Adresse (die „neue"), und die Adresse, unter der der Browser die
Instanz aufruft, ist als `SPACE_UI_LEGACY_ORIGIN` konfiguriert. Damit ist der Browser exakt in
der Lage eines Nutzers, der nach A7 noch das alte Lesezeichen benutzt.

Drei Läufe, je ein Neustart der Wegwerf-Instanz (über die PID-Datei, Hard Rule 9):

  unbefristet LEGACY_UNTIL = open         → Dialog „bis auf Weiteres", kein Datum, Schreiben 201
                                            (2026-10-05, Firmen-VPN erreicht die neue Adresse nicht)
  offen       LEGACY_UNTIL = heute + 14   → Dialog „bis einschließlich …", Schreiben 201
  abgelaufen  LEGACY_UNTIL = gestern      → Dialog „nur noch lesbar", Schreiben 403

    ~/.claude-code-tools/e2e-venv/bin/python phase9_hardening/scripts/p9a_legacy_probe.py
"""
from __future__ import annotations

import datetime
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[1]
SHOTS = REPO_ROOT / "docs" / "screenshots"
NEW_URL = "https://sharefyx.example.invalid"


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


wegwerf = _load("p9_step_g_wegwerf")
check = _load("p9_step_g_self_check")
RESULTS: list[tuple[str, bool, str]] = []


def pruefe(name: str, ok: bool, detail: str = "") -> None:
    RESULTS.append((name, ok, detail))
    print(f"[{'OK  ' if ok else 'FAIL'}] {name}  {detail}")


def _run_instance(until: str) -> None:
    """Start über das Wegwerf-Skript als Subprozess der Projekt-venv (dort liegen die
    authserver-Abhängigkeiten), mit den zwei gedrehten Variablen in der Umgebung."""
    env = os.environ.copy()
    env.update({
        "SPACE_UI_LEGACY_ORIGIN": wegwerf.BASE_URL,
        "SPACE_UI_LEGACY_UNTIL": until,
        "P9A_PUBLIC_BASE_URL": NEW_URL,
    })
    code = (
        "import importlib.util,sys;"
        f"s=importlib.util.spec_from_file_location('w','{HERE / 'p9_step_g_wegwerf.py'}');"
        "m=importlib.util.module_from_spec(s);s.loader.exec_module(m);"
        "import os;m.PUBLIC_BASE_URL=os.environ['P9A_PUBLIC_BASE_URL'];sys.exit(m._start())"
    )
    subprocess.run([str(REPO_ROOT / ".venv/bin/python"), "-c", code], env=env, cwd=REPO_ROOT,
                   check=True)


def _stop() -> None:
    subprocess.run([str(REPO_ROOT / ".venv/bin/python"), str(HERE / "p9_step_g_wegwerf.py"), "stop"],
                   cwd=REPO_ROOT, check=True)


def _probe(pw, label: str, *, writable: bool, want: str) -> None:
    creds = json.loads(wegwerf.CREDS_FILE.read_text())
    base = wegwerf.BASE_URL
    browser = pw.chromium.launch()
    page = browser.new_context(viewport={"width": 1440, "height": 900},
                               ignore_https_errors=True).new_page()
    pruefe(f"{label}: Login", check.login(page, base, creds["password"], creds["otpauth_uri"]))
    page.goto(f"{base}/ui/", wait_until="networkidle")
    dialog = page.locator("#legacy-host-dialog")
    pruefe(f"{label}: Dialog beim Laden sichtbar", dialog.is_visible())
    text = page.locator("#legacy-host-text").inner_text()
    pruefe(f"{label}: Text passt", want in text and NEW_URL in text, repr(text))
    href = page.locator("#legacy-host-link").get_attribute("href")
    pruefe(f"{label}: Link zeigt auf die neue Adresse", href == f"{NEW_URL}/ui/", repr(href))
    page.screenshot(path=str(SHOTS / f"p9a_legacy_{label}.png"))

    page.keyboard.press("Escape")
    pruefe(f"{label}: ESC schließt", not dialog.is_visible())
    page.reload(wait_until="networkidle")
    pruefe(f"{label}: kommt beim nächsten Laden wieder", dialog.is_visible())
    page.locator("#legacy-host-close").click()
    pruefe(f"{label}: Knopf schließt", not dialog.is_visible())

    status = page.evaluate("""() => fetch('/api/v1/items', {method: 'POST',
        headers: {'Content-Type': 'application/json',
                  'X-CSRF-Token': sessionStorage.getItem('sfx:csrf')},
        body: JSON.stringify({type: 'note', title: 'Fensterprobe', body: 'x'})}).then(r => r.status)""")
    erwartet = 201 if writable else 403
    pruefe(f"{label}: Schreiben über die alte Origin → {erwartet}", status == erwartet, f"war {status}")
    browser.close()


def main() -> int:
    today = datetime.date.today()
    with sync_playwright() as pw:
        offen = today + datetime.timedelta(days=14)
        for label, writable, until, want in (
            ("unbefristet", True, "open", "bis auf Weiteres"),
            ("offen", True, offen.isoformat(), offen.strftime("%d.%m.%Y")),
            ("abgelaufen", False, (today - datetime.timedelta(days=1)).isoformat(), "nur noch über"),
        ):
            _run_instance(until)
            try:
                _probe(pw, label, writable=writable, want=want)
            finally:
                _stop()
    failed = [r for r in RESULTS if not r[1]]
    print(f"\n{len(RESULTS) - len(failed)}/{len(RESULTS)} grün")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
