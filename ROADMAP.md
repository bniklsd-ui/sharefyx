---
status: live
purpose: Phasenplan des Space-Servers — was in welcher Reihenfolge gebaut wird und warum, plus Status je Phase
read-when: Phasenwechsel, Scope-Frage („gehört X in diese Phase?"), Planung einer neuen Session
detail: L2
up: CLAUDE.md
down:
  - docs/concepts/phase1_storage_plan.md   # ausführungsreifer P1-Plan
  - docs/concepts/phase2_mcp_plan.md       # ausführungsreifer P2-Plan
  - docs/concepts/phase3_edge_plan.md      # ausführungsreifer P3-Plan
  - docs/concepts/phase4_auth_plan.md      # ausführungsreifer P4-Plan
  - docs/concepts/phase5_ui_plan.md        # ausführungsreifer P5-Plan
  - docs/concepts/phase6_shares_plan.md    # ausführungsreifer P6-Plan
  - docs/concepts/phase6_5_tools_images_plan.md   # ausführungsreifer P6.5-Plan
  - docs/concepts/phase7_spaces_admin_plan.md     # ausführungsreifer P7-Plan
  - docs/concepts/phase8_ui_graph_plan.md         # ausführungsreifer P8-Plan
updated: 2026-10-08 (**P9 ✅** — abgeschlossen, live als `v3.1.4`, Gate 9/9; Bilanz 121 ✅ · 12 ⚠️ · 1 ⬜; Handover `PHASE9_CLOSEOUT_HANDOVER.md`) | 2026-10-08 (**P10-Sammelstelle** `docs/concepts/phase10_intake.md` angelegt, P10-Zeile in der Tabelle; Release `v3.1.4` vorbereitet, Deploy beim Nikinger) | 2026-09-30 (**P9 Step G gebaut** — Löschen nach `._trash/`; **Plan-§9.3-Ort unbaubar, gemessen** (Item nach `rebuild_index()` wieder da, `_trash` = Phantom-Space) ⇒ Nikinger-Entscheidung `DATA_ROOT/._trash/<space>/`, null P1-Änderungen; Browser 14/14 gegen eigene TLS-Wegwerf-Instanz) | ältere Einträge: docs/ROADMAP_UPDATES_ARCHIVE.md
---
# ROADMAP — Space-Server

**Build-Reihenfolge ist verbindlich.** Unter Zeit- oder Token-Druck fällt immer die *späteste*
Phase weg, nie eine frühere Regel. Insbesondere: die UI fällt weg, die Auth-Härtung nicht.

Statusglyphen: ⬜ nicht gestartet · 🔄 aktiv · 🟡 code-complete, nicht live-bewiesen · ✅ live-verifiziert

| Phase | Verzeichnis / Paket | Inhalt | Status |
|---|---|---|---|
| **P1** | `phase1_storage/` · `storage` | Datei-Store + Index + Versionierung. Kein Netz. | ✅ |
| **P2** | `phase2_mcp/` · `mcpserver` | MCP-Server, Token-Auth, 6 Tools. Lokal erreichbar. | ✅ |
| **P3** | `phase3_edge/` | Tunnel, systemd, Health, Logging, Ops-Skripte. Öffentlich erreichbar. | ✅ |
| **P4** | `phase4_auth/` · `authserver` | OAuth 2.1 + DCR; ersetzt den Pfad-Token. | ✅ |
| **P5** | `phase5_ui/` · `webui` | REST-API + Web-UI für Menschen. | ✅ |
| **P6** | `phase6_shares/` (kein eigenes Paket) | Freigaben, Ordner, `patch_item`, Update-Log, Bilder. | 🟡 |
| **P6.5** | `phase6_5_tools_images/` (kein eigenes Paket) | Werkzeug-Ergonomie, Abschluss Bilder. | 🟡 |
| **P7** | `phase7_spaces_admin/` (kein eigenes Paket) | Space-Verwaltung, Mehrfachauswahl, Konsolidierung. | ✅ |
| **P8** | `phase8_ui_graph/` (kein eigenes Paket) | UI-Neuanstrich v3, Verknüpfungs-Graph, P7-Erbposten. | ✅ |
| **P8.5** | `phase8_5_picker_release/` (kein eigenes Paket) | Link-Picker-Politur, v3-Vorabritt + Deploy; schließt Phase 8 ab. | ✅ |
| **P8.6** | `phase8_6_ui_polish/` | UI-Politur v3.0.2: Layout-Reorg, Layering, Rail-Umkehr, drei Graph-Fixes. **Abgeschlossen 2026-09-19, live seit 2026-09-18** (Release `20260918T183907.597248Z`, SHA `1ad2665`, `health_gate.sh --expected-version=v3.0.2 --expected-sha=1ad2665` **9/9 grün**, Ausgabe im Commit). **Zwei Pläne und drei Sichtungs-Revisionen**, weil die Nikinger-Sichtprüfung vom 2026-09-12 neun UX-Befunde statt der Freigabe zurückgab: Plan 1 (Step 0 · Step V · A · B · C · D) → **Bruch** → Plan 2 (E messen · F Layering · G Layout-Umbau · **G-R** · H Rail-Umkehr · **H-R** · **H-R-3** · J) → Gate GA1–GA4 → Step Z. **Bilanz 45 ✅ · 5 ⚠️ · 0 ⬜ · 4 ersetzt** von 54 Abnahmezeilen; `pytest` **995**, `ui_budget` 5/5 (144,7 KB von 250 KB), 38 Commits, 930/256 Zeilen Produktcode. **Keine neunte P1-Contract-Öffnung** — der Bereichs-Tabu-Diff `440e462^..HEAD` ist leer bis auf **eine** vorher angekündigte, datierte Ausnahme (**P8.6-AJ**, Block J: `phase4_auth/authserver`, 2 Dateien, `store.py` 2/2 Zeilen). Service-Touch durch einen Agenten **0**. **Drei Entscheidungen, die die Phase geprägt haben:** **P8.6-O2** wurde bewusst ausgelöst, vorgelegt und entschieden (`.shell` → `240px 480px 1fr`, P8.6-X) · **N.9** kehrte C1/N3-Lesart b um (Abmelden bleibt äußerster Knopf) · **N.12** ordnete die datierte Tabu-Ausnahme an, statt den `pytest`-Flake zu dulden — er war ein echter Produktionsfehler (`secrets.token_urlsafe(16)` liefert in **1,569 %** ein führendes `-`, das `argparse` als Optionsflag liest). **Zwei `[VERIFY]` gehen offen an P9:** **V118** (Zwillingskanten-Linienzahl, aus dem Screenshot nicht beantwortbar) und **V136** (Chips vs. `bindFolderDropTarget()`, nie beantwortet). Kanonischer Closeout: `docs/concepts/phase8_6_ui_polish_plan2.md` §9 (Lock P8.6-W; Plan 1 §9 trägt nur eine Zeiger-Zeile) · Einstieg für P9: `docs/concepts/PHASE8_6_CLOSEOUT_HANDOVER.md` · Grafik: `docs/concepts/phase8_6_ui_polish_uebersicht.svg`. | ✅ |
| **P9** | `phase9_hardening/` | **[2026-10-08] Abgeschlossen, live als `v3.1.4`** (Release `20261008T201607.460757Z`, SHA `d04c0ec`, `health_gate.sh --expected-version=v3.1.4 --expected-sha=d04c0ec` **9/9 OK**, Ausgabe im Commit). Härtungsphase in acht Steps plus sieben Blöcken (doing · trace · Buttons · settings · drei Bildsichtungen · feedback), fünf Deploys `v3.1.0`–`v3.1.4`, 126 Commits, `pytest` 995 → **1265**, `ui_budget` 5/5 (173,1 KB). **Bilanz 121 ✅ · 12 ⚠️ · 1 ⬜** von 134 Abnahmezeilen, `[VERIFY]` 40 ✅ · 1 ⚠️ · 3 ⬜. **Zwei angekündigte P1-Öffnungen** (neunte: `doing`/`assignee`; zehnte: `updated_by` + Git-Autor), beide ohne Migration. Service-Touch durch einen Agenten **0**. Kanonischer Closeout: `phase9_hardening/ABNAHME_MATRIX.md` · Einstieg für P10: `docs/concepts/PHASE9_CLOSEOUT_HANDOVER.md` + `docs/concepts/phase10_intake.md` · Grafik: `docs/concepts/phase9_hardening_uebersicht.svg`. *Herleitung, Stand während der Phase:* **Haertungsphase, kein UI-Umbau** — Plan: `docs/concepts/phase9_hardening_plan.md` (2026-09-19, Locks P9-A–P9-T, Abnahme P9-1–P9-58, `[VERIFY]` V145–V164 + die drei geerbten V118/V136/V120). **[2026-09-19, Nikinger-Entscheidung — diese Zeile ersetzt ihre Vorfassung, sie erledigt sie nicht]:** P9 beseitigt die letzten Schwaechen des laufenden Sharefyx, damit die geplanten Features auf einem Fundament stehen; der frueher hier stehende Inhalt (Obsidian-Map-/Graph-Umbau, verbundene AI-Sessions §10.8) ist per **Lock P9-A nach P10 verschoben**. Acht Steps: **0** Doku-Fundament (INDEX-Rotation gebaut, vier gemessene Defekte, `doc_health`-Test) · **A** echte Domain ueber einen **eigenen VPS als TLS-Terminator**, Funnel bleibt Fallback · **B** `tailscaled-watchdog.service` (zyklisch pruefend, der einzige Ansatz, der den Vorfall vom 2026-09-15 sieht) · **C** Vision-Dienst auf der ungenutzten RTX 3060 (eigener LXC auf dem 3060-Host) · **D** die zwei gemeldeten Bugs (ESC/Vollbild, Drop-Ziel Space-Wurzel) · **E** Karten-Reload-Overload · **F** Schema-Fundament `doing` + `assignee` — **neunte P1-Contract-Oeffnung, angekuendigt und datiert** · **G** Loeschen nach `_trash/`, fuer Nutzer unsichtbar, human-only · **H** `fastmcp` 3.4.4 → 3.4.7. **Zwei Planungsbefunde, die Handover-Annahmen widerlegen:** Tailscale Funnel kann **keine** eigene Domain bedienen — der CNAME-Weg aus `PHASE8_6_CLOSEOUT_HANDOVER.md` §4.2 existiert nicht (P9-E), und Cloudflare Tunnel kaeme dafuer nicht in Frage, weil er P3-A umkehren und R4 zurueckholen wuerde (P9-D); `SharePolicy` ist bereits gebaut, das Cross-Space-Rechte-Thema braucht also **kein** fertiges P6 (Plan §0.6). **Arbeitsform:** Step 0, Gate und Step Z in Claude Code (Pixel + Closeout), die Code-Steps D–H in opencode/M3, und die **Infra-Steps A/B/C als Coarbeit in opencode** — M3 leitet Schritt fuer Schritt an, der Nikinger fuehrt aus und liefert jede echte Ausgabe zurueck (**P9-Q**, Plan §0.5.1). Deploy-Ziel `v3.1.0`. **[2026-09-24, Step C Teil 1:]** NVIDIA-Host-Treiber 580.126.09 installiert mit `--no-unified-memory` auf dem Ryzen-7-5800X-Proxmox-Node mit der RTX 3060 LHR (`10de:2504`); `pve-no-subscription`-Repo ergänzt; drei dokumentierte Fehlbarkeiten auf dem Weg (Header-Paket fehlte, Backports führten denselben 550er-Upstream, Nouveau-Konflikt, `nvidia-uvm/uvm_hmm.c` gegen 7.0.2-6-pve-Mai-Patch); UVM-Trade-off akzeptiert und reversibel; LXC-Anlage + Ollama + Cold-Start-Messung (C7) stehen aus. **Step D 🟡** (D2 fertig, D1 ESC/Vollbild zurückgestellt, kein Blocker). **Step F 🟡** (2026-09-30, code-complete, nicht live-bewiesen: `doing` als Task-Status + `assignee` als erstklassiges Feld mit Index-Spalte — die **neunte und bis jetzt letzte P1-Contract-Öffnung**, angekündigt am 2026-09-19 und jetzt abgearbeitet; `INDEX_SCHEMA_VERSION` 3 → 4, **keine Migration**; **V160 vom Nikinger beantwortet**: `assignee` ist ein Space-Name und wird **nicht** gegen die Space-Liste validiert, das wäre eine zweite, nicht angekündigte Öffnung [Lock **P9-U**]; Plan-§8.2-Umfang am Diff korrigiert — neun Stellen sind gemessen **18 Hunks in genau drei Dateien**, dazu drei vom Plan nicht genannte Pflichtstellen; `pytest` 1039 → 1062. **Ein Befund bewusst nicht behoben:** `_BUCKETS` kennt `doing` nicht, beide Fix-Kandidaten sind Darstellungsentscheidungen und stehen in Plan §15 als P10-Posten). **Step B 🟡** (2026-09-30, M3-Anteil ergänzt — **V153 entschieden und einer der beiden Plan-Wege nachweislich unbaubar**: `sudoers` lebt vom setuid-Bit, `NoNewPrivileges=true` lässt der Kernel das nicht zu (`setpriv --no-new-privs -- sudo -n -l` → *"no new privileges" flag is set*), es bleibt polkit. **Aber:** `systemd 255.4` kennt für Start/Stop/Restart nur die **grobe** Aktion `org.freedesktop.systemd1.manage-units` (man `org.freedesktop.systemd1(5)` §Security), ein `<defaults>`-Eintrag kann **nicht** nach Unit filtern — und ob 255 das `unit`-Attribut mitschickt, ist unprivilegiert nicht auslesbar (`pkcheck` → *not registered*). Gebaut: JS-Regel in `phase3_edge/polkit/` mit zusätzlichem `unit`- **und** User-Abgleich (greift ohne das Attribut nicht — gewollter Fehlerfall; **ohne** Abgleich hätte `savefyx` das Management *aller* Units) + **V153-Probe** in `phase9_hardening/step_b/` (Wegwerf-Unit `ExecStart=/bin/true`, fasst `tailscaled` nicht an) + 4 Wächter (9/9, Gegenprobe 4 Verstöße → 6 rote Assertions). **B0 ✅ `AUTORISIERT`** (V153 damit vollständig entschieden) · **B2 erst gescheitert: `203/EXEC`**, weil `local.env` `REPO_ROOT=/opt/sharefyx/current` setzt und das Release vom 18.09. das Skript vom 26.09. nicht enthält — **Nikinger-Entscheidung 2026-10-01: Systempfad** `/usr/local/libexec/sharefyx/` statt `__REPO_ROOT__` (tail-proxy-Muster, elfter Wächter). **B3 🟡 (2026-10-01): der Restart live belegt** (Stufe 1→2→3, polkit-Pfad, Journal) — **der Rate-Limit-Teil hat einen echten Bug gefunden**: `RuntimeDirectoryPreserve=no`, also löschte systemd die Rate-Limit-State-Datei nach jedem Takt und das Limit war nie in Kraft (zwei Restarts 189 s auseinander). **Fix `RuntimeDirectoryPreserve=yes` + 2 Wächter**; der Test dafür war grün, weil sein Mock einen Zustandsspeicher simuliert, den es live nicht gibt. Re-Probe des zweiten Teils steht aus Install + P9-19 bleiben Nikinger-Schritte) **Step H 🟡** (2026-09-30, code-complete: `fastmcp` **exakt** gepinnt `==3.4.7` — **die Plan-Prämisse „installiert ist 3.4.4" war falsch**, gemessen lief der Live-Release bereits auf 3.4.7, weil `deploy.sh:153` pro Release ein frisches venv baut und der Pin ein **Range** war; der stumme Patch-Drift, den P3-D verbieten wollte, hatte also schon stattgefunden. P3-D/P4-R verlangten den exakten Pin seit 2026-08, im Code stand nie einer. **V163 beantwortet** mit drei Codepunkten statt einer Vermutung: CIMD per P4-E abgeschaltet, `token_endpoint_auth_methods_supported: ["none"]`, kein `OAuthProxy`/`JWTVerifier` — der 3.4.7-Security-Fix ist inert, der Bump Hygiene. **P9-55 in der Form abweichend** (`==3.4.7` statt Range, Nikinger-Entscheidung 2026-09-30). **Wächter als Deploy-Riegel**: `test_the_installed_fastmcp_matches_the_pin` läuft im Release-venv mit (`deploy.sh:169`) — ein Drift ist ein roter Deploy; Gegenprobe 4 Verstöße → 7 rote Assertions; `pytest` 1079 → 1084, `ui_budget` 5/5. Transitives `mcp` bleibt ungepinnt (Dev 1.28.1, Live 1.30.0), benannt statt versteckt. **Domain weiter nicht registriert** (NXDOMAIN + RDAP 404) — Gate/Z wartet auf A4–A8) **Step G 🟡** (2026-09-30, code-complete: Löschen nach `._trash/`, **zweistufiges Gate serverseitig geprüft** (Muster `space-remove`), `version` Pflicht, P9-K human-only. **Der Lösch-Ort aus Plan §9.3 war unbaubar** — gemessen kam das gelöschte Item nach `rebuild_index()` wieder und `_trash` wurde ein Phantom-Space; Nikinger-Entscheidung `DATA_ROOT/._trash/<space>/`, wodurch **null P1-Änderungen** nötig sind. 13+5 Tests, Gegenprobe 11 rot, **Browser 14/14** gegen eine eigene TLS-Wegwerf-Instanz — die ein selbstsigniertes Zertifikat brauchte, weil der CSRF-Origin-Vergleich kein Plain-HTTP-Browser passieren kann) | ✅ |
| **P10** | — (noch kein Verzeichnis) | **Alle Baustellen schließen** — Sammelstelle `docs/concepts/phase10_intake.md` (2026-10-08, kein Plan): P10 = Bestandsaufnahme (Register, Messwerte, Entscheidungen), **P10.5** = Ausführung; Themen Performance, 404/Logo/Tab-Titel, Editor ohne Vorschau-Modus, Erbe aus P9. Neue Funktionen erst **P11**. | ⬜ |

**[2026-09-08 Korrektur, Z-Closeout]:** P8 + P8.5 auf ✅ (Statusregel geändert — vom Nikinger
geprüfte Wegwerf-Automatisierung zählt jetzt als live-verifiziert, siehe `phase8_ui_graph/
CLAUDE.md` §Abnahmestand). Die bisherige **P8.X-Platzhalterzeile ist aufgeteilt** in **P8.6**
(kleine Politur, Patch-Bump `v3.0.2`) und **P9** (Graph-Umbau, Minor-Bump `v3.1.0`) — beide
Arbeitsnamen, noch nicht geplant/gelockt. `docs/concepts/p8x_ui_polish_notes.md` bleibt die
Sammel-Quelle für beide, bis eine Planungs-Session die Aufteilung offiziell zieht.

**[2026-09-06 Korrektur, Phase 8.5 D4-Sichtprobe-Folgesession]:** P8.5 fehlte als eigene
Tabellenzeile — beim Anlegen der P8.X-Zeile mitgefunden und nachgetragen, **keine**
inhaltliche Änderung. (P8.X selbst ist mit dem 2026-09-08-Eintrag oben in P8.6/P9
aufgeteilt worden.)

**[2026-08-23 Korrektur, P7 Step 0]:** P6.5 fehlte als eigene Tabellenzeile — beim Ergänzen der
P7-Zeile mitgefunden und nachgetragen, keine inhaltliche Änderung.

**Korrektur (2026-07-25, P2-Planungssession):** OAuth rückt von „ganz am Ende" auf „direkt nach
P3" — der Pfad-Token soll kurz leben, und die UI ist die Phase, die laut Build-Reihenfolge unter
Druck wegfallen darf, OAuth nicht. Begründung: `docs/concepts/phase2_mcp_plan.md` §0.3.

---

## Phase 1 — Storage-Kern
Status **✅** (2026-07-25): 8 Module + 68 Tests, `space_cli.py` als Beweis. Nikinger-Lauf gegen echten `DATA_ROOT` (`/home/savefyx/savefyx-data`) selbst ausgeführt. Details: `phase1_storage/CLAUDE.md` · Plan: `docs/concepts/phase1_storage_plan.md` · Handover: `docs/concepts/PHASE1_CLOSEOUT_HANDOVER.md`.

## Phase 2 — MCP-Server
Status **✅** (2026-07-26): 8 Module + 133 Tests (76 P1 + 57 P2), `mcp_smoke.py` als Beweis, **Adapter-Abnahme 21/21 gegen den echten Custom Connector** durch den Nikinger (`docs/concepts/P2_ADAPTER_ABNAHME_2026-07-26.md`). Details: `phase2_mcp/CLAUDE.md` · Plan: `docs/concepts/phase2_mcp_plan.md` · Handover: `docs/concepts/PHASE2_CLOSEOUT_HANDOVER.md`.

## Phase 3 — Exposure & Betrieb
Status **✅** (2026-07-27–2026-08-02): 13/13 live bestanden, **Tailscale Funnel** (ersetzt den ursprünglich geplanten Cloudflare-Tunnel, Korrektur 2026-07-28; **CGNAT-konform**, Hard Rule 6 eingehalten). Runbooks (`diagnose.sh` etc.) in `phase3_edge/CLAUDE.md`. Details: `phase3_edge/CLAUDE.md` · Plan: `docs/concepts/phase3_edge_plan.md` · Handover: `docs/concepts/PHASE3_CLOSEOUT_HANDOVER.md`.

## Phase 4 — OAuth 2.1
Status **✅** (2026-07-30): 16/16 live bestanden — Schnitt vollzogen, **Pfad-Token tot**, Argon2id + TOTP + DCR + PKCE, opake rotierende Token, zwei unabhängige Nutzer. Sicherheits-Review in `docs/concepts/P4_SECURITY_REVIEW_2026-07-29.md`. Details: `phase4_auth/CLAUDE.md` · Plan: `docs/concepts/phase4_auth_plan.md` · Handover: `docs/concepts/PHASE4_CLOSEOUT_HANDOVER.md`.

## Phase 5 — Web-UI
Status **✅** (2026-08-09): 20/20 live bestanden. Zwei Blöcke (A Sicherheit/Auth-Selbstverwaltung, B REST-API/UI) mit hartem Gate. **`git diff` auf `storage/`, `mcpserver/{tools,permissions,server}.py` blieb über die gesamte Phase leer** (Kriterium 18 — derselbe Seam-Beweis wie in P4, eine API-Fläche höher). Details: `phase5_ui/CLAUDE.md` · Handover: `docs/concepts/PHASE5_CLOSEOUT_HANDOVER.md`.

## Phase 6 — Freigaben, Ordner, Werkzeug-Ergonomie
Status **🟡** (2026-08-23, bewusst nicht ✅): Code-complete und live deployt, aber nur 12/39 Abnahmezeilen live-verifiziert (drei benannte Tasks für nächste Phase in `PHASE6_CLOSEOUT_HANDOVER.md` §4). Drei Blöcke (A Werkzeuge/Betrieb/Update-Banner, B Dateisystem mit SharePolicy, C Bilder nach 6.5 ausgewandert). Details: `phase6_shares/CLAUDE.md` · Handover: `docs/concepts/PHASE6_CLOSEOUT_HANDOVER.md`.

## Phase 6.5 — Werkzeug-Ergonomie und Bilder
Status **🟡** code-complete (13/14 live, P6.5-14 strukturell offen — Nikinger-Bewertung): fünf offene MCP-Werkzeug-Ergonomie-Punkte geschlossen + Abschluss Block C Bilder (`put_asset`/`get_item_asset`/`<untrusted_content>`). Drei neue Punkte nach Phase 6.5 in `PHASE6_5_CLOSEOUT_HANDOVER.md` benannt. Details: `phase6_5_tools_images/CLAUDE.md` · Handover: `docs/concepts/PHASE6_5_CLOSEOUT_HANDOVER.md`.

## Phase 7 — Space-Verwaltung, Mehrfachauswahl, Konsolidierung
Status **✅** (2026-08-28): 22/24 Abnahmezeilen live, 2 ❌ als benannte Defekte an Phase 8 vererbt (P7-24 TOTP-Replay im Batch, P7-4 Claude-nennt-IDs-statt-Titeln) — die Matrix ist **vollständig durchgelaufen**, das unterscheidet P7 von P6/P6.5. Live: `e88a624`, Health-Gate 3/3 grün. Drei Erbposten aus dem Live-Betrieb (P7-24, P7-4, `remove-space`-Auto-Reindex) in Phase 8 gebaut. Details: `phase7_spaces_admin/CLAUDE.md` · Handover: `docs/concepts/PHASE7_CLOSEOUT_HANDOVER.md`.

## Phase 8 — UI-Neuanstrich, Verknüpfungs-Graph, QoL

**Mission, drei Stränge:** (A) die drei benannten P7-Erbposten sind behoben bzw. entschieden —
ein Batch-Verschieben braucht eine einzige Passwort+TOTP-Eingabe (Reauth-Grant statt
TOTP-Replay), `remove-space` hinterlässt nie wieder einen stalen Index, P7-4 bekommt seine
Zweitprobe. (B/D) ein Mensch sieht in einem Graphen, welche Items wie verknüpft sind
(`links:`-Feld + `itm_`-Body-Referenzen + zuschaltbare Tag-/Ordner-Kanten), und die Übersicht
zeigt tablos, was tatsächlich gebraucht wird. (C) die UI verliert ihren AI-Template-Look:
Lucide-Icons statt HTML-Entities, IBM Plex 16px statt Inter 15px, Farblegende
own/shared/foreign, Liquid-Glass-Akzente mit Pflicht-Fallback — Version v3.0.

- **DRIN:** Reauth-Grant (`POST /api/v1/reauth`), `remove-space`-Auto-Reindex, P7-4-Zweitprobe
  + Textschärfung, achte P1-Contract-Öffnung (`linkscan.py`, `item_links`, `GET /api/v1/graph`),
  `#item/`-Navigation, Link-Picker, Icon-Sprite, Plex-Fonts, Farbsemantik, Glass-Akzente,
  tablose Übersicht, handgerollter Canvas-Graph, v3.0.
- **DRAUSSEN:** FastMCP-4/V79, Body-Volltextsuche UI, Rechteverwaltung über MCP, neues
  MCP-Graph-Tool, Löschen von Items, `_trash/`-Räumung, Funnel-Watchdog, Light-Mode,
  Glyph-Entscheidungen P6/P6.5.
- **Erstmals: Claude Code plant, opencode/M3 führt aus — ohne Advisor-Stufe in der Ausführung**
  (Nikinger-Entscheidung N12; Ersatzmechanismen im Plan §0.6).

**Status 🔄 (2026-09-01, Block A + B ✅ live-verifiziert, Gate B→C bestanden):**
Plan `docs/concepts/phase8_ui_graph_plan.md` ausführungsreif, alle zwölf Nikinger-Fragen
N1–N12 in §0.1 gelockt, Entscheidungen P8-A–P8-Q, Abnahmezeilen P8-1–P8-24, `[VERIFY]`
  V81–V92. Closeout wird §9 des Plans (P8-N: ein Dokument pro Phase, kein separates
  Handover). **Block A (A1 Reauth-Grant, A2 `remove-space`-Auto-Reindex, A3
  P7-4-Zweitprobe 🟡 mit benanntem Restdefekt Klammer/Aufzählung) + Block B
  (`storage/linkscan.py`, `item_links`-Tabelle, `GET /api/v1/graph`, `#item/`-
  Navigation, Link-Picker-Dialog) sind seit `main@007b73d` live, Release
  `20260901T103944.634877Z`. Gate B→C (2026-09-01) grün: 958/958 pytest, Charakterisierung
  byte-identisch, Tabu-Diff leer, `_graph_get` manuell 12/12, Playwright gegen
  Wegwerf 18/18. Nächster Schritt: Block C — Design-Fundament v3 (Plan §4).**

---

## Phase 8.5 — Link-Picker-Politur und v3-Release

**Mission:** drei 🟡-Restdefekte aus Phase-8-Closeout §9.4.1–§9.4.3 schließen, einen vollständigen
v3-Vorabritt über den nie ausgelieferten v3-Build fahren und ihn live deployen — diese Phase
**schließt Phase 8 formal mit ab** (N6, Präzedenz P7 Step A8 für Phase 6.5). ~~**Wichtige Korrektur zum Live-Stand:** v3.0 ist **nicht** ausgeliefert …~~
**[2026-09-05 erledigt]:** der Vorabritt lief 26/26, der Deploy ging durch — live seit
`main@6f19a8f`, Release `20260905T140325.378914Z`, Badge `v3.0.1`, Service-PID 355956.
Der Grund für den vollen 13-Stationen-Ritt (N5) bleibt der richtige: Block C/D waren ein
UI-Umbau, den nie ein echter Nutzer gesehen hatte.

- **DRIN:** Picker-Modus-Umschalter „Text-Link / Kante" mit `localStorage`-Persistenz
  (P8.5-§2 A1); Tastaturnavigation über `aria-activedescendant`-Muster (P8.5-§2 A2); Hint
  `_TITLE_NOT_ID_HINT` generalisierend geschärft mit verbindlicher Abbruchregel (P8.5-§3 B1);
  v3-Vorabritt gegen Wegwerf-Instanz mit 13 Stationen (P8.5-§4 C); Deploy `v3.0` → `v3.0.1`
  als **Nikinger-Aktion** (P8.5-§5 D2, Hard Rule 9); Phase-8-Closeout-Nachtrag
  (`phase8_ui_graph_plan.md` §9).
- **DRAUSSEN:** Phase-8-§9.4.6-Funde (Settle-Zeit / Foreign-Farbe / Knotenklick — bereits am
  2026-09-02 geschlossen), Phase-8-§9.4.7 Glyph-Entscheidung ✅/🟡 (Nikinger-Sache nach
  Live-Deploy + Sichtprüfung), geerbtes Phase-6/6.5/7-Ledger (`phase8_ui_graph_plan.md` §9.4.5),
  FastMCP-4/V79 (eigene Mini-Phase, P5-C), `_trash/`-Räumung, Funnel-Watchdog, Mobile/Realtime,
  Light-Mode, ~~Phase-8.5-Übersichtsgrafik (P8.5-S)~~ **[2026-09-09 aufgehoben, Nikinger]:**
  die Grafik existiert — `docs/concepts/phase8_5_picker_release_uebersicht.svg`, Korrekturnotiz
  im Plan §0.2.

**Plan:** `docs/concepts/phase8_5_picker_release_plan.md` (744 Zeilen, geschrieben 2026-09-03
gegen `main@6272cad`). N1–N7 in §0.1 gelockt, Entscheidungen P8.5-A–P8.5-T, Steps 0/A/B/C/D/Z,
Abnahmezeilen P8.5-1–P8.5-20, `[VERIFY]` V95–V105. **Closeout ist §9 des Plans (gefüllt
2026-09-09, kanonisch); Einstieg für die P8.6-Planung ist
`docs/concepts/PHASE8_5_CLOSEOUT_HANDOVER.md` §4.** **Step 0
abgeschlossen** (Haushalt-Funde, Skelett, Größenkorrekturen); **A1 committet** (`499d9be`,
2026-09-04, Picker-Modus-Umschalter + Body-Markdown-Link-Helper + `localStorage`,
Modul-Status 🟡, Tests ⬜, vollständiger Session-Block im Phase-Head); **Drift nachgezogen**
in einem separaten Folge-Commit (Wurzel-Current-state, dieser Absatz, INDEX-Header);
**A2 committet** (Tastaturnavigation + gemeinsamer Pick-Pfad `_pickLinkPickerAt` +
CSS-Block-Entdopplung am Picker; drei neue statische Tests; Modul-Status 🟡; A1-Block
nach `SESSIONS_ARCHIVE.md` rotiert); **B1 committet** (`_TITLE_NOT_ID_HINT` generalisiert
in `mcpserver/tools.py:159-164` — Schlußsatz „Das gilt in jeder Textform" wörtlich aus
Plan §3 B1; zwei Asserts in `test_tools.py`; Abbruchregel-Abschnitt im Phase-Head;
Modul-Status 🟡; A2-Block nach `SESSIONS_ARCHIVE.md` rotiert); Abnahmestand
**3 ✅ · 4 🟡 · 13 ⬜ von 20**. **nächster Schritt:** **Block C** — v3-Vorabritt gegen
eine Wegwerf-Instanz (Plan §4, 13 Stationen Playwright-Smoke gegen den nie ausgelieferten
v3-Build; Wegwerf-Setup mit tmp `DATA_ROOT`/`auth.sqlite3`/eigenem Port, inkl. Portierung
von `scripts/rotate_session_block.sh` aus Phase 7 für `phase8_5_picker_release/`).

**[2026-09-04, Block C committet]** v3-Vorabritt gegen Wegwerf Port 18773 (V98) gefahren:
`phase8_5_picker_release/scripts/wegwerf_setup_v3ritt.py` (Standing-Permission-Muster aus
Phase 8 reproduziert — eigener Port, tmp `DATA_ROOT`/`auth.sqlite3`, File-Keyring; 30
Items über 3 Spaces alpha/beta/gamma inkl. 1 archiviertes, 1 mit item-level `share_read=
["gamma"]` (P6-§35-39-Deploy-Blocker-Fall), 1 mit Bild-Asset via `put_asset()`; 11
explizite Kanten inkl. V102-Zwillings-Kante Buecherliste ↔ Empfehlungen Nikinger);
`scripts/rotate_session_block.sh` aus `scripts/` nach `phase8_5_picker_release/scripts/`
portiert, YAGNI aus A1/A2 geschlossen; `phase8_5_picker_release/scripts/
v3_ritt_playwright_smoke.py` neu (~720 Zeilen, `pyotp`+`async_playwright`). **Ergebnis:
26/26 Stationen grün** (Chromium 13/13 + Firefox 13/13, V101 für beide Browser
bestätigt); drei echte Befunde vorgelegt, **keine Code-Fixes im Tabu-Bereich nötig**:
(1) Smoke-Bug Edge-Keys `src_id`/`dst_id` → `src`/`dst` (gefixt im Smoke, kein
Server-Bug — passt zu `graph.js:325/394` und `webui/api.py:719`), (2) CSRF-Origin-
Mismatch zwischen `http://127.0.0.1:18773` und `SPACE_PUBLIC_BASE_URL=
https://wegwerf-v3ritt.invalid` wegen `_validate_base_url`-Pflicht (Befund für Step Z /
Plan §4.C3, **nicht** in dieser Phase lösbar ohne Server-Code-Touch), (3) Station 12
nur strukturell (`prefers-reduced-motion`-Regel im CSS gefunden, keine echte
Browser-Probe mit umgeschaltetem UA — bleibt, throwaway-verifiziert in Phase 8
`p8_22_smoke.py`); Modus-Selektor `<select>` vs. N3-Vorschau-Radio nicht als Befund
behandelt (P8.5-F-Planer-Substitution, P8.5-19-Sichtprüfung). Abnahmestand jetzt
**3 ✅ · 13 🟡 · 4 ⬜ von 20** (P8.5-5/-6/-7/-8/-10/-11/-13/-15/-16 aus Block C
`⬜`→`🟡`). 16 Screenshots `docs/screenshots/v3ritt_{chromium,firefox}_NN_*.png` neu.
`pytest -q` 962/962 unverändert (kein Python-Touch im Block-C-Setup), Tabu-Diff §0.3
leer, Service-Touch 0 (PID 195922 / ActiveEnterTimestamp 2026-09-02 11:51:57 CEST
nur gelesen; Wegwerf PID 337447 sauber abgebaut via `kill -TERM $(cat serve.pid)`,
Hard Rule 9-konform). **nächster Schritt:** **Block D** — Release-Vorbereitung
(`v3.0` → `v3.0.1`, neuer `## 2026-09-04`-Block in `docs/UPDATE_LOG.md` mit drei
menschenlesbaren Zeilen), D2 Deploy als **Nikinger-Aktion** (Hard Rule 9 + P8.5-Q,
niemals `sudo systemctl restart sharefyx-mcp` durch opencode/M3), D3 Health-Gate,
D4 Sichtprüfung am echten Gerät, D5 Vierte A3-Probe (an der die Abbruchregel §9.4.1
(N2) fällt oder hält).

**[2026-09-05, D1 committet]** Release-Vorbereitung opencode/M3: Badge `v3.0` →
`v3.0.1` in `phase5_ui/webui/static/app.html:20` (P8.5-N7); neuer `## 2026-09-05`-
Block in `docs/UPDATE_LOG.md` mit drei Zeilen (Picker-Modi / Tastatur / Generalisierter
Hint). **Datums-Drift zur Block-C-Spec ausdrücklich dokumentiert:** Block-C-Absatz oben
hatte noch `## 2026-09-04` vorgeschlagen (geschrieben am 2026-09-04, dem Tag von Block C);
heute ist `date +%F`/`date -u +%F` = 2026-09-05, und `deploy.sh` Z. 117–131 verlangt strikt
`today_utc` oder `today_local` als oberstes Datum, sonst Gate-Abbruch — Eintrag deshalb auf
2026-09-05 datiert. Block-C-Block per Hand nach `SESSIONS_ARCHIVE.md` rotiert
(newest-first, vor B1); Skript `scripts/rotate_session_block.sh` passt nicht auf das
Phase-8.5-Muster mit einem `## Session stopped`-Header + mehreren `### date`-Subblöcken
(Skript zählt `## Session stopped`-Header und sieht immer genau einen → Exit 2 „Bereits
konform"). Modul-Status D `⬜` → `🟡` mit D2–D5 als Nikinger-Aktionen vermerkt. `pytest`
nicht gelaufen (kein Python-Touch), Tabu-Diff §0.3 leer (`app.html` und `docs/UPDATE_LOG.md`
nicht tabu), Service-Touch 0 (PID 195922/ActiveEnterTimestamp 2026-09-02 11:51:57 CEST nur
gelesen). **nächster Schritt:** D2 — Deploy als Nikinger-Aktion
(`SHAREFYX_SYSTEMCTL="sudo systemctl" phase5_ui/scripts/deploy.sh main` in interaktiver
Vordergrund-Shell, V103 prüft den `sudo`-Prompt; Hard Rule 9 — niemals `sudo systemctl`
durch opencode/M3), D3 Health-Gate 3/3 + V105, D4 Sichtprüfung am echten Gerät +
P8.5-19-Abnahme des `<select>`-Modus-Selektors, D5 Vierte A3-Probe (entscheidet §9.4.1
Abbruchregel aus N2).

**[2026-09-05, D2 vom Nikinger zwischen D1 und D3 + D3-Prep committet]** D2 ist zwischen
D1 (Commit heute früh) und D3 (diese Session) **still durch den Nikinger gelaufen** —
Entdeckung kam erst beim ersten Probe-Lauf des Health-Gate-Skripts:
`/opt/sharefyx/current` → `20260905T140325.378914Z` → HEAD `6f19a8f` (D1), Service-PID
**355956** (statt der im D1-Block notierten 195922 — D2-Deploy hat den Dienst erwartungsgemäß
neu gestartet), `ExecMainStartTimestamp=2026-09-05 16:10:18 CEST`. Damit ist D3 nicht mehr
Vorbereitung, sondern **Verifikation des bereits deployten v3.0.1**. Neu gebaut:
`phase8_5_picker_release/scripts/health_gate.sh` (134 Zeilen bash, `set -uo pipefail`,
JSON auf stdout / Details auf stderr nach Hard Rule 7), acht Gates — `/health` 200 mit
Retry-Loop (max `--max-wait` Sekunden, Default 30, wie `deploy.sh` Z. 192-200), `/ui/login`
200, `/api/v1/me` 401, `/mcp/` 401 (wie `deploy.sh` Z. 202-217), `.rail__version` aus
`/ui/static/app.html` (**nicht** `/ui/login` — das ist `pages.py`s Auth-Template und enthält
keine Rail; erste Iteration fiel darauf herein, dann gefixt), `/opt/sharefyx/current` →
Release-Verzeichnis mit `.git`, optional `--require-todays-update-log` (oberster
`## YYYY-MM-DD` in `docs/UPDATE_LOG.md` == heute UTC/local, wie `deploy.sh` Z. 127-131),
optional `--expected-sha=<hex>` (Release-SHA matched Short- oder Full-Form per
Prefix-Vergleich). **Lauf-Beleg 2026-09-05 15:19:53Z** mit `--require-todays-update-log
--expected-sha=6f19a8f`: **8/8 grün**, Exit 0, JSON auf stdout
(`{"action":"health_gate","result":"ok","expected_version":"v3.0.1",
"actual_version":"v3.0.1","active_release":"/opt/sharefyx/releases/20260905T140325.378914Z",
"release_sha":"6f19a8fc1f0bcdc2c3bc91fc934a057964647ed4","port":8765}`). Drei Negativproben
separat verifiziert (Port 9999 → Gate 1 rot, `--expected-version=v9.9.9` → Gate 5 rot,
`--expected-sha=0000000` → Gate 8 rot). **P8.5-17 teilweise abgehakt:** Deploy gelaufen ✅,
Health-Gate 8/8 ✅, Badge `v3.0.1` live ✅, Update-Banner-Live-Anzeige ⬜ (braucht Auth,
Nikinger), V105 ⬜ (echter Anthropic-Connector, Nikinger). Modul-Status-Zeile 6 Block D um
D2 ✅ + D3 🟡 erweitert; Abnahmestand-Zeile P8.5-17 Health-Gate-Teil 🟡; Summary
**3 ✅ · 14 🟡 · 3 ⬜ von 20**; D1-Block (111 Zeilen) per Hand nach `SESSIONS_ARCHIVE.md`
rotiert (Skript passt nicht auf das Phase-8.5-Muster — bewährtes Vorgehen aus D1 selbst).
`pytest` nicht gelaufen (kein Python-Touch), `bash -n` OK, shellcheck nicht verfügbar
(übersprungen, keine Konvention im Repo), Tabu-Diff §0.3 leer, Service-Touch 0 (PID 355956
nur gelesen). **nächster Schritt:** **D4 ✅ erledigt 2026-09-06** (Sichtprüfung am echten Gerät durch den Nikinger,
Update-Banner sichtbar, beide Picker-Modi funktional, drei echte Findings dokumentiert: **P8.5-19
Radiogruppe** statt `<select>` — Tausch 5 Z. ausstehend; **P8.5-6 Bracket-Renderer-Bug** in
`markdown.js` — Fix ausstehend; **UX-2-Step-Knotenklick** als neues Feature für p8.X parkiert;
**Phase 8 ✅ + p8.X** als Nikinger-Entscheidung für Z vorgemerkt); **D5 Vierte A3-Probe**
(entscheidet §9.4.1 Abbruchregel aus N2 — Nikinger-Aktion); **V105-Connector-Check** (echter
Anthropic-Connector — Nikinger-Aktion); **optional vor Z** durch opencode/M3: Radiogruppe-Tausch
(P8.5-19) + Bracket-Renderer-Fix (P8.5-6); dann **Z (Closeout)** mit Phase-8-✅-Eintrag +
p8.X-Ankündigung in `phase8_ui_graph_plan.md §9.4.7`.

---

## Phase 8.X — UI-Polish-Folge-Phase (nur Notizen, kein Plan)

> **[2026-09-19, Korrektur]** Diese Sektion beschreibt den Stand **vor** der P9-Planung und
> bleibt als Herkunftsnachweis stehen. Aktuell gilt: P8.6 ist abgeschlossen (`v3.0.2` live),
> **P9 ist als Haertungsphase geplant** (`docs/concepts/phase9_hardening_plan.md`), und die hier
> unter Punkt 3 genannten „verbundenen AI-Sessions" (§10.8) sind per **Lock P9-A nach P10**
> verschoben — zusammen mit dem Karten-Stilumbau (§2.2/§2.5) und §10.1–§10.7. Die vollstaendige
> P10-Liste steht in Plan §15.

**Mission, ein Satz:** Nach dem v3.0.1-Deploy und dem Phase-8.5-Closeout sammelt diese
Folge-Phase die offenen UI-Polish-Wünsche aus der Sichtprobe-Folgesession 2026-09-06
(Nikinger + Fabian) plus die bereits in Phase 8.5 D4 parkierten p8.X-Punkte.

**Status:** ⬜ nicht gestartet, **kein** Plan-Doc, **kein** Locking. Nikinger-Entscheidung
in Phase 8.5 D4 vorgemerkt (`phase8_5_picker_release/CLAUDE.md` und
`phase8_ui_graph_plan.md §9.4.7`).

**Notiz-Sammlung:** `docs/concepts/p8x_ui_polish_notes.md` (L2, **40.9 KB**, 2026-09-06
angelegt, zuletzt 2026-09-09) — **zehn Abschnitte**: §1 Spaces-Layout-Reorg, §2 Obsidian-Map
(fünf Sub-Punkte), §3 Anzahl-Anzeige Ordner, §4 Edit-in-Place-Vision, §5 Layering-Design-System,
§6 „Konto"→„Einstellungen"-Rename, §7 De-AI-ierung-Lauf 2, §8 customizable Tags + Standard-Tag
„blocked", §9 direkter Feedback-Button, **§10 (2026-09-09) neun Nikinger-Punkte aus dem
Phase-8.5-Closeout-Auftrag** — Icon-/Trägerflächen-Radien, Hover als transparentere
Standardauswahl, Ordner-/Tags-Auswahl, klickbare Spaces, Einstellungsmenü, alles Klickbare mit
Farbausnahme für „Abmelden"/„Archivieren", verbundene AI-Sessions, Hochkant-/Handy-UI.
Anhang §A–§E. **Die Zahlen „16 Themen / 25 KB" hier standen bis 2026-09-09 stale.**

**Reihenfolge der nächsten Schritte (Stand 2026-09-09):**

1. ~~**Phase 8.5 Z**~~ **✅ erledigt 2026-09-09** — Phase 8 + 8.5 formal abgeschlossen,
   Closeout in Plan §9, Handover `docs/concepts/PHASE8_5_CLOSEOUT_HANDOVER.md`.
2. **Planungs-Session für P8.6** (Claude Code, weil §5 Layering + §10 design-system-weit
   sind) — beantwortet die §C-Fragen, schätzt Reichweite, spaltet ggf. in Sub-Phasen.
   **Erster Punkt der Phase: OpenCode-Vision-Plugin installieren** (Nikinger-Vorgabe).
   Einstiegsdokument ist das Handover §4, nicht die Phase-Heads.
3. ~~**Plan-Doc + Phase-Verzeichnis** — Name noch nicht gelockt~~ **✅ erledigt 2026-09-09**
   — gelockt als `phase8_6_ui_polish/` + `docs/concepts/phase8_6_ui_polish_plan.md` (P8.6-A).
   **Die Nummern-Frage ist entschieden:** der Nikinger hat bestätigt, dass sein „eher v3.1
   also p8.7" das meint, was die Dokumente **P9 → `v3.1.0`** nennen. **Es gibt kein P8.7.**
   Die verbundenen AI-Sessions (`p8x_ui_polish_notes.md` §10.8) sind damit P9-Inhalt.
   Umbenannt wurde nichts — der Wortlaut bleibt in §10.8 zitiert stehen.
4. **Ausführung P8.6** in opencode/M3 nach Plan §1–§8, Reihenfolge Step 0 ✅ → Step V
   **aufgeschoben** (Migration steht bevor, Plugin-Pfad zurückgestellt) → A → B
   → C/D → Gate → Deploy → Step Z. Der Closeout wird Plan **§9** (P8-N). **Aktuell
   (2026-09-10): Proxmox-Migration + Ollama-Setup + MCP-Wrapper-Skript als nächster
   Nikinger-Schritt** (Aktionsliste 7 Schritte im Phase-Head §Vormerkungen).

**Was NICHT in p8.X gehört** (klare Außenkanten, Notizen-Datei §B): Body-Volltextsuche
in der Web-UI (Q1 gelockt), Rechteverwaltung über MCP-Tools (P6-M), Löschen von Items
(F2), FastMCP-4/V79 (eigene Mini-Phase per P5-C), Funnel-Watchdog, ~~Mobile/~~Realtime,
Light-Mode (P5-X), Glyph-Entscheidungen P6/P6.5. **[2026-09-09, Nikinger]:** die
**Mobile-Hälfte ist aufgehoben** — die Hochkant-/Handy-Ansicht ist ab sofort ein benanntes
Zukunfts-Item (Notizen §10.9), kein P8.6-Auftrag, aber in einer freieren Phasenplanung zu
berücksichtigen. **Realtime bleibt draußen.**

---

## Bewusst nicht auf der Roadmap

- **Semantische Suche / Embeddings.** Verstößt gegen das Bauprinzip. Bei zwei Nutzern und
  einigen hundert Items schlägt Frontmatter-Filterung jede Vektorsuche in Präzision und Kosten.
- ~~**Feingranulare Rechte.** Zwei Personen, gegenseitiges Vertrauen. Cross-Space-Read ist
  standardmäßig an. Der Schutz gegen fremde Inhalte ist Rule 4, nicht ein ACL-Modell.~~
  **Ergänzung 2026-07-25:** P2 baut den Seam dafür (`Permissions.can_read`), damit es später kein
  Umbau wird — die Policy selbst bleibt bewusst `True` für alle, siehe „Zurückgestellt aus P2".
  **[2026-08-09 Korrektur, P6-Planungssession]:** Der Satz war bis heute richtig; mit Phase 6
  wird er widerlegt — Sichtbarkeitsstufen und Item-/Ordner-Freigaben (P6-J/K) sind jetzt Scope.
  Details: `docs/concepts/phase6_shares_plan.md` §0.5.
- **Mehrmandantenfähigkeit.** Wenn ein dritter Nutzer dazukommt, ist das eine Planungssession,
  kein `if`-Zweig. **[2026-08-09 Korrektur, P6-Planungssession]:** Der Satz ist **erfüllt, nicht
  widerlegt** — die Planungssession hat am 2026-08-09 stattgefunden und genau daraus ist Phase 6
  entstanden; ein dritter Nutzer wird darin real angelegt, geprüft und wieder entfernt (P6-W),
  über eine echte Planungssession, keinen stillen `if`-Zweig.
