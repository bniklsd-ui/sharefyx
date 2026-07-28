---
status: live
purpose: Archiv älterer Session-stopped-Blöcke aus phase4_auth/CLAUDE.md, newest-first, verbatim
read-when: Audit vergangener Sessions dieser Phase; NICHT für normalen Session-Start
detail: L3
up: CLAUDE.md
updated: 2026-07-28
---
# Session-Archiv — Phase 4 OAuth 2.1 + DCR

Newest-first. Drei Rotationen bisher, alle 2026-07-28 (Abschluss Step 3, dann Step 4, dann
Step 5) — via `scripts/rotate_session_block.sh phase4_auth`, nie von Hand.

## Session stopped — 2026-07-28 (V14 + Step 4)

**Ergebnis:** `[VERIFY]` V14 abgeschlossen, Step 4 (Metadaten und dynamische Registrierung)
abgeschlossen. `pytest -q` → **260/260 grün** (244 Vorlauf + 16 neue).

**V14, vor Step 4 verlangt:** Web-Recherche gegen die aktuelle Anthropic-Connector-Doku
bestätigte 13 von 14 Plan-Annahmen aus §0.6 wortgleich. Eine Ausnahme: native/Loopback-Clients
(Claude Code) sind inzwischen dokumentiertes Anthropic-Verhalten, nicht mehr nur eine
Erweiterungs-Idee — Details, Nikinger-Entscheidung (draußen lassen) und der dokumentierte
einfachere Weg für später stehen im Scope-Abschnitt oben, nicht hier dupliziert.

**Step 4:** `metadata.py`, `clients.py`, erste Hälfte `routes.py` gebaut — Details in der
Modul-Status-Tabelle oben (Zeile 5) inkl. aller additiven Abweichungen (`DCRError`,
`increment_register_window`, `starlette`-Deklaration, `oauth_routes()`-Signaturwachstum,
Content-Type-vor-Bremse-Reihenfolge). Nicht dort erwähnt, weil es kein Feature-Delta ist,
sondern ein Doku-Integritäts-Fund: **`test_authserver_does_not_import_mcpserver` existierte
nicht**, obwohl die Harte-Regeln-Zeile P4-A/P4-C sie seit Step 1 namentlich als Beleg zitiert
("Test: `test_authserver_does_not_import_mcpserver`"). Vier Steps lang unbelegt, jetzt in
`test_authserver_config.py` geschlossen. Lehre: eine im Fließtext genannte Testfunktion ist erst
ein Beleg, wenn `pytest --collect-only` sie auch findet — nicht wenn der Name plausibel klingt.
Wer diese Tabelle künftig liest, sollte die anderen dort zitierten Testnamen bei Gelegenheit
stichprobenartig gegen den echten Testbaum prüfen, nicht blind vertrauen.

**Advisor-Reviews dieser Session (zwei, vor und nach der Implementierung):** vor dem Schreiben
bestätigte der Advisor die fünf offenen Designfragen (DCR-Fehlercode-Trennung,
Security-Header-Umfang, Middleware- vs. Handler-Header, `starlette`-Pin-Politik,
`register_attempts`-Modulzugehörigkeit) und flaggte zusätzlich ein ungetestetes Risiko:
Starlette 1.3.1 liegt weit jenseits dessen, was `phase2_mcp` bereits benutzt
(`BaseHTTPMiddleware`, `await request.json()`, benutzerdefinierte Header auf Nicht-200-Antworten
— keins davon im Repo vorher geprüft). Eine Wegwerf-Probe (`httpx.ASGITransport` gegen eine
Zwei-Routen-Spielzeug-App mit Header-Middleware) lief vor jeder echten Implementierung grün —
API-Kompatibilität war damit belegt, nicht angenommen. Nach der Implementierung fand ein zweiter
Advisor-Durchlauf eine echte Lücke: `test_register_requires_json_content_type` allein hätte auch
bei vertauschter Prüfreihenfolge (Bremse vor Content-Type) grün bleiben können — die
Reihenfolge-Entscheidung war getroffen, aber nicht gepinnt. Nachgezogen:
`test_register_rejected_content_type_does_not_consume_rate_limit`.

