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
updated: 2026-09-10 (Step V deferred — Nikinger-Entscheidung: **lokales Vision-Modell** auf Proxmox-Migration (i5-14600KF primär, danach Ryzen 7 5800X) statt Anthropic-Haiku-API. Backend **`InternVL 2.5 8B`** (Apache-2.0, Q4, ~6–8 GB VRAM) auf Ollama; MCP-Wrapper ruft `POST /api/generate` mit base64-Image. Proxmox-Settings (Vorlage für Aktionsliste der nächsten Session) detailliert in §Vormerkungen + Session-Stopped-Sub-Block; Modell-Recherche gegen PromptQuorum „Local Vision Models 2026" — InternVL 2.5 8B (beste UI/Code-Passung), Qwen3-VL 8B (Fallback multilinguales OCR), Llama 3.2 Vision/MiniCPM-V/Moondream (verworfen). Plugin-Pfad (`DavidEasden/opencode-vision`) als Vormerkung zurückgestellt — 3 Commits, AGPL-3.0, kein dokumentiertes MCP-Backend, zu unreif. Kein Code-Touch; nachträglicher Commit nach Step-0-Commit `440e462`) | 2026-09-10 (Step 0 ✅ — Haushalt: Phasenverzeichnis angelegt, sechs kaputte `up:`/`down:`-Links in `p8x_ui_polish_notes.md` gefixt, vier fehlende L1-Cards ergänzt, drei `down:`-Listen korrigiert, `docs/INDEX.md` auf ≤ 38 KB komprimiert, zwei INDEX-Zeilen ergänzt + zwei Drift-Korrekturen; **pytest V107 ✅ 964 passed**, **ui_budget V97 ✅ 130,1 KB**, **V108 offen 863 ms** `_overview`-Latenz, **V106 Sammelmarker offen**, **V110/V112/V114/V115/V117/V119 Block-VERIFY offen**)
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

| # | Modul | Step | Status | Tests |
|---|---|---|---|---|
| 1 | Step 0 — Haushalt + Skelett: Phasenverzeichnis angelegt, sechs kaputte `up:`/`down:`-Links in `p8x_ui_polish_notes.md` gefixt, vier fehlende L1-Cards ergänzt (PROJECT_SESSION_LOG, SICHTPRUEFUNG_RESTBLOCK, SICHTPRUEFUNG_WALKTHROUGH, CLUSTER3_TESTBLOCK), drei `down:`-Listen im Inline-Format korrigiert (phase6_5_tools_images_plan, GLOBAL_SEARCH_PLAN, IMAGES_PLAN), `docs/INDEX.md` auf ≤ 38 KB komprimiert, zwei fehlende INDEX-Zeilen ergänzt (CLUSTER3_TESTBLOCK, THIRD_PARTY_LICENSES), zwei Drift-Korrekturen (`phase8_ui_graph` Softcap-Notiz + `phase5_ui` Behauptung widerrufen), Phasen-Head angelegt | 0 | ✅ | 0 (Skelett, wie P1/P6/6.5/7/8 Step 0) |
| 2 | Step V — **aufgeschoben** (Nikinger-Entscheidung 2026-09-10): Proxmox-Migration des Hosts steht bevor (i5-14600KF, dann Ryzen 7 5800X), Plugin-Installation übersprungen. **Backend:** lokales Vision-Modell `InternVL 2.5 8B` (Q4, Apache-2.0) auf Ollama-Basis statt Anthropic-Haiku-API. Begründung: Hardware-Migration macht lokalen Modell-Server sinnvoll, Proxmox-VM-Migration ist trivial, lokales Modell vermeidet Vendor-Lock-in + Audit-Trail-Aufwand. Vollständige Settings + Modell-Recherche: siehe Session-Block-Eintrag 2026-09-10 („Step V aufgeschoben") und Vormerkungen. | V | 🟡 (deferred — Entscheidung dokumentiert) | 0 (kein Code-Commit; nächste Session liefert Aktion → Command-Liste für Migration + Ollama-Setup + MCP-Wrapper) |
| 3 | Block A — Fundament: A1 Radiogruppe → `<select, (P8.6-H/I), A2 Layer-/Selektions-Tokens (`--bg-void`/`--select-fill`/`--select-fill-quiet`/`--select-line`/`--select-line-quiet`/`--caution`, P8.6-C/D/E/F), A3 `--border-soft`-Renderfehler-Fix (`app.css:1270/1276` → `var(--line)`, Plan §3.3), A4 Konvention v3 um fünfte Kategorie „Vorsicht" in `phase8_ui_graph/CLAUDE.md` §Selection/Choice-Konvention v3 (P8.6-G) | A | ⬜ | 0 → +7 statische Tests (`test_link_picker_uses_a_select_not_a_radio_group`, `test_no_raw_accent_rgba_outside_root`, `test_every_css_var_reference_is_defined`, `test_rail_order_settings_before_tree_logout_last`, `test_account_button_says_einstellungen`, `test_caution_class_only_on_logout_and_archive`, `test_overview_graph_has_no_max_width`) |
| 4 | Block B — Selektion vereinheitlichen: B1 Hover = leise Standardauswahl überall (`var(--select-fill-quiet)` + `outline`), B2 Ordner/Tags/Buckets prüfen, B3 Einstellungsmenü (`#account-show-updates`/`#account-manage-spaces` Navigation), B4 Sweep „alles Klickbare" mit Vorsicht-Kennzeichnung (`class="action--caution"` an Abmelden + Archivieren), B5 Radien (genau eine Änderung: `.link-picker-results` → `var(--radius-sm)`) | B | ⬜ | 0 → +1 statischer Test (`test_caution_class_only_on_logout_and_archive`) + ui_budget bleibt grün |
| 5 | Block C — Struktur: C1 „Konto" → „Einstellungen", Lesart b (Einstellungen nach oben, Abmelden ans Rail-Ende, P8.6-J/N3), C2 „Alle Items" unter die Spaces (`tree.js :: renderRail()`, P8.6-J), C3 Map als rechte Spalte / volle Höhe (`.overview` als Grid, P8.6-K/L), C4 Spaces in der Übersicht klickbar (`.overview__space-row` + `<button class="overview__space-open">`, P8.6-P), C5 Ordner-Zähler clientseitig aus `state.items` (P8.6-O) | C | ⬜ | 0 → ui_budget bleibt grün, Tabu-Diff leer |
| 6 | Block D — Graph-Fixes: D1 V102-Dedup (`dedupeEdges()` ungeordnetes Paar, P8.6-N), D2 deterministischer Layout-Seed (`seedJitter()` FNV-1a-Hash, P8.6-M), D3 `.overview__graph`-Höhe (bereits in C3 erledigt, nur V112-Gegenprobe), **D4 `runSimulation()` `rafId` endlich gelesen + `cancelAnimationFrame`** — die **einzige Scope-Erweiterung** des Plans (P8.6-§6.4: §2.1-Gebiet, aber direkte Ursache von §2.4-Verschlimmerung + 3 Zeilen Fix + schon halb da; **streichen, wenn der Nikinger es in der Sichtprüfung anders sieht**) | D | ⬜ | 0 → ui_budget bleibt grün, Tabu-Diff leer |
| 7 | Gate — Wegwerf-Instanz (eigener Port, eigener tmp-`DATA_ROOT`, PID-Datei, Hard Rule 9) + `p86_polish_smoke.py` 12 Stationen (Plan §7.2, Chromium + Firefox für 2/5/6/11) + Nikinger-Sichtprüfung §7.3 (fünf Entscheidungen: V110 §1, V114 §10.1, B2 §10.3, V112 §2.3, P8.6-R Versionierung) + Deploy `v3.0.2` zweigeteilt (D-a Agent, D-b Nikinger, D-c `health_gate.sh` 8/8) | Gate | ⬜ | 0 → `health_gate.sh` 8/8 + 12 Playwright-Stationen + Nikinger-Sichtprüfung |
| 8 | Step Z — Closeout (Plan §9 füllen, Phase-8.6-N: ein Dokument pro Phase, kein separates Handover-Dokument — P8.6-B; Rotation des Heads, INDEX/ROADMAP/Wurzel-Current-State nachziehen) | Z | ⬜ | 0 → pytest unverändert 964+ grün |

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

## Vormerkungen (nicht Teil eines aktuellen Steps)

- **P8.6-§6.4 (`cancelAnimationFrame` in `runSimulation()`) — streichbar:** der Fix ist
  drei Zeilen + direkt Ursache von §2.4-Verschlimmerung + schon halb da (`var rafId = null`
  wird zugewiesen, aber nie gelesen). Wenn der Nikinger in der Sichtprüfung anders entscheidet,
  ist es die einzige Scope-Erweiterung dieser Phase und wird in Block D gestrichen.
- **„Ordner umbenennen" → P9 oder danach** (Plan §0.4.1, bewusst draußen mit Analyse):
  die billige Frontend-Fassung verliert eine `.share.yml`-Freigabe still als Nebenwirkung
  einer Umbenennung (Hard Rule 4 — Rechte als Nebenwirkung); ein vollständiger Weg bräuchte
  `Store.rename_folder()` und wäre die neunte P1-Contract-Öffnung, die P8.6-S gerade zusperrt.
  Analyse ist der Ersatz für die Wiederholung der Untersuchung — wer das Feature plant, startet
  hier, nicht bei null.
- **Radiogruppe → `<select>`** (P8.6-H, Umkehr der P8.5-19-Entscheidung von 2026-09-06, die
  Nikinger selbst am 2026-09-08 umgekehrt hat): die Beschriftung **innerhalb** der Box
  (kein externes `<label>`), Kategorie *Choice* der Selection/Choice-Konvention v3 wieder
  hergestellt. `localStorage["sfx:linkpicker:mode"]` und sein Wert bleiben unverändert.

- **Vision-Backend: lokales Modell statt API** (Nikinger-Entscheidung 2026-09-10, siehe
  Session-Block-Eintrag unten): Proxmox-Migration zu stärkerem System steht bevor
  (i5-14600KF → Ryzen 7 5800X), Plugin-Installation aus Plan §2 wird übersprungen.
  **Backend:** `InternVL 2.5 8B` (Q4, Apache-2.0, ~6–8 GB VRAM) auf Ollama; MCP-Wrapper
  ruft `POST /api/generate` mit base64-Image. **Proxmox-Settings (Vorlage für die
  Aktionsliste der nächsten Session):**
  - **Host 1 (i5-14600KF, 6 P-Cores + 8 E-Cores, 20 Threads):** 12 vCPUs = 6 P-Cores
    (CPU-Typ `host`, gepinnt auf Cores 0–5) + 4 E-Cores; 16 GB RAM (Ballooning aus);
    50 GB Thin-LVM auf SSD (`local-lvm`); statische IPv4 im Cluster; Ollama lauscht
    auf `127.0.0.1:11434` (kein öffentliches Binding — MCP-Bridge spricht intern).
    P-Cores tragen 100 % der Vision-Inference-Last; E-Cores übernehmen MCP-Server-
    Handler und Ollama-Stream-Pool.
  - **Host 2 (Ryzen 7 5800X, 8 Cores, 16 Threads, Zen 3):** 10 vCPUs = 8 Cores + 2
    Threads (alle gleichwertig, keine P/E-Unterscheidung); CPU-Typ `host`; 16 GB RAM;
    50 GB; Netzwerk identisch.
  - **Setup-Befehle (für die nächste Session als Aktionsliste aufzubereiten):**
    `apt install -y ollama` (oder manuell), `ollama pull internvl2.5:8b`,
    MCP-Wrapper-Skript (~50 Zeilen Python, `requests.post` mit base64).
  - **Proxmox-Details:** NUMA auf Single-Sockel irrelevant; CPU-Pinning für P-Cores
    empfohlen; Memory-Ballooning **aus**; VirtIO-SCSI + iothread für Modell-Disk.
  - **Modell-Recherche (Stand 2026-09-10):** InternVL 2.5 8B (UI/Code-Screenshots, auf
    GitHub-Screenshots trainiert — beste Passung), Qwen3-VL 8B (multilinguales OCR,
    Fallback), Llama 3.2 Vision 11B (verworfen — Deutsch schwächer), MiniCPM-V 4.5
    (verworfen — UI schwächer), Moondream 2 (verworfen — limitiert). Quelle:
    PromptQuorum „Local Vision Models 2026".

## Nächste Session

**Nach Step 0 + Step-V-Entscheidung ist die Proxmox-Migration der nächste Schritt** —
kurze Aktion → Command-Liste für die Migration auf i5-14600KF (primär) bzw. Ryzen 7
5800X (sekundär), gefolgt von Ollama-Setup (`ollama pull internvl2.5:8b`) und
MCP-Wrapper-Skript (~50 Zeilen Python, POST `http://127.0.0.1:11434/api/generate` mit
base64-Image). **Nikinger-Wunsch:** „kurz und knackig Aktion → Command-Liste". Die
folgenden Proxmox-Settings sind im Vormerkungen-Abschnitt unten dokumentiert; sie
gelten als Vorlage für die Aktionsliste der nächsten Session.

Sobald das Vision-Backend steht, gilt `docs/concepts/sichtpruefung_automation_conventions.md`
§4 (Screenshots direkt im Chat). Der Plugin-Pfad aus Plan §2 wird nicht weiter
verfolgt — die Plugin-Landschaft bleibt eine Vormerkung für spätere Phasen, falls
sich das Bild ändert.

## Session stopped

### 2026-09-10 (Step 0 — Haushalt: Phasenverzeichnis, sechs Link-Fixes, vier L1-Cards, INDEX-Kompression, zwei INDEX-Zeilen + zwei Drift-Korrekturen; kein Code-Touch)

**Auftrag:** P8.6-Step-0-Befunde aus der Planungssession gegen `main`@`d1af51b`
(`docs/concepts/phase8_6_ui_polish_plan.md` §1, 2026-09-09) beheben — Phasenverzeichnis
anlegen, sieben Befunde abarbeiten, Baselines V97 + V107 im Head protokollieren. Ein
Commit (Plan §1.10).

**Was in diesem Commit passiert ist (sieben Befunde, in der Reihenfolge ihrer Behebung):**

1. **Befund 1 — sechs kaputte `up:`/`down:`-Links, alle in `p8x_ui_polish_notes.md`**
   gefixt (`../` → `../../`, `./phase8_ui_graph_plan.md` direkt). Gegenprobe gegen die 60
   anderen Frontmatter-Links im Repo: das waren die einzigen sechs.
2. **Befund 2 — vier fehlende L1-Header-Cards** angelegt: `docs/PROJECT_SESSION_LOG.md`
   (L3-Archiv), `phase8_5_picker_release/SICHTPRUEFUNG_RESTBLOCK.md`,
   `phase8_5_picker_release/SICHTPRUEFUNG_WALKTHROUGH.md`,
   `phase8_5_picker_release/CLUSTER3_TESTBLOCK.md`. Die vier dokumentierten Ausnahmen
   (`docs/UPDATE_LOG.md`, `phase5_ui/vendor/lucide/README.md`,
   `phase5_ui/THIRD_PARTY_LICENSES.md`, `phase6_shares/tests/golden/*.md`) bleiben
   korrekt card-los.
3. **Befund 3a — drei `down:`-Listen im Inline-Format** auf Listenform gebracht
   (`docs/concepts/phase6_5_tools_images_plan.md`, `phase6_shares/GLOBAL_SEARCH_PLAN.md`,
   `phase6_shares/IMAGES_PLAN.md`). Der eigentliche Befund war der Prüfer, der diese drei
   Dateien beim alten Listen-Scan still übersprang — gleichzeitig mit dem Fix notiert, der
   P8.6-2-Test wird eine Datei mit leerer `down:`-Extraktion als Warnung ausgeben statt als
   Erfolg.
4. **Befund 4 — zwei fehlende INDEX-Zeilen** ergänzt (`CLUSTER3_TESTBLOCK.md` unter Phase 8.5,
   `THIRD_PARTY_LICENSES.md` unter Referenzmaterial mit Ausnahme-Markierung).
5. **Befund 5 — zwei fehlerhafte INDEX-Zeilen** korrigiert: `phase8_ui_graph/CLAUDE.md`
   bekommt die Softcap-Notiz (Vorbild ist die `phase6_shares`-Zeile, P8-P); `phase5_ui/CLAUDE.md`
   verliert die Behauptung „über dem 40KB-Softcap" — sie war **falsch** (40.957 B = 3 B
   unter dem Softcap), wurde entfernt, ohne die Datei anzufassen.
6. **Befund 6 — `docs/INDEX.md`-Kompression** auf **≤ 38 KB** (genauer: 37.763 B **vor**
   dem Hinzufügen der Phase-8.6-Verzeichnis-Zeilen). Größte Posten: die Plan-Zeilen
   (P8.6/P8.5/P8/P7/P6/P6.5/P5/P4/P3/P2) auf das Wesentliche gestrafft, dated subnotes
   in den Zeilen geschlossener Phasen auf das Neueste + ein Pointer-Satz reduziert
   (L0 ist Landkarte, keine Kurzfassung — Plan §1.5). Sanity-Check: `find … -size +40k`
   trifft die Datei nicht.
7. **Befund 7 — zwei echte Code-Defekte dokumentiert, hier nicht behoben** (Step 0 ist
   Befund, nicht Reparatur): `var(--border-soft)` undefiniert (`app.css:1270/1276`,
   `.link-picker-results` zeichnet keinen Rahmen — Block A / Plan §3.3); `graph.js ::
   runSimulation()` `rafId` lokal aber nie gelesen, kein `cancelAnimationFrame` —
   Block D / Plan §6.4.

**Zusätzlich:** Phasenverzeichnis `phase8_6_ui_polish/` mit `CLAUDE.md` (dieser Head),
`SESSIONS_ARCHIVE.md` (leer mit 📦-Card) und `scripts/` (leer — Wegwerf-Smokes folgen in
Gate/§7) angelegt.

**Selbstprüfung (§0.5):**

- **Tabu-Diff** über die gesamte Phase leer — `git diff --stat -- phase1_storage/storage
  phase4_auth/authserver phase2_mcp/mcpserver phase5_ui/webui/security.py phase5_ui/webui/api.py
  phase5_ui/webui/serializers.py phase5_ui/webui/permissions.py` ergibt nichts (kein
  Code-Touch in dieser Session).
- `pytest -q` nicht gelaufen (kein Python-Touch — Plan §0.5 Punkt 2 gilt, Baseline V107
  von 2026-09-09 reicht für Step 0).
- `node --check` gegenstandslos (kein JS-Touch).
- `python phase5_ui/scripts/ui_budget.py` gegenstandslos (kein `webui/static/`-Touch —
  Baseline V97 von 2026-09-09 reicht für Step 0).
- **Kein rohes `rgba(62,141,243` außerhalb von `:root`** — gegenstandslos in Step 0,
  wird ab Block A zum statischen Test (P8.6-6, §8.2).
- **Größenprüfung** gelaufen: `phase8_6_ui_polish/CLAUDE.md` ist ~13 KB (unter 40-KB-
  Softcap), `SESSIONS_ARCHIVE.md` ist ~0,3 KB (leer mit Card), `scripts/` leer, INDEX
  nach Kompression + neuen Zeilen **unter** 38 KB.
- **Repo-weiter `up:`/`down:`-Link-Scan** gegen alle 60 Frontmatter geprüft: keine
  unauflösbaren Links mehr (vorher 6, jetzt 0). **Repo-weiter `down:`-Listenscan** gegen
  alle Frontmatter geprüft: keine Inline-Format-Listen mehr (vorher 3, jetzt 0).
- **Service-Touch 0** — Production-Dienst PID 355956 nicht angefasst, keine
  Wegwerf-Instanz gestartet (Plan §7.1 Wegwerf-Setup ist Step Gate, nicht Step 0).

**Hard-Rule-8-Doc-Update im selben Commit** (alles in einem Commit, Plan §1.10):
`docs/INDEX.md` (die sieben INDEX-Änderungen oben), `phase8_6_ui_polish/CLAUDE.md`
(dieser Head, neuer Session-Block allein — Rotationsregel P8.6-T eingehalten),
`phase8_6_ui_polish/SESSIONS_ARCHIVE.md` (neu, leer mit 📦-Card),
`phase8_5_picker_release/CLAUDE.md` (Modul-Status unverändert — P8.5 ist closed),
`docs/ROADMAP.md` und `CLAUDE.md` (Wurzel) — siehe separate Commits dieses Z-Closeouts
für die Current-state-/ROADMAP-Updates, die P8.6 als aktive Phase markieren.

**Commit-Message (Plan §1.10, wörtlich):**
`phase 8.6: Step 0 -- Haushalt, sechs kaputte Doku-Links, vier fehlende L1-Cards, INDEX-Kompression`

**Nächster Schritt:** **Step V** — OpenCode-Vision-Plugin-Installation gegen einen echten
Screenshot (V119, Plan §2). Bei Plugin-Repository-Konfig oder Authentifizierungs-Schritten,
die Nikinger-Beteiligung brauchen: **vor** der Installation fragen, nicht im Trial-and-Error-
Verfahren drei Repos durchprobieren.

### 2026-09-10 (Step 0 — nachträglich: Step V aufgeschoben, lokales Modell + Proxmox-Migration; kein weiterer Code-Touch)

**Auftrag:** Nach kurzer Recherche und drei Rückfragen hat der Nikinger entschieden, dass
Step V (Plan §2, OpenCode-Vision-Plugin-Installation) **aufgeschoben** wird zugunsten eines
**lokalen Vision-Modells** auf einem **neu zu migrierenden Proxmox-Host** (i5-14600KF
primär, danach Ryzen 7 5800X). Plugin-Pfad bleibt als Vormerkung, falls die Plugin-Landschaft
sich später ändert — die `DavidEasden/opencode-vision`-Landschaft ist zu unreif
(3 Commits, AGPL-3.0, kein dokumentiertes MCP-Backend) für unseren produktiven Use-Case.

**Entscheidung (mit Begründung):**
- **Backend:** `InternVL 2.5 8B` (Apache-2.0, ~6–8 GB VRAM Q4) auf Ollama-Basis, MCP-Wrapper
  ruft `POST http://127.0.0.1:11434/api/generate` mit base64-Image.
- **Begründung lokal statt API:** Proxmox-Migration des Hosts steht bevor (i5-14600KF ist
  primäres Ziel, danach Ryzen 7 5800X). Proxmox-VM-Migration ist trivial (im Cluster,
  gleiche Architektur). Lokales Modell vermeidet Vendor-Lock-in + Audit-Trail-Aufwand für
  Bild-Analysen in P8.6 + P9. Anthropic-Haiku-API hätte ~3 Cent/Phase gekostet — billig,
  aber die Begründung war eh nie Geld, sondern Tooling-Konsistenz und Audit-Trail.

**Modell-Recherche (Stand 2026-09-10, gegen PromptQuorum „Local Vision Models 2026"):**
- **InternVL 2.5 8B** ✅ — auf GitHub-Screenshots + UI-Mockups + Code-Outputs trainiert, beste
  Passung für unseren Use-Case („sind zwei Radio-Buttons sichtbar?").
- Qwen3-VL 8B — Fallback (multilinguales OCR, 8 Bilder/Request, Apache-2.0).
- Llama 3.2 Vision 11B — verworfen (Deutsch schwächer).
- MiniCPM-V 4.5 — verworfen (UI-Verständnis schwächer).
- Moondream 2 — verworfen (limitierte Szenen-Erkennung).

**Proxmox-Settings (für die nächste Session als Vorlage — die Aktionsliste kommt dort):**

*Host 1: i5-14600KF (6 P-Cores + 8 E-Cores, 20 Threads)*
- vCPUs: **12** = 6 P-Cores (CPU-Typ `host`, gepinnt auf Cores 0–5) + 4 E-Cores
- RAM: **16 GB** (Ballooning **aus**), 50 GB Thin-LVM auf SSD (`local-lvm`)
- Ollama lauscht auf `127.0.0.1:11434` (kein öffentliches Binding)
- Statische IPv4 im Cluster (für MCP-Erreichbarkeit)

*Host 2: Ryzen 7 5800X (8 Cores, 16 Threads, Zen 3)*
- vCPUs: **10** (8 Cores + 2 Threads, alle gleichwertig, CPU-Typ `host`)
- RAM: 16 GB, 50 GB, Netzwerk identisch

*Proxmox-Details (beide Hosts):* NUMA auf Single-Sockel irrelevant; CPU-Pinning empfohlen;
Memory-Ballooning **aus**; VirtIO-SCSI + iothread für Modell-Disk.

*Setup-Befehle:*
```bash
apt install -y ollama
ollama pull internvl2.5:8b
# MCP-Wrapper-Skript: ~50 Zeilen Python, requests.post mit base64-Image
```

**Was in diesem Commit passiert ist (nur Doku, kein Code-Touch):**
1. `phase8_6_ui_polish/CLAUDE.md`: Modul-Status Zeile 2 (Step V) ⬜ → 🟡-deferred;
   Vormerkungen-Sektion um „Vision-Backend: lokales Modell statt API" + Proxmox-Settings
   erweitert; Session-Stopped-Block um diesen Sub-Block ergänzt (P8.6-T-Rotationsregel:
   genau **ein** `## Session stopped`-Block mit einem oder mehreren `### date`-Subblöcken);
   Nächste-Session-Block auf Proxmox-Migration umgeschrieben.
2. `docs/concepts/phase8_6_ui_polish_plan.md` §2 (Step V): Korrekturnotiz am Anfang
   („Plugin-Pfad übersprungen, siehe Phase-Head-Vormerkungen für Proxmox-Plan").
3. `docs/INDEX.md`: updated-Pipe vorne ergänzt.

**Selbstprüfung (kein Code-Touch — analog zu Step 0):**
- Tabu-Diff §0.3 leer
- `pytest`/`ui_budget`/`node --check` gegenstandslos (kein Code-Touch)
- Service-Touch 0 (PID 355956 unverändert)
- Working-Tree nach Commit sauber

**Commit-Message:**
`phase 8.6: Step V deferred -- Proxmox-Migration + lokales Modell (InternVL 2.5 8B)`

**Nächster Schritt (in der nächsten Session, mit Aktions-Liste):**
1. Proxmox-Migration der Vision-VM auf i5-14600KF-Host
2. `ollama install` + `ollama pull internvl2.5:8b`
3. MCP-Wrapper-Skript (~50 Zeilen Python)
4. Smoke-Test gegen einen Phase-8.5-Screenshot (z. B. `c4_p8519_01_radiogruppe_im_dialog.png`)
   als Regression gegen V119-Erwartung
5. Falls erfolgreich → V119 abgehakt, Konventionen §4 aktiv, Plan §2-Aktualisierung mit
   „Vision-Backend: lokal, InternVL 2.5 8B"
6. Falls Ollama + InternVL auf der CPU nicht zufriedenstellend → Wechsel auf i5-14600KF
   vor Ryzen, oder Qwen3-VL 8B als Fallback