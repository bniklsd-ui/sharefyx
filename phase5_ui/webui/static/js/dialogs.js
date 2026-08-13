"use strict";

// -- Rückfragedialog, Anlegen-Dialog, Konflikt-Dialog, Konto-Dialog -------------------------
// Ein Modul für alle Overlay-Dialoge (Plan-Dateiliste nennt kein eigenes conflict.js/account.js
// — dieselbe Datei, weil alle vier denselben Charakter haben: modal, per `hidden`-Attribut
// gesteuert, kein eigener Zustand außerhalb dessen, was sie gerade anzeigen).

import { state, TYPE_LABELS, activeSpaceWritable, spaceByName } from "./state.js";
import { toast } from "./toasts.js";
import { api, csrfToken } from "./api.js";
import { navigate } from "./tree.js";
import {
  loadEditorFromItem, clearDraft, updateVersionBand, afterWrite, handleWriteError,
  currentFormValues,
} from "./editor.js";
import { loadOverview, loadItems, bucketFor } from "./list.js";

var createDialogEl;
var createTypeEl;
var createTitleInputEl;
var createSubmitButtonEl;
var createCancelButtonEl;
var createButtonEl;
var newItemButtonEl;

var conflictDialogEl;
var conflictMessageEl;
var conflictLoadCurrentButtonEl;
var conflictSaveAsNewButtonEl;
var conflictCancelButtonEl;

var confirmDialogEl;
var confirmTitleEl;
var confirmMessageEl;
var confirmOkEl;
var confirmCancelEl;

var accountDialogEl;
var accountErrorEl;
var accountCurrentEl;
var accountTotpEl;
var accountNewEl;
var accountRepeatEl;
var accountSubmitEl;
var accountCancelEl;
var accountButtonEl;

var searchInputEl;

var newFolderDialogEl;
var newFolderParentSelectEl;
var newFolderNameInputEl;
var newFolderSubmitEl;
var newFolderCancelEl;

var moveDialogEl;
var moveFolderSelectEl;
var moveSubmitEl;
var moveCancelEl;
var moveTargetItem = null;

// -- Rückfragedialog (ersetzt window.confirm) ----------------------------------------------

export var pendingConfirmCancel = null;

