---
status: live
purpose: Sammelstelle für Phase 10 — alle offenen Baustellen von Sharefyx an einem Ort, die Zweiteilung P10 (Bestandsaufnahme) / P10.5 (Ausführung) und die Nikinger-Wünsche vom 2026-10-08. Noch kein Plan, keine Locks.
read-when: beim Start von Phase 10, oder wenn irgendwo „nach P10" steht und man wissen will, was damit gemeint ist
detail: L2
up: ../../ROADMAP.md
down:
  - ./phase9_hardening_plan.md                  # 📕 §15 „Was P9 benennt und nicht baut — die P10-Liste" (Herkunft des Erbes)
  - ./phase9_hardening_block_feedback_plan.md   # §3 E2/E3, §8 B8 — Befunde, die nach P10 gehen
  - ./p8x_ui_polish_notes.md                    # §2 Karte, §10 Auswahl-Konvention, §10.9 Hochkant
  - ../../phase9_hardening/ABNAHME_MATRIX.md    # die 12 ⚠️ und der eine ⬜ (Stand Closeout 2026-10-08) — jede Zeile braucht in P10 ein Urteil
  - ../../phase10_inventory/BAUSTELLENREGISTER.md   # seit 2026-10-16 der Stand: das Register, das aus dieser Sammelstelle entstand
updated: 2026-10-19 (neu §8: Note **an** `eurofyx-fleet` — GLM-Ausführer-Befunde für die Fleet-Integration Claude Code + GLM) | 2026-10-16 (Phase 10 begonnen: Zeiger aufs Register oben, §1 bestätigt (P10-A), §2.3 P5-U-Konflikt, neu §2.4 Anbieter-unabhängig und §2.5 Karten-Umbau, §7 Korrektur Caddyfile.template) | 2026-10-13 (Note from other project: eurofyx-fleet S9, neuer Abschnitt 7: Caddy dial_timeout/lb_try live, Quelle nachziehen) | 2026-10-11 (Note from other project: eurofyx-fleet S6, neuer Abschnitt 6: tail-proxy Exit 143) | 2026-10-11 (Note from other project: eurofyx-fleet Block 1 abgeschlossen, neuer Abschnitt 5) | 2026-10-08 (Closeout P9: Zeiger auf `PHASE9_CLOSEOUT_HANDOVER.md` §4 in §3, Matrix-Stand 12 ⚠️ · 1 ⬜) | 2026-10-08 (angelegt — Nikinger-Auftrag nach dem Block feedback: P10 beendet **alle** Baustellen, damit P11 auf einem gehärteten Fundament neue Funktionen denken kann; Zweiteilung P10/P10.5; drei neue Themen: Responsivität/Performance, visuelle Kleinigkeiten, Editor ohne Vorschau/Bearbeiten-Modus)
---

# Phase 10 — Sammelstelle (kein Plan)

> **Das Bild des Nikingers (2026-10-08):** P9 war das Fundament, **P10 baut das Haus fertig und dämmt es**,
> damit P11 überhaupt erst über eine Garage nachdenken darf. Regel daraus: **Phase 10 endet erst, wenn es keine
> offene „Baustelle" mehr gibt.** Neue Funktionen (P11) sind in P10 ausdrücklich nicht Teil des Auftrags.

> **Seit 2026-10-16 ist das Register der Stand:** `phase10_inventory/BAUSTELLENREGISTER.md` (76 Zeilen, Entscheidungsliste D-1–D-18),
> Plan `docs/concepts/phase10_inventory_plan.md`. Diese Sammelstelle bleibt die Herkunft. Notizen anderer Projekte dürfen weiter hier
> landen (Muster §5–§7); Claude Code überträgt sie ins Register.

## 1. Zweiteilung (Vorschlag, Nikinger-Gedanke 2026-10-08)

**[2026-10-16] Bestätigt** (Nikinger, Lock P10-A): erst das Register, dann der P10.5-Plan; die Freigabe des Registers ist das Tor.

| Teil | Auftrag | Ergebnis | Code? |
|---|---|---|---|
| **P10** (Bestandsaufnahme) | alles Offene einsammeln, messen, entscheiden, in Größe und Reihenfolge bringen | ein **Baustellenregister** (§4) + ein Plan mit Locks für P10.5 | nein — nur Messskripte und Probes |
| **P10.5** (Ausführung) | das Register abarbeiten, ein Block je Thema, jeder mit Probe + Gegenlauf | geschlossene Baustellen, Abnahmematrix ohne ⬜ | ja |

