"use strict";

// -- Detail: Nur-lesen (fremdes Item) vs. Editor (eigenes Item) -----------------------------

import { state, editorPart, activeSpaceWritable, setCreateControlsPresent } from "./state.js";
import { el, toast } from "./toasts.js";
import { api } from "./api.js";
import { markdownToHtml } from "./markdown.js";
import { loadItems, loadOverview, renderList } from "./list.js";
import { renderRail } from "./tree.js";
import { confirmDialog, showConflictDialog } from "./dialogs.js";

var shellEl;
var overviewEl;
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
var fieldTitleEl;
var fieldStatusEl;
var fieldDueEl;
var fieldTagsEl;
var fieldLinksEl;
var editorToolbarEl;
var togglePreviewButtonEl;
var editorTextareaEl;
var editorPreviewEl;
var saveButtonEl;
var archiveButtonEl;
var closeButtonEl;
var appendInputEl;
var appendButtonEl;
var conflictDialogEl;
var insertImageButtonEl;
var insertImageInputEl;

export function showOverviewPane() {
  overviewEl.hidden = false;
  detailReadonlyEl.hidden = true;
  detailEditorEl.hidden = true;
  editorPart.detach();
  shellEl.dataset.view = "list";
}

export function clearDetail() {
  state.selectedId = null;
  state.selectedReadonly = false;
  state.editingSnapshot = null;
  state.conflictCurrent = null;
  // Advisor-Fund vor dem Commit (GLOBAL_SEARCH_PLAN.md): ohne diesen Reset blieb
  // `state.scope === "all"` nach "Alle Items" -> Home stehen, `activeSpaceWritable()` gab dort
  // faelschlich `false` zurueck und liess den Anlegen-Knopf auf der eigenen, schreibbaren
  // Uebersicht ausgehaengt. Playwright-bestaetigt (Wegwerf-Instanz, kein Repo-Artefakt).
  state.scope = "space";
  setCreateControlsPresent(activeSpaceWritable());
  showOverviewPane();
  renderRail();
  renderList();
}

function snapshotFromItem(item) {
  return {
    id: item.id, type: item.type, version: item.version,
    title: item.title, body: item.body, status: item.status,
    due: item.due, tags: item.tags.slice(), links: item.links.slice(),
  };
}

export function currentFormValues() {
  return {
    title: fieldTitleEl.value,
    body: editorTextareaEl.value,
    status: fieldStatusEl.value,
    due: fieldDueEl.value || null,
    tags: fieldTagsEl.value.split(",").map(function (s) { return s.trim(); }).filter(Boolean),
    links: fieldLinksEl.value.split(",").map(function (s) { return s.trim(); }).filter(Boolean),
  };
}

function isDirty() {
  if (!state.editingSnapshot) return false;
  var current = currentFormValues();
  var snap = state.editingSnapshot;
  return current.title !== snap.title
    || current.body !== snap.body
    || current.status !== snap.status
    || (current.due || "") !== (snap.due || "")
    || current.tags.join(",") !== snap.tags.join(",")
    || current.links.join(",") !== snap.links.join(",");
}

