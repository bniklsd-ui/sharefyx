#!/usr/bin/env python3
"""P10-J Lauf 1 (P10.5-27) als **Wegwerf-Generalprobe**: opencode + **echtes** Modell (MiniMax M3.1 Flash)
gegen eine Wegwerf-Instanz — der volle Fluss vollautomatisch: Registrierung → `/oauth/authorize` (Passwort + TOTP
im echten Chromium) → Token → das Modell ruft `list_spaces` selbst auf.

Unterschied zu `p105_b6_opencode_e2e.py` (Block 6.6): dort antwortet ein **Stub** als Modell; hier entscheidet das
**echte Modell**, das Werkzeug aufzurufen. Der Server sieht denselben Client (opencode, installiert: 1.18.33) — nur das Modell ist
ein anderes. Was diese Probe **nicht** ersetzt: den Live-Lauf gegen `https://sharefyx.eurofyx.com/mcp` mit dem
echten Konto (P10.5-27) — der Login dort ist Sache des Nikingers.

**Wegwerf:** Instanz aus `phase10_inventory/probes/p10_wegwerf.py` (Port 8799, tmp-`DATA_ROOT`, tmp-`auth.sqlite3`,
TLS selbstsigniert), opencode **isoliert** (eigene `XDG_*` unter `/tmp/opencode/p105-b6-opencode`, Installation
`/tmp/opencode/p105-b6-oc`), Stopp nur per PID/PGID (Hard Rule 9). Die isolierten Verzeichnisse halten den
Wegwerf-Token **fern** vom echten opencode (`~/.local/share/opencode`, Eintrag `sharefyx` bliebe sonst belegt).

**Der Modellschluessel** (Hard Rule 1: nie in eine Datei): er wird zur Laufzeit aus `~/.local/share/opencode/auth.json`
gelesen und nur als `MINIMAX_API_KEY` in die Umgebung des Kindprozesses gesetzt — nicht geschrieben, nicht
ausgegeben (die Ausgabe wird vor dem Schreiben gegen den Schluessel gefiltert).

**Gegenlauf `--skip-auth`:** ohne den Consent-Schritt hat opencode keinen Token → das Modell sieht **kein**
`sharefyx_*`-Werkzeug, der Server loggt **kein** `ev=tool` — die Zellen werden rot.

Aufruf:   `.venv/bin/python phase10_5_finishing/probes/p105_p10j_lauf1_wegwerf.py [--skip-auth] [--model=NAME]`
Ergebnis: `phase10_5_finishing/probes/p105_p10j_lauf1_wegwerf.json` (Gegenlauf: `..._gegenlauf_skip_auth.json`)
"""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import time
from pathlib import Path

HIER = Path(__file__).resolve().parent
MODEL = "minimax/MiniMax-M3.1-Flash"
SKIP_AUTH = False
#: Default: der **installierte** opencode (der, den der Nikinger live benutzt, von nvm); `--bin=` ueberschreibt.
BIN = str(Path.home() / ".nvm/versions/node/v24.18.0/bin/opencode")
for _a in sys.argv[1:]:
    if _a.startswith("--bin="):
        BIN = _a.split("=", 1)[1]
    if _a == "--skip-auth":
        SKIP_AUTH = True
    elif _a.startswith("--model="):
        MODEL = _a.split("=", 1)[1]
RESULT = HIER / ("p105_p10j_lauf1_wegwerf_gegenlauf_skip_auth.json" if SKIP_AUTH else "p105_p10j_lauf1_wegwerf.json")

_argv = sys.argv
sys.argv = [_argv[0]]
_spec = importlib.util.spec_from_file_location("p105_b6_opencode_e2e", HIER / "p105_b6_opencode_e2e.py")
e2e = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(e2e)
sys.argv = _argv

REPO_ROOT = e2e.REPO_ROOT
e2e.OC_BIN = BIN          # alle Aufrufe der geladenen Hilfen laufen ueber dieses Binary
PROMPT = "Rufe das Werkzeug list_spaces auf und nenne mir die Namen der Spaces."


def _schluessel() -> str:
    pfad = Path.home() / ".local/share/opencode/auth.json"
    return json.loads(pfad.read_text(encoding="utf-8"))["minimax"]["key"]


def _filter(text: str, key: str) -> str:
    return text.replace(key, "<key>") if key else text


