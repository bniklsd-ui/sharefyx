"use strict";

// -- Space-Verwaltung (P7 Step C3, P7-Q) ----------------------------------------------------
// Volle `spacectl.py`-Parität in der Weboberfläche: Space anlegen, Mitglieder hinzufügen/
// entfernen, Space entfernen (zweiphasig, Backend in Step C4). Home-Spaces (P7-K) erscheinen
// in der Liste, tragen aber keinen Entfernen-Knopf -- der Server lehnt das ohnehin ab
// (`_spaces_delete`), diese Sperre ist nur die client-seitige Vorwegnahme davon.
//
// Re-Auth folgt demselben eingefrorene-erste-Fassung-Muster wie `dialogs.js`s Freigabe-/
// Verschieben-Dialog (`pendingMemberBody`/`pendingRemoveBody`).

import { state, spaceByName } from "./state.js";
import { el, toast } from "./toasts.js";
import { api } from "./api.js";
import { loadOverview } from "./list.js";

var spaceAdminDialogEl;
var spaceAdminErrorEl;
var spaceAdminListEl;
var spaceCreateNameInputEl;
var spaceCreateSubmitEl;
var spaceAdminCloseEl;

var spaceDetailEl;
var spaceDetailNameEl;
var spaceDetailHomeHintEl;
var spaceMemberListEl;
var spaceMemberNameInputEl;
var spaceMemberWriteSelectEl;
var spaceMemberAddSubmitEl;
var spaceMemberReauthFieldsEl;
var spaceMemberReauthPasswordEl;
var spaceMemberReauthTotpEl;
var spaceRemoveOpenEl;

var spaceRemoveDialogEl;
var spaceRemoveConsequenceEl;
var spaceRemoveErrorEl;
var spaceRemoveConfirmInputEl;
var spaceRemoveReauthFieldsEl;
var spaceRemoveReauthPasswordEl;
var spaceRemoveReauthTotpEl;
var spaceRemoveSubmitEl;
var spaceRemoveCancelEl;

var selectedSpaceName = null;
var pendingMemberBody = null;

function spaceAdminError(message) {
  spaceAdminErrorEl.textContent = message;
  spaceAdminErrorEl.hidden = false;
}

function renderSpaceList() {
  spaceAdminListEl.textContent = "";
  state.spaces.filter(function (space) { return space.writable; }).forEach(function (space) {
    var row = el("div", "space-admin-row");
    var button = el("button", "btn", space.name + (space.name === state.ownSpace ? " (eigener Space)" : ""));
    button.type = "button";
    button.addEventListener("click", function () { selectSpace(space.name); });
    row.appendChild(button);
    spaceAdminListEl.appendChild(row);
  });
}

function selectSpace(name) {
  // Ziel geändert -- eine evtl. eingefrorene Fassung des Hinzufügen-Formulars ist ungültig
  // (dasselbe Muster/derselbe Grund wie `dialogs.js :: pendingMoveBody = null` beim
  // Space-Wechsel im Verschieben-Dialog) -- sonst würde ein Re-Auth-Retry nach einem
  // Space-Wechsel den EINGEFRORENEN Namen/Write-Wert gegen den NEUEN Space abschicken.
  pendingMemberBody = null;
  spaceMemberReauthFieldsEl.hidden = true;
  spaceMemberReauthPasswordEl.value = "";
  spaceMemberReauthTotpEl.value = "";
  spaceMemberNameInputEl.value = "";
  selectedSpaceName = name;
  spaceAdminErrorEl.hidden = true;
  return api("/spaces/" + encodeURIComponent(name) + "/members").then(function (info) {
    spaceDetailEl.hidden = false;
    spaceDetailNameEl.textContent = name;
    spaceDetailHomeHintEl.hidden = !info.home;
    spaceRemoveOpenEl.hidden = info.home;
    spaceMemberListEl.textContent = "";
    info.write.forEach(function (member) { spaceMemberListEl.appendChild(memberRow(name, member, true)); });
    info.read.forEach(function (member) { spaceMemberListEl.appendChild(memberRow(name, member, false)); });
    // C2s eigene Begründung für `orphans`: "der Render-Hinweis fürs Frontend" (Tippfehler-
    // Fänger gegen bekannte Space-Verzeichnisse, nur bei `manageable` überhaupt befüllt) --
    // ignoriert zu lassen würde das Feld ohne jeden Konsumenten seines einzigen Zwecks lassen.
    (info.orphans || []).forEach(function (name) {
      var row = el("li", "space-member-row space-member-row--orphan");
      row.appendChild(el("span", null, name + " (verwaist -- kein solcher Space mehr)"));
      spaceMemberListEl.appendChild(row);
    });
  }).catch(function (err) {
    if (err.message === "unauthenticated") return;
    spaceAdminError(err.message || "Mitgliederliste konnte nicht geladen werden.");
  });
}

