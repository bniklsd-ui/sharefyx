"use strict";

import {
  state, setCreateControlsPresent, activeSpaceWritable, init as initState,
} from "./state.js";
import { init as initToasts } from "./toasts.js";
import { api, csrfToken, reportUnexpectedError } from "./api.js";
import { init as initTree } from "./tree.js";
import * as List from "./list.js";
import * as Editor from "./editor.js";
import {
  init as initDialogs, pendingConfirmCancel, hideConflictDialog, closeCreateDialog,
  closeNewFolderDialog, closeMoveDialog, closeShareDialog, closeLinkPicker,
  closeTrashDialog,
} from "./dialogs.js";
import { init as initUpdates } from "./updates.js";
import { init as initSpaces, closeRemoveSpaceDialog } from "./spaces.js";
import { init as initSettings, closeRightmost } from "./settings.js";
import { init as initGraph, loadGraph as loadGraphPanel } from "./graph.js";

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
  // `settings.js` (P9 Block settings): das Modul verdrahtet die Menüpunkte des Einstellungs-
  // Fensters und hält die Kette. Seine drei Eigentümer (`dialogs.js`, `spaces.js`,
  // `updates.js`) melden sich schon beim **Modul-Auswerten** über `registerPanel()`, also vor
  // dieser Zeile — die Aufrufreihenfolge der `init()`s spielt hier keine Rolle. Steht hier,
  // weil das Modul ohne `init()` gar nichts verdrahtet.
  initSettings();
  initSpaces();
  Editor.init();
  initGraph();

  // -- Übersicht / Logout / Zurück ---------------------------------------------------------

  var homeButtonEl = document.getElementById("home-button");
  // Phase 8 Block D D1 + D2 (Plan §5 D1/D2), Phase 8.6 Plan 2 Block G G3 (P8.6-AA): Klick
  // auf den Übersicht-Knopf schließt den Editor (mit Rueckfrage bei ungespeicherten
  // Aenderungen), schaltet die Listen-Spalte auf die Spaces-Übersicht UND laedt den Graph
  // neu.
  //
  // **V110 als negativer Befund:** `#home-button` und `.tree__scope` ("Alle Items") riefen
  // bisher beide `navigateAll()` -- denselben Knopf, dieselbe Aktion. Plan 2 §4.3 hat sie
  // getrennt: `#home-button` -> Spaces-Übersicht (state.overview = true), `.tree__scope` ->
  // globaler "Alle Items"-Modus (navigateAll, state.overview = false).
  //
  // **state.overview = true wird VOR closeEditor() gesetzt**, nicht im .then(). Grund:
  // closeEditor() -> clearDetail() -> renderListSlot() rendert bereits. Würden wir erst
  // im .then() umschalten, zeigte der erste Frame nach dem Schließen die Item-Liste statt
  // der Übersicht. Bricht der Nutzer die Rückfrage ab (proceed === false), wird es im
  // else-Zweig wieder auf den vorherigen Wert zurückgesetzt -- sonst wechselt ein
  // *abgebrochener* Navigationsversuch trotzdem die Ansicht.
  homeButtonEl.addEventListener("click", function () {
    var previousOverview = state.overview;
    state.overview = true;
    Editor.closeEditor().then(function (proceed) {
      if (proceed === false) {
        state.overview = previousOverview;
        return;
      }
      loadGraphPanel();
    }).catch(function (err) {
      // Sicherheitsnetz: wenn closeEditor() wirft, müssen wir die Overview-Flag selbst
      // wieder zurückrollen, der else-Zweig oben läuft sonst nicht.
      state.overview = previousOverview;
      reportUnexpectedError(err);
    });
  });

  // Phase 8 Block B Step B4 (Plan §3 B4): Klick-Delegation auf `a[href^="#item/"]`. Verwendet
  // den vorhandenen ID-Lookup aus `_items_get` über `GET /api/v1/items/{id}` (Plan §3 B4
  // V86: wiederverwenden, nichts erfinden). Wird auf `document` gehängt, weil das Markdown-
  // Rendering viele Stellen haben kann (Editor-Vorschau, Übersicht, Detail-Readonly) und
  // einzelne Handler an jeder Render-Stelle Code-Duplikate wären.
  var linkPickerDialogEl = document.getElementById("link-picker-dialog");
  document.addEventListener("click", function (event) {
    var anchor = event.target && event.target.closest
      ? event.target.closest('a[href^="#item/"]')
      : null;
    if (!anchor) return;
    var href = anchor.getAttribute("href") || "";
    var match = /^#item\/(itm_[0-9a-f]{8})$/.exec(href);
    if (!match) return;
    event.preventDefault();
    Editor.selectItem(match[1]).catch(reportUnexpectedError);
  });

  document.getElementById("logout-button").addEventListener("click", function () {
    fetch("/ui/logout", { method: "POST", headers: { "X-CSRF-Token": csrfToken() || "" } }).then(
      function () { location.replace("/ui/login"); }
    );
  });

  // Phase 8 Block D D1 + D2 (Plan §5 D1/D2): Refresh-Knopf in der Übersichts-Kopfzeile.
  // Laedt die Übersicht UND den Graph neu -- die Uebersicht liefert die Zaehler (Plan §5 D1
  // haelt den 20s-Polling auf die Zaehler beschraenkt, Refresh ist der einzige Ausloeser
  // fuer den Graph-Reload, damit der Server nicht bei jedem Tick die `/graph`-Query feuert).
  // Beide Calls laufen parallel; ein Fehler in einem blockiert den anderen nicht.
  // P9 Step E: `force: true` ist die **einzige** Ausnahme vom Token-Mechanismus — der Knopf
  // heißt "aktualisieren", und genau für ihn darf die Reihenfolge der zwei parallelen Calls
  // nicht entscheiden (ohne force könnte der Graph laufen, bevor das neue /overview da ist,
  // und deshalb einen Abruf überspringen, obwohl sich etwas geändert hat).
  document.getElementById("overview-refresh").addEventListener("click", function () {
    List.loadOverview().catch(reportUnexpectedError);
    loadGraphPanel({ force: true });
  });

  document.getElementById("back-button").addEventListener("click", function () {
    shellEl.dataset.view = "list";
  });

  // -- Tastatur (§4.6) ----------------------------------------------------------------------

  var conflictDialogEl = document.getElementById("conflict-dialog");
  var createDialogEl = document.getElementById("create-dialog");
  // Step 7 Commit 3, kleine dokumentierte Abweichung vom Plan-Dateiwortlaut (der app.js für
  // diesen Commit nicht nennt): die beiden neuen Dialoge brauchen dieselbe Escape-Behandlung
  // wie jeder andere Overlay-Dialog hier — sie ihr eigenes Süppchen kochen zu lassen wäre eine
  // stillschweigend inkonsistente Tastaturbedienung, kein kleinerer Eingriff.
  var newFolderDialogEl = document.getElementById("new-folder-dialog");
  var moveDialogEl = document.getElementById("move-dialog");
  // Step 7 Commit 5b, dieselbe dokumentierte Abweichung wie Commit 3 oben (app.js steht nicht
  // auf der Plan-Dateiliste dieses Commits) — derselbe Grund: konsistente Tastaturbedienung für
  // jeden Overlay-Dialog, kein Sonderfall für den neuen.
  var shareDialogEl = document.getElementById("share-dialog");
  var confirmDialogEl = document.getElementById("confirm-dialog");
  // P9 Step G: der Löschdialog ist ein Overlay wie alle anderen und gehört deshalb in
  // `anyOverlayOpen()` und in die ESC-Kette -- sonst wäre er der einzige Dialog, den ESC nicht
  // schliesst und den die Tastaturbedienung nicht kennt.
  var trashDialogEl = document.getElementById("trash-dialog");
  // P9 Block settings: die drei früheren Overlays (#account-dialog, #space-admin-dialog,
  // #update-log-dialog) sind **eine** Kette. Für ESC ist sie ein Dialog mit einer eigenen
  // Reihenfolge (P9-AH: das rechteste Panel zuerst) — deshalb `closeRightmost()` statt
  // dreier Einzelzweige. `#space-remove-dialog` steht in der Kette **darüber**: es ist ein
  // modales Bestätigungsfenster (Plan §0.3) und muss vor `closeRightmost()` geprüft werden,
  // sonst schlöß ein ESC das Entfernen-Fenster und der Klick daneben läge wieder frei.
  var settingsOverlayEl = document.getElementById("settings-overlay");
  // P7 Step C3: das Entfernen-Fenster. Es bleibt ein eigenes modales Overlay **über** der
  // Kette (Plan §0.3) und steht deshalb in der ESC-Kette vor `closeRightmost()`.
  var spaceRemoveDialogEl = document.getElementById("space-remove-dialog");
  var detailEditorEl = document.getElementById("detail-editor");
  var searchInputEl = document.getElementById("search-input");
  // P9 Step A: Hinweis auf der alten Adresse -- ein Overlay wie alle anderen, also auch in
  // `anyOverlayOpen()` und in der ESC-Kette (dieselbe Begründung wie beim Löschdialog).
  var legacyHostDialogEl = document.getElementById("legacy-host-dialog");
  document.getElementById("legacy-host-close").addEventListener("click", function () {
    legacyHostDialogEl.hidden = true;
  });

  function formatGermanDate(iso) {
    var parts = iso.split("-");
    return parts[2] + "." + parts[1] + "." + parts[0];
  }

  function showLegacyHostDialog(meta) {
    var legacy = meta.legacy;
    if (!legacy || location.origin !== legacy.origin) return;
    // Drei Zustände: unbefristet (`until` null, 2026-10-05), befristet, abgelaufen.
    var title, text, stay;
    if (legacy.writable && !legacy.until) {
      title = "Es gibt eine neue Adresse";
      text = "Die neue Adresse ist " + meta.canonical_url + ". Falls dein Netz sie noch nicht "
        + "erreicht (z. B. Firmen-VPN), arbeite einfach hier weiter: diese Adresse funktioniert "
        + "bis auf Weiteres vollständig, Lesen und Schreiben. Ein Abschalttermin wird vorher angekündigt.";
      stay = "Hier weiterarbeiten";
    } else if (legacy.writable) {
      title = "Diese Adresse wird abgeschaltet";
      text = "Bitte ab sofort " + meta.canonical_url + " verwenden. Hier funktioniert bis einschließlich "
        + formatGermanDate(legacy.until) + " noch alles, danach nur noch Lesen.";
      stay = "Trotzdem hier bleiben";
    } else {
      title = "Diese Adresse ist nur noch lesbar";
      text = "Änderungen gehen nur noch über " + meta.canonical_url + ".";
      stay = "Hier nur lesen";
    }
    document.getElementById("legacy-host-title").textContent = title;
    document.getElementById("legacy-host-text").textContent = text;
    document.getElementById("legacy-host-close").textContent = stay;
    document.getElementById("legacy-host-link").href = meta.canonical_url + "/ui/";
    legacyHostDialogEl.hidden = false;
  }

  function anyOverlayOpen() {
    return !conflictDialogEl.hidden || !createDialogEl.hidden || !newFolderDialogEl.hidden
      || !moveDialogEl.hidden || !shareDialogEl.hidden || !confirmDialogEl.hidden
      || !trashDialogEl.hidden || !settingsOverlayEl.hidden
      || !spaceRemoveDialogEl.hidden || !linkPickerDialogEl.hidden || !legacyHostDialogEl.hidden;
  }

  // P9-BK (Block feedback B6): Enter löst in jedem Overlay die Primäraktion aus (Plan §5). Eine
  // Tabelle statt elf Einzelhandlern: Overlay -> Primärknopf -> erlaubte Felder (`null` = jedes
  // Textfeld). Reihenfolge wie bei ESC. **Ausgenommen:** `conflict-dialog` (zwei gleichrangige
  // Wege, Enter wäre Raten) und `link-picker-dialog` (eigener Enter-Weg in `dialogs.js`, sonst
  // doppelt). `<textarea>`/`<select>`/`<button>` behalten ihr natives Enter. Ein gesperrter Knopf
  // (`disabled`, z. B. Löschen ohne passenden Titel) bleibt folgenlos — das Gate wird nicht umgangen.
  function enterTable() {
    return [
      [confirmDialogEl, "confirm-ok", "none"],
      [conflictDialogEl, null, null],
      [createDialogEl, "create-submit", null],
      [newFolderDialogEl, "new-folder-submit", null],
      [moveDialogEl, "move-submit", ["move-reauth-totp"]],
      [shareDialogEl, "share-submit", ["share-reauth-totp"]],
      [trashDialogEl, "trash-submit", null],
      [spaceRemoveDialogEl, "space-remove-submit", ["space-remove-confirm-input", "space-remove-reauth-totp"]],
      [settingsOverlayEl, "settings", null],
      [linkPickerDialogEl, null, null],
      [legacyHostDialogEl, "legacy-host-close", "none"],
    ];
  }
  var SETTINGS_ENTER = {
    "settings-password": { button: "account-submit", fields: ["account-totp"] },
    "settings-spaces": { button: "space-create-submit", fields: ["space-create-name-input"] },
    "settings-space-detail": { button: "space-member-add-submit",
      fields: ["space-member-name-input", "space-member-reauth-totp"] },
  };

  function enterPrimaryAction(event, tag) {
    if (tag === "TEXTAREA" || tag === "SELECT" || tag === "BUTTON" || tag === "A") return false;
    var target = document.activeElement;
    var rows = enterTable();
    for (var i = 0; i < rows.length; i++) {
      if (rows[i][0].hidden) continue;
      var buttonId = rows[i][1];
      var fields = rows[i][2];
      if (!buttonId) return false;
      if (buttonId === "settings") {
        var panel = target && target.closest && target.closest(".settings-panel");
        var rule = panel && SETTINGS_ENTER[panel.id];
        if (!rule || rule.fields.indexOf(target.id) === -1) return false;
        buttonId = rule.button;
      } else if (fields === "none") {
        if (tag === "INPUT") return false;
      } else if (tag !== "INPUT" || !rows[i][0].contains(target)
          || (fields && fields.indexOf(target.id) === -1)) {
        return false;
      }
      var button = document.getElementById(buttonId);
      if (!button || button.hidden || button.disabled) return false;
      button.click();
      return true;
    }
    return false;
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
      // Der Browser verlaesst bei ESC selbst den Vollbildmodus und liefert denselben
      // Tastendruck zusaetzlich an die App -- ohne diese Zeile loest ein Druck zwei
      // Aktionen aus (Nikinger-Meldung 2026-09-19, Mac; P9 Step D1).
      if (document.fullscreenElement) return;
      if (!confirmDialogEl.hidden && pendingConfirmCancel) pendingConfirmCancel();
      else if (!conflictDialogEl.hidden) hideConflictDialog();
      else if (!createDialogEl.hidden) closeCreateDialog();
      else if (!newFolderDialogEl.hidden) closeNewFolderDialog();
      else if (!moveDialogEl.hidden) closeMoveDialog();
      else if (!shareDialogEl.hidden) closeShareDialog();
      // P9 Step G: `closeTrashDialog()` statt `hidden = true` — der Dialog hält einen
      // `pendingTrashCancel`, der das Promise auflöst; ein bloßes Verstecken ließe es hängen
      // und der Aufrufer (list.js) wartete ewig auf eine Antwort.
      else if (!trashDialogEl.hidden) closeTrashDialog();
      else if (!spaceRemoveDialogEl.hidden) closeRemoveSpaceDialog();
      // Die Kette schließt von rechts nach links (P9-AH) und weiß selbst, was rechts steht.
      else if (!settingsOverlayEl.hidden) closeRightmost();
      else if (!linkPickerDialogEl.hidden) closeLinkPicker();
      else if (!legacyHostDialogEl.hidden) legacyHostDialogEl.hidden = true;
      else if (state.selectedId !== null) Editor.closeEditor();
      return;
    }
    if (event.key === "Enter" && !event.shiftKey && !event.altKey && !event.metaKey
        && !event.ctrlKey && !event.isComposing) {
      if (enterPrimaryAction(event, tag)) event.preventDefault();
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
        // P7-R: der Kill-Switch blendet den Menüpunkt aus, statisches HTML kennt ihn nicht
        // (kein Templating, P5-T) -- ohne diese Zeile führte ein `False` nur serverseitig zu
        // `404`, der Knopf bliebe sichtbar und würde bei jedem Klick nur einen Fehler zeigen.
        document.getElementById("account-manage-spaces").hidden = !meta.space_admin;
        showLegacyHostDialog(meta);
        var names = Object.keys(meta.buckets);
        if (names.indexOf(state.filter) === -1) state.filter = names[0];
        // P9 Step E: `loadOverview()` setzt `state.graphToken`, das `loadGraph()` unten liest —
        // deshalb muss dieser Aufruf VOR dem ersten `loadGraphPanel()` stehen, sonst erfasst der
        // erste Abruf `null` und der erste Sprung in die Übersicht holt erneut.
        return List.loadOverview();
      })
      .then(function () {
        setCreateControlsPresent(activeSpaceWritable());
        List.renderCrumb();
        return List.loadItems();
      })
      .then(function () {
        // Graph laeuft unabhaengig vom Listen-Scope -- die erste Anzeige ist der Default-
        // Zustand (explizite Kanten, Toggles aus). Plan §5 D2 haelt den 20s-Polling auf die
        // Zaehler beschraenkt; Graph-Refresh nur hier, ueber den Home-Knopf und ueber den
        // Refresh-Knopf im Uebersichts-Kopf.
        return loadGraphPanel();
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
    // P9 Step E (Plan §7.2a): dieses `/overview` ist zugleich die Signatur für den Graphen
    // (`state.graphToken`, gesetzt in `list.js`). Der Poll läuft alle 20 s, bei Fokus und bei
    // Rückkehr in den Tab — der Home-Knopf weiß dadurch ohne eigenen Abruf, ob sich seit dem
    // letzten Graphen-Laden etwas geändert hat (P9-33).
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
