---
status: live
purpose: Phase-10.5-Head — Modulstatus der Blöcke 0–12/Z, Deploy-Tabelle A–D, Abnahmestand P10.5-1–61, offene Punkte beim Nikinger, aktueller Session-Block. Plan und Arbeitsliste stehen in eigenen Dateien.
read-when: Arbeiten in phase10_5_finishing/ — zuerst lesen, zusammen mit dem Session-Block unten
detail: L2
up: ../ROADMAP.md
down:
  - ../docs/concepts/phase10_5_finishing_plan.md    # 📕 der Plan: Locks P10.5-A–W, Blöcke 0–12/Z, Abnahme, [VERIFY] V207–V219
  - ../phase10_inventory/BAUSTELLENREGISTER.md      # 📗 die Arbeitsliste — hier wird abgehakt (P10-B)
  - ../phase10_inventory/ENTSCHEIDUNGEN_ARCHIVE.md  # 📦 §12 Entscheidungsliste D-1–D-18, verbatim
  - SESSIONS_ARCHIVE.md                             # 📦 ältere Session-Blöcke, verbatim, newest-first
updated: 2026-10-22 (Block 0 **abgeschlossen**: 0.6 ROADMAP-Zeile P10.5 auf 🔄, 0.7 Ausführer-Vorbedingung protokolliert — Abnahme P10.5-1–4 ✅) | 2026-10-22 (Block 0: 0.2/0.3 — Phase-Head angelegt (Modulstatus, Deploy-Tabelle, Abnahmestand 61 Zeilen), DO-3-Wächter, `pytest.ini` ergänzt; davor 0.4 (ROADMAP-Wächter eingefroren), 0.5 (INDEX-Luft) und 0.8 (Register-Luft) gebaut — DO-2 vollständig; erster Block)
---
# Phase 10.5 — Finishing

> **Auftrag:** P10.5 schließt jede Baustelle, die im Register als „Ziel P10.5" steht — Betrieb, Fehler, Parität, Performance, MCP-Schicht, Anbieter-Unabhängigkeit, Darstellung, Gehirnkarte, Umbenennen, Suche, Realtime, Editor Stufe 1+2 und Doku. Die Phase endet erst, wenn ein Nicht-Claude-Client live `list_spaces` ausführt, mit zwei Modellanbietern (P10-J); neues Feature kommt erst in P11.

## Freigaben

| Was | Wann | Wer |
|---|---|---|
| Plan `docs/concepts/phase10_5_finishing_plan.md` (Locks P10.5-A–W) | 2026-10-21 | Nikinger |
| Register-Tor **P10-8** — die Spalte „Ziel" wird verbindlich, abgehakt wird im Register | 2026-10-21 | Nikinger |
| **P10-C** — Eingriff in `phase4_auth/` (Lock **P10.5-O**): Loopback-Redirect mit Port, `application_type`, CSP `form-action` | 2026-10-21 | Nikinger |
| **P10.5-N** — P10-I in **beiden** Richtungen: kein Item wandert *in* einen fremden Home-Space hinein **und** nicht *aus* einem heraus | 2026-10-21 | Nikinger |
| Kontextgrenze **400.000** für `MiniMax-M3` und `MiniMax-M3.1-Flash` (P10.5-C, gesetzt von eurofyx-fleet, Neustart 22.10.) | 2026-10-22 | eurofyx-fleet |

## Modulstatus

