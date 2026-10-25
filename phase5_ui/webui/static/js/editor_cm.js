"use strict";

// -- Der nachgeladene Editor (P10.5, Block 11, Schritt 11.2 — ED-1) -------------------------
//
// **Warum nachgeladen und nicht mitgeliefert.** Der Editor (CodeMirror 5) wiegt **71.280 B
// gzip** — das ist mehr als ein Drittel des Erstaufrufs. Der Erstaufruf muss **ohne** den
// Editor auskommen (Übersicht, Liste, Lesesicht), also lädt dieses Modul die Dateien
// **erst, wenn der Editor wirklich gebraucht wird**. Der Budget-Wächter zählt die Dateien
// deshalb unter „Editor nachgeladen" (≤ 80 KB) und nicht unter dem Erstaufruf.
//
// **Die Reihenfolge ist nicht beliebig.** `codemirror.min.js` zuerst (der Kern), dann die
// drei Modus-Dateien: `meta.min.js` und `xml.min.js` sind die Abhängigkeiten des
// Markdown-Modus, `markdown.min.js` kommt zuletzt. **Gemessen am 2026-10-24:** die
// gebaute `markdown.min.js` ist ein UMD-Wrapper, dessen Browser-Zweig nur `t(CodeMirror)`
// aufruft — die `require(...)`-Zweige werden im Browser *nicht* aufgelöst. Deshalb werden
// alle vier Skripte geladen, nicht nur zwei (Plan §Block 11, Schritt 11.1).
//
// **Fehlerpfad: `null`, nicht ein Absturz.** Kann der Editor nicht geladen werden (Netz,
// CSP, fehlende Datei), bleibt die **Textarea** stehen — das ist der Rohmodus (ED-5) und
// ein vollwertiger Notausgang. Der Aufrufer fragt `ensureCodeMirror()` und bekommt `null`.

const VENDOR_BASE = "/ui/static/vendor/codemirror/";
const VENDOR_CSS = "codemirror.min.css";
//: **Fünf Dateien, nicht drei** — siehe den Kopfkommentar und `THIRD_PARTY_LICENSES.md`.
const VENDOR_SCRIPTS = [
  "codemirror.min.js",
  "meta.min.js",
  "xml.min.js",
  "markdown.min.js",
];

//: Das **eine** Promise des Ladevorgangs: der Editor wird höchstens einmal geladen, egal
//: wie oft `ensureCodeMirror()` gerufen wird (die Antwort wird gecacht, nicht der Zustand).
var ladePromise = null;

/**
 * Lädt den Editor (CSS und Skripte) und liefert das `CodeMirror`-Objekt — oder `null`,
 * wenn er nicht ladbar ist. **Das Promise wird gecacht**: ein zweiter Aufruf wartet auf
 * dasselbe Laden.
 */
export function ensureCodeMirror() {
  if (!ladePromise) ladePromise = lade();
  return ladePromise;
}

/** Ist der Editor schon da? (nach `ensureCodeMirror()` oder durch ein anderes Modul) */
export function isLoaded() {
  return typeof window.CodeMirror !== "undefined" && window.CodeMirror !== null;
}

async function lade() {
  try {
    await ladeCss(VENDOR_BASE + VENDOR_CSS);
    for (var i = 0; i < VENDOR_SCRIPTS.length; i++) {
      await ladeScript(VENDOR_BASE + VENDOR_SCRIPTS[i]);
    }
    return isLoaded() ? window.CodeMirror : null;
  } catch (err) {
    // **Kein Wurf nach oben.** Der Editor ist ein Komfort, kein Pfad: wer ihn nicht
    // bekommt, arbeitet in der Textarea weiter (Rohmodus, ED-5).
    console.warn("CodeMirror nicht ladbar — der Editor bleibt Textarea:", err);
    return null;
  }
}

function ladeCss(pfad) {
  return new Promise(function (resolve, reject) {
    // Ein vorhandenes `<link>` (zweiter Aufruf) gilt als geladen.
    if (document.querySelector('link[data-cm-css="' + pfad + '"]')) {
      resolve();
      return;
    }
    var link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = pfad;
    link.setAttribute("data-cm-css", pfad);
    link.onload = function () { resolve(); };
    link.onerror = function () { reject(new Error("CSS nicht ladbar: " + pfad)); };
    // **Vor** `app.css`: bei gleicher Spezifitaet gewinnt die spaetere Datei — das vendorte
    // CSS darf unsere Regeln nicht uebertrumpfen (Befund der Sichtung, 2026-10-25).
    var app = document.querySelector('link[rel="stylesheet"][href$="app.css"]');
    if (app && app.parentNode) app.parentNode.insertBefore(link, app);
    else document.head.appendChild(link);
  });
}

function ladeScript(pfad) {
  return new Promise(function (resolve, reject) {
    var script = document.createElement("script");
    script.src = pfad;
    script.async = false; // **Reihenfolge ist Reihenfolge** (der Modus braucht den Kern)
    script.onload = function () { resolve(); };
    script.onerror = function () { reject(new Error("Skript nicht ladbar: " + pfad)); };
    document.head.appendChild(script);
  });
}
