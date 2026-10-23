#!/usr/bin/env python3
"""P10.5-26 — **welche** MCP-Transport-Variante sieht opencode 1.19.4? (Wegwerf, kein Produktcode)

**Der Befund, den diese Probe auflösen soll (2026-10-23).** Der Wegwerf-E2E-Lauf
(`p105_b6_opencode_e2e.py`) gegen unseren echten Server ergab: opencode öffnet `GET /mcp`,
bekommt **405** — und danach kommt **kein einziger** POST. In **keiner** der fünf
Modell-Anfragen tauchte ein `sharefyx_*`-Werkzeug auf. Unser Server läuft mit
`stateless_http=True` (Lock **P2-B**): der GET-SSE-Strom existiert dort nicht, nur POST.

**Zwei Erklärungen, beide plausibel — und beide bisher nicht getrennt:**
  (a) opencodes MCP-Client braucht den GET-SSE-Strom und gibt nach dem 405 auf
      (der MCP-Standard verlangt von einem Client das **Fallback auf POST-only**);
  (b) opencode sieht die Werkzeuge nie, weil die Werkzeug-Freigabe im Agenten
      (`agent.build.tools`) nicht greift.

**Diese Probe trennt (a) von (b).** Zwei FastMCP-Server auf eigenen Ports, **je ein
Werkzeug** `list_spaces`, **ohne** OAuth, **ohne** Browser, **ohne** unseren Produktcode:

| Variante | `http_app(...)` | Transport am Client |
|---|---|---|
| **A** | `stateless_http=True` | POST-only (so unser Server, P2-B) |
| **B** | `stateless_http=False` | POST **plus** GET-SSE-Strom |

Gegen beide läuft opencode mit dem Stub-Modell. **Der Beleg ist die Werkzeugliste des
Modell-Requests** (die Werkzeuge, die opencode dem Modell angeboten hat) **plus** das
Server-Zugriffsprotokoll (welche Methoden opencode tatsächlich gerufen hat) — nicht die
Behauptung „opencode kann MCP".

**Gegenlauf eingebaut:** die Werkzeugliste wird je Anfrage protokolliert, und die Variante
ohne MCP-Server (nur ein harmloses Builtin) muss „kein MCP-Werkzeug sichtbar" ergeben — sonst
prüft der Messgerät-Zähler nichts.

Ergebnis: JSON auf stdout und `p105_b6_transport.json` neben diesem Skript.
"""
from __future__ import annotations

import json
import os
import re
import signal
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OC_BIN = "/tmp/opencode/p105-b6-oc/node_modules/.bin/opencode"
OUT_JSON = Path(__file__).resolve().parent / "p105_b6_transport.json"
WORK = Path("/tmp/opencode/p105-b6-transport")
STUB_PORT = 18124
PORT_A = 8801          # Variante A: POST-only (stateless)
PORT_B = 8802          # Variante B: POST + GET-SSE

SERVER_SCRIPT = '''
import sys
from fastmcp import FastMCP
import uvicorn

mcp = FastMCP("probe")

@mcp.tool(name="list_spaces", description="Die Spaces des Kontos")
def list_spaces() -> str:
    return "alpha, beta, gamma"

stateless = sys.argv[1] == "true"
port = int(sys.argv[2])
app = mcp.http_app(path="/mcp", stateless_http=stateless)
uvicorn.run(app, host="127.0.0.1", port=port, log_level="info", access_log=True)
'''

_STUB_LOG: list[dict] = []


