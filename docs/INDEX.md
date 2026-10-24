---
status: live
purpose: L0 map of every project .md — one line each; start navigation here
read-when: locating any doc, or deciding whether a file is worth reading at all
detail: L0
up: ../CLAUDE.md
down: every project doc (that is the point)
updated: 2026-10-24 (B11.4: V211 gemessen; zwei neue L3-Archive) | 2026-10-24 (Block 10.5: die Probe ist grün — P10.5-45/46/47/48 ✅; Größen von Phase-Head und Archiven nachgezogen, `FREIGABEN_ARCHIVE.md` neu) | ältere Einträge: docs/INDEX_UPDATES_ARCHIVE.md
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
> **Ausnahmen** (vier Stellen, korrekt so): Harness-Dateien · Test-Fixtures (Card bräche
> den Byte-Vergleich) · maschinell geparste Dateien (z. B. `docs/UPDATE_LOG.md`) ·
> Vendor-/Lizenztext. Details: Plan §1.3.
>
> Glyphs: 🔄 active-phase · 🟡 code-complete, nicht live-bewiesen (Phasenstatus, wie in `ROADMAP.md`) ·
> 📗 live (maintained) · 📕 snapshot (dated, **never edit**) · 📦 archive (verbatim history).
> Für die Oversize-Regel oben zählt 🟡 wie 📗/🔄: ein 🟡-Dokument darf den Softcap nicht reißen.

## Root & governance

- [docs/INDEX.md](./INDEX.md) — 🔗 **diese Karte** (L0) · **37.885 B — unter dem 40-KiB-Softcap** (V145 ✅) · die Karten-Chronik steht in `docs/INDEX_ENTRIES_ARCHIVE.md` · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**
- [CLAUDE.md](../CLAUDE.md) — 📗 **40085 B** (vor der Rotation 114.771 B) · Wurzel-Regelwerk: Kernprinzip der dumme Server, **neun Hard Rules** (1 keine Secrets in Dateien · 3 kein Write ohne `version` · 4 Schreibrechte folgen der Mitgliedschaft · 6 nie ein offener Port · 8 Commit ⇒ Doc-Update · 9 nie `pkill -f`, nie den systemd-Dienst), Working style, Doku-Hygiene und **Current state** (Session-Bloecke, newest-first, **kein** Ein-Block-Limit — P9-A). **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**
- [README.md](../README.md) — 📗 ~7KB · human overview + machine setup (venv, keyring, run, smoke test); **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**
- [ROADMAP.md](../ROADMAP.md) — 📗 **37.197 B** · Phasen 1–10.5, Scope in/out je Phase, Status · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**
- [docs/ROADMAP_UPDATES_ARCHIVE.md](./ROADMAP_UPDATES_ARCHIVE.md) — 📦 **14.371 B** · L3: `updated:`-Kette von `ROADMAP.md`, verbatim (2026-10-07)
- [docs/DOC_LAYERS_CONVENTION.md](./DOC_LAYERS_CONVENTION.md) — 📗 ~5KB · Doc-Layers-Spec (v1, 2026-07-06) · **byte-identische Kopie aus dem Trading-Bot-Repo — nicht projektspezifisch anpassen, sonst divergieren zwei Kopien derselben Regel**
- [docs/concepts/sichtpruefung_automation_conventions.md](./concepts/sichtpruefung_automation_conventions.md) — 📗 **21.765 B** · Konventionen der Sichtprüfungs-Automatisierung · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**
- [docs/concepts/sichtpruefung_automation_tooling.md](./concepts/sichtpruefung_automation_tooling.md) — 📗 ~26KB · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**
- [docs/PROMPTS.md](./PROMPTS.md) — 📗 ~20KB · die drei Workflow-Prompts (Claude-Code-Session-Start, Phasen-Kickoff — seit P9 in Claude Code, Phasen-Abschluss); **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**

## Phase 10 — ✅ abgeschlossen 2026-10-20 (Bestandsaufnahme, kein Produktcode; Plan P10.5)

