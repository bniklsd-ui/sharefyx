---
status: live
purpose: Phase-Head Web-UI, REST-API, Auth-Selbstverwaltung — Scope, harte Regeln, Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase5_ui/ oder an den in P5-B genannten Dateien in authserver/mcpserver — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase5_ui_plan.md             # voller Plan, Entscheidungen P5-A–P5-AE, Steps 0–9
  - ../docs/concepts/PHASE4_CLOSEOUT_HANDOVER.md   # Herkunft der offenen Entscheidungen §4.1–§4.5, [VERIFY]-Bilanz V14–V26
updated: 2026-08-03
---

# CLAUDE.md — Phase 5: Web-UI, REST-API, Auth-Selbstverwaltung (`phase5_ui/`)

> **Menschen benutzen das System ohne SSH und ohne Editor.** Zwei getrennt beweisbare Dinge:
> ein Mensch kann sein Konto selbst verwalten (Einladung, Passwort/TOTP/Recovery, ohne Neustart),
> und ein Mensch kann Notizen/Aufgaben im Browser lesen und schreiben, über eine REST-API auf
> demselben Storage-Kern wie die sechs MCP-Tools.
> **Quelle der Wahrheit ist der Code, nicht dieses Dokument.**
> Vollständiges Design + alle 30 gelockten Entscheidungen (P5-A–P5-AE) + Steps 0–9:
> `../docs/concepts/phase5_ui_plan.md`.

## Mission (zuerst lesen)

