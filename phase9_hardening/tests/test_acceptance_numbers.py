"""Gate/Z (2026-10-03) — die Zahlen der Abnahmematrix dürfen nicht still veralten.

Die Abnahmematrix ist das zentrale Artefakt des Gates: 82 Abnahmezeilen und 34 belegte
`[VERIFY]`-Einträge, jede mit Stand und Beleg. Ihre **Bilanz** stand am 2026-10-03 an **vier**
Stellen im Repo — in der Matrix selbst, in der Modulstatus-Zeile des Phase-Heads, in der
`updated:`-Kette des Heads und in der INDEX-Zeile der Matrix — und die vier Stellen nannten
**drei verschiedene Zahlen**. Eine davon war schlicht falsch: P9-3 und V145 nannten
`61.108 B` für `docs/INDEX.md`, real sind es 71.491 B. Ein Fehler von 8.249 B in einer
Zeile, die ausgerechnet die *Größe einer Datei* zum Gegenstand hat.

`doc_health.py` prüft die Bytezahl einer Datei gegen ihre **INDEX-Zeile** (`oversize`). Es
prüft nicht die Bytezahlen, die **innerhalb** der Matrix stehen. Diese Lücke ist die Ursache
des Fehlers, nicht die Sorgfalt des Schreibers.

Diese Tests schließen genau diese Lücke, in drei Regeln:

1. **EINE Quelle für die Bilanz.** Die Matrix besitzt die Zahl. Modulstatus und INDEX-Zeile
   dürfen sie nicht wiederholen, sonst ist die Kopie irgendwann die veraltete (das ist der
   Fund). Nicht die ganze Datei: die `updated:`-Kette ist ein datierter Session-Record.
2. **KEINE Gegenwartsform auf einer Zahl in einer Kette.** Ein datierter Faden darf seine
   Momentaufnahme nennen, aber nicht behaupten, sie sei „jetzt der Stand". Wortverbot auf
   `"jetzt"`, nicht auf die Zahl — sonst müsste man Historie löschen.
3. **Jede lebende Bytezahl wird nachgemessen** — und zwar **in der Zeile, die die Aussage
   macht**, nicht dateiweit.

Dazu zwei Wächter, die jeweils eine *gemessene Diagnose* festnageln, statt sie zu behaupten:
die Unerreichbarkeit des INDEX-Kriteriums und der Hebel, der den Phase-9-Head unter den
Softcap bringen soll. Beide sind am 2026-10-03 aus **falschen** Annahmen entstanden, und eine
falsche Annahme, die einmal im Repo steht, wird sonst zur Entscheidungsgrundlage.

**Warum die Zählregel für `[VERIFY]` hier steht und nicht nur in der Matrix:** V162 und V163
sind je zweimal vergeben (Lesart A/B), die Tabelle hat deshalb zwei Zeilen mehr als
Nummern. „Zählen" ist ohne die Regel mehrdeutig — und eine mehrdeutige Bilanz ist keine
Bilanz. Die Regel steht als eigene Test-Konstante, damit ein drittes Lesart-Muster das
Wort „A" nicht stillschweigend mitzählt.

**Kein Test prüft eine Zahl, die er sich aus dem subject bildet.** Die Erwartungen
(`ABNAHME_BILANCE`, `VERIFY_BILANCE`) sind abgetippt; die Tests rechnen sie nach — und
vergleichen sie mit dem, was im **Fließtext** der Matrix steht. Die erste Fassung prüfte nur
die Tabelle gegen die Konstante und war damit grün, während genau die Stelle veraltete, die am
schnellsten altert.
"""
import importlib.util
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

MATRIX = REPO_ROOT / "phase9_hardening" / "ABNAHME_MATRIX.md"
HEAD = REPO_ROOT / "phase9_hardening" / "CLAUDE.md"
INDEX = REPO_ROOT / "docs" / "INDEX.md"
# Die gestrichene Masse wird seit dem Split vom 2026-10-04 im **L3-Archiv** gemessen, nicht im
# Head: die durchgestrichenen Statusabsätze standen in den Statusspalten, und die sind gewandert.
STATUS_ARCHIVE = REPO_ROOT / "phase9_hardening" / "MODULE_STATUS_ARCHIVE.md"
INDEX_CRITERION_BYTES = 38912  # der P8.6-Plan-2-Wert, seit 2026-10-03 **ersetzt** (Nikinger-Entscheidung)
SOFTCAP_BYTES = 40 * 1024   # das Kriterium, das seit 2026-10-03 gilt — und das `doc_health` bereits prüft
SIZE_TOLERANCE_BYTES = 2048  # dasselbe absolute Band wie doc_health._named_size_is_current
CAP_BYTES = 300  # der Cap, mit dem P9-3/V145 die Unerreichbarkeit des Kriteriums belegen

