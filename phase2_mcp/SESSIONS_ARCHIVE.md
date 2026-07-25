---
status: live
purpose: Archiv älterer Session-stopped-Blöcke aus phase2_mcp/CLAUDE.md, newest-first, verbatim
read-when: Audit vergangener Sessions dieser Phase; NICHT für normalen Session-Start
detail: L3
up: CLAUDE.md
updated: 2026-07-25
---
# Session-Archiv — Phase 2 MCP-Server

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

