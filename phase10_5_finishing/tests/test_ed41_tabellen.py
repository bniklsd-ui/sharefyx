"""Editor 4.1, Schritt S2: das **Tabellen-Widget** (`phase5_ui/webui/static/js/editor/tabellen.js`).

Plan `docs/concepts/phase10_5_editor_4_1_plan.md` §5 S2, §4.2 (Byte-Vertrag), §4.3 (Sicherheitskette),
§4.4 (Budget-Regel). Statisch, ohne Browser; der Scanner laeuft in `node` (kein Build, P5-T). Das
Verhalten im Browser misst die Probe `probes/p105_ed41_darstellung_probe.py` (Beleg `…_s2.json`).

- **Budget-Regel §4.4:** keine `js/*.js`-Datei importiert eine `js/editor/`-Datei **statisch**; das
  Widget-Modul kommt genau einmal per `import()` aus `editor.js`. Gegenprobe (Plan-Gegenlauf 3):
  ein statischer Import in einer Kopie macht **dieselbe** Pruefung rot.
- **Sicherheitskette:** `innerHTML` nur aus `markdownToHtml()` (Sanitizer), kein `style=`/`<style>` (CSP).
- **Interim-Scanner:** dieselben Tabellen wie der heutige Renderer (`_markdownZeilen`), dieselbe
  Zellteilung (`splitTableRow`) fuer die Klick-Zuordnung.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
STATIC = REPO_ROOT / "phase5_ui" / "webui" / "static"
JS = STATIC / "js"
TABELLEN = JS / "editor" / "tabellen.js"
EDITOR = JS / "editor.js"
MARKDOWN = JS / "markdown.js"

needs_node = pytest.mark.skipif(shutil.which("node") is None, reason="node fehlt (P5-T: kein Build)")

_STATISCH = re.compile(r"""^\s*(?:import|export)\b[^;(]*?\bfrom\s*["']([^"']+)["']|^\s*import\s*["']([^"']+)["']""", re.M)


def statische_editor_importe(static_dir: Path) -> list[str]:
    """Jeder **statische** `import`/`export … from` einer Datei unter `js/editor/` — aus irgendeiner
    `js/**.js`. Leer = die Budget-Regel haelt (der Erstaufruf zieht keinen Editor-Code mit)."""
    js = static_dir / "js"
    editor = (js / "editor").resolve()
    out = []
    for datei in sorted(js.rglob("*.js")):
        for m in _STATISCH.finditer(datei.read_text(encoding="utf-8")):
            ziel = (datei.parent / (m.group(1) or m.group(2))).resolve()
            if ziel.is_relative_to(editor):
                out.append("%s -> %s" % (datei.relative_to(static_dir), m.group(1) or m.group(2)))
    return out


def test_no_module_imports_js_editor_statically():
    assert statische_editor_importe(STATIC) == []


def test_the_guard_bites_on_a_static_import(tmp_path):
    """Plan S2 Gegenlauf (3): ein statischer Import von `js/editor/` -> der Waechter wird rot."""
    kopie = tmp_path / "static"
    shutil.copytree(STATIC / "js", kopie / "js")
    app = kopie / "js" / "app.js"
    app.write_text('import { installiere } from "./editor/tabellen.js";\n' + app.read_text(encoding="utf-8"),
                   encoding="utf-8")
    assert statische_editor_importe(kopie) == ["js/app.js -> ./editor/tabellen.js"]


def test_the_widget_module_is_loaded_once_via_dynamic_import_from_the_editor():
    quelle = EDITOR.read_text(encoding="utf-8")
    assert quelle.count('import("./editor/tabellen.js")') == 1
    alle = "".join(p.read_text(encoding="utf-8") for p in JS.rglob("*.js") if p != EDITOR)
    assert "editor/tabellen.js" not in alle
    # ein fehlgeschlagener Import faellt auf den Rohtext zurueck, nie ein Wurf
    assert re.search(r'import\("\./editor/tabellen\.js"\)\.then\(.*?\)\.catch\(', quelle, re.S)


def test_innerhtml_only_from_markdowntohtml_and_no_inline_style():
    quelle = TABELLEN.read_text(encoding="utf-8")
    zuweisungen = re.findall(r"\.innerHTML\s*=\s*([^;]+);", quelle)
    assert zuweisungen == ["html"], zuweisungen
    assert re.search(r"var html = markdownToHtml\(w\.text,", quelle)
    assert len(re.findall(r"\bmarkdownToHtml\(", re.sub(r"^\s*//.*$", "", quelle, flags=re.M))) == 1
    assert 'from "../markdown.js"' in quelle
    for verboten in ("style=", "<style", "outerHTML", "insertAdjacentHTML", "document.write", "eval("):
        assert verboten not in quelle, verboten


def test_the_widget_does_not_write_history_or_text():
    """V1/V4: Widgets setzen/raeumen aendert keinen Text -- kein Schreibbefehl im Modul ausser im
    Kommentar; `markText` ohne `addToHistory`."""
    code = "\n".join(z for z in TABELLEN.read_text(encoding="utf-8").splitlines() if not z.strip().startswith("//"))
    for schreibt in ("replaceRange", "setValue", "replaceSelection", "addToHistory: true", "execCommand"):
        assert schreibt not in code, schreibt
    assert "clearOnEnter: true" in code and "handleMouseEvents: false" in code
    assert "atomic" not in code  # atomic liesse den Cursor ueber die Tabelle springen (V3-Zelle)


def test_the_separator_regex_is_the_renderers():
    trenner = re.search(r"var TRENNER = (/.*?/);", TABELLEN.read_text(encoding="utf-8")).group(1)
    renderer = re.search(r"var TABLE_SEPARATOR_RE = (/.*?/);", MARKDOWN.read_text(encoding="utf-8")).group(1)
    assert trenner == renderer


def _node(code: str) -> object:
    proc = subprocess.run(["node", "--input-type=module", "-e", code], capture_output=True, text=True,
                          timeout=60, cwd=str(REPO_ROOT))
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


_FAELLE = {
    # Name: (Text, erwartete [von, bis])
    "einfach": ("vor\n\n| a | b |\n|---|---|\n| 1 | 2 |\n\nnach", [[2, 4]]),
    "ende_ohne_newline": ("| a | b |\n|---|---|\n| 1 | 2 |", [[0, 2]]),
    "nur_kopf": ("| a | b |\n|---|---|", [[0, 1]]),
    "ohne_aussenpipes": ("a | b\n:--- | ---:\nx | y\nnur eins\n", [[0, 2]]),
    "zwei_ohne_leerzeile_sind_eine": ("| a |\n|---|\n| 1 |\n| b |\n|---|\n| 2 |\n", [[0, 5]]),
    "zwei_mit_leerzeile": ("| a |\n|---|\n\n| b |\n|---|\n", [[0, 1], [3, 4]]),
    "nach_liste_und_ueberschrift": ("- x\n| a |\n|---|\n## h\n| b |\n|---|\n", [[1, 2], [4, 5]]),
    "im_zaun_nicht": ("```\n| a |\n|---|\n```\n| b |\n|---|\n", [[4, 5]]),
    "zaun_ohne_ende_bis_dateiende": ("```\n| a |\n|---|\n", []),
    "tilde_ist_kein_zaun": ("~~~\n| a |\n|---|\n~~~\n", [[1, 2]]),
    "im_block_bleibt_roh": ("::: {.zentriert}\n| a |\n|---|\n:::\n| b |\n|---|\n", [[4, 5]]),
    "block_ohne_ende_verschluckt": ("::: {.warnung}\n| a |\n|---|\n", []),
    "im_zitat_nicht": ("> | a |\n> |---|\n> | 1 |\n", []),
    "nackter_trenner": ("a | b\n---\n", [[0, 1]]),
    "ohne_pipe_kein_kopf": ("Setext\n---\n", []),
}


@needs_node
def test_the_interim_scanner_finds_the_renderers_tables():
    code = ("import {blockRanges} from './phase5_ui/webui/static/js/editor/tabellen.js';"
            "const f = JSON.parse(process.argv[1] || '{}');")
    faelle = json.dumps({k: v[0] for k, v in _FAELLE.items()})
    code = ("import {blockRanges} from './phase5_ui/webui/static/js/editor/tabellen.js';"
            "const f = %s; const out = {};"
            "for (const [k, t] of Object.entries(f)) out[k] = blockRanges(t.split('\\n')).map(b => [b.von, b.bis]);"
            "console.log(JSON.stringify(out));") % faelle
    ist = _node(code)
    assert ist == {k: v[1] for k, v in _FAELLE.items()}


@needs_node
def test_the_scanner_agrees_with_the_renderer_on_the_corpus():
    """Jede gefundene Tabelle rendert der heutige Renderer als **genau eine** `<table>` -- und die
    Zahl der obersten Tabellen des ganzen Texts ist die Zahl der Bereiche (ohne `:::`-Bloecke, die
    der Scanner bewusst roh laesst). Ohne DOM: der Sanitizer laeuft nicht, nur `_markdownZeilen`."""
    fixtures = sorted((REPO_ROOT / "phase10_5_finishing" / "probes" / "fixtures_ed41").glob("*.txt"))
    code = """
import {blockRanges} from './phase5_ui/webui/static/js/editor/tabellen.js';
import {readFileSync} from 'fs';
globalThis.document = {createElement: () => ({innerHTML: '', content: {children: []}})};
const M = await import('./phase5_ui/webui/static/js/markdown.js');
const out = {};
for (const pfad of %s) {
  const text = readFileSync(pfad, 'utf8').replace(/\\r\\n/g, '\\n');
  const zeilen = text.split('\\n');
  const b = blockRanges(zeilen);
  out[pfad] = {bereiche: b.length, tabellen: b.map(x => {
    const h = M.markdownToHtml(zeilen.slice(x.von, x.bis + 1).join('\\n'), {});
    return (h.match(/<table>/g) || []).length; })};
}
console.log(JSON.stringify(out));
""" % json.dumps([str(p) for p in fixtures])
    # Der Sanitizer braucht ein DOM; die Attrappe (`template` ohne Kinder) liefert die Rohausgabe
    # von `_markdownZeilen` -- gezaehlt werden nur die `<table>`-Tags.
    ist = _node(code)
    gesamt = sum(v["bereiche"] for v in ist.values())
    assert gesamt == 7, ist      # 11:1, 12:2, 26_crlf:1, 27:1, 28:2
    for pfad, v in ist.items():
        assert all(n == 1 for n in v["tabellen"]), (pfad, v)
    namen = {Path(p).name: v["bereiche"] for p, v in ist.items()}
    assert namen["11_tabelle_einfach.txt"] == 1
    assert namen["12_tabelle_ki.txt"] == 2
    assert namen["13_tabelle_im_zitat.txt"] == 0
    assert namen["27_gross.txt"] == 1
    assert namen["28_katalog.txt"] == 2      # die Tabelle im Zitat bleibt roh, wie in der Lesesicht


@needs_node
def test_the_cell_starts_follow_the_renderers_split():
    faelle = {
        "| `retries` | Anzahl der Versuche |": [2, 14],
        "Spalte A | Spalte B | Spalte C": [0, 11, 22],
        "|  | leere Zelle |": [2, 5],
        "| a \\| b | Pipe maskiert |": [2, 7, 11],     # F3: der heutige Renderer teilt an `\\|` (S3)
        "  | x |y|": [4, 7],
        "| a |": [2],
    }
    code = ("import {zellAnfaenge} from './phase5_ui/webui/static/js/editor/tabellen.js';"
            "const f = %s; const out = {}; for (const z of f) out[z] = zellAnfaenge(z);"
            "console.log(JSON.stringify(out));") % json.dumps(list(faelle))
    assert _node(code) == faelle


def test_raw_mode_reconciles_the_widgets():
    """`setRawMode(true)` -> keine Widgets: der Schalter ruft den Abgleich, und der Abgleich liest `roh`."""
    quelle = EDITOR.read_text(encoding="utf-8")
    raw = quelle[quelle.index("function setRawMode(on) {"):]
    raw = raw[:raw.index("\n}\n")]
    assert "if (cmTabellen) cmTabellen.abgleichen();" in raw
    assert 'roh: state.mode === "raw"' in quelle


@needs_node
def test_raw_mode_produces_no_widget_and_live_mode_one():
    """Der Abgleich an einer CodeMirror-Attrappe: `roh` -> 0 Marken, sonst 1 (Cursor ausserhalb)."""
    code = r"""
globalThis.document = {createElement: () => ({innerHTML: '', content: {children: []},
  querySelectorAll: () => [], addEventListener: () => {}})};
const {installiere} = await import('./phase5_ui/webui/static/js/editor/tabellen.js');
const text = 'vor\n\n| a | b |\n|---|---|\n| 1 | 2 |\n\nnach';
let roh = true; const marken = [];
const cm = {state: {}, on() {}, operation(f) { f(); }, getValue: () => text,
  getLine: (n) => text.split('\n')[n], getCursor: () => ({line: 0, ch: 0}),
  listSelections: () => [{anchor: {line: 0, ch: 0}, head: {line: 0, ch: 0}}],
  markText(von, bis, opt) { const m = {von, bis, opt, weg: false, find() { return this.weg ? undefined : {from: von, to: bis}; },
    clear() { this.weg = true; }}; marken.push(m); return m; }};
const T = installiere(cm, () => ({roh}));
const a = T.marken().length;
roh = false; T.abgleichen(); const b = T.marken().length;
roh = true; T.abgleichen(); const c = T.marken().length;
console.log(JSON.stringify({roh: a, live: b, wieder_roh: c, gesetzt: marken.length,
  bereich: [marken[0].von, marken[0].bis], history: 'addToHistory' in marken[0].opt}));
"""
    assert _node(code) == {"roh": 0, "live": 1, "wieder_roh": 0, "gesetzt": 1,
                           "bereich": [{"line": 2, "ch": 0}, {"line": 4, "ch": 9}], "history": False}
