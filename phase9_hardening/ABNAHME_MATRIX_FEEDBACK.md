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

## Block feedback — E1a: Team-Spaces verschieben, archivieren, löschen (P9-135 – P9-137)

> Locks **P9-BP** (Team-Space = kein Home-Space eines Nutzers; jedes Mitglied mit `write:` verschiebt und
> löscht, auch fremde Items) und **P9-BQ** (Eigentum über Git-Autor und `updated_by`, kein neues Feld).
> Plan: `../docs/concepts/phase9_hardening_block_feedback_plan.md` §3 E1, §8 E1a. Stand **gebaut 2026-10-08, nicht deployt.**

| Nr | Kriterium | Stand | Beleg |
|---|---|---|---|
| **P9-135** | Team-Space: jedes Mitglied mit Schreibrecht verschiebt, archiviert und löscht, auch fremde Items, auch per Drag & Drop | ✅ | `test_team_member_deletes_and_moves_a_foreign_item` (Ordner-PATCH 200, DELETE 204, Datei in `._trash/`) · `test_spaces_list_marks_team_spaces` (`team` in `/spaces` **und** `/overview`) · Probe `scripts/p9_feedback_self_check.py` **11/11** (`probes/p9_feedback_e1a_probe.json`): S6 alpha löscht ein Item von **beta** über den echten Zwei-Schritt-Dialog, S7 zieht ein beta-Item per **echter Maus** auf `ablage`, S8 Team-Zeilen mit Löschknopf · **Gegenlauf gegen den Code vor E1a 4/4 rot** (S6, S6b, S7, S8; `…_gegenprobe.json`) · **Archivieren** war schon frei (V191: Editor ist bei schreibbarem Item eingehängt, `api.py` prüft `can_write_item_as_human`) · `pytest` **1259** |
| **P9-136** | Home-Space eines anderen: Löschen und Umräumen bleiben mit `write:` verboten | ✅ | `test_foreign_home_space_keeps_p9_k_even_with_write` — **dieselbe** `.share.yml`, der Space nur per `upsert_user` zum Home-Space gemacht ⇒ 403/403, beide Items unverändert. **Mutation:** `_team_writer` ohne Home-Prüfung ⇒ genau dieser Test rot · `test_team_space_without_write_still_cannot_delete` (nur `read:` ⇒ 403) · **Befund 2026-10-08, behoben:** ein PATCH, der den **eigenen** Space des Items als `space` wiederholt, lief seit Step 7b (2026-08-17) an beiden Riegeln vorbei (gemessen: **200**) — `test_repeating_the_own_space_does_not_skip_the_folder_lock`, ohne Fix rot |
| **P9-137** | Der Papierkorb-Commit trägt den Löschenden als Git-Autor, der Löschdialog nennt `updated_by` | ✅ | Probe S6b: Dialogtext `… Zuletzt geändert von beta.`, `git log -1 --format=%an` im Wegwerf-`DATA_ROOT` = `alpha` · Bild `docs/screenshots/p9_feedback_e1a_loeschen.png` · Wächter `test_team_spaces_unlock_move_drag_and_delete_but_not_share` (`textContent`, nicht `innerHTML`) |

## Block feedback — B3: Schließen im Einstellungsmenü (P9-131)

> Lock **P9-BN**. Stand **gebaut 2026-10-08, nicht deployt.**

| Nr | Kriterium | Stand | Beleg |
|---|---|---|---|
| **P9-131** | Einstellungsmenü hat „Schließen", der Knopf schließt die ganze Kette | ✅ | `#settings-menu-close` in `.overlay__actions` des Menü-Panels, verdrahtet auf `closeSettings` · Probe S9 (`probes/p9_feedback_b3_probe.json`, **12/12**): Menü + Update-Log offen (**2** Panels) → Klick → Overlay `hidden`, **0** Panels offen · **Gegenlauf gegen den alten Client: S9 rot** (11/12) · Wächter `test_the_settings_menu_has_a_close_button_that_closes_the_whole_chain`, ohne Fix rot · Bild `docs/screenshots/p9_feedback_b3_menue.png` (Knopf in Standardhöhe, höher als die Menüpunkte — Sichtprüfung) · `pytest` **1261** |

## Block feedback — B4: Abstand der Mitgliederzeilen (P9-130)

> Lock **P9-BM**. Stand **gebaut 2026-10-08, nicht deployt.**

| Nr | Kriterium | Stand | Beleg |
|---|---|---|---|
| **P9-130** | Mitgliederzeilen mit Standardabstand, **gemessen mit gefüllter Liste** | ✅ | `#space-member-list` als Flex-Spalte mit `gap: var(--space)` (`app.css`), kein `margin` an den Zeilen · Probe S10 (`probes/p9_feedback_b4_probe.json`, **13/13**): `team` → **4** Zeilen (alpha/beta je schreiben + lesen), Abstände **[8, 8, 8]** px gegen `--space` = 8 px · **Gegenlauf `gap: 0` (CSS temporär, danach zurückgesetzt): S10 rot**, Abstände [0, 0] (`probes/p9_feedback_b4_probe_gegenprobe.json`; die übrigen sechs roten Stationen dort sind Folgen der verbrauchten Wegwerf-Instanz, nicht des CSS) · Wächter `test_the_settings_chain_…` (Mitgliederliste: `display`, `flex-direction`, `gap`) · **Abweichung vom Plan, benannt:** die Probe *legt kein Mitglied an* — der Seed von `team` trägt bereits alpha **und** beta, die Liste ist damit im Harness erstmals gefüllt; das schließt die Grenze aus P9-107/P9-110 ebenso, und ein Anlegen bräuchte einen dritten Principal samt Re-Auth. Bild `docs/screenshots/p9_feedback_b4_mitglieder.png` |
