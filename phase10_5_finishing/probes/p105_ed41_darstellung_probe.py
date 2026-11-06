#!/usr/bin/env python3
"""Editor 4.1, Schritt S0 — die **Darstellungs-Probe** (Basislinie, kein Produktcode).

Plan: `docs/concepts/phase10_5_editor_4_1_plan.md` §5 (S0), §4 (V1–V7), §7 (Darstellungs-Check, Schicht 1);
Anhang A1/A7. Korpus, Zellen und Gegenlaeufe: `p105_ed41_spec.py` (eine Quelle, ohne Seiteneffekte).

**Was gemessen wird.** Das Katalog-Item (`fixtures_ed41/28_katalog.txt`, jedes Konstrukt einmal) wird
im **eigenen** Space `alpha` im Editor (CM5) und im **fremden** Space `beta` (alpha hat nur Leserecht)
in der Lesesicht (`#ro-preview`) geoeffnet. Je Konstrukt eine Zelle je Sicht (`l_*`, `e_*`), dazu
die Widersprueche F4a–f (`konflikt_*`, gruen nur, wenn **beide** Sichten das Ziel zeigen), die
Sicherheitszellen `html_als_text`/`keine_aktiven` (XSS-Liste), `tabelle_widget`, `listenzeichen`,
`kontrast` (WCAG-Kontrast jeder Editor-Tokenfarbe gegen den Editorhintergrund, aus `getComputedStyle`),
die Byte-Zellen V1–V3 ueber **alle 28** Fixtures und die Entwurfs-Zellen V7/F7.

**Die Basislinie ist rot — das ist der Befund** (Plan S0). Welche Zelle heute rot sein muss, steht in
`p105_ed41_spec.ZELLEN[...]["basis"]`; eine Abweichung davon steht im Beleg unter `abweichungen`.

**Wegwerf-Instanz** (Root-`CLAUDE.md`): Server, Konto, TLS, Start/Stopp aus Block 14
(`p105_b14_layout_probe.py`, als Modul geladen wie in `p105_b18_live_zeilen_probe.py`); freier Port,
tmp-`DATA_ROOT`/`auth.sqlite3`/DEK, bereinigte Umgebung (`SHAREFYX_*`/`SFX_*`/`SPACE_*` entfernt),
Stopp **nur** ueber die PID-Datei (Hard Rule 9). **Je Browser eine frische Saat** (die Probe schreibt:
V3-Edits, Entwurf, ein fremder PATCH). Playwright aus `~/.claude-code-tools/e2e-venv`
(Chromium 151, Firefox 153).

**Gegenlaeufe** (`--gegenlauf=NAME`, Beleg `p105_ed41_darstellung_gegenlauf_NAME.json`, immer beide
Browser): eine **Kopie** der Fixture-Bytes (Saat) bzw. der statischen Dateien (`STATIC_DIR`) wird
gepatcht; jeder Anker kommt **genau einmal** vor. Der Waechter verlangt, dass sich gegenueber der
Basislinie **genau** die Zellen in `kippt` umdrehen. Drei Arten, weil eine rote Basis-Zelle nicht
durch Rot-Werden beweist, dass sie misst:

| Gegenlauf | Eingriff | kippt |
|---|---|---|
| `fixture_kaputt` | Katalog-Kopie: `#### Katalog…` → `####Katalog…` (keine Ueberschrift) | `l_ueberschrift_h1_h4` gruen → rot |
| `trimend` | `editor.js`-Kopie: `setBody` mit `trimEnd()` (Plan S2 Gegenlauf 4) | `bytes_gleich` gruen → rot |
| `css_rot_nach_gruen` | `app.css`-Kopie: Listenzeichen sichtbar, die vier vendorten Tokenfarben hell | `listenzeichen`, `kontrast` rot → gruen |
| `s1_ohne_ursprung` | `editor.js`-Kopie: Ursprungspruefung (`change.origin === "setValue"`) raus (Plan S1 Gegenlauf 1) | `entwurf_ueberlebt_neuladen` gruen → rot |
| `s1_ohne_version` | `editor.js`-Kopie: Versionspruefung des Entwurfs raus (Plan S1 Gegenlauf 2) | `kein_stilles_zurueck` gruen → rot |
| `s2_ohne_installation` | `editor.js`-Kopie: `import()` des Widget-Moduls zeigt ins Leere (Plan S2 Gegenlauf 1) | `tabelle_widget` + die fuenf Zellen mit Widget-Vorbedingung gruen → rot |
| `s2_ohne_eintritt` | `tabellen.js`-Kopie: Eintritts-Korrektur (`beforeSelectionChange`) raus (Plan S2 Gegenlauf 2) | `pfeil_erste_zeile`, `pfeil_letzte_zeile` (Spalte) gruen → rot |
| `s2_ohne_klickziel` | `tabellen.js`-Kopie: Klick landet am Tabellenanfang statt in der Zelle | `klick_zelle` gruen → rot |
| `s2_polstert` | `tabellen.js`-Kopie: das Widget polstert die Quelle beim Oeffnen neu (V4) | `bytes_gleich` gruen → rot (Strg+S schreibt die Polsterung) |

**S2** (Tabellen-Widget): fuenf neue Zellen (`klick_zelle`, `pfeil_*`, `undo`, `kopieren_quelle`, je mit dem
Widget als Vorbedingung, an `11_tabelle_einfach`), `tabelle_widget` zaehlt die Widget-Marken gegen die obersten
Tabellen der Lesesicht; dazu Information `s2_rand` (ein per API angelegtes Item mit den Randfaellen) und
`tastenkosten_abgleich` (je Taste inkl. Abgleich, Cursor in der gemessenen Zeile). Plan-Gegenlauf (3) „statischer
Import von `js/editor/`" ist ein pytest-Waechter (`tests/test_ed41_tabellen.py`), kein Browserlauf.

**Staende** (ab S1): `p105_ed41_spec.STAND` ist der Stand des Arbeitsbaums; ein Lauf mit beiden Browsern
schreibt `BELEG_JE_STAND[STAND]` (S0 = `p105_ed41_darstellung.json`, eingefroren; S1 = `…_s1.json`; S2 = `…_s2.json`), und
ein Gegenlauf vergleicht mit dem Beleg **dieses** Stands (Feld `referenz` im Gegenlauf-Beleg).

Aufruf:   `.venv/bin/python phase10_5_finishing/probes/p105_ed41_darstellung_probe.py [--browser=chromium|firefox|beide] [--gegenlauf=NAME]`
Ergebnis: `phase10_5_finishing/probes/<BELEG_JE_STAND[STAND]>` (nur ein Lauf mit **beiden** Browsern schreibt
ihn; `--browser=X` allein schreibt nach `/tmp/p105_ed41_darstellung_X.json`). Bilder nach `/tmp/ed41_shots/`.
Die Fixtures werden **von der Platte** gesaet, jede gegen `fixtures_ed41/MANIFEST.json` geprueft (fail-closed).
Rueckgabe 0 = die Probe ist gelaufen; rote Zellen stehen im JSON und auf stderr.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HIER = Path(__file__).resolve().parent
E2E = Path.home() / ".claude-code-tools/e2e-venv/bin/python"
SHOTS = Path("/tmp/ed41_shots")

sys.path.insert(0, str(HIER))
import p105_ed41_spec as spec  # noqa: E402
#: Beleg des **heutigen** Stands (`spec.STAND`): S0 = die Basislinie, ab S1 je Schritt eine eigene Datei --
#: der Beleg eines frueheren Stands wird nie ueberschrieben.
RESULT = HIER / spec.BELEG_JE_STAND[spec.STAND]

GEGENLAUF = None
BROWSER = None
for _a in sys.argv[1:]:
    if _a.startswith("--gegenlauf="):
        GEGENLAUF = _a.split("=", 1)[1]
        if GEGENLAUF not in spec.GEGENLAEUFE:
            raise SystemExit("unbekannter Gegenlauf: %s (bekannt: %s)" % (GEGENLAUF, ", ".join(spec.GEGENLAEUFE)))
    elif _a.startswith("--browser="):
        BROWSER = _a.split("=", 1)[1]
if BROWSER is None:
    BROWSER = "beide"
BROWSERS = ["chromium", "firefox"] if BROWSER == "beide" else [BROWSER]
if GEGENLAUF and BROWSER != "beide":
    raise SystemExit("ein Gegenlauf laeuft immer in beiden Browsern (der Beleg vergleicht je Browser mit der Basislinie)")

# -- b14 als Modul (ohne seine Kommandozeile zu erben; Muster b18) --------------------------------
_argv = sys.argv
sys.argv = [_argv[0]]
_s = importlib.util.spec_from_file_location("p105_b14_layout_probe", HIER / "p105_b14_layout_probe.py")
b14 = importlib.util.module_from_spec(_s)
sys.modules["p105_b14_layout_probe"] = b14
_s.loader.exec_module(b14)
sys.argv = _argv
REPO_ROOT = b14.REPO_ROOT
STATIC_QUELLE = REPO_ROOT / "phase5_ui" / "webui" / "static"

# Der Launcher von b14 patcht nur `graph.js` (und ohne Genau-einmal-Pruefung). Diese Probe baut die
# Kopie selbst und laesst den Server sie ausliefern: eine kleine Weiche vor `load_settings()`.
WEICHE = '''_ed41_static = os.environ.get("ED41_STATIC_DIR")
if _ed41_static:
    from pathlib import Path as _P
    _ed41_orig = mapp.UiSettings
    def _ed41_settings(**kw):
        kw["static_dir"] = _P(_ed41_static)
        return _ed41_orig(**kw)
    mapp.UiSettings = _ed41_settings
'''
_ANKER = "settings = load_settings()\n"
if b14.SERVE_TLS_LAUNCHER.count(_ANKER) != 1:
    raise SystemExit("Anker des Starters nicht genau einmal -- b14.SERVE_TLS_LAUNCHER hat sich geaendert")
b14.SERVE_TLS_LAUNCHER = b14.SERVE_TLS_LAUNCHER.replace(_ANKER, WEICHE + _ANKER)

STATIC_KOPIE = b14.WEGWERF_ROOT / ("static-ed41-%d" % b14.PID)
FIXTURE_JSON = b14.WEGWERF_ROOT / ("ed41-fixtures-%d.json" % b14.PID)
IDS_JSON = b14.WEGWERF_ROOT / ("ed41-ids-%d.json" % b14.PID)

# -- Saat ------------------------------------------------------------------------------------------

SAAT = r'''
import json, struct, sys, zlib
from pathlib import Path
from datetime import datetime, timezone
import storage.files as sfiles
from storage.store import Store
from storage.acl import create_space, add_member
root = Path(sys.argv[1]); fixtures = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
asset_id = sys.argv[4]
z = [0]
def fid():
    z[0] += 1
    return "itm_%08x" % z[0]
sfiles.generate_id = fid
sfiles.new_asset_id = lambda: asset_id
def png1x1():
    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xffffffff)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(b"\x00\xff\x80\x00")) + chunk(b"IEND", b""))
for sp in ("alpha", "beta"):
    create_space(root, sp)
add_member(root, "beta", "alpha", write=False)
s = Store(root, git=False, now_fn=lambda: datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc))
ids, dateien = {}, {}
for sp, prefix in (("alpha", ""), ("beta", "fremd ")):
    for name, body in fixtures.items():
        it = s.create(sp, type="note", status="active", title=prefix + name, body=body)
        ids[sp + ":" + name] = it.id
        if asset_id in body:
            s.put_asset(it.id, data=png1x1(), filename="kontrolle.png")
s.rebuild_index()
for key, iid in ids.items():
    sp = key.split(":", 1)[0]
    dateien[key] = str(next((root / sp).glob(iid + "__*.md")))
json.dump({"ids": ids, "dateien": dateien}, open(sys.argv[3], "w"), indent=1)
'''


def fixtures_fuer_lauf() -> dict[str, str]:
    """Name -> Text (dekodiert aus den **Bytes**: `read_text()` wuerde CRLF uebersetzen)."""
    out = {name: b.decode("utf-8") for name, b in spec.fixtures_von_platte().items()}
    gl = spec.GEGENLAEUFE.get(GEGENLAUF or "", {})
    for name, patches in gl.get("fixture", {}).items():
        text = out[name]
        for alt, neu in patches:
            if text.count(alt) != 1:
                raise SystemExit("Fixture-Anker nicht genau einmal in %s: %r" % (name, alt))
            text = text.replace(alt, neu)
        out[name] = text
    return out


def seed(fixtures: dict[str, str]) -> dict:
    shutil.rmtree(b14.DATA_ROOT, ignore_errors=True)
    b14.DATA_ROOT.mkdir(parents=True, exist_ok=True)
    FIXTURE_JSON.write_text(json.dumps(fixtures, ensure_ascii=False), encoding="utf-8")
    subprocess.run([str(REPO_ROOT / ".venv/bin/python"), "-c", SAAT, str(b14.DATA_ROOT), str(FIXTURE_JSON),
                    str(IDS_JSON), spec.ASSET_ID], check=True, cwd=str(REPO_ROOT),
                   env={**b14._saubere_umgebung(), "PYTHONPATH": str(REPO_ROOT / "phase1_storage")})
    return json.loads(IDS_JSON.read_text(encoding="utf-8"))


def statische_kopie() -> None:
    """Kopie der statischen Dateien mit den Patches des Gegenlaufs (jeder Anker genau einmal)."""
    gl = spec.GEGENLAEUFE.get(GEGENLAUF or "", {})
    os.environ.pop("ED41_STATIC_DIR", None)
    if not gl.get("static"):
        return
    shutil.rmtree(STATIC_KOPIE, ignore_errors=True)
    shutil.copytree(STATIC_QUELLE, STATIC_KOPIE)
    for rel, patches in gl["static"].items():
        datei = STATIC_KOPIE / rel
        text = datei.read_text(encoding="utf-8")
        for alt, neu in patches:
            if text.count(alt) != 1:
                raise SystemExit("Gegenlauf-Anker nicht genau einmal in %s: %r" % (rel, alt[:70]))
            text = text.replace(alt, neu)
        datei.write_text(text, encoding="utf-8")
    os.environ["ED41_STATIC_DIR"] = str(STATIC_KOPIE)


def body_bytes(datei: str) -> bytes:
    roh = Path(datei).read_bytes()
    return roh.split(b"\n---\n", 1)[1]


def frontmatter_bytes(datei: str) -> bytes:
    return Path(datei).read_bytes().split(b"\n---\n", 1)[0]


# -- Browser-Teil (e2e-venv) -----------------------------------------------------------------------

BROWSER_MAIN = r'''
ED = "/ui/static/js/editor.js"
OEFFNE = "async (id) => { const E = await import('/ui/static/js/editor.js'); await E.selectItem(id); return true; }"
CM_DA = "() => !!document.querySelector('#detail-editor .CodeMirror') && !document.getElementById('detail-editor').hidden"
DIALOG = "() => !document.getElementById('confirm-dialog').hidden"
CM = "document.querySelector('#detail-editor .CodeMirror').CodeMirror"

MESSE = """async (id) => {
  const E = await import('/ui/static/js/editor.js');
  const item = await (await fetch('/api/v1/items/' + id)).json();
  const body = E.getBody();
  return {gleich: body === item.body, laenge_api: item.body.length, laenge_editor: body.length,
          cr_api: (item.body.match(/\\r/g) || []).length, dirty: E.isDirty(),
          speichern_aus: document.getElementById('save-button').disabled, api_body: item.body};
}"""

# Editor: Zeile ueber ihren Ankertext finden, in den Sichtbereich holen (viewportMargin 20: sonst
# steht sie nicht im DOM) und ihren DOM-Knoten auswerten.
EDITOR_ZEILEN = """(anker) => {
  const cm = %s;
  cm.setCursor({line: cm.lineCount() - 1, ch: 0});
  const out = {};
  for (const a of anker) {
    let n = -1;
    for (let i = 0; i < cm.lineCount(); i++) { if (cm.getLine(i).indexOf(a) !== -1) { n = i; break; } }
    if (n < 0) { out[a] = null; continue; }
    cm.scrollIntoView({line: n, ch: 0}, 80);
    const h = cm.getLineHandle(n);
    const v = cm.display.view.find(x => x.line === h);
    if (!v || !v.node) { out[a] = {zeile: n, knoten: false}; continue; }
    const pre = v.node.matches('pre.CodeMirror-line') ? v.node : v.node.querySelector('pre.CodeMirror-line');
    let sichtbar = '';
    const walk = (k) => {
      if (k.nodeType === 3) { if (getComputedStyle(k.parentElement).visibility !== 'hidden') sichtbar += k.textContent; return; }
      if (k.classList && k.classList.contains('CodeMirror-widget')) { sichtbar += '[W]'; return; }
      k.childNodes.forEach(walk);
    };
    if (pre) pre.childNodes.forEach(walk);
    const spans = Array.from((pre || v.node).querySelectorAll('span')).filter(s => s.className && s.className.indexOf('cm-') !== -1)
      .map(s => ({k: s.className, t: s.textContent, vis: getComputedStyle(s).visibility}));
    out[a] = {zeile: n, knoten: true, text: cm.getLine(n), sichtbar: sichtbar, spans: spans,
              todo: v.node.querySelectorAll('input.sfx-todo').length,
              wrap_klassen: v.node.className || ''};
  }
  // S2: die Widget-Marken zaehlen (unabhaengig vom Sichtbereich: viewportMargin 20 haelt nur ~30
  // Zeilen im DOM) und den DOM mit der ersten Tabelle im Bild pruefen.
  const T = cm.state.sfxTabellen;
  out.__widget_marken = T ? T.marken().filter(e => e.mark.find()).length : 0;
  let t0 = -1;
  for (let i = 0; i < cm.lineCount(); i++) { if (cm.getLine(i).indexOf('| Einstellung | Bedeutung') === 0) { t0 = i; break; } }
  if (t0 >= 0) cm.scrollIntoView({line: t0, ch: 0}, 200);
  out.__tabellen_im_editor = document.querySelectorAll('#detail-editor .CodeMirror .sfx-tabelle table').length;
  return out;
}""" % CM

# Kontrast: alle Zeilen in Schritten in den Sichtbereich holen, jede `cm-*`-Spanne nach ihrer
# berechneten Farbe gruppieren; WCAG 2.x relative Leuchtdichte, Alpha ueber dem Hintergrund verrechnet.
KONTRAST = """() => {
  const cm = %s;
  const wrap = cm.getWrapperElement();
  const parse = (c) => { const m = c.match(/rgba?\\(([^)]+)\\)/); const p = m[1].split(',').map(x => parseFloat(x));
    return {r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1}; };
  const bg = parse(getComputedStyle(wrap).backgroundColor);
  const lum = (c) => { const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
    return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b); };
  const ueber = (c) => ({r: c.r * c.a + bg.r * (1 - c.a), g: c.g * c.a + bg.g * (1 - c.a), b: c.b * c.a + bg.b * (1 - c.a)});
  const ratio = (c) => { const a = lum(ueber(c)), b = lum(bg); return (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05); };
  const klassen = {};
  for (let n = 0; n < cm.lineCount(); n += 8) {
    cm.scrollIntoView({line: n, ch: 0}, 0);
    for (const v of cm.display.view) {
      if (!v.node) continue;
      v.node.querySelectorAll('span').forEach(s => {
        if (!s.className || s.className.indexOf('cm-') === -1 || !s.textContent.trim()) return;
        if (s.closest('.CodeMirror-widget')) return;
        const col = getComputedStyle(s).color;
        const r = Math.round(ratio(parse(col)) * 100) / 100;
        const key = s.className.split(/\\s+/).filter(x => x.indexOf('cm-') === 0).sort().join(' ');
        if (!klassen[key] || klassen[key].kontrast > r) klassen[key] = {farbe: col, kontrast: r, beispiel: s.textContent.slice(0, 24)};
      });
    }
  }
  const t = parse(getComputedStyle(wrap).color);
  return {hintergrund: getComputedStyle(wrap).backgroundColor, text_kontrast: Math.round(ratio(t) * 100) / 100, klassen: klassen};
}""" % CM

LESESICHT = r"""() => {
  const P = document.getElementById('ro-preview');
  const q = (s) => Array.from(P.querySelectorAll(s));
  const txt = (e) => (e.textContent || '').replace(/\s+/g, ' ').trim();
  const hat = (sel, t) => q(sel).some(e => txt(e) === t);
  const r = {};
  const namen = ['Eins', 'Zwei', 'Drei', 'Vier', 'Fuenf', 'Sechs'];
  r.l_ueberschrift_h1_h4 = [1, 2, 3, 4].every(k => hat('h' + k, 'Katalog Ueberschrift ' + namen[k - 1]));
  r.l_ueberschrift_h5_h6 = hat('h5', 'Katalog Ueberschrift Fuenf') && hat('h6', 'Katalog Ueberschrift Sechs');
  r.l_setext = hat('h1', 'Setext Katalog Eins') && hat('h2', 'Setext Katalog Zwei');
  const absatz = q('p').find(p => txt(p).indexOf('Absatz mit') === 0);
  r.l_inline = !!absatz && !!absatz.querySelector('strong') && txt(absatz.querySelector('strong')) === 'fett'
    && !!absatz.querySelector('em') && !!absatz.querySelector('code') && txt(absatz.querySelector('code')) === 'codespan'
    && !!absatz.querySelector('a[href="https://example.invalid/a"]');
  r.l_durchgestrichen = hat('del', 'weg damit');
  const umbruch = q('p').find(p => txt(p).indexOf('Harter Umbruch hier') === 0);
  r.l_harter_umbruch = !!umbruch && !!umbruch.querySelector('br') && txt(umbruch).indexOf('naechste Zeile nach dem Umbruch') !== -1;
  r.l_autolink = q('a').some(a => txt(a) === 'https://example.invalid/nackt');
  r.l_entitaet = P.textContent.indexOf('Fisch & Chips') !== -1 && P.textContent.indexOf('&amp;') === -1;
  const tabMit = (kopf) => q('table').find(t => txt(t.querySelector('th') || {}) === kopf);
  const zeilen = (t) => t ? Array.from(t.querySelectorAll('tbody tr')).map(tr => Array.from(tr.children).map(txt)) : [];
  const t1 = tabMit('Einstellung');
  r.l_tabelle = !!t1 && t1.querySelectorAll('th').length === 3 && !!t1.querySelector('td code');
  r.l_tabelle_ausrichtung = !!t1 && Array.from(t1.querySelectorAll('th')).some(th => txt(th) === 'Mitte' && th.classList.contains('ta-c'));
  r.l_tabelle_pipe_maskiert = zeilen(t1).some(z => z[0] === 'a | b' && z[1] === 'Pipe maskiert' && z.length === 3);
  const brZelle = t1 ? Array.from(t1.querySelectorAll('td')).find(td => txt(td).indexOf('Zeile') === 0) : null;
  r.l_tabelle_br = !!brZelle && !!brZelle.querySelector('br') && txt(brZelle).indexOf('<br>') === -1;
  const t2 = tabMit('Spalte A');
  r.l_tabelle_ohne_aussenpipes = !!t2 && t2.querySelectorAll('th').length === 3
    && Array.from(t2.querySelectorAll('th')).some(th => txt(th) === 'Spalte B' && th.classList.contains('ta-c'));
  const z2 = zeilen(t2);
  r.l_tabelle_ungleich = z2.some(z => z[0] === 'nur eins' && z.length === 3)
    && z2.some(z => z[0] === 'a' && z.length === 3) && !!t2 && txt(t2).indexOf('d zu viel') === -1;
  r.l_tabelle_im_zitat = q('blockquote table td').some(td => txt(td) === 'eins im Zitat');
  r.l_zitat = q('blockquote').some(b => txt(b).indexOf('Zitat Ebene eins') !== -1);
  r.l_zitat_verschachtelt = q('blockquote blockquote').some(b => txt(b) === 'Zitat Ebene zwei');
  r.l_liste = q('ul > li').some(li => txt(li).indexOf('Punkt eins') === 0);
  r.l_liste_verschachtelt = q('ul > li > ul > li').some(li => txt(li).indexOf('verschachtelt zwei Spaces') === 0)
    && q('ul > li > ul > li > ul > li').some(li => txt(li) === 'Ebene drei tief')
    && q('ul > li > ul > li').some(li => txt(li) === 'vier Spaces eingerueckt');
  r.l_liste_geordnet = q('ol > li').some(li => txt(li) === 'erster Nummernpunkt');
  const liMit = (t) => q('li').filter(li => txt(li).indexOf(t) !== -1);
  const kasten = (li) => li.querySelector(':scope > input[type=checkbox], :scope > p > input[type=checkbox]');
  r.l_aufgabe = liMit('offene Aufgabe').some(li => { const k = kasten(li); return k && k.disabled && !k.checked; })
    && liMit('erledigte Aufgabe').some(li => { const k = kasten(li); return k && k.disabled && k.checked; });
  r.l_aufgabe_verschachtelt = q('li li').some(li => txt(li) === 'Unteraufgabe tief' && kasten(li) && kasten(li).disabled);
  r.l_zaun = q('pre > code').some(c => c.textContent.indexOf('def katalog_zaun(x):') !== -1);
  r.l_zaun_tilde = q('pre').some(p => p.textContent.indexOf('Tilde-Zaun Inhalt') !== -1 && p.textContent.indexOf('~~~') === -1);
  r.l_code_eingerueckt = q('pre').some(p => p.textContent.indexOf('eingerueckter Code Inhalt') !== -1);
  r.l_codespan_format = q('code').some(c => c.textContent === '[x]{.rot}') && q('code .md-c-rot').length === 0;
  r.l_trennlinie = q('hr').some(hr => hr.previousElementSibling && txt(hr.previousElementSibling).indexOf('bleibt Code.') !== -1);
  r.l_format_farbe = hat('span.md-c-rot', 'Rot');
  r.l_format_block = q('div.md-a-zentriert').some(d => txt(d) === 'Zentrierter Katalogtext');
  r.l_format_unbekannt = P.textContent.indexOf('::: {.warnung}') !== -1 && P.textContent.indexOf('Unbekannte Klasse bleibt sichtbar.') !== -1;
  r.l_bild = q('img').some(i => i.getAttribute('alt') === 'Kontrollbild' && (i.getAttribute('src') || '').indexOf('%ASSET%') !== -1);
  r.l_fussnote = q('sup').length > 0;
  r.html_als_text = P.textContent.indexOf('<b>fett per HTML</b>') !== -1 && P.textContent.indexOf('<span class="x">Spanne</span>') !== -1
    && q('b').length === 0;
  // Teile der Konflikt-Zellen (Lesesicht-Seite)
  r.__bild_format = q('img').some(i => i.getAttribute('alt') === 'Alt rot' && (i.getAttribute('src') || '').indexOf('%ASSET%') !== -1);
  const fmt = liMit('Format nach dem Kaestchen');
  r.__aufgabe_format_ok = fmt.length > 0 && fmt.every(li => !li.querySelector('input')) && fmt.some(li => !!li.querySelector('.md-c-rot'));
  r.__aufgabe_geordnet_ok = q('ol > li').some(li => txt(li).indexOf('nummerierte Aufgabe') !== -1 && !!li.querySelector('input[type=checkbox]'));
  r.__html = P.innerHTML.length;
  r.__tabellen_oben = P.querySelectorAll(':scope > table').length;
  return r;
}"""

AKTIVE = r"""() => {
  const P = document.getElementById('ro-preview');
  const boese = Array.from(P.querySelectorAll('script, iframe, svg, style, object, embed, noscript, form, frame, link, meta'))
    .map(e => e.tagName);
  const attrs = [];
  P.querySelectorAll('*').forEach(e => { for (const a of e.attributes) {
    const v = (a.value || '').trim().toLowerCase();
    if (a.name.indexOf('on') === 0 || ((a.name === 'href' || a.name === 'src') && (v.indexOf('javascript:') === 0 || v.indexOf('data:') === 0)))
      attrs.push(e.tagName + '@' + a.name); } });
  return {boese: boese, attrs: attrs, text_hat_script: P.textContent.indexOf('<script>alert(1)</script>') !== -1};
}"""

TASTEN = """(z) => {
  const cm = %s;
  const vorher = cm.getValue();
  const out = {};
  for (const [name, zeile] of Object.entries(z)) {
    cm.scrollIntoView({line: zeile, ch: 0}, 50);
    const laeufe = [];
    for (let r = 0; r < 3; r++) {
      const ts = [];
      for (let k = 0; k < 20; k++) {
        const t0 = performance.now();
        cm.replaceRange('x', {line: zeile, ch: 0});
        cm.getWrapperElement().offsetHeight; cm.display.lineDiv.getBoundingClientRect();
        ts.push(performance.now() - t0);
      }
      // die 20 eingefuegten Zeichen genau wieder entfernen (Undo-Ereignisse verschmelzen je nach
      // Browser-Takt -- gemessen: nach 'while undo' blieb der Text veraendert)
      cm.replaceRange('', {line: zeile, ch: 0}, {line: zeile, ch: 20});
      ts.sort((a, b) => a - b);
      laeufe.push({median: ts[10], p95: ts[18]});
    }
    out[name] = laeufe;
  }
  out.text_wie_vorher = cm.getValue() === vorher;
  return out;
}""" % CM


# S2: Tastenkosten **mit** dem Abgleich des Tabellen-Widgets (wie A5 „bis nach dem Abgleich"): der
# Cursor steht in der gemessenen Zeile (realistisch: in der Tabelle = Rohtext), je Taste
# `replaceRange` + Layout + `abgleichen()` + Layout. Ohne Widget-Modul (Gegenlauf) ohne Abgleich.
TASTEN_ABGLEICH = """(z) => {
  const cm = %s;
  const T = cm.state.sfxTabellen;
  const vorher = cm.getValue();
  const out = {modul: !!T};
  for (const [name, zeile] of Object.entries(z)) {
    cm.setCursor({line: zeile, ch: 0});
    if (T) T.abgleichen();
    cm.scrollIntoView({line: zeile, ch: 0}, 50);
    const laeufe = [];
    for (let r = 0; r < 3; r++) {
      const ts = [];
      for (let k = 0; k < 20; k++) {
        const t0 = performance.now();
        cm.replaceRange('x', {line: zeile, ch: 0});
        cm.getWrapperElement().offsetHeight;
        if (T) T.abgleichen();
        cm.getWrapperElement().offsetHeight; cm.display.lineDiv.getBoundingClientRect();
        ts.push(performance.now() - t0);
      }
      cm.replaceRange('', {line: zeile, ch: 0}, {line: zeile, ch: 20});
      ts.sort((a, b) => a - b);
      laeufe.push({median: ts[10], p95: ts[18]});
    }
    out[name] = laeufe;
    out[name + '_widgets'] = T ? T.marken().filter(e => e.mark.find()).length : 0;
  }
  // Abgleich ohne Aenderung (Cursor ausserhalb, 200-Zeilen-Tabelle als Widget)
  cm.setCursor({line: 1500, ch: 0});
  const leer = [];
  if (T) { T.abgleichen(); for (let k = 0; k < 20; k++) { const t0 = performance.now(); T.abgleichen(); leer.push(performance.now() - t0); } }
  leer.sort((a, b) => a - b);
  out.abgleich_leer_median = leer.length ? leer[10] : null;
  // Zeichnen: Widget der 200-Zeilen-Tabelle neu bauen (Cursor hinein und wieder hinaus)
  if (T) {
    cm.setCursor({line: 100, ch: 0}); T.abgleichen();
    cm.setCursor({line: 1500, ch: 0}); cm.scrollIntoView({line: 2, ch: 0}, 0);
    const t0 = performance.now(); T.abgleichen(); cm.getWrapperElement().offsetHeight; cm.display.lineDiv.getBoundingClientRect();
    out.widget_200_zeichnen_ms = performance.now() - t0;
  }
  out.text_wie_vorher = cm.getValue() === vorher;
  return out;
}""" % CM

WIDGETS = "() => { const t = " + CM + ".state.sfxTabellen; return t ? t.marken().filter(e => e.mark.find()).length : -1; }"
CURSOR = "() => { const c = " + CM + ".getCursor(); return [c.line, c.ch]; }"


def warte_cm(page, item_id):
    page.wait_for_function(CM_DA, timeout=20000)
    page.wait_for_function("(id) => { try { return " + CM + ".getValue() !== undefined; } catch (e) { return false; } }",
                           arg=item_id, timeout=20000)
    page.wait_for_timeout(350)


def oeffne(page, iid, editor=True):
    page.evaluate(OEFFNE, iid)
    if editor:
        warte_cm(page, iid)
    else:
        page.wait_for_timeout(500)


def fokus_ende(page):
    page.evaluate("() => { const cm = " + CM + "; cm.focus(); cm.setCursor({line: cm.lineCount() - 1, ch: cm.getLine(cm.lineCount() - 1).length}); }")


def s2_zellen(page, iid):
    s2 = {}
    oeffne(page, iid)
    if page.evaluate(DIALOG):
        page.click("#confirm-cancel")
    def setze(l, ch):
        page.evaluate("([l, c]) => { const cm = " + CM + "; cm.focus(); cm.setCursor({line: l, ch: c}); }", [l, ch])
        page.wait_for_timeout(200)
    def taste(k):
        page.keyboard.press(k)
        page.wait_for_timeout(200)
    wert = lambda: page.evaluate("() => " + CM + ".getValue()")
    sauber = lambda: not page.evaluate("async () => (await import('/ui/static/js/editor.js')).isDirty()")
    orig = page.evaluate("async (id) => (await (await fetch('/api/v1/items/' + id)).json()).body", iid)
    s2["editor_gleich_api"] = wert() == orig
    # Pfeil ab von der Leerzeile davor -> erste Tabellenzeile (2); Pfeil auf von der Leerzeile danach -> letzte (6)
    for name, start, key in (("pfeil_ab", 1, "ArrowDown"), ("pfeil_auf", 7, "ArrowUp")):
        setze(start, 0)
        e = {"widget_vorher": page.evaluate(WIDGETS)}
        taste(key)
        e["cursor"] = page.evaluate(CURSOR)
        e["widget_nachher"] = page.evaluate(WIDGETS)
        s2[name] = e
    # Klick auf die Zelle „Anzahl der Versuche" (echte Maus) -> Cursor [5,14], Rohtext, Fokus; „Z" nur dort
    setze(8, 0)
    k = {"widget_vorher": page.evaluate(WIDGETS)}
    box = page.evaluate("""() => { const td = Array.from(document.querySelectorAll('#detail-editor .sfx-tabelle td'))
        .find(t => t.textContent.trim() === 'Anzahl der Versuche'); if (!td) return null;
        const r = td.getBoundingClientRect(); return {x: r.x, y: r.y, w: r.width, h: r.height}; }""")
    k["zelle_gefunden"] = box is not None
    if box:
        page.mouse.click(box["x"] + box["w"] * 0.6, box["y"] + box["h"] / 2)
        page.wait_for_timeout(250)
        k["cursor"] = page.evaluate(CURSOR)
        k["soll"] = [5, orig.split("\n")[5].index("Anzahl der Versuche")]
        k["widget_nachher"] = page.evaluate(WIDGETS)
        k["roh_sichtbar"] = page.evaluate("() => document.querySelectorAll('#detail-editor .sfx-tabelle').length === 0")
        k["fokus"] = page.evaluate("() => " + CM + ".hasFocus()")
        page.keyboard.type("Z")
        page.wait_for_timeout(150)
        i = orig.index("Anzahl der Versuche")
        k["nur_die_zelle"] = wert() == orig[:i] + "Z" + orig[i:]
        taste("Control+z")
        k["zurueck"] = wert() == orig and sauber()
    s2["klick"] = k
    # Undo/Redo ueber Widget-Wechsel: das Ein-/Austreten schreibt keine Historie
    setze(8, 0)
    u = {"historie_vorher": page.evaluate("() => " + CM + ".historySize()")}
    for key in ("ArrowUp", "ArrowUp", "ArrowDown", "ArrowDown", "ArrowUp", "ArrowDown"):
        taste(key)
    u["historie_nach_wechseln"] = page.evaluate("() => " + CM + ".historySize()")
    u["text_nach_wechseln"] = wert() == orig
    setze(5, orig.split("\n")[5].index("Anzahl der Versuche"))
    page.keyboard.type("Q")
    page.wait_for_timeout(150)
    for _ in range(3):
        taste("ArrowDown")
    u["cursor_draussen"] = page.evaluate(CURSOR)
    u["widget_mit_q"] = page.evaluate("""() => Array.from(document.querySelectorAll('#detail-editor .sfx-tabelle td'))
        .some(t => t.textContent.trim() === 'QAnzahl der Versuche')""")
    taste("Control+z")
    u["undo_ursprung"] = wert() == orig and sauber()
    taste("Control+y")
    u["redo_q"] = "QAnzahl der Versuche" in wert()
    taste("Control+z")
    u["ende_sauber"] = wert() == orig and sauber()
    s2["undo"] = u
    # Kopieren ueber die Widget-Grenze: Auswahl Zeile 0 bis Ende (Widget bleibt sichtbar) -> Quelle
    setze(0, 0)
    c = {"widget_vorher": page.evaluate(WIDGETS)}
    page.evaluate("""() => { window.__kopie = null; document.addEventListener('copy', (e) => { const t = e.target;
        window.__kopie = (t && typeof t.value === 'string') ? t.value.slice(t.selectionStart, t.selectionEnd) : String(getSelection()); },
        {capture: true, once: true}); }""")
    page.evaluate("() => { const cm = " + CM + "; const n = cm.lineCount() - 1; cm.setSelection({line: 0, ch: 0}, {line: n, ch: cm.getLine(n).length}); }")
    page.wait_for_timeout(200)
    c["widget_waehrend_auswahl"] = page.evaluate(WIDGETS)
    c["auswahl_gleich_quelle"] = page.evaluate("() => " + CM + ".getSelection()") == orig
    page.keyboard.press("Control+c")
    page.wait_for_timeout(200)
    c["kopie_gleich_quelle"] = page.evaluate("() => window.__kopie") == orig
    page.screenshot(path=str(Path(AUFTRAG["shots"]) / ("%s_s2_auswahl.png" % AUFTRAG["browser"])))
    setze(0, 0)
    c["ende_sauber"] = wert() == orig and sauber()
    s2["kopieren"] = c
    page.screenshot(path=str(Path(AUFTRAG["shots"]) / ("%s_s2_widget.png" % AUFTRAG["browser"])))
    return s2


#: Randfaelle (Information, keine Zelle): Liste/Ueberschrift davor, zwei Tabellen ohne Leerzeile (= eine),
#: ungleiche Zeilen, Aufgabe im Koerper, Tabelle im ```-Zaun / ~~~ / :::-Block, sehr breite Tabelle,
#: Tabelle am Dateiende ohne Newline. Soll: jedes Widget = die oberste Tabelle der Lesesicht, gleiche Reihenfolge.
S2_RAND = ("# Rand\n- Liste davor\n| a | b |\n|---|---|\n| 1 | 2 |\n- [ ] aufgabe | in tabelle\n\n"
           "## Ueberschrift\n| h | i |\n|---|---|\n| 3 | 4 |\n\n"
           "| erste | x |\n|---|---|\n| 5 | 6 |\n| zweite | y |\n|---|---|\n| 7 | 8 |\n\n"
           "Zeilen ungleich | b | c\n--- | ---\nnur | zwei | drei | vier\n\n"
           "```\n| im | zaun |\n|---|---|\n```\n\n~~~\n| im | tilde |\n|---|---|\n~~~\n\n"
           "::: {.zentriert}\n| im | block |\n|---|---|\n:::\n\n"
           "| breit | " + "W" * 400 + " |\n|---|---|\n| x | y |\n\n"
           "| e | f |\n|---|---|\n| Ende | ohne Newline |")


def s2_rand(page):
    neu = page.evaluate("""async (body) => { const r = await fetch('/api/v1/items', {method: 'POST', credentials: 'same-origin',
        headers: {'Content-Type': 'application/json', 'X-CSRF-Token': sessionStorage.getItem('sfx:csrf')},
        body: JSON.stringify({space: 'alpha', type: 'note', title: 'S2 Rand', body: body})}); return {status: r.status, item: await r.json()}; }""", S2_RAND)
    out = {"anlegen": neu["status"]}
    if neu["status"] not in (200, 201):
        return out
    iid = neu["item"]["id"]
    oeffne(page, iid)
    page.evaluate("() => { const cm = " + CM + "; cm.focus(); cm.setCursor({line: 0, ch: 0}); }")
    page.wait_for_timeout(400)
    out.update(page.evaluate("""async ([id, body]) => {
      const cm = %s;
      const M = await import('/ui/static/js/markdown.js');
      const E = await import('/ui/static/js/editor.js');
      const T = cm.state.sfxTabellen;
      const marken = T ? T.marken().filter(e => e.mark.find()) : [];
      const widgets = marken.map(e => e.mark.replacedWith.querySelector('table').outerHTML);
      const tpl = document.createElement('template');
      tpl.innerHTML = M.markdownToHtml(body, {itemId: id, assetIds: []});
      const lese = Array.from(tpl.content.children).filter(x => x.tagName === 'TABLE').map(x => x.outerHTML);
      const breit = Array.from(document.querySelectorAll('#detail-editor .sfx-tabelle')).find(w => w.textContent.indexOf('WWWW') !== -1);
      return {widgets: widgets.length, lesesicht_oben: lese.length, gleich_lesesicht: JSON.stringify(widgets) === JSON.stringify(lese),
              zeilen: marken.map(e => [e.mark.find().from.line, e.mark.find().to.line]),
              editor_gleich_api: cm.getValue() === body, sauber: !E.isDirty(),
              seite_breiter_als_fenster: document.documentElement.scrollWidth > window.innerWidth,
              breites_widget_scrollt: !!breit && breit.scrollWidth > breit.clientWidth,
              aufgaben_kaestchen: document.querySelectorAll('#detail-editor input.sfx-todo').length};
    }""" % CM, [iid, S2_RAND]))
    # Pfeil ab ins letzte Widget (Tabelle am Dateiende ohne Newline)
    n = page.evaluate("() => " + CM + ".lineCount()")
    page.evaluate("([l]) => { const cm = " + CM + "; cm.focus(); cm.setCursor({line: l, ch: 0}); }", [n - 4])
    page.wait_for_timeout(200)
    page.keyboard.press("ArrowDown")
    page.wait_for_timeout(200)
    out["ende_pfeil_cursor"] = page.evaluate(CURSOR)
    out["ende_pfeil_soll"] = [n - 3, 0]
    out["editor_gleich_api_danach"] = page.evaluate("(b) => " + CM + ".getValue() === b", S2_RAND)
    page.screenshot(path=str(Path(AUFTRAG["shots"]) / ("%s_s2_rand.png" % AUFTRAG["browser"])))
    return out


def main():
    ids = AUFTRAG["ids"]
    out = {"browser": AUFTRAG["browser"], "bytes": {}, "dialoge_nativ": [], "seitenfehler": []}
    shots = Path(AUFTRAG["shots"])
    shots.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = getattr(p, AUFTRAG["browser"]).launch()
        ctx = browser.new_context(ignore_https_errors=True, viewport={"width": 1600, "height": 1000})
        ctx.add_init_script("localStorage.setItem('sfx:film:gesehen','4.0.0')")
        page = ctx.new_page()
        out["browser_version"] = browser.version
        page.on("pageerror", lambda e: out["seitenfehler"].append(str(e)[:200]))
        def _dlg(d):
            out["dialoge_nativ"].append(d.type + ":" + d.message[:60])
            d.dismiss()
        page.on("dialog", _dlg)
        schreib = []
        page.on("request", lambda r: r.method in ("PATCH", "POST", "PUT", "DELETE") and "/api/v1/items" in r.url
                and schreib.append(r.method + " " + r.url.split("/api/v1/")[1]))
        login(page)

        # -- V1/V2: jedes Fixture oeffnen (CM schon geladen), nichts tun, Strg+S, tippen+loeschen --
        alpha = [k.split(":", 1)[1] for k in ids if k.startswith("alpha:")]
        oeffne(page, ids["alpha:11_tabelle_einfach"])
        for name in alpha:
            iid = ids["alpha:" + name]
            oeffne(page, iid)
            if page.evaluate(DIALOG):
                page.click("#confirm-cancel")
                page.wait_for_timeout(200)
            m = page.evaluate(MESSE, iid)
            out.setdefault("api_bodies", {})[name] = m.pop("api_body")
            fokus_ende(page)
            n0 = len(schreib)
            page.keyboard.press("Control+s")
            page.wait_for_timeout(300)
            m["strg_s_writes"] = len(schreib) - n0
            page.keyboard.type("x")
            page.keyboard.press("Backspace")
            page.wait_for_timeout(150)
            m["dirty_nach_tippen_loeschen"] = page.evaluate("async () => (await import('/ui/static/js/editor.js')).isDirty()")
            out["bytes"][name] = m

        # -- Katalog im Editor ---------------------------------------------------------------------
        oeffne(page, ids["alpha:28_katalog"])
        page.wait_for_timeout(500)
        out["editor"] = page.evaluate(EDITOR_ZEILEN, AUFTRAG["anker"])
        out["kontrast"] = page.evaluate(KONTRAST)
        page.evaluate("() => " + CM + ".scrollTo(0, 0)")
        page.wait_for_timeout(200)
        page.screenshot(path=str(shots / ("%s_editor_katalog_oben.png" % AUFTRAG["browser"])))
        page.evaluate("() => { const cm = " + CM + "; let n = 0; for (let i = 0; i < cm.lineCount(); i++) if (cm.getLine(i).indexOf('Spalte A |') === 0) n = i; cm.scrollIntoView({line: n, ch: 0}, 300); }")
        page.wait_for_timeout(200)
        page.screenshot(path=str(shots / ("%s_editor_katalog_mitte.png" % AUFTRAG["browser"])))

        # -- Katalog + XSS in der Lesesicht (fremder Space) ------------------------------------------
        oeffne(page, ids["beta:28_katalog"], editor=False)
        page.wait_for_function("() => document.getElementById('ro-preview').innerHTML.length > 100", timeout=20000)
        page.wait_for_timeout(500)
        out["lesesicht"] = page.evaluate(LESESICHT.replace("%ASSET%", AUFTRAG["asset_id"]))
        page.screenshot(path=str(shots / ("%s_lesesicht_katalog.png" % AUFTRAG["browser"])), full_page=True)
        oeffne(page, ids["beta:20_xss"], editor=False)
        page.wait_for_function("() => document.getElementById('ro-preview').innerHTML.length > 50", timeout=20000)
        page.wait_for_timeout(1500)       # einem onerror/onload Zeit geben, zu feuern
        out["aktive"] = page.evaluate(AKTIVE)
        out["aktive"]["dialoge_nativ"] = list(out["dialoge_nativ"])

        # -- S2: Tabellen-Widget an 11_tabelle_einfach (Zeilen: 0 Einleitung, 1 leer, 2 Kopf, 3 Trenner,
        #    4-6 Koerper, 7 leer, 8 Schluss ohne Newline). Jede Zelle verlangt das Widget als Vorbedingung.
        out["s2"] = s2_zellen(page, ids["alpha:11_tabelle_einfach"])
        out["s2_rand"] = s2_rand(page)

        # -- V3: ein Zeichen in eine Tabellenzelle; ein Zeichen am Ende einer Datei ohne Newline ------
        v3 = {}
        for name, finde in (("11_tabelle_einfach", "Anzahl der Versuche"), ("22_ohne_newline", None)):
            iid = ids["alpha:" + name]
            oeffne(page, iid)
            if page.evaluate(DIALOG):
                page.click("#confirm-cancel")
            vor = page.evaluate("async (id) => (await (await fetch('/api/v1/items/' + id)).json())", iid)
            if finde:
                pos = page.evaluate("(t) => { const cm = " + CM + "; const i = cm.getValue().indexOf(t); cm.focus(); cm.setCursor(cm.posFromIndex(i)); return i; }", finde)
            else:
                fokus_ende(page)
                pos = len(vor["body"])
            page.keyboard.type("Z")
            n0 = len(schreib)
            page.keyboard.press("Control+s")
            page.wait_for_function("() => document.getElementById('save-button').disabled", timeout=10000)
            page.wait_for_timeout(300)
            nach = page.evaluate("async (id) => (await (await fetch('/api/v1/items/' + id)).json())", iid)
            v3[name] = {"index": pos, "writes": len(schreib) - n0,
                        "nur_das_zeichen": nach["body"] == vor["body"][:pos] + "Z" + vor["body"][pos:],
                        "endet_wie_vorher": nach["body"].endswith("\n") == vor["body"].endswith("\n"),
                        "version": [vor["version"], nach["version"]]}
        out["v3"] = v3

        # -- Tastenkosten (Rohdaten fuer S2: Basis + 2 ms), 2.000-Zeilen-Notiz -------------------------
        oeffne(page, ids["alpha:27_gross"])
        page.wait_for_timeout(500)
        out["tastenkosten"] = page.evaluate(TASTEN, {"absatzzeile": 1500, "tabellenzeile": 100})
        out["tastenkosten_sauber_danach"] = not page.evaluate("async () => (await import('/ui/static/js/editor.js')).isDirty()")
        out["tastenkosten_abgleich"] = page.evaluate(TASTEN_ABGLEICH, {"absatzzeile": 1500, "tabellenzeile": 100})
        out["tastenkosten_abgleich_sauber_danach"] = not page.evaluate("async () => (await import('/ui/static/js/editor.js')).isDirty()")

        # -- Entwurf (V7, F7) -----------------------------------------------------------------------
        def entwuerfe_weg():
            page.evaluate("() => Object.keys(sessionStorage).filter(k => k.indexOf('sfx:draft:') === 0).forEach(k => sessionStorage.removeItem(k))")
        def neu_laden():
            page.reload(wait_until="domcontentloaded")
            page.wait_for_selector("#shell", timeout=30000)
            page.wait_for_timeout(1000)
        A, B, L = ids["alpha:15_aufgaben"], ids["alpha:16_code"], ids["alpha:14_listen_verschachtelt"]
        entwurf = {}
        oeffne(page, ids["alpha:12_tabelle_ki"])
        entwuerfe_weg()
        oeffne(page, B)
        entwurf["oeffnen"] = {"schluessel_nach_oeffnen": page.evaluate("(id) => sessionStorage.getItem('sfx:draft:' + id) !== null", B)}
        # (1) A tippen, neu laden, **B zuerst**, dann A
        entwuerfe_weg()
        oeffne(page, A)
        fokus_ende(page)
        page.keyboard.type("ENTWURF-1")
        page.wait_for_timeout(400)
        e1 = {"entwurf_vor_neuladen": page.evaluate("(id) => (sessionStorage.getItem('sfx:draft:' + id) || '').indexOf('ENTWURF-1') !== -1", A)}
        neu_laden()
        oeffne(page, B)
        oeffne(page, A)
        page.wait_for_timeout(400)
        e1["dialog"] = page.evaluate(DIALOG)
        # S1: solange die Rueckfrage offen ist, liegt der Entwurf noch im Speicher (ein Neuladen jetzt
        # verloere sonst ihn) -- die Szene, in der die Ursprungspruefung die einzige Schranke ist.
        e1["entwurf_waehrend_dialog"] = page.evaluate("(id) => (sessionStorage.getItem('sfx:draft:' + id) || '').indexOf('ENTWURF-1') !== -1", A)
        if e1["dialog"]:
            e1["dialog_text"] = page.evaluate("() => document.getElementById('confirm-message').textContent")
            page.click("#confirm-ok")
            page.wait_for_timeout(400)
        e1["editor_hat_entwurf"] = "ENTWURF-1" in page.evaluate("async () => (await import('/ui/static/js/editor.js')).getBody()")
        entwurf["ueberlebt"] = e1
        # Kontrolle (Anhang A2 Fall 2): derselbe Ablauf, aber **A zuerst** -- hier ueberlebt der Entwurf
        # heute. Beweist, dass die Zelle einen ueberlebenden Entwurf erkennen kann (rot ist kein Messfehler).
        entwuerfe_weg()
        neu_laden()
        oeffne(page, B)
        oeffne(page, A)
        fokus_ende(page)
        page.keyboard.type("ENTWURF-2")
        page.wait_for_timeout(400)
        neu_laden()
        oeffne(page, A, editor=False)
        page.wait_for_timeout(1000)
        k = {"dialog": page.evaluate(DIALOG)}
        if k["dialog"]:
            page.click("#confirm-ok")
            page.wait_for_timeout(400)
        warte_cm(page, A)
        k["editor_hat_entwurf"] = "ENTWURF-2" in page.evaluate("async () => (await import('/ui/static/js/editor.js')).getBody()")
        entwurf["kontrolle_a_zuerst"] = k
        entwuerfe_weg()
        neu_laden()
        # (2) L tippen, neu laden, fremde Aenderung (zweiter Client), **L zuerst**, Dialog bestaetigen, Strg+S
        oeffne(page, B)
        oeffne(page, L)
        fokus_ende(page)
        page.keyboard.type("ENTWURF-ALT")
        page.wait_for_timeout(400)
        neu_laden()
        fremd = "Fremde Fassung vom KI-Client\n"
        e2 = {"fremd": page.evaluate("""async ([id, neu]) => {
          const it = await (await fetch('/api/v1/items/' + id)).json();
          const r = await fetch('/api/v1/items/' + id, {method: 'PATCH', credentials: 'same-origin',
            headers: {'Content-Type': 'application/json', 'X-CSRF-Token': sessionStorage.getItem('sfx:csrf')},
            body: JSON.stringify({version: it.version, body: neu})});
          return {status: r.status, version: (await r.json()).version, alt: it.version};
        }""", [L, fremd])}
        oeffne(page, L, editor=False)
        page.wait_for_timeout(1200)
        # S1: wird der veraltete Entwurf **angeboten** (Konfliktdialog mit beiden Versionen)? Eine gruene
        # Zelle zaehlt nur dann -- ein verschwundener Entwurf liesse die fremde Fassung auch stehen (A13.7).
        e2["konflikt_dialog"] = page.evaluate("() => !document.getElementById('conflict-dialog').hidden")
        e2["konflikt_text"] = page.evaluate("() => document.getElementById('conflict-message').textContent")
        e2["konflikt_fokus"] = page.evaluate("() => document.activeElement && document.activeElement.id")
        page.screenshot(path=str(shots / ("%s_entwurf_veraltet.png" % AUFTRAG["browser"])))
        e2["dialog"] = page.evaluate(DIALOG)
        if e2["dialog"]:
            e2["dialog_text"] = page.evaluate("() => document.getElementById('confirm-message').textContent")
            page.click("#confirm-ok")
            page.wait_for_timeout(500)
        warte_cm(page, L)
        e2["dirty"] = page.evaluate("async () => (await import('/ui/static/js/editor.js')).isDirty()")
        e2["editor_hat_entwurf"] = "ENTWURF-ALT" in page.evaluate("async () => (await import('/ui/static/js/editor.js')).getBody()")
        if e2["dirty"]:
            page.evaluate("() => " + CM + ".focus()")
            page.keyboard.press("Control+s")
            page.wait_for_timeout(1500)
        # Strg+S aus dem veralteten Entwurf laeuft in den Konflikt; dann der vorhandene Weg
        # „Entwurf als neues Item anlegen" (`conflict-save-as-new`) -- der Entwurf geht nicht verloren.
        e2["konflikt_nach_speichern"] = page.evaluate("() => !document.getElementById('conflict-dialog').hidden")
        if e2["konflikt_nach_speichern"]:
            page.click("#conflict-save-as-new")
            # bis der Editor das neue Item zeigt (afterWrite laedt Liste + Uebersicht; Firefox braucht
            # dafuer gemessen laenger als 1,5 s) -- hoechstens 10 s, sonst steht `anders: false` im Beleg
            page.evaluate("""async (alt) => {
              const S = (await import('/ui/static/js/state.js')).state;
              for (let i = 0; i < 100; i++) {
                if (S.editingSnapshot && S.editingSnapshot.id !== alt) return true;
                await new Promise((r) => setTimeout(r, 100));
              }
              return false;
            }""", L)
            page.wait_for_timeout(300)
            e2["neu"] = page.evaluate("""async (alt) => {
              const S = (await import('/ui/static/js/state.js')).state;
              const id = S.editingSnapshot && S.editingSnapshot.id;
              if (!id || id === alt) return {anders: false};
              const it = await (await fetch('/api/v1/items/' + id)).json();
              return {anders: true, hat_entwurf: it.body.indexOf('ENTWURF-ALT') !== -1, version: it.version};
            }""", L)
        e2["entwurf_nach_entscheidung"] = page.evaluate("(id) => sessionStorage.getItem('sfx:draft:' + id) !== null", L)
        nach = page.evaluate("async (id) => (await (await fetch('/api/v1/items/' + id)).json())", L)
        e2["server_version"] = nach["version"]
        e2["fremde_fassung_steht"] = nach["body"] == fremd
        e2["server_hat_entwurf"] = "ENTWURF-ALT" in nach["body"]
        entwurf["kein_stilles_zurueck"] = e2
        out["entwurf"] = entwurf
        out["schreib_requests"] = schreib
        browser.close()
    Path(AUFTRAG["result"]).write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")


main()
'''

#: Die Ankertexte der Editorzeilen (eine Zeile je Anker, im Katalog eindeutig).
ANKER = [
    "# Katalog Ueberschrift Eins", "##### Katalog Ueberschrift Fuenf", "###### Katalog Ueberschrift Sechs",
    "Setext Katalog Eins", "Durchgestrichen:", "> Zitat Ebene eins", "def katalog_zaun(x):",
    "Tilde-Zaun Inhalt", "    eingerueckter Code Inhalt", "- [ ] offene Aufgabe", "  - [ ] Unteraufgabe tief",
    "1. [ ] nummerierte Aufgabe", "- [x]{.rot} Format nach dem Kaestchen", "- Punkt eins",
    "  - verschachtelt zwei Spaces", "[Rot]{.rot} und", "::: {.zentriert}", "::: {.warnung}",
    "Code mit Format:", "| Einstellung | Bedeutung", "Bild mit Format:",
]


def browser_skript() -> str:
    kopf = b14.BROWSER_SKILL.split("\ndef main():\n", 1)[0]
    return kopf + BROWSER_MAIN


def ein_browser(browser: str, creds: dict) -> dict:
    fixtures = fixtures_fuer_lauf()
    saat = seed(fixtures)
    ids, dateien = saat["ids"], saat["dateien"]
    vorher = {k: Path(v).read_bytes() for k, v in dateien.items()}
    statische_kopie()
    b14.PORT = b14._freier_port()
    b14.BASE = "https://127.0.0.1:%d" % b14.PORT
    resultat = b14.WEGWERF_ROOT / ("ed41-roh-%s-%d.json" % (browser, b14.PID))
    skript = b14.WEGWERF_ROOT / ("browser_ed41_%d.py" % b14.PID)
    try:
        b14._serve()
        auftrag = {
            "base": b14.BASE, "space": b14.SPACE, "password": creds["password"], "secret": creds["secret"],
            "repo_root": str(REPO_ROOT), "auth_db": str(b14.AUTH_DB), "result": str(resultat),
            "wachser_space": "beta", "extra_items": 0, "spaces": ["alpha", "beta"], "browser": browser,
            "ids": ids, "anker": ANKER, "asset_id": spec.ASSET_ID,
            "shots": str(SHOTS / (GEGENLAUF or "basis")),
        }
        b14.AUFTRAG_DATEI.write_text(json.dumps(auftrag), encoding="utf-8")
        skript.write_text(browser_skript(), encoding="utf-8")
        proc = subprocess.run([str(E2E), str(skript), str(b14.AUFTRAG_DATEI)], cwd=str(REPO_ROOT),
                              capture_output=True, text=True, timeout=900)
        if proc.returncode != 0:
            print(proc.stdout[-3000:], proc.stderr[-5000:], file=sys.stderr)
            raise SystemExit("Browser-Teil (%s) fehlgeschlagen" % browser)
    finally:
        b14._stop()
        for f in (b14.AUFTRAG_DATEI, skript):       # der Auftrag traegt Passwort + TOTP-Seed
            f.unlink(missing_ok=True)
    roh = json.loads(resultat.read_text(encoding="utf-8"))
    resultat.unlink()
    nachher = {k: Path(v).read_bytes() for k, v in dateien.items()}

    # Platte + Saat-Treue (Information, nicht Zelle): Fixture-Bytes -> Datei-Body -> API-Body
    api = roh.pop("api_bodies")
    beschrieben = {"alpha:11_tabelle_einfach", "alpha:22_ohne_newline", "alpha:14_listen_verschachtelt"}
    treue = {}
    for name, text in fixtures.items():
        treue[name] = {"bytes": len(text.encode("utf-8")),
                       "datei_gleich_fixture": body_bytes_vorher(vorher["alpha:" + name]) == text.encode("utf-8"),
                       "api_gleich_fixture": api.get(name) == text,
                       "cr_fixture": text.count("\r"), "cr_api": (api.get(name) or "").count("\r")}
    roh["saat_treue"] = treue
    roh["platte_unveraendert"] = {k: vorher[k] == nachher[k] for k in dateien if k not in beschrieben}
    # V6 (Information): welche Frontmatter-Zeilen aendert ein echter Write?
    v6 = {}
    for k in ("alpha:11_tabelle_einfach", "alpha:22_ohne_newline"):
        alt = set(frontmatter_bytes_aus(vorher[k]).decode().splitlines())
        neu = set(frontmatter_bytes(dateien[k]).decode().splitlines())
        v6[k.split(":", 1)[1]] = {"weg": sorted(x.split(":", 1)[0] for x in alt - neu),
                                   "neu": sorted(x.split(":", 1)[0] for x in neu - alt)}
        b_alt, b_neu = body_bytes_vorher(vorher[k]), body_bytes(dateien[k])
        v6[k.split(":", 1)[1]]["datei_body_nur_ein_byte_mehr"] = len(b_neu) == len(b_alt) + 1
    roh["v6_frontmatter"] = v6
    return roh


def body_bytes_vorher(roh: bytes) -> bytes:
    return roh.split(b"\n---\n", 1)[1]


def frontmatter_bytes_aus(roh: bytes) -> bytes:
    return roh.split(b"\n---\n", 1)[0]


def _spans(e: dict | None, klasse: str) -> list:
    return [s for s in (e or {}).get("spans", []) if klasse in s["k"].split()]


def zellen(roh: dict) -> dict:
    L, E = roh["lesesicht"], roh["editor"]
    z = {k: bool(v) for k, v in L.items() if not k.startswith("__")}
    akt = roh["aktive"]
    z["keine_aktiven"] = not akt["boese"] and not akt["attrs"] and not akt["dialoge_nativ"] and akt["text_hat_script"]

    z["e_ueberschrift"] = bool(_spans(E["# Katalog Ueberschrift Eins"], "cm-header-1"))
    z["e_ueberschrift_h5_h6"] = bool(_spans(E["##### Katalog Ueberschrift Fuenf"], "cm-header-5")) and bool(
        _spans(E["###### Katalog Ueberschrift Sechs"], "cm-header-6"))
    z["e_zitat"] = bool(_spans(E["> Zitat Ebene eins"], "cm-quote"))
    z["e_zaun"] = bool(_spans(E["def katalog_zaun(x):"], "cm-comment"))
    z["e_aufgabe"] = E["- [ ] offene Aufgabe"]["todo"] == 1 and E["  - [ ] Unteraufgabe tief"]["todo"] == 1
    z["e_format_farbe"] = any(s["t"] == "Rot" for s in _spans(E["[Rot]{.rot} und"], "cm-md-c-rot"))
    z["e_block_bekannt_versteckt"] = E["::: {.zentriert}"]["sichtbar"].strip() == ""
    z["e_durchgestrichen"] = bool(_spans(E["Durchgestrichen:"], "cm-strikethrough"))
    # S2: so viele Widgets wie oberste Tabellen der Lesesicht (Katalog: 2; die Tabelle im Zitat bleibt in
    # beiden Sichten Rohtext), und mit der Tabelle im Bild steht eine echte <table> im Editor-DOM.
    z["tabelle_widget"] = (E["__tabellen_im_editor"] > 0 and E["__widget_marken"] > 0
                           and E["__widget_marken"] == L["__tabellen_oben"])
    z["listenzeichen"] = all(
        any(s["vis"] == "visible" for s in _spans(E[a], "cm-formatting-list"))
        for a in ("- Punkt eins", "  - verschachtelt zwei Spaces"))
    kl = roh["kontrast"]["klassen"]
    z["kontrast"] = bool(kl) and all(v["kontrast"] >= 4.5 for v in kl.values())

    # F4a-f: gruen nur, wenn beide Sichten das Ziel zeigen
    z["konflikt_a_block_unbekannt"] = E["::: {.warnung}"]["sichtbar"].strip() == "::: {.warnung}" and L["l_format_unbekannt"]
    z["konflikt_b_code_format"] = not _spans(E["Code mit Format:"], "cm-md-c-rot") and L["l_codespan_format"]
    z["konflikt_c_bild_format"] = bool(L["__bild_format"]) and L["l_bild"]
    z["konflikt_d_aufgabe_format"] = E["- [x]{.rot} Format nach dem Kaestchen"]["todo"] == 0 and L["__aufgabe_format_ok"]
    z["konflikt_e_aufgabe_geordnet"] = E["1. [ ] nummerierte Aufgabe"]["todo"] == 1 and L["__aufgabe_geordnet_ok"]
    editor_f = (bool(_spans(E["Setext Katalog Eins"], "cm-header-1")) and bool(_spans(E["Tilde-Zaun Inhalt"], "cm-comment"))
                and bool(_spans(E["    eingerueckter Code Inhalt"], "cm-comment")))
    z["konflikt_f_setext_code"] = editor_f and L["l_setext"] and L["l_zaun_tilde"] and L["l_code_eingerueckt"]

    b = roh["bytes"]
    z["bytes_gleich"] = (all(m["gleich"] and not m["dirty"] and m["speichern_aus"] and m["strg_s_writes"] == 0
                             and not m["dirty_nach_tippen_loeschen"] for m in b.values())
                         and all(roh["platte_unveraendert"].values()))
    v3 = roh["v3"]
    z["bytes_zelle"] = v3["11_tabelle_einfach"]["nur_das_zeichen"] and v3["11_tabelle_einfach"]["writes"] == 1
    z["bytes_ohne_newline"] = (v3["22_ohne_newline"]["nur_das_zeichen"] and v3["22_ohne_newline"]["endet_wie_vorher"]
                               and v3["22_ohne_newline"]["writes"] == 1)
    en = roh["entwurf"]
    z["oeffnen_schreibt_keinen_entwurf"] = not en["oeffnen"]["schluessel_nach_oeffnen"]
    u = en["ueberlebt"]
    z["entwurf_ueberlebt_neuladen"] = u["entwurf_vor_neuladen"] and u["entwurf_waehrend_dialog"] and u["editor_hat_entwurf"]
    k = en["kein_stilles_zurueck"]
    # S1 (A13.7): gruen nur, wenn die fremde Fassung steht **und** der veraltete Entwurf angeboten wurde
    # (Dialog nennt beide Versionen) **und** er als neues Item erhalten blieb.
    angeboten = (k["konflikt_dialog"] and ("v%s" % k["fremd"]["alt"]) in k["konflikt_text"]
                 and ("v%s" % k["fremd"]["version"]) in k["konflikt_text"])
    z["kein_stilles_zurueck"] = (k["fremd"]["status"] == 200 and k["fremde_fassung_steht"] and angeboten
                                 and bool(k.get("neu", {}).get("hat_entwurf")))
    s2 = roh["s2"]
    z["pfeil_erste_zeile"] = (s2["pfeil_ab"]["widget_vorher"] >= 1 and s2["pfeil_ab"]["cursor"] == [2, 0]
                              and s2["pfeil_ab"]["widget_nachher"] == 0)
    z["pfeil_letzte_zeile"] = (s2["pfeil_auf"]["widget_vorher"] >= 1 and s2["pfeil_auf"]["cursor"] == [6, 0]
                               and s2["pfeil_auf"]["widget_nachher"] == 0)
    k = s2["klick"]
    z["klick_zelle"] = (k["widget_vorher"] >= 1 and k["zelle_gefunden"] and k["cursor"] == k["soll"]
                        and k["widget_nachher"] == 0 and k["roh_sichtbar"] and k["fokus"] and k["nur_die_zelle"]
                        and k["zurueck"])
    u = s2["undo"]
    z["undo"] = (u["historie_nach_wechseln"] == u["historie_vorher"] and u["text_nach_wechseln"]
                 and u["widget_mit_q"] and u["undo_ursprung"] and u["redo_q"] and u["ende_sauber"])
    c = s2["kopieren"]
    z["kopieren_quelle"] = (c["widget_vorher"] >= 1 and c["widget_waehrend_auswahl"] >= 1 and c["auswahl_gleich_quelle"]
                            and c["kopie_gleich_quelle"] and c["ende_sauber"])
    fehlt = set(spec.ZELLEN) - set(z)
    extra = set(z) - set(spec.ZELLEN)
    if fehlt or extra:
        raise SystemExit("Zellen passen nicht zur Spec: fehlt %s, extra %s" % (sorted(fehlt), sorted(extra)))
    return {n: z[n] for n in spec.ZELLEN}


def main() -> int:
    if not E2E.exists():
        raise SystemExit("Playwright-venv fehlt: %s" % E2E)
    creds = b14._setup()
    beleg = {"plan": "docs/concepts/phase10_5_editor_4_1_plan.md §5 " + spec.STAND, "stand": spec.STAND,
             "referenz": RESULT.name, "gegenlauf": GEGENLAUF,
             "fixtures": len(spec.alle_fixtures()), "browser": {}}
    try:
        for br in BROWSERS:
            roh = ein_browser(br, creds)
            roh["zellen"] = zellen(roh)
            roh["rot"] = [n for n, v in roh["zellen"].items() if not v]
            roh["abweichungen"] = [n for n, v in roh["zellen"].items() if v != spec.ERWARTET[spec.STAND][n]]
            beleg["browser"][br] = roh
            print(br, roh.get("browser_version"), "rot:", len(roh["rot"]), "abweichend:", roh["abweichungen"],
                  file=sys.stderr)
    finally:
        for p in (STATIC_KOPIE, b14.CRED_DIR, b14.DATA_ROOT):
            shutil.rmtree(p, ignore_errors=True)
        for p in (FIXTURE_JSON, IDS_JSON, b14.AUTH_DB, b14.TLS_KEY, b14.TLS_CERT):
            Path(p).unlink(missing_ok=True)
    if GEGENLAUF:
        basis = json.loads(RESULT.read_text(encoding="utf-8"))
        for br, roh in beleg["browser"].items():
            alt = basis["browser"][br]["zellen"]
            roh["gekippt"] = sorted(n for n in roh["zellen"] if roh["zellen"][n] != alt[n])
        beleg["kippt_soll"] = sorted(spec.GEGENLAEUFE[GEGENLAUF]["kippt"])
        beleg["kippt_genau"] = all(r["gekippt"] == beleg["kippt_soll"] for r in beleg["browser"].values())
        ziel = HIER / ("p105_ed41_darstellung_gegenlauf_%s.json" % GEGENLAUF)
    elif BROWSER == "beide":
        ziel = RESULT
    else:
        # Ein Ein-Browser-Lauf ist Entwicklungshilfe, kein Beleg: er darf den Zwei-Browser-Beleg
        # nicht ueberschreiben.
        ziel = Path("/tmp") / ("p105_ed41_darstellung_%s.json" % BROWSER)
    ziel.write_text(json.dumps(beleg, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print("BELEG:", ziel.name, {br: r["rot"] for br, r in beleg["browser"].items()})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
