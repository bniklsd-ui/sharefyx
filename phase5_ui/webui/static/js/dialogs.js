"use strict";

// -- Rückfragedialog, Anlegen-Dialog, Konflikt-Dialog, Konto-Dialog -------------------------
// Ein Modul für alle Overlay-Dialoge (Plan-Dateiliste nennt kein eigenes conflict.js/account.js
// — dieselbe Datei, weil alle vier denselben Charakter haben: modal, per `hidden`-Attribut
// gesteuert, kein eigener Zustand außerhalb dessen, was sie gerade anzeigen).

import { state, TYPE_LABELS, activeSpaceWritable, spaceByName } from "./state.js";
import { el, toast } from "./toasts.js";
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
var moveSpaceSelectEl;
var moveFolderSelectEl;
var moveConsequenceEl;
var moveErrorEl;
var moveReauthFieldsEl;
var moveReauthPasswordEl;
var moveReauthTotpEl;
var moveSubmitEl;
var moveCancelEl;
var moveTargetItem = null;
var pendingMoveBody = null;

var shareDialogEl;
var shareItemTitleEl;
var shareErrorEl;
var shareRowsEl;
var shareReauthFieldsEl;
var shareReauthPasswordEl;
var shareReauthTotpEl;
var shareSubmitEl;
var shareCancelEl;
var shareTargetItem = null;
var pendingShareBody = null;

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

// -- Verschieben (Step 7 Commit 3, Step 7b: Space-Auswahl) --------------------------------------
// Bewusst KEIN Wiederverwenden von `handleWriteError()`/`showConflictDialog()`: die sind an
// `state.editingSnapshot` gekoppelt (das aktuell IM EDITOR offene Item) — ein Verschieben aus
// der Liste heraus betrifft aber typischerweise ein ANDERES Item als das gerade offene, teils
// gar keines. `showConflictDialog()` bliebe dann auf einem `null`/falschen Snapshot sitzen. Ein
// eigener, schlichter Fehlerpfad ist hier korrekt, keine Abkürzung.
//
// Step 7b (ITEM_MOVE_PLAN.md §4.4): derselbe Dialog trägt jetzt zusätzlich eine Space-Auswahl
// (nur `writable: true`-Spaces, Punkt 1) — ein Wechsel des Space baut die Ordnerliste für den
// NEU gewählten Space neu auf und setzt sie auf "(Space-Wurzel)" zurück (§4.1 Punkt 3: ein
// Space-Wechsel ohne eigene Ordnerwahl landet an der Ziel-Wurzel, nicht im gleichnamigen Ordner
// im Zielspace). Re-Auth folgt demselben eingefrorenen-erste-Fassung-Muster wie der
// Freigabedialog (`pendingShareBody`/Advisor-Vorgabe) — hier `pendingMoveBody`.

function populateMoveFolderOptions(spaceName, selectedFolder) {
  moveFolderSelectEl.textContent = "";
  var rootOption = document.createElement("option");
  rootOption.value = "";
  rootOption.textContent = "(Space-Wurzel)";
  moveFolderSelectEl.appendChild(rootOption);
  var space = spaceByName(spaceName);
  ((space && space.folders) || []).forEach(function (path) {
    var opt = document.createElement("option");
    opt.value = path;
    opt.textContent = path.split("/").join(" / ");
    moveFolderSelectEl.appendChild(opt);
  });
  moveFolderSelectEl.value = selectedFolder || "";
}

function updateMoveConsequence(item) {
  var target = moveSpaceSelectEl.value;
  if (target === item.space) {
    moveConsequenceEl.textContent = "";
    return;
  }
  moveConsequenceEl.textContent =
    "Verschiebt das Item aus " + item.space + " nach " + target + ". Alle Mitglieder dieses "
    + "Space können es danach lesen und ändern.";
}

export function openMoveDialog(item) {
  moveTargetItem = item;
  pendingMoveBody = null;
  moveErrorEl.hidden = true;
  moveReauthFieldsEl.hidden = true;
  moveReauthPasswordEl.value = "";
  moveReauthTotpEl.value = "";
  moveSpaceSelectEl.textContent = "";
  state.spaces.filter(function (space) { return space.writable; }).forEach(function (space) {
    var opt = document.createElement("option");
    opt.value = space.name;
    opt.textContent = space.name;
    moveSpaceSelectEl.appendChild(opt);
  });
  moveSpaceSelectEl.value = item.space;
  populateMoveFolderOptions(item.space, item.folder);
  updateMoveConsequence(item);
  moveDialogEl.hidden = false;
}

export function closeMoveDialog() {
  moveDialogEl.hidden = true;
  moveTargetItem = null;
  pendingMoveBody = null;
}

