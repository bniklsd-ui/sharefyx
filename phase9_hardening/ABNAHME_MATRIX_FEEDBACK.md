---
status: live
purpose: Teil der Abnahmematrix Phase 9 — der Block feedback (P9-121 – P9-137). Zeilen mit Stand und Beleg; die Bilanz und die Statusregel stehen im Hub ABNAHME_MATRIX.md
read-when: wenn eine Zeile aus dem feedback-Block gesucht, belegt oder auf einen anderen Marker gesetzt wird
detail: L2
up: ./ABNAHME_MATRIX.md
down:
  - ../docs/concepts/phase9_hardening_block_feedback_plan.md   # P9-121 – P9-137, Locks P9-BG–P9-BQ
updated: 2026-10-08 (P9-133: `pytest` 1265 auf dem Closeout-Commit `926daa6` bestätigt) | 2026-10-08 (Closeout: P9-133/P9-134 eingetragen, beide ✅; Block live als `v3.1.4`) | 2026-10-08 (**B8 gemessen, kein Fix** — V190 beantwortet: ein Space-Wechsel = eine Anfrage; P9-132 ✅ Befundzweig, P9-126 ✅ (390 px gestrichen, Nikinger), Bilanz 118 ✅ · 13 ⚠️ · 1 ⬜) | 2026-10-08 (+1 Zeile P9-126, Block feedback B7; Bilanz 116 ✅ · 14 ⚠️ · 1 ⬜) | 2026-10-08 (angelegt — `ABNAHME_MATRIX_BLOECKE.md` stand bei 39.667 B, die drei E1a-Zeilen hätten den Softcap gerissen; der Abschnitt B1/B2 per `scripts/move_sections.py` verbatim hierher)
---
# Abnahmematrix Phase 9 — Teil: Block feedback (P9-121 – P9-137)

> Lebender Teil (📗), **kein** Archiv: die Zeilen hier zählen in die Bilanz im Hub
> `ABNAHME_MATRIX.md`, und ihr Marker darf sich ändern. Der Abschnitt B1/B2 ist **wortgleich** aus
> `ABNAHME_MATRIX_BLOECKE.md` verschoben worden.
>
> **[2026-10-08, Closeout]** Alle Abschnitte unten sagen „gebaut, nicht deployt" — das ist ihr Stand beim
> Bau. Seit dem 2026-10-08 ist der ganze Block **live als `v3.1.4`** (Release `20261008T201607.460757Z`,
> SHA `d04c0ec`, `health_gate.sh` **9/9 OK**, Ausgabe im Closeout-Commit).

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
| **P9-130** | Mitgliederzeilen mit Standardabstand, **gemessen mit gefüllter Liste** | ✅ | `#space-member-list` als Flex-Spalte mit `gap: var(--space)` (`app.css`), kein `margin` an den Zeilen · Probe S10 (`probes/p9_feedback_b4_probe.json`, **13/13**): `team` → **4** Zeilen (alpha/beta je schreiben + lesen), Abstände **[8, 8, 8]** px gegen `--space` = 8 px · **Gegenlauf `gap: 0` (CSS temporär, danach zurückgesetzt): S10 rot**, Abstände [0, 0] (`probes/p9_feedback_b4_probe_gegenprobe.json`; die übrigen sechs roten Stationen dort sind Folgen der verbrauchten Wegwerf-Instanz, nicht des CSS) · Wächter `test_the_settings_chain_…` (Mitgliederliste: `display`, `flex-direction`, `gap`) · **Abweichung vom Plan, benannt:** die Probe *legt kein Mitglied an* — der Seed von `team` trägt bereits alpha **und** beta, die Liste ist damit im Harness erstmals gefüllt; das schließt die Grenze aus P9-107/P9-110 ebenso, und ein Anlegen bräuchte einen dritten Principal samt Re-Auth. Bild `docs/screenshots/p9_feedback_b4_mitglieder.png` · **Nachsatz nach der Sichtprüfung (2026-10-08):** der „Entfernen"-Knopf klebte am Text (Abstand 0 px); `.space-member-row` ist jetzt Flex mit `justify-content: space-between` und `gap: var(--space)`, der Knopf sitzt auf der rechten Kante von „Hinzufügen“ (beide **1154 px**), Abstand zum Text 83/91 px · Probe S10b, **14/14**; **Gegenlauf ohne die Regel: S10b rot** (Kanten 1071/1063 gegen 1154, Abstand 0; `probes/p9_feedback_b4b_probe_gegenprobe.json`) · Wächter um die Zeilenregel erweitert |

## Block feedback — B5: Titelzeile im Löschdialog (P9-129)

> Lock **P9-BL**. Stand **gebaut 2026-10-08, nicht deployt.**

