---
status: live
purpose: Baustellenregister Phase 10 — jede offene Baustelle von Sharefyx genau einmal, mit Herkunft, Befund am Code, Größe, Risiko, nötiger Entscheidung und Ziel (P10.5 / P11 / verworfen / Termin), dazu die Entscheidungsliste für den Nikinger. Die Arbeitsliste, gegen die P10.5 geplant und abgehakt wird.
read-when: vor jeder P10-/P10.5-Planung oder -Entscheidung; wenn jemand fragt „ist X noch offen?"
detail: L2
up: ./CLAUDE.md
down:
  - ../docs/concepts/phase10_inventory_plan.md    # Plan P10: Locks, Steps, Messungen M1–M7, Abnahme, [VERIFY]
  - ../docs/concepts/phase10_intake.md            # Sammelstelle — Herkunft von §2/§3/§5–§7
  - ../docs/concepts/PHASE9_CLOSEOUT_HANDOVER.md  # Herkunft §4.1–§4.10
updated: 2026-10-16 (finalisiert mit den Antworten des Nikingers: D-1b = C2 Nervenbahnen, BT-13 beantwortet, V199 in die Exec-Session; Bilanz per Skript nachgezählt) | 2026-10-16 (angelegt — Entwurf aus allen Quellen, jede Zeile am Code verankert; Stand vor der Freigabe durch den Nikinger)
---
# Phase 10 — Baustellenregister

> **Stand:** Entwurf vom 2026-10-16 gegen `main@0a7aaf4` (live `v3.1.4`). **Die Freigabe dieses Registers durch den Nikinger ist das
> Tor zu P10.5** (Lock P10-A). Bis dahin ist jede Zeile ein Vorschlag; die Spalte „Ziel" wird erst mit der Entscheidung verbindlich.

**Lesart.** **Größe:** S ≤ ein halber Block · M ein Block · L mehrere Blöcke. **Risiko:** S Schreibpfad (Hard Rule 3) · F Dateiformat oder
P1-Contract · R Rechte (Hard Rule 4) · A Auth/Sicherheit · B Betrieb (Handgriff des Nikingers) · — keines. **Entsch.:** `D-n` = steht in der
Entscheidungsliste §12. **Ziel:** P10.5 · P11 · verworfen · Termin (wartet auf Kalender oder Person, kein Blocker) · P10 (Messung oder Probe in
P10 Step 2) · Wissen (kein Bau, nur festgehalten) · erledigt (mit Beleg). „Empfehlung" heißt: mein Vorschlag, nicht entschieden.

## 1 Betrieb und Infrastruktur (BT)

