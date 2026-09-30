"""Tests für Step G — Löschen (F2) nach `._trash/` (P9-Plan §9.4, P9-45 – P9-52).

Die sieben Tests der Plan-Tabelle §9.4, in der Reihenfolge des Plans:

  1. test_trash_moves_the_file_and_keeps_the_bytes          (P9-47)
  2. test_trash_requires_the_current_version                (Hard Rule 3)
  3. test_trashed_item_disappears_from_list_and_search       (P9-49)
  4. test_trash_creates_a_git_commit                         (P9-48, Hard Rule 5)
  5. test_trash_refuses_a_foreign_item                       (P9-51/P9-K)
  6. test_no_mcp_tool_exposes_trash                          (P9-K, statisch)
  7. test_delete_dialog_requires_the_exact_title            (P9-46, statisch)

Dazu **fünf Tests, die §9.4 nicht nennt** — jeder gegen eine Fehlerklasse, die beim Bauen am
Code sichtbar war:

  8. test_trashed_item_stays_gone_after_a_rebuild             **der wichtigste.** Die Unsichtbarkeit
     ist nicht die des Löschens, sondern die des Ortes: `rebuild_index()` ist der Moment, in dem ein
     Item an einem unbekannten Ort **wieder auftauchen** kann. Die Plan-Variante `<space>/_trash/`
     tat genau das (gemessen, siehe `phase9_hardening/CLAUDE.md`s Block und `store.TRASH_DIR`) — und
     machte `_trash` sogar zu einem Phantom-Space in `list_spaces()`. Ein Test wie 3 allein hätte
     diesen Fehler **durchgelassen**.
  9. test_trash_dir_is_never_scanned_as_a_space              derselbe Fund, zweite Hälfte: `list_spaces()`
     führt jedes Nicht-Punkt-Verzeichnis unter `DATA_ROOT` als Space.
 10. test_incoming_links_of_a_trashed_item_stop_being_a_graph_edge   P9-49 nennt die **Karte**,
     und `index.delete_item()` räumt nur ausgehende Kanten. Die eingehenden bleiben dangling stehen
     und müssen von `_graph_get` weggefiltert werden (beide Endpunkte müssen in der sichtbaren
     Knotenmenge sein). Ohne `index.delete_item()` bliebe die Datei liegen **und** der Index führte
     sie weiter — der Test deckt beide Hälften ab.
 11. test_trash_does_not_touch_a_neighbouring_item           Zwei Items, ein Move: der Nachbar muss
     unangetastet bleiben (Pfad, Bytes, Version).
 12. test_the_rest_api_has_no_route_that_lists_the_trash     P9-J: „kein API-Endpunkt, der
     `_trash/` listet". Statisch über die Routenliste — ein Weg, wie die Unsichtbarkeit wieder
     kaputt werden könnte, ohne dass jemand es bemerkt.

Kein Netz, kein echter DATA_ROOT, kein Dienst, kein LLM. Stores auf `tmp_path`.

**Zu 4 (Git-Commit):** `Store` wird mit `git=True` nur dort benutzt, wo der Commit geprüft
werden soll; die übrigen Tests laufen mit `git=False` wie der Rest des Repos. Geprüft wird die
Commit-**Existenz und -Message** über `git log`, nicht über einen Spy auf `_commit()` — der
Spy bewiese, dass die Methode gerufen wurde, nicht dass ein Commit entstanden ist.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest

from storage.errors import ConflictError, ItemNotFound
from storage.store import TRASH_DIR, Store

REPO_ROOT = Path(__file__).resolve().parents[2]
TOOLS_PY = REPO_ROOT / "phase2_mcp" / "mcpserver" / "tools.py"
API_PY = REPO_ROOT / "phase5_ui" / "webui" / "api.py"
DIALOGS_JS = REPO_ROOT / "phase5_ui" / "webui" / "static" / "js" / "dialogs.js"


@pytest.fixture
def store(tmp_path) -> Store:
    return Store(tmp_path, git=False)


def _trashed(data_root: Path) -> list[Path]:
    return sorted((data_root / TRASH_DIR).rglob("*.md"))


# -- 1.  P9-47: verschieben, bytes unangetastet --------------------------------------------


def test_trash_moves_the_file_and_keeps_the_bytes(store, tmp_path):
    item = store.create("sp", type="task", title="Weg damit", body="Inhalt mit Umlauten: äöü.")
    quelle = tmp_path / "sp" / f"{item.id}__weg-damit.md"
    vorher = quelle.read_bytes()

    store.trash(item.id, version=item.version)

    assert not quelle.exists(), "die Datei liegt noch an ihrem alten Ort"
    ziele = _trashed(tmp_path)
    assert [p.relative_to(tmp_path).as_posix() for p in ziele] == [
        f"{TRASH_DIR}/sp/{item.id}__weg-damit.md"
    ]
    assert ziele[0].read_bytes() == vorher, "es ist ein Move, kein Rewrite"


# -- 2.  Hard Rule 3: `version` ist Pflicht -------------------------------------------------


def test_trash_requires_the_current_version(store):
    item = store.create("sp", type="task", title="Konkurrenz")
    with pytest.raises(ConflictError) as exc:
        store.trash(item.id, version=item.version + 1)
    # Und der Fehler nennt die **aktuelle** Fassung — derselbe Vertrag wie bei jedem anderen
    # Write, damit der Aufrufer den Konflikt auflösen kann statt zu raten.
    assert exc.value.current.version == item.version
    # Nichts passiert: nach dem Conflict steht das Item noch da.
    assert store.get(item.id).id == item.id


# -- 3./8./9.  P9-49: unsichtbar, und zwar dauerhaft ---------------------------------------


def test_trashed_item_disappears_from_list_and_search(store):
    item = store.create("sp", type="task", title="Weg damit")
    store.trash(item.id, version=item.version)
    assert store.search(space="sp").total == 0
    with pytest.raises(ItemNotFound):
        store.get(item.id)
    with pytest.raises(ItemNotFound):
        store.acl_of(item.id)


def test_trashed_item_stays_gone_after_a_rebuild(store, tmp_path):
    """**Der Test, den die Plan-Liste nicht hat.** `rebuild_index()` ist der Moment, in dem ein
    Item an einem unbekannten Ort zurückkommt: es liest `space_dir.rglob("*.md")` **ohne** Skip,
    und ein Item unter `._trash/` liegt außerhalb jedes `space_dir` — genau deshalb ist der
    Punkt-Praefix hier die halbe Funktion. Die Plan-Variante `<space>/_trash/` lag innerhalb
    des Spaces und wurde wieder einsortiert (`folder="_trash"`); sie ist in
    `store.TRASH_DIR` dokumentiert und war der Grund für die Nikinger-Entscheidung vom
    2026-09-30."""
    behalten = store.create("sp", type="task", title="Bleibt")
    weg = store.create("sp", type="task", title="Weg")
    store.trash(weg.id, version=weg.version)

    store.rebuild_index()

    assert [i.title for i in store.search(space="sp").items] == ["Bleibt"]
    with pytest.raises(ItemNotFound):
        store.get(weg.id)
    # Und der Index führt es wirklich nicht mehr, nicht nur die Suche.
    import sqlite3

    conn = sqlite3.connect(tmp_path / ".index.sqlite3")
    try:
        assert conn.execute(
            "SELECT COUNT(*) FROM items WHERE id = ?", (weg.id,)
        ).fetchone()[0] == 0
        assert conn.execute(
            "SELECT COUNT(*) FROM item_links WHERE src_id = ? OR dst_id = ?", (weg.id, weg.id)
        ).fetchone()[0] == 0, "ausgehende Kanten müssen mitgeräumt sein"
    finally:
        conn.close()
    assert behalten.id in {i.id for i in store.search(space="sp").items}


def test_trash_dir_is_never_scanned_as_a_space(store):
    """`list_spaces()` führt jedes Nicht-Punkt-Verzeichnis unter `DATA_ROOT` als Space — mit
    `_trash` wäre beim Löschen eines Items ein **Phantom-Space** entstanden, sichtbar im Rail."""
    store.trash(store.create("sp", type="task", title="Weg").id, version=1)
    assert [s.name for s in store.list_spaces()] == ["sp"]
    assert store.list_spaces()[0].folders == ()


# -- 4.  P9-48: Git-Commit (Hard Rule 5) -----------------------------------------------------


def test_trash_creates_a_git_commit(tmp_path):
    store = Store(tmp_path, git=True)
    item = store.create("sp", type="task", title="Weg damit")
    store.trash(item.id, version=item.version)

    log = subprocess.run(
        ["git", "log", "--format=%s"], cwd=tmp_path, capture_output=True, text=True, check=True
    ).stdout.splitlines()
    assert f"trash {item.id} [sp]" in log, log
    # Und die Datei ist im Commit drin — der Commit ist der Undo-Weg, den P9-J den Menschen
    # verspricht ("Wiederherstellung ist Dateisystem- und Git-Arbeit des Nikingers").
    tracked = subprocess.run(
        ["git", "ls-files"], cwd=tmp_path, capture_output=True, text=True, check=True
    ).stdout.split()
    assert f"{TRASH_DIR}/sp/{item.id}__weg-damit.md" in tracked


# -- 5.  P9-51/P9-K: Rechte-Grenze -----------------------------------------------------------


def test_trash_refuses_a_foreign_item(store, tmp_path):
    """Der Store prüft **keine** Rechte (wie überall — `update`, `move`, `archive` auch nicht);
    der Aufrufer tut es. Dieser Test pinnt deshalb die *Eingabeseite*: der Store arbeitet nur mit
    Item-IDs des eigenen DATA_ROOT, und ein fremdes Item ist für ihn nicht erreichbar, weil es
    nicht in diesem Root liegt. Die eigentliche Rechteprüfung sitzt im Endpunkt
    (`api.py :: _items_delete`) und wird dort getestet — dort, wo sie hingehört."""
    fremd_root = tmp_path / "fremd"
    fremd_root.mkdir()
    fremd = Store(fremd_root, git=False)
    item = fremd.create("sp", type="task", title="Fremd")

    with pytest.raises(ItemNotFound):
        store.trash(item.id, version=item.version)
    assert fremd.get(item.id).id == item.id, "der fremde Store ist unberührt"


# -- 6./12.  P9-K und P9-J: keine Werkzeuge, keine Liste --------------------------------------


def test_no_mcp_tool_exposes_trash():
    """P9-K: **kein** MCP-Werkzeug fürs Löschen. Die Begründung steht im Plan und ist keine
    Formsache: ein Löschwerkzeug im Agenten-Pfad hieße, dass ein prompt-injizierter fremder Body
    eigene Notizen wegräumen kann — Hard Rule 4 nennt fremde Inhalte ausdrücklich als potenzielle
    Befehle. Geprüft wird die **Dekoration**, nicht der Text: ein Werkzeug namens `delete_item`,
    das intern `trash()` aufriefe, würde an dieser Zeile auffallen."""
    source = TOOLS_PY.read_text(encoding="utf-8")
    tool_namen = re.findall(r'@mcp\.tool\(\s*\n?\s*title="([^"]+)"', source)
    assert not [t for t in tool_namen if re.search(r"lösch|delete|trash|entfern", t, re.I)], (
        tool_namen
    )
    assert "def trash" not in source and ".trash(" not in source, (
        "tools.py referenziert trash() — P9-K erlaubt dem Agentenpfad keinen Zugriff darauf"
    )
    # Und derselbe Maßstab an der Werkzeug-Signatur-Liste: kein Parameter namens `confirm`
    # (das Gate gehört dem Menschen, es ist kein Agenten-Gate).
    assert not re.search(r"@mcp\.tool[\s\S]{0,400}?confirm\s*:\s*str", source)


def test_the_rest_api_has_no_route_that_lists_the_trash():
    """P9-J: „kein Eintrag im Rail, keine Wiederherstellung in der UI, **kein API-Endpunkt, der
    `_trash/` listet**". Der dritte Teil ist der einzige, der sich still verschlechtern kann: ein
    späteres `/api/v1/trash` oder ein `?include=trashed` wäre genau die zweite Oberfläche, die
    P9-J ausschließt."""
    routen = re.findall(r'Route\("([^"]+)"', API_PY.read_text(encoding="utf-8"))
    verboten = [r for r in routen if re.search(r"trash|papierkorb|deleted", r, re.I)]
    assert not verboten, verboten
    # `GET /api/v1/items` bleibt der einzige Leseweg und kennt kein Trashed-Filter-Feld.
    items_get = API_PY.read_text(encoding="utf-8").split("async def _items_get(")[1]
    assert 'request.query_params.get("trashed")' not in items_get


# -- 7.  P9-46: der Dialog verlangt den exakten Titel ---------------------------------------


def test_the_locked_button_is_visibly_locked():
    """**Das Gate muss auch *sichtbar* gesperrt sein**, sonst klickt der Mensch ins Leere und
    hält den Knopf für kaputt. Zwei Hälften, und beide sind billig zu prüfen:

    Der Knopf trägt `.btn-primary` (die Klasse, für die `app.css:278` einen echten
    `:disabled`-Zustand definiert: `--surface`-Fläche, `--text-faint`, `cursor: not-allowed`),
    und die CSS-Regel existiert überhaupt noch.

    **Ausdrücklich gemessen, nicht geglaubt:** Die Sichtprüfung am echten Browser meldete für den
    gesperrten Knopf „aktiv". Das war der **VLM**, nicht die Seite — `is_disabled()` im DOM sagt
    `True`, und `app.css:278` stylt den Zustand. Genau die Grenze, die
    `docs/concepts/sichtpruefung_automation_tooling.md` für dieses Werkzeug dokumentiert
    (Zustands- und Detailaussagen sind unbrauchbar, Anwesenheit von Text nicht). Deshalb wird
    hier die *Regel* gepinnt und nicht das Urteil eines Bildlesers."""
    markup = (REPO_ROOT / "phase5_ui" / "webui" / "static" / "app.html").read_text(encoding="utf-8")
    knopf = re.search(r'<button[^>]*id="trash-submit"[^>]*>', markup)
    assert knopf, "#trash-submit fehlt im Markup"
    assert "btn-primary" in knopf.group(0), "der Loesch-Knopf traegt nicht .btn-primary"
    # `disabled` steht im Startzustand: ohne Titel-Eingabe gibt es nichts zu bestaetigen.
    assert "disabled" in knopf.group(0), "der Knopf startet nicht gesperrt"

    css = (REPO_ROOT / "phase5_ui" / "webui" / "static" / "app.css").read_text(encoding="utf-8")
    assert re.search(r"\.btn-primary:disabled\s*\{[^}]*cursor:\s*not-allowed", css), (
        "kein sichtbarer :disabled-Zustand fuer .btn-primary — das Gate waere unsichtbar"
    )


def test_delete_dialog_requires_the_exact_title():
    """P9-46 statisch, am **Mechanismus** und nicht an einem Muster, das irgendwo im File
    hängen könnte. Zwei Hälften, und beide sind nötig:

    1. Der Knopf ist an den **Wert** des Eingabefelds gebunden (`disabled` folgt dem `input`-
       Ereignis). Ohne das gäbe es nur einen Text, der neben einem Knopf steht — der Dialog
       hätte keine zweite Stufe.
    2. Der Vergleich ist **exakt**: `trim()` ja (ein versehentliches Leerzeichen am Ende ist kein
       Fehlklick), aber **kein** `toLowerCase()`, kein `startsWith`, kein Levenshtein. Jede
       Toleranz nimmt dem Gate genau die Sekunde, die §9.2 erzwingen will.

    Bewusst geprüft wird der **Dialog-Block**, nicht die ganze Datei: `dialogs.js` enthält
    genug andere Vergleiche, dass eine Datei-weite Regex hier nichts beweisen würde."""
    source = DIALOGS_JS.read_text(encoding="utf-8")
    block = source.split("// -- Löschdialog")[1].split("// -- Speichern / Konflikt")[0]
    assert block, "kein Löschdialog-Block in dialogs.js"

    # 1) Die Sperre folgt dem Eingabewert — als **eine** Funktion im Dialogblock, aufgerufen vom
    # `input`-Listener. Zwei Orte wären zwei Wahrheiten; wer das Gate später ändert, soll es an
    # genau einer Stelle finden.
    assert re.search(
        r'trashConfirmInputEl\.addEventListener\("input", trashRefreshSubmit\)', source
    ), "der Knopf folgt dem Eingabewert nicht"
    assert re.search(
        r"trashSubmitEl\.disabled = !ziel \|\| trashConfirmInputEl\.value\.trim\(\) !== ziel\.title",
        block,
    ), "die Sperre vergleicht nicht exakt (trim + !==) gegen den Titel"

    # 2) Keine Toleranz im Löschpfad — **im Code, nicht im Kommentar**. Die Kommentare dieses
    # Blocks erwähnen `toLowerCase` und `startsWith` ausdrücklich, um sie *auszuschließen*; ein
    # naiver Textvergleich schlägt deshalb genau das an, was er verhindern soll. Dieselbe Falle
    # hat es in P8.6 Block H gegeben (ein Kommentar mit dem Literal `@media (max-width:1280px)`
    # liess einen Wächter anschlagen). Kommentarzeilen fliegen deshalb raus, bevor geprüft wird.
    code = "\n".join(
        zeile for zeile in block.splitlines() if not zeile.lstrip().startswith("//")
    )
    assert "toLowerCase" not in code, "der Löschpfad normalisiert die Groß-/Kleinschreibung"
    assert not re.search(r"startsWith|includes\(|fuzz|levensh", code, re.I), (
        "der Löschpfad vergleicht ungefähr — das Gate soll eine Sekunde Nachdenken erzwingen"
    )
    # Und der Dialog ist an den Knopf gebunden, nicht nur definiert.
    assert "export function openTrashDialog" in block
    LIST_JS = REPO_ROOT / "phase5_ui" / "webui" / "static" / "js" / "list.js"
    assert "openTrashDialog(item)" in LIST_JS.read_text(encoding="utf-8"), (
        "der Dialog wird nie geöffnet — die Stufe 2 wäre unerreichbar"
    )


# -- 10.  die Karte ---------------------------------------------------------------------------


def test_incoming_links_of_a_trashed_item_stop_being_a_graph_edge(tmp_path):
    """P9-49 nennt ausdrücklich die **Karte**. `index.delete_item()` räumt nur Zeilen mit dieser
    `src_id`; eine Notiz, die das gelöschte Item im Frontmatter oder im Body nennt, behält ihre
    Zeile mit `dst_id` auf den gelöschten Knoten. Das ist Absicht (dangling `dst_id` bleibt
    erlaubt, `delete_item()`s Docstring), **aber** die API muss es filtern: `_graph_get` verlangt,
    dass beide Endpunkte in der sichtbaren Knotenmenge sind, und die kommt aus `search()`.

    Der Test prüft die Kette aus beiden Hälften: dass `delete_item()` die ausgehenden Kanten
    miträumt **und** dass die verbleibende Zeile auf einen Knoten zeigt, den es nicht mehr gibt —
    also genau die Lage, aus der `_graph_get` eine Kante bauen müsste, wenn jemand seinen
    Endpunkt-Filter entfernt."""
    import sqlite3

    store = Store(tmp_path, git=False)
    ziel = store.create("sp", type="task", title="Weg")
    quelle = store.create("sp", type="note", title="Nennt es", links=[ziel.id])
    store.create("sp", type="note", title="Nennt es im Body", body=f"siehe {ziel.id}")

    store.trash(ziel.id, version=ziel.version)

    conn = sqlite3.connect(tmp_path / ".index.sqlite3")
    try:
        knoten = {r[0] for r in conn.execute("SELECT id FROM items")}
        assert ziel.id not in knoten
        verbliebene = conn.execute(
            "SELECT src_id, dst_id FROM item_links WHERE dst_id = ?", (ziel.id,)
        ).fetchall()
        # Genau das ist die dokumentierte Lage: die Zeilen **bleiben** stehen, zeigen aber auf
        # einen Knoten, den `search()` nicht mehr liefert. `_graph_get` filtert daran — käme die
        # Kante durch, hinge ein gelöschtes Item noch in der Karte (P9-49).
        assert verbliebene, "die eingehenden Kanten muessen als dangling erhalten bleiben"
        assert _zeigen_auf_geloeschten_knoten(verbliebene, knoten)
    finally:
        conn.close()
    assert quelle.id in {i.id for i in store.search(space="sp").items}, (
        "die verbleibende Notiz muss erhalten bleiben — es wird das Ziel gelöscht, nicht die Quelle"
    )


def _zeigen_auf_geloeschten_knoten(kanten, knoten) -> bool:
    """Die Quellen existieren noch, die Ziele nicht mehr — das ist der Zustand, den `_graph_get`
    filtern muss. Die Umkehrung („alle zeigen auf existierende Knoten") wäre die Behauptung, es
    gäbe keine dangling Kanten; die gibt es sehr wohl, sie sind nur harmlos."""
    return bool(kanten) and all(src in knoten and dst not in knoten for src, dst in kanten)


# -- 11.  Nachbarn bleiben unberührt ----------------------------------------------------------


def test_trash_does_not_touch_a_neighbouring_item(store, tmp_path):
    a = store.create("sp", type="task", title="Alpha", folder="Projekte")
    b = store.create("sp", type="task", title="Beta", body="Inhalt B")
    vor_b = (tmp_path / "sp" / f"{b.id}__beta.md").read_bytes()

    store.trash(a.id, version=a.version)

    nach_b = store.get(b.id)
    assert nach_b.title == "Beta" and nach_b.version == b.version
    assert (tmp_path / "sp" / f"{b.id}__beta.md").read_bytes() == vor_b
    assert [p.name for p in _trashed(tmp_path)] == [f"{a.id}__alpha.md"]
