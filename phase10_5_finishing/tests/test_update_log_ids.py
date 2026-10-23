"""Der Update-Log-Banner: die IDs dürfen sich **nicht** wiederverwenden (P10.5 Block 7, Schritt 7.0).

**Der Befund, den diese Datei festhält (2026-10-23).** `webui/updates.py :: parse_update_log()`
vergab die IDs (`"<Datum>#<n>"`) **in Dateireihenfolge von oben**. Neue Einträge werden aber
**oben** eingefügt (Changelog) — ein **zweiter Deploy am selben Tag** bekam damit die ID `#1`,
die der erste Deploy desselben Tages **schon** hatte. Der gesehen-Zustand hängt genau an dieser
ID (`users.seen_update_id`, `webui/api.py :: _updates_get`), also galt
`latest_id == seen_update_id` ⇒ **kein Banner**: der neue Eintrag war für den Benutzer stumm.
Gemessen in `phase10_5_finishing/probes/p105_deploy_b_probe.py` (Gruppe E).

**Die Regel, die jetzt gilt:** der Zähler läuft je Datum **von unten** — der älteste Block
eines Datums trägt die #1, ein neu oben eingefügter Block die nächste freie Nummer. Damit
bekommt **jeder neue Block eine ID, die kein bestehender Block trägt**, und die IDs der
bestehenden Blöcke bleiben stehen.

**Der Wächter** ist bewusst am **Banner-Zustand** festgemacht (`latest_id != seen_update_id`),
nicht an der ID-Form: die ID-Form ist eine Implementierungsentscheidung, der Banner-Zustand
das, was der Benutzer sieht. Die Basis-Tests des Parsers stehen in
`phase6_shares/tests/test_updates.py` (dort entstanden sie, P6 Step 3).
"""
from __future__ import annotations

from webui.updates import parse_update_log


def _block(datum: str, *zeilen: str) -> str:
    return "\n".join([f"## {datum}", *(f"- {zeile}" for zeile in zeilen)])


def test_ein_neuer_block_oben_bekommt_eine_id_die_kein_bestehender_block_traegt():
    """**Die Regressionszeile.** Vorher (Zähler von oben) bekam der neue Block die ID, die der
    Benutzer zuletzt gesehen hatte — der Banner blieb stumm."""
    gesehen = parse_update_log(_block("2026-10-23", "Deploy A."))[0].id

    nachher = parse_update_log("\n\n".join([
        _block("2026-10-23", "Deploy B."),
        _block("2026-10-23", "Deploy A."),
    ]))
    assert nachher[0].id != gesehen
    # Der alte Block behält seine ID (der Benutzer bleibt auf seinem Block).
    assert nachher[1].id == gesehen


def test_der_banner_erscheint_nach_einem_zweiten_deploy_am_selben_tag():
    """Die Bedingung aus `webui/static/js/updates.js`: der Banner erscheint genau dann, wenn
    `latest_id != seen_update_id`."""
    gesehen = parse_update_log(_block("2026-10-23", "Deploy A."))[0].id
    nachher = parse_update_log("\n\n".join([
        _block("2026-10-23", "Deploy B."),
        _block("2026-10-23", "Deploy A."),
    ]))
    assert nachher[0].id != gesehen  # ⇒ der Banner erscheint


def test_die_ids_der_bestehenden_blaecke_bleiben_bei_einem_neuen_block_stehen():
    """Die Invariante, auf die der Fix beruht: ein Block **oben** einzufügen verschiebt die
    IDs der Blöcke **darunter** nicht."""
    vorher = parse_update_log(_block("2026-10-23", "Deploy A."))
    nachher = parse_update_log("\n\n".join([
        _block("2026-10-23", "Deploy B."),
        _block("2026-10-23", "Deploy A."),
    ]))
    assert vorher[0].id == nachher[1].id
    assert nachher[0].id != vorher[0].id


def test_je_datum_wird_getrennt_gezaehlt():
    text = "\n\n".join([
        _block("2026-10-23", "Neuestes."),
        _block("2026-10-08", "Aelteres."),
        _block("2026-10-23", "Aelteres am selben Tag."),
    ])
    ids = [e.id for e in parse_update_log(text)]
    assert len(set(ids)) == len(ids)
    assert ids[0].split("#")[0] == ids[2].split("#")[0] == "2026-10-23"
    assert ids[1].split("#")[0] == "2026-10-08"
