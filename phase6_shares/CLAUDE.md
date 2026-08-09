---
status: live
purpose: Phase-Head Freigaben, Ordner, Werkzeug-Ergonomie — Scope, harte Regeln, Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase6_shares/ oder an den in P6-C genannten Dateien in storage/mcpserver/webui — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase6_shares_plan.md         # voller Plan, Entscheidungen P6-A–P6-AC, Steps 0–10
  - ../docs/concepts/PHASE5_CLOSEOUT_HANDOVER.md   # Herkunft der offenen Entscheidungen §4.1–§4.6, [VERIFY]-Bilanz V27–V38
updated: 2026-08-09
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

**Nachtrag, 2026-08-09, zweiter — Advisor-Review vor Sessionende, vier Funde behoben:**
(1) `docs/INDEX.md`s eigene Zeile für `ROADMAP.md` war seit vor dieser Session stale (nannte
„Phases 1–5"/„Phase 6 not yet planned" und eine veraltete Größe) — korrigiert, jetzt „Phases 1–6"/
„P6 🔄 gestartet"/~15KB. (2) Vollständigkeitsprüfung „jede `.md` hat eine Zeile in
`docs/INDEX.md`" nachgeholt (Plan-Punkt 1, vorher nicht gelaufen): alle 32 `.md`-Dateien im Repo
sind verlinkt, einzige Ausnahme `docs/INDEX.md` selbst (verlinkt sich nicht, erwartet). (3)
Staleness-Grep über `README.md`/`AGENTS.md`/`docs/PROMPTS.md`/`phase5_ui/CLAUDE.md`: keine
weiteren Funde — `phase5_ui/CLAUDE.md`s „Browser-Planungssession"-Erwähnungen stehen in seinem
eingefrorenen Session-Block (Historie, nicht editieren); `README.md`s Stand-2026-08-02-Hinweis ist
seit P4→P5 unverändert stale, disclaimt sich aber selbst explizit („siehe Root-`CLAUDE.md` für den
verbindlichen Phasenstand") — bewusst nicht angefasst, außerhalb dieses Step-0-Scopes.
(4) Zwei Dokumentationslücken geschlossen: `scripts/`-Auslassung jetzt im Minor-Drift-Absatz oben
benannt (vorher nur in Gedanken, nicht aufgeschrieben); `ROADMAP.md`s
„Mehrmandantenfähigkeit"-Absatz hatte sich selbst widersprochen (durchgestrichen **und** „nicht
widerlegt" im selben Atemzug) — Durchstreichung entfernt, nur `Feingranulare Rechte` ist
tatsächlich widerlegt (echtes ACL-Modell existiert jetzt), `Mehrmandantenfähigkeit` war erfüllt,
nicht widerlegt. `pytest -q` danach erneut 576/576, Size-Sweep erneut sauber.

**Nachtrag, 2026-08-09, dritter — Step 1 (Werkzeug-Ergonomie) fertig, in derselben Sitzung
fortgesetzt:** `storage/patch.py` (neu: `TextEdit`, `PatchError`, `PatchResult`, `apply_edits()`),
`Store.patch()`, `mcpserver/receipts.py` (neu: `write_receipt()`), siebtes Tool `patch_item`,
`return_body: bool = False` an allen vier Schreib-Tools, `update_item` lehnt `visibility`/
`share_read`/`share_write` mit `ValidationError` ab. `mcp_smoke.py` um einen Patch-Durchgang
erweitert, **13/13 grün**. `pytest -q`: **593 passed** (576 + 17 neue: 5 `phase6_shares/tests/
test_patch.py` + 5 `phase1_storage/tests/test_store.py` + 7 `phase2_mcp/tests/test_tools.py`).

**V48 empirisch geschlossen (fastmcp 3.4.4, installierte Version):** `list[TypedDict]` als
Tool-Parameter rendert zu einem brauchbaren Schema — kein Fallback auf `list[dict[str,str]]`
nötig. Beleg: `patch_item({"edits":[{"old_text":...,"new_text":...}]})` lief erfolgreich durch
den echten `fastmcp.Client`/`StreamableHttpTransport`-Stack, sowohl in
`test_app.py::test_all_seven_tools_are_callable_over_http` als auch in `mcp_smoke.py` — beide
Wege validieren/serialisieren das Schema tatsächlich, kein Mock.

**Drei Advisor-Funde vor dem Commit behoben, keiner davon im Plan explizit benannt:**
1. **Kollateralschaden durch Quittungen-als-Default** — sieben bestehende Tests/Skript-Checks
   gingen von Frontmatter-Text in `create_item`/`append_to_item`/`update_item`-Antworten aus
   (`test_tools.py::test_create_item_uses_principal_space`, `mcp_smoke.py` Checks 2/6/7,
   `test_request_log.py` ×2, `test_app.py` ×2). Alle auf JSON-Quittungsfelder umgestellt;
   `test_app.py`s HTTP-Rundlauf nutzt an drei Stellen bewusst `return_body=True`, damit die
   Inhaltsprüfungen dort weiterhin gegen echten Dateitext laufen.
2. **`update_item`s Riegel ohne die drei Parameter ist wirkungslos** — ohne `visibility`/
   `share_read`/`share_write` als echte Funktionsparameter hätte ein Aufruf mit diesen Feldern
   nie `ValidationError` erreicht (Python/`fastmcp`-Schema hätte vorher abgelehnt). Alle drei als
   `str | list[str] | None = None` ergänzt, geprüft **vor** der Zielraum-/Rechteauflösung.
3. **`phase6_shares/tests/test_store_patch.py`/`test_tools_patch.py` (Plan-Namen) wären
   fixture-los gewesen** — `phase1_storage/tests/conftest.py` und `phase2_mcp/tests/conftest.py`
   sind beide leer, alle Fixtures (`store`/`store_git`/`clock`/`_git_log`/`tools_map`/`_as`) leben
   lokal in `test_store.py`/`test_tools.py`. Plan §5s Zusammenfassungstabelle sagt für beide
   ohnehin „erweitert", nicht „neue Datei" — dieser Tabelle gefolgt, nicht der Step-1-Fließtext-
   Erwähnung. Die vier reinen `apply_edits()`-Funktionstests (kein Store, keine Fixture nötig)
   stehen wie geplant in `phase6_shares/tests/test_patch.py`.

**Kleine, bewusste Abweichungen von der Beispielquittung in Plan §1.5.3** (dokumentiert, nicht
stillschweigend): kein `folder`-Feld (existiert erst ab Step 4, `Item.folder`); Archivieren über
`update_item(status="archived")` liefert `op="update"`, nicht `op="archive"` — die Quittung bildet
die vier Tools ab, nicht `Store`s interne Commit-Op-Namen (die kennen zusätzlich `"archive"`/
`"drift"`). `appended_bytes` bei `append` ist `len(text.encode())` — die Länge des tatsächlich
angehängten Texts, kein `Store`-Umbau nötig.

**Verifiziert:** `pytest -q` → 593 passed. `mcp_smoke.py` (Text und `--json`) → 13/13. Tabu-Diff
gewahrt: nur `storage/`, `mcpserver/{tools,receipts,patch aus storage}.py` und die drei Testdateien
berührt — genau die in P6-C freigegebene Fläche.

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

**Nächster Schritt (konkret):** Step 3 — Update-Log und Banner (`docs/UPDATE_LOG.md` neu,
`webui/updates.py` neu, `webui/api.py`, `authserver/store.py` Schema 3, `webui/static/js/
updates.js`, `app.html`/`app.css`, `deploy.sh`-Gate). Plan §4 Step 3. Vor dem Start: der
Nikinger sollte V42 im Hinterkopf behalten (zwei Tage journald) und den GATE-A→B-Punkt-3-Purge-
Lauf einmal real anstoßen — beides läuft parallel zu Step 3 mit, blockiert ihn nicht.
