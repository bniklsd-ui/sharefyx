---
status: archive
purpose: L3-Archiv der älteren Session-Blöcke des Phase-10.5-Heads — verbatim, newest-first
read-when: beim Audit, wenn der Stand eines früheren Blocks dieser Phase gebraucht wird
detail: L3
up: ./CLAUDE.md
down:
updated: 2026-10-22 (Block 1, Schritt 1.3: erster Block rotiert — der Block-0-Block vom 2026-10-22, verbatim) | 2026-10-22 (angelegt — P10.5 Block 0, Schritt 0.2; noch kein Block rotiert, der erste steht im Head)
---
# Phase 10.5 — Session-Archiv

Hier stehen die älteren `## Session stopped`-Blöcke des Phase-10.5-Heads, **verbatim** und
newest-first — der neueste Block steht im Head (`../CLAUDE.md`), dieser Abschnitt trägt die Chronik.

**Warum es ein Archiv gibt:** die Doc-Layers-Konvention verlangt genau **einen** Session-Block pro
Phase-Head (Rotationsregel ab Tag 1, `scripts/rotate_session_block.sh`). Wer einen älteren Block
sucht, findet ihn hier — nicht im Head.

**Größe:** jeder Block ist auf **4 KiB** begrenzt (Lock P10.5-T, DO-3), geprüft von
`phase10_5_finishing/tests/test_head_rules.py`. Das ist die Lehre aus Phase 9: die alten Blöcke
trugen 10–17 KB, das P9-Archiv wuchs auf 396 KB — der teuerste Abschnitt einer Datei, den jede
Lesesitzung zuerst liest.
## Session stopped — 2026-10-22 (erster Block: Block 0 — Haushalt und Vorbereitung, **abgeschlossen**)

**Ergebnis.** Block 0 abgeschlossen, **DO-2 vollständig erledigt:** Karte `docs/INDEX.md` 37.946 B (3.014 B Luft gegen 40.960 B, vorher 188 B), Register 37.574 B (3.386 B Luft, vorher 6 B), ROADMAP-Wächter P9-6 eingefroren. **Ein Plan-Befund:** der Hebel des Plans (die acht Abschnittsköpfe, zusammen 2.478 B) hätte allein **nicht** gereicht — die geforderten 3.000 B waren daraus nicht erreichbar; der Zielwert blieb, der Hebel wurde erweitert (zwei Abweichungen im Plan-Nachtrag).

**Geliefert (Commits).** `d5f6081` — 0.5: Skript `shorten_index_headings.py` (vier Gegenproben) + Archiv `docs/INDEX_KURZUNG_ARCHIVE.md`, Karte 40.772 → 36.601 B. `3e15f9e` — 0.8: §12 des Registers verbatim nach `phase10_inventory/ENTSCHEIDUNGEN_ARCHIVE.md`. `f7ad5d9` — 0.4: P9-6 eingefroren + Gegenprobe, DO-2 → `✅ 10.5-2 (B0)`. `3586566` — 0.2/0.3: Phase-Head, `SESSIONS_ARCHIVE.md`, DO-3-Wächter, `pytest.ini`. `9ad1c22` — 0.6/0.7: ROADMAP-Zeile + 🔄, Kette rotiert, Ausführer-Vorbedingung protokolliert.

**Gemessen.** `doc_health` **0**; volle Suite **1268 → 1270 → 1279 grün** (289/284/281 s). Neu: `test_index_shortening.py` **5/5** (Rundeweg byteweise, Abbruch ohne Zielberührung) und `test_head_rules.py` **4/4** (ein Session-Block ≤ 4 KiB, Gegenprobe mit 5-KiB-Block).

**Ausführer-Daten.** Modell **MiniMax M3.1 Flash** über opencode (P10.5-B, Open-Test) — wirksamer `limit.context` **400.000** (`~/.config/opencode/opencode.json`, für `MiniMax-M3` und `MiniMax-M3.1-Flash`), von eurofyx-fleet gesetzt (Neustart 22.10.); **P10.5-C ist erfüllt**, Block 1 darf starten. Aufrufe/Kontingent: **nicht sichtbar**. Wanduhrzeit: rund **2 h** für 0.1–0.8. Eingriffe: **1** vom Nikinger (Rollenfrage; Antwort: ich baue Block 0 selbst — die Abweichung von Lock P10.5-D ist datiert festgehalten), **0** von Claude Code. Trailer je Commit: `Co-Authored-By: opencode/MiniMax-M3.1-Flash <noreply@minimax.io>`.

**Gegenlese-Funde.** (1) der Plan-Hebel zu klein (oben); (2) ein falsch gebauter `updated:`-Faden im Plan („ | updated: 2026-10-21") — vom Wächter `test_updated_chain.py` gefangen; (3) ein Syntaxfehler im eigenen Skript (ein gerades `"` in einem deutschen Zitat); (4) ein Test rot nach der Kürzung der Archiv-Größe (45.703 B stand in der Abbildung statt 46.456 B); (5) **ein Paketnamenskonflikt:** `phase10_5_finishing/tests/__init__.py` (vom Plan verlangt) heißt das Modul `tests` — wie `phase3_edge/tests` —, die Sammlung brach mit `ModuleNotFoundError` ab, gelöst mit `phase10_5_finishing/__init__.py`; (6) **für Block 12:** die `updated:`-Kette der Wurzel-`CLAUDE.md` trägt **20.532 B von 33.226 B** (am 2026-09-13 rotiert: 47.094 → 23.007 B, seither wieder gewachsen) — unter der Grenze, aber dieselbe Form wie LG-6.

**Offen / nächster Schritt — Block 1 (Betrieb: BT-1, BT-2, BT-6).** Start mit **1.1 V199** (Ausgabe des Nikinger): `curl -s localhost:2019/config/ | python3 -m json.tool | grep -nE 'dial_timeout|try_duration|try_interval' | head -20` auf dem VPS — erwartet 10 s / 15 s / 1 s; weicht ein Wert ab, zieht die Vorlage die **Live**-Werte nach. Danach: **1.2** `phase9_hardening/step_a/Caddyfile.template:65` → Blockform; drei Tests in `test_tail_proxy.py` lernen sie (`:294`, `:325`, `:389`), neu `test_the_upstream_block_carries_the_fleet_timeouts()`. **1.3** `phase3_edge/systemd/sharefyx-tail-proxy.service`: `SuccessExitStatus=143` unter `Restart=on-failure` + Test; **Installation ist Nikinger-Arbeit** (Hard Rule 9), danach V200. **1.4** `pip freeze --exclude-editable` aus `/opt/sharefyx/current/.venv` (lesbar, gemessen) → `constraints.txt`; `scripts/dev_install.sh` mit `-c`; Wächter in `test_step_h_deps.py`; **Dev-venv neu aufsetzen** (vorher sichern, danach volle Suite). Erlaubte Pfade: Plan §3. **Danach Deploy A (`v3.1.5`)** — Badge, `docs/UPDATE_LOG.md`, Commit, `deploy.sh` **durch den Nikinger**, `health_gate.sh` mit echter Ausgabe (Plan §2.5). Abnahme P10.5-5/6/7.

