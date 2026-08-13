"use strict";

import {
  state, setCreateControlsPresent, activeSpaceWritable, init as initState,
} from "./state.js";
import { init as initToasts } from "./toasts.js";
import { api, csrfToken, reportUnexpectedError } from "./api.js";
import { init as initTree } from "./tree.js";
import * as List from "./list.js";
import * as Editor from "./editor.js";
import { init as initDialogs, pendingConfirmCancel, hideConflictDialog, closeCreateDialog } from "./dialogs.js";
import { init as initUpdates } from "./updates.js";

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

// -- Passwort-Sichtbarkeit (Meldung des Nikingers) -------------------------------------------
// Läuft unbedingt, nicht erst im Shell-Zweig unten: `pages.py`s Login-/Einladungsseiten laden
// dieses Modul jetzt ebenfalls (siehe dortiger Docstring), tragen aber kein `#shell`. Reine
// Fortschreitung (progressive enhancement) — lädt das Modul aus irgendeinem Grund nicht, bleibt
// das Feld einfach maskiert, das native `<form>` funktioniert unverändert weiter.
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
  // Reihenfolge der Modul-Initialisierung ist absichtlich: `state.init()` zuerst (baut die
  // `detachable()`-Wrapper, die `list.js`/`tree.js` in ihrer eigenen `init()` schon lesen
  // könnten), danach die übrigen — untereinander hängt die Reihenfolge nicht von Bedeutung ab,
  // jedes Modul greift beim Aufruf seiner EXPORTIERTEN Funktionen (nicht beim eigenen `init()`)
  // auf andere Module zu, und die sind zu diesem Zeitpunkt alle schon vollständig ausgewertet
  // (ES-Modul-Ladereihenfolge, nicht Aufrufreihenfolge dieser Zeilen).
  initState();
  initToasts();
  initTree();
  List.init();
  initDialogs();
  Editor.init();

  // -- Übersicht / Logout / Zurück ---------------------------------------------------------

  var homeButtonEl = document.getElementById("home-button");
  // `closeEditor()` räumt bereits auf (inklusive Rückfrage bei ungespeicherten Änderungen) und
  // zeigt danach die Übersicht — hier ist nichts weiter zu tun.
  homeButtonEl.addEventListener("click", function () { Editor.closeEditor(); });

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
  var conflictDialogEl = document.getElementById("conflict-dialog");
  var createDialogEl = document.getElementById("create-dialog");
  var confirmDialogEl = document.getElementById("confirm-dialog");
  var accountDialogEl = document.getElementById("account-dialog");
  var detailEditorEl = document.getElementById("detail-editor");
  var searchInputEl = document.getElementById("search-input");

  function anyOverlayOpen() {
    return !conflictDialogEl.hidden || !createDialogEl.hidden
      || !confirmDialogEl.hidden || !accountDialogEl.hidden || !updateLogDialogEl.hidden;
  }

  document.addEventListener("keydown", function (event) {
    var tag = document.activeElement && document.activeElement.tagName;
    var inField = tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT";

    if ((event.metaKey || event.ctrlKey) && event.key === "s") {
      event.preventDefault();
      if (!detailEditorEl.hidden && state.editingSnapshot) Editor.saveItem();
      return;
    }
    if (event.key === "Escape") {
      if (!confirmDialogEl.hidden && pendingConfirmCancel) pendingConfirmCancel();
      else if (!conflictDialogEl.hidden) hideConflictDialog();
      else if (!createDialogEl.hidden) closeCreateDialog();
      else if (!updateLogDialogEl.hidden) updateLogDialogEl.hidden = true;
      else if (!accountDialogEl.hidden) accountDialogEl.hidden = true;
      else if (state.selectedId !== null) Editor.closeEditor();
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
      Editor.selectItem(ids[nextIndex]).catch(reportUnexpectedError);
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
        return List.loadOverview();
      })
      .then(function () {
        setCreateControlsPresent(activeSpaceWritable());
        List.renderCrumb();
        return List.loadItems();
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
    List.loadOverview().catch(reportUnexpectedError);
  }

  window.setInterval(pollCounters, COUNTER_POLL_MS);
  document.addEventListener("visibilitychange", function () {
    if (!document.hidden) pollCounters();
  });
  window.addEventListener("focus", pollCounters);

  // -- Update-Banner (P6 Step 3) -----------------------------------------------------------
  initUpdates();

  Editor.showOverviewPane();
  init();
}
