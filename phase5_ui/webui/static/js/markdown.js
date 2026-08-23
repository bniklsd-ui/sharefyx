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
function inlineMarkdown(escaped, itemId, assetIds) {
  return escaped
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/\*([^*]+)\*/g, "<em>$1</em>")
    // Bildzweig MUSS vor dem Link-Replace laufen (P6.5-J) — sonst frisst die Link-Regex das
    // `[alt](src)` eines `![alt](src)` und das führende `!` bleibt als Text übrig.
    .replace(/!\[([^\]]*)\]\(([^)\s]+)\)/g, function (whole, alt, src) {
      var m = /^asset:(ast_[0-9a-f]{8})$/.exec(src);
      if (m && assetIds && assetIds.indexOf(m[1]) === -1) return alt;
      return '<img src="' + resolveAssetSrc(src, itemId) + '" alt="' + alt + '">';
    })
    .replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, '<a href="$2">$1</a>');
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

export function markdownToHtml(src, options) {
  var itemId = options && options.itemId;
  var assetIds = (options && options.assetIds) || null;
  var lines = escapeHtml(src).replace(/\r\n/g, "\n").split("\n");
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
      out += "<li>" + inlineMarkdown(m[1], itemId, assetIds) + "</li>";
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
]);
var ALLOWED_ATTRS = {
  A: new Set(["href", "target", "rel"]),
  TD: new Set(["class"]),
  TH: new Set(["class"]),
  IMG: new Set(["src", "alt"]),
};
var ALLOWED_CELL_CLASSES = new Set(["ta-l", "ta-c", "ta-r"]);

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
