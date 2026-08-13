"use strict";

// -- DOM-Helfer + Statuszeile (§4.5) ---------------------------------------------------------
// Bis Step 7b gab es für einen gelungenen Schreibvorgang gar keine Rückmeldung — der Nikinger
// klickte deshalb mehrfach auf "Speichern", jeder Klick zählte die Version hoch (Fund V10).
// Die zweite Hälfte dieses Fundes steckt in `updateVersionBand()` (editor.js): "Speichern" ist
// ohne tatsächliche Änderung deaktiviert.
//
// `el()` lebt hier statt in einem eigenen Modul, weil es zusammen mit `toast()` die einzigen
// Bausteine sind, die praktisch jedes andere Modul braucht (Step-7-Split, kein eigener
// utils.js im Plan-Dateiplan) — kein Import-Zyklus, da diese Datei selbst nichts importiert.

var toastEl;
var sessionExpiredCardEl;
var toastTimer = null;

export function el(tag, className, text) {
  var node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

export function showSessionExpiredCard() {
  sessionExpiredCardEl.hidden = false;
}

export function toast(message, kind) {
  toastEl.textContent = message;
  toastEl.className = "toast" + (kind ? " toast--" + kind : "");
  toastEl.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(function () { toastEl.hidden = true; }, kind === "error" ? 6000 : 2800);
}

export function init() {
  sessionExpiredCardEl = document.getElementById("session-expired-card");
  toastEl = document.getElementById("toast");
}
