---
status: live
purpose: Archivierte Session-stopped-Blöcke aus phase6_5_tools_images/CLAUDE.md, verbatim, newest-first
read-when: Auditieren der vollen Phase-6.5-Historie — der aktuelle Session-Block lebt im Phase-Head, nicht hier
detail: L3
up: ./CLAUDE.md
down:
updated: 2026-08-20 (erste Rotation -- Step-0-Session-Block verschoben, Head traegt seither den Block-A-Session-Block)
---
# SESSIONS_ARCHIVE.md — Phase 6.5: Werkzeug-Ergonomie und Bilder

Ein Eintrag, newest-first, verbatim aus `phase6_5_tools_images/CLAUDE.md` per
`scripts/rotate_session_block.sh phase6_5_tools_images`.

## Session stopped — 2026-08-20 (Step 0 gestartet)

**Herkunft:** Nikinger bat um eine Opus-Planungssession für die zwei tatsächlich noch offenen
QoS-Punkte (Werkzeug-Ergonomie-Rest, Block C Bilder) — der ursprüngliche Auftragstext listete
daneben drei Dinge als „zwingend", die bereits gebaut waren (`patch_item`, das neue Dateisystem,
Update-Banner); vor dem Start korrigiert, siehe Claude-Code-Session-Transkript. Ergebnis:
`docs/concepts/phase6_5_tools_images_plan.md` (Opus, Hintergrund, ~882s), sechs offene Fragen
N1–N6 (kein `AskUserQuestion` im Subagenten verfügbar).

**Nikinger-Entscheidungen (`AskUserQuestion`, live in der Claude-Code-Session), in Plan §0.0
gelockt:**
- **N1:** Phase **6.5**, nicht 7/8 — sitzt zwischen der gebauten Phase 6 und der reservierten
  Phase 7 (Space-Admin-UI). Keine Kollision mit `app.html`s „kommt in Phase 7"-Zeichenkette, die
  bleibt unangetastet.
- **N2:** Verzeichnis `phase6_5_tools_images/` (dieses hier).
- **N3:** Bulk-Append **nicht** bauen — Befund: heute schon über mehrzeiligen Text in einem
  `append_to_item`-Aufruf möglich, nur ein Beschreibungssatz nötig.
- **N4:** Body-Volltextsuche für die MCP-Fläche **als Opt-in** bauen (`in_body: bool = False`) —
  `Store.search()` lädt jede Datei ohnehin vollständig, kostet nichts zusätzlich. Q1 (Web-UI,
  keine Body-Suche) bleibt unangetastet.
- **N5 (=B5):** Bild entfernen per **Verschieben** nach `_assets/<item_id>/_trash/`, Entscheidung H
  bleibt formal unangetastet. **Nikinger-Vormerkung, kein Auftrag dieser Phase:** `_trash/` wird
  nie automatisch geräumt — anders als kB-große `.md`-Dateien können MB-große Bilder Git-Historie/
  `DATA_ROOT` über Zeit zu GB-Größen aufwachsen lassen. Braucht mittelfristig eine eigene
  operative Lösung (`diagnose.sh`-Meldung ab Schwelle, oder Operator-Purge-Skript analog zum
  Hard-Delete-Muster aus P1 Entscheidung H).
- **N6:** `MAX_MCP_ASSET_BYTES = 1 MiB` für MCP-Uploads (Web-UI bleibt bei 5 MiB, B2) — Nikinger-
  Begründung: Claude wird über MCP nur selbst erzeugte SVGs oder kleine Screenshots hochladen,
  keine großformatigen Fotos.

**Vier der fünf `IMAGES_PLAN.md`-Fragen (B1–B4) waren bereits vorher entschieden** und in den
Planungsauftrag eingearbeitet: B1 Blobs in Git-Historie ja (mit Größenriegel), B2 5 MiB je Bild
(Web-UI), B3 Bildbytes fremder Items nur bei Schreibrecht **und** nie automatisch — auch nicht bei
eigenen Items, nur auf direkte Anfrage, B4 MCP-Upload erlaubt, aber Ankündigungspflicht bei
**jedem** Aufruf (keine Dauererlaubnis).

**Step 0 heute ausgeführt:**
- `pytest`-Baseline real gemessen (nicht nur aus der Doku übernommen): erster Lauf 771 passed/1
  failed (`phase4_auth/tests/test_authctl.py::test_revoke_kills_the_family`), isoliert grün, auf
  einem zweiten vollen Lauf **772/772 grün** — ein reihenfolgeabhängiger Flake, kein durch diese
  Session verursachter Schaden (keine Codeänderung angefasst). Baseline bestätigt: **772**.
- Fünfte Contract-Öffnung angekündigt (`phase1_storage/CLAUDE.md`, siehe „Geerbte Contracts").
- `phase6_shares/IMAGES_PLAN.md` als nachrangig markiert, V-Register-Übernahme (V59–V62 →
  dieselben Nummern im neuen Plan, kein Duplikat) dort explizit vermerkt.
- `ROADMAP.md`: neue Phase-6.5-Sektion ergänzt.
- `docs/INDEX.md`: Eintrag von „Next phase" auf den jetzt existierenden Phase-Head umgestellt.
- `app.html` Z. 281 **nicht** angefasst (N1-Ergebnis macht das unnötig, gegen den echten Code
  verifiziert).

**Offen für die nächste Session:**
- Diesen Session-stopped-Block + `docs/INDEX.md`/`ROADMAP.md` committen (Nikinger-Freigabe
  ausstehend zum Zeitpunkt des Schreibens).
- Step 0 Rest: keiner — alle acht Punkte des Plans sind entweder erledigt oder als „keine Aktion
  nötig" verifiziert (N1/`app.html`).
- Block A (Steps A1–A4) kann direkt beginnen — keine Abhängigkeit von Block B.
- Block B Step B1 (Storage-Fundament) kann beginnen — P6.5-T ist angekündigt.
- **Bekannte Doku-Schuld, nicht in diesem Step behoben:** `phase6_shares/CLAUDE.md` nennt Block C
  weiterhin als „geplant, nicht gebaut (`IMAGES_PLAN.md`, fünf offene B1–B5)" — stale seit der
  heutigen Nachrangig-Markierung von `IMAGES_PLAN.md`. Der Head liegt bei ~40.863 Bytes, ~100
  unter dem Softcap — eine Korrektur dort braucht zuerst eine Rotation
  (`scripts/rotate_session_block.sh`), bewusst nicht in diesem Docs-Commit mitgemacht, um zwei
  unabhängige mechanische Vorgänge nicht zu vermischen. Vor der nächsten Änderung an diesem Head
  einplanen.
- **Bekannter Flake, nicht Scope dieser Phase:** `phase4_auth/tests/test_authctl.py::
  test_revoke_kills_the_family` schlug im ersten vollen `pytest`-Lauf dieser Session fehl,
  isoliert und im Re-Run grün — reihenfolgeabhängig. Vermerkt in `phase4_auth/CLAUDE.md`, damit
  ein künftiges „Subtask nicht grün" nicht neu diagnostiziert werden muss.

