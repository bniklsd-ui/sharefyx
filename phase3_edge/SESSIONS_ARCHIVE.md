---
status: live
purpose: Archiv älterer Session-stopped-Blöcke aus phase3_edge/CLAUDE.md, newest-first, verbatim
read-when: Audit vergangener Sessions dieser Phase; NICHT für normalen Session-Start
detail: L3
up: CLAUDE.md
updated: 2026-07-27 (Step 5 archiviert)
---

# Session-Archiv — Phase 3 Exposure & Betrieb

## Session stopped — 2026-07-27 (Step 5: Backup und Restore-Nachweis)

**Ergebnis:** Step 5 abgeschlossen. `backup_data_root.sh` (git bundle + Verify + Retention),
`restore_check.sh` (Klon + HEAD/Tree-Vergleich), `sharefyx-backup.service`/`.timer` (Platzhalter,
nicht installiert — Step 7).

**`git bundle create` schlägt auf einem leeren Repo fehl** ("Refusing to create empty bundle") —
jede Testfixture (`data_root`) legt deshalb einen echten Commit an, nicht nur ein leeres
`git init`.

**Zeitstempel-Kollisionsfalle umgangen, nicht nur vermieden (Advisor-Fund, dieselbe Klasse Fehler
wie `mcp_smoke.py` in P2, siehe archivierter Step-7-Block):** `test_backup_retention_keeps_newest_n`
läuft das Skript **nicht** in einer Schleife (bei Sekundenauflösung würden mehrere Bundles
denselben Dateinamen bekommen und sich überschreiben). Stattdessen legt der Test fünf Fake-Bundles
mit distinktem, sortierbarem Namen vor und ruft das Skript nur einmal für das echte, aktuelle
Bundle auf. Der Dateiname selbst trägt jetzt zusätzlich Mikrosekunden (`%6N`, keine Doppelpunkte)
statt nur Sekunden — doppelte Absicherung für den Fall eines künftigen Schleifen-Aufrufs.

**`test_backup_fails_and_cleans_up_on_corrupt_bundle` — echte Korruption, nicht simuliert
(Advisor-Vorschlag umgesetzt):** ein frisch geschriebenes, gültiges Bundle besteht die eigene
`git bundle verify` selbstverständlich. Der Test schiebt stattdessen einen Fake-`git`-Wrapper vor
den echten auf `$PATH`, der `bundle verify` immer mit Exit 1 abbrechen lässt und alles andere an
das echte `git` durchreicht — prüft damit den tatsächlichen Cleanup-Zweig (`rm -f` + Exit ≠ 0),
nicht nur seine Absicht.

**`git bundle verify` schreibt die Ref-Liste auf stdout, die Bestätigung auf stderr** (empirisch
geprüft, nicht angenommen) — im Skript deshalb explizit `>&2` umgeleitet, sonst hätte Hard Rule 7
(stdout nur maschinenlesbares JSON) auf einem Zwischenschritt gebrochen, den der Plan nicht
erwähnt.

