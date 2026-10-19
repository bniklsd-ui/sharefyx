---
status: live
purpose: Auswertung des P10-K-Open-Tests (GLM 5.3 Flash + GLM 5.3 via opencode, 2026-10-18/-19) — wohin das Kontingent ging, wie gut die Arbeit war, ob Claude Code + GLM besser passt
read-when: vor jeder Entscheidung zum Ausführer von P10.5 (Lock P10-K) und bevor eine opencode-/GLM-Session gestartet wird
detail: L2
up: ../INDEX.md
down:
  - ../../phase10_inventory/CLAUDE.md   # Phase-Head, Session-Block mit dem Kontext
updated: 2026-10-19 (angelegt — Claude Code, Auswertung aus `~/.local/share/opencode/opencode.db`, read-only)
---
# P10-K Open-Test — Auswertung GLM/opencode (2026-10-19)

> **Ergebnis zuerst.** Das 5-h-Kontingent fraß **eine** opencode-Session, die 12 h ohne Kompaktierung lief:
> 278 Modellaufrufe, Kontext im Median **326 K** Tokens je Aufruf, Spitze **567 K**, Summe **86,1 M**
> verarbeitete Tokens. Die Ursache ist ein Konfigurationsdetail, nicht das Modell: opencode deklariert
> `glm-5.3-flash` mit **1 M Kontext** und kompaktiert erst kurz davor — also nie. GLM 5.3 (Default) war
> **kein** Kostenfall: 32 Aufrufe, Spitze 129 K; es lief in ein Fenster, das Flash schon geleert hatte.
> Die Lock-Entscheidung P10-K bleibt beim Nikinger — dieses Dokument liefert Befund und Empfehlung.

Quelle aller Zahlen: `~/.local/share/opencode/opencode.db` (2,9 GB, read-only geöffnet), Tabellen `session`,
`message` (`tokens.input`, `tokens.cache.read`), `part` (Tool-Aufrufe und -Ausgaben). Sessions: `…jj3E4bf5`
(Flash, 2026-10-18 19:49 – 10-19 07:21) und `…RSwYPRLr` (GLM 5.3, 10-19 07:26 – 07:56, endet mit
`429 Usage limit reached for 5 hour`).

## 1. Wohin das Kontingent ging

| Größe | Flash `jj3E4bf5` | GLM 5.3 `RSwYPRLr` |
|---|---|---|
| Modellaufrufe | 278 | 32 |
| Kontext je Aufruf p10 / p50 / p90 / max | 126 K / 326 K / 456 K / 567 K | 65 K / 102 K / 125 K / 129 K |
| Summe verarbeiteter Kontext | 86,1 M (davon 83,2 M Cache-Treffer) | 3,2 M |
| Kompaktierung (`time_compacting`) | **nie** | nie (nicht nötig) |
| Nutzer-Prompts | 3 | 2 |
| Tool-Aufrufe (bash/edit/read/grep/write) | 169 / 55 / 37 / 13 / 10 | 44 / 4 / 4 / 0 / 1 |

**Das Fenster, das am 429 starb** (ab 06:00 lokal): 150 Aufrufe, **51,1 M** Kontext-Tokens — davon ~118 Aufrufe
Flash bei 350–466 K je Aufruf, 32 Aufrufe GLM 5.3. Flash allein hat das Fenster geleert.

**Abrechnung (Inferenz, nicht bestätigt):** Z.ai rechnet laut DevPack-Doku in „Prompts" und schätzt
**15–20 Modellaufrufe je Prompt**; für GLM-5.x gelten Token-Multiplikatoren je Modell. Flash machte ~93 Aufrufe
je Nutzer-Prompt bei ~310 K Kontext — das Kontingent verhält sich also wie aufruf- bzw. token-getrieben, nicht wie
„Nachrichten des Nikingers". Quelle: docs.z.ai/devpack/overview, docs.z.ai/devpack/teamplan. Die echte Zahl steht
auf der Usage-Seite im Z.ai-Konto.

### 1.1 Die vier Treiber, nach Gewicht

