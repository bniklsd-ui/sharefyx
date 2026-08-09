"""`docs/UPDATE_LOG.md`-Parser (Plan §1.8, §2.4, §4 Step 3). Streng, wie im Plan gefordert: `##
<ISO-Datum>` beginnt einen Eintrag, `- ` beginnt eine Zeile darin, alles andere wird ignoriert.
Kein Markdown-Rendering hier — `app.js` rendert die Zeilen mit dem bereits vorhandenen
Sanitizer (`markdownToHtml`/`sanitizeHtml`), „der Server ist dumm" gilt auch für einen
Klartext-Log.

**ID-Vergabe:** `"<Datum>#<n>"`, `n` = 1-basierte Position DIESES Datums unter den bisher
gesehenen Überschriften, in Dateireihenfolge — disambiguiert zwei `## <selbes Datum>`-Blöcke,
kein globaler Zähler und kein Zähler pro Aufzählungspunkt (ein Eintrag trägt beliebig viele
`lines`).

**Reihenfolge = Dateireihenfolge, keine Sortierung.** Neue Einträge werden oben eingefügt (wie
ein Changelog) — der ERSTE Eintrag der Datei ist damit der neueste; `latest_id` in `webui/api.py`
liest deshalb `entries[0]`, nicht das Maximum über `date`.

**Fail-soft, nie ein 500 (`load_update_log()`):** fehlende Datei oder ein Encoding-Fehler ⇒ leere
Liste ⇒ kein Banner. Ein kaputtes `UPDATE_LOG.md` darf die UI nicht lahmlegen."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

_HEADING_RE = re.compile(r"^## (\d{4}-\d{2}-\d{2})\s*$")
_LINE_RE = re.compile(r"^- (.+)$")


@dataclass(frozen=True)
class UpdateEntry:
    id: str
    date: str
    lines: list[str] = field(default_factory=list)


def parse_update_log(text: str) -> list[UpdateEntry]:
    entries: list[UpdateEntry] = []
    seen_per_date: dict[str, int] = {}
    current: UpdateEntry | None = None
    for raw_line in text.splitlines():
        heading = _HEADING_RE.match(raw_line)
        if heading is not None:
            date = heading.group(1)
            seen_per_date[date] = seen_per_date.get(date, 0) + 1
            current = UpdateEntry(id=f"{date}#{seen_per_date[date]}", date=date)
            entries.append(current)
            continue
        line = _LINE_RE.match(raw_line)
        if line is not None and current is not None:
            current.lines.append(line.group(1))
    return entries


def load_update_log(path: Path) -> list[UpdateEntry]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return []
    return parse_update_log(text)
