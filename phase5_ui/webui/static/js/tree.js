"use strict";

// -- Navigationsbaum (Step 7b) --------------------------------------------------------------

import { state, BUCKET_LABELS, activeSpaceWritable, setCreateControlsPresent, isGlobalScope, spaceCategory } from "./state.js";
import { el, toast } from "./toasts.js";
import { reportUnexpectedError } from "./api.js";
import { closeEditor } from "./editor.js";
import { loadItems, renderCrumb, moveItemToFolder, clearSelection } from "./list.js";
import { openNewFolderDialog } from "./dialogs.js";
import { iconSvg } from "./icons.js";

var railTreeEl;
var homeButtonEl;

export function bucketNames() {
  return state.meta ? Object.keys(state.meta.buckets) : [];
}

// "Alle Items" (P6-AP/AQ) — `state.activeSpace` bleibt bewusst unangetastet, das ist der
// Rückweg in den zuletzt aktiven Space.
export function navigateAll() {
  state.scope = "all";
  state.filter = null;
  state.folder = null;
  // Phase 8.6 Plan 2 Block G G3/G4 (P8.6-AG / Befund 7a): im "Alle Items"-Modus ist
  // `renderListSlot()` immer in der Listen-Ansicht, nie in der Übersicht -- setzen wir
  // `state.overview` auf false, bevor renderListSlot() zur Frage kommt. Sonst bliebe
  // die Übersicht sichtbar, obwohl der globale Modus sie per Definition ausschließt.
  state.overview = false;
  // V117 (gleiche Begruendung wie in activateView): der erste renderRail() laeuft BEVOR
  // loadItems() resolved -- wenn state.itemsLoaded noch von einem frueheren Space-Modus
  // befuellt ist, wuerden Folder-Counter aus dem falschen Pool gezeigt. Reset auf {}.
  state.itemsLoaded = {};
  clearSelection();
  setCreateControlsPresent(activeSpaceWritable());
  renderRail();
  renderCrumb();
  return loadItems();
}

export function navigate(spaceName, bucket) {
  state.filter = bucket;
  state.folder = null;
  return activateView(spaceName);
}

// Echter Ordner statt Eimer-Filter (Step 7 Commit 1) — exklusiv zu `navigate()`, siehe
// `state.js`s Kommentar zu `state.folder`.
export function navigateFolder(spaceName, folderPath) {
  state.folder = folderPath;
  state.filter = null;
  return activateView(spaceName);
}

export function renderFolders(space) {
  var wrap = document.createDocumentFragment();
  bucketNames().forEach(function (bucket) {
    var button = el("button", "tree__folder");
    button.type = "button";
    button.dataset.space = space.name;
    button.dataset.bucket = bucket;
    // P8.6-H-R-3-Nachtrag (Nikinger-Fund 2026-09-17): Übersicht und ein Space/Eimer sind
    // unterschiedliche Aktionen -- `!state.overview` verhindert, dass ein Eimer aus einer
    // vorigen Space-Navigation als "aktuell" stehen bleibt, waehrend die Übersicht gezeigt
    // wird (`state.activeSpace`/`state.filter` werden beim Wechsel in die Übersicht bewusst
    // NICHT geleert, siehe app.js homeButtonEl-Handler -- der Rückweg in den Space soll die
    // Filterung wiederfinden).
    if (!state.overview && space.name === state.activeSpace && bucket === state.filter) {
      button.setAttribute("aria-current", "true");
    }
    button.appendChild(el("span", "rail__label", BUCKET_LABELS[bucket] || bucket));
    button.appendChild(el("span", "tree__count", String(space.counts[bucket])));
    button.addEventListener("click", function () {
      // Meldung des Nikingers: ein Ordner-/Space-Wechsel über den Baum ließ einen offen
      // gebliebenen Editor unangetastet stehen — Liste und Baum sprangen auf den neuen Space,
      // während rechts weiter der alte (u.U. ungespeicherte) Editor stand, ohne dass man ihn
      // von dort noch schließen konnte. `closeEditor()` fragt bei ungespeicherten Änderungen
      // nach (derselbe Dialog wie das Schliessen-Icon im Editor) und bricht bei "Abbrechen" die Navigation
      // ab, statt sie durchzuführen und den Editor stumm zu verwerfen.
      closeEditor().then(function (proceed) {
        if (proceed === false) return;
        return navigate(space.name, bucket);
      }).catch(reportUnexpectedError);
    });
    wrap.appendChild(button);
  });
  return wrap;
}