# Abgetippt, nicht abgeleitet — der Test soll die Behauptung prüfen, nicht sie wiederholen.
# 2026-10-03: P9-15 von ⬜ auf ⚠️ (gemessen, aber in anderer Form als im Kriterium -- die
# dort genannte Referenz 372,9 ms ist im Code nie ueber Funnel gemessen worden).
# 2026-10-05: P9-27 von ⬜ auf ⚠️ (V188 beantwortet: es ist Betriebssystem-Verhalten, und die Seite
# kann es nicht verhindern -- die Zeile ist nicht erfuellt *worden*, sie ist gegenstandslos geworden;
# Nikinger-Entscheidung 2026-10-05: kein Code, D1 geschlossen). Die drei verbleibenden ⬜ sind
# P9-11 und P9-94 (beide `nmap` von aussen, Mini-Plan §5) und P9-13/V150 (zweites Konto).
# 2026-10-06: +9 Zeilen aus der **zweiten** Bildsichtung des Nikingers (Mini-Plan §11,
# Locks P9-AU–P9-AZ, Abnahme P9-103–P9-111). Alle neun ✅. Zwei davon tragen eine **benannte
# Grenze** im Text und bleiben deshalb ✅ mit Grenze statt ⚠️: P9-107 (die `<li>`-Mitgliederliste
# ist im Harness nicht darstellbar) und P9-110 (nur Deklaration, keine Wirkungsmessung). Beide
# Grenzen sind in der Zeile genannt — eine Abnahmezeile ohne ihre Grenze wäre die Behauptung,
# die §10.3 der Matrix für unzulässig hält.
# 2026-10-06, **dritte** Bildsichtung, zweiter Teil: die vier notierten Zeilen P9-112–P9-115 sind am
# selben Tag **abgelöst** — P9-112 durch seine eigene Widerrufung (der Nikinger schränkte den Auftrag
# auf „nur bei Spaces verwalten" ein), die anderen drei durch P9-116–P9-119, weil ihre Nummern
# inzwischen etwas anderes prüfen als am Vortag. **Die Zeilenzahl bleibt deshalb 116**, und die
# Zuordnung steht vollständig in der Matrix, damit keine Zeile stillschweigend verschwindet.
ABNAHME_BILANCE = {"✅": 101, "⚠️": 12, "⬜": 3}
# 2026-10-05: +7 Zeilen aus dem settings-Nachtrag P9-96–P9-102 (die sieben Punkte aus der
# Bildsichtung des Nikingers, §10 des Mini-Plans). Die zwei neuen ⚠️ sind **benannte
# Abweichungen**, keine offenen Punkte: P9-97 (linker Polsterwert, Nikinger-Entscheidung vom
# 2026-10-05) und P9-99 (`justify-content` statt des im Plan genannten und gemessen wirkungslosen
# `text-align` — der Knopf ist ein Flexcontainer).
ABNAHME_ROWS = 116  # 116 Abnahmezeilen; zuletzt P9-116–P9-119 (die dritte Bildsichtung, gebaut)
# 2026-10-03: V164 von ⬜ auf ✅ (Deploy `v3.1.1` + Health-Gate 9/9). Die Konstante steht
# **vor** dem Zählen, sonst wäre der Test eine Tautologie -- deshalb hat er mich beim
# Zurueckschreiben der Bilanz in die Matrix rot gemeldet, statt sie zu bestaetigen.
# 2026-10-03: V151 von ⚠️ auf ✅ (beide Beine gemessen, VPS-Anteil 2,4-3,6 %).
# 2026-10-05: V188 von ⬜ auf ✅ (vier Quellen, darunter MDN-`browser-compat-data` gemessen:
# `Keyboard.lock` ist `safari: false`). Es ist der letzte der drei ⬜ aus dem settings-Block;
# die zwei übrigen sind V150 und V162 *(Lesart A)*.
VERIFY_BILANCE = {"✅": 35, "⚠️": 1, "⬜": 2}  # Nummern-Lesart, eine Nummer = eine Zeile
VERIFY_ROWS = 41  # 38 Nummern + 2 Zweit-Lesarten + 1 reservierte Bereichszeile
# 2026-10-04 (Nikinger): P9-13/V150 (das zweite Claude-Konto) von ⚠️ auf ⬜ — **zurückgestellt, wandert
# nach P10, ist kein Blocker** (Plan §0.1a; die Regel steht auch in der Wurzel-`CLAUDE.md`
# §Working style). V157 ist damit der einzige verbleibende ⚠️, V150 und V162 *(Lesart A)* die beiden ⬜.
# **Woran man sieht, dass dieser Wächter zählt und nicht nachschlägt:** vor dem Zurückschreiben dieser
# beiden Konstanten meldete er rot und nannte die Differenz `{⚠️: 9} != {⚠️: 10}` — obwohl nirgends eine
# Zahl von Hand angefasst worden war. Genau das ist der Unterschied zwischen einer Maschine, die den
# Zustand prüft, und einer, die die Behauptung wiederholt.

