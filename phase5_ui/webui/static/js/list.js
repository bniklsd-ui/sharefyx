"use strict";

// -- Übersichtsseite + Liste ------------------------------------------------------------------

import { state, BUCKET_LABELS, TYPE_LABELS, activeSpaceWritable, spaceByName, setCreateControlsPresent, isGlobalScope } from "./state.js";
import { el } from "./toasts.js";
import { api, reportUnexpectedError } from "./api.js";
import { navigate, renderRail, bucketNames } from "./tree.js";
import { selectItem } from "./editor.js";
import { openMoveDialog, openShareDialog } from "./dialogs.js";
import { iconSvg } from "./icons.js";

var listCrumbEl;
var listReadonlyEl;
var listRowsEl;
var listEmptyEl;
var listEmptyTextEl;
var listChipsEl;
var searchInputEl;
var createButtonEl;

var listSelectionEl;
var listSelectionCountEl;
var listSelectionMoveEl;
var listSelectionClearEl;

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
  // P6-AT: ohne Space-Angabe ist eine Trefferliste über mehrere Spaces nicht interpretierbar.
  if (isGlobalScope()) parts.unshift(item.space);
  return parts.join(" · ");
}

// -- Sichtbarkeits-Chip (Step 7 Commit 2) -----------------------------------------------------
// Alle Felder stehen bereits auf item_to_json()/summary_to_json() (P6 Step 5) — kein
// Backend-Aufruf, reines Anzeigen. "private" und "human" ohne Freigaben sehen bewusst beide
// gedämpft aus (niemand sonst hat Zugriff); erst eine echte Freigabe hebt den Chip farblich
// hervor, dieselbe "nur Abweichung vom Default fällt auf"-Logik wie `.tree__badge`s "nur lesen".
//
// **Kleine, benannte Abweichung vom Plan-Wortlaut** (der Dispatch dort prüfte `visibility`
// zuerst, "private" unbedingt zu "privat"): `acl.py :: decision_for()` verundet
// `share_read`/`share_write` IMMER in `AclDecision.read`/`write`, unabhängig von `visibility` —
// `permissions.py :: can_read_item_as_human()`/`can_write_item_as_human()` fragen `visibility`
// nur für `Surface.AGENT` (P6-P), nie für Menschen. Ein Item mit `visibility=private` UND
// nicht-leerem `share_read` ist für den freigegebenen Menschen also faktisch lesbar — erreichbar
// schon heute über ein rohes `PATCH /api/v1/items/{id}` (`_items_patch` hat keine Feld-
// Whitelist), nicht erst über Commit 5s künftigen Freigabe-Dialog. Ein Chip, der dort "privat"
// zeigt, würde dem Eigentümer eine falsche Zusicherung machen. Deshalb: `share_read`/
// `share_write` non-empty entscheidet zuerst, `visibility` nur als Fallback ohne Freigaben.
export function visibilityLabel(item) {
  var shared = item.share_read.length > 0 || item.share_write.length > 0;
  if (shared) {
    var names = item.share_read.concat(item.share_write).filter(function (name, i, all) {
      return all.indexOf(name) === i;
    });
    return "geteilt mit " + names.join(", ");
  }
  return item.visibility === "private" ? "privat" : "nur ich";
}

export function visibilityChip(item) {
  var shared = item.share_read.length > 0 || item.share_write.length > 0;
  return el(
    "span", "visibility-chip" + (shared ? " visibility-chip--shared" : ""), visibilityLabel(item)
  );
}

// -- Verschieben: geteilter Schreibpfad für Menü (dialogs.js) und Drag & Drop (tree.js,
// Commit 4) — derselbe `_items_patch`-Aufruf, den Commit 3 schon nutzte, nur aus `dialogs.js`
// hierher gezogen, damit beide Auslöser ihn teilen statt ihn zu duplizieren. Erfolgsmeldung/
// Fehlerbehandlung bleiben bei den Aufrufern (Menü hält dafür einen Dialog offen, Drag & Drop
// nicht — zu wenig gemeinsam, um das auch noch zu teilen).
export function moveItemToFolder(item, folder) {
  return api("/items/" + encodeURIComponent(item.id), {
    method: "PATCH", body: JSON.stringify({ version: item.version, folder: folder }),
  }).then(function () {
    return loadItems().then(loadOverview);
  });
}