// Baut aus der flachen `space.folders`-Liste (`store.py :: list_spaces()`, ein `rglob`-Walk —
// jede Ebene ist als eigener Eintrag enthalten, nie nur die Blätter) eine ≤2-stufige Baumform.
// Tiefe >2 kommt serverseitig nie vor (`MAX_FOLDER_DEPTH`/`validate_folder()`), reines Splitten
// auf "/" reicht deshalb, kein rekursiver Baumbau nötig.
export function buildFolderTree(folders) {
  var tops = [];
  var byTop = {};
  (folders || []).forEach(function (path) {
    if (path.indexOf("/") !== -1) return;
    var node = { path: path, name: path, children: [] };
    byTop[path] = node;
    tops.push(node);
  });
  (folders || []).forEach(function (path) {
    var slash = path.indexOf("/");
    if (slash === -1 || path.indexOf("/", slash + 1) !== -1) return;
    var parent = byTop[path.slice(0, slash)];
    if (parent) parent.children.push({ path: path, name: path.slice(slash + 1) });
  });
  return tops;
}

// Drag & Drop (Step 7 Commit 4) — Drop-Ziel nur für echte Ordner im EIGENEN Space, derselbe
// Eigentümer-Riegel wie der Verschieben-Knopf in list.js (der Server lehnt einen
// `folder`-Wechsel an einem fremden Item ohnehin ab; das Gating hier ist nur bessere UX, keine
// eigene Sicherheitsgrenze). Teilt sich `moveItemToFolder()` mit dem Menü-Pfad (list.js),
// duplizierte Erfolgs-/Fehlermeldung ist bewusst — zu wenig gemeinsam mit dem dialoggebundenen
// Menü-Pfad, um das noch zu teilen (dort muss ein Dialog offen bleiben, hier gibt es keinen).
function bindFolderDropTarget(button, folderPath) {
  button.addEventListener("dragover", function (event) {
    event.preventDefault();
    event.dataTransfer.dropEffect = "move";
    button.classList.add("tree__realfolder--dragover");
  });
  button.addEventListener("dragleave", function () {
    button.classList.remove("tree__realfolder--dragover");
  });
  button.addEventListener("drop", function (event) {
    event.preventDefault();
    button.classList.remove("tree__realfolder--dragover");
    var itemId = event.dataTransfer.getData("text/plain");
    var item = itemId && state.items.filter(function (i) { return i.id === itemId; })[0];
    if (!item) return;
    // Ablegen auf dem eigenen Ausgangsordner ist mit Drag & Drop trivial auszulösen (kurz
    // anheben, direkt wieder loslassen) — ohne diesen Guard verursacht das einen leeren
    // `PATCH` mit Versionssprung + Git-Commit für keine tatsächliche Änderung (Advisor-Fund
    // vor diesem Commit; derselbe Leerlauf existiert im Menü-Pfad seit Commit 3, dort aber
    // schwerer aus Versehen auszulösen, deshalb hier behoben und dort nur benannt).
    if ((item.folder || "") === folderPath) return;
    moveItemToFolder(item, folderPath).then(function () {
      toast("Verschoben nach " + folderPath.split("/").join(" / "));
    }).catch(function (err) {
      if (err.code === "conflict") {
        toast(
          "Ein anderer Client hat dieses Item zwischenzeitlich geändert — bitte neu laden und "
          + "erneut versuchen.", "error",
        );
        return;
      }
      if (err.message === "unauthenticated") return;
      toast(err.message || "Verschieben fehlgeschlagen.", "error");
    });
  });
}

// Phase 8.6 Block C C5 (Plan §5.5): Folder-Zähler clientseitig aus `state.items`. Drei
// Regeln aus §5.5, alle hier umgesetzt:
//   1. Was wird gezählt? Alles, was der Nutzer im Ordner SEHEN würde -- dieselbe Filterung
//      wie die Listenansicht, inklusive `archived`. Implementiert über `item.folder` (oder
//      `""` für Wurzel-Items).
//   2. Unterordner? Nein -- nur direkte Kinder. Ein rekursiver Zähler bräuchte eine
//      Baumsummierung und wäre mehrdeutig ("15" an einem Ordner mit selbst 2 Items).
//   3. Items des Spaces noch nicht geladen? Kein Zähler, nicht "0" -- dieselbe Regel wie
//      `tree.js:224-226` für `renderScopeRow()`, jetzt auf Folder ausgedehnt.
function folderItemCount(spaceName, folderPath) {
  var prefix = folderPath + "/";
  var n = 0;
  for (var i = 0; i < state.items.length; i++) {
    var item = state.items[i];
    if (item.space !== spaceName) continue;
    var f = item.folder || "";
    if (f === folderPath || f.indexOf(prefix) === 0) n++;
  }
  return n;
}