function renderMetaDigest() {
  var v = currentFormValues();
  var parts = [v.status];
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
    versionBandNumberEl.textContent = "v" + state.editingSnapshot.version + " → v" + state.conflictCurrent.version;
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

function setEditorMode(mode) {
  state.mode = mode;
  editorTextareaEl.hidden = mode !== "edit";
  editorPreviewEl.hidden = mode !== "preview";
  togglePreviewButtonEl.textContent = mode === "edit" ? "Vorschau" : "Bearbeiten";
  // Die Formatierhilfen bleiben sichtbar (sie sitzen in derselben Leiste wie der
  // Vorschau-Umschalter), sind in der Vorschau aber deaktiviert — sonst würden sie unsichtbar
  // in die Textarea schreiben.
  Array.prototype.forEach.call(editorToolbarEl.querySelectorAll("[data-md]"), function (b) {
    b.disabled = mode !== "edit";
  });
  if (mode === "preview") {
    editorPreviewEl.innerHTML = markdownToHtml(
      editorTextareaEl.value, { itemId: state.editingSnapshot && state.editingSnapshot.id },
    );
  }
}

function showReadonlyItem(item) {
  editorPart.detach();          // Akzeptanzkriterium 12
  // Beides zwingend, nicht kosmetisch (Advisor-Fund, siehe F7 im Session-Block): `hidden`
  // überlebt das Aushängen des Knotens, und der `Ctrl+S`-Wächter prüft genau dieses Flag
  // zusammen mit `editingSnapshot`. Ohne diese zwei Zeilen bliebe der Editor-Zustand des
  // ZULETZT geöffneten eigenen Items scharf, während rechts ein fremdes Item steht.
  detailEditorEl.hidden = true;
  state.editingSnapshot = null;
  overviewEl.hidden = true;
  detailReadonlyEl.hidden = false;
  roTitleEl.textContent = item.title;
  roMetaEl.textContent = "";
  roMetaEl.appendChild(el("span", "detail__badge-readonly", "Nur lesen — fremder Space (" + item.space + ")"));
  roMetaEl.appendChild(el("span", "tnum version-num", "v" + item.version));
  roMetaEl.appendChild(el("span", null, item.type + " · " + item.status));
  if (item.due) roMetaEl.appendChild(el("span", "tnum", "fällig " + item.due));
  roPreviewEl.innerHTML = markdownToHtml(item.body, { itemId: item.id });
}

function showEditableItem(item, opts) {
  opts = opts || {};
  editorPart.attach();
  overviewEl.hidden = true;
  detailReadonlyEl.hidden = true;
  detailEditorEl.hidden = false;

  state.editingSnapshot = snapshotFromItem(item);
  fieldTitleEl.value = item.title;
  populateStatusSelect(item.type);
  fieldStatusEl.value = item.status;
  fieldDueEl.value = item.due || "";
  fieldTagsEl.value = item.tags.join(", ");
  fieldLinksEl.value = item.links.join(", ");
  editorTextareaEl.value = item.body;
  // Meldung des Nikingers: der Editor öffnete immer in der Bearbeiten-Ansicht, auch beim
  // bloßen Betrachten. Vorgabe jetzt "Vorschau" — außer `opts.mode` sagt etwas anderes:
  // ein frisch angelegtes Item (dialogs.js :: createSubmitButtonEl) will sofort tippen können
  // ("edit"), und ein Neuladen NACH einem Schreibvorgang (afterWrite/Konflikt) behält den
  // Modus bei, den man gerade benutzt hat, statt mitten im Tippen in die Vorschau zu springen.
  setEditorMode(opts.mode || "preview");

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
      editorTextareaEl.value = draft.body;
      fieldStatusEl.value = draft.status;
      fieldDueEl.value = draft.due || "";
      fieldTagsEl.value = draft.tags.join(", ");
      fieldLinksEl.value = draft.links.join(", ");
      updateVersionBand();
      // Advisor-Fund: `setEditorMode()` rendert die Vorschau nur BEIM WECHSEL nach "preview" —
      // stehen wir (Vorgabe seit diesem Fund) schon dort, während der Entwurf asynchron
      // ankommt, zeigte die Vorschau bis hierhin weiter den ALTEN, gespeicherten Text.
      if (state.mode === "preview") {
        editorPreviewEl.innerHTML = markdownToHtml(
      editorTextareaEl.value, { itemId: state.editingSnapshot && state.editingSnapshot.id },
    );
      }
    });
  }
  updateVersionBand();
}

export function loadEditorFromItem(item, opts) {
  state.selectedId = item.id;
  state.selectedReadonly = !!item.readonly;
  state.conflictCurrent = null;
  conflictDialogEl.hidden = true;

  if (item.readonly) showReadonlyItem(item);
  else showEditableItem(item, opts);

  shellEl.dataset.view = "detail";
  renderRail();
  renderList();
}

