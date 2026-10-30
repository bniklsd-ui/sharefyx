---
status: snapshot
purpose: Plan P10.5 Block 15 „Ultra" — die 22 Befunde des Ultra-Reviews (B1–B22) schließen, davor der Hotfix `v3.1.7` für B1; ausführungsreif gegen `main@2d45e66` (Anker = Datei:Zeile dieses Stands, Hotfix-Anker = Live-SHA `e5c834e`). Locks P10.5-X–AG, Schritte H0–H5 und 15.0–15.13, Abnahme P10.5-75–88, `[VERIFY]` V220–V232. Block 16 (Launch-Film) steht in `phase10_5_launch_film_plan.md`.
read-when: vor dem Hotfix, vor jedem Schritt von Block 15, oder wenn ein Befund B1–B22 gebaut, geprüft oder abgenommen wird
detail: L2
up: ../../phase10_5_finishing/CLAUDE.md
down:
  - phase10_5_ultra_review_v4.0.0.md            # 📕 die 22 Befunde mit Datei:Zeile, Schweregrad, Gewissheit — die Quelle dieses Plans
  - phase10_5_launch_film_plan.md               # 📗 Block 16: der Launch-Film (nach Block 15, vor Deploy D)
  - phase10_5_finishing_plan.md                 # 📕 der Phasenplan: §2 Arbeitsregeln, §2.5 Deploy-Ablauf, §5 Zählregel
  - ../../phase1_storage/storage/store.py       # der Kern — P1-Öffnung 16 (Lock P10.5-Z)
  - ../../phase2_mcp/mcpserver/tools.py         # Agentenfläche
  - ../../phase5_ui/webui/api.py                # Web-Fläche
updated: 2026-10-30 (Entwurf der Planungssession „Ultra" — Fable 5.1, Cloud; die Antworten des Nikingers A1–C2 vom 2026-10-30 sind eingearbeitet, der Plan ist freigegeben mit „alles wie empfohlen")
---
# P10.5 Block 15 „Ultra" — die 22 Befunde schließen, davor der Hotfix `v3.1.7`

> **Herkunft.** Das Ultra-Review (Prompt 4, `docs/PROMPTS.md`) hat am 2026-10-30 **22 Befunde**
> geliefert (1 kritisch, 4 hoch, 7 mittel, 10 niedrig) und `v4.0.0` als **nicht freigabefähig**
> bewertet. Der Bericht steht verbatim in `phase10_5_ultra_review_v4.0.0.md`. Diese Planungssession
> hat **jeden** Anker gegen `main@2d45e66` nachgelesen, B1 und B20 ohne Projektabhängigkeiten
> nachgestellt und die Threadpool-Behauptung zu B10 im installierten FastMCP 4.1.3 bestätigt
> (`fastmcp/tools/function_tool.py:538`, `call_sync_fn_in_threadpool`).
>
> **Antworten des Nikingers (2026-10-30), die diesen Plan formen:** A1 Hotfix B1 vorab als `v3.1.7`
> · A2 Ausführer **Claude Code** (Modellwahl: Empfehlung §2.1) · A3 P1-Öffnung 16 für den ganzen
> Block · A4 Typkoerzion im Kern, CRLF tolerant · A5 **Unarchive wird gebaut** (statt nur UI zu
> sperren) · A6 **alle 22 Befunde in diesem Block**, auch B12 und B21 · A7 kein FastMCP-Bump · A8
> Nummerierung Block 15, Zeilen ab P10.5-75, `[VERIFY]` ab V220 · C1 Reihenfolge Hotfix → Block 15 →
> Block 16 → Deploy D · C2 Haushaltsschritte ohne Rückfrage.

## Leseanleitung (Ausführer — zuerst lesen)

1. Lies `phase10_5_finishing_plan.md` §2 (Arbeitsregeln, Wegwerf-Instanz, Rückgabe-Auslöser) und
   §2.5 (Deploy-Ablauf). Sie gelten unverändert; §2 dieses Plans ergänzt sie nur.
2. Lies die Befunde B1–B22 im Review **im Wortlaut**, bevor du den zugehörigen Schritt baust. Der
   Plan zitiert sie nicht erneut; er nennt Anker, Änderung, Tests und das Fertig-Kriterium.
3. **Zeilennummern** gelten für `main@2d45e66` (Block 15) bzw. `e5c834e` (Hotfix). Prüfe jeden
   Anker mit `grep -n`, bevor du editierst — nach dem Hotfix-Merge verschieben sich Zeilen.
4. Ein Schritt ist fertig, wenn seine Tests grün sind, die **volle** Suite grün ist (bereinigte
   Umgebung, Plan P10.5 §2.1 Punkt 5), und der Phase-Head im **selben** Commit nachgezogen ist
   (Hard Rule 8). Jeder Schritt ist ein Commit.
5. **Gegenläufe** gibt es in Block 15 mechanisch für alle Befunde auf einmal (Schritt 15.13): die
   neuen Tests laufen gegen den Code der Block-Basis und müssen dort **rot** sein. Wo ein Schritt
   zusätzlich einen eigenen Gegenlauf nennt, ist er Pflicht.

## §0 Gelockte Entscheidungen

