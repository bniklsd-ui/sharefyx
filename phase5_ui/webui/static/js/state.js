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
  // "space" | "all" — globaler Modus (P6-AP): eigenes Feld statt `activeSpace === null`, weil
  // dieses Repo von genau der Verwechslung schon zweimal getroffen wurde (`ownSpaceActive()`-
  // Fund 2026-08-13, `state.filter=null`-Fund Step 7 Commit 1). Im Modus "all" bleiben `filter`
  // UND `folder` auf `null` (P6-AQ), `activeSpace` bleibt unangetastet (Rückweg).
  scope: "space",
  query: "",
  items: [],
  // Phase 8.6 Plan 2 Block G G3 (P8.6-AA): true = der Listen-Slot zeigt die Uebersicht
  // (Spaces + Zuletzt benutzt), false = er zeigt die Item-Liste. Eigenes Feld statt einer
  // Ableitung aus `activeSpace === null`, aus demselben Grund wie `scope` daneben --
  // dieses Repo ist von genau der Verwechslung schon zweimal getroffen worden
  // (`ownSpaceActive()`-Fund 2026-08-13, `state.filter=null`-Fund Step 7 Commit 1).
  // Wird gesetzt von `#home-button`-Klick (true, app.js), `navigateAll()`/`navigate()`/
  // `navigateFolder()`/`activateView()` (false, tree.js). Initial true, damit der erste
  // Frame nach App-Start die Uebersicht zeigt, nicht eine leere Liste.
  overview: true,
  // Phase 8.6 Block C C5 (Plan §5.5 V117): `{ [spaceName]: true }` -- gesetzt wird in
  // `list.js :: loadItems()`, sobald die Items des aktiven Spaces (oder im globalen Modus
  // alle lesbaren Items) geladen sind. Folder-Zähler im Rail (`tree.js :: folderButton()`)
  // fragen diesen Flag ab und zeigen KEINE Zahl, solange er für den jeweiligen Space fehlt
  // -- "Lieber keine Zahl als eine unwahre" (geltender Kommentar in tree.js:224-226, der
  // genau für diesen Fall steht). Im globalen Modus markiert `loadItems()` zusätzlich
  // jeden Space, von dem es Items gesehen hat, als geladen -- ein Space ohne Items im
  // globalen Modus ist trotzdem "gesehen", sein Zähler ist 0.
  itemsLoaded: {},
  // P9 Step E (Plan §7.2a): Signatur des zuletzt gesehenen `/overview`-Payloads, gesetzt von
  // `list.js :: loadOverview()` — also von **jedem** Pfad, der den Zählerstand holt: Bootstrap,
  // 20s-Zähler-Poll, Fokus, und jeder Schreibvorgang (`afterWrite`, Archivieren, Ordner,
  // Space anlegen/entfernen). Gelesen von `graph.js :: loadGraph()`, das ohne Token-Wechsel den
  // `/graph`-Abruf überspringt (P9-33).
  //
  // **Warum das Feld hier steht und nicht in `graph.js`:** der Erzeuger (`list.js`) und der
  // Verbraucher (`graph.js`) kennen sich nicht — `graph.js` importiert `editor.js`, `editor.js`
  // importiert `list.js`. Ein Import von `list.js` nach `graph.js` wäre ein Zyklus, und ein
  // Melde-Aufruf in den fünf Schreibpfaden (`editor.js`, `dialogs.js`, `spaces.js`) wäre eine
  // zweite Wahrheit über "hat sich etwas geändert", die man beim Hinzufügen eines sechsten
  // Schreibpfades leicht übersieht. Das Blatt-Modul `state.js` wird von beiden ohnehin
  // importiert, hält das Format an **einer** Stelle und kennt die Aufrufer nicht.
  graphToken: null,
  selectedId: null,
  selectedReadonly: false,
  // Mehrfachauswahl (§9, P6-AK) — ein `Set` von Item-IDs, geleert bei jeder Navigation
  // (dieselbe Exklusivitäts-Disziplin wie `folder`/`filter`, siehe tree.js :: activateView()).
  selectedItemIds: new Set(),
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

