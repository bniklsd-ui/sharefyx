---
status: live
purpose: Phase-Head Link-Picker-Politur, Titel-statt-ID-Hint, v3-Vorabritt + Deploy — Scope, harte Regeln, Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase8_5_picker_release/ oder an den in §0.3/§2/§3/§4/§5 des Plans genannten Dateien in phase5_ui/webui/static/ phase2_mcp/mcpserver/ scripts/ — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase8_5_picker_release_plan.md   # voller Plan, Entscheidungen P8.5-A–P8.5-T, §0.1 gelockte N1–N7, Steps 0/A/B/C/D/Z
  - ../phase8_ui_graph/CLAUDE.md                       # Phase 8 — schließt diese Phase mit ab (N6, P8.5-R), kein eigenes Handover
  - ../phase8_ui_graph/SESSIONS_ARCHIVE.md              # Bilanz P8-22/P8-24-Smokes, drei §9.4.6-Befunde (Settle/Farbe/Klick), P8.5-Vorgänger-Session-Block
  - SESSIONS_ARCHIVE.md                                 # ältere Session-Blöcke, newest-first
updated: 2026-09-09 (Z-Closeout Claude Code — **Übersichtsgrafik `docs/concepts/phase8_5_picker_release_uebersicht.svg` + `docs/concepts/PHASE8_5_CLOSEOUT_HANDOVER.md` neu**, beide als datierte Umkehr der Locks **P8.5-S** und **P8.5-R** durch den Nikinger (Plan §0.2 mit Korrekturnotiz); **Plan §9.1–§9.7 gefüllt** (P8.5-T, kanonischer Closeout, Handover verweist darauf statt es zu ersetzen); vier Drifts behoben: Modul-Status Zeilen 2–7 standen 🟡/⬜ gegen 20/20 ✅, Plan §9 leer, Zeile 2 nannte `<select>` statt Radiogruppe, `p8x`-§A führte die vierte A3-Probe noch als offen; **neun Nikinger-Feedback-Punkte als `p8x_ui_polish_notes.md` §10** abgelegt + §5/§6/§C-2-Querverweise, **§B Mobile-Hälfte durchgestrichen aufgehoben** (Realtime bleibt draußen), Nummern-Frage „p8.7 vs. P9" bewusst offengelassen; zwei Session-Sub-Blöcke per `sed`+`cmp` rotiert (Skript passt nicht auf das Ein-`##`-Muster), `updated:`-Pipe 22 → 3 Einträge, 19 verbatim ins Archiv (Head 52.609 → 24.569 B); **kein Code-Touch**, pytest **964/964**, Tabu-Diff §0.3 leer, Service-Touch 0 [PID 355956 unverändert]) | 2026-09-09 (P8.5-6-Folge-Smoke — Bracket-Pfad live-verifiziert, Bilanz 19/1/0 → **20/0/0**, Phase 8.5 vollständig abgeschlossen; v3ritt-Wegwerf frisch hochgefahren, Item `itm_b8b989a1` „Vercel [Hosting]" via `storage.Store.create()` angelegt, Mini-Smoke `phase8_5_picker_release/scripts/p856_bracket_mini_smoke.py` neu (~75 Z., Playwright + Login + Edit-Mode + Picker + 2 Screenshots in beiden Varianten); Screenshot `p856_bracket_preview.png` zeigt „Vercel [Hosting]" als **klickbaren blauen Hyperlink** — programmatische Quittung per Regex auf `<a href="#item/itm_b8b989a1">Vercel [Hosting]</a>` True; Wegwerf sauber per PID-Datei gestoppt, kein `pkill -f`; §Abnahmestand Bilanz → **20/0/0**, §Nächste Session auf P8.6-Planung umgeschrieben, Matrix-Zeile P8.5-6 in `SESSIONS_ARCHIVE.md` auf ✅ mit Folge-Smoke-Beleg; **kein Code-Touch**, pytest unverändert 964/964, Tabu-Diff §0.3 leer, Service-Touch 0 [PID 355956 unverändert]) | 2026-09-09 (Sichtung der 10 P8.5-🟡-Zeilen — 9 ✅, P8.5-6 bleibt 🟡 wegen fehlendem Vorschau-Screenshot des Bracket-Pfads; vier neue Sichtungs-Konventionen in `docs/concepts/sichtpruefung_automation_conventions.md` §1-§4 notiert [Vorschau-Pflicht / Code-vs-Visuell / Deploy-nach-Test / Screenshots-im-Chat]; `_tooling.md` Plugin-Empfehlung auf P8.6-first-step verschärft; Walkthrough/Restblock Top-Notizen; §Abnahmestand Bilanz 10/10 → 19/1/0, §Nächste Session komplett umgeschrieben auf P8.5-6-Brake-Pfad; alter Z-Closeout-Block manuell nach `SESSIONS_ARCHIVE.md` rotiert + 10 Matrix-Zeilen mit Nikinger-Vermerk; **kein Code-Touch**, pytest unverändert 964/964, Tabu-Diff §0.3 leer, Service-Touch 0 [PID 355956 unverändert], keine Wegwerf-Instanzen gestartet) | 2026-09-08 (Scope-Reversal + Session-Ende: Nikinger-Entscheidung im Review des Z-Final-Commits — die 10 P8.5-🟡-Sichtungen (P8.5-6, -7, -8, -9, -10, -11, -12, -13, -14, -15) wandern NICHT nach P8.6, sondern bleiben in Phase 8.5 als erste Sache der nächsten Session; Phase 8.5 head bekommt eine neue Sektion „Nächste Session“ mit den 10 Zeilen einzeln + Werkzeug-Setup-Stand, Stand-Summary entsprechend umformuliert; Wurzel-updated:-Pipe vorne ergänzt; Frontmatter vorne ergänzt; **kein Code-Touch**, pytest unverändert 964/964, Tabu-Diff 0.3 leer, Service-Touch 0 [PID 355956 unverändert]) | ältere Einträge (19) verbatim in `SESSIONS_ARCHIVE.md` §updated-Pipe-Archiv
---

# CLAUDE.md — Phase 8.5: Link-Picker-Politur, Titel-statt-ID-Hint, v3-Vorabritt + Deploy (`phase8_5_picker_release/`)

> Kein eigenes Python-Paket (wie `phase3_edge/`, `phase6_shares/`, `phase6_5_tools_images/`,
> `phase7_spaces_admin/`) — Servercode bleibt in `storage`/`mcpserver`/`webui/static`,
> dieses Verzeichnis trägt nur Kopf, Archiv und Skripte. **Quelle der Wahrheit ist der Code,
> nicht dieses Dokument.**

---

## Mission (zuerst lesen)

Drei Restdefekte aus dem Phase-8-Closeout (§9.4.1–§9.4.3 des `phase8_ui_graph_plan.md`) schließen,
einen vollständigen Vorabritt über den nie ausgelieferten v3-Build fahren und ihn live deployen —
diese Phase **schließt Phase 8 formal mit ab** (N6, P8.5-R, Präzedenz P7 Step A8 für Phase 6.5).

**Reihenfolge 0 → A1 → A2 → B1 → C → D → Z:** Step 0 Fundament, Block A Picker (A1 Body-Modus,
A2 Tastatur), Block B Hint, Block C voller v3-Vorabritt (13 Stationen gegen Wegwerf), Block D
Release als **Nikinger-Aktion** (P8.5-Q, Hard Rule 9), Step Z Closeout. **C und D fallen nie,
A1 fällt nie, A2/B1 sind Fallkandidaten in dieser Reihenfolge** (Plan §8). Details, alle sieben
Nikinger-Fragen N1–N7, gelockte Entscheidungen P8.5-A–P8.5-T, Tabu-Liste, Schritt-Sequenz,
Testliste, Abnahmezeilen: `docs/concepts/phase8_5_picker_release_plan.md`.

## Scope (Kurzform, Details: Plan §0.4)

- **DRIN:** §9.4.2 Picker-Modus-Umschalter (Body / Kante, N3), §9.4.3 Tastaturnavigation
  (`aria-activedescendant`-Muster, kein `tabindex`), §9.4.1 Hint generalisierend schärfen
  (Option a, N2, mit Abbruchregel), voller v3-Vorabritt Block C (13 Stationen, N5), Deploy
  v3.0 → v3.0.1 (N7, P8.5-P), Phase-8-Abschluss (N6, P8.5-R), `localStorage`-Persistenz des
  Picker-Modus (P8.5-G), Insert-at-cursor-Helper-Hub auf Modulebene (P8.5-I), CSS-Block-
  Entdopplung am Picker (P8.5-Block-A2).
- **DRAUSSEN:** Phase-8-§9.4.6-Funde (Settle-Zeit / Foreign-Farbe / Knotenklick — bereits am
  2026-09-02 geschlossen, throwaway-verifiziert, **nicht** Bestandteil dieser Phase),
  Phase-8-§9.4.7 Glyph-Entscheidung ✅/🟡 (Nikinger-Sache nach Live-Deploy + Sichtprüfung),
  geerbtes Phase-6/6.5/7-Ledger (`phase8_ui_graph_plan.md` §9.4.5), FastMCP-4/V79 (eigene
  Mini-Phase, P5-C), Body-Volltextsuche in der Web-UI (Q1), Rechteverwaltung über MCP-Tools
  (P6-M), Löschen von Items (F2), `_trash/`-Räumung, Funnel-Watchdog, Mobile/Realtime,
  Light-Mode (P5-X), Dedup zweier Kanten gleicher Richtung mit unterschiedlichem `kind` (V102 —
  nur messen, nicht fixen), Phase-8.5-Übersichtsgrafik (P8.5-S — drei Fixes und ein Deploy
  tragen kein eigenes SVG).

## Harte Regeln dieser Phase (nicht verhandelbar)

- Alle Hard Rules aus Wurzel-`CLAUDE.md` gelten unverändert — insbesondere Hard Rule 9
  (kein `pkill -f`, niemals den systemd-Dienst anfassen), Hard Rule 1 (keine Secrets in
  Dateien), Hard Rule 8 (Commit ⇒ Doku-Update im selben Commit).
- **§0.3 Tabu-Liste — `git diff` muss über die gesamte Phase leer bleiben** bis auf die eine
  erlaubte Ausnahme:
  - `authserver/` vollständig.
  - `mcpserver/` vollständig **außer** dem einen Beschreibungstext-String
    `_TITLE_NOT_ID_HINT` in `phase2_mcp/mcpserver/tools.py:159-164` (P8.5-D, Präzedenz P7-T
    und P8-§0.4).
  - `phase5_ui/webui/security.py` (P8-Q geerbt).
  - `storage/` vollständig — die achte P1-Contract-Öffnung ist seit dem 2026-09-02
    geschlossen, diese Phase öffnet **keine neunte** (P8.5-§0.3).
  - `phase5_ui/webui/api.py`, `serializers.py`, `permissions.py` — Phase 8.5 baut **keine**
    API-Fläche. Findet der Vorabritt (Block C) einen Serverfehler, ist das ein Befund für den
    Nikinger, kein stiller Fix; siehe Plan §4.C3.
  - **Prüfkommando am Step-Ende** (Plan §0.3):
    ```
    git diff --stat main -- phase4_auth/ phase1_storage/storage/ \
        phase5_ui/webui/security.py phase5_ui/webui/api.py \
        phase5_ui/webui/serializers.py phase5_ui/webui/permissions.py phase2_mcp/
    ```
    Einzige erlaubte Zeile: `phase2_mcp/mcpserver/tools.py` (nur der Hint-Text).
    `phase2_mcp/tests/test_tools.py` steht bewusst nicht unter Tabu — der Test zieht mit.
- **§0.5 Selbstprüf-Checkliste am Ende jedes Steps** (Advisor-Ersatz, P8.5-O-Eskalationsregel):
  `pytest -q` grün, Tabu-Diff leer, `node --check` auf jede berührte JS-Datei,
  `python phase5_ui/scripts/ui_budget.py` grün, Fehlerpfad einmal durchdacht, neue `.md`
  haben L1-Card + INDEX-Zeile, kein Service-Touch.
- **Eskalationsregel opencode/M3 → Claude Code** (P8.5-O, neu in dieser Phase): ein Fund,
  dessen Ursache in einer *früheren* CSS-Regel oder in der Kaskade liegt — nicht in der
  Regel, die man gerade ansieht — wird **nicht symptomatisch gepatcht**, sondern an Claude
  Code eskaliert. Erkennungsmerkmal: „der Wert stimmt im Quelltext, sieht im Browser aber
  anders aus". Anlass: 2026-09-02 Chevron-Größe, zwei opencode/M3-Sitzungen kamen daran
  nicht vorbei.
- **Rotationsregel ab Tag 1.** Dieser Head trägt **genau einen** Session-Block. Beim Anlegen
  eines neuen wandert der bisherige **verbatim** nach `SESSIONS_ARCHIVE.md`, newest-first —
  Durchführung über `scripts/rotate_session_block.sh phase8_5_picker_release`, nie von Hand.
- **Commit ⇒ Note-Update, im selben Commit** (Hard Rule 8): Modul-Status-Tabelle + Session-
  Block + INDEX-Zeile + ROADMAP-Absatz + Wurzel-CLAUDE.md-Current-state-Absatz.
- **§0.5.7 — Kein Service-Touch.** `systemctl status sharefyx-mcp` nur **lesend**, PID und
  Uptime im Session-Block notieren.

## Modul-Status

| # | Modul | Step | Status | Tests |
|---|---|---|---|---|
| 1 | Haushalt (0.1–0.4: vier Funde aus Plan §1 abgearbeitet) + Skelett (0.5) | 0 | ✅ | 0 (Skelett, wie P1/P6/6.5/7/8 Step 0) |
| 2 | A1 — §9.4.2 Picker-Modus-Umschalter (gebaut als `<select class="input">`, am 2026-09-07 auf Radiogruppe getauscht — Rückbau auf `<select>` ist P8.6-Arbeit; + `localStorage`) + Insert-at-cursor-Hub + Body-Markdown-Link-Helper | A | ✅ | ✅ (statische Asserts P8.5-5/-9) |
| 3 | A2 — §9.4.3 Tastaturnavigation (`aria-activedescendant`, `_pickLinkPickerAt`, CSS-Block-Entdopplung) | A | ✅ | ✅ (+3) |
| 4 | B1 — §9.4.1 Hint generalisierend schärfen (`_TITLE_NOT_ID_HINT`, zwei neue Asserts in `test_tools.py`, Abbruchregel wörtlich im Head) | B | ✅ | ✅ (+2 Asserts in bestehendem Test) |
| 5 | C — v3-Vorabritt (Wegwerf-Setup + 13-Stationen-Playwright-Smoke in Chromium + Firefox, drei echte Befunde vorgelegt, keine Code-Fixes im Tabu-Bereich nötig) | C | ✅ | ✅ (Chromium 13/13 + Firefox 13/13, 16 Screenshots) |
| 6 | D — Release (D1 Vorbereitung opencode/M3 ✅; **D2 Deploy ✅ als Nikinger-Aktion 2026-09-05** [Release `20260905T140325.378914Z`, HEAD `6f19a8f`, Service-PID **355956**, `ExecMainStartTimestamp=2026-09-05 16:10:18 CEST`]; **D3 Health-Gate ✅** — `scripts/health_gate.sh` neu, **8/8 grün** gelaufen 2026-09-05 15:19:53Z gegen den frischen Deploy; **D4 Sichtprüfung ✅ als Nikinger-Aktion 2026-09-06** [Block 1–7 + Vorbereitung komplett durchgelaufen, drei echte Funde dokumentiert: **P8.5-19 Radiogruppe** statt `<select>` (Tausch 5 Z. ausstehend), **P8.5-6 Bracket-Renderer-Bug** in `markdown.js` (Fix ausstehend), **UX-2-Step-Knotenklick** als neues Feature für p8.X parkiert]; D5 Vierte A3-Probe **✅ 2026-09-08** [der echte Connector nannte den Titel statt der `itm_…`-ID — §9.4.1 damit ohne fünften Hint-Edit geschlossen]; V105 Connector-Check **✅ 2026-09-08** [`list_spaces` über den reconnecteten sharefyx-MCP-Server + echter claude.ai-Chat des Nikingers]) | D | ✅ | ✅ (Health-Gate 8/8 + Sichtprüfung) |
| 7 | Z — Closeout (Plan §9 gefüllt, Phase-8-Nachtrag, §7-Matrix, Übersichtsgrafik + Handover als **Umkehr von P8.5-S/-R**, Rotation, Größenprüfung) | Z | ✅ | ✅ (964 pytest unverändert) |

## Abbruchregel §9.4.1 (N2, verbindlich)

**Wörtlich aus `docs/concepts/phase8_5_picker_release_plan.md` §3 B1:** Taucht die `itm_…`-ID
in einer **vierten** Oberflächenform auf (Fließtext + Tabelle waren die ersten zwei, der
Klammer-/Aufzählungs-Kontext aus Phase 8 §9.4.1 die dritte), wird §9.4.1 als
**Modellverhalten dokumentiert und geschlossen** (Option c). Kein fünfter Hint-Edit, keine
Schema-Änderung an `search_items`. Der Punkt verschwindet dann aus dem Ledger, statt weiter
vererbt zu werden. — Geprüft wird das in Block D5 (vierte A3-Probe nach dem Deploy, wörtlicher
Prüfauftrag im Plan §3 B1).

## Geerbte Contracts

Achte P1-Contract-Öffnung bleibt **geschlossen** (`phase1_storage/CLAUDE.md`); Phase 8.5 öffnet
**keine** weitere (P8.5-§0.3, explizit). P8-§0.4-Tabu-Ausnahme für `_TITLE_NOT_ID_HINT`
verbatim geerbt (P8.5-D); P8-Q-Verbot auf `webui/security.py` verbatim geerbt.

## Abnahmestand (Plan §7, P8.5-1 – P8.5-20)

**Statusregel geaendert 2026-09-08 (Nikinger-Entscheidung, Sichtpruefungs-Automatisierungs-
Sub-Session):** ✅ = live-verifiziert durch den Nikinger — **das schliesst ab sofort eine vom
Nikinger selbst gepruefte Wegwerf-Instanz-Automatisierung mit ein**, nicht mehr nur einen
eigenhaendigen Klick-Durchlauf am echten Geraet. (W) = Wegwerf-Instanz + vom Nikinger gepruefte
Evidenz reicht ab sofort fuer ✅, (L) = weiterhin nur gegen die echte Produktion beweisbar
(Identitaets-Kriterien), (C) = Code/Test reicht. Volle Herleitung:
`docs/concepts/sichtpruefung_automation_conventions.md`. P8.5-19 hat zusaetzlich den
„Superseded am selben Tag"-Marker (Radiogruppe → `<select>`-Rueckbau vorgemerkt fuer P8.6).

**Vollstaendige §7-Abnahmematrix P8.5-1 bis P8.5-20 (alle 20 Zeilen mit Status, Art, Beleg,
Commit-SHA, Screenshot-Verweis und Nikinger-Pruefvermerk wo zutreffend):**
`SESSIONS_ARCHIVE.md` §Abnahmematrix-Archiv (Phase 8.5, Z-Final-Rotation). Bilanz-Summary
und Stand-Zaehlung bleiben direkt unten im Head.


**Stand (2026-09-09):** **20 ✅ · 0 🟡 · 0 ⬜** von 20. **Sichtung 2026-09-09:** die 10 🟡-Zeilen
aus dem 2026-09-08-Stand durchgesehen — **9 davon (P8.5-7, -8, -9, -10, -11, -12, -13, -14, -15)
auf ✅**, weil: entweder grüne statische Tests (P8.5-9/-12/-14, (C)-Art) oder
Smoke-Skript-Asserted-Behavior + Screenshot des Daten-Zustands (P8.5-7/-10/-11/-13/-15,
(W)-Art) oder Smoke-Asserted-Behavior allein (P8.5-8, (W)-Art). Nikinger-Vertrauens-Regel
„Code/auto = M3-Sache, visuell = Nikinger-Sache" (neu in
`docs/concepts/sichtpruefung_automation_conventions.md` §2): die (C)-Zeilen + Smoke-(W)-Zeilen
sind durch den ausführenden Agenten verifiziert, kein zusätzlicher Sichtungs-Schritt nötig,
sofern der Beleg dokumentiert ist. **P8.5-6-Folge-Smoke 2026-09-09:** v3ritt-Wegwerf frisch
hochgefahren, Item „Vercel [Hosting]" (`itm_b8b989a1`) in alpha angelegt, Picker geöffnet,
Link eingefügt, **zwei Screenshots** aufgenommen (`docs/screenshots/p856_bracket_edit_view.png`
+ `p856_bracket_preview.png`); Vorschau-Panel-Screenshot zeigt „Vercel [Hosting]" als
**klickbaren blauen Hyperlink** — Bracket-Fix vom 2026-09-07 damit **live-verifiziert**.
Phase 8.5 springt auf **20 ✅ · 0 🟡 · 0 ⬜**, **Phase 8.5 formal vollständig abgeschlossen**.
**20 ✅:** P8.5-1/-2/-20 (Step 0, Doku), P8.5-3/-4 (2026-09-08, Connector-Live), P8.5-5
(Bauform), P8.5-6 (2026-09-09, Bracket-Pfad-Vorschau), P8.5-7/-8/-9/-10/-11/-12/-13/-14/-15
(2026-09-09, Sichtung der Block-C-Evidenz + Code/Static-Tests grün), P8.5-16 (2026-09-07
Glass-Fallback), P8.5-17 (2026-09-08 V105 + Update-Banner), P8.5-18 (2026-09-07
Sichtprüfung 1+2), P8.5-19 (2026-09-08 Radiogruppe, superseded für P8.6).

