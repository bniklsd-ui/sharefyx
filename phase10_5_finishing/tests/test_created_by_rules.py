"""Wächter für RE-7 `created_by` — P10.5 Block 9, Schritt 9.1 (P1-Öffnung 12).

**Was dieses Feld ist.** `created_by` nennt den Space, aus dessen **authentifiziertem**
Principal das Item angelegt wurde — dieselbe Klasse wie `updated_by` (P9 Block trace): vom
Server gesetzt, über **keinen** Kanal setzbar, **kein Backfill** (Lock P10.5-W).

**Warum ein eigener Wächter und nicht nur die Verhaltenstests.** Die Verhaltenstests in
`phase1_storage/tests/test_store.py` und `phase2_mcp/tests/test_tools.py` belegen, dass das Feld
*funktioniert*. Sie belegen nicht, **welche Regel** es am Leben hält. Das ist die Fehlerklasse,
die dieser Ordner zweimal gesehen hat (P9-F4/F10: `assignee` war in `Item.extra` statt im Feld,
und `_summary()` vergaß es — der Test auf `get()` allein war grün und falsch).

**Vier Regeln, vier Gegenläufe.** Ein Wächter ohne Gegenlauf beweist nichts: eine Prüfung, die
die falsche Sache prüft, ist grün und falsch zugleich. Jeder Gegenlauf patcht **genau eine**
Regel im echten Code und muss **genau den** zugehörigen Defekt sichtbar machen:

| Regel | Der Defekt, wenn sie fällt |
|---|---|
| `created_by` steht in `_KNOWN_FIELDS` | das Feld landet im `Item.extra`-Sack — doppelt, ohne Default |
| `created_by` steht in `_SYSTEM_MANAGED_FIELDS` | ein Aufrufer kann den Anleger **fälschen** |
| `_summary()` reicht `created_by` durch | `get()` liefert den echten Wert, `search()` liefert `""` |
| `_item_to_text()` schreibt nur bei nicht-leerem Wert | jeder Altbestand-Item bekommt ein stilles `created_by: ""` |

Kein Netz, kein Browser, kein DATA_ROOT, kein Dienst — alles in-process gegen ein `tmp_path`.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from storage import store as store_module
from storage.models import Item, ItemSummary
from storage.store import Store


@pytest.fixture
def store(tmp_path) -> Store:
    return Store(tmp_path, now_fn=lambda: datetime.now(timezone.utc), git=False)


def _datei(root: Path, space: str, item_id: str) -> Path:
    (treffer,) = list((root / space).glob(f"{item_id}__*.md"))
    return treffer


# -- Die vier Regeln, am echten Code ----------------------------------------------------------


def test_created_by_steht_in_known_fields():
    """Ohne diesen Eintrag landet `created_by` in `Item.extra` — der Sack für **unbekannte**
    Frontmatter-Felder. Ein Feld im Sack hat keinen Default, keine `ItemSummary`-Spalte und
    keinen Platz im Adapter; es überlebt nur den Round-Trip (P9 F4, dieselbe Lehre ein drittes
    Mal)."""
    assert "created_by" in store_module._KNOWN_FIELDS


def test_created_by_steht_in_system_managed_fields():
    """Ohne diesen Eintrag wäre das Feld **setzbar**: `create(created_by=…)` und
    `update(created_by=…)` kämen durch, und der Client könnte den Anleger behaupten. Die Sperre
    ist der Kern der Aussage (P9-AA für `updated_by`)."""
    assert "created_by" in store_module._SYSTEM_MANAGED_FIELDS


def test_created_by_wird_durch_summary_durchgereicht(store):
    """`search()` ist der Weg, über den eine **Trefferliste** entsteht. Ohne die Durchreichung
    stünde dort dauerhaft `""`, während `get()` den echten Wert lieferte — genau die Divergenz,
    die P9 Step F als F10 aufgedeckt hat."""
    item = store.create("alpha", type="task", title="Rechnung", actor="alpha")

    treffer = store.search(space="alpha").items[0]

    assert isinstance(treffer, ItemSummary)
    assert treffer.created_by == "alpha"


def test_created_by_wird_nur_bei_nicht_leerem_wert_geschrieben(store, tmp_path):
    """Der **Altbestand** darf durch einen schreibenden Zugriff **keine** leere Zeile bekommen.
    Ohne die Bedingung stünde nach dem ersten Speichern `created_by: ""` in jeder bestehenden
    Datei — ein Frontmatter-Diff, den niemand bestellt hat (P9-42, dieselbe Lehre wie bei
    `assignee` und `updated_by`)."""
    item = store.create("alpha", type="task", title="Altbestand", actor="")

    store.update(item.id, version=item.version, title="Altbestand (neu)")

    text = _datei(tmp_path, "alpha", item.id).read_text(encoding="utf-8")
    assert "created_by" not in text


# -- Die vier Gegenläufe: eine Regel patchen, der Defekt muss sichtbar werden ----------------


def test_gegenlauf_ohne_known_fields_landet_das_feld_im_extra_sack(store, tmp_path, monkeypatch):
    """Gegenlauf 1: `created_by` aus `_KNOWN_FIELDS` entfernt ⇒ das Feld ist **doppelt**: im
    Feld *und* im `Item.extra`-Sack. Der Sack ist für **unbekannte** Felder — ein Item, das
    dort einen bekannten Feldnamen traegt, ist ein Item mit zwei Quellen für denselben Wert."""
    # `_KNOWN_FIELDS` ist ein **set**, kein dict — `monkeypatch.delitem` kann das nicht;
    # der Gegenlauf ersetzt die Menge durch eine ohne den Eintrag.
    monkeypatch.setattr(
        store_module, "_KNOWN_FIELDS", store_module._KNOWN_FIELDS - {"created_by"}
    )

    item = store.create("alpha", type="task", title="Doppelt", actor="alpha")
    gelesen = store.get(item.id)

    assert "created_by" in gelesen.extra, (
        "der Gegenlauf ist wirkungslos: `created_by` steht immer noch nicht im Extra-Sack"
    )
    assert gelesen.extra["created_by"] == "alpha"


def test_gegenlauf_ohne_system_managed_fields_ist_der_anleger_faelschbar(store, tmp_path, monkeypatch):
    """Gegenlauf 2: `created_by` aus `_SYSTEM_MANAGED_FIELDS` entfernt ⇒ ein Aufrufer darf den
    Anleger **behaupten**, und die Behauptung landet sogar auf der Platte.

    Der Weg dorthin ist derselbe wie bei `assignee` (F5): `create()` reicht den unbekannten
    Schlüssel an `Item.extra` weiter, und `_item_to_text()` schreibt `item.extra` **über** den
    berechneten Feldern (`fields.update(item.extra)`) — der Sack gewinnt also gegen das Feld.
    Genau das ist die Aussage, die die Sperre trägt: der Server weiss, wer geschrieben hat —
    und der Client kann das nicht behaupten."""
    monkeypatch.setattr(
        store_module, "_SYSTEM_MANAGED_FIELDS",
        store_module._SYSTEM_MANAGED_FIELDS - {"created_by"},
    )

    item = store.create("alpha", type="task", title="Erfunden", created_by="beta")

    text = _datei(tmp_path, "alpha", item.id).read_text(encoding="utf-8")
    assert "created_by: beta" in text, (
        "der Gegenlauf ist wirkungslos: die gefaelschte Angabe landet nicht auf der Platte"
    )


def test_gegenlauf_ohne_summary_diverquieren_get_und_search(store, monkeypatch):
    """Gegenlauf 3: `_summary()` reicht `created_by` nicht durch ⇒ `search()` liefert `""`,
    während `get()` den echten Wert liefert. Zwei Lesepfade, zwei Werte — die Divergenz, die
    F10 aufgedeckt hat."""
    echtes_summary = store_module._summary

    def _ohne_created_by(item: Item) -> ItemSummary:
        summary = echtes_summary(item)
        summary.created_by = ""
        return summary

    monkeypatch.setattr(store_module, "_summary", _ohne_created_by)

    item = store.create("alpha", type="task", title="Divergenz", actor="alpha")

    assert store.get(item.id).created_by == "alpha"
    assert store.search(space="alpha").items[0].created_by == "", (
        "der Gegenlauf ist wirkungslos: `search()` liefert weiterhin den echten Wert"
    )


def test_gegenlauf_ohne_leerwert_bedingung_bekommt_der_altbestand_eine_leere_zeile(
    store, tmp_path, monkeypatch
):
    """Gegenlauf 4: `_item_to_text()` schreibt das Feld **immer** ⇒ der Altbestand bekommt nach
    dem ersten schreibenden Zugriff ein stilles `created_by: ""` — eine Aussage über einen
    Anleger, den der Server gar nicht kennt."""
    echtes_item_to_text = store_module._item_to_text

    def _immer(item: Item) -> str:
        text = echtes_item_to_text(item)
        return text.replace("version:", "created_by: \"\"\nversion:", 1)

    monkeypatch.setattr(store_module, "_item_to_text", _immer)

    item = store.create("alpha", type="task", title="Altbestand", actor="")

    text = _datei(tmp_path, "alpha", item.id).read_text(encoding="utf-8")
    assert 'created_by: ""' in text, (
        "der Gegenlauf ist wirkungslos: es entsteht keine leere Zeile"
    )
