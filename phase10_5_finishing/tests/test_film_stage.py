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

# `markeBox` wie in der Bühne gemessen (16.6, `filmGeo.markeBox`): Kasten 239 × 49, Tinte darin.
_GEO = ("{marke: {x: 119, y: 24}, ziel: {cx: 3500, cy: 4100, z: 0.05},"
        " markeBox: {w: 239, h: 49, ix: 17, iy: 12, iw: 117, ih: 17}}")


def _film(expr: str):
    script = (f"const f = await import({json.dumps((FILM_DIR / 'film.js').as_uri())});"
              f"const geo = {_GEO}; console.log(JSON.stringify({expr}));")
    out = subprocess.run([NODE, "--input-type=module", "-e", script], capture_output=True,
                         text=True, check=True, timeout=30)
    return json.loads(out.stdout)


@pytest.mark.skipif(NODE is None, reason="node fehlt")
def test_film_state_is_a_pure_function_of_the_frame():
    a, b = _film("[0, 1].map(() => [0, 60, 500, 1175, 1240, 2600, 2800, f.FRAMES - 1].map(n => f.zustand(n, geo)))")
    assert a == b


@pytest.mark.skipif(NODE is None, reason="node fehlt")
def test_camera_rests_while_a_tile_holds_and_puts_it_on_its_side():
    """16.8: im Halt steht die Kamera still (ohne Fokus); die Kachel steht mit ihrer Mitte auf ihrer
    Seite (960 ± 300, 540) und liegt — gedreht, gekippt, herangerückt — ganz im Bild."""
    rows = _film("f.HALTE.map(([an, ab, id]) => { const k = f.kachel(id), m = Math.floor((an + ab) / 2);"
                 " const z = f.zustand(m, geo), s = z.kacheln.find(t => t.id === id);"
                 " return [id, !!k.fokus, k.seite, f.kamera(an, geo), f.kamera(ab - 1, geo), z.cam,"
                 " f.welt2bild(z.cam, s.x + f.TILE_W / 2, s.y + f.TILE_H / 2), s.kipp.push]; })")
    for kid, fokus, seite, cam_an, cam_ab, cam, (mx, my), push in rows:
        if fokus:
            continue
        assert cam_an == cam_ab == cam, kid
        assert (mx, my) == (pytest.approx(960 + seite * 300), pytest.approx(540)), kid
        # Rand: halbe Kachel × Zoom × Heranrücken × 1,09 (Perspektive, die nahe Kante wächst)
        hw, hh = 800 * cam["z"] * push * 1.09, 500 * cam["z"] * push * 1.09
        assert mx - hw >= 0 and mx + hw <= 1920 and my - hh >= 0 and my + hh <= 1080, kid


@pytest.mark.skipif(NODE is None, reason="node fehlt")
def test_focus_push_stays_sharp():
    """Heranfahren nur so weit, wie die 2×-Aufnahme trägt: Bild-Zoom × Heranrücken ≤ 2."""
    zs = _film("f.KACHELN.filter(k => k.fokus).map(k => { const [an, ab] = f.HALTE.find(h => h[2] === k.id);"
               " return Array.from({length: ab - an}, (_, j) => { const z = f.zustand(an + j, geo);"
               " return z.cam.z * z.kacheln.find(t => t.id === k.id).kipp.push; }); })")
    assert len(zs) == 2
    assert all(max(z) <= 2.0 for z in zs)
    assert all(max(z) >= 1.2 for z in zs)  # das Heranfahren ist wirklich da


@pytest.mark.skipif(NODE is None, reason="node fehlt")
def test_tiles_snap_into_the_four_before_the_morph():
    """Während der Fahrt liegen die Kacheln versetzt; vor dem Morph genau im Raster der 4."""
    fahrt, geordnet = _film("[1175, f.MORPH[0]].map(n => f.zustand(n, geo).kacheln)")
    raster = _film("f.KACHELN.map(k => [k.zelle[0] * f.CELL_W, k.zelle[1] * f.CELL_H])")
    assert any((t["x"], t["y"]) != tuple(r) for t, r in zip(fahrt, raster))
    assert all((t["x"], t["y"], t["rot"]) == (r[0], r[1], 0) for t, r in zip(geordnet, raster))
    # 16.8: die 4 bildet sich aus **flachen** Kacheln — keine Kippung, kein Heranrücken übrig
    assert all(t["kipp"] == {"ry": 0, "rx": 0, "push": 1} for t in geordnet)
    zellen = {tuple(z) for z in _film("f.KACHELN.map(k => k.zelle)")}
    assert len(zellen) == 13  # 3 schräg + 4 quer + 6 senkrecht (die Kreuzung zählt einmal)