# **2026-10-04, der Fund, der diese Konstante erzwang.** Die Zählregel („eine doppelt vergebene
# Nummer zählt einmal, mit ihrer Lesart A") wirkt den Marker der **zweiten Lesart weg** — und der
# landet damit in *keiner* Bilanz: nicht in der Überschrift, nicht in `VERIFY_BALANCE`, nirgends.
# Beim Schreiben von V162 *(Lesart B)* (⬜ → ⚠️, mit Doku-Zitat) blieb
# `test_the_verify_balance_is_the_machine_count_under_the_stated_rule` deshalb **grün**, obwohl
# sich der Zustand des Eintrags geändert hatte. Das ist die Repo-Lehre zum achten Mal: ein Wächter,
# der etwas anderes prüft als er behauptet — er behauptet „machine count", und Verwerfen ist auch
# ein Zählen.
#
# Die Arithmetik bleibt bei 34 (das ist die aussagekräftige Übergabezahl, sie steht im Fließtext der
# Matrix und in der Kopfzeile des Phase-Heads), aber **jede zweite Lesart wird hier namentlich
# festgenagelt**: sie kann ihren Marker nicht mehr stillschweigend wechseln, und eine **dritte**
# Lesart fällt als neuer Schlüssel auf, weil der Test die Menge vergleicht.
SECOND_READING_MARKERS = {"V162": "⚠️", "V163": "✅"}

MARKERS = ("✅", "⚠️", "⬜")
# Als Regex-Teile gebaut, damit dieses Modul die Wörter nicht selbst enthält, die es verbietet
# (dieselbe Falle wie der Step-D-Wächter am 2026-10-03, der wegen seines eigenen Docstrings rot war).
BALANCE_TRIPLE_RE = re.compile(r"\d+ ✅ · \d+ ⚠️ · \d+ ⬜")
PRESENT_TENSE_RE = re.compile(r"je" + r"tzt \d+ ✅ · \d+ ⚠️ · \d+ ⬜")

spec = importlib.util.spec_from_file_location("doc_health", REPO_ROOT / "scripts" / "doc_health.py")
doc_health = importlib.util.module_from_spec(spec)
sys.modules["doc_health"] = doc_health
spec.loader.exec_module(doc_health)


def _cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _abnahme_rows() -> list[list[str]]:
    return [_cells(l) for l in MATRIX.read_text(encoding="utf-8").splitlines() if l.startswith("| **P9-")]


def _verify_rows() -> list[list[str]]:
    text = MATRIX.read_text(encoding="utf-8").splitlines()
    start = next(i for i, l in enumerate(text) if l.startswith("## Stand je Eintrag"))
    return [_cells(l) for l in text[start:] if l.startswith("| V")]


