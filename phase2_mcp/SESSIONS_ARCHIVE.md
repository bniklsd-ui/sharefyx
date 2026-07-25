---
status: live
purpose: Archiv älterer Session-stopped-Blöcke aus phase2_mcp/CLAUDE.md, newest-first, verbatim
read-when: Audit vergangener Sessions dieser Phase; NICHT für normalen Session-Start
detail: L3
up: CLAUDE.md
updated: 2026-07-26
---
# Session-Archiv — Phase 2 MCP-Server

## Session stopped — 2026-07-25 (Step 4: Auth, Rechte, Request-Kontext)

**Ergebnis:** `auth.py` (`Principal` frozen dataclass mit gekürztem `__repr__`,
`AuthError`, `SpaceResolver`-Protokoll, `KeyringTokenResolver` mit injiziertem `load_map`,
Dict-Lookup über `sha256(credential)`), `permissions.py` (`Permissions`-Protokoll,
`OwnSpaceWritable`), `logging_setup.py` (`configure_logging()`, `TokenScrubbingFilter` —
ersetzt `/mcp/<segment>` durch `/mcp/<redacted>` in Message **und** Args), `context.py` +
`asgi.py` (`TokenPathASGI`, Details siehe **wichtiger Fund** unten).

**V3 aufgelöst:** `fastmcp.server.dependencies.get_http_request` importiert sauber gegen das
echte `fastmcp==3.4.4` — der im Plan dokumentierte Importpfad stimmt, `fastmcp.dependencies.
CurrentRequest()` ist eine andere (Dependency-Injection-)API für denselben Zweck, nicht die
hier gebrauchte direkte Funktion.

**Wichtiger Fund (empirisch, nicht nur gelesen) — §2.4 ist an einer Stelle nicht umsetzbar wie
geschrieben:** Der Plan beschreibt `assert_principal_matches_request()` als „zieht das
Token-Segment aus dessen Pfad". Das geht nicht: `TokenPathASGI` muss das Token-Segment aus dem
Pfad entfernen, **bevor** es an die innere FastMCP-App delegiert (sonst sieht FastMCPs eigenes
Routing das Segment als Teil des MCP-Pfads und die Anfrage schlägt fehl). Ein Tool, das während
seiner Ausführung `get_http_request().url.path` liest, sieht deshalb nur noch den bereinigten
Pfad.

Zwei ASGI-Mounting-Techniken gegen ein echtes `fastmcp==3.4.4` + `starlette`-Setup
(`httpx.ASGITransport`/`starlette.testclient.TestClient`) durchprobiert:
1. **`root_path`-Akkumulation** (Starlettes eigene Technik, `scope["path"]` bleibt unverändert,
   nur `root_path` wächst) — scheitert an `redirect_slashes`: ein Credential-Segment ohne
   nachfolgenden Pfad lässt `route_path` leer statt `"/"` werden, Starlette antwortet mit 307
   auf eine URL mit angehängtem `/`, bevor die innere App je läuft.
2. **Direkte `path`/`raw_path`-Kürzung** (Plan-Wortlaut) — funktioniert für das Routing
   (kein Redirect, Tool wird aufgerufen), aber `get_http_request().url.path` liefert dann
   nachweislich `"/mcp/"`, nicht das Token — bestätigt das Problem oben empirisch, nicht nur
   theoretisch.

**Lösung:** `TokenPathASGI` hinterlegt `token_hash` in `scope["state"]`, **bevor** es den Pfad
kürzt (Technik 2 bleibt fürs Routing). `scope["state"]` überlebt die Weiterleitung unverändert —
Starlettes offizieller Mechanismus, um Zustand über eine ASGI-Kette hinweg mitzugeben, per
Testprobe bestätigt: `request.state.token_hash` kam im Tool korrekt an. Die
Sicherheitseigenschaft ist identisch zur Plan-Absicht: der Guard vergleicht „was hat unsere
eigene ASGI-Schicht für DIESEN Request aufgelöst" (`scope["state"]["token_hash"]`, gesetzt von
`TokenPathASGI`) gegen „was liefert `get_http_request()` gerade zurück" (`current_principal()`
aus dem ContextVar) und schlägt bei jeder Abweichung laut fehl (`AuthError`) — nicht mehr über
den Pfad, aber mit derselben Garantie. Vollständige Begründung im Docstring von `context.py`.
**Kein Test dafür in Step 4** (braucht einen echten laufenden Request-Kontext) — end-to-end
geprüft in Step 5 über `test_app.py::test_principal_isolation_under_concurrency`.