**Warum getrennt** (meine Begründung, Nikinger darf kippen): P9 hat mehrfach gezeigt, dass „erst bauen, dann messen" Arbeit kostet — die
390-px-Zeile (P9-126) war ein Kriterium, das niemand vorher am Layout geprüft hatte, und die Ladezeit (P9-132) war eine Messung, die vor jeder
Entscheidung stehen muss. P10 zieht beides vor den Bau. **Tor:** P10.5 startet erst, wenn der Nikinger das Register freigibt.

## 2. Neue Wünsche des Nikingers (2026-10-08, wörtlich sinngemäß, Vertiefung von mir)

### 2.1 Responsivität und Performance — überwiegend clientseitig
- **Messen vor Bauen:** `/items` und `/overview` über Funnel im **Browser des Nikingers** (Netzwerk-Tab, drei Wechsel). Die Wegwerf-Messung vom
  2026-10-08 (`probes/p9_feedback_b8_messung.json`) zeigt nur die Struktur: ein Space-Wechsel = **eine** Anfrage, 12–20 ms lokal; die Wartezeit ist
  die Netzstrecke (P9-15: `/overview` ~3,1 s).
- **Kandidaten** (alle ungeprüft): Zwischenspeicher je Space (alte Liste sofort zeigen, im Hintergrund auffrischen — berührt Auswahl, offenen
  Editor, Konfliktpfad) · optimistische Anzeige nach Schreibvorgängen · Vorabladen beim Überfahren eines Space-Eintrags · weniger parallele
  Abrufe beim 20-s-Poll (`/overview` + `/spaces` zusammenfassen oder nur bei geändertem Token) · Listen-Virtualisierung bei großen Spaces ·
  `ui_budget` (heute ~165 KB) als Zielgröße beibehalten.
- **Gleichstand der Ziele zuerst:** eine feste Messanordnung (Instrument, Anzahl Läufe, Wegwerf-Last) und **Zielwerte** werden in P10 festgelegt,
  nicht in P10.5 nach dem Bauen.
- **Bruchstelle:** Hard Rule 3 (kein Write ohne `version`) — ein Zwischenspeicher darf nie eine alte `version` in einen Schreibvorgang tragen.

### 2.2 Visuelle Kleinigkeiten
- **Eigene 404-Seite** im UI-Stil (nur für Browser-Pfade unter `/ui/…`; die API und `/mcp` bleiben bei JSON-Fehlern, Maschinenleser dürfen keine HTML-Seite
  bekommen). Kein Leck: sie nennt weder Pfade noch Spaces.
- **Logo einbinden** — **ausdrücklich vorläufig**: ein einziger Austauschpunkt (eine SVG-Datei plus Favicon), damit das spätere Logo ohne
  Codeänderung ersetzt wird. Orte: Rail-Marke, Login-Seiten, Favicon, 404-Seite.