def _row(prefix: str) -> str:
    """Die Tabellenzeile, die die Aussage macht — strukturell über ihre Nummer gefunden, damit
    der Test die Zahl nicht ein zweites Mal im Anker festschreibt."""
    lines = [l for l in MATRIX.read_text(encoding="utf-8").splitlines() if l.startswith(prefix)]
    assert len(lines) == 1, f"genau eine Zeile mit {prefix!r} erwartet, gefunden {len(lines)}"
    return lines[0]


def _stand_marker(stand: str) -> str | None:
    for m in MARKERS:
        if stand.startswith(m):
            return m
    return None


def _verify_number_key(id_cell: str) -> str:
    """`V162 *(Lesart A)*` und `V162 *(Lesart B)*` sind dieselbe Nummer — die Bilanz zählt sie
    einmal, mit Lesart A (die Reihenfolge im Text)."""
    return re.sub(r"\s*\*\(Lesart [AB]\)\*", "", id_cell)


def _measure_index() -> dict:
    """Die drei Zahlen, mit denen P9-3/V145 ihre Ursache belegen."""
    text = INDEX.read_text(encoding="utf-8")
    total = len(text.encode("utf-8"))
    chain = len(re.search(r"^updated: (.*)$", text, re.M).group(1).encode("utf-8"))
    addenda = 0
    for line in text.splitlines():
        if not line.startswith("- ["):
            continue
        m = re.search(r"\[20\d\d-\d\d-\d\d", line)
        if m:
            addenda += len(line[m.start():].encode("utf-8"))
    return {"total": total, "chain": chain, "addenda": addenda}


def _de(b: int) -> str:
    """Bytezahl in der Schreibweise des Repos: 69.357 B (Punkt als Tausendertrenner)."""
    return f"{b:,}".replace(",", ".")


def _byte_figures(text: str) -> list[int]:
    """Alle Bytezahlen im Text, mit und ohne Tausendertrenner (`69.357 B` **und** `229 B`).

    Bewusst als Kandidatenliste und nicht als Extraktion an einem Anker: der Anker wäre die
    zweite Kopie der Aussage, die der Test prüft. Die erste Fassung kannte nur die
    punktgeschriebene Form und war deshalb **blind für die 229 B gestrichene Masse** — ein
    Wächter, der die Zahl sucht, die er prüfen soll, aber nicht findet, meldet Grün.
    """
    return [
        int(m.group(1).replace(".", ""))
        for m in re.finditer(r"(\d{1,3}(?:\.\d{3})+|\d{1,5})\s*B", text)
    ]


def _has_figure_near(text: str, value: int, tolerance: float) -> bool:
    return any(abs(f - value) <= tolerance for f in _byte_figures(text))


def _headline_triple(text: str, anchor: str) -> dict[str, int]:
    """Die Bilanz, wie sie im Fließtext der Matrix steht — der Ort, der veraltet."""
    lines = [l for l in text.splitlines() if anchor in l]
    assert len(lines) == 1, f"genau eine Zeile mit {anchor!r} erwartet, gefunden {len(lines)}"
    m = re.search(r"(\d+) ✅ · (\d+) ⚠️ · (\d+) ⬜", lines[0])
    assert m is not None, f"keine Marker-Dreierfolge in der Zeile mit {anchor!r}: {lines[0][:120]!r}"
    return dict(zip(MARKERS, (int(m.group(1)), int(m.group(2)), int(m.group(3)))))


def test_the_abnahme_balance_is_the_machine_count_of_its_own_table():
    rows = _abnahme_rows()
    assert len(rows) == ABNAHME_ROWS, f"erwartet {ABNAHME_ROWS} Abnahmezeilen, gefunden {len(rows)}"
    counted: dict[str, int] = {m: 0 for m in MARKERS}
    for cells in rows:
        marker = _stand_marker(cells[2])
        assert marker is not None, f"{cells[0]}: Spalte `Stand` beginnt mit keinem Marker — {cells[2][:60]!r}"
        counted[marker] += 1
    assert counted == ABNAHME_BILANCE
    # Der Fließtext gegen dieselbe Zählung — die Hälfte, die ohne Test veraltet.
    assert _headline_triple(MATRIX.read_text(encoding="utf-8"), "Tabellenzeilen für") == counted


