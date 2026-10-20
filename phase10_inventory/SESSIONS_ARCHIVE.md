---
status: archive
purpose: L3-Archiv der Session-Blöcke des Phase-10-Heads, verbatim, newest-first — jede Rotation per scripts/rotate_session_block.sh
read-when: nur beim Nachvollziehen der Phasenhistorie; der aktuelle Stand steht im Head
detail: L3
up: ./CLAUDE.md
down: []
updated: 2026-10-20 (siebter Block verbatim rotiert, achter im Head) | 2026-10-20 (sechster Block verbatim rotiert, siebter im Head) | 2026-10-19 (vierter Block verbatim rotiert, fuenfter Block neu im Head: erste Claude-Code+GLM-Session, M8+M7) | 2026-10-19 (dritter Block „GLM 5.3 Flash Step 2" verbatim rotiert — Claude-Code-Auswertungssession) | 2026-10-19 (Block 2026-10-18 zweiter Block verbatim rotiert — GLM/opencode Step-2-Session) | 2026-10-18 (angelegt für die erste Rotation)
---
# Phase 10 — Session-Archiv

## Session stopped — 2026-10-20 (siebter Block: M1 im Browser des Nikingers gemessen, D-3 und D-14 beantwortet, Step 2 ✅)

**Ergebnis:** **Step 2 ist 8 von 8** und **Step 4 (Plan P10.5) hat freie Bahn**. Claude Code, mit dem Nikinger
live im Netzwerk-Tab (Firefox Dev Edition Arbeitsnetz, Safari MacBook mobil; Screenshots, kein HAR). Kein
Produktcode, kein Service-Touch.

**Befund (`messung/M1_browser.md`, drei Reihen):** `/api/v1/overview` kostet **4,8–5,2 s auf allen drei Wegen** (Funnel
Arbeit, Funnel mobil, Domain mobil) — der Eingang ändert den Server-Boden nicht, nur `/ui/` (mobil 0,25 s warm bis
6,3 s kalt). `spaces`, `items` und Item-Anfragen **warten hinter `overview`**: frei 0,2–0,3 s, gestaut 4–14 s; ein
freier Item-Wert 95,8 ms. Der Code passt dazu (`api.py:685 _overview` ist `async def` mit synchronem `store.search()`,
kein `to_thread`) — **als Ursache noch nicht bewiesen**. Der 20-s-Poll belegt rund ein Viertel der Zeit.

**Entschieden (Nikinger):** **D-3** = Z1–Z4 (`/overview` ≤ 300 ms live · kein Request hinter `/overview` · Gerüst ≤ 1 s ·
Ladeanimation-Regel: **> 200 ms bekommt einen Ladezustand, < 200 ms geht sofort durch**) — Wortlaut und Abnahme in
`messung/M1_browser.md` §D-3. **D-14** = `qwen2.5vl:7b`.

**Korrigiert:** meine Vermutung, der zweite `overview` nach dem Laden sei der Fokus-Handler, war für die
Dauerläufe falsch (es war der Poll). **Offen bleibt** ein Mitlauf-`overview` bei jedem Item-Öffnen (4 von 4 im
Arbeitsnetz, 3 von 3 Domain) — Hypothese Fokus-Handler (Rückkehr aus dem Inspektor), ungeprüft.

**Nächste Session — Step 4 (Plan P10.5), Claude Code:**
1. Wurzel-`CLAUDE.md`, diesen Head und diesen Block, dann `messung/M1_browser.md` und Register §12 lesen.
2. **Vorab eine Probe** (Wegwerf-Instanz, eigener Port, tmp-`DATA_ROOT`, Hard Rule 9): (a) zwei parallele Anfragen
   gegen `/overview` beweisen oder widerlegen die Event-Loop-Blockade; (b) Item öffnen mit/ohne Fokuswechsel zählt die
   `overview`-Aufrufe. Ergebnis nach `probes/` und Register PF-1/PF-4.
3. **Plan P10.5 schreiben** nach Plan §7 (unverbindliche Vorschau): Blockschnitt mit D-3 (Z1–Z4) als Abnahmezeilen;
   Ladeanimation als UI-Block (Skeleton, Hard Rule 3 beachten); Anbieter-Unabhängigkeit, Karten-Umbau, Editor Stufe 1+2.
4. **Offen beim Nikinger:** V203 (Fleet), V199 (P10.5 Block 1), Freigabe des Registers (Tor P10-A), Zeitfenster der M1-Reihe 3 (fehlt in `M1_browser.md`); Marktblick ~2026-11-10.
5. **Nicht gefahren, bewusst:** die Wegwerf-Probe (Event-Loop, Mitlauf-`overview`) — Schritt 2 oben. Die Wurzel-`CLAUDE.md` „Current state" nennt noch „Richtung Claude Code + GLM" (seit `c80fdbd` überholt): neuen Block per `scripts/rotate_root_current_state.sh` anlegen, wenn der Nikinger es will.
6. **Regeln:** Register ≤ 40.960 B (steht bei 40.874 B) — neue Zeilen kurz, Belege nach `messung/`; INDEX-Kette nur per `prepend_updated_chain.sh` + `rotate_index_updates.sh`; ein Advisor-Aufruf je Commit.

## Session stopped — 2026-10-19 (sechster Block: Kosten-Analyse der GLM-Session, GLM verworfen, Übergabe an M3/opencode)

**Ergebnis:** **GLM ist als Ausführer gestrichen** (Nikinger-Entscheidung, Review §5; Z.ai-Auto-Verlängerung gekündigt).
Ausführer P10.5 = **MiniMax M3 über opencode**; Neubewertung des Marktes ~**2026-11-10** (M3.1 Flash, DeepSeek-
Flash-Tokenplan u. a. — alles `[VERIFY]`), Messlatte in Review §5 vorab festgeschrieben. Note an Fleet: Intake §8
(Nachtrag „GLM verworfen"). Kein Produktcode, kein Service-Touch.

**Kosten-Analyse (Claude Code, `~/.claude/projects/…/7ad1d9ad….jsonl`):** der fünfte Block lief mit 98 Aufrufen,
Kontext p50 108 K / max 165 K, Summe 10,8 M, 99 % Cache-Treffer; ~45 K Grundlast je Aufruf; ein PNG-`Read`
lieferte 139 K Zeichen Base64. Der Nikinger meldet ~70 % des 5-h-Fensters — **lokal nicht herleitbar** (Prompt-
Abrechnung mit 2–3-fach-Multiplikator ergäbe ~15–22 % einer Lite-Rechnung); maßgeblich ist die Z.ai-Usage-Seite.

**Nächste Session — Ausführer MiniMax M3 in opencode (Übergabe):**
1. **Harness zuerst prüfen**, bevor Arbeit beginnt: in `~/.cache/opencode/models.json` das deklarierte
   `limit.context` des M3-Eintrags lesen. Steht dort ≥ 500 K, die Kompaktierung also praktisch nie greift, **stoppen und
   den Nikinger fragen** (das war der 86-M-Fehler des Open-Tests; Review §1.1). Ziel: Kontext ≤ 200 K, eine Session je Step.
2. **Lesen** (kleine Reads, immer `| cut -c1-200` oder `head -c 4000` — Langzeilen-Falle): Wurzel-`CLAUDE.md`,
   diesen Head, diesen Block, danach `BAUSTELLENREGISTER.md` §12 (D-1–D-18). Kein Ganz-Datei-Read alter Phasen-Skripte.
3. **Was zu tun ist:** Step 2 hängt allein an **M1** (Browser des Nikingers, beide Eingänge, Plan §4) → **D-3** → Step 4
   (Plan P10.5). Liefert der Nikinger die M1-Zahlen im Prompt: D-3 im Register §12 festhalten, Step 2 auf ✅, Head
   nachziehen, `doc_health`. **Ohne M1-Zahlen gibt es keine Pflichtarbeit** — dann nur D-14 (Empfehlung `qwen2.5vl:7b`,
   Messung `probes/p10_m8_vision.json`) beim Nikinger abholen und eintragen. **Step 4 (Plan P10.5) schreibt Claude
   Code**, nicht M3 (Planen = Claude Code, Ausführen = M3).
4. **Regeln:** ein Modell-Trailer je Commit; vor **jedem** Commit Glitch-Scan über Diff **und Betreffzeile**; kein
   `pkill -f`, kein Service-Touch, Tests ohne `SHAREFYX_*`/`SFX_*`-Env; Rotation nur per `scripts/rotate_session_block.sh`.
5. **Offen beim Nikinger bleibt:** M1, D-14, V203 (Fleet), V199 (P10.5 Block 1); Marktblick ~2026-11-10.

## Session stopped — 2026-10-19 (fünfter Block: erste Session unter Claude Code + GLM 5.3 — Harness geprüft, M8 + M7 gefahren)

**Auftrag:** erste Ausführungssession unter Claude Code + GLM 5.3 laut viertem Block: Schritt 0
Harness-Prüfung, dann Register-Rotation → M8 Frage 7 → M7. Budgetregeln eingehalten (kleine Reads,
`grep -n`, `cut -c1-200`, diff-Gegenlesen vor jedem Commit).

**Harness (Schritt 0).** Memory ✅, Endpunkt/Modell-Mapping ✅ (`api.z.ai/api/anthropic`, alle drei
Slots `glm-5.3`), Remote Control ❌ (kein Kanal, nur lokale Peers). **Fehlalarm mit Lehrwert:** im
Session-Env steht `CLAUDE_CODE_AUTO_COMPACT_WINDOW=1000000` — ich stoppte die Arbeitsliste und
meldete (gemäß Regel „zeigt es 1 M, sofort stoppen"); der Nikingers `/context` zeigte dann **200 K**
(`glm-5.3`, „Auto-compact window: 200k"): die Variable wirkt in diesem Build **nicht**, Stopp
aufgehoben, datiert korrigiert in `phase10_executor_review_glm.md` §3.1 + Intake §8-Rückmeldung.
Die „~15 M Tokens übrig"-Anzeige ist Plan-Kontingent, kein Fenster.

**Register-Rotation unterlassen (bewusste Abweichung vom vierten Block, mit Begründung):** die
M2–M6-Nachträge liegen als **Tabellenzellen** in elf lebenden Themenabschnitten — `move_sections.py`
verschiebt nur Überschrifts-Abschnitte, es gibt keinen Hebel. Masse der Zellen ≤ 735 B; Register
39,4 KB < 40,96-KiB-Softcap (1,6 KB Luft); Plan §3 erlaubt Messergebnisse unter `messung/` statt im
Register. Regel dafür: neue Registerzeilen kurz halten, Belege nach `messung/`.

**M8 messfertig.** Frage 7 = die echte Falle vom 2026-10-05, Bild `p9_settings_01_menue_1440.png`.
Bekannte Antwort aus **Code/Messung**, nicht aus dem Bild (dieser Harness lädt `Read` auf PNGs zu
einem CDN hoch statt sie anzuzeigen): genau ein Panel, Titel „Einstellungen", **mittig** (P9-AM,
`app.css` `#settings-menu h2 { text-align: center }`; Bild 04 heißt explizit `drei_panels`).
**Dabei datiert korrigiert:** das „z. B."-Beispiel der Sichtprüfungs-Konventionen („linksbündig —
bekannt: ja") war falsch und hatte die erste Fragefassung korrumpiert — die Korrektur steht am
Zeilenort der Konventionen. Ergebnisse (`probes/p10_m8_vision.json`, je 7 Fragen):
`qwen3-vl:8b` **6/7** — reproduziert die Falle exakt („Drei Panels. Titel: alpha."), damit ist der
Streich von 2026-10-05 an echten Daten bestätigt; `qwen2.5vl:7b` **6/7** — besteht die echte Falle
(vollständig korrekt), fällt synthetisch an `overlapping`; `minicpm-v:8b` **4/7** (erfindet „drei
Fenster" mit frei erfundenen Titeln, +2 weitere Fälle); `llama3.2-vision:11b` **unlauffähig** —
CT-111-ollama 0.34.4 meldet `unknown model architecture: 'mllama'` (Infra-Befund, kein Modellurteil;
Modell danach per `/api/delete` wieder entfernt, CT 111 trägt wieder nur die zwei Qwen-Modelle).
**Empfehlung an D-14: `qwen2.5vl:7b`** — Entscheidung beim Nikinger.

**M7 ✅** — `messung/M7_editor.md` (neu, INDEX-Zeile im selben Commit): **CodeMirror 5.65.16**
63,1 KB gz JS (+2,5 CSS), Roundtrip über 10 Fixtures byte-verlustfrei, 239,0 KB < 250-KB-Korridor
(Ist-Stand der UI nachgemessen: 175,0 KB gz; der dokumentierte 144,7 KB war v3.0.2-Single-File-Ära);
**EasyMDE** Roundtrip ok, aber 282,1 KB — reißt V201; **markdown-it** redundant zum vorhandenen
`js/markdown.js`. bytemd vorab aussortiert (kein UMD-Dist, Peer-Deps). Messung im jsdom-Scratchpad
`~/.claude-code-tools/m7` (nicht im Repo, Kategorie jsdom-Scratchpad seit P5 Step 10; zwei
jsdom-Geometrie-Stubs nötig — Harness-, kein Bibliotheksbefund).

**Verifiziert:** `pytest` **1268** grün, `doc_health` 0, Rotation per Skript (automatische
Gegenproben), kein Service-Touch, kein `pkill`, kein Produktcode; CT 111 nur über die HTTP-API
(pull/generate/delete).

**Eigener Fund (Q4/Q5-Klasse, diesmal ich):** mein erster Commit-Betreff trug „das
links**buergerliche**-Beispiel" statt „linksbündige" — der Glitch-Scan lief nur über den Diff, nicht
den Betreff. Vor dem Push per Amendment korrigiert (`dd5acc1`). Lehre: der Scan gehört **auch** über
die Commit-Betreffzeile. *(Nachtrag zur Rotation: der erste Rotationslauf verschob versehentlich
diesen neuen Block statt des alten ins Archiv — neuer Block gehörte unter den alten gesetzt; über
`git checkout` zurückgesetzt und korrekt wiederholt.)*

**Nächster Schritt:** **M1** (Nikinger-Browser, beide Eingänge) → **D-3** → **Step 4 (Plan P10.5)**;
parallel entscheiden: **D-14** (Empfehlung qwen2.5vl:7b oder CT 111 stilllegen), **V203** (Fleet),
V199 (P10.5 Block 1). Einstieg bleibt dieser Head + dieser Block.

## Session stopped — 2026-10-19 (vierter Block: GLM-Open-Test ausgewertet, unvollendete GLM-5.3-Session geschlossen — Ausführer Claude Code)

**Auftragstellung (Nikinger, Sessionbeginn):** GLM 5.3 Flash „deutlich unterdimensioniert", Kontingent gesprengt; GLM 5.3 (Default) besser, aber unter Haiku-Niveau, musste auf den Vision-Container gestoßen werden; die GLM-5.3-Session endete am 5-h-Limit. Auftrag: herausfinden, was so viel kostet, ob Claude Code + GLM besser passt, und die Qualität ansehen.

**Ergebnis.** Auswertung in **`docs/concepts/phase10_executor_review_glm.md`** (neu, aus `~/.local/share/opencode/opencode.db` read-only): **eine** Flash-Session, 278 Aufrufe, Kontext p50 **326 K**, max **567 K**, Summe **86,1 M** Tokens, **nie kompaktiert** — opencode deklariert `glm-5.3(-flash)` mit 1 M Kontext. Deckel 250 K hätte −28 %, 150 K −54 % gespart. GLM 5.3 war kein Kostenfall (32 Aufrufe, max 129 K), es erbte das von Flash geleerte Fenster. Qualität Q1–Q6 (Review §2): CT 111 trotz Plan + MCP-Konfiguration übersehen, falsche Statusaussage, kaputte Rotation (Flash); Token-Glitches in committetem Text (`ROTETING`, `tirelessly窗外`). Claude Code + GLM: Memory und 200-K-Kompaktierung kämen mit — Vergleichslauf empfohlen, **Entscheidung Nikinger (P10-K)**.

**M8 weitergeführt.** GLM-5.3-Runner `probes/p10_m8_vision_probe.py` committet (Docstring-Glitches korrigiert), Fixture-Frage `color_nuance` von „ROTETING-Punkt" auf „ROTEN Punkt" korrigiert, beide auf CT 111 vorhandenen Modelle neu gefahren → `probes/p10_m8_vision.json`: **`qwen3-vl:8b` 6/6**, **`qwen2.5vl:7b` 5/6** (fällt `overlapping`). Befund: die synthetischen Fixtures reproduzieren den Fehler vom 2026-10-05 **nicht** — M8 ist erst aussagekräftig mit der echten Frage 7 (`docs/screenshots/p9_settings_0*`, Wortlaut der damaligen Frage: `sichtpruefung_automation_conventions.md` Vision-Abschnitt). `minicpm-v:8b`, `llama3.2-vision:11b` nicht gezogen.

**Dauerhaft festgehalten:** CT-111-Adresse `192.168.68.140:11434` im Vision-Abschnitt der Sichtprüfungs-Konventionen (stand nur in einem rotierenden Block).

**Verifiziert:** `pytest` **1268** grün (Umgebung ohne `SHAREFYX_*`/`SFX_*`), `doc_health` 0, beide Rotationen per Skript (alle Gegenproben OK); kein Service-Touch, kein `pkill`, kein Produktcode; Register (39,4 KB) nicht angefasst.

**Nachtrag (Nikinger, Sessionende):** P10-K entschieden in der Richtung „Claude Code + GLM" — die Integration baut **eurofyx-fleet**; Sharefyx hat die Befunde dorthin als Note abgelegt (`docs/concepts/phase10_intake.md` §8).

**Nächster Schritt — erste Session unter Claude Code + GLM 5.3** (Annahme: die Fleet-Integration steht; Einstieg wie immer `docs/INDEX.md` → dieser Head → dieser Block).
0. **Harness prüfen, bevor gearbeitet wird (≤ 5 Aufrufe):** `/status` (welches Modell antwortet wirklich — Server-Mapping kann still tauschen), `/context` (Fenster **200 K** erwartet; zeigt es 1 M, sofort stoppen und dem Nikinger melden — das ist der opencode-Fehler von 2026-10-18), Memory sichtbar (`MEMORY.md` nennt CT 111 und den env-Strip). **Remote Control** einmal versuchen (`/remote-control`); Ergebnis — geht/geht nicht + Fehlermeldung — in `phase10_executor_review_glm.md` §3 nachtragen, `[VERIFY]` dort schließen, Rückmeldung an Fleet über eine Zeile in Intake §8.
1. **Budget-Regeln für die Session:** eine Session je Step; Kontext ≤ 150 K anpeilen; keine Ganz-Datei-Reads alter Phasen-Skripte (Kopf + `grep -n`); jede zeilenbasierte Ausgabe auf Doku mit `| cut -c1-200`; vor jedem Commit den Diff auf Token-Glitches gegenlesen (Review §2 Q4/Q5).
2. **Register rotieren** (39,4 KB) per `scripts/move_sections.py` — M2–M6-Nachträge verbatim nach L3 (`phase10_inventory/messung/`), bevor eine Zeile dazukommt.
3. **M8 Frage 7:** die echte Falle vom 2026-10-05 aus `docs/screenshots/p9_settings_0*` (Wortlaut: Vision-Abschnitt der Sichtprüfungs-Konventionen). Bekannte Antwort **vorher** aus dem Bild selbst festhalten, dann `p10_m8_vision_probe.py` gegen beide Modelle auf CT 111. Danach `minicpm-v:8b`, `llama3.2-vision:11b` sequenziell auf CT 111 (`/api/pull`, `/api/delete` dazwischen) — **nie auf dieser VM**. Ergebnis → D-14.
4. **M7** (Editor-Bibliothek ohne Build-Schritt, ED-1/V201).
5. Beim Nikinger: **M1** → D-3 → **Step 4 (Plan P10.5)**.

## Session stopped — 2026-10-18/-19 (dritter Block: Step 2 auf 6 von 8 Messungen gebracht — Ausführer erstmals GLM 5.3 Flash via opencode, P10-K Open-Test)

**Auftragstellung (Nikinger, Sessionbeginn):** Plan §3 nannte Claude Code als Step-2-Ausführer; der Nikinger entschied in der Session: M2–M8 **hier** fahren. Kein Produktcode (P10-H); Wegwerf-Arbeit auf Port 8799 (`probes/p10_wegwerf.py`, zwei Principals nach Technik 4).

**Ergebnis.** **M2** ✅ — Instrument `probes/p10_overview_bench.py` (+3 Wächter in `phase10_inventory/tests/`, pytest 1265 → **1268**): `/overview` bei 4 Spaces × 50 Items Median **2405,6 / 2438,4 / 2414,3 ms** über drei Instrument-Läufe (±1 %, P10-5 ✅), deckungsgleich mit V151s 2,4 s. **M3** ✅ — opencode-DCR über einen Logging-Proxy festgehalten: `application_type: null` (nicht „native"), Loopback `http://127.0.0.1:19876/mcp/oauth/callback`, Auth-Methode `none` → **4× `400 {"error":"invalid_redirect_uri"}`**. M3b: ein direkt registrierter Loopback-Client scheitert auch an `/oauth/authorize` (`flows.py:98` ruft denselben `[SEAM]`) — das Gate steht zweimal, eine Funktion reicht für P10.5; `initialize` handelte **2025-03-26** aus (SSE, fastmcp 3.4.7; `/mcp/` mit Slash nötig). **M4** ✅ — BG-1 **reproduziert** (verzögertes `/overview` → 0 Zeilen, auch nach Lieferung 0, nach Zu/Auf 2; Gegenlauf 2). **M5** ✅ — BG-2 (Kopie trägt `space=gamma`) und BG-3 (Enter in allen neun erreichbaren Overlays) **gehalten**, 14/14 Checks, je Station Gegenlauf; legacy-host im Wegwerf unerreichbar (https-Pflicht des Legacy-Parsers, benannt). **M6** ✅ — Baseline: sichtbare Ruhe **2694,6 ms** (< 3 s), 153 Ticks, Frame-Abstand p50 16,7 ms, Interaktion p95 ≤ 0,3 ms; die naive Lappen-Pipeline kostet **0,2–1,9 ms** (real 66 Cluster bzw. synthetische 200-Punkt-Obergrenze) — **je Frame im 60-fps-Budget**, KA-1s Größe kommt aus Gestalt, nicht aus der Rechnung. Nebenbefund: reduced-motion zeigt **1 rAF-Tick** statt 0 (Bild statisch; vermutlich initiale Zeichnung über rAF) → P10.5 Block 8. **V204** ✅ (LG-10 gegenstandslos — letzte Griffe an allen P6/P6.5-Glyphen: P8-C2 `0d97b3a`; 0 lebende Treffer). **V205** ✅ (AL-1: 7 Zeilen mit P7–P9-Belegen schließbar, 3 offen mit Weg: 14 geteilte-Space-Hälfte, 15 Migration, 29 Connector-Move).

**Offen geblieben.** M1 (Browser des Nikingers) → danach D-3 → Step 4. **M7** ungefahren. **M8** halb vorbereitet: 6 Fixtures mit bekannter Antwort unter `probes/fixtures/` (+ `questions.json`), ollama-Daemon als Nutzerprozess, die vier Modell-Pulls laufen **abgesetzt** weiter (Log `/tmp/opencode/m8_pulls.log`; Ziel: qwen3-vl:8b, qwen2.5vl:7b, minicpm-v:8b, llama3.2-vision:11b — **CPU-only, diese VM hat kein nvidia-smi**). V203: Fleet-Repo liegt hier nicht; V199: Exec-Session. **[2026-10-19 Korrektur, GLM 5.3 — nachgetragen beim Aufräumen des Working Tree:]** die Pulls liefen beim Schreiben bereits nicht mehr (Log endet 07:08, kein Prozess) — sie starben mit der Session, und sie liefen außerdem **auf der falschen Kiste**: Vision-Inferenz gehört auf **CT 111** (`192.168.68.140:11434`, RTX 3060, einziger 11434-Listener laut P9-22-Beweis; P9-C8), nicht auf diese VM (5,8 GiB RAM, keine GPU). `qwen3-vl:8b` steht dort schon (6,1 GB, Q4_K_M, probehalber verifiziert). Die USER-seitigen Partial-Blobs (2,7 GB, redundanter Ziehversuch desselben Modells) sind gelöscht; die **systemweiten** ~8 GB (Binary + Modell, kalter Fallback aus Step C „bis Step Z" — Step Z ist seit 2026-10-08 durch) bleiben unangetastet — Entfernen ist Nikinger-Entscheidung (sudo). M8 läuft gegen CT 111; die Pulls der drei Mitbewerber gehen dorthin, sequenziell mit `rm` zwischendurch.

**Eigene Fehler dieser Session (alle vor dem Commit gefangen, außen dokumentiert):** asyncio-Proxy fraß sich an `read(n)` fest, kein Keep-Alive-/Chunked-Handling, Header-Rewrite ersetzte nur den Body; Seed nannte das falsche Konflikt-Item; Rotations-Skript per python statt bash gerufen. Zwei Betriebsbefunde der Messung selbst im Register PA-7: Bun/opencode ehrt keine CA-Env-Variable im OAuth-Pfad (Messung lief deshalb über plain-http-Proxy mit Issuer-Rewrite — Messinstrument, Serververhalten unverändert).

**Verifiziert:** `pytest` **1268** (nach M2; seither nur Probe-Skripte/Doku), `doc_health` 0, Tabu-Diff P10-11 leer, beide Wegwerf-Instanzen per PID-Datei gestoppt, kein `pkill -f`, kein `systemctl`. Ausführer-Tag: **GLM 5.3 Flash / opencode** (P10-K Open-Test) — Rückfallebene M3 bleibt bis 2026-11-15.

**Nächster Schritt.** M8-Runner schreiben und die vier Modelle gegen die Fixtures fahren, dann M7; parallel M1 beim Nikinger → D-3 → **Step 4 (Plan P10.5)**.

## Session stopped — 2026-10-18 (zweiter Block: alle Entscheidungen D-1–D-18 eingeholt und eingearbeitet; kein Produktcode)

**Ergebnis.** Der Nikinger hat in fünf Fragerunden alle offenen Entscheidungen beantwortet; sie stehen je Zeile im Register §12 und
haben die Ziel-Spalte gesetzt: **P10.5 39** · P10 9 · P11 4 · verworfen 6 · Wissen 6 · Termin 3 · erledigt 3 · an Fleet 2 · 4 ohne Bau
(per Skript gezählt). Zwei neue Locks im Plan §0.2: **P10-I** (niemand verschiebt in den Home-Space eines anderen — destruktiv wie
Löschen) und **P10-J** (Abnahme Anbieter-Ziel: opencode mit M3 **und** mit einem zweiten Modellanbieter). Neue Messung **M8**
(4 Vision-Modelle × 5 gemeine Screenshots, D-14). V206 beantwortet: O7 = P6-Zeile 30, seit P6-AF gebaut.

**Befund für P10.5.** Der Umfang ist deutlich gewachsen: FastMCP 4 / MCP 2026-07-28, Realtime, Bulk-Append-Werkzeug, Space
umbenennen, Editor Stufe 1 + 2 (P5-U aufgehoben) und `created_by` — zwei P1-Öffnungen (elfte, zwölfte). Plan §7 schneidet daraus
zwölf Blöcke; fünf davon sind „L" und brauchen je einen Mini-Plan.

**Nachtrag 2026-10-18 (Sessionende).** Logo D-6 in vier Runden entschieden: **Leuchtbahn, Variante B** (Eselsohr überlagert,
ohne den Fortsatz, der hinausragte) — `docs/concepts/phase10_logo_entwuerfe_final.svg`. Ausführer P10.5 geändert: **Open-Test
GLM 5.3 Flash** (Lock P10-K, ersetzt P10-E; M3-Rückfall bis 2026-11-15). **Die Integration von z.ai/GLM in opencode läuft über
`eurofyx-fleet`, getrennt von diesem Plan** — Sharefyx setzt nur voraus, dass opencode den Ausführer stellt.

**Nächster Schritt.** Step 2: M2–M8 in Claude Code gegen die Wegwerf-Instanz, M1 im Browser
des Nikingers. Dann Step 4 (Plan P10.5).

## Session stopped — 2026-10-16 (erster Block: Phase 10 begonnen — Register-Entwurf, Plan, Karten-Entwürfe; kein Produktcode)

**Ergebnis.** Vier Grundsatzantworten des Nikingers vorab eingeholt: Zweiteilung P10/P10.5 bestätigt (Register zuerst, P10.5-Plan
danach), Anbieter-Unabhängigkeit auf Server-/Connector-Ebene, Karten-Umbau mit Stil + Layout merken + Interaktion („gehirnartiger"),
Ausführer M3 Thinking. Geschrieben: das Register (76 Zeilen, jede mit Anker am Code), der P10-Plan, sechs Karten-SVGs (erste Runde A/B/C →
**C gewählt**, zweite Runde C1–C3). Der „verlorene" Planungsprompt ist `docs/PROMPTS.md` Prompt 2 (Commit `0a7aaf4`, mit den drei
Fleet-Notizen aus intake §5–§7).

**Funde (alle im Register).** Die Caddy-Quelle `Caddyfile.template:65` hinkt dem Live-Fix nach (BT-1, dringend). Sieben Ledger-Posten
fielen beim Übergang P8.6 → P9 ohne Schließvermerk aus der Kette (AL-1, AL-4, LG-7–LG-10, BT-10). Der Editor-Wunsch widerspricht dem
gelockten P5-U (ED-1). MCP 2026-07-28 ist die aktuelle Spec-Version (nicht mehr RC wie in P8 §0.5 notiert) und führt DCR als *deprecated*; Sharefyx lehnt native Clients mit
Loopback-Redirect ab (PA-1). Root-`CLAUDE.md` nannte im `down:` noch P8.6 als aktive Phase — korrigiert. Ein P9-Wächter koppelt die geschlossene Zeile P9-6 an die lebende ROADMAP-Größe und lief im Commit rot: eigene ROADMAP-Zeilen gekürzt statt P9-Testcode anzufassen (DO-2).

**Belege.** `doc_health` 0 Befunde; `test_index_archive` + `test_updated_chain` + `test_doc_health` grün (Commit-Ausgabe); kein
Produktcode-Diff (P10-11). Karten-SVGs mit headless Chromium gerendert und angesehen; Vorschau-Seite (privat):
`https://claude.ai/artifact/Grr7UELUVeh5BecbU239cQ`.

**Nachtrag 2026-10-16 — Plan finalisiert** (Auftrag „only finalize the plan", kein Step 2 in dieser Session). Antworten des
Nikingers: D-1b = **C2 Nervenbahnen**; M1 wie vorgeschlagen; V199 erst in der Exec-Session; BT-13 beantwortet (ja, versehentlich — die
Repo-Auswahl in opencode laggt, Klicks landen daneben); Push freigegeben.

**Nächster Schritt.** Step 2 und 3 parallel: M2–M7 baut und fährt Claude Code (Wegwerf-Instanz, Port 8799); der Nikinger misst M1
nach Plan §4. V199 wandert in die Exec-Session (P10.5 Block 1). Danach Step 4 (Plan P10.5).

