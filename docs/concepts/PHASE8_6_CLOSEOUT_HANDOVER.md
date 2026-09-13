---
status: snapshot
purpose: "Partial-Closeout-Handover P8.6 — Status, Delta seit dem P8.5-Handover, Abnahmestand, die neun UX-Befunde und wo sie gelockte Entscheidungen treffen, [VERIFY]-Bilanz V103–V122. Die Phase ist NICHT abgeschlossen und NICHT ausgeliefert."
read-when: vor dem Entwurf des zweiten P8.6-Plans einmal ganz lesen — ersetzt das Nachlesen von Phase-Head und SESSIONS_ARCHIVE für alles außer der Detailhistorie
detail: L2
up: ../../ROADMAP.md
down:
  - ./phase8_6_ui_polish_plan.md                    # Plan 1, §0.2 Locks P8.6-A–P8.6-U, §8.1 Abnahmematrix, §8.3 VERIFY-Register; §9 bewusst leer
  - ../../phase8_6_ui_polish/CLAUDE.md              # Phase-Head — Modul-Status, Vormerkungen, die neun Befunde im Session-Block wörtlich
  - ../../phase8_6_ui_polish/SESSIONS_ARCHIVE.md    # volle Phasenhistorie, verbatim, newest-first
  - ./PHASE8_5_CLOSEOUT_HANDOVER.md                 # Vorgänger — §4 war der Einstieg in die P8.6-Planung
  - ./p8x_ui_polish_notes.md                        # Inhaltsquelle §1–§10; Plan 2 startet hier, nicht bei null
  - ./sichtpruefung_automation_conventions.md       # §2 Visuelles ist Nikinger-Sache · §5 screenshots_latest-Konvention
  - ./sichtpruefung_automation_tooling.md           # Vision-Backend, Messbefund zum Plugin
updated: 2026-09-13
---
# Phase 8.6 — Partial-Closeout-Handover (P8.6 Plan 1 → P8.6 Plan 2)

> **Das ist kein Phasenabschluss.** Phase 8.6 ist **nicht ausgeliefert**: Badge steht auf
> `v3.0.1`, `origin/main` steht auf `2a93e67`, lokal liegen **drei ungepushte Commits**
> (`90c72e2` Block C, `bc2aa9f` Partial Closeout, plus der Commit, der dieses Dokument
> mitbringt). Sechs von acht Steps sind ✅, **Gate und Step Z sind ⬜**. Der Code ist gebaut und getestet — die Nikinger-Sichtprüfung am
> 2026-09-12 hat ihn nicht abgenommen, sondern **neun UX-Befunde** zurückgegeben.

> **Warum dieses Dokument trotz P8.6-B existiert.** Der Lock sagt „ein Dokument pro Phase,
> ein separates Handover **nur** auf ausdrückliche Nikinger-Anordnung". Die Anordnung ist am
> **2026-09-13** im Closeout-Auftrag erfolgt. Das ist die im Lock vorgesehene Ausnahme, keine
> stille Aufweichung — dieselbe Mechanik wie bei P8.5-R.

> **Plan §9 bleibt leer.** §9 ist nach P8.6-B der *kanonische* Abschluss der Phase. Eine
> Phase, die nicht abgeschlossen ist, bekommt dort keinen Eintrag. Dieses Dokument tritt
> **nicht** an seine Stelle; es ist der Teil-Stand für den, der Plan 2 schreibt.

---

## 1 Status in fünf Sätzen

1. **Alles bis Block C ist gebaut und grün.** `pytest` **970 passed** (Baseline V107 war
   964), `ui_budget.py` **5/5** im Korridor (Bundle 137,5 KB von 250 KB), Tabu-Diff §0.3 über
   die **gesamte** Phase leer, Service-Touch durch einen Agenten: **0** (PID 991 durchgehend).
