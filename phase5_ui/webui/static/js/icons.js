"use strict";

// Lucide-Icon-Helfer (Phase 8 Block C C2, Plan §4.C2).
//
// Verwendung:
//   import { iconSvg } from "./icons.js";
//   el("button", null, iconSvg("folder-input"))   // fuegt das <svg> als Text-Knoten ein
//   oder als HTML-String:
//     innerHTML = iconHtml("x");
//
// Vendoring + Sprite-Block liegen unter `<!-- ICONS:BEGIN --> / <!-- ICONS:END -->` in
// `app.html`; jede Symbol-ID ist `i-<name>` (siehe build_icon_sprite.py). CSS-Klasse `.icon`
// in app.css traegt die gemeinsamen Stroke-/Groessen-Defaults.
//
// CSP-Hinweis: kein Inline-Script, keine Template-Literals mit Funktionskoerpern -- nur ein
// einfacher String-Konstruktor. Reihenfolge der Skript-Loads ist egal, weil die Symbole in
// `app.html` selbst stehen und der Browser sie bei `<use>`-Aufloesung findet.

// Namen, die wir als Icon-HTML rendern wollen. Reihenfolge ist nicht relevant; die Liste ist
// nur zur Konsistenzpruefung gegen den Sprite-Block gedacht -- eine spaetere Erweiterung
// ergaenzt hier den Namen UND fuegt das passende SVG in `vendor/lucide/icons/` hinzu, dann
// `build_icon_sprite.py` laufen lassen. Fehlt der Name in `vendor/lucide/icons/`, faengt der
// Build-Script das mit "MISSING" ab.
var KNOWN = Object.freeze([
  "chevron-down",
  "chevron-right",
  "folder",
  "folder-input",
  "house",
  "image",
  "info",
  "link",
  "log-out",
  "plus",
  "quote",
  "refresh-cw",
  "search",
  "settings",
  "share-2",
  "triangle-alert",
  "waypoints",
  "x",
]);

export function iconSvg(name) {
  if (!KNOWN.includes(name)) {
    // Bewusst kein throw -- die Liste ist die "wir benutzen das"-Spur, nicht eine
    // Laufzeit-Police. Wer einen neuen Namen einsetzt, sieht im DevTools trotzdem,
    // dass er nicht in der Liste steht, und ergaenzt beides (Liste + vendored SVG).
    // eslint-disable-next-line no-console
    console.warn("[icons] unbekannter Icon-Name:", name, "(nicht in KNOWN-Liste)");
  }
  // Element-Konstruktion statt innerHTML: kein Parser-Hop, kein Risiko fuer unescapte
  // Eingaben, identisches Markup wie die in app.html direkt eingebetteten Stellen.
  var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("class", "icon");
  svg.setAttribute("aria-hidden", "true");
  var use = document.createElementNS("http://www.w3.org/2000/svg", "use");
  use.setAttribute("href", "#i-" + name);
  svg.appendChild(use);
  return svg;
}

export function iconHtml(name) {
  return '<svg class="icon" aria-hidden="true"><use href="#i-' + name + '"></use></svg>';
}