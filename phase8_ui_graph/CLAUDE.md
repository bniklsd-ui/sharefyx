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
updated: 2026-09-01 (Doku-Session: Hard Rule 9 in Wurzel-CLAUDE.md ergaenzt nach Phase-8-A3-Vorfall -- kein pkill -f mit Regex, niemals den systemd-Dienst anfassen; PROMPTS.md Hard-Rules-Liste und Tests-Absatz um Stopp-Regel fuer Wegwerf-Instanzen erweitert; docs/INDEX.md drei Zeilen vorne + drei Eintraege angepasst; kein Code, kein Service-Touch, Produktion weiterhin active, head 11.6KB->12.8KB unter Softcap) | 2026-09-01 (A3 gebaut -- _TITLE_NOT_ID_HINT mit Positiv/Negativ-Beispiel geschärft, Test test_tool_descriptions_tell_the_agent_to_name_titles_not_ids auf neuen Wortlaut angepasst, 143 phase2_mcp-Tests gruen, Zweitprobe vom Nikinger live bestaetigt (positiv), dritte Probe nach Deploy offen P8-5) | 2026-08-31 (A2 live-verifiziert -- Test_Space_A2 angelegt + entfernt, 4x GET /api/v1/overview nach DELETE=200 statt 500, Index konsistent mit Dateien, Push danach freigegeben; Block A vollstaendig live ✅) | 2026-08-31 (Nachtrag: Janick live angemeldet -- dritter biologischer Nutzer, Phase-4-Auth-Architektur erstmals mit externem Dritt-Anwender durchgespielt; Connector-UI-Befund: 'Anmeldung fehlgeschlagen' trotz erfolgreicher OAuth-Verbindung, kein Handlungsbedarf, Vormerkung fuer spaeter) | 2026-08-31 (Nachtrag: OpenAI-ChatGPT-Konnektor aktuell nicht kompatibel, benoetigte Settings unbekannt -- Auth-Architektur auf Anthropic-Konnektoren geeicht, andere Settings nicht hinterlegt, Vormerkung ohne Auftrag) | 2026-08-31 (Block A: A2 remove-space-Auto-Reindex gebaut -- spacectl._cmd_remove_space nach remove_space_dir mit store.rebuild_index(), Test beweist keine Karteileichen + keine Kollateralschäden, 913 gruen, Live-Verifikation ausstehend) | 2026-08-31 (Block A: A1 Reauth-Grant Client gebaut -- async runBatchMove + Grant-Round-2, test #3 auf N=14, Browser-Smoke gegen Wegwerf bestanden, Head rotiert, Live-Verifikation ausstehend) | 2026-08-28 (Block A gestartet -- A1 Reauth-Grant Backend gebaut, 912 Tests gruen, Plan-Drift session_id->session_hash + Throttle-Vorzug dokumentiert, JS-Client ausstehend) | 2026-08-28 (Nachtrag: websearch-MCP nachgerüstet -- @zhafron/mcp-web-search, kein API-Key, Live-Probe bestanden, V94 von nein auf ja) | 2026-08-28 (Step 0 abgeschlossen -- opencode-ai 1.18.25 global installiert, Minimax-Provider-Auth vom Nikinger gesetzt, Playwright-MCP verbunden (V93), CLAUDE.md-Regeldatei-Kontrollfrage bestanden, Smoke-Test P8-26 auf Wegwerf-Branch bestanden, Harnesswechsel zu opencode/M3 ab Block A freigegeben) | 2026-08-28 (Skelett angelegt, Step 0 Fundament-Session gestartet)
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
| A3 | P7-4: organische Zweitprobe + `_TITLE_NOT_ID_HINT` schärfen | 🟡 gebaut, Zweitprobe positiv (Nikinger live bestätigt 2026-09-01), dritte Probe nach Deploy offen (P8-5) |
| Block B | Link-Fundament (`linkscan.py`, `item_links`, `GET /api/v1/graph`) | ⬜ |
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
