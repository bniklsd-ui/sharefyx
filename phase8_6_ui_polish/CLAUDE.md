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
updated: 2026-09-10 (Block A ✅ — Fundament: A1 Radiogruppe→`<select class="input">` mit Beschriftung-in-Box + ID-Selektor, A2 sechs neue Tokens in `:root` (`--bg-void`/`--select-fill`/`--select-fill-quiet`/`--select-line`/`--select-line-quiet`/`--caution`) + fünf rohe `rgba(62,141,243,…)` durch Tokens ersetzt + Z. 785 von `.35` auf `--select-line` angeglichen (V109) + `--bg-void` an genau drei Stellen (body, `.list__empty`, `.overview__graph-empty`, P8.6-E), A3 `--border-soft`→`var(--line)` an `app.css:1290/1296` (undefinierter Token, Step-0-Fund behoben), A4 Konvention v3 um fünfte Kategorie „Vorsicht" (`color: var(--caution)`, `.action--caution`-Trägerklasse) in `phase8_ui_graph/CLAUDE.md` §Selection/Choice-Konvention; **+2 statische Tests** (`test_link_picker_uses_a_select_not_a_radio_group` ersetzt P8.5-Test per P8.6-I, `test_no_raw_accent_rgba_outside_root` P8.6-C, `test_every_css_var_reference_is_defined` P8.6-A3 — würde `--border-soft`-Bug gefunden haben); `pytest` V107 ✅ **966 passed**, `ui_budget` V97 ✅ 5/5 (130,4 KB gzip), Tabu-Diff §0.3 leer, Service-Touch 0 — sharefyx-mcp PID 991 nur gelesen via `systemctl status`; **Abweichung von Plan §3.5/§8.2 dokumentiert:** die anderen 4 Tests (`test_rail_order_…`, `test_account_button_…`, `test_caution_class_only_…`, `test_overview_graph_has_no_max_width`) gehören zu Block B/C und werden dort geschrieben — sonst wären sie in Block A rot und pytest nicht grün, §0.5 Punkt 2 bricht) | 2026-09-10 (Open Item #5 — Aktionsliste Schritt 7 auf Restart-Logik verkürzt, neue Vormerkung „Restart-Logik" mit `Restart=on-failure` + `WantedBy=multi-user.target`-Beleg aus `/etc/systemd/system/sharefyx-mcp.service` und `/usr/lib/systemd/system/tailscaled.service`; beide vorherigen Sub-Blöcke (Migration-Vorbereitung + Health-Check nach Proxmox-Migration) **verbatim** nach `SESSIONS_ARCHIVE.md` rotiert — Phase-Head jetzt 34,6 KB, 5,4 KB Reserve zum 40-KB-Softcap; `## Nächste Session` aktualisiert auf „Health-Gate 8/8 (Restart-Logik übernimmt das Hochfahren)"; **kein Code-Touch**, Tabu-Diff §0.3 leer, Service-Touch 0 — sharefyx-mcp PID 991 nur gelesen via `systemctl status`) | 2026-09-10 (Migration-Aktionsliste + Zukunfts-Notes — Proxmox-Migration von Mini-PC `savefyx-VMware-Virtual-Platform` (sharefyx-mcp PID 355956) auf i5-14600KF primär / Ryzen 7 5800X sekundär steht bevor; **7-Schritte-Aktionsliste** in §Vormerkungen dokumentiert [Pause sharefyx-mcp+tailscaled → VM-Migration → VM-Resources → Ollama+InternVL 2.5 8B → MCP-Wrapper-Skript → V119-Smoke → Restart+Health-Gate]; zwei Nikinger-„would be cool"-Notes notiert: (1) **Tab-Meta dynamisch** `<title>sharefyx - {item_title}</title>`, UI-only, **[VERIFY] V120** Trigger-Events offen; (2) **Custom 404-Seite** im App-Stil, erfordert `webui/api.py`-Touch → P8.6-Tabu §0.3 → Folge-Phase P9+. **Step-V-deferred-Sub-Block** (Vorgänger-Session, 4414 B) nach `SESSIONS_ARCHIVE.md` rotiert — Phase-Head wäre sonst über 40-KB-Softcap gerissen, P8.6-T-Rotationsregel „bisherige verbatim". Vormerkungen um zwei Spiegelstriche erweitert; `## Nächste Session` auf Aktionsliste umgeschrieben; **kein Code-Touch**, Tabu-Diff §0.3 leer, Service-Touch 0 — PID 355956 nur gelesen via `systemctl status`) | 2026-09-10 (Step V deferred — Nikinger-Entscheidung: **lokales Vision-Modell** auf Proxmox-Migration (i5-14600KF primär, danach Ryzen 7 5800X) statt Anthropic-Haiku-API. Backend **`InternVL 2.5 8B`** (Apache-2.0, Q4, ~6–8 GB VRAM) auf Ollama; MCP-Wrapper ruft `POST /api/generate` mit base64-Image. Proxmox-Settings (Vorlage für Aktionsliste der nächsten Session) detailliert in §Vormerkungen + Session-Stopped-Sub-Block; Modell-Recherche gegen PromptQuorum „Local Vision Models 2026" — InternVL 2.5 8B (beste UI/Code-Passung), Qwen3-VL 8B (Fallback multilinguales OCR), Llama 3.2 Vision/MiniCPM-V/Moondream (verworfen). Plugin-Pfad (`DavidEasden/opencode-vision`) als Vormerkung zurückgestellt — 3 Commits, AGPL-3.0, kein dokumentiertes MCP-Backend, zu unreif. Kein Code-Touch; nachträglicher Commit nach Step-0-Commit `440e462`) | 2026-09-10 (Step 0 ✅ — Haushalt: Phasenverzeichnis angelegt, sechs kaputte `up:`/`down:`-Links in `p8x_ui_polish_notes.md` gefixt, vier fehlende L1-Cards ergänzt, drei `down:`-Listen korrigiert, `docs/INDEX.md` auf ≤ 38 KB komprimiert, zwei INDEX-Zeilen ergänzt + zwei Drift-Korrekturen; **pytest V107 ✅ 964 passed**, **ui_budget V97 ✅ 130,1 KB**, **V108 offen 863 ms** `_overview`-Latenz, **V106 Sammelmarker offen**, **V110/V112/V114/V115/V117/V119 Block-VERIFY offen**)
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
| 3 | Block A — Fundament: A1 Radiogruppe → `<select, (P8.6-H/I), A2 Layer-/Selektions-Tokens (`--bg-void`/`--select-fill`/`--select-fill-quiet`/`--select-line`/`--select-line-quiet`/`--caution`, P8.6-C/D/E/F), A3 `--border-soft`-Renderfehler-Fix (`app.css:1270/1276` → `var(--line)`, Plan §3.3), A4 Konvention v3 um fünfte Kategorie „Vorsicht" in `phase8_ui_graph/CLAUDE.md` §Selection/Choice-Konvention v3 (P8.6-G) | A | ✅ | 964 → **966** (+2 statische Tests in Block A; `test_link_picker_uses_a_select_not_a_radio_group` ersetzt den P8.5-Test per P8.6-I, `test_no_raw_accent_rgba_outside_root` und `test_every_css_var_reference_is_defined` neu; **Abweichung von Plan §3.5/§8.2:** die anderen 4 Tests (`test_rail_order_…`, `test_account_button_…`, `test_caution_class_only_…`, `test_overview_graph_has_no_max_width`) gehoeren zu Block B/C und werden dort geschrieben, nicht hier — sonst waeren sie in Block A rot und pytest nicht grün, §0.5 Punkt 2 bricht) |
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
  Aktionsliste unten):**
  - **Host 1 (i5-14600KF, 6 P-Cores + 8 E-Cores, 20 Threads):** 12 vCPUs = 6 P-Cores
    (CPU-Typ `host`, gepinnt auf Cores 0–5) + 4 E-Cores; 16 GB RAM (Ballooning aus);
    50 GB Thin-LVM auf SSD (`local-lvm`); statische IPv4 im Cluster; Ollama lauscht
    auf `127.0.0.1:11434` (kein öffentliches Binding — MCP-Bridge spricht intern).
    P-Cores tragen 100 % der Vision-Inference-Last; E-Cores übernehmen MCP-Server-
    Handler und Ollama-Stream-Pool.
  - **Host 2 (Ryzen 7 5800X, 8 Cores, 16 Threads, Zen 3):** 10 vCPUs = 8 Cores + 2
    Threads (alle gleichwertig, keine P/E-Unterscheidung); CPU-Typ `host`; 16 GB RAM;
    50 GB; Netzwerk identisch.
  - **Proxmox-Details:** NUMA auf Single-Sockel irrelevant; CPU-Pinning für P-Cores
    empfohlen; Memory-Ballooning **aus**; VirtIO-SCSI + iothread für Modell-Disk.
  - **Modell-Recherche (Stand 2026-09-10):** InternVL 2.5 8B (UI/Code-Screenshots, auf
    GitHub-Screenshots trainiert — beste Passung), Qwen3-VL 8B (multilinguales OCR,
    Fallback), Llama 3.2 Vision 11B (verworfen — Deutsch schwächer), MiniCPM-V 4.5
    (verworfen — UI schwächer), Moondream 2 (verworfen — limitierte Szenen-Erkennung).
    Quelle: PromptQuorum „Local Vision Models 2026".

- **Proxmox-Migration — Aktionsliste (Nikinger, 2026-09-10, „kurz und knackig
  Aktion → Command-Liste")** für die Migration von Mini-PC
  `savefyx-VMware-Virtual-Platform` (sharefyx-mcp.service PID 355956,
  `ActiveEnterTimestamp=2026-09-05 16:10:18 CEST`, **aktuell noch hier**) auf
  i5-14600KF (primär) bzw. Ryzen 7 5800X (sekundär). **opencode/M3 schreibt nur
  Doku + das MCP-Wrapper-Skript (Schritt 5);** alle `sudo systemctl`-/Proxmox-
  Befehle sind Nikinger-Aktionen (Hard Rule 9 + §0.5.7).

  **Schritt 1 — sharefyx-mcp + Funnel pause (Nikinger, Vordergrund-Shell):**
  ```
  sudo systemctl stop sharefyx-mcp
  sudo systemctl stop tailscaled
  ```
  Verifikation: `systemctl status sharefyx-mcp` → `inactive (dead)`,
  `pgrep -af sharefyx-mcp` liefert nichts. PID 355956 erst beim **Re-Start**
  verschwinden — vor dem Pause **nicht** festhalten, da D2-Deploy erfahrungsgemäß
  den Dienst erwartungsgemäß neu startet.

  **Schritt 2 — VM migrieren (Proxmox, je nach Storage):**

  *Live-Migration* (passende Shared Storage, beide Nodes sehen den Storage):
  ```
  qm migrate <VMID> <target-node> --online --with-local-disks
  ```

  *Cold-Migration* (Default, lokales `local-lvm` — Disk muss mit):
  ```
  qm shutdown <VMID> --timeout 60
  ```
  → in Proxmox-UI: VM auf Ziel-Node verschieben + CPU-Typ auf `host` setzen
  → wieder starten:
  ```
  qm start <VMID>
  ```

  *Re-Build* (nur wenn Mini-PC-Settings nicht passen — z. B. BIOS-Typ):
  ```
  qm stop <VMID>
  qm export <VMID> /tmp/sharefyx-export.vma.zst --format vma_zstd
  # auf Ziel-Node: neue VM anlegen, dann
  qm importdisk <new-vmid> /tmp/sharefyx-export.vma.zst <target-storage> --format vma_zstd
  ```

  **Schritt 3 — VM-Resources setzen (i5-14600KF primär):**
  ```
  qm set <VMID> --cores 12 --sockets 1 --cpu host --numa 0
  qm set <VMID> --memory 16384 --balloon 0
  qm set <VMID> --scsihw virtio-scsi-single --scsi0 local-lvm:50,iothread=1,discard=on
  ```

  **CPU-Pinning** (nur i5-14600KF; Ryzen 7 5800X braucht **kein** Pinning —
  Architektur kennt keine P/E-Unterscheidung, alle Cores gleichwertig):
  ```
  # Bestehende affinity-Zeile entfernen (idempotent), dann neue setzen:
  sed -i '/^affinity:/d' /etc/pve/qemu-server/<VMID>.conf
  echo 'affinity: 0-5,12-15' >> /etc/pve/qemu-server/<VMID>.conf
  # Verifikation:
  grep '^affinity:' /etc/pve/qemu-server/<VMID>.conf
  ```
  P-Core-Pinning 0–5 (= 6 P-Cores) + E-Core-Pinning 12–15 (= 4 E-Cores aus
  der hinteren Hälfte). Wirksam erst nach `qm stop <VMID>` + `qm start <VMID>`.

  Bei Ryzen 7 5800X nur `--cores 10 --sockets 1` setzen, kein Pinning.

  **Schritt 4 — Ollama installieren + Vision-Modell pullen (in der migrierten VM):**
  ```
  sudo apt update && sudo apt install -y ollama
  sudo systemctl enable --now ollama
  ollama pull internvl2.5:8b
  ollama list   # muss internvl2.5:8b zeigen
  ```
  Ollama bindet per Default auf `127.0.0.1:11434` — **kein** öffentliches Binding
  (MCP-Bridge spricht intern; wäre ein Hard-Rule-1-Berührungspunkt).

  **Schritt 5 — MCP-Wrapper-Skript (opencode/M3, neu):**
  Datei `phase8_6_ui_polish/scripts/vision_ollama.py`, ~50 Zeilen Python. Spec:
  `requests.post("http://127.0.0.1:11434/api/generate", json={"model":
  "internvl2.5:8b", "prompt": "...", "images": ["<base64>"], "stream": False})`.
  CLI: `--image <pfad>` + `--prompt <text>`, Stdout = Model-Antwort. Liegt im
  Phase-Verzeichnis, weil das die einzige Stelle ist, an der Skripte leben
  dürfen, die zur Phase gehören.

  **Schritt 6 — V119-Abnahme (Smoke gegen echten Screenshot):**
  ```
  python phase8_6_ui_polish/scripts/vision_ollama.py \
      --image docs/screenshots/c4_p8519_01_radiogruppe_im_dialog.png \
      --prompt "Sind in diesem Dialog zwei Radio-Buttons sichtbar? Welcher ist markiert?"
  ```
  Erwartung: „ja, beide sichtbar; der erste (‚body') ist markiert". **Falls
  Modell untauglich:** Qwen3-VL 8B als Fallback (`ollama pull qwen3-vl:8b`,
  Modell-Name im Skript tauschen — Hard-Rule-1-Variante als Streitfall
  zurück in den Phase-Head, **kein** stiller Tausch).

  **Schritt 7 — Health-Gate (Regression-Schutz, keine manuellen `start`-Calls):**
  ```
  bash phase8_5_picker_release/scripts/health_gate.sh --expected-sha=<HEAD>
  ```
  Erwartung: `health_gate.sh` 8/8 grün. Bei Rot: `journalctl -u sharefyx-mcp
  -n 200` + Diagnose-Block aus `phase3_edge/CLAUDE.md`. V119 erfolgreich → Phase-
  Head Modul-Status V119 🟡 → ✅, neuer `## YYYY-MM-DD`-Block in
  `docs/UPDATE_LOG.md`, V120 (Trigger-Events für Tab-Meta-Notiz) geöffnet.
  **Begründung der Verkürzung (2026-09-10, Restart-Logik entdeckt):** die
  `sudo systemctl start`-Aufrufe sind redundant — siehe „Restart-Logik"-
  Vormerkung unten. Der einzige manuelle Eingriff ist das **`stop`** in Schritt 1
  (zum Lock-Release vor der VM-Migration); nach der Migration sorgt die
  Auto-Restart-Mechanik (systemd `WantedBy=multi-user.target` + `Restart=on-failure`)
  allein für „services sind wieder up".

