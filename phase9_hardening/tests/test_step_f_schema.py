"""Tests für Step F — Schema-Fundament `doing`/`assignee` (P9-Plan §8.5, neunte
P1-Contract-Öffnung P9-G).

Die neun Tests der Plan-Tabelle §8.5, in der Reihenfolge des Plans:

  1. test_task_accepts_the_doing_status                        (F1, P9-40)
  2. test_note_still_rejects_doing                             (F1, P9-41 — die Trennung ist der Punkt)
  3. test_assignee_round_trips_through_the_file                (F2/F6)
  4. test_empty_assignee_is_not_written_to_frontmatter         (F6, P9-42)
  5. test_assignee_survives_an_index_rebuild                   (F7/F9)
  6. test_index_schema_version_is_four                         (F8, statisch)
  7. test_old_index_is_discarded_and_rebuilt                   (F8, kein Migrationsskript)
  8. test_status_hint_lists_doing_without_being_edited         (P9-40)
  9. test_assignee_is_not_swallowed_by_extra                   (F4)

Dazu **fünf Tests für Stellen, die §8.2 nicht nennt und die der Plan für entbehrlich hielt** —
alle fünf sind beim Bauen am Code aufgefallen, jeder mit eigener Fehlerklasse:

 10. test_summary_carries_the_assignee                         (F10 — `_summary()`; ohne die
        Zeile wäre F3 ein totes Feld: `get()` wüsste den Wert, jede Liste nicht)
 11. test_update_stores_assignee_in_the_field_not_in_extra     (F11 — der `else`-Zweig von
        `Store.update()`; der Wert **würde** auch über `Item.extra` in die Datei gelangen,
        `item.assignee` bliebe aber auf "" und F6 (`if item.assignee`) feuerte nie)
 12. test_mcp_filetext_and_read_paths_carry_assignee            (§8.3, statisch + Verhalten:
        `item_to_filetext()` dupliziert die Feldreihenfolge von `_item_to_text` — ohne den
        Eintrag gäbe `return_body=True` etwas anderes zurück als geschrieben wurde)
 13. test_rest_whitelists_carry_assignee                       (§8.3, statisch: POST-Whitelist
        und `_PATCH_FIELDS`; ohne sie lehnt die API das Feld als "Unbekanntes Feld" ab)
 14. test_the_editor_status_dropdown_reads_the_vocabulary      (V159, statisch: `doing` erscheint
        im Editor-Dropdown, weil es `state.meta.status_values[itemType]` liest — gegen die
        Behauptung des Plans, **gemessen** am Aufrufer und nicht geglaubt)
 15. test_the_bucket_hole_for_doing_is_named_not_silently_fixed (Befund aus dem Bau, statisch:
        `_BUCKETS` kennt `doing` nicht — die Oberfläche ist P10, der Befund muss im Code stehen)

**V160 (2026-09-30, Nikinger): `assignee` ist ein Space-Name, ohne Validierung gegen die
Space-Liste.** Test 3/16 pinen das nicht semantisch, sondern am *Mechanismus*: es gibt
keinen Space-Auflösepfad im Schreibpfad (`_coerce_assignee` prüft nur den Typ, Plan §8.4).

Kein Netz, kein echter DATA_ROOT, kein Dienst, kein LLM. Alle Stores auf `tmp_path`, `git=False`.
"""

from __future__ import annotations

import re
import sqlite3
from pathlib import Path

import pytest

from storage.errors import ValidationError
from storage.models import STATUS_VALUES, Item, ItemSummary
from storage.store import Store

REPO_ROOT = Path(__file__).resolve().parents[2]
INDEX_PY = REPO_ROOT / "phase1_storage" / "storage" / "index.py"
TOOLS_PY = REPO_ROOT / "phase2_mcp" / "mcpserver" / "tools.py"
API_PY = REPO_ROOT / "phase5_ui" / "webui" / "api.py"
EDITOR_JS = REPO_ROOT / "phase5_ui" / "webui" / "static" / "js" / "editor.js"
SERIALIZERS_PY = REPO_ROOT / "phase5_ui" / "webui" / "serializers.py"


@pytest.fixture
def store(tmp_path) -> Store:
    return Store(tmp_path, git=False)


