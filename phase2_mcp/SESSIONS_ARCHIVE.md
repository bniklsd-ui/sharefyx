---
status: live
purpose: Archiv älterer Session-stopped-Blöcke aus phase2_mcp/CLAUDE.md, newest-first, verbatim
read-when: Audit vergangener Sessions dieser Phase; NICHT für normalen Session-Start
detail: L3
up: CLAUDE.md
updated: 2026-07-26 (Step 7 archiviert)
---
# Session-Archiv — Phase 2 MCP-Server

## Session stopped — 2026-07-26 (Step 7: Smoke-Test, Messung, Runbook)

**Ergebnis:** `phase2_mcp/scripts/mcp_smoke.py` — Gegenstück zu `space_cli.py` aus P1. Baut ein
**temporäres** `DATA_ROOT` (`tempfile.TemporaryDirectory`, nie das echte), zwei Fixture-Spaces
(`alpha`/`beta`), startet `create_app()` in-process über `httpx.ASGITransport` (kein echter
Port, kein Netz — dasselbe Muster wie `test_app.py`) und fährt alle acht Prüfpunkte aus dem
Plan durch: `list_spaces`, `create_item` ×3, `search_items`, `get_item` eigen/fremd, ein
`update_item`-Konflikt, `append_to_item`, `update_item(status=archived)`, ein `update_item` auf
einen fremden Space. `--json` für maschinenlesbare Ausgabe, sonst Textreport; Exit-Code `1` bei
jeder fehlgeschlagenen Prüfung. README bekam den Abschnitt „MCP-Server smoke-testen", der
Phase-Head diesen hier stehenden Runbook-Abschnitt „Quick-Tunnel-Probe" (oben, dauerhaft, nicht
nur im Session-Block — der Tunnel-Schritt selbst bleibt außerhalb des Repos).

**Kein echter Keyring, bewusst:** `mcp_smoke.py` importiert `keyring` nicht direkt — die beiden
Tokens entstehen über `credentials.generate_token()`/`hash_token()` (reine Funktionen) und
werden per injiziertem `load_map` in einen `KeyringTokenResolver` gereicht, exakt das Muster
aus den Unit-Tests. Ein Skript, das beliebig oft laufen soll, darf die reale Token→Space-Map
unter `nikinger-space` nicht anfassen. Empirisch geprüft (nicht nur behauptet): `load_space_map()`
gegen den echten Keyring zeigt nach mehreren `mcp_smoke.py`-Läufen weiterhin nur den einen
`nikinger`-Eintrag aus Step 3 — keine `alpha`/`beta`-Verschmutzung.

**Ein echter Fund beim ersten Lauf, kein Advisor-Vorgriff:** `list_spaces` schlug beim ersten
Durchlauf fehl (`Spaces=['beta']` statt beider). Ursache: `Store.list_spaces()` leitet Spaces
ausschließlich aus vorhandenen Items ab (P1, keine separate Space-Registry) — `alpha` hatte zum
Zeitpunkt des ersten `list_spaces`-Aufrufs (Plan-Reihenfolge: Prüfpunkt 1, vor jedem
`create_item`) schlicht noch kein Item und war deshalb unsichtbar. Kein Bug in `tools.py`, ein
Fixture-Fehler im Smoke-Skript: `alpha` bekommt jetzt denselben Seed-Eintrag wie `beta`, bevor
die Prüfungen beginnen.

**Automatisiert statt nur manuell bewiesen** (wie `space_cli.py` in P1 per Subprozess-Tests):
`test_mcp_smoke.py` neu, 3 Tests, ruft `mcp_smoke.py` als echten Subprozess auf (kein Import —
gleiche Begründung wie bei `space_cli.py`: Namenskollisionsgefahr über künftige Phasen hinweg,
realistischste Prüfung). Prüft `--json`-Exit-Code 0 und dass alle Checks grün sind (Anzahl
bewusst **nicht** hartkodiert — der Exit-Code trägt das Pass/Fail-Signal, ein `len(checks) ==
N` würde bei jeder künftigen zusätzlichen Prüfung unnötig brechen), den Text-Report per Regex,
und statisch (Quelltext-Grep), dass das Skript `keyring` nicht direkt importiert.

**Advisor-Review vor dem Commit, ein Fund korrigiert (blockierend), zwei kleinere mitgenommen:**
Die erste Fassung der Größenmessung maß `search_items` gegen nur 5 vorhandene Treffer (1058 B)
— das beantwortet nicht die Frage, für die Step 7s eigenes Done-when eine Größentabelle
verlangt: hält das Token-Budget bei einem **echten Default-Listing** (§5 Kriterium 5, 20 Items
< 12 KB)? `mcp_smoke.py` seedet jetzt 17 zusätzliche Füll-Items mit realistischer Body-Länge
(vor den drei `create_item`-Aufrufen, damit diese als jüngste Items sicher im ersten
20er-Fenster bleiben) — `search_items` misst jetzt tatsächlich eine volle 20-Item-Seite.
Kleinere Fixes im selben Aufwasch: der Subprozess-Test hartkodierte die Checkanzahl (`== 11`,
siehe oben) und der YAML-Feld-Extraktor `_extract_field` bekam einen Kommentar zur stillen
Reihenfolge-Abhängigkeit (Frontmatter kommt immer vor dem Body, deshalb gewinnt bei
`re.search` nie eine zufällig gleichlautende Body-Zeile).

**Größenmessung (Bytes je Antwort, Live-Lauf gegen ein temporäres `DATA_ROOT`):**

| Operation | Bytes |
|---|---|
| `list_spaces` | 98 |
| `create_item` #1 | 172 |
| `create_item` #2 | 172 |
| `create_item` #3 | 172 |
| `search_items` (Default-Listing, 20 von 22 Treffern) | 6403 |
| `get_item` (eigen) | 172 |
| `get_item` (fremd, gewrappt) | 242 |
| `update_item` (Konflikt) | 140 |
| `append_to_item` | 183 |
| `update_item` (archivieren) | 187 |
| `update_item` (fremder Space, `write_denied`) | 65 |

