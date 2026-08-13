---
status: live
purpose: Phase-Head Freigaben, Ordner, Werkzeug-Ergonomie — Scope, harte Regeln, Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase6_shares/ oder an den in P6-C genannten Dateien in storage/mcpserver/webui — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase6_shares_plan.md         # voller Plan, Entscheidungen P6-A–P6-AC, Steps 0–10
  - ./ITEM_MOVE_PLAN.md                            # Zusatzplan zu Step 7: Item-Verschieben (Ordner+Space) + Textfarben, P6-AD–P6-AJ
  - ../docs/concepts/PHASE5_CLOSEOUT_HANDOVER.md   # Herkunft der offenen Entscheidungen §4.1–§4.6, [VERIFY]-Bilanz V27–V38
  - ./SESSIONS_ARCHIVE.md                          # Steps 0-6 verbatim (fuenf Eintraege), L3, kein Softcap
updated: 2026-08-13, fuenfter -- (Zusatzplan ITEM_MOVE_PLAN.md geschrieben: Cross-Space-Move + UI + Textfarben; vier Korrekturen an der Planungsvormerkung des vierten Nachtrags; UI-Fund Teil 2 deployed + live bestaetigt, beide Teile geschlossen)
---

# CLAUDE.md — Phase 6: Freigaben, Ordner, Werkzeug-Ergonomie (`phase6_shares/`)

> **Drei Dinge, in dieser Reihenfolge beweisbar:** eine arbeitende Claude-Instanz kann eine
> Drei-Zeilen-Korrektur an einem großen Dokument machen, ohne es komplett neu zu schreiben; ein
> Mensch entscheidet pro Item, wer es sieht, und es gibt Orte, an denen mehrere gemeinsam
> schreiben; das System verträgt einen dritten Nutzer, ohne dass jemand eine Codezeile ändert.
> **Quelle der Wahrheit ist der Code, nicht dieses Dokument.**
> Vollständiges Design + alle 29 gelockten Entscheidungen (P6-A–P6-AC) + Steps 0–10:
> `../docs/concepts/phase6_shares_plan.md`.

## Mission (zuerst lesen)

Diese Phase steht in **keiner** Roadmap-Zeile — sie ist ein QoS-Schnitt aus echtem Betrieb
(`patch_item`-Feedback einer arbeitenden Claude-Instanz, Nikinger-Meldung zu Subspaces/Freigaben).
Drei Blöcke, ein hartes Gate dazwischen: A = Werkzeuge/Betrieb/Update-Banner, B = Dateisystem
(Ordner, Sichtbarkeit, Freigaben, geteilte Spaces), C = Bilder. Unter Druck fällt zuerst C weg,
dann Bs geteilte Spaces — **nie Block A** (P6-A).

## Bauprinzip (Projekt-Kernprinzip)

„Der Server ist dumm." Phase 6 enthält KEINE AI, kein serverseitiges Rendern fremder Bodies,
kein serverseitiges Verarbeiten von Bildern (nur validieren + ausliefern, P5-Y gilt fort).

## Scope (Kurzform, Details: Plan §0.5 P6-A–P6-AC)

- **DRIN:** `patch_item` (punktuelle Textersetzung statt Komplett-Rewrite), Quittungen statt
  Volltext für alle Schreib-Tools, Purge-Erweiterung (O2), Update-Log + Banner, Sichtbarkeitsstufen
  (`private`/`human`), Item- und Ordner-/Space-Freigaben (`.share.yml`, `share_read`/`share_write`),
  echte Ordner (Tiefe ≤2), Migration des Bestands auf `private`, ein dritter Nutzer live bewiesen,
  Bild-Assets (PNG/JPEG/WebP/GIF, Magic Bytes, 5 MiB, kein HEIC), `app.js`-Split ohne Build-Step.
- **DRAUSSEN:** Löschen von Items (bleibt `status: archived`), FastMCP-4/CIMD/DPoP, Volltext-/
  semantische Suche, Realtime/WebSocket, Mobilversion, SQL-Filterung im Store, Rechteverwaltung
  über MCP-Tools, serverseitiges Bild-Rendering/EXIF-Strip, HEIC-Transkodierung.

