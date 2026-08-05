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
| 6 | Nach dem Passwortwechsel: Connector fordert neue Autorisierung · andere UI-Sitzung beendet · aktuelle läuft weiter | 🟡 **teilweise** | Connector-Reconnect ✅ und aktuelle Sitzung lief weiter ✅ (Nikinger, 2026-08-05). **Offen: ein zweiter, gleichzeitig angemeldeter Browser wurde nicht geprüft** — dafür braucht es zwei getrennte Sitzungen (zweites Profil oder privates Fenster), ein zweiter Tab desselben Browsers teilt das Cookie und beweist nichts |
| 7 | Fehlversuchsbremse greift für UI-Login und OAuth-Consent gemeinsam | ✅ | Nikinger live, 2026-08-05 |
| 8 | `authctl.py list-users` zeigt keinen Hash und keinen Seed | ✅ | Nikinger live, 2026-08-05 |
| 9 | `auth.sqlite3` mit `strings`: kein Base32-Seed im Klartext | ✅ | Nikinger live, 2026-08-05 |
| 10 | Anlegen/Bearbeiten/Anhängen/Archivieren über die UI; `.md` im `DATA_ROOT` korrekt **und** Git-Commit existiert | ⬜ offen | UI-Seite funktioniert live; der **Dateinachweis** (`git log` im Datenverzeichnis) steht aus |
| 11 | Konflikt in zwei Tabs → Versionsband `--warn` + Dialog, kein stiller Überschreiber | ✅ | Nikinger live, 2026-08-05 nach Step 7b |
| 12 | Fremder Space sichtbar/lesbar, **ohne** Schreib-Bedienelemente im DOM | ✅ | Nikinger live in DevTools, 2026-08-05 nach Step 7b (vorher nur `hidden` — siehe F7-Umfeld im Session-Block) |
| 13 | Unbekanntes Frontmatter-Feld überlebt eine UI-Bearbeitung unverändert | ⬜ offen | `extra` wird durchgereicht (`serializers.py`), live noch nicht belegt |
| 14 | `format: markdown` erscheint nach dem ersten UI-Schreibvorgang und stört keinen Tool-Aufruf | ⬜ offen | |
| 15 | `ui_budget.py` liefert alle vier Zahlen | ⬜ offen | Step 8 |
| 16 | `deploy.sh` rollt bei kaputtem Health-Endpunkt automatisch zurück | ⬜ offen | Step 8 |
| 17 | Beide Nutzer benutzen UI **und** Connector am selben Tag gegen dieselbe Instanz | ⬜ offen | Step 9 (P5-AE) |
| 18 | `git diff` auf `storage/`, `mcpserver/{tools,permissions,server}.py`: leer | ✅ | bei jedem Step-Commit geprüft, zuletzt Step 7b |
| 19 | Cookie an `/mcp` ignoriert; Bearer an `/api` ignoriert | 🟡 | Testseite ✅ (`test_isolation.py`, `test_overview.py`); der im Plan zusätzlich verlangte **Live-`curl`** steht aus |
| 20 | Reboot: UI, Connector, Timer kommen ohne Handgriff zurück | ⬜ offen | passiv zulässig (wie P3 Zeile 6) |

**Kurz:** 11 von 20 live bestanden, 2 teilweise (6, 19), 7 offen — davon 4 an Step 8/9 gebunden.

---

## Session stopped — 2026-08-05, dritter Nachtrag (Step 7b: UI-Überarbeitung nach Live-Feedback)

**Ergebnis:** Der Nikinger hat Step 6/7 live benutzt und elf Punkte gemeldet; alle sind
umgesetzt, dazu sechs eigene Funde. Die Oberfläche hat jetzt einen Navigationsbaum statt zweier
flacher Rail-Blöcke, eine Übersichtsseite, plastische Bedienelemente, zwei farblich getrennte
Editor-Paneele, Rückmeldung nach jedem Schreibvorgang und gestaltete Auth-Seiten. Ausführungsplan
dieser Session: `/home/savefyx/.claude/plans/merry-tickling-elephant.md`.

**Zwei gelockte Entscheidungen revidiert — Nikinger-Entscheidung 2026-08-05, nicht still:**

