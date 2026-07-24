---
status: live
purpose: L0 map of every project .md — one line each; start navigation here
read-when: locating any doc, or deciding whether a file is worth reading at all
detail: L0
up: ../CLAUDE.md
down: every project doc (that is the point)
updated: 2026-07-24
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

- [CLAUDE.md](../CLAUDE.md) — 📗 ~7KB · rules, core principle, hard rules, working style, current state; auto-loaded every session
- [AGENTS.md](../AGENTS.md) — 📗 ~1KB · harness-neutral entry point for non-Claude-Code agents; points to `CLAUDE.md` + doc-layers navigation
- [README.md](../README.md) — 📗 ~4KB · human overview + machine setup (venv, keyring, run, smoke test)
- [ROADMAP.md](../ROADMAP.md) — 📗 ~5KB · Phases 1–5, scope in/out per phase, status
- [docs/DOC_LAYERS_CONVENTION.md](./DOC_LAYERS_CONVENTION.md) — 📗 ~5KB · Doc-Layers-Spec (v1, 2026-07-06) · **byte-identische Kopie aus dem Trading-Bot-Repo — nicht projektspezifisch anpassen, sonst divergieren zwei Kopien derselben Regel**
- [docs/PROMPTS.md](./PROMPTS.md) — 📗 ~9KB · die drei Workflow-Prompts (Claude-Code-Session-Start, Phasen-Kickoff, Phasen-Abschluss); lesen beim Start eines neuen Chats, nicht mitten in einer Session

## Active phase (1 — Storage-Kern)

- [phase1_storage/CLAUDE.md](../phase1_storage/CLAUDE.md) — 🔄 ~10KB · phase head; Step 0 ✅, Steps 1–7 offen; read + newest Session-stopped block first
- [docs/concepts/phase1_storage_plan.md](./concepts/phase1_storage_plan.md) — 📕 ~13KB · ausführungsreifer P1-Plan (Entscheidungen A–H, Steps 0–7)
- [phase1_storage/SESSIONS_ARCHIVE.md](../phase1_storage/SESSIONS_ARCHIVE.md) — 📦 ~2KB · archivierte Session-stopped-Blöcke, verbatim, newest-first

## Concept docs (📕 snapshots — the plan a phase was built from)

*(noch keine weiteren — P2–P5 werden vor ihrem Start je in einer Browser-Planungssession
geschrieben; Konvention: ein Dokument pro Phase, kein Konzept+Plan+Handover-Trio)*

## Externe Referenz (nicht im Repo)

- `Notizheft_example.html` — 📕 UI-Vorlage aus dem Projektwissen. **Achtung:** enthält eine
  clientseitige Vault-Verschlüsselung, die mit Rahmenentscheidung R4 unvereinbar ist. Nur als
  Layout-/Interaktionsvorlage lesen, nicht als Architekturvorlage.