export function renderCrumb() {
  listCrumbEl.textContent = "";
  if (isGlobalScope()) {
    listCrumbEl.appendChild(el("strong", null, "Alle Items"));
  } else {
    var strong = el("strong", null, state.activeSpace || "");
    listCrumbEl.appendChild(strong);
    var label = state.folder ? state.folder : (BUCKET_LABELS[state.filter] || state.filter);
    listCrumbEl.appendChild(document.createTextNode(" › " + label));
  }
  // Im globalen Modus ist "nur lesen" kein sinnvoller Hinweis (es gibt keinen einen Space, auf
  // den er sich bezöge) — Banner bleibt dort ausgeblendet statt fälschlich sichtbar.
  listReadonlyEl.hidden = isGlobalScope() || activeSpaceWritable();
}

export function renderChips() {
  // §4.5: die aktiven Filter als ENTFERNBARE Chips. Bis Step 7b wurden Chips nur im
  // Leerzustand gezeigt und ließen sich nicht entfernen (`.chip__remove` war totes CSS).
  listChipsEl.textContent = "";
  if (!state.query) return;
  var chip = el("span", "chip");
  chip.appendChild(el("span", null, "Suche: " + state.query));
  var remove = el("button", "chip__remove");
  remove.appendChild(iconSvg("x"));
  remove.type = "button";
  remove.title = "Suche zurücksetzen";
  remove.addEventListener("click", function () {
    state.query = "";
    searchInputEl.value = "";
    clearSelection();   // §9.3 Punkt 1: Suche zurücksetzen zählt als Navigation
    loadItems().catch(reportUnexpectedError);
  });
  chip.appendChild(remove);
  listChipsEl.appendChild(chip);
}

// -- Mehrfachauswahl (§9, P6-AK–AN) ----------------------------------------------------------
// Auswahl leert sich bei jeder Navigation (tree.js :: activateView()/navigateAll()) — ohne diese
// Regel könnte eine Auswahl Items enthalten, die in der aktuellen Listenansicht gar nicht mehr
// sichtbar sind (§9.3 Punkt 1).

export function clearSelection() {
  if (state.selectedItemIds.size === 0) return;
  state.selectedItemIds.clear();
}

function toggleSelected(id) {
  if (state.selectedItemIds.has(id)) state.selectedItemIds.delete(id);
  else state.selectedItemIds.add(id);
  renderList();
}

function renderSelectionToolbar() {
  var count = state.selectedItemIds.size;
  listSelectionEl.hidden = count === 0;
  if (count === 0) return;
  listSelectionCountEl.textContent = count + " ausgewählt";
}

// Zweirunden-Batch-Move (P6-AL/AM), kein neuer Endpunkt — eine sequenzielle Schleife über den
// bereits gebauten Einzel-Move-Pfad (`PATCH /api/v1/items/{id}`, Step 7b). Sequenziell statt
// parallel: `LoginThrottle` ist dieselbe Bremse wie beim UI-Login, parallele Requests könnten sie
// bei einem einzigen falschen Credential-Versuch unnötig strapazieren. `credentials` ist `null`
// für Runde 1 (kein Widen angenommen, P6-AM) oder `{password, totp}` für die Wiederholung der in
// Runde 1 zurückgewiesenen Items. Löst nie selbst auf/ab — der Aufrufer (dialogs.js) entscheidet
// anhand von `results[i].code === "reauth_required"`, ob eine zweite Runde nötig ist.
export function moveSelectedItems(items, target, credentials, onProgress) {
  var results = [];
  var i = 0;
  function next() {
    if (i >= items.length) return Promise.resolve(results);
    var item = items[i];
    var body = Object.assign({ version: item.version, folder: target.folder }, credentials || {});
    if (target.space && target.space !== item.space) body.space = target.space;
    if (onProgress) onProgress(i + 1, items.length);
    return api("/items/" + encodeURIComponent(item.id), {
      method: "PATCH", body: JSON.stringify(body),
    }).then(function () {
      results.push({ item: item, ok: true });
    }).catch(function (err) {
      // Abgelaufene Sitzung mitten im Batch: `api.js` hat die "Sitzung abgelaufen"-Karte bereits
      // synchron gezeigt (dieselbe Unterdrückung wie im Einzel-Move, `err.message ===
      // "unauthenticated"` dort) -- jeder weitere Request würde ohnehin nur wieder 401 liefern.
      // Batch hier abbrechen statt jedes verbleibende Item als "fehlgeschlagen" zu melden.
      if (err && err.message === "unauthenticated") {
        i = items.length;
        return;
      }
      results.push({ item: item, ok: false, code: err.code, message: err.message });
    }).then(function () { i++; return next(); });
  }
  return next();
}

