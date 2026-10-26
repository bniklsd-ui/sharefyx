"""Wächter für den **Seed** des Kartenlayouts — P10.5 Block 14, Schritt 14.1.

`graph.js` ist ein ES-Modul ohne Build-Schritt (P5-T). Der **Seed** (die Welt-Geometrie aus
`computeRegions()`) ist reine Rechnung — sie lässt sich deshalb **ohne Browser** messen: der
Harness `phase10_5_finishing/probes/p105_b14_layout_probe.mjs` lädt das echte Modul in Node
und ruft die exportierte Funktion (Muster: `p105_b8_c2_probe.mjs`).

**Fünf Messungen, fünf Gegenläufe.** Ein Wächter ohne Gegenlauf beweist nichts: eine Messung,
die die falsche Sache misst, ist grün und falsch zugleich (diese Fehlerklasse hat dieser
Ordner zweimal gesehen). Jeder Gegenlauf patcht **eine** Regel in einer Kopie von `graph.js`
und muss **genau die** zugehörige Messung rot machen — nicht nur "irgendeine".

| Messung | Regel (Plan) | Gegenlauf |
|---|---|---|
| `regionen` | §2.1 L1 — eine Region je Space | `anker` (alle Anker auf einem Punkt) |
| `inseln` | §2.2 L2 — die Ordner bilden Gruppen | `inselabstand` (alle Inseln auf dem Anker) |
| `spiralen` | §2.3 L3 — die Items auf einer Goldwinkel-Spirale | `itemradius` (alle Items auf einem Kreis) |
| `stabilitaet` | §2.1 — ein neues Item verschiebt die Anker **nur** beim groessten Space | `slot` |
| `determinismus` | §1 — der Zufall ist der Hash, nicht der Zufallsgenerator | `jitter` |

**Die Reihenfolge der Anker wird unabhaengig nachgeprueft:** der Wächter rechnet den FNV-1a
selbst (in Python) und vergleicht mit der Reihenfolge, die das Modul gemeldet hat. Ein Modul,
das die Spaces nach der Item-Zahl statt nach dem Hash ordnet, fällt hier auf (das ist der
Gegenlauf des Plans §5 für die Regionen-Zelle in Schritt 14.2).

Kein Netz, kein Browser, kein DATA_ROOT, kein Dienst. Node muss vorhanden sein; fehlt es,
überspringt die Laufzeitprüfung (die Testdateien laufen trotzdem).
"""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
PROBE = REPO_ROOT / "phase10_5_finishing" / "probes" / "p105_b14_layout_probe.mjs"

needs_node = pytest.mark.skipif(shutil.which("node") is None, reason="node fehlt (P5-T: kein Build)")

#: Die Messungen und ihre Gegenlaeufe. Der Name des Gegenlaufs muss in der Probe stehen --
#: ein Tippfehler im Wächter waere sonst ein Gegenlauf, der nichts tut (und trotzdem "gruen"
#: meldet).
MESSUNGEN = [
    ("regionen", "anker"),
    ("inseln", "inselabstand"),
    ("spiralen", "itemradius"),
    ("stabilitaet", "slot"),
    ("determinismus", "jitter"),
]

#: Der Datensatz (derselbe wie in der Browser-Probe `p105_b14_layout_probe.py`): fuenf Spaces,
#: 152 Items (30/32/30/30/30 — `beta` hat 32, damit "der groesste Space" eindeutig ist).
SPACES = ["alpha", "beta", "gamma", "delta", "epsilon"]
ITEMS_PRO_SPACE = {"alpha": 30, "beta": 32, "gamma": 30, "delta": 30, "epsilon": 30}
ITEMS = 152
OWN_SPACE = "alpha"


