---
status: live
purpose: Phase-Head MCP-Server — Scope, harte Regeln, gelockte Entscheidungen, Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase2_mcp/ — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase2_mcp_plan.md          # voller Plan, Entscheidungen P2-A–P2-N, Steps 0–7
  - ../docs/concepts/PHASE1_CLOSEOUT_HANDOVER.md # Herkunft der Entscheidungen D1–D6
  - SESSIONS_ARCHIVE.md                          # ältere Session-Blöcke (noch leer)
updated: 2026-07-25
---
# CLAUDE.md — Phase 2: MCP-Server (`phase2_mcp/`)

> **Claude kann lesen und schreiben — lokal, ohne Tunnel.** Ein dünner Adapter über dem in P1
> bewiesenen Storage-Kern: Transport (Streamable HTTP), Identität (Token → Space), Autorisierung
> (eigener Space schreibbar, fremde read-only).
> **Quelle der Wahrheit ist der Code, nicht dieses Dokument.**
> Vollständiges Design + alle 14 gelockten Entscheidungen (P2-A–P2-N) + Steps 0–7:
> `../docs/concepts/phase2_mcp_plan.md`.

## Mission (zuerst lesen)

Der eigentliche Härtetest der Phase ist nicht MCP, sondern **Rule 4**: ein Codepfad, über den
ein fremder Space beschrieben werden kann, existiert nach dieser Phase nicht — auch nicht
versehentlich, auch nicht über `get()`. Zwei gleichzeitige Requests mit zwei verschiedenen
Tokens müssen zwei verschiedene Spaces sehen; wenn dieser Test fällt, ist es ein
Cross-Space-Leak, kein Testproblem.

## Bauprinzip (Projekt-Kernprinzip)

„Der Server ist dumm." **Phase 2 enthält KEINE AI.** Die Tools reichen Store-Ergebnisse durch,
formatieren sie token-sparsam und entscheiden über Rechte. Mehr nicht. Wer hier ein LLM
einbauen will → **stop**.

## Scope

- **DRIN:** `fastmcp` über Streamable HTTP `[VERIFY]`, Token→Space-Auflösung, sechs Tools
  (`list_spaces`, `search_items`, `get_item`, `create_item`, `update_item`, `append_to_item`),
  `<untrusted_content>`-Wrapping fremder Bodies + Snippets, Token-Budget-Disziplin im Listing,
  `/health`.
- **DRAUSSEN:** Löschen (`status: archived` reicht), MCP Resources, MCP Prompts, OAuth,
  öffentliche Erreichbarkeit/Tunnel (P3), SQL-Filterung in `Store.search()` (D6, zurückgestellt).

## Harte Regeln (nicht verhandelbar)

- Alle Hard Rules aus Root-`CLAUDE.md` gelten unverändert — insbesondere: kein Secret in einer
  Datei (Tokens nur als sha256-Hash im Keyring, Service `nikinger-space`), kein Last-Write-Wins,
  kein offener Port am Router, Logging → stderr, stdout nur maschinenlesbares JSON.
- **Rule 4 ist architektonisch, nicht per `if`.** `create_item`/`update_item`/`append_to_item`
  haben keinen `space`-Parameter; der Ziel-Space ist immer der des Principals (P2-G).
- **Auth fail-closed.** Kein/unbekanntes Token → HTTP 401 ohne Detail, nie ein Tool-Fehler, nie
  unterscheidbar von „falsches Token" (P2-N).
- **`stateless_http=True` ab Tag 1** — Sicherheitsbedingung, keine Skalierungsoption (P2-B, §8
  Risiko 1).
- **Token nie im Log.** Uvicorn-Access-Log aus, Scrubbing-Filter auf jedem verbleibenden Logger.
- **Rotationsregel ab Tag 1.** Dieser Head trägt **genau einen** Session-Block. Beim Anlegen
  eines neuen wandert der bisherige **verbatim** nach `SESSIONS_ARCHIVE.md`, newest-first —
  Durchführung über `scripts/rotate_session_block.sh phase2_mcp`, nie von Hand.
- **Commit ⇒ Note-Update, im selben Commit** (Hard Rule 8): Modul-Tabelle unten + Session-Block.

## Die 14 Entscheidungen (P2-A – P2-N) — Kurzform (Details: Plan §0.4)