| Nr | Kriterium | Stand | Beleg |
|---|---|---|---|
| **P9-129** | Löschdialog zeigt den Titel als eigene Zeile direkt über dem Feld (Text, kein HTML) | ✅ | `<span id="trash-title">` im `<label>` zwischen Beschriftung und `#trash-confirm-input`, gefüllt per `textContent` in `openTrashTitleDialog` (`dialogs.js`), fett (600), umbrechend · Probe S11 (`probes/p9_feedback_b5_probe.json`, **15/15**): Text == `<i>B5</i> Titel` (ein HTML-Titel, als Text gezeigt, **0** Kindelemente), Abstand zum Feld **4 px**, Löschknopf **gesperrt** (Gate unverändert, P9-K) · **Gegenlauf gegen den alten Client: S11 rot** (14/15, kein `#trash-title`; `probes/p9_feedback_b5_probe_gegenprobe.json`) · Wächter `test_the_delete_dialog_shows_the_title_as_its_own_line_above_the_field` · Bild `docs/screenshots/p9_feedback_b5_titelzeile.png` |

## Block feedback — B6: Enter löst die Primäraktion aus (P9-127, P9-128)

> Lock **P9-BK**. Stand **gebaut 2026-10-08, nicht deployt.**

| Nr | Kriterium | Stand | Beleg |
|---|---|---|---|
| **P9-127** | Enter löst in jedem Overlay aus Plan §5 die Primäraktion aus, die Ausnahmen bleiben folgenlos | ⚠️ | Eine Tabelle `enterTable()` + `SETTINGS_ENTER` in `app.js` (Overlay → Primärknopf → erlaubte Felder), Reihenfolge wie bei ESC; `conflict-dialog` und `link-picker-dialog` mit `null` ausgenommen · Probe S12 (`probes/p9_feedback_b6_probe.json`, **20/20**): Anlegen-Dialog legt per Enter an (S12a), `<select>` behält sein Enter (S12b), Enter im TOTP-Feld des Passwort-Panels klickt „Ändern" **genau einmal**, im Passwortfeld nicht (S12e) · **Gegenlauf alter `app.js`: S12a rot** (Item nicht angelegt) · Wächter `test_enter_triggers_the_primary_action_in_every_overlay_except_the_two_exceptions` · **⚠️, nicht ✅:** im Browser belegt sind Anlegen, Löschen, `<select>` und das Passwort-Panel; Neuer-Ordner, Verschieben, Teilen, Space-Entfernen, Bestätigen, Legacy-Host und die beiden anderen Einstellungs-Panels stehen **nur in der Tabelle und im Wächter**, nicht in der Probe |
| **P9-128** | Enter am gesperrten Löschknopf ist folgenlos (Gegenlauf) | ✅ | Probe S12c: Enter bei leerem Titelfeld → Dialog bleibt offen, Item da; S12d: Enter mit exaktem Titel löscht · Die Tabelle prüft `button.hidden \|\| button.disabled` vor dem Klick (Gate P9-K unberührt) |