| Block | Inhalt (Register) | Wer | Deploy | Status |
|---|---|---|---|---|
| 0 | Haushalt: Verifikation, Phase-Head, INDEX-Luft, Register-Luft, DO-2, DO-3, Ausführer-Vorbedingung | Claude Code | — | ✅ 2026-10-22 — 0.1–0.8 gebaut, Abnahme P10.5-1–4 ✅ |
| 1 | Betrieb: BT-1, BT-2, BT-6 (+ `constraints.txt`) | Ausführer + Nikinger | A | ⬜ |
| 2 | Fehler, Parität, Regel: BG-1, RE-1, RE-2, P10-I, AL-1 | Ausführer (+ Claude Code Proben) | A | ⬜ |
| 3 | Hygiene: LG-8 (P1-15), LG-7 | Ausführer | A | ⬜ |
| 4 | Performance: PF-1, PF-4, Z1–Z4 | Ausführer (+ Claude Code Proben) | A | ⬜ |
| 5 | MCP-Schicht: PA-5 (FastMCP 4), LG-4 | Ausführer | B | ⬜ |
| 6 | Anbieter: PA-1, PA-2, `/mcp`, PA-6, P10-J | Ausführer + Claude Code + Nikinger | B | ⬜ |
| 7 | Darstellung: UI-1–UI-6, KA-5 | Ausführer (+ Claude Code Sichtung) | C | ⬜ |
| 8 | Karte: Gehirnkarte C2 | Ausführer (+ Claude Code Smoke/Sichtung) | C | ⬜ |
| 9 | Rechte und Namen: RE-7 (P1-12), RE-4 (P1-13), RE-3 (P1-14) | Ausführer | D | ⬜ |
| 10 | Suche und Realtime: LG-1, LG-2 | Ausführer (+ Claude Code Proben) | D | ⬜ |
| 11 | Editor Stufe 1 + 2: ED-1, ED-2, ED-3 (P1-11), ED-5 | Ausführer (+ Claude Code Proben/Sichtung) | D | ⬜ |
| 12 | Doku und Altlasten: DO-1, LG-6, AL-1 (Rest), AL-3, BG-2/BG-3 | Claude Code | — | ⬜ |
| Z | Closeout P10.5 (Handover, Grafik, Rotationen) | Claude Code + Nikinger | — | ⬜ |

## Deploy-Tabelle

| # | Version | SHA | `health_gate` | Ausgabe |
|---|---|---|---|---|
| A | `v3.1.5` | — | — | nach Block 1–4 |
| B | `v3.1.6` | — | — | nach Block 5–6 |
| C | `v3.1.7` | — | — | nach Block 7–8 |
| D | `v3.1.8` | — | — | nach Block 9–11 |

**Ein Deploy ist vier Schritte, kein Commit** (Plan §2.5): volle Suite + `doc_health` + `ui_budget` grün · Badge und `docs/UPDATE_LOG.md` · Commit + Push · **`deploy.sh` durch den Nikinger** (Hard Rule 9) · `health_gate.sh` mit **echter Ausgabe** in den Commit — nie die Behauptung.

## Abnahmestand

**61 Zeilen** (P10.5-1–61). Zählregel (Plan §5): ✅ erfüllt mit Beleg am Ort · ⚠️ erfüllt in anderer Form, Abweichung benannt · ⬜ offen. Die Kriterien stehen wortgleich im Plan (je Block am Ende); die **Belegte** stehen im Commit und im Session-Block.

