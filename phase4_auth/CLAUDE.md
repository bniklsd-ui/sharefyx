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
| 7b | `phase4_auth/scripts/oauth_smoke.py`; `mcpserver/{request_log,logging_setup}.py` erweitert (`OAuthLogASGI`, `_SECRET_PATTERNS`); `scripts/serve.py` verdrahtet (`SPACE_AUTH_MODE`-Gate) | 6b | ✅ | 6 neu in `test_oauth_smoke.py` (neue Datei, 11/11 `oauth_smoke.py` + fünf Regressionstests) + 3 neu in `test_request_log.py` + 6 neu in `test_logging.py` + 1 neu in `test_asgi_bearer.py` (Plan-Done-when-Klausel 3: sechs Tools unter Bearer vs. Pfad-Token) |
| 8 | `phase4_auth/scripts/authctl.py` (+ `store.py :: list_clients`/`list_families`, `config.py :: resolve_db_path`); `phase4_auth/systemd/sharefyx-mcp.service` (`StateDirectory`, zweites Credential, `SPACE_AUTH_MODE`/`SPACE_PUBLIC_BASE_URL`); `install_units.sh`/`local.env.example` erweitert; `oauth_smoke.py --base-url` (echtes Netz) | 7 | 🟡 **Code-Vorbereitung fertig — Live-Teile stehen aus, Sache des Nikingers** (Provisionierung, `sudo systemd-creds`, `systemctl restart`, Connector in beiden Accounts, Abnahmematrix) | 19 neu: 9 `test_authctl.py` (neue Datei) + 5 neu in `test_authserver_store.py` + 1 neu in `test_units.py` (`phase3_edge/tests/`) + 4 neu in `test_oauth_smoke.py` |

**Zeile 1, Step 0:** kritischer Fund — ein nie widerrufener Keyring-Token für einen dritten,
seit P2-B2 umbenannten Space (`nikinger`), live und schreibfähig. Details, Zeitachse und
Behebung (Keyring-Widerruf + Export + `systemctl restart`, beide Male live bestätigt):
`docs/concepts/PHASE3_CLOSEOUT_HANDOVER.md` §5 Nachträge. Übrige Autocompact-Drift-Funde aus dem
Handover behoben (siehe dortiger Commit-Verlauf, nicht hier dupliziert). Geerbte P3-Abnahme:
Zeile 12 (Backup-Timer) durch echten Lauf bestätigt, V13 (`diagnose.sh` vs. echtes Tailscale)
geschlossen; Zeile 6 (Reboot) und Zeile 13 (Restore-Nachweis) bleiben bewusst offen.

**Zeile 2, Step 1 (komprimiert 2026-07-28, Step 6a — settled, testgepinnt, nicht mehr
Arbeitskontext):** `config.py`, `crypto.py` (PKCE gegen RFC-7636-Appendix-B), `errors.py`
(`OAuthError`), `models.py` (Step 1 Platzhalter, seit Step 3 gefüllt). `argon2-cffi==25.1.0`
exakt gepinnt. `.gitignore` um `*.sqlite3` erweitert (V21).

**Zeile 4, Step 3 (komprimiert):** `models.py` gefüllt, `store.py`/`AuthStore` (volles Schema
Plan §2.3), `ratelimit.py`/`LoginThrottle` (Eskalationsformel selbst festgelegt). `pytest -q` →
244/244. Additive Methoden, nicht in der Plan-"fix"-Liste: `create_family`,
`get_login_attempt`/`upsert_login_attempt`/`clear_login_attempt` (`ratelimit.py` führt kein
eigenes SQL). `rotate_refresh(..., access_ttl_s, refresh_ttl_s)` nimmt die TTLs explizit entgegen
statt sie aus dem Bestand abzuleiten — eine Ableitung crasht nach `purge_expired()` auf einer
bereits gelöschten Access-Token-Zeile (kein Randfall). **Hält weiter:** `issue_token_pair` liest
ohne `AND revoked_at IS NULL` — sicher, weil `lookup_access_token`s `revoked_at`-JOIN die
Mission-Garantie trägt, nicht `issue_token_pair`; diesen JOIN nie als redundant vereinfachen.
**Testdatei-Namenskollisionen** (gilt für den ganzen Baum, kein `--import-mode=importlib`): vor
jeder neuen Testdatei `find . -name "test_<name>.py"` gegen den ganzen Baum prüfen, nicht nur
gegen den Plan-Dateinamen — traf real zweimal zu (`test_config.py`→`test_authserver_config.py`,
`test_store.py`→`test_authserver_store.py`).

