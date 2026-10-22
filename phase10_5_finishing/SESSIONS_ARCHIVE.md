---
status: archive
purpose: L3-Archiv der älteren Session-Blöcke des Phase-10.5-Heads — verbatim, newest-first
read-when: beim Audit, wenn der Stand eines früheren Blocks dieser Phase gebraucht wird
detail: L3
up: ./CLAUDE.md
down:
updated: 2026-10-22 (Block-3-Block rotiert — Block 4 begonnen: Performance PF-1/PF-4, Z1–Z4) | 2026-10-22 (Block-2.5-Block rotiert — Block-2-Nachzug + Block 3 begonnen) | 2026-10-22 (Block-2-Block (2.1–2.4) rotiert — Block 2.5 Proben) | 2026-10-22 (Block-1-Block rotiert — Block 2 begonnen) | 2026-10-22 (Block 1, Schritt 1.3: erster Block rotiert — der Block-0-Block vom 2026-10-22, verbatim) | 2026-10-22 (angelegt — P10.5 Block 0, Schritt 0.2; noch kein Block rotiert, der erste steht im Head)
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

## Session stopped — 2026-10-22 (Block 2-Nachzug + Block 3 ✅ — RE-1-Parität, EXIF-Strip, Waisen)

**Ergebnis (Nachzug).** Der Befund aus Probe 2.5 ist geschlossen (Nikinger 2026-10-22: „ja"):
ein Item mit **neuem Ordner** in einem fremden Home-Space legt den Ordner nicht mehr an — Web
**und** MCP. Regel: `permissions.manages_space()` (eigener Space oder Team-Space mit
Schreibrecht), dieselbe wie RE-1 und RE-2. Ohne `folder` bleibt das Anlegen an der
Space-Wurzel erlaubt (P6-U). `ui_budget.py`/`ui_smoke.py` bekommen das Home-Space-Prädikat —
ohne es waren ihre `team`-Flags **immer** `false`.

**Ergebnis (Block 3 ✅).** LG-8: `files.strip_image_metadata()` (JPEG/PNG/WebP, GIF unverändert,
**fail-closed**) + Aufruf in `Store.put_asset()` — **eine** Stelle für Web und MCP. LG-7:
`scripts/asset_orphans.py` (`--report`/`--move`, **ein** Commit, nie gelöscht).

**Geliefert (Commits).** 3.1 `files.py` + 8 Tests · 3.2 `store.py` + 9 Tests + die
Dummy-PNG-Fixtures (acht Dateien in fünf Paketen → jetzt **eine** Fixture in
`phase1_storage/tests/sharefyx_image_bytes.py`, `pytest.ini` setzt `pythonpath`) · 3.3/3.4
`asset_orphans.py` + 7 Tests + `probes/p105_b3_assets_probe.py`.

**Gemessen** (Basis `725215f`): `pytest` **1316 grün** (304 s) · **Wegwerf 8799: 14/14 Zellen**
(`probes/p105_b3_assets.json`): Web 148 B → 94 B, GPS weg, Orientation 6 bleibt, ICC bleibt ·
MCP 94 B, GPS weg, Orientation 6 · sauberes Bild byte-identisch (45 B = 45 B) · Waise gefunden
(und nur sie), `--move` → Papierkorb, **ein** Commit (5 → 6), lebende Assets unberührt ·
`doc_health` 0 · `ui_smoke` 13/13 · `ui_budget` 5/5.

**Ausführer-Daten.** opencode/MiniMax-M3.1-Flash · Kontextgrenze 400.000 (P10.5-C erfüllt) ·
keine Advisor-Runde · Eingriffe Nikinger/Claude Code: 0 · kein `systemctl`, kein `sudo`, kein
echter `DATA_ROOT` · Wegwerf-Instanz nur über die PID-Datei gestoppt (Hard Rule 9), Port 8799
danach frei.

**Plan-Drift, datiert 2026-10-22.** (1) Der Plan sagt „im **Index** keine Item-Zeile" — der
Code prüft gegen die **Dateien** (Hard Rule 2): ein veralteter Index würde die Assets
**lebender** Items als verwaist melden und in den Papierkorb schieben. (2) Der Plan sah die
Proben bei Claude Code; ich habe sie selbst gefahren (stehende Erlaubnis, Wegwerf erlaubt).
(3) `pytest.ini` (eine Zeile `pythonpath`) und acht Testdateien in fünf Pakaten wurden
angefasst — die Dummy-PNG-Header waren nach 3.2 **keine Bilder mehr** (fail-closed).
(4) Die Option heißt `--git-author`, nicht `--author`: der P9-Wächter
`test_only_history_builds_the_git_author_arguments` erlaubt das Literal `--author` nur in
`storage/history.py` (dort wird der Git-Autor **gebaut**; das Skript reicht den Namen nur
durch) — der Wächter bleibt unangetastet.

**Abbruchprüfung (P10.5-E, Basis `45c507b`).** `git diff --stat` nennt neben den erlaubten
Pfaden **sechs** Dateien: `phase2_mcp/scripts/mcp_smoke.py` und fünf Testdateien — alle
**Fixture-Reparaturen** (Dummy-PNG → echte Bytes), keine Produktlogik; `pytest.ini` eine
Zeile. P10.5-F ist sauber: unter `phase1_storage/storage` nur `files.py` und `store.py`.

**Offen / nächster Schritt.** Block 4 (Performance: PF-1, PF-4, Z1–Z4) — Deploy A (`v3.1.5`)
danach. Beim Nikinger offen: AL-1 Zeile 15 (Migration + Live-Check), V203, P10.5-27/28.

## Session stopped — 2026-10-22 (Block 2.5 — Proben Web × MCP und M4; Block 2 ✅ mit einem Befund)

**Ergebnis.** Die Regel aus 2.1–2.4 hält auf einer Wegwerf-Instanz. **28 von 28** bewerteten
Zellen bestehen, und jedes ❌ scheitert mit dem **erwarteten Text** (nicht an einer älteren
Prüfung). BG-1 ist behoben. **Ein Befund:** Ein Item mit **neuem** Ordner in einem fremden
Home-Space mit `write:` anzulegen (`create_item(space=, folder=)`, Web `POST /api/v1/items`)
legt den Ordner an — auf **beiden** Flächen. Damit ist die Parität gewahrt, aber RE-1 hat eine
Hintertür. Deshalb steht P10.5-9 auf ⚠️.

**Geliefert (Commits).** Dieser Commit:
- `probes/p105_b2_rights_probe.py`: Wegwerf 8799, eigene Wurzel, Maschinerie aus
  `p10_wegwerf.py`. Seed: alpha · beta (Home B, `write: [alpha]`) · gamma (Team, write) ·
  delta (Team, nur read).
- `probes/p105_m4_bg1_probe.py`: M4 über TLS, Bestehensregel umgedreht.
- Rohwerte in den beiden `.json` daneben.

**Gemessen** (HEAD `b299968`):

| Matrix | Web | MCP |
|---|---|---|
| Ordner anlegen: eigen/Team ✅ · fremder Home mit `write:` ❌ · read-Team ❌ | ✅ | (kein Werkzeug) |
| Ordner wechseln: eigen/Team ✅ · fremder Home ❌ | ✅ | ✅ |
| Verschieben alpha→gamma ✅ (AL-1 Z. 29) · alpha→beta ❌ · beta→alpha ❌ · beta→gamma ❌ | ✅ | ✅ |
| delta schreiben ❌ · fremder Body gewrappt, eigener nicht (AL-1 Z. 14) | ✅ | ✅ |

- Jede ✅-Zelle ist von der Platte zurückgelesen (`<space>/<ordner>/<id>__*.md`).
- Jedes ❌ hat das Item an der Quelle belassen.
- **M4:** 4 s verzögert → 0 Zeilen beim Öffnen, **3 Zeilen** nach der Antwort, ohne neu zu
  öffnen. Gegenlauf ohne Verzögerung: 3.
- **Gegenlauf der Probe:** ohne `dispatchEvent` → 0 nach der Verzögerung. `list.js` ist
  danach per `git checkout` zurück.
- Prod (8765, PID 1069) unberührt; 8799 nach dem Stopp frei.

**Plan-Drift, datiert 2026-10-22** (der Plan ist 📕, deshalb steht die Drift hier):
1. P6-Zeile 14 heißt im Original „fremder Body auch im geteilten Space gewrappt"
   (`phase6_shares_plan.md:919`), nicht „Schreiben ❌". Beides ist geprüft.
2. M4 erwartet 3 statt 2 Zeilen: beta ist hier beschreibbar.
3. Die MCP-Fläche hat kein Werkzeug „Ordner anlegen".

**Ausführer-Daten.** Claude Code (Proben). Eine Advisor-Runde vor dem Bau. Eingriffe: 0.

**Offen / nächster Schritt.**
- **Nikinger:** Den Befund schließen (`create_item`/`POST /items` mit neuem Ordner nur, wenn
  `manages_space()`)? Das ist Code in `tools.py`/`api.py`. Bremst Block 3 nicht.
- **Nikinger:** Die offene Frage zu `ui_budget.py`/`ui_smoke.py` ohne Home-Space-Prädikat.
- **Ausführer (opencode) — Block 3, Startauftrag** (Plan „Block 3", §2.1–§2.2):
  - Vorher: `limit.context` ≤ 400.000 prüfen · `git status` sauber · Blockbasis = HEAD.
  - **Angekündigt hiermit (2026-10-22): P1-Öffnung 15:** `files.strip_image_metadata()` + Aufruf in
    `Store.put_asset()`. Keine weitere Datei unter `phase1_storage/storage/`.
  - 3.1 `strip_image_metadata(data, mime)` in `files.py` (JPEG/PNG/WebP, GIF unverändert,
    fail-closed `ValidationError`) · 3.2 Aufruf in `put_asset()` nach `sniff_image_mime()`
    (heute **`store.py:943`**, Plan sagt 944) · 3.3 `scripts/asset_orphans.py`
    (Docstring V162 heute `store.py:1045`) · Tests nach Plan 3.4, Fixtures als Bytes.
  - Proben P10.5-12/13 (Wegwerf) macht danach Claude Code.

## Session stopped — 2026-10-22 (Block 2 — Fehler, Parität, Regel: BG-1, RE-1, RE-2, P10-I; **2.1–2.4 gebaut**, 2.5 Proben offen)

**Ergebnis.** Die Schritte 2.1–2.4 stehen — **eine** Regel für Web und MCP, und die
Space-Liste füllt sich nach, wenn das `/overview` spät kommt.

**Die Regel.** `SharePolicy` kennt Home-Spaces (ein Space, der einem Nutzer gehört) und
Team-Spaces (ein geteilter Space, der niemandem gehört); die Policy bekommt dafür ein Prädikat
(`is_home_space`), das `mcpserver/app.py :: create_app()` aus der Auth-DB setzt
(`oauth.store.get_user(space) is not None` — Zeilenabfrage **ohne** TOTP-Entschlüsselung).
`webui/api.py :: _is_team_space()` und `_team_writer()` sind Einzeiler auf die Policy — die
Home-Space-Abfrage gibt es im Code nur noch **einmal**. Durchgesetzt: **RE-1** (Ordner anlegen
im Team-Space, Web), **RE-2** (Ordner wechseln im Team-Space, MCP), **P10-I** (kein Item
wandert in den Home-Space eines anderen) und **P10.5-N** (auch nicht **aus** einem heraus —
Nikinger 2026-10-21). **Fail-closed:** ohne Prädikat kennt die Policy **keinen** Home-Space
und damit auch keinen Team-Space — wer kein Prädikat liefert, sperrt sich selbst.

**BG-1 (2.3).** `list.js` feuert nach dem Füllen von `state.spaces` das Ereignis
`sfx:overview-loaded`; `spaces.js` hört darauf und zeichnet die Liste neu, **wenn** das Panel
offen ist (`#settings-spaces` nicht `hidden`). Der Weg läuft über ein Ereignis, nicht über einen
Import — `spaces.js` importiert `loadOverview()` aus `list.js`, ein Import zurück wäre ein
Zyklus.

**Ein Plan-Befund, datiert:** Schritt 2.4 („Tests") ist kein eigener Commit — die Tests kamen
mit ihrer Regel (2.1–2.3), sonst gäbe es einen Commit mit Code ohne Beweis. Und: die
Test-Fixtures brauchten das Prädikat **auch** dort, wo es die Regel noch nicht prüft (webui,
P7) — ohne Prädikat hätten die Web-Tests nach der Umstellung **keine** Team-Spaces mehr.

**Geliefert (Commits).** `4f6e878` — 2.1. `f4c63b6` — 2.2. `486acda` — 2.3 (BG-1). `da92731` —
Wurzel-Current-state (Block-2-Block oben, Block-1-Block per Skript rotiert).

**Gemessen.** Suite **1299 grün** (280 s). `doc_health` 0 · `ui_budget` 5/5 (173,8 KB gzip).
**Sieben Gegenläufe, alle wirksam:** alte Web-Regel → Ordner-Test rot · P10-I-Prüfung
entfernt → zwei Move-Tests rot · alte MCP-Regel → RE-2-Test rot · MCP-P10-I entfernt → zwei
Tests rot · Quellseite aus `may_move_between()` gestrichen → drei Tests rot · Ereignis aus
`list.js` entfernt → Wächter rot · Prädikat aus `app.py` entfernt → zwei Integrations-Tests
rot.

**Ein Bestandstest musste umgeschrieben werden, mit Begründung:** `test_update_item_with_space_
and_folder_together_uses_space_level_check_not_owner_guard` (2026-08-17, Advisor-Fund) schob
ein Item aus dem Home-Space `alpha` heraus — das verbietet P10.5-N jetzt. Der Testzweck (der
Eigentümer-Riegel darf einen legitimen Cross-Space-Move mit `folder=` nicht blockieren) bleibt,
die Quelle ist jetzt ein Team-Space.

**Ausführer-Daten.** **MiniMax M3.1 Flash** über opencode (P10.5-B), `limit.context`
**400.000** (P10.5-C ✅). Wanduhrzeit: rund **55 min** für 2.1–2.4 (11:44 → 12:39), davon
drei volle Suitenläufe (je ≈ 5 min) und sieben Gegenläufe. Aufrufe/Kontingent:
**nicht sichtbar**. Eingriffe: **0** vom Nikinger, **0** von Claude Code. Trailer je Commit:
`Co-Authored-By: opencode/MiniMax-M3.1-Flash <noreply@minimax.io>`.

**Offen / nächster Schritt.** **2.5 — die Proben** (Plan Schritt 2.5, **Claude Code**):
`phase10_5_finishing/probes/p105_b2_rights_probe.py` auf einer Wegwerf-Instanz (zwei Principale
+ ein Team-Space), Matrix Web × MCP, danach M4 erneut gegen die neue Instanz. Abnahme
**10-8/10-9/10-10/10-11** bleiben ⬜, bis die Probe läuft; AL-1 Zeile 15 bleibt beim Nikinger.
Danach: Deploy A (`v3.1.5`) nach Block 3–4.

## Session stopped — 2026-10-22 (Block 1 — Betrieb: BT-1, BT-2, BT-6; **✅ abgeschlossen**)

**Ergebnis.** Block 1 ist fertig: 1.1 (V199) · 1.2 (BT-1, Caddy-Blockform) · 1.3 (BT-2,
`SuccessExitStatus=143`) · 1.4 (BT-6, `constraints.txt`). Abnahme **P10.5-5 ✅ · 10-6 ✅ · 10-7 ✅**.
**Ein Plan-Befund, datiert:** die Schritte stehen als 1.1 → 1.2 → 1.3 → 1.4, aber 1.1/1.2 hängen an
Ausgaben des Nikingers, 1.3/1.4 nicht — deshalb liefen 1.3/1.4 zuerst. **Deploy A ist laut Plan „nach
Block 1–4" fällig, also nicht jetzt.**

**Geliefert (Commits).** `4fc8d9a` — 1.3 (BT-2). `52b4eec` — 1.4 (BT-6). `f3846e8` + `71e904e` — 1.1/1.2
(BT-1). `60a191a` — INDEX-Größe. (dieser Commit) — V200 abgehakt.

**V199 (1.1), Ausgabe des Nikingers auf der VPS:** `dial_timeout` 10000000000 ns (10 s) ·
`try_duration` 15000000000 ns (15 s) · `try_interval` 1000000000 ns (1 s) · `upstreams[0].dial` =
`100.93.43.122:8765` — die Plan-Annahme, und der Upstream passt zu `<heimvm-tailnet>:8765`.

**V200 (1.3), Lauf vom 2026-10-22 (Fleet-Playbook auf VM 200, `ok=11 changed=3 failed=0`):**
`sharefyx-tail-proxy` **active**, trägt `SuccessExitStatus=143`, nach dem Stopp **`Result=success`**,
**0 failed units** — genau das, was der Fleet-Healthcheck liest. Relay auf `100.93.43.122:8765`, App auf
`127.0.0.1:8765`. **Idempotenz: der zweite `--check` meldet `changed=0`.** Die alte Unit liegt als
Kopie mit Suffix `~` in `/etc/systemd/system/` (systemd liest sie nicht). **Nicht gemessen:** der
Domain-Weg während des Stopps — der Stopp-Start dauerte laut Ansible nur Sekunden, und der öffentliche
Pfad war in den Prüfschritten nicht beteiligt.

**Gemessen.** Suite **1283 grün** (308 s) auf `mcp 1.30.0` / `starlette 1.7.0`. `pip check` grün,
`doc_health` 0. **Gegenläufe, alle wirksam (Details in den Commits):** BT-1 — alte Einzeilenform ·
`dial_timeout 3s` · Direktive außerhalb des Blocks. BT-2 — Zeile fehlt · Zahl 144 · Zeile nicht unter
`Restart=on-failure` · Zeile in der MCP-Unit. BT-6 — Wegwerf-venv mit `starlette 1.3.1` · `-c`
entfernt · Abbruchblock entfernt. Die neuen Wächter laufen im **Release-venv** grün (deploy.sh:169) —
sonst bricht Deploy A.

**Ausführer-Daten.** **MiniMax M3.1 Flash** über opencode (P10.5-B), `limit.context` **400.000**
(P10.5-C ✅). Wanduhrzeit: rund **1 h 40 min** für 1.1–1.4 (10:05 → 11:45), davon vier volle
Suitenläufe (je ≈ 5 min). Aufrufe/Kontingent: **nicht sichtbar**. Eingriffe: **2** vom Nikinger
(V199-Ausgabe, V200-Lauf über Fleet), **0** von Claude Code. Trailer je Commit:
`Co-Authored-By: opencode/MiniMax-M3.1-Flash <noreply@minimax.io>`.

**Gegenlese-Funde — zwei eigene Fehler dieser Session.** (1) `cp -a .venv` kopiert die Skriptshebangs
mit — der erste Gegenlauf traf dadurch das **echte** Dev-venv (dort wurde `starlette` auf 1.3.1
heruntergesetzt). Lehre: eine venv-Kopie nur über `venv/bin/python -m pip` anfassen. (2) Die
Verhaltensprobe war grün, ohne den Abbruch zu prüfen — im PATH der Testumgebung gibt es kein
`python`, das Skript endete vorher mit „command not found"; jetzt hat die Probe einen `python`-Stub.

**Offen / nächster Schritt.** **Block 2** (Fehler, Parität, Regel: BG-1, RE-1, RE-2, P10-I, AL-1) —
Zeile 15 (AL-1) bleibt Nikinger-Arbeit. Beim Nikinger offen: der Caddy-Befehl auf der VPS (Fleet
wartet auf eine Einzelfreigabe) — **von Sharefyx wird dort nichts gebraucht**: die Live-Config trägt
die Werte bereits, und die Quelle zieht jetzt nach.

## Session stopped — 2026-10-22 (erster Block: Block 0 — Haushalt und Vorbereitung, **abgeschlossen**)

**Ergebnis.** Block 0 abgeschlossen, **DO-2 vollständig erledigt:** Karte `docs/INDEX.md` 37.946 B (3.014 B Luft gegen 40.960 B, vorher 188 B), Register 37.574 B (3.386 B Luft, vorher 6 B), ROADMAP-Wächter P9-6 eingefroren. **Ein Plan-Befund:** der Hebel des Plans (die acht Abschnittsköpfe, zusammen 2.478 B) hätte allein **nicht** gereicht — die geforderten 3.000 B waren daraus nicht erreichbar; der Zielwert blieb, der Hebel wurde erweitert (zwei Abweichungen im Plan-Nachtrag).

**Geliefert (Commits).** `d5f6081` — 0.5: Skript `shorten_index_headings.py` (vier Gegenproben) + Archiv `docs/INDEX_KURZUNG_ARCHIVE.md`, Karte 40.772 → 36.601 B. `3e15f9e` — 0.8: §12 des Registers verbatim nach `phase10_inventory/ENTSCHEIDUNGEN_ARCHIVE.md`. `f7ad5d9` — 0.4: P9-6 eingefroren + Gegenprobe, DO-2 → `✅ 10.5-2 (B0)`. `3586566` — 0.2/0.3: Phase-Head, `SESSIONS_ARCHIVE.md`, DO-3-Wächter, `pytest.ini`. `9ad1c22` — 0.6/0.7: ROADMAP-Zeile + 🔄, Kette rotiert, Ausführer-Vorbedingung protokolliert.

**Gemessen.** `doc_health` **0**; volle Suite **1268 → 1270 → 1279 grün** (289/284/281 s). Neu: `test_index_shortening.py` **5/5** (Rundeweg byteweise, Abbruch ohne Zielberührung) und `test_head_rules.py` **4/4** (ein Session-Block ≤ 4 KiB, Gegenprobe mit 5-KiB-Block).

**Ausführer-Daten.** Modell **MiniMax M3.1 Flash** über opencode (P10.5-B, Open-Test) — wirksamer `limit.context` **400.000** (`~/.config/opencode/opencode.json`, für `MiniMax-M3` und `MiniMax-M3.1-Flash`), von eurofyx-fleet gesetzt (Neustart 22.10.); **P10.5-C ist erfüllt**, Block 1 darf starten. Aufrufe/Kontingent: **nicht sichtbar**. Wanduhrzeit: rund **2 h** für 0.1–0.8. Eingriffe: **1** vom Nikinger (Rollenfrage; Antwort: ich baue Block 0 selbst — die Abweichung von Lock P10.5-D ist datiert festgehalten), **0** von Claude Code. Trailer je Commit: `Co-Authored-By: opencode/MiniMax-M3.1-Flash <noreply@minimax.io>`.

**Gegenlese-Funde.** (1) der Plan-Hebel zu klein (oben); (2) ein falsch gebauter `updated:`-Faden im Plan („ | updated: 2026-10-21") — vom Wächter `test_updated_chain.py` gefangen; (3) ein Syntaxfehler im eigenen Skript (ein gerades `"` in einem deutschen Zitat); (4) ein Test rot nach der Kürzung der Archiv-Größe (45.703 B stand in der Abbildung statt 46.456 B); (5) **ein Paketnamenskonflikt:** `phase10_5_finishing/tests/__init__.py` (vom Plan verlangt) heißt das Modul `tests` — wie `phase3_edge/tests` —, die Sammlung brach mit `ModuleNotFoundError` ab, gelöst mit `phase10_5_finishing/__init__.py`; (6) **für Block 12:** die `updated:`-Kette der Wurzel-`CLAUDE.md` trägt **20.532 B von 33.226 B** (am 2026-09-13 rotiert: 47.094 → 23.007 B, seither wieder gewachsen) — unter der Grenze, aber dieselbe Form wie LG-6.

**Offen / nächster Schritt — Block 1 (Betrieb: BT-1, BT-2, BT-6).** Start mit **1.1 V199** (Ausgabe des Nikinger): `curl -s localhost:2019/config/ | python3 -m json.tool | grep -nE 'dial_timeout|try_duration|try_interval' | head -20` auf dem VPS — erwartet 10 s / 15 s / 1 s; weicht ein Wert ab, zieht die Vorlage die **Live**-Werte nach. Danach: **1.2** `phase9_hardening/step_a/Caddyfile.template:65` → Blockform; drei Tests in `test_tail_proxy.py` lernen sie (`:294`, `:325`, `:389`), neu `test_the_upstream_block_carries_the_fleet_timeouts()`. **1.3** `phase3_edge/systemd/sharefyx-tail-proxy.service`: `SuccessExitStatus=143` unter `Restart=on-failure` + Test; **Installation ist Nikinger-Arbeit** (Hard Rule 9), danach V200. **1.4** `pip freeze --exclude-editable` aus `/opt/sharefyx/current/.venv` (lesbar, gemessen) → `constraints.txt`; `scripts/dev_install.sh` mit `-c`; Wächter in `test_step_h_deps.py`; **Dev-venv neu aufsetzen** (vorher sichern, danach volle Suite). Erlaubte Pfade: Plan §3. **Danach Deploy A (`v3.1.5`)** — Badge, `docs/UPDATE_LOG.md`, Commit, `deploy.sh` **durch den Nikinger**, `health_gate.sh` mit echter Ausgabe (Plan §2.5). Abnahme P10.5-5/6/7.