- **Restart-Logik (Nikinger-Fund 2026-09-10, Verifikation in dieser Session
  gelesen, kein Service-Touch)** — was nach der Proxmox-Migration tatsächlich
  gegriffen hat und damit die `sudo systemctl start`-Aufrufe in Schritt 7
  ersetzt:
  - **`sharefyx-mcp.service`** (`/etc/systemd/system/sharefyx-mcp.service:19-20`)
    trägt `Restart=on-failure` + `RestartSec=5` — Crash-Recovery im 5-Sekunden-
    Takt. Plus `After=network-online.target tailscaled.service` und
    `Wants=network-online.target` (Z. 6-7) — Boot-Reihenfolge ist damit
    deterministisch.
  - **`tailscaled.service`** (`/usr/lib/systemd/system/tailscaled.service:18`,
    vom Paket) trägt ebenfalls `Restart=on-failure`. Wird **nicht** durch eine
    eigene Unit ergänzt — die Vendor-Unit reicht.
  - **Beide Units sind `WantedBy=multi-user.target`** (implizit über
    `[Install]`-Sektion). Nach VM-Boot oder VM-Migration-Recovery starten sie
    ohne `systemctl start`-Aufruf.
  - **Konsequenz für die Aktionsliste:** Schritt 7 ist nur noch Health-Gate.
    Die `stop`-Aufrufe in Schritt 1 bleiben — sie sind **kein Restart-Pfad**,
    sondern Lock-Release für die Migration (Live-Migration blockiert sonst,
    Cold-Migration braucht sauberen State). Der **einzige** Schritt, der einen
    systemd-Aufruf enthält, ist also Schritt 1.
  - **V103-Notiz für den Deploy (P8.6-R):** die ungeklärte P8.5-V-Frage „ist
    der `sudo`-Prompt im Vordergrund sichtbar?" beantwortet sich durch diese
    Mechanik von selbst — beim Deploy nach P8.6 gibt es keinen einzigen
    `sudo`-Call mehr (D-a Agent, D-b Nikinger deployt **ohne** `sudo` falls
    Hard-Rule-9-konform ermöglicht — das ist eine Folge-Diskussion mit dem
    Nikinger, **nicht** P8.6-Entscheidung).

