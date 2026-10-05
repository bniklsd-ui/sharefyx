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
import { registerPanel, openSpaceDetail, closeFrom, closeSettings } from "./settings.js";

var spaceAdminErrorEl;
var spaceAdminListEl;
var spaceCreateNameInputEl;
var spaceCreateSubmitEl;
var spaceAdminCloseEl;

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
var spaceDetailCloseEl;

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
    var row = el("button", "tree__folder settings-space-row", space.name + (space.name === state.ownSpace ? " (eigener Space)" : ""));
    row.type = "button";
    // P9-AG: die Zeile traegt denselben Auswahlzustand wie eine Baumzeile, wenn ihr Panel
    // offen ist (Stufe 3). `aria-current` ist hier die Anzeige, nicht der Zustand — der
    // Zustand ist `selectedSpaceName` darunter, genau wie in der Rail.
    if (selectedSpaceName === space.name) row.setAttribute("aria-current", "true");
    row.addEventListener("click", function () { selectSpace(space.name); });
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
    // Erst jetzt das Detail-Panel aufmachen (P9 Block settings §3 Schritt 2): vorher
    // stünde Stufe 3 für einen Frame offen, ohne Namen und ohne Mitgliederliste.
    openSpaceDetail();
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

// P9 Block settings: **der Reset** des Spaces-Panels. Das Öffnen macht `settings.js`, das
// Panel wird hier nicht mehr am DOM gesteuert. `registerPanel()` ist der einzige Weg von
// außen in dieses Modul — derselbe Ablauf, ob das Panel aus dem Menü, aus dem
// Update-Banner oder programmatisch geöffnet wird.
function prepareSpacesPanel() {
  spaceAdminErrorEl.hidden = true;
  selectedSpaceName = null;
  pendingMemberBody = null;
  spaceCreateNameInputEl.value = "";
  spaceMemberNameInputEl.value = "";
  spaceMemberReauthFieldsEl.hidden = true;
  spaceMemberReauthPasswordEl.value = "";
  spaceMemberReauthTotpEl.value = "";
  renderSpaceList();
}
registerPanel("spaces", prepareSpacesPanel);

// P9-AH: „Schließen" schließt dieses Panel und alles rechts davon, nicht die ganze Kette.
export function closeSpaceAdminDialog() {
  closeFrom("spaces");
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
  spaceAdminErrorEl = document.getElementById("space-admin-error");
  spaceAdminListEl = document.getElementById("space-admin-list");
  spaceCreateNameInputEl = document.getElementById("space-create-name-input");
  spaceCreateSubmitEl = document.getElementById("space-create-submit");
  spaceAdminCloseEl = document.getElementById("space-admin-close");

  // P9 Block settings: `#space-detail` ist als **Panel** in die Kette gewandert
  // (`#settings-space-detail`), deshalb existiert der alte Container nicht mehr. `init()`
  // liest die Kindelemente des Panels direkt -- es gibt keinen zweiten Zustand, den ein
  // ausgetauschtes Panel zurücksetzen müsste.
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
  spaceDetailCloseEl = document.getElementById("space-detail-close");

  spaceRemoveDialogEl = document.getElementById("space-remove-dialog");
  spaceRemoveConsequenceEl = document.getElementById("space-remove-consequence");
  spaceRemoveErrorEl = document.getElementById("space-remove-error");
  spaceRemoveConfirmInputEl = document.getElementById("space-remove-confirm-input");
  spaceRemoveReauthFieldsEl = document.getElementById("space-remove-reauth-fields");
  spaceRemoveReauthPasswordEl = document.getElementById("space-remove-reauth-password");
  spaceRemoveReauthTotpEl = document.getElementById("space-remove-reauth-totp");
  spaceRemoveSubmitEl = document.getElementById("space-remove-submit");
  spaceRemoveCancelEl = document.getElementById("space-remove-cancel");

  // P9-AH: „Schließen" schließt sein Panel und alles rechts davon. Stufe 3 (Detail) hat
  // seinen eigenen, Stufe 2 (Spaces) ebenfalls — deshalb zwei Aufrufe mit demselben Muster
  // und nicht einer für die ganze Kette.
  spaceAdminCloseEl.addEventListener("click", closeSpaceAdminDialog);
  spaceDetailCloseEl.addEventListener("click", function () { closeFrom("space-detail"); });

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
        // Die ganze Kette, nicht nur Stufe 2: der eben entfernte Space steht als Zeile in der
        // Liste, und die Liste wird hier **nicht** neu gerendert (`loadOverview()` lädt nur
        // die Zähler). Vor dem Umbau war das unmerklich, weil das Overlay mit verschwand --
        // jetzt bliebe eine Zeile stehen, deren Space es nicht mehr gibt. Ein destruktiver
        // Vorgang, der seinen Kontext verlässt, darf das Fenster schließen.
        closeSettings();
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
