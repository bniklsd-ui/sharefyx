---
status: live
purpose: Baustellenregister Phase 10 — jede offene Baustelle von Sharefyx genau einmal, mit Herkunft, Befund am Code, Größe, Risiko, nötiger Entscheidung und Ziel (P10.5 / P11 / verworfen / Termin), dazu die Entscheidungsliste für den Nikinger. Die Arbeitsliste, gegen die P10.5 geplant und abgehakt wird.
read-when: vor jeder P10-/P10.5-Planung oder -Entscheidung; wenn jemand fragt „ist X noch offen?"
detail: L2
up: ./CLAUDE.md
down:
  - ../docs/concepts/phase10_inventory_plan.md    # Plan P10: Locks, Steps, Messungen M1–M8, Abnahme, [VERIFY]
  - ../docs/concepts/phase10_intake.md            # Sammelstelle — Herkunft von §2/§3/§5–§7
  - ../docs/concepts/PHASE9_CLOSEOUT_HANDOVER.md  # Herkunft §4.1–§4.10
  - ENTSCHEIDUNGEN_ARCHIVE.md               # 📦 §12 Entscheidungsliste D-1–D-18, verbatim (2026-10-22 gewandert)
  - REGISTER_ARCHIVE.md                    # 📦 die geschlossenen Zeilen, verbatim (2026-10-24 gewandert)
  - UPDATES_ARCHIVE.md                      # 📦 die älteren `updated:`-Fäden dieses Registers, verbatim (2026-10-24 rotiert)
updated: 2026-10-24 (B11.4 ✅ — die Live-Darstellung steht; V211 gemessen: `visibility: hidden`; die **geschlossenen** Zeilen sind ins L3-Archiv gewandert, das Register trägt wieder 10.440 B Luft) | 2026-10-24 (B11.3 ✅ — der Live-Editor steht: ein Text, eine Quelle, kein Moduswechsel) | ältere Einträge: phase10_inventory/UPDATES_ARCHIVE.md
---
# Phase 10 — Baustellenregister

> **Stand:** Entwurf vom 2026-10-16 gegen `main@0a7aaf4` (live `v3.1.4`); **alle Entscheidungen D-1–D-18 am 2026-10-16/18 beantwortet**. **Freigegeben 2026-10-21 (Nikinger) — Tor
> P10-8 offen** (Lock P10-A): Die Spalte „Ziel" ist verbindlich; abgehakt wird nach `phase10_5_finishing_plan.md`.

**Lesart.** **Größe:** S ≤ ein halber Block · M ein Block · L mehrere Blöcke. **Risiko:** S Schreibpfad (Hard Rule 3) · F Dateiformat oder
P1-Contract · R Rechte (Hard Rule 4) · A Auth/Sicherheit · B Betrieb (Handgriff des Nikingers) · — keines. **Entsch.:** `D-n` = steht in der
Entscheidungsliste §12 (seit 2026-10-22 verbatim in `ENTSCHEIDUNGEN_ARCHIVE.md`). **Ziel:** P10.5 · P11 · verworfen · Termin (wartet auf Kalender oder Person, kein Blocker) · P10 (Messung oder Probe in
P10 Step 2) · Wissen (kein Bau, nur festgehalten) · erledigt (mit Beleg). „Empfehlung" heißt: mein Vorschlag, nicht entschieden.

## 1 Betrieb und Infrastruktur (BT)

