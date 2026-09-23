---
status: archive
purpose: L3-Archiv der `updated:`-Frontmatter-Kette von `docs/INDEX.md` — verbatim, newest-first
read-when: nur beim Audit, wenn die Herkunft einer INDEX-Änderung rekonstruiert werden muss
detail: L3
up: ./INDEX.md
down:
updated: 2026-09-19 (Archiv angelegt — erste Rotation der INDEX-`updated:`-Kette, von Hand ausgeführt; das Skript `scripts/rotate_index_updates.sh` entsteht in P9 Step 0.1 [Lock P9-L] und übernimmt danach jede weitere Rotation)
---
- 2026-09-20 (**P9 Step 0** — Phasenverzeichnis, INDEX-Rotationsskript, vier Doku-Defekte plus ROADMAP/CLAUDE.md oversize benannt, `doc_health.py`)
- 2026-09-19 (**P9 aufgenommen** — `phase9_hardening_plan.md` + dieses Archiv. Ältere Einträge verbatim: `docs/INDEX_UPDATES_ARCHIVE.md`)
# `docs/INDEX.md` — Archiv der `updated:`-Einträge (L3)

> Die Kette in der Frontmatter von `docs/INDEX.md` trägt **einen** aktuellen Eintrag; ältere
> stehen hier, verbatim und newest-first. Dieselbe Rotationsregel, die `SESSIONS_ARCHIVE.md`
> für Phase-Heads erfüllt — der Grund ist derselbe: die Kette war dreimal in einer Phase die
> Ursache dafür, dass `docs/INDEX.md` das ≤-38-KB-Kriterium riss.

## 2026-09-19

2026-09-19 (**Phase 8.6 abgeschlossen ✅, `v3.0.2` live seit 2026-09-18** [SHA `1ad2665`, `health_gate` 9/9]. Step Z: Abnahmebilanz **45 ✅ · 5 ⚠️ · 0 ⬜ · 4 ersetzt** von 54 Zeilen, `[VERIFY]` **37 zu · 2 offen (V118, V136)**, kanonischer Closeout in `phase8_6_ui_polish_plan2.md` §9, Handover auf **Abschluss**-Fassung P8.6 → P9 umgeschrieben, Uebersichtsgrafik neu. **Diese Datei stand bei Step-Z-Beginn auf 45.870 B** gegen das ≤-38-KB-Kriterium — dritter Verstoss in einer Phase; die `updated:`-Kette ist hier auf **einen** Eintrag gekuerzt und die Phase-8.6-Sektion auf Abschluss-Umfang gebracht. Die eigentliche Loesung — `INDEX_UPDATES_ARCHIVE.md` + Rotation analog `rotate_session_block.sh` — bleibt **P9-Arbeit**; die Handarbeit traegt nachweislich nicht mehr. Aeltere `updated:`-Eintraege: die Phase-Heads und `phase*/SESSIONS_ARCHIVE.md`, sowie `git log -p docs/INDEX.md`.)