> **Wichtige neue Konventionen aus dieser Sichtung (Nikinger-Feedback 2026-09-09):**
> 1. Vorschau-Pflicht bei klickbaren Links (Screenshots müssen den gerenderten Link zeigen,
>    nicht nur die Markdown-Quelle) — `docs/concepts/sichtpruefung_automation_conventions.md` §1.
> 2. Code/automatisierte Tests = M3/Claude-Code-Sache; visuell = Nikinger-Sache — §2.
> 3. Deploy erst nach Testauswertung, nicht danach — §3 (gilt ab P8.6; Phase-8.5-Vorlauf
>    fuhr bereits genau dieses Muster).
> 4. Screenshots im Chat präsentieren, sobald OpenCode-Vision-Plugin installiert ist
>    (P8.6 first step) — §4.

## Vormerkung (2026-09-08, Nikinger-Sichtprüfung C4-1 der Sichtprüfungs-Automatisierungs-Sub-Session)

**Radiogruppe zurück auf die Standard-`<select>`-Auswahlbox (Choice-Konvention v3 aus
`phase8_ui_graph/CLAUDE.md`), die Beschriftung innerhalb der Box statt daneben.** Der Nikinger
hat den Screenshot `docs/screenshots/c4_p8519_01_radiogruppe_im_dialog.png` gesehen (zwei
Radio-Buttons „als Text-Link im Text" / „als Kante (Feld „Links")") und entscheidet sich für
Design-Konsistenz mit dem Rest der App: **die Radiogruppe soll wieder raus, zugunsten des
Standard-`<select class="input">`**, diesmal so, dass die Beschreibung (Label-Text) innerhalb
der Auswahlbox selbst steht statt als externes `<label>` daneben. Das ist eine **Umkehr der
eigenen D4-Entscheidung vom 2026-09-06** („deutlich angenehmer" — siehe P8.5-19-Zeile oben und
`phase8_ui_graph/CLAUDE.md`s Selection/Choice-Konvention-v3-Abschnitt), nicht ein neuer Fund.