## Harte Regeln dieser Phase (nicht verhandelbar)

- Alle Hard Rules aus Root-`CLAUDE.md` gelten unverändert.
- **P6-C — Berührungsfläche.** `storage/`, `mcpserver/tools.py`, `mcpserver/permissions.py` sind
  ausdrücklich **auf** — das hebt P5-B auf (P5s Akzeptanzkriterium 18 ist damit gegenstandslos).
  Weiterhin **tabu**: `mcpserver/asgi.py`, `authserver/{crypto,totp,passwords,resolver,flows}.py`
  (Ausnahme: additive Schema-3-Migration, P6-X).
- **P6-D — Ersatz für den Seam-Beweis.** Charakterisierungstests (Golden Files, byte-identisch)
  **vor** jedem Umbau an `storage/`. Kein Step-Abschluss in Block B ohne grüne Charakterisierung.
- **P6-G — kein inhaltsverankerter Merge.** `patch_item` respektiert `version`-Mismatch wie jeder
  andere Schreibpfad — `ConflictError`, ohne Ausnahme, auch wenn alle Anker noch eindeutig wären.
- **P6-M — Freigaben nur durch Menschen.** Kein MCP-Tool kann `share_read`/`share_write`/
  `visibility` setzen. `update_item` lehnt diese Felder mit `ValidationError` ab.
- **Rotationsregel ab Tag 1.** Dieser Head trägt **genau einen** Session-Block. Beim Anlegen
  eines neuen wandert der bisherige **verbatim** nach `SESSIONS_ARCHIVE.md` —
  `scripts/rotate_session_block.sh phase6_shares`, nie von Hand.
- **Commit ⇒ Note-Update, im selben Commit** (Hard Rule 8): Modul-Tabelle unten + Session-Block.

## Die gelockten Entscheidungen (P6-A – P6-AC) — Kurzform (Details: Plan §0.5)

Drei Blöcke, ein hartes Gate, Block A fällt nie (A) · kein neues Python-Paket, `phase6_shares/`
trägt nur `tests`/`scripts`/`CLAUDE.md` (B) · `storage`/`tools.py`/`permissions.py` auf, P5-B
aufgehoben (C) · Charakterisierungstests als Seam-Ersatz (D) · `patch_item(id, version, edits,
return_body=False)`, Liste sequenzieller `{old_text, new_text}` (E) · exakter Byte-Match, kein
Fuzzy (F) · `version`-Mismatch ⇒ `ConflictError`, kein Ausnahme-Merge (G) · alle vier Schreib-Tools
liefern eine kompakte Quittung statt Volltext, `return_body` holt ihn zurück (H) · kein
`section=`-Lesen, stattdessen `ui_budget.py` misst (I) · zwei Sichtbarkeitsstufen `private`/`human`
(J) · Item-Freigaben `share_read`/`share_write` (K) · Bestand wird `private`, Migrationsreport,
Update-Banner vor der Migration (L) · nur Menschen/UI/Re-Auth ändern Freigaben (M) · Re-Auth bei
Erweiterung, nicht bei Rücknahme (N) · `<untrusted_content>` gilt auch für geteilte Spaces (O) ·
`visibility: human` für die Agentenfläche vollständig nicht existent (P) · echte Verzeichnisse,
Tiefe ≤2, `folder` abgeleitet (Q) · Archiv bleibt flach (R) · SQL-Filterung draußen, aber gemessen
(S) · Mitgliedschaft in `.share.yml`, Datei nicht Datenbank (T) · Hard Rule 4 neu gefasst, nur
`create_item` bekommt `space=` (U) · geteilte Spaces per CLI verwaltet, UI gebaut aber abgeschaltet
(V) · dritter Nutzer live angelegt und wieder entfernt (W) · Update-Log strenges Format, `deploy.sh`
bricht ohne aktuellen Eintrag ab (X) · Assets unter `_assets/`, 5 MiB, relative Markdown-Links (Y) ·
PNG/JPEG/WebP/GIF über Magic Bytes, kein HEIC (Z) · Claude referenziert Assets, lädt nicht hoch,
löscht nicht (AA) · Drag & Drop mit Pflicht-Alternative (AB) · `app.js` in ES-Module aufgeteilt,
weiter ohne Build-Step (AC).

