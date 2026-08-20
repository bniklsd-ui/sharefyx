---
status: live
purpose: Phase-Head Werkzeug-Ergonomie + Bilder — Scope, harte Regeln, Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase6_5_tools_images/ oder an den in §2 des Plans genannten Dateien in mcpserver/storage/webui — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase6_5_tools_images_plan.md   # voller Plan, Entscheidungen P6.5-A–P6.5-V, §0.0 gelockte N1–N6, Steps 0/A/B
  - ../phase6_shares/IMAGES_PLAN.md                  # Vorgänger-Zusatzplan, nachrangig seit 2026-08-20
  - SESSIONS_ARCHIVE.md                              # ältere Session-Blöcke, newest-first
updated: 2026-08-20 (Block B Step B5 gebaut: diagnose.sh Pruefung 13, UPDATE_LOG.md, ui_budget.py Lauf -- Block B vollstaendig, 828 pytest unveraendert, sechste Rotation gelaufen)
---
# CLAUDE.md — Phase 6.5: Werkzeug-Ergonomie und Bilder (`phase6_5_tools_images/`)

> Kein eigenes Python-Paket (wie `phase3_edge/`, `phase6_shares/`) — Servercode bleibt in
> `mcpserver`/`storage`/`webui`. **Quelle der Wahrheit ist der Code, nicht dieses Dokument.**

---

## Mission (zuerst lesen)

Zwei Blöcke: **(A)** eine arbeitende Claude-Instanz findet ihre Werkzeuge, versteht deren
Aufgabenteilung aus der Beschreibung und zahlt keine Tausende Token für eine Versionsnummer.
**(B)** ein Bild liegt im Space, ist im Dokument sichtbar, technisch nur ein Link — und Claude
sieht seine Bytes nur, wenn ein Mensch ausdrücklich danach fragt. Unter Druck fällt Block B weg,
nie Block A (reine Beschreibungs-/Tool-Arbeit ohne Datenformatänderung).

## Scope

- **DRIN:** die fünf offenen MCP-Werkzeug-Ergonomie-Punkte (2026-08-14-Live-Feedback),
  Abschluss Block C Bilder (`storage/`-Fundament, `webui`-Routen, MCP-Asset-Tools).
- **DRAUSSEN:** Bulk-Append-Tool, Body-Volltextsuche in der Web-UI, automatische
  `_trash/`-Räumung, Space-Admin-UI (bleibt Phase 7), Rechteverwaltung über MCP-Tools,
  HEIC/SVG/PDF, serverseitiges Bild-Rendering. Volle Liste: Plan §5 „Explizit draußen".

Details, gelockte Entscheidungen P6.5-A–P6.5-V, Berührungsfläche/Tabu-Dateien, Schritt-Sequenz,
Testliste, Abnahmezeilen: `docs/concepts/phase6_5_tools_images_plan.md`.

## Modul-Status

| Block | Inhalt | Status |
|---|---|---|
| Step 0 | Haushalt/Ankündigungen | ✅ |
| Block A (Steps A1/A2/A4; A3 bewusst nicht gebaut, N3) | Werkzeug-Ergonomie (`mcpserver/tools.py`, `storage/store.py :: search(in_body=)`) | ✅ **gebaut**, noch nicht deployt — Gate A→B (echte Connector-Probe) steht aus |
| Block B Step B1 | Storage-Fundament Bilder (`storage/{files,store,models}.py`) | ✅ **gebaut** |
| Block B Step B2 | REST-Fläche Bilder (`phase5_ui/webui/{api,serializers}.py`) | ✅ **gebaut**, noch nicht deployt |
| Block B Step B3 | Web-UI Anzeigen/Einfügen (`phase5_ui/webui/static/{app.html,app.css,js/{markdown,editor}.js}`) | ✅ **gebaut**, Playwright grün+gesehen, noch nicht deployt |
| Block B Step B4 | MCP-Fläche Bilder (`mcpserver/tools.py` — `get_item_asset`/`put_item_asset`) | ✅ **gebaut**, `mcp_smoke.py` 16/16, noch nicht deployt |
| Block B Step B5 | Betrieb/Deploy-Vorbereitung (`diagnose.sh` Prüfung 13, `UPDATE_LOG.md`, `ui_budget.py`) | ✅ **gebaut, Block B vollständig** |