`search_items` bei 6403 B liegt klar unter dem §5-Budget (20 Items < 12 KB) — jetzt eine echte
Antwort auf die Kriteriumsfrage, nicht nur ein Bestwert-Artefakt. Ergänzt, nicht ersetzt durch
`test_tools.py::test_search_result_size_budget` (Step 6, 20/30-Item-Grenzfälle als
Pass/Fail-Assertion in der Testsuite statt als gemeldete Zahl im Session-Block).

**Verifiziert (live):** `pytest -v` → **132/132 grün** (76 P1 + 56 P2). `mcp_smoke.py` manuell
ausgeführt (Text und `--json`, nach dem Advisor-Fix erneut), alle elf Prüfungen grün,
temporäres Verzeichnis nach Lauf sauber entfernt (`ls /tmp/mcp_smoke_*` findet nichts mehr).

**Phase 2 ist damit code-complete** (ROADMAP.md: 🟡). Fehlt für ✅ „live-verifiziert" (§5.9):
die Quick-Tunnel-Probe durch den Nikinger (Runbook oben) — ein echter Read und ein echter Write
über den Claude-Connector gegen den echten `DATA_ROOT`. Das ist die einzige verbleibende
Handlung dieser Phase, die Claude Code nicht selbst ausführen darf (Hard Rule: kein Test gegen
den echten `DATA_ROOT` durch Claude Code; Tunnel/Connector-Einrichtung ist ohnehin
Nikinger-Sache).

**Nächster Schritt (konkret):** Nikinger führt die Quick-Tunnel-Probe aus (Runbook oben) und
meldet das Ergebnis. Danach: offizieller Phasenabschluss P2 (laut `docs/PROMPTS.md` als eigener
Prompt im Browser-Webchat, analog zu Phase 1s Abschluss) — Status auf ✅, Handover-Dokument für
P3 (Tunnel/systemd/Ops), neue Browser-Planungssession für Phase 3.

## Session stopped — 2026-07-26 (Step 6: Die sechs Tools)