## Modul-Status

| # | Modul | Step | Status | Tests |
|---|---|---|---|---|
| 1 | Haushalt, Verifikationsdurchlauf (V39/V40/V41), Regeländerungen (§0.7 a/b/c), Phase-Head angelegt | 0 | ✅ **vollständig** | 0 (bewusst — reines Skelett, wie P1 Step 0; `phase6_shares/tests/conftest.py` leer angelegt) |
| 2 | Werkzeug-Ergonomie: `storage/patch.py` (neu), `storage/store.py :: patch()`, `mcpserver/receipts.py` (neu), siebtes Tool `patch_item`, `return_body` an allen vier Schreib-Tools, `update_item` lehnt `visibility`/`share_read`/`share_write` ab | 1 | ✅ **vollständig** — `mcp_smoke.py` 13/13 grün | +17 (5 `phase6_shares/tests/test_patch.py`, neue Datei + 5 `phase1_storage/tests/test_store.py` + 7 `phase2_mcp/tests/test_tools.py`); 593 gesamt |
| 3 | Betrieb: O2 (`authserver/store.py :: purge_expired()` räumt `token_families`/`clients` ab, zwei neue Retention-Konstanten), Client-Surface-Logging (`ua`-Feld auf `AccessLogASGI`, **V42 geschlossen, 2026-08-12** — Befund unten), `diagnose.sh` Prüfung 11 (Purge-Frische, INFO), `ui_budget.py :: _measure_latency()` (P6-I/P6-S, eigene `LatencyMetric`, kein Exit-Code-Einfluss) | 2 | ✅ **gebaut, ein Live-Teil beim Nikinger** — Gate-A→B-Punkt 3 (realer Purge-Lauf, `clients`-Zeilenzahl sinkt) bleibt live-Aufgabe, frühestens 2026-08-28 | +11 (8 `phase4_auth/tests/test_authserver_store.py` + 2 `phase2_mcp/tests/test_request_log.py` + 1 `phase2_mcp/tests/test_logging.py`); 604 gesamt |
| 4 | Update-Log und Banner: `authserver/store.py` Schema 3 (`users.seen_update_id`), `webui/updates.py` (neu, Parser), `webui/api.py` (+`GET /api/v1/updates`, +`POST /api/v1/updates/seen`), `webui/static/js/updates.js` (neu, Banner + Konto-Dialog-Link), `app.html`/`app.css`, `deploy.sh`-Gate (P6-X), `docs/UPDATE_LOG.md` (neu, erster Eintrag) | 3 | ✅ **gebaut, Gate-A→B-Punkt 4 vollständig live bestanden** (Banner-Hälfte 2026-08-10, Fabian-Hälfte 2026-08-11, siehe Session-Block) | +16 (3 `phase4_auth/tests/test_authserver_store.py` [258→261] + 7 `phase6_shares/tests/test_updates.py` [neue Datei] + 2 `phase5_ui/tests/test_api.py` + 3 `phase5_ui/tests/test_deploy_scripts.py` + 1 `phase5_ui/tests/test_static_routes.py`); 620 gesamt |
| 5 | Storage-Fundament (Block B): Charakterisierungstests + Goldens zuerst (P6-D), `storage/acl.py` (neu), `models.py`/`files.py`/`index.py`/`store.py`-Erweiterung (`folder`/`visibility`/`share_*`, `acl_of()`, `list_spaces()`), `index.py`-Rebuild-Fix (V46), zweiter Advisor-Durchlauf: `folder` jetzt pfadabgeleitet statt indexvertraut | 4 | ✅ **gebaut, 2026-08-12** — Charakterisierung vor+nach byte-identisch grün, DoD aus Plan §4 Step 4 erfüllt; noch nicht live geprüft (kein eigener Abnahmematrix-Punkt für diesen Step) | +36 `phase1_storage/` (1 `test_models.py` + 11 `test_files.py` + 4 `test_index.py` + 20 `test_store.py`) + 10 `phase6_shares/tests/test_acl.py`; 671 gesamt |
| 6 | Rechtepolitik (Block B): `storage/acl.py` +`grants_for_space()`/`decision_for()`, `store.py` +`acl_reader`-Property (kleine, dokumentierte Erweiterung über Step 5s Dateiliste hinaus), `mcpserver/permissions.py` (`Surface`, `SharePolicy` ersetzt `OwnSpaceWritable`), `mcpserver/app.py` (Verdrahtung über `store.acl_reader`), `mcpserver/tools.py` (alle sieben Tools auf `acl_of()`+`can_read_item`/`can_write_item` umgestellt, `search_items`/`list_spaces` item-weise statt space-weise gefiltert, `create_item(space=, folder=)`, `update_item(folder=)`), `webui/api.py`+`serializers.py` (dieselbe Umstellung, `Surface.HUMAN` über `SharePolicy.can_read_item_as_human()`/`can_write_item_as_human()` gekapselt — P5-B erlaubt weiterhin nur ein `mcpserver`-Symbol) | 5 | ✅ **gebaut, 2026-08-12** — DoD aus Plan §4 Step 5 erfüllt, alle 12 Pflichttests + Fail-Closed-Folder-Fund + `can_write_item`-visibility-Fix (Advisor-Fund nach dem ersten Commit) abgedeckt; noch nicht live geprüft (kein eigener Abnahmematrix-Punkt) | +10 `phase2_mcp/tests/test_tools.py` (30→40) + 9 `test_permissions.py` (3→12, Datei vollständig neu geschrieben) + 2 `phase5_ui/tests/test_api.py` (27→29) + 2 `test_serializers.py` (7→9), Kollateralkorrekturen in `phase2_mcp/tests/test_app.py`/`phase5_ui/tests/test_overview.py`/conftest-Fixtures (keine neuen Tests, nur Assertions auf die neue ACL nachgezogen); 694 gesamt |
| 7 | Verwaltung und Migration (Block B): `phase6_shares/scripts/spacectl.py` (neu — `create-space`/`list-spaces`/`show`/`add-member`/`remove-member`/`remove-space`/`check`), `phase6_shares/scripts/migrate_visibility.py` (neu — `--dry-run` Default, **kein** Versionssprung), `phase3_edge/scripts/diagnose.sh` Prüfung 12 (verwaiste/kaputte `.share.yml`-Referenzen über `spacectl.py check --json`, INFO/WARNUNG, kein Abbruchkriterium) | 6 | ✅ **gebaut, 2026-08-12** — Details, beide Plan-Abweichungen (DATA_ROOT-Auflösung, kein Index-Rebuild) und die Advisor-Runde davor: Session-Block unten. DoD-Live-Teil (realer dritter Nutzer, echter `diagnose.sh`-Lauf) bleibt Nikinger-Sache wie bei Steps 4/5 | +28 (20 `phase6_shares/tests/test_spacectl.py` [neu] + 8 `test_migrate_visibility.py` [neu]); 722 gesamt |

