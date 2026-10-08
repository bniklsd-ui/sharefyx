"use strict";

// -- Einstellungen als Fensterkette (P9 Block settings, Plan §3 Schritt 2) -----------------------
// Bis 2026-10-05 waren es drei eigenständige Overlays (`#account-dialog`, `#space-admin-dialog`,
// `#update-log-dialog`), die sich gegenseitig **ersetzten**: „Spaces verwalten" schloss das
// Konto-Fenster und öffnete ein neues. Der Nikinger wollte stattdessen eine Kette — ein Menü,
// daneben das gewählte Unterfenster, daneben (bei Spaces) das Detail; das Menü bleibt sichtbar,
// damit man sieht, wozu das Fenster gehört.
//
// **Warum ein eigenes Modul und keine drei aufgerissene Overlay-Aufrufe:** Layout, Auswahl-
// Zustand und ESC-Reihenfolge sind jetzt *eine* Sache, nicht drei. Sie zu verteilen hieße, die
// Kette an drei Stellen zu duplizieren — die "dritte Variante", die P9 am 2026-10-01 bei
// `.account-nav` erst entfernt hat. Hier ist sie einmal.
//
// **Drei Zusicherungen, die dieses Modul trägt:**
//
// 1. *Stufe 2 wird ersetzt, Stufe 3 geschlossen* (P9-AG). `openPanel()` setzt genau eine
//    Stufe-2; die Detailstufe wird dabei mitgenommen, sonst hinge sie links neben einem
//    Unterfenster, zu dem sie nicht mehr gehört.
// 2. *Schließen von rechts nach links* (P9-AH). `closeFrom(name)` schließt das genannte Panel
//    **und alles rechts davon**; `closeRightmost()` (ESC) nimmt das rechteste sichtbare. Das
//    Menü ist die linke Stufe — ein ESC darauf schließt die ganze Kette, weil rechts nichts
//    mehr kommt.
// 3. *Der Auswahlzustand folgt dem Fenster* (P9-AG). Genau der Menüknopf des offenen
//    Unterfensters trägt `aria-current="true"` — dieselbe Markierung, die `.tree__folder` in
//    der Rail trägt, und dieselbe CSS-Regel (`app.css`). Kein zweiter Zustand, kein
//    eigener Füll-Farbwert.
//
// **Wer seinen Knopf verdrahtet.** Es gibt genau **einen** Öffner: `openPanel(name)`. Damit
// das nicht zur zweiten Wahrheit wird, liefert jeder Eigentümer nur seinen Zustands-Reset
// dazu (`registerPanel`) — es gibt keinen zweiten `addEventListener` auf denselben Knopf.
// Zwei Öffner auf einem Knopf wären genau die doppelte Zustandshalterung, die der Block
// abbaut; das ist beim Umbau einmal passiert (der Menüpunkt öffnete und schloss gleichzeitig,
// weil `app.js` und dieses Modul denselben Knopf hören wollten).
//
// **Schmal-Modus** (P9-AI): unterhalb der Summe der Panelbreiten bleibt nur das **rechteste**
// Panel sichtbar, mit „Zurück" links oben. Die Panels sind dann keine Nachbarn mehr, sondern
// eine Seitennavigation — dieselbe Regel wie im P8.6-Editor (≤1024 px: Liste **oder** Editor).
// Kein Zusatz, den die Kette „auch kann": ohne ihn gäbe es auf dem Arbeitslaptop kein
// sichtbares Menü, weil rechts kein Platz mehr ist.

var overlayEl;
// Reihenfolge = Stufen. `menu` steht immer links und ist der Anker: ein Klick auf einen
// anderen Menüpunkt ersetzt Stufe 2, nie die Kette selbst.
var STAGES = ["menu", "password", "spaces", "space-detail", "updates"];

var panelEls = {};
var menuItemEls = {};
var prepareBy = {};
var openStage = null;        // null = nur Stufe 1 sichtbar; sonst der Name des Stufe-2-Panels
var openDetail = false;      // Stufe 3 sichtbar?

export function registerPanel(name, prepare) {
  prepareBy[name] = prepare;
}

function show(visible) {
  Object.keys(panelEls).forEach(function (name) {
    var node = panelEls[name];
    if (name === "menu") { node.hidden = !visible; return; }
    if (!visible) { node.hidden = true; return; }
    if (name === "space-detail") { node.hidden = !openDetail; return; }
    node.hidden = name !== openStage;
  });
  syncSelection();
}

// Der Menüpunkt, dessen data-panel zum offenen Panel gehört, trägt `aria-current="true"`,
// alle anderen bekommen es explizit auf "false". Das ist genau die Form, die
// `.tree__folder` in der Rail benutzt (`tree.js :: renderFolders()`) — der Selektor
// `[aria-current="true"]` im Stylesheet greift also ohne neue Regel. Ein *nicht gesetztes*
// Attribut wäre ebenso gültig, aber "false" macht den Zustand im DOM abfragbar und die
// Frage "welcher Knopf ist aktiv" eindeutig.
function syncSelection() {
  Object.keys(menuItemEls).forEach(function (panel) {
    menuItemEls[panel].setAttribute("aria-current", openStage === panel ? "true" : "false");
  });
}