**`SHAREFYX_BACKUP_DIR` ist Konfiguration im Skript (Umgebungsvariable, kein Literal), aber ein
fester Wert in der Unit** (`/var/backups/sharefyx`, Plan §4 Step 5 "Ziel ist Konfiguration ...,
kein Literal im Skript"). Bewusst **kein** fünfter Platzhalter/`local.env`-Eintrag: anders als
`REPO_ROOT`/`DATA_ROOT` ist ein Backup-Zielverzeichnis kein Wert, der zwischen Maschinen
tatsächlich variieren muss — ein FHS-üblicher Pfad reicht, ohne `install_units.sh` und
`local.env.example` um eine fünfte Variable zu erweitern.

**`install_units.sh` unverändert lauffähig für die neuen Units:** es verarbeitet generisch alle
`*.service`/`*.timer` in `phase3_edge/systemd/` (so in Step 4 vorbereitet) — die zwei neuen
Backup-Units laufen ohne Skriptänderung durch dieselbe Platzhalter-Ersetzung und
Unresolved-Placeholder-Prüfung.

**`test_units.py` (Step 4) erweitert, nicht dupliziert:** zwei neue Tests
(`test_all_units_have_no_secret_shaped_value`, `test_all_units_have_no_hardcoded_machine_paths`)
laufen über **alle** Unit-Dateien im Verzeichnis, nicht nur die MCP-Unit — sonst hätte die
Token-Klartext-Versicherung aus Step 4 die beiden neuen Backup-Units stillschweigend
ausgenommen.

**Tests** (`phase3_edge/tests/test_backup_scripts.py`, alle sieben aus dem Plan, gegen
Wegwerf-Git-Repos unter `tmp_path`, nie den echten `DATA_ROOT`): `test_backup_creates_verifiable_bundle`,
`test_backup_emits_single_json_line_on_stdout`, `test_backup_retention_keeps_newest_n`,
`test_backup_fails_and_cleans_up_on_corrupt_bundle`, `test_restore_check_matches_head_and_tree`,
`test_restore_check_detects_divergence`, `test_scripts_have_no_hardcoded_paths`. Plus zwei in
`phase3_edge/tests/test_units.py` (siehe oben).

**Verifiziert:** `.venv/bin/python -m pytest -q` → **168/168 grün** (159 + 9 neue).

**Modul-Status oben nachgezogen** (Zeile 6: ⬜ → ✅, 9 Tests).

**Offen für den Nikinger, weiterhin unverändert:**
1. `mcp_smoke.py`/P3-N-Grenzfrage aus Step 2.
2. Tailscale ist auf dieser VM weiterhin nicht installiert — einziges Gate vor Step 7.

**Nächster Schritt (konkret):** Step 6 — Runbooks, `diagnose.sh`, Cloudflare-Rückbau. Der
Cloudflare-Uninstall selbst ist ein Befehl **für den Nikinger** (destruktive Aktion auf der
realen Maschine, außerhalb des Repos) — Claude Code liefert nur den Runbook-Text, führt ihn
nicht aus.

## Session stopped — 2026-07-27 (Step 4: systemd-Units)

**Ergebnis:** Step 4 abgeschlossen. `phase3_edge/systemd/sharefyx-mcp.service` (Platzhalter,
nicht auf der VM installiert), `phase3_edge/scripts/install_units.sh`, plus `/health` trägt jetzt
`uptime_s` (P3-I).

**`uptime_s` war im Plan §4 keinem Step zugewiesen — Lücke geschlossen, nicht stillschweigend
übersprungen (Advisor-Fund):** P3-I ("genau ein neues Feld") steht in §0.5, §1.1 und in Step 7s
Abnahmematrix (Zeile 1), aber in keinem der Steps 0–7 als Liefergegenstand. Step 6
(`diagnose.sh`, Prüfung 2) und der Disconnected-Runbook setzen das Feld aber voraus. Hier in
Step 4 gebaut, bevor Step 6 es braucht: `app.py :: create_app()` setzt `app.state.start_time =
time.monotonic()` **pro App-Instanz** (nicht Modulebene — sonst teilten sich mehrere
`create_app()`-Aufrufe, z. B. in Tests, einen Startzeitpunkt), `_health()` berechnet
`uptime_s = int(time.monotonic() - request.app.state.start_time)`. `app.py` steht in P3-Ns
Berührungsliste, keine Scope-Erweiterung.

**`test_health_ok` aus P2 korrekt rot geworden, wie von seinem eigenen Kommentar angekündigt:**
der Test prüft absichtlich die exakte Schlüsselmenge der `/health`-Antwort ("fängt eine spätere
Erweiterung um ein zusätzliches Feld ab"). Mit `uptime_s` dazu aktualisiert
(`{"status","service","version","uptime_s"}`), `isinstance(..., int)` und `>= 0` geprüft.
`test_health_leaks_no_space_names` bleibt unverändert grün — `uptime_s` leakt nichts.

**`local.env.example` trug echte Maschinenpfade dieser VM — korrigiert (Advisor-Fund):**
`REPO_ROOT`/`DATA_ROOT`/`VENV` zeigten auf `/home/savefyx/...`. P3-Js eigene Begründung für das
Platzhalterschema ist Maschinenunabhängigkeit ("der Kollege oder eine zweite VM sollen dasselbe
Repo benutzen können"), und §5 Akzeptanzkriterium 8 nennt „kein Maschinenzustand im Repo" — ein
kopiertes Beispiel mit dieser VMs echten Pfaden hätte plausibel, aber falsch ausgesehen. Jetzt
`/path/to/savefxy` etc.

**`install_units.sh` bricht vor jedem `/etc`- oder `systemctl`-Zugriff ab, wenn `local.env`
fehlt** — genau der Pfad, den der Test ausübt, ohne root-Rechte oder einen echten systemd
anzufassen. Verarbeitet generisch alle `*.service`/`*.timer` in `phase3_edge/systemd/` (Step 5
liefert die Backup-Units in dasselbe Verzeichnis, ohne dass dieses Skript sich ändern muss),
prüft nach der Platzhalter-Ersetzung per Regex, ob `__[A-Z_]+__` noch irgendwo übrig ist, und
löscht eine unvollständige Zieldatei sofort statt sie stehen zu lassen. **Die Unit ist nach
diesem Step bewusst noch nicht auf der VM installiert** — das ist Step 7.

**`V9` (`ProtectHome=read-only` + `ReadWritePaths` erlaubt Git-Commits im `DATA_ROOT`) bleibt
offen** — laut Plan nur zur Laufzeit prüfbar, `test_units.py` ist reines Textparsen. Der bereits
in Step 0 bestätigte Fund (Git-Identität `Space Server`/`space-server@localhost` liegt im
`DATA_ROOT` selbst, nicht nur in `~/.gitconfig`) ist der Ausgangspunkt für den ersten
Write-Test in Step 7 — dorthin verschoben, nicht hier vorweggenommen.

**Tests** (`phase3_edge/tests/test_units.py`, alle sechs aus dem Plan):
`test_unit_restarts_on_failure`, `test_unit_loads_credential_encrypted`,
`test_unit_binds_loopback_only`, `test_unit_has_no_secret_shaped_value`,
`test_unit_placeholders_are_unresolved_in_repo`,
`test_install_script_refuses_without_local_env` (kopiert `scripts/`+`systemd/` in ein
Wegwerf-Verzeichnis ohne `local.env` — hermetisch, unabhängig davon, ob auf dieser Maschine
zufällig ein echtes `phase3_edge/local.env` existiert). Plus die aktualisierten
`test_health_ok`/-Assertions in `phase2_mcp/tests/test_app.py`.

**Verifiziert:** `.venv/bin/python -m pytest -q` → **159/159 grün** (153 + 6 neue).

**Modul-Status oben nachgezogen** (Zeile 5: ⬜ → ✅, 6 Tests).

**Offen für den Nikinger (nicht blockierend für Steps 5–6, aber noch nicht gemeldet):**
1. `mcp_smoke.py`/P3-N-Grenzfrage aus Step 2 — ob `mcp_smoke.py` auf `configure_logging()`
   umgestellt werden soll (Zweizeiler), steht weiterhin offen.
2. Tailscale ist auf dieser VM weiterhin nicht installiert (Step 0) — einziges Gate vor Step 7.

**Nächster Schritt (konkret):** Step 5 — Backup- und Restore-Skripte (`git bundle` + Verify +
Retention), Backup-Timer. Beide Skripte laufen in Tests ausschließlich gegen Wegwerf-Git-Repos
unter `tmp_path`, nie gegen den echten `DATA_ROOT`.

## Session stopped — 2026-07-27 (Step 3: Credentials über systemd)

**Ergebnis:** Step 3 abgeschlossen. `credentials.py :: load_space_map()` liest jetzt zuerst ein
von systemd bereitgestelltes Credentials-Verzeichnis, Keyring bleibt Fallback.
`phase3_edge/scripts/export_space_map.py` (neu) exportiert die Space-Map aus dem Keyring als
JSON auf stdout, für `systemd-creds encrypt`.

**`[VERIFY]` V4 und V5 — bereits in Step 0 beantwortet, hier nur referenziert (kein zweiter
Inventarlauf):** V4 (`systemd-creds` vorhanden, systemd 255 ≥ 250, `has-tpm2` → partial →
Host-Key-Verschlüsselung) und V5 (`keyring.backends.SecretService.Keyring`, Priorität 5) stehen
im „Umgebungsstand"-Abschnitt oben und in `SESSIONS_ARCHIVE.md`, Step-0-Block.

**Plan §2.3 war mit sich selbst im Widerspruch — aufgelöst, nicht stillschweigend
weggelesen:** der Plantext sagt, `export_space_map.py` solle
„`credentials.load_space_map()` **aus dem Keyring** (explizit, nicht über die neue
Verzweigung)" lesen — aber `load_space_map()` **ist** ab diesem Step die neue Verzweigung, ein
Aufruf kann nicht zugleich sie selbst und ihre Umgehung sein. Auflösung (Advisor-Review): die
reine Keyring-Leselogik wurde in eine eigene Funktion `load_space_map_from_keyring()`
ausgelagert. `load_space_map()` ruft sie als Fallback; `export_space_map.py` ruft sie direkt.
Ein Leser, zwei Aufrufer, keine Verzweigung im Export-Pfad. `issue()`/`revoke()` bleiben laut
Plan-Vorgabe **unverändert** (0 Zeilen Diff) und rufen weiterhin `load_space_map()` auf — das ist
unschädlich, weil `$CREDENTIALS_DIRECTORY` in ihrem einzigen realen Aufrufkontext
(`issue_token.py`, interaktiv) nie gesetzt ist.

**Der Fallback-Warnhinweis geht auf den Modul-Logger, nicht auf `sharefyx.request`**
(Advisor-Fund): fehlt die Credential-Datei trotz gesetztem Verzeichnis, loggt `load_space_map()`
über `logging.getLogger(__name__)` — landet also auf dem normalen stderr-Handler aus
`configure_logging()`, nicht im JSON-Request-Log. Der Request-Logger ist laut Plan §3.1 für
`ev="tool"`/`ev="http"` reserviert; eine freie Textmeldung dort wäre zwar gültiges JSON
(`JsonLineFormatter` serialisiert auch einen bloßen String), aber strukturell falsch auf einem
Stream, dessen Vertrag eine Feld-Whitelist ist.

**Test-Ladepfad für `export_space_map.py` (Advisor-Fund):** `phase3_edge/` ist kein Python-Paket
(Plan §1.2), ein normaler `import` aus `phase2_mcp/tests/test_credentials.py` funktioniert
deshalb nicht. Geladen über `importlib.util.spec_from_file_location(...)` gegen den absoluten
Pfad — hält `capsys` für den stdout/stderr-Split nutzbar, im Unterschied zu einem
Subprocess-Aufruf. Da `export_space_map.py`s `from mcpserver import credentials` denselben
gecachten Modul-Objekt-Namen trifft wie der Testcode, wirkt der `fake_keyring`-Monkeypatch aus
`test_credentials.py` transparent auch dort — kein zweiter Fake nötig.

**Doku:** `README.md`, Abschnitt „Token ausgeben, rotieren, widerrufen" um „Rotation im
Dienstbetrieb (ab P3)" erweitert — der volle Vierschritt aus P3-M (Token neu ausgeben → Export →
`systemctl restart` → Connector-URL aktualisieren), inklusive des Satzes, dass ein vergessener
Restart wie „Connector kaputt" aussieht, aber ein 401 auf die alte Credential-Datei im tmpfs ist.

**Tests** (`phase2_mcp/tests/test_credentials.py`, alle sechs aus dem Plan, mit `monkeypatch`
auf `$CREDENTIALS_DIRECTORY` und dem bestehenden `fake_keyring`-Fixture — nie der echte
Keyring): `test_load_space_map_prefers_credentials_dir`,
`test_load_space_map_falls_back_when_credentials_dir_unset`,
`test_load_space_map_falls_back_when_credential_file_missing`,
`test_load_space_map_raises_on_malformed_credential`,
`test_export_writes_json_to_stdout_and_note_to_stderr`,
`test_export_contains_no_plaintext_token`.

**Verifiziert:** `.venv/bin/python -m pytest -q` → **153/153 grün** (147 + 6 neue). Alle
bestehenden `test_credentials.py`-Tests (die alte `load_space_map()`-Aufrufe machen) liefen
unverändert grün weiter — `$CREDENTIALS_DIRECTORY` ist in der Testumgebung nie gesetzt, der
Fallback greift transparent.

**Modul-Status oben nachgezogen** (Zeile 4: ⬜ → ✅, 6 Tests).

**Nächster Schritt (konkret):** Step 4 — systemd-Units (`sharefyx-mcp.service`,
`install_units.sh`). `test_unit_has_no_secret_shaped_value` ist die billigste Versicherung gegen
den Token-Klartext-Vorfall, der in P2 zweimal passiert ist.

## Session stopped — 2026-07-27 (Step 2: Request-Log)

**Ergebnis:** Step 2 abgeschlossen. `mcpserver/request_log.py` (neu) liefert beide Ereignisarten
aus Plan §3; `ToolCallLogMiddleware` läuft in `create_app()`, `AccessLogASGI` in `serve.py`.

**`[VERIFY]` V3 aufgelöst, gegen den echten `fastmcp==3.4.4`-Code, nicht nur die Doku geprüft:**
`Middleware.on_call_tool(context: MiddlewareContext[CallToolRequestParams], call_next)`,
`context.message.name` trägt den Tool-Namen, Registrierung über `mcp.add_middleware(...)` in
`app.py :: create_app()` — alles wie im Plan angenommen. **Eine Abweichung vom Plan-Wortlaut,
empirisch begründet:** `request_log.py`s Moduldocstring-Skizze nennt `ERROR_CLASSES:
dict[type[Exception], str]`. Das ist mit dem echten `FastMCP.call_tool()`-Pfad nicht umsetzbar —
gelesen bis in `server.py`: die Middleware-Kette ruft die Kernlogik über `call_next()` auf, und
jede dort erhobene `FastMCPError`/`ToolError` (`ToolError` erbt von `FastMCPError`) wird
unverändert weitergereicht. `tools.py :: map_storage_error()` hat die ursprüngliche
`storage`-Exception zu diesem Zeitpunkt bereits in eine `ToolError` mit Präfix-Text übersetzt
(`"conflict: …"`, `"item_not_found: …"`, …) — ein Typ-Dict würde hier immer denselben einen Typ
treffen. `classify_error()` parst deshalb den Nachrichtenpräfix vor dem ersten `":"` statt den
Exception-Typ zu prüfen. Volle Begründung im Moduldocstring von `request_log.py`.

**`space`-Feld — Semantik bewusst festgelegt, nicht nur implizit:** `_current_space()` liefert
den **authentifizierten Aufrufer** (`Principal.space`), nicht den Zielraum des Tool-Aufrufs. Bei
`get_item`/`update_item` gegen einen fremden Space steht im Log also weiterhin der eigene Space,
nicht der fremde. Das beantwortet Plan §3.4 Frage 2 ("mein Account oder der des Kollegen?")
korrekt; für einen Rule-4-Nachweis (wer hat wohin geschrieben) ist das Request-Log bewusst nicht
die Quelle — das leisten die Tool-Fehlerklasse (`write_denied`) und `test_tools.py`/`test_app.py`
(Advisor-Fund, sonst hätte ein kalter Leser beim Debuggen einer Cross-Space-Ablehnung den
Zielraum im Log vermutet).

**`err: "internal"` ist ein Sammelbecken, nicht nur der Whitelist-Fallback — festgehalten für
Step 7:** die Whitelist (`conflict`, `item_not_found`, `write_denied`, `invalid`) lässt
`auth_error`, `space_not_found` und FastMCPs generisches `"Error calling tool …"` alle in
`internal` fallen. Das ist Plan-konform, bedeutet aber: `err: "internal"` in `journald` kann
sowohl „ungültiger Token mitten im Aufruf" als auch „echter Store-Bug" heißen. Kein Blocker für
P3 (keine Abnahmezeile hängt an der Unterscheidung), aber falls Step 7 auf `internal`-Zeilen
stößt, ist das der erste Ort zum Nachschauen, nicht ein Bug im Logging.

**`TokenScrubbingFilter` erweitert** (`logging_setup.py`, im P3-N-Berührungsbereich): scrubbt
jetzt auch String-Werte innerhalb eines Dict-`record.msg` (vorher nur reine String-Messages) —
sonst wäre der Filter auf dem Request-Log-Pfad ein stiller No-op gewesen, praktisch redundant zu
`AccessLogASGI`s eigener Pfad-Redaktion, aber echte Verteidigung in der Tiefe statt einer
Behauptung. Eigener Test in `test_logging.py`
(`test_scrubbing_filter_redacts_token_in_dict_message`), da die P3-Tests den Filter nicht über
`configure_logging()` einbinden.

**Zirkelimport vermieden:** `request_log.py` importiert `_TOKEN_SEGMENT_RE` aus
`logging_setup.py` auf Modulebene; `logging_setup.py :: configure_logging()` importiert
`JsonLineFormatter`/`LOGGER_NAME` aus `request_log.py` **lazy** (innerhalb der Funktion) — zum
Aufrufzeitpunkt ist `logging_setup` bereits vollständig geladen, kein Zirkelbezug beim
Modul-Import.

**`mcp_smoke.py` bewusst nicht angefasst — P3-N-Grenzfall, an den Nikinger gemeldet:** Step 2s
„Done when" verlangt einen manuellen `mcp_smoke.py`-Lauf mit sichtbaren JSON-Zeilen. `mcp_smoke.py`
ruft aber `logging.basicConfig()` statt `configure_logging()` und geht nie durch `serve.py`
(reines In-Process-`ASGITransport`, kein `AccessLogASGI`) — selbst mit funktionierendem
Tool-Log wäre die Ausgabe ein Python-Dict-Repr, kein JSON. `mcp_smoke.py` steht nicht in P3-Ns
„genau anfassen"-Liste; sie ist als abschließende Aufzählung gelesen worden (wie schon bei
`tools.py`/`server.py`), deshalb keine Änderung dort. Stattdessen manuell gegen ein Wegwerf-Skript
(nie eingecheckt, aus dem Scratchpad gelöscht) verifiziert, das genau den echten Produktionspfad
fährt — `configure_logging()` + `create_app()` + `AccessLogASGI`, `FakeResolver` statt echtem
Keyring, temporäres `DATA_ROOT`: `GET /health` und ein Fremdzugriff mit falschem Token erzeugten
korrekt geformte, redigierte JSON-Zeilen auf stderr (`{"ts":"…","ev":"http","method":"GET",
"path":"/health","status":200,"ms":0}` bzw. mit `path":"/mcp/<redacted>","status":401`). Das ist
strengeres Beweismaterial als `mcp_smoke.py` liefern könnte, weil es den echten `serve.py`-Pfad
inklusive `AccessLogASGI` prüft, den `mcp_smoke.py` konstruktionsbedingt nie durchläuft. Für den
Nikinger: falls `mcp_smoke.py` künftig JSON-Request-Logs zeigen soll, ist das eine bewusste
P3-N-Erweiterung (ein Zweizeiler: `logging.basicConfig` → `configure_logging`), keine
Kleinigkeit, die einfach nachgezogen wird.

**Tests** (alle acht aus dem Plan, `phase2_mcp/tests/test_request_log.py`, plus einer in
`test_logging.py` für die Filter-Erweiterung): `test_json_line_is_valid_json`,
`test_tool_event_has_tool_space_and_duration`, `test_tool_event_error_carries_class_not_message`,
`test_tool_event_never_contains_item_title` (gestärkt gegen eine Tautologie-Falle — prüft jetzt
zuerst `len(tool_events) == 6`, bevor die Abwesenheit des Markers behauptet wird; Advisor-Fund:
sonst wäre der Test identisch grün gegen eine Middleware geblieben, die gar nichts loggt),
`test_http_event_redacts_token_segment`, `test_http_event_logs_401_status`,
`test_logging_failure_does_not_break_tool_call`, `test_request_logger_does_not_propagate_to_root`,
`test_scrubbing_filter_redacts_token_in_dict_message`.

**Verifiziert:** `.venv/bin/python -m pytest -q` → **147/147 grün** (138 + 9 neue).

**Modul-Status oben nachgezogen** (Zeile 3: ⬜ → ✅, 9 Tests). Rotation läuft nach diesem Commit.

**Nächster Schritt (konkret):** Step 3 — `credentials.py` LoadCredential-Pfad,
`export_space_map.py`. Alle Tests mit `monkeypatch` auf `$CREDENTIALS_DIRECTORY` und einem
Fake-Keyring, nie der echte Keyring.

## Session stopped — 2026-07-27 (Step 1: Gerüst und `SPACE_ALLOWED_HOSTS`)

**Ergebnis:** Step 1 abgeschlossen. `phase3_edge/` ist jetzt ein vollständiges (Nicht-Python-)
Verzeichnis mit Test-Anschluss; `SPACE_ALLOWED_HOSTS` existiert als Konfiguration statt
CLI-Zufall (P3-C).

**Dateien:**
- `phase3_edge/local.env.example` — Vorlage mit vier Platzhaltern (`REPO_ROOT`, `DATA_ROOT`,
  `VENV`, `ALLOWED_HOSTS`), ausschließlich Kommentare + Beispielpfade, kein echter Hostname,
  kein Token. `phase3_edge/local.env` selbst ist ab jetzt in `.gitignore` (Kommentar erklärt
  warum: Maschinenpfade, kein Geheimnis — der Hostname steht ohnehin in CT-Logs).
- `phase3_edge/tests/__init__.py` — leer, wie im Plan-Dateibaum vorgesehen (P1/P2 kommen ohne
  aus, P3 bekommt es laut Plan explizit, hier übernommen statt hinterfragt).
- `pytest.ini`: `testpaths` um `phase3_edge/tests` erweitert.
- `mcpserver/config.py`: `Settings.allowed_hosts: tuple[str, ...] = ()` neu, geparst über
  `_parse_allowed_hosts()` aus `SPACE_ALLOWED_HOSTS` (Komma-getrennt, `strip()`, leere Einträge
  verworfen, fehlende Variable → leeres Tupel — dieselbe Kein-Default-auf-echten-Wert-Logik wie
  bei `SPACE_DATA_ROOT`).
- `mcpserver/app.py`: `create_app()` berechnet `hosts = list(allowed_hosts) if allowed_hosts
  else (list(settings.allowed_hosts) or None)` — expliziter Parameter gewinnt, danach Settings,
  sonst FastMCPs eigener Default. Docstring ergänzt.
- `scripts/serve.py`: **unverändert**, wie geplant — `--allowed-host` bleibt `action="append"`,
  `default=None`; die neue Präzedenz lebt vollständig in `create_app()`.

**Tests** (`phase2_mcp/tests/test_config.py`, `test_app.py`, alle fünf aus dem Plan):
`test_allowed_hosts_defaults_to_empty`, `test_allowed_hosts_parses_comma_list`,
`test_allowed_hosts_strips_whitespace_and_drops_empties`,
`test_create_app_prefers_explicit_allowed_hosts_over_settings`,
`test_create_app_uses_settings_allowed_hosts`. Die beiden `app.py`-Tests patchen
`mcpserver.app.build_mcp` gegen eine `_CapturingFastMCP`-Stub-Klasse (`http_app()` zeichnet den
übergebenen `allowed_hosts`-Wert auf) statt den vollen FastMCP-Stack zu starten — Präzedenz ist
reine Verdrahtungslogik in `create_app()`, kein FastMCP-Verhalten (das deckt bereits
`test_asgi.py`/der Rest von `test_app.py` aus P2 ab).

**Verifiziert:**
- `.venv/bin/python -m pytest -q` → **138/138 grün** (133 Baseline + 5 neue).
- `bash scripts/dev_install.sh` (venv aktiviert) lief durch: nur `storage` und `mcpserver`
  editable installiert, `phase3_edge/` lautlos übersprungen (kein `pyproject.toml`) — Plan-Aussage
  in §1.2 damit real geprüft, nicht nur zitiert.

**Modul-Status oben nachgezogen** (Zeile 2: ⬜ → ✅, 5 Tests). Ab diesem Block gilt die
Rotationsregel: der Step-0-Block wandert über `scripts/rotate_session_block.sh phase3_edge`
nach `SESSIONS_ARCHIVE.md`.

**Nächster Schritt (konkret):** Step 2 — `mcpserver/request_log.py` (Tool- und HTTP-Log). Der
wichtigste Test dort ist `test_tool_event_never_contains_item_title` — er prüft eine Zusage,
keine Implementierung.

## Session stopped — 2026-07-27 (Step 0: Doku-Drift, Verifikation, Umgebungsinventar)

**Ergebnis:** Step 0 abgeschlossen. Kein Feature-Code — Haushalt vor dem ersten Baustein.

**A · Doku-Drift geschlossen** (Quelle: `PHASE2_CLOSEOUT_HANDOVER.md` §6 + Plan §0.4/§6):
- Root-`CLAUDE.md`: R5 „OAuth ist Phase 5" → **Phase 4** korrigiert (deckt sich mit der
  ROADMAP-Korrektur vom 2026-07-25, die bereits vorher galt, aber in R5 nicht nachgezogen war).