def test_the_verify_balance_is_the_machine_count_under_the_stated_rule():
    rows = _verify_rows()
    assert len(rows) == VERIFY_ROWS, f"erwartet {VERIFY_ROWS} [VERIFY]-Zeilen, gefunden {len(rows)}"
    counted: dict[str, int] = {m: 0 for m in MARKERS}
    reserved = 0
    seen: set[str] = set()
    second: dict[str, str] = {}
    for cells in rows:
        stand = cells[2]
        if stand.startswith("—"):
            reserved += 1
            continue
        marker = _stand_marker(stand)
        assert marker is not None, f"{cells[0]}: kein Marker in `Stand` — {stand[:60]!r}"
        key = _verify_number_key(cells[0])
        if key in seen:
            # Die zweite Lesart zählt **nicht** in die Bilanz — und genau deshalb wird ihr Marker
            # hier festgehalten, sonst wäre er durch keinen Wächter gedeckt (2026-10-04).
            second[key] = marker
            continue
        seen.add(key)
        counted[marker] += 1
    assert reserved == 1, f"genau eine reservierte Bereichszeile erwartet, gefunden {reserved}"
    assert counted == VERIFY_BILANCE
    assert second == SECOND_READING_MARKERS, (
        f"die Marker der zweiten Lesarten haben sich geändert: gemessen {second}, "
        f"festgenagelt {SECOND_READING_MARKERS}"
    )
    assert sum(counted.values()) == 38, (
        "38 belegte Einträge (2026-10-03: 34, seit dem settings-Block +4 für V185–V188). "
        "Die Übergabezahl 40 war der Nummernbereich, nicht die Zahl belegter Einträge."
    )
    assert _headline_triple(MATRIX.read_text(encoding="utf-8"), "belegte Einträge —") == counted


def test_only_the_matrix_carries_the_balance_not_the_head_and_not_the_index():
    """Regel 1: die Matrix besitzt die Zahl. Eine zweite Kopie ist irgendwann die falsche.

    Geprüft wird der **Modulstatus** des Heads, nicht die ganze Datei: die `updated:`-Kette ist
    ein datierter Session-Record und darf die Momentaufnahme ihres Tages nennen (dafür gibt es
    Regel 2). Der Modulstatus ist dagegen der *live* Status — dort ist eine Kopie eine Lüge mit
    Verzögerung, und genau so stand es hier: 65/10/8, während die Matrix 70/10/3 zählte.
    """
    modulstatus = HEAD.read_text(encoding="utf-8").split("## Modulstatus", 1)[1].split("\n## ", 1)[0]
    found = BALANCE_TRIPLE_RE.search(modulstatus)
    assert found is None, f"der Modulstatus zitiert eine Abnahmebilanz — {found.group(0)!r}"
    index_line = doc_health._index_line_for(INDEX.read_text(encoding="utf-8"), "phase9_hardening/ABNAHME_MATRIX.md")
    assert index_line is not None, "docs/INDEX.md hat keine Zeile für die Abnahmematrix"
    found = BALANCE_TRIPLE_RE.search(index_line)
    assert found is None, f"die INDEX-Zeile der Matrix zitiert eine Abnahmebilanz — {found.group(0)!r}"


def test_no_living_phase9_file_calls_a_dated_balance_the_present_one():
    """Regel 2: ein datierter Faden darf seine Momentaufnahme nennen, nicht behaupten, sie sei
    heute der Stand. Genau das stand am 2026-10-03 als „Matrix <Tagesbilanz>" in der Kette des
    Phase-9-Heads — zwei Tage nach dem Stand, den die Zahl nennt. Die verbotene Form steht hier
    bewusst **nicht** wörtlich: ein Wächter, der das Wort verbietet, darf es nicht selbst im
    Docstring tragen (dieselbe Falle wie der Step-D-Wächter vom 2026-10-03, der daran rot war).
    """
    for path in (HEAD, MATRIX):
        found = PRESENT_TENSE_RE.search(path.read_text(encoding="utf-8"))
        assert found is None, f"{path.name}: eine Bilanz in der Gegenwartsform — {found.group(0)!r}"


