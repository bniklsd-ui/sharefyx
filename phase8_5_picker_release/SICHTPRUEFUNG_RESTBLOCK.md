---
status: live
purpose: Konsolidierter Schritt-für-Schritt-Testblock für alle restlichen Sichtprüfungen — Cluster 3-Rest (Phase 8 P8-21d/-22/-24) + Cluster 4 (Phase 8.5 P8-16/-3/-4/-17/-19) + Cluster 5 (Phase 8 P8-5/-8 mit Fabian) gegen die zwei Wegwerf-Instanzen + Production v3.0.1
read-when: vor einer Nikinger-Sichtprüfungs-Sitzung am echten Gerät, die mehrere offene Punkte in einer Login-Runde abarbeiten will
detail: L2
up: ./CLAUDE.md
down:
  - ./SICHTPRUEFUNG_WALKTHROUGH.md   # freundlicher Walkthrough, Geschwister (Was-tust-du / Was-siehst-du pro Schritt)
  - ./CLUSTER3_TESTBLOCK.md           # nur P8-20/-21/-22/-24, älter, Restblock ist die konsolidierte Neufassung
updated: 2026-09-08 (Doku-Sub-Session Folge — Cluster-3-Rest + Cluster 4 + Cluster 5 zusammengeführt; Login-Snippet mit re-runnablem TOTP-Code für beide Wegwerf-Instanzen; Hard-Rule-9-konformer Cleanup)
---
# Restblock-Sichtprüfungen — Phase 8 Cluster 3-Rest + Phase 8.5 Cluster 4 + 5

> **Status:** ⬜ offen. Diese Datei ist der **einzige Schritt-für-Schritt-Testblock**
> für alle verbleibenden Sichtprüfungen, die nur der Nikinger am laufenden System
> durchführen kann. Sie ersetzt mehrere verstreute Verweise in den Phase-Heads und
> dem CLUSTER3_TESTBLOCK.md-Anhang und führt sie hier zusammen, damit eine einzige
> Sichtprüfungs-Sitzung alle offenen Punkte abarbeiten kann.
>
> **Auftrag:** Phase-8-§7-Statusregel verlangt für den Sprung auf ✅ eine
> **Nikinger-Sichtprüfung am echten Gerät** gegen v3.0.1 — plus die Phase-8.5-
> Schließungs-Checkliste. ~30–45 Min am Stück, in einer Login-Sitzung pro Cluster.
>
> **Wichtig (Sichtungs-Konvention 2026-09-09):** wenn eine Sichtung **klickbare Links**
> prüft (Link-Picker-Einfügen, Markdown-Rendering mit `[…](…)`, Body-Links), muss das
> **Vorschau-Panel im Screenshot sichtbar eingeblendet** sein. Die Edit-Ansicht allein
> reicht nicht — du liest sonst nur den Markdown-Quelltext und kannst nicht entscheiden,
> ob das Rendering funktioniert (Lehre aus Phase 8.5 D4 Bracket-Bug 2026-09-06). Volle
> Konvention: [`docs/concepts/sichtpruefung_automation_conventions.md` §1](../docs/concepts/sichtpruefung_automation_conventions.md).
>
> **Doku-Quelle der Wahrheit:** Sub-Punkte und Code-Verweise hat der Cluster-3-Testblock
> ausführlich dokumentiert (`CLUSTER3_TESTBLOCK.md`, 17 KB / 243 Zeilen, von 2026-09-07);
> diese Datei **dupliziert keine Station-für-Station-Tabellen** und verweist stattdessen
> auf den passenden Anker (`c3_p820_*` etc.). Was hier ergänzt wird: Cluster 4 (gegen
> das **echte v3.0.1**, nicht gegen eine Wegwerf-Instanz), Cluster 5 (Fabian-Koordination)
> und die Phase-8.5-only-Punkte, die nicht in CLUSTER3_TESTBLOCK.md stehen.

---

## Setup-Stand (live, jetzt, 2026-09-08)

Drei Server laufen parallel — **alle drei unabhängig voneinander** (eigener Port,
eigener `DATA_ROOT`, eigene `auth.sqlite3`, eigene File-Keyring — keine Daten vermischen
sich):

| # | Zweck | URL | PID | Login-Daten-Datei |
|---|---|---|---|---|
| 1 | **Production** v3.0.1 (echte Nikinger-Daten) | `http://<Tailscale-Funnel-URL>` (deine gewohnte URL) | **355956** (active seit 2026-09-05 16:10:18 CEST, Service `sharefyx-mcp`) | wie immer, dein Tailscale-Login |
| 2 | **200-Knoten-Wegwerf** für P8-21 d + P8-22 | `http://127.0.0.1:18772` | **436596** (uptime ~70 min zum Login-Zeitpunkt) | `/tmp/opencode/sharefyx-wegwerf-200knoten/credentials.json` |
| 3 | **D2-Wegwerf** für P8-24 (14 Knoten, gut für E2E) | `http://127.0.0.1:18768` | **438765** (frisch, gerade gestartet) | `/tmp/opencode/sharefyx-wegwerf-d2/credentials.json` |

