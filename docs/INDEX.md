---
status: live
purpose: L0 map of every project .md — one line each; start navigation here
read-when: locating any doc, or deciding whether a file is worth reading at all
detail: L0
up: ../CLAUDE.md
down: every project doc (that is the point)
updated: 2026-07-29
---
# Doc Index (L0)

> **The layer model** (full spec: [DOC_LAYERS_CONVENTION.md](./DOC_LAYERS_CONVENTION.md)):
> **L0** = this index · **L1** = a living doc's ≤15-line header card (read via `Read` with
> `limit: 15` — decide from the card whether to descend, follow its `up:`/`down:` links to hop) ·
> **L2** = lean living bodies (≤40KB) · **L3** = archives & dated snapshots, read only when auditing.
>
> **Maintenance:** new .md file ⇒ add one line here in the same commit. Sizes are approximate.
> Oversize check: `find . -name "*.md" -not -path "./.agents/*" -not -path "*/.pytest_cache/*" -size +40k`
> — every hit must be a 📕/📦, never a 📗/🔄.
>
> Glyphs: 🔄 active-phase · 📗 live (maintained) · 📕 snapshot (dated, **never edit**) · 📦 archive (verbatim history).

## Root & governance

- [CLAUDE.md](../CLAUDE.md) — 📗 ~14KB · rules, core principle, hard rules, working style, current state; auto-loaded every session
- [AGENTS.md](../AGENTS.md) — 📗 ~1KB · harness-neutral entry point for non-Claude-Code agents; points to `CLAUDE.md` + doc-layers navigation
- [README.md](../README.md) — 📗 ~5KB · human overview + machine setup (venv, keyring, run, smoke test)
- [ROADMAP.md](../ROADMAP.md) — 📗 ~9KB · Phases 1–5, scope in/out per phase, status
- [docs/DOC_LAYERS_CONVENTION.md](./DOC_LAYERS_CONVENTION.md) — 📗 ~5KB · Doc-Layers-Spec (v1, 2026-07-06) · **byte-identische Kopie aus dem Trading-Bot-Repo — nicht projektspezifisch anpassen, sonst divergieren zwei Kopien derselben Regel**
- [docs/PROMPTS.md](./PROMPTS.md) — 📗 ~11KB · die drei Workflow-Prompts (Claude-Code-Session-Start, Phasen-Kickoff, Phasen-Abschluss); lesen beim Start eines neuen Chats, nicht mitten in einer Session

## Active phase (4 — OAuth 2.1 + DCR)

- [phase4_auth/CLAUDE.md](../phase4_auth/CLAUDE.md) — 🔄 ~35KB · phase head; Steps 0–6 ✅ (Step 6 mit allen drei Done-when-Klauseln belegt), Step 7 (Betrieb, Live-Abnahme, Schnitt) 🟡 **Code-Vorbereitung fertig** (`authctl.py`, Unit-Umzug nach `phase4_auth/systemd/`, `oauth_smoke.py --base-url`) — **Live-Teile stehen aus, Sache des Nikingers** (Runbook im Kopf); enthält seit 2026-07-29 die Kurztabelle der Sicherheitsbefunde S1–S8/O1; read + newest Session-stopped block first
- [docs/concepts/P4_SECURITY_REVIEW_2026-07-29.md](./concepts/P4_SECURITY_REVIEW_2026-07-29.md) — 📕 ~13KB · Sicherheits-Review P3+P4 vor der Live-Abnahme: Befund S1 (`ALLOWED_HOSTS` ohne `127.0.0.1` → `400 Invalid host header`, machte Runbook-Schritt 4 unausführbar, behoben) plus S2–S8/O1 offen, **und** 15 ausdrücklich geprüfte, in Ordnung befundene Punkte (verified negatives) — vor jedem Fix an einem der Befunde lesen
- [docs/concepts/phase4_auth_plan.md](./concepts/phase4_auth_plan.md) — 📕 ~76KB · ausführungsreifer P4-Plan (Entscheidungen P4-A–P4-R, Steps 0–7, eigener Authorization Server, Argon2id + TOTP, opake Token); über 40KB, aber als 📕-Snapshot vom Softcap ausgenommen; Autor Browser-Planungssession 2026-07-28, **ohne frischen Repo-Zugriff geschrieben** — Anker sind Funktionsnamen/Suchstrings, keine Zeilennummern
- [phase4_auth/SESSIONS_ARCHIVE.md](../phase4_auth/SESSIONS_ARCHIVE.md) — 📦 ~45KB · sieben archivierte Session-Blöcke (Step 0+1+2, Step 3, V14+Step 4, Step 5, Step 6a, Step 6b, Step-7-Code-Vorbereitung), verbatim, newest-first

## Completed phases

