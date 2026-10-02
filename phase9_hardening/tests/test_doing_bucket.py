"""Tests für den P9-Block doing — der fünfte Navigations-Eimer (Lock **P9-V**).

Mini-Plan `docs/concepts/phase9_hardening_block_doing_plan.md` §5, T1/T2/T6. Die drei HTTP-
Tests des Blocks (T3/T4/T5) liegen in `phase5_ui/tests/test_overview.py` — dort wohnen die
App-Fixtures, und `phase9_hardening/tests/` hat kein `conftest.py` (V176).

  1. test_bucket_order_is_open_doing_done_note_archived      (T1, P9-X — statisch, Reihenfolge)
  2. test_every_status_value_lands_in_exactly_one_bucket     (T2, P9-61 — Partition, generiert
     aus `STATUS_VALUES`, nicht aus einer hier abgetippten Liste)
  3. test_every_bucket_has_a_german_label                    (T6, P9-63 — kein rohes `doing`)

**Warum T2 der eigentliche Wächter ist.** Die Liste hier ist der Raum, in dem ein Item
verschwinden kann: `bucketFor()` nimmt den ERSTEN passenden Eintrag, und `bucketFor()` liefert
`null`, wenn keiner passt — dann fallen beide Aufrufer auf `|| state.filter` zurück, und die
Entscheidung „welcher Ordner ist das überhaupt?" fällt still aus. Genau so ist `done` in
P5 Step 7b verloren gegangen, und `doing` hätte dasselbe Schicksal gehabt. Die Prüfung liest
deshalb `STATUS_VALUES` aus `storage.models` und bildet `bucketFor()`s Bedingung in Python nach:
**jede** `(Typ, Status)`-Kombination muss in **genau einem** Eimer landen. Beim nächsten neuen
Statuswert schlägt der Test laut an, statt dass der Wert nur niemandem auffällt.

Kein Netz, kein echter DATA_ROOT, kein Dienst, kein LLM.
"""

from __future__ import annotations

import re
from pathlib import Path

from storage.models import STATUS_VALUES

from webui.api import _BUCKETS

REPO_ROOT = Path(__file__).resolve().parents[2]
API_PY = REPO_ROOT / "phase5_ui" / "webui" / "api.py"
STATE_JS = REPO_ROOT / "phase5_ui" / "webui" / "static" / "js" / "state.js"

# `bucketFor()` (static/js/list.js) in Python nachgebildet. Bewusst **zeichenweise** dieselbe
# Bedingung: `!f.type` ist in JS ein falsy-Test auf `undefined` oder `""`, und `_BUCKETS` kennt
# keine dritte Variante — der `or`-Zweig in Python ist deshalb dieselbe Aussage, nicht eine
# Näherung.
def _matches(filters: dict, item_type: str, item_status: str) -> bool:
    type_ok = not filters.get("type") or filters["type"] == item_type
    status_ok = not filters.get("status") or filters["status"] == item_status
    return type_ok and status_ok


# -- T1: die Reihenfolge (P9-X) --------------------------------------------------------------


def test_bucket_order_is_open_doing_done_note_archived():
    """`open` zuerst, `archived` zuletzt, `doing` **zwischen** `open` und `done` — das ist die
    Lebenslaufrichtung einer Aufgabe und zugleich die Leserichtung der Rail. Beide Ränder sind
    funktional, nicht kosmetisch:
    - `archived` zuletzt, weil `bucketFor()` den ersten Treffer nimmt und eine archivierte
      Aufgabe sonst nie ins Archiv käme (`_BUCKETS`-Kommentar, gepinnt von `test_meta.py`),
    - `open` zuerst, weil `app.js` bei unbekanntem `state.filter` auf `names[0]` zurückfällt
      und `state.js` mit `filter: "open"` startet.
    Die Reihenfolge wird hier **aus dem Quelltext** gelesen, nicht aus `list(_BUCKETS)` — der
    Import trägt die Reihenfolge in Python 3.7+ zwar auch, aber der Test soll die Datei
    beschreiben, die ein Mensch liest, und beide können nicht gleichzeitig auseinanderlaufen."""
    source = API_PY.read_text(encoding="utf-8")
    block = re.search(r"_BUCKETS: dict\[str, dict\[str, str\]\] = \{(.*?)\n\}", source, re.DOTALL)
    assert block, "_BUCKETS nicht gefunden"
    reihenfolge = re.findall(r'^\s{4}"([a-z]+)": \{', block.group(1), re.MULTILINE)
    assert reihenfolge == ["open", "doing", "done", "note", "archived"], reihenfolge
    # Und sie stimmt mit dem, was der Server wirklich ausliefert (`test_meta.py` prüft die
    # Nutzlast, dieser Test die Absicht — eins von beiden allein wäre eine halbe Aussage).
    assert list(_BUCKETS) == reihenfolge


