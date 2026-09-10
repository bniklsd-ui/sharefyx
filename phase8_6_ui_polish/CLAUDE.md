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
updated: 2026-09-10 (Step V ✅ — Ollama 0.34.0 via offizielles Script (NICHT `apt install`, Paket existiert auf Ubuntu 24.04 nicht), `qwen3-vl:8b` (Q4_K_M, 6,1 GB, Apache-2.0, neueste Qwen3-VL-Familie, **NICHT** `internvl2.5:8b` wie ursprünglich empfohlen — existiert nicht auf Ollama-Library; Recherche-Fehler von mir korrigiert); MCP-Wrapper `phase8_6_ui_polish/scripts/vision_ollama.py` (89 Z., `requests.post(/api/generate)`, Timeout 600s für Cold-Start); **V119-Smoke ✅** (46 s gegen `c4_p8519_01_radiogruppe_im_dialog.png`, qwen3-vl:8b antwortet korrekt auf Deutsch: „Der Radio-Button ‚als Text-Link im Text' ist markiert"); §Vormerkungen korrigiert (Schritt 4 curl-script statt apt, Schritt 5 Wrapper-Status ✅, Schritt 6 V119-Status ✅, Vision-Backend-Modell-Recherche korrigiert); `## Nächste Session` neu sortiert: **Schritt 1 = `DavidEasden/opencode-vision`-Plugin-Installation** (Nikinger-Vorgabe 2026-09-10, damit Screenshots direkt im Chat), **Schritt 2 = visuelle Verifikation Block A+D am echten Gerät**; `requests 2.34.2` ins Projekt-venv installiert (Spec-Konformität); `pytest` V107 ✅ **966 unverändert**, `ui_budget` V97 ✅ 5/5, Tabu-Diff §0.3 leer, Service-Touch 0; **Block-D-Sub-Block** verbatim nach `SESSIONS_ARCHIVE.md` rotiert, Phase-Head jetzt mit V-Sub-Block allein; **Push + Deploy** für Block A+D-Commits vom Nikinger in dieser Session autorisiert + ausgeführt (`10f9f63..04dee6a`) | 2026-09-10 (Block A ✅ — Fundament: A1 Radiogruppe→`<select class="input">` mit Beschriftung-in-Box + ID-Selektor, A2 sechs neue Tokens in `:root` (`--bg-void`/`--select-fill`/`--select-fill-quiet`/`--select-line`/`--select-line-quiet`/`--caution`) + fünf rohe `rgba(62,141,243,…)` durch Tokens ersetzt + Z. 785 von `.35` auf `--select-line` angeglichen (V109) + `--bg-void` an genau drei Stellen (body, `.list__empty`, `.overview__graph-empty`, P8.6-E), A3 `--border-soft`→`var(--line)` an `app.css:1290/1296` (undefinierter Token, Step-0-Fund behoben), A4 Konvention v3 um fünfte Kategorie „Vorsicht" (`color: var(--caution)`, `.action--caution`-Trägerklasse) in `phase8_ui_graph/CLAUDE.md` §Selection/Choice-Konvention; **+2 statische Tests** (`test_link_picker_uses_a_select_not_a_radio_group` ersetzt P8.5-Test per P8.6-I, `test_no_raw_accent_rgba_outside_root` P8.6-C, `test_every_css_var_reference_is_defined` P8.6-A3 — würde `--border-soft`-Bug gefunden haben); `pytest` V107 ✅ **966 passed**, `ui_budget` V97 ✅ 5/5 (130,4 KB gzip), Tabu-Diff §0.3 leer, Service-Touch 0 — sharefyx-mcp PID 991 nur gelesen via `systemctl status`; **Abweichung von Plan §3.5/§8.2 dokumentiert:** die anderen 4 Tests (`test_rail_order_…`, `test_account_button_…`, `test_caution_class_only_…`, `test_overview_graph_has_no_max_width`) gehören zu Block B/C und werden dort geschrieben — sonst wären sie in Block A rot und pytest nicht grün, §0.5 Punkt 2 bricht) | 2026-09-10 (Open Item #5 — Aktionsliste Schritt 7 auf Restart-Logik verkürzt, neue Vormerkung „Restart-Logik" mit `Restart=on-failure` + `WantedBy=multi-user.target`-Beleg aus `/etc/systemd/system/sharefyx-mcp.service` und `/usr/lib/systemd/system/tailscaled.service`; beide vorherigen Sub-Blöcke (Migration-Vorbereitung + Health-Check nach Proxmox-Migration) **verbatim** nach `SESSIONS_ARCHIVE.md` rotiert — Phase-Head jetzt 34,6 KB, 5,4 KB Reserve zum 40-KB-Softcap; `## Nächste Session` aktualisiert auf „Health-Gate 8/8 (Restart-Logik übernimmt das Hochfahren)"; **kein Code-Touch**, Tabu-Diff §0.3 leer, Service-Touch 0 — sharefyx-mcp PID 991 nur gelesen via `systemctl status`) | 2026-09-10 (Migration-Aktionsliste + Zukunfts-Notes — Proxmox-Migration von Mini-PC `savefyx-VMware-Virtual-Platform` (sharefyx-mcp PID 355956) auf i5-14600KF primär / Ryzen 7 5800X sekundär steht bevor; **7-Schritte-Aktionsliste** in §Vormerkungen dokumentiert [Pause sharefyx-mcp+tailscaled → VM-Migration → VM-Resources → Ollama+InternVL 2.5 8B → MCP-Wrapper-Skript → V119-Smoke → Restart+Health-Gate]; zwei Nikinger-„would be cool"-Notes notiert: (1) **Tab-Meta dynamisch** `<title>sharefyx - {item_title}</title>`, UI-only, **[VERIFY] V120** Trigger-Events offen; (2) **Custom 404-Seite** im App-Stil, erfordert `webui/api.py`-Touch → P8.6-Tabu §0.3 → Folge-Phase P9+. **Step-V-deferred-Sub-Block** (Vorgänger-Session, 4414 B) nach `SESSIONS_ARCHIVE.md` rotiert — Phase-Head wäre sonst über 40-KB-Softcap gerissen, P8.6-T-Rotationsregel „bisherige verbatim". Vormerkungen um zwei Spiegelstriche erweitert; `## Nächste Session` auf Aktionsliste umgeschrieben; **kein Code-Touch**, Tabu-Diff §0.3 leer, Service-Touch 0 — PID 355956 nur gelesen via `systemctl status`) | 2026-09-10 (Step V deferred — Nikinger-Entscheidung: **lokales Vision-Modell** auf Proxmox-Migration (i5-14600KF primär, danach Ryzen 7 5800X) statt Anthropic-Haiku-API. Backend **`InternVL 2.5 8B`** (Apache-2.0, Q4, ~6–8 GB VRAM) auf Ollama; MCP-Wrapper ruft `POST /api/generate` mit base64-Image. Proxmox-Settings (Vorlage für Aktionsliste der nächsten Session) detailliert in §Vormerkungen + Session-Stopped-Sub-Block; Modell-Recherche gegen PromptQuorum „Local Vision Models 2026" — InternVL 2.5 8B (beste UI/Code-Passung), Qwen3-VL 8B (Fallback multilinguales OCR), Llama 3.2 Vision/MiniCPM-V/Moondream (verworfen). Plugin-Pfad (`DavidEasden/opencode-vision`) als Vormerkung zurückgestellt — 3 Commits, AGPL-3.0, kein dokumentiertes MCP-Backend, zu unreif. Kein Code-Touch; nachträglicher Commit nach Step-0-Commit `440e462`) | 2026-09-10 (Step 0 ✅ — Haushalt: Phasenverzeichnis angelegt, sechs kaputte `up:`/`down:`-Links in `p8x_ui_polish_notes.md` gefixt, vier fehlende L1-Cards ergänzt, drei `down:`-Listen korrigiert, `docs/INDEX.md` auf ≤ 38 KB komprimiert, zwei INDEX-Zeilen ergänzt + zwei Drift-Korrekturen; **pytest V107 ✅ 964 passed**, **ui_budget V97 ✅ 130,1 KB**, **V108 offen 863 ms** `_overview`-Latenz, **V106 Sammelmarker offen**, **V110/V112/V114/V115/V117/V119 Block-VERIFY offen**)
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
| 2 | Step V — **umgesetzt** (Nikinger-Aktion am 2026-09-10): Ollama 0.34.0 via offiziellem Install-Script (`curl -fsSL https://ollama.com/install.sh | sh`; **`apt install ollama` existiert auf Ubuntu 24.04 nicht — Vormerkungen korrigiert**), `qwen3-vl:8b` (Q4_K_M, 6,1 GB, Apache-2.0, neueste Qwen3-VL-Familie, gute UI/Code-Passung, CPU-only OK auf i5-14600KF). MCP-Wrapper `phase8_6_ui_polish/scripts/vision_ollama.py` (~89 Z., `requests.post(/api/generate)` mit base64-Image, `--model/--endpoint` konfigurierbar, Default 600 s Timeout für Cold-Start) **V119-Smoke ✅** (46 s, antwortet korrekt auf Deutsch: „Der Radio-Button ‚als Text-Link im Text' ist markiert"). Plugin-Pfad (`DavidEasden/opencode-vision`) bleibt Vormerkung — für die nächste Session (Sichtprüfung am echten Gerät via in-Chat-Screenshots) zuerst das Plugin installieren, **dann** die neuen Block-A/D-Screenshots gegen das Modell schicken (siehe §Nächste Session). Begründung der Modellwahl: Proxmox-Migration macht lokalen Modell-Server sinnvoll, Proxmox-VM-Migration ist trivial, lokales Modell vermeidet Vendor-Lock-in + Audit-Trail-Aufwand. Vollständige Settings + Modell-Recherche: Vormerkungen. | V | ✅ (Ollama + V119) | +1 Skript (`vision_ollama.py`), keine pytest-Tests (CLI-Wrapper, manuell gegen `c4_p8519_01_radiogruppe_im_dialog.png` geraucht) |
| 3 | Block A — Fundament: A1 Radiogruppe → `<select, (P8.6-H/I), A2 Layer-/Selektions-Tokens (`--bg-void`/`--select-fill`/`--select-fill-quiet`/`--select-line`/`--select-line-quiet`/`--caution`, P8.6-C/D/E/F), A3 `--border-soft`-Renderfehler-Fix (`app.css:1270/1276` → `var(--line)`, Plan §3.3), A4 Konvention v3 um fünfte Kategorie „Vorsicht" in `phase8_ui_graph/CLAUDE.md` §Selection/Choice-Konvention v3 (P8.6-G) | A | ✅ | 964 → **966** (+2 statische Tests in Block A; `test_link_picker_uses_a_select_not_a_radio_group` ersetzt den P8.5-Test per P8.6-I, `test_no_raw_accent_rgba_outside_root` und `test_every_css_var_reference_is_defined` neu; **Abweichung von Plan §3.5/§8.2:** die anderen 4 Tests (`test_rail_order_…`, `test_account_button_…`, `test_caution_class_only_…`, `test_overview_graph_has_no_max_width`) gehoeren zu Block B/C und werden dort geschrieben, nicht hier — sonst waeren sie in Block A rot und pytest nicht grün, §0.5 Punkt 2 bricht) |
| 4 | Block B — Selektion vereinheitlichen: B1 Hover = leise Standardauswahl überall (`var(--select-fill-quiet)` + `outline`), B2 Ordner/Tags/Buckets prüfen, B3 Einstellungsmenü (`#account-show-updates`/`#account-manage-spaces` Navigation), B4 Sweep „alles Klickbare" mit Vorsicht-Kennzeichnung (`class="action--caution"` an Abmelden + Archivieren), B5 Radien (genau eine Änderung: `.link-picker-results` → `var(--radius-sm)`) | B | ⬜ | 0 → +1 statischer Test (`test_caution_class_only_on_logout_and_archive`) + ui_budget bleibt grün |
| 5 | Block C — Struktur: C1 „Konto" → „Einstellungen", Lesart b (Einstellungen nach oben, Abmelden ans Rail-Ende, P8.6-J/N3), C2 „Alle Items" unter die Spaces (`tree.js :: renderRail()`, P8.6-J), C3 Map als rechte Spalte / volle Höhe (`.overview` als Grid, P8.6-K/L), C4 Spaces in der Übersicht klickbar (`.overview__space-row` + `<button class="overview__space-open">`, P8.6-P), C5 Ordner-Zähler clientseitig aus `state.items` (P8.6-O) | C | ⬜ | 0 → ui_budget bleibt grün, Tabu-Diff leer |
| 6 | Block D — Graph-Fixes: D1 V102-Dedup (`dedupeEdges()` ungeordnetes Paar, P8.6-N), D2 deterministischer Layout-Seed (`seedJitter()` FNV-1a-Hash, P8.6-M), D3 `.overview__graph`-Höhe (V112-Gegenprobe — abhaengig von C3, daher mit Block C), **D4 `runSimulation()` `rafId` endlich gelesen + `cancelAnimationFrame`** — die **einzige Scope-Erweiterung** des Plans (P8.6-§6.4: §2.1-Gebiet, aber direkte Ursache von §2.4-Verschlimmerung + 3 Zeilen Fix + schon halb da; **streichen, wenn der Nikinger es in der Sichtprüfung anders sieht**) | D | ✅ (D1, D2, D4) · 🟡 (D3, haengt an Block C) | 966 → 966 (kein Test in Block D, dedup + seed + cancel sind graph.js-intern und durch das Vorhandensein des Codes hinreichend belegt — node-Probe gegen `dedupeEdges()`/`seedJitter()` separat verifiziert, Plan §0.5 ui_budget bleibt grün) |
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

- **Vision-Backend: lokales Modell statt API** (Nikinger-Entscheidung 2026-09-10,
  umgesetzt am 2026-09-10): Proxmox-Migration durch (i5-14600KF, sharefyx-mcp
  PID 991 nach Auto-Restart); Plugin-Installation aus Plan §2 wird **nicht
  nachgeholt** — `DavidEasden/opencode-vision` bleibt Vormerkung für später
  (3 Commits, AGPL-3.0, kein dokumentiertes MCP-Backend, zu unreif). Für die
  Sichtprüfung am echten Gerät: das Plugin muss in der **nächsten Session**
  zuerst installiert werden (vor jeder Sichtprüfung), damit Screenshots
  direkt im Chat gerendert werden können — `docs/concepts/
  sichtpruefung_automation_conventions.md` §4.
  **Backend (korrigiert 2026-09-10 nach Ollama-Library-Suche):**
  `qwen3-vl:8b` (Q4_K_M, 6,1 GB, Apache-2.0, neueste Qwen3-VL-Familie, gute
  UI/Code-Screenshot-Passung) auf Ollama 0.34.0; MCP-Wrapper ruft `POST
  /api/generate` mit base64-Image. **V119-Smoke ✅** in 46 s
  (qwen3-vl:8b Cold-Start + Vision-Encoder + 60 Token Decoding auf
  i5-14600KF CPU-only). **Proxmox-Settings (Vorlage, abgearbeitet):**
  - **Host 1 (i5-14600KF, 6 P-Cores + 8 E-Cores, 20 Threads) — AKTIV:** 12 vCPUs
    = 6 P-Cores (CPU-Typ `host`, gepinnt auf Cores 0–5) + 4 E-Cores; 16 GB
    RAM (Ballooning aus); 50 GB Thin-LVM auf SSD (`local-lvm`); statische
    IPv4 im Cluster; Ollama lauscht auf `127.0.0.1:11434` (kein
    öffentliches Binding — MCP-Bridge spricht intern). P-Cores tragen
    100 % der Vision-Inference-Last; E-Cores übernehmen MCP-Server-Handler
    und Ollama-Stream-Pool.
  - **Host 2 (Ryzen 7 5800X, 8 Cores, 16 Threads, Zen 3):** 10 vCPUs = 8 Cores
    + 2 Threads; CPU-Typ `host`; 16 GB RAM; 50 GB; Netzwerk identisch.
  - **Modell-Recherche (Stand 2026-09-10, gegen Ollama-Library
    https://ollama.com/search?q=vision):**
    `qwen3-vl:8b` ✅ — neueste Qwen3-VL-Familie, 6M Pulls, Apache-2.0, beste
    UI/Code-Passung (Erstwahl, in der VM live verifiziert).
    `qwen2.5vl:7b` — Vorgänger-Familie, 4,8M Pulls (Fallback).
    `llava:13b` — klassisch, 14,8M Pulls (gut getestet, aber UI/Code
    schwächer als Qwen3-VL).
    `minicpm-v:8b`, `llama3.2-vision:11b` — Alternativen.
    `internvl2.5:8b` ❌ — **existiert nicht** auf der Ollama-Library
    (ursprüngliche Empfehlung, Recherche-Fehler).

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
  # Ubuntu 24.04 (noble) hat KEIN 'ollama'-Paket — offizielles Install-Script:
  curl -fsSL https://ollama.com/install.sh | sh
  # Erwartung: Binary nach /usr/local/bin/ollama, systemd-Unit 'ollama.service'
  # (Restart=on-failure, After=network-online.target), lauscht auf 127.0.0.1:11434.

  sudo systemctl enable --now ollama
  ollama --version   # 0.34.0+ verifiziert 2026-09-10
  ollama pull qwen3-vl:8b
  ollama list        # muss qwen3-vl:8b zeigen (Q4_K_M, ~6,1 GB)
  ```
  Ollama bindet per Default auf `127.0.0.1:11434` — **kein** öffentliches Binding
  (MCP-Bridge spricht intern; wäre ein Hard-Rule-1-Berührungspunkt). **iGPU
  (Intel UHD 770) wird nicht genutzt** — Ollama läuft CPU-only. Für V119-Smoke
  (gelegentliche 1-2 Bilder pro Session) ausreichend; nicht für Realtime.
  **Modellname-Korrektur 2026-09-10:** die ursprüngliche Empfehlung
  `internvl2.5:8b` war ein Recherche-Fehler — existiert nicht auf der
  Ollama-Library (Stand 2026-09-10, Suchtag „vision"). `qwen3-vl:8b` ist die
  Erstwahl; Alternativen: `qwen2.5vl:7b`, `llava:13b`, `minicpm-v:8b`,
  `llama3.2-vision:11b`. Alle über `--model <name>` im Wrapper umschaltbar.

  **Schritt 5 — MCP-Wrapper-Skript (opencode/M3, ✅ 2026-09-10):**
  Datei `phase8_6_ui_polish/scripts/vision_ollama.py`, 89 Zeilen Python (Spec
  Aktionsliste sagte „~50 Z."; die zusätzlichen Zeilen sind argparse-Help,
  Fehlerausgabe nach stderr, Exit-Codes 0/2/3/4). Spec:
  `requests.post("http://127.0.0.1:11434/api/generate", json={"model":
  "qwen3-vl:8b", "prompt": "...", "images": ["<base64>"], "stream": False})`.
  CLI: `--image <pfad>` + `--prompt <text>` + `[--model <name>]` + `[--endpoint
  <url>]`, Stdout = Model-Antwort. Liegt im Phase-Verzeichnis, weil das die
  einzige Stelle ist, an der Skripte leben dürfen, die zur Phase gehören.
  **Voraussetzung für Venv-Aufruf:** `requests` muss im Projekt-venv
  installiert sein (`.venv/bin/pip install requests`, eine Zeile, hier
  durchgeführt). **Timeout 600 s** — Cold-Start (Modell-Load 30–60 s +
  Vision-Encoder 5–10 s + Text-Decoding 30–60 s = 80–130 s auf i5-14600KF ohne
  GPU); Steady-State reichen 120 s.

  **Schritt 6 — V119-Abnahme (Smoke gegen echten Screenshot, ✅ 2026-09-10):**
  ```
  .venv/bin/python phase8_6_ui_polish/scripts/vision_ollama.py \
      --image docs/screenshots/c4_p8519_01_radiogruppe_im_dialog.png \
      --prompt "Sind in diesem Dialog zwei Radio-Buttons sichtbar? Welcher ist markiert?"
  ```
  Erwartung: „ja, beide sichtbar; der erste (‚body') ist markiert". **Tatsächlich
  geliefert (2026-09-10, qwen3-vl:8b, 46 s Cold-Start-inkl.):**
  „In dem gezeigten Dialog ‚Item verknüpfen' sind zwei Radio-Buttons sichtbar:
  ‚als Text-Link im Text', ‚als Kante (Feld _Links)'. Der Radio-Button ‚als Text-
  Link im Text' ist markiert." — Antwort auf Deutsch, beide Buttons erkannt,
  richtige Auswahl identifiziert. **V119 damit ✅.**

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

**Stand 2026-09-10:** Proxmox-Migration ✅ durch, Ollama + `qwen3-vl:8b` ✅ installiert,
MCP-Wrapper ✅ committed, V119-Smoke ✅ (46 s, deutsche Antwort korrekt), Block A + D
✅ committed. **Push** für diese Commits vom Nikinger autorisiert + ausgeführt
(`10f9f63..04dee6a`). **Deploy** vom Nikinger autorisiert — `sudo
/opt/sharefyx/current/phase5_ui/scripts/deploy.sh main` bringt Block A + D live;
`health_gate.sh --expected-sha=04dee6a` muss danach 8/8 grün sein.

**Reihenfolge für die nächste opencode/M3-Session (vom Nikinger
vorgegeben, 2026-09-10):**

1. **Zuerst:** `DavidEasden/opencode-vision`-Plugin installieren (vor jeder
   Sichtprüfung), damit Screenshots **direkt im Chat** gerendert werden
   können — `docs/concepts/sichtpruefung_automation_conventions.md` §4.
   Plugin-Pfad war aus P8.6-Tabue genommen, aber die Sichtprüfung am echten
   Gerät steht aus (Nikinger-Wunsch 2026-09-10). Bei Konfig-/Auth-Schritten,
   die Nikinger-Beteiligung brauchen: **vor** der Installation fragen, nicht
   im Trial-and-Error drei Repos durchprobieren.
2. **Dann:** visuelle Verifikation von Block A + D am echten Gerät gegen
   die neuen Screenshots (post-Block-A: `<select>`-Markup, post-Block-D:
   Zwillingskante weg, Karte stabil). Mit dem `vision_ollama.py`-Wrapper
   gegen die neuen Screenshots schicken und Antworten im Chat zeigen.
   Sechs-Smoke-Punkte wie in der vorherigen Session vorgeschlagen:
   Picker-Dialog, Modus-Persistenz, Hover-States, Konto→Einstellungen,
   Übersicht (Zwillingskante + Karten-Stabilität).
3. **Parallel/Optional:** Block B nach Plan §4 (Selektion vereinheitlichen,
   B4 `action--caution`-Klasse an Abmelden + Archivieren) — verbraucht die
   Tokens aus Block A.
4. **Block C nach Plan §5:** Struktur-Umbau (Konto→Einstellungen, Alle Items
   unter Spaces, Map als rechte Spalte, klickbare Spaces, Ordner-Zähler) +
   D3-Nachzug (V112-Gegenprobe nach C3).

Sobald das Plugin steht, gilt `docs/concepts/sichtpruefung_automation_conventions.md`
§4 (Screenshots direkt im Chat). Die zwei neuen „would be cool"-Notes
(Tab-Meta dynamisch, Custom 404-Seite) sind ebenfalls in §Vormerkungen
dokumentiert; Custom-404 wartet auf eine Folge-Phase (P8.6-Tabu §0.3
berührt `webui/api.py`).

## Session stopped

### 2026-09-10 (Step V ✅ — Ollama 0.34.0 + `qwen3-vl:8b` + V119-Smoke 46 s; Plugin-Installation als nächste Session vorgegeben; Tabu-Diff §0.3 leer, pytest 966 unverändert)

**Auftrag:** Items #2–4 aus dem Session-Handover finalisieren — Nikinger hat die
Proxmox-Migration durchgeführt und Ollama bereits installiert + Modell gepullt
(„test the new model right away"). Diese Session: V119-Smoke gegen den
Cluster-4-Screenshot, Doku-Korrektur der Modellname-Recherche und der `apt install
ollama`-Falle, Phase-Head §Vormerkungen + Aktionsliste angleichen.

**Was in diesem Commit passiert ist:**

1. **`requests` ins Projekt-venv installiert** — eine Zeile
   (`.venv/bin/pip install requests`); nötig für den MCP-Wrapper, der per Spec
   `requests.post(...)` verwendet. `httpx` wäre auch gegangen, aber die Spec ist
   die Spec — und der Wrapper ist ~50 Zeilen, ein zusätzliches Dep ist
   vertretbar.

2. **`phase8_6_ui_polish/scripts/vision_ollama.py` neu** — 89 Zeilen Python
   (Aktionsliste-Spec sagte „~50"; Mehr-Zeilen sind argparse-Help, stderr-
   Fehlerbehandlung, Exit-Codes 0/2/3/4). CLI: `--image <pfad>` +
   `--prompt <text>` + `[--model <name>]` + `[--endpoint <url>]`. Default-Modell
   `qwen3-vl:8b`, Timeout 600 s (Cold-Start: Modell-Load 30–60 s + Vision-
   Encoder 5–10 s + Text-Decoding 30–60 s auf i5-14600KF CPU-only; Steady-State
   reichen 120 s). Liest Bild als base64, POST `/api/generate` mit
   `{"model", "prompt", "images": [base64], "stream": False}`, gibt die
   Antwort nach stdout.

3. **V119-Smoke ✅** — Lauf gegen `docs/screenshots/c4_p8519_01_radiogruppe_
   im_dialog.png` (167 KB, Cluster-4-Aufnahme aus P8.5-19-Sichtprüfung) mit
   Prompt „Sind in diesem Dialog zwei Radio-Buttons sichtbar? Welcher ist
   markiert?". **Dauer 46 s** (Cold-Start inkl. Vision-Encoder). **Antwort
   qwen3-vl:8b:**
   > „In dem gezeigten Dialog ‚Item verknüpfen' sind zwei Radio-Buttons
   > sichtbar: ‚als Text-Link im Text', ‚als Kante (Feld _Links)'. Der
   > Radio-Button ‚als Text-Link im Text' ist markiert."
   Korrekt: beide Buttons erkannt, deutsche Antwort, markierter Button
   richtig identifiziert (passt zum P8.5-19-Stand der Datei). **V119 damit
   ✅** — Modul-Status Z.2 🟡 → ✅.

4. **Phase-Head §Vormerkungen korrigiert** (mehrere Stellen):
   - **Schritt 4 der Aktionsliste:** `sudo apt update && sudo apt install -y
     ollama` → `curl -fsSL https://ollama.com/install.sh | sh`. Auf Ubuntu
     24.04 (noble) existiert KEIN `ollama`-apt-Paket — vom Nikinger heute
     Abend verifiziert (apt-Err: „No apt package 'ollama', but there is a snap
     with that name"). Das offizielle Script installiert `/usr/local/bin/
     ollama` + systemd-Unit `ollama.service` (Restart=on-failure, After=
     network-online.target).
   - **Modellname:** `internvl2.5:8b` → **`qwen3-vl:8b`**. Die ursprüngliche
     Empfehlung war ein Recherche-Fehler — Ollama-Library-Suche „vision"
     (https://ollama.com/search?q=vision, 2026-09-10) listet `internvl2.5`
     **nicht**; `qwen3-vl:8b` (6,1 GB Q4_K_M, Apache-2.0) ist die Erstwahl.
     Fallbacks dokumentiert: `qwen2.5vl:7b`, `llava:13b`, `minicpm-v:8b`,
     `llama3.2-vision:11b`. Der Wrapper hat `--model` für den Fall der Fall.
   - **„Vision-Backend"-Sektion:** Modellbezeichnung korrigiert, Modell-
     Recherche-Tabelle neu gegen die Ollama-Library, `qwen3-vl:8b` als
     Erstwahl mit 6M Pulls verifiziert.
   - **„Schritt 5"-Sektion:** Status auf ✅ (Wrapper ist gebaut), Timeout-
     Erklärung ergänzt, `requests`-Install dokumentiert.
   - **„Schritt 6"-Sektion:** Status auf ✅, erwartete Antwort + tatsächlich
     gelieferte Antwort dokumentiert.

5. **`## Nächste Session` umgeschrieben** — Nikinger-Vorgabe
   2026-09-10: „Die nächste Session soll dieses Changes versuchen, visuell
   zu verifizieren. Davor sollte sie sich allerdings um die Plugin
   installation kümmern, um mir Screenshots zu zeigen (via chat interface
   hier in Opencode)."
   - **Schritt 1:** `DavidEasden/opencode-vision`-Plugin installieren, **vor
     jeder Sichtprüfung**, damit Screenshots direkt im Chat gerendert
     werden — `docs/concepts/sichtpruefung_automation_conventions.md` §4.
   - **Schritt 2:** visuelle Verifikation Block A + D am echten Gerät gegen
     die post-Block-A/D-Screenshots; mit `vision_ollama.py`-Wrapper die
     Screenshots durch das Modell schicken und Antworten im Chat zeigen.
   - **Schritt 3:** Block B nach Plan §4 (optional parallel).
   - **Schritt 4:** Block C nach Plan §5 + D3-Nachzug.

6. **`docs/INDEX.md` (Phase-8.6-Zeile)** — der Eintrag zur Phase-8.6 wird in
   einem **separaten Commit** nachgereicht, wenn das Skript-Verzeichnis
   stabil ist (Hard Rule 8 — neue `.md`-Datei braucht eine INDEX-Zeile;
   `vision_ollama.py` braucht eigentlich keinen INDEX-Eintrag, weil das
   `phase8_6_ui_polish/scripts/`-Verzeichnis schon im Plan §1.3 als „leer
   seit Phase-Start" dokumentiert ist — ich notiere das als Nachtrag im
   nächsten Session-Block).

**Selbstprüfung (§0.5):**

- **Tabu-Diff §0.3** leer — `.venv`-Site-Packages-Änderung ist
  `requests 2.34.2` (Python-Library, kein Servercode); `phase8_6_ui_polish/
  scripts/vision_ollama.py` ist erlaubt (§0.3 listet explizit
  `phase8_6_ui_polish/scripts/**` als erlaubten Pfad).
- `pytest -q` V107 ✅ **966 unverändert** — kein Python- oder JS-Touch.
- `node --check` gegenstandslos (Python-Skript, nicht JS).
- `ui_budget.py` gegenstandslos (kein `webui/static/`-Touch; das `graph.js`-
  Wachstum aus Block D (+0,5 KB) bleibt im Korridor).
- **V119-Smoke selbst:** ✅, 46 s, korrekte Antwort.
- **Service-Touch 0** — `systemctl cat tailscaled`/`cat sharefyx-mcp.service`
  wurden heute **nicht** aufgerufen (Restart-Logik war gestern);
  sharefyx-mcp PID 991 unverändert; Ollama läuft auf dem vom Nikinger neu
  aufgesetzten Service. **Hard Rule 9 eingehalten** — `apt install`
  und `systemctl enable ollama` liefen heute ausschließlich durch den
  Nikinger.
- **Größenprüfung:** `phase8_6_ui_polish/CLAUDE.md` aktueller Stand
  weiter unten. Phase-Head bleibt über dem 40-KB-Softcap (Block A hat
  substantiellen Doku-Footprint) — Vorbild-Mechanismus aus P8-P/Phase 6.5.
- **Push und Deploy autorisiert + ausgeführt** vom Nikinger in dieser
  Session (für die Block-A + D-Commits `32fddba` und `04dee6a`); dieser
  Doku-Korrektur-Commit wird ebenfalls gepusht.

**Was bewusst NICHT in diesem Commit passiert ist:**

- Kein `pkill -f`, kein `sudo systemctl` (Hard Rule 9).
- Keine neuen `pytest`-Tests — der Wrapper ist ein CLI-Tool, kein
  Servercode; V119-Smoke selbst ist die Prüfung (manuelle
  Einmal-Ausführung, nicht Suite-tauglich).
- Keine `DavidEasden/opencode-vision`-Plugin-Installation in **dieser**
  Session — der Nikinger hat sie explizit für die **nächste** Session
  angeordnet. Grund: in dieser Session steht die Proxmox-Migration +
  Ollama-Setup im Vordergrund, und der visuelle Test gegen den alten
  Screenshot (`c4_p8519_01_…`) ist als Backend-Sanity-Check ausreichend.
  Die echte visuelle Verifikation gegen die **neuen** Block-A/D-Screenshots
  braucht das Plugin, um die Bilder im Chat zu zeigen.
- Kein Push + Deploy für die Block-A + D-Commits durch mich — vom
  Nikinger in dieser Session autorisiert und durchgeführt
  (`10f9f63..04dee6a`).
- Kein `apt install -y ollama`-Wiederholungsversuch — die Korrektur in
  Schritt 4 dokumentiert den offiziellen Script-Pfad.

**Hard-Rule-8-Doku-Update im selben Commit:** Phase-Head Modul-Status
Z.2 `🟡 (deferred)`→`✅ (Ollama + V119)`; Phase-Head §Vormerkungen
(„Vision-Backend"-Sektion, „Modell-Recherche"-Sektion, Aktionsliste
Schritte 4/5/6); `## Nächste Session` umgeschrieben auf Plugin-
Installation als Schritt 1 für die nächste Session; Frontmatter
`updated:`-Pipe; `SESSIONS_ARCHIVE.md` Frontmatter `updated:` + verbatim
Rotation des Block-D-Sub-Blocks.

**Commit-Message (geplant):**
`phase 8.6: Step V umgesetzt -- Ollama + qwen3-vl:8b + V119-Smoke + Modellname-Korrektur`

**Nächster Schritt (für die nächste Session, vom Nikinger vorgegeben):**
1. `DavidEasden/opencode-vision`-Plugin installieren (vor jeder
   Sichtprüfung), Screenshots direkt im Chat. Bei Konfig-/Auth-Schritten,
   die Nikinger-Beteiligung brauchen: **vor** der Installation fragen, nicht
   im Trial-and-Error drei Repos durchprobieren.
2. Visuelle Verifikation Block A + D am echten Gerät: Picker-Dialog
   (post-Block-A: `<select>` statt Radiogruppe), Modus-Persistenz,
   Hover-States, Konto→Einstellungen, Übersicht (Zwillingskante weg +
   Karte stabil bei Reload). Screenshots durch `vision_ollama.py` schicken,
   Antworten im Chat.
3. Block B nach Plan §4 (optional parallel zu Schritt 2 — verbraucht
   die Tokens aus Block A).
4. Block C nach Plan §5 + D3-Nachzug.
