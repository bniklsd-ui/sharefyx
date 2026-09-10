---
status: live
purpose: Phase-Head UI-Neuanstrich v3, Verknüpfungs-Graph, drei P7-Erbposten — Scope, harte Regeln, Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase8_ui_graph/ oder an den in §0.4 des Plans genannten Dateien in storage/mcpserver/webui/scripts — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase8_ui_graph_plan.md       # voller Plan, Entscheidungen P8-A–P8-Q, §0.1 gelockte N1–N12, Steps 0/A/B/C/D/Z
  - ../docs/concepts/PHASE7_CLOSEOUT_HANDOVER.md   # Herkunft der drei Erbposten (P7-24/remove-space/P7-4)
  - SESSIONS_ARCHIVE.md                             # ältere Session-Blöcke, newest-first
updated: 2026-09-08 (Z-Final II: §7-Abnahmematrix P8-1 bis P8-26 [alle 26 Zeilen mit Beleg] + Sichtprüfungs-Status-Tabelle nach SESSIONS_ARCHIVE rotiert; Head von 77 KB auf 64 KB reduziert — Rest ist kanonischer Mission/Scope/Modul-Status/Abnahmestand-Intro/C0/Vormerkungen-Pointer/Selection-Choice-Konvention/Session-Block; Frontmatter vorne ergänzt) | 2026-09-08 (Z-Final: Vormerkungen-Sektion (4 Items, 3 erledigt + 1 nach P9) in den SESSIONS_ARCHIVE rotiert; Head von 92 KB auf 77 KB reduziert; Frontmatter vorne ergänzt) | 2026-09-08 (Z-Closeout: Sichtprüfungs-Automatisierung gegen Wegwerf + echte Produktion, Statusregel geändert (Nikinger-geprüfte Wegwerf-Automatisierung zählt als live-verifiziert), Bilanz 26 ✅ · 0 🟡 · 0 ⬜ -- Phase 8 formal abgeschlossen; P8.6 (→v3.0.2) + P9 (→v3.1.0) als Folgephasen vorgemerkt; stale 2026-09-02-Block rotiert nach SESSIONS_ARCHIVE.md) | 2026-09-07 (Cluster-2-Sichtprüfung 2 + 3 am echten Gerät — erste echte Live-Verifikations-Welle seit D3; Nikinger gegen v3.0.1 bestätigt: P8-14, P8-15, P8-18, P8-19, P8-23 ✅; P8-5, P8-8, P8-16, P8-20/21, P8-22, P8-24 bleiben 🟡 für Cluster 3/5 + Phase-8-§7-Statusregel; Screenshot `phase8_5_picker_release/screenshots/Bildschirmfoto 2026-09-07 um 17.08.37.png` zeigt tabellose Space-Zeilen + Zähler-Chips + VERKNÜPFUNGEN-Graph (eigen blau + geteilt türkis + fremd grau dank Fix B vom 2026-09-02) + ZULETZT-BENUTZT-Sektion + Badge `SHAREFYX v3.0.1`; P8.5-18 jetzt ✅ als Umbrella; Phase-8-Bilanz 14/12/0 → 19/7/0, Phase-8.5-Bilanz 4/13/3 → 5/12/3; Phase-8-Glyph-Entscheidung noch offen, Vorschlag vorerst 🟡 bis Cluster 3/5; P8-16-Werfer-Eidenz aus Cluster-1 ergänzt die Phase-8-§7-Zeile, Status bleibt 🟡 weil §7-Statusregel „✅ = live-verifiziert" gilt; Phase-Head 94.3 KB, Phase 8 geschlossen, exempt) | ältere Einträge: phase8_ui_graph/SESSIONS_ARCHIVE.md
---

# CLAUDE.md — Phase 8: UI-Neuanstrich v3, Verknüpfungs-Graph, QoL (`phase8_ui_graph/`)

> Kein eigenes Python-Paket (wie `phase3_edge/`, `phase6_shares/`, `phase6_5_tools_images/`,
> `phase7_spaces_admin/`) — Servercode bleibt in `storage`/`mcpserver`/`webui`/`scripts`.
> **Quelle der Wahrheit ist der Code, nicht dieses Dokument.**

---

## Mission (zuerst lesen)

Vier Blöcke, Reihenfolge 0 → A → B → Gate → C → D → Z: **A** = drei P7-Erbposten schließen
(P7-24-TOTP-Replay per Reauth-Grant, `remove-space`-Auto-Reindex, P7-4-Zweitprobe) — fällt unter
Druck **nie**. **B** = Link-Fundament, achte P1-Contract-Öffnung (`storage/linkscan.py`,
`item_links`-Tabelle, `GET /api/v1/graph`). **C** = Design-Fundament v3, De-AI-isierung (IBM
Plex, Lucide-Sprite, Farblegende own/shared/foreign, Liquid-Glass-Akzente mit Pflicht-Fallback).
**D** = Übersicht tablos + handgerollter Canvas-Force-Graph.

**Erstmals opencode/M3 als Ausführender ab Block A** (P7-Handover §7) — Step 0 (diese Sitzung)
läuft noch in Claude Code, gemeinsam mit dem Nikinger, und stellt die opencode-Fähigkeits-Parität
her. **Kein Advisor während der Ausführung (P8-L, N12)** — Ersatz: Selbstprüf-Checkliste §0.6 des
Plans + zwei Nikinger-Sichtprüfpunkte.

## Scope

- **DRIN:** die drei P7-Erbposten, Link-Extraktion + Graph-Endpunkt, Design v3
  (Typografie/Icons/Farben/Glas), Übersicht tablos + Force-Graph, `AGENTS.md`-Entfernung,
  opencode-Einrichtung.
- **DRAUSSEN:** FastMCP-4/V79 (eigene Mini-Phase), Body-Volltextsuche, Rechteverwaltung über
  MCP-Tools, neues MCP-Tool für den Graph, Löschen von Items, `_trash/`-Räumung,
  Funnel-Watchdog, Mobile/Realtime, Light-Mode. Volle Liste: Plan §0.5 „DRAUSSEN".

Details, gelockte Entscheidungen P8-A–P8-Q, Verbots-/Tabu-Liste, Schritt-Sequenz, Testliste,
Abnahmezeilen: `docs/concepts/phase8_ui_graph_plan.md`.

**P8-N — ein Dokument pro Phase:** der Closeout wird §9 des Plans, kein separates Handover.

## Modul-Status

| Block | Inhalt | Status |
|---|---|---|
| Step 0 | Fundament-Session (Haushalt, AGENTS.md weg, Skelett, opencode-Setup, Smoke-Test) | ✅ |
| A1 | Reauth-Grant (`webui/reauth.py :: ReauthGrantStore` + Endpoint + Client + Tests, N=14-Batch) | ✅ live-verifiziert (`90441b29`), Test-Space-Probe, ein TOTP-Code für N rechteerweiternde Items |
| A2 | `remove-space`-Auto-Reindex (`spacectl.py :: _cmd_remove_space()` → `store.rebuild_index()`) | ✅ live-verifiziert (`90441b29`), `Test_Space_A2` Remove → 4× `GET /api/v1/overview` 200, Index konsistent |
| A3 | P7-4: organische Zweitprobe + `_TITLE_NOT_ID_HINT` schärfen | 🟡 gebaut + deployt (`7254aa9`, 2026-09-01); Drittprobe (P8-5) **Restdefekt**: Plain-Text sauber, **Klammer-/Aufzählungs-Kontext** nennt weiterhin die `itm_…`-ID — Hint deckt zwei Negativ-Beispiele (plain + Tabelle), Klammern sind eine dritte, nicht genannte Form. **Bleibt 🟡 mit Defekt** (Nikinger-Entscheidung 2026-09-01); der Restdefekt wandert als benannter Defekt in den Phase-8-Closeout (`docs/concepts/phase8_ui_graph_plan.md` §9), wie P7-24/P7-4 damals |
| B1 | `storage/linkscan.py` neu (`ITEM_REF_RE`, `extract_item_refs(body)`) + 15 Tests | ✅ gebaut + live-verifiziert (`ed43ed6` deploy `007b73d`, 2026-09-01); achte P1-Contract-Öffnung angekündigt in `phase1_storage/CLAUDE.md` §Geerbte Contracts (Disziplin der Vorgänger-Öffnungen 3–7); Tabu-Diff leer, Charakterisierungstests byte-identisch grün, 169 phase1_storage-Tests gesamt |
| B2 | `index.py` (`INDEX_SCHEMA_VERSION = 3`, `item_links`-Tabelle + Index, `replace_item_links()`, `all_links()`, `row_from_file` ↳ `body_refs`, `rebuild_index` populiert, `delete_item` räumt src-Zeilen) + `store.py` (`_replace_links_for_item()`, `Store.links_all()`, alle 6 Schreibpfade via `_write_item_file` plus Drift-Repair) + 22 Tests | ✅ gebaut + live-verifiziert (`f4c8844` deploy `007b73d`, 2026-09-01); Tabu-Diff leer, Charakterisierungstests byte-identisch grün, 191 phase1_storage-Tests gesamt (vorher 154 + 15 B1 + 13 B2-index + 9 B2-store) |
| B3 | `webui/api.py :: _graph_get()` + Route `GET /api/v1/graph` + 8 Tests | ✅ gebaut + live-verifiziert (`58ff9a6` deploy `007b73d`, 2026-09-01); Tabu-Diff leer, Charakterisierungstests byte-identisch grün (P5-B-Disziplin gehalten: nur `mcpserver.permissions.SharePolicy` importiert in webui/) |
| B4 | UI: `#item/`-Klick-Delegation (`app.js`) + Link-Picker-Dialog (`app.html`/`app.css`/`dialogs.js`/`editor.js`) | ✅ gebaut + live-verifiziert (`ea14d53` deploy `007b73d`, 2026-09-01); Tabu-Diff leer (insb. `webui/security.py` P8-Q unangetastet); JS-Syntax-Check `node --check` auf `app.js`/`editor.js`/`dialogs.js` OK; 34 statische-Tests grün; ui_budget 5/5 grün (91/250 KB app.js+css+Font) |
| Block B abgeschlossen | `linkscan.py` + `item_links` + `Store.links_all` + `GET /api/v1/graph` + UI-Wiring | ✅ **live-verifiziert** (`007b73d`, 2026-09-01, Release `20260901T103944.634877Z`, Health-Gate 3/3, Versionsbadge v2.2.3); achte P1-Contract-Öffnung bleibt **angekündigt**, geschlossen mit Phase-8-Step-Z |
| Block C | Design-Fundament v3 (Typografie, Icons, Farben, Glas) | 🔄 C0 ✅ · C1 ✅ gebaut (C1a Font-Swap + C1b CSS-Tokens) · C2 ✅ gebaut (Lucide-Sprite, 18 Icons, build_icon_sprite.py, js/icons.js, .icon CSS) · C3 ✅ gebaut (Farbsemantik --space-own/shared/foreign + .rail__glyph--{cat}, .space-dot--{cat}, .legend) · C4 ✅ gebaut (Liquid-Glas-Akzente, .list__head sticky, Auswahl-Sheen 3px + Outline) · C5 ✅ gebaut (F5 ::selection + F21 72ch-Editor + F22 Padding-Token) · wartet auf Nikinger-Sichtprüfung 3 am echten Gerät |
| Block D | Übersicht tablos + Force-Graph | ✅ D1+D2+D3 gebaut (D1 = Übersicht tabellos + globaler Home-Scope, D2 = handgerollter Canvas-Force-Graph, D3 = Versionierung v3.0 + UPDATE_LOG + Sichtprüfung 2 + README Sneak Peak) — **[2026-09-02] drei Restdefekte aus den P8-22/P8-24-Smokes in D2s `js/graph.js`/`webui/api.py` geschlossen** (Settle-Zeit `ALPHA_DECAY`/`ALPHA_MIN`, Foreign-Farbe `writable` statt `shared`, Knotenklick → Item via `onMouseUp`/`selectItem`; Plan §9.4.6, Nikinger-Entscheidung Option (a) für alle drei) — **[2026-09-07] Cluster 2 Sichtprüfung bestätigt P8-14/15/18/19/23 ✅; [2026-09-07] Cluster 3 bestätigt P8-20 ✅ (Hover dimmt, Klick öffnet Editor/Readonly, Drag/Zoom/Pan) und P8-21 a/b/c ✅ (Default explizit, Tag-Toggle, Ordner-Toggle), P8-21 d bleibt für die 200-Knoten-Wegwerf-Session übrig, P8-22 und P8-24 komplett in eine Folge-Session verschoben** (Wegwerf-Setup ist Nikinger-Aktion) |
| Step Z | Closeout | ⬜ |

## Geerbte Contracts

Achte P1-Contract-Öffnung (P8-M) wird in Block B benannt und gebaut — Eintrag folgt in
`phase1_storage/CLAUDE.md` §„Geerbte Contracts" im Öffnungs-Commit, nicht hier dupliziert.

## Abnahmestand (Plan §7, P8-1–P8-26)

**Statusregel geändert 2026-09-08 (Nikinger-Entscheidung, Sichtprüfungs-Automatisierungs-
Sub-Session):** ✅ = live-verifiziert durch den Nikinger — **das schließt ab sofort eine vom
Nikinger selbst geprüfte Wegwerf-Instanz-Automatisierung mit ein**, nicht mehr nur einen
eigenhändigen Klick-Durchlauf am echten Gerät. Begründung wörtlich: „die throwaway ist,
except for files and user, byte by byte identical to the new prod after deploy" — dieselbe
Codebasis wie die Produktion, unterscheidet sich nur in `DATA_ROOT`/`auth.sqlite3`/Identität.
Voraussetzung bleibt: der Nikinger hat die Screenshots/Ergebnisausgabe tatsächlich gesehen —
ein unbeaufsichtigter Skriptlauf allein zählt weiterhin nicht als ✅. (W) = Wegwerf-Instanz +
vom Nikinger geprüfte Evidenz reicht ab sofort für ✅, (L) = weiterhin nur gegen die echte
Produktion beweisbar (Identitäts-Kriterien wie „der bereits autorisierte Connector lebt
noch"), (C) = Code/Test reicht. Volle Herleitung: `docs/concepts/
sichtpruefung_automation_conventions.md`. **Zwei benannte Restdefekte wandern weiterhin in
den Closeout (§9):** Item-Link-Picker füllt nur Frontmatter (Vormerkung), A11y
`aria-selected` im Link-Picker nie per JS gesetzt (Nebenfund 2026-09-02). Die A3-Klammer-/
Aufzählungs-Kontext-Zeile (P8-5) ist mit der 2026-09-08-Sichtprüfung geschlossen (§7 unten) —
kein Restdefekt mehr.

## Abnahmestand (Plan §7, P8-1–P8-26)

**Statusregel geändert 2026-09-08 (Nikinger-Entscheidung, Sichtpruefungs-Automatisierungs-
Sub-Session):** ✅ = live-verifiziert durch den Nikinger — **das schliesst ab sofort eine vom
Nikinger selbst gepruefte Wegwerf-Instanz-Automatisierung mit ein**, nicht mehr nur einen
eigenhaendigen Klick-Durchlauf am echten Geraet. Begruendung woertlich: „the throwaway is,
except for files and user, byte by byte identical to the new prod after deploy" — dieselbe
Codebasis wie die Produktion, unterscheidet sich nur in `DATA_ROOT`/`auth.sqlite3`/Identitaet.
Voraussetzung bleibt: der Nikinger hat die Screenshots/Ergebnisausgabe tatsaechlich gesehen —
ein unbeaufsichtigter Skriptlauf allein zaehlt weiterhin nicht als ✅. (W) = Wegwerf-Instanz +
vom Nikinger gepruefte Evidenz reicht ab sofort fuer ✅, (L) = weiterhin nur gegen die echte
Produktion beweisbar (Identitaets-Kriterien wie „der bereits autorisierte Connector lebt
noch"), (C) = Code/Test reicht. Volle Herleitung: `docs/concepts/
sichtpruefung_automation_conventions.md`. **Zwei benannte Restdefekte wandern weiterhin in
den Closeout (§9):** Item-Link-Picker fuellt nur Frontmatter (Vormerkung), A11y
`aria-selected` im Link-Picker nie per JS gesetzt (Nebenfund 2026-09-02). Die A3-Klammer-/
Aufzaehlungs-Kontext-Zeile (P8-5) ist mit der 2026-09-08-Sichtpruefung geschlossen (§7 unten) —
kein Restdefekt mehr.

**Vollstaendige §7-Abnahmematrix P8-1 bis P8-26 + Sichtpruefungs-Status-Tabelle (alle Belege
inkl. Commit-SHAs, Screenshots und Nikinger-Verweise):** `SESSIONS_ARCHIVE.md`
§Abnahmematrix-Archiv (Phase 8, Z-Final-Rotation). Bilanz-Summary und Bilanz-Awk bleiben
direkt unten im Head.


### Bilanz (Stand 2026-09-08 — Phase 8 vollständig ✅, Closeout vollzogen)

**26 ✅ · 0 🟡 · 0 ⬜** von 26 Zeilen — maschinell gezählt:

```
awk '/^\| P8-[0-9]+ /{ if (/\| ✅ \|/) g++; else if (/\| 🟡 \|/) y++; else if (/\| ⬜ \|/) o++; n++ } \
  END {printf "Zeilen=%d ✅=%d 🟡=%d ⬜=%d\n", n, g, y, o}' phase8_ui_graph/CLAUDE.md
```

Ausgabe dieses Kommandos (2026-09-08): `Zeilen=26 ✅=26 🟡=0 ⬜=0`. Die letzten sechs Zeilen
(P8-5, P8-8, P8-16, P8-21, P8-22, P8-24) sprangen in einer Sichtprüfungs-Automatisierungs-
Sub-Session von 🟡 auf ✅ — fünf davon (P8-8/16/21/22/24) unter der **an diesem Tag geänderten
Statusregel** (§Abnahmestand oben: vom Nikinger geprüfte Wegwerf-Automatisierung zählt jetzt
als live-verifiziert), eine (P8-5) mit echter Live-Evidenz gegen die Produktion (Screenshot
des echten claude.ai-Connectors). **Phase 8 ist damit formal ✅ — Closeout (P8-N/§9) vollzogen
mit diesem Commit**, kein separates Handover-Dokument (Konvention seit P7: der Closeout lebt
hier im Phase-Head, nicht in einer eigenen Datei).

**Zwei benannte Restdefekte bleiben offen, vererbt an die nächste Phase (P8.6):**
Item-Link-Picker füllt nur Frontmatter, nie den Body-Text (Vormerkung seit B4); A11y
`aria-selected` im Link-Picker nie per JS gesetzt (Nebenfund 2026-09-02). Beide sind
kosmetisch/UX, kein Sicherheits- oder Korrektheitsdefekt — dieselbe Kategorie wie P7-24/P7-4
damals an Phase 8 vererbt wurden.

---

## C0 — Anti-AI-Pattern-Research + UI-Audit (P8-25, Plan §4.C0)

**Auftrag:** vor dem ersten UI-Commit in Block C einmal bewusst hinschauen, was die
LLM-Default-Aesthetik 2026 überhaupt ist — und gegen den Code hier halten. „Wir benutzen
keine schablonenhaften AI-Looks" lässt sich nur behaupten, wenn man die Schablonen kennt.
V94 (Web-Recherche für C0-Teil 1) bestätigt: opencode hat brauchbare Web-Recherche.

**Quellen (Teil 1, 2026-09-01):**

| Quelle | Kernbeitrag |
|---|---|
| developersdigest.tech — *AI Design Slop: 16 Patterns That Out Your App as Vibe-Coded* (Krebs' Show-HN-Audit, 1.590 Seiten) | der 16-Punkte-Score, Methodik (Playwright + DOM/CSS-Checks, kein LLM-Judge), Heavy-Slop-Anteil 22 %, Mild 32 %, Clean 46 %; die zwei dominanten CSS-Fingerabdrücke sind shadcn/ui und Glassmorphism |
| sailop.com — *Complete Guide to Anti-AI Design in 2026* | sieben Dimensionen (Color/Typography/Layout/Animation/Components/Spacing/Craft Signals) mit deterministischen Checks; das `#3B82F6`–`#6366F1`-Blau-Band, die `gray-50`-Hintergrund-Signatur, drei gleiche Cards |
| fountaininstitute.com — *7 Signs a UI Has Been Vibe Coded* | Neon-Paletten, Glow-Effekte, Emoji-Icons, Purple-Gradients, Card-in-Card, mehrfarbige Side-Tabs, bedeutungslose Status-Dots |
| noqta.tn — *Escaping AI Slop: Fix the 4 Overused AI UI Patterns* | „Wes Bos’ vier apokalyptische Reiter": übergroße Border-Radii, Glow-Gradients, breites Letter-Spacing, generische „Live"-Badges |
| monet.design — *7 Tips to Make Your Vibe-Coded UI Look Professional* | Tokens zuerst, 8-px-Raster, Echtcontent statt Lorem, Layering statt One-Shot-Prompt, Animation nur als Feedback |
| dev.to/jaainil — *AI Purple Problem: Make Your UI Unmistakable* | OKLCH statt RGB/HSL, Material-You-HCT als Anti-Mittel gegen Monokultur, Tailwind-Defaults als Trainingsbias auf indigo |
| phase8_ui_graph_plan §0.3 Verbotsliste (sechs Punkte) | die für jeden UI-Commit verbindliche Kompaktform, an der sich jeder Fund messen lassen muss |

**Konsolidierter Befund gegen `app.html`/`app.css`/`js/` (Teil 2):** die App ist überwiegend
schon **nicht** auf dem AI-Default-Pfad — P5-X („Dunkel-first, Apple-Formensprache vor
Liquid Glass") und P5-U („nüchterne deutsche UI-Texte") haben die gröbsten Tells
bereits ausgeschlossen. Was bleibt, sind die fünf echten Funde (F1, F9, F10, F11, F16/F19)
plus die sechs Stellen, an denen der Plan-C1–C5/D1 sowieso ansetzt (F12/F13 werden von D1
abgelöst, F4/F20/F21/F24 von C1/C5, F8 bleibt ein bewusster Einzelfall). Keine Funde
eskaliert (P8-25, „benannte Nikinger-Entscheidung"); die Verbotsliste §0.3 hält.

### Findings-Tabelle (Muster → Fundstelle → Fix → Ziel-Step)

| # | Muster (Quelle) | Fundstelle (Datei:Zeile) | Fix | Ziel-Step |
|---|---|---|---|---|
| **F1** | Inter als alleinige Schrift, kein Display-Cut, keine echte Skala — *developersdigest Punkt 1–3* | `app.css:14` (`@font-face Inter Variable`), `:44` (`--font-ui: "Inter Variable"…`), `:83` (`font-size: 15px`) | Plex Sans (variabel, 380–620) + Plex Mono statisch; OFL.txt getauscht; Basis 16 px; Skala als Tokens | **C1** |
| **F2** | Inter-`OFL.txt` muss raus, Plex-`OFL.txt` muss rein (lizenzrechtlich Pflichtbestandteil) | `phase5_ui/webui/static/fonts/OFL.txt` (Inter-Lizenz, 2025-11-22-Datum im Header) | Plex-OFL.txt ersetzen, Lizenztext-Pin wie `build_font_subset.sh` heute schon | **C1** |
| **F3** | Skala als Streu-px (13/14/15/22), keine Tokens | `app.css:83,102–104,243–247,313–320,515–531,572–577,602–603,621–622,802–804` und weitere | `--fs-meta/ui/body/title/page` als Tokens (Plan §4.C1); 16 px body; 1.55 line-height | **C1** |
| **F4** | Body-Schriftgröße 15 px statt 16 px (AI-Default, *Sailop Dim 2*) | `app.css:83` (`body { font-size: 15px; }`) | 16 px + 1.55 line-height (Plan §4.C1) | **C1** |
| **F5** | Kein `::selection`-Styling (Sailop Dim 7, „craft signal") — Text-Highlight ist Browser-Default-Blau | `app.css` (kein `::selection`-Block) | `::selection { background: var(--accent-quiet); color: var(--text); }` als einzige semantische Farbverwendung | **C5** (gehört zur Schriftrundung) |
| **F6** | IDs/Versionen/Metazeilen rendern in Default-Sans (klein, unauffällig), kein Mono-Akzent — *Fountain Institute „Cards for every block of info"* — vermischt Hierarchie-Ebenen | `app.html:95,112` (`#editor-version`, `#meta-item-id`); `app.css:99,785` | IDs/Versionen in `--font-mono` (Plan §4.C1, „IDs, Versions-Badge und Metazeilen rendern in `--font-mono`") | **C1** |
| **F7** | Akzentton-Vereinheitlichung schon gut (Uniformitäts-Wunsch P7-U) — `--accent: #3E8DF3` ist das einzige Blau; keine zweite Akzentfarbe (war früher `--ok` grün, schon zurückgenommen am 2026-08-16) | `app.css:33` (`--accent`), `:546` (`visibility-chip--shared`), `:1048` (`.toast`) | bleibt — kein weiterer Eingriff nötig | **bereits aligned** |
| **F8** | Radiales Auth-Page-Backdrop (Funktion: zieht den Blick zur zentrierten Karte) | `app.css:1186` (`.auth { background: radial-gradient(120% 80% at 50% 0%, #131A23 0%, var(--bg) 70%); }`) | bewusst kein Eingriff — Verbotsliste §0.3 Punkt 2 zielt auf Branding-Flächen, nicht funktionalen Auth-Vordergrund | **bewusst belassen** |
| **F9** | HTML-Entities als Icons (Verbotsliste §0.3 Punkt 1 — *Fountain Institute „Emojis used as icons"*) | `app.html:23` `&#8962;` (Übersicht), `:33` `&#9881;` (Konto), `:39` `&#9099;` (Abmelden), `:50` `&#43;` (Anlegen), `:151` `&#128279;` (Link), `:153` `&#8221;` (Zitat), `:157` `&#128444;` (Bild) | Lucide-Icon-Sprite: `house`/`settings`/`log-out`/`plus`/`link`/`quote`/`image` (Plan §4.C2 Ersetzungs-Map, V92 für die gepinnten Namen) | **C2** |
| **F10** | Text-Glyphen als Icons (gleiche Kategorie wie F9) | `list.js:351` `→` (Verschieben), `:368` `⇄` (Freigeben); `tree.js:203` `▾`/`▸` (Twist); `app.html:83,102` `&times;` (Editor-Schließen, Nur-lesen-Schließen) | `folder-input`/`share-2`/`chevron-down`/`chevron-right`/`x` (Plan §4.C2) | **C2** |
| **F11** | Lucide-Sprite-Infrastruktur partiell: B4 referenziert `#icon-search`, aber kein `<symbol id="icon-…">`-Block existiert in `app.html` — das `use href="#icon-search"` würde heute ins Leere zeigen | `app.html:135` (Verwendung) — `<!-- ICONS:BEGIN -->`-Marker fehlt | Vendoring unter `phase5_ui/vendor/lucide/` (ISC-Lizenz), Generator `build_icon_sprite.py` schreibt den Sprite-Block zwischen Marker (Plan §4.C2); THIRD_PARTY_LICENSES.md neu | **C2** |
| **F12** | Bucket-Counter-Grid (`overview__tiles`) — *Sailop Dim 5/6* „3 identical cards" — funktional, kein Marketing-Grid, aber **ersetzt durch D1** | `app.html:73` (Container); `app.css:579–603` (`.overview__tiles`/`.tile`); `list.js:40–47` (Render) | **ersetzt durch P8-J „tabellose Space-Zeilen mit klickbaren Zählern"** — keine Card-Optik | **D1** (löst es auf) |
| **F13** | Space-Cards für fremde Spaces (`space-card`, identisches Padding+Radius) — *Sailop Dim 5* | `app.html:71–77` (`overview`); `app.css:624–641`; `list.js:74–84` | ersetzt durch P8-J tabellose Zeilen | **D1** (löst es auf) |
| **F14** | Linke Akzentkante an ausgewählter Listenzeile + Akzent-Outline + `.list__rows > li.list__row--selected { box-shadow: inset 2px 0 0 var(--accent); }` — **NICHT** der AI-Tell „rainbow left borders" (eine Farbe, semantisch), aber **P8-H verlangt zusätzlich solide Indikatoren** (3 px-Akzentkante + Outline) | `app.css:471, 480–483, 510–513` | P8-H-Glass: 3-px-solide Akzentkante links + 1-px-Akzent-Outline, damit Auswahl bei deaktiviertem Blur/reduzierter Transparenz vollständig erkennbar bleibt | **C4** (deckt es ab) |
| **F15** | `.preview blockquote { border-left: 3px solid var(--accent); }` — semantisch (Zitatakzent), eine Farbe, **kein** AI-Tell | `app.css:699` | bleibt | **bereits aligned** |
| **F16** | Kein `prefers-reduced-transparency`-Handling (P8-H Pflicht, V85) — Firefox-Benutzer mit aktiviertem Systemsetting sehen heute Glas nicht, aber die App hat heute noch gar kein Glas | `app.css` (fehlt) | `@media (prefers-reduced-transparency: reduce) { .glass { backdrop-filter: none; background: var(--surface-raised); } }` | **C4** |
| **F17** | `:focus-visible` schon da (`app.css:108`); `prefers-reduced-motion` schon da (`app.css:113`) | beide Sailop-Dim-7-Signale abgehakt | bleibt | **bereits aligned** |
| **F18** | Animation 120 ms unter dem 200–300-ms-Profi-Bereich, kein `animate-pulse`/`scale-on-hover`/Framer-Motion, keine Scroll-Reveals | `app.css:119–122` (transition-Liste) | bleibt | **bereits aligned** |
| **F19** | Border-Radius diszipliniert (Token-gesteuert: `--radius: 10px`/`--radius-sm: 6px`, Pill nur dort wo es semantisch passt) — *Noqta „übergroße Border-Radii"* vermieden | `app.css:40–41` (Tokens), `:436,449,540` (Pill, semantisch) | bleibt | **bereits aligned** |
| **F20** | `--space: 8px` mit strikten Vielfachen — *Monet „8-px-Raster"* eingehalten | `app.css:42` | bleibt | **bereits aligned** |
| **F21** | Body-Lesebreite unbegrenzt im Editor (`max-width` nur in `.preview` Padding, nicht in Editor-Textarea) | `app.css:1010–1021` (`.editor__textarea`), `:163–167` (`editor__body`) | `max-width: 72ch;` auf Editor-Body + zentrierte Spalte (Plan §4.C5) | **C5** |
| **F22** | Editor-Body `padding-left: 12px` außerhalb des Space-Tokens (geringfügige Drift, *Monet „konsistentes 8-px-Raster"*) | `app.css:987` (`.editor__body`) | 12 px → `calc(var(--space) * 1.5)` | **C5** |
| **F23** | Drei gleiche Tiles (Bucket-Counter) als Default auf der Übersichtsseite — *Fountain Institute Punkt 5 „Cards for every block of info"* | siehe F12 (dort aufgelöst) | siehe F12 | **D1** |
| **F24** | Keine „Live"-Puls-Dots / keine „New"-Pillen / keine bedeutungslosen Status-Dots — *Fountain Institute Punkt 7* | `app.css` (keine `animation: pulse`) | bleibt | **bereits aligned** |
| **F25** | Keine generische Marketing-Mikrocopy („Build the future", „Scale without limits") — *Noqta „Rewrite the copy in a real voice"* — alle UI-Texte sind nüchternes Deutsch (P5-U) | `app.html`/`app.js`/`js/*.js` (Stichprobe: „Übersicht", „Verschieben", „Speichern", „Abbrechen", „Konflikt", „Erneut anmelden", „Aktuelle Fassung laden") | bleibt | **bereits aligned** |
| **F26** | Kein zentrierter Hero mit Badge über H1 — *developersdigest Punkt 10*, *Sailop Dim 3* — eine Daten-UI hat das nicht, die Übersichtsseite hat `h1.overview__title` (linksbündig, kein Badge darüber) | `app.css:569` (`.overview__title { margin-bottom: var(--space) * 2; }` — keine zentrierten Helden) | bleibt | **bereits aligned** |
| **F27** | Kein shadcn/ui-Visual (eigene Handrolle-CSS seit P5 Step 7b, *developersdigest „CSS-Fingerabdrücke"*) | `app.css` (kein `@apply`, keine shadcn-Tokens) | bleibt | **bereits aligned** |
| **F28** | Keine Aurora-Borealis-Backgrounds / großen farbigen Box-Shadows / Glow-Effekte — *Fountain Institute Punkt 2* | `app.css` (21 box-shadows, alle klein: `0 1px 2px`, `0 3px 8px`, einer 24 px für Modals) | bleibt | **bereits aligned** |
| **F29** | Kein „Magic Blue" Linear-Style (eigener Blauton `#3E8DF3`, *dev.to* „Linear-Aesthetic") | `app.css:33` | bleibt | **bereits aligned** |
| **F30** | Kein `accent-color`-Default-Verlust (am `<select>` schon explizit gesetzt, damit native Optionsliste nicht lila wird — Nikinger-Fund 2026-08-16) | `app.css:202` (`accent-color: var(--accent);`) | bleibt — *das* ist die richtige Antwort auf „AI-Purple-Problem", nicht „auf eine andere Markenfarbe wechseln" | **bereits aligned** |
| **F31** | Kein `::placeholder`-Color-Bloat — `app.css:31` hat `--text-placeholder: #7E8A98` (semantisch, ein Wert) | `app.css:192` | bleibt | **bereits aligned** |
| **F32** | Keine Mehrfach-Side-Tabs in Regenbogen-Farben (Fountain Institute Punkt 6) — eine einzelne Akzentkante an ausgewählter Zeile, *semantisch* | `app.css:480–483` | bleibt | **bereits aligned** |
| **F33** | Keine „Tailwind-blue-purple gradient"-Signatur (Sailop Dim 1, dev.to „AI-Purple-Problem") — die einzigen Gradients sind 180-deg-Erhöhungs-Verläufe auf Buttons/Tiles/Rail (*funktional*, *nicht dekorativ*, Verbotsliste §0.3 Punkt 2 zielt auf Branding-Flächen) | `app.css:125,134,137,142,153,156,224,283,296,434,481,591,928,1044,1074,1152,1192` | bleibt — nur F8 (Auth) wird bewusst nicht angetastet | **bereits aligned** |
| **F34** | Keine Tailwind-`gray-50`-Hintergrundsignatur (Sailop Dim 1) — eigener dunkler Grund `#0B0D10` | `app.css:22` (`--bg`) | bleibt | **bereits aligned** |
| **F35** | Keine Emoji-Icons (Unicode-Emoji) im UI — *Fountain Institute Punkt 3*, Plan §0.3 Verbotsliste | alle JS-Dateien (Stichprobe, kein `:rocket:`/`:white_check_mark:`/`:lock:`) | bleibt | **bereits aligned** |

**Zusammenfassung für die nächsten Steps:**
- **C1** trägt: F1, F2, F3, F4, F6 (Fonts/Tokens/Skala, sechs Stellen)
- **C2** trägt: F9, F10, F11 (alle Icons, Sprite-Infrastruktur, ~10 Stellen)
- **C3** trägt: keine direkten Findings (Farben sind bereits aligned), C3 fügt nur die
  drei Kategoriefarben `space-own`/`space-shared`/`space-foreign` + `.legend` hinzu
- **C4** trägt: F14, F16 (Glass-Akzent + Pflicht-Fallback, zwei Stellen)
- **C5** trägt: F5, F21, F22 (Selection, 72ch, Space-Token-Drift, drei Stellen)
- **D1** trägt: F12, F13, F23 (tabellose Übersicht statt Tiles/Cards — drei Stellen, von D1 aufgelöst)

**Keine Fund-Eskalation nötig** (P8-25): kein Fund ohne Ziel-Step, kein benannter Widerspruch
zu einer gelockten Entscheidung. F8 ist die einzige Stelle, an der die Verbotsliste §0.3 mit
einem bestehenden Verlauf in Berührung kommt — und sie ist durch ihre Funktion (Auth-Vordergrund)
gerechtfertigt; bewusst belassen, dokumentiert hier.

---

## Versions-Bump v2.2 → v2.2.3 (2026-09-01)

`.rail__version` in `phase5_ui/webui/static/app.html` Z. 20: `v2.2` → `v2.2.3`.
**Begründung:** Nikinger führt eine dritte Versionsstelle ein — „die letzte Zahl
der Version entspricht, wenn hinzufügt, der Step-Nummer". Phase 8 Block A Step 3
= A3, daher `v2.2.3`. Bisherige Konvention (P7-U): der Badge zählte Deploy-Zyklen
in zwei Stellen (`v2` → `v2.1` → `v2.2`); die dritte Stelle setzt diese Linie
fort, nicht ersetzt sie — Major (`v2`) bleibt, Minor (`v2.2`) bleibt bis zur
nächsten Phasen-Bumpscheidung, Patch (`v2.2.3`) ist der Step-Counter innerhalb
der Phase. Nur `app.html`-Änderung; `mcpserver.__version__` (`0.1.0`) bleibt
unangetastet (anderes Schema, Python-Introspection, nicht der User-Badge).

---

## Vormerkungen (nicht Teil eines aktuellen Steps)

Vier Vormerkungen aus Phase 8 (drei Nikinger-Sichtpruefungs-Notizen + eine Recherche-Luecke);
**drei davon erledigt** (Selection/Choice-Konvention v3, Listenzeilen-Sheen, Chevron-Fixes),
**eine davon offen und nach P9 verschoben** (Obsidian-Uebersicht-WIP, Nikinger explizit bestaetigt
am 2026-09-02). Volle Verlaufsdokumentation mit den ERLEDIGT-Markern, Funden und Begruendungen
pro Item: `SESSIONS_ARCHIVE.md` §Vormerkungen-Archiv. Aufnahme in den Head erst wieder, wenn ein
neues Vormerkungsthema auftaucht — bis dahin ist die Sektion ein Pointer.

**Aktuell offen (nach P9):** „Obsidian Uebersicht weiterhin WIP" — Block D (tabellose Uebersicht +
Canvas-Force-Graph) ist gebaut und live (`sp2_*`, `c4c5_*`, `d1_*`/`d2_*`), Nikinger hat am
2026-09-02 bestaetigt, dass noch Ueberarbeitung ansteht — gehoert in den Obsidian-Map-Umbau
(Phase 9, `p8x_ui_polish_notes.md` §2). Bis dahin kein Handlungsbedarf in Phase 8.


## Selection/Choice Konvention v3 (Block C, Vormerkung 1 vom 2026-09-01 beantwortet)

**Anlass:** Vormerkung 1 vom 2026-09-01 fragte nach der „Auswahl"-Kategorie. Die App hat
heute vier optisch verwandte, semantisch aber verschiedene Affordances — die Konvention
sortiert sie und legt fest, was wann verwendet wird. Verbindlich ab sofort für jeden
neuen UI-Commit in `webui/static/`.

**[2026-09-10, P8.6-A4/P8.6-G]** um die Kategorie „Vorsicht" ergänzt (Block A, N4/P8.6-F).
Die Konvention hat damit fünf Kategorien statt vier. Sie ist **kein** zweites Konventions-
Dokument — `DOC_LAYERS_CONVENTION.md` verbietet zwei Kopien derselben Regel — und der Phase-8-
Head ist der Ort, an dem sie ohnehin bei jedem UI-Commit gelesen wird.

### Die fünf Kategorien

| Kategorie | Was es macht | Vorbild (Code, Selector) | Visuelle Sprache |
|---|---|---|---|
| **Choice** | *echte Auswahl* zwischen N Werten — einer, keiner oder viele davon gleichzeitig | `<select class="input">` (Vorbild: `#move-space-select`) | sunken (`.input`-Träger) + Lucide-Chevron-down rechts + `accent-color: var(--accent)` für Popup-Highlight |
| **Toggle** | einzelner Bool-Zustand — an/aus, ein/aus, sichtbar/unsichtbar | Buttons mit `aria-pressed` (z. B. `.pw-toggle`, `#home-button`) ODER `<input type="checkbox">` (z. B. `#overview-graph-toggle-tags`) | Button: linear-gradient + 1 px line; Checkbox: native Browser-Default mit `--accent` |
| **Status** | *Anzeige*, nicht Auswahl — was der Zustand IST, nicht was man darauf anwenden kann | `.visibility-chip`, `.list__row-meta`, `.rail__version`, `.tree__badge` (count) | Pill / Mono-Akzent / small-meta, niemals klickbar |
| **Navigation** | *Springt wohin*, oft mit Zähler verbunden — kein „Wert setzen", sondern „woanders hin" | `.tree__scope` (Bucket-Filter) mit `aria-current="true"`, `.tree__folder`, `.tree__space` (Space), `.overview__space-count` (Counter-Chip) | Akzent-Gradient-Fill wenn aktuell (`linear-gradient(180deg, rgba(62,141,243,.20), rgba(62,141,243,.08))`), sonst transparent |
| **Vorsicht** | Aktion mit **Rückweg-Kosten** — nicht zerstörend, aber teuer rückgängig zu machen | `#logout-button`, `#archive-button` (Trägerklasse `.action--caution`) | Standard-Knopfplastik, aber `color: var(--caution)` auf Label und Glyph; **keine** gefüllte rote Fläche |

**Vorsicht ist keine Bestätigungspflicht.** Ein Knopf dieser Kategorie darf trotzdem einen
Bestätigungsdialog haben (Archivieren hat einen), aber die Farbe ersetzt ihn nicht und
verlangt ihn nicht.

### Choice — das Vorbild im Detail (Anker für künftige Commits)

- **Markup:** natives `<select class="input" id="…">`, **nicht** ein eigenes `<div>`/`role="listbox"`-
  Konstrukt. Die App hat heute 7+1 Choice-Stellen, alle identisch:
  1. `#field-status` (Item-Editor, Status)
  2. `#create-type` (Anlegen-Dialog, Item-Typ)
  3. `#new-folder-parent-select` (Anlegen-Dialog, Übergeordneter Ordner)
  4. `#move-space-select` (Verschieben-Dialog, Ziel-Space)
  5. `#move-folder-select` (Verschieben-Dialog, Ziel-Ordner)
  6. `#space-member-write-select` (Space-Verwaltung, lesen/schreiben — hardcodiertes `<option value="">lesen</option>` + `<option value="write">schreiben</option>`)
  7. Per-Item-Share-Row (`dialogs.js :: openShareDialog()` ab Z. 421, dynamisch erzeugte
     `<select class="input">` für jeden bekannten Space — read / write / leer)
- **CSS:** `select.input { appearance: none; padding-right: 28px; background-image:
  url("data:image/svg+xml;…chevron-down…"); accent-color: var(--accent); }` plus
  `:disabled`-Variante in `--text-placeholder`. **Kein** Custom-Chevron via SVG-`<use>`-
  Konstrukt nötig — die Data-URL ist 0,5 KB statt eines zweiten Sprite-Eintrags und bleibt
  portabel (funktioniert auch dann, wenn das Lucide-Sprite noch nicht geladen ist).
- **JS:** `appendChild(option)` mit `.textContent` und `.value`. Die zwei `<option>`-
  Defaults (`lesen`/`schreiben`) im hardcodierten Select dürfen im HTML bleiben, weil sie
  *die* Funktionskonstante sind — kein API-Aufruf nötig.
- **Native Vorteile (Begründung für den Vorbild-Charakter):** Pfeiltasten-Navigation,
  Bild-Auf/Ab, Erstbuchstaben-Sprung, Screenreader-Verhalten, Mobile-Sheet-Darstellung
  — alle automatisch korrekt; der Phase-7-Lila-Fund vom 2026-08-16 (Browser-Akzentton
  statt App-Blau in nativer Optionsliste) wurde durch `accent-color: var(--accent)`
  strukturell geschlossen.

### Was diese Konvention NICHT macht

- **[2026-09-02 Korrektur]** Der Absatz unten stand hier als Momentaufnahme der Sitzung vom
  2026-09-01/-02 und ist überholt: der Nikinger hat die dort verworfene Vereinheitlichung am
  2026-09-02 explizit angeordnet (Vormerkung 3 Punkt 1, Richtung (a), „i like the rail Button
  Style more, Looks cleaner") und sie ist seither gebaut (`app.css`, Session-Block unten). Der
  ursprüngliche Kategorien-Einwand (Listenzeilen-Auswahl = eigene Kategorie, keine Vermischung
  mit Navigation) ist damit per direkter Nikinger-Weisung überstimmt, nicht als falsch
  widerlegt — bewusst als Ausnahme dokumentiert, keine neue Kategorisierungsregel. Die
  **Farbsprache** (Rail-Button-Gradient) ist jetzt identisch, die **Markup-Kategorien** selbst
  (Choice/Toggle/Status/Navigation, Tabelle oben) bleiben unverändert — eine Listenzeile ist
  weiterhin keine Navigation, sie sieht nur jetzt optisch genauso aus wie eine. Ursprünglicher
  Text, unverändert stehen gelassen als Herkunftsnachweis der verworfenen Position:
  *„Sie ändert nichts am Listenzeilen-Sheen aus C4 (3-px-Akzentkante + 1-px-Outline +
  Backdrop-Blur-Sheen) — Vormerkung 2 vom 2026-09-02 (Sichtprüfung 3) hatte drei mögliche
  Richtungen benannt; diese Sitzung hat keine davon umgesetzt, weil der Sheen durch N8
  begründet ist (Auswahl darf nicht allein von Transparenz abhängen, sonst bei
  prefers-reduced-transparency: reduce unsichtbar). Eine Vereinheitlichung mit dem
  Rail-Button-Akzent-Gradient-Fill (Navigation-Kategorie) wäre aus Sicht des Servers eine
  Vermischung zweier Kategorien — semantisch falsch."* N8 selbst ist weiterhin erfüllt, siehe
  die Vormerkung-3-Punkt-1-ERLEDIGT-Notiz oben — der neue Fill ist opak, hängt an keinem Blur.
- Sie passt **nicht** den Counter-Chip-Stil auf der Übersichtsseite an den `<select>`-
  Chevron-Stil an — Counter-Chips sind Navigation, kein Choice, andere Kategorie.

### Wo sie ansetzt, wenn etwas Neues kommt

- **Brauche ich einen Wert aus N?** → `<select class="input">` mit `appendChild(option)`.
  Vorbild: sieben existierende Stellen. **Niemals** eigene Dropdowns / Popovers / `<div
  role="listbox">` ohne triftigen Grund.
- **Ist es an/aus?** → Button mit `aria-pressed` oder `<input type="checkbox">` mit
  explizitem `<label>`. Native Tastatur- und Screenreader-Verhalten eingebaut.
- **Zeige ich nur einen Zustand an?** → `.visibility-chip` / `.list__row-meta` / Pill —
  niemals als Auswahl verkleidet.
- **Springe ich woanders hin?** → Button mit `aria-current` (Navigation aktiv) oder
  semantischer Link.

### Größe dieser Konvention

Reine Doku, kein Code über die Chevron-Data-URL hinaus. Der Konventionstext selbst ist
bewusst knapp gehalten — Tabellenform, ein Markup-Beispiel, keine ausschweifenden
Begründungen pro Choice-Stelle. Sie landet hier im Phase-Head, nicht im Plan, weil sie
eine **Arbeits-Konvention** für die laufende Phase ist; bei Step Z wird sie in die
allgemeine Doku-Layer-Konvention (`docs/DOC_LAYERS_CONVENTION.md`) überführt oder als
P9-Arbeitsanweisung weitergeführt, falls die Nikinger-Entscheidung anders ausfällt.

---

## Session stopped — 2026-09-08 (Z-Closeout: Sichtprüfungs-Automatisierung, Statusregel geändert, Phase 8 formal ✅)

**Auftrag:** die verbliebenen Phase-8/8.5-Sichtprüfungspunkte automatisiert durchführen
(Canvas-Instrumentierung + CDP-Medien-Emulation gegen Wegwerf-Instanzen, echter OAuth+MCP-Dance
für Zweitnutzer-ACL, danach echte Produktions-Checks über den reconnecteten sharefyx-MCP-
Connector), dann vier Nikinger-Entscheidungen umsetzen: Statusregel ändern, Radiogruppe-Rückbau
vormerken, Wegwerf-Instanzen abbauen, Versionierungsplan für die Folgephasen festlegen.

**Neue Skripte:** `p8_21d_tag_cutoff_probe.py` (Canvas-Prototype-Patch zählt Tag-Kanten exakt,
Frame-Teiler-Trick über explizite Kanten als Divisor — genau 10.0 Tag-Kanten/Frame, `spitze`
C(5,2)=10 durchgelassen, `last-200` + 12× `gruppe-NN` korrekt ausgeschlossen);
`p8519_radiogroup_probe.py` (Radiogruppe gegen 200-Knoten-Wegwerf: 2 Radios, kein `<select>`
mehr, `localStorage`-Persistenz — 5/5); `wegwerf_setup_p8_8.py` (erstes Wegwerf-Setup mit ZWEI
unabhängigen Principals, `testuser1`+`testuser2`, statt einem wie bei jedem Vorgänger) +
`p8_8_zweitnutzer_probe.py` (echter OAuth-Dance ohne Browser für beide Principals, dann fünf
echte MCP-Tool-Aufrufe: privates Item nicht in fremder Suche sichtbar, geteiltes Item schon,
`get_item` auf privates Item abgelehnt, `update_item` auf geteiltes [nur `share_read`] Item mit
`write_denied` abgelehnt — 5/5). Echter Fund dabei: `update_item` lehnt `share_read`/
`share_write` kategorisch ab („das geht nur ein Mensch in der UI", `tools.py`) — kein Bug,
dokumentierte Restriktion; Sharing im Wegwerf-Setup daher per direktem
`storage.store.Store.update()` gesetzt, nicht über MCP.

**Nach Reconnect des sharefyx-MCP-Connectors** (Nikinger-Aktion): `list_spaces` gegen die echte
Produktion (vier reale Spaces), zwei `search_items`-Aufrufe, alle vier geforderten Textformen
(Fließtext/Tabelle/Klammer/Aufzählung) live erzeugt, kein `itm_…`-Leck gefunden. Nikinger
lieferte zusätzlich unabhängig einen Screenshot eines echten claude.ai-Chats über denselben
Connector mit derselben Antwortform — zwei unabhängige Live-Belege für dieselbe Zeile.

**Vier Nikinger-Entscheidungen, alle umgesetzt:**
1. **Statusregel geändert:** eine vom Nikinger geprüfte Wegwerf-Automatisierung zählt ab sofort
   als `✅ = live-verifiziert`, nicht mehr nur eine eigenhändige Live-Probe. Begründung wörtlich:
   „the throwaway is, except for files and user, byte by byte identical to the new prod after
   deploy." Volle Herleitung + wiederverwendbare Techniken (Canvas-Instrumentierung, OAuth ohne
   Browser, Zwei-Principal-Wegwerf): neue Datei `docs/concepts/
   sichtpruefung_automation_conventions.md` (samt Schwester-Datei
   `sichtpruefung_automation_tooling.md` für Plugin-Empfehlungen, inkl. Korrektur der
   OpenCode/MiniMax-M3-Bildfrage — das Modell ist nativ multimodal, die Lücke liegt in
   OpenCodes Attachment-Pipeline).
2. **Radiogruppe-Rückbau auf `<select>`** (inline-Beschreibung, Design-Konsistenz) — nur
   vormerkt in `phase8_5_picker_release/CLAUDE.md`, kein Code angefasst.
3. **Housekeeping:** alle drei Wegwerf-Instanzen (200-Knoten, D2, das neue Zwei-Principal-
   Setup) per PID-Datei abgebaut, kein `pkill -f`.
4. **Versionierungsplan:** P8.6 (Arbeitsname) → `v3.0.2`, P9 (Arbeitsname) → `v3.1.0` —
   Größenklassen-Regel jetzt explizit. OpenCode-Vision-Plugin als früher Punkt in P8.6.

**Matrix-Update (dieser Head):** §Abnahmestand-Statusregel ersetzt (siehe oben), sechs Zeilen
gehoben (P8-5, P8-8, P8-16, P8-21, P8-22, P8-24), Bilanz-Abschnitt neu geschrieben —
**26 ✅ · 0 🟡 · 0 ⬜, maschinell gezählt.** Phase 8 ist damit formal ✅. Zwei benannte
Restdefekte (Item-Link-Picker-Body-Lücke, Picker-A11y `aria-selected`) vererbt an P8.6, wie
seinerzeit P7-24/P7-4 an Phase 8 vererbt wurden.

**Weitere Doku-Updates im selben Zyklus (Hard Rule 8):** `phase8_5_picker_release/CLAUDE.md`
(Abnahmestand + eigener Session-Block); `ROADMAP.md` (Phasentabelle P8/P8.5 ✅, alte
P8.X-Platzhalterzeile in P8.6+P9 aufgeteilt); `docs/INDEX.md` (Phase-8/8.5-Header, neue
P8.6+P9-Sektion); Wurzel-`CLAUDE.md` Current-state (ein konsolidierter Closeout-Absatz); zwei
Memory-Dateien (`project_phase_status` komplett neu geschrieben — war 5 Tage stale und faktisch
falsch zum v3-Deploy-Stand; `feedback_throwaway_evidence_counts_as_live` neu). Dieser
Session-Block rotiert den stale gewordenen 2026-09-02-Block (Fixes A/B/C) nach
`SESSIONS_ARCHIVE.md`, Rotationsregel eingehalten (genau ein Block im Head).

**Bewusst nicht gemacht, benannt statt verschwiegen:** die Doc-Hygiene-Kompression selbst
(weitere Rotation über die eine hier hinaus, Trimmen von `docs/INDEX.md`s `updated:`-Pipe) —
alle vier berührten Phase-Heads liegen weiterhin deutlich über dem 40-KB-Softcap. Diese Sitzung
war der angekündigte „Z"-Closeout, hat aber die Kompression selbst nicht angefasst — als
offener Punkt in der `project_phase_status`-Memory vermerkt, kein stiller Verzicht.

**Verifiziert:** kein Python-/JS-Code außerhalb der vier neuen `phase8_ui_graph/scripts/`-
Dateien angefasst, keine Änderung an `webui/`/`mcpserver/`/`storage/` — Tabu-Diff §0.3
irrelevant. Production (`PID 355956`) vor und nach der gesamten Sitzung identisch, kein
`systemctl`-Verb ausgeführt. Drei Wegwerf-Ports (18772/18768/18780) nach Sitzungsende
geschlossen, mit `ss -ltnp` gegengeprüft.

**Commit:** ein Commit für diesen gesamten Closeout (Skripte + Screenshots + alle Doku-Updates
+ Memory) — Nikinger-Aufforderung „correctly end this session". Kein Push ohne weitere
Anweisung.

**Nächster Schritt:** P8.6/P9 sind Arbeitsnamen, keine geplanten Phasen — eine
Planungs-Session (gelockte Entscheidungen, Step 0) steht vor dem ersten Code-Commit in beiden.
Reihenfolge: P8.6 zuerst (inkl. OpenCode-Vision-Plugin früh), P9 danach.
