"""Editor 4.1, Schritt S1 — **Entwurfsschutz** (Plan §4.2 V7, Befund F7), statisch, ohne Browser.

Der Browser-Beleg ist `probes/p105_ed41_darstellung_s1.json` (Zellen `oeffnen_schreibt_keinen_entwurf`,
`entwurf_ueberlebt_neuladen`, `kein_stilles_zurueck`, Waechter `test_ed41_probe.py`). Hier steht fest,
**wie** der Code das erreicht — damit ein spaeterer Schritt (S2 baut in denselben Dateien) die drei
Regeln nicht still verliert:

1. ein Entwurf entsteht nur bei einer **Nutzer**-Aenderung (Ursprung ≠ `setValue`) und nur, wenn der
   Editor vom Schnappschuss abweicht; ein sauberer Editor loescht ihn;
2. der Entwurf traegt seine **Basisversion** und wird beim Oeffnen **vor** `setBody` gelesen;
3. ein Entwurf zu einer anderen Version wird nie still wiederhergestellt (Konfliktdialog, Weg
   `conflict-save-as-new`) — der clientseitige Last-Write-Wins, den Hard Rule 3 sinngemaess verbietet.
"""
from __future__ import annotations

import re
from pathlib import Path

STATIC = Path(__file__).resolve().parents[2] / "phase5_ui" / "webui" / "static"
EDITOR = STATIC / "js" / "editor.js"
DIALOGS = STATIC / "js" / "dialogs.js"
APP_HTML = STATIC / "app.html"


def _text(pfad: Path) -> str:
    return pfad.read_text(encoding="utf-8")


def _rumpf(text: str, funktion: str) -> str:
    start = text.index("function " + funktion + "(")
    tiefe, i = 0, text.index("{", start)
    beginn = i
    while True:
        if text[i] == "{":
            tiefe += 1
        elif text[i] == "}":
            tiefe -= 1
            if tiefe == 0:
                return text[beginn:i + 1]
        i += 1


def test_the_draft_carries_its_base_version_and_a_timestamp_from_the_snapshot():
    rumpf = _rumpf(_text(EDITOR), "saveDraft")
    assert "state.editingSnapshot" in rumpf
    assert "version: snap.version" in rumpf
    assert "gespeichert:" in rumpf
    # Kennung aus dem Schnappschuss, nie aus `selectedId` (F7 ueber `saveItem()`)
    assert "selectedId" not in rumpf
    assert "draftKeyFor(snap.id)" in rumpf


def test_the_draft_lives_in_session_storage_under_the_documented_key_only():
    text = _text(EDITOR)
    assert 'function draftKeyFor(id) { return "sfx:draft:" + id; }' in text
    for funktion in ("saveDraft", "clearDraft", "loadDraftIfAny"):
        rumpf = _rumpf(text, funktion)
        assert "localStorage" not in rumpf, funktion
        assert "sessionStorage" in rumpf, funktion


def test_only_a_user_change_on_a_dirty_editor_writes_a_draft():
    rumpf = _rumpf(_text(EDITOR), "_editorGeaendert")
    assert "function _editorGeaendert(_quelle, change)" in _text(EDITOR)
    ursprung = 'if (change && change.origin === "setValue") return;'
    assert ursprung in rumpf
    assert rumpf.index(ursprung) < rumpf.index("saveDraft()")
    assert "if (dirty) saveDraft();" in rumpf
    # sauber -> kein Entwurf (Tippen + Loeschen hinterlaesst keine Phantom-Rueckfrage)
    assert "else if (state.editingSnapshot) clearDraft(state.editingSnapshot.id);" in rumpf
    # der Gegenlauf-Anker (s1_ohne_ursprung) kommt genau einmal vor
    assert _text(EDITOR).count('  if (change && change.origin === "setValue") return;\n') == 1


def test_the_draft_is_read_before_set_body_when_opening():
    rumpf = _rumpf(_text(EDITOR), "showEditableItem")
    assert rumpf.count("loadDraftIfAny(item.id)") == 1
    assert rumpf.index("loadDraftIfAny(item.id)") < rumpf.index("setBody(item.body)")


def test_a_draft_for_another_version_goes_the_conflict_way_never_a_silent_restore():
    text = _text(EDITOR)
    rumpf = _rumpf(text, "showEditableItem")
    pruefung = "if (draft.version !== item.version) {"
    assert text.count("  " + pruefung + "\n") == 1          # Gegenlauf-Anker s1_ohne_version
    stale = rumpf[rumpf.index(pruefung):]
    stale = stale[:stale.index("return;")]
    # die Basisversion des Entwurfs wird die Version des Schnappschusses -> Strg+S = 409
    assert "state.editingSnapshot.version = typeof draft.version === \"number\" ? draft.version : 0;" in stale
    assert "showConflictDialog(item, { entwurf: draft });" in stale
    # „Wiederherstellen?" nur danach (gleiche Version), und nur auf dem Schnappschuss vom Oeffnen
    assert rumpf.index(pruefung) < rumpf.index('ok: "Wiederherstellen"')
    assert "if (state.editingSnapshot !== snapBeimOeffnen) return;" in rumpf


def test_clear_detail_drops_a_clean_draft_only():
    rumpf = _rumpf(_text(EDITOR), "clearDetail")
    zeile = "if (state.editingSnapshot && !isDirty()) clearDraft(state.editingSnapshot.id);"
    assert zeile in rumpf
    assert rumpf.index(zeile) < rumpf.index("state.editingSnapshot = null;")


def test_the_stale_draft_dialog_reuses_the_conflict_dialog_and_its_save_as_new_path():
    text = _text(DIALOGS)
    rumpf = _rumpf(text, "showConflictDialog")
    assert "function showConflictDialog(current, opts)" in text
    for teil in ('"Veralteter Entwurf"', '"Entwurf verwerfen"', '"Entwurf als neues Item anlegen"',
                 'Entwurf zu "', '"Aktuelle Fassung laden"', '"Meine Fassung als neues Item anlegen"'):
        assert teil in rumpf, teil
    # Fokus auf „Abbrechen": kein Tastendruck verwirft oder schreibt etwas
    assert "conflictCancelButtonEl.focus()" in rumpf
    html = _text(APP_HTML)
    assert '<h2 id="conflict-title">Konflikt</h2>' in html
    assert 'id="conflict-save-as-new"' in html
    # „Entwurf verwerfen" = der vorhandene Knopf, der den Entwurf loescht
    laden = text[text.index("conflictLoadCurrentButtonEl.addEventListener"):]
    laden = laden[:laden.index("conflictSaveAsNewButtonEl.addEventListener")]
    assert "clearDraft(current.id);" in laden


def test_the_editor_does_not_steal_focus_from_an_open_dialog():
    rumpf = _rumpf(_text(EDITOR), "_editorBereit")
    assert re.search(r'if \(!document\.querySelector\("\.overlay:not\(\[hidden\]\)"\)\) cm\.focus\(\);', rumpf)