function folderButton(space, node, isChild) {
  var button = el("button", "tree__folder tree__realfolder" + (isChild ? " tree__realfolder--child" : ""));
  button.type = "button";
  button.dataset.space = space.name;
  button.dataset.folder = node.path;
  // P8.6-H-R-3-Nachtrag: gleiche Begründung wie bei renderFolders() oben -- ein Ordner
  // bleibt sonst als "aktuell" markiert, waehrend die Übersicht gezeigt wird.
  if (!state.overview && space.name === state.activeSpace && state.folder === node.path) {
    button.setAttribute("aria-current", "true");
  }
  button.appendChild(el("span", "rail__label", node.name));
  // C5 Zähler -- nur, wenn `state.itemsLoaded[space.name]` true ist. Sonst fehlt die Zahl
  // (Regel 3). Selektor-Match ist exakt -- der Flag wird in `list.js :: loadItems()` nach
  // jedem API-Roundtrip gesetzt.
  if (state.itemsLoaded[space.name]) {
    var count = folderItemCount(space.name, node.path);
    if (count > 0) {
      button.appendChild(el("span", "tree__count", String(count)));
    }
  }
  button.addEventListener("click", function () {
    // Dieselbe Rückfrage-vor-Navigation-Disziplin wie bei den Eimer-Buttons oben — ein offener,
    // ungespeicherter Editor darf auch durch einen Ordnerwechsel nicht stumm verworfen werden.
    closeEditor().then(function (proceed) {
      if (proceed === false) return;
      return navigateFolder(space.name, node.path);
    }).catch(reportUnexpectedError);
  });
  if (space.own) bindFolderDropTarget(button, node.path);
  return button;
}

export function renderRealFolders(space) {
  var wrap = document.createDocumentFragment();
  buildFolderTree(space.folders).forEach(function (top) {
    wrap.appendChild(folderButton(space, top, false));
    top.children.forEach(function (child) {
      wrap.appendChild(folderButton(space, child, true));
    });
  });
  return wrap;
}

// "+ Ordner" — nur der eigene Space (der Server lehnt `POST .../folders` für jeden anderen
// Space ohnehin ab, `_spaces_create_folder`s Eigentümer-Riegel; derselbe Grund wie beim
// Verschieben-Knopf in `list.js`, hier eine Ebene höher). Reused `.tree__folder` für dieselbe
// Einrückung/Hover-Fläche wie jeder andere Baumeintrag, nur gedämpfter eingefärbt (`app.css`).
function newFolderButton(space) {
  var button = el("button", "tree__folder tree__new-folder");
  button.type = "button";
  button.appendChild(el("span", "rail__label", "+ Ordner"));
  button.addEventListener("click", openNewFolderDialog);
  return button;
}

export function renderSpaceNode(space) {
  var open = space.own || state.expanded[space.name] === true;
  var row = el("button", "tree__space");
  row.type = "button";
  var twist = el("span", "tree__twist");
  twist.appendChild(iconSvg(open ? "chevron-down" : "chevron-right"));
  row.appendChild(twist);
  // Phase 8 C3 (P8-I): rail__glyph nimmt die Space-Kategoriefarbe an (Plex-Tokens
  // app.css :: --space-own/--space-shared/--space-foreign). Der Glyph bleibt ein
  // Buchstabe, keine Icon -- Identitaet, nicht Symbol.
  row.appendChild(el("span", "rail__glyph rail__glyph--" + spaceCategory(space), space.name.charAt(0).toUpperCase()));
  row.appendChild(el("span", "rail__label", space.name));
  if (!space.writable) row.appendChild(el("span", "tree__badge", "nur lesen"));
  row.addEventListener("click", function () {
    state.expanded[space.name] = !open;
    renderRail();
  });
  railTreeEl.appendChild(row);
  if (open) {
    railTreeEl.appendChild(renderFolders(space));
    railTreeEl.appendChild(renderRealFolders(space));
    if (space.own) railTreeEl.appendChild(newFolderButton(space));
  }
}

// Kein Zähler an dieser Zeile: `state.spaces` trägt keine Zahl für "alle lesbaren Items", und
// eine aus den sichtbaren Spaces aufaddierte Zahl wäre falsch — sie ließe genau die item-level
// geteilten Items weg, um die es hier geht. Lieber keine Zahl als eine unwahre.
function renderScopeRow() {
  // Phase 8.6 Block C C2 (Plan §5.2): "Alle Items" bekommt jetzt denselben tree__group-
  // Trenner wie "Mein Space"/"Verbundene Spaces" — sonst klebt die Zeile ohne Überschrift
  // an den Spaces-Block, und der Leser sucht die "Kippschalter"-Funktion an einer Stelle,
  // die nicht als eigene Gruppe erkennbar ist. Die Gruppe heißt "Alles" (analog "Mein
  // Space" / "Verbundene Spaces"), die Schaltfläche selbst bleibt "Alle Items".
  railTreeEl.appendChild(el("div", "tree__group", "Alles"));
  var button = el("button", "tree__scope");
  button.type = "button";
  button.appendChild(el("span", "rail__label", "Alle Items"));
  if (isGlobalScope()) button.setAttribute("aria-current", "true");
  button.addEventListener("click", function () {
    closeEditor().then(function (proceed) {
      if (proceed === false) return;
      return navigateAll();
    }).catch(reportUnexpectedError);
  });
  railTreeEl.appendChild(button);
}

