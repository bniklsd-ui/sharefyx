"""Wächter des Launch-Films in der App (P10.5 Block 17, Plan
`docs/concepts/phase10_5_block17_film_app_plan.md`).

Die Laufzeit (Startbild, Klick spielt mit Ton, nichts lädt ohne Klick) misst die Browser-Probe
`probes/p105_b17_film_probe.py` an der Wegwerf-Instanz. Hier steht, was am **Text** prüfbar ist —
und was ohne Wächter still verrottet.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
STATIC = REPO_ROOT / "phase5_ui" / "webui" / "static"
APP_HTML = (STATIC / "app.html").read_text("utf-8")


def _video_tag() -> str:
    tags = re.findall(r"<video\b[^>]*>", APP_HTML)
    assert len(tags) == 1, tags
    return tags[0]


def test_the_film_name_carries_the_real_hash():
    """Der Name trägt die ersten 8 Hex der echten SHA-256 — und **muss** es: gehashte Namen
    liefert `static_routes.py` ein Jahr `immutable` aus. Ein neuer Schnitt unter altem Namen
    bliebe bei jedem, der den alten gesehen hat, still im Browser-Cache."""
    src = re.search(r'data-src="/ui/static/(media/[^"]+)"', _video_tag()).group(1)
    datei = STATIC / src
    assert datei.is_file(), src
    kurz = re.search(r"\.([0-9a-f]{8})\.mp4$", datei.name).group(1)
    assert hashlib.sha256(datei.read_bytes()).hexdigest().startswith(kurz)


def test_the_video_has_no_src_until_the_click():
    """Kein `src`, `preload="none"`: ohne Klick fragt der Browser die 25,7 MB nie an (Auftrag:
    der Erstaufruf bleibt leicht). Ein `src` im Markup lüde beim Seitenaufruf."""
    tag = _video_tag()
    assert not re.search(r"\ssrc=", tag)
    assert 'preload="none"' in tag


def test_media_holds_only_the_film():
    """`media/` ist im Budget-Wächter ausgenommen (lädt nur auf Abruf). Eine weitere Datei dort
    fiele aus jeder Zählung — sie muss erst begründet werden."""
    assert sorted(p.name for p in (STATIC / "media").iterdir()) == ["sharefyx-4.0.0.cab1f13a.mp4"]


def test_the_module_is_wired_and_remembers_per_browser_only():
    js = (STATIC / "js" / "launchfilm.js").read_text("utf-8")
    app = (STATIC / "js" / "app.js").read_text("utf-8")
    assert 'import { init as initLaunchFilm } from "./launchfilm.js";' in app
    assert "initLaunchFilm();" in app
    assert '"sfx:film:gesehen"' in js
    # Kein Server-Zustand (Auftrag): das Modul spricht nicht mit der API.
    assert "api(" not in js and "fetch(" not in js
    assert 'id="update-log-film"' in APP_HTML
