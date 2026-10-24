---
status: snapshot
purpose: Plan Phase 10.5 (Finishing — alle Baustellen schließen) gegen main@e5a1879 — Locks P10.5-A–W, Blöcke 0–12 + Z mit Schritten, Ankern, Tests, Abnahme P10.5-1–61 (je Probe und Gegenlauf), Deploys A–D, [VERIFY] ab V207, Rückgabe-Auslöser. Arbeitsliste bleibt das Register.
read-when: vor jedem P10.5-Block — §0–§2 ganz, dann NUR den eigenen Block (grep -n '^## Block')
detail: L2
up: ../../ROADMAP.md
down:
  - ../../phase10_inventory/BAUSTELLENREGISTER.md   # 📗 die Arbeitsliste — hier wird abgehakt (P10-B)
  - ./PHASE10_CLOSEOUT_HANDOVER.md                  # 📕 Einstieg, Befunde für den Blockschnitt
  - ./phase10_inventory_plan.md                     # 📕 Locks P10-A–K, Messanordnung M1–M8
  - ../../phase10_inventory/messung/M1_browser.md   # D-3 = Z1–Z4, Probe Event-Loop/Fokus
  - ../../phase10_inventory/messung/M7_editor.md    # CM5-Messung (Editor Stufe 1)
  - ./phase10_intake.md                             # §9 Note an eurofyx-fleet (Kontextgrenze 400 K)
updated: 2026-10-22 (Block 0 Schritt 0.5 gebaut: INDEX gekürzt 40.772 → 36.889 B, Archiv docs/INDEX_KURZUNG_ARCHIVE.md, Plan-Hebel gemessen zu klein) | 2026-10-21 (Nachtrag: Block-0-Reihenfolge, 0.8 Register-Luft, /mcp gemessen, Proben-Quelle) | 2026-10-21 (freigegeben: Plan, P10-C/P10.5-O, P10.5-N beide Richtungen, Tor P10-8) | 2026-10-20 (angelegt — P10.5-Planungschat, Claude Code/Opus; Fragen R1/R2 vom Nikinger beantwortet)
---
# Phase 10.5 — Finishing (Plan)