2. **Die Phase ist an ihrer eigenen Qualitätsregel hängengeblieben, nicht an einem Bug.** Die
   Drei-Bedingungen-Regel des Nikingers (Tests grün · Bilder laut Agent grün · Nikinger hat
   die kritischen Bilder gesichtet) ist zu zwei Dritteln erfüllt; die dritte Bedingung hat
   **neun UX-Befunde** produziert, nicht die Freigabe.
3. **Drei der neun Befunde sind keine Politur, sondern Fragen an gelockte Entscheidungen** —
   Befund 5 löst die Eskalationsregel **P8.6-O2** aus (`.shell`-Grid, alle drei Spaltenbreiten
   auf einmal), Befund 7 **kehrt C1 um** (also N3-Lesart b, eine bereits beantwortete
   Nikinger-Frage), Befund 1+8 treffen **P8.6-E** (`--bg-void` bewusst auf drei Stellen
   begrenzt). Details und Pfad: §4.
4. **Ein Befund wurde auf der Produktion reproduziert, nicht nur am Wegwerf** (Befund 9,
   schmaler Viewport ≤1280px, Knöpfe nicht mehr klickbar). Das hebt ihn aus der Klasse
   „Screenshot sieht komisch aus" heraus: er trifft die **live laufende** `v3.0.1`, also auch
   ohne P8.6-Deploy. Er gehört in Plan 2 ganz nach oben.
