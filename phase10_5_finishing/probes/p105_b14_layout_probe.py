#!/usr/bin/env python3
"""P10.5 Block 14, Schritt 14.0 — die **Basislinie** des Kartenlayouts.

Der Nikinger (2026-10-26, nach den 5x30-Bildern `p105_b15_0{3,4,5}`): „die Karte selbst ist
grossartig, aber das Layout sieht einfach nicht gut aus. Wie Minecraft: Chunks werden zufaellig
generiert, aber nach einer bestimmten Logik angepasst — zufaellig, aber in einer Ordnung."
Plan: `docs/concepts/phase10_5_block14_kartenlayout_plan.md` (§2 das Prinzip, §5 die Abnahme).

**Diese Probe ist Schritt 14.0 des Plans:** sie misst **gegen den heutigen Code** und legt die
**Basislinie** fest. Die Basislinie ist in **Regionen** und **Kamera** bewusst **rot** — das ist
der Beleg, dass die Zellen wirklich messen (ein gruener Baseline-Lauf waere eine Zelle, die
nichts prueft).

**Wegwerf-Instanz** (Plan §6): **freier Port je Lauf**, tmp-`DATA_ROOT` mit **eigenem Baum je
Lauf**, tmp-`auth.sqlite3`, **TLS**, Umgebung **ohne** `SHAREFYX_*`/`SFX_*`/`SPACE_*`, Stopp
**nur** ueber die PID-Datei (Hard Rule 9: nie `pkill -f`, nie der systemd-Dienst). Der Server
laeuft aus dem Projekt-`.venv`, der Browser-Teil aus `~/.claude-code-tools/e2e-venv` (dort
liegt Playwright) — dieselbe Aufteilung wie `p105_b15_screens.py`.

**Warum TLS und nicht http:** `require_csrf()` vergleicht den Origin-Header des Browsers gegen
`SPACE_PUBLIC_BASE_URL` (`webui/security.py`), und die Auth-Konfiguration **verlangt https**
(`authserver/config.py`). Ohne TLS kann der Browser **nicht schreiben** — und diese Probe muss
Items anlegen (Zelle P10.5-68). Muster: `phase10_inventory/probes/p10_wegwerf.py`
(`SERVE_TLS_LAUNCHER`); dort ist derselbe Grund notiert.

**Gemessen wird ueber Positionen, nicht ueber Pixel** (Plan §4): nach dem Einschwingen schreibt
`saveLayout()` alle `x, y` in den `localStorage` — die Probe liest sie (`page.evaluate`) und
verbindet sie mit `/api/v1/graph` (Space, Ordner). **Kein** Test-Haken im Produktcode. Pixel
werden nur an **zwei** Stellen gelesen, wo es keine Alternative gibt: die **Kernpositionen**
(die Kamera-Transformation zu schaetzen) und die **Beschriftungs-Rechtecke** (P10.5-71 verlangt
ausdruecklich „Rechtecke ueber `measureText` nachgerechnet").

> **Datierte Aenderung der Beschriftungs-Messung (2026-10-27, Schritt 14.35).** Die
> *Menge* der gezeichneten Beschriftungen wird jetzt an den **`fillText`-Aufrufen** des letzten
> Bildes gemessen (ein Recorder an der Leinwand-API des Browsers — wieder **kein** Haken im
> Produktcode), nicht mehr an den Pixeln. Grund: die neue Regel **laesst** ueberlappende
> Beschriftungen **weg**, und an den Pixeln ist ein *weggelassenes* Rechteck nicht von einem
> *gezeichneten* zu unterscheiden — zwei ueberlappende Rechtecke teilen sich ihre Pixel. Der
> Pixelbeweis bleibt fuer die **Fokus-Beschriftung** (sie muss wirklich auf der Leinwand
> stehen). Die **Rechtecke** selbst werden weiterhin ueber `ctx.measureText` nachgerechnet
> (Plan §5).

| Zelle | Abnahme | was gemessen wird | gruen, wenn |
|---|---|---|---|
| `determinismus` | P10.5-65 | zwei frische Ladevorgänge (leerer Speicher) → max. Abweichung | ≤ 1 px |
| `regionen` | P10.5-66 | Anteil der Knoten, deren **eigener** Space-Schwerpunkt der naechste ist | ≥ 95 % |
| `kamera` | P10.5-67 | Fuellgrad des Inhalts (Zoom × Welt-Umriss) auf einer Achse | ≥ 60 % **und** der Inhalt passt **und** der Umriss sitzt in der Mitte (≤ 3 px) |
| `stabilitaet` | P10.5-68 | Median-Verschiebung der Knoten **anderer** Spaces nach +1 Item; neues Item in der Region seines Space | ≤ 2 px **und** in der Region |
| `budget` | P10.5-69 | 200 Knoten bis Ruhe · reduced motion 0 Frames | ≤ 3000 ms · 0 Frames |
| `beschriftungen` | P10.5-71 | gezeichnete Beschriftungs-Rechtecke (Fokus + erster Ring) | keine zwei ueberlappen, Fokus immer da |

**Das Fenster der Messung:** 1920x1200 — die Groesse, in der der Nikinger die Kartenbilder
aufgenommen hat (`p105_b15_screens.py`, „1920x1200, Zoom 50 %"). Die Leinwand der Karte ist
der Detail-Slot des Panels; ihre Groesse folgt dem Fenster.

**Zur Kamera-Zelle (datierte Praezisierung, 2026-10-26):** die Abnahmezeile sagt „fuellt der
Inhalt ≥ 60 % der Leinwand auf mindestens einer Achse". Ein **unteres** Mass allein kann die
Zelle nicht tragen: waere der Inhalt **groesser** als die Leinwand, waere der Fuellgrad *ueber*
100 % und die Zelle gruen, obwohl der Nutzer den groessten Teil der Karte nie sieht. Gemessen
wird deshalb **drei** Stuecke (der **heutige** Stand passt — `passt` ist `true`; die Zelle
sichert den Zustand **nach** dem Umbau ab, nicht den von heute):

| Teil | Plan | was |
|---|---|---|
| `fuellgrad` | P10.5-67 | ≥ 60 % der Leinwand auf einer Achse (Zoom × Welt-Umriss) |
| `passt` | Plan §2.5 | der Inhalt passt **in** die Leinwand (sonst ist er beschnitten) |
| `zentriert` | Plan §2.5 („Pan auf die Mitte") | der Umriss liegt in der Leinwandmitte (≤ 3 px) |

Erst mit `passt` und `zentriert` ist der Gegenlauf „`fitView()` aus" (Plan §5) ueberhaupt
erkennbar: `fitView()` setzt genau diese beiden Eigenschaften (Zoom so, dass der Inhalt passt,
Pan auf die Mitte).

**Die Kamera wird zweimal gemessen (Schritt 14.3).** Einmal in der Abnahme-Zelle (152 Knoten)
und einmal in der **Budget-Zelle** (201 Knoten) — dort als `kamera_200_knoten`. Der Grund ist
**E3** (Plan §2.5): reicht `ZOOM_MIN` (0,5) bei 200 Knoten, oder muss der Ausfuehrer ihn senken
(Untergrenze 0,2)? Wuerde der Zoom auf `ZOOM_MIN` abgeklemmt, stuende die Anzeige genau auf
50 % **und** der Inhalt passte nicht in die Leinwand — beides steht im Beleg.

Aufruf:  `.venv/bin/python phase10_5_finishing/probes/p105_b14_layout_probe.py`
Ergebnis: `phase10_5_finishing/probes/p105_b14_layout_probe.json`

**Rueckgabewert 0 = die Probe ist gelaufen.** Ob eine Zelle gruen ist, steht im JSON — die
Basislinie (Schritt 14.0) ist in `regionen` und `kamera` **rot**, und das ist gewollt. Die
roten Zellen stehen zusaetzlich auf stderr (`ROT: [...]`).
"""
from __future__ import annotations

import base64
import json
import os
import re
import secrets
import signal
import ssl
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
WEGWERF_ROOT = Path("/tmp/opencode/sharefyx-wegwerf-b14")
PID = os.getpid()
DATA_ROOT = WEGWERF_ROOT / ("data-%d" % PID)
AUTH_DB = WEGWERF_ROOT / ("auth-%d.sqlite3" % PID)
#: Der DEK liegt in einem **eigenen** Credential-Verzeichnis je Lauf: der Server liest
#: `CREDENTIALS_DIRECTORY/auth-dek` — ein gemeinsames `auth-dek` wuerde bei zwei Laufen
#: umkompiliert und den TOTP-Seed des anderen Laufs unentschluesselbar machen.
CRED_DIR = WEGWERF_ROOT / ("cred-%d" % PID)
DEK_FILE = CRED_DIR / "auth-dek"
SERVE_PID = WEGWERF_ROOT / ("serve-%d.pid" % PID)
SERVE_LOG = WEGWERF_ROOT / ("serve-%d.log" % PID)
TLS_KEY = WEGWERF_ROOT / ("key-%d.pem" % PID)
TLS_CERT = WEGWERF_ROOT / ("cert-%d.pem" % PID)
AUFTRAG_DATEI = WEGWERF_ROOT / ("auftrag-%d.json" % PID)
#: Der Beleg-Dateiname. **Ein Gegenlauf schreibt in eine eigene Datei** — der Normalfall-Beleg
#: (die Abnahme) darf nie von einem Gegenlauf ueberschrieben werden.
RESULT = Path(__file__).resolve().with_name("p105_b14_layout_probe.json")
SPACE = "alpha"

#: Fuenf Spaces, je ein Satz Items. **Abweichung vom Plan-Seed (5x30), datiert 2026-10-26:**
#: `beta` hat **32** Items, die anderen vier je 30 (zusammen **152** Knoten) — damit ist „der groesste Space" eindeutig
#: (`beta`). Der Plan §2.1 verlangt genau das: ein neues Item verschiebt die Anker **nur**, wenn
#: es den **groessten** Space vergroessert. Bei fuenf gleich grossen Spaces waere „nicht-groesster
#: Space" undefiniert — und der Test waere unmoeglich, ohne die Regel selbst zu verbiegen.
SPACES = ["alpha", "beta", "gamma", "delta", "epsilon"]
ITEMS_PRO_SPACE = {"alpha": 30, "beta": 32, "gamma": 30, "delta": 30, "epsilon": 30}
#: Der Space, in dem die Probe ein Item anlegt (fremd, aber mit Schreibrecht — der Probe
#: braucht den Write, um P10.5-68 messen zu koennen).
WACHSER_SPACE = "epsilon"
#: So viele Items werden am Ende **zusaetzlich** angelegt, damit die Budget-Zelle bei
#: **200 Knoten** gemessen wird (P10.5-69 nennt 200 Knoten, nicht 151).
EXTRA_ITEMS = 200 - sum(ITEMS_PRO_SPACE.values())

PORT = 0
BASE = ""