def _fnv1a(text: str) -> int:
    """FNV-1a, 32 Bit -- **unabhaengig** nachgerechnet (der Wächter soll das Modul pruefen, nicht
    es nachbilden). `Math.imul` in JavaScript ist eine 32-Bit-Multiplikation; die Bits sind
    dieselben wie bei der unsignierten Multiplikation modulo 2^32."""
    h = 2166136261
    for zeichen in text:
        h ^= ord(zeichen)
        h = (h * 16777619) & 0xFFFFFFFF
    return h


def _erwartete_reihenfolge() -> list[str]:
    """Der eigene Space zuerst, die anderen nach dem Hash ihres Namens (Plan §2.1)."""
    fremde = sorted(
        (s for s in SPACES if s != OWN_SPACE),
        key=lambda s: (_fnv1a(s), s),
    )
    return [OWN_SPACE] + fremde


def _run(gegenlauf: str | None = None) -> dict:
    cmd = ["node", str(PROBE)]
    if gegenlauf:
        cmd += ["--gegenlauf", gegenlauf]
    proc = subprocess.run(
        cmd, cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=180,
    )
    assert proc.returncode == 0, (
        f"p105_b14_layout_probe.mjs endete mit {proc.returncode}\n"
        f"--- stdout ---\n{proc.stdout}\n--- stderr ---\n{proc.stderr}"
    )
    return json.loads(proc.stdout)


@pytest.fixture(scope="module")
def messung() -> dict:
    """Der Normalfall: alle fuenf Messungen muessen gruen sein."""
    return _run()


@needs_node
def test_alle_messungen_sind_gruen(messung: dict) -> None:
    """Der Normalfall — jede Messung traegt ihr eigenes `ok`."""
    rot = [name for name, _ in MESSUNGEN if not messung["messungen"][name].get("ok")]
    assert not rot, f"diese Messungen sind rot: {rot}"


@needs_node
def test_der_beleg_nennt_den_datensatz_und_die_zahlen(messung: dict) -> None:
    """Der Beleg muss den **Datensatz** nennen und die Zahlen, aus denen die Zellen gingen —
    ohne sie ist "gruen" eine Behauptung."""
    assert messung["schritt"] == "14.1", f"der Beleg ist Schritt {messung['schritt']}"
    assert messung["fixture"]["spaces"] == 5
    assert messung["fixture"]["items"] == ITEMS
    assert messung["fixture"]["items_pro_space"] == ITEMS_PRO_SPACE
    assert messung["fixture"]["own_space"] == OWN_SPACE

    m = messung["messungen"]
    # Regionen (L1): **alle** Knoten liegen ihrem eigenen Space am naechsten, mit deutlichem
    # Abstand zum naechsten fremden Schwerpunkt.
    reg = m["regionen"]
    assert reg["knoten"] == ITEMS
    assert reg["richtig"] == ITEMS, "jeder Knoten liegt seinem eigenen Space am naechsten"
    assert reg["anteil"] == pytest.approx(1.0, abs=1e-9)
    assert reg["engster_abstand_px"] > 10.0, (
        "der Abstand zum naechsten fremden Schwerpunkt muss deutlich sein -- sonst entscheidet "
        "der Zufall")
    # Inseln (L2): die Gruppenbildung -- der Abstand zwischen zwei Inseln ist ein Vielfaches
    # des Abstands innerhalb einer Insel.
    ins = m["inseln"]
    assert ins["spaces_geprueft"] == 5
    for eintrag in ins["roh"]:
        assert eintrag["faktor"] >= 1.8, f"die Inseln von {eintrag['space']} bilden keine Gruppe"
        assert eintrag["kleinster_mittenabstand"] > 1.0, "zwei Inseln liegen auf demselben Punkt"
    # Spiralen (L3): der Radius waechst mit dem Rang, der Winkelabstand ist der Goldwinkel.
    spi = m["spiralen"]
    assert spi["inseln_geprueft"] == 20, "20 Inseln mit Items (5 Spaces x 4 Ordner)"
    assert spi["inseln_ok"] == spi["inseln_geprueft"]
    # Stabilitaet: die Anker bleiben byte-gleich; der wachsende Space selbst darf sich bewegen
    # (seine Region waechst mit) -- das ist die gewollte Wirkung.
    stab = m["stabilitaet"]
    assert stab["wachser_space"] == "epsilon"
    assert stab["groesster_space"] == "beta", "der groesste Space muss eindeutig sein"
    assert stab["anker_verschoben"] == 0, "die Anker der anderen Spaces haben sich bewegt"
    assert stab["groesster_anker_versatz_px"] == 0.0
    assert stab["positionen_verschoben"] == 0, "die Items der anderen Spaces haben sich bewegt"
    assert stab["eigene_positionen_verschoben"] > 0, "der wachsende Space waechst (das ist gewollt)"
    assert stab["eigener_versatz_px"] < 5.0, "der eigene Versatz ist klein (die Wurzel waechst)"
    # Determinismus (P10.5-65): derselbe Datensatz ergibt dieselbe Welt.
    det = m["determinismus"]
    assert det["knoten"] == ITEMS
    assert det["verglichen"] == ITEMS
    assert det["max_abweichung_px"] <= 1.0