Bibliothek `fastmcp>=3.4,<3.5` (A) · Protokoll 2025-11-25, `stateless_http=True` (B) · Starlette-
Wurzel mit `Mount("/mcp")` (C) · Token im Pfad, Auflösung einmal pro Request (D) · Keyring
speichert nur Hashes (E) · `SpaceResolver`/`Permissions` getrennte Seams, beliebig viele Spaces
(F) · Schreib-Tools ohne `space`-Parameter (G) · `<untrusted_content>` mit Escaping (H) ·
kompaktes JSON / Dateitext als Ergebnisformate (I) · Token-Budget `limit=20`/`max=100` (J) ·
Archivieren nur über `update_item(status="archived")`, kein siebtes Tool (K) · drei einmalige
P1-Contract-Erweiterungen (L, Step 2) · OAuth bleibt hinter P3, Seam wird gebaut (M) ·
Fehlerabbildung mit handlungsfähigem Text (N).

## Modul-Status

| # | Modul | Step | Status | Tests |
|---|---|---|---|---|
| 1 | Haushalt, Verifikationsdurchlauf, Rotationsregel operationalisiert | 0 | ✅ | 0 (kein Feature-Code) |
| 2 | Paketgerüst `phase2_mcp/`, `mcpserver/config.py` | 1 | ⬜ | — |
| 3 | P1-Contract-Erweiterungen (`space_of`, `repair_drift`, Statusvalidierung) | 2 | ⬜ | — |
| 4 | `credentials.py`, `scripts/issue_token.py` | 3 | ⬜ | — |
| 5 | `auth.py`, `permissions.py`, `context.py`, `asgi.py`, `logging_setup.py` | 4 | ⬜ | — |
| 6 | `server.py`, `app.py`, `scripts/serve.py` | 5 | ⬜ | — |
| 7 | `tools.py` (die sechs Tools) | 6 | ⬜ | — |
| 8 | `scripts/mcp_smoke.py`, Runbook, Größenmessung | 7 | ⬜ | — |

**Gesamt: 0 Tests bisher** (Step 0 ist Haushalt, kein Feature-Code). Step 2 (P1-Erweiterungen)
fügt acht Tests in `phase1_storage/tests/` hinzu, nicht hier.

## Geerbte Contracts

Aus P1 (`phase1_storage/CLAUDE.md`, `docs/concepts/phase1_storage_plan.md` §1/§2): Frontmatter-
Schema, `Item`/`SpaceInfo`/`ItemSummary`/`SearchResult`/`IndexStats`, `Store`-Signaturen
(`list_spaces`/`search`/`get`/`create`/`update`/`append`/`archive`/`rebuild_index`),
Fehlertypen inkl. `ConflictError.current`. Drei einmalige, vom Nikinger freigegebene
Erweiterungen kommen in Step 2 dieser Phase (`space_of()`, `get(..., repair_drift=)`,
Statusvalidierung) — danach ist der Contract wieder zu.

**D1, festgehalten statt stillschweigend übernommen:** `docs/concepts/PHASE1_CLOSEOUT_HANDOVER.md`
verlangte ausdrücklich Gegenprüfung von `ItemSummary` und `SpaceInfo.name`/`.item_count` (beides
Claude-Code-Eigenentscheidungen aus P1, im P1-Plan nicht spezifiziert), bevor P2 darauf aufbaut.
Der P2-Plan (`docs/concepts/phase2_mcp_plan.md` §0.2) übernimmt beide bereits als „gegeben" —
das zählt als Bestätigung durch die Browser-Planungssession mit dem Nikinger. Hier trotzdem
explizit vermerkt: **gilt als bestätigt, wenn der Nikinger nicht widerspricht** (siehe
Step-0-Session-Block unten).

**Warum nur Hashes im Keyring** (vorgezogen aus Plan §2.3, wird in Step 3 mit Code belegt): der
Server muss ein Token nur *wiedererkennen*, nie *vorzeigen*. Wer diese Eigenschaft aufgibt, um
„das Token nochmal anzeigen" zu können, macht aus dem Keyring eine Passwortliste.

**Was der Pfad-Token nicht ist** (vorgezogen aus Plan §2.3): kein OAuth-Ersatz, kein Schutz
gegen Cloudflare (R4 — Cloudflare sieht bei P3 ohnehin Klartext), gültig bis P3+1. Siehe
P2-Plan §0.3 für die Begründung, warum OAuth trotzdem hinter P3 bleibt statt vorgezogen zu
werden.

**`version` in fremden Spaces** (vorgezogen aus Plan §3.4, wird in Step 3 wirksam): sobald
`get(..., repair_drift=)` existiert, ist `version` in fremden Spaces informativ, nicht
autoritativ — dort gibt es per Architektur keine Writes.

---

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