**Design-Entscheidung, dokumentiert:** Security-Header direkt in den `routes.py`-Handlern statt
über eine Starlette-`Middleware`. Grund: `oauth_routes()` liefert eine flache Routenliste, die
der Wurzel-App **vorangestellt** wird (Plan §3.3), kein eigenes `Mount`/Sub-App — eine app-weite
Middleware in der Wurzel-App träfe auch `/health` und `/mcp`, ein zweites pfadgebundenes Mounten
sieht der Plan an dieser Stelle nicht vor. Vollständiges Set (CSP, Referrer-Policy,
X-Content-Type-Options, X-Frame-Options, Cache-Control, ggf. HSTS) auf beiden
Metadatendokumenten; nur `Cache-Control: no-store` auf `/oauth/register` (Plan §2.6: die
Cache-Control-Zeile überschreibt ihren eigenen Tabellenkopf ausdrücklich mit "auf allen
OAuth-Antworten").

**Nächster Schritt (konkret):** Step 5 — Autorisierungsfluss (`authserver/{flows,templates}.py`,
`routes.py` vervollständigt um `/oauth/authorize` und `/oauth/token`, `test_flows.py`,
`test_routes.py`, `test_templates.py`). Plan §2.4/§5 Step 5. `oauth_routes()` bekommt dabei
voraussichtlich den dritten Parameter `users` (siehe Abweichungsnotiz oben). Die beiden
wichtigsten Tests des Steps laut Plan: ein Fehler vor Prüfung von `client_id`/`redirect_uri`
darf **nie** zu einer Umleitung führen (`test_authorize_rejects_unknown_client_without_redirect`,
`test_authorize_rejects_unregistered_redirect_uri_without_redirect`).

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

---

## Session stopped — 2026-07-28 (Step 0 + Step 1 + Step 2)

**Ergebnis:** Step 0 (Haushalt, Drift, geerbte Abnahme), Step 1 (Gerüst, Konfiguration,
Kryptobausteine) und Step 2 (Passwörter, TOTP, Nutzerakten) abgeschlossen. `pytest -q` →
**225/225 grün** (168 P1+P2+P3 + 57 neue P4-Tests: 20 Step 1 + 37 Step 2).

**Kritischer Fund, geschlossen:** `export_space_map.py` zeigte zu Sessionbeginn drei aktive
Spaces (`fabian`, `niklas`, `nikinger`) statt der erwarteten zwei — ein Keyring-Token aus P2
Step 3, nie widerrufen trotz der B2-Umbenennung `nikinger/` → `niklas/`. Live und schreibfähig
(`Store.create()` legt Zielverzeichnisse automatisch an), aber dormant (`nikinger/` existierte
nicht mehr unter `DATA_ROOT`). Nikinger-Entscheidung: widerrufen. Ausgeführt in zwei Schritten,
beide live bestätigt: Keyring-Widerruf (`issue_token.py --revoke nikinger`), danach Export +
`sudo systemctl restart sharefyx-mcp` (2026-07-28 14:12:49) — `diagnose.sh` danach komplett
grün, `export_space_map.py` zeigt wieder exakt zwei Spaces. Vollständige Zeitachse:
`docs/concepts/PHASE3_CLOSEOUT_HANDOVER.md` §5 Nachträge. Nebeneffekt: die Handover-eigene
„Korrektur" von Fund 1 (die Behauptung, „alle drei Token rotiert" sei Drift und real seien es
zwei gewesen) war selbst falsch — zum Zeitpunkt der Prüfung existierten tatsächlich drei aktive
Spaces.

