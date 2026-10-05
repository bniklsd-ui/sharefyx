"""Gate/Z (2026-10-03) — die `updated:`-Kette ist ein **Werkzeugvertrag**, nicht nur Prosa.

`scripts/rotate_index_updates.sh` (P9-L) hat drei Vorbedingungen, an denen eine Kette scheitern
kann, und keine davon ist im Fließtext sichtbar:

1. Das Feld muss `^updated: ` tragen — das Skript sucht die Zeile mit `grep -n '^updated: '` und
   bricht sonst mit „Keine 'updated:'-Zeile in der Frontmatter gefunden" ab.
2. Der Split-Anker ist `' | ' + ISO-Datum`. Ein Faden, der mit `updated: ` beginnt, sieht für
   diesen Anker **nicht** wie ein Kettenanfang aus und bleibt beim Rotieren stehen — der Fund vom
   2026-10-02, seit dem das Skript dafür die Gegenprobe (e) hat.
3. Derselbe Anker ist blind für ` · ` als Trenner. Auch das war kein Theoriestück: in
   `phase9_hardening/SESSIONS_ARCHIVE.md` trug die Kette **beide** Trenner nebeneinander.

**Dritte Ausprägung derselben Fehlerklasse, gefunden am 2026-10-03:** dasselbe Archiv hatte das
Feld `updated:` **gar nicht mehr** — die Kette stand als nackte Zeile unter `down:`. Das ist eine
Regression: Commit `aee387d` hatte dem Feld das Präfix genommen, der Fund vom 2026-10-02 stellte
es wieder her, und zwei Commits später war es wieder weg. `doc_health` prüft das Feld nicht, also
hat es niemanden gemeldet. Gemessen war der Schaden: **7 von 29 Fäden** (24 %) waren für das
Werkzeug unsichtbar — 4 wegen des Präfixes, 3 wegen des ` · `-Trenners.

**Was hier nicht gebaut wird:** die anderen Dateien mit demselben Defekt. Sie liegen in
abgeschlossenen Phasen, in `ROADMAP.md` oder in einem 📕-Snapshot, den die L0-Konvention nie
wieder editieren lässt — das ist eine Entscheidung des Ningkers, keine Formkorrektur von M3. Sie
stehen deshalb in `KNOWN_OFFENDERS` **mit Fundstelle und Anzahl**, damit die Liste nicht wachsen
kann, ohne dass sie auffällt. Muster wie `EXEMPT_HEX` in `test_static_routes.py`.

**Gegenprobe statt Augenschein:** `test_the_checker_itself_catches_what_it_claims` füttert dem
Prüfer die drei Ausprägungen als Text ein und verlangt, dass jede als Fehler gemeldet wird. Ein
Wächter, der nur grün werden kann, ist der übliche Fehler an dieser Stelle.
"""
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SKIP_DIRS = {".git", ".venv", ".pytest_cache", "node_modules", ".agents", ".claude", ".playwright-mcp"}

# Die Werkzeug-Regeln, 1:1 die Vorbedingungen von `scripts/rotate_index_updates.sh`.
FIELD_RE = re.compile(r"^updated: ", re.M)
CHAIN_RE = re.compile(r"\d{4}-\d{2}-\d{2}\s*\(")          # eine datierte Kette ist da …
SPLIT_ANCHOR_RE = re.compile(r" \| (?=\d{4}-\d{2}-\d{2})")  # … und so sieht der Anker ihren Anfang
THREAD_PREFIX_RE = re.compile(r" \| updated: (?=\d{4}-\d{2}-\d{2})")
# Ein Faden, der **gar keinen** ` | `-Trenner hat, ist für denselben Anker ebenfalls blind — und
# das ist die **vierte** Ausprägung, gefunden am 2026-10-04 von `prepend_updated_chain.sh`, das
# beim Voranstellen eines Fadens abbrach: "ein Faden beginnt bei 8919 ohne ' | '-Trenner". Die drei
# vorhandenen Prüfungen dieses Moduls (Feld, ` | updated: `, ` · `) erkennen das **nicht**.
DATE_START_RE = re.compile(r"\d{4}-\d{2}-\d{2}\s*\(")
# Der zweite Blickblick schließt den ` | updated: `-Präfix aus: ein präfigierter Faden ist blind,
# aber **aus dem anderen Grund** — Clause 2 dieser Datei meldet ihn schon, undClause 4 soll nicht
# dieselbe Fundstelle zweimal zählen. Zwei getrennte Assertions, weil Python keine Lookbehinds
# verschiedener Breite in einer Klammer erlaubt.
BLIND_RE = re.compile(r"(?<! \| )(?<!updated: )\d{4}-\d{2}-\d{2}\s*\(")
DOT_SEPARATOR_RE = re.compile(r" · (?=\d{4}-\d{2}-\d{2}\s*\()")