**Ergebnis:** `mcpserver/tools.py` fertig — `search_items`, `get_item`, `create_item`,
`update_item`, `append_to_item` lösen ihre `NotImplementedError`-Platzhalter aus Step 5 ein.
Neue Modul-Helfer wie im Plan gefordert: `wrap_untrusted()` (§3.5, Ersatzstring wörtlich aus
dem Plan übernommen), `summary_to_dict()`, `item_to_filetext()` (dupliziert bewusst
`storage.store._item_to_text`s Feldreihenfolge — der P1-Contract ist seit Step 2 „wieder zu",
eine weitere Erweiterung wäre keine „einmalige" mehr), `compact_json()`, `map_storage_error()`
(§3.6, alle sechs Fehlerfälle inkl. `PermissionDenied` als P2-eigenem Typ). `test_tools.py` neu
mit allen 20 im Plan benannten Tests plus zwei zusätzlichen (siehe unten). `test_app.py` bekam
einen siebten … achten Test: `test_all_six_tools_are_callable_over_http`, der Step 6s eigenes
Done-when „alle sechs Tools über den ASGI-Testclient aufrufbar" gegen den echten Stack aus
Step 5 beweist (ein voller Rundlauf: `list_spaces` → `create_item` → `search_items` →
`get_item` eigen/fremd → `append_to_item` → `update_item`-Konflikt → `update_item(status=
archived)`).

**Testdesign-Entscheidung, hier festgehalten statt stillschweigend:** `test_tools.py` mockt
`context.assert_principal_matches_request` auf ein No-op (autouse-Fixture) und ruft die von
`tools.register()` zurückgegebenen rohen Tool-Funktionen direkt auf — `@mcp.tool(...)` gibt die
unveränderte Python-Funktion zurück, nicht ein `FunctionTool`-Objekt (empirisch geprüft, nicht
angenommen: ein `type(foo)` nach der Dekoration ist weiterhin `function`). Begründung: die
komplette HTTP/ASGI/Guard-Kette ist bereits in `test_app.py::test_principal_isolation_under_
concurrency` (Step 5) end-to-end bewiesen; zwanzig Tests bräuchten sonst zwanzigmal eine echte
FastMCP-App. `test_create_item_has_no_space_parameter` prüft deshalb `inspect.signature()`
direkt auf der zurückgegebenen Funktion.

**Echter Fund während der Implementierung, nicht nur ein Advisor-Verdacht bestätigt:** die
Step-4-Advisor-Notiz („`map_storage_error()` in Step 6 muss die `AuthError`-als-Tool-Fehler-
Abbildung bewusst treffen, nicht zufällig") war zunächst NICHT umgesetzt — jeder Tool-Body rief
`context.current_principal()` + `context.assert_principal_matches_request()` direkt auf, außerhalb
jedes `try`/`except`. Ein Guard-`AuthError` wäre also roh durchgefallen statt über
`map_storage_error()` zu laufen. Gefunden im Advisor-Review vor dem Commit, behoben durch
`_authenticated_principal()` (bündelt Schritt 1+2 aus §3.3, fängt `AuthError` und wirft den
gemappten `ToolError`). Regressionstest `test_guard_auth_error_is_mapped_to_tool_error` beweist
es. **Kleinere Selbstkorrektur direkt danach:** ein automatisiertes Suchen/Ersetzen beim Umbau
auf `_authenticated_principal()` hatte dessen eigenen Funktionskörper versehentlich auf sich
selbst umgeschrieben (Endlosrekursion) — vor dem ersten Testlauf bemerkt und korrigiert, aber
festgehalten, weil genau der neue Regressionstest diesen Fehler auch bei einem stillen Commit
gefangen hätte.

**Advisor-Review vor dem Commit, drei weitere Funde, alle behoben:**
1. `test_search_limit_is_clamped_to_max` prüfte nur das im Payload echoete `limit`-Feld gegen
   einem Store mit einem einzigen Item — hätte auch mit einem ungeklemmten Limit bestanden.
   Jetzt >100 Items, Assertion zusätzlich auf `len(payload["items"]) == MAX_LIMIT`.
2. Plan §2.2 nennt `search_items` ausdrücklich als den Pfad, an dem `total`/Paginierung falsch
   werden, sobald `can_read` nicht mehr konstant `True` ist — der `_OwnSpaceOnlyVisible`-Test-
   Double bewies den Seam bisher nur für `list_spaces`. Neuer Test
   `test_search_filters_by_can_read_and_reports_filtered_total` beweist ihn jetzt auch für
   `search_items` (`total` zählt die gefilterte, nicht die rohe Trefferzahl).
3. `test_search_result_size_budget` maß den günstigsten Fall (leere Bodies → leere Snippets).
   Fixture jetzt mit realistischer Body-Länge (volles 160-Zeichen-Snippet) und einer Mischung
   aus eigenem und fremdem Space (Wrap-Overhead fließt ins Budget ein) — Budget hält weiterhin.

**Bekannte, dokumentierte Grenze (kein Bug):** `search_items` holt bis zu `_STORE_FETCH_LIMIT =
5000` Treffer vom Store (der ohnehin jede Datei pro Aufruf scannt, D6), filtert/paginiert
`include_archived`/Rechte/`offset`/`limit` selbst in `tools.py`. Über dieser Grenze würde
`total` still unterzählen — für den Zwei-Personen-Space-Server um Größenordnungen entfernt,
als `[SEAM]`-Kommentar im Code und hier festgehalten statt später neu entdeckt zu werden.

**Verifiziert (live):** 22 Tests in `test_tools.py`, `test_app.py` von 7 auf 8 gewachsen.
`pytest -v` → **129/129 grün** (76 P1 + 53 P2).

**Nächster Schritt (konkret):** Step 7 — `scripts/mcp_smoke.py` (Gegenstück zu `space_cli.py`
aus P1, temporäres `DATA_ROOT`, nie das echte), README-Runbook „Quick-Tunnel-Probe", Größen-
messung im Session-Block. Der Tunnel-Schritt selbst läuft beim Nikinger, nicht in Claude Code
(kein Skript/Config/Hostname wird committet). Danach ist Phase 2 code-complete; die Quick-
Tunnel-Probe (ein Read, ein Write über den echten Claude-Connector) macht sie live-verifiziert.

---

## Session stopped — 2026-07-26 (Step 5: Server und App)

**Ergebnis:** `server.py` (`build_mcp(store, permissions, *, name=...)`), `app.py`
(`create_app(*, settings, resolver, store, allowed_hosts=None)` — `OwnSpaceWritable()` wird
dort instanziiert, nicht injiziert, per Plan §2.2 Erweiterungspfad), `scripts/serve.py`
(`--allowed-host`, `access_log=False`). `mcpserver/tools.py` musste dafür bereits entstehen
(siehe Modul-Status-Anmerkung Zeile 7 — kein stiller Contract-Vorgriff): `list_spaces` ist
vollständig implementiert, die übrigen fünf Tools sind mit finaler Signatur/Annotations
registriert und werfen `NotImplementedError` bis Step 6.

**Vom Advisor vor Beginn geprüfte Spannung im Plan-Text, aufgelöst statt blind übernommen:**
Step 5s eigenes „Done when" verlangt `tools/list` mit sechs annotierten Tools und einen
Isolationstest mit echtem Tool-Verhalten — Step 5s Dateiliste nennt aber nur
`server.py`/`app.py`/`serve.py`, `tools.py` steht explizit unter Step 6. Auflösung (bestätigt
gegen §1.2 Abhängigkeitstabelle „`server.py` kennt `tools`" und §7-Warnung vor Vorziehen):
`tools.py` wird in Step 5 mit allen sechs Registrierungen angelegt, aber nur so viel echtem
Verhalten wie der Isolationstest braucht (`list_spaces`) — Step 6 bleibt für Wrapping/
Fehlerabbildung/Token-Budget zuständig, keine Vorwegnahme.

**V2 final bestätigt (nicht nur `[VERIFY]` übernommen):** `fastmcp==3.4.4`,
`FastMCP.http_app(path=…, stateless_http=…, allowed_hosts=…, …)` — Signatur exakt wie geplant,
per `inspect.signature` gegen das echte Paket geprüft, nicht nur gelesen.

**V4 aufgelöst, empirisch gegen eine echte FastMCP-App, nicht nur gegen den Fake-Innen-App aus
Step 4:** die in `asgi.py` (Step 4) implementierte Pfad-Arithmetik (`route_path =
path[len(root_path):]`, `new_path = root_path + "/" + rest if rest else root_path + "/"`)
funktioniert unverändert, wenn `TokenPathASGI` zusätzlich hinter einem echten
`Mount("/mcp", …)` sitzt. Grund, empirisch nachvollzogen: Starlettes `Mount.matches()` ändert
`scope["path"]` **nicht** — nur `scope["root_path"]` wächst um den Mount-Präfix (`""` → `"/mcp"`).
Für den Normalfall `POST /mcp/<token>` (kein weiteres Pfadsegment) liefert die Arithmetik
`rest=""` und damit `new_path = "/mcp/"` — genau der `route_path == "/"`, den die innere
FastMCP-App erwartet (erzeugt mit `path="/"`). Verifiziert per Wegwerfskript gegen ein echtes
`FastMCP`+`Starlette`-Setup (kein Fake): `GET /health` → 200, `POST /mcp/<gültiges-token>` mit
einer echten `initialize`-Anfrage → 200 mit korrekter MCP-Antwort, `POST /mcp/<unbekannt>` →
401 leer. Keine Code-Änderung an `asgi.py`/`context.py` nötig — Step 4s Lösung trägt durch den
echten Mount hindurch.

**Isolationstest (`test_app.py::test_principal_isolation_under_concurrency`) — die wichtigste
Zusicherung der Phase, jetzt grün gegen eine echte, laufende FastMCP-App:** zehn `list_spaces`-
Aufrufe über `asyncio.gather`, alternierend zwei Tokens (`alpha`/`beta`, Fixture-Namen statt
Nikinger/Kollege — Plan §2.2), echte Nebenläufigkeit auf einem Event-Loop (nicht sequenziell).
Jeder Aufruf sieht `writable=true` exakt für den eigenen und `writable=false` für den fremden
Space — kein Cross-Space-Leak. Technischer Unterbau: `httpx.ASGITransport` (kein echter Port,
kein Netz) + `fastmcp.Client`/`StreamableHttpTransport` mit injiziertem
`httpx_client_factory`; Lifespan manuell über `app.router.lifespan_context(app)` statt
simulierter ASGI-Lifespan-Nachrichten — Starlettes eigener Mechanismus, ohne
Zusatzabhängigkeit (`asgi-lifespan` ist nicht installiert und wurde bewusst nicht ergänzt).

**Advisor-Review vor dem Commit — ein Fund korrigiert, einer verschärft:**
1. `test_mcp_requires_token` deckte `POST /mcp/` (leeres Credential → unser 401) und
   `POST /mcp/<unbekannt>` ab, aber nicht `POST /mcp` **ohne** Trailing-Slash. Empirisch geprüft:
   das trifft Starlettes eigenes `redirect_slashes` **vor** `TokenPathASGI` und antwortet mit
   **307** nach `/mcp/`, leerer Body, `Location`-Header ohne Space-/Pfad-/Tokendaten.
   Kein Verstoß gegen P2-N (das 307 sagt nichts über Tokengültigkeit — in diesem Request gibt es
   noch gar kein Token-Segment), aber eine dritte, von außen unterscheidbare Antwortform, die
   sonst erst bei der Live-Tunnel-Probe aufgefallen wäre. Jetzt eigener Test:
   `test_mcp_bare_mount_redirects_without_leaking`.
2. `test_health_leaks_no_space_names` prüfte nur auf Teilstrings (`"alpha" not in body_text`)
   gegen eine Antwort, die strukturell gar keine Space-Daten enthalten kann — vacuous. `test_health_ok`
   prüft jetzt zusätzlich die exakte Schlüsselmenge (`{"status","service","version"}`), das
   fängt eine spätere Feldergänzung ab, nicht nur zufällig gewählte Fixture-Namen.

**Verifiziert (live):** 7 Tests in `test_app.py` — `test_health_ok`,
`test_health_leaks_no_space_names`, `test_mcp_requires_token`,
`test_mcp_bare_mount_redirects_without_leaking`, `test_tools_list_returns_six_tools`,
`test_tools_list_annotations_present`, `test_principal_isolation_under_concurrency`.
`pytest -v` → **106/106 grün** (76 P1 + 30 P2).

**Nächster Schritt (konkret):** Step 6 — `mcpserver/tools.py` fertigstellen: `search_items`,
`get_item`, `create_item`, `update_item`, `append_to_item` (§3.2/§3.4), `<untrusted_content>`-
Wrapping + Escaping (§3.5), Fehlerabbildung inkl. des in Step 4 vermerkten
`AuthError`-als-Tool-Fehler-Falls (§3.6), Token-Budget-Klemmung (`DEFAULT_LIMIT`/`MAX_LIMIT`,
bereits als Modulkonstanten in `tools.py` vorhanden). `test_tools.py` neu, `list_spaces`
braucht dort keine erneute Grundimplementierung, nur ggf. Härtung/Formatkonsistenz mit den
anderen fünf Tools.

---

## Session stopped — 2026-07-25 (Step 4: Auth, Rechte, Request-Kontext)

**Ergebnis:** `auth.py` (`Principal` frozen dataclass mit gekürztem `__repr__`,
`AuthError`, `SpaceResolver`-Protokoll, `KeyringTokenResolver` mit injiziertem `load_map`,
Dict-Lookup über `sha256(credential)`), `permissions.py` (`Permissions`-Protokoll,
`OwnSpaceWritable`), `logging_setup.py` (`configure_logging()`, `TokenScrubbingFilter` —
ersetzt `/mcp/<segment>` durch `/mcp/<redacted>` in Message **und** Args), `context.py` +
`asgi.py` (`TokenPathASGI`, Details siehe **wichtiger Fund** unten).

**V3 aufgelöst:** `fastmcp.server.dependencies.get_http_request` importiert sauber gegen das
echte `fastmcp==3.4.4` — der im Plan dokumentierte Importpfad stimmt, `fastmcp.dependencies.
CurrentRequest()` ist eine andere (Dependency-Injection-)API für denselben Zweck, nicht die
hier gebrauchte direkte Funktion.

**Wichtiger Fund (empirisch, nicht nur gelesen) — §2.4 ist an einer Stelle nicht umsetzbar wie
geschrieben:** Der Plan beschreibt `assert_principal_matches_request()` als „zieht das
Token-Segment aus dessen Pfad". Das geht nicht: `TokenPathASGI` muss das Token-Segment aus dem
Pfad entfernen, **bevor** es an die innere FastMCP-App delegiert (sonst sieht FastMCPs eigenes
Routing das Segment als Teil des MCP-Pfads und die Anfrage schlägt fehl). Ein Tool, das während
seiner Ausführung `get_http_request().url.path` liest, sieht deshalb nur noch den bereinigten
Pfad.

Zwei ASGI-Mounting-Techniken gegen ein echtes `fastmcp==3.4.4` + `starlette`-Setup
(`httpx.ASGITransport`/`starlette.testclient.TestClient`) durchprobiert:
1. **`root_path`-Akkumulation** (Starlettes eigene Technik, `scope["path"]` bleibt unverändert,
   nur `root_path` wächst) — scheitert an `redirect_slashes`: ein Credential-Segment ohne
   nachfolgenden Pfad lässt `route_path` leer statt `"/"` werden, Starlette antwortet mit 307
   auf eine URL mit angehängtem `/`, bevor die innere App je läuft.
2. **Direkte `path`/`raw_path`-Kürzung** (Plan-Wortlaut) — funktioniert für das Routing
   (kein Redirect, Tool wird aufgerufen), aber `get_http_request().url.path` liefert dann
   nachweislich `"/mcp/"`, nicht das Token — bestätigt das Problem oben empirisch, nicht nur
   theoretisch.

**Lösung:** `TokenPathASGI` hinterlegt `token_hash` in `scope["state"]`, **bevor** es den Pfad
kürzt (Technik 2 bleibt fürs Routing). `scope["state"]` überlebt die Weiterleitung unverändert —
Starlettes offizieller Mechanismus, um Zustand über eine ASGI-Kette hinweg mitzugeben, per
Testprobe bestätigt: `request.state.token_hash` kam im Tool korrekt an. Die
Sicherheitseigenschaft ist identisch zur Plan-Absicht: der Guard vergleicht „was hat unsere
eigene ASGI-Schicht für DIESEN Request aufgelöst" (`scope["state"]["token_hash"]`, gesetzt von
`TokenPathASGI`) gegen „was liefert `get_http_request()` gerade zurück" (`current_principal()`
aus dem ContextVar) und schlägt bei jeder Abweichung laut fehl (`AuthError`) — nicht mehr über
den Pfad, aber mit derselben Garantie. Vollständige Begründung im Docstring von `context.py`.
**Kein Test dafür in Step 4** (braucht einen echten laufenden Request-Kontext) — end-to-end
geprüft in Step 5 über `test_app.py::test_principal_isolation_under_concurrency`.

**Verifiziert (live):** 14 neue Tests (`test_auth.py` ×4, `test_permissions.py` ×3,
`test_logging.py` ×1, `test_context.py` ×2 — nicht im Plan gefordert, aber `current_principal`/
`set_principal`/`reset_principal` sind eigenständige, netzunabhängige Logik —,
`test_asgi.py` ×4 gegen einen Fake-Resolver + Fake-Innen-App, keine echte FastMCP-App nötig für
diese Schicht). `pytest -v` → **99/99 grün** (76 P1 + 23 P2). `test_principal_reset_after_request`
bestätigt: nach dem Request wirft `current_principal()` wieder `AuthError` — kein Leck zwischen
Requests.

**Anmerkung des Advisors, hier festgehalten statt in Step 6 neu zu entdecken:** P2-N sagt
„`AuthError` → HTTP 401, nie ein Tool-Fehler". Der Guard läuft aber *innerhalb* eines
Tool-Aufrufs (§3.3 Schritt 2) — das 401-Fenster ist zu diesem Zeitpunkt vorbei, ein
Guard-`AuthError` muss also zwangsläufig als Tool-Fehler auftauchen. Das ist kein Defekt (immer
noch fail-closed, keine fremden Daten), aber `map_storage_error()` in Step 6 muss diese
Abbildung bewusst treffen, nicht zufällig.

**Nächster Schritt (konkret):** Step 5 — `server.py`, `app.py`, `scripts/serve.py`. Das ist die
Stelle, an der `TokenPathASGI` erstmals gegen eine echte FastMCP-App läuft — V4 (`Mount`-
Verhalten) und der `assert_principal_matches_request()`-Guard werden dort erstmals end-to-end
statt isoliert geprüft.

---

## Session stopped — 2026-07-25 (Step 3: Credentials + Token-Ausgabe)

**Ergebnis:** `mcpserver/credentials.py` (`KEYRING_SERVICE = "nikinger-space"`,
`KEYRING_KEY_SPACES = "spaces"`, `generate_token()` → `secrets.token_urlsafe(32)`,
`hash_token()` → sha256-Hex, `load_space_map()`/`save_space_map()`, `issue(space) -> str`,
`revoke(space) -> int`). `keyring` wird ausschließlich in diesem Modul importiert. Im Keyring
liegt nur `{sha256(token): space}` — kein umkehrbares Geheimnis. `phase2_mcp/scripts/
issue_token.py` (`--space`/`--revoke`/`--list`, mutually exclusive): das Token ist das
**einzige** stdout dieses Skripts, und nur beim Ausgeben; alles andere (Warnhinweis, Revoke-
Bestätigung, die Listing-Zeilen) geht auf stderr (Hard Rule 7 — hier besonders eng ausgelegt,
weil das Skript mit dem Geheimnis selbst hantiert).

**Verifiziert (live):** sechs neue Tests in `phase2_mcp/tests/test_credentials.py`
(`test_hash_token_is_stable_hex64`, `test_generate_token_length_and_uniqueness`,
`test_load_space_map_missing_key_returns_empty`, `test_save_load_roundtrip_with_fake_backend`,
`test_issue_stores_only_hash`, `test_revoke_removes_all_hashes_of_space`) — alle gegen einen per
`monkeypatch` gefakten `keyring.get_password`/`set_password` (In-Memory-Dict), fassen den
echten Keyring nie an. `test_issue_stores_only_hash` prüft explizit, dass weder das Klartext-
Token noch irgendein Wert der Map dem Token entspricht — nur der Hash. `pytest -v` →
**85/85 grün** (76 P1 + 9 P2, davon 3 `test_config.py` + 6 `test_credentials.py`).

**V5 — Status nach diesem Schritt:** `keyring --list-backends` zeigt weiterhin
`SecretService.Keyring` (Priorität 5) als real installiertes Backend (aus Step 1). Ein echter
Schreib-/Lese-Roundtrip **gegen dieses Backend** (nicht den Test-Fake) wurde von mir bewusst
**nicht** ausgeführt — das würde in den echten, produktiven Keyring-Eintrag unter Service
`nikinger-space` schreiben, denselben, den P3 später für den echten Connector benutzt. Das ist
strukturell derselbe Fall wie „nie gegen den echten `DATA_ROOT` testen": ein echtes Secret in
einem echten System-Backend ist kein Objekt für einen Probe-Write durch Claude Code. **Modul-
Status Zeile 4 bleibt deshalb 🟡, nicht ✅**, bis der Nikinger einmal real
`python phase2_mcp/scripts/issue_token.py --space nikinger` laufen lässt und das Ergebnis
bestätigt (Token erscheint auf stdout, `--list` zeigt danach den Space mit gekürztem Hash).

**Nachtrag (Nikinger-Bestätigung + Incident, 2026-07-25):** Der Nikinger hat den echten Roundtrip
gefahren. **V5 damit vollständig bestätigt** — `issue_token.py --space nikinger` lief gegen das
echte `SecretService`-Backend, Token erschien einmalig auf stdout, `--list` zeigte danach
`nikinger: <hash-prefix>…` auf stderr. Modul-Status Zeile 4 auf ✅ gehoben.

**Incident, kein stiller Vorbeigang:** Der erste Testlauf wurde vom Nikinger komplett samt
Klartext-Token in den Chat eingefügt — nicht nur der Hash, das Bearer-Token selbst landete damit
in einer Konversation außerhalb des Keyrings, strukturell gleichwertig zu „Token in einem
Commit" (Hard Rule 1: Incident, kein Schönheitsfehler). Sofort erkannt und gemeldet, statt
stillschweigend weiterzumachen. **Behoben durch Rotation:** der Nikinger hat
`--revoke nikinger` (1 Token entfernt) gefolgt von einem neuen `--space nikinger` ausgeführt und
das neue Token diesmal **nicht** in den Chat eingefügt, sondern lokal in
`../nikinger only/bearer_token.md` (außerhalb dieses Code-Repos, nicht Teil von `DATA_ROOT`
oder eines Git-Trackings hier) abgelegt. `--list` bestätigt genau einen aktuellen Eintrag für
`nikinger`. Für künftige Sessions: **Klartext-Tokens gehören nie in den Chat-Verlauf**, auch
nicht „nur zum Testen" — dieselbe Regel wie für Commits.

**Doku-Pflichten aus Plan §2.3, im selben Commit:** `README.md` — neuer Abschnitt „Token
ausgeben, rotieren, widerrufen" (die drei Kommandos, „genau einmal angezeigt", Vorgehen bei
Verlust). Root-`CLAUDE.md` Hard Rule 1 — datierte Korrekturnotiz (`storage/credentials.py`
wurde nie gebaut, realer Pfad ist `phase2_mcp/mcpserver/credentials.py`; die Regel selbst
unverändert). Dieser Head — die beiden vorgezogenen Absätze „Warum nur Hashes im Keyring" und
„Was der Pfad-Token nicht ist" von „vorgezogen, Step 3 liefert Code" auf den realen Codestand
aktualisiert.