**Fund aus B6, kein Plan-Punkt (datiert 2026-10-08):** `dialogs.js :: openTrashTitleDialog` hängte
`{ once: true }`-Listener an Absenden **und** Abbrechen. **Abbrechen ließ den Absenden-Listener stehen**, der nächste Löschdialog
schickte beim Absenden **zwei** DELETEs (der zweite: „Item nicht gefunden", Dialog blieb offen) — und ein Fehlversuch
(Konflikt) verbrauchte den Listener, ein zweiter Klick tat nichts. Gefunden, weil die B5-Probe einen Dialog abbricht und B6 danach
löscht. Behoben mit `AbortController` plus Unterwegs-Flag; **Gegenlauf alter `dialogs.js`: S12d rot** (Dialog offen mit Fehler);
Wächter `test_the_trash_dialog_cleans_up_its_listeners_when_it_closes`.

## Block feedback — B7: Übersicht, Name vor den Zählern (P9-126)

> Lock **P9-BJ**. Stand **gebaut 2026-10-08, nicht deployt.**

| Nr | Kriterium | Stand | Beleg |
|---|---|---|---|
| **P9-126** | Übersicht: Name bis 16 Zeichen voll lesbar bei 1440/1024 px, Chips ≤ 2 Zeilen (390 px **gestrichen**, Nikinger 2026-10-08) | ✅ | **V189 gemessen (vorher):** bei allen fünf Eimern gefüllt und 16 Zeichen Name ist die Namensbox bei 1440 px **0 px breit** (`clientWidth 0`, Text 136 px) — der Name sitzt auf Flex-Basis 0, die Chips auf `auto`. **Gebaut:** `.overview__space-name-label` `flex: 0 1 auto`, `.overview__space-counts` `flex: 1 1 calc(var(--space) * 33)`, `.overview__space-open` `flex-wrap: wrap` (die Leiste rutscht unter den Namen, wenn beides nicht in eine Zeile passt), `title` am Namen (`list.js`). **Probe S13** (`scripts/p9_feedback_self_check.py`, `probes/p9_feedback_b7_probe.json`, **23/23**): 1440 und 1024 px Name voll (136/136), Chips **1 Zeile**, `title` an jeder echten Zeile; **Gegenlauf alte Regel + altes `list.js`** (`p9_feedback_b7_probe_gegenprobe.json`): S13 **rot bei 1440** (Name 0 px) **und 1024** (Titel fehlt), 21/23. **Nikinger-Entscheidung 2026-10-08:** *390 px ist kein Ziel* — Desktop-Untergrenze ist 1024 px, die Mobil-Anwendung wird ein eigenes Design (Zusatz, kein Ersatz); das Kriterium ist darauf eingeengt. **Befund dahinter (gemessen):** bei **390 px** ist die Shell `Rail 240 px + Liste 1fr` (`app.css`, `@media (max-width: 1024px)`), die Zeile **85 px** breit — kein 16-Zeichen-Name passt, egal welche Regel; S13b misst das nur (Name 85 von 136 px, Chips 5 Zeilen). Ein Mobil-Layout ist Lock P9-A und nicht Teil dieser Desktop-Anwendung. **Zweite Abweichung:** der Kandidat `min-width: min(16ch, 40%)` aus P9-BJ entfällt — er reservierte auch für „team" 136 px und schob dessen Chips in eine zweite Zeile; mit dem Umbruch braucht der Name keine Untergrenze. Die Zeile der Probe ist ein **geklonter** Eintrag mit Namen `secus-space-test` und fünf Chips (der Seed hat nur kurze Namen), gemessen wird also die CSS-Regel, nicht Daten. |

## Block feedback — B8: Ladezeit beim Space-Wechsel (P9-132)

> Lock **P9-BO**. Stand **gemessen 2026-10-08, kein Fix gebaut — Befund auf die P10-Liste.**

| Nr | Kriterium | Stand | Beleg |
|---|---|---|---|
| **P9-132** | V190 gemessen; Fix mit Vorher/Nachher **oder** Befund mit Begründung auf der P10-Liste | ✅ | **V190 beantwortet (Befundzweig).** `scripts/p9_feedback_b8_messung.py` (`probes/p9_feedback_b8_messung.json`), drei Läufe je Richtung, echter Browser: ein Space-Wechsel fordert **genau eine** Anfrage, `/items?space=…`, **12–20 ms** (Liste nach 44–46 ms); `/overview` + `/spaces` laufen **nicht** mit — in einem von sechs Läufen erschienen sie, weil der 20-s-Poll zufällig feuerte, und sie laufen parallel. **Begründung gegen einen Fix:** gegen die Wegwerf-Instanz ist der Wechsel eine lokale Anfrage; die gefühlte Wartezeit ist die **Netzstrecke** (P9-15: `/overview` ~3,1 s über Funnel), und die ist vom Entwicklungsrechner aus nicht zu messen, ohne die echte Instanz zu berühren (Nikinger). Der einzige Hebel am Client wäre ein Zwischenspeicher je Space (alte Liste sofort zeigen, im Hintergrund auffrischen) — das ist eine Designänderung mit Berührung von Auswahl, offenem Editor und Konfliktpfad, kein gezielter Fix. **P10-Liste:** (1) `/items`-Latenz über Funnel **am echten Browser des Nikingers** messen (Netzwerk-Tab, drei Wechsel), (2) erst danach Zwischenspeicher je Space entscheiden. |

## Block feedback — Abschluss: Bestand und Sichtprüfung (P9-133, P9-134)

> Plan §6. Stand **gemessen 2026-10-08 beim Closeout**, nach dem Deploy `v3.1.4`. Beide Zeilen standen bis
> zum Closeout in **keiner** Tabelle — die Bilanz zählte 132 statt 134 Abnahmezeilen.

| Nr | Kriterium | Stand | Beleg |
|---|---|---|---|
| **P9-133** | `pytest` grün (≥ 1250 + neue), `ui_budget` 5/5, Tabu-Diff §0.3 leer, Gegenläufe rot | ✅ | **`pytest` 1265 passed** im frischen Release-venv des Deploys `v3.1.4` (`deploy.sh`, 234,91 s, Ausgabe im Closeout-Commit) und im Dev-venv auf dem Closeout-Commit `926daa6` nachgemessen (223,84 s) · `ui_budget` **5/5** (173,1 KB von 250 KB) · Tabu-Diff `302b8c1..HEAD -- phase1_storage phase4_auth phase2_mcp` **leer** (E1a fasste nur `phase5_ui/webui/api.py` an, wie §0.3 es für E1 vorsieht) · Gegenläufe je Schritt rot, belegt in den Zeilen P9-121 – P9-137 und in `probes/p9_feedback_*_gegenprobe.json` |
| **P9-134** | Sichtprüfung des Nikingers, acht Bilder | ✅ | **Nikinger-Aussage beim Closeout 2026-10-08: abgenommen.** Bilder `docs/screenshots/p9_feedback_*.png` (neun Dateien: B1, B2, B3, B4, B5, E1a, B7 bei 1440/1024/390); die eine Nachbesserung aus der Sichtung (B4: „Entfernen" rechtsbündig) steht in P9-130 |
