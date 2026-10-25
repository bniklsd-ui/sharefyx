---
status: live
purpose: Phase-Head UI-Politur (Selektion + Layout, drei Graph-Fixes, Radiogruppe-Rückbau) → Deploy `v3.0.2` — Scope, harte Regeln, Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase8_6_ui_polish/ oder an den in §0.3/§3/§4/§5/§6/§7 des Plans genannten Dateien in `phase5_ui/webui/static/` + `phase5_ui/tests/` + `scripts/` — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase8_6_ui_polish_plan.md   # voller Plan, Entscheidungen P8.6-A–P8.6-U, §0.1 gelockte N1–N4, Steps 0/V/A/B/C/D/Gate/Z
  - ../docs/concepts/p8x_ui_polish_notes.md       # Inhaltsquelle §1–§10 (P8.6-A benennt das Verzeichnis)
  - ../docs/concepts/PHASE8_5_CLOSEOUT_HANDOVER.md   # Einstieg für die P8.6-Planung; §4 = die offenen Entscheidungen
  - SESSIONS_ARCHIVE.md                            # ältere Session-Blöcke, newest-first
  - MODULE_STATUS_ARCHIVE.md                       # 📦 Modul-Status + Vormerkungen, verbatim (DO-1, 2026-10-25)
  - UPDATES_ARCHIVE.md                             # 📦 die älteren `updated:`-Fäden, verbatim
updated: 2026-10-25 (P10.5 Block 12: Modul-Status und Vormerkungen nach MODULE_STATUS_ARCHIVE.md, ältere Fäden nach UPDATES_ARCHIVE.md — 109.230 → 23.6 KB) | 2026-09-19 (**Step Z — Closeout, Phase 8.6 formal abgeschlossen ✅.** Reine Doku-Session, kein Produktcode-Touch. Abnahmematrix beider Plaene vollstaendig ausgewertet (**45 ✅ · 5 ⚠️ · 0 ⬜ · 4 ersetzt** von 54 Zeilen), `[VERIFY]`-Bilanz V97/V103–V144 (**37 zu · 2 offen: V118, V136 · 2 nachtraeglich bilanziert: V140/V141**), **Plan 2 §9 als kanonischer Closeout gefuellt** (P8.6-W) + Zeiger-Zeile in Plan 1 §9, `PHASE8_6_CLOSEOUT_HANDOVER.md` von Partial- auf **Abschluss**-Handover P8.6 → P9 umgeschrieben, Uebersichtsgrafik von PARTIAL CLOSEOUT auf die Abnahmezahl, ROADMAP + Wurzel-`CLAUDE.md` auf ✅. Gemessen: `pytest` **995**, `ui_budget` 5/5 (144,7 KB), Bereichs-Tabu-Diff `440e462^..HEAD` leer bis auf P8.6-AJ. Vier Step-Z-Funde: `docs/INDEX.md` auf **45.870 B** gewachsen (dritter Verstoss, gestrafft); P8.6-18/-19 zusaetzlich ersetzt; V136 nie beantwortet; V140/V141 nie bilanziert. Nikinger-Feedback vom 2026-09-19 im Handover §4.1 abgelegt — zwei Bugs mit erstem Messbefund, ein Rechte-Thema, fuenf Feature-Wuensche) | ältere Einträge: phase8_6_ui_polish/UPDATES_ARCHIVE.md
---
# CLAUDE.md — Phase 8.6: UI-Politur, Selektion + Layout, drei Graph-Fixes (`phase8_6_ui_polish/`)

> Kein eigenes Python-Paket (wie `phase6_shares/`, `phase6_5_tools_images/`,
> `phase7_spaces_admin/`, `phase8_5_picker_release/`) — Servercode bleibt in `storage`/
> `mcpserver`/`webui/static`, dieses Verzeichnis trägt nur Kopf, Archiv und Skripte.
> **Quelle der Wahrheit ist der Code, nicht dieses Dokument.**

---

## Mission (zuerst lesen)