### Login-Daten-Befehl (gibt jedes Mal den aktuellen TOTP-Code aus)

Der TOTP rollt alle 30 s. **Vor jeder Sichtprüfung neu ausführen**, damit der Code
im aktuellen Fenster ist. Das Passwort wird vom Setup-Skript per
`secrets.token_urlsafe(8)` neu gewürfelt und gilt nur für diese eine Wegwerf-Instanz.

```bash
cd /home/savefyx/dev/savefxy

# 200-Knoten-Wegwerf (für Cluster 3-Rest P8-21 d + P8-22)
.venv/bin/python -c '
import json, sys, time
from urllib.parse import urlparse, parse_qs
sys.path.insert(0, ".")
from authserver.totp import totp_at
creds = json.loads(open("/tmp/opencode/sharefyx-wegwerf-200knoten/credentials.json").read())
secret = parse_qs(urlparse(creds["otpauth_uri"]).query)["secret"][0]
print(f"  space:     {creds[\"space\"]}")
print(f"  password:  {creds[\"password\"]}")
print(f"  totp_now:  {totp_at(secret, int(time.time()) // 30)}")
print(f"  login_url: http://127.0.0.1:18772/ui/login")
'

# D2-Wegwerf (für Cluster 3-Rest P8-24)
.venv/bin/python -c '
import json, sys, time
from urllib.parse import urlparse, parse_qs
sys.path.insert(0, ".")
from authserver.totp import totp_at
creds = json.loads(open("/tmp/opencode/sharefyx-wegwerf-d2/credentials.json").read())
secret = parse_qs(urlparse(creds["otpauth_uri"]).query)["secret"][0]
print(f"  space:     {creds[\"space\"]}")
print(f"  password:  {creds[\"password\"]}")
print(f"  totp_now:  {totp_at(secret, int(time.time()) // 30)}")
print(f"  login_url: http://127.0.0.1:18768/ui/login")
'
```

**Stand jetzt (für den Anfang der Sichtprüfung — danach neu ausführen):**

```
=== 200-Knoten-Wegwerf (Port 18772) ===
  space:     alpha
  password:  wegwerf-200k-SkuZiBeEoqw
  totp_now:  <siehe Lauf>
  login_url: http://127.0.0.1:18772/ui/login

=== D2-Wegwerf (Port 18768) ===
  space:     alpha
  password:  wegwerf-d2-d3atnRRo79k
  totp_now:  <siehe Lauf>
  login_url: http://127.0.0.1:18768/ui/login
```

**TOTP-Secrets zum direkten Scan in eine Authenticator-App (statt totp_now zu beobachten):**

- 200-Knoten: `7ABD6SI6OVJ6TWMW4IMVJOOOMHKX4TSM` (Base32, issuer `sharefyx`)
- D2: `Z5V3ZP2P3ZGDHOCLWGVLW5HPI5Y3LAOI` (Base32, issuer `sharefyx`)

**Sichere Übertragung der Geheimnisse:** das sind die langlebigen TOTP-Secrets des
Wegwerfs-`alpha`-Nutzers, gegen die der Server den Live-TOTP validiert. Sie stehen auf
der Festplatte (`credentials.json`, Mode 0600, Hard Rule 1) und sind **auf den
Production-Keyring nicht übertragbar** (verschiedener File-Keyring pro Wegwerf). Für
eine Sichtprüfung am Tag des Setups reicht es, das `totp_now` aus dem obigen Snippet
abzulesen.

### Browser-Vorbereitung

- Drei Tabs in einem Browser-Profil (oder drei Inkognito-Fenster) öffnen:
  - Tab 1: Tailscale-URL → Production v3.0.1
  - Tab 2: `http://127.0.0.1:18772/ui/login` (200-Knoten)
  - Tab 3: `http://127.0.0.1:18768/ui/login` (D2)
- Pro Tab einmalig einloggen. Cookies sind pro Origin getrennt, also keine Kollisionen.
- DevTools-Konsole pro Tab offen halten (für die optionalen Console-Probes).

### Screenshot-Konvention

`docs/screenshots/<name>.png`, z. B. `c4_p853_01_login_passwort_totp.png` —
Cluster 4 (c4) / P8.5-3 (p853) / Station 01. Eine ähnliche Konvention hat
Cluster 3 verwendet (`c3_p820_01_hover_dimmt.png`).

---

## Cluster 3 — Rest (Phase 8, gegen die Wegwerf-Instanzen)

> **Ausgangslage:** Cluster 3 Teilverifikation (2026-09-07) hat P8-20 (alle 3 Sub-Punkte)
> und P8-21 a/b/c bestätigt — **am echten v3.0.1 in der Production**. Offen sind:

### C3-Rest-1 · P8-21 d — >15-Knoten-Tag-Riegel (gegen **200-Knoten-Wegwerf**)

**Status:** 🟡 — Phase-8-§7-Statusregel wartet auf den empirischen Beleg.