- **Tab-Titel je Ansicht** (das ist **V120**, seit P8 „offen gehalten mit Absicht"): z. B. `sharefyx – Startseite`, `sharefyx – <Space>`,
  `sharefyx – Dokument bearbeiten`, `sharefyx – Einstellungen`, `sharefyx – Anmeldung`. Offene Entscheidung: **deutsch oder englisch** (die
  Oberfläche ist deutsch; der Wunsch war englisch formuliert). Titel kommen aus `document.title` (Text, nie HTML), der Item-Titel wird gekürzt.

### 2.3 Editor: Schluss mit Vorschau-/Bearbeiten-Modus — arbeiten wie in Word/Excel
- **Auftrag:** ein Menschen-Editor ohne Moduswechsel; Formatierung sichtbar während des Schreibens; „echte" Formatierung, wenn möglich.
- **Die harte Randbedingung** (die einzige, die das Ganze kippen kann): **die Datei bleibt Markdown + YAML-Frontmatter**, und Claude liest sie als
  solche (Kernprinzip: der Server ist dumm, Dateien sind die Wahrheit). Alles, was der Editor anzeigt, muss **verlustfrei** nach Markdown zurück.
- **Drei Stufen, aufsteigend im Risiko** (zur Entscheidung):
  1. **Live-Darstellung über Markdown** (WYSIWYG-artig: Überschriften, fett/kursiv, Listen, Zitate, Code, Links, Tabellen, **To-do-Kästchen**).
     Kein Formatwechsel, kein P1-Eingriff. To-do-Kästchen stehen schon auf der P9-§15-Liste und brauchen den Schreibpfad (Hard Rule 3).
  2. **Erweiterte Formatierung** (Farben, Ausrichtung, Schriftgröße): in reinem Markdown **nicht ausdrückbar**. Entweder verzichten, oder ein
     definierter Markdown-Zusatz (HTML-Spans/Attribute) — das öffnet das Dateiformat, **alle MCP-Clients lesen es mit**, und es wäre die **elfte
     P1-Contract-Öffnung**. Nur mit ausdrücklicher Nikinger-Entscheidung.
  3. **Excel-artige Tabellen** (Zellen, Formeln): eigener Item-Typ statt Markdown-Tabelle; das ist Funktionsumfang und eher **P11** als Baustellen-Abschluss.
- **Offene Fragen:** Bibliothek (Eigenbau scheidet bei Tabellen und Undo praktisch aus; die Größenwerte von `ui_budget` entscheiden mit) ·
  gleichzeitiges Bearbeiten durch zwei Personen bleibt `ConflictError` (kein Zusammenführen in P10) · Tastaturführung und Barrierefreiheit ·
  was passiert mit Items, die der Editor nicht verlustfrei darstellen kann (Rohmodus als Notausgang).
- **Empfehlung:** Stufe 1 in P10.5, Stufe 2 und 3 als **benannte Entscheidung** des Nikingers im Register, nicht stillschweigend.
- **[2026-10-16, Step 0]:** Stufe 1 hebt das gelockte **P5-U** auf („Markdown-Textarea + Formatierhilfen, kein WYSIWYG") — nur als
  datierte Nikinger-Entscheidung (Register ED-1, D-4).

### 2.4 Anbieter-unabhängig (Nikinger 2026-10-16, „provider agnostic")
- **Ziel:** jeder standardkonforme MCP-Client kann sich verbinden, nicht nur claude.ai — auf Server-/Connector-Ebene. Es blockiert
  keinen Schritt, nur den Abschluss von P10.5; Abnahme: ein Nicht-Claude-Client führt `list_spaces` live aus (Lock P10-C).
- Modell-Routing aus der Endvision bleibt Client-Seite (frühestens P11), nie im Server — Kernprinzip. Register PA-1–PA-7.

### 2.5 Karten-Umbau (Nikinger 2026-10-16)
- Stil (p8x §2.2), Layout über den Reload merken, Interaktion (Suche, Filter, Titel), „etwas gehirnartiger"; Einklappen (§2.5) nicht
  gewählt. Aus drei Entwürfen **C Gehirnkarte** gewählt, drei Stile C1–C3 zur Wahl (Register KA-1–KA-5, D-1b).

## 3. Bekannte Baustellen aus Phase 9 (Erbe, nach Herkunft)

| Herkunft | Posten | Anmerkung |
|---|---|---|
| Block feedback | **Ordner in Team-Spaces anlegen** | heute gesperrt; Rechte-Frage wie E1a |
| Block feedback | **MCP `update_item`: Ordner verschieben in Team-Spaces** | Claude kann dort nicht verschieben, die Web-Oberfläche seit E1a schon |
| Block feedback E2 | **Space umbenennen** | V194: was verweist auf den Namen (Verzeichnis, `.share.yml`, Mitglieder, Index, Links, Auth)? |
| Block feedback E3 | Editor-Umbau | → §2.3 |
| Block feedback B8 | Latenz Space-Wechsel | → §2.1 |
| P9-Plan §15 | Logo + einheitliche Design-Vorlage | → §2.2 (Vorlage: Erweiterung der Auswahl-Konvention v3, nicht ihr Ersatz) |
| P9-Plan §15 | `doing` auf der Übersicht hervorheben · Assignee-Picker und -Filter | Darstellung |
| P9-Plan §15 | Verschieben in fremde Spaces | Rechte-Thema |
| P9-Plan §15 | Body-Volltextsuche (Q1) · Rechteverwaltung über MCP (P6-M) · **FastMCP 4 / V79** · Realtime · Light-Mode (P5-X) · Bulk-Append-Werkzeug · Ordner umbenennen · `_trash/` räumen · ROADMAP-Straffung | Ledger, unverändert offen — jeder braucht ein Urteil: bauen / verwerfen / **P11** |
| `p8x_ui_polish_notes.md` | Karten-Stilumbau §2.2, Karte einklappen §2.5, verbundene AI-Sessions §10.8, Radien-/Auswahl-Vereinheitlichung §10.1–§10.7 | |
| **Closeout P9 (2026-10-08)** | zehn Posten, die hier noch fehlten (Tailnet-ACL 8765, LAN-Ports, `/overview`-Schleife, leere Space-Liste, `mcp`-Pin, Vision-Ersatz, Legacy-Fenster, Kontrast, Ausführer, `created_by`) | `PHASE9_CLOSEOUT_HANDOVER.md` §4 |
| Matrix | **12 ⚠️ und 1 ⬜** (Stand Closeout; vorher 13 ⚠️) (P9-13/V150, zweites Konto — ein *Termin*, kein Blocker) · P9-22 deferred · P9-127 (Enter-Stationen für die übrigen Overlays) | jede Zeile → ✅ / gegenstandslos / ausdrücklich verschoben |
| **Nikinger-Entscheidung 2026-10-08** | **Mobil ist keine Aufgabe dieser Oberfläche.** Desktop-Untergrenze **1024 px**; eine Handy-App wird ein eigenes Design (Zusatz, kein Ersatz). | streicht §10.9 „Hochkant-/Handy-UI" aus der Liste; P9-126 ist darauf eingeengt |

## 4. Was P10 (Bestandsaufnahme) liefert

1. **Baustellenregister** — eine Tabelle, je Posten: Herkunft · Größe (S/M/L) · Risiko (berührt Schreibpfad / Dateiformat / Rechte?) ·
   Entscheidung nötig? · Ziel (**P10.5** / **P11** / verworfen). Grundlage sind §2 und §3, ergänzt um eine Suche nach `TODO`/`FIXME`, die
   `## Backlog`-Sektion des P9-Heads und alle `[VERIFY]`-Zeilen mit Stand ⬜.
2. **Messwerte** für §2.1 (Ladezeiten über Funnel am Browser des Nikingers) und die **Zielwerte**.
3. **Nikinger-Entscheidungen** gesammelt: Editor-Stufen (§2.3), Tab-Titel-Sprache, Ledger-Posten bauen/verwerfen, Reihenfolge.
4. **Plan P10.5** mit Locks, Abnahmezeilen und Blockreihenfolge, im Format der bisherigen Blockpläne (Probe + Gegenlauf je Block).

**Abgrenzung zu P11:** ein Posten, der eine **neue Fähigkeit** schafft (neuer Item-Typ, Tabellenkalkulation, Echtzeit-Zusammenarbeit), ist P11 —
auch wenn er auf dieser Liste landet. P10.5 schließt nur, was heute **angefangen, kaputt, unmessbar oder ungeklärt** ist.

## 5. Note from other project — `eurofyx-fleet` (2026-10-11)

> **Absender:** Claude Code im Repo `eurofyx-fleet` (privates Zentral-Infra-Repo des Nikingers), Session S3.
> **Einzige Änderung an diesem Repo:** genau dieser Abschnitt plus die `updated:`-Zeile der Card. Ausdrücklich freigegeben vom Nikinger (2026-10-11), sonst gilt dort die Regel „nie in Projekt-Repos schreiben". **Nicht committet** — der Commit gehört in die Sharefyx-Session.
> **Kein Auftrag an P10.** Nur Befunde und zwei Entscheidungen, die bei Sharefyx liegen.

**Was geschlossen ist:** P9-Closeout §4.1 (VPS im Tailnet) ist durch **Fleet Block 1** geschlossen. Die Tailnet-Policy erlaubt der VPS (`tag:sharefyx-edge`) jetzt **nur** `VM 200 : tcp 8765`. Vorher war der P9-Grant wirkungslos, weil ein allow-all-Grant mit `src: "*"` auch die VPS einschloss. Die Policy-Datei liegt im Repo `eurofyx-fleet` (`tailnet/policy.hujson`) und wird von dort in der Admin-Konsole eingespielt.

**Gemessen am 2026-10-11:**
- Von der VPS aus sind SSH auf die anderen Tailnet-Knoten, RDP auf den Windows-Rechner sowie die Weboberflächen von Router und Proxmox im LAN **gesperrt**; die Relay-Strecke zu VM 200 läuft (`/health` 200).
- `https://sharefyx.eurofyx.com` und der Tailscale-Funnel liefern von außen `/health` 200, `/ui/login` 200, `/mcp/` 401 — unverändert gegenüber dem Deploy-Smoke.
- Gegenlauf: Ohne den VPS-Grant lehnt die Konsole die Policy ab (`want: Accept, got: Drop`). Es gab keine Betriebsunterbrechung.

**Was P10 wissen sollte:**
1. **Zwei öffentliche Eingänge** (VPS/nginx und Tailscale Funnel). Härtung auf nginx/VPS (Rate-Limit, TLS-Policy) schützt den Funnel-Pfad **nicht**. Der Funnel bleibt bewusst aktiv: Der Firmen-Proxy des Nikingers blockt die Sharefyx-Domain, `*.ts.net` aber nicht.
2. **Offen bei Sharefyx, nicht bei Fleet:** ob das MacBook den Relay-Port erreichen darf. Nutzergeräte behalten heute weiterhin vollen Zugriff auf VM 200.
3. **Host-Header:** Der Relay antwortet auf `/health` mit **400 „Invalid host header"**, wenn man ihn über die Tailnet-IP anspricht. 200 gibt es nur mit `Host: 127.0.0.1:8765`. Das ist Anwendungsverhalten und kein Netzfehler. Fleet-Healthchecks setzen den Header; wer von außen misst, sollte das wissen.
4. **Funnel-Regel:** Sollte VM 200 jemals mit einem Tag versehen werden, verliert sie den User-Owner. Dann muss das Ziel der Funnel-`nodeAttrs` auf diesen Tag zeigen, sonst fällt der Funnel weg. Fleet taggt VM 200 derzeit **nicht**.
5. **Nur zur Info:** Fleet plant ein Backup-Ziel außerhalb von Proxmox (Block „2b"). An Sharefyx und an dessen Backup (`sharefyx-backup.service`) ändert sich dadurch nichts; Entscheidungen dazu stehen noch aus.

## 6. Note from other project — `eurofyx-fleet` (2026-10-11, S6)

> **Absender:** Claude Code im Repo `eurofyx-fleet`, Session S6.
> **Einzige Änderung an diesem Repo:** genau dieser Abschnitt plus die `updated:`-Zeile der Card. Ausdrücklich freigegeben vom Nikinger (2026-10-11, nach dem Präzedenzfall aus §5). **Nicht committet**, der Commit gehört in die Sharefyx-Session.
> **Kein Auftrag an P10.** Ein Befund mit Vorschlag, die Entscheidung liegt bei Sharefyx.

**Befund: `sharefyx-tail-proxy` landet bei jedem geordneten Stopp in `failed`.**
- Gemessen am 2026-10-11 beim Gegenlauf des Fleet-Healthchecks (`systemctl stop sharefyx-tail-proxy`, danach `start`): `socat` beendet sich auf SIGTERM mit **Exit-Code 143**. systemd wertet das als Fehler (`Failed with result 'exit-code'`), die Unit steht danach auf `failed`, obwohl der Stopp gewollt war.
- Folge: Jeder Reboot, jedes Deploy mit Neustart und jeder manuelle Stopp hinterlässt eine `failed`-Unit. Wer `systemctl --failed` als Gesundheitssignal nutzt (Fleet tut das in `vm-dev.sh`: „0 failed units“), sieht einen Fehlalarm. Echte Ausfälle des Relays sind davon nicht mehr zu unterscheiden.
- Der Dienst selbst lief nach `start` wieder normal, `/health` über das Relay war 200, `sharefyx-mcp` blieb unberührt.

**Vorschlag (Sharefyx-Entscheidung):** In `phase3_edge/systemd/sharefyx-tail-proxy.service` im Abschnitt `[Service]` ergänzen:

```ini
SuccessExitStatus=143
```

Hinweise dazu:
- Die installierte Unit unter `/etc/systemd/system/` ist eine Kopie, also braucht es danach den üblichen Deploy-Weg (Kopie + `systemctl daemon-reload`). Ein Neustart des Relays ist dafür nicht nötig, die Direktive wirkt beim nächsten Stopp.
- `phase9_hardening/tests/test_tail_proxy.py` vergleicht die Härtung mit der MCP-Unit. Falls der Test die `[Service]`-Direktiven vollständig vergleicht, muss er diese Zeile kennen.
- Gegenlauf-Idee: nach dem Deploy `systemctl stop` + `start`, danach darf `systemctl is-failed sharefyx-tail-proxy` **nicht** `failed` melden.

**Korrektur zu §5, Punkt 1:** Auf der VPS läuft **Caddy**, nicht nginx (Fleet hat das am 2026-10-11 gemessen). Die Aussage bleibt gleich: Härtung auf dem VPS-Reverse-Proxy schützt den Funnel-Pfad nicht.

## 7. Note from other project — `eurofyx-fleet` (2026-10-13, S9)

> **Absender:** Claude Code im Repo `eurofyx-fleet`, Session S9.
> **Einzige Änderung an diesem Repo:** genau dieser Abschnitt plus die `updated:`-Zeile der Card. Ausdrücklich freigegeben vom Nikinger (2026-10-13, nach dem Präzedenzfall aus §5/§6). **Nicht committet**, der Commit gehört in die Sharefyx-Session.
> **Handlungsbedarf:** Die Live-Datei auf der VPS weicht jetzt von `phase9_hardening/step_a/Caddyfile` ab. Sharefyx entscheidet, ob die Quelle nachzieht. Sonst geht die Änderung beim nächsten Einspielen verloren.

**Befund: kurze Ausfälle der öffentlichen Domain durch Caddys Standard-Wartezeit.**
- Der Fleet-Wächter auf der VPS (alle 5 min `/health` über Caddy → Tailnet → Heim-VM) meldete am 2026-10-13 um 04:30 Berlin DOWN, um 04:40 wieder UP. Im Caddy-Log stehen um 04:30:04 und 04:35:04 `dial tcp <Heim-VM>:8765: i/o timeout`.
- Ursache: VPS und Heim-VM erreichen sich **nie direkt**, nur über Tailscale-DERP-Relays (`tailscale ping`: „direct connection not established“, vermutlich CGNAT am Heimrouter). Nachts lagen beide auf verschiedenen Relays, und die Heim-VM hatte ca. 2 s Relay-Latenz. Der Verbindungsaufbau dauerte länger als Caddys **Standard-`dial_timeout` von 3 s** → Fehler an den Aufrufer. Um 04:35 wechselte die Heim-VM auf dasselbe Relay, danach lief es wieder.
- Dieselben Timeouts stehen schon früher im Caddy-Log (06.10. 18:31 und 19:02, 11.10. 18:58), also vor dem Wächter. Wer in diesen Momenten die Domain aufrief, bekam einen Fehler.
- Die App selbst war gesund: `/health` lokal auf der Heim-VM durchgehend 200. Kein Zusammenhang mit Backups oder Fleet-Läufen.

**Live auf der VPS geändert (Fleet, 2026-10-13, Entscheidung Nikinger):** im Site-Block statt der einzeiligen `reverse_proxy`-Direktive:

```caddyfile
reverse_proxy <Heim-VM>:8765 {
	transport http {
		dial_timeout 10s
	}
	lb_try_duration 15s
	lb_try_interval 1s
}
```

Hinweise dazu:
- `dial_timeout 10s` gibt dem Aufbau über das Relay Zeit. Mit `lb_try_duration` und `lb_try_interval` versucht Caddy es bei einem Hänger bis 15 s lang erneut, im Abstand von 1 s (bei einem einzigen Upstream wird derselbe wieder gewählt).
- `caddy validate` ok, danach `systemctl reload caddy` (kein Neustart). Die aktive Config per Admin-API zeigt 10 s / 15 s / 1 s, `/health` ist lokal und öffentlich 200. Sicherung der alten Datei liegt auf der VPS neben dem Caddyfile (`.fleet-bak-20261013`).
- Der Rest des Caddyfile (Kopf-Kommentar, Logging, kein HSTS, kein `admin off`) ist unverändert.
- Gegenlauf-Idee für Sharefyx: nach dem Einspielen aus der Quelle `curl localhost:2019/config/` und prüfen, dass `dial_timeout`/`try_duration` gesetzt sind.

**Nur zur Info, kein Sharefyx-Thema:** Der Fleet-Wächter meldet jetzt erst nach einem zweiten Fehlversuch 30 s später, damit einzelne Relay-Hänger keinen Alarm auslösen. Die eigentliche Ursache (kein direkter Pfad) liegt am Heimrouter bzw. an der Mobilfunkleitung.

**[2026-10-16 Korrektur, Sharefyx-Session]:** Die Quelle heißt `phase9_hardening/step_a/Caddyfile.template`, nicht `…/Caddyfile`; ihre
Zeile 65 trägt noch die einzeilige `reverse_proxy`-Direktive. Register BT-1 (dringend), V199.

## 8. Note to other project — `eurofyx-fleet` (2026-10-19)

> **Absender:** Claude Code im Repo `savefxy` (Sharefyx), Session 2026-10-19. **Empfänger:** die Fleet-Session, die
> Claude Code + GLM (Z.ai Coding Plan) als Ausführer integriert (Nikinger-Auftrag 2026-10-19). Volltext mit allen
> Zahlen: [`phase10_executor_review_glm.md`](./phase10_executor_review_glm.md).

**BLUF.** Das 5-h-Kontingent des Z.ai-Plans starb an **fehlender Kompaktierung**, nicht am Modell: opencode deklariert
`glm-5.3`/`glm-5.3-flash` mit **1 M Kontext** und kompaktiert deshalb praktisch nie — eine Session lief 12 h mit
Kontext-Median **326 K** je Aufruf (278 Aufrufe, 86,1 M Tokens). Für die Integration heißt das: **Kontext deckeln
(~200 K), eine Session je Arbeitsschritt, GLM-Text gegenlesen.** Flash taugt nicht für mehrstündige Arbeit; GLM 5.3
(Default) ist brauchbar.

**Befunde, die die Integration betreffen:**
- **Kompaktierung.** Claude Code budgetiert ein unbekanntes Modell hinter fremder `ANTHROPIC_BASE_URL` laut Berichten mit
  200 K und kompaktiert dort — das wäre der gewünschte Deckel. `[VERIFY]` per `/context` im ersten Lauf; falls Claude Code
  dem Modell 1 M glaubt (`[1m]`-Suffix im Modellnamen), ist man wieder beim opencode-Fehler.
- **Memory/Kontext.** opencode sah die Claude-Code-Memory (`~/.claude/projects/…/memory/`) **nicht** (0 Treffer in beiden
  Sessions). Mit Claude Code als Harness kommt sie automatisch mit — das war der größte Qualitätshebel (u. a. „Vision
  läuft auf CT 111", „Testumgebung ohne `SHAREFYX_*`").
- **Endpunkt.** Anthropic-kompatibel `https://api.z.ai/api/anthropic` + `ANTHROPIC_AUTH_TOKEN`; Modell-Slots
  (Opus/Sonnet/Haiku) auf GLM mappen. Exakte Variablen `[VERIFY]` an docs.z.ai/devpack/tool/claude. Token gehört in den
  Keyring bzw. eine Shell-Funktion, **nicht** in eine Datei im Repo (Sharefyx Hard Rule 1).
- **Abrechnung (Inferenz).** Z.ai zählt „Prompts" ≈ 15–20 Modellaufrufe und gewichtet GLM-5.x mit Token-Multiplikatoren;
  Flash machte ~93 Aufrufe je Nutzer-Nachricht. Aufrufe × Kontext ist die Größe, die man begrenzen muss.
- **Langzeilen-Falle (Sharefyx-spezifisch).** Die Sharefyx-Doku hat Absätze als Einzelzeilen: `head -60` lieferte 41 K
  Zeichen. Ausgaben dort mit `| cut -c1-200` oder `head -c` begrenzen.
- **Qualität.** Flash: Vision-Container trotz Plan + MCP-Konfiguration übersehen, falsche Statusaussage, kaputte
  Doku-Rotation. Beide GLM-Varianten: Token-Glitches in committetem Text (`ROTETING`, `tirelessly窗外`) — ein Gegenlese-
  Schritt vor jedem Commit gehört in den Ablauf.
- **Remote Control** (claude.ai ↔ lokale Claude-Code-Session) hängt nach unserem Verständnis an einem claude.ai-Login; ein
  gesetztes `ANTHROPIC_AUTH_TOKEN` hat Vorrang vor dem Login. Ob Remote Control mit Z.ai-Endpunkt geht, ist **ungeprüft**
  `[VERIFY]` — Erwartung: eher nein; dann bleibt für Fernbedienung Tailscale + SSH/tmux.

**Handlungsbedarf Fleet:** keiner an Sharefyx. Sharefyx fährt den ersten Lauf unter Claude Code + GLM als gedeckelten
Vergleich (Phase-10-Head, Session-Block 2026-10-19 „Nächster Schritt") und meldet `/context`- und Remote-Control-Befund zurück.
