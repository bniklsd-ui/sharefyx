---
status: live
purpose: Phase-Head Web-UI, REST-API, Auth-Selbstverwaltung — Scope, harte Regeln, Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase5_ui/ oder an den in P5-B genannten Dateien in authserver/mcpserver — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase5_ui_plan.md             # voller Plan, Entscheidungen P5-A–P5-AE, Steps 0–9
  - ../docs/concepts/PHASE4_CLOSEOUT_HANDOVER.md   # Herkunft der offenen Entscheidungen §4.1–§4.5, [VERIFY]-Bilanz V14–V26
  - ABNAHME_MATRIX_ARCHIVE.md                     # §Abnahmestand, 20 Zeilen mit Belegen, verbatim rotiert 2026-10-02
updated: 2026-10-02 (**§Abnahmestand rotiert** — Gate/Z-Doku-Pflege P9-L: 99 Zeilen / 12.195 B wandern **verbatim** nach `ABNAHME_MATRIX_ARCHIVE.md` (neu, L3, mit L1-Card), inkl. der Kurzfassung, der beiden späteren Nachträge (2026-08-13-Korrektur, 2026-10-02 trace-Block) und der Cutover-Notiz; der Head behält Stand + Zeiger und **20/20 ✅, Phase 5 ✅** wörtlich. **Nichts gestrichen**, Roundtrip-Gegenprobe vor dem Schreiben. **43.801 B ~33 KB**, damit unter dem 40-KiB-Softcap. Reiner Doku-Schritt, kein Code-Touch) | 2026-08-13 (Nikinger-Feedback: Versionsnummer neben der Wortmarke, kosmetisch, keine Tests)
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
| 9 | UI-Gerüst: `webui/static_routes.py` (`GET /ui/` sitzungsgated, `GET /ui/static/{path}`), `webui/static/{app.html,app.css,app.js,fonts/}`, `webui/config.py :: UiSettings.static_dir`, `scripts/build_font_subset.sh` (echte Inter-Variable-Subsetting-Pipeline, schließt V31 — **[2026-08-09 Korrektur, Closeout-Session]:** hier ursprünglich fälschlich als „V27" bezeichnet, das ist tatsächlich `permissions.py`s Klassennamen aus Step 5, siehe `phase5_ui_plan.md` §8), `mcpserver/app.py` mountet `static_routes()` | 6 | ✅ **vollständig** — Navigation/Liste/Suche/schreibgeschützte Detailansicht gegen die echte REST-API aus Step 5; **kein** Editor, **kein** Markdown-Rendering, **kein** Versionsband (bewusst Step-7-Scope). Korrigiert einen Plan-Selbstwiderspruch (§1.5-Tabelle „`/ui/` Auth: keine" vs. der im selben Plan-Abschnitt verlangte Testname `test_index_route_requires_session`) zugunsten des Tests, Details im Session-Block unten | +8 (7 `test_static_routes.py`, neue Datei; `phase2_mcp/tests/test_app.py` +1 `test_ui_index_route_reachable_through_create_app`; JS bleibt laut Plan unit-ungetestet) |
| 10 | Editor, Vorschau, Konflikt, Frontmatter-Felder: `webui/api.py` +`GET /api/v1/meta`; `webui/static/app.js` um Markdown-Parser/Sanitizer (geerntet + erweitert aus `docs/concepts/notiz_heft_example.html`), Editor-Zustand, Versionsband, Speichern/Konfliktdialog, Anlegen/Anhängen/Archivieren, Frontmatter-Felder, Entwurfsschutz, „Sitzung abgelaufen"-Karte, Formatierhilfen-Leiste erweitert; `webui/static/{app.css,app.html}` entsprechend erweitert | 7 | ✅ **vollständig** — kein Passwortänderungsdialog (eigener Nachtrag, Zeilen 5/6 der Block-A-Abnahme folgen dort), kein Deploy/Rollback (Step 8), keine zweite Formatvariante (P5-Z bleibt Seam). Umfangreiche Node/jsdom-gestützte End-to-End-Simulation (Scratchpad, nicht im Repo) fand und schloss zwei echte Funde vor dem Commit: (1) das Test-Mock selbst hatte einen `includes()`-Bug (`/api/v1/meta` matchte fälschlich auch `/api/v1/me`) — beim Beheben zusätzlich `reportUnexpectedError()` in `app.js` ergänzt, weil (2) `loadItems()`/`selectItem()`/`init()` bei einem `401` sonst eine unbehandelte Promise-Ablehnung hinterließen (im Browser nur eine Konsolenwarnung, in Node ein Prozessabbruch — trotzdem sauber behandelt, nicht auf das mildere Browser-Verhalten verlassen) | +4 (2 `test_meta.py`, neue Datei + 2 `test_api.py`: `test_conflict_response_current_item_matches_item_to_json_exactly`, `test_append_endpoint_concatenates_patch_endpoint_replaces`; JS bleibt laut Plan unit-ungetestet, die jsdom-Simulation ist eine Entwicklungshilfe dieser Session, kein Teil der Suite) |
| 11 | UI-Überarbeitung nach Live-Feedback: Navigationsbaum + Übersichtsseite (`GET /api/v1/overview` neu, `GET /api/v1/meta` um `buckets` erweitert, `webui/serializers.py :: overview_row_to_json()`), plastische Bedienelemente + zwei farblich getrennte Editor-Paneele (`app.css` weitgehend neu), Toasts/Dirty-Gating/schließbarer Editor/entfernbare Chips (`app.js`), gestaltete Auth-Seiten (`pages.py` + `app.css`), Passwortwechsel-Dialog für die Block-A-Zeilen 5/6 | 7b | ✅ **vollständig** — **revidiert Plan §4.1 und §4.3** (Nikinger-Entscheidung 2026-08-05, Tabelle im Session-Block; die Plandatei bleibt als 📕-Snapshot unverändert). Schließt elf Live-Meldungen und sechs eigene Funde (F1–F6). Zwei Funde darüber hinaus: ein vierter Ordner **„Erledigt"** (eine `done`-Aufgabe war in der Oberfläche nirgends mehr auffindbar) und **Akzeptanzkriterium 12 war bisher nur halb erfüllt** — Editor/„+"/Anlegen-Dialog standen permanent in `app.html` und waren nur `hidden`; `app.js :: detachable()` hängt sie jetzt wirklich aus dem DOM aus. 51 jsdom-Prüfungen, `ui_smoke.py` 12/12 | +33 (7 `test_overview.py` + 24 `test_pages_markup.py`, zwei neue Dateien; +1 `test_meta.py`, +1 `test_static_routes.py`; `test_invite_enroll.py` und `scripts/ui_smoke.py` mussten ihre Seed-Suchregex auf das neue Klassen-Markup nachziehen, kein neuer Test) |
| 12 | Betrieb: `phase5_ui/scripts/{deploy,rollback,authbackup,restore_auth_check}.sh` + `ui_budget.py`; `phase5_ui/systemd/{sharefyx-authbackup.service,.timer,sharefyx-staging.service}`; `install_units.sh` um drei **optionale** Staging-Platzhalter erweitert; `diagnose.sh` um vier Prüfungen (UI erreichbar, offene UI-Sitzungen, jüngstes Auth-Backup, aktives Release) | 8 | ✅ **gebaut, Live-Teile beim Nikinger** — **löst V10 auf** (Messtabelle im Session-Block, alle fünf Größen im Korridor) und korrigiert eine **V13-Drift in `phase3_edge/`** (dort seit 2026-07-28 als geschlossen dokumentiert und 114 Zeilen weiter unten in derselben Datei noch als offen geführt). Drei dokumentierte Plan-Abweichungen (Health-Gate ohne authentifizierte Probe — Hard Rule 1; dritter Staging-Platzhalter; Platzhalter optional statt Pflicht). Eigener Fund beim echten Probelauf: ein zurückgerolltes Release wäre das nächste Rollback-Ziel gewesen → `*.failed`-Markierung | +21 (15 `test_deploy_scripts.py`, neue Datei; +6 `test_units.py`, darunter `test_every_placeholder_in_every_unit_is_known_to_the_install_script` — allgemeiner als die im Plan genannten) |
| 13 | UI-Revision nach Live-Feedback des Nikingers (elf Punkte) + Review von Step 8/S10: OAuth-Consent-Seite gestaltet (`phase4_auth/authserver/{templates,routes}.py`, CSP `style-src`/`font-src` erweitert), Ordner-Wechsel schließt/fragt jetzt bei offenem Editor + Nur-lesen-Ansicht bekommt ein „×" (`app.js :: navigate()`/`showReadonlyItem()`), Anlegen-Dialog-Typ folgt dem aktiven Ordner, Editor öffnet standardmäßig in der Vorschau (zwei Ausnahmen: Neuanlage, Neuladen nach Schreibvorgang), Archivieren vom „×" weggerückt, Abmelden-Icon getauscht, Passwort-Sichtbarkeit (Konto-Dialog + Login-/Einladungsseite, `pages.py` lädt jetzt `app.js`), Zähler-Polling (20s + Fokus/Sichtbarkeit) | 8b (Live-Feedback, kein Plan-Step) | ✅ **vollständig, gebaut und deployt** (2026-08-07) | +2 (`test_templates.py`: einer ersetzt, einer neu); JS bleibt laut Plan unit-ungetestet, 27 jsdom-Prüfungen im Scratchpad (nicht im Repo) gegen die neue Editor-Öffnen-/Navigations-/Toggle-Logik |

