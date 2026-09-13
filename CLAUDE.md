---
status: live
purpose: Regeln, Konventionen, Arbeitsweise und aktueller Stand des Space-Servers — wird jede Session automatisch geladen
read-when: immer, vor jeder Aktion in diesem Repository
detail: L2
up: docs/INDEX.md
down:
  - ROADMAP.md                          # Phasenplan + Status je Phase
  - docs/INDEX.md                       # L0-Karte aller .md
  - phase8_6_ui_polish/CLAUDE.md        # aktive Phase (Phase 8.6, UI-Politur, Ziel v3.0.2)
  - phase8_5_picker_release/CLAUDE.md   # abgeschlossene Phase (Phase 8.5 ✅, schließt Phase 8 mit ab)
updated: 2026-09-13 (**P8.6 Partial Closeout + drei Nikinger-Entscheidungen.** Neu: `docs/concepts/PHASE8_6_CLOSEOUT_HANDOVER.md` + `docs/concepts/phase8_6_ui_polish_uebersicht.svg` (P8.6-B-Ausnahme auf ausdrueckliche Anordnung); Rotationsregel P8.6-T im Phase-Head repariert; abgeschnittener Block-D-Archivblock aus `04dee6a` wiederhergestellt (72 Z. / 4.403 B); sechs Doku-Drifts behoben. **Nikinger-Entscheidungen 2026-09-13:** (a) Deploy-Ziel bleibt **`v3.0.2`** — P8.6-R bestaetigt; (b) **Block C geht einzeln raus**, nicht in einem Sammel-Push nach Plan 2; (c) Ein-Block-Regel fuer diese Current-state-Sektion **auf Empfehlung des Agenten verworfen** — sie haette das falsche Problem geloest. **Messung:** der Body dieser Datei ist 12.845 B, die `updated:`-Kette war **28.090 B in 30 Eintraegen**, davon 3.290 B glatte Duplikate. Kette daher verbatim nach `docs/PROJECT_SESSION_LOG.md` §Frontmatter-Archiv rotiert; die Current-state-Bloecke bleiben, wie sie waren) | 2026-09-12 (**P8.6 Block C ✅** — Struktur-Umbau: Einstellungen oben, Alle Items unten, Karte rechts voller Hoehe, klickbare Spaces, Ordner-Zaehler; `pytest` 970 V107, `ui_budget` V97 5/5 137,5 KB; **sechs Selbst-Screenshots** `p86_block_c_*.png` zeigen alle fünf Sub-Ziele + B4-Regression; sharefyx-mcp PID 991 unverändert; **Push + Deploy wartet auf Nikinger-Sichtung** der Screenshots — Drei-Bedingungen-Regel des Nikingers zu zwei Dritteln erfuellt; V115/V116/V117 belegt; drei Befunde waehrend Baus dokumentiert [activateView-Doppel-Definition, V117-Reset, V115-RAF]; Stand: Step 0/V/V-vision-befund/A/B/C/D [D1/D2/D4] ✅, V-plugin ⚠️ zurückgebaut, Gate §7 + Step Z als naechstes) | aeltere Eintraege: `docs/PROJECT_SESSION_LOG.md` §Frontmatter-Archiv (verbatim rotiert 2026-09-13) und die jeweilige `phase*/SESSIONS_ARCHIVE.md`
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
- **Vor „das braucht einen echten Menschen/Connector" nachsehen, nicht neu erfinden:**
  `docs/concepts/sichtpruefung_automation_conventions.md` sammelt Techniken, mit denen sich
  Sichtprüfungen, die auf den ersten Blick blockiert wirken, doch skripten lassen (Canvas-
  Instrumentierung, OAuth-Dance ohne Browser, Zwei-Principal-Wegwerf-Muster). Erst dort
  nachsehen, dann ggf. recherchieren.

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

