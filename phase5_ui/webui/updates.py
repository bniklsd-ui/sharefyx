"""`docs/UPDATE_LOG.md`-Parser (Plan §1.8, §2.4, §4 Step 3). Streng, wie im Plan gefordert: `##
<ISO-Datum>` beginnt einen Eintrag, `- ` beginnt eine Zeile darin, alles andere wird ignoriert.
Kein Markdown-Rendering hier — `app.js` rendert die Zeilen mit dem bereits vorhandenen
Sanitizer (`markdownToHtml`/`sanitizeHtml`), „der Server ist dumm" gilt auch für einen
Klartext-Log.

**ID-Vergabe:** `"<Datum>#<n>"`, `n` = 1-basierte Position DIESES Datums unter den bisher
gesehenen Überschriften, **von unten gezählt** — der älteste Block eines Datums bekommt die #1,
jeder **oben** eingefügte Block die nächste freie Nummer. Kein globaler Zähler und kein
Zähler pro Aufzählungspunkt (ein Eintrag trägt beliebig viele `lines`).

**[2026-10-23, P10.5 Block 7, Schritt 7.0 — datierte Korrektur, Befund vom 2026-10-23]:**
vorher lief der Zähler **von oben** (Dateireihenfolge). Neue Einträge werden aber **oben**
eingefügt (Changelog-Konvention) — und der gesehen-Zustand hängt genau an dieser ID
(`users.seen_update_id`). Ein **zweiter Deploy am selben Tag** bekam damit die ID `#1`, die der
erste Deploy dieses Tages **schon** hatte: `latest_id == seen_update_id` ⇒ **kein Banner**, der
neue Eintrag war für den Benutzer stumm. Gemessen in
`phase10_5_finishing/probes/p105_deploy_b_probe.py` (Gruppe E). Der Zähler läuft jetzt von
unten: die IDs der **bestehenden** Blöcke bleiben dabei stehen (der älteste Block eines Datums
hatte vorher schon die #1), ein neu oben eingefügter Block bekommt eine **neue** ID. Ein
Sonderfall bleibt: bei einem Datum mit **zwei** Blöcken (2026-10-23, 2026-09-01, 2026-08-13)
**tauschen** die beiden IDs ihre Plätze — wer damals den oberen Block gesehen hat, sieht ihn
**einmal** wieder (harmlos, der Block ist längst alt).

**Reihenfolge = Dateireihenfolge, keine Sortierung.** Neue Einträge werden oben eingefügt (wie
ein Changelog) — der ERSTE Eintrag der Datei ist damit der neueste; `latest_id` in `webui/api.py`
liest deshalb `entries[0]`, nicht das Maximum über `date`.

**Fail-soft, nie ein 500 (`load_update_log()`):** fehlende Datei oder ein Encoding-Fehler ⇒ leere
Liste ⇒ kein Banner. Ein kaputtes `UPDATE_LOG.md` darf die UI nicht lahmlegen."""
from __future__ import annotations

import re
from dataclasses import dataclass, field, replace
from pathlib import Path

_HEADING_RE = re.compile(r"^## (\d{4}-\d{2}-\d{2})\s*$")
_LINE_RE = re.compile(r"^- (.+)$")


@dataclass(frozen=True)
class UpdateEntry:
    id: str
    date: str
    lines: list[str] = field(default_factory=list)


def parse_update_log(text: str) -> list[UpdateEntry]:
    """Parst `docs/UPDATE_LOG.md` — streng, wie im Plan gefordert.

    **Zwei Durchgänge, absichtlich:** erst die Blöcke einsammeln (Überschrift + Zeilen), dann
    die IDs vergeben. Die IDs müssen **je Datum von unten** gezählt werden, damit ein neu
    **oben** eingefügter Block eine ID bekommt, die **kein** bestehender Block schon trägt —
    davon hängt der Update-Banner ab (`latest_id` vs. `users.seen_update_id`). Der Grund steht
    im Moduldocstring.
    """
    eintraege: list[UpdateEntry] = []
    datum: str | None = None
    zeilen: list[str] = []
    for raw_line in text.splitlines():
        heading = _HEADING_RE.match(raw_line)
        if heading is not None:
            if datum is not None:
                eintraege.append(UpdateEntry(id="", date=datum, lines=zeilen))
            datum = heading.group(1)
            zeilen = []
            continue
        line = _LINE_RE.match(raw_line)
        if line is not None and datum is not None:
            zeilen.append(line.group(1))
    if datum is not None:
        eintraege.append(UpdateEntry(id="", date=datum, lines=zeilen))

    # Der Zähler läuft **von unten** (rückwärts über die Liste): der älteste Block eines
    # Datums bekommt die #1, der nächste darüber die #2, und so weiter.
    zaehler: dict[str, int] = {}
    for index in range(len(eintraege) - 1, -1, -1):
        eintrag = eintraege[index]
        zaehler[eintrag.date] = zaehler.get(eintrag.date, 0) + 1
        eintraege[index] = replace(eintrag, id=f"{eintrag.date}#{zaehler[eintrag.date]}")
    return eintraege


def load_update_log(path: Path) -> list[UpdateEntry]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return []
    return parse_update_log(text)