5. **Die Vision-Frage ist entschieden und hat ein Werkzeug gekostet.** Der vom Nikinger
   vorgegebene Plugin-Pfad (`DavidEasden/opencode-vision`) wurde installiert, **gemessen** und
   **zurückgebaut**: er amputiert M3s nativen Bildpfad. Ollama + `qwen3-vl:8b` bleiben als
   Offline-Fallback liegen. Konvention §4 („Screenshots im Chat") ist in OpenCode **dauerhaft
   unerfüllbar** und bleibt Claude-Code-only.

---

## 2 Delta seit dem P8.5-Handover

**15 Commits**, `d1af51b..bc2aa9f`. Produktcode-Aggregat: **841 insertions, 191 deletions**
über 9 Dateien. Die Implementierungsdetails stehen im Code und in Plan §3–§6 — hier nur, was
**wo** liegt:

| Was | Wo | Commit |
|---|---|---|
| Step 0 — 6 Doku-Links, 4 L1-Cards, INDEX-Kompression, 2 Code-Defekte gefunden | repo-weit, `docs/INDEX.md` | `440e462` |
| Block A — `<select>`-Rückbau, 6 Tokens, `--border-soft`-Fix, Konvention v3 „Vorsicht" | `app.{html,css}`, `js/dialogs.js`, `phase8_ui_graph/CLAUDE.md` | `32fddba` |
| Block D — V102-Dedup, FNV-1a-Layout-Seed, `cancelAnimationFrame` | `js/graph.js` | `04dee6a` |
| Step V — Ollama 0.34.0 + `qwen3-vl:8b` + `vision_ollama.py`, V119-Smoke 46 s | `phase8_6_ui_polish/scripts/` | `cf57d8c` |
| Step V-plugin — Plugin + MCP-Server `local_vision` (AGPL-Check dokumentiert) | `~/.config/opencode/`, `scripts/mcp_local_vision_server.py` | `cd25712` |
| V121+V122 — visuelle Verifikation A+D gegen Wegwerf auf Port 18773 | `docs/screenshots/p8_6_block_*.png` | `5152d35` |
| **V-vision-befund — das Plugin ist der Defekt** (A/B/C-Messung mit `opencode run`) | Tooling-Doku | `bdf1383`, Rückbau `700471e` |
| Block B — eine konsolidierte Hover-Regel, `.account-nav`, `.action--caution` (genau 2) | `app.{html,css}` | `a5d8c97` |
| §5-Konvention — `screenshots_latest/` + Dateiname-und-Checkkriterium-Pflicht | `screenshots_latest/`, Konventionsdoku | `2a93e67` |
| Block C — Rail-Reihenfolge, „Alle Items" unten, `.overview`-Grid, klickbare Spaces, Ordner-Zähler | `app.{html,css}`, `js/{tree,list,state,graph}.js` | `90c72e2` |
| Partial Closeout — die neun Befunde, Vormerkung „p8.6 plan 2 (N.6)" | Phase-Head | `bc2aa9f` |

**Deploy-Stand:** **kein Deploy in dieser Phase.** Live läuft weiterhin `v3.0.1` aus P8.5
(Release `20260905T140325.378914Z`). Der Host hat gewechselt (Proxmox-Migration auf
i5-14600KF), `sharefyx-mcp` läuft dort als **PID 991** über die Auto-Restart-Mechanik.

---

## 3 Abnahmestand

Plan §8.1 führt **32 Zeilen** (P8.6-1 … P8.6-32). Sie sind **nicht** abschließend ausgewertet
worden — das war Step-Z-Arbeit und Step Z hat nie stattgefunden. Was in dieser
Closeout-Session **maschinell** nachgeprüft wurde, steht hier; alles andere ist offen:

| Zeile | Prüfung | Ergebnis |
|---|---|---|
| P8.6-4 | `docs/INDEX.md` ≤ 38 KB nach allen neuen Zeilen der Phase | **❌ verletzt** — 40.870 B vor dieser Session. Siehe §7 |
| P8.6-6 | `rgba(62,141,243` nur noch in `:root` | ✅ 6 Treffer, alle `:root` bzw. Erklärungskommentar |
| P8.6-7 | `--border-soft` kommt nicht mehr vor | ✅ nur noch als historische Notiz im Kommentar (`app.css:887`) |
| P8.6-14 | `.btn:hover`/`.btn-primary:hover` ohne Hex-Verläufe | ✅ `color-mix()` auf Tokens |
| P8.6-16 | genau zwei Elemente tragen `.action--caution` | ✅ 2, maschinell gehalten durch `test_caution_class_only_on_logout_and_archive` |
| P8.6-17 | kein hartkodierter Radius mehr in `app.css` | ⚠️ **im Sinn erfüllt** — der Token-Drift (`6px`) ist weg; vier `border-radius: 999px` bleiben, das ist die Pillenform, kein Token |
| P8.6-20 | kein Vorkommen von „Konto" in `webui/` und `tests/` | ⚠️ **im Sinn erfüllt** — kein sichtbares Label mehr; die Restvorkommen sind das deutsche Wort in Sperr-Meldungen (`api.py:302`) und Kommentare über die Umbenennung. **Das Kriterium ist zu breit formuliert**, Plan 2 sollte es auf „kein Label" schärfen |
| P8.6-28 | `pytest` grün, ≥ 964 | ✅ **970 passed in 116 s** (gemessen 2026-09-13) |
| P8.6-30 | Tabu-Diff §0.3 über die gesamte Phase leer | ✅ leer |
| P8.6-31 | `v3.0.2` live, Badge sichtbar, `health_gate.sh` 8/8 | **⬜ nicht erreicht** — Badge steht auf `v3.0.1` |
| P8.6-32 | Service-Touch durch einen Agenten: 0 | ✅ PID 991 durchgehend, Wegwerf nur per PID-Datei gestoppt |

**Die (W)-Zeilen** (P8.6-8, -10, -12, -13, -18, -19, -21 bis -27) sind gebaut, aber **nicht
abgenommen**: die Sichtprüfung, die sie hätte schließen sollen, ist in Befunde umgeschlagen.
Mehrere von ihnen (P8.6-21 „Map ~40 % Breite", P8.6-22 „unter 1280px ohne Überlappung") sind
durch die Befunde 4 und 9 sogar **aktiv widerlegt** — Plan 2 muss sie neu formulieren, nicht
nur neu prüfen.

---

## 4 Die neun Befunde — wo sie stehen und wo sie den Plan treffen

**Der Wortlaut steht an zwei Stellen und wird hier nicht ein drittes Mal kopiert:**
`phase8_6_ui_polish/SESSIONS_ARCHIVE.md` → Block „2026-09-12 (Block-C-Sichtung Nikinger)",
und die Commit-Message von `bc2aa9f`. Was hier steht, ist die **Bewertung**, die dort fehlt.

### 4.1 Der eine Befund, der auf Produktion reproduziert ist

**Befund 9** (schmaler Viewport ≤1280px: Karte „sieht komisch aus", Knöpfe nicht mehr
klickbar) hat der Nikinger **selbst auf der Produktion** nachgestellt. Er hängt damit **nicht**
am P8.6-Deploy — er ist im live laufenden `v3.0.1` und war es vermutlich schon vor Block C.
Die `@media (max-width: 1280px)`-Regel aus C3 kann ihn verschlimmert, aber nicht verursacht
haben. **Plan 2 sollte ihn zuerst instrumentieren** (CDP-Probe gegen die Wegwerf bei
1024 / 1200 / 1440), bevor er ihn repariert; sonst wird ein Symptom gepatcht.

### 4.2 Die drei Befunde, die gelockte Entscheidungen öffnen

| Befund | Trifft | Warum das kein CSS-Ticket ist |
|---|---|---|
| **5** — Spaces + „Zuletzt benutzt" in den Listen-Slot links, Map rechts, Editor im rechten Slot | **P8.6-O2** (`app.css:327-332`, `.shell`-Grid) | Die Regel sagt: wer Rail-, Listen- **und** Detail-Breite gleichzeitig anfasst, macht einen Architektur-Schnitt und eskaliert. Block C hat das bewusst vermieden und nur `.overview` umgebaut. **Plan 2 kann es nicht vermeiden** — das ist genau der Umbau, den die Regel meint. |
| **7** (zweite Hälfte) — Einstellungen nach unten, direkt über Abmelden | **C1 / N3-Lesart b** | C1 hat „Einstellungen nach oben, Abmelden ans Rail-Ende" gebaut, weil der Nikinger die Frage N3 am 2026-09-09 so beantwortet hat. Befund 7 dreht das um. Das ist eine **Umkehr einer beantworteten Frage**, kein neuer Wunsch — und gehört als solche in Plan 2 datiert, nicht als Bugfix. |
| **1 + 8** — verschiedene Grautöne, YAML-Header „sieht wie eine Warnung aus" | **P8.6-E** (`--bg-void` an genau drei Stellen) | Block A hat den Layer-0-Token bewusst sparsam gesetzt („ein Layer, der überall liegt, ist kein Layer"). Die Befunde verlangen eine *durchgängige* Layer-Zuordnung für Editor, YAML-Panel und Append-Zeile. Plan 2 weitet P8.6-E entweder aus oder ersetzt es — beides ist eine Lock-Entscheidung. |

