#!/usr/bin/env python3
"""P10.5-26 — **Matrix gegen unseren echten Wegwerf-Server**: welche opencode-Einstellung
bringt die MCP-Werkzeuge bis zum Modell?

**Was bis hierher gemessen ist (2026-10-23).**
  * Gegen einen **einfachen** FastMCP-Server (ohne OAuth, ohne unseren Produktcode) arbeitet
    opencode 1.19.4 **einwandfrei** — mit und ohne GET-SSE-Strom (`stateless_http` true/false):
    das Werkzeug `*_list_spaces` landet im Modell-Request und wird aufgerufen. Der 405 auf
    `GET /mcp` ist also **nicht** die Ursache.
  * Gegen **unseren** Wegwerf-Server (OAuth + `stateless_http=True`, Lock P2-B) sieht das Modell
    **kein** MCP-Werkzeug. Das Server-Log zeigt `initialize` (200), `notifications/initialized`
    (202) — und **kein** `tools/list`, **kein** `tools/call`, **keine** `ev=tool`-Zeile (in der
    ganzen Logdatei: **null**).

**Diese Probe variiert genau eine opencode-Einstellung je Lauf** und liest danach dieselben
zwei Belege: die Werkzeugliste des Modell-Requests und den Server-Log-Abschnitt des Laufs.

| Variante | `oauth` | `headers` | `protocol` |
|---|---|---|---|
| 1 `default` | Auto (DCR) | — | `legacy` (Vorgabe) |
| 2 `bearer` | `false` | `Authorization: Bearer …` | `legacy` |
| 3 `bearer_auto` | `false` | `Authorization: Bearer …` | `auto` |
| 4 `bearer_2026` | `false` | `Authorization: Bearer …` | `2026-07-28` |

Der Bearer-Token stammt aus dem **Wegwerf**-Tokenstand von opencode (eine Wegwerf-Datei in
`/tmp`, kein Produktgeheimnis) und wird **nirgends** ausgegeben — die Ausgabe maskiert ihn.

Ergebnis: JSON auf stdout und `p105_b6_opencode_matrix.json` neben diesem Skript.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OC_BIN = "/tmp/opencode/p105-b6-oc/node_modules/.bin/opencode"
OUT_JSON = Path(__file__).resolve().parent / "p105_b6_opencode_matrix.json"
OC_HOME = Path("/tmp/opencode/p105-b6-opencode")
AUTH_FILE = OC_HOME / "data" / "opencode" / "mcp-auth.json"
SERVER_LOG = Path("/tmp/opencode/sharefyx-wegwerf-p10/serve.log")
BASE_URL = "https://127.0.0.1:8799"
STUB_PORT = 18125

_STUB_LOG: list[dict] = []


def _token() -> str:
    """Der Wegwerf-Bearer-Token aus dem opencode-Tokenstand — nur intern benutzt."""
    data = json.loads(AUTH_FILE.read_text())
    return data["sharefyx"]["tokens"]["accessToken"]


class _StubModelHandler(BaseHTTPRequestHandler):
    """Stub-Modell mit Rundengrenze (der Fehler der ersten Fassung, 2026-10-22: endlose Schleife)."""

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
        mcp_names = [n for n in tool_names if n.startswith("sharefyx_")]
        messages = data.get("messages") or []
        called = None
        for message in messages:
            for call in (message.get("tool_calls") or []):
                called = (call.get("function") or {}).get("name") or called
        eintrag = {"runde": len(_STUB_LOG) + 1, "werkzeuge": tool_names,
                   "mcp_werkzeuge": mcp_names, "zuletzt_gerufen": called, "antwort": None}
        _STUB_LOG.append(eintrag)
        if mcp_names and called != mcp_names[0]:
            eintrag["antwort"] = f"tool:{mcp_names[0]}"
            self._reply_tool(mcp_names[0])
        elif called is not None and any("list_spaces" in n for n in mcp_names):
            eintrag["antwort"] = "text:ergebnis"
            self._reply({"role": "assistant", "content": "list_spaces gerufen."}, finish="stop")
        else:
            eintrag["antwort"] = "text:kein_werkzeug"
            self._reply({"role": "assistant", "content": "kein list_spaces-Werkzeug sichtbar"},
                        finish="stop")

    def _reply(self, message: dict, *, finish: str) -> None:
        self._sse([{"delta": {"role": "assistant", "content": message.get("content") or ""}},
                   {"delta": {}, "finish_reason": finish}])

    def _reply_tool(self, name: str) -> None:
        self._sse([{"delta": {"role": "assistant", "content": None, "tool_calls": [{
            "index": 0, "id": f"call_{name}", "type": "function",
            "function": {"name": name, "arguments": "{}"}}]}},
            {"delta": {}, "finish_reason": "tool_calls"}])

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


def _env() -> dict[str, str]:
    env = os.environ.copy()
    for name in list(env):
        if name.startswith("SHAREFYX_") or name.startswith("SFX_"):
            env.pop(name)
    env.update({
        "XDG_CONFIG_HOME": str(OC_HOME / "config"),
        "XDG_DATA_HOME": str(OC_HOME / "data"),
        "XDG_CACHE_HOME": str(OC_HOME / "cache"),
        "XDG_STATE_HOME": str(OC_HOME / "state"),
        "NODE_TLS_REJECT_UNAUTHORIZED": "0",
    })
    return env


def _write_config(server: dict[str, object]) -> None:
    config_dir = OC_HOME / "config" / "opencode"
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
        "agent": {"build": {"tools": {"sharefyx_*": True, "glob": True}}},
        "mcp": {"sharefyx": server},
    }, indent=2), encoding="utf-8")


def _variant(name: str, server: dict[str, object]) -> dict:
    _STUB_LOG.clear()
    _write_config(server)
    env = _env()
    stand = SERVER_LOG.stat().st_size if SERVER_LOG.exists() else 0
    stub = ThreadingHTTPServer(("127.0.0.1", STUB_PORT), _StubModelHandler)
    thread = threading.Thread(target=stub.serve_forever, daemon=True)
    thread.start()
    ergebnis: dict = {"variante": name, "server_konfiguration": {
        k: ("<bearer>" if k == "headers" else v) for k, v in server.items()}}
    try:
        run = subprocess.run(
            [OC_BIN, "run", "Rufe list_spaces auf.", "--model", "stub/stub-1",
             "--format", "json", "--print-logs", "--log-level", "INFO"],
            env=env, cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=120,
        )
        ergebnis["run_exit"] = run.returncode
        ergebnis["run_text_tail"] = run.stdout[-800:]
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
    if SERVER_LOG.exists():
        with SERVER_LOG.open("rb") as fh:
            fh.seek(stand)
            neu = fh.read().decode("utf-8", errors="replace")
        ergebnis["server_zugriffe"] = [
            line for line in neu.splitlines() if '"ev":"http"' in line or "ev=tool" in line]
    return ergebnis


def main() -> int:
    token = _token()
    varianten = [
        ("1_default", {"type": "remote", "url": f"{BASE_URL}/mcp", "enabled": True}),
        ("2_bearer", {"type": "remote", "url": f"{BASE_URL}/mcp", "enabled": True,
                      "oauth": False, "headers": {"Authorization": f"Bearer {token}"}}),
        ("3_bearer_auto", {"type": "remote", "url": f"{BASE_URL}/mcp", "enabled": True,
                           "oauth": False, "headers": {"Authorization": f"Bearer {token}"},
                           "protocol": "auto"}),
        ("4_bearer_2026", {"type": "remote", "url": f"{BASE_URL}/mcp", "enabled": True,
                           "oauth": False, "headers": {"Authorization": f"Bearer {token}"},
                           "protocol": "2026-07-28"}),
    ]
    result: dict = {"probe": "p105_b6_opencode_matrix", "base_url": BASE_URL}
    for name, server in varianten:
        result[name] = _variant(name, server)
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    OUT_JSON.write_text(text, encoding="utf-8")
    print(text.replace(token, "<bearer>"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
