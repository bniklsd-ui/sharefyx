---
status: archive
purpose: L3-Archiv der am 2026-10-22 aus `docs/INDEX.md` gekürzten Texte — die Abschnittsköpfe und die Kartenzeilen, die dort standen, verbatim. Die Karte trägt wieder Stand, dieses Archiv trägt die Chronik des Kürzens.
read-when: beim Audit, wenn eine alte Kartenzeile rekonstruiert werden muss, oder wenn die Herleitung einer Zahl aus der Karte gesucht wird, die am 2026-10-22 dort verschwand
detail: L3
up: ./INDEX.md
down:
updated: 2026-10-22 (angelegt — P10.5 Block 0, Schritt 0.5, DO-2: die Karte brauchte Luft; der Plan nannte als Hebel die Abschnittsköpfe, gemessen tragen die acht Köpfe zusammen 2.478 B, aus den Köpfen allein waren die geforderten 3.000 B nicht erreichbar — deshalb wandern auch drei Kartenzeilen-Chroniken hierher)
---
# Kürzungs-Archiv der INDEX-Karte

> **Was hier steht:** die Texte, die am 2026-10-22 aus `docs/INDEX.md` gewandert sind — **verbatim**,
> byteweise identisch, ungekürzt. Zwei Arten: die **Abschnittsköpfe** der abgeschlossenen Phasen und
> drei **Kartenzeilen**, deren Rest Chronik war (Herleitung, Messreihen, Befundgeschichten).

**Warum.** Die Karte stand am 2026-10-21 bei 40.772 B gegen die harte Grenze 40.960 B
(`phase9_hardening/tests/test_index_archive.py`): 188 B Luft, und jede Phase kostet eine Zeile.
Der Plan P10.5 (Schritt 0.5, DO-2) verlangt **≥ 3.000 B Luft**. Der Plan nannte als Hebel die
**Abschnittsköpfe** — **gemessen tragen die acht `## Phase …`-Zeilen zusammen 2.478 B**, und mit
einer neuen Zeile von ≤ 120 B ist die Ersparnis höchstens ~1,7 B. Aus den Köpfen allein war die
Plan-Zahl **nicht erreichbar** (der Plan nannte „P8.6 allein ~600 B" — das stimmt: 617 B; nur die
Summe fehlte). Deshalb wandern zusätzlich drei Kartenzeilen-Chroniken hierher.

**Was die Karte jetzt trägt:** Glyph, Größe, Ein-Satz-Stand, Zeiger. Nicht mehr die Herleitung.

**Nichts ist verloren.** Das Skript `phase10_5_finishing/scripts/shorten_index_headings.py` prüft
vor dem Schreiben, dass jede alte Zeile **genau einmal** in der Karte vorkam, dass die Karte mit
den alten Zeilen zurück **byte-identisch** rekonstruiert werden kann, dass jede verschobene Zeile
**byte-identisch** hier steht und dass die Ersparnis ≥ 3.000 B ist; bei jeder Abweichung bricht es
ab, **ohne eine der beiden Dateien anzufassen**.

**Verwandt:** `docs/INDEX_ENTRIES_ARCHIVE.md` trägt die **datierten Nachträge** (43 Einträge, seit
2026-10-03), `docs/INDEX_UPDATES_ARCHIVE.md` die `updated:`-Kette der Karte. Drei Archive, drei
verschiedene Fragen: Nachtrag, Kette, Kürzung.

## Abschnittsköpfe vor der Kürzung (2026-10-22), verbatim


> **Aus der Karte verschoben (2026-10-22, P10.5 Block 0 Schritt 0.5 — DO-2), verbatim:**

```
## Phase 10 — ✅ abgeschlossen 2026-10-20 (Bestandsaufnahme, kein Produktcode). P10 und P10.5 sind eine Mission: Plan P10.5 freigegeben, Tor P10-8 offen (2026-10-21). Phasenziele: Anbieter-Unabhängigkeit, Karten-Umbau (Gehirnkarte)
```