| ID | Posten | Herkunft | Befund am Code / Stand | Gr. | Risiko | Entsch. | Ziel |
|---|---|---|---|---|---|---|---|
| BT-1 | **Caddy-Quelle zieht nicht nach** — live `dial_timeout 10s`, `lb_try_duration 15s`, `lb_try_interval 1s` | intake §7 (Fleet S9) | Quelle `phase9_hardening/step_a/Caddyfile.template:65` trägt noch die einzeilige `reverse_proxy <heimvm-tailnet>:8765`. **Dringend:** wer aus der Quelle einspielt, nimmt den Fix zurück. Fleet nannte `step_a/Caddyfile` — die Datei heißt `Caddyfile.template` · V199 liest der Nikinger in der Exec-Session unmittelbar vor der Änderung | S | B | D-10 | P10.5, erster Block |
| BT-2 | `sharefyx-tail-proxy` endet bei SIGTERM mit Exit 143 → Unit `failed` | intake §6 (Fleet S6) | `phase3_edge/systemd/sharefyx-tail-proxy.service`, `[Service]` ohne `SuccessExitStatus`. `phase9_hardening/tests/test_tail_proxy.py :: test_hardening_matches_the_mcp_service` vergleicht Direktiven mit der MCP-Unit — die neue Zeile muss dort bekannt sein · V200 | S | B | D-11 | P10.5 |
| BT-3 | Tailnet-ACL: Nutzergeräte (MacBook) erreichen VM 200 voll, auch den Relay-Port 8765 | Handover §4.1, intake §5.2 | VPS-Seite ist durch Fleet Block 1 geschlossen (`tag:sharefyx-edge` → nur VM 200:8765). Die Policy lebt in `eurofyx-fleet/tailnet/policy.hujson`, nicht in diesem Repo | S | A, B | D-9 | Termin (Fleet-Repo) |
| BT-4 | Sechs LAN-Ports auf `0.0.0.0` (7070, 7777, 47984/89/90, 48010 — Sunshine u. a.) | Handover §4.2 | kein Sharefyx-Code, Dienste der VM außerhalb des Repos | S | A | D-12 | verworfen hier, an Fleet (Empfehlung) |
| BT-5 | Übergangsfenster der alten Adresse unbefristet (`LEGACY_UNTIL=open`) | Handover §4.7 | `phase4_auth/systemd/sharefyx-mcp.service:20`, `phase5_ui/webui/api.py:397` (`date.max`). Der Firmen-Proxy blockt die Domain, der Funnel bleibt nötig (intake §5.1) | S | B | D-15 | Termin: Arbeitslaptop um den 2026-11-02 erneut testen |
| BT-6 | Transitives `mcp` ungepinnt | Handover §4.5, P9 Step H | `phase2_mcp/pyproject.toml:25` pinnt nur `fastmcp==3.4.7`; gemessen 2026-10-16: Dev-venv `mcp 1.28.1`, live laut Handover `1.30.0` | S | B | D-13 | P10.5 |
| BT-7 | Zwei öffentliche Eingänge (VPS/Caddy und Funnel) — Härtung am Proxy schützt den Funnel nicht | intake §5.1, §6 (Caddy statt nginx) | Rate-Limits leben in der App (`authserver/ratelimit.py`) und gelten auf beiden Wegen. Regel daraus: Härtung gehört in die App, nicht in den Proxy | — | A | nein | Wissen |
| BT-8 | Relay antwortet über die Tailnet-IP mit 400 „Invalid host header" | intake §5.3 | `ALLOWED_HOSTS` (P4-Befund S1) — Messhinweis für Healthchecks, kein Fehler | — | — | nein | Wissen |
| BT-9 | Funnel-`nodeAttrs` hängen am User-Owner — VM 200 taggen nähme den Funnel weg | intake §5.4 | Fleet taggt VM 200 nicht | — | B | nein | Wissen |
| BT-10 | Funnel-Watchdog (geerbtes Ledger, fiel beim Übergang P8.6 → P9 aus der Kette) | P8.5-Handover §4.7 | `phase3_edge/scripts/tailscaled_watchdog.sh:93` prüft nur `Self.Online`; der Fleet-Wächter prüft alle 5 min den **Domain**-Pfad. Den **Funnel**-Pfad prüft von außen niemand · V203 | S | B | D-17 | P10.5 oder Fleet |
| BT-11 | Vision-Dienst (CT 111): `qwen3-vl:8b` als Prüfwerkzeug gestrichen | Handover §4.6 | Ersatz mit **einer** Frage bekannter Antwort testen, oder CT 111 stilllegen | S | — | D-14 | P10.5 (Werkzeug) |
| BT-12 | Fleet plant ein Backup-Ziel außerhalb von Proxmox | intake §5.5 | `sharefyx-backup.service` bleibt unverändert | — | — | nein | Wissen |
| BT-13 | opencode-Projektmarker im echten Datenverzeichnis (`savefyx-data/.git/opencode`, 40 B, 2026-09-04) | Step 0 (2026-10-16) | **beantwortet 2026-10-16 (Nikinger): ja, versehentlich** — bei der Repo-Auswahl in opencode laggt die Oberfläche, Klicks landen auf dem falschen Eintrag. Kein Datenbefund, nur Metadaten gelesen. Regel: Agenten arbeiten nie im `DATA_ROOT`; vor dem ersten Schreibschritt das Arbeitsverzeichnis prüfen | — | B | nein | Wissen |

## 2 Performance (PF)

| ID | Posten | Herkunft | Befund am Code / Stand | Gr. | Risiko | Entsch. | Ziel |
|---|---|---|---|---|---|---|---|
| PF-1 | `/api/v1/overview` = 6 Durchgänge × sichtbare Spaces (~2,4 s Serverarbeit live, 4 Spaces / 197 Items) | Handover §4.3, P9-15, V151 | `phase5_ui/webui/api.py:685 _overview()`: je Space ein `store.search(…, limit=1)` pro Eimer (`:695`) plus die Liste (`:702`), und jeder Aufruf liest jede indizierte Datei (`Store.search()`, P6-S). Zwei Wege: Zählen über den Index (P1-Kern `storage/`, Hard Rule 2 bleibt gewahrt) oder ein Durchgang je Space mit Zählung im Adapter | M | F? | D-3 | P10.5 |
| PF-2 | Messanordnung und Zielwerte fehlen | intake §2.1 | P10 Step 2: M1 (Browser des Nikingers, beide Eingänge) und M2 (Wegwerf-Instrument). Die Messlatte 372,9 ms ist falsch (anderes Instrument, P9-15) | S | — | D-3 | P10 |
| PF-3 | Client-Zwischenspeicher je Space, optimistische Anzeige, Vorabladen | intake §2.1 | ungeprüfte Kandidaten. Bruchstelle Hard Rule 3: kein Cache darf eine alte `version` in einen Write tragen | M | S | D-3 | P10.5, nur wenn M1 es nach PF-1 noch verlangt |
| PF-4 | 20-s-Poll holt `/overview` und `/spaces` getrennt | intake §2.1 | `phase5_ui/webui/static/js/app.js:402–417 pollCounters()` (20 s + Fokus + Sichtbarkeit) | S | — | nein | P10.5, mit PF-1 |
| PF-5 | Listen-Virtualisierung bei großen Spaces | intake §2.1 | live 197 Items, kein Messbefund | M | — | D-3 | verworfen, bis eine Messung es verlangt (Empfehlung) |
| PF-6 | `ui_budget` bleibt Zielgröße | intake §2.1 | 173,1 KB von 250 KB (P9-Closeout). Editor (ED-1) und Karte (KA-1) müssen hineinpassen | — | — | nein | P10.5, Abnahmekriterium je Block |

