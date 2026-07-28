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

---

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
