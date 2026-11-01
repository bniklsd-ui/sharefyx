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


# --- Block 16.2: der Film (`film/film.js`) -------------------------------------------------------

_GEO = "{marke: {x: 119, y: 24}, ziel: {cx: 3500, cy: 4100, z: 0.05}}"


def _film(expr: str):
    script = (f"const f = await import({json.dumps((FILM_DIR / 'film.js').as_uri())});"
              f"const geo = {_GEO}; console.log(JSON.stringify({expr}));")
    out = subprocess.run([NODE, "--input-type=module", "-e", script], capture_output=True,
                         text=True, check=True, timeout=30)
    return json.loads(out.stdout)


@pytest.mark.skipif(NODE is None, reason="node fehlt")
def test_film_state_is_a_pure_function_of_the_frame():
    a, b = _film("[0, 1].map(() => [0, 500, 1175, 2840, 2950, 3299].map(n => f.zustand(n, geo)))")
    assert a == b


@pytest.mark.skipif(NODE is None, reason="node fehlt")
def test_camera_rests_on_each_tile_while_it_holds():
    rows = _film("f.HALTE.map(([an, ab, id]) => [f.kamera(Math.floor((an + ab) / 2), geo), f.mitte(f.kachel(id))])")
    for cam, (cx, cy) in rows[1:]:  # der erste Halt endet im Zoom aus der Marke
        assert (cam["cx"], cam["cy"], cam["z"]) == (cx, cy, 0.85)


@pytest.mark.skipif(NODE is None, reason="node fehlt")
def test_tiles_snap_into_the_four_before_the_morph():
    """Während der Fahrt liegen die Kacheln versetzt; vor dem Morph genau im Raster der 4."""
    fahrt, geordnet = _film("[1175, f.MORPH[0]].map(n => f.zustand(n, geo).kacheln)")
    raster = _film("f.KACHELN.map(k => [k.zelle[0] * f.CELL_W, k.zelle[1] * f.CELL_H])")
    assert any((t["x"], t["y"]) != tuple(r) for t, r in zip(fahrt, raster))
    assert all((t["x"], t["y"], t["rot"]) == (r[0], r[1], 0) for t, r in zip(geordnet, raster))
    zellen = {tuple(z) for z in _film("f.KACHELN.map(k => k.zelle)")}
    assert len(zellen) == 13  # 3 schräg + 4 quer + 6 senkrecht (die Kreuzung zählt einmal)


@pytest.mark.skipif(NODE is None, reason="node fehlt")
def test_old_tiles_turn_new_during_their_sweep():
    vorher, nachher = _film("[f.kachel('s5').streif[0] - 1, f.kachel('s5').streif[1]]"
                            ".map(n => f.zustand(n, geo).kacheln.find(k => k.id === 's5').streif)")
    assert (vorher, nachher) == (0, 1)