@pytest.mark.skipif(NODE is None, reason="node fehlt")
def test_old_tiles_turn_new_during_their_sweep():
    vorher, nachher = _film("[f.kachel('s5').streif[0] - 1, f.kachel('s5').streif[1]]"
                            ".map(n => f.zustand(n, geo).kacheln.find(k => k.id === 's5').streif)")
    assert (vorher, nachher) == (0, 1)


# --- Block 16.6: der Auftakt ---------------------------------------------------------------------

@pytest.mark.skipif(NODE is None, reason="node fehlt")
def test_opening_mark_is_never_cut_off():
    """Sichtung 1: vom Namen war nur ein angeschnittenes „x“ zu sehen. Im ganzen Auftakt liegt die
    Tinte der Marke (Zeichen, Name, Version) mit Rand im Bild — groß in der Mitte und im Flug."""
    rows = _film("Array.from({length: f.HALTE[0][0] + 1}, (_, n) => { const z = f.zustand(n, geo);"
                 " return [n, z.marke.deck, z.marke.pose]; })")
    b = {"ix": 17, "iy": 12, "iw": 117, "ih": 17}
    sichtbar = [r for r in rows if r[1] > 0]
    assert sichtbar, "die Marke erscheint im Auftakt nie"
    for n, _deck, p in sichtbar:
        x0, y0 = p["x"] + b["ix"] * p["s"], p["y"] + b["iy"] * p["s"]
        x1, y1 = x0 + b["iw"] * p["s"], y0 + b["ih"] * p["s"]
        assert 20 <= x0 and x1 <= 1900 and 20 <= y0 and y1 <= 1060, (n, x0, y0, x1, y1)
    gross = max(p["s"] for _n, _d, p in sichtbar)
    assert gross * b["iw"] >= 800  # groß genug, um gelesen zu werden


@pytest.mark.skipif(NODE is None, reason="node fehlt")
def test_opening_mark_lands_on_the_rail_of_the_first_tile():
    """Gelandet sitzt die Marke im Maßstab der Kamera auf dem Kachelpunkt (0, 8) von s1."""
    pose, cam, ziel = _film("(() => { const n = f.HALTE[0][0], z = f.zustand(n, geo), s1 = z.kacheln[0];"
                            " return [z.marke.pose, z.cam, f.welt2bild(z.cam, ...f.kachelPunkt(s1, 0, 8))]; })()")
    assert pose["s"] == pytest.approx(cam["z"])
    assert (pose["x"], pose["y"]) == (pytest.approx(ziel[0]), pytest.approx(ziel[1]))


# --- Block 16.7: das Raster ----------------------------------------------------------------------

@pytest.mark.skipif(NODE is None, reason="node fehlt")
def test_grid_keeps_its_density_through_every_zoom():
    """Vom Halt (z 0,85) bis zur großen 4 (z ≈ 0,07): der Abstand auf dem Bild bleibt in [80, 160)
    px — beim Herauszoomen wird das Raster nicht zu Brei."""
    abst = _film("Array.from({length: f.FRAMES}, (_, n) => f.zustand(n, geo).raster.abstand)")
    assert all(80 <= a < 160 for a in abst), (min(abst), max(abst))


@pytest.mark.skipif(NODE is None, reason="node fehlt")
def test_grid_moves_slower_than_the_tiles():
    """Parallaxe: zwischen zwei Halten wandert der Ursprung des Rasters halb so weit wie die Welt."""
    (a, ca), (b, cb) = _film("[f.HALTE[1][0], f.HALTE[2][0]].map(n => { const z = f.zustand(n, geo);"
                             " return [z.raster, z.cam]; })")
    welt = (cb["cx"] - ca["cx"]) * ca["z"]
    assert welt != 0
    assert (b["ux"] - a["ux"]) / -welt == pytest.approx(0.5)


@pytest.mark.skipif(NODE is None, reason="node fehlt")
def test_grid_appears_with_the_bang_and_steps_back_for_the_glyph():
    vor, nach, ende = _film("[f.AUFTAKT.knall - 1, f.HALTE[0][0], f.FRAMES - 1]"
                            ".map(n => f.zustand(n, geo).raster.deck)")
    assert vor == 0 and nach == 1 and ende == pytest.approx(0.25)