**Reihenfolge 0 → V → A → B → C/D → Gate → Z:** Step 0 Fundament, Step V OpenCode-Vision-Plugin
(`DavidEasden/opencode-vision`, Plan §2 — Nikinger-Vorgabe 2026-09-08, **erster** Schritt vor
jedem Code-Touch; bei Scheitern aller drei Kandidaten: Befund protokollieren, mit dem alten
Verfahren weitermachen, Phase wartet nicht), Block A Fundament (A1 Radiogruppe zurück auf
`<select>`, A2 Layer-/Selektions-Tokens, A3 `--border-soft`-Renderfehler-Fix, A4 Konvention v3
um Kategorie „Vorsicht"), Block B Selektion vereinheitlichen (B1 leise Standardauswahl + Hover,
B2 Ordner/Tags/Buckets, B3 Einstellungsmenü, B4 Sweep „alles Klickbare" mit Vorsicht-Kennzeichnung,
B5 Radien), Block C Struktur (`§6` „Konto"→„Einstellungen" + `§1` „Alle Items" unter die Spaces +
`§1` Map als rechte Spalte/volle Höhe + `§10.4` klickbare Spaces + `§3` Ordner-Zähler) bzw. Block D
Graph-Fixes (V102-Dedup, deterministischer Layout-Seed, `cancelAnimationFrame`-Lauf-Abbruch),
dann Gate (Wegwerf + Smoke + Nikinger-Sichtprüfung), dann Deploy `v3.0.2` als Nikinger-Aktion,
dann Step Z Closeout im Plan §9. **C und D sind unabhängig voneinander und dürfen getauscht
werden; A vor B ist zwingend** (P8.6-U). Details, alle vier Nikinger-Fragen N1–N4, gelockte
Entscheidungen P8.6-A–P8.6-U, Tabu-Liste, Schritt-Sequenz, Testliste, Abnahmezeilen,
`[VERIFY]`-Register: `docs/concepts/phase8_6_ui_polish_plan.md`.

## Scope (Kurzform, Details: Plan §0.4 P8.6-A–P8.6-U)

- **DRIN:** Selektions-Welle + Layout (Reichweite N1) — §5 Layering-Tokens + §10.1–§10.7
  Selektions-Vereinheitlichung + §6 „Konto"→„Einstellungen" (Lesart b) + §3 Ordner-Zähler +
  §1 Rail-/Übersichts-Reorg + §10.4 klickbare Spaces + §2.3/§2.4 Map-Fixes + Radiogruppe-
  Rückbau auf `<select>`; **V102 frontend-dedupliziert** (`graph.js:156`, N2 — bewusst
  **keine neunte P1-Contract-Öffnung**, P8.6-S); §10.7 als **fünfte Konventions-Kategorie
  „Vorsicht"** (`--caution = --danger` unter neuem Namen, N4, P8.6-F/G); Deploy `v3.0.2`
  (P8.6-R — Patch-Bump, weil §1 Flächen verschiebt aber keine Informationsarchitektur ändert;
  wenn der Nikinger in der Sichtprüfung anders entscheidet, ist `v3.1.0` seine Entscheidung
  **nach** Step Z, nicht die des Ausführenden); OpenCode-Vision-Plugin-Installation (P8.6 first
  step, Nikinger-Vorgabe 2026-09-08 — nicht Teil der UI-Politur selbst, aber bewusst früh in
  derselben Phase, damit die nächste Sichtprüfungsrunde davon profitiert).