export function confirmDialog(options) {
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

// -- Speichern / Konflikt (§4.5, Akzeptanzkriterium 11) ------------------------------------

export function showConflictDialog(current) {
  state.conflictCurrent = current;
  updateVersionBand();
  conflictMessageEl.textContent =
    "Ein anderer Client hat dieses Item zwischenzeitlich geändert (deine Version v"
    + state.editingSnapshot.version + " → aktuelle Version v" + current.version + ").";
  conflictDialogEl.hidden = false;
}

export function hideConflictDialog() {
  conflictDialogEl.hidden = true;
  state.conflictCurrent = null;
  updateVersionBand();
}

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

export function closeCreateDialog() {
  createDialogEl.hidden = true;
}

// -- Neuer Ordner (Step 7 Commit 3, K4) ------------------------------------------------------
// Ein Elternordner-Dropdown statt eines Knopfs pro Baumzeile: funktional dieselbe Grenze wie
// "Knopf bei Tiefe 2 deaktiviert" aus dem Plan — nur Tiefe-1-Ordner stehen als Elternoption zur
// Wahl, ein Tiefe-2-Ordner würde als Elternteil eine unzulässige Tiefe 3 erzeugen und taucht
// deshalb im Dropdown gar nicht erst auf, statt als deaktivierte Option daneben zu stehen.
// Vermeidet außerdem, jede Baumzeile um einen zweiten, verschachtelten Button erweitern zu
// müssen (dieselbe Falle wie bei den Listenzeilen, siehe list.js).

export function openNewFolderDialog() {
  if (!state.ownSpace) return;   // sollte nicht erreichbar sein, der Knopf existiert nur fürs eigene Space
  newFolderParentSelectEl.textContent = "";
  var rootOption = document.createElement("option");
  rootOption.value = "";
  rootOption.textContent = "(oberste Ebene)";
  newFolderParentSelectEl.appendChild(rootOption);
  var own = spaceByName(state.ownSpace);
  ((own && own.folders) || [])
    .filter(function (path) { return path.indexOf("/") === -1; })
    .forEach(function (path) {
      var opt = document.createElement("option");
      opt.value = path;
      opt.textContent = path;
      newFolderParentSelectEl.appendChild(opt);
    });
  newFolderNameInputEl.value = "";
  newFolderDialogEl.hidden = false;
  newFolderNameInputEl.focus();
}

export function closeNewFolderDialog() {
  newFolderDialogEl.hidden = true;
}

// -- Verschieben (Step 7 Commit 3) ------------------------------------------------------------
// Bewusst KEIN Wiederverwenden von `handleWriteError()`/`showConflictDialog()`: die sind an
// `state.editingSnapshot` gekoppelt (das aktuell IM EDITOR offene Item) — ein Verschieben aus
// der Liste heraus betrifft aber typischerweise ein ANDERES Item als das gerade offene, teils
// gar keines. `showConflictDialog()` bliebe dann auf einem `null`/falschen Snapshot sitzen. Ein
// eigener, schlichter Fehlerpfad ist hier korrekt, keine Abkürzung.

export function openMoveDialog(item) {
  moveTargetItem = item;
  moveFolderSelectEl.textContent = "";
  var rootOption = document.createElement("option");
  rootOption.value = "";
  rootOption.textContent = "(kein Ordner)";
  moveFolderSelectEl.appendChild(rootOption);
  var space = spaceByName(item.space);
  ((space && space.folders) || []).forEach(function (path) {
    var opt = document.createElement("option");
    opt.value = path;
    opt.textContent = path.split("/").join(" / ");
    moveFolderSelectEl.appendChild(opt);
  });
  moveFolderSelectEl.value = item.folder || "";
  moveDialogEl.hidden = false;
}

export function closeMoveDialog() {
  moveDialogEl.hidden = true;
  moveTargetItem = null;
}

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

export function init() {
  createDialogEl = document.getElementById("create-dialog");
  createTypeEl = document.getElementById("create-type");
  createTitleInputEl = document.getElementById("create-title-input");
  createSubmitButtonEl = document.getElementById("create-submit");
  createCancelButtonEl = document.getElementById("create-cancel");
  createButtonEl = document.getElementById("create-button");
  newItemButtonEl = document.getElementById("new-item-button");

  conflictDialogEl = document.getElementById("conflict-dialog");
  conflictMessageEl = document.getElementById("conflict-message");
  conflictLoadCurrentButtonEl = document.getElementById("conflict-load-current");
  conflictSaveAsNewButtonEl = document.getElementById("conflict-save-as-new");
  conflictCancelButtonEl = document.getElementById("conflict-cancel");

  confirmDialogEl = document.getElementById("confirm-dialog");
  confirmTitleEl = document.getElementById("confirm-title");
  confirmMessageEl = document.getElementById("confirm-message");
  confirmOkEl = document.getElementById("confirm-ok");
  confirmCancelEl = document.getElementById("confirm-cancel");

  accountDialogEl = document.getElementById("account-dialog");
  accountErrorEl = document.getElementById("account-error");
  accountCurrentEl = document.getElementById("account-current");
  accountTotpEl = document.getElementById("account-totp");
  accountNewEl = document.getElementById("account-new");
  accountRepeatEl = document.getElementById("account-repeat");
  accountSubmitEl = document.getElementById("account-submit");
  accountCancelEl = document.getElementById("account-cancel");
  accountButtonEl = document.getElementById("account-button");

  searchInputEl = document.getElementById("search-input");

  newFolderDialogEl = document.getElementById("new-folder-dialog");
  newFolderParentSelectEl = document.getElementById("new-folder-parent-select");
  newFolderNameInputEl = document.getElementById("new-folder-name-input");
  newFolderSubmitEl = document.getElementById("new-folder-submit");
  newFolderCancelEl = document.getElementById("new-folder-cancel");

  moveDialogEl = document.getElementById("move-dialog");
  moveFolderSelectEl = document.getElementById("move-folder-select");
  moveSubmitEl = document.getElementById("move-submit");
  moveCancelEl = document.getElementById("move-cancel");

  newFolderCancelEl.addEventListener("click", closeNewFolderDialog);
  newFolderSubmitEl.addEventListener("click", function () {
    var name = newFolderNameInputEl.value.trim();
    if (!name) { newFolderNameInputEl.focus(); return; }
    var parent = newFolderParentSelectEl.value;
    var folder = parent ? parent + "/" + name : name;
    api("/spaces/" + encodeURIComponent(state.ownSpace) + "/folders", {
      method: "POST", body: JSON.stringify({ folder: folder }),
    }).then(function (result) {
      closeNewFolderDialog();
      return loadOverview().then(function () { toast("Ordner angelegt · " + result.folder); });
    }).catch(function (err) {
      if (err.message === "unauthenticated") return;
      toast(err.message || "Ordner anlegen fehlgeschlagen.", "error");
    });
  });

  moveCancelEl.addEventListener("click", closeMoveDialog);
  moveSubmitEl.addEventListener("click", function () {
    var item = moveTargetItem;
    if (!item) return;
    var folder = moveFolderSelectEl.value;
    api("/items/" + encodeURIComponent(item.id), {
      method: "PATCH", body: JSON.stringify({ version: item.version, folder: folder }),
    }).then(function () {
      closeMoveDialog();
      return loadItems().then(loadOverview).then(function () {
        toast(folder ? "Verschoben nach " + folder.split("/").join(" / ") : "In die oberste Ebene verschoben");
      });
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

  conflictLoadCurrentButtonEl.addEventListener("click", function () {
    var current = state.conflictCurrent;
    var mode = state.mode;   // wer gerade bearbeitet hat, bleibt beim Bearbeiten (siehe editor.js :: afterWrite())
    clearDraft(current.id);
    hideConflictDialog();
    loadEditorFromItem(current, { mode: mode });
    toast("Aktuelle Fassung geladen · v" + current.version, "warn");
  });

  conflictSaveAsNewButtonEl.addEventListener("click", function () {
    var values = currentFormValues();
    var payload = Object.assign({ type: state.editingSnapshot.type, format: "markdown" }, values);
    var previousId = state.editingSnapshot.id;   // siehe F7-Kommentar in editor.js über saveItem()
    hideConflictDialog();
    api("/items", { method: "POST", body: JSON.stringify(payload) }).then(function (item) {
      clearDraft(previousId);
      return afterWrite(item, "Als neues Item angelegt · " + item.title);
    }).catch(function (err) {
      handleWriteError(err, "Anlegen fehlgeschlagen.");
    });
  });

  conflictCancelButtonEl.addEventListener("click", hideConflictDialog);

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
          document.getElementById("field-title").focus();
        });
    }).catch(function (err) {
      handleWriteError(err, "Anlegen fehlgeschlagen.");
    });
  });

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
}