**Nächster Schritt (konkret):** Step 4 — `auth.py`, `permissions.py`, `context.py`, `asgi.py`,
`logging_setup.py`. Kein Keyring-Zugriff dort direkt (nur über injizierte `load_map`), also kein
weiterer V5-Haltepunkt nötig — der steht weiterhin offen, bis der Nikinger den echten Roundtrip
bestätigt.

## Session stopped — 2026-07-25 (Step 2: P1-Contract-Erweiterungen)

**Ergebnis:** Die drei vom Nikinger freigegebenen, einmaligen Erweiterungen (Plan §0.4 Punkt L,
§4 Step 2) in `phase1_storage/storage/` eingebracht:
- `models.py`: `STATUS_VALUES` (Statusvokabular je `type`) + `valid_statuses()`.
- `store.py`: neuer Helper `_check_type_and_status()`, aufgerufen aus `create()` und `update()`
  — wirft `ValidationError` bei unbekanntem `type` oder unerlaubtem `status` (D2).
- `store.py :: space_of(item_id)` — reiner Index-Lookup, kein Datei-Read, `ItemNotFound` bei
  unbekannter ID.
- `store.py :: get(item_id, *, repair_drift=True)` + `_reconcile_and_get_row(...,
  repair_drift=True)` — bei `repair_drift=False` und erkannter Drift wird nur der Index
  nachgezogen, kein Frontmatter-Rewrite, kein Git-Commit (D3). Default `True` lässt jedes
  bestehende P1-Verhalten unverändert.

