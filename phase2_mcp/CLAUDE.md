---
status: live
purpose: Phase-Head MCP-Server — Scope, harte Regeln, gelockte Entscheidungen, Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase2_mcp/ — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase2_mcp_plan.md          # voller Plan, Entscheidungen P2-A–P2-N, Steps 0–7
  - ../docs/concepts/PHASE1_CLOSEOUT_HANDOVER.md # Herkunft der Entscheidungen D1–D6
  - SESSIONS_ARCHIVE.md                          # ältere Session-Blöcke, newest-first
updated: 2026-08-13 (Nikinger-Feedback: update_item/append_to_item/patch_item-Beschreibungen präzisiert, kein Verhaltens-/Testzahländerung)
---
# CLAUDE.md — Phase 2: MCP-Server (`phase2_mcp/`)

> **Claude kann lesen und schreiben — lokal, ohne Tunnel.** Ein dünner Adapter über dem in P1
> bewiesenen Storage-Kern: Transport (Streamable HTTP), Identität (Token → Space), Autorisierung
> (eigener Space schreibbar, fremde read-only).
> **Quelle der Wahrheit ist der Code, nicht dieses Dokument.**
> Vollständiges Design + alle 14 gelockten Entscheidungen (P2-A–P2-N) + Steps 0–7:
> `../docs/concepts/phase2_mcp_plan.md`.

## Mission (zuerst lesen)

Der eigentliche Härtetest der Phase ist nicht MCP, sondern **Rule 4**: ein Codepfad, über den
ein fremder Space beschrieben werden kann, existiert nach dieser Phase nicht — auch nicht
versehentlich, auch nicht über `get()`. Zwei gleichzeitige Requests mit zwei verschiedenen
Tokens müssen zwei verschiedene Spaces sehen; wenn dieser Test fällt, ist es ein
Cross-Space-Leak, kein Testproblem.

## Bauprinzip (Projekt-Kernprinzip)

„Der Server ist dumm." **Phase 2 enthält KEINE AI.** Die Tools reichen Store-Ergebnisse durch,
formatieren sie token-sparsam und entscheiden über Rechte. Mehr nicht. Wer hier ein LLM
einbauen will → **stop**.

## Scope

- **DRIN:** `fastmcp` über Streamable HTTP, Token→Space-Auflösung, sechs Tools
  (`list_spaces`, `search_items`, `get_item`, `create_item`, `update_item`, `append_to_item`),
  `<untrusted_content>`-Wrapping fremder Bodies + Snippets, Token-Budget-Disziplin im Listing,
  `/health`. **[2026-08-09 Korrektur, P6 Step 1]:** ein siebtes Tool ist dazugekommen —
  `patch_item` (P6-E, `storage/patch.py`) — siehe Modul-Status unten und
  `phase6_shares/CLAUDE.md`. Die P2-eigene Entscheidungsliste K unten bleibt als historischer
  Beschluss stehen, ist aber überholt (Korrekturnotiz dort).
- **DRAUSSEN:** Löschen (`status: archived` reicht), MCP Resources, MCP Prompts, OAuth,
  öffentliche Erreichbarkeit/Tunnel (P3), SQL-Filterung in `Store.search()` (D6, zurückgestellt).

## Harte Regeln (nicht verhandelbar)

- Alle Hard Rules aus Root-`CLAUDE.md` gelten unverändert — insbesondere: kein Secret in einer
  Datei (Tokens nur als sha256-Hash im Keyring, Service `nikinger-space`), kein Last-Write-Wins,
  kein offener Port am Router, Logging → stderr, stdout nur maschinenlesbares JSON.
- **Rule 4 ist architektonisch, nicht per `if`.** `create_item`/`update_item`/`append_to_item`
  haben keinen `space`-Parameter; der Ziel-Space ist immer der des Principals (P2-G).
  **[2026-08-12 Korrektur, P6 Step 5]:** für `create_item` nicht mehr wörtlich wahr —
  root-`CLAUDE.md`s Hard Rule 4 wurde bereits am 2026-08-09 (P6-U) neu gefasst: der Ziel-Space
  ist weiterhin **per Default** der Principal, aber `create_item(space=...)` erlaubt jetzt
  einen anderen, wenn dessen `.share.yml` dort `write:` gewährt — die Ausnahme ist Daten auf
  der Platte, kein `if` im Code, dieselbe architektonische Eigenschaft, nur nicht mehr
  parameterlos. `update_item`/`append_to_item` bleiben ohne `space`-Parameter (ein bestehendes
  Item hat seinen Space bereits, siehe `acl_of()`). Details: `phase6_shares/CLAUDE.md`
  Step-5-Session-Block.
- **Auth fail-closed.** Kein/unbekanntes Token → HTTP 401 ohne Detail, nie ein Tool-Fehler, nie
  unterscheidbar von „falsches Token" (P2-N).
- **`stateless_http=True` ab Tag 1** — Sicherheitsbedingung, keine Skalierungsoption (P2-B, §8
  Risiko 1).
