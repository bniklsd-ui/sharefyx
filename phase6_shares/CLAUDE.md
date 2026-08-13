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
  - ./SESSIONS_ARCHIVE.md                          # Steps 0-6 verbatim (sechs Eintraege), L3, kein Softcap
updated: 2026-08-13, sechster -- (Step 7a gebaut+erweitert: Textfarben-Token app.css, Wortmarke/Versionen weiss + v2.1, Sichtprobe zweimal per Screenshot verifiziert, Deploy beim Nikinger; Rotations-Reihenfolge-Bug im eigenen Skript gefunden+von Hand korrigiert)
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
| 8 | Lesbarkeit der Textfarben (`ITEM_MOVE_PLAN.md` §3, P6-AD/AE): `phase5_ui/webui/static/app.css` — `--text-muted`/`--text-faint` kalibriert angehoben, neues `--text-placeholder`, `.input::placeholder` darauf umgehängt. **Nachtrag, Nikinger-Feedback vor dem Deploy:** Wortmarke „sharefyx" + Versionsbadge (jetzt `v2.1`, `app.html`) sowie alle Versionsnummern aus den Dateien (`recent-row__meta`, `.editor__version`, `.version-band__number`, `ro-meta`) jetzt `var(--text)` statt `--text-faint`/`--text-muted` — neue Klasse `.version-num` trennt die Versionsnummer farblich vom gedämpften Begleittext im selben Element (`app.css`/`app.js`) | 7a | ✅ **gebaut, Deploy beim Nikinger** — Kontrastwerte bereits in `ITEM_MOVE_PLAN.md` §3.1 protokolliert (durchgerechnet vor dieser Session); Sichtprobe zweimal per In-Process-Server + Screenshot gegen die echte `app.css`/`app.js` (Login-Seite, Liste mit Chips, Editor mit Meta-Panel — alle drei beide Male gesehen, nicht behauptet). Deploy braucht Sudo für den Neustart, außerhalb dessen, was Claude Code selbst kann (Präzedenz: Steps-4–6-Cutover, `SESSIONS_ARCHIVE.md`) | 0 (P5-T: JS/CSS bleiben unit-ungetestet; `pytest` unverändert als Regressionsprobe — 724 gesamt vor UND nach beiden Teilen dieser Session, keiner davon neu) |

## Geerbte Contracts

**[2026-08-09, P6 Step 0] Dritte, benannte Öffnung des P1-Contracts** (Plan §1.4): `models.py`
bekommt `folder`/`visibility`/`share_read`/`share_write`, `store.py` bekommt `acl_of()`/`patch()`/
erweiterte `create()`/`update()`/`search()`/`list_spaces()`. Wird in Step 4 umgesetzt, hier nur
angekündigt — nach Phasenabschluss (Step 10) wieder geschlossen, siehe `phase1_storage/CLAUDE.md`.

---

## Session stopped — 2026-08-13, sechster — (Step 7a gebaut: Textfarben-Token)