def _path_of(data_root: Path, item_id: str) -> Path:
    """Der Pfad der Item-Datei. Bewusst **gesucht**, nicht gerechnet: `files.py` haengt einen
    Title-Slug an den Dateinamen (`itm_x__t.md`), und der Slug aendert sich mit dem Titel —
    ein Test, der den Pfad einmal zu Beginn festhaelt, laeuft nach dem ersten `update()` in
    einen `FileNotFoundError` und behauptet dann einen Fehler, den es nicht gibt."""
    for candidate in data_root.rglob("*.md"):
        if f"id: {item_id}\n" in candidate.read_text(encoding="utf-8"):
            return candidate
    raise AssertionError(f"keine Item-Datei fuer {item_id} unter {data_root}")


# -- 1./2.  F1: das Statusvokabular ---------------------------------------------------------


def test_task_accepts_the_doing_status(store):
    item = store.create("sp", type="task", title="Angebot schreiben", status="doing")
    assert item.status == "doing"
    assert store.get(item.id).status == "doing"


def test_note_still_rejects_doing(store):
    """`note` bleibt `{active, archived}` (P9-H). Die Trennung ist der Punkt des Feldes: ein
    `doing` auf einer Notiz ist ein Tippfehler, kein Feature — und genau deshalb gehoert der Wert
    in den Kern statt in einen Tag."""
    assert STATUS_VALUES["note"] == frozenset({"active", "archived"})
    with pytest.raises(ValidationError) as exc:
        store.create("sp", type="note", title="Notiz", status="doing")
    assert "doing" in str(exc.value)


# -- 3./4.  F2/F6: der Round-Trip über die Datei -------------------------------------------


def test_assignee_round_trips_through_the_file(store, tmp_path):
    created = store.create("sp", type="task", title="Angebot", assignee="privat-nikinger")
    # Datei-Inhalt, nicht nur das Objekt: der Kern ist die Datei (Hard Rule 2), ein Round-Trip
    # ueber ein Python-Objekt beweist nichts.
    text = _path_of(tmp_path, created.id).read_text(encoding="utf-8")
    assert "assignee: privat-nikinger" in text
    # ... und ueber ein frisches Store-Objekt, also ueber die Datei neu eingelesen.
    reopened = Store(tmp_path, git=False)
    assert reopened.get(created.id).assignee == "privat-nikinger"


def test_empty_assignee_is_not_written_to_frontmatter(store, tmp_path):
    """F6/P9-42. Ein Item **ohne** `assignee` (jeder Altbestand-Item) darf bei einem beliebigen
    Write kein stilles `assignee: ""` bekommen — das waere ein Frontmatter-Diff in jedem
    Altbestand-Item, den niemand bestellt hat."""
    created = store.create("sp", type="task", title="Ohne Assignee")
    path = _path_of(tmp_path, created.id)
    assert "assignee" not in path.read_text(encoding="utf-8")

    # Der Altbestand-Item wird jetzt von aussen angefasst (Fremd-Edit, der haeufigste Fall) …
    current = store.get(created.id)
    store.update(created.id, version=current.version, title="Ohne Assignee, umbenannt")
    # … und der Wert bleibt "" und unsichtbar, auch nach einem zweiten Read aus der Datei.
    assert "assignee" not in _path_of(tmp_path, created.id).read_text(encoding="utf-8")
    assert Store(tmp_path, git=False).get(created.id).assignee == ""


# -- 5./6./7.  F7/F8/F9: der Index ------------------------------------------------------------


def test_assignee_survives_an_index_rebuild(store, tmp_path):
    created = store.create("sp", type="task", title="Mit Assignee", assignee="sp")
    store.rebuild_index()
    conn = sqlite3.connect(tmp_path / ".index.sqlite3")
    try:
        assert conn.execute("SELECT assignee FROM items WHERE id = ?", (created.id,)).fetchone() == (
            "sp",
        )
    finally:
        conn.close()
    # ... und der Neuaufbau darf den Wert am Item nicht zerstoeren.
    assert store.get(created.id).assignee == "sp"


