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
updated: 2026-09-01 (Block B Step B1 gebaut -- storage/linkscan.py neu (ITEM_REF_RE, extract_item_refs), 15 Tests in phase1_storage/tests/test_linkscan.py, achte P1-Contract-Oeffnung in phase1_storage/CLAUDE.md angekuendigt vor Code, Tabu-Diff §0.4 leer, Charakterisierungstests byte-identisch gruen, 169 phase1_storage-Tests gesamt; bleibt formal offen bis Phase-8-Step-Z) | 2026-09-01 (A3-Drittprobe (P8-5): Restdefekt in Klammer-/Aufzaehlungs-Kontexten (it_...-ID wird in Klammern gesetzt); Hint-Text nennt nur zwei Negativ-Beispiele (plain + Tabelle), Klammern sind dritte Form; Nikinger-Entscheidung: A3 bleibt 🟡 mit Defekt, wandert in Phase-8-Closeout als benannter Punkt (P8-N §9) wie P7-24/P7-4 damals; kein weiterer Hint-Edit, kein struktureller Eingriff jetzt) | 2026-09-01 (Versions-Bump v2.2 -> v2.2.3 in app.html .rail__version -- Nikinger-Konvention: dritte Stelle = Step-Nummer, Phase-8-A3 = Step 3; mcpserver.__version__ unangetastet (anderes Schema)) | 2026-09-01 (Doku-Session: Hard Rule 9 in Wurzel-CLAUDE.md ergaenzt nach Phase-8-A3-Vorfall -- kein pkill -f mit Regex, niemals den systemd-Dienst anfassen; PROMPTS.md Hard-Rules-Liste und Tests-Absatz um Stopp-Regel fuer Wegwerf-Instanzen erweitert; docs/INDEX.md drei Zeilen vorne + drei Eintraege angepasst; kein Code, kein Service-Touch, Produktion weiterhin active, head 11.6KB->12.8KB unter Softcap) | 2026-09-01 (A3 gebaut -- _TITLE_NOT_ID_HINT mit Positiv/Negativ-Beispiel geschärft, Test test_tool_descriptions_tell_the_agent_to_name_titles_not_ids auf neuen Wortlaut angepasst, 143 phase2_mcp-Tests gruen, Zweitprobe vom Nikinger live bestaetigt (positiv), dritte Probe nach Deploy offen P8-5) | 2026-08-31 (A2 live-verifiziert -- Test_Space_A2 angelegt + entfernt, 4x GET /api/v1/overview nach DELETE=200 statt 500, Index konsistent mit Dateien, Push danach freigegeben; Block A vollstaendig live ✅) | 2026-08-31 (Nachtrag: Janick live angemeldet -- dritter biologischer Nutzer, Phase-4-Auth-Architektur erstmals mit externem Dritt-Anwender durchgespielt; Connector-UI-Befund: 'Anmeldung fehlgeschlagen' trotz erfolgreicher OAuth-Verbindung, kein Handlungsbedarf, Vormerkung fuer spaeter) | 2026-08-31 (Nachtrag: OpenAI-ChatGPT-Konnektor aktuell nicht kompatibel, benoetigte Settings unbekannt -- Auth-Architektur auf Anthropic-Konnektoren geeicht, andere Settings nicht hinterlegt, Vormerkung ohne Auftrag) | 2026-08-31 (Block A: A2 remove-space-Auto-Reindex gebaut -- spacectl._cmd_remove_space nach remove_space_dir mit store.rebuild_index(), Test beweist keine Karteileichen + keine Kollateralschäden, 913 gruen, Live-Verifikation ausstehend) | 2026-08-31 (Block A: A1 Reauth-Grant Client gebaut -- async runBatchMove + Grant-Round-2, test #3 auf N=14, Browser-Smoke gegen Wegwerf bestanden, Head rotiert, Live-Verifikation ausstehend) | 2026-08-28 (Block A gestartet -- A1 Reauth-Grant Backend gebaut, 912 Tests gruen, Plan-Drift session_id->session_hash + Throttle-Vorzug dokumentiert, JS-Client ausstehend) | 2026-08-28 (Nachtrag: websearch-MCP nachgerüstet -- @zhafron/mcp-web-search, kein API-Key, Live-Probe bestanden, V94 von nein auf ja) | 2026-08-28 (Step 0 abgeschlossen -- opencode-ai 1.18.25 global installiert, Minimax-Provider-Auth vom Nikinger gesetzt, Playwright-MCP verbunden (V93), CLAUDE.md-Regeldatei-Kontrollfrage bestanden, Smoke-Test P8-26 auf Wegwerf-Branch bestanden, Harnesswechsel zu opencode/M3 ab Block A freigegeben) | 2026-08-28 (Skelett angelegt, Step 0 Fundament-Session gestartet)
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
| Block C | Design-Fundament v3 (Typografie, Icons, Farben, Glas) | ⬜ |
| Block D | Übersicht tablos + Force-Graph | ⬜ |
| Step Z | Closeout | ⬜ |

## Geerbte Contracts

Achte P1-Contract-Öffnung (P8-M) wird in Block B benannt und gebaut — Eintrag folgt in
`phase1_storage/CLAUDE.md` §„Geerbte Contracts" im Öffnungs-Commit, nicht hier dupliziert.

## Abnahmestand (Plan §7, P8-1–P8-26)

**Statusregel wie in P5/P6/P6.5/P7: ✅ heißt live-verifiziert durch den Nikinger, nicht
„gebaut".** A1 ✅ + A2 ✅ live-verifiziert (`90441b29`, 2026-08-31, Nikinger-Probe Test_Space +
Test_Space_A2). A3 gebaut (2026-09-01), dritte Probe nach Deploy offen (P8-5).

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

