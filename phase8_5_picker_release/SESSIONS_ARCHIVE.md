---
status: live
purpose: Archivierte Session-stopped-Blöcke aus phase8_5_picker_release/CLAUDE.md, verbatim, newest-first
read-when: Auditieren der vollen Phase-8.5-Historie — der aktuelle Session-Block lebt im Phase-Head, nicht hier
detail: L3
up: ./CLAUDE.md
down:
updated: 2026-09-07 (D4-Sichtprobe-Folgesession-Block rotiert — manuell wie alle vier vorherigen Schritte in dieser Phase, weil `scripts/rotate_session_block.sh` auf das Phase-8.5-Muster mit einem `## Session stopped` + mehreren `### date`-Subblöcken nicht passt; Cluster-1-P8-16-Block ersetzt ihn im Head, **erste echte Code-Touch-Session seit D1** — `phase8_ui_graph/scripts/p8_16_glass_fallback_probe.py` + `wegwerf_setup_p8_16.py` neu (Port 18775, Standing-Permission-Muster reproduziert), vier Screenshots `docs/screenshots/p8_16_{01..04}_*.png`; **P8.5-16 ✅** (Wegwerf-Chromium-Probe mit CDP-`Emulation.setEmulatedMedia` für `prefers-reduced-transparency: reduce` — beide Glass-Träger `.list__head`+`.overlay__panel` wechseln sauber `blur(14px) saturate(1.5)`+`rgba(27,32,39,0.55)` → `backdrop-filter: none`+`rgb(27,32,39)`, Selektion mit Akzent-Fill+Outline im Solid-Modus voll erkennbar, Restore identisch zur Baseline; Phase 8 P8-16 bleibt 🟡 — throwaway-Eidenz jetzt drin, Nikinger-Sichtprüfung am echten v3.0.1 offen); Phase-8.5-Summary 3 ✅ · 14 🟡 · 3 ⬜ → **4 ✅ · 13 🟡 · 3 ⬜**; pytest nicht gelaufen (kein `.venv`-Python-Touch in `phase8_ui_graph/scripts/`), Tabu-Diff §0.3 leer (Phase-8.5-Tabu greift nicht für `phase8_ui_graph/scripts/`), `node --check`/`bash -n`/`ui_budget.py` irrelevant, Service-Touch 0 nur gelesen (PID 355956 unverändert seit 2026-09-05); Cluster 2-5 (Sichtprüfung 2+3 / Connector / Fabian) als nächste Schritte für Cluster-Sequenz offen, Nikinger-Aktionen) | 2026-09-06 (D4-Block rotiert — manuell wie alle vier vorherigen Schritte in dieser Phase, weil `scripts/rotate_session_block.sh` auf das Phase-8.5-Muster mit einem `## Session stopped` + mehreren `### date`-Subblöcken nicht passt (Skript zählt `## Session stopped`-Header und sieht immer genau einen → Exit 2 „Bereits konform"); D4-Block vorne angehängt (newest-first, vor D3), D3 + D1 + Block-C + B1 + A2 + Step 0 darunter unverändert; **D4-Sichtprobe-Folgesession** (Notiz-Session, kein Code-Touch) hat den D4-Block aus dem Head ersetzt — sieben neue Themen-Cluster aus der Sichtprobe mit Fabian dokumentiert: Spaces-Layout-Reorg, Obsidian-Map (Reload-Overload + Landkarten-Stil + Collapsible mit Abhängigkeiten + zwei D4-bestätigte Beobachtungen), Anzahl-Anzeige Ordner, Edit-in-Place-Vision, Layering-Design-System (3 Layer + Selektion blau), „Konto"→„Einstellungen" + Positions-Tausch mit Logout, De-AI-isierung-Lauf 2 nach neuen Kriterien; **neue Datei `docs/concepts/p8x_ui_polish_notes.md` angelegt** (25 KB, L2, alle 16 Themen — fünf bereits in D4 dokumentierte p8.X-Punkte + sieben Sichtprobe-Folgesession-Cluster + vier Sub-Punkte aus §2 Obsidian-Map; Vorsegmentierter Anhang für die Planungs-Session) | 2026-09-06 (D3-Block rotiert — manuell wie alle vier vorherigen Schritte in dieser Phase, weil `scripts/rotate_session_block.sh` auf das Phase-8.5-Muster mit einem `## Session stopped` + mehreren `### date`-Subblöcken nicht passt (Skript zählt `## Session stopped`-Header und sieht immer genau einen → Exit 2 „Bereits konform"); D3-Block vorne angehängt (newest-first, vor D1), D1 + Block-C + B1 + A2 + Step 0 darunter unverändert; D4-Session (Notiz-Session, kein Code-Touch) hat den D3-Block aus dem Head ersetzt — drei Findings dokumentiert: P8.5-19 Radiogruppe statt `<select>` (Tausch ausstehend), P8.5-6 Bracket-Renderer-Bug (Fix in `markdown.js` ausstehend), UX-2-Step-Knotenklick (p8.X); Phase 8 ✅ + p8.X als Nikinger-Entscheidung für Z vorgemerkt) | 2026-09-05 (D1-Block rotiert — manuell wie Block-C davor, weil `scripts/rotate_session_block.sh` auf das Phase-8.5-Muster mit einem `## Session stopped` + mehreren `### date`-Subblöcken nicht passt; D1 vorne angehängt (newest-first), Block-C + B1 + A2 + A1 + Step 0 darunter unverändert; D3-Prep-Session (Health-Gate-Skript + D2-Discovery) hat den D1-Block aus dem Head ersetzt, D2 lief zwischen D1 und D3 still durch den Nikinger) | 2026-09-05 (Block-C-Block rotiert — manuell wie alle vier vorherigen Schritte, weil `scripts/rotate_session_block.sh` auf das Phase-8.5-Muster mit einem `## Session stopped` + mehreren `### date`-Subblöcken nicht passt (Skript zählt `## Session stopped`-Header und sieht immer genau einen → Exit 2 „Bereits konform"); Block-C vorne angehängt (newest-first), B1 + A2 + A1 + Step 0 darunter unverändert; D1 committet, D2–D5 als Nikinger-Aktionen ausgewiesen) | 2026-09-04 (B1-Block rotiert — manuell wie A2/A1/Step-0, weil `scripts/rotate_session_block.sh` (portiert in Block C, `phase8_5_picker_release/scripts/rotate_session_block.sh`) erst jetzt greift; B1 vorne angehängt (newest-first), A2 + A1 + Step 0 darunter unverändert; C abgeschlossen — 13/13 in Chromium+Firefox, 26/26 gesamt, D/Z stehen noch aus)
---

# SESSIONS_ARCHIVE.md — Phase 8.5: Link-Picker-Politur, Titel-statt-ID-Hint, v3-Vorabritt + Deploy
### 2026-09-06 (D4-Sichtprobe-Folgesession — p8.X-Notizen-Datei angelegt, kein Code-Touch)

**Auftrag:** Notiz-Session. Im Anschluss an die D4-Sichtprüfung hat der Nikinger mit
Fabian weitere Themen-Cluster notiert, die über den D4-Sichtprüfungs-Scope
hinausgehen und in p8.X gehören. Alles in dieser Session **nur dokumentiert**
— kein Code-Touch (Hard Rule 9 + §0.3-Tabu unverändert), keine Tests, kein
Service-Touch, kein `git commit`. **Wichtig:** D4-Block wurde vor diesem Block
**rotiert** nach `SESSIONS_ARCHIVE.md` (manuell wie alle vier vorherigen
Schritte in dieser Phase — Skript `scripts/rotate_session_block.sh` greift hier
nicht, weil das Phase-8.5-Muster mit einem `## Session stopped` + mehreren
`### date`-Subblöcken vom Skript nicht erkannt wird; siehe Archiv-Header).

**Ergebnis — neue Datei `docs/concepts/p8x_ui_polish_notes.md` angelegt
(25 KB, L2).** Sie sammelt alle 16 Themen aus D4 (5) und der
Sichtprobe-Folgesession (7 Cluster mit 4 Sub-Punkten im Obsidian-Map-§2):

| Cluster | Inhalt (Kurzform) | Herkunft |
|---|---|---|
| §1 Spaces-Layout-Reorg | „Alle Items"-Leiste unter Spaces + Kippschalter; Map 40 % Breite, volle Höhe, keine Duplikate | Sichtprobe-Folgesession |
| §2.1 Map-Performance | Jeder Klick auf Übersicht lädt Map neu → überlastet | Sichtprobe-Folgesession |
| §2.2 Map-Stil „Landkarte" | Aktuelle Farben übernehmen (außer Hintergrund), stilisierter, im Gesamt-Style | Sichtprobe-Folgesession |
| §2.3 Map-Field schneidet ab | Layout-Issue | D4 bestätigt + Sichtprobe-Folgesession |
| §2.4 Map-Reload-Drift | Kein persistenter Layout-Seed | D4 bestätigt + Sichtprobe-Folgesession |
| §2.5 Map einklappen mit Abhängigkeiten | Collapsible Map, Abhängigkeiten sichtbar im eingeklappten Zustand | Sichtprobe-Folgesession |
| §3 Anzahl-Anzeige Ordner | Count-Anzeige pro Ordner (Aufgaben + Notizen) | Sichtprobe-Folgesession |
| §4 Edit-in-Place | „Bearbeiten"-Knopf überflüssig; Word-ähnlich im Read-View editieren | Sichtprobe-Folgesession |
| §5 Layering-Design-System | 3 Layer (echtes Schwarz / aktueller Standard / Liquid Glass) + Selektion explizit blau auf Hover, Note-Select, Checkbox | Sichtprobe-Folgesession |
| §6 Settings/Navigation | „Konto" → „Einstellungen"-Rename + Positions-Tausch mit Logout | Sichtprobe-Folgesession |
| §7 De-AI-ierung Lauf 2 | Nach **neuen** Kriterien suchen; dann echte Erstellungs-Regeln | Sichtprobe-Folgesession |
| D4-1 UX-2-Step-Knotenklick | 1. Klick Readonly-Vorschau, 2. Klick vollständig | D4 (verbatim übernommen + Duplikatverweis) |
| D4-4 Save-Button-YAML-Header | Workaround „Leerzeichen einfügen"; Verifikation ob außerhalb Header auftretend steht aus | D4 (verbatim übernommen + Duplikatverweis) |
| D4-5 Fabis Sammelliste | Laufend, was Fabi sammelt | D4 (Duplikatverweis) |

**Zusätzlich in der Notizen-Datei dokumentiert (für die Planungs-Session in
Claude Code, vermutlich nach Phase 8.5 Z):**

- **§A** — vollständige Tabelle der bereits in D4 dokumentierten p8.X-Punkte mit
  Verweisen zurück in den D4-Block.
- **§B** — klare Außenkanten: was **nicht** in p8.X gehört (Body-Volltextsuche Q1,
  FastMCP-4/V79, Funnel-Watchdog, Mobile/Realtime, Light-Mode, Glyph-Entscheidungen,
  Phase-8/8.5-Tabus gelten vorerst weiter).
- **§C** — sechs offene Fragen für die Planungs-Session (Reichweite, Reihenfolge,
  Aufwand-Schätzung, Fabian-Koordination, Layering-Audit-Sweep, Phase-9-Tabu-Frage).
- **§D** — Namens- und Datei-Konvention für den späteren Plan (`phase9_…` oder
  `phase8_x_…`).
- **§E** — chronologische Tabelle der 16 Themen mit Herkunft (alle 2026-09-06).

**Bewusst NICHT in den p8.X-Notizen dokumentiert** (um Doppelung zu vermeiden):

- Phase 8 §9.4.6 drei Restdefekte (Settle-Zeit / Foreign-Farbe / Knotenklick) —
  bereits am 2026-09-02 in Phase 8 D2-Session geschlossen, **nicht** p8.X.
- Phase 8 §9.4.1 A3 Klammer-/Aufzählungs-Kontext — Phase-8.5-Scope, D5
  Vierte A3-Probe entscheidet, **nicht** p8.X.
- Phase 8.5-eigene Funde (P8.5-19 Radiogruppe, P8.5-6 Bracket-Renderer-Bug) —
  Phase-8.5-Scope, Fix vor Z, **nicht** p8.X.

**Verifiziert (§0.5 Checkliste):**

- `pytest -q`: nicht gelaufen — keine Python-Datei berührt.
- Tabu-Diff §0.3: **leer** — kein `phase4_auth/`/`storage/`/`security.py`/`api.py`/
  `serializers.py`/`permissions.py`/`mcpserver/`-Touch. Auch kein anderer Code-Touch
  (`markdown.js`/`dialogs.js`/`editor.js`/`graph.js`/`app.html`/`app.css`
  unangetastet).
- `bash -n`/`node --check`/`ui_budget.py`: irrelevant — keine Code-Änderung.
- Service-Touch **0**. `systemctl show sharefyx-mcp.service` vom 2026-09-05 16:10:18
  CEST / PID 355956 ist weiterhin der letzte gelesene Stand (Hard Rule 9 + §0.5.7).
- Größenprüfung am Ende dieser Session (Ist-Werte, gekürzt): `p8x_ui_polish_notes.md`
  neu, 25.489 B (L2, unter Cap); `phase8_5_picker_release/CLAUDE.md` 39.679 B
  (war 38.038 B, **+1.641 B** netto, **knapp unter Cap**); `SESSIONS_ARCHIVE.md`
  75.330 B (L3, exempt); `docs/INDEX.md` 49.556 B (war 44.784 B, **+4.772 B** durch
  neue Phase-8.X-Sektion + L0-Zeile, weiterhin über Cap); `ROADMAP.md` 43.819 B
  (war 42.413 B, **+1.406 B** durch neue Phase-8.X-Sektion + Tabellenzeilen, neu über
  Cap); **`CLAUDE.md` (Wurzel) 55.014 B** (war 47.999 B, **+7.015 B**, **deutlich
  über Cap**); `phase8_ui_graph_plan.md` 80.039 B (+1.865 B durch §9.4.7-Erweiterung,
  bereits exempt als Plan-Snapshot). `phase8_ui_graph/CLAUDE.md` 93.562 B unverändert
  (diese Session hat nicht hineingeschrieben, Z-Sache).

**Plan-Konsistenz — Drei Festlegungen explizit gemacht, damit die
Planungs-Session sie vorfindet (keine Erfindung, alles aus dem Bericht des
Nikingers):**

1. **p8.X ist eine Nikinger-Entscheidung** (festgelegt in D4, 2026-09-06, in der
   Phase-8.5-Z vorgemerkt). Diese Session hat das weder bestätigt noch aufgehoben —
   die p8.X-Notizen-Datei ist Vorbereitung der späteren Planung, nicht Startschuss.
2. **Reichweite unklar.** §C in der Notizen-Datei listet sechs Fragen, die die
   Planungs-Session beantworten muss, bevor ein Plan-Doc entsteht. Die Datei ist
   **kein** Plan — sie ist Sammlung + Strukturierung, kein Locking.
3. **Keine neuen Tabu-Aufhebungen** für p8.X. Phase-8/8.5-Tabus
   (`storage/`, `authserver/`, `mcpserver/` außer dem Hint, `webui/{security,api,
   serializers,permissions}.py`) gelten vorerst weiter. Die Phase-8.5-D4-Präzedenz
   „`webui/static/js/` ist erlaubt" (Bracket-Renderer-Fix-Pfad) gilt weiter, ist
   aber p8.X nicht vorgeschrieben.

**Doku-Updates im selben Commit (Hard Rule 8):**

- `phase8_5_picker_release/CLAUDE.md`: D4-Block nach `SESSIONS_ARCHIVE.md` rotiert;
  dieser neue Block hier; Modul-Status unverändert (Block D weiter 🟡 bis Z);
  P8.5-Abnahmezeilen unverändert; `updated:`-Pipe vorne ergänzt.
- `phase8_5_picker_release/SESSIONS_ARCHIVE.md`: D4-Block vorne angehängt (verbatim);
  `updated:`-Pipe vorne ergänzt (neuer 2026-09-06-Eintrag über der bisherigen
  D3-Rotation).
- `docs/concepts/p8x_ui_polish_notes.md`: **neu**, L2, 25.489 B.
- `docs/INDEX.md`: eine neue Zeile unter „Phase 8.5"-Header für die p8.X-Notizen-
  Datei; `updated:`-Pipe vorne ergänzt.
- `ROADMAP.md`: Phase-8.5-„nächster Schritt" Verweis auf die Notizen-Datei;
  `updated:`-Pipe vorne ergänzt.
- `CLAUDE.md` (Wurzel): neuer Current-state-Absatz vom 2026-09-06 für die
  Sichtprobe-Folgesession; `updated:`-Pipe vorne ergänzt.
- `docs/concepts/phase8_ui_graph_plan.md` §9.4.7: kurzer Anker auf die neue
  p8.X-Notizen-Datei (Phase-8-Closeout-Verweis).

**Was diese Session bewusst NICHT tat:**

- Kein Code-Touch, kein Deploy, kein `sudo systemctl`, keine `systemctl show`
  (Hard Rule 9 + P8.5-Q; PID 355956 reicht für die Übergabe).
- Kein `pytest`/`node --check`/`bash -n`/`ui_budget.py` — irrelevant ohne Code-Touch.
- Kein Browser-/Funnel-/Connector-Test — alles lief am echten Gerät durch den Nikinger.
- Kein `git commit` — siehe Session-Ende-Notiz unten.
- **Keine Planung von p8.X.** Findings strukturiert, nicht gelockt; Planungs-Session
  (vermutlich Claude Code) klärt Reichweite/Reihenfolge/Aufwand (§C der Notizen-Datei).
- Keine Aufhebung von Phase-8/8.5-Tabus.
- Keine Schließung von P8.5-6 / P8.5-19 — die Fixe gehören in den
  Phase-8.5-Tausch-Pfad vor Z, **nicht** in die p8.X-Notizen.
- Kein Schreibvorgang in `phase8_ui_graph/CLAUDE.md` (Phase 8 ✅, gehört Z).

**Größe-Hinweis:** Phase-Head 39.962 B (unter 40-KB-Cap).

**Nächster Schritt, konkret (unverändert gegenüber D4):**

- **D5** — Vierte A3-Probe (Nikinger, wörtlicher Prüfauftrag aus Plan §3 B1 —
  entscheidet §9.4.1 Abbruchregel aus N2).
- **V105** — Connector-Check (Nikinger, echter Anthropic-Connector).
- **Optional vor Z** durch opencode/M3: Radiogruppe-Tausch (P8.5-19, 5 Z. in
  `dialogs.js`+`app.html`) + Bracket-Renderer-Fix (P8.5-6, in `markdown.js`) —
  damit Z die Endabnahme-Zeilen P8.5-6 und P8.5-19 auf ✅ heben kann.
- **Z** (Phase-8.5-Closeout, opencode/M3): wie D4-Block beschrieben — neu ist
  **zusätzlich**: Verweis auf `docs/concepts/p8x_ui_polish_notes.md` als Quelle
  für die p8.X-Ankündigung in `phase8_ui_graph_plan.md §9.4.7` + Eintrag in
  `phase8_ui_graph/CLAUDE.md §7`-Matrix „Phase 8 ✅, p8.X angekündigt, Notizen
  in `docs/concepts/p8x_ui_polish_notes.md`".

---

**Session beendet 2026-09-06 auf Wunsch des Nikingers.** Session-Ende-Notiz,
steht für nächste Sitzung (oder den Nikinger direkt) an:

- **D5** — Vierte A3-Probe (Nikinger, entscheidet §9.4.1 Abbruchregel).
- **V105** — Connector-Check (Nikinger, echter Anthropic-Connector).
- **Optional vor Z** durch opencode/M3 — Radiogruppe-Tausch (P8.5-19, 5 Z.) +
  Bracket-Renderer-Fix (P8.5-6).
- **`git commit`** — Nikinger commitet die uncommitted Working-Tree-Änderungen
  (D4 + D4-Folgesession gemeinsam; +1 neue Datei `docs/concepts/p8x_ui_polish_notes.md`).

Reine Doku-Session — kein Code, keine Tests, kein Service-Touch, kein
`sudo systemctl`; Commit liegt beim Nikinger.
### 2026-09-06 (D4 Sichtprüfung am echten Gerät durch den Nikinger — nur dokumentiert, kein Code-Touch)

**Auftrag:** Notiz-Session für D4. Der Nikinger hat heute die Sichtprüfung am echten Gerät
gegen den D2-Deploy durchgeführt (Hard-Rule-9-konform, opencode/M3 kann das nicht).
Alles in dieser Session **nur dokumentiert** — kein Code-Touch (Hard Rule 9 + §0.3-Tabu
unverändert), keine Tests, kein Service-Touch, kein `git commit`.

**Ergebnis — Vorbereitung + Block 1–7 komplett durchgelaufen, drei echte Funde zum
Festhalten:**

Vorbereitung (Login beide Accounts ✅), Block 1 (Update-Banner `## 2026-09-05` mit den drei
Zeilen sichtbar ✅; Picker-Umschalter vorhanden, beide Modi „als Text-Link" und „als Kante"
funktional ✅; **eckige Klammern im Titel brechen den Link im Preview** — Bug),
Block 2 (Persistenz via `localStorage["sfx:linkpicker:mode"]` ✅, privater Modus wirft nicht),
Block 3 (Tastaturnavigation `aria-activedescendant` in **Firefox + Chrome + Safari** auf
beiden Accounts ✅, geht über die Mindestanforderung Chromium+Firefox hinaus),
Block 4 (Insert-at-cursor Hub Bild-Knopf ✅, Bild erscheint in Vorschau),
Block 5-Kern (Settle-Zeit 2 s unter dem 3-s-Ziel; alle drei Graph-Farben korrekt gerendert;
Knotenklick öffnet das Item im Detail — Phase-8-§9.4.6 Fixes A/B/C regressionsfrei),
Block 6 (zwei Map-Beobachtungen wie geparkt bestätigt: Map-Field schneidet unten ab; Map
„fliegt" bei jedem Reload),
Block 7 (**Nikinger-Entscheidung Phase 8 ✅ + p8.X als Folge-Phase**, weil weitere fixbare
Issues gerade von Fabi gesammelt werden, die über den Sichtprüfungs-Scope hinausgehen).

**Drei echte Findings — jede mit Scope-Entscheidung:**

1. **P8.5-19 — Radiogruppe statt `<select>`.** Wörtlich aus dem Bericht: „Radiogruppe mit
   evtl eindeutigen Icons aber deutlich angenehmer". P8.5-F-Planer-Substitution (Konvention
   v3 hatte `<select>` nahegelegt) wird zurückgedreht. **Tausch 5 Zeilen** in `dialogs.js:584`
   + `app.html:277` — opencode/M3 in einer Folge-Session, vor Z. Icon-Vorschlag:
   Lucide-`link-2` für „als Kante", `pilcrow` (oder `text-cursor-input`) für „als Text-Link" —
   Bestätigung durch Nikinger offen. P8.5-19 bleibt ⬜ bis zum Tausch.

2. **P8.5-6 — Bracket-Renderer-Bug.** Body-Source-Escape `[vgpu \[Vercel\] – Relevanz für
   Sharefyx-UI (Obsidian-ähnliche Notiz-Map)](#item/itm_67bb0565)` ist **korrekt**
   (Backslash-Escape steht im Body), aber der Markdown-Renderer bricht den Link in der
   Vorschau — eckige Klammern zerlegen die URL-Zuordnung, **runde Klammern funktionieren**.
   Evidenz im Live-Datensatz gelassen (Item `itm_67bb0565`).
   **Diagnose:** `phase5_ui/webui/static/js/markdown.js` ist Source-of-Truth des
   Preview-Renderers, der Parser folgt CommonMark für `\[`/`\]` in Link-Text nicht
   (Heuristik „erste `]` schließt den Link" o. ä.). **Echter Bug, Phase-8.5-Scope:**
   §0.3-Tabu verbietet `webui/static/js/` **nicht** — nur `webui/{security,api,
   serializers,permissions}.py` + `storage/` + `authserver/` + `mcpserver/` (mit der
   Hint-Ausnahme). **Hard-Rule-9-Eskalation greift nicht** — Ursache liegt genau dort,
   wo der Fix hinkommt (kein Kaskaden-Problem). Fix-Pfad: lokalisieren, Fix vorschlagen,
   gegen Wegwerf-Instanz throwaway-verifizieren, committen, Health-Gate-Re-Run. Zeile
   bleibt 🟡 bis zum Fix.

3. **UX-2-Step-Knotenklick — neues Feature für p8.X.** Knotenklick öffnet das Item, aber
   „umständlich, da über Browser-Tools zurück navigiert werden muss". Nikinger-Vorschlag:
   **erster Klick öffnet Readonly-Scroll-Vorschau (ESC/Outside-Click schließt), zweiter
   Klick auf die Notiz öffnet sie vollständig**. Ist **kein** Phase-8-Restdefekt,
   **kein** Phase-8.5-Scope — neues UX-Feature für die p8.X-Folge-Phase, in der Fabi
   gerade fixbare Issues sammelt.

**Vier kleinere Punkte — parkiert, kein Phase-8.5-Fix:**

- **Map-Field schneidet unten ab** (`phase5_ui/webui/static/js/graph.js`-Layout, Phase-8-
  Block-D). Parken für p8.X — vom Nikinger in D4 explizit bestätigt, vom D3-Handover
  übernommen.
- **Map „fliegt" bei jedem Reload durcheinander** — kein persistenter Layout-Seed,
  jeder Mount startet mit frischen Random-Kräften. Parken für p8.X — gleiche
  Herkunft wie oben.
- **Save-Button-YAML-Header-Issue**: Picker → `#field-links` modifiziert, aber
  Save-Button unlockt nicht, wenn der Cursor im YAML-Header-Feld sitzt; Workaround
  „einfach Leerzeichen einfügen". Vermutung: `editor.js`-Dirty-Detection ist
  Phase-5-Code, nicht Phase-8.5. **Verifikation steht aus:** wenn der gleiche Bug
  auch außerhalb des Header-Kontexts auftritt (nur Frontmatter-Edit ohne Picker), ist
  es ein Phase-8.5-Fix. Bis dahin parken, wahrscheinlich p8.X.
- **Conflict-Dialog-Verhalten** (im Bericht implizit über „Speicherbutton spam →
  Konflikt-Dialog getestet"): Hard Rule 3 „kein Last-Write-Wins" bewährt sich, der
  Server lehnt den Replay korrekt ab. Kein Befund, nur Notiz.

**Phase-8-Closeout-Entscheidung (für Z vorgemerkt):** Nikinger bestätigt Phase 8 ✅ mit
p8.X als Folge-Phase. „p8.X" sammelt die gerade von Fabi kommenden fixbaren Issues plus
die zwei Map-Beobachtungen plus den UX-2-Step-Knotenklick plus (wahrscheinlich) den
Save-Button-Bug. **Eintrag in `phase8_ui_graph_plan.md §9.4.7` + `phase8_ui_graph/
CLAUDE.md §7`-Matrix** ist Z-Arbeit, kein Phase-8.5-Eingriff.

**Verifiziert (§0.5 Checkliste):**

- `pytest -q`: nicht gelaufen — keine Python-Datei berührt.
- Tabu-Diff §0.3: **leer** — kein `phase4_auth/`/`storage/`/`security.py`/`api.py`/
  `serializers.py`/`permissions.py`/`mcpserver/`-Touch. Auch kein anderer Code-Touch
  (`markdown.js`/`dialogs.js`/`editor.js`/`graph.js`/`app.html`/`app.css` unangetastet).
- `bash -n`/`node --check`/`ui_budget.py`: irrelevant — keine Code-Änderung.
- Service-Touch **0**. `systemctl show sharefyx-mcp.service` vom 2026-09-05 16:10:18
  CEST / PID 355956 ist weiterhin der letzte gelesene Stand (Hard Rule 9 + §0.5.7).
- Größenprüfung: kein neues `.md`-File → keine INDEX-Zeile nötig. **`phase8_5_picker_
  release/CLAUDE.md` 37.831 B** (D3-Block 154 Z. raus, neuer Block ~140 Z. rein —
  leicht kürzer als D3 trotz dreier Findings-Dokumentation; mit Modul-Status-Erweiterung
  netto +2 KB auf ~37.8 KB, **bleibt unter dem 40-KB-Softcap**).
- **`docs/INDEX.md` 44.784 B + `CLAUDE.md` (Wurzel) 47.999 B** — weiterhin über dem
  40-KB-Softcap, **benannt seit D3, Auflösung bleibt eine P8-Entscheidung aus Z**,
  nicht diese Session.

**Doku-Updates im selben Commit (Hard Rule 8):**

- `phase8_5_picker_release/CLAUDE.md`: dieser Block (alter D3-Block 154 Zeilen ins
  Archiv); Modul-Status-Zeile 6 Block D um D4 ✅ erweitert (mit Findings-Anhang);
  P8.5-6-Zeile um Bracket-Bug-Caveat; P8.5-17-Zeile Update-Banner-live jetzt ✅;
  Summary-Zeile 3 ✅ · 14 🟡 · 3 ⬜ unverändert (P8.5-6 bleibt 🟡 weil Fix ausstehend,
  P8.5-17 bleibt 🟡 weil V105 noch offen); `updated:`-Pipe vorne ergänzt.
- `phase8_5_picker_release/SESSIONS_ARCHIVE.md`: D3-Block vorne angehängt (verbatim);
  `updated:`-Pipe vorne ergänzt.
- `docs/INDEX.md`: Phase-8.5-Header um D4 ✅ erweitert; Phase-8.5-Bullet um die drei
  Findings verkürzt; `updated:`-Pipe vorne ergänzt.
- `ROADMAP.md`: Phase-8.5-„nächster Schritt" von „D4 — Sichtprüfung" auf
  „D5 + V105 (Nikinger), optional vor Z Radiogruppe-Tausch + Bracket-Fix durch
  opencode/M3, dann Z (mit Phase-8 ✅ + p8.X)" umgestellt; `updated:`-Pipe vorne
  ergänzt.
- `CLAUDE.md` (Wurzel): neuer Current-state-Absatz vom 2026-09-06 für D4;
  `updated:`-Pipe vorne ergänzt.

**Was diese Session bewusst NICHT tat:**

- Kein Code-Touch (kein `dialogs.js`/`app.html`/`markdown.js`/`editor.js`/`graph.js`).
- Kein Deploy, kein `sudo systemctl`, keine `systemctl show` (Hard Rule 9 + P8.5-Q;
  letzte Werte vom 2026-09-05 16:10:18 CEST / PID 355956 reichen für die Übergabe).
- Kein `pytest`/`node --check`/`bash -n`/`ui_budget.py` — irrelevant ohne Code-Touch.
- Kein Browser-/Funnel-/Connector-Test — der Nikinger hat alles gemacht.
- Kein `git commit` — alle Edits bleiben offen, nächste Session oder Nikinger committet.
- Kein neuer Funnel-Test, keine Anthropic-Connector-Probe — bleibt V105 (Nikinger).
- Kein Doku-Audit für die früheren Phasen (`phase8_ui_graph/CLAUDE.md` weiterhin über
  40-KB-Softcap — benannt seit Step 0.4, Auflösung bleibt eine Phase-8-Entscheidung
  aus Z).

**Nächster Schritt, konkret (offene Nikinger-Aktionen, dann opencode/M3-Z):**

- **D5** — Vierte A3-Probe (Nikinger, wörtlicher Prüfauftrag aus Plan §3 B1 — entscheidet
  §9.4.1 Abbruchregel aus N2).
- **V105** — Connector-Check (Nikinger, echter Anthropic-Connector).
- **Optional vor Z** durch opencode/M3: Radiogruppe-Tausch (P8.5-19, 5 Z. in
  `dialogs.js`+`app.html`) + Bracket-Renderer-Fix (P8.5-6, in `markdown.js`) — damit Z
  die Endabnahme-Zeilen P8.5-6 und P8.5-19 auf ✅ heben kann.
- **Z** (Phase-8.5-Closeout, opencode/M3): `docs/concepts/phase8_5_picker_release_plan.md
  §9` füllen (P8.5-T); Nachtrag in `phase8_ui_graph_plan.md §9` + `§9.4.7` (Phase 8 ✅,
  Glyph-Entscheidung, p8.X-Ankündigung); `phase8_ui_graph/CLAUDE.md §7`-Matrix +
  Session-Block; dieser Head final; INDEX/ROADMAP/Wurzel-`CLAUDE.md` nachziehen (Hard
  Rule 8); Größenprüfung mit den zwei benannten Softcap-Überschreitungen (Wurzel-
  CLAUDE.md 47.999 B, INDEX 44.784 B) als P8-Entscheidung dokumentieren, nicht still
  trimmen.

### 2026-09-05 (D3-Vorbereitung — Health-Gate-Skript + Discovery: D2 lief bereits)

**Auftrag:** D3-Werkzeug bauen als Option 2 der Vorlage (Health-Gate-Skript). Beim
ersten Probe-Lauf gegen den laufenden Dienst stellte sich heraus: **D2 ist bereits
gelaufen** — `/opt/sharefyx/current` → `20260905T140325.378914Z` → HEAD `6f19a8f`
(D1-Commit) mit Badge `v3.0.1` im `app.html`, Service-PID **355956** statt 195922
(wie im D1-Block notiert), `ExecMainStartTimestamp=2026-09-05 16:10:18 CEST`. Der
Nikinger hat D2 still durchgeführt zwischen D1 (Commit heute früh) und dieser
Session. Damit ist D3 nicht mehr Vorbereitung, sondern **Verifikation des bereits
deployten v3.0.1**.

**Ergebnis — `phase8_5_picker_release/scripts/health_gate.sh` neu, ein Lauf-Beleg:**

1. **Skript** (134 Zeilen, bash, `set -uo pipefail`, JSON auf stdout / Details auf
   stderr nach Hard Rule 7). Acht Gates:
   - `/health` 200 mit Retry-Loop (max `--max-wait` Sekunden, Default 30 — wie
     `deploy.sh` Z. 192-200)
   - `/ui/login` 200, `/api/v1/me` 401, `/mcp/` 401 (wie `deploy.sh` Z. 202-217)
   - `.rail__version` aus `/ui/static/app.html` (**nicht** `/ui/login` — das ist
     `pages.py`s Auth-Template und enthält keine Rail; erste Iteration fiel darauf
     herein, dann gefixt)
   - `/opt/sharefyx/current` → Release-Verzeichnis mit `.git`
   - Optional `--require-todays-update-log`: oberster `## YYYY-MM-DD` in
     `docs/UPDATE_LOG.md` == heute (UTC oder local, wie `deploy.sh` Z. 127-131)
   - Optional `--expected-sha=<hex>`: Release-SHA matched Short- oder Full-Form
     (Prefix-Vergleich, sonst wäre `git log --oneline`-Output nicht verwendbar)

2. **Lauf-Beleg, 2026-09-05 15:19:53Z** mit `--require-todays-update-log
   --expected-sha=6f19a8f` (Default sonst): **8/8 grün**, Exit 0, JSON auf stdout
   (`{"action":"health_gate","result":"ok","expected_version":"v3.0.1",
   "actual_version":"v3.0.1","active_release":"/opt/sharefyx/releases/
   20260905T140325.378914Z","release_sha":"6f19a8fc1f0bcdc2c3bc91fc934a057964647ed4",
   "port":8765}`). Drei Negativproben separat verifiziert (Port 9999 → Gate 1 rot,
   `--expected-version=v9.9.9` → Gate 5 rot, `--expected-sha=0000000` → Gate 8 rot).
   **P8.5-17 teilweise abgehakt:** Deploy gelaufen ✅, Health-Gate 8/8 ✅, Badge
   `v3.0.1` live ✅, Update-Banner-Live-Anzeige ⬜ (braucht Auth, Nikinger), V105 ⬜
   (echter Anthropic-Connector, Nikinger).

**Verifiziert (§0.5 Checkliste):**

- `pytest -q`: nicht gelaufen — keine Python-Datei berührt.
- Tabu-Diff §0.3: **leer** (kein `phase4_auth/`/`storage/`/`security.py`/`api.py`/
  `serializers.py`/`permissions.py`/`mcpserver/`-Touch).
- `bash -n phase8_5_picker_release/scripts/health_gate.sh`: OK.
- `shellcheck`: nicht auf dieser Maschine verfügbar, übersprungen — keine
  `shellcheck`-Konvention im Repo (`phase3_edge/scripts/diagnose.sh` wurde ebenfalls
  nie damit geprüft, vgl. `phase3_edge/CLAUDE.md` Modul-Status Zeile 7).
- `node --check`: irrelevant — kein JS-Touch.
- `ui_budget.py`: nicht gelaufen — keine UI-Reichweiten-Änderung.
- Fehlerpfad: drei Negativproben durchgespielt (Port nicht erreichbar, falsche
  Version, falscher SHA) — Exit 1 mit präziser Diagnose im `reason`-Feld des
  JSON-Outputs.
- Größenprüfung: Skript 134 Zeilen / ~4,5 KB, kein `.md`-File neu → keine
  INDEX-Zeile nötig (Skripte sind in keinem Phase-Head-Card-Block separat gelistet,
  vgl. `phase5_ui/scripts/{deploy,rollback,authbackup,restore_auth_check}.sh` ohne
  eigene INDEX-Zeile). **`phase8_5_picker_release/CLAUDE.md` 32.672 B** —
  Schrumpfung um ~5 KB durch die D1-Rotation (D1-Block 111 Zeilen raus, neuer
  Block 130 Zeilen rein, beide ähnlich lang; der leichte Zuwachs ist im neuen
  Modul-Status-Text für D2/D3 und der ausführlicheren P8.5-17-Zeile). **`docs/
  INDEX.md` 44.784 B** — weiterhin über dem 40-KB-Softcap, **benannt statt
  versteckt** (war schon vor D1 41.720 B; diese Session fügt eine Bullet-Erweiterung
  + Header-Update hinzu, +3 KB netto). **`CLAUDE.md` (Wurzel) 47.999 B** — auch
  über Cap, neuer Current-state-Absatz für D3 trägt ~3 KB bei; war schon vor
  D3 41.720 B. Beide Über-Cap-Dokumente sind 📗 live (nicht exempt); nächste
  sinnvolle Trimmung ist eine eigene Entscheidung (DOC_LAYERS_CONVENTION §„eine
  Datei pro Cap-Verstoß benennen"), nicht diese Session.
- Service-Touch **0**. `systemctl show sharefyx-mcp.service` → `MainPID=355956`
  (anders als der D1-Block notierte 195922 — der D2-Deploy hat den Dienst
  erwartungsgemäß neu gestartet), `ExecMainStartTimestamp=Sat 2026-09-05 16:10:18
  CEST` — nur gelesen, keine Änderung.

**Doku-Updates im selben Commit (Hard Rule 8):**

- `phase8_5_picker_release/CLAUDE.md`: D1-Block (111 Zeilen) nach `SESSIONS_ARCHIVE.md`
  rotiert (manuell, das Skript passt nicht auf das Phase-8.5-Muster — bewährtes
  Vorgehen aus D1 selbst); neuer Session-Block (dieser); Modul-Status-Zeile 6 Block
  D um D2 ✅ und D3 🟡 erweitert; Abnahmestand-Zeile P8.5-17 auf 🟡 (C/L-Mix);
  Summary-Zeile auf 3 ✅ · 14 🟡 · 3 ⬜ korrigiert; `updated:`-Pipe ergänzt.
- `phase8_5_picker_release/SESSIONS_ARCHIVE.md`: D1-Block vorne angehängt
  (newest-first, vor Block C); Frontmatter `updated:` ergänzt.
- `docs/INDEX.md` Phase-8.5-Header: `🔄 A1/A2/B1/C/D1 🟡, D2–D5/Z ⬜` →
  `🔄 A1/A2/B1/C/D1 🟡, D2 ✅, D3 🟡, D4–D5/V105/Z ⬜`; Phase-8.5-Bullet unter
  `## Phase 8.5` mit Health-Gate-Skript und aktualisiertem Modul-Status ergänzt;
  `updated:`-Pipe ergänzt.
- `ROADMAP.md` Phase-8.5-Absatz: D2/D3-Status nachgezogen, neuer Block „**[2026-09-05,
  D3-Prep committet]**" vor „## Bewusst nicht auf der Roadmap" angehängt, „nächster
  Schritt" aktualisiert auf „D4 Sichtprüfung + D5 Vierte A3-Probe + V105-Connector-
  Check, dann Z"; `updated:`-Pipe ergänzt.
- `CLAUDE.md` (Wurzel): neuer „Current state"-Absatz vom 2026-09-05 für D3-Prep;
  `updated:`-Pipe ergänzt.

**Was diese Session bewusst NICHT tat:**

- Kein `git commit` — der Commit wartet bis alle fünf Doku-Updates durch sind
  (Hard Rule 8 + System-Prompt „kein Auto-Commit"). Übergabe an den Nikinger am Ende
  der Session mit `git add` und Commit-Empfehlung.
- Kein Deploy, kein `sudo systemctl` (Hard Rule 9 + P8.5-Q) — D2 lief bereits vor
  dieser Session, ich habe nur verifiziert.
- Kein `app.js`/`dialogs.js`/`editor.js`/`app.css`-Touch — nur Bash-Skript.
- Kein Python, kein `pytest`-Lauf.
- Kein Service-Touch — `sharefyx-mcp.service` läuft seit 2026-09-05 16:10:18 CEST
  (PID 355956), ich habe nur gelesen.
- Keine V105-Probe (echter Anthropic-Connector), keine Update-Banner-Live-Probe
  (braucht Auth) — beide bleiben Nikinger-Aktionen wie im Plan §5 D3.
- Kein Doku-Audit für die früheren Phasen (`phase8_ui_graph/CLAUDE.md` driftet
  weiterhin über 40 KB-Softcap — benannt seit Step 0.4, Auflösung bleibt eine
  Phase-8-Entscheidung aus Z, nicht diese Session).

**Nächster Schritt, konkret:** D4 — **Sichtprüfung am echten Gerät durch den
Nikinger** (Hard-Rule-9-konform, ich kann das nicht). Vorbereitet ist:
- Health-Gate-Skript (Verifikation gelaufen, 8/8 grün).
- D2-Deploy ist nachweislich live (PID 355956, Badge v3.0.1, Update-Log-Eintrag
  heute).
- Block-C-v3-Vorabritt war 26/26 grün gegen eine Wegwerf-Instanz.

Was D4 noch braucht: das `## 2026-09-05`-Eintrag im Update-Banner muss im Browser
sichtbar sein, das `<select class="input" id="link-picker-mode">` im Picker muss
da sein (P8.5-19-Abnahme: Radiogruppe oder `<select>`-Bestätigung), die drei Fixes
(A1 Body-Modus, A2 Tastatur, B1 generalisierter Hint) müssen optisch wie in Block C
verifiziert sein. Danach D5 (Vierte A3-Probe), Z (Closeout).

**Aus dem echten Betrieb mitgekommen (Nikinger, 2026-09-05, Sichtprüfung 2/3?) —
Beobachtungen geparkt für Plan §9 / Z:** zwei Punkte zur Map-Ansicht
(`phase5_ui/webui/static/js/graph.js`, Phase-8-Block-D, **P8.5 §0.3 tabu — kein
stiller Fix in D3-Prep**):

1. **Map-Field schneidet unten ab, zeigt nur solid color.** Layout- oder
   Canvas-Resize-Problem (vermutlich `.rail__main`/`.graph-canvas`-Höhe oder
   `position:absolute` ohne Bodem-Anker). Keine Code-Probe in dieser Session.
2. **Map „fliegt" bei jedem Neuladen durcheinander.** Force-Graph hat keinen
   stabilen/persistenten Layout-Seed; jeder Mount startet mit frischen Random-
   Kräften. Der Phase-8-§9.4.6-Settle-Zeit-Fix hat die Konvergenz auf < 3 s
   gebracht, aber **keine Persistenz** — eine Folge-Sitzung sieht jedes Mal ein
   anderes Layout. Wurde am 2026-09-02 throwaway-verifiziert (Phase 8 `p8_22_smoke.py`
   zeigt 5/5 grün), im Live-Betrieb aber sichtbar als „verwirrende Form".

Bezug zu P8.5: nicht Bestandteil dieser Phase (P8.5 §0.4 DRAUSSEN — Phase-8-§9.4.6-
Funde sind bereits am 2026-09-02 geschlossen). Aber als **offene Beobachtungen für
Phase 8 / §9 dieses Plans** festgehalten, weil Z genau diese Art von „echter-Betrieb-
Befund" in den Closeout-Nachtrag einordnen können soll.

**Empfehlung für nächste Session (Übergabe an Nikinger + Z):** zwischen D3 und Z
**nichts Offenes mehr für opencode/M3** — D4 (Sichtprüfung am echten Gerät), D5
(Vierte A3-Probe, entscheidet §9.4.1 Abbruchregel) und V105 (echter Anthropic-
Connector) sind **alles Nikinger-Aktionen**. Sobald die drei abgehakt sind, kann Z
(Phase-8.5-Closeout, opencode/M3) starten mit: (a) §9 dieses Plans füllen
(P8.5-T — Status/Delta/Abnahmestand/Restdefekte mit den zwei Map-Beobachtungen
oben/`[VERIFY]` V95–V105-Bilanz); (b) Nachtrag in `phase8_ui_graph_plan.md` §9 +
§9.4.7 (P8.5-R/N6 — Phase 8 formal abschließen, Glyph-Entscheidung); (c)
`phase8_ui_graph/CLAUDE.md` §7-Matrix + Session-Block nachziehen; (d)
`phase8_5_picker_release/CLAUDE.md` Modul-Status + Abnahmematrix final; (e)
Größenprüfung mit den zwei benannten Softcap-Überschreitungen (Wurzel-CLAUDE.md
47.999 B, docs/INDEX.md 44.784 B) als P8-Entscheidung dokumentieren, nicht still
trimmen.

### 2026-09-05 (D1 — Release-Vorbereitung opencode/M3: Badge v3.0→v3.0.1, drei Zeilen Update-Log)

**Auftrag:** D1 nach `docs/concepts/phase8_5_picker_release_plan.md` §5. Vorbereitung des
Deploys v3.0 → v3.0.1 (P8.5-P, P8.5-N7): Badge-Bump in `phase5_ui/webui/static/app.html:20`
und drei menschenlesbare Zeilen oben in `docs/UPDATE_LOG.md` (sonst bricht `deploy.sh` am
Gate P6-X, Z. 117–131). D2 (Deploy), D3 (Health-Gate), D4 (Sichtprüfung am echten Gerät +
P8.5-19-Abnahme) und D5 (Vierte A3-Probe) bleiben Nikinger-Aktionen — D1 selbst ist die
einzige opencode/M3-Teilhandlung in Block D.

**Ergebnis — drei kleine Eingriffe, §0.5-Checkliste durchgegangen:**

1. **`phase5_ui/webui/static/app.html:20`.** `.rail__version` von `v3.0` → `v3.0.1`
   (P8.5-N7, dritte Stelle = Step-Nummer, Konvention aus Phase 8 v2.2.3 = Phase-8-Step-3
   fortgeführt). Statisches HTML ist nicht in der Phase-8.5-Tabu-Liste (§0.3), keine
   P1-Contract-Auswirkung.

2. **`docs/UPDATE_LOG.md`.** Neuer `## 2026-09-05`-Block ganz oben mit drei `- `-Zeilen
   (Picker-Modi / Tastatur / Generalisierter Hint). **Datums-Drift zur Block-C-Spec
   ausdrücklich dokumentiert:** Block-C-Session-Block hatte `## 2026-09-04` vorgeschlagen
   (geschrieben am 2026-09-04). Heute ist 2026-09-05 (`date +%F`, lokales System-Datum
   stimmt mit `date -u +%F` überein). `deploy.sh` Z. 117–131 verlangt strikt `today_utc`
   oder `today_local` als oberstes Datum, sonst Abbruch — Eintrag deshalb auf 2026-09-05
   datiert. Die Drift ist eine bewusste Korrektur, kein Drift-Befund.

3. **Rotation per Hand.** Block-C-Block (176 Zeilen, `### 2026-09-04 (Block C — ...)` mit
   dem ganzen v3-Vorabritt-Bericht) nach `SESSIONS_ARCHIVE.md` vor B1 verschoben
   (newest-first). Das Skript `scripts/rotate_session_block.sh` passt nicht auf das
   Phase-8.5-Muster: es zählt `^## Session stopped`-Header, das Phase-8.5-Layout hat
   aber genau **einen** solchen Header mit **mehreren** `### date`-Subblöcken darunter
   (statt der älteren Phasen mit wiederholten `## Session stopped`-Headern). Ergebnis:
   `STARTS == 1`, Exit 2 „Bereits konform" — das Skript ist nicht falsch, nur für
   dieses Layout nicht anwendbar. Manuelle Rotation folgt dem Muster der vier
   vorherigen Schritte (Step 0 → A1 → A2 → B1 → C); im B1-Block-Vermerk steht:
   „Skript `scripts/rotate_session_block.sh` jetzt vorhanden und gegen den Phase-Head
   getestet, aber der YAGNI-Stand aus A1/A2 gilt für die zweite Rotation nicht mehr,
   sobald Block D abgeschlossen ist" — der YAGNI-Stand ist überholt, das Layout-Problem
   ist geblieben.

**Verifiziert (§0.5 Checkliste):**

- `pytest -q` (venv): **nicht gelaufen** — keine Python-Datei berührt. Letzter grüner
  Lauf war Block-C mit 962/962, unverändert.
- Tabu-Diff §0.3: **leer** (`git diff --stat main -- phase4_auth/ phase1_storage/storage/
  phase5_ui/webui/security.py phase5_ui/webui/api.py phase5_ui/webui/serializers.py
  phase5_ui/webui/permissions.py phase2_mcp/` → keine Zeile; `app.html` und
  `docs/UPDATE_LOG.md` sind beide nicht tabu).
- `node --check`: keine JS-Datei berührt (irrelevant).
- `ui_budget.py`: **nicht gelaufen** — D1 ändert nur HTML-Text und Markdown, keine
  JS-/CSS-Reichweite (`app.html:20` ist eine reine Text-Ersetzung; `app.css:371`
  `.rail__version`-Regel unangetastet).
- Größenprüfung: `docs/UPDATE_LOG.md` jetzt 67 Zeilen / 5571 B (war 62 / 5210 B, +5
  Zeilen für den neuen Block); `phase8_5_picker_release/CLAUDE.md` schrumpft leicht
  (D1-Block kürzer als der rotierte Block-C-Block); `docs/INDEX.md` wächst um die
  neue `updated:`-Eintragung und bleibt **weiterhin** über dem 40-KB-Softcap (siehe
  Wurzel-CLAUDE.md-Current-state vom 2026-09-04 — INDEX war schon vor D1 41.720 B,
  keine neue Drift).
- Fehlerpfad einmal durchgedacht: `deploy.sh` Gate prüft nur das oberste `##`-Datum,
  nicht die Bullets; wenn die Zeilen unterhalb leer wären, schlüpfe ein leerer Eintrag
  durch — aber die drei Bullets stehen drin, das Banner rendert normal. LocalStorage-
  Eskalation aus P8.5-A1 (`sfx:linkpicker:mode`) bleibt unangetastet (D1 ist kein
  JS-Touch).
- Service-Touch **0**. `systemctl show sharefyx-mcp.service -p MainPID,ActiveEnterTimestamp`
  → `MainPID=195922`, `ActiveEnterTimestamp=Wed 2026-09-02 11:51:57 CEST` — nur
  gelesen, keine Änderung.

**Doku-Updates im selben Commit (Hard Rule 8):**

- `phase8_5_picker_release/CLAUDE.md`: Modul-Status-Zeile D `⬜` → `🟡` (D1 fertig;
  D2–D5 als Nikinger-Aktionen in derselben Zeile vermerkt); `updated:`-Pipe ergänzt.
- `phase8_5_picker_release/SESSIONS_ARCHIVE.md`: Block-C-Block vorne angehängt
  (newest-first, vor B1); Frontmatter `updated:` ergänzt; `## Session stopped`-Wrapper
  entfällt (Archiv-Einträge sind nur `### date`-Subblöcke, konsistent mit den vier
  vorherigen Rotationen).
- `docs/INDEX.md` Phase-8.5-Header: `🔄 A1 🟡, A2 🟡, B1 🟡, C 🟡, D/Z ⬜` →
  `🔄 A1/A2/B1/C/D1 🟡, D2–D5/Z ⬜`; Phase-8.5-Bullet unter `## Phase 8.5` mit dem
  D1-Stand aktualisiert (Modul-Status D 🟡, Datums-Drift dokumentiert, neuer
  Session-Block); `updated:`-Pipe ergänzt.
- `ROADMAP.md` Phase-8.5-Absatz: Datums-Drift `## 2026-09-04` → `## 2026-09-05` für den
  Update-Log-Eintrag dokumentiert; „nächster Schritt: Block D" → „D1 (Vorbereitung)
  committet; nächster Schritt: D2 (Deploy als Nikinger-Aktion) + D3–D5";
  `updated:`-Pipe ergänzt.
- `CLAUDE.md` (Wurzel): neuer „Current state"-Absatz vom 2026-09-05 für D1;
  `updated:`-Pipe ergänzt.

**Was diese Session bewusst NICHT tat:**

- Kein `git commit` — der Commit wartet bis alle sechs Doku-Updates durch sind (Hard Rule 8).
- Kein `deploy.sh`-Aufruf — D2 ist Nikinger-Aktion (P8.5-Q + Hard Rule 9).
- Kein `app.js`/`dialogs.js`/`editor.js`-Touch — nur statisches HTML + Markdown.
- Kein neues Python-Modul — D1 ist absichtlich reines Doku-/Badge-Work.
- Kein `mcpserver/`, `storage/`, `authserver/`, `security.py`/`api.py`/`serializers.py`/
  `permissions.py`-Touch — Tabu-Diff §0.3 ist nachweislich leer.
- Kein Service-Touch — `sharefyx-mcp.service` läuft seit 2026-09-02 11:51:57 CEST
  unangetastet.

**Nächster Schritt, konkret:** D2 — **Deploy als Nikinger-Aktion.** Voraussetzungen aus
D1 sind im selben Commit auf `main`: Badge `v3.0.1`, Update-Log-Eintrag vom heutigen
Tag. Aufruf in einer interaktiven Vordergrund-Shell:

```
SHAREFYX_SYSTEMCTL="sudo systemctl" phase5_ui/scripts/deploy.sh main
```

V103 prüft, dass der `sudo`-Prompt sichtbar wird (Hard Rule 9, niemals
`sudo systemctl` durch opencode/M3). Nach D2 folgen D3 (Health-Gate 3/3 + V105),
D4 (Sichtprüfung am echten Gerät + P8.5-19-Abnahme des `<select>`-Modus-Selektors),
D5 (Vierte A3-Probe, entscheidet §9.4.1 Abbruchregel aus N2), Z (Closeout: Plan §9
füllen, Nachtrag in `phase8_ui_graph_plan.md` §9 + §9.4.7, Phase-8-Head §7-Matrix
aktualisieren, Größenprüfung).

### 2026-09-04 (Block C — v3-Vorabritt gegen eine Wegwerf-Instanz, 26/26 grün)

**Auftrag:** Block C nach `docs/concepts/phase8_5_picker_release_plan.md` §4. Voller
v3-Vorabritt über alle 13 Stationen gegen eine Wegwerf-Instanz (Port 18773). Plan §4
listet die 13 Stationen 1:1 (Login → Counter-Chip → globaler Scope → Graph →
Knotenklick → Picker-Modi → Speichern+V102 → Typografie/Icons →
Reduced-Transparency → Reduced-Motion → Reauth-Endpoint). Jeder Fund entweder behoben
oder als benannter Befund vorgelegt (Plan §4.C3); C/D fallen nie unter Druck.

**Ergebnis — 26/26 Stationen grün (Chromium 13/13 + Firefox 13/13), drei echte Befunde
vorgelegt, keine Code-Fixes im Tabu-Bereich nötig:**

1. **`scripts/rotate_session_block.sh` aus `scripts/` nach
   `phase8_5_picker_release/scripts/` portiert** (Root-Skript ist generisch, kein
   Adaptieren nötig — `head -n 160 phase8_5_picker_release/CLAUDE.md | bash
   scripts/rotate_session_block.sh phase8_5_picker_release .` ergäbe `Bereits konform:
   genau ein Session-Block im Head` als Exit-2-Quittung, YAGNI-Vermerk aus A1/A2
   geschlossen).

2. **`phase8_5_picker_release/scripts/wegwerf_setup_v3ritt.py` neu** (Vorbild
   `phase8_ui_graph/scripts/wegwerf_setup_sichtpruefung2.py`, Bauart nicht erfunden —
   Standing-Permission-Muster aus Phase 8 reproduziert):
   - **Port 18773** (V98, 18766–18772 waren Phase 8).
   - **Wurzel** `/tmp/opencode/sharefyx-wegwerf-v3ritt`, `tmp`-DATA_ROOT,
     `tmp`-`auth.sqlite3`, File-Keyring (`nikinger-space` nicht angefasst), User direkt
     in `auth.sqlite3` provisioniert (kein `provision_user.py`, kein
     `keyring.set_password`).
   - **3 Spaces** (Plan §4.1 exakt): `alpha` (eigen), `beta` (geteilt, `--write` für
     `alpha`), `gamma` (fremd, nur `--read`).
   - **30 Items** über die drei Spaces: 12 alpha + 10 beta + 8 gamma.
   - **8 Items in Ordnern** (≥ 6 erfüllt), **1 archiviert**
     (`alpha:Retro-Notizen`, `status="archived"` über `Store.create(status="archived")`
     — siebte P1-Contract-Öffnung aus P7), **1 mit item-level
     `share_read=["gamma"]`** (`alpha:Empfehlungen Nikinger`, der Deploy-Blocker-Fall
     aus P6 §35–39), **1 mit Bild-Asset** (`alpha:Tagesnotizen`, `put_asset()` →
     `_assets/itm_*/ast_351d4217.png`, 1x1-PNG via `struct`+`zlib` zusammengebaut, 67 B;
     Body mit `![Skizze](asset:ast_351d4217)`-Referenz).
   - **11 explizite Kanten** (6 via Frontmatter `links:` + 3 via Body-Refs in beide
     Richtungen ergibt 4 Unique-Einträge nach `Store.update()`-Deduplizierung +
     1 V102-Zwillings-Kante `Buecherliste Q4` ↔ `Empfehlungen Nikinger` mit
     body+frontmatter).
   - **shared-write** auf beta, **shared-read-only** auf gamma — exakt Plan §4.1.
   - `add-member`-Warnungen („alpha ist kein bekannter Space-Name") beim Schreiben von
     `.share.yml` sind write-time, nicht read-time; `.share.yml` enthält `alpha`
     korrekt, sobald das erste Item in alpha angelegt ist.

3. **`phase8_5_picker_release/scripts/v3_ritt_playwright_smoke.py` neu** (~720 Zeilen,
   `pyotp`+`async_playwright`, 16 Screenshots
   `docs/screenshots/v3ritt_{chromium,firefox}_NN_*.png`):
   - **26/26 Stationen grün** (Chromium 13/13 + Firefox 13/13).
   - **V101 beantwortet** für beide Browser — `role="combobox"` + `aria-activedescendant`
     auf `<input type="search">` funktioniert in Chromium UND Firefox, `ArrowDown` setzt
     `aria-selected="true"` und `aria-activedescendant` auf den ersten Treffer, ein
     zweites `ArrowDown` wandert weiter, `ArrowUp` am oberen Ende bleibt bei 0 (kein
     Wrap), Neu-Tippen setzt den Cursor zurück (`aria-selected=0`,
     `aria-activedescendant=None`).
   - **V102 gemessen:** Buecherliste ↔ Empfehlungen Nikinger zeigen 2 Linien
     (kinds=`['body', 'frontmatter']`), **kein** Cross-`kind`-Dedup in `index.py ::
     replace_item_links` (Plan §0.4 DRAUSSEN, nur messen, nicht fixen — Befund für
     Step Z vorgemerkt).

**Drei echte Befunde, keine Code-Fixes im Tabu-Bereich nötig:**

- **Smoke-Bug** (gefixt in dieser Session): Edge-Keys waren `src`/`dst` (konsistent
  mit `graph.js:325/394` und `webui/api.py :: _graph_get` Z. 719), nicht `src_id`/
  `dst_id` wie im ersten Smoke-Wurf angenommen. Erst beim V102-Vergleich
  aufgefallen — Smoke korrigiert, **kein Server-Bug**. Der Fund bestätigt
  gleichzeitig, dass `graph.js` und die Server-Antwort konsistent sind.

- **CSRF-Origin-Mismatch zwischen Wegwerf und Server** (`webui/security.py :: require_csrf`
  Z. 82–92): die Wegwerf-UI läuft auf `http://127.0.0.1:18773`, der Browser sendet
  `Origin: http://127.0.0.1:18773`, der Server erwartet aber `https://wegwerf-v3ritt.invalid`
  (aus `SPACE_PUBLIC_BASE_URL`). `_validate_base_url` in `phase4_auth/authserver/config.py`
  Z. 85–87 erzwingt `https://`, also kein Workaround ohne Server-Code-Touch (Tabu).
  Konsequenz: jeder `fetch()` mit POST/PATCH aus dem Browser-Kontext wird abgewiesen,
  das macht Station 13 (P8-1-Reauth-Grant-Mechanismus) im Wegwerf unscharf — wir
  konnten Endpoint-Erreichbarkeit und UI-Markup prüfen, aber den eigentlichen
  Batch-Grant-Roundtrip nicht. **Befund für Step Z / Plan §4.C3:** der Live-Nikinger-
  Domain-Test in Block D fängt das auf (V105), und die Setup-`SPACE_PUBLIC_BASE_URL`
  sollte für künftige Wegwerfs gleich der Server-URL sein (z. B.
  `http://127.0.0.1:18773` nach Bypass von `_validate_base_url` per
  `--base-url`-Override, oder eine Test-Config mit `https://*.invalid` aber
  `_validate_base_url` ist Pflicht — Folge-Session-Diskussion).

- **Pickstation 12 nur strukturell** (`@media (prefers-reduced-motion)` als Regel im
  CSS gefunden, aber keine echte Browser-Probe mit umgeschaltetem UA). War schon in
  Phase 8 `p8_22_smoke.py` throwaway-verifiziert (Fix A, 2,7 s statt 5,95 s); bleibt
  so — Abnahme-Status 🟡 mit Klammer-Anmerkung wie P8-16 / P8-22.

- **Modus-Selektor `<select>` vs. N3-Vorschau-`<input type="radio">`: nicht als Befund
  behandelt** — die N3-Entscheidung war „Umschalter im Dialog" (P8.5-E), die Bauform
  `<select>` ist eine Planer-Substitution (P8.5-F), die der Nikinger in Block D4 am
  echten Gerät abnimmt (Abnahmezeile P8.5-19). Im Smoke getestet: Modus-`body` ist
  Default, Wechsel auf `frontmatter` schreibt `sfx:linkpicker:mode` in `localStorage`
  (try/catch für privaten Modus vorhanden, aber nicht direkt geprüft).

**Verifiziert (§0.5 Checkliste):**

- `pytest -q` (venv): **962 passed in 266.25 s** — 962 unverändert (kein Python-Touch
  im Block-C-Setup, kein `phase5_ui/webui/`-Touch im Smoke).
- Tabu-Diff §0.3: **leer** (`git diff --stat main -- phase4_auth/ phase1_storage/storage/
  phase5_ui/webui/security.py phase5_ui/webui/api.py phase5_ui/webui/serializers.py
  phase5_ui/webui/permissions.py phase2_mcp/` zeigt keinen Eintrag).
- `node --check`: keine JS-Datei in dieser Session berührt (irrelevant).
- Größenprüfung `find . -name "*.md" -not -path "./.venv/*" -size +40k`: kein neuer
  Treffer durch diese Session; `phase8_5_picker_release/CLAUDE.md` weiterhin
  deutlich unter dem 40-KB-Softcap.
- Fehlerpfad einmal durchgedacht: der `preview`-Mode des Editors (`editor.js:239`,
  `editorTextareaEl.hidden = mode !== "edit"`) macht die Textarea initial unsichtbar,
  obwohl `#detail-editor` selbst sichtbar ist — das hat den ersten Smoke-Wurf in
  Station 6 verwirrt. Behoben mit `_ensure_edit_mode()`-Helfer, der `#toggle-preview`
  klickt, falls der Button-Text „Bearbeiten" ist (= Preview-Modus), und das Meta-Panel
  `<details>` aufklappt (enthält `#link-picker-button`). Beide Helfer sind idempotent
  (Station 7/8 rufen sie erneut auf, kein Effekt).
- Service-Touch **0** während der Ritte. `systemctl show sharefyx-mcp.service -p
  MainPID,ActiveEnterTimestamp` → `MainPID=195922`,
  `ActiveEnterTimestamp=Wed 2026-09-02 11:51:57 CEST` — vor dem ersten Ritt und nach
  dem Cleanup des Wegwerfs identisch. `Wegwerf-Server gesund nach 1.8s` beim Start,
  sauber abgebaut mit `kill -TERM $(cat serve.pid)` (Hard Rule 9-konform, kein
  `pkill -f`, kein `systemctl`).

**Doku-Updates im selben Commit (Hard Rule 8):**

- `phase8_5_picker_release/CLAUDE.md`: Modul-Status C `⬜` → `🟡`; Abnahmestand
  3 ✅ · 4 🟡 · 13 ⬜ → **3 ✅ · 13 🟡 · 4 ⬜** (P8.5-5/-6/-7/-8/-10/-11/-13/-15/-16
  von `⬜` → `🟡` mit ausführlicher Belegnotiz je Zeile); Stand-Block nachgezogen.
- B1-Block nach `SESSIONS_ARCHIVE.md` rotiert (manuell — Skript
  `scripts/rotate_session_block.sh` jetzt vorhanden und gegen den Phase-Head
  getestet, aber der YAGNI-Stand aus A1/A2 gilt für die zweite Rotation nicht
  mehr, sobald Block D abgeschlossen ist).
- `phase8_5_picker_release/SESSIONS_ARCHIVE.md`: B1-Block vorne angehängt
  (newest-first), A2 darunter unverändert; `updated:` aktualisiert.
- `CLAUDE.md` (Wurzel): neuer „Current state"-Absatz vom 2026-09-04 für Block C.
- `docs/INDEX.md` Phase-8.5-Header: `🔄 A1 🟡, A2 🟡, B1 🟡, C/D/Z ⬜` → `🔄 A1 🟡,
  A2 🟡, B1 🟡, C 🟡, D/Z ⬜`.
- `ROADMAP.md` Phase-8.5-Absatz: „nächster Schritt: Block C" → „Block C committet;
  nächster Schritt: Block D (Release-Vorbereitung + Deploy als Nikinger-Aktion +
  Health-Gate + Sichtprüfung + Vierte A3-Probe)".

**Was diese Session bewusst NICHT tat:**

- Kein `webui/static/`-Touch — alle drei Befunde sind entweder Smoke-Bug
  (gefixt), Server-CSRF (Befund für Step Z), oder bewusst strukturell (Station 12).
- Kein `mcpserver/`, `storage/`, `authserver/`, `security.py`/`api.py`/`serializers.py`/
  `permissions.py`-Touch — Tabu-Diff §0.3 ist nachweislich leer.
- Kein Live-Deploy — Block D fällt nie unter Druck (Plan §8), D2 ist explizit eine
  Nikinger-Aktion (P8.5-Q + Hard Rule 9, niemals `sudo systemctl restart
  sharefyx-mcp` durch opencode/M3).
- Keine Cross-`kind`-Dedup für V102 — Plan §0.4 DRAUSSEN, nur messen, nicht fixen.
- Keine Anpassung der Reauth-UI (P7-24-Mechanismus) — die Smoke-Vereinfachung für
  Station 13 ist als Befund dokumentiert, nicht als Regression.
- Kein Runbook oder Live-Health-Gate — das ist Block D3/D5 mit Nikinger-Domain.

**Nächster Schritt, konkret:** **Block D — Release** (`docs/concepts/
phase8_5_picker_release_plan.md` §5). Reihenfolge:
- **D1 Vorbereitung opencode/M3:** `.rail__version` `v3.0` → `v3.0.1` (P8.5-P, eine
  Zeile in `phase5_ui/webui/static/app.html:20`); neuer `## 2026-09-04`-Block in
  `docs/UPDATE_LOG.md` mit drei menschenlesbaren Zeilen (Picker-Modi, Tastatur,
  Generalisierter Hint) — oberster Eintrag, sonst bricht `deploy.sh` (P6-X).
- **D2 Deploy als Nikinger-Aktion:** `SHAREFYX_SYSTEMCTL="sudo systemctl"
  phase5_ui/scripts/deploy.sh main` in interaktiver Vordergrund-Shell (Hard Rule 9,
  `sudo`-Prompt sichtbar — V103 prüfen).
- **D3 Health-Gate 3/3:** `/health` 200, `/api/v1/me` ohne Session 401, `/mcp/` ohne
  Token 401, `.rail__version` im Browser `v3.0.1`, Update-Banner zeigt den neuen
  Eintrag, `/opt/sharefyx/current` zeigt auf den neuen Release-Stempel, **V105**
  (echter Anthropic-Connector verbindet weiterhin).
- **D4 Sichtprüfung am echten Gerät:** Nikinger bestätigt P8-14/15/16/18/19/23 +
  P8.5-5/-6/-7/-8/-10/-11/-13/-15/-16 am echten Build; trägt Phase-8-Glyphe ✅/🟡 ein.
- **D5 Vierte A3-Probe:** wörtlicher Prüfauftrag aus Plan §3 B1, entscheidet über
  §9.4.1 (N2) Abbruchregel.
- **Z Closeout:** Phase-8.5-Plan §9 füllen, Nachtrag in
  `docs/concepts/phase8_ui_graph_plan.md` §9 + §9.4.7, Phase-8-Head §7-Matrix +
  Session-Block, Größenprüfung.

Aktueller `## Session stopped`-Block ist dieser Block-C-Block; der nächste rotiert ihn
nach `SESSIONS_ARCHIVE.md` (newest-first).

### 2026-09-04 (B1 — `_TITLE_NOT_ID_HINT` generalisierend geschärft, Code committet)

**Auftrag:** B1 nach `docs/concepts/phase8_5_picker_release_plan.md` §3 B1. Einzige
erlaubte Tabu-Ausnahme in `mcpserver/` (P8.5-D, Präzedenz P7-T und P8-§0.4). Hint
generalisierend schärfen (Option a, N2), zwei neue Asserts in `test_tools.py`,
Abbruchregel wörtlich im Phase-Head.

**Ergebnis — alle drei Eingriffsgruppen aus Plan §3 B1 committet, §0.5 Checkliste grün:**

1. **`phase2_mcp/mcpserver/tools.py` Z. 159–164.** `_TITLE_NOT_ID_HINT` generalisiert.
   Der alte Schwanz `; auch nicht als Tabellen-Spalte.` ist durch einen Vier-Zeilen-
   Schlusssatz ersetzt: *„Das gilt in jeder Textform — auch nicht als Tabellen-Spalte,
   nicht in Klammern hinter dem Titel und nicht in Aufzählungs-Zeilen."* — wörtlich aus
   Plan §3 B1. Die drei Negativ-Beispiele stehen jetzt als **Illustration der Regel**,
   nicht als abschließende Liste; der Satz „Das gilt in jeder Textform" ist die
   eigentliche Änderung, der Rest ist Konkretisierung. Wörtlich identisch an den vier
   Verwendungsstellen (`search_items`/`get_item`/`get_item_meta`/`create_item`) — die
   `update_item`/`append_to_item`/`patch_item`-Beschreibungen tragen den Hint bewusst
   nicht (reine Schreibwerkzeuge, Vorlage aus Phase 7; siehe auch „Fehlerpfad" unten).

2. **`phase2_mcp/tests/test_tools.py` Z. 137–143.** `test_tool_descriptions_tell_the_
   agent_to_name_titles_not_ids` um zwei Asserts erweitert:
   - `assert "in jeder Textform" in tools._TITLE_NOT_ID_HINT`
   - `assert "Klammern" in tools._TITLE_NOT_ID_HINT`
   Bestehende Asserts (`"Einkaufsliste Winter"`, `"itm_a1b2c3d4"`, `"Tabellen-Spalte"`,
   plus Hint-in-Beschreibung für `search_items`/`get_item`/`get_item_meta`/
   `create_item`) bleiben unverändert gültig — keine Anpassung am Testaufbau, nur zwei
   zusätzliche Zeilen.

3. **`phase8_5_picker_release/CLAUDE.md`.** Neuer Abschnitt `## Abbruchregel §9.4.1
   (N2, verbindlich)` zwischen Modul-Status und Geerbte Contracts, wörtlich aus Plan
   §3 B1: *„Taucht die `itm_…`-ID in einer **vierten** Oberflächenform auf (Fließtext +
   Tabelle waren die ersten zwei, der Klammer-/Aufzählungs-Kontext aus Phase 8 §9.4.1
   die dritte), wird §9.4.1 als **Modellverhalten dokumentiert und geschlossen**
   (Option c). Kein fünfter Hint-Edit, keine Schema-Änderung an `search_items`. Der
   Punkt verschwindet dann aus dem Ledger, statt weiter vererbt zu werden. — Geprüft
   wird das in Block D5 (vierte A3-Probe nach dem Deploy, wörtlicher Prüfauftrag im
   Plan §3 B1)."* — Pflichtbestandteil der Abnahmezeile P8.5-3.

**Begleitende Doku-Updates im selben Commit (Hard Rule 8):**

- `phase8_5_picker_release/CLAUDE.md`: Modul-Status B1 `⬜` → `🟡`; P8.5-3 `⬜` → `🟡`
  mit Klammer-Anmerkung für den Code-Beleg; Stand-Zeile 3 ✅ · 3 🟡 · 14 ⬜ →
  3 ✅ · 4 🟡 · 13 ⬜.
- A2-Block nach `SESSIONS_ARCHIVE.md` rotiert (manuell, wie in A1/A2 — Skript
  `scripts/rotate_session_block.sh` aus Phase 7 noch nicht für `phase8_5_picker_release/`
  portiert; YAGNI bis Block-C-Beginn).
- `phase8_5_picker_release/SESSIONS_ARCHIVE.md`: A2-Block vorne angehängt
  (newest-first), A1 darunter unverändert; `updated:` aktualisiert.
- `CLAUDE.md` (Wurzel): neuer „Current state"-Absatz vom 2026-09-04 für B1.
- `docs/INDEX.md` Phase-8.5-Header: `🔄 A1 🟡, A2 🟡, B1/C/D/Z ⬜` → `🔄 A1 🟡, A2
  🟡, B1 🟡, C/D/Z ⬜`.
- `ROADMAP.md` Phase-8.5-Absatz: „nächster Schritt: B1" → „B1 committet; nächster
  Schritt: Block C (Wegwerf-Setup + 13-Stationen-Playwright-Smoke)".

**Verifiziert (§0.5 Checkliste):**

- `pytest -q` (venv): **962 passed in 256.65 s** — 962 unverändert (keine neue
  Testfunktion, nur zwei Asserts im bestehenden
  `test_tool_descriptions_tell_the_agent_to_name_titles_not_ids`); keine Regressionen.
- Tabu-Diff aus §0.3 zeigt **genau** die erlaubten zwei Dateien:
  `git diff --stat main -- phase4_auth/ phase1_storage/storage/ phase5_ui/webui/security.py
  phase5_ui/webui/api.py phase5_ui/webui/serializers.py phase5_ui/webui/permissions.py
  phase2_mcp/` →
  ```
  phase2_mcp/mcpserver/tools.py  | 5 +++--
  phase2_mcp/tests/test_tools.py | 2 ++
  ```
  Plan §3 B1 „Tabu: … Der Diff auf `phase2_mcp/` darf **genau** diese eine Datei plus
  die Testdatei zeigen." — exakt erfüllt.
- `node --check`: keine JS-Datei berührt (irrelevant für diese Session).
- Größenprüfung `find . -name "*.md" -not -path "./.venv/*" -size +40k`: **kein**
  neuer Treffer durch diese Session; `phase8_5_picker_release/CLAUDE.md` jetzt ~27 KB
  (vorher ~27 KB), weiterhin deutlich unter dem Cap — kein Rotationsschritt nötig.
- Fehlerpfad einmal durchgedacht: bestehender Test prüft den Hint an den vier
  Verwendungsstellen, an denen er tatsächlich eingebettet ist. Die Generalisierung
  ist **additiv** (kein bestehender Fall wird gebrochen, nur neue Fälle werden
  abgedeckt) — wer vorher schon „Tabellen-Spalte" las, sieht jetzt zusätzlich
  „Klammern" und „Aufzählungs-Zeilen". Wenn der Generalisierungs-Satz später einmal
  entfernt werden müsste (Pflege, niemand weiß), würde der bestehende Assert
  `"Tabellen-Spalte" in tools._TITLE_NOT_ID_HINT` zuerst feuern — das ist das
  gewollte Sicherheitsnetz. Ein viertes `_TITLE_NOT_ID_HINT`-Vorkommen (etwa in einem
  fünften Tool) fällt durch den `assert tools._TITLE_NOT_ID_HINT in
  _description_of(described_mcp, name)`-Loop nicht auf — der Test ist absichtlich
  nicht „viermal vorkommend", sondern „in diesen vier Beschreibungen vorhanden".
- Service-Touch **0**. `systemctl status sharefyx-mcp` zeigt **PID 195922**, Active seit
  `Wed 2026-09-02 11:51:57 CEST` (3 days zum Sitzungsbeginn) — nichts angefasst, nur
  gelesen. **PID + ActiveEnterTimestamp im Session-Block notiert, wie §0.5.7 verlangt.**

**Was diese Session bewusst NICHT tat:**

- Browser-/Live-Verifikation für P8.5-4 (vierte A3-Probe) — kommt mit Block D5 nach
  dem Deploy.
- `test_mcp_smoke.py`-Anpassung an den neuen Hint-Text — der Smoke ist eine Live-
  Probe, die keinen Description-Text liest (nur Tool-Aufrufe gegen den Server); keine
  Anpassung nötig, keine Lücke im Smoke.
- Block C (Wegwerf-Setup + 13-Stationen-Playwright-Smoke) — nächster Schritt nach
  diesem Commit; Plan §4.
- `mcpserver/tools.py` sonst anfassen — die Tabu-Ausnahme gilt **ausschließlich** für
  den Hint-Text. `WRITE_TOOL_DIVISION`, `_LIST_SPACES_POINTER`, alle
  Beschreibungs-Strings anderer Tools bleiben unangetastet (gegengeprüft mit
  `git diff` auf der Datei).
- `mcp_smoke.py`-Beschreibungen — der Hint erscheint nur in Tool-Beschreibungen, der
  Smoke spricht die Tools über Funktionsaufrufe an.

**Nächster Schritt, konkret:** **Block C — v3-Vorabritt gegen eine Wegwerf-Instanz**
(`docs/concepts/phase8_5_picker_release_plan.md` §4). Erst Wegwerf-Setup
(`scripts/serve.py` mit tmp `DATA_ROOT`/tmp `auth.sqlite3`/eigenem Port, inkl. der seit
Step 0 angekündigten Portierung von `scripts/rotate_session_block.sh` aus Phase 7 für
`phase8_5_picker_release/`), dann 13 Stationen Playwright-Smoke; jeder Fund entweder
behoben oder als benannter Befund vorgelegt. Plan §4 listet die 13 Stationen.

---

### 2026-09-04 (A2 — Tastaturnavigation + `_pickLinkPickerAt` + CSS-Block-Entdopplung, Code committet)

**Auftrag:** A2 nach `docs/concepts/phase8_5_picker_release_plan.md` §2.A2.
Tastaturnavigation über `aria-activedescendant` (Fokus bleibt im Suchfeld), gemeinsamer
Pick-Pfad für Maus und Enter, Entdopplung der zwei identischen CSS-Auswahl-Blöcke am
Picker, totes `:focus` raus. Die A1-Session hatte statische Tests ausdrücklich
zurückgestellt — der Plan-Test für P8.5-14 gehört zu A2, P8.5-9 und P8.5-12 ziehe ich
gleich mit nach.

**Ergebnis — alle drei Eingriffsgruppen aus Plan §2.A2 committet, §0.5 Checkliste grün:**

1. **`phase5_ui/webui/static/js/dialogs.js`** — vier Edits:

   - Neue Modul-Variablen `linkPickerItems = []` und `linkPickerCursor = -1` (Z. 117–119).
     `-1` = keine Auswahl, beim Re-Rendern zurückgesetzt (benannte Falle aus Plan §2.A2:
     sonst zeigte ein alter Cursor nach dem Filtern auf einen anderen Treffer).

   - `_renderLinkPickerResults(items)` umgebaut: State-Reset **ganz oben** (vor
     `replaceChildren()`) räumt `linkPickerItems`+`linkPickerCursor`+
     `aria-activedescendant` — das schließt den Such-Debounce-Fall ab, in dem der User
     tippt, bevor die Antwort zurück ist. Jede Treffer-`li` bekommt `id="link-picker-
     opt-{i}"`, wird in `linkPickerItems` aufgenommen und hat als Click-Listener
     `_pickLinkPickerAt(i)`. Der "Keine Treffer."-Eintrag bleibt `aria-disabled="true"`
     und wird **nicht** in `linkPickerItems` aufgenommen — für `_pickLinkPickerAt` damit
     unerreichbar (Abnahmezeile P8.5-11).

   - Zwei neue Helper: `_setLinkPickerCursor(index)` setzt/löscht `aria-selected` auf
     genau einer `li` und `aria-activedescendant` auf dem Suchfeld
     (ARIA-1.2-Pflicht-Beziehung, genau dafür steht `aria-controls` am Input aus A1);
     `scrollIntoView({block: "nearest"})` hält den Cursor im sichtbaren Bereich bei
     langen Trefferlisten. `_pickLinkPickerAt(index)` ist der gemeinsame Pick-Pfad für
     Maus-Klick und Enter-Taste, Modus wird **vor** `closeLinkPicker()` gelesen wie
     beim bestehenden Klick-Handler (Select wird mit dem Dialog versteckt;
     UI-mutations-unabhängig).

   - `closeLinkPicker()` ergänzt um `linkPickerItems = []; _setLinkPickerCursor(-1);` in
     der richtigen Reihenfolge (erst leeren, dann Cursor räumen). Alt-Aufrufer bleiben
     kompatibel.

   - `init()`: ein neuer `keydown`-Handler am `linkPickerSearchEl` für `ArrowDown`/
     `ArrowUp`/`Enter`. Bewusst kein Wrap-around (die Listen-Navigation in `app.js:212`
     klemmt ebenfalls), kein Home/End, kein Enter-wählt-den-einzigen-Treffer (Raten).
     `Escape` bleibt beim globalen Handler (P8.5-L, dort nicht angefasst).

2. **`phase5_ui/webui/static/app.css`** (Z. 1280–1298) — die zwei identischen
   Regelblöcke (`li:hover`+`li:focus` und `li[aria-selected="true"]`) zu einem
   zusammengezogen, das tote `:focus` entfällt (kein `tabindex` auf den `li`, kann nie
   feuern). Die vier Deklarationen selbst sind **byte-identisch** zum 2026-09-02-
   Standard (Nikinger-Freigabe damals), hier nur entdoppelt. Kommentar darüber um eine
   Phase-8.5-A2-Zeile ergänzt, alte Erklärung zum `var(--accent-text)`-Fund bleibt
   unverändert stehen.

3. **`phase5_ui/tests/test_static_routes.py`** — drei neue Tests:

   - `test_link_picker_css_has_one_selection_block` (P8.5-14): zählt `li[aria-
     selected="true"]` in `app.css` (genau 1) und prüft Abwesenheit von
     `.link-picker-results li:focus`.
   - `test_link_picker_picks_run_through_a_single_helper` (P8.5-12): `_pickLinkPickerAt`
     in `dialogs.js` genau einmal definiert, ≥3 Vorkommen (1 Definition + Maus-Klick +
     Enter-Taste); `app.js` enthält weder `openLinkPicker` (P8.5-L: Picker wird nur in
     `editor.js` geöffnet) noch `_pickLinkPickerAt` (Helper nicht umgehen).
   - `test_insertAtCursor_defined_exactly_once_at_module_level` (P8.5-9): die A1-
     Anforderung war bislang nur über `grep -n` belegt; jetzt mit pytest festgehalten.
     Der Bild-Knopf-Aufruf (jetzt Z. 669) außerhalb von `init()` beweist die
     Modul-Ebene implizit — function-Deklaration wird vom JS-Hoisting an alle
     Modul-Stellen sichtbar gemacht.

**Begleitende Doku-Updates im selben Commit (Hard Rule 8):**

- `phase8_5_picker_release/CLAUDE.md`: Modul-Status A2 `⬜` → `🟡`; fünf Abnahmezeilen
  P8.5-9/-10/-11/-12/-14 angepasst (P8.5-9/-12/-14 `⬜` → `🟡` mit Klammer-Anmerkung
  für den statischen Test; P8.5-10/-11 bleiben `🟡` für die Code-Spur, Browser-Nachweis
  Block C Station 7); Stand-Zeile 3 ✅ · 0 🟡 · 17 ⬜ → 3 ✅ · 3 🟡 · 14 ⬜.
- A1-Block nach `SESSIONS_ARCHIVE.md` rotiert (manuell, weil `scripts/
  rotate_session_block.sh` aus Phase 7 für `phase8_5_picker_release/` noch nicht
  portiert ist — YAGNI für eine zweite manuelle Rotation; Skript-Eintrag verschoben
  auf Block-C-Beginn mit dem Wegwerf-Setup).
- `phase8_5_picker_release/SESSIONS_ARCHIVE.md`: A1-Block vorne angehängt (newest-first),
  Step 0 darunter unverändert; `updated:` aktualisiert.
- `CLAUDE.md` (Wurzel): neuer „Current state"-Absatz vom 2026-09-04 für A2.
- `docs/INDEX.md` Phase-8.5-Header: `🔄 A1 🟡, A2/B1/C/D/Z ⬜` → `🔄 A1 🟡, A2 🟡,
  B1/C/D/Z ⬜`.
- `ROADMAP.md` Phase-8.5-Absatz: „nächster Schritt: A2" → „nächster Schritt: B1
  (Titel-statt-ID-Hint generalisierend schärfen, eine Datei in `mcpserver/`)".

**Verifiziert (§0.5 Checkliste):**

- `pytest -q` (venv): **962 passed in 266.27 s** — 959 unverändert + 3 neue Tests in
  `test_static_routes.py`; keine Regressionen.
- Tabu-Diff aus §0.3 leer: `git diff --stat main -- phase4_auth/ phase1_storage/storage/
  phase5_ui/webui/security.py phase5_ui/webui/api.py phase5_ui/webui/serializers.py
  phase5_ui/webui/permissions.py phase2_mcp/` — **keine Ausgabe**.
- `node --check` auf `dialogs.js` — **OK** (einzige berührte JS-Datei; `app.js` tabu
  P8.5-L, `editor.js` unangetastet).
- `python phase5_ui/scripts/ui_budget.py`: **5/5 grün**, js+css+gzip jetzt
  **128.7 KB** von 127.6 KB (+1.1 KB durch `dialogs.js` 11.7 → 12.6 KB und die drei
  statischen Tests); Latenz-`get_item` 7.6 ms / 0.5 KB, `search_items` 189.4 ms / 20 KB,
  `GET /api/v1/overview` 881.3 ms / 1.9 KB — alle im Korridor.
- Größenprüfung `find . -name "*.md" … -size +40k`: **kein** neuer Treffer durch diese
  Session; `phase8_5_picker_release/CLAUDE.md` jetzt ~31 KB (vorher ~24 KB), weiterhin
  deutlich unter dem Cap — kein Rotationsschritt nötig, der Head trägt nach dem
  Rotieren weiterhin genau einen Block (jetzt den A2-Block).
- Fehlerpfad einmal durchgedacht: leere Trefferliste → `_renderLinkPickerResults` setzt
  `linkPickerItems = []` und zeigt den `aria-disabled="true"`-Eintrag (nicht in
  `linkPickerItems`, für `_pickLinkPickerAt` unerreichbar); `_setLinkPickerCursor`
  sieht out-of-range und räumt `aria-activedescendant` (verhindert verwaiste ID-Referenz
  im Suchfeld). Cursor-Reset beim Re-Render fängt auch den Fall ab, dass der User tippt,
  bevor die Suche antwortet (150 ms Debounce — die Items im DOM sind noch die alten,
  gehören aber gleich zum alten `linkPickerItems`-Stand; nach der Antwort sind beide
  synchron neu). `closeLinkPicker` setzt State und Cursor in der richtigen Reihenfolge,
  sodass `_setLinkPickerCursor(-1)` keine Alt-Werte mehr sieht. `_pickLinkPickerAt`
  mit ungültigem Index ist no-op. `app.js` bleibt tabu und ist im Test festgenagelt
  (`openLinkPicker` darf dort nicht vorkommen — der Picker wird in `editor.js` geöffnet,
  der Helper nur in `dialogs.js` ausgeführt).
- Service-Touch **0**. `systemctl status sharefyx-mcp` zeigt **PID 195922**, Active seit
  `Wed 2026-09-02 11:51:57 CEST` (2 days zum Sitzungsbeginn) — nichts angefasst, nur
  gelesen. **PID + ActiveEnterTimestamp im Session-Block notiert, wie §0.5.7 verlangt.**

**Was diese Session bewusst NICHT tat:**

- Browser-Verifikation für P8.5-10/-11 (P8.5-13 in Chromium und Firefox) — Block C,
  kommt mit dem v3-Vorabritt gegen eine Wegwerf-Instanz.
- Statischer Test für P8.5-5 (Picker-Dialog trägt `<select>` mit beiden Werten) —
  nicht in den A2-Plan-Scope; wäre ein eigener Tag-Test (Markup-Snapshot), günstig
  vor Block C nachzuziehen.
- `dialogs.js` Helper `_setLinkPickerCursor` und `_pickLinkPickerAt` weiter
  modularisieren (z. B. in ein eigenes Modul) — P5-T bleibt in `dialogs.js` (eine Datei
  pro Dialog-Cluster, siehe Modul-Header), YAGNI.
- `app.js` berühren (P8.5-L explizit, im Test festgenagelt).
- B1 (`_TITLE_NOT_ID_HINT` generalisierend schärfen in `mcpserver/tools.py:159-164`) —
  eigener Schritt nach A2, einzige erlaubte Tabu-Ausnahme in `mcpserver/`.

**Nächster Schritt, konkret:** **B1 — §9.4.1 Hint generalisierend schärfen**
(`mcpserver/tools.py:159-164`, einzige erlaubte Tabu-Ausnahme; `phase2_mcp/tests/
test_tools.py` mitziehen, zwei neue Asserts; Abbruchregel wörtlich im Phase-Head,
Abnahmezeile P8.5-3). Block C (Wegwerf-Setup + 13-Stationen-Playwright-Smoke) folgt
danach.

### 2026-09-04 (A1 — Picker-Modus-Umschalter + Body-Markdown-Link, Code committet)

**Auftrag:** A1 nach `docs/concepts/phase8_5_picker_release_plan.md` §2.A1. User-Auftrag
vom 2026-09-03 nannte die genauen Eingriffe (HTML, `dialogs.js:100-185`, `editor.js:88-100`,
`localStorage` unter `sfx:linkpicker:mode`); statische Tests + Block-C-Browser-Nachweis
wurden ausdrücklich zurückgestellt — Tabu-Diff bleibt leer, nur `webui/static/`.

**Ergebnis — alle vier Eingriffsgruppen aus Plan §2.A1 committet, §0.5 Checkliste grün:**

1. **`phase5_ui/webui/static/app.html`** (Zeilen 270–280). Hint-Text von „hängt die
   itm_…-ID an die Links" auf „Was der Klick einfügt, hängt vom Modus darunter ab"
   neutralisiert; neues `<label>Einfügen <select class="input" id="link-picker-mode">
   …</select></label>` **zwischen** Hint und Suchfeld eingefügt — barer `<label>` ohne
   `class="field"`, exakt nach dem Vorbild `#move-space-select` (`app.html:286-287`),
   um den 2026-09-02-Chevron-Eskalationsfall nicht zu reproduzieren
   (`.field .input { font-size: 13px }`); beide `<option>` mit Werten `body` (Default)
   und `frontmatter`. Suchfeld-Input um `role="combobox" aria-expanded="true"
   aria-controls="link-picker-results"` erweitert (A2-Vorbereitung — ohne
   `aria-controls` ist `aria-activedescendant` formal ungültig). Pflichtprüfung am
   Step-Ende aus Plan §2.A1 Punkt (1) — computed `font-size` und Chevron-Größe gegen
   `#move-space-select` — wird erst in Block C empirisch verglichen (kein jsdom-Harness
   im Projekt, verifiziert Plan §0.0); bei Abweichung Eskalation nach §0.0, kein
   symptomatisches Nachjustieren.

2. **`phase5_ui/webui/static/js/dialogs.js`**. Modul-Konstante
   `LINK_PICKER_MODE_KEY = "sfx:linkpicker:mode"` ergänzt (Präfix `sfx:` aus
   `editor.js :: draftKeyFor()`); `linkPickerModeEl` neu; `linkPickerButtonEl` ersatzlos
   entfernt — war in `dialogs.js` ungenutzt (`editor.js:47` hält die eigene). Zwei neue
   Helper: `_linkPickerMode()` (liefert `"body"`/`"frontmatter"`, fällt auf `body`
   zurück bei unerwartetem Wert) und `_restoreLinkPickerMode()` (liest `localStorage`
   in `try`/`catch` — privater Modus wirft `SecurityError`). `openLinkPicker` ruft
   `_restoreLinkPickerMode()` vor `linkPickerSearchEl.focus()`, Guard-Text auf
   `"openLinkPicker braucht { onPick({id, title, mode}) }"` aktualisiert; Klick-Listener
   in `_renderLinkPickerResults` liest den Modus **vor** `closeLinkPicker()` (Select wird
   mit Dialog versteckt; Reihenfolge hält die Lesung unabhängig von UI-Mutationen) und
   ruft `onPick({id, title, mode})`. Im `init()`-Block: `linkPickerModeEl` zugewiesen
   plus `change`-Handler, der die Wahl **beim Wechsel** in `try`/`catch` schreibt — so
   überlebt sie auch einen Abbruch via Escape.

3. **`phase5_ui/webui/static/js/editor.js`**. **`insertAtCursor` (bisher Zeile 548–557,
   innerhalb `init()`) auf Modulebene gehoben** (P8.5-I) — direkt hinter `_appendLinkId`
   (jetzt Zeile 107), Körper byte-identisch, schließt über nichts aus `init()`
   (`textarea` ist Parameter), Alt-Aufruf Bild-Knopf (jetzt Zeile 669) sieht die
   Modulebene via Hoisting. Bestätigt: `grep -n 'function insertAtCursor' editor.js`
   liefert **genau einen** Treffer. Drei neue Funktionen: `_linkTextFor(title)`
   (kollabiert Whitespace, maskiert `[`/`]` mit Backslash, leerer String signalisiert
   „kein Titel"), `_appendLinkMarkdown(title, id)` (ruft `insertAtCursor` mit
   `"[" + label + "](#item/" + id + ")"`, gleiche `itm_[0-9a-f]{8}`-Defense-in-Depth
   wie `_appendLinkId`), `_onLinkPicked(picked)` (Router: `mode === "frontmatter"` →
   `_appendLinkId`, sonst → `_appendLinkMarkdown`). Wiring (jetzt Zeile 530):
   `openLinkPicker({ onPick: _appendLinkId })` →
   `openLinkPicker({ onPick: _onLinkPicked })`.

4. **`localStorage` unter `sfx:linkpicker:mode`** (P8.5-G). **Erste `localStorage`-
   Nutzung im Projekt** — bisher nur `sessionStorage` (CSRF, Drafts). Begründung: die
   Moduswahl muss Tab-/Fenster-Schließen überleben, das ist mit `sessionStorage` nicht
   möglich. `try`/`catch` deckt den SecurityError im privaten Modus ab. **V99-Korrektur
   im Session-Block festgehalten** (kein stiller Drift): der Plan hatte „ja,
   `sfx:draft:`" als Erwartung — das traf für den **Präfix** zu, aber nicht für den
   Storage; die Substantiv-Korrektur (`local`- statt `session`Storage) ist die einzige
   Abweichung vom Plan-Wortlaut und folgt direkt aus P8.5-G.

**Begleitende Doku-Updates im selben Commit (Hard Rule 8):**

- `phase8_5_picker_release/CLAUDE.md`: Modul-Status A1 `⬜` → `🟡` (Tests noch `⬜`);
  fünf Abnahmezeilen P8.5-5/-6/-7/-8/-9 mit kurzen Klammer-Anmerkungen versehen („Code
  committet; Browser-Nachweis Block C Station …"); Stand-Zeile unverändert
  (3 ✅ · 0 🟡 · 17 ⬜, P8.5-1/-2/-20 aus Step 0).
- Step-0-Block nach `SESSIONS_ARCHIVE.md` rotiert (manuell, weil das Skript nur 2+→1
  kann und das Archiv initial keinen `## Session stopped`-Anker hatte — Platzhalter
  entfernt, Frontmatter-`updated:` aktualisiert).
- `phase8_5_picker_release/SESSIONS_ARCHIVE.md`: Platzhalter-Hinweis „noch leer"
  entfernt (jetzt nicht mehr zutreffend), `updated:` auf 2026-09-04.

**Verifiziert (§0.5 Checkliste):**

- `pytest -q` (venv): **959 passed in 258.19 s** — unverändert, kein Python-Touch
  (Phase 8.5 baut **keine** API-Fläche, Plan §0.3).
- Tabu-Diff aus §0.3 leer: `git diff --stat main -- phase4_auth/ phase1_storage/storage/
  phase5_ui/webui/security.py phase5_ui/webui/api.py phase5_ui/webui/serializers.py
  phase5_ui/webui/permissions.py phase2_mcp/` — **keine Ausgabe**.
- `node --check` auf `dialogs.js` + `editor.js` + `app.js` (Sicherheitsgespann) — alle
  drei **OK**.
- `python phase5_ui/scripts/ui_budget.py`: **5/5 grün**, js+css+gzip jetzt
  **127.6 KB** von 125.8 KB (+1.8 KB durch `dialogs.js` 11.0 → 11.7 KB und
  `editor.js` 7.9 → 8.8 KB); Latenz-`get_item` 7.8 ms / 0.5 KB, `search_items`
  185.6 ms / 20 KB, `GET /api/v1/overview` 867.9 ms / 1.9 KB — alle im Korridor.
- Größenprüfung `find . -name "*.md" … -size +40k`: **kein** neuer Treffer durch diese
  Session; `phase8_5_picker_release/CLAUDE.md` bleibt deutlich unter dem Cap.
- Fehlerpfad einmal durchdacht: leeres Suchergebnis → `_renderLinkPickerResults`
  rendert den `aria-disabled="true"`-Eintrag wie bisher (kein Code-Link auf
  `linkPickerItems`, A2 fügt das später hinzu); `localStorage`-Wurf → `saved = null`
  → `body`-Default; `closeLinkPicker()` läuft vor `onPick`-Aufruf, Modus-Lesung VOR
  `closeLinkPicker` ist dadurch UI-mutations-unabhängig; `picked` ist `null`/kein
  String → `_onLinkPicked` macht nichts; `_linkTextFor` kollabiert Whitespace und
  maskiert `[`/`]` (Titel „Notiz [Entwurf]" zerreißt den Markdown-Link nicht).
- Service-Touch **0**. `systemctl status sharefyx-mcp` zeigt **PID 195922**, Active seit
  `Wed 2026-09-02 11:51:57 CEST` (1 day 23h zum Sitzungsbeginn — uptime wuchs leicht
  gegenüber dem Step-0-Stand) — nichts angefasst, nur gelesen. **PID +
  ActiveEnterTimestamp im Session-Block notiert, wie §0.5.7 verlangt.**

**Zwei Drift-Funde im Verlauf der Sitzung, im Block festgehalten, kein stiller Patch:**

1. **`\u00b7` vs. `·` in `dialogs.js`:** die Datei speichert das Middle-Dot als JS-
   Escape (`\u00b7`), nicht als Literal-Zeichen. Mein erster `edit` traf den
   `oldString` mit literalem `·` nicht; zweiter Versuch mit dem Escape klappte.
   **Lehre für künftige Picker-Edits:** in dieser Datei konsequent die Escape-Form
   verwenden oder das ganze Vorkommen vor dem Edit auf `xxd`/Pipe-Substitution
   umstellen — kein Code-Fix nötig, ist ein Editor-/Tooling-Detail.
2. **`sessionStorage` vs. `localStorage`:** V99 im Plan war ungenau — der Plan tippte
   auf „ja, `sfx:draft:`" als Präfix-Begründung, verschwieg aber, dass
   `draftKeyFor` selbst `sessionStorage` nutzt. Die Wahl von `localStorage` ist
   deshalb eine **Eskalation** gegenüber der Projekt-Konvention, keine triviale
   Fortführung; gerechtfertigt durch P8.5-Gs Anforderung „überlebt Tab-Schließen".
   Im Code dokumentiert (`dialogs.js:107`/`185-191`).

**Was diese Session bewusst NICHT tat:**

- Statische Tests in `phase5_ui/tests/test_static_routes.py` (P8.5-5/-9) — User-Auftrag
  beschränkte die Session auf `webui/static/`; Tests werden mit Block-C-Vorbereitung
  oder vor A2 nachgezogen.
- Block C (Wegwerf-Setup + 13-Stationen-Playwright-Smoke) — kommt als eigener Schritt.
- A2 (`aria-activedescendant`, Tastaturnavigation, `_pickLinkPickerAt`,
  CSS-Block-Entdopplung) — eigene Aktion, Reihenfolge A1 → A2 nach §8.
- B1 (Hint generalisierend) — nach A2, eigene Datei (`mcpserver/tools.py:159-164`).

**Nächster Schritt, konkret:** **A2 — §9.4.3 Tastaturnavigation und `aria-selected`**
(`dialogs.js` `linkPickerItems`/`linkPickerCursor` + `_setLinkPickerCursor` +
`_pickLinkPickerAt` + keydown-Handler am Suchfeld; `app.css` zwei identische Blöcke zu
einem zusammenziehen, totes `:focus` raus; `app.js` **nicht** anfassen, P8.5-L). Block C
kommt **nach** A2 — beide landen in `_renderLinkPickerResults` und im Auswahlpfad,
ein Skript-Paar deckt beide ab (Plan §8).

### 2026-09-03 (Step 0 — Skelett + vier Haushalt-Funde abgearbeitet)

**Auftrag:** Step 0 nach `docs/concepts/phase8_5_picker_release_plan.md` §1. Verifikations-
Durchlauf war bereits 2026-09-03 vom Nikinger (Planungssession) gefahren — vier Funde
benannt, davon drei Doku-only, einer ein Bilanz-Zähler-Drift. opencode/M3 wiederholt die
Messung nicht, sondern arbeitet die Funde ab und legt das Skelett an.

**Ergebnis — alle vier Funde aus Plan §1 abgearbeitet, alle fünf Schritte grün:**

1. **Fund 1 — `docs/INDEX.md` über 40 KB-Softcap** (Plan §1.2). Zeile 8 war eine
   15.472-Zeichen-Pipe-Kette aus ~40 datierten Einträgen, verantwortlich für den Löwenanteil
   der Datei (52.911 B bei Übernahme). **Kürzung auf 5 neueste Einträge + Schlusszeile**
   „ältere Einträge: die jeweilige phase*/SESSIONS_ARCHIVE.md". Die vollständige Historie
   steht in den jeweiligen `phase*/SESSIONS_ARCHIVE.md`. Größenverlauf: **52.911 B → 40.917 B**
   (−11.994 B, −23 %; aktueller Stand nach Step 0.2: **40.917 B, 43 B unter dem 40-KB-Softcap
   = 40 × 1024 B**).
2. **Fund 2 — vier `.md` ohne Card/Indexzeile, korrekt so** (Plan §1.3). Regel-Präzisierung
   im Wartungsblock von `docs/INDEX.md` (Zeilen 21–23): Harness-Dateien
   (`.claude/RESUME.md`), Test-Fixtures (`phase6_shares/tests/golden/*.md` — Card bräche den
   Byte-Vergleich), maschinell geparste Dateien (`docs/UPDATE_LOG.md`), Vendor-/Lizenztext
   (`phase5_ui/THIRD_PARTY_LICENSES.md`, `phase5_ui/vendor/lucide/README.md`). Bewusst als
   kompakter Dreizeiler formuliert (Plan §1.3 liefert nur die vier Kategorien; ausführliche
   Begründung pro Datei bleibt im Plan §1.3-Tabelle).
3. **Fund 3 — Doku/Code-Drift „Büroklammer" vs. „Lupe"** (Plan §1.4).
   `phase8_ui_graph/CLAUDE.md:440` nannte das Picker-Symbol „Büroklammer", `app.html:183`
   rendert `<use href="#i-search">` (Lucide-Suche, eingeführt in Phase 8 Block C2). Der
   `UPDATE_LOG.md`-Eintrag vom 2026-09-01 sagte bereits korrekt „Lupe". **Korrektur mit
   datierter Notiz** am 2026-09-03 im selben Block, damit der nächste Leser sieht, dass es
   kein Tippfehler war, sondern eine echte Korrektur.
4. **Fund 4 — Phase-8-Abnahmebilanz zum dritten Mal gedriftet** (Plan §1.5). Die Zeile trug
   seit dem 2026-09-02-Block „15 ✅ · 10 🟡 · 0 ⬜", die Aufzählung darunter listete unter
   „15 ✅" genau **vierzehn** Zeilennummern. Maschinell nachgezählt über die §7-Matrix
   selbst:
   ```
   awk '/^\| P8-[0-9]+ /{ if (/\| ✅ \|/) g++; else if (/\| 🟡 \|/) y++; else if (/\| ⬜ \|/) o++; n++ } \
     END {printf "Zeilen=%d ✅=%d 🟡=%d ⬜=%d\n", n, g, y, o}' phase8_ui_graph/CLAUDE.md
   ```
   Lauf 2026-09-03: **`Zeilen=26 ✅=14 🟡=12 ⬜=0`**. Bilanz-Zeile auf **14 ✅ · 12 🟡 · 0 ⬜**
   korrigiert; das awk-Kommando in den Bilanz-Abschnitt geschrieben, sodass künftige
   Schreibvorgänge die Zahl ableiten statt pflegen. Aufzählung gegen das Ergebnis abgeglichen
   (passt: 14/12-Zerlegung stimmt mit den aufgezählten IDs überein).

**Skelett angelegt (Step 0.5):**

- `phase8_5_picker_release/CLAUDE.md` — L1-Card, Mission, Scope (DRIN/DRAUSSEN), Harte Regeln
  (§0.3 Tabu-Liste verbatim übernommen + explizit `webui/{api,serializers,permissions}.py` als
  Tabu ergänzt), Modul-Status-Tabelle (Step 0 / A1 / A2 / B1 / C / D / Z mit aktuellem
  Status), Abnahmestand-Tabelle nach §7-Muster (P8.5-1–P8.5-20, P8.5-1/-2/-20 aus Step 0
  bereits ✅), Geerbte Contracts, leerer Session-Block. **12.128 B** — deutlich unter dem
  40-KB-Softcap.
- `phase8_5_picker_release/SESSIONS_ARCHIVE.md` — L1-Card, leerer Body mit Hinweis, dass der
  erste rotierte Block hierher wandert, sobald die zweite Session den Step-0-Block ablöst.
  **555 B**.
- `phase8_5_picker_release/scripts/` — leeres Verzeichnis, wird in Block C gefüllt
  (Wegwerf-Setup + Playwright-Ritt).

**Begleitende Doku-Updates im selben Commit (Hard Rule 8):**

- `ROADMAP.md` — neuer Abschnitt „Phase 8.5 — Link-Picker-Politur und v3-Release" eingefügt
  **vor** „Bewusst nicht auf der Roadmap" (Plan §1.6 Zeile 352). Status: „Step 0
  abgeschlossen", nächster Schritt „A1".
- `CLAUDE.md` (Wurzel) — `down:`-Zeile zeigt jetzt auf `phase8_5_picker_release/CLAUDE.md`
  (vorher `phase8_ui_graph/CLAUDE.md` — Umstellung nach Skelett-Anlage, wie der 2026-09-03-
  Absatz in „Current state" angekündigt hatte). Neuer Absatz unter Phase 8.5 mit Step-0-
  Zusammenfassung; `updated:`-Kette um den Step-0-Eintrag am Anfang verlängert. **41.462 B** —
  damit 502 B **über** dem 40-KB-Softcap. Das war bereits vor Step 0 absehbar (Kandidat für
  dieselbe Kompression wie 2026-08-08, INDEX.md-Zeile 27); kein Step-0-Auftrag, kein
  Step-0-Aufräumschritt — Vermerk in `docs/INDEX.md` bleibt korrekt.
- `docs/INDEX.md` — `## Phase 8.5 — 🔄 …`-Abschnitt mit drei INDEX-Zeilen war bereits durch
  den Nikinger angelegt (Planungs-Commit 2026-09-03); Step 0 hat daran nichts geändert.
  Dateigröße 40.917 B — 43 B unter dem Cap, **nicht** 264 B wie nach Fund 1 alleine, weil
  Fund 2 die Ausnahmenliste hinzugefügt hat.

**Verifiziert (§0.5 Checkliste):**

- `pytest -q` (venv): **959 passed in 270.79 s** — unverändert, kein Python-Touch in
  dieser Session (nur `.md` und Skelett-`.md`).
- Tabu-Diff aus §0.3 leer:
  `git diff --stat main -- phase4_auth/ phase1_storage/storage/ phase5_ui/webui/security.py
  phase5_ui/webui/api.py phase5_ui/webui/serializers.py phase5_ui/webui/permissions.py
  phase2_mcp/` — **keine Ausgabe**.
- `node --check` auf JS-Dateien: keine berührt.
- `python phase5_ui/scripts/ui_budget.py`: keine UI-Änderung, irrelevant für Step 0.
- Service-Touch **0**. `systemctl status sharefyx-mcp` zeigt **PID 195922**, Active seit
  `Wed 2026-09-02 11:51:57 CEST` (1 day 21h zum Sitzungsbeginn), CPU 18min 33s — nichts
  angefasst, nur gelesen. **PID + ActiveEnterTimestamp im Session-Block notiert, wie §0.5.7
  verlangt.**
- Größenprüfung `find . -name "*.md" -not -path "./.venv/*" -not -path "*/.pytest_cache/*"
  -size +40k` (Plan §6 Step Z Punkt 6 — vorab geprüft, weil Step 0 schon Doku-Maße ändert):
  jeder Treffer ist entweder 📕 (Plan-Snapshot, `docs/concepts/*_plan.md`) oder bereits
  vorher als „über 40KB-Softcap benannt" markiert (`phase8_ui_graph/CLAUDE.md` 93.562 B,
  `phase6_shares/CLAUDE.md` 41.032 B, `CLAUDE.md` 41.462 B seit diesem Schritt). **Neu durch
  Step 0** ist der Eintrag für `CLAUDE.md` — siehe oben.

**Eine Korrektur am Plan, im Session-Block festgehalten, kein stille Abweichung:**

Fund 1 + Fund 2 zusammen landeten **zunächst 75 B über dem Cap**. Der Plan nennt
„neuesten fünf" explizit, hatte aber die zusätzlichen Bytes der Fund-2-Ausnahmenliste nicht
mitgerechnet (seine Schätzung „mit ihr ~52,7 KB" war ein Vorher-Wert, kein Nachher-Wert).
**Lösung:** Fund 2 als Drei- statt Vierzeiler formuliert, Datei landete auf 40.917 B
(43 B unter dem Cap). Beide Anforderungen — fünf Einträge **und** Ausnahmen dokumentiert —
gehalten, Plan-Wortlaut im Session-Block nicht gebrochen. Wer den Plan liest und `updated:`
als Pipe-getrennte Liste erwartet, sieht sie weiterhin (Schlusszeile ist erkennbar, weil
„ältere Einträge: …" mit Doppelpunkt beginnt).

**Nächster Schritt, konkret:** Block A / **A1 — §9.4.2 Picker-Modus-Umschalter**.
`docs/concepts/phase8_5_picker_release_plan.md` §2.A1 enthält die genauen Eingriffe
(`app.html` Zeile 270–280 mit `<select class="input" id="link-picker-mode">`, `dialogs.js`
Zeile 100–185, `editor.js` Zeile 88–100 + 548–557, `localStorage`-Persistenz unter
`sfx:linkpicker:mode`). Tabu-Diff-Kommando am Step-Ende weiter leer halten — A1 berührt
nur `webui/static/{app.html,app.css,js/dialogs.js,js/editor.js}`.