# -- Die Gegenläufe (Plan §5) ----------------------------------------------------------------------
#
# Ein Wächter ohne Gegenlauf beweist nichts: eine Messung, die die falsche Sache misst, ist
# grün und falsch zugleich (diese Fehlerklasse hat dieser Ordner zweimal gesehen). Jeder
# Gegenlauf **patcht genau eine Regel** in einer Kopie von `graph.js` (der Arbeitsbaum bleibt
# unberührt) und muss **genau die** zugehörige Zelle rot machen.
#
# | Gegenlauf | Regel (Plan) | Zelle | der Fehler |
# |---|---|---|---|
# | `zentrum` | §2.4 -- die Gravitation zieht zum **eigenen Space-Anker** | `regionen` | sie zieht zur Leinwandmitte (das ist der Stand von 14.1) |
# | `querfeder` | §2.4 -- die Querfeder ist **schwach und lang** | `stabilitaet` | sie ist so stark und kurz wie die Feder im Space |
# | `alpha` | §2.4 -- die Startenergie ist die **gesäte** | `budget` | `ALPHA_START_SEEDED` → 1 und `ALPHA_DECAY` → 0,995 (die Simulation reisst das 3-s-Budget) |
# | `fitview` | §2.5 -- die Kamera **passt sich ein** | `kamera` | `fitView()` ist aus (das ist der Stand von 14.2) |
# | `beschriftung` | §2.7 -- die Beschriftungen **überlappen sich nicht** | `beschriftungen` | die Kollisionsprüfung ist aus (das ist der Stand von 14.2) |
# | `region` | §2.1 L1 -- **eine Region je Space** | `regionen` | der zweite Space bekommt **keine eigene Region** (sein Abstand ist null) |
#
# **`zentrum` und `region` (datierte Korrektur, Schritt 14.4):** der Plan §5 nannte für
# **P10.5-66** den Gegenlauf "`ANCHOR_GRAVITY` → Leinwandmitte". **Gemessen:** dieser
# Gegenlauf macht **keine** Zelle rot (14.2) — er wirkt auf die **Weltgröße**, nicht auf die
# Regionen-Zelle. Der Gegenlauf, der die Zelle **wirklich** rot macht, ist `region`: er bricht
# die Regel, die sie misst (**eine Region je Space**).
#
# **Die Anker sind eindeutig** (Regel + Nachbarzeile, nicht nur ein Wert) -- sonst patcht der
# Gegenlauf den Kommentar über der Regel statt der Regel.
GEGENLAEUFE = {
    "zentrum": {
        "var anker = spaceRegions && spaceRegions.spaces ? spaceRegions.spaces[node.space] : null;":
            "var anker = {x: cssWidth / 2, y: cssHeight / 2};",
    },
    "querfeder": {
        "var quer = aa.space !== bb.space;": "var quer = false;",
    },
    "alpha": {
        "const ALPHA_START_SEEDED = 0.5;": "const ALPHA_START_SEEDED = 1;",
        "const ALPHA_DECAY = 0.97;": "const ALPHA_DECAY = 0.995;",
    },
    # **14.3: die Kamera passt sich nicht ein.** Der Anker ist die **erste Zeile des
    # Rumpfes** von `fitView()` -- sie wird durch ein bedingungsloses `return;` ersetzt, die
    # Funktion ist damit ein No-op (Plan §5: der Gegenlauf zu P10.5-67 ist "fitView() aus").
    # Nicht der Aufrufer wird gepatcht: sonst bliebe der Doppelklick (der `fitView()` ruft)
    # wirksam, und der Gegenlauf maesste nicht die Regel, sondern nur ihren Aufrufer.
    "fitview": {
        "  if (nodes.length === 0 || cssWidth <= 0 || cssHeight <= 0) return;":
            "  return;  // Gegenlauf 14.3: fitView() ist aus",
    },
    # **14.35: die Kollisionspruefung der Beschriftungen ist aus.** Der Anker ist die
    # **Regel + Nachbarzeile** (die erste Zeile des Rumpfes von `labelRectOverlaps()` plus die
    # Schleife darunter) -- gepatcht wird die *Regel*, nicht ihr Aufrufer: sonst wuerde der
    # Aufrufer (`drawLabels()`) noch immer die Rechtecke sammeln, und der Gegenlauf wuerde
    # nicht die Ueberlappung, sondern nur den Wegfall der *Pruefung* messen.
    "beschriftung": {
        "function labelRectOverlaps(rect, belegt) {\n  for (var i = 0; i < belegt.length; i++) {":
            "function labelRectOverlaps(rect, belegt) {\n"
            "  return false;  // Gegenlauf 14.35: die Kollisionspruefung ist aus\n"
            "  for (var i = 0; i < belegt.length; i++) {",
    },
    # **14.4: die Regionen-Zuordnung des Spaces verschieben.** Die Regel (Plan §2.1, L1): "eine
    # **Region je Space**". Der Gegenlauf legt **alle** Anker auf **einen** Punkt -- es gibt
    # dann nur noch **eine** Region statt einer je Space (derselbe Gegenlauf wie im Seed-Harness
    # `anker`: die Regel wird in beiden Schichten gebrochen).
    #
    # **Warum *alle* Anker und nicht einer (gemessen, Schritt 14.4):** die Browser-Probe misst
    # die **entspannte** Karte, und die **Anker-Gravitation repariert** eine verschobene
    # Region: der verschobene Cluster wird von der Repulsion wieder herausgeschoben (gemessen:
    # der zweite Space bekommt den Anker des eigenen => der Cluster liegt **205 px** daneben,
    # die Regions-Zelle bleibt **grün** bei 100 %; verschiebt man nur die *Ordner-Inseln*,
    # bleiben 97,4 % bzw. 98,7 % grün). **Erst wenn kein Space einen eigenen Anker hat, bleiben
    # die Items ineinander** -- dann wird die Zelle rot (92,1 % statt 95 %).
    #
    # **Der Anker ist die Regelzeile** (die eine Zeile, die den **Abstand** der Region vom
    # Anker bestimmt) -- gepatcht wird die *Platzierung der Region*, nicht ihr Radius.
    "region": {
        "    var abstand = k === 0 ? 0 : slot * Math.sqrt(k);":
            "    var abstand = 0;",
    },
}



#: Der Gegenlauf dieses Laufs (`None` = der Normalfall).
GEGENLAUF = None
#: **Die Startwert-Messung (Schritt 14.4).** Die vier L4-Konstanten des Plans (§2.4) sind
#: **Startwerte** — "in 14.4 werden sie **gemessen** (nicht gesetzt)" (Plan §2.4, datiert
#: 2026-10-26). Ein Lauf mit `--konstante=NAME=WERT` patcht die Konstante in der **Kopie**
#: der statischen Dateien (der Arbeitsbaum bleibt unberührt, wie bei einem Gegenlauf) und
#: schreibt seinen Beleg in eine **eigene** Datei — der Normalfall-Beleg darf nie von einer
#: Messvariante überschrieben werden.
#:
#: **Warum die Option und kein neuer Gegenlauf:** ein Gegenlauf macht eine Zelle **rot** und
#: belegt damit, dass die Zelle die Regel misst. Eine Messvariante dagegen **misst** die
#: Wirkung eines Wertes — sie beantwortet die Frage "welcher Wert ist der richtige?".
#: Beides ist derselbe Mechanismus (ein Patch in einer Kopie), aber mit anderem Ziel.
KONSTANTEN: dict[str, str] = {}
#: Der Dateiname des Belegs (ohne `--label` aus den Werten gebildet).
LABEL = ""
for _arg in sys.argv[1:]:
    if _arg.startswith("--gegenlauf="):
        GEGENLAUF = _arg.split("=", 1)[1]
    elif _arg.startswith("--konstante="):
        _name, _, _wert = _arg.split("=", 1)[1].partition("=")
        KONSTANTEN[_name.strip()] = _wert.strip()
    elif _arg.startswith("--label="):
        LABEL = _arg.split("=", 1)[1].strip()
if GEGENLAUF is not None and GEGENLAUF not in GEGENLAEUFE:
    raise SystemExit("unbekannter Gegenlauf: %s (bekannt: %s)"
                     % (GEGENLAUF, ", ".join(sorted(GEGENLAEUFE))))
if GEGENLAUF is not None and KONSTANTEN:
    raise SystemExit("ein Lauf ist entweder ein Gegenlauf oder eine Messvariante — nicht beides")
if KONSTANTEN and not LABEL:
    LABEL = "_".join("%s%s" % (n, w) for n, w in sorted(KONSTANTEN.items()))

#: Die **Block-14-Konstanten** (Plan §2) — sie stehen im Beleg, damit der Leser weiss,
#: mit welchen Werten gemessen wurde. Der Wert kommt aus der **echten** `graph.js` (nach dem
#: Patch), nicht aus einer Dublette hier.
#:
#: **`LOBE_CLOSE_PX` (Plan 14.6 §2.2)** — der Schliess-Radius der Koerpermaske. Die Zeile
#: steht hier **ab Schritt 14.6.0**, damit `--konstante=LOBE_CLOSE_PX=…` die Messvariante
#: meldet. `_konstanten_werte()` liest die Werte aus dem **echten** Quelltext: die Konstante
#: steht erst ab 14.6.1 in `graph.js` (dort kommt der Algorithmus) — bis dahin fehlt sie im
#: Beleg, ohne dass ein Lauf still scheitert (`_konstanten_patch()` sagt **laut** Bescheid,
#: wenn jemand einen Wert setzen will, den es noch nicht gibt).
BLOCK14_KONSTANTEN = [
    "REGION_ITEM_STEP", "REGION_PAD", "REGION_GAP", "ISLAND_FACTOR", "ITEM_STEP",
    "ITEM_JITTER_PX", "GOLDEN_ANGLE", "ANCHOR_GRAVITY", "CROSS_SPRING_FACTOR",
    "CROSS_SPRING_LENGTH_FACTOR", "ALPHA_START_SEEDED", "FIT_MARGIN", "LOBE_CLOSE_PX",
    # Plan 14.7 (Schritt 14.7.1): die drei Hebel und die Glaettung
    "ANCHOR_LAYOUT", "ANCHOR_HEX_ORDER", "LOBE_SCALE", "LOBE_SMOOTH_PASSES",
]

#: **Das Messpflaster** (Schritt 14.6.0): ein Patch, der **keinen Fehler** einbaut, sondern
#: sichtbar macht, was die Regel tut (Muster: `p105_b8_c2_probe.mjs`, `globalThis.__furrowCells`).
#: Die Bilder-Probe traegt ihr Pflaster hier ein (`GRAPH_PATCH_EXTRA`) — der Weg ist derselbe
#: wie bei einem Gegenlauf: der **Arbeitsbaum bleibt unberuehrt**, der Server serviert eine
#: **Kopie** der statischen Dateien.
GRAPH_PATCH_EXTRA: dict = {}


def _graph_text() -> str:
    return (REPO_ROOT / "phase5_ui" / "webui" / "static" / "js" / "graph.js").read_text(
        encoding="utf-8")


def _konstanten_patch() -> dict:
    """Der Patch der Messvariante: `const NAME = alt;` → `const NAME = neu;`.

    Der Anker wird aus der **echten** `graph.js` gelesen (nicht hier wiederholt) — sonst
    wäre die Dublette die stille Abweichung, die dieser Ordner zweimal getroffen hat."""
    text = _graph_text()
    patch = {}
    for name, wert in KONSTANTEN.items():
        treffer = re.search(r"^const %s = ([^;]+);" % re.escape(name), text, re.M)
        if not treffer:
            raise SystemExit("Konstante steht nicht in graph.js: " + name)
        alt = "const %s = %s;" % (name, treffer.group(1))
        if alt in patch:
            raise SystemExit("zwei Konstanten mit demselben Anker: " + alt)
        patch[alt] = "const %s = %s;" % (name, wert)
    return patch


def _konstanten_werte(text: str) -> dict:
    """Die Werte der Block-14-Konstanten in einem (ggf. gepatchten) Quelltext."""
    werte = {}
    for name in BLOCK14_KONSTANTEN:
        treffer = re.search(r"^const %s = ([^;]+);" % re.escape(name), text, re.M)
        if treffer:
            werte[name] = treffer.group(1)
    return werte