function memberRow(space, name, canWrite) {
  var row = el("li", "space-member-row");
  row.appendChild(el("span", null, name + (canWrite ? " (schreiben)" : " (lesen)")));
  var removeButton = el("button", "btn", "Entfernen");
  removeButton.type = "button";
  removeButton.addEventListener("click", function () {
    api("/spaces/" + encodeURIComponent(space) + "/members/" + encodeURIComponent(name), {
      method: "DELETE",
    }).then(function () {
      toast("Mitglied entfernt · " + name);
      return selectSpace(space);
    }).catch(function (err) {
      if (err.message === "unauthenticated") return;
      spaceAdminError(err.message || "Entfernen fehlgeschlagen.");
    });
  });
  row.appendChild(removeButton);
  return row;
}

export function openSpaceAdminDialog() {
  spaceAdminErrorEl.hidden = true;
  spaceDetailEl.hidden = true;
  selectedSpaceName = null;
  pendingMemberBody = null;
  spaceCreateNameInputEl.value = "";
  spaceMemberNameInputEl.value = "";
  spaceMemberReauthFieldsEl.hidden = true;
  spaceMemberReauthPasswordEl.value = "";
  spaceMemberReauthTotpEl.value = "";
  renderSpaceList();
  spaceAdminDialogEl.hidden = false;
}

export function closeSpaceAdminDialog() {
  spaceAdminDialogEl.hidden = true;
  selectedSpaceName = null;
  pendingMemberBody = null;
}

function spaceRemoveError(message) {
  spaceRemoveErrorEl.textContent = message;
  spaceRemoveErrorEl.hidden = false;
}

export function openRemoveSpaceDialog(space) {
  spaceRemoveErrorEl.hidden = true;
  spaceRemoveReauthFieldsEl.hidden = true;
  spaceRemoveReauthPasswordEl.value = "";
  spaceRemoveReauthTotpEl.value = "";
  spaceRemoveConfirmInputEl.value = "";
  spaceRemoveConsequenceEl.textContent =
    "Alle Items in " + space + " wandern in deinen Space " + state.ownSpace
    + " und werden dort archiviert. Der Space " + space + " selbst verschwindet. Die "
    + "Zuordnung ist danach weg.";
  spaceRemoveDialogEl.hidden = false;
}

export function closeRemoveSpaceDialog() {
  spaceRemoveDialogEl.hidden = true;
}