1. **Keine Kompaktierung — Konfiguration.** `~/.cache/opencode/models.json` deklariert `glm-5.3`, `glm-5.3-flash`
   und `glm-5.3-highspeed` je mit `limit.context: 1000000`. opencode kompaktiert erst bei „Limit minus Puffer"
   — bei 567 K Spitze nie erreicht. **Gegenrechnung:** mit Deckel 250 K wären es **62,1 M** statt 86,1 M (−28 %),
   mit 150 K **39,7 M** (−54 %). Die Bitte des Nikingers „unter 250 K halten" kam bei ~450 K und änderte am
   Verhalten nichts — Flash setzte die Session fort statt sie zu schneiden.
2. **Ganz-Datei-Reads alter Phasen-Skripte als Vorlage.** 641 K Zeichen Read-Ausgabe; die größten:
   `phase8_6_ui_polish/scripts/p86_block_h_r_part2_self_check.py` **115.820** Zeichen,
   `phase8_ui_graph/scripts/p8_22_smoke.py` 71.648, `phase8_5_picker_release/scripts/wegwerf_setup_v3ritt.py`
   52.882. Jedes davon fuhr danach in **jedem** folgenden Aufruf mit.
3. **Die Langzeilen-Falle dieses Repos.** `git diff CLAUDE.md | head -60` lieferte **41.457** Zeichen,
   `sed -n '176,200p' CLAUDE.md` 20.281 — die Doku hat Absätze als Einzelzeilen, `head`/`sed` nach Zeilen
   begrenzen hier **keine Bytes**. Gilt für jeden Ausführer, Claude Code eingeschlossen: `| cut -c1-200` oder
   `head -c 4000` anhängen.
4. **Eine Session für fünf Messungen.** M2–M6 liefen hintereinander in einer Session; jede Messung erbte den
   Kontext aller vorigen. Ein Commit je Messung war da — eine neue Session je Messung nicht.

### 1.2 Hebel in opencode (`[VERIFY]` gegen die installierte Version)

- Pro Modell die Kontextgrenze **künstlich senken**, damit die Auto-Kompaktierung früh greift — derselbe
  Mechanismus, den `~/.config/opencode/opencode.json` für MiniMax schon nutzt:
  `provider."zai-coding-plan".models."glm-5.3-flash".limit.context = 200000` (Schlüsselpfad `[VERIFY]` gegen
  `opencode.ai/config.json`).
- `compaction`-Block (`auto`, `prune`, Puffer) laut v2-Doku — Feldnamen unterscheiden sich zwischen den
  Doku-Versionen (`reserved` vs. `buffer`), deshalb `[VERIFY]`.
- Arbeitsregel unabhängig vom Werkzeug: **eine Session je Messung/Step**, Übergabe über den Session-Block.

## 2. Qualität

| # | Befund | Wer | Folge |
|---|---|---|---|
| Q1 | Vision-Container übersehen, obwohl er im Kontext stand: Flash las Plan §4 M8 („RTX 3060", „CT 111"), hatte das MCP-Werkzeug `local_vision` mit `LOCAL_VISION_ENDPOINT=http://192.168.68.140:11434` (`~/.config/opencode/opencode.jsonc:30`) — und schloss im Reasoning „GPU-Annahme hält von dieser VM aus nicht, M8 läuft CPU-only", statt den Widerspruch aufzulösen. Startete ollama lokal und vier Pulls auf der 5,8-GiB-VM. | Flash | falsche Kiste, 2,7 GB Partial-Blobs, Nikinger musste eingreifen |
| Q2 | Falsche Statusaussage im Session-Block: „Pulls laufen abgesetzt weiter" — sie waren beim Schreiben schon tot (Log endet 07:08). | Flash | von GLM 5.3 gefunden und datiert korrigiert |
| Q3 | Rotation beim Sessionende kaputt: Wurzel-`updated:`-Kette aus altem Puffer überschrieben; erst ein falscher Marker-Treffer, dann eine Extraktion, die das ganze Archiv mitnahm. | Flash | von GLM 5.3 aus der `.bak` bewiesen und repariert (`727c02b`) |
| Q4 | Token-Glitches in committetem Text: Fixture-Frage „trägt den **ROTETING**-Punkt?" (`p10_m8_fixtures.py:77`, `questions.json:22`) — die M8-Messung `color_nuance` lief mit einer kaputten Frage; Commit-Betreff „festgeha**I**ten". | Flash | Frage 2026-10-19 auf „ROTEN Punkt" korrigiert, `color_nuance` neu gefahren |
| Q5 | Sprachmischung im Docstring des M8-Runners: „oder tirelessly窗外 erfindet", „qwen3-vl denket sichtbar". | GLM 5.3 | korrigiert; der Runner selbst funktioniert |
| Q6 | M8-Fixtures diskriminieren nicht: `qwen3-vl:8b` besteht **6/6**, inkl. `empty_area` — der Falle, an der es am 2026-10-05 an echten Daten scheiterte. GLM 5.3 hat das **selbst erkannt** und die echte `p9_settings`-Frage als siebte begonnen. | GLM 5.3 (gut) | M8 bleibt offen, s. Phase-Head |