# --- Block 16.8: Bewegung, Text, Tempo ------------------------------------------------------------

@pytest.mark.skipif(NODE is None, reason="node fehlt")
def test_every_scene_writes_its_text_with_the_sweep_on_the_free_side():
    rows = _film("f.KACHELN.map((k, i) => { const [an, ab] = f.HALTE[i];"
                 " return [k.id, k.seite, !!k.text, f.textZustand(k.streif[0] - 1), f.textZustand(ab - 6),"
                 " f.textZustand(ab + 30)]; })")
    for kid, seite, hat_text, vorher, voll, danach in rows:
        assert hat_text, kid
        assert vorher is None or vorher["id"] != kid, kid  # erst mit dem Streif
        assert voll["id"] == kid and voll["seite"] == -seite, kid
        assert all(w["deck"] == pytest.approx(1, abs=0.02) for w in voll["woerter"]), kid
        assert danach is None or danach["id"] != kid, kid


@pytest.mark.skipif(NODE is None, reason="node fehlt")
def test_film_is_faster_and_within_length():
    """16.8 (c): schneller als Fassung 1 (55 s), Kriterium L3 (40–60 s)."""
    sekunden = _film("f.FRAMES / f.FPS")
    assert 40 <= sekunden <= 50


_FILM_VENV = Path.home() / ".claude-code-tools" / "film-venv" / "bin" / "python"
_FONTS = FILM_DIR.parents[1] / "phase5_ui" / "webui" / "static" / "fonts"


@pytest.mark.skipif(NODE is None or not _FILM_VENV.exists(), reason="node oder film-venv (fontTools) fehlt")
def test_film_texts_are_in_the_font_subsets():
    """Die Schriften sind Teilsätze — ein fehlendes Zeichen fiele **lautlos** auf eine Systemschrift
    zurück. Jeder Text des Films steht im Teilsatz der Sans, jede Terminalzeile in dem der Mono."""
    import re

    sans = "".join(_film("f.KACHELN.flatMap(k => k.text)")) + "harefyx v3.1.6 v4.0.0 4.0.0"
    html = (FILM_DIR / "film.html").read_text(encoding="utf-8")
    term = html[html.index("function terminalZeilen"):html.index("const geo = {}")]
    mono = "".join(re.findall(r'"([^"]*)"', term)) + "".join(re.findall(r"'([^']*)'", term))
    lauf = Path.home() / "sharefyx-film" / "daten" / "ki_lauf.json"
    if lauf.exists():  # die Namen und Titel aus dem echten Lauf
        mono += lauf.read_text(encoding="utf-8")
    script = ("import json, sys; from fontTools.ttLib import TTFont\n"
              "a = json.load(sys.stdin); out = {}\n"
              "for name, text in a.items():\n"
              "    cm = TTFont(name).getBestCmap()\n"
              "    out[name] = sorted({c for c in text if c not in '\\n' and ord(c) not in cm})\n"
              "print(json.dumps(out))")
    fonts = {str(_FONTS / "IBMPlexSans-subset.6c21979f.woff2"): sans,
             str(_FONTS / "IBMPlexMono-subset.a8d5dfa6.woff2"): mono}
    out = subprocess.run([str(_FILM_VENV), "-I", "-c", script], input=json.dumps(fonts),
                         capture_output=True, text=True, check=True, timeout=60)
    fehlt = json.loads(out.stdout)
    assert all(v == [] for v in fehlt.values()), fehlt


@pytest.mark.skipif(NODE is None, reason="node fehlt")
def test_only_the_playing_tile_is_bright_while_it_holds():
    """Vorschau 16.8: Nachbarkacheln ragten in die Textseite. Im Halt steht die aktive Kachel voll da,
    alle anderen auf ≤ 35 %; vor dem Morph (Fahrt vorbei) sind wieder alle hell."""
    rows = _film("f.HALTE.map(([an, ab, id]) => [id, f.zustand(Math.floor((an + ab) / 2), geo).kacheln"
                 ".map(t => [t.id, t.deckkraft])])")
    for kid, kacheln in rows:
        for tid, deck in kacheln:
            assert deck == pytest.approx(1) if tid == kid else deck <= 0.36, (kid, tid, deck)
    assert all(t["deckkraft"] == 1 for t in _film("f.zustand(f.MORPH[0], geo).kacheln"))