**Verifiziert (live):** 14 neue Tests (`test_auth.py` ×4, `test_permissions.py` ×3,
`test_logging.py` ×1, `test_context.py` ×2 — nicht im Plan gefordert, aber `current_principal`/
`set_principal`/`reset_principal` sind eigenständige, netzunabhängige Logik —,
`test_asgi.py` ×4 gegen einen Fake-Resolver + Fake-Innen-App, keine echte FastMCP-App nötig für
diese Schicht). `pytest -v` → **99/99 grün** (76 P1 + 23 P2). `test_principal_reset_after_request`
bestätigt: nach dem Request wirft `current_principal()` wieder `AuthError` — kein Leck zwischen
Requests.

**Anmerkung des Advisors, hier festgehalten statt in Step 6 neu zu entdecken:** P2-N sagt
„`AuthError` → HTTP 401, nie ein Tool-Fehler". Der Guard läuft aber *innerhalb* eines
Tool-Aufrufs (§3.3 Schritt 2) — das 401-Fenster ist zu diesem Zeitpunkt vorbei, ein
Guard-`AuthError` muss also zwangsläufig als Tool-Fehler auftauchen. Das ist kein Defekt (immer
noch fail-closed, keine fremden Daten), aber `map_storage_error()` in Step 6 muss diese
Abbildung bewusst treffen, nicht zufällig.

**Nächster Schritt (konkret):** Step 5 — `server.py`, `app.py`, `scripts/serve.py`. Das ist die
Stelle, an der `TokenPathASGI` erstmals gegen eine echte FastMCP-App läuft — V4 (`Mount`-
Verhalten) und der `assert_principal_matches_request()`-Guard werden dort erstmals end-to-end
statt isoliert geprüft.

---

## Session stopped — 2026-07-25 (Step 3: Credentials + Token-Ausgabe)

**Ergebnis:** `mcpserver/credentials.py` (`KEYRING_SERVICE = "nikinger-space"`,
`KEYRING_KEY_SPACES = "spaces"`, `generate_token()` → `secrets.token_urlsafe(32)`,
`hash_token()` → sha256-Hex, `load_space_map()`/`save_space_map()`, `issue(space) -> str`,
`revoke(space) -> int`). `keyring` wird ausschließlich in diesem Modul importiert. Im Keyring
liegt nur `{sha256(token): space}` — kein umkehrbares Geheimnis. `phase2_mcp/scripts/
issue_token.py` (`--space`/`--revoke`/`--list`, mutually exclusive): das Token ist das
**einzige** stdout dieses Skripts, und nur beim Ausgeben; alles andere (Warnhinweis, Revoke-
Bestätigung, die Listing-Zeilen) geht auf stderr (Hard Rule 7 — hier besonders eng ausgelegt,
weil das Skript mit dem Geheimnis selbst hantiert).

**Verifiziert (live):** sechs neue Tests in `phase2_mcp/tests/test_credentials.py`
(`test_hash_token_is_stable_hex64`, `test_generate_token_length_and_uniqueness`,
`test_load_space_map_missing_key_returns_empty`, `test_save_load_roundtrip_with_fake_backend`,
`test_issue_stores_only_hash`, `test_revoke_removes_all_hashes_of_space`) — alle gegen einen per
`monkeypatch` gefakten `keyring.get_password`/`set_password` (In-Memory-Dict), fassen den
echten Keyring nie an. `test_issue_stores_only_hash` prüft explizit, dass weder das Klartext-
Token noch irgendein Wert der Map dem Token entspricht — nur der Hash. `pytest -v` →
**85/85 grün** (76 P1 + 9 P2, davon 3 `test_config.py` + 6 `test_credentials.py`).

**V5 — Status nach diesem Schritt:** `keyring --list-backends` zeigt weiterhin
`SecretService.Keyring` (Priorität 5) als real installiertes Backend (aus Step 1). Ein echter
Schreib-/Lese-Roundtrip **gegen dieses Backend** (nicht den Test-Fake) wurde von mir bewusst
**nicht** ausgeführt — das würde in den echten, produktiven Keyring-Eintrag unter Service
`nikinger-space` schreiben, denselben, den P3 später für den echten Connector benutzt. Das ist
strukturell derselbe Fall wie „nie gegen den echten `DATA_ROOT` testen": ein echtes Secret in
einem echten System-Backend ist kein Objekt für einen Probe-Write durch Claude Code. **Modul-
Status Zeile 4 bleibt deshalb 🟡, nicht ✅**, bis der Nikinger einmal real
`python phase2_mcp/scripts/issue_token.py --space nikinger` laufen lässt und das Ergebnis
bestätigt (Token erscheint auf stdout, `--list` zeigt danach den Space mit gekürztem Hash).