// -- Freigeben (Step 7 Commit 5b) -------------------------------------------------------------
// Ein PATCH mit `share_read`/`share_write` kann die effektive Lese-/Schreibmenge erweitern
// (`webui.shares :: widens()`, Commit 5a) — der Server antwortet dann `403 reauth_required`
// statt dem geänderten Item, statt es abzulehnen. `pendingShareBody` friert die Anfrage beim
// ERSTEN Absenden ein (Advisor-Hinweis vor diesem Commit): eine Auswahländerung, während das
// Re-Auth-Formular offen ist, darf nicht plötzlich eine andere Anfrage ausliefern als die, die
// das Gate tatsächlich geprüft hat — nur `password`/`totp` werden bei jedem Versuch frisch aus
// den Feldern gelesen, der Rest bleibt die eingefrorene erste Fassung.
//
// Nur Spaces, die dieser Actor bereits kennt (`state.spaces`, aus `/api/v1/spaces` — P6-V: eine
// vollständige, ungefilterte Space-Liste gibt es für einen Menschen absichtlich nicht, Space-
// Verwaltung bleibt CLI-only). Freigeben ist damit auf „mit einem bereits sichtbaren Space
// teilen" begrenzt — ein bewusster, benannter Schnitt, kein Versehen.
//
// Kein `visibility`-Feld in diesem Dialog (Scope-Schnitt derselben Session, Advisor bestätigt):
// der Chip zeigt `visibility` bereits an (Commit 2), niemand hat verlangt, sie aus der UI heraus
// zu ändern — ein Freigabe-MATRIX-Dialog plus ein Re-Auth-Formular ist für einen Commit genug.

function shareRowSelectValue(item, spaceName) {
  if (item.share_write.indexOf(spaceName) !== -1) return "write";
  if (item.share_read.indexOf(spaceName) !== -1) return "read";
  return "";
}

export function openShareDialog(item) {
  shareTargetItem = item;
  pendingShareBody = null;
  shareErrorEl.hidden = true;
  shareReauthFieldsEl.hidden = true;
  shareReauthPasswordEl.value = "";
  shareReauthTotpEl.value = "";
  shareItemTitleEl.textContent = item.title;
  shareRowsEl.textContent = "";
  state.spaces
    .filter(function (space) { return space.name !== item.space; })
    .forEach(function (space) {
      var label = el("label", null, space.name);
      var select = document.createElement("select");
      select.className = "input";
      select.dataset.space = space.name;
      [["", "kein Zugriff"], ["read", "lesen"], ["write", "schreiben"]].forEach(function (pair) {
        var opt = document.createElement("option");
        opt.value = pair[0];
        opt.textContent = pair[1];
        select.appendChild(opt);
      });
      select.value = shareRowSelectValue(item, space.name);
      label.appendChild(select);
      shareRowsEl.appendChild(label);
    });
  shareDialogEl.hidden = false;
}

export function closeShareDialog() {
  shareDialogEl.hidden = true;
  shareTargetItem = null;
  pendingShareBody = null;
}

function shareError(message) {
  shareErrorEl.textContent = message;
  shareErrorEl.hidden = false;
}