### 4.3 Folge für die Versionierung

**P8.6-R** lockt `v3.0.2` als Patch-Bump mit der Begründung „§1 verschiebt Flächen, ändert aber
**keine** Informationsarchitektur". Befund 5 ändert genau die: der Übersichts-Slot wird zum
Listen-Slot, der Editor wandert in den rechten Slot. **Die Begründung des Locks trägt nicht
mehr.** Der Lock selbst sagt ausdrücklich, dass `v3.1.0` die Entscheidung des Nikingers wäre,
nie die des Ausführenden — **Plan 2 legt die Frage vor, entscheidet sie nicht.**

### 4.4 Die drei verbleibenden Befunde

2 (Konto-Dialog-Knöpfe unsichtbar), 3 (Refresh überlappt die Karte), 4 (Karte zu klein),
6 (Hover verrutscht nach Space-Klick) sind gewöhnliche Korrekturen ohne Lock-Berührung.
**Befund 2 ist zuerst eine Messfrage**, keine Bauaufgabe: `.account-nav` wurde in Block B
eingeführt und der Screenshot zeigt die Knöpfe nicht — ob sie fehlen, unsichtbar sind oder
außerhalb des Viewports liegen, ist ungeklärt.

---

## 5 `[VERIFY]`-Bilanz V103–V122

