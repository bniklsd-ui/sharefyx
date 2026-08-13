"use strict";

// -- Markdown/Sanitizer (Plan §3.5, Step 7) --------------------------------------------------
// Geerntet aus docs/concepts/notiz_heft_example.html (sanitizeHtml/markdownToHtml/safeHref,
// Zeilen 212-275) und erweitert: h1-h4 (Quelle nur h1-h3), Zitate + GFM-Tabellen (Quelle hat
// keins von beidem). NICHT übernommen: Style-Attribute (unsere CSP `style-src 'self'` ohne
// `unsafe-inline` verhindert ohnehin, dass ein `style="..."` je greift), IMG/FIGURE/FONT/
// `data-asset-*` (kein Anhang-Feature, P5-AA), Task-Checklisten (nicht in §3.5s Teilmenge),
// `tel:`/`#note:`/`#asset:` (§3.5 nennt nur http/https/mailto/#item/<id>).
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

function inlineMarkdown(escaped) {
  return escaped
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/\*([^*]+)\*/g, "<em>$1</em>")
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

export function markdownToHtml(src) {
  var lines = escapeHtml(src).replace(/\r\n/g, "\n").split("\n");
  var out = "";
  var i = 0;
  var listType = null;
  var paragraph = [];

  function flushParagraph() {
    if (paragraph.length) {
      out += "<p>" + inlineMarkdown(paragraph.join(" ")) + "</p>";
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
        out += "<th" + cls + ">" + inlineMarkdown(cell.trim()) + "</th>";
      });
      out += "</tr></thead><tbody>";
      i += 2;
      while (i < lines.length && lines[i].indexOf("|") !== -1 && lines[i].trim() !== "") {
        var cells = splitTableRow(lines[i]);
        out += "<tr>";
        cells.forEach(function (cell, idx) {
          var cls = aligns[idx] ? ' class="' + aligns[idx] + '"' : "";
          out += "<td" + cls + ">" + inlineMarkdown(cell.trim()) + "</td>";
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
      out += "<h" + level + ">" + inlineMarkdown(m[2]) + "</h" + level + ">";
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
      out += "<blockquote>" + quoteLines.map(function (l) { return "<p>" + inlineMarkdown(l) + "</p>"; }).join("") + "</blockquote>";
      continue;
    }

    if ((m = line.match(/^[-*]\s+(.*)$/))) {
      flushParagraph();
      if (listType !== "ul") {
        closeList();
        out += "<ul>";
        listType = "ul";
      }
      out += "<li>" + inlineMarkdown(m[1]) + "</li>";
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
      out += "<li>" + inlineMarkdown(m[1]) + "</li>";
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
  "UL", "OL", "LI", "BLOCKQUOTE", "A", "TABLE", "THEAD", "TBODY", "TR", "TD", "TH", "HR",
]);
var ALLOWED_ATTRS = {
  A: new Set(["href", "target", "rel"]),
  TD: new Set(["class"]),
  TH: new Set(["class"]),
};
var ALLOWED_CELL_CLASSES = new Set(["ta-l", "ta-c", "ta-r"]);

function safeHref(href) {
  var h = (href || "").trim();
  if (/^#item\/[a-zA-Z0-9_-]+$/.test(h)) return h;
  if (/^(https?:|mailto:)/i.test(h)) return h;
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