def main() -> int:
    key = _schluessel()
    creds = json.loads(e2e.CREDS_FILE.read_text())["users"][0]
    result: dict = {"probe": "p105_p10j_lauf1_wegwerf", "modell": MODEL, "opencode_bin": BIN,
                    "opencode_version": subprocess.run([BIN, "--version"], capture_output=True, text=True).stdout.strip(),
                    "base_url": e2e.BASE_URL, "gegenlauf": "skip_auth" if SKIP_AUTH else None}

    e2e._wegwerf_restart()
    e2e._reset_registration_window()
    e2e._fresh_auth_state()
    time.sleep(1.5)
    env = e2e.opencode_env()                       # schreibt die Stub-Config -- gleich ersetzt
    config = {
        "$schema": "https://opencode.ai/config.json",
        "model": MODEL,
        "agent": {"build": {"tools": {"sharefyx_*": True}}},
        "mcp": {"sharefyx": {"type": "remote", "url": f"{e2e.BASE_URL}/mcp", "enabled": True}},
    }
    (e2e.OC_CONFIG / "opencode" / "opencode.json").write_text(json.dumps(config, indent=2), encoding="utf-8")
    env["MINIMAX_API_KEY"] = key
    result["opencode_config"] = config

    auth_log_path = Path("/tmp/opencode/p105-p10j-auth.log")
    auth_proc = None
    try:
        if not SKIP_AUTH:
            auth_log = auth_log_path.open("wb")
            auth_proc = subprocess.Popen(
                [e2e.OC_BIN, "mcp", "auth", "sharefyx", "--print-logs", "--log-level", "DEBUG"],
                env=env, cwd=str(REPO_ROOT), stdout=auth_log, stderr=subprocess.STDOUT, start_new_session=True)
            url, deadline = None, time.time() + 90
            while time.time() < deadline:
                m = e2e.AUTHORIZE_RE.search(auth_log_path.read_text(errors="replace"))
                if m:
                    url = m.group(0)
                    break
                if auth_proc.poll() is not None:
                    break
                time.sleep(0.3)
            result["authorize_url_gefunden"] = bool(url)
            if url:
                browser = subprocess.run(
                    [e2e.E2E_PY, str(e2e.BROWSER_HELPER), url, creds["space"], creds["password"],
                     e2e._totp_secret(creds["otpauth_uri"]), str(e2e.BROWSER_JSON)],
                    capture_output=True, text=True, timeout=180)
                result["browser_exit"] = browser.returncode
            try:
                auth_proc.wait(timeout=90)
            except subprocess.TimeoutExpired:
                e2e._kill_group(auth_proc)
            auth_log.close()
            result["auth_ok"] = "Authentication successful" in auth_log_path.read_text(errors="replace")

        log = Path("/tmp/opencode/sharefyx-wegwerf-p10/serve.log")
        stand = log.stat().st_size if log.exists() else 0
        t0 = time.time()
        run = subprocess.run(
            [e2e.OC_BIN, "run", PROMPT, "--model", MODEL, "--format", "json", "--print-logs", "--log-level", "INFO"],
            env=env, cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=240)
        result["run_exit"] = run.returncode
        result["run_dauer_s"] = round(time.time() - t0, 1)
        out = _filter(run.stdout, key)
        result["run_stdout_tail"] = out[-5000:]
        result["run_stderr_tail"] = _filter(run.stderr, key)[-1500:]
        # Aus dem JSON-Strom: wurde ein sharefyx-Werkzeug **vom Modell** aufgerufen, und mit welchem Ergebnis?
        aufrufe = []
        for zeile in out.splitlines():
            try:
                ev = json.loads(zeile)
            except ValueError:
                continue
            teil = ev.get("part") or {}
            if teil.get("type") == "tool" and "sharefyx" in str(teil.get("tool", "")):
                st = teil.get("state") or {}
                aufrufe.append({"tool": teil.get("tool"), "status": st.get("status"),
                                "ergebnis": str(st.get("output") or "")[:400]})
        result["modell_werkzeugaufrufe"] = aufrufe
        neu = ""
        if log.exists():
            with log.open("rb") as fh:
                fh.seek(stand)
                neu = fh.read().decode("utf-8", errors="replace")
        result["server_ev_tool"] = [l[-300:] for l in neu.splitlines() if '"ev":"tool"' in l or "ev=tool" in l]
    except Exception as exc:                        # die Probe endet nie ohne Ergebnisdatei
        result["error"] = _filter(repr(exc), key)
    finally:
        if auth_proc is not None and auth_proc.poll() is None:
            e2e._kill_group(auth_proc)
        subprocess.run([str(REPO_ROOT / ".venv/bin/python"), str(REPO_ROOT / "phase10_inventory/probes/p10_wegwerf.py"),
                        "stop"], cwd=str(REPO_ROOT), check=False, stdout=subprocess.DEVNULL)

    ok_calls = [a for a in result.get("modell_werkzeugaufrufe", []) if "list_spaces" in str(a["tool"]) and a["status"] == "completed"]
    ok_server = [l for l in result.get("server_ev_tool", []) if "list_spaces" in l and ("ok=true" in l or '"ok":true' in l or "ok=True" in l)]
    result["zellen"] = {
        "auth": bool(result.get("auth_ok")),
        "modell_ruft_list_spaces": bool(ok_calls),
        "server_log_ev_tool_ok": bool(ok_server),
    }
    result["alle_gruen"] = all(result["zellen"].values())
    RESULT.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: result.get(k) for k in ("modell", "gegenlauf", "auth_ok", "run_exit", "run_dauer_s",
                                                "modell_werkzeugaufrufe", "server_ev_tool", "zellen", "error")},
                     ensure_ascii=False, indent=1)[:3500])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