- [phase10_inventory/CLAUDE.md](../phase10_inventory/CLAUDE.md) — 📗 ~8KB · Phase-10-Head: Modulstatus Steps 0–4/Z (✅; Step 4 = Plan P10.5, 2026-10-21), ein Session-Block (Planungschat)
- [phase10_inventory/SESSIONS_ARCHIVE.md](../phase10_inventory/SESSIONS_ARCHIVE.md) — 📦 ~27KB · ältere Session-Blöcke, verbatim
- [phase10_inventory/BAUSTELLENREGISTER.md](../phase10_inventory/BAUSTELLENREGISTER.md) — 📗 **30.822 B** (10.138 B Luft) — 76 Baustellen; die Arbeitsliste für P10.5 (Tor P10-8 offen) · die **geschlossenen** Zeilen zeigen auf `REGISTER_ARCHIVE.md`
- [phase10_inventory/REGISTER_ARCHIVE.md](../phase10_inventory/REGISTER_ARCHIVE.md) — 📦 **17.549 B** · die **geschlossenen** Registerzeilen (26), verbatim (2026-10-24 gewandert)
- [phase10_inventory/ENTSCHEIDUNGEN_ARCHIVE.md](../phase10_inventory/ENTSCHEIDUNGEN_ARCHIVE.md) — 📦 **5.615 B** · L3-Archiv der Entscheidungsliste D-1–D-18 des Phase-10-Registers — jede Frage, ihre Empfehlung und die Antwort des Nikingers, verbatim; am 2026-10-22 aus dem Register gewandert (P10.5 Block 0, Schritt 0.8)
- [phase10_inventory/UPDATES_ARCHIVE.md](../phase10_inventory/UPDATES_ARCHIVE.md) — 📦 **4.509 B** · L3-Archiv der `updated:`-Fäden des Phase-10-Registers, verbatim — am 2026-10-24 rotiert, weil das Register an der Grenze stand
- [phase10_inventory/messung/M1_browser.md](../phase10_inventory/messung/M1_browser.md) — 📗 ~13KB · M1: Browser-Messung (Firefox/Safari, Funnel/Domain): `/overview` 4,8–5,2 s auf allen Wegen, Stau hinter `overview`; D-3-Ziele Z1–Z4 (> 200 ms Ladeanimation)
- [phase10_inventory/messung/M7_editor.md](../phase10_inventory/messung/M7_editor.md) — 📗 ~5KB · M7: Editor-Bibliothek ohne Build-Schritt — CM5 65,6 KB gz + Roundtrip 10/10 + 239 KB im Korridor ✅, EasyMDE 282 KB ❌ (V201), markdown-it redundant; füttert ED-1
- [docs/concepts/phase10_inventory_plan.md](./concepts/phase10_inventory_plan.md) — 📕 ~26KB · Plan P10 gegen `main@0a7aaf4`: Locks P10-A–K, M1–M8, Abnahme P10-1–12, V195–V206, P10.5-Schnitt §7, Closeout §8
- [docs/concepts/phase10_executor_review_glm.md](./concepts/phase10_executor_review_glm.md) — 📗 ~14KB · Auswertung P10-K-Open-Test (GLM via opencode): Kontingent-Treiber, Qualität Q1–Q6, Claude Code + GLM, §5 Entscheidung: GLM verworfen, Marktblick ~2026-11-10
- [docs/concepts/phase10_intake.md](./concepts/phase10_intake.md) — 📗 ~28KB · Sammelstelle, Herkunft des Registers: Wünsche 2026-10-08/-16, Erbe P9, Fleet-Notizen §5–§7, Notes **an** Fleet §8 (GLM verworfen) und §9 (P10.5: Kontextgrenze 400 K)
- [docs/concepts/phase10_karte_c_stil_1.svg](./concepts/phase10_karte_c_stil_1.svg) — 📕 Karten-Entwürfe: `phase10_karte_entwurf_{a,b,c}.svg` (erste Runde, Wahl C) und `phase10_karte_c_stil_{1,2,3}.svg` (Stile der Gehirnkarte, gewählt C2); `phase10_logo_entwuerfe{,_c,_mix,_final}.svg` (Logo D-6, vier Runden)
- [docs/concepts/PHASE10_CLOSEOUT_HANDOVER.md](./concepts/PHASE10_CLOSEOUT_HANDOVER.md) — 📕 ~14KB · Abschluss-Handover P10 → P10.5: Planungsdossier (Step 4 + Tor wandern), offene Entscheidungen, [VERIFY]-Bilanz
- [docs/concepts/phase10_5_finishing_plan.md](./concepts/phase10_5_finishing_plan.md) — 📕 ~93KB · Plan P10.5 gegen `main@e5a1879`, freigegeben 2026-10-21: Locks P10.5-A–W, Blöcke 0–12/Z, Deploys A–D, Abnahme P10.5-1–61, V207–V219
- [docs/concepts/phase10_inventory_uebersicht.svg](./concepts/phase10_inventory_uebersicht.svg) — 📕 ~16KB · Phase-10-Übersichtsgrafik 1080×1080 (Closeout 2026-10-20, gerendert und angesehen)

## Phase 10.5 — 🔄 in Arbeit (Finishing — alle Baustellen schließen; Plan `docs/concepts/phase10_5_finishing_plan.md`, Ausführer M3.1 Flash als Open-Test)

- [phase10_5_finishing/CLAUDE.md](../phase10_5_finishing/CLAUDE.md) — 📗 **36.972 B** · Phase-10.5-Head: Modulstatus der Blöcke 0–12/Z, Deploy-Tabelle A–D, Abnahmestand P10.5-1–61 (42 ✅ · 0 ⚠️ · 19 ⬜), offene Punkte beim Nikinger, ein Session-Block (≤ 4 KiB, DO-3)
- [phase10_5_finishing/SESSIONS_ARCHIVE.md](../phase10_5_finishing/SESSIONS_ARCHIVE.md) — 📦 **90673 B** · L3-Archiv der älteren Session-Blöcke dieser Phase, verbatim, newest-first
- [phase10_5_finishing/STARTUPTRAG_ARCHIVE.md](../phase10_5_finishing/STARTUPTRAG_ARCHIVE.md) — 📦 **14291 B** · L3-Archiv der **Startaufträge von Block 7 und Block 9** (verbatim verschoben 2026-10-23 bzw. 2026-10-24) — Schritte 7.4–7.7 und die Ankündigung der drei P1-Öffnungen



- [phase10_5_finishing/FREIGABEN_ARCHIVE.md](../phase10_5_finishing/FREIGABEN_ARCHIVE.md) — 📦 **3.577 B** · die Freigaben der Phase 10.5, verbatim aus dem Head verschoben
- [phase10_5_finishing/MODULSTATUS_ARCHIVE.md](../phase10_5_finishing/MODULSTATUS_ARCHIVE.md) — 📦 **8.581 B** · die **ausführlichen** Statusspalten der Blöcke 0–10 (11), verbatim (2026-10-24 gewandert)
- [phase10_5_finishing/UPDATES_ARCHIVE.md](../phase10_5_finishing/UPDATES_ARCHIVE.md) — 📦 **11465 B** · L3-Archiv der älteren `updated:`-Fäden des Phase-10.5-Heads, verbatim, newest-first (rotiert 2026-10-23 mit `scripts/rotate_index_updates.sh`, wie beim Phase-9-Head)

## Phase 8.6 — ✅ abgeschlossen 2026-09-19 (UI-Politur, live `v3.0.2`; zwei Pläne)