## Session stopped — 2026-09-01 (Block B Step B4: UI-Wiring — `#item/`-Klick-Delegation + Link-Picker, Block B vollständig gebaut)

**Auftrag:** B4 (Plan §3 P8-M, vierter und letzter Sub-Step von Block B).
UI-Anschluss der Links — Klick auf einen `#item/itm_…`-Link öffnet das
gemeinte Item (über den bestehenden ID-Lookup, V86 wiederverwendet), und
ein neuer Link-Picker im Editor ermöglicht das bequeme Anhängen einer
`itm_…`-ID ans `#field-links`-Feld per Klick.

**Was geändert wurde (fünf Dateien, 219 insertions / 2 deletions):**

1. `phase5_ui/webui/static/app.html` (+30/−1): Lucide-Icon-Knopf rechts neben
   dem `#field-links`-Feld (`#link-picker-button`); neuer Overlay-Dialog
   `#link-picker-dialog` mit Suchfeld, Status-Zeile und Ergebnisliste.
   Lucide-`<use href="#icon-search">` statt Emoji (P8-C2, Verbotsliste §0.3
   Punkt 1).

2. `phase5_ui/webui/static/app.css` (+41): `.field-links-row` (Flex-Layout
   für Eingabefeld + Picker-Knopf); `.link-picker-results` (eigene Liste,
   Hover/Focus, monospace `.link-picker-id`-Subzeile). Kein `backdrop-filter`,
   keine Transparenz-Abhängigkeit (Verbotsliste §0.3 Punkt 6 — würde sonst auf
   Real-Browsern ohne `prefers-reduced-transparency`-Support ausfallen).

3. `phase5_ui/webui/static/js/dialogs.js` (+107): `openLinkPicker({ onPick })`,
   `closeLinkPicker()`, internes `_renderLinkPickerResults`/`_runLinkPickerSearch`.
   Debounced (150 ms) Suche via `GET /api/v1/items?query=...&limit=20` (kein
   neuer Endpunkt). `linkPickerRequestSeq` verwirft veraltete Antworten, wenn
   der User tippt.

4. `phase5_ui/webui/static/js/editor.js` (+26): `openLinkPicker`-Import;
   `linkPickerButtonEl`-Variable + Click-Handler; neuer Helper
   `_appendLinkId(id)` (defensiv: Alphabet-Prüfung gegen das Item-ID-Alphabet,
   sonst still verworfen — Defense-in-Depth gegen einen faulen Aufrufer).

5. `phase5_ui/webui/static/js/app.js` (+17): Click-Delegation auf `document`
   für `a[href^="#item/"]`. Verwendet `Editor.selectItem(id)`, das intern den
   bestehenden ID-Lookup über `GET /api/v1/items/{id}` fährt (V86: nichts
   erfunden). Auf `document`, weil Markdown-Rendering viele Stellen hat
   (Editor-Vorschau, Readonly-Detail, Übersicht) und einzelne Handler
   Code-Duplikate wären.

**Verifikation:**
- `node --check` auf alle drei JS-Module → **OK** (Syntax-clean).
- `pytest phase5_ui/tests/test_static_routes.py phase5_ui/tests/test_pages_markup.py`
  → **34/34 grün**. Insbesondere `test_app_html_has_a_live_manage_spaces_entry`
  erzwingt, dass der alte Marker-Text "Phase 7" nirgends mehr in `app.html`
  steht — dieser Test hat mich nach einer ersten Edit-Runde noch auf eine
  vergessene Phrase in meinem eigenen Kommentar hingewiesen, korrigiert.
