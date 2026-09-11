---
status: live
purpose: reusable techniques for turning a "needs a human / needs a real connector" Sichtprüfung into a scripted, throwaway-verifiable one
read-when: before assuming a Sichtprüfung criterion is structurally blocked — check here first whether a throwaway-instance substitution already exists as a pattern
detail: L2
up: ../INDEX.md
down:
  - ./sichtpruefung_automation_tooling.md   # separate concern: plugins for VIEWING screenshots (Claude Code vs. OpenCode), not for RUNNING checks
updated: 2026-09-11 (§5 neu — Nikinger-Vorgabe: Schnellzugriff-Verzeichnis `screenshots_latest/` am Repo-Root als Symlink-Komfort auf die Originale in `docs/screenshots/<phase>_*`, dazu die Pflicht „Dateiname + Checkkriterium im Chat nennen" bei jeder Sichtprüfungs-Verifikation; volle Beschreibung in §5, README mit Tabelle + Checkkriterien liegt in `screenshots_latest/README.md` — Beispiel-Befüllung Phase 8.6 Block B mit vier Screenshots: `01_overview_logout_caution.png` / `02_list_hover_quiet_selection.png` / `03_editor_archive_caution.png` / `04_account_dialog_navigation.png`) | 2026-09-09 (P8.5-6-Folge-Smoke — Bracket-Pfad live-verifiziert per Mini-Smoke gegen v3ritt-Wegwerf mit `itm_b8b989a1` „Vercel [Hosting]" + Vorschau-Panel-Screenshot, §1-Beispiel-Absatz aktualisiert mit dem Resolution-Pfad; Phase 8.5 vollständig abgeschlossen **Bilanz 20 ✅ · 0 🟡 · 0 ⬜**) | 2026-09-09 (vier neue Konventionen für Sichtungs-Skripte + -Output: §1 Vorschau-Pflicht bei klickbaren Links, §2 Wer validiert was [Code/auto = M3 oder Claude Code, visuell = Nikinger-Auge], §3 Deploy erst nach Testauswertung, §4 Screenshots im Chat präsentieren sobald opencode-vision installiert ist; Nikinger-Feedback 2026-09-09 aus der Sichtung der 10 P8.5-🟡-Zeilen — P8.5-6 bleibt 🟡 wegen fehlendem Vorschau-Screenshot des Bracket-Pfads) | 2026-09-08 (erste Fassung, Phase-8.5-Sichtprüfungs-Sub-Session)
---

# Sichtprüfungs-Automatisierung — Techniken (nicht: Werkzeuge)

> Für "was installiere ich, damit ich Screenshots sehen kann" siehe die Schwester-Datei
> [`sichtpruefung_automation_tooling.md`](./sichtpruefung_automation_tooling.md). Diese Datei
> ist das Gegenstück: **wie** man eine Sichtprüfung, die auf den ersten Blick einen echten
> Menschen oder einen echten Connector braucht, trotzdem skriptbar macht — mit konkretem,
> lauffähigem Code aus einer echten Session, nicht nur der Idee.

## Konventionen für Sichtungs-Skripte und -Output (Nikinger-Feedback 2026-09-09)

Vier Regeln aus der Phase-8.5-Sichtungs-Praxis (Block C 2026-09-04 + Sichtung 2026-09-09),
verbindlich für alle künftigen Sichtungs-Runden. Vor jeder neuen Runde prüfen, ob eine der
vier das Vorgehen verändert — und ggf. Skripte + Walkthroughs nachziehen.

### 1. Vorschau-Pflicht bei klickbaren Links

Wenn eine Sichtung **klickbare Links** prüft (Link-Picker-Einfügen, Markdown-Rendering mit
`[…](…)`, Body-Links), genügt ein Screenshot der **Edit-Ansicht** nicht. Der Nikinger muss
im Bild sehen können, dass der Link **gerendert als klickbarer Hyperlink** erscheint — sonst
liest er nur den Markdown-Quelltext und kann nicht entscheiden, ob das Rendering
funktioniert. Konkret: das Vorschau-Panel muss im Screenshot sichtbar eingeblendet sein (oder
eine zweite Renderer-Screenshot-Variante vorliegen).

