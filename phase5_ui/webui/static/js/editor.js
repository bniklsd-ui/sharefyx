"use strict";

// -- Detail: Nur-lesen (fremdes Item) vs. Editor (eigenes Item) -----------------------------

import { state, editorPart, activeSpaceWritable, setCreateControlsPresent, setViewTitle, listViewTitle } from "./state.js";
import { el, toast } from "./toasts.js";
import { api, reportUnexpectedError } from "./api.js";
import { markdownToHtml, FORMAT_VOKABULAR } from "./markdown.js";
import { loadItems, loadOverview, renderList, renderListSlot } from "./list.js";
import { renderRail } from "./tree.js";
import { confirmDialog, showConflictDialog, openLinkPicker } from "./dialogs.js";
import { iconSvg } from "./icons.js";
import { withLoading } from "./loading.js";
import { ensureCodeMirror } from "./editor_cm.js";

var shellEl;
// P10.5, Block 4 (2026-10-22, Z4): der Detail-Slot traegt den Ladezustand beim Oeffnen.
var detailEl;
// Phase 8.6 Plan 2 Block G G5: das, was in Block C `overviewEl` hieß (#detail-overview, der
// Wrapper um Spaces + Graph), ist nach dem Umzug nur noch die Karte. Das DOM-Element heißt
// jetzt `#detail-graph`; die Spaces-Übersicht lebt in `#list-overview` und wird von
// `list.js :: renderListSlot()` gesteuert.
var graphPaneEl;
var detailReadonlyEl;
var roTitleEl;
var roMetaEl;
var roPreviewEl;
var roCloseButtonEl;

var detailEditorEl;
var editorVersionEl;
var versionBandEl;
var versionBandNumberEl;
var metaPanelEl;
var metaDigestEl;
var metaItemIdEl;
var fieldTitleEl;
var fieldStatusEl;
var fieldDueEl;
// P9 Block trace: `assignee` (editierbar) und `updated_by` (reine Anzeige, P9-AA).
var fieldAssigneeEl;
var metaUpdatedByEl;
// P10.5 Block 9 (RE-7): `created_by` (reine Anzeige, wie `updated_by`).
var metaCreatedByEl;
var fieldTagsEl;
var fieldLinksEl;
var editorToolbarEl;
var togglePreviewButtonEl;
var editorTextareaEl;
// P10.5, Block 11, Schritt 11.3 (ED-1): **unbenutzt seit dem Live-Editor.** Die Vorschau-
// Paneele im Editor (getrenntes HTML) gibt es nicht mehr -- der Live-Editor ist die Ansicht
// (Schritt 11.4 raeumt das Element aus dem Markup ab). Die **Lesesicht** fremder Items
// rendert weiter ueber `markdown.js` (`roPreviewEl`).
var editorPreviewEl;
// P10.5, Block 11, Schritt 11.3 (ED-1): der **Live-Editor**. `cm` ist die CodeMirror-Instanz
// (null = nicht geladen oder nicht ladbar). **Die Textarea ist der Notausgang** (ED-5, der
// Rohmodus): solange `cm` null ist, traegt die Textarea den Text, und alle Zugriffe gehen
// ueber `getBody()`/`setBody()` -- nie direkt ueber `.value`.
var cm = null;
//: Laedt der Editor gerade? (Dann darf kein zweiter Ladevorgang starten.)
var cmLaden = false;
//: Die zuletzt markierte Cursorzeile (fuer `sfx-active-line`, Schritt 11.4).
var cmCursorZeile = null;
// P10.5, Block 11, Schritt 11.5 (ED-2): die **To-do-Kaestchen**. Je Eintrag
// `{mark, text, kasten}` — die Marke (das `markText` im Dokument) und das Kaestchen, das
// sie traegt. **Der Text bleibt die Quelle**: das Kaestchen ersetzt nur die Darstellung
// der Zeichen `[ ]`/`[x]`.
var cmTodoMarken = [];
var saveButtonEl;
var archiveButtonEl;
var closeButtonEl;
var appendInputEl;
var appendButtonEl;
var conflictDialogEl;
var insertImageButtonEl;
var insertImageInputEl;
var assetStripEl;
var linkPickerButtonEl;  // Phase 8 Block B Step B4 (Plan §3 B4)
// P10.5, Block 10, Schritt 10.3 (P10.5-S): das Hinweisband "Geaendert von ... -- neu laden?".
var changedBannerEl;
var changedBannerTextEl;
var changedReloadButtonEl;
var changedCloseButtonEl;

export function showOverviewPane() {
  graphPaneEl.hidden = false;
  detailReadonlyEl.hidden = true;
  detailEditorEl.hidden = true;
  editorPart.detach();
  shellEl.dataset.view = "list";
  // P10.5 Block 7.3 (UI-3, V120): der Tab-Titel folgt der Listenansicht — Spaces-Übersicht,
  // „Alle Items" oder der Name des aktiven Space. `listViewTitle()` ist die eine Quelle für
  // alle drei (der Spacewechsel an drei Stellen würde sonst drei Aufrufstellen brauchen).
  setViewTitle(listViewTitle());
}

export function clearDetail() {
  state.selectedId = null;
  state.selectedReadonly = false;
  state.editingSnapshot = null;
  state.conflictCurrent = null;
  // P10.5-S: das Hinweisband gehoert zum Item -- mit dem Item verschwindet es.
  hideChangedBanner();
  // Advisor-Fund vor dem Commit (GLOBAL_SEARCH_PLAN.md): ohne diesen Reset blieb
  // `state.scope === "all"` nach "Alle Items" -> Home stehen, `activeSpaceWritable()` gab dort
  // faelschlich `false` zurueck und liess den Anlegen-Knopf auf der eigenen, schreibbaren
  // Uebersicht ausgehaengt. Playwright-bestaetigt (Wegwerf-Instanz, kein Repo-Artefakt).
  //
  // Phase 8.6 Plan 2 Block G G3 (Plan §4.3): dieselbe Zeile ist jetzt AUCH das einzige,
  // was `state.scope` aus "all" zurück auf "space" bringt, NACHDEM `navigateAll()` aus
  // dem Home-Handler entfernt ist (Plan §4.3, G3). Der alte Handler rief closeEditor ->
  // clearDetail (setzt scope="space") -> navigateAll (setzt scope="all" wieder). Nach
  // G3 lässt der Home-Button den Scope auf "space" stehen, weil das, was der Nutzer
  // sehen soll, jetzt `state.overview = true` macht (Spaces-Übersicht), nicht der
  // globale Modus. Wer diese Zeile später als toten Code entfernt, bricht den
  // Home-Knopf -- ohne den Reset bleibt `isGlobalScope()` true, und
  // `renderListSlot()` ruft nie `renderOverview()` auf.
  state.scope = "space";
  setCreateControlsPresent(activeSpaceWritable());
  showOverviewPane();
  renderRail();
  // Phase 8.6 Plan 2 Block G G4 (V128): Slot-schaltend rendern, nicht direkt die Liste.
  // Welche der beiden Ansichten (Übersicht vs. Item-Liste) sichtbar wird, entscheidet
  // `state.overview` -- nicht diese Funktion.
  renderListSlot();
}

function snapshotFromItem(item) {
  return {
    id: item.id, type: item.type, version: item.version,
    title: item.title, body: item.body, status: item.status,
    due: item.due, assignee: item.assignee || "",
    tags: item.tags.slice(), links: item.links.slice(),
    assets: (item.assets || []).slice(),
  };
}

// P7-A3 (V73): `assets` liefert `markdownToHtml()`s dritten Kontextschlüssel, damit ein
// entferntes Asset als Alt-Text statt als kaputtes `<img>` rendert.
function assetIdsOf(assets) {
  return (assets || []).map(function (a) { return a.id; });
}

// Phase 8 Block B Step B4 (Plan §3 B4): Link-Picker-Callback. Hängt eine `itm_…`-ID an
// `#field-links` an (Komma-Konvention). Dedupliziert nicht — wer dieselbe ID zweimal
// verlinken will, kann das bewusst tun, und der Server akzeptiert es ohnehin (Phase-6-
// Spezifikation: `links` ist `list[str]`). Die Alphabet-Prüfung ist eine harte Garantie,
// dass der Picker-Callback nichts in das Feld schreibt, was nicht durch `links: ITEM_REF_RE`
// als Frontmatter-Kante akzeptiert würde — Defense-in-Depth gegen einen faulen Aufrufer.
function _appendLinkId(id) {
  if (!/^itm_[0-9a-f]{8}$/.test(id)) return;
  var current = fieldLinksEl.value
    .split(",").map(function (s) { return s.trim(); }).filter(Boolean);
  current.push(id);
  fieldLinksEl.value = current.join(", ");
}

