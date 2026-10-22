#!/usr/bin/env python3
"""6.6 — Wegwerf-E2E: der **echte opencode** gegen die Wegwerf-Instanz (Plan Block 6, Schritt 6.6).

Der Plan verlangt den vollen Fluss: Registrierung → `/oauth/authorize` (Login + TOTP) → Code →
Token → `list_spaces`. Diese Messanordnung:

1. **Wegwerf-Instanz** (`phase10_inventory/probes/p10_wegwerf.py`, Port 8799, TLS mit einem
   selbstsignierten Zertifikat CN/SAN `127.0.0.1`) — sie laeuft **den Repo-Stand**, also mit dem
   Code dieses Blocks.
2. **opencode isoliert** (eigene `XDG_*`, eigene Installation `opencode-ai@1.19.4`): die
   MCP-URL steht **ohne** Slash (`https://127.0.0.1:8799/mcp`) — damit ist Schritt 6.3 an einem
   echten Client geprueft (vorher: 307 auf `/mcp/`).
   `NODE_TLS_REJECT_UNAUTHORIZED=0` ist noetig, weil Bun im OAuth-Pfad dem selbstsignierten
   Zertifikat nicht traut. **[Befund 2026-10-22]:** die M3-Messung (2026-10-18, opencode
   1.18.33) said "Bun ehrt keine CA-Variablen im OAuth-Pfad" — mit 1.19.4 greift
   `NODE_TLS_REJECT_UNAUTHORIZED=0` **dort** wieder. Der Issuer-Rewrite-Proxy aus M3 ist damit
   fuer diese Messung **nicht** noetig — und weggelassen, weil er den `resource`-Parameter
   umschreiben wuerde und der Server ihn dann ablehnt (der Client sandte `resource=http://…`,
   der Server erwartet `https://…` — der Server hat recht, der Proxy hatte gelogen).
3. **Chromium** (Playwright, eigenes venv) macht den Consent: Passwort + TOTP, Klick auf
   „Anmelden" → der Consent-POST antwortet mit 302 auf `http://127.0.0.1:19876/...` → Chromium
   muss dem folgen duerfen (**V197**, CSP `form-action`).

Ergebnis: JSON auf stdout + `p105_b6_opencode_e2e.json` neben diesem Skript.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import signal
import subprocess
import sys
import threading
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
WEGWERF_ROOT = Path("/tmp/opencode/sharefyx-wegwerf-p10")
CREDS_FILE = WEGWERF_ROOT / "credentials.json"
OC_BIN = "/tmp/opencode/p105-b6-oc/node_modules/.bin/opencode"
E2E_PY = "/home/savefyx/.claude-code-tools/e2e-venv/bin/python"
BROWSER_HELPER = REPO_ROOT / "phase10_5_finishing" / "probes" / "p105_b6_consent_browser.py"
OUT_JSON = Path(__file__).resolve().parent / "p105_b6_opencode_e2e.json"
BROWSER_JSON = Path("/tmp/opencode/p105-b6-consent.json")
OC_CONFIG = Path("/tmp/opencode/p105-b6-opencode/config")
OC_DATA = Path("/tmp/opencode/p105-b6-opencode/data")
OC_CACHE = Path("/tmp/opencode/p105-b6-opencode/cache")
OC_STATE = Path("/tmp/opencode/p105-b6-opencode/state")
BASE_URL = "https://127.0.0.1:8799"
STUB_PORT = 18123  # der Stub-Modell-Endpunkt (lokal, Wegwerf)

AUTHORIZE_RE = re.compile(r"https://127\.0\.0\.1:8799/oauth/authorize\?[^\s\"']+")


class _StubModelHandler(BaseHTTPRequestHandler):
    """Minimaler OpenAI-kompatibler Chat-Endpoint — **Messgeraet**, kein Serverbaustein.

    `opencode run` braucht ein Modell, um ein Werkzeug aufzurufen. Fuer die Wegwerf-Messung
    genuegt ein Stub: die erste Anfrage wird mit einem Tool-Aufruf von `list_spaces`
    beantwortet, die zweite (mit dem Tool-Ergebnis) mit Text. Damit ruft opencode das
    MCP-Werkzeug wirklich auf — ohne Modell, ohne Netz, ohne Schluessel.
    """

    protocol_version = "HTTP/1.1"

    def log_message(self, *args) -> None:  # Ausgabe nur ins Log, nicht auf stderr
        pass

    def do_POST(self) -> None:  # noqa: N802 (http.server-Namenskonvention)
        length = int(self.headers.get("content-length", 0))
        raw = self.rfile.read(length)
        Path("/tmp/opencode/p105-b6-stub-request.json").write_bytes(raw)
        try:
            data = json.loads(raw)
        except ValueError:
            data = {}
        messages = data.get("messages") or []
        tools = data.get("tools") or []
        tool_name = None
        for tool in tools:
            name = (tool.get("function") or {}).get("name") or ""
            if "list_spaces" in name:
                tool_name = name
                break
        tool_result = next((m for m in messages if m.get("role") == "tool"), None)
        tool_names = [(t.get("function") or {}).get("name") or "" for t in tools]

        if tool_result is not None and "list_spaces" in str(tool_result.get("content")):
            content = "list_spaces ausgefuehrt: " + str(tool_result.get("content"))[:800]
            self._reply({"role": "assistant", "content": content}, finish="stop")
        elif tool_name is not None:
            self._reply_tool(tool_name)
        elif "glob" in tool_names:
            # Die MCP-Verbindung stand beim ersten Request noch nicht: ein harmloses Builtin
            # haelt die Schleife am Leben, bis die Werkzeuge da sind.
            self._reply_tool("glob", arguments={"pattern": "ZZZ_nicht_vorhanden_*"})
        else:
            self._reply({"role": "assistant", "content": "kein list_spaces-Werkzeug sichtbar"},
                        finish="stop")

    def _reply(self, message: dict, *, finish: str) -> None:
        """Textantwort — als SSE, weil opencode `stream: true` sendet (der AI-SDK-Provider
        erwartet Chunks, kein einzelnes JSON)."""
        self._sse([
            {"delta": {"role": "assistant", "content": message.get("content") or ""}},
            {"delta": {}, "finish_reason": finish},
        ])

    def _reply_tool(self, name: str, *, arguments: dict | None = None) -> None:
        self._sse([
            {"delta": {"role": "assistant", "content": None, "tool_calls": [{
                "index": 0, "id": f"call_{name}", "type": "function",
                "function": {"name": name, "arguments": json.dumps(arguments or {})},
            }]}},
            {"delta": {}, "finish_reason": "tool_calls"},
        ])

    def _sse(self, chunks: list[dict]) -> None:
        self.send_response(200)
        self.send_header("content-type", "text/event-stream")
        self.send_header("cache-control", "no-cache")
        self.send_header("connection", "close")
        self.end_headers()
        for chunk in chunks:
            payload = {
                "id": "chatcmpl-stub", "object": "chat.completion.chunk", "created": 0,
                "model": "stub-1", "choices": [{"index": 0, **chunk}],
            }
            self.wfile.write(f"data: {json.dumps(payload)}\n\n".encode("utf-8"))
        self.wfile.write(b"data: [DONE]\n\n")
        self.wfile.flush()


def _clean_env() -> dict[str, str]:
    env = os.environ.copy()
    for name in list(env):
        if name.startswith("SHAREFYX_") or name.startswith("SFX_"):
            env.pop(name)
    return env


def opencode_env() -> dict[str, str]:
    for path in (OC_CONFIG, OC_DATA, OC_CACHE, OC_STATE):
        path.mkdir(parents=True, exist_ok=True)
    config_dir = OC_CONFIG / "opencode"
    config_dir.mkdir(parents=True, exist_ok=True)
    (config_dir / "opencode.json").write_text(json.dumps({
        "$schema": "https://opencode.ai/config.json",
        "provider": {
            "stub": {
                "npm": "@ai-sdk/openai-compatible",
                "name": "Stub",
                "options": {"baseURL": f"http://127.0.0.1:{STUB_PORT}/v1", "apiKey": "stub"},
                "models": {"stub-1": {"name": "Stub 1", "tool_call": True}},
            },
        },
        "model": "stub/stub-1",
        "agent": {
            # Die MCP-Werkzeuge des "build"-Agenten sind **nicht** standardmaessig aktiv;
            # das Muster ist "<server>_*" (gemessen: "sharefyx_list_spaces" o. Ae.).
            # `glob` daneben, damit die erste Anfrage ueberhaupt ein Werkzeug traegt (harmlos:
            # die Muster treffen nichts).
            "build": {"tools": {"sharefyx_*": True, "glob": True}},
        },
        "mcp": {
            "sharefyx": {"type": "remote", "url": f"{BASE_URL}/mcp", "enabled": True},
        },
    }, indent=2), encoding="utf-8")
    env = _clean_env()
    env.update({
        "XDG_CONFIG_HOME": str(OC_CONFIG),
        "XDG_DATA_HOME": str(OC_DATA),
        "XDG_CACHE_HOME": str(OC_CACHE),
        "XDG_STATE_HOME": str(OC_STATE),
        "NODE_TLS_REJECT_UNAUTHORIZED": "0",
    })
    return env


def _kill_group(proc: subprocess.Popen) -> None:
    """Die opencode-Gruppe beenden (SIGTERM, dann SIGKILL) — **per PID/PGID**, nie per
    Regex-Muster (Hard Rule 9: `pkill -f` trifft die echte Instanz mit)."""
    try:
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
    except (ProcessLookupError, PermissionError):
        pass
    try:
        proc.wait(timeout=15)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            pass
        proc.wait(timeout=15)


def _totp_secret(otpauth_uri: str) -> str:
    return urllib.parse.parse_qs(urllib.parse.urlsplit(otpauth_uri).query)["secret"][0]


def _wegwerf_restart() -> None:
    """Die Wegwerf-Instanz **neu starten** — sie laeuft den Repo-Stand in ihrem Prozess, ein
    zwischenzeitlich gepatchter Code (z. B. der CSP-Gegenlauf) ist sonst nicht angekommen."""
    for action in ("stop", "start"):
        subprocess.run(
            [str(REPO_ROOT / ".venv/bin/python"),
             str(REPO_ROOT / "phase10_inventory/probes/p10_wegwerf.py"), action],
            cwd=str(REPO_ROOT), check=False, stdout=subprocess.DEVNULL,
        )


def _reset_registration_window() -> None:
    """Das **DCR-Kontingent** (20 Registrierungen pro Stunde, Plan §2.7) zurücksetzen.

    Die Probe registriert mehrfach (Auth-Lauf, Debug-Lauf, Werkzeuglauf) — nach 20 Versuchen
    antwortet der Server mit **429 rate_limited** und der Auth-Fluss bricht ab, **ohne** dass
    am Produktcode etwas kaputt wäre. Das ist ein Messinstrument-Fehler: die Wegwerf-`auth.sqlite3`
    ist Wegwerf-Daten (nie die echte), das Zurücksetzen ist ein `DELETE` auf **eine** Zeile.
    """
    db = WEGWERF_ROOT / "auth.sqlite3"
    if not db.exists():
        return
    import sqlite3
    conn = sqlite3.connect(db)
    try:
        conn.execute("DELETE FROM register_attempts")
        conn.commit()
    finally:
        conn.close()


def _fresh_auth_state() -> None:
    """Der isolierte opencode-Tokenstand wird geloescht: sonst nimmt der zweite Lauf den
    gespeicherten Token und **macht gar keinen Consent-Fluss** (der erste Lauf hat den Token
    ja schon geholt). Messbar: ohne Authorize-URL im Log."""
    token_file = OC_DATA / "opencode" / "mcp-auth.json"
    if token_file.exists():
        token_file.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--no-tool-call", action="store_true",
                        help="den Werkzeugaufruf (Stub-Modell) auslassen — fuer Gegenlaeufe, "
                             "die nur den Consent-Fluss messen wollen")
    args = parser.parse_args()

    creds = json.loads(CREDS_FILE.read_text())["users"][0]
    result: dict = {
        "probe": "p105_b6_opencode_e2e",
        "opencode_binary": OC_BIN,
        "base_url": BASE_URL,
    }

    _wegwerf_restart()
    _reset_registration_window()
    _fresh_auth_state()
    time.sleep(1.5)
    env = opencode_env()
    result["opencode_config"] = json.loads((OC_CONFIG / "opencode" / "opencode.json").read_text())

    auth_log_path = Path("/tmp/opencode/p105-b6-auth.log")
    auth_log = auth_log_path.open("wb")
    auth_proc = subprocess.Popen(
        [OC_BIN, "mcp", "auth", "sharefyx", "--print-logs", "--log-level", "DEBUG"],
        env=env, cwd=str(REPO_ROOT), stdout=auth_log, stderr=subprocess.STDOUT,
        start_new_session=True,
    )

    try:
        authorize_url = None
        deadline = time.time() + 90
        while time.time() < deadline:
            text = auth_log_path.read_text(errors="replace")
            match = AUTHORIZE_RE.search(text)
            if match:
                authorize_url = match.group(0)
                break
            if auth_proc.poll() is not None:
                break
            time.sleep(0.3)
        result["authorize_url"] = authorize_url

        if not authorize_url:
            result["error"] = "keine /oauth/authorize-URL im opencode-Log"
        else:
            browser = subprocess.run(
                [E2E_PY, str(BROWSER_HELPER), authorize_url, creds["space"], creds["password"],
                 _totp_secret(creds["otpauth_uri"]), str(BROWSER_JSON)],
                capture_output=True, text=True, timeout=180,
            )
            result["browser_exit"] = browser.returncode
            result["browser_stderr_tail"] = browser.stderr[-1500:]
            result["browser"] = json.loads(BROWSER_JSON.read_text()) if BROWSER_JSON.exists() else None

        try:
            auth_proc.wait(timeout=90)
        except subprocess.TimeoutExpired:
            _kill_group(auth_proc)
        result["auth_exit"] = auth_proc.returncode
        auth_log.close()
        log_text = auth_log_path.read_text(errors="replace")
        result["auth_log_tail"] = log_text[-3000:]
        result["auth_ok"] = "Authentication successful" in log_text

        debug = subprocess.run(
            [OC_BIN, "mcp", "debug", "sharefyx", "--print-logs", "--log-level", "INFO"],
            env=env, cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=120,
        )
        result["debug_exit"] = debug.returncode
        result["debug_stdout_tail"] = debug.stdout[-3000:]
        result["debug_stderr_tail"] = debug.stderr[-3000:]

        # Der Werkzeug-Aufruf: opencode laeuft mit dem Stub-Modell und ruft list_spaces.
        if not args.no_tool_call:
            stub_server = ThreadingHTTPServer(("127.0.0.1", STUB_PORT), _StubModelHandler)
            stub_thread = threading.Thread(target=stub_server.serve_forever, daemon=True)
            stub_thread.start()
            try:
                run = subprocess.run(
                    [OC_BIN, "run", "Rufe list_spaces auf.", "--model", "stub/stub-1",
                     "--format", "json", "--print-logs", "--log-level", "INFO"],
                    env=env, cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=120,
                )
                result["run_exit"] = run.returncode
                result["run_stdout_tail"] = run.stdout[-4000:]
                result["run_stderr_tail"] = run.stderr[-2500:]
            finally:
                stub_server.shutdown()
                stub_server.server_close()
    except Exception as exc:  # die Messung darf nie ohne Ergebnisdatei enden
        result["error"] = repr(exc)
    finally:
        if auth_proc.poll() is None:
            _kill_group(auth_proc)

    OUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