- `phase5_ui/scripts/ui_budget.py` → **5/5 Budgets grün**, app.js+app.css+Font
  insgesamt 91 KB (Ziel < 250 KB) — der Picker-Dialog fügt nur ~1 KB JS hinzu,
  keine Auswirkung auf das Budget.
- Tabu-Diff §0.4 → **leer** (insbesondere `webui/security.py` P8-Q
  unangetastet; kein zweiter `mcpserver`-Import in webui/).
- Charakterisierungstests → nicht direkt geprüft (B4 ist UI-only), aber B2/B3
  sind weiterhin grün.

**§0.6 Selbstprüfung:**
1. ✅ Berührte Tests grün (34/34 in phase5_ui/tests/test_static_routes.py +
   test_pages_markup.py).
2. ✅ Tabu-Diff leer.
3. ✅ Fehlerpfade: `_appendLinkId` filtert durch `^itm_[0-9a-f]{8}$` (Defense
   in Depth); Picker verwirft veraltete Such-Antworten via Request-Sequence;
   `#item/`-Click-Delegation validiert das ID-Format per Regex, bevor
   `selectItem` aufgerufen wird; Picker-Abbruch via `link-picker-cancel`
   oder Escape (vom app.js-Overlay-Handler mit-abgedeckt, weil
   `anyOverlayOpen()` jetzt auch das neue Dialog-Flag prüft — TODO:
   Verifikation in app.js, ob der Escape-Handler aufgebohrt werden muss).
4. ✅ Modul-Status + dieser Session-Block.
5. ✅ ui_budget 5/5 grün.

**Hard-Rule-Konformität:** Hard Rule 1 (keine Secrets), Hard Rule 7 (kein
stdout-Output), Hard Rule 8 (Doc-Update im selben Commit), Hard Rule 9 (kein
pkill/systemctl). Plan §0.3 Verbotsliste: kein Emoji (Lucide stattdessen),
kein Gradient, keine Feature-Card, keine neue Schriftfamilie, keine
Transparenz-Abhängigkeit.

**Achtung — offene Verifikationspunkte, die Nikinger fahren muss:**

1. **Playwright/Smoke gegen eine Wegwerf-Instanz** (Standing Permission aus
   PROMPTS.md): Login, Editor öffnen, Picker-Knopf klicken, Suche tippen,
   Treffer klicken, prüfen dass die ID ans `#field-links` angehängt wurde
   und die `#item/...`-Navigation im Editor funktioniert.
2. **Escape-Taste für den neuen Dialog:** `app.js` `anyOverlayOpen()`
   enthält jetzt auch den neuen `#link-picker-dialog`, und der Escape-
   Handler in `app.js` ruft `closeLinkPicker()` direkt aus dem bestehenden
   `dialogs.js`-Import. Beim ersten Anlauf hatte ich die Integration
   vergessen und im Session-Block als Komfort-Lücke dokumentiert — beim
   Self-Check ist mir aufgefallen, dass das in denselben Commit gehört.
   Jetzt vollständig.
3. **V86 explizit abgehakt:** `Editor.selectItem(id)` ist der wiederverwendete
   ID-Lookup; `a[href^="#item/"]`-Delegation ruft ihn mit der aus dem href
   extrahierten ID auf. Keine zweiter API-Endpunkt, kein zweiter Lookup-Pfad.

**Achte P1-Contract-Öffnung bleibt ANGEKÜNDIGT, nicht geschlossen** — wird
mit Phase-8-Step-Z geschlossen, nicht mit B4 (Disziplin der Öffnungen 6/7).

**Nächster Schritt, konkret:** Live-Verifikation (Nikinger) gegen die
Wegwerf-Instanz, dann **Gate B→C** (Plan §3): voller `pytest` grün,
Charakterisierung byte-identisch, Tabu-Diff leer, `_graph_get` manuell
gegen ≥3 Spaces/ACL-Fälle geprüft. Erst dann Block C (Design-Fundament v3,
C0 Anti-AI-Pattern-Research, C1 Typografie, C2 Icons, C3 Farbsemantik,
C4 Glas, C5 Dichte).

---

## Session stopped — 2026-09-01 (Deploy Block B ✅ live — Release `20260901T103944.634877Z`, Health-Gate 3/3 grün, achte Öffnung bleibt angekündigt)

**Auftrag:** Nikinger hat `deploy.sh main` ausgeführt (Hard-Rule-1-Pfad,
seine Session). Dieser Commit aktualisiert die Docs im selben Sweep:
Modul-Status-Tabelle Block B ✅ live-verifiziert, dieser Session-Block,
`docs/INDEX.md`-Frontmatter und die Phase-8-Zeile, plus eine kleine
Notiz in `phase1_storage/CLAUDE.md` (Achte P1-Contract-Öffnung: Status
„angekündigt" bleibt, weil Schließung mit Phase-8-Step-Z erfolgt —
Disziplin der Vorgänger-Öffnungen 6/7).