// Phase 8.5 A1 (P8.5-I): `insertAtCursor` aus `init()` auf Modulebene gehoben, damit der
// Picker-Callback (`_onLinkPicked`) ihn auch ausserhalb von `init()` erreichen kann.
// Koerper unveraendert -- schliesst ueber nichts aus `init()`, `textarea` ist Parameter.
// Alle Alt-Aufrufstellen innerhalb von `init()` (Bild-Knopf, Zeile ~632) sehen die
// Modulebene ebenfalls, function-Deklarationen sind gehoistet.
function insertAtCursor(textarea, text) {
  // P10.5, Block 11, Schritt 11.3 (ED-1): im Live-Editor ersetzt CodeMirror die Auswahl
  // (`replaceSelection`) -- der Cursor bleibt hinter dem eingefuegten Text stehen, wie in der
  // Textarea. **Der Aufrufer uebergibt die Textarea weiterhin**, damit der Notausgang
  // (ED-5) unveraendert funktioniert.
  if (cm) {
    cm.replaceSelection(text);
    cm.focus();
    return;
  }
  var start = textarea.selectionStart;
  var end = textarea.selectionEnd;
  var value = textarea.value;
  textarea.value = value.slice(0, start) + text + value.slice(end);
  var pos = start + text.length;
  textarea.selectionStart = textarea.selectionEnd = pos;
  textarea.focus();
  textarea.dispatchEvent(new Event("input", { bubbles: true }));
}

// Phase 8.5 A1 (P8.5-H): Body-Variante des Link-Pickers. Erzeugt einen klickbaren Markdown-
// Link `[<Titel>](#item/<id>)` an der Cursorposition. Die `itm_`-ID darin ist gleichzeitig
// eine Graph-Kante (`storage/linkscan.py` matcht sie im Body, `#item/`-Praefix eingeschlossen
// -- Plan §0.3-Verweis). Deshalb ist im sichtbaren Fall ein zusaetzlicher Eintrag in `links:`
// redundant.
function _linkTextFor(title) {
  var t = (title || "").replace(/\s+/g, " ").trim();
  if (!t) return "";
  // Eckige Klammern im Titel maskiert -- ein Titel wie `Notiz [Entwurf]` wuerde den
  // Markdown-Link sonst zerreissen. Rueckgabe leerer String signalisiert "kein Titel".
  return t.replace(/([\[\]])/g, "\\$1");
}

function _appendLinkMarkdown(title, id) {
  if (!/^itm_[0-9a-f]{8}$/.test(id)) return;
  var label = _linkTextFor(title);
  if (!label) label = id;  // kein Titel verfuegbar -> ID als sichtbarer Text (selten, aber
                            // moeglich: API liefert irgendwann ein Item ohne Titel)
  insertAtCursor(editorTextareaEl, "[" + label + "](#item/" + id + ")");
}

// Phase 8.5 A1: Modus-Router des Picker-Callbacks. `dialogs.js` ruft diesen mit dem vom
// Nutzer gewaehlten Modus; die ID landet entweder im Frontmatter (`links:`) oder als
// Markdown-Link im Body. `picked` ist `{id, title, mode}` aus `dialogs.js`.
function _onLinkPicked(picked) {
  if (!picked || typeof picked.id !== "string") return;
  if (picked.mode === "frontmatter") _appendLinkId(picked.id);
  else _appendLinkMarkdown(picked.title, picked.id);
}

// -- Der Text des Editors (P10.5, Block 11, Schritt 11.3 — ED-1/ED-5) ----------------------
//
// **Ein Zugriff, eine Quelle.** Vor dem Live-Editor gab es nur die Textarea; jetzt trägt
// der Live-Editor (CodeMirror) den Text, und die Textarea ist der **Notausgang** (ED-5).
// Wer direkt `editorTextareaEl.value` liest, liest im Live-Modus den **alten** Text --
// deshalb gehen alle Zugriffe ueber diese zwei Funktionen.
//
// `getBody()` liest, `setBody(text)` schreibt. Ist der Editor nicht ladbar, bleibt die
// Textarea die Quelle -- der Rohmodus ist kein halber Editor, sondern ein vollwertiger.

export function getBody() {
  if (cm) return cm.getValue();
  return editorTextareaEl ? editorTextareaEl.value : "";
}

export function setBody(text) {
  if (cm) {
    // P10.5, Block 11, Schritt 11.4: `setValue` **ersetzt das ganze Dokument** -- und die
    // Zeilenklassen haengen am Dokument, nicht am Editor. Die Cursorzeile verliert dabei
    // ihre Markierung (`sfx-active-line`), ohne dass CM5 ein `cursorActivity` feuert: der
    // Cursor steht danach auf Zeile 0, `cmCursorZeile` steht auch auf 0, und die
    // Kurzpruefung in `_cursorZeileSetzen()` haelt die alte (falsche) Meinung.
    //
    // **Gemessen am 2026-10-24 an der Wegwerf-Instanz:** nach dem Wechsel auf ein zweites
    // Item war **keine** Zeile mehr mit `sfx-active-line` markiert -- die Formatierungszeichen
    // der Cursorzeile blieben unsichtbar (der Gegenlauf der Probe bricht genau diese Zellen:
    // `cursorzeile_markiert`, `cursorzeile_markiert_nach_zurueck`,
    // `formatierung_auf_der_cursorzeile_sichtbar`).
    // Deshalb: den Marker-Zustand **vor** dem `setValue` zuruecksetzen und danach neu setzen.
    cmCursorZeile = null;
    cm.setValue(text);
    _cursorZeileSetzen();
    return;
  }
  if (editorTextareaEl) editorTextareaEl.value = text;
}

// Text und Auswahl, unabhaengig vom Editor (Formatierhilfen, Einfuegen an der Cursorposition).
function _textUndAuswahl() {
  if (cm) {
    var von = cm.getCursor("from");
    var bis = cm.getCursor("to");
    return {
      text: cm.getValue(),
      start: cm.indexFromPos(von),
      end: cm.indexFromPos(bis),
    };
  }
  return {
    text: editorTextareaEl.value,
    start: editorTextareaEl.selectionStart,
    end: editorTextareaEl.selectionEnd,
  };
}

// Ersetzt einen Textbereich und setzt die Auswahl danach. **Dieselbe Wirkung in beiden
// Editoren** -- der Notausgang (Textarea) verhaelt sich wie der Live-Editor.
function _ersetze(start, end, neuerText, auswahlStart, auswahlEnde) {
  if (start > end) {
    var tausch = start; start = end; end = tausch;
  }
  if (cm) {
    cm.replaceRange(neuerText, cm.posFromIndex(start), cm.posFromIndex(end));
    cm.setSelection(cm.posFromIndex(auswahlStart), cm.posFromIndex(auswahlEnde));
    cm.focus();
    return;
  }
  var wert = editorTextareaEl.value;
  editorTextareaEl.value = wert.slice(0, start) + neuerText + wert.slice(end);
  editorTextareaEl.selectionStart = editorTextareaEl.selectionEnd = auswahlStart;
  editorTextareaEl.focus();
  editorTextareaEl.dispatchEvent(new Event("input", { bubbles: true }));
}

export function currentFormValues() {
  return {
    title: fieldTitleEl.value,
    body: getBody(),
    status: fieldStatusEl.value,
    due: fieldDueEl.value || null,
    // P9 Block trace: getrimmt, weil `_coerce_assignee()` den Wert ebenfalls `.strip()`t —
    // sonst waere "  niklas " vs. "niklas" ein Dauer-Ungespeichert-Zustand ohne Aenderung.
    assignee: fieldAssigneeEl.value.trim(),
    tags: fieldTagsEl.value.split(",").map(function (s) { return s.trim(); }).filter(Boolean),
    links: fieldLinksEl.value.split(",").map(function (s) { return s.trim(); }).filter(Boolean),
  };
}

// [P10.5, Block 10, Schritt 10.3 -- LG-2/P10.5-S] `export`, weil der Realtime-Client
// entscheiden muss, ob er den Editor ueberschreiben darf: ein **geaenderter** Editor wird
// nie ueberschrieben (P10.5-S), ein sauberer schon.
export function isDirty() {
  if (!state.editingSnapshot) return false;
  var current = currentFormValues();
  var snap = state.editingSnapshot;
  return current.title !== snap.title
    || current.body !== snap.body
    || current.status !== snap.status
    || (current.due || "") !== (snap.due || "")
    || current.assignee !== (snap.assignee || "")
    || current.tags.join(",") !== snap.tags.join(",")
    || current.links.join(",") !== snap.links.join(",");
}

