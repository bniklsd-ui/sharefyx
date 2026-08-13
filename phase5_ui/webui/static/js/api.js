"use strict";

import { toast, showSessionExpiredCard } from "./toasts.js";

var API_BASE = "/api/v1";

export function csrfToken() {
  return sessionStorage.getItem("sfx:csrf");
}

export function api(path, opts) {
  opts = opts || {};
  var method = opts.method || "GET";
  var headers = Object.assign({ "Content-Type": "application/json" }, opts.headers || {});
  if (method !== "GET" && method !== "HEAD") {
    var token = csrfToken();
    if (token) headers["X-CSRF-Token"] = token;
  }
  return fetch(API_BASE + path, Object.assign({}, opts, { method: method, headers: headers })).then(
    function (response) {
      if (response.status === 401) {
        // Step 7: keine sofortige Navigation mehr (anders als Step 6) — eine ganzflächige
        // Karte statt eines Redirects mitten im Tippen, §4.5. Der Entwurf liegt bereits in
        // sessionStorage (draftKeyFor()), geht durch das Stehenbleiben auf der Seite nicht
        // verloren; "Erneut anmelden" navigiert bewusst voll zu /ui/login (Plan-Entscheidung,
        // kein zweiter Login-Endpunkt) und der Bootstrap-Redirect zurück zu /ui/ landet wieder
        // hier, der Entwurf wird beim erneuten Öffnen des Items angeboten.
        showSessionExpiredCard();
        return Promise.reject(new Error("unauthenticated"));
      }
      return response.json().catch(function () { return null; }).then(function (body) {
        if (!response.ok) {
          var err = new Error((body && body.message) || response.statusText);
          err.code = body && body.error;
          err.detail = body && body.detail;
          return Promise.reject(err);
        }
        return body;
      });
    }
  );
}

// Für Aufrufe, die aus Event-Handlern lose angestoßen werden (Laden, Auswählen, Init) statt
// aus einer Nutzeraktion mit eigener Fehlerbehandlung: ohne dieses Netz bliebe die von `api()`s
// 401-Zweig zurückgegebene Promise unbehandelt — die "Sitzung abgelaufen"-Karte erscheint zwar
// trotzdem (das passiert synchron in `api()`, bevor verworfen wird), aber eine unbehandelte
// Ablehnung ist unnötiger Lärm in der Konsole und in strengeren Laufzeiten (Fund aus Step 7:
// Node bricht bei einer unbehandelten Promise-Ablehnung den Prozess ab, ein Browser gibt nur
// eine Konsolenwarnung — trotzdem sauber behandeln).
export function reportUnexpectedError(err) {
  if (err && err.message === "unauthenticated") return;
  console.error(err);
  toast(err && err.message ? err.message : "Unerwarteter Fehler.", "error");
}