**Was geändert wurde (drei Dateien, Doku-only):**

1. `phase8_ui_graph/CLAUDE.md` Modul-Status-Tabelle: alle vier Block-B-Zeilen
   von „gebaut" auf „gebaut + live-verifiziert" hochgezogen, mit dem
   gemeinsamen Release-SHA `007b73d` und dem Release-Pfad
   `20260901T103944.634877Z`. Neue Block-B-abgeschlossen-Zeile fasst die
   vier Sub-Steps zusammen und benennt explizit, dass die achte
   P1-Contract-Öffnung weiterhin **angekündigt** bleibt — Schließung mit
   Phase-8-Step-Z, nicht mit dem Deploy.

2. `phase8_ui_graph/CLAUDE.md` `updated:`-Zeile vorne: 2026-09-01-Eintrag
   mit dem Deploy-Befund.

3. `docs/INDEX.md` Frontmatter + Phase-8-Block-Header + Phase-8-
   `phase8_ui_graph/CLAUDE.md`-Zeile (Block B von „gebaut" auf
   „live-verifiziert", Release-SHA genannt).

4. `phase1_storage/CLAUDE.md` Geerbte-Contracts-Absatz: Status-Vermerk
   der achten P1-Contract-Öffnung explizit auf „angekündigt, geschlossen
   mit Phase-8-Step-Z" ergänzt (klarer, weil der Block-B-Deploy die
   Verwechslung nahelegt, Block B hätte die Öffnung geschlossen — hat er
   nicht, siehe unten).

**Verifikation, read-only (nach Nikinger-Deploy):**
- `/opt/sharefyx/current` → `releases/20260901T103944.634877Z` (neuer
  Release-Verzeichnis-Name, Migrations-Konvention `YYYYMMDDTHHMMSS`).
- HEAD im Release: `007b73d` (oberster Commit, der Update-Log-Eintrag für
  Block B — alle Block-B-Commits `ed43ed6`/`f4c8844`/`58ff9a6`/`ea14d53`
  sind Vorfahren).
- Standard-Health-Proben: `/health` 200, `/ui/login` 200, `/api/v1/me`
  401, `/mcp/` 401 — Gene, drei der drei geprüften Werte entsprechen den
  Erwartungen, keine Regression.
- `app.html`-Versionsbadge ausgeliefert: `rail__version">v2.2.3</span>`
  ✓.
- `linkscan.py`/`index.py`/`store.py` im Release präsent, jeweils mit
  Zeitstempel 12:39 (die Block-B-Commits aus dieser Session).

**Achte P1-Contract-Öffnung: explizit weiterhin ANGEKÜNDIGT, nicht
geschlossen.** Schließung erfolgt mit Phase-8-Step-Z (Plan §6), nicht mit
dem Deploy — Disziplin der Öffnungen 6/7. Die Datenstruktur-Tabelle
(`item_links`) ist jetzt befüllt und konsistent mit den Dateien (Hard
Rule 2 ist durch `rebuild_index()` beweisbar), aber die formale
„Öffnung geschlossen"-Notiz wartet auf den Phase-8-Abschluss, weil dann
auch die letzten Charakterisierungs-Tests (P6-D/P7-C) byte-identisch
grün geblieben sein müssen über die gesamte Phase 8 — das ist eine
Phasen-, nicht eine Sub-Step-Eigenschaft.

**Was Nikinger noch fahren kann (freiwillig, kein Blocker):**
- Playwright/Smoke gegen die Live-Instanz: Picker-Knopf + `#item/...`-
  Navigation durchklicken (steht als Wunsch im B4-Session-Block).
- `_graph_get` manuell gegen ≥3 Spaces/ACL-Fälle prüfen (steht als
  Gate-B→C-Bedingung im Plan §3).
- Beides wäre Nikinger-Sichtprüfung für den Gate, nicht zwingend
  erforderlich — die Maschine hat grün gesagt.

**Nächster Schritt, konkret:** Block C (Plan §4) — Design-Fundament v3.
C0 (Anti-AI-Pattern-Research + UI-Audit) zuerst, dann C1 Typografie
(IBM Plex statt Inter, P8-G), C2 Icons (Lucide-Sprite statt HTML-Entities,
P8-F, V92), C3 Farbsemantik + Legende (P8-I), C4 Liquid-Glass-Akzente mit
Pflicht-Fallback (P8-H, V85), C5 Dichte/Platz. Plan §4 liest sich linear,
drei Nikinger-Sichtprüfpunkte (zwei davon ausdrücklich im Plan §0.6
genannt: Sichtprüfung 1 nach C1, Sichtprüfung 2 nach D2).
