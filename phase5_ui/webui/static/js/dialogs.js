"use strict";

// -- Rückfragedialog, Anlegen-Dialog, Konflikt-Dialog, Konto-Dialog -------------------------
// Ein Modul für alle Overlay-Dialoge (Plan-Dateiliste nennt kein eigenes conflict.js/account.js
// — dieselbe Datei, weil alle vier denselben Charakter haben: modal, per `hidden`-Attribut
// gesteuert, kein eigener Zustand außerhalb dessen, was sie gerade anzeigen).

import { state, TYPE_LABELS, activeSpaceWritable } from "./state.js";
import { toast } from "./toasts.js";
import { api, csrfToken } from "./api.js";
import { navigate } from "./tree.js";
import {
  loadEditorFromItem, clearDraft, updateVersionBand, afterWrite, handleWriteError,
  currentFormValues,
} from "./editor.js";
import { loadOverview, bucketFor } from "./list.js";

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