| Lock | Entscheidung | Herkunft |
|---|---|---|
| **P10.5-X** | **Hotfix `v3.1.7` vorab, nur B1.** Branch `hotfix/v3.1.7-b1` von `e5c834e` (Live-SHA Deploy B; der verwundbare Code ist dort byteweise derselbe wie in `main`, `store.py:1012/1030`). Inhalt: `asset_id`-Validierung in Store, Tool und Route, die vier B1-Tests, Badge `v3.1.7`, ein Update-Log-Block. Deploy durch den Nikinger (`deploy.sh hotfix/v3.1.7-b1`). Die Nummer `v3.1.7` ist frei: Deploy C ist nie gelaufen. Danach Merge nach `main` (§3 H4). | Nikinger A1, 2026-10-30 |
| **P10.5-Y** | **Ausführer = Claude Code** für Hotfix, Block 15 und Block 16 — datierte Abweichung von P10.5-B (opencode/M3.1 Flash), wie bei 14.7: Sicherheitsfixes im P1-Kern mit Wächter und Gegenlauf, der M3-Endpunkt endet am 2026-11-15. **Modellempfehlung** (Nikinger entscheidet): Opus 5.5 für Hotfix und 15.1–15.11 (alles, was `phase1_storage/storage/` oder `phase4_auth/` berührt), Sonnet 5.5 für 15.0, 15.12, 15.13 und Block 16. | Nikinger A2 |
| **P10.5-Z** | **P1-Öffnung 16, angekündigt und eng geprobt** (Zählung nach `phase1_storage/CLAUDE.md`): `storage/store.py`, `storage/index.py`, `storage/files.py`, `storage/history.py`, `storage/frontmatter.py`, `storage/models.py`. Abbruchkriterium am Blockende: `git diff --stat <block-basis>..HEAD -- phase1_storage/storage` nennt **nur** diese sechs Dateien. `INDEX_SCHEMA_VERSION` 4 → **5** (B12), keine Migration: der Index ist Ableitung, `index.connect()` verwirft und baut neu (Hard Rule 2). | Nikinger A3; P10.5-F |
| **P10.5-AA** | **Typkoerzion im Kern (B5), CRLF tolerant (B20).** Handeditierte Dateien sind erlaubt (Phase-1-Mission); YAMLs implizite Typen (`title: 2026` → `int`) sind kein Wille des Menschen. Skalare in `id/space/type/title/status` werden zu `str`, Listenfelder zu `list[str]`; `version` zu `int` oder Fehler. CRLF-Dateien werden beim Lesen LF-normalisiert, der nächste Write schreibt LF (bewusst keine Byte-Identität für CRLF — vorher waren sie gar nicht lesbar). Was sich nicht koerzieren lässt, überspringt der Neuaufbau mit `logger.critical` und Pfad (B3). | Nikinger A4; Review B5/B20 |
| **P10.5-AB** | **Unarchive = reiner Statuswechsel aus `archived`.** `Store.update()` erlaubt auf einem archivierten Item **genau** `{"status": <offener Status des Typs>}`; das Item wandert aus `_archive/` an die **Space-Wurzel** (der Ordner ist für archivierte Items nicht gespeichert), `version+1`, Commit `unarchive <id>`. Jedes andere Feld bleibt gesperrt, bis das Item wiederhergestellt ist. MCP (`update_item(status=…)`) und REST (`PATCH {version, status}`) brauchen dafür keinen neuen Parameter. UI: archivierte eigene Items öffnen **nur lesend** mit Knopf „Wiederherstellen"; `archived` verschwindet aus der Status-Auswahl des Editors (Archivieren bleibt der eigene Knopf). Entscheidung H (kein Delete) und K (Archivieren über `update_item`) bleiben unberührt. | Nikinger A5; Review B16 |
| **P10.5-AC** | **B12 = Index-first-Suche.** `Store.search()` filtert, sortiert und blättert ausschließlich über Indexspalten; Dateien liest sie **nur** bei `in_body=True`. Dafür trägt der Index ab Schema 5 zusätzlich `snippet`, `updated_by`, `created_by`. **Hard Rule 2 bleibt gewahrt:** vor dem Filtern vergleicht `search()` je Indexzeile `stat()` (mtime, size) mit der Zeile und liest **nur** veränderte Dateien nach (`repair_drift=False`, kein Write) — eine Hand-Änderung ist damit sofort sichtbar, ohne jede Datei zu lesen. `_STORE_FETCH_LIMIT` steigt in beiden Adaptern auf 50 000. REST-Schreibrouten rufen den Store über `asyncio.to_thread` (wie `_overview`). B10 ist damit mitgelöst: der ganze Lesevorgang läuft unter `Store._lock`, eine verschwundene Datei wird übersprungen, nicht geworfen. | Nikinger A6; Review B10/B12 |
| **P10.5-AD** | **B21 = Kappe für `auth_requests`, Eingriff in `phase4_auth/` nach dem P10-C-Muster.** `AuthStore.create_auth_request()` löscht zuerst abgelaufene Zeilen (opportunistisch, nicht erst der tägliche Purge) und hält je `client_id` höchstens **20** offene Anfragen (FIFO: die ältesten fliegen). **Freigabe des Nikingers für den Eingriff: „alles gleich fixen", 2026-10-30** — mit der Freigabe dieses Plans bestätigt. Vorher wird gemessen (15.11), weil B21 im Review nur „vermutet" ist. | Nikinger A6; P10-C |
| **P10.5-AE** | **Eine Space-Namensregel (B6):** `files.validate_space_name()` — die Regel aus `acl.create_space()` (kein `/`, kein führender Punkt, kein reservierter Name) plus: nicht leer, kein Whitespace am Rand, kein `\`/NUL. Aufrufer: `acl.create_space()`, `Store.create()`, `Store.move()`, `Store.rename_space()`. Die Adapter brauchen keine eigene Prüfung — der Kern wirft `ValidationError`, beide Flächen bilden sie bereits ab (`invalid:` bzw. 422). | Review B6 |
| **P10.5-AF** | **Eine Versionsquelle (B17):** `mcpserver.__version__` ist die Produktversion und steht **gleich** dem Badge in `app.html`. Ein Wächter vergleicht beide; `health_gate.sh` prüft zusätzlich `/health`. Deploy-Schritt D2 (Plan P10.5 §2.5) nennt ab jetzt **beide** Stellen. Die `version` in `pyproject.toml` bleibt die Paketversion (0.1.0) und ist nicht gemeint. | Review B17 |
| **P10.5-AG** | **Reihenfolge und Pins.** Hotfix → Block 15 → Block 16 → Deploy D `v4.0.0`. Kein FastMCP-Bump vor dem Release: 4.1.4 (2026-10-26) ändert keine von uns genutzte Schnittstelle, die zwei Sicherheitseinträge betreffen FastMCP-Proxies (nicht im Einsatz) und `certifi ≥ 2026.10.19` (bereits gepinnt). Prüfpunkt erneut bei der Deploy-D-Vorbereitung (V231). Betriebsposten daraus für den Nikinger: der OS-Truststore der VM nach dem eMudhra-CA-Vorfall (FastMCP-Hinweis 4.1.3) — `apt`-Update, kein Code. | Nikinger A7, C1; Recherche 2026-10-30 |

**Was Block 15 ausdrücklich nicht tut:** kein neues Werkzeug, kein neues Feld außer Indexspalten, kein
Light-Mode, kein Papierkorb-Räumen (LG-5), kein Umbau der Rechtepolitik über B4 hinaus, kein
Range-Pin, keine Änderung an `flows.py` (P10.5-O bleibt).

## §1 Ausgangslage (gemessen 2026-10-30, Planungssession)

- **Repo:** `main@2d45e66` = Branch-Basis. **Live:** `v3.1.6` (`e5c834e`, Deploy B). Deploy C
  (`v3.1.7`) wurde vorbereitet, nie deployt; `main` trägt bereits Badge `v4.0.0` und den
  Update-Log-Block `## 2026-10-26`.
- **Testbasis** (Scratchpad-venv aus `constraints.txt`, bereinigte Umgebung): **1654 grün, 5 rot** —
  alle fünf in `phase5_ui/tests/test_deploy_scripts.py` (`authbackup`/`restore_auth_check`), weil das
  `sqlite3`-Binary im Container fehlt. Identisch mit dem Review-Befund, kein Codebefund.
- **Step 0:** `doc_health` 0; Oversize nur 📕/📦; Indexzeilen vollständig. Luft-Befunde: `docs/INDEX.md`
  5 B unter dem Reserve-Wächter, `phase2_mcp/CLAUDE.md` 329 B unter dem Softcap,
  `phase10_5_finishing/CLAUDE.md` 1.478 B — die Planungssession hat INDEX und P10.5-Head Luft
  verschafft (Kürzungs-Archiv, Modulstatus-Archiv); der P2-Head ist Schritt 15.0.
- **Anker-Verifikation:** alle 22 Datei:Zeile-Anker stimmen (Tabelle in §4 je Schritt). B1 mit
  `pathlib` reproduziert (`'../../../bob/.share.*'` → `.share.yml`), B20 reproduziert
  (`FrontmatterError` bei CRLF), YAML-Typen zu B5 reproduziert (`title: 2026` → `int`).
- **PyPI 2026-10-30:** fastmcp 4.1.4 / 4.2.0a1 (Pre-Release), mcp 2.3.0 (= Pin), starlette 1.10.0
  (Pin 1.9.0), pydantic 2.14.2 (Pin 2.14.1). MCP-Spec: 2026-07-28 weiterhin „Current".
- **Starlette 1.9.0** `FileResponse` kennt `Range`/`Accept-Ranges` (im installierten Paket gelesen,
  `starlette/responses.py:324, 367`) — relevant für Block 16, hier als V222 ✅ vorgemerkt.

## §2 Arbeitsregeln (ergänzend zu Plan P10.5 §2)

### 2.1 Ausführer, Modell, Session

Claude Code (P10.5-Y). Eine Session je Schritt; Blockbasis per `git rev-parse HEAD` in den
Session-Block. Vor dem ersten Edit eines Schritts: Anker mit `grep -n` prüfen. **Empfehlung Modell**
(§0 P10.5-Y): Opus 5.5 überall, wo `phase1_storage/storage/` oder `phase4_auth/` angefasst wird
(Hotfix, 15.1–15.11), Sonnet 5.5 für Haushalt, Doku, Abschluss und Block 16. Der Plan ist für Sonnet
geschrieben; Opus soll ihn **nicht** neu herleiten, sondern Anker verifizieren und Drift datiert
notieren.

### 2.2 Erlaubte Pfade (Block 15)

`phase1_storage/storage/{store,index,files,history,frontmatter,models}.py` (P10.5-Z) ·
`phase1_storage/scripts/space_cli.py` (nur Ausgabe `files_skipped`) · `phase1_storage/tests/**` ·
`phase2_mcp/mcpserver/{tools,logging_setup,request_log,__init__}.py` · `phase2_mcp/tests/**` ·
`phase5_ui/webui/{api,security}.py`, `phase5_ui/webui/static/{app.html,js/editor.js,js/api.js,app.css}`
· `phase5_ui/tests/**` · `phase4_auth/authserver/store.py` (nur B21, P10.5-AD) · `phase4_auth/tests/**`
· `phase8_5_picker_release/scripts/health_gate.sh` (Gate 5b) · `phase7_spaces_admin/tests/**` (B4, B6)
· `phase10_5_finishing/{probes,tests}/**` · `README.md`, `docs/UPDATE_LOG.md`, Phase-Heads, `docs/INDEX.md`,
`phase10_inventory/BAUSTELLENREGISTER.md` (Abhaken). **Tabu:** `authserver/flows.py`, `routes.py`,
`graph.js`, `markdown.js`, systemd-Units.

### 2.3 Wegwerf-Instanz, Stopp, Umgebung

Wie Plan P10.5 §2.3 und Block 14.7 §6: Port 8799, tmp-`DATA_ROOT`, tmp-`auth.sqlite3`, Vorlage
`phase10_inventory/probes/p10_wegwerf.py`, Stopp **nur** über die PID-Datei (Hard Rule 9), Tests mit
`env -u PYTHONPATH $(env | grep -oE '^(SHAREFYX_|SFX_|SPACE_)[A-Z_]*' | sed 's/^/-u /')`. Playwright
aus `~/.claude-code-tools/e2e-venv`. Nie gegen `DATA_ROOT`, die echte `auth.sqlite3`, den Keyring
oder den Dienst.

### 2.4 Der mechanische Gegenlauf (Schritt 15.13)