# Datei -> (fehlendes `updated:`-Feld, Fäden mit Präfix, Fäden hinter ` · `).
# Alle fünf sind **gemessen** am 2026-10-03, keine Schätzung; `docs/screenshots/README.md` hat
# zusätzlich gar kein Feld. Wer eine Zeile repariert, streicht sie hier — und die Größenangabe in
# `docs/INDEX.md` zieht mit (das hat `doc_health` am 2026-10-03 zweimal rot gemeldet).
# **2026-10-05:** `screenshots_latest/README.md` ist repariert (zwei Fäden mit `updated: `-Präfix
# entfernt, Fadeninhalte byte-identisch) — die Datei stand in der Liste, weil ein Ganzzahl-Eintrag
# mit zwei Fäden nicht abnimmt, wenn man einen davon repariert; sie ist deshalb **ganz** gestrichen
# und nicht auf 1 heruntergezählt.
# **2026-10-05, später am Tag:** dasselbe für `docs/screenshots/README.md`, und dort waren es
# **beide** Ausprägungen zugleich — das `updated:`-Feld fehlte ganz (deshalb `missing=True`) und
# zwei von sechs Fäden trugen ein `updated: `-Präfix. Repariert wurde in zwei Schritten, weil
# `scripts/prepend_updated_chain.sh` ein vorhandenes `^updated: ` **verlangt** und sonst abbricht
# (Gegenprobe (e)): erst das Feld und die zwei Präfixe, mit einer Byte-Gegenprobe, die die sechs
# Fadeninhalte einzeln gegen die alte Zeile stellt, dann der neue Faden mit dem Skript. Der
# Eintrag ist **gestrichen**, nicht auf 0/0 gesetzt: mit 0-0-Präfixen und fehlendem Feld wäre er
# eine unsichtbare Ausnahme, deren Verschwinden kein Test bemerkt.
KNOWN_OFFENDERS: dict[str, tuple[bool, int, int]] = {
    "ROADMAP.md": (False, 4, 0),
    "docs/concepts/phase9_hardening_block_trace_plan.md": (False, 1, 0),  # 📕, nie editieren
    "phase8_6_ui_polish/CLAUDE.md": (False, 1, 0),  # abgeschlossene Phase
}


def frontmatter(path: Path) -> str | None:
    """Frontmatter als Text, oder `None` wenn die Datei keins hat."""
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 3)
    return None if end < 0 else text[4 : end + 1]


def chain_defects(fm: str) -> tuple[bool, int, int]:
    """Die drei Vorbedingungen an einer Frontmatter: (Feld da?, Faden-Präfixe, ` · `-Trenner).

    Geprüft wird **nur** eine datierte Kette (`CHAIN_RE`) — eine Datei ohne eine solche Zeile hat
    nichts zu rotieren, und `FOO: bar` in einer Kartenzeile ist kein Faden.
    """
    if not CHAIN_RE.search(fm):
        return (False, 0, 0)
    return (
        not bool(FIELD_RE.search(fm)),
        len(THREAD_PREFIX_RE.findall(fm)),
        len(DOT_SEPARATOR_RE.findall(fm)),
    )

# Datumsanfänge, die der Anker nicht sieht und die **doch** keine Verstoße sind — oder
# Verstoße in fremden Dateien, die nicht gebaut wurden. Zwei Arten, eine Liste: Sie sind
# harmlos — ohne ` | ` davor schneidet der Anker dort nie —, aber sie tauchen in jeder Zählung auf
# und müssen deshalb **namentlich** benannt sein, sonst ist die Zahl nicht prüfbar. Nach dem Kontext
# benannt, nicht nach Byte-Offset: ein Offset ändert sich bei jedem neuen Faden.
KNOWN_BLIND: dict[str, list[str]] = {
    # **Zwei echte verklebte Fäden in fremden Phasen — nicht gebaut.** Sie folgen dem Muster der
    # beiden anderen Ausnahmelisten dieses Moduls: gemessen, benannt, nicht angefasst. Wer sie
    # repariert, streicht sie hier, und `test_the_named_blind_spots_still_exist` meldet den Eintrag
    # als tot. Nach dem Kontext benannt, nicht nach Byte-Offset — ein Offset ändert sich bei jedem
    # neuen Faden, ein Kontext nicht.
    "phase6_shares/IMAGES_PLAN.md": [
        "2026-08-19 (neu geschrieben, Planungssession",  # 1 Faden, abgeschlossene Phase
    ],
    "phase8_5_picker_release/SESSIONS_ARCHIVE.md": [
        "2026-09-07 (D4-Sichtprobe-Folgesession-Block rotiert",  # 1 Faden, Archiv
    ],
}
# **`phase9_hardening/SESSIONS_ARCHIVE.md` stand am 2026-10-04 kurz in dieser Liste und ist jetzt
# leer** — und damit ist das der Grund, warum die Liste kein leeres Element zulassen darf: ein
# Kommentar-Element wäre ein Wächter, der **nur grün werden kann**, die schlimmere Form von
# "kein Fund". Die Datei trug drei verklebte Fäden (repariert, +9 B) **und** eine Prosa-Erwähnung
# "Head trägt Block 2026-09-25 (3)", die wie ein Faden aussieht: das Datum ist das Datum *dieses*
# Fadens und steht bereits am Fadenanfang, also ist "Head trägt Block (3)" **verlustfrei in der
# Sache** und behebt zugleich den Abbruch von `prepend_updated_chain.sh` — das Skript kann einen
# Faden und eine Erwähnung nicht unterscheiden und bricht fail-closed ab, was richtig ist. Seitdem
# hat diese Datei **null** blinde Stellen, und taucht wieder eine auf, ist sie ein frischer Verstoß.


