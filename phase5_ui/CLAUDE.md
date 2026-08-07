---
status: live
purpose: Phase-Head Web-UI, REST-API, Auth-Selbstverwaltung — Scope, harte Regeln, Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase5_ui/ oder an den in P5-B genannten Dateien in authserver/mcpserver — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase5_ui_plan.md             # voller Plan, Entscheidungen P5-A–P5-AE, Steps 0–9
  - ../docs/concepts/PHASE4_CLOSEOUT_HANDOVER.md   # Herkunft der offenen Entscheidungen §4.1–§4.5, [VERIFY]-Bilanz V14–V26
updated: 2026-08-06
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
| 13 | UI-Revision nach Live-Feedback des Nikingers (elf Punkte) + Review von Step 8/S10: OAuth-Consent-Seite gestaltet (`phase4_auth/authserver/{templates,routes}.py`, CSP `style-src`/`font-src` erweitert), Ordner-Wechsel schließt/fragt jetzt bei offenem Editor + Nur-lesen-Ansicht bekommt ein „×" (`app.js :: navigate()`/`showReadonlyItem()`), Anlegen-Dialog-Typ folgt dem aktiven Ordner, Editor öffnet standardmäßig in der Vorschau (zwei Ausnahmen: Neuanlage, Neuladen nach Schreibvorgang), Archivieren vom „×" weggerückt, Abmelden-Icon getauscht, Passwort-Sichtbarkeit (Konto-Dialog + Login-/Einladungsseite, `pages.py` lädt jetzt `app.js`), Zähler-Polling (20s + Fokus/Sichtbarkeit) | 8b (Live-Feedback, kein Plan-Step) | ✅ **vollständig, gebaut und deployt** (2026-08-07) | +2 (`test_templates.py`: einer ersetzt, einer neu); JS bleibt laut Plan unit-ungetestet, 27 jsdom-Prüfungen im Scratchpad (nicht im Repo) gegen die neue Editor-Öffnen-/Navigations-/Toggle-Logik |

---