// P9 Step E (Plan §7.2a): reduziert ein `/api/v1/overview`-Payload auf eine Signatur des
// Nutzdatenstands. Bewusst als Zeichenkette statt als Hash — `===` auf einem String ist beim
// Lesen nachvollziehbar, und der Aufbau ist O(n) über wenige hundert Zeilen: billiger als jeder
// Round-Trip, für den diese Signatur ihn einspart.
//
// Was hineingeht, und warum genau das: je Space der `item_count`, die Bucket-Zähler und die
// fünf zuletzt geänderten Items mit `id`/`version`/`updated` (`api.py :: _overview`,
// `_RECENT_LIMIT = 5`). Ein Schreibvorgang setzt `updated` hoch, das Item rückt damit in die
// "Zuletzt benutzt"-Liste und erhöht `version` — die Signatur ändert sich also bei jedem
// Schreibvorgang, im eigenen Space wie in einem fremden.
//
// **Die bewusst in Kauf genommene Grenze:** ändert ein Item nur seine Tags und ist es in
// seinem Space nicht mehr unter den fünf zuletzt geänderten Items, bleibt die Signatur gleich
// und der Graph steht bis zum manuellen Refresh. Genau dieses Item ist dann aber auch in der
// Übersicht daneben nicht zu sehen — der Graph ist nie reichhaltiger als die Seite, auf der
// er hängt. Ohne diese Grenze gäbe es nur zwei Auswege: ein Feld am Graph-Payload (P9-M
// verbietet es) oder ein serverseitiger Änderungs-Zähler (eine neue Route, noch teurer).
export function overviewToken(overview) {
  if (!overview || !overview.length) return null;
  var parts = [];
  for (var i = 0; i < overview.length; i++) {
    var space = overview[i];
    var counts = space.counts || {};
    var countParts = [];
    var keys = Object.keys(counts).sort();
    for (var k = 0; k < keys.length; k++) countParts.push(keys[k] + "=" + counts[keys[k]]);
    var recent = space.recent || [];
    var recentParts = [];
    for (var r = 0; r < recent.length; r++) {
      recentParts.push(recent[r].id + "@" + recent[r].version + "@" + (recent[r].updated || ""));
    }
    parts.push(
      space.name + "#" + space.item_count + "#" + countParts.join(",") + "#" + recentParts.join(",")
    );
  }
  parts.sort();     // die Reihenfolge der Spaces im Payload ist eine Server-Detailfrage
  return parts.join("|");
}

// Live-Fund 2026-08-13, zweiter Teil desselben Bugs: der Sidebar-/Übersicht-Fix (writable
// statt own aus /api/v1/spaces) betraf nur das Badge dort -- jede Stelle, die tatsächlich
// Schreib-Bedienelemente ein-/ausblendet, fragte weiterhin nur nach dem eigenen Home-Space
// statt tatsächlichem Schreibrecht. Ein geteilter, fremder-aber-schreibbarer Space (z.B.
// IT-Sekus-Projekt) verlor damit trotz behobenem Badge weiterhin den Anlegen-Knopf.
export function activeSpaceWritable() {
  if (state.scope === "all") return false;
  if (state.activeSpace === null) return false;
  var space = spaceByName(state.activeSpace);
  return !!(space && space.writable);
}

// Phase 8 Block C C3 (Plan §4.C3 P8-I) -- Ableitung der Space-Kategorie aus den von
// `GET /spaces` gelieferten Feldern (`own`/`writable`). Drei Werte, eine Farbe pro Wert
// (`app.css :: --space-own/--space-shared/--space-foreign`). Aufrufer: Rail-Glyph
// (`tree.js :: renderSpaceNode()`), Metazeilen-Punkt (`list.js :: renderList()`), Legende
// (`app.html`, statisch). `foreign` als Fallback für `null`/`undefined` (z.B. wenn das
// Item zu einem Space gehoert, der in `state.spaces` noch nicht geladen ist -- der
// Aufrufer hat den Space-Namen, aber `spaceByName()` liefert null; konservativ "fremd"
// ist sicherer als "eigener").
export function spaceCategory(space) {
  if (!space) return "foreign";
  if (space.own) return "own";
  if (space.writable) return "shared";
  return "foreign";
}

export function isGlobalScope() {
  return state.scope === "all";
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