- **DRAUSSEN:** §2.1 Map-Performance / §2.2 Landkarten-Stil / §2.5 Karte einklappen →
  **P9** (Graph-Umbau, die Ausnahme für den `cancelAnimationFrame`-Lauf ist §6.4 unten
  begründet und streichbar); §4 Edit-in-Place → eigene Phase (berührt Hard Rule 3 + P7-24);
  §7 De-AI-ierung Lauf 2 → eigene Claude-Code-Recherche-Session; §8 Tags + §9 Feedback-Button →
  nach P8.6 (beide brauchen eine neue Tabu-Bewertung); §10.8 verbundene AI-Sessions → **P9**
  (N1-Randnotiz: „eher v3.1 also p8.7" meint P9); §10.9 Hochkant-/Handy-UI → benanntes
  Zukunfts-Item, kein P8.6-Auftrag; „Ordner umbenennen" → bewusst draußen mit Analyse
  (Plan §0.4.1 — die billige Fassung verliert eine `.share.yml`-Freigabe still als
  Nebenwirkung, das wäre eine Rechteänderung, gegen die Hard Rule 4 schreibt); CSRF-Origin-
  Mismatch bei Wegwerf-Instanzen (Handover §4.3) → P8.6 braucht keinen Reverse-Proxy;
  Body-Volltextsuche (Q1), Rechteverwaltung über MCP-Tools (P6-M), Löschen von Items (F2),
  FastMCP-4 (V79), Funnel-Watchdog, Realtime, Light-Mode (P5-X), Glyph-Entscheidungen P6/P6.5,
  Bulk-Append-MCP-Tool.

## Harte Regeln dieser Phase (nicht verhandelbar)

- Alle Hard Rules aus Wurzel-`CLAUDE.md` gelten unverändert — insbesondere Hard Rule 9
  (kein `pkill -f` mit Regex, niemals den systemd-Dienst anfassen), Hard Rule 1 (keine Secrets
  in Dateien), Hard Rule 8 (Commit ⇒ Doku-Update im selben Commit).
- **§0.3 Tabu-Liste** (P8.6 verbatim, Plan §0.3) — `git diff` muss über die gesamte Phase
  leer bleiben, bis auf die erlaubten Ausnahmen:
  - `phase1_storage/storage/**` — **Tabu, keine Ausnahme** (P8.6-S).
  - `phase4_auth/authserver/**` — **Tabu, keine Ausnahme**.
  - `phase2_mcp/mcpserver/**` — **Tabu, keine Ausnahme**, auch nicht der Hint-Text (das war
    eine P8.5-Ausnahme mit eigener Begründung, in P8.6 aberkannt).
  - `phase5_ui/webui/{security,api,serializers,permissions}.py` — **Tabu**. §3 kommt
    clientseitig aus (P8.6-O), keine `_overview`-Erweiterung.
  - `phase5_ui/webui/static/**` — **Erlaubt**, das ist die Arbeitsfläche der Phase.
  - `phase5_ui/webui/pages.py` — **Erlaubt, aber nur für Template-/Routing-Trivialitäten**.
    Wenn ein Schritt hier mehr als eine Zeile braucht: an den Nikinger eskalieren.
  - `phase5_ui/tests/**`, `phase8_6_ui_polish/scripts/**` — **Erlaubt**.
  - **Prüfkommando am Step-Ende:**
    ```
    git diff --stat -- phase1_storage/storage phase4_auth/authserver \
        phase2_mcp/mcpserver phase5_ui/webui/security.py phase5_ui/webui/api.py \
        phase5_ui/webui/serializers.py phase5_ui/webui/permissions.py
    ```
    Eine nicht-leere Ausgabe ist ein Abbruchgrund, kein Kommentar-Anlass.
- **§0.5 Selbstprüf-Checkliste am Ende jedes Steps** (Advisor-Ersatz, P8.5-O-Eskalationsregel
  + P8.6-O2-Architekturregel `.shell`-Grid):
  `pytest -q` grün, Tabu-Diff leer, `node --check` auf jede berührte JS-Datei,
  `python phase5_ui/scripts/ui_budget.py` 5/5 im Korridor, **kein rohes `rgba(62,141,243`
  außerhalb von `:root`** (ab Block A statischer Test §8.2), neue `.md` haben L1-Card +
  INDEX-Zeile, kein Service-Touch.
- **Eskalationsregel opencode/M3 → Claude Code** (P8.5-O wörtlich übernommen): ein Fund,
  dessen Ursache in einer *früheren* CSS-Regel oder in der Kaskade liegt — nicht in der Regel,
  die man gerade ansieht — wird **nicht symptomatisch gepatcht**, sondern an Claude Code
  eskaliert. Erkennungsmerkmal: „der Wert stimmt im Quelltext, sieht im Browser aber anders
  aus".
- **Neue Eskalationsregel P8.6-O2:** wenn ein Schritt aus Block C das `.shell`-Grid
  (`app.css:327-332`) in einer Weise ändern will, die Rail-, Listen- **und** Detail-Breite
  gleichzeitig betrifft, ist das ein Architektur-Schnitt und keine Politur → eskalieren.
- **Rotationsregel ab Tag 1.** Dieser Head trägt **genau einen** Session-Block (P8.6-T).
  Beim Anlegen eines neuen wandert der bisherige **verbatim** nach `SESSIONS_ARCHIVE.md`,
  Durchführung über `scripts/rotate_session_block.sh phase8_6_ui_polish`, nie von Hand.
- **Commit ⇒ Note-Update, im selben Commit** (Hard Rule 8): Modul-Status-Tabelle + Session-
  Block + INDEX-Zeile + ROADMAP-Absatz + Wurzel-CLAUDE.md-Current-state-Absatz.
- **§0.5.7 — Kein Service-Touch.** `systemctl status sharefyx-mcp` nur **lesend**, PID und
  Uptime im Session-Block notieren. Wegwerf-Instanzen nur über PID-Datei / `pgrep -f`
  mit `$`-Anker / eindeutigen Port stoppen — nie über `pkill -f`.

## Modul-Status
> **Verbatim verschoben** nach `MODULE_STATUS_ARCHIVE.md` (`scripts/move_sections.py`) — dort unter derselben Überschrift.

## Geerbte Contracts

P8.6-S: **keine neunte P1-Contract-Öffnung.** Die achte (`storage/linkscan.py` + `Store.links_all()`)
bleibt seit Phase 8 Step B geschlossen, der Index wird in P8.6 nicht angefasst. Damit gilt
die `phase1_storage/CLAUDE.md`-Liste der Contract-Öffnungen ohne Nachtrag. Die Tabu-Liste
`phase5_ui/webui/security.py` (P8-Q) bleibt verbatim; `phase2_mcp/mcpserver/` ist in P8.6
anders als in P8.5 **vollständig tabu** (kein Hint-Text-Edits, die Hint-Arbeit ist in P8.5
geschlossen, V105-Vierte-A3-Probe ✅ 2026-09-08).

## Baselines vor dem ersten Code-Touch (gemessen 2026-09-09, Plan §1.6/§1.7)

| Marker | Wert | Status |
|---|---|---|
| **V107** (`pytest`) | **964 passed in 257 s** (mit ausgehängten `SHAREFYX_*`/`SFX_*`) | ✅ geschlossen (Plan §1.6) |
| **V97** (`ui_budget.py`, aus P8.5-Handover geerbt) | **5/5 im Korridor**, app.js+app.css+Font gzip 130,1 KB von 250 KB | ✅ geschlossen (Plan §1.7) |
| **V108** (`_overview`-Latenz) | **~863 ms** (historisch dokumentiert 438–453 ms) | 🟡 offen — vor Block C drei Läufe mitteln, Rauschen oder Regression; **kein P8.6-Auftrag**, Befund ggf. P9 |
| **V106** (Sammelmarker für alle `Datei:Zeile`-Anker) | gegen `main`@`d1af51b` gemessen | ✅ beim Step-0-Stand, vor jedem Block neu zu prüfen |
| **V103** (`deploy.sh`-`sudo`-Prompt-Sichtbarkeit, geerbt) | unbeantwortet aus P8.5 (D2 lief still) | 🟡 beim Deploy (Plan §7.4) |

**`ui_budget.py` Detailwerte** (`phase5_ui/scripts/ui_budget.py`, Lauf 2026-09-09):

| Messgröße | Ist | Ziel |
|---|---|---|
| `GET /api/v1/items?limit=50` roh | 26,5 KB | < 64 KB |
| `GET /api/v1/items?limit=50` gzip | 1,3 KB | < 12 KB |
| `GET /api/v1/items/{id}` typisch | 0,7 KB | < 8 KB |
| `app.js + app.css + Font` gzip | **130,1 KB** | < 250 KB |
| Erstaufruf `/ui/` bis interaktiv | 138,3 KB | < 400 KB |


**[2026-09-13, Korrektur — von Phase 8.6 ist nichts live.** Am Server gemessen:
`/opt/sharefyx/current` → `releases/20260905T140325.378914Z`, dort `git rev-parse HEAD` =
**`6f19a8f`** (der P8.5-Release vom 2026-09-05); sechs Block-Marker (`bg-void`, `select-fill`,
`dedupeEdges`, `seedJitter`, `account-nav`, `overview__col-right`) haben **0 Treffer live** und
6 im Repo; unter `/opt/sharefyx/releases/` liegt kein Verzeichnis nach dem 2026-09-05, und
`deploy.sh:107` legt pro Lauf ein neues an. **Die `updated:`-Kette und der Step-V-Session-Block
behaupten „Push + Deploy für Block A + D ausgeführt, `health_gate.sh --expected-sha=04dee6a`
8/8 grün" — der Push stimmt, der Deploy nicht.** **Das Werkzeug ist in Ordnung, die Behauptung war es nicht.** `health_gate.sh` liest den Release-SHA in Gate 8 aus `git -C /opt/sharefyx/current rev-parse HEAD` (Z. 134/160) — es kann also gar nicht gegen den Arbeitsbaum durchrutschen. Gegenprobe am 2026-09-13 gefahren: `health_gate.sh --expected-sha=04dee6a` meldet **7 OK und einen FEHLER** („Release-SHA ist 6f19a8f…, erwartet 04dee6a"). Das dokumentierte „8/8 grün gegen `--expected-sha=04dee6a`" ist damit **nie so gelaufen**. Konsequenz für Plan 2: D-c aus Plan §7.4 bleibt ein belastbarer Schritt — man muss ihn nur wirklich ausführen und das Ergebnis übernehmen, statt es zu notieren. Die Stellen bleiben verbatim stehen (sie sind
rotierte Historie), diese Notiz steht datiert daneben. Folge: `deploy.sh` liefert `main` aus,
einen Deploy „nur Block C" gibt es nicht — der nächste Lauf bringt A+B+C+D zusammen. Der Push
ist davon unberührt. Volle Herleitung: `docs/concepts/PHASE8_6_CLOSEOUT_HANDOVER.md` §4.6.**

