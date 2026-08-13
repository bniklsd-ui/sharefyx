"use strict";

// -- Übersichtsseite + Liste ------------------------------------------------------------------

import { state, BUCKET_LABELS, TYPE_LABELS, activeSpaceWritable, spaceByName, setCreateControlsPresent } from "./state.js";
import { el } from "./toasts.js";
import { api, reportUnexpectedError } from "./api.js";
import { navigate, renderRail, bucketNames } from "./tree.js";
import { selectItem } from "./editor.js";

var listCrumbEl;
var listReadonlyEl;
var listRowsEl;
var listEmptyEl;
var listEmptyTextEl;
var listChipsEl;
var searchInputEl;
var createButtonEl;

var overviewTitleEl;
var overviewTilesEl;
var overviewRecentEl;
var overviewForeignEl;

export function renderOverview() {
  var own = spaceByName(state.ownSpace);
  overviewTitleEl.textContent = state.ownSpace || "";
  overviewTilesEl.textContent = "";
  overviewRecentEl.textContent = "";
  overviewForeignEl.textContent = "";
  if (!own) return;

  bucketNames().forEach(function (bucket) {
    var tile = el("button", "tile");
    tile.type = "button";
    tile.appendChild(el("span", "tile__count tnum", String(own.counts[bucket])));
    tile.appendChild(el("span", "tile__label", BUCKET_LABELS[bucket] || bucket));
    tile.addEventListener("click", function () {
      navigate(own.name, bucket).catch(reportUnexpectedError);
    });
    overviewTilesEl.appendChild(tile);
  });

  if (own.recent.length === 0) {
    overviewRecentEl.appendChild(el("li", "recent-row__meta", "Noch nichts vorhanden."));
  }
  own.recent.forEach(function (item) {
    var li = el("li");
    var row = el("button", "recent-row");
    row.type = "button";
    // Fremdtext ausschließlich über textContent, nie innerHTML — dieselbe Disziplin wie in
    // renderList(). Die Übersicht zeigt bewusst keine Textausschnitte (siehe
    // serializers.py :: overview_row_to_json()).
    row.appendChild(el("span", "recent-row__title", item.title));
    var recentMetaEl = el("span", "recent-row__meta tnum");
    recentMetaEl.appendChild(el("span", "version-num", "v" + item.version));
    recentMetaEl.appendChild(document.createTextNode(" · " + item.updated.slice(0, 10)));
    row.appendChild(recentMetaEl);
    row.addEventListener("click", function () { openFromOverview(own.name, item); });
    li.appendChild(row);
    overviewRecentEl.appendChild(li);
  });

  var foreign = state.spaces.filter(function (s) { return !s.own; });
  if (foreign.length) {
    overviewForeignEl.appendChild(el("h2", "overview__heading", "Verbundene Spaces"));
    foreign.forEach(function (space) {
      var card = el("button", "space-card");
      card.type = "button";
      card.appendChild(el("span", "rail__glyph", space.name.charAt(0).toUpperCase()));
      card.appendChild(el("span", null, space.name));
      card.appendChild(el("span", "space-card__meta", space.item_count + " Items" + (space.writable ? "" : " · nur lesen")));
      card.addEventListener("click", function () {
        state.expanded[space.name] = true;
        navigate(space.name, "note").catch(reportUnexpectedError);
      });
      overviewForeignEl.appendChild(card);
    });
  }
}

export function openFromOverview(spaceName, item) {
  // Ein Klick in "Zuletzt benutzt" darf nicht in einem Ordner landen, der das Item gar nicht
  // enthält — sonst ist die Liste daneben leer, während rechts das Item steht.
  var bucket = bucketFor(item) || state.filter;
  navigate(spaceName, bucket)
    .then(function () { return selectItem(item.id); })
    .catch(reportUnexpectedError);
}

export function loadOverview() {
  // `/overview` trägt die Zähler/„Zuletzt benutzt"; `/spaces` trägt `folders`/`members` (Step 7
  // Commit 1) — kein neuer Endpunkt, nur ein zweiter, paralleler Aufruf und ein Merge nach Name.
  // Beide Routen filtern über dieselbe `_visible_space_infos()`, jeder Eintrag aus `/overview`
  // hat also eine passende `/spaces`-Zeile; der Fallback greift nur defensiv.
  return Promise.all([api("/overview"), api("/spaces")]).then(function (results) {
    var overview = results[0];
    var byName = {};
    results[1].forEach(function (s) { byName[s.name] = s; });
    overview.forEach(function (s) {
      var extra = byName[s.name];
      s.folders = extra ? extra.folders : [];
      s.members = extra ? extra.members : [];
    });
    state.spaces = overview;
    renderRail();
    renderOverview();
  });
}

// -- Liste ----------------------------------------------------------------------------------

export function itemMetaLine(item) {
  var parts = [item.type, item.status];
  if (item.due) parts.push(item.due);
  if (item.tags && item.tags.length) parts.push(item.tags.join(", "));
  return parts.join(" · ");
}

export function renderCrumb() {
  listCrumbEl.textContent = "";
  var strong = el("strong", null, state.activeSpace || "");
  listCrumbEl.appendChild(strong);
  var label = state.folder ? state.folder : (BUCKET_LABELS[state.filter] || state.filter);
  listCrumbEl.appendChild(document.createTextNode(" › " + label));
  listReadonlyEl.hidden = activeSpaceWritable();
}