**Ausdrücklich nur vormerken, keine Code-Änderung in dieser Session.** Wenn umgesetzt: betrifft
`dialogs.js` (Selektor zurück auf `#link-picker-mode`/`getElementById`), `app.html`
(`<fieldset class="link-picker-modes">` + 2× `<input type="radio">` → `<select
id="link-picker-mode">` mit den zwei `<option>`-Werten `body`/`frontmatter`, Text der Optionen
ist die "innerhalb der Box" Beschreibung), `app.css` (Radiogruppen-Block raus, Standard-`.input`-
Choice-Stil aus der Konvention v3 reicht), `phase5_ui/tests/test_static_routes.py`
(`test_link_picker_uses_a_radio_group_not_a_select` müsste umgekehrt werden — der Testname
selbst wäre dann falsch benannt, Umbenennung nötig). P8.5-19/P8.5-5-Zeilen in der Abnahmestand-
Tabelle oben mit müssten neu bewertet werden, sobald das umgesetzt ist.

## Nächste Phasen (Nikinger-Entscheidung 2026-09-08, noch nicht geplant/gelockt)

Phase 8 und Phase 8.5 sind mit diesem Commit formal ✅ (siehe Bilanz-Abschnitte in
`phase8_ui_graph/CLAUDE.md` und oben). Zwei Folge-Phasen sind besprochen, aber **noch nicht
geplant** (kein Step 0, keine gelockten Entscheidungen — das ist eine künftige
Planungs-Session, kein Auftrag dieser):

