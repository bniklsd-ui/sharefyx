"use strict";

// -- Markdown/Sanitizer (Plan §3.5, Step 7) --------------------------------------------------
// Geerntet aus docs/concepts/notiz_heft_example.html (sanitizeHtml/markdownToHtml/safeHref,
// Zeilen 212-275) und erweitert: h1-h4 (Quelle nur h1-h3), Zitate + GFM-Tabellen (Quelle hat
// keins von beidem), IMG (P6.5-J, Phase 6.5 Block B — nur `/api/v1/items/.../assets/...`,
// aufgelöst aus `asset:<id>`-Markern, siehe `safeSrc()`/`resolveAssetSrc()`). NICHT übernommen:
// Style-Attribute (unsere CSP `style-src 'self'` ohne `unsafe-inline` verhindert ohnehin, dass
// ein `style="..."` je greift), FIGURE/FONT/`data-asset-*`, Task-Checklisten (nicht in §3.5s
// Teilmenge), `tel:`/`#note:` (§3.5 nennt nur http/https/mailto/#item/<id>/asset:<id>).
//
// Pipeline exakt wie §3.5: sanitizeHtml(markdownToHtml(escapeHtml(src))) — das Vor-Escaping der
// GESAMTEN Quelle stört keine Markdown-Syntax (#, *, Backtick, [](), -, |, : sind keine
// HTML-Sonderzeichen), macht aber literales `<script>` im Nutzertext schon vor dem Parser
// inert. Einzige Folge: `>` (Zitat-Marker) kommt als `&gt;` an, die Zitat-Erkennung matcht
// deshalb gegen `&gt;`, nicht `>`.

// -- Format-Konvention Stufe 2 (P10.5, Block 11, Schritt 11.6 -- ED-3) ----------------------
//
// **Das Vokabular.** Drei Gruppen, jede eine **feste** Menge: Farben · Groessen ·
// Ausrichtungen. Ein unbekanntes `.irgendwas` bleibt **wörtlich** — im Text steht dann
// genau das, was der Mensch geschrieben hat.
//
// **Zwei Formen.** Inline: `[Text]{.rot}` (höchstens **eine** Farbe und höchstens **eine**
// Größe). Block: `::: {.zentriert}` … `:::` (eine Ausrichtung; der Inhalt wird rekursiv
// gerendert).
//
// **Warum das im Client steht und nicht im Server.** Die Konvention ist **Format**, keine
// Semantik: der Server speichert den Text, wie er ist (P10.5-I — „kein Code in
// `storage/`"), und erst der Browser rendert ihn. Ein Server, der die Klassen kennt, wäre
// ein Server, der Inhalte interpretiert — genau das verbietet das Kernprinzip.
var FORMAT_FARBEN = {
  "rot": "md-c-rot",
  "blau": "md-c-blau",
  "gruen": "md-c-gruen",
  "gelb": "md-c-gelb",
};
var FORMAT_GROESSEN = {
  "klein": "md-s-klein",
  "normal": "md-s-normal",
  "gross": "md-s-gross",
};
var FORMAT_AUSRICHTUNGEN = {
  "links": "md-a-links",
  "zentriert": "md-a-zentriert",
  "rechts": "md-a-rechts",
};

//: Die Inline-Form des Plans: `\[([^\]\n]+)\]\{((?:\.[a-z]+)(?: \.[a-z]+)?)\}`.
var FORMAT_INLINE_RE = /\[([^\]\n]+)\]\{((?:\.[a-z]+)(?: \.[a-z]+)?)\}/g;

//: Die Klassen einer Inline-Form: **höchstens eine Farbe und höchstens eine Größe**.
//: Alles andere — unbekannt, zwei Farben, zwei Größen — liefert `null`, und der Text
//: bleibt **wörtlich**.
function _formatInlineKlassen(klassen) {
  var namen = klassen.trim().split(/\s+/).map(function (n) { return n.replace(/^\./, ""); });
  var farbe = null;
  var groesse = null;
  for (var i = 0; i < namen.length; i++) {
    var name = namen[i];
    if (FORMAT_FARBEN[name]) {
      if (farbe) return null;          // **zwei** Farben: nicht erlaubt
      farbe = FORMAT_FARBEN[name];
    } else if (FORMAT_GROESSEN[name]) {
      if (groesse) return null;        // **zwei** Größen: nicht erlaubt
      groesse = FORMAT_GROESSEN[name];
    } else {
      return null;                     // unbekannte Klasse: **wörtlich**
    }
  }
  if (!farbe && !groesse) return null;
  return [farbe, groesse].filter(Boolean).join(" ");
}

