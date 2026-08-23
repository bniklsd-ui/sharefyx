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
updated: 2026-08-23 (Abnahmematrix eroeffnet, P6.5-1/2/4 live bestanden -- 3 von 14 Zeilen, neunte Rotation gelaufen)
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
| Block A (Steps A1/A2/A4; A3 bewusst nicht gebaut, N3) | Werkzeug-Ergonomie (`mcpserver/tools.py`, `storage/store.py :: search(in_body=)`) | ✅ **gebaut, live deployt 2026-08-21, Gate A→B bestanden 2026-08-21** — echte Connector-Probe über claude.ai/Claude-Code-Connector, siehe Session-Block |
| Block B Step B1 | Storage-Fundament Bilder (`storage/{files,store,models}.py`) | ✅ **gebaut, live deployt 2026-08-21** |
| Block B Step B2 | REST-Fläche Bilder (`phase5_ui/webui/{api,serializers}.py`) | ✅ **gebaut, live deployt 2026-08-21** |
| Block B Step B3 | Web-UI Anzeigen/Einfügen (`phase5_ui/webui/static/{app.html,app.css,js/{markdown,editor}.js}`) | ✅ **gebaut, live deployt 2026-08-21**, Playwright vor dem Deploy grün+gesehen |
| Block B Step B4 | MCP-Fläche Bilder (`mcpserver/tools.py` — `get_item_asset`/`put_item_asset`) | ✅ **gebaut, live deployt 2026-08-21**, `mcp_smoke.py` 16/16 |
| Block B Step B5 | Betrieb/Deploy-Vorbereitung (`diagnose.sh` Prüfung 13, `UPDATE_LOG.md`, `ui_budget.py`) | ✅ **gebaut, Block B vollständig, live deployt 2026-08-21** |

## Geerbte Contracts

Fünfte, benannte Öffnung des P1-Contracts (`storage/{files,store,models}.py`) — **gebaut**
2026-08-20 (Step B1), siehe `phase1_storage/CLAUDE.md` unter „Geerbte Contracts" (P6.5-T).
Details dort, nicht hier dupliziert.

## Abnahmestand (Plan §6, P6.5-1–P6.5-14)

**Statusregel wie in P5/P6: ✅ heißt live-verifiziert durch den Nikinger, nicht „gebaut".** Der
Plan selbst (`docs/concepts/phase6_5_tools_images_plan.md`) ist ein 📕-Snapshot und wird nicht
mehr editiert — der laufende Abnahmestand lebt hier, wie bei jeder Vorgängerphase.

| # | Kriterium (Kurzform) | Block | Stand | Beleg |
|---|---|---|---|---|
| P6.5-1 | Frische Instanz sagt NICHT „nur eigener Space" | A | ✅ | Nikinger, echter Connector, 2026-08-23 — Instanz nannte `niklas` UND `IT-Sekus-Projekt` (`write: true`) korrekt, `fabian` korrekt read-only |
| P6.5-2 | Nennt erlaubte `status`-Werte ohne Fehlversuch | A | ✅ | Nikinger, echter Connector, 2026-08-23 — `note: active\|archived`, `task: archived\|done\|open`, exakter Treffer im ersten Versuch |
| P6.5-3 | Nutzt `get_item_meta` vor einem Folge-Append | A | offen | noch nicht beobachtet — die 2026-08-23-Sitzung enthielt keinen Append-Fall |
| P6.5-4 | Erklärt `patch_item`/`update_item`/`append_to_item`-Aufgabenteilung aus den Beschreibungen | A | ✅ | Nikinger, echter Connector, 2026-08-23 — korrekt: nur `update_item` erreicht Frontmatter, `patch_item`/`append_to_item` brauchen `version`, `patch_item` verlangt exakt einen Treffer |
| P6.5-5 | Bild-Upload sichtbar im UI-Dokument | B | offen | Browser |
| P6.5-6 | `.md`-Datei enthält nur `asset:`-Referenz, kein Binär/base64 | B | offen | `cat` im `DATA_ROOT` |
| P6.5-7 | Bilddatei unter `_assets/<item_id>/`, kein UI-Ordner | B | offen | `ls` + Browser |
| P6.5-8 | Fabian sieht freigegebenes Bild, `403` ohne Freigabe | B | offen | Nikinger + Fabian, Browser + `curl` |
| P6.5-9 | Ein Upload = genau ein Git-Commit | B | offen | `git log --oneline` |
| P6.5-10 | Cross-Space-Move nimmt Bild mit, ein Commit | B | offen | Browser + `git log` |
| P6.5-11 | Fremde `<img>`-URLs/`javascript:` kein Netzabruf, kein `<img>` | B | offen | DevTools Network-Tab |
| P6.5-12 | Bild entfernbar, Referenz rendert danach als Alt-Text | B | offen | Browser — entfällt bei N5=„gar nicht" |
| P6.5-13 | Claude sieht fremdes Bild nur bei `share_write`, nicht bei reinem `share_read` | B | offen | Nikinger + Fabian, echter Connector |
| P6.5-14 | Kündigt jeden Upload an, lädt nie unaufgefordert | B | offen | Nikinger, echter Connector, zwei Gespräche |