Lehre aus Phase 8.5: D4 (2026-09-06) hat den Bracket-Bug in `markdown.js` gefunden, weil
der Markdown-Source-Escape korrekt war (`\[Vercel\]`), aber der Renderer die eckige Klammer
im Titel als Ende des Link-Texts interpretierte und der Link damit visuell zerbrach. **Wäre
der damalige Smoke mit eingeblendetem Vorschau-Panel gelaufen, wäre der Bug schon im
Block-C-Smoke aufgefallen, nicht erst in der manuellen D4-Sichtprüfung.** P8.5-6 blieb
deshalb bis 2026-09-09 🟡 (kein Vorschau-Screenshot des Bracket-Pfads vorhanden, nur
statische Tests + Code-Review); der P8.5-6-Folge-Smoke selben Tags hat die Lücke
geschlossen — Mini-Smoke gegen v3ritt-Wegwerf mit Item `itm_b8b989a1` „Vercel [Hosting]"
+ Vorschau-Panel-Screenshot bestätigt den Bracket-Fix live, Screenshot
`docs/screenshots/p856_bracket_preview.png` zeigt „Vercel [Hosting]" als klickbaren
blauen Hyperlink, programmatische Quittung per Regex auf
`<a href="#item/itm_b8b989a1">Vercel [Hosting]</a>` True.

### 2. Wer validiert was (Code / Wegwerf / Live / Visuell)

| Art | Wer validiert | Beweis-Material |
|---|---|---|
| **(C) Code/Test** | **vollständig durch M3 oder Claude Code** — kein Nikinger-Schritt nötig, sofern im Abnahme-Archiv dokumentiert | grünes `pytest` / `node --check` / `bash -n` + statischer-Test-Beleg |
| **(W) Wegwerf + Nikinger-Sichtung** | M3 fährt den Smoke, Nikinger sichtet Evidenz | Smoke-Skript-Output + Screenshots (mit Vorschau bei Links, s. Regel 1) |
| **(L) nur live** | Nikinger am echten System | Connector-Output, Browser-Session |
| **Visuelle Sichtungen** (Markup, Layout, Rendering, Animation) | **immer Nikinger-Auge**, bis das OpenCode-Vision-Plugin (P8.6 first step) installiert ist und M3 die Bilder nativ mit-vorlegen kann | Screenshots — ab P8.6 direkt im Chat, vorher als Dateipfade + Was-zu-validieren |

### 3. Deploy erst nach Testauswertung — nicht umgekehrt

Reihenfolge für künftige Phasen (P8.6, P9) ist **immer**:

1. **Wegwerf-Instanzen** (W-Smokes), **statische Tests**, Build-Skripte, `ui_budget.py` laufen
   gegen einen frischen Wegwerf-Build, dessen `git checkout` identisch zum geplanten
   Release-Stand ist (Hard Rule 9-konform über PID-Datei, niemals `pkill -f`).
2. **Nikinger sichtet** die Evidenz (Skript-Logs, Screenshots, Console-Cross-Checks).
3. Stand ist „sicher" — **dann** erst der Deploy als **Nikinger-Aktion** (Hard Rule 9:
   niemals von opencode/M3 oder Claude Code ausgelöst).

Nicht: Deploy → Tests → vielleicht Rollback. Der Phase-8.5-Vorlauf fährt genau dieses
Muster — D3-Health-Gate (8/8 grün vor D2-Deploy) + Sichtungs-Block C/D → erst danach der
eigentliche Deploy durch den Nikinger.

### 4. Screenshots im Chat präsentieren (**nur Claude Code** — in OpenCode nicht möglich, 2026-09-11)

Sobald das OpenCode-Vision-Plugin (`DavidEasden/opencode-vision`, siehe
[`sichtpruefung_automation_tooling.md`](./sichtpruefung_automation_tooling.md)) als erster
Punkt in P8.6 installiert ist, gilt für künftige Sichtungs-Runden dasselbe wie bei Claude
Code: jeder Screenshot wird hier im Chat präsentiert, darunter steht **eine kurze Zeile „Was
du validieren sollst"**. Der Nikinger sichtet dann direkt am Bild — ohne den Umweg über
das Dateisystem. **Bis das Plugin installiert ist**, müssen Screenshots über das Dateisystem
geöffnet werden, und der M3/Claude-Code listet sie als Dateipfade + kurze
Was-zu-validieren-Beschreibung auf.