- **P8.6 (Arbeitsname) → Deploy-Ziel `v3.0.2`** (Patch-Bump, gleiche Größenklasse wie 8.5
  selbst): Radiogruppe-Rückbau auf `<select>` mit inline-Beschreibung (Vormerkung oben) +
  die restlichen Punkte aus `docs/concepts/p8x_ui_polish_notes.md` (16 Themen, u. a.
  Spaces-Layout-Reorg, „Konto"→„Einstellungen"-Rename, customizable Tags, Feedback-Button,
  De-AI-ierung Lauf 2). **Nikinger-Vorgabe: eines der ersten Punkte in P8.6 ist die
  OpenCode-Vision-Plugin-Installation** (`DavidEasden/opencode-vision`, siehe
  `docs/concepts/sichtpruefung_automation_tooling.md`) — nicht Teil der UI-Politur selbst,
  aber bewusst früh in derselben Phase, damit die nächste Sichtprüfungsrunde davon profitiert.
- **P9 (Arbeitsname) → Deploy-Ziel `v3.1.0`** (Minor-Bump, gleiche Größenklasse wie der
  ursprüngliche v3.0-Design-Umbau): der Obsidian-Map-/Graph-Umbau (die fünf Sub-Punkte aus
  `p8x_ui_polish_notes.md` §2 — Performance-Reload, Landkarten-Stil, Field schneidet ab,
  Reload-Drift, Collapsible mit Abhängigkeiten). **Nikinger-Erwartung: das ist der
  voraussichtlich finale große UI-Umbau** — danach keine weitere Minor-Version-würdige
  Design-Runde in Sicht, nur noch Patch-Politur.