## Geerbte Contracts

**[2026-08-09, P6 Step 0] Dritte, benannte Öffnung des P1-Contracts** (Plan §1.4): `models.py`
bekommt `folder`/`visibility`/`share_read`/`share_write`, `store.py` bekommt `acl_of()`/`patch()`/
erweiterte `create()`/`update()`/`search()`/`list_spaces()`. Wird in Step 4 umgesetzt, hier nur
angekündigt — nach Phasenabschluss (Step 10) wieder geschlossen, siehe `phase1_storage/CLAUDE.md`.

---

## Session stopped — 2026-08-13, fünfter — (Planungssession: `ITEM_MOVE_PLAN.md`, keine Code-Änderung)

**Auftrag:** Nikinger — die Planungsvormerkung des vorigen Blocks zu einem ausführungsreifen Plan
ausbauen, **inklusive** der UI-Bedienung zum Verschieben (geteilte Spaces über die UI anlegen
ausdrücklich **nicht**, P6-V bleibt), plus ein gemeldeter Lesbarkeitsdefekt („der graue Text ist
nicht gut lesbar"). Ablage als persistente Notiz im Phasenverzeichnis mit semantischer Verknüpfung
zum Hauptplan. Reine Doku-Session — kein Code angefasst, `git diff` außerhalb `.md` leer.

**Ergebnis: `phase6_shares/ITEM_MOVE_PLAN.md` (neu, 27 KB).** Entscheidungen **P6-AD–P6-AJ**
(Fortsetzung der Hauptplan-Nummerierung, die bei P6-AC endet), drei unabhängig lieferbare
Schnitte — **Step 7a** (Textfarben, jederzeit lieferbar) · **Step 7** (unverändert, Hauptplan) ·
**Step 7b** (Cross-Space-Move, setzt Step 7 voraus) —, Abnahmezeilen **25–30**, `[VERIFY]`
**V52–V55**, Nebenbefunde **O6/O7**. Verknüpfung im Hauptplan an zwei Stellen (`down:`-Eintrag der
Header-Card + datierter Hinweiskasten direkt über Step 7); der 📕-Snapshot bleibt inhaltlich
unverändert — dieselbe Behandlung wie die Korrekturnotiz in `P2_ADAPTER_ABNAHME_2026-07-26.md`.

**Vier Korrekturen an der Planungsvormerkung des vorigen Blocks** (dort steht „geprüft und
bestätigt fehlend auf allen drei Schichten" — gegen den Code nachgeprüft ist das so nicht haltbar;
der alte Text bleibt im Archiv verbatim stehen, dies ist die datierte Ersetzung):
1. **`Store.update(folder=…)` verschiebt real** und ist seit Step 4 gebaut (`store.py:475-480`,
   `_write_item_file():285-286`). Probelauf gegen ein Wegwerf-`DATA_ROOT`: die Datei landet unter
   `niklas/projekte/alpha/…md`; Tiefe > 2 und reservierte Namen werfen `ValidationError`. Auch
   `mcpserver/tools.py :: update_item(folder=)` und `webui/api.py :: _items_patch` können es,
   beide mit dem Eigentümer-only-Riegel vom 2026-08-12.
2. **`Store.update(space=…)` scheitert laut, nicht still** — `space` steht in
   `_SYSTEM_MANAGED_FIELDS` (`store.py:43`), `ValidationError: Feld 'space' ist vom Store
   verwaltet`. Der „still als Extra-Feld"-Effekt existiert, betrifft aber nur echte Tippfehler
   (`spce=…`), nicht `space` — festgehalten als **O6**, und der Grund, warum `move()` eine
   benannte Signatur statt `**changes` bekommt.
3. **Die UI kennt keine echten Ordner.** `app.js :: renderFolders()` rendert die vier Buckets,
   nicht Verzeichnisse; `GET /api/v1/overview` liefert gar kein `folders`-Feld (nur
   `/api/v1/spaces` tut das, und den benutzt der Baum nicht). Der fehlende Verschieben-Knopf ist
   ein Symptom, nicht die Ursache.
4. **Menschen können nicht einmal in einen Ordner anlegen** — `_items_post`s Feld-Whitelist
   (`api.py:343`) kennt `folder` nicht, `create_item(folder=)` über MCP schon. Die Agentenfläche
   kann seit Step 5 etwas, das die Menschenfläche nicht kann; im Zusatzplan als K4 mitgeschnitten.

**Der Fund, der Step 7b klein macht:** `_write_item_file()` berechnet den Zielpfad aus
`item.space` **und** `item.folder` — es hat nur nie ein `Item` mit geändertem `space` gesehen.
Simuliert (Wegwerf-`DATA_ROOT`, `replace(item, space="fabian")` + der bestehende Pfad): Datei
liegt danach unter `fabian/`, Frontmatter-`space:` ist mitgezogen, `get()`/`acl_of()`/`search()`
konsistent, **ein** Git-Commit (`move itm_… [fabian]`) mit von Git erkanntem Rename
(`{niklas/alt => fabian}/…`). Der Storage-Anteil von Step 7b ist damit eine öffentliche Methode um
bereits funktionierende Mechanik, kein neuer Schreibpfad. Zweiter Nebenbefund aus denselben
Läufen: **O7** — leer gewordene Quellordner bleiben liegen und erscheinen weiter in
`list_spaces().folders` (reiner Verzeichnis-Walk), was der Baum aus Step 7 als Geisterordner
zeigen würde; Behandlung als P6-AF im Zusatzplan.

**Nikinger-Entscheidung dieser Session (Grautext, per Frage gestellt statt geraten):** gemessen
sind es zwei Token, nicht eines — `--text-muted` (#9AA6B4, 19 Stellen) besteht WCAG AA bereits
(6.6–7.9:1), `--text-faint` (#64707E, 16 Stellen) fällt mit **3.2–3.9:1** durch. Gewählt:
**kalibriert anheben** (`--text-muted` → `#C4CDD8`, `--text-faint` → `#A7B2BF`) **plus ein neues
`--text-placeholder` (#7E8A98)** für `.input::placeholder`. Die wörtliche Fassung „alles auf
`--text`" hätte leere Eingabefelder wie gefüllte aussehen lassen und das absichtlich leise
Versionsband (Designsystem §4.4) so laut wie den Titel gemacht. Umsetzung ist Step 7a, **noch
nicht gebaut**.

**UI-Fund aus dem vorigen Block vollständig geschlossen:** der `activeSpaceWritable()`-Fix (Teil 2)
ist deployed und vom Nikinger per **manuellem UI-Test im Browser** validiert. Read-only
gegengeprüft statt die Meldung übernommen: `/opt/sharefyx/current` → Release
`20260813T120925.743482Z`, Arbeitsstand `92b918b` — derselbe Commit, der den Fix enthält, und
identisch mit dem lokalen `main`-HEAD; `docs/UPDATE_LOG.md` trägt dafür einen echten, heute
datierten Eintrag („hotfixed Rechte für shared space"), das `deploy.sh`-Gate (P6-X) ist also
regulär gelaufen, nicht per Override. **Beide Teile des UI-Funds sind live bestätigt.**

**Rotation in dieser Session ausgeführt:** der Head hatte mit diesem Block 40,2 KB erreicht und
damit den 40-KB-Softcap gerissen. Der vorige Block (2026-08-12, dritter, mit vier Nachträgen)
ist über `scripts/rotate_session_block.sh phase6_shares` **verbatim** nach `SESSIONS_ARCHIVE.md`
gewandert — nicht von Hand, nicht abgetippt. Die dort eingefügte Korrekturnotiz zum
deployten UI-Fix ist mitgewandert und steht damit an der Aussage, die sie korrigiert.

**Verifiziert:** kein Code geändert, `pytest -q` trotzdem zweimal als Regressionsprobe gefahren →
**724 passed**, unverändert. `git status --short` zeigt ausschließlich `.md`-Dateien. Die Belege
dieser Session sind drei Probeläufe gegen Wegwerf-`DATA_ROOT`s im Scratchpad (nie gegen den echten
`DATA_ROOT`, Hard Rule) und ein selbst geschriebener WCAG-Kontrastrechner; alle Ergebnisse stehen
im Zusatzplan §1.3/§3.1, keiner davon ist ein Repo-Artefakt geworden. **Der Advisor war in dieser
Session nicht verfügbar** (nicht in der Tool-Liste) — statt eines Advisor-Durchlaufs wurde jede
Behauptung des Plans einzeln gegen den Code oder einen Probelauf gestellt; das ist ein Ersatz,
kein Gleichwertiger, und beim nächsten substanziellen Commit nachzuholen.

**Nächster Schritt (konkret):** `ITEM_MOVE_PLAN.md` vom Nikinger freigeben lassen — damit sind
P6-AD–P6-AJ gelockt. Danach ist **Step 7a** (vier CSS-Token-Zeilen + eine Regel in `app.css`)
sofort und unabhängig lieferbar und derzeit der einzige noch nicht deployte UI-Rest; ein eigener
kleiner Deploy dafür ist die realistische Form. **Step 7** (UI Dateisystem, `app.js`-Split,
Freigabedialog, Ordnerbaum) bleibt der nächste große Schnitt, **Step 7b** setzt ihn voraus.
Gate-A→B-Punkt 3 unverändert offen (realer Purge-Lauf, frühestens 2026-08-28).
