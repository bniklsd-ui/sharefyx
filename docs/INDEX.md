---
status: live
purpose: L0 map of every project .md — one line each; start navigation here
read-when: locating any doc, or deciding whether a file is worth reading at all
detail: L0
up: ../CLAUDE.md
down: every project doc (that is the point)
updated: 2026-08-12 (P6 Step 5 gebaut -- SharePolicy/Surface ersetzt OwnSpaceWritable; Gate-A→B nur noch Punkt 3 offen)
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

- [CLAUDE.md](../CLAUDE.md) — 📗 ~17KB · rules, core principle, hard rules, working style, current state; auto-loaded every session — 2026-08-08 komprimiert (war ~41KB), P4/P5-Detailhistorie lebt jetzt nur noch in den jeweiligen Phase-Heads
- [AGENTS.md](../AGENTS.md) — 📗 ~1KB · harness-neutral entry point for non-Claude-Code agents; points to `CLAUDE.md` + doc-layers navigation
- [README.md](../README.md) — 📗 ~5KB · human overview + machine setup (venv, keyring, run, smoke test)
- [ROADMAP.md](../ROADMAP.md) — 📗 ~15KB · Phases 1–6, scope in/out per phase, status (P1–P5 ✅, P6 🔄 gestartet)
- [docs/DOC_LAYERS_CONVENTION.md](./DOC_LAYERS_CONVENTION.md) — 📗 ~5KB · Doc-Layers-Spec (v1, 2026-07-06) · **byte-identische Kopie aus dem Trading-Bot-Repo — nicht projektspezifisch anpassen, sonst divergieren zwei Kopien derselben Regel**
- [docs/PROMPTS.md](./PROMPTS.md) — 📗 ~15KB · die drei Workflow-Prompts (Claude-Code-Session-Start, Phasen-Kickoff im Browser, Phasen-Abschluss); **[2026-08-09]** Phasen-Abschluss läuft jetzt in Claude Code statt Browser+Google-Drive (Nikinger-Entscheidung, Effizienz); lesen beim Start eines neuen Chats, nicht mitten in einer Session

## Active phase (6 — Freigaben, Ordner, Werkzeug-Ergonomie)

- [phase6_shares/CLAUDE.md](../phase6_shares/CLAUDE.md) — 🔄 ~21KB · phase head; **Block A (Steps 0–3) vollständig gebaut** (Werkzeuge/Betrieb/Update-Banner — Details im Archiv, siehe unten), **GATE A→B nur noch Punkt 3 offen** (Purge-Zeilenrückgang, frühestens 2026-08-28); Step 4 (Storage-Fundament, Block B) **✅ gebaut** (2026-08-12, jetzt im Archiv); **[2026-08-12] Step 5 (Rechtepolitik, Block B: `SharePolicy`/`Surface` ersetzt `OwnSpaceWritable`, item-level ACL in `tools.py`/`webui/api.py`, Fail-Closed-Folder-Move [Nikinger-Entscheidung]) ✅ gebaut** — 12 Pflichttests + 1 Ergänzung grün, 691 Tests gesamt, `mcp_smoke.py`/`ui_smoke.py`/`ui_budget.py` real grün; Kopf am selben Tag unter Softcap rotiert (Step 4 → Archiv); read + newest Session-stopped block first
- [phase6_shares/SESSIONS_ARCHIVE.md](../phase6_shares/SESSIONS_ARCHIVE.md) — 📦 ~50KB · drei Einträge, newest-first: Step 4 (Storage-Fundament, 2026-08-12-Rotation) + Steps 1–3 (Werkzeug-Ergonomie, Betrieb, Update-Log/Banner, 2026-08-12-Rotation) + Steps 0–2-Kurzfassung (2026-08-10-Rotation), alle verbatim aus `phase6_shares/CLAUDE.md`
- [docs/concepts/phase6_shares_plan.md](./concepts/phase6_shares_plan.md) — 📕 ~58KB · ausführungsreifer P6-Plan: Entscheidungen P6-A–P6-AC, Steps 0–10 (Block A Werkzeuge/Betrieb, Block B Dateisystem, Block C Bilder, hartes Gate A→B), Rechtemodell §1.2, Abnahmematrix 1–24, [VERIFY]-Register V39–V51; über 40KB, aber als 📕-Snapshot vom Softcap ausgenommen; Autor Browser-Planungssession 2026-08-09 gegen den Drive-Snapshot `2026_08_09_sharefyx-main`
- [docs/UPDATE_LOG.md](./UPDATE_LOG.md) — 📗 <1KB · menschenlesbarer Änderungs-Log fürs Update-Banner in `/ui` (P6 Step 3, Plan §1.8/§2.4); streng geparst von `webui/updates.py :: parse_update_log()` (`## <ISO-Datum>` beginnt einen Eintrag, `- ` eine Zeile); neue Einträge werden **oben** eingefügt (Changelog-Konvention, oberster Eintrag = neuester); `deploy.sh` bricht ohne einen heute datierten obersten Eintrag ab (P6-X); erster Eintrag (2026-08-09) kündigt die künftige Sichtbarkeitsumstellung an