```
## Phase 8.6 — ✅ abgeschlossen 2026-09-19, Step Z inklusive; live als `v3.0.2` seit 2026-09-18 (SHA `1ad2665`, `health_gate` 9/9). UI-Politur mit **zwei Plaenen und drei Sichtungs-Revisionen**: Plan 1 (Step 0/V/A/B/C/D) wurde am 2026-09-12 nicht abgenommen — neun UX-Befunde statt Freigabe —, Plan 2 (E/F/G/**G-R**/H/**H-R**/**H-R-3**/J) hat sie abgearbeitet. Bilanz **45 ✅ · 5 ⚠️ · 0 ⬜ · 4 ersetzt** von 54 Zeilen; `pytest` **995**, `ui_budget` 5/5 (144,7 KB); **keine neunte P1-Contract-Oeffnung**, eine angekuendigte Tabu-Ausnahme (P8.6-AJ). Zwei `[VERIFY]` gehen offen an P9: **V118**, **V136**
```

```
## Phase 8.5 — ✅ abgeschlossen 2026-09-09, Step Z inklusive (Link-Picker-Politur, Titel-statt-ID-Hint, v3-Vorabritt + Deploy; schließt Phase 8 formal mit ab; Bilanz **20 ✅ · 0 🟡 · 0 ⬜**; Statusregel geändert — vom Nikinger geprüfte Wegwerf-Automatisierung zählt als live-verifiziert; Closeout kanonisch in Plan §9, Einstieg für P8.6 über `PHASE8_5_CLOSEOUT_HANDOVER.md`; Folgephasen P8.6 → v3.0.2 + P9 → v3.1.0 vorgemerkt)
```

```
## Phase 9 — ✅ abgeschlossen 2026-10-08; live als `v3.1.4` seit 2026-10-08 (SHA `d04c0ec`, `health_gate` 9/9). Härtungsphase: acht Steps (0 Doku-Fundament · A eigene Domain über VPS · B Watchdog · C Vision auf der RTX 3060 · D zwei Bugs · E Karten-Reload · F Schema `doing`/`assignee` · G Löschen nach `._trash/` · H `fastmcp`-Pin) plus sieben Blöcke (doing · trace · Buttons · settings · drei Bildsichtungen · feedback). 134 Abnahmezeilen, Bilanz in `ABNAHME_MATRIX.md`; zwei angekündigte P1-Öffnungen; Einstieg für P10: `PHASE9_CLOSEOUT_HANDOVER.md`
```

```
## Phase 8 — ✅ abgeschlossen 2026-09-08 (UI-Neuanstrich v3, Verknüpfungs-Graph, drei P7-Erbposten; Bilanz 26 ✅ · 0 🟡 · 0 ⬜ — maschinell gezählt; Closeout vollzogen im selben Commit wie Phase 8.5, kein separates Handover-Dokument, Konvention seit P7)
```

```
## Phase 7 — ✅ abgeschlossen, live-verifiziert (`e88a624`, 22 von 24 Abnahmezeilen, 2 benannte Defekte an P8 vererbt)
```

```
## Phase 6 — 🟡 code-complete, nicht vollständig live-bewiesen (Restarbeiten: Fabian-Sitzung, §9 Mehrfachauswahl, Doku-Audit)
```

```
## Phase 6.5 — 🟡 code-complete, 13/14 live bestanden (P6.5-14 strukturell offen)
```

## Kartenzeilen vor der Kürzung (2026-10-22), verbatim
> **Aus der Karte verschoben (2026-10-22, P10.5 Block 0 Schritt 0.5 — DO-2), verbatim:**

- [docs/INDEX.md](./INDEX.md) — 🔗 **diese Karte** (L0) · **38.288 B — unter dem 40-KiB-Softcap** (V145 ✅ seit 2026-10-03; **Nikinger-Entscheidung 2026-10-03: die datierten Nachträge wandern nach `docs/INDEX_ENTRIES_ARCHIVE.md`, das Kriterium von 38.912 B (P8.6 Plan 2 §1.2) auf den 40-KiB-Softcap neu baseliniert** — die 38.912 B waren für eine Datei mit weniger Zeilen gesetzt und waren **per Kürzen unerreichbar**: gemessen waren 71.573 B, davon **37.391 B Nachträge in 43 von 93 Einträgen**, und selbst 300 B je Zeile hätten 39.971 B ergeben. Verschoben per `scripts/archive_index_entries.sh` mit fünf Gegenproben, darunter die byteweise Reassemblierung des Originals; **4 Gegenproben des Skripts rot** (Schnitt mitten im Satz · `**` am falschen Ort · im INDEX vergessener Nachtrag · der Zeiger als Markdown-Link, den `doc_health` für die INDEX-Zeile des Archivs hielt) · **Wächter**: `phase9_hardening/tests/test_index_archive.py` — harter Größen-Gate, kein Nachtrag im INDEX, Archiv vollständig) · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**

