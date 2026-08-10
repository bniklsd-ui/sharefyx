---
status: live
purpose: Phase-Head Freigaben, Ordner, Werkzeug-Ergonomie — Scope, harte Regeln, Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase6_shares/ oder an den in P6-C genannten Dateien in storage/mcpserver/webui — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase6_shares_plan.md         # voller Plan, Entscheidungen P6-A–P6-AC, Steps 0–10
  - ../docs/concepts/PHASE5_CLOSEOUT_HANDOVER.md   # Herkunft der offenen Entscheidungen §4.1–§4.6, [VERIFY]-Bilanz V27–V38
updated: 2026-08-09 (Step 3 — Update-Log und Banner, Block A vollständig gebaut)
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
| 3 | Betrieb: O2 (`authserver/store.py :: purge_expired()` räumt `token_families`/`clients` ab, zwei neue Retention-Konstanten), Client-Surface-Logging (`ua`-Feld auf `AccessLogASGI`, V42), `diagnose.sh` Prüfung 11 (Purge-Frische, INFO), `ui_budget.py :: _measure_latency()` (P6-I/P6-S, eigene `LatencyMetric`, kein Exit-Code-Einfluss) | 2 | ✅ **gebaut, Live-Teile beim Nikinger** — V42 (echtes journald, zwei Tage) und Gate-A→B-Punkt 3 (realer Purge-Lauf, `clients`-Zeilenzahl sinkt) sind live-Aufgaben, nicht in dieser Session baubar | +11 (8 `phase4_auth/tests/test_authserver_store.py` + 2 `phase2_mcp/tests/test_request_log.py` + 1 `phase2_mcp/tests/test_logging.py`); 604 gesamt |
| 4 | Update-Log und Banner: `authserver/store.py` Schema 3 (`users.seen_update_id`), `webui/updates.py` (neu, Parser), `webui/api.py` (+`GET /api/v1/updates`, +`POST /api/v1/updates/seen`), `webui/static/js/updates.js` (neu, Banner + Konto-Dialog-Link), `app.html`/`app.css`, `deploy.sh`-Gate (P6-X), `docs/UPDATE_LOG.md` (neu, erster Eintrag) | 3 | ✅ **gebaut, Live-Teile beim Nikinger** — Gate-A→B-Punkt 4 (Banner im echten Browser, Fabian hat den Eintrag gesehen) ist live-Aufgabe | +16 (3 `phase4_auth/tests/test_authserver_store.py` [258→261] + 7 `phase6_shares/tests/test_updates.py` [neue Datei] + 2 `phase5_ui/tests/test_api.py` + 3 `phase5_ui/tests/test_deploy_scripts.py` + 1 `phase5_ui/tests/test_static_routes.py`); 620 gesamt |

## Geerbte Contracts

**[2026-08-09, P6 Step 0] Dritte, benannte Öffnung des P1-Contracts** (Plan §1.4): `models.py`
bekommt `folder`/`visibility`/`share_read`/`share_write`, `store.py` bekommt `acl_of()`/`patch()`/
erweiterte `create()`/`update()`/`search()`/`list_spaces()`. Wird in Step 4 umgesetzt, hier nur
angekündigt — nach Phasenabschluss (Step 10) wieder geschlossen, siehe `phase1_storage/CLAUDE.md`.

---

## Session stopped — 2026-08-09 (Step 0 — Haushalt, Verifikation, Regeländerungen)

**Auftrag:** Nikinger startete Phase 6 direkt in Claude Code (kein Browser-Planungsauftrag nötig —
`docs/concepts/phase6_shares_plan.md` lag bereits ausführungsreif und untracked im Repo, aus einer
Browser-Planungssession vom selben Tag gegen den Drive-Snapshot `2026_08_09_sharefyx-main`
geschrieben). Gearbeitet wurde Plan §4 Step 0, Punkte 1–6.

**Verifikationsdurchlauf (Plan-Punkt 1):**
- `pytest -q`: **576 passed** — deckt sich exakt mit der Plan-Behauptung. **V39 geschlossen.**
- `git status`: sauber bis auf das untracked `docs/concepts/phase6_shares_plan.md` (jetzt
  hinzugefügt). `HEAD` == `origin/main` (5524a42) — Push-Stand sauber.
- `find . -name "*.md" -size +40k`: keine neuen Treffer durch diesen Commit; bestehende Treffer
  sind bereits 📕/📦 (unverändert seit P5).
- `up:`/`down:`-Links: alle in diesem Commit neu gesetzten (`phase6_shares/CLAUDE.md` ↔
  `docs/concepts/phase6_shares_plan.md`, `docs/INDEX.md`-Zeilen) lösen auf.

