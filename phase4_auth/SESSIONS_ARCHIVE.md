---
status: live
purpose: Archiv älterer Session-stopped-Blöcke aus phase4_auth/CLAUDE.md, newest-first, verbatim
read-when: Audit vergangener Sessions dieser Phase; NICHT für normalen Session-Start
detail: L3
up: CLAUDE.md
updated: 2026-07-29
---
# Session-Archiv — Phase 4 OAuth 2.1 + DCR

Newest-first. Sieben Rotationen bisher (Abschluss Step 3, dann Step 4, dann Step 5, dann Step
6a, dann Step 6b, dann die Step-7-Code-Vorbereitung, dann Befund S1 + Sicherheits-Review,
2026-07-28/29) — via
`scripts/rotate_session_block.sh phase4_auth`, nie von Hand.

## Session stopped — 2026-07-29 (Step 7, Code-Vorbereitung)

**Ergebnis:** Alles, was Step 7 **ohne** echte VM/echten Keyring/echte Claude-Accounts bauen
lässt, ist fertig — die Live-Teile (Provisionierung, `systemd-creds`, `systemctl restart`,
Connector, Abnahmematrix) sind Sache des Nikingers (Runbook oben). `pytest -q` →
**350/350 grün** (331 Vorlauf + 19 neue). **Phase 4 bleibt 🟡, nicht ✅** — Step 7 selbst ist
nicht abgeschlossen, nur code-vorbereitet.