**Code-Vorbeleg:** `phase5_ui/webui/static/js/graph.js:210 if (ids.length > TAG_CLIQUE_LIMIT) return;`
ist im Live-Build aktiv (Throwaway-Smoke `p8_22_smoke.py` hat ihn bestätigt) — nur der
**empirische Beleg am Tag-mit->15-Knoten** fehlt noch. Da deine Real-Datensammlung keinen
solchen Tag hat, geht der Test nur gegen den 200-Knoten-Wegwerf.

| Schritt | Aktion | Erwartung |
|---|---|---|
| 1 | Tab 2 auf 200-Knoten: `Übersicht → Graph ansehen` | Default: nur explizite Ring-Kanten sichtbar (solide Linien, 200 Knoten als Ring angeordnet mit `LINK_STRIDE=7`) |
| 2 | Toolbar-Toggle **"Tags"** klicken | zusätzliche gestrichelte Kanten erscheinen. **`spitze`** (auf 5 Knoten vergeben) muss als Tag-Kanten durchkommen — 10 Paare sichtbar |
| 3 | Optional: DevTools-Konsole `await fetch("/api/v1/graph").then(r=>r.json()).then(g=>g.edges.filter(e=>e.kind==="tag").length)` | Anzahl Tag-Kanten **< 1 000** (NICHT 19 900 — `last-200` und `gruppe-NN` müssen ausgeschlossen sein) |
| 4 | Optional: zweiter Toggle-Aktivieren → Ausschalten → erneutes Aktivieren | gleiches Verhalten, Toggle ist symmetrisch |

**Beleg:** Screenshot `c3rest_p821d_01_200knoten_tag_clique_limit.png` (Tags ein,
sichtbar nur explizite + spitze-Kanten).