@needs_node
def test_die_reihenfolge_der_anker_ist_der_hash_und_nicht_die_item_zahl(messung: dict) -> None:
    """Die Reihenfolge der Anker ist der **Hash des Space-Namens** (Plan §2.1) -- nicht die
    Item-Zahl (die waechst mit jedem neuen Item und wuerde alle Anker verschieben).

    Der Wächter rechnet den FNV-1a **selbst** und vergleicht: ein Modul, das die Spaces nach
    der Item-Zahl sortiert, faellt hier auf -- und zwar unabhaengig davon, wie die Probe
    zaehlt."""
    erwartet = _erwartete_reihenfolge()
    assert messung["reihenfolge"] == erwartet, (
        "die Anker-Reihenfolge ist nicht der Hash des Space-Namens")
    # **Der Datensatz muss die beiden Reihenfolgen unterscheiden koennen** -- sonst waere der
    # Test blind (bei 30/32/30/30/30 sind "Hash" und "Item-Zahl" zufaellig nicht gleich).
    nach_zahl = sorted(
        (s for s in SPACES if s != OWN_SPACE),
        key=lambda s: (-ITEMS_PRO_SPACE[s], s),
    )
    assert nach_zahl != erwartet[1:], (
        "der Datensatz kann die Item-Zahl-Reihenfolge nicht von der Hash-Reihenfolge "
        "unterscheiden -- der Test waere dann aussagelos")


@needs_node
@pytest.mark.parametrize("messung_name,gegenlauf", MESSUNGEN)
def test_der_gegenlauf_macht_genau_seine_zelle_rot(messung_name: str, gegenlauf: str) -> None:
    """**Jeder Gegenlauf macht genau eine Zelle rot** -- seine.

    Macht er mehrere rot, prueft er nicht seine Regel, sondern etwas anderes (diese
    Fehlerklasse hat die C2-Probe einmal gehabt: ein Gegenlauf, der die ganze Karte kaputt
    macht, beweist fuer nichts). Macht er keine rot, prueft die gruene Zelle nichts."""
    bericht = _run(gegenlauf)
    rot = [name for name, _ in MESSUNGEN if not bericht["messungen"][name].get("ok")]
    assert rot == [messung_name], (
        f"der Gegenlauf {gegenlauf!r} macht {rot} rot — er muss genau [{messung_name!r}] rot machen")


@needs_node
def test_ein_manipulierter_beleg_wuerde_abgelehnt() -> None:
    """Die Gegenprobe: **dieselbe** Prueffunktion (nicht eine nachgebaute Logik) muss an einem
    manipulierten Beleg rot werden -- sonst prueft der Wächter nichts."""
    beleg = _run()
    beleg["messungen"]["regionen"]["richtig"] = 12
    with pytest.raises(AssertionError):
        test_der_beleg_nennt_den_datensatz_und_die_zahlen(beleg)