def test_the_live_byte_figures_in_the_matrix_are_the_real_sizes():
    """Regel 3: die lebenden Bytezahlen der Matrix werden nachgemessen, nicht geglaubt.
    `61.108 B` stand hier zwei Tage lang als „heute" und war um 8.249 B falsch.

    **Zeilenweise, nicht dateiweit:** der erste Entwurf suchte die Zahl in der ganzen Datei und
    war grün, obwohl die P9-3-Zeile falsch war — eine dritte, korrekte Nennung irgendwo genügte.
    Eine Zahl, die eine Zeile behauptet, wird in **ihrer** Zeile geprüft.

    **Warum ein Band und keine exakte Gleichheit:** die Matrix nennt die Größe einer Datei, in
    der die Zeile steht, die diese Zahl nennt. Jeder Edit dort verschiebt die Zahl — und
    `docs/INDEX.md` wird am Ende jeder Session angefasst. Exakte Gleichheit hieße eine
    Wartungsschleife: dieselbe Zahl gekoppelt an zwei Stellen. Das Band ist **±2 KB**, weil es
    das Band ist, an dem `doc_health._named_size_is_current` die INDEX-Zeile schon misst — die
    Matrix soll nicht strenger sein als die Regel, die ohnehin für dieselbe Zahl gilt. Der Fehler,
    um den es geht, lag bei 8.249 B und bleibt darin rot.
    """
    for prefix, path in (("| **P9-3**", INDEX), ("| V145 |", INDEX), ("| **P9-6**", REPO_ROOT / "ROADMAP.md")):
        size = path.stat().st_size
        assert _has_figure_near(_row(prefix), size, SIZE_TOLERANCE_BYTES), (
            f"die Zeile {prefix!r} nennt keine Bytezahl im ±{SIZE_TOLERANCE_BYTES}-B-Band zur heutigen "
            f"Größe von {path.name} ({_de(size)} B)"
        )
    # Der historische Vergleichswert darf stehen, aber nicht als heutiger.
    assert "38.822 B" in _row("| **P9-3**"), "der Vergleichswert vom Phasenstart (06ab4f6) ist weg — Kontext prüfen"

    # **Das ist der neu baselinerte Wert, und er ist zum ersten Mal eine Prüfung statt einer Angabe.**
    # Vorher stand hier `assert size > 38.912` — eine Prüfung, die nur *fehlschlagen* konnte, wenn
    # die Datei schrumpfte, und die seit dem 2026-10-03 ohnehin überholt war. Jetzt gilt die
    # Gegenrichtung: P9-3 und V145 stehen auf ✅, und ✅ ist nur wahr, wenn die Karte unter dem
    # Kriterium liegt. Wächst sie darüber, wird nicht die Zeile stillschweigend falsch, sondern
    # dieser Test rot.
    for prefix in ("| **P9-3**", "| V145 |"):
        assert _row(prefix).split("|")[3].strip().startswith("✅"), (
            f"{prefix} steht nicht auf ✅, obwohl die Karte jetzt unter dem Kriterium liegt — die "
            "Abnahmezeile und der Zustand muessen zusammenpassen"
        )
    assert INDEX.stat().st_size <= SOFTCAP_BYTES, (
        f"docs/INDEX.md ist auf {INDEX.stat().st_size} B gewachsen und damit über dem "
        f"{SOFTCAP_BYTES}-B-Softcap. P9-3/V145 stehen dann nicht mehr zu Recht auf ✅: die "
        "Nachtraege gehoeren nach docs/INDEX_ENTRIES_ARCHIVE.md (scripts/archive_index_entries.sh), "
        "nicht in die Kartenzeilen."
    )