**[2026-09-13, Nikinger-Entscheidungen]** **(a)** Deploy-Ziel bleibt **`v3.0.2`** — P8.6-R
bestätigt. **(b)** **Block C geht einzeln raus** (Push), nicht in einem Sammel-Push nach
Plan 2 — zur Deploy-Einschränkung siehe die Korrektur darüber. **(c)** Die Ein-Block-Regel für
die Current-state-Sektion der Wurzel-`CLAUDE.md` ist **verworfen**; stattdessen ist dort die
`updated:`-Kette rotiert (47.094 → 23.007 B). **(d)** **Push ja, Deploy nein** (Nikinger, 2026-09-13, nachdem die Tatsachenlage aus §4.6 vorlag): die Commits gehen nach `origin/main`, **ausgeliefert wird nicht**. Live bleibt damit `6f19a8f` (P8.5). Ein Push ändert nichts an der Produktion — die drei von Block C neu eingeführten Befunde 3/4/6 erreichen keinen Nutzer, bis Plan 2 sie abgearbeitet hat. Handover §4.5.

## Vormerkungen (nicht Teil eines aktuellen Steps)
> **Verbatim verschoben** nach `MODULE_STATUS_ARCHIVE.md` (`scripts/move_sections.py`) — dort unter derselben Überschrift.

