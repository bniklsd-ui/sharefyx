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
updated: 2026-08-02
---
# ROADMAP — Space-Server

**Build-Reihenfolge ist verbindlich.** Unter Zeit- oder Token-Druck fällt immer die *späteste*
Phase weg, nie eine frühere Regel. Insbesondere: die UI fällt weg, die Auth-Härtung nicht.

Statusglyphen: ⬜ nicht gestartet · 🔄 aktiv · 🟡 code-complete, nicht live-bewiesen · ✅ live-verifiziert

| Phase | Verzeichnis / Paket | Inhalt | Status |
|---|---|---|---|
| **P1** | `phase1_storage/` · `storage` | Datei-Store + Index + Versionierung. Kein Netz. | ✅ |
| **P2** | `phase2_mcp/` · `mcpserver` | MCP-Server, Token-Auth, 6 Tools. Lokal erreichbar. | ✅ |
| **P3** | `phase3_edge/` | Tunnel, systemd, Health, Logging, Ops-Skripte. Öffentlich erreichbar. | 🟡 |
| **P4** | `phase4_auth/` · `authserver` | OAuth 2.1 + DCR; ersetzt den Pfad-Token. | ✅ |
| **P5** | `phase5_ui/` · `webui` | REST-API + Web-UI für Menschen. | 🔄 |

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

**Status 🟡 (2026-07-27, Live-Abnahme zweite Session; 2026-07-29/2026-08-02 fortgeschrieben):**
10 von 13 Abnahmezeilen live bestanden am 2026-07-27 (Details: `docs/concepts/
P3_ABNAHME_2026-07-27.md`). Nikinger-Entscheidung: Reboot-Test (Zeile 6), Backup-Timer-Lauf
(Zeile 12) und Restore-Nachweis (Zeile 13) werden nicht mehr aktiv nachgeholt, sondern auf die
nächste Phase verschoben — ein unbeabsichtigter Reboot ist ohnehin der reale Prüffall, 12/13
lösen sich mit dem nächsten Backup-Zyklus. **[2026-07-29:]** Zeile 12 löste sich mit dem
P4-Step-0-Backup-Zyklus, Zeile 6 mit einem unbeabsichtigten Reboot der VM
(Windows-Host-Neustart des Nikingers) — beide jetzt ✅, Belege in `phase3_edge/CLAUDE.md`.
Damit stehen **12 von 13**. **[2026-08-02, P5 Step 0:]** Claude Code hat `restore_check.sh`
(Zeile 13, Restore-Nachweis) read-only gegen das frischeste Backup-Bundle
(`sharefyx-data-20260801T220156.234086Z.bundle`) gefahren — Ergebnis `ok:true`, HEAD und Baum
identisch mit dem echten `DATA_ROOT`. **Bewusst noch nicht als ✅ gewertet:** dieser Prompt
reserviert „jeden End-to-End-Test gegen das echte Datenverzeichnis" für den Nikinger selbst: der
Lauf hier ist ein Kandidatenbeleg, keine Abnahme. Status bleibt 🟡, bis der Nikinger den Lauf
bestätigt oder selbst wiederholt (ein Befehl, siehe `phase3_edge/CLAUDE.md` Session-Block
2026-08-02).

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

**Status 🔄 (2026-08-02):** Planungssession abgeschlossen, ausführungsreifer Plan liegt vor
(`docs/concepts/phase5_ui_plan.md`, Entscheidungen P5-A–P5-AE, Steps 0–9). Step 0 (Haushalt,
Rückbau, Doku-Drift) läuft. Phase-Head: `phase5_ui/CLAUDE.md`.

---

## Bewusst nicht auf der Roadmap

- **Semantische Suche / Embeddings.** Verstößt gegen das Bauprinzip. Bei zwei Nutzern und
  einigen hundert Items schlägt Frontmatter-Filterung jede Vektorsuche in Präzision und Kosten.
- **Feingranulare Rechte.** Zwei Personen, gegenseitiges Vertrauen. Cross-Space-Read ist
  standardmäßig an. Der Schutz gegen fremde Inhalte ist Rule 4, nicht ein ACL-Modell. **Ergänzung
  2026-07-25:** P2 baut den Seam dafür (`Permissions.can_read`), damit es später kein Umbau wird
  — die Policy selbst bleibt bewusst `True` für alle, siehe „Zurückgestellt aus P2".
- **Mehrmandantenfähigkeit.** Wenn ein dritter Nutzer dazukommt, ist das eine Planungssession,
  kein `if`-Zweig.