# -- Der TLS-Launcher: dieselbe App wie `phase2_mcp/scripts/serve.py`, plus TLS ----------------
# (Muster aus `phase10_inventory/probes/p10_wegwerf.py :: SERVE_TLS_LAUNCHER`.)
SERVE_TLS_LAUNCHER = '''"""Dieselbe App wie phase2_mcp/scripts/serve.py, plus TLS."""
import os, sys, json
sys.path.insert(0, os.environ["REPO_ROOT"])
from datetime import datetime, timedelta, timezone
import uvicorn
import storage.files as sfiles
import storage.store as sstore

# **Deterministische Item-IDs auch fuer die serverseitig erzeugten Items.** `files.generate_id()`
# zieht `secrets.token_hex(4)` — zufaellig. Der Saat-Jitter ist ein **Hash der ID**
# (`graph.js :: seedJitter()`), also fliegt die Karte bei jedem Item mit zufaelliger ID an
# eine andere Stelle: gemessen war der Median-Verschiebungswert der Stabilitaets-Zelle
# laufverschieden (287 px gegen 227 px bei identischem Code und identischem Datensatz).
# Die IDs der Seed-Items enden bei 0x98 — der Zaehler hier startet darueber.
_z = [0x900]
def _feste_id():
    _z[0] += 1
    return 'itm_%08x' % _z[0]
sfiles.generate_id = _feste_id

# **Eingefrorene Uhr mit Zaehler.** `store.search()` sortiert nach `-updated` (der Index
# liefert `ORDER BY id`) — die Item-Zeitstempel sind die Wanduhr, also wechselt die
# **Reihenfolge** der Knoten in `/api/v1/graph` und damit der Saat-Ring der Karte, sobald
# zwei Items ueber eine Sekundengrenze fallen. Gemessen: die 48 Extra-Items standen im
# einen Lauf mit 0x91a..., im anderen mit 0x92c... vorn — die Karten waren nicht dieselben.
# Der Zaehler gibt jedem **neu angelegten** Item einen eigenen, streng wachsenden
# Zeitstempel (2026-01-02 12:00 + n Sekunden — juenger als der Seed-Stand 2026-01-01),
# damit bleibt die Reihenfolge bei jedem Lauf dieselbe.
_n = [0]
def _now():
    return datetime(2026, 1, 2, 12, 0, 0, tzinfo=timezone.utc) + timedelta(seconds=_n[0])
_orig_create = sstore.Store.create
def _create(self, *args, **kwargs):
    _n[0] += 1
    return _orig_create(self, *args, **kwargs)
sstore.Store.create = _create

from authserver.config import load_auth_settings, load_data_encryption_key
from authserver.store import AuthStore
from authserver.userdir import UserDirectory
from storage.store import Store
import mcpserver.app as mapp
from mcpserver.app import OAuthConfig, create_app
from mcpserver.config import load_settings
from mcpserver.logging_setup import configure_logging
from mcpserver.request_log import AccessLogASGI, OAuthLogASGI

# **Der Gegenlauf (Schritt 14.2).** Die statischen Dateien werden aus einer **Kopie** serviert,
# in der `graph.js` **gepatcht** ist -- die Arbeitskopie im Repo bleibt unberuehrt (ein
# Gegenlauf darf den Arbeitsbaum nie veraendern). `UiSettings.static_dir` zeigt dann auf die
# Kopie (`create_app()` baut die `UiSettings` selbst -- deshalb wird das Symbol im
# `mcpserver.app`-Modul ersetzt, nicht in `webui.config`).
_patched = os.environ.get("GRAPH_PATCH")
if _patched:
    import shutil
    from pathlib import Path
    _quelle = Path(os.environ["REPO_ROOT"]) / "phase5_ui" / "webui" / "static"
    _kopie = Path(os.environ["STATIC_DIR"])
    if _kopie.exists():
        shutil.rmtree(_kopie)
    shutil.copytree(_quelle, _kopie)
    _datei = _kopie / "js" / "graph.js"
    _text = _datei.read_text(encoding="utf-8")
    for _alt, _neu in json.loads(_patched).items():
        if _alt not in _text:
            raise SystemExit("Gegenlauf-Anker nicht gefunden: " + _alt[:60])
        _text = _text.replace(_alt, _neu)
    _datei.write_text(_text, encoding="utf-8")
    _orig_settings = mapp.UiSettings
    def _settings_mit_kopie(**kwargs):
        kwargs["static_dir"] = _kopie
        return _orig_settings(**kwargs)
    mapp.UiSettings = _settings_mit_kopie

settings = load_settings()
configure_logging(settings.log_level)
auth_settings = load_auth_settings()
auth_store = AuthStore(auth_settings.db_path, now_fn=lambda: datetime.now(timezone.utc))
users = UserDirectory(auth_store, dek=load_data_encryption_key())
oauth = OAuthConfig(settings=auth_settings, store=auth_store, users=users)
app = create_app(settings=settings, store=Store(settings.data_root, now_fn=_now),
                 allowed_hosts=["127.0.0.1"], oauth=oauth)
app = AccessLogASGI(OAuthLogASGI(app))
uvicorn.run(app, host=settings.host, port=settings.port, access_log=False,
            log_level=settings.log_level.lower(),
            ssl_keyfile=os.environ["TLS_KEY"], ssl_certfile=os.environ["TLS_CERT"])
'''


def _freier_port() -> int:
    """Ein freier TCP-Port auf dem Loopback (binden auf 0, dann schliessen)."""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


def _saubere_umgebung() -> dict:
    """Umgebung ohne `SHAREFYX_*`/`SFX_*`/`SPACE_*` (Plan §6) — sonst wuerde eine in der
    Login-Shell stehende `SPACE_DATA_ROOT`-Zeile die Wegwerf-Instanz still gegen den echten
    Datenwurzelbaum laufen lassen."""
    env = os.environ.copy()
    for name in list(env):
        if name.startswith(("SHAREFYX_", "SFX_", "SPACE_")):
            env.pop(name)
    return env


def _setup() -> dict:
    """DEK + Wegwerf-Konto `alpha` (Passwort + TOTP) im tmp-`auth.sqlite3`."""
    WEGWERF_ROOT.mkdir(parents=True, exist_ok=True)
    CRED_DIR.mkdir(parents=True, exist_ok=True)
    DATA_ROOT.mkdir(parents=True, exist_ok=True)
    raw = secrets.token_bytes(32)
    DEK_FILE.write_bytes(base64.urlsafe_b64encode(raw).rstrip(b"=") + b"\n")
    os.chmod(DEK_FILE, 0o600)

    from authserver import passwords, totp
    from authserver.config import decode_data_encryption_key
    from authserver.secretbox import seal
    from authserver.store import AuthStore

    password = "wegwerf-b14-" + secrets.token_urlsafe(8)
    secret_b32 = totp.generate_secret()
    dek = decode_data_encryption_key(DEK_FILE.read_text().strip(), origin=str(DEK_FILE))
    store = AuthStore(str(AUTH_DB), now_fn=lambda: datetime.now(timezone.utc))
    store.upsert_user(
        space=SPACE,
        password_hash=passwords.hash_password(password),
        totp_secret_enc=seal(secret_b32.encode("ascii"), key=dek, aad=SPACE.encode("utf-8")),
        totp_alg="SHA1",
        totp_confirmed_at=datetime.now(timezone.utc),
        status="active",
    )
    store.set_totp_counter(SPACE, 0)
    return {"space": SPACE, "password": password, "secret": secret_b32}


def _seed() -> None:
    """Die Datenlage: fuenf Spaces mit Items, Ordnern, Ring-Kanten, einem **Hub** je Space
    (fuer P10.5-71: ein Knoten mit >= 5 Nachbarn) und Kanten quer zwischen den Spaces.

    `alpha` darf in allen vier fremden Spaces **lesen und schreiben** — die Reads, damit die
    Karte alle fuenf Spaces zeigt, die Writes, damit die Probe das Item fuer P10.5-68
    anlegen kann."""
    import shutil
    shutil.rmtree(DATA_ROOT, ignore_errors=True)
    DATA_ROOT.mkdir(parents=True, exist_ok=True)
    code = (
        "import sys; sys.path.insert(0, 'phase1_storage')\n"
        "from pathlib import Path\n"
        "from datetime import datetime, timezone\n"
        "import storage.files as sfiles\n"
        "from storage.store import Store\n"
        "from storage.acl import create_space, add_member\n"
        # **deterministische Item-IDs**: `files.generate_id()` zieht `secrets.token_hex(4)` —
        # zufaellig. Die Karte ist zwar deterministisch (der Jitter ist ein Hash der ID), aber
        # ohne feste IDs ist der **Datensatz** zufaellig: gemessen lagen die Welt-Umrisse
        # zwischen 383x629 px und 711x897 px (Fuellgrad 73 % bis 104 %) — die Basislinie waere
        # damit nicht reproduzierbar. Muster: `phase8_ui_graph/scripts/wegwerf_setup_200knoten.py`
        # ("deterministisch generiert, kein Zufall -- die Messung soll reproduzierbar sein").
        "_zaehler = [0]\n"
        "def _feste_id():\n"
        "    _zaehler[0] += 1\n"
        "    return 'itm_%08x' % _zaehler[0]\n"
        "sfiles.generate_id = _feste_id\n"
        f"root = Path({str(DATA_ROOT)!r})\n"
        f"spaces = {SPACES!r}\n"
        f"counts = {ITEMS_PRO_SPACE!r}\n"
        "for sp in spaces: create_space(root, sp)\n"
        "for sp in spaces[1:]: add_member(root, sp, 'alpha', write=True)\n"
        # **feste Zeitstempel.** `store.search()` sortiert nach `-updated` (der Index liefert\n"
        "# `ORDER BY id`), und die Item-Zeitstempel sind die **Wanduhr**: ohne feste Zeit ist\n"
        "# die **Reihenfolge** der Knoten in `/api/v1/graph` von Lauf zu Lauf verschieden --\n"
        "# und damit der Saat-Ring der Karte (er wird nach Index gesetzt). Gemessen: die\n"
        "# Welt-Umrisse lagen zwischen 596x889 px und 463x1020 px. Mit festem `now_fn` ist die\n"
        "# Sortierung stabil (alle Zeitstempel gleich) und die Reihenfolge die Index-Reihenfolge.\n"
        "s = Store(root, git=False,\n"
        "          now_fn=lambda: datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc))\n"
        "typen = [('task','open'), ('task','doing'), ('task','done'), ('note','active'), ('note','active')]\n"
        "worte = ['Plan', 'Notiz', 'Idee', 'Frage', 'Antwort', 'Tabelle', 'Skizze', 'Protokoll', 'Liste', 'Entwurf']\n"
        "ids = {}\n"
        "for sp in spaces:\n"
        "    ids[sp] = []\n"
        "    n = counts[sp]\n"
        "    for i in range(n):\n"
        "        typ, st = typen[i % 5]\n"
        "        it = s.create(sp, type=typ, status=st,\n"
        "                      title='%s %s %02d' % (sp.title(), worte[i % 10], i + 1),\n"
        "                      folder='ordner-%d' % (i % 4 + 1),\n"
        "                      tags=['netz', 'gruppe-%d' % (i % 3 + 1)])\n"
        "        ids[sp].append(it.id)\n"
        "# die Kanten: Ring (j+1, j+7), jeder fuenfte quer in den naechsten Space, und der\n"
        "# **Hub** (das erste Item verweist auf sechs weitere) -- P10.5-71 verlangt einen\n"
        "# Fokus-Knoten mit >= 5 Nachbarn.\n"
        "for k, sp in enumerate(spaces):\n"
        "    eigene = ids[sp]; n = len(eigene)\n"
        "    nachbar = ids[spaces[(k + 1) % len(spaces)]]\n"
        "    for j, ziel in enumerate(eigene):\n"
        "        kandidaten = [eigene[(j + 1) % n], eigene[(j + 7) % n]]\n"
        "        if j % 5 == 0: kandidaten.append(nachbar[j % len(nachbar)])\n"
        "        if j == 0: kandidaten += eigene[1:7]\n"
        "        links = []\n"
        "        for x in kandidaten:\n"
        "            if x not in links: links.append(x)\n"
        "        s.update(ziel, version=1, links=links)\n"
        "s.rebuild_index()\n"
        "print('geseedet:', {sp: len(v) for sp, v in ids.items()})\n"
    )
    subprocess.run([".venv/bin/python", "-c", code], check=True, cwd=str(REPO_ROOT),
                   env={**_saubere_umgebung(), "PYTHONPATH": str(REPO_ROOT / "phase1_storage")})


