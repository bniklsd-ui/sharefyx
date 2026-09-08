---
status: live
purpose: reusable techniques for turning a "needs a human / needs a real connector" Sichtprüfung into a scripted, throwaway-verifiable one
read-when: before assuming a Sichtprüfung criterion is structurally blocked — check here first whether a throwaway-instance substitution already exists as a pattern
detail: L2
up: ../INDEX.md
down:
  - ./sichtpruefung_automation_tooling.md   # separate concern: plugins for VIEWING screenshots (Claude Code vs. OpenCode), not for RUNNING checks
updated: 2026-09-08 (erste Fassung, Phase-8.5-Sichtprüfungs-Sub-Session)
---

# Sichtprüfungs-Automatisierung — Techniken (nicht: Werkzeuge)

> Für "was installiere ich, damit ich Screenshots sehen kann" siehe die Schwester-Datei
> [`sichtpruefung_automation_tooling.md`](./sichtpruefung_automation_tooling.md). Diese Datei
> ist das Gegenstück: **wie** man eine Sichtprüfung, die auf den ersten Blick einen echten
> Menschen oder einen echten Connector braucht, trotzdem skriptbar macht — mit konkretem,
> lauffähigem Code aus einer echten Session, nicht nur der Idee.

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
