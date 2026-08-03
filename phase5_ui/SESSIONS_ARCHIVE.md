---
status: live
purpose: Archiv älterer Session-stopped-Blöcke aus phase5_ui/CLAUDE.md, newest-first, verbatim
read-when: Audit vergangener Sessions dieser Phase; NICHT für normalen Session-Start
detail: L3
up: CLAUDE.md
updated: 2026-08-03 (dritter Block archiviert, Rotation nach Step 3)
---

# Session-Archiv — Phase 5 Web-UI, REST-API, Auth-Selbstverwaltung

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

---

## Session stopped — 2026-08-02 (Step 1: Sicherheitsbefunde S2–S8 vollständig geschlossen)

**Für den nächsten, kalten Leser:** zweite Session der Phase. Der Nikinger gab grünes Licht für
Step 1 mit einer Einschränkung: falls der Plan Voraussetzungen nennt, die noch nicht erfüllt
sind, zuerst das klären. Genau das traf zu — Details unten unter „Plan-Drift, vor jedem Fix
geklärt". Alle sieben Befunde (S2–S8) sind geschlossen, `pytest -q` lief vor Beginn bei 333/333
und steht am Ende bei **353/353**.

**Plan-Drift, vor jedem Fix geklärt (nicht blind übernommen):** Plan §5 Step 1 nennt für S6 den
Fix „entfällt strukturell mit `UserDirectory.get()`" und für S7 eine Erweiterung von
`purge_expired()` um `ui_sessions`/`invites` — beides sind Schema-2/`UserDirectory`-Artefakte
aus **Step 2**, der noch nicht gebaut ist (`authserver/userdir.py` existiert nicht,
`SCHEMA_VERSION` steht weiterhin auf `"1"`, keine `ui_sessions`/`invites`-Tabelle). Statt auf
nicht existierenden Code zu bauen: S6 bekam die vom Sicherheits-Review selbst vorgeschlagene
Fix-Skizze direkt auf dem aktuellen `Mapping`-Zugriff (`record.get(...)` statt `record[...]`);
S7 bekam den Timer plus die Längenbegrenzung jetzt, die `ui_sessions`/`invites`-Abdeckung bleibt
wie vom Plan selbst vorgesehen (`test_purge_removes_expired_sessions_and_invites` trägt im Plan
den Zusatz „nach Step 2 zu ergänzen") ein Nachtrag für Step 2. Advisor-Review vor Beginn hat
diese beiden Stellen bestätigt und zusätzlich zwei Live-Risiken benannt (S3/S4 könnten laufende
Connector-Token invalidieren) — read-only DB-Gegenprobe war von der Auto-Mode-Klassifizierung
blockiert; Code-Analyse zeigt aber, dass `resource`/`scope` deterministisch aus `settings`
abgeleitet werden (`config.py :: AuthSettings.resource`, `flows.py`s `scope or "space"`-Default)
und deshalb für alle real ausgestellten Token übereinstimmen — siehe „Nächster Schritt" unten,
diese Annahme sollte vor einem echten Restart einmal gegengelesen werden.

**S2 — `refresh_token`-Grant prüft jetzt `client_id`:** `store.py :: rotate_refresh()` bekam
einen Pflicht-`client_id`-Parameter, geprüft gegen `token_families.client_id` **vor** der
`rotated_at`-Prüfung — ein Mismatch ist ein früher `return None` (`invalid_grant`), **kein**
Familienwiderruf (ein falscher `client_id` ist kein Replay, sonst wäre der neue Check selbst ein
Fernauslöser gegen fremde, legitime Familien — das ist laut Plan „die wichtigere Hälfte").
`flows.py :: issue_token()` verlangt `client_id` jetzt auch im Refresh-Zweig. Alle bestehenden
Aufrufer (`oauth_smoke.py` Schritte 8/9, mehrere Store-/Flow-Tests) angepasst.

**S3/S4 — Audience- und Scope-Check bei der Bearer-Auflösung:** `OAuthTokenResolver.__init__`
nimmt jetzt ein Pflicht-`expected_resource` entgegen, `resolve()` lehnt ab, wenn
`record.resource` nicht passt (S3) oder `"space"` nicht in `record.scope.split()` steht (S4).
`mcpserver/app.py :: create_app()` verdrahtet `expected_resource=oauth.settings.resource`.

**S5 — Redirect-Query-Merge statt Verstümmelung:** `routes.py :: _authorize_response()` baut
die Redirect-URL jetzt über `urlsplit`/`parse_qsl`/`urlencode`/`urlunsplit` und mischt
`code`/`state`/`error` in eine vorhandene Query hinein, statt bedingungslos ein zweites `?`
anzuhängen.

**S6 — kein `KeyError` mehr bei kaputten Nutzerakten:** `flows.py :: submit_consent()` liest
`record.get("pwd")`/`record.get("totp", "")` statt per Index — ein unvollständiger Datensatz
ergibt jetzt dieselbe generische Fehlermeldung wie ein unbekannter Space (Enumerationsschutz
bleibt intakt, `totp.verify()` fing ungültiges Base32 bereits vorher ab).

**S7 — Purge-Timer + Längenbegrenzung:** `phase5_ui/systemd/sharefyx-purge.{service,timer}`
(täglich, ruft `authctl.py purge-expired`) — `install_units.sh`s `SYSTEMD_SRCS` um
`phase5_ui/systemd` erweitert (sonst wäre der Timer totes Gewicht, Advisor-Fund). **Live noch
nicht aktiv:** anders als `sharefyx-backup.timer` (dessen Enable-Schritt im Inbetriebnahme-
Runbook bereits gelaufen ist) gibt es für `sharefyx-purge.timer` noch **keinen** ausgeführten
Enable-Schritt — `install_units.sh` kopiert die Unit-Dateien nach `/etc/systemd/system/`, das
allein startet keinen Timer. Nikinger-Aktion, sobald `install_units.sh` das nächste Mal läuft:
`sudo systemctl enable --now sharefyx-purge.timer` (analog zu Schritt 5 im bestehenden Runbook
für `sharefyx-backup.timer`). Bis dahin ist S7 code-seitig geschlossen, aber operativ noch
inaktiv — `purge_expired()` läuft weiterhin nur, wenn jemand `authctl.py purge-expired` von
Hand ruft. Zusätzlich `ratelimit.py :: MAX_SPACE_LEN = 128` — `space` kommt unauthentifiziert
aus dem Formular und war ohne Längenbegrenzung ein Disk-DoS-Vektor als PRIMARY KEY in
`login_attempts`.

**S8 — `install_units.sh` sourced nicht mehr blind:** ersetzt durch ein striktes
KEY=VALUE-Parsen (kein `eval`, keine Shell-Interpretation) statt `source`. **Bewusste Abweichung
vom Plan-Wortlaut:** die Plan-Tabelle nannte eine root-Ownership-Prüfung per `stat`
(„Abbruch wenn nicht root") — das widerspräche dem im Repo selbst dokumentierten Modell, in dem
`local.env` `savefyx` gehört und von `savefyx` angelegt wird (README.md, Runbooks). Stattdessen
die vom Sicherheits-Review selbst vorgeschlagene Fix-Skizze („grep-basiertes Parsen") gewählt,
die dieselbe Schwachstelle (beliebiger Bash-Code aus einer `savefyx`-schreibbaren Datei, als
root ausgeführt) ohne die Ownership-Kollision schließt. Manuell gegen eine Injection-Zeile
(`touch /tmp/PWNED`) verifiziert, bevor der Pytest-Test geschrieben wurde: Skript bricht mit
`ABBRUCH: ... kein KEY=VALUE` ab, keine Datei entsteht.

**Verifiziert, nicht nur behauptet:** `pytest -q` → **353/353 grün** (333 + 20: 2
`test_authserver_store.py` + 4 `test_resolver.py` + 2 `test_routes.py` + 3 `test_flows.py` + 2
`test_ratelimit.py` + 5 `test_units.py` + 2 `test_security_review_register.py`, neue Datei).
`test_security_review_register_is_empty` (neu) parst die S2–S8-Tabelle in
`phase4_auth/CLAUDE.md` direkt und schlägt fehl, sollte je eine Zeile wieder ohne ✅ dastehen.
`phase4_auth/CLAUDE.md`s S2–S8-Tabelle im selben Commit nachgezogen (Status-Spalte ergänzt,
veralteter „Keiner von S2–S8 ist gefixt"-Absatz durch eine datierte Korrekturnotiz ersetzt —
dieses Dokument ist 📗 live gepflegt, kein 📕-Snapshot, deshalb direkt korrigiert statt in einem
separaten Nachtrag dupliziert). `git diff` bleibt außerhalb der P5-B-Berührungsfläche
(`authserver/`, `mcpserver/app.py`, `phase3_edge/scripts/install_units.sh`,
`phase3_edge/tests/test_units.py`, neue `phase5_ui/systemd/`) leer auf `storage/`,
`mcpserver/tools.py`, `mcpserver/permissions.py`, `mcpserver/server.py` (Akzeptanzkriterium 18).

**Kleine Abweichung von P5-B, dokumentiert statt still erweitert:** `phase4_auth/scripts/
oauth_smoke.py` steht nicht auf Plan §5 Step 1s Dateiliste — geändert wurden zwei
`grant_type="refresh_token"`-Aufrufe (Schritte 8/9), die jetzt `client_id` mitschicken müssen
(S2-Signaturänderung an `flows.issue_token()`). Gleiche Kategorie wie `mcp_smoke.py` im
P4-Schnitt: eine erzwungene Anpassung an eine geänderte Signatur, kein neuer Scope-Griff.

**Nächster Schritt (konkret):** Zwei Dinge, bevor Step 2 beginnt — beide Sache des Nikingers,
keine Claude-Code-Aufgabe:

1. **Live-Voraussetzung vor dem nächsten `sudo systemctl restart sharefyx-mcp`:** S3/S4 fügen
   neue Ablehnungsbedingungen in den Bearer-Auflösungspfad ein, der gerade zwei echte
   Verbindungen (`niklas`, `fabian`) bedient. Code-Analyse zeigt, dass `resource`/`scope` für
   real ausgestellte Token deterministisch mit den jetzt geprüften Erwartungswerten
   übereinstimmen sollten (siehe „Plan-Drift" oben) — das ist aber eine Ableitung aus dem Code,
   **keine** Live-Verifikation (der read-only DB-Zugriff war für Claude Code in dieser Session
   durch die Auto-Mode-Klassifizierung blockiert). Vor dem nächsten Restart einmal gegenlesen:
   ```
   sqlite3 -readonly /var/lib/sharefyx/auth.sqlite3 \
     "SELECT space, scope, resource FROM token_families WHERE revoked_at IS NULL;"
   ```
   **Bestehensbedingung:** jede Zeile trägt `resource = https://savefyx-vmware-virtual-platform.tail89fc2a.ts.net/mcp`
   und `scope` enthält das Wort `space`. Trifft das nicht zu, loggt der Restart beide Nutzer aus
   (ein Client **darf** laut `SUPPORTED_SCOPES` legitim nur `offline_access` ohne `space`
   angefordert haben — das ist der konkrete Fehlfall, den S4 dann greifen lässt).
2. **`sudo systemctl enable --now sharefyx-purge.timer`** nach dem nächsten
   `install_units.sh`-Lauf (siehe S7 oben) — ohne diesen Schritt bleibt der Purge-Timer
   installiert, aber inaktiv.

Danach: Step 2 (Auth-Datenmodell Schema 2, `secretbox.py`, `userdir.py` — schließt auch die
S6/S7-Restarbeit von oben strukturell ab).

---

## Session stopped — 2026-08-02 (Step 0: Haushalt, Rückbau, Doku-Drift, P3 komplett ✅)

**Für den nächsten, kalten Leser:** erste Session der Phase. Der Nikinger bat um die ersten
Kommandos für den Phasenstart; Step 0 B/D (rein lesend) liefen direkt in dieser Session (das
Environment **ist** die VM — `savefyx-VMware-Virtual-Platform`, `/etc/sharefyx/*.cred`
vorhanden), Step 0 A (Rückbau) und C (Doku-Drift) sind Claude-Code-Arbeit und liefen im Anschluss
ebenfalls autonom, wie vom Nikinger freigegeben („start with the initial steps you can do now
without needing me"). Der Nikinger hat A.7 (`install_units.sh` + Restart + Live-Check +
`spaces.cred`-Löschung) noch in derselben Session live nachgezogen, plus einen eigenen
Restore-Check-Lauf und drei Lesezugriffe über den echten Connector — Details unten. **Step 0
ist damit vollständig abgeschlossen.**

**B — Verifikationsdurchlauf (vor jeder Änderung):** `pytest -q` → 347 grün (bestätigt den
dokumentierten Ausgangsstand). Alle `up:`/`down:`/Markdown-Links in allen 26 `.md`-Dateien lösen
auf (zwei harmlose False-Positives aus Inline-Code-Beispielen in
`docs/DOC_LAYERS_CONVENTION.md`, keine echten Links). Jede über 40 KB liegende `.md` ist korrekt
📕/📦. Jeder Phase-Head trug genau einen `## Session stopped`-Block. Jede getrackte `.md` hatte
eine Zeile in `docs/INDEX.md`.

**D — Umgebungsinventar:** Python 3.12.3, sqlite3 3.45.1, systemd 255, Tailscale 1.98.9 (Funnel
live auf Port 8765). Ports 8080/8081/9090 frei → Kandidat für Staging (**V36**). `cryptography`
liegt bereits im `.venv` (49.0.0, transitive Abhängigkeit von Authlib/joserfc/SecretStorage,
`AESGCM` importiert sauber) — **noch nicht** in einem `pyproject.toml` gepinnt, das ist Step 2s
Aufgabe (**V28** teilweise aufgelöst: Version bekannt, Pinning offen). Kein `vnstat` installiert
→ **V12** bleibt offen. 32 GB frei auf `/`.

**A — Rückbau `spaces.cred` + P2-Token-Reste** (`docs/concepts/PHASE4_CLOSEOUT_HANDOVER.md`
§4.5):

1. `phase4_auth/systemd/sharefyx-mcp.service`: Zeile `LoadCredentialEncrypted=spaces:
   /etc/sharefyx/spaces.cred` entfernt.
2. **Pfaddrift im Plan korrigiert, nicht blind übernommen:** der Plan nannte
   `phase2_mcp/scripts/export_space_map.py` — das Skript lag tatsächlich unter
   `phase3_edge/scripts/export_space_map.py` (P3 Step 3 hat es dort gebaut). Gelöscht wurde die
   reale Datei, nicht die im Plan genannte (die nie existierte).
3. `phase2_mcp/scripts/issue_token.py` gelöscht.
4. `phase2_mcp/mcpserver/credentials.py` auf `hash_token()` reduziert — `issue`/`revoke`/
   `load_space_map`/`load_space_map_from_keyring`/`save_space_map`/`credential_path`/
   `generate_token` sowie die Keyring-Konstanten entfernt, `hash_token` bewusst belassen
   (`asgi.py` dokumentiert die Byte-Identität mit `authserver.crypto.hash_secret`, Plan-Vorgabe).
5. `mcpserver/auth.py :: KeyringTokenResolver` entfernt (letzter Aufrufer war `TokenPathASGI`,
   selbst seit dem P4-Schnitt tot) — `SpaceResolver`-Protokoll bleibt stehen
   (`authserver.resolver.OAuthTokenResolver` erfüllt es strukturell).
6. `mcpserver/app.py`s Docstring korrigiert (behauptete noch, `KeyringTokenResolver` sei
   „weiterhin gebraucht von `issue_token.py`" — das Skript existiert nicht mehr).
7. Tests bereinigt: `test_auth.py` 4→1 (nur `test_principal_repr_hides_token` bleibt),
   `test_credentials.py` 12→1 (nur `test_hash_token_is_stable_hex64` bleibt),
   `test_units.py :: test_unit_loads_credential_encrypted` prüft jetzt zusätzlich die
   **Abwesenheit** der `spaces:`-Zeile statt nur ihre Anwesenheit.
   **`pytest -q` → 333 grün (347 − 14, Aufschlüsselung oben, keine neue Lücke).**
8. **Nikinger-Aktion, live ausgeführt (2026-08-02, gleiche Session):** `restore_check.sh`
   selbst wiederholt (identischer HEAD, `ok:true` — siehe Nebenfund unten), danach
   `sudo phase3_edge/scripts/install_units.sh` → `sudo systemctl restart sharefyx-mcp` →
   `curl http://127.0.0.1:8765/health` → `{"status":"ok",…,"uptime_s":14}` → erst danach
   `sudo rm -f /etc/sharefyx/spaces.cred`, exakt in dieser Reihenfolge. **Step 0 A damit
   vollständig.**

**Nebenfund, jetzt echte Abnahme statt nur Kandidat:** P3 Zeile 13 (Restore-Nachweis) war seit
dem 2026-07-29-Handover offen. Claude Code hatte `restore_check.sh` zunächst selbst gegen das
frischeste Bundle gefahren (`ok:true`) — bewusst nur als Kandidatenbeleg gewertet, weil der
Session-Auftrag „jeden End-to-End-Test gegen das echte Datenverzeichnis" dem Nikinger vorbehält
(Advisor-Fund dieser Session). Der Nikinger hat den identischen Befehl danach selbst ausgeführt
(`head: 3756c26a7d826def1246bb4dc826e9ee10e764b3`, `ok:true`, identisch zum Kandidatenlauf).
**Phase 3 steht damit bei 13/13, Status ✅.** `phase3_edge/CLAUDE.md`, `ROADMAP.md`,
Root-`CLAUDE.md` und `docs/INDEX.md` nachgezogen.

**Live-Verifikation nach dem Restart (Nikinger, über den echten Connector):** drei Lesezugriffe
gegen die neu gestartete Unit — `list_spaces` (`niklas`: 7 Items/`writable:true`, `fabian`:
2 Items/`writable:false` — Rule 4 sichtbar korrekt) und `search_items` (3 aktive Items im
eigenen Space, jüngstes `P4 TTL-Test` v2 vom 2026-07-30 — derselbe Datensatz wie beim
P4-Abnahmezeile-9-Beweis, also Kontinuität über den Rückbau-Restart hinweg belegt). Kein
Schreibzugriff (bewusst, war nicht gefragt).

**Zwei P5-relevante Beobachtungen aus diesem Live-Check, für spätere Steps vorgemerkt:**

- **`list_spaces`s `item_count` zählt inklusive Archiv, `search_items`s Default nicht.**
  `niklas` zeigt 7 in `list_spaces`, aber nur 3 aktive Treffer in `search_items`
  (`include_archived=false` per Default) — kein Bug, aber ein UI-Fallstrick: die Rail (Step 6)
  würde „7" zeigen, während die Liste 3 Zeilen hat. **Für Step 6 vormerken:** entweder beide
  Zahlen anzeigen (`3 von 7`) oder `item_count` explizit als „inklusive Archiv" beschriften,
  bevor irgendein UI-Zähler daraus abgeleitet wird.
- **`fabian`s Space hat bereits zwei echte Items**, kein Leerzustand. Für die
  Zwei-Personen-Abnahme (Akzeptanzkriterium 12/17: fremder Space read-only, keine
  Schreib-Bedienelemente im DOM) heißt das: es gibt schon echten Testinhalt, kein
  künstlich anzulegender Leerraum nötig, wenn Fabian in Step 9 einsteigt.

**C — Doku-Drift geschlossen:**

1. `ROADMAP.md`: P5-Zeile ⬜→🔄 (mit Status-Absatz + Scope-Erweiterung Auth-Selbstverwaltung),
   P3-Zeile 🟡→✅ (Restore-Nachweis-Nachtrag), `down:`-Liste um die P4-/P5-Pläne ergänzt (fehlten
   bisher, kleine unabhängige Lücke, beiläufig geschlossen).
2. Root-`CLAUDE.md`: „Aktive Phase" auf P5 umgehängt (P4-Absatz bleibt als abgeschlossene
   Historie stehen, „Nächster Schritt" nachgezogen), `down:` auf `phase5_ui/CLAUDE.md`,
   `updated:` gesetzt. „Noch nicht entschieden": der Web-UI-Punkt ist mit P5-V entschieden,
   datierte Korrekturnotiz statt ersatzloser Streichung.
3. `README.md`: **[VERIFY] V34 aufgelöst** — der Snapshot war bereits größtenteils überarbeitet
   (Architekturdiagramm, „ab Phase 5" waren schon korrekt), aber der komplette
   „Token ausgeben, rotieren, widerrufen"-Abschnitt beschrieb noch die jetzt gelöschten Skripte.
   Ersetzt durch einen Abschnitt, der auf OAuth 2.1 + DCR (P4) und die kommende
   Selbstverwaltung (P5 Step 4) verweist. Setup-Callout auf den aktuellen Fünf-Phasen-Stand
   gehoben.
4. `docs/INDEX.md`: neuer Abschnitt „Active phase (5 — Web-UI)" mit den Zeilen für
   `phase5_ui_plan.md`, `PHASE4_CLOSEOUT_HANDOVER.md` und diesen Phase-Head; P4 bleibt unter
   „Completed phases" (war dort schon korrekt einsortiert, keine Änderung nötig); Größenangaben
   für `phase3_edge/CLAUDE.md`/`SESSIONS_ARCHIVE.md` und `phase4_auth/CLAUDE.md`-Zeile
   (P3-Status) nachgezogen.

**Nächster Schritt (konkret):** Step 0 ist vollständig — keine offenen Punkte mehr, weder
code- noch live-seitig. Step 1 (Sicherheitsbefunde S2–S8, `docs/concepts/
P4_SECURITY_REVIEW_2026-07-29.md` vorher lesen) kann beginnen, sobald der Nikinger grünes Licht
gibt.

---

