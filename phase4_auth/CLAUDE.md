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

## Geerbte Contracts

Aus P2 (`phase2_mcp/CLAUDE.md`, `docs/concepts/phase2_mcp_plan.md` §2/§3): sechs Tools,
Tool-Contract, Fehlerabbildung, `SpaceResolver` → `Principal`, `Permissions`-Seam. Aus P3
(`phase3_edge/CLAUDE.md`, `docs/concepts/phase3_edge_plan.md` §2/§3): Credential-Weg systemd →
Prozess, Request-Log-Format, Unit-Platzhalter-Mechanik. **Der Contract ist ab jetzt wieder zu** —
P4 ändert `asgi.py`/`context.py` (P4-Q), fasst `tools.py`/`permissions.py`/`auth.py` nicht an.

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
