#!/usr/bin/env python3
"""P10.5 Block 16.4 — der Ton des Launch-Films, im Code erzeugt (Plan §3.4, Q4).

Keine Aufnahme, keine Lizenzfrage: Flächen (ein D-Dur-Akkord mit None, leicht verstimmt), ein
Urknall am Anfang (ein Sog zum Funken, dann ein tiefer Schlag
mit Rauschen), ein Glockenton bei jeder Ankunft der Kamera an einer Kachel, ein Anschwellen im Zoom heraus, ein
Glitzern im Morph und ein Schlussakkord. Die Zeitmarken kommen **aus `film.js`** (HALTE, ZOOM_AUS,
MORPH, ENDE) — Bild und Ton haben eine Quelle. Fester Seed, nur numpy ⇒ dieselbe Datei in jedem
Lauf (Kriterium L1 gilt auch hier: Hash im Ergebnis).

Aufruf: `~/.claude-code-tools/film-venv/bin/python ton.py [--out ~/sharefyx-film/ton.wav]`.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

FILM = Path(__file__).resolve().parent
RATE = 48000


def marken() -> dict:
    node = shutil.which("node") or "/usr/bin/node"
    script = (f"const f = await import({json.dumps((FILM / 'film.js').as_uri())});"
              "console.log(JSON.stringify({FPS: f.FPS, FRAMES: f.FRAMES, HALTE: f.HALTE,"
              " ZOOM_AUS: f.ZOOM_AUS, MORPH: f.MORPH, ENDE: f.ENDE, AUFTAKT: f.AUFTAKT}));")
    return json.loads(subprocess.run([node, "--input-type=module", "-e", script],
                                     capture_output=True, text=True, check=True).stdout)


def hz(midi: float) -> float:
    return 440.0 * 2 ** ((midi - 69) / 12)


def ton(f: float, dauer: float, teile=(1.0,), gewichte=(1.0,), abkling=None) -> np.ndarray:
    t = np.arange(int(dauer * RATE)) / RATE
    s = sum(w * np.sin(2 * np.pi * f * k * t) for k, w in zip(teile, gewichte))
    if abkling:
        s = s * np.exp(-t / abkling)
    return s


def huelle(n: int, an: float, ab: float) -> np.ndarray:
    t = np.arange(n) / RATE
    e = np.minimum(1, t / max(an, 1e-3)) * np.minimum(1, (t[-1] - t) / max(ab, 1e-3))
    return np.clip(e, 0, 1) ** 1.5


def hall(x: np.ndarray, rng: np.random.Generator, laenge=2.8, nass=0.32) -> np.ndarray:
    n = int(laenge * RATE)
    ir = rng.standard_normal(n) * np.exp(-np.arange(n) / RATE / (laenge / 5.5))
    ir /= np.sqrt((ir ** 2).sum())
    m = 1 << int(np.ceil(np.log2(len(x) + n)))
    y = np.fft.irfft(np.fft.rfft(x, m) * np.fft.rfft(ir, m), m)[: len(x)]
    return (1 - nass) * x + nass * y


def mischen(dauer: float, m: dict) -> np.ndarray:
    rng = np.random.default_rng(0x5FA1)
    n = int(dauer * RATE)
    L = np.zeros(n)
    R = np.zeros(n)
    sek = lambda frame: frame / m["FPS"]  # noqa: E731

    def setze(sig, start_s, links=1.0, rechts=1.0):
        a = int(start_s * RATE)
        b = min(n, a + len(sig))
        if a >= n:
            return
        L[a:b] += links * sig[: b - a]
        R[a:b] += rechts * sig[: b - a]

    # 1) Fläche: D-Dur mit None (D2 A2 D3 F#3 A3 E4), je Stimme zwei leicht verstimmte Sinus.
    akkord = [38, 45, 50, 54, 57, 64]
    flaeche_ende = sek(m["ENDE"][0]) + 0.2
    for i, note in enumerate(akkord):
        for verst, (l, r) in ((-0.06, (0.8, 0.4)), (0.06, (0.4, 0.8))):
            s = ton(hz(note + verst), flaeche_ende, (1, 2, 3), (1, 0.25, 0.08))
            s *= huelle(len(s), 3.5, 1.5) * (0.055 if note < 50 else 0.035)
            setze(s, 0.0, l, r)
    # 1b) Urknall (16.6): ein Sog, der zum Funken ansteigt, dann ein tiefer Schlag mit Rauschen.
    f0, knall = sek(m["AUFTAKT"]["funke"][0]), sek(m["AUFTAKT"]["knall"])
    k = int((knall - f0) * RATE)
    sog = rng.standard_normal(k)
    for j in range(1, k):  # Tiefpass, der sich öffnet
        sog[j] = sog[j - 1] + (0.004 + 0.08 * (j / k) ** 2) * (sog[j] - sog[j - 1])
    setze(sog * np.linspace(0, 1, k) ** 3 * 0.9, f0)
    schlag = ton(hz(26), 3.5, (1, 1.5, 2), (1, 0.3, 0.15), abkling=0.9) * 0.22
    krach = rng.standard_normal(int(1.2 * RATE)) * np.exp(-np.arange(int(1.2 * RATE)) / RATE / 0.18)
    for j in range(1, len(krach)):
        krach[j] = krach[j - 1] + 0.05 * (krach[j] - krach[j - 1])
    setze(schlag, knall)
    setze(krach * 0.6, knall, 1.0, 0.9)
    # 2) Glocke bei jeder Ankunft — die Töne laufen den Akkord hinauf.
    glocken = [74, 76, 78, 81, 83, 86, 78, 81, 83, 86, 88, 90, 93]
    for i, (an, _ab, _id) in enumerate(m["HALTE"]):
        s = ton(hz(glocken[i % len(glocken)]), 2.5, (1, 2.76, 5.4), (1, 0.35, 0.12), abkling=0.55)
        pan = 0.5 + 0.35 * np.sin(i * 1.7)
        setze(s * 0.09, sek(max(an, 30)), 1.2 - pan, 0.2 + pan)
    # 3) Anschwellen im Zoom heraus: gefiltertes Rauschen + Oktave der Fläche.
    a, b = sek(m["ZOOM_AUS"][0]), sek(m["MORPH"][0])
    k = int((b - a) * RATE)
    rausch = rng.standard_normal(k)
    tief = np.zeros(k)
    alpha = 0.02
    for j in range(1, k):  # einfacher Tiefpass, wird heller
        alpha = 0.01 + 0.06 * j / k
        tief[j] = tief[j - 1] + alpha * (rausch[j] - tief[j - 1])
    setze(tief * np.linspace(0, 1, k) ** 2 * 0.5, a, 0.9, 0.9)
    # 4) Glitzern im Morph: schnelle, zufällig gesetzte hohe Akkordtöne.
    a, b = sek(m["MORPH"][0]), sek(m["MORPH"][1])
    t = a
    while t < b:
        note = rng.choice([86, 88, 90, 93, 95, 98])
        s = ton(hz(note), 0.6, (1, 3.0), (1, 0.2), abkling=0.12) * 0.035
        p = rng.random()
        setze(s, t, 1 - p * 0.8, 0.2 + p * 0.8)
        t += 0.045 + rng.random() * 0.05
    # 5) Schlussakkord + tiefer Grundton, wenn die Schrift steht.
    a = sek(m["MORPH"][1]) - 0.2
    for note, w in ((26, 0.22), (38, 0.12), (50, 0.08), (54, 0.06), (57, 0.06), (62, 0.05), (66, 0.04)):
        s = ton(hz(note), dauer - a, (1, 2), (1, 0.2), abkling=2.2) * w
        setze(s, a)
    mix = np.stack([L, R], axis=1)
    mix = np.stack([hall(mix[:, 0], np.random.default_rng(1)), hall(mix[:, 1], np.random.default_rng(2))], axis=1)
    mix *= huelle(n, 0.05, 1.2)[:, None]  # Ausblenden am Ende
    return mix / np.abs(mix).max() * 10 ** (-1 / 20)  # Spitze −1 dBFS


def main() -> int:
    out = Path(sys.argv[sys.argv.index("--out") + 1]) if "--out" in sys.argv else \
        Path.home() / "sharefyx-film" / "ton.wav"
    m = marken()
    dauer = m["FRAMES"] / m["FPS"]
    pcm = (mischen(dauer, m) * 32767).astype("<i2")
    with wave.open(str(out), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(pcm.tobytes())
    print(json.dumps({"wav": str(out), "sekunden": dauer,
                      "sha256": hashlib.sha256(out.read_bytes()).hexdigest()}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
