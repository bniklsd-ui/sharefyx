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
updated: 2026-10-22 (Block 2 Schritte 2.1–2.2: eine Regel für Web und MCP — SharePolicy mit Home-Space-Prädikat, RE-1 Ordner anlegen, RE-2 Ordner wechseln, P10-I/P10.5-N beide Richtungen; Suite 1296 grün) | 2026-10-22 (Block 2 Schritt 2.1: SharePolicy kennt Home-Spaces und Team-Spaces, Prädikat aus der Auth-DB, eine Regel für Web und MCP) | 2026-10-22 (Block 1 **abgeschlossen**: V200 vom Fleet-Lauf belegt — Unit installiert, `Result=success`, 0 failed units; Abnahme 10-5/6/7 ✅) | 2026-10-22 (Block 1 Schritte 1.1/1.2: BT-1 — Caddy-Vorlage in Blockform mit den V199-Live-Werten (10s/15s/1s) + neuer Waechter; Abnahme 10-5 auf ✅) | 2026-10-22 (Block 1 Schritt 1.4: BT-6 — `constraints.txt` aus dem Live-Freeze, `scripts/dev_install.sh` mit `-c`, zwei Wächter, Dev-venv neu; Suite 1282 gruen auf den Live-Versionen) | 2026-10-22 (Block 1 Schritt 1.3: BT-2 — `SuccessExitStatus=143` in der Relay-Unit, Wächter 13/13, vier Gegenläufe; Block-0-Block rotiert) | 2026-10-22 (Block 0 **abgeschlossen**: 0.6 ROADMAP-Zeile P10.5 auf 🔄, 0.7 Ausführer-Vorbedingung protokolliert — Abnahme P10.5-1–4 ✅) | 2026-10-22 (Block 0: 0.2/0.3 — Phase-Head angelegt (Modulstatus, Deploy-Tabelle, Abnahmestand 61 Zeilen), DO-3-Wächter, `pytest.ini` ergänzt; davor 0.4 (ROADMAP-Wächter eingefroren), 0.5 (INDEX-Luft) und 0.8 (Register-Luft) gebaut — DO-2 vollständig; erster Block)
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
| 1 | Betrieb: BT-1, BT-2, BT-6 (+ `constraints.txt`) | Ausführer + Nikinger | A | ✅ 2026-10-22 — **1.1–1.4 gebaut und abgenommen** (V199 gelesen · BT-1 Caddy-Blockform · BT-2 `SuccessExitStatus=143`, live V200 ✅ · BT-6 `constraints.txt`); Abnahme 10-5/6/7 ✅, Suite 1283 grün |
| 2 | Fehler, Parität, Regel: BG-1, RE-1, RE-2, P10-I, AL-1 | Ausführer (+ Claude Code Proben) | A | 🔄 2026-10-22 — **2.1 + 2.2 gebaut** (eine Regel für Web und MCP: RE-1 Ordner anlegen, RE-2 Ordner wechseln, P10-I/P10.5-N kein Verschieben in **oder aus** einem fremden Home-Space); 2.3 (BG-1), 2.4 (Tests mit den Regeln), 2.5 (Proben, Claude Code) offen |
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
| P10.5-5 | BT-1: Vorlage trägt die Live-Werte (V199 ✅) | ✅ | 1.2 · this commit · V199: dial_timeout 10 s · try_duration 15 s · try_interval 1 s |
| P10.5-6 | BT-2: Unit installiert, `Result=success` bei Exit 143 (V200 ✅) | ✅ | 1.3 · Fleet-Lauf 2026-10-22: `Result=success`, 0 failed units, active |
| P10.5-7 | `constraints.txt` = Live-Stand; Dev-venv daraus grün; Wächter grün | ✅ | 1.4 · this commit · Freeze byte-identisch zur Datei, Suite 1282 grün auf `mcp 1.30.0` / `starlette 1.7.0` |
| P10.5-8 | BG-1: Die Liste füllt sich, sobald das verzögerte `/overview` ankommt, ohne Panel neu zu öffnen | ⬜ | — |
| P10.5-9 | RE-1/RE-2: dieselbe Matrix auf Web und MCP | ⬜ | 2.2 gebaut (beide Flächen) · Probe 2.5 offen |
| P10.5-10 | P10-I auf beiden Flächen durchgesetzt | ⬜ | 2.2 gebaut (P10-I + P10.5-N) · Probe 2.5 offen |
| P10.5-11 | AL-1: Zeilen 14 und 29 geschlossen; Zeile 15 mit Weg beim Nikinger (Migration + Live-Check) | ⬜ | 2.2 gebaut (Zeilen 14/29 als Probe vorbereitet) · Probe 2.5 offen; Zeile 15 beim Nikinger |
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

**Summe:** 7 ✅ · 0 ⚠️ · 54 ⬜ (von 61).

## Offen beim Nikinger

