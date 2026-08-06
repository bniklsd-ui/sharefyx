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
| 13 | UI-Revision nach Live-Feedback des Nikingers (elf Punkte) + Review von Step 8/S10: OAuth-Consent-Seite gestaltet (`phase4_auth/authserver/{templates,routes}.py`, CSP `style-src`/`font-src` erweitert), Ordner-Wechsel schließt/fragt jetzt bei offenem Editor + Nur-lesen-Ansicht bekommt ein „×" (`app.js :: navigate()`/`showReadonlyItem()`), Anlegen-Dialog-Typ folgt dem aktiven Ordner, Editor öffnet standardmäßig in der Vorschau (zwei Ausnahmen: Neuanlage, Neuladen nach Schreibvorgang), Archivieren vom „×" weggerückt, Abmelden-Icon getauscht, Passwort-Sichtbarkeit (Konto-Dialog + Login-/Einladungsseite, `pages.py` lädt jetzt `app.js`), Zähler-Polling (20s + Fokus/Sichtbarkeit) | 8b (Live-Feedback, kein Plan-Step) | ✅ **vollständig, gebaut — Deploy steht noch aus** | +2 (`test_templates.py`: einer ersetzt, einer neu); JS bleibt laut Plan unit-ungetestet, 27 jsdom-Prüfungen im Scratchpad (nicht im Repo) gegen die neue Editor-Öffnen-/Navigations-/Toggle-Logik |

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
| — | *(Staging war kein eigenes Akzeptanzkriterium — P5-AB nennt es im Scope, §6 prüft es nicht. Am 2026-08-06 abgeschaltet, Begründung im Session-Block.)* | | |
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

## Session stopped — 2026-08-06 (Step 8b — Review + elf Live-Feedback-Punkte, zwei Befunde für den Nikinger)

**Auftrag:** „Step 8 ist fertig, aber nicht commited" prüfen, Sicherheits-/Korrektheits-Review,
dann so viel wie machbar aus einer Liste von elf Live-Meldungen des Nikingers umsetzen.

**Erste Korrektur, bevor irgendetwas gebaut wurde:** die Prämisse „nicht commited" stimmte
nicht — `git log` zeigte den S10-Abschluss-Commit bereits als `HEAD` (`e760f0e`), Arbeitsbaum
sauber. Tatsächlicher Zustand, per `git fetch`/`git status -sb` belegt: **lokaler `main` liegt
34 Commits vor `origin/main`, noch nie gepusht** — und `/opt/sharefyx/current` läuft auf dem
Stand VOR dem S10-Fix (Deploy fällig, siehe voriger Session-Block). Zwei getrennte, beide beim
Nikinger liegende Schritte: **Push** und **Deploy**, nicht einer. Diese Session hat keins von
beiden ausgeführt (Hard Rule: was die reale Infrastruktur anfasst, macht der Nikinger).
**Wichtig für den Nikinger: jede Änderung dieser Session ist erst nach einem Deploy sichtbar** —
dieselbe Falle wie O1/S10 in den vorigen zwei Sessions.

**Review Step 8 + S10 (vor jeder Änderung):** `deploy.sh`/`rollback.sh`/`authbackup.sh` erneut
gelesen (nicht nur die Doku übernommen) — Health-Gate, `*.failed`-Markierung, Pre-Deploy-Backup,
`sqlite3 .backup`+Verifikation, alles wie dokumentiert. **`restore_auth_check.sh` war beim
letzten Review nicht gelesen worden** (Lücke dieser Session behoben) — trägt dieselbe
`mktemp -d`+`trap … EXIT`-Disziplin wie `authbackup.sh`, kein Klartext bleibt liegen. S10-Fix
(`routes_auth.py :: _invite_post()`) noch einmal nachvollzogen: `revoke_families_for_space()`/
`revoke_sessions_for_space()` rufen exakt dieselben, bereits seit P5-Q bestehenden Store-Methoden
auf, kein neuer Codepfad. **Keine neuen Sicherheitsbefunde.**

**Elf Live-Meldungen — neun umgesetzt, zwei als eigenständige Befunde für den Nikinger vorgelegt
statt stillschweigend entschieden oder verworfen:**