**3 von 14 live bestanden** (Block A: 3 von 4, Block B: 0 von 10). Geerbte, in dieser Phase
nicht gelöste Live-Proben aus P6 (Abnahmezeilen 25–30/35–39, Gate A→B Punkt 3, `diagnose.sh`
vor jedem Deploy): unverändert offen, siehe Plan §6 Fußnote.

---

## Session stopped — 2026-08-23 (Abnahmematrix eröffnet: P6.5-1/2/4 live bestanden)

**Korrektur zur Vorsitzung:** deren Schlusssatz „Phase 6.5 hat keine offenen Bau- oder
Verifikationsschritte mehr" war zu stark — Gate A→B (Code/Connector-Rundlauf funktioniert) und
die vollständige Abnahmematrix (Plan §6, P6.5-1–14, „✅ heißt live-verifiziert durch den
Nikinger") sind zwei verschiedene Dinge. Diese Session baut die bis dahin fehlende
Abnahmematrix-Sektion in diesem Head nach (existierte vorher gar nicht — anders als bei P5/P6)
und trägt die ersten drei Zeilen ein.

**Auftrag:** Nikinger fragte, ob eine spontane, nicht-abgesprochene Nutzungssitzung (Ordner +
Datei über den Connector anlegen, NVIDIA-Notizen) bereits Testwert für die Abnahmematrix hat.
Antwort: nur zufällig, nicht gezielt — P6.5-1–4 verlangen laut Plan **gepunktete Fragen** an eine
Instanz, kein Nebenprodukt einer anderen Aufgabe (Details siehe Antwort im Chat). Auf Vorschlag
drei konkrete Fragen im selben Gespräch gestellt, echte Antworten erhalten und geprüft.

**Geprüft, Wortlaut gegen den Plan-Wortlaut abgeglichen, keine Interpretation nötig:**
- **P6.5-1 ✅** — Instanz nannte `niklas` (eigen) UND `IT-Sekus-Projekt` (geteilt, `write: true`)
  als beschreibbar, `fabian` korrekt als reinen Lesezugriff. Sagte an keiner Stelle „nur eigener
  Space" — genau der Fehler, den P6.5-B beheben sollte.
- **P6.5-2 ✅** — `note: active|archived`, `task: archived|done|open`, exakter Treffer, kein
  Fehlversuch. Deckt sich byte-genau mit `storage.models.STATUS_VALUES`.
- **P6.5-4 ✅** — Aufgabenteilung korrekt aus der Beschreibung abgeleitet: nur `update_item`
  erreicht Frontmatter, `patch_item`/`append_to_item` brauchen `version` (Optimistic Locking),
  `patch_item` verlangt exakt einen Treffer sonst kompletter Fehlschlag ohne Teil-Schreiben.
- **P6.5-3 — weiterhin offen.** Diese Sitzung enthielt keinen Lesen-vor-Folge-Append-Fall, kann
  also weder bestätigen noch widerlegen, ob eine Instanz von sich aus `get_item_meta` statt
  `get_item` für die Versionsnummer wählt.

**Neu gebaut, nicht nur editiert:** die Sektion „Abnahmestand" existierte in diesem Head bisher
nicht (anders als `phase5_ui/CLAUDE.md`/`phase6_shares/CLAUDE.md`, die beide eine laufend
gepflegte Matrix führen). Jetzt angelegt, alle 14 Zeilen aus Plan §6 übernommen, drei auf ✅,
Rest „offen" mit Beleg-Spalte (wer/wie prüft). Statusregel identisch zu P5/P6: ✅ = live-
verifiziert, nicht „Code existiert".

**Verifiziert:** kein Code-Diff (reine Doku-Session). `git status` zeigt ausschließlich den
Phase-Head + `SESSIONS_ARCHIVE.md` + `docs/INDEX.md`.

**Offen für die nächste Session:**
- 11 von 14 Abnahmezeilen offen — P6.5-3 (weitere Connector-Frage), P6.5-5–12 (Browser/
  `DATA_ROOT`, Block B), P6.5-13/14 (Connector + Fabian, zwei Gespräche).
- V64, `filename`-Persistenzfrage, Doku-Schuld, `test_authctl.py`-Flake: unverändert offen.