Der Härtetest der Phase ist nicht die Oberfläche, sondern **Block A vor Block B**: ein System,
in dem ein Mensch sein Passwort selbst setzen kann, ist auch ohne schöne Oberfläche ein
Werkzeug. Eine schöne Oberfläche auf einem Konto, das nur per SSH existiert, ist es nicht. Unter
Druck fällt Block B (REST-API/UI) weg, nicht Block A (Sicherheit/Selbstverwaltung) — dieselbe
Roadmap-Regel („die späteste Phase fällt weg, nie eine frühere Regel") eine Ebene tiefer.

## Bauprinzip (Projekt-Kernprinzip)

„Der Server ist dumm." **Phase 5 enthält KEINE AI**, kein serverseitiges Rendern fremder Bodies
zu HTML (P5-Y), kein LLM, keine Zusammenfassung, kein Auto-Tagging.

## Scope (Kurzform, Details: Plan §0.5 P5-A–P5-AE)

- **DRIN:** Sicherheitsbefunde S2–S8 vollständig schließen (P5-S), Auth-Datenmodell in
  `auth.sqlite3` (Schema 2: `users`/`invites`/`recovery_codes`/`ui_sessions`), eigene
  Cookie-Session für die UI (kein OAuth, P5-D), REST-API `/api/v1/*` über denselben Storage-Kern,
  statische Single-File-UI unter `/ui` (kein Build-Step, P5-T), Deploy/Rollback/Staging/
  Auth-Backup (P5-AB/P5-R).
- **DRAUSSEN:** zweites Dateiformat/Anhänge (Seam ja, Implementierung nein, P5-Z/P5-AA),
  FastMCP-4-Umstieg/CIMD/DPoP (P5-C), Mobilversion (P5-W), Realtime/WebSocket, Löschen (bleibt
  `status: archived`), Rechte zwischen Spaces jenseits von Rule 4.

## Harte Regeln dieser Phase (nicht verhandelbar)

- Alle Hard Rules aus Root-`CLAUDE.md` gelten unverändert.
- **P5-B — Berührungsfläche.** P5 darf `authserver/` und `mcpserver/{app,asgi}.py` anfassen.
  **Tabu:** `storage/`, `mcpserver/tools.py`, `mcpserver/permissions.py`, `mcpserver/server.py`
  — `git diff` darauf ist am Phasenende leer (Akzeptanzkriterium 18). `webui` darf genau **ein**
  Symbol aus `mcpserver` importieren (`permissions.OwnSpaceWritable`), sonst nichts — ein Test
  hält das fest (`test_webui_imports_exactly_one_mcpserver_symbol`).
- **P5-D/P5-F — zwei getrennte Auth-Wege, architektonisch, nicht per `if`.** `/mcp` akzeptiert
  niemals Cookies (nur `Authorization: Bearer`). `/api`/`/ui` akzeptieren niemals Bearer-Token
  (nur Cookie-Session). Beide Richtungen sind Tests (Akzeptanzkriterium 19).
- **P5-G — UI-Session ≠ OAuth-Consent.** `/oauth/authorize` liest niemals Cookies und verlangt
  bei jeder Connector-Autorisierung Passwort **und** TOTP, auch bei bestehender UI-Sitzung.
- **P5-Y — fremde Bodies werden nie serverseitig zu HTML gerendert.** Die API liefert reinen
  Text; Rendering + Sanitizing passiert ausschließlich im Browser.
- **Rotationsregel ab Tag 1.** Dieser Head trägt **genau einen** Session-Block. Beim Anlegen
  eines neuen wandert der bisherige **verbatim** nach `SESSIONS_ARCHIVE.md` — Durchführung über
  `scripts/rotate_session_block.sh phase5_ui`, nie von Hand.
- **Commit ⇒ Note-Update, im selben Commit** (Hard Rule 8): Modul-Tabelle unten + Session-Block.

## Die gelockten Entscheidungen (P5-A – P5-AE) — Kurzform (Details: Plan §0.5)

Ein Phasenschnitt, zwei Blöcke, harter Gate dazwischen (A) · Berührungsfläche `authserver`/
`mcpserver/{app,asgi}` (B) · MCP-Revision 2026-07-28 bleibt eigene Mini-Phase (C) · eigene
Cookie-Session, kein OAuth für die UI (D) · `__Host-sfx_session`, Idle 12h/Absolut 7d (E) ·
`/mcp` nie Cookies, `/api`+`/ui` nie Bearer (F) · UI-Session kürzt Consent nicht ab (G) ·
Double-Submit-CSRF + Herkunftsprüfung (H) · Nutzerakten wandern in `auth.sqlite3` (I) ·
TOTP-Seeds AES-256-GCM verschlüsselt, drittes Credential `auth-dek` (J) · Einladungstoken/
Recovery-Codes/Session-IDs gehasht, nicht Argon2id (K) · `UserDirectory` liest live, kein
Neustart mehr nötig — schließt O1 (L) · Erstvergabe über Einmal-Einladung (M) · zehn
Recovery-Codes ersetzen den TOTP-Faktor (N) · Passwortpolitik 12–128 Zeichen + lokale Blocklist
(O) · Re-Auth bei sicherheitsrelevanten Änderungen (P) · Passwortwechsel widerruft alle
Token-Familien + fremde UI-Sessions (Q) · eigenes verschlüsseltes Auth-Backup (R) · S2–S8
vollständig schließen (S) · statische Single-File-UI, kein Build (T) · Markdown-Textarea +
Formatierhilfen, kein WYSIWYG (U) · Notizheft-Neubau mit Ernte (V) · 16:9-Desktop first, keine
Mobilversion (W) · Dunkel-first, Apple-Formensprache vor „Liquid Glass" (X) · fremde Bodies nie
serverseitig gerendert (Y) · Format-Seam ohne Implementierung (Z) · Anhänge draußen (AA) ·
Release-Verzeichnisse + Health-Gate + Staging, kein Blue/Green (AB) · Blue/Green als Seam (AC) ·
Messung statt Schätzung (`ui_budget.py`, AD) · gemeinsame Live-Abnahme, beide Nutzer (AE).

## Modul-Status

| # | Modul | Step | Status | Tests |
|---|---|---|---|---|
| 1 | Haushalt, Verifikationsdurchlauf, Rückbau P2-Token-Reste, Doku-Drift, P3-Restore-Nachweis | 0 | ✅ **vollständig** — A.7 vom Nikinger live ausgeführt, P3 Zeile 13 vom Nikinger bestätigt (13/13, Phase 3 ✅) | −14 (Rückbau, kein neuer Feature-Code) |
| 2 | Sicherheitsbefunde S2–S8 vollständig geschlossen (`authserver/{resolver,flows,store,ratelimit,routes}.py`, `phase3_edge/scripts/install_units.sh`, `phase5_ui/systemd/sharefyx-purge.{service,timer}`) | 1 | ✅ **vollständig** — 7/7 Befunde geschlossen, Meta-Test bestätigt keine offene Zeile mehr | +20 (2 `test_authserver_store.py` + 4 `test_resolver.py` + 2 `test_routes.py` + 3 `test_flows.py` + 2 `test_ratelimit.py` + 5 `test_units.py` + 2 `test_security_review_register.py`, neue Datei) |
| 3 | Auth-Datenmodell: Schema 2, `secretbox.py`, `userdir.py`, `flows.py`/`app.py`/`serve.py` auf `UserDirectory` umgestellt, `import_users_to_db.py` | 2 | ✅ **vollständig** — schließt O1 strukturell (kein Cache mehr) und die S7/S6-Restarbeit aus Step 1 (`ui_sessions`/`invites`-Purge, `UserDirectory.get()` ersetzt den Übergangs-Fix) | +61 (7 `test_secretbox.py` + 8 `test_authserver_config.py` + 23 `test_authserver_store.py` + 13 `test_userdir.py` + 3 `test_flows.py` + 7 `test_import_users_to_db.py`, drei neue Dateien) |
| 4 | Neues Paket `phase5_ui/` (`pyproject.toml`, `webui/{__init__,config,security,sessions,pages,routes_auth,errors}.py`, `phase5_ui/tests/`): Sessions, CSRF, Login/Logout | 3 | ✅ **vollständig** — `/ui/login`, `/ui/logout` gegen eine echte In-Process-`Starlette`-App durchgespielt; **V35 geschlossen** (`dev_install.sh`s `phase*_*/`-Glob nimmt `phase5_ui/` ohne Skriptänderung auf) | +22 (5 `test_sessions.py` + 7 `test_security.py` + 7 `test_routes_auth.py` + 3 `test_isolation.py`, vier neue Testdateien + `conftest.py`) |

---

## Session stopped — 2026-08-03 (Step 3: neues Paket `phase5_ui/` — Sessions, CSRF, Login/Logout)

**Für den nächsten, kalten Leser:** vierte Session der Phase, direkt im Anschluss an Step 2
(„weiter" nach der Advisor-Review + Commit von Step 2). Plan §5 Step 3 zeigt nur auf §2.7
(Sessions/CSRF/Re-Auth) und §3.4 (Sicherheits-Header) — **nicht** auf §2.8 (Einladungs-/
Enrollment-Fluss, braucht `webui/passwords_policy.py` aus Step 4) und **nicht** auf §2.9
(Passwortpolitik). Entsprechend baut dieser Step ausschließlich Login/Logout, nicht
`/ui/invite/{token}` — auch wenn §1.3s Modulkarte `routes_auth.py`/`pages.py` mit „Einladung,
Enrollment" beschreibt: das ist die **finale** Form über mehrere Steps hinweg, nicht Step 3s
Umfang. Mit dem Advisor vor dem ersten Code vorab geklärt (keine Ambiguität stillschweigend
aufgelöst).

**Neues Paket, editable installiert:** `phase5_ui/pyproject.toml` (Paket `webui`, Abhängigkeit
`authserver`), `webui/__init__.py`. `dev_install.sh`s `phase*_*/`-Glob nimmt das Verzeichnis ohne
Skriptänderung auf — **V35 damit geschlossen**, keine Codeänderung nötig, nur geprüft. Root-
`pytest.ini`s `testpaths` um `phase5_ui/tests` ergänzt (ohne diese Zeile hätte `pytest -q` vom
Repo-Wurzelverzeichnis die neuen 22 Tests nie gesammelt — mit `pytest phase5_ui/tests` allein
wäre das unbemerkt geblieben, Advisor-Hinweis).

**Bauteile, in Reihenfolge:**

1. **`config.py`** — `UiSettings` (Cookie-Name `__Host-sfx_session`, `idle_ttl_s`/
   `absolute_ttl_s` als Code-Konstanten 12h/7d nach P5-E, **nicht** über Umgebungsvariablen wie
   `AuthSettings.access_ttl_s` — P5-E nennt keinen Live-Testbedarf wie
   `SPACE_OAUTH_ACCESS_TTL_S` in P4, ein ungenutzter Konfigurationshaken wäre eine Fläche mehr,
   die falsch gesetzt werden kann). **Bewusst OHNE Env-Loader** (anders als
   `authserver.config.load_auth_settings()`, Advisor-Fund: eine erste Fassung hatte
   `load_ui_settings()`, aber nichts rief sie auf und kein Test deckte sie ab — totes Gewicht,
   Hard Rule 7 — entfernt statt ungetestet stehen gelassen). Ein eigenes `UiSettings`-Objekt,
   keine gemeinsame Settings-Klasse mit `authserver` (würde beide Seiten koppeln); die echte
   Umgebungsvariablen-Verdrahtung entscheidet sich erst in Step 5/6, wenn `/ui` real in
   `scripts/serve.py` gemountet wird. `static_dir` fehlt aus demselben „noch kein Bedarf"-Grund
   (§1.3s Modulkarte nennt es als Teil der finalen Form über mehrere Steps, nicht als
   Step-3-Bedarf — Step 3 liefert keine statischen Dateien aus).
2. **`errors.py`** — `CsrfError` (→403), kleinere Menge als `authserver/errors.py`: kein
   RFC-Fehlercode-Vokabular, das kommt erst mit `ApiError` in Step 5.
3. **`sessions.py :: SessionManager`** — `issue`/`load`/`rotate`/`clear` über die
   Step-2-`AuthStore`-Methoden (`create_session`/`touch_session`/`revoke_session`), kein
   eigenes SQL. Cookie exakt nach Plan: `Path=/`, `Secure`, `HttpOnly`, `SameSite=Strict`, kein
   `Domain`, kein `Max-Age`.
4. **`security.py`** — `ui_security_headers()` (eigene CSP, **getrennt** von
   `authserver/routes.py :: _security_headers()` — die OAuth-Seite braucht `claude.ai` in
   `form-action`, die UI nicht) und `require_csrf()`. **Dokumentierte Abweichung vom
   Plan-Schnipsel** (mit dem Advisor vorab abgestimmt, kein Alleingang): die Plan-Signatur zeigt
   nur `require_csrf(request, session)`, aber §2.7s Text selbst verlangt den Origin-Vergleich
   gegen `settings.base_url` — die Funktion trägt deshalb zusätzlich `settings: UiSettings` und
   `form_token: str | None` (der bereits aus dem Formular gelesene Wert, damit die Funktion den
   Request-Body nicht selbst konsumieren und nicht `async` werden muss — ein Aufrufer, der
   ohnehin `await request.form()` braucht, reicht das Feld einfach durch).
5. **`pages.py`** — `render_login_page()`/`render_error_page()` nach dem Muster von
   `authserver/templates.py` (kein Framework, kein `<script>`). **`render_logged_in_page()`
   zusätzlich zum Plan-Wortlaut, dokumentiert statt stillschweigend:** `SessionManager.rotate()`
   gibt den CSRF-Token nur EIN einziges Mal als Klartext zurück (`ui_sessions` speichert nur
   `csrf_hash`) — ein bloßer `302`-Redirect nach erfolgreichem Login hätte diesen Wert
   verworfen, und keine nachfolgende CSRF-geprüfte Anfrage (z. B. Logout) hätte je einen
   gültigen Wert vorlegen können. Die Seite trägt den Token als verstecktes Feld in einem
   Logout-Formular — Übergangslösung, **wird in Step 6 durch die echte App-Shell ersetzt**, kein
   dauerhafter Bestandteil des Designs.
6. **`routes_auth.py`** — `ui_auth_routes()`: `GET`/`POST /ui/login`, `POST /ui/logout`. Login
   dupliziert bewusst die enumerationssichere Prüfung aus `flows.py :: submit_consent()`
   (Argon2id unconditional, TOTP/Recovery nur wenn der Space existiert, dieselbe
   `LoginThrottle`/`login_attempts`-Tabelle) statt sie zu teilen — P5-G hält UI-Sitzung und
   OAuth-Consent architektonisch getrennt, eine gemeinsame Funktion wäre eine Kopplung, die der
   Plan hier nicht vorsieht. `/ui/invite/{token}` bewusst NICHT gebaut (siehe oben).

**Advisor-Fund, vor dem Commit behoben — derselbe Fehler wie in P5 Step 2, eine Zeile über der
Kopiervorlage übersehen:** die erste Fassung rief `store.set_totp_counter()` **innerhalb** des
TOTP-Zweigs auf, sobald `accepted_counter is not None` — also potenziell **vor** dem
Passwort-Gate weiter unten. Ein richtiger TOTP-Code mit falschem Passwort hätte damit das
aktuelle 30-Sekunden-Zeitfenster für den echten Nutzer verbrannt, exakt die Lehre, die der
Kommentar zwei Zeilen darüber in `flows.py` festhält (dort saß der Aufruf schon richtig, hinter
dem Gate) — beim Nachbau hier trotzdem in den falschen Zweig gerutscht. Fix: `accepted_counter`
vor der Verzweigung auf `None` initialisiert, `set_totp_counter()` erst nach
`throttle.reset(space)` (also nach dem vollständigen Erfolg) aufgerufen, genau wie in
`flows.py`. Neuer Test `test_correct_totp_with_wrong_password_does_not_burn_the_counter`
(`test_routes_auth.py`): falsches Passwort + gültiger TOTP-Code → 401, Zähler bleibt `None`.

**Tests, vier neue Testdateien plus `conftest.py` (`phase5_ui/tests/`, gemeinsame Fixtures — Muster
wie `test_flows.py`, `base_url` bewusst `https://…`: `__Host-`-Cookies verlangen `Secure`, httpx
sendet ein `Secure`-Cookie nicht über `http://` zurück, sonst sähen die Session-Tests grün aus,
ohne dass das Cookie je zurückreist):**
- `test_sessions.py` (5) — Cookie-Flags, kein `Domain`, Session-ID nie im Klartext in
  `ui_sessions` (direkte SQLite-Abfrage gegen die Testdatenbank, nicht nur Rückgabetyp-Prüfung),
  Idle-/Absolut-Timeout.
- `test_security.py` (7) — `require_csrf()` als reine Funktion (fehlender/falscher Token,
  fremde Herkunft, `Sec-Fetch-Site`-Ersatz bei fehlendem `Origin`, `GET` braucht keinen Token),
  CSP ohne `unsafe-inline`, `form-action` nur `'self'` (belegt: **nicht** die OAuth-Header).
- `test_routes_auth.py` (7) — Enumerationsschutz (falsches Passwort/unbekannter Space
  ununterscheidbar), Session-Rotation bei Login, Logout widerruft serverseitig, abgelaufenes
  Cookie wird beim Logout-Response gelöscht (`Max-Age=0`), Sicherheits-Header auf UI-Seiten,
  gemeinsame Fehlversuchsbremse mit dem OAuth-Consent-Login (fünf UI-Fehlversuche sperren auch
  einen anschließenden `flows.submit_consent()`-Aufruf für denselben Space), der
  TOTP-Zähler-Regressionstest oben.
- `test_isolation.py` (3, Akzeptanzkriterium §6.19/P5-F/P5-G) — `/mcp` ignoriert ein echtes,
  gültiges UI-Sitzungscookie (bleibt 401), `/oauth/authorize` liest niemals Cookies (identische
  Anfrage mit/ohne Sitzungscookie liefert dasselbe Login-Formular, kein abgekürzter Consent),
  `/api`-Bearer-Test als **dokumentierter Platzhalter** („nach Step 5 zu schärfen", Plan-Wortlaut
  wörtlich übernommen) — `/api/v1/*` existiert erst ab Step 5, ein Mount hier vorzugreifen wäre
  erfundener Scope; geprüft wird stattdessen, dass `SessionManager.load()` einen
  `Authorization`-Header schlicht ignoriert (kein Cookie → `None`, unabhängig vom Bearer-Wert).

**Verifiziert, nicht nur behauptet:** `pytest -q` (Repo-Wurzel, `pytest.ini` inklusive
`phase5_ui/tests`) → **436/436 grün** (414 zu Step-2-Ende, +22). `git diff` bleibt auf den
Tabu-Pfaden (`storage/`, `mcpserver/tools.py`/`permissions.py`/`server.py`) leer — `webui`
importiert in diesem Step nichts aus `mcpserver` (die P5-B-Ausnahme,
`permissions.OwnSpaceWritable`, kommt erst mit der REST-API in Step 5/6;
`test_webui_imports_exactly_one_mcpserver_symbol` deshalb bewusst noch nicht gebaut — ein Test
für „genau ein Import" wäre bei null Imports nicht aussagekräftig). `Done when` aus Plan §5
Step 3 („Login/Logout gegen eine In-Process-App durchgespielt") liegt buchstäblich vor:
`test_routes_auth.py` fährt echte `POST /ui/login` → `POST /ui/logout`-Rundläufe gegen eine aus
`ui_auth_routes()` gebaute `Starlette`-App, kein interner Kurzschluss über `SessionManager`
allein.

**Nächster Schritt (konkret):** Step 4 (Selbstverwaltung — Einladung, Passwort, TOTP, Recovery,
Connectoren: `webui/{account,reauth,passwords_policy}.py`, `webui/blocklist.txt`,
`authctl.py`-Erweiterungen). Danach der harte Gate vor Block B (Abnahmezeilen 1–9 live). Die
drei liegen gebliebenen Live-Aktionen aus Step 1/2 (S3/S4-Gegenprobe, Purge-Timer aktivieren,
Migrations-Runbook) bleiben unverändert offen, Sache des Nikingers, blockieren aber weiterhin
keinen Code-Step.
