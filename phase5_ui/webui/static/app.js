"use strict";

// -- Bootstrap: Übernahme des CSRF-Tokens von der Login-Erfolgsseite (Plan-Abweichung 2,
// phase5_ui/CLAUDE.md Session-Block 2026-08-05) --------------------------------------------
// `routes_auth.py :: _login_post()` liefert den CSRF-Token nur EIN einziges Mal als Klartext
// (`ui_sessions` speichert nur den Hash) — als verstecktes Feld auf genau dieser Seite. Diese
// Datei läuft dort UND auf der echten Shell (`/ui/`); auf der Erfolgsseite existiert kein
// `#shell`, das unterscheidet die beiden Fälle ohne zusätzliches Signal.
//
// **[2026-08-06, Advisor-Fund vor dem Commit]:** seit `pages.py`s `_PAGE` auf JEDER Seite
// `app.js` lädt (Passwort-Sichtbarkeit), tragen `render_enrollment_page()` (TOTP-Seed/QR) und
// `render_recovery_codes_page()` (zehn Recovery-Codes) IHRERSEITS ein `<input name="csrf">` —
// beide zeigen ein Geheimnis, das nur EIN einziges Mal sichtbar ist. Ein Selektor auf
// `input[name="csrf"]` hätte auf beiden Seiten sofort nach `/ui/` weitergeleitet, bevor der
// Mensch den QR-Code fotografieren bzw. die Codes abschreiben konnte. Das Feld trägt deshalb
// jetzt zusätzlich `id="bootstrap-csrf"` — NUR auf der echten Bootstrap-Seite
// (`render_logged_in_page()`) — und dieser Selektor prüft explizit danach, nicht mehr nach
// jedem `name="csrf"`.
(function bootstrapCsrf() {
  var csrfField = document.getElementById("bootstrap-csrf");
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

// -- Passwort-Sichtbarkeit (Meldung des Nikingers) -------------------------------------------
// Läuft unbedingt, nicht erst in initShell(): `pages.py`s Login-/Einladungsseiten laden app.js
// jetzt ebenfalls (siehe dortiger Docstring), tragen aber kein `#shell`. Reine Fortschreitung
// (progressive enhancement) — lädt app.js aus irgendeinem Grund nicht, bleibt das Feld einfach
// maskiert, das native `<form>` funktioniert unverändert weiter.
(function initPasswordToggles() {
  Array.prototype.forEach.call(document.querySelectorAll(".pw-toggle"), function (button) {
    var target = document.getElementById(button.dataset.target);
    if (!target) return;
    button.addEventListener("click", function () {
      var reveal = target.type === "password";
      target.type = reveal ? "text" : "password";
      button.textContent = reveal ? "Verbergen" : "Anzeigen";
      button.setAttribute("aria-pressed", reveal ? "true" : "false");
    });
  });
})();

var shellEl = document.getElementById("shell");
if (shellEl) {
  initShell();
}

function initShell() {
  var API_BASE = "/api/v1";

  // Beschriftung der Ordner. Die Ordner SELBST (und ihre Filterkombinationen) kommen aus
  // `GET /api/v1/meta`, nicht von hier — sonst gäbe es zwei Definitionen desselben Vokabulars
  // (siehe `api.py :: _BUCKETS`). Diese Tabelle liefert nur die deutschen Namen.
  var BUCKET_LABELS = {
    open: "Offen",
    done: "Erledigt",
    note: "Notizen",
    archived: "Archiv",
  };

  // Deutsche Beschriftung für `storage.models`s Typ-Vokabular ("task"/"note") — dieselbe
  // Übersetzungstabelle wie BUCKET_LABELS, nur für den Anlegen-Dialog. `state.meta.status_values`
  // bleibt die Quelle der WERTE (P5-U), diese Tabelle liefert nur die Anzeige.
  var TYPE_LABELS = {
    task: "Aufgabe",
    note: "Notiz",
  };

  var state = {
    spaces: [],          // aus /overview: {name, own, item_count, counts, recent}
    ownSpace: null,
    activeSpace: null,
    expanded: {},        // fremder Space-Name -> aufgeklappt?
    filter: "open",
    query: "",
    items: [],
    selectedId: null,
    selectedReadonly: false,
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
  // aus einer Nutzeraktion mit eigener Fehlerbehandlung: ohne dieses Netz bliebe die von `api()`s
  // 401-Zweig zurückgegebene Promise unbehandelt — die "Sitzung abgelaufen"-Karte erscheint zwar
  // trotzdem (das passiert synchron in `api()`, bevor verworfen wird), aber eine unbehandelte
  // Ablehnung ist unnötiger Lärm in der Konsole und in strengeren Laufzeiten (Fund aus Step 7:
  // Node bricht bei einer unbehandelten Promise-Ablehnung den Prozess ab, ein Browser gibt nur
  // eine Konsolenwarnung — trotzdem sauber behandeln).
  function reportUnexpectedError(err) {
    if (err && err.message === "unauthenticated") return;
    console.error(err);
    toast(err && err.message ? err.message : "Unerwarteter Fehler.", "error");
  }

  // -- DOM-Referenzen -----------------------------------------------------------------------

  var railTreeEl = document.getElementById("rail-tree");
  var homeButtonEl = document.getElementById("home-button");
  var accountButtonEl = document.getElementById("account-button");

  var listCrumbEl = document.getElementById("list-crumb");
  var listReadonlyEl = document.getElementById("list-readonly");
  var listRowsEl = document.getElementById("list-rows");
  var listEmptyEl = document.getElementById("list-empty");
  var listEmptyTextEl = document.getElementById("list-empty-text");
  var listChipsEl = document.getElementById("list-chips");
  var searchInputEl = document.getElementById("search-input");
  var createButtonEl = document.getElementById("create-button");
  var newItemButtonEl = document.getElementById("new-item-button");

  var detailEl = document.getElementById("detail");
  var overviewEl = document.getElementById("detail-overview");
  var overviewTitleEl = document.getElementById("overview-title");
  var overviewTilesEl = document.getElementById("overview-tiles");
  var overviewRecentEl = document.getElementById("overview-recent");
  var overviewForeignEl = document.getElementById("overview-foreign");

  var detailReadonlyEl = document.getElementById("detail-readonly");
  var roTitleEl = document.getElementById("ro-title");
  var roMetaEl = document.getElementById("ro-meta");
  var roPreviewEl = document.getElementById("ro-preview");
  var roCloseButtonEl = document.getElementById("ro-close-button");

  var detailEditorEl = document.getElementById("detail-editor");
  var editorVersionEl = document.getElementById("editor-version");
  var versionBandEl = document.getElementById("version-band");
  var versionBandNumberEl = document.getElementById("version-band-number");
  var metaPanelEl = document.getElementById("meta-panel");
  var metaDigestEl = document.getElementById("meta-digest");
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
  var closeButtonEl = document.getElementById("close-button");
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

  var confirmDialogEl = document.getElementById("confirm-dialog");
  var confirmTitleEl = document.getElementById("confirm-title");
  var confirmMessageEl = document.getElementById("confirm-message");
  var confirmOkEl = document.getElementById("confirm-ok");
  var confirmCancelEl = document.getElementById("confirm-cancel");

  var accountDialogEl = document.getElementById("account-dialog");
  var accountErrorEl = document.getElementById("account-error");
  var accountCurrentEl = document.getElementById("account-current");
  var accountTotpEl = document.getElementById("account-totp");
  var accountNewEl = document.getElementById("account-new");
  var accountRepeatEl = document.getElementById("account-repeat");
  var accountSubmitEl = document.getElementById("account-submit");
  var accountCancelEl = document.getElementById("account-cancel");

  var sessionExpiredCardEl = document.getElementById("session-expired-card");
  var toastEl = document.getElementById("toast");

  function el(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function showSessionExpiredCard() {
    sessionExpiredCardEl.hidden = false;
  }

  // -- Statuszeile (§4.5) --------------------------------------------------------------------
  // Bis Step 7b gab es für einen gelungenen Schreibvorgang gar keine Rückmeldung — der Nikinger
  // klickte deshalb mehrfach auf "Speichern", jeder Klick zählte die Version hoch (Fund V10).
  // Die zweite Hälfte dieses Fundes steckt in `updateVersionBand()`: "Speichern" ist ohne
  // tatsächliche Änderung deaktiviert.

  var toastTimer = null;

  function toast(message, kind) {
    toastEl.textContent = message;
    toastEl.className = "toast" + (kind ? " toast--" + kind : "");
    toastEl.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toastEl.hidden = true; }, kind === "error" ? 6000 : 2800);
  }

  // -- Bedienelemente aus dem DOM lösen (Akzeptanzkriterium 12) -------------------------------
  // "Fremder Space: sichtbar, lesbar, OHNE Schreib-Bedienelemente im DOM" heißt wörtlich: nicht
  // `hidden`, sondern nicht vorhanden. Bis Step 7b standen Editor, "+"-Knopf und Anlegen-Dialog
  // permanent im Dokument und waren nur ausgeblendet — mit DevTools also auffindbar. Diese
  // Hilfsfunktion hängt den ganzen Teilbaum aus und später an derselben Elternstelle wieder ein;
  // Kindreferenzen und Event-Listener überleben das unverändert.

  function detachable(node) {
    var parent = node.parentNode;
    return {
      attach: function () { if (!node.parentNode) parent.appendChild(node); },
      detach: function () { if (node.parentNode) node.parentNode.removeChild(node); },
    };
  }

  var editorPart = detachable(detailEditorEl);
  var createTriggers = [detachable(newItemButtonEl), detachable(createButtonEl)];
  var createDialogPart = detachable(createDialogEl);

  function setCreateControlsPresent(present) {
    createTriggers.forEach(function (part) { present ? part.attach() : part.detach(); });
    // Der Dialog hängt NUR am Space, nicht an der Trefferlage — sonst könnte ein Listen-Neuladen
    // einen gerade geöffneten Anlegen-Dialog aus dem Dokument reißen.
    activeSpaceWritable() ? createDialogPart.attach() : createDialogPart.detach();
  }

  // Live-Fund 2026-08-13, zweiter Teil desselben Bugs: der Sidebar-/Übersicht-Fix (writable
  // statt own aus /api/v1/spaces) betraf nur das Badge dort -- jede Stelle, die tatsächlich
  // Schreib-Bedienelemente ein-/ausblendet, fragte weiterhin nur nach dem eigenen Home-Space
  // statt tatsächlichem Schreibrecht. Ein geteilter, fremder-aber-schreibbarer Space (z.B.
  // IT-Sekus-Projekt) verlor damit trotz behobenem Badge weiterhin den Anlegen-Knopf.
  function activeSpaceWritable() {
    if (state.activeSpace === null) return false;
    var space = spaceByName(state.activeSpace);
    return !!(space && space.writable);
  }

  // -- Rückfragedialog (ersetzt window.confirm) ----------------------------------------------

  var pendingConfirmCancel = null;

  function confirmDialog(options) {
    return new Promise(function (resolve) {
      confirmTitleEl.textContent = options.title;
      confirmMessageEl.textContent = options.message;
      confirmOkEl.textContent = options.ok || "OK";
      confirmDialogEl.hidden = false;
      confirmOkEl.focus();

      function finish(value) {
        confirmDialogEl.hidden = true;
        confirmOkEl.removeEventListener("click", onOk);
        confirmCancelEl.removeEventListener("click", onCancel);
        pendingConfirmCancel = null;
        resolve(value);
      }
      function onOk() { finish(true); }
      function onCancel() { finish(false); }

      confirmOkEl.addEventListener("click", onOk);
      confirmCancelEl.addEventListener("click", onCancel);
      pendingConfirmCancel = onCancel;
    });
  }

  // -- Navigationsbaum (Step 7b) --------------------------------------------------------------

  function bucketNames() {
    return state.meta ? Object.keys(state.meta.buckets) : [];
  }

  function navigate(spaceName, bucket) {
    state.activeSpace = spaceName;
    state.filter = bucket;
    setCreateControlsPresent(activeSpaceWritable());
    renderRail();
    renderCrumb();
    return loadItems();
  }

  function renderFolders(space) {
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

  function renderSpaceNode(space) {
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

  function renderRail() {
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

  // -- Übersichtsseite ------------------------------------------------------------------------

  function spaceByName(name) {
    for (var i = 0; i < state.spaces.length; i++) {
      if (state.spaces[i].name === name) return state.spaces[i];
    }
    return null;
  }

  function renderOverview() {
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

  function openFromOverview(spaceName, item) {
    // Ein Klick in "Zuletzt benutzt" darf nicht in einem Ordner landen, der das Item gar nicht
    // enthält — sonst ist die Liste daneben leer, während rechts das Item steht.
    var bucket = bucketFor(item) || state.filter;
    navigate(spaceName, bucket)
      .then(function () { return selectItem(item.id); })
      .catch(reportUnexpectedError);
  }

  function loadOverview() {
    return api("/overview").then(function (spaces) {
      state.spaces = spaces;
      renderRail();
      renderOverview();
    });
  }

  // -- Liste ----------------------------------------------------------------------------------

  function itemMetaLine(item) {
    var parts = [item.type, item.status];
    if (item.due) parts.push(item.due);
    if (item.tags && item.tags.length) parts.push(item.tags.join(", "));
    return parts.join(" · ");
  }

  function renderCrumb() {
    listCrumbEl.textContent = "";
    var strong = el("strong", null, state.activeSpace || "");
    listCrumbEl.appendChild(strong);
    listCrumbEl.appendChild(document.createTextNode(" › " + (BUCKET_LABELS[state.filter] || state.filter)));
    listReadonlyEl.hidden = activeSpaceWritable();
  }

  function renderChips() {
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

  function renderList() {
    listRowsEl.textContent = "";
    renderChips();

    if (state.items.length === 0) {
      listEmptyEl.hidden = false;
      if (state.query) {
        listEmptyTextEl.textContent = "Keine Treffer für „" + state.query + "“.";
      } else if (!activeSpaceWritable()) {
        listEmptyTextEl.textContent = "In diesem Ordner liegt nichts.";
      } else {
        listEmptyTextEl.textContent =
          "Noch nichts unter „" + (BUCKET_LABELS[state.filter] || state.filter) + "“.";
      }
      // Meldung des Nikingers, gleicher Fund wie der Anlegen-Dialog: der Knopf sagte immer
      // "Notiz", auch im "Offen"/"Erledigt"-Ordner (Typ "task"). Folgt jetzt demselben Typ, den
      // ein Klick tatsächlich anlegen würde (siehe openCreateDialog()).
      var emptyBucket = state.meta && state.meta.buckets[state.filter];
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

  function filterParams() {
    // Die drei/vier Ordner kommen serverseitig aus `api.py :: _BUCKETS` und werden über
    // `GET /api/v1/meta` geliefert — hier steht bewusst keine zweite Definition mehr.
    var bucket = state.meta && state.meta.buckets[state.filter];
    return Object.assign({}, bucket || {});
  }

  function bucketFor(item) {
    var names = bucketNames();
    for (var i = 0; i < names.length; i++) {
      var f = state.meta.buckets[names[i]];
      var typeOk = !f.type || f.type === item.type;
      var statusOk = !f.status || f.status === item.status;
      if (typeOk && statusOk) return names[i];
    }
    return null;
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

  // -- Detail: Nur-lesen (fremdes Item) vs. Editor (eigenes Item) -----------------------------

  function showOverviewPane() {
    overviewEl.hidden = false;
    detailReadonlyEl.hidden = true;
    detailEditorEl.hidden = true;
    editorPart.detach();
    shellEl.dataset.view = "list";
  }

  function clearDetail() {
    state.selectedId = null;
    state.selectedReadonly = false;
    state.editingSnapshot = null;
    state.conflictCurrent = null;
    showOverviewPane();
    renderRail();
    renderList();
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

  function renderMetaDigest() {
    var v = currentFormValues();
    var parts = [v.status];
    if (v.due) parts.push("fällig " + v.due);
    if (v.tags.length) parts.push(v.tags.join(", "));
    metaDigestEl.textContent = parts.join(" · ");
  }

  function updateVersionBand() {
    versionBandEl.classList.remove("is-dirty", "is-conflict");
    if (!state.editingSnapshot) {
      versionBandNumberEl.textContent = "";
      editorVersionEl.textContent = "";
      saveButtonEl.disabled = true;
      return;
    }
    var dirty = isDirty();
    // Der Kern des V10-Fundes: ohne echte Änderung gibt es nichts zu speichern, und ein Klick
    // darf die Version nicht hochzählen.
    saveButtonEl.disabled = !dirty;
    if (state.conflictCurrent) {
      versionBandEl.classList.add("is-conflict");
      versionBandNumberEl.textContent = "v" + state.editingSnapshot.version + " → v" + state.conflictCurrent.version;
      editorVersionEl.textContent = "Konflikt";
    } else if (dirty) {
      versionBandEl.classList.add("is-dirty");
      versionBandNumberEl.textContent = "v" + state.editingSnapshot.version + "+";
      editorVersionEl.textContent = "ungespeichert";
    } else {
      versionBandNumberEl.textContent = "v" + state.editingSnapshot.version;
      editorVersionEl.textContent = "v" + state.editingSnapshot.version + " gespeichert";
    }
    renderMetaDigest();
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
    editorPreviewEl.hidden = mode !== "preview";
    togglePreviewButtonEl.textContent = mode === "edit" ? "Vorschau" : "Bearbeiten";
    // Die Formatierhilfen bleiben sichtbar (sie sitzen in derselben Leiste wie der
    // Vorschau-Umschalter), sind in der Vorschau aber deaktiviert — sonst würden sie unsichtbar
    // in die Textarea schreiben.
    Array.prototype.forEach.call(editorToolbarEl.querySelectorAll("[data-md]"), function (b) {
      b.disabled = mode !== "edit";
    });
    if (mode === "preview") {
      editorPreviewEl.innerHTML = markdownToHtml(editorTextareaEl.value);
    }
  }

  function showReadonlyItem(item) {
    editorPart.detach();          // Akzeptanzkriterium 12
    // Beides zwingend, nicht kosmetisch (Advisor-Fund, siehe F7 im Session-Block): `hidden`
    // überlebt das Aushängen des Knotens, und der `Ctrl+S`-Wächter prüft genau dieses Flag
    // zusammen mit `editingSnapshot`. Ohne diese zwei Zeilen bliebe der Editor-Zustand des
    // ZULETZT geöffneten eigenen Items scharf, während rechts ein fremdes Item steht.
    detailEditorEl.hidden = true;
    state.editingSnapshot = null;
    overviewEl.hidden = true;
    detailReadonlyEl.hidden = false;
    roTitleEl.textContent = item.title;
    roMetaEl.textContent = "";
    roMetaEl.appendChild(el("span", "detail__badge-readonly", "Nur lesen — fremder Space (" + item.space + ")"));
    roMetaEl.appendChild(el("span", "tnum version-num", "v" + item.version));
    roMetaEl.appendChild(el("span", null, item.type + " · " + item.status));
    if (item.due) roMetaEl.appendChild(el("span", "tnum", "fällig " + item.due));
    roPreviewEl.innerHTML = markdownToHtml(item.body);
  }

  function showEditableItem(item, opts) {
    opts = opts || {};
    editorPart.attach();
    overviewEl.hidden = true;
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
    // Meldung des Nikingers: der Editor öffnete immer in der Bearbeiten-Ansicht, auch beim
    // bloßen Betrachten. Vorgabe jetzt "Vorschau" — außer `opts.mode` sagt etwas anderes:
    // ein frisch angelegtes Item (createSubmitButtonEl) will sofort tippen können ("edit"),
    // und ein Neuladen NACH einem Schreibvorgang (afterWrite/Konflikt) behält den Modus bei,
    // den man gerade benutzt hat, statt mitten im Tippen in die Vorschau zu springen.
    setEditorMode(opts.mode || "preview");

    var draft = loadDraftIfAny(item.id);
    if (draft && (draft.title !== item.title || draft.body !== item.body)) {
      confirmDialog({
        title: "Ungespeicherter Entwurf",
        message: "Für dieses Item liegt ein ungespeicherter Entwurf in diesem Tab. Wiederherstellen?",
        ok: "Wiederherstellen",
      }).then(function (restore) {
        if (!restore) {
          clearDraft(item.id);
          return;
        }
        fieldTitleEl.value = draft.title;
        editorTextareaEl.value = draft.body;
        fieldStatusEl.value = draft.status;
        fieldDueEl.value = draft.due || "";
        fieldTagsEl.value = draft.tags.join(", ");
        fieldLinksEl.value = draft.links.join(", ");
        updateVersionBand();
        // Advisor-Fund: `setEditorMode()` rendert die Vorschau nur BEIM WECHSEL nach "preview" —
        // stehen wir (Vorgabe seit diesem Fund) schon dort, während der Entwurf asynchron
        // ankommt, zeigte die Vorschau bis hierhin weiter den ALTEN, gespeicherten Text.
        if (state.mode === "preview") {
          editorPreviewEl.innerHTML = markdownToHtml(editorTextareaEl.value);
        }
      });
    }
    updateVersionBand();
  }

  function loadEditorFromItem(item, opts) {
    state.selectedId = item.id;
    state.selectedReadonly = !!item.readonly;
    state.conflictCurrent = null;
    conflictDialogEl.hidden = true;

    if (item.readonly) showReadonlyItem(item);
    else showEditableItem(item, opts);

    shellEl.dataset.view = "detail";
    renderRail();
    renderList();
  }

  function selectItem(id) {
    state.selectedId = id;
    renderList();
    return api("/items/" + encodeURIComponent(id)).then(function (item) {
      return loadEditorFromItem(item);
    });
  }

  // -- Editor schließen (Meldung des Nikingers: der Editor blieb "immer" offen) ----------------

  function closeEditor() {
    if (!isDirty()) {
      clearDetail();
      return Promise.resolve(true);
    }
    return confirmDialog({
      title: "Ungespeicherte Änderungen",
      message: "Der Editor enthält Änderungen, die noch nicht gespeichert sind. Verwerfen?",
      ok: "Verwerfen",
    }).then(function (discard) {
      if (!discard) return false;
      clearDraft(state.selectedId);
      clearDetail();
      return true;
    });
  }

  closeButtonEl.addEventListener("click", function () { closeEditor(); });

  // Nur-lesen-Ansicht (fremdes Item): kein `editingSnapshot`, also nichts Ungespeichertes —
  // schließt ohne Rückfrage, anders als `closeEditor()`.
  roCloseButtonEl.addEventListener("click", function () { clearDetail(); });

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

  // Nach jedem Schreibvorgang: Liste neu laden (Reihenfolge/Zugehörigkeit kann sich geändert
  // haben) UND die Zähler im Baum, sonst zeigt die Navigation Zahlen von vorhin.
  function afterWrite(item, message) {
    clearDraft(item.id);
    // Modus VOR dem Neuladen einfangen: showEditableItem()s Vorgabe ist seit dem
    // Vorschau-Default "preview", ein Schreibvorgang mitten im Tippen soll aber nicht aus dem
    // Editor reißen — wer gerade bearbeitet, bleibt beim Bearbeiten.
    var mode = state.mode;
    return loadItems()
      .then(loadOverview)
      .then(function () {
        loadEditorFromItem(item, { mode: mode });
        toast(message);
      });
  }

  function handleWriteError(err, fallback) {
    if (err.code === "conflict" && err.detail && err.detail.current) {
      showConflictDialog(err.detail.current);
      return;
    }
    if (err.message === "unauthenticated") return;
    toast(err.message || fallback, "error");
  }

  // Jeder Schreibvorgang adressiert das Item über `state.editingSnapshot.id`, NIE über
  // `state.selectedId` (Advisor-Fund, F7 im Session-Block): `selectItem()` setzt `selectedId`
  // sofort, `editingSnapshot` erst wenn die Antwort da ist. Zwischen beidem liegt ein Fenster, in
  // dem `selectedId` schon auf Item B zeigt, während Version und Formularwerte noch zu Item A
  // gehören — ein `Ctrl+S` in diesem Moment schriebe A's Inhalt unter B's Kennung, und wenn beide
  // Versionen zufällig gleich sind, ohne Konflikt. Das ist genau der stille Überschreiber, den
  // Hard Rule 3 verbietet, nur eben clientseitig herbeigeführt. Über den Schnappschuss adressiert
  // stammen Kennung und Version beweisbar aus demselben Lesevorgang.
  function saveItem() {
    if (!state.editingSnapshot || !isDirty()) return Promise.resolve();
    var payload = Object.assign(
      { version: state.editingSnapshot.version, format: "markdown" }, currentFormValues()
    );
    return api("/items/" + encodeURIComponent(state.editingSnapshot.id), {
      method: "PATCH", body: JSON.stringify(payload),
    }).then(function (item) {
      return afterWrite(item, "Gespeichert · v" + item.version);
    }).catch(function (err) {
      handleWriteError(err, "Speichern fehlgeschlagen.");
    });
  }

  saveButtonEl.addEventListener("click", function () { saveItem(); });

  conflictLoadCurrentButtonEl.addEventListener("click", function () {
    var current = state.conflictCurrent;
    var mode = state.mode;   // wer gerade bearbeitet hat, bleibt beim Bearbeiten (siehe afterWrite())
    clearDraft(current.id);
    hideConflictDialog();
    loadEditorFromItem(current, { mode: mode });
    toast("Aktuelle Fassung geladen · v" + current.version, "warn");
  });

  conflictSaveAsNewButtonEl.addEventListener("click", function () {
    var values = currentFormValues();
    var payload = Object.assign({ type: state.editingSnapshot.type, format: "markdown" }, values);
    var previousId = state.editingSnapshot.id;   // siehe F7-Kommentar über `saveItem()`
    hideConflictDialog();
    api("/items", { method: "POST", body: JSON.stringify(payload) }).then(function (item) {
      clearDraft(previousId);
      return afterWrite(item, "Als neues Item angelegt · " + item.title);
    }).catch(function (err) {
      handleWriteError(err, "Anlegen fehlgeschlagen.");
    });
  });

  conflictCancelButtonEl.addEventListener("click", hideConflictDialog);

  // -- Anhängen (eigener Pfad, nicht über PATCH) ----------------------------------------------

  appendButtonEl.addEventListener("click", function () {
    var text = appendInputEl.value.trim();
    if (!text || !state.editingSnapshot) return;
    api("/items/" + encodeURIComponent(state.editingSnapshot.id) + "/append", {
      method: "POST", body: JSON.stringify({ version: state.editingSnapshot.version, text: text }),
    }).then(function (item) {
      appendInputEl.value = "";
      return afterWrite(item, "Angehängt · v" + item.version);
    }).catch(function (err) {
      handleWriteError(err, "Anhängen fehlgeschlagen.");
    });
  });

  // -- Archivieren -----------------------------------------------------------------------------

  archiveButtonEl.addEventListener("click", function () {
    if (!state.editingSnapshot) return;
    confirmDialog({
      title: "Archivieren",
      message: "Das Item wandert ins Archiv. Gelöscht wird nichts — du findest es unter „Archiv“ wieder.",
      ok: "Archivieren",
    }).then(function (ok) {
      if (!ok) return;
      return api("/items/" + encodeURIComponent(state.editingSnapshot.id) + "/archive", {
        method: "POST", body: JSON.stringify({ version: state.editingSnapshot.version }),
      }).then(function (item) {
        // Nach dem Archivieren blieb das Item bis Step 7b im Editor stehen, obwohl es aus der
        // Liste verschwunden war — der Editor zeigte etwas, das daneben nicht mehr existierte.
        clearDraft(item.id);
        state.editingSnapshot = null;
        return loadItems().then(loadOverview).then(function () {
          clearDetail();
          toast("Archiviert · " + item.title);
        });
      }).catch(function (err) {
        handleWriteError(err, "Archivieren fehlgeschlagen.");
      });
    });
  });

  // -- Anlegen (P5-U: Typ nach dem Anlegen nicht mehr änderbar) ------------------------------

  function openCreateDialog() {
    if (!activeSpaceWritable()) return;   // sollte nicht erreichbar sein, der Knopf ist dann ausgehängt
    if (state.meta) {
      createTypeEl.textContent = "";
      Object.keys(state.meta.status_values).forEach(function (t) {
        var opt = document.createElement("option");
        opt.value = t;
        opt.textContent = TYPE_LABELS[t] || t;
        createTypeEl.appendChild(opt);
      });
      // Meldung des Nikingers: "wenn man einen Task machen will, steht auch Notiz" — der
      // Dropdown behielt seinen Vorgabewert (das erste `<option>`, immer "note") unabhängig
      // vom gerade offenen Ordner. Der aktive Ordner nennt seinen Typ selbst
      // (`_BUCKETS`/`api.py`), "archived" nicht (typunabhängig) — dort bleibt die Vorgabe.
      var bucket = state.meta.buckets[state.filter];
      if (bucket && bucket.type) createTypeEl.value = bucket.type;
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
      // Meldung des Nikingers: eine angelegte Notiz "landete in Notizen", war im gerade
      // sichtbaren Ordner also nicht zu sehen. Der aktive Ordner springt jetzt dorthin mit, wo
      // das neue Item tatsächlich liegt.
      state.query = "";
      searchInputEl.value = "";
      return navigate(state.ownSpace, bucketFor(item) || state.filter)
        .then(loadOverview)
        .then(function () {
          // Trap beim Vorschau-Default (Advisor-Fund): ein frisch angelegtes Item hat einen
          // leeren Body — in "preview" öffnend stünde man vor einer leeren Vorschau statt der
          // Textarea, in die man eigentlich sofort tippen will.
          loadEditorFromItem(item, { mode: "edit" });
          toast("Angelegt · " + item.title);
          fieldTitleEl.focus();
        });
    }).catch(function (err) {
      handleWriteError(err, "Anlegen fehlgeschlagen.");
    });
  });

  // -- Konto: Passwort ändern (Block-A-Abnahmezeilen 5/6) --------------------------------------

  function openAccountDialog() {
    accountErrorEl.hidden = true;
    accountCurrentEl.value = "";
    accountTotpEl.value = "";
    accountNewEl.value = "";
    accountRepeatEl.value = "";
    accountDialogEl.hidden = false;
    accountCurrentEl.focus();
  }

  function accountError(message) {
    accountErrorEl.textContent = message;
    accountErrorEl.hidden = false;
  }

  accountButtonEl.addEventListener("click", openAccountDialog);
  accountCancelEl.addEventListener("click", function () { accountDialogEl.hidden = true; });

  accountSubmitEl.addEventListener("click", function () {
    if (accountNewEl.value !== accountRepeatEl.value) {
      accountError("Die beiden neuen Passwörter stimmen nicht überein.");
      return;
    }
    accountErrorEl.hidden = true;
    accountSubmitEl.disabled = true;
    fetch("/api/v1/account/password", {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-CSRF-Token": csrfToken() || "" },
      body: JSON.stringify({
        password: accountCurrentEl.value,
        totp: accountTotpEl.value,
        new_password: accountNewEl.value,
      }),
    }).then(function (response) {
      return response.json().catch(function () { return null; }).then(function (body) {
        accountSubmitEl.disabled = false;
        if (!response.ok) {
          var reasons = body && body.detail && body.detail.reasons;
          accountError(
            (body && body.message ? body.message : "Passwortwechsel fehlgeschlagen.")
            + (reasons && reasons.length ? " (" + reasons.join("; ") + ")" : "")
          );
          return;
        }
        // P5-E/P5-Q: der Wechsel rotiert die Sitzung. Der neue CSRF-Token kommt genau EINMAL in
        // dieser Antwort — ohne diese Zeile schlüge jede folgende Schreibanfrage mit
        // `403 csrf_failed` fehl.
        if (body && body.csrf_token) sessionStorage.setItem("sfx:csrf", body.csrf_token);
        accountDialogEl.hidden = true;
        toast("Passwort geändert. Connectoren müssen neu autorisiert werden.", "warn");
      });
    }).catch(function () {
      accountSubmitEl.disabled = false;
      accountError("Der Dienst ist gerade nicht erreichbar.");
    });
  });

  // -- Formatierhilfen (P5-U: fügt Markdown-Syntax in die Textarea ein, kein `execCommand`,
  // kein WYSIWYG) -----------------------------------------------------------------------------

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
      // `<select>`/`<input type=date>` feuern in manchen Browsern nur `change`, nicht `input`.
      input.addEventListener("change", function () {
        updateVersionBand();
        saveDraft();
      });
    }
  );

  metaPanelEl.addEventListener("toggle", renderMetaDigest);

  // -- Suche (200ms Debounce) -----------------------------------------------------------

  var searchTimer = null;
  searchInputEl.addEventListener("input", function () {
    state.query = searchInputEl.value;
    clearTimeout(searchTimer);
    searchTimer = setTimeout(function () { loadItems().catch(reportUnexpectedError); }, 200);
  });

  // -- Übersicht / Logout / Zurück ---------------------------------------------------------

  // `closeEditor()` räumt bereits auf (inklusive Rückfrage bei ungespeicherten Änderungen) und
  // zeigt danach die Übersicht — hier ist nichts weiter zu tun.
  homeButtonEl.addEventListener("click", function () { closeEditor(); });

  document.getElementById("logout-button").addEventListener("click", function () {
    fetch("/ui/logout", { method: "POST", headers: { "X-CSRF-Token": csrfToken() || "" } }).then(
      function () { location.replace("/ui/login"); }
    );
  });

  document.getElementById("back-button").addEventListener("click", function () {
    shellEl.dataset.view = "list";
  });

  // -- Tastatur (§4.6) ----------------------------------------------------------------------

  var updateLogDialogEl = document.getElementById("update-log-dialog");

  function anyOverlayOpen() {
    return !conflictDialogEl.hidden || !createDialogEl.hidden
      || !confirmDialogEl.hidden || !accountDialogEl.hidden || !updateLogDialogEl.hidden;
  }

  document.addEventListener("keydown", function (event) {
    var tag = document.activeElement && document.activeElement.tagName;
    var inField = tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT";

    if ((event.metaKey || event.ctrlKey) && event.key === "s") {
      event.preventDefault();
      if (!detailEditorEl.hidden && state.editingSnapshot) saveItem();
      return;
    }
    if (event.key === "Escape") {
      if (!confirmDialogEl.hidden && pendingConfirmCancel) pendingConfirmCancel();
      else if (!conflictDialogEl.hidden) hideConflictDialog();
      else if (!createDialogEl.hidden) closeCreateDialog();
      else if (!updateLogDialogEl.hidden) updateLogDialogEl.hidden = true;
      else if (!accountDialogEl.hidden) accountDialogEl.hidden = true;
      else if (state.selectedId !== null) closeEditor();
      return;
    }
    if (event.key === "/" && !inField) {
      event.preventDefault();
      searchInputEl.focus();
      return;
    }
    if ((event.key === "ArrowDown" || event.key === "ArrowUp") && !inField && !anyOverlayOpen()) {
      event.preventDefault();
      var ids = state.items.map(function (item) { return item.id; });
      if (ids.length === 0) return;
      var currentIndex = ids.indexOf(state.selectedId);
      var step = event.key === "ArrowDown" ? 1 : -1;
      var nextIndex = currentIndex === -1 ? 0 : Math.min(ids.length - 1, Math.max(0, currentIndex + step));
      selectItem(ids[nextIndex]).catch(reportUnexpectedError);
    }
  });

  // -- Init ------------------------------------------------------------------------------

  function init() {
    return api("/me")
      .then(function (me) {
        state.ownSpace = me.space;
        state.activeSpace = me.space;
        return api("/meta");
      })
      .then(function (meta) {
        state.meta = meta;
        var names = Object.keys(meta.buckets);
        if (names.indexOf(state.filter) === -1) state.filter = names[0];
        return loadOverview();
      })
      .then(function () {
        setCreateControlsPresent(activeSpaceWritable());
        renderCrumb();
        return loadItems();
      })
      .catch(reportUnexpectedError);
  }

  // -- Zähler-Synchronisation (Meldung des Nikingers: „wenn eine neue Notiz dazu kommt, geht der
  // Counter nicht hoch") -----------------------------------------------------------------------
  // Reines Polling auf der bereits vorhandenen REST-API — P5 schließt Realtime/WebSocket aus
  // (Plan §0.5), nicht ein periodisches Nachfragen einer bestehenden Route. `loadOverview()`
  // fasst ausschließlich Baum-Zähler und die (ohnehin nur ohne offenes Item sichtbare)
  // Übersichtsseite an, nie den Editor — sicher neben einer laufenden Bearbeitung. 20s statt der
  // vorgeschlagenen 5s: jeder Aufruf kostet einen `search()` je Bucket UND sichtbarem Space
  // (`api.py :: _overview()`), 5s wäre für einen Zwei-Personen-Server unnötig oft. Pausiert,
  // solange der Tab nicht sichtbar ist, holt dafür sofort bei Rückkehr/Fokus nach.
  var COUNTER_POLL_MS = 20000;

  function pollCounters() {
    if (document.hidden) return;
    loadOverview().catch(reportUnexpectedError);
  }

  window.setInterval(pollCounters, COUNTER_POLL_MS);
  document.addEventListener("visibilitychange", function () {
    if (!document.hidden) pollCounters();
  });
  window.addEventListener("focus", pollCounters);

  // -- Update-Banner (P6 Step 3) -----------------------------------------------------------
  // `updates.js` muss VOR dieser Datei geladen sein (siehe dortiger Docstring), sonst existiert
  // `window.SharefyxUpdates` an dieser Stelle noch nicht.
  if (window.SharefyxUpdates) window.SharefyxUpdates.init({ api: api, toast: toast });

  showOverviewPane();
  init();
}