## Abnahmestand (Plan §6) — Stand 2026-08-07

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
| 10 | Anlegen/Bearbeiten/Anhängen/Archivieren über die UI; `.md` im `DATA_ROOT` korrekt **und** Git-Commit existiert | ✅ | **Nikinger live, 2026-08-07** — vier UI-Aktionen auf `itm_b252a444`, `git log --oneline` im Datenverzeichnis zeigt vier eigene Commits (`create`/`update`/`append`/`archive`), Datei liegt danach korrekt unter `_archive/` |
| 11 | Konflikt in zwei Tabs → Versionsband `--warn` + Dialog, kein stiller Überschreiber | ✅ | Nikinger live, 2026-08-05 nach Step 7b |
| 12 | Fremder Space sichtbar/lesbar, **ohne** Schreib-Bedienelemente im DOM | ✅ | Nikinger live in DevTools, 2026-08-05 nach Step 7b (vorher nur `hidden` — siehe F7-Umfeld im Session-Block) |
| 13 | Unbekanntes Frontmatter-Feld überlebt eine UI-Bearbeitung unverändert | ✅ | **Nikinger live, 2026-08-07** — `custom_test: roundtrip-check` per Hand in `itm_749d6a12`s Frontmatter eingefügt, danach eine UI-Bearbeitung gespeichert; Feld überlebte unverändert. Nebenfund: `version` sprang 3→5 statt 3→4 — kein Bug, `store.py :: _reconcile_and_get_row()` erkannte die externe Änderung, schrieb einen eigenen `drift`-Commit (Version-Repair, Entscheidung D), erst danach kam der `update`-Commit der UI obendrauf; `git log` zeigt beide Commits einzeln |
| 14 | `format: markdown` erscheint nach dem ersten UI-Schreibvorgang und stört keinen Tool-Aufruf | ✅ | Feld war nach der ersten UI-Bearbeitung von `itm_749d6a12` bereits gesetzt; **Claude Code live über den echten MCP-Connector** (`get_item`, Space `niklas`) gegengeprüft — sauberer Read, keine Fehlermeldung, `format: markdown` unverändert im Ergebnis |
| 15 | `ui_budget.py` liefert alle vier Zahlen | ✅ | **Nikinger live, 2026-08-07** (`.venv/bin/python phase5_ui/scripts/ui_budget.py`, nachdem ein bloßes `python3` mit `ModuleNotFoundError: httpx` scheiterte — falscher Interpreter, kein Befund). Alle 5 Messgrößen im Zielkorridor, deckungsgleich mit dem Kandidatenbeleg vom 2026-08-05 |
| 16 | `deploy.sh` rollt bei kaputtem Health-Endpunkt automatisch zurück | ✅ | **Nikinger live, 2026-08-05 20:40**, nach dem Cutover auf `/opt/sharefyx/current`. `SHAREFYX_PORT=9999` zeigte das Gate auf einen toten Port (der Dienst selbst blieb gesund — simuliert wird ein kaputter Health-Endpunkt, nicht ein kaputter Dienst). Read-only gegengeprüft, nicht nur die Meldung übernommen: `current` zeigt wieder aufs erste Release, das gescheiterte liegt als `…Z.failed` daneben, `ExecMainStartTimestamp` passt zum Rollback-Neustart, alle vier Proben und der öffentliche Funnel-Weg wieder korrekt. **Der `.failed`-Fund vom selben Tag in Aktion:** ohne die Markierung wäre genau dieses Verzeichnis beim nächsten Rollback das Ziel gewesen |
| 17 | Beide Nutzer benutzen UI **und** Connector am selben Tag gegen dieselbe Instanz | ⬜ offen | Step 9 (P5-AE) |
| — | *(Staging war kein eigenes Akzeptanzkriterium — P5-AB nennt es im Scope, §6 prüft es nicht. Am 2026-08-06 abgeschaltet, Begründung im Session-Block.)* | | |
| 18 | `git diff` auf `storage/`, `mcpserver/{tools,permissions,server}.py`: leer | ✅ | bei jedem Step-Commit geprüft, zuletzt Step 7b |
| 19 | Cookie an `/mcp` ignoriert; Bearer an `/api` ignoriert | ✅ | Testseite ✅ (`test_isolation.py`, `test_overview.py`) **plus Nikinger live, 2026-08-07**: `curl` gegen `PUBLIC_BASE_URL` (aus `phase3_edge/local.env`) — `GET /api/v1/me` ohne Cookie/Bearer → `401`; `GET /mcp/` mit gefälschtem `__Host-sfx_session`-Cookie (kein Bearer) → `401` |
| 20 | Reboot: UI, Connector, Timer kommen ohne Handgriff zurück | ⬜ offen | passiv zulässig (wie P3 Zeile 6) |

**Kurz:** 18 von 20 live bestanden, 0 teilweise, 2 offen (17, 20). Zeilen 10/13/14/15/19 sind am
2026-08-07 den Sprung von „Code fertig" auf „Nikinger live" gegangen — **✅ heißt
live-verifiziert, nicht gebaut.** Von den zwei verbleibenden braucht 17 Fabian (Step 9), 20 ist
passiv (nächster echter Reboot oder ein bewusst ausgelöster).

**Cutover auf Release-Verzeichnisse vollzogen (2026-08-05 20:37, Nikinger):** der Dienst läuft
seither aus `/opt/sharefyx/current` statt aus dem Git-Arbeitsverzeichnis. „Datei ändern +
`systemctl restart`" ist damit wirkungslos — es zählt nur noch, was `deploy.sh` gebaut hat.
Rückweg, falls je nötig: `REPO_ROOT`/`VENV` in `phase3_edge/local.env` zurück auf
`/home/savefyx/dev/savefxy` und `install_units.sh` erneut.

---

## Session stopped — 2026-08-06 (Verifikationssession: Push bestätigt, Deploy-Lücke quantifiziert)

**Auftrag:** Sanity-Check des einen offenen Punkts aus dem letzten Handover — die Behauptung
„Dienst läuft seit dem Step-8-Cutover aus `/opt/sharefyx/current`" —, plus generelle Orientierung
zu Sessionbeginn. Kein Code angefasst, keine Live-Aktion ausgeführt (nur read-only).