//: Die Klassen einer Block-Form: **nur** Ausrichtungen (eine). Alles andere → `null`.
function _formatBlockKlassen(klassen) {
  var namen = klassen.trim().split(/\s+/).map(function (n) { return n.replace(/^\./, ""); });
  if (namen.length !== 1) return null;
  return FORMAT_AUSRICHTUNGEN[namen[0]] || null;
}

//: **Eine** Quelle fuer das Vokabular: der Editor (Werkzeugleiste und Overlay) laedt
//: dieselbe Liste, die der Renderer kennt. Zwei Listen waeren zwei Wahrheiten — und die
//: Werkzeugleiste koennte etwas anbieten, das der Renderer nicht kennt.
export var FORMAT_VOKABULAR = {
  farben: FORMAT_FARBEN,
  groessen: FORMAT_GROESSEN,
  ausrichtungen: FORMAT_AUSRICHTUNGEN,
};

function escapeHtml(value) {
  return String(value == null ? "" : value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

// `asset:<id>` löst nur auf, wenn ein `itemId` mitgegeben wurde (`updates.js` ruft
// `markdownToHtml()` ohne Item-Kontext auf) — ohne Auflösung bleibt der Marker im `src` stehen,
// `safeSrc()` in `sanitizeHtml()` lehnt ihn dann als unbekanntes Schema ab und ersetzt das
// `<img>` durch seinen Alt-Text. Kein Crash, kein Sonderfall nötig (P6.5-J, „fallende Kante").
function resolveAssetSrc(src, itemId) {
  var m = /^asset:(ast_[0-9a-f]{8})$/.exec(src);
  if (!m) return src;
  return itemId ? "/api/v1/items/" + itemId + "/assets/" + m[1] : src;
}

// P7-A3 (V73): `resolveAssetSrc()` prüft nur die URL-**Form**, nicht ob das Asset noch
// existiert — nach einem Entfernen (Verschieben nach `_trash/`) matcht die Route weiterhin,
// der Browser bekäme einen `404` statt eines sauberen Alt-Texts. `assetIds` (aus `item.assets`,
// wenn mitgegeben) macht die Existenzprüfung hier explizit, bevor überhaupt ein `<img>`
// entsteht — ohne `assetIds` bleibt das alte Verhalten (jede `ast_…`-Form wird aufgelöst).
//
// Phase 8.5 P8.5-6 (D4-Fund 2026-09-06, Pre-Z-Tausch 2026-09-07): Link- und Bild-Regex
// tolerieren jetzt `\[` / `\]` als Escape im Alt/Title-Text. Vorher matchte `[^\]]+`
// gierig bis zum ersten `]`, und ein Titel wie `Notiz \[Entwurf\]` (so eingefügt vom Picker
// über `editor.js :: _linkTextFor`, das `[`/`]` per `\[$1` maskiert) zerlegte die URL-Zuordnung
// -- eckige Klammern ja, runde nein. Die neue Alternative `\\[\[\]]` frisst genau zwei Zeichen
// als Einheit (`\` + `[` oder `]`); nach dem Match wird `\[`/`\]` im Text wieder zu `[`/`]`
// unescaped, damit der gerenderte Link-Text die Klammern literal zeigt.
function inlineMarkdown(escaped, itemId, assetIds) {
  // **Die Codespans zuerst.** Ein Codespan ist der einzige Bereich, in dem **keine**
  // Formatierung stattfindet — sie werden ausgeschnitten, die Regeln laufen nur über den
  // Rest, und am Ende kommen sie unverändert zurück.
  //
  // **Warum das neu ist (2026-10-25, Block 11.6):** die alte Kette lief über den ganzen
  // Text, also auch **innerhalb** eines Codespans — `**fett**` in `` `**fett**` `` wurde
  // **fett**. Die neue Format-Regel hätte denselben Fehler geerbt (`` `[x]{.rot}` `` wäre
  // rot geworden). Der Schnitt ist eine Korrektur, kein Umbau: die Ausgabe ändert sich nur
  // dort, wo sie vorher **falsch** war.
  var teile = escaped.split(/(`[^`]+`)/g);
  var raus = [];
  for (var i = 0; i < teile.length; i++) {
    if (i % 2) {
      // Der Codespan: nur der `<code>`-Rahmen, **keine** weitere Formatierung.
      raus.push(teile[i].replace(/^`([^`]+)`$/, "<code>$1</code>"));
    } else {
      raus.push(_inlineRegeln(teile[i], itemId, assetIds));
    }
  }
  return raus.join("");
}

function _inlineRegeln(escaped, itemId, assetIds) {
  return escaped
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/\*([^*]+)\*/g, "<em>$1</em>")
    // P10.5, Block 11, Schritt 11.6 (ED-3): die **Format-Konvention** — *vor* den Links,
    // wie im Plan. Ein unbekanntes `.irgendwas` (oder zwei Farben) bleibt **wörtlich**.
    .replace(FORMAT_INLINE_RE, function (whole, text, klassen) {
      var erlaubt = _formatInlineKlassen(klassen);
      if (!erlaubt) return whole;
      return '<span class="' + erlaubt + '">' + text + "</span>";
    })
    // Bildzweig MUSS vor dem Link-Replace laufen (P6.5-J) — sonst frisst die Link-Regex das
    // `[alt](src)` eines `![alt](src)` und das führende `!` bleibt als Text übrig.
    // Phase 8.5 P8.5-6: Alt-Text darf `\[` / `\]` enthalten (siehe Kommentar oben).
    .replace(/!\[((?:\\[\[\]]|[^\]])*)\]\(([^)\s]+)\)/g, function (whole, alt, src) {
      var m = /^asset:(ast_[0-9a-f]{8})$/.exec(src);
      if (m && assetIds && assetIds.indexOf(m[1]) === -1) return alt.replace(/\\([\[\]])/g, "$1");
      return '<img src="' + resolveAssetSrc(src, itemId) + '" alt="' +
        alt.replace(/\\([\[\]])/g, "$1") + '">';
    })
    // Phase 8.5 P8.5-6: Link-Text darf `\[` / `\]` enthalten (siehe Kommentar oben).
    .replace(/\[((?:\\[\[\]]|[^\]])+)\]\(([^)\s]+)\)/g, function (whole, text, url) {
      return '<a href="' + url + '">' + text.replace(/\\([\[\]])/g, "$1") + '</a>';
    });
}

