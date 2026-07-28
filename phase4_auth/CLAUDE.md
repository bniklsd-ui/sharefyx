---
status: live
purpose: Phase-Head OAuth 2.1 + DCR — Scope, harte Regeln, Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase4_auth/ oder an den in P4-Q genannten Dateien in phase2_mcp/mcpserver — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase4_auth_plan.md          # voller Plan, Entscheidungen P4-A–P4-R, Steps 0–7
  - ../docs/concepts/PHASE3_CLOSEOUT_HANDOVER.md  # Herkunft der offenen Entscheidungen, Doku-Drift, [VERIFY]-Bilanz
  - SESSIONS_ARCHIVE.md                            # ältere Session-Blöcke, newest-first
updated: 2026-07-28
---

# CLAUDE.md — Phase 4: OAuth 2.1 + DCR (`phase4_auth/`)

> **Der Pfad-Token verschwindet.** Ein eigener, handgeschriebener Authorization Server im selben
> Prozess ersetzt ihn — Discovery, Dynamic Client Registration, PKCE, Argon2id + TOTP, opake
> rotierende Token. Kein Upstream-IdP, kein `auth=`-Parameter an `FastMCP`.
> **Quelle der Wahrheit ist der Code, nicht dieses Dokument.**
> Vollständiges Design + alle 18 gelockten Entscheidungen (P4-A–P4-R) + Steps 0–7:
> `../docs/concepts/phase4_auth_plan.md`.

## Mission (zuerst lesen)

Der eigentliche Härtetest der Phase ist nicht der erste erfolgreiche Login, sondern der erste
erfolgreiche **Fehlschlag**: ein wiederverwendeter Refresh-Token muss die ganze Token-Familie
töten, ein zweimal eingelöster Authorization-Code muss die daraus entstandenen Token widerrufen,
und ein falsches Passwort darf nicht verraten, ob das Konto existiert. Diese drei Fälle sind
Akzeptanzkriterien, keine Kür (Plan §0.1).

## Bauprinzip (Projekt-Kernprinzip)

„Der Server ist dumm." **Phase 4 enthält KEINE AI, keine neuen Tools, keine Fachlogik.** Wer
hier `tools.py` anfasst, ist in der falschen Phase (P4-Q).

## Scope (Kurzform, Details: Plan §0.3/§0.7 P4-A–P4-R)

- **DRIN:** Protected Resource Metadata (RFC 9728), Authorization Server (RFC 8414), Dynamic
  Client Registration (RFC 7591), PKCE `S256` (RFC 7636), Token-Rotation + Familien-Widerruf
  (RFC 9700), `iss` im Authorization Response (RFC 9207), Argon2id-Passwörter, TOTP (RFC 6238)
  als zweiter Faktor, befristeter Parallelbetrieb `SPACE_AUTH_MODE=both`.
- **DRAUSSEN:** REST/UI (P5), MCP-Revision 2026-07-28, `fastmcp` 4, D6, neue Tools,
  feingranulare Lese-Rechte, Off-site-Backup, Monitoring, `/oauth/revoke`, `/oauth/introspect`,
  Recovery-Codes für den zweiten Faktor, CIMD (Seam vorhanden, siehe Plan §2.6 `[SEAM]`).

**[2026-07-28 Nachtrag, `[VERIFY]` V14 vor Step 4]:** Web-Recherche gegen die aktuelle
Anthropic-Doku (`claude.com/docs/connectors/building/{authentication,lazy-authentication}`,
live geprüft) bestätigt 13 von 14 Plan-Annahmen aus §0.6 wortgleich oder sinngleich — **eine
Ausnahme:** native/Loopback-Clients (RFC 8252 §7.3) sind inzwischen ein **dokumentiertes,
aktuelles** Anthropic-Verhalten, nicht mehr nur eine Erweiterungs-Idee. Claude Code deklariert
laut aktueller Doku `http://127.0.0.1/callback` **und** `http://localhost/callback` in seinem
CIMD, Port ignoriert, und Anthropic verlangt von AS-Betreibern, beide zu akzeptieren.

**Nikinger-Entscheidung (2026-07-28):** trotzdem draußen lassen für Step 4 — weniger Variablen,
die parallel getestet werden müssten. Rejection von `application_type: native` bleibt wie
geplant (§2.6). Diese Notiz dokumentiert den **einfacheren Weg für später**, damit er bei
Bedarf nicht neu recherchiert werden muss:

