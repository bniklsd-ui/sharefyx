---
status: live
purpose: Phase-10.5-Head — Modulstatus der Blöcke 0–13/Z, Deploy-Tabelle A–D, Abnahmestand P10.5-1–64, offene Punkte beim Nikinger, aktueller Session-Block. Plan und Arbeitsliste stehen in eigenen Dateien.
read-when: Arbeiten in phase10_5_finishing/ — zuerst lesen, zusammen mit dem Session-Block unten
detail: L2
up: ../ROADMAP.md
down:
  - ../docs/concepts/phase10_5_finishing_plan.md    # 📕 der Plan: Locks P10.5-A–W, Blöcke 0–12/Z, Abnahme, [VERIFY] V207–V219
  - ../phase10_inventory/BAUSTELLENREGISTER.md      # 📗 die Arbeitsliste — hier wird abgehakt (P10-B)
  - ../phase10_inventory/ENTSCHEIDUNGEN_ARCHIVE.md  # 📦 §12 Entscheidungsliste D-1–D-18, verbatim
  - SESSIONS_ARCHIVE.md                             # 📦 ältere Session-Blöcke, verbatim, newest-first
  - UPDATES_ARCHIVE.md                              # 📦 die älteren `updated:`-Fäden dieses Heads, verbatim
  - STARTUPTRAG_ARCHIVE.md                          # 📦 die Startaufträge der Blöcke 7 und 9, verbatim
  - MODULSTATUS_ARCHIVE.md                         # 📦 die ausführlichen Statusspalten der Blöcke 0–10, verbatim
  - ABNAHME_ARCHIVE.md                             # 📦 die geschlossenen Abnahmezeilen (P10.5-1–72), verbatim
  - FREIGABEN_ARCHIVE.md                           # 📦 die Freigaben der Phase, verbatim
updated: 2026-10-30 (Block 15.5c: Titel ≤ 256 Zeichen; Live-Durchsicht 0 Treffer; Session-Ende) | 2026-10-30 (Block 15.5b: Verwalten-Knöpfe nur bei `manageable`) | 2026-10-30 (Block 15.5: B6/B7 — Space-Name eine Regel, Slug ≤ 100 Byte) | 2026-10-30 (Block 15.4b: B4′ + Selbst-Austragen; E1 überholt) | 2026-10-30 (Block 15.4: B4 geschlossen, P10.5-78 ✅) | 2026-10-30 (Block 15.3b: `share_*`-Skalar = eine Freigabe, E5 gebaut) | 2026-10-30 (Session-Ende: E5 = A entschieden, nächste Session 15.3b → 15.4) | ältere Einträge: phase10_5_finishing/UPDATES_ARCHIVE.md
---
# Phase 10.5 — Finishing

> **Auftrag:** P10.5 schließt jede Baustelle, die im Register als „Ziel P10.5" steht — Betrieb, Fehler, Parität, Performance, MCP-Schicht, Anbieter-Unabhängigkeit, Darstellung, Gehirnkarte, Umbenennen, Suche, Realtime, Editor Stufe 1+2 und Doku. Die Phase endet erst, wenn ein Nicht-Claude-Client live `list_spaces` ausführt, mit zwei Modellanbietern (P10-J); neues Feature kommt erst in P11.

## Freigaben
> **Verbatim verschoben** nach `FREIGABEN_ARCHIVE.md` (`scripts/move_sections.py`) — dort unter derselben Überschrift.

## Modulstatus

