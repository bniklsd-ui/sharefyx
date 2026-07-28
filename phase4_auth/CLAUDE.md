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
| 7a | `authserver/resolver.py`; `mcpserver/{asgi,context,app}.py` verdrahtet (Bearer-Auflösung, `AuthModeASGI`, `oauth=None`) | 6a | ✅ | 19 (6 `test_resolver.py` + 13 `test_asgi_bearer.py`) |

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

**Zeile 7a, Step 6a:** `authserver/resolver.py` (`OAuthTokenResolver`, `ResolvedPrincipal`,
`ResolveError` — erfüllt `mcpserver.auth.SpaceResolver` strukturell, ohne `mcpserver` zu
importieren, Plan §1.3). `mcpserver/asgi.py`: `BearerAuthASGI` (Authorization-Header →
`ResolvedPrincipal` → echter `Principal`), `AuthModeASGI` (P4-N-Weiche), `_credential_from_path`
aus `TokenPathASGI` herausgezogen (geteilt mit `AuthModeASGI`s `both`-Dispatch, verhaltensgleich).
`mcpserver/app.py`: `create_app(..., oauth: OAuthConfig | None = None)` — **ein** optionaler
Parameter (Plan §3.3), root-`TrustedHostMiddleware` nur wenn `oauth is not None` **und**
`allowed_hosts` gesetzt ist. `mcpserver/context.py` **unverändert** — siehe Fund unten.
`pytest -q` → **315/315 grün** (296 Vorlauf + 19 neue: 6 `test_resolver.py` + 13
`test_asgi_bearer.py`). `test_app.py` explizit separat gegen den unveränderten Diff laufen
lassen (`git diff --stat`, leer) — Bedingung für „`oauth=None` verhält sich exakt wie P3".

**Fund statt Umsetzung — `context.py` brauchte keine Änderung:** Plan §3.2 kündigt an, der Guard
solle „den `Authorization`-Header desselben Requests lesen und dessen `sha256` vergleichen".
Real gebraucht wurde das nicht: `BearerAuthASGI` schreibt `token_hash` in **denselben**
`scope["state"]`-Slot, mit **derselben** `sha256`-Funktion (`authserver.crypto.hash_secret` ==
`credentials.hash_token`, byte-identisch), den `TokenPathASGI` bereits seit P2 benutzt —
`assert_principal_matches_request()` liest diesen Slot bereits generisch, ganz ohne
Moduswissen. Nicht nur behauptet: `test_bearer_token_reaches_a_real_tool_call` treibt ein
echtes Bearer-Token durch den vollen Stack (`create_app()` → `AuthModeASGI` → `BearerAuthASGI` →
FastMCP → `tools.py :: list_spaces` → der echte Guard) bis zu einem echten Tool-Ergebnis; wäre
der Guard falsch verdrahtet, würde hier `AuthError` auftreten, nicht in einem Fake. Zweiter
Advisor-Durchlauf dieser Session verlangte genau diesen Beweis — die erste Fassung hatte den
Fund nur gegen einen Fake-Resolver (`test_valid_bearer_sets_principal_space`) und einen
handgebauten Fake-Request (`test_guard_rejects_principal_from_other_request`) belegt, keiner
von beiden lässt `scope["state"]` tatsächlich durch die echte FastMCP-App laufen.

**Zweiter Advisor-Fund derselben Session:** `TrustedHostMiddleware` (P4-P) wurde von keinem Test
tatsächlich instanziiert — die einzige bestehende Integrationsprobe hatte `allowed_hosts=()`,
die Bedingung `hosts is not None` griff also nie. Nachgezogen:
`test_trusted_host_middleware_protects_root_app_when_configured` — erlaubter Host → 200 auf
`/health` **und** `/.well-known/oauth-protected-resource`, fremder Host → 400. Wichtig für Step 7:
`/health` muss unter der Middleware weiter antworten, P3s Disconnected-Runbook hängt daran.

