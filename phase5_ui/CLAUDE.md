---
status: live
purpose: Phase-Head Web-UI, REST-API, Auth-Selbstverwaltung — Scope, harte Regeln, Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase5_ui/ oder an den in P5-B genannten Dateien in authserver/mcpserver — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase5_ui_plan.md             # voller Plan, Entscheidungen P5-A–P5-AE, Steps 0–9
  - ../docs/concepts/PHASE4_CLOSEOUT_HANDOVER.md   # Herkunft der offenen Entscheidungen §4.1–§4.5, [VERIFY]-Bilanz V14–V26
updated: 2026-08-02
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

---

## Session stopped — 2026-08-02 (Step 2: Auth-Datenmodell Schema 2, `UserDirectory`, Migration)

**Für den nächsten, kalten Leser:** dritte Session der Phase, direkt im Anschluss an Step 1
(„go on" nach der Zusammenfassung der beiden noch offenen Live-Aktionen). Plan §5 Step 2s
eigene Reihenfolge (secretbox → Schema 2 + Store → `userdir.py` → `flows.py`/`app.py`-Umstieg →
Migrationsskript) wurde genau so durchlaufen. `pytest -q` stand zu Beginn bei 353/353, am Ende
bei **414/414** (+61, siehe Advisor-Nachtrag unten: zwei Tests kamen nach der ersten
412/412-Marke noch dazu, ein zweiter Advisor-Durchlauf fand einen echten Bug zwischen ihnen).

**Plan-Drift, vor dem Umbau geklärt (Advisor-Review vor Beginn):** keine — die Reihenfolge und
alle fünf Bauteile aus §2.2–§2.6 waren mit dem realen Repo-Stand deckungsgleich (Step 1 hatte
`UserDirectory`/Schema 2 bereits als „noch nicht gebaut" markiert, genau das ist jetzt
nachgeholt). Zwei Stellen, an denen bewusst über den Plan-Wortlaut hinausgegangen oder von ihm
abgewichen wurde, beide vorab mit dem Advisor abgestimmt:

- **Recovery-Code im OAuth-Consent-Formular** (§2.5, „ein Wert mit Bindestrich und Länge 11 wird
  als Recovery-Code geprüft") ist bereits in diesem Step verdrahtet, nicht erst in Step 4 — die
  Formerkennung lebt einzig in `userdir.py :: looks_like_recovery_code()`, `flows.py` leitet sie
  nicht selbst her. Wichtiger Fallstrick, den der Advisor benannte: ein Recovery-Login hat keinen
  TOTP-Zähler (`accepted_counter` bleibt `None`), `store.set_totp_counter()` darf deshalb NICHT
  mehr unbedingt nach jedem Erfolg laufen (vorher tat es das) — sonst würde ein Recovery-Login
  stillschweigend den TOTP-Replay-Zähler auf `None` zurücksetzen. Jetzt hinter
  `if accepted_counter is not None:` gattert, Regressionsgefahr in einem eigenen Testfall nicht
  extra geprüft (kein Recovery-Code existiert vor Step 4 für echte Nutzer, aber die Guard-Logik
  selbst ist über `test_totp_replay_is_rejected_without_burning_the_stored_counter` weiterhin
  abgedeckt, da dieser Test ausschließlich den TOTP-Zweig durchläuft).
- **`UserDirectory.__init__` prüft „DEK fehlt UND `users` nicht leer" selbst**, nicht
  `config.py` (der Plan nennt die Bedingung nur bei `secretbox.py`, ohne eine Datei festzulegen)
  — Begründung: das ist die Stelle, die tatsächlich entschlüsseln muss und bei jedem
  Prozessstart genau einmal läuft; `config.load_data_encryption_key()` bleibt eine reine
  Lesefunktion ohne Kenntnis vom `AuthStore`.

**Bauteile, in Reihenfolge:**

1. **`secretbox.py`** — AES-256-GCM (`cryptography.hazmat...aead.AESGCM`), `nonce || ciphertext`
   als ein `bytes`-Blob, `SecretBoxError` als einziger Fehlertyp (kein Unterschied nach Ursache
   nach außen, dieselbe Enumerationslogik wie `passwords.verify_password`).
2. **`config.py :: load_data_encryption_key()`** + `generate_/encode_/decode_data_encryption_key()`
   — dieselbe Verzweigung wie `users.load_users()` (`CREDENTIALS_DIRECTORY/auth-dek` zuerst,
   Keyring `nikinger-space`/`auth-dek` als Dev-Fallback), aber **kein** stiller
   Warn-und-Keyring-Fallback bei fehlender Datei: Abwesenheit ist hier entscheidungsrelevant für
   den Aufrufer (`UserDirectory.__init__`), nicht etwas, das diese Funktion selbst auflösen darf.
   `users.py`s Docstring-Behauptung „`keyring` wird nur hier importiert" korrigiert (gilt seit
   diesem Commit für zwei Module, unabhängig voneinander). **V28 geschlossen:** `cryptography`
   war bereits im `.venv` (49.0.0), jetzt exakt in `phase4_auth/pyproject.toml` gepinnt.
3. **Schema 2** (`store.py`) — vier neue Tabellen (`users`/`invites`/`recovery_codes`/
   `ui_sessions`), rein additiv, `SCHEMA_VERSION` `"1"`→`"2"` per `INSERT ... ON CONFLICT DO
   UPDATE` (vorher `INSERT OR IGNORE` — ein Prozess, der eine alte Schema-1-Datei öffnet,
   migriert jetzt automatisch beim ersten Start). Vollständige Methodenliste aus Plan §2.3
   (Nutzerakten/Einladungen/Recovery-Codes/UI-Sessions) 1:1 umgesetzt, neue Dataclasses
   `UserRow`/`InviteRow`/`SessionRow` in `models.py` (`SessionRow` trägt `session_hash`/
   `csrf_hash`, nie Klartext — dieselbe Hash-only-Disziplin wie Token/Codes, P5-K).
   **S7 dabei vollständig geschlossen:** `purge_expired()` deckt jetzt auch `ui_sessions`
   (absolut abgelaufen oder >7 Tage widerrufen) und `invites` (abgelaufen oder >7 Tage
   konsumiert) ab — die in Step 1 dokumentierte Lücke („Tabellen existieren erst in Step 2")
   ist damit geschlossen, `phase4_auth/CLAUDE.md`s S7-Zeile nachgezogen.
4. **`userdir.py`** — `UserDirectory.get()` liest live (kein Cache, **schließt O1 strukturell**:
   eine Provisionierung wirkt jetzt ohne Neustart), entschlüsselt `totp_secret_enc` mit AAD =
   Space-Name, fängt `SecretBoxError` ab (Log-Warnung, `totp_secret=None` statt Absturz) — **das
   ist S6s endgültige, strukturelle Schließung**, der `record.get(...)`-Übergangsfix aus Step 1
   ist jetzt entfernt (Zeile im Findings-Register bei `phase4_auth/CLAUDE.md` entsprechend
   nachgezogen: „geschlossen (P5 Step 1)" statt „strukturell erst in Step 2").
5. **`flows.py`/`routes.py`/`mcpserver/app.py`/`scripts/serve.py` auf `UserDirectory` umgestellt**
   — Advisor-Vorgabe befolgt: **verhaltensneutral**, nicht durch umgeschriebene Tests nur
   behauptet. In `test_flows.py`/`test_routes.py` änderte sich ausschließlich die
   `users`-Fixture-Konstruktion (jetzt `store.upsert_user(...)` + `UserDirectory(store, dek=...)`
   statt eines rohen Dicts) — alle Assertions blieben unverändert. **Zwei Ausnahmen, explizit
   dokumentiert statt still verschwunden:** `test_broken_user_record_yields_generic_login_failure`
   und `test_unknown_space_and_broken_record_are_indistinguishable` konnten ihren ursprünglichen
   Testfall (`{SPACE: {}}`, ein Dict ohne `"pwd"`/`"totp"`) nicht mehr herstellen — genau das IST
   S6s strukturelle Schließung (`store.get_user()` liefert nie ein unvollständiges Zwischending).
   Beide auf den jetzt einzig erreichbaren „kaputten Datensatz"-Fall umgestellt: ein TOTP-Seed,
   der mit einem ANDEREN DEK versiegelt wurde (z. B. nach einem DEK-Rotationsfehler) — beweist
   dieselbe Eigenschaft (generischer Fehlschlag, kein Absturz) unter der neuen Architektur.
   Neuer expliziter Test `test_flows_still_authenticate_with_userdirectory` (Plan-Namensvorgabe).
6. **`import_users_to_db.py`** — `--dry-run` Standard, `--apply` schreibt, `--force` überschreibt
   vorhandene Zeilen. Liest ausschließlich `load_users_from_keyring()` (nie das
   Credential-Snapshot). `totp_confirmed_at` übernimmt den ursprünglichen `created_at`-Wert (die
   Seeds sind live bewiesen, kein „unconfirmed"-Zustand für Bestandsnutzer). Bricht laut ab,
   wenn kein DEK geladen werden kann und der Keyring nicht leer ist.

**Kollateralberührungen außerhalb der Step-2-Dateiliste, dokumentiert (gleiche Kategorie wie
`oauth_smoke.py` in Step 1):** `phase2_mcp/scripts/serve.py` (Pflicht — `OAuthConfig.users`
ändert den Typ), `phase2_mcp/scripts/mcp_smoke.py` + `phase4_auth/scripts/oauth_smoke.py` +
`phase2_mcp/tests/{test_app,test_asgi_bearer,test_request_log,test_serve}.py` +
`phase4_auth/tests/test_oauth_smoke.py` (alle bauten `OAuthConfig(...users=...)` mit einem
rohen Dict). `phase4_auth/systemd/sharefyx-mcp.service` + `phase3_edge/tests/test_units.py`:
`LoadCredentialEncrypted=auth-users:...` entfernt (der Code liest diese Datei seit diesem
Commit nirgends mehr — dieselbe „totes Gewicht sofort abbauen"-Disziplin wie beim
`spaces.cred`-Fund in P4, nicht wie damals erst beim nächsten Unit-Umbau liegen gelassen),
`auth-dek:/etc/sharefyx/auth-dek.cred` dafür neu. `authserver/users.py :: load_users()` (die
Credential-Datei-Variante, nicht `load_users_from_keyring()`) ist jetzt echter toter Code —
bewusst NICHT gelöscht (außerhalb der Step-2-Dateiliste), Docstring korrigiert, vorgemerkt für
einen künftigen Rückbau, sobald `auth-users.cred`/der Keyring-Eintrag laut Migrations-Reihenfolge
unten formal abgelöst sind.

**Verifiziert, nicht nur behauptet:** `pytest -q` → **414/414 grün** (412 zu Sessionsende, +2 aus
den beiden Advisor-Nachträgen unten). Zusätzlich beide Smoke-Skripte real gelaufen (nicht nur
`pytest` grün behauptet, dreimal — einmal zu Sessionsende, je einmal nach jedem Advisor-Fund):
`mcp_smoke.py --json` → 12/12, `oauth_smoke.py --json` (In-Process-Default, echter
`UserDirectory`+DEK-Pfad) → **11/11** — der volle OAuth-Login-Fluss (Passwort + TOTP, jetzt über
verschlüsselte Seeds in `auth.sqlite3` statt einem Dict) funktioniert nach dem Umbau unverändert.
`git diff` bleibt auf den Tabu-Pfaden (`storage/`, `mcpserver/tools.py`/`permissions.py`/
`server.py`) leer.

**Zwei Advisor-Durchläufe vor dem Commit (dieselbe Session, wie in
`feedback_advisor_before_commit` festgehalten), drei echte Lücken gefunden, alle vor dem Commit
geschlossen, keine danach:**

1. Diese Datei dokumentierte Step 2 bereits als abgeschlossen, aber Root-`CLAUDE.md`s „Nächster
   Schritt" stand noch auf „Step 2" — dieselbe Drift-Kategorie, die diese Zeile in P4 schon
   dreimal betraf. Nachgezogen auf Step 3, mit datierter Korrekturnotiz statt stillem Fix.
2. Der neue `if accepted_counter is not None:`-Guard in `flows.py :: submit_consent()`
   (Recovery-Code-Zweig) war unbewiesen — der Session-Text behauptete, er sei durch
   `test_totp_replay_is_rejected_without_burning_the_stored_counter` gedeckt, aber dieser Test
   durchläuft laut eigener Beschreibung ausschließlich den TOTP-Zweig, nie den Recovery-Zweig.
   Neuer Test `test_recovery_code_login_does_not_touch_totp_counter` (`test_flows.py`) schließt
   das: Login mit einem Recovery-Code, danach `store.get_totp_counter(SPACE)` weiterhin `None`.
   Ohne diesen Test hätte eine Regression den TOTP-Replay-Zähler nach jedem Recovery-Login
   stillschweigend auf `None` zurückgesetzt — sicherheitsrelevant, nicht kosmetisch.
3. **Zweiter Durchlauf, echter Bug, nicht nur ein Test-Loch:** `users.consume_recovery_code()`
   mutiert (stempelt `used_at` in derselben Transaktion) und wurde VOR dem Passwort-Gate
   aufgerufen — ein Recovery-Code, korrekt eingegeben, aber mit einem Tippfehler im
   Passwortfeld, wurde dabei unwiderruflich verbrannt, ohne dass der Login gelang. Exakt das
   Spiegelbild der Lehre zwei Zeilen darunter im selben Modul („Zähler erst nach VOLLSTÄNDIGEM
   Erfolg hochsetzen"), nur auf der anderen Verzweigung übersehen. Fix: `totp_ok = password_ok
   and users.consume_recovery_code(...)` — Argon2id läuft weiterhin unconditional (Enumerations-
   schutz unberührt, ~55ms dominieren die paar µs SQLite-Lookup um Größenordnungen). Neuer Test
   `test_wrong_password_with_valid_recovery_code_does_not_burn_it`: falsches Passwort + gültiger
   Code → `ErrorPage`, derselbe Code funktioniert im nächsten Versuch mit korrektem Passwort noch.

Ein vom ersten Advisor-Durchlauf genannter Punkt (Schema-1→2-Migration gegen eine reale
Alt-Datenbank, nicht nur eine frisch angelegte) war bereits vorhanden
(`test_schema_migrates_from_v1_to_v2_without_data_loss`, baut eine echte Schema-1-DB von Hand,
öffnet sie über den normalen `AuthStore`-Konstruktor, prüft Datenerhalt UND Versions-Bump) —
falscher Alarm, im Advisor-Kontext fehlte lediglich der Diff-Ausschnitt, der das gezeigt hätte.

**Live-Runbook „Migration der Nutzerakten" (Nikinger-Aktion, Reihenfolge ist entscheidend —
Plan §2.6, Advisor-Vorgabe dieser Session):**

```
# 0) VORAUSSETZUNG, bevor irgendetwas installiert wird: der DEK muss existieren, BEVOR die
#    neue Unit-Zeile (LoadCredentialEncrypted=auth-dek:...) aktiv wird — sonst startet der
#    Dienst gar nicht mehr (dieselbe Falle wie spaces.cred in P4).
python -c "from authserver.config import generate_data_encryption_key, encode_data_encryption_key; \
  print(encode_data_encryption_key(generate_data_encryption_key()))" \
  | sudo systemd-creds encrypt --name=auth-dek - /etc/sharefyx/auth-dek.cred
sudo chmod 600 /etc/sharefyx/auth-dek.cred

# 1) Units installieren (bringt die neue auth-dek-Zeile UND entfernt die alte auth-users-Zeile)
sudo phase3_edge/scripts/install_units.sh
sudo systemctl restart sharefyx-mcp   # `users`-Tabelle ist noch leer -> UserDirectory(dek=...)
                                       # startet klaglos, aber noch niemand kann sich anmelden
systemctl status sharefyx-mcp

# 2) Migration, erst --dry-run, dann --apply (Backup vorher empfohlen, wie immer vor Schreiben
#    gegen die reale auth.sqlite3)
STATE_DIRECTORY=/var/lib/sharefyx python phase4_auth/scripts/import_users_to_db.py
STATE_DIRECTORY=/var/lib/sharefyx python phase4_auth/scripts/import_users_to_db.py --apply

# 3) Restart, damit UserDirectory die migrierten Zeilen sieht (O1 ist zwar geschlossen — kein
#    Cache mehr —, aber die Zeilen existieren ja erst nach diesem --apply-Lauf)
sudo systemctl restart sharefyx-mcp

# 4) Beide Nutzer melden sich am Connector an (UI kommt erst in Step 3/6) — ERST DANACH weiter.
#    Login niklas, Login fabian — beide mit unverändertem Passwort/TOTP.

# 5) Erst nachdem Schritt 4 für BEIDE bestätigt ist: alte Credential-Datei + Keyring-Eintrag
#    entfernen (nicht vorher — Lehre aus spaces.cred: eine Credential-Zeile und die Realität
#    dürfen nie auseinanderlaufen).
sudo rm -f /etc/sharefyx/auth-users.cred
python -c "import keyring; keyring.delete_password('nikinger-space', 'auth-users')"
```

**Nächster Schritt (konkret):** Drei Dinge stehen aus, alle Sache des Nikingers, keine davon
blockiert den nächsten Code-Step:

1. **Aus Step 1 weiterhin offen:** die S3/S4-Live-Gegenprobe gegen `token_families`
   (`resource`/`scope` der laufenden Verbindungen) vor dem nächsten Restart — siehe Absatz oben.
2. **Aus Step 1 weiterhin offen:** `sudo systemctl enable --now sharefyx-purge.timer`.
3. **Neu aus Step 2:** das Migrations-Runbook oben, in genau dieser Reihenfolge — kann mit (1)
   kombiniert werden, da beide denselben `install_units.sh`-Lauf und Restart teilen.

Code-seitig kann parallel weitergehen: Step 3 (Sessions, CSRF, Login-Seiten — neues Paket
`phase5_ui/` mit `webui/{config,security,sessions,pages,routes_auth,errors}.py`).