- Root-`CLAUDE.md`: R4 um die datierte Ergänzung zu Tailscale Funnel erweitert (§0.4 des Plans,
  wörtlich übernommen) — der ursprüngliche Cloudflare-Satz bleibt stehen, er beschreibt weiterhin
  korrekt, was dort gilt.
- Root-`CLAUDE.md`, „Current state": aktive Phase auf **P3** umgestellt, P2 in einen eigenen
  ✅-Absatz nach dem Muster von Phase 1 verschoben (inkl. Hinweis, dass der formale
  Abschluss-Handover jetzt existiert — der Satz „Formaler Phasenabschluss … steht noch aus" war
  mit `PHASE2_CLOSEOUT_HANDOVER.md` bereits überholt). `down:`-Karte von `phase2_mcp/CLAUDE.md`
  auf `phase3_edge/CLAUDE.md` umgehängt.
- `ROADMAP.md` und `phase2_mcp/CLAUDE.md`: `` `fastmcp` über Streamable HTTP `[VERIFY]` `` →
  Marker entfernt (live widerlegt, siehe P2-Abnahme).
- `ROADMAP.md`, Header-Card `down:`: `phase2_mcp_plan.md` und `phase3_edge_plan.md` ergänzt.
- `ROADMAP.md`, P3-Zeile: ⬜ → 🔄.
- `ROADMAP.md`, „Zurückgestellt aus P2": MCP-Revisions-Eintrag von Datum auf **Trigger**
  umgestellt (P3-E) — „erstes `fastmcp`-Release mit Support", nicht der 2026-07-28-Termin.