- **Token nie im Log.** Uvicorn-Access-Log aus, Scrubbing-Filter auf jedem verbleibenden Logger.
- **Rotationsregel ab Tag 1.** Dieser Head trägt **genau einen** Session-Block. Beim Anlegen
  eines neuen wandert der bisherige **verbatim** nach `SESSIONS_ARCHIVE.md`, newest-first —
  Durchführung über `scripts/rotate_session_block.sh phase2_mcp`, nie von Hand.
- **Commit ⇒ Note-Update, im selben Commit** (Hard Rule 8): Modul-Tabelle unten + Session-Block.

## Die 14 Entscheidungen (P2-A – P2-N) — Kurzform (Details: Plan §0.4)

Bibliothek `fastmcp>=3.4,<3.5` (A) · Protokoll 2025-11-25, `stateless_http=True` (B) · Starlette-
Wurzel mit `Mount("/mcp")` (C) · Token im Pfad, Auflösung einmal pro Request (D) · Keyring
speichert nur Hashes (E) · `SpaceResolver`/`Permissions` getrennte Seams, beliebig viele Spaces
(F) · Schreib-Tools ohne `space`-Parameter (G) · `<untrusted_content>` mit Escaping (H) ·
kompaktes JSON / Dateitext als Ergebnisformate (I) · Token-Budget `limit=20`/`max=100` (J) ·
Archivieren nur über `update_item(status="archived")`, kein siebtes Tool (K) · drei einmalige
P1-Contract-Erweiterungen (L, Step 2) · OAuth bleibt hinter P3, Seam wird gebaut (M) ·
Fehlerabbildung mit handlungsfähigem Text (N).

**[2026-08-09 Korrektur, P6 Step 1]:** K ist überholt — `patch_item` ist ein siebtes Tool
(P6-E/F/G, `phase6_shares_plan.md`). Der Teil von K, der Archivieren betrifft
(„nur über `update_item(status=archived)`") bleibt unverändert richtig; nur der Nebensatz
„kein siebtes Tool" ist mit P6 nicht mehr haltbar. K bleibt hier historisch stehen (P2s
Beschlusslage war zum Zeitpunkt richtig), die Korrektur ist die Ersetzung, keine stille
Streichung.

## Modul-Status

| # | Modul | Step | Status | Tests |
|---|---|---|---|---|
| 1 | Haushalt, Verifikationsdurchlauf, Rotationsregel operationalisiert | 0 | ✅ | 0 (kein Feature-Code) |
| 2 | Paketgerüst `phase2_mcp/`, `mcpserver/config.py` | 1 | ✅ | 3 |
| 3 | P1-Contract-Erweiterungen (`space_of`, `repair_drift`, Statusvalidierung) | 2 | ✅ | 8 (in `phase1_storage/tests/`) |
| 4 | `credentials.py`, `scripts/issue_token.py` | 3 | ✅ (echter Keyring-Roundtrip vom Nikinger bestätigt) | 6 |
| 5 | `auth.py`, `permissions.py`, `context.py`, `asgi.py`, `logging_setup.py` | 4 | ✅ | 14 |
| 6 | `server.py`, `app.py`, `scripts/serve.py` | 5 | ✅ | 8 (`test_app.py`) |
| 7 | `tools.py` (die sechs Tools) | 6 | ✅ | 23 (`test_tools.py`) |
| 8 | `scripts/mcp_smoke.py`, Runbook, Größenmessung | 7 | ✅ **live-verifiziert** | 3 (`test_mcp_smoke.py`) |
| 9 | Siebtes Tool `patch_item` (P6-E/F/G) + `mcpserver/receipts.py` (neu, Quittungen statt Volltext, P6-H) + `return_body` an allen vier Schreib-Tools + `update_item` lehnt `visibility`/`share_read`/`share_write` ab (P6-M) | P6 Step 1 | ✅ | +7 (`test_tools.py` 23→30), Kollateralkorrekturen in `test_app.py`/`test_request_log.py`/`mcp_smoke.py` (keine neuen Tests, nur Assertions auf JSON statt Frontmatter-Text umgestellt) |
| 10 | Client-Surface-Logging (V42): `ua`-Feld auf der `ev="http"`-Zeile (`AccessLogASGI`), gekürzt auf 120 Zeichen, läuft durch `TokenScrubbingFilter` wie jedes andere Feld. Bewusst **nicht** auf `ev="tool"` — `context.py` ist nicht auf P6 Step 2s Berührungsliste | P6 Step 2 | ✅ **gebaut, V42 geschlossen (2026-08-12, `phase6_shares/CLAUDE.md` Step-2/-3-Session-Block)** — zwei Tage echtes journald ausgewertet: `ua` wird von echten MCP-Clients zuverlässig gesetzt, unterscheidet aber NICHT zwischen Claude-Oberflächen (278/278 echte `/mcp`-Aufrufe trugen `"Claude-User"`, egal ob Claude Code oder claude.ai) — negativer, aber definitiver Befund | +3 (`test_request_log.py` 11→13, `test_logging.py` 8→9) |
| 11 | Rechtepolitik (P6 Step 5): `permissions.py` (`Surface`, `SharePolicy` ersetzt `OwnSpaceWritable`, `can_read_item`/`can_write_item` beide surface-scharf inkl. `visibility` — Advisor-Fund am `can_write_item`, siehe Nachtrag im Phase-Head), `tools.py` (alle sieben Tools auf `acl_of()`+`can_read_item`/`can_write_item`, `search_items`/`list_spaces` item-weise gefiltert, `create_item(space=,folder=)`, `update_item(folder=)` mit Fail-Closed-Riegel gegen Nicht-Eigentümer-Verschiebung — Nikinger-Entscheidung, kein Plan-Text), `app.py` (Verdrahtung über `store.acl_reader`) | P6 Step 5 | ✅ **gebaut** — Details, alle zwölf Pflichttests, die Fail-Closed-Ergänzung und der `can_write_item`-Fix: `phase6_shares/CLAUDE.md` Step-5-Session-Block | +10 (`test_tools.py` 30→40), `test_permissions.py` vollständig neu (3→12 Tests, `OwnSpaceWritable`-Klasse entfernt), Kollateralkorrekturen in `test_app.py`/`mcp_smoke.py` (keine neuen Tests, Assertions auf die neue Fail-Closed-Sichtbarkeit umgestellt) |