**Nachtrag (Nikinger-Bestätigung + Incident, 2026-07-25):** Der Nikinger hat den echten Roundtrip
gefahren. **V5 damit vollständig bestätigt** — `issue_token.py --space nikinger` lief gegen das
echte `SecretService`-Backend, Token erschien einmalig auf stdout, `--list` zeigte danach
`nikinger: <hash-prefix>…` auf stderr. Modul-Status Zeile 4 auf ✅ gehoben.

**Incident, kein stiller Vorbeigang:** Der erste Testlauf wurde vom Nikinger komplett samt
Klartext-Token in den Chat eingefügt — nicht nur der Hash, das Bearer-Token selbst landete damit
in einer Konversation außerhalb des Keyrings, strukturell gleichwertig zu „Token in einem
Commit" (Hard Rule 1: Incident, kein Schönheitsfehler). Sofort erkannt und gemeldet, statt
stillschweigend weiterzumachen. **Behoben durch Rotation:** der Nikinger hat
`--revoke nikinger` (1 Token entfernt) gefolgt von einem neuen `--space nikinger` ausgeführt und
das neue Token diesmal **nicht** in den Chat eingefügt, sondern lokal in
`../nikinger only/bearer_token.md` (außerhalb dieses Code-Repos, nicht Teil von `DATA_ROOT`
oder eines Git-Trackings hier) abgelegt. `--list` bestätigt genau einen aktuellen Eintrag für
`nikinger`. Für künftige Sessions: **Klartext-Tokens gehören nie in den Chat-Verlauf**, auch
nicht „nur zum Testen" — dieselbe Regel wie für Commits.

**Doku-Pflichten aus Plan §2.3, im selben Commit:** `README.md` — neuer Abschnitt „Token
ausgeben, rotieren, widerrufen" (die drei Kommandos, „genau einmal angezeigt", Vorgehen bei
Verlust). Root-`CLAUDE.md` Hard Rule 1 — datierte Korrekturnotiz (`storage/credentials.py`
wurde nie gebaut, realer Pfad ist `phase2_mcp/mcpserver/credentials.py`; die Regel selbst
unverändert). Dieser Head — die beiden vorgezogenen Absätze „Warum nur Hashes im Keyring" und
„Was der Pfad-Token nicht ist" von „vorgezogen, Step 3 liefert Code" auf den realen Codestand
aktualisiert.

**Nächster Schritt (konkret):** Step 4 — `auth.py`, `permissions.py`, `context.py`, `asgi.py`,
`logging_setup.py`. Kein Keyring-Zugriff dort direkt (nur über injizierte `load_map`), also kein
weiterer V5-Haltepunkt nötig — der steht weiterhin offen, bis der Nikinger den echten Roundtrip
bestätigt.

## Session stopped — 2026-07-25 (Step 2: P1-Contract-Erweiterungen)

**Ergebnis:** Die drei vom Nikinger freigegebenen, einmaligen Erweiterungen (Plan §0.4 Punkt L,
§4 Step 2) in `phase1_storage/storage/` eingebracht:
- `models.py`: `STATUS_VALUES` (Statusvokabular je `type`) + `valid_statuses()`.
- `store.py`: neuer Helper `_check_type_and_status()`, aufgerufen aus `create()` und `update()`
  — wirft `ValidationError` bei unbekanntem `type` oder unerlaubtem `status` (D2).
- `store.py :: space_of(item_id)` — reiner Index-Lookup, kein Datei-Read, `ItemNotFound` bei
  unbekannter ID.
- `store.py :: get(item_id, *, repair_drift=True)` + `_reconcile_and_get_row(...,
  repair_drift=True)` — bei `repair_drift=False` und erkannter Drift wird nur der Index
  nachgezogen, kein Frontmatter-Rewrite, kein Git-Commit (D3). Default `True` lässt jedes
  bestehende P1-Verhalten unverändert.

**Details, Code-Anker und die vollständige Begründung stehen in `phase1_storage/CLAUDE.md`**
unter „Geerbte Contracts" (Code-nah, nicht hier dupliziert — Vorgabe aus diesem Head selbst,
„Was hier bewusst NICHT steht").

