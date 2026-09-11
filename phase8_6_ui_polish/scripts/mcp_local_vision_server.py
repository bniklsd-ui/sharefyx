#!/usr/bin/env python3
"""MCP server: local_vision -- thin stdio wrapper around Ollama vision.

Exposes a single MCP tool `local_vision` that takes an image path and a prompt,
sends them to a local Ollama instance (qwen3-vl:8b by default), and returns the
model's textual analysis. This is the backend for the `opencode-vision` plugin,
which intercepts pasted images in OpenCode and tells the orchestrator model to
call this tool with the saved path.

Protocol: MCP (Model Context Protocol) JSON-RPC over stdio. stderr is for logs
(Hard Rule 7 -- stdout only carries MCP responses). No external SDK -- just
stdlib + requests (already in the project venv). Implementation is intentionally
small; the existing `vision_ollama.py` CLI wrapper covers ad-hoc use.

Exit codes (Hard Rule 7): 0 on graceful shutdown, 2 on protocol error,
3 on Ollama unreachable, 4 on tool error.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
from pathlib import Path
from typing import Any

import requests

SERVER_NAME = "local_vision"
SERVER_VERSION = "1.0.0"
PROTOCOL_VERSION = "2024-11-05"

DEFAULT_MODEL = "qwen3-vl:8b"
DEFAULT_ENDPOINT = "http://127.0.0.1:11434"
DEFAULT_TIMEOUT_S = 600

SUPPORTED_MIMES = {
    "image/png": "png",
    "image/jpeg": "jpg",
    "image/jpg": "jpg",
    "image/webp": "webp",
}


def log(msg: str) -> None:
    """stderr log line (Hard Rule 7)."""
    print(f"[local_vision] {msg}", file=sys.stderr, flush=True)


def fail(code: int, message: str) -> None:
    log(f"exit {code}: {message}")
    sys.exit(code)


def send(response: dict[str, Any]) -> None:
    """Write one JSON-RPC response to stdout."""
    sys.stdout.write(json.dumps(response) + "\n")
    sys.stdout.flush()


def ok(id_: Any, result: Any) -> None:
    send({"jsonrpc": "2.0", "id": id_, "result": result})


def err(id_: Any, code: int, message: str, data: Any = None) -> None:
    payload: dict[str, Any] = {"jsonrpc": "2.0", "id": id_, "error": {"code": code, "message": message}}
    if data is not None:
        payload["error"]["data"] = data
    send(payload)


def tool_result(text: str, is_error: bool = False) -> dict[str, Any]:
    return {"content": [{"type": "text", "text": text}], "isError": is_error}


def handle_initialize(params: dict[str, Any]) -> dict[str, Any]:
    return {
        "protocolVersion": PROTOCOL_VERSION,
        "capabilities": {"tools": {"listChanged": False}},
        "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
    }


def handle_tools_list(_params: dict[str, Any]) -> dict[str, Any]:
    return {
        "tools": [
            {
                "name": "local_vision",
                "description": (
                    "Analyze an image with a local vision model (Ollama, qwen3-vl:8b "
                    "by default). Takes a filesystem path to the image and a prompt; "
                    "returns the model's textual analysis. Use this whenever the user "
                    "shares a screenshot, photo, or other image and you need to "
                    "describe or reason about its contents."
                ),
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": (
                                "Absolute or relative path to an image file on disk "
                                "(PNG, JPEG, or WebP). The path is provided by the "
                                "opencode-vision plugin after saving a pasted image."
                            ),
                        },
                        "prompt": {
                            "type": "string",
                            "description": (
                                "Question or instruction for the vision model. Keep it "
                                "specific -- the model answers in the language of the "
                                "prompt."
                            ),
                        },
                        "model": {
                            "type": "string",
                            "description": (
                                "Override the default Ollama model "
                                f"(default: {DEFAULT_MODEL})."
                            ),
                        },
                    },
                    "required": ["path", "prompt"],
                    "additionalProperties": False,
                },
            }
        ]
    }


def call_ollama(
    image_path: str,
    prompt: str,
    model: str,
    endpoint: str,
    timeout_s: int,
) -> str:
    p = Path(image_path).expanduser().resolve()
    if not p.is_file():
        raise FileNotFoundError(f"image not found: {p}")

    mime = None
    ext = p.suffix.lower().lstrip(".")
    for m, e in SUPPORTED_MIMES.items():
        if e == ext:
            mime = m
            break
    if mime is None:
        mime = "image/png"

    try:
        data = p.read_bytes()
    except OSError as exc:
        raise RuntimeError(f"cannot read image: {exc}") from exc

    b64 = base64.b64encode(data).decode("ascii")

    url = endpoint.rstrip("/") + "/api/generate"
    payload = {"model": model, "prompt": prompt, "images": [b64], "stream": False}
    log(f"POST {url} model={model} prompt={len(prompt)}c image={p.name} ({len(data)}B)")

    try:
        resp = requests.post(url, json=payload, timeout=timeout_s)
    except requests.RequestException as exc:
        raise RuntimeError(f"Ollama unreachable at {endpoint}: {exc}") from exc

    if resp.status_code != 200:
        snippet = resp.text[:300]
        raise RuntimeError(f"Ollama HTTP {resp.status_code}: {snippet}")

    try:
        body = resp.json()
    except ValueError as exc:
        raise RuntimeError(f"Ollama returned non-JSON: {exc}") from exc

    answer = (body.get("response") or "").strip()
    if not answer:
        raise RuntimeError(f"Ollama returned empty response: {body!r}")

    return answer


def handle_tools_call(params: dict[str, Any]) -> dict[str, Any]:
    arguments = params.get("arguments") or {}
    image_path = arguments.get("path")
    prompt = arguments.get("prompt")
    if not isinstance(image_path, str) or not isinstance(prompt, str):
        return tool_result(
            "both `path` (string) and `prompt` (string) are required", is_error=True
        )

    model = arguments.get("model") or os.environ.get("LOCAL_VISION_MODEL", DEFAULT_MODEL)
    endpoint = os.environ.get("LOCAL_VISION_ENDPOINT", DEFAULT_ENDPOINT)
    try:
        timeout_s = int(os.environ.get("LOCAL_VISION_TIMEOUT_S", str(DEFAULT_TIMEOUT_S)))
    except ValueError:
        timeout_s = DEFAULT_TIMEOUT_S

    try:
        answer = call_ollama(image_path, prompt, model, endpoint, timeout_s)
    except FileNotFoundError as exc:
        return tool_result(f"error: {exc}", is_error=True)
    except RuntimeError as exc:
        log(f"call failed: {exc}")
        return tool_result(f"error: {exc}", is_error=True)
    except Exception as exc:
        log(f"unexpected: {exc!r}")
        return tool_result(f"unexpected error: {exc}", is_error=True)

    return tool_result(answer)


HANDLERS = {
    "initialize": handle_initialize,
    "tools/list": handle_tools_list,
    "tools/call": handle_tools_call,
}


def serve() -> int:
    log(f"starting (endpoint={DEFAULT_ENDPOINT}, model={DEFAULT_MODEL})")
    for raw in sys.stdin:
        line = raw.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except ValueError as exc:
            err(None, -32700, f"parse error: {exc}")
            continue

        method = msg.get("method")
        msg_id = msg.get("id")
        params = msg.get("params") or {}

        if method is None:
            if msg_id is not None:
                err(msg_id, -32600, "missing method")
            continue

        if method.startswith("notifications/"):
            log(f"notification: {method}")
            continue

        handler = HANDLERS.get(method)
        if handler is None:
            err(msg_id, -32601, f"method not found: {method}")
            continue

        try:
            result = handler(params)
        except Exception as exc:
            log(f"handler {method} crashed: {exc!r}")
            err(msg_id, -32603, f"internal error: {exc}")
            continue

        ok(msg_id, result)

    log("stdin closed, shutting down")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="mcp_local_vision_server",
        description=(
            "MCP server exposing `local_vision` (Ollama-backed image analysis). "
            "Started by OpenCode via `opencode.json`; not intended for direct CLI use."
        ),
    )
    parser.add_argument("--check", action="store_true", help="smoke-check Ollama reachability, do not serve")
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT, help="Ollama base URL")
    args = parser.parse_args()

    if args.check:
        try:
            r = requests.get(args.endpoint.rstrip("/") + "/api/tags", timeout=5)
            r.raise_for_status()
            models = [m["name"] for m in r.json().get("models", [])]
            log(f"Ollama reachable, {len(models)} model(s) installed")
            for n in models:
                log(f"  - {n}")
            return 0
        except Exception as exc:
            fail(3, f"Ollama not reachable at {args.endpoint}: {exc}")

    return serve()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        log("interrupted")
        sys.exit(0)
    except BrokenPipeError:
        log("broken pipe")
        sys.exit(0)