def test_the_nightrags_stay_archived_and_the_row_keeps_its_derivation():
    """P9-3 ist am 2026-10-03 von ⚠️ auf ✅ gewandert, und damit stellt sich die Frage neu, was diese
    Zeile jetzt noch tragen muss.

    **Zwei Dinge, und sie werden verwechselt.** Der *Zustand* ist: die Nachträge sind archiviert,
    die Karte ist unter dem Kriterium. Die *Herleitung* — 37.391 B Nachträge in 43 von 93
    Einträgen, ein Cap von 300 B ergäbe 39.971 B, die Kette hat 1.155 B — ist die Begründung
    dafür, warum das Kriterium neu baseliniert und nicht gekürzt wurde. Sie gehört weiter in die
    Zeile, sonst ist das ✅ in fünf Jahren eine Behauptung. **Beide werden geprüft und sie sind
    verschiedene Prüfungen:** der Zustand am Zustand, die Herleitung an ihren Zahlen.

    Die Nachtragszahl wird **ohne Band** geprüft und **nicht** gegen die alte 37.391 B: die ist
    Geschichte. Geprüft wird, dass der Schwanz wieder klein ist — wächst er zurück auf ein Viertel
    der Datei, ist die Rotation entweder rückgängig gemacht oder umgangen worden.
    """
    m = _measure_index()
    assert m["addenda"] < m["total"] * 0.10, (
        f"die datierten Nachträge sind wieder {_de(m['addenda'])} B von {_de(m['total'])} B — die "
        "Nachtrags-Rotation wurde umgangen oder zurückgenommen"
    )
    assert m["chain"] < m["total"] / 2, "die Kette ist nicht mehr ein Bruchteil der Datei — die Diagnose ist zu neu"
    row = _row("| **P9-3**")
    for figure, what in ((37391, "der Nachtragsmasse von 2026-10-03"), (39971, "der Cap-Rechnung"),
                         (1155, "der `updated:`-Kette")):
        assert f"{_de(figure)} B" in row, (
            f"P9-3 nennt die Zahl für {what} ({_de(figure)} B) nicht mehr — ohne sie ist das ✅ eine "
            "Behauptung statt einer Herleitung"
        )
    assert "38.822 B" in row, "der Vergleichswert vom Phasenstart (06ab4f6) ist weg — Kontext prüfen"


def _figure_near_word(text: str, word: str, value: int, tolerance: float) -> bool:
    """Existiert **im Fenster um das Wort herum** eine Bytezahl mit passendem Wert?

    Die dritte Fassung derselben Prüfung. „Irgendwo im Text eine Zahl im Band" ist grün
    gelaufen, obwohl die Aussage falsch war (Gegenprobe G7) — eine Kandidatenliste findet immer
    eine passende Zahl, wenn das Dokument lang genug ist. Der Anker muss das **Wort** sein, das
    die Messung benennt, nicht eine beliebige Stelle im Satz. Fenster 120 Zeichen, symmetrisch.
    """
    for m in re.finditer(r"(\d{1,3}(?:\.\d{3})+|\d{1,5})\s*B", text):
        if abs(int(m.group(1).replace(".", "")) - value) > tolerance:
            continue
        for w in re.finditer(re.escape(word), text):
            if abs(m.start() - w.start()) <= 120:
                return True
    return False


def _struck_mass(path: Path) -> int:
    """Die Masse des durchgestrichenen Textes **in der ganzen Datei** — nicht nur in der
    Modulstatus-Tabelle, denn die Behauptung lautete „durchgestrichene Statusabsätze im
    Modulstatus", und eine Prüfung, die enger sucht als die Behauptung, prüft die Behauptung
    nicht."""
    return sum(
        len(m.group(0).encode("utf-8"))
        for m in re.finditer(r"~~.+?~~", path.read_text(encoding="utf-8"), re.S)
    )