> **Status: freigegeben 2026-10-21 (Nikinger), ab jetzt 📕** — Änderungen nur als datierte Nachträge. Am selben Tag freigegeben:
> der `phase4_auth/`-Eingriff (P10-C, Lock P10.5-O), P10.5-N in **beiden** Richtungen und das Register-Tor P10-8 (Register-Kopf).
> Block 0 überträgt die Freigaben in den Phase-Head `phase10_5_finishing/CLAUDE.md`.
> **[Nachtrag 2026-10-21, Planungschat]** Vier Korrekturen nach der Freigabe, inline als `[Nachtrag 2026-10-21]` markiert, keine
> Design-Änderung: Block-0-Reihenfolge (INDEX-Luft zuerst), neuer Schritt 0.8 (Register-Luft), `/mcp`-Begründung gemessen (6.3), Quelle der
> Protokoll-Probe (5.6).
>
> **[Nachtrag 2026-10-22, Block 0 — Ausführer MiniMax M3.1 Flash]** Schritt **0.5** ist gebaut, und der Plan-Hebel
> hat **nicht** gereicht: **gemessen** tragen die acht `## Phase …`-Zeilen zusammen **2.478 B**, und mit einer neuen Zeile
> von ≤ 120 B ist die Ersparnis **höchstens ~1,7 B** — die geforderten 3.000 B sind aus den Köpfen **nicht erreichbar**
> (der Plan nennt „P8.6 allein ~600 B" — das stimmt: 617 B; nur die Summe fehlte). **Der Zielwert bleibt, der Hebel
> wurde erweitert:** zusätzlich wandern drei Kartenzeilen-Chroniken und die Chronik der Karte selbst in das Archiv.
> **Zwei Abweichungen, beide datiert und begründet:**
> **(1)** Das Archiv heißt `docs/INDEX_KURZUNG_ARCHIVE.md` statt `docs/INDEX_HEADINGS_ARCHIVE.md` — es trägt mehr als
> Überschriften, und ein Name, der lügt, ist schlimmer als eine Umbenennung.
> **(2)** Der Plan nannte **eine** neue INDEX-Zeile; es werden **vier** (dieses Archiv, `ENTSCHEIDUNGEN_ARCHIVE.md`,
> der Phase-Head und sein `SESSIONS_ARCHIVE.md`) — dafür war die zusätzliche Kürzung nötig.
> **Gemessen:** Karte **40.772 B → 36.889 B** (Ersparnis **4.171 B**, Luft **4.071 B** unter 40.960 B), `doc_health` **0**,
> `test_index_archive.py` grün, neue Wächter `phase10_5_finishing/tests/test_index_shortening.py` **5/5**
> (Rundeweg byteweise, Abbruch ohne Zielberührung, das Skript legt das Archiv nicht an).
> **Keine Design-Änderung**, keine Lock-Verletzung: DO-2 bleibt DO-2, nur der Hebel ist der gemessene.

> **Auftrag in einem Satz:** P10.5 schließt jede Registerzeile mit Ziel P10.5 — Betrieb, Fehler, Performance, MCP-Schicht
> (FastMCP 4), Anbieter-Unabhängigkeit, Darstellung, Gehirnkarte, Umbenennen, Suche, Realtime, Editor Stufe 1+2, Doku —
> und endet erst, wenn ein Nicht-Claude-Client live `list_spaces` ausführt, mit zwei Modellanbietern (P10-J).
> Das Bild des Nikingers: das Haus fertig bauen und dämmen. Neues kommt erst in P11.

**Gegen:** `main@e5a1879` (2026-10-20), live `v3.1.4` (`d04c0ec`, Release `20261008T201607.460757Z`: `fastmcp 3.4.7`,
`mcp 1.30.0`, `starlette 1.7.0`), Dev-venv `fastmcp 3.4.7`/`mcp 1.28.1`/`starlette 1.3.1`, `pytest` **1268** grün.
Alle Zeilenanker in diesem Plan sind **Stand `e5a1879`**. Wer einen Block startet, prüft sie nach (Prompt 1: verifizieren
und verankern, nicht neu herleiten). Die Funktionsnamen sind stabil, die Zeilennummern wandern.

## Leseanleitung (für jeden Ausführer — zuerst lesen)

1. Lies **§0, §1, §2 ganz** und danach **nur den Abschnitt deines Blocks**: `grep -n '^## Block' docs/concepts/phase10_5_finishing_plan.md`
   und dann `sed -n '<von>,<bis>p' … | cut -c1-220`. Lies den Plan nie ganz in eine Session; er ist dafür zu groß.
2. **Langzeilen-Falle:** Die Doku dieses Repos hat Absätze als Einzelzeilen. Jede Ausgabe mit `| cut -c1-220` oder `| head -c 4000`
   begrenzen. `head -60` hat einmal 41 K Zeichen geliefert (Review GLM §1.1).
3. **Keine Ganz-Datei-Reads alter Phasen-Skripte als Vorlage.** Die Vorlagen stehen in diesem Plan beim Namen; lies daraus die
   Funktion, die du brauchst (`grep -n 'def ' … `), nicht die Datei.
4. **Eine Session je Block-Schritt** (Lock P10.5-C). Übergabe zwischen Sessions nur über den Session-Block im Phase-Head.

---

## §0 Gelockte Entscheidungen

### §0.1 Locks P10.5-A–W

| Lock | Entscheidung | Herkunft |
|---|---|---|
| **P10.5-A** | **Umfang = jede Registerzeile mit Ziel P10.5** (39 Zeilen, `BAUSTELLENREGISTER.md`) plus die Ergänzungen dieses Plans (`constraints.txt`, `/mcp` ohne Slash, Shutdown-Frist, INDEX-Luft). Das Register bleibt die Arbeitsliste (P10-B): abgehakt wird **dort**, je Zeile mit Datum und Beleg. Kein zweites Register. | P10-A/B, Handover §2 |
| **P10.5-B** | **Ausführer = MiniMax M3.1 Flash (offiziell) über opencode, als Open-Test; Rückfall MiniMax M3.** Die Bewertung machen Trading-Bot und eurofyx-fleet, nicht dieser Plan. Baseline sind die M3- und M3.1-Flash-Werte aus dem Trading-Bot. Dieser Plan schreibt **keine** Bewertungsrubrik, er sorgt nur für die Rohdaten: **(1)** Modell-Trailer in jedem Commit, `Co-Authored-By: opencode/MiniMax-M3.1-Flash <noreply@minimax.io>` (Rückfall: `opencode/MiniMax-M3`), **(2)** je Block im Session-Block: Wanduhrzeit, Modellaufrufe/Kontingent laut Anbieter-Anzeige (wenn sichtbar), **(3)** Eingriffe des Nikingers und von Claude Code, gezählt, **(4)** beim Gegenlesen gefundene Fehler, auch in Betreffzeilen. Der Plan ist ausführer-agnostisch: Ein Ausführerwechsel ist **kein Planwechsel**. Löst **P10-E und P10-K** datiert ab. | Nikinger 2026-10-20 (PS), Review §5 |
| **P10.5-C** | **Kontextgrenze 400.000 Tokens** für das Ausführer-Modell in opencode. Sie wird **von eurofyx-fleet gesetzt** (Note `phase10_intake.md` §9), nicht von diesem Repo. Vor jedem Block wird geprüft: Ist `limit.context` > 400.000, wird der Block nicht gestartet (Rückgabe an den Nikinger). Dazu gilt: **eine Session je Block-Schritt.** | Nikinger 2026-10-20 (R2), Handover §5 Nr. 3 |
| **P10.5-D** | **Rollen.** *Claude Code* macht Block 0, die Deploy-Vorbereitung A–D, alle Browser-/Playwright-Proben und Screenshots, Block 12 und Z. *Der Ausführer* macht die Code-Blöcke 1–11. *Der Nikinger* macht jeden `sudo`/`systemctl`-Aufruf, `deploy.sh`, VPS (V199), CT 111, jede Live-Abnahme und jede Sichtung. **Hard Rule 9 gilt ohne Ausnahme:** Kein Agent ruft `systemctl` auf, kein `pkill -f`, Wegwerf-Instanzen werden nur per PID-Datei oder Port gestoppt. | P9 §0.5, Hard Rule 9 |
| **P10.5-E** | **Erlaubte Pfade je Block** stehen im Blockkopf. Abbruchprüfung am Blockende: `git diff --stat <block-basis>..HEAD -- . ':!<erlaubte Pfade>'` muss leer sein, außer `.md`-Doku. Ein Treffer heißt **Rückgabe**, kein „kurz mitgemacht". | Advisor 2026-10-20 |
| **P10.5-F** | **Fünf P1-Öffnungen, angekündigt und eng geprobt** (Zählung nach P9, Index in `phase1_storage/CLAUDE.md`): **(11)** Format-Konvention Stufe 2 — reine Konvention, **kein Code in `storage/`**; **(12)** `created_by`; **(13)** `Store.rename_folder()`; **(14)** `Store.rename_space()`, nur Team-Spaces; **(15)** EXIF-Bereinigung in `Store.put_asset()`. (11)/(12) entschied der Nikinger am 2026-10-18 (D-4/D-16), (13)–(15) gab er am 2026-10-20 frei. Abbruchkriterium je Block: `git diff --stat <block-basis>..HEAD -- phase1_storage/storage` nennt **nur** die im Block angekündigten Dateien. | D-4, D-16, Nikinger 2026-10-20 (R1) |
| **P10.5-G** | **PF-1 = ein Durchgang im Adapter.** `_overview` zählt alle Eimer aus **einem** `store.search()`, ohne P1-Eingriff. Gemessen: 109 ms statt 2.436 ms im M2-Seed. **Rückfall:** Ist `result.total > len(result.items)` (mehr als `_STORE_FETCH_LIMIT` = 5000 Items), fällt `_overview` auf den heutigen Pfad zurück: Korrektheit vor Tempo. Eine Zählung über den Index (0,4 ms, eine P1-Öffnung) kommt erst, wenn live nach Deploy A > 300 ms gemessen werden. Dann entscheidet der Nikinger neu (Handover §5 Nr. 5). | Nikinger 2026-10-20 (R1) |
| **P10.5-H** | **Editor = CodeMirror 5, nachgeladen beim ersten Öffnen eines Editors.** Der Erstaufruf bleibt im 250-KB-Korridor. `ui_budget.py` bekommt eine **zweite** Zeile „Editor nachgeladen (gzip)" mit Grenze 80 KB. Ein Wächter verlangt, dass **jede** Datei unter `webui/static/` genau einer der beiden Zeilen zugeordnet ist (heute zählt `ui_budget.py:237` nur `js/*.js`; ein Unterordner entkäme still). Lädt CM5 nicht, fällt der Editor auf die Textarea zurück (= Rohmodus, ED-5). | Nikinger 2026-10-20 (R1), M7 |
| **P10.5-I** | **Stufe 2 = Pandoc-Attribute mit geschlossenem Vokabular.** Inline `[Text]{.rot}`, `[Text]{.rot .gross}`; Block `::: {.zentriert}` … `:::`. Vokabular: Farben `rot orange gruen blau grau`, Größen `klein gross`, Ausrichtung `links zentriert rechts` (nur Block). Kein HTML-Durchlass, kein `style=`. Eine unbekannte Klasse wird **wörtlich** angezeigt (verlustfrei, sichtbar). `storage/` bleibt dafür unberührt. | Nikinger 2026-10-20 (R1), D-4 |
| **P10.5-J** | **LG-4 = `append_to_items`**: mehrere Items in einem Aufruf, je Eintrag eigene `version` (Hard Rule 3), eigener Store-Write, eigene Quittung. Teilerfolg ist möglich und wird je Eintrag gemeldet. Kein Alles-oder-nichts über Dateien hinweg, höchstens 20 Einträge. Löst P6.5-N3 datiert ab. | Nikinger 2026-10-20 (R2), D-17 |
| **P10.5-K** | **P10-J, zweiter Modellanbieter = ein lokales Modell über Ollama auf CT 111** (`192.168.68.140:11434`). Lauf 1 der Live-Abnahme: opencode + M3.1 Flash. Lauf 2: opencode + Ollama-Provider. Der Server sieht beide Male denselben Client. | Nikinger 2026-10-20 (R2) |
| **P10.5-L** | **Realtime = Server-Sent Events** auf `GET /api/v1/events` (Cookie-Sitzung). Die Quelle ist ein **Git-HEAD-Wächter**: Hard Rule 5 macht aus jedem erfolgreichen Write einen Commit, also heißt „HEAD hat sich bewegt" genau „Daten haben sich geändert". Das gilt für MCP, Web und Hand-Edits gleichermaßen, ohne Eingriff in die Schreibpfade. Gemeldet werden nur Space-Namen, die die Sitzung sehen darf. Der 20-s-Poll wird zum Rückfall (120 s, nur solange der Stream nicht offen ist). Ein Neustart wartet auf offene Streams höchstens **10 s**. | Plan, D-17 (LG-2) |
| **P10.5-M** | **Umbenennen nur für Ordner und Team-Spaces.** Home-Spaces werden in P10.5 nie umbenannt: Ihr Name ist die Identität (Auth-DB, Token-Familien, Freigabelisten, `assignee`, `updated_by`). Umbenennen ist human-only (Web-UI), kein MCP-Werkzeug (Linie von RE-6). | Nikinger 2026-10-20 (R1) |
| **P10.5-N** | **P10-I wird in `SharePolicy` durchgesetzt**, also auf beiden Flächen über eine Regel: Kein Item wandert **in** den Home-Space eines anderen — und, **freigegeben 2026-10-21**, auch nicht **aus** dem Home-Space eines anderen heraus (das wäre dort ein Löschen; P9-K sperrt Löschen in fremden Home-Spaces). Team-Spaces bleiben frei. | P10-I, P9-K, Nikinger 2026-10-21 |
| **P10.5-O** | **Eingriff in `phase4_auth/` (P10-C), minimal.** **(1)** `redirect_uri_allowed()` kennt eine zweite Regel: exakt `http://127.0.0.1:<port><pfad>` mit explizitem Port, ohne Userinfo, Query oder Fragment. **(2)** `register_client()` nimmt `application_type` ∈ {fehlend, `null`, `"native"`, `"web"`} an; `"web"` zusammen mit einer Loopback-Adresse wird abgelehnt (`invalid_redirect_uri`), jeder andere Wert → `invalid_client_metadata`. **(3)** CSP `form-action` bekommt `http://127.0.0.1:*`. **Bewusst nicht:** kein portagnostischer Vergleich (RFC 8252 §7.3) — opencode nutzt einen festen Port, und ein portagnostischer Vergleich hätte den byte-genauen Abgleich in `flows.py:98` geändert (der `[SEAM]` verspricht „diese Funktion und ihre Tests, sonst nichts"). Kein `localhost`, kein `[::1]`: Eine CSP-Host-Quelle kann kein IPv6-Literal ausdrücken (V210). `flows.py` bleibt unberührt. **Freigegeben 2026-10-21 (Nikinger).** | P10-C, D-8, Nikinger 2026-10-21 |
| **P10.5-P** | **FastMCP 4.** Exakter Pin auf die beim Blockstart neueste `4.1.x` (V207), nie ein Range-Pin (P3-D). Beide Protokoll-Ären werden getestet: `legacy` (Handshake `2025-11-25`, so verbindet sich claude.ai heute) und `auto` (`2026-07-28`, zustandslos). **P9-R wird datiert abgelöst** (Kommentar in `phase2_mcp/pyproject.toml`). Der Rückweg ist `rollback.sh` (jedes Release hat sein eigenes venv, kein Schema-/Datenwechsel in Block 5). | D-17 (PA-5), Trockenlauf §1.2 |
| **P10.5-Q** | **`constraints.txt` (Repo-Wurzel) ist die einzige Quelle aller transitiven Versionen.** `scripts/dev_install.sh` installiert mit `-c constraints.txt` (Dev und Deploy, ein Weg). Ein Wächter vergleicht installiert gegen Constraints, er läuft im Release-venv mit (`deploy.sh:169`). Das ist BT-6/D-13 („`mcp` exakt pinnen"), zu Ende gedacht: Live ist bereits gedriftet (`starlette` 1.7.0 live, 1.3.1 dev). | D-13, Befund 2026-10-20 |
| **P10.5-R** | **Vier Deploys:** A nach Block 1–4, B nach 5–6, C nach 7–8, D nach 9–11. Default sind Patch-Bumps `v3.1.5`–`v3.1.8`. Ein Minor-Sprung (etwa `v3.2.0` für Deploy B) ist die Entscheidung des Nikingers, nie eines Agenten. Jedes Deploy: Badge, `UPDATE_LOG`, `deploy.sh` (Nikinger), `health_gate.sh` mit **echter Ausgabe** im Commit. | Memory „UI version scheme" |
| **P10.5-S** | **Hard Rule 3 gegen Platzhalter, Realtime und Cache:** Kein Ladezustand, kein zwischengespeicherter Stand und kein Realtime-Ereignis trägt je eine `version` in einen Write. Geschrieben wird nur mit der `version` des zuletzt **vollständig geladenen** Items. Ein geänderter Editor wird nie überschrieben. | M1 §D-3 |
| **P10.5-T** | **Session-Block ≤ 4 KiB** (DO-3), mit Wächtertest in `phase10_5_finishing/tests/`. | D-17 (DO-3) |
| **P10.5-U** | **Nummerierung:** Locks `P10.5-A…`, Abnahme `P10.5-1…`, `[VERIFY]` ab **V207**. Blöcke tragen Ziffern 0–12 und Z, kein Buchstabe kollidiert mit einem Lock. | P10-G |
| **P10.5-V** | **Kurzname `finishing`:** Verzeichnis `phase10_5_finishing/`, dieser Plan, später `PHASE10_5_CLOSEOUT_HANDOVER.md`. | Handover §5 Nr. 6 |
| **P10.5-W** | **`created_by` ohne Backfill.** Neue Items tragen das Feld, alte bleiben ohne. Die UI zeigt dann nichts an. Ein leeres Feld wird nie erfunden (dieselbe Regel wie `updated_by`). | Plan |

### §0.2 Was P10.5 ausdrücklich nicht tut

CIMD und ChatGPT (PA-3/PA-4 → P11/nicht geplant) · Home-Spaces umbenennen (P10.5-M) · Excel-Tabellen (ED-4), Handy-Oberfläche (UI-7),
verbundene AI-Sessions (LG-11) → P11 · Light-Mode, Papierkorb leeren, Rechteverwaltung über MCP (verworfen) · PF-3 (Cache) und PF-5
(Virtualisierung), solange Z1–Z3 gemessen halten · portagnostische Loopback-Redirects · jede Form von „Verstehen" im Server
(Kernprinzip: EXIF-Strip ist Byte-Chirurgie, Realtime meldet nur Space-Namen und einen Commit-Hash).

### §0.3 Termine, keine Blocker

Arbeitslaptop-Test um den **2026-11-02**, danach `LEGACY_UNTIL` setzen (BT-5, D-15) · Fabian-Zeilen AL-2/AL-6 (V150) · einmalige Bewertung
P6.5-14 (AL-4) · Marktblick ~2026-11-10 (extern, Trading-Bot/eurofyx-fleet) · M3-Endpunkt zugesagt bis 2026-11-15 · V203 (Funnel-Wächter) bei
eurofyx-fleet.

---

## §1 Ausgangslage (gemessen in der Planungssession, 2026-10-20)

### §1.1 Step-0-Befund (Verifikations-Durchlauf)

`scripts/doc_health.py` → **0 Befunde** (`index_lines`, `header_cards`, `updown_links`, `oversize`). 29 Dateien > 40 KB, alle 📕/📦 außer
den drei bekannten „benannt statt versteckt"-Heads (`phase8_6_ui_polish/CLAUDE.md` 109.230 B, `phase8_ui_graph/CLAUDE.md` 47.861 B,
`phase6_shares/CLAUDE.md` 41.032 B → DO-1, Block 12). **Ein Befund mit Handlungsbedarf:** `docs/INDEX.md` steht bei **40.450 B** gegen die
harte Grenze **40.960 B** (`phase9_hardening/tests/test_index_archive.py:39`, `SOFTCAP_BYTES = 40 * 1024`). Jede P10.5-Datei braucht eine
Zeile, also muss Block 0 zuerst Platz schaffen. Sonst: nichts zu tun.

### §1.2 FastMCP-4-Trockenlauf (Wegwerf-venv `~/.claude-code-tools/p105-fmcp4-venv`, außerhalb des Repos)

`fastmcp 4.1.2` (am 2026-10-20 erschienen) zieht `mcp 2.3.0`, `mcp-types 2.3.0`, `httpx2 2.15.1` und `starlette 1.9.0`.

| Lauf | Ergebnis |
|---|---|
| volle Suite | **1267 grün, 1 rot**: `test_step_h_deps.py::test_the_installed_fastmcp_matches_the_pin` (erwartet) |
| P2–P9-Suite mit `FASTMCP_MCP_CAMELCASE_COMPAT=false`, Warnungen sichtbar | **1033 grün, 3 rot**: Pin-Wächter + `phase2_mcp/tests/test_app.py:384–387` (`readOnlyHint` … liest camelCase) + `phase2_mcp/tests/test_tools.py:921` (`content.mimeType`) — **reine Testanpassungen, kein Produktcode** |
| `mcp_smoke.py` / `oauth_smoke.py` / `ui_budget.py` | 16/16 · 11/11 · grün (alte `httpx`-`ASGITransport`-Fabriken laufen weiter) |
| Protokoll-Probe gegen `create_app()` | Client `mode="auto"` → **`2026-07-28`**, `mode="legacy"` → **`2025-11-25`**; Annotations in beiden Ären korrekt; `initialize` mit `2026-07-28`-Angebot → `2025-11-25` (richtig: die neue Ära hat keinen Handshake) |

Folgerung: Block 5 ist eine Pin-, Test- und Abnahmefrage, kein Umbau. **Live-Fakt:** `mcp 1.30.0` (live) kennt Protokolle nur bis
`2025-11-25` (`SUPPORTED_PROTOCOL_VERSIONS`). claude.ai rollt `2026-07-28` laut Anthropic-Blog noch aus. Nach Block 5 bedient der Server
beide Ären.

### §1.3 PF-1-Messung (M2-Seed 4 × 50, Dev-venv, in-process)

Heutiger Weg (6 × `search()` je Space) **2.435,9 ms** · ein `search()` über alles **109,0 ms** · `index.all_rows()` **0,4 ms**.
Ursache: `Store.search()` (`phase1_storage/storage/store.py:552`) lädt bei **jedem** Aufruf jede indizierte Datei (`_row_to_item`).
Der Bench misst etwa halb so lang wie live (2,4 s gegen 4,8 s). Z1 ist damit **plausibel, nicht bewiesen**, und die Live-Messung nach
Deploy A ist Teil der Abnahme.

### §1.4 Größen, die beim Bauen zählen

| Datei | Stand | Grenze | Luft |
|---|---|---|---|
| `docs/INDEX.md` | 40.772 B (nach dem Plan-Commit) | 40.960 B (Test) | 188 B → **[Nachtrag 2026-10-21]** Block 0.5 ist der erste Schreibschritt |
| `BAUSTELLENREGISTER.md` | 40.954 B (nach dem Tor) | 40.960 B | 6 B → **[Nachtrag 2026-10-21]** Block 0.8 schafft ≥ 3 KB; vorher wird nicht abgehakt |
| `ROADMAP.md` | 37.055 B | 37.725 B (P9-6-Band ±2.048 B um 35.677 B, `test_acceptance_numbers.py:332`) | 670 B → Block 0 (DO-2) |
| UI-Budget (`ui_budget.py`, Zeile 3) | 177.264 B gz | 256.000 B | 78.736 B; CM5 (65,6 KB) würde ~11 KB übrig lassen → P10.5-H |

### §1.5 Fallen, die dieser Plan schon kennt

| Falle | Wo | Was zu tun ist |
|---|---|---|
| Test-Harness erbt `SHAREFYX_*`/`SFX_*`/`SPACE_*` | jede Shell | Tests immer mit bereinigter Umgebung (Memory; einmal 52 Neustarts der Produktion) |
| Arbeitsverzeichnis im `DATA_ROOT` | BT-13 | vor dem ersten Schreibschritt `pwd` prüfen: muss `…/dev/savefxy` sein |
| Wegwerf aus P10 trägt 500 Bulk-Items | `/tmp/opencode/sharefyx-wegwerf-p10` | für jede Probe **neu** anlegen (`phase10_inventory/probes/p10_wegwerf.py`) |
| `/mcp` ohne Slash → 307 | `mcpserver/app.py` (`Mount("/mcp")`) | Block 6 bedient `/mcp` exakt |
| Uvicorn wartet unbegrenzt auf offene Streams | `phase2_mcp/scripts/serve.py:77` (kein `timeout_graceful_shutdown`) | Block 10, bevor SSE live geht |
| `space` steht im Frontmatter jeder Item-Datei | `store.py:55/74`, Golden `phase6_shares/tests/golden/*.md` | `rename_space` schreibt jede Datei um (Block 9) |
| `ui_budget.py:237` zählt nur `js/*.js` | Budget | Block 11: Zuordnungs-Wächter |
| `test_clients.py:63` verlangt die Ablehnung von `native` | P4-Policy | Block 6 dreht den Test bewusst um (dokumentiert) |
| drei P9-Tests verlangen `reverse_proxy` einzeilig | `test_tail_proxy.py:294`, `:325`, `:389` | Block 1 passt die Regex an die Blockform an |
| opencode deklariert M3/M3.1 Flash mit 1 M Kontext | `~/.cache/opencode/models.json` | P10.5-C: 400 K durch Fleet, Prüfung vor jedem Block |

---

## §2 Arbeitsregeln für jeden Block

### §2.1 Ablauf einer Block-Session

1. **Kontextgrenze prüfen** (P10.5-C): Für das Ausführer-Modell gilt `limit.context ≤ 400000` in der wirksamen opencode-Konfiguration
   (`~/.config/opencode/opencode.json`, Überschreibung je Modell; sonst `~/.cache/opencode/models.json`). Ist der Wert > 400.000 → **Stopp**.
2. `pwd` = Repo. `git status` sauber. Notiere die Blockbasis: `git rev-parse HEAD` → Session-Block.
3. Lies §0–§2 und deinen Block. Prüfe die Anker deines Schritts (`grep -n`), bevor du editierst.
4. Arbeite **atomar** entlang der Schritte. Ein Commit je abgeschlossenem Schritt. Kein Schritt ist „fertig" ohne grünes `pytest`.
5. **Tests immer mit bereinigter Umgebung:**
   `env -u PYTHONPATH $(env | grep -oE '^(SHAREFYX_|SFX_|SPACE_)[A-Z_]*' | sed 's/^/-u /') .venv/bin/python -m pytest -q`
6. Am Blockende: Abbruchprüfung (P10.5-E, P10.5-F), Register-Zeilen abhaken (§2.2), Phase-Head nachziehen (Hard Rule 8).

### §2.2 Commits, Register, Session-Block

- **Betreff:** `phase 10.5: Block <n>.<schritt> -- <was> (<Register-IDs>); pytest <zahl> gruen`. **Lies den Betreff vor dem Commit
  einmal gegen** (GLM-Lehre: Glitches in Betreffzeilen).
- **Trailer:** den Modell-Trailer aus P10.5-B in jedem Commit des Ausführers. Commits von Claude Code tragen ihren eigenen Trailer.
- **Hard Rule 8:** Jeder Schritt-Abschluss-Commit zieht im **selben** Commit die Modulstatus-Tabelle des Heads und den Session-Block nach.
  Eine neue `.md` bekommt im selben Commit eine L1-Card und eine INDEX-Zeile.
- **Register abhaken:** In `BAUSTELLENREGISTER.md` wird die Ziel-Spalte der Zeile ersetzt, nicht ergänzt, etwa `P10.5` → `✅ 10-2x (B4)`
  (**[Nachtrag 2026-10-21]** die Luft dafür schafft Block 0.8; vorher wird nicht abgehakt). Belege stehen im Head bzw. im Commit, nicht im Register.
- **Session-Block (≤ 4 KiB, P10.5-T),** fest gegliedert: *Ergebnis* · *Geliefert (Commits)* · *Gemessen* (pytest, Proben) ·
  *Ausführer-Daten* (Modell, Wanduhrzeit, Aufrufe/Kontingent, Eingriffe Nikinger/Claude Code, Gegenlese-Funde) · *Offen/Nächster Schritt*.
  Der vorige Block rotiert **per Skript**: `scripts/rotate_session_block.sh phase10_5_finishing`.

### §2.3 Wegwerf-Instanz (Proben)

Eigener Port **8799**, `tmp`-`DATA_ROOT`, `tmp`-`auth.sqlite3`, bereinigte Umgebung, Start und Stopp über die PID-Datei des
Wegwerf-Skripts. Vorlage: `phase10_inventory/probes/p10_wegwerf.py` (zwei Principale, Muster aus
`docs/concepts/sichtpruefung_automation_conventions.md`). Playwright aus `~/.claude-code-tools/e2e-venv`. Probe-Skripte von P10.5 liegen
unter `phase10_5_finishing/probes/`, Rohwerte als JSON daneben (Muster P10). **Nie** gegen `DATA_ROOT`, die echte `auth.sqlite3`
oder den Keyring.

### §2.4 Rückgabe-Auslöser (allgemein — der Ausführer stoppt und meldet im Session-Block)

1. Ein Schritt braucht eine Datei außerhalb der erlaubten Pfade (P10.5-E).
2. `git diff --stat -- phase1_storage/storage` zeigt eine nicht angekündigte Datei (P10.5-F).
3. Ein Test **außerhalb** des Blocks wird rot und der Grund ist nicht offensichtlich der eigene Diff.
4. Ein `[VERIFY]` fällt anders aus als der Plan annimmt.
5. Der Plan ist mehrdeutig oder widerspricht dem Code. Dann gilt: Der Code gewinnt, eine kleine Drift wird mit datierter Notiz gefixt,
   eine große geht an den Nikinger.
6. Irgendetwas verlangt `systemctl`, `sudo`, den echten `DATA_ROOT`, die echte `auth.sqlite3` oder den Keyring.
7. Drei erfolglose Anläufe am selben Fehler.
8. Der Kontext der Session geht über 300 K, ohne dass der Schritt fertig ist: Schnitt, Übergabe im Session-Block, neue Session.

### §2.5 Deploy-Ablauf (A–D, gleich jedes Mal)

| # | Schritt | Wer |
|---|---|---|
| D1 | Volle Suite grün, `doc_health` 0, `ui_budget.py` grün (alle Zeilen) | Claude Code |
| D2 | Badge `phase5_ui/webui/static/app.html:20` (`.rail__version`) auf die neue Version · `docs/UPDATE_LOG.md`-Eintrag `## <Deploy-Tag>`, jede Aussage **eine** `- `-Zeile, deutsch, für Menschen | Claude Code |
| D3 | Commit + Push | Claude Code |
| D4 | `SHAREFYX_RELEASES_DIR=/opt/sharefyx/releases SHAREFYX_CURRENT_LINK=/opt/sharefyx/current SHAREFYX_DATA_ROOT=/home/savefyx/savefyx-data SHAREFYX_BACKUP_DIR=/var/lib/sharefyx-backup SHAREFYX_SYSTEMCTL="sudo systemctl" phase5_ui/scripts/deploy.sh main` (`[VERIFY]` gegen die letzte P9-Ausführung, `phase9_hardening/SESSIONS_ARCHIVE.md`) | **Nikinger** |
| D5 | `phase8_5_picker_release/scripts/health_gate.sh --expected-version=<v> --require-todays-update-log --expected-sha=<sha>` — **die echte Ausgabe** gehört in den Session-Block, nie die Behauptung | Claude Code (liest) |
| D6 | Live-Prüfungen des Deploys (je Deploy unten) | Nikinger |
| D7 | Bei Rot: `phase5_ui/scripts/rollback.sh` | **Nikinger** |

---

## §3 Blockübersicht

| Block | Inhalt (Register) | Wer | Gr. | Deploy | Erlaubte Pfade (Code) |
|---|---|---|---|---|---|
| 0 | Haushalt: Verifikation, Phase-Head, INDEX-Luft, Register-Luft, DO-2, DO-3, Ausführer-Vorbedingung | Claude Code | S | — | `phase10_5_finishing/`, `docs/`, `ROADMAP.md`, `pytest.ini`, `phase9_hardening/tests/test_acceptance_numbers.py`, `phase10_inventory/*.md` (0.8, Nachtrag 2026-10-21) |
| 1 | Betrieb: BT-1, BT-2, BT-6 (+ `constraints.txt`) | Ausführer + Nikinger | S | A | `phase9_hardening/step_a/`, `phase9_hardening/tests/`, `phase3_edge/systemd/`, `scripts/dev_install.sh`, `constraints.txt` |
| 2 | Fehler, Parität, Regel: BG-1, RE-1, RE-2, P10-I, AL-1 | Ausführer (+ Claude Code Proben) | S–M | A | `phase2_mcp/mcpserver/{permissions,app,tools}.py`, `phase5_ui/webui/{api.py,static/js/{list,spaces}.js}`, Tests, `phase10_5_finishing/probes/` |
| 3 | Hygiene: LG-8 (P1-15), LG-7 | Ausführer | S | A | `phase1_storage/storage/{files,store}.py`, `phase1_storage/tests/`, `phase10_5_finishing/scripts/` |
| 4 | Performance: PF-1, PF-4, Z1–Z4 | Ausführer (+ Claude Code Proben) | M | A | `phase5_ui/webui/{api.py,static/**}`, Tests, `phase10_5_finishing/probes/` |
| 5 | MCP-Schicht: PA-5 (FastMCP 4), LG-4 | Ausführer | M | B | `phase2_mcp/`, `constraints.txt`, `phase9_hardening/tests/test_step_h_deps.py`, `phase10_5_finishing/probes/` |
| 6 | Anbieter: PA-1, PA-2, `/mcp`, PA-6, P10-J | Ausführer + Claude Code + Nikinger | M | B | `phase4_auth/authserver/{clients,config}.py`, `phase4_auth/tests/`, `phase2_mcp/mcpserver/app.py`, `phase2_mcp/tests/`, `CLAUDE.md` (eine Zeile) |
| 7 | Darstellung: UI-1–UI-6, KA-5 | Ausführer + Claude Code (Sichtung) | M | C | `phase5_ui/webui/**`, `phase2_mcp/mcpserver/app.py` (eine Route), Tests |
| 8 | Karte: KA-1, KA-2, KA-3 | Ausführer + Claude Code (Smoke/Sichtung) | M–L | C | `phase5_ui/webui/static/{js/graph.js,app.css,app.html}`, `phase8_ui_graph/scripts/p8_22_smoke.py` (nur lesen/ausführen) |
| 9 | Rechte und Namen: RE-7 (P1-12), RE-4 (P1-13), RE-3 (P1-14) | Ausführer | L | D | `phase1_storage/storage/{models,store,index}.py`, `phase2_mcp/mcpserver/tools.py`, `phase5_ui/webui/**`, Tests |
| 10 | Suche und Realtime: LG-1, LG-2 | Ausführer (+ Claude Code Proben) | L | D | `phase5_ui/webui/**` (neu `events.py`, `js/realtime.js`), `phase2_mcp/mcpserver/app.py`, `phase2_mcp/scripts/serve.py`, Tests |
| 11 | Editor: ED-1, ED-2, ED-3 (P1-11), ED-5 | Ausführer (+ Claude Code Proben/Sichtung) | L | D | `phase5_ui/webui/**` (neu `static/vendor/codemirror/`), `phase5_ui/scripts/ui_budget.py`, `phase5_ui/THIRD_PARTY_LICENSES.md`, `phase2_mcp/mcpserver/tools.py` (Beschreibungstexte), Tests |
| 12 | Doku + Altlasten: DO-1, LG-6, AL-1/3, BG-2/3-Nachzug | Claude Code | S | — | nur `.md` und Doku-Skripte |
| Z | Closeout P10.5 (Prompt 3) | Claude Code + Nikinger | S | — | nur `.md`/`.svg` |

**Reihenfolge-Logik:** Das Dringende kommt zuerst (BT-1). Die Performance kommt vor allem Sichtbaren, weil jede spätere Browser-Probe
sonst hinter `/overview` wartet. Die MCP-Schicht liegt unter der Anbieter-Arbeit, damit PA-1 schon auf dem neuen Stack abgenommen wird.
Die drei L-Blöcke kommen zuletzt, und Realtime geht dem Editor voran, weil der Editor dessen „geändert"-Signal braucht.

---

## Block 0 — Haushalt und Vorbereitung (Claude Code)

**Register:** DO-2, DO-3 (+ Step-0-Platzhalter). **Ziel:** Jede spätere Datei findet Platz, die Wächter halten, der Ausführer startet
unter den richtigen Bedingungen. **Erlaubte Pfade:** siehe §3.

**[Nachtrag 2026-10-21] Reihenfolge:** 0.1 → **0.5** (INDEX-Luft, samt der INDEX-Zeile des neuen Archivs) → **0.8** (Register-Luft) → 0.4 →
0.2/0.3 → 0.6 → 0.7. Grund: Nach dem Plan-Commit hat `docs/INDEX.md` nur 188 B Luft, und 0.2 braucht zwei INDEX-Zeilen (~400 B) im
selben Commit (Hard Rule 8). Die Register-Luft muss vor dem ersten Abhaken stehen (§2.2).

**0.1 Verifikations-Durchlauf wiederholen.** `doc_health.py` → 0; Oversize-`find` (Kopf `docs/INDEX.md`); jeder Treffer muss 📕/📦 oder
einer der drei benannten Heads sein. Der Befund von §1.1 gilt, falls sich nichts geändert hat: „nichts zu tun außer INDEX-Luft".

**0.2 Phase-Verzeichnis anlegen.** `phase10_5_finishing/CLAUDE.md` (Head) mit L1-Card (`status: live`, `up: ../ROADMAP.md`,
`down:` Plan, Register, `SESSIONS_ARCHIVE.md`). Inhalt: Auftrag (2 Sätze) · Freigaben (Plan, Tor P10-8, P10-C, P10.5-N mit Datum) ·
**Modulstatus** (eine Zeile je Block 0–12/Z mit Status-Spalte) · **Deploy-Tabelle** A–D (Version, SHA, `health_gate`) · **Abnahme-Zähler**
(P10.5-1–61: ✅/⚠️/⬜) · Offen beim Nikinger · genau **ein** Session-Block. Dazu `phase10_5_finishing/SESSIONS_ARCHIVE.md` (📦, Card)
und `phase10_5_finishing/tests/__init__.py`; `pytest.ini` → `testpaths` um `phase10_5_finishing/tests` ergänzen.

**0.3 DO-3-Wächter.** `phase10_5_finishing/tests/test_head_rules.py`:
`test_the_head_carries_exactly_one_session_block()` und `test_the_session_block_is_at_most_4_kib()` (UTF-8-Bytes vom
`## Session stopped`-Kopf bis zum nächsten `## ` oder EOF, Grenze 4096).

**0.4 DO-2 (a) — ROADMAP-Wächter einfrieren.** `phase9_hardening/tests/test_acceptance_numbers.py:332`: `("| **P9-6**", ROADMAP)` aus der
Live-Schleife nehmen. Ersatz ist eine eingefrorene Assertion: `assert "35.677 B" in _row("| **P9-6**")` mit Docstring-Satz „P9-6 ist
geschlossen; seine Zahl ist eine Momentaufnahme vom 2026-10-07, keine Live-Größe — eingefroren in P10.5 Block 0 (D-17, DO-2)". P9-3 und
V145 bleiben in der Schleife: Sie messen `docs/INDEX.md`, und der Softcap-Test hält die Datei ohnehin unter 40.960 B.

**0.5 DO-2 (b) — INDEX-Luft ≥ 3.000 B.** **[Nachtrag 2026-10-22: gebaut — der Plan-Hebel reichte nicht (2.478 B Überschriften), der Hebel wurde auf Kartenzeilen-Chroniken erweitert, Karte 40.772 → 36.889 B; Details im Kopfnachtrag.]** Die längsten Texte im INDEX sind die Abschnittsköpfe der abgeschlossenen Phasen (P6, P6.5, P7,
P8, P8.5, P8.6, P9; P8.6 allein ~600 B). Neues Skript `phase10_5_finishing/scripts/shorten_index_headings.py`:
- Eingabe ist eine explizite Abbildung `{alte Kopfzeile: neue Kopfzeile}` im Skript, je Kopf ≤ 120 Zeichen, zum Beispiel
  `## Phase 8.6 — ✅ abgeschlossen 2026-09-19 (UI-Politur, live v3.0.2)`.
- Die alten Kopfzeilen wandern **verbatim** in ein neues 📦 `docs/INDEX_HEADINGS_ARCHIVE.md` (L1-Card, ein Abschnitt
  „Abschnittsköpfe vor der Kürzung (Datum), verbatim").
- Vor dem Schreiben laufen vier Gegenproben, sonst bricht das Skript ohne Zielberührung ab: (a) jede alte Zeile kommt im INDEX genau einmal
  vor; (b) Reassemblierung: INDEX-neu, mit alten Zeilen zurückersetzt, ist byte-identisch zum Original; (c) jede alte Zeile steht nach dem
  Schreiben byte-identisch im Archiv; (d) die Ersparnis ist ≥ 3.000 B.
- Danach: INDEX-Zeile für das Archiv, `doc_health` 0, `test_index_archive.py` grün.
- **`[VERIFY]`** zuerst prüfen, ob `test_index_archive.py` Abschnittsköpfe selbst prüft (`test_every_pointer_has_a_section_and_every_section_a_pointer`).
  Trifft das zu, wird die Abbildung so gewählt, dass die Zeiger-Logik unverändert bleibt.

**0.6 ROADMAP-Zeile P10.5** (nach 0.4): Verzeichnis `phase10_5_finishing/`, Status 🔄, Ausführer „M3.1 Flash (Open-Test), Rückfall M3",
Plan-Zeiger. Netto ≤ 300 B. Die `updated:`-Kette läuft per `scripts/prepend_updated_chain.sh` + `scripts/rotate_index_updates.sh ROADMAP.md docs/ROADMAP_UPDATES_ARCHIVE.md`.

**0.7 Ausführer-Vorbedingung dokumentieren.** Das Ergebnis der §2.1-Prüfung (wirksamer `limit.context` für M3.1 Flash und M3) gehört in
den Session-Block, ebenso die Trailer-Zeichenkette aus P10.5-B. Ist der Wert > 400.000 → Block 1 startet nicht; der Nikinger stößt Fleet an.

**0.8 [Nachtrag 2026-10-21] Register-Luft ≥ 3 KB.** `phase10_inventory/BAUSTELLENREGISTER.md` steht nach dem Tor bei 40.954 B (6 B Luft),
und jedes Abhaken nach §2.2 macht eine Zelle länger. Zuerst wird ein 📦 `phase10_inventory/ENTSCHEIDUNGEN_ARCHIVE.md` mit L1-Card angelegt
(das Ziel muss existieren; `scripts/move_sections.py` legt keines an). Dann:
`scripts/move_sections.py phase10_inventory/BAUSTELLENREGISTER.md phase10_inventory/ENTSCHEIDUNGEN_ARCHIVE.md "## 12 Entscheidungsliste (für P10 Step 3)"`.
§12 (3.904 B, alle D-1–D-18 beantwortet, also abgeschlossen) wandert verbatim, die Überschrift bleibt mit Zeiger stehen. Dazu die
INDEX-Zeile für das Archiv und `down:` in der Register-Card um das Archiv ergänzen. Kriterium: Register ≤ 37.900 B.

**Abnahme Block 0**

| # | Kriterium | Probe | Gegenlauf |
|---|---|---|---|
| **P10.5-1** | Step-0-Bericht steht im Session-Block, `doc_health` 0 | Skriptausgabe | — |
| **P10.5-2** | DO-2: INDEX ≥ 3.000 B unter der Grenze; ROADMAP-Wächter eingefroren; **[Nachtrag 2026-10-21]** Register ≥ 3.000 B unter der Grenze (0.8); Suite grün | `wc -c`, `pytest` | eine absichtlich falsche P9-6-Zahl in einer Kopie macht den neuen Test rot |
| **P10.5-3** | DO-3: Wächter grün auf dem echten Head | `pytest phase10_5_finishing/tests` | ein 5-KiB-Block (Fixture) macht ihn rot |
| **P10.5-4** | Ausführer-Vorbedingung erfüllt und protokolliert (≤ 400 K) | Session-Block | ein Wert > 400 K stoppt (dokumentierte Regel) |

---

## Block 1 — Betrieb (Ausführer + Nikinger)

**Register:** BT-1 (dringend), BT-2, BT-6. **Erlaubte Pfade:** siehe §3. **Nichts darf eurofyx-fleet stören:** Die Live-Caddy-Config
gehört Fleet, dieses Repo zieht nur die Vorlage nach (D-10).

**1.1 V199 (Nikinger, unmittelbar vor 1.2).** Auf dem VPS:
`curl -s localhost:2019/config/ | python3 -m json.tool | grep -nE 'dial_timeout|try_duration|try_interval|upstreams|dial' | head -20`.
Die Ausgabe gehört in den Session-Block. Erwartet werden `dial_timeout` 10 s, `try_duration` 15 s, `try_interval` 1 s (JSON in
Nanosekunden: `10000000000`, `15000000000`, `1000000000`). Weicht ein Wert ab, zieht die Vorlage die **Live**-Werte nach, nicht die des
Plans.

**1.2 BT-1 Vorlage.** `phase9_hardening/step_a/Caddyfile.template:65` wird zur Blockform:
```
	reverse_proxy <heimvm-tailnet>:8765 {
		transport http {
			dial_timeout 10s
		}
		lb_try_duration 15s
		lb_try_interval 1s
	}
```
Die Tests in `phase9_hardening/tests/test_tail_proxy.py` bleiben in ihrer Absicht und lernen die Blockform: `:294` und `:325`, Regex
`^\s*reverse_proxy\s+<heimvm-tailnet>:(\d+)(\s*\{)?\s*$`; `:389`, Substitutionsprüfung auf `reverse_proxy 100.93.43.122:8765` als
Präfix der Zeile. Neu: `test_the_upstream_block_carries_the_fleet_timeouts()` (alle drei Direktiven innerhalb des Blocks).
`caddy validate` läuft hier nicht (Caddy ist auf der VM nicht installiert); geprüft wird gegen V199.

**1.3 BT-2 Unit.** `phase3_edge/systemd/sharefyx-tail-proxy.service`, `[Service]`: neue Zeile `SuccessExitStatus=143` direkt unter
`Restart=on-failure`. Test `phase9_hardening/tests/test_tail_proxy.py::test_sigterm_exit_143_counts_as_success()`.
**Installation durch den Nikinger** (Hard Rule 9): Unit-Datei installieren wie in P9 Step A (`[VERIFY]` Befehl in
`phase9_hardening/step_a/RUNBOOK_STEP_A.md` §3), `sudo systemctl daemon-reload`.
**V200 (Nikinger):** `sudo systemctl stop sharefyx-tail-proxy; systemctl show sharefyx-tail-proxy -p Result -p ExecMainStatus; sudo systemctl start sharefyx-tail-proxy`.
Erwartet: `Result=success`, `ExecMainStatus=143`. **Der Domain-Weg ist dabei für Sekunden weg**, das ist vorher anzukündigen.

**1.4 BT-6 → `constraints.txt` (P10.5-Q).**
1. **Lesend** im Live-Release: `/opt/sharefyx/current/.venv/bin/pip freeze --exclude-editable > /tmp/p105_constraints_live.txt`.
2. Daraus wird `constraints.txt` im Repo-Root: Kopfkommentar (Herkunft, Datum, „erzeugt mit pip freeze, nie von Hand editieren"), dann die
   Zeilen sortiert.
3. `scripts/dev_install.sh:12` wird zu `python -m pip install -c "$repo_root/constraints.txt" -e "$pkg_dir[dev]"`. Fehlt die Datei,
   bricht das Skript mit einer Meldung ab: kein stiller Drift.
4. Das Dev-venv wird neu aufgesetzt (`rm -rf .venv && python3 -m venv .venv && bash scripts/dev_install.sh`), danach läuft die volle Suite.
   Sie muss grün sein, jetzt auf den Live-Versionen (`mcp 1.30.0`, `starlette 1.7.0`).
5. Wächter in `phase9_hardening/tests/test_step_h_deps.py`: `test_dev_install_uses_the_constraints_file()` (Textprüfung des Skripts) und
   `test_every_installed_distribution_matches_the_constraints()` (`importlib.metadata.distributions()` gegen die Datei, editierbare
   Projektpakete ausgenommen). Der vorhandene `fastmcp`-Pin-Test bleibt.

**Abnahme Block 1**

| # | Kriterium | Probe | Gegenlauf |
|---|---|---|---|
| **P10.5-5** | BT-1: Vorlage trägt die Live-Werte (V199 ✅) | Testsuite + V199-Ausgabe | die alte Einzeilenform macht `test_the_upstream_block_carries_the_fleet_timeouts` rot |
| **P10.5-6** | BT-2: Unit installiert, `Result=success` bei Exit 143 (V200 ✅) | Nikinger-Ausgabe | ohne die Zeile `Result=exit-code` (Fleet S6, bekannt) — nicht nachgestellt |
| **P10.5-7** | `constraints.txt` = Live-Stand; Dev-venv daraus grün; Wächter grün | `pytest` | in einem Wegwerf-venv mit `starlette` ≠ Constraint wird der Wächter rot |

---

## Block 2 — Fehler, Parität, Regel (Ausführer; Proben Claude Code)

**Register:** BG-1, RE-1, RE-2, RE-5/P10-I, AL-1 (P6-Zeilen 14, 29; 15 → Nikinger). **Erlaubte Pfade:** siehe §3.

**2.1 Eine Regel für Web und MCP — `SharePolicy` erweitern** (`phase2_mcp/mcpserver/permissions.py:39`):
```python
class SharePolicy:
    def __init__(self, acl: AclReader, *, is_home_space: Callable[[str], bool] | None = None) -> None: ...
    def is_team_space(self, space: str) -> bool:          # None-Prädikat → False (fail-closed: keine Team-Rechte)
    def manages_space(self, actor: str, space: str) -> bool:
        # actor == space  ODER  (is_team_space(space) und can_write(actor, space))
    def may_move_between(self, actor: str, source: str, target: str) -> bool:
        # False, wenn target ein fremder Home-Space ist (P10-I);
        # False, wenn source ein fremder Home-Space ist (P10.5-N, freigegeben 2026-10-21)
```
`mcpserver/app.py :: create_app()` baut `SharePolicy(store.acl_reader, is_home_space=lambda s: oauth.store.get_user(s) is not None)`.
`get_user()` nimmt den Weg ohne TOTP-Entschlüsselung (Begründung `api.py:427`). `webui/api.py:422 _is_team_space` und `:434 _team_writer`
werden zu Einzeilern auf `permissions.is_team_space` / `permissions.manages_space`; das hält den Diff klein. P5-B bleibt gewahrt: webui
importiert weiter nur `SharePolicy` (`test_webui_imports_exactly_one_mcpserver_symbol`).

**2.2 RE-1 (Web, Ordner anlegen):** `api.py:458–460`. Statt `space != session.space` gilt `not permissions.manages_space(session.space, space)`,
Meldung „Ordner können nur im eigenen Space oder in einem Team-Space mit Schreibrecht angelegt werden."
**RE-2 (MCP, Ordner wechseln):** `phase2_mcp/mcpserver/tools.py:752`. Statt `acl.space != principal.space` gilt
`not permissions.manages_space(principal.space, acl.space)`.
**P10-I:** `tools.py` direkt nach dem P6-AE-Block (`:732–736`) und `api.py` nach `:970–974`, jeweils für den echten Space-Wechsel:
`if not permissions.may_move_between(actor, acl.space, target): raise …` (MCP: `PermissionDenied(target)`; Web: `ApiError("forbidden",
"Verschieben in den Home-Space eines anderen ist nicht erlaubt.")`).

**2.3 BG-1 (Space-Liste leer):** `phase5_ui/webui/static/js/list.js:191`. Nach `state.spaces = overview;` folgt
`window.dispatchEvent(new CustomEvent("sfx:overview-loaded"));`. In `spaces.js` kommt nach `registerPanel("spaces", prepareSpacesPanel)`
(`:139`) ein Listener: Ist das Spaces-Panel offen, wird `renderSpaceList()` aufgerufen. `[VERIFY]` den Namen der Offen-Abfrage im
Panel-Modul (`registerPanel`/`closeFrom` in `settings.js`); gibt es keinen, wird das `hidden`-Attribut des Panel-Elements geprüft.
**Der Weg über ein Ereignis ist Absicht:** `list.js` darf `spaces.js` nicht importieren, sonst entsteht ein Zyklus (Kommentar `list.js:200`).

**2.4 Tests.** `phase2_mcp/tests/test_permissions.py`: `test_team_space_needs_a_home_space_predicate`,
`test_manages_space_owner_and_team_writer`, `test_foreign_home_space_is_never_a_move_target`, `test_foreign_home_space_is_never_a_move_source`. `phase5_ui/tests/test_api.py`: `test_team_writer_creates_folder_in_team_space`,
`test_folder_create_in_foreign_home_space_is_forbidden_even_with_write`, `test_move_into_foreign_home_space_is_forbidden`.
`phase2_mcp/tests/test_tools.py`: `test_update_item_folder_change_in_team_space_by_team_writer`, `test_update_item_move_into_foreign_home_space_denied`.

**2.5 Proben (Claude Code, Wegwerf, zwei Principale + ein Team-Space):** `phase10_5_finishing/probes/p105_b2_rights_probe.py`.
Matrix Web × MCP: Ordner anlegen und Ordner wechseln (eigener ✅ / Team mit `write:` ✅ / fremder Home mit `write:` ❌) · Verschieben
(Team ✅ / in fremden Home ❌ / aus fremdem Home ❌) · AL-1 Zeile 29 (Move über die MCP-Fläche ✅) · Zeile 14 (geteilter
read-Space: Schreiben ❌). Danach M4 erneut: `phase10_inventory/probes/p10_m4_bg1_probe.py` gegen die neue Wegwerf-Instanz.

**Abnahme Block 2**

| # | Kriterium | Probe | Gegenlauf |
|---|---|---|---|
| **P10.5-8** | BG-1: Die Liste füllt sich, sobald das verzögerte `/overview` ankommt, ohne Panel neu zu öffnen | M4-Probe: Verzögerung 4 s → 2 Zeilen | ohne Verzögerung 2 Zeilen (wie P10) |
| **P10.5-9** | RE-1/RE-2: dieselbe Matrix auf Web und MCP | Probe 2.5 | fremder Home-Space mit `write:` ❌ auf beiden Flächen |
| **P10.5-10** | P10-I auf beiden Flächen durchgesetzt | Probe 2.5 | Team-Space-Ziel bleibt ✅ |
| **P10.5-11** | AL-1: Zeilen 14 und 29 geschlossen; Zeile 15 mit Weg beim Nikinger (Migration + Live-Check) | Probe 2.5 | — |

---

## Block 3 — Hygiene (Ausführer)

**Register:** LG-8 (P1-Öffnung 15), LG-7. **Erlaubte Pfade:** siehe §3. **Ankündigung im Phase-Head vor dem ersten Commit:** „P1-Öffnung 15:
`files.strip_image_metadata()` + Aufruf in `Store.put_asset()`".

**3.1 `phase1_storage/storage/files.py :: strip_image_metadata(data: bytes, mime: str) -> bytes`** (neu, reine Byte-Chirurgie, keine
neue Abhängigkeit):
- **JPEG:** Marker-Folge bis `SOS` durchgehen. **Weg** fallen `APP1` (Exif und XMP), `APP13` (IPTC/Photoshop), `COM`. **Bleiben** `APP0` (JFIF),
  `APP2` (ICC-Profil, Farbtreue) und `APP14` (Adobe, nötig für CMYK). Trug das Original ein Exif-`Orientation` ≠ 1 (Tag `0x0112` in IFD0), wird
  ein **minimales** `APP1` mit nur diesem Tag neu geschrieben, sonst stehen Handyfotos quer. Ab `SOS` wird alles byte-genau kopiert.
- **PNG:** Die Chunks `eXIf`, `tEXt`, `iTXt`, `zTXt` und `tIME` fallen weg, alle anderen bleiben in Reihenfolge.
- **WebP (RIFF):** Die Chunks `EXIF` und `XMP ` fallen weg, die zugehörigen Flag-Bits in `VP8X` werden gelöscht, die RIFF-Größe wird neu gesetzt.
- **GIF:** unverändert (kein Exif; dokumentiert im Docstring).
- **Fail-closed:** Eine Struktur, die der Parser nicht vollständig versteht, ergibt `ValidationError("Bild konnte nicht bereinigt werden")`.
  Hard-Rule-5-Geist: Nie wird ein halbbereinigtes Bild gespeichert.

**3.2 Aufruf** in `Store.put_asset()` (`store.py:929`), direkt nach `sniff_image_mime()` (`:944`) und vor `atomic_write_bytes()`:
`data = files.strip_image_metadata(data, mime)`. `AssetInfo.bytes` zählt die bereinigte Länge. Weil beide Flächen (Web-Upload,
`put_item_asset`) hier durchlaufen, gibt es genau eine Stelle.

**3.3 LG-7 — `phase10_5_finishing/scripts/asset_orphans.py`** (human-only, wie `spacectl.py`). Ein verwaister Asset-Ordner ist
`<space>/_assets/<item_id>/`, zu dem es im Index **keine** Item-Zeile in diesem Space gibt. Typisch ist das ein Item nach `trash()`, siehe den
Docstring `store.py:1042`, „Aufräum-Posten benannt (V162)". Aufruf: `--data-root <pfad>` ist **Pflicht** (kein Default). `--report`
(Default) gibt JSON auf stdout aus (`[{space, item_id, files, bytes}]`, Summe). `--move` verschiebt jeden Ordner mit `files.move_asset_dir()`
nach `DATA_ROOT/._trash/<space>/_assets/<item_id>/` und macht **einen** Commit über `storage.history.commit(data_root, "asset-orphans: N
Ordner", author=<--author>)`. Es wird **nie** gelöscht (LG-5: Der Papierkorb wird nicht geleert). Der Live-Lauf ist Nikinger-Sache: zuerst nur
`--report`.

**3.4 Tests.** `phase1_storage/tests/test_files.py`: `test_strip_jpeg_removes_gps_exif_and_keeps_icc`, `test_strip_jpeg_keeps_orientation_only`,
`test_strip_png_removes_text_chunks`, `test_strip_webp_removes_exif_and_clears_flags`, `test_strip_leaves_clean_image_byte_identical`,
`test_strip_rejects_truncated_jpeg`. Die Fixtures werden im Test **gebaut** (Bytes), keine Binärdateien im Repo. `test_store.py`:
`test_put_asset_stores_the_stripped_bytes`. `phase10_5_finishing/tests/test_asset_orphans.py`: Bericht findet den Trash-Fall, `--move`
verschiebt und committet, lebende Item-Assets bleiben unberührt, fehlendes `--data-root` → Exit ≠ 0.

**Abnahme Block 3**

| # | Kriterium | Probe | Gegenlauf |
|---|---|---|---|
| **P10.5-12** | EXIF weg nach Upload über Web **und** MCP; Orientierung bleibt | Wegwerf: Bild mit GPS hochladen, gespeicherte Datei parsen | ein Bild ohne Metadaten bleibt byte-identisch |
| **P10.5-13** | Verwaiste Asset-Ordner werden gefunden und nur auf Wunsch in den Papierkorb verschoben | Wegwerf: Item mit Bild → `trash` → `--report` findet es → `--move` | Assets lebender Items unberührt |

---

## Block 4 — Performance (Ausführer; Browser-Proben Claude Code)

**Register:** PF-1, PF-4, PF-6 (Budget als Kriterium), D-3 = Z1–Z4. **Erlaubte Pfade:** siehe §3.

**4.1 `_overview` (`phase5_ui/webui/api.py:685`) — ein Durchgang (P10.5-G).**
```python
result = await asyncio.to_thread(store.search, None, limit=_STORE_FETCH_LIMIT, offset=0)
if result.total > len(result.items):        # > 5000 Items: Korrektheit vor Tempo
    logger.warning(...); return await _overview_per_bucket(...)   # der heutige Weg, unverändert als Funktion
by_space = _group_by_space(result.items)    # nur sichtbare Spaces (_visible_space_infos)
counts  = _bucket_counts(by_space[name])    # reine Funktion, dieselben Gleichheitsfilter wie _BUCKETS (api.py:165)
recent  = sorted(by_space[name], key=lambda i: i.updated, reverse=True)[:_RECENT_LIMIT]
```
`_bucket_counts(items) -> dict[str, int]` wendet je Eimer **genau** die Feldgleichheiten aus `_BUCKETS` an (`type`, `status`). Damit bleibt die
Semantik von heute erhalten (`search(...).total`), und auch die Zähler sind weiterhin **nicht** ACL-gefiltert. Das ist kein Fix, es ist Parität.
Jeder Eintrag bekommt zusätzlich `"folders"` und `"members"` aus `SpaceInfo` (gleiche Felder wie `serializers.py:137 space_to_json`).

**4.2 `asyncio.to_thread`** auch für den `store.search()`-Aufruf in `_items_get` (`:838`) und `_graph_get` (`:720`). `Store` ist
threadsicher (`index.py:131 check_same_thread=False`, `store.py:252 RLock`).

**4.3 PF-4 Client.** `list.js:177 loadOverview()` holt nur noch `api("/overview")` (`folders`/`members` stecken jetzt darin), und der Merge
(`:183–190`) fällt weg. `app.js:404 pollCounters()` bekommt eine Mindestpause von 10 s (`lastPollAt`) für die Auslöser `focus` und
`visibilitychange`. Das Intervall bleibt bis Block 10 bei 20 s.

**4.4 Z4/Z3 — Ladezustand.** Neues Modul `phase5_ui/webui/static/js/loading.js`:
`export function withLoading(el, promise, { delayMs = 200 } = {})`. Ist `promise` nach 200 ms noch offen, bekommt `el` die Klasse `is-loading`
(Gerüst/Platzhalter); beim Abschluss wird sie entfernt. Bei < 200 ms gibt es **kein** Flackern. Eingesetzt wird es für Übersicht, Liste,
Item-Öffnen und Karte. `app.css`: `.is-loading`-Gerüst. Bei `prefers-reduced-motion` ist es statisch, ohne Schimmer. **P10.5-S:** Ein
Platzhalter enthält nie eine `version`.

**4.5 Tests.** `phase5_ui/tests/test_overview.py`:
`test_one_pass_counts_equal_per_bucket_search_totals` (Parität über Fixtures: mehrere Spaces, alle fünf Eimer, archiviert, geteilt, leer),
`test_overview_falls_back_beyond_fetch_limit` (Limit per Monkeypatch klein), `test_overview_entries_carry_folders_and_members`,
`test_overview_runs_search_off_the_event_loop` (Monkeypatch `asyncio.to_thread` zählt Aufrufe).

**4.6 Proben (Claude Code).** M2-Bench (`phase10_inventory/probes/p10_overview_bench.py`): Median ≤ 300 ms. Event-Loop-Probe
`phase10_inventory/probes/p10_pf_eventloop_probe.py` gegen eine **neue** Wegwerf-Instanz mit 500 Bulk-Items (`p10_pf_bulk_seed.py`):
`/health` hinter `/overview` ≤ 200 ms. Playwright `phase10_5_finishing/probes/p105_b4_loading_probe.py`: `/overview` per Route um 2 s
verzögern → Space-Wechsel und Item-Öffnen ≤ 1 s (Z2); Endpunkt 150 ms → kein `is-loading`, Endpunkt 400 ms → `is-loading` sichtbar (Z4);
Shell `DOMContentLoaded` ≤ 1 s (Z3).

**Abnahme Block 4**

| # | Kriterium | Probe | Gegenlauf |
|---|---|---|---|
| **P10.5-14** | Z1 im Bench: Median ≤ 300 ms (heute 2.405 ms) | M2-Instrument | — |
| **P10.5-15** | Parität: neue Zähler = alte `search().total` je Eimer | Unit-Test | Fixture mit > Limit nimmt den alten Weg |
| **P10.5-16** | Z2: kein Request wartet hinter `/overview` | Event-Loop-Probe + Playwright | heutiger Code (Vergleichslauf aus P10: 4,3–4,8 s) |
| **P10.5-17** | Z3/Z4: Gerüst ≤ 1 s; Ladezustand genau ab 200 ms | Playwright | 150 ms → kein Platzhalter |
| **P10.5-18** | Live nach Deploy A: `/overview` Waiting ≤ 300 ms, Space-Wechsel während des Polls ≤ 1 s (Nikinger, DevTools, beide Eingänge) | M1-Anordnung | > 300 ms = Messbefund → Nikinger entscheidet über die Index-Zählung (P10.5-G) |

### Deploy A — `v3.1.5` (nach Block 1–4)

§2.5. **Live-Prüfungen (Nikinger):** P10.5-18 · eine Zeile Caddy (V199 bleibt Fleet-Sache) · Upload eines Handyfotos (EXIF weg,
richtig gedreht) · Spaces-Panel direkt nach dem Laden öffnen (BG-1).

---

## Block 5 — MCP-Schicht (Ausführer)

**Register:** PA-5 (FastMCP 4 / MCP 2026-07-28), LG-4, BT-6 (zweiter Teil). **Erlaubte Pfade:** siehe §3.

**5.1 V207 beim Blockstart:** `pip index versions fastmcp` → neueste `4.1.x`; die Changelog-Einträge seit 4.1.2 lesen (GitHub Releases
`PrefectHQ/fastmcp`). Steht dort eine Breaking-Änderung an `http_app`, `Middleware`, `get_http_request`, `ToolError` oder
`utilities.types.Image` → **Rückgabe**.

**5.2 Pin und Abhängigkeiten.**
- `phase2_mcp/pyproject.toml:25`: `fastmcp==4.1.<x>`. Der Kommentarblock darüber bekommt die datierte Ablösung von P9-R:
  „[2026-10-2x, P10.5 Block 5] Obergrenze 3.4.x aufgehoben — FastMCP 4 / MCP 2026-07-28 ist P10.5-P; Trockenlauf 2026-10-20: Suite
  1267/1268 vor Testanpassung".
- **Frisches** Dev-venv, Installation **ohne** Constraints (`pip install -e` je Paket mit dem neuen Pin), volle Suite, dann
  `pip freeze --exclude-editable > constraints.txt` (Kopfkommentar aktualisieren), dann `dev_install.sh` erneut mit Constraints und
  die Suite noch einmal.
- Testanpassungen (camelCase → snake_case): `phase2_mcp/tests/test_app.py:384–387` (`read_only_hint`, `destructive_hint`, `idempotent_hint`,
  `open_world_hint`) und `phase2_mcp/tests/test_tools.py:921` (`content.mime_type`).
- Die Suite läuft zusätzlich einmal mit `FASTMCP_MCP_CAMELCASE_COMPAT=false` und ohne Warnungsfilter: 0 rot, 0 `FastMCPDeprecationWarning`.
- Docstrings, die „verifiziert gegen fastmcp 3.4.4" sagen (`mcpserver/context.py:9`, `request_log.py:33`), bekommen eine datierte Zeile
  „gilt unverändert unter 4.1.x (Suite + Smokes, Block 5)".

**5.3 Protokollversion im Log (für V198/V208).** `mcpserver/request_log.py`: Die Feld-Whitelist `_ALLOWED_FIELDS` (`:62`) bekommt
`"proto"`, und `ToolCallLogMiddleware.on_call_tool` (`:134`) setzt `proto` aus dem Request-Kontext. `[VERIFY V219]` den Zugriffspfad unter 4.1.x, etwa
`context.fastmcp_context.request_context.protocol_version`. Ist kein stabiler Pfad zu finden, entfällt das Feld; dann wird V208 per
Wegwerf-Probe beantwortet, nicht live.

**5.4 LG-4 — neues Werkzeug `append_to_items`** in `phase2_mcp/mcpserver/tools.py`, direkt nach `append_to_item` (`:826`):
```python
class AppendEntry(BaseModel):          # pydantic; extra="forbid"
    item_id: str
    version: int
    text: str

@mcp.tool(title="Text an mehrere Items anhängen", description=..., annotations={readOnly False, destructive False, idempotent False, openWorld False})
def append_to_items(entries: list[AppendEntry]) -> str:
    # 1..20 Einträge, sonst ToolError("validation_failed: 1–20 Einträge")
    # je Eintrag GENAU der Pfad von append_to_item: acl_of → can_write_item(AGENT) → store.append(version, actor)
    # Fehler je Eintrag einfangen (ItemNotFound/ConflictError/ValidationError/PermissionDenied) → Quittung {item_id, ok:false, error:<klasse>, detail}
    # Erfolg → {item_id, ok:true, version:<neu>, appended_bytes}
    # Rückgabe: compact_json({"results": [...], "ok": n_ok, "failed": n_failed})
```
Der Beschreibungstext enthält: je Eintrag die zuletzt gelesene `version`; Teilerfolg möglich; ein Konflikt stoppt die anderen nicht; für
ein einzelnes Item reicht `append_to_item`. Bei Konflikt ist der Weg derselbe wie bei `append_to_item`: neu lesen. `ToolCallLogMiddleware`
loggt den Werkzeugnamen; die Fehlerklasse ist `"partial"`, wenn `failed > 0`.

**5.5 Tests.** `test_tools.py`: `test_append_to_items_appends_each_with_its_own_version`, `test_append_to_items_reports_conflict_and_continues`,
`test_append_to_items_denies_foreign_entry_and_continues`, `test_append_to_items_rejects_empty_and_more_than_20`,
`test_append_to_items_rejects_unknown_entry_fields`. `test_app.py`: Die Werkzeugzahl in `tools/list` steigt um 1 (`[VERIFY]` jeden Test,
der die Zahl festhält). `phase2_mcp/scripts/mcp_smoke.py`: Check 17 `append_to_items` (zwei Einträge, einer mit falscher Version →
`ok:1, failed:1`).

**5.6 Protokoll-Probe ins Repo:** `phase10_5_finishing/probes/p105_b5_protocol_probe.py` (**[Nachtrag 2026-10-21]** Vorlage: `~/.claude-code-tools/p105/proto_probe.py` auf der
Sharefyx-VM, außerhalb des Repos; läuft der Ausführer auf einem anderen Host, wird sie nach der Tabelle in §1.2 neu geschrieben; in-process, beide Ären,
`list_spaces` + `tools/list`-Annotations) mit JSON-Ausgabe; Wächter `phase10_5_finishing/tests/test_protocol_probe.py` ruft sie auf.

**5.7 Vor Deploy B:** Der Nikinger sagt Fabian Bescheid („kurzer Neustart; der Connector sollte ohne neue Anmeldung weiterlaufen"). Die
Token, der Issuer und die Auth-DB bleiben unverändert, also ist kein Re-Auth zu erwarten.

**Abnahme Block 5**

| # | Kriterium | Probe | Gegenlauf |
|---|---|---|---|
| **P10.5-19** | Suite grün mit Compat aus; Pin = installiert; `constraints.txt` neu erzeugt und Wächter grün | `pytest`, Warnungsbilanz | `mcp` ≠ Constraint im Wegwerf-venv → rot |
| **P10.5-20** | Beide Ären in-process: `legacy` → `2025-11-25`, `auto` → `2026-07-28`, `list_spaces` ok | Probe 5.6 | Anfrage mit unbekannter Protokollversion → `UnsupportedProtocolVersion`-Fehler |
| **P10.5-21** | LG-4: Tests + Smoke 17/17 | `pytest`, `mcp_smoke.py` | Konflikt-/Fremdeintrag blockiert die übrigen nicht |
| **P10.5-22** | Live nach Deploy B: claude.ai-Connector `list_spaces`/`search_items`/`get_item`/`update_item` ok (Nikinger); Log-Feld `proto` zeigt die Ära (V208) | Nikinger + Journal (lesend) | — |

---

## Block 6 — Anbieter-Unabhängigkeit (Ausführer + Claude Code + Nikinger)

**Register:** PA-1, PA-2, PA-6, PA-7/P10-J (+ `/mcp` ohne Slash). **P10.5-O freigegeben 2026-10-21.** **Erlaubte Pfade:** siehe §3.

**6.0 V209 vor dem Bauen (Claude Code).** Die aktuelle opencode-Version wird isoliert installiert (npm meldet 1.19.3, gemessen war
1.18.33). Dann läuft `phase10_inventory/probes/p10_m3_dcr_probe.py` erneut und hält den DCR-Request fest: `redirect_uris` (Host
`127.0.0.1` oder `localhost`? Port?) und `application_type`. **Rückgabe-Auslöser:** Nennt der Request `localhost` oder `[::1]`, fällt
P10.5-O so nicht → der Nikinger entscheidet über `localhost` (CSP `http://localhost:*` wäre ausdrückbar).

**6.1 `phase4_auth/authserver/clients.py:18 redirect_uri_allowed()`** — zweite Regel, ein Zweig:
```python
parsed = urlsplit(uri)
if parsed.scheme == "http":
    return (parsed.hostname == "127.0.0.1" and parsed.port is not None and 1 <= parsed.port <= 65535
            and not parsed.username and not parsed.password and not parsed.query and not parsed.fragment)
# https-Zweig unverändert (Allowlist der Origins)
```
Der `[SEAM]`-Docstring wird datiert umgeschrieben („gebaut P10.5 Block 6: exakter Vergleich, nur 127.0.0.1, Port explizit; portagnostisch
bewusst nicht, siehe P10.5-O").
**`register_client()` (`:40`):** Die Pauschalablehnung von `native` (`:52–55`) fällt weg. Neu gilt: `application_type not in (None, "native",
"web")` → `DCRError("invalid_client_metadata")`; `application_type == "web"` und irgendeine Loopback-URI → `DCRError("invalid_redirect_uri")`.
**`flows.py` bleibt unberührt.** Der byte-genaue Abgleich (`:98`) plus `redirect_uri_allowed()` reichen, weil opencode exakt die registrierte
URI sendet.

**6.2 `phase4_auth/authserver/config.py:53 csp_form_action`** → `" ".join(("'self'", *self.allowed_redirect_origins, "http://127.0.0.1:*"))`,
Docstring datiert (P4 Live-Fund 8c: Chromium prüft `form-action` auch gegen das Redirect-Ziel).

**6.3 `/mcp` ohne Slash.** In `phase2_mcp/mcpserver/app.py :: create_app()` kommt **vor** `routes.append(Mount("/mcp", app=bearer))` ein
`Route("/mcp", endpoint=_ExactMount(bearer), methods=["GET", "POST", "DELETE"])`. Es ist eine kleine Klasse (Starlette behandelt nur
Nicht-Funktionen als ASGI-App):
```python
class _ExactMount:
    def __init__(self, app): self._app = app
    async def __call__(self, scope, receive, send):
        scope = dict(scope, path="/", root_path=scope.get("root_path", "") + "/mcp")   # wie Mount es setzt
        await self._app(scope, receive, send)
```
`[VERIFY]` gegen das, was `Mount` in der installierten Starlette-Version in `scope` schreibt (`raw_path` bleibt). Danach ist
`https://sharefyx.eurofyx.com/mcp`, die URL aus P10-C, ohne Umleitung erreichbar. **[Nachtrag 2026-10-21, gemessen]** Die heutige 307
zeigt live auf `https://…/mcp/` (Domain und Funnel, `curl -X POST`); wer ihr folgt, kommt an. Die Route bleibt trotzdem: Ein Client, der
einer 307 bei POST nicht folgt (etwa `httpx` mit dem Default `follow_redirects=False`), scheitert heute, und die Abnahme-URL aus P10-C
steht ohne Slash.

**6.4 PA-6.** Wurzel-`CLAUDE.md` §What this project is: „und deren Claude-Instanzen" → „und deren MCP-Clients (Claude und andere)". Datierte
Notiz, eine Zeile.

**6.5 Tests.** `phase4_auth/tests/test_clients.py`: **`test_register_rejects_native_application_type` (`:63`) wird bewusst ersetzt** durch
`test_register_accepts_native_with_loopback_redirect`, `test_register_accepts_missing_application_type_with_loopback` (opencode-Form aus
M3: `application_type: null`), `test_register_rejects_web_with_loopback`, `test_register_rejects_unknown_application_type`,
`test_loopback_requires_explicit_port`, `test_loopback_rejects_localhost_and_ipv6`, `test_loopback_rejects_query_fragment_userinfo`,
`test_https_rules_unchanged`. `test_redirect_uri_allowed_is_the_only_matching_path` (`:125`) bleibt grün (eine Funktion).
`test_authserver_config.py`: `test_csp_form_action_allows_loopback_port_wildcard`. `test_flows.py`: `test_authorize_accepts_registered_loopback_uri`,
`test_authorize_rejects_unregistered_loopback_port` (der byte-genaue Abgleich hält). `phase2_mcp/tests/test_app.py`:
`test_mcp_without_trailing_slash_is_served_without_redirect`, `test_mcp_without_trailing_slash_requires_bearer` (401 + Challenge).

**6.6 Wegwerf-E2E (Claude Code).** Voller Fluss mit dem echten opencode gegen die Wegwerf-Instanz: Registrierung → `/oauth/authorize`
(Login + TOTP per Playwright) → Code → Token → `list_spaces`. Die Messanordnung kommt aus M3: Bun ehrt im OAuth-Pfad keine
CA-Variablen, also läuft der Fluss über den plain-http-Proxy mit Issuer-Rewrite (`p10_m3_dcr_probe.py`). **V197 (Chromium +
`form-action`):** Der Consent-POST führt per 302 zu `http://127.0.0.1:<port>/…` und kommt beim lokalen Lauscher an. Gegenlauf: Mit
einer Konfiguration ohne den Loopback-Eintrag blockiert Chromium (CSP-Verletzung in der Konsole). Skript:
`phase10_5_finishing/probes/p105_b6_opencode_e2e.py`.

**6.7 Live-Abnahme P10-J (Nikinger, nach Deploy B).**
- **Topologie:** Browser und der Callback-Lauscher von opencode laufen auf **derselben** Maschine. Läuft opencode auf der VM und der
  Browser auf dem MacBook: `ssh -L 19876:127.0.0.1:19876 <vm>` während der Anmeldung.
- Config `[VERIFY V218]`: in `opencode.json` `mcp.sharefyx = {type: "remote", url: "https://sharefyx.eurofyx.com/mcp", oauth: {}}`.
  Dann `opencode mcp auth sharefyx`.
- **Lauf 1:** Modell `MiniMax-M3.1-Flash` → „Rufe list_spaces auf." → Ergebnis mit den eigenen Spaces.
- **Lauf 2 (P10.5-K):** Provider Ollama auf CT 111 (`[VERIFY V214]`: OpenAI-kompatible `baseURL` `http://192.168.68.140:11434/v1`,
  Erreichbarkeit vom opencode-Host, ein Modell mit Tool-Aufrufen — zuerst `qwen2.5vl:7b` (vorhanden) prüfen; sonst wählt der Nikinger ein
  kleines Textmodell und zieht es **auf CT 111**, nie auf der Sharefyx-VM).
- **Beleg:** je Lauf ein Screenshot des Tool-Ergebnisses und eine Journalzeile `tool=list_spaces` mit der `client_id` von opencode.

**Abnahme Block 6**

| # | Kriterium | Probe | Gegenlauf |
|---|---|---|---|
| **P10.5-23** | DCR: `native`/fehlend + `http://127.0.0.1:<port>/…` angenommen; `web` + Loopback, `localhost`, `[::1]`, ohne Port, `http://` fremd → abgelehnt; https-Regeln unverändert | Unit-Tests | claude.ai-Redirect weiter ✅ |
| **P10.5-24** | V197: Chromium folgt dem Consent-Redirect zu 127.0.0.1 | Probe 6.6 | ohne CSP-Eintrag blockiert |
| **P10.5-25** | `/mcp` ohne Slash: 200 mit Bearer, 401 ohne; kein 307 | Unit-Test + `curl` live | `/mcp/` unverändert |
| **P10.5-26** | Wegwerf-E2E: opencode führt `list_spaces` aus | Probe 6.6 | — |
| **P10.5-27** | **Live P10-J Lauf 1** (M3.1 Flash) | Nikinger | — |
| **P10.5-28** | **Live P10-J Lauf 2** (lokales Modell, CT 111) — mit 27 die Abschlussbedingung der Phase | Nikinger | — |

### Deploy B — `v3.1.6` (Minor-Sprung `v3.2.0` nur auf Wort des Nikingers) — nach Block 5–6

§2.5, dazu 5.7 (Fabian). **Live-Prüfungen:** P10.5-22, P10.5-25 (`curl -si -X POST https://sharefyx.eurofyx.com/mcp` → 401 mit
Challenge, nicht 307), P10.5-27/28.

---

## Block 7 — Darstellung (Ausführer; Screenshots Claude Code; Sichtung Nikinger)

**Register:** UI-1, UI-2, UI-3, UI-4, UI-5, UI-6, KA-5. **Erlaubte Pfade:** siehe §3.

**7.1 UI-1 — 404-Seite.** `phase5_ui/webui/pages.py`: `render_not_found_page() -> str` über `_page(title="Nicht gefunden", body=…)` (`:49`),
Text „Diese Seite gibt es nicht." und ein Link „Zur Übersicht" (`/ui/`). Route `Route("/ui/{rest:path}", _ui_not_found, methods=["GET"])`
wird in `create_app()` **nach** allen `/ui`-Routen angehängt (nach `api_routes(...)`), sonst überdeckt der Fänger `account_routes`.
Status 404, `Cache-Control: no-store`. `/ui/static/<fehlt>` bleibt Klartext (`static_routes.py:86`), API und `/mcp` bleiben JSON.
Tests (`test_static_routes.py`): `test_unknown_ui_path_renders_html_404`, `test_known_ui_routes_win_over_the_catch_all` (login, invite,
account), `test_missing_static_file_stays_plain_text`, `test_api_404_stays_json`.

**7.2 UI-2 — Logo (D-6, Variante B „Überlagert").** Das Zeichen kommt aus `docs/concepts/phase10_logo_entwuerfe_final.svg` (Gruppe der
Variante B, **ohne** den Fortsatz der oberen Zelle, der über das Eselsohr ragte) und wird **eine** Datei:
`phase5_ui/webui/static/logo.svg`, der einzige Austauschpunkt. Farben laufen als `currentColor` bzw. über die Tokens
`--select-fill`/`--select-line`, sonst stimmt der Dunkelmodus nicht. Die Marke ist „S"-Zeichen + Wortrest „harefyx": `app.html:20` →
`<div class="rail__brand"><img class="brand__mark" src="/ui/static/logo.svg" alt="S">harefyx<span class="rail__version">…</span></div>`,
`pages.py:42` gleich. Favicon: `<link rel="icon" type="image/svg+xml" href="/ui/static/logo.svg">` in `app.html` und `_page`
(`[VERIFY V215]` Safari). Test: `test_pages_markup.py::test_brand_uses_the_single_logo_file` (beide Stellen zeigen auf dieselbe Datei).

**7.3 UI-3 — Tab-Titel (V120, D-5 deutsch).** `state.js`: `export function setViewTitle(part) { document.title = part ? part + " · sharefyx" : "sharefyx"; }`.
Aufrufe: Übersicht (`editor.js:56 showOverviewPane`) „Übersicht", Space-Liste (Navigation in `list.js`, `[VERIFY]` Funktion) = Space-Name,
Item (`editor.js:466 loadEditorFromItem`) = Titel, Karte (`graph.js:182 loadGraph`) „Karte", Einstellungen (Panel-Öffnen) „Einstellungen".

**7.4 UI-4 — Sichtung, dann Fix (D-17 „nach Sichtung").** Claude Code nimmt nach `docs/concepts/sichtpruefung_automation_conventions.md`
Screenshots der acht Hauptansichten auf. Der Nikinger erstellt daraus eine Liste von **höchstens 10** Posten (Radien, Auswahlzustand,
Abstände). Der Ausführer setzt sie in `app.css` um, mit der Auswahl-Konvention v3 (`phase8_ui_graph/CLAUDE.md`). Was über 10 Posten
hinausgeht, wandert nach P11.

**7.5 UI-5 — Kontrast (D-7).** `app.css`: neues Token `--caution-text` (heller als `--caution`), nur für den Text von
`.btn.action--caution`. Wächter `phase10_5_finishing/tests/test_contrast.py::test_caution_text_meets_wcag_aa()`: liest die Token-Werte aus
`app.css` und rechnet den WCAG-Kontrast gegen den Knopfhintergrund, ≥ 4,5:1.

**7.6 UI-6 — Assignee-Filter.** `api.py:821 _items_get` nimmt `assignee=<space>` an und filtert **im Adapter** (`i.assignee == value`), vor der
Paginierung. `ItemSummary.assignee` existiert (`models.py:90`). In der UI kommt eine Auswahl „Zugewiesen" in die Listenkopfzeile (`list.js`)
mit den Spaces aus `state.spaces` + „alle". Tests: `test_api.py::test_items_filter_by_assignee`, `test_items_assignee_filter_respects_acl`.

**7.7 KA-5 — `doing` hervorheben.** Übersicht: Der Eimer „In Arbeit" bekommt die Akzentklasse (`app.css`). Karte: `doing`-Knoten tragen
einen statischen Akzentring, ohne Animation.

**Abnahme Block 7**

| # | Kriterium | Probe | Gegenlauf |
|---|---|---|---|
| **P10.5-29** | UI-1: HTML-404 für unbekannte `/ui`-Pfade | Unit-Tests | bekannte Routen gewinnen; API bleibt JSON |
| **P10.5-30** | UI-2: Logo an beiden Stellen + Favicon aus einer Datei | Unit-Test + Screenshot | — |
| **P10.5-31** | UI-3: deutscher Titel je Ansicht (V120 ✅) | Playwright liest `document.title` je Ansicht | — |
| **P10.5-32** | UI-4: Sichtungsliste abgearbeitet (Nikinger bestätigt) | Screenshots vorher/nachher | — |
| **P10.5-33** | UI-5: Kontrast ≥ 4,5:1 | Wächtertest | altes Token liefert 4,38 → rot |
| **P10.5-34** | UI-6: Filter in API und UI | Unit-Tests + Playwright | unlesbare Items erscheinen nie |
| **P10.5-35** | KA-5 sichtbar auf Übersicht und Karte | Screenshot, Sichtung | — |

---

## Block 8 — Karte: Gehirnkarte C2 (Ausführer; Smoke und Screenshots Claude Code; Sichtung Nikinger)

**Register:** KA-1, KA-2, KA-3. **Vorlage (Bild):** `docs/concepts/phase10_karte_c_stil_2.svg` (C2 Nervenbahnen). **Datenquelle bleibt
`GET /api/v1/graph`** mit den neun Feldern (P10-D), kein zehntes. **Erlaubte Pfade:** siehe §3. **Budget:** `graph.js` darf um höchstens
+8 KB gz wachsen.

**8.1 Lappen** (`graph.js`, neu `computeLobes()` + `drawLobes()`). Die Pipeline ist die aus M6 (`phase10_inventory/probes/p10_m6_lobe_probe.py:100`,
`LOBE_PIPELINE`), mit zwei Änderungen. **(a)** Die Zuordnung „nächster Knoten" ergibt den **Space des Knotens** als Lappen-ID, und die
Furche liegt dort, wo ein 4-Nachbar einem **anderen Space** gehört. **(b)** Die Körpermaske besteht aus den Zellen innerhalb von
`LOBE_REACH = 48` px um den nächsten Knoten. Zellgröße 8 px. Berechnet wird **einmal** nach dem Einschwingen und nach dem Drag-Ende,
nicht je Frame (M6: 0,2–1,9 ms). Das Ergebnis wird als `Path2D` gecacht. `drawLobes()` läuft vor `drawEdges()` (`:558`): die Kontur je Lappen in der Space-Farbe (`--space-own/-shared/-foreign`),
innen eine leise zweite Linie in einem **dunkleren Ton desselben Tokens**, nicht über Alpha (P8 §0.3 Nr. 6).

**8.2 Bahnen** (`drawEdges`): quadratische Bézier, der Kontrollpunkt liegt senkrecht zur Mitte und wächst mit der Länge; die Breite ist
`1 + log2(1 + min(deg(a), deg(b)))`.

**8.3 Zellen** (`drawNodes`, `:595`): Kreis, Membranring 2 px in der Space-Farbe, 2–4 kurze Fortsätze, deterministisch aus dem Hash der
Item-ID (gleiche Zeichnung bei jedem Laden).

**8.4 Aktivierung.** Neu `neighborRings(id) -> {first: Set, second: Set}` neben `neighborSet` (`:643`). Fokus (Hover/Klick): der Fokus hell
(`--accent`), der erste Ring blau, der zweite Ring halb, der Rest gedimmt. `DIM_ALPHA` (`:115`) wird 0,45 (D-1b: Abdunkeln nur bei Hover
oder Treffer). **Ruhezustand ohne Fokus: alles voll deckend.**

**8.5 KA-2 — Layout merken.** `localStorage`-Schlüssel `sfx:graph:layout:v1:<eigener Space>`, Wert `{"v":1,"pos":{"<id>":[x,y],…}}`,
höchstens 2000 Einträge. Gespeichert wird nach dem Einschwingen und nach dem Drag-Ende (gedrosselt 1 s). `seedInitialPositions()` (`:376`)
nimmt zuerst die gespeicherten Positionen und für den Rest den deterministischen Seed (`seedJitter`, `:403`); unbekannte IDs werden
ignoriert. Knopf „Layout zurücksetzen" löscht den Schlüssel; Statuszeile „Layout gemerkt" (wie in der Vorlage). Kein Serverzustand.

**8.6 KA-3 — Suche, Filter, Titel.** Werkzeugleiste mit Suchfeld (Titel, Teilstring, ohne Groß/Klein) → Treffer hervorgehoben, Rest gedimmt,
Anzeige „N Treffer"; Auswahl Typ (alle/Notiz/Aufgabe) und Status → nicht passende Knoten **und** ihre Bahnen ausgeblendet. Titel: Fokus +
erster Ring immer, sonst weiter ab `ZOOM_LABEL_THRESHOLD` (`:114`).

**8.7 Reduced motion (M6-Nebenbefund).** Im reduced-motion-Pfad wird das erste Bild synchron gezeichnet: 0 rAF-Ticks, statisch.

**8.8 Proben.** `phase8_ui_graph/scripts/p8_22_smoke.py` bei 200 Knoten (Baseline M6: Ruhe 2694,6 ms) → Ruhe ≤ 3000 ms, Frame-Abstand p95
≤ 16,7 ms bei Interaktion. Playwright: Neuladen hält die Positionen (KA-2); Suche/Filter-Zählung (KA-3); reduced motion 0 Ticks.
Screenshots: Ruhe, Fokus mit zwei Ringen, Suche, Filter → Sichtung.

**Abnahme Block 8**

| # | Kriterium | Probe | Gegenlauf |
|---|---|---|---|
| **P10.5-36** | 200 Knoten: Ruhe ≤ 3 s, Frame p95 ≤ 16,7 ms | `p8_22_smoke.py` | Baseline M6 |
| **P10.5-37** | C2-Stil: Lappen, Furchen, Zellen, Aktivierung (Nikinger-Sichtung) | Screenshots | Ruhe voll deckend |
| **P10.5-38** | KA-2: Layout überlebt das Neuladen | Playwright | „Layout zurücksetzen" → deterministischer Seed |
| **P10.5-39** | KA-3: Suche/Filter/Titel | Playwright | Filter blendet Bahnen mit aus |
| **P10.5-40** | reduced motion: statisch, 0 Ticks | Playwright | — |

### Deploy C — `v3.1.7` (nach Block 7–8)

§2.5. **Live-Prüfungen (Nikinger):** Karte mit echten Daten (Sichtung), Logo/Favicon in Firefox und Safari, 404-Seite, Titel.

---

## Block 9 — Rechte und Namen (Ausführer)

**Register:** RE-7 (P1-12), RE-4 (P1-13, V193), RE-3 (P1-14, V194). **Erlaubte Pfade:** siehe §3. **Ankündigung im Phase-Head vor dem ersten
Commit** mit den drei Öffnungen und den betroffenen Dateien `models.py`, `store.py`, `index.py`. Abbruch, wenn
`git diff --stat -- phase1_storage/storage` mehr nennt.

**9.1 RE-7 `created_by`** (wie `updated_by`, P9 Block trace). `models.py`: `Item.created_by: str = ""` (nach `updated_by`, `:51`) und
`ItemSummary.created_by: str = ""` (`:95`). In `store.py` an **zwei** Stellen eintragen: `_KNOWN_FIELDS` (`:54`), sonst landet das Feld
beim Lesen in `Item.extra` (dieselbe Falle, die der Kommentar dort für `updated_by` nennt), und `_SYSTEM_MANAGED_FIELDS` (`:74`).
`Store.create()` (`:616`) setzt `created_by=actor`; **leerer Akteur → das Feld fehlt in der Datei** (P10.5-W, kein erfundenes Leerfeld).
Kein Schreibweg ändert es danach (`update`, `append`, `patch`, `move`, `archive`, `trash`). Frontmatter: `frontmatter.py` ist generisch und
bleibt unberührt. Die Reihenfolge entsteht im Feld-Dict in `store.py` (um `:153`): direkt nach `updated_by`. `[VERIFY]` die Golden-Dateien
`phase6_shares/tests/golden/*.md` entstehen ohne Akteur und dürfen sich nicht ändern. **Kein Index-Schema-Sprung** (wie `updated_by`). Adapter: MCP `get_item_meta`/`item_to_filetext` und
`serializers.py` geben `created_by` aus; die Editor-Metazeile (`editor.js:284 renderUpdatedByLine`) zeigt „erstellt von X" nur, wenn das Feld
gesetzt ist.

**9.2 RE-4 `Store.rename_folder(space: str, old: str, new: str, *, actor: str = "") -> int`.** Ordner stehen **nicht** im Frontmatter (aus
dem Pfad abgeleitet), also wird keine Item-Datei umgeschrieben und keine `version` erhöht. Unter `self._lock` + `_file_write_lock()`: beide
Namen über `files.validate_folder()`; `old` muss existieren, `new` darf nicht existieren; derselbe Space; `new` darf nicht unter `old`
liegen. Dann Rename-Marker schreiben (9.4) → `os.rename(<space>/<old>, <space>/<new>)` (atomar, gleiches Dateisystem) + `fsync` des
Elternverzeichnisses → Index-Zeilen mit `folder == old` oder `folder` beginnend mit `old + "/"` umschreiben (`folder`, `path`) → ein Commit
`rename-folder <space>:<old>→<new>` → Marker löschen. Rückgabe: Zahl der betroffenen Items. Die `.share.yml` im Ordner wandert mit dem
Verzeichnis. `[VERIFY]` dass `AclReader` Ordnerfreigaben über den Pfad findet und sein `stat()`-Cache den neuen Pfad frisch liest.
**Web:** `PATCH /api/v1/spaces/{space}/folders` mit Body `{"from": "…", "to": "…"}` (neben der POST-Route `api.py:1356`), Rechte
`permissions.manages_space(session.space, space)`, Sitzung + CSRF. **UI:** Kontextaktion „Umbenennen" am Ordner im Baum (`tree.js`).

**9.3 RE-3 `Store.rename_space(old: str, new: str, *, actor: str = "") -> int`.** `space` steht **im Frontmatter** jeder Datei (§1.5), also
gilt die Semantik von `move()` (`store.py:831`): Jedes Item des Spaces bekommt `space=new`, `version+1`, `updated=now`, `updated_by=actor`
oder den bisherigen Wert. Das ist der B2-Schutz: Verzeichnis und Frontmatter laufen nie auseinander. Ablauf unter beiden Locks:
`new` validieren (dieselbe Namensregel wie `acl.create_space`, `acl.py:277`), darf nicht existieren; Marker schreiben → `os.rename(DATA_ROOT/old,
DATA_ROOT/new)` → jede Item-Datei unter `new/` (inkl. `_archive/`) mit `space: new` neu schreiben (atomar je Datei, **ohne** Einzel-Commit;
interner Helfer neben `_write_item_file`) → `._trash/old` → `._trash/new`, falls vorhanden (Dateien dort unverändert: Historie) → Index-Zeilen
neu (`space`, `path`, `version`, `updated`, `sha256`, `mtime`, `size`) → **ein** Commit `rename-space <old>→<new>` → Marker löschen.
Fremde `.share.yml`, die `old` nennen (`acl.spaces_referencing`, `acl.py:304`), und Items mit `assignee == old` werden **nicht** angefasst,
sondern in der Antwort gemeldet (wie bei `_spaces_delete`).
**Web:** `PATCH /api/v1/spaces/{space}` mit Body `{"name": "<neu>"}` (`[VERIFY]` dass diese Methode auf der Route frei ist). Erlaubt nur, wenn
`permissions.is_team_space(space)` (P10.5-M), der Akteur den Space verwaltet (`manages_space`), es keinen Nutzer mit dem neuen Namen gibt
(`auth_store.get_user(new) is None`) und der Name frei ist. Schutzstufe wie `_spaces_delete` (`api.py:580`: Sitzung + CSRF), dazu in der UI die
Eingabe des neuen Namens zur Bestätigung.

**9.4 Absturzsicherheit (beide Renames).** Der Marker `DATA_ROOT/.rename-pending.json` (`{"kind", "space", "old", "new", "actor", "started"}`)
wird atomar geschrieben, **bevor** das erste Verzeichnis wandert. `Store.__init__` (`store.py:242`) prüft ihn nach `index.connect` (`:254`):
Ist er da, wird der Rename idempotent zu Ende geführt (Verzeichnis-Rename nur, wenn `old` noch existiert; Frontmatter nur, wo `space` noch
`old` sagt), dann `rebuild_index()` (Hard Rule 2: Der Index ist ableitbar), Commit, Marker löschen. Der Punkt-Präfix hält den Marker aus
beiden Scans heraus (wie `._trash`, P9 Step G).

**9.5 Tests.** `phase1_storage/tests/test_store.py`: `test_created_by_set_on_create_and_never_changed`, `test_created_by_absent_without_actor`,
`test_old_file_without_created_by_reads_as_empty`, `test_rename_folder_moves_nested_and_share_file_keeps_versions`,
`test_rename_folder_index_equals_rebuild`, `test_rename_folder_refuses_existing_target_and_descendant`,
`test_rename_space_rewrites_frontmatter_bumps_versions_one_commit`, `test_rename_space_moves_trash_dir_untouched`,
`test_rename_space_index_equals_rebuild`, `test_rename_resumes_after_crash` (Monkeypatch wirft nach k Dateien → neuer `Store` → Endzustand
konsistent, Marker weg), `test_rename_space_reports_foreign_references_without_touching_them` **[Nachtrag 2026-10-24: liegt in `phase5_ui/tests/test_api.py`, nicht hier — das Melden der Fremdverweise passiert in der Antwort der Web-Fläche (wie `orphan_refs` beim Space-Entfernen), und `acl.spaces_referencing()` ist keine Kern-Aufgabe des Stores]**. Golden-Tests bleiben unverändert grün.
`phase5_ui/tests/test_api.py`: `test_rename_folder_by_owner_and_team_writer` **[Nachtrag 2026-10-24]** *als **zwei** Tests gebaut — `…_by_owner` und `…_in_team_space_is_allowed`; der Gegenlauf zum gesperrten fremden Home-Space braucht getrennte Tests*, `test_rename_folder_in_foreign_home_space_forbidden`,
`test_rename_team_space`, `test_rename_home_space_is_refused` (P10.5-M), `test_rename_space_to_existing_or_user_name_is_refused`.
`phase2_mcp/tests/test_tools.py`: `test_get_item_meta_shows_created_by`.

**Abnahme Block 9**

| # | Kriterium | Probe | Gegenlauf |
|---|---|---|---|
| **P10.5-41** | RE-7: `created_by` auf neuen Items über Web und MCP sichtbar | Tests + Wegwerf | alte Items ohne Feld, nichts erfunden |
| **P10.5-42** | RE-4 atomar (V193 ✅): ein Commit, Versionen unverändert, Freigabe wandert mit | Tests + Wegwerf | Ziel existiert → abgelehnt, nichts bewegt |
| **P10.5-43** | RE-3 nur Team-Space (V194 ✅): Frontmatter = Verzeichnis, ein Commit, Absturz wird wiederaufgenommen | Tests + Wegwerf | Home-Space → abgelehnt |
| **P10.5-44** | P1-Diff nennt nur die angekündigten Dateien | `git diff --stat` | — |

---

## Block 10 — Suche und Realtime (Ausführer; Proben Claude Code)

**Register:** LG-1, LG-2. **Erlaubte Pfade:** siehe §3.

**10.1 LG-1 — Volltext in der Web-UI.** `api.py:821 _items_get`: Parameter `in_body=1` → `store.search(..., in_body=True)` (gibt es seit
P6.5-N4). Die ACL-Filterung danach bleibt unverändert: Gefunden wird nur, was die Sitzung lesen darf. UI: Schalter „Volltext" am Suchfeld
(`list.js`), auch im globalen Suchmodus. Tests: `test_items_query_in_body_only_when_requested`, `test_in_body_search_never_returns_unreadable_items`.

**10.2 LG-2 — Realtime (P10.5-L).** Neues Modul `phase5_ui/webui/events.py`:
```python
def read_git_head(data_root: Path) -> str | None
    # .git/HEAD → "ref: refs/heads/<b>" → .git/refs/heads/<b>, sonst .git/packed-refs; detached HEAD = Hash direkt
    # live: HEAD = "ref: refs/heads/master", refs/heads/master als Datei, keine packed-refs (gelesen 2026-10-20)
def changed_spaces(data_root: Path, old: str, new: str) -> set[str]
    # git -C data_root diff --name-only old new → erste Pfadkomponente; "._trash/<s>/…" → <s>; Dateien in der Wurzel ignorieren
class ChangeFeed:
    def __init__(self, data_root: Path, *, interval_s: float = 1.0, head_reader=read_git_head, differ=changed_spaces) -> None
    async def subscribe(self) -> AsyncIterator[set[str]]   # EIN Poll-Task je App, startet mit dem ersten Abonnenten, endet mit dem letzten
    async def aclose(self) -> None                         # beendet alle Abonnements (Shutdown)
```
Route `GET /api/v1/events` (in `api_routes`): Sitzung ist Pflicht (Cookie, P5-F; GET braucht kein CSRF). Antwort ist eine
`StreamingResponse(media_type="text/event-stream")` mit den Headern `Cache-Control: no-store` und `X-Accel-Buffering: no`. Ereignis:
`event: changed\ndata: {"spaces": [<nur sichtbare>], "head": "<12 Zeichen>"}\n\n`, gefiltert über `_visible_spaces(session.space)`;
**ein unsichtbarer Space-Name verlässt den Server nie**. Alle 25 s ein Herzschlag `: ping\n\n`; bei jedem Herzschlag wird die Sitzung neu
geprüft, und ist sie ungültig, endet der Stream. Höchstens 3 Streams je Sitzung, darüber 429.
**Shutdown:** `create_app()` umhüllt die Lifespan (heute `lifespan=mcp_app.lifespan`, `app.py`): `async with mcp_app.lifespan(app): yield`
und danach `await feed.aclose()`. `phase2_mcp/scripts/serve.py:77`: `uvicorn.run(..., timeout_graceful_shutdown=5)` (`[VERIFY V213]`
Parametername und Verhalten in uvicorn 0.51).

**10.3 Client** `phase5_ui/webui/static/js/realtime.js` (neu): `new EventSource("/api/v1/events")`. Bei `changed`: `List.loadOverview()`;
ist der aktive Listen-Space betroffen → Liste neu laden; Karte über `state.graphToken` (läuft schon über `loadOverview`). **Offenes Item
(P10.5-S):** Ist der Editor nicht geändert, wird das Item frisch geholt und bei neuer `version` neu geladen (Inhalt **und** Version
zusammen). Ist er geändert, erscheint ein Hinweisband „Geändert von <updated_by> — neu laden?"; nie wird überschrieben, und Speichern
führt wie heute in den Konfliktdialog. **Poll:** `app.js:402 COUNTER_POLL_MS` gilt nur noch, solange `EventSource.readyState !== OPEN`, mit
120 s; Fokus/Sichtbarkeit lösen weiter aus (mit der Mindestpause aus 4.3).

**10.4 Tests** `phase5_ui/tests/test_events.py`: `test_read_git_head_ref_file`, `test_read_git_head_packed_refs`, `test_read_git_head_detached`,
`test_changed_spaces_maps_paths_and_trash`, `test_events_filter_invisible_spaces`, `test_events_require_session`,
`test_events_heartbeat_revalidates_and_closes_expired_session`, `test_events_limit_three_streams_per_session`,
`test_feed_starts_and_stops_with_subscribers`, `test_store_write_reaches_subscriber_within_two_intervals` (echtes tmp-Git über `Store(git=True)`),
`test_feed_aclose_ends_streams`.

**10.5 Proben.** In-process/Wegwerf: ein MCP-Write → der Browser (Playwright) zeigt die Änderung in ≤ 2 s; Write in einem unsichtbaren Space
→ kein Ereignis; geänderter Editor bleibt stehen, Band erscheint. **Shutdown:** Wegwerf mit zwei offenen Streams, SIGTERM über die
PID-Datei → Prozess ist in ≤ 10 s beendet.

**Abnahme Block 10**

| # | Kriterium | Probe | Gegenlauf |
|---|---|---|---|
| **P10.5-45** | LG-1: Volltext in der UI | Tests + Playwright | ohne Schalter nur Titel/Tags |
| **P10.5-46** | Realtime: Änderung ≤ 2 s sichtbar | Probe 10.5 | unsichtbarer Space → kein Ereignis |
| **P10.5-47** | P10.5-S: geänderter Editor nie überschrieben; Neuladen trägt frische `version` | Playwright | Speichern mit alter Version → Konfliktdialog |
| **P10.5-48** | Shutdown ≤ 10 s mit offenen Streams | Wegwerf-SIGTERM | heutiger Stand (ohne Frist) wartet |
| **P10.5-49** | Live nach Deploy D: Ereignisse kommen über **beide** Eingänge an (V212 ✅) | Nikinger: zwei Fenster, ein Write | — |

---

## Block 11 — Editor Stufe 1 + 2 (Ausführer; Proben und Screenshots Claude Code; Sichtung Nikinger)

**Register:** ED-1, ED-2, ED-3 (P1-11, nur Konvention), ED-5, PF-6/V201-Rest. **P5-U ist datiert aufgehoben (D-4).** **Erlaubte Pfade:** siehe §3.

**11.1 Vendor.** CodeMirror `5.65.16` (M7; `[VERIFY]` neueste 5.65.x) → `phase5_ui/webui/static/vendor/codemirror/`:
`codemirror.min.js`, `markdown.min.js` (Mode), `codemirror.min.css`. Lizenz (MIT) + Quelle + SHA-256 je Datei in
`phase5_ui/THIRD_PARTY_LICENSES.md`. Es gibt keine neue `.md`; die Datei ist eine Lizenz-Ausnahme. `[VERIFY V211]` CM5 unter der UI-CSP
(`webui/security.py`). Stile, die CM5 per JS als CSSOM setzt, sind erlaubt; geprüft wird im Browser auf CSP-Verletzungen.

**11.2 Nachladen** (`js/editor_cm.js`, neu): `export function ensureCodeMirror(): Promise<object|null>` lädt CSS (`<link>`) und dann
nacheinander beide Skripte (`<script>`, gleiche Origin). Das Promise wird gecacht. Bei einem Fehler wird es mit `null` aufgelöst, und der
Editor bleibt Textarea (= Rohmodus, ED-5).

**11.3 Editor ohne Moduswechsel** (`editor.js`). Alle 14 Zugriffe auf `editorTextareaEl.value` gehen über `getBody()`/`setBody(text)`
(CM vorhanden → `cm.getValue()`/`cm.setValue()`, sonst Textarea): `isDirty`, Entwürfe, `currentFormValues`, `saveItem`, `insertAtCursor`
(`:128` → `cm.replaceSelection`). `setEditorMode` (`:291`) wird `setRawMode(on)`. Der Knopf `togglePreviewButtonEl` heißt „Rohtext". Die
Vorgabe beim Öffnen (`:431`) ist der Live-Modus. Lesesicht fremder Items (`showReadonlyItem`, `:369`) bleibt HTML über `markdown.js`.
`CodeMirror.fromTextArea(editorTextareaEl, {mode: {name: "markdown", highlightFormatting: true}, lineWrapping: true, …})`.

**11.4 Live-Darstellung.** CSS für `.cm-header-1…6`, `.cm-strong`, `.cm-em`, `.cm-link`, `.cm-quote`, `.cm-comment` und `.cm-formatting`
(gedimmt). Bei `cursorActivity` setzt `addLineClass` die Klasse `sfx-active-line` auf die Cursorzeile; Zeichen der Klasse `.cm-formatting`
sind auf allen **anderen** Zeilen ausgeblendet (Obsidian-artig). `[VERIFY V211]`: `display:none` gegen `font-size:0` — der Ausführer prüft
beide, Kriterium ist die korrekte Cursorposition nach Klick (Playwright: Klick auf ein Wort, tippen, Text vergleichen). Rohmodus: alle
Zeichen sichtbar, keine Widgets.

**11.5 ED-2 — To-do-Kästchen.** Im Live-Modus wird `- [ ]`/`- [x]` am Zeilenanfang per `cm.markText(…, {replacedWith: <checkbox>})` ersetzt.
Ein Klick schaltet den Text im Puffer. **War der Editor vorher ungeändert, folgt sofort `saveItem()`** (mit der Snapshot-`version`, Hard
Rule 3; ein Konflikt öffnet den bestehenden Dialog). War er geändert, gehört der Klick zur nächsten Speicherung. Lesesicht
(`markdown.js`): Kästchen werden angezeigt und sind deaktiviert; kein Schreibweg außerhalb des Editors.

**11.6 ED-3 — Stufe 2 (P10.5-I).** Ankündigung im Phase-Head: „P1-Öffnung 11: Format-Konvention, kein Code in `storage/`".
- `markdown.js`: Inline-Regel nach dem Escaping, vor den Links:
  `\[([^\]\n]+)\]\{((?:\.[a-z]+)(?: \.[a-z]+)?)\}` → nur bekannte Klassen (höchstens eine Farbe + eine Größe) →
  `<span class="md-c-rot md-s-gross">…</span>`, sonst wörtlich. Block: Zeile `::: {.zentriert}` → sammeln bis `:::` →
  `<div class="md-a-zentriert">` + rekursiv `markdownToHtml(inner)`; keine Verschachtelung; ein fehlendes Ende → wörtlich.
- Sanitizer (`:224 ALLOWED_TAGS`, `:228 ALLOWED_ATTRS`): `span` und `div` mit `class` nur aus einer festen Menge (Muster
  `ALLOWED_CELL_CLASSES`, `:234`).
- Editor: Werkzeugleiste mit Farbe, Größe und Ausrichtung, die die Syntax einfügen; ein CM5-Overlay (`cm.addOverlay`) färbt `[…]{.rot}`
  schon beim Schreiben.
- MCP: Ein Satz `_FORMAT_HINT` in `tools.py` erweitert die Beschreibungen von `create_item`, `update_item`, `append_to_item`,
  `append_to_items` und `patch_item` (Syntax + Vokabular).
- Doku: Zeile im Öffnungs-Index `phase1_storage/CLAUDE.md` („2026-10-2x, P10.5 Block 11 · Format-Konvention Stufe 2 · kein Code").
- Tests: kein JS-Unit-Rahmen im Repo (P5-T). Geprüft wird mit einer Playwright-Probe, die `markdownToHtml` mit Fixtures im Browser aufruft
  (`phase10_5_finishing/probes/p105_b11_markdown_probe.py`), und Python-Tests für `_FORMAT_HINT` in den Beschreibungen.

**11.7 Budget (P10.5-H).** `phase5_ui/scripts/ui_budget.py:237`: Zeile 3 zählt alle Dateien unter `static/` außer `vendor/`, `app.html`
(kommt in Zeile 4) und Fonts (eigene Zählung). Neue Zeile `Metric("Editor nachgeladen (gzip)", …, 80 * KB, …)` über `static/vendor/**`. Die
Dateiauswahl wandert in eine Funktion `static_payload_files(static_dir) -> tuple[list[Path], list[Path]]` (Erstaufruf, nachgeladen).
Wächter `phase10_5_finishing/tests/test_budget_coverage.py::test_every_static_file_is_counted_exactly_once()`.

**11.8 Roundtrip (V201-Rest).** Die zehn M7-Fixtures (Beschreibung `phase10_inventory/messung/M7_editor.md`) als Items in der Wegwerf-Instanz.
Je Item: öffnen → `isDirty() === false` → speichern ist nicht nötig → Datei byte-identisch; danach ein Zeichen tippen und wieder löschen →
`isDirty() === false`. Offizieller `ui_budget.py`-Lauf gegen den echten Build.

**Abnahme Block 11**

| # | Kriterium | Probe | Gegenlauf |
|---|---|---|---|
| **P10.5-50** | Budget: Erstaufruf ≤ 250 KB, Editor ≤ 80 KB, jede Datei gezählt | `ui_budget.py` + Wächter | Datei unter `vendor/` ohne Zuordnung → rot |
| **P10.5-51** | ED-1: kein Moduswechsel, Live-Darstellung (Nikinger-Sichtung) | Screenshots | CM nicht ladbar → Textarea funktioniert |
| **P10.5-52** | Roundtrip 10/10 byte-identisch, Öffnen macht nie „geändert" | Probe 11.8 | — |
| **P10.5-53** | ED-2: Klick bei sauberem Editor schreibt mit `version`; bei geändertem nur Puffer | Playwright | Konflikt → Dialog, kein Überschreiben |
| **P10.5-54** | ED-3: Vokabular gerendert, unbekannte Klasse wörtlich; `get_item` zeigt Rohtext | Probe 11.6 + MCP | `{.style}` / HTML bleibt wörtlich |
| **P10.5-55** | ED-5: Rohtext-Schalter zeigt jedes Zeichen | Playwright | — |
| **P10.5-56** | P1-11 dokumentiert; `git diff -- phase1_storage/storage` für ED-3 leer | `git diff --stat` | — |

### Deploy D — `v3.1.8` (nach Block 9–11)

§2.5. **Live-Prüfungen (Nikinger):** P10.5-49 (Realtime über Domain **und** Funnel, V212) · Editor mit echtem Item (Sichtung) ·
Kästchen-Klick · Umbenennen eines Test-Team-Spaces (danach zurück) · Neustart-Dauer im Journal (≤ 10 s, lesend).

---

## Block 12 — Doku und Altlasten (Claude Code)

**Register:** DO-1, LG-6, AL-1 (Rest), AL-3, BG-2/BG-3 (Matrix-Nachzug), PA-6 (falls nicht in Block 6). **Nur `.md`.**

- **DO-1:** Die drei Heads (`phase8_6_ui_polish/CLAUDE.md`, `phase8_ui_graph/CLAUDE.md`, `phase6_shares/CLAUDE.md`) werden unter 40 KB
  gebracht, mit `scripts/move_sections.py <quelle> <ziel> "<Überschrift>"` an Abschnittsgrenzen, verbatim, Überschrift mit Zeiger
  bleibt. Ziel ist je Phase ein 📦 `MODULE_STATUS_ARCHIVE.md` (Muster P9) bzw. das vorhandene `SESSIONS_ARCHIVE.md`. INDEX-Zeilen nachziehen.
- **LG-6:** `ROADMAP.md` < 30 KB. Abgeschlossene Abschnitte wandern verbatim (`move_sections.py`) nach `docs/ROADMAP_ARCHIVE.md` (📦, neu).
  Der P9-6-Wächter ist seit Block 0 eingefroren, also sicher.
- **AL-1/AL-3:** P6-Matrix (`phase6_shares/CLAUDE.md`): Zeilen 7, 9, 16, 17, 23, 25, 30 + 14/29 (Block 2) mit Beleg schließen (V205-Liste);
  31–34 auf „in P7 gebaut" nachziehen; 15 mit dem Stand aus Block 2.
- **BG-2/BG-3:** In der P9-Matrix werden P9-124/P9-127 datiert mit den M5-Belegen ergänzt (⚠️ → ✅, Statusregel P8.5).
- **Register:** Jede Zeile mit Ziel P10.5 trägt ✅/⚠️ mit Datum und Block; die Bilanz wird per Skript gezählt (Muster P10-3).

**Abnahme:** **P10.5-57** keine 📗/🔄/🟡-Datei > 40 KB (`doc_health` 0, Oversize-`find`) · **P10.5-58** `ROADMAP.md` < 30 KB, Wächter grün ·
**P10.5-59** Register-Bilanz per Skript, jede P10.5-Zeile mit Beleg.

---

## Block Z — Closeout P10.5 (Claude Code nach Prompt 3; Nikinger)

**Bedingung:** P10.5-27 **und** P10.5-28 ✅ (P10-J), alle Deploys mit echter `health_gate`-Ausgabe.
`docs/concepts/PHASE10_5_CLOSEOUT_HANDOVER.md` (Card, INDEX-Zeile) · `docs/concepts/phase10_5_finishing_uebersicht.svg` (1080 × 1080,
gerendert **und** angesehen) · ROADMAP P10.5 ✅ · Wurzel-„Current state" per `scripts/rotate_root_current_state.sh` · Memory „Phase status".
**Abnahme:** **P10.5-60** P10-J zweimal live belegt · **P10.5-61** Closeout-Dokumente + Rotationen per Skript.

---

## §4 `[VERIFY]` — neu ab V207, dazu die geerbten

| V | Frage | wird geklärt in |
|---|---|---|
| **V207** | Neueste `fastmcp 4.1.x` beim Blockstart; Breaking-Änderungen seit 4.1.2 an den genutzten APIs? | Block 5.1 |
| **V208** | Welche Ära nutzen claude.ai und opencode live nach Deploy B? (löst V198 ab) | Block 5.3 / P10.5-22 |
| **V209** | Welchen DCR-Request schickt die **aktuelle** opencode-Version (Host, Port, `application_type`)? (löst V195 für die Abnahme ab) | Block 6.0 |
| **V210** | Kann eine CSP-Host-Quelle `[::1]` ausdrücken? (Annahme: nein → nur 127.0.0.1) | Block 6 (Spec-Lektüre, kein Bau) |
| **V211** | CM5 unter der UI-CSP; Marker-Ausblendung ohne Cursorfehler | Block 11.1/11.4 |
| **V212** | SSE über Caddy 2.6.2 (VPS) und Tailscale Funnel ohne Pufferung (≤ 2 s) | Block 10 / P10.5-49 |
| **V213** | `uvicorn.run(timeout_graceful_shutdown=…)` in 0.51: Name und Wirkung auf offene Streams | Block 10.2 |
| **V214** | CT 111: Modell mit Tool-Aufrufen, Erreichbarkeit vom opencode-Host | Block 6.7 |
| **V215** | Safari zeigt das SVG-Favicon | Block 7.2 |
| **V216** | Schreibt `test_index_archive.py` die Form der Abschnittsköpfe vor? | Block 0.5 |
| **V217** | Deploy-Aufruf (Umgebungszeilen) gegen die letzte P9-Ausführung | §2.5 D4 |
| **V218** | opencode-Config-Schlüssel für Remote-MCP mit OAuth und für einen Ollama-Provider (Doku der installierten Version) | Block 6.7 |
| **V219** | Zugriff auf die Protokollversion in der FastMCP-4-Middleware | Block 5.3 |

**Geerbt und hier geschlossen:** V197 (Block 6), V199 (Block 1), V200 (Block 1), V201-Rest (Block 11), V193 (Block 9), V194 (Block 9),
V120 (Block 7). **Bleibt draußen:** V203 (eurofyx-fleet), V150 (Termin).

## §5 Abnahme — Zählregel

Statusregel wie P9/P10: ✅ erfüllt mit Beleg am Ort · ⚠️ erfüllt in anderer Form, Abweichung benannt · ⬜ offen. Seit P8.5 zählt vom
Nikinger geprüfte Wegwerf-Automation als live (Memory). Kriterien, die an einer Identität hängen (Fabian, zweites Konto), zählen so
nicht. **61 Zeilen** (P10.5-1–61), gezählt im Phase-Head. Die Phase ist ✅, wenn alle Zeilen ✅/⚠️ sind und P10.5-27/28 ✅.