def test_index_schema_version_is_four():
    """F8, statisch. `INDEX_SCHEMA_VERSION = 4` ist keine Kosmetik: `connect()` verwirft einen
    Index mit abweichender `user_version` (P9-Plan §8.2). Ein stehengebliebenes 3 hiesse: der
    deployed `assignee`-Wert landet in einer Tabelle, die es gar nicht gibt."""
    source = INDEX_PY.read_text(encoding="utf-8")
    match = re.search(r"^INDEX_SCHEMA_VERSION = (\d+)$", source, re.MULTILINE)
    assert match, "INDEX_SCHEMA_VERSION nicht gefunden"
    assert match.group(1) == "4"


def test_old_index_is_discarded_and_rebuilt(store, tmp_path):
    """F8 in Aktion: ein Index mit `user_version=3` wird **verworfen und leer neu angelegt**,
    nicht migriert. Wer hier ein `ALTER TABLE` baut, hat Hard Rule 2 missverstanden."""
    created = store.create("sp", type="task", title="Bleibt", assignee="sp")
    conn = sqlite3.connect(tmp_path / ".index.sqlite3")
    conn.execute("PRAGMA user_version = 3")
    conn.commit()
    conn.close()

    fresh = Store(tmp_path, git=False)          # loest den Verwerf + rebuild aus
    assert fresh.get(created.id).assignee == "sp"
    conn = sqlite3.connect(tmp_path / ".index.sqlite3")
    try:
        assert conn.execute("PRAGMA user_version").fetchone()[0] == 4
        assert conn.execute("SELECT COUNT(*) FROM items").fetchone()[0] == 1
    finally:
        conn.close()


# -- 8.  P9-40: das Vokabular erreicht MCP, ohne dass eine Zeile in tools.py es abtippt --------


def test_status_hint_lists_doing_without_being_edited():
    """`_status_hint()` generiert aus `STATUS_VALUES` (P6.5-C) — genau dieser Umweg ist der
    Grund fuer F1 im Kern statt fuer eine Liste in `tools.py`. Der Test vergleicht den
    generierten Text gegen das echte Vokabular; er **behauptet nicht**, dass `tools.py` unveraendert
    ist (der MCP-Teil von §8.3 aendert es sehr wohl) — er behauptet, dass dort kein
    Statuswort steht."""
    from mcpserver.tools import _status_hint

    hint = _status_hint()
    for item_type, values in STATUS_VALUES.items():
        assert f"{item_type}: {'|'.join(sorted(values))}" in hint
    assert "doing" in hint.split("task: ")[1].split(" ")[0]
    # Kein abgetipptes Vokabular: die drei Werte tauchen nicht als eigene Wortliste im Modul auf.
    module_source = TOOLS_PY.read_text(encoding="utf-8")
    assert not re.search(r"['\"](open|doing|done)['\"]\s*[|,]\s*['\"]", module_source), (
        "tools.py enthaelt ein abgetipptes Statusvokabular — das ist genau die Drift, die "
        "_status_hint() ausloesen sollte"
    )


# -- 9./10./11.  F4, F10, F11: wo der Wert nicht verloren gehen darf ---------------------------


def test_assignee_is_not_swallowed_by_extra(store, tmp_path):
    """F4. Ohne `"assignee"` in `_KNOWN_FIELDS` landet der Wert in `Item.extra` — der
    Round-Trip funktionierte dann zwar, aber das Feld haette weder Default noch Index-Spalte
    und waere ein unbekannter Schluessel. Der Test vergleicht beide Orte."""
    created = store.create("sp", type="task", title="Feld", assignee="sp")
    item = store.get(created.id)
    assert item.assignee == "sp"
    assert "assignee" not in item.extra


def test_summary_carries_the_assignee(store):
    """F10 — **nicht in §8.2 genannt.** `_summary()` ist die einzige Stelle, die eine
    Trefferzeile baut. Ohne die Durchreicherung stuende in `search()` dauerhaft `""`, waehrend
    `get()` den echten Wert liefert: zwei Flächen, zwei Wahrheiten, ohne Fehler."""
    created = store.create("sp", type="task", title="Treffer", assignee="sp")
    hit = next(i for i in store.search(space="sp").items if i.id == created.id)
    assert isinstance(hit, ItemSummary)
    assert hit.assignee == "sp"