Reihenfolge ist bewusst P8.6 vor P9 (kleine Politur zuerst, inkl. Werkzeug-Verbesserung,
danach der große Graph-Umbau mit besserem Werkzeug in der Hand).

## Nächste Session

**Phase 8.5 ist vollständig abgeschlossen (20 ✅ · 0 🟡 · 0 ⬜), Step Z inklusive.** Der
Closeout liegt in `docs/concepts/phase8_5_picker_release_plan.md` **§9** (kanonisch); das
Einstiegsdokument für die nächste Planung ist
[`docs/concepts/PHASE8_5_CLOSEOUT_HANDOVER.md`](../docs/concepts/PHASE8_5_CLOSEOUT_HANDOVER.md)
**§4** (offene Entscheidungen), nicht mehr dieser Head. Übersichtsgrafik:
`docs/concepts/phase8_5_picker_release_uebersicht.svg`. Der nächste Schritt liegt
**außerhalb** von Phase 8.5: P8.6-Planung in Claude Code (gelockte Entscheidungen + Step 0,
ein Schritt vor dem ersten Code-Commit).
**Nikinger-Vorgabe: erster Punkt in P8.6 ist die OpenCode-Vision-Plugin-Installation**
(`DavidEasden/opencode-vision`, siehe
[`docs/concepts/sichtpruefung_automation_tooling.md`](../docs/concepts/sichtpruefung_automation_tooling.md))
— nicht Teil der UI-Politur selbst, aber bewusst früh in derselben Phase, damit die nächste
Sichtungs-Runde von den Plugin-Erleichterungen profitiert (Screenshots direkt im Chat +
Was-zu-validieren-Zeile darunter).