## Geerbte Contracts

Fünfte, benannte Öffnung des P1-Contracts (`storage/{files,store,models}.py`) — **gebaut**
2026-08-20 (Step B1), siehe `phase1_storage/CLAUDE.md` unter „Geerbte Contracts" (P6.5-T).
Details dort, nicht hier dupliziert.

---

## Session stopped — 2026-08-20 (Block B Step B5 gebaut: Betrieb/Deploy-Vorbereitung — Block B vollständig)

**Auftrag:** direkter Anschluss an Step B4, letzter Schritt von Block B. Plan §3 Step B5:
`diagnose.sh` Prüfung 13 (Größenmessung), `docs/UPDATE_LOG.md`-Eintrag, `ui_budget.py`-Lauf.
Reines Betriebs-/Ops-Skript-Zeug, keine Python-Kernlogik — bewusst kein Advisor-Call nötig,
Nikinger-Vorgabe für diese Session: nur noch EIN Advisor-Call insgesamt, für den Abschluss.

**Gebaut, exakt wie im Plan §3 Step B5 vorgezeichnet:**
- `phase3_edge/scripts/diagnose.sh` — **Prüfung 13** (neu, INFO, kein Abbruchkriterium, dieselbe
  Kategorie wie 9/11/12): Gesamtgröße aller `_assets/`-Verzeichnisse über alle Spaces (`find
  -mindepth 2 -maxdepth 2 -type d -name '_assets'`, passend zu `files.py :: asset_dir()`s
  echtem Pfad `<data_root>/<space>/_assets`) + Größe von `$DATA_ROOT/.git`. Begründung direkt im
  Skript: B1 = ja (Bilder werden mitcommittet, Git-Historie wächst monoton, ein entferntes Bild
  gibt keine Bytes frei) und B2 = 5 MiB je Bild ohne Space-Gesamtbudget heißt „messen statt
  deckeln" — diese Prüfung ist das Messgerät. Nutzt dieselbe `$data_root`-Auflösung wie Prüfung
  12 (kein zweiter `local.env`-Read). `numfmt --to=iec` für menschenlesbare Ausgabe, Fallback
  auf rohe Byte-Zahl, falls `numfmt` fehlt.
- `docs/UPDATE_LOG.md` — neuer Eintrag oben, heutiges Datum (P6-X-Gate in `deploy.sh` verlangt
  das), zwei Zeilen: Bilder in Notizen (Upload/Ansehen/Einfügen im Editor), Claude beschreibt
  seine Werkzeuge klarer.
- `phase5_ui/scripts/ui_budget.py` einmal real gelaufen (temporäres `DATA_ROOT`, kein Live-
  Zugriff): alle 5 Messgrößen weiterhin im Zielkorridor — `app.js + app.css + Font (gzip)`
  jetzt **79.5 KB** (Ziel < 250 KB), trotz `markdown.js` (+Bildzweig/`safeSrc`) und `editor.js`
  (+Upload-Handler/`insertAtCursor`) deutlich unter dem Korridor. Erstaufruf-Gesamtgröße 84.1 KB
  (Ziel < 400 KB).

**Kein Code-Fund, keine Abweichung.** Reines Betriebsartefakt-Kapitel, bewusst ohne Advisor-
Runde (Nikinger-Vorgabe dieser Session: ein einziger Advisor-Call, für die Abschlussprüfung
unten) — die diagnose.sh-Logik selbst wurde stattdessen gegen ein echtes temporäres
Test-`DATA_ROOT` (zwei `_assets/`-Verzeichnisse verschiedener Größe + ein `.git`-Verzeichnis,
nie das reale) durchgerechnet: 12345+5000 Bytes Assets korrekt zu 17345 summiert, 2000 Bytes
`.git` korrekt gemeldet — Arithmetik verifiziert, nicht nur `bash -n` (Syntaxprüfung) vertraut.

