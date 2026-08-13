"use strict";

// -- Navigationsbaum (Step 7b) --------------------------------------------------------------

import { state, BUCKET_LABELS, activeSpaceWritable, setCreateControlsPresent } from "./state.js";
import { el } from "./toasts.js";
import { reportUnexpectedError } from "./api.js";
import { closeEditor } from "./editor.js";
import { loadItems, renderCrumb } from "./list.js";

var railTreeEl;
var homeButtonEl;

export function bucketNames() {
  return state.meta ? Object.keys(state.meta.buckets) : [];
}

function activateView(spaceName) {
  state.activeSpace = spaceName;
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
  }
}

export function renderRail() {
  railTreeEl.textContent = "";
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