| # | Frage | Ergebnis |
|---|---|---|
| **V97** | `ui_budget.py`-Baseline (geerbt) | ✅ vor Phasenstart geschlossen — 5/5, 130,1 KB; am Ende 137,5 KB, weiter im Korridor |
| **V107** | `pytest`-Baseline | ✅ 964 → **970**, gemessen 2026-09-13 |
| **V106** | Sammelmarker: alle `Datei:Zeile`-Anker gegen `main`@`d1af51b` | ✅ **kein Anker-Drift über die Phase gemeldet.** Achtung für Plan 2: die Anker aus Plan 1 zeigen jetzt auf den Stand **vor** Block A–D und sind teilweise verschoben — Plan 2 braucht einen **eigenen** Sammelmarker gegen `bc2aa9f` |
| **V108** | `_overview` 863 ms — Rauschen oder Regression? | ✅ **aufgelöst, keine Regression.** Nach der Proxmox-Migration 365 / 370 / 380 ms in drei Blöcken gemessen. Die 863 ms waren Last auf dem alten Mini-PC |
| **V109** | `app.css:785` `.35` vs. `--accent-line` `.40` | ✅ angeglichen auf `--select-line` (Block A, „im Zweifel angleichen") |
| **V111** | Phase-8-Head-Größe im INDEX nachgezogen? | ✅ **erst am 2026-09-13 geschlossen, nicht in Block A.** Die INDEX-Zeile nannte bis dahin die Zahl von vor Block A (42.343 B) plus eine *Schätzung* des Zuwachses; real sind es 43.190 B (+847 B statt ~600 B). Jetzt korrigiert |
| **V112** | Schneidet die Map vor dem Fix messbar ab? | ✅ geschlossen durch C3 + D3-Nachzug; Regressionswächter `test_overview_graph_has_no_max_width_or_min_height` |
| **V113** | Setzt `renderSpaceNode()` `aria-current` korrekt? | ✅ **als negativer Befund geschlossen** — `.tree__space` setzt im Code **gar kein** `aria-current`, und die Variable heißt `state.activeSpace`, nicht `state.space`. Plan §4.2 lag falsch. Bewusst nicht repariert (B2 war „prüfen, nicht bauen") |
| **V115** | Reicht der `ResizeObserver` beim ersten Öffnen? | ✅ **nein** — `loadGraph()` braucht `requestAnimationFrame(resize)`, sonst rechnet `seedInitialPositions()` gegen eine 0×0-Box |
| **V116** | `activateView(name)` oder `navigate(name, "open")`? | ✅ `activateView`, exportiert. Nebenbefund: die Funktion war doppelt definiert, `PAGE ERROR` im Self-Smoke |
| **V117** | Trägt `state.items` beim Rail-Rendern die Items aller Spaces? | ✅ **nein** — daher `state.itemsLoaded` + Reset in `activateView()`/`navigateAll()` |
| **V119** | Existiert der Referenz-Screenshot für den Vision-Smoke? | ✅ ja, Smoke 46 s, korrekte deutsche Antwort |
| **V121** | End-to-End durch den `local_vision`-MCP-Server | ✅ ja — der Server ist korrekt; das **Plugin** darüber war der Defekt |
| **V122** | Block-D-Ergebnis visuell (Doppelrand weg, Karte stabil) | ✅ gegen das live-deployte `v3.0.1` verifiziert |
| **V110** | Ist der bestehende `#home-button`/`.tree__scope`-Mechanismus der „Kippschalter"? | **⬜ offen** — war für die Sichtprüfung vorgesehen; die lieferte Befunde statt Antworten |
| **V114** | Welche Trägerflächen meinte der Nikinger in §10.1? | **⬜ offen**, gleicher Grund |
| **V118** | Tag-Kante + explizite Kante zwischen denselben Knoten: zwei Linien gewollt? | **⬜ offen**, gleicher Grund. `dedupeEdges()` fasst `implicitEdges` bewusst **nicht** an |
| **V103** *(geerbt aus P8.5)* | `deploy.sh`: ist der `sudo`-Prompt im Vordergrund sichtbar? | **⬜ offen** — hängt am Deploy, und der fand nicht statt. Zweite Phase in Folge unbeantwortet |
| **V120** | Welche Events sollen den dynamischen Tab-Titel auslösen? | **⬜ offen, bewusst** — in P8.6 eröffnet, außerhalb des Scopes („would be cool"-Note) |

**Bilanz: 14 geschlossen, 5 offen.** Vier der fünf offenen (V110, V114, V118, V103) hängen
am Gate bzw. am Deploy — sie sind **nicht** vergessen worden, sie sind blockiert.

---

## 6 P1-Contract

**Keine neunte Öffnung, und keine angekündigt.** P8.6-S hat `storage/` von vornherein
zugesperrt; V102 wurde per Frontend-Dedup in `graph.js` gelöst (N2), §3 Ordner-Zähler
clientseitig aus `state.items` (P8.6-O). Der Tabu-Diff über `phase1_storage/storage`,
`phase4_auth/authserver`, `phase2_mcp/mcpserver` und die vier `webui/*.py` war über die
gesamte Phase leer — auch der Hint-Text, der in P8.5 die eine Ausnahme war, blieb unberührt.

**Achtung für Plan 2:** keiner der neun Befunde verlangt einen Server-Touch. Wenn Plan 2
einen braucht, ist das eine neue Tatsache und wird **angekündigt**, nicht beim Bauen entdeckt.

---

## 7 Doku-Befunde dieser Closeout-Session

Vier Drifts, alle im selben Commit wie dieses Dokument behoben oder benannt:

1. **Rotationsregel P8.6-T war verletzt.** Der Phase-Head trug einen `## Session
   stopped`-Block **plus** einen zweiten Session-Block als `###` darunter — genau das
   Phase-8.5-Muster, das P8.6-T verbietet, und genau der Fall, bei dem
   `scripts/rotate_session_block.sh` fälschlich „bereits konform" meldet. Behoben: die
   `###`-Überschrift auf das `## Session stopped — <Datum>`-Schema gebracht (das Skript
   fordert das in seinem eigenen Warnzweig), dann das Skript laufen lassen. Alle vier
   Gegenproben grün, Head **72.958 → 59.797 B**.
2. **Der Block-D-Session-Block im Archiv war abgeschnitten.** Die Hand-Rotation vom
   2026-09-10 hat ihn mitten im Satz („…am Anfang, falls vorhanden, und setzt") gekappt —
   **72 Zeilen / 4.403 B fehlten**, darunter die vollständige `node`-Probe von `dedupeEdges()`
   (4/4) und `seedJitter()` (5/5). Wiederhergestellt **mechanisch aus
   `04dee6a:phase8_6_ui_polish/CLAUDE.md`**, nicht abgetippt; `cmp` gegen das Original
   byte-identisch, Altbestand nachweislich unverändert. **Das ist der Beleg dafür, warum die
   Rotation ins Skript gehört und nicht in die Hand.**
3. **„Lokalstand 7 Commits voraus" war falsch.** Der Session-Block vom 2026-09-12 behauptete
   7 (bzw. 6) ungepushte Commits. `git fetch` + `git rev-list --left-right --count` sagen:
   **2**. Die früheren Commits sind am 2026-09-10 und -11 gepusht worden. Korrigiert.
4. **P8.6-4 ist verletzt.** `docs/INDEX.md` stand bei **40.870 B**, das Abnahmekriterium
   fordert ≤ 38 KB. Der Phase-Head kennt das Problem als P9-Vormerkung (die
   `updated:`-Frontmatter-Kette wächst, nicht der Body) und schreibt als Zwischenlösung
   „pro Session einen alten Pipe-Eintrag straffen" vor — in dieser Session angewandt.

**Eine Konvention steht noch offen:** `screenshots_latest/` zeigt weiterhin auf die **Block-B**-
Screenshots, obwohl der Nikinger die **Block-C**-Bilder gesichtet hat. Die §5-Konvention regelt
den Wechsel nur „bei Phasenwechsel", und P8.6 wechselt nicht — deshalb hier **bewusst nicht
angefasst**, aber benannt. Plan 2 sollte entscheiden, ob die Symlinks blockweise mitziehen.

---

## 8 Arbeitsweise und Werkzeug-Stand

Unverändert: **Claude Code plant, opencode/M3 führt aus, kein Advisor in der Ausführung**
(N4). Ersatz bleibt die §0.5-Selbstprüf-Checkliste plus die Nikinger-Sichtprüfung. Neu bzw.
geändert in dieser Phase:

- **Der Vision-Plugin-Pfad ist tot, und zwar gemessen.** `minimax/MiniMax-M3` steht im
  models.dev-Cache als `attachment: true` und sieht Bilder **nativ** (Lauf A `--pure`:
  0 Tool-Calls, korrekte Antwort). Mit Plugin: **9 Tool-Calls**, FilePart gelöscht, Selbstbau
  per `curl`. Ursache: `removeProcessedImageParts()` amputiert bei `models: ["*"]` auch das
  Modell, das die Krücke nicht braucht. **Zweitbefund:** das OpenCode-Web-UI hat keinen
  Tool-Result-Bild-Slot — Konvention §4 („Screenshots im Chat") ist dort **dauerhaft
  unerfüllbar**. Der Workflow ist stattdessen: Playwright schreibt auf Platte → M3 liest mit
  dem eingebauten `read`-Tool → M3 nennt **Pfad und eigene Bewertung**.
- **Konvention §5 ist neu und gilt** (`2a93e67`): zu jedem Sichtprüfungs-Screenshot nennt der
  Agent im Chat **Dateiname** (vorzugsweise aus `screenshots_latest/`) **und** ein
  ein- bis zweisätziges **Checkkriterium**.
- **Eskalationsregel P8.6-O2** ist in dieser Phase eingeführt *und* eingehalten worden —
  Block C hat das `.shell`-Grid nicht angefasst. Plan 2 wird die Regel auslösen (§4.2).
- **Hard Rule 9 gehalten:** kein `pkill -f`, kein `systemctl`-Schreibzugriff, alle
  Wegwerf-Instanzen (Port 18773) über PID-Datei gestoppt.

---

## 9 Was dieser Handover nicht enthält

- **Den Wortlaut der neun Befunde.** `phase8_6_ui_polish/SESSIONS_ARCHIVE.md`, Block
  „2026-09-12 (Block-C-Sichtung Nikinger)" — und die Commit-Message `bc2aa9f`.
- **Die Implementierungsdetails.** Sie stehen im Code und in
  `phase8_6_ui_polish_plan.md` §3–§6. Wer wissen will, *warum* der Layout-Seed ein FNV-1a-Hash
  ist und kein `localStorage`-Snapshot, liest P8.6-M — dort steht auch das verworfene
  Gegenmodell.
- **Die Phase-8.5-Historie.** `PHASE8_5_CLOSEOUT_HANDOVER.md`,
  `phase8_5_picker_release_plan.md` §9.
- **Das geerbte Ledger.** Unverändert offen, P8.6 hat davon nichts angefasst und nichts still
  abgeräumt: `PHASE8_5_CLOSEOUT_HANDOVER.md` §4.7.
- **Einen zweiten P8.6-Plan.** Dieser Handover benennt Entscheidungen; er trifft keine. Das
  Locking ist die Aufgabe der Planungs-Session — insbesondere die Versionsfrage aus §4.3, die
  **ausdrücklich** dem Nikinger gehört.