// Phase 8.6 Block C C4 (Plan §5.4): exportiert, weil der Space-Klick in der Übersicht
// (`list.js :: renderOverview()`, die "overview__space-open"-Schaltfläche) auf
// `activateView(name)` navigiert — semantisch "in den Space wechseln, ohne Filter zu
// setzen". `navigate(name, bucket)` würde einen Bucket mitgeben, den der Nutzer in der
// Übersicht nicht explizit wählt (er klickt die Zeile, nicht den Counter-Chip).
//
// V117-Befund: state.itemsLoaded wurde im globalen Modus ("Alle Items") für alle
// sichtbaren Spaces gesetzt -- beim Übergang von "all" zurück in einen einzelnen Space
// würde renderRail() aber die Items des globalen Pools zählen, nicht die des
// Ziel-Spaces (state.items wird erst in loadItems() umgeschaltet, renderRail() läuft
// aber ZUVOR). Reset auf false löst das: renderRail() zeigt bis zur loadItems-Auflösung
// leere Folder-Counter, danach sind sie korrekt für den neuen Space.
export function activateView(spaceName) {
  // Jeder Klick auf einen Space/Eimer/Ordner führt aus dem globalen Modus zurück (P6-AP), ohne
  // dass jede Aufrufstelle das selbst erinnern muss.
  state.scope = "space";
  state.activeSpace = spaceName;
  // Phase 8.6 Plan 2 Block G G3 (P8.6-AA): ein Sprung in einen Space ist immer ein
  // Verlassen der Übersicht. `renderListSlot()` wertet `state.overview` aus, um die
  // Item-Liste statt der Spaces-Übersicht anzuzeigen.
  state.overview = false;
  // V117: alle per "all" gesetzten Loaded-Flags zurücksetzen -- sonst zeigt das Rail
  // für ein paar ms Counts aus dem globalen Pool, die zum Ziel-Space gar nicht passen.
  state.itemsLoaded = {};
  // §9.3 Punkt 1: Navigation leert die Auswahl, dieselbe Exklusivitäts-Disziplin wie
  // `folder`/`filter` — sonst könnte eine Auswahl Items enthalten, die hier gar nicht mehr
  // sichtbar sind.
  clearSelection();
  setCreateControlsPresent(activeSpaceWritable());
  renderRail();
  renderCrumb();
  return loadItems();
}

export function renderRail() {
  railTreeEl.textContent = "";
  // Phase 8.6 Block C C2 (Plan §5.2): "Alle Items" wandert von ganz oben hinter die Spaces —
  // der "Kippschalter" zwischen Space-Sicht und globaler Sicht ist jetzt das LETZTE Element
  // im Rail, nicht das erste. Der Nikinger wollte "Alle Items" nicht mehr als prominentesten
  // Eintrag (er war visuell vor dem eigenen Space), sondern als bewusste Aktion am Ende der
  // Navigation. Der bestehende Mechanismus (toggle über `state.scope`) bleibt — der
  // `navigateAll()`-Klick ist unverändert.
  var own = state.spaces.filter(function (s) { return s.own; });
  var foreign = state.spaces.filter(function (s) { return !s.own; });

  if (own.length) {
    railTreeEl.appendChild(el("div", "tree__group", "Mein Space"));
    own.forEach(renderSpaceNode);
  }
  if (foreign.length) {
    railTreeEl.appendChild(el("div", "tree__group", "Verbundene Spaces"));
    foreign.forEach(renderSpaceNode);
  }
  renderScopeRow();
  // P8.6-H-R-3-Nachtrag (Nikinger-Fund 2026-09-17): `selectedId === null` markierte
  // Home/Übersicht auch dann als "aktuell", wenn tatsächlich ein Space/Eimer/Ordner oder
  // der globale "Alle Items"-Modus ohne ausgewähltes Item angezeigt wurde -- zwei
  // gleichzeitig "aktuelle" Rail-Einträge für zwei verschiedene Aktionen. `#home-button`
  // steht seit Block G konkret für die Übersicht (Plan 2 §4.3), also ist deren eigener
  // Zustandsflag `state.overview` der richtige Schalter, nicht die Item-Auswahl.
  homeButtonEl.setAttribute("aria-current", state.overview === true ? "true" : "false");
}

export function init() {
  railTreeEl = document.getElementById("rail-tree");
  homeButtonEl = document.getElementById("home-button");
}
