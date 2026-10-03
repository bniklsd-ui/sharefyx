"""Gate/Z (2026-10-03) — die Nachtrags-Rotation der INDEX-Karte, und was sie wieder verbietet.

`docs/INDEX.md` stand am 2026-10-03 bei 71.573 B, davon **37.391 B datierte Nachträge in 43 von
93 Einträgen**. Das ist die seit Wochen als ungeklärt geführte Überschreitung (P9-3/V145), und
sie ist am 2026-10-03 **gemessen** worden: die `updated:`-Kette der Karte hat 1.155 B und war
rotiert, und selbst ein Cap von 300 B je Eintragszeile hätte 39.971 B ergeben — das alte
Kriterium 38.912 B (P8.6 Plan 2 §1.2, für eine Datei mit weniger Zeilen gesetzt) war per
Kürzen **unerreichbar**. Nikinger-Entscheidung 2026-10-03: Nachträge ins L3-Archiv, Kriterium
auf den 40-KiB-Softcap neu baseliniert.

Diese Tests halten das Ergebnis fest und **die vier Grenzen, an denen der erste Entwurf des
Skripts gescheitert ist** — jede davon ist ein eingebauter Verstoß, kein Beispiel:

1. **Ein Schnitt mitten im Satz** — die Plausibilitätsprüfung bricht ab, wenn der Kopf nicht an
   einer Grenze endet. Der erste Lauf tat genau das und hätte den Satz `… (V145; **` verstümmelt.
2. **Das `**` am falschen Ort** — der Nachtrag-Anker muss ein vorangestelltes `**` *mitnehmen*,
   sonst bleibt die Auszeichnung im Kopf und der Archivabschnitt beginnt mit `**[`. Geprüft wird
   das am echten Skriptlauf, nicht an der Regex.
3. **Ein im INDEX vergessener Nachtrag** — die Byte-Buchhaltung allein kann das nicht sehen: ein
   zu früh geschnittener Rest ist ja im Archiv. Erst (d) unterscheidet Verschieben von Weglassen.
4. **Der Zeiger als Markdown-Link** — `doc_health._index_line_for()` erkennt eine Zeile an
   `](pfad)`, wertete den Zeiger `](INDEX_ENTRIES_ARCHIVE.md)` also als die INDEX-Zeile *des
   Archivs* und meldete für ein frisches Archiv `glyph='🔗'`. Ein Zeiger, der wie ein Eintrag
   aussieht, ist für einen Zeiger die falsche Form.

Dazu die beiden Eigenschaften, die den Zustand halten: **jeder Zeiger hat einen Abschnitt und
jeder Abschnitt einen Zeiger** (der einzige Weg, wie Chronik verloren geht, ist ein Zeiger ohne
Abschnitt), und die Karte bleibt unter dem neu baselinierten Kriterium.
"""
import re
import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "archive_index_entries.sh"
INDEX = REPO_ROOT / "docs" / "INDEX.md"
ARCHIVE = REPO_ROOT / "docs" / "INDEX_ENTRIES_ARCHIVE.md"
SOFTCAP_BYTES = 40 * 1024

POINTER = "**Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**"
SECTION_RE = re.compile(r"^## `([^`]+)`$", re.M)
ADDENDA_RE = re.compile(r"(?:\*\*)?\[(?:20\d\d-\d\d-\d\d)")


def _de(b: int) -> str:
    return f"{b:,}".replace(",", ".")


def _addenda_bytes(index_text: str) -> int:
    """Bytes der datierten Nachträge in den Kartenzeilen. Der erste Entwurf zählte nur physische
    Zeilen und kam auf 32.814 B statt 37.391 — fünf Einträge der Karte erstrecken sich über
    mehrere Zeilen, und ihre Nachträge waren damit teilweise unsichtbar. Der Unterschied ist
    4,5 KB und damit größer als das Toleranzfenster jedes Bandes."""
    total = 0
    for line in index_text.splitlines():
        if not line.startswith("- ["):
            continue
        m = ADDENDA_RE.search(line)
        if m:
            total += len(line[m.start():].encode("utf-8"))
    return total


def test_the_index_is_under_the_rebaselined_criterion():
    assert INDEX.stat().st_size <= SOFTCAP_BYTES, (
        f"docs/INDEX.md ist {_de(INDEX.stat().st_size)} B und damit über dem "
        f"{SOFTCAP_BYTES}-B-Softcap — die Nachträge gehören nach docs/INDEX_ENTRIES_ARCHIVE.md"
    )


def test_no_entry_line_carries_a_dated_addendum_any_more():
    """Gegenprobe (3). Der INDEX ist eine Stand-Karte: eine Zeile, die wieder mit `[2026-…`
    anfängt, ist eine Zeile, die wieder wächst."""
    offenders = [l[:80] for l in INDEX.read_text(encoding="utf-8").splitlines()
                 if l.startswith("- [") and ADDENDA_RE.search(l)]
    assert not offenders, f"{len(offenders)} Kartenzeile(n) mit datiertem Nachtrag: {offenders}"


