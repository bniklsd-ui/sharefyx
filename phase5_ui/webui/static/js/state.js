"use strict";

// -- Geteilter Anwendungszustand + abgeleitete UI-Helfer -------------------------------------
// `state` ist ein einzelnes, über alle Module geteiltes Objekt (Modul-Bindings sind live in
// ES-Modulen — andere Dateien importieren dieselbe Referenz und mutieren ihre Felder, nie das
// Binding selbst neu zuweisen). Das ist dieselbe Semantik wie die frühere closure-gebundene
// `state`-Variable in `initShell()`, nur auf Modulebene statt Funktionsebene.

// Beschriftung der Ordner. Die Ordner SELBST (und ihre Filterkombinationen) kommen aus
// `GET /api/v1/meta`, nicht von hier — sonst gäbe es zwei Definitionen desselben Vokabulars
// (siehe `api.py :: _BUCKETS`). Diese Tabelle liefert nur die deutschen Namen.
export var BUCKET_LABELS = {
  open: "Offen",
  done: "Erledigt",
  note: "Notizen",
  archived: "Archiv",
};

// Deutsche Beschriftung für `storage.models`s Typ-Vokabular ("task"/"note") — dieselbe
// Übersetzungstabelle wie BUCKET_LABELS, nur für den Anlegen-Dialog. `state.meta.status_values`
// bleibt die Quelle der WERTE (P5-U), diese Tabelle liefert nur die Anzeige.
export var TYPE_LABELS = {
  task: "Aufgabe",
  note: "Notiz",
};

export var state = {
  // aus /overview gemischt mit folders/members aus /spaces (Step 7 Commit 1, list.js ::
  // loadOverview()): {name, own, writable, item_count, counts, recent, folders, members}
  spaces: [],
  ownSpace: null,
  activeSpace: null,
  expanded: {},        // fremder Space-Name -> aufgeklappt?
  filter: "open",
  // echter Ordnerpfad (z.B. "Projekte/Backend") statt eines Eimer-Filters — exklusiv zu
  // `filter`, nie beide gleichzeitig gesetzt (Step 7 Commit 1, tree.js :: navigate()/
  // navigateFolder()).
  folder: null,
  query: "",
  items: [],
  selectedId: null,
  selectedReadonly: false,
  meta: null,
  mode: "edit",
  editingSnapshot: null,
  conflictCurrent: null,
};

export function spaceByName(name) {
  for (var i = 0; i < state.spaces.length; i++) {
    if (state.spaces[i].name === name) return state.spaces[i];
  }
  return null;
}

// Live-Fund 2026-08-13, zweiter Teil desselben Bugs: der Sidebar-/Übersicht-Fix (writable
// statt own aus /api/v1/spaces) betraf nur das Badge dort -- jede Stelle, die tatsächlich
// Schreib-Bedienelemente ein-/ausblendet, fragte weiterhin nur nach dem eigenen Home-Space
// statt tatsächlichem Schreibrecht. Ein geteilter, fremder-aber-schreibbarer Space (z.B.
// IT-Sekus-Projekt) verlor damit trotz behobenem Badge weiterhin den Anlegen-Knopf.
export function activeSpaceWritable() {
  if (state.activeSpace === null) return false;
  var space = spaceByName(state.activeSpace);
  return !!(space && space.writable);
}

// -- Bedienelemente aus dem DOM lösen (Akzeptanzkriterium 12) -------------------------------
// "Fremder Space: sichtbar, lesbar, OHNE Schreib-Bedienelemente im DOM" heißt wörtlich: nicht
// `hidden`, sondern nicht vorhanden. Bis Step 7b standen Editor, "+"-Knopf und Anlegen-Dialog
// permanent im Dokument und waren nur ausgeblendet — mit DevTools also auffindbar. Diese
// Hilfsfunktion hängt den ganzen Teilbaum aus und später an derselben Elternstelle wieder ein;
// Kindreferenzen und Event-Listener überleben das unverändert.

export function detachable(node) {
  var parent = node.parentNode;
  return {
    attach: function () { if (!node.parentNode) parent.appendChild(node); },
    detach: function () { if (node.parentNode) node.parentNode.removeChild(node); },
  };
}

export var editorPart;
export var createTriggers;
export var createDialogPart;

export function setCreateControlsPresent(present) {
  createTriggers.forEach(function (part) { present ? part.attach() : part.detach(); });
  // Der Dialog hängt NUR am Space, nicht an der Trefferlage — sonst könnte ein Listen-Neuladen
  // einen gerade geöffneten Anlegen-Dialog aus dem Dokument reißen.
  activeSpaceWritable() ? createDialogPart.attach() : createDialogPart.detach();
}

export function init() {
  var detailEditorEl = document.getElementById("detail-editor");
  var newItemButtonEl = document.getElementById("new-item-button");
  var createButtonEl = document.getElementById("create-button");
  var createDialogEl = document.getElementById("create-dialog");

  editorPart = detachable(detailEditorEl);
  createTriggers = [detachable(newItemButtonEl), detachable(createButtonEl)];
  createDialogPart = detachable(createDialogEl);
}
