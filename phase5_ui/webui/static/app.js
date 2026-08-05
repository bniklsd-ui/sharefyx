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

// -- Markdown/Sanitizer (Plan §3.5, Step 7) --------------------------------------------------
// Geerntet aus docs/concepts/notiz_heft_example.html (sanitizeHtml/markdownToHtml/safeHref,
// Zeilen 212-275) und erweitert: h1-h4 (Quelle nur h1-h3), Zitate + GFM-Tabellen (Quelle hat
// keins von beidem). NICHT übernommen: Style-Attribute (unsere CSP `style-src 'self'` ohne
// `unsafe-inline` verhindert ohnehin, dass ein `style="..."` je greift), IMG/FIGURE/FONT/
// `data-asset-*` (kein Anhang-Feature, P5-AA), Task-Checklisten (nicht in §3.5s Teilmenge),
// `tel:`/`#note:`/`#asset:` (§3.5 nennt nur http/https/mailto/#item/<id>).
//
// Pipeline exakt wie §3.5: sanitizeHtml(markdownToHtml(escapeHtml(src))) — das Vor-Escaping der
// GESAMTEN Quelle stört keine Markdown-Syntax (#, *, Backtick, [](), -, |, : sind keine
// HTML-Sonderzeichen), macht aber literales `<script>` im Nutzertext schon vor dem Parser
// inert. Einzige Folge: `>` (Zitat-Marker) kommt als `&gt;` an, die Zitat-Erkennung matcht
// deshalb gegen `&gt;`, nicht `>`.

function escapeHtml(value) {
  return String(value == null ? "" : value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function inlineMarkdown(escaped) {
  return escaped
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/\*([^*]+)\*/g, "<em>$1</em>")
    .replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, '<a href="$2">$1</a>');
}

function splitTableRow(line) {
  var trimmed = line.trim();
  if (trimmed.charAt(0) === "|") trimmed = trimmed.slice(1);
  if (trimmed.charAt(trimmed.length - 1) === "|") trimmed = trimmed.slice(0, -1);
  return trimmed.split("|");
}

function cellAlignClass(token) {
  var t = token.trim();
  var left = t.charAt(0) === ":";
  var right = t.charAt(t.length - 1) === ":";
  if (left && right) return "ta-c";
  if (right) return "ta-r";
  if (left) return "ta-l";
  return "";
}

var TABLE_SEPARATOR_RE = /^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?\s*$/;

