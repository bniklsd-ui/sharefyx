---
status: live
purpose: Archivierte Session-stopped-Blöcke aus phase8_5_picker_release/CLAUDE.md, verbatim, newest-first
read-when: Auditieren der vollen Phase-8.5-Historie — der aktuelle Session-Block lebt im Phase-Head, nicht hier
detail: L3
up: ./CLAUDE.md
down:
updated: 2026-09-04 (Step-0-Block rotiert — manuell, weil Skript nur 2+→1 kann und Archiv initial keinen `## Session stopped`-Anker hatte; Platzhalter entfernt, Block unten angehängt; Block-A/A2/B1/C/D/Z stehen noch aus)
---

# SESSIONS_ARCHIVE.md — Phase 8.5: Link-Picker-Politur, Titel-statt-ID-Hint, v3-Vorabritt + Deploy

### 2026-09-03 (Step 0 — Skelett + vier Haushalt-Funde abgearbeitet)

**Auftrag:** Step 0 nach `docs/concepts/phase8_5_picker_release_plan.md` §1. Verifikations-
Durchlauf war bereits 2026-09-03 vom Nikinger (Planungssession) gefahren — vier Funde
benannt, davon drei Doku-only, einer ein Bilanz-Zähler-Drift. opencode/M3 wiederholt die
Messung nicht, sondern arbeitet die Funde ab und legt das Skelett an.

**Ergebnis — alle vier Funde aus Plan §1 abgearbeitet, alle fünf Schritte grün:**

1. **Fund 1 — `docs/INDEX.md` über 40 KB-Softcap** (Plan §1.2). Zeile 8 war eine
   15.472-Zeichen-Pipe-Kette aus ~40 datierten Einträgen, verantwortlich für den Löwenanteil
   der Datei (52.911 B bei Übernahme). **Kürzung auf 5 neueste Einträge + Schlusszeile**
   „ältere Einträge: die jeweilige phase*/SESSIONS_ARCHIVE.md". Die vollständige Historie
   steht in den jeweiligen `phase*/SESSIONS_ARCHIVE.md`. Größenverlauf: **52.911 B → 40.917 B**
   (−11.994 B, −23 %; aktueller Stand nach Step 0.2: **40.917 B, 43 B unter dem 40-KB-Softcap
   = 40 × 1024 B**).
2. **Fund 2 — vier `.md` ohne Card/Indexzeile, korrekt so** (Plan §1.3). Regel-Präzisierung
   im Wartungsblock von `docs/INDEX.md` (Zeilen 21–23): Harness-Dateien
   (`.claude/RESUME.md`), Test-Fixtures (`phase6_shares/tests/golden/*.md` — Card bräche den
   Byte-Vergleich), maschinell geparste Dateien (`docs/UPDATE_LOG.md`), Vendor-/Lizenztext
   (`phase5_ui/THIRD_PARTY_LICENSES.md`, `phase5_ui/vendor/lucide/README.md`). Bewusst als
   kompakter Dreizeiler formuliert (Plan §1.3 liefert nur die vier Kategorien; ausführliche
   Begründung pro Datei bleibt im Plan §1.3-Tabelle).
3. **Fund 3 — Doku/Code-Drift „Büroklammer" vs. „Lupe"** (Plan §1.4).
   `phase8_ui_graph/CLAUDE.md:440` nannte das Picker-Symbol „Büroklammer", `app.html:183`
   rendert `<use href="#i-search">` (Lucide-Suche, eingeführt in Phase 8 Block C2). Der
   `UPDATE_LOG.md`-Eintrag vom 2026-09-01 sagte bereits korrekt „Lupe". **Korrektur mit
   datierter Notiz** am 2026-09-03 im selben Block, damit der nächste Leser sieht, dass es
   kein Tippfehler war, sondern eine echte Korrektur.
4. **Fund 4 — Phase-8-Abnahmebilanz zum dritten Mal gedriftet** (Plan §1.5). Die Zeile trug
   seit dem 2026-09-02-Block „15 ✅ · 10 🟡 · 0 ⬜", die Aufzählung darunter listete unter
   „15 ✅" genau **vierzehn** Zeilennummern. Maschinell nachgezählt über die §7-Matrix
   selbst:
   ```
   awk '/^\| P8-[0-9]+ /{ if (/\| ✅ \|/) g++; else if (/\| 🟡 \|/) y++; else if (/\| ⬜ \|/) o++; n++ } \
     END {printf "Zeilen=%d ✅=%d 🟡=%d ⬜=%d\n", n, g, y, o}' phase8_ui_graph/CLAUDE.md
   ```
   Lauf 2026-09-03: **`Zeilen=26 ✅=14 🟡=12 ⬜=0`**. Bilanz-Zeile auf **14 ✅ · 12 🟡 · 0 ⬜**
   korrigiert; das awk-Kommando in den Bilanz-Abschnitt geschrieben, sodass künftige
   Schreibvorgänge die Zahl ableiten statt pflegen. Aufzählung gegen das Ergebnis abgeglichen
   (passt: 14/12-Zerlegung stimmt mit den aufgezählten IDs überein).

**Skelett angelegt (Step 0.5):**

- `phase8_5_picker_release/CLAUDE.md` — L1-Card, Mission, Scope (DRIN/DRAUSSEN), Harte Regeln
  (§0.3 Tabu-Liste verbatim übernommen + explizit `webui/{api,serializers,permissions}.py` als
  Tabu ergänzt), Modul-Status-Tabelle (Step 0 / A1 / A2 / B1 / C / D / Z mit aktuellem
  Status), Abnahmestand-Tabelle nach §7-Muster (P8.5-1–P8.5-20, P8.5-1/-2/-20 aus Step 0
  bereits ✅), Geerbte Contracts, leerer Session-Block. **12.128 B** — deutlich unter dem
  40-KB-Softcap.