def test_every_pointer_has_a_section_and_every_section_a_pointer():
    """Der einzige Weg, wie Chronik verloren geht, ist ein Zeiger ohne Abschnitt — und ein
    Abschnitt ohne Zeiger ist eine Tatsache, die niemand mehr findet."""
    index_text = INDEX.read_text(encoding="utf-8")
    pointers = index_text.count(POINTER)
    sections = SECTION_RE.findall(ARCHIVE.read_text(encoding="utf-8"))
    assert pointers == len(sections), (
        f"{pointers} Zeiger im INDEX, aber {len(sections)} Abschnitte im Archiv — "
        "die beiden Seiten müssen sich decken"
    )
    assert pointers > 40, "die Rotation hat die Nachträge nicht gefunden (erwartet > 40 Einträge)"


def _logical_entries(index_text: str) -> list[str]:
    """Ein Karten-Eintrag ist ein Bullet plus seine Folgezeilen. **Fünf Einträge der Karte
    erstrecken sich über mehrere physische Zeilen** — der `phase8_ui_graph`-Eintrag trägt seinen
    Zeiger deshalb auf der *letzten* Zeile. Die erste Fassung der Prüfung hat nur die erste
    physische Zeile gelesen und meldete für genau diesen Abschnitt „keine Kartenzeile", während
    die Kartenzeile direkt daneben stand."""
    out, cur = [], None
    for line in index_text.splitlines(keepends=True):
        if line.startswith("- ["):
            if cur is not None:
                out.append(cur)
            cur = line
        elif cur is not None and line.strip() and not line.startswith(("#", "|")):
            cur += line
        else:
            if cur is not None:
                out.append(cur); cur = None
    if cur is not None:
        out.append(cur)
    return out


def test_every_pointer_names_an_entry_that_exists():
    """Jeder Archivabschnitt trägt den **Linktext** der Kartenzeile, auf die er sich bezieht
    (`- [docs/INDEX.md](./INDEX.md)` → `docs/INDEX.md`). Geprüft wird deshalb gegen den Linktext
    und nicht gegen den Pfad: bei der Karte selbst zeigt der Link auf `./INDEX.md`, die
    Beschriftung aber auf `docs/INDEX.md`."""
    entries = _logical_entries(INDEX.read_text(encoding="utf-8"))
    for label in SECTION_RE.findall(ARCHIVE.read_text(encoding="utf-8")):
        assert any(f"[{label}]" in e for e in entries), (
            f"Archivabschnitt `{label}` hat keine Kartenzeile in docs/INDEX.md"
        )
        assert any(POINTER in e for e in entries if f"[{label}]" in e), (
            f"Archivabschnitt `{label}` hat keinen Zeiger in seiner Kartenzeile"
        )


def test_the_archive_sections_keep_their_dated_text_verbatim():
    """Der Zweck des Ganzen: der Nachtrag ist *datiert* und bleibt lesbar. Ein Abschnitt, der
    auf eine Sammelzeile eingedampft wurde, verliert genau das, wofür ein Archiv da ist."""
    for label, body in re.findall(r"^## `([^`]+)`\n\n(.*?)(?=^## `|\Z)", ARCHIVE.read_text(encoding="utf-8"), re.S | re.M):
        assert ADDENDA_RE.search(body), f"Abschnitt `{label}` enthält keinen datierten Nachtrag"


# ---------------------------------------------------------------- Skript-Gegenproben
def _sandbox(tmp_path: Path) -> Path:
    (tmp_path / "docs").mkdir(parents=True)
    shutil.copy(INDEX, tmp_path / "docs" / "INDEX.md")
    shutil.copy(ARCHIVE, tmp_path / "docs" / "INDEX_ENTRIES_ARCHIVE.md")
    return tmp_path


def _run(root: Path) -> subprocess.CompletedProcess:
    return subprocess.run([str(SCRIPT), str(root)], capture_output=True, text=True)


def test_a_second_run_is_a_noop_exit_2(tmp_path):
    """Nach der Rotation hat kein Eintrag mehr einen Nachtrag. Der zweite Lauf muss das *sagen*
    und nichts tun — ein Skript, das ein zweites Mal dieselben Nachträge anhängt, hat die erste
    Rotation nicht erkannt."""
    root = _sandbox(tmp_path)
    assert _run(root).returncode == 2, "erster Lauf sollte nichts zu tun haben (der INDEX ist bereits rotiert)"
    before = (root / "docs" / "INDEX.md").read_text(encoding="utf-8")
    again = _run(root)
    assert again.returncode == 2, again.stderr
    assert "Nichts zu tun" in again.stdout
    assert (root / "docs" / "INDEX.md").read_text(encoding="utf-8") == before
    assert SECTION_RE.findall((root / "docs" / "INDEX_ENTRIES_ARCHIVE.md").read_text(encoding="utf-8"))