**Zeile 7, Step 6 abgeschlossen:** `search_items`, `get_item`, `create_item`, `update_item`,
`append_to_item` lösen ihre seit Step 5 bestehenden `NotImplementedError`-Platzhalter ein
(§3.2/§3.4/§3.5/§3.6) — `list_spaces` war seit Step 5 bereits fertig. Zeile 6 (`test_app.py`)
wuchs um einen sechsten Test (`test_all_six_tools_are_callable_over_http`), der Step 6s eigenes
Done-when „alle sechs Tools über den ASGI-Testclient aufrufbar" gegen den echten Stack aus
Step 5 beweist — `test_tools.py` allein kann das nicht, weil dort der Guard gemockt ist (siehe
SESSIONS_ARCHIVE.md).

**Zeile 8, Step 7 abgeschlossen:** `mcp_smoke.py` (Gegenstück zu `space_cli.py` aus P1) plus
Runbook „Quick-Tunnel-Probe" oben und README-Abschnitt „MCP-Server smoke-testen". Grün gegen
ein temporäres `DATA_ROOT` verifiziert (Session-Block).

**Phase 2 ist ab 2026-07-26 live-verifiziert (§5.9):** der Nikinger hat die Quick-Tunnel-Probe
durchgeführt und zusätzlich eine vollständige Adapter-Abnahme über den echten Custom Connector
gefahren — 21 von 21 Prüfungen bestanden, gegen den echten `DATA_ROOT`, mit Rohantworten als
Beweis. Details, Prüfmatrix und Belege: `docs/concepts/P2_ADAPTER_ABNAHME_2026-07-26.md`.
`ROADMAP.md` steht jetzt auf ✅.

**Fund B1 aus der Abnahme, behoben (2026-07-26):** `list_spaces` zeigte den eigenen Space
nicht, solange er kein einziges Item hatte — `Store.list_spaces()` leitet Spaces ausschließlich
aus Indexzeilen ab (P1, keine separate Space-Registry), ein leerer Space hat keine. Eine
frische Claude-Sitzung sah damit ausschließlich Spaces, in die sie nicht schreiben darf, ohne
Möglichkeit, den eigenen Space-Namen vor dem ersten `create_item` zu erfahren. **Was geändert
wurde:** `mcpserver/tools.py :: list_spaces()` nimmt den eigenen Space jetzt immer in die
Antwort auf, notfalls mit `item_count: 0` — reine Tool-Schicht-Ergänzung, kein Store-Eingriff,
kein Contract-Bruch. Neuer Test `test_list_spaces_includes_empty_own_space`
(`test_tools.py`).

**Fund B2, behoben (2026-07-26, vom Nikinger auf dem echten `DATA_ROOT`):** Space-Namen
`nikinger`/`niklas` waren gemischt (Token gehörte zu `niklas`, das einzige Item aus dem
P1-Livetest lag unter `nikinger/`). Der Nikinger hat sich für Option 1 aus
`docs/concepts/P2_ADAPTER_ABNAHME_2026-07-26.md` §4 entschieden: `nikinger/` → `niklas/`
umbenannt (`git mv`, Frontmatter-`space:`-Feld im einzigen betroffenen Item vorher per `sed`
mitgezogen, damit Datei und Verzeichnis nie auseinanderlaufen), danach `reindex` gegen den
echten `DATA_ROOT`. Verifiziert: `space_cli list` zeigt jetzt ausschließlich `niklas: 3
Item(s)`, `nikinger` existiert nicht mehr. Kein Code-Eingriff — reine Datenoperation auf dem
echten `DATA_ROOT`, wie in §4 vorgesehen von Claude Code nicht selbst ausgeführt. Damit sind
beide Befunde aus der Abnahme geschlossen.