**Tests:** keine neuen (Bash-Skript + Markdown-Doku, kein Python — dieselbe Kategorie wie P5-T
für JS: `diagnose.sh` hat repo-weit keine Unit-Tests, nur `bash -n` + reale Läufe als Beweis,
kein einziger Test in `phase3_edge/tests/`/`phase5_ui/tests/` referenziert das Skript). `pytest`
**828 unverändert**. Tabu-Diff nicht relevant (kein `storage/`/`mcpserver/`/`webui`-Python-Diff
in diesem Step — nur `phase3_edge/scripts/diagnose.sh` + `docs/UPDATE_LOG.md`, beide laut Plan
§2 ausdrücklich erlaubt).

**Verifiziert:** `bash -n diagnose.sh` sauber, Prüfung-13-Arithmetik gegen ein echtes
Temp-`DATA_ROOT` nachgerechnet (Ergebnis oben), `ui_budget.py` real gelaufen (5/5 im
Zielkorridor, Rohausgabe gesehen), `pytest` 828/828 unverändert, `git status` zeigt nur die
beiden erwarteten Dateien. **Advisor-Nachprobe vor dem Commit:** Prüfung 13 gegen dieselbe
Temp-Harness erneut gefahren, diesmal mit `set -euo pipefail` (wie im echten Skript) UND einem
per `chmod 000` unlesbaren Space-Unterverzeichnis — `find ... 2>/dev/null` überspringt ihn
lautlos, die `while <(process substitution)`-Schleife bricht `pipefail` nicht, das Skript
endet weiterhin mit `exit 0`. Kein Fund, nur bestätigt.

**Block B (Bilder) ist damit vollständig: Steps B1–B5 alle gebaut, noch nicht deployt.**

**Offen für die nächste Session:**
- Commit + Push (Nikinger-Freigabe ausstehend zum Zeitpunkt des Schreibens).
- **Vor jedem Deploy:** `diagnose.sh` frisch fahren (geerbte Auflage seit dem
  Funnel-Reboot-Fund, `phase3_edge/CLAUDE.md`) — jetzt inklusive der neuen Prüfung 13.
- **`docs/UPDATE_LOG.md`s neuer oberster Eintrag trägt `2026-08-20`.** `deploy.sh`s P6-X-Gate
  verlangt an JEDEM Deploy-Tag ein heutiges Top-Datum — findet der Deploy nicht heute statt,
  muss das Datum vor dem `deploy.sh`-Lauf einmal nachgezogen werden (oder
  `SHAREFYX_ALLOW_STALE_UPDATELOG=1` bewusst gesetzt werden), sonst bricht ein ansonsten
  sauberer Deploy grundlos am Gate ab.
- **`ROADMAP.md` Zeile 15 (`Step 0 gestartet`) bewusst stehen gelassen, nicht nachgezogen** —
  Hard Rule 8 nennt nur Phase-Head + `docs/INDEX.md`, `ROADMAP.md` wird laut Präzedenz (P5)
  erst beim Phasenabschluss aktualisiert, nicht bei jedem Step. Explizit vermerkt, damit das
  eine bewusste Entscheidung bleibt und keine unbemerkte Drift.
- Gate A→B (echte Connector-Probe für Block A) steht weiterhin aus, unverändert — **das ist
  jetzt der einzige verbleibende Blocker vor einem Deploy von Block A UND B**, keine offenen
  Bau-Schritte mehr in dieser Phase außer der Deploy-Vorbereitung selbst.
- V64 (löst `destructiveHint: True` bei claude.ai tatsächlich eine Rückfrage aus?) bleibt offen,
  braucht dieselbe echte Connector-Probe wie Gate A→B — beide können in einem Aufwasch geprüft
  werden, sobald der Nikinger den Connector gegen diesen Stand testet.
- `filename`-Persistenzfrage (dreimal berührt: B1/B2/B4, nie entschieden) bleibt offen.
- Bekannte Doku-Schuld (`phase6_shares/CLAUDE.md` Block-C-Text stale) und der
  `test_authctl.py`-Flake bleiben unverändert offen.
