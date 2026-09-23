---
status: live
purpose: Archiv der rotierten Phase-9-Session-Blöcke, verbatim, newest-first
read-when: Chronik einer älteren P9-Session gesucht — nicht beim normalen Arbeiten in der Phase
detail: L3
up: ./CLAUDE.md
down:
updated: 2026-09-23 (erste Rotation — Step-0-Block aus dem Head verschoben, verbatim) | 2026-09-20 (angelegt, noch leer)
---

# Phase 9 — Sessions Archive

Leer. Rotation per `scripts/rotate_session_block.sh phase9_hardening`, sobald
`phase9_hardening/CLAUDE.md` einen zweiten `## Session stopped`-Block trägt.

## Session stopped — 2026-09-20

**Step 0 ✅ — Claude Code, ein Commit.**

`phase9_hardening/` angelegt (`CLAUDE.md`, `SESSIONS_ARCHIVE.md`, `tests/`). `scripts/` bleibt
vorerst leer und damit ungetrackt (git committet keine leeren Verzeichnisse) — beide neuen
Skripte gehören plangemäß (§2.1/§2.3) ins repo-weite `scripts/`, nicht hierher; ein
phasenlokales `scripts/` entsteht erst, sobald ein späterer P9-Step eins braucht, genau wie bei
`phase8_6_ui_polish/scripts/`.

**INDEX-Rotation gebaut (P9-L):** `scripts/rotate_index_updates.sh`, dieselbe Mechanik wie
`rotate_session_block.sh` (Ausschneiden per `sed`, Reassemblierung mit `cmp` geprüft, jeder
Block byte-identisch gegengelesen, erst danach geschrieben) — aber auf eine **einzelne
physische Zeile** angewandt: die `updated:`-Frontmatter-Zeile von `docs/INDEX.md` wird an
` | `-Trennern **gefolgt von einem ISO-Datum** (`\d{4}-\d{2}-\d{2}`) gesplittet, nicht an jedem
` | ` — sonst hätte ein ` | ` innerhalb eines Eintrags den Schnitt verfälscht. Vier Gegenproben
vor dem Schreiben: (a) Byte-Buchhaltung (rotierte Einträge + Rest-Zeile + Trenner == Original),
(b) `cmp` der Reassemblierung, (c) jeder rotierte Eintrag byte-identisch im Archiv
wiedergefunden, (d) der Frontmatter-Closer `---` steht danach auf eigener Zeile. Getestet gegen
eine `tmp_path`-Fixture mit synthetischer Mehr-Eintrags-Kette (`test_rotate_index_updates.py`),
nicht gegen die echte `docs/INDEX.md` — die Kette dort trägt aktuell nur einen Eintrag (vom
2026-09-19 von Hand rotiert), das Skript liefe dort auf den „nichts zu tun"-Pfad.

**Vier geplante Defekte repariert (§2.2) plus drei ungeplante, vom `doc_health.py`-Bau selbst
aufgedeckt (nicht im Plan, aber trivial und im selben Commit behoben statt liegengelassen) —
sieben insgesamt:**

*Geplant, §2.2:*
- **0-a** die fünf `up:`/`down:`-Links in `phase8_6_ui_polish_block_h_r_3_escalation.md`
  korrigiert (drei waren `docs/concepts`-Geschwister und brauchten `./`, zwei zeigten auf
  `phase8_6_ui_polish/` und brauchten `../../`)
- **0-b** beide Mini-Pläne (`phase8_6_ui_polish_block_g_r_plan.md`,
  `phase8_6_ui_polish_block_h_r_plan.md`) haben jetzt eine L1-Card (`status: snapshot`)
- **0-c** `docs/INDEX.md`s `ROADMAP.md`-Zeile nennt jetzt die reale Größe (42.080 B) und P9;
  `ROADMAP.md` bleibt über dem Softcap, benannt statt versteckt (P8-P) — Straffung ist
  Step-Z-Arbeit
- **0-d** `docs/screenshots_latest/` entfernt — Gegenprobe zeigte alle sechs Symlinks dort
  bereits tot (`../p86_block_g_r_*.png` löst nicht auf, Original liegt unter
  `docs/screenshots/`); `screenshots_latest/` am Repo-Root ist die von Konvention §5 und
  `docs/INDEX.md:143` gemeinte Instanz und bleibt

*Ungeplant:*
- Wurzel-`CLAUDE.md` stand bei **64.401 B**, deutlich über dem 40-KB-Softcap —
  `docs/INDEX.md`s eigene Zeile dafür behauptete noch „~22 KB" aus der Frontmatter-Rotation vom
  2026-09-13; seither haben drei P9-Planungscommits (`06ab4f6`, `633338d`, `2f752f9`) den
  `## Current state`-Body weiter wachsen lassen (die Rotation von 2026-09-13 betraf nur die
  `updated:`-Kette, nicht den Body — P9-A hat eine Ein-Block-Regel für den Body ausdrücklich
  verworfen). Nikinger-Entscheidung: **benennen, nicht kürzen** — dieselbe P8-P-Konvention wie
  `phase8_6_ui_polish/CLAUDE.md` und `phase6_shares/CLAUDE.md`. Die Zeile trägt jetzt die reale
  Größe und die Benennung statt der stalen Zahl. **Der größte Einzelbefund dieser Session** —
  eine Datei war eine Woche lang um das Dreifache größer, als ihre eigene Index-Zeile behauptete,
  unbemerkt bis `doc_health.py` sie fing.