export function init() {
  spaceAdminDialogEl = document.getElementById("space-admin-dialog");
  spaceAdminErrorEl = document.getElementById("space-admin-error");
  spaceAdminListEl = document.getElementById("space-admin-list");
  spaceCreateNameInputEl = document.getElementById("space-create-name-input");
  spaceCreateSubmitEl = document.getElementById("space-create-submit");
  spaceAdminCloseEl = document.getElementById("space-admin-close");

  spaceDetailEl = document.getElementById("space-detail");
  spaceDetailNameEl = document.getElementById("space-detail-name");
  spaceDetailHomeHintEl = document.getElementById("space-detail-home-hint");
  spaceMemberListEl = document.getElementById("space-member-list");
  spaceMemberNameInputEl = document.getElementById("space-member-name-input");
  spaceMemberWriteSelectEl = document.getElementById("space-member-write-select");
  spaceMemberAddSubmitEl = document.getElementById("space-member-add-submit");
  spaceMemberReauthFieldsEl = document.getElementById("space-member-reauth-fields");
  spaceMemberReauthPasswordEl = document.getElementById("space-member-reauth-password");
  spaceMemberReauthTotpEl = document.getElementById("space-member-reauth-totp");
  spaceRemoveOpenEl = document.getElementById("space-remove-open");

  spaceRemoveDialogEl = document.getElementById("space-remove-dialog");
  spaceRemoveConsequenceEl = document.getElementById("space-remove-consequence");
  spaceRemoveErrorEl = document.getElementById("space-remove-error");
  spaceRemoveConfirmInputEl = document.getElementById("space-remove-confirm-input");
  spaceRemoveReauthFieldsEl = document.getElementById("space-remove-reauth-fields");
  spaceRemoveReauthPasswordEl = document.getElementById("space-remove-reauth-password");
  spaceRemoveReauthTotpEl = document.getElementById("space-remove-reauth-totp");
  spaceRemoveSubmitEl = document.getElementById("space-remove-submit");
  spaceRemoveCancelEl = document.getElementById("space-remove-cancel");

  spaceAdminCloseEl.addEventListener("click", closeSpaceAdminDialog);

  spaceCreateSubmitEl.addEventListener("click", function () {
    var name = spaceCreateNameInputEl.value.trim();
    if (!name) { spaceCreateNameInputEl.focus(); return; }
    spaceAdminErrorEl.hidden = true;
    api("/spaces", { method: "POST", body: JSON.stringify({ name: name }) }).then(function () {
      spaceCreateNameInputEl.value = "";
      toast("Space angelegt · " + name);
      return loadOverview().then(renderSpaceList);
    }).catch(function (err) {
      if (err.message === "unauthenticated") return;
      spaceAdminError(err.message || "Anlegen fehlgeschlagen.");
    });
  });

  spaceMemberAddSubmitEl.addEventListener("click", function () {
    var space = selectedSpaceName;
    if (!space) return;
    var name = spaceMemberNameInputEl.value.trim();
    if (pendingMemberBody === null) {
      if (!name) { spaceMemberNameInputEl.focus(); return; }
      pendingMemberBody = { name: name, write: spaceMemberWriteSelectEl.value === "write" };
    }
    var body = Object.assign({}, pendingMemberBody);
    if (!spaceMemberReauthFieldsEl.hidden) {
      body.password = spaceMemberReauthPasswordEl.value;
      body.totp = spaceMemberReauthTotpEl.value;
    }
    api("/spaces/" + encodeURIComponent(space) + "/members", {
      method: "POST", body: JSON.stringify(body),
    }).then(function () {
      spaceMemberNameInputEl.value = "";
      spaceMemberReauthFieldsEl.hidden = true;
      pendingMemberBody = null;
      toast("Mitglied hinzugefügt · " + body.name);
      return selectSpace(space);
    }).catch(function (err) {
      if (err.code === "reauth_required") {
        spaceMemberReauthFieldsEl.hidden = false;
        spaceAdminError(err.message);
        spaceMemberReauthPasswordEl.focus();
        return;
      }
      pendingMemberBody = null;
      if (err.message === "unauthenticated") return;
      spaceAdminError(err.message || "Hinzufügen fehlgeschlagen.");
    });
  });

  spaceRemoveOpenEl.addEventListener("click", function () {
    if (selectedSpaceName) openRemoveSpaceDialog(selectedSpaceName);
  });
  spaceRemoveCancelEl.addEventListener("click", closeRemoveSpaceDialog);
  spaceRemoveSubmitEl.addEventListener("click", function () {
    var space = selectedSpaceName;
    if (!space) return;
    spaceRemoveErrorEl.hidden = true;
    var body = {
      confirm: spaceRemoveConfirmInputEl.value,
      password: spaceRemoveReauthPasswordEl.value,
      totp: spaceRemoveReauthTotpEl.value,
    };
    api("/spaces/" + encodeURIComponent(space), { method: "DELETE", body: JSON.stringify(body) })
      .then(function (result) {
        closeRemoveSpaceDialog();
        closeSpaceAdminDialog();
        toast("Space entfernt · " + result.archived + " Item(s) archiviert");
        return loadOverview();
      }).catch(function (err) {
        if (err.code === "reauth_required") {
          spaceRemoveReauthFieldsEl.hidden = false;
          spaceRemoveError(err.message);
          spaceRemoveReauthPasswordEl.focus();
          return;
        }
        if (err.message === "unauthenticated") return;
        spaceRemoveError(err.message || "Entfernen fehlgeschlagen.");
      });
  });
}