```bash
basis=$(git rev-parse <block-basis>)                      # steht im Session-Block von 15.0
git worktree add /tmp/b15-gegenlauf "$basis"
PYTHONPATH=/tmp/b15-gegenlauf/phase1_storage:/tmp/b15-gegenlauf/phase2_mcp:/tmp/b15-gegenlauf/phase4_auth:/tmp/b15-gegenlauf/phase5_ui \
  .venv/bin/python -m pytest -q <nur die in Block 15 neuen Testdateien/-funktionen> -p no:cacheprovider
git worktree remove /tmp/b15-gegenlauf
```

`PYTHONPATH` steht vor den `.pth`-Einträgen der editierbaren Installation, die alten Pakete gewinnen
also den Import. **Erwartung:** jeder neue Test rot, kein alter berührt. Die Zahl der roten Tests steht
im Session-Block; weicht sie von der Zahl der neuen Tests ab, ist das ein Befund (ein Test, der am
alten Code grün ist, prüft nichts).

### 2.5 Rückgabe-Auslöser (zusätzlich zu Plan P10.5 §2.4)

- Ein `[VERIFY]` aus §6 fällt anders aus als angenommen und der Schritt hängt davon ab.
- `git diff --stat -- phase1_storage/storage` nennt eine Datei außerhalb von P10.5-Z.
- Ein Test außerhalb des eigenen Schritts wird rot und der Diff erklärt es nicht offensichtlich.
- Die Messung in 15.11 zeigt, dass `auth_requests` live **nicht** wächst (dann B21 als „Wissen"
  schließen statt bauen — Entscheidung Nikinger).

## §3 Hotfix `v3.1.7` — nur B1 (Lock P10.5-X)

**Anker am Live-Stand `e5c834e`:** `storage/store.py:1012` (`get_asset`) und `:1030` (`delete_asset`),
je `target_dir.glob(f"{asset_id}.*")` · `storage/files.py:41` `ASSET_ID_RE`, `:54` `ASSET_MIME_TYPES`,
`:82` `asset_path()` · `mcpserver/tools.py:1031` `get_item_asset`, `:1057` (Metadaten-Zweig),
`:1073` (`store.get_asset`) · `webui/api.py:1420` `_assets_get_one`, `:1431`; `:1448` `_assets_delete`,
`:1460` · `webui/static/app.html:20` Badge `v3.1.6` · `docs/UPDATE_LOG.md` oberster Block `## 2026-10-23`.

| Schritt | Inhalt | Fertig, wenn |
|---|---|---|
| **H0** | `git fetch origin main && git checkout -b hotfix/v3.1.7-b1 e5c834e`; venv aus dem `constraints.txt` **dieses** Stands (`scripts/dev_install.sh`); volle Suite als Basis (erwartet grün bis auf `sqlite3`-Tests, falls das Binary fehlt). Blockbasis notieren. | Suite-Zahl notiert |
| **H1** | **Der Patch = Schritt 15.1, auf dem alten Stand**: `files.require_asset_id()`, `files.ASSET_EXTENSIONS`, `files.find_asset_path()`; `get_asset`/`delete_asset` ohne `glob`; Prüfung in `get_item_asset` (vor `store.acl_of`) und in beiden Asset-Routen (422). Die vier Tests aus 15.1 **mit denselben Namen** (der Merge dedupliziert). | Tests grün, volle Suite grün |
| **H2** | Badge `app.html:20` → `v3.1.7`; `docs/UPDATE_LOG.md` neuer oberster Block `## <Deploy-Tag>` mit **einer** Zeile: „Behoben: Bild-IDs werden jetzt streng geprüft — ein Bild lässt sich nur noch über seine eigene ID abrufen oder entfernen." **Kein Head-Edit auf dem Hotfix-Branch** (Merge-Hygiene); Hard Rule 8 wird auf `main` in 15.1 erfüllt — datierte Ausnahme, hier begründet. | Commit, Push `hotfix/v3.1.7-b1` |
| **H3** | **Nikinger:** `deploy.sh hotfix/v3.1.7-b1` (Umgebungszeilen wie Plan P10.5 §2.5 D4), dann `health_gate.sh --expected-version=v3.1.7 --require-todays-update-log --expected-sha=<sha>`. **Live-Probe (Nikinger, über den eigenen Connector):** `get_item_asset(item_id=<eigenes Item>, asset_id="../../../x")` → `invalid: …`; ein echtes Asset lädt weiterhin. Beide Ausgaben in den Session-Block. | `health_gate` 9/9 OK, Live-Probe wie erwartet |
| **H4** | `git checkout main && git merge --no-ff hotfix/v3.1.7-b1`. Erwartete Konflikte: `app.html` (Badge → **`v4.0.0` behalten**), `docs/UPDATE_LOG.md` (die Blöcke von `main` behalten; die Hotfix-Zeile als **letzte Zeile in den Block `## 2026-10-26`** übernehmen, den Hotfix-Tagesblock **nicht** auf `main` führen — wer `v3.1.7` sah, hat ihn gesehen), evtl. Kontextdrift in `tools.py`/`api.py`. Danach Suite grün. | Merge-Commit auf `main`, Suite grün |
| **H5** | Deploy-Tabelle im Head: neue Zeile `H | v3.1.7 | <sha> | 9/9 OK | Hotfix B1 — live seit <Datum>`; Modulzeile 15 Status „Hotfix live". | Head im selben Commit |

**Warum kein Head-Edit auf dem Branch (H2):** der Head auf `e5c834e` ist 70 Commits alt; jede Zeile
dort würde beim Merge kollidieren und müsste von Hand gelöst werden — genau die Fehlerklasse, die
Hard Rule 8 vermeiden will. Der Head wird deshalb auf `main` nachgezogen, am selben Tag, mit dem
Verweis auf den Hotfix-SHA.

## §4 Block 15 — die Schritte

Je Schritt: **Anker** (Datei:Zeile auf `2d45e66`) · **Änderung** (exakte Namen) · **Tests**
(Datei::Funktion; Wächter prüft den Fix, Gegenlauf macht ihn mechanisch rot — §2.4) · **Fertig, wenn**.

### 15.0 Haushalt (Sonnet, vor dem ersten Fix)

1. **Abnahmezeilen P10.5-75–88** (§5) als ⬜ in die Head-Tabelle; `tests/test_head_rules.py`
   `test_the_acceptance_sum_matches_the_table` **74 → 92** (zwei Stellen, Docstring datiert) —
   zusammen mit den vier Zeilen 89–92 aus dem Film-Plan; Plan P10.5 §5: datierter Nachtrag
   „+18 Zeilen aus Block 15/16".
2. **P2-Head unter den Softcap bringen** (`phase2_mcp/CLAUDE.md`, 40.631 B): die elf
   Zählkorrektur-Absätze (`**[2026-07-28 Korrektur, P4 Step 6a]**` … `**[2026-08-20, Phase 6.5 Step B4]**`,
   Zeilen ~196–286) unter eine neue Überschrift `### Zählkorrekturen der Test-Summe (2026-07-28 –
   2026-08-20), Chronik` stellen und per `scripts/move_sections.py phase2_mcp/CLAUDE.md
   phase2_mcp/SESSIONS_ARCHIVE.md "### Zählkorrekturen …"` verbatim verschieben (Zeiger bleibt).
   Danach `wc -c` < 32 KB.
3. **Probe-Skelett** `phase10_5_finishing/probes/p105_b15_ultra_probe.py` nach dem Muster
   `p105_b2_rights_probe.py` (eigene Wurzel `/tmp/opencode/sharefyx-wegwerf-p105-b15`, Principals
   `alpha`/`bob`, Team-Space `team`): Befehle `setup · start · cells · perf · gegenlauf · stop ·
   cleanup`; Zellen kommen je Schritt dazu (§5 nennt sie).
4. **Register:** Zeilen BG-4 (Befunde) und UI-11 (Film) existieren seit der Planungssession;
   abgehakt wird am Blockende (15.13).

**Fertig, wenn:** Head trägt 92 Abnahmezeilen (18 ⬜ neu), `test_head_rules` grün, P2-Head < 40 KB,
`doc_health` 0, Probe-Skelett `setup/start/stop` an der Wegwerf-Instanz einmal gefahren.

### 15.1 B1 + B15 — `asset_id` validieren, nie wieder globben (Opus)

**Anker:** `store.py:1477` `get_asset`, `:1483` glob · `:1491` `delete_asset`, `:1501` glob ·
`files.py:41` `ASSET_ID_RE`, `:54` `ASSET_MIME_TYPES`, `:82` `asset_path()` · `tools.py:1065`
`get_item_asset`, `:1097` Metadaten-Zweig (`store.list_assets`), `:1107` `store.get_asset` ·
`api.py:1699` `_assets_get_one`, `:1727` `_assets_delete`.