function renderMetaDigest() {
  var v = currentFormValues();
  var parts = [v.status];
  if (v.assignee) parts.push("bei " + v.assignee);
  if (v.due) parts.push("fällig " + v.due);
  if (v.tags.length) parts.push(v.tags.join(", "));
  metaDigestEl.textContent = parts.join(" · ");
}

export function updateVersionBand() {
  versionBandEl.classList.remove("is-dirty", "is-conflict");
  if (!state.editingSnapshot) {
    versionBandNumberEl.textContent = "";
    editorVersionEl.textContent = "";
    saveButtonEl.disabled = true;
    return;
  }
  var dirty = isDirty();
  // Der Kern des V10-Fundes: ohne echte Änderung gibt es nichts zu speichern, und ein Klick
  // darf die Version nicht hochzählen.
  saveButtonEl.disabled = !dirty;
  if (state.conflictCurrent) {
    versionBandEl.classList.add("is-conflict");
    versionBandNumberEl.textContent = "v" + state.editingSnapshot.version + " → v" + state.conflictCurrent.version;  // P8-C2 Audit: "→" hier ist Sprach-Interpunktion ("Version X wird zu Y"), kein Icon
    editorVersionEl.textContent = "Konflikt";
  } else if (dirty) {
    versionBandEl.classList.add("is-dirty");
    versionBandNumberEl.textContent = "v" + state.editingSnapshot.version + "+";
    editorVersionEl.textContent = "ungespeichert";
  } else {
    versionBandNumberEl.textContent = "v" + state.editingSnapshot.version;
    editorVersionEl.textContent = "v" + state.editingSnapshot.version + " gespeichert";
  }
  renderMetaDigest();
}

// -- Entwurfsschutz (§4.5): sessionStorage, nie localStorage, nur für den eigenen Tab und
// nur für Items, die man gerade bearbeitet (nicht für fremde/schreibgeschützte Items — die
// haben keinen Editor).

function draftKeyFor(id) { return "sfx:draft:" + id; }

function saveDraft() {
  if (!state.selectedId) return;
  sessionStorage.setItem(draftKeyFor(state.selectedId), JSON.stringify(currentFormValues()));
}

export function clearDraft(id) {
  sessionStorage.removeItem(draftKeyFor(id));
}

function loadDraftIfAny(id) {
  var raw = sessionStorage.getItem(draftKeyFor(id));
  if (!raw) return null;
  try { return JSON.parse(raw); } catch (e) { return null; }
}

function populateStatusSelect(itemType) {
  fieldStatusEl.textContent = "";
  ((state.meta && state.meta.status_values[itemType]) || []).forEach(function (s) {
    var opt = document.createElement("option");
    opt.value = s;
    opt.textContent = s;
    fieldStatusEl.appendChild(opt);
  });
}

// P9 Block trace: die Vorschlagsliste hinter `#field-assignee`. Aus `state.spaces`, nicht aus
// einer eigenen Abfrage — es ist dieselbe Liste, die die Rail zeigt, damit "bei <Space>" immer
// einen Space nennt, den es gibt. **Vorschlag, keine Whitelist**: `assignee` ist ein freier
// Space-Name (V160, keine Pruefung gegen die Liste), und ein Feld, das einen vorhandenen Wert
// ablehnen wuerde, waere eine stille Datenverweigerung. Fremde Spaces stehen mit drin — sie sind
// sichtbar (`writable: false`) und genau die, die man in einem geteilten Space eintragen will.
function fillAssigneeOptions() {
  var list = document.getElementById("assignee-options");
  if (!list) return;
  list.textContent = "";
  state.spaces.forEach(function (space) {
    var opt = document.createElement("option");
    opt.value = space.name;
    list.appendChild(opt);
  });
}

// P9 Block trace: die Lesezeile "zuletzt geändert von X". Leer, wenn das Item das Feld nicht
// trägt — P9-AB (kein Backfill, kein erfundener Name) heißt hier: **keine Zeile**, nicht
// "zuletzt geändert von unbekannt". Das Datum kommt aus demselben Item, `updated_by` behauptet
// den Menschen dahinter.
function renderUpdatedByLine(item) {
  if (!metaUpdatedByEl) return;
  metaUpdatedByEl.textContent = item.updated_by
    ? "Zuletzt geändert von " + item.updated_by + " · " + (item.updated || "")
    : "";
}

// P10.5 Block 9 (RE-7): die Lesezeile "erstellt von X". Leer, wenn das Item das Feld nicht
// trägt — **kein Backfill** (Lock P10.5-W): ein Altbestand-Item zeigt hier nichts, und es wird
// auch nichts erfunden. Eine **eigene** Zeile, nicht eine zweite Angabe in der `updated_by`-Zeile:
// die beiden Aussagen beziehen sich auf verschiedene Zeitpunkte, und eine leere `created_by`
// (Altbestand) darf die `updated_by`-Zeile nicht verschlucken.
function renderCreatedByLine(item) {
  if (!metaCreatedByEl) return;
  metaCreatedByEl.textContent = item.created_by
    ? "Erstellt von " + item.created_by + " · " + (item.created || "")
    : "";
}

// P10.5, Block 11, Schritt 11.6 (ED-3): der **Overlay-Token** des Live-Editors.
//
// **Nur die Farbe.** Eine Groessen-Klasse aendert die Zeilenhoehe — und ein Editor, in dem
// die Zeilen springen, ist schlimmer als ein Editor, der die Groesse erst in der Vorschau
// zeigt. Die Ausrichtung ist ein **Block** und laesst sich im Fliesstext nicht faerben.
//
// Der Stream gehoert dem Overlay (CM5 faehrt Overlay und Modus auf **zwei** Streams) — der
// Zaehler `stream.pos` ist also der Overlay-eigene, nicht der des Markdown-Modus.
function _formatOverlayToken(stream) {
  // **Drei Stuecke**, stateless ueber Vorausschau und das Zeichen davor: `[` (Zeichen),
  // der Text (Farbe), `]{.rot}` (Zeichen). Die **Zeichen** tragen `formatting` — dieselbe
  // Klasse wie die Markdown-Zeichen, also blendet `app.css` sie auf den anderen Zeilen aus.
  // Eine **unbekannte** Klasse bleibt wörtlich (kein Stueck wird erkannt). Eine Groesse
  // allein faerbt nichts (sie wuerde die Zeilenhoehe aendern), nimmt dem Text aber die
  // Verweis-Optik des Markdown-Modus (`md-plain`).
  var V = FORMAT_VOKABULAR;
  function klasse(a, b) {
    var k = [a, b].filter(Boolean);
    for (var n = 0; n < k.length; n++) if (!V.farben[k[n]] && !V.groessen[k[n]]) return null;
    for (var f = 0; f < k.length; f++) if (V.farben[k[f]]) return V.farben[k[f]];
    return k.length ? "md-plain" : null;
  }
  var rest = stream.string.slice(stream.pos);
  var davor = stream.pos > 0 ? stream.string.charAt(stream.pos - 1) : "";
  if (stream.sol() && /^:::/.test(rest)) { stream.skipToEnd(); return "formatting"; }
  var m = /^\[([^\]\n]+)\]\{\.([a-z]+)(?: \.([a-z]+))?\}/.exec(rest);
  if (m && klasse(m[2], m[3])) {
    stream.next();                                   // das `[`
    return "formatting";
  }
  var am = /^([^\]\n]+)\]\{\.([a-z]+)(?: \.([a-z]+))?\}/.exec(rest);
  if (davor === "[" && am && klasse(am[2], am[3])) {
    stream.pos += am[1].length;                      // der Text
    return klasse(am[2], am[3]);
  }
  var zm = /^\]\{\.([a-z]+)(?: \.([a-z]+))?\}/.exec(rest);
  if (zm && klasse(zm[1], zm[2]) && /\[[^\]\n]+$/.test(stream.string.slice(0, stream.pos))) {
    stream.pos += zm[0].length;                      // `]{.rot}`
    return "formatting";
  }
  stream.next();
  return null;
}

