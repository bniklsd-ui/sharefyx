---
status: live
purpose: Archiv älterer Session-stopped-Blöcke aus phase1_storage/CLAUDE.md, newest-first, verbatim
read-when: Audit vergangener Sessions dieser Phase; NICHT für normalen Session-Start
detail: L3
up: CLAUDE.md
updated: 2026-07-24
---
# Session-Archiv — Phase 1 Storage-Kern

## Session stopped — 2026-07-24 (Planung abgeschlossen, Bau noch nicht gestartet)

**Ergebnis:** Die initialen Projektdokumente wurden in einer Browser-Planungssession erstellt
(Root-`CLAUDE.md`, `AGENTS.md`, `README.md`, `ROADMAP.md`, `docs/INDEX.md`, dieser Phase-Head,
`docs/concepts/phase1_storage_plan.md`). Rahmenentscheidungen R1–R6 sind in der Root-`CLAUDE.md`
gelockt, die Phase-1-Entscheidungen A–H im Plan. **Es existiert noch kein Code und kein Repo.**

**Nächster Schritt (konkret):** In Claude Code Step 0 des Plans ausführen — Repo initialisieren,
diese Dokumente als ersten Commit einchecken, `pyproject.toml` mit Paket `storage` nested als
`phase1_storage/storage/` anlegen, `scripts/dev_install.sh` schreiben, `pytest` grün mit null
Tests. Danach Step 1.

**Vor dem Start zu erledigen (Blocker für Step 0):**
1. ~~`docs/DOC_LAYERS_CONVENTION.md` kopieren~~ → **erledigt 2026-07-24**, byte-identisch
   übernommen, Index-Zeile gesetzt.
2. **`DATA_ROOT`-Pfad festlegen** (konkreter Pfad auf der VM). Die Dateisystemfrage ist
   beantwortet: VMware-VM mit Ubuntu, lokale virtuelle Platte → **ext4**, `flock` verlässlich
   (Plan §3.2, `[VERIFY]` aufgelöst). Offen bleibt nur, *welches* Verzeichnis es wird — und die
   Zusage, es nicht auf einen Shared Folder oder ein Backup-Share zu legen.

**Offene `[VERIFY]` in diesem Track:** Round-Trip-Treue von `python-frontmatter` (Plan Step 1) ·
Namenskollision `IndexError_` (Plan §1) · Methode zur Dateisystem-Ermittlung unter Ubuntu
(Plan Step 3) · Snippet-/Listing-Größenziel 3 KB (Plan Step 6).
**Aufgelöst:** `flock` auf dem Ziel-Dateisystem (ext4 bestätigt, 2026-07-24).

**Ehrlich geflaggt:** Dieser Plan wurde **ohne** Repo geschrieben — es gibt nichts, wogegen die
Contracts verifiziert werden konnten. Jede Signatur hier ist ein Vorschlag der Planung, kein
verifizierter Repo-Stand. Abweichungen beim Bau sind erwartbar und gehören als datierte
Korrekturnotiz in dieses Dokument, nicht in einen stillen Fix.