**Details, Code-Anker und die vollständige Begründung stehen in `phase1_storage/CLAUDE.md`**
unter „Geerbte Contracts" (Code-nah, nicht hier dupliziert — Vorgabe aus diesem Head selbst,
„Was hier bewusst NICHT steht").

**Verifiziert (live):** acht neue Tests in `phase1_storage/tests/test_store.py`
(`test_space_of_returns_space`, `test_space_of_unknown_raises_item_not_found`,
`test_get_repair_drift_false_leaves_file_untouched`, `test_get_repair_drift_false_creates_no_commit`,
`test_get_repair_drift_true_still_bumps`, `test_create_rejects_unknown_status`,
`test_update_rejects_unknown_status`, `test_update_accepts_valid_status_per_type`). Gesamtsuite
`pytest -v` → **79/79 grün** (76 in `phase1_storage/tests/` inkl. dieser acht, 3 in
`phase2_mcp/tests/`). Keine bestehende P1-Test musste angepasst werden — die einzigen
Store-Aufrufe mit explizitem `status=` in `test_store.py` (`status="open"` auf einem `task`,
`status="done"` auf einem `task`) waren bereits typkonform.

**Nächster Schritt (konkret):** Step 3 — `credentials.py` + `scripts/issue_token.py`. Braucht
eine Nikinger-Rückmeldung, sobald der finale Funktionstest (`keyring`-Wert schreiben und
zurücklesen) gelaufen ist — V5 ist bis dahin „vielversprechend", nicht „bestätigt".