// P10.5, Block 11, Schritt 11.3 (ED-1): der Live-Editor entsteht **beim Öffnen** eines
// Items, nicht beim Laden der Seite — der Erstaufruf bleibt ohne Editor (das Budget
// „Editor nachgeladen"). Bis der Editor da ist, trägt die **Textarea** den Text (der
// Notausgang, ED-5): der Mensch kann also sofort tippen, und der Editor übernimmt, sobald
// er geladen ist.
function _editorBereit() {
  if (cm || cmLaden) return;
  cmLaden = true;
  ensureCodeMirror().then(function (CodeMirror) {
    cmLaden = false;
    // **Nicht ladbar?** Dann bleibt die Textarea — der Rohmodus ist der Notausgang (ED-5).
    if (!CodeMirror || cm) return;
    // **Vor** `cm` gesetzt: `getBody()` liest ab dann den Editor, nicht mehr die Textarea.
    var text = editorTextareaEl.value;
    var cursor = editorTextareaEl.selectionStart;
    cm = CodeMirror.fromTextArea(editorTextareaEl, {
      mode: { name: "markdown", highlightFormatting: true },
      lineWrapping: true,
      lineNumbers: false,
      // Kein Faltbalken, keine Zeilennummern: die Flaeche gehoert dem Text.
      viewportMargin: 20,
    });
    cm.on("change", _editorGeaendert);
    // P10.5, Block 11, Schritt 11.5 (ED-2): die To-do-Kaestchen werden nach **jeder**
    // Aenderung neu bestimmt -- der Text ist die Quelle, das Kaestchen nur seine
    // Darstellung. Ein zweiter Zuhoer: `_editorGeaendert` rechnet Version und Entwurf,
    // dieser setzt die Kaestchen.
    cm.on("change", _todoMarkenAuffrischen);
    // P10.5, Block 11, Schritt 11.4 (ED-1): die **Cursorzeile** traegt die Klasse
    // `sfx-active-line` -- sie ist die Zeile, in der gerade geschrieben wird. Dort bleiben
    // auch die Formatierungszeichen sichtbar (s. `app.css`).
    cm.on("cursorActivity", function () { _cursorZeileSetzen(); });
    // P10.5, Block 11, Schritt 11.6 (ED-3): der **Overlay** — `[Text]{.rot}` faerbt sich
    // schon **beim Schreiben**, nicht erst in der Vorschau. Das ist der Unterschied
    // zwischen einem Format und einem Format, das man erst nach dem Speichern sieht.
    cm.addOverlay({ token: _formatOverlayToken });
    if (cm.getValue() !== text) cm.setValue(text);
    // Der Editor kann mitten im Tippen eintreffen — der Cursor bleibt, wo der Mensch war.
    try {
      cm.setCursor(cm.posFromIndex(cursor));
      cm.focus();
    } catch (err) { /* der Cursor ist kein Pfad */ }
    setRawMode(state.mode === "raw");
    // Die Cursorzeile von Anfang an markieren (CM feuert „cursorActivity" erst bei einer
    // Bewegung).
    _cursorZeileSetzen();
  });
}

// P10.5, Block 11, Schritt 11.4 (ED-1): die Cursorzeile markieren. **Nur eine** Klasse an
// **einer** Zeile -- sonst sammeln sich die Markierungen ueber die Sitzung.
function _cursorZeileSetzen() {
  if (!cm) return;
  var zeile = cm.getCursor().line;
  if (cmCursorZeile === zeile) return;
  if (cmCursorZeile !== null) {
    cm.removeLineClass(cmCursorZeile, "wrap", "sfx-active-line");
  }
  // **Der „wrap"-Layer**, nicht der „background"-Layer: nur der Wrap-Layer **enthaelt den
  // Text** -- der Background-Layer ist eine eigene Ebene hinter der Zeile (dort landet die
  // Klasse, ohne dass ein Nachfahr die Formatierungszeichen finden koennte). Gemessen am
  // 2026-10-24 im echten Browser (CM5 5.65.16): die Klasse sitzt am Wrap-Layer, und
  // `.sfx-active-line .cm-formatting` trifft die Formatierungszeichen der Cursorzeile.
  cm.addLineClass(zeile, "wrap", "sfx-active-line");
  cmCursorZeile = zeile;
}

// **Eine Aenderung, ein Ort:** der Live-Editor feuert „change", die Textarea feuert „input".
// Beides heisst dasselbe: Version neu rechnen und den Entwurf sichern.
function _editorGeaendert() {
  updateVersionBand();
  saveDraft();
}

// -- To-do-Kaestchen (P10.5, Block 11, Schritt 11.5 -- ED-2) ---------------------------------
//
// **Was der Plan verlangt:** `- [ ]`/`- [x]` am Zeilenanfang werden im Live-Modus per
// `cm.markText(..., {replacedWith: <checkbox>})` ersetzt; ein Klick schaltet **den Text im
// Puffer**. War der Editor **vor** dem Klick unveraendert, folgt sofort `saveItem()` (mit
// der Snapshot-`version`, Hard Rule 3; ein Konflikt oeffnet den bestehenden Dialog). War er
// **geaendert**, gehoert der Klick zur naechsten Speicherung.
//
// **Der Text ist die Quelle, das Kaestchen ist die Darstellung.** Im Dokument steht
// weiterhin `[ ]` — der Server bekommt Text, keine Sonderzeichen. Ein Kaestchen, das man
// anhaelt, ohne zu speichern, waere ein zweiter Zustand; genau den gibt es hier nicht.
//
// **Warum `atomic`:** der Cursor darf nicht **in** `[ ]` hinein — der Bereich ist ein
// Zeichen, kein Text. `atomic: true` sagt CodeMirror genau das.
var TODO_MUSTER = /^([ \t]*[-*+][ \t]+)\[([ xX])\]/;
//: Dieselbe Erkennung auf den **ganzen** Text — nur wenn irgendwo eine To-do-Zeile steht,
//: lohnt das Durchsuchen der Zeilen.
var TODO_VORHANDEN = /^[ \t]*[-*+][ \t]+\[[ xX]\]/m;

function _todoKasten(erledigt) {
  var kasten = document.createElement("input");
  kasten.type = "checkbox";
  kasten.checked = !!erledigt;
  kasten.className = "sfx-todo";
  kasten.title = erledigt ? "Erledigt — klicken zum Abhaken" : "Als erledigt markieren";
  // **Der Klick gehoert dem Kaestchen, nicht dem Editor.** CodeMirror hoert das `mousedown`
  // an der Huelle und setzt dort den Cursor — ohne `stopPropagation` wuerde der Klick den
  // Cursor versetzen und der Editor den Fokus bekommen; das Kaestchen wuerde nie angehakt.
  kasten.addEventListener("mousedown", function (e) {
    e.preventDefault();
    e.stopPropagation();
  });
  kasten.addEventListener("click", function (e) {
    e.preventDefault();
    e.stopPropagation();
    _todoUmschalten(kasten);
  });
  return kasten;
}

// Der Klick schaltet **den Text im Puffer** — `[ ]` und `[x]` wechseln sich ab. Danach
// entscheidet der Zustand **vor** dem Klick, ob gespeichert wird.
function _todoUmschalten(kasten) {
  if (!cm) return;
  var mark = kasten.sfxMark;
  var bereich = mark && mark.find();
  if (!bereich) return;                       // der Text passt nicht mehr (waehrend des Klicks?)
  var alt = cm.getRange(bereich.from, bereich.to);
  var neu = null;
  if (alt === "[ ]") neu = "[x]";
  else if (alt === "[x]" || alt === "[X]") neu = "[ ]";
  if (neu === null) return;
  // **Der Zustand VOR** dem Klick: `isDirty()` vergleicht mit dem Schnappschuss, und der
  // Klick hat den Text noch nicht geaendert — der Wert ist also der Zustand *vor* dem
  // Klick. War der Editor unveraendert, ist der Klick ein Schreibvorgang (Hard Rule 3:
  // mit der Version aus dem Schnappschuss). War er geaendert, gehoert der Klick zur
  // naechsten Speicherung: ein Klick ist dann nur Puffer.
  var sauber = !isDirty();
  cm.replaceRange(neu, bereich.from, bereich.to);
  if (sauber) saveItem();
}