> **[2026-09-11 Korrektur]** Diese Konvention ist in OpenCode **nicht erfüllbar** und war es nie —
> das Plugin ändert daran nichts. OpenCodes Web-UI (1.18.30) rendert Bild-Attachments
> ausschließlich an *User*-Nachrichten (`user-message-attachment-image`); für Assistant- bzw.
> Tool-Result-Parts existiert kein Bild-Slot im ausgelieferten Bundle. Bilder fließen dort nur
> Mensch → Modell, nicht zurück. Beleg + A/B-Messung:
> [`sichtpruefung_automation_tooling.md`](./sichtpruefung_automation_tooling.md) §Messbefund
> 2026-09-11. **Für OpenCode gilt daher weiter die „Bis das Plugin installiert ist"-Variante**
> (Dateipfad + Was-zu-validieren-Zeile) — dauerhaft, nicht übergangsweise. Der Ausgleich: M3 liest
> Screenshots seit demselben Befund **selbst** (`read`-Tool), muss also nicht mehr nachfragen, was
> auf dem Bild zu sehen ist.

### 5. Schnellzugriff `screenshots_latest/` + Dateinamen + Checkkriterium (Nikinger-Vorgabe 2026-09-11)

**Verzeichnis `screenshots_latest/` am Repo-Root:** enthält die Screenshots der **aktuellen**
Phase als Symlinks auf die Originale in `docs/screenshots/<phase>_*`. Single source of truth
bleibt `docs/screenshots/`; das Verzeichnis ist nur Lese-Komfort für den Nikinger —
`ls screenshots_latest/` zeigt sofort, was die laufende Phase an Sichtprüfungs-Belegen
produziert hat, ohne dass der Nikinger durch die History scrollen muss. Naming: durchnummeriert
mit kurzem Inhalt im Filename (`01_overview_logout_caution.png` o. ä.), **nicht** mit
Phase-Tag — der ändert sich beim Phasenwechsel, der Inhalt bleibt. **Rotation beim
Phasenwechsel** ist Teil der Phase-Closeout-Pflichten (alte Symlinks weg, neue anlegen,
`README.md` mit neuer Tabelle + Checkkriterien ersetzen, `updated:`-Frontmatter ergänzen —
alles im selben Commit wie die Phasen-Closeout-Doku-Updates).

**Dateiname + Checkkriterium im Chat:** wenn M3/Claude-Code einen Screenshot für eine
Verifikation erstellt, sagt es **immer** im Chat zwei Dinge dazu:

1. **Dateiname** (vorzugsweise aus `screenshots_latest/`, nicht der Original-Pfad)
2. **Kurzes Checkkriterium** (ein bis zwei Sätze, was auf dem Bild zu sehen ist)

