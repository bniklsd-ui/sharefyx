#!/usr/bin/env python3
"""P10.5 Block 16 — Render-Treiber des Launch-Films (Plan §3.1/§3.3).

Lädt eine Bühnenseite (`probe.html`, später `film.html`) über einen lokalen HTTP-Server auf
127.0.0.1 (zufälliger Port, nur Lesen), ruft je Bild `renderFrame(n)` auf und nimmt das Bild per
CDP `Page.captureScreenshot` auf. Die Bilder gehen per `image2pipe` **direkt** in ffmpeg — keine
Frame-Dateien auf der Platte der Live-VM. Je Bild wird ein SHA-256 gerechnet; zwei Läufe über
denselben Bereich müssen dieselben Hashes liefern (Kriterium L1).

Aufruf mit `~/.claude-code-tools/film-venv/bin/python`:
  render.py --page probe.html --start 0 --end 120 [--out film.mp4] [--dpr 2] [--still N:pfad.png]
Ausgabe: JSON auf stdout (Hashes, Sekunden je Bild), Protokoll auf stderr.
"""
from __future__ import annotations

import argparse
import base64
import functools
import hashlib
import http.server
import json
import subprocess
import sys
import threading
import time
from pathlib import Path

FILM_DIR = Path(__file__).resolve().parent
REPO_ROOT = FILM_DIR.parents[1]
STATIC_DIR = REPO_ROOT / "phase5_ui" / "webui" / "static"
WORK_DIR = Path.home() / "sharefyx-film"  # Aufnahmen und MP4, außerhalb des Repos
W, H, FPS = 1920, 1080, 60


class _Handler(http.server.SimpleHTTPRequestHandler):
    """/film/* → dieses Verzeichnis · /static/* → UI-Statik · /still/* → Aufnahmen. Sonst 404."""

    ROOTS = {"film": FILM_DIR, "static": STATIC_DIR, "still": WORK_DIR / "stills"}

    def translate_path(self, path: str) -> str:
        parts = path.split("?", 1)[0].lstrip("/").split("/", 1)
        root = self.ROOTS.get(parts[0])
        if root is None or len(parts) < 2:
            return str(FILM_DIR / "__nicht_da__")
        target = (root / parts[1]).resolve()
        return str(target) if target.is_relative_to(root.resolve()) else str(FILM_DIR / "__nicht_da__")

    def log_message(self, *_args) -> None:  # stdout bleibt JSON (Hard Rule 7)
        pass


def _serve() -> tuple[http.server.ThreadingHTTPServer, int]:
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(_Handler))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, server.server_address[1]


def _ffmpeg(out: Path) -> subprocess.Popen:
    import imageio_ffmpeg

    cmd = [imageio_ffmpeg.get_ffmpeg_exe(), "-hide_banner", "-loglevel", "error", "-y",
           "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "png", "-i", "-",
           "-vf", f"scale={W}:{H}:flags=lanczos", "-c:v", "libx264", "-preset", "slow",
           "-crf", "17", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)]
    return subprocess.Popen(cmd, stdin=subprocess.PIPE)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--page", default="probe.html")
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--end", type=int, default=120)
    ap.add_argument("--dpr", type=float, default=2.0)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--still", action="append", default=[], help="N:pfad.png — Einzelbild sichern")
    args = ap.parse_args()

    from playwright.sync_api import sync_playwright

    stills = {int(k): Path(v) for k, v in (s.split(":", 1) for s in args.still)}
    server, port = _serve()
    enc = _ffmpeg(args.out) if args.out else None
    hashes: list[str] = []
    t0 = time.perf_counter()
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        # Gerendert wird mit `clip.scale` = dpr: Chromium rastert die Seite dabei neu in dieser
        # Auflösung (16.0 gemessen: scharf wie `--force-device-scale-factor`, ein 1×-Bild
        # hochgerechnet ist weich). Ein `device_scale_factor` am Kontext allein reicht **nicht** —
        # `Page.captureScreenshot` liefert dann trotzdem 1920 × 1080.
        page = browser.new_page(viewport={"width": W, "height": H})
        page.goto(f"http://127.0.0.1:{port}/film/{args.page}")
        page.wait_for_function("window.stageReady !== undefined")
        page.evaluate("window.stageReady")
        cdp = page.context.new_cdp_session(page)
        t_ready = time.perf_counter()
        for n in range(args.start, args.end):
            # Zwei rAF warten nur darauf, dass das gesetzte Bild gemalt ist — der Zustand selbst
            # hängt allein an n.
            page.evaluate("n => { renderFrame(n); return new Promise(r => requestAnimationFrame("
                          "() => requestAnimationFrame(r))); }", n)
            png = base64.b64decode(cdp.send("Page.captureScreenshot", {
                "format": "png", "optimizeForSpeed": True,
                "clip": {"x": 0, "y": 0, "width": W, "height": H, "scale": args.dpr}})["data"])
            hashes.append(hashlib.sha256(png).hexdigest())
            if n in stills:
                stills[n].write_bytes(png)
            if enc is not None:
                enc.stdin.write(png)
        browser.close()
    t_end = time.perf_counter()
    server.shutdown()
    if enc is not None:
        enc.stdin.close()
        if enc.wait() != 0:
            print("ffmpeg ist gescheitert", file=sys.stderr)
            return 1
    frames = args.end - args.start
    result = {"page": args.page, "frames": frames, "dpr": args.dpr,
              "s_per_frame": round((t_end - t_ready) / max(frames, 1), 4),
              "setup_s": round(t_ready - t0, 2),
              "frames_sha256": hashlib.sha256("".join(hashes).encode()).hexdigest(),
              "first_last": [hashes[0][:16], hashes[-1][:16]] if hashes else []}
    if args.out:
        result["mp4"] = str(args.out)
        result["mp4_sha256"] = hashlib.sha256(args.out.read_bytes()).hexdigest()
        result["mp4_bytes"] = args.out.stat().st_size
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