- [phase9_hardening/step_b/RUNBOOK_STEP_B.md](../phase9_hardening/step_b/RUNBOOK_STEP_B.md) — 📗 ~26KB · **der geführte Step-B-Ablauf B0–B3** (tailscaled-watchdog installieren und live beweisen) mit **drei gemessenen Befunden, die den Plan §4 korrigiert haben**: **der `sudoers`-Weg ist unbaubar** (die Unit setzt `NoNewPrivileges=true`, sudo lebt vom setuid-Bit — `setpriv --no-new-privs -- sudo -n -l` → *"no new privileges" flag is set*) · **die Box kennt nur die grobe polkit-Aktion** (`systemd 255.4`: `manage-units` für Start/Stop/Restart, man `org.freedesktop.systemd1(5)` §Security), ein `<defaults>`-Eintrag kann **nicht** nach Unit filtern · **die Units sind auf der VM noch nicht installiert** (`/etc/systemd/system/tailscaled-watchdog.*` fehlt, `list-timers` = 0). **V153 damit entschieden** (polkit) — ob systemd 255 das `unit`-Attribut mitschickt, war unprivilegiert nicht auslesbar (`pkcheck` → *not registered*) — **B0 hat es gemessen: `AUTORISIERT`**, Journal-Beleg bei `User=root` ⇒ die enge Regel trägt. Nebenbefund: eine Verweigerung kostet hier 25 s (kein polkit-Agent, headless). · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**

- [phase8_ui_graph/CLAUDE.md](../phase8_ui_graph/CLAUDE.md) — 📗 ~47KB — **6.901 B ÜBER dem 40-KiB-Softcap, benannt statt versteckt** (P8-P; **war schon auf HEAD
über der Grenze** (45.365 B), die alte Angabe `~43KB` lag nur noch im Toleranzfenster des Wächters;
die zwei B17-Korrekturen kosten +2.496 B, der Rest ist gewachsene Phase-8-Chronik — **die Lösung ist
die Rotation, kein Kürzen**) · Phase-8-Head, alle Bloecke ✅, Phase formal ✅, Abnahmestand **26 ✅ · 0 🟡 · 0 ⬜**. Traegt die **Selection/Choice-Konvention v3**, seit P8.6 Block A mit fuenfter Kategorie Vorsicht
(`.action--caution`) — deshalb bei jedem UI-Commit zu lesen · **Nachtrag: `docs/INDEX_ENTRIES_ARCHIVE.md`**

- [docs/INDEX_ENTRIES_ARCHIVE.md](./INDEX_ENTRIES_ARCHIVE.md) — 📦 **45.703 B** · L3-Archiv der **datierten Nachträge aus den Einträgen dieser Karte**, verbatim, ein Abschnitt je Karte in der Reihenfolge der Karte (nicht newest-first — wer einen Nachtrag sucht, sucht ihn über den Dateinamen, nicht über ein Datum). Angelegt am 2026-10-03, weil die Karte bei **71.573 B** stand und **37.391 B** davon Nachträge in 43 von 93 Einträgen waren — mehr als die Hälfte, und die seit Wochen als ungeklärt geführte Ursache der Überschreitung (P9-3/V145). **Die `updated:`-Kette der Karte ist nicht die Restmasse: 1.155 B, am 2026-10-03 rotiert** — wer die Datei rotieren wollte, hätte die falsche Stelle angefasst. Verschoben per `scripts/archive_index_entries.sh` (fünf Gegenproben, darunter die byteweise Reassemblierung des Originals und „kein datierter Nachtrag bleibt im INDEX", die Verschieben von Weglassen unterscheidet); **vier Skript-Gegenproben waren rot, bevor es lief** — die Liste in `phase9_hardening/tests/test_index_archive.py`. **Regel für die nächste Session:** eine Kartenzeile bekommt wieder einen datierten Nachtrag, *wenn* er kurz ist — `test_no_entry_line_carries_a_dated_addendum_any_more` verbietet sie vollständig, und das ist Absicht: die Karte ist Stand, das Archiv ist Chronik