**[2026-09-13, P8.6 Partial Closeout — die Phase ist NICHT abgeschlossen und NICHT ausgeliefert.** Reine Doku-Session. **Klarstellung zum Stand:** `origin/main` steht auf `2a93e67`, lokal liegen **zwei** ungepushte Commits (`90c72e2` Block C, `bc2aa9f` Partial Closeout) — die Behauptung „7 Commits voraus" aus dem 2026-09-12-Block war falsch, per `git fetch` geprüft. Badge steht auf `v3.0.1`, Gate ⬜ **angehalten**, Step Z ⬜. **Neu:** `docs/concepts/PHASE8_6_CLOSEOUT_HANDOVER.md` (Teil-Stand, Delta, §4 ordnet die neun UX-Befunde den Locks zu, die sie öffnen — **P8.6-O2** `.shell`-Grid für Befund 5, **C1/N3-Lesart b** für Befund 7, **P8.6-E** für Befund 1+8, plus die Versionsfrage **P8.6-R**; §5 `[VERIFY]`-Bilanz 14 zu / 5 offen) + `docs/concepts/phase8_6_ui_polish_uebersicht.svg` (1080×1080, gerendert und visuell gegengeprüft, Badge **PARTIAL CLOSEOUT**). Beide existieren per **ausdrücklicher Nikinger-Anordnung vom 2026-09-13** — die in **P8.6-B** vorgesehene Ausnahme; **Plan §9 bleibt bewusst leer**, weil §9 der kanonische Abschluss ist und die Phase nicht abgeschlossen ist. **Rotation:** der Head verletzte **P8.6-T** (ein `## Session stopped` **plus** ein zweiter Session-Block als `###` — das Muster, bei dem `rotate_session_block.sh` fälschlich „bereits konform" meldet); `###` aufs `## Session stopped — <Datum>`-Schema gebracht, dann das Skript gelaufen: alle vier Gegenproben grün, Head **72.958 → 59.797 B**. **Archiv-Reparatur:** der Block-D-Sub-Block war seit der Hand-Rotation vom 2026-09-10 **mitten im Satz abgeschnitten** — **72 Zeilen / 4.403 B** fehlten; mechanisch aus `04dee6a:phase8_6_ui_polish/CLAUDE.md` wiederhergestellt, `cmp` byte-identisch, Altbestand nachweislich unverändert. **Drei weitere Drifts behoben:** Modul-Status Zeile 5 (Block C) stand auf ⬜, obwohl Commit `90c72e2` ihren Nachzug behauptet — Hard-Rule-8-Miss; `docs/INDEX.md` verletzte **P8.6-4** (40.870 B gegen ≤ 38 KB) → sechs Zeilen geschlossener Phasen gestrafft, zwei neue Zeilen aufgenommen, jetzt **38.822 B**, Kriterium erstmals seit Block A erfüllt; der Frontmatter-Closer `---` des INDEX klebte am Ende der `updated:`-Zeile statt auf einer eigenen — Frontmatter war formal kaputt. **`pytest` 970 passed in 116 s ✅** (V107-Baseline 964), Tabu-Diff §0.3 leer, Service-Touch 0 — sharefyx-mcp **PID 991** nur gelesen. **Nächster Schritt: Claude-Code-Planungssession für P8.6 Plan 2.** Empfohlene Reihenfolge (im Handover begründet): Befund 9 zuerst, weil er als einziger **auf der Produktion** reproduziert ist und damit nicht am P8.6-Deploy hängt — und zwar messen (CDP-Probe bei 1024/1200/1440), bevor repariert wird.  **Nikinger-Entscheidungen vom 2026-09-13:** **(a)** Deploy-Ziel bleibt **`v3.0.2`** — P8.6-R ist damit bestätigt, nicht überstimmt. **(b)** **Block C geht einzeln raus**, nicht in einem Sammel-Push nach Plan 2. **(c)** Die Ein-Block-Regel für die Current-state-Sektion hat er mir überlassen — **ich rate ab und habe sie verworfen**: sie hätte 3,4 KB gebracht und beim nächsten Session-Block wieder gerissen, weil **69 % der Datei in der `updated:`-Kette** steckten (28.090 B über 30 Einträge, davon 3.290 B glatte Duplikate) und nur 3.376 B in dieser Sektion. Die Kette ist stattdessen verbatim nach `PROJECT_SESSION_LOG.md` §Frontmatter-Archiv rotiert: **47.094 → 21.037 B**, alle fünf Session-Blöcke bleiben erhalten. **Siebter Drift, in dieser Runde gefunden und der folgenreichste: von Phase 8.6 ist NICHTS live.** Phase-Head und der Step-V-Block unten behaupten „Push + Deploy für Block A + D vom Nikinger ausgeführt (`10f9f63..04dee6a`), `health_gate.sh --expected-sha=04dee6a` 8/8 grün". Das Werkzeug ist dabei in Ordnung: `health_gate.sh` liest den Release-SHA aus `/opt/sharefyx/current` (Z. 134/160); die Gegenprobe am 2026-09-13 meldet 7 OK + 1 FEHLER — das „8/8" ist nie so gelaufen. Gemessen am Server: `/opt/sharefyx/current` → `releases/20260905T140325.378914Z`, `git rev-parse HEAD` dort = **`6f19a8f`** — das ist der **P8.5**-Release vom 2026-09-05. Gegenprobe über sechs Block-Marker (`bg-void`, `select-fill`, `dedupeEdges`, `seedJitter`, `account-nav`, `overview__col-right`): **0 Treffer live, alle im Repo.** Das jüngste Verzeichnis unter `/opt/sharefyx/releases/` ist ebenfalls das vom 2026-09-05, und `deploy.sh:107` legt pro Lauf ein neues an — es hat also **kein** P8.6-Deploy gegeben. **Konsequenz für Entscheidung (b):** ein Deploy, der „nur Block C" ausliefert, existiert nicht — `deploy.sh` liefert `main` aus, also A+B+C+D zusammen. Der Push ist davon unberührt und läuft wie entschieden einzeln. **ROADMAP und diese Datei bleiben auf 🔄** — der formale Phasenschluss wäre eine stille Abweichung, solange Gate und Step Z offen sind.