**Gebaut:**
- `phase4_auth/systemd/sharefyx-mcp.service` — **umgezogen** von `phase3_edge/systemd/` (Plan
  §5 Step 7: „ERSETZT die P3-Fassung", inhaltlich jetzt eine P4-Unit). `git mv`, nicht Kopie
  (Historie bleibt erhalten, keine zwei Quellen für dieselbe Unit — ein zweiter Advisor-Fund
  dieser Session: eine Kopie-statt-Move hätte ein stilles Doppel-Install-Risiko über
  Glob-Reihenfolge geschaffen). Ergänzt: `StateDirectory=sharefyx`, `StateDirectoryMode=0700`,
  `LoadCredentialEncrypted=auth-users:…`, `Environment=SPACE_AUTH_MODE=__AUTH_MODE__`/
  `SPACE_PUBLIC_BASE_URL=__PUBLIC_BASE_URL__`. `Documentation=` zeigt jetzt auf dieses Dokument.
  **`StateDirectory=sharefyx` allein reicht** für den Auth-DB-Pfad — systemd exportiert
  `$STATE_DIRECTORY`, `authserver/config.py` liest exakt diesen Namen, keine zusätzliche
  `Environment=SPACE_AUTH_DB=`-Zeile nötig (geprüft, nicht angenommen).
- `phase3_edge/scripts/install_units.sh` (P4-berührt, bleibt P3-Eigentum): liest jetzt aus
  **zwei** Verzeichnissen (`phase3_edge/systemd/` **und** `phase4_auth/systemd/`); zwei neue
  Platzhalter im Sed-Kommando **und** in der Pflichtvariablen-Prüfung (ein stiller
  Leerstring-Fallback bei fehlendem `local.env`-Eintrag wäre der falsche Fehlermodus). `phase3_
  edge/local.env.example` um `AUTH_MODE`/`PUBLIC_BASE_URL` ergänzt.
- `phase3_edge/tests/test_units.py` (P4-berührt, dieselbe „genuinely necessary"-Begründung wie
  jede andere P4-Q-artige Cross-Phase-Berührung): `UNIT_PATH`/`ALL_UNIT_PATHS` folgen dem Umzug,
  zwei neue Tests (`StateDirectory`, zweites Credential). Kein Test-Verhalten geändert, nur der
  Quellpfad — `pytest phase3_edge/tests/test_units.py` war der Beweis dafür, nicht nur eine
  Behauptung (Advisor-Vorgabe: „das ist der Arbiter, nicht noch eine Runde Nachdenken").
  `phase3_edge/CLAUDE.md` Zeile 5 bekam dieselbe Art datierte Korrekturnotiz wie
  `phase2_mcp/CLAUDE.md`s Testzahl-Drift — historische Zähl-Zeilen bleiben unangetastet.
- `authserver/store.py :: list_clients()`/`list_families(space=)` (additiv, kein Plan-Skelett-
  Eintrag — gleiches Muster wie `create_family` in Step 3), neues `TokenFamily`-Dataclass in
  `models.py`. `authserver/config.py :: resolve_db_path()` aus `load_auth_settings()`
  herausgezogen — ein Operator-Werkzeug, das für „eine Familie widerrufen" plötzlich
  `SPACE_PUBLIC_BASE_URL` verlangt, wäre eine unnötige Hürde für eine SSH-Sitzung.
- `phase4_auth/scripts/authctl.py` (neu) — fünf dünne Unterbefehle (`list-clients`,
  `list-tokens [--space]`, `revoke --family-id`, `unlock --space`, `purge-expired`), je einer
  über eine bestehende `AuthStore`-Methode. **`revoke` kennt nur `--family-id`**, keinen
  `--space`-Sammelwiderruf — komponierbar aus `list-tokens --space` + mehreren `revoke`-Aufrufen,
  bewusst keine zweite Fläche dafür (Advisor-Vorgabe).
- `phase4_auth/scripts/oauth_smoke.py`: `--base-url`-Modus (Plan §5 Step 7 Punkt 4). Passwort/
  TOTP-Seed über `getpass.getpass()`, **nie** als Argument (zwei dokumentierte
  Klartext-Token-Vorfälle in diesem Repo, keinen dritten produzieren). Die elf Prüfungen sind
  jetzt in `_run_checks()` ausgelagert, parametrisiert über `client`/`mcp_client_factory` — vom
  Default- UND vom `--base-url`-Modus gleichermaßen benutzt.
  **Echter Korrekturbedarf beim Refactor gefunden, nicht nur Umbau:** die Discovery-Prüfungen
  verglichen `resource`/`issuer` bisher gegen einen vorab bekannten `AuthSettings`-Wert — im
  `--base-url`-Modus meldet ein echter Server seine echte `SPACE_PUBLIC_BASE_URL`
  (`https://<node>.ts.net`), nicht `http://127.0.0.1:8765`, unter dem das Skript ihn gerade
  anspricht. Ein Vergleich gegen einen vorberechneten Erwartungswert wäre dort strukturell
  falsch gewesen. Jetzt: Selbstkonsistenz-Prüfung (`resource == f"{issuer}/mcp"`, aus der
  Antwort selbst gelesen) — stärkere Prüfung, gilt in jedem Modus gleich, kein Sonderfall nötig.
  Getestet gegen einen **echten** lokal lauschenden `uvicorn`-Server (`test_
  network_mode_runs_against_a_real_server`, kein `ASGITransport`) — der eigentliche Beweis für
  Punkt 4, nicht nur Argument-Parsing.

**Ein bewusster Rückzieher in dieser Session, dokumentiert statt verschwiegen:** die erste
Advisor-Antwort empfahl, den physischen Verbleib der Unit in `phase3_edge/systemd/` zu belassen
(Begründung: `install_units.sh`s Verzeichnis ist im Skript fest verdrahtet, „nur
Platzhalterliste" schien das zu bestätigen). Beim Lesen von `phase3_edge/tests/test_units.py`
(auf Advisor-Anraten, bevor irgendetwas angefasst wurde) zeigte sich: ein Verbleib hätte
denselben Widerspruch nur verschoben, nicht aufgelöst. Ein zweiter Advisor-Durchlauf mit dem
Fund bestätigte den Umzug als richtig — Details siehe oben. Genau die Art Kurskorrektur, die
dieses Repo für den Menschen sichtbar machen soll, nicht still im Diff verschwinden lassen
(Working-Style-Regel „Widersprechende Evidenz wird ein expliziter Befund").

**Nächster Schritt (konkret):** Das Runbook oben, Schritt 1 (`provision_user.py`) — Sache des
Nikingers. Danach Schritte 2–8 in genau dieser Reihenfolge. `docs/concepts/
P4_ABNAHME_<Datum>.md` erst nach Schritt 7 schreiben (Advisor-Vorgabe: ein Ergebnis-Protokoll
für eine noch nicht gelaufene Matrix wäre ein fabriziertes Protokoll). Schritt 8 (Schnitt,
inklusive `TokenPathASGI`/`AuthModeASGI`-Entfernung) läuft **im selben Commit** wie die
Abnahme, nicht vorgezogen.

## Session stopped — 2026-07-28 (Step 6b)

**Ergebnis:** Step 6b (`oauth_smoke.py`, Logging-Erweiterung, `serve.py`-Gate) abgeschlossen.
`pytest -q` → **331/331 grün** (315 Vorlauf + 16 neue: 6 `test_oauth_smoke.py` + 3 neu in
`test_request_log.py` + 6 neu in `test_logging.py` + 1 neu in `test_asgi_bearer.py`). Reihenfolge
wie in der Kurznotiz der Vorsession festgelegt: `oauth_smoke.py` zuerst, Logging danach,
`serve.py`-Gate zuletzt.

**Alle drei Done-when-Klauseln aus Plan §5 Step 6 jetzt belegt, nicht nur die ersten beiden.**
Advisor-Fund beim Abschluss-Review (siehe unten): `pytest` grün und `oauth_smoke.py` 11/11 waren
da, die dritte Klausel („die sechs Tools verhalten sich unter Bearer-Auth exakt wie unter
Pfad-Token, Diff der Antworten im Session-Block") war unbelegt — `oauth_smoke.py` und Step 6as
`test_bearer_token_reaches_a_real_tool_call` rufen beide nur `list_spaces`. Nachgezogen:
`test_six_tools_behave_identically_under_bearer_and_path_token` (`test_asgi_bearer.py`, ein
Store, ein Space, `mode="both"`, ein Pfad-Token-Principal und eine OAuth-Familie auf demselben
Space). Ergebnis, **qualifiziert statt pauschal** (Plan-Wortlaut "exakt wie" trifft nicht
unbesehen zu):
- **Drei Lese-Tools byte-identisch:** `list_spaces`, `search_items`, `get_item` (eigen **und**
  fremd, inklusive `<untrusted_content>`-Wrap) — beide Aufrufe laufen vor jedem Schreibzugriff
  gegen denselben, unveränderten Store-Zustand.
- **Drei Schreib-Tools identisch bis auf `id`/`created`/`updated`:** `create_item`,
  `update_item`, `append_to_item` erzeugen je Aufruf eine neue Zufalls-ID und einen neuen
  Zeitstempel der echten Systemuhr — das ist Konstruktion, keine Abweichung. Verglichen wird das
  restliche Frontmatter + Body (`_invariant_fields()`-Helfer).
- **Cross-Space-Schreibversuch:** `write_denied` unter beiden Credentials gleich.

**Gebaut:**
- `phase4_auth/scripts/oauth_smoke.py` (neu) — Gegenstück zu `mcp_smoke.py`, treibt den vollen
  Fluss ohne Browser: Discovery → DCR → `GET`/`POST /oauth/authorize` → Code → Token → echter
  Tool-Aufruf mit Bearer → Refresh → Refresh-Replay (`invalid_grant`, Familie tot) → zweite,
  unabhängige Runde nur für den Code-Replay-Nachweis (die erste Familie ist nach dem
  Refresh-Replay bereits tot) → Code-Replay (`invalid_grant`, Familie tot). **11/11 Prüfungen**
  (Plan §6 Abnahmezeilen 10/11: Refresh- **und** Code-Replay, beide über dieses Skript) — Runde 1
  ist in `authorize_get`/`authorize_post` aufgeteilt, Runde 2 bündelt GET+POST+Token-Tausch in
  einer Prüfung (sonst wären es zwölf), dokumentiert im Moduldocstring statt still abweichend.
  Baut `AuthSettings`/die eine Nutzerakte direkt über `passwords.hash_password()`/
  `totp.generate_secret()` — nie `load_users()`/`load_auth_settings()`, TOTP-Seed ist ein echtes,
  umkehrbares Geheimnis (anders als P2/P3s Token-Hashes). `test_oauth_smoke.py` (neu, sechs
  Tests): JSON/Text-Report grün, exakt 11 Prüfungen (Regressionstest gegen die Zählungsentscheidung),
  Refresh-/Code-Replay-Checks existieren namentlich, kein Keyring-/Nutzerakten-Import,
  `test_oauth_log_never_contains_secrets`.
- `mcpserver/request_log.py`: `_ALLOWED_FIELDS` um `stage`/`client_id`/`grant` erweitert (Plan
  §4 wörtlich — erlaubt alle drei, `OAuthLogASGI` füllt aber nur zwei, siehe unten).
  `OAuthLogASGI` (neu, nach dem Vorbild von `AccessLogASGI`): loggt **ausschließlich**
  `/oauth/*` (Discovery/`/health`/`/mcp` bleiben bei `AccessLogASGI`s `ev="http"`, keine
  Doppelprotokollierung derselben Anfrage). `stage` kommt ausschließlich aus Methode+Pfad
  (`_STAGE_BY_ROUTE`), `client_id` ausschließlich aus dem Query-String von `GET
  /oauth/authorize`. **Kein Body-, kein Header-Read** — deshalb bleiben `err`, `grant` und
  `space` aus Plan §4s Beispielzeilen bewusst leer (jedes bräuchte einen Formular-/JSON-Body-
  Read); `token_code`/`token_refresh` kollabieren mangels Body-Zugriff auf `stage="token"`
  (Kompromiss aus der Vorsession, hier umgesetzt). `stage` bleibt ganz weg (nicht `null`) für
  Anfragen unter `/oauth/` ohne passende Route. `ok` ist HTTP-Status-Ebene: ein abgelehntes
  Consent (`action=deny`) loggt `ok=True`, weil die Anfrage selbst korrekt beantwortet wurde —
  wer den *Fluss* beurteilen will, braucht die Redirect-Query, nicht dieses Log.
- `mcpserver/logging_setup.py`: `_TOKEN_SEGMENT_RE` unverändert (Pfad-Redaktion). Neu
  `_SECRET_PATTERNS` (Verteidigung in der Tiefe, praktisch redundant zur Feld-Whitelist/
  `OAuthLogASGI`s Body-Freiheit): `_kv_pattern()`-Helfer deckt sowohl Form-Encoding
  (`password=…`) als auch JSON (`"access_token": "…"`) mit einem Muster ab, plus ein Muster für
  `Authorization: Bearer …`. `TokenScrubbingFilter` benutzt jetzt `_scrub()` (alle Muster) statt
  nur `_TOKEN_SEGMENT_RE`.
- `scripts/serve.py`: `SPACE_AUTH_MODE`-Gate exakt wie in der Vorsession gelockt umgesetzt —
  `"SPACE_AUTH_MODE" in os.environ` entscheidet, ob überhaupt ein `OAuthConfig`-Bündel gebaut
  wird (`load_auth_settings()` **ungefangen**, kein `try/except`); fehlt die Variable bleibt
  `oauth=None`, exakt der P3-Pfad. `AccessLogASGI(OAuthLogASGI(app))` **unbedingt** verdrahtet
  (nicht nur wenn `oauth is not None`) — ohne `/oauth/*`-Routen ist `OAuthLogASGI` ein reiner
  No-op, Dev- und Prod-Pfad bleiben damit strukturell gleich verdrahtet.

**Drei Advisor-Durchläufe — die ersten zwei wie in der Vorsession angewiesen, der dritte beim
Abschluss-Review dieser Session hinzugekommen:**

1. **Vor `OAuthLogASGI`:** bestätigte, dass `err`/`grant`/`space` keinen Test brauchen und
   verworfen werden können (Body-Read wäre die Umkehrung der Regel, die `stage`s Body-Freiheit
   erst sicher macht); korrigierte die Scope-Frage auf `/oauth/*` **ohne** `/.well-known/*`
   (Discovery hat keine Stage im Plan-Enum); `client_id` nur aus dem Query-String von
   `authorize_get`, kein Response-Body-Reader für `/oauth/register`/`/oauth/token`.
2. **Nach der ersten Implementierung:** fand denselben Musterfehler wie in Step 4/5/6a ein
   drittes/viertes Mal — `test_oauth_log_never_contains_secrets` prüfte eine Abwesenheit
   (`secret not in full_text`) ohne zu beweisen, dass `full_text` überhaupt Inhalt hatte; ein
   leerer Logpuffer (z. B. durch entfernte Verdrahtung oder Loggername-Drift) hätte denselben
   Test unbemerkt grün gelassen. Nachgezogen: eine Prüfung, dass alle vier `stage`-Werte aus dem
   echten Lauf tatsächlich im Logpuffer stehen, **bevor** die Abwesenheitsprüfung läuft. Zusätzlich
   gefunden: `stage=None` wurde als `"stage": null` geloggt statt weggelassen (jetzt behoben,
   hält den Feldwert innerhalb von Plan §4s Enum); `_load_oauth_smoke_module()` ließ
   `sys.modules["oauth_smoke"]` nach dem Test stehen (jetzt `try/finally`-bereinigt).
3. **Beim Abschluss-Review, vor dem Commit:** derselbe Musterfehler noch einmal, diesmal auf
   Ebene der ganzen Step-Behauptung statt eines einzelnen Tests — die Session-Notiz „Step 6 ist
   vollständig" stand bereits im Entwurf, bevor die dritte Done-when-Klausel (Bearer-vs-
   Pfad-Token-Diff über alle sechs Tools) überhaupt geprüft war. Nachgezogen:
   `test_six_tools_behave_identically_under_bearer_and_path_token`, siehe oben. Ohne diesen
   Durchlauf wäre die Lücke erst in Step 7 oder später aufgefallen.

**Bewusste Design-Entscheidung, dokumentiert statt Überraschung für einen kalten Leser:**
`test_oauth_log_never_contains_secrets` fängt **bewusst ohne** `TokenScrubbingFilter` im
Aufnahmepfad (ein bloßer `logging.Handler`, gleiches Muster wie
`test_request_log.py::_CapturingHandler`) — der Filter würde ein echtes Leck nachträglich
verdecken. Der Test prüft die **primäre** Sicherung (Feld-Whitelist + `OAuthLogASGI`s Body-/
Header-Freiheit), nicht die Verteidigung in der Tiefe; der Filter selbst ist separat getestet
(`test_logging.py`, sechs neue parametrisierte Fälle für `_SECRET_PATTERNS`).

**Doku-Funde, nicht Teil des Codes:**
- `phase2_mcp/CLAUDE.md`s „Gesamt: 90 Tests"-Zeile war durch diese Session erneut falsch
  geworden (dieselbe Drift-Kategorie wie in Step 6a, jetzt ein zweites Mal in dieser Phase
  gefunden): `test_logging.py` wuchs 2→8, `test_request_log.py` 8→11, `test_asgi_bearer.py`
  13→14 (alle drei P4-Q-Berührungen, nicht auf Plan §5 Step 6s eigener Dateiliste — dieselbe Art
  erwarteten Wachstums wie `oauth_routes()`s dritter Parameter in Step 4/5). Korrigiert im
  selben Commit auf **100 Tests** (`pytest --collect-only -q` je Datei nachgezählt, nicht aus der
  alten Summe hochgerechnet).
- `README.md`s „Lokal ohne Tunnel starten"-Beispiel erwähnte `SPACE_AUTH_MODE` gar nicht — das
  ist korrekt (der Default-Pfad braucht die Variable nicht), aber für einen kalten Leser nicht
  von einer vergessenen Aktualisierung zu unterscheiden. Eine Zeile ergänzt, die das explizit
  macht und auf diesen Head verweist.

**Nächster Schritt (konkret):** Step 6 ist jetzt mit allen drei Done-when-Klauseln belegt;
**Step 7 — Betrieb, Live-Abnahme,
Schnitt** ist der nächste, siehe Plan §5 Step 7 und die Abnahmematrix (16 Zeilen, davon 14 ohne
den Kollegen fahrbar). Kein offener Code-Fund aus Step 6b. `phase4_auth/scripts/authctl.py` und
die Unit-Ergänzungen (`StateDirectory`, `LoadCredentialEncrypted=auth-users`,
`Environment=SPACE_AUTH_MODE=__AUTH_MODE__`/`SPACE_PUBLIC_BASE_URL=__PUBLIC_BASE_URL__`) existieren
noch nicht — erster konkreter Schritt der 7er-Session.

**Bekannte Lücke für Step 7, jetzt schon benannt statt erst dort entdeckt:** `oauth_smoke.py`
läuft heute nur in-process (`ASGITransport`, kein `--base-url`-Schalter). Plan §5 Step 7 Punkt 4
will es gegen `127.0.0.1:8765` fahren, **bevor** irgendjemand einen Connector anfasst — dieser
Netzwerk-Modus fehlt noch und ist bewusst nicht spekulativ in 6b gebaut (nichts, wogegen er in
diesem Step hätte verifiziert werden können). Teil der 7er-Session, nicht vergessen.

## Session stopped — 2026-07-28 (Step 6a)

**Ergebnis:** Step 6a (Resolver + Bearer-Auflösung + `create_app()`-Verdrahtung) abgeschlossen.
`pytest -q` → **315/315 grün** (296 Vorlauf + 19 neue: 6 `test_resolver.py` + 13
`test_asgi_bearer.py`). `test_app.py` separat gelaufen (10/10) und per `git diff --stat`
byte-identisch zum Stand vor diesem Commit bestätigt.

**Gebaut:** `authserver/resolver.py`, `mcpserver/asgi.py` (`BearerAuthASGI`, `AuthModeASGI`,
`_credential_from_path`-Extraktion), `mcpserver/app.py` (`OAuthConfig`, `oauth=None`-Parameter,
root-`TrustedHostMiddleware`). Details + alle additiven Funde in der Modul-Status-Tabelle oben
(Zeile 7a), nicht hier dupliziert.

**Split von Step 6 in 6a/6b, vor der Umsetzung mit dem Advisor abgestimmt:** die volle
Plan-Dateiliste für Step 6 (`resolver.py` + Test, sechs `mcpserver`-Dateien, `oauth_smoke.py`,
`request_log.py`/`logging_setup.py`-Erweiterung, zwei weitere Tests) ist deutlich größer als
jeder vorige Step und enthält mit `oauth_smoke.py` ein zweites Deliverable im Gewand eines
Testhelfers — das Skript ist der Beweis der ganzen Phase (RFC-9700-Replay ohne Browser), nicht
etwas, das nebenbei in einem bereits vollen Commit entsteht. Begründung + Aufteilung: siehe
Modul-Status-Zeile 7a oben.

**Zwei Advisor-Durchläufe, beide fündig, derselbe Musterfehler wie in Step 4/5 — ein Test war
zunächst nur gegen ein Fake bewiesen, nicht gegen den echten Stack:**

1. **Vor der Umsetzung** bestätigte der Advisor den 6a/6b-Split und markierte drei Stellen, an
   denen die Plan-Beschreibung („Guard bekommt einen Authorization-Header-Vergleich") vermutlich
   nicht mehr zum real gebauten `context.py` (state-basiert seit P2 Step 4, siehe dortige
   Abweichungsnotiz) passt — mit der Anweisung, das zu verifizieren statt blind zu übernehmen.
2. **Nach der ersten Implementierung** fand ein zweiter Durchlauf, dass genau diese Verifikation
   nur gegen Fakes lief: `test_valid_bearer_sets_principal_space` prüft einen Hash-Vergleich in
   einer Fake-Inner-App, `test_guard_rejects_principal_from_other_request` monkeypatcht
   `get_http_request` auf ein handgebautes Fake-Objekt — keiner der beiden lässt ein echtes
   Bearer-Token durch die echte FastMCP-App bis zu `tools.py`s echtem Guard-Aufruf laufen.
   Nachgezogen: `test_bearer_token_reaches_a_real_tool_call` (voller Stack, echtes
   `list_spaces`-Ergebnis). Zusätzlich fehlte jede Instanziierung von `TrustedHostMiddleware` —
   die einzige bisherige Integrationsprobe hatte `allowed_hosts=()`, die Bedingung griff nie.
   Nachgezogen: `test_trusted_host_middleware_protects_root_app_when_configured` (erlaubter vs.
   fremder Host, `/health` bleibt erreichbar).

**Lehre, dieselbe wie am Ende von Step 5, jetzt ein drittes Mal bestätigt:** eine Behauptung über
unveränderten/korrekten Code ("`context.py` braucht keine Änderung") ist erst ein Fund, wenn ein
Test sie gegen den echten Aufrufpfad beweist — ein Test gegen ein Fake beweist nur, dass das Fake
tut, was erwartet wird.

**Doku-Fund, nicht Teil des Codes:** `phase2_mcp/CLAUDE.md`s Testzahl-Zeile stand auf 57 und war
bereits vor dieser Session falsch (fehlendes `test_request_log.py`, mehrere stumm gewachsene
Einzelzahlen) — dieselbe Drift-Kategorie wie die root-`CLAUDE.md`-Korrektur aus Step 5, diesmal
in einer bereits **abgeschlossenen** Phase gefunden, weil P4 Step 6a eine ihrer Dateien anfasst.
Korrigiert im selben Commit, siehe dortige datierte Korrekturnotiz — die historischen
Modul-Status-Zeilen von P2 selbst bleiben unangetastet.

**Nächster Schritt (konkret):** Step 6b — `mcpserver/request_log.py` (`ev="oauth"`, Felder
`stage`/`client_id`/`grant`, `OAuthLogASGI` als neuer ASGI-Wrapper nach dem Vorbild von
`AccessLogASGI`: **außerhalb** von `create_app()`, in `scripts/serve.py`, damit `test_app.py`
weiterhin unverändert läuft — Begründung identisch zu `AccessLogASGI`s eigener Platzierung),
`mcpserver/logging_setup.py` (`_SECRET_PATTERNS`-Satz erweitert um `code=`, `access_token`,
`refresh_token`, `password`, `totp`, `Authorization: Bearer …`), `phase4_auth/scripts/
oauth_smoke.py` (Gegenstück zu `space_cli.py`/`mcp_smoke.py`: Discovery → DCR → `/authorize` →
Formular-POST mit Passwort + errechnetem TOTP → Code → Token → `tools/call` mit Bearer → Refresh
→ Reuse mit dem alten Refresh-Token, muss `invalid_grant` liefern und die Familie töten),
`scripts/serve.py`-Verdrahtung (liest `SPACE_AUTH_MODE`, baut bei `oauth`/`both` `AuthSettings` +
`AuthStore` + `load_users()` und reicht sie als `OAuthConfig` an `create_app()`).
**Entscheidungspunkt vor dem Schreiben — gelockt (Nikinger, 2026-07-28, vor der 6b-Session):**
zwei unabhängige Weichen, nicht eine. (1) Ob `serve.py` überhaupt ein `OAuthConfig`-Bündel baut
(`AuthSettings`/`AuthStore`/`load_users()`) — das entscheidet, ob der P3-Dev-Pfad ohne jede neue
Env-Var weiterläuft. (2) `SPACE_AUTH_MODE` selbst (`token`/`both`/`oauth`, Default `oauth`),
die einzig steuert, wie `AuthModeASGI` `/mcp` bedient, **sobald** das Bündel existiert.
`load_auth_settings()` regelt (2) bereits korrekt und laut — fehlendes `SPACE_PUBLIC_BASE_URL`
in `oauth`/`both` wirft, das ist gewollt (gleiches Fail-Closed-Muster wie `SPACE_DATA_ROOT`).
Die Lücke lag ausschließlich bei (1): ein unbedingter `load_auth_settings()`-Aufruf zwänge auch
einen lokalen Lauf ohne jede Absicht, P4 zu testen, durch (2)s Validierung.

**Entscheidung:** `serve.py` prüft die **rohe Env-Var-Anwesenheit** `"SPACE_AUTH_MODE" in
os.environ` — nicht den bereits gedefaulteten Rückgabewert von `load_auth_settings()` — als
alleinige Weiche für (1). Fehlt sie: `oauth=None`, exakt der heutige P3-Pfad, keine neue
Anforderung. Ist sie gesetzt (jeder der drei Werte): `load_auth_settings()` läuft echt, Bündel
wird gebaut, ein Konfigurationsfehler stirbt laut — kein `try/except` um den Aufruf, das wäre
ein stiller Fallback auf schwächere Auth genau dort, wo P4 das verhindern soll. Sicher für den
echten Produktionspfad: die Step-7-Unit-Vorlage setzt `Environment=SPACE_AUTH_MODE=
__AUTH_MODE__` ohnehin immer explizit — die Weiche ist kein neuer Sonderfall, sie spiegelt nur,
wie die Unit bereits geplant war. Plan §4/§5 Step 6, Dateiliste dort. Zwei verbleibende benannte Tests: `test_oauth_log_never_contains_
secrets` (treibt über `oauth_smoke.py`, Markerwerte `ZZZ-PASSWORD`/`ZZZ-CODE`, prüft den ganzen
Logpuffer), `test_oauth_events_carry_stage_and_duration`. **`OAuthLogASGI`s `stage`-Ableitung
darf keinen Request-Body lesen** (der trägt `code_verifier`/`refresh_token`) — Methode+Pfad
reichen für `register`/`authorize_get`/`authorize_post`/`token_code`-oder-`token_refresh`; wenn
sich `token_code` und `token_refresh` ohne Body-Zugriff nicht unterscheiden lassen, ist
`stage="token"` (ohne die Grant-Unterscheidung) der akzeptierte Kompromiss, dokumentiert statt
stillschweigend gelöst (Advisor-Vorgabe dieser Session). Step 6b Done-when (Plan): `pytest`
grün, `oauth_smoke.py` 11/11, die sechs Tools verhalten sich unter Bearer-Auth exakt wie unter
Pfad-Token (Antwort-Diff im Session-Block).

**Kurznotiz für die 6b-Session:** `serve.py`-Gate ist bereits gelockt (siehe Entscheidungspunkt
oben) — nicht neu entscheiden, nur umsetzen (`"SPACE_AUTH_MODE" in os.environ` als alleinige
Weiche fürs Bündel, `load_auth_settings()` sonst wie gehabt laut scheitern lassen). Zwei
Dateien anfassen, die nicht in der Step-6-Liste stehen, aber betroffen sein könnten:
`README.md`/`phase3_edge/CLAUDE.md`, falls das Runbook „lokal starten" den Fall ohne
`SPACE_AUTH_MODE` erwähnt — kurz gegenprüfen, ob dort eine Zeile nachgezogen werden muss.
`oauth_smoke.py` zuerst schreiben (es ist der Beweis, nicht ein Nebenprodukt), Logging danach.
Advisor **vor** dem Schreiben von `OAuthLogASGI` fragen (die Body-Lesen-vs-`stage`-Genauigkeit
ist ein echter Kompromiss, siehe oben) und **nach** der ersten Implementierung — beide Male hat
das in Step 5 und 6a echte Funde gebracht, nicht nur in Step 5. Vor jeder neuen Testdatei
`find . -name "test_<name>.py"` gegen den ganzen Baum prüfen (Kollisionsregel aus Step 3, gilt
weiter). `test_app.py` nach der `serve.py`-Änderung separat laufen lassen und `git diff --stat`
dagegen prüfen — bleibt es unverändert, ist das Gate richtig gebaut.

## Session stopped — 2026-07-28 (Step 5)

**Ergebnis:** Step 5 (Autorisierungsfluss) abgeschlossen. `pytest -q` → **296/296 grün** (260
Vorlauf + 36 neue: 22 `test_flows.py` + 9 `test_routes.py` + 4 `test_templates.py` + 1 neu in
`test_totp.py`).

**Gebaut:** `flows.py` (`start_authorize`, `submit_consent`, `issue_token` — frei von jedem
HTTP-Framework-Import, kleine eingefrorene Ergebnis-Typen statt Starlette-`Response`),
`templates.py` (Wegwerf-UI, kein JS/CSS-Build/Cookie), `routes.py` vervollständigt um
`GET`/`POST /oauth/authorize` und `POST /oauth/token`. Details + alle additiven Abweichungen
(`store.now()`, `get_totp_counter`/`set_totp_counter`, `totp.verify()`-Härtung, `oauth_routes()`-
dritter-Parameter, `_token_headers()`, `error_description`, `redirect_uri_allowed()` jetzt auch
in `start_authorize`, POST-Fehlerseite statt erneutem Formular, Enumerationsschutz-Timing-
Begründung) in der Modul-Status-Tabelle oben (Zeile 6), nicht hier dupliziert.

**Zwei Advisor-Durchläufe (vor und nach der Implementierung), beide fündig:**

*Vor der Implementierung* bestätigte der Advisor den Grundriss (kleine Ergebnis-Typen statt
Starlette-Responses in `flows.py`) und benannte drei Lücken gegenüber der reinen Dateiliste, die
alle blockierend waren: fehlende `totp_replay`-Zugriffsmethoden im Store, der noch nicht
gebaute dritte `oauth_routes()`-Parameter (inkl. der beiden bestehenden Fixtures, die dadurch
brechen würden), und das fehlende `Pragma: no-cache` auf der Token-Antwort. Außerdem die
Timing-Analyse zum Enumerationsschutz (Argon2id dominiert TOTP, das Weglassen von `totp.verify()`
für einen unbekannten Space ist deshalb kein Orakel) und der Hinweis, den TOTP-Zähler erst nach
vollständigem Erfolg hochzusetzen, nicht schon bei richtigem TOTP mit falschem Passwort.

*Nach der Implementierung* fand ein zweiter Durchlauf vier weitere Lücken, obwohl alle 20 im
Plan benannten Tests bereits grün liefen — die Prüfung war "alle benannten Tests bestehen",
nicht "jeder Fehlerpfad aus §2.4 hat genau einen Test" (das eigentliche Plan-Done-when):

1. **Ein Test war grün aus dem falschen Grund.** `test_all_token_errors_use_invalid_grant` baute
   drei Codes vorab in einer Liste, die Uhr rückte dabei kumulativ vor — der zweite Code traf
   exakt auf seine eigene `expires_at`-Grenze (`code_ttl_s=60`, Uhr bei Verwendung genau +60s
   seit Ausstellung) und schlug über "abgelaufen" fehl, nicht über den geprüften Client-ID-
   Mismatch. Behoben: jeder Fall stellt seinen Code unmittelbar vor seinem eigenen
   `pytest.raises`-Block aus, nicht vorab. Dieselbe Reihenfolge-Lehre wie Step 4
   (`test_register_requires_json_content_type`), jetzt zum zweiten Mal real eingetreten.
2. **Kein Test für TOTP-Replay** — der Fehlerpfad aus Plan §2.4 POST-Schritt 6 hatte keine
   Abdeckung, und die neuen Store-Methoden `get_totp_counter`/`set_totp_counter` liefen nur in
   der Richtung, die den Schutz umgeht (`_issue_code` rückt die Uhr bewusst vor, damit
   aufeinanderfolgende Logins in einem Test nicht kollidieren). Nachgezogen:
   `test_totp_replay_is_rejected_without_burning_the_stored_counter`.
3. **Kein `invalid_scope`-Test** — Plan §2.4 GET-Schritt 3 nennt ihn, `start_authorize`
   implementiert ihn, nichts prüfte ihn. Nachgezogen:
   `test_authorize_rejects_scope_outside_allowlist`.
4. Zwei günstige Ergänzungen ebenfalls nachgezogen: `iss` auf dem Erfolgs-Redirect war nur beim
   Fehlerfall geprüft (`test_authorize_success_redirect_carries_iss`), und die neue
   Nie-wirft-Härtung von `totp.verify()` selbst hatte keinen Test
   (`test_verify_never_raises_on_malformed_secret_or_unknown_algo` in `test_totp.py`).

**Lehre für künftige Steps:** "alle im Plan benannten Tests sind grün" ist eine schwächere Prüfung
als "jeder Fehlerpfad hat genau einen Test" — ein Test kann aus einem anderen als dem
beabsichtigten Grund grün sein (Fund 1), oder ein im Plan nur in Prosa erwähnter Fehlerpfad kann
ganz ohne Test bleiben (Funde 2–3), ohne dass die benannte Testliste das anzeigt.

**Root-`CLAUDE.md`-Drift geschlossen:** die letzte Aktualisierung dort (Commit `766bf53`) blieb
bei Step 1 stehen — Step 2, Step 3 und Step 4 hatten das „Current state"-Kapitel nicht
nachgezogen, drei Steps stumm stale (dieselbe Kategorie Fund wie die Korrektur in `766bf53`
selbst). In diesem Commit mitgezogen, siehe dortige datierte Korrekturnotiz.

**Nächster Schritt (konkret):** Step 6 — Anbindung an den Resource Server (`mcpserver/asgi.py`,
`mcpserver/context.py`, `mcpserver/app.py`, Plan §3/§5 Step 6). `oauth_routes()` trägt bereits
den vollen Drei-Parameter-Anker (`auth_settings, auth_store, users`) — Step 6 muss ihn nur noch
aus `create_app()` heraus mit echten `load_users()`-Daten aufrufen, nichts an der Signatur ändern.
`AuthModeASGI` ersetzt `TokenPathASGI` unter `Mount("/mcp", ...)`; `assert_principal_matches_
request()` bekommt den `Authorization`-Header-Vergleich zusätzlich zum bestehenden Pfadsegment-
Vergleich (P4-Q: `mcpserver/context.py`/`app.py`/`asgi.py` gehören zur erlaubten
Berührungsfläche, `tools.py`/`permissions.py`/`auth.py` nicht). Plan §3.3 pinnt zusätzlich die
Form der `create_app()`-Erweiterung selbst: genau **ein** optionaler Parameter `oauth=None` —
fehlt er, verhält sich `create_app` exakt wie in P3, damit die bestehenden `test_app.py`-Tests
unverändert gültig bleiben (Bedingung dafür, dass ein Testfehler in P4 auch nachweisbar aus P4
stammt, nicht aus einer stillen Signaturverschiebung). Nicht drei separate Parameter
(`auth_settings`/`auth_store`/`users`) einzeln in `create_app` durchreichen. Das ist der Step,
der den Plan-Umbau erstmals gegen den echten `mcpserver` verdrahtet — bisher lief alles
ausschließlich innerhalb von `authserver`.

---

## Session stopped — 2026-07-28 (V14 + Step 4)

**Ergebnis:** `[VERIFY]` V14 abgeschlossen, Step 4 (Metadaten und dynamische Registrierung)
abgeschlossen. `pytest -q` → **260/260 grün** (244 Vorlauf + 16 neue).

**V14, vor Step 4 verlangt:** Web-Recherche gegen die aktuelle Anthropic-Connector-Doku
bestätigte 13 von 14 Plan-Annahmen aus §0.6 wortgleich. Eine Ausnahme: native/Loopback-Clients
(Claude Code) sind inzwischen dokumentiertes Anthropic-Verhalten, nicht mehr nur eine
Erweiterungs-Idee — Details, Nikinger-Entscheidung (draußen lassen) und der dokumentierte
einfachere Weg für später stehen im Scope-Abschnitt oben, nicht hier dupliziert.

**Step 4:** `metadata.py`, `clients.py`, erste Hälfte `routes.py` gebaut — Details in der
Modul-Status-Tabelle oben (Zeile 5) inkl. aller additiven Abweichungen (`DCRError`,
`increment_register_window`, `starlette`-Deklaration, `oauth_routes()`-Signaturwachstum,
Content-Type-vor-Bremse-Reihenfolge). Nicht dort erwähnt, weil es kein Feature-Delta ist,
sondern ein Doku-Integritäts-Fund: **`test_authserver_does_not_import_mcpserver` existierte
nicht**, obwohl die Harte-Regeln-Zeile P4-A/P4-C sie seit Step 1 namentlich als Beleg zitiert
("Test: `test_authserver_does_not_import_mcpserver`"). Vier Steps lang unbelegt, jetzt in
`test_authserver_config.py` geschlossen. Lehre: eine im Fließtext genannte Testfunktion ist erst
ein Beleg, wenn `pytest --collect-only` sie auch findet — nicht wenn der Name plausibel klingt.
Wer diese Tabelle künftig liest, sollte die anderen dort zitierten Testnamen bei Gelegenheit
stichprobenartig gegen den echten Testbaum prüfen, nicht blind vertrauen.

**Advisor-Reviews dieser Session (zwei, vor und nach der Implementierung):** vor dem Schreiben
bestätigte der Advisor die fünf offenen Designfragen (DCR-Fehlercode-Trennung,
Security-Header-Umfang, Middleware- vs. Handler-Header, `starlette`-Pin-Politik,
`register_attempts`-Modulzugehörigkeit) und flaggte zusätzlich ein ungetestetes Risiko:
Starlette 1.3.1 liegt weit jenseits dessen, was `phase2_mcp` bereits benutzt
(`BaseHTTPMiddleware`, `await request.json()`, benutzerdefinierte Header auf Nicht-200-Antworten
— keins davon im Repo vorher geprüft). Eine Wegwerf-Probe (`httpx.ASGITransport` gegen eine
Zwei-Routen-Spielzeug-App mit Header-Middleware) lief vor jeder echten Implementierung grün —
API-Kompatibilität war damit belegt, nicht angenommen. Nach der Implementierung fand ein zweiter
Advisor-Durchlauf eine echte Lücke: `test_register_requires_json_content_type` allein hätte auch
bei vertauschter Prüfreihenfolge (Bremse vor Content-Type) grün bleiben können — die
Reihenfolge-Entscheidung war getroffen, aber nicht gepinnt. Nachgezogen:
`test_register_rejected_content_type_does_not_consume_rate_limit`.

**Design-Entscheidung, dokumentiert:** Security-Header direkt in den `routes.py`-Handlern statt
über eine Starlette-`Middleware`. Grund: `oauth_routes()` liefert eine flache Routenliste, die
der Wurzel-App **vorangestellt** wird (Plan §3.3), kein eigenes `Mount`/Sub-App — eine app-weite
Middleware in der Wurzel-App träfe auch `/health` und `/mcp`, ein zweites pfadgebundenes Mounten
sieht der Plan an dieser Stelle nicht vor. Vollständiges Set (CSP, Referrer-Policy,
X-Content-Type-Options, X-Frame-Options, Cache-Control, ggf. HSTS) auf beiden
Metadatendokumenten; nur `Cache-Control: no-store` auf `/oauth/register` (Plan §2.6: die
Cache-Control-Zeile überschreibt ihren eigenen Tabellenkopf ausdrücklich mit "auf allen
OAuth-Antworten").

**Nächster Schritt (konkret):** Step 5 — Autorisierungsfluss (`authserver/{flows,templates}.py`,
`routes.py` vervollständigt um `/oauth/authorize` und `/oauth/token`, `test_flows.py`,
`test_routes.py`, `test_templates.py`). Plan §2.4/§5 Step 5. `oauth_routes()` bekommt dabei
voraussichtlich den dritten Parameter `users` (siehe Abweichungsnotiz oben). Die beiden
wichtigsten Tests des Steps laut Plan: ein Fehler vor Prüfung von `client_id`/`redirect_uri`
darf **nie** zu einer Umleitung führen (`test_authorize_rejects_unknown_client_without_redirect`,
`test_authorize_rejects_unregistered_redirect_uri_without_redirect`).

---

## Session stopped — 2026-07-28 (Step 3)

**Ergebnis:** Step 3 (Persistenz und Bremse) abgeschlossen. `pytest -q` → **244/244 grün**
(225 Vorlauf + 19 neue: 14 `test_authserver_store.py` + 5 `test_ratelimit.py`).

**Advisor-Review vor der Implementierung** (Hard Rule aus dem Session-Auftrag: Advisor vor
substanzieller Arbeit) fand einen echten Absturzmodus im ursprünglichen Entwurf: `rotate_refresh`
sollte die neue Access-Token-Laufzeit aus der jüngsten `access_tokens`-Zeile der Familie ableiten.
Nach einem `purge_expired()`-Lauf (auch über `authctl.py purge-expired`, Plan §1.2) existiert
diese Zeile bei einem Client, der erst nach Ablauf des Access-Tokens (60 min) aber innerhalb der
Refresh-Gültigkeit (30 d) rotiert, nicht mehr — kein Randfall, der Normalpfad einer langlebigen
Session. Behoben, bevor Code geschrieben wurde: `rotate_refresh` nimmt jetzt `access_ttl_s`/
`refresh_ttl_s` explizit entgegen (siehe Abweichungsnotiz unten). Regressionstest:
`test_rotate_refresh_after_access_token_purged`.

**Abweichungen vom Plan-Methodenskelett** (dokumentiert, nicht still übernommen — Plan-Kopf
warnt selbst, dass er ohne frischen Repo-Zugriff geschrieben wurde):
- **`create_family`** — nicht in der Plan-"fix"-Liste, aber durch die FK
  `auth_codes.family_id` erzwungen: eine `token_families`-Zeile muss existieren, bevor
  `issue_code` einen Code an sie binden kann (Plan §2.4 POST /oauth/authorize Schritt 8 nennt
  zwei Schritte — Familie anlegen, dann Code erzeugen — für die es zwei Store-Aufrufe braucht).
- **`rotate_refresh(refresh_token, *, access_ttl_s, refresh_ttl_s)`** statt nur
  `refresh_token` — siehe Advisor-Fund oben. Kleinere Drift als der Absturzmodus einer
  Bestands-Ableitung.
- **`get_login_attempt`/`upsert_login_attempt`/`clear_login_attempt`** — nicht in der
  Plan-"fix"-Liste, aber notwendig, weil `ratelimit.py` selbst kein SQL führen darf (Step-3-Regel:
  SQL nur in `store.py`) und `login_attempts` sonst nirgends anfassbar wäre.
- **Eskalationsformel in `ratelimit.py` selbst festgelegt** — der Plan gibt nur die vier
  Konstanten vor (`MAX_FAILURES=5`, `WINDOW_S=900`, `BASE_LOCKOUT_S=900`, `MAX_LOCKOUT_S=86400`),
  keine Formel. Gewählt: `failures` zählt monoton, bei jedem Vielfachen von `MAX_FAILURES` eine
  neue Sperre mit `BASE_LOCKOUT_S * 2**(n-1)` (gedeckelt bei `MAX_LOCKOUT_S`), `WINDOW_S`-Vergessen
  nur solange `locked_until IS NULL` (also bevor es je zu einer Sperre kam) — danach bleibt das
  Fenster für den Space bewusst tot bis zu einem erfolgreichen Login (`reset()`). Grund: die
  erste Sperrdauer (900 s) liegt in derselben Größenordnung wie `WINDOW_S`; ein Fenster-Reset
  nach Sperrablauf würde die Eskalation bei jedem erneuten Versuch auf Stufe 1 zurückwerfen.
  Dokumentiert im Docstring von `ratelimit.py`, hier verlinkt statt dupliziert.
- **`CREATE TABLE`/`CREATE INDEX ... IF NOT EXISTS`** statt der Plan-Rohform — macht
  `initialise()` und damit `test_reopen_is_idempotent` erst korrekt (Reconnect auf denselben
  Pfad darf nicht auf bereits existierenden Tabellen scheitern).
- **Testdatei `test_authserver_store.py`, nicht `test_store.py`** — dieselbe Namenskollision
  wie in Step 1 bei `test_authserver_config.py`, diesmal mit `phase1_storage/tests/test_store.py`
  (kein gemeinsames Elternpaket, kein `--import-mode=importlib`). Kollidierte real beim ersten
  vollen `pytest -q`-Lauf dieser Session (`import file mismatch`), nicht nur theoretisch — siehe
  Fund unten.

**SQL-Containment-Grep** (Step-3-Done-when, `authserver/` + `phase4_auth/scripts/`):
```
$ grep -rniE "SELECT |INSERT INTO|UPDATE .* SET|DELETE FROM|CREATE TABLE|CREATE INDEX|PRAGMA |executescript|conn\.execute|\.execute\(" phase4_auth/authserver phase4_auth/scripts --include="*.py" -l
phase4_auth/authserver/store.py
```
Einziger Treffer — kein SQL außerhalb `store.py`.

**Fund während der Arbeit, behoben:** erster `pytest -q`-Gesamtlauf brach mit `import file
mismatch` ab (`phase4_auth/tests/test_store.py` vs. bereits importiertes
`phase1_storage/tests/test_store.py`) — exakt die Namenskollisionsklasse, vor der die
Special-Task-Notiz zu Beginn dieser Session warnte (dort für `test_config.py`/`tests/__init__.py`
aus Step 1 dokumentiert). Behoben durch Umbenennung auf `test_authserver_store.py`, dazu
`__pycache__` in allen `tests/`-Verzeichnissen gelöscht (stand noch vom vorherigen Lauf).
Nicht: die Plan-Dateinamen zurück auf `test_store.py` erzwingen — das war exakt die Warnung.

**`test_no_plaintext_secret_in_database`:** treibt den vollen Fluss (Auth-Request, Code, Token,
Rotation) mit echten erzeugten Geheimnissen, liest `auth.sqlite3` **und** `auth.sqlite3-wal`
(WAL-Modus — das Geheimnis kann im WAL-File statt im Hauptfile stehen), prüft Abwesenheit der
vier Klartext-Geheimnisse (`request_id`, `code`, `access_token`, `refresh_token`) **und**
Anwesenheit mindestens eines `sha256`-Hex-Hashes — eine reine Abwesenheitsprüfung wäre auch bei
einem still no-op-gebliebenen Fluss grün gelaufen (Advisor-Hinweis).

**Nächster Schritt (konkret):** Step 4 — Metadaten und dynamische Registrierung
(`authserver/{metadata,clients}.py`, erste Hälfte von `routes.py`, `test_metadata.py`,
`test_clients.py`). PRM/AS-Metadatendokumente (RFC 9728/8414), DCR (RFC 7591),
Redirect-Origin-Allowlist inkl. `[SEAM]`-Funktion `redirect_uri_allowed` (Plan §2.2/§2.6, §5
Step 4). Vor Beginn: `[VERIFY]` V14 — die Anthropic-Auth-Doku einmal gegenlesen, sie ist laut
Plan die einzige Quelle, die sich ohne Vorwarnung ändert.

---

## Session stopped — 2026-07-28 (Step 0 + Step 1 + Step 2)

**Ergebnis:** Step 0 (Haushalt, Drift, geerbte Abnahme), Step 1 (Gerüst, Konfiguration,
Kryptobausteine) und Step 2 (Passwörter, TOTP, Nutzerakten) abgeschlossen. `pytest -q` →
**225/225 grün** (168 P1+P2+P3 + 57 neue P4-Tests: 20 Step 1 + 37 Step 2).

**Kritischer Fund, geschlossen:** `export_space_map.py` zeigte zu Sessionbeginn drei aktive
Spaces (`fabian`, `niklas`, `nikinger`) statt der erwarteten zwei — ein Keyring-Token aus P2
Step 3, nie widerrufen trotz der B2-Umbenennung `nikinger/` → `niklas/`. Live und schreibfähig
(`Store.create()` legt Zielverzeichnisse automatisch an), aber dormant (`nikinger/` existierte
nicht mehr unter `DATA_ROOT`). Nikinger-Entscheidung: widerrufen. Ausgeführt in zwei Schritten,
beide live bestätigt: Keyring-Widerruf (`issue_token.py --revoke nikinger`), danach Export +
`sudo systemctl restart sharefyx-mcp` (2026-07-28 14:12:49) — `diagnose.sh` danach komplett
grün, `export_space_map.py` zeigt wieder exakt zwei Spaces. Vollständige Zeitachse:
`docs/concepts/PHASE3_CLOSEOUT_HANDOVER.md` §5 Nachträge. Nebeneffekt: die Handover-eigene
„Korrektur" von Fund 1 (die Behauptung, „alle drei Token rotiert" sei Drift und real seien es
zwei gewesen) war selbst falsch — zum Zeitpunkt der Prüfung existierten tatsächlich drei aktive
Spaces.

**Autocompact-Drift aus dem P3-Handover (§5) behoben:** README.md voll auf P3-Stand gezogen
(Cloudflare-Diagramm, Phasennummern OAuth/Web-UI, Tokenbeispiel), ROADMAP.md (Cloudflare →
Tailscale Funnel, `LoadCredential` → `LoadCredentialEncrypted`, P4-Paketname `auth` →
`authserver` per P4-B), Root-`CLAUDE.md` (R3-Ergänzung analog R4, Kollege-Prozess-Frage als in
P3-G entschieden markiert, „Aktive Phase" auf P4 gesetzt), `phase3_edge/CLAUDE.md`
(Tailscale-Installationsstatus, V13 geschlossen).

**Geerbte P3-Abnahme:** Zeile 12 (Backup-Timer) durch `systemctl list-timers` bestätigt (echter
Lauf 2026-07-28 00:00:50). Zeile 6 (Reboot) bleibt bewusst passiv offen. Zeile 13
(Restore-Nachweis) bewusst **nicht** nachgeholt — braucht ein frisches Bundle, kein Lauf
während ungeklärtem Credential-Zustand (war zum Prüfzeitpunkt ohnehin gegeben).

**Environment-Inventar (Step 0, `[VERIFY]` aufgelöst):** systemd 255 (≥235 für
`StateDirectory=`), NTP synchronisiert (`yes`), `argon2-cffi` aktuell `25.1.0` (P4-R-Pin),
`fastmcp` stabil weiterhin `3.4.5`/installiert `3.4.4` — **kein** stabiles 4.x, nur eine Alpha
`4.0.0a2` (`pip index versions --pre`). Der Plan-Befund „FastMCP 4 spricht die neue Revision,
P3-E-Trigger gefallen" ist damit nur zur Hälfte richtig — eine Alpha ist kein Release. Notiert,
keine Aktion (V25: nur beobachten).

**Step 1:** `authserver/{config,models,crypto,errors}.py` gebaut, `phase4_auth/pyproject.toml`
(Paket `authserver`, `argon2-cffi==25.1.0` exakt), `pytest.ini` um `phase4_auth/tests` erweitert,
`.gitignore` um `*.sqlite3` erweitert (V21). Abweichung vom Plan bei der Testdatei-Benennung
(siehe Modul-Status oben) — Ursache Namenskollisionen mit bestehenden `tests`-Verzeichnissen,
nicht antizipierbar ohne Repo-Zugriff (der Plan wurde ohne diesen geschrieben, siehe Plan-Kopf).

**Step 2:** `passwords.py` (Argon2id über `argon2-cffi`, `verify_password` wirft nie —
`InvalidHashError` erbt von `ValueError`, nicht von `Argon2Error`, ein Test
(`test_verify_returns_false_on_garbage_hash`) deckte das sofort auf, `DUMMY_HASH` für den
Enumerationsschutz), `totp.py` (RFC 6238 über RFC 4226, stdlib, alle 15 Appendix-B-Vektoren
SHA1/SHA256/SHA512 grün, Replay-Schutz über injizierten `last_counter`), `users.py` (spiegelt
`credentials.py :: load_space_map()` bewusst — Credentials-Verzeichnis zuerst, Keyring-Fallback,
`warning` bei fehlender Datei, Ausnahme bei kaputtem Inhalt). `provision_user.py`/
`export_auth_users.py` nach `issue_token.py`/`export_space_map.py`-Muster, gegen Fake-Keyring
+ injizierten `get_password` getestet — **nicht** gegen den echten Keyring ausgeführt, gleiche
Grenze wie bei P2 Step 3s `--space nikinger`-Roundtrip (Sache des Nikingers, nicht Claude Codes).

**`[VERIFY]` V17, gemessen (nicht geraten):** Argon2id mit den Plan-Default-Parametern
(`t=2, m=19456, p=1`) maß auf dieser VM **~15 ms** je Durchlauf — deutlich unter dem
Zielkorridor 50–250 ms. Nach Plan-Vorgabe `t` erhöht: `t=8` misst **~53 ms** (`m`/`p`
unverändert), fünf Läufe, Werte im Session-Log oben unter „Step 2" nachvollziehbar. Konstante
in `passwords.py` dokumentiert den gemessenen statt einen geratenen Wert.

**Nächster Schritt (konkret):** Step 3 — Persistenz und Bremse (`authserver/{store,
ratelimit}.py`, `test_store.py`, `test_ratelimit.py`). Schema aus Plan §2.3, `AuthStore`
kapselt **jede** SQL-Anweisung (kein SQL außerhalb dieses Moduls, per Grep im Session-Block zu
belegen), `now_fn` injiziert. Der Kern der Phase — Code-Replay/Refresh-Replay-Tötungsregeln
(RFC 9700) sind hier, nicht später.

---

