"""Step D (P9-28 – P9-30): die Abnahmezeilen und ihr Browser-Beleg hängen aneinander.

**Der Fund, aus dem diese Datei entstand.** Am 2026-10-03 stand Step D2 seit dem 2026-09-23 als
gebaut in der Modulstatus-Tabelle, mit **drei** statischen Wächtern in `test_static_routes.py` —
und **null** Fahrten am Browser. Die Wächter prüfen die *Form* des Aufrufs
(`bindFolderDropTarget()` hat genau zwei Aufrufstellen, die Space-Zeile hängt hinter einem
`if (space.own)`), nicht sein *Verhalten*. Drei Abnahmezeilen standen deshalb als ⬜ bzw. ⚠️ „am
Gerät nicht belegt", und die Station, die sie schließen sollte — die erste von GA2 in Plan §11 —
war nie gebaut. Das ist dieselbe Fehlerklasse wie der trace-Beleg vom 2026-10-02: die Aussage
über den Zustand des Codes war richtig, der Beleg für den Zustand *beim Menschen* fehlte, und
beides sieht beim bloßen Öffnen des Heads identisch aus.

**Was diese Tests hier tun — und warum sie nicht nur den Beleg prüfen.** `test_committed_probe_evidence.py`
liest bereits alle `probes/*.json` und verlangt grüne Stationen. Das ist die *Haltegrichtung*:
eine Probe, die rot ist, fällt durch. Die Rückrichtung — eine Abnahmezeile, die ✅ behauptet, ohne
dass eine Station sie trägt — prüft hier niemand, und genau die ist die gefährlichere: sie ist
beim Lesen des Dokuments nicht vom Messwert zu unterscheiden.

Daher die Deckung **in beiden Richtungen**, und dafür trägt jede Station im JSON ihr eigenes
`zeile`-Feld (siehe `pruefe(..., zeile=…)` in `p9_step_d_self_check.py`):

  * Jede Zeile, die die Matrix als belegt führt, braucht **mindestens eine** grüne Station, die
    sie nennt. Fehlt die, ist die ✅ eine Behauptung.
  * Jede Station muss eine Zeile nennen, die in der Matrix überhaupt existiert. Sonst trägt ein
    Beleg eine Abnahme, die es nicht gibt — die Umkehrung desselben Fehlers.
  * Die beiden Gegenläufe liegen **rot** im Repo. Sie sind der Nachweis der Falsifizierbarkeit,
    und sie müssen es bleiben: ein Beleg, dessen Falsifizierbarkeit man nicht zeigt, ist eine
    Behauptung mit Messwerten.

**Gegenproben zu diesem Test** (siehe Commit-Text): eine Station aus der Probe-Datei entfernt ⇒
Test 2 rot; eine Matrix-Zeile auf ⬜ zurückgesetzt ⇒ Test 3 rot; beide Gegenproben zurückgebaut.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PROBE = REPO_ROOT / "phase9_hardening" / "probes" / "p9_step_d_probe.json"
GEGENPROBEN = (
    # **Die Namen sind nicht frei gewählt:** `test_committed_probe_evidence.py` erkennt einen
    # Gegenlauf daran, dass der Dateistem mit `_gegenprobe` **endet** — nicht dass er das Wort
    # enthält. `p9_step_d_gegenprobe_g1.json` enthielt es nur und wäre deshalb als Erfolgsbeleg
    # gelesen worden; beide Tests dort wurden rot. Dass kein einziger der sechs älteren Block-Belege
    # einen Gegenlauf im Repo hat, ist übrigens genau der Grund, warum diese Regel bisher nicht
    # aufgefallen ist — sie wurde gegen noch nicht existierende Dateien geschrieben.
    REPO_ROOT / "phase9_hardening" / "probes" / "p9_step_d_gegenprobe.json",
    REPO_ROOT / "phase9_hardening" / "probes" / "p9_step_d_g2_gegenprobe.json",
)
MATRIX = REPO_ROOT / "phase9_hardening" / "ABNAHME_MATRIX.md"
SCRIPT = REPO_ROOT / "phase9_hardening" / "scripts" / "p9_step_d_self_check.py"

# Die Zeilen, die dieser Test pflegt. Fest verdrahtet statt aus der Matrix gelesen: die Liste ist
# die *Behauptung* dieses Tests, ein Auslesen würde den Test tautologisch machen.
BELEGT_ZEILEN = ("P9-28", "P9-29", "P9-30")


def _probe() -> dict:
    return json.loads(PROBE.read_text(encoding="utf-8"))


def _matrix_zeile(zeile_id: str) -> str:
    """Die Tabellenzeile zu einer Abnahme-ID. `P9-10` muss `P9-10a`/`P9-10b` **nicht** treffen —
    die sind eigene Zeilen, und ein Präfix-Treffer würde die falsche Zeile lesen."""
    for line in MATRIX.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*\*\*(" + re.escape(zeile_id) + r")\*\*\s*\|", line)
        if m:
            return line
    raise AssertionError(f"Abnahmezeile {zeile_id} steht nicht in {MATRIX.name}")


def test_der_step_d_beleg_ist_vorhanden_und_gruen():
    report = _probe()
    assert report.get("alle_ok") is True, "der Beleg meldet sich selbst als nicht gruen"
    assert report["befunde"], "der Beleg traegt keine Stationen"
    assert all(b.get("zeile") for b in report["befunde"]), (
        "eine Station nennt keine Abnahmezeile — die Deckung ist damit nicht pruefbar"
    )


def test_jede_als_belegt_gefuehrte_zeile_hat_mindestens_eine_gruene_station():
    report = _probe()
    gedeckt = {b["zeile"] for b in report["befunde"] if b["ok"]}
    fehlend = [z for z in BELEGT_ZEILEN if z not in gedeckt]
    assert not fehlend, (
        f"die Matrix fuehrt {', '.join(fehlend)} als belegt, aber keine gruene Station der "
        f"Probe nennt sie (gedeckt: {sorted(gedeckt)})"
    )


def test_jede_station_nennt_eine_zeile_die_es_in_der_matrix_gibt():
    report = _probe()
    bekannt = {z for z in re.findall(r"\*\*(P9-\d+[a-z]?)\*\*", MATRIX.read_text(encoding="utf-8"))}
    fremd = sorted({b["zeile"] for b in report["befunde"]} - bekannt)
    assert not fremd, f"Stationen nennen Zeilen, die es in der Matrix nicht gibt: {fremd}"


def test_die_drei_step_d_zeilen_tragen_ihre_zeile_in_der_matrix():
    """Die andere Hälfte desselben Arguments: die Matrix muss die Zeile als belegt führen, und sie
    muss den Beleg **nennen**. Ein ✅ ohne Dateinamen im Detail ist die Behauptung, die dieses
    Konstrukt verhindern soll."""
    for zeile_id in BELEGT_ZEILEN:
        zeile = _matrix_zeile(zeile_id)
        assert "✅" in zeile, f"{zeile_id} ist nicht als belegt gefuehrt: {zeile[:90]}"
        assert PROBE.name in zeile, f"{zeile_id} nennt den Beleg {PROBE.name} nicht"


def test_die_gegenlaeufe_liegen_rot_im_repo():
    """Der Nachweis der Falsifizierbarkeit, und zwar als Datei, nicht als Erinnerung.

    G1 hat die Space-Zeilen-Bindung entfernt (Stationen 2/3/5 müssen rot werden, 6–9 bleiben grün),
    G2 den `fullscreenElement`-Guard (Station 9). Beide Bilder gingen nach `/tmp`, damit kein
    Gegenlauf je den grünen Beleg überschreiben kann — derselbe Fehler wie beim trace-Block
    (2026-10-02), dort hat der Gegenlauf die Probe-Datei im Repo ersetzt."""
    for pfad in GEGENPROBEN:
        assert pfad.exists(), f"Gegenlauf fehlt: {pfad.name}"
        report = json.loads(pfad.read_text(encoding="utf-8"))
        rot = [b["pruefung"] for b in report["befunde"] if not b["ok"]]
        assert rot, f"{pfad.name} ist gruen — ein Gegenlauf, der nichts widerlegt, ist keiner"


def test_das_probeskript_baut_den_zug_aus_echtem_mouse_input_und_nicht_durch_dispatch():
    """Der Wächter gegen den Fehler, den diese Probe zuerst hätte haben können.

    Ein `element.dispatchEvent(new DragEvent(...))` im Skript würde dieselben Stationen grün
    bekommen und **nichts** beweisen: es belegt den Listener, nicht den Zug eines Menschen. Der
    Test verlangt deshalb beide Hälften — `mouse.down`/`move`/`up` als echte Input-Pipeline **und**
    eine Messung, die den vom Browser erzeugten Ereignisstrom überhaupt erst zählt.

    **Die Prüfung läuft über `tokenize`, nicht über den Rohtext** — und das ist keine Feinheit.
    Der erste Entwurf dieses Tests war `assert "dispatchEvent" not in js` und damit **rot**, weil
    das Skript in seinem Docstring genau dieses Wort benennt, um es zu verhindern. Ein Wächter, der
    die Begründung verbietet, verbietet die Sache nicht. Dieselbe Falle ist in Phase 9 dreimal
    passiert (P8.6 Block H, Step G, B17) und wird hier deshalb konstruktiv gelöst: Tokenizer statt
    Textsuche, Kommentare und Strings fliegen raus, gemessen wird der Code.
    """
    import tokenize

    js = SCRIPT.read_text(encoding="utf-8")
    code_zeilen: list[str] = []
    with SCRIPT.open("rb") as fh:
        for tok in tokenize.tokenize(fh.readline):
            if tok.type in (tokenize.COMMENT, tokenize.STRING):
                continue
            code_zeilen.append(tok.string)
    # Der Tokenizer liefert jedes Token einzeln; ohne Leerzeichen ergibt das den **Code** in
    # Normalform, in der ein Aufruf wie `page.mouse.down()` wieder als solcher zu erkennen ist.
    code = "".join(code_zeilen)

    for muster in ("page.mouse.down()", "page.mouse.up()", "page.mouse.move("):
        assert muster in code, f"die Probe benutzt `{muster}` nicht — sie wuerde nicht echt ziehen"
    assert "dispatchEvent" not in code, (
        "das Probeskript dispatcht Drag-Ereignisse selbst — das beweist den Listener, nicht den Zug"
    )
    for muster in ("dragstart", "dragover", "drop"):
        assert muster in js, f"die Ereignisnamen {muster!r} kommen im Skript nicht vor"