function hideChain() {
  openStage = null;
  openDetail = false;
  show(false);
  overlayEl.hidden = true;
}

// ESC und „Schließen" eines Panels: dieses Panel und alles **rechts** davon (P9-AH). Der
// Menüknopf schließt die ganze Kette, weil rechts von ihm nichts liegen kann.
//
// **Die rechte Kante schneidet die Kette ab, sie leert sie nicht** — drei Fälle, und der
// dritte war ein Fehler dieses Moduls: `space-detail` ist die *rechteste* Stufe, rechts von
// ihr liegt nichts, also schließt ihr „Schließen"/„Zurück" **nur sie** und lässt Stufe 2
// stehen. Die erste Fassung setzte für jeden Namen `openStage = null` und räumte damit beim
// Schließen des Details auch die Spaces-Liste weg — im breiten Modus sichtbar (Panel links
// verschwindet mit), im Schmal-Modus als Fehler, weil es keine Stufe 2 mehr gab, zu der man
// zurückkehren könnte.
export function closeFrom(name) {
  if (name === "menu") { hideChain(); return; }
  if (name === "space-detail") { openDetail = false; show(true); return; }
  openStage = null;
  openDetail = false;
  show(true);
}

export function closeRightmost() {
  if (openDetail) openDetail = false;
  else if (openStage) openStage = null;
  else { hideChain(); return; }
  show(true);
}

export function openPanel(name) {
  if (prepareBy[name]) prepareBy[name]();
  openStage = name;
  // Stufe 3 gehört zu „Spaces verwalten" — ein anderer Menüpunkt nimmt sie mit (P9-AG).
  if (name !== "spaces") openDetail = false;
  show(true);
  overlayEl.hidden = false;
}

// Stufe 3. `spaces.js :: selectSpace()` ruft das **nach** dem eigenen `api()`-Aufruf, damit
// das Panel nicht mit leerem Inhalt aufblitzt; der Klick auf eine Space-Zeile ist der einzige
// Weg hierher, „Zurück" der einzige Weg zurück (P9-AH: es schließt Stufe 3 und alles rechts
// davon — links bleibt die Kette stehen).
export function openSpaceDetail() {
  openStage = "spaces";
  openDetail = true;
  show(true);
  overlayEl.hidden = false;
}

// Die Kette ohne Stufe 2: das Menü allein. Der Rail-Knopf „Einstellungen" ruft das auf.
export function openSettings() {
  openStage = null;
  openDetail = false;
  show(true);
  overlayEl.hidden = false;
}

// Die ganze Kette schließen — für Fälle, in denen der Inhalt der Stufe 2 nicht mehr sinnvoll
// ist (ein Space wurde entfernt; die Liste wird nicht neu gerendert). `closeFrom("menu")`
// wäre dasselbe, aber der eigene Name sagt am Aufrufer, was gemeint ist.
export function closeSettings() {
  hideChain();
}

export function init() {
  overlayEl = document.getElementById("settings-overlay");
  STAGES.forEach(function (name) {
    panelEls[name] = document.getElementById("settings-" + name);
  });
  // **Jede** Stufe außer dem Menü bekommt ihren „Zurück"-Knopf verdrahtet — auch Stufe 3.
  // Die erste Fassung nahm `space-detail` hier aus (mit der Begründung, die rechteste Stufe
  // werde ohnehin von rechts geschlossen) und traf damit genau den Fall, für den der Knopf
  // erfunden ist: im Schmal-Modus ist Stufe 3 das **einzige** sichtbare Panel, und „Zurück"
  // ist dort der einzige Weg zur Stufe 2. Die Browser-Probe S8 hat ihn als toten Knopf
  // gemeldet, nicht als fehlenden.
  STAGES.forEach(function (name) {
    if (name === "menu") return;
    var back = panelEls[name].querySelector(".settings-back");
    if (back) back.addEventListener("click", function () { closeFrom(name); });
  });

  // Ein Klick auf einen Menüpunkt öffnet sein Panel; derselbe Punkt schließt es wieder.
  // Das Toggle ist eine Zutat, kein Lock — aber ohne ihn lässt sich ein offenes Fenster nur
  // über ESC oder „Schließen" loswerden, und beides ist der Umweg.
  STAGES.forEach(function (name) {
    if (name === "menu" || name === "space-detail") return;
    var button = overlayEl.querySelector('[data-panel="' + name + '"]');
    if (!button) return;
    menuItemEls[name] = button;
    button.addEventListener("click", function () {
      if (openStage === name) closeFrom(name);
      else openPanel(name);
    });
  });

  // P9-BN: „Schließen" im Menü schließt die ganze Kette, wie ESC auf der letzten Stufe.
  document.getElementById("settings-menu-close").addEventListener("click", closeSettings);

  overlayEl.addEventListener("click", function (event) {
    // Hintergrund-Klick schließt die ganze Kette — dieselbe Form wie bei jedem anderen
    // Overlay hier (P9-AH). Der Trick ist `closest(".settings-chain")`: ein Klick auf ein
    // Panel trifft dessen Vorfahren, ein Klick auf den abgedunkelten Hintergrund nicht.
    if (event.target.closest && event.target.closest(".settings-chain")) return;
    hideChain();
  });
}
