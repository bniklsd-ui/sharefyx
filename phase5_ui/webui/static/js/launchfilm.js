"use strict";

// Launch-Film v4.0.0 (P10.5 Block 17, Plan `docs/concepts/phase10_5_block17_film_app_plan.md`).
//
// Beim ersten Start in diesem Browser ein Startbild im Vollbild; der Klick auf „Film ansehen"
// spielt ab. Im Update-Log steht ein Knopf zum Wiedersehen.
//
// **Warum ein Startbild statt Autoplay (Entscheidung E2, Nikinger 2026-11-01):** ohne Nutzergeste
// sperren Browser den Ton und die Fullscreen-API — und der Klick auf „Anmelden" überlebt die
// Weiterleitung nach `/ui/` nicht. Der Klick hier ist die Geste: Ton **und** echtes Vollbild.
//
// **Das Video lädt nur beim Abspielen:** das `src` steht als `data-src` im Markup und wird erst
// im Klick gesetzt. Startbild und „Überspringen" fragen die 25,7 MB nie an.
//
// **„Schon gesehen" lebt nur im Browser** (`localStorage`, kein Server-Zustand — Auftrag). Der
// Wert ist die Film-Version: ein späterer Film bekommt einen neuen Wert und erscheint wieder.

var SEEN_KEY = "sfx:film:gesehen";
var FILM_VERSION = "4.0.0";

var rootEl, startEl, videoEl, closeEl;

// `null` heißt „kein Speicher" (privates Fenster: `localStorage` wirft SecurityError, Muster
// `dialogs.js`). Dann **kein** Startbild — sonst stünde es bei jedem Laden da.
function readSeen() {
  try { return window.localStorage.getItem(SEEN_KEY) || ""; } catch (e) { return null; }
}

function markSeen() {
  try { window.localStorage.setItem(SEEN_KEY, FILM_VERSION); } catch (e) { /* s. readSeen */ }
}

function isOpen() {
  return rootEl && !rootEl.hidden;
}

function showStart() {
  startEl.hidden = false;
  videoEl.hidden = true;
  closeEl.hidden = true;
  rootEl.hidden = false;
  document.getElementById("launch-film-play").focus();
}

// Läuft **im** Klick-Handler: nur dort erlauben Browser Vollbild und Ton.
function play() {
  startEl.hidden = true;
  videoEl.hidden = false;
  closeEl.hidden = false;
  rootEl.hidden = false;
  if (rootEl.requestFullscreen) {
    // Scheitert das Vollbild, bleibt die Überlagerung — sie deckt das Fenster ohnehin.
    rootEl.requestFullscreen().catch(function () {});
  }
  videoEl.src = videoEl.dataset.src;
  videoEl.play().catch(function () {});
  closeEl.focus();
}

function close() {
  if (!isOpen()) return;
  if (document.fullscreenElement === rootEl) document.exitFullscreen().catch(function () {});
  videoEl.pause();
  // `src` entfernen + `load()` gibt den Puffer frei; sonst lädt der Browser im Hintergrund weiter.
  videoEl.removeAttribute("src");
  videoEl.load();
  rootEl.hidden = true;
}

export function init() {
  rootEl = document.getElementById("launch-film");
  if (!rootEl) return;
  startEl = document.getElementById("launch-film-start");
  videoEl = document.getElementById("launch-film-video");
  closeEl = document.getElementById("launch-film-close");

  document.getElementById("launch-film-play").addEventListener("click", play);
  document.getElementById("launch-film-skip").addEventListener("click", close);
  closeEl.addEventListener("click", close);
  videoEl.addEventListener("ended", close);

  var replayEl = document.getElementById("update-log-film");
  if (replayEl) replayEl.addEventListener("click", play);

  // Capture-Phase: der globale Escape-Handler in `app.js` soll den Tastendruck nicht **auch**
  // bekommen (er schlösse sonst das Update-Log hinter dem Film). Kommt ESC hier an, schließt er
  // den Film **immer** — auch im Vollbild (`close()` verlässt es selbst). Chrome schluckt ESC im
  // Vollbild meist und verlässt nur das Vollbild; dann schließt der zweite Druck. Eine Ausnahme
  // „im Vollbild nichts tun" ließe den Film dort stehen, wo der Browser ESC doch durchreicht
  // (Mac, `app.js`-Kommentar P9 D1) — Probe P6, 2026-11-01.
  window.addEventListener("keydown", function (event) {
    if (event.key !== "Escape" || !isOpen()) return;
    event.stopPropagation();
    close();
  }, true);

  var seen = readSeen();
  if (seen !== null && seen !== FILM_VERSION) {
    // Sofort merken, nicht am Filmende: wer neu lädt, bekommt das Startbild nicht in Schleife.
    markSeen();
    showStart();
  }
}