1. **Redirect-Matching ist der leichte Teil**, nicht der ganze Umfang: `redirect_uri_allowed()`
   (das `[SEAM]` aus Plan §2.6) bräuchte eine zweite Vergleichsregel für Loopback-URIs mit
   ignoriertem Port — genau wie der Docstring dort bereits vorwegnimmt.
2. **Der eigentliche Umfang ist CIMD, nicht DCR.** Claude Code identifiziert sich laut Doku über
   eine CIMD-URL als `client_id`, nicht über `/oauth/register`. Das heißt: nicht nur die
   Redirect-Prüfung lockern, sondern eine zweite Client-Identifizierungsart (CIMD-Dokument per
   HTTP abrufen, statt DCR-Registrierungszeile aus `clients`-Tabelle lesen) zusätzlich zu DCR
   bauen. Das ist der eigentliche Aufwand, nicht die Redirect-URI-Regel.
3. **`client_id_metadata_document_supported` bleibt abwesend** in den AS-Metadaten (Plan §2.2),
   bis Punkt 2 gebaut ist — die Anwesenheit dieses Felds ist laut Doku das Signal, mit dem
   Claude auf CIMD statt DCR umschaltet.
4. Quelle/Zeitpunkt: Agent-Recherche dieser Session, 2026-07-28, gegen die oben genannten
   Live-Seiten — kein `[VERIFY]`-Rest, das war bereits die Verifikation.

## Harte Regeln dieser Phase (nicht verhandelbar)

- **P4-A/P4-C — Eigener AS, strikte Abhängigkeitsrichtung.** `mcpserver → authserver`, niemals
  umgekehrt. `authserver` importiert nichts aus `mcpserver` oder `storage` — kennt nur
  Starlette, SQLite, `argon2-cffi`. Test: `test_authserver_does_not_import_mcpserver`.
- **P4-D — Token opak.** `secrets.token_urlsafe(32)`, gespeichert wird ausschließlich
  `sha256`-Hex. Kein JWT, kein JWKS, kein Signing-Key.
- **P4-F — Argon2id, nicht scrypt.** `m=19456 KiB, p=1` (OWASP + BSI TR-02102-1).
  **[2026-07-28 Korrektur, P4 Step 2]:** `t=2` war der Plan-Default, nicht der scharfe Wert —
  `[VERIFY]` V17 maß auf dieser VM ~15 ms damit (unter dem Zielkorridor 50–250 ms), Code läuft
  seit Step 2 mit **`t=8`** (~53–55 ms, gemessen). Konstante: `authserver/passwords.py ::
  ARGON2_TIME_COST`. V17 geschlossen, kein offener Punkt mehr.
- **P4-I — Ausnahme von Hard Rule 2.** Die Auth-SQLite (`/var/lib/sharefyx/auth.sqlite3`) ist
  autoritativ, keine Ableitung aus Dateien — benannte Ausnahme, berührt keine Nutzdaten.
- **P4-Q — Berührungsfläche.** P4 darf in `phase2_mcp/` genau anfassen: `mcpserver/asgi.py`,
  `mcpserver/context.py`, `mcpserver/app.py`, `mcpserver/config.py`, `mcpserver/request_log.py`,
  `mcpserver/logging_setup.py`, `scripts/serve.py`. **Nicht anfassen:** `tools.py`,
  `permissions.py`, `server.py`, `auth.py`, `credentials.py`, `storage/*`. Änderungsbedarf dort
  ist ein Befund für den Nikinger, keine Aufgabe.
- **P4-R — Bibliotheks-Pins.** `fastmcp==3.4.4` bleibt exakt (P3-D unverändert).
  `argon2-cffi==25.1.0` exakt gepinnt (in Step 0 gemessen, kein Range). Sonst keine neuen
  Laufzeitabhängigkeiten: kein `authlib`, kein `pyjwt`, kein `jinja2`, kein `itsdangerous`.

## Modul-Status