**Nebenbefund beim Nachtesten, nicht Teil der Abnahme:** `mcp_smoke.py`s eigener
`search_items`-Check war intermittierend flakig. Ursache: das Skript legt über 20 Items in
einer engen Schleife über die reale Systemuhr an (kein injizierter `now_fn` wie in den
Unit-Tests) — auf einer schnellen VM bekamen mehrere Items denselben `updated`-Zeitstempel,
und `Store.search()`s Sortierung entschied unter dieser Bindung über die Indexreihenfolge,
nicht die Anlegereihenfolge. Das drückte gelegentlich eines der drei `create_item`-Items aus
der Top-20-Seite. Kein Bug in `tools.py`/`store.py`. Behoben durch Aufteilen des Checks: die
Default-Listing-Prüfung misst nur noch Form + Größe (unabhängig von genau diesen drei IDs), eine
neue gezielte `search_items(query="Smoke-Item")`-Prüfung bestätigt die Fundbarkeit unabhängig
von Paginierung/Sortierreihenfolge. Acht Läufe in Folge grün, `pytest` viermal in Folge grün.

**Sicherheitsvorfall während der Abnahme, dokumentiert statt stillschweigend übergangen:** der
Nikinger teilte einen Screenshot des Connectors, der die volle URL inklusive Pfad-Token im
Klartext zeigte — und Claude Code wiederholte diesen Token dann selbst im Chat, um den Fund zu
erklären. Strukturell derselbe Vorfall wie in Step 3 (`SESSIONS_ARCHIVE.md`): ein Token außerhalb
des Keyrings, diesmal zusätzlich selbst verursacht statt nur weitergemeldet. **Sofort erkannt
und benannt, nicht stillschweigend weitergemacht.** Der Nikinger hat den Token für `niklas`
umgehend rotiert (`--revoke` + neu `--space`). Der Screenshot wurde **nicht** in dieses Repo
übernommen. Lehre, gleich wie in Step 3: ein Klartext-Token gehört nie in eine Antwort, auch
nicht beim Erklären eines Fundes — dieselbe Regel wie für Commits gilt auch für das eigene
Zitieren.

**[Korrektur 2026-07-26, Folgesession]:** Die Bilddatei lag bis zur Folgesession weiterhin
ungetrackt im Arbeitsverzeichnis (`docs/test-results/`) — nie versioniert, aber auch nicht
sofort entfernt. Nach Rücksprache mit dem Nikinger (Token bereits rotiert, Löschung freigegeben)
gelöscht. Lehre ergänzt: eine Doku-Aussage über den Repo-Zustand ist erst wahr, wenn `git
status` sie bestätigt, nicht wenn die Absicht dokumentiert wurde. Details: aktueller
Session-Block.

**[2026-07-28 Korrektur, P4 Step 6a]:** die Zeile unten stand auf 57 und war bereits vor dieser
Session falsch — `test_request_log.py` (P3 Step 2, `ev="oauth"`-Vorlauf) fehlte in der Aufzählung
komplett, und mehrere Einzelzahlen waren stumm gewachsen (`test_config.py` 3→6,
`test_credentials.py` 6→12, `test_logging.py` 1→2, `test_app.py` 8→10), ohne dass ein
P3-Abschluss-Commit diese Zeile nachzog. Reale Zahl per `pytest --collect-only -q` je Datei
neu gezählt, nicht aus der alten Summe hochgerechnet. Die historischen Modul-Status-Zeilen oben
(P2s eigene, längst abgeschlossene Steps) bleiben unangetastet — nur diese eine, unten mit der
Zeit driftende Summenzeile wird korrigiert. Gleiche Fund-Kategorie wie die root-`CLAUDE.md`-
Korrektur im selben Commit: „aktive Phase ist P4" ist kein Freibrief, Dateien anzufassen und
ihre Zähl-Zeile stehen zu lassen.

**[2026-07-28 Korrektur, P4 Step 6b]:** dieselbe Drift-Kategorie trat ein zweites Mal ein, einen
Step später — `test_logging.py` wuchs 2→8 (sechs neue parametrisierte `_SECRET_PATTERNS`-Fälle),
`test_request_log.py` 8→11 (drei neue `OAuthLogASGI`-Tests) und `test_asgi_bearer.py` 13→14 (Plan
§5 Step 6s dritte Done-when-Klausel — Diff aller sechs Tools unter Bearer vs. Pfad-Token, bisher
unbelegt), alle drei P4-Q-Berührungen, ohne dass ein Step-6a-Abschluss-Commit diese Zeile für die
eigenen zukünftigen Änderungen vorgemerkt hätte. Reale Zahl wieder per `pytest --collect-only -q`
je Datei neu gezählt.