| Gelockt | Bisher | Jetzt | Grund |
|---|---|---|---|
| **Plan §4.1** | „Keine Verläufe, keine Schlagschatten außer einem einzigen für Modale" | Verlauf + Innenhighlight + Kante + weicher Schatten auf Bedienelementen; eingelassene Eingabefelder | Die Zurücknahme führte live dazu, dass Knöpfe nicht als Knöpfe erkennbar waren. |
| **Plan §4.3** | Rail = zwei flache Blöcke (Spaces, Filter) | Rail = Baum (Übersicht · eigener Space ▸ Ordner · verbundene Spaces) + eigene Übersichtsseite | „Filter" sah aus wie eine zweite Top-Ebene neben „Spaces"; tatsächlich ist ein Filter immer an einen Space gebunden. Genau daher kam die Meldung „meine Notizen landen in *Notizen*, nicht in meinem Bereich". |

Unverändert bleiben: Farbtoken, Typografie (§4.2), Versionsband (§4.4), Fokusring und
120-ms-Bewegungsregel (§4.6), P5-U (kein WYSIWYG), P5-Y (kein serverseitiges Rendern), P5-W
(keine Mobilversion). `docs/concepts/phase5_ui_plan.md` bleibt als 📕-Snapshot **unverändert** —
dieselbe Handhabung wie beim §1.2-Widerspruch am 2026-08-03.

