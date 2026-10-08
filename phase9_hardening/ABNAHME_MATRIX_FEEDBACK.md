---
status: live
purpose: Teil der Abnahmematrix Phase 9 — der Block feedback (P9-121 – P9-137). Zeilen mit Stand und Beleg; die Bilanz und die Statusregel stehen im Hub ABNAHME_MATRIX.md
read-when: wenn eine Zeile aus dem feedback-Block gesucht, belegt oder auf einen anderen Marker gesetzt wird
detail: L2
up: ./ABNAHME_MATRIX.md
down:
  - ../docs/concepts/phase9_hardening_block_feedback_plan.md   # P9-121 – P9-137, Locks P9-BG–P9-BQ
updated: 2026-10-08 (angelegt — `ABNAHME_MATRIX_BLOECKE.md` stand bei 39.667 B, die drei E1a-Zeilen hätten den Softcap gerissen; der Abschnitt B1/B2 per `scripts/move_sections.py` verbatim hierher)
---
# Abnahmematrix Phase 9 — Teil: Block feedback (P9-121 – P9-137)

> Lebender Teil (📗), **kein** Archiv: die Zeilen hier zählen in die Bilanz im Hub
> `ABNAHME_MATRIX.md`, und ihr Marker darf sich ändern. Der Abschnitt B1/B2 ist **wortgleich** aus
> `ABNAHME_MATRIX_BLOECKE.md` verschoben worden.

## Block feedback — B1: Anlegen im aktiven schreibbaren Space (P9-121 – P9-124)

> Locks **P9-BG** (der Server liest `space`, geprüft wie `tools.py:641`) und **P9-BI** (die Konfliktkopie
> trägt den Space des Konflikt-Items). Plan: `../docs/concepts/phase9_hardening_block_feedback_plan.md` §4 B1.
> Behebt R2 „Anlegen im fremden Space landet im Home-Space". Stand **gebaut 2026-10-07, nicht deployt.**

| Nr | Kriterium | Stand | Beleg |
|---|---|---|---|
| **P9-121** | Anlegen im Team-Space legt **dort** an, und man landet dort | ✅ | `test_create_item_in_writable_foreign_space_lands_there` · Zwei-Principalen-Probe (`scripts/p9_feedback_self_check.py`) **4/4**, S1 misst die Datei unter `team/` und **nicht** unter `alpha/`; **Gegenlauf gegen den alten Client 2/4 rot** (S1 + S2) · `pytest` **1252** |
| **P9-122** | Anlegen ohne `space` → Home-Space, unverändert | ✅ | `test_create_item_without_space_still_lands_in_home` · Probe S3 |
| **P9-123** | Anlegen im fremden Home ohne `write:` → 403, nichts geschrieben | ✅ | `test_create_item_in_foreign_space_without_write_is_forbidden` prüft zusätzlich, dass **keine Datei** entstanden ist (fail-closed, Hard Rule 4 Fassung 2026-08-09) |
| **P9-124** | Die Konfliktkopie („als neu speichern") landet im Space des Konflikt-Items | ⚠️ | Client: `dialogs.js` setzt `payload.space` aus `state.conflictCurrent.space` (**nicht** aus dem Editier-Snapshot, der kein `space` trägt — datierte Korrektur im Plan §8). Die Serverseite ist durch P9-121 belegt; **die Konfliktstrecke selbst wurde im Browser nicht gefahren** — benannte Lücke, schließt eine Probe mit zwei Sitzungen auf demselben Item |
| **P9-125** | Der Anlegen-Dialog nennt sein Ziel | ✅ | **B2, Lock P9-BH, 2026-10-08:** `#create-target` im Dialog, gefüllt per `textContent` aus `state.activeSpace` — **derselben** Quelle wie der POST aus B1. Probe (`scripts/p9_feedback_self_check.py`, `probes/p9_feedback_b2_probe.json`) **6/6 plus eine Messung**: S4 liest im offenen Dialog `Anlegen in: team`, S4b `Anlegen in: alpha (dein Home-Space)`; **Gegenlauf gegen den alten Client 4/6 rot** (S4 + S4b, Zielzeile fehlt), `probes/p9_feedback_b2_probe_gegenprobe.json` · Wächter `test_the_create_dialog_names_its_target_space`, gegen den alten Client rot · Bild `docs/screenshots/p9_feedback_b2_ziel_team.png` · `pytest` **1253** · **benannte Abweichung vom Plan:** der Fall „globale Sicht / nur lesbarer Space → Home" ist **unerreichbar**, der Dialog ist dort ausgehängt (`setCreateControlsPresent`, Guard in `openCreateDialog`); für die Übersicht **gemessen** (S5: nach `team` → Übersicht **0** sichtbare Anlegen-Knöpfe, obwohl `state.activeSpace` dort `team` bleibt) — Plan §8 B2 |