// Die Kaestchen **bestimmen** — nach jeder Aenderung, weil der Text die Quelle ist.
//
// **Bestehende Marken, die noch passen, bleiben unangetastet.** Sie zu loeschen und neu zu
// setzen wuerde das Kaestchen neu aufbauen (Flackern) — und, schlimmer, den Cursor
// versetzen, wenn er direkt neben dem Kaestchen steht. Deshalb wird nur verglichen und nur
// bei Abweichung ersetzt.
function _todoMarkenAuffrischen() {
  if (!cm) return;
  var text = cm.getValue();
  var gewuenscht = [];
  // Der **Rohmodus** (ED-5) zeigt **jedes** Zeichen — also auch das `[ ]` eines To-dos.
  // Dann gibt es keine Kaestchen.
  if (state.mode !== "raw" && TODO_VORHANDEN.test(text)) {
    var zeilen = text.split("\n");
    for (var nr = 0; nr < zeilen.length; nr++) {
      var m = TODO_MUSTER.exec(zeilen[nr]);
      if (!m) continue;
      gewuenscht.push({
        von: { line: nr, ch: m[1].length },
        bis: { line: nr, ch: m[1].length + 3 },
        text: "[" + m[2] + "]",
        erledigt: m[2] !== " ",
      });
    }
  }
  var offen = cmTodoMarken.slice();
  cmTodoMarken = [];
  gewuenscht.forEach(function (wunsch) {
    var treffer = -1;
    for (var i = 0; i < offen.length; i++) {
      var eintrag = offen[i];
      var bereich = eintrag.mark.find();
      if (!bereich) continue;                 // die Marke ist nicht mehr im Dokument
      if (bereich.from.line === wunsch.von.line && bereich.from.ch === wunsch.von.ch
          && bereich.to.line === wunsch.bis.line && bereich.to.ch === wunsch.bis.ch
          && eintrag.text === wunsch.text) {
        treffer = i;
        break;
      }
    }
    if (treffer >= 0) {
      cmTodoMarken.push(offen.splice(treffer, 1)[0]);
      return;
    }
    var kasten = _todoKasten(wunsch.erledigt);
    var mark = cm.markText(wunsch.von, wunsch.bis, { replacedWith: kasten, atomic: true });
    kasten.sfxMark = mark;
    cmTodoMarken.push({ mark: mark, text: wunsch.text, kasten: kasten });
  });
  // Was uebrig bleibt, passt nicht mehr (der Text wurde geaendert) — aufraeumen.
  offen.forEach(function (eintrag) { eintrag.mark.clear(); });
}

// P10.5, Block 11, Schritt 11.3 (ED-1): **kein Moduswechsel mehr.** Vorher wechselte der
// Editor zwischen „Vorschau" (HTML) und „Bearbeiten" (Textarea) — der Wechsel war eine
// eigene Ansicht und damit ein Weg, auf dem ein ungespeicherter Text verloren gehen konnte.
// Jetzt ist der Editor **immer** der Live-Editor (CodeMirror mit Markdown-Hervorhebung); der
// Schalter heisst „Rohtext" und schaltet **innerhalb** desselben Editors zwischen der
// Live-Darstellung und dem **Rohtext** (ED-5: jedes Zeichen sichtbar).
//
// **Der Rohmodus ist kein halber Editor, sondern ein vollwertiger:** im Live-Editor heisst
// „Rohtext" nur, dass die Hervorhebung wegaellt — der Text bleibt derselbe, und im Notausgang
// (CM nicht ladbar) ist die Textarea ohnehin der Rohmodus.
function setRawMode(on) {
  state.mode = on ? "raw" : "live";
  if (cm) {
    // Ohne Modus faellt die Hervorhebung weg -- jede Zeile bleibt sichtbar (ED-5).
    cm.setOption("mode", on ? null : { name: "markdown", highlightFormatting: true });
    var huelle = cm.getWrapperElement();
    if (huelle) huelle.classList.toggle("is-raw", !!on);
  }
  // P10.5, Block 11, Schritt 11.5 (ED-5/ED-2): im Rohtext steht **jedes** Zeichen — also
  // auch das `[ ]` eines To-dos. Die Kaestchen werden abgeraeumt und beim Zurueckschalten
  // neu gesetzt.
  _todoMarkenAuffrischen();
  togglePreviewButtonEl.textContent = on ? "Live" : "Rohtext";
  togglePreviewButtonEl.setAttribute("aria-pressed", on ? "true" : "false");
  // Die Formatierhilfen bleiben **aktiv** (sie schreiben in den Puffer, in beiden Ansichten
  // gleich) — sie sind kein Vorschau-Feature, sondern ein Schreibbefehl.
}

// P7-A1: die ID ist eine interne Adresse, kein Anzeigename — deshalb nur als Kopierfeld, nie
// als Suchbegriff/Titelersatz beworben. Kein `execCommand`-Fallback: fehlt die Clipboard-API,
// bleibt der Text markierbar, das genügt (kein sicherheitsrelevanter Pfad).
function idChip(itemId) {
  var chip = el("button", "id-chip", itemId);
  chip.type = "button";
  chip.title = "ID kopieren";
  chip.addEventListener("click", function () {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(itemId).then(function () {
        toast("ID kopiert.");
      });
    }
  });
  return chip;
}

// P7-A3: kein neuer Serverpfad — `storage/store.py :: delete_asset()` verschiebt nach
// `_assets/<item_id>/_trash/`, löscht nie (N5 aus 6.5, Entscheidung H aus P1 bleibt
// unangetastet). Wortwahl deshalb "entfernen", nie "löschen".
function renderAssetStrip(item) {
  assetStripEl.textContent = "";
  var assets = item.assets || [];
  if (!assets.length) return;
  assets.forEach(function (asset) {
    var row = el("span", "asset-strip__item");
    row.appendChild(el("span", null, asset.filename || asset.id));
    var removeButton = el("button", "asset-strip__remove");
    removeButton.appendChild(iconSvg("x"));
    removeButton.type = "button";
    removeButton.title = "Bild entfernen";
    removeButton.addEventListener("click", function () {
      confirmDialog({
        title: "Bild entfernen",
        message: "Das Bild wird aus dem Dokument entfernt und in den Papierkorb des Items verschoben.",
        ok: "Entfernen",
      }).then(function (confirmed) {
        if (!confirmed) return;
        api("/items/" + encodeURIComponent(item.id) + "/assets/" + encodeURIComponent(asset.id), {
          method: "DELETE",
        }).then(function () {
          item.assets = item.assets.filter(function (a) { return a.id !== asset.id; });
          renderAssetStrip(item);
          toast("Bild entfernt.");
        }).catch(function (err) {
          toast(err.message || "Entfernen fehlgeschlagen.", "error");
        });
      });
    });
    row.appendChild(removeButton);
    assetStripEl.appendChild(row);
  });
}

function showReadonlyItem(item) {
  editorPart.detach();          // Akzeptanzkriterium 12
  // Beides zwingend, nicht kosmetisch (Advisor-Fund, siehe F7 im Session-Block): `hidden`
  // überlebt das Aushängen des Knotens, und der `Ctrl+S`-Wächter prüft genau dieses Flag
  // zusammen mit `editingSnapshot`. Ohne diese zwei Zeilen bliebe der Editor-Zustand des
  // ZULETZT geöffneten eigenen Items scharf, während rechts ein fremdes Item steht.
  detailEditorEl.hidden = true;
  state.editingSnapshot = null;
  // Phase 8.6 Plan 2 Block G G5: `overviewEl` heißt jetzt `graphPaneEl` -- das DOM-Element
  // heißt `#detail-graph` (vorher `#detail-overview`), referenziert aber nach dem Umzug
  // aus G2 nur noch die Karte, nicht die Spaces.
  graphPaneEl.hidden = true;
  detailReadonlyEl.hidden = false;
  roTitleEl.textContent = item.title;
  roMetaEl.textContent = "";
  roMetaEl.appendChild(el("span", "detail__badge-readonly", "Nur lesen — fremder Space (" + item.space + ")"));
  roMetaEl.appendChild(el("span", "tnum version-num", "v" + item.version));
  roMetaEl.appendChild(idChip(item.id));
  roMetaEl.appendChild(el("span", null, item.type + " · " + item.status));
  // P9 Block trace: dieselben beiden Angaben wie im Editor — fuer ein fremdes Item gibt es
  // kein Kopfdaten-Panel (der Editor wird da gar nicht erst angehaengt, Akzeptanzkriterium 12),
  // also waere die Meta-Zeile die einzige Stelle, an der man sie ueberhaupt sieht.
  if (item.assignee) roMetaEl.appendChild(el("span", null, "bei " + item.assignee));
  if (item.updated_by) {
    roMetaEl.appendChild(el("span", null, "zuletzt geändert von " + item.updated_by));
  }
  if (item.due) roMetaEl.appendChild(el("span", "tnum", "fällig " + item.due));
  roPreviewEl.innerHTML = markdownToHtml(item.body, {
    itemId: item.id, assetIds: assetIdsOf(item.assets),
  });
}