**[2026-08-09 Ergänzung, P6 Step 2 — P6-I/P6-S]:** `scripts/ui_budget.py` bekommt eine zweite,
informative Messfunktion `_measure_latency()` (eigene `LatencyMetric`-Dataclass, kein
`budget_bytes`/`ok`) für `search_items`/`get_item` (MCP, echter `mcpserver.app::create_app()`)
und `GET /api/v1/overview` — bewusst getrennt von den vier live-verifizierten Größen-`Metric`s
oben (Zeile 12, Abnahmezeile 15): eine Zeitmessung darf `main()`s Exit-Code nicht
zeitabhängig machen. Jede der drei Messungen macht einen verworfenen Aufwärmlauf vor dem
gemessenen Aufruf (Advisor-Fund vor dem Commit dieser Session — ein einzelner kalter Aufruf
misst sonst Routen-Setup/Session-Verhandlung statt der Fläche selbst). Dreifach reproduzierter
Lauf gegen ein temporäres `DATA_ROOT` (dieser Session, nicht real-live): `search_items`
95–96 ms/20 KB, `get_item` 5 ms/0,5 KB, `GET /api/v1/overview` **438–453 ms/1,5 KB** —
konstant über alle Läufe, also keine Kaltstart-Zahl, sondern eine reproduzierbare Kostenstelle
(P6-S: `Store.search()` liest weiterhin jede indizierte Datei). Kein neuer Test (`ui_budget.py`
hat wie `mcp_smoke.py` keine Unit-Tests, nur den realen Lauf als Beweis). Volle Herleitung:
`phase6_shares/CLAUDE.md` Step-2-Session-Block.

