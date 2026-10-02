---
status: live
purpose: Verzeichnis der **aktuellen** Phase — Schnellzugriff für Nikinger, kein Grabbing in `docs/screenshots/<phase>_*`
read-when: Nikinger will die jüngsten Sichtprüfungs-Screenshots sehen, ohne durch die History zu scrollen
detail: L3 (Pointer-Verzeichnis, keine eigene Inhaltsquelle)
up: ../phase9_hardening/CLAUDE.md   # aktive Phase
down:
  - ../docs/screenshots/                # kanonische Ablage; diese Verzeichnis ist nur Symlink-Komfort
updated: 2026-10-02 (Rotation auf die `p9_doing_*`-Belege: vier Symlinks neu, die drei `p9_btn2_*`-Links raus — der Knopfoptik-Fall ist erledigt und abgenommen) | 2026-10-01 (Rotation auf die `.toolbar-btn`-Belege (`p9_btn2_*`): drei Symlinks neu, die drei `p9_step_e_*`-Links raus — Step E ist als Beleg in `docs/screenshots/` erledigt und die aktuell offene Sichtfrage ist die Knopfoptik vor dem Deploy. **Vier unversionierte Tailscale-Kopien** mit Leerzeichen im Namen wandern nach `docs/screenshots/p9_step_a_01..04_*` (Infra-Beleg zu A3, ausdrücklich keine Sichtprüfung), die fünfte Datei `Machines - Tailscale.html` ist gelöscht: leere SPA-Hülle, `tailscale-api-prefetch` = `{}`, kein Bildwert) | updated: 2026-09-28 (Phase **9** — Rotation auf die ersten P9-Bilder: die sieben P8.6-Gate-Symlinks sind weg, drei `p9_step_e_*`-Links rein (P8.6-AK sagt genau das: "sie bleiben stehen, bis P9 eigene Screenshots produziert" — Step E hat als erster P9-Step welche produziert) | 2026-09-19 (Phase 8.6 abgeschlossen — Rotation auf die **Gate-Belege**: sieben Symlinks auf `p86_smoke_*` ersetzen die fünf H-R-3-Links. Das sind die Bilder, auf denen die Freigabe von `v3.0.2` beruht. Bleiben stehen, bis P9 eigene Screenshots produziert.)
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

## Aktueller Inhalt (Phase **9**, fünfter Eimer „In Arbeit", Stand 2026-10-02)

Vier Bilder aus `phase9_hardening/scripts/p9_doing_self_check.py` gegen die **eigene**
TLS-Wegwerf-Instanz (`p9_doing_wegwerf.py`, Port 18776, Chromium 1440x900). Sie zeigen den Block,
der die Voraussetzung für den Deploy `v3.1.0` war: eine Aufgabe mit `status: doing` bekommt einen
eigenen Navigationsordner, und beim Speichern im Editor springen die Rail-Zähler **ohne Reload**
um.

**Der Beleg ist die Messung, nicht das Bild.** Das Skript prüft 11 Stationen aus dem echten DOM
(`probes/p9_doing_probe.json`, 11/11 grün). Die **Gegenprobe** ist der eigentliche Beleg: mit
zurückgenommenem `_BUCKETS`-Eintrag melden **7 von 11** Stationen rot. **Grün bleiben dabei
S5/S7/S8** — die prüfen die Maschinenebene, und die war schon vorher korrekt; das Loch war rein
navigativ. Das Bild beantwortet die eine Frage, die keine Messung kann: **gefällt es.**

| Dateiname | Original | Checkkriterium |
|---|---|---|
| `01_uebersicht_chip.png` | `../docs/screenshots/p9_doing_01_uebersicht_chip.png` | **Die Übersicht:** die Zeile `alpha` trägt neben „Offen 1“ und „Erledigt 1“ einen Chip **„1 In Arbeit“**. Wichtig: **deutsch**, nicht das rohe Schema-Wort `doing` — genau die eine Ebene, die P9-W übersetzt. |
| `02_rail_fuenf_ordner.png` | `../docs/screenshots/p9_doing_02_rail_fuenf_ordner.png` | **Die Rail mit fünf Ordnern** (oben nach unten): Offen 1 · **In Arbeit 1** · Erledigt 1 · Notizen 1 · Archiv 0. Prüfen: nichts abgeschnitten, nichts überlappt, „In Arbeit“ steht zwischen „Offen“ und „Erledigt“. |
| `03_liste_in_arbeit.png` | `../docs/screenshots/p9_doing_03_liste_in_arbeit.png` | **Der Ordner „In Arbeit“ geöffnet:** enthält genau **eine** Zeile, „Laufende Probe“. Die Brotkrume oben muss `alpha › In Arbeit` zeigen — derselbe deutsche Begriff, nicht `doing`. |
| `04_nach_statuswechsel.png` | `../docs/screenshots/p9_doing_04_nach_statuswechsel.png` | **Der Kernbeleg:** nach dem Speichern eines Statuswechsels `offen → doing` stehen in der Rail **Offen 0** und **In Arbeit 2** — **ohne einen Reload**. Genau daran hängt P9-64. |

**Warum die Wegwerf-Instanz und nicht das echte Gerät:** der Beleg braucht einen reproduzierbaren
Vorher-Zustand (S5 **verbraucht** den Zustand — die offene Aufgabe wird zur laufenden) und einen
Gegenlauf, also zwei Instanzen mit demselben Seed. Am echten Datenbestand wäre beides nicht zu
halten. Für den Gesamteindruck bleibt die Sichtprüfung am echten Gerät nötig — dafür ist der
Augenschein am Deploy-Tag (Mini-Plan §8.5) zuständig.

**Nicht hier, mit Begründung.** Die vier Tailscale-Adminbilder aus A3 (2026-09-30) und die
`.toolbar-btn`-Belege aus dem 2026-10-01 sind versioniert unter `docs/screenshots/p9_step_a_01..04_*`
bzw. `p9_btn2_*` und gehören nicht in die Schnellansicht: die ersteren sind Infra-Beleg ohne
Bildwert, die letzteren sind mit der Standardoptik der Knöpfe erledigt.

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
