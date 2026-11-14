---
status: snapshot
purpose: Plan Phase 11, Block 0 (Haushalt, Baseline, Probe-Instanz) und Block 1 (Editor 4.1 „Writer-Optik", v4.1.0) gegen main@1128fdb — 20 Schritte, je mit Bauauftrag, Funktionsnamen, Ankern (String + Zeile vom 2026-11-13/14), Tests, Abnahme, Rot-Probe, Fallen und Startauftrag.
read-when: vor einem Schritt B0.x oder B1.x — nur den eigenen Abschnitt lesen (grep -n '^## B'); vorher den Rahmen phase11_editor_plan.md §0, §2, §7
detail: L2
up: ./phase11_editor_plan.md
down:
  - ../../phase11_editor/anker.json                 # die Anker dieses Plans, maschinenlesbar (P11-W)
  - ./phase10_5_editor_4_1_plan.md                  # 📗 Befunde F1–F14, Verträge §4.1–§4.4
  - ./phase10_5_editor_4_1_plan_anhang.md           # 📗 Messmethoden A3 (Konformität), A6 (Klick), A7 (Konstrukt × Fläche)
updated: 2026-11-14 (Abschluss-Durchgang: B0.3-Befehle korrigiert, B1.10–B1.16 mit Ankern, Tests und Fallen; 111 Anker, jeder genau einmal) | 2026-11-13 (angelegt — Planungssitzung P11; 89 Anker am selben Tag maschinell geprüft, jeder genau einmal)
---
# Phase 11 — Block 0 und Block 1 (Schritte)

> **Lies zuerst den Rahmen** (`phase11_editor_plan.md` §0, §2, §7). Hier steht je Schritt nur, was dieser Schritt braucht.
> **Kürzel:** **C** = Claude Code · **E** = Ausführer (opencode, MiniMax M3.1 Flash; Rückfall P11-I) · **N** = Nikinger ·
> 🖼 = Bildurteil nötig (nur C oder N, P11-J) · 📊 = hängt an der Form echter Daten.
> **Pfade:** `S/` steht für `phase5_ui/webui/static/`. **Anker:** String wörtlich, Zeile vom 2026-11-13/14 (derselbe Code, `main@1128fdb`); die heutige Zeile
> nennt `.venv/bin/python phase11_editor/scripts/plan_anker.py <Schritt>`.

## Rahmen jedes Startauftrags (steht wortgleich im Head)

> Du arbeitest im Repo `savefxy` an **Phase 11, Schritt `<Schritt>`**. Lies in dieser Reihenfolge: den Session-Block in
> `phase11_editor/CLAUDE.md`; `docs/concepts/phase11_editor_plan.md` §0, §2 und §7 ganz; in
> `docs/concepts/phase11_editor_plan_block1.md` **nur** den Abschnitt `## <Schritt>`. Begrenze jede Shell-Ausgabe mit
> `| cut -c1-240`. Rufe zuerst `.venv/bin/python phase11_editor/scripts/plan_anker.py <Schritt>` auf. Baue **genau diesen
> Schritt** in **einer** Sitzung (Kontext höchstens 200.000 Tokens; bei 150.000 ohne Abschluss: Schnitt und Übergabe).
> Tests nur mit bereinigter Umgebung (§2.1 Nr. 3). Nur Wegwerf-Instanzen, Stopp über die PID-Datei; kein `sudo`, kein
> `systemctl`, kein Push, kein Deploy. Ein Commit am Ende nach §2.1 Nr. 5, mit deinem Modell-Trailer. Bei einem Auslöser aus
> §2.3: Stopp und Meldung im Session-Block. Der Schritt-Auftrag folgt.

---

## Schrittfolge

| Schritt | Inhalt | Wer | Hängt ab von |
|---|---|---|---|
| B0.1 | Haushalt: INDEX teilen, Doku-Code-Durchgang | C | — |
| B0.2 | Baseline der Aufzeichnung | C | B0.1 |
| B0.3 | Probe-Instanz | C + **N** 📊 | B0.1 |
| B1.0 | Probe-Fundament (kein Produktcode) | C | B0.2 |
| B1.1 | Oberfläche: Ladeansicht, Rail, Listenkopf | C 🖼 | B1.0 |
| B1.2 | Typografie und Flächen | C 🖼 | B1.0 |
| B1.3 | Renderer-Fassade und Sicherheit | E | B1.0 |
| B1.4 | Erweiterungen und Konformität | E | B1.3 |
| B1.5 | Editor-Modus = Wahrheit | E | B1.4 |
| B1.6 | Einklappen I: Inline | C | B1.2, B1.5 |
| B1.7 | Einklappen II: Blockmarker, Listen, Kästchen | C 🖼 | B1.6 |
| B1.8 | Listen und Tasten | E | B1.7 |
| B1.9 | Raster I: Zelle wählen und bearbeiten | C 🖼 | B1.4, B1.7 |
| B1.10 | Raster II: Struktur | E | B1.9 |
| B1.11 | Raster III: Bereich und Zwischenablage | E | B1.10 |
| B1.12 | Suchen und Ersetzen | E | B1.7 |
| B1.13 | Komfort und Glyphen — **streichbar** | E | B1.7 |
| B1.14 | Darstellungs-Gate | C | alle davor |
| B1.15 | Sichtung auf der Probe-Instanz | C + **N** 🖼 📊 | B1.14, B0.3 |
| B1.16 | Release `v4.1.0` | C + **N** | B1.15 |

Unter Zeitdruck fällt zuerst B1.13, dann B1.11. Nie B1.14 oder B1.15.

---

## B0.1 — Haushalt: INDEX teilen, Doku-Code-Durchgang (C)

**Erlaubte Pfade:** `docs/`, `scripts/`, `phase*/tests/` (nur Wächter, die die Karte lesen), `phase1_storage/storage/frontmatter.py` (**nur** der Kommentar unten), Wurzel-`CLAUDE.md`, Memory.
**Bau.**
1. **Karte teilen.** Neue Datei `docs/INDEX_ABGESCHLOSSEN.md` (📦-Kopf, L0-Teil 2). Die Abschnitte aller abgeschlossenen Phasen wandern **verbatim** dorthin: `scripts/move_sections.py docs/INDEX.md docs/INDEX_ABGESCHLOSSEN.md "<Überschrift>" …` (die Überschrift bleibt mit Zeiger stehen). In `docs/INDEX.md` bleiben: Kopf, „Root & governance", Phase 11, „Referenzmaterial", Session-Log.
2. **`scripts/doc_health.py`:** `_read_index_lines(index_path)` liefert den Text **beider** Karten (zweite Datei optional: fehlt sie, gilt nur die erste). `check_index_lines` meldet weiter „keine Zeile in docs/INDEX.md", nennt aber beide Dateien.
3. **Wächter:** in `phase11_editor/tests/test_index_karten.py`: `docs/INDEX.md` ≤ 32.960 B (≥ 8.000 B Luft); jede `.md` hat **genau eine** Zeile, in **einer** der zwei Karten; Gegenprobe im Test (eine Datei in beiden Karten → rot; eine in keiner → rot).
4. **Doku-Code-Durchgang:** `doc_health` = 0. **E6:** der Kommentar in `frontmatter.py` sagt „der Body behaelt seine Zeilenenden byteweise" — das gilt für `parse()`, nicht für den Store (`read_text()` übersetzt CR/CRLF, Editor-Plan F8). Kommentar um genau diesen Satz ergänzen; **kein** Code. Die Zeile B20 in `phase1_storage/CLAUDE.md:169` bekommt denselben datierten Nachsatz.
5. **Doku-Hygiene** in der Wurzel-`CLAUDE.md`: ein datierter Satz „L0 = zwei Dateien" (die Konvention `DOC_LAYERS_CONVENTION.md` bleibt byte-identisch).
6. **Betrieb klein** (Closeout §6 Nr. 15): drei Zeilen im Head unter „Offen bei Eurofleet". Kein Code.
7. **Memory:** `project_phase_status.md` und die Zeile in `MEMORY.md` nachziehen.
8. **Haushalt-Befunde** (geprüft 2026-11-14 in der Planung; B0.1 schreibt sie als Ergebnis in den Session-Block, auch die No-Ops; **kein** Edit außer Nr. 8c):
   a. `.claude/RESUME.md` **existiert nicht** (`.claude/` ist seit 2026-07-24 ignoriert; die zwei WIP-Checkpoint-Commits liegen auf keinem Branch). Die Ausnahme `doc_health.py:22` **bleibt**: `_iter_markdown` liest `.claude/` absichtlich mit, und der Harness legt die Datei bei einem Limit-Checkpoint neu an. → No-Op.
   b. **Alt-Benennungen:** „Space-Server" in Wurzel-`CLAUDE.md`, `ROADMAP.md`, `README.md` ist der Gattungsname des Projekts, „Sharefyx" der Produktname — kein Umbenennen. Die veraltete Vorgabe `EXPECTED_VERSION=v3.0.1` in `health_gate.sh:29` ist ein Fehlbild (Rahmen §7) und gehört zu B17 (Block 3). → No-Op.
   c. **Verwaiste Dateien:** keine; die größten versionierten Dateien (Film 25,7 MB, drei Karten-Bilder je ~0,6 MB) sind gewollt. **Verwaiste Branches:** `p105-block5`, `p105-block7`, `p105-block9` sind in `main` enthalten; `hotfix-b1` und `deploy-version-marker-only` tragen je einen Commit, der nicht auf `main` liegt. Löschen nur nach OK des Nikingers (steht unter „Offen beim Nikinger").
9. **Archiv für die Session-Blöcke:** `phase11_editor/SESSIONS_ARCHIVE.md` anlegen (📦-Card nach dem Muster `phase10_5_finishing/SESSIONS_ARCHIVE.md`, Zeile im Phase-11-Abschnitt der Karte) — **nach** Nr. 1, vorher hat die Karte keinen Platz (37.956 von 37.960 B). Erst dann rotiert `scripts/rotate_session_block.sh phase11_editor` den Planungsblock; ohne die Datei bricht das Skript ab (`Archiv fehlt`, Z. 76).

**Anker.**
| Datei | Zeile | String |
|---|---|---|
| `scripts/doc_health.py` | 61 | `def _read_index_lines(index_path: Path) -> str:` |
| `scripts/doc_health.py` | 65 | `def check_index_lines(repo_root: Path, index_text: str) -> list[str]:` |
| `phase10_5_finishing/tests/test_register_archive.py` | 129 | `def test_the_register_and_the_index_keep_their_reserve():` |
| `phase1_storage/storage/frontmatter.py` | 20 | `` # Geschrieben wird weiter nur `\n` (`serialize()`); der Body behaelt seine Zeilenenden byteweise. `` |

**Tests.** Neu `test_index_karten.py` (3 Tests + 2 Gegenproben). Bestehende Wächter, die die Karte lesen, mit Absicht anpassen — vorher auflisten: `grep -rln 'INDEX.md' phase*/tests scripts`.
**Abnahme:** P11-1. **Rot-Probe:** die Gegenproben im Test; zusätzlich von Hand eine Zeile aus der Karte nehmen → `doc_health` meldet genau diese Datei.
**Fallen.** Reihenfolge: Teilung (Nr. 1) → Archiv anlegen (Nr. 9) → Rotation; umgekehrt scheitert zuerst die Rotation, dann der Platz in der Karte. · `move_sections.py` verschiebt an `## `-Grenzen: die Karte zitiert in ihrem Kopf eigene Überschriften (Memory „head edit anchor trap") — nach dem Lauf die Zahl der `## `-Zeilen in beiden Dateien zählen. · `git diff --stat -- phase1_storage/storage` darf **genau** `frontmatter.py` zeigen, und `git diff` darin nur Kommentarzeilen; alles andere ist Auslöser §2.3 Nr. 2.
**Startauftrag B0.1:** „Teile die Doku-Karte in `docs/INDEX.md` und `docs/INDEX_ABGESCHLOSSEN.md`, lehre `doc_health.py` beide Dateien, baue den Wächter mit Gegenproben, zieh E6 als Kommentar nach und leg `phase11_editor/SESSIONS_ARCHIVE.md` an, bevor du den Planungsblock rotierst. Fertig, wenn `docs/INDEX.md` ≤ 32.960 B ist, `doc_health` 0 meldet und die volle Suite grün ist."

## B0.2 — Baseline der Aufzeichnung (C)

**Bau.** Nach B0.1 messen und **im Head** festhalten, mit Commit-SHA: volle Suite (Zahl, Dauer) · `doc_health` · `ui_budget` (alle Zeilen mit Wert) · Darstellungs-Probe `--browser=beide` (rote Zellen je Browser, Abweichungen). Der Neulauf der Probe ändert im Beleg nur Zeitwerte: `git checkout -- phase10_5_finishing/probes/p105_ed41_darstellung_s2.json`.
**Erwartung** (Rahmen §8): 1939 + neue Wächter grün, 0 rot · `doc_health` 0 · 6/6 · 26 rot von 62, 0 Abweichungen.
**Abnahme:** P11-2. **Rot-Probe:** jede Abweichung von §8 ist ein Befund im Session-Block, bevor B1.0 startet — die Baseline ist die Messung, gegen die jeder spätere Schritt rot werden kann.
**Startauftrag B0.2:** „Miss die Baseline nach B0.1 (Suite, `doc_health`, `ui_budget`, Darstellungs-Probe beide Browser) und trag Zahlen und SHA in den Head ein. Jede Abweichung vom Rahmen §8 ist ein Befund."

## B0.3 — Probe-Instanz (C bereitet vor, **N** führt aus) 📊

**Erlaubte Pfade:** `phase11_editor/scripts/`, `phase11_editor/tests/`, `phase3_edge/scripts/install_units.sh`, `phase5_ui/systemd/sharefyx-staging.service`, `phase3_edge/tests/test_units.py`.
**Geprüft 2026-11-14 (nur lesend).** Die installierte Staging-Unit läuft aus `/opt/sharefyx/current`, also aus dem Release der Produktion (V228 ✅) · alle installierten Units sind byte-gleich mit Vorlage + `local.env` (Ausnahme: eine Kommentarzeile in `sharefyx-tail-proxy.service`) · `/opt/sharefyx` gehört `savefyx`: `deploy.sh` braucht dort kein `sudo`, nur für `systemctl` · `install_units.sh` schreibt **jede** Unit neu und endet mit `systemctl enable --now sharefyx-mcp.service` (Z. 124) — deshalb der Filter unten.
**Bau (C).**
1. `phase11_editor/scripts/probe_instanz_kopie.sh`: `rsync -a --delete --delete-excluded --exclude='.index.sqlite3*'` von `SHAREFYX_DATA_ROOT` nach `SHAREFYX_STAGING_DATA_ROOT`. **Bricht ab**, wenn beide Pfade gleich sind, wenn das Ziel nicht auf `-staging` endet oder wenn die Quelle fehlt. Kein Literal im Skript (Muster `phase3_edge/scripts/backup_data_root.sh`). Ausgabe: eine JSON-Zeile (Zahl der `.md`-Dateien in Quelle und Ziel). `--delete-excluded` löscht auch den alten Index der Kopie; beim nächsten Start baut `Store.__init__` ihn neu (`index.connect` liefert `rebuilt=True`, `store.py:364`).
2. `install_units.sh`: (a) optionale Platzhalter `STAGING_REPO_ROOT` (Vorgabe `${REPO_ROOT}`) und `STAGING_VENV` (Vorgabe `${VENV}`); die Staging-Unit benutzt `__STAGING_REPO_ROOT__`/`__STAGING_VENV__` in `Documentation=`, `WorkingDirectory=` und `ExecStart=`. Ohne die zwei Zeilen in `local.env` rendert alles wie heute. (b) **Filter:** `install_units.sh [<unit> …]` installiert nur die genannten Units; `enable --now sharefyx-mcp.service` läuft nur ohne Filter. (c) Zwei Nähte wie in `deploy.sh`, damit der Filter testbar ist: `SYSTEMD_DEST="${SHAREFYX_SYSTEMD_DEST:-/etc/systemd/system}"`, `SYSTEMCTL="${SHAREFYX_SYSTEMCTL:-systemctl}"`.
3. Die Befehle für den Nikinger, vollständig und **in dieser Reihenfolge**, in den Head unter „Offen beim Nikinger" (Kosten: keine; `sudo` nur in ii und iv):
   i. zwei Zeilen in `phase3_edge/local.env`: `STAGING_REPO_ROOT=/opt/sharefyx/staging` und `STAGING_VENV=/opt/sharefyx/staging/.venv`.
   ii. `sudo phase3_edge/scripts/install_units.sh sharefyx-staging.service` — rendert **nur** die Staging-Unit.
   iii. `SHAREFYX_DATA_ROOT=<echt> SHAREFYX_STAGING_DATA_ROOT=<echt>-staging phase11_editor/scripts/probe_instanz_kopie.sh`.
   iv. `SHAREFYX_RELEASES_DIR=/opt/sharefyx/staging-releases SHAREFYX_CURRENT_LINK=/opt/sharefyx/staging SHAREFYX_SERVICE=sharefyx-staging SHAREFYX_PORT=8766 SHAREFYX_ALLOW_STALE_UPDATELOG=1 SHAREFYX_SYSTEMCTL="sudo systemctl" phase5_ui/scripts/deploy.sh main` — **ohne** `SHAREFYX_DATA_ROOT` (sonst bündelt der Deploy vorab die echten Daten). Der Neustart lädt die Kopie mit frischem Index. Dauer ≈ 10 min (die Release-Tests laufen mit); Platz je Release ≈ 310 MB, `deploy.sh` behält fünf (≈ 1,6 GB).
   v. `phase8_5_picker_release/scripts/health_gate.sh --port=8766 --current-link=/opt/sharefyx/staging --expected-version=<v> --expected-sha=<sha>`.
   vi. Konto, erst **nach** dem ersten Start (`StateDirectory` legt den Ordner an): `SPACE_AUTH_DB=/var/lib/sharefyx-staging/auth.sqlite3 SPACE_PUBLIC_BASE_URL=<Adresse der Probe-Instanz> /opt/sharefyx/staging/.venv/bin/python /opt/sharefyx/staging/phase4_auth/scripts/authctl.py invite <space>` — `SPACE` ist positional, `--purpose` kennt nur `initial`/`reset` (Drift aus P7: `phase7_spaces_admin/CLAUDE.md`, Abnahmezeile 6).
   vii. `tailscale serve` für Port 8766 (Bedarf 1, V226) · `systemctl show -p MainPID sharefyx-mcp.service` vor ii und nach vii: dieselbe PID.

**Anker** (für Nr. 2).
| Datei | Zeile | String |
|---|---|---|
| `phase3_edge/scripts/install_units.sh` | 34 | `SYSTEMD_DEST="/etc/systemd/system"` |
| `phase3_edge/scripts/install_units.sh` | 82 | `STAGING_BASE_URL="${STAGING_BASE_URL:-${PUBLIC_BASE_URL}:${STAGING_PORT}}"` |
| `phase3_edge/scripts/install_units.sh` | 110 | `    -e "s#__STAGING_BASE_URL__#${STAGING_BASE_URL}#g" \` |
| `phase3_edge/scripts/install_units.sh` | 124 | `systemctl enable --now sharefyx-mcp.service` |
| `phase5_ui/systemd/sharefyx-staging.service` | 3 | `Documentation=file://__REPO_ROOT__/phase5_ui/CLAUDE.md` |
| `phase5_ui/systemd/sharefyx-staging.service` | 24 | `WorkingDirectory=__REPO_ROOT__` |
| `phase5_ui/systemd/sharefyx-staging.service` | 35 | `ExecStart=__VENV__/bin/python __REPO_ROOT__/phase2_mcp/scripts/serve.py` |
| `phase3_edge/tests/test_units.py` | 199 | `    for placeholder in ("__STAGING_PORT__", "__STAGING_DATA_ROOT__", "__STAGING_BASE_URL__"):` |

**Tests.** `phase11_editor/tests/test_probe_instanz_kopie.py` (tmp-Verzeichnisse: kopiert; gleiche Pfade → Abbruch; Ziel ohne `-staging` → Abbruch; Quelle fehlt → Abbruch; die Quelle bleibt byte-gleich; ein alter Index im Ziel ist danach weg). `phase3_edge/tests/test_units.py`: der Platzhalter-Wächter kennt die zwei neuen Namen; **Filter-Test** nach dem hermetischen Muster `test_install_script_refuses_without_local_env` (Kopie von `scripts/` und `systemd/` nach `tmp_path`, eigenes `local.env`, `SHAREFYX_SYSTEMD_DEST=tmp`, `SHAREFYX_SYSTEMCTL` = Stub, der seine Argumente protokolliert): mit Filter liegt genau eine Datei im Ziel und der Stub sah kein `enable`; ohne Filter alle und `enable --now sharefyx-mcp.service`.
**Abnahme:** P11-3 (**N**): `health_gate` gegen Port 8766 grün · Login mit dem Staging-Konto · Zahl der Items = Zahl der Quelle · von außerhalb des Tailnets nicht erreichbar · `sharefyx-mcp.service` trägt dieselbe Haupt-PID wie vorher.
**Rot-Probe:** die drei Abbruchfälle des Kopierskripts · der Filter-Test ohne Filter-Zweig (alle Units installiert) wird rot · `health_gate --port=8766` **vor** dem Start der Unit ist rot.
**Fallen.** Die Unit lädt denselben DEK wie die Produktion (V227) bei **eigener** Auth-Datenbank: ein Produktionskonto gibt es dort nicht. · „Staging zeigt alte Daten" ist kein Fehler: kopiert wird nur auf Befehl, und erst der Neustart (Schritt iv) lädt den neuen Index. · `deploy.sh` bricht mit „trägt keinen Eintrag vom heutigen Tag" ab: `SHAREFYX_ALLOW_STALE_UPDATELOG=1` fehlt (nur für die Probe-Instanz, nie für die Produktion). · `health_gate` ohne `--current-link` prüft `/opt/sharefyx/current` — also das Release der **Produktion** — und meldet grün für das falsche Release. · `tailscale serve` richtet Eurofleet oder der Nikinger ein (Bedarf 1, V226), nie ein Agent.
**Startauftrag B0.3:** „Baue das Kopierskript mit seinen drei Abbrüchen, die zwei Staging-Platzhalter und den Unit-Filter in `install_units.sh` samt Tests. Schreib die sieben Befehle für den Nikinger in der Reihenfolge des Plans vollständig in den Head. Führe selbst nichts aus, was `sudo` braucht."

---

## B1.0 — Probe-Fundament (C, kein Produktcode)

**Erlaubte Pfade:** `phase11_editor/probes/`, `phase11_editor/tests/`.
**Bau.**
1. **Korpus** `phase11_editor/probes/fixtures_p11/` (`.txt`, byte-genau, mit `MANIFEST.json` wie `fixtures_ed41/`): `01_tabelle_unter_text.txt` (Tabelle direkt unter einer Textzeile — die Korpus-Lücke), `02_notiz.txt` (eine KI-typische Notiz: Überschriften h1–h3, Absatz mit fett/kursiv/Code/Link `#item/…` und `https://…`, Liste zweier Ebenen, nummerierte Liste, drei Aufgaben, Zitat, breite Tabelle mit sieben Spalten, Zaun, `~~durch~~`, Trennlinie; ≥ 40 Zeilen mit je ≥ 2 Wörtern), `03_raster.txt` (Tabelle mit leerer Zelle, `\|` in einer Zelle, Codespan mit `|`, `<br>`, ungleicher Zeilenlänge, ohne Außen-Pipes, je ein Link `[Notiz](#item/itm_0123abcd)` und `https://example.org` in einer Zelle), `04_grenzen.txt` (`a **b** c`, einzelnes `*`, `_` im Wort, `` ` `` unpaarig, `[x]{.rot}`, `::: {.zentriert}`, `***fett und kursiv***`, `**[Link](https://example.org)**` — die letzten zwei erzeugen angrenzende Klapp-Bereiche, B1.6).
2. **Spec** `p11_writer_spec.py`: `ZELLEN` (Name → `{basis, ab, grund}`), `GEGENLAEUFE` (Name → `{static: {datei: [[alt, neu]]}, kippt: [...]}`), `STAND`, `BELEG_JE_STAND`. Form wie `p105_ed41_spec.py:428–540`.
3. **Probe** `p11_writer_probe.py`: lädt `p105_b14_layout_probe.py` als Modul und setzt dieselbe Weiche wie die Darstellungs-Probe; sät beide Korpora (`fixtures_ed41` nur lesend über `p105_ed41_spec.fixtures_von_platte()`); misst je Browser alle Zellen des Rahmens §4 (P11-7 bis P11-22). **Messmethoden, verbindlich:**
   - `klick30`: je sichtbarer Zeile das zweite Wort mit ≥ 4 Buchstaben, das nicht unter einer Marke liegt; Klick bei 25 % seines ersten Zeichens; **zwei** Bedingungen: der Hit-Test des Browsers (`caretRangeFromPoint`, in Firefox `caretPositionFromPoint`, V230) trifft den Wortanfang **und** ein getipptes Zeichen steht genau dort; **nach jedem Ziel Cursor zurück, Scroll wiederherstellen, Koordinaten neu messen**.
   - `gleichtext`: sichtbarer Text des Editors (alle Textknoten der Zeilen, ohne Knoten in eingeklappten Bereichen, Widgets über ihr `textContent`), Leerraum normalisiert, gegen `textContent` von `#ro-preview` desselben Bodys im fremden Space.
   - `tastenkosten`: `27_gross`, Zeile ≥ 900, 3 × 20 `replaceRange` mit erzwungenem Layout, Median synchron.
   - `ladeansicht`: Abruf des zweiten Items per umwickeltem `fetch` um 900 ms verzögert; Messung bei 100 ms und bei 450 ms.
   - `rail_fest`: Fenster 1600 × 620, sieben Spaces mit je vier Ordnern.
4. **Basislinie:** rot erwartet für `schrift`, `kante`, `marker_eingeklappt`, `gleichtext`, `listenpunkt`, `ebenen`, `ladeansicht`, `rail_fest`, `flaechen`, `listenkopf`, alle `raster_*`, `suche_*`, `liste_*`, `taste_*`; grün erwartet für `klick30`, `doppelklick`, `dreifachklick`, `ziehen`, `grenzen`, `undo20`, `tastenkosten`, `kaestchen`, `tabelle_breite`. Eine Abweichung steht im Beleg unter `abweichungen` und ist ein Befund.

**Anker.** `phase10_5_finishing/probes/p105_ed41_darstellung_probe.py:108` `WEICHE = '''_ed41_static = os.environ.get("ED41_STATIC_DIR")` — die Weiche, die die Kopie der statischen Dateien ausliefert; wortgleich übernehmen, nicht neu erfinden.
**Tests.** `phase11_editor/tests/test_p11_probe.py`: Beleg-Schema; Zellnamen = Spec; die Basislinie ist rot genau dort, wo die Spec es sagt; jeder Gegenlauf-Anker kommt genau einmal vor; kein Geheimnis im Beleg (Muster `test_ed41_probe.py:294`).
**Abnahme:** die Probe läuft in beiden Browsern, 0 Abweichungen. **Rot-Probe (Selbsttest):** Gegenlauf `soll_falsch` setzt in einer Kopie ein falsches Soll für `kaestchen` → genau diese Zelle kippt.
**Fallen.** „Fast alle Klicks daneben" ist das Messgerät (Rahmen §7). · Die Probe schreibt (Entwurf, Edits): nie gegen die Probe-Instanz oder die Produktion.
**Startauftrag B1.0:** „Baue Korpus, Spec und Writer-Probe nach den verbindlichen Messmethoden; kein Produktcode. Fertig, wenn die Probe in Chromium und Firefox läuft, die Basislinie mit der Spec übereinstimmt (0 Abweichungen) und der Selbsttest genau eine Zelle kippt."

## B1.1 — Oberfläche: Ladeansicht, Rail, Listenkopf (C 🖼)

**Erlaubte Pfade:** `S/js/loading.js`, `S/js/editor.js` (nur die eine Zeile), `S/js/tree.js`, `S/app.html`, `S/app.css`, Tests, Probe-Spec.
**Bau.**
1. **Ladeansicht (F1).** `withLoading(el, promise, { delayMs = 200, wechselKlasse = null } = {})`: wird nach `delayMs` zusammen mit `is-loading` gesetzt und mit ihr entfernt. `selectItem()` übergibt `{ wechselKlasse: "is-wechsel" }`. CSS: `.detail.is-wechsel > * { visibility: hidden; }` — das Gerüst (`::after`) liegt dann auf leerem Grund. Unter 200 ms ändert sich nichts (kein Flackern).
2. **Rail (F3).** Neues Element `<div class="rail__scope" id="rail-scope"></div>` zwischen `#rail-tree` und `.rail__account`. `tree.js`: `railScopeEl` in `init()`; `renderRail()` leert beide; `renderScopeRow()` schreibt Gruppenzeile und Knopf nach `railScopeEl`. CSS: `.rail { overflow: hidden; }` (nach der Sammelregel), `.rail__tree { flex: 1 1 auto; min-height: 0; overflow-y: auto; }`, `.rail__scope { padding: 0 var(--space); }`.
3. **Listenkopf (F5, Lesart P11-V).** `.list__head` verlässt die beiden Glas-Sammelregeln und trägt `background: var(--bg-void)` wie `.list`; Trennstrich und `position: sticky` bleiben.

**Anker.**
| Datei | Zeile | String |
|---|---|---|
| `S/js/editor.js` | 939 | `return withLoading(detailEl, api("/items/" + encodeURIComponent(id))).then(function (item) {` |
| `S/js/loading.js` | 30 | `export function withLoading(el, promise, { delayMs = 200 } = {}) {` |
| `S/js/loading.js` | 59 | `if (!finished) el.classList.add("is-loading");` |
| `S/app.css` | 3025 | `.is-loading::after {` (mit der Folgezeile `  content: "";`) |
| `S/app.css` | 429 | `.rail, .list, .detail {` (drei Zeilen bis `}`) |
| `S/app.css` | 689 | `.rail__tree { padding: 0 var(--space); }` |
| `S/app.css` | 762 | `.rail__account {` (mit `  margin-top: auto;`) |
| `S/app.html` | 34 | `<div class="rail__tree" id="rail-tree"></div>` |
| `S/js/tree.js` | 349 | `railTreeEl.appendChild(el("div", "tree__group", "Alles"));` |
| `S/js/tree.js` | 400 | `  railTreeEl.textContent = "";` |
| `S/js/tree.js` | 429 | `  railTreeEl = document.getElementById("rail-tree");` |
| `S/app.css` | 824 | `.list__head {` (mit dem Kommentar `/* Liquid-Glas-Träger`) |
| `S/app.css` | 2976 | `   Capability vorhanden ist, der Default-Block läuft sonst. */` (danach beginnen die zwei Glas-Sammelregeln) |

**Tests.** pytest statisch: `loading.js` entfernt die Wechselklasse im selben Zweig wie `is-loading`; `renderScopeRow` schreibt nicht mehr nach `railTreeEl`; `#rail-scope` steht zwischen Baum und Konto. Der Wächter `test_view_titles.py` und die P8.6-Rail-Tests laufen mit.
**Abnahme:** P11-20, P11-21, P11-22 (Listenkopf). **Bilder** (Read, vorher/nachher): Ladeansicht bei 450 ms · Rail bei 620 px · Listenkopf — an den Nikinger; V231 entscheidet er.
**Rot-Probe.** `ohne_wechsel` (die Option aus `selectItem` nehmen) → nur `ladeansicht` rot · `rail_scrollt` (die Zeile `overflow-y: auto` am Baum nehmen) → nur `rail_fest` rot · `kopf_glas` (Listenkopf zurück in die Sammelregel) → nur `listenkopf` rot.
**Fallen.** `rail_fest` ist zahnlos, wenn der Baum gar nicht überläuft — die Zelle verlangt `scrollHeight > clientHeight` am Baum. · `#detail` enthält auch die Karte: `is-wechsel` wird nur gesetzt, wenn gerade ein Item offen ist (`shellEl.dataset.view === "detail"`), sonst blendet es die Karte aus.
**Startauftrag B1.1:** „Baue die drei Oberflächen-Punkte: neutrale Ladeansicht beim Notizwechsel, feste Rail-Fußzeile mit ‚Alle Items', Listenkopf im Ton seiner Fläche. Fertig, wenn `ladeansicht`, `rail_fest`, `listenkopf` in beiden Browsern grün sind, jeder der drei Gegenläufe genau seine Zelle kippt und drei Vorher/Nachher-Bilder im Session-Block genannt sind."

## B1.2 — Typografie und Flächen (C 🖼)

**Erlaubte Pfade:** `S/app.css`, `S/app.html`, `S/js/editor.js` (nur tote Teile), Tests, Probe-Spec.
**Bau.**
1. **Ein typografisches System:** `.CodeMirror` → `font-family: var(--font-ui); font-size: var(--fs-body); line-height: 1.6;`. Überschriften wie die Lesesicht: `.cm-header-1` 22 px, `-2` 18 px, `-3`/`-4` 16 px fett. Code (`.cm-comment`) Plex Mono 13 px. Die Größen-Klassen behalten `line-height: 0` (die Zeile springt sonst).
2. **Gemeinsame Lesebreite:** neues Token `--lesebreite` (Startwert `46rem`, in der Sitzung am Bild entscheiden); `.CodeMirror-lines { max-width: var(--lesebreite); margin: 0 auto; }`, `.preview` bekommt dieselbe Breite für seinen Inhalt. Die Regel an `.editor__textarea` (`max-width: 72ch`) folgt dem Token.
3. **Breite Tabellen** scrollen im Widget und in der Lesesicht (`overflow-x: auto` an einem Block um die Tabelle); nie breiter als der Container.
4. **Flächen (F2):** genau **zwei** Töne im Editor. Leisten (Kopf, Kopfdaten-Kopf, Text-Kopf, Anhängen) = **ein** Ton; Schreibfläche (`.panel--body`, `#editor-body`, `.CodeMirror`) = `--editor-bg`. Dafür `--panel-body` auf `var(--editor-bg)` setzen und die Leisten auf einen gemeinsamen Token `--leiste`.
5. **Aufräumen (F14):** `#editor-preview`, `editorPreviewEl`, `.toolbar-btn--wide` entfernen. **Nicht** entfernen: `setRawMode`, `.glass`.
6. **Randbefund:** links unten neben der Anhängen-Zeile steht ein abgeschnittenes Zeichen (in allen Bildern vom 2026-11-12). Erster Verdächtiger `.version-band__number`: Ursache klären, beheben oder als Befund melden.

**Anker.**
| Datei | Zeile | String |
|---|---|---|
| `S/app.css` | 2022 | `.CodeMirror {` (mit `  flex: 1;`) |
| `S/app.css` | 2042 | `  line-height: 21px;` (mit der schließenden Klammer) |
| `S/app.css` | 2044 | `.CodeMirror-lines { padding: calc(var(--space) * 2) calc(var(--space) * 3); }` |
| `S/app.css` | 2051 | `.CodeMirror .sfx-tabelle {` |
| `S/app.css` | 2072 | `.CodeMirror .cm-header-1 { font-size: 1.3em; }` |
| `S/app.css` | 2106 | `.CodeMirror .cm-md-s-klein { font-size: .85em; line-height: 0; }` |
| `S/app.css` | 1981 | `.editor__textarea {` |
| `S/app.css` | 1509 | `.preview {` |
| `S/app.css` | 71 | `  --editor-bg:     #0C1017;` |
| `S/app.css` | 167 | `  --panel-body:    #10151B;` |
| `S/app.css` | 2197 | `.editor__append {` |
| `S/app.css` | 1971 | `.version-band__number {` |
| `S/app.css` | 1918 | `.toolbar-btn--wide { font-family: var(--font-ui); padding: 0 10px; }` |
| `S/app.html` | 365 | `<div class="preview editor__preview" id="editor-preview" hidden></div>` |
| `S/js/editor.js` | 53 | `var editorPreviewEl;` |
| `S/js/editor.js` | 1076 | `editorPreviewEl = document.getElementById("editor-preview");` |

**Tests.** `test_editor_live.py` an den Rückbau anpassen; `test_contrast.py` läuft mit. Die Kommentare `app.css:2030–2041` und `2066–2070` (feste Zeilenhöhe) werden durch die neue Begründung ersetzt, nicht stehen gelassen.
**Abnahme:** P11-7, P11-18, P11-22 (Flächen); `klick30` bleibt 100 % (die Zeichen sind in diesem Schritt noch per `visibility` versteckt — gemessen 38/38 mit Plex Sans, Editor-Plan-Anhang A6); `tastenkosten` ≤ 8 ms. **Bilder:** `02_notiz` oben und unten, `27_gross` bei Zeile 1500, vorher/nachher.
**Rot-Probe.** `mono_zurueck` (Schrift zurück auf `--font-mono`) → nur `schrift` · `vier_toene` (`--panel-body` zurück auf `#10151B`) → nur `flaechen` · `tabelle_ohne_scroll` → nur `tabelle_breite`.
**Fallen.** V225: nach dem Schriftwechsel `cm.refresh()` nach dem Laden der Schrift (`document.fonts.ready`), sonst misst CM5 mit der Ersatzschrift und Klicks liegen daneben. · Eine Regel greift nicht: das vendorte CSS (Rahmen §7).
**Startauftrag B1.2:** „Stell den Editor auf das typografische System der Lesesicht (Plex Sans 16 px, Überschriften 22/18/16, Code Mono), gib Editor und Lesesicht eine gemeinsame Lesebreite, reduziere die Editor-Flächen auf zwei Töne und räum die toten Teile ab. Fertig, wenn `schrift`, `flaechen`, `tabelle_breite` grün sind, `klick30` 100 % bleibt und die Bilder im Session-Block stehen."

## B1.3 — Renderer-Fassade und Sicherheit (E)

**Erlaubte Pfade:** `S/vendor/marked/`, `S/js/markdown.js`, `S/js/editor.js`, `S/js/updates.js`, `S/js/editor/tabellen.js`, `phase5_ui/scripts/ui_budget.py`, `phase5_ui/THIRD_PARTY_LICENSES.md`, Tests, Darstellungs-Probe und ihre Spec.
**Bau.**
1. **Vendoren:** `S/vendor/marked/marked.esm.js` = `lib/marked.esm.js` aus `marked@18.1.3`, **unverändert**: 49.668 B, SHA-256 `e76f3b37046a5d294159872002e5f6fcda8ed232e1be45ff76b3863f2919dae3` (geprüft 2026-11-13, erneut 2026-11-14 aus dem npm-Cache). **Ohne Netz:** `npm pack marked@18.1.3 --offline` in einem Scratch-Ordner, dann `tar -xzf` (der Tarball liegt im npm-Cache dieser VM); fehlt er dort, ist der Download Netz → Auslöser §2.3 Nr. 6. Lizenztext: `package/LICENSE`. Keine `.map`. Abschnitt in `THIRD_PARTY_LICENSES.md` nach dem Muster des CodeMirror-Abschnitts. Vorher V220.
2. **Fassade** `js/markdown.js`, gleiche Importeure: `ensureRenderer(): Promise<boolean>` (lädt marked per `import()`, einmal, Ergebnis gecacht; `false` bei Fehlschlag) · `markdownToHtml(src, {itemId, assetIds}): string` (synchron; ist der Renderer nicht geladen, liefert sie den **escapten** Text in `<pre>` — nie rohes HTML) · `blockRanges(src): [{typ, von, bis}]` (Zeilenbereiche der obersten Tokens aus der Summe ihrer `raw`-Längen) · `FORMAT_VOKABULAR` unverändert. Der alte Zeilenparser `_markdownZeilen` und `inlineMarkdown` entfallen; `sanitizeHtml`, `safeHref`, `safeSrc`, `resolveAssetSrc` bleiben.
3. **SI1:** ein marked-Renderer für `html`-Tokens (Block und Inline) gibt `escapeHtml(token.raw)` zurück; Ausnahme genau `<br>`, `<br/>`, `<br />`. **SI2:** `ALLOWED_TAGS` + `DEL`, `H5`, `H6`, `SUP`. Das Vor-Escapen der ganzen Quelle entfällt.
4. **Aufrufer warten:** `showReadonlyItem` und `updates.js` rufen `ensureRenderer().then(…)` und prüfen danach, ob dasselbe Item noch gewählt ist. `editor.js` lädt das Tabellen-Widget erst nach `ensureRenderer()`.
5. **Budget (P11-N):** `static_payload_files()` liefert drei Listen (Erstaufruf, Editor, Renderer = `vendor/marked/**`); zwei Zeilen „Editor nachgeladen" < 100 KB und „Renderer nachgeladen" < 20 KB.

**Anker.**
| Datei | Zeile | String |
|---|---|---|
| `S/js/markdown.js` | 203 | `export function markdownToHtml(src, options) {` |
| `S/js/markdown.js` | 214 | `function _markdownZeilen(lines, itemId, assetIds) {` |
| `S/js/markdown.js` | 376 | `var ALLOWED_TAGS = new Set([` |
| `S/js/markdown.js` | 426 | `function sanitizeHtml(html) {` |
| `S/js/editor.js` | 8 | `import { markdownToHtml, FORMAT_VOKABULAR } from "./markdown.js";` |
| `S/js/editor.js` | 834 | `  roPreviewEl.innerHTML = markdownToHtml(item.body, {` |
| `S/js/editor.js` | 573 | `import("./editor/tabellen.js").then(function (modul) {` |
| `S/js/updates.js` | 41 | `body.innerHTML = markdownToHtml(markdownList(entry.lines));` |
| `S/js/updates.js` | 67 | `bannerBodyEl.innerHTML = markdownToHtml(zeilen.length ? zeilen[0] : "");` |
| `S/js/editor/tabellen.js` | 172 | `var html = markdownToHtml(w.text, { itemId: k.itemId, assetIds: k.assetIds });` |
| `S/js/editor/tabellen.js` | 174 | `if (html.indexOf("<table>") !== 0 \|\| html.indexOf("<table>", 1) !== -1` |
| `phase5_ui/scripts/ui_budget.py` | 142 | `nachgeladen = sorted(p for p in (static_dir / "vendor").rglob("*") if p.is_file())` |
| `phase5_ui/scripts/ui_budget.py` | 314 | `"Editor nachgeladen (gzip)", editor_total, 80 * KB, ", ".join(editor_parts),` |
| `phase5_ui/THIRD_PARTY_LICENSES.md` | 34 | `## CodeMirror 5 (Editor Stufe 1+2)` |
| `phase10_5_finishing/probes/p105_ed41_spec.py` | 519 | `STAENDE = ["S0", "S1", "S2"]` (neuer Stand `S3a`, Beleg `p105_ed41_darstellung_s3a.json`) |
| `phase10_5_finishing/probes/p105_ed41_spec.py` | 520 | `STAND = "S2"` |

**Tests.** Neu `phase11_editor/tests/test_renderer_vendor.py` (Datei da, SHA-256 = Lizenzdatei, Gegenprobe mit vertauschter Datei — Muster `test_codemirror_vendor.py:80`). XSS-Fixtures als Textprüfung. Mit Absicht geändert: `test_editor_format.py::test_the_inline_rule_comes_before_the_links`, `phase5_ui/tests/test_static_routes.py::test_markdown_link_regex_allows_escaped_brackets` (wird Probe-Zelle), `test_budget_coverage.py::test_the_two_corridors_hold` (drei Korridore), `test_ed41_tabellen.py::test_the_separator_regex_is_the_renderers` und die drei Scanner-Tests daneben (der Interim-Scanner bleibt bis B1.4).
**Abnahme:** P11-5, P11-24. Darstellungs-Probe Stand **S3a**: `html_als_text` und `keine_aktiven` grün; der Korpus öffnet in Lesesicht und Update-Log ohne Seitenfehler; keine Zelle, die in S2 grün war, wird rot.
**Rot-Probe.** `s3a_ohne_html_override` → nur `html_als_text` rot · `s3a_sanitizer_onerror` (Sanitizer erlaubt `onerror`) → nur `keine_aktiven` rot · ein statischer Import von `vendor/marked` → Budget-Wächter rot.
**Fallen.** Lesesicht leer oder `<pre>`: `ensureRenderer()` nicht abgewartet oder V222 (CSP). · `&amp;amp;` im Text: das Vor-Escapen läuft noch. · Tabellen-Widget fehlt, ohne Fehlermeldung: die Absicherung `tabellen.js:174–175` verlangt `html.slice(-8) === "</table>"`, marked 18.1.3 endet aber auf `</table>\n` (gemessen 2026-11-14; der Anfang `<table>\n<thead>` besteht die Prüfung). Die Ausgabe vor der Prüfung `trim()`en — die Prüfung bleibt. · `align="left"` an `th`/`td` verschwindet im Sanitizer: gewollt bis B1.4 (Klassen `ta-l/ta-c/ta-r`).
**Startauftrag B1.3:** „Vendore marked 18.1.3 (SHA-256 im Plan), bau `js/markdown.js` zur Fassade um (`ensureRenderer`, `markdownToHtml`, `blockRanges`), ersetze das Vor-Escapen durch den HTML-Token-Override (SI1) und erweitere den Sanitizer (SI2), teile das Budget in drei Korridore. Fertig, wenn die Darstellungs-Probe im Stand S3a `html_als_text` und `keine_aktiven` grün zeigt, beide Gegenläufe genau ihre Zelle kippen und `ui_budget` alle Zeilen OK meldet."

## B1.4 — Erweiterungen und Konformität (E)

**Erlaubte Pfade:** `S/js/markdown.js`, `S/js/editor/tabellen.js`, `phase2_mcp/mcpserver/tools.py` (**nur** der eine Satz), Probe, Spec, Fixtures, `THIRD_PARTY_LICENSES.md`, Tests.
**Bau.**
1. **marked-Erweiterungen** in der Fassade: Format inline `[Text]{.rot .gross}` (Bild vor Format; im Codespan nie), Format-Block `::: {.zentriert}` … `:::` (unbekannte Klasse bleibt wörtlich, **keine** Zeile verschwindet), Fußnoten als eigene Erweiterung ohne IDs (E7: Verweis `<sup>`, Liste am Ende).
2. **Overrides:** Tabellen-Ausrichtung als Klasse `ta-l/ta-c/ta-r` statt `align=`; Kästchen erzwungen `disabled`; `asset:`-Bilder über `resolveAssetSrc`; Links über `safeHref`.
3. **`blockRanges`** kommt aus der Fassade; der Interim-Scanner in `tabellen.js` und sein `TRENNER` entfallen; das Widget ruft `blockRanges(cm.getValue())`.
4. **Konformität:** `fixtures_ed41/gfm_0.29_beispiele.json`, **einmal** extrahiert (Quelle, Version, SHA-256 und Lizenz nach Editor-Plan S3b; Zählweise Anhang A3). Die Probe liest nur die Datei, nie das Netz.
5. **E9:** ein Satz in `_FORMAT_HINT`: die Weboberfläche zeigt GFM (Tabellen, Aufgaben, Fußnoten), rohes HTML bleibt Text außer `<br>`.

**Anker.**
| Datei | Zeile | String |
|---|---|---|
| `S/js/markdown.js` | 50 | `var FORMAT_INLINE_RE =` |
| `S/js/markdown.js` | 195 | `function _todoHtml(inhalt, itemId, assetIds) {` |
| `S/js/markdown.js` | 396 | `var ALLOWED_CELL_CLASSES = new Set(["ta-l", "ta-c", "ta-r"]);` |
| `S/js/editor/tabellen.js` | 22 | `var TRENNER =` |
| `S/js/editor/tabellen.js` | 43 | `export function blockRanges(zeilen) {` |
| `phase2_mcp/mcpserver/tools.py` | 223 | `"Weboberfläche zeigt dieselben Formate."` |

**Tests.** Die Scanner-Tests in `phase10_5_finishing/tests/test_ed41_tabellen.py` werden auf die Fassade umgestellt: `test_the_separator_regex_is_the_renderers` (Z. 94), `test_the_interim_scanner_finds_the_renderers_tables` (Z. 128), `test_the_scanner_agrees_with_the_renderer_on_the_corpus` (Z. 141); `test_the_cell_starts_follow_the_renderers_split` (Z. 178) erst in B1.9. Ein Test hält den `_FORMAT_HINT`-Satz fest.
**Abnahme:** P11-4. Stand **S3b**: `konformitaet` ≥ 95 %; alle `l_*`-Zellen grün; `tabelle_widget` und die fünf S2-Zellen bleiben grün.
**Rot-Probe.** `s3b_ohne_format` → `l_format_*` rot · `s3b_ohne_align` → `l_tabelle_ausrichtung` rot · `s3b_alter_teiler` (Zellen an jedem `|` teilen) → `l_tabelle_pipe_maskiert` rot.
**Fallen.** `mcpserver/tools.py` ist sonst Sperrzone: der Diff dort ist genau eine geänderte Zeichenkette. · V-E6 (harte Umbrüche 8/15) ist vermutlich der Kanonisierer, nicht marked.
**Startauftrag B1.4:** „Bau die marked-Erweiterungen (Format inline und Block, Fußnoten ohne IDs) und die Overrides, stell das Tabellen-Widget auf `blockRanges` der Fassade um, extrahiere die GFM-Beispiele einmal als Fixture und ergänze den einen Satz in `_FORMAT_HINT`. Fertig, wenn im Stand S3b `konformitaet` ≥ 95 % ist, alle `l_*`-Zellen grün sind und die drei Gegenläufe genau ihre Zellen kippen."

## B1.5 — Editor-Modus = Wahrheit (E)

**Erlaubte Pfade:** `S/js/editor.js`, `S/js/editor_cm.js`, `S/app.css`, `S/vendor/codemirror/` (nur Entfernen von `xml.min.js`, falls V-E8 es trägt; dann auch `phase5_ui/THIRD_PARTY_LICENSES.md`), Probe, Spec, Tests.
**Bau.** Editor und Lesesicht dürfen sich nicht mehr widersprechen (Editor-Plan F4–F6):
1. Modus-Optionen `strikethrough: true`, `taskLists: true`, `xml: false` an **beiden** Stellen, an denen der Modus gesetzt wird.
2. `theme: "sfx"` und Regeln `.cm-s-sfx .cm-*` über Tokens — die `.cm-s-default`-Farben greifen dann nicht mehr; jede Tokenfarbe ≥ 4,5 : 1 gegen `--editor-bg`.
3. Der Format-Overlay ignoriert Codespans; eine `:::`-Zeile wird nur versteckt, wenn `blockRanges` sie als gültigen Block kennt.
4. Kästchen-Regel = GFM: Leerraum nach `]` Pflicht, auch in nummerierten Listen (`TODO_MUSTER`).
**Nicht** in diesem Schritt: Listenzeichen sichtbar machen (das löst B1.7 durch Punkte).

**Anker.**
| Datei | Zeile | String |
|---|---|---|
| `S/js/editor.js` | 540 | `      mode: { name: "markdown", highlightFormatting: true },` (mit der Folgezeile `      lineWrapping: true,`) |
| `S/js/editor.js` | 740 | `    cm.setOption("mode", on ? null : { name: "markdown", highlightFormatting: true });` |
| `S/js/editor.js` | 462 | `function _formatOverlayToken(stream) {` |
| `S/js/editor.js` | 504 | `if (stream.sol() && /^:::/.test(rest)) { stream.skipToEnd(); return "formatting"; }` |
| `S/js/editor.js` | 625 | `var TODO_MUSTER = /^([ \t]*[-*+][ \t]+)\[([ xX])\]/;` |
| `S/js/editor_cm.js` | 25 | `const VENDOR_SCRIPTS = [` |
| `S/app.css` | 2110 | `.CodeMirror .cm-variable-2, .CodeMirror .cm-variable-3 { color: var(--editor-text); }` |

**Tests.** `test_editor_live.py::test_the_editor_is_created_from_the_textarea_with_the_markdown_mode` und `test_editor_todo.py` mit Absicht anpassen. Bei entferntem `xml.min.js` drei Stellen: `phase10_5_finishing/tests/test_editor_cm.py::test_the_script_list_matches_the_vendor_directory`, die Dateiliste in `phase10_5_finishing/tests/test_codemirror_vendor.py` (Z. 30, `"xml.min.js",`) und die Tabellenzeile in `THIRD_PARTY_LICENSES.md`.
**Abnahme:** P11-6. Stand **S4**: `konflikt_a` bis `konflikt_f`, `kontrast`, `e_durchgestrichen` grün. `listenzeichen` bleibt rot bis B1.7 — das steht so in der Spec.
**Rot-Probe.** `s4_overlay_im_code` → `konflikt_b` · `s4_theme_default` → `kontrast` · `s4_kaestchen_ohne_leerraum` → `konflikt_d`.
**Fallen.** Die Modus-Optionen stehen an **zwei** Stellen; nach `setRawMode(false)` fehlt sonst `strikethrough`. · `- [x]{.rot}` ist danach kein Kästchen mehr: gewollt (GFM), steht im Update-Log.
**Startauftrag B1.5:** „Stell den CM5-Modus auf GFM (durchgestrichen, Aufgaben, kein xml), gib dem Editor ein eigenes Theme mit Kontrast ≥ 4,5 : 1, lass den Overlay Codespans auslassen, versteck `:::` nur bei gültigem Block und zieh die Kästchen-Regel auf GFM. Fertig, wenn im Stand S4 alle `konflikt_*`, `kontrast` und `e_durchgestrichen` grün sind und die drei Gegenläufe genau ihre Zellen kippen."

## B1.6 — Einklappen I: Inline (C)

**Erlaubte Pfade:** neu `S/js/editor/marken.js`; `S/js/editor.js`, `S/app.css`, Probe-Spec, Tests.
**Bau.** `js/editor/marken.js`, per `import()` nach dem Tabellen-Widget geladen:
- `export function installiere(cm, kontext)` → `{ abgleichen(), stat }`; `kontext()` liefert `{ roh }`.
- `_paare(tokens)` → `[{art, von, bis, teile: [{von, bis}]}]` für `strong`, `em`, `strikethrough`, `code` (zwei gleiche `formatting-*`-Tokens derselben Zeile) und Link (`[` … `]` plus `(`, Adresse, `)`). **Unpaariges wird nie eingeklappt.**
- `_formatPaare(text)` → dieselbe Form für `[Text]{.rot}` per Regex aus `FORMAT_VOKABULAR` — diese Zeichen kommen **nicht** aus `getLineTokens` (sie stammen aus dem Overlay).
- `_wunsch(n)` → sortierte Liste `[{von, bis, art}]`: alle Teile aller Paare, deren Bereich der Cursor **nicht** berührt (`cur.line === n && von ≤ cur.ch ≤ bis` heißt berührt).
- `_ist(n)` → die eigenen Marken der Zeile aus `cm.findMarks`, erkannt an `mark.sfxMarke === true`. **Keine eigene Liste** (Undo stellt Marken wieder her).
- `_abgleich()`: für jede Zeile des Sichtbereichs Wunsch gegen Ist; nur bei Abweichung räumen und neu setzen: `cm.markText(von, bis, {collapsed: true, inclusiveLeft: false, inclusiveRight: false})`, danach `mark.sfxMarke = true`. Zeilen unter einem Tabellen-Widget überspringen. Im Rohmodus alle räumen.
- **Auslöser:** `changes`, `cursorActivity`, `viewportChange` → `setTimeout(…, 0)`, zusammengefasst. **Nie** „update". **Mausregel:** `mousedown` in der Hülle setzt `mausUnten`; `mouseup` am Fenster setzt `mausBis = jetzt + MAUS_RUHE_MS` (450); solange eines gilt, wird nicht aufgedeckt.
- CSS: die drei `visibility`-Regeln entfallen; `_cursorZeileSetzen` und `sfx-active-line` bleiben bis B1.7.

**Anker.**
| Datei | Zeile | String |
|---|---|---|
| `S/js/editor.js` | 559 | `    cm.addOverlay({ token: _formatOverlayToken });` |
| `S/js/editor.js` | 555 | `    cm.on("cursorActivity", function () { _cursorZeileSetzen(); });` |
| `S/js/editor.js` | 584 | `function _cursorZeileSetzen() {` |
| `S/app.css` | 2114 | `.CodeMirror .cm-formatting { visibility: hidden; }` |
| `S/app.css` | 2115 | `.CodeMirror .sfx-active-line .cm-formatting { visibility: visible; }` |
| `S/app.css` | 2118 | `.CodeMirror.is-raw .cm-formatting { visibility: visible; }` |

**Tests.** `phase11_editor/tests/test_marken.py` (statisch): Laden nur per `import()`; kein `"update"`-Zuhörer; `sfxMarke` an jeder gesetzten Marke; die Konstante `MAUS_RUHE_MS`. Vorher V221.
**Abnahme:** P11-8 (Inline-Teil), P11-10, P11-11, P11-12. In **diesem** Schritt bleiben `# `, `> ` und Listenzeichen wie heute versteckt — dafür steht bis B1.7 **eine** Übergangsregel in `app.css` (nur `cm-formatting-header`, `-quote`, `-list`).
**Rot-Probe.** `ohne_mausregel` → `doppelklick` und `dreifachklick` rot **in Firefox**, `ziehen` in beiden · `unpaarig_einklappen` → `gleichtext` für `04_grenzen` rot · `eigene_liste` (Buchführung über ein Array statt `findMarks`) → `undo20` rot.
**Fallen.** Rahmen §7: verdoppelte Marken, Endlosschleife, fehlendes Zeichen. · `collapsed` ist in CM5 immer atomar: der Cursor überspringt den Bereich; „aufgedeckt" heißt, die Marke ist weg. · **CM5 wirft** bei teilweise überlappenden eingeklappten Bereichen (`Inserting collapsed marker partially overlapping an existing one`, `markText` in 5.65.16, geprüft am npm-Quelltext 2026-11-14) — die Ausnahme fällt im `setTimeout` und sieht aus wie „ab hier fehlen alle Marken". `_wunsch` vereinigt deshalb überlappende Teile zu einem Bereich, bevor gesetzt wird; angrenzende Bereiche (`***x***`, `**[x](y)**`) sind erlaubt. · `tastenkosten` über 8 ms: der Abgleich räumt Marken ohne Signaturvergleich (V235).
**Startauftrag B1.6:** „Bau `js/editor/marken.js`: Inline-Paare und Format-Formen werden per `markText` eingeklappt und nur aufgedeckt, solange der Cursor das Element berührt; Maus erst 450 ms nach dem Loslassen; Buchführung nur über `cm.findMarks`. Fertig, wenn `klick30`, `doppelklick`, `dreifachklick`, `ziehen`, `grenzen`, `undo20` in beiden Browsern grün sind, `tastenkosten` ≤ 8 ms ist und die drei Gegenläufe genau ihre Zellen kippen."

## B1.7 — Einklappen II: Blockmarker, Listen, Kästchen (C 🖼)

**Erlaubte Pfade:** `S/js/editor/marken.js`, `S/js/editor.js`, `S/app.css`, Probe-Spec, Tests.
**Bau.** Der **eine Zeilenbauer** in `marken.js` übernimmt alles, was eine Zeile trägt:
- Überschrift: `# ` eingeklappt außer auf der Cursorzeile. Zitat: `> ` ebenso, dazu Zeilenklasse `sfx-zitat` (Balken links).
- Liste: führender Leerraum eingeklappt; Zeilenklasse `sfx-liste` und `sfx-ebene-1…5` (Ebene aus `state.listStack` des Modus); `- `/`* `/`+ ` wird ein Punkt-Widget (`span.sfx-punkt`), außer der Cursor steht im Zeichen; Nummern bleiben Text. Hängender Einzug per CSS.
- Aufgabe: das Kästchen aus `editor.js` zieht in den Zeilenbauer um (`_todoKasten`, `_todoMarkenAuffrischen`, `cmTodoMarken`); `editor.js` behält nur `_todoUmschalten` und gibt es als `kontext.todoKlick` hinein. Das Listenzeichen vor einem Kästchen wird eingeklappt.
- Zaun, eingerückter Code, Trennlinie: Zeilenklassen aus `blockRanges` (Fläche wie `.preview pre`).
- Entfällt: die Übergangsregel aus B1.6, `_cursorZeileSetzen`, `sfx-active-line`.

**Anker.**
| Datei | Zeile | String |
|---|---|---|
| `S/js/editor.js` | 67 | `var cmTodoMarken = [];` |
| `S/js/editor.js` | 551 | `    cm.on("change", _todoMarkenAuffrischen);` |
| `S/js/editor.js` | 630 | `function _todoKasten(erledigt) {` |
| `S/js/editor.js` | 653 | `function _todoUmschalten(kasten) {` |
| `S/js/editor.js` | 679 | `function _todoMarkenAuffrischen() {` |
| `S/js/editor.js` | 747 | `  _todoMarkenAuffrischen();` (mit der Folgezeile `  if (cmTabellen) cmTabellen.abgleichen();`) |
| `S/app.css` | 2132 | `.sfx-todo,` (mit `.preview .md-todo {`) |

**Tests.** `test_editor_todo.py` mit Absicht umgestellt (die Erkennung liegt jetzt in `marken.js`; der Schreibweg `_todoUmschalten` → `saveItem()` bleibt in `editor.js` und wird weiter geprüft: Hard Rule 3).
**Abnahme:** P11-8 (ganz), P11-9, P11-12, P11-13; Darstellungs-Probe: `listenzeichen` grün (die Zelle prüft dann den Punkt); `e_aufgabe` bleibt grün. **Bilder:** `02_notiz` ganz, Cursor in Überschrift, im Listenpunkt, im Link; `28_katalog`.
**Rot-Probe.** `punkt_weg` → `listenpunkt` · `ebene_flach` → `ebenen` · `raute_sichtbar` → `kante` und `marker_eingeklappt` · `kaestchen_alt` (die Erkennung zurück nach `editor.js`, ohne Zeilenbauer) → `undo20`.
**Fallen.** „Pos1 landet vor dem Punkt, Getipptes zerstört den Listenpunkt": das Widget braucht `selectLeft: false` (Verhalten in der Sitzung messen, Zelle `grenzen`). · Rollbalken springt in `27_gross` (V225): CM5 schätzt Höhen aus der Zeichenzahl und zählt Eingeklapptes mit — messen, ob Zeile 1500 nach dem Sprung im Bild steht.
**Startauftrag B1.7:** „Erweitere `marken.js` zum einen Zeilenbauer: Überschrift- und Zitatzeichen, Listenpunkt als Widget mit Ebenen-Einzug, Kästchen aus `editor.js` übernommen, Code- und Trennlinien als Zeilenklassen. Fertig, wenn `marker_eingeklappt`, `kante`, `gleichtext`, `listenpunkt`, `ebenen`, `kaestchen` grün sind, `tastenkosten` ≤ 8 ms bleibt, die vier Gegenläufe genau ihre Zellen kippen und die Bilder im Session-Block stehen."

## B1.8 — Listen und Tasten (E)

**Erlaubte Pfade:** neu `S/js/editor/tasten.js`; `S/js/editor.js`, `S/app.html`, `phase5_ui/scripts/build_icon_sprite.py` (nur zwei Icons), Probe-Spec, Tests.
**Bau.** `js/editor/tasten.js`: `export function installiere(cm, aktionen)` setzt `cm.addKeyMap({...})`:
- **Enter** in einem Listen- oder Aufgabenpunkt setzt fort (gleiche Ebene, nächste Nummer, leeres Kästchen); ein **leerer** Punkt beendet die Liste.
- **Tab / Umschalt+Tab** im Listenpunkt stufen um eine Ebene (Einzug auf die Inhaltsspalte des Elternpunkts: `- ` → 2, `1. ` → 3). Außerhalb von Listen und Tabellen fügt Tab **zwei Leerzeichen** ein (E8), nie `\t`.
- **Rücktaste** am Inhaltsanfang eines Listenpunkts, einer Überschrift oder eines Zitats entfernt das **ganze** Zeichen (aus `- Text` wird `Text`).
- **Strg/Cmd+B, I, K** rufen `aktionen.bold`, `.italic`, `.link`.
- Zwei neue Knöpfe in der Leiste: Durchgestrichen (`data-md="strike"`) und Aufgabe (`data-md="task"`), mit Icons aus dem Sprite (V232).
- Umnummerieren nur bei Enter und Tab in der **eigenen** Liste (V3).

**Anker.**
| Datei | Zeile | String |
|---|---|---|
| `S/js/editor.js` | 1183 | `  function wrapSelection(marker) {` |
| `S/js/editor.js` | 1190 | `  function insertLinePrefix(prefix) {` |
| `S/js/editor.js` | 1196 | `  var TOOLBAR_ACTIONS = {` |
| `S/app.html` | 321 | `<button type="button" class="toolbar-btn" data-md="code" title="Code" aria-label="Code">` |
| `S/app.html` | 336 | `<button type="button" class="toolbar-btn" data-md="ol" title="Nummerierung" aria-label="Nummerierung">` |

**Tests.** `test_knopfleiste_word.py` um die zwei Knöpfe erweitern (Reihenfolge nach Word: Durchgestrichen in „Schriftart", Aufgabe in „Absatz").
**Abnahme:** P11-14 (Zellen `liste_enter`, `liste_leer_beendet`, `liste_tab`, `taste_rueck_marker`, `taste_tab_leerzeichen`, `taste_strg_b`, je mit erwartetem Body-Diff).
**Rot-Probe.** Je Regel ein Patch: z. B. `tab_tabulator` (`\t` statt zwei Leerzeichen) → nur `taste_tab_leerzeichen`.
**Fallen.** `TOOLBAR_ACTIONS` liegt **in** `init()`: die Tastatur bekommt die Funktionen übergeben, sie werden nicht kopiert. · Strg+B im Browser öffnet Lesezeichen, wenn `preventDefault` fehlt.
**Startauftrag B1.8:** „Bau `js/editor/tasten.js` mit den Listen- und Tastenregeln des Plans und ergänze die Knöpfe Durchgestrichen und Aufgabe. Fertig, wenn alle `liste_*`- und `taste_*`-Zellen in beiden Browsern grün sind und jeder Gegenlauf genau seine Zelle kippt."

## B1.9 — Raster I: Zelle wählen und bearbeiten (C 🖼)

**Erlaubte Pfade:** neu `S/js/editor/raster.js`; `S/js/editor/tabellen.js`, `S/app.css`, Probe-Spec, Tests.
**Bau.** `js/editor/raster.js` (Bedienung; `tabellen.js` bleibt das Widget):
- `export function zellBereiche(zeile)` → `[{von, bis}]`: Teilung an jedem `|`, vor dem eine **gerade** Zahl von `\` steht; Außen-Pipes ab; je Zelle der **getrimmte** Inhalt; eine leere Zelle bekommt die Stelle nach dem ersten Leerzeichen.
- `export function maskiere(text)` → `|` ohne `\` davor wird `\|`; Zeilenumbruch wird `<br>`.
- `export function installiere(cm, tabellen)`: Zustand `aktiv = {von, r, c}` (Tabellenanfang, Zeile, Spalte).
  - Klick auf eine Zelle wählt sie (Klasse `sfx-zelle-aktiv`), Fokus auf die Hülle (`tabIndex = 0`).
  - Tasten an der Hülle: Pfeile bewegen; **Tippen ersetzt** (Eingabefeld mit dem Zeichen); **F2, Enter, Doppelklick** öffnen das Eingabefeld mit dem **Quelltext** der Zelle; **Entf** leert; **Strg/Cmd+Z und +Y** rufen `cm.undo()`/`cm.redo()` und wählen dieselbe Zelle wieder.
  - Im Eingabefeld (`input.sfx-zelle-eingabe`): **Enter** schreibt und geht eine Zeile tiefer, **Tab** / **Umschalt+Tab** schreiben und gehen nach rechts / links, **Esc** verwirft, Verlassen schreibt.
  - Schreiben = `cm.changeGeneration(true)`, dann `cm.replaceRange(maskiere(wert), {line, ch: von}, {line, ch: bis}, "+sfxzelle")`, **nur** wenn sich der Text ändert; danach synchron `tabellen.abgleichen()` und dieselbe Zelle wieder wählen. **Warum `changeGeneration(true)`:** CM5 verschmilzt eine Änderung mit dem letzten Undo-Schritt, wenn ihr Ursprung gleich ist, mit `+` beginnt und weniger als `historyEventDelay` (1250 ms) vergangen sind (`addChangeToHistory`, 5.65.16) — ohne den Schnitt macht **ein** Strg+Z zwei schnell nacheinander bearbeitete Zellen rückgängig.
  - **Esc** (im Eingabefeld: verwerfen; an der gewählten Zelle: Auswahl lösen, Fokus an CodeMirror) ruft immer `e.stopPropagation()`: die globale Esc-Kette in `app.js:317 ff.` (nur lesen, kein Edit) schließt sonst die ganze Notiz. Esc schließt nie den Editor aus dem Raster heraus; erst ein zweites Esc in CodeMirror tut es, wie heute.
  - **Klick auf einen Link in einer Zelle** wählt nur die Zelle: ein `click`-Zuhörer an der Hülle ruft bei `e.target.closest("a")` `preventDefault()` und `stopPropagation()`. Sonst wechselt `app.js:135 ff.` per `selectItem()` die Notiz **ohne** Rückfrage (heute schützt davor nur, dass `_klick` das Widget schon beim `mousedown` entfernt), und ein `https://`-Link verlässt die App. Folgen erst mit Strg/Cmd+Klick (B1.13).
  - Pfeil nach oben aus der Kopfzeile oder nach unten aus der letzten Zeile gibt den Fokus an CodeMirror zurück (Cursor in der Zeile davor oder danach). Der bestehende Eintritt per Pfeil (`_eintritt`) wählt statt des Quelltexts die erste oder letzte Zelle.
- **Rückfall auf den Rohtext** (das heutige Verhalten: Widget weg, Cursor in die Quelle): wenn die Zahl der Zellen in Quelle und Darstellung in **irgendeiner** Zeile der Tabelle abweicht, oder über den Knopf „Quelltext" an der Tabelle.
- `tabellen.js`: der `change`-Zuhörer räumt nicht bei Ursprung `+sfxzelle`; die Hülle bekommt Raster statt `_klick`.

**Anker.**
| Datei | Zeile | String |
|---|---|---|
| `S/js/editor/tabellen.js` | 90 | `export function zellAnfaenge(zeile) {` |
| `S/js/editor/tabellen.js` | 181 | `    var mark = cm.markText({ line: w.von, ch: 0 }, { line: w.bis, ch: w.laenge },` |
| `S/js/editor/tabellen.js` | 183 | `    huelle.addEventListener("mousedown", function (e) { _klick(e, mark); });` |
| `S/js/editor/tabellen.js` | 201 | `  function _klick(e, mark) {` |
| `S/js/editor/tabellen.js` | 222 | `  function _eintritt(_cm, obj) {` |
| `S/js/editor/tabellen.js` | 243 | `  cm.on("change", function (_cm, ch) {` |
| `S/js/editor/tabellen.js` | 257 | `  cm.state.sfxTabellen = {` |

**Tests.** `phase11_editor/tests/test_raster.py`: `zellBereiche` und `maskiere` als reine Funktionen in Node (Muster `test_ed41_tabellen.py:128`), Fälle aus `03_raster.txt`. Mit Absicht geändert: `test_ed41_tabellen.py::test_the_cell_starts_follow_the_renderers_split`, `::test_the_widget_does_not_write_history_or_text` (das Raster schreibt — über `replaceRange`, nie anders). Die S2-Zelle `klick_zelle` der Darstellungs-Probe wird abgelöst (Klick wählt, statt die Quelle zu öffnen): Spec datiert nachziehen.
**Abnahme:** P11-15: `raster_waehlen`, `raster_pfeile`, `raster_tippen_ersetzt`, `raster_f2_quelltext`, `raster_enter_tab`, `raster_esc`, `raster_entf`, `raster_undo`, `raster_pipe`, `raster_rueckfall`, `raster_raus_rein`, `raster_link_klick`; `bytes_zelle`: der Body-Diff ist genau die eine Zelle. **Messung `raster_undo`:** zwei Zellen im Abstand < 1 s bearbeiten, dann **ein** Strg+Z → nur die zweite Zelle ist zurück. **Messung `raster_esc`:** Esc im Eingabefeld und Esc an der gewählten Zelle → die Notiz bleibt offen (`#detail` zeigt den Editor). **Bilder:** gewählte Zelle, offenes Eingabefeld, Tabelle mit Rückfall.
**Rot-Probe.** `raster_polstert` (Schreiben füllt die Spalte auf) → nur `bytes_zelle` · `ohne_maske` → nur `raster_pipe` · `ohne_ursprung` (der `change`-Zuhörer räumt immer) → `raster_enter_tab` (die nächste Zelle ist nicht gewählt) · `ohne_generation` (kein `changeGeneration(true)`) → nur `raster_undo` · `esc_blubbert` (kein `stopPropagation`) → nur `raster_esc` · `link_klick_durch` (kein `click`-Zuhörer) → nur `raster_link_klick` (Klick auf `#item/…` und `https://…` in einer Zelle: Notiz und URL bleiben, die Zelle ist gewählt).
**Fallen.** Gemessen 2026-11-13 (Machbarkeitstest): CodeMirror nimmt dem Raster den Fokus nicht; `cm.hasFocus()` ist `false`, solange eine Zelle gewählt ist. · Schwarzer Balken unter der Seite: DOM-`scrollIntoView` (Rahmen §7). · Die Zelle `<br>` zeigt in der Anzeige einen Umbruch, im Eingabefeld `<br>` — das ist die Regel (P11-G), kein Fehler.
**Startauftrag B1.9:** „Bau `js/editor/raster.js`: Zellcursor, Pfeile, Tippen ersetzt, F2/Enter/Doppelklick bearbeiten den Quelltext der Zelle in einem Eingabefeld, Enter und Tab schreiben per `replaceRange` genau diese Zelle, Esc verwirft, Rückfall auf den Rohtext bei abweichender Zellzahl. Fertig, wenn alle `raster_*`-Zellen und `bytes_zelle` in beiden Browsern grün sind, die sechs Gegenläufe genau ihre Zellen kippen und drei Bilder im Session-Block stehen."

## B1.10 — Raster II: Struktur (E)

**Erlaubte Pfade:** `S/js/editor/raster.js`, `S/app.html`, `S/app.css`, Probe-Spec, Tests.
**Bau.** Befehle auf der gewählten Zelle, jeder als **ein** `cm.operation` (ein Undo-Schritt): `zeileEinfuegen("davor"|"danach")`, `zeileLoeschen()`, `spalteEinfuegen("links"|"rechts")`, `spalteLoeschen()`, `ausrichtung("links"|"mitte"|"rechts"|"keine")` (ändert nur die Trennerzelle), `tabelleEinfuegen()` (3 × 2 an der Cursorzeile, Knopf in der Leiste, Gruppe „Einfügen"). **Tab in der letzten Zelle** legt eine Zeile an (wie in Word). Bedienung: eine kleine Leiste über der gewählten Tabelle (`div.sfx-raster-leiste`, sechs Knöpfe mit `aria-label`). Neue Zeilen und Zellen folgen dem Stil der Nachbarzeile (Außen-Pipes ja oder nein, ein Leerzeichen innen); nichts wird aufgefüllt.
**Anker.** `S/app.html:349` `<div class="toolbar-group" data-word-group="einfuegen">` — der Knopf „Tabelle einfügen" kommt in diese Gruppe (nach „Link"); `test_knopfleiste_word.py` kennt die Gruppen. `raster.js` entsteht in B1.9 und hat noch keine Anker.
**Tests.** Reine Funktionen `zeileNeu(nachbar, spalten)`, `ohneSpalte(zeile, c)`, `mitSpalte(zeile, c)` in Node; `test_knopfleiste_word.py` um den Knopf erweitern.
**Ursprung und Undo.** Jeder Befehl schreibt mit dem Ursprung `sfxraster` — **ohne** `+`: dann verschmilzt CM5 nur Änderungen derselben `cm.operation` (gleiche Operation-ID), nie zwei Befehle nacheinander, und der Gegenlauf unten kann beißen. Die Ausnahme im `change`-Zuhörer von `tabellen.js` (B1.9) gilt genau für `+sfxzelle` und `sfxraster`, für keinen anderen Ursprung.
**Fallen.** `ausrichtung` schreibt nur die Trennerzeile; die Zellen behalten ihre Bytes (V8). · Mit einem `+`-Ursprung bliebe die Zelle `raster_op_ein_undo` auch ohne `cm.operation` grün (CM5 verschmilzt gleiche `+`-Ursprünge binnen 1250 ms) — zahnlos.
**Abnahme:** P11-16: je Befehl eine Zelle `raster_op_*` mit **erwartetem Body-Diff** (Zeilennummern und Inhalt); die Kopfzeile lässt sich nicht löschen; die letzte Spalte lässt sich nicht löschen; `raster_op_ein_undo`: nach `spalteEinfuegen` stellt **ein** Strg+Z den Body byte-gleich wieder her.
**Rot-Probe.** Je Befehl ein Patch, z. B. `spalte_nur_kopf` (die Spalte wird nur in der Kopfzeile eingefügt) → nur `raster_op_spalte_ein` · `op_ohne_operation` (die Zeilen einzeln, ohne `cm.operation`) → nur `raster_op_ein_undo`.
**Startauftrag B1.10:** „Erweitere das Raster um die Strukturbefehle des Plans, je als ein Undo-Schritt, mit einer kleinen Leiste über der gewählten Tabelle. Fertig, wenn jede `raster_op_*`-Zelle den erwarteten Body-Diff zeigt und jeder Gegenlauf genau seine Zelle kippt."

## B1.11 — Raster III: Bereich und Zwischenablage (E)

**Erlaubte Pfade:** `S/js/editor/raster.js`, `S/app.css`, Probe-Spec, Tests.
**Bau.** **Bereich:** Umschalt+Pfeile, Umschalt+Klick und Ziehen wählen ein Rechteck (`sfx-zelle-bereich`). **Kopieren (Strg/Cmd+C)** legt den **Quelltext** der Zellen als TSV in die Zwischenablage (Zeilen `\n`, Zellen `\t`). **Einfügen (Strg/Cmd+V)** in eine gewählte Zelle: TSV oder eine HTML-Tabelle (`DOMParser`, nur `textContent`, **nie** Markup) füllt ab der Zelle nach rechts und unten; fehlende **Zeilen** werden angelegt, zu viele **Spalten** führen zum Abbruch mit Meldung (nichts wird geschrieben). **Entf** leert den Bereich. Einfügen einer HTML- oder TSV-Tabelle **außerhalb** einer Tabelle erzeugt eine Markdown-Tabelle an der Cursorzeile.
**Tests.** Reine Funktionen in Node: `alsTsv(matrix)` und `ausTsv(text)` (Rundlauf; `\t` und Zeilenumbruch in einer Zelle). `ausHtmlTabelle` braucht `DOMParser` und wird nur in der Probe gemessen.
**Abnahme:** P11-17: `raster_ablage_kopie`, `raster_ablage_tsv`, `raster_ablage_html_nur_text` (eine HTML-Tabelle mit `<script>` und `onerror` ergibt nur Text), `raster_ablage_zu_breit` (0 Bytes Änderung).
**Rot-Probe.** `html_als_markup` (statt `textContent` wird `innerHTML` übernommen) → `raster_ablage_html_nur_text` rot.
**Fallen.** Die Zwischenablage-API braucht in Chromium eine Berechtigung (`context.grant_permissions`), in Firefox geht nur der Weg über ein künstliches `paste`-Ereignis: die Probe misst beide Wege, nicht denselben.
**Startauftrag B1.11:** „Bau Bereichsauswahl, Kopieren als TSV und Einfügen von TSV und HTML-Tabellen (nur Text) ins Raster. Fertig, wenn die vier `raster_ablage_*`-Zellen grün sind und der Gegenlauf `html_als_markup` genau seine Zelle kippt."

## B1.12 — Suchen und Ersetzen (E)

**Erlaubte Pfade:** neu `S/js/editor/suche.js`; `S/vendor/codemirror/searchcursor.js`, `S/js/editor_cm.js`, `S/js/editor.js`, `S/js/app.js` (nur die Esc-Reihenfolge), `S/app.html`, `S/app.css`, Lizenzdatei, Probe-Spec, Tests.
**Bau.** `searchcursor` 5.65.16 vendoren, **ohne Netz** und unverändert: `addon/search/searchcursor.js` aus `npm pack codemirror@5.65.16 --offline` (npm-Cache dieser VM; 12.234 B, gzip ≈ 3,1 KB, SHA-256 `2c0b8cd8fe7ca5ca2253f4aacc914b390bff5b3cac3475df66c43a9ea8c8ccbe`, geprüft 2026-11-14). Die Datei ist nicht minifiziert — gewollt: die jsDelivr-`.min.js` gäbe es nur über das Netz (V234 ✅), die 1 KB mehr trägt der Korridor „Editor nachgeladen" (≤ 100 KB). Eintragen an drei Stellen: `VENDOR_SCRIPTS`, Tabelle in `THIRD_PARTY_LICENSES.md`, Liste in `test_codemirror_vendor.py`. `js/editor/suche.js`: ein eigenes deutsches Feld über dem Editor (kein `dialog.js`): Suchen, Groß/klein, nächster, voriger, Ersetzen, Alle ersetzen (**ein** Undo-Schritt per `cm.operation`, Ursprung `sfxsuche` **ohne** `+` — mit `+` verschmölze CM5 die Ersetzungen auch ohne `cm.operation`, und der Gegenlauf wäre zahnlos). Strg/Cmd+F und +H nur bei Fokus im Editor; Esc schließt zuerst das Feld. Ein Treffer wird gewählt — damit deckt die Aufdeck-Regel ihn von selbst auf. Treffer in Tabellen: das Raster gibt den Fokus ab, der Treffer steht im Quelltext (Rückfall-Weg).
**Anker.**
| Datei | Zeile | String |
|---|---|---|
| `S/js/editor_cm.js` | 29 | `  "markdown.min.js",` (mit der Folgezeile `];`) |
| `S/js/app.js` | 337 | `      else if (state.selectedId !== null) Editor.closeEditor();` — die Zeile davor bekommt `else if (<Suchfeld offen>) <schließen>;` |
| `phase5_ui/THIRD_PARTY_LICENSES.md` | 51 | `` \| `meta.min.js` \| `` (Zeilenanfang; die neue Zeile folgt darunter) |
| `phase10_5_finishing/tests/test_codemirror_vendor.py` | 31 | `    "meta.min.js",` |

**Tests.** Neu `phase11_editor/tests/test_suche.py` (statisch): `suche.js` nur per `import()`; „Alle ersetzen" liegt in `cm.operation` und schreibt mit dem Ursprung `sfxsuche`; Strg+F/H nur mit `preventDefault`. Mit Absicht geändert: `test_codemirror_vendor.py` (Liste + Prüfsumme), `test_editor_cm.py::test_the_script_list_matches_the_vendor_directory`.
**Fallen.** Ohne `preventDefault` öffnet Strg+F die Suche des Browsers. · Esc schließt die Notiz statt des Felds: die neue Zeile steht **nach** `closeEditor` oder gar nicht in der Kette. · Ersetzen in einer Tabelle räumt das Widget (Rückfall auf den Quelltext): gewollt — `sfxsuche` steht **nicht** in der Ausnahme des `change`-Zuhörers.
**Abnahme:** P11-19: `suche_findet_1500` in `27_gross`, `suche_alle_ein_undo`, `suche_esc_laesst_editor_offen`, `suche_treffer_aufgedeckt`.
**Rot-Probe.** `ohne_operation` (Alle ersetzen ohne `cm.operation`) → `suche_alle_ein_undo`.
**Startauftrag B1.12:** „Vendore `searchcursor` 5.65.16 und bau `js/editor/suche.js` mit eigenem Feld: Suchen, Ersetzen, Alle ersetzen als ein Undo-Schritt. Fertig, wenn die vier `suche_*`-Zellen grün sind und der Gegenlauf genau seine Zelle kippt."

## B1.13 — Komfort und Glyphen (E, streichbar)

**Erlaubte Pfade:** neu `S/js/editor/komfort.js`; `S/js/editor.js`, `S/js/dialogs.js`, `S/app.html`, `S/app.css`, `S/fonts/`, `phase5_ui/scripts/build_font_subset_plex.sh`, Probe-Spec, Tests.
**Bau.** `js/editor/komfort.js` (per `import()` wie `marken.js`), `export function installiere(cm, kontext)`:
1. **Gliederung:** ein Knopf am Ende der Gruppe „vorlagen" öffnet eine Liste der Überschriften h1–h3 aus `blockRanges(cm.getValue())`; Klick setzt den Cursor an den Zeilenanfang und ruft `cm.scrollIntoView(pos, 80)`.
2. **Zählung:** `<span class="editor__zaehlung" id="editor-zaehlung">` am Ende der Anhängen-Zeile: „N Wörter · M Zeichen" des **sichtbaren** Texts (wie `gleichtext`), 300 ms entprellt nach `changes`.
3. **Strg/Cmd+Klick auf einen Link** (im Text und in einer Rasterzelle): `#item/itm_…` → `closeEditor().then(function (weiter) { if (weiter) selectItem(id); })` — `selectItem` allein fragt **nicht** (geprüft: `editor.js:933`; Muster `list.js:124`); `http(s)` → `window.open(url, "_blank", "noopener")`. Ohne Strg/Cmd bleibt ein Klick ein Klick in den Text.
4. **Konfliktdialog (E11):** unter `#conflict-message` ein Zeilenvergleich „deine Fassung ↔ aktuelle Fassung" (LCS über Zeilen, nur Anzeige, `textContent`, nie `innerHTML`); `showConflictDialog(current, opts)` bekommt den eigenen Body über `opts.mein`.
5. **Glyphen:** die `UNICODES`-Zeile um `U+2190,U+2192,U+21D2,U+2713,U+2717,U+2264,U+2265,U+2248` erweitern — **acht** neue Zeichen; `U+2191` und `U+2193` stehen schon drin (geprüft 2026-11-14). Beide Teilmengen neu bauen, Dateinamen mit neuem Hash, `@font-face` in `app.css` nachziehen.

**Anker.**
| Datei | Zeile | String |
|---|---|---|
| `S/app.html` | 345 | `<div class="toolbar-group" data-word-group="vorlagen">` |
| `S/app.html` | 369 | `<div class="editor__append">` |
| `S/app.html` | 728 | `<p id="conflict-message"></p>` |
| `S/js/dialogs.js` | 455 | `export function showConflictDialog(current, opts) {` |
| `phase5_ui/scripts/build_font_subset_plex.sh` | 32 | `UNICODES="U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD"` |
| `S/app.css` | 15 | `  src: url("/ui/static/fonts/IBMPlexSans-subset.6c21979f.woff2") format("woff2");` |
| `S/app.css` | 22 | `  src: url("/ui/static/fonts/IBMPlexMono-subset.a8d5dfa6.woff2") format("woff2");` |

**Tests.** Neu `phase11_editor/tests/test_komfort.py`: der LCS-Zeilenvergleich als reine Funktion in Node (gleich, eingefügt, gelöscht, geändert); `komfort.js` nur per `import()`; kein `innerHTML` im Konfliktvergleich. Mit Absicht geändert: `phase10_5_finishing/tests/test_film_stage.py:239–240` (pinnt die zwei Font-Dateinamen). `test_static_routes.py:73` liest die Fonts per Glob und bleibt.
**Abnahme:** P11-28: `gliederung`, `link_folgen_fragt` (Strg+Klick auf `#item/…` bei ungespeicherter Änderung zeigt die Rückfrage), `glyphen` (die Breite von `→ ✓ ≤` wird mit Plex gemessen, nicht mit der Ersatzschrift); Erstaufruf wächst um < 2 KB.
**Rot-Probe.** `alte_teilmenge` → nur `glyphen` · `folgen_ohne_frage` (`selectItem` direkt) → nur `link_folgen_fragt`.
**Fallen.** **Der Font-Neubau braucht Netz:** `build_font_subset_plex.sh` lädt zwei Release-Zips von GitHub (SHA-256-gepinnt) — Auslöser §2.3 Nr. 6. Mit OK des Nikingers (Kosten: keine) baut Claude Code den Glyphen-Teil, sonst entfällt Nr. 5 und P11-28 zählt ⚠️. Werkzeuge: `PATH=~/.claude-code-tools/film-venv/bin:$PATH` (dort liegen `fontTools` und `brotli`, geprüft 2026-11-14; V-E9 ✅); die Projekt-venv hat beide nicht. · Klick auf einen Link öffnet die Notiz, ohne zu fragen: der Weg führte an `closeEditor()` vorbei.
**Startauftrag B1.13:** „Bau `js/editor/komfort.js` mit Gliederung, Zählung, Strg/Cmd+Klick auf Links (mit Rückfrage) und dem Zeilenvergleich im Konfliktdialog; den Glyphen-Teil nur, wenn der Nikinger den Download freigegeben hat. Fertig, wenn `gliederung` und `link_folgen_fragt` grün sind, beide Gegenläufe genau ihre Zelle kippen und `ui_budget` alle Zeilen OK meldet."

## B1.14 — Darstellungs-Gate (C)

**Erlaubte Pfade:** `phase11_editor/`, `phase10_5_finishing/probes/` (Spec und Gegenläufe), `phase8_5_picker_release/scripts/health_gate.sh` (nur der neue Schalter), Head.
**Bau.** 1. Beide Proben in beiden Browsern; **jede** Zelle hat einen Gegenlauf, der genau sie rot macht — fehlende bauen, zahnlose neu bauen. 2. `phase11_editor/tests/test_p11_katalog.py`: jedes Konstrukt des Katalogs hat Fixture-Abschnitt, Zelle und Gegenlauf; Vendor-SHA-256 = Lizenzdatei. 3. `health_gate.sh --render-katalog` (optional): ruft `phase11_editor/scripts/render_katalog.py --base-url=…` auf — nur lesende GETs auf die Static-Route; `js/markdown.js` nennt jedes Konstrukt, `vendor/marked/marked.esm.js` hat den SHA-256 des Releases. Der Kern `pruefe(markdown_js, marked_bytes, sha) -> list[str]` ist eine reine Funktion und wird ohne Server getestet (`health_gate.sh` selbst hat bis heute keinen eigenen Test; `test_deploy_scripts.py` prüft nur das Gate in `deploy.sh`). 4. Byte-Vertrag V1–V8 über beide Korpora. 5. Der Ablauf §2.4 wortgleich in den Head. 6. V224 (Safari), wenn Bedarf 8 erfüllt ist.
**Anker.** `phase8_5_picker_release/scripts/health_gate.sh:44` `    --expected-sha=*)     EXPECTED_SHA="${1#*=}" ;;` — der neue Schalter kommt als nächster `case`-Zweig darunter.
**Tests.** `test_p11_katalog.py` (Nr. 2) · neu `phase11_editor/tests/test_render_katalog.py`: `pruefe()` mit richtigem SHA → leer, mit vertauschter Datei → ein Befund, mit fehlendem Konstrukt → ein Befund.
**Abnahme:** P11-23, P11-25. **Rot-Probe:** ein Konstrukt ohne Fixture → der Katalog-Wächter ist rot; die Liste aller Gegenläufe mit `kippt_genau` steht im Beleg.
**Startauftrag B1.14:** „Schließ das Darstellungs-Gate: jede Zelle beider Proben bekommt einen Gegenlauf, der genau sie kippt; bau den Katalog-Wächter und den optionalen statischen Check in `health_gate.sh`; trag den Deploy-Ablauf in den Head ein. Fertig, wenn beide Proben in beiden Browsern grün sind und jeder Gegenlauf `kippt_genau` meldet."

## B1.15 — Sichtung auf der Probe-Instanz (C + **N**) 🖼 📊

**Hier wird gegen echte Daten geprüft** — die Stelle der Sequenz, die die Lehre aus Deploy D verlangt.
**Bau.** 1. **N:** die Befehle iii–v aus B0.3, wortgleich und in dieser Reihenfolge (Kopie → Deploy mit Neustart → `health_gate` mit `--current-link=/opt/sharefyx/staging`). 2. **N + C:** Sichtung von ≥ 5 echten Notizen: die größte (1836 Zeilen), eine mit breiter Tabelle, eine Aufgabenliste, eine von einem KI-Client geschriebene, eine aus Fabians Space (Lesesicht). Je Notiz: sieht sie aus wie ein Dokument? Tippen, eine Zelle ändern, speichern — **nur in der Kopie**. 3. **C:** jeder Fund wird eine Fixture im Korpus und eine Zelle, dann der Fix (eigene Sitzung, wenn nötig). 4. V223 (IME, Rechtschreib-Unterstreichung), V229.
**Abnahme:** P11-26 — das Urteil des Nikingers, mit Datum und den Namen der fünf Notizen im Head (keine Inhalte).
**Rot-Probe:** ein Fund ohne Fixture ist kein erledigter Fund.
**Fallen.** Echte Inhalte gehören nie in das Repo: Fixtures aus Funden werden **nachgebaut**, nicht kopiert (das Repo ist öffentlich).
**Startauftrag B1.15:** „Begleite die Sichtung des Nikingers auf der Probe-Instanz: bereite die Befehle vor, nimm jeden Fund als nachgebaute Fixture mit Zelle auf und behebe ihn. Fertig, wenn der Nikinger P11-26 abnimmt."

## B1.16 — Release `v4.1.0` (C + **N**)

**Erlaubte Pfade:** `S/app.html` (nur das Badge), `docs/UPDATE_LOG.md`, Head, `ROADMAP.md`, Wurzel-`CLAUDE.md`, Memory.
**Anker.**
| Datei | Zeile | String |
|---|---|---|
| `S/app.html` | 25 | `<span class="rail__version">v4.0.2</span>` |
| `docs/UPDATE_LOG.md` | 12 | `## 2026-11-06` (der neue Eintrag kommt darüber) |

**Bau.** Ablauf §2.4 D0–D7. Update-Log in menschlicher Sprache: der Editor sieht aus wie ein Dokument; Tabellen wie in Excel; Suchen und Ersetzen; `- [x]{.rot}` ist kein Kästchen mehr; Entitäten wie `&amp;` erscheinen als Zeichen. Fabian kurz Bescheid (Neustart).
**Abnahme:** P11-27. **Rot-Probe:** `health_gate` mit der **echten** Ausgabe im Session-Block; eine Behauptung zählt nicht.
**Fallen.** `deploy.sh` verlangt als oberste `##`-Überschrift im Update-Log den Deploy-Tag (UTC oder lokal): den Eintrag am Deploy-Tag datieren, sonst bricht der Deploy ab — für die Produktion **nie** `SHAREFYX_ALLOW_STALE_UPDATELOG=1`. · `health_gate --require-todays-update-log` nur am Deploy-Tag (Datumsfalle, Deploy F). · Gate 5 vergleicht das Badge mit `--expected-version`; ohne den Schalter gilt die veraltete Vorgabe `v3.0.1`.
**Startauftrag B1.16:** „Bereite das Release `v4.1.0` nach §2.4 vor (D0–D3) und lies nach dem Deploy des Nikingers die echte `health_gate`-Ausgabe in den Session-Block. Du deployst nicht selbst."