# -- T2: die Partition über das gesamte Statusvokabular (P9-61) ------------------------------


def test_every_status_value_lands_in_exactly_one_bucket():
    """Jede `(Typ, Status)`-Kombination aus `STATUS_VALUES` landet in **genau einem** Eimer.

    Zwei Fehlerklassen, beide still:
    - **null Treffer** → `bucketFor()` liefert `null`, der Ordner existiert nicht, das Item ist
      nur über Suche und „Alle Items" auffindbar. Genau das war `done` vor Step 7b und `doing`
      vor diesem Block.
    - **mehr als ein Treffer** → es gewinnt die Reihenfolge, also zählt ein Item doppelt in
      `_overview()`, während der Listenfilter es nur einmal zeigt. Das bricht die
      Konstruktionseigenschaft „Zähler == Liste", die `_overview()` trägt.

    Beide Richtungen werden geprüft, weil „null" die teurere Hälfte ist und „mehrfach" die
    stillere: der duplizierte Eimer fällt erst auf, wenn jemand die Zahlen vergleicht."""
    kombinationen = [
        (typ, status)
        for typ, statuswerte in sorted(STATUS_VALUES.items())
        for status in sorted(statuswerte)
    ]
    assert kombinationen, "STATUS_VALUES ist leer — der Test prüfte nichts"
    for typ, status in kombinationen:
        treffer = [name for name, f in _BUCKETS.items() if _matches(f, typ, status)]
        assert len(treffer) == 1, (
            f"({typ}, {status}) landet in {len(treffer)} Eimern: {treffer} — "
            f"null Treffer heißt 'Item nicht auffindbar', mehr als einer heißt 'zählt doppelt'"
        )
    # Der Vollständigkeit halber die Umkehrung als eigene Zeile: jeder Eimer muss von **irgendeiner**
    # Kombination aus `STATUS_VALUES` erreicht werden. Ein toter Eimer (etwa ein zurückgelassener
    # `_trash`- oder `doing`-Eimer nach einer Umbenennung) wäre sonst unauffindbar für diesen Test.
    getroffen = {name for typ, status in kombinationen for name, f in _BUCKETS.items()
                 if _matches(f, typ, status)}
    assert getroffen == set(_BUCKETS), f"niemand erreicht: {set(_BUCKETS) - getroffen}"


# -- T6: die Beschriftung (P9-63) -------------------------------------------------------------


def test_every_bucket_has_a_german_label():
    """Jeder Eimer hat ein deutsches Label, und keiner zeigt seinen rohen Schema-Namen.

    `tree.js :: renderFolders()` liest `BUCKET_LABELS[b] || b` — der `||`-Rückfall bedeutet: ein
    fehlendes Label ist **kein Fehler**, es sieht nur aus wie ein Feature mit englischem Wort.
    Deshalb wird die Menge der Labels gegen die Menge der Eimer geprüft, nicht nur `doing` alone.

    Gelesen wird die Tabelle **aus `state.js`**, per Regex: das ist die Datei, die der Browser
    bekommt. Die Doppelpinung (JS-Quelle lesen *und* `_BUCKETS` importieren) ist Absicht — ein
    Modul-Dict gäbe es nur auf der Python-Seite, und genau da geht der Fehler sonst unbemerkt
    durch."""
    source = STATE_JS.read_text(encoding="utf-8")
    block = re.search(r"export var BUCKET_LABELS = \{(.*?)\n\};", source, re.DOTALL)
    assert block, "BUCKET_LABELS nicht gefunden"
    labels = dict(re.findall(r'^\s{2}(\w+): "([^"]+)",\s*$', block.group(1), re.MULTILINE))
    assert set(labels) == set(_BUCKETS), (
        f"Label-Menge {set(labels)} != Eimer-Menge {set(_BUCKETS)} — "
        f"ohne Label greift `BUCKET_LABELS[b] || b` und der Ordner heißt roh 'doing'"
    )
    assert labels["doing"] == "In Arbeit"
    # Und keine Beschriftung darf den rohen Schema-Wortlaut wiederholen (P9-W: übersetzt wird
    # nur die Navigationsebene).
    assert all(label != name for name, label in labels.items()), labels