| # | Modul | Step | Status | Tests |
|---|---|---|---|---|
| 1 | Haushalt, Drift, geerbte Abnahme, kritischer Keyring-Fund (nikinger-Token) | 0 | ✅ | 0 (kein Feature-Code) |
| 2 | Paketgerüst `phase4_auth/`, `authserver/{config,models,crypto,errors}.py` | 1 | ✅ | 20 (5 `test_crypto.py` + 12 `test_authserver_config.py` + 3 `test_errors.py`) |
| 3 | `authserver/{passwords,totp,users}.py`, `scripts/{provision_user,export_auth_users}.py` | 2 | ✅ | 37 (6 `test_passwords.py` + 21 `test_totp.py` + 10 `test_users.py`) |
| 4 | `authserver/{store,ratelimit}.py` | 3 | ✅ | 19 (14 `test_authserver_store.py` + 5 `test_ratelimit.py`) |
| 5 | `authserver/{metadata,clients}.py`, erste Hälfte `routes.py` | 4 | ✅ | 16 (7 `test_metadata.py` + 8 `test_clients.py` + 1 neu in `test_authserver_config.py`) |
| 6 | `authserver/{flows,templates}.py`, `routes.py` vervollständigt (`/oauth/authorize`, `/oauth/token`) | 5 | ✅ | 36 (22 `test_flows.py` + 9 `test_routes.py` + 4 `test_templates.py` + 1 neu in `test_totp.py`) |

**Zeile 1, Step 0:** kritischer Fund — ein nie widerrufener Keyring-Token für einen dritten,
seit P2-B2 umbenannten Space (`nikinger`), live und schreibfähig. Details, Zeitachse und
Behebung (Keyring-Widerruf + Export + `systemctl restart`, beide Male live bestätigt):
`docs/concepts/PHASE3_CLOSEOUT_HANDOVER.md` §5 Nachträge. Übrige Autocompact-Drift-Funde aus dem
Handover behoben (siehe dortiger Commit-Verlauf, nicht hier dupliziert). Geerbte P3-Abnahme:
Zeile 12 (Backup-Timer) durch echten Lauf bestätigt, V13 (`diagnose.sh` vs. echtes Tailscale)
geschlossen; Zeile 6 (Reboot) und Zeile 13 (Restore-Nachweis) bleiben bewusst offen.

**Zeile 2, Step 1:** `config.py` (`AuthSettings`/`load_auth_settings`, Env-Validierung inkl.
`SPACE_PUBLIC_BASE_URL`-Härtung), `crypto.py` (opake Token, `sha256`, PKCE gegen den
RFC-7636-Appendix-B-Vektor getestet, nicht gegen einen selbst berechneten Wert), `errors.py`
(RFC-6749-Fehlercode-Whitelist, `OAuthError`), `models.py` (Step 1: Platzhalter — seit Step 3
gefüllt, siehe Zeile 4 unten). `argon2-cffi==25.1.0` exakt gepinnt (P4-R, in Step 0 gemessen).
`dev_install.sh` nimmt `phase4_auth/` ohne Änderung auf (V16 bestätigt). `.gitignore` um
`*.sqlite3` erweitert (V21 — vorher griff nur `.index.sqlite3` spezifisch, `auth.sqlite3` wäre
committebar gewesen).

**Zeile 4, Step 3:** `models.py` gefüllt (`Client`, `PendingAuthRequest`, `AuthorizationCode`,
`AccessTokenRecord`, `LoginAttempt` — frozen dataclasses, kein SQL). `store.py` (`AuthStore`):
volles Schema aus Plan §2.3 (`CREATE TABLE IF NOT EXISTS`, idempotent für `test_reopen_is_
idempotent`), alle Methoden der Plan-"fix"-Liste plus vier additive (`create_family`,
`get_login_attempt`, `upsert_login_attempt`, `clear_login_attempt` — Begründung siehe
Abweichungsnotiz unten). `ratelimit.py` (`LoginThrottle`): Eskalationsformel selbst festgelegt
(Plan gibt nur Konstanten vor), führt kein eigenes SQL. `pytest -q` → **244/244 grün** (225
Vorlauf + 19 neue: 14 `test_authserver_store.py` + 5 `test_ratelimit.py`). SQL-Containment-Grep
bestätigt: kein SQL außerhalb `store.py` (Ergebnis im Session-Block unten).

**Abweichung vom Plan, dokumentiert statt still übernommen — Testdatei-Namenskollisionen
(gilt für den ganzen Baum, nicht nur einzelne Steps; kein `--import-mode=importlib`
konfiguriert, kein gemeinsames Elternpaket zwischen den Phasen-`tests`-Verzeichnissen):**
- Der Plan sah `phase4_auth/tests/__init__.py` vor. Das kollidiert real mit dem bereits
  bestehenden `phase3_edge/tests/__init__.py` — beide würden pytest als dasselbe
  Top-Level-Modul `tests` gelten. Behoben durch Weglassen, wie in `phase1_storage/tests`/
  `phase2_mcp/tests` bereits gehandhabt (kein `__init__.py`).