## Nächste Session

**Phase 8.6 ist abgeschlossen.** `v3.0.2` ist seit dem 2026-09-18 live (SHA `1ad2665`,
`health_gate.sh` 9/9); Step Z ist am 2026-09-19 durchgeführt, ROADMAP und Wurzel-`CLAUDE.md`
stehen auf ✅. **In diesem Verzeichnis ist nichts mehr zu tun** — es ist ab jetzt Archiv.

**Der Einstieg in die nächste Phase ist `docs/concepts/PHASE8_6_CLOSEOUT_HANDOVER.md`**
(Abschluss-Handover P8.6 → P9), nicht dieser Head. Der kanonische Closeout mit Abnahmematrix,
`[VERIFY]`-Bilanz und Restdefekten steht in `docs/concepts/phase8_6_ui_polish_plan2.md` §9
(Lock P8.6-W).

**Drei Dinge, die eine P9-Planungssession aus dieser Phase mitnehmen sollte:**

1. **Zwei offene Marker gehen mit über:** **V118** (Zwillingskanten-Linienzahl — aus dem
   Screenshot nicht beantwortbar, ohne Hover zeigt die Karte keine Knoten-Labels) und **V136**
   (Chip-`<span role="button">` vs. `bindFolderDropTarget()` — nie beantwortet, und seit dem
   Nikinger-Feedback vom 2026-09-19 nicht mehr akademisch).
