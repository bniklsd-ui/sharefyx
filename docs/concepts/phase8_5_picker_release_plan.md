---
status: live
purpose: ausführungsreifer Plan für Phase 8.5 — Link-Picker-Politur, Titel-statt-ID-Hint, v3-Vorabritt und Deploy
read-when: Phase 8.5 ausführen, oder nachschlagen warum ein Phase-8-Restposten so und nicht anders geschlossen wurde
detail: L2
up: ../INDEX.md
down: ../../phase8_5_picker_release/CLAUDE.md
updated: 2026-09-03 (neu — Planungssession Claude Code/Opus gegen main@6272cad; N1–N7 gelockt, P8.5-A–P8.5-T, Steps 0/A/B/C/D/Z, Abnahme P8.5-1–P8.5-18, [VERIFY] V95–V105)
---

# Phase 8.5 — Link-Picker-Politur und v3-Release (`phase8_5_picker_release/`)

> **Ergebnis in einem Satz:** Diese Phase schließt die drei benannten Restdefekte aus dem
> Phase-8-Closeout (§9.4.1–§9.4.3), fährt einen vollständigen Vorabritt über den nie
> ausgelieferten v3-Build, bringt ihn live und schließt Phase 8 damit formal ab.
>
> **Ausführender:** opencode/M3, ohne Advisor-Stufe (N4, geerbt von P8-N12).
> **Planungsstand:** `main`@`6272cad`, 2026-09-03, Arbeitsverzeichnis sauber.
> **Kein eigenes Python-Paket** — der Code liegt in `phase2_mcp/mcpserver/` und
> `phase5_ui/webui/static/`, das Phasenverzeichnis trägt nur Kopf, Archiv und Skripte.

---

## §0 Rahmen

### §0.0 Arbeitsweise

- **Ausführender:** opencode/M3 (N4). **Keine Advisor-Stufe** — Ersatz ist die
  Selbstprüf-Checkliste §0.5 plus die Nikinger-Sichtprüfung in Block D. Das ist dieselbe
  Konstruktion wie in Phase 8 (P8-L/N12), bewusst fortgeführt.
- **Eskalationsregel (P8.5-O, neu):** Ein Fund, dessen Ursache in einer *früheren*
  CSS-Regel oder in der Kaskade liegt — nicht in der Regel, die man gerade ansieht —
  wird **nicht symptomatisch gepatcht**, sondern an Claude Code eskaliert. Anlass:
  2026-09-02, die Chevron-Größe war nicht am Chevron falsch, sondern an
  `.field .input { font-size: 13px }`; zwei opencode/M3-Sitzungen kamen daran nicht vorbei.
  Erkennungsmerkmal: *„der Wert stimmt im Quelltext, sieht im Browser aber anders aus"*.
- **Regeldateien vor dem ersten Edit lesen:** Wurzel-`CLAUDE.md` (insbesondere Hard Rules
  1, 5, 8, 9), `docs/DOC_LAYERS_CONVENTION.md`, `phase8_ui_graph/CLAUDE.md`
  §„Selection/Choice Konvention v3" (Zeile 462 ff., verbindlich für jeden UI-Commit).
- **Wegwerf-Instanzen:** Standing Permission gilt (Wurzel-`CLAUDE.md`, `docs/PROMPTS.md`).
  Eigener Port, `tmp`-DATA_ROOT, File-Keyring-Backend, Stopp **ausschließlich** über die
  PID-Datei. **Niemals** `pkill -f` mit Regex, **niemals** `systemctl` (Hard Rule 9).
- **Flake-Regel:** Ein einzelner roter Test wird einmal isoliert wiederholt
  (`pytest -q <nodeid>`); bleibt er rot, ist er ein Befund, kein Flake.

### §0.1 Nikinger-Entscheidungen N1–N7 (gelockt, 2026-09-03)

| # | Frage | Lock |
|---|---|---|
| **N1** | Phasennummer und Verzeichnis | **Phase 8.5**, nicht Phase 9. Verzeichnis `phase8_5_picker_release/`, Plan `docs/concepts/phase8_5_picker_release_plan.md`. Begründung: alle drei Items sind Phase-8-Restposten, und mit dem Deploy im Scope *beendet* die Phase die Phase 8, statt etwas Neues aufzumachen — dieselbe Rolle, die Phase 6.5 zwischen P6 und P7 hatte. Namensmuster folgt `phase6_5_tools_images` (zwei Substantive, beide Scope-Hälften benannt): `picker` = §9.4.2 + §9.4.3, `release` = Vorabritt + Deploy. |
| **N2** | §9.4.1 (Klammer-/Aufzählungs-Kontext) | **Option (a) + Abbruchregel.** Hint ein letztes Mal schärfen; tritt der Defekt danach in einer **vierten** Oberflächenform auf, wird der Punkt als Modellverhalten geschlossen (Option c) — **kein fünfter Hint-Edit**. |
| **N3** | §9.4.2 (Picker füllt nur Frontmatter) | **Umschalter im Dialog.** Ein Knopf bleibt, der Dialog bekommt eine Modus-Auswahl „als Kante (`links:`)" / „als Text-Link im Text". Letzte Wahl wird gemerkt. Verworfen: zweiter Werkzeugleisten-Knopf, Ein-Klick-für-beides, Umwidmung des bestehenden Knopfs. **Bauform noch nicht gelockt:** die Vorschau, die der Nikinger bei dieser Wahl vor sich hatte, zeigte **zwei Radio-Knöpfe**; der Plan setzt stattdessen ein `<select class="input">` an (P8.5-F) — das ist eine **Planer-Substitution auf Konventionsgrund, keine Nikinger-Entscheidung**, und wird in der Sichtprüfung bestätigt oder zurückgedreht (Abnahmezeile P8.5-19). |
| **N4** | Ausführender + Prüfstufe | **Wieder opencode/M3, ohne Advisor.** §0.5-Checkliste + Sichtprüfung ersetzen die Advisor-Runde. |
| **N5** | Testtiefe vor dem Deploy | **Voller v3-Vorabritt gegen eine Wegwerf-Instanz** (Block C): realistischer Datensatz, kompletter Playwright-Ritt über Block C + Block D + die neuen Fixes. **Jeder gefundene Bug wird in dieser Phase behoben.** Erst danach Deploy. Begründung: Block C/D sind ein UI-Umbau, den noch nie ein echter Nutzer gesehen hat. |
| **N6** | Phase-8-Abschluss | **Phase 8.5 schließt Phase 8 formal mit ab** — wie P7 Step A8 mit Phase 6.5 verfuhr. Nach Deploy + Sichtprüfung trägt der Nikinger die ✅/🟡-Entscheidung ein; der Nachtrag geht in `docs/concepts/phase8_ui_graph_plan.md` §9 (P8-N: ein Dokument pro Phase), **nicht** in ein neues Dokument. |
| **N7** | Versionsbadge | **`v3.0` → `v3.0.1`.** Dritte Stelle = Step-Nummer, Konvention aus Phase 8 (v2.2.3 = Phase-8-Step-3) fortgeführt; hier Phase-8.5-Deploy-Step. |

### §0.2 Gelockte Entscheidungen P8.5-A – P8.5-T

