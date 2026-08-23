---
status: live
purpose: Phasenplan des Space-Servers — was in welcher Reihenfolge gebaut wird und warum, plus Status je Phase
read-when: Phasenwechsel, Scope-Frage („gehört X in diese Phase?"), Planung einer neuen Session
detail: L2
up: CLAUDE.md
down:
  - docs/concepts/phase1_storage_plan.md   # ausführungsreifer P1-Plan
  - docs/concepts/phase2_mcp_plan.md       # ausführungsreifer P2-Plan
  - docs/concepts/phase3_edge_plan.md      # ausführungsreifer P3-Plan
  - docs/concepts/phase4_auth_plan.md      # ausführungsreifer P4-Plan
  - docs/concepts/phase5_ui_plan.md        # ausführungsreifer P5-Plan
  - docs/concepts/phase6_shares_plan.md    # ausführungsreifer P6-Plan
  - docs/concepts/phase6_5_tools_images_plan.md   # ausführungsreifer P6.5-Plan
  - docs/concepts/phase7_spaces_admin_plan.md     # ausführungsreifer P7-Plan
updated: 2026-08-23 (Phase 6.5 formal abgeschlossen als P7 Step A8 -- 🟡 code-complete, 12 von 14 Abnahmezeilen live, zwei per testnutzer-p7-Substitution, PHASE6_5_CLOSEOUT_HANDOVER.md neu) | 2026-08-23 (neue Phase 7 -- Space-Verwaltung, Mehrfachauswahl, Konsolidierung -- ergaenzt, Step 0 gestartet; fehlende P6.5-Tabellenzeile nachgetragen) | 2026-08-23 (Phase 6 auf 🟡 code-complete -- 12 von 39 Abnahmezeilen live, Sprung auf ✅ ist offene Nikinger-Entscheidung) | 2026-08-20 (neue Phase 6.5 -- Werkzeug-Ergonomie + Bilder -- ergaenzt, Step 0 gestartet)
---
# ROADMAP — Space-Server

**Build-Reihenfolge ist verbindlich.** Unter Zeit- oder Token-Druck fällt immer die *späteste*
Phase weg, nie eine frühere Regel. Insbesondere: die UI fällt weg, die Auth-Härtung nicht.

Statusglyphen: ⬜ nicht gestartet · 🔄 aktiv · 🟡 code-complete, nicht live-bewiesen · ✅ live-verifiziert

| Phase | Verzeichnis / Paket | Inhalt | Status |
|---|---|---|---|
| **P1** | `phase1_storage/` · `storage` | Datei-Store + Index + Versionierung. Kein Netz. | ✅ |
| **P2** | `phase2_mcp/` · `mcpserver` | MCP-Server, Token-Auth, 6 Tools. Lokal erreichbar. | ✅ |
| **P3** | `phase3_edge/` | Tunnel, systemd, Health, Logging, Ops-Skripte. Öffentlich erreichbar. | ✅ |
| **P4** | `phase4_auth/` · `authserver` | OAuth 2.1 + DCR; ersetzt den Pfad-Token. | ✅ |
| **P5** | `phase5_ui/` · `webui` | REST-API + Web-UI für Menschen. | ✅ |
| **P6** | `phase6_shares/` (kein eigenes Paket) | Freigaben, Ordner, `patch_item`, Update-Log, Bilder. | 🟡 |
| **P6.5** | `phase6_5_tools_images/` (kein eigenes Paket) | Werkzeug-Ergonomie, Abschluss Bilder. | 🟡 |
| **P7** | `phase7_spaces_admin/` (kein eigenes Paket) | Space-Verwaltung, Mehrfachauswahl, Konsolidierung. | 🔄 |

**[2026-08-23 Korrektur, P7 Step 0]:** P6.5 fehlte als eigene Tabellenzeile — beim Ergänzen der
P7-Zeile mitgefunden und nachgetragen, keine inhaltliche Änderung.

**Korrektur (2026-07-25, P2-Planungssession):** OAuth rückt von „ganz am Ende" auf „direkt nach
P3" — der Pfad-Token soll kurz leben, und die UI ist die Phase, die laut Build-Reihenfolge unter
Druck wegfallen darf, OAuth nicht. Begründung: `docs/concepts/phase2_mcp_plan.md` §0.3.

---

## Phase 1 — Storage-Kern

**Mission:** Ein Datenmodell, das Menschen im Editor und Claude über Tools *gleichzeitig*
benutzen können, ohne sich gegenseitig zu überschreiben. Das ist der harte Teil, nicht MCP.

- **DRIN:** Frontmatter-Modelle, atomarer Datei-Store, SQLite-Index + Rebuild, optimistic
  Locking, Git-Commit je Write, Query-Layer (nur Frontmatter im Listing), CLI als Beweis.
- **DRAUSSEN:** MCP, HTTP, Auth, Tunnel, UI, Volltextsuche über Bodies, Anhänge.
- **Warum zuerst:** ohne Konfliktbehandlung produziert jede spätere Phase stillen Datenverlust,
  und stiller Datenverlust wird erst bemerkt, wenn er nicht mehr reparabel ist.

Plan: `docs/concepts/phase1_storage_plan.md`. Phase-Head: `phase1_storage/CLAUDE.md`.

**Korrektur (2026-07-25):** Alle acht Module (Steps 0–7) fertig, 68 Tests grün (70 bei
Phasenabschluss, minus zwei bei Entfernung toten Codes — `rename_for_new_slug()` — in P2 Step 0),
`space_cli.py` als Beweis. Status **✅ live-verifiziert**: der Nikinger hat den Lauf gegen den
echten `DATA_ROOT` (`/home/savefyx/savefyx-data`) selbst ausgeführt (Hard Rule: kein Test gegen
den echten DATA_ROOT durch Claude Code) — `create`/`list`/`search` funktionieren, der Git-Commit
im Datenverzeichnis landet real, `.gitignore` hält `.index.sqlite3`/`.write.lock` draußen (die
reale Probe auf den Advisor-Fund aus Step 5). Details + Transkript:
`phase1_storage/CLAUDE.md`, Session-Block. Handover an P2:
`docs/concepts/PHASE1_CLOSEOUT_HANDOVER.md`.

## Phase 2 — MCP-Server

**Mission:** Claude kann lesen und schreiben — lokal, ohne Tunnel.

- **DRIN:** `fastmcp` über Streamable HTTP, Token→Space-Auflösung, sechs Tools
  (`list_spaces`, `search_items`, `get_item`, `create_item`, `update_item`, `append_to_item`),
  `<untrusted_content>`-Wrapping fremder Bodies, Token-Budget-Disziplin im Listing.
- **DRAUSSEN:** Löschen (`status: archived` reicht), MCP Resources, MCP Prompts, OAuth,
  öffentliche Erreichbarkeit.
- **Explizit gegen MCP Resources entschieden:** Tools sind der verlässliche Pfad in Claude.ai.
  Wer Resources ergänzen will, muss es vorher messen, nicht annehmen.

Plan: `docs/concepts/phase2_mcp_plan.md`. Phase-Head: `phase2_mcp/CLAUDE.md`.

**Stand 2026-07-26:** alle acht Module (Steps 0–7) fertig, 133 Tests grün (76 P1 + 57 P2),
`mcp_smoke.py` als Beweis (Gegenstück zu `space_cli.py` aus P1). Status **✅ live-verifiziert**:
der Nikinger hat die Quick-Tunnel-Probe **und** eine vollständige Adapter-Abnahme über den
echten Custom Connector gefahren — 21 von 21 Prüfungen gegen den echten `DATA_ROOT`, mit
Rohantworten als Beweis. Protokoll: `docs/concepts/P2_ADAPTER_ABNAHME_2026-07-26.md`. Ein Fund
(fehlende Sichtbarkeit des eigenen, noch leeren Space in `list_spaces`) wurde noch am selben Tag
behoben; ein zweiter (Space-Namen `nikinger`/`niklas` gemischt) wurde vom Nikinger direkt am
echten `DATA_ROOT` behoben (`nikinger/` → `niklas/`, siehe `phase2_mcp/CLAUDE.md`). Keine
offenen Findings mehr. Handover an P3: `docs/concepts/PHASE2_CLOSEOUT_HANDOVER.md`.

### Zurückgestellt aus P2 (bewusst, nicht vergessen)

- **D6 — `Store.search()` liest jede indizierte Datei von der Platte.** Gefiltert/sortiert wird
  in Python, nicht in SQL. Bei zwei Nutzern und einigen hundert Items unkritisch, aber P2 hängt
  das an einen Mobilfunk-Uplink. Kostenfrage, kein Bug — SQL-Filterung ist eine
  contract-neutrale Optimierung im `storage`-Paket, kein Adapter-Thema.
- **MCP-Revision 2026-07-28** (Sessions entfallen, `Mcp-Method`/`Mcp-Name`-Header werden Pflicht)
  — nicht in P2 adressiert. **Korrektur (2026-07-27, P3 Step 0):** Migration hängt an einem
  **Trigger, nicht an einem Datum** — erstes `fastmcp`-Release mit Support für die neue Revision.
  P3-E (`docs/concepts/phase3_edge_plan.md`) begründet das: `fastmcp` 3.4.4 hat noch keinen
  Support, bestehende 2025-11-25-Server brechen laut MCP-Blog nicht, neue Clients handeln
  herunter. Watch-Item, keine Terminfrage.
- **Lese-Rechte zwischen Spaces.** Der Seam existiert ab P2 (`Permissions.can_read`, heute immer
  `True`, aber schon von jedem Lesepfad aufgerufen), die Policy fehlt bewusst. Siehe „Bewusst
  nicht auf der Roadmap" unten — der Satz dort bleibt richtig, der Seam macht ihn nur nicht mehr
  unumkehrbar.

## Phase 3 — Exposure & Betrieb

**Mission:** Der Connector steht in beiden Claude-Accounts und bleibt stehen.

- **DRIN:** Tailscale Funnel (Korrektur 2026-07-28: ersetzt die ursprünglich geplante
  Cloudflare-Tunnel-Zeile, siehe P3-A), systemd-Unit (`Restart=on-failure`,
  `LoadCredentialEncrypted`), `/health`, strukturiertes Request-Log mit Tool-Name und Dauer,
  Backup des Datenverzeichnisses, Runbook „Connector zeigt Disconnected".
- **DRAUSSEN:** VPS-Migration (dokumentierte Option, eigener Track), Monitoring/Alerting.
- **Bekanntes Risiko:** Mobilfunk-Uplink. Claude zeigt bei Nichterreichbarkeit nur
  „Disconnected" mit minimaler Diagnose — deshalb ist das Log kein Nice-to-have, sondern
  Teil des Scope.

**Status ✅ (2026-07-27, Live-Abnahme zweite Session; 2026-07-29/2026-08-02 fortgeschrieben):**
10 von 13 Abnahmezeilen live bestanden am 2026-07-27 (Details: `docs/concepts/
P3_ABNAHME_2026-07-27.md`). Nikinger-Entscheidung: Reboot-Test (Zeile 6), Backup-Timer-Lauf
(Zeile 12) und Restore-Nachweis (Zeile 13) werden nicht mehr aktiv nachgeholt, sondern auf die
nächste Phase verschoben — ein unbeabsichtigter Reboot ist ohnehin der reale Prüffall, 12/13
lösen sich mit dem nächsten Backup-Zyklus. **[2026-07-29:]** Zeile 12 löste sich mit dem
P4-Step-0-Backup-Zyklus, Zeile 6 mit einem unbeabsichtigten Reboot der VM
(Windows-Host-Neustart des Nikingers) — beide jetzt ✅, Belege in `phase3_edge/CLAUDE.md`.
Damit stehen **12 von 13**. **[2026-08-02, P5 Step 0:]** Claude Code fuhr `restore_check.sh`
(Zeile 13, Restore-Nachweis) zunächst selbst read-only gegen das frischeste Backup-Bundle
(`sharefyx-data-20260801T220156.234086Z.bundle`, `ok:true`) — bewusst nur als Kandidatenbeleg
gewertet, da dieser Prompt „jeden End-to-End-Test gegen das echte Datenverzeichnis" dem
Nikinger vorbehält. **Der Nikinger hat denselben Lauf danach selbst ausgeführt** (identischer
HEAD `3756c26a…`, `ok:true`) und im selben Zug Step-0-A.7 live nachgezogen
(`install_units.sh`, Restart, `/health`, `spaces.cred` gelöscht). **13 von 13 Abnahmezeilen
live bestanden — Status ✅.** Details: `phase3_edge/CLAUDE.md` Session-Block 2026-08-02.

## Phase 4 — OAuth 2.1

**Mission:** Der Pfad-Token verschwindet.

**Status ✅ (2026-07-30, Schnitt vollzogen):** 16 von 16 Prüfungen live bestanden — Discovery,
DCR, Consent, Token-Ausgabe, beide RFC-9700-Replay-Abwehren, Rule 4 unter echtem OAuth **und**
einem zweiten, unabhängigen Nutzer (Fabian), Fehlversuchsbremse, Token-Ablauf/Auto-Refresh
(belegt on-demand, kein Hintergrund-Timer), Pfad-Token tot (Runbook-Schritt 8, live
gegenverifiziert: `SPACE_AUTH_MODE=oauth`, `export_space_map.py` → 0 Einträge, alte
Pfad-Token-URL → 401). `TokenPathASGI`/`AuthModeASGI` sind im selben Commit wie die Abnahme aus
dem Code entfernt, `SPACE_AUTH_MODE` auf einen Wert reduziert (`oauth`) — Plan-Wortlaut „auf
zwei Werte reduzieren" war ohne frischen Repo-Zugriff geschrieben und ungenau, siehe
`authserver/config.py`. Protokoll: `docs/concepts/P4_ABNAHME_2026-07-29.md` (drei Nachträge,
2026-07-30). Sicherheits-Review (kein Auth-Bypass, kein Cross-Space-Leck) in
`docs/concepts/P4_SECURITY_REVIEW_2026-07-29.md` — Befunde S2–S8/O1 bleiben offen, bewusst nicht
Teil dieses Schnitts.

- **DRIN:** Protected Resource Metadata, Authorization Server, Dynamic Client Registration,
  PKCE, Token-Rotation. `[VERIFY]` Callback-URLs und unterstützte Auth-Spec-Version gegen die
  aktuelle Anthropic-Doku — das ändert sich schneller als dieses Dokument.
- **Warum direkt nach P3 statt ganz am Ende (Korrektur 2026-07-25):** der Pfad-Token soll kurz
  leben; P2 baut den Seam dafür bereits (`SpaceResolver` liefert einen `Principal`, egal ob aus
  Pfad-Token oder OAuth-Access-Token — der Umbau berührt keine Zeile Tool-Code). Nicht
  optional-für-immer: P4 ist der lehrreichste Teil des gesamten Projekts. Wer ihn dauerhaft
  überspringt, hat ein Ablagesystem gebaut und nichts gelernt.
- **Korrektur (2026-07-28, P4-Planungssession):** Paketname ist `authserver`, nicht `auth` wie
  oben in der Tabelle ursprünglich vorgesehen — `mcpserver/auth.py` existiert seit P2, ein
  zweites Top-Level-Paket `auth` daneben wäre für Menschen und `grep` eine Falle
  (`docs/concepts/phase4_auth_plan.md`, Entscheidung P4-B). Tabelle oben bereits korrigiert.

## Phase 5 — Web-UI

**Mission:** Menschen legen Aufgaben und Notizen ohne Editor an.

- **DRIN:** REST-API über demselben Storage-Kern, UI gegen diese API.
- **DRAUSSEN:** Realtime/Collaboration, Anhänge, Mobile-App.
- ~~**Offene Entscheidung:** Neubau vs. Adaption des `Notizheft_example.html`.~~ **[2026-08-02
  Korrektur, P5-Planungssession, Entscheidung P5-V]:** entschieden — **Neubau mit Ernte**.
  Übernommen werden Layout-Ideen sowie `sanitizeHtml`/`markdownToHtml`; verworfen wird die
  clientseitige Vault-Verschlüsselung (unvereinbar mit R4), `localStorage`/IndexedDB als
  Speicher und `connect-src 'none'`. Details: `docs/concepts/phase5_ui_plan.md` §0.5.
- **Rückt hinter OAuth (Korrektur 2026-07-25):** die UI ist die Phase, die unter Zeit-/Token-
  Druck wegfallen darf; OAuth nicht. Innerhalb der Phase gilt dieselbe Regel eine Ebene tiefer:
  unter Druck fällt Block B (REST-API/UI) weg, nicht Block A (Sicherheit/Auth-Selbstverwaltung).
- **Erweiterung (2026-08-02 Planungssession):** Scope wächst gegenüber der ursprünglichen
  Roadmap-Zeile um **Auth-Selbstverwaltung** (Einladung, Passwort/TOTP/Recovery-Code selbst
  setzen, ohne SSH/Neustart) — kommt aus `docs/concepts/PHASE4_CLOSEOUT_HANDOVER.md` §4.1 und
  ist ausdrücklich Block A der Phase, nicht optional. Ohne sie ist die UI eine Oberfläche auf
  einem Konto, das nur per SSH existiert.

**Status ✅ (2026-08-09):** Abnahmematrix vollständig — 20/20 Zeilen live bestanden, 0 teilweise,
0 offen (`docs/concepts/P5_ABNAHME_2026-08-09.md`). Beide Blöcke (A Sicherheit/
Auth-Selbstverwaltung, B REST-API/UI) durch das harte Gate. `git diff` auf `storage/`,
`mcpserver/{tools,permissions,server}.py` blieb über die gesamte Phase leer (Kriterium 18).
Formaler Abschluss-Handover an P6: `docs/concepts/PHASE5_CLOSEOUT_HANDOVER.md`. Phase-Head:
`phase5_ui/CLAUDE.md`.

---

## Phase 6 — Freigaben, Ordner, Werkzeug-Ergonomie

**Mission:** Drei Dinge beweisbar — punktuelle Textkorrektur statt Komplett-Rewrite
(`patch_item`), Menschen entscheiden pro Item wer es sieht plus Orte, an denen mehrere gemeinsam
schreiben, und das System verträgt einen dritten Nutzer ohne Codeänderung.

- **DRIN:** `patch_item` + Quittungen statt Volltext, Sichtbarkeitsstufen (`private`/`human`),
  Item- und Ordner-/Space-Freigaben, echte Ordner, Update-Log/Banner, Bild-Assets als verlinkte
  Dateien.
- **DRAUSSEN:** Löschen von Items, FastMCP-4/CIMD/DPoP, Volltext-/semantische Suche, Realtime,
  Mobilversion, Rechteverwaltung über MCP-Tools, HEIC, serverseitiges Bild-Rendering.
- Steht in **keiner** ursprünglichen Roadmap-Zeile — ein QoS-Schnitt aus echtem Betrieb (siehe
  „Phase-6-Vormerkungen" in Root-`CLAUDE.md`, jetzt hier eingepflegt). Drei Blöcke, ein hartes
  Gate: A = Werkzeuge/Betrieb/Update-Banner, B = Dateisystem, C = Bilder — unter Druck fällt
  zuerst C weg, dann Bs geteilte Spaces, **nie Block A**.

**Status 🔄 (2026-08-13):** Block A (Steps 0–3) vollständig gebaut, Gate A→B 3/4 Punkte live
bestanden. Block B Steps 4–6 (Storage-Fundament, Rechtepolitik, Verwaltung/Migration) ✅ gebaut
**und seit 2026-08-13 live deployed** (`main`@`d068d1c`) — Cutover auf die neue `SharePolicy`
vollzogen, eine Leserichtung (niklas→fabian) über den echten Connector live-verifiziert, die
andere offen. Ein UI-Fund (geteilte Spaces zeigten „nur lesen" trotz Schreibrecht) hatte zwei
Teile — Space-Listen-Badge ist deployed und live bestätigt, ein zweiter Teil (Anlegen-Knopf/
Text innerhalb des Spaces, dieselbe Ursachenkategorie an anderer Stelle) ist behoben, aber noch
nicht deployed. Eine Planungsvormerkung für die nächste Session (Item-Verschieben zwischen
Ordnern/Spaces) steht offen. Herkunft: `docs/concepts/PHASE5_CLOSEOUT_HANDOVER.md` §4.1–§4.6. Plan:
`docs/concepts/phase6_shares_plan.md` (Entscheidungen P6-A–P6-AC, Steps 0–10). Details:
`phase6_shares/CLAUDE.md`s Session-Block vom 2026-08-13.

**Status-Korrektur (2026-08-23, Phasenabschluss): 🔄 → 🟡, bewusst nicht ✅.** Sämtlicher P6-Code
ist gebaut und live deployt (`main`@`f96125e`), aber nur **12 von 39 Abnahmezeilen** sind
live-verifiziert — und die Statusregel dieses Projekts sagt „✅ heißt live-verifiziert, nicht
gebaut". Vier Zeilen (31–34, §9 Mehrfachauswahl) wurden nie gebaut; Block C (Zeilen 19–22/40–47,
Bilder) ist nach Phase 6.5 ausgewandert; sieben weitere Zeilen hängen an einer Sitzung mit
Fabians eigenem Login. **Der Sprung auf ✅ ist eine offene Nikinger-Entscheidung.** Vollständiger
Zeilenstatus, offene Entscheidungen und `[VERIFY]`-Bilanz:
`docs/concepts/PHASE6_CLOSEOUT_HANDOVER.md`. Übersichtsgrafik:
`docs/concepts/phase6_shares_uebersicht.svg`.

---

## Phase 6.5 — Werkzeug-Ergonomie und Bilder

**Mission, zwei Blöcke:** (A) Eine arbeitende Claude-Instanz findet ihre Werkzeuge, versteht deren
Aufgabenteilung aus der Beschreibung und zahlt keine Tausende Token für eine Versionsnummer.
(B) Ein Bild liegt im Space, ist im Dokument sichtbar, technisch nur ein Link — und Claude sieht
seine Bytes nur, wenn ein Mensch ausdrücklich danach fragt.

- **DRIN:** fünf offene MCP-Werkzeug-Ergonomie-Punkte (`list_spaces`-Beschreibungsfehler,
  `patch_item`/`update_item`-Aufgabenteilung, `get_item_meta`, Status-Enum in Tool-Beschreibungen,
  Body-Suche als MCP-Opt-in), Abschluss Block C Bilder (Speicherung als Asset-Datei, Referenz im
  Body, MCP-Lesen nur bei Schreibrecht und nie automatisch, MCP-Upload mit Ankündigungspflicht,
  Entfernen per Verschieben nach `_trash/`).
- **DRAUSSEN:** Bulk-Append-Tool (Befund: heute schon über mehrzeiligen Text möglich), Body-
  Volltextsuche in der Web-UI (Q1 bleibt gelockt), automatische `_trash/`-Räumung (Vormerkung,
  kein Auftrag), Space-Admin-UI (bleibt Phase 7), Rechteverwaltung über MCP-Tools, HEIC/SVG/PDF
  als Bildformat, serverseitiges Bild-Rendering.
- Sitzt bewusst zwischen Phase 6 und Phase 7 — kein Space-Admin-UI-Scope, `app.html`s „kommt in
  Phase 7"-Zeichenkette bleibt unangetastet und korrekt. Zwei Blöcke, kein hartes Gate zwischen
  ihnen (Block B bei Zeitdruck komplett verschiebbar, Block A nicht).

**Status-Korrektur (2026-08-23, formaler Abschluss als P7 Step A8): 🔄 → 🟡, bewusst nicht ✅.**
Sämtlicher P6.5-Code ist gebaut und live deployt (`main`@`f96125e`), **12 von 14 Abnahmezeilen**
sind live-verifiziert (zwei davon über eine im P7-Plan §A8.1 gebilligte Substitution —
`testnutzer-p7` statt Fabian). Verbleibend offen: P6.5-12 (Entfernen-Knopf inzwischen von P7
Step A3 gebaut, kein Browser-Klick-Nachweis) und P6.5-14 (Nikingers eigene Bewertung, kein
Selbstzertifizierungs-Kriterium). **Der Sprung auf ✅ ist eine offene Nikinger-Entscheidung.**
Vollständiger Zeilenstatus, offene Entscheidungen und `[VERIFY]`-Bilanz:
`docs/concepts/PHASE6_5_CLOSEOUT_HANDOVER.md`. Übersichtsgrafik:
`docs/concepts/phase6_5_tools_images_uebersicht.svg`.

---

## Phase 7 — Space-Verwaltung, Mehrfachauswahl, Konsolidierung

**Mission, drei Blöcke:** (A) ein Mensch findet ein Item wieder, das eine Claude-Instanz ihm
gegenüber `itm_807df219` genannt hat, und kann ein eingefügtes Bild wieder loswerden. (C) ein
Mensch entscheidet im Browser, wer seinen Space lesen darf, legt einen geteilten Space an und
wird einen wieder los, ohne dass dabei ein Item verloren geht. (B) zehn Items wandern in einem
Vorgang in denselben Zielordner, mit einem Re-Auth-Formular statt zehn.

- **DRIN:** Item-ID sichtbar + auffindbar, Bild-Entfernen-Knopf (schließt P6.5-12), Feld-
  Whitelist an `_items_patch` (schließt O6), Doku-Audit der P6-Modul-Zeilen 8–16, Sichtbarkeits-
  Migration live, dritter Principal `testnutzer-p7`, formaler Abschluss Phase 6.5, volle
  Space-Verwaltung in der Weboberfläche (anlegen/Mitglieder/entfernen, Home-Spaces ausgenommen
  vom Anlegen/Entfernen), Mehrfachauswahl (`ITEM_MOVE_PLAN.md` §9).
- **DRAUSSEN:** FastMCP-4-Umstieg, `owner:`-Feld in `.share.yml`, Löschen von Items,
  Rechteverwaltung über MCP-Tools, automatische `_trash/`-Räumung, Funnel-Watchdog, Body-
  Volltextsuche in der Web-UI, Mehrfachauswahl für andere Aktionen als Verschieben.
- **Reihenfolge 0 → A → Gate → C → B** (bewusst nicht die Buchstabenfolge) — Block C trägt den
  Namen dieser Phase (seit P6 Step 7 Commit 6 in `app.html` als „kommt in Phase 7" reserviert)
  und fällt unter Druck nie vor Block B.

**Status 🔄 (2026-08-23, Step 0 läuft):** Plan `docs/concepts/phase7_spaces_admin_plan.md`
ausführungsreif, alle zehn Nikinger-Fragen N1–N10 in §0.1 gelockt. Step 0.1–0.6 gefahren: `pytest`
828 grün, Doku-Audit der P6-Modul-Zeilen 8–16 + Vormerkungspunkt 2 mit SHA-Beweis abgeschlossen
(alle live deployt, Stale-Doku in `phase6_shares/CLAUDE.md`/Root-`CLAUDE.md`/`docs/INDEX.md`
korrigiert), ein Link-Fund behoben (`docs/PROMPTS.md`), Softcap-Prüfung 12/12 konform, Skelett
angelegt. Herkunft: `docs/concepts/PHASE6_CLOSEOUT_HANDOVER.md`. Details:
`phase7_spaces_admin/CLAUDE.md`s Session-Block.

---

## Bewusst nicht auf der Roadmap

- **Semantische Suche / Embeddings.** Verstößt gegen das Bauprinzip. Bei zwei Nutzern und
  einigen hundert Items schlägt Frontmatter-Filterung jede Vektorsuche in Präzision und Kosten.
- ~~**Feingranulare Rechte.** Zwei Personen, gegenseitiges Vertrauen. Cross-Space-Read ist
  standardmäßig an. Der Schutz gegen fremde Inhalte ist Rule 4, nicht ein ACL-Modell.~~
  **Ergänzung 2026-07-25:** P2 baut den Seam dafür (`Permissions.can_read`), damit es später kein
  Umbau wird — die Policy selbst bleibt bewusst `True` für alle, siehe „Zurückgestellt aus P2".
  **[2026-08-09 Korrektur, P6-Planungssession]:** Der Satz war bis heute richtig; mit Phase 6
  wird er widerlegt — Sichtbarkeitsstufen und Item-/Ordner-Freigaben (P6-J/K) sind jetzt Scope.
  Details: `docs/concepts/phase6_shares_plan.md` §0.5.
- **Mehrmandantenfähigkeit.** Wenn ein dritter Nutzer dazukommt, ist das eine Planungssession,
  kein `if`-Zweig. **[2026-08-09 Korrektur, P6-Planungssession]:** Der Satz ist **erfüllt, nicht
  widerlegt** — die Planungssession hat am 2026-08-09 stattgefunden und genau daraus ist Phase 6
  entstanden; ein dritter Nutzer wird darin real angelegt, geprüft und wieder entfernt (P6-W),
  über eine echte Planungssession, keinen stillen `if`-Zweig.