- ~~**V199**~~ ✅ 2026-10-22 (Block 1.1) — Live-Werte auf dem VPS: `dial_timeout` 10 s, `try_duration` 15 s, `try_interval` 1 s, Upstream `100.93.43.122:8765`. Die Vorlage trägt jetzt genau diese Werte.
- ~~**V200**~~ ✅ 2026-10-22 (Block 1.3) — Fleet-Playbook auf VM 200: `ok=11 changed=3 failed=0`, `sharefyx-tail-proxy` **active** mit `SuccessExitStatus=143`, nach dem Stopp **`Result=success`**, **0 failed units**, zweiter `--check` meldet `changed=0`. **Nicht gemessen:** der Domain-Weg während des Stopps (der Stopp dauerte Sekunden; der öffentliche Pfad war nicht beteiligt). Die alte Unit liegt als Kopie mit Suffix `~` unter `/etc/systemd/system/` — systemd liest sie nicht.
- **V203** — Funnel-Pfad von außen gewacht? (BT-10, Klärung eurofyx-fleet).
- **P10.5-27/28** — Live-Abnahme P10-J: zwei Modellanbieter, ein Server, ein Werkzeug (`list_spaces`) — Block 6 und Z.
- **Block 2, Zeile 15 (AL-1)** — Migration + Live-Check beim Nikinger.

## Session stopped — 2026-10-22 (Block 2 — Fehler, Parität, Regel: BG-1, RE-1, RE-2, P10-I; **in Arbeit**, Schritte 2.1 und 2.2 gebaut)

**Ergebnis.** Schritte 2.1 und 2.2 stehen: **eine** Regel für Web und MCP. `SharePolicy` kennt
Home-Spaces (ein Space, der einem Nutzer gehört) und Team-Spaces (ein geteilter Space, der
niemandem gehört); die Policy bekommt dafür ein Prädikat (`is_home_space`), das
`mcpserver/app.py :: create_app()` aus der Auth-DB setzt (`oauth.store.get_user(space) is not
None` — Zeilenabfrage **ohne** TOTP-Entschlüsselung). `webui/api.py :: _is_team_space()` und
`_team_writer()` sind Einzeiler auf die Policy — die Home-Space-Abfrage gibt es im Code nur
noch **einmal**. Durchgesetzt: **RE-1** (Ordner anlegen im Team-Space, Web), **RE-2** (Ordner
wechseln im Team-Space, MCP), **P10-I** (kein Item wandert in den Home-Space eines anderen) und
**P10.5-N** (auch nicht **aus** einem heraus — Nikinger 2026-10-21).

**Fail-closed (Plan Block 2):** ohne Prädikat kennt die Policy **keinen** Home-Space — und
damit auch keinen Team-Space. Wer kein Prädikat liefert, sperrt sich selbst.

**Ein Plan-Befund, datiert:** Schritt 2.4 („Tests") ist kein eigener Commit — die Tests kamen
mit ihrer Regel (2.1/2.2), sonst gäbe es einen Commit mit Code ohne Beweis. Und: die
Test-Fixtures brauchten das Prädikat **auch** dort, wo es die Regel noch nicht prüft (webui,
P7) — ohne Prädikat hätten die Web-Tests nach der Umstellung **keine** Team-Spaces mehr.

**Geliefert (Commits).** `4f6e878` — 2.1. (dieser Commit) — 2.2: `mcpserver/tools.py`
(RE-2, P10-I), `webui/api.py` (RE-1, P10-I), `PermissionDenied` mit optionalem Grund,
`test_tools.py` 77 → 81, `test_app.py` 15 → 17, `test_api.py` 79 → 82.

**Gemessen.** Suite **1296 grün** (276 s). `doc_health` 0. **Sieben Gegenläufe, alle
wirksam:** alte Web-Regel → Ordner-Test rot · P10-I-Prüfung entfernt → zwei Move-Tests rot ·
alte MCP-Regel → RE-2-Test rot · MCP-P10-I entfernt → zwei Tests rot · Quellseite aus
`may_move_between()` gestrichen → drei Tests rot · Ereignis aus `list.js` entfernt →
Wächter rot · Prädikat aus `app.py` entfernt → zwei Integrations-Tests rot.

**Ein Test musste umgeschrieben werden, mit Begründung:** `test_update_item_with_space_and_
folder_together_uses_space_level_check_not_owner_guard` (2026-08-17, Advisor-Fund) schob ein
Item aus dem Home-Space `alpha` heraus — das verbietet P10.5-N jetzt. Der Testzweck (der
Eigentümer-Riegel darf einen legitimen Cross-Space-Move mit `folder=` nicht blockieren) bleibt,
die Quelle ist jetzt ein Team-Space.

**Ausführer-Daten.** **MiniMax M3.1 Flash** über opencode (P10.5-B), `limit.context`
**400.000** (P10.5-C ✅). Wanduhrzeit: rund **1 h 10 min** für 2.1–2.2. Aufrufe/Kontingent:
**nicht sichtbar**. Eingriffe: **0** vom Nikinger, **0** von Claude Code. Trailer je Commit:
`Co-Authored-By: opencode/MiniMax-M3.1-Flash <noreply@minimax.io>`.

**Offen / nächster Schritt.** **2.3** (BG-1: die Space-Liste füllt sich, wenn das verzögerte
`/overview` ankommt) · **2.4** (Tests mit den Regeln) · **2.5** (Proben: Wegwerf, zwei
Principale + ein Team-Space — **Claude Code**). Abnahme 10-9/10-10/10-11 bleiben ⬜, bis die
Probe läuft.
