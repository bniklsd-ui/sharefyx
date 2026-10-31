"""P10.5 Block 16 — Wächter für die Bühne des Launch-Films (Plan §3.1, Kriterium L1).

Kein Browser, kein Netz: die reinen Funktionen aus `film/stage.js` laufen in Node, der
Pfadschutz des Render-Servers in Python. Der Volllauf-Determinismus (zwei Läufe, gleiche
Hashes) ist ein Messbefund an der Bühne (`probes/p105_b16_0_probe.json`), kein Unit-Test —
er braucht Chromium.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

FILM_DIR = Path(__file__).resolve().parents[1] / "film"
sys.path.insert(0, str(FILM_DIR))
import render  # noqa: E402

NODE = shutil.which("node")


def _stage(expr: str):
    script = (f"const s = await import({json.dumps((FILM_DIR / 'stage.js').as_uri())});"
              f"console.log(JSON.stringify({expr}));")
    out = subprocess.run([NODE, "--input-type=module", "-e", script], capture_output=True,
                         text=True, check=True, timeout=30)
    return json.loads(out.stdout)


@pytest.mark.skipif(NODE is None, reason="node fehlt")
def test_prng_is_the_same_sequence_for_the_same_seed():
    a, b, c = _stage("[1, 1, 2].map(seed => { const r = s.prng(seed); return [r(), r(), r()]; })")
    assert a == b
    assert a != c
    assert all(0 <= x < 1 for x in a + c)


@pytest.mark.skipif(NODE is None, reason="node fehlt")
def test_phase_is_clamped_and_eased():
    vals = _stage("[-10, 0, 30, 60, 90].map(n => s.phase(n, 0, 60))")
    assert vals[0] == 0 and vals[1] == 0
    assert vals[2] == pytest.approx(0.5)
    assert vals[3] == 1 and vals[4] == 1


@pytest.mark.skipif(NODE is None, reason="node fehlt")
def test_camera_puts_the_world_point_into_the_middle():
    assert _stage("s.cameraTransform(100, 50, 2)") == \
        "translate(960px, 540px) scale(2) translate(-100px, -50px)"


@pytest.mark.parametrize("path", ["/film/../../CLAUDE.md", "/static/../../../CLAUDE.md",
                                  "/etc/passwd", "/", "/still/../../.ssh/id_ed25519"])
def test_render_server_serves_nothing_outside_its_three_roots(path):
    handler = object.__new__(render._Handler)
    target = Path(handler.translate_path(path))
    assert target.name == "__nicht_da__"


def test_render_server_maps_its_roots():
    handler = object.__new__(render._Handler)
    assert Path(handler.translate_path("/film/stage.js")) == FILM_DIR / "stage.js"
    assert Path(handler.translate_path("/static/logo.svg")) == render.STATIC_DIR / "logo.svg"
