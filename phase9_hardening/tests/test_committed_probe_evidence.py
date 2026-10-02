"""Die committen Browser-Belege müssen grün sein — und ein Gegenlauf darf sie nicht überschreiben.

**Der Fund vom 2026-10-02, aus dem diese Datei entstanden ist.** Das trace-Selbstcheck-Skript hat
keinen Gegenlauf-Mechanismus; der Gegenlauf wurde von Hand gemacht (Leer-Prüfung kurz aus
`editor.js` entfernt, laufen lassen, wiederhergestellt). Skript und Ausgabepfade waren dabei
**dieselben** — also hat der Gegenlauf die Probe-Datei *überschrieben*, und im Commit `43fcac0`
lag als „Browser 8/8"-Beleg eine Probe mit `alle_ok: false` und `S5 ... vorher='alpha'
nachher='beta'`. Das Bild `p9_trace_05_p9z_fremd.png` stammte aus demselben Lauf und zeigte
`beta`, während `screenshots_latest/README.md` es als den positiven Fall („das Feld behält
`alpha`") vorstellte. Der Code war in Ordnung (`editor.js` trug die Leer-Prüfung) — **der Beleg
war es nicht**, und beim ersten erneuten Hinsehen fiel es auf.

Warum ein Test und nicht nur eine Notiz: die anderen drei Proben desselben Verzeichnisses waren
grün, der Fehler ist also *nicht* sichtbar, wenn man nur auf die Datei schaut, die man braucht.

**Grünheit wird über die Stationen gemessen, nicht über die Zusammenfassung.** Die Proben tragen
zwei Formen (`alle_ok: true` bei den Selbstchecks, `result: "ok"` bei den Pixel-Proben), und eine
Zusammenfassung, die den Stationen widerspricht, ist schlimmer als eine fehlende. Deshalb prüft
Test 1 die Stationen, Test 2 die Übereinstimmung.

**Die Regel, die daraus folgt:** ein Gegenlauf schreibt in eine **anders benannte** Datei
(`*_gegenprobe.json` bzw. `*_gegenprobe_*.png`). Diese Tests überspringen solche Dateien bewusst —
sie dürfen rot sein, das ist ihr Zweck.
"""
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PROBE_DIR = REPO_ROOT / "phase9_hardening" / "probes"

GEGENPROBE_SUFFIX = "_gegenprobe"


def _reports() -> list[tuple[Path, dict]]:
    out = []
    for p in sorted(PROBE_DIR.glob("*.json")):
        if p.stem.endswith(GEGENPROBE_SUFFIX):
            continue
        out.append((p, json.loads(p.read_text(encoding="utf-8"))))
    return out


def _rote_stationen(report: dict) -> list[str]:
    return [b.get("pruefung", "?") for b in report.get("befunde", []) if not b.get("ok")]


def _sagt_gruen(report: dict) -> bool | None:
    """Was die Zusammenfassung behauptet, oder None, wenn die Datei keine trägt."""
    for key in ("alle_ok", "result", "ok"):
        if key in report:
            return report[key] is True or report[key] == "ok"
    return None


def test_the_probe_directory_is_not_empty():
    assert _reports(), "es gibt keine Probe — dann prüft dieser Test ins Leere"


def test_every_committed_probe_has_no_red_station():
    rot = []
    for p, report in _reports():
        if stationen := _rote_stationen(report):
            rot.append(f"{p.name}: {stationen}")
    assert not rot, (
        "im Repo liegen Browser-Belege mit roten Stationen, die als Erfolgsnachweis zitiert werden: "
        + "; ".join(rot)
        + f" — ein Gegenlauf gehört nach *{GEGENPROBE_SUFFIX}*.json"
    )


def test_a_probe_summary_agrees_with_its_stations():
    """Test 1 liest die Stationen, Test 2 die Zusammenfassung. Widersprechen sie sich, ist der
    Fehler nicht 'die Probe ist rot', sondern 'die Probe lügt' — das ist der härtere Fall, und
    er ist beim bloßen Öffnen der Datei nicht sichtbar."""
    widerspruch = []
    for p, report in _reports():
        sagt = _sagt_gruen(report)
        if sagt is None:
            continue
        stationen_oder_rot = bool(_rote_stationen(report))
        # Widerspruch, wenn die Zusammenfassung "gruen" sagt, aber eine Station rot ist — oder
        # umgekehrt. (Ein Rot-Befund und eine gruene Zusammenfassung ist derselbe Widerspruch.)
        if sagt == stationen_oder_rot:
            widerspruch.append(
                f"{p.name}: Zusammenfassung sagt {'gruen' if sagt else 'rot'}, "
                f"Stationen sind {'nicht gruen' if stationen_oder_rot else 'alle gruen'}"
            )
    assert not widerspruch, "; ".join(widerspruch)


def test_a_counter_probe_may_be_red_but_must_be_named_like_one():
    for p, report in _reports():
        if _rote_stationen(report) or _sagt_gruen(report) is False:
            assert p.stem.endswith(GEGENPROBE_SUFFIX), (
                f"{p.name} enthaelt rote Stationen, heisst aber nicht *{GEGENPROBE_SUFFIX}.json"
            )
