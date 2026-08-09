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
updated: 2026-08-06
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
| 8 | `phase4_auth/scripts/authctl.py` (+ `store.py :: list_clients`/`list_families`, `config.py :: resolve_db_path`); `phase4_auth/systemd/sharefyx-mcp.service` (`StateDirectory`, zweites Credential, `SPACE_AUTH_MODE`/`SPACE_PUBLIC_BASE_URL`); `install_units.sh`/`local.env.example` erweitert; `oauth_smoke.py --base-url` (echtes Netz) | 7 | ✅ **Live-Abnahme abgeschlossen — 16/16 bestanden** (2026-07-30, Protokoll `docs/concepts/P4_ABNAHME_2026-07-29.md`). **[2026-07-30 Korrektur:** diese Zeile stand hier bis zu diesem Commit noch auf „12/16, 2026-07-29" — Zeile 9, 14/15 und der Schnitt liefen danach alle noch in derselben bzw. der Folgesession durch, ohne dass ein Zwischen-Commit diese Tabellenzeile nachzog. Dieselbe Drift-Kategorie, die Root-`CLAUDE.md` mehrfach dokumentiert (dort ist die Zeile explizit gegen genau dieses Vergessen abgesichert, diese Tabellenzeile hier bisher nicht).**]** | 21 neu: 9 `test_authctl.py` (neue Datei) + 5 neu in `test_authserver_store.py` + 3 neu in `test_units.py` (`phase3_edge/tests/`, davon 2 aus S1) + 4 neu in `test_oauth_smoke.py` |
| 8a | **Befund S1** (2026-07-29): `ALLOWED_HOSTS` ohne `127.0.0.1` machte Runbook-Schritt 4 unausführbar — `local.env.example` + `install_units.sh`-Warnung + Runbook korrigiert, kein Servercode geändert | 7 | ✅ | 2 neu in `test_units.py` (in Zeile 8 mitgezählt) |
| 8b | `phase4_auth/scripts/abnahme_run.sh` (2026-07-29) — automatisiert die acht maschinell prüfbaren Abnahmezeilen (1,2,3,10,11,12,13,16), spiegelt Aufbau/Redaktionsmuster von `phase3_edge/scripts/abnahme_run.sh` 1:1. Live gegen den echten Dienst probegelaufen (Zeilen 1/2/3/12 ok, 13/16 korrekt übersprungen, 10/11 korrekt übersprungen ohne echtes Passwort). Kein Ersatz für Zeilen 4–9/14/15 — eine curl-Nachbildung des Login-Formulars wäre eine zweite, ungetestete OAuth-Implementierung | 7 | ✅ | 0 (Runbook/Skript, gleiche Ausnahme wie `diagnose.sh`/`phase3_edge/scripts/abnahme_run.sh` — kein Unit-Test für ein Skript, das echten `systemd`/`journalctl`/Netzzugriff braucht) |
| 8c | **Live-Fund 2026-07-30:** `routes.py :: _security_headers()` — `form-action` trug nur `'self'`, Chromium prüft es aber auch gegen das Redirect-Ziel einer Formular-Antwort (hier: `302` nach `https://claude.ai/...`) und blockierte Fabians Verbindung lautlos nach jedem erfolgreichen Login. Fix: `config.py :: AuthSettings.csp_form_action` (neue Property, hält den Seam `test_redirect_uri_allowed_is_the_only_matching_path` intakt), `form-action 'self' https://claude.ai https://claude.com`. Deployt (`sudo systemctl restart`), Fabian erneut verbunden — **live bestätigt**: vollständiger Selbsttest aller sechs Tools (siehe Zeile 14/15 unten) | 7 | ✅ | 1 neu in `test_routes.py` |
| 8d | **Zeile 9 durchgeführt (2026-07-30):** `SPACE_OAUTH_ACCESS_TTL_S=60` via systemd-Drop-in, Connector neu verbunden, `create_item` → 90s Pause → `append_to_item`. DB-Gegenprobe (Claude Code, read-only): 14 `access_tokens`-Zeilen derselben `family_id`, Refresh **on-demand** exakt beim ersten Aufruf nach Ablauf, kein Hintergrund-Timer, kein neuer Login | 7 | ✅ | 0 (Live-Test, kein Code) |
| 8e | **Schnitt vollzogen (2026-07-30, Runbook-Schritt 8):** Nikinger führte `SPACE_AUTH_MODE=oauth`/`install_units.sh`/Restart/beide `--revoke`/`spaces.cred` neu/zweiter Restart live aus — **vor** jeder Code-Änderung (Plan-Reihenfolge). Claude Code verifizierte read-only (`systemctl cat` → `oauth`, `export_space_map.py` → 0 Einträge, alte Pfad-Token-URL → `401`, `/health` → `200`) und entfernte danach `TokenPathASGI`/`AuthModeASGI` aus `mcpserver/asgi.py`/`app.py` (`resolver`-Parameter aus `create_app()` entfällt mit), reduzierte `SPACE_AUTH_MODE` auf `_VALID_MODES=("oauth",)` (Plan-Wortlaut „zwei Werte" war ungenau, siehe `authserver/config.py`), entfernte `serve.py`s Step-6b-Gate (`oauth` jetzt Pflicht) — beide Nikinger-Entscheidungs-Reversierungen vorab per `AskUserQuestion` abgestimmt. **Zeile 16 damit live bestanden, 16/16, Phase 4 ✅.** | 7 | ✅ | 347 gesamt (vorher 353) — `test_asgi.py` gelöscht, `test_asgi_bearer.py` 14→10, `test_serve.py` neu (+2), restliche Dateien auf Bearer-Fixtures umgestellt |

**Steps 0–6a (Details für die Tabellenzeilen 1–7a oben) sind komprimiert und nach
`SESSIONS_ARCHIVE.md` verschoben** (2026-07-31, gleiche Rotationslogik wie
`scripts/rotate_session_block.sh`s Session-Blöcke — verbatim verschoben, nicht neu
zusammengefasst; Reassemblierung gegen den Originalstand geprüft). Diese Zeilen waren laut
eigener Notiz seit Step 6a „settled, testgepinnt, nicht mehr Arbeitskontext" — Grund für den
Nikinger-Auftrag, den Kopf unter den 40KB-Softcap zu bringen (siehe Session-Block unten, Fund
„44KB-Softcap"). Steps 7/7a–8e (die aktuell relevanten) bleiben unverändert oben in der Tabelle
und unten im Runbook/Session-Block.

## Geerbte Contracts

Aus P2 (`phase2_mcp/CLAUDE.md`, `docs/concepts/phase2_mcp_plan.md` §2/§3): sechs Tools,
Tool-Contract, Fehlerabbildung, `SpaceResolver` → `Principal`, `Permissions`-Seam. Aus P3
(`phase3_edge/CLAUDE.md`, `docs/concepts/phase3_edge_plan.md` §2/§3): Credential-Weg systemd →
Prozess, Request-Log-Format, Unit-Platzhalter-Mechanik. **Der Contract ist ab jetzt wieder zu** —
P4 ändert `asgi.py`/`app.py` (P4-Q). **[2026-07-28, Step 6a]:** `context.py` stand hier
ursprünglich mit auf der Änderungsliste (Plan §3.2 kündigt eine an) — real geändert wurde es
nicht, siehe Zeile 7a unten. P4 fasst `tools.py`/`permissions.py`/`auth.py` weiterhin nicht an.

## Runbook „Inbetriebnahme" (Step 7) — ausgeführt, nach `SESSIONS_ARCHIVE.md` verschoben

**[2026-08-06]** Phase 4 ist ✅ (16/16 live, Schnitt vollzogen); dieses Runbook wurde vom
Nikinger vollständig ausgeführt und ist damit Historie, kein lebender Text mehr. Es steht
**verbatim** in `SESSIONS_ARCHIVE.md` unter derselben Überschrift — verschoben, weil dieser
Head sonst über dem 40-KB-Softcap der Doc-Layers-Konvention liegt (ein 📗 darf das nicht,
ein 📦 schon). Wer die Inbetriebnahme nachvollziehen will, liest es dort.

## Sicherheits-Review 2026-07-29 — offene Befunde S2–S8

Vollständiges Dokument mit Fehlfällen, Fix-Skizzen und der Liste der **geprüften und in Ordnung
befundenen** Punkte: `../docs/concepts/P4_SECURITY_REVIEW_2026-07-29.md`. Kurzfassung:

| # | Befund | Schwere | Datei | Status |
|---|---|---|---|---|
| S1 | `ALLOWED_HOSTS` ohne `127.0.0.1` → `400 Invalid host header` lokal, Runbook-Schritt 4 unausführbar | Blocker | `local.env` / `install_units.sh` | ✅ **behoben** (2026-07-29) |
| S2 | `refresh_token`-Grant prüft `client_id` nicht (RFC 6749 §6) | niedrig | `flows.py`, `store.py :: rotate_refresh` | ✅ **geschlossen** (P5 Step 1) |
| S3 | Kein Audience-Check: `AccessTokenRecord.resource` wird nie gegen `settings.resource` geprüft | niedrig (heute) | `resolver.py` | ✅ **geschlossen** (P5 Step 1) |
| S4 | `scope` wird beim Zugriff nie durchgesetzt | niedrig | `resolver.py` | ✅ **geschlossen** (P5 Step 1) |
| S5 | `f"{redirect_uri}?{query}"` zerlegt einen Redirect mit vorhandenem Query | niedrig | `routes.py :: _authorize_response` | ✅ **geschlossen** (P5 Step 1) |
| S6 | `record["pwd"]`/`record["totp"]` → `KeyError` → 500 bricht den „wirft nie"-Vertrag daneben | niedrig-mittel | `flows.py :: submit_consent` | ✅ **geschlossen** (P5 Step 1) |
| S7 | Unbegrenztes Zeilenwachstum aus unauth. Eingabe, `purge_expired()` nur manuell (kein Timer) | niedrig-mittel | `store.py`, `ratelimit.py` | ✅ **vollständig geschlossen** (P5 Step 1: Timer + Längenbegrenzung; P5 Step 2: `purge_expired()` deckt jetzt auch `ui_sessions`/`invites` ab, sobald diese Tabellen mit Schema 2 existierten) |
| S8 | `sudo install_units.sh` sourced eine nutzerschreibbare Datei als root | sehr niedrig | `install_units.sh` | ✅ **geschlossen** (P5 Step 1) |
| O1 | Nutzerakten werden **einmal beim Start** gelesen — Provisionierung wirkt erst nach Restart | Betriebsnotiz | `scripts/serve.py` | ✅ **geschlossen im Code** (P5 Step 2 — `UserDirectory.get()` liest live, kein Cache mehr); **live wirksam erst nach dem Migrations-Runbook** (`phase5_ui/CLAUDE.md` Session-Block 2026-08-02), bis dahin läuft der Dienst noch auf dem alten Build |
| S10 | **Ein Reset über eine Einladung widerrief weder Token-Familien noch UI-Sitzungen** — der Passwortwechsel tut das seit P5 Step 4 (P5-Q), der *stärkere* Reset nicht. Ein altes Refresh-Token behielt vollen Zugriff, obwohl Passwort **und** TOTP ersetzt waren. Live gefunden: nach einem echten Reset standen neun Familien vom 30.07. weiter auf aktiv | mittel | `webui/routes_auth.py :: _invite_post()` | ✅ **geschlossen** (2026-08-06) — `revoke_families_for_space()` + `revoke_sessions_for_space()`, Grund `invite_redeemed`; Test gegen den ungefixten Stand als rot gegengeprüft. **Wirkt erst nach einem Deploy.** Herleitung: `phase5_ui/CLAUDE.md`, Session-Block 2026-08-06 |
| O2 | **`clients` und `token_families` werden von `purge_expired()` nie abgeräumt** — beide wachsen unbegrenzt (live: 35 DCR-Registrierungen in einer Woche für zwei Personen, 20 Token-Familien). Verschärfend: `clients.last_used_at` wird nur bei der Registrierung auf `NULL` gesetzt und nie geschrieben — die eine Spalte, an der man eine verwaiste Registrierung erkennen könnte, ist tot. Sicherheitsrisiko gering (eine Registrierung allein gewährt nichts) | Betriebsnotiz | `store.py :: purge_expired()`, `store.py:265` | ✅ **geschlossen im Code** (2026-08-09, P6 Step 2) — `purge_expired()` löscht jetzt auch tote `token_families` (widerrufen ODER natürlich abgelaufen: keine Kind-Zeile mehr in `access_tokens`/`refresh_tokens`/`auth_codes`) und `clients` ohne verbliebene Familie, je mit eigener Altersgrenze (`TOKEN_FAMILY_RETENTION_S`=30d, `CLIENT_RETENTION_S`=90d — länger, weil ein Passwortwechsel Familien sofort widerruft, während die Client-Registrierung im Claude-Account bestehen bleibt). `clients.last_used_at` bleibt tot wie beschrieben, wird für dieses Kriterium nicht gebraucht. **Wirkt erst nach einem Deploy, live-Purge-Lauf ist Nikinger-Sache** (`phase6_shares/CLAUDE.md` Step-2-Session-Block, Gate A→B Punkt 3) |
| S9 | `submit_consent()` prüfte `record.status` nie — ein per `authctl.py disable-user` gesperrter Space konnte sich über den OAuth-Consent-Login sofort eine neue Token-Familie holen, die Sperre war ohne UI-Anteil wirkungslos | niedrig-mittel | `flows.py :: submit_consent` | ✅ **geschlossen** (P5 Step 4) |

**[2026-08-02 Korrektur, P5 Step 1]:** der Absatz „Keiner von S2–S8 ist gefixt" stand hier
bewusst zwischen Step 7 und der Live-Abnahme — dieser Zustand ist jetzt überholt. Alle sieben
Befunde S2–S8 sind in P5 Step 1 geschlossen (Details, Tests, Commit: `phase5_ui/CLAUDE.md`
Session-Block 2026-08-02). Dieser Kopf ist ein 📗 live gepflegtes Dokument, kein 📕-Snapshot —
die Tabelle wird hier direkt nachgezogen statt in einem separaten Nachtrag dupliziert.

**[2026-08-03, P5 Step 4]:** ein neuer Befund **S9** (Tabelle oben) — eine geschlossene Phase
mit einem 📗 live gepflegten Kopf bekommt bei Code-Änderungen dieselbe Behandlung wie S2–S8, kein
stiller Abstand. `submit_consent()` (`flows.py`) prüft jetzt `record.status == "active"` als
zusätzliches Erfolgskriterium neben Passwort/TOTP, enumerationssicher (kein eigener Fehlercode,
läuft nach demselben unconditional Argon2id-Verify wie zuvor) — Gegenstück zur analogen Prüfung
in `webui/routes_auth.py :: _login_post` (P5 Step 4). Auslöser: `authctl.py disable-user` (Step
7, Modul-Status Zeile 8 oben) widerrief bisher nur Sitzungen und Token-Familien, aber kein
Login-Pfad prüfte je `users.status` — ein deaktivierter Space konnte sich mit unverändertem
Passwort/TOTP sofort neu einloggen bzw. neu autorisieren (Advisor-Fund, `phase5_ui/CLAUDE.md`
Session-Block 2026-08-03 hat die volle Herleitung). Dieselbe Session ergänzte `store.py` um
`revoke_families_for_space()` (P5-Q, Passwortwechsel widerruft ALLE Familien) und
`revoke_invites_for_space()` (schließt eine verwandte Lücke: eine noch nicht eingelöste
Einladung hätte `disable-user` sonst über `_invite_post`s `upsert_user(..., status="active")`
umgangen) sowie `authctl.py` um `invite`/`list-users`/`disable-user`/`enable-user`/
`list-sessions`/`revoke-sessions` (Step 4, Plan-Tabelle oben in „Runbook" fehlt dafür — die
Unterbefehle sind neuer P5-Umfang, keine Ergänzung des P4-Runbooks). Details, Tests, Commit:
`phase5_ui/CLAUDE.md` Session-Block 2026-08-03.

**[2026-08-06, P5 Step 8b, kein Sicherheitsbefund — Nikinger-Feedback „alte UI beim
Connector-Neuanmelden"]:** `authserver/templates.py :: render_login_form()` trug seit P4 den
Docstring „wird in Phase 5 ersetzt" — P5-G verbietet das aber ausdrücklich (getrennter
Consent-Flow als Absicht, keine Übergangslösung), das Modul blieb dadurch die rohe
Phase-4-Wegwerf-UI, während `webui/pages.py` seit Step 7b gestaltet ist. Behoben durch
CSS-Wiederverwendung (`<link>` auf `/ui/static/app.css`, kein Python-Import — P4-A bleibt
unverändert), `routes.py :: _security_headers()`s CSP dafür von `style-src 'unsafe-inline'`
(ohne `'self'`) auf `style-src 'self'; font-src 'self'` umgestellt. Reine Gestaltungskorrektur,
keine Rechte-/Auth-Änderung. Details: `phase5_ui/CLAUDE.md` Session-Block 2026-08-06 (Step 8b).

**[2026-08-09, P6 Step 2 — O2 geschlossen]:** `store.py :: purge_expired()` räumt jetzt auch
`token_families`/`clients` ab (zwei neue Konstanten, `TOKEN_FAMILY_RETENTION_S`/
`CLIENT_RETENTION_S`, +8 Tests in `test_authserver_store.py`, 250→258). Volle Herleitung
(Prädikat, FK-Reihenfolge, warum zwei getrennte Fristen) und der Rest von Step 2 (Client-
Surface-Logging, `diagnose.sh`, `ui_budget.py`): `phase6_shares/CLAUDE.md` Step-2-Session-Block —
lebt dort, nicht doppelt hier, weil P4 formal abgeschlossen ist und dieser Kopf nur die O2-Zeile
selbst nachzieht.

**[2026-08-09, P6 Step 3 — Schema 3]:** `store.py`s erste echte Spaltenerweiterung auf einer
bereits gefüllten Tabelle (`users.seen_update_id TEXT`, additiv, `PRAGMA table_info()`-Check vor
`ALTER TABLE`, da SQLite dafür kein `IF NOT EXISTS` kennt — anders als V1→V2, das nur neue
Tabellen anlegte). `SCHEMA_VERSION` jetzt `"3"`, zwei neue Methoden
(`get_seen_update_id`/`set_seen_update_id`), +3 Tests in `test_authserver_store.py` (258→261,
darunter ein Migrationstest v2→v3 nach dem Muster des bestehenden v1→v2-Tests). Speist das
Update-Log-Banner in `phase5_ui/webui/api.py`. Volle Herleitung: `phase6_shares/CLAUDE.md`
Step-3-Session-Block — lebt dort, gleiche Begründung wie beim O2-Absatz oben.

---

## Session stopped — 2026-07-30 (Schnitt vollzogen, 16/16, Phase 4 ✅ — TokenPathASGI entfernt)

**Für den nächsten, kalten Leser:** vorige Session endete mit 15/16, einzig der Schnitt
(Runbook-Schritt 8) stand aus. Diese Session begann nach einem Context-Compaction-Verlust — der
einzige erhaltene Rest war eine Notiz: „16/16 confirmed — SPACE_AUTH_MODE=oauth is live, and the
old path-token URL now returns 401". Auftrag laut CLAUDE.md-Root-Prompt: erst den echten
Plan-Wortlaut lesen statt aus der eigenen Runbook-Paraphrase zu arbeiten, dann handeln.

**Erster Schritt, vor jeder Code-Änderung: die 16/16-Prämisse selbst verifizieren, nicht aus dem
Kontext-Rest übernehmen.** `git status` stand auf `d06ced0` (15/16, Schnitt offen) — die Notiz
allein wäre laut Repo-eigener Lehre („eine Doku-Aussage über den Repo-Zustand ist erst wahr,
wenn `git status` sie bestätigt", `phase2_mcp/CLAUDE.md`) kein Beleg gewesen. Read-only
gegengeprüft: `systemctl cat sharefyx-mcp` → `SPACE_AUTH_MODE=oauth`,
`SPACE_PUBLIC_BASE_URL=https://savefyx-vmware-virtual-platform.tail89fc2a.ts.net`;
`export_space_map.py` → `0 Einträge` (beide Pfad-Token tot); `curl` gegen die alte
Pfad-Token-URL (`/mcp/<beliebig>`) → `401`; `/health` → `200`, `uptime_s` plausibel seit dem
Restart. Der Nikinger hatte Runbook-Schritt 8 also tatsächlich bereits live ausgeführt, **vor**
jeder Code-Änderung — genau die vom Plan verlangte Reihenfolge. **Zeile 16 damit live bestanden,
16/16.**

**Scope-Klärung vor dem Umbau, per `AskUserQuestion`:** der Plan-Satz „TokenPathASGI und
AuthModeASGI aus dem Code entfernen" hat einen größeren Blast Radius als der Runbook-Kommentar
nahelegt — `README.md`s Dev-Workflow, `phase2_mcp/scripts/mcp_smoke.py` und `serve.py`s
Step-6b-`SPACE_AUTH_MODE`-Gate (eine gelockte Nikinger-Entscheidung vom 2026-07-28) hängen alle
am `oauth=None`-Pfad, der mit `TokenPathASGI` verschwindet. Zwei Fragen dem Nikinger vorgelegt,
nicht angenommen: (1) vollen Rückbau inklusive Dev-Pfad, oder Dev-Pfad als bewusste Ausnahme
erhalten? (2) `SPACE_AUTH_MODE` auf einen Wert (`oauth`) oder zwei (Plan-Wortlaut, aber nach der
vollen Entfernung funktional unbegründet) reduzieren? Antwort: **voller Rückbau**, **ein Wert**.

**Umsetzung, ein Commit:**
- `phase2_mcp/mcpserver/asgi.py` — `TokenPathASGI`, `AuthModeASGI`, `_credential_from_path`,
  `_send_401` gelöscht. Nur `BearerAuthASGI` bleibt.
- `phase2_mcp/mcpserver/app.py` — `create_app()`: `resolver`-Parameter entfernt (diente nur dem
  Bau von `TokenPathASGI`), `oauth: OAuthConfig` jetzt ohne Default, die `if oauth is None`-Weiche
  entfällt, `Mount("/mcp")` bekommt `BearerAuthASGI` direkt.
- `phase4_auth/authserver/config.py` — `_VALID_MODES=("oauth",)`, `base_url` unconditional
  Pflicht (die `mode in ("oauth","both")`-Verzweigung war mit nur einem gültigen Wert tot).
- `phase2_mcp/scripts/serve.py` — Step-6b-Gate (`"SPACE_AUTH_MODE" in os.environ`) entfernt,
  `load_auth_settings()` läuft jetzt immer ungefangen.
- `phase2_mcp/scripts/mcp_smoke.py`, `phase4_auth/scripts/oauth_smoke.py`,
  `phase4_auth/tests/test_oauth_smoke.py`, `phase2_mcp/tests/test_app.py`,
  `phase2_mcp/tests/test_asgi_bearer.py`, `phase2_mcp/tests/test_request_log.py` — Pfad-Token-
  Fixtures (`KeyringTokenResolver`/`_FakePathResolver`/feste Token-Strings im Pfad) durch echte,
  gegen eine temporäre `AuthStore` gemintete Bearer-Token ersetzt (`create_family()` +
  `issue_token_pair()`, dasselbe Muster wie `test_asgi_bearer.py` es für P4 Step 6a schon nutzte).
  **`mcp_smoke.py` steht nicht auf P4-Qs Berührungsliste** (die nennt `scripts/serve.py`, nicht
  `scripts/mcp_smoke.py`) — dem Nikinger vorab per `AskUserQuestion` vorgelegt (Option nannte
  die Datei explizit), gewählt: „Voller Rückbau". Genehmigt, nicht stillschweigend erweitert.
- `phase2_mcp/tests/test_serve.py` (neu) — bisher deckte kein Test `serve.py :: main()`s
  Verdrahtung ab (Settings → `AuthSettings` → `create_app()` → `uvicorn.run()`), beide
  Smoke-Skripte bauen `create_app()` direkt und rufen `main()` nie auf. Ohne diesen Test wäre der
  nächste `systemctl restart sharefyx-mcp` der erste echte Test dieser Verdrahtung gewesen
  (Advisor-Fund, zweiter Durchlauf dieser Session). `uvicorn.run`/`load_users` gepatcht, nie der
  echte Keyring oder ein echter Port.
- `phase2_mcp/tests/test_asgi.py` gelöscht (testete ausschließlich `TokenPathASGI`).
  `test_asgi_bearer.py` um `_FakePathResolver`, `test_auth_mode_token_preserves_p2_behaviour`,
  `test_auth_mode_both_serves_bearer_and_path`, `test_default_auth_mode_is_oauth` und
  `test_six_tools_behave_identically_under_bearer_and_path_token` gekürzt (14→10) — die
  Bearer-vs-Pfad-Token-Vergleichstests hatten mit dem Wegfall der zweiten Seite keinen
  Vergleichspartner mehr; **bewusst dokumentiert entfernt**, kein stilles Verschwinden (Advisor-
  Vorgabe dieser Session).
- `phase4_auth/tests/test_authserver_config.py` —
  `test_load_auth_settings_token_mode_does_not_require_base_url` durch
  `test_load_auth_settings_rejects_token_mode_after_the_cut` ersetzt.
- `README.md`, `phase3_edge/local.env.example`, `phase4_auth/CLAUDE.md` (dieses Dokument),
  `context.py`/`asgi.py`/`app.py`-Docstrings — auf den Schnitt nachgezogen.

**Verifiziert, nicht nur behauptet:** `pytest -q` → **347/347 grün** (vorher 353 — die Differenz
ist die Nettosumme aus `test_asgi.py` [-4], `test_asgi_bearer.py` [14→10, -4] und dem neuen
`test_serve.py` [+2, Advisor-Fund im zweiten Durchlauf: `serve.py :: main()`s Verdrahtung war
bis dahin ungetestet — beide Smoke-Skripte bauen `create_app()` direkt und rufen `main()` nie
auf], keine neue Lücke). `git diff --stat` auf `tools.py`/`permissions.py`/`server.py`/`storage/`
→ **leer** (Akzeptanzkriterium §6.9). Zusätzlich real gelaufen, nicht nur `pytest` grün
behauptet:
`mcp_smoke.py --json` → 12/12 Checks grün gegen den vollen `create_app()`-Stack mit echten
Bearer-Token; `oauth_smoke.py` (In-Process-Default) → **11/11 Prüfungen grün** (Discovery, DCR,
Consent, Code-Tausch, echter Tool-Aufruf mit Bearer, Refresh, Refresh-Replay tötet die Familie,
zweite Authorize-Runde, Code-Replay tötet die Familie) — der volle OAuth-Fluss funktioniert nach
der Entfernung des `resolver`-Parameters unverändert.

**Ergebnis: 16 von 16 Abnahmezeilen live bestanden. Phase 4 ✅ — alle acht Steps (0–7)
abgeschlossen.** `ROADMAP.md`, `docs/INDEX.md`, Root-`CLAUDE.md` im selben Commit nachgezogen
(P4 auf ✅, R5 abschließend korrigiert, Hard Rule 1 um den TOTP-Seed-Satz ergänzt).
`phase2_mcp/CLAUDE.md`s Test-Zähl-Zeile ebenfalls nachgezogen (100→94, `test_asgi.py`
verschwunden, `test_asgi_bearer.py` 14→10, `test_serve.py` neu mit 2).

**Zweiter Advisor-Durchlauf dieser Session** (nach dem ersten Commit-Entwurf, vor dem
tatsächlichen Commit) fand vier weitere Punkte: `serve.py :: main()` war ungetestet (behoben,
`test_serve.py` oben), `test_mcp_requires_token` prüfte `401` ohne den `WWW-Authenticate`-Header
zu prüfen (ergänzt — genau das ist Abnahmezeile 2), `spaces.cred` wurde totes Gewicht (dokumentiert
oben im Runbook, nicht angefasst), `mcp_smoke.py` liegt außerhalb von P4-Qs Berührungsliste
(bereits vorab mit dem Nikinger abgestimmt, hier nur nachträglich in den Papierpfad
aufgenommen). Alle vier in diesem Commit behoben oder dokumentiert, keiner still liegen gelassen.

**Nachtrag 2026-07-31 — Stale-Doc-Sweep (Nikinger-Auftrag, vor dem Push):** ein zweiter Check
lief gezielt nach veralteten Doku-Aussagen, nicht nur nach fehlenden Statusupdates. Drei echte
Funde, alle Kommentar-/Docstring-only: `phase3_edge/CLAUDE.md`s Disconnected-Runbook behauptete
noch, der `400`-Fehler träfe nur „unter `SPACE_AUTH_MODE=both|oauth`" — seit dem Schnitt ist die
`TrustedHostMiddleware` unconditional aktiv, der Mode-Qualifier war gegenstandslos, korrigiert
(aktiv gelesenes Runbook, nicht nur historische Notiz). Gleicher Fund in
`phase3_edge/tests/test_units.py`s Docstring, korrigiert ohne Testlogik/Fixture-Daten
anzufassen. `phase2_mcp/mcpserver/credentials.py :: load_space_map()`s Docstring behauptete, der
laufende Dienst löse Token noch darüber auf (`auth.py :: KeyringTokenResolver`) — seit dem
Schnitt läuft die Live-Auflösung ausschließlich über `OAuthTokenResolver`/Bearer,
`load_space_map()` bleibt nur Bestandswerkzeug. `pytest -q` weiterhin grün. Commit `47d5bc4`.

**Zweiter Nachtrag 2026-07-31 — Kopf unter den 40KB-Softcap komprimiert (Nikinger-Auftrag):**
die Steps-0–6a-Detailnarrative (Tabellenzeilen 1–7a, seit Step 6a als „settled, nicht mehr
Arbeitskontext" markiert) ist **verbatim** nach `SESSIONS_ARCHIVE.md` verschoben — gleiche
Disziplin wie `scripts/rotate_session_block.sh`: nichts abgetippt, drei-Teile-Schnitt
(`sed -n`) gegen den Originalstand auf Byte-Identität geprüft, bevor beide Dateien geschrieben
wurden. Die Modul-Status-**Tabelle** (alle 16 Zeilen) bleibt vollständig im Kopf; nur die Prosa
darunter ist gewandert. `phase4_auth/CLAUDE.md`: 46862 B → 35202 B (unter dem Softcap).
`phase4_auth/SESSIONS_ARCHIVE.md`: 59395 B → 72546 B (L3, kein Cap). `docs/INDEX.md`s
Größenangaben im selben Commit nachgezogen. `pytest -q` unverändert grün — reine Doku-Bewegung,
keine Code-Zeile berührt.

**Nächster Schritt (konkret):** kein offener Code- oder Live-Punkt mehr in P4, der Kopf ist
wieder unter dem Softcap. Es fehlt nur noch der **formale** Phasenabschluss (Handover-Dokument
P4→P5, analog `PHASE3_CLOSEOUT_HANDOVER.md`) — laut `docs/PROMPTS.md` ein eigener Prompt im
Browser-Webchat, Sache des Nikingers. Dabei mitnehmen: `spaces.cred`/`export_space_map.py` aus
der P4-Unit entfernen (siehe Runbook-Fund oben). Phase 3 bleibt bei 🟡 stehen (nur Zeile 13,
Restore-Nachweis, fehlt) — unverändert durch diese Session, nicht Teil ihres Auftrags.

**Dritter Nachtrag, 2026-08-02 (P5 Step 0 A — Rückbau vollzogen, mehrere Stellen oben jetzt
historisch):** der formale Phasenabschluss ist erledigt (`docs/concepts/
PHASE4_CLOSEOUT_HANDOVER.md`, P5-Planungssession), und der „Fund, nicht behoben" oben
(`spaces.cred`/`export_space_map.py` als totes Gewicht) ist geschlossen: beide Skripte
(`phase2_mcp/scripts/issue_token.py`, `phase3_edge/scripts/export_space_map.py`) sind gelöscht,
die `LoadCredentialEncrypted=spaces:…`-Zeile ist aus der Unit entfernt, `credentials.py` ist auf
`hash_token()` reduziert (`auth.py :: KeyringTokenResolver` mit entfernt). Konsequenz für diesen
Kopf: **die Runbook-Schritte 3/4 im „Schnitt"-Codeblock oben** (`issue_token.py --revoke`,
`export_space_map.py | systemd-creds encrypt`) beschreiben ausschließlich, was am 2026-07-30
tatsächlich lief — nicht mehr, was heute ausführbar wäre, beide Skripte existieren nicht mehr.
Ebenso ist die Aussage „`load_space_map()` bleibt nur Bestandswerkzeug" (Nachtrag oben) durch den
Rückbau überholt: die Funktion selbst ist entfernt, nicht nur ihr Docstring korrigiert. Beide
Stellen bleiben als historischer Nachweis stehen (Prinzip wie im Rest dieses Kopfs: Session-Blöcke
werden nicht rückwirkend umgeschrieben), diese Notiz macht die Drift nachvollziehbar. Details,
Testzahlen und die (noch offene) Nikinger-Aktion A.7: `phase5_ui/CLAUDE.md` Session-Block
2026-08-02.