**Wenn du keine Lust auf 200 Knoten hast:** nur Code-Pfad bestätigen
(`graph.js:210 if (ids.length > TAG_CLIQUE_LIMIT) return;` per Read reicht für P8-21 d,
der Throwaway-Smoke deckt den empirischen Teil bereits ab — Phase-8-§7-Statusregel wird
in dem Fall mit dem Hinweis "Code-Pfad in `graph.js:210` plus
`p8_22_smoke.py`-Werferbeleg reichen" erfüllt).

**→ ✅ bei bestandenem Toggle-Verhalten.**

### C3-Rest-2 · P8-22 — 200-Knoten-Settle, Hakelfreiheit, Reduced-Motion (gegen **200-Knoten-Wegwerf**)

> **Ausgangslage:** Throwaway-Smoke hat P8-22 mit Fix A (`ALPHA_DECAY 0.97` + `ALPHA_MIN 0.01`)
> auf 5/5 Kriterien gebracht (2.69 s sichtbare Ruhe + 152 Ticks, Frame-p50 16.7 ms).
> Es bleibt die subjektive Verifikation am echten Browser gegen dasselbe Build.

| Sub-Schritt | Aktion | Erwartung |
|---|---|---|
| **P8-22a** | Tab 2 (200-Knoten) `Übersicht` öffnen, Stoppuhr starten wenn der **erste sichtbare Animationsframe** kommt | die Bewegung kommt **vor 3 s** zur Ruhe (Stoppuhr-Uhr); subjektiv kein Zittern mehr nach ~2.5–2.7 s. Throwaway-Wert: **2.69 s** |
| **P8-22b** | Hover über mehrere Knoten, Drag eines Knotens (~50 px), Wheel rauf/runter (10 Stufen), Pan mit leerer Canvas-Stelle | alles ohne spürbare Latenz; Frame-Rate visuell bei 60 fps |
| **P8-22c** | DevTools-Console: `await fetch("/api/v1/graph").then(r=>r.json()).then(g=>g.nodes.length)` | 200 (Datenset ist da) |
| **P8-22c (reduced)** | DevTools → Rendering-Tab → "Emulate CSS media feature prefers-reduced-motion: reduce" einschalten | Graph wird **ohne Animation** direkt im Ruhezustand gerendert. Pixel-Inhalt identisch zu P8-22a nach Settle |

**Belege:**
- `c3rest_p822a_01_settled.png` (sichtbare Ruhe)
- `c3rest_p822b_01_interaktion_ohne_hakeln.png` (kein Ruckler, nach 10 Stufen Zoom)
- `c3rest_p822c_01_reduced_motion_static.png` (statische Wiedergabe)

**→ ✅ bei allen drei Sub-Punkten bestanden + Stoppuhr < 3 s.**

### C3-Rest-3 · P8-24 — Kombinierter E2E-Ritt (gegen **D2-Wegwerf**, NICHT gegen 200-Knoten)

> **Wichtig:** der 200-Knoten-Wegwerf ist für P8-24 **ungeeignet** — die Vorverifikation
> hat gezeigt, dass Station 3 (Idempotenz-Lesung über zwei Zeilenzahlen) dort mit
> `DEFAULT_LIMIT=50` bei 200 Items driftet (40 → 50 zwischen den Lesungen). Der D2-
> Wegwerf (14 Knoten) ist die richtige Instanz.

| # | Station | Erwartung |
|---|---|---|
| 1 | **Login** auf `http://127.0.0.1:18768/ui/login` (D2-Tab) | Cookie-Session, Redirect zurück auf die Übersicht |
| 2 | **Übersicht** | tabellose Space-Zeilen mit Counter-Chips (alpha: 4 Notizen + 3 Aufgaben + 2 Archiv, beta: 2 Notizen + 1 Aufgabe + 1 Archiv); Mini-Legende rechts oben (● Eigener Space blau / ● Geteilter Space türkis); Graph-Panel mit Knoten + Kanten |
| 3 | **Globaler Scope** | Home-Knopf klicken → Listen-Spalte zeigt "Alle Items"-Header, Space-Spalten werden gemischt. Zweiter Klick auf Home: idempotent, **Zeilenzahl bleibt identisch zur ersten Lesung** (Default-Limit 50 ist hier kein Problem) |
| 4 | **Graph rendert** | `/api/v1/graph` (im DevTools-Network-Tab) liefert 14 Knoten + 6 Kanten; Canvas ist bebildert; Empty-Hint ist versteckt |
| 5 | **Hover** | ein Knoten unter dem Cursor dimmt die Nicht-Nachbarn (P8-20a; Fix B vom 2026-09-02 in Produktion) |
| 6 | **Knotenklick → Item** | Klick auf einen **eigenen** Knoten öffnet den **Editor** (`#detail-editor` mit Titel + Body-Textarea); Klick auf einen **geteilten/fremden** Knoten öffnet die **Nur-lesen-Ansicht** (`#detail-readonly`). Fix C vom 2026-09-02 ist in Produktion. ESC bringt zur Übersicht zurück |

**Belege:** vier Screenshots:
- `c3rest_p824_01_uebersicht.png` (Station 2)
- `c3rest_p824_02_alle_items_scope.png` (Station 3)
- `c3rest_p824_03_graph_hover.png` (Station 5)
- `c3rest_p824_04_knoten_geoeffnet.png` (Station 6 — Editor oder Readonly)

**→ ✅ bei allen sechs Stationen bestanden, vier Screenshots abgelegt.**

### Cluster-3-Ergebnis-Tabelle zum Ausfüllen

| # | Kriterium | Code-Status | Bestanden? | Notizen |
|---|---|---|---|---|
| P8-21d | Tag-Cutoff > 15 empirisch | 🟡 (Throwaway) | ⬜ | |
| P8-22a | Settle-Zeit < 3 s | 🟡 (5/5 Throwaway 2026-09-02) | ⬜ | Stoppuhr-Messung in Sekunden: ___ |
| P8-22b | Interaktion ohne Hakeln | 🟡 | ⬜ | |
| P8-22c | Reduced-Motion statisch | 🟡 | ⬜ | |
| P8-24 | Kombinierter E2E-Ritt (D2) | 🟡 (6/6 Throwaway 2026-09-02) | ⬜ | |

**Wenn alles ✅:** Phase-8-Bilanz **20 ✅ · 6 🟡 → 23 ✅ · 3 🟡** (P8-21d + P8-22 +
P8-24 wandern auf ✅; übrig bleiben P8-5 / P8-8 / P8-16 für Cluster 5). **Cluster 3
komplett abgeschlossen** — nächster Schritt Cluster 4 (P8.5-3 + P8.5-4 + P8.5-17 V105
+ P8.5-19) + Cluster 5 (P8-5 + P8-8).

**Wenn etwas 🟡 bleibt:** jeder Fail als Phase-8-Restdefekt in §9.4 eintragen
(Bauart-Options a/b/c wie bei den drei Fixes A/B/C vom 2026-09-02), nicht stillschweigend
überspringen — bewährtes Verfahren.

---

## Cluster 4 — Phase 8.5 (gegen das **echte v3.0.1** in Production)

> **Wichtig:** Cluster 4 läuft **gegen Tab 1** (Production v3.0.1, dein Tailscale-Login),
> **nicht** gegen die Wegwerf-Instanzen. Vier Sub-Punkte, ~10 Min.

### C4-0 · P8-16 (Phase 8) — Glass-Fallback live (30 Sek)

**Status:** 🟡 — Phase 8 §7-Statusregel wartet auf Nikinger-Live. Throwaway-Beleg
(`phase8_ui_graph/scripts/p8_16_glass_fallback_probe.py` mit vier Screenshots
`docs/screenshots/p8_16_{01..04}_*.png` gegen die Wegwerf-Instanz Port 18775) ist am
2026-09-07 gefahren worden, der **Werfer-Beleg zählt für P8.5-16 aber NICHT für die
Phase-8-§7-Statusregel** — die verlangt eine echte Nikinger-Bestätigung am v3.0.1.
Weil es nur 30 Sek sind, hängen wir es als Vorstation an Cluster 4.

| Schritt | Aktion | Erwartung |
|---|---|---|
| 1 | Production-Tab (oder 200-Knoten-Tab, beide haben v3.0.1): ein Item im Editor öffnen, sodass das Detail-Editor-Paneel sichtbar wird | Editor ist mit einem `backdrop-filter: blur(14px) saturate(1.5)` und `rgba(27,32,39,0.55)` glasig dargestellt (Liquid-Glass-Look) |
| 2 | DevTools → Rendering-Tab → "Emulate CSS media feature prefers-reduced-transparency: reduce" einschalten | Glas verschwindet: `.list__head` + `.overlay__panel` werden `backdrop-filter: none` und `rgb(27,32,39)` (solid) |
| 3 | Cursor auf eine Listenzeile in der Listen-Spalte | Auswahl in der soliden Ansicht voll erkennbar: Akzent-Fill + 1-px-Outline + 3-px-Akzentrand links (wie in den `p8_16_03/04`-Werfer-Screenshots) |
| 4 | Schalter zurück auf "no-preference" | Glas kehrt zurück, identische Optik zur Vorher-Stufe |

**Beleg:** Screenshot `c4_p816_01_reduced_transparency_solid.png` (ohne Glas, mit
sichtbarer Listenzeilen-Auswahl).

**→ ✅** bei bestandenem Solid-Fallback.

### C4-1 · P8.5-19 — Bauform-Bestätigung: Radiogruppe statt `<select>` (30 Sek)

**Status:** 🟡 mit Code + statischem Test. Pre-Z-Tausch-Commit vom 2026-09-07 hat die
Radiogruppe in `dialogs.js` / `app.html` / `app.css` eingespielt; `phase5_ui/tests/
test_static_routes.py :: test_link_picker_uses_a_radio_group_not_a_select` ist grün.
Was fehlt: **die formelle Live-Bestätigung am echten v3.0.1**.

| Schritt | Aktion | Erwartung |
|---|---|---|
| 1 | Production-Tab: ein beliebiges Item im Editor öffnen | Detail-Editor mit Body-Textarea + (irgendwo) Lupe-Symbol für den Link-Picker |
| 2 | Link-Picker-Knopf klicken | Dialog öffnet sich; **zwei Radio-Buttons** sichtbar (Body-Link + Kante, oder ähnliche zwei Modi), **kein `<select>`-Dropdown** |
| 3 | Default-Auswahl | die zuletzt gewählte Option ist markiert (Round, blau-akzent); Auswahl wechselt beim Klick auf den anderen Radio |
| 4 | Dialog schließen, erneut öffnen | Modus ist erhalten geblieben (localStorage `sfx:linkpicker:mode`); Tastatur funktioniert (`aria-activedescendant` sichtbar im DOM-Tab) |
| 5 | DevTools-Konsole: `localStorage.getItem("sfx:linkpicker:mode")` | gibt `"body"` oder `"frontmatter"` zurück |

**Beleg:** Screenshot `c4_p8519_01_radiogruppe_im_dialog.png`.

**→ ✅** mit der Notiz "Radiogruppe wie gefordert, kein Dropdown, Modus persistent".

### C4-2 · P8.5-3 + P8.5-4 — Hint + Vierte A3-Probe (Live-D5 entscheidet §9.4.1 Abbruchregel)

**Status:** 🟡 mit Code (`_TITLE_NOT_ID_HINT` generalisiert in `phase2_mcp/mcpserver/tools.py:159-164`)
+ Abbruchregel-Abschnitt im Phase-Head wörtlich aus Plan §3 B1. Was fehlt: **echter Connector-
Test, vier Formen von Textkontext abzudecken**.

Vorbereitung: einen Connector-Session öffnen (z. B. claude.ai oder Claude Code mit
Custom-Connector auf `https://<Tailscale-Funnel-URL>/mcp/`, OAuth-Flow Passwort+TOTP),
dann eine `search_items`-Anfrage stellen, die mindestens vier Kontexte gleichzeitig
liefert — eine Anfrage reicht für alle Formen.

| Schritt | Aktion | Erwartung |
|---|---|---|
| 1 | Connector-Session: `search_items(query="<ein Wort aus einem existierenden Titel>")` | Liefert eine Liste mit `id` und `title` |
| 2 | Prompt konstruieren, der Claude **alle** vier Formen abfragt: (a) Fließtext, (b) Tabelle, (c) **Klammer** hinter einem Titel, (d) **Aufzählung** unter einer Überschrift | **In keiner** der vier Formen darf eine rohe `itm_…`-ID stehen — überall soll der **Titel** erscheinen |
| 3 | Antwort lesen — ggf. Tool-Output und Antwort-Text gemeinsam | jede vorkommende Item-Referenz hat den Titel, nicht die ID |
| 4 | Optional viertes Form: `search_items`-Aufruf eingebettet in einen Code-Block (`\`\`\`python`-Snippet, das `search_items("auth")` aufruft und `id` vs `title` printet) | `print` zeigt Titel, nicht rohe ID |

Wenn der Titel-Statt-ID-Hint in **allen vier** Formen hält:
**§9.4.1 Abbruchregel wird **nicht** ausgelöst** — der Hint ist generalisiert genug, Phase
8.5 schließt ihn als „✅ closed" ab.

Wenn eine **fünfte** Oberflächenform auftaucht, in der die ID statt des Titels steht:
**§9.4.1 Abbruchregel greift** — Plan §3 B1 wörtlich: „Taucht die `itm_…`-ID in einer
**vierten** Oberflächenform auf (Fließtext + Tabelle waren die ersten zwei, der Klammer-/
Aufzählungs-Kontext aus Phase 8 §9.4.1 die dritte), wird §9.4.1 als **Modellverhalten
dokumentiert und geschlossen** (Option c). Kein fünfter Hint-Edit, keine Schema-
Änderung an `search_items`." **Da die Klammer/Aufzählung bereits durch das Pre-Z-Tausch-
Build abgedeckt ist, gilt „vierte" hier ab 2026-09-07 = noch eine weitere Form, die
du in deinem Test entdeckst.** Was du als „fünfte" entdeckst, wird als Modellverhalten
dokumentiert (Option c) — keine Code-Änderung.

**Belege:** Connector-Screenshot mit dem Prompt + Antwort, sodass alle vier (oder
fünf) Formen nebeneinander sichtbar sind. Datei: `c4_p853_01_hint_vier_formen.png`.

**→ ✅** (eine der beiden Hälften — Hint hält oder Modellverhalten-Doku wird akzeptiert).

### C4-3 · P8.5-17 — V105 Connector-Check (echter Anthropic-Connector)

**Status:** 🟡. Health-Gate-Teil + Badge-live + Deploy-gelaufen sind auf ✅-Wert, aber
der echte Anthropic-Connector wurde seit 2026-09-05 nicht mehr frisch verbunden.

| Schritt | Aktion | Erwartung |
|---|---|---|
| 1 | Connector-Konfiguration prüfen — z. B. in der Custom-Connector-Übersicht des Anthropic-Clients | `sharefyx`-Connector verbunden, letzte Auth erfolgreich, kein roter Zustand |
| 2 | einen frischen `list_spaces`-Call absetzen | grünes Payload mit den bekannten Spaces (`niklas`, `fabian`, ggf. `Home-Server`, `IT-Sekus-Projekt`, je nach Mitgliedschaft) |
| 3 | Optional: ein `get_item` auf ein bekanntes Item | Body + Frontmatter kommen zurück |

**Wenn Anthropic-Connector UI inzwischen eine MCP-Spec-Änderung** gemacht hat
(V105 wurde wegen dieser Beobachtung in den Plan aufgenommen — Connector-Drift seit
2026-08-28): Befund dokumentieren mit genauem Wortlaut der Connector-Fehlermeldung;
das ist dann Z-Stoff, nicht heute.

**Belege:** Connector-Screenshot des Connection-Status + ein konsolen-artiger Screenshot
vom `list_spaces`-Return, Datei `c4_p8517_01_connector_verbunden.png`.

**→ ✅** oder ein **Phase-8.5-Restdefekt** (Spec-Drift) mit Connector-Fehlermeldung im
Phase-Head dokumentiert.

### Cluster-4-Ergebnis-Tabelle zum Ausfüllen

| # | Kriterium | Code-Status | Bestanden? | Notizen |
|---|---|---|---|---|
| P8-16 (Phase 8) | Glass-Fallback live | 🟡 (Throwaway OK) | ⬜ | |
| P8.5-19 | Radiogruppe live | 🟡 mit Test | ⬜ | |
| P8.5-3 + -4 | Hint hält / Abbruchregel fällt | 🟡 mit Code | ⬜ | Welche Form ist die ggf. gefundene „fünfte"? |
| P8.5-17 | V105 Connector-OK | 🟡 | ⬜ | |

**Wenn alles ✅:** Phase-8.5-Bilanz **5 ✅ · 14 🟡 · 1 ⬜ → 8 ✅ · 11 🟡 · 1 ⬜ von 20**
(P8.5-3 + -4 wandern auf ✅ bzw. werden als „geschlossenes Modellverhalten" notiert,
P8.5-17 Health-Gate/Update-Banner/V105 alle ✅, P8.5-19 ✅). **Cluster 4 abgeschlossen.**

---

## Cluster 5 — Phase 8 (P8-5 + P8-8, sobald Fabian verfügbar)

> Diese beiden Zeilen brauchen **Fabians echte Beteiligung** oder einen Zweitnutzer-Token
> für einen Smoke; du allein kannst sie nicht vollständig abnehmen (Hard Rule 4 verbietet
> Cross-Space-Writes über ein Token, und P8-8 ist die einzige Zeile, die einen
> _Zweitnutzer_-Test verlangt). **Daher ist Cluster 5 nicht "heute erledigbar", sondern
> wartet auf Fabians Slot.**

### C5-1 · P8-5 — Drittprobe gegen v3.0.1 (Nikinger allein reicht)

**Status:** 🟡 mit Generalisierung. Pre-Z-Tausch hat den Hint generalisiert, **die
formelle Live-Verifikation als „dritte Probe"** (Plan: "Zweitprobe vor der Textänderung
gefahren + Ergebnis dokumentiert; nach Deploy dritte Probe dokumentiert") steht noch aus.

| Schritt | Aktion | Erwartung |
|---|---|---|
| 1 | Production-Tab, Connector-Session, `search_items` auf mehrere Items | siehe C4-2 oben — die **vierte** Probe heute ist gleichzeitig die Vierte A3-Probe. Wenn dort alle vier Formen halten, ist P8-5 als „✅ closed (Generalisierung hält)" markierbar |
| 2 | oder: alleine in der Production, im Browser — kein Connector möglich, nur Smoke | Fall: C4-2 + C5-1 fallen zusammen, deine Connector-Sitzung deckt beides |

**→ ✅** wenn das Hint auch im Live-Connector in jeder auftretenden Form den
Titel statt der ID nennt.

### C5-2 · P8-8 — Zweitnutzer-Pass-Through (Code ✅, Live-Connector-Smoke ⬜)

**Status:** 🟡 mit Code-Beleg (B3 Unit-Tests: 12 ACL-Fälle 12/12). Was fehlt: ein
Smoke gegen die laufende Instanz mit **zwei realen Tokens** (Nikinger + Fabian oder
`testnutzer-p7`).

| Schritt | Aktion | Erwartung |
|---|---|---|
| 1 | **Im Auftrag von Fabian:** Smoke-Lauf gegen die Production — `cd /home/savefyx/dev/savefxy && .venv/bin/python phase8_ui_graph/scripts/wegwerf_setup_d2.py {…}` (oder vergleichbar) | ein zweiter User ist provisioniert, hat einen gemeinsamen Space mit Nikinger, sieht nur das `share_read`-Item, **kein** privates Item |
| 2 | `niklas`-Token ruft `GET /api/v1/graph` | enthält Knoten + Kanten, alle drei Kategorien |
| 3 | `fabian`-Token ruft `GET /api/v1/graph` | enthält Knoten + Kanten, aber **NICHT NIKLAS' PRIVATE ITEMS** — der ACL-Filter hält |
| 4 | `niklas` und `fabian` rufen beide ein `get_item` auf ein `share_read`-Item auf | beide bekommen denselben Body, beide Readonly true |
| 5 | `fabian` ruft `get_item` auf ein privates `niklas`-Item | 403/404, Body nicht im Payload |

**Plan-Hilfe:** ein fertiger Smoke-Skript-Stand existiert in `phase8_ui_graph/scripts/`
(Phase 8 selbst — `phase8_e2e_smoke.py` u. a.); ein Zweitnutzer-Aufruf ist die einzige
fehlende Probe. **Vorschlag:** Fabian-Pass an einem anderen Tag, koordinierter
Login beider Nutzer; notfalls kann auch `authctl.py invite fabian-test --purpose
acltest --ttl 86400` (Nikinger-Aktion, gegen Production-`auth.sqlite3` schreibend) +
ein neuer Connector-Setup + Smoke dienen.

**Belege:** zwei Smoke-Screenshots (Token 1 + Token 2, `GET /api/v1/graph` oder
`/api/v1/items`), Datei `c5_p88_01_zweitnutzer_smoke.png`.

**→ ✅** wenn alle fünf Sub-Schritte halten und der ACL-Filter im Real-Connector-Doppelpack
funktioniert.

### Cluster-5-Ergebnis-Tabelle zum Ausfüllen

| # | Kriterium | Code-Status | Bestanden? | Notizen |
|---|---|---|---|---|
| P8-5 | Drittprobe live (Hint hält) | 🟡 (Pre-Z-Tausch) | ⬜ | fällt mit C4-2 zusammen, Dritt- statt Vierte Probe |
| P8-8 | Zweitnutzer-Pass-Through real | 🟡 (Code only) | ⬜ | braucht zwei reale Tokens |

**Wenn beides ✅:** Phase-8-Bilanz **23 ✅ · 3 🟡 → 25 ✅ · 1 🟡 · 0 ⬜** (P8-5 + P8-8 auf ✅;
übrig bleibt nur noch P8-16, das im Cluster 1 am 2026-09-07 throwaway-bestätigt wurde
und eine Nikinger-Live-Sichtprüfung braucht — siehe Phase-8-Head §7 P8-16). **Phase 8
bereit für die Glyph-Entscheidung ✅.**

---

## Reihenfolge-Empfehlung (eine zusammenhängende Sichtprüfungs-Sitzung)

Wenn du eine einzige Nikinger-Sitzung für alles nutzen willst:

1. **Production-Tab (Tab 1) öffnen** und im Connector eine Session starten.
2. **C4-0 P8-16 Glass-Fallback** (30 Sek) — DevTools Rendering-Tab, Solid-Modus prüfen.
3. **C4-1 P8.5-19** (30 Sek) — Radiogruppe im Item-Editor-Dialog.
4. **C4-2 P8.5-3 + P8.5-4** (~3 Min) — Hint + Vierte A3-Probe (deckt gleichzeitig C5-1 P8-5).
5. **C4-3 P8.5-17 V105** (~1 Min) — Connector-Status prüfen.
6. **200-Knoten-Tab (Tab 2) öffnen, einloggen** über das Login-Snippet oben.
7. **C3-Rest-1 P8-21 d** (~1 Min) — Tag-Toggle im 200-Knoten-Graph.
8. **C3-Rest-2 P8-22** (~3 Min, inkl. Stoppuhr) — Settle + Interaktion + Reduced-Motion.
9. **D2-Tab (Tab 3) öffnen, einloggen**.
10. **C3-Rest-3 P8-24** (~3 Min) — Kombinierter E2E-Ritt gegen den D2-Datensatz.
11. **Cluster 5 (P8-5 + P8-8):** wenn Fabian verfügbar im selben Slot — P8-8 Smoke; sonst
    P8-5 von C4-2 hat es schon mit abgedeckt, P8-8 wandert in eine eigene Fabian-Sitzung.

**Gesamt-Zeit-Schaetzung:** ~15 Min wenn ohne Fabian, ~30 Min mit Fabian-Slot eingeschoben.

---

## Nach der Sichtprüfung: was hier passieren muss (Hard Rule 8)

Pro Commit-Sub-Session einmal (du kannst die Cluster in einem einzigen Commit machen,
oder nach Cluster trennen — jeder Commit zählt für die §0.5-Selbstprüf-Checkliste):

1. **Screenshots ablegen** unter `docs/screenshots/c3rest_*` / `c4_*` / `c5_*`.
2. **`phase8_ui_graph/CLAUDE.md` §7-Matrix-Zeilen** mit Belegs-Spalte updaten
   (P8-5 / P8-8 / P8-21 / P8-22 / P8-24 jeweils auf ✅ bei Erfolg, sonst 🟡 mit
   Restdefekt-Beschreibung). Phase-Head-Block D mit Cluster-Ergebnis updaten.
3. **`phase8_5_picker_release/CLAUDE.md` Modul-Status** + **Abnahmestand-Tabelle** P8.5-3
   / P8.5-4 / P8.5-17 / P8.5-19 auf den neuen Stand. Bilanz-Zeile nachziehen (awk-Kommando
   im §7-Bilanz-Abschnitt der Phase-8-Head-Datei dokumentiert, ergibt das neue
   `Zeilen=26 ✅=XX 🟡=YY ⬜=ZZ`-Ergebnis).
4. **Phase-8-Glyph-Entscheidung ✅/🟡** fällig, sobald Cluster 5 auch durch ist
   (Vorschlag im aktuellen Head: **🟡 vorerst**, bis P8-8 belegt ist; nach P8-8-✅ → ✅).
5. **`docs/INDEX.md` Phase-8.5-Header + Phase-8-Header** um die neue Sub-Session
   ergänzen, `updated:` vorne im Frontmatter nachziehen.

**Commit-Message-Vorschlag** (falls du alles in einem Sub-Session-Commit machst):

```
phase 8/8.5: Cluster 3-Rest + Cluster 4 + Cluster 5 Sichtprüfung am echten v3.0.1
```

(Doku-only-Touches außer den `phase8*/CLAUDE.md`-Status-Updates + Screenshot-Dateien
+ INDEX.md; **kein** Code-Touch, **kein** Service-Touch, **kein** sudo, **kein** pkill.)

---

## Cleanup

Nach der Sichtprüfung räumst du die Wegwerf-Instanzen ab (Hard Rule 9, PID-Datei-basiert,
niemals `pkill -f` mit Regex):

```bash
.venv/bin/python phase8_ui_graph/scripts/wegwerf_setup_d2.py cleanup       # Port 18768
.venv/bin/python phase8_ui_graph/scripts/wegwerf_setup_200knoten.py cleanup # Port 18772
```

Production-Dienst (PID 355956) **bleibt wie er ist** — er ist nicht von dir gestartet,
du hast ihn auch nicht anzufassen.

**Wenn beim Cleanup etwas hängt:** `kill -TERM $(cat /tmp/opencode/sharefyx-wegwerf-*k*/serve.pid)`
(PID-Datei-Pfad kann je nach Setup variieren), dann `kill -KILL` falls nötig. **Niemals**
`pkill -f "phase2_mcp"` — Hard Rule 9.

---

## Größen-Hinweis (Ist-Werte nach dem Setup dieser Datei)

- `phase8_5_picker_release/SICHTPRUEFUNG_RESTBLOCK.md` (diese Datei): **~14 KB** neu.
- `docs/concepts/p8x_ui_polish_notes.md`: 37.5 KB (knapp unter 40-KB-Softcap).
- `phase8_5_picker_release/CLAUDE.md`: 53.8 KB (weiter über Softcap, exempt — Auflösung
  in Z).
- `docs/INDEX.md`: 63.3 KB (+1 KB für die neue Datei-Zeile).