- `docs/PROJECT_SESSION_LOG.md` begann mit einer führenden Leerzeile vor der Frontmatter
  (`\n---\n...`) statt direkt mit `---` — einzige Datei im Repo mit diesem Defekt, `header_cards`
  hätte ihn sonst als Befund gemeldet. Entfernt.
- `docs/INDEX.md`s Zeile für `docs/screenshots/` verlinkte auf das Verzeichnis
  (`./screenshots/`) statt auf dessen `README.md`, obwohl der Text „L1-Header-Card in
  `docs/screenshots/README.md`" bereits sagte, wo die Card liegt — der Direktlink fehlte. Auf
  `./screenshots/README.md` umgestellt, analog zum bereits bestehenden Muster bei
  `screenshots_latest/`, dessen INDEX-Zeile direkt auf sein `README.md` zeigt. **Das ist eine
  Konventions-Entscheidung, keine reine Linkkorrektur:** jedes künftige `<dir>/README.md` in
  diesem Repo braucht ab jetzt entweder denselben Direktlink-auf-README-Zeigers oder eine
  eigene INDEX-Zeile — `doc_health.py`s `index_lines`-Prüfung erzwingt das ab sofort. Wer das
  zurück auf einen Verzeichnislink „korrigiert", bricht den Scan.

**`doc_health.py` gebaut** (`scripts/doc_health.py`, stdout nur JSON, Logging nach stderr —
Hard Rule 7) mit den vier Prüfungen aus §2.3 (`index_lines`, `header_cards`, `updown_links`,
`oversize`). Die Ausnahmeliste ist eine Konstante mit den vier in `docs/INDEX.md` benannten
Fällen. **`oversize` unterscheidet drei Zustände statt zwei:** 📕/📦-Snapshots sind immer
ausgenommen; 📗/🟡-Dateien über 40 KB sind nur dann kein Befund, wenn ihre `docs/INDEX.md`-Zeile
die Zeichenkette „benannt statt versteckt" **und** eine aktuelle Größenangabe trägt — exakte
Byte-Zahl **oder** gerundete `~NNKB` innerhalb von **±2 KB** der echten Dateigröße, keine
Prozent-Toleranz (eine Prozent-Toleranz hätte bei einer 106-KB-Datei ±32 KB durchgelassen; der
gefundene Defekt war „~22 KB" für eine 64-KB-Datei — eine feste, kleine Bandbreite fängt genau
das, ohne mit der Dateigröße mitzuwachsen). `index_lines` sucht ebenfalls pfad-, nicht
namensbasiert — `CLAUDE.md` allein kommt in einem Dutzend INDEX-Zeilen vor, ein bloßer
Namens-Treffer hätte jede neue `phaseN/CLAUDE.md` für immer kostenlos bestehen lassen. Genau
dieses Muster trägt `phase8_6_ui_polish/CLAUDE.md`, `phase6_shares/CLAUDE.md` und jetzt
`ROADMAP.md` und Wurzel-`CLAUDE.md`. Ein 📗/🟡-Fund ohne Benennung bleibt ein echter Befund.
`phase9_hardening/tests/test_doc_health.py` nagelt alle vier Prüfungen fest, `oversize` inkl.
Gegenprobe für einen benannten, einen unbenannten und einen stale-benannten Fall.
`pytest.ini`s `testpaths` fehlte `phase9_hardening/tests` — ohne die Zeile wären diese 13 Tests
für jeden `pytest -q`-Lauf unsichtbar geblieben, und P9-9 („pytest ≥ 995, Step 0 addiert die
neuen doc_health-Tests") wäre unerfüllbar gewesen. Zeile ergänzt — **das ist eine geteilte
Config-Datei, keine Doku-Zeile**, deshalb hier ausdrücklich benannt statt beiläufig
mitgeführt. Nebenbefund dabei: `phase8_ui_graph/`, `phase8_5_picker_release/` und
`phase8_6_ui_polish/` haben gar kein eigenes `tests/`-Verzeichnis (ihre Tests leben in
`phase5_ui/tests` bzw. `phase4_auth/tests`) — Phase 9 ist die erste Phase mit einem eigenen
`tests/`-Ordner seit `phase7_spaces_admin/`.

**Baseline gemessen, zweistufig:** vor jeder Änderung `.venv/bin/python -m pytest -q` →
**995 passed in 185,98 s** (V147, exakt die geforderte Zahl). Nach Step 0 komplett (13 neue
Tests + die `pytest.ini`-Ergänzung, die sie erst sichtbar macht) → **1008 passed in 182,78 s**
— 995 + 13, rechnerisch geprüft, nicht nur behauptet. Phasenstart-SHA: `06ab4f6` (Stand vor
diesem Commit). Kein `ui_budget`-Touch nötig (kein `phase5_ui/webui/static/**` berührt), kein
`node --check` nötig (kein JS berührt). Tabu-Diff §0.3 leer — reine Doku-/Skript-Session. Kein
`pkill -f`, kein `systemctl`, sharefyx-mcp nicht berührt.

**Nächster Schritt:** Step A (Domain über eigenen VPS) als Coarbeit in opencode (P9-Q) —
Voraussetzung ist die Domain-/VPS-Beschaffung durch den Nikinger, siehe Prompt-Vorlauf. B und C
laufen unabhängig davon weiter, A blockiert die Phase nicht.

