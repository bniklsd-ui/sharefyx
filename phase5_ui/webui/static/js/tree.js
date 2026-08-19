"use strict";

// -- Navigationsbaum (Step 7b) --------------------------------------------------------------

import { state, BUCKET_LABELS, activeSpaceWritable, setCreateControlsPresent, isGlobalScope } from "./state.js";
import { el, toast } from "./toasts.js";
import { reportUnexpectedError } from "./api.js";
import { closeEditor } from "./editor.js";
import { loadItems, renderCrumb, moveItemToFolder } from "./list.js";
import { openNewFolderDialog } from "./dialogs.js";

var railTreeEl;
var homeButtonEl;

export function bucketNames() {
  return state.meta ? Object.keys(state.meta.buckets) : [];
}

function activateView(spaceName) {
  // Jeder Klick auf einen Space/Eimer/Ordner führt aus dem globalen Modus zurück (P6-AP), ohne
  // dass jede Aufrufstelle das selbst erinnern muss.
  state.scope = "space";
  state.activeSpace = spaceName;
  setCreateControlsPresent(activeSpaceWritable());
  renderRail();
  renderCrumb();
  return loadItems();
}

// "Alle Items" (P6-AP/AQ) — `state.activeSpace` bleibt bewusst unangetastet, das ist der
// Rückweg in den zuletzt aktiven Space.
export function navigateAll() {
  state.scope = "all";
  state.filter = null;
  state.folder = null;
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
    if (space.name === state.activeSpace && bucket === state.filter) {
      button.setAttribute("aria-current", "true");
    }
    button.appendChild(el("span", "rail__label", BUCKET_LABELS[bucket] || bucket));
    button.appendChild(el("span", "tree__count", String(space.counts[bucket])));
    button.addEventListener("click", function () {
      // Meldung des Nikingers: ein Ordner-/Space-Wechsel über den Baum ließ einen offen
      // gebliebenen Editor unangetastet stehen — Liste und Baum sprangen auf den neuen Space,
      // während rechts weiter der alte (u.U. ungespeicherte) Editor stand, ohne dass man ihn
      // von dort noch schließen konnte. `closeEditor()` fragt bei ungespeicherten Änderungen
      // nach (derselbe Dialog wie das "×" im Editor) und bricht bei "Abbrechen" die Navigation
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

function folderButton(space, node, isChild) {
  var button = el("button", "tree__folder tree__realfolder" + (isChild ? " tree__realfolder--child" : ""));
  button.type = "button";
  button.dataset.space = space.name;
  button.dataset.folder = node.path;
  if (space.name === state.activeSpace && state.folder === node.path) {
    button.setAttribute("aria-current", "true");
  }
  button.appendChild(el("span", "rail__label", node.name));
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
  row.appendChild(el("span", "tree__twist", open ? "▾" : "▸"));
  row.appendChild(el("span", "rail__glyph", space.name.charAt(0).toUpperCase()));
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

export function renderRail() {
  railTreeEl.textContent = "";
  renderScopeRow();
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
  homeButtonEl.setAttribute("aria-current", state.selectedId === null ? "true" : "false");
}

export function init() {
  railTreeEl = document.getElementById("rail-tree");
  homeButtonEl = document.getElementById("home-button");
}