**Zeile 5, Step 4 (komprimiert):** `metadata.py` (PRM + AS-Metadaten), `clients.py` (DCR,
`redirect_uri_allowed()` als `[SEAM]`), `routes.py` erste Hälfte (`.well-known`-Pfade,
`/oauth/register`). Security-Header direkt in den Handlern statt Middleware (Routen werden der
Wurzel-App vorangestellt, kein eigenes `Mount`). `pytest -q` → 260/260. Additive Funde: `errors.py
:: DCRError`/`DCR_ERROR_CODES` bewusst getrennt von `OAuthError` (sonst erschienen
`invalid_redirect_uri`/`invalid_client_metadata` fälschlich auch aus `/oauth/authorize`/
`/oauth/token` als gültig); `store.py :: increment_register_window()` (stündliches Fenster, kein
`reset()` — jede Registrierung zählt, unabhängig vom Ausgang); `test_authserver_does_not_
import_mcpserver` fehlte trotz Zitat in P4-A/C seit Step 1, vier Steps lang unbelegt, jetzt
geschlossen; `oauth_routes(auth_settings, auth_store)` zwei Parameter (Plan §3.3 ankert die
Step-6-Form mit drei — erwartetes Wachstum, keine Drift); Content-Type-Prüfung läuft vor der
Registrierungsbremse (falsch typisierte Anfrage verbraucht kein Kontingent, gepinnt).

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
`mcpserver/config.py` geprüft und **unverändert gelassen**: Plan §1.2 listet es unter „GEÄNDERT:
… neue Settings", real gebraucht wurde keine — `AuthSettings.mode`/TTLs/`base_url` decken alles
ab, `Settings.allowed_hosts` existiert bereits seit P4-P für genau diesen Zweck. Kein erfundenes
Feld, um die Plan-Dateiliste zu erfüllen (gleiche Regel wie `errors.py` in Step 5).
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

## Runbook „Inbetriebnahme" (Step 7, live — führt der Nikinger aus, nicht Claude Code)

Claude Code liefert Code, Units und diese Befehlsfolge; alles, was den echten `DATA_ROOT`, den
echten Keyring, echte Nutzerakten/Token oder die Claude-Accounts berührt, führt der Nikinger
selbst aus (Plan §5 Step 7) — dieselbe Arbeitsteilung wie P3s „Inbetriebnahme"
(`phase3_edge/CLAUDE.md`). **Reihenfolge ist der halbe Runbook** (Plan-Wortlaut).