function markdownToHtml(src) {
  var lines = escapeHtml(src).replace(/\r\n/g, "\n").split("\n");
  var out = "";
  var i = 0;
  var listType = null;
  var paragraph = [];

  function flushParagraph() {
    if (paragraph.length) {
      out += "<p>" + inlineMarkdown(paragraph.join(" ")) + "</p>";
      paragraph = [];
    }
  }
  function closeList() {
    if (listType) {
      out += listType === "ul" ? "</ul>" : "</ol>";
      listType = null;
    }
  }

  while (i < lines.length) {
    var line = lines[i];
    var m;

    if (/^```/.test(line)) {
      flushParagraph();
      closeList();
      out += "<pre><code>";
      i++;
      while (i < lines.length && !/^```/.test(lines[i])) {
        out += lines[i] + "\n";
        i++;
      }
      out += "</code></pre>";
      i++;
      continue;
    }

    if (line.indexOf("|") !== -1 && i + 1 < lines.length && TABLE_SEPARATOR_RE.test(lines[i + 1])) {
      flushParagraph();
      closeList();
      var headerCells = splitTableRow(line);
      var aligns = splitTableRow(lines[i + 1]).map(cellAlignClass);
      out += "<table><thead><tr>";
      headerCells.forEach(function (cell, idx) {
        var cls = aligns[idx] ? ' class="' + aligns[idx] + '"' : "";
        out += "<th" + cls + ">" + inlineMarkdown(cell.trim()) + "</th>";
      });
      out += "</tr></thead><tbody>";
      i += 2;
      while (i < lines.length && lines[i].indexOf("|") !== -1 && lines[i].trim() !== "") {
        var cells = splitTableRow(lines[i]);
        out += "<tr>";
        cells.forEach(function (cell, idx) {
          var cls = aligns[idx] ? ' class="' + aligns[idx] + '"' : "";
          out += "<td" + cls + ">" + inlineMarkdown(cell.trim()) + "</td>";
        });
        out += "</tr>";
        i++;
      }
      out += "</tbody></table>";
      continue;
    }

    if ((m = line.match(/^(#{1,4})\s+(.*)$/))) {
      flushParagraph();
      closeList();
      var level = m[1].length;
      out += "<h" + level + ">" + inlineMarkdown(m[2]) + "</h" + level + ">";
      i++;
      continue;
    }

    if ((m = line.match(/^&gt;\s?(.*)$/))) {
      flushParagraph();
      closeList();
      var quoteLines = [m[1]];
      i++;
      while (i < lines.length && (m = lines[i].match(/^&gt;\s?(.*)$/))) {
        quoteLines.push(m[1]);
        i++;
      }
      out += "<blockquote>" + quoteLines.map(function (l) { return "<p>" + inlineMarkdown(l) + "</p>"; }).join("") + "</blockquote>";
      continue;
    }

    if ((m = line.match(/^[-*]\s+(.*)$/))) {
      flushParagraph();
      if (listType !== "ul") {
        closeList();
        out += "<ul>";
        listType = "ul";
      }
      out += "<li>" + inlineMarkdown(m[1]) + "</li>";
      i++;
      continue;
    }

    if ((m = line.match(/^\d+\.\s+(.*)$/))) {
      flushParagraph();
      if (listType !== "ol") {
        closeList();
        out += "<ol>";
        listType = "ol";
      }
      out += "<li>" + inlineMarkdown(m[1]) + "</li>";
      i++;
      continue;
    }

    if (/^(-{3,}|\*{3,}|_{3,})$/.test(line.trim())) {
      flushParagraph();
      closeList();
      out += "<hr>";
      i++;
      continue;
    }

    if (line.trim() === "") {
      flushParagraph();
      closeList();
      i++;
      continue;
    }

    closeList();
    paragraph.push(line.trim());
    i++;
  }
  flushParagraph();
  closeList();
  return sanitizeHtml(out);
}

var ALLOWED_TAGS = new Set([
  "P", "BR", "STRONG", "EM", "CODE", "PRE", "H1", "H2", "H3", "H4",
  "UL", "OL", "LI", "BLOCKQUOTE", "A", "TABLE", "THEAD", "TBODY", "TR", "TD", "TH", "HR",
]);
var ALLOWED_ATTRS = {
  A: new Set(["href", "target", "rel"]),
  TD: new Set(["class"]),
  TH: new Set(["class"]),
};
var ALLOWED_CELL_CLASSES = new Set(["ta-l", "ta-c", "ta-r"]);

function safeHref(href) {
  var h = (href || "").trim();
  if (/^#item\/[a-zA-Z0-9_-]+$/.test(h)) return h;
  if (/^(https?:|mailto:)/i.test(h)) return h;
  return "";
}

function sanitizeHtml(html) {
  var template = document.createElement("template");
  template.innerHTML = html || "";

  function walk(node) {
    var children = [].slice.call(node.children);
    for (var idx = 0; idx < children.length; idx++) {
      var child = children[idx];
      if (!ALLOWED_TAGS.has(child.tagName)) {
        child.replaceWith.apply(child, [].slice.call(child.childNodes));
        walk(node);
        return;
      }
      var allowed = ALLOWED_ATTRS[child.tagName] || new Set();
      [].slice.call(child.attributes).forEach(function (attr) {
        if (!allowed.has(attr.name.toLowerCase())) child.removeAttribute(attr.name);
      });
      if ((child.tagName === "TD" || child.tagName === "TH") && child.hasAttribute("class")) {
        if (!ALLOWED_CELL_CLASSES.has(child.getAttribute("class"))) child.removeAttribute("class");
      }
      if (child.tagName === "A") {
        var safe = safeHref(child.getAttribute("href"));
        if (safe) {
          child.setAttribute("href", safe);
          if (/^https?:/i.test(safe)) {
            child.setAttribute("target", "_blank");
            child.setAttribute("rel", "noopener noreferrer");
          } else {
            child.removeAttribute("target");
            child.removeAttribute("rel");
          }
        } else {
          child.removeAttribute("href");
        }
      }
      walk(child);
    }
  }
  walk(template.content);
  return template.innerHTML;
}

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
    meta: null,
    mode: "edit",
    editingSnapshot: null,
    conflictCurrent: null,
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
          // Step 7: keine sofortige Navigation mehr (anders als Step 6) — eine ganzflächige
          // Karte statt eines Redirects mitten im Tippen, §4.5. Der Entwurf liegt bereits in
          // sessionStorage (draftKeyFor()), geht durch das Stehenbleiben auf der Seite nicht
          // verloren; "Erneut anmelden" navigiert bewusst voll zu /ui/login (Plan-Entscheidung,
          // kein zweiter Login-Endpunkt) und der Bootstrap-Redirect zurück zu /ui/ landet wieder
          // hier, der Entwurf wird beim erneuten Öffnen des Items angeboten.
          showSessionExpiredCard();
          return Promise.reject(new Error("unauthenticated"));
        }
        return response.json().catch(function () { return null; }).then(function (body) {
          if (!response.ok) {
            var err = new Error((body && body.message) || response.statusText);
            err.code = body && body.error;
            err.detail = body && body.detail;
            return Promise.reject(err);
          }
          return body;
        });
      }
    );
  }

  // Für Aufrufe, die aus Event-Handlern lose angestoßen werden (Laden, Auswählen, Init) statt
  // aus einer Nutzeraktion mit eigener Fehlerbehandlung (Speichern/Anhängen/Archivieren/
  // Anlegen haben je eigene `.catch()`): ohne dieses Netz bliebe die von `api()`s 401-Zweig
  // zurückgegebene Promise unbehandelt — die "Sitzung abgelaufen"-Karte erscheint zwar trotzdem
  // (das passiert synchron in `api()`, bevor verworfen wird), aber eine unbehandelte Ablehnung
  // ist unnötiger Lärm in der Konsole und in strengeren Laufzeiten (Fund dieser Session: Node
  // bricht bei einer unbehandelten Promise-Ablehnung den Prozess ab, ein Browser nur eine
  // Konsolenwarnung — trotzdem sauber behandeln, nicht auf das mildere Browser-Verhalten
  // verlassen).
  function reportUnexpectedError(err) {
    if (err && err.message === "unauthenticated") return;
    console.error(err);
  }

  // -- DOM-Referenzen -----------------------------------------------------------------------

  var railSpacesEl = document.getElementById("rail-spaces");
  var listRowsEl = document.getElementById("list-rows");
  var listEmptyEl = document.getElementById("list-empty");
  var listChipsEl = document.getElementById("list-chips");
  var searchInputEl = document.getElementById("search-input");
  var createButtonEl = document.getElementById("create-button");
  var newItemButtonEl = document.getElementById("new-item-button");

  var detailEmptyEl = document.getElementById("detail-empty");
  var detailReadonlyEl = document.getElementById("detail-readonly");
  var roTitleEl = document.getElementById("ro-title");
  var roMetaEl = document.getElementById("ro-meta");
  var roPreviewEl = document.getElementById("ro-preview");

  var detailEditorEl = document.getElementById("detail-editor");
  var versionBandEl = document.getElementById("version-band");
  var versionBandNumberEl = document.getElementById("version-band-number");
  var fieldTitleEl = document.getElementById("field-title");
  var fieldStatusEl = document.getElementById("field-status");
  var fieldDueEl = document.getElementById("field-due");
  var fieldTagsEl = document.getElementById("field-tags");
  var fieldLinksEl = document.getElementById("field-links");
  var editorToolbarEl = document.getElementById("editor-toolbar");
  var togglePreviewButtonEl = document.getElementById("toggle-preview");
  var editorTextareaEl = document.getElementById("editor-textarea");
  var editorPreviewEl = document.getElementById("editor-preview");
  var saveButtonEl = document.getElementById("save-button");
  var archiveButtonEl = document.getElementById("archive-button");
  var appendInputEl = document.getElementById("append-input");
  var appendButtonEl = document.getElementById("append-button");

  var createDialogEl = document.getElementById("create-dialog");
  var createTypeEl = document.getElementById("create-type");
  var createTitleInputEl = document.getElementById("create-title-input");
  var createSubmitButtonEl = document.getElementById("create-submit");
  var createCancelButtonEl = document.getElementById("create-cancel");

  var conflictDialogEl = document.getElementById("conflict-dialog");
  var conflictMessageEl = document.getElementById("conflict-message");
  var conflictLoadCurrentButtonEl = document.getElementById("conflict-load-current");
  var conflictSaveAsNewButtonEl = document.getElementById("conflict-save-as-new");
  var conflictCancelButtonEl = document.getElementById("conflict-cancel");

  var sessionExpiredCardEl = document.getElementById("session-expired-card");

  function el(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function showSessionExpiredCard() {
    sessionExpiredCardEl.hidden = false;
  }

  // -- Rail/Liste (Step 6, unverändert) ------------------------------------------------------

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
    }).catch(reportUnexpectedError);
  }

  // -- Detail: Nur-lesen (fremder Space) vs. Editor (eigener Space) -------------------------

  function clearDetail() {
    state.selectedId = null;
    state.editingSnapshot = null;
    state.conflictCurrent = null;
    detailEmptyEl.hidden = false;
    detailReadonlyEl.hidden = true;
    detailEditorEl.hidden = true;
  }

  function snapshotFromItem(item) {
    return {
      id: item.id, type: item.type, version: item.version,
      title: item.title, body: item.body, status: item.status,
      due: item.due, tags: item.tags.slice(), links: item.links.slice(),
    };
  }

  function currentFormValues() {
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

  function updateVersionBand() {
    versionBandEl.classList.remove("is-dirty", "is-conflict");
    if (!state.editingSnapshot) {
      versionBandNumberEl.textContent = "";
      return;
    }
    if (state.conflictCurrent) {
      versionBandEl.classList.add("is-conflict");
      versionBandNumberEl.textContent = "v" + state.editingSnapshot.version + " → v" + state.conflictCurrent.version;
    } else if (isDirty()) {
      versionBandEl.classList.add("is-dirty");
      versionBandNumberEl.textContent = "v" + state.editingSnapshot.version + "+";
    } else {
      versionBandNumberEl.textContent = "v" + state.editingSnapshot.version;
    }
  }

  // -- Entwurfsschutz (§4.5): sessionStorage, nie localStorage, nur für den eigenen Tab und
  // nur für Items, die man gerade bearbeitet (nicht für fremde/schreibgeschützte Items — die
  // haben keinen Editor).

  function draftKeyFor(id) { return "sfx:draft:" + id; }

  function saveDraft() {
    if (!state.selectedId) return;
    sessionStorage.setItem(draftKeyFor(state.selectedId), JSON.stringify(currentFormValues()));
  }

  function clearDraft(id) {
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
    editorToolbarEl.hidden = mode !== "edit";
    editorPreviewEl.hidden = mode !== "preview";
    togglePreviewButtonEl.textContent = mode === "edit" ? "Vorschau" : "Bearbeiten";
    if (mode === "preview") {
      editorPreviewEl.innerHTML = markdownToHtml(editorTextareaEl.value);
    }
  }

  function loadEditorFromItem(item) {
    state.selectedId = item.id;
    state.conflictCurrent = null;
    conflictDialogEl.hidden = true;
    detailEmptyEl.hidden = true;

    if (item.readonly) {
      detailEditorEl.hidden = true;
      detailReadonlyEl.hidden = false;
      roTitleEl.textContent = item.title;
      roMetaEl.textContent = "";
      roMetaEl.appendChild(el("span", "detail__badge-readonly", "Nur lesen — fremder Space (" + item.space + ")"));
      roMetaEl.appendChild(el("span", "tnum", "v" + item.version));
      roMetaEl.appendChild(el("span", null, item.type + " · " + item.status));
      if (item.due) roMetaEl.appendChild(el("span", "tnum", "fällig " + item.due));
      roPreviewEl.innerHTML = markdownToHtml(item.body);
    } else {
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
      setEditorMode("edit");

      var draft = loadDraftIfAny(item.id);
      if (draft && (draft.title !== item.title || draft.body !== item.body)) {
        if (window.confirm("Es gibt einen ungespeicherten Entwurf für dieses Item. Wiederherstellen?")) {
          fieldTitleEl.value = draft.title;
          editorTextareaEl.value = draft.body;
          fieldStatusEl.value = draft.status;
          fieldDueEl.value = draft.due || "";
          fieldTagsEl.value = draft.tags.join(", ");
          fieldLinksEl.value = draft.links.join(", ");
        } else {
          clearDraft(item.id);
        }
      }
      updateVersionBand();
    }
    shellEl.dataset.view = "detail";
    renderList();
  }

  function selectItem(id) {
    state.selectedId = id;
    renderList();
    return api("/items/" + encodeURIComponent(id)).then(loadEditorFromItem).catch(reportUnexpectedError);
  }

  // -- Speichern / Konflikt (§4.5, Akzeptanzkriterium 11) ------------------------------------

  function showConflictDialog(current) {
    state.conflictCurrent = current;
    updateVersionBand();
    conflictMessageEl.textContent =
      "Ein anderer Client hat dieses Item zwischenzeitlich geändert (deine Version v"
      + state.editingSnapshot.version + " → aktuelle Version v" + current.version + ").";
    conflictDialogEl.hidden = false;
  }

  function hideConflictDialog() {
    conflictDialogEl.hidden = true;
    state.conflictCurrent = null;
    updateVersionBand();
  }

  function saveItem() {
    var payload = Object.assign(
      { version: state.editingSnapshot.version, format: "markdown" }, currentFormValues()
    );
    return api("/items/" + encodeURIComponent(state.selectedId), {
      method: "PATCH", body: JSON.stringify(payload),
    }).then(function (item) {
      clearDraft(item.id);
      return loadItems().then(function () { loadEditorFromItem(item); });
    }).catch(function (err) {
      if (err.code === "conflict") showConflictDialog(err.detail.current);
      else if (err.message !== "unauthenticated") window.alert(err.message || "Speichern fehlgeschlagen.");
    });
  }

  saveButtonEl.addEventListener("click", saveItem);

  conflictLoadCurrentButtonEl.addEventListener("click", function () {
    var current = state.conflictCurrent;
    clearDraft(current.id);
    hideConflictDialog();
    loadEditorFromItem(current);
  });

  conflictSaveAsNewButtonEl.addEventListener("click", function () {
    var values = currentFormValues();
    var payload = Object.assign({ type: state.editingSnapshot.type, format: "markdown" }, values);
    var previousId = state.selectedId;
    hideConflictDialog();
    api("/items", { method: "POST", body: JSON.stringify(payload) }).then(function (item) {
      clearDraft(previousId);
      return loadItems().then(function () { loadEditorFromItem(item); });
    }).catch(function (err) {
      if (err.message !== "unauthenticated") window.alert(err.message || "Anlegen fehlgeschlagen.");
    });
  });

  conflictCancelButtonEl.addEventListener("click", hideConflictDialog);

  // -- Anhängen (eigener Pfad, nicht über PATCH — siehe Moduldocstring-Pendant server-seitig) -

  appendButtonEl.addEventListener("click", function () {
    var text = appendInputEl.value.trim();
    if (!text || !state.editingSnapshot) return;
    api("/items/" + encodeURIComponent(state.selectedId) + "/append", {
      method: "POST", body: JSON.stringify({ version: state.editingSnapshot.version, text: text }),
    }).then(function (item) {
      appendInputEl.value = "";
      return loadItems().then(function () { loadEditorFromItem(item); });
    }).catch(function (err) {
      if (err.code === "conflict") showConflictDialog(err.detail.current);
      else if (err.message !== "unauthenticated") window.alert(err.message || "Anhängen fehlgeschlagen.");
    });
  });

  // -- Archivieren ---------------------------------------------------------------------------

  archiveButtonEl.addEventListener("click", function () {
    if (!state.editingSnapshot) return;
    if (!window.confirm("Item wirklich archivieren?")) return;
    api("/items/" + encodeURIComponent(state.selectedId) + "/archive", {
      method: "POST", body: JSON.stringify({ version: state.editingSnapshot.version }),
    }).then(function (item) {
      clearDraft(item.id);
      return loadItems().then(function () { loadEditorFromItem(item); });
    }).catch(function (err) {
      if (err.message !== "unauthenticated") window.alert(err.message || "Archivieren fehlgeschlagen.");
    });
  });

  // -- Anlegen (P5-U: Typ nach dem Anlegen nicht mehr änderbar) ------------------------------

  function openCreateDialog() {
    if (state.meta) {
      createTypeEl.textContent = "";
      Object.keys(state.meta.status_values).forEach(function (t) {
        var opt = document.createElement("option");
        opt.value = t;
        opt.textContent = t;
        createTypeEl.appendChild(opt);
      });
    }
    createTitleInputEl.value = "";
    createDialogEl.hidden = false;
    createTitleInputEl.focus();
  }

  function closeCreateDialog() {
    createDialogEl.hidden = true;
  }

  createButtonEl.addEventListener("click", openCreateDialog);
  newItemButtonEl.addEventListener("click", openCreateDialog);
  createCancelButtonEl.addEventListener("click", closeCreateDialog);

  createSubmitButtonEl.addEventListener("click", function () {
    var title = createTitleInputEl.value.trim();
    if (!title) { createTitleInputEl.focus(); return; }
    api("/items", {
      method: "POST", body: JSON.stringify({ type: createTypeEl.value, title: title, body: "" }),
    }).then(function (item) {
      closeCreateDialog();
      return loadItems().then(function () { loadEditorFromItem(item); });
    }).catch(function (err) {
      if (err.message !== "unauthenticated") window.alert(err.message || "Anlegen fehlgeschlagen.");
    });
  });

  // -- Formatierhilfen (P5-U: fügt Markdown-Syntax in die Textarea ein, kein `execCommand`,
  // kein WYSIWYG — die Idee einer Symbolleiste ist aus dem Notizheft-Beispiel geerntet, die
  // Umsetzung nicht: dort steuert die Leiste ein `contenteditable`-Feld) -----------------------

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

  [fieldTitleEl, fieldStatusEl, fieldDueEl, fieldTagsEl, fieldLinksEl, editorTextareaEl].forEach(
    function (input) {
      input.addEventListener("input", function () {
        updateVersionBand();
        saveDraft();
      });
    }
  );

  // -- Init ------------------------------------------------------------------------------

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
        return api("/meta");
      })
      .then(function (meta) {
        state.meta = meta;
        return loadItems();
      })
      .catch(reportUnexpectedError);
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

  document.addEventListener("keydown", function (event) {
    var tag = document.activeElement && document.activeElement.tagName;
    var inField = tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT";

    if ((event.metaKey || event.ctrlKey) && event.key === "s") {
      event.preventDefault();
      if (!detailEditorEl.hidden && state.editingSnapshot) saveItem();
      return;
    }
    if (event.key === "Escape") {
      if (!conflictDialogEl.hidden) hideConflictDialog();
      else if (!createDialogEl.hidden) closeCreateDialog();
      return;
    }
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