function splitTableRow(line) {
  var trimmed = line.trim();
  if (trimmed.charAt(0) === "|") trimmed = trimmed.slice(1);
  if (trimmed.charAt(trimmed.length - 1) === "|") trimmed = trimmed.slice(0, -1);
  return trimmed.split("|");
}

function cellAlignClass(token) {
  var t = token.trim();
  var left = t.charAt(0) === ":";
  var right = t.charAt(t.length - 1) === ":";
  if (left && right) return "ta-c";
  if (right) return "ta-r";
  if (left) return "ta-l";
  return "";
}

var TABLE_SEPARATOR_RE = /^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?\s*$/;

// P10.5, Block 11, Schritt 11.5 (ED-2): die **Lesesicht** zeigt das To-do-Kaestchen —
// **deaktiviert**. Es gibt dort keinen Schreibweg: angehakt wird nur im Editor, und der
// Editor schreibt mit `version` (Hard Rule 3). Der Sanitizer **erzwingt** `disabled` noch
// einmal (fail-closed) — erlauben waere nicht genug.
function _todoHtml(inhalt, itemId, assetIds) {
  var m = /^\[([ xX])\](\s*)(.*)$/.exec(inhalt);
  if (!m) return inlineMarkdown(inhalt, itemId, assetIds);
  var erledigt = m[1] !== " ";
  return '<input type="checkbox" class="md-todo" disabled' + (erledigt ? " checked" : "")
    + "> " + inlineMarkdown(m[3], itemId, assetIds);
}