def _serve() -> int:
    """Der Wegwerf-Server auf TLS (eigener Port, eigener Datenbaum, PID-Datei).
    **Faellt der Health-Check durch, wird der Server gestoppt** — sonst bliebe er zurueck
    und haelte den Port (die Falle aus Block 13)."""
    env = _saubere_umgebung()
    env["SPACE_DATA_ROOT"] = str(DATA_ROOT)
    env["SPACE_AUTH_DB"] = str(AUTH_DB)
    env["SPACE_PUBLIC_BASE_URL"] = BASE
    env["SPACE_PORT"] = str(PORT)
    env["CREDENTIALS_DIRECTORY"] = str(CRED_DIR)
    env["PYTHONPATH"] = str(REPO_ROOT)
    env["REPO_ROOT"] = str(REPO_ROOT)
    env["TLS_KEY"] = str(TLS_KEY)
    env["TLS_CERT"] = str(TLS_CERT)
    if GEGENLAUF is not None:
        # **Der Gegenlauf:** der Server serviert eine **Kopie** der statischen Dateien, in der
        # `graph.js` gepatcht ist (der Arbeitsbaum bleibt unberuehrt).
        env["GRAPH_PATCH"] = json.dumps(GEGENLAEUFE[GEGENLAUF])
        env["STATIC_DIR"] = str(WEGWERF_ROOT / ("static-%d" % PID))
    elif KONSTANTEN:
        # **Die Messvariante (Schritt 14.4):** dieselbe Kopie, aber mit einem anderen
        # Startwert. Auch hier bleibt der Arbeitsbaum unberuehrt.
        env["GRAPH_PATCH"] = json.dumps(_konstanten_patch())
        env["STATIC_DIR"] = str(WEGWERF_ROOT / ("static-%d" % PID))
    if GRAPH_PATCH_EXTRA:
        # **Das Messpflaster (Schritt 14.6.0):** es baut **keinen Fehler** ein, es legt nur
        # die Zahlen offen, die die Karte im Inneren berechnet. Es wird **zusaetzlich** auf
        # dieselbe Kopie gepatcht (die Anker stehen in verschiedenen Zeilen — der
        # Gegenlauf-/Varianten-Patch fasst die Konstanten an, das Pflaster den Rumpf).
        patch = json.loads(env.get("GRAPH_PATCH", "{}"))
        patch.update(GRAPH_PATCH_EXTRA)
        env["GRAPH_PATCH"] = json.dumps(patch)
        env["STATIC_DIR"] = str(WEGWERF_ROOT / ("static-%d" % PID))


    subprocess.run(
        ["openssl", "req", "-x509", "-newkey", "rsa:2048", "-keyout", str(TLS_KEY),
         "-out", str(TLS_CERT), "-days", "2", "-nodes", "-subj", "/CN=127.0.0.1",
         "-addext", "subjectAltName=IP:127.0.0.1"],
        check=True, capture_output=True,
    )
    launcher = WEGWERF_ROOT / ("serve_tls_%d.py" % PID)
    launcher.write_text(SERVE_TLS_LAUNCHER, encoding="utf-8")
    log = SERVE_LOG.open("ab")
    proc = subprocess.Popen(
        [".venv/bin/python", str(launcher)],
        env=env, cwd=str(REPO_ROOT), stdout=log, stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    SERVE_PID.write_text(str(proc.pid))
    ctx = ssl._create_unverified_context()
    gesund = False
    try:
        for _ in range(80):
            try:
                urllib.request.urlopen(f"{BASE}/health", timeout=1, context=ctx).read()
                gesund = True
                break
            except Exception:
                time.sleep(0.25)
    finally:
        if not gesund:
            # der Server ist **nicht** gesund geworden: **erst stoppen, dann melden** — sonst
            # bliebe er zurueck und haelte den Port (die Falle aus Block 13)
            if proc.poll() is None:
                _stop()
    if not gesund:
        raise SystemExit("Wegwerf-Server wurde nicht gesund.")
    return proc.pid


def _lebt(pid: int) -> bool:
    """Lebt der Prozess **noch**?

    **Ein Zombie zaehlt nicht als lebend.** Der Probe-Prozess raeumt sein Kind nicht ab
    (`Popen` wird nicht geholt) — nach dem `SIGTERM` bleibt die PID als Zombie stehen, und
    `os.kill(pid, 0)` sagt weiterhin „lebt". Der Stopp wartete deshalb **zehn Sekunden** auf
    einen Prozess, den es nicht mehr gab (gemessen 2026-10-28, Schritt 14.6.0) und meldete
    dann faelschlich „beendete sich nicht — SIGKILL".
    """
    try:
        with open("/proc/%d/stat" % pid, "r", encoding="utf-8") as fh:
            zustand = fh.read().rsplit(")", 1)[1].split()[0]
    except FileNotFoundError:
        return False
    except OSError:
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return False
        return True
    return zustand != "Z"


def _stop() -> None:
    """Stopp **nur** ueber die PID-Datei (Hard Rule 9)."""
    if not SERVE_PID.exists():
        return
    pid = int(SERVE_PID.read_text().strip())
    try:
        os.kill(pid, signal.SIGTERM)
        for _ in range(40):
            time.sleep(0.25)
            if not _lebt(pid):
                return
        print(f"WARNUNG: Wegwerf-Server {pid} beendete sich nicht — SIGKILL.", file=sys.stderr)
        os.kill(pid, signal.SIGKILL)
    except ProcessLookupError:
        pass


# ============================================================================================
# Der Browser-Teil. Playwright liegt im e2e-venv, nicht im Projekt-venv — deshalb ein **eigenes
# Skript**, das seinen Auftrag ueber eine Datei bekommt (kein `.format()` auf einem Quelltext,
# in dem JavaScript steht).
# ============================================================================================

BROWSER_SKILL = r'''"""Der Browser-Teil der Block-14-Probe (Playwright, e2e-venv)."""
import base64, hashlib, hmac, json, math, struct, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

AUFTRAG = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
BASE = AUFTRAG["base"]
SPACE = AUFTRAG["space"]
RESULT = Path(AUFTRAG["result"])
REPO_ROOT = AUFTRAG["repo_root"]
AUTH_DB = AUFTRAG["auth_db"]
WACHSER_SPACE = AUFTRAG["wachser_space"]
EXTRA_ITEMS = AUFTRAG["extra_items"]
SPACES = AUFTRAG["spaces"]


def totp_now(secret_b32):
    key = base64.b32decode(secret_b32 + "=" * (-len(secret_b32) % 8))
    counter = int(time.time() // 30)
    digest = hmac.new(key, struct.pack(">q", counter), hashlib.sha1).digest()
    # Das LETZTE Byte des Digests (RFC 4226, §5.3) — `digest[0]` ist der falsche Offset.
    offset = digest[-1] & 0x0F
    code = (struct.unpack(">I", digest[offset:offset + 4])[0] & 0x7FFFFFFF) % 1000000
    return f"{code:06d}"


def totp_zuruecksetzen():
    """Jeder Login **verbraucht** einen TOTP-Schritt (`totp.verify(last_counter=...)`) — ein
    zweiter Login im selben 30-Sekunden-Fenster schlaegt deshalb mit 401 fehl. Muster aus
    `p105_b8_karte_probe.py :: _totp_zaehler_zuruecksetzen`."""
    code = (
        "from datetime import datetime, timezone\n"
        "from authserver.store import AuthStore\n"
        f"store = AuthStore({AUTH_DB!r}, now_fn=lambda: datetime.now(timezone.utc))\n"
        f"store.set_totp_counter({SPACE!r}, 0)\n"
    )
    subprocess.run([str(Path(REPO_ROOT) / ".venv" / "bin" / "python"), "-c", code], check=True)


# -- Die Hilfsfunktionen in der Seite ---------------------------------------------------------

KASTEN = r"""() => {
  const c = document.getElementById('overview-graph-canvas');
  if (!c) return null;
  const r = c.getBoundingClientRect();
  return {left: r.left, top: r.top, width: r.width, height: r.height,
          dw: c.width, dh: c.height, dpr: c.width / r.width};
}"""

ZOOM = r"""() => {
  const el = document.getElementById('overview-graph-zoom');
  if (!el) return null;
  const m = /(-?\d+)\s*%/.exec(el.textContent || '');
  return m ? parseInt(m[1], 10) / 100 : null;
}"""

ABLAGE = r"""() => {
  const ks = Object.keys(localStorage).filter(k => k.startsWith('sfx:graph:layout'));
  if (!ks.length) return null;
  const v = JSON.parse(localStorage.getItem(ks[0]));
  return {key: ks[0], v: v.v, pos: v.pos || {}};
}"""

GRAFIK = r"""async () => (await fetch('/api/v1/graph')).json()"""

NEUES_ITEM = r"""async (args) => {
  const tok = (document.getElementById('bootstrap-csrf') || {}).value
           || sessionStorage.getItem('sfx:csrf');
  const r = await fetch('/api/v1/items', {
    method: 'POST',
    headers: {'Content-Type': 'application/json', 'x-csrf-token': tok},
    body: JSON.stringify(args.body),
  });
  const text = await r.text();
  if (!r.ok) throw new Error('POST /api/v1/items -> ' + r.status + ' ' + text);
  return JSON.parse(text);
}"""

# Die **Kernpixel**: die gefuellte Scheibe und der Membranring eines Knotens tragen die
# Space-Farbe in voller Deckung (Muster aus `p105_b8_karte_probe.py`).
KERNE = r"""() => {
  const RAUM = [[74, 147, 240], [46, 184, 166], [139, 147, 161]];
  const c = document.getElementById('overview-graph-canvas');
  const r = c.getBoundingClientRect();
  const sx = r.width / c.width, sy = r.height / c.height;
  const d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data;
  const nah = (p, w, t) => Math.abs(p[0] - w[0]) <= t && Math.abs(p[1] - w[1]) <= t
                         && Math.abs(p[2] - w[2]) <= t;
  const raum = [];
  for (let y = 0; y < c.height; y += 1) {
    for (let x = 0; x < c.width; x += 1) {
      const i = (y * c.width + x) * 4;
      if (d[i + 3] < 250) continue;
      const p = [d[i], d[i + 1], d[i + 2]];
      for (const w of RAUM) if (nah(p, w, 4)) { raum.push([x, y]); break; }
    }
  }
  const g = [];
  for (const [x, y] of raum) {
    let treffer = null;
    for (const c2 of g) {
      if (Math.abs(c2.x / c2.n - x) < 14 && Math.abs(c2.y / c2.n - y) < 14) {
        treffer = c2; break;
      }
    }
    if (treffer) { treffer.x += x; treffer.y += y; treffer.n += 1; }
    else g.push({x: x, y: y, n: 1});
  }
  return g.filter(c2 => c2.n >= 4).map(c2 => ({
    x: (c2.x / c2.n) * sx, y: (c2.y / c2.n) * sy, px: c2.n}));
}"""

# Die Kamera-Transformation (zoom, pan) aus den **Kernpositionen** und den **Weltpositionen**:
# screen = zoom * welt + pan. Fuer jeden (Kern, Weltpunkt) ist der passende pan implizit
# gegeben; der **Modus** der Pan-Werte ist der gesuchte (die echten Paarungen liefern denselben
# Pan, die falschen je einen anderen). Der Zoom kommt aus der Anzeige, wird aber nachgesucht,
# weil die Anzeige auf ganze Prozent rundet.
PAN = r"""(args) => {
  const kerne = args.kerne, welt = args.welt, z0 = args.zoom;
  if (!kerne.length || !welt.length) return null;
  const bucket = (px, py) => Math.round(px * 2) + ',' + Math.round(py * 2);
  const zaehle = (z) => {
    const eimer = new Map();
    for (const [sx, sy] of kerne) {
      for (const [wx, wy] of welt) {
        const px = sx - z * wx, py = sy - z * wy;
        const k = bucket(px, py);
        const a = eimer.get(k);
        if (a) a.n += 1; else eimer.set(k, {n: 1});
      }
    }
    let top = 0;
    for (const a of eimer.values()) if (a.n > top) top = a.n;
    return top;
  };
  let bestZ = z0, bestN = -1;
  for (let d = -0.06; d <= 0.0601; d += 0.002) {
    const z = z0 * (1 + d);
    if (z <= 0.05) continue;
    const n = zaehle(z);
    if (n > bestN) { bestN = n; bestZ = z; }
  }
  for (let d = -0.003; d <= 0.0031; d += 0.0002) {
    const z = bestZ * (1 + d);
    if (z <= 0.05) continue;
    const n = zaehle(z);
    if (n > bestN) { bestN = n; bestZ = z; }
  }
  // der Pan: der **Median** der Kandidaten im Gewinner-Eimer (der Mittelwert litte unter den
  // falschen Paarungen, die denselben Eimer treffen)
  const eimer = new Map();
  for (const [sx, sy] of kerne) {
    for (const [wx, wy] of welt) {
      const px = sx - bestZ * wx, py = sy - bestZ * wy;
      const k = bucket(px, py);
      const a = eimer.get(k);
      if (a) a.push([px, py]); else eimer.set(k, [[px, py]]);
    }
  }
  let top = [];
  for (const a of eimer.values()) if (a.length > top.length) top = a;
  const med = (idx) => {
    const v = top.map(p => p[idx]).sort((a, b) => a - b);
    return v[Math.floor(v.length / 2)];
  };
  // die **Unsicherheit** der Bestimmung: die Spannweite der Kandidaten im Gewinner-Eimer
  // (der Pan ist der Median — die Kandidaten streuen) und die Zoom-Aufloesung des Netzes
  const streu = (idx) => {
    const v = top.map(p => p[idx]);
    return Math.max(...v) - Math.min(...v);
  };
  return {zoom: bestZ, panX: med(0), panY: med(1), treffer: top.length,
          pan_streuung: Math.max(streu(0), streu(1)), zoom_schritt: bestZ * 0.0002};
}"""

# Der **Recorder** der gezeichneten Beschriftungen (Schritt 14.35).
#
# **Kein Haken im Produktcode** (Plan §4): die Probe haengt sich an die **Leinwand-API** des
# Browsers. `clearRect` beginnt jeden Zeichendurchgang (`graph.js :: draw()` loescht am Anfang
# die Leinwand), `fillText` schreibt die Beschriftung. Was zwischen dem letzten `clearRect` und
# dem Ende des Durchgangs geschrieben wurde, ist die **gezeichnete Menge des letzten Bildes**.
#
# **Warum nicht die Pixel?** (der Stand vor 14.35): die Pixel-Schnueffelei konnte nicht
# unterscheiden, ob eine Beschriftung gezeichnet wurde oder nicht — zwei ueberlappende
# Rechtecke teilen sich ihre Pixel, und ein *weggelassenes* Rechteck sah wie ein gezeichnetes
# aus. Genau das waere nach der neuen Regel falsch: die Regel **laesst** Ueberlappendes weg.
# Der Pixelbeweis bleibt fuer die **Fokus-Beschriftung** (sie muss wirklich auf der Leinwand
# stehen) — dort kann nichts anderes ihre Pixel haben.
LABEL_RECORDER = r"""
(() => {
  const proto = CanvasRenderingContext2D.prototype;
  const origClear = proto.clearRect;
  const origFill = proto.fillText;
  window.__labels = {calls: [], frames: 0};
  proto.clearRect = function (x, y, w, h) {
    if (this.canvas && this.canvas.id === 'overview-graph-canvas') {
      window.__labels.calls = [];
      window.__labels.frames += 1;
    }
    return origClear.call(this, x, y, w, h);
  };
  proto.fillText = function (text, x, y) {
    if (this.canvas && this.canvas.id === 'overview-graph-canvas') {
      window.__labels.calls.push({text: String(text), x: x, y: y, alpha: this.globalAlpha});
    }
    return origFill.call(this, text, x, y);
  };
})();
"""

# Die **gezeichneten** Beschriftungen des letzten Bildes.
GEZEICHNETE_LABELS = "() => (window.__labels ? window.__labels.calls : [])"

# Die **Beschriftungs-Rechtecke**: Breite aus `ctx.measureText` (die Schrift des Graphen:
# 12px "IBM Plex Sans Var"), Hoehe = die Schrift (12 px). Die Koordinaten kommen aus dem
# Recorder — sie sind **CSS-Pixel** (die App zeichnet die Beschriftungen nach `restore()`, also
# ohne Zoom). Zusaetzlich wird an den **Pixeln** geprueft, ob die Beschriftung wirklich
# gemalt wurde (der Beweis fuer die Fokus-Beschriftung).
BESCHRIFTUNGEN = r"""(args) => {
  const LABEL = [196, 205, 216];
  const c = document.getElementById('overview-graph-canvas');
  const ctx = c.getContext('2d');
  const r = c.getBoundingClientRect();
  const sx = c.width / r.width, sy = c.height / r.height;
  const d = ctx.getImageData(0, 0, c.width, c.height).data;
  ctx.font = '12px "IBM Plex Sans Var", system-ui, sans-serif';
  ctx.textBaseline = 'middle';
  const nah = (p, w, t) => Math.abs(p[0] - w[0]) <= t && Math.abs(p[1] - w[1]) <= t
                         && Math.abs(p[2] - w[2]) <= t;
  const out = [];
  for (const k of args.aufrufe) {
    const w = ctx.measureText(k.text).width;
    const x0 = k.x, y0 = k.y - 6;
    const px0 = Math.round(x0 * sx), px1 = Math.round((x0 + w) * sx);
    const py0 = Math.round(y0 * sy), py1 = Math.round((y0 + 12) * sy);
    const imBild = px0 >= 0 && py0 >= 0 && px1 <= c.width && py1 <= c.height;
    let treffer = 0;
    if (imBild) {
      for (let y = py0; y < py1; y++) {
        for (let x = px0; x < px1; x++) {
          const i = (y * c.width + x) * 4;
          if (d[i + 3] < 250) continue;
          if (nah([d[i], d[i + 1], d[i + 2]], LABEL, 10)) treffer += 1;
        }
      }
    }
    out.push({text: k.text, breite: w, x0: x0, y0: y0, x1: x0 + w, y1: y0 + 12,
              pixel: treffer, hat_pixel: treffer > 0, imBild: imBild});
  }
  return out;
}"""

# Die Karte ist **gemalt** (irgendetwas steht im Canvas) — die Vorbedingung der
# Ruhe-Messung.
GEPAINTET = """() => {
  const c = document.getElementById('overview-graph-canvas');
  if (!c) return false;
  const d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data;
  for (let i = 3; i < d.length; i += 400) if (d[i] !== 0) return true;
  return false;
}"""

# Die Zahl der **Kernpixel**: die Knotenkerne tragen die Space-Farbe in voller Deckung. Damit
# laesst sich belegen, dass die Karte **wirklich gemalt** wurde — ohne diesen Beleg waere die
# reduced-motion-Zelle (0 Frames) eine leere Aussage.
KERNPIXEL = """() => {
  const RAUM = [[74, 147, 240], [46, 184, 166], [139, 147, 161]];
  const c = document.getElementById('overview-graph-canvas');
  if (!c) return 0;
  const d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data;
  const nah = (p, w) => Math.abs(p[0] - w[0]) <= 6 && Math.abs(p[1] - w[1]) <= 6
                      && Math.abs(p[2] - w[2]) <= 6;
  let n = 0;
  for (let i = 0; i < d.length; i += 4) {
    if (d[i + 3] < 250) continue;
    const p = [d[i], d[i + 1], d[i + 2]];
    for (const w of RAUM) if (nah(p, w)) { n += 1; break; }
  }
  return n;
}"""

# Der Canvas-Hash: die Karte ist zur Ruhe gekommen, wenn er sich zweimal hintereinander nicht
# mehr aendert (Muster aus `p105_b8_karte_probe.py`).
CANVAS_HASH = r"""() => {
  const c = document.getElementById('overview-graph-canvas');
  if (!c) return null;
  const d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data;
  let h = 0x811c9dc5, painted = 0;
  for (let i = 0; i < d.length; i += 64) {
    h ^= d[i] + d[i + 1] + d[i + 2] + d[i + 3];
    h = (h * 16777619) >>> 0;
    if (d[i + 3] !== 0) painted += 1;
  }
  return {hash: h, painted: painted, now: performance.now()};
}"""

# Zaehlt die Animationsframes, die **aus graph.js** kommen (der Stack entscheidet -- Playwrights
# eigenes Polling zaehlt nicht mit; derselbe Filter wie in `p105_b8_karte_probe.py`).
RAF_PROBE = """
(() => {
  const log = {count: 0, other: 0, stamps: []};
  window.__rafLog = log;
  const orig = window.requestAnimationFrame.bind(window);
  window.requestAnimationFrame = function (cb) {
    const fromGraph = String(new Error().stack || '').includes('graph.js');
    return orig(function (t) {
      if (fromGraph) { log.count += 1; log.stamps.push(performance.now()); }
      else { log.other += 1; }
      return cb(t);
    });
  };
})();
"""


def login(page):
    totp_zuruecksetzen()
    page.goto(BASE + "/ui/login", wait_until="domcontentloaded")
    page.fill('input[name="space"]', SPACE)
    page.fill('input[name="password"]', AUFTRAG["password"])
    page.fill('input[name="totp"]', totp_now(AUFTRAG["secret"]))
    page.click('form[action="/ui/login"] button[type="submit"]')
    page.wait_for_selector("#shell", timeout=30000)
    page.wait_for_selector(".overview__graph canvas", state="visible", timeout=20000)


def settle(page, budget_ms=60000):
    """Warten, bis die Simulation **keine Frames mehr anfordert**.

    Der Canvas-Hash taugt dafuer **nicht** (Muster aus `p105_b8_karte_probe.py`, dort harmlos):
    in den ersten Frames wird die Karte zweimal **unveraendert** gezeichnet — der Seed steht,
    die Simulation hat noch nicht gerechnet — der Hash bleibt also stabil, und die Probe
    erkannte die Karte als „zur Ruhe gekommen", **bevor** ueberhaupt simuliert wurde. Gemessen
    wurde das an der Welt: der Umriss war um die Haelfte zu klein (der Seed-Ring statt des
    Gleichgewichts), und die Zellen sprangen von Lauf zu Lauf.

    Das richtige Signal ist der `requestAnimationFrame` **aus graph.js**: er kommt in jedem
    Simulations-Tick und hoert auf, wenn `alpha` unter `ALPHA_MIN` ist. „0 Frames" ist der
    Sonderfall des reduced-motion-Pfads (dort rechnet die Simulation synchron)."""
    page.wait_for_function(GEPAINTET, timeout=30000)
    last = -1
    still = 0
    elapsed = 0
    while elapsed <= budget_ms:
        n = page.evaluate("() => window.__rafLog.count")
        if n == last:
            still += 1
            # vier Zehntel ohne neuen Frame = die Simulation ist durch
            if still >= 4 and (n > 0 or elapsed > 4000):
                return
        else:
            still = 0
        last = n
        page.wait_for_timeout(100)
        elapsed += 100
    raise RuntimeError("die Simulation kam nicht zur Ruhe")


def frischer_lauf(page, leer=True):
    """Ein kompletter Durchlauf: (leeren) Speicher loeschen, neu laden, warten, ablesen.

    **Die Falle, die hier aufgedeckt wird (2026-10-26, Schritt 14.2):** `localStorage.clear()`
    loescht die Ablage — aber die **App** speichert sie **periodisch** (der Ereignis-Feed
    pollt im Sekundentakt, jeder Graph-Neulauf speichert am Ende, gedrosselt um 1 s). Zwischen
    dem Loeschen und dem `reload()` kann ein **wartendes** Speichern zuschlagen: die Ablage ist
    dann wieder da, der neue Lauf laedt sie — und **pinnt** alle Knoten (`seedInitialPositions()`
    haelt gemerkte Positionen fest). Ein solcher Lauf **misst nichts**: die Knoten stehen
    genau da, wo sie standen, und jede Verschiebung faellt zwangslaufig aus.

    Deshalb wird der Ablage-Zustand **unmittelbar nach dem Neuladen** gelesen — **bevor** die
    Simulation rechnet. `pinned_beim_start` > 0 heisst: der Lauf war **gepinnt**, die Messung
    taugt nichts. Der Aufrufer muss das pruefen (und der Wächter muss es pruefen)."""
    if leer:
        page.evaluate("() => { localStorage.clear(); }")
    page.reload(wait_until="domcontentloaded")
    page.wait_for_selector(".overview__graph canvas", state="visible", timeout=20000)
    ablage_beim_start = page.evaluate(ABLAGE)
    settle(page)
    # das Speichern ist gedrosselt (1 s) — erst danach steht die Ablage bereit
    page.wait_for_timeout(1600)
    ergebnis = lesen(page)
    ergebnis["pinned_beim_start"] = len(ablage_beim_start["pos"]) if ablage_beim_start else 0
    ergebnis["knoten_beim_start"] = len(ablage_beim_start["pos"]) if ablage_beim_start else 0
    return ergebnis


def lesen(page):
    """Alles, was eine Messung braucht, in einem Rutsch."""
    ablage = page.evaluate(ABLAGE)
    if not ablage or not ablage["pos"]:
        raise RuntimeError("keine Ablage im localStorage (das Layout wurde nicht gemerkt)")
    return {
        "ablage": ablage,
        "zoom": page.evaluate(ZOOM),
        "kasten": page.evaluate(KASTEN),
        "grafik": page.evaluate(GRAFIK),
        "kerne": page.evaluate(KERNE),
        "kernpixel": page.evaluate(KERNPIXEL),
        "raf": page.evaluate("() => window.__rafLog"),
    }


def ruhe_ms(stamps):
    """Die Zeit **bis zur Ruhe**: vom ersten bis zum letzten Frame der Simulation.

    Gemessen wird die **gesamte Spanne** des Ladevorgangs (`stamps[-1] - stamps[0]`) — der
    conservative Wert: ein Frame-Stillstand mitten in der Simulation (GC, Last) kann ihn
    **nicht kuerzen** (die fruehere Burst-Schnitt-Messung tat genau das: sie trennte bei
    *jedem* Abstand > 300 ms und mass danach nur den Rest — eine Lastspitze haette die
    Budget-Zelle falsch gruen gemacht). Die Luecken zwischen den Frames werden **mit
    berichtet** (`luecken`), damit man sieht, ob es ueberhaupt mehrere Phasen gab.

    Die Simulation bricht ab, wenn `alpha < ALPHA_MIN`; der letzte `requestAnimationFrame`
    **aus graph.js** ist der, der den letzten Tick anstoesst — die Ruhe ist also eine Frame
    nach ihm. Der gemessene Wert ist damit um **bis zu eine Frame (~16 ms) zu klein**."""
    if not stamps or len(stamps) < 2:
        return None, []
    s = sorted(stamps)
    luecken = [round(s[i] - s[i - 1]) for i in range(1, len(s)) if s[i] - s[i - 1] > 100]
    # auf ganze Millisekunden gerundet: die Frame-Stempel tragen Sub-Millisekunden-Rauschen
    # (0,2 ms zwischen zwei Laeufen) — der Beleg soll **byteweise** vergleichbar sein
    return round(s[-1] - s[0]), luecken


def _pruefsumme(pos):
    """Eine **Pruefsumme** der Positionen: derselbe Datensatz muss dieselbe Summe ergeben.
    Damit unterscheidet der Beleg „die Karte ist anders gemalt" von „die Karte liegt
    anders" — ohne dass der ganze Positionssatz in die Datei muesste."""
    h = 2166136261
    for nid in sorted(pos):
        for wert in ("%.3f" % pos[nid][0], "%.3f" % pos[nid][1]):
            for zeichen in wert:
                h ^= ord(zeichen)
                h = (h * 16777619) & 0xFFFFFFFF
    return h


def schwerpunkte(pos, raum_von):
    """Je Space der Schwerpunkt (arithmetisches Mittel) der Knoten."""
    summe = {}
    for nid, xy in pos.items():
        sp = raum_von.get(nid)
        if sp is None:
            continue
        s = summe.setdefault(sp, [0.0, 0.0, 0])
        s[0] += xy[0]
        s[1] += xy[1]
        s[2] += 1
    return {sp: [v[0] / v[2], v[1] / v[2]] for sp, v in summe.items()}


def naechster_schwerpunkt(xy, zentren):
    """Der Space, dessen Schwerpunkt dem Punkt am naechsten liegt."""
    best = None
    for sp, z in zentren.items():
        d = ((xy[0] - z[0]) ** 2 + (xy[1] - z[1]) ** 2) ** 0.5
        if best is None or d < best[1]:
            best = (sp, d)
    return best


def _pan(page, kerne, pos, zoom):
    """Die Kamera-Transformation (zoom, pan) aus den Kernpositionen und den Weltpositionen.

    `screen = zoom * welt + pan` — fuer jeden (Kern, Weltpunkt) ist der passende Pan implizit
    gegeben; der **Modus** der Pan-Werte ist der gesuchte. Das ist dieselbe Rechnung, die
    die Beschriftungs-Zelle macht (sie braucht die absoluten Bildrechtecke).

    **Der verfeinerte Zoom** (`bestZ`) ist die Quelle fuer *alle* Rechnungen: die Anzeige
    rundet auf ganze Prozent (`(zoom*100).toFixed(0)`), der Fuellgrad und die Zentrierung
    duerfen aber nicht mit einem anderen Zoom rechnen als der Pan (sonst entstuende ein
    Versatz von Zehntelpixeln — ein Zehntel der 3-px-Schwelle)."""
    welt = [[xy[0], xy[1]] for xy in pos.values()]
    treffer = page.evaluate(PAN, {"kerne": [[k["x"], k["y"]] for k in kerne],
                                  "welt": welt, "zoom": zoom})
    if not treffer or treffer["treffer"] < 3:
        return None
    return treffer


def kamera_messung(page, lauf, pos):
    """Die **Kamera-Zelle** (P10.5-67): Fuellgrad, Passung, Zentrierung.

    Der Pan der Kamera kommt aus den **Kernpositionen** und den Weltpositionen (derselbe Weg,
    den die Beschriftungs-Zelle geht) -- er steht im Modul, nicht im DOM. Ohne ihn ist die
    Zentrierung nicht messbar.

    **Ein** Zoom fuer alle Rechnungen: der verfeinerte aus der Pan-Bestimmung (die Anzeige
    rundet auf ganze Prozent).

    **Die Zentrierung** (Plan §2.5: "Pan auf die Mitte"): der Umriss des Inhalts muss in der
    Leinwandmitte liegen. Vor `fitView()` saß er **32,3 px** neben der Mitte -- der Umriss des
    Inhalts liegt beim Anker des eigenen Space, nicht in der Mitte der Welt.

    Dieselbe Rechnung laeuft **zweimal**: einmal fuer die 152 Knoten der Abnahme-Zelle und
    einmal fuer die 201 Knoten der Budget-Zelle (E3: reicht `ZOOM_MIN` bei 200 Knoten?).
    """
    passend = _pan(page, lauf["kerne"], pos, lauf["zoom"])
    if not passend:
        return {"messbar": False, "grund": "die Kamera liess sich nicht bestimmen", "ok": False}
    zoom = passend["zoom"]
    pan_x, pan_y = passend["panX"], passend["panY"]
    kasten = lauf["kasten"]
    xs = [xy[0] for xy in pos.values()]
    ys = [xy[1] for xy in pos.values()]
    welt = {"x0": min(xs), "x1": max(xs), "y0": min(ys), "y1": max(ys)}
    bild_w = zoom * (welt["x1"] - welt["x0"])
    bild_h = zoom * (welt["y1"] - welt["y0"])
    fuellgrad = max(bild_w / kasten["width"], bild_h / kasten["height"])
    passt = (bild_w <= kasten["width"] * 1.02 and bild_h <= kasten["height"] * 1.02)
    mitte_x = kasten["width"] / 2
    mitte_y = kasten["height"] / 2
    umriss_mitte = [(welt["x0"] + welt["x1"]) / 2, (welt["y0"] + welt["y1"]) / 2]
    versatz = max(abs(umriss_mitte[0] * zoom + pan_x - mitte_x),
                  abs(umriss_mitte[1] * zoom + pan_y - mitte_y))
    zentriert = versatz <= 3.0
    # die **Unsicherheit** der Kamerabestimmung: die Streuung der Pan-Kandidaten
    # plus der Zoom-Rasterfehler (Zoom-Raster × Welt-Ausdehnung)
    unsicherheit = (passend["pan_streuung"]
                    + passend["zoom_schritt"] * max(welt["x1"] - welt["x0"],
                                                    welt["y1"] - welt["y0"]))
    return {
        "messbar": True,
        "zoom": zoom,
        "zoom_anzeige": lauf["zoom"],
        "leerwand": [kasten["width"], kasten["height"]],
        "welt": welt,
        "bild_mass": [bild_w, bild_h],
        "fuellgrad": fuellgrad,
        "passt": passt,
        "pan": [pan_x, pan_y],
        "umriss_mitte": umriss_mitte,
        "versatz_mitte_px": versatz,
        "unsicherheit_px": unsicherheit,
        "zentriert": zentriert,
        "ok": fuellgrad >= 0.60 and passt and zentriert,
    }


def nachbarn_je_knoten(grafik):
    """Die **eindeutigen** Nachbarn je Knoten — wie `graph.js :: recomputeDegrees()`: der
    Client fasst frontmatter- und body-Kante derselben Paarung zu einer zusammen."""
    nachbarn = {}
    for e in grafik["edges"]:
        nachbarn.setdefault(e["src"], set()).add(e["dst"])
        nachbarn.setdefault(e["dst"], set()).add(e["src"])
    return nachbarn


def _truncate(titel, n=28):
    """Die Beschriftung, wie der Client sie zeichnet (`graph.js :: truncate()`)."""
    if not titel:
        return ""
    return titel if len(titel) <= n else titel[: n - 1] + "…"


def beschriftungen(page, lauf, pos, raum_von, nachbarn):
    """P10.5-71 — die gezeichneten Beschriftungs-Rechtecke.

    Der Fokus-Knoten: der Knoten mit den meisten **Nachbarn**, der **im Bild** liegt (sonst
    kann der Browser ihn nicht ueberfahren). Die Nachbarn kommen aus `/api/v1/graph` — die App
    zeichnet im Fokus-Zustand den Fokus und den **ersten Ring** (`drawLabels()`).

    **Datierte Aenderung der Messung (2026-10-26, Schritt 14.35):** gemessen wird nicht mehr
    an den **Pixeln**, sondern an den **`fillText`-Aufrufen** des letzten Bildes (der Recorder
    haengt sich an `clearRect`/`fillText` der Leinwand — **kein** Haken im Produktcode). Grund:
    die neue Regel **laesst** ueberlappende Beschriftungen weg, und an den Pixeln ist ein
    *weggelassenes* Rechteck von einem *gezeichneten* nicht zu unterscheiden (zwei
    ueberlappende Rechtecke teilen sich ihre Pixel). Der Pixelbeweis bleibt fuer die
    **Fokus-Beschriftung** — sie muss wirklich auf der Leinwand stehen."""
    kerne = lauf["kerne"]
    zoom = lauf["zoom"]
    welt = [[xy[0], xy[1]] for xy in pos.values()]
    passend = page.evaluate(PAN, {"kerne": [[k["x"], k["y"]] for k in kerne],
                                   "welt": welt, "zoom": zoom})
    if not passend or passend["treffer"] < 3:
        return {"messbar": False, "grund": "die Kamera liess sich nicht bestimmen",
                "treffer": passend["treffer"] if passend else 0, "ok": False}
    kasten = lauf["kasten"]
    titel_von = {n["id"]: n["title"] for n in lauf["grafik"]["nodes"]}

    # die im Bild liegenden Knoten: der Kern, der dem Weltpunkt am naechsten liegt
    sichtbar = []
    for nid, xy in pos.items():
        wx = xy[0] * passend["zoom"] + passend["panX"]
        wy = xy[1] * passend["zoom"] + passend["panY"]
        best = None
        for k in kerne:
            d = ((k["x"] - wx) ** 2 + (k["y"] - wy) ** 2) ** 0.5
            if best is None or d < best[0]:
                best = (d, k)
        if best and best[0] <= 6.0:
            sichtbar.append(nid)
    kandidaten_fokus = [(nid, len(nachbarn.get(nid, ()))) for nid in sichtbar]
    kandidaten_fokus = [k for k in kandidaten_fokus if k[1] >= 5]
    if not kandidaten_fokus:
        return {"messbar": False, "grund": "kein sichtbarer Knoten mit >= 5 Nachbarn",
                "sichtbar": len(sichtbar), "ok": False}
    fokus_id = max(kandidaten_fokus, key=lambda k: k[1])[0]

    fx = pos[fokus_id][0] * passend["zoom"] + passend["panX"]
    fy = pos[fokus_id][1] * passend["zoom"] + passend["panY"]
    if not (0 <= fx <= kasten["width"] and 0 <= fy <= kasten["height"]):
        return {"messbar": False, "grund": "der Fokus-Knoten liegt nicht im Bild",
                "fokus": fokus_id, "sichtbar": len(sichtbar), "ok": False}

    # der Zeiger auf den Fokus — die App zeichnet jetzt Fokus + ersten Ring
    page.mouse.move(kasten["left"] + fx, kasten["top"] + fy)
    page.wait_for_timeout(600)

    # **die Kandidaten**: die Knoten, die eine Beschriftung bekommen *koennten* (Fokus +
    # erster Ring) — die Zahl geht in den Beleg, damit man sieht, wie viele weggelassen
    # wurden.
    ring = sorted(nachbarn.get(fokus_id, ()))
    kandidaten = []
    for nid in [fokus_id] + ring:
        xy = pos.get(nid)
        if xy is None:
            continue
        deg = len(nachbarn.get(nid, ()))
        r = min(12, 4 + 2 * math.log2(1 + deg))
        kandidaten.append({"id": nid, "titel": titel_von.get(nid, ""), "x": xy[0],
                           "y": xy[1], "r": r})
    # **die gezeichneten Beschriftungen**: der Recorder meldet die `fillText`-Aufrufe des
    # letzten Bildes.
    aufrufe = page.evaluate(GEZEICHNETE_LABELS)
    rects = page.evaluate(BESCHRIFTUNGEN, {"aufrufe": aufrufe})
    # **die Fokus-Beschriftung**: sie ist die erste gezeichnete (Vorrang) und muss auf der
    # Leinwand stehen — der Pixelbeweis.
    fokus_text = _truncate(titel_von.get(fokus_id, ""))
    fokus_rect = next((r for r in rects if r["text"] == fokus_text), None)
    fokus_beschriftung = bool(fokus_rect and fokus_rect["hat_pixel"])
    # die **Ueberlappungen**: zwei gezeichnete Rechtecke duerfen sich nicht schneiden
    ueber = []
    for i in range(len(rects)):
        for j in range(i + 1, len(rects)):
            a, b = rects[i], rects[j]
            if (b["x0"] < a["x1"] and a["x0"] < b["x1"]
                    and b["y0"] < a["y1"] and a["y0"] < b["y1"]):
                ueber.append([a["text"], b["text"]])
    # **Mindestzahl gezeichneter Beschriftungen**: sonst waere die Zelle gruen, wenn die App
    # nur noch die Fokus-Beschriftung zeichnet (kein Ueberlappungspaar — aber auch keine
    # Nachbarbeschriftung, die man pruefen koennte). **Zwei** gezeichnete sind das Minimum;
    # die *Haelfte* der Kandidaten war vor 14.35 die Bedingung — das **waere jetzt der
    # falsche Massstab**: die Regel laesst ueberlappende Beschriftungen bewusst weg, eine
    # Minderheit gezeichneter Beschriftungen ist ihr **Ergebnis**, kein Fehler.
    genug = len(rects) >= 2
    return {
        "messbar": True,
        "fokus": fokus_id,
        "fokus_titel": fokus_text,
        "nachbarn": len(ring),
        "kandidaten": len(kandidaten),
        "gezeichnet": len(rects),
        "unterdrueckt": len(kandidaten) - len(rects),
        "texte": [r["text"] for r in rects],
        "ueberlappungen": ueber,
        "fokus_beschriftung": fokus_beschriftung,
        "fokus_pixel": fokus_rect["pixel"] if fokus_rect else 0,
        "genug_gezeichnet": genug,
        "zoom": passend["zoom"],
        "pan": [passend["panX"], passend["panY"]],
        "unsicherheit_px": (passend["pan_streuung"]
                            + passend["zoom_schritt"] * max(
                                abs(max(xy[0] for xy in pos.values()) - min(xy[0] for xy in pos.values())),
                                abs(max(xy[1] for xy in pos.values()) - min(xy[1] for xy in pos.values())))),
        "treffer": passend["treffer"],
        "ok": len(ueber) == 0 and fokus_beschriftung and genug,
    }


def main():
    fehler = []
    messungen = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1920, "height": 1200},
                                  ignore_https_errors=True)
        page = ctx.new_page()
        page.add_init_script(RAF_PROBE)
        # **Der Recorder der gezeichneten Beschriftungen** (Schritt 14.35): er haengt sich an
        # die Leinwand-API des Browsers, nicht in den Produktcode (Plan §4).
        page.add_init_script(LABEL_RECORDER)
        page.on("pageerror", lambda e: fehler.append(str(e)))
        login(page)

        # ---- 1) Zwei frische Laeufe: Determinismus, Regionen, Kamera -----------------------
        lauf1 = frischer_lauf(page)
        lauf2 = frischer_lauf(page)
        pos1 = lauf1["ablage"]["pos"]
        pos2 = lauf2["ablage"]["pos"]
        raum_von = {n["id"]: n["space"] for n in lauf2["grafik"]["nodes"]}
        nachbarn = nachbarn_je_knoten(lauf2["grafik"])

        abw = 0.0
        for nid, xy in pos2.items():
            if nid in pos1:
                abw = max(abw, max(abs(xy[0] - pos1[nid][0]), abs(xy[1] - pos1[nid][1])))
        # **beide Laeufe muessen dieselbe Knotenmenge haben** — sonst waere eine Zelle
        # „gruen", die nur einen Knoten vergleicht (der Zaehler `gemeinsam` stand vorher
        # nur im Beleg, nicht in der Bedingung).
        gemeinsam = len([n for n in pos2 if n in pos1])
        messungen["determinismus"] = {
            "knoten": len(pos2),
            "knoten_lauf1": len(pos1),
            "gemeinsam": gemeinsam,
            "max_abweichung_px": abw,
            "ok": bool(abw <= 1.0 and gemeinsam == len(pos1) == len(pos2) and len(pos2) > 0),
        }

        zentren = schwerpunkte(pos2, raum_von)
        richtig = 0
        falsch_beispiele = []
        # **Die Marge (Schritt 14.4):** je Knoten der Abstand zum **naechsten fremden**
        # Schwerpunkt minus dem Abstand zum **eigenen** Schwerpunkt. Positiv = der Knoten
        # liegt in seiner Region, und die Zahl sagt, **wie viel** Spielraum die Trennung
        # hat (ein Wert nahe 0 waere eine Zelle, die beim naechsten Item kippt). Ohne diese
        # Zahl waere die Konstanten-Wahl eine Augenentscheidung.
        margen = []
        abstaende_eigen = []
        abstaende_fremd = []
        for nid, xy in pos2.items():
            eigen = raum_von.get(nid)
            if eigen is None:
                continue
            best = naechster_schwerpunkt(xy, zentren)
            if best[0] == eigen:
                richtig += 1
            elif len(falsch_beispiele) < 5:
                falsch_beispiele.append({"id": nid, "space": eigen, "naechster": best[0]})
            d_eigen = ((xy[0] - zentren[eigen][0]) ** 2 + (xy[1] - zentren[eigen][1]) ** 2) ** 0.5
            d_fremd = None
            for sp, z in zentren.items():
                if sp == eigen:
                    continue
                d = ((xy[0] - z[0]) ** 2 + (xy[1] - z[1]) ** 2) ** 0.5
                if d_fremd is None or d < d_fremd:
                    d_fremd = d
            if d_fremd is None:
                continue
            abstaende_eigen.append(d_eigen)
            abstaende_fremd.append(d_fremd)
            margen.append(d_fremd - d_eigen)
        anzahl = sum(1 for nid in pos2 if raum_von.get(nid) is not None)
        anteil = richtig / anzahl if anzahl else 0.0
        margen.sort()
        # **Die Dichte** (Schritt 14.4): der kleinste Abstand zwischen zwei Knoten und die
        # Zahl der Paare, deren **Kreise sich ueberlappen** (der Radius folgt dem Produktcode:
        # `NODE_RADIUS_BASE + NODE_RADIUS_PER_LOG * log2(1 + Grad)`, gedeckelt). Das sind die
        # Zahlen, mit denen der **Seed** geprueft wurde (Plan §2.3: "dicht, ohne Ueberlappung"):
        # ohne sie waere `ITEM_STEP` (14 px) eine Setzung, keine Messung.
        grad = {nid: len(nb) for nid, nb in nachbarn.items()}
        ids = list(pos2.keys())
        engster = None
        ueberlappungen = 0
        for i in range(len(ids)):
            a = pos2[ids[i]]
            ra = min(4 + 2 * math.log2(1 + grad.get(ids[i], 0)), 12)
            for j in range(i + 1, len(ids)):
                b = pos2[ids[j]]
                d = ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5
                if engster is None or d < engster:
                    engster = d
                rb = min(4 + 2 * math.log2(1 + grad.get(ids[j], 0)), 12)
                if d < ra + rb:
                    ueberlappungen += 1
        messungen["regionen"] = {
            "knoten": anzahl,
            "richtig": richtig,
            "anteil": anteil,
            "schwerpunkte": zentren,
            "beispiele_falsch": falsch_beispiele,
            # **Die Marge** (Schritt 14.4): die Trennung der Regionen hat einen **Spielraum**.
            "marge_min_px": margen[0] if margen else None,
            "marge_median_px": margen[len(margen) // 2] if margen else None,
            "abstand_eigen_median_px": (sorted(abstaende_eigen)[len(abstaende_eigen) // 2]
                                        if abstaende_eigen else None),
            "abstand_fremd_min_px": min(abstaende_fremd) if abstaende_fremd else None,
            # **Die Dichte** (Schritt 14.4): die Zahlen des Seeds.
            "engster_abstand_px": engster,
            "ueberlappende_paare": ueberlappungen,
            "ok": anteil >= 0.95,
        }


        messungen["kamera"] = kamera_messung(page, lauf2, pos2)

        # ---- 2) Die Beschriftungen (P10.5-71) ----------------------------------------------
        messungen["beschriftungen"] = beschriftungen(page, lauf2, pos2, raum_von, nachbarn)

        # ---- 3) Stabilitaet (P10.5-68) -----------------------------------------------------
        neues = page.evaluate(NEUES_ITEM, {"body": {
            "type": "note", "status": "active", "title": "Probe Stabilitaet",
            "space": WACHSER_SPACE, "folder": "ordner-1"}})
        # **Der Feed einpendeln lassen**: der Aenderungsfeed pollt im Sekundentakt, das Ereignis
        # kommt also bis zu ~1 s nach dem Anlegen — und die App legt dann **neu** (und merkt
        # die Karte). Ohne diese Pause liest der folgende Lauf je nach Zeitpunkt eine andere
        # Ablage: der Wert der Zelle waere laufverschieden (gemessen: 287 px gegen 227 px bei
        # identischem Code). Nach der Pause steht die App **ruhig**.
        page.wait_for_timeout(2500)
        # (a) die **gemerkte** Karte: neu laden, die Ablage kennt das neue Item noch nicht
        gemerkt = frischer_lauf(page, leer=False)
        pos_g = gemerkt["ablage"]["pos"]
        zentren_g = schwerpunkte(pos_g, raum_von)
        xy_neu = pos_g.get(neues["id"])
        nah = naechster_schwerpunkt(xy_neu, zentren_g) if xy_neu else None
        in_region = bool(nah and nah[0] == WACHSER_SPACE)
        # die **Abstaende**: das neue Item liegt entweder mitten in der Region seines Space
        # (dann ist es der naechste Nachbar des eigenen Space) oder auf dem globalen Ring
        # (dann ist es ein Ausreisser). Die Abstaende machen den Unterschied **messbar**,
        # nicht nur den Zufallsklick „naechster Schwerpunkt".
        abstand_eigen = None
        abstand_fremd = None
        if xy_neu:
            for nid, xy in pos_g.items():
                if nid == neues["id"]:
                    continue
                d = ((xy[0] - xy_neu[0]) ** 2 + (xy[1] - xy_neu[1]) ** 2) ** 0.5
                if raum_von.get(nid) == WACHSER_SPACE:
                    abstand_eigen = d if abstand_eigen is None else min(abstand_eigen, d)
                else:
                    abstand_fremd = d if abstand_fremd is None else min(abstand_fremd, d)
        # (b) der **frische** Lauf: die Knoten der anderen Spaces duerfen sich nicht bewegen
        frisch = frischer_lauf(page, leer=True)
        pos_f = frisch["ablage"]["pos"]
        # **Der frische Lauf muss wirklich frisch sein** (2026-10-26, Schritt 14.2): stand die
        # Ablage schon **vor** der Simulation da, war der Lauf **gepinnt** — die Knoten standen
        # fest, und die Zelle waere zwangslaufig gruen (ein Fehlgruen ohne Aussage).
        if frisch["pinned_beim_start"]:
            messungen["stabilitaet"] = {
                "messbar": False,
                "grund": "der frische Lauf war gepinnt (die Ablage war schon da)",
                "pinned_beim_start": frisch["pinned_beim_start"],
                "ok": False,
            }
            raise SystemExit("der frische Lauf war gepinnt — die Stabilitaets-Zelle misst nichts")
        andere = [nid for nid in pos2 if raum_von.get(nid) and raum_von[nid] != WACHSER_SPACE]
        schritte = []
        for nid in andere:
            if nid in pos_f:
                a, b = pos2[nid], pos_f[nid]
                schritte.append((((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5))
        schritte.sort()
        median = schritte[len(schritte) // 2] if schritte else None
        messungen["stabilitaet"] = {
            "wachser_space": WACHSER_SPACE,
            "neues_item": neues["id"],
            "position_neu": xy_neu,
            "naechster_schwerpunkt": nah[0] if nah else None,
            "in_eigener_region": in_region,
            "abstand_eigener_space_px": abstand_eigen,
            "abstand_fremder_space_px": abstand_fremd,
            "andere_spaces": len(andere),
            "median_verschiebung_px": median,
            "max_verschiebung_px": schritte[-1] if schritte else None,
            # **Die Pruefsummen** der beiden Laeufe: sie tragen den Beleg, dass die Karten
            # wirklich **verschieden** sind (der Vergleich zweier Laeufe braucht zwei
            # verschiedene Karten — sonst vergleicht die Zelle eine Karte mit sich).
            "pruefsumme_vorher": _pruefsumme(pos2),
            "pruefsumme_nachher": _pruefsumme(pos_f),
            "pinned_beim_start": frisch["pinned_beim_start"],
            "knoten_frisch": len(frisch["grafik"]["nodes"]),
            "kasten_frisch": frisch["kasten"],
            "position_neu_frisch": pos_f.get(neues["id"]),
            "ok": bool(median is not None and median <= 2.0 and in_region
                       and _pruefsumme(pos2) != _pruefsumme(pos_f)),
        }
        # **Die Positionen der beiden Laeufe** (zum Vergleich mit dem Node-Harness; die Datei
        # landet **nicht** im Repo — sie ist ein Arbeitsmittel, kein Beleg).
        _dump = Path("/tmp/opencode") / ("p105_b14_stab_%d.json" % AUFTRAG["pid"])
        try:
            _dump.write_text(json.dumps({"vorher": pos2, "nachher": pos_f,
                                         "reihenfolge": [n["id"] for n in frisch["grafik"]["nodes"]],
                                         "reihenfolge_vorher": [n["id"] for n in lauf2["grafik"]["nodes"]]},
                                        ensure_ascii=False), encoding="utf-8")
        except OSError:
            pass

        # ---- 4) Budget (P10.5-69): 200 Knoten, Zeit bis Ruhe, reduced motion ---------------
        for i in range(EXTRA_ITEMS):
            sp = SPACES[i % len(SPACES)]
            page.evaluate(NEUES_ITEM, {"body": {
                "type": "note", "status": "active", "title": "Probe Budget %02d" % (i + 1),
                "space": sp, "folder": "ordner-2"}})
        # **wieder einpendeln lassen** (derselbe Grund wie oben: das Ereignis kommt bis zu
        # ~1 s spaeter, die App legt dann neu und merkt die Karte — sonst liest der frische
        # Lauf je nach Zeitpunkt eine andere Ablage)
        page.wait_for_timeout(2500)
        gross = frischer_lauf(page, leer=True)
        pos_gross = gross["ablage"]["pos"]
        ms, luecken = ruhe_ms(gross["raf"]["stamps"])
        ctx2 = browser.new_context(viewport={"width": 1920, "height": 1200},
                                   ignore_https_errors=True, reduced_motion="reduce")
        page2 = ctx2.new_page()
        page2.add_init_script(RAF_PROBE)
        login(page2)
        page2.wait_for_timeout(3000)
        raf2 = page2.evaluate("() => window.__rafLog")
        kern2 = page2.evaluate(KERNPIXEL)
        ctx2.close()
        messungen["budget"] = {
            "knoten": len(pos_gross),
            "pos_pruefsumme": _pruefsumme(pos_gross),
            "graph_reihenfolge": [n["id"] for n in gross["grafik"]["nodes"][:8]],
            "graph_knoten": len(gross["grafik"]["nodes"]),
            "ruhe_ms": ms,
            "luecken_ms": luecken,
            "raf_calls": gross["raf"]["count"],
            "raf_calls_reduced_motion": raf2["count"],
            "kern_pixel_reduced_motion": kern2,
            "kern_pixel": gross["kernpixel"],
            "grenze_ms": 3000,
            # **E3 (Plan §2.5):** reicht `ZOOM_MIN` (0,5) bei **200 Knoten**? Die Kamera wird
            # auch hier eingepasst -- die Messung steht als **eigene** Kamera-Zelle in der
            # Budget-Zelle, nicht in der Abnahme-Zelle (dort sind es 152 Knoten).
            #
            # **Der Zoom ist die Anzeige** (auf ganze Prozent gerundet). Wuerde der Zoom auf
            # `ZOOM_MIN` **abgeklemmt**, stuende er genau auf 50 % **und** der Inhalt passte
            # **nicht** in die Leinwand (`passt` false) -- beides steht hier.
            "kamera_200_knoten": kamera_messung(page, gross, pos_gross),
            "ok": bool(ms is not None and ms <= 3000 and len(pos_gross) >= 200
                       and raf2["count"] == 0 and kern2 > 0 and gross["kernpixel"] > 0),
        }

        ctx.close()
        browser.close()

    bericht = {
        "probe": "p105_b14_layout_probe",
        "schritt": AUFTRAG.get("schritt", "14.4"),
        "gegenlauf": AUFTRAG.get("gegenlauf"),
        # **Die Randbedingung der Messung (Schritt 14.4):** welche Startwerte hat der Server
        # ausgeliefert? Ohne diese Zeile waere der Beleg eine Behauptung ohne Randbedingung.
        "konstanten_varianten": AUFTRAG.get("konstanten_varianten") or {},
        "konstanten_gesendet": AUFTRAG.get("konstanten_gesendet") or {},
        "zeit": datetime.now(timezone.utc).isoformat(),
        "seed": AUFTRAG["seed"],
        "messungen": messungen,
        # **ein** Seitenfehler im Graph-Code wuerde die Zellen stumm verfaelchen — er
        # muss die Gesamtaussage rot machen, nicht nur im Beleg stehen.
        "alle_kriterien_erfuellt": bool(all(m.get("ok") for m in messungen.values())
                                        and not fehler),
        "seitenfehler": fehler,
    }
    RESULT.write_text(json.dumps(bericht, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(bericht, ensure_ascii=False, indent=2))
    rot = [k for k, v in messungen.items() if not v.get("ok")]
    if rot:
        print(f"ROT: {rot}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''


def main() -> int:
    global PORT, BASE, RESULT
    if GEGENLAUF is not None:
        RESULT = Path(__file__).resolve().with_name(
            "p105_b14_layout_probe_gegenlauf_%s.json" % GEGENLAUF)
    elif KONSTANTEN:
        # **Die Messvariante schreibt in ihre eigene Datei** — der Normalfall-Beleg (die
        # Abnahme) darf nie von einer Messvariante ueberschrieben werden.
        RESULT = Path(__file__).resolve().with_name(
            "p105_b14_layout_probe_konstante_%s.json" % LABEL)
    PORT = _freier_port()
    BASE = f"https://127.0.0.1:{PORT}"
    creds = _setup()
    _seed()
    try:
        _serve()
        # **Die gesendeten Werte** der Block-14-Konstanten: der Beleg muss sagen, **womit**
        # gemessen wurde (sonst ist die Datei eine Behauptung ohne Randbedingung).
        text = _graph_text()
        for alt, neu in (GEGENLAEUFE[GEGENLAUF].items() if GEGENLAUF is not None
                         else _konstanten_patch().items()):
            text = text.replace(alt, neu)
        auftrag = {
            "base": BASE,
            "space": SPACE,
            "password": creds["password"],
            "secret": creds["secret"],
            "repo_root": str(REPO_ROOT),
            "auth_db": str(AUTH_DB),
            "result": str(RESULT),
            "wachser_space": WACHSER_SPACE,
            "extra_items": EXTRA_ITEMS,
            "pid": PID,
            "gegenlauf": GEGENLAUF,
            # **Die Messvariante (14.4):** die variierten Startwerte und die Werte, die
            # **tatsaechlich** serviert wurden.
            "konstanten_varianten": KONSTANTEN,
            "konstanten_gesendet": _konstanten_werte(text),
            "schritt": "14.4",
            "spaces": SPACES,
            "seed": {"spaces": len(SPACES), "items": sum(ITEMS_PRO_SPACE.values()),
                     "items_pro_space": ITEMS_PRO_SPACE, "wachser_space": WACHSER_SPACE},
        }
        AUFTRAG_DATEI.write_text(json.dumps(auftrag), encoding="utf-8")
        skript = WEGWERF_ROOT / ("browser_%d.py" % PID)
        skript.write_text(BROWSER_SKILL, encoding="utf-8")
        e2e = Path.home() / ".claude-code-tools/e2e-venv/bin/python"
        proc = subprocess.run(
            [str(e2e), str(skript), str(AUFTRAG_DATEI)],
            cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=900,
        )
        print(proc.stdout.strip()[-6000:])
        if proc.returncode != 0:
            print(proc.stderr.strip()[-6000:], file=sys.stderr)
            return 1
    finally:
        # **jeder** Ausgang stoppt den Wegwerf-Server — ueber die PID-Datei (Hard Rule 9)
        _stop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
