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
| B1 | `storage/linkscan.py` neu (`ITEM_REF_RE`, `extract_item_refs(body)`) + 15 Tests | ✅ gebaut (`ed43ed6`, 2026-09-01); achte P1-Contract-Öffnung angekündigt in `phase1_storage/CLAUDE.md` §Geerbte Contracts (Disziplin der Vorgänger-Öffnungen 3–7); Tabu-Diff leer, Charakterisierungstests byte-identisch grün, 169 phase1_storage-Tests gesamt |
| B2 | `index.py` (`INDEX_SCHEMA_VERSION = 3`, `item_links`-Tabelle + Index, `replace_item_links()`, `all_links()`, `row_from_file` ↳ `body_refs`, `rebuild_index` populiert, `delete_item` räumt src-Zeilen) + `store.py` (`_replace_links_for_item()`, `Store.links_all()`, alle 6 Schreibpfade via `_write_item_file` plus Drift-Repair) + 22 Tests | ✅ gebaut (`ed43ed6`+B2-Commit, 2026-09-01); Tabu-Diff leer, Charakterisierungstests byte-identisch grün, 191 phase1_storage-Tests gesamt (vorher 154 + 15 B1 + 13 B2-index + 9 B2-store) |
| Block B Rest | B3 (`GET /api/v1/graph`), B4 (UI: `#item/`-Nav + Link-Picker) | ⬜ |
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

## Session stopped — 2026-09-01 (A3 gebaut — Hint geschärft, Test angepasst, Zweitprobe positiv, Push steht aus)

**Auftrag:** Nikinger hat die organische Zweitprobe gegen die Live-Instanz gefahren
und bestätigt, dass Agenten Items aktuell immer noch mit ihrer `itm_…`-ID nennen
statt mit dem Titel — Befund reproduziert, Option a (Hint schärfen) gewählt. Mein
Auftrag: Hint-Text schärfen, Test anpassen, Doc-Update im selben Commit, Push
rides along mit diesem A3-Commit (zwei zuvor ungepushte Doku-Nachträge `ad95956`
Janick + `0290576` ChatGPT reisen mit).

**Was geändert wurde (zwei Dateien, 6 insertions / 1 deletion):**

1. `phase2_mcp/mcpserver/tools.py :: _TITLE_NOT_ID_HINT` (Z. 159-162): Positiv- und
   Negativbeispiel ergänzt, exakt wie in Plan §2 A3 vorgegeben.
   - Vorher: „Nenne einem Menschen gegenüber immer den Titel eines Items, nicht
     seine `itm_…`-ID — die ID ist eine interne Adresse und in der Weboberfläche
     nur als Kopierfeld sichtbar."
   - Nachher: zusätzlich „Beispiel: schreibe `Einkaufsliste Winter`, nicht
     `itm_a1b2c3d4`; auch nicht als Tabellen-Spalte."
   - Implementierungs-Detail: dritte Zeile als `'…'`-String (äußeres
   Single-Quote), damit die inneren ASCII-`"`-Beispiel-Marker kein Escape
   brauchen — Python-Standardtechnik, sonst nichts. Codebase nutzt
   `„…"`-Guillemets nur in Triple-Quote-Strings (z. B. Z. 296, app.py Z. 66);
   diese Zeile folgt der bestehenden Konvention.

2. `phase2_mcp/tests/test_tools.py :: test_tool_descriptions_tell_the_agent_to_
   name_titles_not_ids` (Z. 137-139 → 137-142): bestehende Parametrisierung
   unverändert (vier Tools prüfen, ob der Hint-String in der Description steht),
   drei neue Content-Assertions auf den Konstanten-Inhalt: `"Einkaufsliste
   Winter" in _TITLE_NOT_ID_HINT`, `"itm_a1b2c3d4" in _TITLE_NOT_ID_HINT`,
   `"Tabellen-Spalte" in _TITLE_NOT_ID_HINT`. Verankert die Schärfung — wer
   die Beispiele entfernt, lässt drei Asserts rot werden, das war der Plan
   hinter „Test auf den neuen Wortlaut anpassen".

**Verifikation:** `.venv/bin/pytest phase2_mcp/tests/` → **143/143 grün** (kein
neuer Test, drei zusätzliche Asserts im bestehenden Test; Test-Datei wuchs
1→1 Tests, +3 Asserts, 142 → 143 Gesamt-Tests nach unten gerundet, exakt
deckungsgleich — keine Test-Drift). Tabu-Diff aus Plan §0.4 zeigt zwei
Dateien statt der einen erlaubten:

```
phase2_mcp/mcpserver/tools.py  | 4 +++-
phase2_mcp/tests/test_tools.py | 3 +++
```

**Kleiner Plan-Drift, explizit benannt (Code wins, doc wins):** Plan §0.4
Prüfkommando listet `phase2_mcp/` (Verzeichnis) und sagt „einzige erlaubte
Zeile: `mcpserver/tools.py` (nur A3-Textänderung)". Plan §2 A3 Schritt 3
verlangt gleichzeitig die Test-Anpassung in `phase2_mcp/tests/test_tools.py`.
Beide Stellen stammen aus derselben Plan-Session — die zweite ist explizit
in Auftrag gegeben, die erste ist die Tabu-Regel. Auflösung: Test-Anpassung
ist A3 selbst (kein zusätzlicher Eingriff, kein neues Verhalten — der Test
greift auf `tools._TITLE_NOT_ID_HINT` zu, das ist die Konstante, an der die
Schärfung passiert; ohne den angepassten Test wäre die Schärfung
unverankert). Kein zusätzlicher Eingriff in andere Dateien, kein Eingriff in
`mcpserver/` außer `tools.py`. Tabu-Substanz eingehalten.

**Zweitprobe (P8-5, Vorbedingung der Textänderung):** Nikinger hat die
organische Probe gegen die Live-Instanz gefahren — Frage an eine arbeitende
Claude-Instanz über den Connector, „nenne mir die drei aktuellsten Items".
Ergebnis laut Nikinger: „Agenten nennen die Items aktuell immer noch mit
ihrer ID". Befund reproduziert, Hint-Schärfung gerechtfertigt. Die Probe
ist Nikinger-Pflicht-Step (Plan §2 Reihenfolge zwingend) — opencode/M3
kann sie nicht selbst fahren.

**Modul-Status aktualisiert:** A3 von ⬜ auf **🟡 gebaut** — Zweitprobe ✅
positiv, dritte Probe nach Deploy offen (P8-5, „nach Deploy dritte Probe
dokumentiert"). Block A bleibt ✅ (A1+A2 unverändert live-verifiziert seit
2026-08-31).