- [phase3_edge/CLAUDE.md](../phase3_edge/CLAUDE.md) — 📗 ~19KB · phase head; Steps 0–6 ✅, Step 7 (Live-Abnahme) 🟡 funktional beendet — jetzt 12/13 (Zeile 12 in P4 Step 0, Zeile 6 am 2026-07-29 durch einen unbeabsichtigten Reboot passiv erfüllt, beide live bestätigt); nur Zeile 13 (Restore-Nachweis) fehlt noch für ✅; **[P4 Step 7]** MCP-Unit zog nach `phase4_auth/systemd/` um; read + newest Session-stopped block first
- [docs/concepts/phase3_edge_plan.md](./concepts/phase3_edge_plan.md) — 📕 ~46KB · ausführungsreifer P3-Plan (Entscheidungen P3-A–P3-N, Steps 0–7); über 40KB, aber als 📕-Snapshot vom Softcap ausgenommen
- [phase3_edge/SESSIONS_ARCHIVE.md](../phase3_edge/SESSIONS_ARCHIVE.md) — 📦 ~53KB · zehn archivierte Session-Blöcke (Step 0–6, inkl. Live-Abnahme-Funde B3/B4, beide Live-Abnahme-Sessions vom 2026-07-27, Token-Rotation-Session vom 2026-07-28), verbatim, newest-first
- [docs/concepts/P3_ABNAHME_2026-07-27.md](./concepts/P3_ABNAHME_2026-07-27.md) — 📕 ~19KB · Abnahmeprotokoll Phase 3: 10/13 live bestanden, Zeilen 6/12/13 per Nikinger-Entscheidung auf nächste Phase verschoben, CLI-Ausschnitt als Beleg, Befunde B5/B6
- [docs/concepts/PHASE3_CLOSEOUT_HANDOVER.md](./concepts/PHASE3_CLOSEOUT_HANDOVER.md) — 📕 ~17KB · Abschluss-Handover P3→P4: Status, Delta seit dem P2-Handover, [VERIFY]-Bilanz V1–V13, geerbte Abnahmezeilen 6/12/13, Doku-Drift-Liste aus der Autocompact-Session inkl. Nachträgen zum nikinger-Token-Fund, offene Entscheidungen für die OAuth-Planung
- [docs/concepts/phase3_edge_uebersicht.svg](./concepts/phase3_edge_uebersicht.svg) — 📕 Übersichtsgrafik Phase 3 (Request-Weg, Komponenten)
- [phase2_mcp/CLAUDE.md](../phase2_mcp/CLAUDE.md) — 📗 ~20KB · phase head; Steps 0–7 ✅, **live-verifiziert** (Quick-Tunnel-Probe + Adapter-Abnahme durch den Nikinger, 2026-07-26); Quick-Tunnel-Runbook seit P3 Step 6 durch Verweis ersetzt; read + newest Session-stopped block first
- [docs/concepts/phase2_mcp_plan.md](./concepts/phase2_mcp_plan.md) — 📕 ~46KB · ausführungsreifer P2-Plan (Entscheidungen P2-A–P2-N, Steps 0–7); über 40KB, aber als 📕-Snapshot vom Softcap ausgenommen
- [docs/concepts/P2_ADAPTER_ABNAHME_2026-07-26.md](./concepts/P2_ADAPTER_ABNAHME_2026-07-26.md) — 📕 ~11KB · Abnahmeprotokoll über den echten Custom Connector, 21/21 Prüfungen, beide Befunde behoben (B1, B2 — siehe Nachtrag)
- [phase2_mcp/SESSIONS_ARCHIVE.md](../phase2_mcp/SESSIONS_ARCHIVE.md) — 📦 ~38KB · acht archivierte Session-Blöcke (Step 0–7), verbatim, newest-first
- [docs/concepts/PHASE2_CLOSEOUT_HANDOVER.md](./concepts/PHASE2_CLOSEOUT_HANDOVER.md) — 📕 ~11KB · Abschluss-Handover P2→P3: Status, Delta seit dem P1-Handover, offene Entscheidungen für die Exposure-Phase, [VERIFY]-Bilanz V1–V9
- [phase1_storage/CLAUDE.md](../phase1_storage/CLAUDE.md) — 📗 ~11KB · phase head; alle acht Module ✅, 76 Tests (inkl. acht P2-Contract-Erweiterungstests), live-verifiziert gegen den echten DATA_ROOT (2026-07-25); Frontmatter-Schema + `Store`-Signaturen jetzt Contract für P2
- [docs/concepts/phase1_storage_plan.md](./concepts/phase1_storage_plan.md) — 📕 ~15KB · ausführungsreifer P1-Plan (Entscheidungen A–H, Steps 0–7)
- [phase1_storage/SESSIONS_ARCHIVE.md](../phase1_storage/SESSIONS_ARCHIVE.md) — 📦 ~27KB · archivierte Session-stopped-Blöcke, verbatim, newest-first
- [docs/concepts/PHASE1_CLOSEOUT_HANDOVER.md](./concepts/PHASE1_CLOSEOUT_HANDOVER.md) — 📕 ~12KB · Abschluss-Handover P1→P2: Status, Delta, Contract, offene Entscheidungen D1–D6, `[VERIFY]`-Bilanz

## Concept docs (📕 snapshots — the plan a phase was built from)

*(noch keine weiteren — P5 wird vor ihrem Start in einer eigenen Browser-Planungssession
geschrieben; Konvention: ein Dokument pro Phase, kein Konzept+Plan+Handover-Trio. P1-, P2-, P3-
und P4-Pläne stehen oben bei ihrer jeweiligen Phase, nicht doppelt hier gelistet.)*

## Externe Referenz (nicht im Repo)

- `Notizheft_example.html` — 📕 UI-Vorlage aus dem Projektwissen. **Achtung:** enthält eine
  clientseitige Vault-Verschlüsselung, die mit Rahmenentscheidung R4 unvereinbar ist. Nur als
  Layout-/Interaktionsvorlage lesen, nicht als Architekturvorlage.
