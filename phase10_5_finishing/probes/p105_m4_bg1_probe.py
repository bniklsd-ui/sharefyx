#!/usr/bin/env python3
"""P10.5 Block 2, Schritt 2.5 — M4 erneut (BG-1, Abnahme P10.5-8), gegen die Wegwerf-Instanz von
`p105_b2_rights_probe.py` (Port 8799, TLS).

Nutzt die Messschritte von `phase10_inventory/probes/p10_m4_bg1_probe.py` unverändert (Login,
`/overview` per Route um 4 s verzögert, Panel sofort öffnen, Zeilen zählen), dreht aber drei
Dinge, ohne die P10-Datei anzufassen (deren JSON und Screenshots sind P10-Belege):

1. **TLS:** die P10-Probe spricht `http://`, die Wegwerf-Instanz `https://` (CSRF-Origin,
   Vorlage `p10_wegwerf.py`) — Kontext mit `ignore_https_errors`.
2. **Bestehensregel umgedreht:** P10 bestand, wenn der Fehler **auftrat** (0 Zeilen nach der
   Verzögerung). Hier besteht die Probe, wenn die Liste sich **ohne** erneutes Öffnen füllt.
3. **Zeilenzahl aus dem Seed:** alpha schreibt in alpha, beta (Home von B mit `write: [alpha]`)
   und gamma (Team) → **3** Zeilen, nicht die 2 des P10-Seeds (dort war beta nur lesbar). Der
   Plan nennt „2 Zeilen", weil er den P10-Seed meinte; Abweichung benannt, nicht versteckt.

Aufruf mit dem Playwright-venv (`~/.claude-code-tools/e2e-venv/bin/python`). Ausgabe: JSON auf
stdout, `p105_m4_bg1.json` daneben; Screenshots in den Scratch unter der Wegwerf-Wurzel.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "phase10_inventory" / "probes"))
import p10_m4_bg1_probe as m4  # noqa: E402

ROOT = Path("/tmp/opencode/sharefyx-wegwerf-p105-b2")
m4.BASE_URL = "https://127.0.0.1:8799"
m4.SHOT_DIR = ROOT
OUT_JSON = Path(__file__).with_name("p105_m4_bg1.json")
EXPECTED_WRITABLE = 3  # alpha + beta (write:) + gamma (Team); delta ist nur lesbar


def main() -> int:
    creds = json.loads((ROOT / "credentials.json").read_text())["users"][0]
    assert creds["space"] == "alpha"
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        context = browser.new_context(viewport={"width": 1440, "height": 900},
                                      ignore_https_errors=True)
        page = context.new_page()
        m4.login(page, m4.BASE_URL, creds["space"], creds["password"], creds["otpauth_uri"])
        delayed = m4.run_delayed(page)
        immediate = m4.run_immediate(page)
        browser.close()
    sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=REPO_ROOT,
                         capture_output=True, text=True).stdout.strip()
    result = {
        "probe": "p105_m4_bg1", "head": sha, "delay_s": m4.DELAY_S,
        "expected_writable_spaces": EXPECTED_WRITABLE,
        "delayed_path": delayed, "immediate_path": immediate,
        # P10.5-8: beim Öffnen leer (die Verzögerung wirkt), danach voll — ohne neu zu öffnen.
        "bg1_fixed": (delayed["count_on_open"] == 0
                      and delayed["count_after_delay_resolved"] == EXPECTED_WRITABLE
                      and immediate["count_on_open"] == EXPECTED_WRITABLE),
    }
    OUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["bg1_fixed"] else 1


if __name__ == "__main__":
    sys.exit(main())