- **Zukunfts-Notes außerhalb des aktuellen Phasen-Scopes (Nikinger, 2026-09-10,
  „would be cool")** — explizit **nicht** P8.6, **nicht** P9, erst notiert:
  - **Tab-Meta-Texte dynamisch** — `<title>sharefyx - {item_title}</title>` beim
    Bearbeiten-Dialog oder Detail-Ansicht statt des aktuellen statischen
    `sharefyx`-Titels. UI-only, vermutlich `app.js :: openDetail()`/
    `closeDetail()` mit `document.title`-Update. Niedrigschwellig; könnte
    Anhängsel an P8.6-Block B werden (P8.6-H/I/J), oder eigene Mini-Phase.
    **[VERIFY] V120** — welche Events den Title-Update triggern sollen
    (Editor-Open, Detail-Open, Spaces-Wechsel, Suche).
  - **Custom 404-Seite** — statt FastAPI-Default-JSON
    (`{"detail": "Not Found"}`) eine HTML-Seite im App-Stil (Logo + „Diese Seite
    gibt es nicht" + Link zur Startseite). Statisches HTML in
    `phase5_ui/webui/static/404.html` + Custom-ExceptionHandler in
    `webui/api.py`. **Vorsicht:** `webui/api.py` ist im P8.6-Tabu (§0.3) — die
    Note gehört in eine Folge-Phase, in der die Tabu-Liste neu bewertet wird.
    Nicht-P8.6, vermutlich P9+ oder eigene Mini-Phase. Niedrigschwellig
    technisch, aber tabu-berührt.

## Nächste Session

**Nach Step 0 + Step-V-Entscheidung ist die Proxmox-Migration der nächste Schritt** —
die ausführungsreife Aktionsliste (7 Schritte, Aktion → Befehl) steht jetzt im
Vormerkungen-Abschnitt oben unter „Proxmox-Migration — Aktionsliste (Nikinger,
2026-09-10)". Kurzfassung: Pause `sharefyx-mcp` + `tailscaled` (Nikinger) → VM
migrieren (Proxmox `qm migrate` oder shutdown+move) → VM-Resources setzen
(`qm set --cores 12 --memory 16384 --balloon 0 --cpu host`) → `apt install
-y ollama` + `ollama pull internvl2.5:8b` (in der migrierten VM) →
`phase8_6_ui_polish/scripts/vision_ollama.py` (opencode/M3, ~50 Z. Python,
`POST /api/generate` mit base64-Image) → V119-Smoke gegen
`c4_p8519_01_radiogruppe_im_dialog.png` → **Health-Gate** 8/8 (Restart-Logik
übernimmt das Hochfahren, siehe Vormerkung „Restart-Logik" — Schritt 7 hat
keine `systemctl start`-Aufrufe mehr).

Sobald das Vision-Backend steht, gilt `docs/concepts/sichtpruefung_automation_conventions.md`
§4 (Screenshots direkt im Chat). Der Plugin-Pfad aus Plan §2 wird nicht weiter
verfolgt — die Plugin-Landschaft bleibt eine Vormerkung für spätere Phasen, falls
sich das Bild ändert. Die zwei neuen „would be cool"-Notes (Tab-Meta dynamisch,
Custom 404-Seite) sind ebenfalls in §Vormerkungen dokumentiert.

## Session stopped

### 2026-09-10 (Block A ✅ — Fundament: Radiogruppe→`<select>`, Layer-/Selektions-Tokens, `--border-soft`-Fix, Konvention v3 um „Vorsicht"; Tabu-Diff §0.3 leer, pytest 964→966)

**Auftrag:** Block A nach Plan §3 — A1 Radiogruppe → `<select class="input">` (P8.6-H/I),
A2 Layer-/Selektions-Tokens + fünf rohe `rgba(62,141,243,…)` durch `var(--select-fill)`/
`var(--select-line)` ersetzen (P8.6-C/D/E/F), A3 `--border-soft`-Renderfehler-Fix in
`app.css` (P8.6-§3.3), A4 Konvention v3 um die fünfte Kategorie „Vorsicht" erweitern
(P8.6-G). Reihenfolge: Token-Fundament zuerst (A vor B ist zwingend, P8.6-U). Ziel ist,
dass Block B/C/D die Tokens verbrauchen, ohne selbst welche anzulegen.

**Was in diesem Commit passiert ist:**

1. **`phase5_ui/webui/static/app.html` (A1):** `<fieldset class="link-picker-modes">` mit
   zwei `<input type="radio" name="link-picker-mode">` ersetzt durch
   `<div class="input input--labeled"><label class="input-label-inline" for="link-picker-mode">Einfügen</label><select class="input" id="link-picker-mode"><option value="body" selected>…</option><option value="frontmatter">…</option></select></div>`.
   `localStorage["sfx:linkpicker:mode"]` und sein Wert unveraendert (bestehende Browser
   behalten ihre Wahl).

2. **`phase5_ui/webui/static/js/dialogs.js` (A1):** Modul-Konstante `LINK_PICKER_MODE_NAME`
   entfernt; `_linkPickerMode()` und `_restoreLinkPickerMode()` lesen/schreiben jetzt
   `linkPickerModeEl.value` statt `input[name="…"]:checked`; `initLinkPicker()` haengt
   den `change`-Listener an **ein** Element statt einer `NodeList`-Schleife. Kommentar
   zur P8.6-A1-Motivation am Konstantenblock (war: P8.5-Bezug, jetzt: P8.6-Bezug mit
   Verlauf-Hinweis).

3. **`phase5_ui/webui/static/app.css` (A1/A2/A3):**
   - `:root` (Z. 28-83) um **sechs** neue Tokens erweitert: `--bg-void: #000` (P8.6-D,
     Layer 0, "echtes Schwarz" fuer OLED); `--select-fill` und `--select-fill-quiet`
     (voller und halbtransparenter Selektions-Verlauf, P8.6-C); `--select-line` und
     `--select-line-quiet` (volle und halbtransparente Akzent-Linie, P8.6-C); `--caution:
     var(--danger)` (Alias fuer die fuenfte Konventions-Kategorie, P8.6-F).
   - **Fuenf** rohe `rgba(62,141,243,…)`-Vorkommen ausserhalb `:root` (Z. 403/685/719/
     785/1291) durch Tokens ersetzt; Z. 785 zusaetzlich von `.35` auf `--select-line`s
     `.40` angeglichen (V109, "Im Zweifel angleichen"). `grep "rgba(62,141,243"` trifft
     jetzt nur noch `:root`-Zeilen + den Erklaerungs-Kommentar.
   - `--border-soft` (undefiniert, Step-0-Fund) an Z. 1290/1296 durch `var(--line)`
     ersetzt — der bestehende Haarlinien-Token, den jede andere Panel-Kante verwendet.
   - `--bg-void` an genau **drei** Stellen eingesetzt (P8.6-E): `body` (Boot/Login-
     Hintergrund), `.list__empty, .detail__empty`, `.overview__graph-empty`. **Bewusst
     sparsam** — die uebrigen 60+ Stellen bleiben auf `--bg` (Layer 1).
   - `.link-picker-modes`/`.link-picker-mode*`-CSS-Bloecke (A1, Z. 1334-1361) entfernt.
   - Neue `.input--labeled`/`.input-label-inline`-CSS-Klassen fuer den `<div>`-Traeger
     mit Label-inline + Select-rechts.

4. **`phase8_ui_graph/CLAUDE.md` (A4):** Selection/Choice-Konvention v3 um eine **fuenfte
   Tabellenzeile** „Vorsicht" erweitert (`.action--caution`-Tragerklasse, `color:
   var(--caution)`, **keine** gefuellte rote Flaeche). Ueberschrift „Die vier Kategorien"
   → „Die **fuenf** Kategorien"; Block-Datum-Notiz am Anfang des Abschnitts (P8.6-G:
   die Konvention bleibt in **einem** Dokument, kein zweites Konventions-Doc — `DOC_
   LAYERS_CONVENTION.md` verbietet zwei Kopien derselben Regel). Zusatzsatz zur
   Abgrenzung: *„Vorsicht ist keine Bestaetigungspflicht. Ein Knopf dieser Kategorie
   darf trotzdem einen Bestaetigungsdialog haben (Archivieren hat einen), aber die
   Farbe ersetzt ihn nicht und verlangt ihn nicht."*

5. **`phase5_ui/tests/test_static_routes.py`:** bestehender P8.5-Test
   `test_link_picker_uses_a_radio_group_not_a_select` → umgekehrt + umbenannt zu
   `test_link_picker_uses_a_select_not_a_radio_group` (P8.6-I, Docstring traegt beide
   Richtungen mit Datum). Zwei neue Tests: `test_no_raw_accent_rgba_outside_root`
   (P8.6-C, maschineller Waelchter ueber die fuenf Stellen) und `test_every_css_var_
   reference_is_defined` (P8.6-A3, haette den `--border-soft`-Bug gefunden — und
   findet den naechsten; matcht nicht nur `:root`, weil `@supports`/andere Scopes auch
   definieren duerfen, **und** strippt CSS-Kommentare, damit historische Token-Namen
   wie `--accent-text` in Erklaerungs-Kommentaren nicht als „undefiniert" gezaehlt
   werden).

6. **Hard-Rule-8-Doku-Update im selben Commit:** `phase8_6_ui_polish/CLAUDE.md` Modul-
   Status Tabelle (Zeile 3 `⬜`→`✅`, +2 statische Tests dokumentiert, Abweichung von
   Plan §3.5/§8.2 erklaert), Phase-Head-Session-Sub-Block (Rotation: vorheriger
   Item-#5-Block verbatim nach `SESSIONS_ARCHIVE.md`), Frontmatter `updated:`-Pipe,
   `docs/INDEX.md` Phase-8.6-Zeile aktualisiert, `ROADMAP.md` P8.6-Zeile aktualisiert,
   Wurzel-`CLAUDE.md` Current-state Block ergaenzt.

**Selbstpruefung (§0.5):**

- **Tabu-Diff** ueber die gesamte Phase leer: `git diff --stat -- phase1_storage/
  storage phase4_auth/authserver phase2_mcp/mcpserver phase5_ui/webui/{security,api,
  serializers,permissions}.py` liefert nichts. Erlaubte Pfade beruehrt:
  `phase5_ui/webui/static/{app.html,app.css,js/dialogs.js}`, `phase5_ui/tests/
  test_static_routes.py`, `phase8_ui_graph/CLAUDE.md` (P8.6-G explizit).
- **`pytest -q`** **966 passed in 118 s** (V107-Baseline 964 → +2; Netto-Effekt des
  Test-Renames + 2 neuer Tests).
- **`node --check`** auf `dialogs.js`: OK (kein Syntax-Fehler nach der LINK_PICKER_MODE_
  NAME-Entfernung und dem Init-Block-Umbau).
- **`ui_budget.py`** **5/5 im Zielkorridor** (V97-Baseline gehalten): `items?limit=50`
  roh 26,5 KB, gzip 1,3 KB; `items/{id}` 0,7 KB; `app.js+app.css+Font` gzip **130,4 KB**
  (Baseline 130,1 KB, +0,3 KB durch die neuen Tokens und `.input--labeled`-Bloecke —
  unter dem 250-KB-Ziel); Erstaufruf 138,6 KB (unter 400 KB). `dialogs.js` 13,1 KB
  (Baseline 12,6 KB, +0,5 KB durch die ausfuehrlicheren Kommentare und das Entfernen
  der NodeList-Schleife; **kein** Code-Wachstum in der heissen Pfad-Linie). V108
  „_overview"-Latenz heute **365 ms** (deutlich unter der historischen 438–453 ms-
  Spanne, kein Rauschen — die 863 ms aus V108-Baseline war ein Ausreisser, vermutlich
  Last auf dem alten Mini-PC vor der Migration).
- **Punkt 5 der §0.5-Checkliste** (kein rohes `rgba(62,141,243` ausserhalb `:root`):
  maschinell verifiziert (`python3`-Inline-Skript `:root`-Block entfernt, dann
  `grep "rgba(62,141,243"` → **0 Treffer**).
- **Phase 8 §0.3-Verbotsliste** eingehalten: kein Emoji-Icon, kein Gradient-Branding,
  kein 3er-Card-Grid, keine dekorative Farbe, keine neue Schriftfamilie, kein Element
  dessen Erkennbarkeit allein von Transparenz/Blur abhaengt (manuell bestaetigt).
- **Groessenpruefung:** `phase5_ui/webui/static/app.css` 62,5 KB (vorher 61,4 KB, +1,1 KB
  durch Tokens + drei `--bg-void`-Stellen + `.input--labeled`); `app.html` 31,7 KB;
  `dialogs.js` 45,1 KB; `phase8_ui_graph/CLAUDE.md` 43,2 KB (vorher 42,3 KB, **+850 B**
  statt der geplanten ~600 B — die Konventionstabelle hat mehr zusaetzlichen Text als
  nur eine Tabellenzeile). `phase8_6_ui_polish/CLAUDE.md` aktueller Stand weiter unten.
- **Service-Touch 0** — kein `sudo systemctl`, kein `pkill -f`, kein Pfad auf den
  echten `DATA_ROOT`/Keyring. Production-Dienst sharefyx-mcp (PID 991) **nicht**
  angefasst.
- **`ollama list`** meldet weiterhin `command not found` — Items #2–4 aus dem Handover
  bleiben blockiert (Nikinger-Aktion fuer Schritt 4 der Aktionsliste).

**Was bewusst NICHT in diesem Commit passiert ist:**

- **Kein Block B/C/D-Code-Touch** — A vor B ist zwingend (P8.6-U), und der Token-
  Vorrat ist jetzt vollstaendig. Block B kann mit B1 (Hover-Vereinheitlichung) und
  B4 (`action--caution`-Klasse an Abmelden + Archivieren) anfangen.
- **Keine Schritte 1–3 der Aktionsliste** (Ollama/MCP-Wrapper/V119-Smoke) — bleiben
  Nikinger- bzw. Proxmox-migrationsabhaengig.
- **Keine Tests fuer Block B/C** (die anderen 4 aus Plan §8.2) — bewusste Abweichung
  vom Plan §3.5/§8.2, weil sie in Block A rot waeren. Sie werden in Block B/C/D
  geschrieben, sobald ihr Code existiert. **Dokumentiert in der Modul-Status-Tabelle.**
- **Kein `pkill -f`**, **kein `sudo systemctl`**, **kein Push** ohne Nikinger-
  Anweisung.
- **Keine Custom-404-Seite, kein Tab-Meta-Dynamic-Title** — die zwei „would be cool"-
  Zukunfts-Notes bleiben explizit draussen (P8.6-Tabu, Phase-Head §Vormerkungen).

**Commit-Message (geplant):**
`phase 8.6: Block A -- Radiogruppe zurueck auf select, Layer-/Selektions-Tokens, --border-soft-Fix`

**Naechster Schritt (in dieser oder naechsten Session):**
1. **Block B** nach Plan §4 (B1 Hover-Vereinheitlichung, B2 Ordner/Tags/Buckets,
   B3 Einstellungsmenue-Navigation, B4 Sweep mit `action--caution`-Klasse an Abmelden
   + Archivieren, B5 eine Radius-Aenderung an `.link-picker-results`). Hinzu kommen
   `test_caution_class_only_on_logout_and_archive` als statischer Test (P8.6-B4).
2. Block C nach Plan §5 (Struktur-Umbau: Konto→Einstellungen, Alle Items unter
   Spaces, Map als rechte Spalte, klickbare Spaces, Ordner-Zaehler). Drei weitere
   statische Tests.
3. Block D nach Plan §6 (V102-Dedup, deterministischer Layout-Seed, optional
   `cancelAnimationFrame`-Fix in `runSimulation()` — der „streichen, wenn der Nikinger
   es in der Sichtpruefung anders sieht"-Vorbehalt bleibt).
4. Erst nach A/B/C/D: Gate (§7) mit Wegwerf-Instanz + Nikinger-Sichtpruefung +
   Deploy `v3.0.2`.