| Block | Inhalt (Register) | Wer | Deploy | Status |
|---|---|---|---|---|
| 0 | Haushalt: Verifikation, Phase-Head, INDEX-Luft, Register-Luft, DO-2, DO-3, Ausführer-Vorbedingung | Claude Code | — | ✅ 2026-10-22 |
| 1 | Betrieb: BT-1, BT-2, BT-6 (+ `constraints.txt`) | Ausführer + Nikinger | A | ✅ 2026-10-22 |
| 2 | Fehler, Parität, Regel: BG-1, RE-1, RE-2, P10-I, AL-1 | Ausführer (+ Claude Code Proben) | A | ✅ 2026-10-22 |
| 3 | Hygiene: LG-8 (P1-15), LG-7 | Ausführer | A | ✅ 2026-10-22 |
| 4 | Performance: PF-1, PF-4, Z1–Z4 | Ausführer (+ Claude Code Proben) | A | ✅ 2026-10-22 |
| 5 | MCP-Schicht: PA-5 (FastMCP 4), LG-4 | Ausführer | B | ✅ 2026-10-22 |
| 6 | Anbieter: PA-1, PA-2, `/mcp`, PA-6, P10-J | Ausführer + Claude Code + Nikinger | B | ✅ 2026-10-22 |
| 7 | Darstellung: UI-1–UI-6, KA-5 | Ausführer (+ Claude Code Sichtung) | C | 🔄 2026-10-24 |
| 8 | Karte: Gehirnkarte C2 | Ausführer (+ Claude Code Smoke/Sichtung) | C | 🔄 2026-10-24 |
| 9 | Rechte und Namen: RE-7 (P1-12), RE-4 (P1-13), RE-3 (P1-14) | Ausführer | D | ✅ 2026-10-24 |
| 10 | Suche und Realtime: LG-1, LG-2 | Ausführer (+ Claude Code Proben) | D | ✅ 2026-10-24 |
| 11 | Editor Stufe 1 + 2: ED-1, ED-2, ED-3 (P1-11), ED-5 | Ausführer (+ Claude Code Proben/Sichtung) | D | 🔄 2026-10-24 — **11.1 Vendor** (CodeMirror 5.65.16, **fünf** Dateien statt drei — gemessen: der UMD-Browser-Zweig der `markdown.min.js` löst `require("../xml/xml")` **nicht** auf) · **11.2 Nachlader** (`js/editor_cm.js`: CSS → Kern → Modus-Dateien, Promise gecacht, Fehler → `null` = Textarea/Rohmodus) · **11.3 Live-Editor** (`editor.js`: `getBody()`/`setBody()`, `setRawMode(on)`, Schalter „Rohtext", Probe 12/12 grün) · **11.4 Live-Darstellung** (V211 **gemessen**: `visibility: hidden` hält die Cursorposition, `display: none`/`font-size: 0` rücken sie 2 Zeichen vor; Probe 15/15 grün) · **11.5 To-do-Kästchen** (ED-2: `cm.markText(…, {replacedWith: <checkbox>, atomic: true})` — der **Text** bleibt die Quelle; Klick bei sauberem Editor speichert **sofort** mit `version`, bei geändertem nur der Puffer; Lesesicht **deaktiviert**; Probe 8/8 grün, Gegenlauf bricht genau die Schreibzelle) · **11.7 Budget** (`ui_budget.py`: `static_payload_files()` — **jede Datei genau einmal**; Erstaufruf **209,3 KB** ≤ 250 KB, Editor **69,7 KB** ≤ 80 KB; Wächter `tests/test_budget_coverage.py` mit Gegenprobe) · **11.8 Roundtrip** (V201-Rest: die **zehn** M7-Fixtures **10/10 byte-identisch**, Öffnen macht den Editor **nicht** geändert, Dateien auf der Platte byte-identisch) · **11.6 Format-Konvention** (ED-3: `markdown.js` — Vokabular **Farbe** (rot/blau/gruen/gelb) · **Größe** (klein/normal/gross) · **Ausrichtung** (links/zentriert/rechts); Inline `[Text]{.rot}`, Block `::: {.zentriert}` … `:::`; eine **unbekannte** Klasse bleibt **wörtlich**; der Sanitizer lässt `span`/`div` nur mit Klassen aus der festen Menge durch; die **Codespans** sind ausgeschnitten (darin wird **nichts** formatiert — das behebt einen Alt-Fehler); Editor: drei Felder in der Werkzeugleiste + ein **CM5-Overlay**, das `[…]{.rot}` schon beim Schreiben färbt; MCP: `_FORMAT_HINT` **wörtlich identisch** an allen fünf Body-Schreib-Werkzeugen; Probe `probes/p105_b11_markdown_probe.py`: **9/9 Zellen grün**, der Gegenlauf bricht genau die Zelle „unbekannte Klasse wörtlich“) |
| 12 | Doku und Altlasten: DO-1, LG-6, AL-1 (Rest), AL-3, BG-2/BG-3 | Claude Code | — | ✅ 2026-10-25 — **DO-1** (die drei Heads: 8.6 109.230 → 23.614 B, 8 47.861 → 34.225 B, 6 41.032 → 34.801 B; verbatim per `move_sections.py`, die 33-KB-Kette von 8.6 per Skript in `UPDATES_ARCHIVE.md`) · **LG-6** (`ROADMAP.md` 37.197 → 26.457 B, Phase 8.5 → `docs/ROADMAP_ARCHIVE.md`) · **AL-1/AL-3** (P6-Nachzug in `phase6_shares/CLAUDE.md`) · **BG-2/BG-3** (P9-124/127 ⚠️ → ✅, Bilanz 123/10/1) · **Register-Bilanz** per `scripts/register_bilanz.py` (46 P10.5-Zeilen: 40 ✅ · 6 ⬜) |
| 13 | Aufträge des Nikingers: UI-8 (die Größen wirken live), UI-9 (die Knopfleiste nach Word), UI-10 (die Knopffarben) | Claude Code (Sichtung Nikinger) | D | ✅ 2026-10-25 — **13.1** (die Stufen wirken im **Live-Editor**: Basis 13 px, `klein` 11,05 px, `normal` 13 px, `groß` 15,6 px; die **Zeilenhöhe bleibt 21 px** in allen drei Stufen — die Ursache war die Prozent-`line-height`: CM5 rechnet `defaultTextHeight` **einmal** (aus 50 Zeilen); der Overlay liefert Farbe **und** Größe in beliebiger Reihenfolge) · **13.2** (die Leiste: **fünf** Gruppen in Words Ribbon-Reihenfolge, alle Knöpfe 26 × 24 px, Trenner dazwischen, **keine** HTML-Entity-Zeichen als Icons; **B** und **I** bleiben Buchstaben; die fünf neuen Icons aus dem Lucide-Tarball **1.38.0**, SHA-256 **verifiziert**) · **13.3** (die Fläche: `--btn-std-fill` = `rgba(62,141,243,.20)` — die **datierte Umkehr** der P9-Entscheidung vom 2026-10-01; `--caution` `#F06A6E` → **`#FF8A8E`**, Kontrast **nachgerechnet**: 4,76:1 statt 3,59:1) · **13.4** (die **ganze** Karte: 1920 × 1200, Zoom 50 % — die Welt der Knoten vollständig im Bild) · Probe `probes/p105_b13_knopfleiste_probe.py` **8/8 grün**, der Gegenlauf **5 Zellen rot**; Wächter `tests/test_knopfleiste_word.py` (9) und `tests/test_contrast.py` (3) grün · **Fund:** `i-chevron-left` stand im Sprite, die Quelldatei war **nie** vendored — der Sprite war damit nicht aus dem Bestand reproduzierbar; nachgetragen und **alle 25** vendored Dateien byteweise gegen den Tarball geprüft |
| 14 | Kartenlayout „zufällig, aber geordnet“ (Nikinger 2026-10-26) — Plan `docs/concepts/phase10_5_block14_kartenlayout_plan.md` | Ausführer (opencode) + Claude Code (Bilder) | D | ✅ 2026-10-29 (Sichtung P10.5-70 abgenommen) — **vorher** 🔄 2026-10-28 — **14.0–14.5 gebaut und gemessen** (die Herleitung **verbatim** im L3-Anhang `docs/concepts/phase10_5_block14_kartenlayout_plan_anhang.md`, den Anmerkungen der Schritte 14.0–14.4): Determinismus **0,0 px** · Regionen **152/152 = 100 %** · Stabilität Median **0,0 px** · Budget **201** Knoten in **2147 ms**, **0** Frames · Kamera Füllgrad **91,1 %**, Versatz **0,49 px** · Beschriftungen **0** überlappende Paare (13 Kandidaten, 10 gezeichnet) · **14.5: die drei Kartenbilder** (`docs/screenshots/p105_b14_karte_0{1,2,3}_*.png`) und **der Rand-Fall aus §2.5 gemessen**: die Lappen-Kontur stand **3,8 px** über dem Leinwandrand ⇒ **`FIT_MARGIN` 40 → 56 px** (die 8 px Luft über `LOBE_REACH` = 48 px), jetzt **10,7 px** Luft, **kein** Beschnitt; Füllgrad **93,6 % → 91,1 %**, Zoom **92 % → 90 %** · Wächter `tests/test_b14_layout_probe.py` (18) + `tests/test_b14_karte_bilder.py` (7) · **Nachzug 14.5 (2026-10-28): die Lappen-Kontur am Rasterrand war offen** (`traceContour()` liess die Randkante weg → Bruchstücke mit Sehnen, sichtbar am linken Lappen) — behoben, Bilder neu, Luft links **7,2 px**, Wächter `tests/test_lobe_kontur_geschlossen.py` (2); Update-Log-Zeile geschrieben · **P10.5-70 wartet auf die Sichtung** · **14.6.0 ✅ (2026-10-28): die Basislinie der Karte gemessen** — die neue Zelle `koerper` ist **rot**: der Körper besteht aus **5** Komponenten (1815/1670/1656/1651/1538 Zellen), es gibt **0** Furche-Zellen und **0** Paare (je Space **1** Lappen); Raster 156 × 125, Zellgröße **8 px**; kleinster Abstand zweier Spaces **183,0 px**; `computeLobes()` **20,1 ms** (152 Knoten) · **35,0 ms** (201 Knoten, Grenze 50 ms) · Plan `docs/concepts/phase10_5_block14_6_plan.md` (Schritt 14.6.0, Anmerkungen dort) · **zwei Durchgänge** (Bilder/Rand **ungepatcht**, Zahlen/Zeit **gepatcht** über ein Messpflaster in einer Kopie von `graph.js`) — die Bilder blieben **byteweise identisch**; Wächter `tests/test_b14_karte_bilder.py` (16) · **14.6.1 ✅ (2026-10-28): der Algorithmus und die sechs Varianten** — das Schließen der Körpermaske (Polster · Wachsen · **exakte** Distanztransformation · Körper = geschlossen ∪ Maske), **kein Knoten bewegt sich**; die **Regressionsprobe** ist erfüllt: bei `LOBE_CLOSE_PX = 0` sind die drei Bilder **byteweise identisch** mit den drei im Repo · Varianten 0/80/120/160/200/240 gemessen: **160** ist der kleinste Wert mit **einer** Komponente (80 und 120: **drei**), Reach **unverändert** (48,4 px), Zeit **28,4 ms** (152) · **36,3 ms** (201 Knoten, Median aus fünf Aufrufen, Grenze 50) — **ab 200 werden die Lappen von der Furche aufgefressen** (Reach rechts **−3,9 px**, oben **−89,5 px** bei 240; bei 240 ist die 52-px-Grenze **gerissen**) · Beleg `probes/p105_b14_6_varianten_messung.json`, Bilder **außerhalb** des Repos · Wächter `tests/test_lobe_schliessen.py` (4, die Distanztransformation gegen die Brute-Force) · **STOPP — E1 (Wahl des Werts) beim Nikinger** — **14.6.2 ✅ (2026-10-28): der Wert steht (`LOBE_CLOSE_PX = 160`, vom Nikinger nach der Standardregel des Plans entschieden) und der Wächter beißt** — die neue C2-Messung `koerper` misst an einem **zweiten** festen Eingang (`KOERPER_POSITIONEN`: die drei Gruppen berühren sich bei `0` **nicht**), Normalfall **1** Komponente / **3** Lappen / **53** Furche-Zellen, der Gegenlauf `koerper` (`LOBE_CLOSE_PX` → 0) macht **3** Komponenten daraus und **nur** diese Messung rot — der Browser bestätigt **1** Komponente, **146** Furche-Zellen, Reach **47,9 / 44,1 / 48,4 / 44,6 px**, Luft **7,2 / 10,7 / 82,9 / 85,6 px**, Zeit **29,7 ms** (152) · **43,0 ms** (201) · **14.6.3 ✅ (2026-10-28): die Belege neu — das Layout ist unberührt (alle sechs Messungen der Layout-Probe **identisch**, bis auf drei Tintenpixel: 7250 → 7253), die `koerper`-Zelle ist **grün** (**1** Komponente, **1** Lappen je Space, **146** Furche-Zellen, **4** Paare, Reach **47,9 / 44,1 / 48,4 / 44,6 px**, Luft **7,2 / 10,7 / 82,9 / 85,6 px**, `computeLobes()` **30,8 ms** (152) · **34,6 ms** (201)), die **drei Bilder im Repo sind ersetzt** (byteweise identisch mit den Variantenbildern 160), die Karten-Probe **alle Messungen grün** — **P10.5-72 ✅** (Summe **64 ✅ · 0 ⚠️ · 8 ⬜ von 72**); Wächter `tests/test_b14_karte_bilder.py` prüft jetzt die **Kriterien** statt der Basislinien-Zahlen (19 Tests, zwei neue Gegenproben) · **14.6.4 (2026-10-29, Claude Code):** Update-Log-Zeile ✅ (Z. 19: „ein zusammenhängendes Gebilde, jeder Space als eigener Bereich darin“); **Vorbefund zur Sichtung P10.5-70** im Session-Block — das Urteil bleibt beim Nikinger · **14.7 geplant (2026-10-29):** kompakt + verteilt + glatt — Plan `docs/concepts/phase10_5_block14_7_plan.md`, Ausführung **Claude Code** (Nikinger-Entscheidung), nächster Schritt **14.7.0** (Messung zuerst) · **14.7.0 (b) STOPP (2026-10-29):** die Stabilitätsbrüche aus 14.4 sind **Chaos** (Lappen sortieren sich innen um, Schwerpunkte ≤ 6,2 px), **kein Überlauf**; die Dichte setzt das Kräftegleichgewicht, nicht der Seed (Lappenradius 100–119 px bei `ITEM_STEP` 14, 100–123 px bei 20) — `SPREAD` nach §2.2 wird **nicht** gebaut, Beleg `probes/p105_b14_7_ursache_b4.json` · **14.7.0 ✅ (2026-10-29):** Nikinger: Empfehlung **A** — §2.2 neu als `LOBE_SCALE` (Gleichgewicht im Lappen ×s, selbstähnlich); Basislinie der Form: Solidität **0,497**, NN **25,1 px**, Zusatzkrümmung **11,10 rad/100 px**, Konturabstand **8,0 px**, Querbahnen außen **29,5 %**; Zeilen **P10.5-73/74** ⬜; Wächter `tests/test_b14_7_form.py` · **14.7.1 ✅ (2026-10-29):** `ANCHOR_LAYOUT`/`ANCHOR_HEX_ORDER`/`LOBE_SCALE`/`LOBE_SMOOTH_PASSES` in `graph.js`, Nullwerte = Block 14 (Layout-Probe gleich, Bilder byteweise gleich); H1–H5 grün, Gegenlauf `ring` rot an H1+H2; Wächter `tests/test_b14_7_hex.py` · **14.7.2 🔄 STOPP E1 + E2 (2026-10-29):** Raster 9 + 12 Läufe (`probes/p105_b14_7_raster.json`) — strenge Stabilität (Max ≤ 3 px) hält nur heute; Kandidat **hexg_s1.5** (Solidität 0,830, NN 36,0 px, Median/Max 1,0/9,1 px, Zelle 68 grün) + Glättung **2**; **Fund behoben:** Kontur zerfiel bei krummer Zellgröße (betrifft auch heute), Wächter `tests/test_b14_7_kontur_zellgroesse.py` · **14.7.3/14.7.4 ✅ (2026-10-29):** Nikinger nimmt `hexg_s1.5_glatt2` ab („das nehme ich ab“) — Werte gesetzt, Repo-Bilder **byteweise gleich** dem abgenommenen Bild; alle Layout-Zellen grün; **Befund A** (Marge 21,8 px) akzeptiert; **Befund B (b):** Gegenläufe `region` (Index-Permutation) und `beschriftung` (Zoomszene, 57 Paare ohne Regel) neu gebaut · **14.7.5 ✅:** P10.5-73/74 ✅, Update-Log Z. 19 neu · **P10.5-70 ✅ (2026-10-29):** alle drei Bilder vom Nikinger abgenommen — Block 14 **fertig** |
| 15 | Fixes aus dem Ultra-Review B1–B10 — Plan `docs/concepts/phase10_5_block15_review_fixes_plan.md` | Claude Code | D | 🔄 2026-10-30 — **15.1 ✅** B1/B15 (`asset_id` nie roh zum Pfad: `Store._asset_matches()`, `\Z`; 9 Wächter, Gegenlauf 9 rot; P10.5-75 ✅) · **15.2 ✅** B2/B3/B20 (Dienststart scheitert nie an Daten: Rebuild je Datei + eine Transaktion, Elternordner, Wiederaufnahme fängt; Gegenlauf 6/5/5 rot; P10.5-76 ✅) · **15.3 ✅** B5/B8 (Lesen nachsichtig, Schreiben streng, kein Fehler nach dem Write; Gegenlauf je Fix rot; P10.5-77 ✅) · **15.3b ✅** E5 (`share_*`-Skalar = eine Freigabe, `WARNING` mit Pfad; Gegenlauf 3/3/2 rot) · **15.4 ✅** B4 (`manages_space` in GET/POST/DELETE der Mitglieder-Routen; Gegenlauf 3 rot; P10.5-78 ✅) · **15.4b ✅** B4′ (`share_*`/`visibility` fremder Home-Space-Items nur mit `manages_space`) + E6 (Selbst-Austragen) · **15.5 ✅** B6/B7 (`files.is_valid_space_name()` in `create`/`move`/`rename_space`/`acl.create_space`; Slug ≤ 100 UTF-8-Byte in `item_filename()`, E3 gemessen: `f_namemax` 255, tmp-Name + 14; Gegenlauf 6/15/1 rot) · **15.5b ✅** UI-Rest 15.4 (Hinzufügen/Entfernen nur bei `manageable`, eigener Name bleibt; Browser-Probe 4/4, Gegenlauf 3 rot) · **15.5c ✅** E3: Titel ≤ 256 Zeichen (Kern + `maxlength`; Gegenlauf 3 + 1 rot) · 15.6 B9/B10 ⬜ · **E1 überholt (2026-10-30): kein Hotfix, Deploy D nach allen Fixes am Wochenende** · E4: Opus** |
| Z | Closeout P10.5 (Handover, Grafik, Rotationen) | Claude Code + Nikinger | — | ⬜ |

> **Die ausführlichen Statusspalten der Blöcke 0–10 stehen verbatim in
> [`MODULSTATUS_ARCHIVE.md`](MODULSTATUS_ARCHIVE.md) (L3) — hier trägt der Modulstatus den
> **Kurzstand**. Grund: der Head stand beim Bau von Block 11.4 über dem Softcap; die
> Details der geschlossenen Blöcke bleiben im Archiv nachlesbar, der Head bleibt der
> *live* Stand.

## Deploy-Tabelle

| # | Version | SHA | `health_gate` | Ausgabe |
|---|---|---|---|---|
| A | `v3.1.5` | `7358f22` | **9/9 OK** | nach Block 1–4 — **live seit 2026-10-23**, Release `20261023T065010.377336Z` |
| B | `v3.1.6` | `e5c834e` | **9/9 OK** | nach Block 5–6 (+ **Block 7.0**, die Update-Log-ID) — **live seit 2026-10-23**, Release `20261023T165838.591015Z` · **Deploy beim Nikinger** (Hard Rule 9, `sudo`; `deploy.sh main` → Release-Tests **1380 grün** (340,7 s) → Symlink-Wechsel → Dienst neu gestartet) · `health_gate.sh --expected-version=v3.1.6 --require-todays-update-log --expected-sha=e5c834e` → **9/9 OK** (`.rail__version` v3.1.6, Release-SHA `e5c834e…`, Update-Log 2026-10-23) · **Block 7.1 (UI-1) ist gemergt** (`f0e76b0`, aus `p105-block7`) — **nicht** in diesem Release, sondern in `v3.1.7` |
| C | `v3.1.7` | — | — | nach Block 7–8 — **2026-10-24 vorbereitet** (Badge, eigener `## 2026-10-24`-Block im Update-Log, Suite 1425 grün, `doc_health` 0, `ui_budget` 5/5), **`deploy.sh` beim Nikinger** |
| D | `v4.0.0` (vorher `v3.1.8`; Nikinger 2026-10-26) | — | — | nach Block 9–11 **+ 13** + Nachzug 2026-10-26 (**enthält RE-4 `rename_folder` und RE-3 `rename_space`**) (die UI-Änderungen aus Block 13 fahren mit) · **+ Block 14.7** (Karte kompakt/verteilt/glatt, 2026-10-29 geplant) · **+ Block 15** (Review-Fixes B1–B10 inkl. B1 — **kein** Hotfix vorab, Nikinger 2026-10-30: Deploy nach allen Fixes, Wochenende) |

**Stand 2026-10-24 (Abend):** Deploy A ist **live** (`v3.1.5`, Release `20261023T065010.377336Z`, SHA `7358f22`, `health_gate` **9/9 OK**); der Branch `p105-block5` (Block 5 + 6 + P10.5-26) ist **gemergt**. **Deploy B ist ebenfalls live**: `v3.1.6`, Release `20261023T165838.591015Z`, SHA `e5c834e`, `health_gate` **9/9 OK** (aus `main` mit `fastmcp 4.1.3`; der Deploy lief beim Nikinger, die Release-Tests im Release **1380 grün** in 340,7 s). **Block 7.1 (UI-1) ist gemergt** (`f0e76b0`) und damit ab `v3.1.7` dabei. **Deploy C (`v3.1.7`) ist vorbereitet** — Badge, eigener Update-Log-Block `## 2026-10-24` (9 Zeilen für Menschen), Suite **1425 grün** (332,6 s), `doc_health` 0, `ui_budget` **5/5** (Erstaufruf 204,5 KB); **`deploy.sh` liegt beim Nikinger**. **Die Generalprobe davor ist gefahren: 26/26 Zellen grün an der Wegwerf-Instanz** (Details im Session-Block unten; die Zeile stand vorher auf „25/25" — **datierte Korrektur**, der Block-7.0-Commit hat die Probe um eine Zelle erweitert). **Der Deploy-Aufruf der letzten Session ist an den Release-Tests gescheitert — nicht am Befehl:** eine verklebte `updated:`-Zeile in `SESSIONS_ARCHIVE.md` (behoben, Details im Session-Block) — es fehlt nur noch der Deploy-Aufruf durch den Nikinger. **Block 7.1 (UI-1) ist gebaut** auf dem Branch `p105-block7` — **nicht gemergt** (Nikinger-Entscheidung: Deploy A vor dem Branch-Merge); der Merge wartet auf Deploy A/B.

**Ein Deploy ist vier Schritte, kein Commit** (Plan §2.5): volle Suite + `doc_health` + `ui_budget` grün · Badge und `docs/UPDATE_LOG.md` · Commit + Push · **`deploy.sh` durch den Nikinger** (Hard Rule 9) · `health_gate.sh` mit **echter Ausgabe** in den Commit — nie die Behauptung.

## Abnahmestand

**72 Zeilen** (P10.5-1–72) — **geteilt**: die **geschlossenen** Zeilen (✅/⚠️) stehen
**verbatim** in [`ABNAHME_ARCHIVE.md`](ABNAHME_ARCHIVE.md) (L3), hier stehen die **offenen**
(⬜) und die Summe. **[2026-10-27, Block 14.35]** die Beschriftungs-Zeile des Kartenlayouts ist
**geschlossen**: **P10.5-71** (keine zwei gezeichneten Beschriftungs-Rechtecke überlappen
sich — **0** Paare statt 5, **3** von **13** Beschriftungen weggelassen, die Fokus-
Beschriftung ist am Pixel nachgewiesen da) steht jetzt im Archiv, mit ihrem Beleg; die
Zeilen 68/69 sind geschlossen, **70 wartet auf die Bilder**. **[2026-10-26, Block 14.3]**
die Kamera-Zeile: **P10.5-67** (der Inhalt füllt **93,6 %** der Leinwand, passt **in** sie
und sitzt **0,42 px** neben der Mitte — vorher 32,3 px) steht jetzt im Archiv, mit ihrem
Beleg; die Zeilen 68/69/71 bleiben offen, 70 wartet auf die Bilder.
**[2026-10-28, Block 14.5 — datierte Änderung der Zahlen]** der Rand der Kamera ist von
**40 px** auf **56 px** gewachsen (die Lappen-Kontur stand sonst **3,8 px** über dem
Leinwandrand — der Plan §2.5); der Füllgrad ist deshalb **91,1 %** statt 93,6 % und der
Versatz **0,49 px** statt 0,42 px. Die **Abnahmezeile** P10.5-67 (≥ 60 %) bleibt davon
**unberührt** ✅. **[2026-10-26, Block 14.1]** die
erste Zeile des Kartenlayouts ist geschlossen: **P10.5-65** (der Determinismus — zwei frische
Ladevorgänge, **0,0 px** über 152 Knoten). **[2026-10-25, Block 13]** +3 Zeilen (62/63/64) —
die älteren Zeilen unverändert. **[2026-10-26, Block 14.0]** +7 Zeilen (65–71 — die
Abnahmezeilen des Kartenlayouts, aus dem Plan
`docs/concepts/phase10_5_block14_kartenlayout_plan.md` §5).
Zählregel (Plan §5): ✅ erfüllt mit Beleg am Ort · ⚠️ erfüllt in anderer Form, Abweichung
benannt · ⬜ offen. Die Kriterien der Blöcke 14 stehen **wortgleich** im Plan
(`docs/concepts/phase10_5_block14_kartenlayout_plan.md` §5), die älteren Zeilen sind Kurzfassungen
(je Block am Ende des jeweiligen Plans); die **Belegte**
stehen im Commit und im Session-Block.

> **Datierte Korrektur zum Plan (2026-10-25, Block 11.8).** Der Plan §5 sagt „**61 Zeilen**,
> gezählt im Phase-Head". Der Head stand beim Bau von Block 11.8 bei **41.398 B** — über dem
> Softcap (40.960 B). Die geschlossenen Zeilen wandern deshalb **verbatim** in ein L3-Archiv
> (derselbe Schnitt wie beim Modulstatus in Block 11.4); **gezählt** werden die 61 Zeilen
> weiterhin — im Head **und** im Archiv.

| # | Kriterium | Status | Beleg |
|---|---|---|---|
| P10.5-18 | Live nach Deploy A: `/overview` Waiting ≤ 300 ms, Space-Wechsel während des Polls ≤ 1 s (Nikinger, DevTools, beide Eingänge) | ⬜ | — |
| P10.5-22 | Live nach Deploy B: claude.ai-Connector `list_spaces`/`search_items`/`get_item`/`update_item` ok (Nikinger); Log-Feld `proto` zeigt die Ära (V208) | ⬜ | — |
| P10.5-27 | **Live P10-J Lauf 1** (M3.1 Flash) | ⬜ | — |
| P10.5-28 | **Live P10-J Lauf 2** (lokales Modell, CT 111) — mit 27 die Abschlussbedingung der Phase | ⬜ | — |
| P10.5-49 | Live nach Deploy D: Ereignisse kommen über **beide** Eingänge an (V212 ✅) | ⬜ | — |

| P10.5-79 | Ultra-Review B6/B7/B9/B10: Space-Name und Titellänge geprüft, kein Einladungs-Token im Log, Suche übersteht paralleles Umbenennen | ⬜ | — |
| P10.5-60 | P10-J zweimal live belegt | ⬜ | — |
| P10.5-61 | Closeout-Dokumente + Rotationen per Skript | ⬜ | — |

**Summe:** 71 ✅ · 0 ⚠️ · 8 ⬜ (von 79). **[2026-10-30, Block 15.4]** +1 ✅ (10-78 B4 Mitglieder) ⇒ 71 ✅ · 0 ⚠️ · 8 ⬜. **[2026-10-30, Block 15.3]** +1 ✅ (10-77 B5/B8 Typen) ⇒ 70 ✅ · 0 ⚠️ · 9 ⬜. **[2026-10-30, Block 15.2]** +1 ✅ (10-76 B2/B3/B20 Dienststart) ⇒ 69 ✅ · 0 ⚠️ · 10 ⬜. **[2026-10-30, Block 15.1]** +1 ✅ (10-75 B1/B15 `asset_id`) und +4 Zeilen (76–79, Plan Block 15 §4) ⇒ 68 ✅ · 0 ⚠️ · 11 ⬜. **[2026-10-29, Sichtung]** +1 ✅ (10-70 die drei Kartenbilder von Block 14.7, vom Nikinger abgenommen) ⇒ 67 ✅ · 0 ⚠️ · 7 ⬜. **[2026-10-29, Block 14.7.5]** +2 ✅ (10-73 kompakt und verteilt — Solidität 0,830, NN 35,95 px; 10-74 glatt — Zusatzkrümmung 1,86) ⇒ 66 ✅ · 0 ⚠️ · 8 ⬜. **[2026-10-29, Block 14.7.0]** +2 Zeilen (73/74 — Form und Kontur der Karte, Plan `docs/concepts/phase10_5_block14_7_plan.md` §5; die Basislinie ist rot, das ist der Befund) ⇒ 64 ✅ · 0 ⚠️ · 10 ⬜. **[2026-10-28, Block 14.6.3]** +1 ✅ (10-72 der **Körper** — die Körpermaske aller Spaces ist **eine** Komponente (6274 Zellen), jeder Space hat **genau einen** Lappen, **146** Furche-Zellen, **4** Paare, Reach **47,9 / 44,1 / 48,4 / 44,6 px**, Luft **7,2 / 10,7 / 82,9 / 85,6 px**, `computeLobes()` **30,8 ms** (152) · **34,6 ms** (201 Knoten) — der Gegenlauf `koerper` macht **genau diese** Zelle rot) ⇒ 64 ✅ · 0 ⚠️ · 8 ⬜. **[2026-10-27, Block 14.35]** +1 ✅ (10-71 die Beschriftungen — **0** überlappende Paare (der Stand 14.3 zählte **4** per Pixelvergleich — der Recorder zählt dieselbe Szene mit **5**), **3** von **13** Beschriftungen weggelassen, die Fokus-Beschriftung am Pixel nachgewiesen da; der Gegenlauf `beschriftung` macht **genau diese** Zelle rot) ⇒ 63 ✅ · 0 ⚠️ · 8 ⬜. **[2026-10-26, Block 14.3]** +1 ✅ (10-67 die Kamera — Füllgrad **93,6 %**, der Inhalt passt, der Umriss sitzt **0,42 px** neben der Mitte statt 32,3 px) ⇒ 62 ✅ · 0 ⚠️ · 9 ⬜. **[2026-10-26, Block 14.2]** +3 ✅ (10-66 die Regionen — **152/152 = 100 %**; 10-68 die Stabilität — Median **0,0 px**; 10-69 das Budget —
 201 Knoten in **2147 ms**, 0 Frames) ⇒ 61 ✅ · 0 ⚠️ · 10 ⬜. **[2026-10-26, Block 14.1]** +1 ✅ (10-65 der Determinismus — zwei frische Ladevorgänge, **0,0 px** über 152 Knoten, der Beleg byteweise reproduzierbar; der Gegenlauf `seedJitter` → `Math.random()` macht **genau diese** Zelle rot) ⇒ 58 ✅ · 0 ⚠️ · 13 ⬜. **[2026-10-26, Block 14.0]** +7 Zeilen (65–71 — das Kartenlayout; die **Basislinie** ist in `regionen`, `kamera`, `beschriftungen` und `stabilitaet` **rot**, das ist gewollt und gemessen) ⇒ 57 ✅ · 0 ⚠️ · 14 ⬜. **[2026-10-26, Nikinger-Sichtung]** +3 ✅ (10-32 UI-4, 10-37 C2-Stil, 10-51 Editor live) ⇒ 57 ✅ · 0 ⚠️ · 7 ⬜. **[2026-10-25, Block 13]** +3 ✅ (10-62 die Editor-Größen, 10-63 die Knopfleiste nach Word, 10-64 die Knopffarben) ⇒ 54 ✅ · 0 ⚠️ · 10 ⬜. **[2026-10-25, Block 12]** +3 ✅ (10-57 Oversize, 10-58 ROADMAP, 10-59 Register-Bilanz) ⇒ 51 ✅ · 0 ⚠️ · 10 ⬜. **[2026-10-25, Block 11.6]** +2 ✅ (10-54 ED-3 die Format-Konvention, 10-56 die P1-Ankündigung) ⇒ 48 ✅ · 0 ⚠️ · 13 ⬜. **[2026-10-25, Block 11.8]** +2 ✅ (10-52 der Roundtrip, 10-55 der Rohmodus) ⇒ 46 ✅ · 0 ⚠️ · 15 ⬜. **[2026-10-25, Block 11.5]** +1 ✅ (10-53, ED-2 die To-do-Kästchen) ⇒ 44 ✅ · 0 ⚠️ · 17 ⬜. **[2026-10-25, Block 11.7]** +1 ✅ (10-50, das Budget) ⇒ 43 ✅ · 0 ⚠️ · 18 ⬜. **[2026-10-24, Block 10.5]** +4 ✅ (10-45, 10-46, 10-47, 10-48) ⇒ 42 ✅ · 0 ⚠️ · 19 ⬜. **[2026-10-24, Block 9.3]** +2 ✅ (10-43, 10-44) ⇒ 38 ✅ · 0 ⚠️ · 23 ⬜. **[2026-10-24, Block 9.2]** +1 ✅ (10-42, RE-4 `rename_folder`) ⇒ 36 ✅ · 0 ⚠️ · 25 ⬜. **[2026-10-24, Block 9.1]** +1 ✅ (10-41, RE-7 `created_by`) ⇒ 35 ✅ · 0 ⚠️ · 26 ⬜. **[2026-10-24, Block 8]** +4 ✅ (10-36, 10-38, 10-39, 10-40) ⇒ 34 ✅ · 0 ⚠️ · 27 ⬜. **[Stand 2026-10-24, Block 7.5–7.7]** 33, 34 und 35 ✅. **[Korrektur 2026-10-22, Block 6]** Die Zeile stand vorher auf „21 ✅ · 0 ⚠️ · 40 ⬜“ — die Tabelle trug aber **20** ✅ (der Zähler war schon vor diesem Block falsch; Block 5 hat eine Zeile auf ✅ gezogen und die Summe nicht nachgezogen). Neu: **23**, weil Block 6 drei Zeilen (10-23/24/25) auf ✅ gesetzt hat. Ein Wächter prüft die Summe jetzt gegen die Tabelle (`tests/test_head_rules.py`) — **über beide Dateien**, seit die geschlossenen Zeilen im Archiv stehen. **[2026-10-23, Block 7.1]** +1 ✅ (10-29, UI-1) ⇒ 25 ✅ · 0 ⚠️ · 36 ⬜. **[2026-10-23, Block 7.2]** +1 ✅ (10-30, UI-2) ⇒ 26 ✅ · 0 ⚠️ · 35 ⬜. **[2026-10-23, Block 7.3]** +1 ✅ (10-31, UI-3) ⇒ 27 ✅ · 0 ⚠️ · 34 ⬜.

## Offen beim Nikinger

- ~~**Vor Deploy D (15.5): Space-Durchsicht**~~ ✅ 2026-10-30 (Claude Code, Nikinger-Auftrag, read-only): **0** Treffer bei 263 Items. **E3** ✅ Nikinger: Titel ≤ **256** Zeichen (15.5c).
- ~~**V199**~~ ✅ 2026-10-22 (Block 1.1) — Live-Werte auf dem VPS: `dial_timeout` 10 s, `try_duration` 15 s, `try_interval` 1 s, Upstream `100.93.43.122:8765`. Die Vorlage trägt jetzt genau diese Werte.
- ~~**V200**~~ ✅ 2026-10-22 (Block 1.3) — Fleet-Playbook auf VM 200: `ok=11 changed=3 failed=0`, `sharefyx-tail-proxy` **active** mit `SuccessExitStatus=143`, nach dem Stopp **`Result=success`**, **0 failed units**, zweiter `--check` meldet `changed=0`. **Nicht gemessen:** der Domain-Weg während des Stopps (der Stopp dauerte Sekunden; der öffentliche Pfad war nicht beteiligt). Die alte Unit liegt als Kopie mit Suffix `~` unter `/etc/systemd/system/` — systemd liest sie nicht.
- **V203** — Funnel-Pfad von außen gewacht? (BT-10, Klärung eurofyx-fleet).
- ~~**P10.5-26 vor P10.5-27/28**~~ ✅ 2026-10-23 — **widerlegt, und zwar beide Verdachtsmomente.**
  Der `405` auf `GET /mcp` ist **nicht** die Ursache (gegen einen offenen FastMCP-Server mit *und*
  ohne SSE-Strom arbeitet opencode einwandfrei; der 405 steht auch im **erfolgreichen** Lauf gegen
  unseren Server im Log), und der behauptete serverseitige Werkzeugaufruf war **nicht belegt** —
  die Wegwerf-`serve.log` enthielt bis zum 2026-10-23 **null** `ev=tool`-Zeilen. Der Auslöser lag
  im **Messgerät**: der Stub-Prototyp lief endlos, und der `mcp debug`-Schritt stand vor dem
  Werkzeuglauf. Beleg: `probes/p105_b6_opencode_e2e.json` (`ev=tool, tool=list_spaces, ok=true`).
  **Kein Produktcode angefasst** — P2-B (`stateless_http=True`) bleibt, wie gelockt.
- ~~**Merge-Reihenfolge**~~ ✅ 2026-10-23 (Nikinger-Entscheidung) — **Deploy A zuerst, dann der
  Merge**: Deploy A lief aus `main` (`7358f22`, `fastmcp 3.4.7` im Dev-venv), **danach** ist
  `p105-block5` (Block 5 + 6 + P10.5-26) nach `main` gemergt. Der Merge durfte **nicht** vor
  dem Deploy A auf `main` landen, sonst hätte `deploy.sh main` den Block-5/6-Stand unter der
  Nummer `v3.1.5` ausgeliefert.
- **P10.5-18** (Deploy A) — Live-Messung nach dem Deploy: `/overview` Waiting ≤ 300 ms, Space-Wechsel
  während des Polls ≤ 1 s (beide Eingänge, DevTools). Dazu die drei Live-Checks aus Plan
  §Deploy A: eine Zeile Caddy (V199 bleibt Fleet-Sache) · Handyfoto-Upload (EXIF weg, richtig
  gedreht) · Spaces-Panel direkt nach dem Laden (BG-1).
- **P10.5-27/28** — Live-Abnahme P10-J: zwei Modellanbieter, ein Server, ein Werkzeug (`list_spaces`) — Block 6 und Z. **Voraussetzung ist erfüllt:** die Wegwerf-E2E (P10.5-26) zeigt, dass ein Nicht-Claude-Client (`list_spaces` gelingt) — offen ist nur noch der **Live**-Lauf mit zwei Modellanbietern.
- **Handover-Posten (Regelkandidat, Nikinger 2026-10-25):** Sichtungen **zuerst als Bilder an der Wegwerf-Instanz**, live nur, was der Server nicht selbst entscheiden kann — steht als Arbeitsweise schon in der Wurzel-`CLAUDE.md` (2026-10-22); für den Closeout-Handover als feste Regel prüfen.
- **Block 2, Zeile 15 (AL-1)** — Migration + Live-Check beim Nikinger.
- **[2026-10-28 entschieden: Option B — ein Körper, das Layout bleibt; Plan 14.6 `docs/concepts/phase10_5_block14_6_plan.md`]** **NEU 2026-10-26 (Block 14.2): die „Gehirnkarte“ wird zu Inseln — die C2-Furche hat im neuen
  Layout keinen Gegenstand.** Die neue L4 (Anker-Gravitation + Querfedern) rückt die Spaces
  **auseinander**: die Lappen zweier Spaces **berühren** sich nicht mehr. **Gemessen:** die
  Furche-Zellen in der C2-Probe **62 → 0**; in der Produktionskarte (5 Spaces) liegen die
  Schwerpunkte der Spaces **mindestens 346 px** auseinander, der Radius der Körpermaske ist
  **48 px** ⇒ dort kann keine Furche entstehen. Die **C2-Zeichenregel** ist damit im Alltag
  **nicht mehr sichtbar** (die Furchen zwischen den Lappen), die Bahnen zwischen den Spaces
  werden **lang**. **Kein Fehler, eine Folge des beauftragten Layouts** — aber eine **sichtbare
  Änderung** der in Block 8/9 abgenommenen Optik. **Was der Nikinger entscheiden muss:** die
  Bilder aus **14.5** zeigen die Inseln (gemessen: **5** Lappen, **0** Furche-Zellen — die
  Inseln berühren sich nicht); soll die C2-Optik (Furchen, Bahnen) an die Inseln
  angepasst werden (eigener Schritt nach 14.5) oder so bleiben? **Bis dahin** ist der C2-Wächter
  auf einen **festen Eingang** gestellt (zwei Spaces **berühren** sich dort, wo die Furche etwas
  zu trennen hat) — er prüft damit die **Zeichenregel**, nicht das Layout; ohne diese Reparatur
  wäre der Gegenlauf „Furche aus“ **grün** geblieben, ohne dass der Fehler wiederhergestellt
  war (`probes/p105_b8_c2_probe.mjs`, datierter Kommentar; `tests/test_graph_c2.py`).
  **Stand 2026-10-28 (Block 14.6): die Frage ist beantwortet — Option B ist umgesetzt.** Der
  Körper ist geschlossen (`LOBE_CLOSE_PX = 160`; die sechs Varianten in 14.6.1, der Wert vom
  Nikinger nach der Standardregel des Plans §3 entschieden), die Karte ist **ein Körper** mit
  Lappen und Furchen, **kein Knoten** hat seinen Platz gewechselt. **P10.5-72** ist ✅ (der
  Beleg: `probes/p105_b14_karte_bilder.json`). **Offen bleibt die Sichtung P10.5-70** — die
  drei Bilder im Repo sind die **neuen** (Schritt 14.6.3).
- **2026-10-28 (Block 14.5): die Update-Log-Zeile für das neue Kartenlayout** ist **geschrieben**
  (Nachzug 14.5, im Block `## 2026-10-26` — dem Block des Deploys D). **Bleibt beim Deploy:**
  das `deploy.sh`-Gate verlangt, dass die
  **oberste** `##`-Überschrift in `docs/UPDATE_LOG.md` **das Datum des Deploy-Tages** trägt
  (jetzt `## 2026-10-26`) — der Block muss am Deploy-Tag **umdatiert** werden, sonst bricht
  das Gate ab (`SHAREFYX_ALLOW_STALE_UPDATELOG=1` überspringt es, ist aber nicht die Absicht).
- ~~**Deploy B (`v3.1.6`)**~~ ✅ **2026-10-23** — **live**: Release `20261023T165838.591015Z`, SHA
  `e5c834e`, `health_gate` **9/9 OK** (`.rail__version` v3.1.6). Die Release-Tests im Release
  **1380 grün** (340,7 s), Symlink-Wechsel, Dienst neu gestartet — Details im Session-Block.
  **Live danach:** **P10.5-22** (claude.ai-Connector
  `list_spaces`/`search_items`/`get_item`/`update_item`, Log-Feld `proto` zeigt die Ära, V208) ·
  **P10.5-25** (`curl -si -X POST …/mcp` → **401 mit Challenge**, kein 307) · **P10.5-27/28**
  (Live P10-J, zwei Modellanbieter). **5.7:** Fabian kurz Bescheid („kurzer Neustart; der
  Connector sollte ohne neue Anmeldung weiterlaufen").
- ~~**Befund 2.5 (P10.5-9 ⚠️)**~~ ✅ 2026-10-22 (Block-2-Nachzug, Nikinger-Entscheidung „ja") — `create_item(space=, folder=<neu>)` und `POST /api/v1/items` legen im fremden Home-Space mit `write:` **keinen** neuen Ordner mehr an; die Regel ist `permissions.manages_space()` (eigener Space oder Team-Space mit Schreibrecht), auf beiden Flächen. Ohne `folder` bleibt das Anlegen an der Space-Wurzel erlaubt (P6-U).

## Startauftrag — Block 7 (Darstellung: UI-1–UI-6, KA-5) · Ausführer
> **Verbatim verschoben** nach `STARTUPTRAG_ARCHIVE.md` (`scripts/move_sections.py`) — dort unter derselben Überschrift.

## Startauftrag — Block 9 (Rechte und Namen: RE-7, RE-4, RE-3) · Ausführer
> **Verbatim verschoben** nach `STARTUPTRAG_ARCHIVE.md` (`scripts/move_sections.py`) — dort unter derselben Überschrift.

## Nächste Session — Aufträge des Nikingers (2026-10-25): **alle vier gebaut** (Block 13)

> **Stand 2026-10-27:** die vier Aufträge (Editor-Größen, Knopfleiste nach Word, Knopffarben, die
> ganze Gehirnkarte) sind gebaut **und gemessen** — Belege im Modulstatus, Abnahmezeilen
> P10.5-62/63/64, die Aufträge **wortgleich** im Session-Archiv (`SESSIONS_ARCHIVE.md`, Block 13).
> **Offen ist die Sichtung**, nicht die Arbeit: die drei **Sichtungen** **P10.5-37** (C2-Stil der
> Karte), **P10.5-51** (Editor Stufe 1) und **P10.5-32** (UI-4) — drei Bilder, drei Urteile; die
> Deploys **C** (`v3.1.7`) und **D** (`v3.1.8`, jetzt **mit** den Änderungen aus Block 13) liegen
> beim Nikinger.

## Session stopped — 2026-10-30 (Block 15.5 + 15.5b + 15.5c: Space-Name eine Regel, Slug ≤ 100 Byte, Gast-Knöpfe, Titel ≤ 256)

**Ergebnis.** Drei Schritte gebaut, je ein Commit. **15.5 (B6/B7):** `files.is_valid_space_name()`
ist die **eine** Regel (Kern: `Store.create()`/`move()`; ersetzt die Kopien in `rename_space()`/
`acl.create_space()`) — `team/`, `./team`, `team/.` ⇒ MCP `invalid`, REST 422, keine Datei. Der
Slug im Dateinamen ist auf **100 UTF-8-Byte** gekürzt (`files.item_filename()`); E3 gemessen:
`f_namemax` 255, die tmp-Datei von `atomic_write` ist Name + 14 ⇒ Grenze 224. **15.5b:** der
Space-Dialog zeigt Hinzufügen/Entfernen nur bei `manageable`, der eigene Name behält „Entfernen“
(E6); nach dem Austragen zurück zur Liste (vorher 403 beim Neuladen). **15.5c (E3, Nikinger:
256):** Titel ≤ **256 Zeichen** im Kern — beim Update nur ein **geänderter** Titel (die UI schickt
ihn bei jedem Speichern mit) —, dazu `maxlength="256"` an beiden Titelfeldern.

**Beleg.** 15.5: 40 Fälle, Gegenlauf 6/15/1 rot, Suite 1798 + 1 vorbestehend rot (INDEX-Reserve
seit `31fa401`, behoben). 15.5b: Browser-Probe `probes/p105_b15_5b_gast_knoepfe_probe.py` 4/4,
Gegenlauf 3 rot (der erste war zahnlos, neu gebaut). 15.5c: 3 Wächter, Gegenlauf Limit aus 3 rot ·
„nur geänderter Titel“ aus 1 rot; volle Suite danach **1802 passed, 0 rot** (401 s). **P10.5-79** bleibt ⬜ (B9/B10). Summe **71 ✅ ·
0 ⚠️ · 8 ⬜ von 79**.

**Live-Durchsicht (Nikinger-Auftrag, read-only, `/home/savefyx/savefyx-data`):** `space:` ≠
Verzeichnis **0** · 263 Items · längster Titel **89** Zeichen · **4** Dateien mit Slug > 100 Byte
(bekommen beim nächsten Write den kurzen Namen) · `git status` im Datenrepo sauber.

**Nächste Session — 15.6 (B9/B10), Opus, kalt startbar:**
1. Lesen: Plan §3 Zeile 15.6 + Review-Bericht B9/B10
   (`docs/concepts/phase10_5_ultra_review_v4.0.0.md`). **Erst reproduzieren**, dann bauen.
2. **B9:** `GET /ui/invite/<token>` steht im Klartext in der `ev="http"`-Zeile — redigiert wird
   nur `/mcp/<token>`. Orte: `phase2_mcp/mcpserver/request_log.py` (~Z. 221),
   `logging_setup.py` (`_SECRET_PATTERNS`). Wächter: Log enthält das Token nicht.
3. **B10:** `Store.search()` (`phase1_storage/storage/store.py`) liest Dateien nach dem Lock —
   paralleles Umbenennen ⇒ `FileNotFoundError`. Fix: verschwundene Datei je Zeile überspringen.
   Wächter: Such-Threads gegen Titel-Updates/`trash`, kein Fehler.
4. Danach **15.7:** volle Suite, `doc_health`, **Update-Log-Zeilen** (15.5b: Gäste sehen keine
   Verwaltungsknöpfe, können sich austragen; 15.5c: Titel höchstens 256 Zeichen), Head-Bilanz,
   P10.5-79. Dann Launch-Film, dann Deploy D am Wochenende (beim Nikinger).