Das gilt **unabhängig** davon, ob M3 das Bild selbst mit dem `read`-Tool beurteilen kann —
die Nikinger-Verifikation ist der Pflicht-Beleg (siehe §2 oben: „Visuelle Sichtungen
= immer Nikinger-Auge"). Auch wenn M3's eigene Bewertung positiv ist, nennt M3 die
Checkkriterien, damit der Nikinger nicht erst rätseln muss, was auf dem Bild zu sehen ist.

**Ausnahmen** (in denen M3 den Dateinamen + Checkkriterium nicht nennt):
- Wenn der Screenshot ein **reiner Build-Beleg** ist (z. B. „Smoke gegen Wegwerf X
  bestanden, hier der Konsolen-Output als Bild") und M3 den Befund bereits im Klartext
  dokumentiert hat.
- Wenn die Verifikation **programmatisch** ist (Regex auf gerenderten HTML-Output
  o. ä.) und der Screenshot nur Anhang ist.

Vollständige Tabelle der aktuellen Screenshots + Checkkriterien liegt in
[`../../screenshots_latest/README.md`](../../screenshots_latest/README.md) — nicht dupliziert,
damit sie beim Phasenwechsel nur einmal aktualisiert werden muss.

## Der Kernsatz, bevor du eine Zeile Code schreibst

**„Blockiert" heißt oft „gegen die falsche Instanz getestet", nicht „technisch unmöglich".**
Bevor du eine Sichtprüfungs-Zeile als „nur durch den Nikinger/Fabian möglich" abhakst, prüfe:
- Braucht das Kriterium wirklich **diese eine** Instanz (z. B. „der bereits autorisierte
  Connector funktioniert nach dem Deploy noch" — das ist Identität, nicht Verhalten), oder
- braucht es nur **irgendeine** Instanz mit der richtigen Eigenschaft (z. B. „ein LLM nennt
  Titel statt IDs" — das ist Modellverhalten, jede sharefyx-Instanz mit demselben Tool-Text
  reicht) oder **zwei unabhängige Principals** (P8-8-Kategorie — zwei echte Space-Logins
  reichen, sie müssen nicht „Nikinger" und "Fabian" heißen).

Drei von vier ursprünglich als „blockiert" eingestuften Phase-8/8.5-Sichtprüfungen (P8.5-3/4,
P8-5, P8-8) fielen in die zweite Kategorie und wurden in derselben Session doch noch
automatisiert. Nur eine (P8.5-17 V105 — „der schon autorisierte Connector lebt noch") war
echte Kategorie eins.

## Technik 1 — Canvas-Instrumentierung ohne App-Code anzufassen

**Problem:** eine Canvas-Zeichnung (hier: der Force-Graph in `graph.js`) hat internen State
(`implicitEdges`, Tag-Kanten-Anzahl), der nicht `export`iert wird — man kann ihn nicht per
`page.evaluate()` auslesen, ohne den Quellcode zu ändern.

**Lösung:** `context.add_init_script()` (Playwright) patcht
`CanvasRenderingContext2D.prototype.setLineDash`/`.stroke` **bevor** irgendein App-Skript
lädt. Jeder `stroke()`-Aufruf der echten App wird gezählt, kategorisiert nach dem zuletzt
gesetzten `setLineDash`-Muster (`[4,4]` = Tag-Kante, `[1.5,3]` = Ordner-Kante, `[]` = explizite
Kante — das sind die tatsächlichen Werte aus `graph.js :: drawEdges()`). Null Zeilen App-Code
geändert, trotzdem eine exakte Zählung des internen Zustands.

**Falle: eine Dauerschleife zeichnet jeden Frame neu.** Ein Zeitfenster (`wait_for_timeout`)
zählt automatisch **mehrere** Frames, nicht einen — der erste Versuch ergab 310 statt 10
gezeichneter Tag-Kanten (31 Frames × 10). Zwei Auswege, die zweite ist robuster:
- Ein einzelner rAF-Tick abwarten (`await page.evaluate("() => new Promise(r =>
  requestAnimationFrame(() => requestAnimationFrame(r)))")`) — funktioniert nur, wenn die
  eigene Zählschleife exakt mit dem Browser-rAF synchron läuft, was bei mehreren
  unabhängigen rAF-Ketten nicht garantiert ist (in dieser Session unzuverlässig).
- **Der robustere Weg:** eine bekannte Konstante (hier: die Anzahl expliziter Kanten aus
  `/api/v1/graph`, unabhängig vom Toggle-Zustand) wird JEDEN Frame exakt einmal gezeichnet.
  `gemessene_plain_calls / explizite_kanten_anzahl` = Anzahl erfasster Frames,
  `gemessene_tag_calls / frames` = Tag-Kanten pro Frame, **unabhängig von der Fenstergröße**.
  Funktioniert auch, wenn das Fenster zufällig 3, 19 oder 34 Frames erwischt.
- **Zweite Falle dabei:** direkt nach einem Toggle-Klick können ein paar Übergangs-Frames
  noch 0 zeichnen (bevor `rebuildImplicitEdges()` durchgelaufen ist) — das zieht den Mittelwert
  unter den echten Wert. Fix: den Zähler-Reset NACH einer kurzen Anlaufzeit (200–300 ms) nach
  dem Klick setzen, nicht davor.

Volles Beispiel: `phase8_ui_graph/scripts/p8_21d_tag_cutoff_probe.py`.

## Technik 2 — CDP-Medien-Emulation für `prefers-reduced-*`

`ctx.new_cdp_session(page)` → `cdp.send("Emulation.setEmulatedMedia", {"features": [...]})`
schaltet `prefers-reduced-motion`/`prefers-reduced-transparency` um, ohne einen echten
Browser mit echtem OS-Setting zu brauchen. Danach `getComputedStyle()` auf die betroffenen
Elemente lesen (z. B. `backdropFilter`) — nicht raten, ob der Fallback gegriffen hat.
Beispiel: `phase8_ui_graph/scripts/p8_16_glass_fallback_probe.py`.

## Technik 3 — OAuth-Dance gegen eine Wegwerf-Instanz, ohne Browser

**Problem:** ein Sichtprüfungs-Kriterium braucht ein echtes, authentifiziertes Bearer-Token
(für einen MCP-Tool-Aufruf), aber du hast keinen Browser mit Nikinger-Login zur Verfügung —
oder willst absichtlich NICHT die echten Produktions-Credentials anfassen.

**Lösung:** der komplette OAuth-2.1-Flow (Discovery → Dynamic Client Registration → PKCE →
Authorize-Formular → Token-Tausch) ist reines HTTP, keine Browser-Notwendigkeit — die
"Consent-Seite" ist nur ein `<form>`, das `httpx` genauso ausfüllen kann wie ein Browser.
`phase4_auth/scripts/oauth_smoke.py :: _run_checks()` implementiert das bereits vollständig
(inklusive Refresh/Replay-Härtung), ist aber an dessen eigene `Check`-Buchführung gekoppelt —
für eine einmalige Token-Beschaffung reicht ein **schlankerer Nachbau** derselben sechs
Schritte (Discovery-GET, DCR-POST, Authorize-GET zur `request_id`, Authorize-POST mit
Space+Passwort+TOTP, Redirect-Code extrahieren, Token-POST). Reale, lauffähige Fassung:
`phase8_ui_graph/scripts/p8_8_zweitnutzer_probe.py :: _get_access_token()` — importiert nur
`authserver.crypto`/`authserver.totp` direkt, keine Kopie der P4-Sicherheitslogik.

**Wichtig, falls zwei Runden im selben 30-Sekunden-Fenster laufen:** `totp.verify()` verlangt
einen **strikt größeren** Zähler als der zuletzt akzeptierte (Replay-Schutz) — die zweite
Principal-Runde braucht `counter_offset=1`, sonst wird ihr eigener (korrekter) TOTP-Code als
Replay abgelehnt, obwohl nichts falsch lief.

## Technik 4 — zwei unabhängige Principals auf einer Wegwerf-Instanz

**Falle, die dich zuerst aufhält:** jedes bisherige `wegwerf_setup_*.py`-Skript in diesem Repo
ruft `_provision_user()` genau **einmal** — `beta`/`gamma` sind Ziel-Spaces mit
`add-member`-Freigabe, aber **keine eigenen Logins**. Ein Test, der zwei unabhängig
einloggbare Identitäten braucht (P8-8-Kategorie: „sieht Nutzer B etwas von Nutzer A, das er
nicht sehen soll"), lässt sich auf keiner bestehenden Wegwerf-Instanz fahren, ohne das Setup
zu erweitern.

**Lösung:** `_provision_user()` einfach zweimal aufrufen, mit zwei verschiedenen Space-Namen
— sie landen als zwei unabhängige Zeilen in derselben `auth.sqlite3`, jede mit eigenem
Passwort + TOTP-Secret. Vollständiges Beispiel: `phase8_ui_graph/scripts/
wegwerf_setup_p8_8.py`. Von da an ist der Rest identisch zu Technik 3, zweimal ausgeführt.

**Zweite Falle: `share_read`/`share_write` sind über KEIN MCP-Tool setzbar.**
`mcpserver/tools.py :: update_item()` weist das explizit ab — Tool-Fehlermeldung
`"visibility/share_read/share_write sind über kein MCP-Tool änderbar — das geht nur ein
Mensch in der UI"`. Das ist **kein Bug**, sondern eine bewusste, im Tool-Docstring
dokumentierte Restriktion — aber sie sitzt nur in der Tool-Schicht, nicht im Storage-Kern:
`storage.store.Store.update(item_id, version=1, share_read=[...])` funktioniert direkt. Für
ein Wegwerf-Setup (deine eigene tmp-`DATA_ROOT`, kein Trick gegen irgendetwas Echtes) ist das
der richtige Weg, eine Freigabe für den Testaufbau zu setzen, ohne einen Menschen zu
simulieren, der in einer UI klickt.

## Fehler-Signaturen, die sich wiederholen lassen (nicht neu erfinden)

`phase2_mcp/scripts/mcp_smoke.py` hat die Assertion-Muster für die zwei häufigsten
Sichtprüfungs-Fehlerfälle bereits etabliert — beide funktionieren unverändert gegen jede
Wegwerf-Instanz:
- **Fremdes, aber lesbares Item:** `"<untrusted_content" in text and f'space="{FOREIGN}"' in text`.
- **Verbotener Schreibzugriff:** `denial = await client.call_tool(..., raise_on_error=False);
  denial.is_error and "write_denied" in denial.content[0].text`.

## Wann diese Techniken NICHT greifen

Wenn das Kriterium wörtlich die **Identität** prüft, nicht das Verhalten — „funktioniert der
Connector, den der Nikinger bereits autorisiert hat, nach dem Deploy noch" — gibt es keine
Wegwerf-Substitution, die das ersetzt. Das ist der einzige Fall aus der Phase-8.5-Runde, der
tatsächlich nur durch den Nikinger selbst ging (einmalig, danach blieb der Connector über
Sessions hinweg authentifiziert).