**Änderung.**
- `files.py`: `ASSET_EXTENSIONS: tuple[str, ...] = ("png", "jpg", "gif", "webp")` (die Endungen aus
  `ASSET_MIME_TYPES` plus WebP, das `sniff_image_mime()` gesondert erkennt);
  `def require_asset_id(asset_id: str) -> str` (nicht-`str` oder kein `ASSET_ID_RE.fullmatch` →
  `ValidationError(f"Ungültige asset_id: {asset_id!r} — erwartet ast_<8 hex>")`);
  `def find_asset_path(data_root, space, item_id, asset_id) -> Path | None` (ruft
  `require_asset_id`, baut je Endung `asset_dir(...) / f"{asset_id}.{ext}"`, gibt den ersten
  existierenden Pfad zurück — **kein** `glob`, keine Wildcards).
- `store.py` `get_asset`/`delete_asset`: erste Zeile `asset_id = files.require_asset_id(asset_id)`;
  `path = files.find_asset_path(self._data_root, row["space"], item_id, asset_id)`;
  `if path is None: raise ItemNotFound(asset_id)`; Rest mit `path` statt `matches[0]`.
- `tools.py` `get_item_asset`: **vor** `store.acl_of(item_id)`:
  `if not isinstance(asset_id, str) or not files.ASSET_ID_RE.fullmatch(asset_id): raise
  map_storage_error(ValidationError(...)) from None` → `invalid:`-Präfix (stabiler Fehlervertrag).
  Import `from storage import files` ergänzen.
- `api.py` `_assets_get_one`/`_assets_delete`: dieselbe Prüfung → `ApiError("validation_failed",
  "'asset_id' hat nicht die Form ast_<8 hex>.")` (422), **vor** `store.acl_of`.

