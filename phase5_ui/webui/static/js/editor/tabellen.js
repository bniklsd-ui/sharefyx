"use strict";

// -- Tabellen-Widget im Editor (Editor 4.1, Schritt S2 — Hotfix v4.0.2) ---------------------
//
// Plan `docs/concepts/phase10_5_editor_4_1_plan.md` §5 S2, Verträge §4.2 (V1–V4), Prototyp
// Anhang A4. **Nachgeladen** (Budget-Regel §4.4): `editor.js` holt diese Datei per `import()`,
// nachdem CodeMirror steht — nie statisch. Scheitert der Import, bleibt der Editor, was er
// vorher war (Tabellen als Rohtext).
//
// **Das Widget ist eine Sicht, kein Schreibweg.** Eine GFM-Tabelle, in der weder Cursor noch
// ein Auswahlende steht, wird per `markText({replacedWith})` durch **dieselbe** Tabelle ersetzt,
// die die Lesesicht zeigt (`markdownToHtml()` auf genau die Quellzeilen — derselbe Renderer,
// derselbe Sanitizer). Der Text im Dokument bleibt Byte für Byte, wie er war: Widgets setzen,
// räumen und neu bauen ändert nichts am Text und nichts an der Historie (`addToHistory` aus).
// Bearbeitet wird **immer** der Rohtext: ein Klick in eine Zelle oder ein Pfeil in die Tabelle
// räumt das Widget ab und setzt den Cursor in die Quelle.

import { markdownToHtml } from "../markdown.js";

//: = `TABLE_SEPARATOR_RE` in `markdown.js` (dort nicht exportiert; S3 ersetzt beides durch
//: `blockRanges()` der Renderer-Fassade).
var TRENNER = /^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?\s*$/;
var BLOCK_AUF = /^:::[ \t]*\{([^}]*)\}[ \t]*$/;
var BLOCK_ZU = /^:::[ \t]*$/;

/**
 * **Interim-Scanner** (bis S3 die Renderer-Fassade `blockRanges()` liefert): die Zeilenbereiche
 * der **obersten** Tabellen, in der Schleifenreihenfolge von `_markdownZeilen` (`markdown.js`):
 * `:::`-Block → Zaun ```` ``` ```` → Tabelle → Zitat. Gleiche Regeln, gleiche Fehler —
 * Widget und Lesesicht sollen dieselbe Tabelle sehen:
 *
 * - `:::`-Block (bekannt, unbekannt oder ohne Ende): verschluckt alles bis `:::`/Dateiende —
 *   Tabellen darin bleiben im Editor **Rohtext** (bewusst; die Ausrichtung gehört S4).
 * - Zaun nur ```` ``` ```` am Zeilenanfang, ohne Ende bis Dateiende; `~~~` ist für den Renderer
 *   **kein** Zaun — eine Tabelle darin rendert er, also auch das Widget.
 * - Tabelle: Zeile mit `|`, nächste Zeile Trenner; Körper, solange eine Zeile `|` trägt und
 *   nicht leer ist (zwei Tabellen ohne Leerzeile = **eine**).
 * - Zitatzeilen (`>`) werden verschluckt: eine Tabelle im Zitat bleibt Rohtext (wie die Lesesicht).
 *
 * @param {string[]} zeilen
 * @returns {{typ: string, von: number, bis: number}[]}  Zeilen inklusive
 */
export function blockRanges(zeilen) {
  var out = [];
  var n = zeilen.length;
  var i = 0;
  while (i < n) {
    var z = zeilen[i];
    if (BLOCK_AUF.test(z)) {
      i++;
      while (i < n) {
        if (BLOCK_ZU.test(zeilen[i])) { i++; break; }
        i++;
      }
      continue;
    }
    if (/^```/.test(z)) {
      i++;
      while (i < n && !/^```/.test(zeilen[i])) i++;
      i++;
      continue;
    }
    if (z.indexOf("|") !== -1 && i + 1 < n && TRENNER.test(zeilen[i + 1])) {
      var von = i;
      i += 2;
      while (i < n && zeilen[i].indexOf("|") !== -1 && zeilen[i].trim() !== "") i++;
      out.push({ typ: "table", von: von, bis: i - 1 });
      continue;
    }
    if (/^>/.test(z)) {
      i++;
      while (i < n && /^>/.test(zeilen[i])) i++;
      continue;
    }
    i++;
  }
  return out;
}