export function markdownToHtml(src, options) {
  var itemId = options && options.itemId;
  var assetIds = (options && options.assetIds) || null;
  // **Einmal** escapen, dann die Zeilen rendern. Der Block `::: {...}` rendert seinen
  // Inhalt **rekursiv** — und der Aufruf darf **nicht** noch einmal escapen (sonst stünde
  // `&amp;` im Text statt `&`).
  return _markdownZeilen(
    escapeHtml(src).replace(/\r\n/g, "\n").split("\n"), itemId, assetIds
  );
}

function _markdownZeilen(lines, itemId, assetIds) {
  var out = "";
  var i = 0;
  var listType = null;
  var paragraph = [];

  function flushParagraph() {
    if (paragraph.length) {
      out += "<p>" + inlineMarkdown(paragraph.join(" "), itemId, assetIds) + "</p>";
      paragraph = [];
    }
  }
  function closeList() {
    if (listType) {
      out += listType === "ul" ? "</ul>" : "</ol>";
      listType = null;
    }
  }

  while (i < lines.length) {
    var line = lines[i];
    var m;

    // P10.5, Block 11, Schritt 11.6 (ED-3): der Block `::: {.zentriert}` … `:::`. Der
    // Inhalt wird **rekursiv** gerendert (eine Liste mit einer Tabelle darin bleibt eine
    // Tabelle). **Keine Verschachtelung**: ein `:::` im Inhalt beendet den Block.
    // **Kein Ende oder unbekannte Klasse → wörtlich**: die `:::`-Zeilen bleiben Text, die
    // Ausrichtung greift nicht.
    if ((m = line.match(/^:::[ \t]*\{([^}]*)\}[ \t]*$/))) {
      flushParagraph();
      closeList();
      var blockKlassen = _formatBlockKlassen(m[1]);
      var inner = [];
      var geschlossen = false;
      i++;
      while (i < lines.length) {
        if (/^:::[ \t]*$/.test(lines[i])) { geschlossen = true; i++; break; }
        inner.push(lines[i]);
        i++;
      }
      if (!geschlossen || !blockKlassen) {
        paragraph.push(line);
        inner.forEach(function (z) { paragraph.push(z); });
        continue;
      }
      out += '<div class="' + blockKlassen + '">'
        + _markdownZeilen(inner, itemId, assetIds) + "</div>";
      continue;
    }

    if (/^```/.test(line)) {
      flushParagraph();
      closeList();
      out += "<pre><code>";
      i++;
      while (i < lines.length && !/^```/.test(lines[i])) {
        out += lines[i] + "\n";
        i++;
      }
      out += "</code></pre>";
      i++;
      continue;
    }

    if (line.indexOf("|") !== -1 && i + 1 < lines.length && TABLE_SEPARATOR_RE.test(lines[i + 1])) {
      flushParagraph();
      closeList();
      var headerCells = splitTableRow(line);
      var aligns = splitTableRow(lines[i + 1]).map(cellAlignClass);
      out += "<table><thead><tr>";
      headerCells.forEach(function (cell, idx) {
        var cls = aligns[idx] ? ' class="' + aligns[idx] + '"' : "";
        out += "<th" + cls + ">" + inlineMarkdown(cell.trim(), itemId, assetIds) + "</th>";
      });
      out += "</tr></thead><tbody>";
      i += 2;
      while (i < lines.length && lines[i].indexOf("|") !== -1 && lines[i].trim() !== "") {
        var cells = splitTableRow(lines[i]);
        out += "<tr>";
        cells.forEach(function (cell, idx) {
          var cls = aligns[idx] ? ' class="' + aligns[idx] + '"' : "";
          out += "<td" + cls + ">" + inlineMarkdown(cell.trim(), itemId, assetIds) + "</td>";
        });
        out += "</tr>";
        i++;
      }
      out += "</tbody></table>";
      continue;
    }

    if ((m = line.match(/^(#{1,4})\s+(.*)$/))) {
      flushParagraph();
      closeList();
      var level = m[1].length;
      out += "<h" + level + ">" + inlineMarkdown(m[2], itemId, assetIds) + "</h" + level + ">";
      i++;
      continue;
    }

    if ((m = line.match(/^&gt;\s?(.*)$/))) {
      flushParagraph();
      closeList();
      var quoteLines = [m[1]];
      i++;
      while (i < lines.length && (m = lines[i].match(/^&gt;\s?(.*)$/))) {
        quoteLines.push(m[1]);
        i++;
      }
      out += "<blockquote>" + quoteLines.map(function (l) { return "<p>" + inlineMarkdown(l, itemId, assetIds) + "</p>"; }).join("") + "</blockquote>";
      continue;
    }

    if ((m = line.match(/^[-*]\s+(.*)$/))) {
      flushParagraph();
      if (listType !== "ul") {
        closeList();
        out += "<ul>";
        listType = "ul";
      }
      // P10.5, Block 11, Schritt 11.5 (ED-2): eine To-do-Zeile traegt ihr Kaestchen —
      // in der **Lesesicht** deaktiviert (s. `_todoHtml`).
      out += "<li>" + _todoHtml(m[1], itemId, assetIds) + "</li>";
      i++;
      continue;
    }

    if ((m = line.match(/^\d+\.\s+(.*)$/))) {
      flushParagraph();
      if (listType !== "ol") {
        closeList();
        out += "<ol>";
        listType = "ol";
      }
      out += "<li>" + inlineMarkdown(m[1], itemId, assetIds) + "</li>";
      i++;
      continue;
    }

    if (/^(-{3,}|\*{3,}|_{3,})$/.test(line.trim())) {
      flushParagraph();
      closeList();
      out += "<hr>";
      i++;
      continue;
    }

    if (line.trim() === "") {
      flushParagraph();
      closeList();
      i++;
      continue;
    }

    closeList();
    paragraph.push(line.trim());
    i++;
  }
  flushParagraph();
  closeList();
  return sanitizeHtml(out);
}

var ALLOWED_TAGS = new Set([
  "P", "BR", "STRONG", "EM", "CODE", "PRE", "H1", "H2", "H3", "H4",
  "UL", "OL", "LI", "BLOCKQUOTE", "A", "TABLE", "THEAD", "TBODY", "TR", "TD", "TH", "HR", "IMG",
  // P10.5, Block 11, Schritt 11.5 (ED-2): das To-do-Kaestchen der **Lesesicht**. Es wird
  // **nur** von `markdownToHtml()` erzeugt (der Quelltext ist vorher escaped), und der
  // Sanitizer erzwingt `type="checkbox"` und `disabled` (s. unten).
  "INPUT",
  // P10.5, Block 11, Schritt 11.6 (ED-3): die **Format-Konvention** — `span` (Inline) und
  // `div` (Block). Nur mit `class` aus der festen Menge (s. `ALLOWED_FORMAT_CLASSES`).
  "SPAN", "DIV",
]);
var ALLOWED_ATTRS = {
  A: new Set(["href", "target", "rel"]),
  TD: new Set(["class"]),
  TH: new Set(["class"]),
  IMG: new Set(["src", "alt"]),
  INPUT: new Set(["type", "checked", "disabled", "class"]),
  SPAN: new Set(["class"]),
  DIV: new Set(["class"]),
};
var ALLOWED_CELL_CLASSES = new Set(["ta-l", "ta-c", "ta-r"]);
//: Die erlaubten Klassen am To-do-Kaestchen (ED-2) — dieselbe Strenge wie bei den
//: Tabellen-Zellen: eine feste Menge, kein freier Text.
var ALLOWED_TODO_CLASSES = new Set(["md-todo"]);
//: Die erlaubten Klassen der **Format-Konvention** (ED-3) — **eine feste Menge**, aus dem
//: Vokabular oben. Eine Klasse, die nicht darin steht, wird entfernt; der **Inhalt**
//: bleibt (es geht nur die Auszeichnung verloren, nicht der Text).
var ALLOWED_FORMAT_CLASSES = new Set(
  Object.keys(FORMAT_FARBEN).map(function (k) { return FORMAT_FARBEN[k]; })
    .concat(Object.keys(FORMAT_GROESSEN).map(function (k) { return FORMAT_GROESSEN[k]; }))
    .concat(Object.keys(FORMAT_AUSRICHTUNGEN).map(function (k) { return FORMAT_AUSRICHTUNGEN[k]; }))
);

function safeHref(href) {
  var h = (href || "").trim();
  if (/^#item\/[a-zA-Z0-9_-]+$/.test(h)) return h;
  if (/^(https?:|mailto:)/i.test(h)) return h;
  return "";
}

// Ausschließlich unsere eigene Asset-Download-Route — kein `data:` (CSP erlaubt es zwar,
// P6.5-V verbietet es trotzdem: ein `data:`-URI trägt beliebige Bytes direkt im Markdown-Text,
// nicht mehr nur einen Verweis auf ein bereits ACL-geprüftes Asset), keine fremde Domain (kein
// Tracking-Pixel/kein Netzabruf beim bloßen Lesen eines fremden Items, Hard Rule 4).
function safeSrc(src) {
  var s = (src || "").trim();
  if (/^\/api\/v1\/items\/itm_[0-9a-f]{8}\/assets\/ast_[0-9a-f]{8}$/.test(s)) return s;
  return "";
}

function sanitizeHtml(html) {
  var template = document.createElement("template");
  template.innerHTML = html || "";

  function walk(node) {
    var children = [].slice.call(node.children);
    for (var idx = 0; idx < children.length; idx++) {
      var child = children[idx];
      if (!ALLOWED_TAGS.has(child.tagName)) {
        child.replaceWith.apply(child, [].slice.call(child.childNodes));
        walk(node);
        return;
      }
      var allowed = ALLOWED_ATTRS[child.tagName] || new Set();
      [].slice.call(child.attributes).forEach(function (attr) {
        if (!allowed.has(attr.name.toLowerCase())) child.removeAttribute(attr.name);
      });
      if ((child.tagName === "TD" || child.tagName === "TH") && child.hasAttribute("class")) {
        if (!ALLOWED_CELL_CLASSES.has(child.getAttribute("class"))) child.removeAttribute("class");
      }
      if (child.tagName === "INPUT") {
        // P10.5, Block 11, Schritt 11.5 (ED-2): das To-do-Kaestchen der **Lesesicht** —
        // ein Kaestchen, **kein Schreibweg**. `type` und `disabled` werden **erzwungen**,
        // nicht bloss erlaubt: ein anhakbares Kaestchen waere ein Schreibweg ausserhalb
        // des Editors — und ohne `version` (Hard Rule 3).
        child.setAttribute("type", "checkbox");
        child.setAttribute("disabled", "disabled");
        if (!ALLOWED_TODO_CLASSES.has(child.getAttribute("class"))) child.removeAttribute("class");
      }
      if (child.tagName === "SPAN" || child.tagName === "DIV") {
        // P10.5, Block 11, Schritt 11.6 (ED-3): die **Format-Konvention**. Die Klassen
        // kommen aus einer **festen Menge** — jede andere Klasse wird entfernt, der
        // **Inhalt bleibt**. (Dieselbe Strenge wie bei den Tabellen-Zellen: ein freier
        // Klassenname waere ein freier CSS-Hook.)
        if (child.hasAttribute("class")) {
          var formatKlassen = child.getAttribute("class").split(/\s+/).filter(function (k) {
            return ALLOWED_FORMAT_CLASSES.has(k);
          });
          if (formatKlassen.length) child.setAttribute("class", formatKlassen.join(" "));
          else child.removeAttribute("class");
        }
      }
      if (child.tagName === "IMG") {
        var safeImgSrc = safeSrc(child.getAttribute("src"));
        if (!safeImgSrc) {
          // Ein <img> ohne src ist ein toter Knoten (P6.5-J) -- durch den Alt-Text ersetzen,
          // nicht nur das Attribut entfernen. Trifft `javascript:`/fremde Domains/data:-URIs/
          // unaufgelöste `asset:`-Marker gleichermaßen.
          child.replaceWith(document.createTextNode(child.getAttribute("alt") || ""));
          walk(node);
          return;
        }
        child.setAttribute("src", safeImgSrc);
      }
      if (child.tagName === "A") {
        var safe = safeHref(child.getAttribute("href"));
        if (safe) {
          child.setAttribute("href", safe);
          if (/^https?:/i.test(safe)) {
            child.setAttribute("target", "_blank");
            child.setAttribute("rel", "noopener noreferrer");
          } else {
            child.removeAttribute("target");
            child.removeAttribute("rel");
          }
        } else {
          child.removeAttribute("href");
        }
      }
      walk(child);
    }
  }
  walk(template.content);
  return template.innerHTML;
}
