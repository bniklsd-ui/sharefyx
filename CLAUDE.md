---
status: live
purpose: Regeln, Konventionen, Arbeitsweise und aktueller Stand des Space-Servers — wird jede Session automatisch geladen
read-when: immer, vor jeder Aktion in diesem Repository
detail: L2
up: docs/INDEX.md
down:
  - ROADMAP.md                          # Phasenplan + Status je Phase
  - docs/INDEX.md                       # L0-Karte aller .md
  - phase7_spaces_admin/CLAUDE.md       # aktive Phase
updated: 2026-09-01 (Phase 8 Gate B→C bestanden -- Current-state-Absatz erweitert, Phase-8-Head rotiert, Block C als nächster Schritt markiert; kein Code, kein Service-Touch in dieser Sitzung) | 2026-09-01 (Hard Rule 9 ergänzt — kein pkill -f mit Regex, niemals den systemd-Dienst anfassen; Lehre aus dem Prod-Vorfall 2026-09-01, Phase 8 Step A3 Nachbereitung) | 2026-08-23 (Phase 7 Step 0: down: auf phase7_spaces_admin/CLAUDE.md umgestellt, stale d348e2e-Deploy-Behauptung im Current-state-Absatz korrigiert) | 2026-08-09 (Phase 6 🔄 gestartet — Hard Rule 4 neu gefasst (P6-U), Current state umgestellt)
---
# CLAUDE.md — Project Instructions

> Read this file before doing anything in this repository.
> It is the single source of truth for project rules, conventions, and current state.

---

## What this project is

Ein **geteilter Kontext-Space-Server** für zwei Personen (Nikinger + Kollege) und deren
Claude-Instanzen. Notizen und Aufgaben liegen als Markdown-Dateien mit YAML-Frontmatter auf
einer Heim-VM; Claude greift über einen **Remote-MCP-Server** (Custom Connector, Streamable
HTTP) lesend und schreibend darauf zu, Menschen über eine Web-UI oder direkt im Editor.

Der Server läuft hinter **CGNAT** (RUT X50, Mobilfunk) — die Verbindung kommt von Anthropics
Backend, nicht vom Client. Erreichbarkeit daher **ausschließlich über einen ausgehenden
Tunnel**, niemals über Port-Forwarding.

Build order: `ROADMAP.md` · Doku-Karte: `docs/INDEX.md`

---

## Core principle (read carefully)

**Bauprinzip: Der Server ist dumm.**

Die gesamte Intelligenz sitzt beim Client (Claude). Der Server ist ein Aktenschrank mit
Schloss — mehr nicht.

**Der Server macht:**
- Dateien lesen/schreiben (atomar), Frontmatter parsen/serialisieren
- Index pflegen, Suchen beantworten, Paginierung
- Auth (Token → Space), Autorisierung (eigener Space schreibbar, fremde read-only)
- Versionierung, Konflikterkennung, Git-Commits
- Fehlerbehandlung, Logging, Health

**Der Server macht NIEMALS:**
- LLM-Calls, Embeddings, semantische Suche, Zusammenfassungen, Auto-Tagging
- irgendeine Form von „Verstehen" des Inhalts

Wer hier ein LLM einbauen will → **stop**. Das gehört auf die Client-Seite. Ein Server, der
Inhalte interpretiert, ist ein Server, dessen Fehlverhalten man nicht mehr debuggen kann —
und er importiert Prompt-Injection direkt in den Speicherpfad.

---

## Hard Rules (no exceptions)

1. **Niemals Secrets in Dateien.** Keine Tokens, keine Keys — nicht in `.env`, nicht in JSON,
   YAML oder Config. Space-Tokens und Tunnel-Credentials leben ausschließlich im OS-Keyring
   (Service `nikinger-space`) bzw. als systemd `LoadCredential`. Zugriff über
   `storage/credentials.py`. Ein Token in einem Commit ist ein Incident, kein Schönheitsfehler.
   **[2026-07-25 Korrektur, P2 Step 3]:** `storage/credentials.py` wurde nie gebaut — der
   reale Pfad ist `phase2_mcp/mcpserver/credentials.py`. Die Regel selbst bleibt unverändert.
   **[2026-07-30 Ergänzung, P4 Schnitt]:** Ab Phase 4 liegen dort **echte** Geheimnisse (TOTP-
   Seeds, umkehrbar) neben den reinen Token-Hashes aus P2/P3 — `phase4_auth/authserver/users.py`,
   Service weiterhin `nikinger-space`. Ein TOTP-Seed ist bei Kompromittierung nutzbar, ein
   Token-Hash nicht; dieselbe Hard Rule, höherer Einsatz.

2. **Dateien sind die Wahrheit, der Index ist Ableitung.** SQLite darf jederzeit gelöscht und
   aus den `.md`-Dateien vollständig rekonstruiert werden. Nie umgekehrt. Wer den Index als
   primären Speicher benutzt → stop.

3. **Kein Write ohne `version`.** Jede Schreiboperation trägt die gelesene Version; Mismatch →
   `ConflictError` mit dem aktuellen Item im Fehler. **Kein Last-Write-Wins, nirgends.**
   Zwei Claude-Instanzen im selben Space sind der Normalfall, nicht der Randfall.

