---
status: live
purpose: Verzeichnis der **aktuellen** Phase — Schnellzugriff für Nikinger, kein Grabbing in `docs/screenshots/<phase>_*`
read-when: Nikinger will die jüngsten Sichtprüfungs-Screenshots sehen, ohne durch die History zu scrollen
detail: L3 (Pointer-Verzeichnis, keine eigene Inhaltsquelle)
up: ../phase8_6_ui_polish/CLAUDE.md   # aktive Phase
down:
  - ../docs/screenshots/                # kanonische Ablage; diese Verzeichnis ist nur Symlink-Komfort
updated: 2026-09-11 (Konvention etabliert — Phase 8.6 Block B als Erstbefüllung)
---
# `screenshots_latest/` — Schnellzugriff auf die Screenshots der aktuellen Phase

**Was hier liegt:** die Screenshots, die **in der aktuell laufenden Phase** für die
Sichtprüfung relevant sind — als **Symlinks** auf die Originale in
`../docs/screenshots/<phase>_*`. Single source of truth bleibt `docs/screenshots/`;
dieses Verzeichnis ist ein Lese-Komfort, kein Archiv.

**Wann aktualisieren:** zu Beginn jeder neuen Phase (oder am Ende der vorigen) —
die alten Symlinks raus, die neuen rein. opencode/M3 macht das im selben Commit wie
die Doku-Aktualisierung der Phase, kein eigener PR.

**Naming:** durchnummeriert mit kurzem Screenshot-Inhalt im Filename, **nicht** mit
Phase-Tag (der ändert sich beim Phasenwechsel, der Inhalt bleibt). Begründung:
der Nikinger soll die Datei auch ohne Phase-Kontext sofort verstehen.

## Sichtprüfungs-Konvention (Nikinger 2026-09-11, neu)

Wenn opencode/M3 Screenshots aufnimmt, sagt es **immer** zwei Dinge in den Chat:

1. **Dateiname** (was hier in `screenshots_latest/` liegt, nicht der Original-Pfad)
2. **Checkkriterium** (kurz — was der Nikinger auf dem Bild sehen soll, ein bis zwei Sätze)

Das gilt unabhängig davon, ob M3 selbst das Bild mit dem `read`-Tool beurteilen kann —
auch wenn M3's eigene Bewertung positiv ist, ist die **Nikinger-Verifikation** der
Pflicht-Beleg (P8.6-O-Eskalationsregel: ein Build, der nur durch Selbstprüfung eines
bildfähigen Modells abgesichert ist, ist noch nicht live-verifiziert; die
`Sichtpruefung`-Schwester-Datei regelt das vollständig).

Ausnahmen, in denen M3 den Dateinamen + Checkkriterium **nicht** nennt:
- Wenn der Screenshot ein reiner Build-Beleg ist (z. B. „Smoke gegen Wegwerf X
  bestanden, hier der Konsolen-Output als Bild") und M3 den Befund bereits im
  Klartext dokumentiert hat.
- Wenn die Verifikation programmatisch ist (Regex auf gerenderten HTML-Output
  o. ä.) und der Screenshot nur Anhang ist.

## Aktueller Inhalt (Phase 8.6 Block B, Stand 2026-09-11)

| Dateiname | Original | Checkkriterium |
|---|---|---|
| `01_overview_logout_caution.png` | `../docs/screenshots/p86_block_b_01_overview.png` | **Rail-Bottom: "Abmelden" ist rot (Vorsicht-Farbe `var(--caution)`), "Konto" bleibt in Standard-Textfarbe.** Beweis: B4 `action--caution` greift auf `#logout-button`. |
| `02_list_hover_quiet_selection.png` | `../docs/screenshots/p86_block_b_02_list_hover.png` | **Erste Listen-Zeile hat eine leise bläuliche Tönung + 1px-Outline (nicht der volle `--select-fill`-Verlauf wie bei `aria-current`).** Beweis: B1 konsolidierte Hover-Regel greift für `.list__row` ohne `aria-current`. |
| `03_editor_archive_caution.png` | `../docs/screenshots/p86_block_b_03_editor.png` | **Editor offen, "Archivieren"-Knopf oben rechts ist rot, "Speichern"-Knopf daneben weiß.** Beweis: B4 auch auf `#archive-button`, Knopfplastik bleibt erhalten. |
| `04_account_dialog_navigation.png` | `../docs/screenshots/p86_block_b_04_account_dialog.png` | **"Passwort ändern"-Dialog offen: "Update-Log ansehen" und "Spaces verwalten" sind Navigation (kein Knopfplastik-Hintergrund, leiser Hover-Outline), "Ändern"/"Abbrechen" sind weiterhin die echten `.btn`/`.btn-primary`.** Beweis: B3 `.account-nav`-Klasse statt `.btn`-Plastik. |

**Bonus für den Nikinger:** oben links in `01_overview_logout_caution.png` ist auch
der `update-banner` zu sehen (P6-Step-3-Eintrag vom 2026-09-11) — separate
Verifikation, nicht Teil von Block B, nur weil das Banner zufällig da ist.

## Rotation

Beim Phasen-Wechsel (z. B. Phase 8.6 → Phase 8.7/P9):

1. Neue Screenshots unter `docs/screenshots/<new_phase>_*` aufnehmen.
2. Alle alten Symlinks hier löschen.
3. Neue Symlinks hier anlegen, mit dem Nummerierungs-Schema der neuen Phase
   (z. B. `01_...`, `02_...`).
4. Diese README.md aktualisieren mit der neuen Tabelle + Checkkriterien.
5. Im selben Commit den `updated:`-Eintrag oben ergänzen.

opencode/M3 macht das **selbst** ohne Rückfrage — es ist Teil der
Phase-Closeout-Pflichten, kein Nikinger-Auftrag.