| # | Kriterium | Status | Beleg |
|---|---|---|---|
| P10.5-1 | Step-0-Bericht steht im Session-Block, `doc_health` 0 | ✅ | d5f6081 · doc_health 0 |
| P10.5-2 | DO-2: INDEX ≥ 3.000 B unter der Grenze; ROADMAP-Wächter eingefroren; **[Nachtrag 2026-10-21]** Register ≥ 3.000 B unter der Grenze (0.8); Suite grün | ✅ | d5f6081 · 3e15f9e · f7ad5d9 |
| P10.5-3 | DO-3: Wächter grün auf dem echten Head | ✅ | dieser Commit |
| P10.5-4 | Ausführer-Vorbedingung erfüllt und protokolliert (≤ 400 K) | ✅ | dieser Commit |
| P10.5-5 | BT-1: Vorlage trägt die Live-Werte (V199 ✅) | ⬜ | — |
| P10.5-6 | BT-2: Unit installiert, `Result=success` bei Exit 143 (V200 ✅) | ⬜ | — |
| P10.5-7 | `constraints.txt` = Live-Stand; Dev-venv daraus grün; Wächter grün | ⬜ | — |
| P10.5-8 | BG-1: Die Liste füllt sich, sobald das verzögerte `/overview` ankommt, ohne Panel neu zu öffnen | ⬜ | — |
| P10.5-9 | RE-1/RE-2: dieselbe Matrix auf Web und MCP | ⬜ | — |
| P10.5-10 | P10-I auf beiden Flächen durchgesetzt | ⬜ | — |
| P10.5-11 | AL-1: Zeilen 14 und 29 geschlossen; Zeile 15 mit Weg beim Nikinger (Migration + Live-Check) | ⬜ | — |
| P10.5-12 | EXIF weg nach Upload über Web **und** MCP; Orientierung bleibt | ⬜ | — |
| P10.5-13 | Verwaiste Asset-Ordner werden gefunden und nur auf Wunsch in den Papierkorb verschoben | ⬜ | — |
| P10.5-14 | Z1 im Bench: Median ≤ 300 ms (heute 2.405 ms) | ⬜ | — |
| P10.5-15 | Parität: neue Zähler = alte `search().total` je Eimer | ⬜ | — |
| P10.5-16 | Z2: kein Request wartet hinter `/overview` | ⬜ | — |
| P10.5-17 | Z3/Z4: Gerüst ≤ 1 s; Ladezustand genau ab 200 ms | ⬜ | — |
| P10.5-18 | Live nach Deploy A: `/overview` Waiting ≤ 300 ms, Space-Wechsel während des Polls ≤ 1 s (Nikinger, DevTools, beide Eingänge) | ⬜ | — |
| P10.5-19 | Suite grün mit Compat aus; Pin = installiert; `constraints.txt` neu erzeugt und Wächter grün | ⬜ | — |
| P10.5-20 | Beide Ären in-process: `legacy` → `2025-11-25`, `auto` → `2026-07-28`, `list_spaces` ok | ⬜ | — |
| P10.5-21 | LG-4: Tests + Smoke 17/17 | ⬜ | — |
| P10.5-22 | Live nach Deploy B: claude.ai-Connector `list_spaces`/`search_items`/`get_item`/`update_item` ok (Nikinger); Log-Feld `proto` zeigt die Ära (V208) | ⬜ | — |
| P10.5-23 | DCR: `native`/fehlend + `http://127.0.0.1:<port>/…` angenommen; `web` + Loopback, `localhost`, `[::1]`, ohne Port, `http://` fremd → abgelehnt; https-Regeln unverändert | ⬜ | — |
| P10.5-24 | V197: Chromium folgt dem Consent-Redirect zu 127.0.0.1 | ⬜ | — |
| P10.5-25 | `/mcp` ohne Slash: 200 mit Bearer, 401 ohne; kein 307 | ⬜ | — |
| P10.5-26 | Wegwerf-E2E: opencode führt `list_spaces` aus | ⬜ | — |
| P10.5-27 | **Live P10-J Lauf 1** (M3.1 Flash) | ⬜ | — |
| P10.5-28 | **Live P10-J Lauf 2** (lokales Modell, CT 111) — mit 27 die Abschlussbedingung der Phase | ⬜ | — |
| P10.5-29 | UI-1: HTML-404 für unbekannte `/ui`-Pfade | ⬜ | — |
| P10.5-30 | UI-2: Logo an beiden Stellen + Favicon aus einer Datei | ⬜ | — |
| P10.5-31 | UI-3: deutscher Titel je Ansicht (V120 ✅) | ⬜ | — |
| P10.5-32 | UI-4: Sichtungsliste abgearbeitet (Nikinger bestätigt) | ⬜ | — |
| P10.5-33 | UI-5: Kontrast ≥ 4,5:1 | ⬜ | — |
| P10.5-34 | UI-6: Filter in API und UI | ⬜ | — |
| P10.5-35 | KA-5 sichtbar auf Übersicht und Karte | ⬜ | — |
| P10.5-36 | 200 Knoten: Ruhe ≤ 3 s, Frame p95 ≤ 16,7 ms | ⬜ | — |
| P10.5-37 | C2-Stil: Lappen, Furchen, Zellen, Aktivierung (Nikinger-Sichtung) | ⬜ | — |
| P10.5-38 | KA-2: Layout überlebt das Neuladen | ⬜ | — |
| P10.5-39 | KA-3: Suche/Filter/Titel | ⬜ | — |
| P10.5-40 | reduced motion: statisch, 0 Ticks | ⬜ | — |
| P10.5-41 | RE-7: `created_by` auf neuen Items über Web und MCP sichtbar | ⬜ | — |
| P10.5-42 | RE-4 atomar (V193 ✅): ein Commit, Versionen unverändert, Freigabe wandert mit | ⬜ | — |
| P10.5-43 | RE-3 nur Team-Space (V194 ✅): Frontmatter = Verzeichnis, ein Commit, Absturz wird wiederaufgenommen | ⬜ | — |
| P10.5-44 | P1-Diff nennt nur die angekündigten Dateien | ⬜ | — |
| P10.5-45 | LG-1: Volltext in der UI | ⬜ | — |
| P10.5-46 | Realtime: Änderung ≤ 2 s sichtbar | ⬜ | — |
| P10.5-47 | P10.5-S: geänderter Editor nie überschrieben; Neuladen trägt frische `version` | ⬜ | — |
| P10.5-48 | Shutdown ≤ 10 s mit offenen Streams | ⬜ | — |
| P10.5-49 | Live nach Deploy D: Ereignisse kommen über **beide** Eingänge an (V212 ✅) | ⬜ | — |
| P10.5-50 | Budget: Erstaufruf ≤ 250 KB, Editor ≤ 80 KB, jede Datei gezählt | ⬜ | — |
| P10.5-51 | ED-1: kein Moduswechsel, Live-Darstellung (Nikinger-Sichtung) | ⬜ | — |
| P10.5-52 | Roundtrip 10/10 byte-identisch, Öffnen macht nie „geändert" | ⬜ | — |
| P10.5-53 | ED-2: Klick bei sauberem Editor schreibt mit `version`; bei geändertem nur Puffer | ⬜ | — |
| P10.5-54 | ED-3: Vokabular gerendert, unbekannte Klasse wörtlich; `get_item` zeigt Rohtext | ⬜ | — |
| P10.5-55 | ED-5: Rohtext-Schalter zeigt jedes Zeichen | ⬜ | — |
| P10.5-56 | P1-11 dokumentiert; `git diff -- phase1_storage/storage` für ED-3 leer | ⬜ | — |
| P10.5-57 | keine 📗/🔄/🟡-Datei > 40 KB (`doc_health` 0, Oversize-`find`) | ⬜ | — |
| P10.5-58 | `ROADMAP.md` < 30 KB, Wächter grün | ⬜ | — |
| P10.5-59 | Register-Bilanz per Skript, jede P10.5-Zeile mit Beleg | ⬜ | — |
| P10.5-60 | P10-J zweimal live belegt | ⬜ | — |
| P10.5-61 | Closeout-Dokumente + Rotationen per Skript | ⬜ | — |