**[2026-07-30 Korrektur, P4 Schnitt (Runbook-Schritt 8)]:** dieselbe Drift-Kategorie trat ein
drittes Mal ein, in die andere Richtung — `TokenPathASGI`/`AuthModeASGI` sind entfernt,
`test_asgi.py` (nur `TokenPathASGI`) gelöscht, `test_asgi_bearer.py` von 14 auf 10 gekürzt (die
Bearer-vs-Pfad-Token-Vergleichstests aus P4 Step 6a/6b haben keinen Vergleichspartner mehr).
Reale Zahl wieder per `pytest --collect-only -q` je Datei neu gezählt, nicht aus der alten Summe
heruntergerechnet.

**[2026-08-02 Korrektur, P5 Step 0 A]:** die Zeile unten trug noch 94 mit
`12 test_credentials.py + 4 test_auth.py` — der P5-Rückbau (`docs/concepts/
PHASE4_CLOSEOUT_HANDOVER.md` §4.5) hat `issue_token.py`/`export_space_map.py`/
`KeyringTokenResolver` entfernt und damit `test_credentials.py` auf 1 (nur `test_hash_token_
is_stable_hex64`) und `test_auth.py` auf 1 (nur `test_principal_repr_hides_token`) gekürzt.
Reale Zahl: **80**, nicht 94 — vierte Instanz derselben Drift-Kategorie, die diese Zeile schon
dreimal betraf (siehe die drei Korrekturen oben), diesmal aber im selben Commit korrigiert statt
erst später gefunden.

**[2026-08-03 Korrektur, P5 Step 4 Nachtrag]:** `test_app.py` 10→13 — `mcpserver/app.py ::
create_app()` mountet jetzt `webui.routes_auth`/`webui.account` (vorgezogen aus P5 Step 5, siehe
`phase5_ui/CLAUDE.md`s Session-Block 2026-08-03 für Anlass und Begründung). Dieselbe
Berührungsfläche wie P4-Q (`mcpserver/app.py` ist dort explizit erlaubt) — P5-B erlaubt es
ebenfalls. Kein Eigen-Auftrag dieser Phase, nur die Zähl-Zeile hier nachgezogen, dieselbe
Disziplin wie bei den P4-Korrekturen oben.

**[2026-08-05 Korrektur, P5 Step 5+6]:** dieselbe Drift-Kategorie wie oben, diesmal über zwei
P5-Schritte hinweg aufgelaufen — weder der Step-5-Nachtrag (`test_api_items_reachable_through_
create_app`, `test_app.py` 13→14) noch der Step-6-Commit (`test_ui_index_route_reachable_
through_create_app`, 14→15) hatten diese Zeile nachgezogen. Reale Zahl wieder per `pytest
--collect-only -q` je Datei neu gezählt, nicht aus der alten Summe hochgerechnet: **Gesamt: 85
Tests.**

**[2026-08-09 Korrektur, P6 Step 1]:** achte Instanz derselben Drift-Kategorie (siehe die sieben
Korrekturen oben) — `test_tools.py` wuchs 23→30 (siebtes Tool `patch_item` + Quittungsformat-Tests
+ `update_item`-Riegel-Test, Modul-Status Zeile 9), diesmal im selben Commit korrigiert statt
später gefunden. Reale Zahl wieder per `pytest --collect-only -q` je Datei neu gezählt: **Gesamt:
92 Tests.**

**[2026-08-09 Korrektur, P6 Step 2]:** neunte Instanz, im selben Commit korrigiert —
`test_request_log.py` 11→13 (`ua`-Feld: Kürzung, Abwesenheit) und `test_logging.py` 8→9 (`ua`
durch `TokenScrubbingFilter`), Modul-Status Zeile 10. Reale Zahl wieder per `pytest
--collect-only -q` je Datei neu gezählt: **Gesamt: 95 Tests.**

**[2026-08-09, P6 Step 3]:** `create_app()` (`mcpserver/app.py`) reicht `oauth.store` jetzt als
fünftes Argument an `api_routes(...)` durch — Update-Log-Banner braucht `AuthStore` (Schema 3,
`seen_update_id`), dieselbe Instanz wie `account_routes()`. **Dokumentierte Ein-Zeilen-
Abweichung** von P6 Step 3s Plan-Dateiliste (die nur `webui/api.py` nennt), kein Eigen-Auftrag
dieser Phase — keine neue Testdatei hier, kein Test in `phase2_mcp/tests/` betroffen, Testzahl
unverändert bei 95. Volle Herleitung: `phase6_shares/CLAUDE.md` Step-3-Session-Block.

**[2026-08-12 Korrektur, P6 Step 5]:** zehnte Instanz derselben Drift-Kategorie, im selben
Commit korrigiert — `test_tools.py` wuchs 30→39 (elf Pflichttests/Fail-Closed-Ergänzung zur
neuen Rechtepolitik, Modul-Status Zeile 11) und `test_permissions.py` 3→10 (Datei vollständig
neu geschrieben, `OwnSpaceWritable`-Klasse entfernt). Reale Zahl wieder per `pytest
--collect-only -q` je Datei neu gezählt: **Gesamt: 111 Tests.**