**[2026-08-09 Ergänzung, P6 Step 3]:** Update-Log-Banner (Plan §1.8): `webui/updates.py` (neu,
`parse_update_log()`/`load_update_log()`), `webui/config.py` (`UiSettings.update_log_path`,
Default `docs/UPDATE_LOG.md` im Repo-/Release-Root), `webui/api.py` (+`GET /api/v1/updates`,
+`POST /api/v1/updates/seen`, fünfter Parameter `auth_store: AuthStore` an `api_routes()` — der
gesehen-Zustand lebt in Schema 3, nicht im `storage`-Kern), `webui/static/js/updates.js` (neu,
`window.SharefyxUpdates`, MUSS vor `app.js` geladen werden — beide `defer`, aber `updates.js`
ruft `app.js`s globale `markdownToHtml()`/`sanitizeHtml()` und `app.js` ruft
`SharefyxUpdates.init()` an seinem eigenen Ende), `app.html`/`app.css` (Banner + „Update-Log
ansehen" im Konto-Dialog + Update-Log-Dialog, `position:fixed`-Banner + `body.has-update-banner`
statt einer Grid-Änderung an `.shell`, damit §4.1s Drei-Spalten-Layout unangetastet bleibt).
`deploy.sh` bekommt ein Gate (P6-X): bricht ab, wenn `docs/UPDATE_LOG.md`s oberste `##`-
Überschrift nicht das heutige Datum (UTC oder lokal) trägt, `SHAREFYX_ALLOW_STALE_UPDATELOG=1`
überspringt es — Default in `test_deploy_scripts.py`s `_env()`-Helfer gesetzt, sonst wären alle
bestehenden Deploy-Tests am neuen Gate gescheitert (`source_repo`-Fixture trägt kein Log).
`scripts/ui_budget.py`/`ui_smoke.py` mussten ihren direkten `api_routes(...)`-Aufruf um den
neuen Parameter nachziehen (kein neuer Test, reiner Signatur-Fix). `docs/UPDATE_LOG.md` (neu,
erster Eintrag datiert 2026-08-09, kündigt die künftige Sichtbarkeitsumstellung an, P6-L/H1).
+5 Tests in `phase5_ui/tests/` (`test_api.py` +2: GET/POST-Roundtrip, Banner-Zustand pro Space
getrennt;
`test_deploy_scripts.py` +3: Gate blockiert, Gate lässt einen echten datierten Eintrag durch,
Override umgeht es — Meta-Test `test_harness_ignores_ambient_sharefyx_configuration` um die neue
Env-Var ergänzt). Node/jsdom-Simulation (Scratchpad, nicht im Repo, gleiche Kategorie wie Step
10/11): echte `<script>`-Tags statt `window.eval()` genutzt, nachdem eine erste Fassung mit
`eval()` einen falschen Befund lieferte (`"use strict"`-Direct-Eval isoliert Top-Level-
Deklarationen, ein echtes `<script defer>`-Tag tut das nicht) — Banner erscheint mit
gerendertem Markdown, „Verstanden" versteckt es und postet `/updates/seen`, „Update-Log
ansehen" öffnet den Dialog, ein bereits gesehener `latest_id` unterdrückt das Banner. Volle
Herleitung: `phase6_shares/CLAUDE.md` Step-3-Session-Block.

