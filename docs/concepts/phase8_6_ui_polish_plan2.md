---
status: snapshot
purpose: "Plan 2 der Phase 8.6 — ausfuehrungsreifer Bauplan fuer die neun UX-Befunde der Nikinger-Sichtung vom 2026-09-12. Enthaelt den Layout-Umbau (Befund 5, bewusste Ausloesung von P8.6-O2), die Layering-Korrektur, die Rail-Umkehr und den Gate/Deploy-Weg nach v3.0.2. Ab Step Z ist §9 der kanonische Closeout der Phase."
read-when: vor jedem Block dieser Phase; Plan 1 nur noch fuer die Historie der Bloecke A–D
detail: L2
up: ../../ROADMAP.md
down:
  - ./PHASE8_6_CLOSEOUT_HANDOVER.md                 # Teil-Stand Plan 1, §4 Befund→Lock-Zuordnung, §5 VERIFY-Bilanz
  - ./phase8_6_ui_polish_plan.md                    # Plan 1 (📕) — Locks P8.6-A–P8.6-U, Abnahme 1–32, VERIFY V95–V122
  - ../../phase8_6_ui_polish/CLAUDE.md              # Phase-Head — Modul-Status, Vormerkungen
  - ../../phase8_6_ui_polish/SESSIONS_ARCHIVE.md    # volle Phasenhistorie, Wortlaut der neun Befunde
  - ./p8x_ui_polish_notes.md                        # Inhaltsquelle §1–§10
  - ./sichtpruefung_automation_conventions.md       # §2 Visuelles ist Nikinger-Sache · §5 screenshots_latest
updated: 2026-09-13 (Plan 2 geschrieben — Claude-Code-Planungssession gegen `main`@`26a7cc9`; sechs Nikinger-Entscheidungen, Locks P8.6-W–P8.6-AL, Abnahme P8.6-33–P8.6-54, VERIFY V123–V139)
---
# Phase 8.6 — Plan 2: Layout-Reorg, Layering, Rail-Umkehr (Plan)

> **Wozu dieses Dokument.** Plan 1 ist gebaut, getestet und **nicht ausgeliefert**. Die
> Nikinger-Sichtprüfung vom 2026-09-12 hat statt der Freigabe **neun UX-Befunde**
> zurückgegeben. Plan 2 arbeitet sie ab und führt die Phase zu Gate und Deploy `v3.0.2`.
>
> **Ausführender:** opencode/M3, ohne Advisor (N4, unverändert). Ersatz bleibt die
> §0.5-Selbstprüf-Checkliste plus die Nikinger-Sichtprüfung.
>
> **Einstieg:** `PHASE8_6_CLOSEOUT_HANDOVER.md` einmal ganz lesen, dann hier weiter. Plan 1
> wird **nicht** mehr gebraucht, außer für die Historie der Blöcke A–D — alles, was Plan 2
> braucht, steht hier noch einmal mit eigenen, frisch gemessenen Ankern.

---

## §0 Rahmen

### §0.1 Die sechs Nikinger-Entscheidungen dieser Planungssession (2026-09-13)

| # | Frage | Entscheidung |
|---|---|---|
| **N.7** | Befund 5 löst **P8.6-O2** aus — welche `.shell`-Spaltenbreite? | **`240px 480px 1fr`.** Der Architektur-Schnitt ist eskaliert, vorgelegt und entschieden. Begründung für 480: die Space-Zeilen brauchen gemessen **~433 px** (Glyph + Name + bis zu drei Zähler-Chips, Screenshot `p86_block_c_01` x=650→1083); 380 px reichen nicht. |
| **N.8** | Karte + Editor im rechten Slot — ersetzen oder teilen? | **Ersetzen.** Zusatz des Nikingers, wörtlich: *„Sollte aber weiterhin über ESC wieder rückgängig gemacht werden. Klick auf Item in Karte → Editor öffnet sich → ESC → Karte ist wieder da."* Der ESC-Rückweg ist damit **Abnahmekriterium**, nicht Nebenwirkung. |
| **N.9** | Befund 7b kehrt **C1 / N3-Lesart b** um — bewusst? | **Ja, bewusst.** Zusatz: *„Allerdings ist das Layout trotzdem etwas anders als davor. Abmelden bleibt weiterhin der äußerste Knopf."* Also: beide Knöpfe unten, Reihenfolge **Einstellungen → Abmelden**, Abmelden bleibt letztes Element. |
| **N.10** | Befunde 1+8 — was ersetzt den warmen Stich der Kopfdaten? | **Layer-Tiefe statt Farbe.** Das Kopfdaten-Panel wird kühl wie der Rest und unterscheidet sich nur noch über die Layer-Höhe. |
| **N.11** | Wo steht Plan 2? | **Eigenes Dokument** `phase8_6_ui_polish_plan2.md`. Plan 1 bleibt als 📕-Snapshot unangetastet. |
| **N.12** | `pytest`-Flake (§1.3) — Test oder Produktionscode? | **Beides fixen** — aber *„nicht jetzt, sondern im Plan vermerken"*. Damit ist der Touch in `phase4_auth/authserver/**` eine **ausdrücklich angeordnete, datierte Tabu-Ausnahme** (P8.6-AJ), keine stille Aufweichung. |

**Nicht neu gestellt, weil am 2026-09-13 bereits entschieden** (Handover §4.5): Deploy-Ziel
bleibt **`v3.0.2`** (a) · Block C ist **einzeln gepusht** (b) · Ein-Block-Regel für die
Wurzel-`CLAUDE.md` **verworfen** (c) · **Push ja, Deploy nein** (d). Plan 2 öffnet keine davon
erneut.

### §0.2 Gelockte Entscheidungen

Fortsetzung der Buchstabenfolge aus Plan 1 (dort A–U). **`P8.6-V` wird übersprungen** — Plan 1
hat einen *Schritt* namens „Step V"; ein Lock desselben Namens im selben Phasenkontext wäre
eine Verwechslung, die niemand mehr auflöst. Ebenso entfällt `P8.6-Z` (Step Z).

