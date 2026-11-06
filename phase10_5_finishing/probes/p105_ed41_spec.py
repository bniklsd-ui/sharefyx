#!/usr/bin/env python3
"""Editor 4.1, Schritt S0 — Korpus, Zellen und Gegenlaeufe der Darstellungs-Probe (eine Quelle).

Plan: `docs/concepts/phase10_5_editor_4_1_plan.md` §5 (S0), §4 (V1–V7, F-Liste), §7; Anhang A7.
Dieses Modul hat **keine Seiteneffekte beim Import** — die Probe
(`p105_ed41_darstellung_probe.py`) und der Waechter (`tests/test_ed41_probe.py`) lesen beide hier.

**Die Fixtures sind synthetisch** (gebaut aus den Konstrukt-Zaehlungen des Plans, Anhang A7 —
kein echter Notiztext). Quelle der Wahrheit ist das Woerterbuch `NEUE_FIXTURES` unten; die Bytes
liegen zusaetzlich als Dateien in `fixtures_ed41/` plus `fixtures_ed41/MANIFEST.json`
(SHA-256 + Bytezahl je Datei). Der Waechter prueft beides gegeneinander: ein Editor, der beim
Speichern Leerzeichen am Zeilenende kappt, ein Newline anhaengt oder einen BOM entfernt, macht
ihn rot.

**Warum `.txt` und nicht `.md`:** `scripts/doc_health.py` behandelt jede `*.md` als Dokument
(Header-Card, INDEX-Zeile) und nimmt nur `fixtures_m7/` aus (`FIXTURE_PRAEFIX`). Eine Card
wuerde die Bytes zerstoeren, ein neuer Praefix waere ein Eingriff ausserhalb von S0. Die Probe
liest die Bytes, nicht die Endung.

**Die zehn M7-Fixtures werden referenziert, nicht kopiert** (`../fixtures_m7/`, schon vom
Waechter `test_probe_b11_roundtrip.py` festgehalten) — ihr SHA-256 steht trotzdem im Manifest,
damit eine Aenderung auch diesen Korpus rot macht.

Aufruf (schreibt die Dateien + das Manifest neu, nur nach einer gewollten Korpus-Aenderung):
`.venv/bin/python phase10_5_finishing/probes/p105_ed41_spec.py`
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HIER = Path(__file__).resolve().parent
FIXTURE_DIR = HIER / "fixtures_ed41"
M7_DIR = HIER / "fixtures_m7"
MANIFEST = FIXTURE_DIR / "MANIFEST.json"

#: Die feste Asset-ID des Katalog-Bildes (die Saat setzt `files.new_asset_id` auf diesen Wert).
ASSET_ID = "ast_0000e041"

NEUE_FIXTURES: dict[str, str] = {}

NEUE_FIXTURES["11_tabelle_einfach"] = (
    "Einleitung vor der Tabelle.\n"
    "\n"
    "| Einstellung | Bedeutung |\n"
    "|---|---|\n"
    "| `timeout` | Zeit in **Sekunden** |\n"
    "| `retries` | Anzahl der Versuche |\n"
    "| `mode` | *schnell* oder *gruendlich* |\n"
    "\n"
    "Text nach der Tabelle."
)

# KI-Varianten: ohne aeussere Pipes, Ausrichtung, ungleich lange Zeilen (GFM Ex. 202-204),
# `\|` und `|` im Codespan (Ex. 200), leere Zelle, `<br>` in der Zelle (E4).
NEUE_FIXTURES["12_tabelle_ki"] = (
    "## Varianten\n"
    "\n"
    "Spalte A | Spalte B | Spalte C\n"
    ":--- | :---: | ---:\n"
    "links | mitte | rechts\n"
    "nur eins\n"
    "a | b | c | d (zu viel)\n"
    "\n"
    "| Befehl | Wirkung |\n"
    "| ------ | ------- |\n"
    "| `a \\| b` | Pipe maskiert im Code |\n"
    "| a \\| b | Pipe maskiert |\n"
    "| ~~alt~~ neu | durchgestrichen |\n"
    "| Zeile<br>Umbruch | br in der Zelle |\n"
    "|  | leere Zelle |\n"
)

NEUE_FIXTURES["13_tabelle_im_zitat"] = (
    "> Zitat mit Tabelle:\n"
    ">\n"
    "> | k | v |\n"
    "> |---|---|\n"
    "> | 1 | eins |\n"
)

NEUE_FIXTURES["14_listen_verschachtelt"] = (
    "- Punkt eins\n"
    "- Punkt zwei\n"
    "  - verschachtelt A (zwei Spaces)\n"
    "  - verschachtelt B\n"
    "    - tiefer (Ebene drei)\n"
    "- Punkt drei\n"
    "\n"
    "1. erster\n"
    "   1. unter-erster\n"
    "   2. unter-zweiter\n"
    "2. zweiter\n"
    "    - vier Spaces eingerueckt\n"
    "\n"
    "* Stern\n"
    "+ Plus\n"
    "\n"
    "3. beginnt bei drei\n"
    "4. vier\n"
)

NEUE_FIXTURES["15_aufgaben"] = (
    "- [ ] offen\n"
    "- [x] erledigt\n"
    "- [X] erledigt gross\n"
    "  - [ ] Unteraufgabe\n"
    "* [ ] Stern-Aufgabe\n"
    "1. [ ] nummerierte Aufgabe\n"
    "2. [x] nummeriert erledigt\n"
    "- [x]{.rot} Format direkt nach dem Kaestchen\n"
    "- [ ]kein Leerraum nach der Klammer\n"
)

NEUE_FIXTURES["16_code"] = (
    "```python\n"
    "def f(x):\n"
    "    return x | 1  # | Pipe\n"
    "```\n"
    "\n"
    "```\n"
    "ohne Sprache\n"
    "```\n"
    "\n"
    "~~~\n"
    "Tilde-Zaun\n"
    "~~~\n"
    "\n"
    "~~~js\n"
    "const a = '<b>kein HTML</b>';\n"
    "~~~\n"
    "\n"
    "    eingerueckter Code (4 Spaces)\n"
    "\n"
    "Inline `**nicht fett**` und `[x]{.rot}` im Code.\n"
)

NEUE_FIXTURES["17_ueberschriften"] = (
    "# H1\n"
    "## H2\n"
    "### H3\n"
    "#### H4\n"
    "##### H5\n"
    "###### H6\n"
    "\n"
    "Setext Eins\n"
    "===========\n"
    "\n"
    "Setext Zwei\n"
    "-----------\n"
    "\n"
    "Absatz\n"
    "\n"
    "* * *\n"
    "\n"
    "- - -\n"
    "\n"
    "___\n"
)

NEUE_FIXTURES["18_zitate_fussnoten"] = (
    "> Ebene 1\n"
    "> > Ebene 2\n"
    "> > > Ebene 3\n"
    "\n"
    "Text mit Fussnote[^1] und noch einer[^lang].\n"
    "\n"
    "[^1]: Die erste Fussnote.\n"
    "[^lang]: Eine laengere Fussnote.\n"
)

NEUE_FIXTURES["19_inline_html"] = (
    "Das ist ~~veraltet~~ und das <b>fett per HTML</b>, Zeile<br>Umbruch, Zeile<br/>zwei, "
    "Zeile<br />drei, <kbd>Strg</kbd>+<kbd>S</kbd>, H<sub>2</sub>O, x<sup>2</sup>.\n"
    "\n"
    "<details><summary>Mehr</summary>\n"
    "\n"
    "Versteckter Text.\n"
    "\n"
    "</details>\n"
    "\n"
    "Platzhalter wie <domain> und <repo> bleiben Text.\n"
    "\n"
    "Fisch &amp; Chips, gesch&uuml;tzt&nbsp;Leerzeichen.\n"
)

# Die XSS-Liste des Plans §4.3 (SI1-SI5). Jede Zeile ist ein eigener Absatz.
NEUE_FIXTURES["20_xss"] = (
    "<script>alert(1)</script>\n"
    "\n"
    "<img src=x onerror=alert(2)>\n"
    "\n"
    "<svg onload=alert(3)>\n"
    "\n"
    "<iframe src=\"https://example.invalid/\"></iframe>\n"
    "\n"
    "<style>body{display:none}</style>\n"
    "\n"
    "<a href=\"javascript:alert(4)\">js-link</a>\n"
    "\n"
    "[md-js](javascript:alert(5))\n"
    "\n"
    "![md-data](data:image/png;base64,AAAA)\n"
    "\n"
    "<javascript:alert(6)>\n"
    "\n"
    "&lt;script&gt;alert(7)&lt;/script&gt;\n"
    "\n"
    "<!-- HTML-Kommentar -->\n"
    "\n"
    "<noscript><p title=\"</noscript><img src=x onerror=alert(8)>\">\n"
)

NEUE_FIXTURES["21_format_konvention"] = (
    "[Rot]{.rot} [Gross]{.gross} [Beides]{.rot .gross} [Unbekannt]{.lila}\n"
    "\n"
    "::: {.zentriert}\n"
    "Zentrierter Text\n"
    ":::\n"
    "\n"
    "::: {.warnung}\n"
    "Unbekannte Klasse: dieser Text darf nie verschwinden.\n"
    ":::\n"
    "\n"
    "Code: `[x]{.rot}` und Bild ![[alt]{.rot}](asset:" + ASSET_ID + ")\n"
)

NEUE_FIXTURES["22_ohne_newline"] = "Erste Zeile\n\nLetzte Zeile ohne Newline"

NEUE_FIXTURES["23_tabs"] = (
    "\tTab am Anfang\n"
    "Zeile mit Tab\tdrin\n"
    "- Liste\n"
    "\t- mit Tab eingerueckt\n"
    "naechste Zeile\t\n"
)

NEUE_FIXTURES["24_doppel_leerzeichen"] = (
    "Harter Umbruch mit zwei Spaces  \n"
    "naechste Zeile\n"
    "Harter Umbruch mit Backslash\\\n"
    "naechste Zeile\n"
    "Zeile mit drei Spaces am Ende   \n"
    "\n\n\n"
    "Ende mit Leerzeilen\n\n"
)

NEUE_FIXTURES["25_unicode"] = (
    "﻿BOM am Anfang des Bodys\n"
    "Trenner (U+2028) und NBSP und Familie \U0001F468‍\U0001F469‍\U0001F467 "
    "und RTL שלום\n"
    "Kombiniert: é und \U0001F44D\U0001F3FD, Pfeile ← → ✓ ≤\n"
)

# Bestand: 0 CRLF (Plan F8). Der Server liefert LF (`read_text`) — die Probe haelt das als
# **Information** fest, nicht als Zelle (V1-V3 gelten gegen den API-Body).
NEUE_FIXTURES["26_crlf"] = "Zeile eins\r\nZeile zwei\r\n\r\n| a | b |\r\n|---|---|\r\n| 1 | 2 |\r\n"


def _gross() -> str:
    """2.000 Zeilen mit einer 200-Zeilen-Tabelle (Plan E10: groesste echte Notiz 1.836 Zeilen)."""
    zeilen = ["# Grosse Notiz", "", "| Nr | Name | Wert | Notiz |", "|---:|---|:---:|---|"]
    for i in range(1, 201):
        zeilen.append("| %d | Eintrag %d | %d | **fett** und `code` %d |" % (i, i, i * 7, i))
    zeilen.append("")
    n = 2000 - len(zeilen)
    for i in range(1, n + 1):
        zeilen.append("Absatzzeile %d mit [Link](https://example.invalid/%d) und *kursiv*." % (i, i))
    return "\n".join(zeilen) + "\n"


NEUE_FIXTURES["27_gross"] = _gross()

# **Das Katalog-Item** (Plan §7): jedes Konstrukt der Teilmenge genau einmal, jede Zeile mit
# einem **eindeutigen Ankertext** (die Probe sucht die Editorzeile ueber ihn). Die Probe
# oeffnet es einmal im eigenen Space (Editor) und einmal im fremden (Lesesicht).
NEUE_FIXTURES["28_katalog"] = (
    "# Katalog Ueberschrift Eins\n"
    "## Katalog Ueberschrift Zwei\n"
    "### Katalog Ueberschrift Drei\n"
    "#### Katalog Ueberschrift Vier\n"
    "##### Katalog Ueberschrift Fuenf\n"
    "###### Katalog Ueberschrift Sechs\n"
    "\n"
    "Setext Katalog Eins\n"
    "===================\n"
    "\n"
    "Setext Katalog Zwei\n"
    "-------------------\n"
    "\n"
    "Absatz mit **fett**, *kursiv*, `codespan` und einem [Link](https://example.invalid/a).\n"
    "\n"
    "Durchgestrichen: ~~weg damit~~ steht da.\n"
    "\n"
    "Harter Umbruch hier  \n"
    "naechste Zeile nach dem Umbruch.\n"
    "\n"
    "Nackte URL: https://example.invalid/nackt\n"
    "\n"
    "Entitaet: Fisch &amp; Chips\n"
    "\n"
    "| Einstellung | Bedeutung | Mitte |\n"
    "|---|---|:---:|\n"
    "| `timeout` | Zeit in **Sekunden** | m1 |\n"
    "| a \\| b | Pipe maskiert | m2 |\n"
    "| Zeile<br>Umbruch | br in Zelle | m3 |\n"
    "\n"
    "Spalte A | Spalte B | Spalte C\n"
    ":--- | :---: | ---:\n"
    "links | mitte | rechts\n"
    "nur eins\n"
    "a | b | c | d zu viel\n"
    "\n"
    "> Zitat Ebene eins\n"
    "> > Zitat Ebene zwei\n"
    "\n"
    "> | k | v |\n"
    "> |---|---|\n"
    "> | 1 | eins im Zitat |\n"
    "\n"
    "- Punkt eins\n"
    "  - verschachtelt zwei Spaces\n"
    "    - Ebene drei tief\n"
    "- Punkt zwei\n"
    "    - vier Spaces eingerueckt\n"
    "\n"
    "1. erster Nummernpunkt\n"
    "2. zweiter Nummernpunkt\n"
    "\n"
    "- [ ] offene Aufgabe\n"
    "- [x] erledigte Aufgabe\n"
    "  - [ ] Unteraufgabe tief\n"
    "\n"
    "1. [ ] nummerierte Aufgabe\n"
    "\n"
    "- [x]{.rot} Format nach dem Kaestchen\n"
    "\n"
    "```python\n"
    "def katalog_zaun(x):\n"
    "    return x\n"
    "```\n"
    "\n"
    "~~~\n"
    "Tilde-Zaun Inhalt\n"
    "~~~\n"
    "\n"
    "    eingerueckter Code Inhalt\n"
    "\n"
    "Code mit Format: `[x]{.rot}` bleibt Code.\n"
    "\n"
    "* * *\n"
    "\n"
    "[Rot]{.rot} und [Gross]{.gross} und [Unbekannt]{.lila}\n"
    "\n"
    "::: {.zentriert}\n"
    "Zentrierter Katalogtext\n"
    ":::\n"
    "\n"
    "::: {.warnung}\n"
    "Unbekannte Klasse bleibt sichtbar.\n"
    ":::\n"
    "\n"
    "Bild normal: ![Kontrollbild](asset:" + ASSET_ID + ")\n"
    "\n"
    "Bild mit Format: ![[Alt rot]{.rot}](asset:" + ASSET_ID + ")\n"
    "\n"
    "Inline-HTML: <b>fett per HTML</b> und <span class=\"x\">Spanne</span>.\n"
    "\n"
    "Fussnote hier[^1].\n"
    "\n"
    "[^1]: Die Fussnote des Katalogs.\n"
    "\n"
    "Ende des Katalogs.\n"
)


def neue_fixture_datei(name: str) -> Path:
    return FIXTURE_DIR / (name + ".txt")


def alle_fixtures() -> dict[str, bytes]:
    """Name -> Bytes, die **zehn M7** (von der Platte) und die neuen (aus dem Woerterbuch)."""
    out: dict[str, bytes] = {}
    for pfad in sorted(M7_DIR.glob("*.md")):
        out["m7_" + pfad.stem] = pfad.read_bytes()
    for name, text in NEUE_FIXTURES.items():
        out[name] = text.encode("utf-8")
    return out


def fixtures_von_platte() -> dict[str, bytes]:
    """Name -> Bytes **von der Platte**, jede Datei gegen `MANIFEST.json` geprueft (fail-closed).

    Die Probe saet diese Bytes — gemessen wird also, was im Repo liegt, nicht das Woerterbuch."""
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))["dateien"]
    out: dict[str, bytes] = {}
    for rel, soll in manifest.items():
        b = (FIXTURE_DIR / rel).resolve().read_bytes()
        ist = hashlib.sha256(b).hexdigest()
        if ist != soll["sha256"] or len(b) != soll["bytes"]:
            raise SystemExit("Fixture weicht vom Manifest ab: %s (sha256 %s, erwartet %s)" % (rel, ist, soll["sha256"]))
        out[soll["name"]] = b
    return out


def manifest_soll() -> dict:
    eintraege = {}
    for pfad in sorted(M7_DIR.glob("*.md")):
        b = pfad.read_bytes()
        eintraege["../fixtures_m7/" + pfad.name] = {
            "name": "m7_" + pfad.stem, "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}
    for name, text in NEUE_FIXTURES.items():
        b = text.encode("utf-8")
        eintraege[name + ".txt"] = {"name": name, "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}
    return {"hinweis": "SHA-256 je Fixture-Datei; Quelle der Wahrheit: p105_ed41_spec.py :: NEUE_FIXTURES "
                       "(M7: ../fixtures_m7/, referenziert). Neu erzeugen nur nach gewollter Aenderung.",
            "dateien": eintraege}


# ------------------------------------------------------------------------------------------------
# Die Zellen. `basis` = erwarteter Stand **heute** (main, v4.0.1): True = gruen, False = rot.
# `ziel` = der Schritt, der die Zelle gruen machen soll. `grund` = Plan-Befund.
# Eine Zelle, deren Messung von `basis` abweicht, ist ein **Befund** (die Probe meldet sie unter
# `abweichungen`; der Waechter macht sie rot, bis jemand die Erwartung bewusst nachzieht).
# ------------------------------------------------------------------------------------------------

ZELLEN: dict[str, dict] = {}


def _z(name, sicht, basis, ziel, grund):
    ZELLEN[name] = {"sicht": sicht, "basis": basis, "ziel": ziel, "grund": grund}


# Lesesicht (fremdes Item im Space beta, `#ro-preview`), Katalog-Item
_z("l_ueberschrift_h1_h4", "lesesicht", True, "-", "heute ok")
_z("l_ueberschrift_h5_h6", "lesesicht", False, "S3b", "F3 h5/h6 = Absatz")
_z("l_setext", "lesesicht", False, "S3b", "F3/F4f Setext = Absatz")
_z("l_inline", "lesesicht", True, "-", "strong/em/code/a heute ok")
_z("l_durchgestrichen", "lesesicht", False, "S3b", "F3 ~~ woertlich")
_z("l_harter_umbruch", "lesesicht", False, "S3b", "F3 harte Umbrueche verschluckt")
_z("l_autolink", "lesesicht", False, "S3b", "A7 nackte URL = Text")
_z("l_entitaet", "lesesicht", False, "S3a", "§4.1 &amp; heute woertlich (Vor-Escaping)")
_z("l_tabelle", "lesesicht", True, "-", "heute ok")
_z("l_tabelle_ausrichtung", "lesesicht", True, "-", "ta-c heute ok")
_z("l_tabelle_pipe_maskiert", "lesesicht", False, "S3b", "F3 \\| teilt die Zelle")
_z("l_tabelle_br", "lesesicht", False, "S3a", "E4 <br> heute Text")
_z("l_tabelle_ohne_aussenpipes", "lesesicht", True, "-", "heute ok")
_z("l_tabelle_ungleich", "lesesicht", False, "S3b", "F3 GFM Ex. 202-204")
_z("l_tabelle_im_zitat", "lesesicht", False, "S3b", "F3 Tabelle im Zitat = Rohtext")
_z("l_zitat", "lesesicht", True, "-", "heute ok")
_z("l_zitat_verschachtelt", "lesesicht", False, "S3b", "F3 > Ebene 2 als Text")
_z("l_liste", "lesesicht", True, "-", "heute ok")
_z("l_liste_verschachtelt", "lesesicht", False, "S3b", "F3 verschachtelte Liste = Absatz")
_z("l_liste_geordnet", "lesesicht", True, "-", "heute ok")
_z("l_aufgabe", "lesesicht", True, "-", "Kaestchen disabled heute ok")
_z("l_aufgabe_verschachtelt", "lesesicht", False, "S3b", "A7 Kaestchen nur oberste Ebene")
_z("l_zaun", "lesesicht", True, "-", "heute ok")
_z("l_zaun_tilde", "lesesicht", False, "S3b", "F3/F4f ~~~ = Absatz")
_z("l_code_eingerueckt", "lesesicht", False, "S3b", "F3/F4f Einzugs-Code = Absatz")
_z("l_codespan_format", "lesesicht", True, "-", "Codespan schuetzt heute")
_z("l_trennlinie", "lesesicht", False, "S3b", "F3 * * * -> <ul><li>")
_z("l_format_farbe", "lesesicht", True, "-", "span.md-c-rot heute ok")
_z("l_format_block", "lesesicht", True, "-", "div.md-a-zentriert heute ok")
_z("l_format_unbekannt", "lesesicht", True, "-", "::: {.warnung} woertlich heute ok")
_z("l_bild", "lesesicht", True, "-", "Kontrollbild asset: heute ok")
_z("l_fussnote", "lesesicht", False, "S3b", "F3/E7 Fussnote woertlich")
_z("html_als_text", "lesesicht", True, "S3a", "§4.3 SI1 (heute: Vor-Escaping)")
_z("keine_aktiven", "lesesicht", True, "S3a", "§4.3 SI2 Sanitizer")

# Editor (eigenes Item im Space alpha), Katalog-Item
_z("e_ueberschrift", "editor", True, "-", "cm-header-1 heute ok")
_z("e_ueberschrift_h5_h6", "editor", True, "-", "cm-header-5/6 heute ok")
_z("e_zitat", "editor", True, "-", "cm-quote heute ok")
_z("e_zaun", "editor", True, "-", "Code im Zaun heute ok")
_z("e_aufgabe", "editor", True, "-", "sfx-todo heute ok")
_z("e_format_farbe", "editor", True, "-", "cm-md-c-rot heute ok")
_z("e_block_bekannt_versteckt", "editor", True, "-", ":::{.zentriert}-Zeilen versteckt heute ok")
_z("e_durchgestrichen", "editor", False, "S4", "A7 strikethrough-Option aus")
_z("tabelle_widget", "editor", False, "S2", "F1 Tabelle im Editor = Rohtext")
_z("listenzeichen", "editor", False, "S4", "F5 .cm-formatting {visibility:hidden} trifft Listenzeichen")
_z("kontrast", "editor", False, "S4", "F6 Tokenfarben < 4,5:1")

# Widersprueche Editor <-> Lesesicht (F4a-f): gruen nur, wenn **beide** Sichten das Ziel zeigen
_z("konflikt_a_block_unbekannt", "beide", False, "S4", "F4a ::: {.warnung} im Editor unsichtbar")
_z("konflikt_b_code_format", "beide", False, "S4", "F4b Overlay faerbt [x]{.rot} im Codespan")
_z("konflikt_c_bild_format", "beide", False, "S3b", "F4c ![[alt]{.rot}](asset:) zerstoert das Bild")
_z("konflikt_d_aufgabe_format", "beide", False, "S4", "F4d - [x]{.rot}: GFM kein Kaestchen")
_z("konflikt_e_aufgabe_geordnet", "beide", False, "S4", "F4e 1. [ ] ohne Kaestchen")
_z("konflikt_f_setext_code", "beide", False, "S3b", "F4f Setext/~~~/Einzug: Editor ja, Lesesicht nein")

# Bytes (V1-V3, V5), alle Fixtures im eigenen Space
_z("bytes_gleich", "bytes", True, "-", "V1+V2: Editor = API-Body, nichts geaendert, kein Write, Datei unberuehrt")
_z("bytes_zelle", "bytes", True, "-", "V3: ein Zeichen in einer Tabellenzelle -> nur dieses Byte")
_z("bytes_ohne_newline", "bytes", True, "-", "V3/V5: Edit am Ende ergaenzt kein Newline")

# Entwurf (V7, F7)
_z("oeffnen_schreibt_keinen_entwurf", "entwurf", False, "S1", "F7a setValue -> change -> saveDraft")
_z("entwurf_ueberlebt_neuladen", "entwurf", False, "S1", "F7a anderes Item zuerst -> Entwurf ueberschrieben")
_z("kein_stilles_zurueck", "entwurf", False, "S1", "F7b Entwurf ohne Version -> fremde Aenderung still zurueckgesetzt")

ERWARTET_BASIS = {n: z["basis"] for n, z in ZELLEN.items()}

# ------------------------------------------------------------------------------------------------
# Staende (Plan §5): jeder Editor-Schritt heilt genau die Zellen, deren `ziel` er ist. `STAND` ist der
# Stand des **heutigen** Arbeitsbaums; die Probe schreibt ihren Beleg nach `BELEG_JE_STAND[STAND]` und
# vergleicht ihre Gegenlaeufe mit **diesem** Beleg (gleicher Baum). Die Basislinie (S0) bleibt eingefroren.
# ------------------------------------------------------------------------------------------------

STAENDE = ["S0", "S1"]
STAND = "S1"
BELEG_JE_STAND = {"S0": "p105_ed41_darstellung.json", "S1": "p105_ed41_darstellung_s1.json"}
ERWARTET = {s: {n: z["basis"] or z["ziel"] in STAENDE[1:STAENDE.index(s) + 1] for n, z in ZELLEN.items()}
            for s in STAENDE}

# ------------------------------------------------------------------------------------------------
# Selbsttest (Gegenlaeufe). Jeder Gegenlauf aendert **eine Kopie** — der Fixture-Bytes in der
# Saat oder der statischen Dateien, die der Wegwerf-Server ausliefert. Arbeitsbaum und
# `fixtures_ed41/` bleiben unberuehrt. Jeder Anker muss **genau einmal** vorkommen.
# `kippt` = die Zellen, die sich gegenueber der Basislinie umdrehen **muessen** (und nur die).
# ------------------------------------------------------------------------------------------------

GEGENLAEUFE: dict[str, dict] = {
    # Plan S0: "ein absichtlich falsches Soll in einer Kopie -> genau die Zelle rot". Das Soll ist
    # das Katalog-Item: die h4-Zeile verliert ihr Leerzeichen (`####Katalog` ist in GFM **keine**
    # Ueberschrift). Gruen -> rot, nur `l_ueberschrift_h1_h4`.
    "fixture_kaputt": {
        "fixture": {"28_katalog": [["#### Katalog Ueberschrift Vier\n", "####Katalog Ueberschrift Vier\n"]]},
        "kippt": ["l_ueberschrift_h1_h4"],
    },
    # Plan S2 Gegenlauf (4): `setBody` mit `trimEnd()` -> nur `bytes_gleich` rot (gruen -> rot).
    "trimend": {
        "static": {"js/editor.js": [["    cm.setValue(text);\n    _cursorZeileSetzen();",
                                     "    cm.setValue(text.trimEnd());\n    _cursorZeileSetzen();"]]},
        "kippt": ["bytes_gleich"],
    },
    # Rot -> gruen: eine rote Basis-Zelle beweist erst etwas, wenn sie gruen werden **kann**.
    # Zwei CSS-Zeilen in der Kopie von `app.css`: Listenzeichen sichtbar, die vier vendorten
    # Tokenfarben (A9) hell. Erwartet: genau `listenzeichen` und `kontrast` werden gruen.
    "css_rot_nach_gruen": {
        "static": {"app.css": [[
            ".CodeMirror.is-raw .cm-formatting { visibility: visible; }\n",
            ".CodeMirror.is-raw .cm-formatting { visibility: visible; }\n"
            ".CodeMirror .cm-formatting-list { visibility: visible; }\n"
            ".CodeMirror .cm-keyword, .CodeMirror .cm-tag, .CodeMirror .cm-attribute, "
            ".CodeMirror .cm-string { color: var(--editor-text); }\n"]]},
        "kippt": ["listenzeichen", "kontrast"],
    },
    # Plan S1 Gegenlauf (1): Ursprungspruefung raus. **Ehrlich gemessen:** das allein faerbt weder
    # `oeffnen_schreibt_keinen_entwurf` (der `isDirty()`-Guard haelt: beim Oeffnen ist der Editor sauber)
    # noch den Entwurf nach der Rueckfrage (er wird **vor** `setBody` gelesen). Es bricht die Szene, in
    # der die Ursprungspruefung die einzige Schranke ist: `setBody` beim Oeffnen meldet „sauber" ->
    # der Entwurf wird geloescht, waehrend die Rueckfrage noch offen ist (ein Neuladen jetzt verloere
    # ihn). Gruen -> rot, nur `entwurf_ueberlebt_neuladen`.
    "s1_ohne_ursprung": {
        "static": {"js/editor.js": [['  if (change && change.origin === "setValue") return;\n', ""]]},
        "kippt": ["entwurf_ueberlebt_neuladen"],
        "ab": "S1",
    },
    # Plan S1 Gegenlauf (2): Versionspruefung raus -> der veraltete Entwurf geht den Weg „gleiche
    # Version" (Wiederherstellen? -> Strg+S setzt die fremde Fassung still zurueck). Nur `kein_stilles_zurueck`.
    "s1_ohne_version": {
        "static": {"js/editor.js": [["  if (draft.version !== item.version) {\n", "  if (false) {\n"]]},
        "kippt": ["kein_stilles_zurueck"],
        "ab": "S1",
    },
}


def main() -> int:
    FIXTURE_DIR.mkdir(exist_ok=True)
    for name, text in NEUE_FIXTURES.items():
        neue_fixture_datei(name).write_bytes(text.encode("utf-8"))
    MANIFEST.write_text(json.dumps(manifest_soll(), indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"fixtures": len(alle_fixtures()), "neu": len(NEUE_FIXTURES), "zellen": len(ZELLEN)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
