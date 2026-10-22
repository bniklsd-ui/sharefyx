// P10.5, Block 4 (2026-10-22), Z3/Z4 — der Ladezustand.
//
// Auf der langsamen Strecke wartet der Mensch mehrere Sekunden, ohne zu sehen, ob gearbeitet
// wird (M1: `/overview` 4,8 s). Dieser Baustein sagt „es läuft noch" — aber **erst ab 200 ms**.
// Darunter gibt es kein Flackern: ein schneller Abruf soll den Bildschirm nicht überhaupt
// anflackern. Die 200 ms sind die Grenze aus dem Plan (Block 4, Schritt 4.4), dieselbe Zahl
// wie in der Abnahme P10.5-17 („Ladezustand genau ab 200 ms").
//
// **Der Platzhalter trägt nie eine Versionsangabe** (P10.5-S). Das ist hier nicht nur
// Konvention, sondern by construction: dieses Modul schreibt **keinen Text** in die
// Oberfläche — es setzt eine CSS-Klasse, und das Gerüst entsteht rein aus CSS. Damit kann
// hier weder eine Versionsnummer noch ein Zähler erscheinen, und nichts davon kann je in
// einen Schreibvorgang gelangen.
//
// **Warum eine eigene Datei:** vier Aufrufstellen (Übersicht, Liste, Item-Öffnen, Karte) brauchen
// dieselbe Logik. Eine Datei statt vier Kopien — dieselbe Begründung wie bei `state.js` und
// `api.js` in diesem Projekt.

// Setzt die Klasse `is-loading` auf `el`, solange `promise` nach `delayMs` noch offen ist.
// Gibt das Promise **unverändert** zurück: der Aufrufer hängt seine eigenen `.then()` an
// dasselbe Promise, und die Reihenfolge bleibt: der Abruf löst auf, die Klasse fällt, der
// Inhalt wird gezeichnet — alles vor dem nächsten Bild.
export function withLoading(el, promise, { delayMs = 200 } = {}) {
  if (!el || !promise || typeof promise.then !== "function") return promise;
  var finished = false;
  var timer = null;

  function done() {
    finished = true;
    if (timer !== null) {
      window.clearTimeout(timer);
      timer = null;
    }
    el.classList.remove("is-loading");
  }

  // Zwei Zweige, **ein** Handler: ein Fehler muss den Ladezustand genauso beenden wie ein
  // Erfolg — sonst bliebe das Gerüst bei einem 500er für immer stehen. Der abgeleitete Promise
  // löst in beiden Fällen auf (die Ablehnung ist damit behandelt), das ursprüngliche Promise
  // bleibt unangetastet und wird vom Aufrufer quittiert.
  promise.then(done, done);

  timer = window.setTimeout(function () {
    timer = null;
    if (!finished) el.classList.add("is-loading");
  }, delayMs);

  return promise;
}