function showEditableItem(item, opts) {
  opts = opts || {};
  editorPart.attach();
  // Phase 8.6 Plan 2 Block G G5: dasselbe Element wie in showReadonlyItem (vorher
  // overviewEl). Wenn der Editor aufgeht, muss die Karte aus dem Detail-Slot verschwinden;
  // kommt sie zurück (ESC), übernimmt das clearDetail() via showOverviewPane().
  graphPaneEl.hidden = true;
  detailReadonlyEl.hidden = true;
  detailEditorEl.hidden = false;

  // P10.5-S: ein neu geoeffnetes Item hat keine fremde Aenderung -- das Band ist zuerst weg.
  hideChangedBanner();
  state.editingSnapshot = snapshotFromItem(item);
  metaItemIdEl.textContent = "";
  metaItemIdEl.appendChild(idChip(item.id));
  renderAssetStrip(state.editingSnapshot);
  fieldTitleEl.value = item.title;
  populateStatusSelect(item.type);
  fieldStatusEl.value = item.status;
  fieldDueEl.value = item.due || "";
  fieldAssigneeEl.value = item.assignee || "";
  renderUpdatedByLine(item);
  renderCreatedByLine(item);
  fillAssigneeOptions();
  fieldTagsEl.value = item.tags.join(", ");
  fieldLinksEl.value = item.links.join(", ");
  // P10.5, Block 11, Schritt 11.3 (ED-1): der **Live-Editor** trägt den Text — vor dem
  // Laden des Editors die Textarea (der Notausgang, ED-5).
  _editorBereit();
  setBody(item.body);

  // **Die Vorgabe beim Öffnen ist der Live-Modus** (Plan §Block 11, Schritt 11.3): es gibt
  // keinen Moduswechsel mehr, also beginnt der Editor in der Live-Darstellung. `opts.mode`
  // darf den **Rohmodus** verlangen ("raw") — das tut derzeit niemand, aber der Pfad ist
  // derselbe wie für "live" und damit nicht zukunftsblind.
  setRawMode(opts.mode === "raw");

  var draft = loadDraftIfAny(item.id);
  if (draft && (draft.title !== item.title || draft.body !== item.body)) {
    confirmDialog({
      title: "Ungespeicherter Entwurf",
      message: "Für dieses Item liegt ein ungespeicherter Entwurf in diesem Tab. Wiederherstellen?",
      ok: "Wiederherstellen",
    }).then(function (restore) {
      if (!restore) {
        clearDraft(item.id);
        return;
      }
      fieldTitleEl.value = draft.title;
      setBody(draft.body);
      fieldStatusEl.value = draft.status;
      fieldDueEl.value = draft.due || "";
      fieldAssigneeEl.value = draft.assignee || "";
      fieldTagsEl.value = draft.tags.join(", ");
      fieldLinksEl.value = draft.links.join(", ");
      updateVersionBand();
    });
  }
  updateVersionBand();
}

export function loadEditorFromItem(item, opts) {
  // P10.5 Block 7.3 (UI-3, V120): der Tab-Titel nennt das Item, das offen ist — auch im
  // Nur-Lesen-Fall (`showReadonlyItem`), denn der Titel folgt dem **Inhalt**, nicht der
  // Ansicht, in der er gerade steht.
  setViewTitle(item.title);
  state.selectedId = item.id;
  state.selectedReadonly = !!item.readonly;
  state.conflictCurrent = null;
  conflictDialogEl.hidden = true;

  if (item.readonly) showReadonlyItem(item);
  else showEditableItem(item, opts);

  shellEl.dataset.view = "detail";
  renderRail();
  // Phase 8.6 Plan 2 Block G G4 (V128): Slot-schaltend rendern, nicht direkt die Liste.
  // Bleibt der Nutzer im Listen-Modus (state.overview === false), aktualisiert das die
  // aria-current-Markierung; ist er im Übersichts-Modus (kommt per Klick aus einem
  // Recent-Item), wird der Listen-Slot auf die Item-Liste des Ziels umgeschaltet.
  renderListSlot();
}

export function selectItem(id) {
  state.selectedId = id;
  // Phase 8.6 Plan 2 Block G G4 (V128): Slot-schaltend rendern.
  renderListSlot();
  // P10.5, Block 4 (2026-10-22, Z4): der Ladezustand ab 200 ms. Der Abruf holt das Item,
  // der Slot zeigt bis dahin den vorigen Stand — ohne Geruest sieht das aus wie ein Hanger.
  return withLoading(detailEl, api("/items/" + encodeURIComponent(id))).then(function (item) {
    return loadEditorFromItem(item);
  });
}

// -- Editor schließen (Meldung des Nikingers: der Editor blieb "immer" offen) ----------------

export function closeEditor() {
  if (!isDirty()) {
    clearDetail();
    return Promise.resolve(true);
  }
  return confirmDialog({
    title: "Ungespeicherte Änderungen",
    message: "Der Editor enthält Änderungen, die noch nicht gespeichert sind. Verwerfen?",
    ok: "Verwerfen",
  }).then(function (discard) {
    if (!discard) return false;
    clearDraft(state.selectedId);
    clearDetail();
    return true;
  });
}

// -- Speichern / Konflikt (§4.5, Akzeptanzkriterium 11) ------------------------------------

// Nach jedem Schreibvorgang: Liste neu laden (Reihenfolge/Zugehörigkeit kann sich geändert
// haben) UND die Zähler im Baum, sonst zeigt die Navigation Zahlen von vorhin.
export function afterWrite(item, message) {
  clearDraft(item.id);
  // Modus VOR dem Neuladen einfangen: showEditableItem()s Vorgabe ist seit dem
  // Vorschau-Default "preview", ein Schreibvorgang mitten im Tippen soll aber nicht aus dem
  // Editor reißen — wer gerade bearbeitet, bleibt beim Bearbeiten.
  var mode = state.mode;
  return loadItems()
    .then(loadOverview)
    .then(function () {
      loadEditorFromItem(item, { mode: mode });
      toast(message);
    });
}

// -- Fremde Aenderung waehrend des Editierens (P10.5, Block 10, Schritt 10.3 -- P10.5-S) -------
//
// **Die Regel: ein geaenderter Editor wird nie ueberschrieben.** Wer tippt, hat eine
// aeltere Version des Items offen; ein fremder Write hebt sie nicht auf. Hard Rule 3 (kein
// Write ohne `version`) macht den Konflikt sichtbar -- das Speichern mit der alten Version
// laeuft in den Konfliktdialog, wie heute. Der Server meldet nur, dass sich etwas
// geaendert hat; **die Entscheidung trifft der Mensch**.

export function showChangedBanner(item) {
  if (!changedBannerEl) return;
  changedBannerEl.dataset.itemId = item.id;
  var von = item.updated_by ? ("Geaendert von " + item.updated_by) : "Geaendert";
  changedBannerTextEl.textContent = von + " \u2014 neu laden?";
  changedBannerEl.hidden = false;
}

export function hideChangedBanner() {
  if (!changedBannerEl) return;
  changedBannerEl.hidden = true;
  changedBannerEl.dataset.itemId = "";
}

// Der Serverstand ist neuer als der angezeigte: **Inhalt und Version zusammen** uebernehmen
// (sonst zeigte der Editor eine Version, die es nicht gibt). Der Entwurf wird verworfen --
// der Editor war sauber, der Entwurf kann also nichts Neues enthalten.
export function reloadFromServer(item) {
  clearDraft(item.id);
  hideChangedBanner();
  var mode = state.mode;
  loadEditorFromItem(item, { mode: mode });
}

export function handleWriteError(err, fallback) {
  if (err.code === "conflict" && err.detail && err.detail.current) {
    showConflictDialog(err.detail.current);
    return;
  }
  if (err.message === "unauthenticated") return;
  toast(err.message || fallback, "error");
}

// Jeder Schreibvorgang adressiert das Item über `state.editingSnapshot.id`, NIE über
// `state.selectedId` (Advisor-Fund, F7 im Session-Block): `selectItem()` setzt `selectedId`
// sofort, `editingSnapshot` erst wenn die Antwort da ist. Zwischen beidem liegt ein Fenster, in
// dem `selectedId` schon auf Item B zeigt, während Version und Formularwerte noch zu Item A
// gehören — ein `Ctrl+S` in diesem Moment schriebe A's Inhalt unter B's Kennung, und wenn beide
// Versionen zufällig gleich sind, ohne Konflikt. Das ist genau der stille Überschreiber, den
// Hard Rule 3 verbietet, nur eben clientseitig herbeigeführt. Über den Schnappschuss adressiert
// stammen Kennung und Version beweisbar aus demselben Lesevorgang.
export function saveItem() {
  if (!state.editingSnapshot || !isDirty()) return Promise.resolve();
  var payload = Object.assign(
    { version: state.editingSnapshot.version, format: "markdown" }, currentFormValues()
  );
  return api("/items/" + encodeURIComponent(state.editingSnapshot.id), {
    method: "PATCH", body: JSON.stringify(payload),
  }).then(function (item) {
    return afterWrite(item, "Gespeichert · v" + item.version);
  }).catch(function (err) {
    handleWriteError(err, "Speichern fehlgeschlagen.");
  });
}

