---
status: live
purpose: Archiv älterer Session-stopped-Blöcke aus phase2_mcp/CLAUDE.md, newest-first, verbatim
read-when: Audit vergangener Sessions dieser Phase; NICHT für normalen Session-Start
detail: L3
up: CLAUDE.md
updated: 2026-07-25
---
# Session-Archiv — Phase 2 MCP-Server

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