| ID | Posten | Herkunft | Befund am Code / Stand | Gr. | Risiko | Entsch. | Ziel |
|---|---|---|---|---|---|---|---|
| BT-1 | **Caddy-Quelle zieht nicht nach** — live `dial_timeout 10s`, `lb_try_duration 15s`, `lb_try_interval 1s` | intake §7 (Fleet S9) | → 📦 `REGISTER_ARCHIVE.md` | S | B | D-10 | ✅ 10-5 (B1.2) |
| BT-2 | `sharefyx-tail-proxy` endet bei SIGTERM mit Exit 143 → Unit `failed` | intake §6 (Fleet S6) | → 📦 `REGISTER_ARCHIVE.md` | S | B | D-11 | ✅ 10-6 (B1.3) |
| BT-3 | Tailnet-ACL: Nutzergeräte (MacBook) erreichen VM 200 voll, auch den Relay-Port 8765 | Handover §4.1, intake §5.2 | VPS-Seite ist durch Fleet Block 1 geschlossen (`tag:sharefyx-edge` → nur VM 200:8765). Die Policy lebt in `eurofyx-fleet/tailnet/policy.hujson`, nicht in diesem Repo · **[2026-10-18]** D-9: das MacBook behält den Zugriff auf 8765 — bewusst, zum Debuggen | S | A, B | D-9 | Wissen (akzeptiert) |
| BT-4 | Sechs LAN-Ports auf `0.0.0.0` (7070, 7777, 47984/89/90, 48010 — Sunshine u. a.) | Handover §4.2 | kein Sharefyx-Code, Dienste der VM außerhalb des Repos · **[2026-10-18]** D-12 | S | A | D-12 | an Fleet abgegeben |
| BT-5 | Übergangsfenster der alten Adresse unbefristet (`LEGACY_UNTIL=open`) | Handover §4.7 | `phase4_auth/systemd/sharefyx-mcp.service:20`, `phase5_ui/webui/api.py:397` (`date.max`). Der Firmen-Proxy blockt die Domain, der Funnel bleibt nötig (intake §5.1) · **[2026-10-18]** D-15 | S | B | D-15 | Termin: Arbeitslaptop um den 2026-11-02 erneut testen, dann Enddatum |
| BT-6 | Transitives `mcp` ungepinnt | Handover §4.5, P9 Step H | → 📦 `REGISTER_ARCHIVE.md` | S | B | D-13 | ✅ 10-7 (B1.4) |
| BT-7 | Zwei öffentliche Eingänge (VPS/Caddy und Funnel) — Härtung am Proxy schützt den Funnel nicht | intake §5.1, §6 (Caddy statt nginx) | Rate-Limits leben in der App (`authserver/ratelimit.py`) und gelten auf beiden Wegen. Regel daraus: Härtung gehört in die App, nicht in den Proxy | — | A | nein | Wissen |
| BT-8 | Relay antwortet über die Tailnet-IP mit 400 „Invalid host header" | intake §5.3 | `ALLOWED_HOSTS` (P4-Befund S1) — Messhinweis für Healthchecks, kein Fehler | — | — | nein | Wissen |
| BT-9 | Funnel-`nodeAttrs` hängen am User-Owner — VM 200 taggen nähme den Funnel weg | intake §5.4 | Fleet taggt VM 200 nicht | — | B | nein | Wissen |
| BT-10 | Funnel-Watchdog (geerbtes Ledger, fiel beim Übergang P8.6 → P9 aus der Kette) | P8.5-Handover §4.7 | `phase3_edge/scripts/tailscaled_watchdog.sh:93` prüft nur `Self.Online`; der Fleet-Wächter prüft alle 5 min den **Domain**-Pfad. Den **Funnel**-Pfad prüft von außen niemand · V203 · **[2026-10-18]** D-17 | S | B | D-17 | an Fleet abgegeben (Fleet-Wächter um den Funnel-Pfad erweitern) |
| BT-11 | Vision-Dienst (CT 111): `qwen3-vl:8b` als Prüfwerkzeug gestrichen | Handover §4.6 | Ersatz mit **einer** Frage bekannter Antwort testen, oder CT 111 stilllegen · **[2026-10-18]** D-14: Modell-Recherche in Claude Code, Liste von 4 Modellen, Test gegen 5 sehr verschiedene, gemeine Screenshots (echt oder gebaut); fällt jedes, wird CT 111 stillgelegt · **[2026-10-19, M8 messfertig]** Frage 7 = die echte Falle vom 2026-10-05 (`p9_settings_01`, known aus Code: ein Panel „Einstellungen", Titel **mittig** — P9-AM-CSS; das „linksbündig"-Beispiel der Konventionen war falsch, datiert korrigiert): `qwen3-vl:8b` **6/7** — reproduziert die Falle exakt („Drei Panels. Titel: alpha."), `qwen2.5vl:7b` **6/7** — besteht die echte Falle, fällt synthetisch an `overlapping`; `minicpm-v:8b` **4/7** — erfindet „drei Fenster" mit frei erfundenen Titeln; `llama3.2-vision:11b` **unlauffähig** auf dem Stack (ollama 0.34.4: `unknown model architecture: 'mllama'`, Modell wieder gelöscht, CT 111 trägt wieder nur die zwei Qwen-Modelle). **Empfehlung an D-14: `qwen2.5vl:7b`** — einziger Kandidat, der die echte Falle besteht; dokumentierte Schwäche `overlapping` | S | — | D-14 | P10 (M8), danach Entscheidung |
| BT-12 | Fleet plant ein Backup-Ziel außerhalb von Proxmox | intake §5.5 | `sharefyx-backup.service` bleibt unverändert | — | — | nein | Wissen |
| BT-13 | opencode-Projektmarker im echten Datenverzeichnis (`savefyx-data/.git/opencode`, 40 B, 2026-09-04) | Step 0 (2026-10-16) | **beantwortet 2026-10-16 (Nikinger): ja, versehentlich** — bei der Repo-Auswahl in opencode laggt die Oberfläche, Klicks landen auf dem falschen Eintrag. Kein Datenbefund, nur Metadaten gelesen. Regel: Agenten arbeiten nie im `DATA_ROOT`; vor dem ersten Schreibschritt das Arbeitsverzeichnis prüfen | — | B | nein | Wissen |

## 2 Performance (PF)

| ID | Posten | Herkunft | Befund am Code / Stand | Gr. | Risiko | Entsch. | Ziel |
|---|---|---|---|---|---|---|---|
| PF-1 | `/api/v1/overview` = 6 Durchgänge × sichtbare Spaces (~2,4 s Serverarbeit live, 4 Spaces / 197 Items) | Handover §4.3, P9-15, V151 | → 📦 `REGISTER_ARCHIVE.md` | M | F? | D-3 | ✅ 10-14 (B4) |
| PF-2 | Messanordnung und Zielwerte fehlen | intake §2.1 | P10 Step 2: M1 (Browser des Nikingers, beide Eingänge) und M2 (Wegwerf-Instrument). Die Messlatte 372,9 ms ist falsch (anderes Instrument, P9-15) · **[2026-10-18, M2]** M2-Anteil erledigt: Instrument `phase10_inventory/probes/p10_overview_bench.py` im Repo (4 Spaces × 50 Items, ein Principal sieht alle vier — die Verzerrung des Ein-Space-Bilds ist als Assertion im Instrument und im Wächter verriegelt) + 3 Tests; **Zielwerte (D-3) stehen erst mit M1** · **[2026-10-20, M1]** → `messung/M1_browser.md` | S | — | D-3 | P10 |
| PF-3 | Client-Zwischenspeicher je Space, optimistische Anzeige, Vorabladen | intake §2.1 | ungeprüfte Kandidaten. Bruchstelle Hard Rule 3: kein Cache darf eine alte `version` in einen Write tragen | M | S | D-3 | P10.5, nur wenn M1 es nach PF-1 noch verlangt |
| PF-4 | 20-s-Poll holt `/overview` und `/spaces` getrennt | intake §2.1 | → 📦 `REGISTER_ARCHIVE.md` | S | — | nein | ✅ 10-16 (B4) |
| PF-5 | Listen-Virtualisierung bei großen Spaces | intake §2.1 | live 197 Items, kein Messbefund | M | — | D-3 | verworfen, bis eine Messung es verlangt (Empfehlung) |
| PF-6 | `ui_budget` bleibt Zielgröße | intake §2.1 | → 📦 `REGISTER_ARCHIVE.md` | — | — | nein | ✅ 10-14 (B4) |

## 3 Anbieter-Unabhängigkeit (PA) — Phasenziel, Nikinger 2026-10-16

> **Ziel (Lock P10-C):** jeder standardkonforme MCP-Client kann sich verbinden, nicht nur claude.ai. Blockiert keinen Step, nur den
> Abschluss von P10.5. **Abnahme:** ein Nicht-Claude-Client führt `list_spaces` live über `https://sharefyx.eurofyx.com/mcp` aus.
> Modell-Routing bleibt Client-Seite (frühestens P11), nie im Server. Stand der Spec: **MCP 2026-07-28** ist laut Versionierungsseite
> die **aktuelle** Version („Current"; P8 §0.5 führte sie am 2026-08-28 noch als RC). DCR ist dort *deprecated*, CIMD empfohlen
> (AS **SHOULD**); Reihenfolge der Clients: Vorregistrierung → CIMD → DCR → Nutzer fragen.

| ID | Posten | Herkunft | Befund am Code / Stand | Gr. | Risiko | Entsch. | Ziel |
|---|---|---|---|---|---|---|---|
| PA-1 | Native/Loopback-Clients werden abgelehnt | Code, Spec 2026-07-28 | → 📦 `REGISTER_ARCHIVE.md` | M | A | D-8 | ✅ 10-23 (B6.1) — zweite Regel `http://127.0.0.1:<port>` (P10.5-O) + `application_type` ∈ {fehlend, null, native, web}; **V209**: opencode 1.19.4 (127.0.0.1, Port 19876, `application_type` fehlt) → derselbe DCR-Request jetzt **201** (vorher 400) |
| PA-2 | CSP `form-action` kennt nur `'self'` plus Web-Origins | P4 Modul 8c (Live-Fund 2026-07-30) | → 📦 `REGISTER_ARCHIVE.md` | S | A | nein (folgt aus PA-1) | ✅ 10-24 (B6.2) — CSP `form-action` mit `http://127.0.0.1:*`; **V197 ✅** (Chromium folgt dem Redirect); Gegenlauf ohne den Eintrag: Chromium blockiert lautlos |
| PA-3 | Web-Clients (ChatGPT u. a.) | Code, OpenAI-Doku | Origins sind per `SPACE_OAUTH_ALLOWED_REDIRECT_ORIGINS` konfigurierbar (`config.py:134`), kein Code nötig. ChatGPT-Callback laut OpenAI-Doku `https://chatgpt.com/connector_platform_oauth_redirect` (oder `…/connector/oauth/{callback_id}`), also eine Origin. ChatGPT unterstützt `none` mit PKCE — der AS kennt nur `none` (`metadata.py:34`), das passt. Offen: was ChatGPT per DCR genau anfragt · V196 · **[2026-10-18]** D-8: kein eigenes ChatGPT-Abo, keine Planung auf andere Nutzer | S | A, B | D-8 | nicht geplant |
| PA-4 | CIMD fehlt | Spec 2026-07-28, P4-E | `metadata.py` lässt `client_id_metadata_document_supported` bewusst weg — sonst schaltet claude.ai auf CIMD um und der laufende Connector wechselt den Weg. CIMD heißt außerdem: der Server holt fremde HTTPS-URLs (SSRF-Fläche auf der Heim-VM) · **[2026-10-18]** D-8 („wie vorgeschlagen") | L | A | D-8 | P11 |
| PA-5 | MCP-Protokoll 2026-07-28 / FastMCP 4 (V79) | Ledger, P8 §0.5 | → 📦 `REGISTER_ARCHIVE.md` | L | A | D-17 | ✅ 10-19/20 (B5) |
| PA-6 | Die Projektbeschreibung nennt nur Claude | Wurzel-`CLAUDE.md` §What this project is | → 📦 `REGISTER_ARCHIVE.md` | S | — | nein | ✅ B6.4 (PA-6) — Wurzel-`CLAUDE.md`: „deren **MCP-Clients (Claude und andere)**“ |
| PA-7 | Abnahme-Client und Messung | Lock P10-C | → 📦 `REGISTER_ARCHIVE.md` | S | B | D-8 | P10 (M3 ✅) + P10.5 |

## 4 Karte (KA) — Umbau, Nikinger 2026-10-16

> Gewählt: Stil (p8x §2.2), Layout merken, Interaktion; dazu „etwas gehirnartiger". Erste Runde:
> `docs/concepts/phase10_karte_entwurf_{a,b,c}.svg` (A Landkarte · B Gehirn · C Gehirnkarte) — **entschieden: C** (D-1, 2026-10-16).
> Zweite Runde, drei Stile innerhalb C: `docs/concepts/phase10_karte_c_stil_{1,2,3}.svg` (C1 Flächen · C2 Nervenbahnen · C3 Höhenlinien),
> **gewählt: C2 Nervenbahnen** (D-1b, 2026-10-16). Nicht gewählt: Einklappen (§2.5).

| ID | Posten | Herkunft | Befund am Code / Stand | Gr. | Risiko | Entsch. | Ziel |
|---|---|---|---|---|---|---|---|
| KA-1 | Stil: **Gehirnkarte im Stil C2 Nervenbahnen** (D-1 + D-1b, 2026-10-16) — Spaces als Lappen eines Körpers mit leiser Innenlinie, Furchen als Space-Grenzen, Bahnen stärker geschwungen, Knoten als Zellen mit Membran-Ring und Fortsätzen, ein Fokus aktiviert erste und zweite Nachbarn | p8x §2.2, Nikinger 2026-10-16 | `phase5_ui/webui/static/js/graph.js` (33 KB, handgerollt, `draw()`/`drawEdges()`/`drawNodes()`, keine Bibliothek). Die Lappen entstehen im Browser: Raster, nächster Knoten, Erosion als Furche, Konturverfahren — keine festen Formen, kein Server. Farbe nur mit Bedeutung, keine Transparenz-Abhängigkeit (P8 §0.3 Nr. 4/6). Ruhezustand ohne Fokus: alle Knoten voll deckend; Abdunkeln (0,45) nur bei Hover oder Treffer — Form und Farbe tragen die Bedeutung · **[2026-10-18, M6] Baseline + Lappenkosten gemessen** (`probes/p10_m6_lobe_probe.py` + `p10_m6_lobe.json`, `messung/M6_p8_22_200knoten.txt`): Bestand bei 200 Knoten — sichtbare Ruhe **2694,6 ms** (< 3 s, knapp), 153 Ticks / 2517,6 ms, Frame-Abstand p50 16,7 ms; Interaktion p95 ≤ 0,3 ms. Die naive Lappen-Pipeline (Raster × nächster Knoten, Erosion, Kontur, erste Fassung ohne Optimierung) kostet **0,2–0,6 ms** real (66 sichtbare Cluster) bzw. **0,5–1,9 ms** an der synthetischen 200-Punkt-Obergrenze — **je Frame problemlos im 60-fps-Budget**, einmal nach dem Settle ohnehin trivial. Damit kommt die Größe M–L aus Interaktion/Gestalt, nicht aus der Berechnung. **Nebenbefund:** der reduced-motion-Pfad zeigt **1 rAF-Tick statt 0** (Bild bleibt statisch, Hash über 600 ms unverändert — vermutlich die einmalige initiale Zeichnung über rAF); Beleg im Smoke-Lauf, P10.5-Block 8 nimmt den mit · **[2026-10-24, B8] ✅** C2 gebaut: Lappen (8-px-Raster, Erosion als Furche, geglättete Kontur), Bahnen als Bézier, Zellen mit Membranring und 2–4 Fortsätzen, drei Aktivierungsstufen · Browser-Probe `p105_b8_karte_probe.py` 4/4 mit 3 roten Gegenläufen · **die Sichtung (P10.5-37) steht noch aus** | M–L | — | D-1b | P10.5 |
| KA-2 | Layout über den Reload merken | p8x §2.4 (Rest), Nikinger 2026-10-16 | heute nur innerhalb einer Sitzung (P9 Step E), Seed deterministisch (P8.6-D2). Ablage im Browser (`localStorage`), kein Serverzustand · **[2026-10-24, B8] ✅** `sfx:graph:layout:v1:<eigener Space>`, gemerkte Knoten **gepinnt** (der Plan nennt nur den Saatpunkt — Abweichung im Code begründet) · Browser-Probe: der Zug überlebt das Neuladen | S | — | nein | P10.5 |
| KA-3 | Interaktion: Suche mit Treffer, Filter nach Typ/Status, Titel ohne Zoom | Nikinger 2026-10-16 | der Graph-Knoten trägt neun Felder (`api.py :: _graph_get`, ab `:720`): `id, title, space, own, writable, type, status, folder, tags` — Suche und Filter brauchen **kein** neues Feld. „Kürzlich geändert" (Entwurf B) bräuchte ein zehntes (`updated`) = API-Öffnung · **[2026-10-24, B8] ✅** Suchfeld (Trefferzahl im **eigenen** Feld), Typ-/Statusfilter (blenden Knoten **und** Bahnen aus), Titel ohne Zoom · kein zehntes API-Feld | M | — | D-1 | P10.5 |
| KA-4 | Einklappen mit Abhängigkeiten | p8x §2.5 | am 2026-10-16 nicht gewählt · **[2026-10-18]** D-2 | — | — | D-2 | verworfen |
| KA-5 | `doing` auf Übersicht und Karte hervorheben | P9-Plan §15, P9-P | der fünfte Eimer existiert (Block doing); die prominente Darstellung fehlt | S | — | nein | P10.5, mit KA-1 oder UI |

## 5 Editor (ED)

| ID | Posten | Herkunft | Befund am Code / Stand | Gr. | Risiko | Entsch. | Ziel |
|---|---|---|---|---|---|---|---|
| ED-1 | Schreiben ohne Wechsel zwischen Vorschau und Bearbeiten (Stufe 1: Live-Darstellung über Markdown) | intake §2.3, feedback E3 | `phase5_ui/webui/static/js/editor.js:294–302 setEditorMode()` schaltet `preview`/`edit`, Vorgabe `preview` (`:431`). **Widerspricht dem gelockten P5-U** („Markdown-Textarea + Formatierhilfen, kein WYSIWYG") — Umkehr nur als datierte Nikinger-Entscheidung. Eine Bibliothek muss ohne Build-Schritt laufen (P5-T) und ins `ui_budget` passen · V201 · **[2026-10-18]** D-4: Stufe 1 ja — **P5-U ist damit datiert aufgehoben** · **[2026-10-19, M7]** gemessen (`messung/M7_editor.md`): **CM5 65,6 KB gz, Roundtrip 10/10 verlustfrei, 239,0 KB < 250 KB Korridor ✅**; EasyMDE Roundtrip ok, aber 282,1 KB ❌ (V201); markdown-it redundant zum vorhandenen `js/markdown.js`; Empfehlung CM5 + vorhandene Vorschau (0-Byte-Textarea-Variante als Alternative) — Wahl im Plan P10.5 · **[2026-10-24, B11.1]** der vendorte Editor liegt (CM **5.65.16**, **fünf** Dateien statt drei — gemessen: der UMD-Browser-Zweig löst die `require`s nicht auf; 71.280 B gzip) · **[2026-10-24, B11.3]** der Live-Editor steht: `getBody()`/`setBody()`, **kein Moduswechsel** (der Schalter heißt „Rohtext"), Probe 12/12 grün · **[2026-10-24, B11.4]** die Live-Darstellung steht: CM5-Grundlayout, Token-Stile, gedimmter `.cm-formatting`, Cursorzeile `sfx-active-line` auf dem **Wrap**-Layer — **V211 ✅** (gemessen, nicht behauptet): `visibility: hidden` hält die Cursorposition, `display: none` und `font-size: 0` rücken sie **2 Zeichen** nach vorn · **ein Produktfehler gefunden und behoben**: `cm.setValue()` nimmt die Zeilenklassen mit, und `clearDetail()` setzt `cm` **nicht** auf null — beim Itemwechsel blieb die Cursorzeile unmarkiert · Probe **15/15** grün, Gegenlauf rot · **[2026-10-25, B11.8]** der **Roundtrip** ist gemessen: die **zehn** M7-Fixtures als Items in der Wegwerf-Instanz — **10/10 byte-identisch**, das **Öffnen** macht den Editor **nicht** geändert (`isDirty() === false`, Speicher-Knopf deaktiviert), ein Zeichen tippen und wieder löschen → wieder sauber, und die **Item-Dateien auf der Platte sind byte-identisch** (V201-Rest) | L | S | D-4 | P10.5 |
| ED-2 | To-do-Kästchen im Text, anklickbar | P9-Plan §15, intake §2.3 | `markdown.js` plus Schreibpfad: ein Klick ist ein Write mit `version` (Hard Rule 3) | M | S | D-4 | P10.5, mit ED-1 · **[2026-10-25, B11.5]** gebaut: `cm.markText(…, {replacedWith: <checkbox>, atomic: true})` im Live-Editor (der **Text** bleibt die Quelle — der Klick schreibt `[ ]`/`[x]` in den Puffer); bei **sauberem** Editor folgt sofort `saveItem()` mit der Snapshot-`version`, bei **geaendertem** nur der Puffer; die Lesesicht zeigt das Kaestchen **deaktiviert** (der Sanitizer **erzwingt** `disabled`) · **Wegwerf `probes/p105_b11_todo_probe.py`: 8/8 Zellen grün**, der **Gegenlauf** (die Datei ohne `if (sauber) saveItem();`) bricht **genau die Schreibzelle** |
| ED-3 | Erweiterte Formatierung (Farbe, Ausrichtung, Größe) | intake §2.3 Stufe 2 | in Markdown nicht ausdrückbar → elfte P1-Contract-Öffnung, alle MCP-Clients lesen mit · **[2026-10-18]** D-4: Stufe 2 ja — definierter Markdown-Zusatz, **P1-Öffnung Dateiformat**, alle MCP-Clients lesen mit; eigener Mini-Plan | L | F | D-4 | P10.5 |
| ED-4 | Excel-artige Tabellen | intake §2.3 Stufe 3 | eigener Item-Typ = neue Fähigkeit | L | F | nein | P11 |
| ED-5 | Rohmodus als Notausgang | intake §2.3 | für Items, die der Editor nicht verlustfrei darstellt | S | S | nein | P10.5, mit ED-1 · **[2026-10-25, B11.8]** der Rohmodus ist **gemessen**: im Rohtext trägt der DOM-Text **dieselben Zeichen** wie das Dokument — bei **allen zehn** M7-Fixtures (die Leerzeichen-Darstellung von CM5 — Tab als Tabstopp, erstes Leerzeichen einer Zeile als geschütztes Leerzeichen — ist **Darstellung**, kein verborgenes Zeichen) |

## 6 Darstellung (UI)

| ID | Posten | Herkunft | Befund am Code / Stand | Gr. | Risiko | Entsch. | Ziel |
|---|---|---|---|---|---|---|---|
| UI-1 | Eigene 404-Seite für `/ui/…` | intake §2.2 | unbekannte `/ui/`-Pfade enden im Standard-404 von Starlette; fehlende statische Dateien im Klartext „Nicht gefunden." (`phase5_ui/webui/static_routes.py:86`). API und `/mcp` bleiben bei JSON | S | — | nein | P10.5 |
| UI-2 | Logo, vorläufig, ein Austauschpunkt (SVG + Favicon) | intake §2.2, P9-Plan §15 | die Marke ist heute Text: `app.html:20 .rail__brand`, `pages.py:42 .auth__brand`; kein Favicon · **[2026-10-18]** D-6: Wortmarke, deren „S" mit dem Teilen-Zeichen (drei verbundene Punkte) verschmilzt, Rest leicht poliert, im Sharefyx-Stil; drei Entwürfe in `docs/concepts/phase10_logo_entwuerfe.svg` (A Bahnen-S · B Teilen-S · C Kachel-S) → Tendenz C (Nikinger 2026-10-18); Runde 2 in `phase10_logo_entwuerfe_c.svg` (C1 Zellen · C2 Bahnen · C3 Negativ · C4 Netz); Runde 3 = Mischung aller vier (Kante C1, Form + Fortsätze C2, ausgestanzt C3, Eselsohr C4, Fläche im Auswahl-Stil `--select-fill`/`--select-line`): `phase10_logo_entwuerfe_mix.svg`, Option 1 Schablone · Option 2 Leuchtbahn → **Option 2** (Nikinger 2026-10-18); Runde 4 `phase10_logo_entwuerfe_final.svg`: A Freigestellt · B Überlagert → **D-6 entschieden: B Überlagert** (Nikinger 2026-10-18), ohne den einen Fortsatz der oberen Zelle, der über das Eselsohr hinausragte. Vorlage für den Austauschpunkt in P10.5 | S | — | D-6 | P10.5 |
| UI-3 | Tab-Titel je Ansicht (V120) | intake §2.2 | `app.html:6` statisch `<title>sharefyx</title>`, kein `document.title` im JS · **[2026-10-18]** D-5: deutsch | S | — | D-5 | P10.5 |
| UI-4 | Einheitliche Design-Vorlage, Radien-/Auswahl-Vereinheitlichung | P9-Plan §15, p8x §10.1–§10.7 | Auswahl-Konvention v3 in `phase8_ui_graph/CLAUDE.md`; P9 hat Knöpfe (B17) und Einstellungen vereinheitlicht. Der Rest ist eine Liste, die erst eine Sichtung ergibt · **[2026-10-18]** D-17 ja, nach Sichtung | M | — | D-17 | P10.5, nach Sichtung |
| UI-5 | Kontrast der Vorsicht-Beschriftung 4,38:1 (unter AA 4,5:1) | Handover §4.8, B17 | `.btn.action--caution` mit `color: var(--caution)` · **[2026-10-18]** D-7 ja: hellere Vorsichtfarbe nur für Text | S | — | D-7 | P10.5 (Empfehlung: schließen) |
| UI-6 | Assignee-Picker und -Filter | P9-Plan §15 | der Editor hat Feld und Vorschlagsliste (`editor.js:263ff.`); Filter in der Liste fehlt | S | — | nein | P10.5 |
| UI-7 | Handy-Oberfläche | Nikinger 2026-10-08 | Desktop-Untergrenze 1024 px; eine Handy-App wird ein eigenes Design | — | — | nein | P11 |

## 7 Rechte und Spaces (RE)

| ID | Posten | Herkunft | Befund am Code / Stand | Gr. | Risiko | Entsch. | Ziel |
|---|---|---|---|---|---|---|---|
| RE-1 | Ordner in Team-Spaces anlegen | Block feedback | → 📦 `REGISTER_ARCHIVE.md` | S | R | D-17 | ✅ 10-9 (B2.5 + Nachzug 10-22) |
| RE-2 | MCP `update_item`: Ordner wechseln in Team-Spaces | Block feedback, Handover §6 | → 📦 `REGISTER_ARCHIVE.md` | S | R | nein (Parität) | ✅ 10-9 (B2.5) |
| RE-3 | Space umbenennen (V194) | feedback E2 | → 📦 `REGISTER_ARCHIVE.md` | L | R, F, A | D-17 | ✅ 10-24 (B9.3) |
| RE-4 | Ordner umbenennen (V193) | P9-Plan §15 | → 📦 `REGISTER_ARCHIVE.md` | M | R | D-17 | ✅ 10-24 (B9.2) |
| RE-5 | Verschieben in fremde Spaces | P9-Plan §15 | → 📦 `REGISTER_ARCHIVE.md` | S | R | D-17 | ✅ 10-10 (B2.5) |
| RE-6 | Rechteverwaltung über MCP (P6-M) | Ledger | Hard Rule 4: die Freigabeliste ist „über kein Item-Tool änderbar"; P6-17 belegt, dass kein Tool `share_*` setzt · **[2026-10-18]** nicht gewählt | M | R, A | D-17 | verworfen |
| RE-7 | `created_by` sichtbar machen (elfte Öffnung) | Handover §4.10, P9-BQ | → 📦 `REGISTER_ARCHIVE.md` | S | F | D-16 | ✅ 10-24 (B9.1) |

## 8 Fehler und offene Proben (BG)

| ID | Posten | Herkunft | Befund am Code / Stand | Gr. | Risiko | Entsch. | Ziel |
|---|---|---|---|---|---|---|---|
| BG-1 | Space-Liste bleibt leer, wenn „Spaces verwalten" vor `loadOverview()` geöffnet wird | P9 Block R | → 📦 `REGISTER_ARCHIVE.md` | S | — | nein | ✅ 10-8 (B2.5) |
| BG-2 | P9-124 ⚠️ — Konfliktkopie im Browser nie gefahren | Matrix | → 📦 `REGISTER_ARCHIVE.md` | S | S | nein | P10 (M5 ✅) → P10.5 |
| BG-3 | P9-127 ⚠️ — Enter nur für vier von elf Overlays im Browser belegt | Matrix | → 📦 `REGISTER_ARCHIVE.md` | S | — | nein | P10 (M5 ✅) |

## 9 Ledger — je ein Urteil (LG)

| ID | Posten | Herkunft | Befund am Code / Stand | Gr. | Risiko | Entsch. | Ziel |
|---|---|---|---|---|---|---|---|
| LG-1 | Body-Volltextsuche in der Web-UI (Q1) | Ledger | → 📦 `REGISTER_ARCHIVE.md` | M | — | D-17 | ✅ 10-45 (B10.1 + B10.5) |
| LG-2 | Realtime | Ledger | → 📦 `REGISTER_ARCHIVE.md` | L | — | D-17 | ✅ 10-46/47/48 (B10.2 + B10.3 + B10.5) |
| LG-3 | Light-Mode (P5-X) | Ledger | Dunkel-first ist gelockt · **[2026-10-18]** nicht gewählt | M | — | D-17 | verworfen |
| LG-4 | Bulk-Append-MCP-Werkzeug | Ledger | → 📦 `REGISTER_ARCHIVE.md` | M | S | D-17 | ✅ 10-21 (B5) |
| LG-5 | `_trash/` räumen | Ledger | `DATA_ROOT/._trash/<space>/` wächst; erste Live-Löschung 2026-10-07 (V162 A). Werkzeug human-only, wie `spacectl.py` · **[2026-10-18]** D-17: der Papierkorb wird nicht geleert | S | B | D-17 | verworfen |
| LG-6 | `ROADMAP.md` straffen | Ledger | 37.296 B, `updated:`-Kette seit 2026-10-07 rotiert | S | — | nein | P10.5 (Doku-Block) |
| LG-7 | O4 — verwaiste Assets | P6, fiel bei P8.6 → P9 aus der Kette | → 📦 `REGISTER_ARCHIVE.md` | S | — | D-17 | ✅ 10-13 (B3.3–3.4) |
| LG-8 | O5 — kein EXIF-Strippen bei Bildern | P6, wiedergefunden | → 📦 `REGISTER_ARCHIVE.md` | S | A | D-17 | ✅ 10-12 (B3.1–3.2) |
| LG-9 | O7 — leere Ordner überleben einen Move | P6, wiedergefunden | Verhältnis zu P6-Zeile 30 („leergewordener Ordner verschwindet aus dem Baum") ungeklärt · V206 · **[2026-10-18]** V206 beantwortet: dieselbe Frage. Seit P6-AF räumt `store.py:909 _cleanup_emptied_folders()` geleerte Quellordner bis zur Space-Wurzel ab, ein Ordner mit `.share.yml` bleibt mit Absicht. Kein Bau, nur der Nachweis | S | — | D-17 | mit AL-1 (P6-Zeile 30) |
| LG-10 | Glyph-Entscheidungen P6/P6.5 | P6/P6.5, wiedergefunden | vermutlich durch P8 erledigt (nur Lucide-Sprite, P8 §0.3 Nr. 1) · V204 · **[2026-10-18, V204 beantwortet: gegenstandslos]** git log -S ueber die betroffenen Glyphen (Baum-Twists ▸/▾, Freigeben-Knopf ⇄, HTML-Entities &#8962;/&#9881;/&#128444;/&#128279;): letzter Griff je Glyph ist der P8-C2-Commit `0d97b3a` (Lucide-Sprite), danach keine Aenderung mehr; aktuelle Treffer in `webui/static/`: 0 in Markup/JS (1 grep-Treffer = Binaer-Font, Fehlalarm). Keine P6-/P6.5-Entscheidung hat einen lebenden Traeger mehr | — | — | nein | P10 (Prüfung) |
| LG-11 | Verbundene AI-Sessions (p8x §10.8) | P9-Plan §15 | neue Fähigkeit | L | — | nein | P11 |

## 10 Altlasten früherer Phasen (AL)

| ID | Posten | Herkunft | Befund am Code / Stand | Gr. | Risiko | Entsch. | Ziel |
|---|---|---|---|---|---|---|---|
| AL-1 | P6 🟡 — Zeilen 7, 9, 14, 15, 16, 17, 23, 25, 29, 30 offen (fielen bei P8.6 → P9 aus der Kette) | P6-Handover §3, P8.5-Handover §4.7 | Kandidaten für Nachweis aus späteren Belegen: 7 (Update-Log-Gate in jedem P9-Deploy), 9 (Ordner real), 16/30 (Wegwerf-belegt — zählt seit P8.5 als live), 23 (Reboot ↔ Watchdog P9-B), 25 (UI seither neu) · V205 · **[2026-10-18, V205 beantwortet — Abgleich mit P7–P9 plus M3/M5-Wegwerf-Belege dieser Session]** **schliessbar (7):** Zeile 7 (deploy.sh-Gate: in jedem P9-Deploy aktiv, Unit-Tests, der 2026-08-14-Vorfall selbst), 9 (echte Ordner am DATA_ROOT, 2026-08-23 nachgeprüft), 16 (Re-Auth beim Widen am Browser: M5-Station share, reauth_appeared; Ruecknahme bleibt gate-frei), 17 (p8_8-Zweitnutzer-Probe liess update_item share_read/share_write live ablehnen), 23 (2026-08-19 live widerlegt → P9-B Watchdog live gegen dieselbe Fehlerklasse), 25 (gegenstandslos — die UI, auf die sich die Zeile bezog, ist seit P8 v3 ganz neu), 30 (Wegwerf-belegt, zaehlt seit P8.5 als live) · **offen (3):** 14 (Fremd-Space-Haelfte live belegt; die GETEILTE-Space-Haelfte braucht eine Mini-Sonde gegen einen read-Space), 15 (braucht gelaufene visibility-Migration + Live-Check), 29 (Move ueber den Connector — eine kleine MCP-Sonde kann sie schliessen, z. B. in P10.5 Block 2) · **[2026-10-18]** D-18 ja; Zeile 30 deckt LG-9 mit ab | M | — | D-18 | 🟡 10-11 ✅ (B2.5; 15 Nikinger, Rest B12) |
| AL-2 | P6-Zeilen 10–13, 18, 24, 27, 28, 36, 37 brauchen Fabian oder einen dritten Nutzer | P6-Handover §3 | P7 hat einen Teil per `testnutzer-p7` ersetzt; der Rest ist ein Termin (Wurzel §Working style) · **[2026-10-18]** D-18 ja | — | — | D-18 | Termin |
| AL-3 | P6-Zeilen 31–34 (Mehrfachauswahl) stehen auf „nie gebaut" | P6-Handover §3 | in P7 gebaut (ROADMAP P7) — die Zeilen sind nie nachgezogen | S | — | nein | P10 (Doku) |
| AL-4 | P6.5 🟡 — P6.5-14 („kündigt jeden Upload an") | `phase6_5_tools_images/CLAUDE.md:78` | Bewertung des Nikingers; zwei Datenpunkte liegen vor · **[2026-10-18]** D-18 | — | — | D-18 | Entscheidung des Nikingers (einmalig) |
| AL-5 | P9 ⚠️ ohne Code-Arbeit: P9-15, 22, 27, 31, 55, 56, 72, 74, 97, 99 | Handover §3 | die Begründung steht je Zeile; nur das Urteil „ausreichend" fehlt · **[2026-10-18]** D-18 | — | — | D-18 | erledigt (ausreichend) |
| AL-6 | P9-13 / V150 — zweites Konto über die neue Adresse | Matrix ⬜ | Termin, kein Blocker | — | B | nein | Termin |
| AL-7 | V157 ⚠️ (WebKit ungemessen) · V162 B ⚠️ (`serve --tcp` und ACL) | Handover §5 | V162 B hängt an BT-3 · **[2026-10-18]** V162 B entfällt mit D-9 (Zugriff akzeptiert) | — | — | nein | gegenstandslos |

## 11 Doku und Werkzeuge (DO)

| ID | Posten | Herkunft | Befund am Code / Stand | Gr. | Risiko | Entsch. | Ziel |
|---|---|---|---|---|---|---|---|
| DO-1 | Drei Phase-Heads über dem Softcap, „benannt statt versteckt": `phase8_6_ui_polish/CLAUDE.md` (~106 KB), `phase8_ui_graph/CLAUDE.md` (~47 KB), `phase6_shares/CLAUDE.md` (~41 KB) | Step 0 (2026-10-16) | `scripts/move_sections.py` existiert seit 2026-10-07 genau dafür | S | — | nein | P10.5 (Doku-Block) |
| DO-2 | **Zwei Doku-Wächter am Rand.** `docs/INDEX.md` 39.421 B gegen die harte Grenze 40.960 B (`test_index_archive.py`; jede Phase kostet ~1 KB). Und `test_acceptance_numbers.py :: test_the_live_byte_figures_in_the_matrix_are_the_real_sizes` koppelt die **geschlossene** P9-Zeile P9-6 (35.677 B) an die **lebende** Größe von `ROADMAP.md` (±2.048 B): nach dem P10-Commit 159 B Luft, die nächste ROADMAP-Zeile reißt ihn | Step 0, Testlauf 2026-10-16 | → 📦 `REGISTER_ARCHIVE.md` | S | — | D-17 | ✅ 10.5-2 (B0) |
| DO-3 | Ausführlichkeit der Session-Blöcke (10–17 KB, P9-Archiv 396 KB) | Handover §7 | Kostenfaktor jeder Lesesitzung · **[2026-10-18]** D-17 ja: Session-Block ≤ 4 KB | S | — | D-17 | P10.5 (Obergrenze je Block im Plan) |
| DO-4 | Planungsprompt „verloren" | Nikinger 2026-10-16 | war nie verloren: `docs/PROMPTS.md` Prompt 2, datierte Korrektur in `0a7aaf4` | — | — | nein | erledigt (`0a7aaf4`) |
| DO-5 | Fleet-Notiz §7 nennt `step_a/Caddyfile` | Step 0 | die Datei heißt `Caddyfile.template`; datierte Korrektur in intake §7 | — | — | nein | erledigt (Plan-Commit) |

## Bilanz (nach den Entscheidungen, 2026-10-18)

**76 Zeilen** in elf Themen (BT 13 · PF 6 · PA 7 · KA 5 · ED 5 · UI 7 · RE 7 · BG 3 · LG 11 · AL 7 · DO 5). Nach dem **ersten** Ziel
der Spalte: **P10.5 39** · **P10 9** (Messung, Probe oder Prüfung) · **P11 4** · **verworfen 6** (davon PA-3 „nicht geplant") ·
**Wissen 6** · **Termin 3** · **erledigt 3** · **an Fleet 2** · **4 ohne Bau** (RE-5 ist eine gelockte Regel, LG-9 geht in AL-1 auf,
AL-4 ist eine einmalige Bewertung des Nikingers, AL-7 ist gegenstandslos). Gezählt per Skript über die Ziel-Spalte.

**Zwei P1-Öffnungen sind entschieden** (D-4 Stufe 2: Dateiformat · D-16: `created_by`) — nach P9 die elfte und zwölfte; beide
werden im P10.5-Plan angekündigt und eng geprobt wie die neunte und zehnte.