def test_a_missing_archive_aborts_instead_of_being_created(tmp_path):
    """Das Skript legt das Archiv nicht an: eine L3-Datei mit L1-Card und INDEX-Zeile zu erzeugen
    ist eine Handarbeit, und ein Skript, das sie stillschweigend tut, macht die Karte unlesbar,
    weil `doc_health` dann keine Zeile findet."""
    root = _sandbox(tmp_path)
    (root / "docs" / "INDEX_ENTRIES_ARCHIVE.md").unlink()
    result = _run(root)
    assert result.returncode == 3
    assert "nicht angelegt" in result.stderr
    assert not (root / "docs" / "INDEX_ENTRIES_ARCHIVE.md").exists()


def test_a_roundtrip_restores_the_original_byte_for_byte(tmp_path):
    """Gegenproben (b) und (c) des Skripts, unabhängig nachgerechnet: nachträge aus dem Archiv in
    den INDEX zurück einsetzen, Zeiger entfernen — und es muss die Originaldatei sein. Ohne das
    ist „verbatim" nur eine Behauptung im Skriptkommentar."""
    root = _sandbox(tmp_path)
    original = (root / "docs" / "INDEX.md").read_text(encoding="utf-8")
    # Ein INDEX mit genau einem Nachtrag: minimal, aber mit allen drei Sonderfällen des Laufes
    # (Kopf mit Leerzeichen am Ende, `**` vor dem Datum, Ausgabe in zwei physischen Zeilen).
    original = original.replace(
        "- [README.md](../README.md) — 📗 ~7KB",
        "- [README.md](../README.md) — 📗 ~7KB · Einstieg.\n  Folgezeile mit Text. **[2026-01-01] ein Nachtrag",
    )
    (root / "docs" / "INDEX.md").write_text(original, encoding="utf-8")
    result = _run(root)
    assert result.returncode == 0, result.stderr

    new = (root / "docs" / "INDEX.md").read_text(encoding="utf-8")
    archive_before = ARCHIVE.read_text(encoding="utf-8")
    archive_after = (root / "docs" / "INDEX_ENTRIES_ARCHIVE.md").read_text(encoding="utf-8")
    sections = re.findall(r"^## `([^`]+)`\n\n(.*?)(?=^## `|\Z)", archive_after, re.S | re.M)
    # **Nur die Abschnitte dieses Laufs** sind neu — das Archiv hat vorher schon 43.
    touched = set(re.findall(r"^## `([^`]+)`\n", archive_after[len(archive_before):], re.M))
    assert sections, "der Lauf hat nichts verschoben"
    assert POINTER in new
    # Der Abschnitt, der zur README-Zeile gehört, muss genau ihr Nachtrag sein
    readme = dict(sections).get("README.md")
    assert readme is not None, f"Abschnittsüberschriften: {[s for s, _ in sections][:5]}"
    # **Der Abschnitt beginnt mit dem eingesetzten Nachtrag** — wie weit er reicht, haengt davon
    # ab, *wo* man den Nachtrag einfuegt, und der Test setzt ihn in den laufenden Text einer
    # Zeile, die schon einen Zeiger traegt. Genau das ist der Alltagsfall des naechsten Laufs und
    # der Grund fuer die Formulierung: der Skriptkopf nennt den doppelten Zeiger als bekannte
    # Kosmetik, weil die *Regel* jetzt lautet, dass Kartenzeilen keine Nachtraege mehr bekommen.
    assert readme.strip().startswith("**[2026-01-01] ein Nachtrag")

    # Rueckwaerts: **nach Etikett und nur fuer die Zeiger dieses Laufs** — genau so macht es das
    # Skript. Die erste Fassung des Tests ist den Zeigern nachgegangen und hat den Nachtrag in die
    # Zeile der *Karte selbst* gesetzt, weil deren Zeiger zuerst kommt; die Reihenfolge
    # nachzudenken ist derselbe Fehler, den auch das Skript einmal gemacht hat.
    bodies = {label: body for label, body in sections}
    rebuilt, current = [], None
    for line in new.splitlines(keepends=True):
        m = re.match(r"^- \[([^\]]+)\]", line)
        if m:
            current = m.group(1)
        if line.rstrip("\n").endswith(POINTER) and current in touched:
            rebuilt.append(line.rstrip("\n")[: -len(POINTER)] + bodies[current].rstrip("\n") + "\n")
        else:
            rebuilt.append(line)
    assert "".join(rebuilt) == original, "die Reassemblierung liefert nicht die Originaldatei"