## 3 Anbieter-Unabhängigkeit (PA) — Phasenziel, Nikinger 2026-10-16

> **Ziel (Lock P10-C):** jeder standardkonforme MCP-Client kann sich verbinden, nicht nur claude.ai. Blockiert keinen Step, nur den
> Abschluss von P10.5. **Abnahme:** ein Nicht-Claude-Client führt `list_spaces` live über `https://sharefyx.eurofyx.com/mcp` aus.
> Modell-Routing bleibt Client-Seite (frühestens P11), nie im Server. Stand der Spec: **MCP 2026-07-28** ist laut Versionierungsseite
> die **aktuelle** Version („Current"; P8 §0.5 führte sie am 2026-08-28 noch als RC). DCR ist dort *deprecated*, CIMD empfohlen
> (AS **SHOULD**); Reihenfolge der Clients: Vorregistrierung → CIMD → DCR → Nutzer fragen.

| ID | Posten | Herkunft | Befund am Code / Stand | Gr. | Risiko | Entsch. | Ziel |
|---|---|---|---|---|---|---|---|
| PA-1 | Native/Loopback-Clients werden abgelehnt | Code, Spec 2026-07-28 | `phase4_auth/authserver/clients.py :: redirect_uri_allowed()` verlangt `https` und eine erlaubte Origin; `register_client()` lehnt `application_type: "native"` ab. Laut Spec **SHOULD** ein nativer Client genau das senden. opencode registriert per DCR mit Loopback-Callback (laut PR #5940 Standard `http://127.0.0.1:19876/mcp/oauth/callback`, V195) → heute `invalid_client_metadata` bzw. `invalid_redirect_uri`. Der `[SEAM]`-Docstring sagt: diese Funktion und ihre Tests, sonst nichts | M | A | D-8 | P10.5 |
| PA-2 | CSP `form-action` kennt nur `'self'` plus Web-Origins | P4 Modul 8c (Live-Fund 2026-07-30) | `phase4_auth/authserver/config.py :: AuthSettings.csp_form_action`. Chromium prüft `form-action` auch gegen das Redirect-Ziel; ein Loopback-Redirect nach dem Login würde lautlos blockiert — derselbe Fehler wie 2026-07-30 mit claude.ai · V197 | S | A | nein (folgt aus PA-1) | P10.5 |
| PA-3 | Web-Clients (ChatGPT u. a.) | Code, OpenAI-Doku | Origins sind per `SPACE_OAUTH_ALLOWED_REDIRECT_ORIGINS` konfigurierbar (`config.py:134`), kein Code nötig. ChatGPT-Callback laut OpenAI-Doku `https://chatgpt.com/connector_platform_oauth_redirect` (oder `…/connector/oauth/{callback_id}`), also eine Origin. ChatGPT unterstützt `none` mit PKCE — der AS kennt nur `none` (`metadata.py:34`), das passt. Offen: was ChatGPT per DCR genau anfragt · V196 | S | A, B | D-8 | P10.5, nur wenn gewollt |
| PA-4 | CIMD fehlt | Spec 2026-07-28, P4-E | `metadata.py` lässt `client_id_metadata_document_supported` bewusst weg — sonst schaltet claude.ai auf CIMD um und der laufende Connector wechselt den Weg. CIMD heißt außerdem: der Server holt fremde HTTPS-URLs (SSRF-Fläche auf der Heim-VM) | L | A | D-8 | P11 (Empfehlung) — für das Phasenziel nicht nötig |
| PA-5 | MCP-Protokoll 2026-07-28 / FastMCP 4 (V79) | Ledger, P8 §0.5 | gemessen 2026-10-16: Dev `mcp 1.28.1` handelt bis `2025-11-25`. Die Spec 2026-07-28 handelt **je Anfrage** aus (`_meta`, `server/discover`) und beschreibt eine Rückwärtskompatibilität zu handshake-basierten Servern. Offen: was kann live `mcp 1.30.0`, und nutzt der Abnahme-Client diesen Weg? · V198 | L | A | D-17 | P10 (M3 misst) → Umstieg P11 |
| PA-6 | Die Projektbeschreibung nennt nur Claude | Wurzel-`CLAUDE.md` §What this project is | „für zwei Personen … und deren Claude-Instanzen" | S | — | nein | P10.5, Closeout |
| PA-7 | Abnahme-Client und Messung | Lock P10-C | P10 Step 2 M3: echter DCR-Request des Clients gegen eine Wegwerf-Instanz, Ablehnung erwartet → Baseline. Live-Abnahme in P10.5 durch den Nikinger | S | B | D-8 | P10 (M3) + P10.5 |

## 4 Karte (KA) — Umbau, Nikinger 2026-10-16

> Gewählt: Stil (p8x §2.2), Layout merken, Interaktion; dazu „etwas gehirnartiger". Erste Runde:
> `docs/concepts/phase10_karte_entwurf_{a,b,c}.svg` (A Landkarte · B Gehirn · C Gehirnkarte) — **entschieden: C** (D-1, 2026-10-16).
> Zweite Runde, drei Stile innerhalb C: `docs/concepts/phase10_karte_c_stil_{1,2,3}.svg` (C1 Flächen · C2 Nervenbahnen · C3 Höhenlinien),
> **gewählt: C2 Nervenbahnen** (D-1b, 2026-10-16). Nicht gewählt: Einklappen (§2.5).

| ID | Posten | Herkunft | Befund am Code / Stand | Gr. | Risiko | Entsch. | Ziel |
|---|---|---|---|---|---|---|---|
| KA-1 | Stil: **Gehirnkarte im Stil C2 Nervenbahnen** (D-1 + D-1b, 2026-10-16) — Spaces als Lappen eines Körpers mit leiser Innenlinie, Furchen als Space-Grenzen, Bahnen stärker geschwungen, Knoten als Zellen mit Membran-Ring und Fortsätzen, ein Fokus aktiviert erste und zweite Nachbarn | p8x §2.2, Nikinger 2026-10-16 | `phase5_ui/webui/static/js/graph.js` (33 KB, handgerollt, `draw()`/`drawEdges()`/`drawNodes()`, keine Bibliothek). Die Lappen entstehen im Browser: Raster, nächster Knoten, Erosion als Furche, Konturverfahren — keine festen Formen, kein Server. Farbe nur mit Bedeutung, keine Transparenz-Abhängigkeit (P8 §0.3 Nr. 4/6). Ruhezustand ohne Fokus: alle Knoten voll deckend; Abdunkeln (0,45) nur bei Hover oder Treffer — Form und Farbe tragen die Bedeutung | M–L | — | D-1b | P10.5 |
| KA-2 | Layout über den Reload merken | p8x §2.4 (Rest), Nikinger 2026-10-16 | heute nur innerhalb einer Sitzung (P9 Step E), Seed deterministisch (P8.6-D2). Ablage im Browser (`localStorage`), kein Serverzustand | S | — | nein | P10.5 |
| KA-3 | Interaktion: Suche mit Treffer, Filter nach Typ/Status, Titel ohne Zoom | Nikinger 2026-10-16 | der Graph-Knoten trägt neun Felder (`api.py :: _graph_get`, ab `:720`): `id, title, space, own, writable, type, status, folder, tags` — Suche und Filter brauchen **kein** neues Feld. „Kürzlich geändert" (Entwurf B) bräuchte ein zehntes (`updated`) = API-Öffnung | M | — | D-1 | P10.5 |
| KA-4 | Einklappen mit Abhängigkeiten | p8x §2.5 | am 2026-10-16 nicht gewählt | — | — | D-2 | verworfen (Empfehlung) oder P11 |
| KA-5 | `doing` auf Übersicht und Karte hervorheben | P9-Plan §15, P9-P | der fünfte Eimer existiert (Block doing); die prominente Darstellung fehlt | S | — | nein | P10.5, mit KA-1 oder UI |

## 5 Editor (ED)

| ID | Posten | Herkunft | Befund am Code / Stand | Gr. | Risiko | Entsch. | Ziel |
|---|---|---|---|---|---|---|---|
| ED-1 | Schreiben ohne Wechsel zwischen Vorschau und Bearbeiten (Stufe 1: Live-Darstellung über Markdown) | intake §2.3, feedback E3 | `phase5_ui/webui/static/js/editor.js:294–302 setEditorMode()` schaltet `preview`/`edit`, Vorgabe `preview` (`:431`). **Widerspricht dem gelockten P5-U** („Markdown-Textarea + Formatierhilfen, kein WYSIWYG") — Umkehr nur als datierte Nikinger-Entscheidung. Eine Bibliothek muss ohne Build-Schritt laufen (P5-T) und ins `ui_budget` passen · V201 | L | S | D-4 | P10.5 |
| ED-2 | To-do-Kästchen im Text, anklickbar | P9-Plan §15, intake §2.3 | `markdown.js` plus Schreibpfad: ein Klick ist ein Write mit `version` (Hard Rule 3) | M | S | D-4 | P10.5, mit ED-1 |
| ED-3 | Erweiterte Formatierung (Farbe, Ausrichtung, Größe) | intake §2.3 Stufe 2 | in Markdown nicht ausdrückbar → elfte P1-Contract-Öffnung, alle MCP-Clients lesen mit | L | F | D-4 | verworfen oder P11 (Empfehlung) |
| ED-4 | Excel-artige Tabellen | intake §2.3 Stufe 3 | eigener Item-Typ = neue Fähigkeit | L | F | nein | P11 |
| ED-5 | Rohmodus als Notausgang | intake §2.3 | für Items, die der Editor nicht verlustfrei darstellt | S | S | nein | P10.5, mit ED-1 |

## 6 Darstellung (UI)

| ID | Posten | Herkunft | Befund am Code / Stand | Gr. | Risiko | Entsch. | Ziel |
|---|---|---|---|---|---|---|---|
| UI-1 | Eigene 404-Seite für `/ui/…` | intake §2.2 | unbekannte `/ui/`-Pfade enden im Standard-404 von Starlette; fehlende statische Dateien im Klartext „Nicht gefunden." (`phase5_ui/webui/static_routes.py:86`). API und `/mcp` bleiben bei JSON | S | — | nein | P10.5 |
| UI-2 | Logo, vorläufig, ein Austauschpunkt (SVG + Favicon) | intake §2.2, P9-Plan §15 | die Marke ist heute Text: `app.html:20 .rail__brand`, `pages.py:42 .auth__brand`; kein Favicon | S | — | D-6 | P10.5 |
| UI-3 | Tab-Titel je Ansicht (V120) | intake §2.2 | `app.html:6` statisch `<title>sharefyx</title>`, kein `document.title` im JS | S | — | D-5 | P10.5 |
| UI-4 | Einheitliche Design-Vorlage, Radien-/Auswahl-Vereinheitlichung | P9-Plan §15, p8x §10.1–§10.7 | Auswahl-Konvention v3 in `phase8_ui_graph/CLAUDE.md`; P9 hat Knöpfe (B17) und Einstellungen vereinheitlicht. Der Rest ist eine Liste, die erst eine Sichtung ergibt | M | — | D-17 | P10.5, nach Sichtung |
| UI-5 | Kontrast der Vorsicht-Beschriftung 4,38:1 (unter AA 4,5:1) | Handover §4.8, B17 | `.btn.action--caution` mit `color: var(--caution)` | S | — | D-7 | P10.5 (Empfehlung: schließen) |
| UI-6 | Assignee-Picker und -Filter | P9-Plan §15 | der Editor hat Feld und Vorschlagsliste (`editor.js:263ff.`); Filter in der Liste fehlt | S | — | nein | P10.5 |
| UI-7 | Handy-Oberfläche | Nikinger 2026-10-08 | Desktop-Untergrenze 1024 px; eine Handy-App wird ein eigenes Design | — | — | nein | P11 |

## 7 Rechte und Spaces (RE)

| ID | Posten | Herkunft | Befund am Code / Stand | Gr. | Risiko | Entsch. | Ziel |
|---|---|---|---|---|---|---|---|
| RE-1 | Ordner in Team-Spaces anlegen | Block feedback | `phase5_ui/webui/api.py:459–460`: `space != session.space` → „Ordner können nur im eigenen Space angelegt werden." | S | R | D-17 | P10.5 |
| RE-2 | MCP `update_item`: Ordner wechseln in Team-Spaces | Block feedback, Handover §6 | `phase2_mcp/mcpserver/tools.py:752` erlaubt `folder` nur dem Eigentümer-Space; die Web-Oberfläche darf es seit E1a (P9-BG/BP) → zwei Wege, zwei Regeln | S | R | nein (Parität) | P10.5 |
| RE-3 | Space umbenennen (V194) | feedback E2 | es gibt keine Umbenenn-Funktion (`spacectl.py`, `storage/`). Verweise: Verzeichnis, `.share.yml`, Mitglieder, Index, Links, Auth (`users.space`), `assignee` (Space-Name ohne Validierung, V160) | L | R, F, A | D-17 | P11 (Empfehlung) |
| RE-4 | Ordner umbenennen (V193) | P9-Plan §15 | die billige Frontend-Fassung lässt die `.share.yml` eines geteilten Ordners zurück (P8.6-Plan §0.4.1) | M | R | D-17 | P10.5 oder P11 |
| RE-5 | Verschieben in fremde Spaces | P9-Plan §15 | `store.move()` und P6-AE existieren; offen ist die Regel, nicht der Code | S | R | D-17 | Entscheidung |
| RE-6 | Rechteverwaltung über MCP (P6-M) | Ledger | Hard Rule 4: die Freigabeliste ist „über kein Item-Tool änderbar"; P6-17 belegt, dass kein Tool `share_*` setzt | M | R, A | D-17 | verworfen (Empfehlung) |
| RE-7 | `created_by` sichtbar machen (elfte Öffnung) | Handover §4.10, P9-BQ | die Spur existiert schon (`updated_by` + Git-Autor) | S | F | D-16 | verworfen oder P11 (Empfehlung) |

## 8 Fehler und offene Proben (BG)

| ID | Posten | Herkunft | Befund am Code / Stand | Gr. | Risiko | Entsch. | Ziel |
|---|---|---|---|---|---|---|---|
| BG-1 | Space-Liste bleibt leer, wenn „Spaces verwalten" vor `loadOverview()` geöffnet wird | P9 Block R | `spaces.js` liest `state.spaces`, das erst `list.js :: loadOverview()` füllt; `spaces.js:214` lädt nur in einem Pfad nach · V202 | S | — | nein | P10 (M4) → P10.5 |
| BG-2 | P9-124 ⚠️ — Konfliktkopie im Browser nie gefahren | Matrix | `dialogs.js` setzt `payload.space` aus `state.conflictCurrent.space` | S | S | nein | P10 (M5) |
| BG-3 | P9-127 ⚠️ — Enter nur für vier von elf Overlays im Browser belegt | Matrix | `app.js :: enterTable()` + `SETTINGS_ENTER` | S | — | nein | P10 (M5) |

## 9 Ledger — je ein Urteil (LG)

| ID | Posten | Herkunft | Befund am Code / Stand | Gr. | Risiko | Entsch. | Ziel |
|---|---|---|---|---|---|---|---|
| LG-1 | Body-Volltextsuche in der Web-UI (Q1) | Ledger | MCP kann es (`search_items(in_body=True)`), `api.py` und die UI nicht | M | — | D-17 | P10.5 oder P11 |
| LG-2 | Realtime | Ledger | der 20-s-Poll reicht für zwei Personen | L | — | D-17 | P11 (Empfehlung) |
| LG-3 | Light-Mode (P5-X) | Ledger | Dunkel-first ist gelockt | M | — | D-17 | verworfen (Empfehlung) |
| LG-4 | Bulk-Append-MCP-Werkzeug | Ledger | ein neues Tool ist eine neue Fähigkeit | M | S | D-17 | P11 |
| LG-5 | `_trash/` räumen | Ledger | `DATA_ROOT/._trash/<space>/` wächst; erste Live-Löschung 2026-10-07 (V162 A). Werkzeug human-only, wie `spacectl.py` | S | B | D-17 | P10.5 |
| LG-6 | `ROADMAP.md` straffen | Ledger | 37.296 B, `updated:`-Kette seit 2026-10-07 rotiert | S | — | nein | P10.5 (Doku-Block) |
| LG-7 | O4 — verwaiste Assets | P6, fiel bei P8.6 → P9 aus der Kette | kein Prüf- oder Räumweg | S | — | D-17 | P10.5 |
| LG-8 | O5 — kein EXIF-Strippen bei Bildern | P6, wiedergefunden | GPS- und Gerätedaten bleiben im hochgeladenen Bild | S | A | D-17 | P10.5 (Empfehlung) |
| LG-9 | O7 — leere Ordner überleben einen Move | P6, wiedergefunden | Verhältnis zu P6-Zeile 30 („leergewordener Ordner verschwindet aus dem Baum") ungeklärt · V206 | S | — | D-17 | P10 (Prüfung) |
| LG-10 | Glyph-Entscheidungen P6/P6.5 | P6/P6.5, wiedergefunden | vermutlich durch P8 erledigt (nur Lucide-Sprite, P8 §0.3 Nr. 1) · V204 | — | — | nein | P10 (Prüfung) |
| LG-11 | Verbundene AI-Sessions (p8x §10.8) | P9-Plan §15 | neue Fähigkeit | L | — | nein | P11 |

## 10 Altlasten früherer Phasen (AL)

| ID | Posten | Herkunft | Befund am Code / Stand | Gr. | Risiko | Entsch. | Ziel |
|---|---|---|---|---|---|---|---|
| AL-1 | P6 🟡 — Zeilen 7, 9, 14, 15, 16, 17, 23, 25, 29, 30 offen (fielen bei P8.6 → P9 aus der Kette) | P6-Handover §3, P8.5-Handover §4.7 | Kandidaten für Nachweis aus späteren Belegen: 7 (Update-Log-Gate in jedem P9-Deploy), 9 (Ordner real), 16/30 (Wegwerf-belegt — zählt seit P8.5 als live), 23 (Reboot ↔ Watchdog P9-B), 25 (UI seither neu) · V205 | M | — | D-18 | P10 (Prüfung) → P10.5 |
| AL-2 | P6-Zeilen 10–13, 18, 24, 27, 28, 36, 37 brauchen Fabian oder einen dritten Nutzer | P6-Handover §3 | P7 hat einen Teil per `testnutzer-p7` ersetzt; der Rest ist ein Termin (Wurzel §Working style) | — | — | D-18 | Termin |
| AL-3 | P6-Zeilen 31–34 (Mehrfachauswahl) stehen auf „nie gebaut" | P6-Handover §3 | in P7 gebaut (ROADMAP P7) — die Zeilen sind nie nachgezogen | S | — | nein | P10 (Doku) |
| AL-4 | P6.5 🟡 — P6.5-14 („kündigt jeden Upload an") | `phase6_5_tools_images/CLAUDE.md:78` | Bewertung des Nikingers; zwei Datenpunkte liegen vor | — | — | D-18 | Entscheidung |
| AL-5 | P9 ⚠️ ohne Code-Arbeit: P9-15, 22, 27, 31, 55, 56, 72, 74, 97, 99 | Handover §3 | die Begründung steht je Zeile; nur das Urteil „ausreichend" fehlt | — | — | D-18 | P10 (Bestätigung) |
| AL-6 | P9-13 / V150 — zweites Konto über die neue Adresse | Matrix ⬜ | Termin, kein Blocker | — | B | nein | Termin |
| AL-7 | V157 ⚠️ (WebKit ungemessen) · V162 B ⚠️ (`serve --tcp` und ACL) | Handover §5 | V162 B hängt an BT-3 | — | — | nein | mit BT-3 / gegenstandslos |

## 11 Doku und Werkzeuge (DO)

| ID | Posten | Herkunft | Befund am Code / Stand | Gr. | Risiko | Entsch. | Ziel |
|---|---|---|---|---|---|---|---|
| DO-1 | Drei Phase-Heads über dem Softcap, „benannt statt versteckt": `phase8_6_ui_polish/CLAUDE.md` (~106 KB), `phase8_ui_graph/CLAUDE.md` (~47 KB), `phase6_shares/CLAUDE.md` (~41 KB) | Step 0 (2026-10-16) | `scripts/move_sections.py` existiert seit 2026-10-07 genau dafür | S | — | nein | P10.5 (Doku-Block) |
| DO-2 | **Zwei Doku-Wächter am Rand.** `docs/INDEX.md` 39.421 B gegen die harte Grenze 40.960 B (`test_index_archive.py`; jede Phase kostet ~1 KB). Und `test_acceptance_numbers.py :: test_the_live_byte_figures_in_the_matrix_are_the_real_sizes` koppelt die **geschlossene** P9-Zeile P9-6 (35.677 B) an die **lebende** Größe von `ROADMAP.md` (±2.048 B): nach dem P10-Commit 159 B Luft, die nächste ROADMAP-Zeile reißt ihn | Step 0, Testlauf 2026-10-16 | im P10-Commit rot gelaufen und durch Kürzen der eigenen ROADMAP-Zeilen grün gemacht — nicht durch einen Eingriff in P9-Testcode (P10-H). Lösung: den Test auf den Closeout-Stand einfrieren oder P9-6 aus der Live-Prüfung nehmen; Code in `phase9_hardening/tests/`, also nur mit Nikinger-OK | S | — | D-17 | P10.5, vor der nächsten ROADMAP-Änderung |
| DO-3 | Ausführlichkeit der Session-Blöcke (10–17 KB, P9-Archiv 396 KB) | Handover §7 | Kostenfaktor jeder Lesesitzung | S | — | D-17 | P10.5 (Obergrenze je Block im Plan) |
| DO-4 | Planungsprompt „verloren" | Nikinger 2026-10-16 | war nie verloren: `docs/PROMPTS.md` Prompt 2, datierte Korrektur in `0a7aaf4` | — | — | nein | erledigt (`0a7aaf4`) |
| DO-5 | Fleet-Notiz §7 nennt `step_a/Caddyfile` | Step 0 | die Datei heißt `Caddyfile.template`; datierte Korrektur in intake §7 | — | — | nein | erledigt (Plan-Commit) |

## 12 Entscheidungsliste (für P10 Step 3)

Antworten werden hier **mit Datum** eingetragen; erst dann wird das „Ziel" der Registerzeile verbindlich.

| D | Frage | Zeilen | Empfehlung | Antwort |
|---|---|---|---|---|
| D-1 | Welcher Karten-Entwurf (A Landkarte · B Gehirn · C Gehirnkarte) oder welche Mischung? | KA-1, KA-3 | C mit der Aktivierung aus B, ohne „kürzlich geändert" (kein zehntes Feld) | **C** — Nikinger 2026-10-16 („Option C finde ich mega") |
| D-1b | Welcher Stil innerhalb C (C1 Flächen · C2 Nervenbahnen · C3 Höhenlinien) oder welche Mischung? | KA-1 | C1 als Grundbild, Aktivierung aus C2 nur beim Hover | **C2 Nervenbahnen** — Nikinger 2026-10-16 |
| D-2 | Einklappen der Karte (§2.5): verwerfen oder P11? | KA-4 | verwerfen | offen |
| D-3 | Zielwerte Performance und welcher Weg für `/overview` | PF-1–PF-3, PF-5 | Ziele nach M1/M2 festlegen; Vorschlag zum Start: `/overview` serverseitig ≤ 300 ms bei Live-Last, Space-Wechsel gefühlt ≤ 1 s über die Domain | offen |
| D-4 | Editor: Stufe 1 bauen (hebt P5-U auf)? Stufe 2 (elfte Öffnung)? | ED-1–ED-3 | Stufe 1 ja, mit Rohmodus; Stufe 2 nein | offen |
| D-5 | Tab-Titel deutsch oder englisch? | UI-3 | deutsch, wie die Oberfläche | offen |
| D-6 | Logo-Platzhalter: Wortmarke als SVG oder ein schlichtes Zeichen? | UI-2 | Wortmarke „sharefyx" als SVG, ein Austauschpunkt | offen |
| D-7 | Kontrast 4,38:1 schließen? | UI-5 | ja: hellere Vorsichtfarbe nur für Text | offen |
| D-8 | Anbieter: welcher Abnahme-Client, gehören Web-Clients und CIMD dazu? | PA-1, PA-3, PA-4, PA-7 | opencode als Abnahme-Client; DCR für native Clients + Loopback; ChatGPT nur per Konfiguration, falls gewollt; CIMD → P11 | offen |
| D-9 | Darf das MacBook den Relay-Port 8765 erreichen? | BT-3 | nein — nur `tag:sharefyx-edge` | offen |
| D-10 | Caddy-Vorlage auf die Live-Werte nachziehen? | BT-1 | ja, nach V199 | offen |
| D-11 | `SuccessExitStatus=143` in die Relay-Unit? | BT-2 | ja | offen |
| D-12 | LAN-Ports: Sharefyx-Posten oder Fleet? | BT-4 | Fleet | offen |
| D-13 | `mcp` exakt pinnen (auf den Live-Stand)? | BT-6 | ja, `mcp==1.30.0` nach Messung | offen |
| D-14 | Vision-Modell: Ersatz testen oder CT 111 stilllegen? | BT-11 | eine Frage bekannter Antwort an einen Kandidaten; fällt sie, stilllegen | offen |
| D-15 | Übergangsfenster wieder befristen — wann? | BT-5 | Test am 2026-11-02, danach Datum setzen | offen |
| D-16 | `created_by` (elfte Öffnung)? | RE-7 | nein | offen |
| D-17 | Ledger-Urteile: BT-10, PA-5, UI-4, RE-1, RE-3–RE-6, LG-1–LG-5, LG-7–LG-9, DO-2, DO-3 | s. Zeilen | je Zeile in der Spalte „Ziel" | offen |
| D-18 | Altlasten: P6/P6.5 mit späteren Belegen schließen, Rest als Termin führen, P9-⚠️ als ausreichend bestätigen? | AL-1, AL-2, AL-4, AL-5 | ja | offen |

## Bilanz (Entwurf, 2026-10-16)

**76 Zeilen** in elf Themen (BT 13 · PF 6 · PA 7 · KA 5 · ED 5 · UI 7 · RE 7 · BG 3 · LG 11 · AL 7 · DO 5). Nach dem **ersten** Ziel
der Spalte: **P10.5 37** (davon 3 mit Alternative „oder P11"/„oder Fleet") · **P10 11** (Messung, Probe oder Prüfung) · **P11 7** ·
**verworfen 7** (alles Empfehlungen) · **Termin 4** · **Wissen 5** · **erledigt 2** · **ohne Ziel 3** (RE-5 und AL-4 warten auf eine
Entscheidung, AL-7 hängt an BT-3). Gezählt per Skript über die Ziel-Spalte, nicht von Hand; die verbindliche
Bilanz entsteht erst nach §12.