- `phase8_5_picker_release/SESSIONS_ARCHIVE.md` — L1-Card, leerer Body mit Hinweis, dass der
  erste rotierte Block hierher wandert, sobald die zweite Session den Step-0-Block ablöst.
  **555 B**.
- `phase8_5_picker_release/scripts/` — leeres Verzeichnis, wird in Block C gefüllt
  (Wegwerf-Setup + Playwright-Ritt).

**Begleitende Doku-Updates im selben Commit (Hard Rule 8):**

- `ROADMAP.md` — neuer Abschnitt „Phase 8.5 — Link-Picker-Politur und v3-Release" eingefügt
  **vor** „Bewusst nicht auf der Roadmap" (Plan §1.6 Zeile 352). Status: „Step 0
  abgeschlossen", nächster Schritt „A1".
- `CLAUDE.md` (Wurzel) — `down:`-Zeile zeigt jetzt auf `phase8_5_picker_release/CLAUDE.md`
  (vorher `phase8_ui_graph/CLAUDE.md` — Umstellung nach Skelett-Anlage, wie der 2026-09-03-
  Absatz in „Current state" angekündigt hatte). Neuer Absatz unter Phase 8.5 mit Step-0-
  Zusammenfassung; `updated:`-Kette um den Step-0-Eintrag am Anfang verlängert. **41.462 B** —
  damit 502 B **über** dem 40-KB-Softcap. Das war bereits vor Step 0 absehbar (Kandidat für
  dieselbe Kompression wie 2026-08-08, INDEX.md-Zeile 27); kein Step-0-Auftrag, kein
  Step-0-Aufräumschritt — Vermerk in `docs/INDEX.md` bleibt korrekt.
- `docs/INDEX.md` — `## Phase 8.5 — 🔄 …`-Abschnitt mit drei INDEX-Zeilen war bereits durch
  den Nikinger angelegt (Planungs-Commit 2026-09-03); Step 0 hat daran nichts geändert.
  Dateigröße 40.917 B — 43 B unter dem Cap, **nicht** 264 B wie nach Fund 1 alleine, weil
  Fund 2 die Ausnahmenliste hinzugefügt hat.

**Verifiziert (§0.5 Checkliste):**

- `pytest -q` (venv): **959 passed in 270.79 s** — unverändert, kein Python-Touch in
  dieser Session (nur `.md` und Skelett-`.md`).
- Tabu-Diff aus §0.3 leer:
  `git diff --stat main -- phase4_auth/ phase1_storage/storage/ phase5_ui/webui/security.py
  phase5_ui/webui/api.py phase5_ui/webui/serializers.py phase5_ui/webui/permissions.py
  phase2_mcp/` — **keine Ausgabe**.
- `node --check` auf JS-Dateien: keine berührt.
- `python phase5_ui/scripts/ui_budget.py`: keine UI-Änderung, irrelevant für Step 0.
- Service-Touch **0**. `systemctl status sharefyx-mcp` zeigt **PID 195922**, Active seit
  `Wed 2026-09-02 11:51:57 CEST` (1 day 21h zum Sitzungsbeginn), CPU 18min 33s — nichts
  angefasst, nur gelesen. **PID + ActiveEnterTimestamp im Session-Block notiert, wie §0.5.7
  verlangt.**
- Größenprüfung `find . -name "*.md" -not -path "./.venv/*" -not -path "*/.pytest_cache/*"
  -size +40k` (Plan §6 Step Z Punkt 6 — vorab geprüft, weil Step 0 schon Doku-Maße ändert):
  jeder Treffer ist entweder 📕 (Plan-Snapshot, `docs/concepts/*_plan.md`) oder bereits
  vorher als „über 40KB-Softcap benannt" markiert (`phase8_ui_graph/CLAUDE.md` 93.562 B,
  `phase6_shares/CLAUDE.md` 41.032 B, `CLAUDE.md` 41.462 B seit diesem Schritt). **Neu durch
  Step 0** ist der Eintrag für `CLAUDE.md` — siehe oben.

**Eine Korrektur am Plan, im Session-Block festgehalten, kein stille Abweichung:**

Fund 1 + Fund 2 zusammen landeten **zunächst 75 B über dem Cap**. Der Plan nennt
„neuesten fünf" explizit, hatte aber die zusätzlichen Bytes der Fund-2-Ausnahmenliste nicht
mitgerechnet (seine Schätzung „mit ihr ~52,7 KB" war ein Vorher-Wert, kein Nachher-Wert).
**Lösung:** Fund 2 als Drei- statt Vierzeiler formuliert, Datei landete auf 40.917 B
(43 B unter dem Cap). Beide Anforderungen — fünf Einträge **und** Ausnahmen dokumentiert —
gehalten, Plan-Wortlaut im Session-Block nicht gebrochen. Wer den Plan liest und `updated:`
als Pipe-getrennte Liste erwartet, sieht sie weiterhin (Schlusszeile ist erkennbar, weil
„ältere Einträge: …" mit Doppelpunkt beginnt).

**Nächster Schritt, konkret:** Block A / **A1 — §9.4.2 Picker-Modus-Umschalter**.
`docs/concepts/phase8_5_picker_release_plan.md` §2.A1 enthält die genauen Eingriffe
(`app.html` Zeile 270–280 mit `<select class="input" id="link-picker-mode">`, `dialogs.js`
Zeile 100–185, `editor.js` Zeile 88–100 + 548–557, `localStorage`-Persistenz unter
`sfx:linkpicker:mode`). Tabu-Diff-Kommando am Step-Ende weiter leer halten — A1 berührt
nur `webui/static/{app.html,app.css,js/dialogs.js,js/editor.js}`.