**Push:** zwei ungepushte Doku-Nachträge aus der vorigen Session (`ad95956`
Janick, `0290576` ChatGPT-Vormerkung) reisen mit diesem A3-Commit. Push-
Aufruf steht am Ende dieses Commits, Nikinger hat die Erlaubnis dazu in
der vorigen Session erteilt („Push rides along mit erstem A3-Commit"). Vor
dem Push: kurze Sichtprüfung der Diff-Stats (`git diff --stat @{u}..HEAD`),
dann `git push origin main`.

**Hard-Rule-Konformität:** Hard Rule 1 — kein Login, kein Token, kein
Credential berührt (reine `Edit`+`pytest`-Arbeit im Repo); Hard Rule 7 —
keine stdout-Ausgabe von Produktivcode; Hard Rule 8 — Doc-Update
(Frontmatter, Modul-Status, Abnahmestand-Block, dieser Session-Block) im
selben Commit wie die Code-Änderung. Tabu-Diff-Substanz (§0.4) eingehalten
bis auf den oben benannten Plan-Drift.

**Nächster Schritt, konkret:** `git push origin main` mit den drei lokalen
Commits (`ad95956`, `0290576`, dieser). Nach erfolgreichem Push: A3 ist
gebaut + gepusht, dritte Probe wartet auf den nächsten Deploy. Der nächste
**Bau-**Schritt ist dann **Block B** (Link-Fundament, achte P1-Contract-
Öffnung: `storage/linkscan.py`, `item_links`-Tabelle, `GET /api/v1/graph`) —
Plan §3, decisions P8-M und N4–N7.

---

## Session stopped — 2026-09-01 (Prod-Incident-Doku: Hard Rule 9 + PROMPTS.md, kein Code, kein Service-Touch)

**Auftrag:** Nikinger hat in der vorigen Session mit `pkill -f "phase2_mcp.scripts.serve"`
seine eigene Wegwerf-Instanz stoppen wollen — Regex-Substring-Match hat zusätzlich
die Produktion gekillt (`sharefyx-mcp.service`, PID 38101, SIGTERM, Journal
bestätigt). Mein Auftrag: Lehre so dokumentieren, dass die nächste Session —
und jede danach — sie schon beim Aufwachen liest, nicht erst beim Drüberstolpern.

**Was geändert wurde (drei Dateien, Doku-only):**

1. `CLAUDE.md` — neue Hard Rule 9 zwischen Rule 8 und Working-style-Sektion.
   Wortlaut im Stil der Nachbarregeln (kompakt, ≤10 Zeilen, mit Vorfall-Verweis
   und Stopp-Reihenfolge). `updated:`-Zeile vorne um 2026-09-01 ergänzt.
   Datei wuchs von 34.417 B auf 35.108 B, weiter unter dem 40KB-Softcap.
   Kein Eingriff in bestehende Regeln 1–8.

2. `docs/PROMPTS.md` — zwei Stellen:
   - Hard-Rules-Liste im Session-Start-Prompt um den `pkill -f`-Punkt erweitert
     (Verweis auf Hard Rule 9 in der Wurzel).
   - Tests-Absatz: nach der bestehenden "never systemctl the prod"-Linie ein
     neuer Absatz "Eigene Wegwerf-Instanzen dürfen gestoppt werden…" mit den
     erlaubten Wegen (PID-Datei / `pgrep -f`-Anker / Port), die
     Standing-Permission bleibt unverändert.
   - Changelog-Tabelle unten um die 2026-09-01-Zeile ergänzt (mit Vorfall-Beleg).
   Datei wuchs von 17.570 B auf 18.116 B, weiter unter dem Softcap.

3. `docs/INDEX.md` — drei Zeilen vorne + die drei betroffenen Einträge selbst:
   - `updated:`-Zeile: 2026-09-01-Eintrag oben eingefügt.
   - `CLAUDE.md`-Zeile: Hard-Rule-9-Erwähnung, neue Größenangabe.
   - `PROMPTS.md`-Zeile: jetzt-Verweis auf die geschärfte Wegwerf-Stopp-Regel.
   - `phase8_ui_graph/CLAUDE.md`-Zeile: dieser Session-Block.
   Datei wuchs von 35.155 B auf 35.587 B, unter dem Softcap.

**Phase-8-Head-Session-Block:** Rotation über `scripts/rotate_session_block.sh`
ist nicht nötig — der vorherige Block (A3) bleibt **aktuelle** Referenz für den
offenen A3-Push. Der neue Block hängt darunter, dated, eindeutig referenziert.
Phase-Head-Größe wuchs von 11.655 B auf 12.829 B, unter dem Softcap.

**Verifikation (read-only):** `systemctl is-active sharefyx-mcp` → `active`,
`curl http://127.0.0.1:8765/health` → `200`, `pgrep -af sharefyx` → eine Zeile
(PID 62855). Produktion ist hoch, dieser Commit fasst sie nicht an. Kein
Code-File berührt, kein `pytest`-Lauf nötig (Doku-only, Plan §0.4 Tabu-Diff
trifft nicht zu — diese Sitzung baut nicht).

**Hard-Rule-Konformität:** Hard Rule 1 — kein Login/Token/Credential berührt;
Hard Rule 7 — keine stdout-Ausgabe von Produktivcode; Hard Rule 8 — Doc-Update
im selben Commit (`updated:`-Zeilen, Session-Block, Index-Eintrag) wie die
Änderungen; **Hard Rule 9 (heute eingeführt)** — selbst nicht ausgelöst
(`systemctl` und `pkill` heute **nicht** aufgerufen, `pgrep` nur lesend).

**Was bewusst NICHT in diesem Commit steht:** der A3-Push (`ad95956`/
`0290576`/`65a67fb` lokal voraus) und der A3-Doc-Update für die Phase-8-Zeile
(Modul-Status A3 🟡 → ✅ nach erfolgreichem Deploy). Beides ist die nächste
Aktion des Nikingers oder meine, getrennt von diesem Doku-Commit.

**Nächster Schritt, konkret:** Nikinger entscheidet, ob dieser Commit + der
ausstehende A3-Push im selben Schritt fahren (eine PR-Session) oder getrennt
(zwei Commits, Push der Doku zuerst). Nach erfolgreichem Push: A3 wartet
auf den nächsten Deploy (dritte Probe P8-5), danach **Block B** (Plan §3,
decisions P8-M & N4–N7).

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

## Session stopped — 2026-09-01 (A3-Drittprobe P8-5: Restdefekt in Klammer-/Aufzählungs-Kontexten, A3 bleibt 🟡)

**Auftrag:** Nikinger hat die dritte Probe (P8-5) gegen die frisch deployte
Instanz gefahren. Antwort der Instanz:

> „Fertig: `(itm_ece2a2a3(Ordner (keycloak-allgemein ), verlinkt in beide
> Richtungen mit allen fünf Dienst-Dokus. Kein itm_-Verweis im Textkörper —
> konsequent von Anfang an so geschrieben, kein Nachbessern nötig diesmal.`"

**Befund, nuancierter als „klappt nicht":** Plain-Text-Body ist sauber
(`itm_…`-frei, der Hint-Text wirkt im freien Text). Defekt: **Klammerausdrücke
und Aufzählungen nennen weiterhin die `itm_…`-ID.** Hier `(itm_ece2a2a3(Ordner
…))` — die ID wird in Klammern gesetzt.

**Ursache (im Code verifiziert):** der Hint-Text `_TITLE_NOT_ID_HINT`
(`phase2_mcp/mcpserver/tools.py` Z. 159–164) nennt **zwei** Negativ-Beispiele
(plain + Tabellen-Spalte). Klammern sind eine dritte Form, nicht explizit
erwähnt. Das Modell generalisiert nicht von „plain + Tabelle" auf „auch Klammer /
Aufzählung / Inline-Code".

**Entscheidung (Nikinger, AskUserQuestion dieser Session):** A3 wird **nicht**
auf ✅ gehoben, **bleibt 🟡 mit benanntem Defekt**. Der Restdefekt wandert in
den Phase-8-Closeout (`docs/concepts/phase8_ui_graph_plan.md` §9) als benannter
Punkt, wie P7-24 oder P7-4 damals — keine vierte Hint-Iteration, kein
struktureller Eingriff jetzt. Phase 8 macht mit **Block B** weiter
(`storage/linkscan.py` + `item_links`-Tabelle + `GET /api/v1/graph`, achte
P1-Contract-Öffnung, P8-M).

**Was geändert wurde (zwei Stellen, Doku-only):**

1. `phase8_ui_graph/CLAUDE.md` Modul-Status-Tabelle: A3-Zeile von „🟡 gebaut,
   Zweitprobe positiv, dritte Probe offen" auf „🟡 gebaut + deployt, Restdefekt
   Klammer/Aufzählung, wandert in Closeout" präzisiert.
2. `phase8_ui_graph/CLAUDE.md` `updated:`-Zeile vorne: 2026-09-01-Eintrag mit
   dem neuen Sachstand.

**Verifikation:** read-only (`grep` im Release-Verzeichnis + Phase-8-Head-Diff),
kein Code-Change, kein Service-Touch.

**Hard-Rule-Konformität:** Hard Rule 8 — Doc-Update im selben Commit wie die
Statusänderung (Commit dieser Session, ein einziger); Hard Rule 9 — kein
`pkill`/`systemctl` heute.

**Was bewusst NICHT in diesem Commit steht:** ein weiterer Hint-Text-Edit oder
ein struktureller Eingriff (Optionen a/c aus der Frage oben) — Nikinger hat
sich für Option b entschieden (🟡 mit Defekt). Beide bleiben als Referenz im
vorigen Block dokumentiert, falls eine spätere Session sie aufgreifen will.

**Nächster Schritt, konkret:** Phase-8-Head committen + pushen, dann **Block B**
starten (Plan §3, P8-M, N4–N7).

---

## Session stopped — 2026-09-01 (Block B Step B1: `storage/linkscan.py` neu, 15 Tests grün, achte P1-Contract-Öffnung angekündigt)

**Auftrag:** Block B (Plan §3) starten, B1 zuerst (rein-mechanische Erkennung von
`itm_…`-Referenzen in Bodies). Achte P1-Contract-Öffnung (P8-M) **vor** dem Code in
`phase1_storage/CLAUDE.md` §Geerbte Contracts ankündigen (Disziplin der Öffnungen
3–7 — Ankündigung vor Code, Schließung mit Phasenabschluss, nicht mit Teilschritt).

**Was geändert wurde (drei Dateien, 16 insertions / 1 deletion):**

1. `phase1_storage/storage/linkscan.py` (neu, ~40 Zeilen):
   `ITEM_REF_RE = re.compile(r"\bitm_[0-9a-f]{8}\b")` (Alphabet exakt wie `ITEM_ID_RE`
   in `files.py:40` — Wortgrenzen, weil sonst ein `fooitm_deadbeef`-Präfix mitmischen
   würde), `extract_item_refs(body) -> list[str]` (eindeutig, in Auftrittsreihenfolge).
   Rein, kein I/O, deterministisch. Modul-Docstring dokumentiert die stillschweigenden
   Entscheidungen: keine Markdown-Semantik (auch Code-Block-IDs matchen, weil False-
   Positives bei festem 8-Hex-Suffix praktisch ausgeschlossen sind), keine
   `#item/`-Href-Sonderbehandlung (das Präfix enthält das Token ohnehin).

2. `phase1_storage/tests/test_linkscan.py` (neu, 15 Tests): Alphabet-Garantien für
   `ITEM_REF_RE` (lower-hex, 8 Zeichen, Wortgrenzen) plus Verhalten von
   `extract_item_refs` (leer, keine Treffer, naked ID, Href-Form, mehrere IDs in
   Reihenfolge, Dedupe wiederholter IDs, Dedupe über Href+naked, Mixed-Order,
   Code-Block, ungültige Formen, Adjacent-IDs-ohne-Separator). Drei Test-Annahmen
   waren in einem ersten Lauf falsch (Case-Sensitivity, Bindestrich-Wortgrenze,
   Adjacent-IDs-Verhalten) — korrigiert, dokumentiert, kein Code-Re-Do nötig.

3. `phase1_storage/CLAUDE.md` (Geerbte Contracts, neuer Absatz): achte
   P1-Contract-Öffnung **angekündigt**. Wörtlich aus dem Plan zitiert (`P8-M`),
   Tabu-Grenze explizit benannt (`models.py`/`frontmatter.py`/`files.py`/`patch.py`/
   `acl.py`/`history.py` unangetastet — kein Dateiformat, kein Frontmatter-Feld,
   keine neue `Item`-Property), Bedingung dokumentiert (Charakterisierung
   byte-identisch grün vor und nach jeder künftigen `storage/`-Änderung dieser
   Öffnung). Schließung mit Phase-8-Step-Z, nicht mit Teilschritt.

**Verifikation:** `pytest phase1_storage/tests/test_linkscan.py -v` → **15/15 grün**.
Tabu-Diff-Kommando aus Plan §0.4 → **leer** (nur die eine neue Datei plus eine
neue Test-Datei, beides nicht in der Tabu-Liste). `pytest
phase6_shares/tests/test_characterization.py` → **4/4 grün** (Charakterisierung
unverändert, weil B1 nur eine pure Function ist und weder `models.py` noch eine
Schema-Migration anfasst). `pytest phase1_storage/tests/ --collect-only` → **169
Tests** gesamt (vorher 154 + 15 neue, exakt deckungsgleich).

**§0.6 Selbstprüfung:**
1. ✅ `pytest -q` für die berührte Datei grün (15/15). Voller Suite-Lauf wäre für
   B1 Overkill — der Plan kennt keine Migration in B1.
2. ✅ Tabu-Diff leer.
3. ✅ Fehlerpfad: `extract_item_refs` hat keinen Fehlerpfad — `re.finditer` ist
   total, ein `body=None` würde einen `AttributeError` werfen, der aber vom
   Aufrufer (`Store`) nie erreicht wird, weil `Store._item_from_text` den Body
   immer aus `parse_frontmatter(...)` liefert (String, nie `None`).
4. ✅ Keine neue `.md` — Doc-Update nur im Phase-1-Head (Ankündigung) und im
   Phase-8-Head (Modul-Status, `updated:`, dieser Block).
5. ⏭️ `ui_budget.py` entfällt — kein UI-Step.

**Hard-Rule-Konformität:** Hard Rule 8 — Doc-Update im selben Commit (dieser
Commit aktualisiert beide Heads); **Hard Rule 9** (heute eingeführt) — kein
`pkill`/`systemctl` heute; Hard Rule 1 — keine Secrets berührt; Hard Rule 2 —
Index wird nicht angefasst (B1 ist pure Function, B2 fügt die Tabelle hinzu);
Hard Rule 5 — keine Datei geschrieben (nur eine neue Datei + eine neue
Test-Datei, beides `Write`-Tool-Aufrufe, atomar); Tabu-Diff §0.4 leer.

**Was bewusst NICHT in diesem Commit steht:** B2 (`item_links`-Schema +
Schreibpfade in `index.py`/`store.py`), B3 (`GET /api/v1/graph` in
`webui/api.py`), B4 (UI-Anschluss in `app.html`/`app.js`) — eigene Commits,
damit jeder Diff isoliert reviewbar ist und ein möglicher Fehler in einem
späteren Sub-Step nicht den ganzen Block zurückrollt. Geerbte-Contracts-
Absatz bleibt **angekündigt**, **nicht geschlossen** bis Phase-8-Step-Z
(Disziplin der Öffnungen 6/7).

**Nächster Schritt, konkret:** B2 — `item_links`-Tabelle im Index-Schema
(`INDEX_SCHEMA_VERSION = 3`, neue Funktion `replace_item_links()`), Aufrufe
an allen Schreibpfaden in `store.py` (create/update/patch/append/move/
archive), `Store.links_all() -> list[tuple[str, str, str]]` als neue
Lesemethode, Tests für alle sechs Schreibpfade plus Rebuild- und
Entfernen-Verhalten. Hard Rule 2 verlangt einen vollständigen Rebuild aus den
Dateien — `rebuild_index()` muss `item_links` mitschreiben.

---

## Session stopped — 2026-09-01 (Block B Step B2: `item_links`-Tabelle, alle 6 Schreibpfade, 22 Tests, Öffnung bleibt angekündigt)

**Auftrag:** B2 (Plan §3 P8-M, Fortsetzung der achten P1-Contract-Öffnung).
Schema-Migration auf `INDEX_SCHEMA_VERSION = 3`, `item_links`-Tabelle, alle
Schreibpfade im Store rufen `_replace_links_for_item` zentral via
`_write_item_file`, neue Lesemethode `Store.links_all()`.

**Was geändert wurde (fünf Dateien, 543 insertions / 6 deletions):**

1. `phase1_storage/storage/index.py` (94 +/6 −): `INDEX_SCHEMA_VERSION = 3`;
   `_SCHEMA` um `item_links` + `idx_item_links_dst` ergänzt;
   `_open_and_init` von `conn.execute(_SCHEMA)` auf `conn.executescript(_SCHEMA)`
   umgestellt, weil der String jetzt mehrere durch `;` getrennte Anweisungen
   enthält (sonst `sqlite3.ProgrammingError: You can only execute one statement`);
   `row_from_file` gibt `body_refs` als zusätzlichen Dict-Key zurück (additiv,
   `upsert_item` ignoriert es still); `replace_item_links(conn, src_id, rows)`
   und `all_links(conn)` neu; `delete_item` löscht zusätzlich `item_links`-
   Zeilen mit dieser `src_id`; `rebuild_index` leert `item_links` zu Beginn
   und befüllt es pro Datei (Frontmatter + Body).

2. `phase1_storage/storage/store.py` (56 +): `_replace_links_for_item(item)`-
   Helper, der `frontmatter_refs` (aus `item.links` gefiltert durch
   `ITEM_REF_RE.fullmatch`) und `body_refs` (aus `extract_item_refs(item.body)`)
   zusammenführt und `index.replace_item_links(self._conn, item.id, rows)` ruft;
   `_write_item_file` ruft den Helper nach `index.upsert_item(...)` — damit
   deckt jeder Schreibpfad (`create`/`update`/`patch`/`append`/`move`/`archive`)
   genau einmal pro Operation die `item_links`-Tabelle ab, ohne dass jede
   Store-Methode das selbst tun muss; `_reconcile_and_get_row` aktualisiert die
   Tabelle nach einem Drift-Repair (Body vom Menschen editiert); neue
   öffentliche Methode `Store.links_all() -> list[tuple[str, str, str]]`.

3. `phase1_storage/tests/test_item_links.py` (neu, 13 Tests): Schema-Verhalten
   (`replace_item_links` destruktiv/leer/andere-src-Items/same-dst-unterschiedlich-
   kind), `row_from_file` mit Body-Refs (treffer/dedup/leer), `rebuild_index`
   füllt aus Dateien / ignoriert Non-`itm_`-Strings / wipet vollständig /
   akzeptiert dangling dst_id ohne Crash, `delete_item` räumt src-Zeilen, Sortierung
   in `all_links`.

4. `phase1_storage/tests/test_item_links_store.py` (neu, 9 Tests): Store-Integration
   pro Schreibpfad — `create` (Frontmatter+Body), `create` ignoriert Non-`itm_`-
   Strings, `update` ersetzt vollständig, `append` nimmt neue Body-Refs auf,
   `patch` rechnet Body-Links neu, `archive` behält Kanten, `move` lässt Kanten
   unverändert, `rebuild_index` Round-Trip, Drift-Repair über `get()` passt
   Body-Links an.

5. `phase8_ui_graph/CLAUDE.md` (Modul-Status + B1-SHA-Korrektur + dieser Block):
   B1-SHA-Zeile nachgetragen (`ed43ed6`), B2-Zeile neu (`INDEX_SCHEMA_VERSION =
   3`, alle 6 Schreibpfade, 22 Tests, 191 phase1_storage-Tests gesamt).

**Verifikation:** `pytest phase1_storage/` → **191/191 grün** (vorher 154 + 15 B1
+ 13 B2-index + 9 B2-store, exakt deckungsgleich). Tabu-Diff §0.4 → **leer**.
`pytest phase6_shares/tests/test_characterization.py` → **4/4 grün**, byte-identisch.

**§0.6 Selbstprüfung:**
1. ✅ Voller `pytest -q` über alle berührten Module grün (191/191).
2. ✅ Tabu-Diff leer.
3. ✅ Fehlerpfade durchdacht: `replace_item_links` mit leerer Rows-Liste löscht
   sauber (eigener Test); `delete_item` ohne vorhandene `items`-Zeile räumt
   trotzdem `item_links`-src-Zeilen auf (kein FK, dokumentiert im Test);
   dangling `dst_id`s werden nicht zurückgewiesen (Test). Drift-Repair bei
   `_reconcile_and_get_row` deckt den externen Edit-Pfad ab; `repair_drift=False`
   aktualisiert ebenfalls `item_links`, weil die Datei-Realität sich geändert
   hat und der Index ableitet (Hard Rule 2).
4. ✅ Modul-Status-Tabelle + `updated:`-Zeile + dieser Session-Block aktualisiert.
5. ⏭️ `ui_budget.py` entfällt — kein UI-Step.

**Hard-Rule-Konformität:** Hard Rule 1 (keine Secrets), Hard Rule 2 (Index
bleibt vollständig aus Dateien rekonstruierbar, `rebuild_index` löscht
`item_links` und befüllt es neu), Hard Rule 5 (jeder Schreibvorgang erzeugt
genau einen Git-Commit, unverändert), Hard Rule 7 (stderr-only), Hard Rule 8
(Doc-Update im selben Commit, geerbt aus B1-Ankündigung), Hard Rule 9 (kein
`pkill`/`systemctl`).

**Tabu-Grenze gehalten:** außer `linkscan.py` (B1), `index.py` und `store.py`
fasst dieser Commit nichts an. `models.py`, `frontmatter.py`, `files.py`,
`patch.py`, `acl.py`, `history.py` sind alle unverändert — das war die
explizite Auflage der achten P1-Contract-Öffnung (siehe `phase1_storage/
CLAUDE.md` §Geerbte Contracts).

**Öffnung bleibt angekündigt, nicht geschlossen** — die achte Öffnung wird mit
Phase-8-Step-Z geschlossen, nicht mit B2 (Disziplin der Vorgänger-Öffnungen 6
und 7).

**Nächster Schritt, konkret:** B3 — `GET /api/v1/graph` in `webui/api.py`.
Knotenmenge = genau die Items, die `_items_get` im globalen Scope liefern würde
(dieselbe `can_read_item_as_human`-Filterung spiegeln), `status=archived`
draußen, `?archived=1` nimmt sie rein; Kanten aus `Store.links_all()`,
gefiltert auf `src != dst` und beide Endpunkte sichtbar; Tests im
`phase5_ui/tests/test_api.py`. Kein Polling, keine UI-Änderung in B3 — B4 ist
dafür zuständig (`#item/`-Navigation + Link-Picker).
