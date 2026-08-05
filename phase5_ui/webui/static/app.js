"use strict";

// -- Bootstrap: Übernahme des CSRF-Tokens von der Login-Erfolgsseite (Plan-Abweichung 2,
// phase5_ui/CLAUDE.md Session-Block 2026-08-05) --------------------------------------------
// `routes_auth.py :: _login_post()` liefert den CSRF-Token nur EIN einziges Mal als Klartext
// (`ui_sessions` speichert nur den Hash) — als verstecktes Feld auf genau dieser Seite. Diese
// Datei läuft dort UND auf der echten Shell (`/ui/`); auf der Erfolgsseite existiert kein
// `#shell`, das unterscheidet die beiden Fälle ohne zusätzliches Signal.
(function bootstrapCsrf() {
  var csrfField = document.querySelector('input[name="csrf"]');
  if (csrfField && location.pathname !== "/ui/") {
    sessionStorage.setItem("sfx:csrf", csrfField.value);
    location.replace("/ui/");
  }
})();

var shellEl = document.getElementById("shell");
if (shellEl) {
  initShell();
}

function initShell() {
  var API_BASE = "/api/v1";

  var state = {
    spaces: [],
    ownSpace: null,
    activeSpace: null,
    filter: "open",
    query: "",
    items: [],
    selectedId: null,
  };

  // -- API-Client -------------------------------------------------------------------------

  function csrfToken() {
    return sessionStorage.getItem("sfx:csrf");
  }

  function api(path, opts) {
    opts = opts || {};
    var method = opts.method || "GET";
    var headers = Object.assign({ "Content-Type": "application/json" }, opts.headers || {});
    if (method !== "GET" && method !== "HEAD") {
      var token = csrfToken();
      if (token) headers["X-CSRF-Token"] = token;
    }
    return fetch(API_BASE + path, Object.assign({}, opts, { method: method, headers: headers })).then(
      function (response) {
        if (response.status === 401) {
          // Kein Entwurfsschutz nötig (Plan-Abweichung 2): Step 6 hat noch nichts Eingetipptes
          // zu verlieren. Step 7 ersetzt das durch die volle "Sitzung abgelaufen"-Karte (§4.5),
          // sobald der Editor existiert.
          location.replace("/ui/login");
          return Promise.reject(new Error("unauthenticated"));
        }
        return response.json().catch(function () { return null; }).then(function (body) {
          if (!response.ok) {
            var err = new Error((body && body.message) || response.statusText);
            err.code = body && body.error;
            return Promise.reject(err);
          }
          return body;
        });
      }
    );
  }

  // -- Render ------------------------------------------------------------------------------

  var railSpacesEl = document.getElementById("rail-spaces");
  var listRowsEl = document.getElementById("list-rows");
  var listEmptyEl = document.getElementById("list-empty");
  var listChipsEl = document.getElementById("list-chips");
  var detailEmptyEl = document.getElementById("detail-empty");
  var detailContentEl = document.getElementById("detail-content");
  var detailTitleEl = document.getElementById("detail-title");
  var detailMetaEl = document.getElementById("detail-meta");
  var detailBodyEl = document.getElementById("detail-body");
  var searchInputEl = document.getElementById("search-input");

  function el(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function renderRail() {
    railSpacesEl.textContent = "";
    state.spaces.forEach(function (space) {
      var button = el("button", "rail__space");
      button.type = "button";
      button.dataset.space = space.name;
      if (space.name === state.activeSpace) button.setAttribute("aria-current", "true");
      var glyph = el("span", "rail__glyph", space.name.charAt(0).toUpperCase());
      var label = el("span", "rail__label", space.name + (space.own ? "" : " · nur lesen"));
      button.appendChild(glyph);
      button.appendChild(label);
      button.addEventListener("click", function () {
        state.activeSpace = space.name;
        renderRail();
        loadItems();
      });
      railSpacesEl.appendChild(button);
    });
  }

  function itemMetaLine(item) {
    var parts = [item.type, item.status];
    if (item.due) parts.push(item.due);
    if (item.tags && item.tags.length) parts.push(item.tags.join(", "));
    return parts.join(" · ");
  }

  function renderList() {
    listRowsEl.textContent = "";
    listChipsEl.textContent = "";
    if (state.items.length === 0) {
      listEmptyEl.hidden = false;
      if (state.query || state.activeSpace !== state.ownSpace) {
        var chip = el("span", "chip", "Filter: " + state.filter);
        listChipsEl.appendChild(chip);
      }
      return;
    }
    listEmptyEl.hidden = true;
    state.items.forEach(function (item) {
      var li = el("li");
      var button = el("button", "list__row");
      button.type = "button";
      button.dataset.id = item.id;
      if (item.id === state.selectedId) button.setAttribute("aria-current", "true");
      button.appendChild(el("div", "list__row-title", item.title));
      button.appendChild(el("div", "list__row-meta tnum", itemMetaLine(item)));
      button.addEventListener("click", function () { selectItem(item.id); });
      li.appendChild(button);
      listRowsEl.appendChild(li);
    });
  }

  function renderDetail(item) {
    detailEmptyEl.hidden = true;
    detailContentEl.hidden = false;
    detailTitleEl.textContent = item.title;
    detailMetaEl.textContent = "";
    var badgeHost = detailMetaEl;
    if (item.readonly) {
      var badge = el("span", "detail__badge-readonly", "Nur lesen — fremder Space");
      badgeHost.appendChild(badge);
    }
    badgeHost.appendChild(el("span", "tnum", "v" + item.version));
    badgeHost.appendChild(el("span", null, item.type + " · " + item.status));
    if (item.due) badgeHost.appendChild(el("span", "tnum", "fällig " + item.due));
    detailBodyEl.textContent = item.body;
    shellEl.dataset.view = "detail";
  }

  function clearDetail() {
    state.selectedId = null;
    detailEmptyEl.hidden = false;
    detailContentEl.hidden = true;
  }

  // -- Laden ---------------------------------------------------------------------------------

  function filterParams() {
    // "Offen": Aufgaben ohne Abschluss. "Notizen": aktive Notizen. "Archiv": alles Archivierte,
    // typunabhängig — dieselbe Aufteilung wie die drei Rail-Beschriftungen im Mockup (§4.3).
    if (state.filter === "note") return { type: "note", status: "active" };
    if (state.filter === "archived") return { status: "archived" };
    return { type: "task", status: "open" };
  }

  function loadItems() {
    var params = new URLSearchParams(filterParams());
    if (state.activeSpace) params.set("space", state.activeSpace);
    if (state.query) params.set("query", state.query);
    return api("/items?" + params.toString()).then(function (result) {
      state.items = result.items;
      renderList();
    });
  }

  function selectItem(id) {
    state.selectedId = id;
    renderList();
    return api("/items/" + encodeURIComponent(id)).then(renderDetail);
  }

  function init() {
    return api("/me")
      .then(function (me) {
        state.ownSpace = me.space;
        state.activeSpace = me.space;
        return api("/spaces");
      })
      .then(function (spaces) {
        state.spaces = spaces;
        renderRail();
        return loadItems();
      });
  }

  // -- Suche (200ms Debounce) -----------------------------------------------------------

  var searchTimer = null;
  searchInputEl.addEventListener("input", function () {
    state.query = searchInputEl.value;
    clearTimeout(searchTimer);
    searchTimer = setTimeout(loadItems, 200);
  });

  // -- Filter-Buttons ---------------------------------------------------------------------

  document.querySelectorAll(".rail__filter").forEach(function (button) {
    button.addEventListener("click", function () {
      document.querySelectorAll(".rail__filter").forEach(function (b) {
        b.removeAttribute("aria-current");
      });
      button.setAttribute("aria-current", "true");
      state.filter = button.dataset.filter;
      loadItems();
    });
  });

  // -- Logout / Zurück ---------------------------------------------------------------------

  document.getElementById("logout-button").addEventListener("click", function () {
    fetch("/ui/logout", { method: "POST", headers: { "X-CSRF-Token": csrfToken() || "" } }).then(
      function () { location.replace("/ui/login"); }
    );
  });

  document.getElementById("back-button").addEventListener("click", function () {
    shellEl.dataset.view = "list";
  });

  // -- Tastatur (§4.6) ----------------------------------------------------------------------
  // `Esc`/`Ctrl+S` sind hier bewusst NICHT gebunden: Step 6 hat keinen Dialog zu schließen und
  // nichts zu speichern (kein Editor, das ist Step 7) — eine tote Tastenbindung wäre schlechter
  // als eine fehlende.
  document.addEventListener("keydown", function (event) {
    var tag = document.activeElement && document.activeElement.tagName;
    var inField = tag === "INPUT" || tag === "TEXTAREA";
    if (event.key === "/" && !inField) {
      event.preventDefault();
      searchInputEl.focus();
      return;
    }
    if ((event.key === "ArrowDown" || event.key === "ArrowUp") && !inField) {
      event.preventDefault();
      var ids = state.items.map(function (item) { return item.id; });
      if (ids.length === 0) return;
      var currentIndex = ids.indexOf(state.selectedId);
      var step = event.key === "ArrowDown" ? 1 : -1;
      var nextIndex = currentIndex === -1 ? 0 : Math.min(ids.length - 1, Math.max(0, currentIndex + step));
      selectItem(ids[nextIndex]);
    }
  });

  clearDetail();
  init();
}