## Session stopped — 2026-07-25 (Step 1: Paketgerüst)

**Ergebnis:** `phase2_mcp/pyproject.toml` (Paket `mcpserver`, spiegelt
`phase1_storage/pyproject.toml` exakt bis auf Name/Description/Dependencies —
`dependencies = ["storage", "fastmcp>=3.4,<3.5", "keyring>=25"]`,
`dev = ["pytest", "pytest-asyncio", "httpx"]`), `mcpserver/__init__.py`
(`__version__ = "0.1.0"`), `mcpserver/config.py` (`Settings`-Dataclass `frozen, kw_only`:
`data_root: Path` Pflicht ohne Default, `host="127.0.0.1"`, `port=8765`, `log_level="INFO"`;
`load_settings(env)` liest `SPACE_DATA_ROOT`/`SPACE_HOST`/`SPACE_PORT`/`SPACE_LOG_LEVEL`, wirft
`ValueError` bei fehlendem `SPACE_DATA_ROOT` oder nicht-parsbarem `SPACE_PORT`). Kein Secret in
`Settings` — `config.py` kennt laut Modulübersicht „nichts", importiert entsprechend nur
Standardbibliothek.

**Drift gegenüber dem Plan, dated:** Plan §4 Step 1 nennt `tests/__init__.py` als Datei. P1 hat
in `phase1_storage/tests/` nie ein `__init__.py`, sondern ein leeres `conftest.py` als
Platzhalter (Step 0 des P1-Plans). Hier aus Konsistenzgründen mit dem bereits etablierten
Repo-Vorbild identisch gehalten: `phase2_mcp/tests/conftest.py` (leer) statt `__init__.py`.
Funktional gleichwertig für `pytest`-Discovery.