**[2026-08-12 Korrektur, P6 Step 5 Nachtrag]:** elfte Instanz — Advisor-Fund nach dem ersten
Step-5-Commit (`can_write_item` prüfte `visibility` nicht, siehe `phase6_shares/CLAUDE.md`s
Step-5-Session-Block), sofort im Folgecommit behoben. `test_permissions.py` 10→12,
`test_tools.py` 39→40. **Gesamt: 114 Tests.**

**Gesamt: 114 Tests** in `phase2_mcp/tests/` (6 `test_config.py` + 1 `test_credentials.py` + 1
`test_auth.py` + 12 `test_permissions.py` + 9 `test_logging.py` + 2 `test_context.py` + 15
`test_app.py` + 40 `test_tools.py` + 3 `test_mcp_smoke.py` + 13 `test_request_log.py` + 10
`test_asgi_bearer.py` [seit dem Schnitt: nur noch `BearerAuthASGI`, kein `TokenPathASGI`/
`AuthModeASGI` mehr, Details `phase4_auth/CLAUDE.md`] + 2 `test_serve.py` [neu, Schnitt:
`serve.py :: main()`s Verdrahtung bis `uvicorn.run()`, vorher ungetestet]). Acht weitere Tests
aus Step 2 liegen in
`phase1_storage/tests/` (siehe
Modul-Status Zeile 3 und `phase1_storage/CLAUDE.md`), werden dort mitgezählt, nicht hier.

**[2026-08-13 Korrektur, Nikinger-Feedback aus echtem Betrieb]:** eine arbeitende Claude-
Instanz meldete zwei vermeintliche Lücken — Status/`links` seien über `patch_item`/
`append_to_item` nicht änderbar, weil beide nur den Body anfassen. Beides war schon vorher
technisch möglich: `update_item(item_id, version, status=...)` bzw. `update_item(...,
links=[...])` ändert nur die übergebenen Felder (`tools.py :: update_item()` baut `changes`
ausschließlich aus Nicht-`None`-Argumenten, Zeile ~520) — `body` weglassen lässt den Body
unangetastet, kein Komplett-Rewrite. Der reale Fehler war eine **Beschreibungslücke**, kein
Codefehler: `update_item`s Tool-Description sagte nirgends, dass alle Felder unabhängig
optional sind, und `patch_item`/`append_to_item` verwiesen nicht auf `update_item` als
richtiges Werkzeug für Frontmatter-Felder. Behoben durch drei Beschreibungs-Ergänzungen in
`mcpserver/tools.py` (`update_item`, `append_to_item`, `patch_item`) — keine Signatur-, Schema-
oder Verhaltensänderung, daher keine neuen Tests nötig. **Gesamt weiterhin 114 Tests**,
`pytest phase2_mcp/tests/test_tools.py` 40/40 grün nach der Änderung.