def test_the_head_is_under_the_softcap_and_the_struck_mass_is_no_lever():
    """**Umgekehrt am 2026-10-04, und die Begründung steht hier, weil ein umgedrehter Wächter sonst
    zur Lüge wird.** (Muster wie beim doing-Wächter am 2026-10-02 und beim Step-F-Wächter: beide
    Richtungen mit Datum.)

    **Die Aussage am 2026-10-03** (dieses Modul, „der vierte Fund"): der Rest über dem Softcap seien
    die durchgestrichenen Statusabsätze im Modulstatus — genannt als **7.467 B** mit dem Zusatz,
    Streichen sei „die einzige Maßnahme, die den Head sicher unter dem Softcap brächte". Gemessen
    waren **189 B** in der ganzen Datei (heute 229 B), die tragende Masse war der *lebendige*
    Modulstatus. Geprüft wurde: (a) ein zu kleiner Hebel kann die Überschreitung nicht beseitigen,
    (b) die lebende Masse ist die tragende, (c) der neueste Session-Block nennt die gemessene
    Zahl, sonst liest der nächste Start wieder die alte.

    **Die Lage am 2026-10-04:** Nikinger entschied, die ausführlichen Statusspalten nach
    `MODULE_STATUS_ARCHIVE.md` zu ziehen (verbatim, Roundtrip-Gegenprobe). Der Head stand bei
    56.860 B und liegt jetzt **unter** dem 40-KiB-Softcap. Damit ist (a) **gegenstandslos** — es
    gibt keine Überschreitung, die ein Hebel beseitigen müsste — und (b) ist **falsch geworden**:
    der Modulstatus ist nicht mehr die tragende Masse, er ist der kleinste Teil des Heads.

    Also nicht die alten Zeilen löschen, sondern die Aussage drehen und **beide** herstellen:
    * **(1) Der neue Zustand, hart:** der Head liegt unter dem Softcap. Ohne Band, denn eine
      Überschreitung versteckt sich nicht „ein bisschen" — `doc_health` prüft dieselbe Größe
      zusätzlich gegen die `docs/INDEX.md`-Zeile.
    * **(2) Die alte Diagnose bleibt widerlegt, aber ohne Vakuum:** statt `struck < oversize` (bei
      negativem `oversize` wäre das `229 < −4.000`, also **immer** wahr und damit wertlos) gilt
      „die gestrichene Masse bleibt ein Bruchteil der Datei". In **beiden** Lagen wahr, in keiner
      vakuos.
    * **(3) Die tragende Masse ist Kurzstand plus L3-Archiv**, nicht eine breite Tabelle: geprüft
      in `test_table_shape.py :: test_every_status_cell_of_the_head_survives_verbatim_in_the_l3_archive`.
    * **(c) bleibt unverändert:** der neueste Session-Block nennt die gemessene Zahl am Wort
      „gestrichen".

    **Nicht gebaut:** ein Textverbot auf die alte, zu große Zahl — eine Korrektur muss sie nennen
    können, um zu sagen, was falsch war.
    """
    size = HEAD.stat().st_size
    assert size <= SOFTCAP_BYTES, (
        f"der Phase-9-Head steht bei {_de(size)} B, das sind {_de(size - SOFTCAP_BYTES)} B über dem "
        "40-KiB-Softcap — nach dem Split vom 2026-10-04 wäre das ein Rückschritt, kein Zustand"
    )
    # **Die gestrichene Masse wird im L3-Archiv gemessen, seitdem die Statusspalten dorthin
    # gewandert sind** — im Head sind es **0 B**, und eine Prüfung „0 B ist ein Bruchteil der
    # Datei" wäre die Formkorrektur eines Wächters ohne Aussage. Die Diagnose vom 2026-10-03
    # lautete über die Statusspalten, also wird sie dort gemessen, wo die jetzt stehen.
    struck = _struck_mass(STATUS_ARCHIVE)
    assert struck > 0, "im L3-Archiv ist keine gestrichene Masse mehr — die Widerlegung ist gegenstandslos"
    # Die erste Fassung verglich `struck < _struck_mass(ARCHIV) + size * 0.05` — also **gegen sich
    # selbst** plus 5 %: bei 229 B ist `229 < 229 + 1.559` immer wahr. Eine Prüfung, die
    # unveränderlich grün ist, ist die schlimmere Form von "kein Fund"; sie ist hier ersetzt durch
    # den Bruchteil an der Datei, die die Massen trägt.
    assert struck < STATUS_ARCHIVE.stat().st_size * 0.05, (
        f"die gestrichene Masse ({struck} B) ist ein nennenswerter Teil des Archivs "
        f"({_de(STATUS_ARCHIVE.stat().st_size)} B) — die Widerlegung vom 2026-10-03 (7.467 B "
        "behauptet, 189 B gemessen) gilt dann nicht mehr"
    )
    block = HEAD.read_text(encoding="utf-8").split("## Session stopped", 1)[1]
    assert _figure_near_word(block, "gestrichen", struck, max(struck * 0.10, 1)), (
        f"der neueste Session-Block nennt keine Bytezahl im Fenster um das Wort „gestrichen“ herum "
        f"für die gemessene Masse ({struck} B) — die Zahl muss an ihrem Wort stehen"
    )