**Notwendige Ergänzung, die der Plan nicht auflistete:** `pytest.ini` (`testpaths =
phase1_storage/tests`) hätte `phase2_mcp/tests/` nie gefunden. Erweitert auf
`testpaths = phase1_storage/tests phase2_mcp/tests` — sonst wären alle P2-Tests ab hier
unsichtbar für `pytest` gewesen, ohne dass ein Fehler das angezeigt hätte.

**Verifiziert (live):** `./scripts/dev_install.sh` fand `phase2_mcp/` automatisch über den
`phase*_*/`-Glob (keine Änderung am Skript nötig, wie im Plan erwartet), installierte `storage`
und `mcpserver` editable, zog `fastmcp==3.4.4` (exakt die in Step 0 als aktuellste 3.4.x-Version
verifizierte) und `keyring==25.7.0` echt aus PyPI. `from mcpserver import __version__` →
`"0.1.0"`. `pytest -v` → **71/71 grün** (68 aus P1 + 3 neue in `test_config.py`:
`test_load_settings_requires_data_root`, `test_load_settings_defaults`,
`test_load_settings_port_invalid_raises`).

**V5 (Keyring-Backend) weiter aufgelöst, noch nicht endgültig:** `keyring --list-backends` nach
echter Installation zeigt `keyring.backends.SecretService.Keyring` mit Priorität 5 (höchste) —
das in Step 0 vermutete Backend ist real verfügbar, nicht nur plausibel. Endgültig verifiziert
ist V5 erst, wenn Step 3 tatsächlich einen Wert schreibt und zurückliest (`credentials.py`
existiert noch nicht).

**Nächster Schritt (konkret):** Step 2 — die drei freigegebenen P1-Contract-Erweiterungen
(`space_of()`, `get(..., repair_drift=)`, Statusvalidierung) in `phase1_storage/storage/`.
Kein weiterer Haltepunkt vorgesehen (Plan §4 Step 2 ist mechanisch, Erweiterungen sind bereits
freigegeben).

## Session stopped — 2026-07-25 (Step 0: Haushalt + Verifikationsdurchlauf)

**Ergebnis:** Erster Claude-Code-Durchlauf für Phase 2. Kein Feature-Code — Step 0 ist reiner
Haushalt, wie im Plan (`docs/concepts/phase2_mcp_plan.md` §4 Step 0) vorgegeben.