export function selectItem(id) {
  state.selectedId = id;
  renderList();
  return api("/items/" + encodeURIComponent(id)).then(function (item) {
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
  overviewEl = document.getElementById("detail-overview");

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
  fieldTitleEl = document.getElementById("field-title");
  fieldStatusEl = document.getElementById("field-status");
  fieldDueEl = document.getElementById("field-due");
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

  closeButtonEl.addEventListener("click", function () { closeEditor(); });

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

  function wrapSelection(textarea, marker) {
    var start = textarea.selectionStart;
    var end = textarea.selectionEnd;
    var value = textarea.value;
    var selected = value.slice(start, end);
    textarea.value = value.slice(0, start) + marker + selected + marker + value.slice(end);
    textarea.selectionStart = start + marker.length;
    textarea.selectionEnd = start + marker.length + selected.length;
    textarea.focus();
    textarea.dispatchEvent(new Event("input", { bubbles: true }));
  }

  function insertAtCursor(textarea, text) {
    var start = textarea.selectionStart;
    var end = textarea.selectionEnd;
    var value = textarea.value;
    textarea.value = value.slice(0, start) + text + value.slice(end);
    var pos = start + text.length;
    textarea.selectionStart = textarea.selectionEnd = pos;
    textarea.focus();
    textarea.dispatchEvent(new Event("input", { bubbles: true }));
  }

  function insertLinePrefix(textarea, prefix) {
    var start = textarea.selectionStart;
    var value = textarea.value;
    var lineStart = value.lastIndexOf("\n", start - 1) + 1;
    textarea.value = value.slice(0, lineStart) + prefix + value.slice(lineStart);
    textarea.selectionStart = textarea.selectionEnd = start + prefix.length;
    textarea.focus();
    textarea.dispatchEvent(new Event("input", { bubbles: true }));
  }

  var TOOLBAR_ACTIONS = {
    bold: function (t) { wrapSelection(t, "**"); },
    italic: function (t) { wrapSelection(t, "*"); },
    code: function (t) { wrapSelection(t, "`"); },
    h: function (t) { insertLinePrefix(t, "## "); },
    quote: function (t) { insertLinePrefix(t, "> "); },
    ul: function (t) { insertLinePrefix(t, "- "); },
    ol: function (t) { insertLinePrefix(t, "1. "); },
    hr: function (t) {
      var start = t.selectionStart;
      var before = t.value.slice(0, start);
      var prefix = before === "" || before.charAt(before.length - 1) === "\n" ? "" : "\n";
      t.value = before + prefix + "\n---\n\n" + t.value.slice(start);
      t.focus();
      t.dispatchEvent(new Event("input", { bubbles: true }));
    },
    link: function (t) {
      // Platzhalter statt einer echten URL-Vorlage — ein Schema-Präfix im Quelltext würde
      // `test_app_js_makes_no_external_requests` als externe Referenz auffassen; ein
      // Platzhalter-Wort ist ohnehin klarer als eine Vorlage, die wie ein echter Link aussieht.
      var start = t.selectionStart;
      var end = t.selectionEnd;
      var selected = t.value.slice(start, end) || "Linktext";
      var url = "Ziel-URL";
      var snippet = "[" + selected + "](" + url + ")";
      t.value = t.value.slice(0, start) + snippet + t.value.slice(end);
      var urlStart = start + selected.length + 3;
      t.selectionStart = urlStart;
      t.selectionEnd = urlStart + url.length;
      t.focus();
      t.dispatchEvent(new Event("input", { bubbles: true }));
    },
  };

  Array.prototype.forEach.call(editorToolbarEl.querySelectorAll("[data-md]"), function (button) {
    button.addEventListener("click", function () {
      var action = TOOLBAR_ACTIONS[button.dataset.md];
      if (action) action(editorTextareaEl);
    });
  });

  togglePreviewButtonEl.addEventListener("click", function () {
    setEditorMode(state.mode === "edit" ? "preview" : "edit");
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
      insertAtCursor(editorTextareaEl, "![" + (file.name || "Bild") + "](asset:" + asset.id + ")");
      if (state.mode === "preview") {
        editorPreviewEl.innerHTML = markdownToHtml(editorTextareaEl.value, { itemId: itemId });
      }
    }).catch(function (err) {
      toast(err.message || "Bild-Upload fehlgeschlagen.", "error");
    });
  });

  [fieldTitleEl, fieldStatusEl, fieldDueEl, fieldTagsEl, fieldLinksEl, editorTextareaEl].forEach(
    function (input) {
      input.addEventListener("input", function () {
        updateVersionBand();
        saveDraft();
      });
      // `<select>`/`<input type=date>` feuern in manchen Browsern nur `change`, nicht `input`.
      input.addEventListener("change", function () {
        updateVersionBand();
        saveDraft();
      });
    }
  );

  metaPanelEl.addEventListener("toggle", renderMetaDigest);
}