/**
 * Die Spalte (`ch`), an der jede **gerenderte** Zelle einer Quellzeile beginnt — nach der
 * Teilung des heutigen Renderers (`splitTableRow`: trimmen, äußere `|` ab, an **jedem** `|`
 * teilen). Damit trifft die k-te Zelle im Widget die k-te Zelle der Quelle, auch wo der
 * Renderer falsch teilt (`\|`, `|` im Codespan — Befund F3, heilt S3). Ziel ist das erste
 * Zeichen nach dem Leerraum der Zelle; eine leere Zelle bekommt die Stelle nach einem Leerzeichen.
 *
 * @param {string} zeile
 * @returns {number[]}
 */
export function zellAnfaenge(zeile) {
  var start = zeile.length - zeile.replace(/^\s+/, "").length;
  var ende = zeile.replace(/\s+$/, "").length;
  if (start < ende && zeile.charAt(start) === "|") start++;
  if (ende > start && zeile.charAt(ende - 1) === "|") ende--;
  var out = [];
  var pos = start;
  zeile.slice(start, ende).split("|").forEach(function (teil) {
    var vorne = teil.length - teil.replace(/^\s+/, "").length;
    out.push(pos + (vorne < teil.length ? vorne : Math.min(1, teil.length)));
    pos += teil.length + 1;
  });
  return out;
}

/**
 * Hängt die Widgets an eine CodeMirror-Instanz. `kontext()` liefert bei jedem Abgleich
 * `{roh, itemId, assetIds}` (Rohmodus = keine Widgets; die IDs für `asset:`-Bilder in Zellen).
 * Rückgabe: `{abgleichen, marken}` — `abgleichen()` sofort (z. B. nach `setRawMode`).
 */