def blind_positions(fm: str) -> list[str]:
    """Datumsanfänge einer Kette, die der Rotations-Anker nicht sieht (Kette selbst ausgenommen)."""
    if not CHAIN_RE.search(fm):
        return []
    line = next((l for l in fm.splitlines() if l.startswith("updated: ")), "")
    body = line[len("updated: ") :]
    # Gesucht wird in `body[1:]`, damit der **erste** Faden (Position 0) nicht als verklebt gilt —
    # und indiziert wird in denselben String. Ein Off-by-one an dieser Stelle hat die erste Fassung
    # erzeugt: die Treffer begannen mit dem Trennerzeichen statt mit dem Datum.
    rest = body[1:]
    return [rest[mm.start() : mm.start() + 60] for mm in BLIND_RE.finditer(rest)]


def md_files() -> list[Path]:
    out: list[Path] = []
    for path in REPO_ROOT.rglob("*.md"):
        if SKIP_DIRS & set(path.relative_to(REPO_ROOT).parts):
            continue
        out.append(path)
    return sorted(out)


def offenders() -> list[str]:
    found: list[str] = []
    for path in md_files():
        rel = path.relative_to(REPO_ROOT).as_posix()
        fm = frontmatter(path)
        if fm is None:
            continue
        missing, prefixes, dots = chain_defects(fm)
        if missing or prefixes or dots:
            known = KNOWN_OFFENDERS.get(rel)
            if known is not None and known == (missing, prefixes, dots):
                continue  # gemessen, benannt, unverändert — siehe Moduldocstring
            found.append(
                f"{rel}: Feld={'fehlt' if missing else 'da'}, "
                f"Fäden mit ' | updated: '={prefixes}, Fäden hinter ' · '={dots}"
            )
    return found


def test_no_unnamed_file_breaks_the_rotation_contract():
    assert offenders() == []


def test_the_known_offenders_still_look_exactly_as_measured():
    """Gegenprobe: die Ausnahmeliste darf nicht still veralten.

    Wer eine Fundstelle repariert, muss sie hier streichen — sonst meldet dieser Test den
    Veteranen als *unbekannten* Verstoß und der eigentliche Wächter bleibt grün. Umgekehrt
    verschwindet ein reparierter Eintrag nicht einfach: er taucht als frischer Verstoß auf.
    """
    measured: dict[str, tuple[bool, int, int]] = {}
    for path in md_files():
        rel = path.relative_to(REPO_ROOT).as_posix()
        if rel not in KNOWN_OFFENDERS:
            continue
        fm = frontmatter(path)
        assert fm is not None, f"{rel} hat gar kein Frontmatter mehr"
        measured[rel] = chain_defects(fm)
    assert measured == KNOWN_OFFENDERS, (
        "Die Ausnahmeliste stimmt nicht mehr mit dem Repo überein — entweder ist eine Fundstelle "
        "repariert (dann hier streichen, die Korrektur aber in der Session festhalten) oder ein "
        "neuer Verstoß ist dazugekommen (dann in KNOWN_OFFENDERS mit Fundstelle aufnehmen)"
    )


def test_the_checker_itself_catches_what_it_claims():
    """Gegenprobe am Prüfer, nicht am Datenbestand."""
    with_field = "status: live\nupdated: 2026-10-03 (a) | 2026-10-02 (b)\n"
    missing_field = "status: live\ndown:\n2026-10-03 (a) | 2026-10-02 (b)\n"
    thread_prefix = "updated: 2026-10-03 (a) | updated: 2026-10-02 (b)\n"
    dot_separator = "updated: 2026-10-03 (a) · 2026-10-02 (b)\n"
    no_chain = "status: live\nupdated: 2026-10-03 (P9-L gebaut)\n"  # Faden, aber keine Kette

    assert chain_defects(with_field) == (False, 0, 0)
    assert chain_defects(missing_field) == (True, 0, 0)
    assert chain_defects(thread_prefix) == (False, 1, 0)
    assert chain_defects(dot_separator) == (False, 0, 1)
    assert chain_defects(no_chain) == (False, 0, 0)