function collectShareBody(item) {
  var shareRead = [];
  var shareWrite = [];
  // `write` reicht als alleiniger Eintrag in `share_write` — `acl.py :: decision_for()` bildet
  // `read = grant.read | item_read | item_write`, ein Schreib-Grantee ist also automatisch auch
  // lese-effektiv, ohne zusätzlich in `share_read` zu stehen (dieselbe Logik, die schon
  // `visibilityChip()`s `share_read.concat(share_write)`-Dedupe in `list.js` voraussetzt).
  Array.prototype.forEach.call(shareRowsEl.querySelectorAll("select"), function (select) {
    if (select.value === "read") shareRead.push(select.dataset.space);
    else if (select.value === "write") shareWrite.push(select.dataset.space);
  });
  return { version: item.version, share_read: shareRead, share_write: shareWrite };
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
  moveSpaceSelectEl = document.getElementById("move-space-select");
  moveFolderSelectEl = document.getElementById("move-folder-select");
  moveConsequenceEl = document.getElementById("move-consequence");
  moveErrorEl = document.getElementById("move-error");
  moveReauthFieldsEl = document.getElementById("move-reauth-fields");
  moveReauthPasswordEl = document.getElementById("move-reauth-password");
  moveReauthTotpEl = document.getElementById("move-reauth-totp");
  moveSubmitEl = document.getElementById("move-submit");
  moveCancelEl = document.getElementById("move-cancel");

  shareDialogEl = document.getElementById("share-dialog");
  shareItemTitleEl = document.getElementById("share-item-title");
  shareErrorEl = document.getElementById("share-error");
  shareRowsEl = document.getElementById("share-rows");
  shareReauthFieldsEl = document.getElementById("share-reauth-fields");
  shareReauthPasswordEl = document.getElementById("share-reauth-password");
  shareReauthTotpEl = document.getElementById("share-reauth-totp");
  shareSubmitEl = document.getElementById("share-submit");
  shareCancelEl = document.getElementById("share-cancel");

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
  moveSpaceSelectEl.addEventListener("change", function () {
    var item = moveTargetItem;
    if (!item) return;
    // Space-Wechsel setzt die Ordnerauswahl auf die Ziel-Wurzel zurück (§4.1 Punkt 3) --
    // ein Ordnername im alten Space bedeutet im neuen etwas anderes.
    populateMoveFolderOptions(moveSpaceSelectEl.value, "");
    updateMoveConsequence(item);
    pendingMoveBody = null;   // Ziel geändert -- eine evtl. eingefrorene Fassung ist ungültig
    moveReauthFieldsEl.hidden = true;
    moveErrorEl.hidden = true;
  });
  moveSubmitEl.addEventListener("click", function () {
    var item = moveTargetItem;
    if (!item) return;
    moveErrorEl.hidden = true;
    if (pendingMoveBody === null) {
      var targetSpace = moveSpaceSelectEl.value;
      var folder = moveFolderSelectEl.value;
      pendingMoveBody = { version: item.version, folder: folder };
      if (targetSpace !== item.space) pendingMoveBody.space = targetSpace;
    }
    var body = Object.assign({}, pendingMoveBody);
    if (!moveReauthFieldsEl.hidden) {
      body.password = moveReauthPasswordEl.value;
      body.totp = moveReauthTotpEl.value;
    }
    // Werte VOR `closeMoveDialog()` sichern -- die setzt `pendingMoveBody` auf `null` zurück
    // (echter Fund der Playwright-Verifikation dieser Session: `pendingMoveBody` nach dem
    // Schließen gelesen warf einen TypeError, der die Erfolgsmeldung stumm verschluckte).
    var movedFolder = pendingMoveBody.folder;
    var movedSpace = pendingMoveBody.space;
    api("/items/" + encodeURIComponent(item.id), {
      method: "PATCH", body: JSON.stringify(body),
    }).then(function () {
      closeMoveDialog();
      return loadItems().then(loadOverview).then(function () {
        toast(
          movedSpace
            ? "Verschoben nach " + movedSpace
            : (movedFolder ? "Verschoben nach " + movedFolder.split("/").join(" / ") : "In die oberste Ebene verschoben")
        );
      });
    }).catch(function (err) {
      if (err.code === "reauth_required") {
        moveReauthFieldsEl.hidden = false;
        moveErrorEl.textContent = err.message;
        moveErrorEl.hidden = false;
        moveReauthPasswordEl.focus();
        return;
      }
      if (err.code === "conflict") {
        moveErrorEl.textContent =
          "Ein anderer Client hat dieses Item zwischenzeitlich geändert — bitte neu laden und "
          + "erneut versuchen.";
        moveErrorEl.hidden = false;
        return;
      }
      if (err.message === "unauthenticated") return;
      moveErrorEl.textContent = err.message || "Verschieben fehlgeschlagen.";
      moveErrorEl.hidden = false;
    });
  });

  shareCancelEl.addEventListener("click", closeShareDialog);
  shareSubmitEl.addEventListener("click", function () {
    var item = shareTargetItem;
    if (!item) return;
    shareErrorEl.hidden = true;
    // Erste Fassung einfrieren, nicht bei jedem Versuch aus dem DOM neu bauen (Advisor-Hinweis)
    // — nur `password`/`totp` kommen bei jedem Klick frisch aus den Feldern.
    if (pendingShareBody === null) pendingShareBody = collectShareBody(item);
    var body = Object.assign({}, pendingShareBody);
    if (!shareReauthFieldsEl.hidden) {
      body.password = shareReauthPasswordEl.value;
      body.totp = shareReauthTotpEl.value;
    }
    api("/items/" + encodeURIComponent(item.id), {
      method: "PATCH", body: JSON.stringify(body),
    }).then(function () {
      closeShareDialog();
      return loadItems().then(loadOverview).then(function () { toast("Freigabe gespeichert."); });
    }).catch(function (err) {
      if (err.code === "reauth_required") {
        shareReauthFieldsEl.hidden = false;
        shareError(err.message);
        shareReauthPasswordEl.focus();
        return;
      }
      if (err.code === "conflict") {
        shareError(
          "Ein anderer Client hat dieses Item zwischenzeitlich geändert — bitte neu laden und "
          + "erneut versuchen.",
        );
        return;
      }
      if (err.message === "unauthenticated") return;
      shareError(err.message || "Freigeben fehlgeschlagen.");
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