**Notiz für Step 7 (nicht verteidigt, nur dokumentiert):** in `both`-Modus routet ein
Pfad-Segment, das vorhanden aber **ungültig** ist, zu `TokenPathASGI` und bekommt ein blankes
401 ohne `WWW-Authenticate` — ein Bearer-Client, der je einen Unterpfad von `/mcp/` anspricht,
verliert den Discovery-Hinweis. Mit `path="/"` (Mount-Wurzel) und `stateless_http=True` sollte
das unerreichbar sein; falls Step 7s Live-Abnahme das anders zeigt, ist das hier vorgemerkt,
kein neuer Fund.

**Split-Entscheidung (Advisor, vor der Umsetzung):** Step 6 ist laut Plan-Dateiliste deutlich
größer als jeder vorige Step — `authserver/resolver.py` + Test, sechs geänderte
`mcpserver`-Dateien, `oauth_smoke.py` (das eigentliche Phasenbeweis-Skript, RFC-9700-Replay
inklusive), `request_log.py`/`logging_setup.py`-Erweiterung, zwei weitere Tests. Aufgeteilt in
**6a** (dieser Commit: Resolver, `BearerAuthASGI`/`AuthModeASGI`, `create_app()`-Verdrahtung,
zehn der zwölf Plan-Tests) und **6b** (nächste Session: Logging-Erweiterung, `oauth_smoke.py`,
`scripts/serve.py`-Verdrahtung, die beiden verbleibenden Tests). Begründung: `oauth_smoke.py`
ist der Beweis der ganzen Phase, kein Testhelfer — verdient eine eigene Session, keinen
Seitenast eines bereits vollen Commits.

## Geerbte Contracts

Aus P2 (`phase2_mcp/CLAUDE.md`, `docs/concepts/phase2_mcp_plan.md` §2/§3): sechs Tools,
Tool-Contract, Fehlerabbildung, `SpaceResolver` → `Principal`, `Permissions`-Seam. Aus P3
(`phase3_edge/CLAUDE.md`, `docs/concepts/phase3_edge_plan.md` §2/§3): Credential-Weg systemd →
Prozess, Request-Log-Format, Unit-Platzhalter-Mechanik. **Der Contract ist ab jetzt wieder zu** —
P4 ändert `asgi.py`/`app.py` (P4-Q). **[2026-07-28, Step 6a]:** `context.py` stand hier
ursprünglich mit auf der Änderungsliste (Plan §3.2 kündigt eine an) — real geändert wurde es
nicht, siehe Zeile 7a unten. P4 fasst `tools.py`/`permissions.py`/`auth.py` weiterhin nicht an.

---

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
`AuthStore` + `load_users()` und reicht sie als `OAuthConfig` an `create_app()`). Plan §4/§5
Step 6, Dateiliste dort. Zwei verbleibende benannte Tests: `test_oauth_log_never_contains_
secrets` (treibt über `oauth_smoke.py`, Markerwerte `ZZZ-PASSWORD`/`ZZZ-CODE`, prüft den ganzen
Logpuffer), `test_oauth_events_carry_stage_and_duration`. **`OAuthLogASGI`s `stage`-Ableitung
darf keinen Request-Body lesen** (der trägt `code_verifier`/`refresh_token`) — Methode+Pfad
reichen für `register`/`authorize_get`/`authorize_post`/`token_code`-oder-`token_refresh`; wenn
sich `token_code` und `token_refresh` ohne Body-Zugriff nicht unterscheiden lassen, ist
`stage="token"` (ohne die Grant-Unterscheidung) der akzeptierte Kompromiss, dokumentiert statt
stillschweigend gelöst (Advisor-Vorgabe dieser Session). Step 6b Done-when (Plan): `pytest`
grün, `oauth_smoke.py` 11/11, die sechs Tools verhalten sich unter Bearer-Auth exakt wie unter
Pfad-Token (Antwort-Diff im Session-Block).