**Auftrag:** Nikinger — Step 7a bauen (`ITEM_MOVE_PLAN.md` §3, vom vorigen Block als „sofort und
unabhängig lieferbar" benannt): vier Token-Zeilen plus eine Regel in `app.css`, eigener kleiner
Deploy samt `UPDATE_LOG.md`-Eintrag.

**Ergebnis: gebaut, noch nicht deployt.** `phase5_ui/webui/static/app.css` — gegen den echten
Code verifiziert (`--text-muted`/`--text-faint` standen exakt an der im Plan genannten Stelle,
`.input::placeholder` exakt an Zeile 187 wie in §3.1 vermerkt):
```
--text-muted:       #C4CDD8;   /* war #9AA6B4 */
--text-faint:       #A7B2BF;   /* war #64707E */
--text-placeholder: #7E8A98;   /* neu, nur .input::placeholder */
```
Kontrastwerte waren bereits in `ITEM_MOVE_PLAN.md` §3.1 durchgerechnet (vorige Session) —
diese Session hat sie nicht neu gemessen, nur die vier Zeilen umgesetzt.

**Sichtprobe (Pflicht laut §3.3 DoD), diese Session neu gebaut, kein Repo-Artefakt:** Server
(braucht Projekt-`.venv`) und Browser-Treiber (braucht nur `playwright`) sprechen über echtes
HTTP miteinander, kein gemeinsamer Prozess nötig. `~/.claude-code-tools/svg-venv` hatte bereits
einen gecachten Chromium (`~/.cache/ms-playwright`, für die SVG-Renderpipeline) — das
`playwright`-Paket testweise trotzdem zusätzlich ins Projekt-`.venv` installiert, um Server und
Treiber im selben Skript zu starten. **Advisor-Fund vor dem Commit:** das bricht die im Repo
bereits etablierte Trennung — `svg-venv` existiert genau dafür, damit Browser-Automatisierung
nicht in das `.venv` einsickert, aus dem `pytest`/`deploy.sh` laufen. Behoben: `playwright`/
`greenlet`/`pyee` wieder aus dem Projekt-`.venv` deinstalliert; das Screenshot-Skript startet den
Server weiterhin mit dem Projekt-`.venv` (echter `uvicorn`, echte `authserver`/`webui`-Module),
treibt den Browser aber mit `svg-venv`s Python — zwei Prozesse, zwei Umgebungen, eine
HTTP-Verbindung dazwischen.

Skript (`/tmp/.../scratchpad/ui_screenshot.py`, nicht Teil des Repos): temporäres `DATA_ROOT` +
temporäre `AuthStore`, alle vier Routengruppen inkl. `static_routes()` gemountet, echter
`uvicorn` auf `localhost` (nicht `127.0.0.1` — Chrome behandelt nur `localhost` als potenziell
vertrauenswürdig genug für das `Secure`-Cookie ohne TLS), Einladung+TOTP-Enrollment per `httpx`
vorbereitet, echter Login-Roundtrip durch das Browser-Formular. Ein Stolperstein unterwegs:
`http.cookiejar` (unter `httpx`) verweigert das Zurücksenden eines `Secure`-Cookies über eine
reine `http://`-Verbindung strikter als ein echter Browser — Cookie deshalb zwischen den beiden
`httpx`-Schritten manuell weitergereicht statt der Jar vertraut.

Drei Screenshots gesehen (`Read`, nicht nur behauptet): Login-Seite (Platzhalter „TOTP- oder
Recovery-Code" jetzt klar lesbar), Liste mit Ordner-Chips/Kennzahlen-Kacheln/„Zuletzt benutzt"
(Space-Navigation, Zähler, Versionsstempel „v1 · 2026-08-13" alle im kalibrierten Grau lesbar),
Editor mit Meta-Panel („Kopfdaten YAML-Frontmatter", Formatierleiste, Versionsband „v1",
„Zeile anhängen..."-Platzhalter). Alle drei DoD-Sichten aus §3.3 abgedeckt.

**`docs/UPDATE_LOG.md`:** eine neue `- `-Zeile unter dem bereits heute datierten
`## 2026-08-13`-Abschnitt (kein neuer Heading nötig, das Datum stimmt bereits) — deploy.sh-Gate
(P6-X) bleibt damit ohne Override erfüllbar.

**Deploy bewusst nicht in dieser Session ausgeführt:** `deploy.sh` braucht Sudo für den
Service-Neustart — außerhalb dessen, was Claude Code selbst kann (dieselbe Grenze wie beim
Steps-4–6-Cutover, `SESSIONS_ARCHIVE.md`, dort ausdrücklich „vom Nikinger ausgeführt"). Dieser
Prozess läuft auf der echten Produktions-VM (`systemctl status sharefyx-mcp` zeigt den echten,
aktiven Dienst mit echtem Traffic während dieser Session) — ein Redeploy ist eine Aktion mit
Wirkung auf ein geteiltes System (Fabian benutzt denselben Dienst), also Nikinger-Sache, nicht
automatisch von Claude Code auszulösen.

**Rotation in dieser Session ausgeführt, mit Korrektur:** `scripts/rotate_session_block.sh
phase6_shares` archiviert den Block mit dem **höchsten Zeilenindex** im Head als „neuesten" —
Konvention ist also: der aktuellste Block steht am **Ende** der Datei, nicht am Anfang. Der
sechste Block wurde zunächst versehentlich **vor** dem fünften eingefügt; das Skript hat
daraufhin den fünften (älteren) behalten und den sechsten ins Archiv verschoben — mechanisch
korrekt nach seiner eigenen Regel, nur mit vertauschter Eingabe. Von Hand korrigiert: der fünfte
Block liegt jetzt an seiner richtigen Archivposition (vor „Step 6, dritter", newest-first), der
Head trägt nur noch diesen sechsten Block. Kein Byte-Identitätsverlust — beide Blöcke wurden
unverändert verschoben, nur die Zuordnung war falsch.

**Verifiziert:** `pytest -q` **724 passed** (unverändert — P5-T: JS/CSS bleiben
unit-ungetestet, keine neuen Tests erwartet). `git status --short` zeigt ausschließlich
`app.css`, `docs/UPDATE_LOG.md`, `phase6_shares/CLAUDE.md`, `phase6_shares/ITEM_MOVE_PLAN.md`,
`phase6_shares/SESSIONS_ARCHIVE.md`, `docs/INDEX.md`. `.venv` selbst ist nicht versioniert —
der Playwright-Fund war deshalb nur über den Advisor-Durchlauf sichtbar, nicht über `git status`.
Tabu-Diff nicht relevant (P5-B betrifft `storage/`/`mcpserver/{tools,permissions,server}.py`,
nicht `webui/static/`). Advisor vor diesem Commit konsultiert — beide Funde (Zeitform der
Verifiziert-Zeile, `.venv`-Leck) in dieser Fassung des Blocks bereits behoben.

**Nachtrag, noch vor dem ersten Deploy — Nikinger-Feedback:** Wortmarke „sharefyx" + Versionsbadge
sollten weiß statt grau sein, Badge auf `v2.1`; zusätzlich **alle Versionsnummern aus den
Dateien** (`item.version`, überall wo die UI sie zeigt) ebenfalls weiß statt grau. Das ist eine
bewusste Umkehrung eines Teils der §3.2-Entscheidung von vorhin (dort ausdrücklich *gegen*
„alles auf `--text`" — Platzhalter-Verwechslungsgefahr, leises Versionsband) — Nikinger hat hier
gezielt nur die Versionsnummern selbst gemeint, nicht die Platzhalter/Begleittexte, und das ist
sein Ruf, nicht meiner; keine Rücksprache nötig, nur sauber umgesetzt.

Vier Fundstellen identifiziert (`grep` nach `item.version`/`.rail__version` in `app.js`/`app.css`,
nicht geraten): `.rail__brand`+`.rail__version` (Wortmarke, Badge — Badge-`opacity:.6` dabei
entfernt, sonst bliebe „weiß" nur ein gedämpftes Weiß und der Zweck der Änderung wäre verfehlt),
`.editor__version` und `.version-band__number` (beide zeigen nur Versionstext, direkte
Farbänderung reicht), `.recent-row__meta`/`ro-meta` (zeigen Version **und** Datum/Typ im selben
Element — hier eine neue Klasse `.version-num` eingeführt statt die ganze Zeile weiß zu machen,
damit nur die Zahl selbst hervortritt, Datum/Typ bleiben gedämpft; `recent-row__meta` dafür in
`app.js` von einem Text-Span auf zwei verschachtelte Kindknoten umgebaut, `ro-meta`s Version-Span
bekam nur eine zweite Klasse). `app.html`: `v2` → `v2.1`.

**Eine Inferenz über den wörtlichen Auftrag hinaus, benannt statt still gemacht:** `ro-meta` ist
die Nur-lesen-Ansicht eines **fremden** Items (geteilter Space) — „alle Versionsnummern aus den
Dateien" wortwörtlich genommen schließt das ein, aber es ist die einzige der vier Fundstellen, zu
der kein Grep-Treffer zwang, sondern eine Lesart. Mitgenommen, weil die Alternative (dieselbe
Versionszahl in der eigenen Ansicht weiß, in der fremden grau) inkonsistent gewirkt hätte — bei
Widerspruch ist das eine Korrektur wert, kein stiller Fakt.

**Sichtprobe wiederholt**, diesmal mit der aus dem ersten Advisor-Fund gezogenen Konsequenz sauber
umgesetzt statt nur nachträglich repariert: Server-Setup (`server_setup.py`, Projekt-`.venv`,
Import von `authserver`/`webui`/`storage`) startet `uvicorn` und ruft danach `svg-venv`s Python
als **separaten Subprozess** nur für `screenshot_client.py` (reines Playwright, kein
Projekt-Import) — beide Umgebungen bleiben getrennt, kein erneutes Pip-Install im Projekt-`.venv`.
Drei neue Screenshots gesehen: Wortmarke „SHAREFYX v2.1" weiß, „v1 · 2026-08-13" in der
Übersicht mit weißer Zahl und gedämpftem Datum, Editor-Header „v1 gespeichert" und die
Versionsband-Zahl „v1" beide weiß.

**Verifiziert (zweiter Teil):** `pytest -q` erneut **724 passed**, unverändert. `.venv` erneut auf
ein sauberes `pip show playwright` geprüft (leer) — diesmal von vornherein nie installiert, kein
Nachräumen nötig. `git status --short` zeigt ausschließlich `app.css`/`app.html`/`app.js`.

**Nachtrag, noch vor dem ersten Deploy — Nikinger-Weisung zum Update-Banner:** nur die
v2.1-Zeilen dieser Deploy-Ära sollen im Banner erscheinen, nicht die v2-Rückschau (Umstellung
live + beide Hotfixes) erneut. `docs/UPDATE_LOG.md :: parse_update_log()` zeigt im Banner **immer
nur `entries[0]`** — ein Eintrag ist ein `##`-Block, nicht eine Zeile. Der bestehende
`## 2026-08-13`-Block (7 Zeilen: 2 neue v2.1 + 5 alte v2) in **zwei** gleichdatierte Blöcke
gesplittet — die eigene Docstring-Doku in `updates.py` sieht das ausdrücklich vor
("disambiguiert zwei `## <selbes Datum>`-Blöcke"). Oben (neu, `id=2026-08-13#1`): nur die zwei
v2.1-Zeilen. Darunter (`id=2026-08-13#2`): die fünf v2-Zeilen unverändert, bleiben im
Vollständigen Log ("Update-Log ansehen") sichtbar, verschwinden nur aus dem Auto-Popup.
Nachgeprüft, nicht nur behauptet: `parse_update_log()` gegen die echte Datei ausgeführt,
`entries[0]` hat exakt die zwei neuen Zeilen.

**Eine ehrlich benannte Unsicherheit, kein stiller Fund:** die ID-Vergabe ist rein positionell
(erstes gleichdatiertes Heading in Dateireihenfolge = `#1`), nicht inhaltsbasiert. Falls der
Nikinger das Banner für den `92b918b`-Deploy (die fünf v2-Zeilen, damals ebenfalls unter
`2026-08-13#1`) bereits gesehen/weggeklickt hat, trägt `users.seen_update_id` bereits genau diese
ID — und die neuen v2.1-Zeilen erben jetzt dieselbe ID, weil sie ebenfalls zum ersten
gleichdatierten Block wurden. In diesem Fall poppt das Banner **nicht** automatisch neu auf,
obwohl der Inhalt neu ist; „Update-Log ansehen" zeigt es trotzdem korrekt. Kein Zugriff auf die
echte `auth.sqlite3` genommen, um das zu prüfen (Auto-Mode-Classifier blockierte den Pfadversuch,
zu Recht — das wäre ein Griff in echte Nutzerdaten ohne zwingenden Grund). Für den Nikinger:
falls das Banner nach dem Deploy nicht von selbst erscheint, ist das der Grund, kein neuer Bug.

**Nikinger-Klarstellung zum Versionsschema, für spätere Bumps:** Versionsnummern spiegeln
Deploy-Zyklen, nicht Phasen — jeder Deploy erhöht die Zahl, Schema `x.y.z` wie in klassischer
Software-Versionierung, **nicht** neu bei 1 anfangend (diese Ära zählt als Fortsetzung von v2,
daher `v2.1`, nächster Deploy `v2.2` usw.).

**Nächster Schritt (konkret):** Nikinger führt `deploy.sh main` aus (Sudo-Neustart), bestätigt
danach live in allen drei Ansichten (Login, Liste, Editor) — das ist §3.3s letzter DoD-Punkt,
jetzt inklusive der weißen Wortmarke/Versionen — **und** dass das Banner nur die v2.1-Zeilen
zeigt (mit der oben benannten Unsicherheit im Hinterkopf). Danach ist **Step 7a vollständig
geschlossen** und der einzige noch offene UI-Rest aus `ITEM_MOVE_PLAN.md` erledigt. **Step 7**
(UI Dateisystem) ist als eigener Plan freigegeben (`/home/savefyx/.claude/plans/
serialized-seeking-aurora.md`, Nikinger-Entscheidung: Rename-Funktion bleibt draußen, Aufbau in
Unterschritten mit Checkpoints) — Ausführung beginnt in derselben Session, sobald dieser Nachtrag
committet ist. **Step 7b** setzt Step 7 voraus. Gate-A→B-Punkt 3 unverändert offen (realer
Purge-Lauf, frühestens 2026-08-28).