def test_update_stores_assignee_in_the_field_not_in_extra(store):
    """F11 — **nicht in §8.2 genannt, und der am leichtesten übersehene.** `assignee` steht nicht
    in `known_updatable`, also waere es im `else`-Zweig gelandet: der Wert ginge ueber
    `fields.update(item.extra)` trotzdem in die Datei (ein blinder Punkt — "es funktioniert" ist
    hier kein Beweis), `item.assignee` bliebe aber auf "". F6 (`if item.assignee`) feuerte dann
    nie mehr, und `update(assignee="")` koennte ein gesetztes Feld nicht mehr leeren."""
    created = store.create("sp", type="task", title="Wird umgehaengt", assignee="alt")
    updated = store.update(created.id, version=1, assignee="neu")
    assert updated.assignee == "neu"
    assert "assignee" not in updated.extra

    # Und das Leeren muss funktionieren (der Agent loest eine Aufgabe so).
    cleared = store.update(created.id, version=updated.version, assignee="")
    assert cleared.assignee == ""
    assert store.get(created.id).assignee == ""


# -- 12./13.  §8.3: die Schichten ueber dem Kern -------------------------------------------


def test_mcp_filetext_and_read_paths_carry_assignee(store):
    """`item_to_filetext()` dupliziert **bewusst** die Feldreihenfolge von `_item_to_text`
    (Modul-Docstring). Ohne den Eintrag gäbe `create_item(assignee=…, return_body=True)` einen
    Dateitext zurueck, der das Feld nicht traegt, waehrend die Datei es hat."""
    from mcpserver.tools import item_to_filetext, summary_to_dict

    created = store.create("sp", type="task", title="Filetext", assignee="sp")
    assert "assignee: sp" in item_to_filetext(created)
    assert "assignee" not in item_to_filetext(store.create("sp", type="task", title="Leer"))

    hit = next(i for i in store.search(space="sp").items if i.id == created.id)
    assert summary_to_dict(hit, own=True)["assignee"] == "sp"

    # `get_item` und die Trefferliste muessen dasselbe sagen — ein Agent haelt die beiden
    # Seiten sonst nicht gegeneinander.
    get_item_source = TOOLS_PY.read_text(encoding="utf-8").split('"visibility": item.visibility,')[1]
    assert '"assignee": item.assignee' in get_item_source.split("compact_json(payload)")[0]


def test_rest_whitelists_carry_assignee():
    """§8.3: `POST /api/v1/items` filtert ueber eine Feld-Whitelist, `PATCH` ueber
    `_PATCH_FIELDS`. Fehlt `assignee` in einer von beiden, antwortet die API
    `validation_failed` — das Feld waere ueber REST unschreibbar, obwohl der Kern es kann."""
    source = API_PY.read_text(encoding="utf-8")
    post_whitelist = re.search(
        r'if key in \{([^}]*)\}\n\s*\}', source.split("async def _items_post")[1]
    )
    assert post_whitelist, "POST-Whitelist nicht gefunden"
    assert '"assignee"' in post_whitelist.group(1)

    patch_fields = re.search(r"_PATCH_FIELDS = frozenset\(\{(.*?)\}\)", source, re.DOTALL)
    assert patch_fields, "_PATCH_FIELDS nicht gefunden"
    assert '"assignee"' in patch_fields.group(1)

    # Und beide Serialisierungen, sonst landet der Wert in keiner Antwort.
    serializers = SERIALIZERS_PY.read_text(encoding="utf-8")
    assert '"assignee": item.assignee' in serializers
    assert '"assignee": s.assignee' in serializers


# -- 14.  V159: `doing` im Editor-Dropdown, ohne JS-Aenderung ---------------------------------