**Cutover-Behauptung live gegengeprüft, nicht nur übernommen:** `systemctl cat sharefyx-mcp` →
`WorkingDirectory=/opt/sharefyx/current`, `ExecStart=/opt/sharefyx/current/.venv/bin/python
/opt/sharefyx/current/phase2_mcp/scripts/serve.py`. Bestätigt.

**Korrektur einer veralteten Behauptung im vorigen Session-Block:** dort steht „lokaler `main`
liegt 34 Commits vor `origin/main`, nie gepusht". `git status -sb` → `main...origin/main`
(0 Commits Differenz in beide Richtungen) — **der Push ist inzwischen erfolgt** (vom Nikinger,
außerhalb dieser Session). Root-`CLAUDE.md`s identische Behauptung trägt dieselbe Korrektur.

**Deploy-Lücke präzise quantifiziert statt nur „Deploy fällig" zu wiederholen:**
`/opt/sharefyx/current` → `readlink -f` → `/opt/sharefyx/releases/20260805T183144.605094Z` →
dort `git log` → `HEAD` = `6bf22e5`. `git log --oneline 6bf22e5..HEAD` (lokal) zeigt **12
Commits**, darunter genau die drei, die der vorige Session-Block als „erst nach Deploy sichtbar"
benannt hatte: den S10-Fix (`e760f0e`), Step 8b (`2237c0f`) und die F1/F2-Entscheidung
(`8b11862`). Deploy bleibt Sache des Nikingers (Hard Rule: reale Infrastruktur).

**Kein eigenständig ausführbarer Schritt gefunden:** Abnahmematrix (`phase5_ui/CLAUDE.md`
§„Abnahmestand") erneut gegen die Session-Notiz geprüft — alle sieben nicht-✅-Zeilen (10, 13,
14, 15, 17, 19, 20) sind entweder Kandidatenbeleg (15, bereits von Claude Code gefahren, braucht
den Lauf des Nikingers) oder verlangen laut eigenem „Beleg"-Feld explizit einen Live-Vorgang
(Browser-Nutzung, `curl`, Reboot, Step 9 mit Fabian). Kein Widerspruch zwischen Root-`CLAUDE.md`s
„Nächster Schritt: Zeile 15/19/Step 9" und diesem Head — Abnahme-*Zeilen* sind keine Plan-*Steps*,
aber beide landen am selben Ort: beim Nikinger.

**Verifiziert:** keine Testsuite gelaufen (kein Code geändert, `pytest`/`ui_budget.py` also nicht
nötig — beide würden ohnehin eine bereinigte Shell-Umgebung brauchen,
[[feedback_test_harness_never_inherits_env]]). Tabu-Diff nicht relevant (kein Diff).

**Nachtrag, 2026-08-07 — Deploy + Zeilen 15/19 vom Nikinger live erledigt:**
`SHAREFYX_RELEASES_DIR=/opt/sharefyx/releases SHAREFYX_CURRENT_LINK=/opt/sharefyx/current
SHAREFYX_DATA_ROOT=/home/savefyx/savefyx-data SHAREFYX_BACKUP_DIR=/var/lib/sharefyx-backup
phase5_ui/scripts/deploy.sh main` lief durch (576/576 Tests im Release, Health-Gate `/ui/login`→
`200`, `/api/v1/me`→`401`, `/mcp/`→`401`), JSON-Zeile bestätigt `"result":"ok"`,
`"sha":"a835d1d..."`. Read-only gegengeprüft, nicht nur die Meldung übernommen: `readlink -f
/opt/sharefyx/current` → neues Release-Verzeichnis, `git log --oneline -1` darin → `a835d1d`,
identisch mit dem lokalen `main`-HEAD zum Deploy-Zeitpunkt. **Deploy-Lücke damit geschlossen.**
Zeile 15: `ui_budget.py` scheiterte beim ersten Versuch mit bloßem `python3`
(`ModuleNotFoundError: httpx`) — falscher Interpreter, kein Befund; mit `.venv/bin/python`
liefen alle 5 Messgrößen im Korridor, deckungsgleich mit dem Kandidatenbeleg. Zeile 19: `curl`
gegen `PUBLIC_BASE_URL` (`phase3_edge/local.env`) — `/api/v1/me` ohne Auth → `401`, `/mcp/` mit
gefälschtem Session-Cookie statt Bearer → `401`. **Abnahmestand jetzt 15/20, 0 teilweise.**
Beide Zeilen in der Tabelle oben nachgezogen.