**Autocompact-Drift aus dem P3-Handover (§5) behoben:** README.md voll auf P3-Stand gezogen
(Cloudflare-Diagramm, Phasennummern OAuth/Web-UI, Tokenbeispiel), ROADMAP.md (Cloudflare →
Tailscale Funnel, `LoadCredential` → `LoadCredentialEncrypted`, P4-Paketname `auth` →
`authserver` per P4-B), Root-`CLAUDE.md` (R3-Ergänzung analog R4, Kollege-Prozess-Frage als in
P3-G entschieden markiert, „Aktive Phase" auf P4 gesetzt), `phase3_edge/CLAUDE.md`
(Tailscale-Installationsstatus, V13 geschlossen).

**Geerbte P3-Abnahme:** Zeile 12 (Backup-Timer) durch `systemctl list-timers` bestätigt (echter
Lauf 2026-07-28 00:00:50). Zeile 6 (Reboot) bleibt bewusst passiv offen. Zeile 13
(Restore-Nachweis) bewusst **nicht** nachgeholt — braucht ein frisches Bundle, kein Lauf
während ungeklärtem Credential-Zustand (war zum Prüfzeitpunkt ohnehin gegeben).

**Environment-Inventar (Step 0, `[VERIFY]` aufgelöst):** systemd 255 (≥235 für
`StateDirectory=`), NTP synchronisiert (`yes`), `argon2-cffi` aktuell `25.1.0` (P4-R-Pin),
`fastmcp` stabil weiterhin `3.4.5`/installiert `3.4.4` — **kein** stabiles 4.x, nur eine Alpha
`4.0.0a2` (`pip index versions --pre`). Der Plan-Befund „FastMCP 4 spricht die neue Revision,
P3-E-Trigger gefallen" ist damit nur zur Hälfte richtig — eine Alpha ist kein Release. Notiert,
keine Aktion (V25: nur beobachten).

**Step 1:** `authserver/{config,models,crypto,errors}.py` gebaut, `phase4_auth/pyproject.toml`
(Paket `authserver`, `argon2-cffi==25.1.0` exakt), `pytest.ini` um `phase4_auth/tests` erweitert,
`.gitignore` um `*.sqlite3` erweitert (V21). Abweichung vom Plan bei der Testdatei-Benennung
(siehe Modul-Status oben) — Ursache Namenskollisionen mit bestehenden `tests`-Verzeichnissen,
nicht antizipierbar ohne Repo-Zugriff (der Plan wurde ohne diesen geschrieben, siehe Plan-Kopf).

**Step 2:** `passwords.py` (Argon2id über `argon2-cffi`, `verify_password` wirft nie —
`InvalidHashError` erbt von `ValueError`, nicht von `Argon2Error`, ein Test
(`test_verify_returns_false_on_garbage_hash`) deckte das sofort auf, `DUMMY_HASH` für den
Enumerationsschutz), `totp.py` (RFC 6238 über RFC 4226, stdlib, alle 15 Appendix-B-Vektoren
SHA1/SHA256/SHA512 grün, Replay-Schutz über injizierten `last_counter`), `users.py` (spiegelt
`credentials.py :: load_space_map()` bewusst — Credentials-Verzeichnis zuerst, Keyring-Fallback,
`warning` bei fehlender Datei, Ausnahme bei kaputtem Inhalt). `provision_user.py`/
`export_auth_users.py` nach `issue_token.py`/`export_space_map.py`-Muster, gegen Fake-Keyring
+ injizierten `get_password` getestet — **nicht** gegen den echten Keyring ausgeführt, gleiche
Grenze wie bei P2 Step 3s `--space nikinger`-Roundtrip (Sache des Nikingers, nicht Claude Codes).

**`[VERIFY]` V17, gemessen (nicht geraten):** Argon2id mit den Plan-Default-Parametern
(`t=2, m=19456, p=1`) maß auf dieser VM **~15 ms** je Durchlauf — deutlich unter dem
Zielkorridor 50–250 ms. Nach Plan-Vorgabe `t` erhöht: `t=8` misst **~53 ms** (`m`/`p`
unverändert), fünf Läufe, Werte im Session-Log oben unter „Step 2" nachvollziehbar. Konstante
in `passwords.py` dokumentiert den gemessenen statt einen geratenen Wert.

**Nächster Schritt (konkret):** Step 3 — Persistenz und Bremse (`authserver/{store,
ratelimit}.py`, `test_store.py`, `test_ratelimit.py`). Schema aus Plan §2.3, `AuthStore`
kapselt **jede** SQL-Anweisung (kein SQL außerhalb dieses Moduls, per Grep im Session-Block zu
belegen), `now_fn` injiziert. Der Kern der Phase — Code-Replay/Refresh-Replay-Tötungsregeln
(RFC 9700) sind hier, nicht später.

---