2. **Das Nikinger-Feedback vom 2026-09-19** liegt vollständig im Handover §4.1, bewusst in drei
   Klassen sortiert: zwei Bugs mit erstem Messbefund, **ein Rechte-Thema** (Verschieben in fremde
   Spaces ist Hard Rule 4 / `.share.yml`, nicht CSS), fünf gewöhnliche Feature-Wünsche.
3. **Die Sichtprüfungs-Frage ist offen** (Handover §4.6). Drei der fünf Revisionsrunden dieser
   Phase gehen darauf zurück, dass opencode/M3 seine eigenen Screenshots geglättet beschreibt.
   Zwei Optionen liegen als Vormerkung bereit, **keine ist entschieden.**

**Sichtprüfungs-Workflow (unverändert, Befund 2c):** Playwright schreibt den Screenshot auf
Platte → M3 liest ihn mit dem eingebauten `read`-Tool → M3 nennt **Dateiname und eigenes
Checkkriterium** (Konvention §5). Ein Rendern im OpenCode-Chat ist technisch nicht möglich.

## Session stopped — 2026-09-19 (Claude Code — Step Z: Closeout, Phase 8.6 formal abgeschlossen)

**Auftrag:** Rückblick auf die beendete Phase, Übersichtsgrafik, Handover für den P9-Chat,
Rotationsprüfung, alles in **einem** Commit (Hard Rule 8). Reine Doku-Session — **kein
Produktcode-Touch**, der Tabu-Diff dieser Session ist trivial leer.