def test_the_split_anchor_really_is_blind_for_a_prefixed_thread():
    """Der Anker, nicht der Prüfer: diese beiden Fäden sind für das Skript **ein** Thread.

    Ohne diesen Test könnte der Prefix-Defekt für einen Fehler des Prüfers gehalten werden — der
    Prüfer könnte zählen, was das Skript nie sehen würde, und der Fehler bliebe unentdeckt.
    """
    broken = "2026-10-03 (a) | updated: 2026-10-02 (b)"
    fixed = "2026-10-03 (a) | 2026-10-02 (b)"
    assert len(SPLIT_ANCHOR_RE.split(broken)) == 1
    assert len(SPLIT_ANCHOR_RE.split(fixed)) == 2


def test_no_thread_is_invisible_to_the_rotation_anchor():
    """Die vierte Ausprägung, und die ist von `prepend_updated_chain.sh` gefunden worden.

    Am 2026-10-04 brach das Skript beim Voranstellen ab: die Kette von `SESSIONS_ARCHIVE.md` trug
    **drei** Fäden, die ohne jeden ` | `-Trenner in ihrem Vorgänger klebten (30 sichtbare Fäden bei
    33 Rotationssätzen). Repariert (+9 B, Fadeninhalte byte-identisch). Ohne diesen Test wäre der
    Defekt beim nächsten Rotieren **stillschweigend** wieder aufgetreten — das Skript bricht ab,
    aber es *findet* nicht, und diese Datei wird nicht bei jedem Rotieren angefasst.
    """
    for path in md_files():
        rel = path.relative_to(REPO_ROOT).as_posix()
        fm = frontmatter(path)
        if fm is None:
            continue
        blind = blind_positions(fm)
        if not blind:
            continue
        named = KNOWN_BLIND.get(rel, [])
        unexpected = [b for b in blind if not any(b.startswith(n[:20]) for n in named)]
        assert not unexpected, (
            f"{rel}: {len(unexpected)} Faden(fäden) ohne ' | '-Trenner, also für "
            f"rotate_index_updates.sh unsichtbar — in KNOWN_BLIND eintragen, wenn es eine "
            f"Erwähnung im Fließtext ist, sonst reparieren: {unexpected}"
        )


def test_the_named_blind_spots_still_exist():
    """Gegenprobe: eine Ausnahme ohne Text darf nicht still verschwinden.

    **Und die Grenze der Nadel, ausdrücklich:** sie identifiziert den Text **ab** dem Datum, nicht
    den Satz davor. Eine Änderung im Fließtext *vor* der Stelle wird deshalb nicht gemeldet — das ist
    keine Lücke im Wächter, sondern eine Eigenschaft einer Nadel: sie ist ein Fingerabdruck, kein
    vollständiger Kontext. Der Gegenlauf, der das beweisen sollte, hat zuerst genau den Text vor der
    Stelle geändert und war deshalb **grün** — die zweite Fassung ändert den Text, an dem die Nadel
    hängt, und meldet rot.
    """
    for rel, needles in KNOWN_BLIND.items():
        fm = frontmatter(REPO_ROOT / rel)
        assert fm is not None, f"{rel} hat kein Frontmatter mehr"
        for needle in needles:
            assert needle in fm, f"{rel}: die als Prosa benannte Stelle {needle!r} gibt es nicht mehr"


def test_the_p9_sessions_archive_carries_its_field_and_all_its_threads():
    """Der Regressionstest: das Feld ist wieder da, und die Kette ist vollständig sichtbar.

    Die 29 ist der gemessene Stand vom 2026-10-03 nach der Reparatur, nicht eine Wunschzahl. Als
    Untergrenze formuliert, damit der Test nicht an jedem neuen Rotations-Eintrag bricht — die
    Aussage, die er tragen soll, ist „kein Faden ist mehr blind", nicht „es sind genau 29".
    """
    fm = frontmatter(REPO_ROOT / "phase9_hardening" / "SESSIONS_ARCHIVE.md")
    assert fm is not None
    assert FIELD_RE.search(fm), "das `updated:`-Feld fehlt wieder (Regression vom 2026-10-02)"
    missing, prefixes, dots = chain_defects(fm)
    assert (missing, prefixes, dots) == (False, 0, 0)

    line = next(l for l in fm.splitlines() if l.startswith("updated: "))
    threads = SPLIT_ANCHOR_RE.split(line[len("updated: ") :])
    assert len(threads) >= 29, f"die Kette verliert Fäden: {len(threads)} < 29"
    assert all(t.startswith(tuple("0123456789")) for t in threads), "ein Thread beginnt nicht mit einem Datum"
