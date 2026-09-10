---
status: live
purpose: Phasenplan des Space-Servers — was in welcher Reihenfolge gebaut wird und warum, plus Status je Phase
read-when: Phasenwechsel, Scope-Frage („gehört X in diese Phase?"), Planung einer neuen Session
detail: L2
up: CLAUDE.md
down:
  - docs/concepts/phase1_storage_plan.md   # ausführungsreifer P1-Plan
  - docs/concepts/phase2_mcp_plan.md       # ausführungsreifer P2-Plan
  - docs/concepts/phase3_edge_plan.md      # ausführungsreifer P3-Plan
  - docs/concepts/phase4_auth_plan.md      # ausführungsreifer P4-Plan
  - docs/concepts/phase5_ui_plan.md        # ausführungsreifer P5-Plan
  - docs/concepts/phase6_shares_plan.md    # ausführungsreifer P6-Plan
  - docs/concepts/phase6_5_tools_images_plan.md   # ausführungsreifer P6.5-Plan
  - docs/concepts/phase7_spaces_admin_plan.md     # ausführungsreifer P7-Plan
  - docs/concepts/phase8_ui_graph_plan.md         # ausführungsreifer P8-Plan
updated: 2026-09-09 (Phase-8.5-Z-Closeout — Phase 8.5 mit Step Z **vollständig abgeschlossen**; Übersichtsgrafik + `PHASE8_5_CLOSEOUT_HANDOVER.md` neu (Umkehr der Locks P8.5-S/P8.5-R durch den Nikinger, im Plan §0.2 datiert), Plan §9 gefüllt; im Phase-8.5-Abschnitt die stale „v3.0 ist nicht ausgeliefert"-Korrektur durchgestrichen (der Deploy lief am 2026-09-05) und P8.5-S aus DRAUSSEN gestrichen; im Phase-8.X-Abschnitt die stale Notiz-Zahlen „16 Themen / 25 KB" auf **zehn Abschnitte / 40.9 KB** korrigiert, Schritt 1 als erledigt markiert, **Mobile-Hälfte der Außenkante aufgehoben** (Realtime bleibt draußen), Nummern-Frage „p8.7 vs. P9" als offen notiert) | ältere Einträge: die jeweiligen Phase-Header und `docs/PROJECT_SESSION_LOG.md`
---
# ROADMAP — Space-Server

**Build-Reihenfolge ist verbindlich.** Unter Zeit- oder Token-Druck fällt immer die *späteste*
Phase weg, nie eine frühere Regel. Insbesondere: die UI fällt weg, die Auth-Härtung nicht.

Statusglyphen: ⬜ nicht gestartet · 🔄 aktiv · 🟡 code-complete, nicht live-bewiesen · ✅ live-verifiziert

| Phase | Verzeichnis / Paket | Inhalt | Status |
|---|---|---|---|
| **P1** | `phase1_storage/` · `storage` | Datei-Store + Index + Versionierung. Kein Netz. | ✅ |
| **P2** | `phase2_mcp/` · `mcpserver` | MCP-Server, Token-Auth, 6 Tools. Lokal erreichbar. | ✅ |
| **P3** | `phase3_edge/` | Tunnel, systemd, Health, Logging, Ops-Skripte. Öffentlich erreichbar. | ✅ |
| **P4** | `phase4_auth/` · `authserver` | OAuth 2.1 + DCR; ersetzt den Pfad-Token. | ✅ |
| **P5** | `phase5_ui/` · `webui` | REST-API + Web-UI für Menschen. | ✅ |
| **P6** | `phase6_shares/` (kein eigenes Paket) | Freigaben, Ordner, `patch_item`, Update-Log, Bilder. | 🟡 |
| **P6.5** | `phase6_5_tools_images/` (kein eigenes Paket) | Werkzeug-Ergonomie, Abschluss Bilder. | 🟡 |
| **P7** | `phase7_spaces_admin/` (kein eigenes Paket) | Space-Verwaltung, Mehrfachauswahl, Konsolidierung. | ✅ |
| **P8** | `phase8_ui_graph/` (kein eigenes Paket) | UI-Neuanstrich v3, Verknüpfungs-Graph, P7-Erbposten. | ✅ |
| **P8.5** | `phase8_5_picker_release/` (kein eigenes Paket) | Link-Picker-Politur, v3-Vorabritt + Deploy; schließt Phase 8 ab. | ✅ |
| **P8.6** | `phase8_6_ui_polish/` | **Geplant 2026-09-09**, Plan: `docs/concepts/phase8_6_ui_polish_plan.md`. Reichweite „Selektions-Welle + Layout" — Layering-Tokens, eine Selektionssprache für alles Klickbare, „Konto"→„Einstellungen", Ordner-Zähler, Rail-/Übersichts-Reorg, klickbare Spaces, drei Graph-Fixes (V102/§2.3/§2.4), Radiogruppe-Rückbau auf `<select>`; **erster Punkt: OpenCode-Vision-Plugin**. Deploy-Ziel `v3.0.2`. | 🔄 |
| **P9** | (nicht angelegt, Arbeitsname) | Obsidian-Map-/Graph-Umbau (`p8x_ui_polish_notes.md` §2) + verbundene AI-Sessions (§10.8). **Vorgemerkt 2026-09-10: „Ordner umbenennen"** — in P8.6 geprüft und bewusst vertagt, volle Analyse in `phase8_6_ui_polish_plan.md` §0.4.1 (die billige Frontend-Fassung lässt die `.share.yml` eines geteilten Ordners still zurück; der saubere Weg ist die **neunte P1-Contract-Öffnung**). Deploy-Ziel `v3.1.0`, laut Nikinger voraussichtlich letzter großer UI-Umbau. | ⬜ |

**[2026-09-08 Korrektur, Z-Closeout]:** P8 + P8.5 auf ✅ (Statusregel geändert — vom Nikinger
geprüfte Wegwerf-Automatisierung zählt jetzt als live-verifiziert, siehe `phase8_ui_graph/
CLAUDE.md` §Abnahmestand). Die bisherige **P8.X-Platzhalterzeile ist aufgeteilt** in **P8.6**
(kleine Politur, Patch-Bump `v3.0.2`) und **P9** (Graph-Umbau, Minor-Bump `v3.1.0`) — beide
Arbeitsnamen, noch nicht geplant/gelockt. `docs/concepts/p8x_ui_polish_notes.md` bleibt die
Sammel-Quelle für beide, bis eine Planungs-Session die Aufteilung offiziell zieht.

**[2026-09-06 Korrektur, Phase 8.5 D4-Sichtprobe-Folgesession]:** P8.5 fehlte als eigene
Tabellenzeile — beim Anlegen der P8.X-Zeile mitgefunden und nachgetragen, **keine**
inhaltliche Änderung. (P8.X selbst ist mit dem 2026-09-08-Eintrag oben in P8.6/P9
aufgeteilt worden.)

**[2026-08-23 Korrektur, P7 Step 0]:** P6.5 fehlte als eigene Tabellenzeile — beim Ergänzen der
P7-Zeile mitgefunden und nachgetragen, keine inhaltliche Änderung.

**Korrektur (2026-07-25, P2-Planungssession):** OAuth rückt von „ganz am Ende" auf „direkt nach
P3" — der Pfad-Token soll kurz leben, und die UI ist die Phase, die laut Build-Reihenfolge unter
Druck wegfallen darf, OAuth nicht. Begründung: `docs/concepts/phase2_mcp_plan.md` §0.3.

---

## Phase 1 — Storage-Kern
Status **✅** (2026-07-25): 8 Module + 68 Tests, `space_cli.py` als Beweis. Nikinger-Lauf gegen echten `DATA_ROOT` (`/home/savefyx/savefyx-data`) selbst ausgeführt. Details: `phase1_storage/CLAUDE.md` · Plan: `docs/concepts/phase1_storage_plan.md` · Handover: `docs/concepts/PHASE1_CLOSEOUT_HANDOVER.md`.

## Phase 2 — MCP-Server
Status **✅** (2026-07-26): 8 Module + 133 Tests (76 P1 + 57 P2), `mcp_smoke.py` als Beweis, **Adapter-Abnahme 21/21 gegen den echten Custom Connector** durch den Nikinger (`docs/concepts/P2_ADAPTER_ABNAHME_2026-07-26.md`). Details: `phase2_mcp/CLAUDE.md` · Plan: `docs/concepts/phase2_mcp_plan.md` · Handover: `docs/concepts/PHASE2_CLOSEOUT_HANDOVER.md`.

## Phase 3 — Exposure & Betrieb
Status **✅** (2026-07-27–2026-08-02): 13/13 live bestanden, **Tailscale Funnel** (ersetzt den ursprünglich geplanten Cloudflare-Tunnel, Korrektur 2026-07-28; **CGNAT-konform**, Hard Rule 6 eingehalten). Runbooks (`diagnose.sh` etc.) in `phase3_edge/CLAUDE.md`. Details: `phase3_edge/CLAUDE.md` · Plan: `docs/concepts/phase3_edge_plan.md` · Handover: `docs/concepts/PHASE3_CLOSEOUT_HANDOVER.md`.

## Phase 4 — OAuth 2.1
Status **✅** (2026-07-30): 16/16 live bestanden — Schnitt vollzogen, **Pfad-Token tot**, Argon2id + TOTP + DCR + PKCE, opake rotierende Token, zwei unabhängige Nutzer. Sicherheits-Review in `docs/concepts/P4_SECURITY_REVIEW_2026-07-29.md`. Details: `phase4_auth/CLAUDE.md` · Plan: `docs/concepts/phase4_auth_plan.md` · Handover: `docs/concepts/PHASE4_CLOSEOUT_HANDOVER.md`.

## Phase 5 — Web-UI
Status **✅** (2026-08-09): 20/20 live bestanden. Zwei Blöcke (A Sicherheit/Auth-Selbstverwaltung, B REST-API/UI) mit hartem Gate. **`git diff` auf `storage/`, `mcpserver/{tools,permissions,server}.py` blieb über die gesamte Phase leer** (Kriterium 18 — derselbe Seam-Beweis wie in P4, eine API-Fläche höher). Details: `phase5_ui/CLAUDE.md` · Handover: `docs/concepts/PHASE5_CLOSEOUT_HANDOVER.md`.

## Phase 6 — Freigaben, Ordner, Werkzeug-Ergonomie
Status **🟡** (2026-08-23, bewusst nicht ✅): Code-complete und live deployt, aber nur 12/39 Abnahmezeilen live-verifiziert (drei benannte Tasks für nächste Phase in `PHASE6_CLOSEOUT_HANDOVER.md` §4). Drei Blöcke (A Werkzeuge/Betrieb/Update-Banner, B Dateisystem mit SharePolicy, C Bilder nach 6.5 ausgewandert). Details: `phase6_shares/CLAUDE.md` · Handover: `docs/concepts/PHASE6_CLOSEOUT_HANDOVER.md`.

## Phase 6.5 — Werkzeug-Ergonomie und Bilder
Status **🟡** code-complete (13/14 live, P6.5-14 strukturell offen — Nikinger-Bewertung): fünf offene MCP-Werkzeug-Ergonomie-Punkte geschlossen + Abschluss Block C Bilder (`put_asset`/`get_item_asset`/`<untrusted_content>`). Drei neue Punkte nach Phase 6.5 in `PHASE6_5_CLOSEOUT_HANDOVER.md` benannt. Details: `phase6_5_tools_images/CLAUDE.md` · Handover: `docs/concepts/PHASE6_5_CLOSEOUT_HANDOVER.md`.

## Phase 7 — Space-Verwaltung, Mehrfachauswahl, Konsolidierung
Status **✅** (2026-08-28): 22/24 Abnahmezeilen live, 2 ❌ als benannte Defekte an Phase 8 vererbt (P7-24 TOTP-Replay im Batch, P7-4 Claude-nennt-IDs-statt-Titeln) — die Matrix ist **vollständig durchgelaufen**, das unterscheidet P7 von P6/P6.5. Live: `e88a624`, Health-Gate 3/3 grün. Drei Erbposten aus dem Live-Betrieb (P7-24, P7-4, `remove-space`-Auto-Reindex) in Phase 8 gebaut. Details: `phase7_spaces_admin/CLAUDE.md` · Handover: `docs/concepts/PHASE7_CLOSEOUT_HANDOVER.md`.

## Phase 8 — UI-Neuanstrich, Verknüpfungs-Graph, QoL

**Mission, drei Stränge:** (A) die drei benannten P7-Erbposten sind behoben bzw. entschieden —
ein Batch-Verschieben braucht eine einzige Passwort+TOTP-Eingabe (Reauth-Grant statt
TOTP-Replay), `remove-space` hinterlässt nie wieder einen stalen Index, P7-4 bekommt seine
Zweitprobe. (B/D) ein Mensch sieht in einem Graphen, welche Items wie verknüpft sind
(`links:`-Feld + `itm_`-Body-Referenzen + zuschaltbare Tag-/Ordner-Kanten), und die Übersicht
zeigt tablos, was tatsächlich gebraucht wird. (C) die UI verliert ihren AI-Template-Look:
Lucide-Icons statt HTML-Entities, IBM Plex 16px statt Inter 15px, Farblegende
own/shared/foreign, Liquid-Glass-Akzente mit Pflicht-Fallback — Version v3.0.

- **DRIN:** Reauth-Grant (`POST /api/v1/reauth`), `remove-space`-Auto-Reindex, P7-4-Zweitprobe
  + Textschärfung, achte P1-Contract-Öffnung (`linkscan.py`, `item_links`, `GET /api/v1/graph`),
  `#item/`-Navigation, Link-Picker, Icon-Sprite, Plex-Fonts, Farbsemantik, Glass-Akzente,
  tablose Übersicht, handgerollter Canvas-Graph, v3.0.
- **DRAUSSEN:** FastMCP-4/V79, Body-Volltextsuche UI, Rechteverwaltung über MCP, neues
  MCP-Graph-Tool, Löschen von Items, `_trash/`-Räumung, Funnel-Watchdog, Light-Mode,
  Glyph-Entscheidungen P6/P6.5.
- **Erstmals: Claude Code plant, opencode/M3 führt aus — ohne Advisor-Stufe in der Ausführung**
  (Nikinger-Entscheidung N12; Ersatzmechanismen im Plan §0.6).

**Status 🔄 (2026-09-01, Block A + B ✅ live-verifiziert, Gate B→C bestanden):**
Plan `docs/concepts/phase8_ui_graph_plan.md` ausführungsreif, alle zwölf Nikinger-Fragen
N1–N12 in §0.1 gelockt, Entscheidungen P8-A–P8-Q, Abnahmezeilen P8-1–P8-24, `[VERIFY]`
  V81–V92. Closeout wird §9 des Plans (P8-N: ein Dokument pro Phase, kein separates
  Handover). **Block A (A1 Reauth-Grant, A2 `remove-space`-Auto-Reindex, A3
  P7-4-Zweitprobe 🟡 mit benanntem Restdefekt Klammer/Aufzählung) + Block B
  (`storage/linkscan.py`, `item_links`-Tabelle, `GET /api/v1/graph`, `#item/`-
  Navigation, Link-Picker-Dialog) sind seit `main@007b73d` live, Release
  `20260901T103944.634877Z`. Gate B→C (2026-09-01) grün: 958/958 pytest, Charakterisierung
  byte-identisch, Tabu-Diff leer, `_graph_get` manuell 12/12, Playwright gegen
  Wegwerf 18/18. Nächster Schritt: Block C — Design-Fundament v3 (Plan §4).**

---

## Phase 8.5 — Link-Picker-Politur und v3-Release

**Mission:** drei 🟡-Restdefekte aus Phase-8-Closeout §9.4.1–§9.4.3 schließen, einen vollständigen
v3-Vorabritt über den nie ausgelieferten v3-Build fahren und ihn live deployen — diese Phase
**schließt Phase 8 formal mit ab** (N6, Präzedenz P7 Step A8 für Phase 6.5). ~~**Wichtige Korrektur zum Live-Stand:** v3.0 ist **nicht** ausgeliefert …~~
**[2026-09-05 erledigt]:** der Vorabritt lief 26/26, der Deploy ging durch — live seit
`main@6f19a8f`, Release `20260905T140325.378914Z`, Badge `v3.0.1`, Service-PID 355956.
Der Grund für den vollen 13-Stationen-Ritt (N5) bleibt der richtige: Block C/D waren ein
UI-Umbau, den nie ein echter Nutzer gesehen hatte.

- **DRIN:** Picker-Modus-Umschalter „Text-Link / Kante" mit `localStorage`-Persistenz
  (P8.5-§2 A1); Tastaturnavigation über `aria-activedescendant`-Muster (P8.5-§2 A2); Hint
  `_TITLE_NOT_ID_HINT` generalisierend geschärft mit verbindlicher Abbruchregel (P8.5-§3 B1);
  v3-Vorabritt gegen Wegwerf-Instanz mit 13 Stationen (P8.5-§4 C); Deploy `v3.0` → `v3.0.1`
  als **Nikinger-Aktion** (P8.5-§5 D2, Hard Rule 9); Phase-8-Closeout-Nachtrag
  (`phase8_ui_graph_plan.md` §9).
- **DRAUSSEN:** Phase-8-§9.4.6-Funde (Settle-Zeit / Foreign-Farbe / Knotenklick — bereits am
  2026-09-02 geschlossen), Phase-8-§9.4.7 Glyph-Entscheidung ✅/🟡 (Nikinger-Sache nach
  Live-Deploy + Sichtprüfung), geerbtes Phase-6/6.5/7-Ledger (`phase8_ui_graph_plan.md` §9.4.5),
  FastMCP-4/V79 (eigene Mini-Phase, P5-C), `_trash/`-Räumung, Funnel-Watchdog, Mobile/Realtime,
  Light-Mode, ~~Phase-8.5-Übersichtsgrafik (P8.5-S)~~ **[2026-09-09 aufgehoben, Nikinger]:**
  die Grafik existiert — `docs/concepts/phase8_5_picker_release_uebersicht.svg`, Korrekturnotiz
  im Plan §0.2.

**Plan:** `docs/concepts/phase8_5_picker_release_plan.md` (744 Zeilen, geschrieben 2026-09-03
gegen `main@6272cad`). N1–N7 in §0.1 gelockt, Entscheidungen P8.5-A–P8.5-T, Steps 0/A/B/C/D/Z,
Abnahmezeilen P8.5-1–P8.5-20, `[VERIFY]` V95–V105. **Closeout ist §9 des Plans (gefüllt
2026-09-09, kanonisch); Einstieg für die P8.6-Planung ist
`docs/concepts/PHASE8_5_CLOSEOUT_HANDOVER.md` §4.** **Step 0
abgeschlossen** (Haushalt-Funde, Skelett, Größenkorrekturen); **A1 committet** (`499d9be`,
2026-09-04, Picker-Modus-Umschalter + Body-Markdown-Link-Helper + `localStorage`,
Modul-Status 🟡, Tests ⬜, vollständiger Session-Block im Phase-Head); **Drift nachgezogen**
in einem separaten Folge-Commit (Wurzel-Current-state, dieser Absatz, INDEX-Header);
**A2 committet** (Tastaturnavigation + gemeinsamer Pick-Pfad `_pickLinkPickerAt` +
CSS-Block-Entdopplung am Picker; drei neue statische Tests; Modul-Status 🟡; A1-Block
nach `SESSIONS_ARCHIVE.md` rotiert); **B1 committet** (`_TITLE_NOT_ID_HINT` generalisiert
in `mcpserver/tools.py:159-164` — Schlußsatz „Das gilt in jeder Textform" wörtlich aus
Plan §3 B1; zwei Asserts in `test_tools.py`; Abbruchregel-Abschnitt im Phase-Head;
Modul-Status 🟡; A2-Block nach `SESSIONS_ARCHIVE.md` rotiert); Abnahmestand
**3 ✅ · 4 🟡 · 13 ⬜ von 20**. **nächster Schritt:** **Block C** — v3-Vorabritt gegen
eine Wegwerf-Instanz (Plan §4, 13 Stationen Playwright-Smoke gegen den nie ausgelieferten
v3-Build; Wegwerf-Setup mit tmp `DATA_ROOT`/`auth.sqlite3`/eigenem Port, inkl. Portierung
von `scripts/rotate_session_block.sh` aus Phase 7 für `phase8_5_picker_release/`).

**[2026-09-04, Block C committet]** v3-Vorabritt gegen Wegwerf Port 18773 (V98) gefahren:
`phase8_5_picker_release/scripts/wegwerf_setup_v3ritt.py` (Standing-Permission-Muster aus
Phase 8 reproduziert — eigener Port, tmp `DATA_ROOT`/`auth.sqlite3`, File-Keyring; 30
Items über 3 Spaces alpha/beta/gamma inkl. 1 archiviertes, 1 mit item-level `share_read=
["gamma"]` (P6-§35-39-Deploy-Blocker-Fall), 1 mit Bild-Asset via `put_asset()`; 11
explizite Kanten inkl. V102-Zwillings-Kante Buecherliste ↔ Empfehlungen Nikinger);
`scripts/rotate_session_block.sh` aus `scripts/` nach `phase8_5_picker_release/scripts/`
portiert, YAGNI aus A1/A2 geschlossen; `phase8_5_picker_release/scripts/
v3_ritt_playwright_smoke.py` neu (~720 Zeilen, `pyotp`+`async_playwright`). **Ergebnis:
26/26 Stationen grün** (Chromium 13/13 + Firefox 13/13, V101 für beide Browser
bestätigt); drei echte Befunde vorgelegt, **keine Code-Fixes im Tabu-Bereich nötig**:
(1) Smoke-Bug Edge-Keys `src_id`/`dst_id` → `src`/`dst` (gefixt im Smoke, kein
Server-Bug — passt zu `graph.js:325/394` und `webui/api.py:719`), (2) CSRF-Origin-
Mismatch zwischen `http://127.0.0.1:18773` und `SPACE_PUBLIC_BASE_URL=
https://wegwerf-v3ritt.invalid` wegen `_validate_base_url`-Pflicht (Befund für Step Z /
Plan §4.C3, **nicht** in dieser Phase lösbar ohne Server-Code-Touch), (3) Station 12
nur strukturell (`prefers-reduced-motion`-Regel im CSS gefunden, keine echte
Browser-Probe mit umgeschaltetem UA — bleibt, throwaway-verifiziert in Phase 8
`p8_22_smoke.py`); Modus-Selektor `<select>` vs. N3-Vorschau-Radio nicht als Befund
behandelt (P8.5-F-Planer-Substitution, P8.5-19-Sichtprüfung). Abnahmestand jetzt
**3 ✅ · 13 🟡 · 4 ⬜ von 20** (P8.5-5/-6/-7/-8/-10/-11/-13/-15/-16 aus Block C
`⬜`→`🟡`). 16 Screenshots `docs/screenshots/v3ritt_{chromium,firefox}_NN_*.png` neu.
`pytest -q` 962/962 unverändert (kein Python-Touch im Block-C-Setup), Tabu-Diff §0.3
leer, Service-Touch 0 (PID 195922 / ActiveEnterTimestamp 2026-09-02 11:51:57 CEST
nur gelesen; Wegwerf PID 337447 sauber abgebaut via `kill -TERM $(cat serve.pid)`,
Hard Rule 9-konform). **nächster Schritt:** **Block D** — Release-Vorbereitung
(`v3.0` → `v3.0.1`, neuer `## 2026-09-04`-Block in `docs/UPDATE_LOG.md` mit drei
menschenlesbaren Zeilen), D2 Deploy als **Nikinger-Aktion** (Hard Rule 9 + P8.5-Q,
niemals `sudo systemctl restart sharefyx-mcp` durch opencode/M3), D3 Health-Gate,
D4 Sichtprüfung am echten Gerät, D5 Vierte A3-Probe (an der die Abbruchregel §9.4.1
(N2) fällt oder hält).

**[2026-09-05, D1 committet]** Release-Vorbereitung opencode/M3: Badge `v3.0` →
`v3.0.1` in `phase5_ui/webui/static/app.html:20` (P8.5-N7); neuer `## 2026-09-05`-
Block in `docs/UPDATE_LOG.md` mit drei Zeilen (Picker-Modi / Tastatur / Generalisierter
Hint). **Datums-Drift zur Block-C-Spec ausdrücklich dokumentiert:** Block-C-Absatz oben
hatte noch `## 2026-09-04` vorgeschlagen (geschrieben am 2026-09-04, dem Tag von Block C);
heute ist `date +%F`/`date -u +%F` = 2026-09-05, und `deploy.sh` Z. 117–131 verlangt strikt
`today_utc` oder `today_local` als oberstes Datum, sonst Gate-Abbruch — Eintrag deshalb auf
2026-09-05 datiert. Block-C-Block per Hand nach `SESSIONS_ARCHIVE.md` rotiert
(newest-first, vor B1); Skript `scripts/rotate_session_block.sh` passt nicht auf das
Phase-8.5-Muster mit einem `## Session stopped`-Header + mehreren `### date`-Subblöcken
(Skript zählt `## Session stopped`-Header und sieht immer genau einen → Exit 2 „Bereits
konform"). Modul-Status D `⬜` → `🟡` mit D2–D5 als Nikinger-Aktionen vermerkt. `pytest`
nicht gelaufen (kein Python-Touch), Tabu-Diff §0.3 leer (`app.html` und `docs/UPDATE_LOG.md`
nicht tabu), Service-Touch 0 (PID 195922/ActiveEnterTimestamp 2026-09-02 11:51:57 CEST nur
gelesen). **nächster Schritt:** D2 — Deploy als Nikinger-Aktion
(`SHAREFYX_SYSTEMCTL="sudo systemctl" phase5_ui/scripts/deploy.sh main` in interaktiver
Vordergrund-Shell, V103 prüft den `sudo`-Prompt; Hard Rule 9 — niemals `sudo systemctl`
durch opencode/M3), D3 Health-Gate 3/3 + V105, D4 Sichtprüfung am echten Gerät +
P8.5-19-Abnahme des `<select>`-Modus-Selektors, D5 Vierte A3-Probe (entscheidet §9.4.1
Abbruchregel aus N2).

**[2026-09-05, D2 vom Nikinger zwischen D1 und D3 + D3-Prep committet]** D2 ist zwischen
D1 (Commit heute früh) und D3 (diese Session) **still durch den Nikinger gelaufen** —
Entdeckung kam erst beim ersten Probe-Lauf des Health-Gate-Skripts:
`/opt/sharefyx/current` → `20260905T140325.378914Z` → HEAD `6f19a8f` (D1), Service-PID
**355956** (statt der im D1-Block notierten 195922 — D2-Deploy hat den Dienst erwartungsgemäß
neu gestartet), `ExecMainStartTimestamp=2026-09-05 16:10:18 CEST`. Damit ist D3 nicht mehr
Vorbereitung, sondern **Verifikation des bereits deployten v3.0.1**. Neu gebaut:
`phase8_5_picker_release/scripts/health_gate.sh` (134 Zeilen bash, `set -uo pipefail`,
JSON auf stdout / Details auf stderr nach Hard Rule 7), acht Gates — `/health` 200 mit
Retry-Loop (max `--max-wait` Sekunden, Default 30, wie `deploy.sh` Z. 192-200), `/ui/login`
200, `/api/v1/me` 401, `/mcp/` 401 (wie `deploy.sh` Z. 202-217), `.rail__version` aus
`/ui/static/app.html` (**nicht** `/ui/login` — das ist `pages.py`s Auth-Template und enthält
keine Rail; erste Iteration fiel darauf herein, dann gefixt), `/opt/sharefyx/current` →
Release-Verzeichnis mit `.git`, optional `--require-todays-update-log` (oberster
`## YYYY-MM-DD` in `docs/UPDATE_LOG.md` == heute UTC/local, wie `deploy.sh` Z. 127-131),
optional `--expected-sha=<hex>` (Release-SHA matched Short- oder Full-Form per
Prefix-Vergleich). **Lauf-Beleg 2026-09-05 15:19:53Z** mit `--require-todays-update-log
--expected-sha=6f19a8f`: **8/8 grün**, Exit 0, JSON auf stdout
(`{"action":"health_gate","result":"ok","expected_version":"v3.0.1",
"actual_version":"v3.0.1","active_release":"/opt/sharefyx/releases/20260905T140325.378914Z",
"release_sha":"6f19a8fc1f0bcdc2c3bc91fc934a057964647ed4","port":8765}`). Drei Negativproben
separat verifiziert (Port 9999 → Gate 1 rot, `--expected-version=v9.9.9` → Gate 5 rot,
`--expected-sha=0000000` → Gate 8 rot). **P8.5-17 teilweise abgehakt:** Deploy gelaufen ✅,
Health-Gate 8/8 ✅, Badge `v3.0.1` live ✅, Update-Banner-Live-Anzeige ⬜ (braucht Auth,
Nikinger), V105 ⬜ (echter Anthropic-Connector, Nikinger). Modul-Status-Zeile 6 Block D um
D2 ✅ + D3 🟡 erweitert; Abnahmestand-Zeile P8.5-17 Health-Gate-Teil 🟡; Summary
**3 ✅ · 14 🟡 · 3 ⬜ von 20**; D1-Block (111 Zeilen) per Hand nach `SESSIONS_ARCHIVE.md`
rotiert (Skript passt nicht auf das Phase-8.5-Muster — bewährtes Vorgehen aus D1 selbst).
`pytest` nicht gelaufen (kein Python-Touch), `bash -n` OK, shellcheck nicht verfügbar
(übersprungen, keine Konvention im Repo), Tabu-Diff §0.3 leer, Service-Touch 0 (PID 355956
nur gelesen). **nächster Schritt:** **D4 ✅ erledigt 2026-09-06** (Sichtprüfung am echten Gerät durch den Nikinger,
Update-Banner sichtbar, beide Picker-Modi funktional, drei echte Findings dokumentiert: **P8.5-19
Radiogruppe** statt `<select>` — Tausch 5 Z. ausstehend; **P8.5-6 Bracket-Renderer-Bug** in
`markdown.js` — Fix ausstehend; **UX-2-Step-Knotenklick** als neues Feature für p8.X parkiert;
**Phase 8 ✅ + p8.X** als Nikinger-Entscheidung für Z vorgemerkt); **D5 Vierte A3-Probe**
(entscheidet §9.4.1 Abbruchregel aus N2 — Nikinger-Aktion); **V105-Connector-Check** (echter
Anthropic-Connector — Nikinger-Aktion); **optional vor Z** durch opencode/M3: Radiogruppe-Tausch
(P8.5-19) + Bracket-Renderer-Fix (P8.5-6); dann **Z (Closeout)** mit Phase-8-✅-Eintrag +
p8.X-Ankündigung in `phase8_ui_graph_plan.md §9.4.7`.

---

## Phase 8.X — UI-Polish-Folge-Phase (nur Notizen, kein Plan)

**Mission, ein Satz:** Nach dem v3.0.1-Deploy und dem Phase-8.5-Closeout sammelt diese
Folge-Phase die offenen UI-Polish-Wünsche aus der Sichtprobe-Folgesession 2026-09-06
(Nikinger + Fabian) plus die bereits in Phase 8.5 D4 parkierten p8.X-Punkte.

**Status:** ⬜ nicht gestartet, **kein** Plan-Doc, **kein** Locking. Nikinger-Entscheidung
in Phase 8.5 D4 vorgemerkt (`phase8_5_picker_release/CLAUDE.md` und
`phase8_ui_graph_plan.md §9.4.7`).

**Notiz-Sammlung:** `docs/concepts/p8x_ui_polish_notes.md` (L2, **40.9 KB**, 2026-09-06
angelegt, zuletzt 2026-09-09) — **zehn Abschnitte**: §1 Spaces-Layout-Reorg, §2 Obsidian-Map
(fünf Sub-Punkte), §3 Anzahl-Anzeige Ordner, §4 Edit-in-Place-Vision, §5 Layering-Design-System,
§6 „Konto"→„Einstellungen"-Rename, §7 De-AI-ierung-Lauf 2, §8 customizable Tags + Standard-Tag
„blocked", §9 direkter Feedback-Button, **§10 (2026-09-09) neun Nikinger-Punkte aus dem
Phase-8.5-Closeout-Auftrag** — Icon-/Trägerflächen-Radien, Hover als transparentere
Standardauswahl, Ordner-/Tags-Auswahl, klickbare Spaces, Einstellungsmenü, alles Klickbare mit
Farbausnahme für „Abmelden"/„Archivieren", verbundene AI-Sessions, Hochkant-/Handy-UI.
Anhang §A–§E. **Die Zahlen „16 Themen / 25 KB" hier standen bis 2026-09-09 stale.**

**Reihenfolge der nächsten Schritte (Stand 2026-09-09):**

1. ~~**Phase 8.5 Z**~~ **✅ erledigt 2026-09-09** — Phase 8 + 8.5 formal abgeschlossen,
   Closeout in Plan §9, Handover `docs/concepts/PHASE8_5_CLOSEOUT_HANDOVER.md`.
2. **Planungs-Session für P8.6** (Claude Code, weil §5 Layering + §10 design-system-weit
   sind) — beantwortet die §C-Fragen, schätzt Reichweite, spaltet ggf. in Sub-Phasen.
   **Erster Punkt der Phase: OpenCode-Vision-Plugin installieren** (Nikinger-Vorgabe).
   Einstiegsdokument ist das Handover §4, nicht die Phase-Heads.
3. ~~**Plan-Doc + Phase-Verzeichnis** — Name noch nicht gelockt~~ **✅ erledigt 2026-09-09**
   — gelockt als `phase8_6_ui_polish/` + `docs/concepts/phase8_6_ui_polish_plan.md` (P8.6-A).
   **Die Nummern-Frage ist entschieden:** der Nikinger hat bestätigt, dass sein „eher v3.1
   also p8.7" das meint, was die Dokumente **P9 → `v3.1.0`** nennen. **Es gibt kein P8.7.**
   Die verbundenen AI-Sessions (`p8x_ui_polish_notes.md` §10.8) sind damit P9-Inhalt.
   Umbenannt wurde nichts — der Wortlaut bleibt in §10.8 zitiert stehen.
4. **Ausführung P8.6** in opencode/M3 nach Plan §1–§8, Reihenfolge Step 0 → Step V → A → B
   → C/D → Gate → Deploy → Step Z. Der Closeout wird Plan **§9** (P8-N).

**Was NICHT in p8.X gehört** (klare Außenkanten, Notizen-Datei §B): Body-Volltextsuche
in der Web-UI (Q1 gelockt), Rechteverwaltung über MCP-Tools (P6-M), Löschen von Items
(F2), FastMCP-4/V79 (eigene Mini-Phase per P5-C), Funnel-Watchdog, ~~Mobile/~~Realtime,
Light-Mode (P5-X), Glyph-Entscheidungen P6/P6.5. **[2026-09-09, Nikinger]:** die
**Mobile-Hälfte ist aufgehoben** — die Hochkant-/Handy-Ansicht ist ab sofort ein benanntes
Zukunfts-Item (Notizen §10.9), kein P8.6-Auftrag, aber in einer freieren Phasenplanung zu
berücksichtigen. **Realtime bleibt draußen.**

---

## Bewusst nicht auf der Roadmap

- **Semantische Suche / Embeddings.** Verstößt gegen das Bauprinzip. Bei zwei Nutzern und
  einigen hundert Items schlägt Frontmatter-Filterung jede Vektorsuche in Präzision und Kosten.
- ~~**Feingranulare Rechte.** Zwei Personen, gegenseitiges Vertrauen. Cross-Space-Read ist
  standardmäßig an. Der Schutz gegen fremde Inhalte ist Rule 4, nicht ein ACL-Modell.~~
  **Ergänzung 2026-07-25:** P2 baut den Seam dafür (`Permissions.can_read`), damit es später kein
  Umbau wird — die Policy selbst bleibt bewusst `True` für alle, siehe „Zurückgestellt aus P2".
  **[2026-08-09 Korrektur, P6-Planungssession]:** Der Satz war bis heute richtig; mit Phase 6
  wird er widerlegt — Sichtbarkeitsstufen und Item-/Ordner-Freigaben (P6-J/K) sind jetzt Scope.
  Details: `docs/concepts/phase6_shares_plan.md` §0.5.
- **Mehrmandantenfähigkeit.** Wenn ein dritter Nutzer dazukommt, ist das eine Planungssession,
  kein `if`-Zweig. **[2026-08-09 Korrektur, P6-Planungssession]:** Der Satz ist **erfüllt, nicht
  widerlegt** — die Planungssession hat am 2026-08-09 stattgefunden und genau daraus ist Phase 6
  entstanden; ein dritter Nutzer wird darin real angelegt, geprüft und wieder entfernt (P6-W),
  über eine echte Planungssession, keinen stillen `if`-Zweig.