**V40 — CVE-2026-48710 („BadHost"):** `pip show starlette` → **1.3.1**, ≥ 1.0.1. **Nicht
betroffen, geprüft-in-Ordnung.** Kein Pin-Update nötig, kein Befund S11.

**V41 — Anthropic-Connector-Doku (Nachfolger V33, seit P4 Step 0 mehrfach durchgereicht ohne
Bearbeitung — siehe `PHASE5_CLOSEOUT_HANDOVER.md` V33-Zeile):** **Diesmal tatsächlich gelesen**,
und zwar die richtige Fläche — dieses Projekt nutzt **Custom Connectors auf claude.ai/Desktop**
(R2), nicht die API-seitige `mcp_servers`/`mcp_toolset`-Fläche. `support.claude.com/en/articles/
11175166` (Custom-Connector-Guide) **nennt keine** Grenze für Tool-Anzahl, Beschreibungslänge oder
Schemaform — auch nichts zu Array-of-Objects-Parametern (relevant für `patch_item`s
`edits: list[TypedDict]`, Step 1). Zwei Drittquellen (sunpeak.ai, startdebugging.net, zur API-
Fläche, nicht zu Custom Connectors) behaupten ein 2KB-Deskriptionslimit bzw. Genauigkeitsverlust
ab 30–50 Tools — **unbestätigt für diese Fläche, nicht übernommen**, nur als Kontext notiert.
sechs → sieben Tools bleibt so oder so weit im unauffälligen Bereich. **V41 geschlossen**, echtes
Schemaform-Verhalten (`list[TypedDict]` durch `fastmcp` 3.4.x) bleibt V48, Step 1, empirisch zu
prüfen.

**Regeländerungen §0.7:**
- **(a) Hard Rule 4** in Root-`CLAUDE.md` neu gefasst, alter Wortlaut durchgestrichen stehen
  gelassen. **Zusatz gegenüber dem Plantext:** ein Satz, dass die neue Regel **erst mit Step 5**
  scharf wird (`.share.yml`/`share_write`/`SharePolicy` existieren vor Step 4/5 nicht im Code) —
  bis dahin gilt faktisch weiter die durchgestrichene Fassung. Reiner Zusatz, ändert die gelockte
  Formulierung nicht. Der `<untrusted_content>`-Satz der alten Regel bleibt **unverändert aktuell**
  (P6-O bestätigt ihn), nur der Cross-Space-Write-Satz wird ersetzt.
- **(b) `ROADMAP.md`:** neue P6-Zeile (🔄) plus datierte Korrekturen an „Feingranulare Rechte" und
  „Mehrmandantenfähigkeit" unter „Bewusst nicht auf der Roadmap".
- **(c) Handover §4.5:** der Plan-Widerspruch (P5 Step 9 „frische Einladung" vs. Plan §2.6 „reine
  Credential-Migration") wird hier festgehalten, nicht im 📕-Snapshot `phase5_ui_plan.md`:
  **gelebt wurde der Step-9-Weg** (frische Einladung). Damit geschlossen.

**V37 (Plan-Punkt 6) — „Exakte Abschnittsüberschriften in `docs/INDEX.md`":** laut
`PHASE5_CLOSEOUT_HANDOVER.md` (📕, nicht editierbar) „faktisch erledigt, nie explizit vermerkt".
**Hier formal abgehakt:** die Active-phase-Überschrift folgt in diesem Commit wieder demselben
Muster (`## Active phase (6 — …)`), wie es P5 in Step 0 anlegte.

**Minor Drift, inline korrigiert (kein Nikinger-Entscheid nötig):**
- `pytest.ini`s `testpaths` nennt Verzeichnisse explizit (kein Glob) — der Plan erwähnt das
  Nachziehen nirgends. `phase6_shares/tests` ergänzt, sonst würde Step 1 seine eigenen Tests nie
  einsammeln.
- Plan-Punkt 5 wollte `docs/INDEX.md` in diesem Commit auch um eine Zeile für `docs/UPDATE_LOG.md`
  ergänzen — diese Datei existiert erst ab Step 3. INDEX' eigene Regel („neue `.md` ⇒ Zeile im
  selben Commit") verbietet das Vorgreifen. Verschoben auf Step 3.
- `phase6_shares/tests/conftest.py` bewusst leer angelegt (P1-Step-0-Präzedenzfall: „Step 0 hat
  bewusst keine Tests, reines Skelett" — `phase1_storage/tests/conftest.py` ist bis heute leer).
- Plan-Punkt 5 nennt auch `scripts/` als Step-0-Deliverable. Git verfolgt keine leeren
  Verzeichnisse, und der erste reale Inhalt (`spacectl.py`/`migrate_visibility.py`) entsteht laut
  Plan erst in Step 6 — `scripts/` entsteht implizit mit der ersten Datei dort, nicht als leerer
  Platzhalter in diesem Commit.

**Phase-Head angelegt** (dieses Dokument), `docs/INDEX.md` um Plan + Phase-Head ergänzt, Root-
`CLAUDE.md`s „Current state" auf 🔄 Phase 6 gestellt.

**Verifiziert:** `pytest -q` nach allen Änderungen erneut grün (siehe Verifikations-Task, Ergebnis
oben) — Änderungen dieser Session sind ausschließlich Dokumentation + eine leere `conftest.py` +
eine `pytest.ini`-Zeile, kein Feature-Code.

**Nachtrag, 2026-08-09, zweiter — Advisor-Review vor Sessionende, vier Funde behoben** (Kurzform,
settled): `docs/INDEX.md`s `ROADMAP.md`-Zeile war stale, korrigiert; Vollständigkeitsprüfung
„jede `.md` hat eine INDEX-Zeile" nachgeholt, alle 32 verlinkt; Staleness-Grep über
`README.md`/`AGENTS.md`/`docs/PROMPTS.md`/`phase5_ui/CLAUDE.md` — keine weiteren Funde;
`ROADMAP.md`s „Mehrmandantenfähigkeit"-Absatz hatte sich selbst widersprochen, korrigiert.
`pytest -q` → 576/576, Size-Sweep sauber.

**Nachtrag, 2026-08-09, dritter — Step 1 (Werkzeug-Ergonomie) fertig** (Kurzform, settled):
`storage/patch.py` (neu: `TextEdit`/`PatchError`/`PatchResult`/`apply_edits()`), `Store.patch()`,
`mcpserver/receipts.py` (neu), siebtes Tool `patch_item`, `return_body` an allen vier
Schreib-Tools, `update_item` lehnt `visibility`/`share_read`/`share_write` ab. `mcp_smoke.py`
13/13. **V48 geschlossen:** `list[TypedDict]` rendert per `fastmcp` 3.4.4 zu einem brauchbaren
Schema, kein Fallback nötig — belegt über den echten `fastmcp.Client`. Drei Advisor-Funde vor
dem Commit: Kollateralschaden durch Quittungen-als-Default (sieben Tests auf JSON umgestellt),
`update_item`s Riegel war ohne die drei echten Parameter wirkungslos (ergänzt, `fastmcp` hätte
sonst vorher abgelehnt), Plan-Testdateinamen wären fixture-los gewesen (Fixtures folgen §5s
Tabelle, nicht dem Fließtext). Kleine Quittungs-Abweichungen von Plan §1.5.3 dokumentiert:
kein `folder` vor Step 4, Archivieren liefert `op="update"` nicht `op="archive"`. `pytest -q` →
**593 passed** (+17: 5 `test_patch.py` + 5 `test_store.py` + 7 `test_tools.py`). Tabu-Diff
gewahrt: nur `storage/`, `mcpserver/{tools,receipts}.py`, drei Testdateien.

**Nachtrag, 2026-08-09, vierter — zweiter Advisor-Durchlauf, zwei Funde vor Sessionende
behoben:** (1) Hard Rule 8 verlangte `phase1_storage/CLAUDE.md` und `phase2_mcp/CLAUDE.md` im
**selben** Commit wie `storage/patch.py`/`tools.py` — waren stattdessen einen Commit zu spät
nachgezogen. Beide jetzt aktuell: Modul-Status-Zeilen (P6 Step 1 als Zeile 9 je Paket),
Testzahlen 81/92 (`pytest --collect-only -q` nachgezählt), `phase2_mcp/CLAUDE.md`s P2-K-
Entscheidung („kein siebtes Tool") mit datierter Korrektur versehen, dritte Contract-Öffnung in
`phase1_storage/CLAUDE.md` dokumentiert. (2) `test_patch_creates_exactly_one_git_commit` prüfte
`len(log) == 2` (absolute Commitzahl im ganzen Test-Repo) statt das Delta — wäre auch bei einem
Bug in `create()`s Commit-Anzahl grün geblieben. Auf Vorher/Nachher-Differenz umgestellt. 593/593
weiterhin grün, eigener Commit (nicht `--amend`).

**Nachtrag, 2026-08-09, fünfter — Step 2 (Betrieb) fertig, in derselben Sitzung fortgesetzt.**
Plan §4 Step 2 (`docs/concepts/phase6_shares_plan.md:694-709`) ist der einzige Block-A-Step ohne
DoD/Testliste im Plandokument — vier Prosa-Punkte, keine Spezifikation. Zwei Advisor-Pässe vor
bzw. nach der Umsetzung eingeholt (Details unten je Punkt und im Verifiziert-Absatz); die
Ausführungsplanung selbst lag nur als Session-lokale Skizze vor und ist hier vollständig
nacherzählt, kein separates Dokument im Repo.

**1. O2** — `authserver/store.py :: purge_expired()` räumt jetzt auch `token_families` (tot =
nach dem bestehenden Ablauf-Sweep keine Kind-Zeile mehr in `access_tokens`/`refresh_tokens`/
`auth_codes` — deckt widerrufen, natürlich abgelaufen UND abgebrochene Autorisierung mit einem
Prädikat ab, letzteres nennt der Plan-Text nicht explizit, bewusste Erweiterung) und `clients`
(kein verbleibender `token_families`-Eintrag) ab, je mit eigener Altersgrenze:
`TOKEN_FAMILY_RETENTION_S` (30 Tage) und **länger** `CLIENT_RETENTION_S` (90 Tage) — eine
`clients`-Zeile ist die Registrierung, die ein Connector im Claude-Account weiter vorzeigt, und
P5-Q widerruft bei einem Passwortwechsel sofort alle Familien; zu kurze Client-Retention riskiert
„unknown client" beim nächsten Autorisierungsversuch statt eines einfachen Re-Auth. `NOT EXISTS`
statt `NOT IN` (immun gegen NULL-in-Subquery, auch wenn die FK-Spalten heute `NOT NULL` sind).
Reihenfolge zwingend wegen `PRAGMA foreign_keys=ON` (store.py:218): Familien zuerst, dann
Clients, in derselben Transaktion. Die 30-Tage-Grenze zählt ab `COALESCE(revoked_at,
created_at)`, nicht ab `created_at` allein — **zweiter Advisor-Durchlauf, echter Fund vor dem
Commit:** eine per Replay-Erkennung getötete Familie (der Härtetest aus der Phase-4-Mission,
`revoked_reason='refresh_replay'`) wäre unter der `created_at`-only-Fassung binnen 24h wieder
verschwunden, wenn sie schon Wochen alt war — ihr einziger forensischer Beleg gelöscht statt 30
Tage aufbewahrt. `ui_sessions`/`invites` daneben zählten schon immer richtig ab ihrem Ereignis;
`token_families` war beim ersten Entwurf die Ausnahme, jetzt korrigiert, mit eigenem
Regressionstest (`test_purge_expired_keeps_a_family_revoked_today_even_if_born_long_ago`).
+8 Tests in `test_authserver_store.py` (250→258).

**2. Client-Surface-Logging (`ua`, V42)** — landet ausschließlich auf `AccessLogASGI`s
`ev="http"`-Zeile (`_ALLOWED_FIELDS` + 120-Zeichen-Kürzung), nicht auf `ev="tool"`:
`ToolCallLogMiddleware` hat keinen ASGI-Scope-Zugriff, `context.py` steht nicht auf Step 2s
Berührungsliste. Geteilter Zeitstempel mit der `ev="tool"`-Zeile reicht für V42 (welche
Oberfläche stellte diese Anfrage). Verifiziert (nicht nur vom Advisor vermutet):
`TokenScrubbingFilter` (`logging_setup.py:65-77`) scrubbt Dict-**Werte** vor dem Formatter, ist
am `sharefyx.request`-Handler angeschlagen (`_configure_request_logger`) — `ua` bekommt beide
Verteidigungen (Kürzung + Muster-Scrub), nicht nur eine. +3 Tests (`test_request_log.py` 11→13,
`test_logging.py` 8→9).

**3. `diagnose.sh`** — Prüfung 11, INFO-Kategorie (kein `diagnose()`-Abbruch, gleiche Einordnung
wie die Backup-Frische-Prüfung direkt daneben): Alter von `sharefyx-purge.timer`s letztem Lauf
über `systemctl show ... --property=LastTriggerUSec`, WARNUNG mit Enable-Befehl falls nie
gelaufen, sonst WARNUNG ab > 48h. Der zweite Plan-Punkt (verwaiste Space-Namen in `.share.yml`)
bewusst nicht gebaut — die Datei existiert erst ab Step 4, der Plan selbst nennt das „ab Block
B". Kein Unit-Test (Skript hat wie der Rest von `diagnose.sh` keine automatisierten Tests) —
**aber real gegen den echten, auf dieser Maschine laufenden `sharefyx-purge.timer` geprüft**
(Advisor-Vorgabe, zweiter Durchlauf: `bash -n` beweist nur Syntax, nicht Ausgabeformat, genau der
Fehler hinter V13 „Ausgabeformat nie live geprüft"). Diese Session lief zufällig direkt auf der
Heim-VM (bestätigt über `hostname`/`DATA_ROOT`/`systemctl is-active sharefyx-mcp`, siehe
Projekt-Memory) — read-only `systemctl show sharefyx-purge.timer --property=LastTriggerUSec`
lieferte einen echten Zeitstempel (`LoadState=loaded`, `ActiveState=active`), das neue Skript-
Fragment korrekt gegengerechnet: Alter ≈ 18,6h, unter 48h, INFO-Zweig korrekt genommen — sowie
gegen einen nicht existierenden Unit-Namen (leere Ausgabe, `LoadState=not-found`), WARNUNG-Zweig
korrekt genommen. Kein Schreibzugriff, kein `restart`/`enable` — bleibt Nikinger-Sache.

**4. `ui_budget.py`** — neue, eigenständige `_measure_latency()` + `LatencyMetric`-Dataclass
(kein `budget_bytes`/`ok`, eigene JSON-Sektion `"latency"`) für `search_items`/`get_item` (MCP,
echter `mcpserver.app::create_app()`, gleicher Client/Transport-Stack wie `mcp_smoke.py`) und
`GET /api/v1/overview` (Session-Cookie direkt über `AuthStore.create_session()` gemintet, kein
Login-Umweg). Bewusst getrennt von den vier bestehenden Größen-`Metric`s: die hätten
`main()`s Exit-Code — ein live-verifiziertes Abnahme-Artefakt (P5 Zeile 15) — zeitabhängig
gemacht. Jede der drei Messungen macht einen verworfenen Aufwärmlauf vor dem gemessenen Aufruf
(Advisor-Fund, zweiter Durchlauf) — ohne den hätte ein einzelner kalter Aufruf Routen-Setup/
Session-Verhandlung mitgemessen, nicht die eigentliche Frage von P6-I/P6-S beantwortet. Echter
Lauf gegen ein temporäres `DATA_ROOT` (220 Items, dieselbe Saat wie `_measure()`, Hard Rule 2:
Index rekonstruiert sich immer aus den Dateien), **dreifach reproduziert:** `search_items`
95–96 ms/20 KB, `get_item` 5 ms/0,5 KB, `GET /api/v1/overview` **438–453 ms/1,5 KB** — konstant
über alle drei Läufe hinweg, also kein Kaltstart-Artefakt, sondern eine echte, reproduzierbare
Kostenstelle. `/api/v1/overview` aggregiert vermutlich über den vollen Index (P6-S, `Store.
search()` liest weiterhin jede Datei) — genau die Zahl, die die nächste Entscheidung laut Plan
haben sollte, kein Zufallsfund. Kein neuer Test (`ui_budget.py` hatte nie welche, gleiche
Kategorie wie `mcp_smoke.py`).

**Hard Rule 8, fünf Köpfe im selben Commit:** `phase4_auth/CLAUDE.md` (O2-Zeile geschlossen),
`phase2_mcp/CLAUDE.md` (Modul-Status Zeile 10 + „Gesamt"-Zeile neunte Drift-Instanz, 92→95),
`phase3_edge/CLAUDE.md` (Prüfung-11-Ergänzung), `phase5_ui/CLAUDE.md` (`ui_budget.py`-Ergänzung),
dieser Kopf. `docs/INDEX.md`s `phase2_mcp`-Zeile im selben Commit nachgezogen (Testzahl,
Step-2-Erwähnung).

**Verifiziert:** `pytest -q` → **604 passed** (593 + 11 neue, deckt sich exakt). Volle
Testsuite gelaufen, nicht nur die vier neuen Dateien. `ui_budget.py` real ausgeführt (Text UND
`--json`) — Zahlen oben sind aus diesem echten Lauf, keine Schätzung. `mcp_smoke.py --json`
weiterhin 13/13 (Step-1-Baseline unangetastet). `authctl.py purge-expired` nicht gesondert
gegen eine Temp-DB nachgestellt — bereits vollständig über die neuen `purge_expired()`-Tests
abgedeckt, ein zusätzlicher CLI-Probelauf hätte denselben Code-Pfad kein zweites Mal geprüft.

**Status ehrlich, nicht optimistisch:** Step 2 kann nicht ✅ schließen. V42 braucht zwei echte
Tage journald auf der Live-VM; Gate A→B Punkt 3 braucht einen echten Purge-Lauf mit sinkender
`clients`-Zeilenzahl. Beide sind Nikinger-Sache, nicht in dieser Session baubar — Status bewusst
**„gebaut, Live-Teile beim Nikinger"** (P5 Step 8s Präzedenzformulierung), V42 in der
Modul-Status-Tabelle namentlich offen.

**Nachtrag, 2026-08-09, sechster — Step 3 (Update-Log und Banner) fertig, in derselben Sitzung
fortgesetzt.** Advisor-Review **vor** der Umsetzung eingeholt (Auftrag: „letzten machbaren Step
zu Ende bringen, Rest als Kommandos für den Nikinger"), vier Punkte daraus direkt übernommen,
nicht erst am Ende nachgezogen.

**Schema 3** (`authserver/store.py`): `users.seen_update_id TEXT`, additiv — anders als V1→V2
(nur neue Tabellen) muss diese Migration eine **bereits gefüllte** Tabelle erweitern; SQLite
kennt für `ALTER TABLE ADD COLUMN` kein `IF NOT EXISTS`, `_apply_schema_v3()` prüft deshalb
`PRAGMA table_info()` selbst. `SCHEMA_VERSION` → `"3"`. Zwei neue Methoden
(`get_seen_update_id`/`set_seen_update_id`), bewusst **nicht** als `UserRow`-Feld (Advisor-Fund:
`authctl.py`/`userdir.py`/`import_users_to_db.py` konsumieren `UserRow`, keines braucht diesen
Zustand). Drei bestehende Tests hätten sonst mit der falschen `schema_version`-Zahl weiter
gegrünt (`"2"` statt `"3"`) — beim ersten `pytest`-Lauf gefunden und korrigiert, nicht vom
Advisor: `test_schema_is_created_and_versioned`, die V1→V2-Migrationsprobe (endet nach Schema 3
zwangsläufig bei `"3"`, nicht `"2"`) und die dedizierte Versionsprobe selbst (umbenannt zu
`test_schema_version_is_three_after_initialise`). +3 Tests in `test_authserver_store.py`
(258→261): der v2→v3-Migrationstest (gleiches Muster wie der bestehende v1→v2-Test — Schema 2
von Hand gebaut, über `AuthStore` geöffnet, Spalte + Version geprüft) und zwei
`seen_update_id`-Roundtrip-Tests.

**`webui/updates.py`** (neu): `parse_update_log()`/`UpdateEntry`/`load_update_log()`. Strikt nach
Plan §2.4: `## <ISO-Datum>` beginnt einen Eintrag, `- ` eine Zeile, alles andere wird ignoriert.
ID = `"<Datum>#<n>"`, `n` zählt Wiederholungen desselben Datums in Dateireihenfolge (disambiguiert
zwei `## <selbes Datum>`-Blöcke). **Reihenfolge = Dateireihenfolge, nicht sortiert** — neue
Einträge werden oben eingefügt wie ein Changelog, `entries[0]` ist der neueste; das ist die
Prämisse, auf der sowohl `deploy.sh`s Gate („oberste Überschrift") als auch `api.py`s `latest_id`
aufbauen. `load_update_log()` fail-soft (fehlende/kaputte Datei ⇒ leere Liste ⇒ kein Banner, nie
ein 500) — kein Markdown-Rendering hier, das macht `app.js` mit dem vorhandenen Sanitizer (Hard
Rule 7 sinngemäß: der Server bleibt dumm, auch bei einem Log-Parser). +7 Tests
(`phase6_shares/tests/test_updates.py`, neue Datei — reine Funktionstests, kein Store, gleiche
Kategorie wie `test_patch.py`).

**`webui/api.py`**: `GET /api/v1/updates` (Einträge + `latest_id` + `seen_update_id` der
Sitzung), `POST /api/v1/updates/seen` (schreibt den **serverseitig berechneten** `latest_id`, nie
eine vom Client geschickte ID — Advisor-Vorgabe: unnötige Validierungsfläche und ein
Stale-Client-Rennen sonst umsonst). `api_routes()` bekommt dafür einen fünften Parameter,
`auth_store: AuthStore` — der gesehen-Zustand lebt in der Auth-SQLite, nicht im `storage`-Kern.
**Dokumentierte Ein-Zeilen-Abweichung** von Step 3s Plan-Dateiliste (nennt nur `webui/api.py`,
nicht `mcpserver/app.py`): `create_app()` muss den neuen Parameter durchreichen (`oauth.store`,
dieselbe Instanz wie `account_routes()`, kein zweiter DB-Handle) — acht weitere direkte
`api_routes(...)`-Aufrufer (`conftest.py` × 1, `test_api.py` × 3, `test_overview.py` × 1,
`ui_budget.py` × 2, `ui_smoke.py` × 1) mussten denselben fünften Parameter nachziehen. Per
`grep -rn "api_routes("` **vollständig** gefunden, nicht stichprobenartig — die ersten beiden
`pytest`-Läufe fingen nur die Testdateien ab; `ui_budget.py --json` real ausgeführt deckte den
gemockten Suite-Blindspot (Skripte laufen nie unter `pytest`) auf, `TypeError: api_routes()
missing 1 required positional argument`.

**`webui/static/js/updates.js`** (neu): `window.SharefyxUpdates.init({api, toast})`, injiziert
von `app.js`s `initShell()` an dessen eigenem Ende. **Muss vor `app.js` geladen werden**
(`app.html`, beide `defer`) — `updates.js` ruft `app.js`s globale `markdownToHtml()`/
`sanitizeHtml()` (Top-Level-Funktionen, kein IIFE, deshalb window-Properties trotz `"use
strict"`), umgekehrt bräuchte `app.js` sonst einen noch nicht existierenden
`window.SharefyxUpdates`. Advisor-Fund **vor** der Umsetzung, sonst hätte ein stiller No-Op das
Banner nie gezeigt, `pytest` bliebe grün (JS bleibt laut Plan unit-ungetestet, P5) — der
Nikinger hätte es im Browser gefunden, nicht die Suite.

**Node/jsdom-Simulation** (Scratchpad, nicht im Repo, gleiche Kategorie wie P5 Step 10/11):
erster Versuch mit `window.eval(appJs)` + `window.eval(updatesJs)` warf fälschlich
`ReferenceError: markdownToHtml is not defined` — **echter Befund über die Testmethode, kein
Bug im Code:** Strict-Mode-Direct-`eval()` isoliert Top-Level-Deklarationen von der aufrufenden
Umgebung (ECMAScript-Spezialfall genau für `eval()`), ein reales `<script defer>`-Tag tut das
nicht. Zweiter Versuch mit echten, ins DOM eingehängten `<script>`-Elementen (treue
Nachbildung von `<script src=... defer>`) lief sauber durch: Banner erscheint mit gerendertem
Markdown (`**Eintrag**` → `<strong>`), setzt `body.has-update-banner`, „Verstanden" versteckt
es und postet `/updates/seen`, „Update-Log ansehen" öffnet den Dialog mit denselben Einträgen,
ein bereits gesehener `latest_id` unterdrückt das Banner beim erneuten Laden vollständig.

**`deploy.sh`-Gate (P6-X):** läuft direkt nach `release_sha` (vor venv/pip/pytest — ein sicher
vermeidbarer Abbruch soll in Sekunden kommen, nicht nach dem teuersten Skriptteil), akzeptiert
UTC- **oder** lokales Datum (ein Deploy kurz nach Mitternacht Lokalzeit läge in UTC noch am
Vortag — ein falscher Abbruch bei einem legitimen Eintrag wäre der schlechtere Fehler als eine
zu großzügige Prüfung). `SHAREFYX_ALLOW_STALE_UPDATELOG=1` überspringt es. **Live-Fund beim
ersten Testlauf** (nicht Advisor): die `grep | sed`-Pipeline unter `pipefail` warf bei einer
fehlenden/leeren Datei einen rohen Bash-Fehler statt der eigenen ABBRUCH-Zeile — `grep` liefert
1 bei keinem Treffer, `pipefail` reicht das durch, `set -e` bricht die Zuweisung sofort ab,
bevor die eigene `if`-Prüfung überhaupt läuft. Mit `|| true` behoben. `test_deploy_scripts.py`s
`_env()`-Helfer setzt die Override-Variable jetzt als Default (die `source_repo`-Fixture trägt
kein `docs/UPDATE_LOG.md`, ohne Default wären alle ~18 bestehenden Deploy-Tests am neuen Gate
gescheitert, nicht nur die drei, die es gezielt prüfen) — dieselbe `_clean_environ()`-Disziplin,
die die Testliste (Plan §5) für jede neue Skript-Testdatei vorschreibt. +3 Tests: Gate blockiert
(kein Log), Gate lässt einen echten heute datierten Eintrag durch (Positivpfad, nicht nur der
Fehlerfall), Override umgeht ein fehlendes Log. Meta-Test
`test_harness_ignores_ambient_sharefyx_configuration` um die neue Env-Var ergänzt (hätte sonst
seinerseits falsch geschlagen).

**`docs/UPDATE_LOG.md`** (neu): erster Eintrag, datiert 2026-08-09, kündigt die künftige
Sichtbarkeitsumstellung an (P6-L, H1 — Pflichtinhalt laut Plan). **Ehrlich zum Gate:** dieser
Eintrag ist nur am 2026-08-09 selbst „frisch" — deployt der Nikinger an einem späteren Tag ohne
neuen Eintrag, blockiert `deploy.sh` by design (Override oder neuer Eintrag), das ist keine
Regression, sondern der Zweck des Gates.

**Schema-3-Rollback-Sicherheit geprüft** (`deploy.sh` rollt bei einem gerissenen Health-Gate auf
altes Binary zurück — „altes Binary gegen Schema-3-DB" ist ein realer Pfad). `upsert_user()`/
`_user_from_row()` benennen Spalten immer schon explizit, die neue Spalte ist für altes Binary
inert. **Eine echte, harmlose Nebenwirkung:** altes Binärs `initialise()` kennt
`_apply_schema_v3()` nicht und schreibt `schema_meta.schema_version` beim Start zurück auf
„2" (Spalte bleibt physisch stehen) — bis der nächste erfolgreiche Deploy wieder „3" schreibt.

**Kleine Design-Entscheidung:** Banner als `position: fixed` statt einer Grid-Zeile in `.shell`
(§4.1s Drei-Spalten-Layout bleibt unverändert); „Update-Log ansehen" sitzt im bestehenden
Konto-Dialog statt einen zweiten Einstellungs-Einstiegspunkt zu erfinden.

**Verifiziert:** `pytest -q` → **620 passed** (604 + 16 neue, deckt sich exakt: 3
`test_authserver_store.py` + 7 `test_updates.py` + 2 `test_api.py` + 3
`test_deploy_scripts.py` + 1 `test_static_routes.py` — der letzte aus dem zweiten Advisor-
Durchlauf, siehe unten). `mcp_smoke.py --json` weiterhin 13/13. `ui_budget.py --json` und
`ui_smoke.py --json` real ausgeführt, beide sauber (erst NACH dem Signatur-Fix — vorher der
`TypeError`-Fund oben). `node --check` auf `app.js`/`updates.js`. Tabu-Diff: `mcpserver/app.py`
ist eine dokumentierte Ein-Zeilen-Abweichung (siehe oben), sonst nur `phase4_auth/authserver/
store.py`, `phase5_ui/webui/{updates,api,config}.py`, `phase5_ui/webui/static/*`,
`phase5_ui/scripts/deploy.sh`, `phase5_ui/scripts/{ui_budget,ui_smoke}.py`, `docs/UPDATE_LOG.md`,
Testdateien — genau die in Step 3s Plan-Dateiliste plus die eine dokumentierte Abweichung.

**Zweiter Advisor-Durchlauf, vier Funde vor dem Commit behoben:** (1) Bannerhöhe war fest
(`44px`) statt am realen, mehrzeiligen Eintragstext gemessen — Fix + Begründung stehen jetzt als
Kommentar in `app.css`/`updates.js` (`syncBannerHeight()`). (2) „sechs weitere Aufrufer" war
falsch gezählt, tatsächlich acht (`grep`-Beleg oben) — korrigiert. (3) Die `updates.js`-vor-
`app.js`-Reihenfolge stand nur in Docstrings, kein Test bewies sie — zwei Ergänzungen in
`test_static_routes.py` (Content-Type-Tabelle + `test_updates_js_loads_before_app_js`). (4)
Schema-3-Rollback-Sicherheit tatsächlich geprüft, nicht nur behauptet — Ergebnis + der eine
harmlose Fund (`schema_version` fällt nach einem Rollback vorübergehend auf „2") stehen im
Absatz direkt darüber.

**Status ehrlich, nicht optimistisch:** Step 3 kann nicht ✅ schließen. Gate-A→B-Punkt 4
verlangt den echten Browser (Banner erscheint/verschwindet/ist wiederfindbar) **und** dass
Fabian den Eintrag über die Sichtbarkeitsumstellung tatsächlich gesehen hat — beides
Nikinger/Fabian-Sache. Status bewusst **„gebaut, Live-Teile beim Nikinger"**.

**Nächster Schritt (konkret):** Block A (Steps 0–3) ist damit vollständig **gebaut**, nichts
davon ist live. Vor Block B steht **GATE A→B** (Plan §4, vier Punkte) — konsolidierte
Reihenfolge für den Nikinger, über Step 2 und Step 3 hinweg, nicht nur Step 3 isoliert:

1. **Frisches Auth-Backup vor dem Deploy** — dieser Deploy migriert die laufende `auth.sqlite3`
   auf Schema 3 (additiv, aber ein frisches Backup unmittelbar davor kostet nichts und deckt
   genau den Fall ab, den `deploy.sh`s eigenes Pre-Deploy-Bundle NICHT abdeckt — das sichert nur
   `DATA_ROOT`, nicht `auth.sqlite3`): `sudo systemctl start sharefyx-authbackup.service`
   (bereits installierter Oneshot, `phase5_ui/systemd/sharefyx-authbackup.service`) — kein
   manueller `authbackup.sh`-Aufruf mit Env-Vars nötig.
2. **Deploy** — `phase5_ui/scripts/deploy.sh main` (oder der passende Ref). Bricht ohne einen
   heute datierten `docs/UPDATE_LOG.md`-Eintrag ab (P6-X) — der vorhandene Eintrag ist auf
   2026-08-09 datiert, trägt also nur am Tag des tatsächlichen Deploys; an einem späteren Tag
   entweder einen neuen Eintrag ergänzen oder `SHAREFYX_ALLOW_STALE_UPDATELOG=1` setzen (bewusst
   so, kein Bug).
3. ~~Gate-A→B-Punkt 1+2~~ — **✅ live bestanden, 2026-08-09** (Nachtrag unten).
4. **Gate-A→B-Punkt 4 — teilweise, ein echter Fund korrigiert (Nachtrag „achter" unten):**
   Banner erschien beim ersten echten Test, Text war aber mitten im Satz abgeschnitten
   (Content-Bug in `docs/UPDATE_LOG.md`, nicht im Parser — behoben + Regressionstest). Bleibt
   zu prüfen: Banner jetzt vollständig, verschwindet nach „Verstanden", unter Konto →
   „Update-Log ansehen" wiederfindbar. **Und Fabian muss den Eintrag gesehen haben** — ohne
   seine Bestätigung schließt dieser Punkt nicht.
5. **V42 (Step 2, weiterhin offen)** — zwei Tage echtes journald abwarten, danach prüfen, ob das
   `ua`-Feld reale Claude-Oberflächen unterscheidet (`grep '"ev":"http"'` in den Logs, `ua`-Werte
   vergleichen).
6. **Gate-A→B-Punkt 3** — **versucht, 2026-08-09, korrekt noch nicht abgeschlossen** (Nachtrag
   unten): `clients`/`token_families` sind noch zu jung für die 30/90-Tage-Grenze. Frühestens
   ab 2026-08-28 erneut prüfen (`authctl.py purge-expired`, gegen den echten Zeilenrückgang).

Erst wenn alle vier Gate-Punkte stehen, beginnt Step 4 (Storage-Fundament, Block B) — nicht
vorher, das Gate ist im Plan hart. V42 blockiert das Gate nicht, sollte aber nicht vergessen
werden.

**Nachtrag, 2026-08-09, siebter — Gate-A→B-Punkte 1–3 live geprüft** (Claude Code direkt auf der
VM, Connector zuvor vom Nikinger neu verbunden — die alte Verbindung hatte noch den 6-Tool-Stand
von vor P6). **Punkte 1+2 ✅:** an `itm_1b4fd59e` (Wegwerf-Testitem, danach archiviert) —
mehrdeutiger `old_text` schlägt fehl (`"edits[0] fand 2 Treffer (Zeilen 2, 4)"`), Datei
unverändert (`version` blieb 1); drei Ersetzungen über zwei Aufrufe, erster ohne `return_body`
liefert eine Quittung (`{"op":"patch",...,"replacements":2,"lines":[1,4],"bytes":{...}}`), zweiter
mit `return_body=true` den vollen Text. Vier eigene Git-Commits in `DATA_ROOT` bestätigt (`create`/
`patch`×2/`archive`). **Punkt 3 — Mechanismus bestätigt, Zahl noch nicht gesunken:**
`SPACE_AUTH_DB=/var/lib/sharefyx/auth.sqlite3 authctl.py purge-expired` lief sauber, 7 reale
abgelaufene Zeilen entfernt (1 `auth_codes` + 6 `access_tokens`) — aber `clients`/`token_families`
beide `0`, **ehrlicher Grund, kein Fehlschlag:** die älteste tote Familie ist vom 2026-07-29, elf
Tage alt, unter der 30-Tage-Grenze; kein Client ist 90 Tage alt (Dienst existiert erst seit
2026-07-24/29). Zeitgleich stiegen `clients`/`token_families` sogar leicht (39→40, 22→23) — der
Nikinger-Reconnect des Connectors registrierte einen neuen DCR-Client, reine Nebenwirkung der
Live-Prüfung selbst. `journalctl -u sharefyx-purge.service` bestätigt zusätzlich: der tägliche
Timer lief zuletzt Aug 9 00:04 (VOR dem heutigen Deploy) noch mit dem alten Purge-Code (Ausgabe
ohne `token_families`/`clients`-Schlüssel) — der heutige manuelle Lauf war der erste mit dem neuen
O2-Code, der nächste Timer-Lauf (Aug 10 00:02) läuft bereits dagegen. **Ob Schritt 1
(Auth-Backup vor dem Deploy) lief, ist aus dem Chat nicht ersichtlich** — der Nikinger postete
nur die `deploy.sh`-Ausgabe. Kein Vorfall, falls übersprungen (additive Migration, kein
Datenverlustrisiko), aber im Nachhinein nicht mehr sinnvoll nachholbar — beim nächsten Deploy
nicht vergessen.

**Nachtrag, 2026-08-10, achter — Gate-A→B-Punkt 4: Content-Bug im Banner gefunden+behoben,
Timer-Bestätigung nachgezogen.** Nikinger-Meldung: Banner sichtbar, Text abgeschnitten bei
„…und alles Neue ist nach". **Kein Parser-Bug** (tut exakt, was Plan §2.4 verlangt: nur `## `/
`- `-Zeilen zählen) — **ein Content-Bug:** der erste `docs/UPDATE_LOG.md`-Eintrag war weich
umgebrochener Fließtext über vier physische Zeilen, der Parser verschluckte die drei
Fortsetzungszeilen stillschweigend. Behoben: zwei echte `- `-Zeilen (je eine physische Zeile) +
ein `<!-- -->`-Formathinweis am Dateianfang. **Regressionstest ergänzt, nicht nur die Datei
gefixt:** `test_real_update_log_has_no_swallowed_continuation_lines` liest die REALE Datei, kein
Test hatte das bis dahin getan. +1 Test (`test_updates.py` 7→8, 621 gesamt). Parser-Gegenprobe:
beide Zeilen jetzt vollständig. **Purge-Timer bestätigt:** Lauf vom 2026-08-10 00:02 mit dem
neuen O2-Code (`token_families`/`clients` beide `0`, konsistent — noch nichts alt genug).
Punkt 4 bleibt offen bis der Nikinger den gefixten Banner erneut prüft und Fabian ihn gesehen
hat.

**Softcap-Warnung:** dieser Kopf ist nahe am 40KB-Softcap. Wenn Step 4 einen neuen `## Session
stopped`-Block eröffnet, sind die Step-0/1/2-Nachträge die Kompressionskandidaten — verbatim
nach `SESSIONS_ARCHIVE.md` (neue Datei), Muster wie `phase4_auth/CLAUDE.md`s Steps-0–6a-
Verschiebung: `sed -n`, Byte-Identität vor dem Löschen geprüft.
