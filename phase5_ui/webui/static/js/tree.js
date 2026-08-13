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

export function navigate(spaceName, bucket) {
  state.activeSpace = spaceName;
  state.filter = bucket;
  setCreateControlsPresent(activeSpaceWritable());
  renderRail();
  renderCrumb();
  return loadItems();
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
  if (open) railTreeEl.appendChild(renderFolders(space));
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