Reihenfolge unverändert: **P8.6 zuerst** (kleine Politur-Größe wie P8.5 selbst, Ziel
`v3.0.2`), **danach P9** (Obsidian-Map-/Graph-Umbau, Ziel `v3.1.0`, laut Nikinger
voraussichtlich finaler großer UI-Umbau).

Setup-Stand zum Sessionende: Production v3.0.1 live (PID 355956 unverändert, ~3 Tage
Uptime); der v3ritt-Wegwerf wurde nach der P8.5-6-Folge-Smoke sauber per PID-Datei
gestoppt (Hard Rule 9-konform, kein `pkill -f`); zwei Wegwerf-Instanzen aus dem
Cluster-3-Vorlauf (200-Knoten auf 18772, D2 auf 18768) waren schon am 2026-09-08 abgebaut
worden.

## Session stopped

### 2026-09-09 (Z-Closeout-Session Claude Code — Übersichtsgrafik + Handover + Plan-§9, zwei Locks umgekehrt; kein Code-Touch)

**Auftrag:** Phasen-Abschluss-Prompt (Prompt 3, `docs/PROMPTS.md`) — Rückblick auf die
abgeschlossene Phase 8.5, Übersichtsgrafik, Handover, Rotationsprüfung, ein Commit. Dazu
neun Nikinger-Feedback-Punkte, die zwischen den Sessions angefallen sind.