**Die elf Meldungen des Nikingers und was daraus wurde:**
1. *Keine Bestätigung beim Speichern* → Statuszeile `#toast` (§4.5 sah sie schon für „Dienst nicht
   erreichbar" vor) nach jedem Schreibvorgang, mit Versionsnummer: „Gespeichert · v11".
2. *Editor lässt sich nicht schließen* → `× Schließen` in der Kopfleiste, `Esc`, und die
   Übersicht-Schaltfläche; bei ungespeicherten Änderungen erst eine Rückfrage.
3. *Undurchsichtig, wo was hinkommt* → zwei beschriftete Paneele mit **verschiedenen Farben**:
   „Text (Markdown)" kühl (`--panel-body`), „Kopfdaten (YAML-Frontmatter)" warm (`--panel-meta`),
   zugeklappt vorbelegt (`<details>`, klappt also auch ohne JS) mit Zusammenfassungszeile und dem
   Hinweis, dass diese Felder in der Regel ein verbundenes Claude pflegt.
4. *„Ich kann in Fabis Space anlegen"* → **echter Fund, UI-seitig.** Der Server war immer korrekt
   (`_items_post()` liest nie ein `space` aus dem Body, P5-A), aber die UI zeigte „+" und „Erste
   Notiz anlegen" auch im fremden Space. Jetzt: Nur-lesen-Balken über der Liste, und die
   Bedienelemente werden **aus dem DOM ausgehängt** (siehe eigener Fund 7 unten).
5. *Eigene Notizen landen „in Notizen"* → strukturell durch den Baum gelöst; zusätzlich springt
   der aktive Ordner nach dem Anlegen dorthin, wo das neue Item tatsächlich liegt.
6. *UI-Umbau (Übersicht + Spaces als Überordner)* → umgesetzt, `GET /api/v1/overview` speist
   Kacheln, „Zuletzt benutzt" und die Zähler-Plaketten im Baum.
7. *Zu wenig Reaktion* → Toasts, Zähler im Baum nach jedem Schreibvorgang aktualisiert, aktiver
   Pfad sichtbar, „Speichern" deaktiviert wenn es nichts zu speichern gibt.
8. *Login-Seite unverändert* → alle sechs Seiten aus `pages.py` tragen jetzt die Karte
   `.auth`/`.auth-card`. **Ursache war nicht Faulheit, sondern eine Lücke:** die Seiten luden
   `app.css`, benutzten daraus aber keine einzige Klasse — ein Stylesheet-Link ohne Markup sieht
   im Diff nach Gestaltung aus und ist keine. `test_pages_markup.py` hält das jetzt fest.
9. *3D/Skeuomorphismus* → siehe Revision §4.1 oben.
10. *Verschiedene Farben für Text- und YAML-Feld* → siehe Punkt 3.
11. *Obsidian-artige Graph-Ansicht* → **Nikinger-Entscheidung: zurückgestellt.** Die Übersicht
    ist so gebaut, dass sie später als weitere Kachel eingehängt werden kann.

**Sechs eigene Funde (F1–F6), alle behoben:**
- **F1** `render_enrollment_page()` setzte den weißen QR-Hintergrund per `style="…"` — `security.py`
  sendet `style-src 'self'` **ohne** `unsafe-inline`, das blockiert auch Style-Attribute. Die
  Regel griff also nie: ein Fix, der wie einer aussah. Jetzt `class="qr-frame"`, mit Test.
- **F2** `window.alert`/`window.confirm` an fünf Stellen → eigener `#confirm-dialog` und Toasts.
- **F3** Nach dem Archivieren blieb das Item im Editor stehen, obwohl es aus der Liste
  verschwunden war → Editor schließt sich, Toast bestätigt.
- **F4** Der Leerzustand sagte immer „Keine Notizen in diesem Space", auch bei einer Suche ohne
  Treffer → drei unterschiedene Zustände (§4.5 verlangt das ausdrücklich).
- **F5** Filter-Chips wurden nur im Leerzustand gerendert und waren nicht entfernbar; `.chip__remove`
  war totes CSS → Such-Chip immer sichtbar und entfernbar.
- **F6** „Speichern" war immer aktiv → **das ist die Ursache des `v10`-Erlebnisses**, nicht nur die
  fehlende Bestätigung. Ohne echte Änderung ist der Knopf jetzt deaktiviert (und sieht auch so aus).
- **F7 — Advisor-Fund vor dem Commit, der schwerwiegendste der Session (Vorbestand aus Step 7).**
  Alle drei Schreibpfade adressierten das Item über `state.selectedId`, nahmen die Version aber aus
  `state.editingSnapshot`. `selectItem()` setzt `selectedId` **sofort**, `editingSnapshot` erst
  wenn die Antwort da ist — dazwischen liegt ein Fenster, in dem beide zu verschiedenen Items
  gehören. Ein `Strg+S` in diesem Moment schriebe den Inhalt von Item A unter der Kennung von Item
  B, und wenn beide Versionen zufällig gleich sind, **ohne Konflikt**: ein stiller Überschreiber,
  genau das, was Hard Rule 3 verbietet — nur clientseitig herbeigeführt, wo der Server nichts
  merken kann. Ein zweiter Pfad kam **erst durch Step 7b** hinzu: über „Zuletzt benutzt" lässt sich
  ein fremdes Item öffnen, ohne den Editor vorher zu verlassen; `showReadonlyItem()` hängte den
  Editor zwar aus, setzte aber weder `detailEditorEl.hidden = true` noch
  `state.editingSnapshot = null` — und `hidden` überlebt das Aushängen, der `Strg+S`-Wächter blieb
  also scharf. Behoben: alle drei Schreibaufrufe adressieren über `state.editingSnapshot.id`
  (Kennung und Version stammen damit beweisbar aus demselben Lesevorgang), plus die zwei fehlenden
  Zeilen in `showReadonlyItem()`. **Gegenprobe gefahren, nicht nur behauptet:** die jsdom-Prüfung
  „Strg+S bei offenem fremden Item schreibt nicht" wurde gegen eine Kopie mit zurückgenommenem Fix
  laufen gelassen — dort **ein** Schreibaufruf, mit Fix **null**.

**Zwei Funde, die über die Meldungen hinausgehen:**
- **Vierter Ordner „Erledigt".** Die drei Ordner des Mockups decken `STATUS_VALUES["task"]` nicht
  ab: eine auf `done` gesetzte Aufgabe fiel durch alle drei und war in der Oberfläche nirgends
  mehr auffindbar, bis jemand sie archivierte. `_BUCKETS` hat jetzt vier Einträge; ein Test hält
  fest, dass jeder Zähler exakt so viele Items meint, wie die Liste beim Klick zeigt.
- **Akzeptanzkriterium 12 war bisher nur halb erfüllt.** Der Step-7-Session-Block behauptet, für
  fremde Items würden „keine Editor-Elemente überhaupt gerendert" — tatsächlich standen Editor,
  „+"-Knopf und Anlegen-Dialog permanent in `app.html` und waren nur `hidden`, mit DevTools also
  auffindbar. Kriterium 12 sagt wörtlich „**ohne** Schreib-Bedienelemente **im DOM**". `app.js ::
  detachable()` hängt diese drei Teilbäume jetzt wirklich aus dem Dokument aus und später wieder
  ein; die jsdom-Simulation prüft beide Richtungen. **Korrektur an der Step-7-Zeile der
  Modultabelle, nicht am Step-7-Block selbst** (der ist rotiert und bleibt verbatim).

**Neuer Endpunkt `GET /api/v1/overview`** (wie `/api/v1/meta` in Step 7 in keiner Plan-Routentabelle):
je sichtbarem Space die vier Bucket-Zähler und die fünf zuletzt geänderten Items. Die Arbeit liegt
bewusst serverseitig — der Plan lässt JavaScript ungetestet, Python nicht. Kein LLM, keine Deutung,
nur Zählen und Sortieren; das Kernprinzip „der Server ist dumm" bleibt gewahrt. `GET /api/v1/meta`
gibt zusätzlich `buckets` heraus, damit `app.js` das Ordnervokabular nicht ein zweites Mal
definiert. `recent` trägt **kein** `snippet`: die Übersicht ist die erste Fläche, die mehrere
Spaces nebeneinander zeigt, ohne dass man bewusst „in einen fremden Space gewechselt" ist — dort
gehört fremder Fließtext nicht hin (Rule 4 dem Geiste nach). **Nebenwirkung, damit sie niemand
sucht:** `GET /api/v1/spaces` hat damit keinen Aufrufer mehr in `app.js` (`init()` geht
`/me` → `/meta` → `/overview`; `/overview` liefert die Space-Liste mit). Der Endpunkt bleibt —
er ist Teil des §3.1-Vertrags und weiterhin getestet, nur eben nicht mehr von der eigenen
Oberfläche benutzt.

**Verifiziert:** `pytest -q` (Repo-Wurzel) → **549/549 grün** (516 vorher, +33: 7 `test_overview.py`
+ 24 `test_pages_markup.py` (3 Aussagen × 8 Seiten) + 1 `test_meta.py` + 1 `test_static_routes.py`).
`pyflakes` sauber, `node --check app.js` sauber. `scripts/ui_smoke.py` → **12/12** (die
Seed-Suchregex musste auf das neue Klassen-Markup nachgezogen werden, gleiche Anpassung wie in
`test_invite_enroll.py` — beide Stellen mit datierter Notiz). `git diff --stat` auf `storage/`,
`mcpserver/tools.py`/`permissions.py`/`server.py` bleibt **leer** (Akzeptanzkriterium 18). Eine
Node/jsdom-Simulation im Scratchpad (nichts davon im Repo) fuhr **53 Prüfungen** über den vollen
Lebenszyklus — Baum, Übersicht, Anlegen mit Ordnersprung, Dirty-Gating (belegt: drei Klicks auf
„Speichern" ohne Änderung erzeugen **einen** `PATCH`, nicht drei), Vorschau, Anhängen, Konflikt,
Schließen mit und ohne Änderungen, fremder Space (fünf Prüfungen auf „nicht im DOM" plus die zwei
F7-Prüfungen), Suche mit Chip, Archivieren, Passwortdialog inklusive CSRF-Rotation,
Sitzungsablauf — alle grün. Ein Fehlschlag darin war ein Fehler der Simulation selbst
(`getElementById` auf einem korrekt ausgehängten Knoten), kein `app.js`-Fund.

**Advisor:** beim ersten Versuch (vor dem Bauen) nicht erreichbar („temporarily overloaded",
dasselbe Bild wie in der Step-6/7-Session), beim Review **vor dem Commit** dann erreichbar — und
er fand mit **F7** den schwerwiegendsten Fehler der Session, den weder `pytest` noch die
jsdom-Simulation in ihrer damaligen Fassung erreicht hatten (die Simulation prüfte
DOM-Anwesenheit, betrat aber nie den Zustand „eigenes Item mit lebendem `editingSnapshot` →
fremdes Item öffnen"). Zwei kleinere Advisor-Punkte ebenfalls übernommen: die Größenangabe für
Root-`CLAUDE.md` in `docs/INDEX.md` (26 → 32 KB — genau die Drift-Kategorie, die diese Datei
schon fünfmal getroffen hat) und der Hinweis, dass `/api/v1/spaces` keinen UI-Aufrufer mehr hat.

**Manuell (Nikinger, nicht Teil dieses Steps):**
- `sudo phase3_edge/scripts/install_units.sh && sudo systemctl restart sharefyx-mcp` — **Schritt
  null**, sonst liefert der Dienst weiter den alten Build.
- Sichtprüfung im echten Browser (Layout/Fokus/Tastatur verhalten sich in jsdom nicht identisch
  zu Chrome): Übersicht, Baum, plastische Bedienelemente, die zwei Panelfarben, Login-Seite.
- Fremder Space in DevTools: **kein** Schreib-Bedienelement im DOM (Akzeptanzkriterium 12).
- **Block-A-Abnahmezeilen 5 und 6** sind jetzt ohne DevTools-Behelf testbar: `⚙ Konto` →
  Passwort ändern ohne `systemctl restart`, neuer Login sofort gültig (Zeile 5); danach fordert
  der Connector neue Autorisierung, eine zweite UI-Sitzung ist beendet, die aktuelle läuft weiter
  (Zeile 6).

**Nächster Schritt (konkret):** Zeilen 5/6 live abnehmen (siehe oben), danach Step 8 (Betrieb:
Deploy, Rollback, Staging, Auth-Backup, Messung — Plan §5 Step 8).

---