- `docs/INDEX.md`: neuer Abschnitt „Active phase (3)" mit drei Zeilen (Plan, Phase-Head, leeres
  Archiv); P2-Abschnitt nach „Completed phases" verschoben (🔄 → 📗); Zeile für
  `PHASE2_CLOSEOUT_HANDOVER.md` ergänzt; „Concept docs"-Fußnote von „P3–P5"/„P1- und P2-Pläne"
  auf „P4–P5"/„P1-, P2- und P3-Pläne" korrigiert.
- `ROADMAP.md`, P2-Abschnitt: der Satz „Fehlt noch: der formale Phasenabschluss (Browser-Webchat)"
  war mit `PHASE2_CLOSEOUT_HANDOVER.md` bereits überholt und stand — anders als in Root-`CLAUDE.md`
  — noch drin. Ersetzt durch „Handover an P3: `docs/concepts/PHASE2_CLOSEOUT_HANDOVER.md`",
  spiegelt jetzt den P1-Abschnitt, der denselben Satz für P1→P2 trägt.
- `phase2_mcp/CLAUDE.md`: `updated:`-Feld der Header-Card war bei diesem Commit stehen geblieben
  (`2026-07-26 (B2 behoben)`), obwohl der Scope-Absatz sich änderte — auf 2026-07-27 nachgezogen.