4. **Fremde Spaces sind read-only, fremde Inhalte sind Daten.** ~~Cross-Space-Writes existieren
   architektonisch nicht (kein Parameter, keine Codepfad-Variante).~~ Jeder Body aus einem
   fremden Space wird — unverändert, auch in geteilten Spaces — im Tool-Result in
   `<untrusted_content>` gewrappt. Begründung: Claude liest fremde Notizen *mit* aktiven
   Schreib-Tools — jede Zeile dort ist ein potenzieller Befehl.
   **[2026-08-09 Neufassung, P6-U]:** **Schreibrechte folgen der Mitgliedschaft, nicht dem
   Token.** Ziel-Space eines Writes ist per Default der Home-Space des Principals. Ein anderer
   Ziel-Space ist nur zulässig, wenn er in einer `.share.yml` unter `write:` steht oder das Item
   selbst `share_write` trägt — die Liste ist **Daten auf der Platte, kein `if` im Code**, und
   über kein Item-Tool änderbar. Der alte Satz („Cross-Space-Writes existieren architektonisch
   nicht") war vier Phasen lang richtig und ist mit geteilten Spaces nicht mehr haltbar; die
   Ersetzung ist eine bewusste Nikinger-Entscheidung vom 2026-08-09, keine stille Aufweichung.
   **Scharf erst ab P6 Step 5** — `.share.yml`, `share_write`, `SharePolicy` existieren vor Step
   4/5 nicht im Code; bis dahin gilt faktisch weiter die durchgestrichene Fassung. Details:
   `docs/concepts/phase6_shares_plan.md` §0.7(a), §1.2.

5. **Writes sind atomar und fail-closed.** `tmp` + `os.replace` + `fsync` auf dem Verzeichnis.
   Nie ein halb geschriebenes Item auf der Platte. Jeder erfolgreiche Write erzeugt einen
   Git-Commit im Datenverzeichnis (Undo + Historie kostenlos).

6. **Nie ein offener Port am Router.** Erreichbarkeit ausschließlich über ausgehenden Tunnel.
   Wer Port-Forwarding oder DynDNS vorschlägt → stop, das scheitert an CGNAT und öffnet die
   Heim-VM.

7. **Logging → stderr; stdout nur maschinenlesbares JSON.** Atomic commits. Kein Subtask
   „done" ohne grünes `pytest` (gemockt, **kein Netz, kein echter Tunnel** in Unit-Tests).

8. **Commit ⇒ Doc-Update (zwingend, auch auf direkte Anweisung).** Jeder Step-Abschluss-Commit
   aktualisiert im **selben** Commit die Modul-/Status-Tabelle der Phase **und** den
   `## Session stopped`-Block. Neue `.md` ⇒ Zeile in `docs/INDEX.md` im selben Commit.

9. **Niemals per Regex-Substring Prozesse killen, niemals den systemd-Dienst anfassen.**
   `pkill -f <muster>` matcht mit Extended Regex — ein einzelner `.` matcht `/`, ein Modulname
   im eigenen und im Production-Args reicht, um die falsche PID zu treffen. Konkret
   (2026-09-01, Phase 8 Step A3 Nachbereitung): `pkill -f "phase2_mcp.scripts.serve"` killte
   sowohl die Wegwerf-Instanz als auch die Produktion (`sharefyx-mcp.service`, PID 38101,
   SIGTERM, Journal bestätigt). Stopp-Reihenfolge: **eigene** Wegwerf-Instanzen sind erlaubt
   zu stoppen, aber ausschließlich über PID-Datei, `pgrep -f` mit Anker (`$`) oder über den
   eindeutigen Port — nie über Regex im Cmdline. Den **einen** systemd-verwalteten
   `sharefyx-mcp.service` startet/stoppt/restartet **ausschließlich der Nikinger**
   (`sudo systemctl ...` läuft nicht aus dem `savefyx`-User, und auch wenn es liefe:
   Handlungsgrenze). Vor jedem `kill`/`pkill`/`systemctl` zuerst fragen: *ist das die echte
   Instanz, oder meine Wegwerf-Instanz, oder gar nicht meine?* Im Zweifel: fragen, nicht
   schießen.

---

## Working style

- **Quelle der Wahrheit ist der Code, nicht dieses Dokument.** Bei Widerspruch gewinnt das
  getestete Artefakt; das Dokument wird sofort mit datierter Korrekturnotiz gefixt.
- **`[VERIFY]`-Marker:** Alles, was gegen den echten Repo-Stand oder eine externe API geprüft
  werden muss, ist so markiert. Bei Ausführung verifizieren, **nie** als gesichert übernehmen.
- **Gelockte Entscheidungen bleiben gelockt.** Widersprechende Evidenz wird ein expliziter
  Befund für den Menschen, nie eine stille Abweichung.
- **Act vs. ask:** reversible, in-scope Schritte selbst ausführen; bei destruktiven Aktionen,
  Scope-Änderungen und Out-of-Scope-Edits stoppen und fragen.
- **Handover für einen kalten Leser schreiben.** Ergebnis zuerst, kein Session-Slang, nächster
  Schritt konkret genug zum Sofortstart.

## Doku-Hygiene (Doc-Layers)

Vollspec: `docs/DOC_LAYERS_CONVENTION.md` (v1, 2026-07-06) — **byte-identische Kopie aus dem
Trading-Bot-Repo**, dort bewusst projekt-agnostisch geschrieben. Sie wird hier **nicht**
projektspezifisch angepasst: zwei Kopien derselben Regel, die sich unterschiedlich entwickeln,
sind schlimmer als eine, die an einer Stelle etwas allgemein formuliert ist. Wer sie ändern
will, ändert sie im Trading-Bot-Repo und kopiert erneut.

Kurzform: **L0** = `docs/INDEX.md` · **L1** = ≤15-Zeilen-Header-Card oben in jedem *lebenden*
Dokument · **L2** = schlanke Bodies, Softcap **≤40 KB** · **L3** = Archive und datierte
Snapshots. Rotationsregel ab Tag 1 scharf: ein Phase-Head trägt **genau einen** aktuellen
`## Session stopped`-Block; der vorherige wandert **verbatim** nach `SESSIONS_ARCHIVE.md`.
Durchführung über `scripts/rotate_session_block.sh <phase_verzeichnis>`, nie von Hand.

> Diese Regel gilt hier ab dem ersten Commit, nicht als späterer Rettungseinsatz. Im
> Trading-Bot-Repo wuchs `phase8_scheduler/CLAUDE.md` auf 211 KB, bevor sie eingeführt wurde.

---

## Current state

**[2026-09-01] Phase 8 — 🔄 Block A + B ✅ live-verifiziert, Gate B→C bestanden.** UI-Neuanstrich v3,
Verknüpfungs-Graph (`GET /api/v1/graph` + `item_links`-Tabelle + `linkscan.py` + UI-Wiring), drei
P7-Erbposten (P7-24 Reauth-Grant ✅, `remove-space`-Auto-Reindex ✅, P7-4 Zweitprobe 🟡 mit
benanntem Restdefekt Klammer/Aufzählung). Plan: `docs/concepts/phase8_ui_graph_plan.md` (N1–N12
gelockt, P8-A–P8-Q, Abnahme P8-1–P8-24, `[VERIFY]` V81–V92). Kernentscheidungen: P7-24-Fix als
**Reauth-Grant** (vierte Option, in der Planung gefunden — kein Aufweichen des Anti-Replay),
**achte P1-Contract-Öffnung benannt** (Link-Extraktion beim Indexieren für den Graphen), Design
v3 (IBM Plex, Lucide-Sprite, Farblegende own/shared/foreign, Glass-Akzente mit Fallback).
**Ausführung erstmals opencode/M3, ohne Advisor-Stufe (N12)** — Ersatz: Plan §0.6 +
zwei Nikinger-Sichtprüfpunkte. Closeout wird §9 des Plans (ein Dokument pro Phase, P8-N).
**Gate B→C (2026-09-01)** alle vier Bedingungen grün: 958/958 pytest, Charakterisierung
byte-identisch, Tabu-Diff leer, `_graph_get` manuell gegen 3 Spaces + 12 ACL-Fälle 12/12,
Playwright-Smoke gegen Wegwerf-Instanz 18/18 (Picker + `#item/`-Navigation).
**Nächster Schritt:** Block C (Design-Fundament v3, Plan §4) — C0 Anti-AI-Research →
C1 Plex → C2 Lucide → C3 Farbsemantik → C4 Glass → C5 Dichte.

**[2026-08-28] Phase 8 geplant — ⬜ nicht gestartet.** UI-Neuanstrich v3, Verknüpfungs-Graph,
drei P7-Erbposten. Plan: `docs/concepts/phase8_ui_graph_plan.md` (N1–N12 gelockt, P8-A–P8-Q,
Abnahme P8-1–P8-24, `[VERIFY]` V81–V92). Kernentscheidungen: P7-24-Fix als **Reauth-Grant**
(vierte Option, in der Planung gefunden — kein Aufweichen des Anti-Replay), **achte
P1-Contract-Öffnung benannt** (Link-Extraktion beim Indexieren für den Graphen), Design v3
(IBM Plex, Lucide-Sprite, Farblegende own/shared/foreign, Glass-Akzente mit Fallback).
**Ausführung erstmals opencode/M3, ohne Advisor-Stufe (N12)** — Ersatz: Plan §0.6 +
zwei Nikinger-Sichtprüfpunkte. Closeout wird §9 des Plans (ein Dokument pro Phase, P8-N).

**[2026-08-28] Phase 7 abgeschlossen — ✅ live-verifiziert.** Space-Verwaltung in der
Weboberfläche, Mehrfachauswahl, Konsolidierung (`phase7_spaces_admin/`, kein eigenes Python-Paket)
sind gebaut, live deployt (`main`@`e88a624`, 2026-08-27) und abgenommen. **Abnahmestand: 22 von 24
Zeilen ✅, 2 ❌, 0 ungeprüft** — die Matrix ist vollständig durchgelaufen; das unterscheidet diese
Phase von P6/P6.5, wo Zeilen ungeprüft blieben. **Der Sprung auf ✅ ist eine Nikinger-Entscheidung
vom 2026-08-28** unter der Bedingung, dass die beiden ❌ als benannte Defekte an Phase 8 vererbt
werden: **P7-24** (`list.js :: moveSelectedItems()` reicht denselben TOTP-Code an jedes
sequenzielle PATCH einer Batch-Runde — der Server lehnt den Replay korrekt ab, ein Batch mit N
rechteerweiternden Items braucht real N Codes statt einem; echter Mechanismus-Defekt, Fix
bewusst in P8) und **P7-4** (Claude nennt Menschen gegenüber IDs statt Titeln, trotz der Anweisung
in vier Tool-Beschreibungen — kein Code-Fehler). **Dritter Erbposten aus dem Live-Betrieb:
`spacectl.py remove-space` reindiziert den SQLite-Index nicht** — der Incident vom 2026-08-27
(`GET /api/v1/overview` → 500 für jeden eingeloggten Nutzer) kam genau daher; der Zustand ist
per `space_cli.py reindex` behoben, die Ursache nicht. Sechste und siebte P1-Contract-Öffnung mit
dieser Phase geschlossen, keine achte angekündigt. **Einstiegsdokument für die Phase-8-Planung:
`docs/concepts/PHASE7_CLOSEOUT_HANDOVER.md`** (dort §4 die offenen Entscheidungen, §7 die
geänderte Arbeitsweise: Claude Code plant, opencode/M3 führt aus). Übersichtsgrafik:
`docs/concepts/phase7_spaces_admin_uebersicht.svg`. **Die folgenden Absätze bleiben als
Verlaufsdokumentation stehen.**

**[2026-08-23] Phase 7 aktiv — Space-Verwaltung, Mehrfachauswahl, Konsolidierung**
(`phase7_spaces_admin/`, kein eigenes Python-Paket) — **🔄, Block A weit fortgeschritten.** Step 0
(Haushalt + Doku-Audit) ✅, danach A1/A2 (Item-ID sichtbar+auffindbar)/A3 (Bild-Entfernen-Knopf,
schließt P6.5-12)/A4 (Feld-Whitelist, schließt O6) gebaut, A5 (Sichtbarkeits-Migration) live
`--apply` gefahren, A7/A7b (dritter Principal `testnutzer-p7` + `testcred.py`) live angelegt,
**A8 (formaler Abschluss Phase 6.5) durchgeführt** — siehe unten. Verbleibend in Block A: A6
(Purge-Gate, kalendarisch frühestens 2026-08-28). Plan: `docs/concepts/
phase7_spaces_admin_plan.md` (Entscheidungen P7-A–P7-W, alle zehn Nikinger-Fragen N1–N10 gelockt
in §0.1). Phase-Head: `phase7_spaces_admin/CLAUDE.md`.

**[2026-08-27 Korrektur]** Der Absatz oben blieb seit dem Phasenstart stehen und ist überholt.
**Phase 7 ist inhaltlich vollständig** — Block A (inkl. A8, Phase 6.5 formal abgeschlossen),
Gate A→C, Block C (C1–C5, Space-Verwaltung in der Weboberfläche) und Block B (Mehrfachauswahl,
`ITEM_MOVE_PLAN.md` §9) sind alle gebaut. **Live deployt, 2026-08-27, Nikinger-Lauf:**
`/opt/sharefyx/current` → `e88a6244d8eebb5d08d1d93c4a2725f84a2f5971`, Health-Gate 3/3 grün
(`/ui/login`→200, `/api/v1/me`→401, `/mcp/`→401 — alle drei die erwarteten Antworten, kein
Fehlschlag). **[2026-08-28 Korrektur]** Abnahmezeilen 31–34 (`ITEM_MOVE_PLAN.md` §9.5) sind seither
vom Nikinger selbst live gegen die echte Instanz bestätigt — 32/33/34 ohne Vorbehalt, 31 mit dem
bereits bekannten P7-24-TOTP-Vorbehalt (kein neuer Fund, Fix in der nächsten Phase). **A6
(Purge-Gate/P7-9) ebenfalls gefahren** — `token_families` 35→31, `clients` unverändert 54 wie
erwartet (90-Tage-Fenster erst 2026-10-27). **Kein offener Test/Gate mehr.** Verbleibend: Step Z
Rest (Phase-7-Closeout-Dokumente, Übersichtsgrafik, Rotationsprüfung). **Noch nicht ✅** — „✅
heißt live-verifiziert, nicht gebaut", der formale Sprung folgt erst mit dem Closeout. Details:
`phase7_spaces_admin/CLAUDE.md`, aktueller Session-Block.

**[2026-08-23, P7 Step A8] Phase 6.5 formal abgeschlossen als 🟡 — code-complete und live
deployt, aber NICHT vollständig live-verifiziert.** Bewusst **nicht** ✅: **12 von 14
Abnahmezeilen** live, davon zwei (P6.5-8/13) über eine im P7-Plan §A8.1 gebilligte Substitution
— `testnutzer-p7` statt Fabian, derselbe serverseitige Rechte-Code-Pfad. Verbleibend offen:
P6.5-12 (Entfernen-Knopf jetzt von P7 Step A3 gebaut, kein Browser-Klick-Nachweis) und P6.5-14
(Nikingers eigene Bewertung, kein Selbstzertifizierungs-Kriterium — bleibt strukturell offen).
Handover: `docs/concepts/PHASE6_5_CLOSEOUT_HANDOVER.md`. Übersichtsgrafik:
`docs/concepts/phase6_5_tools_images_uebersicht.svg`. **Der untenstehende Absatz vom
Phasenstart (2026-08-20) bleibt als Verlaufsdokumentation stehen, ist inzwischen überholt.**

**[2026-08-20] Zweite aktive Phase gestartet: Phase 6.5 — Werkzeug-Ergonomie und Bilder**
(`phase6_5_tools_images/`, kein eigenes Python-Paket) — **🔄 Step 0.** Sitzt bewusst zwischen der
noch laufenden Phase 6 und der reservierten Phase 7 (Space-Admin-UI, `app.html` unverändert).
Deckt die fünf noch offenen MCP-Werkzeug-Ergonomie-Punkte (siehe „Noch nicht entschieden" unten —
**jetzt geplant, nicht mehr offen**) und den Abschluss von Block C Bilder ab (löst
`phase6_shares/IMAGES_PLAN.md` als maßgebliche Quelle ab). Plan: `docs/concepts/
phase6_5_tools_images_plan.md` (Entscheidungen P6.5-A–P6.5-V, alle sechs Nikinger-Fragen N1–N6
gelockt in §0.0). Phase-Head: `phase6_5_tools_images/CLAUDE.md`.

**[2026-08-23] Phase 6 abgeschlossen als 🟡 — code-complete und live deployt, aber NICHT
vollständig live-verifiziert.** Bewusst **nicht** ✅: nur **12 von 39 Abnahmezeilen** sind
live-verifiziert, vier (31–34, §9 Mehrfachauswahl) wurden nie gebaut, Block C ist nach Phase 6.5
ausgewandert, sieben Zeilen hängen an einer Sitzung mit Fabians eigenem Login. Es gibt bewusst
**kein** `P6_ABNAHME_<datum>.md` — der Zeilenstatus steht in
`docs/concepts/PHASE6_CLOSEOUT_HANDOVER.md` §3. **Der Sprung auf ✅ ist eine offene
Nikinger-Entscheidung.** Zwei Aufgaben sind vom Nikinger ausdrücklich für die nächste Phase
benannt: (1) **Doku-Audit** der Modul-Status-Zeilen 8–16 in `phase6_shares/CLAUDE.md`, die noch
„gebaut, noch nicht deployt" tragen — vermutlich stale, wie sich am 2026-08-23 schon für die
globale Suche zeigte, aber **zu prüfen, nicht zu raten**; (2) **kein Entfernen-Knopf für Bilder**
in `phase5_ui/webui/static/js/editor.js`, obwohl N5 gelockt ist und der `DELETE`-Endpunkt
existiert (blockiert P6.5-12). Übersichtsgrafik: `docs/concepts/phase6_shares_uebersicht.svg`.
**Phase 6.5 ist davon unberührt und läuft weiter.** Der folgende Absatz bleibt als
Verlaufsdokumentation stehen.

**Phase 6 — Freigaben, Ordner, Werkzeug-Ergonomie** (`phase6_shares/`, kein
eigenes Python-Paket) — **🔄 gestartet, 2026-08-09.** Ausführungsreifer Plan lag bereits vor
(`docs/concepts/phase6_shares_plan.md`, Entscheidungen P6-A–P6-AC, Steps 0–10, drei Blöcke: A =
Werkzeuge/Betrieb/Update-Banner, B = Dateisystem, C = Bilder, hartes Gate zwischen A und B).
Herkunft/offene Entscheidungen: `docs/concepts/PHASE5_CLOSEOUT_HANDOVER.md` §4.1–§4.6. Phase-Head:
`phase6_shares/CLAUDE.md`. Step 0 ✅, Step 1 ✅ (`patch_item`, Quittungen statt Volltext), Step 2
✅ **gebaut** (O2 geschlossen, `ua`-Feld, **V42 geschlossen 2026-08-12** — `ua` unterscheidet
nicht zwischen Claude-Oberflächen, `diagnose.sh`/`ui_budget.py`-Ergänzungen), Step 3 ✅
**gebaut, Live-Teile beim Nikinger** (Update-Log und
Banner — Schema 3, `webui/updates.py`, `deploy.sh`-Gate). **Block A (Steps 0–3) damit
vollständig gebaut.** **GATE A→B: 3 von 4 Punkten live bestanden** (patch_item, Banner + Fabians
Bestätigung) — nur noch Punkt 3 offen (Purge-Zeilenrückgang, frühestens 2026-08-28), per
Nikinger-Entscheidung vor Gate-Abschluss mitgetragen, nicht blockierend für Block B. Block B:
Step 4 (Storage-Fundament — `storage/acl.py`, `folder`/`visibility`/`share_*`) ✅ **gebaut**,
Step 5 (Rechtepolitik — `SharePolicy`/`Surface` ersetzt `OwnSpaceWritable`, item-level ACL in
`mcpserver/tools.py`/`webui/api.py`) ✅ **gebaut** (2026-08-12), Step 6 (Verwaltung/Migration —
`spacectl.py`, `migrate_visibility.py`, `diagnose.sh` Prüfung 12) ✅ **gebaut** (2026-08-12).
**[2026-08-13] Steps 4–6 live deployed** (`main`@`d068d1c`, Nikinger-Entscheidung „power right
through the deployment", Sudo-Neustart durch ihn) — Cutover auf die neue `SharePolicy` vollzogen,
vorher `niklas`↔`fabian` gegenseitiges Lesen per `.share.yml` gesichert (sonst hätte der Cutover
genau das stillschweigend entzogen). Live-Verifikation **eine Richtung bestätigt** (niklas liest
fabian über den echten Connector, `<untrusted_content>`-Wrapping hält), **fabian→niklas offen**.
Neuer Shared Space `IT-Sekus-Projekt` angelegt (beide Principals `--write`, für Nutzung/Testing).
**Ein UI-Fund, zwei Teile:** `IT-Sekus-Projekt` zeigte sich in der Weboberfläche als „nur lesen"
trotz `writable:true`. Teil 1 (Space-Liste liefert kein `writable`-Feld) ist **deployed und live
bestätigt weg** — Badge korrekt. Teil 2, vom Nikinger direkt danach gemeldet: **innerhalb** des
Spaces stand weiterhin „nur lesen", der Anlegen-Knopf blieb versteckt — eine zweite, unabhängige
Stelle in `app.js` (`ownSpaceActive()`, acht Aufrufstellen) fragte weiterhin „eigener Space?"
statt „schreibbar?". Behoben (`activeSpaceWritable()` ersetzt alle acht Stellen). **[2026-08-13
Nachtrag] deployed und live bestätigt** — Release `20260813T120925.743482Z` (`main`@`92b918b`),
vom Nikinger per manuellem UI-Test im Browser validiert. **Damit sind beide Teile des UI-Funds
geschlossen.** Details: `phase6_shares/CLAUDE.md`s Session-Block vom selben Tag.

**[2026-08-18] Deploy-Blocker, Nikinger-Entscheidung, noch offen:** ein sophistizierter E2E-Lauf
gegen eine Wegwerf-Instanz fand einen echten UI-Fund — es gibt keinen „über alle lesbaren Items
hinweg suchen"-Modus, ein Item mit ausschließlich item-level `share_write`/`share_read` (kein
space-level Grant) ist über die Web-UI unauffindbar, nur über den MCP-Connector erreichbar. Vom
Nikinger als echter Bug eingestuft, **muss vor dem nächsten Deploy geplant und behoben werden**.
**[2026-08-19 Nachtrag] Geplant UND gebaut, noch nicht deployt/committet:**
`phase6_shares/GLOBAL_SEARCH_PLAN.md` (Entscheidungen **P6-AO–P6-AT**, Abnahmezeilen 35–39).
Kernbefund der Planung, im Code verifiziert: `GET /api/v1/items` **ohne** `space`-Parameter ist
bereits die globale, item-weise ACL-gefilterte Suche (`webui/api.py :: _items_get` →
`can_read_item_as_human`) — es fehlt ausschließlich die UI-Fläche, kein neuer Endpunkt. **Q1
(Suchreichweite) vom Nikinger entschieden:** nur Titel/Tags, keine Body-Volltextsuche in diesem
Schnitt — offene, dokumentierte Lücke, kein stilles Schließen. Steps G1–G2 gebaut
(`serializers.py`/`api.py`/`state.js`/`tree.js`/`list.js`/`app.css`), 7 neue Tests, `pytest`
765→772 grün, Tabu-Diff leer. Zusätzlich Playwright-verifiziert gegen eine Wegwerf-Instanz
(10/10 grün, Pflichtfall aus Zeile 28 nachgestellt) — ein Advisor-Fund dabei entdeckt und noch
vor dem Commit behoben: `editor.js :: clearDetail()` (Home-Button) setzte `state.scope` nicht
zurück, ließ den Anlegen-Knopf nach „Alle Items" → Home fälschlich ausgehängt. **[2026-08-19,
committet]** `main`@`d348e2e`. **[2026-08-23 Korrektur, P7 Step-0-Audit]** live deployt seit
`main`@`f96125e` (`git merge-base --is-ancestor d348e2e f96125e`) — diese Zeile hatte die
Korrektur, die `phase6_shares/CLAUDE.md` bereits am 2026-08-23 bekam, selbst nie erhalten.
Details: `phase6_shares/CLAUDE.md`s aktuellem Session-Block.

