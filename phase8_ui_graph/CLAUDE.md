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
updated: 2026-10-25 (P10.5 Block 12: Abschnitt C0 verbatim nach SESSIONS_ARCHIVE.md — 47.861 → 34.225 B) | 2026-09-08 (Z-Final II: §7-Abnahmematrix P8-1 bis P8-26 [alle 26 Zeilen mit Beleg] + Sichtprüfungs-Status-Tabelle nach SESSIONS_ARCHIVE rotiert; Head von 77 KB auf 64 KB reduziert — Rest ist kanonischer Mission/Scope/Modul-Status/Abnahmestand-Intro/C0/Vormerkungen-Pointer/Selection-Choice-Konvention/Session-Block; Frontmatter vorne ergänzt) | 2026-09-08 (Z-Final: Vormerkungen-Sektion (4 Items, 3 erledigt + 1 nach P9) in den SESSIONS_ARCHIVE rotiert; Head von 92 KB auf 77 KB reduziert; Frontmatter vorne ergänzt) | 2026-09-08 (Z-Closeout: Sichtprüfungs-Automatisierung gegen Wegwerf + echte Produktion, Statusregel geändert (Nikinger-geprüfte Wegwerf-Automatisierung zählt als live-verifiziert), Bilanz 26 ✅ · 0 🟡 · 0 ⬜ -- Phase 8 formal abgeschlossen; P8.6 (→v3.0.2) + P9 (→v3.1.0) als Folgephasen vorgemerkt; stale 2026-09-02-Block rotiert nach SESSIONS_ARCHIVE.md) | 2026-09-07 (Cluster-2-Sichtprüfung 2 + 3 am echten Gerät — erste echte Live-Verifikations-Welle seit D3; Nikinger gegen v3.0.1 bestätigt: P8-14, P8-15, P8-18, P8-19, P8-23 ✅; P8-5, P8-8, P8-16, P8-20/21, P8-22, P8-24 bleiben 🟡 für Cluster 3/5 + Phase-8-§7-Statusregel; Screenshot `phase8_5_picker_release/screenshots/Bildschirmfoto 2026-09-07 um 17.08.37.png` zeigt tabellose Space-Zeilen + Zähler-Chips + VERKNÜPFUNGEN-Graph (eigen blau + geteilt türkis + fremd grau dank Fix B vom 2026-09-02) + ZULETZT-BENUTZT-Sektion + Badge `SHAREFYX v3.0.1`; P8.5-18 jetzt ✅ als Umbrella; Phase-8-Bilanz 14/12/0 → 19/7/0, Phase-8.5-Bilanz 4/13/3 → 5/12/3; Phase-8-Glyph-Entscheidung noch offen, Vorschlag vorerst 🟡 bis Cluster 3/5; P8-16-Werfer-Eidenz aus Cluster-1 ergänzt die Phase-8-§7-Zeile, Status bleibt 🟡 weil §7-Statusregel „✅ = live-verifiziert" gilt; Phase-Head 94.3 KB, Phase 8 geschlossen, exempt) | ältere Einträge: phase8_ui_graph/SESSIONS_ARCHIVE.md
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
> **Verbatim verschoben** nach `SESSIONS_ARCHIVE.md` (`scripts/move_sections.py`) — dort unter derselben Überschrift.

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

**[2026-10-02, B17 — was „Standard-Knopfplastik" heute heißt, und eine gemessene Korrektur an der
Umsetzung.** Die Zeile oben stand aus dem Jahr 2026-09-10, als „Standard-Knopfplastik" die graue
`--btn-face-*`-Fläche meinte. Seit dem 2026-10-01 trägt `.btn` die **Rail-Optik**
(`--btn-std-fill`/`--btn-std-line`, deckende Werte). Der Wortlaut der Konvention gilt unverändert —
**und er war zwischenzeitlich nicht eingehalten:** `#archive-button` behielt als *einziger* Knopf
die alte graue Fläche, und die ist `#2A313A`, also **heller** als die Standardfläche `#0C1C31`.
Gemessen heißt das: „Vorsicht" war der auffälligste Knopf der Editor-Fußzeile statt des Standards —
das Gegenteil dessen, was diese Zeile verlangt. `.btn.action--caution` trägt seit dem 2026-10-02
**exakt** die Standardfläche, und die Unterscheidung sitzt allein in der Beschriftung.

**Von den beiden Trägern hat ohnehin nur einer eine Fläche:** `#logout-button` ist ein
`.rail__action` (`background: none`, Rail-Knopf) und trägt die Vorsicht nur an der Farbe; nur
`#archive-button` ist ein `.btn` und erbt damit die Fläche. Wer hier künftig „die beiden
Vorsicht-Knöpfe" liest, muss das nicht verwechseln.

**Was ausdrücklich *nicht* gebaut wurde:** eine eigene, rot getönte Flächenfamilie
(`--caution-std-*`). Sie *wäre* die „gefüllte rote Fläche", die diese Zeile ausschließt — sie war
der erste Kandidat und wurde vom Nikinger am 2026-10-02 nach dem Vorlegen des Konflikt-Zitats
verworfen. Das ist der Grund, warum die Linie „**keine** gefüllte rote Fläche" hier steht und nicht
weichen muss.

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

- **[2026-10-01 Ergänzung, P9, Nikinger-Entscheidung]** Die Rail-Optik gilt jetzt für **alle
  Standardknöpfe**: `.btn` trägt das Bild von `#home-button[aria-current]` auf der Rail, als
  **deckende** Tokens `--btn-std-fill`/`--btn-std-line` (die halbtransparenten `--select-*` wirken
  auf grauem Grund blauer); Navigationsknöpfe tragen `.btn` selbst, `.account-nav` ist nur Layout.
  Ausnahmen: `.btn-primary`
  (Hauptaktion) und `.action--caution` (Vorsicht, z. B. Archivieren — behält die graue Plastik).
  Ersetzt H-R.2 (Akzentkante an `.account-nav`).

  **[2026-10-02, B17, Nikinger-Entscheidung — der Satz „behält die graue Plastik" ist hiermit
  überholt und darf nicht mehr als Ist-Stand gelesen werden.]** Er beschrieb den Zustand zwischen
  dem 2026-10-01 und dem 2026-10-02; heute trägt `.btn.action--caution` **exakt** die
  Standardfläche, und der alte `--btn-face-*`-Satz hängt nur noch am Badge `.rail__glyph`
  (dort ausdrücklich gewollt, siehe `test_rail_glyph_is_a_badge_and_keeps_the_plastic`).
  Grund, gemessen statt geschmeckt: die graue Fläche ist heller als die Standardfläche, „Vorsicht"
  war damit der auffälligste Knopf der Fußzeile statt des Standards. Die **Kategorie** bleibt
  sichtbar, nur an der Beschriftung (`--caution`) statt an der Fläche — das ist die Zeile der
  Kategorientabelle oben, wortgleich. `.btn-primary` (Hauptaktion) bleibt wie gehabt die einzige
  Fläche-Ausnahme.

- **[2026-10-01, zweite Runde desselben Tages, P9, Nikinger-Entscheidung] `.toolbar-btn` ist
  mitgezogen** — die zehn Formatierhilfen + der Vorschau-Umschalter waren der **letzte** echte
  Knopf auf der alten grauen Plastik (`--btn-face-*`), nachdem `.btn` am Vortag umgestellt worden
  war; zwei Knopfoptiken in einem Panel sind genau der Befund, den die erste Runde an
  `.account-nav` gestellt hatte. **Maße und Typografie bleiben** (24 px Höhe, Monospace,
  `--text-muted`): die Formatierleiste ist eine Werkzeugleiste, keine Dialogleiste — sie
  unterscheidet sich in der Größe, nicht in der Sorte. Vier Punkte, die beim Nachziehen zu
  entscheiden waren und die als Regeln bleiben:
  1. **`:disabled` bleibt auf `--surface`, nicht auf `--btn-std-fill`.** Die Hilfen sind in der
     Vorschau abgeschaltet (`editor.js :: setEditorMode`); ein deaktivierter Standardknopf muss
     „inaktiv lesbar" heißen, nicht „Standardknopf in einem anderen Zustand".
  2. **Der äußere Schlagschatten fällt weg** (`0 1px 2px rgba(0,0,0,.45)`), weil `.btn` ihn auch
     nicht trägt — sonst wäre jeder Pixelvergleich mit `#home-button` genau an der Unterkante
     daneben.
  3. **`.rail__glyph` (der 20×20-Buchstaben-Badge am Space) bleibt auf `--btn-face-*`** — ein Badge
     ist kein Knopf: er hat keine Aktion, und die drei Kategorie-Varianten daneben tragen ohnehin
     eigene Hex-Werte (Phase 8 C3).
  4. **`.pw-toggle` (die kleinen „Anzeigen"-Knöpfe) waren nie eine offene Frage** — sie tragen
     `.btn` und sind mitgezogen worden; sie überschreiben nur `padding`/`font-size`.

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