**Zwei gelockte Entscheidungen wurden vom Nikinger selbst umgekehrt** (nicht still
aufgeweicht — an beiden Stellen datiert vermerkt, Plan §0.2):

- **P8.5-S** („keine Übersichtsgrafik für Phase 8.5") → `docs/concepts/phase8_5_picker_release_uebersicht.svg`
  (1080×1080, Stil der Phase-7-Grafik, headless-Chromium gerendert und visuell gegengeprüft).
- **P8.5-R** („kein neues Handover-Dokument") → `docs/concepts/PHASE8_5_CLOSEOUT_HANDOVER.md`.
  **P8.5-T bleibt unangetastet:** Plan §9 ist gefüllt und bleibt der kanonische Closeout,
  das Handover verweist darauf, statt es zu ersetzen.

**Vier Doku/Code-Drifts gefunden und im selben Commit behoben:**

1. **Modul-Status-Tabelle war stale** — Zeilen 2–7 standen auf 🟡/⬜ (A1/A2/B1/C/D 🟡, Z ⬜),
   während der Abnahmestand direkt darunter 20/20 ✅ meldete. Alle sechs Zeilen nachgezogen,
   D5 + V105 mit Datum und Beleg eingetragen.
2. **Plan §9 war leer**, obwohl P8.5-T ihn als kanonischen Closeout festlegt und die Phase
   seit dem 2026-09-08 als abgeschlossen geführt wird. §9.1–§9.7 gefüllt.
3. **Modul-Status Zeile 2 nannte `<select class="input">`** als gebaute Form — seit dem
   Pre-Z-Tausch am 2026-09-07 ist es eine Radiogruppe. Mit Rückbau-Hinweis korrigiert.
4. **`p8x_ui_polish_notes.md` §A** führte die vierte A3-Probe noch als „wird in D5
   entschieden" — sie lief am 2026-09-08 und ist ✅.

**Neun Nikinger-Feedback-Punkte als `p8x_ui_polish_notes.md` §10 abgelegt** (Zitat +
Code-Anker, ungewichtet): Icon-/Trägerflächen-Radien, Hover-Auswahl als transparentere
Standardauswahl, Ordner-/Tags-Auswahl, klickbare Spaces, Einstellungsmenü, alles Klickbare
mit Farbausnahme für „Abmelden"/„Archivieren", verbundene AI-Sessions, Hochkant-/Handy-UI.
Sieben davon sind Verschärfungen von §5/§6 — §5, §6 und §C-2 tragen jetzt Querverweise.
**Im Code geprüft:** `app.css` hat 37 `border-radius`-Deklarationen mit sechs Werten, davon
ein hartkodiertes `6px` in `.link-picker-results` am Token vorbei.

**Zwei Punkte, die bewusst nicht selbst entschieden wurden:**

- **„eher v3.1 also p8.7"** kollidiert mit der dokumentierten Reihe P8.6 → `v3.0.2` /
  P9 → `v3.1.0`. Wortlaut zitiert, **nichts umbenannt** — Frage für die P8.6-Planung.
- **Mobile/Hochkant** stand in `p8x_ui_polish_notes.md` §B und im ROADMAP-Abschnitt als
  bewusste Außenkante. Die Mobile-Hälfte ist jetzt durchgestrichen + datiert aufgehoben;
  **Realtime bleibt draußen.**

**Plan-§6-Step-Z-Punkt 2 nachgeholt** — er war in *keiner* Session erledigt worden: der
Phase-8-Plan (`docs/concepts/phase8_ui_graph_plan.md`) führte §9.4.1/§9.4.2/§9.4.3 weiter als
offene Restdefekte, obwohl Phase 8 seit dem 2026-09-08 auf ✅ steht — ein kalter Leser hätte
dort drei offene Defekte einer abgeschlossenen Phase gefunden. Alle drei tragen jetzt einen
datierten **„✅ ERLEDIGT in Phase 8.5"**-Kopf mit Mechanismus, Commit-SHA und Zeiger auf
Plan §9; §9.4.2 nennt zusätzlich den an P8.6 vererbten V102-Befund. §9.4.7 hat den
vollzogenen ✅-Sprung (**26/0/0**) bekommen, die stale Bilanz „15 ✅ · 10 🟡" ist als
Planungsstand markiert statt gelöscht.

**Rotation:** der Head trug **einen** `## Session stopped` mit **zwei** datierten
`###`-Unterblöcken. `scripts/rotate_session_block.sh` zählt `##`-Überschriften und hätte
„bereits konform" gemeldet — rotiert wurde deshalb per `sed`-Schnitt mit dreifacher
`cmp`-Gegenlesung (Reassemblierung == Original · beide Blöcke byte-identisch im Archiv ·
Archivbestand unverändert), nichts abgetippt. Head **52.609 → 41.469 B**, Archiv
**172.010 → 183.150 B**.

**Selbstprüfung (§0.5):** `pytest -q` **964 passed** in 267 s (unverändert) · Tabu-Diff §0.3
**leer** · kein JS/CSS-Touch, also `node --check`/`ui_budget.py` gegenstandslos ·
**Service-Touch 0** (`systemctl status` nur lesend, PID **355956**, Uptime 3 Tage) · keine
Wegwerf-Instanz gestartet · Größenprüfung gelaufen: `p8x_ui_polish_notes.md` landete beim
Einfügen von §10 bei 41.166 B und wurde durch Kompression der `updated:`-Pipe, des
Intro-Blocks und von §10 selbst auf **40.866 B** unter den Softcap zurückgeholt.

**Nächster Schritt:** P8.6-Planungs-Session in Claude Code. Einstiegsdokument ist
`docs/concepts/PHASE8_5_CLOSEOUT_HANDOVER.md` (§4 = die offenen Entscheidungen), nicht mehr
dieser Head. Erster Punkt der Phase bleibt die OpenCode-Vision-Plugin-Installation.