**[2026-08-19, MUSS-VOR-DEM-NÄCHSTEN-DEPLOY] Funnel überlebte den Reboot nicht sauber:** nach
dem Reboot dieser Session war Sharefyx von einem echten Gerät ohne VPN/Tailscale aus
unerreichbar (`NS_ERROR_CONNECTION_REFUSED`), obwohl Dienst, lokales `/health` und `tailscale
funnel status` alle gesund aussahen — `sudo systemctl restart tailscaled` behob es sofort.
`diagnose.sh` Prüfung 5 hätte das bisher **nicht** zuverlässig erkannt (MagicDNS verdeckte den
echten öffentlichen Pfad) und ist jetzt entsprechend korrigiert. Selbstheilung/Watchdog für den
Funnel-Backhaul ist eine bewusst offene Entscheidung, kein Auftrag. Volle Herleitung:
`phase3_edge/CLAUDE.md`, Abschnitt „[2026-08-19 MUSS-VOR-DEM-NÄCHSTEN-DEPLOY]".

**[2026-08-19] Block C (Bilder) ist geplant:** `phase6_shares/IMAGES_PLAN.md` (Entscheidungen
**P6-AU–P6-BB**, Abnahmezeilen 40–47) — **fünf offene Nikinger-Entscheidungen B1–B5** (Binärblobs
in der Git-Historie des `DATA_ROOT` vs. Hard Rule 5, Größenriegel, Bildbytes fremder Items vor
einem sehenden Modell als Injektionskanal, den `<untrusted_content>` strukturell nicht erreicht,
MCP-Upload, Löschen eines Bildes vs. Entscheidung H/„kein Delete im Kern-API"). Vor dem Bau
einzuholen, nicht von Claude zu entscheiden.

**Phase 5 — Web-UI, REST-API und Auth-Selbstverwaltung** (`phase5_ui/`, Paket `webui`) — **✅
abgeschlossen, 2026-08-09 — 20/20 Abnahmezeilen live bestanden, 0 teilweise, 0 offen.** Zwei
Blöcke (A = Sicherheit + Auth-Selbstverwaltung, B = REST-API + UI) mit hartem Gate dazwischen,
beide durchlaufen. Menschen setzen ihr Passwort jetzt selbst im Browser, ohne SSH und ohne
Neustart (schließt Betriebsnotiz O1 auch live). Cutover auf `/opt/sharefyx/current` seit
2026-08-05, `deploy.sh`-Zyklus läuft. `git diff` auf `storage/`,
`mcpserver/{tools,permissions,server}.py` blieb über die gesamte Phase leer (Kriterium 18) —
derselbe Seam-Beweis wie in Phase 4, eine API-Fläche höher.

Vollständige Matrix, Modul-Status je Step und die gesamte Live-Debugging-Historie (u. a. der
Origin/CSRF-Fund am Block-A-Gate, die Step-7b-Revision von Plan §4.1/§4.3, Sicherheitsbefund S9)
stehen in `phase5_ui/CLAUDE.md` — read + newest Session-stopped-Block first, das ist die
maßgebliche Quelle für diese Phase, nicht diese Zeile hier. Ältere Session-Blöcke:
`phase5_ui/SESSIONS_ARCHIVE.md`.

Plan: `docs/concepts/phase5_ui_plan.md` (Entscheidungen P5-A–P5-AE, Steps 0–9). Herkunft/offene
Entscheidungen: `docs/concepts/PHASE4_CLOSEOUT_HANDOVER.md`. Abnahmeprotokoll:
`docs/concepts/P5_ABNAHME_2026-08-09.md`. Formaler Abschluss-Handover an P6:
`docs/concepts/PHASE5_CLOSEOUT_HANDOVER.md`.

**Phase-6-Vormerkungen — [2026-08-09 erledigt] alle vier Punkte sind jetzt Scope von Phase 6**
(`docs/concepts/phase6_shares_plan.md`: F1 → P6-J/K/Q/T, F2 → §0.6 weiterhin bewusst draußen,
Client-Surface-Logging → P6-A5/Step 2, `patch_item` → P6-E/F/G/Step 1). Absatz bleibt stehen als
Herkunftsnachweis, nicht mehr als offene Sammlung:
- **F1** — Subspaces/eigene Ordner + „shared Spaces" (Nikinger-Meldung, Step 8b): F1a
  (Default-Leserechte auf eigene Connectoren verengen) ist ein kleiner eigener Schnitt; F1b (ein
  Space, in dem alle unabhängig volle Rechte haben) kollidiert frontal mit Hard Rule 4, kein
  Ad-hoc.
- **F2** — vollständiges Löschen bleibt draußen (Plan §0.5 nennt es explizit), nur Archivieren.
- **Client-Surface-Logging** (2026-08-07) — welche Claude-Oberfläche (claude.ai/Desktop vs.
  Claude Code) einen Request stellte, ins Request-Log, nicht in die UI. Kein Blocker —
  Nikinger-Entscheidung 2026-08-07: Claude Code darf den produktiven Connector wie jede andere
  Oberfläche nutzen, das ist architektonisch identisch (Token → Space, nicht Token → Client).
- **`patch_item`** (2026-08-08, Live-Feedback einer arbeitenden Claude-Instanz über den echten
  Connector) — `update_item` ersetzt immer den kompletten Body; eine Drei-Zeilen-Korrektur an
  einem großen Dokument erzwingt einen Komplett-Rewrite, teuer und riskant, weil dabei mehr
  verloren gehen kann als bei einem gezielten Patch. Vorschlag aus der Rückmeldung:
  `patch_item(item_id, version, old_text, new_text)`, schlägt hart fehl, wenn `old_text` nicht
  genau einmal vorkommt (kein stilles Teil-Überschreiben). Betrifft `mcpserver/tools.py`
  (P5-B tabu für diese Phase), also kein Ad-hoc-Fix — Kandidat für denselben späteren Zuschnitt
  wie F1/F2.

**Phase 4 — OAuth 2.1 + DCR** (`phase4_auth/`, Paket `authserver`) — **✅ abgeschlossen,
2026-07-30 — 16/16 Abnahmezeilen live bestanden, Schnitt vollzogen.** Der Pfad-Token ist
verschwunden; ein eigener, im selben Prozess laufender Authorization Server (Discovery, Dynamic
Client Registration, PKCE, Argon2id + TOTP, opake rotierende Token) authentifiziert seither jeden
Connector. Kritischer Fund in Step 0: ein nie widerrufener Keyring-Token für einen seit P2
umbenannten dritten Space (`nikinger`) — live und schreibfähig, aber ohne zugehöriges
Verzeichnis; noch vor dem Schnitt widerrufen und live gegen `diagnose.sh`/
`export_space_map.py` bestätigt (Details: `docs/concepts/PHASE3_CLOSEOUT_HANDOVER.md` §5).

Sicherheitsbefunde **S1–S10 / O1–O2** (S1–S8 und S10 geschlossen; O1 strukturell durch P5
geschlossen; **O2 offen** — `clients`/`token_families` werden nie abgeräumt) stehen mit vollem
Verlauf und Fundstellen in `phase4_auth/CLAUDE.md`, ebenso der Modul-Status aller acht Steps und
das ausgeführte Inbetriebnahme-Runbook.

Plan: `docs/concepts/phase4_auth_plan.md` (Entscheidungen P4-A–P4-R, Steps 0–7 — geschrieben ohne
frischen Repo-Zugriff, siehe Plan-Kopf). Herkunft/offene Entscheidungen:
`docs/concepts/PHASE3_CLOSEOUT_HANDOVER.md`. Abnahmeprotokoll:
`docs/concepts/P4_ABNAHME_2026-07-29.md`. Sicherheits-Review vor der Abnahme:
`docs/concepts/P4_SECURITY_REVIEW_2026-07-29.md`. Formaler Abschluss-Handover an P5:
`docs/concepts/PHASE4_CLOSEOUT_HANDOVER.md`.

**Phase 3 — Exposure & Betrieb** (`phase3_edge/`, kein eigenes Python-Paket — Servercode bleibt
in `mcpserver`): ✅ **live-verifiziert, 13/13** — Ursprungsstand 10/13
(`docs/concepts/P3_ABNAHME_2026-07-27.md`). Zeile 6 (Reboot) löste sich am 2026-07-29 durch
einen unbeabsichtigten Reboot der VM (Windows-Host-Neustart des Nikingers), Zeile 12
(Backup-Timer-Lauf) durch einen realen Timer-Lauf in P4 Step 0. **[2026-08-02, P5 Step 0:]**
Zeile 13 (Restore-Nachweis) ist die letzte gefallen — Claude Code fuhr `restore_check.sh`
zunächst selbst als Kandidatenbeleg, der Nikinger führte denselben Lauf danach selbst aus
(identischer HEAD, `ok:true`) — echte Abnahme. **Phase 3 damit vollständig ✅.** Formaler
Abschluss-Handover an P4: `docs/concepts/PHASE3_CLOSEOUT_HANDOVER.md`. Plan: `docs/concepts/
phase3_edge_plan.md` (Entscheidungen P3-A–P3-N gelockt, Steps 0–7). Phase-Head:
`phase3_edge/CLAUDE.md`.

**Phase 2 — MCP-Server** (`phase2_mcp/`, Paket `mcpserver`): ✅ **abgeschlossen,
live-verifiziert seit 2026-07-26** — Quick-Tunnel-Probe + vollständige Adapter-Abnahme über den
echten Custom Connector durch den Nikinger, 21/21 Prüfungen, siehe
`docs/concepts/P2_ADAPTER_ABNAHME_2026-07-26.md`. Claude liest und schreibt über einen lokalen
`fastmcp`-Server auf den P1-Storage-Kern — Token→Space-Auflösung, sechs Tools,
`<untrusted_content>`-Wrapping fremder Bodies. Formaler Abschluss-Handover an P3:
`docs/concepts/PHASE2_CLOSEOUT_HANDOVER.md`. Plan: `docs/concepts/phase2_mcp_plan.md`
(Entscheidungen P2-A–P2-N, Steps 0–7). Phase-Head: `phase2_mcp/CLAUDE.md`.

**Phase 1 — Storage-Kern** (`phase1_storage/`, Paket `storage`): ✅ **abgeschlossen,
live-verifiziert.** Alle acht Module (Steps 0–7), 68 Tests grün (70 bei Phasenabschluss, minus
zwei bei Entfernung toten Codes in P2 Step 0 — siehe `phase1_storage/CLAUDE.md`) —
Frontmatter/Modelle, atomarer Datei-Store, SQLite-Index, Versionierung + Konfliktbehandlung,
Git-Commit je Write, Query-Layer, `space_cli.py` als Beweis. Der Nikinger hat den Lauf gegen den
echten `DATA_ROOT` (`/home/savefyx/savefyx-data`) selbst ausgeführt (2026-07-25, Hard Rule: kein
Test gegen den echten DATA_ROOT durch Claude Code). Details + Transkript:
`phase1_storage/CLAUDE.md`, Session-Block. Plan: `docs/concepts/phase1_storage_plan.md`
(Entscheidungen A–H gelockt, Steps 0–7). Die dort definierten Frontmatter-Felder und
`Store`-Signaturen sind ab jetzt Contract für P2 (drei einmalige, freigegebene Erweiterungen in
P2 Step 2 — siehe P2-Plan §0.4 Punkt L).

**Gelockte Rahmenentscheidungen (Nikinger, 2026-07-24, Browser-Planung):**

| # | Thema | Lock |
|---|---|---|
| R1 | Plan/Ausführung | Planung im Browser-Chat, Ausführung in Claude Code — wie im Trading-Bot-Projekt. |
| R2 | Plan-Tier | Beide Nutzer auf **Claude Pro**. Custom Connectors sind auf Pro verfügbar; jeder fügt seinen Connector selbst hinzu (kein Owner-Gate wie bei Team/Enterprise). `[VERIFY]` bei Ausführung gegen die aktuelle Doku. |
| R3 | Erreichbarkeit | **CGNAT** (RUT X50, Mobilfunk). Start mit **Cloudflare Tunnel** (schnellster Weg zum ersten Erlebnis), Migration auf **VPS + WireGuard** als P3-Option. Der MCP-Server ändert sich dabei nicht. **[2026-07-28 Ergänzung, P4 Step 0]:** Gebaut wurde stattdessen **Tailscale Funnel** (P3-A) — weder Cloudflare Tunnel noch VPS+WireGuard. Die Beschlusslage oben bleibt historisch korrekt stehen; Details zum tatsächlichen Weg: `docs/concepts/phase3_edge_plan.md` §0.4. |
| R4 | Vertraulichkeit | Bewusst akzeptiert: bei Cloudflare Tunnel terminiert Cloudflare TLS und sieht Klartext. **Kein E2E.** Der Server muss lesen können, damit Claude lesen kann — das schließt das Krypto-Modell des `Notizheft_example.html` aus. **[2026-07-27 Ergänzung, P3 Step 0]:** Ab P3 läuft der Weg über Tailscale Funnel; dort terminiert die Node selbst TLS, siehe `docs/concepts/phase3_edge_plan.md` §0.4. Der Relay-Betreiber sieht Notizinhalte damit nicht mehr im Klartext — „kein E2E" bleibt trotzdem richtig, denn Tailscale bleibt vertrauenswürdige Infrastruktur (Koordinationsserver, DNS, Relays). |
| R5 | Auth v0 | Token im Pfad (`/mcp/<token>`), Token = Identität = Space. Ehrlich benannter Kompromiss (Bearer-Passwort in einer URL, landet in Logs). **OAuth 2.1 + DCR ist Phase 4**, nicht optional-für-immer. **[2026-07-30 abgelöst, P4 Schnitt:]** Der Pfad-Token existiert nicht mehr — `TokenPathASGI` ist aus dem Code entfernt, beide Pfad-Token live widerrufen, `SPACE_AUTH_MODE` lässt nur noch `oauth` zu. Der Connector authentifiziert sich seither über OAuth 2.1 + DCR (Passwort + TOTP), siehe P4. |
| R6 | Zweck | **Lernprojekt**, später evtl. Arbeitswerkzeug. Bei Zielkonflikt gewinnt Lerneffekt über Bequemlichkeit — außer bei Safety/Secrets, dort gewinnt immer die sichere Variante. |

**Noch nicht entschieden (bewusst offen, für spätere Planungssessions):**
- ~~MCP-Werkzeug-Ergonomie, fünf offene Punkte~~ **[2026-08-20 geplant und gelockt]** — jetzt
  Block A von Phase 6.5 (`docs/concepts/phase6_5_tools_images_plan.md` §3, Entscheidungen
  P6.5-A–P6.5-H u. a.). Kein offener Planungsbedarf mehr — nur noch **nicht gebaut**. Der
  Absatz unten bleibt als Herkunftsnachweis stehen.
- ~~Item-Verschieben zwischen Ordnern und Spaces~~ **[2026-08-17 geplant und gelockt]** —
  `phase6_shares/ITEM_MOVE_PLAN.md` §4 (Step 7b, Space-Move, Entscheidungen P6-AD–AJ) + §9
  (Mehrfachauswahl, P6-AK–AN) sind ausführungsreif und per Nikinger-Freigabe gelockt. Kein
  offener Planungsbedarf mehr — nur noch **nicht gebaut**. Details:
  `phase6_shares/CLAUDE.md`s aktuellem Session-Block.
- **MCP-Werkzeug-Ergonomie, Live-Feedback einer arbeitenden Claude-Instanz** (Nikinger-Meldung,
  2026-08-14, nach einem sitzungsreichen Protokollierungstag — 40+ `append_to_item`-Aufrufe für
  ein einziges Log-Dokument) — sechs Punkte: kein Bulk-Append, `list_spaces` in der eigenen
  Tool-Exploration nicht auffindbar genug (führte zur falschen Aussage „Claude kann nur im
  eigenen Space schreiben"), `patch_item`-vs-`update_item`-Aufgabenteilung nirgends
  zusammengefasst, `get_item` liefert immer den vollen Body (kein `get_item_meta` nur für
  Frontmatter/Version), Status-Enum-Werte nicht in der Tool-Beschreibung dokumentiert (Ratefehler
  „archiviert" statt „archived"), gelegentlich unzuverlässige Suchtreffer. **Ein Befund davon ist
  eine irreführende Fehlermeldung, kein reines Ergonomie-Wunsch:** `patch_item` auf einem
  Frontmatter-Feld liefert „0 Treffer — lies das Item neu" (klingt nach Textmatching-Problem),
  obwohl die Ursache kategorisch ist (`patch_item` erreicht Frontmatter grundsätzlich nicht) —
  ein erneutes Lesen hätte nie geholfen. **[2026-08-14 behoben]** dieser eine Befund (Text nennt
  jetzt die Ursache + `update_item` als Alternative, keine Frontmatter-Erkennungslogik ergänzt);
  die übrigen fünf Punkte betreffen ausschließlich `mcpserver/tools.py` (P6-C erlaubt das) und
  sind **[2026-08-20]** als Block A von Phase 6.5 geplant, siehe oben. Volltext:
  `phase6_shares/CLAUDE.md`, Abschnitt „Vormerkungen".

**[2026-08-02 Korrektur, P5-Planungssession]:** der bis dahin offene Punkt „Web-UI: Neubau gegen
die REST-API vs. Adaption des `Notizheft_example.html`" ist entschieden — **Neubau mit Ernte**
(Entscheidung P5-V, `docs/concepts/phase5_ui_plan.md` §0.5): Layout-Ideen sowie
`sanitizeHtml`/`markdownToHtml` werden übernommen, die clientseitige Vault-Verschlüsselung
(unvereinbar mit R4), `localStorage`/IndexedDB und `connect-src 'none'` werden verworfen.

**[2026-07-28 Korrektur, P4 Step 0]:** Der Punkt „Ob der Kollege einen eigenen Server-Prozess
oder nur einen eigenen Space bekommt" stand hier fälschlich noch als offen. Das ist seit P3-G
entschieden und live bewiesen: **ein Prozess, ein Space je Person.** Zwei Spaces existieren real
(`niklas`, `fabian`), beide über denselben `sharefyx-mcp.service`.