| ID | Entscheidung | Begründung |
|---|---|---|
| **P8.6-W** | **Plan 2 ist ein eigenes Dokument.** Plan 1 bleibt 📕 und wird **nicht editiert**, außer einer einzigen Zeiger-Zeile in seinem §9. Der **kanonische Closeout der Phase wandert nach Plan 2 §9**. | N.11. P8.6-B („ein Dokument pro Phase") und die INDEX-Klassifikation 📕 („dated, **never edit**") widersprechen sich hier. P8.6-Bs Zweck ist, ein *Konzept+Plan+Handover-Trio* zu verhindern — nicht, einen zweiten Durchgang in einen eingefrorenen Snapshot zu pressen. Ohne die Zeiger-Zeile endete die Phase mit **zwei** leeren §9. |
| **P8.6-X** | **`.shell` wird `240px 480px 1fr`** (`app.css:345`). Das ist die **bewusste, eskalierte und entschiedene** Auslösung von **P8.6-O2**. | N.7. P8.6-O2 fordert Eskalation, nicht Verbot. Die Regel hat funktioniert: Block C hat das Raster nicht angefasst, Plan 2 fasst es nach Vorlage an. Gemessen bei 1440 px: Rail 240 + Liste 480 + Detail **720** = 50 % der Seite für die Karte — P8.6-K wollte „ca. 40 % der gesamten Seite" und lieferte real 302 px (21 %), siehe §1.4. |
| **P8.6-Y** | **Die Übersicht zieht in den `.list`-Slot, die Karte bekommt den `.detail`-Slot allein.** Der Editor **ersetzt** die Karte; **ESC stellt sie wieder her**. | N.8 + Befund 5. Der ESC-Weg ist bereits verdrahtet (`app.js:197` → `Editor.closeEditor()` → `clearDetail()` → `showOverviewPane()`), ebenso der Karten-Knoten-Klick (`graph.js:647` → `selectItem()`). Der Umbau muss diese Kette **erhalten**, nicht erfinden — deshalb steht sie als Abnahmekriterium drin und nicht als Bauaufgabe. |
| **P8.6-AA** | **Kein View-State-Automat.** Die Umschaltung läuft weiter über `shellEl.dataset.view` + `showOverviewPane()`/`clearDetail()`. Neu ist **genau ein** Feld: `state.overview` (Boolean). | `state.js:39-43` dokumentiert wörtlich, warum dieses Repo Modi **nicht** aus `activeSpace === null` ableitet („von genau der Verwechslung schon zweimal getroffen"). Ein eigenes Feld ist die etablierte Antwort — dieselbe Mechanik wie `state.scope`. Ein Enum-Automat wäre ein dritter Mechanismus für dieselbe Frage. |
| **P8.6-AB** | **Layering per Tiefe statt Farbton.** `--panel-meta`, `--panel-meta-head` und `--panel-meta-line` verlieren ihren `--warn`-Bezug. Zuordnung: **Kopfdaten-Panel = Layer 2**, **Editor-Textfläche = Layer 3**, **Append-Zeile = Layer 2**. | N.10 + Befund 8. Gemessene Ursache: `--panel-meta-line: rgba(229,169,60,.22)` **ist** `--warn: #E5A93C` bei 22 % — byte-genau dieselben Kanäle. Der Befund „sieht wie eine Warnung aus" ist keine Wahrnehmungsfrage, sondern eine Tokenfrage. |
| **P8.6-AC** | **P8.6-E bleibt unverändert gültig.** `--bg-void` bleibt an genau drei Stellen. Die durchgängige Layer-Zuordnung aus Befund 1+8 entsteht über `--surface`/`--surface-raised`, **nicht** über mehr Schwarz. | Handover §4.2 lässt Plan 2 die Wahl „P8.6-E ausweiten **oder** ersetzen". Beides wäre falsch: die Befunde verlangen *Konsistenz* der Grautöne, nicht *mehr Layer 0*. P8.6-Es eigene Begründung („ein Layer, der überall liegt, ist kein Layer") trägt unverändert. |
| **P8.6-AD** | **Die rohen Grauwerte außerhalb `:root` werden auf Token gehoben:** `#0E1116` (`app.css:362`, `.rail`), `#131A23` (`:1776`, Login-Grund), `#1A2029` (`:1782`, `.auth-card`). **`#fff` (`:1829`, `.qr-frame`) bleibt** — ein QR-Code braucht echtes Weiß. | Befund 1 („verschiedene Grautöne"). Gemessener Bestand: **10 Flächen-Token in `:root`** plus **4 rohe Hex-Werte außerhalb**. Drei davon sind Flächen ohne Token — genau die Klasse, die der neue Wächter-Test (§8.2) künftig verhindert. Die drei Verläufe bei `:487/492/497` sind **Kategoriefarben** (`--space-own/-shared/-foreign`), keine Grautöne, und bleiben. |
| **P8.6-AE** | **Rail-Umkehr:** `.rail__account` (`app.css:606`, `app.html:42`) trägt wieder **beide** Knöpfe, Reihenfolge **Einstellungen → Abmelden**; Abmelden bleibt das **letzte** Element. Der Test `test_rail_order_settings_before_tree_logout_last` wird **umgekehrt und umbenannt**, Docstring trägt beide Richtungen. | N.9 + Befund 7b. Die Umkehr-statt-Löschen-Mechanik ist **P8.6-I** (Radiogruppe), wörtlich übernommen: „der Testname wird sonst zur Lüge". Der Test ist der einzige Ort, an dem die Anordnungsentscheidung maschinell festgehalten ist. |
| **P8.6-AF** | **Befund 6 ist eine Lock-Abweichung, keine CSS-Wanze.** **P8.6-P** sagt: die Zeile `.overview__space-row` wird **als Ganzes** klickbar. C4 hat stattdessen einen **inneren** `<button class="overview__space-open">` gebaut. Fix = **P8.6-P wiederherstellen**. | Der Hover-Fill in Screenshot `p86_block_c_02` endet bei x=845, die Zeile reicht bis x=1083 — das ist der innere Button, nicht die Zeile. Ein `:hover`-Patch auf die Zeile wäre eine symptomatische Reparatur und würde **P8.5-O** verletzen (Ursache liegt in einer früheren Entscheidung, nicht in der Regel, die man sieht). |
| **P8.6-AG** | **„Alle Items"-Modus (Befund 7a):** bei `state.scope === "all"` zeigt der `.list`-Slot **die Item-Liste**; die Übersichts-Blöcke (Spaces, Space-Name, Zuletzt benutzt) werden **gar nicht gerendert**, nicht nur versteckt. | Befund 7a. Heute rendert `renderOverview()` (`list.js:31`) immer die Daten des **eigenen** Space, unabhängig von `state.scope` — deshalb steht in Screenshot `p86_block_c_04` („Alle Items") der Titel „alpha" samt Spaces-Liste. Nicht rendern statt verstecken, weil die Blöcke im globalen Modus keine wahre Aussage haben. |
| **P8.6-AH** | **Reihenfolge: Messen → Fundament → Umbau → Rest.** Block E misst und baut nichts. Block F legt Token. Block G baut um. Blöcke H und J räumen nach. | Handover §4.1 fordert „Befund 9 zuerst … messen, bevor repariert wird"; **P8.6-U** fordert „Fundament → Fläche → Struktur". Beides hält, sobald man *Messen* von *Bauen* trennt — Block E ist reine Messung und verletzt P8.6-U nicht. |
| **P8.6-AJ** | **Datierte Tabu-Ausnahme:** `phase4_auth/authserver/crypto.py` und zwei Zeilen in `phase4_auth/authserver/store.py` dürfen für den ID-Generator-Fix angefasst werden (§6). **`phase1_storage/storage/**` bleibt zu — keine neunte P1-Contract-Öffnung.** | N.12, ausdrückliche Anordnung vom 2026-09-13. Handover §6 verlangt: „Wenn Plan 2 einen Server-Touch braucht, ist das eine neue Tatsache und wird **angekündigt**, nicht beim Bauen entdeckt." Dies ist die Ankündigung. |
| **P8.6-AK** | **`screenshots_latest/` zieht blockweise mit der Nikinger-Sichtung**, nicht erst beim Phasenwechsel. | Handover §7 delegiert die Entscheidung an Plan 2. Die Symlinks zeigen heute auf **Block B**, obwohl der Nikinger **Block C** gesichtet hat — der Zweck der §5-Konvention („der Agent nennt den Dateinamen des Bildes, das gerade gilt") ist damit verfehlt. Der Auslöser ist die Sichtung, nicht der Phasenwechsel. |
| **P8.6-AL** | **Befunde 3 und 4 werden nach Block G neu gemessen, nicht vorher geplant.** | Block G löscht ihre Ursachen: der Refresh-Knopf zieht mit der Übersicht in den Listen-Slot (Befund 3 verschwindet mit `grid-column: 1 / -1`), und die Karte bekommt den ganzen `.detail`-Slot (Befund 4 verschwindet mit `1fr 40%`). CSS für etwas zu planen, das der nächste Block löscht, ist Arbeit mit negativem Ertrag. |

### §0.3 Tabu — unverändert, mit **einer** datierten Ausnahme

| Pfad | Status in Plan 2 |
|---|---|
| `phase1_storage/storage/**` | **Tabu.** Keine Ausnahme (P8.6-S gilt weiter). |
| `phase2_mcp/mcpserver/**` | **Tabu.** Keine Ausnahme. |
| `phase4_auth/authserver/**` | **Tabu — mit genau einer benannten Ausnahme:** `crypto.py` (neue Funktion) und `store.py` Z. 294 + 393 (zwei geänderte Aufrufe), ausschließlich für §6. Jede andere Zeile bleibt tabu. |
| `phase5_ui/webui/{security,api,serializers,permissions}.py` | **Tabu.** Kein Befund verlangt einen Touch. |
| `phase5_ui/webui/static/**` | **Erlaubt** — Arbeitsfläche der Phase. |
| `phase5_ui/webui/pages.py` | **Erlaubt, nur Template-/Routing-Trivialitäten.** Mehr als eine Zeile ⇒ eskalieren. |
| `phase5_ui/tests/**`, `phase4_auth/tests/**`, `phase8_6_ui_polish/scripts/**` | **Erlaubt.** |

**Tabu-Diff-Pflicht vor jedem Commit:**

```
git diff --stat -- phase1_storage/storage phase2_mcp/mcpserver \
  phase5_ui/webui/security.py phase5_ui/webui/api.py \
  phase5_ui/webui/serializers.py phase5_ui/webui/permissions.py
```

muss **leer** sein. Für `phase4_auth/authserver` gilt eine **eigene**, engere Probe (§6.4) —
sie darf genau zwei Dateien und die dort genannten Zeilen zeigen, sonst ist sie ein
Abbruchgrund.

### §0.4 Was draußen bleibt

Unverändert aus Plan 1 §0.4: §2.1 Map-Performance · §2.2 Map-Stil · **§2.5 Karte einklappen**
(→ P9; der Nikinger hat die Option in N.8 ausdrücklich **nicht** gewählt) · §4 Edit-in-Place ·
§7 De-AI-Lauf 2 · §8 Tags · §9 Feedback-Button · §10.8 verbundene AI-Sessions · §10.9
Hochkant-/Handy-UI · „Ordner umbenennen" (Analyse: Plan 1 §0.4.1) · CSRF-Origin-Mismatch bei
Wegwerf-Instanzen.

**Neu draußen, benannt statt versteckt:**

- **Die Suche im Übersichts-Zustand.** Der `.list__head` (Krume + Suchfeld + „+") wird im
  Übersichts-Zustand ausgeblendet (§4.2). Eine Suche ohne Space-Kontext wäre eine neue
  Funktion, kein Umbau.
- **Ein Zähler an „Alle Items".** Der Kommentar in `tree.js:245-247` („Lieber keine Zahl als
  eine unwahre") bleibt wörtlich stehen und gilt weiter.

**Geerbtes Ledger** (Handover §4.7 → `PHASE8_5_CLOSEOUT_HANDOVER.md`): unverändert offen.
Plan 2 fasst davon nichts an und räumt nichts still ab.

### §0.5 Selbstprüf-Checkliste (Advisor-Ersatz)

Vor **jedem** Commit, in dieser Reihenfolge:

1. **Tabu-Diff** §0.3 leer? (Plus die enge `authserver`-Probe §6.4, falls Block J.)
2. **`pytest -q`** grün, **≥ 969 passed**? (Baseline §1.3 — und den Flake dort kennen.)
3. **`phase5_ui/scripts/ui_budget.py`** 5/5 im Korridor? (Baseline §1.4.)
4. **Verbotsliste Phase 8 §0.3** eingehalten? Kein Emoji-Icon, kein Gradient-Branding, kein
   3er-Card-Grid, **keine dekorative Farbe**, keine neue Schriftfamilie, kein Element, dessen
   Erkennbarkeit allein von Transparenz/Blur abhängt.
5. **Kein rohes `rgba(62,141,243`** außerhalb `:root`, **und ab Block F kein roher
   Flächen-Hex** außerhalb `:root` (neuer Wächter, §8.2).
6. **Doc-Update im selben Commit** (Hard Rule 8): Modul-/Status-Tabelle **und** `## Session
   stopped`-Block im Phase-Head. Neue `.md` ⇒ Zeile in `docs/INDEX.md`.
7. **Kein `pkill -f`, kein `systemctl`** (Hard Rule 9). Wegwerf-Instanzen nur über PID-Datei
   oder Port stoppen.
8. **Ein `## Session stopped`-Block pro Session** (P8.6-T), danach
   `scripts/rotate_session_block.sh phase8_6_ui_polish`. **Nie von Hand rotieren** — die
   Hand-Rotation vom 2026-09-10 hat 72 Zeilen mitten im Satz abgeschnitten.

**Eskalationsregeln, beide gültig:** **P8.5-O** (Ursache liegt in einer früheren CSS-Regel oder
in der Kaskade ⇒ nicht symptomatisch patchen, eskalieren; Erkennungsmerkmal: „der Wert stimmt
im Quelltext, sieht im Browser aber anders aus"). **P8.6-O2** ist für Plan 2 **verbraucht** —
sie ist ausgelöst, vorgelegt und durch P8.6-X entschieden. Ein *weiterer* Griff ins
`.shell`-Raster über `240px 480px 1fr` hinaus löst sie erneut aus.

---

## §1 Step 0' — Haushalt und Verifikation

**Dieser Schritt ist in der Planungssession am 2026-09-13 durchgeführt worden**, gegen
`main`@`26a7cc9`. Der ausführende Agent **behebt** die Befunde, er sucht sie nicht erneut.

### §1.1 Befund: Doku-Hygiene ist sauber — bis auf eine Zahl

Repo-weiter Scan über 109 `.md`-Dateien (ohne `.venv/`):

| Prüfung | Ergebnis |
|---|---|
| Unauflösbare `up:`/`down:`-Links | **0** ✅ |
| Fehlende L1-Header-Cards | **0 echte** — die fünf Treffer sind die vier dokumentierten INDEX-Ausnahmen (`docs/UPDATE_LOG.md` maschinell geparst · `.claude/RESUME.md` Harness · `phase5_ui/vendor/lucide/README.md` + `phase5_ui/THIRD_PARTY_LICENSES.md` Vendor/Lizenz) plus `docs/PROJECT_SESSION_LOG.md`, das **hat** eine Card (`status: archive`) ✅ |
| Fehlende INDEX-Zeilen | **0 echte** — die Treffer sind Test-Fixtures (`phase6_shares/tests/golden/*.md`, dokumentierte Ausnahme) und `docs/INDEX.md` selbst ✅ |

**„Nichts zu tun" ist hier das Ergebnis.** Nur eine Sache ist zu tun, und die ist echt:

### §1.2 Befund: `docs/INDEX.md` hatte **97 Byte** Luft — in dieser Session behoben

Bei Sessionbeginn: `docs/INDEX.md` = **38.815 B**. Abnahmekriterium **P8.6-4** fordert
**≤ 38 KB = 38.912 B**. Headroom: **97 Byte** — und Plan 2 fügt eine Zeile von ~1,2 KB hinzu.

**In dieser Planungssession erledigt, nicht an Block E delegiert** (eine neue `.md` braucht
ihre INDEX-Zeile nach Hard Rule 8 im *selben* Commit — das Kriterium wäre sonst genau dort
gerissen, wo es niemand gesucht hätte):

| Schritt | Wirkung |
|---|---|
| Sieben Zeilen **geschlossener** Phasen gestrafft (P7-, P6- und P8.5-Handover, P8.5-Plan, P8.5-Head, P4-Head, P3-Head) | **−1.549 B** |
| Plan-2-Zeile + Abschnitts-Überschrift + `updated:`-Eintrag | **+1.205 B** |
| **Stand** | **38.471 B**, **441 B Luft** |

Die `updated:`-Frontmatter-Kette war hier **nicht** die Quelle — sie wiegt in dieser Datei nur
554 B über drei Einträge. Das ist der Unterschied zur Wurzel-`CLAUDE.md`, wo am 2026-09-13
**69 %** der Dateigröße in der Kette steckten. Gemessen, nicht angenommen.

**Für Block E bleibt:** nichts. **Für Step Z bleibt:** die Gegenprobe, weil jeder weitere
Block eine Zeile hinzufügen kann. `[VERIFY] V124`.

> **Der Inhalt ist nicht verloren gegangen.** Gestrafft wurde ausschließlich Narrativ, das im
> verlinkten Dokument selbst steht. Was ein L0-Index leisten muss — *finden* und *entscheiden,
> ob Lesen sich lohnt* —, steht in jeder der sieben Zeilen weiter drin. Bei
> `PHASE8_5_CLOSEOUT_HANDOVER.md` ist der Verweis auf **§4.7 (geerbtes Ledger)** dabei
> ausdrücklich **hinzugekommen**, weil Plan 2 §0.4 darauf zeigt.

### §1.3 Befund: die `pytest`-Baseline ist **969 + 1 Flake**, nicht 970

Gemessen 2026-09-13 gegen `26a7cc9`: **`1 failed, 969 passed in 114.29 s`**.

```
FAILED phase4_auth/tests/test_authctl.py::test_revoke_kills_the_family
  authctl revoke: error: argument --family-id: expected one argument
```

**Isoliert läuft der Test grün** (1 passed in 0.37 s), ebenso das ganze `phase4_auth/tests/`
(261 passed). Es ist **keine** Testreihenfolgen-Abhängigkeit.

**Ursache, gemessen:** `store.create_family()` (`phase4_auth/authserver/store.py:393`) erzeugt
`family_id = crypto.new_secret(16)` = `secrets.token_urlsafe(16)`, Alphabet `[A-Za-z0-9_-]`.
Beginnt der Wert mit `-`, hält `argparse` ihn für eine Option und nicht für den Wert von
`--family-id` (`phase4_auth/scripts/authctl.py:199`). Gemessene Häufigkeit über 200.000 Ziehungen:

| Erstes Zeichen | Anteil | Wirkung |
|---|---|---|
| `-` | **1,569 %** | `argparse` bricht ab — Test rot, **CLI für einen Menschen ebenfalls kaputt** |
| `_` | 1,584 % | unkritisch |

Das trifft **P8.6-28 / P8.6-46** („`pytest` grün") in rund **einem von 64** Vollläufen — und es
ist nicht nur ein Testproblem: `authctl revoke --family-id <id>` scheitert für einen echten
Operator bei jeder 64. Familie.

**Behandlung: Block J (§6), beide Hälften, auf ausdrückliche Anordnung (N.12).**

**Baseline für alle Gates dieser Phase: `≥ 969 passed, ≤ 1 failed und dieses eine failed
ausschließlich der oben genannte Flake`. Ab Block J: `≥ 972 passed, 0 failed`.**

### §1.4 Befund: UI-Budget und Latenz sind im Korridor (gemessen)

`phase5_ui/scripts/ui_budget.py`, 2026-09-13: **5/5 im Zielkorridor**.

| Messgröße | Wert | Ziel |
|---|---|---|
| `app.js + app.css + Font` (gzip) | **137,5 KB** | < 250 KB |
| Erstaufruf `/ui/` bis interaktiv | **146,7 KB** | < 400 KB |
| `GET /api/v1/overview` (informativ) | **372,9 ms** | — |

Die 372,9 ms bestätigen **V108** ein zweites Mal: die 863 ms vom Phasenstart waren Last auf
dem alten Mini-PC, keine Regression. `app.css` liegt bei **21,1 KB** gzip — Block G fügt
netto wenig hinzu (das `.overview`-Grid und seine Media-Query **entfallen**, siehe §4.6).

### §1.5 Befund: die Anker aus Plan 1 sind gedriftet — Beleg

**V106 ist verbraucht** (gegen `d1af51b` gemessen, 841 Zeilen Produktcode später). Der Beleg,
dass ein neuer Sammelmarker nötig ist, steht in Plan 1 selbst:

| Plan-1-Anker | Behauptet | Ist (`26a7cc9`) |
|---|---|---|
| `.shell`-Grid (P8.6-O2) | `app.css:327-332` | **`app.css:345-350`** (+18) |
| `.overview__graph` (P8.6-L) | `app.css:915-924` | **`app.css:1074-1080`** (+159) |
| `renderRail()` (P8.6-J) | `tree.js:242-255` | **`tree.js:297-318`** (+55) |

**`[VERIFY] V123` — neuer Sammelmarker:** alle `Datei:Zeile`-Anker **dieses** Plans gelten
gegen `main`@`26a7cc9`. **Bei Drift melden, nicht raten.** Die drei Commits zwischen `bc2aa9f`
(im Handover genannt) und `26a7cc9` sind **reine Doku-Commits** — **gemessen, nicht aus den
Commit-Messages geschlossen:** `git diff --stat bc2aa9f..26a7cc9 -- phase5_ui/webui/static`
ist **leer**, und `git diff --name-only bc2aa9f..26a7cc9` nennt **neun** Dateien, alle unter
`docs/`, `phase8_6_ui_polish/` oder im Wurzelverzeichnis. Die `static`-Anker haben sich
zwischen beiden Ständen also nicht bewegt.

### §1.6 Abschluss Step 0'

**Step 0' ist mit dieser Planungssession abgeschlossen.** Es bleibt **keine** Aufgabe für den
ausführenden Agenten: Doku-Hygiene sauber (§1.1), INDEX-Budget hergestellt (§1.2), Baselines
gemessen (§1.3/§1.4), Anker-Drift belegt und der neue Sammelmarker gesetzt (§1.5).

Der Commit dieser Session enthält: `phase8_6_ui_polish_plan2.md` (neu, mit L1-Card) ·
`docs/INDEX.md` (sieben Zeilen gestrafft, Plan-2-Zeile, Abschnitts-Überschrift, `updated:`) ·
Phase-Head (Modul-Status + **ein** `## Session stopped`-Block) · `ROADMAP.md` ·
Wurzel-`CLAUDE.md`. Danach `scripts/rotate_session_block.sh phase8_6_ui_polish`.

**Der ausführende Agent beginnt bei Block E.**

---

## §2 Block E — **Messen, nicht bauen** (Befund 9)

> **Dieser Block ändert keine einzige Zeile Produktcode.** Sein Ergebnis ist ein Messprotokoll
> im Phase-Head plus ein Skript. Wer hier CSS anfasst, hat den Block missverstanden.

### §2.1 Warum Befund 9 zwei Befunde ist

Der Nikinger hat ihn **auf der Produktion** reproduziert. Die Produktion ist `6f19a8f`
(**P8.5**, `v3.0.1`) — dort gibt es Block C **nicht**. Damit zerfällt der Befund:

| | **9a — Produktion (`6f19a8f`)** | **9b — aktueller `main` (`26a7cc9`)** |
|---|---|---|
| `.overview` | `flex: 1; overflow-y: auto` (live `app.css:802-806`) | `display: grid; flex: 1; min-height: 0; **overflow: hidden**` (`app.css:908-925`) |
| `@media (max-width:1280px)` | nur Rail-Kollaps, kein `.overview`-Eintrag | zusätzlich `grid-template-columns: 1fr; grid-template-rows: auto auto auto; height: auto` (`app.css:1877-1885`) |
| Ursache | **unbekannt — zu messen** | **Hypothese:** `flex: 1` gewinnt gegen `height: auto`, `overflow: hidden` bleibt ⇒ **kein Scroll-Container**, Inhalt wird geklippt statt scrollbar |
| Sichtbar in | — | `p86_block_c_06_karte_unter_liste_1200px.png`: „VERKNÜPFUNGEN" (y=623) liegt über der Recent-Zeile „Styleguide pflegen" (y=637), die Karte ist am unteren Rand abgeschnitten |

**Die Falle, die dieser Block vermeidet:** 9b reparieren und „behoben" melden. 9a bliebe dann
**live auf `v3.0.1`** stehen — der eine Befund, der heute wirklich einen Nutzer trifft.

### §2.2 E1 — Die CDP-Probe

Neues Skript **`phase8_6_ui_polish/scripts/p86_viewport_probe.py`** (Playwright, venv
`~/.claude-code-tools/e2e-venv`). Signatur:

```python
def probe(page, width: int, height: int = 900) -> dict
def main() -> int        # --base-url, --widths 1024,1200,1440, --out <json>, --label <str>
```

Pro Breite erhebt `probe()`:

| Feld | Wie | Wofür |
|---|---|---|
| `rects` | `getBoundingClientRect()` für `#shell`, `#list`, `#detail`, `#detail-overview`, `.overview__col-left`, `.overview__col-right`, `#overview-graph`, `#overview-refresh`, `.rail__account` | Geometrie, Überlappung |
| `styles` | `getComputedStyle()` → `overflow`, `overflowY`, `height`, `display`, `gridTemplateRows`, `flex` für `#detail`, `#detail-overview`, beide Spalten | die 9b-Hypothese steht oder fällt hier |
| `clipped` | `scrollHeight > clientHeight && overflowY === "hidden"` je Container | **kein Scroll-Container** — der eigentliche Vorwurf |
| `reachable` | `document.elementFromPoint(cx, cy)` auf den Mittelpunkt **jedes** `button`-Elements; `true`, wenn der Treffer der Knopf selbst oder ein Nachfahre ist | **beweist** „nicht mehr klickbar", statt es zu behaupten |
| `offscreen` | `rect.bottom > innerHeight \|\| rect.top < 0` je Knopf | unterscheidet „verdeckt" von „außerhalb" |

Ausgabe: **JSON auf stdout** (Hard Rule 7 — Logging nach stderr), plus ein Screenshot je
Breite nach `docs/screenshots/p86_probe_<label>_<width>.png`.

### §2.3 E2 — Zweimal laufen lassen

| Lauf | Ziel | Zugriff |
|---|---|---|
| **E2a** | Wegwerf-Instanz auf aktuellem `main` (Port 18773, §7.1) | voller Zugriff |
| **E2b** | **Produktion** `https://<SPACE_PUBLIC_BASE_URL>` | **ausschließlich lesend** — GET/Render, kein POST, kein Schreiben, kein `systemctl`, kein Service-Touch |

> **E2b ist eine Sichtprüfung, kein Eingriff.** Playwright loggt sich mit den vorhandenen
> Zugangsdaten ein und sieht sich Seiten an. Wenn der Login-Pfad im Browser-Kontext an CSRF
> scheitert (Plan 1 §7.2, Handover §4.3), **wird E2b abgebrochen und dem Nikinger gemeldet** —
> nicht mit einem Workaround erzwungen. Ein gemessenes „geht nicht" ist ein Ergebnis.

### §2.4 E3 — Das Protokoll

In den Phase-Head, als Tabelle: pro Breite und pro Ziel (`main` / Produktion) die Zahl der
Knöpfe mit `reachable === false`, welche das sind, und ob `clipped` für `#detail-overview`
wahr ist.

**`[VERIFY] V125`:** trägt 9a dieselbe Ursache wie 9b, eine andere, oder **gar keine**
(d. h. der Befund ist auf Produktion nicht reproduzierbar und war eine Fehlzuordnung)?
**Melden, nicht raten.**

**`[VERIFY] V126`:** wie viele Knöpfe sind bei 1024 px unerreichbar? Unter 1024 greift
`@media (max-width: 1024px)` mit `.shell { grid-template-columns: 64px 1fr }` und
`data-view`-Umschaltung — ein **drittes** Layout, das die Sichtprüfung nie gesehen hat.

### §2.5 Abschluss Block E

Ein Commit: Skript + Protokoll + Screenshots. **Kein Produktcode.**
Tabu-Diff leer (trivial). `pytest` unverändert.

---

## §3 Block F — Layering (Befunde 1 + 8)

**P8.6-U-Position: Fundament.** Block F legt die Flächen fest, die Block G dann verschiebt.
Andersherum müsste Block G seine neuen Flächen zweimal einfärben.

### §3.1 F1 — Die Kopfdaten werden kühl (P8.6-AB)

`app.css:107-111`:

| Token | Ist | Soll | Warum |
|---|---|---|---|
| `--panel-body` | `#10151B` | **unverändert** | Layer 3, die Textfläche. Korrekt so. |
| `--panel-body-head` | `#161C24` | **unverändert** | Layer 2 über Layer 3. Korrekt so. |
| `--panel-meta` | `#1A1611` | **`var(--surface)`** (`#14181D`) | Layer 2, kühl. |
| `--panel-meta-head` | `#221C15` | **`var(--surface-raised)`** (`#1B2027`) | Layer 2, angehoben — der Klapp-Kopf ist das *Bedienelement* des Panels. |
| `--panel-meta-line` | `rgba(229,169,60,.22)` | **`var(--line)`** | **Das ist der Befund.** `(229,169,60)` **ist** `--warn: #E5A93C`. |

**Der Kommentarblock bei `app.css:103-106`** („Zwei Panelfarben, damit ‚wo kommt der Text hin'
und ‚wo kommen die Kopfdaten hin' ohne Beschriftung unterscheidbar sind: … die Kopfdaten
bekommen einen warmen Stich") **wird nicht gelöscht, sondern datiert ersetzt** — mit der
Begründung von N.10: die Unterscheidung bleibt, sie läuft ab jetzt über Layer-Höhe statt
Farbton.

> **Die verworfene Alternative, benannt:** den Stich kühl-blau statt warm-gelb zu machen. Das
> hätte die Farbkodierung erhalten, aber eine zweite Nicht-Akzent-Farbe eingeführt — genau
> „dekorative Farbe", Phase-8-§0.3-Verbot Punkt 4. Der Nikinger hat in N.10 die Layer-Tiefe
> gewählt.

### §3.2 F2 — Die Layer-Zuordnung des Editors vervollständigen

Befund 8 wörtlich: *„YAML-Header … gehört in Layer 2. Editor selbst in Layer 3. ‚Zeile
Einfügen' in Layer 2."*

| Element | Anker | Layer | Maßnahme |
|---|---|---|---|
| `.panel--meta` (Kopfdaten) | `app.css:1345` | **2** | über F1 erledigt |
| `.panel--body` (Textfläche) | `app.css:1385` | **3** | `--panel-body`, bereits korrekt — **prüfen, nicht ändern** |
| `.editor__textarea` | `app.css:1584` | **3** | erbt von `.panel--body`; **`[VERIFY] V127`** — setzt sie einen eigenen Hintergrund? |
| `.editor__append` („Zeile anhängen") | `app.css:1606` | **2** | **hier ist der Bau**: eigene Fläche `var(--surface)` + Oberkante `1px solid var(--line)` |

### §3.3 F3 — Die vier rohen Grautöne (P8.6-AD)

| Anker | Wert | Träger | Maßnahme |
|---|---|---|---|
| `app.css:362` | `#0E1116` | `.rail`-Verlauf | neuer Token **`--rail-top`** in `:root`, direkt unter `--surface-raised`, mit Kommentarzeile |
| `app.css:1776` | `#131A23` | Login-Grund (radial) | neuer Token **`--auth-glow`** |
| `app.css:1782` | `#1A2029` | `.auth-card`-Verlauf | neuer Token **`--auth-card-top`** |
| `app.css:1829` | `#fff` | `.qr-frame` | **bleibt.** Kommentar ergänzen: ein QR-Code braucht echtes Weiß, das ist kein Flächenton |

**Nicht anfassen:** `app.css:487/492/497` (`#5DA8F7/#3A7DCB`, `#48C9B6/#259C8C`,
`#9CA3B0/#6F7686`) — das sind die drei Space-Kategoriefarben, keine Grautöne.

### §3.4 F4 — Der Wächter

Neuer Test `test_no_raw_surface_hex_outside_root` (§8.2). **Er ist der eigentliche Ertrag von
Block F**: er schließt eine Fehlerklasse, nicht eine Instanz — dieselbe Logik, die
`test_every_css_var_reference_is_defined` in Block A zum wichtigsten der sieben gemacht hat.

### §3.5 Abschluss Block F

Ein Commit. Erwartung: `pytest` **+1** (der neue Wächter). `ui_budget` 5/5.
**Screenshot-Pflicht (§5-Konvention):** je ein Bild vom geöffneten Editor **vorher/nachher**
nach `docs/screenshots/p86_block_f_{01,02}_*.png`, Checkkriterium in einem Satz.
`screenshots_latest/` **mitziehen** (P8.6-AK).

---

## §4 Block G — Der Layout-Umbau (Befund 5, dann 3/4/6/7a)

> **Der größte Block der Phase.** Er löst P8.6-O2 aus — bewusst, vorgelegt, durch P8.6-X
> entschieden. Hier wird das seit Phase 5 unveränderte `.shell`-Raster verschoben.

### §4.1 G1 — Das Raster (P8.6-X)

`app.css:345`:

```css
.shell { grid-template-columns: 240px 480px 1fr; }   /* war: 240px 380px 1fr */
```

**Und die zwei Media-Queries mitziehen:**

| Anker | Ist | Soll |
|---|---|---|
| `app.css:1872` | `.shell { grid-template-columns: 64px 380px 1fr; }` | **`64px 480px 1fr`** |
| `app.css:1892` | `.shell { grid-template-columns: 64px 1fr; }` | **unverändert** (zweispaltig, `data-view`-Umschaltung) |

**Gemessene Folge bei 1440 px:** Rail 240 + Liste 480 + Detail **720 px = 50 % der Seite** für
die Karte. Heute sind es 302 px = 21 %. P8.6-K zitierte §1 mit „ca. 40 % der gesamten Seite" —
das war nie erfüllt, weil `1fr 40%` **40 % des Detail-Slots** meint, nicht der Seite
(756 px Inhaltsbreite × 40 % = 302 px; Vorhersage und Messung stimmen auf das Pixel überein).

### §4.2 G2 — Die Übersicht zieht um (P8.6-Y)

**DOM-Umzug in `app.html`.** Ziel-Struktur:

```
section.list#list
  header.list__head                 <- unverändert, aber im Übersichts-Zustand hidden
  div.overview#list-overview        <- NEU hier: Inhalt aus head-row + col-left
    header.overview__header         (Titel + #overview-refresh)   <- Befund 3 loest sich hier
    div.legend
    ol.overview__spaces#overview-spaces
    h2.overview__heading  "Zuletzt benutzt"
    ol.overview__recent#overview-recent
  ol.list__rows#list-rows
  div.list__empty#list-empty

section.detail#detail
  button.detail__back#back-button
  div.detail__graph#detail-graph    <- war: div.overview__col-right
    h2.overview__heading  "Verknuepfungen"
    div.overview__graph#overview-graph   (Toolbar, Canvas, Empty bleiben unveraendert)
  div#detail-readonly
  div#detail-editor
```

**Die drei Wrapper-DIVs aus C3 (`overview__head-row`, `overview__col-left`,
`overview__col-right`) entfallen** — sie existierten nur für das zweispaltige Grid, und das
Grid entfällt mit dem Umzug.

**IDs, die sich NICHT ändern dürfen:** `#overview-title`, `#overview-refresh`,
`#overview-spaces`, `#overview-recent`, `#overview-graph`, `#overview-graph-toolbar`,
`#overview-graph-zoom`, `#overview-graph-empty`. Sie werden aus `list.js`, `graph.js` und
`app.js:134` per `getElementById` geholt; ein Rename wäre ein Umbau ohne Ertrag.
**`#detail-overview` wird zu `#list-overview`** — diese eine ID ändert sich, Aufrufstelle ist
`editor.js` (`overviewEl`).

#### §4.2.1 Die Hoehenkette von `.detail__graph` — **der gefaehrlichste Teil des Umbaus**

**Das Grid, das §4.6 loescht, war die definite Hoehe der Karte.** `.overview__graph`
(`app.css:1074-1080`) hat **keine** eigene `height`; ihr Canvas hat `height: 100%`
(`app.css:1081-1085`). Die Hoehe kam bisher aus zwei Zeilen, die beide entfallen:
`grid-template-rows: auto 1fr` (`:911`) und `.overview__col-right .overview__graph { flex: 1 }`
(`:933`).

**Wer §4.2 und §4.6 woertlich ausfuehrt und nichts nachlegt, baut den V112-Bug wieder ein** —
denselben, den P8.6-L in genau diesen Worten beschreibt: *„Prozentuale Hoehen brauchen einen
Elternteil mit definiter Hoehe; `min-height` ist keine."* Das Canvas faellt dann auf seine
Attribut-Hoehe zurueck, waehrend `resize()` (`graph.js:474-484`) die Attribute aus
`getBoundingClientRect()` setzt — die Rueckkopplung, die unten abschneidet.

**Die Ersatzkette wird vollstaendig hingeschrieben, nicht abgeleitet.** `.detail` ist bereits
`display: flex; flex-direction: column; min-height: 0` (`app.css:372-376`), also:

```css
/* Phase 8.6 Plan 2 G2 (P8.6-Y): Ersatz fuer die geloeschte Grid-Zeile `auto 1fr`.
   .detail ist ein Flex-Column-Container -- .detail__graph holt sich die Resthoehe mit
   `flex: 1` und gibt sie mit `min-height: 0` an das Kind weiter (ohne `min-height: 0`
   waere die Flex-Basis der Inhalt, und die Karte waechst statt zu fuellen). Die zweite
   Ebene ist noetig, weil zwischen .detail__graph und .overview__graph noch die
   `.overview__heading`-Ueberschrift steht. */
.detail__graph {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
  padding: calc(var(--space) * 4);
}
.detail__graph .overview__graph { flex: 1; min-height: 0; }
```

**`[VERIFY] V138` — vor dem Commit messen, nicht annehmen:** `#overview-graph`
`getBoundingClientRect().height` > 0 **und** unterer Rand innerhalb des Viewports, bei allen
drei Breiten. `p86_viewport_probe.py` aus Block E erhebt das bereits — der Nachher-Lauf (V130)
deckt es mit ab.

> **Warum das hier als eigener Unterabschnitt steht und nicht als Nebensatz in §4.6:** die
> Loeschung und der Ersatz stehen in **zwei verschiedenen Abschnitten** des Plans. Genau diese
> Aufteilung ist der Weg, auf dem ein ausfuehrender Agent die eine Haelfte umsetzt und die
> andere uebersieht. Der Regressionswaechter dafuer ist
> `test_detail_graph_has_a_definite_height_chain` (§8.2).

### §4.3 G3 — `state.overview` (P8.6-AA)

**Ein Boolean in `state.js`**, eingefügt direkt hinter `scope` (`state.js:43`), mit einem
Kommentar im Stil der Nachbarn:

```js
// Phase 8.6 Plan 2 G3 (P8.6-AA): true = der Listen-Slot zeigt die Uebersicht (Spaces +
// Zuletzt benutzt), false = er zeigt die Item-Liste. Eigenes Feld statt einer Ableitung
// aus `activeSpace === null`, aus demselben Grund wie `scope` daneben -- dieses Repo ist
// von genau der Verwechslung schon zweimal getroffen worden.
overview: true,
```

**Wer setzt ihn:**

| Aufrufstelle | Anker | Setzt |
|---|---|---|
| `#home-button`-Klick | `app.js:99` | **`true`** |
| `navigate(spaceName, bucket)` | `tree.js:37` | `false` |
| `navigateFolder(spaceName, folderPath)` | `tree.js:45` | `false` |
| `navigateAll()` | `tree.js:22` | `false` |
| `activateView(spaceName)` | `tree.js:279` | `false` |

**Wo im `#home-button`-Handler, ist nicht egal.** Der Handler lautet heute
(`app.js:99-105`):

```js
Editor.closeEditor().then(function (proceed) {
  if (proceed === false) return;
  navigateAll();          // <- entfaellt
  loadGraphPanel();
})
```

`closeEditor()` ruft `clearDetail()`, und `clearDetail()` **rendert bereits**
(`editor.js:68-70`: `showOverviewPane()`, `renderRail()`, `renderList()`). Wird
`state.overview = true` **innerhalb** des `.then()` gesetzt, hat `clearDetail()` schon mit dem
alten `false` gerendert — der Nutzer sieht einen Frame lang die Item-Liste.
**`state.overview = true` wird deshalb VOR dem `closeEditor()`-Aufruf gesetzt**, nicht im
`.then()`. Bricht der Nutzer die Rückfrage ab (`proceed === false`), wird es im
`else`-Zweig wieder auf den vorherigen Wert zurückgesetzt — sonst wechselt ein *abgebrochener*
Navigationsversuch trotzdem die Ansicht.

> **Eine Zeile wird durch diesen Umbau tragend, die es vorher nicht war.** `clearDetail()`
> setzt `state.scope = "space"` (`editor.js:78`). Der Kommentar darüber erklärt das als
> Advisor-Fund, und der alte Handler hat den Reset unmittelbar danach mit `navigateAll()`
> wieder überschrieben — die Zeile sah also wirkungslos aus. **Nach dem Wegfall von
> `navigateAll()` ist sie das einzige, was `isGlobalScope()` beim Rückweg aus „Alle Items"
> wieder falsch macht** — und damit das einzige, was `showOverview` überhaupt wahr werden
> lässt. Wer sie später als toten Code entfernt, bricht den Home-Knopf. Der Kommentar dort
> wird um diesen Satz ergänzt.

> **Befund aus der Planung, der hier hängt:** `#home-button` ruft heute **`navigateAll()`**
> (`app.js:99-105`) — „Übersicht" und „Alle Items" sind **dieselbe Aktion**. Genau das ist die
> Doppelung, die der Nikinger in §1 der Notizen gemeint hat; **V110** („ist der bestehende
> Mechanismus der Kippschalter?") ist damit als *negativer* Befund beantwortet: es gibt heute
> gar keinen zwei-Zustands-Schalter, es gibt zwei Knöpfe für **einen** Zustand.
> **G3 trennt sie:** `#home-button` → Übersicht, `.tree__scope` → globaler Scope.
> `navigateAll()` aus dem Home-Handler **entfernen**; `loadGraphPanel()` bleibt.

### §4.4 G4 — Das Rendern umschalten

`list.js :: renderList()` (`list.js:311`) und `renderOverview()` (`list.js:31`) bekommen einen
gemeinsamen Vorspann. Neue, **exportierte** Funktion in `list.js`:

```js
export function renderListSlot() {
  var showOverview = state.overview && !isGlobalScope();
  listHeadEl.hidden     = showOverview;
  listOverviewEl.hidden = !showOverview;
  listRowsEl.hidden     = showOverview;
  if (showOverview) {
    // V139: listEmptyEl gehoert renderList() (list.js:317/346) und wird hier NICHT
    // gerendert -- ohne diese Zeile bliebe der "Erste Notiz anlegen"-Block aus einem
    // leeren Space unter der Uebersicht stehen.
    listEmptyEl.hidden = true;
    renderOverview();
  } else {
    renderList();   // setzt listEmptyEl.hidden selbst, in beiden Zweigen
  }
}
```

- **`#list-empty` hat genau einen Eigentümer, und das bleibt `renderList()`.**
  `renderListSlot()` schaltet es im Übersichts-Zweig nur **aus** und schreibt es im
  Listen-Zweig **nicht** — sonst gäbe es zwei Schreiber für eine Sichtbarkeit, und der
  zweite überschreibt die Fallunterscheidung des ersten (`list.js:317` leer-mit-Grund
  vs. `:346` nicht leer). **`[VERIFY] V139`:** aus einem leeren Space auf „Übersicht"
  klicken — steht „Erste Notiz anlegen" noch unter den Spaces?
- `listHeadEl.hidden = showOverview` ist §0.4 („Suche im Übersichts-Zustand bleibt draußen").
- `!isGlobalScope()` ist **P8.6-AG / Befund 7a**: im „Alle Items"-Modus ist `showOverview`
  **immer** falsch, also wird `renderOverview()` **gar nicht aufgerufen** — die Blöcke
  entstehen nicht, statt versteckt zu werden.

**Aufrufstellen umstellen** (überall dort, wo heute `renderList()` **oder** `renderOverview()`
direkt gerufen wird): `editor.js :: clearDetail()` (`editor.js:69`), `tree.js ::
activateView()`, `list.js :: loadItems()` (`list.js:475`), `loadOverview()` (`list.js:137`),
`app.js:276`. **`[VERIFY] V128` — vollständige Aufrufliste gegen `26a7cc9` prüfen; bei Drift
melden.**

### §4.5 G5 — Die Karte im Detail-Slot, Editor ersetzt sie, ESC bringt sie zurück (P8.6-Y/N.8)

`editor.js :: showOverviewPane()` (`editor.js:49`) benennt nur um, was es schon tut:

```js
export function showOverviewPane() {
  graphPaneEl.hidden     = false;     // war: overviewEl
  detailReadonlyEl.hidden = true;
  detailEditorEl.hidden   = true;
  editorPart.detach();
  shellEl.dataset.view = "list";
}
```

**Die ESC-Kette existiert bereits vollständig und wird nicht gebaut, sondern bewiesen:**

| Schritt | Anker | Status |
|---|---|---|
| Klick auf Karten-Knoten → Editor | `graph.js:647` `selectItem(pressStart.node.id)` | ✅ vorhanden |
| Editor belegt den Detail-Slot | `editor.js:404` `shellEl.dataset.view = "detail"` | ✅ vorhanden |
| **ESC** → Editor zu | `app.js:197` `else if (state.selectedId !== null) Editor.closeEditor()` | ✅ vorhanden |
| `closeEditor()` → `clearDetail()` → `showOverviewPane()` | `editor.js:419,68` | ✅ vorhanden |

**Aufgabe von G5 ist also Erhaltung, nicht Konstruktion** — plus ein Regressionstest (§8.2)
und Station 5 des Smoke-Skripts (§7.2). **`[VERIFY] V129`:** überlebt die Kette den DOM-Umzug
aus G2? Konkret: `graph.js` liest `#overview-graph` — der Knoten wandert mit, aber sein
**Elternteil** wechselt von `.overview__col-right` nach `.detail__graph`; `resize()`
(`graph.js:474-484`) rechnet gegen `getBoundingClientRect()` des Elternteils.

### §4.6 G6 — Was ersatzlos gelöscht wird

| Weg | Anker | Warum |
|---|---|---|
| `.overview`-Grid (`display: grid`, `grid-template-*`, `gap`, `overflow: hidden`) | `app.css:908-925` | Die Übersicht ist im `.list`-Slot ein einspaltiger Fluss. Kein Grid mehr nötig. |
| `.overview__head-row`, `.overview__col-left`, `.overview__col-right` | `app.css:927-933` | Die Wrapper entfallen mit G2. |
| Der `.overview`-Teil von `@media (max-width: 1280px)` | `app.css:1877-1885` | **Das ist die Ursache von Befund 9b.** Sie verschwindet mit dem Grid. |
| `.overview__spaces { max-width: 720px }` | `app.css:986` | Ein 720-px-Cap in einem 480-px-Slot ist wirkungslos und irreführend. |
| `.overview__recent { max-width: 720px }` | `app.css:1152` | dito |

> **Deshalb steht Block E vor Block G.** Wenn 9b hier ohne Messung verschwindet, weiß niemand
> mehr, ob die Ursache getroffen war oder nur das Symptom mit dem Grid abgeräumt wurde. Block E
> hat die Messung vorher gemacht; der **Nachher**-Lauf derselben Probe ist die Gegenprobe
> (`[VERIFY] V130`).

### §4.7 G7 — Die Space-Zeile wieder ganz klickbar (P8.6-AF, Befund 6)

`list.js:31-126` (`renderOverview()`) und `app.css:992-1035`.

**Ist:** `<li class="overview__space-row">` → `<div class="overview__space-name">` →
`<button class="overview__space-open">` (Glyph + Name) · daneben `<div
class="overview__space-counts">` mit Chips.
**Hover liegt auf dem inneren Button** ⇒ der Fill endet vor den Chips ⇒ Befund 6.

**Soll (P8.6-P wiederherstellen):**

- `.overview__space-open` wird zum **Zeilen-Button**: er umschließt Glyph, Namen **und** die
  Chip-Leiste; `<li>` bleibt reiner Listenträger.
- Chips bleiben `<button>` **innerhalb** — verschachtelte `<button>` sind ungültiges HTML,
  deshalb: **Chips werden `<span role="button" tabindex="0">`** mit `click`- **und**
  `keydown`-Handler (Enter/Space). Das `stopPropagation()` aus `list.js:79` bleibt tragend.
- Hover-Regel (Block B, `app.css:1031`) wandert vom inneren Button auf den Zeilen-Button.

> **Die Alternative, die verworfen wird:** `.overview__space-row` selbst klickbar machen
> (Listener auf dem `<li>`). Genau das wäre „eine Behauptung ohne HTML-Semantik" — der
> Kommentar in `list.js:52-56` sagt das schon, und er hat recht. Der Zeilen-**Button** erfüllt
> P8.6-P *und* behält Tab-Stopp und Screenreader-Rolle.
>
> **Warum das der eigentliche Fix ist:** P8.6-P wurde für den Fall geschrieben, dass ein Space
> **lauter Null-Zähler** hat — `list.js:66` (`if (!count) return;`) rendert dann gar keinen
> Chip. Solange der Klick nur am Namen hängt, ist die Zeile in ihrer Fläche fast leer und
> trotzdem nur an einem Streifen anklickbar. Befund 6 ist das sichtbare Symptom desselben
> Konstruktionsfehlers.

### §4.8 G8 — Befunde 3 und 4 gegenprüfen (P8.6-AL)

**Nichts bauen. Messen und melden:**

- **Befund 3** (Refresh über der Karte): `#overview-refresh` steht nach G2 im `.list`-Slot,
  die Karte im `.detail`-Slot. Sie können sich geometrisch nicht mehr überlagern.
  **`[VERIFY] V131`** — mit `p86_viewport_probe.py` gegenprüfen, nicht behaupten.
- **Befund 4** (Karte zu klein): 302 px → **720 px** bei 1440 px. **`[VERIFY] V132`** — messen.
  Reicht das dem Nikinger? Das entscheidet er in der Sichtprüfung, nicht der Agent.

### §4.9 Abschluss Block G

**Ein Commit, nicht mehrere** — G1–G7 sind gegenseitig abhängig (ein halber Umzug ist eine
kaputte Seite). Erwartung: `pytest` **+3** (§8.2), `ui_budget` 5/5, `app.css` **kleiner** als
vorher (das Grid und seine Media-Query entfallen).
**Screenshot-Pflicht:** mindestens 1440 px, 1200 px, 1024 px, Übersicht + Space geöffnet +
Editor offen + Editor per ESC geschlossen → `docs/screenshots/p86_block_g_{01..06}_*.png`,
je ein Satz Checkkriterium. `screenshots_latest/` mitziehen (P8.6-AK).

---

## §5 Block H — Rail-Umkehr und Konto-Dialog (Befunde 7b + 2)

### §5.1 H1 — Einstellungen zurück nach unten (P8.6-AE, Befund 7b)

`app.html:33-35` und `app.html:42-52`.

**Soll:**

```
nav.rail#rail
  div.rail__brand
  button.rail__home#home-button            "Uebersicht"
  div.rail__tree#rail-tree                 (Spaces, dann "Alles" / "Alle Items")
  div.rail__account
    button.rail__action#account-button      "Einstellungen"   <- zurueck hierher
    button.rail__action.action--caution#logout-button  "Abmelden"  <- bleibt letztes Element
```

- `.rail__account` (`app.css:606`) ist `display: flex; gap: 4px` — für zwei gestapelte,
  volle Knöpfe: `flex-direction: column`. **Dann entfällt die Sonderregel
  `@media (max-width:1280px) { .rail__account { flex-direction: column } }`
  (`app.css:1876`)** — sie wird zum Normalfall.
- `.rail__action--account { margin: 0 var(--space) var(--space); width: auto; }`
  (`app.css:418`) gehörte zur Oben-Platzierung und wird geprüft, nicht blind übernommen.
- **N.9 wörtlich:** *„Abmelden bleibt weiterhin der äußerste Knopf."* Reihenfolge im DOM ist
  damit `#account-button`, **dann** `#logout-button`.

**Test `test_rail_order_settings_before_tree_logout_last` (`test_static_routes.py:505`) wird
umgekehrt und umbenannt** zu `test_rail_order_settings_and_logout_at_the_end` — Docstring
trägt **beide** Richtungen mit Datum (2026-09-09 N3-Lesart b → 2026-09-13 N.9). Mechanik
wörtlich wie **P8.6-I**.

### §5.2 H2 — Der Konto-Dialog (Befund 2) — **die Messfrage ist geschlossen**

Handover §4.4 nennt Befund 2 „zuerst eine Messfrage: ob sie fehlen, unsichtbar sind oder
außerhalb des Viewports liegen, ist ungeklärt." **Sie ist in dieser Planungssession geklärt —
die Knöpfe sind da:**

| Beleg | Fundstelle |
|---|---|
| Markup existiert | `app.html:484-485`, beide `<button class="account-nav">` |
| Sie **rendern** sichtbar | `docs/screenshots/p86_block_b_04_account_dialog.png`, „Update-Log ansehen" bei y≈306, „Spaces verwalten" bei y≈358 |
| Warum sie „zu fehlen scheinen" | `app.css:619-633`: `background: none; border: none;` — **keinerlei Bedienelement-Anmutung**. Sie lesen sich als Fließtext zwischen Erklärabsatz und Formular. |

**`[VERIFY] V133` ist damit vorab beantwortet** und bleibt nur als Gegenprobe im Smoke-Skript
(`reachable === true` für beide IDs).

**Bau:** `.account-nav` bekommt eine ruhige, dauerhafte Anmutung nach Konvention v3, Kategorie
*Navigation* — **kein** Knopfrelief (sie sind keine Aktionen), aber sichtbar bedienbar:
linke Akzentkante `2px solid var(--line-strong)`, `padding-left` entsprechend, Chevron-Icon
`#i-chevron-right` rechts über `margin-left: auto`. Der Hover aus B1 (`app.css:634`) bleibt
unverändert.

> **Warum nicht einfach `.btn`:** B3 hat sie bewusst **nicht** zu Knöpfen gemacht („Beides sind
> KEINE Aktionen (öffnen etwas, ändern nichts)", `app.css:613-618`). Diese Begründung trägt —
> der Fehler war nicht die Kategorie, sondern dass *Navigation* im Ruhezustand gar keine
> Anmutung bekam. Der Chevron ist die kleinstmögliche Reparatur, die die Kategorie erhält.

### §5.3 Abschluss Block H

Ein Commit. `pytest` unverändert in der Zahl (ein Test umbenannt, keiner neu).
**Screenshot-Pflicht:** Rail (Voll- und 1200-px-Breite) + geöffneter Konto-Dialog →
`docs/screenshots/p86_block_h_{01..03}_*.png`. `screenshots_latest/` mitziehen.

---

## §6 Block J — Der `pytest`-Flake, beide Hälften (P8.6-AJ)

> **Block „I" wird übersprungen** — `P8.6-I` ist ein bestehender Lock aus Plan 1. Ein Block
> gleichen Buchstabens daneben wäre dieselbe Verwechslungsfalle wie `P8.6-V`.

### §6.1 J1 — Der Produktionsfehler (Tabu-Ausnahme, eng)

**`phase4_auth/authserver/crypto.py`** — neue Funktion, direkt unter `new_secret()` (Z. 14-15):

```python
def new_public_id(nbytes: int = 16) -> str:
    """Wie `new_secret`, aber nie mit `-` beginnend.

    IDs, die ein Mensch auf einer Kommandozeile weiterreicht (`authctl revoke --family-id
    <ID>`), duerfen nicht wie eine Option aussehen -- `argparse` bricht sonst mit
    "expected one argument" ab. Gemessen 2026-09-13: `secrets.token_urlsafe` liefert in
    1,569 % der Faelle ein fuehrendes `-`. Rejection-Sampling statt Umkodierung, damit
    Alphabet und Laenge identisch zu `new_secret` bleiben; der Entropieverlust ist der
    eines verworfenen 64stel.
    """
    while True:
        value = secrets.token_urlsafe(nbytes)
        if not value.startswith("-"):
            return value
```

**`phase4_auth/authserver/store.py`** — genau **zwei** Zeilen:

| Anker | Ist | Soll |
|---|---|---|
| `store.py:294` | `client_id = crypto.new_secret(16)` | `crypto.new_public_id(16)` |
| `store.py:393` | `family_id = crypto.new_secret(16)` | `crypto.new_public_id(16)` |

**Die zehn anderen `new_secret`-Aufrufstellen bleiben unverändert** (`store.py:339, 465, 516,
517, 578, 579, 905, 1019, 1020`). Sie erzeugen opake Geheimnisse, die nie auf einer
Kommandozeile stehen — ihr Alphabet zu verengen wäre eine Entropieänderung ohne Anlass.

### §6.2 J2 — Der Altbestand

Bereits vergebene IDs können mit `-` beginnen. Der Generator-Fix erreicht sie nicht.

**`phase4_auth/scripts/authctl.py`** — `p_revoke` (Z. 199) bekommt einen `help`-Text:

```python
p_revoke.add_argument(
    "--family-id", metavar="ID", required=True,
    help="Familien-ID. Beginnt sie mit '-', die Gleichheitsform verwenden: --family-id=-abc",
)
```

**Das ist die ganze Maßnahme für den Altbestand.** Eine automatische Umschreibung von
`sys.argv` wäre ein Sonderweg an `argparse` vorbei, den niemand mehr erwartet.

### §6.3 J3 — Die Tests

| Test | Datei | Zweck |
|---|---|---|
| `test_revoke_kills_the_family` | `phase4_auth/tests/test_authctl.py:102` | auf `"--family-id=" + family_id` umstellen — **Verteidigung in der Tiefe**: der Test ist danach unabhängig vom Generator grün |
| `test_new_public_id_never_starts_with_a_dash` | `phase4_auth/tests/test_crypto.py` | 5.000 Ziehungen, keine beginnt mit `-`; zusätzlich Länge und Alphabet identisch zu `new_secret` |
| `test_revoke_accepts_a_family_id_starting_with_a_dash` | `phase4_auth/tests/test_authctl.py` | Altbestands-Pfad: `authctl.main(["revoke", "--family-id=-abc"])` gibt rc 0 |

### §6.4 J4 — Die enge Tabu-Probe

Vor dem Commit:

```
git diff --stat -- phase4_auth/authserver
```

Erwartete Ausgabe: **genau zwei Dateien** (`crypto.py`, `store.py`), in `store.py` **genau
2 geänderte Zeilen**. Jede Abweichung ist ein Abbruchgrund.

### §6.5 Abschluss Block J

Ein eigener Commit, **getrennt von jedem UI-Commit** — ein Auth-Touch gehört nicht in einen
CSS-Diff. Erwartung: `pytest` **+3, 0 failed**. Danach ist die Baseline **≥ 972 passed**.

---

## §7 Gate — Wegwerf-Ritt, Sichtprüfung, Deploy

### §7.1 GA1 — Wegwerf-Instanz

Muster aus Phase 8.5 (`phase8_5_picker_release/scripts/`): **Port 18773**, eigener
tmp-`DATA_ROOT`, eigene `auth.sqlite3`, **PID-Datei**.

**Hard Rule 9, ohne Ausnahme:** Stoppen **ausschließlich** über PID-Datei oder den eindeutigen
Port. **Kein `pkill -f`.** `sharefyx-mcp.service` wird nicht angefasst — nicht gestartet, nicht
gestoppt, nicht neu geladen. Am 2026-09-01 hat ein einziges
`pkill -f "phase2_mcp.scripts.serve"` die Produktion mitgenommen.

**Bekannte Stolperstelle aus Block C:** drei fehlgeschlagene Logins lösen das
`login_attempts`-Rate-Limit aus. Zurücksetzen über `cleanup` + `setup` + `seed-items` +
`start`, nicht durch Warten.

### §7.2 GA2 — Smoke-Skript `p86_polish_smoke.py`

**Plan 1 §7.2 hatte 12 Stationen und wurde nie geschrieben. Die Stationsliste dort ist
teilweise überholt** — sie prüft ein Layout, das Block G gerade löscht. **Maßgeblich ist die
Liste hier.**

`phase8_6_ui_polish/scripts/p86_polish_smoke.py` (Playwright, venv
`~/.claude-code-tools/e2e-venv`), je ein Screenshot nach `docs/screenshots/p86_smoke_*.png`:

| # | Station | Prüft | Befund/Lock |
|---|---|---|---|
| 1 | Login → Übersicht, 1440 px | Übersicht steht im **Listen-Slot**; `#detail-graph` füllt den Detail-Slot | 5 / P8.6-Y |
| 2 | Rail-Reihenfolge | `#home-button`, `#rail-tree`, dann `.rail__account` mit `#account-button` **vor** `#logout-button` | 7b / P8.6-AE |
| 3 | Space-Zeile hovern | Fill deckt **die ganze Zeile** inkl. Chip-Leiste | 6 / P8.6-AF |
| 4 | Space-Zeile klicken | Listen-Slot wechselt auf Items; Karte bleibt stehen | 5 |
| 5 | **Item anklicken → ESC** | Editor ersetzt die Karte, **ESC bringt die Karte zurück** | **N.8**, Abnahme P8.6-36 |
| 6 | **Karten-Knoten anklicken → ESC** | derselbe Weg über `graph.js:647` | **N.8** |
| 7 | „Alle Items" klicken | **keine** Spaces-Übersicht, **kein** Space-Name, **kein** „Zuletzt benutzt" | 7a / P8.6-AG |
| 8 | Editor öffnen, Kopfdaten aufklappen | YAML-Panel **kühl**, kein warmer Stich; Append-Zeile abgesetzt | 1+8 / P8.6-AB |
| 9 | Konto-Dialog öffnen | beide `.account-nav` sichtbar **und** `elementFromPoint`-erreichbar | 2 |
| 10 | 1200 px | **alle** Knöpfe erreichbar; `#list-overview` scrollbar, nicht geklippt | **9b** |
| 11 | 1024 px | `data-view`-Umschaltung, `.detail__back` erreichbar | **V126** |
| 12 | Übersicht zweimal öffnen | identisches Kartenbild (Pixelvergleich) | §2.4 / P8.6-M |
| 13 | Zwillingskanten-Item | **eine** Linie statt zwei | V102 / P8.6-N |
| 14 | Link-Picker öffnen, Modus wechseln, neu öffnen | `<select>`, Chevron sichtbar, Wahl aus `localStorage` wiederhergestellt | P8.6-H |

**Beide Browser** (Chromium + Firefox) für Stationen **3, 5, 8, 10** — das sind die mit
CSS-/Fokus-Verhalten, das auseinanderlaufen kann.

**CSRF-Grenze beachten:** die Wegwerf läuft auf `http://127.0.0.1:18773`, die `Origin` passt
nicht zu `SPACE_PUBLIC_BASE_URL` ⇒ **jeder POST/PATCH aus dem Browser-Kontext wird
abgewiesen**. Alle 14 Stationen oben sind bewusst Lese-/Render-Stationen; schreibende
Vorbereitung läuft über `storage.Store`, nicht über UI-Klicks.

### §7.3 GA3 — Nikinger-Sichtprüfung

Nach `sichtpruefung_automation_conventions.md`: **§2** Visuelles ist Nikinger-Sache, der Agent
zertifiziert nicht selbst, dass etwas „schöner" aussieht · **§1** wo etwas klickbar wird, den
**gerenderten** Zustand zeigen · **§3** Deploy erst nach Testauswertung · **§5** zu jedem Bild
**Dateiname** (aus `screenshots_latest/`) **und** ein ein- bis zweisätziges **Checkkriterium**.

**§4 („Screenshots im Chat") ist in OpenCode dauerhaft unerfüllbar** — gemessen, Handover §8.
Der Workflow ist: Playwright schreibt auf Platte → M3 liest mit dem eingebauten `read`-Tool →
M3 nennt **Pfad und eigene Bewertung**.

**Die fünf Punkte, die der Nikinger entscheidet** (nicht der Agent):

1. **Befund 4 neu bewertet:** sind 720 px (50 % der Seite) die richtige Kartengröße? (**V132**)
2. **§10.1 — welche Trägerflächen?** (**V114**, aus Plan 1 unbeantwortet)
3. **§6.4 — bleibt der `cancelAnimationFrame`-Fix drin?** (benannte Scope-Erweiterung, streichbar)
4. **V118 — Tag-Kante + explizite Kante: zwei Linien gewollt?** (`dedupeEdges()` fasst
   `implicitEdges` bewusst nicht an)
5. **Der 1024-px-Zustand** (**V126**) — nie gesichtet, jetzt erstmals im Bild

**V110 wird nicht mehr gestellt** — §4.3 beantwortet sie als negativen Befund.

**Statusregel** (seit 2026-09-08): eine vom Nikinger geprüfte Wegwerf-Automatisierung zählt
als **live-verifiziert (✅)**, nicht als 🟡. Das gilt **nicht** für identitätsförmige Kriterien.

### §7.4 GA4 — Deploy `v3.0.2`

**Es gibt keinen Deploy „nur Plan 2".** `deploy.sh` baut ein Release aus `main` — der nächste
Lauf liefert **Block A + B + C + D + Plan 2 zusammen** aus (Handover §4.6). Das ist kein
Nebeneffekt, das ist die Lieferung der ganzen Phase.

| Schritt | Wer | Was |
|---|---|---|
| **D-a** | Agent | Badge `app.html:20` `v3.0.1` → **`v3.0.2`**; **obersten Block in `docs/UPDATE_LOG.md` mit dem heutigen Datum** — `deploy.sh` bricht sonst ab (P6-X); Commit |
| **D-b** | **Nikinger** | `deploy.sh` ausführen. **Kein Agent fasst `systemctl` an** (Hard Rule 9). |
| **D-c** | Agent | `health_gate.sh --expected-sha=<neuer SHA>` gegen die Produktion — reine `curl`-GETs, **8/8 erwartet**. **Das Ergebnis wird übernommen, nicht notiert.** |

> **D-c ist die Stelle, an der Plan 1 gescheitert ist.** Der Phase-Head behauptete
> „8/8 grün gegen `--expected-sha=04dee6a`"; die Gegenprobe am 2026-09-13 lieferte **7 OK +
> 1 FEHLER**, weil `/opt/sharefyx/current` nie auf einen P8.6-Release zeigte. Das Werkzeug war
> in Ordnung — es liest den Release-SHA aus `git -C /opt/sharefyx/current rev-parse HEAD`
> (`health_gate.sh:134,160`) und kann gar nicht gegen den Arbeitsbaum durchrutschen. **Die
> Behauptung war das Problem.** D-c ist deshalb kein Häkchen, sondern ein Lauf mit
> Ausgabe im Commit.

**`[VERIFY] V134` (geerbt als V103, zweite Phase in Folge offen):** ist der `sudo`-Prompt von
`deploy.sh` im Vordergrund sichtbar? Der Nikinger notiert einen Satz, dann ist sie zu.

### §7.5 Step Z — Closeout

1. Abnahmematrix §8.1 **vollständig** auswerten — jede Zeile mit Beleg, nicht mit Zuversicht.
2. `[VERIFY]`-Register §8.3 bilanzieren.
3. **§9 dieses Dokuments füllen** — das ist nach **P8.6-W** der kanonische Abschluss.
4. **Eine Zeiger-Zeile** in Plan 1 §9 (die einzige erlaubte Änderung an dem 📕-Snapshot).
5. Phase-Head, `ROADMAP.md`, `docs/INDEX.md`, Wurzel-`CLAUDE.md` auf ✅.
6. Übersichtsgrafik `phase8_6_ui_polish_uebersicht.svg` auf den Endstand — Badge von
   **PARTIAL CLOSEOUT** auf die Abnahmezahl.
7. `rotate_session_block.sh phase8_6_ui_polish`.

---

## §8 Abnahme, Tests, `[VERIFY]`-Register

### §8.1 Abnahmematrix

Art: **(C)** Code/Test, vom Agenten belegbar · **(W)** Wegwerf-Instanz + Nikinger-Sichtung ·
**(L)** nur live entscheidbar. Fortsetzung der Nummerierung aus Plan 1 (dort 1–32).

| # | Kriterium | Art | Befund/Lock |
|---|---|---|---|
| P8.6-33 | `docs/INDEX.md` **≤ 38.912 B** *nach* allen Plan-2-Zeilen | (C) | §1.2 |
| P8.6-34 | `p86_viewport_probe.py` existiert; Protokoll für 1024/1200/1440 px liegt im Phase-Head, für **beide** Ziele (`main` + Produktion) oder mit begründetem Abbruch für die Produktion | (C) | §2 |
| P8.6-35 | `.shell` ist `240px 480px 1fr`; beide Media-Queries mitgezogen | (C) | P8.6-X |
| P8.6-36 | **Item anklicken → Editor · ESC → Karte wieder da.** Gilt für Klick in der Liste **und** für Klick auf einen Karten-Knoten | (C+W) | **N.8** |
| P8.6-37 | Übersicht (Spaces + Zuletzt benutzt + Refresh) steht im `.list`-Slot; die Karte hat den `.detail`-Slot allein | (W) | Befund 5 |
| P8.6-38 | Im Modus „Alle Items" wird `renderOverview()` **nicht aufgerufen** — maschinell geprüft, nicht nur gesichtet | (C+W) | Befund 7a / P8.6-AG |
| P8.6-39 | Hover auf einer Space-Zeile deckt die **ganze** Zeile inkl. Chip-Leiste; Space mit lauter Null-Zählern ist klickbar **und** per Tastatur erreichbar | (W) | Befund 6 / P8.6-AF |
| P8.6-40 | `#overview-refresh` und `#overview-graph` überlappen sich bei keiner der drei Breiten (`p86_viewport_probe.py`) | (C) | Befund 3 / V131 |
| P8.6-41 | Karte ist bei 1440 px **≥ 700 px** breit | (C) | Befund 4 / V132 |
| P8.6-42 | Rail: `#account-button` steht **in** `.rail__account`, **vor** `#logout-button`; `#logout-button` ist das letzte Element des Rails | (C) | N.9 / P8.6-AE |
| P8.6-43 | Beide `.account-nav`-Knöpfe sind sichtbar, per `elementFromPoint` erreichbar und als bedienbar erkennbar | (C+W) | Befund 2 |
| P8.6-44 | `--panel-meta*` tragen keinen `--warn`-Bezug mehr; `grep -c "229,169,60" app.css` = **0** außerhalb `--warn` selbst | (C) | Befund 8 / P8.6-AB |
| P8.6-45 | Kein roher Flächen-Hex mehr außerhalb `:root` außer `#fff` in `.qr-frame`; maschinell gehalten | (C) | Befund 1 / P8.6-AD |
| P8.6-46 | `pytest` **≥ 972 passed, 0 failed** — inklusive der drei neuen Auth-Tests | (C) | §6 |
| P8.6-47 | `git diff --stat -- phase4_auth/authserver` zeigt **genau zwei Dateien**, in `store.py` genau 2 Zeilen | (C) | P8.6-AJ / §6.4 |
| P8.6-48 | Tabu-Diff §0.3 über **ganz Plan 2** leer — **keine neunte P1-Contract-Öffnung** | (C) | P8.6-S |
| P8.6-49 | `ui_budget.py` 5/5 im Korridor | (C) | §1.4 |
| P8.6-50 | Bei 1200 px und 1024 px ist **kein** Knopf unerreichbar (`reachable === false` = 0) | (C+W) | Befund 9 |
| P8.6-51 | `v3.0.2` live, Badge sichtbar, `health_gate.sh --expected-sha=<SHA>` **8/8**, Ausgabe im Commit | (L) | §7.4 |
| P8.6-52 | Service-Touch durch einen Agenten: **0**. Wegwerf nur per PID-Datei/Port gestoppt | (C) | Hard Rule 9 |
| P8.6-53 | Die Karte hat nach dem Umzug eine **definite Hoehe**: `#overview-graph` `getBoundingClientRect().height` > 0 und unterer Rand im Viewport, bei 1024/1200/1440 px. **Der V112-Bug ist nicht wieder da** | (C) | §4.2.1 / V138 |
| P8.6-54 | `#list-empty` ist im Übersichts-Zustand unsichtbar, auch nach einem Wechsel aus einem leeren Space | (C+W) | §4.4 / V139 |

**Aus Plan 1 offen und hier mitgeführt:** P8.6-8, -10, -12, -13, -18, -19, -23, -24, -25, -26,
-27 (die (W)-Zeilen, deren Sichtprüfung in Befunde umgeschlagen ist). **P8.6-21 und P8.6-22
werden ersetzt** — sie sind durch die Befunde 4 und 9 aktiv widerlegt; ihre Nachfolger sind
**P8.6-41** und **P8.6-50**. **P8.6-20** wird auf „kein sichtbares Label ‚Konto' in
`webui/static/`" geschärft (Handover §3: das alte Kriterium war zu breit formuliert und traf
das deutsche Wort in Sperrmeldungen).

### §8.2 Testliste (neu zu schreiben)

UI-Tests in `phase5_ui/tests/test_static_routes.py` (610 Zeilen, etablierter Ort);
Auth-Tests in `phase4_auth/tests/`.

| Testname | Datei | Prüft | Block |
|---|---|---|---|
| `test_no_raw_surface_hex_outside_root` | `test_static_routes.py` | jede `background`-Deklaration in `app.css` außerhalb `:root` nutzt `var(--…)` oder eine Kategoriefarbe; **Ausnahmeliste: genau `#fff` in `.qr-frame`**. Der Wächter über P8.6-AD | F |
| `test_meta_panel_is_not_tinted_with_the_warning_colour` | `test_static_routes.py` | `229,169,60` kommt in `app.css` nur in der `--warn`-Definition vor | F |
| `test_shell_grid_is_240_480_1fr` | `test_static_routes.py` | `.shell` und die 1280-px-Query tragen `480px` | G |
| `test_overview_lives_in_the_list_slot` | `test_static_routes.py` | `#list-overview` steht in `app.html` **innerhalb** `section.list`, `#overview-graph` **innerhalb** `section.detail` | G |
| `test_detail_graph_has_a_definite_height_chain` | `test_static_routes.py` | `.detail__graph` traegt `flex: 1` **und** `min-height: 0`, und `.detail__graph .overview__graph` traegt `flex: 1` — der **V112-Waechter nach dem Umzug** (§4.2.1). Prueft die *Anwesenheit* einer Hoehenquelle, waehrend `test_overview_graph_has_no_max_width_or_min_height` die *Abwesenheit* eines Caps prueft; beide werden gebraucht | G |
| `test_overview_grid_and_its_media_query_are_gone` | `test_static_routes.py` | weder `overview__col-left` noch `overview__col-right` noch `grid-template-columns: 1fr 40%` kommen vor — **der 9b-Regressionswächter** | G |
| `test_rail_order_settings_and_logout_at_the_end` | `test_static_routes.py:505` | **Umkehrung**, Docstring trägt beide Richtungen (P8.6-AE) | H |
| `test_new_public_id_never_starts_with_a_dash` | `phase4_auth/tests/test_crypto.py` | 5.000 Ziehungen, Länge + Alphabet wie `new_secret` | J |
| `test_revoke_accepts_a_family_id_starting_with_a_dash` | `phase4_auth/tests/test_authctl.py` | Altbestands-Pfad über die `=`-Form | J |

**Zwei bestehende Tests werden angepasst, nicht gelöscht:**
`test_overview_graph_has_no_max_width_or_min_height` (`:578`) — der Selektor wandert mit dem
Element. `test_revoke_kills_the_family` (`test_authctl.py:102`) — auf die `=`-Form.

> **`test_overview_grid_and_its_media_query_are_gone` ist der wichtigste der acht.** Er ist
> der einzige, der eine *gelöschte* Ursache festhält. Block G räumt Befund 9b weg, indem er
> das Grid entfernt — ohne diesen Test kann eine spätere Phase das Grid arglos
> wieder einführen und den Befund mit ihm.

### §8.3 `[VERIFY]`-Register

Fortsetzung aus Plan 1 (dort V95–V122).

| # | Frage | Wann |
|---|---|---|
| **V123** | **Sammelmarker:** alle `Datei:Zeile`-Anker dieses Plans gegen `main`@`26a7cc9`. **Bei Drift melden, nicht raten.** | vor jedem Block |
| **V124** | `docs/INDEX.md` ≤ 38.912 B nach allen Plan-2-Zeilen? | Step 0' |
| **V125** | Trägt Befund **9a** (Produktion) dieselbe Ursache wie 9b, eine andere, oder ist er dort nicht reproduzierbar? | Block E |
| **V126** | Wie viele Knöpfe sind bei **1024 px** unerreichbar? Das dritte Layout ist nie gesichtet worden | Block E + Gate |
| **V127** | Setzt `.editor__textarea` (`app.css:1584`) einen eigenen Hintergrund, oder erbt sie von `.panel--body`? | Block F |
| **V128** | Vollständige Liste der Aufrufstellen von `renderList()`/`renderOverview()` gegen `26a7cc9` | Block G |
| **V129** | Überlebt `graph.js :: resize()` den Elternteil-Wechsel von `.overview__col-right` nach `.detail__graph`? | Block G |
| **V130** | **Gegenprobe:** dieselbe `p86_viewport_probe.py` nach Block G — ist 9b weg, und *warum* | nach Block G |
| **V131** | Überlappen `#overview-refresh` und `#overview-graph` nach G2 noch? | Block G |
| **V138** | Hat `#overview-graph` nach dem Umzug eine Hoehe > 0 und einen sichtbaren unteren Rand — bei allen drei Breiten? **Der V112-Bug, wiedereingebaut, waere die teuerste Regression der Phase** | Block G, vor dem Commit |
| **V139** | Aus einem **leeren** Space auf „Übersicht“ klicken — steht „Erste Notiz anlegen“ (`#list-empty`) noch unter den Spaces? | Block G |
| **V132** | Sind 720 px (50 % der Seite) die richtige Kartengröße? **Nikinger-Entscheidung** | Sichtprüfung |
| **V133** | Sind beide `.account-nav` per `elementFromPoint` erreichbar? *(vorab beantwortet, §5.2 — bleibt als Gegenprobe)* | Gate |
| **V134** *(geerbt V103)* | `deploy.sh`: `sudo`-Prompt im Vordergrund sichtbar? | Deploy |
| **V135** | Bricht das Rate-Limit `login_attempts` den Smoke-Lauf bei 14 Stationen × 2 Browser? | Gate |
| **V136** | Kollidiert die `<span role="button">`-Umstellung der Chips (G7) mit dem Drag-and-Drop-Ziel `bindFolderDropTarget()` (`tree.js:108`)? | Block G |
| **V137** | `.rail__action--account` (`app.css:418`) — nach der Rail-Umkehr noch nötig, oder Rest der Oben-Platzierung? | Block H |

**Aus Plan 1 weiter offen und hier mitgeführt:** **V114** (welche Trägerflächen meinte der
Nikinger in §10.1) und **V118** (zwei Linien bei Tag-Kante + expliziter Kante) — beide gehen
in die Sichtprüfung §7.3.
**V110 ist geschlossen**, als negativer Befund: §4.3.
**V106 ist verbraucht** und durch **V123** ersetzt.

---

## §9 Closeout

*Leer bis Step Z. Dieser Abschnitt ist nach **P8.6-W** der **kanonische** Abschluss der Phase
8.6 — Status in fünf Sätzen, Delta über **beide** Pläne, Abnahmestand 1–52, Restdefekte,
`[VERIFY]`-Bilanz V95–V139, P1-Contract-Aussage, und was nicht enthalten ist. Plan 1 §9 bleibt
leer und trägt nur eine Zeiger-Zeile hierher.*