- `test_config.py` hätte mit `phase2_mcp/tests/test_config.py` kollidiert (gleicher Basename,
  keine Pakete) — Datei heißt deshalb `test_authserver_config.py` (Step 1).
- **[2026-07-28, P4 Step 3]:** dieselbe Klasse traf real ein zweites Mal, nicht nur theoretisch
  — der erste volle `pytest -q`-Lauf dieser Session brach mit `import file mismatch` ab, weil
  `phase4_auth/tests/test_store.py` mit dem bereits bestehenden `phase1_storage/tests/
  test_store.py` kollidiert. Behoben: Datei heißt `test_authserver_store.py`. **Regel für
  künftige Steps:** vor dem Anlegen einer neuen Testdatei `find . -name "test_<name>.py"`
  gegen den ganzen Baum prüfen, nicht nur gegen den Plan-Dateinamen — die Kollision ist am
  Basename festgemacht, nicht am Phasenverzeichnis.

**Additive `AuthStore`-Methoden, nicht in der Plan-"fix"-Liste (Step 3, für `flows.py` in Step 5
relevant):** `create_family` (FK `auth_codes.family_id` erzwingt eine Familie vor dem ersten
Code), `get_login_attempt`/`upsert_login_attempt`/`clear_login_attempt` (weil `ratelimit.py`
selbst kein SQL führen darf). `rotate_refresh(refresh_token, *, access_ttl_s, refresh_ttl_s)`
nimmt zusätzlich die beiden TTLs entgegen statt sie aus dem Bestand abzuleiten — eine
Bestands-Ableitung hätte nach `purge_expired()` auf einer bereits gelöschten Access-Token-Zeile
gecrasht (Advisor-Fund, kein Randfall). **Hinweis für `flows.py` (Step 5):** `issue_token_pair`
liest die Familie ohne `AND revoked_at IS NULL` — sicher, weil `lookup_access_token` den
`revoked_at`-JOIN als eigene Prüfung hat (die Mission-Garantie "Replay tötet die Familie" hängt
also an `lookup_access_token`, nicht an `issue_token_pair`). Diesen JOIN in Step 5 nicht als
redundant wegvereinfachen.

**Zeile 5, Step 4:** `metadata.py` (PRM + AS-Metadaten, reine Funktionen aus `AuthSettings`,
`client_id_metadata_document_supported` bewusst abwesend), `clients.py` (DCR, `redirect_uri_
allowed()` als `[SEAM]`, `check_register_rate_limit()`), `routes.py` (erste Hälfte: beide
`.well-known`-Pfade, AS-Metadaten, `/oauth/register` — Anker `oauth_routes(auth_settings,
auth_store)` für Step 6, Plan §3.3). Security-Header direkt in den Handlern statt über
Middleware (Begründung im `routes.py`-Modul-Docstring: die Routen werden der Wurzel-App
vorangestellt, kein eigenes `Mount`, eine app-weite Middleware träfe auch `/health`/`/mcp`).
`pytest -q` → **260/260 grün** (244 Vorlauf + 16 neue). SQL-Containment-Grep weiterhin sauber
(nur `store.py`).

**Additive Änderungen außerhalb der Step-4-Dateiliste (`metadata.py`/`clients.py`/`routes.py`):**
- `errors.py :: DCRError`/`DCR_ERROR_CODES` — RFC-7591-Fehlercodes für `/oauth/register`,
  bewusst **getrennt** von `OAuthError`/`OAUTH_ERROR_CODES`: eine Vermischung hätte
  `invalid_redirect_uri`/`invalid_client_metadata` fälschlich auch aus `/oauth/authorize` oder
  `/oauth/token` als gültige Antworten erscheinen lassen (relevant für Step 5s
  `test_all_token_errors_use_invalid_grant`).
- `store.py :: increment_register_window()` — stündliches, epoch-ausgerichtetes Fenster für die
  grobe `/oauth/register`-Bremse (Plan §2.7, `register_attempts`-Tabelle existierte bereits seit
  Step 3, nur ohne Zugriffsmethode). Kein `reset()` wie bei `login_attempts`: jede Registrierung
  zählt gegen das Kontingent, unabhängig vom Ausgang — deshalb lebt die Policy-Konstante
  (`MAX_REGISTRATIONS_PER_WINDOW = 20`) in `clients.py`, nicht in `ratelimit.py`, dessen
  Docstring sich ausdrücklich auf Login pro Space bezieht.
