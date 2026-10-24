"use strict";

// Update-Banner + Einstellungsabschnitt „Update-Log" (Plan §1.8, §4 Step 3, P6 Step 3).
// Step 7: als ES-Modul umgezogen (vorher `webui/static/js/updates.js` als eigenständiges
// globales Skript, `window.SharefyxUpdates`, MUSS-vor-app.js-Ladereihenfolge) — das Modulsystem
// löst genau das Problem, das die alte Ladereihenfolge-Regel umging: `markdownToHtml` kommt
// jetzt per echtem `import`, kein globaler Name mehr, der zufällig schon existieren muss.

import { api } from "./api.js";
import { markdownToHtml } from "./markdown.js";
import { registerPanel, closeFrom } from "./settings.js";

function markdownList(lines) {
  return lines.map(function (line) { return "- " + line; }).join("\n");
}

export function init() {
  var bannerEl = document.getElementById("update-banner");
  var bannerBodyEl = document.getElementById("update-banner-body");
  var bannerDismissEl = document.getElementById("update-banner-dismiss");
  var bannerLogEl = document.getElementById("update-banner-log");
  // P9 Block settings: Stufe 2 der Fensterkette, kein eigenes Overlay mehr. Der Container
  // heißt weiter `#update-log-list` (unveränderte ID, die Renders hängen daran).
  var logListEl = document.getElementById("update-log-list");
  var logCloseEl = document.getElementById("update-log-close");

  // Markup fehlt auf Seiten ohne die Shell (Login/Einladung/Enrollment, `pages.py`) — dort
  // läuft `init()` nie, wie bei jedem anderen Shell-Feature auch.
  if (!bannerEl || !logListEl) return;

  var entries = [];

  function renderLog() {
    logListEl.innerHTML = "";
    entries.forEach(function (entry) {
      var heading = document.createElement("h3");
      heading.className = "update-log__date";
      heading.textContent = entry.date;
      logListEl.appendChild(heading);
      var body = document.createElement("div");
      body.innerHTML = markdownToHtml(markdownList(entry.lines));
      logListEl.appendChild(body);
    });
    if (entries.length === 0) {
      logListEl.appendChild(document.createElement("p")).textContent = "Noch keine Einträge.";
    }
  }

  // `--banner-h` (app.css) ist nur ein Startwert -- der Bannertext ist so lang wie der jeweils
  // neueste UPDATE_LOG.md-Eintrag, `offsetHeight` misst die WIRKLICHE, ggf. mehrzeilige Höhe,
  // nachdem der Text steht und `hidden` weg ist (erzwingt einen synchronen Layout-Flush, bevor
  // der Browser das nächste Frame malt -- kein sichtbares Springen).
  function syncBannerHeight() {
    document.documentElement.style.setProperty("--banner-h", bannerEl.offsetHeight + "px");
  }

  function showBanner(latest) {
    // P10.5 Block 7.4, Posten 3 (Sichtung des Nikingers vom 2026-10-24): der Banner zeigte
    // ALLE Zeilen des neuesten Eintrags und war dadurch bis zu ~140 px hoch — er verdeckte
    // oben eine halbe Bildschirmhöhe und schob jede angemeldete Ansicht darunter. Jetzt
    // trägt er nur die ERSTE Zeile als Schlagzeile; der ganze Eintrag steht im Update-Log
    // (Einstellungen), das der Knopf „Alle Änderungen" direkt öffnet.
    //
    // Die Zeile kommt als Markdown (der Log-Text darf `**fett**` tragen), aber ohne Liste:
    // eine Liste würde wieder Hoehe in die Zeile bringen, die der Banner nicht haben darf.
    var zeilen = latest.lines || [];
    bannerBodyEl.innerHTML = markdownToHtml(zeilen.length ? zeilen[0] : "");
    bannerEl.hidden = false;
    document.body.classList.add("has-update-banner");
    syncBannerHeight();
  }

  function hideBanner() {
    bannerEl.hidden = true;
    document.body.classList.remove("has-update-banner");
  }

  // Ein Fenster-Resize kann die Zeilenzahl des Banners ändern (schmaleres Fenster -> mehr
  // Zeilen) -- ohne das würde `.shell` entweder zu wenig Platz lassen (Text überlappt) oder zu
  // viel (unnötiger Leerraum), solange das Banner sichtbar bleibt.
  window.addEventListener("resize", function () {
    if (!bannerEl.hidden) syncBannerHeight();
  });

  bannerDismissEl.addEventListener("click", function () {
    hideBanner();
    // Fire-and-forget (P6-X): ein gescheiterter `seen`-Aufruf zeigt das Banner beim nächsten
    // Laden erneut — lästig, aber nie ein Grund, dem Menschen hier eine Fehlermeldung
    // hinzuwerfen, die er nicht beeinflussen kann.
    api("/updates/seen", { method: "POST" }).catch(function () {});
  });

  // P10.5 Block 7.4, Posten 3: „Alle Änderungen" öffnet den vollständigen Update-Log in den
  // Einstellungen (dieselbe Fensterkette, dasselbe `renderLog` wie der Menüpunkt) — der
  // Banner zeigt nur noch die Schlagzeile, der Rest des Eintrags verschwindet sonst.
  // Das Banner bleibt dabei stehen: „Verstanden" bleibt der einzige Weg, es wegzuklicken.
  if (bannerLogEl) {
    bannerLogEl.addEventListener("click", function () {
      // Der Weg zum Update-Log: ein **Ereignis**, kein `openPanel` -- der Wächter
      // `test_only_one_module_opens_a_panel` (Phase 9) hält fest, dass es genau einen Öffner
      // für die Fensterkette gibt (`settings.js`). Das Banner fragt, die Kette entscheidet.
      window.dispatchEvent(new CustomEvent("sfx:open-panel", { detail: { name: "updates" } }));
    });
  }

  // [VERIFY] V186 (2026-10-05, beantwortet): das Update-Banner öffnet das Log **nicht** — es
  // trägt nur „Verstanden" (`#update-banner-dismiss`), keinen zweiten Knopf. Der einzige Weg
  // ins Log ist der Menüpunkt „Update-Log" in den Einstellungen. Plan §3 Schritt 1 nannte
  // „Alle Updates ansehen" — das war eine Annahme über ein Bedienelement, das es nicht gibt.
  //
  // **[2026-10-24, P10.5 Block 7.4, Posten 3 — datierte Korrektur zu V186:]** das Banner
  // trägt **jetzt** einen zweiten Knopf, „Alle Änderungen" (`#update-banner-log`). Grund: der
  // Banner zeigt nur noch die **erste Zeile** des neuesten Eintrags (vorher alle Zeilen, bis zu
  // ~140 px Höhe) — ohne diesen Knopf wäre der Rest des Eintrags unerreichbar. Der Knopf
  // öffnet **denselben** Update-Log in den Einstellungen (das Ereignis `sfx:open-panel`, das
  // `settings.js` entgegennimmt); am Update-Log selbst ändert sich nichts.
  //
  // Das Rendern ist der `prepare`-Eintrag dieses Panels (P9 Block settings): das Öffnen macht
  // `settings.js`, und genau ein Ort soll entscheiden, wann ein Panel aufgeht.
  registerPanel("updates", renderLog);
  logCloseEl.addEventListener("click", function () { closeFrom("updates"); });

  api("/updates").then(function (body) {
    entries = body.entries || [];
    if (entries.length > 0 && body.latest_id && body.latest_id !== body.seen_update_id) {
      showBanner(entries[0]);
    }
  }).catch(function () {
    // Kein Toast: ein kaputtes/unerreichbares Update-Log ist kein Fehler, den ein Mensch hier
    // beheben kann (`webui/updates.py :: load_update_log()` ist serverseitig ohnehin fail-soft).
  });
}
