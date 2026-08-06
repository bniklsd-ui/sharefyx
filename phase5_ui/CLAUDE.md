---
status: live
purpose: Phase-Head Web-UI, REST-API, Auth-Selbstverwaltung — Scope, harte Regeln, Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase5_ui/ oder an den in P5-B genannten Dateien in authserver/mcpserver — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase5_ui_plan.md             # voller Plan, Entscheidungen P5-A–P5-AE, Steps 0–9
  - ../docs/concepts/PHASE4_CLOSEOUT_HANDOVER.md   # Herkunft der offenen Entscheidungen §4.1–§4.5, [VERIFY]-Bilanz V14–V26
updated: 2026-08-05
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
| 5 | Selbstverwaltung: Einladung/Enrollment, Passwort, TOTP, Recovery, Connectoren (`webui/{account,reauth,passwords_policy}.py`, `webui/blocklist.txt`, `webui/{pages,routes_auth,errors}.py` erweitert; `authctl.py`-Erweiterung um `invite`/`list-users`/`disable-user`/`enable-user`/`list-sessions`/`revoke-sessions`; `authserver/store.py` um `revoke_families_for_space()`/`revoke_invites_for_space()`; `authserver/flows.py :: submit_consent()` um den Status-Gate) | 4 | ✅ **vollständig** — **V30 geschlossen** (Blocklist-Herkunft: `SecLists`-10k-Liste, siehe `passwords_policy.py`-Docstring); zwei Advisor-Funde vor dem Commit behoben (**S9** in `phase4_auth/CLAUDE.md`s Befund-Tabelle: `disable-user` blockierte den Login nicht; verworfener CSRF-Token nach Passwortwechsel — beide Details im Session-Block unten) | +31 (7 `test_account.py` + 7 `test_invite_enroll.py` + 3 `test_passwords_policy.py` + 1 `test_reauth.py`, vier neue Testdateien; +1 `test_routes_auth.py`; P4-seitig +1 `test_flows.py` + 8 `test_authctl.py` + 3 `test_authserver_store.py`) |
| 6 | `/ui/*` aus Step 5 vorgezogen verdrahtet: `mcpserver/app.py :: create_app()` mountet `ui_auth_routes()`+`account_routes()` (kein neuer Parameter, `UiSettings`/`SessionManager` aus dem vorhandenen `oauth`-Bündel gebaut) | 4→5 (Gate-Voraussetzung) | ✅ **vollständig** — Live-Fund des Nikingers (`/ui/invite/…` → `404`) UND ein Plan-Widerspruch (§1.2 verbietet `mcpserver→webui`, §1.5 verlangt es) gemeinsam geschlossen, Entscheidung + Details im Session-Block unten | +3 (`phase2_mcp/tests/test_app.py`: `test_create_app_mounts_ui_routes_without_import_cycle`, `test_ui_login_reachable_through_create_app`, `test_ui_invite_reachable_through_create_app`) |
| 7 | `/ui/enroll/confirm`: CSRF-Fehlschlag rendert jetzt einen Retry (`routes_auth.py :: _enrollment_retry()`, geteilt mit „falscher Code") statt `render_error_page()`s Sackgasse; **Root Cause gefunden und behoben:** `webui/security.py`s `Referrer-Policy` von `no-referrer` auf `strict-origin` — `no-referrer` liess die Fetch-Spec den `Origin`-Header eines reinen HTML-`<form>`-POSTs auf `null` setzen, auch bei einer echten Same-Origin-Anfrage | 4 (Gate-Live-Fund) | ✅ **vollständig, live bestätigt** — Prozess-Neustart-Zeitstempel gegen die erste erfolgreiche `200`-Antwort auf `/ui/enroll/confirm` read-only gegengeprüft (nicht nur behauptet); `errors.py :: CsrfError`s Docstring korrigiert (unabhängiger, vorbestehender Fund); Details `SESSIONS_ARCHIVE.md` (Fünfter–Neunter Nachtrag, 2026-08-03/04) | +2 (`test_enroll_confirm_csrf_failure_offers_a_retry_not_a_dead_end`, `test_csrf_foreign_origin_logs_the_received_value_but_not_to_the_client`, `test_ui_referrer_policy_does_not_null_the_origin_header_on_same_origin_posts` — drei Tests, siehe Archiv für die Aufschlüsselung je Nachtrag) |
| 8 | REST-API v1: `webui/{api,serializers}.py`, `mcpserver/app.py :: create_app()` mountet `api_routes(ui_settings, store, ui_sessions, own_space_writable)` (`OwnSpaceWritable()` jetzt einmal instanziiert, geteilt mit `build_mcp()`) | 5 | ✅ **vollständig** — `scripts/ui_smoke.py` (neu, Gegenstück zu `mcp_smoke.py`/`oauth_smoke.py`) läuft In-Process durch Einladung→Enrollment→Login→`/api/v1/{me,spaces,items,...}`, 12/12 Prüfungen grün; eigener Fund (nicht im Plan-Testliste): `storage.store.Store.archive()` hat anders als `update()`/`append()` keinen Schutz gegen ein bereits archiviertes Item — in `api.py` (nicht in `storage/`, dort tabu) mit einem zusätzlichen `store.get()`-Check NACH der Rechteprüfung geschlossen | +38 (23 `test_api.py` + 7 `test_serializers.py`, zwei neue Testdateien; `phase2_mcp/tests/test_app.py` +1 `test_api_items_reachable_through_create_app`; `phase5_ui/tests/test_isolation.py` `test_api_endpoint_ignores_bearer_token` geschärft — Platzhalter seit Step 3 gegen die echte, gemountete Route ersetzt, kein zusätzlicher Test) |
| 9 | UI-Gerüst: `webui/static_routes.py` (`GET /ui/` sitzungsgated, `GET /ui/static/{path}`), `webui/static/{app.html,app.css,app.js,fonts/}`, `webui/config.py :: UiSettings.static_dir`, `scripts/build_font_subset.sh` (echte Inter-Variable-Subsetting-Pipeline, schließt V27), `mcpserver/app.py` mountet `static_routes()` | 6 | ✅ **vollständig** — Navigation/Liste/Suche/schreibgeschützte Detailansicht gegen die echte REST-API aus Step 5; **kein** Editor, **kein** Markdown-Rendering, **kein** Versionsband (bewusst Step-7-Scope). Korrigiert einen Plan-Selbstwiderspruch (§1.5-Tabelle „`/ui/` Auth: keine" vs. der im selben Plan-Abschnitt verlangte Testname `test_index_route_requires_session`) zugunsten des Tests, Details im Session-Block unten | +8 (7 `test_static_routes.py`, neue Datei; `phase2_mcp/tests/test_app.py` +1 `test_ui_index_route_reachable_through_create_app`; JS bleibt laut Plan unit-ungetestet) |
| 10 | Editor, Vorschau, Konflikt, Frontmatter-Felder: `webui/api.py` +`GET /api/v1/meta`; `webui/static/app.js` um Markdown-Parser/Sanitizer (geerntet + erweitert aus `docs/concepts/notiz_heft_example.html`), Editor-Zustand, Versionsband, Speichern/Konfliktdialog, Anlegen/Anhängen/Archivieren, Frontmatter-Felder, Entwurfsschutz, „Sitzung abgelaufen"-Karte, Formatierhilfen-Leiste erweitert; `webui/static/{app.css,app.html}` entsprechend erweitert | 7 | ✅ **vollständig** — kein Passwortänderungsdialog (eigener Nachtrag, Zeilen 5/6 der Block-A-Abnahme folgen dort), kein Deploy/Rollback (Step 8), keine zweite Formatvariante (P5-Z bleibt Seam). Umfangreiche Node/jsdom-gestützte End-to-End-Simulation (Scratchpad, nicht im Repo) fand und schloss zwei echte Funde vor dem Commit: (1) das Test-Mock selbst hatte einen `includes()`-Bug (`/api/v1/meta` matchte fälschlich auch `/api/v1/me`) — beim Beheben zusätzlich `reportUnexpectedError()` in `app.js` ergänzt, weil (2) `loadItems()`/`selectItem()`/`init()` bei einem `401` sonst eine unbehandelte Promise-Ablehnung hinterließen (im Browser nur eine Konsolenwarnung, in Node ein Prozessabbruch — trotzdem sauber behandelt, nicht auf das mildere Browser-Verhalten verlassen) | +4 (2 `test_meta.py`, neue Datei + 2 `test_api.py`: `test_conflict_response_current_item_matches_item_to_json_exactly`, `test_append_endpoint_concatenates_patch_endpoint_replaces`; JS bleibt laut Plan unit-ungetestet, die jsdom-Simulation ist eine Entwicklungshilfe dieser Session, kein Teil der Suite) |
| 11 | UI-Überarbeitung nach Live-Feedback: Navigationsbaum + Übersichtsseite (`GET /api/v1/overview` neu, `GET /api/v1/meta` um `buckets` erweitert, `webui/serializers.py :: overview_row_to_json()`), plastische Bedienelemente + zwei farblich getrennte Editor-Paneele (`app.css` weitgehend neu), Toasts/Dirty-Gating/schließbarer Editor/entfernbare Chips (`app.js`), gestaltete Auth-Seiten (`pages.py` + `app.css`), Passwortwechsel-Dialog für die Block-A-Zeilen 5/6 | 7b | ✅ **vollständig** — **revidiert Plan §4.1 und §4.3** (Nikinger-Entscheidung 2026-08-05, Tabelle im Session-Block; die Plandatei bleibt als 📕-Snapshot unverändert). Schließt elf Live-Meldungen und sechs eigene Funde (F1–F6). Zwei Funde darüber hinaus: ein vierter Ordner **„Erledigt"** (eine `done`-Aufgabe war in der Oberfläche nirgends mehr auffindbar) und **Akzeptanzkriterium 12 war bisher nur halb erfüllt** — Editor/„+"/Anlegen-Dialog standen permanent in `app.html` und waren nur `hidden`; `app.js :: detachable()` hängt sie jetzt wirklich aus dem DOM aus. 51 jsdom-Prüfungen, `ui_smoke.py` 12/12 | +33 (7 `test_overview.py` + 24 `test_pages_markup.py`, zwei neue Dateien; +1 `test_meta.py`, +1 `test_static_routes.py`; `test_invite_enroll.py` und `scripts/ui_smoke.py` mussten ihre Seed-Suchregex auf das neue Klassen-Markup nachziehen, kein neuer Test) |
| 12 | Betrieb: `phase5_ui/scripts/{deploy,rollback,authbackup,restore_auth_check}.sh` + `ui_budget.py`; `phase5_ui/systemd/{sharefyx-authbackup.service,.timer,sharefyx-staging.service}`; `install_units.sh` um drei **optionale** Staging-Platzhalter erweitert; `diagnose.sh` um vier Prüfungen (UI erreichbar, offene UI-Sitzungen, jüngstes Auth-Backup, aktives Release) | 8 | ✅ **gebaut, Live-Teile beim Nikinger** — **löst V10 auf** (Messtabelle im Session-Block, alle fünf Größen im Korridor) und korrigiert eine **V13-Drift in `phase3_edge/`** (dort seit 2026-07-28 als geschlossen dokumentiert und 114 Zeilen weiter unten in derselben Datei noch als offen geführt). Drei dokumentierte Plan-Abweichungen (Health-Gate ohne authentifizierte Probe — Hard Rule 1; dritter Staging-Platzhalter; Platzhalter optional statt Pflicht). Eigener Fund beim echten Probelauf: ein zurückgerolltes Release wäre das nächste Rollback-Ziel gewesen → `*.failed`-Markierung | +21 (15 `test_deploy_scripts.py`, neue Datei; +6 `test_units.py`, darunter `test_every_placeholder_in_every_unit_is_known_to_the_install_script` — allgemeiner als die im Plan genannten) |

---

## Abnahmestand (Plan §6) — Stand 2026-08-05

Die Ergebnisse entstanden über sechs Sessions verteilt, mehrere davon schon in
`SESSIONS_ARCHIVE.md`. Diese Tabelle ist der **eine** Ort, an dem der Gesamtstand steht; sie
wird bei jedem Live-Ergebnis nachgezogen. **Statusregel des Plans: ✅ heißt live-verifiziert,
nicht gebaut. Phase 5 bleibt 🟡, solange eine Zeile offen ist.**

| # | Kriterium | Stand | Beleg |
|---|---|---|---|
| 1 | Einladungslink erzeugt, Konto von null auf aktiv | ✅ | Nikinger live, 2026-08-04 |
| 2 | Einladungslink ein zweites Mal → abgelehnt | ✅ | Nikinger live, 2026-08-05 |
| 3 | TOTP-Seed einmal gezeigt, Authenticator-Code akzeptiert | ✅ | Nikinger live, 2026-08-04 (nach dem `Referrer-Policy`/Origin-Fund) |
| 4 | Recovery-Code ersetzt den TOTP-Code, danach abgelehnt | ✅ | Nikinger live, 2026-08-05 |
| 5 | Passwort im Browser geändert **ohne** `systemctl restart`, neuer Login sofort gültig | ✅ | Nikinger live, 2026-08-05 nach Step 7b — **schließt Betriebsnotiz O1 auch live** |
| 6 | Nach dem Passwortwechsel: Connector fordert neue Autorisierung · andere UI-Sitzung beendet · aktuelle läuft weiter | ✅ | **Nikinger live, 2026-08-05** mit einem privaten Fenster als zweiter Sitzung (ein zweiter Tab teilt das Cookie und beweist nichts). Das private Fenster bekam die „Sitzung abgelaufen"-Karte. **Read-only in der DB gegengeprüft statt den Screenshot zu übernehmen:** 7 × `ui_sessions.revoked_reason='password_changed'`, 7 × `token_families.revoked_reason='password_changed'` (Connector muss neu autorisieren), und 6 × `rotated` — genau P5-Q, die eigene Sitzung wird **rotiert, nicht widerrufen** |
| 7 | Fehlversuchsbremse greift für UI-Login und OAuth-Consent gemeinsam | ✅ | Nikinger live, 2026-08-05 |
| 8 | `authctl.py list-users` zeigt keinen Hash und keinen Seed | ✅ | Nikinger live, 2026-08-05 |
| 9 | `auth.sqlite3` mit `strings`: kein Base32-Seed im Klartext | ✅ | Nikinger live, 2026-08-05 |
| 10 | Anlegen/Bearbeiten/Anhängen/Archivieren über die UI; `.md` im `DATA_ROOT` korrekt **und** Git-Commit existiert | ⬜ offen | UI-Seite funktioniert live; der **Dateinachweis** (`git log` im Datenverzeichnis) steht aus |
| 11 | Konflikt in zwei Tabs → Versionsband `--warn` + Dialog, kein stiller Überschreiber | ✅ | Nikinger live, 2026-08-05 nach Step 7b |
| 12 | Fremder Space sichtbar/lesbar, **ohne** Schreib-Bedienelemente im DOM | ✅ | Nikinger live in DevTools, 2026-08-05 nach Step 7b (vorher nur `hidden` — siehe F7-Umfeld im Session-Block) |
| 13 | Unbekanntes Frontmatter-Feld überlebt eine UI-Bearbeitung unverändert | ⬜ offen | `extra` wird durchgereicht (`serializers.py`), live noch nicht belegt |
| 14 | `format: markdown` erscheint nach dem ersten UI-Schreibvorgang und stört keinen Tool-Aufruf | ⬜ offen | |
| 15 | `ui_budget.py` liefert alle vier Zahlen | 🟡 **Kandidatenbeleg** | Von Claude Code gefahren, Ergebnis steht als Tabelle im Session-Block (alle fünf Größen im Korridor, **löst V10 auf**). Nach dem Muster von P3 Zeile 13 gilt das als Kandidat, nicht als Abnahme — **der Lauf des Nikingers macht die Zeile ✅** |
| 16 | `deploy.sh` rollt bei kaputtem Health-Endpunkt automatisch zurück | ✅ | **Nikinger live, 2026-08-05 20:40**, nach dem Cutover auf `/opt/sharefyx/current`. `SHAREFYX_PORT=9999` zeigte das Gate auf einen toten Port (der Dienst selbst blieb gesund — simuliert wird ein kaputter Health-Endpunkt, nicht ein kaputter Dienst). Read-only gegengeprüft, nicht nur die Meldung übernommen: `current` zeigt wieder aufs erste Release, das gescheiterte liegt als `…Z.failed` daneben, `ExecMainStartTimestamp` passt zum Rollback-Neustart, alle vier Proben und der öffentliche Funnel-Weg wieder korrekt. **Der `.failed`-Fund vom selben Tag in Aktion:** ohne die Markierung wäre genau dieses Verzeichnis beim nächsten Rollback das Ziel gewesen |
| 17 | Beide Nutzer benutzen UI **und** Connector am selben Tag gegen dieselbe Instanz | ⬜ offen | Step 9 (P5-AE) |
| 18 | `git diff` auf `storage/`, `mcpserver/{tools,permissions,server}.py`: leer | ✅ | bei jedem Step-Commit geprüft, zuletzt Step 7b |
| 19 | Cookie an `/mcp` ignoriert; Bearer an `/api` ignoriert | 🟡 | Testseite ✅ (`test_isolation.py`, `test_overview.py`); der im Plan zusätzlich verlangte **Live-`curl`** steht aus |
| 20 | Reboot: UI, Connector, Timer kommen ohne Handgriff zurück | ⬜ offen | passiv zulässig (wie P3 Zeile 6) |

**Kurz:** 13 von 20 live bestanden, 2 teilweise (15, 19), 5 offen. Die zwei „teilweise" sind
allesamt Zeilen, bei denen die Code-Seite fertig ist und nur der Lauf des Nikingers fehlt — das
ist Absicht und keine Nachlässigkeit: **✅ heißt live-verifiziert, nicht gebaut.**

**Cutover auf Release-Verzeichnisse vollzogen (2026-08-05 20:37, Nikinger):** der Dienst läuft
seither aus `/opt/sharefyx/current` statt aus dem Git-Arbeitsverzeichnis. „Datei ändern +
`systemctl restart`" ist damit wirkungslos — es zählt nur noch, was `deploy.sh` gebaut hat.
Rückweg, falls je nötig: `REPO_ROOT`/`VENV` in `phase3_edge/local.env` zurück auf
`/home/savefyx/dev/savefxy` und `install_units.sh` erneut.

---

## Session stopped — 2026-08-05, vierter Nachtrag (Step 8: Deploy, Rollback, Staging, Auth-Backup, Messung)

**Ergebnis:** Step 8 ist gebaut. Bis hierher lief der Dienst direkt aus dem
Git-Arbeitsverzeichnis — ein Editor-Speichern wirkte sofort auf die laufende Instanz, ein
Rollback gab es nicht, und die `auth.sqlite3` (Passwort-Hashes, **umkehrbare** TOTP-Seeds,
Token-Familien) wurde von **keinem** Backup erfasst; gesichert war nur der `DATA_ROOT`. Ein
Plattenschaden hätte die Notizen gerettet und beide Konten gekostet.

Neu: `phase5_ui/scripts/{deploy.sh,rollback.sh,authbackup.sh,restore_auth_check.sh,ui_budget.py}`,
`phase5_ui/systemd/{sharefyx-authbackup.service,.timer,sharefyx-staging.service}`, vier weitere
Prüfungen in `phase3_edge/scripts/diagnose.sh`, drei optionale Platzhalter in
`install_units.sh`.

**Nikinger-Entscheidungen dieser Planung (2026-08-05):** Deploy-Quelle ist das **lokale Repo**,
nicht GitHub („von GitHub klonen nur Leute, die das Projekt selber hosten wollen") — `deploy.sh
origin/main` funktioniert nach einem `git fetch` trotzdem, der Klon bringt die Remote-Refs mit.
Staging wird **jetzt** gebaut, wie in P5-AB gelockt.

**Drei dokumentierte Abweichungen vom Plan-Wortlaut:**
1. **Health-Gate ohne „authentifizierte API-Probe".** Der Plan verlangt eine; eine echte
   Anmeldung bräuchte Passwort **und** TOTP-Seed auf der Platte, und **Hard Rule 1 verbietet das
   ausnahmslos**. Stattdessen vier Proben, die dasselbe beweisen, ohne ein Geheimnis anzulegen:
   `/health` → 200, `/ui/login` → 200 (webui gemountet), `/api/v1/me` ohne Cookie → **401**,
   `/mcp/` ohne Bearer → **401**. Ein Deploy, der versehentlich die Authentisierung ausbaut,
   fällt damit auf — genau darum ging es bei der Forderung.
2. **Drei Staging-Platzhalter statt zwei.** `__STAGING_BASE_URL__` kam dazu, weil
   `SPACE_PUBLIC_BASE_URL` unter `AUTH_MODE=oauth` Pflicht ist (`authserver/config.py`) — mit nur
   Port und `DATA_ROOT` wäre die Unit nicht startfähig gewesen.
3. **Die Staging-Platzhalter sind optional mit Default, nicht Pflicht.** Sonst bräche
   `install_units.sh` auf **jeder bestehenden Installation** ab, sobald die neue Unit dazukommt —
   die `local.env` der VM kennt die Schlüssel ja noch nicht. Defaults: Port `8766`,
   `<DATA_ROOT>-staging`, `<PUBLIC_BASE_URL>:<STAGING_PORT>`.

**Zwei eigene Funde:**
- **Ein zurückgerolltes Release wäre das nächste Rollback-Ziel gewesen.** Aufgefallen erst beim
  echten Probelauf, nicht beim Schreiben: nach einem gescheiterten Health-Gate bleibt das
  Release liegen (gewollt — man will hineinsehen können), ist aber das **jüngste** Verzeichnis.
  Der nächste erfolgreiche Deploy hätte es damit zum „vorherigen" Release gemacht; ein Rollback
  wäre auf genau dem Stand gelandet, der eben nachweislich den Gate gerissen hat. `deploy.sh`
  markiert es jetzt als `*.failed`, `rollback.sh` schließt solche Verzeichnisse aus. Beides mit
  einem Test festgehalten.
- **V13-Drift in `phase3_edge/`.** `phase3_edge/CLAUDE.md` dokumentiert V13 seit dem 2026-07-28
  als geschlossen — und führt es 114 Zeilen weiter unten in derselben Datei noch als offen; der
  `[VERIFY]`-Kommentar in `diagnose.sh` trug dieselbe veraltete Aussage („bei Abweichung in
  Step 7 korrigieren"). Beide Stellen mit datierter Notiz korrigiert. Kein `[VERIFY]` dieser Art
  ist mehr offen.

**Messung (P5-AD) — löst `[VERIFY]` V10 auf.** `ui_budget.py`, 220 synthetische Items,
in-process gegen ein temporäres `DATA_ROOT`:

| Messgröße | Gemessen | Ziel | |
|---|---|---|---|
| `GET /api/v1/items?limit=50` roh | **22.4 KB** | < 64 KB | ✅ |
| `GET /api/v1/items?limit=50` gzip | **1.2 KB** | < 12 KB | ✅ |
| `GET /api/v1/items/{id}` typisch | **0.6 KB** | < 8 KB | ✅ |
| `app.js` + `app.css` + Font | **54.8 KB** | < 250 KB | ✅ (js 14.6 / css 6.3 / Font 33.9) |
| Erstaufruf `/ui/` bis interaktiv | **58.2 KB** | < 400 KB | ✅ |

Alle fünf im Korridor, mit großem Abstand. **Was die letzte Zahl NICHT ist:** ein
Browser-Messwert. Sie summiert, was ein frischer Browser laden muss (`app.html` + statische
Dateien gzip + die drei Bootstrap-Antworten `/api/v1/{me,meta,overview}`, die `init()` in genau
dieser Reihenfolge holt) — ohne Verbindungsaufbau, TLS-Handshake und HTTP-Header. Eine
Nachbildung, ehrlich benannt, keine Labormessung.

**`[SEAM]` Blue/Green (P5-AC), dokumentiert statt gebaut:** `deploy.sh` liest den Zielport aus
**einer** Variablen (`SHAREFYX_PORT`) und benutzt sie an **einer** Stelle (der Health-Gate-URL).
Der spätere Weg wäre eine Template-Unit `sharefyx-mcp@.service` plus Zielwechsel über
`tailscale serve`/`funnel`. **Die Bedingung, unter der das überhaupt sinnvoll wird:** ab dann
müssen alle Schemaänderungen expand/contract-fähig sein, weil zwei Farben dieselbe
`auth.sqlite3`, denselben Index und dasselbe Git-Repo teilen. Solange das nicht gilt, wäre
Blue/Green kein Sicherheitsgewinn, sondern zwei Prozesse, die sich gegenseitig die Daten
umschreiben.

**Verifiziert:** `pytest -q` → **570/570 grün** (549 vorher, +21: 15 `test_deploy_scripts.py`
neu, +6 `test_units.py`). `pyflakes` und `bash -n` über alle neuen/geänderten Dateien sauber.
`deploy.sh`/`rollback.sh` **real gefahren** gegen ein Wegwerf-Layout mit gestubbtem
`systemctl`/`curl` und einem echten kleinen Git-Repo als Quelle — beide Fehlschlagpfade (rote
Tests, gerissener Health-Gate) inklusive Prüfung, wohin der Symlink danach zeigt.
`authbackup.sh`/`restore_auth_check.sh` real gegen eine echte kleine SQLite-Datei (Retention,
`0600`, Zeilenzählung). `install_units.sh` hermetisch gegen eine Wegwerf-Kopie mit umgebogenem
Ziel — alle acht Units ohne unaufgelösten Platzhalter. `git diff --stat` auf `storage/`,
`mcpserver/{tools,permissions,server}.py` bleibt **leer** (Akzeptanzkriterium 18).

Ein Test verdient eine eigene Erwähnung, weil er über die im Plan genannten hinausgeht:
`test_every_placeholder_in_every_unit_is_known_to_the_install_script` prüft **allgemein**, dass
kein `__FOO__` in irgendeiner Unit dem Installationsskript unbekannt ist. Ohne ihn hätte die
nächste Unit mit einem neuen Platzhalter erst beim `sudo install_units.sh` auf der echten
Maschine einen Abbruch erzeugt — und zwar für **alle** Units, nicht nur die neue.

**Advisor:** in dieser Session **nicht erreichbar** („temporarily overloaded", beim Review vor
dem Commit erneut versucht) — anders als in Step 7b, wo er mit F7 den schwersten Fund beisteuerte.
Ersatz: der dokumentierte Fallback (`pytest` + `pyflakes` + `bash -n` + echte Probeläufe aller
Skripte) plus ein gezielter Selbst-Review der riskantesten Stellen, der zwei Dinge ergab, beide
behoben: (1) beim **allerersten** Deploy gibt es kein vorheriges Release, `rollback.sh` bricht
dann korrekt ab — die Meldung sagt jetzt warum, und der Kommentar erklärt, weshalb das kein
Betriebsproblem ist (vor dem Cutover zeigt die Unit noch aufs Arbeitsverzeichnis; genau deshalb
steht der erste Deploy im Runbook **vor** dem Cutover). (2) `test_deploy_script_aborts_when_
tests_fail` scheitert in Wahrheit daran, dass im Wegwerf-Release gar kein `pytest` installiert
ist, nicht an einem absichtlich roten Test — der Docstring behauptete das Gegenteil und sagt es
jetzt geradeheraus. Die Aussage des Tests bleibt gültig: `deploy.sh` unterscheidet nicht zwischen
„Test rot" und „Testlauf nicht durchführbar", und beides muss denselben Abbruch auslösen.

**Nachtrag 2026-08-05, beim ersten echten Deploy des Nikingers — der schwerwiegendste Fund
dieses Steps, und er stammt aus meinem eigenen Testcode:**

Der Deploy brach ab („Tests im Release rot"), das Release wurde gelöscht, der Symlink blieb
unberührt — **das Sicherheitsnetz hat exakt so funktioniert, wie es soll.** Die Ursache dahinter
war aber keine echte Regression:

`test_deploy_scripts.py :: _env()` baute die Testumgebung aus `dict(os.environ)` und setzte nur
die Variablen, die es selbst braucht. Der Nikinger hatte für den Deploy
`SHAREFYX_SYSTEMCTL="sudo systemctl"` **exportiert** — diese Variable rutschte damit in jeden
Testlauf durch. Die Tests bauten also ein `deploy.sh`, das `sudo systemctl restart sharefyx-mcp`
**auf der echten Maschine** aufrief. Das PATH-Stubbing schützt davor nicht: `sudo` findet das
echte Binary über `secure_path`, nicht über den vorangestellten Stub-Pfad. Und weil unmittelbar
vorher ein `sudo -v` gelaufen war, brauchte es nicht einmal ein Terminal.

**Nachgeprüft, nicht vermutet:** `journalctl` zählte im Testfenster **52** Start-/Stop-Zeilen der
Produktiv-Unit. Die Testsuite hat den laufenden Dienst dutzendfach neu gestartet. Folgenlos
(ein Neustart ist harmlos, `/health` und `/ui/login` antworten wieder mit 200), aber es hätte nie
passieren dürfen: dieselbe Regel, die für `DATA_ROOT` und Netz gilt — **nie gegen die Realität** —
gilt für die Prozesssteuerung genauso.

Behoben in **beiden** betroffenen Testdateien über ein gemeinsames `_clean_environ()`, das jede
`SHAREFYX_*`/`SFX_*`-Variable des Aufrufers verwirft:
`phase5_ui/tests/test_deploy_scripts.py` (dort eskaliert) und
`phase3_edge/tests/test_backup_scripts.py` (dieselbe Bauart, dort hätte ein exportiertes
`SHAREFYX_BACKUP_KEEP` die Retention-Tests still verfälscht — vorsorglich mitgeschlossen).
Regressionstest `test_harness_ignores_ambient_sharefyx_configuration` hält fest, dass **nur**
vom Test selbst gesetzte Variablen übrig bleiben. Gegenprobe gefahren: mit exportiertem
`SHAREFYX_SYSTEMCTL`/`SHAREFYX_RELEASES_DIR`/`SHAREFYX_BACKUP_KEEP` waren vorher **3 Tests rot**,
danach alle grün.

**Die allgemeine Lehre, die über diesen Fall hinausgeht:** ein Test, dessen Verhalten von der
Shell des Aufrufers abhängt, ist kein Test. Wenn eine Testsuite ein Programm gegen eine Attrappe
laufen lässt, muss sie die Umgebung **konstruieren**, nicht erben.

**Nachtrag 2026-08-05/06 — Staging live, `[VERIFY]` V36 geschlossen:** der Nikinger hat den
DATA_ROOT geklont, `sharefyx-staging.service` aktiviert und die Instanz über
`sudo tailscale serve --bg --https=8766 8766` freigegeben. **Bewusst mit `sudo` statt
`tailscale set --operator=savefyx`** (Nikinger-Entscheidung): die Serve-Konfiguration überlebt
ohnehin im `tailscaled`-Zustand, ein dauerhaftes Operator-Recht würde dagegen genau dem Benutzer,
unter dem `deploy.sh` läuft, erlauben, den **Produktiv**-Funnel umzustellen oder abzuschalten.
Least privilege vor Bequemlichkeit.

**V36 read-only gegengeprüft:** Funnel steht auf 443 → `127.0.0.1:8765` (öffentlich, unverändert),
Serve auf 8766 → `127.0.0.1:8766` und ist als **`tailnet only`** ausgewiesen — kein gemeinsamer
Port, Staging nie über Funnel (P5-AB). Staging antwortet über den Tailnet-Weg mit 200 auf
`/health` und `/ui/login`, Produktiv unverändert 200.

**Die Falle, die dabei nicht zugeschnappt ist** (und die ich vorher in `local.env.example`
benannt habe): `STAGING_PORT` ist der **lokale** Port, `tailscale serve --https=<X>` bestimmt den,
den der Browser sieht. Der Default `<PUBLIC_BASE_URL>:<STAGING_PORT>` stimmt **nur**, wenn beide
gleich sind. Hier sind sie es (8766/8766), die eingesetzte `SPACE_PUBLIC_BASE_URL` deckt sich
exakt mit der realen Serve-URL. Bei `--https=8443` wäre sie falsch gewesen — und der erste
Einladungslink auf Staging wäre in demselben `403 Herkunft (Origin) stimmt nicht` gelandet, der
in P4 und P5 je eine Session gekostet hat. Deshalb war die Reihenfolge „erst serven, dann
ablesen, dann eintragen" keine Förmlichkeit.

**Nachtrag 2026-08-06 — der erste Staging-Einladungslink führte ins Leere, Ursache zweimal
meine, behoben:** der Nikinger meldete „die Accounts waren noch aktiv, die Einladungslinks haben
beide nicht funktioniert". Read-only nachgesehen statt geraten — und das Gegenteil belegt:
**Staging hatte 0 Nutzer, 0 UI-Sitzungen, 2 unverbrauchte Einladungen und insgesamt 4 Anfragen**;
Produktiv dagegen `niklas`/`fabian` aktiv. Das Journal zeigte den eigentlichen Vorgang wörtlich:
`{"path":"/ui/invite/kktcp…","status":404}` **auf der Produktivinstanz**. Die Einladung war für
die Staging-Datenbank erzeugt, der Link zeigte auf Produktiv. **Die Instanz-Trennung hat also
exakt funktioniert** — nur war das Werkzeug irreführend:

1. Mein Runbook-Befehl setzte nur `STATE_DIRECTORY`. `authctl.py invite` **verlangt** aber
   zusätzlich `SPACE_PUBLIC_BASE_URL` (`authctl.py:94`) — der Nikinger musste die fehlende
   Variable also selbst ergänzen, und der naheliegende Wert ist die Produktiv-URL.
2. `authctl.py invite` schrieb den Token in die Datenbank aus `STATE_DIRECTORY`/`SPACE_AUTH_DB`
   und baute den Link aus `SPACE_PUBLIC_BASE_URL` — **zwischen beiden gab es keinerlei
   Verbindung und keinen Abgleich.** Die Fehlermeldung auf der falschen Instanz lautet
   „Einladung ungültig oder abgelaufen", was sich wie „Konto existiert bereits" liest und in eine
   ganz andere Richtung führt.

Behoben (Nikinger-Anregung): `invite` nennt jetzt auf stderr die **beschriebene Datenbank mit
Kennzeichnung `[PRODUKTIV]`/`[STAGING]`**, die **gebaute Ziel-URL** und eine Prüfaufforderung.
Der Link selbst bleibt allein auf stdout (Hard Rule 7). Bewusst **keine** Heuristik, die aus der
URL auf die Instanz schließt: die Staging-URL enthält das Wort „staging" nicht (sie unterscheidet
sich nur im Port), eine solche Prüfung läge in der Hälfte der Fälle daneben. Das Werkzeug nennt
die Hälfte, die es sicher weiß — welche Datenbank es beschrieben hat — und überlässt den Abgleich
dem Menschen. **Der stärkere Weg wäre**, dass der Dienst seine `SPACE_PUBLIC_BASE_URL` beim Start
in `schema_meta` hinterlegt; dann könnte `authctl` autoritativ widersprechen. Als möglicher
Ausbau notiert, nicht gebaut — das berührt `authserver/store.py`s Startpfad und war für diesen
Nachtrag zu viel.

**Nachtrag 2026-08-06, zweiter Anlauf — „Proxy-Server verweigert die Verbindung" auf Staging:
kein Fehler, sondern die Sicherheitseigenschaft bei der Arbeit.** Der Nikinger bekam die Meldung
im Browser für `…ts.net:8766`. Serverseitig war alles gesund (Dienst `active`, `127.0.0.1:8766`
→ 200, **und der Tailnet-Name `https://…:8766/health` von der VM aus ebenfalls → 200**,
Serve-Konfiguration unverändert, `tailscaled` lauscht auf `100.118.131.68:8766`). Der Server
nahm die Verbindung also an — der Browser kam nie an.

`tailscale status` zeigt die Ursache in einer Zeile: **das Tailnet enthält genau ein Gerät**, die
VM selbst. Keine Peers. Der Windows-Host des Nikingers ist **nicht** Mitglied.

Der Grund, warum das nie auffiel:

| | Weg | Tailnet-Mitgliedschaft nötig? |
|---|---|---|
| Produktiv (443) | `tailscale funnel` → öffentliches Internet | **nein** |
| Staging (8766) | `tailscale serve` → nur Tailnet | **ja** |

Die Produktiv-UI lief immer über den **öffentlichen Funnel**, nie über das Tailnet. Staging ist
per P5-AB bewusst nicht öffentlich — also ist es aus einem Nicht-Tailnet-Browser korrekt
unerreichbar. Firefox' Wortlaut („Proxy-Server verweigert…") ist dabei irreführend; es ist eine
schlicht abgewiesene Verbindung, kein Proxy im Spiel (auf der VM sind weder Proxy-Umgebungs-
variablen noch ein GNOME-Systemproxy gesetzt, und es existiert dort gar kein Firefox-Profil —
der Browser läuft auf einem anderen Rechner).

**Weg zum Zugang:** Tailscale auf dem Windows-Host installieren, mit demselben Konto anmelden.
Bewusst **nicht** die Alternativen: ein SSH-Tunnel bräche die Basis-URL
(`https://…:8766` gegen `http://localhost:8766` → exakt der Origin-Fehler aus P4/P5), und
Staging über Funnel freizugeben verbietet P5-AB — eine Testinstanz gehört nicht ins öffentliche
Internet.

**Damit ist auch der „Zertifikatsfehler" bei Fabians Konto sehr wahrscheinlich erklärt** (Fabians
Gerät ist ebenso wenig im Tailnet) — **aber nicht bewiesen**: der Wortlaut lautete „Zertifikat",
nicht „Verbindung verweigert", und ein TLS-Fehler erreicht den Server nie, es steht also nichts
im Journal. Bleibt als offener, kleiner Punkt stehen, bis er wieder auftritt: exakter Wortlaut
und die URL aus der Adresszeile genügen zur Einordnung.

**Manuell (Nikinger — alles, was Realität berührt):**
1. **Einmalig:** `sudo mkdir -p /opt/sharefyx/releases && sudo chown -R savefyx:savefyx /opt/sharefyx`
2. Erster Deploy aus dem Arbeitsverzeichnis:
   `SHAREFYX_RELEASES_DIR=/opt/sharefyx/releases SHAREFYX_CURRENT_LINK=/opt/sharefyx/current
   phase5_ui/scripts/deploy.sh main`
3. **Cutover:** `REPO_ROOT=/opt/sharefyx/current` und `VENV=/opt/sharefyx/current/.venv` in
   `phase3_edge/local.env`, dann `sudo phase3_edge/scripts/install_units.sh` + Restart.
   **Ab hier ist „Datei ändern + `systemctl restart`" wirkungslos** — es zählt nur noch, was
   deployt wurde. Escape-Hatch, falls nötig: den `current`-Symlink von Hand auf das
   Arbeitsverzeichnis zeigen lassen.
4. **Abnahmezeile 16:** Health-Endpunkt absichtlich unerreichbar machen (`SHAREFYX_PORT` auf
   einen toten Port), deployen, beobachten, dass automatisch zurückgerollt wird.
5. `sudo systemctl enable --now sharefyx-authbackup.timer`, danach `restore_auth_check.sh`
   **selbst ausführen** — der Nachweis ist der Lauf, nicht das Skript (Lehre aus P3 Zeile 13).
6. Staging hochziehen, `tailscale serve` prüfen — **V36:** nicht derselbe Port wie der Funnel.
   Achtung: Staging hat eine **eigene** `auth.sqlite3`, die Produktivkonten gelten dort nicht.
7. Unabhängig von Step 8 weiterhin offen: **Abnahmezeile 6** — zweiter Browser (privates
   Fenster/zweites Profil) angemeldet lassen, Passwort ändern, prüfen dass genau der abgemeldet
   wird und die aktuelle Sitzung weiterläuft.

**Nächster Schritt (konkret):** die sieben Punkte oben, dann Step 9 (gemeinsame Live-Abnahme
beider Nutzer + Handover, Plan §5 Step 9 / P5-AE).
