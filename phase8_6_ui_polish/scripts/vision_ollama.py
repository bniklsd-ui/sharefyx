#!/usr/bin/env python3
"""Phase 8.6 — MCP-Wrapper für Ollama-Vision-Modelle (Aktionsliste Schritt 5).

CLI: `vision_ollama.py --image <pfad> --prompt <text> [--model <name>] [--endpoint <url>]`
Stdout: Model-Antwort. Exit-Codes: 0=OK, 2=Argument/IO-Fehler, 3=Ollama nicht erreichbar,
4=leere Antwort.

Default-Modell `qwen3-vl:8b` (Ollama-Library-Suche "vision", 2026-09-10): neueste
Qwen3-VL-Familie, gute UI/Code-Screenshot-Passung, Apache-2.0, ~5 GB Q4, handhabbar
CPU-only (~5–15 tok/s auf i5-14600KF ohne GPU). Alternativen via `--model`:
`qwen2.5vl:7b` (etwas älter), `llava:13b` (klassisch, gut getestet), `minicpm-v:8b`,
`llama3.2-vision:11b` (größer).

Endpoint `127.0.0.1:11434` ist Ollama-Default-Binding (kein öffentliches Binding
nötig; MCP-Bridge spricht intern, Hard-Rule-1-Berührungspunkt vermieden).

Eingesetzt von V119-Smoke (Aktionsliste Schritt 6) gegen `docs/screenshots/*.png`.
"""
from __future__ import annotations

import argparse
import base64
import json
import sys
from pathlib import Path

import requests

OLLAMA_URL = "http://127.0.0.1:11434"
DEFAULT_MODEL = "qwen3-vl:8b"
# V119-Coldstart (Modell erst aus Disk in RAM, dann Vision-Encoder ueber das Bild, dann LLM):
# 6 GB Q4 auf i5-14600KF ohne GPU braucht 30-60s Modell-Load + 5-10s Vision-Encoder + 30-60s
# Text-Decoding = ~80-130s. 600s ist grosszuegig; spaeter im steady-state (Modell schon in RAM)
# reichen 120s.
TIMEOUT_SEC = 600


def main() -> int:
    p = argparse.ArgumentParser(description="Ollama-Vision-Wrapper (Phase 8.6).")
    p.add_argument("--image", required=True, help="Pfad zum Bild (PNG/JPG/WebP).")
    p.add_argument("--prompt", required=True, help="Frage an das Vision-Modell.")
    p.add_argument("--model", default=DEFAULT_MODEL,
                   help=f"Ollama-Modellname (default: {DEFAULT_MODEL}).")
    p.add_argument("--endpoint", default=OLLAMA_URL,
                   help=f"Ollama-API-URL (default: {OLLAMA_URL}).")
    args = p.parse_args()

    image_path = Path(args.image)
    if not image_path.is_file():
        print(f"FEHLER: Bild nicht gefunden: {args.image}", file=sys.stderr)
        return 2

    try:
        image_b64 = base64.b64encode(image_path.read_bytes()).decode("ascii")
    except OSError as e:
        print(f"FEHLER: Bild-Lesen fehlgeschlagen: {e}", file=sys.stderr)
        return 2

    try:
        r = requests.post(
            f"{args.endpoint}/api/generate",
            json={
                "model": args.model,
                "prompt": args.prompt,
                "images": [image_b64],
                "stream": False,
            },
            timeout=TIMEOUT_SEC,
        )
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"FEHLER: Ollama-API nicht erreichbar ({args.endpoint}): {e}",
              file=sys.stderr)
        return 3

    try:
        body = r.json()
    except ValueError as e:
        print(f"FEHLER: Ollama-Antwort kein JSON: {e}", file=sys.stderr)
        return 3

    response = body.get("response", "").strip()
    if not response:
        print(f"FEHLER: leere Antwort von Ollama: {json.dumps(body)[:200]}",
              file=sys.stderr)
        return 4

    print(response)
    return 0


if __name__ == "__main__":
    sys.exit(main())