**Advisor-Fund vor dem Commit, ein Punkt offen gehalten statt übernommen:** das Beispiel im
Report lautete wörtlich „status: open → archiviert" — geprüft statt angenommen: `models.py ::
STATUS_VALUES` (Zeile 95-98) ist rein englisch (`note`: `active`/`archived`; `task`: `open`/
`done`/`archived`). Ein `update_item(..., status="archiviert")` schlägt weiterhin mit
`ValidationError` fehl, das ist die vom Nikinger freigegebene Statusvalidierung aus P2 Step 2
(`STATUS_VALUES`/`valid_statuses()`, `phase1_storage/CLAUDE.md` „Geerbte Contracts"), keine
stille Aufweichung wert. Der reale Aufruf muss `status="archived"` (englisch) verwenden. Report
1 ist damit nur **teilweise** durch diesen Commit gelöst: das Werkzeug existiert und ist jetzt
auffindbar, aber die reportende Instanz griff möglicherweise zusätzlich zum falschen
Statuswort — kein Tool-Fehler, sondern ein Vokabular-Missverständnis, das die präzisierte
Beschreibung allein nicht behebt (die erlaubten Werte stehen dort nicht aufgezählt). Report 2
(`links`) hat keine Vokabular-Falle — `links` ist eine freie Liste ohne `*_VALUES`-Whitelist.

**[2026-08-14 Korrektur, P6-Vormerkung]:** `tools.py :: map_storage_error()`s Text für
`PatchError.found == 0` („lies das Item neu mit get_item und prüfe den exakten Text") war
irreführend bei einem Frontmatter-Zugriffsversuch — `patch_item` erreicht Frontmatter
kategorisch nie (operiert nur auf dem Body-String), ein erneutes Lesen hilft in diesem Fall nie.
Text nennt jetzt die tatsächliche Ursache und verweist auf `update_item`, keine
Frontmatter-Erkennungslogik ergänzt. Bestehender Test um zwei Assertions erweitert, kein neuer
Test. **Gesamt weiterhin 114 Tests.** Volle Herleitung: `phase6_shares/CLAUDE.md`s
Session-Block, Nachtrag „Werkzeug-Ergonomie".

## Geerbte Contracts

Aus P1 (`phase1_storage/CLAUDE.md`, `docs/concepts/phase1_storage_plan.md` §1/§2): Frontmatter-
Schema, `Item`/`SpaceInfo`/`ItemSummary`/`SearchResult`/`IndexStats`, `Store`-Signaturen
(`list_spaces`/`search`/`get`/`create`/`update`/`append`/`archive`/`rebuild_index`),
Fehlertypen inkl. `ConflictError.current`. **[2026-07-25, Step 2 abgeschlossen]** Drei
einmalige, vom Nikinger freigegebene Erweiterungen sind eingebracht (`space_of()`,
`get(..., repair_drift=)`, Statusvalidierung über `models.STATUS_VALUES`) — Details, Tests und
Begründung stehen in `phase1_storage/CLAUDE.md` unter „Geerbte Contracts" (dort, nicht doppelt
hier, da Code-nah). **Der Contract ist ab jetzt wieder zu.**

**D1, festgehalten statt stillschweigend übernommen:** `docs/concepts/PHASE1_CLOSEOUT_HANDOVER.md`
verlangte ausdrücklich Gegenprüfung von `ItemSummary` und `SpaceInfo.name`/`.item_count` (beides
Claude-Code-Eigenentscheidungen aus P1, im P1-Plan nicht spezifiziert), bevor P2 darauf aufbaut.
Der P2-Plan (`docs/concepts/phase2_mcp_plan.md` §0.2) übernimmt beide bereits als „gegeben" —
das zählt als Bestätigung durch die Browser-Planungssession mit dem Nikinger. Hier trotzdem
explizit vermerkt: **gilt als bestätigt, wenn der Nikinger nicht widerspricht** (siehe
Step-0-Session-Block unten).

**Warum nur Hashes im Keyring** (Plan §2.3, seit Step 3 in `mcpserver/credentials.py` real
umgesetzt): der Server muss ein Token nur *wiedererkennen*, nie *vorzeigen*. `issue()` gibt das
Token genau einmal zurück; ab dann existiert im Keyring nur noch
`{sha256(token): space}`. Wer diese Eigenschaft aufgibt, um „das Token nochmal anzeigen" zu
können, macht aus dem Keyring eine Passwortliste.

**Was der Pfad-Token nicht ist** (Plan §2.3): kein OAuth-Ersatz, kein Schutz gegen Cloudflare
(R4 — Cloudflare sieht bei P3 ohnehin Klartext), gültig bis P3+1. Siehe P2-Plan §0.3 für die
Begründung, warum OAuth trotzdem hinter P3 bleibt statt vorgezogen zu werden.

**`version` in fremden Spaces** (Plan §3.4): `get(..., repair_drift=)` existiert seit Step 2 im
Store; genutzt wird es ab Step 6 (`tools.py :: get_item`, §3.4). Dort ist `version` in fremden
Spaces informativ, nicht autoritativ — es gibt dort per Architektur keine Writes.

## Runbook „Quick-Tunnel-Probe" — historisch, ersetzt (P3 Step 6)

Quick Tunnel war der **einmalige P2-Nachweis** (live-verifiziert 2026-07-26, 21 Tool-Aufrufe über
eine echte Konversation, Protokoll: `docs/concepts/P2_ADAPTER_ABNAHME_2026-07-26.md`). Der
**Betriebsweg ist ab P3 Tailscale Funnel** — stabiler Hostname statt einer bei jedem
`cloudflared`-Neustart neu vergebenen Subdomain. Runbooks, Voraussetzungen und die
Inbetriebnahme-Anleitung: `phase3_edge/CLAUDE.md`.

**Cloudflare Named Tunnel** bleibt als dokumentierter Ausweichweg stehen, falls Funnel einmal
ausfällt (Plan §8 Risiko 1) — Voraussetzung dafür ist eine eigene, bei Cloudflare verwaltete
Domain (anders als der oben benutzte Quick Tunnel, der ohne Account/Domain auskam). Details bei
Bedarf neu recherchieren; hier bewusst nicht dupliziert, um keine zwei Wege nach außen in der
Doku parallel zu pflegen (P3 Step 6 baut zudem den `cloudflared`-Rückbau auf dieser VM in das
Runbook ein, siehe `phase3_edge/CLAUDE.md`).

---

## Session stopped — 2026-07-26 (Live-Verifizierung: Adapter-Abnahme, B1-Fix, Screenshot-Fund)

**Ergebnis:** Phase 2 ist **live-verifiziert** (§5.9). Der Nikinger hat die Quick-Tunnel-Probe
durchgeführt und zusätzlich eine vollständige Adapter-Abnahme über den echten Custom Connector
gefahren — 21 von 21 Prüfungen gegen den echten `DATA_ROOT`, mit Rohantworten als Beweis.
Vollständiges Protokoll: `docs/concepts/P2_ADAPTER_ABNAHME_2026-07-26.md`. `ROADMAP.md` steht
auf ✅. Details siehe Modul-Status-Tabelle oben (Zeile 8).

**Fund B1, behoben:** `list_spaces` zeigte den eigenen Space nicht, solange er kein Item hatte.
`mcpserver/tools.py :: list_spaces()` nimmt den eigenen Space jetzt immer in die Antwort auf,
notfalls mit `item_count: 0` — reine Tool-Schicht-Ergänzung, kein Store-Eingriff. Neuer Test
`test_list_spaces_includes_empty_own_space`.

**`mcp_smoke.py`-Flakiness behoben:** das Skript legt Items in einer engen Schleife über die
reale Systemuhr an; auf einer schnellen VM konnten mehrere Items denselben `updated`-Zeitstempel
bekommen, wodurch die stabile Sortierung gelegentlich eines der drei `create_item`-Items aus der
Top-20-Seite drückte. Kein Bug in `tools.py`/`store.py`. Der `search_items`-Check ist jetzt
zweigeteilt: eine Default-Listing-Prüfung (Form + Größe, unabhängig von genau diesen IDs) und
eine gezielte `search_items(query="Smoke-Item")`-Prüfung für die Fundbarkeit. Aktueller Lauf:
12/12 Checks grün (`python phase2_mcp/scripts/mcp_smoke.py --json`).

**Sicherheitsvorfall, zweiteilig:** (1) Während der Abnahme zeigte ein Screenshot des Connectors
die Verbindungs-URL inklusive Pfad-Token im Klartext, und der Token wurde beim Erklären des
Fundes zusätzlich im Chat wiederholt — strukturell derselbe Vorfall wie in Step 3
(`SESSIONS_ARCHIVE.md`). Sofort erkannt, der Nikinger hat den Token für `niklas` umgehend
rotiert (`--revoke` + neu `--space`). (2) Bei der Übernahme in diese Session stellte sich heraus,
dass genau dieser Screenshot trotz gegenteiliger Doku-Aussage weiterhin ungetrackt im
Arbeitsverzeichnis lag (`docs/test-results/2026_07_26_p2-mcp-test/`) — die Behauptung „bewusst
nicht ins Repo übernommen" war zum Zeitpunkt dieser Session schlicht falsch. Vor jeder Aktion
beim Nikinger nachgefragt (Datei ist sein Artefakt, Löschen ist destruktiv); er bestätigte, dass
der abgebildete Token bereits durch den Rotationsschritt zerstört ist, und gab die Löschung
frei. Datei + leeres Verzeichnis entfernt, `docs/concepts/P2_ADAPTER_ABNAHME_2026-07-26.md` §7
um eine datierte Korrekturnotiz ergänzt (die Aussage selbst wird nicht rückwirkend umgeschrieben
— das Dokument ist ein 📕-Snapshot). Lehre: eine Doku-Aussage über den Repo-Zustand ist erst
wahr, wenn `git status` sie bestätigt, nicht wenn die Absicht dokumentiert wurde.

**Fund B2, behoben (2026-07-26, vom Nikinger auf dem echten `DATA_ROOT`):** Space-Namen
`nikinger`/`niklas` waren gemischt. Der Nikinger hat Option 1 aus
`docs/concepts/P2_ADAPTER_ABNAHME_2026-07-26.md` §4 gewählt — professionellerer Name, `niklas`
bleibt: `nikinger/` → `niklas/` umbenannt, dabei das Frontmatter-`space:`-Feld des einzigen
betroffenen Items (`itm_7a6f9f7f`) per `sed` mitgezogen (sonst widerspräche Frontmatter dem
Verzeichnis), `git mv` statt Kopie (Historie bleibt erhalten), danach `space_cli reindex`.
Verifiziert direkt vom Nikinger: `space_cli list` → `niklas: 3 Item(s)`, kein `nikinger` mehr.
Reine Datenoperation auf dem echten `DATA_ROOT`, wie in §4 vorgesehen nicht von Claude Code
selbst ausgeführt — Claude Code lieferte nur die Befehlsfolge. Damit sind beide Befunde aus der
Abnahme geschlossen, keine offenen Findings mehr.

**Verifiziert:** `pytest -v` → **133/133 grün** (76 P1 + 57 P2, Aufschlüsselung je Testdatei
gegen die Modul-Status-Tabelle nachgezählt, exakt deckungsgleich). `mcp_smoke.py --json` → 12/12
Checks grün. `git status` nach der Bereinigung → `docs/test-results/` existiert nicht mehr.
B2-Fix vom Nikinger direkt am echten `DATA_ROOT` verifiziert (`space_cli list`/`search`-Ausgabe
oben).

**Nächster Schritt (konkret):** Keine offenen Code- oder Daten-Findings mehr in P2. Es fehlt
nur noch der **formale** Phasenabschluss — laut `docs/PROMPTS.md` ein eigener Prompt im
Browser-Webchat (analog Phase 1s Abschluss), inklusive Handover-Dokument für P3
(Tunnel/systemd/Ops). Das ist Sache des Nikingers, nicht etwas, das Claude Code aus einem
Code-Commit heraus erklären kann. Danach: neue Browser-Planungssession für Phase 3.