| # | Meldung | Ergebnis |
|---|---|---|
| 1 | Notiz lässt sich nach Space-Wechsel nicht schließen | ✅ Zwei Ursachen, beide behoben: die Nur-lesen-Ansicht (fremder Space) hatte **kein** „×" (Editor hatte eins) — jetzt `#ro-close-button`. Und ein Ordner-Klick im Baum ließ einen offen gebliebenen, ungespeicherten Editor unangetastet stehen, ohne Rückfrage — `navigate()`s Aufrufer im Baum ruft jetzt erst `closeEditor()` (fragt bei ungespeicherten Änderungen, Entwurf bleibt im `sessionStorage` erhalten), Abbrechen lässt den Editor unverändert stehen |
| 2 | SubSpaces/Unterordner für fabi/niklas | 🔴 **Nicht umgesetzt — Befund F1 unten, Phase-6-Kandidat** |
| 3 | „Task anlegen" zeigt „Notiz" | ✅ War kein reiner Beschriftungsfehler: `openCreateDialog()` selektierte nie etwas vor, das erste `<option>` (immer `note`, alphabetisch/Insertion-Order) blieb stehen — im „Offen"/„Erledigt"-Ordner (Typ `task`) legte „Anlegen" also immer eine Notiz an, unabhängig vom Klick. Jetzt: Vorauswahl folgt `state.meta.buckets[state.filter].type`. Dieselbe Ursache traf den „Erste Notiz anlegen"-Knopf im Leerzustand, jetzt ebenfalls ordner-abhängig |
| 4 | Zähler geht nicht hoch, ohne wegzuklicken | ✅ Polling auf `GET /api/v1/overview` (bereits vorhanden), alle 20s + sofort bei Tab-Fokus/-Sichtbarkeit. **Kein Realtime/WebSocket** (Plan §0.5 draußen) — reines Nachfragen einer bestehenden Route, rührt den Editor nie an |
| 5 | Items vollständig löschen | 🔴 **Nicht umgesetzt — Befund F2 unten** |
| 6 | „später": Space, den nur der User beschreiben kann, Claude nicht | ⬜ Bewusst vom Nikinger selbst verschoben, hier nur protokolliert — keine Aktion |
| 7 | Alte UI beim Connector-Neuanmelden | ✅ Root Cause: `authserver/templates.py`s `render_login_form()` war seit P4 das rohe Wegwerf-Formular — der Docstring sagte „wird in P5 ersetzt", P5-G verbietet aber genau das (getrennter Consent-Flow als Absicht). Nie nachgezogen. Jetzt: `.auth`/`.auth-card`-Kartendesign aus `app.css` wiederverwendet (`<link>`, kein Python-Import, P4-A bleibt intakt), `_security_headers()`s CSP von `style-src 'unsafe-inline'` (ohne `'self'` — ein `<link>` wäre geblockt worden, dieselbe Fehlerklasse wie der `style=`-Fund hinter dem QR-Code in Step 7b) auf `style-src 'self'; font-src 'self'` umgestellt. Bewusst **kein** `<script>` auf dieser Seite (sicherheitskritischer als `webui`, P5-G) |
| 8 | Passwort-Sichtbarkeit beim Eintippen | ✅ `.pw-field`/`.pw-toggle` + `app.js :: initPasswordToggles()` (läuft unbedingt, nicht nur in `initShell()`). Konto-Dialog (3 Felder) sowie Login-/Einladungsseite (`pages.py` lädt jetzt `app.js`, reine Fortschreitung — ohne JS bleibt das Feld maskiert, das native Formular funktioniert unverändert) |
| 9 | Archivieren zu nah am „×" | ✅ Reihenfolge getauscht (Archivieren jetzt am anderen Ende der Leiste) + `.editor__close-button { margin-left: … }` als zusätzlicher Abstand |
| 10 | Shared Spaces ersetzen den Standard-eigenen-Space | 🔴 **Nicht umgesetzt — Befund F1 unten (mit #2 zusammengefasst), zwei Teilfragen** |
| 11 | Editor öffnet standardmäßig in „Bearbeiten", soll „Vorschau" sein | ✅ `showEditableItem(item, opts)` — Vorgabe jetzt `preview`. Zwei Fallen (Advisor-Fund, vor dem Commit behoben): ein frisch angelegtes Item hat leeren Body, öffnet deshalb explizit mit `opts.mode:"edit"` (sonst leere Vorschau statt Textarea); ein Neuladen nach Speichern/Anhängen/Konflikt-„Aktuelle laden" behält den Modus bei, den man gerade benutzt hat (`afterWrite()`/`conflictLoadCurrentButtonEl` reichen `state.mode` durch), sonst risse ein `Ctrl+S` mitten im Tippen in die Vorschau |
| — | Anderes Icon für Abmelden | ✅ `&#9211;` (Ein/Aus, zu nah am `&#9881;`-Zahnrad direkt daneben) → `&#9099;` (⎋, ISO-7000-Abmelde-Symbol) |

**Bewusste Lücke bei Meldung 1, nicht übersehen:** nur `renderFolders()`s Klick-Handler (Baum)
ruft jetzt `closeEditor()` vor der Navigation. `selectItem()` (Listenzeilen, Pfeiltasten) und
`openFromOverview()` wechseln weiterhin OHNE Rückfrage direkt zum nächsten Item — bewusst nicht
mitgezogen: der Entwurf bleibt in jedem Fall im `sessionStorage` erhalten (kein permanenter
Verlust), und das war nicht die Meldung des Nikingers. Sollte sich das als zu leichtfertig
erweisen, ist `closeEditor()` bereits die richtige Stelle zum Nachziehen.

**Akzeptanzkriterium 12 gegengeprüft, nicht nur angenommen:** `#ro-close-button` sitzt in
`#detail-readonly`, außerhalb des `#detail-editor`-Teilbaums, den
`test_write_controls_live_inside_detachable_containers` prüft — er schreibt nichts (nur
`clearDetail()`) und ist ohnehin kein „Schreib-Bedienelement" im Sinne des Kriteriums. Zeile 12
der Abnahmematrix bleibt unverändert ✅.

**Advisor-Fund vor dem Commit, der schwerwiegendste dieser Session:** `pages.py`s `_PAGE` lädt
seit Meldung 8 (Passwort-Sichtbarkeit) `app.js` auf JEDER servergerenderten Seite — auch auf
`render_enrollment_page()` (TOTP-Seed/QR) und `render_recovery_codes_page()` (zehn
Recovery-Codes), die BEIDE selbst ein `name="csrf"`-Feld tragen (fürs Logout-Formular). `app.js`s
Bootstrap-Funktion (`bootstrapCsrf()`) suchte bis dahin nach JEDEM `input[name="csrf"]` außerhalb
von `/ui/` und leitete sofort nach `/ui/` weiter — das hätte auf beiden Seiten ausgelöst und wäre
von einem Geheimnis weggenavigiert, das nur EIN einziges Mal gezeigt wird, bevor ein Mensch den
QR-Code fotografieren bzw. die Codes abschreiben konnte. Nie live beobachtet, vom Advisor vor dem
Commit gefunden. Behoben: `render_logged_in_page()`s Feld trägt jetzt zusätzlich
`id="bootstrap-csrf"`, `bootstrapCsrf()` sucht gezielt danach. Mit Playwright/Chromium
(Scratchpad, temporäre Installation, nicht im Repo) gegen echte, gerenderte `pages.py`-Ausgaben
gegengeprüft: kein Redirect auf Enrollment-/Recovery-Seite, Redirect weiterhin korrekt auf der
Bootstrap-Seite. Dieselbe Session nutzte Playwright zusätzlich für einen echten
Browser-Screenshot der Passwort-Sichtbarkeit (Login, Konto-Dialog) und des Editors (Vorschau-
Vorgabe, Archivieren/Speichern/×-Reihenfolge) gegen einen temporären Dev-Server (tmp DATA_ROOT,
tmp Auth-DB, Fake-DEK — nie die echte Infrastruktur) — alles wie im Code erwartet, keine
CSS-Kaskaden-Überraschung (dieselbe Fehlerklasse, die dieses Projekt beim `style=`-QR-Hintergrund
und dem `no-referrer`-Origin-Fund schon zweimal getroffen hat).

**Befund F1 (SubSpaces + Shared Spaces, zusammengefasst — Meldungen #2 und #10 sind dieselbe
Idee aus zwei Blickwinkeln):** nicht umgesetzt, **zwei unabhängige Teilentscheidungen** für den
Nikinger, keine gemeinsame:
  - **F1a — eigener Space standardmäßig nur für den User + dessen eigene Connectoren lesbar**
    (nicht mehr „von jedem"): eine **Verschärfung** der Default-Leserechte. Fasst
    `mcpserver/permissions.py` an (P5-B tabu für diese Phase), verletzt aber **keine** Hard Rule
    — Rule 4 verbietet Cross-Space-*Writes*, nicht das Verengen von Reads. Vertretbar als eigener,
    kleiner Schnitt.
  - **F1b — ein „shared Space", in dem alle unabhängig volle Rechte haben** (bzw. einzelne
    Dateien/Unterordner mit „shared"-Markierung): kollidiert **frontal** mit Hard Rule 4
    („Fremde Spaces sind read-only … Cross-Space-Writes existieren architektonisch nicht — kein
    Parameter, keine Codepfad-Variante", **„no exceptions"**), fasst `tools.py`+`permissions.py`
    an (beide P5-B tabu, Akzeptanzkriterium 18 verlangt dort einen leeren Diff) und ändert das
    Vertrauensmodell, auf dem `<untrusted_content>` beruht. **Phase-6-Kandidat, keine
    Ad-hoc-Umsetzung.**
  - Echte Unterordner (Meldung #2, unabhängig von Rechten gedacht) sind mit Tags **nicht**
    sauber nachbaubar — ein Tag hat keine eigene Identität, „Anlegen" eines leeren Ordners
    ergibt damit keinen Sinn, und sobald Ordner potenziell Rechtegrenzen tragen sollen (F1b),
    ist ihr natürlicher Ort ein echtes Verzeichnis in `storage/` — ebenfalls tabu. Eine
    Tag-basierte Notlösung jetzt wäre wahrscheinlich Wegwerfarbeit vor F1b.

**Befund F2 (vollständiges Löschen):** nicht umgesetzt, zweifach blockiert — Plan §0.5 nennt
„Löschen (bleibt `status: archived`)" wörtlich unter DRAUSSEN, und `storage.store.Store` hat
keine Lösch-Methode; sie zu bauen hieße `storage/` anzufassen (P5-B tabu). Keine Ad-hoc-Lösung.

**Verifiziert:** `pytest -q` → **576/576** (+1: `test_templates.py`s „kein `<link>`"-Test ersetzt
durch einen, der den `<link>` bewusst erwartet — dieselbe Kategorie Test-Revision wie frühere
gelockte-Entscheidung-Revisionen, dokumentiert statt still geändert). `scripts/ui_smoke.py` →
12/12. Tabu-Diff (`storage/`, `mcpserver/{tools,permissions,server}.py`) → leer.
`test_webui_imports_exactly_one_mcpserver_symbol` weiterhin grün. Zusätzlich: 27 jsdom-Prüfungen
in einem Scratchpad-Harness (nicht im Repo, gleiche Praxis wie Step 7/7b) gegen die neue
Editor-Öffnen-/Navigations-/Passwort-Toggle-Logik — insbesondere den Abbrechen/Bestätigen-Zyklus
beim Ordner-Wechsel mit ungespeichertem Editor, den kein Python-Test erreichen kann.

**Revidierter Test, dokumentiert statt still geändert:** `phase4_auth/tests/test_templates.py ::
test_login_form_has_no_javascript_no_stylesheet_no_cookie_hint` pinnte „kein `<link>`" als
Absicht (Phase-4-Ära, vor P5-G). Umbenannt/gesplittet in
`test_login_form_has_no_javascript_no_cookie_hint` (Rest unverändert) +
`test_login_form_loads_the_shared_stylesheet_via_link_not_inline_style` (neu, erwartet den
`<link>`) — dieselbe Handhabung wie die §4.1/§4.3-Revisionen in Step 7b: Plan-/Test-Snapshot
bleibt historisch stehen, der Code + die lebende Doku ziehen nach, mit datierter Begründung.

**Offen für die nächste Session:**
- **Push UND Deploy stehen beide aus** (siehe oben) — beides Sache des Nikingers.
- **F1/F2 entschieden (Nikinger, 2026-08-06):** F1a/F1b (Subspaces/Shared Spaces) sowie eine
  Archiv-Neugestaltung (Gruppierung nach Datum/Thema für einen „aufgeräumten" Eindruck, als
  Antwort auf F2) sind beide **auf eine spätere Phase verschoben**. F2 selbst bleibt bei „kein
  Löschen, nur Archivieren" — keine Ad-hoc-Umsetzung.
- **Klarstellung des Nikingers zu Testpraxis/`/opt/sharefyx`:** Langzeittests laufen gegen den
  echten `sharefyx-mcp`-Dienst (kein separates Staging — bewusst so entschieden, s.o.),
  Nachtests direkt nach einer Entwicklungssession laufen in einer Wegwerfinstanz (wie in dieser
  Session) — Tailscale lässt sich auf den Arbeitslaptops (den Hauptzugriffsgeräten für die UI)
  nicht installieren. Laut Step-8-Cutover läuft der Dienst seit 2026-08-05 aus
  `/opt/sharefyx/current`, nicht mehr aus dem Git-Arbeitsverzeichnis — nur als Referenz notiert,
  falls das der nächsten Session widerspricht, ist das ein Befund, keine stille Übernahme.
- Kein weiterer Plan-Step ist eigenständig ausführbar: Step 9 (P5-AE, gemeinsame Live-Abnahme)
  braucht Fabian und den Nikinger live — nichts, das diese Session vorwegnehmen konnte.
- Fabians neun alte Token-Familien (voriger Session-Block) und O2 bleiben unverändert offen.