```
# 0) Vorbereitung — bereits erledigt (dieser Commit)
#    phase4_auth/systemd/sharefyx-mcp.service, install_units.sh + local.env.example erweitert,
#    authctl.py, oauth_smoke.py --base-url. local.env um AUTH_MODE=both, PUBLIC_BASE_URL
#    ergänzen (cp phase3_edge/local.env.example phase3_edge/local.env, falls noch nicht
#    geschehen — die sechs Werte eintragen).

# 1) Nutzerakten provisionieren (TOTP-Seeds SOFORT in die Authenticator-Apps, QR aus der
#    otpauth://-URI — provision_user.py zeigt sie genau einmal)
python phase4_auth/scripts/provision_user.py --space niklas
python phase4_auth/scripts/provision_user.py --space fabian

# 2) Nutzerakten verschlüsselt bereitstellen — immer als Pipe, nie über eine Zwischendatei
#    (P3 §2.1, höherer Einsatz als bei spaces.cred: hier sind es echte TOTP-Seeds)
python phase4_auth/scripts/export_auth_users.py \
  | sudo systemd-creds encrypt --name=auth-users - /etc/sharefyx/auth-users.cred
sudo chmod 600 /etc/sharefyx/auth-users.cred

# 3) Units installieren, Dienst neu starten (AUTH_MODE=both aus local.env — Pfad-Token UND
#    Bearer laufen parallel, nichts fällt während der Abnahme aus)
sudo phase3_edge/scripts/install_units.sh
systemctl status sharefyx-mcp

# 4) oauth_smoke.py gegen den lokalen Port — BEVOR irgendjemand einen Connector anfasst
python phase4_auth/scripts/oauth_smoke.py --base-url http://127.0.0.1:8765 --space niklas
#    Fragt Passwort + TOTP-Seed interaktiv ab (getpass, nie als Argument). 11/11 erwartet.

# 5) Discovery von außen — resource gegen die geplante Connector-URL halten
curl -s https://<node>.<tailnet>.ts.net/.well-known/oauth-protected-resource
curl -s https://<node>.<tailnet>.ts.net/.well-known/oauth-authorization-server

# 6) Connector in BEIDEN Accounts neu anlegen: https://<node>.<tailnet>.ts.net/mcp
#    Ohne Client-ID, ohne Secret. Connect -> Passwort + TOTP -> Consent.

# 7) Abnahmematrix fahren (unten) — Protokoll nach P2/P3-Konvention, mit Belegen statt
#    Behauptungen. docs/concepts/P4_ABNAHME_<Datum>.md erst NACH diesem Schritt schreiben
#    (ein Ergebnis-Protokoll für eine Matrix, die noch nicht gelaufen ist, wäre ein
#    fabriziertes Protokoll — Advisor-Vorgabe dieser Session).

# 8) Schnitt (NICHT auf einen Termin warten — Plan-Wortlaut: „ein both-Modus, der auf einen
#    Termin wartet, ist genau das Risiko, dessentwegen P4 vorgezogen wurde")
#    AUTH_MODE=oauth in local.env, install_units.sh erneut, restart.
python phase2_mcp/scripts/issue_token.py --revoke niklas
python phase2_mcp/scripts/issue_token.py --revoke fabian
python phase3_edge/scripts/export_space_map.py \
  | sudo systemd-creds encrypt --name=spaces - /etc/sharefyx/spaces.cred
sudo systemctl restart sharefyx-mcp
#    Danach TokenPathASGI/AuthModeASGI aus dem Code entfernen, SPACE_AUTH_MODE auf zwei Werte
#    reduzieren — Codeentfernung IM SELBEN COMMIT wie die Abnahme (Plan-Wortlaut), nicht vorab.
```

**Abnahmematrix** (16 Zeilen, Protokoll nach P2/P3-Konvention — Belege statt Behauptungen):

| # | Prüfung | Erwartung | Braucht Fabian |
|---|---|---|---|
| 1 | `/health` von außen | unverändert, unauthentifiziert | nein |
| 2 | `POST /mcp` ohne Token | **401** mit korrektem `WWW-Authenticate` | nein |
| 3 | Discovery von außen | beide `.well-known` liefern, `resource` exakt | nein |
| 4 | Connect `niklas` | DCR → Consent → Tool-Aufruf erfolgreich | nein |
| 5 | Falsches Passwort | generische Meldung, keine Enumeration | nein |
| 6 | Fünf Fehlversuche | Sperre greift, `authctl.py unlock --space niklas` hebt sie | nein |
| 7 | Falscher TOTP-Code | Fehlschlag; korrekter Code danach erfolgreich | nein |
| 8 | TOTP-Replay | derselbe Code ein zweites Mal → Fehlschlag | nein |
| 9 | Access-Token-Ablauf | TTL kurz setzen, Claude refresht selbständig | nein |
| 10 | Refresh-Replay | `oauth_smoke.py` → `invalid_grant`, Familie tot | nein |
| 11 | Code-Replay | `oauth_smoke.py` → `invalid_grant`, Familie tot | nein |
| 12 | Fremdregistrierung | `redirect_uri` auf fremder Domain → abgelehnt | nein |
| 13 | Secret-Grep im journald | **leer** | nein |
| 14 | Connect `fabian` | eigener Space, eigener Login | **ja** |
| 15 | Cross-Space unter OAuth | fremder Body gewrappt, Schreibversuch `write_denied` | **ja** |
| 16 | Pfad-Token tot | alte URL → 401 | nein |

**Terminrisiko (Nikinger-Entscheidung 2026-07-28, im Plan gelockt):** Zeilen 14/15 brauchen
Fabian — ein Terminrisiko, das die Phase nicht blockieren soll. 14/16 bestanden → 🟡
code-complete (P5 darf beginnen); ✅ erst nach beiden Zwei-Personen-Zeilen. Schritt 8 (Schnitt)
darf **nicht** auf einen Termin warten, siehe Runbook oben.

**Done when** (Plan §5 Step 7): 14/16 bestanden, Schnitt vollzogen, Pfad-Token widerrufen,
`TokenPathASGI` entfernt, Protokoll geschrieben, `ROADMAP.md`/`docs/INDEX.md`/Phase-Head
nachgezogen.

---

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