## Completed phases

- [phase5_ui/CLAUDE.md](../phase5_ui/CLAUDE.md) — 📗 ~34KB · phase head; Steps 0–8b ✅ (Block A Sicherheit/Selbstverwaltung + Block B REST-API/UI, hartes Gate dazwischen, beide durchlaufen) — **20/20 Abnahmezeilen live bestanden, Phase 5 ✅** (2026-08-09); enthält die vollständige Abnahmematrix, Modul-Status je Step und die Live-Debugging-Historie (Origin/CSRF-Fund am Block-A-Gate, Step-7b-Revision von Plan §4.1/§4.3, Sicherheitsbefund S9); **[2026-08-09, P6 Step 3]** Update-Log-Banner (`webui/{updates,api,config}.py`, `deploy.sh`-Gate) — Details `phase6_shares/CLAUDE.md`; read + newest Session-stopped block first
- [docs/concepts/PHASE5_CLOSEOUT_HANDOVER.md](./concepts/PHASE5_CLOSEOUT_HANDOVER.md) — 📕 ~18KB · Abschluss-Handover P5→P6: Status, Delta seit dem P4-Handover, offene Entscheidungen §4.1–§4.6 (F1/F2, `patch_item`, Client-Surface-Logging, O2), [VERIFY]-Bilanz V27–V38
- [docs/concepts/phase5_ui_uebersicht.svg](./concepts/phase5_ui_uebersicht.svg) — 📕 Übersichtsgrafik Phase 5 (Cookie-Session vs. Bearer-Trennung, Konvergenz auf denselben Storage-Kern)
- [docs/concepts/P5_ABNAHME_2026-08-09.md](./concepts/P5_ABNAHME_2026-08-09.md) — 📕 ~11KB · Abnahmeprotokoll Phase 5: **20/20 live bestanden**, Kurzbeleg für Zeile 20 (Reboot), Befunde-Übersicht (Origin-Fund, S9/S10-Nebenfund, F1/F2, `patch_item`-Feedback), Runbook-Schritt 4 (`auth-users`-Credential/Keyring) bereits erledigt vorgefunden
- [docs/concepts/phase5_ui_plan.md](./concepts/phase5_ui_plan.md) — 📕 ~80KB · ausführungsreifer P5-Plan: Entscheidungen P5-A–P5-AE, Steps 0–9 (Block A Sicherheit/Selbstverwaltung, Block B REST-API/UI), Designsystem (§4.1/§4.3 in Step 7b revidiert, Snapshot bleibt unverändert), Abnahmematrix 1–20, [VERIFY]-Register V27–V38; über 40KB, aber als 📕-Snapshot vom Softcap ausgenommen
- [phase5_ui/SESSIONS_ARCHIVE.md](../phase5_ui/SESSIONS_ARCHIVE.md) — 📦 ~159KB · dreizehn archivierte Session-Blöcke (Step 0–4 inkl. Block-A-Gate/Origin-Fund, Block-A-Gate-Live-Lauf, Step 6, Step 7, Step 7b, Step 8, Step 8b, Verifikationssession/Zeilen-10-19-Nachträge), verbatim
- [phase4_auth/CLAUDE.md](../phase4_auth/CLAUDE.md) — 📗 ~33KB · phase head; Steps 0–7 ✅ (alle acht Steps, Schnitt vollzogen, `TokenPathASGI` entfernt) — **16/16 Abnahmezeilen live bestanden, Phase 4 ✅** (2026-07-30); Steps-0–6a-Detailnarrative 2026-07-31 nach `SESSIONS_ARCHIVE.md` komprimiert, unter dem 40KB-Softcap; enthält die Kurztabelle der Sicherheitsbefunde **S1–S10 / O1–O2** (S10 neu, 2026-08-06 — ein Reset über eine Einladung widerrief weder Token-Familien noch Sitzungen; O2 geschlossen im Code 2026-08-09, P6 Step 2 — `purge_expired()` räumt `token_families`/`clients` jetzt ab); das ausgeführte Inbetriebnahme-Runbook zog am 2026-08-06 verbatim ins Archiv (Softcap); **[2026-08-06, P5 Step 8b]** OAuth-Consent-Seite (`authserver/templates.py`/`routes.py`) gestaltet, kein Sicherheitsbefund; **[2026-08-09, P6 Step 3]** Schema 3 (`users.seen_update_id`, additive `ALTER TABLE`) — Details `phase6_shares/CLAUDE.md`; read + newest Session-stopped block first
- [docs/concepts/PHASE4_CLOSEOUT_HANDOVER.md](./concepts/PHASE4_CLOSEOUT_HANDOVER.md) — 📕 ~18KB · Abschluss-Handover P4→P5: Status, Delta seit dem P3-Handover, offene Entscheidungen für die Web-UI-Planung §4.1–§4.5, [VERIFY]-Bilanz V14–V26
- [docs/concepts/phase4_auth_uebersicht.svg](./concepts/phase4_auth_uebersicht.svg) — 📕 Übersichtsgrafik Phase 4 (Auth-Fluss, Komponenten)
- [docs/concepts/P4_ABNAHME_2026-07-29.md](./concepts/P4_ABNAHME_2026-07-29.md) — 📕 ~24KB · Abnahmeprotokoll Phase 4: **16/16 live bestanden** (drei Nachträge 2026-07-30: Zeilen 14/15, Zeile 9, Schnitt+Zeile 16), CLI-Ausschnitt + DB-Gegenprobe als Beleg, Befunde B1–B3 (alle klein, zwei behoben)
- [docs/concepts/P4_SECURITY_REVIEW_2026-07-29.md](./concepts/P4_SECURITY_REVIEW_2026-07-29.md) — 📕 ~13KB · Sicherheits-Review P3+P4 vor der Live-Abnahme: Befund S1 (behoben) plus **S2–S8 in P5 Step 1 geschlossen** (`phase4_auth/CLAUDE.md`s Tabelle, Status-Nachtrag 2026-08-02) und Betriebsnotiz O1 (weiterhin offen), **und** 15 ausdrücklich geprüfte, in Ordnung befundene Punkte (verified negatives) — der Snapshot selbst bleibt unverändert (📕), der aktuelle Status steht im Phase-Head
- [docs/concepts/phase4_auth_plan.md](./concepts/phase4_auth_plan.md) — 📕 ~76KB · ausführungsreifer P4-Plan (Entscheidungen P4-A–P4-R, Steps 0–7, eigener Authorization Server, Argon2id + TOTP, opake Token); über 40KB, aber als 📕-Snapshot vom Softcap ausgenommen; Autor Browser-Planungssession 2026-07-28, **ohne frischen Repo-Zugriff geschrieben** — Anker sind Funktionsnamen/Suchstrings, keine Zeilennummern
- [phase4_auth/SESSIONS_ARCHIVE.md](../phase4_auth/SESSIONS_ARCHIVE.md) — 📦 ~82KB · das ausgeführte Inbetriebnahme-Runbook (Step 7, 2026-08-06 verbatim aus dem Head verschoben) plus neun archivierte Session-Blöcke (Step 0+1+2, Step 3, V14+Step 4, Step 5, Step 6a, Step 6b, Step-7-Code-Vorbereitung, Befund S1+Sicherheits-Review+12/16-Abnahme, CSP-Fix+Zeilen 14/15+Zeile 9/15/16) plus die komprimierte Steps-0–6a-Detailnarrative (2026-07-31, keine Session-Rotation, eigener Abschnitt), verbatim, newest-first
- [phase3_edge/CLAUDE.md](../phase3_edge/CLAUDE.md) — 📗 ~21KB · phase head; alle 8 Steps ✅ — **13/13 Abnahmezeilen live bestanden, Phase 3 ✅** (Zeile 13/Restore-Nachweis am 2026-08-02 vom Nikinger selbst bestätigt); **[P4 Step 7]** MCP-Unit liegt in `phase4_auth/systemd/`; read + newest Session-stopped block first
- [docs/concepts/phase3_edge_plan.md](./concepts/phase3_edge_plan.md) — 📕 ~46KB · ausführungsreifer P3-Plan (Entscheidungen P3-A–P3-N, Steps 0–7); über 40KB, aber als 📕-Snapshot vom Softcap ausgenommen
- [phase3_edge/SESSIONS_ARCHIVE.md](../phase3_edge/SESSIONS_ARCHIVE.md) — 📦 ~55KB · elf archivierte Session-Blöcke (Step 0–6, inkl. Live-Abnahme-Funde B3/B4, beide Live-Abnahme-Sessions vom 2026-07-27, Token-Rotation-Session vom 2026-07-28, Zeile-6-Reboot-Session vom 2026-07-29), verbatim, newest-first
- [docs/concepts/P3_ABNAHME_2026-07-27.md](./concepts/P3_ABNAHME_2026-07-27.md) — 📕 ~19KB · Abnahmeprotokoll Phase 3: 10/13 live bestanden, Zeilen 6/12/13 per Nikinger-Entscheidung auf nächste Phase verschoben, CLI-Ausschnitt als Beleg, Befunde B5/B6
- [docs/concepts/PHASE3_CLOSEOUT_HANDOVER.md](./concepts/PHASE3_CLOSEOUT_HANDOVER.md) — 📕 ~17KB · Abschluss-Handover P3→P4: Status, Delta seit dem P2-Handover, [VERIFY]-Bilanz V1–V13, geerbte Abnahmezeilen 6/12/13, Doku-Drift-Liste aus der Autocompact-Session inkl. Nachträgen zum nikinger-Token-Fund, offene Entscheidungen für die OAuth-Planung
- [docs/concepts/phase3_edge_uebersicht.svg](./concepts/phase3_edge_uebersicht.svg) — 📕 Übersichtsgrafik Phase 3 (Request-Weg, Komponenten)
- [phase2_mcp/CLAUDE.md](../phase2_mcp/CLAUDE.md) — 📗 ~24KB · phase head; Steps 0–7 ✅, **live-verifiziert** (Quick-Tunnel-Probe + Adapter-Abnahme durch den Nikinger, 2026-07-26); Quick-Tunnel-Runbook seit P3 Step 6 durch Verweis ersetzt; **[2026-08-03]** `create_app()` mountet jetzt auch `webui`-Routen (P5 Step 4 Nachtrag, siehe `phase5_ui/CLAUDE.md`); **[2026-08-09, P6 Step 1]** siebtes Tool `patch_item` + Quittungen statt Volltext; **[P6 Step 2]** `ua`-Feld (Client-Surface-Logging, V42 geschlossen 2026-08-12 — unterscheidet nicht zwischen Oberflächen); **[P6 Step 3]** `create_app()` reicht `oauth.store` an `api_routes()` durch (dokumentierte Ein-Zeilen-Abweichung, kein neuer Test hier); 95 Tests; read + newest Session-stopped block first
- [docs/concepts/phase2_mcp_plan.md](./concepts/phase2_mcp_plan.md) — 📕 ~46KB · ausführungsreifer P2-Plan (Entscheidungen P2-A–P2-N, Steps 0–7); über 40KB, aber als 📕-Snapshot vom Softcap ausgenommen
- [docs/concepts/P2_ADAPTER_ABNAHME_2026-07-26.md](./concepts/P2_ADAPTER_ABNAHME_2026-07-26.md) — 📕 ~11KB · Abnahmeprotokoll über den echten Custom Connector, 21/21 Prüfungen, beide Befunde behoben (B1, B2 — siehe Nachtrag)
- [phase2_mcp/SESSIONS_ARCHIVE.md](../phase2_mcp/SESSIONS_ARCHIVE.md) — 📦 ~38KB · acht archivierte Session-Blöcke (Step 0–7), verbatim, newest-first
- [docs/concepts/PHASE2_CLOSEOUT_HANDOVER.md](./concepts/PHASE2_CLOSEOUT_HANDOVER.md) — 📕 ~11KB · Abschluss-Handover P2→P3: Status, Delta seit dem P1-Handover, offene Entscheidungen für die Exposure-Phase, [VERIFY]-Bilanz V1–V9
- [phase1_storage/CLAUDE.md](../phase1_storage/CLAUDE.md) — 📗 ~12KB · phase head; alle acht Module ✅, live-verifiziert gegen den echten DATA_ROOT (2026-07-25); Frontmatter-Schema + `Store`-Signaturen Contract für P2; **[2026-08-09, P6 Step 1]** dritte, benannte Contract-Öffnung — `store.py :: patch()` + `patch.py` (neu), 81 Tests
- [docs/concepts/phase1_storage_plan.md](./concepts/phase1_storage_plan.md) — 📕 ~15KB · ausführungsreifer P1-Plan (Entscheidungen A–H, Steps 0–7)
- [phase1_storage/SESSIONS_ARCHIVE.md](../phase1_storage/SESSIONS_ARCHIVE.md) — 📦 ~27KB · archivierte Session-stopped-Blöcke, verbatim, newest-first
- [docs/concepts/PHASE1_CLOSEOUT_HANDOVER.md](./concepts/PHASE1_CLOSEOUT_HANDOVER.md) — 📕 ~12KB · Abschluss-Handover P1→P2: Status, Delta, Contract, offene Entscheidungen D1–D6, `[VERIFY]`-Bilanz

## Concept docs (📕 snapshots — the plan a phase was built from)

*(keine eigenen Einträge hier — Konvention: ein Dokument pro Phase, kein
Konzept+Plan+Handover-Trio. P1- bis P5-Pläne stehen oben bei ihrer jeweiligen Phase, nicht
doppelt hier gelistet.)*

## Referenzmaterial (nicht Teil des Plan/Konzept/Handover-Trios)

- [docs/concepts/notiz_heft_example.html](./concepts/notiz_heft_example.html) — 📕 UI-Vorlage,
  vom Nikinger in P5 Step 7 ins Repo gelegt (vorher nur im Projektwissen, für Claude Code nicht
  zugänglich). **Achtung:** enthält eine clientseitige Vault-Verschlüsselung, die mit
  Rahmenentscheidung R4 unvereinbar ist. Nur als Layout-/Interaktionsvorlage lesen, nicht als
  Architekturvorlage — P5-V dokumentiert genau, was daraus geerntet wurde und was bewusst nicht
  (`phase5_ui/CLAUDE.md`, Step-7-Session-Block).