**Abweichung vom Plan, benannt:** `phase3_edge/CLAUDE.md` und `SESSIONS_ARCHIVE.md` (Plan-Step 1)
wurden bereits in Step 0 angelegt — minimal (L1-Card, Modul-Status, dieser Block), Scope/Runbooks
folgen wie geplant in Step 1. Grund: Hard Rule 8 verlangt den Phase-Head im selben Commit wie
jeden Step-Abschluss, und `docs/INDEX.md` braucht in diesem Commit bereits einen realen
Link-Empfänger statt eines toten Links.

**Sicherheits-Check vor dem Commit:** Die drei neuen, unversionierten Dateien
(`PHASE2_CLOSEOUT_HANDOVER.md`, `phase3_edge_plan.md`, `phase2_mcp_uebersicht.svg`) wurden vor
dem Staging mit `grep -aoE '[A-Za-z0-9_-]{32,}'` auf token-förmige Strings geprüft — Treffer
waren ausschließlich Testfunktionsnamen aus dem Plan. Das SVG (P2-Architekturdiagramm) enthält
nur den literalen Platzhalter `‹token›`, keinen echten Wert. Die SVG ist kein `.md` und damit
laut `docs/INDEX.md`-Scope („L0 map of every project .md") nicht indexpflichtig — bewusst nicht
aufgenommen, hier vermerkt statt stillschweigend übergangen.

**B · Verifikationsdurchlauf:**
- `git status` vor dem Commit: nur die drei erwarteten neuen Dateien untracked, sonst sauber.
- `docs/test-results/` existiert nicht (per `ls`, nicht per Doku-Aussage geprüft).
- Oversize-Check (`find … -size +40k`): zwei Treffer, `phase2_mcp_plan.md` und
  `phase3_edge_plan.md` — beide 📕, damit erlaubt.
- `pytest -q` über `.venv/bin/python -m pytest` (nicht System-Python): **133/133 grün**, deckt
  sich mit ROADMAP/Handover-Baseline.

**C · Umgebungsinventar** (alles `[VERIFY]`, read-only, kein Eingriff in echten `DATA_ROOT`/Keyring/Token):

| Prüfung | Ergebnis |
|---|---|
| Python | 3.12.3 |
| venv (für `ExecStart`, V6) | `/home/savefyx/dev/savefxy/.venv/bin/python` — Symlink-Kette über `python3` → System-`/usr/bin/python3.12`; der venv-Pfad selbst ist der korrekte `ExecStart`-Wert (aktiviert `pyvenv.cfg`/site-packages), nicht das Symlink-Ziel |
| `fastmcp` (V2) | **3.4.4 exakt installiert** — deckt sich bereits mit dem P3-D-Pin, keine Änderung nötig |
| Keyring-Backend (V5) | `keyring.backends.SecretService.Keyring` (priority 5), Chainer als Default-Frontend — deckt sich mit dem in P2 vom Nikinger bestätigten Roundtrip |
| systemd (V4) | Version 255 (≥250 ✓) |
| `systemd-creds` (V4) | vorhanden; `has-tpm2` → **„partial"**, kein volles TPM2-Sealing verfügbar (`+system`/`+subsystem`/`+libraries`, `-firmware`/`-driver`), Exit 3. `systemd-creds encrypt` fällt in diesem Fall auf Host-Key-Verschlüsselung zurück — für P3-F ausreichend (die Datei ist eine Hash-Map, kein umkehrbares Geheimnis; siehe Plan-Begründung) |
| Tailscale (V7) | **NICHT installiert** — `tailscale: command not found`. Echter Befund, kein „nichts zu tun": vor Step 7 (und vor jedem Live-Test von Step 4/6 gegen einen echten Funnel) muss der Nikinger Tailscale installieren, dem Tailnet beitreten, MagicDNS + HTTPS-Zertifikate aktivieren und `nodeAttrs: funnel` im Policy-File setzen. Blockiert **nicht** Steps 1–6 (reiner Code/Test-Weg), blockiert **Step 7**. |
| Dateisystem `DATA_ROOT` | `ext4` bestätigt — P1-Bedingung für `flock` weiterhin erfüllt |
| `cloudflared` | vorhanden unter `/usr/local/bin/cloudflared`, **kein** systemd-Service registriert (nur die P2-Quick-Tunnel-Nutzung von Hand) — Rückbau bleibt wie geplant Aufgabe von Step 6 |
| Git-Identität in `DATA_ROOT` | vorhanden (`Space Server` / `space-server@localhost`) — relevant für den in Plan §4 Step 4 benannten `ProtectSystem=strict`/Git-Commit-Fallstrick, dort real zu prüfen |

**Verifiziert:** `pytest -q` (via `.venv/bin/python -m pytest`) → 133/133 grün. `git status` vor
Commit sauber bis auf die drei erwarteten neuen Dateien. Secret-Scan der drei Dateien negativ.

**Nächster Schritt (konkret):** Step 1 — `phase3_edge/`-Gerüst vervollständigen
(`local.env.example`, `tests/__init__.py`, `.gitignore`-Ergänzung, `pytest.ini`-Erweiterung) und
Konfiguration (`SPACE_ALLOWED_HOSTS` in `config.py`/`app.py`, fünf Tests laut Plan). **Vor
Step 7** braucht es zusätzlich eine Nikinger-Aktion außerhalb des Plans selbst: Tailscale auf
dieser VM installieren und die Tailnet-Voraussetzungen (V7) einrichten — sonst lässt sich der
Runbook-Teil aus Step 7 nicht gegenprüfen.