**Drift gegenüber dem Plan, hier festgehalten statt beim Commit improvisiert:** Der Plan
listet `phase2_mcp/CLAUDE.md` erst unter Step 1 („Paketgerüst"). Hard Rule 8 verlangt aber,
dass **jeder** Step-Commit die Modul-Tabelle und den Session-Block **eines Phase-Heads**
aktualisiert — und Root-`CLAUDE.md`s `down:`-Link auf die aktive Phase brauchte ohnehin ein
reales Ziel. Deshalb dieser Head + `SESSIONS_ARCHIVE.md` bereits in Step 0 angelegt, mit
Rotationsregel und Skriptverweis von Anfang an (nicht wie in P1 erst nachträglich eingeführt).
Step 1 füllt das Paketgerüst (`pyproject.toml`, `mcpserver/__init__.py`, `mcpserver/config.py`)
und aktualisiert diesen Head weiter.

**A · Rotationsregel operationalisiert (Herkunft: `PHASE1_CLOSEOUT_HANDOVER.md` A1–A3):**
1. `phase1_storage/CLAUDE.md`: die verbliebene Überschrift `## Phase 1 ist live-verifiziert (…)`
   auf das Schema gebracht → `## Session stopped — 2026-07-25 (Phase 1 live-verifiziert, Phase
   abgeschlossen)`.
2. `scripts/rotate_session_block.sh` (lag bereits fertig geschrieben und ungetrackt im Repo,
   nicht von dieser Session verfasst) eingecheckt, `chmod +x`, für `phase1_storage` gelaufen:
   Head 35.053 B → 9.479 B, Archiv 2.308 B → 27.882 B, ein Block (346 Zeilen) verlustfrei
   verschoben, Reassemblierung + Byte-Rückvergleich bestanden. `.bak`-Dateien nach Sichtprüfung
   gelöscht. Manuelle Nacharbeiten erledigt: `SESSIONS_ARCHIVE.md`-Frontmatter `updated:` auf
   2026-07-25, `docs/INDEX.md`-Größenangaben nachgezogen, Nahtstellen sauber (eine Leerzeile,
   keine doppelte).
3. Verweise gesetzt: Root-`CLAUDE.md` („Doku-Hygiene"), `phase1_storage/CLAUDE.md` („Harte
   Regeln", `sed -n 'A,Bp'`-Wortlaut ersetzt), `docs/PROMPTS.md` (Prompt 1 + Prompt 3 Punkt 4)
   nennen jetzt den Skriptaufruf. `docs/DOC_LAYERS_CONVENTION.md` unangetastet (byte-identische
   Kopie). Keine Indexzeile für die `.sh`.

**B · Verifikationsdurchlauf:**
- `up:`/`down:`-Ziele: alle auflösbar nach dieser Session (Root-`CLAUDE.md` zeigte auf
  `phase1_storage/CLAUDE.md`, jetzt auf diesen Head umgehängt).
- Fehlende Indexzeilen gefunden und ergänzt: `docs/concepts/PHASE1_CLOSEOUT_HANDOVER.md`,
  `docs/concepts/phase2_mcp_plan.md`, dieser Head, `SESSIONS_ARCHIVE.md` — alle jetzt in
  `docs/INDEX.md` unter „Active phase (2)" bzw. „Completed phases".
- `find . -name "*.md" -size +40k`: einziger Treffer `docs/concepts/phase2_mcp_plan.md`
  (46.833 B) — ist 📕, also regelkonform trotz Überschreitung des Softcaps.
- `files.rename_for_new_slug()` war toter Produktivcode (`store.py` nutzt `files.move_file()`
  direkt, bestätigt per `grep`) — entfernt, samt der zwei Tests in `test_files.py`. P1-Tests
  70 → 68, `pytest` grün. Doku-Drift im (jetzt archivierten) Step-2-Session-Block mit datierter
  Korrektur versehen, **bevor** die Rotation lief.
- Branchname `master` (`DATA_ROOT`) vs. `main` (Code-Repo): bestätigt kosmetisch, kein Remote
  betroffen, jetzt in `README.md` als bewusst eingefroren dokumentiert.
- Drei Schreibweisen (`sharefyx`/`/home/savefyx/…`/`/home/savefyx/dev/savefxy`): in `README.md`
  als bewusst eingefroren dokumentiert (Nikinger-Entscheidung 2026-07-25) — eine Umbenennung
  würde Pfade brechen, die P3 in systemd-Units schreibt.

**C · Festlegungen eingetragen:** `ROADMAP.md` — OAuth (bisher P5) rückt direkt hinter P3 auf
P4, Web-UI (bisher P4) rückt auf P5 dahinter; neuer Abschnitt „Zurückgestellt aus P2" mit drei
Einträgen (D6, MCP-Revision 2026-07-28, Lese-Rechte zwischen Spaces); P2-Zeile auf 🔄. Root-
`CLAUDE.md` „Current state": aktive Phase jetzt P2, `down:` auf `phase2_mcp/CLAUDE.md`
umgehängt, P1 zu einem knappen abgeschlossenen Absatz verdichtet.

**`[VERIFY]`-Register, Ergebnisse dieser Session (siehe Plan §8):**
- **V1** (Repo-Stand nach P1-Abschluss) — aufgelöst, siehe A/B oben.
- **V2** (`fastmcp`-Version) — aufgelöst: `pip index versions fastmcp` zeigt `3.4.4` als
  aktuellste 3.4.x-Version, exakt im gepinnten Fenster `>=3.4,<3.5`. Kein Drift.
- **V3** (Importpfad `get_http_request`) — **offen**, `fastmcp` ist noch nicht installiert
  (kommt erst Step 1). Bei Ausführung von §2.4 gegen die echte installierte Version prüfen.
- **V4** (`Mount("/mcp")`-Verhalten) — **offen**, hängt an Step 5 (`app.py` existiert noch nicht).
- **V5** (Keyring-Backend auf der VM) — **vielversprechend, aber nicht final**: `dbus-daemon`
  und `gnome-keyring-daemon` sind installiert, `DBUS_SESSION_BUS_ADDRESS` ist gesetzt — das
  SecretService-Backend sollte funktionieren. Python-Paket `keyring` ist noch nicht installiert
  (kommt Step 3); `keyring --list-backends` dort final prüfen und dem Nikinger melden statt
  selbst eine Datei-Fallback-Lösung zu wählen.
- **V6** (Python-Version) — aufgelöst: `Python 3.12.3` auf der VM, `.venv` nutzt dieselbe
  Version. Erfüllt ≥3.10 komfortabel.
- **V7** (Custom Connectors auf Pro) — **offen**, gehört zu Step 7 (Runbook).
- **V8** (Größenbudget gegen echte Beispieldaten) — **offen**, gehört zu Step 6.
- **V9** (Namensinkonsistenzen im echten `DATA_ROOT`) — aufgelöst per read-only `ls`:
  `/home/savefyx/savefyx-data/` enthält genau einen Space-Ordner (`nikinger`), kein
  Umbenennungsbedarf.

**Baseline vor jeder P2-Änderung (live geprüft):** `pytest` in `phase1_storage/` lief 70/70
grün vor der Entfernung von `rename_for_new_slug()`, danach 68/68 grün — Regression
ausgeschlossen, nicht nur behauptet.

**Für Step 1 vorgemerkt:** Paketgerüst `phase2_mcp/pyproject.toml` (Paket `mcpserver`,
Abhängigkeit auf `storage` + `fastmcp>=3.4,<3.5` + `keyring>=25`), `mcpserver/__init__.py`,
`mcpserver/config.py` mit `Settings`/`load_settings()`. `scripts/dev_install.sh` findet das
Verzeichnis automatisch (Glob über `phase*_*/`) — keine Änderung dort nötig.

**Nächster Schritt (konkret):** Step 1 (Paketgerüst) — kein weiterer Haltepunkt vor Step 2
(P1-Contract-Erweiterungen) vorgesehen, da beide klein und mechanisch sind; Step 3 (Credentials)
braucht wieder eine Nikinger-Rückmeldung wegen V5.