**Summe:** 4 ✅ · 0 ⚠️ · 57 ⬜ (von 61).

## Offen beim Nikinger

- **V199** — Block 1.1: `curl localhost:2019/config/` auf dem VPS, unmittelbar bevor die Caddy-Vorlage nachzieht (BT-1). Die Ausgabe gehört in den Session-Block.
- **V200** — Block 1.3: `sudo systemctl stop sharefyx-tail-proxy` und `systemctl show … -p Result -p ExecMainStatus`; der Domain-Weg ist dabei für Sekunden weg, das ist vorher anzukündigen.
- **V203** — Funnel-Pfad von außen gewacht? (BT-10, Klärung eurofyx-fleet).
- **P10.5-27/28** — Live-Abnahme P10-J: zwei Modellanbieter, ein Server, ein Werkzeug (`list_spaces`) — Block 6 und Z.
- **Block 2, Zeile 15 (AL-1)** — Migration + Live-Check beim Nikinger.

## Session stopped — 2026-10-22 (erster Block: Block 0 — Haushalt und Vorbereitung, **abgeschlossen**)

**Ergebnis.** Block 0 abgeschlossen, **DO-2 vollständig erledigt:** Karte `docs/INDEX.md` 37.946 B (3.014 B Luft gegen 40.960 B, vorher 188 B), Register 37.574 B (3.386 B Luft, vorher 6 B), ROADMAP-Wächter P9-6 eingefroren. **Ein Plan-Befund:** der Hebel des Plans (die acht Abschnittsköpfe, zusammen 2.478 B) hätte allein **nicht** gereicht — die geforderten 3.000 B waren daraus nicht erreichbar; der Zielwert blieb, der Hebel wurde erweitert (zwei Abweichungen im Plan-Nachtrag).

**Geliefert (Commits).** `d5f6081` — 0.5: Skript `shorten_index_headings.py` (vier Gegenproben) + Archiv `docs/INDEX_KURZUNG_ARCHIVE.md`, Karte 40.772 → 36.601 B. `3e15f9e` — 0.8: §12 des Registers verbatim nach `phase10_inventory/ENTSCHEIDUNGEN_ARCHIVE.md`. `f7ad5d9` — 0.4: P9-6 eingefroren + Gegenprobe, DO-2 → `✅ 10.5-2 (B0)`. `3586566` — 0.2/0.3: Phase-Head, `SESSIONS_ARCHIVE.md`, DO-3-Wächter, `pytest.ini`. `9ad1c22` — 0.6/0.7: ROADMAP-Zeile + 🔄, Kette rotiert, Ausführer-Vorbedingung protokolliert.