**Was gut war.** Flash lieferte M2–M6 mit Instrument, Gegenläufen und Wächtern (pytest 1265 → 1268), hielt
Hard Rule 9 (PID-Datei, kein `pkill -f`) und strippte `SHAREFYX_*`/`SFX_*` — weil Plan §4 die Memory-Regel
zitiert. GLM 5.3 prüfte die halbfertige Flash-Rotation byteweise, statt sie zu glauben, fand CT 111 selbst
(aus P9-Belegen, Adresse per Probe bestätigt) und blieb bei 129 K Kontext.

**Einordnung.** Flash ist für mehrstündige, mehrstufige Arbeit in diesem Repo zu schwach: Q1–Q4 sind Fehler
im Zusammenhang-Halten über lange Kontexte, nicht im Einzelschritt. GLM 5.3 arbeitet sauberer, hat aber dieselbe
Glitch-Klasse (Q5) — jeder committete Text braucht eine Gegenlese.

## 3. Claude Code + GLM statt opencode + GLM?

Z.ai bietet einen Anthropic-kompatiblen Endpunkt für Claude Code (`ANTHROPIC_BASE_URL=https://api.z.ai/api/anthropic`
plus Auth-Token, Modell-Slots auf GLM gemappt; Quelle docs.z.ai/devpack/tool/claude — exakte Variablen und
Modellnamen `[VERIFY]` auf der Seite, nicht aus Drittquellen).

| Punkt | opencode + GLM (heute) | Claude Code + GLM |
|---|---|---|
| Kompaktierung | greift bei deklarierten 1 M praktisch nie | Claude Code budgetiert unbekannte Modelle hinter fremder `ANTHROPIC_BASE_URL` mit **200 K** und kompaktiert dort — genau der gewünschte Deckel (Berichte aus Issues, `[VERIFY]` per `/context`) |
| Memory (`~/.claude/projects/…/memory/`) | **unsichtbar** — 0 Treffer für `MEMORY.md`/`52×` in beiden Sessions; Flash kannte die env-Regel nur, weil Plan §4 sie zitiert | lädt `MEMORY.md` automatisch (Live-VM, keine schweren Proben, env-Strip, Keyring) |
| `CLAUDE.md`-Hierarchie, Skills, Hooks | Wurzel-`CLAUDE.md` als Fallback | nativ, inkl. Phasen-Heads beim Betreten |
| Werkzeug-Grenzen | `read` voll, bash ungedeckelt | `Read` mit Zeilenlimit; bash-Ausgabe gedeckelt — die Langzeilen-Falle bleibt trotzdem |
| Risiko | bekannt | Tool-Use-Treue von GLM im Claude-Code-Format ungemessen; Server-seitiges Modell-Mapping kann still ein anderes Modell liefern |

**Empfehlung (Nikinger-Entscheidung, P10-K ist gelockt):** einen **kurzen**, gedeckelten Vergleichslauf mit
Claude Code + GLM 5.3 auf einer abgeschlossenen Aufgabe (Vorschlag: M8 Frage 7) — erst nach Reset des
Fensters, eine Session, Ziel ≤ 150 K. Flash nicht weiter als Ausführer; falls opencode bleibt: Kontextgrenze
je Modell auf 200 K senken und eine Session je Step.

## 4. Was dauerhaft festgehalten werden musste

Die CT-111-Adresse stand nur in einem Session-Block, der rotiert, und in einer opencode-Konfiguration. Ab
2026-10-19 steht sie hier und in `sichtpruefung_automation_conventions.md` (Abschnitt lokales Vision-Modell):
**Vision-Inferenz läuft auf CT 111, `http://192.168.68.140:11434` (RTX 3060), nie auf der sharefyx-VM.**