**Nachtrag, 2026-08-07, zweiter — Zeilen 10/13/14 vom Nikinger live erledigt:**
Zeile 10: vier UI-Aktionen (Anlegen/Bearbeiten/Anhängen/Archivieren) auf `itm_b252a444`,
`git log` im `DATA_ROOT` zeigt vier eigene Commits, je einen pro Aktion (Hard Rule 5 hält unter
echter Nutzung). Zeile 13: unbekanntes Frontmatter-Feld (`custom_test: roundtrip-check`) von
Hand eingefügt, überlebte danach unverändert eine echte UI-Bearbeitung — Nebenfund dabei: die
Version sprang zwei statt eins, weil `store.py`s Drift-Erkennung (Entscheidung D) die externe
Änderung zuerst mit einem eigenen `drift`-Commit reparierte, bevor der `update`-Commit der UI
folgte — kein Bug, dokumentiertes Verhalten, per `git log` einzeln nachvollzogen. Zeile 14: `Claude
Code` selbst rief `get_item` über den echten, produktiven MCP-Connector (Space `niklas`) auf das
Testitem auf — sauberer Read trotz `format: markdown`-Feld. **Abnahmestand jetzt 18/20, nur noch
17 (Step 9) und 20 (Reboot) offen.**

**Nebenfund dieser Session — nicht sicherheitsrelevant, aber ungeklärt bis eben:** der
`get_item`-Aufruf oben lief über einen `claude_ai_`-präfigierten Connector-Tool-Namen, der laut
Claude Code auf einen in eurem Anthropic-Account konfigurierten Custom Connector zeigt (dieselbe
Autorisierung wie ein claude.ai-Web-/Desktop-Zugriff — der OAuth-Bearer unterscheidet laut Design
nicht *welche* Claude-Oberfläche ihn benutzt, nur *welcher Space*). Bisher nie bewusst
entschieden, nur nie aufgefallen. Nikinger-Entscheidung 2026-08-07: **kein Ausschluss** — sobald
Unterordner/teambezogene Notizen existieren (siehe Befund F1, vorige Session), gibt es keinen
Nachteil darin, dass auch Claude Code darauf schreiben kann. **Für später vorgemerkt, kein
Blocker, kein Scope für diese Phase:** ein Log-Feld, das festhält, *welche* Client-Oberfläche
(claude.ai/Desktop vs. Claude Code) einen Request gestellt hat — muss nicht in die UI, reicht im
Log. Naheliegender Ort bei Umsetzung: derselbe Request-Log-Pfad, der schon Bearer-Requests
protokolliert (`phase2_mcp/mcpserver`, `test_request_log.py`) — vermutlich über den
`User-Agent`-Header, falls MCP-Clients den zuverlässig genug setzen; das ist bei Umsetzung zu
verifizieren, nicht heute. Phase-6-Kandidat, gemeinsam mit F1/F2 zu betrachten.

**Offen für die nächste Session:**
- Zwei Zeilen offen: 17 (Step 9, braucht Fabian + Nikinger gemeinsam), 20 (passiver
  Reboot-Nachweis wie P3 Zeile 6 — kann jederzeit nebenbei fallen, erzwungen oder natürlich).
- Step 9 (P5-AE) ist der einzige verbleibende Plan-Step — braucht Fabian + Nikinger live,
  nichts, das eine Session ohne beide vorwegnehmen kann.
- Phase-6-Vormerkung (siehe Nebenfund oben): Client-Surface-Logging, zusammen mit F1/F2 zu
  planen, nicht isoliert.
