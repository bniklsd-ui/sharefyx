---
status: archive
purpose: Archivierte Session-stopped-Blöcke aus phase8_6_ui_polish/CLAUDE.md, verbatim, newest-first
read-when: Auditieren der vollen Phase-8.6-Historie — der aktuelle Session-Block lebt im Phase-Head, nicht hier
detail: L3
up: ./CLAUDE.md
down:
updated: 2026-09-10 (V-umgesetzt-Sub-Block [vom 2026-09-10 früh] verbatim aus dem Phase-Head hierher rotiert vor dem V-plugin-Commit (P8.6-T-Rotationsregel); Phase-Head trägt jetzt nur den V-plugin-Sub-Block, SESSIONS_ARCHIVE jetzt mit sieben Sub-Blöcken)
---
# SESSIONS_ARCHIVE.md — Phase 8.6: UI-Politur, Selektion + Layout, drei Graph-Fixes

Archiv der historischen Sub-Blöcke, newest-first. Der aktuelle Session-Block lebt im
Phase-Head (`./CLAUDE.md` §Session stopped). Rotation nach P8.6-T: bei jedem neuen
`### date`-Sub-Block wandert der bisherige **verbatim** hierher. Skript
`scripts/rotate_session_block.sh phase8_6_ui_polish` für saubere Übernahme — die
Phase-8.5-Step-V-deferred-Rotation am 2026-09-10 wurde **per Hand** gemacht, weil
das Skript auf das Phase-8.5-Muster passt und mit einem `## Session stopped` + mehreren
`### date`-Subblöcken Exit 2 „Bereits konform" wirft.

---



### 2026-09-10 (Step V ✅ — Ollama 0.34.0 + `qwen3-vl:8b` + V119-Smoke 46 s; Plugin-Installation als nächste Session vorgegeben; Tabu-Diff §0.3 leer, pytest 966 unverändert)