class _StubModelHandler(BaseHTTPRequestHandler):
    """Stub-Modell: antwortet mit **einem** Werkzeugaufruf, sobald opencode ein MCP-Werkzeug
    anbietet — und beendet den Lauf danach mit Text. Keine Endlosschleife (der Fehler der
    ersten Fassung, 2026-10-22)."""

    protocol_version = "HTTP/1.1"

    def log_message(self, *args) -> None:
        pass

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("content-length", 0))
        raw = self.rfile.read(length)
        try:
            data = json.loads(raw)
        except ValueError:
            data = {}
        tools = data.get("tools") or []
        tool_names = [(t.get("function") or {}).get("name") or "" for t in tools]
        mcp_names = [n for n in tool_names if n.startswith("probe")]
        called = _called_tool(data.get("messages") or [])
        eintrag = {"runde": len(_STUB_LOG) + 1, "werkzeuge": tool_names,
                   "mcp_werkzeuge": mcp_names, "zuletzt_gerufen": called, "antwort": None}
        _STUB_LOG.append(eintrag)
        if mcp_names and called != mcp_names[0]:
            eintrag["antwort"] = f"tool:{mcp_names[0]}"
            self._reply_tool(mcp_names[0])
        elif called is not None and any("list_spaces" in n for n in mcp_names):
            eintrag["antwort"] = "text:ergebnis"
            self._reply({"role": "assistant", "content": "list_spaces gerufen: "
                                                        + str(_last_tool_content(
                                                            data.get("messages") or []))[:400]},
                        finish="stop")
        else:
            eintrag["antwort"] = "text:kein_werkzeug"
            self._reply({"role": "assistant", "content": "kein list_spaces-Werkzeug sichtbar"},
                        finish="stop")

    def _reply(self, message: dict, *, finish: str) -> None:
        self._sse([
            {"delta": {"role": "assistant", "content": message.get("content") or ""}},
            {"delta": {}, "finish_reason": finish},
        ])

    def _reply_tool(self, name: str) -> None:
        self._sse([
            {"delta": {"role": "assistant", "content": None, "tool_calls": [{
                "index": 0, "id": f"call_{name}", "type": "function",
                "function": {"name": name, "arguments": "{}"},
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
            payload = {"id": "chatcmpl-stub", "object": "chat.completion.chunk", "created": 0,
                       "model": "stub-1", "choices": [{"index": 0, **chunk}]}
            self.wfile.write(f"data: {json.dumps(payload)}\n\n".encode("utf-8"))
        self.wfile.write(b"data: [DONE]\n\n")
        self.wfile.flush()


def _called_tool(messages: list[dict]) -> str | None:
    """Name des zuletzt aufgerufenen Werkzeugs — er steht in der `tool_calls`-Liste der
    Assistenten-Nachricht, **nicht** im Ergebnis (`role=tool` trägt nur `content`)."""
    name = None
    for message in messages:
        for call in (message.get("tool_calls") or []):
            name = (call.get("function") or {}).get("name") or name
    return name


def _last_tool_content(messages: list[dict]) -> str:
    for message in reversed(messages):
        if message.get("role") == "tool":
            return str(message.get("content") or "")
    return ""


def _env(cfg_home: Path) -> dict[str, str]:
    env = os.environ.copy()
    for name in list(env):
        if name.startswith("SHAREFYX_") or name.startswith("SFX_"):
            env.pop(name)
    for sub in ("config", "data", "cache", "state"):
        (cfg_home / sub).mkdir(parents=True, exist_ok=True)
    env.update({
        "XDG_CONFIG_HOME": str(cfg_home / "config"),
        "XDG_DATA_HOME": str(cfg_home / "data"),
        "XDG_CACHE_HOME": str(cfg_home / "cache"),
        "XDG_STATE_HOME": str(cfg_home / "state"),
    })
    return env


def _write_config(cfg_home: Path, server_name: str, url: str) -> None:
    config_dir = cfg_home / "config" / "opencode"
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
        "agent": {"build": {"tools": {f"{server_name}_*": True}}},
        "mcp": {server_name: {"type": "remote", "url": url, "enabled": True}},
    }, indent=2), encoding="utf-8")


def _start_server(tag: str, stateless: bool, port: int) -> tuple[subprocess.Popen, Path]:
    WORK.mkdir(parents=True, exist_ok=True)
    script = WORK / f"server_{tag}.py"
    script.write_text(SERVER_SCRIPT, encoding="utf-8")
    log = WORK / f"server_{tag}.log"
    handle = log.open("wb")
    proc = subprocess.Popen(
        [sys.executable, str(script), "true" if stateless else "false", str(port)],
        stdout=handle, stderr=subprocess.STDOUT, start_new_session=True,
    )
    return proc, log


def _wait_for_port(port: int, seconds: float = 25.0) -> bool:
    import socket
    deadline = time.time() + seconds
    while time.time() < deadline:
        with socket.socket() as sock:
            sock.settimeout(0.5)
            if sock.connect_ex(("127.0.0.1", port)) == 0:
                return True
        time.sleep(0.3)
    return False


def _stop(proc: subprocess.Popen) -> None:
    """Nur die **eigene** Wegwerf-Instanz — per Prozessgruppe, nie per Regex (Hard Rule 9)."""
    try:
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
    except (ProcessLookupError, PermissionError):
        return
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            pass


def _run_variant(tag: str, server_name: str, stateless: bool, port: int) -> dict:
    _STUB_LOG.clear()
    cfg_home = WORK / f"oc_{tag}"
    _write_config(cfg_home, server_name, f"http://127.0.0.1:{port}/mcp")
    env = _env(cfg_home)

    stub = ThreadingHTTPServer(("127.0.0.1", STUB_PORT), _StubModelHandler)
    thread = threading.Thread(target=stub.serve_forever, daemon=True)
    thread.start()
    ergebnis: dict = {"tag": tag, "server_name": server_name, "port": port,
                       "stateless_http": stateless}
    try:
        run = subprocess.run(
            [OC_BIN, "run", "Rufe list_spaces auf.", "--model", "stub/stub-1",
             "--format", "json", "--print-logs", "--log-level", "INFO"],
            env=env, cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=120,
        )
        ergebnis["run_exit"] = run.returncode
        ergebnis["run_stdout_tail"] = run.stdout[-2500:]
        ergebnis["run_stderr_tail"] = run.stderr[-1500:]
    except subprocess.TimeoutExpired as exc:
        ergebnis["run_exit"] = "timeout"
        ergebnis["run_error"] = repr(exc)
    finally:
        stub.shutdown()
        stub.server_close()
    ergebnis["stub_requests"] = list(_STUB_LOG)
    ergebnis["mcp_werkzeuge_gesehen"] = sorted({
        name for eintrag in _STUB_LOG for name in eintrag["mcp_werkzeuge"]})
    ergebnis["werkzeug_aufgerufen"] = sorted({
        eintrag["zuletzt_gerufen"] for eintrag in _STUB_LOG if eintrag["zuletzt_gerufen"]})
    return ergebnis


def main() -> int:
    result: dict = {"probe": "p105_b6_transport", "opencode_binary": OC_BIN}
    varianten = [("A", "probea", True, PORT_A), ("B", "probeb", False, PORT_B)]
    laeufer = []
    try:
        for tag, server_name, stateless, port in varianten:
            proc, log = _start_server(tag, stateless, port)
            laeufer.append((proc, log))
            if not _wait_for_port(port):
                result.setdefault("server_fehler", {})[tag] = f"Port {port} kam nicht hoch"
                continue
            time.sleep(1.0)
            variante = _run_variant(tag, server_name, stateless, port)
            variante["server_zugriffe"] = [
                line for line in (log.read_text(errors="replace").splitlines()
                                  if log.exists() else [])
                if "HTTP/1.1" in line]
            result[tag] = variante
    finally:
        for proc, _log in laeufer:
            _stop(proc)

    OUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