export function renderChips() {
  // §4.5: die aktiven Filter als ENTFERNBARE Chips. Bis Step 7b wurden Chips nur im
  // Leerzustand gezeigt und ließen sich nicht entfernen (`.chip__remove` war totes CSS).
  listChipsEl.textContent = "";
  if (!state.query) return;
  var chip = el("span", "chip");
  chip.appendChild(el("span", null, "Suche: " + state.query));
  var remove = el("button", "chip__remove", "×");
  remove.type = "button";
  remove.title = "Suche zurücksetzen";
  remove.addEventListener("click", function () {
    state.query = "";
    searchInputEl.value = "";
    loadItems().catch(reportUnexpectedError);
  });
  chip.appendChild(remove);
  listChipsEl.appendChild(chip);
}

export function renderList() {
  listRowsEl.textContent = "";
  renderChips();

  if (state.items.length === 0) {
    listEmptyEl.hidden = false;
    if (state.query) {
      listEmptyTextEl.textContent = "Keine Treffer für „" + state.query + "“.";
    } else if (!activeSpaceWritable()) {
      listEmptyTextEl.textContent = "In diesem Ordner liegt nichts.";
    } else if (state.folder) {
      listEmptyTextEl.textContent = "Noch nichts in „" + state.folder + "“.";
    } else {
      listEmptyTextEl.textContent =
        "Noch nichts unter „" + (BUCKET_LABELS[state.filter] || state.filter) + "“.";
    }
    // Meldung des Nikingers, gleicher Fund wie der Anlegen-Dialog: der Knopf sagte immer
    // "Notiz", auch im "Offen"/"Erledigt"-Ordner (Typ "task"). Folgt jetzt demselben Typ, den
    // ein Klick tatsächlich anlegen würde (siehe dialogs.js :: openCreateDialog()). In einem
    // echten Ordner (state.filter === null) gibt es keinen Typ-Hinweis dafür — Default "note",
    // Anlegen selbst bleibt ohnehin Commit-3-Scope (K4, Ordner-Whitelist am Server).
    var emptyBucket = state.meta && state.filter && state.meta.buckets[state.filter];
    var emptyType = (emptyBucket && emptyBucket.type) || "note";
    createButtonEl.textContent = "Erste " + (TYPE_LABELS[emptyType] || emptyType) + " anlegen";
    // Der Anlegen-Knopf ist bei einer leeren Suche fehl am Platz (er legt kein Item mit dem
    // Suchbegriff an) und bei einem fremden Space gar nicht erst im DOM.
    if (activeSpaceWritable()) setCreateControlsPresent(!state.query);
    return;
  }

  listEmptyEl.hidden = true;
  if (activeSpaceWritable()) setCreateControlsPresent(true);
  state.items.forEach(function (item) {
    var li = el("li");
    var button = el("button", "list__row");
    button.type = "button";
    button.dataset.id = item.id;
    if (item.id === state.selectedId) button.setAttribute("aria-current", "true");
    button.appendChild(el("div", "list__row-title", item.title));
    button.appendChild(el("div", "list__row-meta tnum", itemMetaLine(item)));
    button.addEventListener("click", function () { selectItem(item.id).catch(reportUnexpectedError); });
    li.appendChild(button);
    listRowsEl.appendChild(li);
  });
}

export function filterParams() {
  // Echter Ordner und Eimer-Filter sind exklusiv (Step 7 Commit 1) — ein Ordner sendet nur
  // `folder=<Pfad>`, kein `type`/`status` mehr, `store.search(folder=…)` ist exakt, nicht
  // Präfix (V55), zeigt also nur Items direkt in diesem Ordner (Finder-Stil).
  if (state.folder) return { folder: state.folder };
  // Die drei/vier Eimer kommen serverseitig aus `api.py :: _BUCKETS` und werden über
  // `GET /api/v1/meta` geliefert — hier steht bewusst keine zweite Definition mehr.
  var bucket = state.meta && state.meta.buckets[state.filter];
  return Object.assign({}, bucket || {});
}

export function bucketFor(item) {
  var names = bucketNames();
  for (var i = 0; i < names.length; i++) {
    var f = state.meta.buckets[names[i]];
    var typeOk = !f.type || f.type === item.type;
    var statusOk = !f.status || f.status === item.status;
    if (typeOk && statusOk) return names[i];
  }
  return null;
}

export function loadItems() {
  var params = new URLSearchParams(filterParams());
  if (state.activeSpace) params.set("space", state.activeSpace);
  if (state.query) params.set("query", state.query);
  return api("/items?" + params.toString()).then(function (result) {
    state.items = result.items;
    renderList();
  });
}

export function init() {
  listCrumbEl = document.getElementById("list-crumb");
  listReadonlyEl = document.getElementById("list-readonly");
  listRowsEl = document.getElementById("list-rows");
  listEmptyEl = document.getElementById("list-empty");
  listEmptyTextEl = document.getElementById("list-empty-text");
  listChipsEl = document.getElementById("list-chips");
  searchInputEl = document.getElementById("search-input");
  createButtonEl = document.getElementById("create-button");

  overviewTitleEl = document.getElementById("overview-title");
  overviewTilesEl = document.getElementById("overview-tiles");
  overviewRecentEl = document.getElementById("overview-recent");
  overviewForeignEl = document.getElementById("overview-foreign");

  // -- Suche (200ms Debounce) -----------------------------------------------------------
  var searchTimer = null;
  searchInputEl.addEventListener("input", function () {
    state.query = searchInputEl.value;
    clearTimeout(searchTimer);
    searchTimer = setTimeout(function () { loadItems().catch(reportUnexpectedError); }, 200);
  });
}
