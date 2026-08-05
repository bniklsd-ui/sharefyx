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

---

## Session stopped — 2026-08-05 (Step 6: UI-Gerüst — Shell, Tokens, Navigation, Liste, Suche)

**Ergebnis:** Step 6 ist fertig — `GET /ui/` liefert erstmals die echte App-Shell
(`webui/static/{app.html,app.css,app.js}`) statt der Step-3-Übergangsseite, verdrahtet gegen
`/api/v1/{me,spaces,items,items/{id}}` aus Step 5. Bewusst **kein** Editor, **kein**
Markdown-Rendering (§3.5), **kein** Versionsband (§4.4), **kein** Konfliktdialog — das ist
wörtlich Step 7s Aufgabenliste, nicht vorgezogen.

**Korrektur zu Plan §1.5s Routentabelle, vor dem Bau entschieden (nicht erst live gefunden):**
die Tabelle trägt für `/ui/` in der Auth-Spalte „keine" ein, aber derselbe Plan-Abschnitt (§5
Step 6) verlangt im selben Atemzug einen Test namens `test_index_route_requires_session` — ein
direkter Widerspruch innerhalb desselben 📕-Dokuments, dieselbe Kategorie wie der
`mcpserver→webui`-Zirkel aus P5 Step 4 (dort ebenfalls zugunsten des konkreteren Textes gegen
eine Ableitungstabelle aufgelöst, siehe `SESSIONS_ARCHIVE.md`). Aufgelöst zugunsten des
Testnamens: `GET /ui/` ohne gültige Sitzung → `303` nach `/ui/login` (`webui/static_routes.py ::
_index()`), mit Sitzung → `200` mit `app.html`. Dem Nikinger nicht vorab zur Entscheidung
vorgelegt (anders als der Zirkel-Fund in P5 Step 4) — die Kategorie ist dieselbe, aber die
Auflösung war hier eindeutig genug (ein Tabellen-Zellwert gegen einen explizit benannten Test im
selben Abschnitt), um sie als „kleine Drift" statt „entscheidungsbedürftig" einzustufen (Root-
`CLAUDE.md`: „kleine Drift selbst fixen und datiert vermerken; wenn nicht klein, stoppen und
fragen"). Wird hier vermerkt, nicht still verschwiegen.

**CSRF-Token-Übergabe an die Shell (im Plan nicht spezifiziert):** `SessionManager.rotate()`
gibt den CSRF-Token nur EIN einziges Mal als Klartext zurück (`ui_sessions` speichert nur den
Hash) — der Plan sagt nirgends, wie `app.js` daran kommt. Lösung: die seit Step 3 bestehende
Login-Erfolgsseite (`pages.py :: render_logged_in_page()`) behält ihr `<input type="hidden"
name="csrf" value="...">` unverändert und bekommt zusätzlich `<script src="/ui/static/app.js"
defer>`. `app.js`s Bootstrap-Teil (läuft auf JEDER `/ui/*`-Seite, erkennt sich selbst an
`document.getElementById('shell')`s Fehlen) liest das Feld aus, legt den Wert in
`sessionStorage['sfx:csrf']` ab (kein `localStorage` — konsistent mit dem in §4.5 bereits
gelockten Entwurfsschutz-Muster) und leitet per `location.replace('/ui/')` weiter. Ein `401
unauthenticated` von irgendeinem API-Aufruf schickt in Step 6 schlicht zu `/ui/login` zurück —
kein Entwurfsschutz nötig, es gibt in Step 6 noch nichts Eingetipptes zu verlieren; Step 7 baut
dafür die volle „Sitzung abgelaufen"-Karte aus §4.5, sobald der Editor existiert. Logout bleibt
ohne JavaScript funktionsfähig (das Formular aus Step 3 ist unverändert), `app.js` ergänzt nur
einen bequemeren Weg (`fetch('/ui/logout', ...)` mit dem CSRF-Header statt Formular-Submit).

**Font (V27 im VERIFY-Register, hier geschlossen statt auf Systemstack ausgewichen):**
`phase5_ui/scripts/build_font_subset.sh` (neu) lädt Inter Variable v4.1
(`github.com/rsms/inter`, OFL-1.1, SHA256-geprüft), pinnt die optische Größe auf Textgröße
(`opsz=14` — die einzige, die diese UI benutzt) und beschneidet die Gewichtsachse auf `380:620`
(deckt 400/500/600 aus Plan §4.2 mit Marge ab), subsetzt danach auf den
Google-Fonts-„latin"-Unicodebereich (deckt deutsche Umlaute/ß über Latin-1 Supplement ab) plus
`tnum/lnum/pnum/kern/liga/calt`. Ergebnis: **34,7 KB** (Ziel < 120 KB), variable Gewichtsachse
erhalten (`fvar: wght 380–620`), alle deutschen Sonderzeichen + `€` im `cmap` geprüft. Datei
trägt einen Kurzhash des Inhalts (`InterVariable-subset.2fa9d1dc.woff2`) — macht sie zu einem
echten „gehashten Asset" für `static_routes.py`s Cache-Header-Regel (unten), nicht nur einem
hypothetischen Fall. `LICENSE.txt` liegt unverändert als `webui/static/fonts/OFL.txt` daneben.
**Reproduzierbarkeit ist nicht Bit-Identität:** ein erneuter Lauf des Skripts kann eine andere
Hex-Prüfsumme erzeugen (der `head`-Tabellen-Zeitstempel in TTF/WOFF2 ist nicht deterministisch
über Compiler-Läufe hinweg) — das ist bei einem content-hashed Dateinamen erwartet und
unschädlich, verlangt aber bei jedem Font-Rebuild eine manuelle Ein-Zeilen-Anpassung der
`@font-face`-`src`-URL in `app.css`.

**Cache-Header-Regel (§3.4 „`no-store` außer für `/ui/static` mit gehashtem Namen"):**
`static_routes.py :: _HASHED_NAME_RE` erkennt einen Kurzhash unmittelbar vor der Dateiendung
(Punkt- oder Bindestrich-getrennt) — nur solche Dateien bekommen `public, max-age=31536000,
immutable`. `app.html`/`app.css`/`app.js` tragen bewusst KEINEN Hash (kein Build-Step, P5-T —
sie werden von Hand editiert; ein `immutable`-Cache auf einem unveränderten Dateinamen wäre nach
der nächsten Änderung ein tagelang stiller Bug) und bekommen `no-store`.

**Scope innerhalb der Shell:** Rail (Spaces + Filter „Offen"/„Notizen"/„Archiv" + Logout),
Liste (Suchfeld mit 200ms-Debounce, `↑`/`↓`-Navigation, `/`-Fokus-Shortcut), Detail
(schreibgeschützte Ansicht: Titel/Status/Fällig/Tags/Version, Rohtext in `<pre>`, sichtbare
„Nur lesen"-Kennzeichnung bei `item.readonly` — erfüllt den Geist von Akzeptanzkriterium 12
schon jetzt, auch wenn die Live-Abnahme erst mit einem echten Editor in Step 7 sinnvoll ist).
Rail-Kollaps ≤1280px und Liste-hinter-Zurück-Navigation <1024px (§4.3) sind gebaut, größtenteils
reines CSS, ein `data-view`-Attribut auf `#shell` für die eine JS-Umschaltung. `Esc`/`Ctrl+S`
bewusst NICHT gebunden (kein Dialog zu schließen, nichts zu speichern in Step 6) — im Code
kommentiert, warum sie fehlen, statt sie tot zu binden.

**Verifiziert:** `pytest -q` (Repo-Wurzel) → **512/512 grün** (504 vor diesem Step, +8: 7
`test_static_routes.py`, neue Datei, + 1 `test_ui_index_route_reachable_through_create_app` in
`phase2_mcp/tests/test_app.py`; `app.js` bleibt laut Plan unit-ungetestet, kein Node im
Projekt). `pyflakes` über alle neuen/geänderten Python-Dateien sauber. `git diff --stat` auf
`storage/`, `mcpserver/tools.py`/`permissions.py`/`server.py` bleibt leer (Akzeptanzkriterium
§6.18). Zusätzlich ein manueller In-Process-Durchlauf (wie `ui_smoke.py`, kein echter Browser):
anonymer `GET /ui/` → `303`/`/ui/login`, Login → Bootstrap-Seite mit `<script>`-Tag, `GET /ui/`
mit Sitzung → `200`/`app.html`, `GET /ui/static/app.css` → `200`/`text/css`/`no-store`,
`GET /ui/static/does-not-exist.css` → `404`. **Advisor-Review vor diesem Commit war nicht
möglich** (Tool zweimal „temporarily overloaded" zurückgemeldet, wie schon beim Step-5-Nachtrag
— derselbe dokumentierte Ersatz, nicht übersprungen): `pyflakes`, voller `pytest -q`, der
manuelle In-Process-Durchlauf oben, Tabu-Pfad-Diff, alles vor dem Commit.

**Manuell (Nikinger, nicht Teil dieses Steps):** ein echter Browser-Blick auf `/ui/` gegen eine
Wegwerf-Instanz — Layout/Typografie/die 1280px-/1024px-Breakpoints lassen sich nicht aus
`pytest` beurteilen.

**Nächster Schritt (konkret):** Step 7 (Editor, Vorschau, Konflikt, Frontmatter-Felder — Plan
§3.5, §4.4, §4.5, P5-U). Baut auf der in Step 6 gelegten `app.js`-Struktur auf (State/Render-
Funktionen, API-Client mit `sessionStorage`-CSRF, bereits vorbereiteter `X-CSRF-Token`-Pfad für
Nicht-GET-Aufrufe). Ersetzt außerdem den einfachen `401`→`/ui/login`-Redirect aus Step 6 durch
die volle „Sitzung abgelaufen"-Karte samt Entwurfsschutz (§4.5), sobald es etwas Eingetipptes
gibt, das dabei verloren gehen könnte. Zeilen 5/6 der Block-A-Abnahme folgen weiterhin, sobald
ein echter Klick-Pfad für `/api/v1/account/password` existiert.