- [phase8_6_ui_polish/CLAUDE.md](../phase8_6_ui_polish/CLAUDE.md) — 📗 ~106KB · Phase-Head, **ab jetzt Archiv**. Modul-Status Step 0/V/A/B/C/D/E/F/G/G-R/H/H-R/H-R-3/J/Gate/**Z** alle ✅, Baselines, §Vormerkungen (Domain-Kandidat, Tailscaled-Watchdog, INDEX-Rotation, Sichtpruefungs-Realitaet vs. Chat-Beschreibung) und **ein** Session-Block (2026-09-19, Step Z). Ueber dem 40-KB-Softcap — benannt statt versteckt (P8-P)
- [phase8_6_ui_polish/SESSIONS_ARCHIVE.md](../phase8_6_ui_polish/SESSIONS_ARCHIVE.md) — 📦 ~234KB · volle Phasenhistorie verbatim, newest-first; jede Rotation per `scripts/rotate_session_block.sh`. Enthaelt den **Wortlaut der neun UX-Befunde** (Block 2026-09-12) und das Gate-Protokoll (2026-09-18)
- [docs/concepts/phase8_6_ui_polish_plan.md](./concepts/phase8_6_ui_polish_plan.md) — 📕 ~84KB · **Plan 1** gegen `main@d1af51b`. Locks P8.6-A–U, Abnahme 1–32, `[VERIFY]` V106–V119. §9 traegt nur eine **Zeiger-Zeile** auf Plan 2 §9 (P8.6-W) — die einzige Aenderung am Snapshot
- [docs/concepts/phase8_6_ui_polish_plan2.md](./concepts/phase8_6_ui_polish_plan2.md) — 📕 ~87KB · **Plan 2** gegen `main@26a7cc9`, arbeitet die neun Befunde ab. Locks P8.6-W–AL, Abnahme 33–54, `[VERIFY]` V123–V139. **§9 ist der kanonische Closeout der Phase** — Status, Delta ueber beide Plaene, Abnahmematrix Zeile fuer Zeile mit Beleg, Restdefekte, `[VERIFY]`-Bilanz V97/V103–V144, §9.5 „was die Phase ueber ihre eigene Doku gelernt hat"
- [docs/concepts/phase8_6_ui_polish_block_g_r_plan.md](./concepts/phase8_6_ui_polish_block_g_r_plan.md) — 🟢 ~17KB · Mini-Plan Revision 1 (Breakpoints 1200/1024, Layer-Ton, Editor-Head sticky)
- [docs/concepts/phase8_6_ui_polish_block_h_r_plan.md](./concepts/phase8_6_ui_polish_block_h_r_plan.md) — 🟢 ~28KB · Mini-Plan Revision 2 (OLED-BLACK, `.account-nav`-Akzent, CDP-Proben V142/V143/V144 — zwei davon: **kein Fix noetig**)
- [docs/concepts/phase8_6_ui_polish_block_h_r_3_escalation.md](./concepts/phase8_6_ui_polish_block_h_r_3_escalation.md) — 🟢 ~14KB · Eskalations-Report Revision 3 (Locks H-R.6/.7/.8; kein JS-/HTML-Touch — `dataset.view` gab es seit Block G ohne CSS-Konsument)
- [docs/concepts/PHASE8_6_CLOSEOUT_HANDOVER.md](./concepts/PHASE8_6_CLOSEOUT_HANDOVER.md) — 📕 ~30KB · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**
- [docs/concepts/phase8_6_ui_polish_uebersicht.svg](./concepts/phase8_6_ui_polish_uebersicht.svg) — 📕 ~17KB · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**

## Phase 8.5 — ✅ abgeschlossen 2026-09-09 (Link-Picker-Politur, live `v3.0.2`)

- [phase8_5_picker_release/CLAUDE.md](../phase8_5_picker_release/CLAUDE.md) — 📗 ~26KB · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**
- [phase8_5_picker_release/SESSIONS_ARCHIVE.md](../phase8_5_picker_release/SESSIONS_ARCHIVE.md) — 📦 ~200KB · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**
- [phase8_5_picker_release/SICHTPRUEFUNG_RESTBLOCK.md](../phase8_5_picker_release/SICHTPRUEFUNG_RESTBLOCK.md) — 📗 ~28KB
- [phase8_5_picker_release/SICHTPRUEFUNG_WALKTHROUGH.md](../phase8_5_picker_release/SICHTPRUEFUNG_WALKTHROUGH.md) — 📗 ~29KB · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**
- [phase8_5_picker_release/CLUSTER3_TESTBLOCK.md](../phase8_5_picker_release/CLUSTER3_TESTBLOCK.md) — 📗 ~17KB · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**
- [docs/concepts/phase8_5_picker_release_plan.md](./concepts/phase8_5_picker_release_plan.md) — 📕 ~57KB · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**
- [docs/concepts/PHASE8_5_CLOSEOUT_HANDOVER.md](./concepts/PHASE8_5_CLOSEOUT_HANDOVER.md) — 📕 ~18KB · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**
- [docs/concepts/phase8_5_picker_release_uebersicht.svg](./concepts/phase8_5_picker_release_uebersicht.svg) — 📕 ~16KB · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**
## Phase 9 — ✅ abgeschlossen 2026-10-08 (Härtung: acht Steps + sieben Blöcke, live `v3.1.4`)

- [phase9_hardening/CLAUDE.md](../phase9_hardening/CLAUDE.md) — 📗 **33.001 B** · Phase-9-Head (abgeschlossen 2026-10-08): Modulstatus-Kurzstand, Backlog, ein Session-Block (Closeout); ausführlicher Modulstatus in `MODULE_STATUS_ARCHIVE.md` · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**
- [phase9_hardening/ABNAHME_MATRIX.md](../phase9_hardening/ABNAHME_MATRIX.md) — 📗 **21.216 B** · **Hub** der Abnahmematrix: Stand, Statusregel, Bilanz-Überschrift; die Zeilen stehen seit 2026-10-07 in drei lebenden Teilen (Oversize-Fix, `scripts/move_sections.py`) · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**
- [phase9_hardening/ABNAHME_MATRIX_STEPS.md](../phase9_hardening/ABNAHME_MATRIX_STEPS.md) — 📗 **31.990 B** · Matrix-Teil: Step 0–H und Phasenweit (P9-1 – P9-58)
- [phase9_hardening/ABNAHME_MATRIX_BLOECKE.md](../phase9_hardening/ABNAHME_MATRIX_BLOECKE.md) — 📗 **37.185 B** · Matrix-Teil: Blöcke doing/trace/settings und die drei Bildsichtungen (P9-59 – P9-120)
- [phase9_hardening/ABNAHME_MATRIX_FEEDBACK.md](../phase9_hardening/ABNAHME_MATRIX_FEEDBACK.md) — 📗 **17.422 B** · Matrix-Teil: Block feedback (P9-121 – P9-137), seit 2026-10-08
- [phase9_hardening/ABNAHME_MATRIX_VERIFY.md](../phase9_hardening/ABNAHME_MATRIX_VERIFY.md) — 📗 **20.860 B** · Matrix-Teil: `[VERIFY]` je Eintrag (V145 – V194), Zählregel, `[VERIFY]`-Bilanz
- [phase9_hardening/step_a/RUNBOOK_STEP_A.md](../phase9_hardening/step_a/RUNBOOK_STEP_A.md) — 📗 **17.476 B** · Step-A-Runbook; §0 Befund 1–10 und A1–A7 seit 2026-10-07 im Archiv, hier bleiben §1, A8/A9 (A8 offen für das zweite Konto), §3–§6 · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**
- [phase9_hardening/step_a/RUNBOOK_STEP_A_ARCHIVE.md](../phase9_hardening/step_a/RUNBOOK_STEP_A_ARCHIVE.md) — 📦 **47.158 B** · L3: Runbook §0 (zehn Befunde) und A1–A7, verbatim
- [phase9_hardening/step_b/RUNBOOK_STEP_B.md](../phase9_hardening/step_b/RUNBOOK_STEP_B.md) — 📗 ~26KB · **der geführte Step-B-Ablauf B0–B3** (tailscaled-watchdog installieren und live beweisen) mit **drei gemessenen Befunden** (der `sudoers`-Weg ist unbaubar, die Box kennt nur die grobe polkit-Aktion, die Units fehlen auf der VM) — **V153 damit entschieden (polkit)**, B0 hat `AUTORISIERT` gemessen · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**
- [phase9_hardening/SESSIONS_ARCHIVE.md](../phase9_hardening/SESSIONS_ARCHIVE.md) — 📦 **396.550 B**** · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**
- [phase9_hardening/MODULE_STATUS_ARCHIVE.md](../phase9_hardening/MODULE_STATUS_ARCHIVE.md) — 📦 **38.362 B** — L3-Archiv der ausführlichen §-Modulstatus-Statusspalten, verbatim, eine Sektion je Step (2026-10-04 angelegt, Nikinger-Entscheidung; **der letzte Hebel** gegen die Softcap-Überschreitung des Phase-9-Heads)
- [phase9_hardening/UPDATES_ARCHIVE.md](../phase9_hardening/UPDATES_ARCHIVE.md) — 📦 **33.086 B** · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**
- [docs/concepts/phase9_hardening_plan.md](./concepts/phase9_hardening_plan.md) — 📕 ~66KB · **der P9-Plan**, ausfuehrungsreif, 📕-Snapshot gegen `main@2f752f9`. Locks **P9-A–P9-T**, Abnahme **P9-1–P9-58**, `[VERIFY]` **V145–V164** plus die drei geerbten (V118, V136, V120). **Zwei Befunde, die eine Handover-Annahme widerlegen:** Tailscale Funnel kann keine eigene Domain (der CNAME-Weg aus `PHASE8_6_CLOSEOUT_HANDOVER.md` §4.2 existiert nicht, P9-E), und `SharePolicy` ist bereits gebaut — das Cross-Space-Rechte-Thema braucht **kein** fertiges P6 (§0.6). §12 ist der kanonische Closeout, §15 die P10-Liste
- [docs/concepts/phase9_hardening_block_trace_plan.md](./concepts/phase9_hardening_block_trace_plan.md) — 📕 **26.392 B** · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**
- [docs/concepts/phase9_hardening_block_doing_plan.md](./concepts/phase9_hardening_block_doing_plan.md) — 📕 **43.221 B** · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**
- [docs/concepts/phase9_hardening_block_settings_plan.md](./concepts/phase9_hardening_block_settings_plan.md) — 📕 **30.035 B** (§10–§12.1 seit 2026-10-07 im Archiv) · Mini-Plan 2026-10-05: Einstellungen als Fensterkette (P9-AE–AL), V118 eine Linie, D1 neu beschrieben, P9-11-Portscan-Anleitung (§5), Closeout-Liste (§6); Abnahme P9-83–95, V185–188 · **§10 = der Nachtrag aus der Bildsichtung (Locks P9-AM–P9-AS, Abnahme P9-96–P9-102), ebenfalls gebaut (§10.1) — zwei der Vorgaben sind dabei als No-op bzw. unerreichbar widerlegt**
- [docs/concepts/phase9_hardening_block_settings_plan_ARCHIVE.md](./concepts/phase9_hardening_block_settings_plan_ARCHIVE.md) — 📦 **37.271 B** · L3: die ausgeführten Nachträge §10, §11, §12, §12.1 (Locks P9-AM–P9-BF), verbatim
- [docs/concepts/phase9_hardening_block_feedback_plan.md](./concepts/phase9_hardening_block_feedback_plan.md) — 📕 **36.457 B** · Mini-Plan: Nutzer-Rückmeldung 2026-10-07, B1–B8 + E1a gebaut und als `v3.1.4` live; E2/E3 → P10
- [docs/concepts/phase9_hardening_uebersicht.svg](./concepts/phase9_hardening_uebersicht.svg) — 📕 ~17KB · Phase-9-Übersichtsgrafik 1080×1080 (Closeout 2026-10-08, gerendert und angesehen): Steps, Blöcke, Ausführer-Band mit Open-Test
- [docs/concepts/PHASE9_CLOSEOUT_HANDOVER.md](./concepts/PHASE9_CLOSEOUT_HANDOVER.md) — 📕 **15.583 B** · Abschluss-Handover P9 → P10: Status, Delta, Posten für P10 (§4), [VERIFY]-Bilanz, Open-Test MiniMax M3/M3.1
- [docs/concepts/p8x_ui_polish_notes.md](./concepts/p8x_ui_polish_notes.md) — 🟡 ~40KB · **Inhaltsquelle** der P8.6-Planung, zehn Abschnitte §1–§10 + Anhang §A–§E (Spaces-Layout, Obsidian-Map, Ordner-Zaehler, Edit-in-Place, Layering-Politik, Settings-Rename, De-AI-Lauf 2, Tags, Feedback-Button, §10 = neun Nikinger-Punkte vom 2026-09-09). **Bewusst kein Plan-Doc** — der Plan ist `phase8_6_ui_polish_plan.md`; welche Abschnitte P8.6 uebernimmt und welche nach P9 gehen, steht dort in §0.4. **§B: die Mobile-Haelfte der Aussenkante ist aufgehoben** (Nikinger 2026-09-09), Realtime bleibt draussen. 40.866 B — knapp unter dem Softcap. · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**
## Phase 8 — ✅ abgeschlossen 2026-09-08 (UI-Neuanstrich v3, Verknüpfungs-Graph)

- [phase8_ui_graph/CLAUDE.md](../phase8_ui_graph/CLAUDE.md) — 📗 ~47KB — **6.901 B ÜBER dem 40-KiB-Softcap, benannt statt versteckt** (P8-P; die Lösung ist die Rotation, kein Kürzen) · Phase-8-Head, alle Bloecke ✅, Abnahmestand **26 ✅ · 0 🟡 · 0 ⬜**, trägt die **Selection/Choice-Konvention v3** (fünfte Kategorie Vorsicht) · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**
- [phase8_ui_graph/SESSIONS_ARCHIVE.md](../phase8_ui_graph/SESSIONS_ARCHIVE.md) — 📦 ~218KB · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**
- [docs/concepts/phase8_ui_graph_plan.md](./concepts/phase8_ui_graph_plan.md) — 📕 ~83KB · ausfuehrungsreifer P8-Plan gegen `main@8f46745`, **erstmals fuer opencode/M3 als Ausfuehrenden**. N1–N12 in §0.1 gelockt, Entscheidungen P8-A–P8-Q, vier Bloecke (0 → A → B → Gate → C → D → Z), Abnahme P8-1–P8-24, `[VERIFY]` V81–V92. **§9 ist der kanonische P8-Closeout** (P8-N: ein Dokument pro Phase) — §9.4.1–§9.4.3 stehen seit Phase 8.5 auf ERLEDIGT, §9.4.7 auf 26/0/0, §9.4.5 traegt das geerbte Ledger. Kein Advisor (P8-L). Als 📕-Snapshot ausgenommen
- [docs/screenshots/](./screenshots/README.md) — 📗 ~1.1MB · kanonische Ablage aller Sichtpruefungs-Bilder, pro Phase praefixiert (`sp2_*`, `c4c5_*`, `p86_block_*`, `p86_probe_*`, `p86_smoke_*` = die 17 Gate-Belege von `v3.0.2`, `p9_step_*`, `p9_btn*`, `p9_doing_*`, `p9_trace_0*`, `p9a_legacy_*`) · die `c4c5_*`-Bilder besetzen die „Sneak Peak"-Tabelle im `README.md` · Schnellzugriff auf die jeweils aktuellen: `screenshots_latest/` · L1-Header-Card in `docs/screenshots/README.md` · keine Geheimnisse in den Bildern, nur UI-Rendering

## Phase 7 — ✅ abgeschlossen (Space-Verwaltung, Mehrfachauswahl; live `e88a624`)

- [phase7_spaces_admin/CLAUDE.md](../phase7_spaces_admin/CLAUDE.md) — 📗 ~35KB · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**
- [phase7_spaces_admin/SESSIONS_ARCHIVE.md](../phase7_spaces_admin/SESSIONS_ARCHIVE.md) — 📦 ~103KB · zwei Einträge, newest-first: **2026-08-24** (der lange Block — A6-Purge, Deploy-Blocker-Fund, Block C C1–C5, siebte Contract-Öffnung, Block B, echter Deploy, Abnahmematrix-Walkthrough, P7-24-Fund, Live-Incident, A6/P7-9) und **2026-08-23** (Step 0 + Block A bis A8), verbatim
- [docs/concepts/PHASE7_CLOSEOUT_HANDOVER.md](./concepts/PHASE7_CLOSEOUT_HANDOVER.md) — 📕 ~20KB · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**
- [docs/concepts/phase7_spaces_admin_uebersicht.svg](./concepts/phase7_spaces_admin_uebersicht.svg) — 📕 Übersichtsgrafik Phase 7 (Blockfolge 0 → A → Gate → C → B, der zweiphasige Space-Entfernen-Mechanismus, `testnutzer-p7`-Lebenszyklus, „Was Phase 8 erbt"), Status-Badge grün mit sichtbarer 22/24-Bilanz
- [docs/concepts/phase7_spaces_admin_plan.md](./concepts/phase7_spaces_admin_plan.md) — 📕 ~75KB · ausfuehrungsreifer P7-Plan gegen `main@f5691e0`. Vier Bloecke (0 → A → Gate → C → B): Haushalt, Fixes (Item-ID sichtbar, Bild-Entfernen, Feld-Whitelist, dritter Principal `testnutzer-p7`), Space-Verwaltung in der Weboberflaeche mit voller `spacectl.py`-Paritaet, Mehrfachauswahl. Gelockt P7-A–P7-W, N1–N10, Abnahme P7-1–P7-24, `[VERIFY]` V71–V80. P7-W: `testcred.py` macht Testnutzer-Credentials fuer Claude Code nutzbar. Als 📕-Snapshot ausgenommen
## Phase 6 — 🟡 code-complete, nicht live-bewiesen (Freigaben, Ordner, Werkzeuge)

- [phase6_shares/CLAUDE.md](../phase6_shares/CLAUDE.md) — 🟡 ~41KB · Phase-6-Head. Block A (Steps 0-3) ✅, Gate A→B 3/4 (Purge-Zeilenrueckgang offen); Steps 4-6 ✅ live; Step 7a/7/7b ✅ live; Mehrfachauswahl nie gebaut (ging nach Phase 7). Phase als 🟡 code-complete abgeschlossen — 12/39 Abnahmezeilen live; Handover: `PHASE6_CLOSEOUT_HANDOVER.md`. **Ueber dem 40KB-Softcap, benannt statt versteckt** (P8-P): die Phase hat genau einen Abschluss-Block, `rotate_session_block.sh` braeche mit `exit 2` ab — ein kuenstlicher Session-Block waere schlimmer als die Uebergroesse
- [phase6_shares/SESSIONS_ARCHIVE.md](../phase6_shares/SESSIONS_ARCHIVE.md) — 📦 ~188KB · vierzehn Einträge, newest-first: 2026-08-19 Deploy-Blocker + 2026-08-18 Abschluss-Review + 2026-08-17 Planungssession Step 7b + 2026-08-16 UI-Feedback-Punkte + 2026-08-14 v2.1 deployt + 2026-08-13 Steps 7a/7 + 2026-08-13 Planungssession ITEM_MOVE_PLAN + 2026-08-12 Steps 4-6/1-3 + 2026-08-09 Step 0, alle verbatim
- [docs/concepts/phase6_shares_plan.md](./concepts/phase6_shares_plan.md) — 📕 ~58KB · ausführungsreifer P6-Plan: Entscheidungen P6-A–P6-AC, Steps 0–10 (Block A Werkzeuge/Betrieb, Block B Dateisystem, Block C Bilder, hartes Gate A→B), Rechtemodell §1.2, Abnahmematrix 1–24, [VERIFY]-Register V39–V51; über 40KB, aber als 📕-Snapshot vom Softcap ausgenommen; Autor Browser-Planungssession 2026-08-09 gegen den Drive-Snapshot `2026_08_09_sharefyx-main`
- [phase6_shares/ITEM_MOVE_PLAN.md](../phase6_shares/ITEM_MOVE_PLAN.md) — 📗 ~39KB · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**
- [phase6_shares/GLOBAL_SEARCH_PLAN.md](../phase6_shares/GLOBAL_SEARCH_PLAN.md) — 📗 ~23KB · Zusatzplan zum **Deploy-Blocker vom 2026-08-18**: „über alle lesbaren Items suchen"-Modus in der Web-UI (P6-AO–AT, Abnahme 35–39). **Kernbefund:** `GET /api/v1/items` ohne `space`-Parameter ist bereits die globale item-weise ACL-gefilterte Suche (`api.py :: _items_get` → `can_read_item_as_human`) — es fehlt nur die UI-Fläche. · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**
- [phase6_shares/IMAGES_PLAN.md](../phase6_shares/IMAGES_PLAN.md) — 📗 ~25KB · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**
- [docs/concepts/PHASE6_CLOSEOUT_HANDOVER.md](./concepts/PHASE6_CLOSEOUT_HANDOVER.md) — 📕 ~20KB · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**
- [docs/concepts/phase6_shares_uebersicht.svg](./concepts/phase6_shares_uebersicht.svg) — 📕 Übersichtsgrafik Phase 6 (eine `SharePolicy` für zwei Surfaces, `acl.py :: decision_for()` liest `.share.yml`/`share_*`/`visibility` von der Platte, fail-closed; Blockleiste A/B/C; eigener Kasten „Was offen ist"), Status-Badge bewusst gelb statt grün
- [docs/UPDATE_LOG.md](./UPDATE_LOG.md) — 📗 <1KB · menschenlesbarer Änderungs-Log fürs Update-Banner in `/ui` (P6 Step 3, Plan §1.8/§2.4); streng geparst von `webui/updates.py :: parse_update_log()` (`## <ISO-Datum>` beginnt einen Eintrag, `- ` eine Zeile); neue Einträge werden **oben** eingefügt (Changelog-Konvention, oberster Eintrag = neuester); `deploy.sh` bricht ohne einen heute datierten obersten Eintrag ab (P6-X); erster Eintrag (2026-08-09) kündigt die künftige Sichtbarkeitsumstellung an

## Phase 6.5 — 🟡 code-complete, 13/14 live bestanden (Werkzeug-Ergonomie)

- [phase6_5_tools_images/CLAUDE.md](../phase6_5_tools_images/CLAUDE.md) — 🟡 ~15KB · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**
- [phase6_5_tools_images/SESSIONS_ARCHIVE.md](../phase6_5_tools_images/SESSIONS_ARCHIVE.md) — 📦 ~69KB · zwölf Einträge (Step 0, Block A, Block B Steps B1–B5, Live-Deploy, Gate A→B, Abnahmematrix ×3), verbatim
- [docs/concepts/phase6_5_tools_images_plan.md](./concepts/phase6_5_tools_images_plan.md) — 📕 ~62KB · ausfuehrungsreifer P6.5-Plan, zwei Bloecke: A = MCP-Werkzeug-Ergonomie (fuenf Punkte des 2026-08-14-Live-Feedbacks), B = Abschluss Bilder — loest `phase6_shares/IMAGES_PLAN.md` als massgebliche Quelle ab. Gelockt P6.5-A–P6.5-V, N1–N6 Nikinger-Vorgabe, Abnahme 1–14, `[VERIFY]` V59–V70. Als 📕-Snapshot ausgenommen
- [docs/concepts/PHASE6_5_CLOSEOUT_HANDOVER.md](./concepts/PHASE6_5_CLOSEOUT_HANDOVER.md) — 📕 ~9KB · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**
- [docs/concepts/phase6_5_tools_images_uebersicht.svg](./concepts/phase6_5_tools_images_uebersicht.svg) — 📕 Übersichtsgrafik Phase 6.5 (zwei Blöcke, `get_item_asset()`s Rechtegrenze, testnutzer-p7-Substitution, „Was offen ist"), Status-Badge bewusst gelb statt grün

## Completed phases

- [phase5_ui/CLAUDE.md](../phase5_ui/CLAUDE.md) — 📗 **33.280 B — wieder unter dem 40-KiB-Softcap** · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**
- [docs/concepts/PHASE5_CLOSEOUT_HANDOVER.md](./concepts/PHASE5_CLOSEOUT_HANDOVER.md) — 📕 ~18KB · Abschluss-Handover P5→P6: Status, Delta seit dem P4-Handover, offene Entscheidungen §4.1–§4.6 (F1/F2, `patch_item`, Client-Surface-Logging, O2), [VERIFY]-Bilanz V27–V38
- [docs/concepts/phase5_ui_uebersicht.svg](./concepts/phase5_ui_uebersicht.svg) — 📕 Übersichtsgrafik Phase 5 (Cookie-Session vs. Bearer-Trennung, Konvergenz auf denselben Storage-Kern)
- [docs/concepts/P5_ABNAHME_2026-08-09.md](./concepts/P5_ABNAHME_2026-08-09.md) — 📕 ~11KB · Abnahmeprotokoll Phase 5: **20/20 live bestanden**, Kurzbeleg für Zeile 20 (Reboot), Befunde-Übersicht (Origin-Fund, S9/S10-Nebenfund, F1/F2, `patch_item`-Feedback), Runbook-Schritt 4 (`auth-users`-Credential/Keyring) bereits erledigt vorgefunden
- [docs/concepts/phase5_ui_plan.md](./concepts/phase5_ui_plan.md) — 📕 ~80KB · ausführungsreifer P5-Plan: Entscheidungen P5-A–P5-AE, Steps 0–9 (Block A Sicherheit/Selbstverwaltung, Block B REST-API/UI), Designsystem (§4.1/§4.3 in Step 7b revidiert, Snapshot bleibt unverändert), Abnahmematrix 1–20, [VERIFY]-Register V27–V38; über 40KB, aber als 📕-Snapshot vom Softcap ausgenommen
- [phase5_ui/ABNAHME_MATRIX_ARCHIVE.md](../phase5_ui/ABNAHME_MATRIX_ARCHIVE.md) — 📦 ~13KB · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**
- [phase5_ui/SESSIONS_ARCHIVE.md](../phase5_ui/SESSIONS_ARCHIVE.md) — 📦 ~159KB · dreizehn archivierte Session-Blöcke (Step 0–4 inkl. Block-A-Gate/Origin-Fund, Block-A-Gate-Live-Lauf, Step 6, Step 7, Step 7b, Step 8, Step 8b, Verifikationssession/Zeilen-10-19-Nachträge), verbatim
- [phase4_auth/CLAUDE.md](../phase4_auth/CLAUDE.md) — 📗 ~33KB · phase head; Steps 0–7 ✅ — **16/16 Abnahmezeilen live bestanden, Phase 4 ✅** (2026-07-30). Sicherheitsbefunde **S1–S10 / O1–O2** (S10 neu 2026-08-06, O2 geschlossen 2026-08-09). Detailnarrative + Inbetriebnahme-Runbook liegen im `SESSIONS_ARCHIVE.md`; read + newest Session-stopped block first
- [docs/concepts/PHASE4_CLOSEOUT_HANDOVER.md](./concepts/PHASE4_CLOSEOUT_HANDOVER.md) — 📕 ~18KB · Abschluss-Handover P4→P5: Status, Delta seit dem P3-Handover, offene Entscheidungen für die Web-UI-Planung §4.1–§4.5, [VERIFY]-Bilanz V14–V26
- [docs/concepts/phase4_auth_uebersicht.svg](./concepts/phase4_auth_uebersicht.svg) — 📕 Übersichtsgrafik Phase 4 (Auth-Fluss, Komponenten)
- [docs/concepts/P4_ABNAHME_2026-07-29.md](./concepts/P4_ABNAHME_2026-07-29.md) — 📕 ~24KB · Abnahmeprotokoll Phase 4: **16/16 live bestanden** (drei Nachträge 2026-07-30: Zeilen 14/15, Zeile 9, Schnitt+Zeile 16), CLI-Ausschnitt + DB-Gegenprobe als Beleg, Befunde B1–B3 (alle klein, zwei behoben)
- [docs/concepts/P4_SECURITY_REVIEW_2026-07-29.md](./concepts/P4_SECURITY_REVIEW_2026-07-29.md) — 📕 ~13KB · Sicherheits-Review P3+P4 vor der Live-Abnahme: Befund S1 (behoben) plus **S2–S8 in P5 Step 1 geschlossen** (`phase4_auth/CLAUDE.md`s Tabelle, Status-Nachtrag 2026-08-02) und Betriebsnotiz O1 (weiterhin offen), **und** 15 ausdrücklich geprüfte, in Ordnung befundene Punkte (verified negatives) — der Snapshot selbst bleibt unverändert (📕), der aktuelle Status steht im Phase-Head
- [docs/concepts/phase4_auth_plan.md](./concepts/phase4_auth_plan.md) — 📕 ~76KB · ausführungsreifer P4-Plan (Entscheidungen P4-A–P4-R, Steps 0–7, eigener Authorization Server, Argon2id + TOTP, opake Token); über 40KB, aber als 📕-Snapshot vom Softcap ausgenommen; Autor Browser-Planungssession 2026-07-28, **ohne frischen Repo-Zugriff geschrieben** — Anker sind Funktionsnamen/Suchstrings, keine Zeilennummern
- [phase4_auth/SESSIONS_ARCHIVE.md](../phase4_auth/SESSIONS_ARCHIVE.md) — 📦 ~82KB · das ausgeführte Inbetriebnahme-Runbook (Step 7, 2026-08-06 verbatim aus dem Head verschoben) plus neun archivierte Session-Blöcke (Step 0+1+2, Step 3, V14+Step 4, Step 5, Step 6a, Step 6b, Step-7-Code-Vorbereitung, Befund S1+Sicherheits-Review+12/16-Abnahme, CSP-Fix+Zeilen 14/15+Zeile 9/15/16) plus die komprimierte Steps-0–6a-Detailnarrative (2026-07-31, keine Session-Rotation, eigener Abschnitt), verbatim, newest-first
- [phase3_edge/CLAUDE.md](../phase3_edge/CLAUDE.md) — 📗 ~30KB · phase head; alle 8 Steps ✅ — **13/13 Abnahmezeilen live bestanden, Phase 3 ✅**. MCP-Unit liegt in `phase4_auth/systemd/`. · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**
- [docs/concepts/phase3_edge_plan.md](./concepts/phase3_edge_plan.md) — 📕 ~46KB · ausführungsreifer P3-Plan (Entscheidungen P3-A–P3-N, Steps 0–7); über 40KB, aber als 📕-Snapshot vom Softcap ausgenommen
- [phase3_edge/SESSIONS_ARCHIVE.md](../phase3_edge/SESSIONS_ARCHIVE.md) — 📦 ~57KB · zwölf archivierte Session-Blöcke (Step 0–6, inkl. Live-Abnahme-Funde B3/B4, beide Live-Abnahme-Sessions vom 2026-07-27, Token-Rotation-Session vom 2026-07-28, Zeile-6-Reboot-Session vom 2026-07-29, **Zeile-13-Restore-Bestätigung vom 2026-08-02**), verbatim, newest-first
- [docs/concepts/P3_ABNAHME_2026-07-27.md](./concepts/P3_ABNAHME_2026-07-27.md) — 📕 ~19KB · Abnahmeprotokoll Phase 3: 10/13 live bestanden, Zeilen 6/12/13 per Nikinger-Entscheidung auf nächste Phase verschoben, CLI-Ausschnitt als Beleg, Befunde B5/B6
- [docs/concepts/PHASE3_CLOSEOUT_HANDOVER.md](./concepts/PHASE3_CLOSEOUT_HANDOVER.md) — 📕 ~17KB · Abschluss-Handover P3→P4: Status, Delta seit dem P2-Handover, [VERIFY]-Bilanz V1–V13, geerbte Abnahmezeilen 6/12/13, Doku-Drift-Liste aus der Autocompact-Session inkl. Nachträgen zum nikinger-Token-Fund, offene Entscheidungen für die OAuth-Planung
- [docs/concepts/phase3_edge_uebersicht.svg](./concepts/phase3_edge_uebersicht.svg) — 📕 Übersichtsgrafik Phase 3 (Request-Weg, Komponenten)
- [phase2_mcp/CLAUDE.md](../phase2_mcp/CLAUDE.md) — 📗 ~24KB · phase head; Steps 0–7 ✅, live-verifiziert 2026-07-26. Seither erweitert: `webui`-Routen-Mount (P5 Step 4), siebtes Tool `patch_item` + `ua`-Feld + `oauth.store`-Durchreichung (P6 Steps 1–3). 95 Tests; read + newest Session-stopped block first
- [docs/concepts/phase2_mcp_plan.md](./concepts/phase2_mcp_plan.md) — 📕 ~46KB · ausführungsreifer P2-Plan (Entscheidungen P2-A–P2-N, Steps 0–7); über 40KB, aber als 📕-Snapshot vom Softcap ausgenommen
- [docs/concepts/P2_ADAPTER_ABNAHME_2026-07-26.md](./concepts/P2_ADAPTER_ABNAHME_2026-07-26.md) — 📕 ~11KB · Abnahmeprotokoll über den echten Custom Connector, 21/21 Prüfungen, beide Befunde behoben (B1, B2 — siehe Nachtrag)
- [phase2_mcp/SESSIONS_ARCHIVE.md](../phase2_mcp/SESSIONS_ARCHIVE.md) — 📦 ~38KB · acht archivierte Session-Blöcke (Step 0–7), verbatim, newest-first
- [docs/concepts/PHASE2_CLOSEOUT_HANDOVER.md](./concepts/PHASE2_CLOSEOUT_HANDOVER.md) — 📕 ~11KB · Abschluss-Handover P2→P3: Status, Delta seit dem P1-Handover, offene Entscheidungen für die Exposure-Phase, [VERIFY]-Bilanz V1–V9
- [phase1_storage/CLAUDE.md](../phase1_storage/CLAUDE.md) — 📗 **20.212 B — wieder unter dem 40-KiB-Softcap** · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**
- [docs/concepts/phase1_storage_plan.md](./concepts/phase1_storage_plan.md) — 📕 ~15KB · ausführungsreifer P1-Plan (Entscheidungen A–H, Steps 0–7)
- [phase1_storage/SESSIONS_ARCHIVE.md](../phase1_storage/SESSIONS_ARCHIVE.md) — 📦 ~27KB · archivierte Session-stopped-Blöcke, verbatim, newest-first
- [phase1_storage/CONTRACTS_ARCHIVE.md](../phase1_storage/CONTRACTS_ARCHIVE.md) — 📦 ~32KB · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**
- [docs/concepts/PHASE1_CLOSEOUT_HANDOVER.md](./concepts/PHASE1_CLOSEOUT_HANDOVER.md) — 📕 ~12KB · Abschluss-Handover P1→P2: Status, Delta, Contract, offene Entscheidungen D1–D6, `[VERIFY]`-Bilanz

## Concept docs (📕 snapshots — the plan a phase was built from)

*(keine eigenen Einträge hier — Konvention: ein Dokument pro Phase, kein
Konzept+Plan+Handover-Trio. P1- bis P5-Pläne stehen oben bei ihrer jeweiligen Phase, nicht
doppelt hier gelistet.)*

## Project-wide session log (Wurzel-Current-State-Archiv)

- [docs/INDEX_ENTRIES_ARCHIVE.md](./INDEX_ENTRIES_ARCHIVE.md) — 📦 **46.456 B** · L3-Archiv der **datierten Nachträge aus den Einträgen dieser Karte**, verbatim, ein Abschnitt je Karte in der Reihenfolge der Karte (nicht newest-first). **Regel:** eine Kartenzeile bekommt **keinen** datierten Nachtrag mehr (`test_no_entry_line_carries_a_dated_addendum_any_more`) — die Karte ist **Stand**, das Archiv ist **Chronik**
- [docs/INDEX_KURZUNG_ARCHIVE.md](./INDEX_KURZUNG_ARCHIVE.md) — 📦 **11.961 B** · L3-Archiv der aus der Karte gekürzten Texte — die acht Abschnittsköpfe und fünf Kartenzeilen-Chroniken, verbatim (die letzten zwei am 2026-10-24, DO-2-Luft); die Karte trägt wieder Stand, dieses Archiv die Chronik des Kürzens

- [docs/INDEX_UPDATES_ARCHIVE.md](./INDEX_UPDATES_ARCHIVE.md) — 📦 **19.557 B** · L3-Archiv der `updated:`-Kette **dieser** Datei, verbatim, newest-first. Erste Rotation 2026-09-19 von Hand; **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**
- [docs/PROJECT_SESSION_LOG.md](./PROJECT_SESSION_LOG.md) — 📦 **259.775 B** (vor der 24-Block-Rotation 101.450 B) · L3-Archiv der historischen `[YYYY-MM-DD]`-Session-Bloecke aus `CLAUDE.md` §Current state, newest-first, plus §Frontmatter-Archiv (die `updated:`-Kette der Wurzel-`CLAUDE.md`, 28 Eintraege, verbatim seit 2026-09-13). Wer die Chronik einer alten Phase sucht, faengt hier an, nicht im Wurzel-Head

## Referenzmaterial (nicht Teil des Plan/Konzept/Handover-Trios)

- [screenshots_latest/](../screenshots_latest/README.md) — 🔗 Symlink-Komfort · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**
- [phase5_ui/THIRD_PARTY_LICENSES.md](../phase5_ui/THIRD_PARTY_LICENSES.md) — 📦 Lizenztext · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**
- [docs/concepts/notiz_heft_example.html](./concepts/notiz_heft_example.html) — 📕 UI-Vorlage,
  vom Nikinger in P5 Step 7 ins Repo gelegt (vorher nur im Projektwissen, für Claude Code nicht
  zugänglich). **Achtung:** enthält eine clientseitige Vault-Verschlüsselung, die mit
  Rahmenentscheidung R4 unvereinbar ist. Nur als Layout-/Interaktionsvorlage lesen, nicht als
  Architekturvorlage — P5-V dokumentiert genau, was daraus geerntet wurde und was bewusst nicht
  (`phase5_ui/CLAUDE.md`, Step-7-Session-Block).