def test_a_cut_in_the_middle_of_a_sentence_aborts_without_writing(tmp_path):
    """Gegenprobe (1). Der Anker wird absichtlich so verbogen, dass der Kopf mitten im Satz
    endet — und dann muss das Skript abbrechen, **ohne** eine der beiden Dateien angefasst zu
    haben. Ein Schnitt, der abbricht nachdem er geschrieben hat, ist schlimmer als einer, der
    falsch schneidet."""
    root = _sandbox(tmp_path)
    index = root / "docs" / "INDEX.md"
    text = index.read_text(encoding="utf-8")
    # "… Einstieg." -> Anker mitten im Wort: der Kopf endet auf "Einst"
    text = text.replace("- [README.md](../README.md) — 📗 ~7KB", "- [README.md](../README.md) — 📗 ~7KB **[2026-01-01] X")
    index.write_text(text, encoding="utf-8")
    before_index = index.read_text(encoding="utf-8")
    before_archive = (root / "docs" / "INDEX_ENTRIES_ARCHIVE.md").read_text(encoding="utf-8")
    result = _run(root)
    assert result.returncode == 1, result.stdout
    assert index.read_text(encoding="utf-8") == before_index
    assert (root / "docs" / "INDEX_ENTRIES_ARCHIVE.md").read_text(encoding="utf-8") == before_archive


def test_a_weakened_cut_anchor_is_caught_before_anything_is_written(tmp_path):
    """Die vierte Skript-Gegenprobe — **und die Korrektur meiner eigenen Behauptung darüber.**

    Ich hatte (d) „kein datierter Nachtrag bleibt im INDEX" als die Prüfung gepriesen, die einen
    vergessenen Nachtrag fängt. **Der Test zeigt: der geschwächte Anker wird zuerst von der
    Satzgrenzen-Prüfung gefangen**, weil der Kopf dann auf `**` endet — und (d) ist der
    *Rückfall*, der eingreift, wenn der Schnitt zu *spät* greift. Mit dem heutigen Anker (erster
    Treffer) ist dieser Fall nicht erzeugbar, ohne das Skript zu verändern. Das ist kein Grund,
    (d) zu streichen — es ist die Vorabversion desselben Satzes, den
    `test_no_entry_line_carries_a_dated_addendum_any_more` am echten Artefakt prüft, und es kostet
    eine Zeile. Aber es ist nicht die Prüfung, die den Fehler fängt, und das gehört in den
    Skriptkopf, nicht in eine Fußnote.

    Der Verstoß wird am **Anker** gebaut, nicht am Dokument: eine Skriptkopie verliert die
    `**`-Alternative, geschnitten wird also nur ein Nachtrag, der mit `[` beginnt.
    """
    root = _sandbox(tmp_path)
    index = root / "docs" / "INDEX.md"
    index.write_text(index.read_text(encoding="utf-8").replace(
        "- [README.md](../README.md) — 📗 ~7KB",
        "- [README.md](../README.md) — 📗 ~7KB · Einstieg. **[2026-01-01] ein Nachtrag",
    ), encoding="utf-8")
    before_index = index.read_text(encoding="utf-8")
    before_archive = (root / "docs" / "INDEX_ENTRIES_ARCHIVE.md").read_text(encoding="utf-8")

    weakened = root / "archive_geschwaecht.sh"
    source = SCRIPT.read_text(encoding="utf-8")
    assert source.count(r'(?:\*\*)?\[(?:20\d\d-\d\d-\d\d)') >= 1, "Ankerform geaendert?"
    weakened.write_text(source.replace(r'(?:\*\*)?\[', r"\["), encoding="utf-8")
    weakened.chmod(0o755)
    result = subprocess.run([str(weakened), str(root)], capture_output=True, text=True)
    assert result.returncode == 1, f"der geschwaechte Anker muss abbrechen, nicht durchlaufen: {result.stdout}"
    assert "Schnittpunkt ist vermutlich falsch" in result.stderr, result.stderr
    assert index.read_text(encoding="utf-8") == before_index, "der Abbruch hat die Karte doch angefasst"
    assert (root / "docs" / "INDEX_ENTRIES_ARCHIVE.md").read_text(encoding="utf-8") == before_archive

    # **Gegenprobe der Gegenprobe:** mit dem unveraenderten Anker muss dieselbe Eingabe durchlaufen.
    root2 = _sandbox(tmp_path / "b")
    index2 = root2 / "docs" / "INDEX.md"
    index2.write_text(before_index, encoding="utf-8")
    assert _run(root2).returncode == 0
    assert "[2026-01-01]" not in index2.read_text(encoding="utf-8"), "der Nachtrag steht noch in der Karte"
    assert "**[2026-01-01] ein Nachtrag" in (root2 / "docs" / "INDEX_ENTRIES_ARCHIVE.md").read_text(encoding="utf-8")