**Tests.** `phase1_storage/tests/test_files.py::test_require_asset_id_accepts_only_the_documented_form`
(gültig · `ast_ZZZZZZZZ` · `*` · `../../../bob/.share` · `""` · `123`) ·
`test_files.py::test_find_asset_path_never_leaves_the_asset_directory` ·
`phase1_storage/tests/test_store.py::test_get_asset_rejects_a_traversal_id_and_leaves_bobs_files_alone`
(Bobs Item und `.share.yml` existieren; Alice' Item hat ein Asset; `get_asset(alice_item,
"../../../bob/.share")` → `ValidationError`; `delete_asset` ebenso; Bobs Dateien unverändert, keine
Commit-Zahl erhöht) · `test_store.py::test_get_asset_rejects_wildcards` (B15: `"*"`, `"ast_*"`) ·
`phase2_mcp/tests/test_tools.py::test_get_item_asset_rejects_a_malformed_asset_id_before_touching_the_store`
(`invalid:`; `store.get_asset` per Monkeypatch zählt 0 Aufrufe) ·
`phase5_ui/tests/test_api.py::test_asset_routes_reject_a_malformed_asset_id_with_422` (GET + DELETE mit
`ast_zz` und `%2A`).

**Fertig, wenn:** Tests grün, volle Suite grün, `mcp_smoke.py --json` 17/17, Probe-Zelle `b1` grün
(zwei Principals an der Wegwerf-Instanz, derselbe Aufruf wie im Review → `invalid:`), Head-Zeile 15
und `phase1_storage/CLAUDE.md` (Öffnung 16 angekündigt) nachgezogen. Nach dem Hotfix-Merge besteht
dieser Schritt aus **Verifikation plus Head** — der Code ist dann schon auf `main`.

### 15.2 B2 + B22 — Umbenennen robust, der Start scheitert nie an einem Marker (Opus)

**Anker:** `store.py:547` `rename_folder`, `:930` `_rename_directory` (`:942` `os.rename`), `:777`
`_resume_pending_rename` (aufgerufen `:315` in `__init__`), `:806` `_resume_folder_rename`, `:623`
`rename_space` · `api.py:759` `_spaces_rename_folder` (`:792` fängt nur `ValidationError`,
`ValueError`), `:689` `_spaces_rename_space` · `history.py:86` `commit`, `:106` Fehlerzweig.

**Änderung.**
- `_rename_directory`: vor `os.rename` → `new_dir.parent.mkdir(parents=True, exist_ok=True)` (gilt
  damit für Rename **und** Wiederaufnahme; verschachtelte Ziele sind laut `MAX_FOLDER_DEPTH = 2`
  legitim).
- `_resume_pending_rename`: den Körper nach `marker = …` in `try/except Exception` hüllen →
  `logger.critical("Rename-Wiederaufnahme gescheitert — der Marker bleibt liegen, der Dienst startet:
  %s", marker, exc_info=True)`; **kein** Re-Raise. Der Marker bleibt (nichts wird still verworfen), der
  Store ist benutzbar.
- `api.py` beide Rename-Routen: `except (ValidationError, ValueError, OSError)`; `OSError` →
  `ApiError("validation_failed", f"Umbenennen fehlgeschlagen: {exc.strerror or exc}")`.
- `history.commit` (B22): schlägt `git commit` fehl, zuerst `_run_git(data_root, "status",
  "--porcelain")`; ist der Rückgabewert 0 und die Ausgabe leer → `logger.info("nichts zu committen:
  %s", message)` und return; sonst wie bisher `critical`. Kein zusätzlicher Git-Aufruf im Normalpfad.

**Tests.** `test_store.py::test_rename_folder_into_a_missing_parent_creates_it_and_moves_the_share_file`
(`projekte` → `archiv/projekte` ohne `archiv/`; Index == `rebuild_index`) ·
`test_store.py::test_a_poisoned_rename_marker_never_prevents_store_start` (Marker `kind=folder`, `old`
und `new` existieren nicht → `Store()` startet; Marker liegt noch; `caplog` CRITICAL) ·
`test_store.py::test_resume_of_a_rename_whose_target_parent_is_missing_completes` ·
`test_store.py::test_rename_of_an_empty_folder_logs_no_critical` ·
`phase1_storage/tests/test_history.py::test_commit_without_changes_logs_info_not_critical` ·
`test_api.py::test_rename_folder_into_a_missing_parent_is_200` ·
`test_api.py::test_rename_folder_os_error_is_422_not_500` (Monkeypatch `os.rename` → `PermissionError`).

**Fertig, wenn:** Tests grün, Probe-Zelle `b2` (Rename in fehlenden Elternordner über die Web-API,
danach Neustart der Wegwerf-Instanz mit absichtlich vergiftetem Marker → `/health` 200).

### 15.3 B3 + B20 — der Neuaufbau überspringt, was er nicht lesen kann (Opus)

**Anker:** `index.py:274` `rebuild_index`, `:285` `DELETE FROM items`, `:291` `row_from_file`, `:197`
`replace_item_links` (`conn.commit()` je Aufruf — committet den `DELETE` nach der ersten Datei) ·
`index.py:228` `row_from_file` · `store.py:321` `self.rebuild_index()` in `__init__` · `models.py:124`
`IndexStats` · `frontmatter.py:15` `_FRONTMATTER_RE`, `:54` `parse` ·
`phase1_storage/scripts/space_cli.py` (`reindex`-Ausgabe).

**Änderung.**
- `models.py`: `IndexStats.files_skipped: int = 0` (additiv, Default — kontraktverträglich).
- `index.py`: `replace_item_links(conn, src_id, rows, *, commit: bool = True)`; `rebuild_index`
  ruft es mit `commit=False`, committet **einmal** am Ende, und rollt bei einer unerwarteten
  Ausnahme zurück (`try: … except BaseException: conn.rollback(); raise`) — der alte Index bleibt
  dann stehen. Je Datei: `try: row = row_from_file(...) except Exception as exc:
  logger.critical("Index-Neuaufbau: %s übersprungen (%s: %s)", md_path, type(exc).__name__, exc);
  skipped += 1; continue`. **Warum `Exception` und nicht eine Liste:** `FrontmatterError`, `KeyError`
  (fehlendes Pflichtfeld), `UnicodeDecodeError`, `yaml.YAMLError`, `ValueError` (Typkoerzion aus
  15.4) — und jede weitere Datenkrankheit darf den Start nie verhindern; der Pfad steht im Log.
- `frontmatter.parse`: `text = text.replace("\r\n", "\n")` vor dem Match (B20, P10.5-AA).
- `space_cli.py reindex`: `files_skipped` mit ausgeben.

**Tests.** `test_index.py::test_rebuild_index_skips_an_unparseable_file_and_keeps_the_rest`
(`alice/README.md` ohne Frontmatter + drei Items → 3 indiziert, `files_skipped == 1`, CRITICAL nennt
`README.md`) · `test_index.py::test_rebuild_index_is_one_transaction` (Monkeypatch `row_from_file`
wirft beim zweiten Aufruf `RuntimeError` → Ausnahme propagiert, Indexzeilen **wie vorher**) ·
`test_store.py::test_store_start_with_a_foreign_md_in_a_space_works` (frischer Index + README →
`Store()`, `get()` der Items ok) · `phase1_storage/tests/test_frontmatter.py::test_crlf_parses_and_serializes_lf`
· `test_index.py::test_rebuild_index_counts_a_crlf_item`.

**Fertig, wenn:** Tests grün; Probe-Zelle `b3`: Wegwerf-`DATA_ROOT` mit `README.md` und einer
CRLF-Datei, Index gelöscht, Neustart → `/health` 200 und `search_items` zählt alle echten Items.

### 15.4 B5 + B8 — Typen im Kern, nichts wird halb geschrieben (Opus)

**Anker:** `store.py:133` `_item_from_text` (`:140` title, `:141` status, `:144` tags), `:1054`
`' '.join(item.tags)`, `:476` `slugify(item.title)` in `_write_item_file`, `:460` `_write_item_file`
(Links nach dem Write: `:481` `_replace_links_for_item`), `:1080` `create`, `:1150` `update` ·
`index.py:238` Felder in `row_from_file` · `api.py:1318` POST-`kwargs`, `:1480` PATCH-`changes` ·
`tools.py:524` (pydantic schützt MCP; V220).

**Änderung.**
- `models.py`: `def normalize_fields(fields: dict) -> dict` — Kopie mit: `id/space/type/title/status`
  → `str(v)` falls nicht `str` und nicht `None`; `tags/links/share_read/share_write` → `None`→`[]`,
  Skalar→`[str(v)]`, Liste→`[str(x) for x in v if x is not None]`; `version` → `int(v)` (bei
  `ValueError`/`TypeError`: `ValidationError` mit Feldname). Aufrufer: `store._item_from_text` (direkt
  nach `parse_frontmatter`) und `index.row_from_file` (ebenso).
- `store.py`: `' '.join(map(str, item.tags))` (Gürtel und Hosenträger); neue Helfer
  `_require_str(name, value)` und `_require_str_list(name, value)` → `ValidationError`; `create()`
  prüft `title`, `body`, `type`, `status` (falls gesetzt), `folder`, `tags`, `links`, `share_*`;
  `update()` prüft dieselben Schlüssel im `changes`-Durchlauf (`known_updatable`-Zweig und
  `share_*`-Zweig). `MAX_TITLE_CHARS = 300` (siehe 15.6) gehört in dieselbe Prüfung.
- `_write_item_file`: Linkzeilen **vor** `files.atomic_write` berechnen — `_replace_links_for_item`
  wird zu `_link_rows(item) -> list[tuple[str, str]]` (reine Rechnung) + `index.replace_item_links`
  nach dem Upsert. Ein Fehler in der Extraktion kommt damit **vor** dem Write.
- REST: keine zweite Typprüfung — `ValidationError` aus dem Kern wird schon zu 422
  (`_map_store_error`). Nur `_items_post`: der bestehende `body`-Check bleibt.

**Tests.** `phase1_storage/tests/test_models.py::test_normalize_fields_coerces_yaml_scalars` (Tabelle:
`title: 2026`→`"2026"`, `tags: [2026, "a"]`→`["2026","a"]`, `tags: x`→`["x"]`, `links: null`→`[]`,
`version: "3"`→`3`, `version: "x"`→`ValidationError`) ·
`test_store.py::test_search_survives_integer_tags_in_a_hand_edited_file` (Datei von Hand mit
`tags: [2026]`, `rebuild_index`, `search(query="2026")` findet sie) ·
`test_store.py::test_update_survives_an_integer_title_in_a_hand_edited_file` ·
`test_store.py::test_create_rejects_non_string_title_body_and_tags` (`title=123`, `body=5`,
`tags="abc"`, `tags=[1]`, `links=[None]`) ·
`test_store.py::test_update_with_a_non_string_body_writes_nothing` (SHA der Datei und `version`
unverändert, Commit-Zahl unverändert) · `test_api.py::test_post_items_with_integer_tags_is_422` ·
`test_api.py::test_patch_items_with_integer_title_folder_or_body_is_422_and_leaves_the_item_untouched`
· `test_tools.py::test_create_item_rejects_integer_tags` (V220: pydantic weist `[1,2]` für `list[str]`
ab — sonst fängt der Kern).

**Fertig, wenn:** Tests grün; Probe-Zelle `b5`: Hand-Edit `tags: [2026]` + `title: 2026` an der
Wegwerf-Instanz → `search_items(query=…)` und Web-Suche antworten, `update_item` schreibt.

### 15.5 B4 — Mitglieder verwaltet, wer den Space verwaltet (Opus)

**Anker:** `api.py:876` `_space_members_post`, `:897` `_space_members_delete` (je
`permissions.can_write(session.space, space)`), `:845` `manageable` in `_space_members_get` ·
`permissions.py` `SharePolicy.manages_space()`.

**Änderung.** Alle drei Stellen → `permissions.manages_space(session.space, space)`; Fehlertext
„Mitglieder verwaltet nur der Eigentümer des Space oder ein Team-Mitglied mit Schreibrecht."
`manageable` zeigt damit, was die Routen tun.

**Tests.** `phase7_spaces_admin/tests/test_space_admin_api.py::test_a_write_guest_cannot_manage_members_of_a_foreign_home_space`
(Bob gewährt Alice `write:`; Alice POST/DELETE Mitglieder → 403; GET `manageable: false`) ·
`::test_a_team_space_writer_still_manages_members` (200). V221: die Fixture muss das
`is_home_space`-Prädikat setzen (sonst ist jeder Space „Team").

**Fertig, wenn:** Tests grün; Probe-Zelle `b4` (dieselbe Matrix an der Wegwerf-Instanz: `bob`-Home
mit `write: [alpha]` → 403; `team` → 200).

### 15.6 B6 + B7 + B13 + B14 — Namen, Längen, IDs, Offsets (Opus)

**Anker:** `tools.py:702` `target_space`, `:883` `update_item(space=)` · `api.py:1288`, `:1378` ·
`acl.py:282` `create_space`-Regel · `store.py:656` `rename_space`-Regel, `:1080` `create`, `:1302`
`move`, `:1129` `files.generate_id()` · `files.py:351` `slugify`, `:362` `item_filename`, `:373`
`validate_folder`, `:412` `atomic_write` (mkstemp → `OSError 36`) · `tools.py:541` Slice mit
ungeklemmtem `offset` · `store.py:1016` `search(limit, offset)`.

**Änderung.**
- **B6:** `files.validate_space_name(name) -> str` (P10.5-AE); `acl.create_space()` ruft sie statt
  der Inline-Regel (`AclWriteError` bleibt der dortige Fehlertyp: `except ValidationError as exc:
  raise AclWriteError(str(exc))`); `Store.create()` erste Zeile `space =
  files.validate_space_name(space)`; `Store.move()` bei `space is not None`; `Store.rename_space()`
  für `new`. Die Adapter bleiben, wie sie sind (der Kern wirft, die Abbildung existiert).
- **B7:** `files.SLUG_MAX_BYTES = 80`; `slugify(title)` kürzt das Ergebnis auf höchstens 80
  UTF-8-Bytes, bevorzugt an einem `-`, strippt `-`, fällt auf `"item"` zurück (gilt über
  `validate_folder` auch für Ordnersegmente). `store.MAX_TITLE_CHARS = 300`; `create()`/`update()`
  → `ValidationError("Titel länger als 300 Zeichen")`. Dateiname damit ≤ 4+1+8+2+80+3 = 98 Bytes.
- **B13:** `Store._new_item_id()`: bis zu 8× `files.generate_id()`, bis `index.get_item_row(conn,
  id) is None`; danach `RuntimeError("keine freie Item-ID nach 8 Versuchen")`. `create()` nutzt sie.
- **B14:** `tools.search_items`: `offset = max(0, offset)` direkt nach `clamped_limit`;
  `Store.search`: `offset = max(0, offset)`, `limit = max(1, limit)`.

**Tests.** `test_files.py::test_validate_space_name_rules` (Tabelle) ·
`test_store.py::test_create_and_move_reject_a_space_name_with_a_trailing_slash` ·
`phase7_spaces_admin/tests/test_acl_write.py::test_create_space_uses_the_shared_space_name_rule` ·
`test_tools.py::test_create_item_with_a_slashed_space_name_is_invalid_not_a_foreign_item` ·
`test_api.py::test_post_items_with_a_slashed_space_is_422` ·
`test_files.py::test_slugify_caps_at_80_bytes_on_a_dash_boundary_and_handles_multibyte` ·
`test_store.py::test_a_300_char_title_is_rejected_and_a_200_umlaut_title_writes_a_short_filename` ·
`test_store.py::test_update_to_a_long_cjk_title_renames_without_oserror` ·
`test_store.py::test_create_retries_on_an_id_collision` (Monkeypatch `generate_id` liefert erst eine
belegte, dann eine freie ID) · `test_tools.py::test_search_items_clamps_a_negative_offset`
(`offset=-3` → `offset: 0`, `truncated` korrekt).

**Fertig, wenn:** Tests grün; Probe-Zellen `b6` (`create_item(space="team/")` → `invalid:` auf MCP
**und** 422 auf REST) und `b7` (200 Umlaute → 201/Quittung, Dateiname ≤ 100 B).

### 15.7 B9 — das Einladungs-Token verlässt das Log (Opus)

**Anker:** `logging_setup.py:11` `_TOKEN_SEGMENT_RE`, `:38` `_SECRET_PATTERNS` · `request_log.py:221`
Redaktion nur über `_TOKEN_SEGMENT_RE` · `routes_auth.py:291` `/ui/invite/{token}`.

**Änderung.** `logging_setup.py`: `_INVITE_SEGMENT_RE = re.compile(r"(/ui/invite/)[^\s\"'/?#]+")`,
in `_SECRET_PATTERNS` aufnehmen; neu `def redact_path(path: str) -> str` (wendet beide Segment-Muster
an). `request_log.py:221`: `path = redact_path(scope.get("path", ""))`.

**Tests.** `phase2_mcp/tests/test_request_log.py::test_the_invite_token_is_redacted_in_the_http_line`
(ASGI-Wrapper, `GET /ui/invite/Qm9z…` → `path == "/ui/invite/<redacted>"`) ·
`phase2_mcp/tests/test_logging.py` — ein weiterer Fall in der parametrisierten Secret-Tabelle.

**Fertig, wenn:** Tests grün; Probe-Zelle `b9`: `grep -c Qm9z serve.log` der Wegwerf-Instanz = 0 nach
einem Einladungsaufruf.

### 15.8 B11 — ein Move ist ganz oder gar nicht (Opus)

**Anker:** `store.py:1372` `files.move_asset_dir(...)` **vor** `:1377` `_write_item_file`.

**Änderung.**
```python
src_assets = files.asset_dir(self._data_root, current.space, current.id)
dst_assets = files.asset_dir(self._data_root, target_space, current.id)
files.move_asset_dir(src_assets, dst_assets)
try:
    self._write_item_file(new_item, old_path=old_path, op="move", actor=actor)
except BaseException:
    files.move_asset_dir(dst_assets, src_assets)   # Rollback — kein halber Move (B11)
    raise
```

**Tests.** `test_store.py::test_move_rolls_the_asset_directory_back_when_the_item_write_fails`
(Monkeypatch `files.atomic_write` → `OSError`; Assets wieder an der Quelle, Index unverändert, keine
neue Commit-Zahl).

**Fertig, wenn:** Test grün; der bestehende `test_move_carries_the_asset_directory_and_still_produces_one_commit` bleibt grün.

### 15.9 B16 — Unarchive (Opus; UI-Teil Sonnet möglich)

**Anker:** `store.py:1165` (`update`: „ist archiviert — update verboten"), `:1278` `archive()`,
`:460` `_write_item_file` (Zielpfad nach Status), `:73` `_DEFAULT_STATUS` · `tools.py:769`
`update_item` (Beschreibung `:753ff.`, `_status_hint()` `:155`) · `api.py:485` `_meta`, `:1357`
`_items_patch` · `editor.js:373` `populateStatusSelect`, `:865–870` (`readonly` → `showReadonlyItem`
sonst `showEditableItem`), `:770ff.` `showReadonlyItem` (Badge „Nur lesen — fremder Space").

**Änderung.**
- `models.py`: `DEFAULT_STATUS = {"task": "open", "note": "active"}`; `store.py` behält
  `_DEFAULT_STATUS = DEFAULT_STATUS` als Alias.
- `store.update()`: statt des Riegels —
  ```python
  unarchive = current.status == "archived"
  if unarchive and (set(changes) != {"status"} or changes["status"] == "archived"):
      raise ValidationError(f"Item {item_id} ist archiviert — erst wiederherstellen "
                            "(nur status=<offener Status> ist erlaubt), dann bearbeiten")
  ```
  danach der bestehende Weg; bei `unarchive` zusätzlich `folder=""` im `replace(...)` und
  `op="unarchive"` an `_write_item_file` (der Zielpfad ist dann `files.item_path(..., folder="")`,
  `move_file` holt die Datei aus `_archive/`).
- `tools.py` `update_item`-Beschreibung: „Ein archiviertes Item stellt `status=<offener Status>`
  wieder her — es landet an der Space-Wurzel; andere Felder erst danach." (ein Satz, wörtlich auch in
  `_status_hint()` nicht nötig).
- `api.py` `_meta`: `"default_status": dict(DEFAULT_STATUS)`.
- `editor.js`: `populateStatusSelect()` lässt `archived` weg; im Öffnen-Pfad vor dem
  `readonly`-Zweig: `if (item.status === "archived" && !item.readonly) { showArchivedItem(item);
  return; }`. `showArchivedItem(item)` = `showReadonlyItem(item)` mit Badge „Archiviert — zum
  Bearbeiten wiederherstellen" und Knopf `#detail-unarchive` („Wiederherstellen", `.btn`), Klick →
  `api("/items/" + item.id, {method: "PATCH", body: JSON.stringify({version: item.version, status:
  state.meta.default_status[item.type]})})` → Toast „Wiederhergestellt", Item neu laden (öffnet im
  Editor); 409 → Konflikt-Toast wie beim Speichern. Kein `app.html`-Markup nötig (die Lesesicht baut
  ihre Elemente in JS); `app.css` nur, falls `.btn` im `roMetaEl` Abstand braucht.

**Tests.** `test_store.py::test_unarchive_moves_the_file_back_to_the_space_root_with_one_commit`
(`status` aus `archived` → `open`; Pfad an der Wurzel, `version+1`, Commit-Betreff `unarchive <id>
[<space>]`, Index == `rebuild_index`) · `test_store.py::test_update_of_other_fields_while_archived_is_rejected`
· `test_store.py::test_unarchive_to_archived_is_rejected` · `test_store.py::test_unarchive_then_update_works`
· `test_tools.py::test_update_item_restores_an_archived_item` (`get_item_meta`: `status open`, `folder ""`)
· `test_api.py::test_patch_status_restores_an_archived_item` ·
`phase5_ui/tests/test_meta.py::test_meta_carries_default_status` · Probe-Zelle `unarchive`
(Playwright: eigenes archiviertes Item → Knopf sichtbar → Klick → Editor offen, Status `open`; die
Status-Auswahl enthält kein `archived`).

**Fertig, wenn:** Tests und Probe-Zelle grün; `mcp_smoke.py` unverändert 17/17.

### 15.10 B12 + B10 — Suche aus dem Index, Writes neben dem Loop (Opus)

**Anker:** `store.py:1016` `search` (`:1032` `all_rows` unter Lock, danach `_row_to_item` je Zeile
**ohne** Lock), `:246` `_summary`, `:221` `_snippet`, `:369` `_reconcile_and_get_row` · `index.py:38`
`INDEX_SCHEMA_VERSION = 4`, `:40` `_SCHEMA`, `:152` `upsert_item`, `:228` `row_from_file` ·
`tools.py:89` `_STORE_FETCH_LIMIT`, `:461` `list_spaces` zählt `human` über `search` · `api.py:241`
`_STORE_FETCH_LIMIT`, `:1004` `_overview` (Muster `asyncio.to_thread`), `:1272` `_items_post`, `:1357`
`_items_patch`, `:1513` `_items_delete`, `:1587` `_items_append`, `:1617` `_items_archive`, `:1658`
`_assets_post`, `:1727` `_assets_delete`, `:759` `_spaces_rename_folder`, `:689` `_spaces_rename_space`.

**Änderung.**
- `index.py`: Schema **5** — Spalten `snippet TEXT NOT NULL DEFAULT ''`, `updated_by TEXT NOT NULL
  DEFAULT ''`, `created_by TEXT NOT NULL DEFAULT ''` in `_SCHEMA`, `_upsert_no_commit` und
  `row_from_file` (`snippet` = `_snippet(body)`, aus `store.py` nach `models.py` verschoben als
  `snippet_of(body, length=160)`; die Actor-Felder wie in `_item_from_text`). `connect()` verwirft den
  alten Index beim ersten Start (vorhandener Mechanismus, kein Code).
- `store.search()` (Signatur unverändert, `in_body` bleibt):
  1. `with self._lock:` um **alles**;
  2. `rows = index.all_rows(conn)`; **Frischeprüfung:** je Zeile `stat()` des Pfads — fehlt die
     Datei → Zeile überspringen (`logger.warning`); weichen `mtime`/`size` ab →
     `self._reconcile_and_get_row(row["id"], repair_drift=False)` (liest **diese** Datei, kein Write)
     und die frische Zeile verwenden;
  3. Filter über Indexspalten (`space`, `folder`, `type`, `status`, `tags_json`, `due`; `query` auf
     `title` + Tags); bei `in_body=True` zusätzlich Body-Lesen **nur** für die Kandidaten;
  4. Sortierung wie heute über Indexspalten (`status`, `due`, `updated` — ISO-Z-Strings sortieren
     chronologisch);
  5. `total`, Seite, `ItemSummary` **aus der Zeile** (`_summary_from_row(row)` — alle Felder
     inklusive `snippet`, `updated_by`, `created_by`).
  `_row_to_item` wird in `search()` nicht mehr aufgerufen.
- `tools.py`/`api.py`: `_STORE_FETCH_LIMIT = 50_000` (Kommentar datiert; der Rückfall in
  `_overview` bleibt).
- `api.py`: jeder Store-**Schreib**aufruf in den oben genannten Routen läuft über
  `await asyncio.to_thread(store.<methode>, …)` (Kwargs werden durchgereicht; die Rechteprüfung
  davor bleibt synchron). `_spaces_delete` bleibt (Orchestrierung, eigener Schritt wäre nötig).

**Tests.** `test_index.py::test_schema_5_rows_carry_snippet_and_actors` (+ `INDEX_SCHEMA_VERSION == 5`,
alter Index → `rebuilt=True`) · `test_store.py::test_search_reads_no_item_file_when_in_body_is_false`
(Monkeypatch `Path.read_text`/`read_bytes` zählt 0) ·
`test_store.py::test_search_sees_a_hand_edit_without_a_prior_get` (Titel von Hand geändert →
`search(query=neu)` findet, `version` unverändert, kein Commit) ·
`test_store.py::test_search_skips_a_row_whose_file_vanished` ·
`test_store.py::test_concurrent_search_and_title_updates_never_raise` (3 Such-Threads × 100 gegen
100 Titel-Updates — der B10-Wächter) · `test_store.py::test_search_in_body_still_reads_only_candidates`
· `test_tools.py`/`test_api.py`: bestehende Suchtests bleiben grün (Snippets kommen jetzt aus dem
Index — gleicher Text).

**Messung (Probe `perf`, Wegwerf, 1500 Items mit 400-Byte-Bodies wie im Review):** `search(limit=20)`
und `search(query=…)` je Median aus 5 Aufrufen — Review-Werte 916 ms / 872 ms, **Ziel ≤ 100 ms**;
`list_spaces()` ≤ 20 ms; `/health` während 10 paralleler `PATCH`-Aufrufe ≤ 200 ms (Logik aus
`p105_b4_eventloop_probe.py`). Zahlen in `probes/p105_b15_ultra.json`, Wächter
`tests/test_b15_ultra_probe.py` liest sie.

**Fertig, wenn:** Tests grün, Messung unter den Zielen, Kommentar an `INDEX_SCHEMA_VERSION` datiert,
`phase1_storage/CLAUDE.md` nennt Schema 5 unter Öffnung 16.

### 15.11 B21 — `auth_requests` begrenzen (Opus; Freigabe P10.5-AD)

**Anker:** `authserver/store.py:328` `create_auth_request` · `authserver/flows.py:120` (Aufruf, nach
Client- und Redirect-Prüfung) · `authserver/config.py:41` `request_ttl_s` (V223: Default lesen).

**Schritt 1 — messen (Wegwerf):** 300 × `GET /oauth/authorize` mit registriertem Client (Muster
`p105_b6_dcr_probe.py`), danach `SELECT COUNT(*) FROM auth_requests` über das `sqlite3`-Modul
(Python, nicht das Binary) auf der tmp-DB. Ergebnis in den Session-Block. Wächst die Tabelle nicht,
ist B21 „Wissen" — Rückgabe an den Nikinger (§2.5).

**Schritt 2 — bauen:** in `create_auth_request()` unter `self._lock`, in **einer** Transaktion:
`DELETE FROM auth_requests WHERE expires_at < :now`; Zählung offener Anfragen des Clients (`consumed_at
IS NULL AND expires_at >= :now`); ab `MAX_PENDING_AUTH_REQUESTS_PER_CLIENT = 20` die ältesten (nach
`created_at`) löschen, bis 19 bleiben; dann `INSERT`. `logger.warning` je Räumung (eine Zeile mit Zahl).
Konstante im Modulkopf, datiert.

**Tests.** `phase4_auth/tests/test_authserver_store.py::test_pending_auth_requests_per_client_are_capped_fifo`
(25 anlegen → 20 offen, die fünf ältesten fehlen) ·
`::test_expired_auth_requests_are_purged_opportunistically` (Uhr vorstellen) ·
`phase4_auth/tests/test_flows.py::test_a_legitimate_authorize_still_works_after_a_burst`.

**Fertig, wenn:** Tests grün; Probe-Zelle `b21` (300 GETs → ≤ 20 Zeilen je Client; ein regulärer
Consent danach gelingt); `phase4_auth/CLAUDE.md` Befund-Tabelle: neue Zeile **S11** (B21) mit Datum.

### 15.12 B17 + B18 + B19 + Update-Log (Sonnet)

**Anker:** `phase2_mcp/mcpserver/__init__.py:1` · `app.py:169` `/health` · `app.html:25` Badge ·
`health_gate.sh:101–117` (Gate 5) · `README.md:145` · `history.py:15` `_GITIGNORE_CONTENT`, `:38`
`ensure_repo` · `files.py:412` (`mkstemp(prefix=f".{path.name}.", suffix=".tmp")`).

**Änderung.**
- **B17:** `__version__ = "4.0.0"` (Kommentar: Produktversion = Badge, Wächter). Neuer Test
  `phase10_5_finishing/tests/test_version_single_source.py::test_health_version_equals_the_badge`
  (Regex `rail__version">v([\d.]+)<` in `app.html` == `mcpserver.__version__`). `health_gate.sh`:
  **Gate 5b** — `/health` liefert `"version":"<EXPECTED_VERSION ohne v>"` (`python3 -c`, kein `jq`;
  V224 entfällt damit). Plan P10.5 §2.5 D2: datierter Nachtrag „Badge **und** `__version__`".
- **B18:** `README.md:145` → „Fährt die **elf** Tools einmal komplett durch (17 Prüfungen; …)";
  `updated:`-Faden per `scripts/prepend_updated_chain.sh`.
- **B19:** `_GITIGNORE_CONTENT = ".index.sqlite3*\n.write.lock\n.*.tmp\n"`; `ensure_repo()` ergänzt
  die Zeile `.*.tmp`, wenn eine bestehende `.gitignore` sie nicht trägt (idempotent; auf der VM greift
  das beim nächsten Start, der nächste Write committet die `.gitignore`).
- **Update-Log** (Block `## 2026-10-26`, je Aussage **eine** `- `-Zeile, Deutsch): „Behoben: Bild-IDs
  werden jetzt streng geprüft …" (falls nicht schon durch H4 dort) · „Behoben: Ein Ordner lässt sich
  auch in einen noch nicht vorhandenen Oberordner umbenennen; ein abgebrochenes Umbenennen blockiert
  den Start nicht mehr." · „Behoben: Eine fremde oder beschädigte Markdown-Datei im Space-Ordner hält
  die Suche nicht mehr auf — sie wird übersprungen und im Protokoll genannt." · „Behoben: Mitglieder
  eines persönlichen Space verwaltet nur noch dessen Eigentümer." · „Behoben: Zahlen als Titel oder
  Tags in von Hand bearbeiteten Dateien brechen Suche und Speichern nicht mehr." · „Neu: Archivierte
  Einträge lassen sich wiederherstellen — in der Oberfläche mit einem Klick, über die KI-Verbindung mit
  dem offenen Status." · „Die Suche liest jetzt aus dem Index statt aus jeder Datei — Listen und Suchen
  bleiben auch bei vielen Einträgen schnell." · „Sehr lange Titel werden abgelehnt statt mit einem
  Fehler zu scheitern; Dateinamen bleiben kurz."

**Tests.** der neue Versions-Wächter · `phase1_storage/tests/test_history.py::test_ensure_repo_adds_the_tmp_pattern_to_an_existing_gitignore`
· `::test_an_orphan_tmp_file_is_not_committed` (`.foo.md.ab12.tmp` anlegen, `commit()`, `git ls-files`
kennt sie nicht) · `phase5_ui/tests/test_deploy_scripts.py`: ein Test für Gate 5b (Stub-`/health`).

**Fertig, wenn:** Tests grün, `doc_health` 0, Update-Log-Parser (`webui/updates.py`) liest den Block
mit den neuen Zeilen (bestehende Tests).

### 15.13 Abschluss Block 15 (Sonnet)

1. Volle Suite grün (bereinigte Umgebung), `scripts/doc_health.py` 0, `phase5_ui/scripts/ui_budget.py`
   grün (alle Zeilen), `phase2_mcp/scripts/mcp_smoke.py --json` 17/17.
2. **Gegenlauf** nach §2.4 — Zahl der roten Tests = Zahl der neuen Tests; beides im Session-Block.
3. Probe `p105_b15_ultra_probe.py cells` an der Wegwerf-Instanz: alle Zellen grün (`b1 b2 b3 b4 b5 b6 b7
   b9 unarchive b21`), `perf` unter den Zielen; JSON im Repo (`probes/p105_b15_ultra.json`), Wächter
   `tests/test_b15_ultra_probe.py` grün.
4. **P1-Kriterium:** `git diff --stat <block-basis>..HEAD -- phase1_storage/storage` nennt nur die sechs
   Dateien aus P10.5-Z; Eintrag „Öffnung 16" in `phase1_storage/CLAUDE.md` auf ✅.
5. Register: BG-4 → `✅ 10-75–88 (B15)`; Phase-Heads (P1, P2, P4, P5) je eine datierte Modulzeile;
   Abnahmezeilen 75–88 ✅ mit Beleg; Session-Block ≤ 4 KiB; Rotation per Skript.
6. `docs/UPDATE_LOG.md` vollständig (15.12), Badge `v4.0.0` bleibt; Deploy D wartet auf Block 16 (C1).

## §5 Abnahme — neue Zeilen P10.5-75–88 (Zählregel Plan P10.5 §5; 89–92 im Film-Plan)

| # | Kriterium | Beleg |
|---|---|---|
| P10.5-75 | **Hotfix `v3.1.7` live:** `health_gate` 9/9 OK mit `--expected-version=v3.1.7`; Live-Probe des Nikingers: `get_item_asset(asset_id="../../../x")` → `invalid:`, ein echtes Asset lädt | Ausgabe im Session-Block, Deploy-Tabelle Zeile H |
| P10.5-76 | **B1/B15:** `get_asset`/`delete_asset` lehnen jede ID außerhalb `ast_<8 hex>` ab, bevor ein Pfad gebaut wird; Tool `invalid:`, Route 422; Bobs Dateien bleiben unberührt | Tests 15.1, Probe-Zelle `b1` |
| P10.5-77 | **B2/B22:** Rename in fehlenden Elternordner gelingt; ein vergifteter Marker verhindert den Start nie (CRITICAL im Log, Marker bleibt); Rename eines leeren Ordners ohne CRITICAL | Tests 15.2, Zelle `b2` |
| P10.5-78 | **B3/B20:** Neuaufbau überspringt unlesbare Dateien mit Pfad im Log, zählt `files_skipped`, läuft in einer Transaktion; CRLF-Items werden indiziert | Tests 15.3, Zelle `b3` |
| P10.5-79 | **B5/B8:** Nicht-String-Werte aus Hand-Edits brechen weder Suche noch Update; Nicht-String-Eingaben an REST/MCP ergeben 422/`invalid:`, **vor** jedem Write | Tests 15.4, Zelle `b5` |
| P10.5-80 | **B4:** Mitglieder eines fremden Home-Space kann ein Schreib-Gast weder hinzufügen noch entfernen (403, `manageable: false`); Team-Space unverändert | Tests 15.5, Zelle `b4` |
| P10.5-81 | **B6/B7/B13/B14:** `space="team/"` → `invalid:`/422 auf beiden Flächen; 300-Zeichen-Titel abgelehnt, 200 Umlaute ergeben einen Dateinamen ≤ 100 B; ID-Kollision wird aufgelöst; negativer Offset auf 0 geklemmt | Tests 15.6, Zellen `b6`, `b7` |
| P10.5-82 | **B9:** ein Einladungs-Token steht in keiner `ev="http"`-Zeile | Test 15.7, Zelle `b9` |
| P10.5-83 | **B11:** ein scheiternder Move lässt Assets und Item an der Quelle | Test 15.8 |
| P10.5-84 | **B16:** Unarchive über MCP, REST und UI; Item an der Space-Wurzel, `version+1`, Commit `unarchive`; `archived` nicht in der Status-Auswahl; andere Felder bleiben bis dahin gesperrt | Tests 15.9, Zelle `unarchive` |
| P10.5-85 | **B12/B10:** `search(limit=20)` bei 1500 Items ≤ 100 ms (vorher 916 ms), kein Datei-Read ohne `in_body`, Hand-Edits sofort sichtbar; Suche und Umbenennen parallel ohne Fehler; `/health` hinter einem Write-Burst ≤ 200 ms | Tests 15.10, Probe `perf` |
| P10.5-86 | **B21:** 300 Authorize-Aufrufe hinterlassen ≤ 20 offene `auth_requests` je Client, der reguläre Consent funktioniert | Tests 15.11, Zelle `b21` |
| P10.5-87 | **B17/B18/B19:** `/health`-Version = Badge (Wächter + Gate 5b), README nennt elf Tools, verwaiste tmp-Dateien werden nicht committet | Tests 15.12 |
| P10.5-88 | **Block 15 geschlossen:** volle Suite, `doc_health` 0, `ui_budget` grün, `mcp_smoke` 17/17, Gegenlauf rot in genau den neuen Tests, P1-Kriterium erfüllt, Register BG-4 ✅ | 15.13, Session-Block |

Summe im Head danach **92 Zeilen**; `tests/test_head_rules.py` prüft sie gegen Head und `ABNAHME_ARCHIVE.md`.

## §6 `[VERIFY]` — neu ab V220

| V | Frage | wird geklärt in |
|---|---|---|
| **V220** | Weist pydantic (lax, FastMCP-Tool-Argumente) `tags=[1, 2]` für `list[str]` ab, oder koerziert es? | 15.4 (Test) |
| **V221** | Setzen die API-Test-Fixtures (`full_app_items`, `app` in `phase7_spaces_admin/tests`) das `is_home_space`-Prädikat? Sonst ist dort jeder Space „Team" und der B4-Test prüft nichts | 15.5 |
| **V222** | ✅ vorab (2026-10-30): Starlette 1.9.0 `FileResponse` beherrscht `Range`/`Accept-Ranges` (`starlette/responses.py:324, 367`) — Block 16 | — |
| **V223** | `DEFAULT_REQUEST_TTL_S` in `authserver/config.py` und das Intervall des Purge-Timers (`sharefyx-purge.timer`) | 15.11 Schritt 1 |
| **V224** | entfällt — Gate 5b nutzt `python3 -c`, kein `jq` | — |
| **V225** | Playwright-Version in `~/.claude-code-tools/e2e-venv` (`record_video_size`, `page.clock`) | Block 16, 16.1 |
| **V226** | `ffmpeg` mit `libx264` auf der VM (`ffmpeg -encoders \| grep 264`) | Block 16, 16.0 |
| **V227** | Node ≥ 18 auf der VM — nur für den Remotion-Rückfall | Block 16, nur bei Rückfall |
| **V228** | Autoplay-Regeln: Chromium (stumm + `playsinline`) und Safari für das In-App-Overlay | Block 16, 16.4 |
| **V229** | WAAPI-`currentTime`-Takt und `<video>`-Seek je Frame sind in headless Chromium deterministisch (zwei Renders, identische Frame-Hashes) | Block 16, 16.3 |
| **V230** | Live `SELECT COUNT(*) FROM auth_requests` vor dem Fix — **Nikinger**, nur lesend; das `sqlite3`-Binary fehlt laut Review auf der VM möglicherweise → Python-Einzeiler | 15.11 |
| **V231** | FastMCP-Stand bei der Deploy-D-Vorbereitung (Sicherheitseinträge seit 4.1.4?) · Remotion-5-Lizenz nur bei Rückfall | §7, Block 16 |
| **V232** | Lädt `load_ui_settings()` neue `SPACE_UI_*`-Variablen über denselben Weg wie `SPACE_UI_LEGACY_ORIGIN` (Unit `sharefyx-mcp.service:19`)? Für `media_dir` in Block 16 | Block 16, 16.4 |

## §7 Deploy D — Änderungen gegenüber Plan P10.5 §2.5

- **D2** nennt zwei Versionsstellen: Badge `app.html` **und** `mcpserver/__init__.py` (P10.5-AF);
  der Update-Log-Block `## 2026-10-26` wird am Deploy-Tag umdatiert (bestehende Regel) und trägt die
  Zeilen aus 15.12 und 16.5.
- **Vor D4 (Nikinger):** Medienverzeichnis und Unit-Umgebung aus dem Film-Plan (§3 dort); OS-Truststore
  (P10.5-AG, `apt`).
- **D5:** `health_gate.sh --expected-version=v4.0.0 --require-todays-update-log --expected-sha=<sha>`
  mit Gate 5b.
- **D6 Live-Prüfungen (zusätzlich zu Plan P10.5 §Deploy D):** B1-Probe erneut (wie H3) · ein
  archiviertes eigenes Item wiederherstellen · `/health` zeigt `4.0.0` · Film-Overlay einmal (Film-Plan
  P10.5-92).

## §8 Nachlauf

- **Memory (VM):** Claude Code auf der VM zieht seine Memory-Dateien nach (Phasenstatus: Block 15
  ✅/🔄, Hotfix `v3.1.7`, Lock P10.5-Y Ausführer Claude Code, Lock P10.5-AC Index-first). Die
  Planungssession lief in einem Cloud-Container ohne Memory-Zugriff.
- **Closeout Z** bleibt wie im Plan P10.5 (Bedingung P10.5-27/28). Das Register bleibt die Arbeitsliste
  (BG-4, UI-11); kein zweites Register (P10-B).
- **ROADMAP:** die P10.6-Zeile ist mit der Planungssession datiert in Block 16 aufgelöst; die P10.5-Zeile
  wird mit Deploy D nachgezogen, nicht vorher.