**Vorab gemessen statt übernommen** (Plan 2 §7.5.1: „jede Zeile mit Beleg, nicht mit
Zuversicht"):

| Messung | Ergebnis |
|---|---|
| `pytest -q` | **995 passed in 117,63 s**, exit 0 |
| `ui_budget.py` | **5/5 im Korridor**, Bundle 144,7 KB von 250 KB, `app.css` 25,4 KB gzip, `/api/v1/overview` 395,1 ms |
| Tabu-Diff **über die ganze Phase** (`440e462^..HEAD`, nicht Working Tree) | **leer** für die sechs harten Pfade |
| enge `authserver`-Probe, gleicher Bereich | **2 Dateien** (`crypto.py` +16, `store.py` 2/2 Zeilen) — exakt P8.6-AJ |
| live vs. `main` | live `1ad2665`, HEAD `860ed72`; Differenz = `deploy.sh` + sein Test + Doku, **kein Anwendungscode** |
| Smoke-Report | 18/18 Stationen `ok: true`, 17 PNG unter `docs/screenshots/p86_smoke_*.png` |

**Warum der Bereichs-Diff und nicht `git diff`:** der Arbeitsbaum war zu Sessionbeginn sauber,
ein Working-Tree-Diff hätte also *vakuös* leer gemeldet und über die Phase gar nichts bewiesen.
P8.6-30/-48 fordern „über die **gesamte** Phase" — das ist ein Bereichs-Diff gegen den ersten
Phasen-Commit, sonst ist die Abnahmezeile eine Selbstbestätigung. Dieselbe Falle, in die die
Phase am 2026-09-13 schon einmal getreten ist (Plan 2 §9.5).

**Vier Funde in Step Z selbst — alle im selben Commit behoben oder benannt:**

1. **`docs/INDEX.md` stand auf 45.870 B** gegen das ≤-38-KB-Kriterium (P8.6-4 / P8.6-33).
   **Dritter Verstoß derselben Zeile in dieser Phase** (40.870 → 38.822 → 38.471 → 45.870). In
   diesem Commit wieder von Hand gestrafft: `updated:`-Kette auf einen aktuellen Eintrag plus
   Zeiger, P8.6-Block auf den Umfang einer abgeschlossenen Phase gebracht. **Nicht** gelöst wurde
   die Ursache — `docs/INDEX_UPDATES_ARCHIVE.md` + Rotation ist und bleibt P9-Arbeit, ein
   Doku-Struktur-Umbau ist kein Closeout-Auftrag. Die Empfehlung steht jetzt im Handover §4.4.
2. **P8.6-18 und P8.6-19 sind ebenfalls ersetzt**, nicht nur -21/-22. Plan 2 §8.1 hat zwei
   ersetzte Zeilen benannt; die Rail-Umkehr (N.9 / P8.6-AE) hat zwei weitere **still** obsolet
   gemacht — sie fordern „Einstellungen oben, Abmelden allein unten", das Gegenteil des heutigen
   Zustands. Nachfolger ist P8.6-42. Nachgetragen in Plan 2 §9.3.
3. **V136 ist nie beantwortet worden.** Plan 2 §8.3 stellt die Frage für Block G; kein einziges
   Block-Protokoll greift sie auf — sie ist durchgerutscht, nicht entschieden. Sie steht deshalb
   als **offen** in der Bilanz, nicht als geschlossen.
4. **V140/V141 waren materiell beantwortet, aber nie bilanziert.** Beide wurden im
   H-R-Mini-Plan als Sichtprüfungs-Marker eröffnet; die H-R-Sichtung fand statt und lieferte die
   drei Befunde, die Block H-R-3 abgearbeitet hat. Unter ihrem Namen abgehakt wurden sie nie —
   in Plan 2 §9.6 nachgeholt.

**Zwei Abnahmezeilen bewusst nicht grün gemeldet**, obwohl der Code tut, was gemeint war:
**P8.6-15** (die geforderte *Zuordnungstabelle im Phase-Head* wurde nie geschrieben — der Sweep
lief, sein Ergebnis hält ein Test) und **P8.6-44** (die `--panel-meta*`-Tokens tragen keinen
`--warn`-Bezug mehr, aber `app.css:770`/`:1306` behalten `rgba(229,169,60,.10)` — beides
**echte** Warn-Elemente mit `border`/`color: var(--warn)`; das Kriterium forderte `grep = 0` und
war damit breiter als sein eigener Zweck). Beide Male ist die Zeile zu weit gefasst, nicht der
Code zu nachlässig — und beide Male wäre ein ✅ eine kleine Lüge.

**Das Nikinger-Feedback vom 2026-09-19** ist im Handover §4.1 abgelegt, **nicht** als flache
Feature-Liste: zwei der acht Punkte sind Bugs und einer ist ein Rechte-Thema. Zu den beiden Bugs
liegt ein erster, read-only gemessener Befund bei, damit der P9-Planer nicht bei null anfängt:
`bindFolderDropTarget()` hat **genau eine** Aufrufstelle (`tree.js:205`, `if (space.own)`) — es
gibt ein Drop-Ziel *in* einen Ordner, aber keines zurück auf die Space-Wurzel; und der globale
ESC-Handler (`app.js:204`) prüft **nicht** auf `document.fullscreenElement`, weshalb ein
Tastendruck auf dem Mac zwei Aktionen auslöst. Beide Befunde sind Hinweise, keine Diagnosen.

**Geschrieben in diesem Commit:** Plan 2 §9 (kanonischer Closeout, P8.6-W) · eine Zeiger-Zeile
in Plan 1 §9 (die einzige erlaubte Änderung am 📕-Snapshot) ·
`docs/concepts/PHASE8_6_CLOSEOUT_HANDOVER.md` von Partial- auf **Abschluss**-Handover P8.6 → P9
umgeschrieben (die beiden von ROADMAP/Head/Plan 2 zitierten Abschnitte §4.5/§4.6 sind im Kopf
gesichert, die alte Fassung liegt in `373a431`) · `phase8_6_ui_polish_uebersicht.svg` neu
gezeichnet, Badge von **PARTIAL CLOSEOUT** auf **45 ✅ · 5 ⚠️ · 0 ⬜**, zwei Bahnen (Plan 1 /
Plan 2) mit der roten Bruchstelle dazwischen · ROADMAP-Zeile und Wurzel-`CLAUDE.md` auf ✅ ·
`docs/INDEX.md` gestrafft und nachgezogen · `screenshots_latest/` auf die Gate-Bilder umgehängt
(P8.6-AK).

**Die Grafik ist vor dem Abschluss gerendert und angesehen worden**, nicht ungesehen gemeldet:
`~/.claude-code-tools/svg_to_png.py` → PNG → gelesen. Der erste Durchgang hatte **sechs**
Textüberläufe (Kopfzeile unter dem Badge, Mission-Zeile 1, Gate-Box, drei VERIFY-Kästen, Fußzeile)
und zwei Pfeile, die von der nachfolgenden `<rect>` überdeckt wurden — SVG kennt keine
z-Reihenfolge außer der Dokumentreihenfolge. Beides behoben, zweiter und dritter Durchgang sauber.

**Rotationsprüfung (Punkt 4 des Auftrags):** der Head trug bei Sessionbeginn **genau einen**
`## Session stopped`-Block (2026-09-18) — das Skript hätte mit Exit 2 abgebrochen. Erst nach dem
Anhängen dieses Blocks sind es zwei, und die Rotation läuft; der 2026-09-18-Block wandert
**verbatim** ins Archiv. Die vier Gegenproben des Skripts (verlustfreier Schnitt, genau ein Block
im neuen Head, byte-identische Ablage, unveränderter Archivbestand) sind der Prüfschritt, der
laut Auftrag bleibt.

**Eine Falle unterwegs, sofort zurückgerollt:** der erste Patch-Versuch an diesem Head hat
`str.index("## Nächste Session")` benutzt — der Treffer lag in der **`updated:`-Frontmatter-Kette**
(Zeile 23), nicht auf der Überschrift (Zeile 570), und hätte 66 KB aus der Datei geschnitten.
`git checkout --` hat den Stand wiederhergestellt, der zweite Versuch schneidet ausschließlich
mit Zeilenumbruch-Ankern und prüft vorher die Trefferzahl (`assert s.count(A) == 1`). Der Head
zitiert seine eigenen Überschriften in der Kette — wer hier ohne Anker schneidet, trifft die
Kopie statt des Originals.

**Selbstprüfung §0.5:** Tabu-Diff leer (diese Session berührt nur `docs/`, `*.md`, `*.svg` und
`screenshots_latest/`) · `pytest` **995 passed** · `ui_budget` 5/5 · kein `node --check` nötig
(kein JS/CSS-Touch) · kein `pkill -f`, kein `systemctl` · `sharefyx-mcp` nicht angefasst ·
keine neue `.md` ohne INDEX-Zeile (das Handover hat seine Zeile behalten, die Grafik ebenfalls).

**Nächster Schritt: P9-Planungssession.** Einstieg ist
`docs/concepts/PHASE8_6_CLOSEOUT_HANDOVER.md`, nicht dieser Head. Dieses Verzeichnis ist ab
jetzt Archiv.