**Gemessen.** `doc_health` **0**; volle Suite **1268 → 1270 → 1279 grün** (289/284/281 s). Neu: `test_index_shortening.py` **5/5** (Rundeweg byteweise, Abbruch ohne Zielberührung) und `test_head_rules.py` **4/4** (ein Session-Block ≤ 4 KiB, Gegenprobe mit 5-KiB-Block).

**Ausführer-Daten.** Modell **MiniMax M3.1 Flash** über opencode (P10.5-B, Open-Test) — wirksamer `limit.context` **400.000** (`~/.config/opencode/opencode.json`, für `MiniMax-M3` und `MiniMax-M3.1-Flash`), von eurofyx-fleet gesetzt (Neustart 22.10.); **P10.5-C ist erfüllt**, Block 1 darf starten. Aufrufe/Kontingent: **nicht sichtbar**. Wanduhrzeit: rund **2 h** für 0.1–0.8. Eingriffe: **1** vom Nikinger (Rollenfrage; Antwort: ich baue Block 0 selbst — die Abweichung von Lock P10.5-D ist datiert festgehalten), **0** von Claude Code. Trailer je Commit: `Co-Authored-By: opencode/MiniMax-M3.1-Flash <noreply@minimax.io>`.

**Gegenlese-Funde.** (1) der Plan-Hebel zu klein (oben); (2) ein falsch gebauter `updated:`-Faden im Plan („ | updated: 2026-10-21") — vom Wächter `test_updated_chain.py` gefangen; (3) ein Syntaxfehler im eigenen Skript (ein gerades `"` in einem deutschen Zitat); (4) ein Test rot nach der Kürzung der Archiv-Größe (45.703 B stand in der Abbildung statt 46.456 B); (5) **ein Paketnamenskonflikt:** `phase10_5_finishing/tests/__init__.py` (vom Plan verlangt) heißt das Modul `tests` — wie `phase3_edge/tests` —, die Sammlung brach mit `ModuleNotFoundError` ab, gelöst mit `phase10_5_finishing/__init__.py`; (6) **für Block 12:** die `updated:`-Kette der Wurzel-`CLAUDE.md` trägt **20.532 B von 33.226 B** (am 2026-09-13 rotiert: 47.094 → 23.007 B, seither wieder gewachsen) — unter der Grenze, aber dieselbe Form wie LG-6.

**Offen / nächster Schritt — Block 1 (Betrieb: BT-1, BT-2, BT-6).** Start mit **1.1 V199** (Ausgabe des Nikinger): `curl -s localhost:2019/config/ | python3 -m json.tool | grep -nE 'dial_timeout|try_duration|try_interval' | head -20` auf dem VPS — erwartet 10 s / 15 s / 1 s; weicht ein Wert ab, zieht die Vorlage die **Live**-Werte nach. Danach: **1.2** `phase9_hardening/step_a/Caddyfile.template:65` → Blockform; drei Tests in `test_tail_proxy.py` lernen sie (`:294`, `:325`, `:389`), neu `test_the_upstream_block_carries_the_fleet_timeouts()`. **1.3** `phase3_edge/systemd/sharefyx-tail-proxy.service`: `SuccessExitStatus=143` unter `Restart=on-failure` + Test; **Installation ist Nikinger-Arbeit** (Hard Rule 9), danach V200. **1.4** `pip freeze --exclude-editable` aus `/opt/sharefyx/current/.venv` (lesbar, gemessen) → `constraints.txt`; `scripts/dev_install.sh` mit `-c`; Wächter in `test_step_h_deps.py`; **Dev-venv neu aufsetzen** (vorher sichern, danach volle Suite). Erlaubte Pfade: Plan §3. **Danach Deploy A (`v3.1.5`)** — Badge, `docs/UPDATE_LOG.md`, Commit, `deploy.sh` **durch den Nikinger**, `health_gate.sh` mit echter Ausgabe (Plan §2.5). Abnahme P10.5-5/6/7.