export function renderList() {
  listRowsEl.textContent = "";
  renderChips();
  renderSelectionToolbar();

  if (state.items.length === 0) {
    listEmptyEl.hidden = false;
    if (isGlobalScope()) {
      listEmptyTextEl.textContent = state.query
        ? "Keine Treffer für „" + state.query + "“."
        : "Keine lesbaren Items.";
    } else if (state.query) {
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
    if (state.selectedItemIds.has(item.id)) li.classList.add("list__row--selected");
    var button = el("button", "list__row");
    button.type = "button";
    button.dataset.id = item.id;
    if (item.id === state.selectedId) button.setAttribute("aria-current", "true");
    button.appendChild(el("div", "list__row-title", item.title));
    var metaEl = el("div", "list__row-meta tnum");
    metaEl.appendChild(el("span", null, itemMetaLine(item)));
    metaEl.appendChild(visibilityChip(item));
    button.appendChild(metaEl);
    var movable = !item.readonly && item.space === state.ownSpace;
    button.addEventListener("click", function (event) {
      // Strg+Klick (Nikinger-Vorgabe, §9.3 Punkt 1) togglet statt zu öffnen — nur für Items, die
      // sich überhaupt in einem Batch verschieben ließen (dieselbe `movable`-Bedingung wie der
      // Verschieben-Knopf unten).
      if (movable && (event.ctrlKey || event.metaKey)) {
        toggleSelected(item.id);
        return;
      }
      selectItem(item.id).catch(reportUnexpectedError);
    });
    li.appendChild(button);
    if (movable) {
      // Long-Press (Nikinger-Vorgabe, zweiter Auslöser neben Strg+Klick) — nur für Touch/Pen,
      // eine Maus deckt bereits Strg+Klick ab. Best-effort: P5-W lässt diese App bewusst
      // Desktop-first, kein dedizierter Touch-Testlauf für diesen Pfad.
      var longPressTimer = null;
      li.addEventListener("pointerdown", function (event) {
        if (event.pointerType === "mouse") return;
        longPressTimer = setTimeout(function () { toggleSelected(item.id); }, 500);
      });
      li.addEventListener("pointerup", function () { clearTimeout(longPressTimer); });
      li.addEventListener("pointerleave", function () { clearTimeout(longPressTimer); });
    }
    // Verschieben-Knopf als GESCHWISTER von `.list__row`, nicht darin verschachtelt — zwei
    // `<button>` ineinander ist ungültiges HTML und Browser hangeln das eine daraus hervor,
    // was den Klick-Handler unvorhersehbar macht. `.list__rows > li` ist deshalb Flex (app.css),
    // `.list__row` nimmt den Platz, dieser Knopf bleibt fest daneben. Nur fürs eigene,
    // schreibbare Item — der Server lehnt einen Ordnerwechsel an einem fremden Item ohnehin ab
    // (`_items_patch`s Eigentümer-Riegel), der Knopf zeigt also nur, was wirklich erlaubt ist.
    // Menü-Knopf bleibt die Pflicht-Alternative zu Drag & Drop (P6-AB) — dieselbe
    // `movable`-Bedingung entscheidet über beide, nicht nur über den Knopf (jetzt oben einmal
    // berechnet, §9 braucht sie zusätzlich für Strg+Klick/Long-Press).
    if (movable) {
      var moveButton = el("button", "list__row-move");
      moveButton.type = "button";
      moveButton.title = "In Ordner verschieben";
      moveButton.setAttribute("aria-label", "In Ordner verschieben");
      moveButton.appendChild(iconSvg("folder-input"));
      moveButton.addEventListener("click", function (event) {
        event.stopPropagation();
        openMoveDialog(item);
      });
      li.appendChild(moveButton);

      // Freigeben-Knopf (Step 7 Commit 5b) — dieselbe Geschwister-Regel wie der
      // Verschieben-Knopf, aus demselben Grund (zwei `<button>` ineinander wäre ungültiges
      // HTML). Dieselbe `movable`-Bedingung: nur ein eigenes, schreibbares Item lässt sich
      // freigeben (eine UI-seitige Einschränkung, keine zusätzliche Serverregel — `_items_patch`
      // selbst prüft `share_read`/`share_write`-Änderungen nicht auf Eigentümerschaft, siehe
      // `api.py`s `folder`-Riegel-Kommentar; dieser Knopf zeigt bewusst nur den einfachsten,
      // erwarteten Fall).
      var shareButton = el("button", "list__row-share");
      shareButton.type = "button";
      shareButton.title = "Freigeben";
      shareButton.setAttribute("aria-label", "Freigeben");
      shareButton.appendChild(iconSvg("share-2"));
      shareButton.addEventListener("click", function (event) {
        event.stopPropagation();
        openShareDialog(item);
      });
      li.appendChild(shareButton);

      // Drag & Drop (Step 7 Commit 4) — die `<li>` ist der Ziehgriff, nicht `.list__row`,
      // damit ein Klick auf den Button weiterhin normal öffnet/navigiert; nur `dragstart`
      // trägt die Nutzlast (Item-ID), die Zielseite (tree.js) löst sie über `state.items` auf.
      li.draggable = true;
      li.classList.add("list__row-draggable");
      li.addEventListener("dragstart", function (event) {
        event.dataTransfer.setData("text/plain", item.id);
        event.dataTransfer.effectAllowed = "move";
        li.classList.add("list__row-draggable--active");
      });
      li.addEventListener("dragend", function () {
        li.classList.remove("list__row-draggable--active");
      });
    }
    listRowsEl.appendChild(li);
  });
}