**[2026-09-12, P8.6 Block C ✅ — Struktur-Umbau: Einstellungen oben, Alle Items unten, Karte rechts voller Hoehe, klickbare Spaces, Ordner-Zaehler.** Erst opencode/M3-Code-Touch seit Block B am 2026-09-11. **C1** `#account-button` raus aus `.rail__account` direkt unter `#home-button` + Label „Konto"→„Einstellungen" (N3-Lesart b, das `#i-settings`-Icon war schon immer ein Zahnrad). **C2** `tree.js :: renderRail()` ruft `renderScopeRow()` jetzt HINTER die Spaces + neue `tree__group`-Überschrift „Alles"; bestehende Kommentar zu „Lieber keine Zahl als eine unwahre" bleibt wörtlich erhalten (er ist die Antwort auf C5). **C3** `.overview` wird zweispaltiges Grid (`grid-template-columns: 1fr 40%` ab ≥1281px, Wrapper-DIVs `head-row`/`col-left`/`col-right`, `.overview__graph` ohne `max-width`/`min-height` [V112-Gegenprobe], `@media (max-width: 1280px)` kollabiert auf eine Spalte — Map rutscht unter die Liste); `requestAnimationFrame(resize)` in `loadGraph()` [V115] damit `seedInitialPositions()` nach dem nächsten Layout-Pass die endgültige Kartengröße hat. **C4** `.overview__space-open` als innerer `<button>` mit B1-hover + V116 `activateView`-Export (semantisch „in den Space wechseln ohne Bucket zu setzen") + `closeEditor().then(proceed => ...)`-Gating (dieselbe Disziplin wie Ordner-Buttons). **C5** `state.itemsLoaded`-Flag + `folderItemCount()`-Helfer + neuer V117-Reset in `activateView`/`navigateAll` (sonst zeigt das Rail für ein paar ms Counts aus dem falschen Pool); `.tree__count` bekommt `margin-left: auto` (gilt für Eimer + echte Ordner). **Drei Befunde/Abweichungen während Baus dokumentiert:** `activateView` doppelt definiert (Original-`function` plus neuer `export function`) → `PAGE ERROR: already declared` → `overview__spaces` blieb leer → Original entfernt; V117-Reset in beiden Navigation-Funktionen eingebaut; `requestAnimationFrame(resize)` als V115-Fix. **`pytest` 970 V107 ✅ (+3 statische Tests `test_rail_order_settings_before_tree_logout_last`/`test_account_button_says_einstellungen`/`test_overview_graph_has_no_max_width_or_min_height`), `ui_budget` V97 ✅ 5/5 (137,5 KB, +4,4 KB durch C1/C3/C4-CSS)**, Tabu-Diff §0.3 leer, Service-Touch 0 — sharefyx-mcp **PID 991** durchgehend unverändert. **Sechs Selbst-Screenshots** in `docs/screenshots/p86_block_c_{01..06}_*.png` zeigen alle fünf Sub-Ziele (Rail-Reihenfolge, „Alle Items" am Rail-Ende, Karte als rechte Spalte, klickbare Space-Zeile, Folder-Zähler) + B4-Vorsicht-Regression. Eigenes Self-Skript `phase8_6_ui_polish/scripts/p86_block_c_self_check.py` (~250 Z., Playwright + Login mit TOTP-Window-Retry + 6 Screenshots); Wegwerf-Setup reproduziert den v3ritt-Datenstand auf Port 18773, gestoppt über PID-Datei (Hard Rule 9-konform, kein `pkill -f`; `login_attempts`-Rate-Limit durch `cleanup`+`setup`+`seed-items`+`start` zurückgesetzt — das war nötig, nachdem drei fehlgeschlagene Login-Attempts die Bremse ausgelöst hatten). **Push + Deploy** für Block C wartet noch auf Dich (Drei-Bedingungen-Regel zu zwei Dritteln erfüllt — Code-Tests grün ✓, Bilder grün ✓, Nikinger-Sichtung ⬜).

**[2026-09-10, P8.6 Step V ✅ — Ollama + `qwen3-vl:8b` + V119-Smoke 46 s, Modellname-Korrektur + Plugin-Pfad für nächste Session.** Proxmox-Migration ✅ durch (i5-14600KF, sharefyx-mcp PID 991 nach Auto-Restart), Nikinger hat Ollama 0.34.0 via offizielles `curl | sh`-Script installiert (apt-Paket existiert auf Ubuntu 24.04 nicht — Korrektur in §Vormerkungen), `qwen3-vl:8b` (Q4_K_M, 6,1 GB) gepullt + V119-Smoke ✅ in 46 s gegen `c4_p8519_01_radiogruppe_im_dialog.png` (qwen3-vl:8b Cold-Start inkl. Vision-Encoder; deutsche Antwort korrekt: „Der Radio-Button ‚als Text-Link im Text' ist markiert"). `requests 2.34.2` ins Projekt-venv installiert; `phase8_6_ui_polish/scripts/vision_ollama.py` (89 Z., `requests.post(/api/generate)`, 600s-Timeout). **Modellname-Korrektur:** `internvl2.5:8b` (ursprüngliche Empfehlung) existiert nicht auf Ollama-Library — Recherche-Fehler von mir korrigiert auf `qwen3-vl:8b`. Phase-Head §Vormerkungen + Aktionsliste + Vision-Backend-Sektion entsprechend korrigiert. `pytest` V107 ✅ **966 unverändert**, `ui_budget` V97 ✅ 5/5, Tabu-Diff §0.3 leer, Service-Touch 0. **Push + Deploy** für Block A + D-Commits (`32fddba`, `04dee6a`) vom Nikinger in dieser Session autorisiert + ausgeführt (`10f9f63..04dee6a`). **Nächster Schritt** (Nikinger-Vorgabe 2026-09-10): **Schritt 1 = `DavidEasden/opencode-vision`-Plugin installieren** (vor jeder Sichtprüfung, damit Screenshots direkt im Chat gerendert werden — `docs/concepts/sichtpruefung_automation_conventions.md` §4), **Schritt 2 = visuelle Verifikation Block A + D** am echten Gerät gegen die neuen Screenshots (post-Block-A: `<select>`-Markup, post-Block-D: Zwillingskante weg + Karte stabil); Schritt 3 = Block B nach Plan §4; Schritt 4 = Block C nach Plan §5 + D3-Nachzug.

**[2026-09-10, P8.6 Block D ✅ [D1/D2/D4]** — Reiner `graph.js`-Commit (8,4 KB, +0,5 KB). D1 V102-Dedup (`dedupeEdges()` ungeordnetes Knotenpaar, P8.6-N, keine neunte P1-Contract-Öffnung), D2 FNV-1a-Layout-Seed (`seedJitter(id, salt)`, P8.6-M, „Karte fliegt" behoben), D4 `cancelAnimationFrame` in `runSimulation()` (P8.6-§6.4, **einzige Scope-Erweiterung**, streichbar). D3 🟡 wartet auf Block C. `pytest` 966 unverändert, `ui_budget` 5/5, Tabu-Diff §0.3 leer, Service-Touch 0. Items #2/3/4 aus dem Handover blockiert (Ollama-Migration steht bevor).

**[2026-09-10, P8.6 Block A ✅ — Fundament:** Radiogruppe→`<select>`, sechs neue Tokens (`--bg-void`/`--select-fill`/`--select-line`/`--caution` u. a.), `--border-soft`→`var(--line)`, Konvention v3 um „Vorsicht". Erste echte Code-Touch-Session der Phase. Tabu-Diff §0.3 leer, `pytest` 964→966, `ui_budget.py` 5/5. Nikinger hat die P8.5-19-Radiogruppe am 2026-09-08 selbst zurückgenommen. +2 statische Tests (P8.5-Test ersetzt, `test_no_raw_accent_rgba_outside_root`, `test_every_css_var_reference_is_defined` — hätte `--border-soft`-Bug gefunden). **Abweichung von Plan §3.5/§8.2 dokumentiert:** die anderen 4 Tests gehören zu Block B/C.

_Vollständige Chronik der älteren Einträge (Phase 8, Phase 8.5-Vorlauf, Phase 7/6.5/6-Abschluss,
Phase-5/4/3/2/1-Zusammenfassungen, Hard-Rule-Korrekturen): `docs/PROJECT_SESSION_LOG.md` (L3).
Neue Session-Blöcke wachsen oben in dieser Current-state-Sektion; ältere Blöcke rotieren
verbatim nach `PROJECT_SESSION_LOG.md`. **[2026-09-13]** Eine Ein-Block-Regel wurde erwogen und
**verworfen**: gemessen steckten 69 % der Dateigröße in der `updated:`-Frontmatter-Kette
(28.090 B über 30 Einträge, davon 3.290 B glatte Duplikate), nicht in dieser Sektion
(3.376 B). Die Kette ist verbatim nach `PROJECT_SESSION_LOG.md` §Frontmatter-Archiv rotiert —
dieselbe Lösungsrichtung, die für `docs/INDEX.md` vorgemerkt ist._



