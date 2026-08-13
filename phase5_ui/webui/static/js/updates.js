"use strict";

// Update-Banner + Einstellungsabschnitt „Update-Log" (Plan §1.8, §4 Step 3, P6 Step 3).
// Step 7: als ES-Modul umgezogen (vorher `webui/static/js/updates.js` als eigenständiges
// globales Skript, `window.SharefyxUpdates`, MUSS-vor-app.js-Ladereihenfolge) — das Modulsystem
// löst genau das Problem, das die alte Ladereihenfolge-Regel umging: `markdownToHtml` kommt
// jetzt per echtem `import`, kein globaler Name mehr, der zufällig schon existieren muss.

import { api } from "./api.js";
import { markdownToHtml } from "./markdown.js";

function markdownList(lines) {
  return lines.map(function (line) { return "- " + line; }).join("\n");
}

export function init() {
  var bannerEl = document.getElementById("update-banner");
  var bannerBodyEl = document.getElementById("update-banner-body");
  var bannerDismissEl = document.getElementById("update-banner-dismiss");
  var logDialogEl = document.getElementById("update-log-dialog");
  var logListEl = document.getElementById("update-log-list");
  var logCloseEl = document.getElementById("update-log-close");
  var showUpdatesEl = document.getElementById("account-show-updates");

  // Markup fehlt auf Seiten ohne die Shell (Login/Einladung/Enrollment, `pages.py`) — dort
  // läuft `init()` nie, wie bei jedem anderen Shell-Feature auch.
  if (!bannerEl || !logDialogEl) return;

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
    bannerBodyEl.innerHTML = markdownToHtml(markdownList(latest.lines));
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

  if (showUpdatesEl) {
    showUpdatesEl.addEventListener("click", function () {
      renderLog();
      logDialogEl.hidden = false;
    });
  }
  logCloseEl.addEventListener("click", function () { logDialogEl.hidden = true; });

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