**Verifiziert (live):** acht neue Tests in `phase1_storage/tests/test_store.py`
(`test_space_of_returns_space`, `test_space_of_unknown_raises_item_not_found`,
`test_get_repair_drift_false_leaves_file_untouched`, `test_get_repair_drift_false_creates_no_commit`,
`test_get_repair_drift_true_still_bumps`, `test_create_rejects_unknown_status`,
`test_update_rejects_unknown_status`, `test_update_accepts_valid_status_per_type`). Gesamtsuite
`pytest -v` → **79/79 grün** (76 in `phase1_storage/tests/` inkl. dieser acht, 3 in
`phase2_mcp/tests/`). Keine bestehende P1-Test musste angepasst werden — die einzigen
Store-Aufrufe mit explizitem `status=` in `test_store.py` (`status="open"` auf einem `task`,
`status="done"` auf einem `task`) waren bereits typkonform.

**Nächster Schritt (konkret):** Step 3 — `credentials.py` + `scripts/issue_token.py`. Braucht
eine Nikinger-Rückmeldung, sobald der finale Funktionstest (`keyring`-Wert schreiben und
zurücklesen) gelaufen ist — V5 ist bis dahin „vielversprechend", nicht „bestätigt".

## Session stopped — 2026-07-25 (Step 1: Paketgerüst)

**Ergebnis:** `phase2_mcp/pyproject.toml` (Paket `mcpserver`, spiegelt
`phase1_storage/pyproject.toml` exakt bis auf Name/Description/Dependencies —
`dependencies = ["storage", "fastmcp>=3.4,<3.5", "keyring>=25"]`,
`dev = ["pytest", "pytest-asyncio", "httpx"]`), `mcpserver/__init__.py`
(`__version__ = "0.1.0"`), `mcpserver/config.py` (`Settings`-Dataclass `frozen, kw_only`:
`data_root: Path` Pflicht ohne Default, `host="127.0.0.1"`, `port=8765`, `log_level="INFO"`;
`load_settings(env)` liest `SPACE_DATA_ROOT`/`SPACE_HOST`/`SPACE_PORT`/`SPACE_LOG_LEVEL`, wirft
`ValueError` bei fehlendem `SPACE_DATA_ROOT` oder nicht-parsbarem `SPACE_PORT`). Kein Secret in
`Settings` — `config.py` kennt laut Modulübersicht „nichts", importiert entsprechend nur
Standardbibliothek.

**Drift gegenüber dem Plan, dated:** Plan §4 Step 1 nennt `tests/__init__.py` als Datei. P1 hat
in `phase1_storage/tests/` nie ein `__init__.py`, sondern ein leeres `conftest.py` als
Platzhalter (Step 0 des P1-Plans). Hier aus Konsistenzgründen mit dem bereits etablierten
Repo-Vorbild identisch gehalten: `phase2_mcp/tests/conftest.py` (leer) statt `__init__.py`.
Funktional gleichwertig für `pytest`-Discovery.

**Notwendige Ergänzung, die der Plan nicht auflistete:** `pytest.ini` (`testpaths =
phase1_storage/tests`) hätte `phase2_mcp/tests/` nie gefunden. Erweitert auf
`testpaths = phase1_storage/tests phase2_mcp/tests` — sonst wären alle P2-Tests ab hier
unsichtbar für `pytest` gewesen, ohne dass ein Fehler das angezeigt hätte.

**Verifiziert (live):** `./scripts/dev_install.sh` fand `phase2_mcp/` automatisch über den
`phase*_*/`-Glob (keine Änderung am Skript nötig, wie im Plan erwartet), installierte `storage`
und `mcpserver` editable, zog `fastmcp==3.4.4` (exakt die in Step 0 als aktuellste 3.4.x-Version
verifizierte) und `keyring==25.7.0` echt aus PyPI. `from mcpserver import __version__` →
`"0.1.0"`. `pytest -v` → **71/71 grün** (68 aus P1 + 3 neue in `test_config.py`:
`test_load_settings_requires_data_root`, `test_load_settings_defaults`,
`test_load_settings_port_invalid_raises`).

**V5 (Keyring-Backend) weiter aufgelöst, noch nicht endgültig:** `keyring --list-backends` nach
echter Installation zeigt `keyring.backends.SecretService.Keyring` mit Priorität 5 (höchste) —
das in Step 0 vermutete Backend ist real verfügbar, nicht nur plausibel. Endgültig verifiziert
ist V5 erst, wenn Step 3 tatsächlich einen Wert schreibt und zurückliest (`credentials.py`
existiert noch nicht).

