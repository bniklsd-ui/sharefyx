"use strict";

// -- Realtime (P10.5, Block 10, Schritt 10.3 — LG-2, Lock P10.5-L) ---------------------------
//
// **Was der Server meldet:** die **Space-Namen**, die sich geändert haben, plus den
// Commit-Hash. Keine Inhalte — der Client holt sich die Daten über die normale API, die
// ihre Rechte prüft. Der Server ist dumm (Kernprinzip), und ein fremder Body im Ereignis
// wäre ein Datenleck an der Rechteprüfung vorbei.
//
// **Drei Folgen eines Ereignisses:**
//
// 1. `List.loadOverview()` — die Zähler im Baum und die Übersicht. Das setzt auch
//    `state.graphToken`, an dem die Karte hängt (P9-33): die Karte braucht keinen eigenen
//    Abruf.
// 2. `List.loadItems()` — **nur**, wenn der aktive Space betroffen ist. Im globalen Modus
//    („Alle Items") ist jede Änderung betroffen.
// 3. Das **offene Item** (P10.5-S) — siehe `refreshOpenItem()`.

import { state, isGlobalScope } from "./state.js";
import { api, reportUnexpectedError } from "./api.js";
import * as List from "./list.js";
import * as Editor from "./editor.js";

var source = null;

export function init() {
  // **Kein `EventSource` → der Poll-Rückfall trägt.** Kein Fehler, kein Abbruch: die
  // Oberfläche funktioniert ohne Realtime weiter (20-s-Poll, alle 120 s, solange der
  // Stream nicht offen ist).
  if (typeof EventSource === "undefined") return;
  try {
    source = new EventSource("/api/v1/events");
  } catch (err) {
    source = null;
    return;
  }
  source.addEventListener("changed", onChanged);
}

// Ist der Stream offen? Der Aufrufer (der Zähler-Poll) fragt das alle 20 s: solange der
// Stream offen ist, trägt er die Änderungen — der Poll wäre doppelt.
export function isOpen() {
  return !!source && source.readyState === EventSource.OPEN;
}

function onChanged(event) {
  var payload;
  try {
    payload = JSON.parse(event.data);
  } catch (err) {
    return;
  }
  var spaces = payload.spaces || [];
  List.loadOverview().catch(reportUnexpectedError);
  if (isGlobalScope() || (state.activeSpace && spaces.indexOf(state.activeSpace) !== -1)) {
    List.loadItems().catch(reportUnexpectedError);
  }
  refreshOpenItem();
}

// Das offene Item (P10.5-S): **nie ueberschreiben**.
//
// Sauberer Editor → der Serverstand wird geholt, und bei neuerer `version` neu geladen
// (Inhalt **und** Version zusammen — sonst zeigte der Editor eine Version, die es nicht
// gibt). Geaenderter Editor → ein Hinweisband erscheint, und **der Mensch** entscheidet;
// das Speichern laeuft weiter ueber die alte Version in den Konfliktdialog (Hard Rule 3).
function refreshOpenItem() {
  var id = state.selectedId;
  if (!id) return;
  api("/items/" + encodeURIComponent(id)).then(function (item) {
    var snap = state.editingSnapshot;
    if (snap && item.version <= snap.version) return;
    if (snap && Editor.isDirty()) {
      Editor.showChangedBanner(item);
      return;
    }
    Editor.reloadFromServer(item);
  }).catch(reportUnexpectedError);
}