export function init() {
  shellEl = document.getElementById("shell");
  detailEl = document.getElementById("detail");
  // Phase 8.6 Plan 2 Block G G5: `#detail-overview` (Block-C-Name) wurde in G2 zu
  // `#list-overview` (im Listen-Slot) und `#detail-graph` (im Detail-Slot, die Karte).
  // `graphPaneEl` ist die Karte, weil das, was `showOverviewPane()` zeigt, seit G5
  // nur noch sie ist.
  graphPaneEl = document.getElementById("detail-graph");

  detailReadonlyEl = document.getElementById("detail-readonly");
  roTitleEl = document.getElementById("ro-title");
  roMetaEl = document.getElementById("ro-meta");
  roPreviewEl = document.getElementById("ro-preview");
  roCloseButtonEl = document.getElementById("ro-close-button");

  detailEditorEl = document.getElementById("detail-editor");
  editorVersionEl = document.getElementById("editor-version");
  versionBandEl = document.getElementById("version-band");
  versionBandNumberEl = document.getElementById("version-band-number");
  metaPanelEl = document.getElementById("meta-panel");
  metaDigestEl = document.getElementById("meta-digest");
  metaItemIdEl = document.getElementById("meta-item-id");
  fieldTitleEl = document.getElementById("field-title");
  fieldStatusEl = document.getElementById("field-status");
  fieldDueEl = document.getElementById("field-due");
  fieldAssigneeEl = document.getElementById("field-assignee");
  metaUpdatedByEl = document.getElementById("meta-updated-by");
  metaCreatedByEl = document.getElementById("meta-created-by");
  fieldTagsEl = document.getElementById("field-tags");
  fieldLinksEl = document.getElementById("field-links");
  editorToolbarEl = document.getElementById("editor-toolbar");
  togglePreviewButtonEl = document.getElementById("toggle-preview");
  editorTextareaEl = document.getElementById("editor-textarea");
  editorPreviewEl = document.getElementById("editor-preview");
  saveButtonEl = document.getElementById("save-button");
  archiveButtonEl = document.getElementById("archive-button");
  closeButtonEl = document.getElementById("close-button");
  appendInputEl = document.getElementById("append-input");
  appendButtonEl = document.getElementById("append-button");
  conflictDialogEl = document.getElementById("conflict-dialog");
  insertImageButtonEl = document.getElementById("insert-image-button");
  insertImageInputEl = document.getElementById("insert-image-input");
  assetStripEl = document.getElementById("asset-strip");
  linkPickerButtonEl = document.getElementById("link-picker-button");
  changedBannerEl = document.getElementById("editor-changed");
  changedBannerTextEl = document.getElementById("editor-changed-text");
  changedReloadButtonEl = document.getElementById("editor-changed-reload");
  changedCloseButtonEl = document.getElementById("editor-changed-close");

  closeButtonEl.addEventListener("click", function () { closeEditor(); });

  // -- Hinweisband (P10.5-S): das Item wurde von aussen geaendert, waehrend der Editor
  // ungespeicherte Aenderungen traegt. **Nichts wird ueberschrieben** -- der Knopf laedt
  // den Serverstand erst auf ausdruecklichen Wunsch, und dann mit Rueckfrage (die
  // ungespeicherten Aenderungen gehen dabei verloren).
  if (changedReloadButtonEl) {
    changedReloadButtonEl.addEventListener("click", function () {
      var id = changedBannerEl && changedBannerEl.dataset.itemId;
      if (!id) return;
      confirmDialog({
        title: "Neu laden",
        message: "Die ungespeicherten Aenderungen in diesem Editor gehen verloren. "
          + "Der Serverstand wird geladen.",
        ok: "Neu laden",
      }).then(function (ok) {
        if (!ok) return;
        return api("/items/" + encodeURIComponent(id)).then(function (item) {
          reloadFromServer(item);
          toast("Neu geladen \u00b7 v" + item.version);
        }).catch(reportUnexpectedError);
      });
    });
  }
  if (changedCloseButtonEl) {
    changedCloseButtonEl.addEventListener("click", function () { hideChangedBanner(); });
  }

  // Phase 8 Block B Step B4 (Plan §3 B4) + Phase 8.5 A1: Link-Picker-Knopf öffnet den Dialog;
  // der Callback routet je nach gewaehltem Modus (`body` / `frontmatter`) den Treffer entweder
  // als `[Titel](#item/itm_…)` an die Cursorposition oder als `itm_…`-ID in `#field-links`
  // (Komma-Konvention, kein API-Umbau). Idempotent: derselbe Picker laesst sich mehrfach
  // oeffnen; die Moduswahl ueberlebt das in `localStorage`.
  linkPickerButtonEl.addEventListener("click", function () {
    openLinkPicker({ onPick: _onLinkPicked });
  });

  // Nur-lesen-Ansicht (fremdes Item): kein `editingSnapshot`, also nichts Ungespeichertes —
  // schließt ohne Rückfrage, anders als `closeEditor()`.
  roCloseButtonEl.addEventListener("click", function () { clearDetail(); });

  saveButtonEl.addEventListener("click", function () { saveItem(); });

  // -- Anhängen (eigener Pfad, nicht über PATCH) ----------------------------------------------

  appendButtonEl.addEventListener("click", function () {
    var text = appendInputEl.value.trim();
    if (!text || !state.editingSnapshot) return;
    api("/items/" + encodeURIComponent(state.editingSnapshot.id) + "/append", {
      method: "POST", body: JSON.stringify({ version: state.editingSnapshot.version, text: text }),
    }).then(function (item) {
      appendInputEl.value = "";
      return afterWrite(item, "Angehängt · v" + item.version);
    }).catch(function (err) {
      handleWriteError(err, "Anhängen fehlgeschlagen.");
    });
  });

  // -- Archivieren -----------------------------------------------------------------------------

  archiveButtonEl.addEventListener("click", function () {
    if (!state.editingSnapshot) return;
    confirmDialog({
      title: "Archivieren",
      message: "Das Item wandert ins Archiv. Gelöscht wird nichts — du findest es unter „Archiv“ wieder.",
      ok: "Archivieren",
    }).then(function (ok) {
      if (!ok) return;
      return api("/items/" + encodeURIComponent(state.editingSnapshot.id) + "/archive", {
        method: "POST", body: JSON.stringify({ version: state.editingSnapshot.version }),
      }).then(function (item) {
        // Nach dem Archivieren blieb das Item bis Step 7b im Editor stehen, obwohl es aus der
        // Liste verschwunden war — der Editor zeigte etwas, das daneben nicht mehr existierte.
        clearDraft(item.id);
        state.editingSnapshot = null;
        return loadItems().then(loadOverview).then(function () {
          clearDetail();
          toast("Archiviert · " + item.title);
        });
      }).catch(function (err) {
        handleWriteError(err, "Archivieren fehlgeschlagen.");
      });
    });
  });

  // -- Formatierhilfen (P5-U: fügt Markdown-Syntax in die Textarea ein, kein `execCommand`,
  // kein WYSIWYG) -----------------------------------------------------------------------------

  // P10.5, Block 11, Schritt 11.3 (ED-1): die Formatierhilfen arbeiten ueber
  // `_textUndAuswahl()`/`_ersetze()` — damit wirken sie im Live-Editor (CodeMirror) **und**
  // im Notausgang (Textarea) gleich. Der Code ist damit **einer**, nicht zweier.
  function wrapSelection(marker) {
    var a = _textUndAuswahl();
    var gewaehlt = a.text.slice(a.start, a.end);
    _ersetze(a.start, a.end, marker + gewaehlt + marker,
             a.start + marker.length, a.start + marker.length + gewaehlt.length);
  }

  function insertLinePrefix(prefix) {
    var a = _textUndAuswahl();
    var lineStart = a.text.lastIndexOf("\n", a.start - 1) + 1;
    _ersetze(lineStart, lineStart, prefix, a.start + prefix.length, a.start + prefix.length);
  }

  var TOOLBAR_ACTIONS = {
    bold: function () { wrapSelection("**"); },
    italic: function () { wrapSelection("*"); },
    code: function () { wrapSelection("`"); },
    h: function () { insertLinePrefix("## "); },
    quote: function () { insertLinePrefix("> "); },
    ul: function () { insertLinePrefix("- "); },
    ol: function () { insertLinePrefix("1. "); },
    hr: function () {
      var a = _textUndAuswahl();
      var before = a.text.slice(0, a.start);
      var prefix = before === "" || before.charAt(before.length - 1) === "\n" ? "" : "\n";
      _ersetze(a.start, a.start, prefix + "\n---\n\n", a.start, a.start);
    },
    link: function () {
      // Platzhalter statt einer echten URL-Vorlage — ein Schema-Präfix im Quelltext würde
      // `test_app_js_makes_no_external_requests` als externe Referenz auffassen; ein
      // Platzhalter-Wort ist ohnehin klarer als eine Vorlage, die wie ein echter Link aussieht.
      var a = _textUndAuswahl();
      var selected = a.text.slice(a.start, a.end) || "Linktext";
      var url = "Ziel-URL";
      var snippet = "[" + selected + "](" + url + ")";
      var urlStart = a.start + selected.length + 3;
      _ersetze(a.start, a.end, snippet, urlStart, urlStart + url.length);
    },
  };

  Array.prototype.forEach.call(editorToolbarEl.querySelectorAll("[data-md]"), function (button) {
    button.addEventListener("click", function () {
      var action = TOOLBAR_ACTIONS[button.dataset.md];
      if (action) action();
    });
  });

  // P10.5, Block 11, Schritt 11.6 (ED-3): die **Format-Konvention** in der Werkzeugleiste.
  // Drei Felder: Farbe · Groesse · Ausrichtung. Die Farbe und die Groesse sind **Inline**
  // (`[Text]{.rot}`), die Ausrichtung ist ein **Block** (`::: {.zentriert}` … `:::`).
  //
  // **Die Form wird erkannt, nicht blind gesetzt.** Liegt die Auswahl in einer bereits
  // vorhandenen Form, wandert die neue Klasse **in dieselbe Form** (`[Text]{.rot .gross}`)
  // — ein Nesting (`[[Text]{.rot}]{.gross}`) waere nicht falsch, aber unlesbar und beim
  // Rendern kaputt (die Klammer-Regel laesst kein `]` im Text zu).
  var formatFarbeEl = document.getElementById("format-farbe");
  var formatGroesseEl = document.getElementById("format-groesse");
  var formatAusrichtungEl = document.getElementById("format-ausrichtung");

  function _formatFormFinden(text, start, end) {
    var muster = /\[([^\]\n]+)\]\{([^}]*)\}/g;
    var m;
    while ((m = muster.exec(text)) !== null) {
      var von = m.index;
      var bis = m.index + m[0].length;
      if (start >= von && end <= bis) {
        return {
          index: von,
          laenge: m[0].length,
          text: m[1],
          namen: m[2].trim().split(/\s+/).filter(Boolean).map(function (n) {
            return n.replace(/^\./, "");
          }),
        };
      }
    }
    return null;
  }

  function _formatKlassenSetzen(gruppe, wert) {
    var a = _textUndAuswahl();
    var form = _formatFormFinden(a.text, a.start, a.end);
    if (form) {
      // **Dieselbe Gruppe ersetzen, die andere behalten:** eine zweite Farbe ist nicht
      // erlaubt (der Renderer laesst sie wörtlich), eine Farbe plus eine Größe schon.
      var istFarbe = gruppe === "farben";
      var namen = form.namen.filter(function (n) {
        return istFarbe ? !(n in FORMAT_VOKABULAR.farben) : !(n in FORMAT_VOKABULAR.groessen);
      });
      namen.push(wert);
      var formText = "[" + form.text + "]{." + namen.join(" ") + "}";
      _ersetze(
        form.index, form.index + form.laenge, formText,
        form.index + 1, form.index + 1 + form.text.length
      );
      return;
    }
    var selected = a.text.slice(a.start, a.end) || "Text";
    var snippet = "[" + selected + "]{." + wert + "}";
    _ersetze(a.start, a.end, snippet, a.start + 1, a.start + 1 + selected.length);
  }

  function _formatAusrichtungSetzen(wert) {
    var a = _textUndAuswahl();
    var inhalt = a.text.slice(a.start, a.end);
    var block = "::: {." + wert + "}\n" + inhalt + "\n:::";
    // Der Cursor landet **im** Block — zwischen der oeffnenden und der schliessenden Zeile.
    _ersetze(
      a.start, a.end, block,
      a.start + ("::: {." + wert + "}\n").length,
      a.start + ("::: {." + wert + "}\n").length + inhalt.length
    );
  }

  if (formatFarbeEl) {
    formatFarbeEl.addEventListener("change", function () {
      var wert = formatFarbeEl.value;
      if (!wert) return;
      _formatKlassenSetzen("farben", wert);
      formatFarbeEl.value = "";
    });
  }
  if (formatGroesseEl) {
    formatGroesseEl.addEventListener("change", function () {
      var wert = formatGroesseEl.value;
      if (!wert) return;
      _formatKlassenSetzen("groessen", wert);
      formatGroesseEl.value = "";
    });
  }
  if (formatAusrichtungEl) {
    formatAusrichtungEl.addEventListener("change", function () {
      var wert = formatAusrichtungEl.value;
      if (!wert) return;
      _formatAusrichtungSetzen(wert);
      formatAusrichtungEl.value = "";
    });
  }

  // P10.5, Block 11, Schritt 11.3 (ED-1/ED-5): der Schalter heißt "Rohtext" und schaltet
  // **innerhalb** des Live-Editors zwischen Live-Darstellung und Rohtext (kein Moduswechsel
  // mehr — s. `setRawMode()`).
  togglePreviewButtonEl.addEventListener("click", function () {
    setRawMode(state.mode !== "raw");
  });

  // -- Bild einfügen (Block B Step B3, P6.5-J) — der Pflichtweg ist dieser Knopf, kein
  // Zwischenablage-/Drag&Drop-Einfügen (P6-AB gilt sinngemäß fort, dieselbe Regel wie bei
  // Ordner-Verschieben). Roh-Upload wie `webui/api.py`s Route ihn erwartet, kein Multipart.
  insertImageButtonEl.addEventListener("click", function () {
    if (!state.editingSnapshot) return;
    insertImageInputEl.value = "";
    insertImageInputEl.click();
  });

  insertImageInputEl.addEventListener("change", function () {
    var file = insertImageInputEl.files[0];
    if (!file || !state.editingSnapshot) return;
    var itemId = state.editingSnapshot.id;
    api("/items/" + encodeURIComponent(itemId) + "/assets", {
      method: "POST", body: file, headers: { "Content-Type": "application/octet-stream" },
    }).then(function (asset) {
      state.editingSnapshot.assets.push(asset);
      renderAssetStrip(state.editingSnapshot);
      insertAtCursor(editorTextareaEl, "![" + (file.name || "Bild") + "](asset:" + asset.id + ")");
    }).catch(function (err) {
      toast(err.message || "Bild-Upload fehlgeschlagen.", "error");
    });
  });

  // P9 Block trace, Lock P9-Z — der Client fuellt `assignee`, der Server niemals. Dem Server
  // Bedeutung zu geben ("in Arbeit heisst: X arbeitet daran") waere genau die Statussemantik, die
  // das Kernprinzip verbietet; der Server kennt Token → Space, nicht die Absicht eines
  // Menschen. Diese Regel steht deshalb in einem Client-Zweig — und in `_ASSIGNEE_HINT` fuer
  // das LLM, damit beide Clients dieselbe Regel haben.
  //
  // **Zwei Bedingungen, beide notwendig:**
  // 1. nur beim Wert `doing` — jeder andere Status fasst `assignee` nicht an,
  // 2. nur wenn das Feld **leer** ist — ein gesetzter Wert wird nie ueberschrieben (P9-Z
  //    woertlich: "Ein gesetztes assignee ueberschreibst du nur, wenn ein Mensch es
  //    ausdruecklich sagt"). Ohne diese zweite Bedingung wuerde jeder, der eine fremde
  //    Aufgabe in Arbeit zieht, sie sich selbst zuschreiben.
  //
  // **V184:** `state.ownSpace` ist in `app.js :: init()` gesetzt, bevor ueberhaupt eine Liste
  // geladen wird — der Editor kann also nicht ohne ihn offen sein. Der `!state.ownSpace`-Guard
  // steht trotzdem da: die Alternative waere ein `undefined` als Space-Name in einer
  // Nutzeroberflaeche, und die kostet nichts.
  fieldStatusEl.addEventListener("change", function () {
    if (fieldStatusEl.value !== "doing") return;
    if (fieldAssigneeEl.value.trim() !== "" || !state.ownSpace) return;
    fieldAssigneeEl.value = state.ownSpace;
    renderMetaDigest();
  });

  // P10.5, Block 11, Schritt 11.3 (ED-1): die Felder **und** die Textarea (der Notausgang)
  // melden ihre Aenderung ueber `_editorGeaendert()` — derselbe Ort wie beim Live-Editor
  // (CodeMirror feuert „change").
  [fieldTitleEl, fieldStatusEl, fieldDueEl, fieldAssigneeEl, fieldTagsEl, fieldLinksEl, editorTextareaEl].forEach(
    function (input) {
      input.addEventListener("input", _editorGeaendert);
      // `<select>`/`<input type=date>` feuern in manchen Browsern nur `change`, nicht `input`.
      input.addEventListener("change", _editorGeaendert);
    }
  );

  metaPanelEl.addEventListener("toggle", renderMetaDigest);
}