**Nächster Schritt (konkret):** Step 2 — die drei freigegebenen P1-Contract-Erweiterungen
(`space_of()`, `get(..., repair_drift=)`, Statusvalidierung) in `phase1_storage/storage/`.
Kein weiterer Haltepunkt vorgesehen (Plan §4 Step 2 ist mechanisch, Erweiterungen sind bereits
freigegeben).

## Session stopped — 2026-07-25 (Step 0: Haushalt + Verifikationsdurchlauf)

**Ergebnis:** Erster Claude-Code-Durchlauf für Phase 2. Kein Feature-Code — Step 0 ist reiner
Haushalt, wie im Plan (`docs/concepts/phase2_mcp_plan.md` §4 Step 0) vorgegeben.

**Drift gegenüber dem Plan, hier festgehalten statt beim Commit improvisiert:** Der Plan
listet `phase2_mcp/CLAUDE.md` erst unter Step 1 („Paketgerüst"). Hard Rule 8 verlangt aber,
dass **jeder** Step-Commit die Modul-Tabelle und den Session-Block **eines Phase-Heads**
aktualisiert — und Root-`CLAUDE.md`s `down:`-Link auf die aktive Phase brauchte ohnehin ein
reales Ziel. Deshalb dieser Head + `SESSIONS_ARCHIVE.md` bereits in Step 0 angelegt, mit
Rotationsregel und Skriptverweis von Anfang an (nicht wie in P1 erst nachträglich eingeführt).
Step 1 füllt das Paketgerüst (`pyproject.toml`, `mcpserver/__init__.py`, `mcpserver/config.py`)
und aktualisiert diesen Head weiter.

**A · Rotationsregel operationalisiert (Herkunft: `PHASE1_CLOSEOUT_HANDOVER.md` A1–A3):**
1. `phase1_storage/CLAUDE.md`: die verbliebene Überschrift `## Phase 1 ist live-verifiziert (…)`
   auf das Schema gebracht → `## Session stopped — 2026-07-25 (Phase 1 live-verifiziert, Phase
   abgeschlossen)`.
2. `scripts/rotate_session_block.sh` (lag bereits fertig geschrieben und ungetrackt im Repo,
   nicht von dieser Session verfasst) eingecheckt, `chmod +x`, für `phase1_storage` gelaufen:
   Head 35.053 B → 9.479 B, Archiv 2.308 B → 27.882 B, ein Block (346 Zeilen) verlustfrei
   verschoben, Reassemblierung + Byte-Rückvergleich bestanden. `.bak`-Dateien nach Sichtprüfung
   gelöscht. Manuelle Nacharbeiten erledigt: `SESSIONS_ARCHIVE.md`-Frontmatter `updated:` auf
   2026-07-25, `docs/INDEX.md`-Größenangaben nachgezogen, Nahtstellen sauber (eine Leerzeile,
   keine doppelte).
3. Verweise gesetzt: Root-`CLAUDE.md` („Doku-Hygiene"), `phase1_storage/CLAUDE.md` („Harte
   Regeln", `sed -n 'A,Bp'`-Wortlaut ersetzt), `docs/PROMPTS.md` (Prompt 1 + Prompt 3 Punkt 4)
   nennen jetzt den Skriptaufruf. `docs/DOC_LAYERS_CONVENTION.md` unangetastet (byte-identische
   Kopie). Keine Indexzeile für die `.sh`.

**B · Verifikationsdurchlauf:**
- `up:`/`down:`-Ziele: alle auflösbar nach dieser Session (Root-`CLAUDE.md` zeigte auf
  `phase1_storage/CLAUDE.md`, jetzt auf diesen Head umgehängt).
- Fehlende Indexzeilen gefunden und ergänzt: `docs/concepts/PHASE1_CLOSEOUT_HANDOVER.md`,
  `docs/concepts/phase2_mcp_plan.md`, dieser Head, `SESSIONS_ARCHIVE.md` — alle jetzt in
  `docs/INDEX.md` unter „Active phase (2)" bzw. „Completed phases".
- `find . -name "*.md" -size +40k`: einziger Treffer `docs/concepts/phase2_mcp_plan.md`
  (46.833 B) — ist 📕, also regelkonform trotz Überschreitung des Softcaps.
- `files.rename_for_new_slug()` war toter Produktivcode (`store.py` nutzt `files.move_file()`
  direkt, bestätigt per `grep`) — entfernt, samt der zwei Tests in `test_files.py`. P1-Tests
  70 → 68, `pytest` grün. Doku-Drift im (jetzt archivierten) Step-2-Session-Block mit datierter
  Korrektur versehen, **bevor** die Rotation lief.
- Branchname `master` (`DATA_ROOT`) vs. `main` (Code-Repo): bestätigt kosmetisch, kein Remote
  betroffen, jetzt in `README.md` als bewusst eingefroren dokumentiert.
- Drei Schreibweisen (`sharefyx`/`/home/savefyx/…`/`/home/savefyx/dev/savefxy`): in `README.md`
  als bewusst eingefroren dokumentiert (Nikinger-Entscheidung 2026-07-25) — eine Umbenennung
  würde Pfade brechen, die P3 in systemd-Units schreibt.

**C · Festlegungen eingetragen:** `ROADMAP.md` — OAuth (bisher P5) rückt direkt hinter P3 auf
P4, Web-UI (bisher P4) rückt auf P5 dahinter; neuer Abschnitt „Zurückgestellt aus P2" mit drei
Einträgen (D6, MCP-Revision 2026-07-28, Lese-Rechte zwischen Spaces); P2-Zeile auf 🔄. Root-
`CLAUDE.md` „Current state": aktive Phase jetzt P2, `down:` auf `phase2_mcp/CLAUDE.md`
umgehängt, P1 zu einem knappen abgeschlossenen Absatz verdichtet.

**`[VERIFY]`-Register, Ergebnisse dieser Session (siehe Plan §8):**
- **V1** (Repo-Stand nach P1-Abschluss) — aufgelöst, siehe A/B oben.
- **V2** (`fastmcp`-Version) — aufgelöst: `pip index versions fastmcp` zeigt `3.4.4` als
  aktuellste 3.4.x-Version, exakt im gepinnten Fenster `>=3.4,<3.5`. Kein Drift.
- **V3** (Importpfad `get_http_request`) — **offen**, `fastmcp` ist noch nicht installiert
  (kommt erst Step 1). Bei Ausführung von §2.4 gegen die echte installierte Version prüfen.
- **V4** (`Mount("/mcp")`-Verhalten) — **offen**, hängt an Step 5 (`app.py` existiert noch nicht).
- **V5** (Keyring-Backend auf der VM) — **vielversprechend, aber nicht final**: `dbus-daemon`
  und `gnome-keyring-daemon` sind installiert, `DBUS_SESSION_BUS_ADDRESS` ist gesetzt — das
  SecretService-Backend sollte funktionieren. Python-Paket `keyring` ist noch nicht installiert
  (kommt Step 3); `keyring --list-backends` dort final prüfen und dem Nikinger melden statt
  selbst eine Datei-Fallback-Lösung zu wählen.
- **V6** (Python-Version) — aufgelöst: `Python 3.12.3` auf der VM, `.venv` nutzt dieselbe
  Version. Erfüllt ≥3.10 komfortabel.
- **V7** (Custom Connectors auf Pro) — **offen**, gehört zu Step 7 (Runbook).
- **V8** (Größenbudget gegen echte Beispieldaten) — **offen**, gehört zu Step 6.
- **V9** (Namensinkonsistenzen im echten `DATA_ROOT`) — aufgelöst per read-only `ls`:
  `/home/savefyx/savefyx-data/` enthält genau einen Space-Ordner (`nikinger`), kein
  Umbenennungsbedarf.

**Baseline vor jeder P2-Änderung (live geprüft):** `pytest` in `phase1_storage/` lief 70/70
grün vor der Entfernung von `rename_for_new_slug()`, danach 68/68 grün — Regression
ausgeschlossen, nicht nur behauptet.

**Für Step 1 vorgemerkt:** Paketgerüst `phase2_mcp/pyproject.toml` (Paket `mcpserver`,
Abhängigkeit auf `storage` + `fastmcp>=3.4,<3.5` + `keyring>=25`), `mcpserver/__init__.py`,
`mcpserver/config.py` mit `Settings`/`load_settings()`. `scripts/dev_install.sh` findet das
Verzeichnis automatisch (Glob über `phase*_*/`) — keine Änderung dort nötig.

**Nächster Schritt (konkret):** Step 1 (Paketgerüst) — kein weiterer Haltepunkt vor Step 2
(P1-Contract-Erweiterungen) vorgesehen, da beide klein und mechanisch sind; Step 3 (Credentials)
braucht wieder eine Nikinger-Rückmeldung wegen V5.