- **`test_authserver_does_not_import_mcpserver` fehlte, seit die Zeile P4-A/P4-C ("nicht
  verhandelbar") sie in Step 1 erstmals namentlich referenzierte — vier Steps lang unbelegt.**
  Geschlossen in `test_authserver_config.py`: Grep über `authserver/*.py` mit
  zeilenanfang-verankertem Regex (`re.MULTILINE`), damit Prosa-Erwähnungen (z. B. in
  `users.py`s eigenem Docstring) nicht mitzählen, nur echte `import`/`from`-Statements.
- `starlette>=1.3,<2` neu **deklariert** in `phase4_auth/pyproject.toml` (P4-A/C nennt Starlette
  bereits als erwartete Abhängigkeit) — war zuvor bereits transitiv installiert (`mcp`/
  `sse-starlette`), `dev_install.sh` zeigt deshalb keine sichtbare Änderung; das ist kein
  vergessener Schritt. `httpx`/`pytest-asyncio` als Dev-Extras ergänzt, gleiches Testmuster wie
  `phase2_mcp/tests/test_app.py` (`httpx.ASGITransport`, `@pytest.mark.asyncio`, kein
  `asyncio_mode`-Config nötig, Default-„strict"-Modus).
- `oauth_routes(auth_settings, auth_store)` — zwei Parameter in Step 4. Plan §3.3 ankert die
  **Step-6-Aufrufform** mit drei Parametern (`..., users`) — Step 5 erweitert die Signatur, wenn
  die Login-Routen `users` tatsächlich brauchen. Das ist erwartetes Wachstum über „Step 4 baut
  die erste Hälfte, Step 5 vervollständigt", keine Drift.
- Reihenfolge in `_register`: Content-Type-Prüfung **vor** der Registrierungsbremse — eine
  falsch typisierte Anfrage verbraucht kein Kontingent. Bewusst, gegen einen Selbstläufer-Fehler
  gepinnt (`test_register_rejected_content_type_does_not_consume_rate_limit`).

**Zeile 6, Step 5:** `flows.py` (neu, bewusst frei von jedem HTTP-Framework-Import — `start_
authorize`/`submit_consent`/`issue_token` geben kleine eingefrorene Ergebnis-Typen zurück,
`routes.py` übersetzt sie; sonst wäre der Fluss nur über HTTP testbar, siehe Modul-Docstring),
`templates.py` (neu, Wegwerf-UI), `routes.py` vervollständigt um `GET`/`POST /oauth/authorize`
und `POST /oauth/token`. `pytest -q` → **296/296 grün** (260 Vorlauf + 36 neue). SQL-Containment-
und `redirect_uri_allowed`-Containment-Greps weiterhin sauber (Belege im Session-Block unten).

**Additive Änderungen außerhalb der Step-5-Dateiliste:**
- `store.py :: now()` — exponiert die injizierte `now_fn` des Stores, damit `ratelimit.
  LoginThrottle` und `totp.verify()` in `flows.py` **dieselbe** Uhr benutzen statt eine zweite zu
  injizieren (Advisor-Fund: ein eingefrorener Test-Clock im Store, aber echte Zeit anderswo,
  wäre ein stiller Drift-Herd). `oauth_routes()` baut `LoginThrottle(auth_store, now_fn=auth_
  store.now)` intern selbst — Plan §3.3 ankert weiterhin genau drei Parameter für Step 6
  (`auth_settings, auth_store, users`), eine vierte `now_fn` wäre unnötig gewesen.
- `store.py :: get_totp_counter()`/`set_totp_counter()` — die Tabelle `totp_replay` existiert
  seit Step 3, aber ohne Zugriffsmethode (gleiches additives Muster wie `increment_register_
  window` in Step 4). Zähler wird **nur** nach vollständigem Erfolg (Passwort UND TOTP)
  hochgesetzt, nicht schon bei richtigem TOTP mit falschem Passwort — sonst könnte, wer einen
  TOTP-Code beobachtet (z. B. über die Schulter), das aktuelle Zeitfenster des echten Nutzers
  verbrennen, ohne selbst das Passwort zu kennen.
- `totp.py :: verify()` gehärtet (Step 2 baute die Funktion, Step 5 fand die Lücke): ein
  unbekannter `totp_alg` oder ein nicht valides Base32-`secret` aus einer kaputten Nutzerakte
  warfen zuvor einen unbehandelten `ValueError` statt `None` zurückzugeben — ein 500 statt
  "Anmeldung fehlgeschlagen." Jetzt spiegelt `verify()` `passwords.verify_password`s
  Nie-wirft-Vertrag. Test: `test_verify_never_raises_on_malformed_secret_or_unknown_algo`
  (`test_totp.py`).
- `oauth_routes()` — dritter Parameter `users` jetzt gebaut (Plan §3.3 ankerte ihn bereits für
  Step 6, siehe Abweichungsnotiz Step 4 oben), ohne Default — die beiden bestehenden Fixtures in
  `test_clients.py`/`test_metadata.py` (`Starlette(routes=oauth_routes(settings, store))`)
  entsprechend auf `oauth_routes(settings, store, {})` erweitert.
- `_security_headers()`/`_token_headers()` getrennt: `Pragma: no-cache` steht in Plan §2.4 nur
  beim Token-Endpunkt, nicht in der allgemeinen Header-Tabelle §2.6 — ein gemeinsames Set hätte
  den Header auf die Metadatendokumente und das Consent-Formular mitgeschleift, wo er nicht
  gefordert ist.
- `RedirectError` trägt zusätzlich `error_description` (Plan §2.4: "Ab jetzt gehen Fehler als
  Redirect mit `error`, `error_description`, `state` und `iss` zurück" — im ersten Entwurf
  übersehen, im Advisor-Review dieser Session gefunden). Feste, statische Texte je Fehlercode
  (`flows.py :: _ERROR_DESCRIPTIONS`), keine Unterscheidung nach Ursache innerhalb eines Codes.
- `redirect_uri_allowed()` wird jetzt auch aus `start_authorize()` aufgerufen, nicht nur aus
  `register_client()` (Plan §2.6: "Sie wird von `/oauth/register` **und** von `/oauth/authorize`
  aufgerufen" — im ersten Entwurf ebenfalls übersehen, gleicher Advisor-Fund). Verteidigung in
  der Tiefe: eine später verschärfte Allowlist muss auch längst registrierte Redirects neu
  bewerten, nicht nur neue Registrierungen ablehnen.
- POST-`/oauth/authorize`-Fehlschläge (falsches Passwort/TOTP, gesperrtes Konto, abgelaufene/
  verbrauchte `AuthRequest`) rendern eine **Fehlerseite**, kein erneutes Formular — nur
  `action == "deny"` erzeugt einen Redirect (`access_denied`). Das ist Plan-Wortlaut (§2.4:
  "Fehlerseite", nicht "Formular erneut"), hier ausdrücklich benannt, weil es von der
  intuitiveren "bei Fehlschlag Formular mit Meldung erneut zeigen" abweicht.
- Enumerationsschutz: für einen unbekannten Space läuft ein echter Argon2id-Verify gegen
  `passwords.DUMMY_HASH`, aber **kein** `totp.verify()`-Aufruf — Argon2id bei `t=8` (~55 ms)
  dominiert die TOTP-HMAC-Prüfung um Größenordnungen, das Weglassen ist deshalb kein
  Timing-Orakel (Advisor-Review, durch `test_wrong_password_and_unknown_space_give_identical_
  response` mit Aufruf-Zähler statt Wanduhr-Messung belegt).

## Geerbte Contracts

Aus P2 (`phase2_mcp/CLAUDE.md`, `docs/concepts/phase2_mcp_plan.md` §2/§3): sechs Tools,
Tool-Contract, Fehlerabbildung, `SpaceResolver` → `Principal`, `Permissions`-Seam. Aus P3
(`phase3_edge/CLAUDE.md`, `docs/concepts/phase3_edge_plan.md` §2/§3): Credential-Weg systemd →
Prozess, Request-Log-Format, Unit-Platzhalter-Mechanik. **Der Contract ist ab jetzt wieder zu** —
P4 ändert `asgi.py`/`context.py` (P4-Q), fasst `tools.py`/`permissions.py`/`auth.py` nicht an.

---

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
Berührungsfläche, `tools.py`/`permissions.py`/`auth.py` nicht). Das ist der Step, der den
Plan-Umbau erstmals gegen den echten `mcpserver` verdrahtet — bisher lief alles ausschließlich
innerhalb von `authserver`.