export function filterParams() {
  // P6-AQ, die kritischste Zeile dieses Plans: ohne diesen Riegel würde `state.filter`s Default
  // ("open") den globalen Modus auf `type=task&status=open` einschränken — eine fremde Notiz
  // bliebe dann weiterhin unauffindbar, ein fix-förmiges No-Op.
  if (isGlobalScope()) return {};
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
  if (state.activeSpace && !isGlobalScope()) params.set("space", state.activeSpace);
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

  listSelectionEl = document.getElementById("list-selection");
  listSelectionCountEl = document.getElementById("list-selection-count");
  listSelectionMoveEl = document.getElementById("list-selection-move");
  listSelectionClearEl = document.getElementById("list-selection-clear");

  listSelectionMoveEl.addEventListener("click", function () {
    var items = state.items.filter(function (item) { return state.selectedItemIds.has(item.id); });
    if (items.length) openMoveDialog(items);
  });
  listSelectionClearEl.addEventListener("click", function () {
    state.selectedItemIds.clear();
    renderList();
  });

  overviewTitleEl = document.getElementById("overview-title");
  overviewTilesEl = document.getElementById("overview-tiles");
  overviewRecentEl = document.getElementById("overview-recent");
  overviewForeignEl = document.getElementById("overview-foreign");

  // -- Suche (200ms Debounce) -----------------------------------------------------------
  var searchTimer = null;
  searchInputEl.addEventListener("input", function () {
    state.query = searchInputEl.value;
    clearSelection();   // §9.3 Punkt 1: Suche zählt als Navigation
    clearTimeout(searchTimer);
    searchTimer = setTimeout(function () { loadItems().catch(reportUnexpectedError); }, 200);
  });
}