**[2026-08-12 Ergänzung, P6 Step 5]:** `webui/api.py`/`webui/serializers.py` auf die neue
`SharePolicy`/`Surface.HUMAN`-Rechtepolitik umgestellt (ersetzt `OwnSpaceWritable`) — jeder
Item-Lese-/Schreibpfad löst jetzt über `store.acl_of()`+`can_read_item`/`can_write_item` auf
statt über `store.space_of()`+space-level `can_read`/`can_write`; `_items_get`/`search_items`
filtern item-weise, nicht mehr space-weise. `SharePolicy.can_read_item_as_human()` kapselt
`Surface.HUMAN` innerhalb von `mcpserver/permissions.py`, damit P5-B weiterhin nur ein
`mcpserver`-Symbol erlaubt (`test_webui_imports_exactly_one_mcpserver_symbol` jetzt gegen
`SharePolicy`, nicht mehr `OwnSpaceWritable`). Serializer bekommen `folder`/`visibility`/
`share_read`/`share_write`/`shared`; `readonly` bleibt ein vom Aufrufer übergebener Wert, jetzt
ACL- statt space-identitätsbasiert. Fail-closed-Ergänzung ohne Plan-Text (Nikinger-Entscheidung
2026-08-12): `_items_patch` lehnt `folder`-Änderungen durch Nicht-Eigentümer ab. +2 Tests in
`test_api.py` (27→29: `test_get_item_from_foreign_space_without_share_is_forbidden`/
`test_get_shared_item_from_foreign_space_is_readonly_true` ersetzen das alte „jeder fremde
Space ist immer lesbar"-Verhalten; `test_spaces_omits_foreign_space_without_a_share` neu) +2
`test_serializers.py` (7→9, neue Felder). `test_overview.py`/`conftest.py`-Fixtures mussten auf
`SharePolicy(item_store.acl_reader)` nachgezogen werden (kein neuer Test, reiner Signatur-Fix,
gleiche Kategorie wie P6 Step 3s `ui_budget.py`-Fund oben). Volle Herleitung, inkl. des
Advisor-Funds zum Folder-Move und der Nikinger-Entscheidung dazu:
`phase6_shares/CLAUDE.md` Step-5-Session-Block.

**[2026-08-17 Ergänzung, P6 Step 7b Commit 2/3]:** `webui/api.py :: _items_patch` bekommt
`space` im PATCH-Body (`ITEM_MOVE_PLAN.md` §4.3, P6-AD–AJ) — routet auf `store.move()`, sobald
`space` gesetzt ist. Rechteprüfung P6-AE (space-level `permissions.can_write()` auf Quelle UND
Ziel) läuft vor dem bestehenden `folder`-Eigentümer-Riegel; dieser greift jetzt nur noch bei
`space is None` (**Advisor-Fund vor dem Bauen**, derselbe wie im MCP-Adapter: der alte Riegel
hätte sonst legitime Cross-Space-Moves mit gleichzeitig gesetztem `folder` blockiert). Der
Re-Auth-Gate aus Step 7 Commit 5a (`require_share_reauth`) bekommt dafür keinen neuen Code —
`after_state.space` trägt jetzt den Zielspace, `widens()` vergleicht wie gehabt. Space-Wechsel
ohne `folder` im Body landet an der Ziel-Space-Wurzel (`""`), nicht im gleichnamigen Ordner im
Ziel. K4 (`folder` in `_items_post`s Whitelist) war bereits seit Step 7 Commit 3 erledigt, kein
neuer Fund. Fünf neue Tests in `test_api.py` (Widen verlangt Re-Auth, Narrow nicht, Space-ohne-
Folder-Default, P6-AE-Kern via item-level `share_write`, Guard-Routing-Regression). **Advisor-
Fund während des Bauens (nicht vor dem Commit, sondern ein eigener Fehler dieser Session):** ein
zu grob gewähltes `old_string` beim Einfügen der neuen Tests hatte
`test_widening_share_write_with_correct_credentials_succeeds` versehentlich mitten
durchgeschnitten — die vier Abschlusszeilen dieses bestehenden Tests landeten dadurch am Ende
der letzten neuen Testfunktion und lösten dort einen `NameError` aus. Vor dem Testlauf-Erfolg
bemerkt und korrigiert (`git diff` gegenkontrolliert, nicht nur der grüne Lauf vertraut).

**[2026-08-17 Ergänzung, P6 Step 7b Commit 3/3]:** `webui/static/{app.html,js/dialogs.js}` —
Verschieben-Dialog (§4.4) bekommt Space-Auswahl (nur `writable: true`), Ordnerliste baut sich
beim Space-Wechsel neu auf, Klartext-Konsequenz, `space` im `PATCH`-Body, Re-Auth im
eingefrorene-erste-Fassung-Muster wie der Freigabedialog (`pendingMoveBody`). P5-T: kein
Unit-Test, echte Playwright-Verifikation (Scratchpad) stattdessen — Login, Move `alpha`→`beta`,
Re-Auth korrekt ausgelöst und mit Credentials abgeschlossen, Toast+PATCH-Antwort+Screenshot
gegengeprüft. **Echter Fund der Verifikation:** `closeMoveDialog()` nullt `pendingMoveBody`,
der ursprüngliche Handler las danach `pendingMoveBody.space` für die Toast-Meldung — ein
`TypeError` verschluckte sie lautlos (Move gelang, aber ohne Rückmeldung). Werte jetzt vor dem Reset gesichert; ohne Browserlauf unentdeckt geblieben. Drag & Drop auf
einen Space-Knoten (§4.4 Punkt 3) bewusst nicht gebaut — P6-AB verlangt nur die Menüvariante.
Kein Live-Deploy, keine Nikinger-Bestätigung.

---

## Abnahmestand (Plan §6) — Stand 2026-08-09

> **[2026-10-02, rotiert (Gate/Z-Doku-Pflege, P9-L)]** Die vollständige Matrix — alle 20 Zeilen mit
> Kriterium, Stand und Beleg, dazu die Kurzfassung, die beiden späteren Nachträge (2026-08-13-Korrektur,
> 2026-10-02 trace-Block) und die Cutover-Notiz — steht ab jetzt
> **verbatim** in `ABNAHME_MATRIX_ARCHIVE.md` (L3, 📦): 99 Zeilen / 12.195 B wortgleich (der
> Abschnitt war 102 Zeilen / 12.259 B, die Differenz ist der `---`-Trenner). Nichts gestrichen,
> nichts umformuliert. Warum: Phase 5 ist seit 2026-08-09 abgeschlossen, die Matrix wurde seither
> nicht mehr nachgezogen — sie war gewachsenes Deckmaterial, kein lebender Status.

**Der Stand selbst, unverändert:** **20 von 20 Abnahmezeilen ✅ live bestanden (2026-08-09),
formaler Phasenschluss vollzogen, Phase 5 ✅.** Statusregel des Plans: **✅ heißt live-verifiziert,
nicht gebaut.** Die Einzelzeilen und ihre Belege stehen im Archiv; das Abnahmeprotokoll als
Kurzfassung (u. a. der Kurzbeleg für Zeile 20) liegt in
`../docs/concepts/P5_ABNAHME_2026-08-09.md`.

---

## Session stopped — 2026-08-09 (Zeile 20 live bestanden — Abnahmematrix vollständig, 20/20)

**Auftrag:** Nikinger meldete einen soeben erfolgten, unbewusst ausgelösten VM-Reboot ohne
eigenen Handgriff danach — der passive Prüffall für die letzte offene Abnahmezeile (20).
Read-only-Verifikation nach dem Maßstab von P3 Zeile 6 (`phase3_edge/CLAUDE.md`,
Korrekturnotiz 2026-07-29): Service-Autostart, Connector-Traffic, UI-Erreichbarkeit,
Funnel-Persistenz, Timer-Enable-Status. Details, alle Belege und der volle Nachtrag-Text stehen
im vorigen Session-Block, jetzt in `SESSIONS_ARCHIVE.md` (Rotation im selben Commit).

**Ergebnis: Zeile 20 ✅. Abnahmematrix 20/20, 0 teilweise, 0 offen.** Matrix in diesem Head
sowie `docs/INDEX.md` nachgezogen. Root-`CLAUDE.md`/`ROADMAP.md` bewusst noch nicht auf
„Phase 5 ✅" gesetzt — das hängt an den Step-9-Abschlussarbeiten, nicht an der Matrix allein.

**Verifiziert:** keine Testsuite gelaufen (keine Code-Änderung, nur Doku). Tabu-Diff nicht
relevant (kein Diff außerhalb `.md`).

**Nachtrag, 2026-08-09, dritter — Runbook-Schritt 4 bereits erledigt vorgefunden, kein Kommando
nötig:** Nikinger-Anfrage, ob das alte `auth-users`-Credential/Keyring gefahrlos entfernbar ist,
ohne einen Re-Login bei Fabian anzustoßen. Read-only geprüft statt spekuliert: die live
installierte Unit (`systemctl cat sharefyx-mcp`) trägt nur noch `LoadCredentialEncrypted=
auth-dek:...`, keine `auth-users`-Zeile mehr (deckt sich mit `test_units.py`s Assertion aus der
2026-08-02-Korrektur, P5 Step 2); `/etc/sharefyx/` enthält keine `auth-users.cred`-Datei; der
Keyring-Eintrag `nikinger-space`/`auth-users` existiert nicht mehr
(`keyring.get_password(...)` → `None`, `auth-dek` zum Vergleich `not None`). Codeseitig liest
die Laufzeit (`flows.py`, `app.py`) ohnehin nur noch über `UserDirectory`/`auth.sqlite3` —
`users.py :: load_users_from_keyring()` wird von keinem laufenden Prozess mehr aufgerufen, nur
noch von den Admin-Skripten `provision_user.py`/`export_auth_users.py`. **Ergebnis: nichts zu
tun, kein Kommando ausgegeben — der Schritt war schon vollzogen**, vermutlich beim
Unit-Redeploy in Step 2. Danach `docs/concepts/P5_ABNAHME_2026-08-09.md` geschrieben
(Nikinger-Auftrag: Abnahmeprotokoll ist Claude-Code-Job, Handover/SVG bleiben vorerst
Webchat-Job — Planänderung dazu angekündigt, nicht Teil dieser Session), `docs/INDEX.md` im
selben Commit nachgezogen.

**Nachtrag, 2026-08-09, vierter — Step-9-Abschlussarbeiten fertig, formaler Phasenschluss
vollzogen (Claude-Code-Session statt Webchat, Nikinger-Entscheidung — Details
`docs/PROMPTS.md`):** `docs/concepts/phase5_ui_uebersicht.svg` (1080×1080, Stil der
Vorgänger-Grafiken, zweimal gerendert und visuell gegengeprüft — erst Header/Mission-Box-Overflow
und eine Zeilenkollision in der Bausteine-Spalte gefunden und behoben, danach ein
`mcpserver/asgi.py`-Bezug korrigiert, der Datei nie in P5 geändert war) und
`docs/concepts/PHASE5_CLOSEOUT_HANDOVER.md` (Status/Delta/offene Entscheidungen §4.1–§4.6/
`[VERIFY]`-Bilanz V27–V38 für P6, Skelett von `PHASE4_CLOSEOUT_HANDOVER.md` übernommen)
geschrieben. Rotationsprüfung: dieser Head trägt weiterhin **genau einen** Session-Block (dieser,
jetzt mit vier Nachträgen) — kein Rotieren nötig.

**Formaler Phasenschluss, Nikinger-Entscheidung (AskUserQuestion dieser Session, „im selben
Commit"):** `ROADMAP.md`s P5-Zeile und Status-Absatz auf ✅, Root-`CLAUDE.md`s „Current state"
auf „keine aktive Phase, Phase 5 ✅, Phase 6 noch nicht geplant" umgeschrieben (vorheriger
🔄-Absatz durch dieselbe Textform ersetzt, die Phase 4 beim eigenen Abschluss bekam),
`docs/INDEX.md`s Abschnitt „Active phase" entfernt und die `phase5_ui`-Zeilen samt der beiden
neuen Dateien nach „Completed phases" verschoben. Nebenbei eine bereits vorher stale
Größenangabe korrigiert (`ROADMAP.md` stand mit „~9KB" im Index, tatsächlich ~13KB — unabhängig
von dieser Session entstanden, beiläufig mit demselben Commit behoben). Alles zusammen mit
diesem Head in **einem** Commit (Hard Rule 8).

**Push:** lokaler `main` lag zu Sessionbeginn 4 Commits vor `origin/main` — auf ausdrücklichen
Nikinger-Wunsch dieser Session direkt nach dem Abschluss-Commit gepusht (holt damit auch die
vier vorher schon lokal fertigen, noch ungepushten Commits nach).

**Verifiziert:** keine Testsuite gelaufen (nur `.md`/`.svg`-Änderungen, kein Code). Tabu-Diff
nicht relevant. SVG zweimal mit `~/.claude-code-tools/svg_to_png.py` gerendert und per `Read`
visuell geprüft, nicht ungesehen übernommen.

**Offen für die nächste Session (P6 — Browser-Planungssession, kein Claude-Code-Step):**
- `docs/concepts/PHASE5_CLOSEOUT_HANDOVER.md` **vor** dem Plan-Entwurf einmal ganz lesen — das
  ist der Einstiegspunkt, nicht dieser Head.
- Offener Befund, nicht aufgelöst: Step 9 Punkt 3 („frische Einladung") widerspricht §2.6
  (Migrationsrunbook, keine neue Einladung) — für den nächsten Plan-Review vormerken.
- Phase-6-Vormerkungen (alle zusammen zu planen, nicht isoliert): F1/F2 (Subspaces/Löschen),
  Client-Surface-Logging, `patch_item` (Werkzeug-Feedback 2026-08-08), O2 (geerbt aus P4).
- `[VERIFY]` V33 (Anthropic-Connector-Doku erneut gegenlesen) wurde in P5 nie explizit
  bearbeitet — echt offen, siehe Handover §5.1.