| # | Entscheidung | Begründung |
|---|---|---|
| **P8.5-A** | Verzeichnis `phase8_5_picker_release/` mit `CLAUDE.md` + `SESSIONS_ARCHIVE.md` + `scripts/`. Kein Python-Paket. | N1; Muster von `phase6_5_tools_images/` und `phase7_spaces_admin/`. |
| **P8.5-B** | §9.4.1 = Option (a), **einmal**, mit schriftlicher Abbruchregel in der Abnahmezeile P8.5-3. | N2. |
| **P8.5-C** | Der neue Hint-Satz formuliert **generalisierend**, nicht als dritte Aufzählung. | Zwei Runden Aufzählung (plain, Tabelle) haben je die nächste unaufgezählte Form eingeladen. Eine Regel („in jeder Textform") plus Beispiele *als Illustration* ist der letzte billige Hebel; eine dritte Aufzählung sagt eine vierte Form voraus. |
| **P8.5-D** | **Keine neue Tabu-Ausnahme.** Der P8-§0.4-Carve-out („`mcpserver/` vollständig **außer** reinen Beschreibungstext-Strings in `tools.py`", Präzedenz P7-T) wird verbatim geerbt. | Der Edit ist genau ein Beschreibungstext-String. Eine neue Ausnahme zu schreiben, wo eine bestehende exakt passt, verwässert die Tabu-Liste. |
| **P8.5-E** | §9.4.2 = Modus-Umschalter im Picker-Dialog. | N3. |
| **P8.5-F** | Der Umschalter wird als natives **`<select class="input">`** gebaut. **Das ist eine Planer-Substitution, kein Nikinger-Lock** — die Vorschau zur N3-Entscheidung zeigte eine **Radiogruppe**, und genau die hat er ausgewählt. | Grund für die Substitution: die Selection/Choice-Konvention v3 (`phase8_ui_graph/CLAUDE.md:471-497`) legt für die Kategorie *Choice* nativ `<select class="input">` fest, **explizit nicht** ein eigenes Konstrukt; alle 7+1 bestehenden Choice-Stellen sind so gebaut, und die Konvention ist „verbindlich ab sofort für jeden neuen UI-Commit". Gratis dazu: Chevron, `accent-color`, Pfeiltasten, Screenreader, Mobile-Sheet. **Gegenargument, das für die Radiogruppe spricht und bewusst nicht wegdiskutiert wird:** ein `<select>` verbirgt die zweite Option bis zum Öffnen — bei einem Umschalter, der ändert *was ein Klick tut*, ist dauerhafte Sichtbarkeit ein echtes Argument. **Auflösung:** gebaut wird die `<select>`-Fassung; **der Nikinger bestätigt sie in der Sichtprüfung oder ordnet die Radiogruppe an** (Abnahmezeile P8.5-19, Art (L)). Der Tausch ist ein 5-Zeilen-Eingriff und wäre dann eine bewusste, dokumentierte Ausnahme der Konvention — Präzedenz: die Listenzeilen-Ausnahme vom 2026-09-02. |
| **P8.5-G** | Default-Modus `body`. Letzte Wahl in `localStorage` unter `sfx:linkpicker:mode`, Lesen/Schreiben in `try`/`catch`. | `body` ist der strikt mächtigere Modus: ein Body-Link ist **gleichzeitig** eine Graph-Kante (siehe P8.5-J-Begründung). Präfix `sfx:` folgt `editor.js :: draftKeyFor()` (`"sfx:draft:" + id`), also bestehende Konvention, kein neues Schema. `try`/`catch`, weil `localStorage` im privaten Fenster wirft. |
| **P8.5-H** | `openLinkPicker`s Callback-Signatur wird `onPick({ id, title, mode })`. | Der Titel liegt im Suchergebnis bereits vor (`dialogs.js:151`), erreicht den Callback heute aber nie (`dialogs.js:158` reicht nur `item.id` weiter). Ein Objekt statt drei Positionsargumenten, damit ein späterer vierter Schlüssel keine Signaturänderung erzwingt. |
| **P8.5-I** | `insertAtCursor(textarea, text)` wird aus `editor.js :: init()` auf Modulebene gehoben. **Keine zweite Implementierung.** | Die Funktion steht heute bei `editor.js:548` **innerhalb** von `export function init()` (Zeile 439) und ist damit für den Picker-Callback auf Modulebene (`editor.js:94`) unerreichbar. Sie schließt über nichts aus `init()` — `textarea` ist Parameter —, der Hub ist also verlustfrei; alle bestehenden Aufrufstellen innerhalb von `init()` sehen die Modulebene weiterhin. |
| **P8.5-J** | Der Body-Link wird an der **Cursorposition** eingefügt, nicht am Ende. `selectionStart === 0` (Nutzer war nie im Textfeld) ist akzeptiertes Verhalten: Einfügen ganz oben, `insertAtCursor` fokussiert danach die Textarea, der Nutzer sieht also, wo es gelandet ist. | Gleiches Verhalten wie der Bild-Knopf (`editor.js:632`, `insertAtCursor(… "![…](asset:…)")`) — ein zweites Einfüge-Verhalten für dasselbe Textfeld wäre inkonsistent. Verworfen: „ans Ende anhängen" (verliert die Cursor-Semantik). |
| **P8.5-K** | §9.4.3 = `aria-activedescendant`-Muster: Der Fokus bleibt im Suchfeld, ein virtueller Cursor wandert über `aria-selected`. **Kein `tabindex` auf die `li`.** | Ein `tabindex` würde den Fokus aus genau dem Feld ziehen, in das der Nutzer gerade tippt, um zu filtern. Das ist das ARIA-Standardmuster für eine getippte Auswahlliste. |
| **P8.5-L** | **Kein Eingriff in `app.js`.** | Der globale Pfeiltasten-Handler (`app.js:206`) greift nur, wenn `!inField && !anyOverlayOpen()` — das Suchfeld *ist* ein Feld, und der Picker steht in `anyOverlayOpen()` (`app.js:174`). Es gibt keine Kollision, also auch keinen Grund, die Datei anzufassen. Escape wird bereits global auf `closeLinkPicker()` geführt (`app.js:198`) — **nicht duplizieren**. |
| **P8.5-M** | Klick- und Enter-Pfad teilen sich **eine** Funktion `_pickLinkPickerAt(index)`. | Zwei Auswahlpfade, die auseinanderdriften, sind der klassische A11y-Bug. Nebeneffekt: der Leer-Eintrag („Keine Treffer.", `aria-disabled="true"`, ohne `data-itemId`) ist über eine gemeinsame Item-Liste strukturell nicht auswählbar. |
| **P8.5-N** | Vor dem Deploy ein vollständiger v3-Vorabritt gegen eine Wegwerf-Instanz (Block C). Funde werden in dieser Phase behoben. | N5. |
| **P8.5-O** | Eskalationsregel opencode/M3 → Claude Code bei Kaskaden-Ursachen (§0.0). | Empirisch aus der Sitzung vom 2026-09-02. |
| **P8.5-P** | `.rail__version` `v3.0` → `v3.0.1`. `mcpserver.__version__` bleibt unangetastet (anderes Schema). | N7; die Trennung der beiden Versionsschemata ist seit Phase 8 A3 dokumentiert. |
| **P8.5-Q** | Der Deploy ist eine **Nikinger-Aktion**. Claude/opencode bereitet vor, führt nicht aus, fasst den Dienst nicht an. | Hard Rule 9. `deploy.sh` braucht `SHAREFYX_SYSTEMCTL="sudo systemctl"`, `sudo` läuft nicht aus dem `savefyx`-User. |
| **P8.5-R** | Phase 8 wird in dieser Phase formal abgeschlossen; der Nachtrag geht in `docs/concepts/phase8_ui_graph_plan.md` §9. ~~Kein neues Handover-Dokument.~~ **[2026-09-09 Korrektur, Closeout-Session]:** Der Nikinger hat im Closeout-Auftrag ausdrücklich ein Handover verlangt — `docs/concepts/PHASE8_5_CLOSEOUT_HANDOVER.md` existiert und ist der Einstiegspunkt für die P8.6-Planung. §9 unten bleibt der **kanonische** Closeout; das Handover tritt daneben, nicht an seine Stelle. Umkehr durch denselben Menschen, der den Lock gesetzt hat. | N6 + P8-N („ein Dokument pro Phase"). |
| **P8.5-S** | ~~**Keine Übersichtsgrafik** für Phase 8.5.~~ **[2026-09-09 Korrektur, Closeout-Session]:** aufgehoben durch den Nikinger im Closeout-Auftrag — `docs/concepts/phase8_5_picker_release_uebersicht.svg` existiert (1080×1080, Stil der Phase-7-Grafik). Die ursprüngliche Begründung trug bis zum Schluss nicht mehr: die Phase erklärt am Ende zwei nicht-offensichtliche Mechanismen (Body-Link *ist* eine Kante; die Zweiteilung des Deploys durch Hard Rule 9) und eine mitten in der Phase geänderte Statusregel. | Drei Fixes und ein Deploy tragen kein eigenes SVG. „So viel wie nötig." P6/P7 hatten eine, weil dort je ein neues Rechte- bzw. Verwaltungsmodell zu erklären war. |
| **P8.5-T** | Der Closeout wird **§9 dieses Plans**. **Gilt unverändert** — §9 ist gefüllt und bleibt kanonisch; das Handover aus der P8.5-R-Korrektur referenziert §9, statt es zu ersetzen. | P8-N geerbt. |

### §0.3 Tabu-Liste (Diff muss über die gesamte Phase leer bleiben)

Unverändert aus P8 §0.4 übernommen, plus zwei Ergänzungen:

- `authserver/` vollständig.
- `mcpserver/` vollständig **außer** dem einen Beschreibungstext-String `_TITLE_NOT_ID_HINT`
  (`phase2_mcp/mcpserver/tools.py:159-164`) — P8.5-D, Präzedenz P7-T/P8-§0.4.
- `phase5_ui/webui/security.py` (P8-Q geerbt).
- `storage/` **vollständig** — die achte P1-Contract-Öffnung ist seit dem 2026-09-02
  geschlossen (`phase1_storage/CLAUDE.md`), diese Phase öffnet **keine neunte**.
- `phase5_ui/webui/api.py`, `serializers.py`, `permissions.py` — Phase 8.5 baut **keine**
  API-Fläche. Findet der Vorabritt (Block C) einen Serverfehler, ist das ein Befund für
  den Nikinger, kein stiller Fix; siehe C3.
- **Prüfkommando am Step-Ende:**
  ```
  git diff --stat main -- phase4_auth/ phase1_storage/storage/ \
      phase5_ui/webui/security.py phase5_ui/webui/api.py \
      phase5_ui/webui/serializers.py phase5_ui/webui/permissions.py phase2_mcp/
  ```
  Einzige erlaubte Zeile: `phase2_mcp/mcpserver/tools.py` (nur der Hint-Text).
  `phase2_mcp/tests/test_tools.py` steht bewusst nicht unter Tabu — der Test zieht mit.

### §0.4 DRAUSSEN (bewusst, nicht vergessen)

Geerbtes Ledger aus `phase8_ui_graph_plan.md` §9.4.5 (P6-Zeilen 7/9/14–17/23/25/29/30,
P6.5-14, O4/O5/O7, `_trash/`-Räumung, Glyph-Entscheidungen P6/P6.5) · FastMCP-4/V79
(eigene Mini-Phase, P5-C) · Body-Volltextsuche in der Web-UI (Q1) · Rechteverwaltung über
MCP-Tools (P6-M) · Löschen von Items (F2) · Funnel-Watchdog · Mobile/Realtime ·
Light-Mode (P5-X) · neues MCP-Tool für den Graphen (P8 §0.5) · **Dedup zweier Kanten
gleicher Richtung mit unterschiedlichem `kind`** (siehe V102 — falls der Vorabritt zeigt,
dass zwei Linien gezeichnet werden, ist das ein benannter Befund für die nächste Phase,
kein Fix hier).

### §0.5 Selbstprüf-Checkliste am Ende **jedes** Steps (Advisor-Ersatz)

1. `pytest -q` grün (Flake-Regel §0.0).
2. Tabu-Diff-Kommando aus §0.3 leer bzw. nur die eine erlaubte Zeile.
3. Bei JS-Änderungen: `node --check` auf **jede** berührte Datei.
4. Bei UI-Änderungen: `python phase5_ui/scripts/ui_budget.py` — alle Budgets grün.
5. Fehlerpfad einmal durchdacht: Was passiert bei leerem Suchergebnis, bei
   `localStorage`-Wurf, bei Cursor auf `-1`, bei geschlossenem Editor?
6. Neue/geänderte `.md` haben L1-Card **und** `docs/INDEX.md`-Zeile; Modul-Status-Tabelle
   und `## Session stopped`-Block im Phase-Head aktualisiert (Hard Rule 8) — **im selben
   Commit**.
7. Kein Service-Touch: `systemctl status sharefyx-mcp` nur **lesend**, PID und Uptime im
   Session-Block notieren.

### §0.6 `[VERIFY]`-Register V95–V105

| # | Frage | Wann |
|---|---|---|
| V95 | **Sammelmarker.** Jeder in diesem Plan zitierte `Datei:Zeile`-Anker ist gegen `main`@`6272cad` (2026-09-03) verifiziert. Vor **jedem** Edit erneut prüfen — Zeilennummern wandern. | laufend |
| V96 | `pytest -q`-Ausgangsstand real **959**? (letzte Messung 2026-09-02) | Step 0 |
| V97 | `ui_budget.py`-Ausgangsstand real **125.8/250 KB**, 5/5 grün? | Step 0 |
| V98 | Ist Port **18773** frei? (18766–18772 waren Phase-8-Wegwerf-Ports) | C1 |
| V99 | Nutzt das Projekt `localStorage` bereits? Erwartet: ja, `editor.js :: draftKeyFor()` → `"sfx:draft:"`. Falls nein, ist P8.5-G neu zu begründen. | A1 |
| V100 | Wird `insertAtCursor` außerhalb von `init()` erwartet oder anderswo geshadowed? Erwartet: nein, einzige Definition bei `editor.js:548`. | A1 |
| V101 | Verhalten von `role="combobox"` + `aria-activedescendant` auf `<input type="search">` in **Chromium und Firefox** — empirisch prüfen, nicht aus der Spec übernehmen. Firefox ist die Browser-Realität dieses Projekts (Funnel-Incident-Report kam aus Firefox). | A2 |
| V102 | Zeichnen `_graph_get` + `graph.js` eine Frontmatter-Kante und eine Body-Kante zwischen **denselben** zwei Knoten als eine oder als zwei Linien? (`item_links` hat kein Cross-`kind`-Dedup, `index.py:183-203`.) Nur messen, nicht fixen (§0.4). | C2 |
| V103 | Hat `phase5_ui/scripts/deploy.sh` seit dem Hänger vom 2026-09-01 eine Änderung erfahren? Läuft der `sudo`-Prompt sichtbar im Vordergrund? | D2 |
| V104 | Ist der Playwright-MCP unter opencode noch verbunden (Nachfolger von V93)? Sonst läuft Block C als Claude-Code-Zuarbeit. | Step 0 |
| V105 | Verbindet der echte Anthropic-Connector nach dem Deploy weiterhin (MCP-Spec-/Connector-Drift seit 2026-08-28)? | D3 |

---

## §1 Step 0 — Haushalt und Verifikations-Durchlauf

**Der Durchlauf ist bereits gefahren** (Claude Code, 2026-09-03, gegen `main`@`6272cad`).
Ergebnis unten. opencode/M3 **wiederholt die Messung nicht**, sondern arbeitet die vier
Funde ab und legt das Phasenskelett an.

### §1.1 Messergebnis (2026-09-03)

| Prüfung | Ergebnis |
|---|---|
| `up:`/`down:`-Links über alle 57 `.md` auflösbar | ✅ **0 kaputt** — nichts zu tun |
| Jede `.md` hat eine `docs/INDEX.md`-Zeile | 4 ohne: `.claude/RESUME.md` (Harness-Datei), 3× `phase6_shares/tests/golden/*.md` (pytest-Golden-Fixtures) — **keine Projektdoku**, siehe Fund 2 |
| Jede lebende `.md` hat eine L1-Card (YAML-Frontmatter) | 4 ohne: `.claude/RESUME.md`, `docs/UPDATE_LOG.md`, `phase5_ui/THIRD_PARTY_LICENSES.md`, `phase5_ui/vendor/lucide/README.md` — siehe Fund 2 |
| Head über 40 KB gelaufen | **Ja: `docs/INDEX.md` = 49.981 B** — siehe Fund 1. Ferner bekannt und benannt: `phase8_ui_graph/CLAUDE.md` 90,7 KB, `phase6_shares/CLAUDE.md` 40,1 KB |

### §1.2 Fund 1 — `docs/INDEX.md` reißt den eigenen Softcap (Step 0.1)

`docs/INDEX.md` ist ein 📗-Dokument mit **49.981 B** (gemessen 2026-09-03 *vor* der Zeile für
diesen Plan; mit ihr ~52,7 KB — vor dem Kürzen selbst nachmessen) und damit über dem
40-KB-Softcap, den es in seinem eigenen Wartungsblock (Zeile 18–19) *anordnet*. Rotation ist hier kein Mittel
— die Datei trägt keine Session-Blöcke.

**Ursache, gemessen:** Zeile 8 (`updated:`) ist eine einzige, pipe-getrennte Kette von rund
vierzig datierten Einträgen und macht den Löwenanteil der Datei aus. Dieselbe Historie
steht vollständig in den `SESSIONS_ARCHIVE.md`-Dateien der jeweiligen Phasen.

**Auftrag:** `updated:` auf die **neuesten fünf** Einträge kürzen und eine Schlusszeile
anhängen: `… | ältere Einträge: die jeweilige phase*/SESSIONS_ARCHIVE.md`. Größe vor und
nach im Session-Block nennen.
**Das ist bewusst als benannter Schritt geführt, nicht als stille Aufräumaktion** — es
löscht Historie, auch wenn sie dupliziert ist.

### §1.3 Fund 2 — vier `.md` ohne Card/Indexzeile sind korrekt so (Step 0.2)

Kein Fix, sondern eine **Regel-Präzisierung**. `docs/INDEX.md` Zeile 17 (`neue .md-Datei ⇒
eine Zeile hier im selben Commit`) kennt heute keine Ausnahme, hat aber vier:

| Datei | Warum keine Card/Zeile |
|---|---|
| `.claude/RESUME.md` | Harness-Datei, kein Projektdokument |
| `phase6_shares/tests/golden/{archived,drift_repaired,roundtrip_create}.md` | pytest-Golden-Fixtures — eine Frontmatter-Card würde den Byte-Vergleich brechen |
| `docs/UPDATE_LOG.md` | `webui/updates.py :: parse_update_log()` parst streng; ein YAML-Block wäre Müll im Banner. Trägt stattdessen einen HTML-Kommentar-Kopf |
| `phase5_ui/THIRD_PARTY_LICENSES.md`, `phase5_ui/vendor/lucide/README.md` | Lizenz-/Vendor-Text, wird unverändert mitgeliefert |

**Auftrag:** Wartungsblock in `docs/INDEX.md` um genau diese vier Ausnahmen ergänzen
(`Ausgenommen: Harness-Dateien, Test-Fixtures, maschinell geparste Dateien, Vendor-/Lizenztext`).

### §1.4 Fund 3 — Doku/Code-Drift beim Picker-Symbol (Step 0.3)

`phase8_ui_graph/CLAUDE.md:440` nennt den Picker-Knopf ein **„Büroklammer-Symbol"**.
`app.html:181-183` rendert `<use href="#i-search">` — eine **Lupe**. Der
`UPDATE_LOG.md`-Eintrag vom 2026-09-01 sagt korrekt „Lupe".
**Auftrag:** Zeile 440 korrigieren, mit datierter Notiz.

### §1.5 Fund 4 — Abnahmebilanz Phase 8 stimmt zum dritten Mal nicht (Step 0.4)

`phase8_ui_graph/CLAUDE.md:122` sagt **„15 ✅ · 10 🟡 · 0 ⬜"** von 26 Zeilen.
Maschinell nachgezählt über die Matrix selbst: **14 ✅ · 12 🟡 · 0 ⬜**. Auch die
Aufzählung direkt darunter listet unter „15 ✅" genau **vierzehn** Zeilennummern
(P8-1, 2, 3, 4, 6, 7, 9, 10, 11, 12, 13, 17, 25, 26).

Der Zähler ist damit zum dritten Mal gedriftet (2026-09-02 zweimal korrigiert).
**Auftrag:** Zahl korrigieren, Aufzählung gegen die Matrix abgleichen, und **die Zahl
künftig aus der Tabelle ableiten statt sie zu pflegen** — Prüfkommando in den Phase-Head
schreiben:
```
awk '/^\| P8-[0-9]+ /{ if (/\| ✅ \|/) g++; else if (/\| 🟡 \|/) y++; else if (/\| ⬜ \|/) o++; n++ } \
  END {printf "Zeilen=%d ✅=%d 🟡=%d ⬜=%d\n", n, g, y, o}' phase8_ui_graph/CLAUDE.md
```

### §1.6 Skelett anlegen (Step 0.5)

- `phase8_5_picker_release/CLAUDE.md` — L1-Card, Modul-Status-Tabelle (Step 0 / A / B / C /
  D / Z), leerer `## Session stopped`-Block, `## Abnahmestand` als Tabelle nach dem
  §7-Muster.
- `phase8_5_picker_release/SESSIONS_ARCHIVE.md` — L1-Card, leer.
- `phase8_5_picker_release/scripts/` — leer, wird in Block C gefüllt.
- Drei neue `.md` ⇒ drei Zeilen in `docs/INDEX.md` unter einem neuen Abschnitt
  `## Phase 8.5 — 🔄 …`, **im selben Commit** (Hard Rule 8).
- `ROADMAP.md`: neuer Abschnitt `## Phase 8.5 — Link-Picker-Politur und v3-Release`
  **vor** `## Bewusst nicht auf der Roadmap` (heute Zeile 352).
- Wurzel-`CLAUDE.md` „Current state": neuer Absatz oben.

**DoD Step 0:** vier Funde abgearbeitet, Skelett steht, `docs/INDEX.md` wieder unter 40 KB,
`pytest -q` unverändert grün, Tabu-Diff leer.

---

## §2 Block A — Link-Picker (fällt **nie** unter Druck, außer A2, siehe §8)

### A1 — §9.4.2: Modus-Umschalter und Body-Link

**Ziel:** Wer im Picker einen Treffer wählt, bekommt wahlweise die ID im `links:`-Feld
(Graph-Kante, unsichtbar) **oder** einen klickbaren `[Titel](#item/itm_…)` an der
Cursorposition im Text.

**Warum der Body-Link beides kann** (Kernbefund dieser Planung, im Code verifiziert):
`phase1_storage/storage/linkscan.py :: extract_item_refs()` sucht `\bitm_[0-9a-f]{8}\b`
**überall im Body** und behandelt das `#item/`-Präfix ausdrücklich mit — der Docstring sagt
das wörtlich. Ein Body-Link erzeugt also bereits eine Kante (`item_links.kind = "body"`,
`index.py:250-251`). Der Frontmatter-Eintrag ist für den *sichtbaren* Fall redundant; er
bleibt nötig für die *unsichtbare* Kante. Genau das rechtfertigt zwei Modi statt einem
Kombi-Klick.

**Dateien und exakte Eingriffe:**

**(1) `phase5_ui/webui/static/app.html`** — `#link-picker-dialog`, heute Zeile 270–280.

- Nach der `<p class="overlay__hint">` (Zeile 273), **vor** dem Suchfeld, einfügen:
  ```html
  <label>Einfügen
    <select class="input" id="link-picker-mode">
      <option value="body">als Text-Link im Text</option>
      <option value="frontmatter">als Kante (Feld „Links")</option>
    </select>
  </label>
  ```
  **Bares `<label>`, ausdrücklich NICHT `class="field"`** — verifiziert 2026-09-03:
  `#move-space-select`, das Vorbild der Konvention, sitzt in `app.html:286-287` ebenfalls in
  einem baren `<label>` innerhalb eines `.overlay__panel`. Ein `.field`-Wrapper zöge
  `.field .input { font-size: 13px }` herein — **genau die Regel, die am 2026-09-02 die
  Chevron-Eskalation ausgelöst hat**. Kein `.field` in einem Overlay-Panel.
  **Pflichtprüfung am Ende von A1:** computed `font-size` und Chevron-Größe dieses Selects
  gegen `#move-space-select` vergleichen; Abweichung ⇒ Eskalation nach §0.0, kein Nachjustieren
  am neuen Selektor.
  Reihenfolge der `<option>` ist die Default-Reihenfolge; die tatsächliche Vorauswahl setzt
  JS aus `localStorage` (P8.5-G).
- Suchfeld (Zeile 274) um drei Attribute ergänzen:
  `role="combobox" aria-expanded="true" aria-controls="link-picker-results"`.
  Ohne `aria-controls` ist `aria-activedescendant` aus A2 formal ungültig.
- Hinweistext (Zeile 273) anpassen — er behauptet heute, ein Klick hänge die ID an die
  Links an; das gilt künftig nur noch im Modus „als Kante".

**(2) `phase5_ui/webui/static/js/dialogs.js`** — Picker-Modul, heute Zeile 100–186 + Init
Zeile 505–517.

- Modul-Konstante ergänzen:
  ```js
  var LINK_PICKER_MODE_KEY = "sfx:linkpicker:mode";
  ```
- Modul-Variablen: `linkPickerModeEl` neu.
  **`linkPickerButtonEl` (Zeile 107 + Zuweisung Zeile 510) ersatzlos entfernen** — die
  Variable wird in `dialogs.js` nirgends gelesen; `editor.js:47` hält ihre eigene.
- Neu:
  ```js
  function _linkPickerMode() {
    return linkPickerModeEl.value === "frontmatter" ? "frontmatter" : "body";
  }

  function _restoreLinkPickerMode() {
    var saved = null;
    try { saved = window.localStorage.getItem(LINK_PICKER_MODE_KEY); } catch (e) { saved = null; }
    linkPickerModeEl.value = (saved === "frontmatter") ? "frontmatter" : "body";
  }
  ```
  Der `change`-Handler des Selects schreibt zurück, ebenfalls in `try`/`catch` — **beim
  Wechsel, nicht beim Picken**, damit die Wahl auch einen Abbruch überlebt.
- `openLinkPicker(opts)` (Zeile 115): Guard-Text auf die neue Signatur ziehen
  (`"openLinkPicker braucht { onPick({id, title, mode}) }"`), `_restoreLinkPickerMode()`
  vor `linkPickerSearchEl.focus()` aufrufen.
- `closeLinkPicker()` (Zeile 127): den Modus **nicht** zurücksetzen (er ist persistent);
  Cursor und `aria-activedescendant` zurücksetzen (Details in A2).
- `_renderLinkPickerResults(items)` (Zeile 136): Klick-Listener ruft künftig
  `_pickLinkPickerAt(i)` (A2). Der Callback bekommt:
  ```js
  onPick({ id: item.id, title: item.title, mode: mode });
  ```
  wobei `mode` **vor** `closeLinkPicker()` gelesen wird.

**(3) `phase5_ui/webui/static/js/editor.js`**

- **Hub (P8.5-I):** `insertAtCursor` (heute Zeile 548–557, innerhalb `init()`) unverändert
  auf Modulebene verschieben, direkt hinter `_appendLinkId` (Zeile 100). Kein Umschreiben
  des Körpers.
- Neu, direkt darunter:
  ```js
  // Phase 8.5 A1: Body-Variante des Link-Pickers. Erzeugt einen klickbaren Markdown-Link;
  // die `itm_`-ID darin ist gleichzeitig eine Graph-Kante (storage/linkscan.py matcht sie
  // im Body, `#item/`-Praefix eingeschlossen) -- deshalb ist ein zusaetzlicher Eintrag in
  // `links:` fuer den sichtbaren Fall redundant.
  function _linkTextFor(title, id) {
    var t = (title || "").replace(/\s+/g, " ").trim();
    if (!t) return id;
    return t.replace(/([\[\]])/g, "\\$1");
  }

  function _appendLinkMarkdown(title, id) {
    if (!/^itm_[0-9a-f]{8}$/.test(id)) return;
    insertAtCursor(editorTextareaEl, "[" + _linkTextFor(title, id) + "](#item/" + id + ")");
  }

  function _onLinkPicked(picked) {
    if (!picked || typeof picked.id !== "string") return;
    if (picked.mode === "frontmatter") _appendLinkId(picked.id);
    else _appendLinkMarkdown(picked.title, picked.id);
  }
  ```
  `_linkTextFor` maskiert `[`/`]` — ein Titel wie `Notiz [Entwurf]` würde den Link sonst
  zerreißen — und kollabiert Zeilenumbrüche, weil ein Markdown-Linktext einzeilig sein muss.
  Die `itm_`-Alphabetprüfung ist bewusst identisch mit der in `_appendLinkId` (Zeile 95),
  gleiche Defense-in-Depth-Begründung.
- Verdrahtung (heute Zeile 481): `openLinkPicker({ onPick: _appendLinkId })` →
  `openLinkPicker({ onPick: _onLinkPicked })`.

**(4) `phase5_ui/webui/static/app.css`** — kein neuer Selektor nötig; `.field`/`.input`
tragen den Umschalter, `select.input` bringt Chevron und `accent-color` bereits mit
(Selection/Choice-Konvention v3). Falls die Dialogbreite kneift, ist `.overlay__panel`
**nicht** anzufassen — dann ist es ein Befund, kein Fix (§0.0-Eskalationsregel).

**Tests A1:**

| Art | Datei | Was |
|---|---|---|
| statisch | `phase5_ui/tests/test_static_routes.py` | `test_link_picker_dialog_has_a_mode_select` — `app.html` enthält `id="link-picker-mode"` und **beide** `value="body"`/`value="frontmatter"` |
| statisch | `phase5_ui/tests/test_static_routes.py` | `test_link_picker_search_is_a_combobox` — `role="combobox"`, `aria-controls="link-picker-results"` |
| statisch | `phase5_ui/tests/test_static_routes.py` | `test_editor_js_builds_item_body_links` — `editor.js` enthält `"](#item/"` |
| Syntax | — | `node --check` auf `editor.js` und `dialogs.js` |
| Browser | Block C, Station 6/8 | Maus-Pfad in beiden Modi |

Muster für die statischen Tests: `test_app_html_has_a_live_manage_spaces_entry`
(`test_static_routes.py:141`) — gleiche Bauart, nichts erfinden.

**DoD A1:** Checkliste §0.5 grün · beide Modi im Browser nachgewiesen (Block C) ·
`ui_budget.py` grün · Tabu-Diff leer.

### A2 — §9.4.3: Tastaturnavigation und `aria-selected`

**Ziel:** `ArrowDown`/`ArrowUp` bewegen eine sichtbare Auswahl durch die Trefferliste,
`Enter` wählt. Die seit dem Sweep vom 2026-09-02 in `app.css:1293-1298` stehende Regel
`.link-picker-results li[aria-selected="true"]` hört auf, toter Code zu sein.

**Heutiger Zustand, verifiziert:** `dialogs.js:147` setzt `role="option"`, **nie**
`aria-selected`. Die `li` tragen kein `tabindex`, weshalb auch die `:focus`-Hälfte der
CSS-Regel (Zeile 1286-1292) nie feuert. Zwei Regelblöcke mit identischen Deklarationen.

**Dateien und exakte Eingriffe:**

**(1) `dialogs.js`** — neue Modul-Variablen:
```js
var linkPickerItems = [];    // die aktuell gerenderten Treffer, Index = Cursor-Index
var linkPickerCursor = -1;   // -1 = keine Auswahl
```

- `_renderLinkPickerResults(items)`:
  - **ganz zu Beginn** `linkPickerItems = []; linkPickerCursor = -1;` und
    `linkPickerSearchEl.removeAttribute("aria-activedescendant")` — sonst überlebt ein
    Cursor das Neu-Filtern und zeigt auf einen anderen Treffer (benannte Falle).
  - Der Leer-Eintrag („Keine Treffer.") wird wie heute erzeugt, aber **nicht** in
    `linkPickerItems` aufgenommen.
  - Für jeden Treffer: `li.id = "link-picker-opt-" + i;` und
    `linkPickerItems.push(item);`, Klick → `_pickLinkPickerAt(i)`.
- Neu:
  ```js
  function _setLinkPickerCursor(index) {
    var lis = linkPickerResultsEl.children;
    for (var k = 0; k < lis.length; k++) lis[k].removeAttribute("aria-selected");
    if (index < 0 || index >= linkPickerItems.length) {
      linkPickerCursor = -1;
      linkPickerSearchEl.removeAttribute("aria-activedescendant");
      return;
    }
    linkPickerCursor = index;
    var li = lis[index];
    li.setAttribute("aria-selected", "true");
    linkPickerSearchEl.setAttribute("aria-activedescendant", li.id);
    li.scrollIntoView({ block: "nearest" });
  }

  function _pickLinkPickerAt(index) {
    var item = linkPickerItems[index];
    if (!item) return;
    var onPick = linkPickerOnPick;
    var mode = _linkPickerMode();          // VOR closeLinkPicker lesen
    closeLinkPicker();
    if (onPick) onPick({ id: item.id, title: item.title, mode: mode });
  }
  ```
- `closeLinkPicker()` ergänzen: `linkPickerItems = []; _setLinkPickerCursor(-1);`
  (die Reihenfolge ist wichtig — erst leeren, dann Cursor räumen).
- Init (Zeile 511 ff.), **ein** neuer Handler am Suchfeld:
  ```js
  linkPickerSearchEl.addEventListener("keydown", function (event) {
    if (event.key === "ArrowDown") {
      event.preventDefault();
      _setLinkPickerCursor(Math.min(linkPickerItems.length - 1, linkPickerCursor + 1));
    } else if (event.key === "ArrowUp") {
      event.preventDefault();
      _setLinkPickerCursor(Math.max(0, linkPickerCursor - 1));
    } else if (event.key === "Enter") {
      event.preventDefault();
      if (linkPickerCursor >= 0) _pickLinkPickerAt(linkPickerCursor);
    }
  });
  ```
  Bewusst **kein** Wrap-around (die Listen-Navigation in `app.js:212` klemmt ebenfalls),
  **kein** `Home`/`End`, **kein** Enter-wählt-den-einzigen-Treffer (Raten). `Escape` bleibt
  beim globalen Handler (P8.5-L).

**(2) `app.css`** — die zwei identischen Blöcke (Zeile 1286–1298) zu einem zusammenziehen:
```css
.link-picker-results li:hover,
.link-picker-results li[aria-selected="true"] { … unverändert … }
```
Das tote `:focus` entfällt (kein `tabindex`, kann nie feuern). **Die Deklarationen selbst
bleiben byte-identisch** — sie sind der am 2026-09-02 vom Nikinger freigegebene
Auswahl-Standard, hier wird nur entdoppelt.

**(3) `app.js`** — **nicht anfassen** (P8.5-L, Begründung dort).

**Tests A2:**

| Art | Was |
|---|---|
| statisch | `test_link_picker_css_has_one_selection_block` — in `app.css` genau **ein** Vorkommen von `li[aria-selected="true"]` und **kein** `.link-picker-results li:focus` |
| Syntax | `node --check` auf `dialogs.js` |
| Browser (Block C, Station 7) | `ArrowDown` setzt `aria-selected="true"` auf dem ersten `li` und `aria-activedescendant` auf dem Suchfeld · zweites `ArrowDown` wandert weiter · `ArrowUp` am oberen Ende bleibt bei 0 · `Enter` fügt ein · Neu-Tippen setzt den Cursor zurück (kein `aria-selected` mehr im DOM) |
| Browser | V101: dieselbe Station in **Chromium und Firefox** |

**DoD A2:** wie A1, plus V101 beantwortet.

---

## §3 Block B — Titel statt ID (§9.4.1)

### B1 — Hint schärfen, ein letztes Mal

**Datei:** `phase2_mcp/mcpserver/tools.py:159-164`.
Verwendet an vier Stellen (Zeilen 387, 462, 499, 560) — wörtlich identisch, das bleibt so.

**Heutiger Text (verifiziert):**
> Nenne einem Menschen gegenüber immer den Titel eines Items, nicht seine itm_…-ID — die ID
> ist eine interne Adresse und in der Weboberfläche nur als Kopierfeld sichtbar. Beispiel:
> schreibe „Einkaufsliste Winter", nicht „itm_a1b2c3d4"; auch nicht als Tabellen-Spalte.

**Neuer Text (P8.5-C — generalisierend, nicht aufzählend):**
```python
_TITLE_NOT_ID_HINT = (
    "Nenne einem Menschen gegenüber immer den Titel eines Items, nicht seine itm_…-ID — die "
    "ID ist eine interne Adresse und in der Weboberfläche nur als Kopierfeld sichtbar. "
    'Beispiel: schreibe „Einkaufsliste Winter", nicht „itm_a1b2c3d4". Das gilt in jeder '
    "Textform — auch nicht als Tabellen-Spalte, nicht in Klammern hinter dem Titel und "
    "nicht in Aufzählungs-Zeilen."
)
```
Der Satz „Das gilt in jeder Textform" ist die eigentliche Änderung; die drei Beispiele
stehen danach als **Illustration der Regel**, nicht als abschließende Liste. Zwei Runden
reiner Aufzählung (2026-09-01: plain + Tabelle) haben je die nächste unaufgezählte Form
eingeladen — deshalb dieses Mal eine Regel.

**Test:** `phase2_mcp/tests/test_tools.py:137-142`,
`test_tool_descriptions_tell_the_agent_to_name_titles_not_ids`.
Bestehende Asserts (`"Einkaufsliste Winter"`, `"itm_a1b2c3d4"`, `"Tabellen-Spalte"`, plus
Hint-in-Beschreibung für `search_items`/`get_item`/`get_item_meta`/`create_item`) bleiben
**alle** gültig. Zwei ergänzen:
```python
assert "in jeder Textform" in tools._TITLE_NOT_ID_HINT
assert "Klammern" in tools._TITLE_NOT_ID_HINT
```

**Tabu:** Keine neue Ausnahme (P8.5-D). Der Diff auf `phase2_mcp/` darf **genau** diese
eine Datei plus die Testdatei zeigen.

**Vierte Probe (nach dem Deploy, Block D5) — wörtlicher Prüfauftrag für den Nikinger:**
Über den echten Connector, in einem frischen Chat:
> „Zeig mir meine offenen Aufgaben — einmal als Fließtext, einmal als Tabelle, einmal als
> Aufzählung, und nenne bei jeder in Klammern dazu, in welchem Space sie liegt."

Bestanden, wenn in **keiner** der vier Formen eine rohe `itm_…`-ID auftaucht.

**Abbruchregel (N2, verbindlich):** Taucht die ID in einer **vierten** Oberflächenform auf,
wird §9.4.1 als **Modellverhalten dokumentiert und geschlossen** (Option c). Kein fünfter
Hint-Edit, keine Schema-Änderung an `search_items`. Der Punkt verschwindet dann aus dem
Ledger, statt weiter vererbt zu werden.

**DoD B1:** Checkliste §0.5 grün · `pytest -q phase2_mcp/` grün · Tabu-Diff zeigt genau die
erlaubte Zeile.

---

## §4 Block C — v3-Vorabritt gegen eine Wegwerf-Instanz (fällt **nie**)

**Warum dieser Block existiert:** Block C (Plex, Lucide, Farbsemantik, Glas) und Block D
(tabellose Übersicht, Force-Graph) sind gebaut, aber **nie ausgeliefert**. Verifiziert am
2026-09-03: `/opt/sharefyx/current` → `20260901T103944.634877Z` → `007b73d` (Block B),
Badge `v2.2.3`; das Repo trägt `v3.0`. Die Einzel-Smokes der P8-Steps haben jeder für sich
bestanden, aber nie zusammen gegen **einen** Datensatz. N5 verlangt genau das.

### C1 — Wegwerf-Instanz und Datensatz

**Datei:** `phase8_5_picker_release/scripts/wegwerf_setup_v3ritt.py`.
**Vorlage:** `phase8_ui_graph/scripts/wegwerf_setup_c4c5.py` — Bauart übernehmen, nicht neu
erfinden: eigener Port, `tmp`-DATA_ROOT, `keyring.backend`-File-Backend, Nutzer direkt über
`AuthStore.upsert_user()`/`set_totp()`/`confirm_totp()` in `auth.sqlite3` (kein
`provision_user.py`, kein Schreiben in `nikinger-space`), Stopp über `serve.pid`.

- **Port 18773** (V98 — 18766–18772 waren Phase 8).
- **Wurzel:** `/tmp/opencode/sharefyx-wegwerf-v3ritt`.
- **Datensatz** (bewusst größer als bei den Einzel-Smokes, aber unter der 200-Knoten-Marke,
  die in P8-24 Station 3 an `DEFAULT_LIMIT=50` scheiterte):
  - drei Spaces: `alpha` (eigen), `beta` (geteilt, `write`), `gamma` (fremd, nur `read`)
  - ~30 Items, davon ≥6 in Ordnern, 1 archiviert, 1 mit ausschließlich item-level
    `share_read` (der Deploy-Blocker-Fall aus P6 §35–39)
  - ≥6 explizite Kanten: 3 über `links:`, 3 über `itm_`-Referenzen im Body
  - ≥2 Tags, die mehrere Items teilen (für den Tag-Toggle)
  - 1 Item mit Bild-Asset

### C2 — Der Ritt

**Datei:** `phase8_5_picker_release/scripts/v3_ritt_playwright_smoke.py`.
Vorlage: `phase8_ui_graph/scripts/phase8_e2e_smoke.py`. **Achtung, echte Selektoren** —
der P8-Ritt scheiterte einmal an erfundenen IDs: der Editor ist `#detail-editor`, die
Nur-lesen-Ansicht `#detail-readonly` (`app.html:126/138`).

| # | Station | Nachweis | Deckt ab |
|---|---|---|---|
| 1 | Login → Übersicht | tabellose Space-Zeilen, Zähler-Chips, Legende sichtbar | P8-18 |
| 2 | Zähler-Chip klicken | Liste im richtigen Scope, Zeilenzahl plausibel | P8-18 |
| 3 | „Übersicht" klicken | globaler „Alle Items"-Scope, idempotent bei Wiederholung | P8-19 |
| 4 | Graph | Knoten in **allen drei** Farben nicht-leer; Hover dimmt; Tag-Toggle **und** Ordner-Toggle erweitern sichtbar; Settle < 3 s | P8-15, P8-20, P8-21, P8-22 |
| 5 | Knotenklick | Editor bzw. Nur-lesen-Ansicht öffnet sich | P8-20, P8-24 |
| 6 | Picker, Maus, Modus „Text-Link" | Textarea enthält danach `[<Titel>](#item/itm_…)` an der Cursorposition | **A1** |
| 7 | Picker, Tastatur | `ArrowDown` → `aria-selected="true"` + `aria-activedescendant`; `ArrowUp` klemmt bei 0; `Enter` fügt ein; Neu-Tippen räumt den Cursor | **A2**, V101 (Chromium **und** Firefox) |
| 8 | Picker, Modus „Kante" | `#field-links` bekommt die ID, Textarea **unverändert**; Moduswahl überlebt Schließen+Öffnen | **A1**, P8.5-G |
| 9 | Speichern → neu laden | `GET /api/v1/graph` liefert die neue Kante; `kind` passend zum Modus. **V102 hier messen:** beide Modi auf dasselbe Ziel anwenden — zeichnet der Graph eine oder zwei Linien? | P8-6, V102 |
| 10 | Typografie + Icons | Plex geladen (computed `font-family`), 0 Icon-Entities, Lucide-Sprite auflösbar | P8-14, P8-13 |
| 11 | `prefers-reduced-transparency: reduce` + `backdrop-filter` aus | Auswahl bleibt erkennbar, Overlays solide | **P8-16** (die einzige P8-Zeile ohne jeden empirischen Beleg) |
| 12 | `prefers-reduced-motion: reduce` | Graph rendert statisch, keine Animation | P8-22 |
| 13 | Mehrfachauswahl + Batch-Move | ein Passwort + ein TOTP für N Items (Reauth-Grant) | P8-1 Regression |

**Wohin V102s Antwort geht (sonst landet eine gemessene Zahl nirgends):** Zeigt Station 9
**zwei** Linien, wird das in **§9 dieses Plans** unter „Restdefekte und offene Entscheidungen"
als benannter Befund eingetragen — mit Messwert, Fundstelle (`index.py :: replace_item_links`
kennt kein Cross-`kind`-Dedup) und der Feststellung, dass ein Dedup eine `_graph_get`-Änderung
wäre und damit unter §0.3 fällt. **Nicht** hier fixen. Zeigt sie **eine** Linie, wird V102 in
§9.5 schlicht als beantwortet abgehakt.

Screenshots nach `docs/screenshots/v3ritt_NN_*.png`, Namensmuster wie in Phase 8.

### C3 — Bugfix-Schleife

- Jeder Fund wird **benannt** (Station, Symptom, Fundstelle) und **in dieser Phase behoben**
  (N5) — solange er in `webui/static/` oder in den neuen Phase-8.5-Stellen liegt.
- **Ausnahme:** Ein Fund, dessen Fix `webui/api.py`, `serializers.py`, `permissions.py`
  oder `storage/` bräuchte, ist ein **Befund für den Nikinger**, kein stiller Fix (§0.3).
  Vorlegen mit Optionen, wie es Phase 8 mit §9.4.6 gemacht hat.
- **Eskalation:** Kaskaden-Ursachen → Claude Code (§0.0, P8.5-O).
- Nach jedem Fix: Ritt **vollständig** wiederholen, nicht nur die betroffene Station. Zwei
  der drei Phase-8-Smoke-Fehlschläge waren Fehler *im Smoke-Skript selbst*.

**DoD Block C:** alle 13 Stationen grün · Checkliste §0.5 grün · Wegwerf-Instanz sauber
abgebaut (`kill -TERM $(cat serve.pid)`) · Produktion nachweislich unangetastet (PID +
Uptime vorher/nachher im Session-Block).

---

## §5 Block D — Release (fällt **nie**)

### D1 — Vorbereitung (opencode/M3)

- `phase5_ui/webui/static/app.html:20`: `.rail__version` `v3.0` → **`v3.0.1`** (P8.5-P).
- `docs/UPDATE_LOG.md`: **neuer** `## <Deploy-Datum>`-Block **ganz oben**. Der bestehende
  `## 2026-09-02`-Block (Block D) bleibt stehen — das Banner zeigt nur `entries[0]`, und
  `deploy.sh` bricht ohne einen **heute** datierten obersten Eintrag ab (P6-X). Format ist
  streng: `## <YYYY-MM-DD>`, dann `- `-Zeilen, **jede Aussage in genau einer physischen
  Zeile**, kein weicher Umbruch.
  Inhalt, menschenlesbar, drei Zeilen:
  - Der Link-Picker kann jetzt zwei Dinge: einen anklickbaren Verweis in den Text einfügen
    oder eine unsichtbare Verknüpfung im Feld „Links" anlegen — umschaltbar im Dialog.
  - Im Link-Picker funktionieren jetzt Pfeiltasten und Enter, nicht nur die Maus.
  - Claude nennt dir Notizen jetzt auch in Klammern und Aufzählungen beim Titel statt bei
    der internen Kennung.
- **Datumsfalle, benannt:** Am 2026-08-27 brach das Deploy-Gate, weil der Eintrag auf ein
  Datum in der Zukunft lautete. Vor dem Schreiben `date -u +%F` **und** `date +%F` prüfen —
  `deploy.sh` akzeptiert beide (Zeile 131).

### D2 — Deploy (**Nikinger-Aktion**, P8.5-Q)

```bash
SHAREFYX_SYSTEMCTL="sudo systemctl" phase5_ui/scripts/deploy.sh main
```
- **In einer interaktiven Vordergrund-Shell**, damit der `sudo`-Prompt sichtbar ist. Der
  Lauf vom 2026-09-01 hing genau daran über Nacht — und die Doku behauptete danach einen
  Deploy, den es nie gab. V103 vorher prüfen.
- opencode/M3 **führt nicht aus, fasst den Dienst nicht an** (Hard Rule 9). Vorbereiten,
  Kommando nennen, warten.

### D3 — Health-Gate und Live-Verifikation

| Prüfung | Erwartung |
|---|---|
| `GET /health` | 200 |
| `GET /api/v1/me` ohne Session | 401 |
| `GET /mcp/` ohne Token | 401 |
| `.rail__version` im Browser | `v3.0.1` |
| Update-Banner | zeigt den neuen Eintrag |
| `/opt/sharefyx/current` | zeigt auf den neuen Release-Stempel, `git log -1` = der deployte SHA |
| V105 | echter Anthropic-Connector verbindet weiterhin |

### D4 — Sichtprüfung am echten Gerät (Nikinger)

Standard aus `phase8_ui_graph_plan.md` §8. Schließt bei Erfolg **P8-14, P8-15, P8-16,
P8-18, P8-19, P8-23** und die Phase-8.5-Zeilen. Was der Nikinger sieht und nicht mag, wird
protokolliert — Umsetzung ist dann eine Entscheidung, kein Automatismus.

### D5 — Vierte A3-Probe

Prüfauftrag wörtlich aus §3 B1. Ergebnis entscheidet nach der Abbruchregel (N2), ob
§9.4.1 als ✅ oder als „geschlossen, Modellverhalten" endet.

---

## §6 Step Z — Closeout

1. §9 dieses Plans füllen (P8.5-T).
2. **Nachtrag in `docs/concepts/phase8_ui_graph_plan.md` §9** (P8.5-R/N6):
   §9.4.1/§9.4.2/§9.4.3 als erledigt markieren mit Zeiger hierher; §9.4.7-Glyphe nach
   Nikinger-Entscheidung eintragen; Bilanz gegen die korrigierte Zählung (§1.5).
3. `phase8_ui_graph/CLAUDE.md`: §7-Matrix-Zeilen auf den Stand nach D3/D4 heben,
   Session-Block, Rotation prüfen.
4. `phase8_5_picker_release/CLAUDE.md`: Modul-Status vollständig, Abnahmematrix §7 gefüllt,
   `## Session stopped` aktuell, Rotation über `scripts/rotate_session_block.sh`.
5. `docs/INDEX.md`, `ROADMAP.md`, Wurzel-`CLAUDE.md` „Current state" nachziehen — **im
   selben Commit** wie der Abschluss (Hard Rule 8).
6. Größenprüfung: `find . -name "*.md" -not -path "./.venv/*" -size +40k` — jeder Treffer
   muss 📕/📦 sein oder benannt.

---

## §7 Abnahmematrix P8.5-1 – P8.5-20

Legende: **(C)** = Code/Test beweist es · **(W)** = Wegwerf-Instanz/Browser beweist es ·
**(L)** = nur live durch den Nikinger beweisbar.
Glyphen: ✅ live-verifiziert · 🟡 gebaut + Beleg ohne Live-Verify · ⬜ offen.

| # | Kriterium | Art |
|---|---|---|
| P8.5-1 | `docs/INDEX.md` wieder unter 40 KB; Ausnahmeregel für die vier card-losen `.md` steht drin | C |
| P8.5-2 | Doku/Code-Drift „Büroklammer" → Lupe korrigiert; Phase-8-Bilanz stimmt mit der maschinellen Zählung überein (real 14/12/0, dokumentiert war 15/10/0) | C |
| P8.5-3 | `_TITLE_NOT_ID_HINT` generalisiert; `test_tools.py` grün mit den zwei neuen Asserts; **Abbruchregel wörtlich im Phase-Head** | C |
| P8.5-4 | Vierte A3-Probe über den echten Connector: keine rohe `itm_…`-ID in Fließtext, Tabelle, Klammer, Aufzählung | L |
| P8.5-5 | Picker-Dialog trägt `<select class="input" id="link-picker-mode">` mit beiden Werten; Konvention v3 eingehalten | C |
| P8.5-6 | Modus „Text-Link": Klick fügt `[<Titel>](#item/itm_…)` an der Cursorposition ein; Titel mit `[`/`]` bricht den Link nicht | W |
| P8.5-7 | Modus „Kante": Klick hängt die ID an `#field-links`, Textarea unverändert | W |
| P8.5-8 | Moduswahl überlebt Schließen + Öffnen des Dialogs (`localStorage`); privater Modus wirft nicht | W |
| P8.5-9 | `insertAtCursor` existiert **genau einmal**, auf Modulebene; alle Alt-Aufrufe in `init()` funktionieren unverändert | C |
| P8.5-10 | `ArrowDown`/`ArrowUp` setzen `aria-selected` + `aria-activedescendant`; `Enter` wählt; Cursor klemmt an beiden Enden | W |
| P8.5-11 | Neu-Tippen setzt den Cursor zurück; der „Keine Treffer."-Eintrag ist nie auswählbar | W |
| P8.5-12 | Tastatur- und Maus-Pfad laufen beide durch `_pickLinkPickerAt`; `app.js` unverändert | C |
| P8.5-13 | V101 in Chromium **und** Firefox beantwortet | W |
| P8.5-14 | `app.css` hat genau einen Auswahl-Block für den Picker, kein totes `:focus` | C |
| P8.5-15 | v3-Vorabritt: alle 13 Stationen grün gegen die Wegwerf-Instanz; jeder Fund entweder behoben oder als benannter Befund vorgelegt | W |
| P8.5-16 | P8-16 empirisch belegt (`prefers-reduced-transparency` + `backdrop-filter` aus, Auswahl erkennbar) | W |
| P8.5-17 | Deploy gelaufen, Health-Gate 3/3, Badge `v3.0.1` live, Update-Banner zeigt den neuen Eintrag, Connector verbindet (V105) | L |
| P8.5-18 | Sichtprüfung am echten Gerät durchgeführt; Phase-8-Glyphe ✅/🟡 vom Nikinger eingetragen; P8-14/15/16/18/19/23 aufgelöst | L |
| P8.5-19 | **Bauform des Umschalters bestätigt:** der Nikinger nimmt die `<select>`-Fassung ab **oder** ordnet die Radiogruppe aus seiner N3-Vorschau an. Diese Zeile existiert, weil P8.5-F eine Planer-Substitution ist und keine seiner Entscheidungen — sie darf nicht durch die Sichtprüfung durchrutschen | L |
| P8.5-20 | Das Zählkommando aus §1.5 steht im Phase-8-Head, und die dortige Bilanz-Zeile verweist darauf statt eine gepflegte Zahl zu tragen — der Zähler ist dreimal gedriftet, das ist der Fix gegen ein viertes Mal | C |

---

## §8 Reihenfolge und Fallregel

**Reihenfolge:** Step 0 → **A1** → **A2** → **B1** → **C** → **D** → **Z**.

**Warum A1 vor A2** (die im Auftrag genannte Begründung wurde geprüft und trägt nicht):
Der Auftrag argumentierte mit einem „jsdom-Smoke", der zweimal umgeschrieben werden müsste.
**Es gibt keinen jsdom-Harness in diesem Projekt** — verifiziert: keine `package.json`
außerhalb von `.venv`, keine `*.test.js`, kein Picker-spezifischer pytest. Die JS-Prüfstrecke
ist `node --check` + statische Asserts auf `app.html`/`app.js`/`app.css` + Playwright gegen
eine Wegwerf-Instanz.
Die **richtige** Begründung führt zum selben Ergebnis: A1 und A2 landen beide in
`_renderLinkPickerResults` und im Auswahlpfad. Baut man sie in dieser Reihenfolge, deckt
**ein** Skript-Paar (`wegwerf_setup_v3ritt.py` + `v3_ritt_playwright_smoke.py`) beide ab —
Stationen 6/8 für A1, Station 7 für A2. Umgekehrt müsste Station 7 nach A1 nachgezogen
werden.

**Warum B1 nach A2 und nicht davor:** B1 ist völlig unabhängig (andere Datei, anderer
Mechanismus, ein Test-Assert) und braucht als einziger Punkt einen **Live-Connector** zur
Verifikation — es hat keinen Vorteil, ihn früh zu bauen, aber den Nachteil, dass ein
angefasstes `mcpserver/` die Tabu-Diff-Zeile über die ganze Picker-Arbeit hinweg
verunreinigt. Er kann ebenso gut ganz zu Beginn stehen; die Entscheidung ist bewusst
schwach.

**Fallregel unter Zeitdruck:**
1. **C und D fallen nie.** Der Deploy ist der Zweck dieser Phase (N5), nicht ihr Anhang.
2. **A1 fällt nie.** Das ist der Restdefekt mit echtem Nutzerschmerz.
3. **A2 ist der erste Kandidat.** Fällt A2, bleibt §9.4.3 als benannter Defekt stehen —
   dann aber **ohne** die `app.css`-Entdopplung, sonst steht die Regel wieder tot da.
4. **B1 ist der zweite Kandidat.** Fällt B1, gilt sofort die Abbruchregel: §9.4.1 wird als
   Modellverhalten geschlossen (Option c), nicht ein weiteres Mal vererbt.

---

## §9 Closeout (Phase-8.5-Closeout — P8.5-T, kanonisch)

> §9 ist nach P8.5-T **das** Closeout dieser Phase. Das am 2026-09-09 zusätzlich angelegte
> `PHASE8_5_CLOSEOUT_HANDOVER.md` (P8.5-R-Korrektur) ist der schlanke Einstiegspunkt für die
> P8.6-Planung und verweist hierher — es ersetzt §9 nicht.

### §9.1 Status in fünf Sätzen

1. **Phase 8.5 ist inhaltlich vollständig und live.** Alle drei Restdefekte aus
   `phase8_ui_graph_plan.md` §9.4.1–§9.4.3 sind geschlossen, der v3-Vorabritt lief
   **26/26** (13 Stationen × Chromium + Firefox) gegen eine Wegwerf-Instanz, und der
   Deploy ging als Nikinger-Aktion durch: Release `20260905T140325.378914Z`,
   `main`@`6f19a8f`, Badge `v3.0.1`, Service-PID **355956**.
2. **Die Phase schließt Phase 8 formal mit ab** (N6/P8.5-R): Phase 8 steht bei
   **26 ✅ · 0 🟡 · 0 ⬜**, Phase 8.5 bei **20 ✅ · 0 🟡 · 0 ⬜**.
3. **Mitten in der Phase hat sich die Statusregel geändert** (Nikinger-Entscheidung
   2026-09-08): eine von ihm geprüfte Wegwerf-Instanz-Automatisierung zählt als
   „live-verifiziert", weil die Wegwerf ein byte-identischer Git-Checkout ist und sich nur
   in `DATA_ROOT`/`auth.sqlite3`/Identität unterscheidet. Das hob beide Bilanzen ohne eine
   Zeile neuen Code. Herleitung und Grenzen: `sichtpruefung_automation_conventions.md`.
4. **Ein Befund wurde bewusst gemessen statt gefixt:** V102 — Body- und Frontmatter-Kante
   zwischen denselben zwei Knoten zeichnen **zwei** Linien (`kinds=['body','frontmatter']`),
   `index.py :: replace_item_links` hat kein Cross-`kind`-Dedup. Das war §0.4 so
   vorgesehen; der Punkt geht als benannter Befund an P8.6 (§9.4.1 unten).
5. **Die Tabu-Liste hat über die gesamte Phase gehalten.** Der §0.3-Diff war in jedem Step
   leer bis auf die eine erlaubte Zeile (`_TITLE_NOT_ID_HINT` in `tools.py`). Keine neunte
   P1-Contract-Öffnung, kein Service-Touch aus einer Agenten-Session, 964 pytest grün.

### §9.2 Delta

Die Tabelle steht in `PHASE8_5_CLOSEOUT_HANDOVER.md` §2 (Was / Wo / Commit-SHA) und wird
hier nicht dupliziert. Kurzform der Code-Pfade: `webui/static/js/{dialogs,editor,markdown}.js`
· `webui/static/{app.html,app.css}` · `phase2_mcp/mcpserver/tools.py` (nur der Hint-Text) ·
`phase5_ui/tests/test_static_routes.py` · `phase8_5_picker_release/scripts/` (Wegwerf-Setups,
`v3_ritt_playwright_smoke.py`, `health_gate.sh`, `p8519_radiogroup_probe.py`,
`p856_bracket_mini_smoke.py`).

### §9.3 Abnahmestand

**20 ✅ · 0 🟡 · 0 ⬜** von 20 — Art-Verteilung **8× (C) · 8× (W) · 4× (L)**. Kanonische
Tabelle mit Beleg, SHA, Screenshot und Nikinger-Sichtungsvermerk pro Zeile:
`phase8_5_picker_release/SESSIONS_ARCHIVE.md` §Abnahmematrix-Archiv.

Zwei Zeilen brauchen eine Erläuterung:

- **P8.5-19 ist ✅ und am selben Tag überholt.** Die Frage der Zeile („welche Bauform?")
  *wurde* beantwortet — der Nikinger ordnete am 2026-09-06 die Radiogruppe an, sie wurde
  gebaut und gegen die 200-Knoten-Wegwerf verifiziert. Am 2026-09-08 hat er die eigene
  Entscheidung zugunsten der Konventions-Konsistenz umgekehrt. Der Rückbau auf
  `<select class="input">` mit Beschriftung *in* der Box ist P8.6-Arbeit.
- **P8.5-6 fiel als letzte 🟡-Zeile am 2026-09-09**, nachdem die neu formulierte Konvention
  §1 („Vorschau-Pflicht bei klickbaren Links") einen Screenshot des *gerenderten* Links
  verlangte statt der Markdown-Quelle. Beleg: `p856_bracket_mini_smoke.py` +
  `docs/screenshots/p856_bracket_preview.png`.

### §9.4 Restdefekte und offene Entscheidungen

Ausführlich, mit Optionen und Empfehlung, in `PHASE8_5_CLOSEOUT_HANDOVER.md` §4. Hier die
Liste, damit sie im Plan selbst nicht fehlt:

1. **V102-Zwillingskante** — zwei Linien statt einer. Drei Wege: Server-Dedup (**wäre die
   neunte P1-Contract-Öffnung**), `graph.js`-Dedup beim Zeichnen (kein Contract berührt,
   Vorschlag), oder bewusst so lassen. Nicht gelockt.
2. **Radiogruppe → `<select>`** — Rückbau samt Testumbenennung
   (`test_link_picker_uses_a_radio_group_not_a_select` wird sonst zur Lüge).
3. **CSRF-Origin-Mismatch im Wegwerf-Setup** — `_validate_base_url` erzwingt `https://`,
   damit fällt jeder Browser-POST gegen eine `http://127.0.0.1`-Wegwerf durch. Setup-Frage,
   kein Server-Bug; Station 13 blieb deshalb strukturell.
4. **P8.6-Inhalt** — zehn Abschnitte in `p8x_ui_polish_notes.md`, davon §10 neu mit den neun
   Nikinger-Feedback-Punkte vom 2026-09-09 (§10 dort). Erster Punkt der Phase bleibt die
   OpenCode-Vision-Plugin-Installation.
5. **Zwei Nummerierungs-Fragen** — „v3.1 also p8.7" aus dem Nikinger-Feedback gegen die
   dokumentierte Reihe P8.6 → `v3.0.2` / P9 → `v3.1.0`; und der Verzeichnisname der
   Folgephase (§D der Notizen kennt P8.6 noch nicht).
6. **Mobile/Hochkant ist keine Außenkante mehr** (Nikinger, 2026-09-09) — in
   `p8x_ui_polish_notes.md` §B und im ROADMAP-Abschnitt durchgestrichen statt gelöscht.
   **Realtime bleibt draußen.**
7. **Geerbtes Ledger** unverändert offen (`phase8_ui_graph_plan.md` §9.4.5) — Phase 8.5 hat
   davon nichts angefasst und nichts still abgeräumt.

### §9.5 `[VERIFY]`-Bilanz V95–V105

Volle Tabelle mit Belegen: `PHASE8_5_CLOSEOUT_HANDOVER.md` §5. Bilanz: **8 beantwortet**
(V95, V96, V98, V99, V100, V101, V102, V105), davon **zwei mit anderem Ergebnis als
erwartet** — **V99** (das Projekt nutzte bisher nur `sessionStorage`; `localStorage` ist
eine bewusste Eskalation) und **V102** (zwei Linien statt einer). **Drei offen:** **V97**
halb (Step 0 übersprang die Messung, der spätere Lauf war 5/5 grün, die Ausgangszahl
125.8 KB wurde nie gegengeprüft), **V103** nie beobachtet (D2 lief still durch den
Nikinger — beim nächsten Deploy einfach mitprotokollieren), **V104** gegenstandslos (Block C
lief als geschriebenes Playwright-Skript, nicht über MCP).

### §9.6 P1-Contract

Die achte Öffnung bleibt geschlossen; Phase 8.5 hat **keine neunte** geöffnet und keine
angekündigt. **Für P8.6 relevant:** die Server-Variante von §9.4.1 *wäre* die neunte —
anzukündigen in der Planung, nicht beim Bauen zu entdecken.

### §9.7 Was dieser Closeout nicht enthält

- Keine Phase-8-Historie (steht in `phase8_ui_graph_plan.md` §9).
- Keinen P8.6-Plan — dieser Closeout benennt Entscheidungen, er trifft keine.
- Keine Auflösung des geerbten Ledgers.
- Keine Bewertung der neun Feedback-Punkte vom 2026-09-09; sie sind in
  `p8x_ui_polish_notes.md` §10 als Zitat plus Code-Anker abgelegt, ungewichtet.