def test_the_editor_status_dropdown_reads_the_vocabulary():
    """[VERIFY] V159, **gemessen am Aufrufer statt geglaubt**. Plan §8.3 behauptet, `dialogs.js`
    lese die Statuswerte bereits und `doing` erscheine ohne Codeaenderung. Gemessen ist: das
    gilt fuer `editor.js :: populateStatusSelect()` (liest `state.meta.status_values[itemType]`
    und rendert **rohe Werte**), fuer `dialogs.js:323` aber nur halb — dort iteriert es
    `Object.keys(state.meta.status_values)`, also das **Typ**-Vokabular, und der Anlegen-Dialog
    hat ueberhaupt keinen Status-Knopf (`createStatus` existiert nicht). Die Behauptung ist also
    fuer den Editor richtig und fuer den Dialog gegenstandslos."""
    source = EDITOR_JS.read_text(encoding="utf-8")
    assert "state.meta.status_values[itemType]" in source
    # Der Wert kommt unuebersetzt in die Option — deshalb genuegt der Kern-Eintrag.
    assert re.search(r"opt\.textContent = s;", source)
    assert not re.search(r"assignee|doing", source), (
        "editor.js nennt Step-F-Vokabular — dann waere der Test hier keine Wache mehr, sondern "
        "eine zweite Quelle (genau das, was die Konvention verbietet)"
    )


# -- 15.  Der Befund, den Step F nicht fixt --------------------------------------------------


def test_the_bucket_hole_for_doing_is_named_not_silently_fixed():
    """`_BUCKETS` (`api.py`) kennt `doing` nicht, und das ist **eine bewusste Unterlassung**,
    keine Vollständigkeit. `bucketFor()` (`list.js`) vergleicht `f.status === item.status`
    exakt und liefert fuer eine `doing`-Aufgabe `null`; beide Aufrufer fallen auf
    `|| state.filter` zurueck. Warum trotzdem nicht hier gefixt: ein fuenfter `_BUCKETS`-Eintrag
    erzeugt ueber `bucketNames() = Object.keys(state.meta.buckets)` einen **fuenften Rail-Eintrag**
    (`tree.js:72`) mit unuebersetztem Label — das ist die Hervorhebung, die P9-P P10 zuteilt.
    Dieser Test pinnt den Befund **im Code**: faellt er irgendwann weg, ohne dass P10 es behoben
    hat, ist das ein Fehler."""
    source = API_PY.read_text(encoding="utf-8")
    buckets = re.search(r"_BUCKETS: dict\[str, dict\[str, str\]\] = \{(.*?)\n\}", source, re.DOTALL)
    assert buckets, "_BUCKETS nicht gefunden"
    assert '"doing"' not in buckets.group(1)
    assert "P9 Step F" in source.split("_BUCKETS:")[0], "der Befund-Geheimvermerk fehlt"


# -- V160: die Entscheidung, die die Tests 3/4/16 mechanisch tragen -------------------------


def test_assignee_is_coerced_but_never_resolved_to_a_space(store):
    """V160: Space-Name, **ohne** Validierung. Der Test pinnt die Mechanik, nicht die Semantik:
    `_coerce_assignee` prueft den Typ (nicht den Inhalt) — und im Schreibpfad gibt es keinen
    Space-Aufloeser. Ein `assignee="gibt-es-nicht"` ist deshalb gueltig und wird geschrieben;
    genau das ist die Entscheidung, keine Versehenheit (Plan §8.4: eine Pruefung gegen die
    Space-Liste waere eine zweite, nicht angekuendigte Contract-Oeffnung)."""
    created = store.create("sp", type="task", title="Fremder Name", assignee="gibt-es-nicht")
    assert store.get(created.id).assignee == "gibt-es-nicht"
    # Whitespace wird getrimmt, damit "  " nicht als gesetzter Wert durchgeht.
    assert store.create("sp", type="task", title="Leer", assignee="   ").assignee == ""
    with pytest.raises(ValidationError) as exc:
        store.create("sp", type="task", title="Zahl", assignee=42)
    assert "assignee" in str(exc.value)


def test_the_dataclass_defaults_are_backwards_compatible():
    """Beide Dataclasses sind `kw_only` mit Default — ein Item ohne `assignee` (jeder
    Altbestand, jedes Test-Fixture im Repo) konstruiert weiterhin ohne Argument. Ohne Default
    waere das eine Reparaturrunde durch jedes einzelne `Item(...)` im Repo."""
    assert Item(id="i", space="s", type="task", title="t", status="open",
                created=None, updated=None, version=1).assignee == ""
    assert ItemSummary(id="i", space="s", type="task", title="t", status="open",
                       created=None, updated=None, version=1, snippet="").assignee == ""
