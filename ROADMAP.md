---
status: live
purpose: Phasenplan des Space-Servers — was in welcher Reihenfolge gebaut wird und warum, plus Status je Phase
read-when: Phasenwechsel, Scope-Frage („gehört X in diese Phase?"), Planung einer neuen Session
detail: L2
up: CLAUDE.md
down:
  - docs/concepts/phase1_storage_plan.md   # ausführungsreifer P1-Plan
updated: 2026-07-25
---
# ROADMAP — Space-Server

**Build-Reihenfolge ist verbindlich.** Unter Zeit- oder Token-Druck fällt immer die *späteste*
Phase weg, nie eine frühere Regel. Insbesondere: die UI fällt weg, die Auth-Härtung nicht.

Statusglyphen: ⬜ nicht gestartet · 🔄 aktiv · 🟡 code-complete, nicht live-bewiesen · ✅ live-verifiziert

| Phase | Verzeichnis / Paket | Inhalt | Status |
|---|---|---|---|
| **P1** | `phase1_storage/` · `storage` | Datei-Store + Index + Versionierung. Kein Netz. | 🟡 |
| **P2** | `phase2_mcp/` · `mcpserver` | MCP-Server, Token-Auth, 6 Tools. Lokal erreichbar. | ⬜ |
| **P3** | `phase3_edge/` | Tunnel, systemd, Health, Logging, Ops-Skripte. Öffentlich erreichbar. | ⬜ |
| **P4** | `phase4_ui/` · `webui` | REST-API + Web-UI für Menschen. | ⬜ |
| **P5** | `phase5_auth/` · `auth` | OAuth 2.1 + DCR; ersetzt den Pfad-Token. | ⬜ |

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

**Korrektur (2026-07-25):** Alle acht Module (Steps 0–7) sind fertig, 70 Tests grün, inklusive
der `space_cli.py` als Beweis (manueller Durchlauf: Space anlegen, Items finden, Konflikt
provozieren und verständlich anzeigen — alles gegen ein Scratch-Verzeichnis, nicht den echten
`DATA_ROOT`). Status **🟡, nicht ✅**: der offizielle Phasen-Abschluss (eigener Prompt, siehe
`docs/PROMPTS.md`) und ein Lauf gegen den echten `DATA_ROOT` stehen noch aus — Letzteres ist
Nikinger-Sache (Hard Rule: kein Test gegen den echten DATA_ROOT durch Claude Code).

## Phase 2 — MCP-Server

**Mission:** Claude kann lesen und schreiben — lokal, ohne Tunnel.

- **DRIN:** `fastmcp` über Streamable HTTP `[VERIFY]`, Token→Space-Auflösung, sechs Tools
  (`list_spaces`, `search_items`, `get_item`, `create_item`, `update_item`, `append_to_item`),
  `<untrusted_content>`-Wrapping fremder Bodies, Token-Budget-Disziplin im Listing.
- **DRAUSSEN:** Löschen (`status: archived` reicht), MCP Resources, MCP Prompts, OAuth,
  öffentliche Erreichbarkeit.
- **Explizit gegen MCP Resources entschieden:** Tools sind der verlässliche Pfad in Claude.ai.
  Wer Resources ergänzen will, muss es vorher messen, nicht annehmen.

## Phase 3 — Exposure & Betrieb

**Mission:** Der Connector steht in beiden Claude-Accounts und bleibt stehen.

- **DRIN:** Cloudflare Tunnel, systemd-Unit (`Restart=on-failure`, `LoadCredential`),
  `/health`, strukturiertes Request-Log mit Tool-Name und Dauer, Backup des Datenverzeichnisses,
  Runbook „Connector zeigt Disconnected".
- **DRAUSSEN:** VPS-Migration (dokumentierte Option, eigener Track), Monitoring/Alerting.
- **Bekanntes Risiko:** Mobilfunk-Uplink. Claude zeigt bei Nichterreichbarkeit nur
  „Disconnected" mit minimaler Diagnose — deshalb ist das Log kein Nice-to-have, sondern
  Teil des Scope.

## Phase 4 — Web-UI

**Mission:** Menschen legen Aufgaben und Notizen ohne Editor an.

- **DRIN:** REST-API über demselben Storage-Kern, UI gegen diese API.
- **DRAUSSEN:** Realtime/Collaboration, Anhänge, Mobile-App.
- **Offene Entscheidung:** Neubau vs. Adaption des `Notizheft_example.html`. Dessen
  clientseitige Verschlüsselung ist mit R4 unvereinbar und müsste entfallen — was den
  Anpassungsaufwand womöglich über den eines Neubaus hebt. Vor P4 in einer Planungssession
  klären, nicht während der Implementierung.

## Phase 5 — OAuth 2.1

**Mission:** Der Pfad-Token verschwindet.

- **DRIN:** Protected Resource Metadata, Authorization Server, Dynamic Client Registration,
  PKCE, Token-Rotation. `[VERIFY]` Callback-URLs und unterstützte Auth-Spec-Version gegen die
  aktuelle Anthropic-Doku — das ändert sich schneller als dieses Dokument.
- **Warum zuletzt und trotzdem nicht optional:** P5 ist der lehrreichste Teil des gesamten
  Projekts. Wer ihn dauerhaft überspringt, hat ein Ablagesystem gebaut und nichts gelernt.

---

## Bewusst nicht auf der Roadmap

- **Semantische Suche / Embeddings.** Verstößt gegen das Bauprinzip. Bei zwei Nutzern und
  einigen hundert Items schlägt Frontmatter-Filterung jede Vektorsuche in Präzision und Kosten.
- **Feingranulare Rechte.** Zwei Personen, gegenseitiges Vertrauen. Cross-Space-Read ist
  standardmäßig an. Der Schutz gegen fremde Inhalte ist Rule 4, nicht ein ACL-Modell.
- **Mehrmandantenfähigkeit.** Wenn ein dritter Nutzer dazukommt, ist das eine Planungssession,
  kein `if`-Zweig.