**Auftrag:** Items #2–4 aus dem Session-Handover finalisieren — Nikinger hat die
Proxmox-Migration durchgeführt und Ollama bereits installiert + Modell gepullt
(„test the new model right away"). Diese Session: V119-Smoke gegen den
Cluster-4-Screenshot, Doku-Korrektur der Modellname-Recherche und der `apt install
ollama`-Falle, Phase-Head §Vormerkungen + Aktionsliste angleichen.

**Was in diesem Commit passiert ist:**

1. **`requests` ins Projekt-venv installiert** — eine Zeile
   (`.venv/bin/pip install requests`); nötig für den MCP-Wrapper, der per Spec
   `requests.post(...)` verwendet. `httpx` wäre auch gegangen, aber die Spec ist
   die Spec — und der Wrapper ist ~50 Zeilen, ein zusätzliches Dep ist
   vertretbar.

2. **`phase8_6_ui_polish/scripts/vision_ollama.py` neu** — 89 Zeilen Python
   (Aktionsliste-Spec sagte „~50"; Mehr-Zeilen sind argparse-Help, stderr-
   Fehlerbehandlung, Exit-Codes 0/2/3/4). CLI: `--image <pfad>` +
   `--prompt <text>` + `[--model <name>]` + `[--endpoint <url>]`. Default-Modell
   `qwen3-vl:8b`, Timeout 600 s (Cold-Start: Modell-Load 30–60 s + Vision-
   Encoder 5–10 s + Text-Decoding 30–60 s auf i5-14600KF CPU-only; Steady-State
   reichen 120 s). Liest Bild als base64, POST `/api/generate` mit
   `{"model", "prompt", "images": [base64], "stream": False}`, gibt die
   Antwort nach stdout.

3. **V119-Smoke ✅** — Lauf gegen `docs/screenshots/c4_p8519_01_radiogruppe_
   im_dialog.png` (167 KB, Cluster-4-Aufnahme aus P8.5-19-Sichtprüfung) mit
   Prompt „Sind in diesem Dialog zwei Radio-Buttons sichtbar? Welcher ist
   markiert?". **Dauer 46 s** (Cold-Start inkl. Vision-Encoder). **Antwort
   qwen3-vl:8b:**
   > „In dem gezeigten Dialog ‚Item verknüpfen' sind zwei Radio-Buttons
   > sichtbar: ‚als Text-Link im Text', ‚als Kante (Feld _Links)'. Der
   > Radio-Button ‚als Text-Link im Text' ist markiert."
   Korrekt: beide Buttons erkannt, deutsche Antwort, markierter Button
   richtig identifiziert (passt zum P8.5-19-Stand der Datei). **V119 damit
   ✅** — Modul-Status Z.2 🟡 → ✅.

4. **Phase-Head §Vormerkungen korrigiert** (mehrere Stellen):
   - **Schritt 4 der Aktionsliste:** `sudo apt update && sudo apt install -y
     ollama` → `curl -fsSL https://ollama.com/install.sh | sh`. Auf Ubuntu
     24.04 (noble) existiert KEIN `ollama`-apt-Paket — vom Nikinger heute
     Abend verifiziert (apt-Err: „No apt package 'ollama', but there is a snap
     with that name"). Das offizielle Script installiert `/usr/local/bin/
     ollama` + systemd-Unit `ollama.service` (Restart=on-failure, After=
     network-online.target).
   - **Modellname:** `internvl2.5:8b` → **`qwen3-vl:8b`**. Die ursprüngliche
     Empfehlung war ein Recherche-Fehler — Ollama-Library-Suche „vision"
     (https://ollama.com/search?q=vision, 2026-09-10) listet `internvl2.5`
     **nicht**; `qwen3-vl:8b` (6,1 GB Q4_K_M, Apache-2.0) ist die Erstwahl.
     Fallbacks dokumentiert: `qwen2.5vl:7b`, `llava:13b`, `minicpm-v:8b`,
     `llama3.2-vision:11b`. Der Wrapper hat `--model` für den Fall der Fall.
   - **„Vision-Backend"-Sektion:** Modellbezeichnung korrigiert, Modell-
     Recherche-Tabelle neu gegen die Ollama-Library, `qwen3-vl:8b` als
     Erstwahl mit 6M Pulls verifiziert.
   - **„Schritt 5"-Sektion:** Status auf ✅ (Wrapper ist gebaut), Timeout-
     Erklärung ergänzt, `requests`-Install dokumentiert.
   - **„Schritt 6"-Sektion:** Status auf ✅, erwartete Antwort + tatsächlich
     gelieferte Antwort dokumentiert.

5. **`## Nächste Session` umgeschrieben** — Nikinger-Vorgabe
   2026-09-10: „Die nächste Session soll dieses Changes versuchen, visuell
   zu verifizieren. Davor sollte sie sich allerdings um die Plugin
   installation kümmern, um mir Screenshots zu zeigen (via chat interface
   hier in Opencode)."
   - **Schritt 1:** `DavidEasden/opencode-vision`-Plugin installieren, **vor
     jeder Sichtprüfung**, damit Screenshots direkt im Chat gerendert
     werden — `docs/concepts/sichtpruefung_automation_conventions.md` §4.
   - **Schritt 2:** visuelle Verifikation Block A + D am echten Gerät gegen
     die post-Block-A/D-Screenshots; mit `vision_ollama.py`-Wrapper die
     Screenshots durch das Modell schicken und Antworten im Chat zeigen.
   - **Schritt 3:** Block B nach Plan §4 (optional parallel).
   - **Schritt 4:** Block C nach Plan §5 + D3-Nachzug.

6. **`docs/INDEX.md` (Phase-8.6-Zeile)** — der Eintrag zur Phase-8.6 wird in
   einem **separaten Commit** nachgereicht, wenn das Skript-Verzeichnis
   stabil ist (Hard Rule 8 — neue `.md`-Datei braucht eine INDEX-Zeile;
   `vision_ollama.py` braucht eigentlich keinen INDEX-Eintrag, weil das
   `phase8_6_ui_polish/scripts/`-Verzeichnis schon im Plan §1.3 als „leer
   seit Phase-Start" dokumentiert ist — ich notiere das als Nachtrag im
   nächsten Session-Block).

**Selbstprüfung (§0.5):**

- **Tabu-Diff §0.3** leer — `.venv`-Site-Packages-Änderung ist
  `requests 2.34.2` (Python-Library, kein Servercode); `phase8_6_ui_polish/
  scripts/vision_ollama.py` ist erlaubt (§0.3 listet explizit
  `phase8_6_ui_polish/scripts/**` als erlaubten Pfad).
- `pytest -q` V107 ✅ **966 unverändert** — kein Python- oder JS-Touch.
- `node --check` gegenstandslos (Python-Skript, nicht JS).
- `ui_budget.py` gegenstandslos (kein `webui/static/`-Touch; das `graph.js`-
  Wachstum aus Block D (+0,5 KB) bleibt im Korridor).
- **V119-Smoke selbst:** ✅, 46 s, korrekte Antwort.
- **Service-Touch 0** — `systemctl cat tailscaled`/`cat sharefyx-mcp.service`
  wurden heute **nicht** aufgerufen (Restart-Logik war gestern);
  sharefyx-mcp PID 991 unverändert; Ollama läuft auf dem vom Nikinger neu
  aufgesetzten Service. **Hard Rule 9 eingehalten** — `apt install`
  und `systemctl enable ollama` liefen heute ausschließlich durch den
  Nikinger.
- **Größenprüfung:** `phase8_6_ui_polish/CLAUDE.md` aktueller Stand
  weiter unten. Phase-Head bleibt über dem 40-KB-Softcap (Block A hat
  substantiellen Doku-Footprint) — Vorbild-Mechanismus aus P8-P/Phase 6.5.
- **Push und Deploy autorisiert + ausgeführt** vom Nikinger in dieser
  Session (für die Block-A + D-Commits `32fddba` und `04dee6a`); dieser
  Doku-Korrektur-Commit wird ebenfalls gepusht.

**Was bewusst NICHT in diesem Commit passiert ist:**

- Kein `pkill -f`, kein `sudo systemctl` (Hard Rule 9).
- Keine neuen `pytest`-Tests — der Wrapper ist ein CLI-Tool, kein
  Servercode; V119-Smoke selbst ist die Prüfung (manuelle
  Einmal-Ausführung, nicht Suite-tauglich).
- Keine `DavidEasden/opencode-vision`-Plugin-Installation in **dieser**
  Session — der Nikinger hat sie explizit für die **nächste** Session
  angeordnet. Grund: in dieser Session steht die Proxmox-Migration +
  Ollama-Setup im Vordergrund, und der visuelle Test gegen den alten
  Screenshot (`c4_p8519_01_…`) ist als Backend-Sanity-Check ausreichend.
  Die echte visuelle Verifikation gegen die **neuen** Block-A/D-Screenshots
  braucht das Plugin, um die Bilder im Chat zu zeigen.
- Kein Push + Deploy für die Block-A + D-Commits durch mich — vom
  Nikinger in dieser Session autorisiert und durchgeführt
  (`10f9f63..04dee6a`).
- Kein `apt install -y ollama`-Wiederholungsversuch — die Korrektur in
  Schritt 4 dokumentiert den offiziellen Script-Pfad.

**Hard-Rule-8-Doku-Update im selben Commit:** Phase-Head Modul-Status
Z.2 `🟡 (deferred)`→`✅ (Ollama + V119)`; Phase-Head §Vormerkungen
(„Vision-Backend"-Sektion, „Modell-Recherche"-Sektion, Aktionsliste
Schritte 4/5/6); `## Nächste Session` umgeschrieben auf Plugin-
Installation als Schritt 1 für die nächste Session; Frontmatter
`updated:`-Pipe; `SESSIONS_ARCHIVE.md` Frontmatter `updated:` + verbatim
Rotation des Block-D-Sub-Blocks.

**Commit-Message (geplant):**
`phase 8.6: Step V umgesetzt -- Ollama + qwen3-vl:8b + V119-Smoke + Modellname-Korrektur`

**Nächster Schritt (für die nächste Session, vom Nikinger vorgegeben):**
1. `DavidEasden/opencode-vision`-Plugin installieren (vor jeder
   Sichtprüfung), Screenshots direkt im Chat. Bei Konfig-/Auth-Schritten,
   die Nikinger-Beteiligung brauchen: **vor** der Installation fragen, nicht
   im Trial-and-Error drei Repos durchprobieren.
2. Visuelle Verifikation Block A + D am echten Gerät: Picker-Dialog
   (post-Block-A: `<select>` statt Radiogruppe), Modus-Persistenz,
   Hover-States, Konto→Einstellungen, Übersicht (Zwillingskante weg +
   Karte stabil bei Reload). Screenshots durch `vision_ollama.py` schicken,
   Antworten im Chat.
3. Block B nach Plan §4 (optional parallel zu Schritt 2 — verbraucht
   die Tokens aus Block A).
4. Block C nach Plan §5 + D3-Nachzug.

### 2026-09-10 (Step 0 — nachträglich: Step V aufgeschoben, lokales Modell + Proxmox-Migration; kein weiterer Code-Touch)

**Auftrag:** Nach kurzer Recherche und drei Rückfragen hat der Nikinger entschieden, dass
Step V (Plan §2, OpenCode-Vision-Plugin-Installation) **aufgeschoben** wird zugunsten eines
**lokalen Vision-Modells** auf einem **neu zu migrierenden Proxmox-Host** (i5-14600KF
primär, danach Ryzen 7 5800X). Plugin-Pfad bleibt als Vormerkung, falls die Plugin-Landschaft
sich später ändert — die `DavidEasden/opencode-vision`-Landschaft ist zu unreif
(3 Commits, AGPL-3.0, kein dokumentiertes MCP-Backend) für unseren produktiven Use-Case.

**Entscheidung (mit Begründung):**
- **Backend:** `InternVL 2.5 8B` (Apache-2.0, ~6–8 GB VRAM Q4) auf Ollama-Basis, MCP-Wrapper
  ruft `POST http://127.0.0.1:11434/api/generate` mit base64-Image.
- **Begründung lokal statt API:** Proxmox-Migration des Hosts steht bevor (i5-14600KF ist
  primäres Ziel, danach Ryzen 7 5800X). Proxmox-VM-Migration ist trivial (im Cluster,
  gleiche Architektur). Lokales Modell vermeidet Vendor-Lock-in + Audit-Trail-Aufwand für
  Bild-Analysen in P8.6 + P9. Anthropic-Haiku-API hätte ~3 Cent/Phase gekostet — billig,
  aber die Begründung war eh nie Geld, sondern Tooling-Konsistenz und Audit-Trail.

**Modell-Recherche (Stand 2026-09-10, gegen PromptQuorum „Local Vision Models 2026"):**
- **InternVL 2.5 8B** ✅ — auf GitHub-Screenshots + UI-Mockups + Code-Outputs trainiert, beste
  Passung für unseren Use-Case („sind zwei Radio-Buttons sichtbar?").
- Qwen3-VL 8B — Fallback (multilinguales OCR, 8 Bilder/Request, Apache-2.0).
- Llama 3.2 Vision 11B — verworfen (Deutsch schwächer).
- MiniCPM-V 4.5 — verworfen (UI-Verständnis schwächer).
- Moondream 2 — verworfen (limitierte Szenen-Erkennung).

**Proxmox-Settings (für die nächste Session als Vorlage — die Aktionsliste kommt dort):**

*Host 1: i5-14600KF (6 P-Cores + 8 E-Cores, 20 Threads)*
- vCPUs: **12** = 6 P-Cores (CPU-Typ `host`, gepinnt auf Cores 0–5) + 4 E-Cores
- RAM: **16 GB** (Ballooning **aus**), 50 GB Thin-LVM auf SSD (`local-lvm`)
- Ollama lauscht auf `127.0.0.1:11434` (kein öffentliches Binding)
- Statische IPv4 im Cluster (für MCP-Erreichbarkeit)

*Host 2: Ryzen 7 5800X (8 Cores, 16 Threads, Zen 3)*
- vCPUs: **10** (8 Cores + 2 Threads, alle gleichwertig, CPU-Typ `host`)
- RAM: 16 GB, 50 GB, Netzwerk identisch

*Proxmox-Details (beide Hosts):* NUMA auf Single-Sockel irrelevant; CPU-Pinning empfohlen;
Memory-Ballooning **aus**; VirtIO-SCSI + iothread für Modell-Disk.

*Setup-Befehle:*
```bash
apt install -y ollama
ollama pull internvl2.5:8b
# MCP-Wrapper-Skript: ~50 Zeilen Python, requests.post mit base64-Image
```

**Was in diesem Commit passiert ist (nur Doku, kein Code-Touch):**
1. `phase8_6_ui_polish/CLAUDE.md`: Modul-Status Zeile 2 (Step V) ⬜ → 🟡-deferred;
   Vormerkungen-Sektion um „Vision-Backend: lokales Modell statt API" + Proxmox-Settings
   erweitert; Session-Stopped-Block um diesen Sub-Block ergänzt (P8.6-T-Rotationsregel:
   genau **ein** `## Session stopped`-Block mit einem oder mehreren `### date`-Subblöcken);
   Nächste-Session-Block auf Proxmox-Migration umgeschrieben.
2. `docs/concepts/phase8_6_ui_polish_plan.md` §2 (Step V): Korrekturnotiz am Anfang
   („Plugin-Pfad übersprungen, siehe Phase-Head-Vormerkungen für Proxmox-Plan").
3. `docs/INDEX.md`: updated-Pipe vorne ergänzt.

**Selbstprüfung (kein Code-Touch — analog zu Step 0):**
- Tabu-Diff §0.3 leer
- `pytest`/`ui_budget`/`node --check` gegenstandslos (kein Code-Touch)
- Service-Touch 0 (PID 355956 unverändert)
- Working-Tree nach Commit sauber

**Commit-Message:**
`phase 8.6: Step V deferred -- Proxmox-Migration + lokales Modell (InternVL 2.5 8B)`

**Nächster Schritt (in der nächsten Session, mit Aktions-Liste):**
1. Proxmox-Migration der Vision-VM auf i5-14600KF-Host
2. `ollama install` + `ollama pull internvl2.5:8b`
3. MCP-Wrapper-Skript (~50 Zeilen Python)
4. Smoke-Test gegen einen Phase-8.5-Screenshot (z. B. `c4_p8519_01_radiogruppe_im_dialog.png`)
   als Regression gegen V119-Erwartung
5. Falls erfolgreich → V119 abgehakt, Konventionen §4 aktiv, Plan §2-Aktualisierung mit
   „Vision-Backend: lokal, InternVL 2.5 8B"
6. Falls Ollama + InternVL auf der CPU nicht zufriedenstellend → Wechsel auf i5-14600KF
   vor Ryzen, oder Qwen3-VL 8B als Fallback

### 2026-09-10 (Step 0 — Haushalt: Phasenverzeichnis, sechs Link-Fixes, vier L1-Cards, INDEX-Kompression, zwei INDEX-Zeilen + zwei Drift-Korrekturen; kein Code-Touch)

**Auftrag:** P8.6-Step-0-Befunde aus der Planungssession gegen `main`@`d1af51b`
(`docs/concepts/phase8_6_ui_polish_plan.md` §1, 2026-09-09) beheben — Phasenverzeichnis
anlegen, sieben Befunde abarbeiten, Baselines V97 + V107 im Head protokollieren. Ein
Commit (Plan §1.10).

**Was in diesem Commit passiert ist (sieben Befunde, in der Reihenfolge ihrer Behebung):**

1. **Befund 1 — sechs kaputte `up:`/`down:`-Links, alle in `p8x_ui_polish_notes.md`**
   gefixt (`../` → `../../`, `./phase8_ui_graph_plan.md` direkt). Gegenprobe gegen die 60
   anderen Frontmatter-Links im Repo: das waren die einzigen sechs.
2. **Befund 2 — vier fehlende L1-Header-Cards** angelegt: `docs/PROJECT_SESSION_LOG.md`
   (L3-Archiv), `phase8_5_picker_release/SICHTPRUEFUNG_RESTBLOCK.md`,
   `phase8_5_picker_release/SICHTPRUEFUNG_WALKTHROUGH.md`,
   `phase8_5_picker_release/CLUSTER3_TESTBLOCK.md`. Die vier dokumentierten Ausnahmen
   (`docs/UPDATE_LOG.md`, `phase5_ui/vendor/lucide/README.md`,
   `phase5_ui/THIRD_PARTY_LICENSES.md`, `phase6_shares/tests/golden/*.md`) bleiben
   korrekt card-los.
3. **Befund 3a — drei `down:`-Listen im Inline-Format** auf Listenform gebracht
   (`docs/concepts/phase6_5_tools_images_plan.md`, `phase6_shares/GLOBAL_SEARCH_PLAN.md`,
   `phase6_shares/IMAGES_PLAN.md`). Der eigentliche Befund war der Prüfer, der diese drei
   Dateien beim alten Listen-Scan still übersprang — gleichzeitig mit dem Fix notiert, der
   P8.6-2-Test wird eine Datei mit leerer `down:`-Extraktion als Warnung ausgeben statt als
   Erfolg.
4. **Befund 4 — zwei fehlende INDEX-Zeilen** ergänzt (`CLUSTER3_TESTBLOCK.md` unter Phase 8.5,
   `THIRD_PARTY_LICENSES.md` unter Referenzmaterial mit Ausnahme-Markierung).
5. **Befund 5 — zwei fehlerhafte INDEX-Zeilen** korrigiert: `phase8_ui_graph/CLAUDE.md`
   bekommt die Softcap-Notiz (Vorbild ist die `phase6_shares`-Zeile, P8-P); `phase5_ui/CLAUDE.md`
   verliert die Behauptung „über dem 40KB-Softcap" — sie war **falsch** (40.957 B = 3 B
   unter dem Softcap), wurde entfernt, ohne die Datei anzufassen.
6. **Befund 6 — `docs/INDEX.md`-Kompression** auf **≤ 38 KB** (genauer: 37.763 B **vor**
   dem Hinzufügen der Phase-8.6-Verzeichnis-Zeilen). Größte Posten: die Plan-Zeilen
   (P8.6/P8.5/P8/P7/P6/P6.5/P5/P4/P3/P2) auf das Wesentliche gestrafft, dated subnotes
   in den Zeilen geschlossener Phasen auf das Neueste + ein Pointer-Satz reduziert
   (L0 ist Landkarte, keine Kurzfassung — Plan §1.5). Sanity-Check: `find … -size +40k`
   trifft die Datei nicht.
7. **Befund 7 — zwei echte Code-Defekte dokumentiert, hier nicht behoben** (Step 0 ist
   Befund, nicht Reparatur): `var(--border-soft)` undefiniert (`app.css:1270/1276`,
   `.link-picker-results` zeichnet keinen Rahmen — Block A / Plan §3.3); `graph.js ::
   runSimulation()` `rafId` lokal aber nie gelesen, kein `cancelAnimationFrame` —
   Block D / Plan §6.4.

**Zusätzlich:** Phasenverzeichnis `phase8_6_ui_polish/` mit `CLAUDE.md` (dieser Head),
`SESSIONS_ARCHIVE.md` (leer mit 📦-Card) und `scripts/` (leer — Wegwerf-Smokes folgen in
Gate/§7) angelegt.

**Selbstprüfung (§0.5):**

- **Tabu-Diff** über die gesamte Phase leer — `git diff --stat -- phase1_storage/storage
  phase4_auth/authserver phase2_mcp/mcpserver phase5_ui/webui/security.py phase5_ui/webui/api.py
  phase5_ui/webui/serializers.py phase5_ui/webui/permissions.py` ergibt nichts (kein
  Code-Touch in dieser Session).
- `pytest -q` nicht gelaufen (kein Python-Touch — Plan §0.5 Punkt 2 gilt, Baseline V107
  von 2026-09-09 reicht für Step 0).
- `node --check` gegenstandslos (kein JS-Touch).
- `python phase5_ui/scripts/ui_budget.py` gegenstandslos (kein `webui/static/`-Touch —
  Baseline V97 von 2026-09-09 reicht für Step 0).
- **Kein rohes `rgba(62,141,243` außerhalb von `:root`** — gegenstandslos in Step 0,
  wird ab Block A zum statischen Test (P8.6-6, §8.2).
- **Größenprüfung** gelaufen: `phase8_6_ui_polish/CLAUDE.md` ist ~13 KB (unter 40-KB-
  Softcap), `SESSIONS_ARCHIVE.md` ist ~0,3 KB (leer mit Card), `scripts/` leer, INDEX
  nach Kompression + neuen Zeilen **unter** 38 KB.
- **Repo-weiter `up:`/`down:`-Link-Scan** gegen alle 60 Frontmatter geprüft: keine
  unauflösbaren Links mehr (vorher 6, jetzt 0). **Repo-weiter `down:`-Listenscan** gegen
  alle Frontmatter geprüft: keine Inline-Format-Listen mehr (vorher 3, jetzt 0).
- **Service-Touch 0** — Production-Dienst PID 355956 nicht angefasst, keine
  Wegwerf-Instanz gestartet (Plan §7.1 Wegwerf-Setup ist Step Gate, nicht Step 0).

**Hard-Rule-8-Doc-Update im selben Commit** (alles in einem Commit, Plan §1.10):
`docs/INDEX.md` (die sieben INDEX-Änderungen oben), `phase8_6_ui_polish/CLAUDE.md`
(dieser Head, neuer Session-Block allein — Rotationsregel P8.6-T eingehalten),
`phase8_6_ui_polish/SESSIONS_ARCHIVE.md` (neu, leer mit 📦-Card),
`phase8_5_picker_release/CLAUDE.md` (Modul-Status unverändert — P8.5 ist closed),
`docs/ROADMAP.md` und `CLAUDE.md` (Wurzel) — siehe separate Commits dieses Z-Closeouts
für die Current-state-/ROADMAP-Updates, die P8.6 als aktive Phase markieren.

**Commit-Message (Plan §1.10, wörtlich):**
`phase 8.6: Step 0 -- Haushalt, sechs kaputte Doku-Links, vier fehlende L1-Cards, INDEX-Kompression`

**Nächster Schritt:** **Step V** — OpenCode-Vision-Plugin-Installation gegen einen echten
Screenshot (V119, Plan §2). Bei Plugin-Repository-Konfig oder Authentifizierungs-Schritten,
die Nikinger-Beteiligung brauchen: **vor** der Installation fragen, nicht im Trial-and-Error-
Verfahren drei Repos durchprobieren.



---

### 2026-09-10 (Migration-Vorbereitung — Proxmox-Aktionsliste + zwei „would be cool"-Zukunfts-Notes; Doku + Skelett, kein Code-Touch)

**Auftrag:** Nikinger kündigt die Proxmox-Migration an („this step is for the
migration") und wünscht „kurz und knackig Aktion → Command-Liste" für die nächste
Session. Außerdem zwei Future-Notes notieren: Tab-Meta-Texte dynamisch
(`sharefyx - {item_title}`) und eine Custom-404-Seite. Mini-PC
`savefyx-VMware-Virtual-Platform` ist **noch** der aktive Host (sharefyx-mcp
PID 355956 seit 2026-09-05 16:10:18 CEST); der Nikinger wird die Services selbst
pause, sobald er so weit ist.

**Was in diesem Commit passiert ist (nur Doku, kein Code-Touch):**

1. **`phase8_6_ui_polish/CLAUDE.md` §Vormerkungen erweitert** um zwei neue
   Spiegelstriche:
   - **„Proxmox-Migration — Aktionsliste (Nikinger, 2026-09-10)"** — 7 Schritte,
     Aktion → Befehl (Pause `sharefyx-mcp` + `tailscaled` via `sudo systemctl
     stop` → VM migrieren via `qm migrate` oder shutdown+move → VM-Resources via
     `qm set --cores 12 --memory 16384 --balloon 0 --cpu host` (+ CPU-Pinning
     `affinity: 0-5,12-15` für i5-14600KF, **kein** Pinning für Ryzen 7 5800X)
     → `apt install -y ollama` + `ollama pull internvl2.5:8b` →
     `phase8_6_ui_polish/scripts/vision_ollama.py` (opencode/M3-Build-Auftrag)
     → V119-Smoke gegen `c4_p8519_01_radiogruppe_im_dialog.png` → `sudo
     systemctl start tailscaled sharefyx-mcp` + `health_gate.sh` 8/8).
   - **„Zukunfts-Notes außerhalb des aktuellen Phasen-Scopes (Nikinger,
     2026-09-10, ‚would be cool')"** — Tab-Meta dynamisch
     (`<title>sharefyx - {item_title}</title>`, UI-only, **[VERIFY] V120**
     Trigger-Events offen) und Custom-404-Seite im App-Stil (Vorsicht:
     `webui/api.py` ist im P8.6-Tabu §0.3, gehört in eine Folge-Phase).
   Bestehende „Vision-Backend: lokales Modell statt API"-Sektion konsistent
   gehalten; „Setup-Befehle"-Sub-Bullet wanderte in die Aktionsliste.

2. **`phase8_6_ui_polish/SESSIONS_ARCHIVE.md` mit rotiertem Vorgänger-Sub-Block
   befüllt** — der „Step 0 — nachträglich: Step V aufgeschoben"-Sub-Block (4.414 B,
   Vorgänger-Commit vom selben Tag) wurde **verbatim** hierher verschoben, weil
   sonst der Phase-Head den 40-KB-Softcap gerissen hätte (P8.6-T-Rotationsregel
   „beim Anlegen eines neuen wandert der bisherige verbatim nach
   SESSIONS_ARCHIVE.md"). Skript `scripts/rotate_session_block.sh` aus P7 passt
   nicht auf das Phase-8.5/8.6-Muster (ein `## Session stopped` + mehrere
   `### date`-Subblöcke — Skript-Exit 2 „Bereits konform"), deshalb **per Hand**.
   Das Archiv ist L3-exempt, neuer Stand 5.685 B.

3. **`## Nächste Session` umgeschrieben** auf Verweis auf die Aktionsliste in
   §Vormerkungen.

4. **`updated:`-Pipe** vorne ergänzt um den neuen Eintrag.

**Selbstprüfung (§0.5):**

- **Tabu-Diff** über die gesamte Phase leer (`git diff --stat -- phase1_storage/storage
  phase4_auth/authserver phase2_mcp/mcpserver phase5_ui/webui/{security,api,serializers,permissions}.py`
  ergibt nichts — kein Code-Touch in dieser Session).
- `pytest -q`/`node --check`/`ui_budget.py` gegenstandslos (kein Code-Touch;
  Baseline V107 = 964 passed, V97 = 5/5 reichen für Doku-only).
- **Größenprüfung** gelaufen: `phase8_6_ui_polish/CLAUDE.md` ist 37.836 B nach
  Vormerkungs-Erweiterung + Rotation des Step-V-Sub-Blocks nach
  `SESSIONS_ARCHIVE.md` (5.685 B, L3-exempt). Head hat 2.124 B Reserve zum
  40-KB-Softcap — ausreichend für die geplanten Co-Edits in
  `docs/concepts/phase8_6_ui_polish_plan.md` §2 und `CLAUDE.md` Current-state.
- **Service-Touch 0** — Production-Dienst PID 355956 nur **gelesen** (`systemctl
  status sharefyx-mcp --no-pager`); keine `sudo systemctl`-Aktion, kein
  `pkill -f`, kein Pfad auf den echten `DATA_ROOT`/Keyring.
- **Vorbereitete Co-Edits** (Hard-Rule-8-Doku-Update im selben Commit):
  `docs/concepts/phase8_6_ui_polish_plan.md` §2 (Verweis-Korrekturnotiz),
  `CLAUDE.md` (Wurzel) Current-state (neuer Eintrag oben + Rotation des
  P8.6-Step-0-Blocks nach `docs/PROJECT_SESSION_LOG.md`), `docs/INDEX.md`
  (Pipe-Update), `ROADMAP.md` (P9-Hinweis).

**Was bewusst NICHT in diesem Commit passiert ist:**

- Kein `phase8_6_ui_polish/scripts/vision_ollama.py` (Schritt 5 der Aktionsliste)
  — Teil der **nächsten** Session, nach der Proxmox-Migration. Ollama + Vision-
  Backend als Voraussetzung; jetzt wäre es Spekulation.
- Keine §11 in `p8x_ui_polish_notes.md` für die Zukunfts-Notes — die Datei ist
  40.882 B (78 B unter Softcap), jede Erweiterung würde über Cap reißen. Der
  Phase-Head-Vormerkungen-Abschnitt ist der etablierte Ort.
- Kein Patch an `webui/api.py` (Custom-404-Seite) — P8.6-Tabu §0.3, bewusst
  draußen.
- Kein Code-Touch in `app.js` (Tab-Meta-Notiz) — explizit „future", nicht P8.6.

**Commit-Message (geplant):**
`phase 8.6: Migrations-Vorbereitung -- Aktionsliste Proxmox + 2 Zukunfts-Notes`

**Nächster Schritt (in der nächsten Session, nach der Proxmox-Migration):**
1. Migration durchgeführt (Nikinger), sharefyx-mcp PID wechselt
2. Ollama-Status in der migrierten VM verifiziert (`ollama list`)
3. MCP-Wrapper-Skript `phase8_6_ui_polish/scripts/vision_ollama.py` schreiben
4. V119-Smoke gegen `c4_p8519_01_radiogruppe_im_dialog.png`
5. Bei Erfolg: V119 ✅, Modul-Status-Update, `docs/UPDATE_LOG.md`-Eintrag,
   V120 für Tab-Meta-Trigger-Events öffnen

### 2026-09-10 (Health-Check nach Proxmox-Migration; services via Auto-Restart-Logik, kein Service-Touch durch opencode/M3)

**Auftrag:** Nikinger meldet „Migration ist komplett durch — willkommen auf dem
leistungsstärkeren Host". Vorschlag: Health-Check, dann diese Session beenden und
pushen. Keine Doku-Erweiterung verlangt — nur die Übergabe sauber machen.

**Was diese Session noch getan hat (rein lesend, kein Eingriff):**

1. **Health-Check** gegen den frisch migrierten Host:
   `bash phase8_5_picker_release/scripts/health_gate.sh` → **8/8 grün** (PID 991
   sharefyx-mcp, PID 926 tailscaled, `v3.0.1`, Release
   `6f19a8fc1f0bcdc2c3bc91fc934a057964647ed4`).
2. **CPU-Identität verifiziert:** `lscpu` zeigt `Intel(R) Core(TM) i5-14600KF`,
   also der primäre Ziel-Host aus der Aktionsliste (Pinning `0-5,12-15` wurde
   im VM-Config gesetzt — wirksam erst beim nächsten qemu-Start, der aktuell
   noch vom alten läuft).
3. **Hostname unverändert:** `savefyx-VMware-Virtual-Platform` — **offene
   Aufgabe** für die nächste Session (entweder `hostnamectl set-hostname` oder
   bewusst lassen).
4. **Restart-Logik entdeckt:** als ich dem Nikinger die `sudo systemctl start`-
   Befehle geben wollte, waren die Dienste schon up (PID 991 vs. vorher 355956).
   Nikinger-Korrektur: „das war dann wohl unsere Restart Logik". Es gibt also
   eine Auto-Restart-Mechanik, die nach der Migration automatisch gegriffen hat.
   **Konsequenz für die Aktionsliste:** Schritt 7 „Restart + Health-Gate" ist
   verkürzbar — die Health-Gate-`expect`-Spalte bleibt (Regression-Schutz),
   der `sudo systemctl start …`-Block entfällt. **Vormerken für nächste
   Session:** Aktionsliste in §Vormerkungen entsprechend korrigieren, einen
   Satz zur Restart-Logik (wo ist sie definiert? `Restart=on-failure` in
   `sharefyx-mcp.service`? Eine `Requires=`-Kette? Eine eigene Timer-Unit?)
   aufnehmen — entscheidet der Nikinger.

**Selbstprüfung (§0.5, Endstand):**

- **Tabu-Diff §0.3** weiterhin leer (kein Code-Touch).
- **Service-Touch 0** über die gesamte Session — die Dienste wurden **gelesen**
  (`systemctl status`, `systemctl is-active`, `pgrep -af`,
  `health_gate.sh`), aber nicht gestartet/gestoppt/restartet. Der PID-Wechsel
  355956 → 991 ist die Auto-Restart-Mechanik, nicht opencode/M3.
- **Kein `pkill -f`**, kein `sudo systemctl`-Aufruf, kein Pfad auf den echten
  `DATA_ROOT`/Keyring in dieser Session.
- **`pytest` 964/964 V107 ✅**, **`ui_budget.py` 5/5 V97 ✅** unverändert.
- **Phase-Head-Größe** 38,7 KB nach Schritt-2/3-Erweiterung (2,3 KB Reserve
  zum 40-KB-Softcap).
- **SESSIONS_ARCHIVE.md** 5,7 KB (rotierter Step-V-deferred-Subblock).

**Was diese Session bewusst NICHT getan hat:**

- Kein `hostnamectl set-hostname` — der Nikinger entscheidet, ob der alte Name
  ersetzt wird (Cluster-Konvention? `savefyx-master`? gar nichts?).
- Kein neues `deploy.sh main` — diese Session hatte **keinen Code-Touch**,
  also keinen Anlass für einen neuen Release. `6f19a8f` / `v3.0.1` bleibt
  aktiv; ein Phase-8.6-Release (`v3.0.2`) kommt mit dem ersten Block-A/B/C/D.
- Kein Ollama-Setup, kein MCP-Wrapper, kein V119-Smoke — das ist **Schritt 4–6**
  der Aktionsliste und gehört in die nächste Session, **nachdem** der Nikinger
  sich für Ollama-Pfad vs. alternative Vision-Lösung entschieden hat (siehe
  „Restart-Logik"-Vormerkung oben).
- Kein Push vor diesem Eintrag — der Commit-Block unten wird der **einzige**
  Commit dieser Session.

**Commit-Message (final, geplant):**
`phase 8.6: Migration durch -- Aktionsliste + 2 Zukunfts-Notes + Health-Check 8/8`

**Nächster Schritt (für die neue Session nach dem Push):**
1. **Hostname-Entscheidung** (Nikinger): `savefyx-VMware-Virtual-Platform` →
   `savefyx-master` o.ä.? Falls ja: `sudo hostnamectl set-hostname <neu>` +
   ggf. `/etc/hosts`-Eintrag.
2. **Ollama + InternVL 2.5 8B** aufsetzen (Aktionsliste Schritt 4, in der
   migrierten VM auf i5-14600KF).
3. **MCP-Wrapper-Skript** `phase8_6_ui_polish/scripts/vision_ollama.py` (~50 Z.
   Python, `requests.post(.../api/generate)`).
4. **V119-Smoke** gegen `c4_p8519_01_radiogruppe_im_dialog.png`.
5. **Restart-Logik in der Aktionsliste korrigieren** (Schritt 7 kürzen,
   Vormerkung „Restart-Logik" eintragen).
6. **Phase-8.6-Block A–D** nach Plan §3–§6.
---

### 2026-09-10 (Open Item #5 — Aktionsliste Schritt 7 verkürzt, Restart-Logik-Vormerkung; nur Doku, kein Code-Touch)

**Auftrag:** Open Item #5 aus dem Session-Handover (2026-09-10, „Health-Check nach
Proxmox-Migration"). Die `sudo systemctl start`-Aufrufe in Schritt 7 der Proxmox-
Aktionsliste sind redundant, weil eine systemd-Restart-Logik greift — der einzige
manuelle Eingriff ist `stop` in Schritt 1 für Lock-Release. Restart-Logik
verifizieren, Schritt 7 kürzen, Vormerkung „Restart-Logik" eintragen. Service-
Datei-Lesen ist erlaubt (§0.5.7: `systemctl status` / `cat service` nur lesend,
kein `sudo systemctl`).

**Was diese Session getan hat (nur Doku, kein Code-Touch):**

1. **Restart-Logik verifiziert** durch Lesen von
   `/etc/systemd/system/sharefyx-mcp.service` und `/usr/lib/systemd/system/tailscaled.service`:
   - `sharefyx-mcp.service:19-20` trägt `Restart=on-failure` + `RestartSec=5` —
     Crash-Recovery im 5-Sekunden-Takt.
   - `sharefyx-mcp.service:6-7` setzt `After=network-online.target tailscaled.service`
     und `Wants=network-online.target` — Boot-Reihenfolge deterministisch.
   - `tailscaled.service` (Vendor, `/usr/lib/systemd/system/`) trägt ebenfalls
     `Restart=on-failure`. Beide Units sind `WantedBy=multi-user.target` (implizit).
   - **Schlussfolgerung:** nach VM-Boot oder VM-Migration-Recovery starten die
     Services **ohne** `systemctl start`-Aufruf. Der einzige manuelle `stop`-
     Call bleibt in Schritt 1 (Lock-Release vor der Migration). Beleg: nach
     der Proxmox-Migration am 2026-09-10 waren beide Dienste sofort up (PID 991
     statt 355956) **ohne** dass opencode/M3 systemctl angerührt hat.

2. **Schritt 7 der Aktionsliste verkürzt:** die `sudo systemctl start tailscaled`
   und `sudo systemctl start sharefyx-mcp`-Zeilen entfernt, dafür eine
   Begründung als Block-Kommentar darunter dokumentiert (Verweis auf die neue
   Vormerkung „Restart-Logik"). Schritt 7 ist jetzt nur noch der Health-Gate-
   Block (`bash .../health_gate.sh --expected-sha=<HEAD>`), 8/8 grün erwartet.

3. **Neue Vormerkung „Restart-Logik (Nikinger-Fund 2026-09-10, ...)"** in §Vormerkungen
   eingefügt — direkt nach der Aktionsliste, vor den Zukunfts-Notes. Vier Spiegelstriche:
   - sharefyx-mcp Restart-Definition mit Zeilen-Ankern,
   - tailscaled Vendor-Unit,
   - `[Install] WantedBy=multi-user.target`-Konsequenz für Boot/Recovery,
   - V103-Notiz für den Deploy (P8.5-V-Frage „sudo-Prompt im Vordergrund" beantwortet
     sich durch diese Mechanik — beim Deploy nach P8.6 gibt es **keinen** `sudo`-Call
     mehr im Agenten-Pfad, der Nikinger-deploy benötigt ggf. eine Folge-Diskussion).

4. **`§Nächste Session` aktualisiert:** „sharefyx-mcp wieder starten + health_gate.sh"
   durch „Health-Gate 8/8 (Restart-Logik übernimmt das Hochfahren)" ersetzt, mit
   Verweis auf die Vormerkung.

5. **P8.6-T-Rotation durchgeführt** (per Hand, weil Skript passt nicht auf das
   Muster): beide vorhergehenden Sub-Blöcke „Migration-Vorbereitung" (4,2 KB) und
   „Health-Check nach Proxmox-Migration" (3,6 KB) **verbatim** nach
   `SESSIONS_ARCHIVE.md` verschoben — Phase-Head trägt jetzt nur diesen einen
   Sub-Block.

6. **`updated:`-Pipe** vorne ergänzt um den neuen Eintrag.

**Selbstprüfung (§0.5):**

- **Tabu-Diff §0.3** leer — kein Code-Touch in dieser Session
  (`git diff --stat -- phase1_storage/storage phase4_auth/authserver
  phase2_mcp/mcpserver phase5_ui/webui/{security,api,serializers,permissions}.py`
  liefert keine Ausgabe).
- `pytest -q` / `node --check` / `ui_budget.py` gegenstandslos (kein Python-,
  kein JS-, kein CSS-Touch — Baseline V107 = 964 passed, V97 = 5/5 reichen
  für Doku-only).
- **Größenprüfung:** `phase8_6_ui_polish/CLAUDE.md` ist nach Rotation **34,6 KB**
  (5,4 KB Reserve zum 40-KB-Softcap) — ausreichend für Block A/B/C/D-Code-
  Touches + zugehörige §0.5-Selbstprüfungen. `SESSIONS_ARCHIVE.md` ist jetzt
  26,9 KB (L3-exempt).
- **Service-Touch 0** — `cat /etc/systemd/system/sharefyx-mcp.service` und
  `systemctl cat tailscaled` sind **lesend**. Production-Dienst sharefyx-mcp
  (PID 991, `ActiveEnterTimestamp=Thu 2026-09-10 19:37:48 CEST`) **nicht**
  angefasst, kein `sudo systemctl`, kein `pkill -f`. Der `pgrep -af phase2_mcp`
  wurde nur gelesen.
- **`ollama list`** meldet `command not found` — bestätigt, dass die
  Proxmox-Migration zwar durch ist, aber Ollama-Setup noch aussteht. Items #2–4
  aus dem Handover bleiben **blockiert**.

**Was diese Session bewusst NICHT getan hat:**

- **Keine Phase-8.6-Block-A/B/C/D-Code-Touches** — das ist Open Item #6 und der
  Hauptumfang, der mit Block A (§3) zwingend zuerst käme (P8.6-U). Diese Session
  hat den Open-Item-#5-Vorbau abgeschlossen; Block A–D bleiben in dieser oder
  der nächsten Session.
- **Kein `hostnamectl set-hostname`** — bleibt beim Nikinger (Tailscale-Name).
- **Kein Ollama-Setup, kein MCP-Wrapper, kein V119-Smoke** — diese sind
  Schritt 4–6 der Aktionsliste und brauchen die Proxmox-Migration (✅ durch)
  **plus** den Nikinger-`apt install ollama`-Schritt.
- **Kein Push ohne Nikinger-Anweisung.**

**Commit-Message (geplant):**
`phase 8.6: Open Item #5 -- Aktionsliste Schritt 7 auf Restart-Logik verkuerzt`

**Nächster Schritt (für dieselbe oder nächste Session):**
1. **Phase-8.6-Block A** nach Plan §3 (A1 Radiogruppe→select, A2 Tokens,
   A3 `--border-soft`-Fix, A4 Konvention v3 + „Vorsicht") + 7 neue statische Tests.
2. Block B (§4), Block C (§5), Block D (§6) — je ein Commit, je Selbstprüfung.
3. Block D ist unabhängig von Block C und darf mit A oder B zusammenrücken.
4. Erst nach A/B/C/D: Gate (§7) mit Wegwerf-Instanz + Nikinger-Sichtprüfung +
   Deploy `v3.0.2` (zweigeteilt: D-a Agent / D-b Nikinger / D-c Health-Gate).


---

### 2026-09-10 (Block A ✅ — Fundament: Radiogruppe→`<select>`, Layer-/Selektions-Tokens, `--border-soft`-Fix, Konvention v3 um „Vorsicht"; Tabu-Diff §0.3 leer, pytest 964→966)

**Auftrag:** Block A nach Plan §3 — A1 Radiogruppe → `<select class="input">` (P8.6-H/I),
A2 Layer-/Selektions-Tokens + fünf rohe `rgba(62,141,243,…)` durch `var(--select-fill)`/
`var(--select-line)` ersetzen (P8.6-C/D/E/F), A3 `--border-soft`-Renderfehler-Fix in
`app.css` (P8.6-§3.3), A4 Konvention v3 um die fünfte Kategorie „Vorsicht" erweitern
(P8.6-G). Reihenfolge: Token-Fundament zuerst (A vor B ist zwingend, P8.6-U). Ziel ist,
dass Block B/C/D die Tokens verbrauchen, ohne selbst welche anzulegen.

**Was in diesem Commit passiert ist:**

1. **`phase5_ui/webui/static/app.html` (A1):** `<fieldset class="link-picker-modes">` mit
   zwei `<input type="radio" name="link-picker-mode">` ersetzt durch
   `<div class="input input--labeled"><label class="input-label-inline" for="link-picker-mode">Einfügen</label><select class="input" id="link-picker-mode"><option value="body" selected>…</option><option value="frontmatter">…</option></select></div>`.
   `localStorage["sfx:linkpicker:mode"]` und sein Wert unveraendert (bestehende Browser
   behalten ihre Wahl).

2. **`phase5_ui/webui/static/js/dialogs.js` (A1):** Modul-Konstante `LINK_PICKER_MODE_NAME`
   entfernt; `_linkPickerMode()` und `_restoreLinkPickerMode()` lesen/schreiben jetzt
   `linkPickerModeEl.value` statt `input[name="…"]:checked`; `initLinkPicker()` haengt
   den `change`-Listener an **ein** Element statt einer `NodeList`-Schleife. Kommentar
   zur P8.6-A1-Motivation am Konstantenblock (war: P8.5-Bezug, jetzt: P8.6-Bezug mit
   Verlauf-Hinweis).

3. **`phase5_ui/webui/static/app.css` (A1/A2/A3):**
   - `:root` (Z. 28-83) um **sechs** neue Tokens erweitert: `--bg-void: #000` (P8.6-D,
     Layer 0, "echtes Schwarz" fuer OLED); `--select-fill` und `--select-fill-quiet`
     (voller und halbtransparenter Selektions-Verlauf, P8.6-C); `--select-line` und
     `--select-line-quiet` (volle und halbtransparente Akzent-Linie, P8.6-C); `--caution:
     var(--danger)` (Alias fuer die fuenfte Konventions-Kategorie, P8.6-F).
   - **Fuenf** rohe `rgba(62,141,243,…)`-Vorkommen ausserhalb `:root` (Z. 403/685/719/
     785/1291) durch Tokens ersetzt; Z. 785 zusaetzlich von `.35` auf `--select-line`s
     `.40` angeglichen (V109, "Im Zweifel angleichen"). `grep "rgba(62,141,243"` trifft
     jetzt nur noch `:root`-Zeilen + den Erklaerungs-Kommentar.
   - `--border-soft` (undefiniert, Step-0-Fund) an Z. 1290/1296 durch `var(--line)`
     ersetzt — der bestehende Haarlinien-Token, den jede andere Panel-Kante verwendet.
   - `--bg-void` an genau **drei** Stellen eingesetzt (P8.6-E): `body` (Boot/Login-
     Hintergrund), `.list__empty, .detail__empty`, `.overview__graph-empty`. **Bewusst
     sparsam** — die uebrigen 60+ Stellen bleiben auf `--bg` (Layer 1).
   - `.link-picker-modes`/`.link-picker-mode*`-CSS-Bloecke (A1, Z. 1334-1361) entfernt.
   - Neue `.input--labeled`/`.input-label-inline`-CSS-Klassen fuer den `<div>`-Traeger
     mit Label-inline + Select-rechts.

4. **`phase8_ui_graph/CLAUDE.md` (A4):** Selection/Choice-Konvention v3 um eine **fuenfte
   Tabellenzeile** „Vorsicht" erweitert (`.action--caution`-Tragerklasse, `color:
   var(--caution)`, **keine** gefuellte rote Flaeche). Ueberschrift „Die vier Kategorien"
   → „Die **fuenf** Kategorien"; Block-Datum-Notiz am Anfang des Abschnitts (P8.6-G:
   die Konvention bleibt in **einem** Dokument, kein zweites Konventions-Doc — `DOC_
   LAYERS_CONVENTION.md` verbietet zwei Kopien derselben Regel). Zusatzsatz zur
   Abgrenzung: *„Vorsicht ist keine Bestaetigungspflicht. Ein Knopf dieser Kategorie
   darf trotzdem einen Bestaetigungsdialog haben (Archivieren hat einen), aber die
   Farbe ersetzt ihn nicht und verlangt ihn nicht."*

5. **`phase5_ui/tests/test_static_routes.py`:** bestehender P8.5-Test
   `test_link_picker_uses_a_radio_group_not_a_select` → umgekehrt + umbenannt zu
   `test_link_picker_uses_a_select_not_a_radio_group` (P8.6-I, Docstring traegt beide
   Richtungen mit Datum). Zwei neue Tests: `test_no_raw_accent_rgba_outside_root`
   (P8.6-C, maschineller Waelchter ueber die fuenf Stellen) und `test_every_css_var_
   reference_is_defined` (P8.6-A3, haette den `--border-soft`-Bug gefunden — und
   findet den naechsten; matcht nicht nur `:root`, weil `@supports`/andere Scopes auch
   definieren duerfen, **und** strippt CSS-Kommentare, damit historische Token-Namen
   wie `--accent-text` in Erklaerungs-Kommentaren nicht als „undefiniert" gezaehlt
   werden).

6. **Hard-Rule-8-Doku-Update im selben Commit:** `phase8_6_ui_polish/CLAUDE.md` Modul-
   Status Tabelle (Zeile 3 `⬜`→`✅`, +2 statische Tests dokumentiert, Abweichung von
   Plan §3.5/§8.2 erklaert), Phase-Head-Session-Sub-Block (Rotation: vorheriger
   Item-#5-Block verbatim nach `SESSIONS_ARCHIVE.md`), Frontmatter `updated:`-Pipe,
   `docs/INDEX.md` Phase-8.6-Zeile aktualisiert, `ROADMAP.md` P8.6-Zeile aktualisiert,
   Wurzel-`CLAUDE.md` Current-state Block ergaenzt.

**Selbstpruefung (§0.5):**

- **Tabu-Diff** ueber die gesamte Phase leer: `git diff --stat -- phase1_storage/
  storage phase4_auth/authserver phase2_mcp/mcpserver phase5_ui/webui/{security,api,
  serializers,permissions}.py` liefert nichts. Erlaubte Pfade beruehrt:
  `phase5_ui/webui/static/{app.html,app.css,js/dialogs.js}`, `phase5_ui/tests/
  test_static_routes.py`, `phase8_ui_graph/CLAUDE.md` (P8.6-G explizit).
- **`pytest -q`** **966 passed in 118 s** (V107-Baseline 964 → +2; Netto-Effekt des
  Test-Renames + 2 neuer Tests).
- **`node --check`** auf `dialogs.js`: OK (kein Syntax-Fehler nach der LINK_PICKER_MODE_
  NAME-Entfernung und dem Init-Block-Umbau).
- **`ui_budget.py`** **5/5 im Zielkorridor** (V97-Baseline gehalten): `items?limit=50`
  roh 26,5 KB, gzip 1,3 KB; `items/{id}` 0,7 KB; `app.js+app.css+Font` gzip **130,4 KB**
  (Baseline 130,1 KB, +0,3 KB durch die neuen Tokens und `.input--labeled`-Bloecke —
  unter dem 250-KB-Ziel); Erstaufruf 138,6 KB (unter 400 KB). `dialogs.js` 13,1 KB
  (Baseline 12,6 KB, +0,5 KB durch die ausfuehrlicheren Kommentare und das Entfernen
  der NodeList-Schleife; **kein** Code-Wachstum in der heissen Pfad-Linie). V108
  „_overview"-Latenz heute **365 ms** (deutlich unter der historischen 438–453 ms-
  Spanne, kein Rauschen — die 863 ms aus V108-Baseline war ein Ausreisser, vermutlich
  Last auf dem alten Mini-PC vor der Migration).
- **Punkt 5 der §0.5-Checkliste** (kein rohes `rgba(62,141,243` ausserhalb `:root`):
  maschinell verifiziert (`python3`-Inline-Skript `:root`-Block entfernt, dann
  `grep "rgba(62,141,243"` → **0 Treffer**).
- **Phase 8 §0.3-Verbotsliste** eingehalten: kein Emoji-Icon, kein Gradient-Branding,
  kein 3er-Card-Grid, keine dekorative Farbe, keine neue Schriftfamilie, kein Element
  dessen Erkennbarkeit allein von Transparenz/Blur abhaengt (manuell bestaetigt).
- **Groessenpruefung:** `phase5_ui/webui/static/app.css` 62,5 KB (vorher 61,4 KB, +1,1 KB
  durch Tokens + drei `--bg-void`-Stellen + `.input--labeled`); `app.html` 31,7 KB;
  `dialogs.js` 45,1 KB; `phase8_ui_graph/CLAUDE.md` 43,2 KB (vorher 42,3 KB, **+850 B**
  statt der geplanten ~600 B — die Konventionstabelle hat mehr zusaetzlichen Text als
  nur eine Tabellenzeile). `phase8_6_ui_polish/CLAUDE.md` aktueller Stand weiter unten.
- **Service-Touch 0** — kein `sudo systemctl`, kein `pkill -f`, kein Pfad auf den
  echten `DATA_ROOT`/Keyring. Production-Dienst sharefyx-mcp (PID 991) **nicht**
  angefasst.
- **`ollama list`** meldet weiterhin `command not found` — Items #2–4 aus dem Handover
  bleiben blockiert (Nikinger-Aktion fuer Schritt 4 der Aktionsliste).

**Was bewusst NICHT in diesem Commit passiert ist:**

- **Kein Block B/C/D-Code-Touch** — A vor B ist zwingend (P8.6-U), und der Token-
  Vorrat ist jetzt vollstaendig. Block B kann mit B1 (Hover-Vereinheitlichung) und
  B4 (`action--caution`-Klasse an Abmelden + Archivieren) anfangen.
- **Keine Schritte 1–3 der Aktionsliste** (Ollama/MCP-Wrapper/V119-Smoke) — bleiben
  Nikinger- bzw. Proxmox-migrationsabhaengig.
- **Keine Tests fuer Block B/C** (die anderen 4 aus Plan §8.2) — bewusste Abweichung
  vom Plan §3.5/§8.2, weil sie in Block A rot waeren. Sie werden in Block B/C/D
  geschrieben, sobald ihr Code existiert. **Dokumentiert in der Modul-Status-Tabelle.**
- **Kein `pkill -f`**, **kein `sudo systemctl`**, **kein Push** ohne Nikinger-
  Anweisung.
- **Keine Custom-404-Seite, kein Tab-Meta-Dynamic-Title** — die zwei „would be cool"-
  Zukunfts-Notes bleiben explizit draussen (P8.6-Tabu, Phase-Head §Vormerkungen).

**Commit-Message (geplant):**
`phase 8.6: Block A -- Radiogruppe zurueck auf select, Layer-/Selektions-Tokens, --border-soft-Fix`

**Naechster Schritt (in dieser oder naechsten Session):**
1. **Block B** nach Plan §4 (B1 Hover-Vereinheitlichung, B2 Ordner/Tags/Buckets,
   B3 Einstellungsmenue-Navigation, B4 Sweep mit `action--caution`-Klasse an Abmelden
   + Archivieren, B5 eine Radius-Aenderung an `.link-picker-results`). Hinzu kommen
   `test_caution_class_only_on_logout_and_archive` als statischer Test (P8.6-B4).
2. Block C nach Plan §5 (Struktur-Umbau: Konto→Einstellungen, Alle Items unter
   Spaces, Map als rechte Spalte, klickbare Spaces, Ordner-Zaehler). Drei weitere
   statische Tests.
3. Block D nach Plan §6 (V102-Dedup, deterministischer Layout-Seed, optional
   `cancelAnimationFrame`-Fix in `runSimulation()` — der „streichen, wenn der Nikinger
   es in der Sichtpruefung anders sieht"-Vorbehalt bleibt).
4. Erst nach A/B/C/D: Gate (§7) mit Wegwerf-Instanz + Nikinger-Sichtpruefung +
   Deploy `v3.0.2`.


---

### 2026-09-10 (Block D ✅ [D1/D2/D4] — V102-Dedup, FNV-1a-Layout-Seed, `cancelAnimationFrame` in `runSimulation()`; Tabu-Diff §0.3 leer, pytest 966 unverändert)

**Auftrag:** Block D nach Plan §6 — V102-Zwillingskante in `graph.js:156` deduplizieren
(P8.6-N), deterministischer Layout-Seed statt `Math.random()` (P8.6-M), und die
**einzige** Scope-Erweiterung des Plans: `cancelAnimationFrame` in `runSimulation()`
(P8.6-§6.4). D3 (`.overview__graph`-Höhe) bleibt 🟡, weil die V112-Gegenprobe den
C3-Layout-Umbau voraussetzt — wird mit Block C nachgezogen.

**Was in diesem Commit passiert ist (nur `phase5_ui/webui/static/js/graph.js`):**

1. **D1 (P8.6-N, V102-Dedup):** `loadGraph()` Z. 156 nimmt `data.edges` jetzt durch eine
   `dedupeEdges()`-Helferfunktion hindurch entgegen. Schlüssel ist das **ungeordnete**
   Knotenpaar `min(src,dst)+"|"+max(src,dst)`; `kind` des ersten Treffers gewinnt.
   `Object.create(null)` als Map (kein Prototyp, bewusste Aussage „Menge, keine
   Struktur"). Dedup bei der Übernahme, **nicht** erst in `drawEdges()` — sonst wäre
   die Doppelkante aus dem Bild aber in der Kanten-Zählung weiterhin (Konsumenten:
   Zeichnen, Nachbarschafts-Hervorhebung `drawLabels()`, Hit-Testing). Was der Dedup
   **nicht** anfasst: `implicitEdges` (Tag-/Ordner-Kanten, andere Semantik) — die
   dürfen neben einer expliziten Kante stehen, **[VERIFY] V118** für die Sichtprüfung
   (Tag-Kante + explizite Kante zwischen denselben Knoten: zwei Linien gewollt?).
2. **D2 (P8.6-M, deterministischer Layout-Seed):** `seedInitialPositions()` Z. 258/259
   `Math.random() - 0.5` durch `seedJitter(n.id, 1)` bzw. `seedJitter(n.id, 2)`
   ersetzt. `seedJitter(id, salt)` ist FNV-1a 32-Bit (`h = 2166136261; h ^= c;
   h = Math.imul(h, 16777619); …`), deterministisch + plattformunabhängig
   (`Math.imul` exakt 32-Bit), unkorreliert für benachbarte IDs — genau das, was ein
   Jitter braucht. Der Ring nach Index (`angle = i / nodes.length * 2π`) war schon
   deterministisch; nur der Jitter war es nicht. Folge: gleiche Daten ⇒ gleiches
   Bild, „die Karte fliegt" (Nikinger-Fund 2026-09-06, Notizen §2.4) ist behoben.
3. **D4 (P8.6-§6.4, `cancelAnimationFrame` in `runSimulation()` — Scope-Erweiterung
   mit Streich-Vorbehalt):** der vorher lokal angelegte `var rafId = null` wurde auf
   Modulebene (`var activeRafId = null`) gehoben. `runSimulation()` ruft jetzt
   `cancelAnimationFrame(activeRafId)` am Anfang, falls vorhanden, und setzt