export function installiere(cm, kontext) {
  var marken = [];           // {mark, von, bis, text}
  var geplant = null;

  function planen() {
    if (geplant === null) geplant = setTimeout(abgleichen, 0);
  }

  function abgleichen() {
    if (geplant !== null) { clearTimeout(geplant); geplant = null; }
    // **Nie ein Wurf aus einem Änderungs-Handler** — ein Fehler hier kostet höchstens das Widget.
    try { cm.operation(_abgleich); } catch (err) { console.warn("Tabellen-Widget:", err); }
  }

  function _drin(b, sel) {
    for (var s = 0; s < sel.length; s++) {
      var a = sel[s].anchor.line, h = sel[s].head.line;
      if ((a >= b.von && a <= b.bis) || (h >= b.von && h <= b.bis)) return true;
    }
    return false;
  }

  function _abgleich() {
    var k = kontext() || {};
    var wunsch = [];
    if (!k.roh) {
      var zeilen = cm.getValue().split("\n");
      var sel = cm.listSelections();
      blockRanges(zeilen).forEach(function (b) {
        if (_drin(b, sel)) return;
        wunsch.push({ von: b.von, bis: b.bis, laenge: zeilen[b.bis].length,
                      text: zeilen.slice(b.von, b.bis + 1).join("\n") });
      });
    }
    // Erst zuordnen, dann alte räumen, dann neue setzen — zwei eingeklappte Bereiche dürfen
    // sich nie teilweise überlappen (CodeMirror wirft sonst).
    var offen = marken;
    var bleiben = [];
    var neu = [];
    wunsch.forEach(function (w) {
      for (var i = 0; i < offen.length; i++) {
        var e = offen[i];
        var f = e.mark.find();
        if (f && e.text === w.text && f.from.line === w.von && f.from.ch === 0
            && f.to.line === w.bis && f.to.ch === w.laenge) {
          bleiben.push(offen.splice(i, 1)[0]);
          return;
        }
      }
      neu.push(w);
    });
    offen.forEach(function (e) { e.mark.clear(); });
    marken = bleiben;
    neu.forEach(function (w) {
      try {
        var m = _baue(w, k);
        if (m) marken.push(m);
      } catch (err) { console.warn("Tabellen-Widget:", err); }
    });
  }

  function _baue(w, k) {
    var html = markdownToHtml(w.text, { itemId: k.itemId, assetIds: k.assetIds });
    // Absicherung gegen Abweichung Scanner ↔ Renderer: nur genau **eine** Tabelle wird Widget.
    if (html.indexOf("<table>") !== 0 || html.indexOf("<table>", 1) !== -1
        || html.slice(-8) !== "</table>") return null;
    var huelle = document.createElement("div");
    huelle.className = "preview sfx-tabelle";
    huelle.innerHTML = html;               // nur Ausgabe von markdownToHtml (inkl. Sanitizer)
    // Kein eigener Fokus: Tastatur = Pfeile, Bildschirmleser lesen die echte <table>.
    huelle.querySelectorAll("a").forEach(function (a) { a.tabIndex = -1; });
    var mark = cm.markText({ line: w.von, ch: 0 }, { line: w.bis, ch: w.laenge },
      { replacedWith: huelle, clearOnEnter: true, handleMouseEvents: false });
    huelle.addEventListener("mousedown", function (e) { _klick(e, mark); });
    huelle.addEventListener("click", function (e) {
      if (e.target.closest && e.target.closest("a")) e.preventDefault();
    });
    return { mark: mark, von: w.von, bis: w.bis, text: w.text };
  }

  // Klick in eine Zelle → Widget weg, Cursor an den Anfang dieser Zelle in der Quelle.
  function _zielDerZelle(zelle, f) {
    var tr = zelle.parentNode;
    var zeile = tr.parentNode.tagName === "THEAD"
      ? f.from.line
      : f.from.line + 2 + Array.prototype.indexOf.call(tr.parentNode.rows, tr);
    var anf = zellAnfaenge(cm.getLine(zeile) || "");
    var ch = anf[Array.prototype.indexOf.call(tr.cells, zelle)];
    return { line: zeile, ch: typeof ch === "number" ? ch : 0 };
  }

  function _klick(e, mark) {
    if (e.button !== 0) return;
    var zelle = e.target.closest ? e.target.closest("td, th") : null;
    if (!zelle) return;                    // Rand/Bildlaufleiste: dem Browser lassen
    e.preventDefault();
    e.stopPropagation();
    try {
      var f = mark.find();
      if (!f) return;
      var ziel = _zielDerZelle(zelle, f);
      cm.operation(function () {
        mark.clear();
        cm.focus();
        cm.setCursor(ziel);
      });
    } catch (err) { console.warn("Tabellen-Widget:", err); }
  }

  // Pfeil ↓/↑ in ein Widget: CodeMirror rechnet die Zielspalte gegen die Widget-Zeile und landet
  // am Tabellenende (Anhang A4). `beforeCursorEnter` darf den Cursor nicht versetzen — darum hier,
  // bevor die Auswahl gesetzt wird: von oben → erste Tabellenzeile, von unten → letzte.
  function _eintritt(_cm, obj) {
    try {
      if (obj.origin !== "+move" || obj.ranges.length !== 1) return;
      var r = obj.ranges[0];
      if (r.anchor.line !== r.head.line || r.anchor.ch !== r.head.ch) return;
      var alt = cm.getCursor("head");
      for (var i = 0; i < marken.length; i++) {
        var f = marken[i].mark.find();
        if (!f || r.head.line < f.from.line || r.head.line > f.to.line) continue;
        var zeile = alt.line < f.from.line ? f.from.line : alt.line > f.to.line ? f.to.line : -1;
        if (zeile < 0) return;
        var p = { line: zeile, ch: Math.min(alt.ch, cm.getLine(zeile).length) };
        obj.update([{ anchor: p, head: p }]);
        return;
      }
    } catch (err) { console.warn("Tabellen-Widget:", err); }
  }

  // Eine Änderung **im** Widget-Bereich ohne Cursor dort (Undo, programmatisch): das Widget sofort
  // räumen — sonst zeigt es alten Text und CodeMirror misst die eingeklappte Zeile bei jeder Taste neu
  // (gemessen: 9 ms je Zeichen in der 200-Zeilen-Tabelle). Der Abgleich baut es danach einmal neu.
  cm.on("change", function (_cm, ch) {
    try {
      var von = ch.from.line, bis = ch.from.line + ch.text.length - 1;
      marken.forEach(function (e) {
        var f = e.mark.find();
        if (f && von <= f.to.line && bis >= f.from.line) e.mark.clear();
      });
    } catch (err) { console.warn("Tabellen-Widget:", err); }
  });
  cm.on("changes", planen);
  cm.on("cursorActivity", planen);
  cm.on("beforeSelectionChange", _eintritt);
  abgleichen();
  // `cm.state.sfxTabellen`: dieselbe Schnittstelle für die Probe (Abgleich messen, Marken zählen).
  cm.state.sfxTabellen = {
    abgleichen: abgleichen,
    marken: function () { return marken.slice(); },
  };
  return cm.state.sfxTabellen;
}
