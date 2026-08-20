---
status: live
purpose: Phase-Head Werkzeug-Ergonomie + Bilder — Scope, harte Regeln, Modulstatus, aktueller Session-Handover
read-when: Arbeiten in phase6_5_tools_images/ oder an den in §2 des Plans genannten Dateien in mcpserver/storage/webui — zuerst lesen, zusammen mit dem neuesten Session-stopped-Block
detail: L2
up: ../CLAUDE.md
down:
  - ../docs/concepts/phase6_5_tools_images_plan.md   # voller Plan, Entscheidungen P6.5-A–P6.5-V, §0.0 gelockte N1–N6, Steps 0/A/B
  - ../phase6_shares/IMAGES_PLAN.md                  # Vorgänger-Zusatzplan, nachrangig seit 2026-08-20
  - SESSIONS_ARCHIVE.md                              # ältere Session-Blöcke, newest-first
updated: 2026-08-20 (Block B Step B3 gebaut: Markdown-Bildzweig + Editor-Upload, 818 pytest unveraendert [P5-T], Playwright 13/13 gruen und gesehen, dritte Rotation gelaufen)
---
# CLAUDE.md — Phase 6.5: Werkzeug-Ergonomie und Bilder (`phase6_5_tools_images/`)

> Kein eigenes Python-Paket (wie `phase3_edge/`, `phase6_shares/`) — Servercode bleibt in
> `mcpserver`/`storage`/`webui`. **Quelle der Wahrheit ist der Code, nicht dieses Dokument.**

---

## Mission (zuerst lesen)

Zwei Blöcke: **(A)** eine arbeitende Claude-Instanz findet ihre Werkzeuge, versteht deren
Aufgabenteilung aus der Beschreibung und zahlt keine Tausende Token für eine Versionsnummer.
**(B)** ein Bild liegt im Space, ist im Dokument sichtbar, technisch nur ein Link — und Claude
sieht seine Bytes nur, wenn ein Mensch ausdrücklich danach fragt. Unter Druck fällt Block B weg,
nie Block A (reine Beschreibungs-/Tool-Arbeit ohne Datenformatänderung).

## Scope

- **DRIN:** die fünf offenen MCP-Werkzeug-Ergonomie-Punkte (2026-08-14-Live-Feedback),
  Abschluss Block C Bilder (`storage/`-Fundament, `webui`-Routen, MCP-Asset-Tools).
- **DRAUSSEN:** Bulk-Append-Tool, Body-Volltextsuche in der Web-UI, automatische
  `_trash/`-Räumung, Space-Admin-UI (bleibt Phase 7), Rechteverwaltung über MCP-Tools,
  HEIC/SVG/PDF, serverseitiges Bild-Rendering. Volle Liste: Plan §5 „Explizit draußen".

Details, gelockte Entscheidungen P6.5-A–P6.5-V, Berührungsfläche/Tabu-Dateien, Schritt-Sequenz,
Testliste, Abnahmezeilen: `docs/concepts/phase6_5_tools_images_plan.md`.

## Modul-Status

| Block | Inhalt | Status |
|---|---|---|
| Step 0 | Haushalt/Ankündigungen | ✅ |
| Block A (Steps A1/A2/A4; A3 bewusst nicht gebaut, N3) | Werkzeug-Ergonomie (`mcpserver/tools.py`, `storage/store.py :: search(in_body=)`) | ✅ **gebaut**, noch nicht deployt — Gate A→B (echte Connector-Probe) steht aus |
| Block B Step B1 | Storage-Fundament Bilder (`storage/{files,store,models}.py`) | ✅ **gebaut** |
| Block B Step B2 | REST-Fläche Bilder (`phase5_ui/webui/{api,serializers}.py`) | ✅ **gebaut**, noch nicht deployt |
| Block B Step B3 | Web-UI Anzeigen/Einfügen (`phase5_ui/webui/static/{app.html,app.css,js/{markdown,editor}.js}`) | ✅ **gebaut**, Playwright grün+gesehen, noch nicht deployt |
| Block B Steps B4–B5 | MCP-Asset-Tools, offene Advisor-Vormerkungen | ⏳ nicht begonnen |

## Geerbte Contracts

Fünfte, benannte Öffnung des P1-Contracts (`storage/{files,store,models}.py`) — **gebaut**
2026-08-20 (Step B1), siehe `phase1_storage/CLAUDE.md` unter „Geerbte Contracts" (P6.5-T).
Details dort, nicht hier dupliziert.

---

## Session stopped — 2026-08-20 (Block B Step B3 gebaut: Markdown-Bildzweig + Editor-Upload)

**Auftrag:** direkter Anschluss an Step B2, Nikinger-Wunsch „nächster Schritt, atomar" für
Context-Checks dazwischen. Step B3 aus Plan §3: `markdown.js`s Bildzweig, Sanitizer-Erweiterung
um `IMG`, „Bild einfügen"-Knopf im Editor, `.md-body img`-CSS-Regel, Playwright-Pflichtfälle.

**Gebaut, exakt wie im Plan §3 Step B3 vorgezeichnet, zwei dokumentierte Namensabweichungen
(siehe unten):**
- `webui/static/js/markdown.js` — Bildzweig in `inlineMarkdown()` **vor** dem Link-Replace
  (P6.5-J), `resolveAssetSrc()` löst `asset:<id>` nur bei gesetztem `itemId` auf; `itemId` wird
  durch `markdownToHtml(src, options)` an alle sieben `inlineMarkdown()`-Aufrufstellen
  durchgereicht (Paragraph/Tabellenzellen/Überschrift/Zitat/beide Listenarten). `ALLOWED_TAGS`
  +`IMG`, `ALLOWED_ATTRS.IMG = {src, alt}`. `safeSrc()` (neu, neben `safeHref()`) akzeptiert
  ausschließlich `/^\/api\/v1\/items\/itm_[0-9a-f]{8}\/assets\/ast_[0-9a-f]{8}$/` — kein
  `data:`, keine fremde Domain (P6.5-V). `sanitizeHtml()`s `walk()` ersetzt ein `<img>` ohne
  gültiges `src` durch seinen Alt-Text-Knoten (nicht nur das Attribut entfernen — toter Knoten
  sonst), exakt derselbe Mechanismus deckt `javascript:`, fremde Domains, `data:`-URIs UND
  unaufgelöste `asset:`-Marker ab (`updates.js`s „fallende Kante", kein Sonderfall nötig). Kopf-
  kommentar korrigiert (P6.5-K — IMG/`asset:` sind nicht mehr „bewusst nicht übernommen").
- `webui/static/js/editor.js` — `insertAtCursor()` (neuer Helfer neben `wrapSelection()`/
  `insertLinePrefix()`), Upload-Handler auf `#insert-image-input` (`change`): rohe Bytes per
  `api()` an `POST .../assets`, Erfolg fügt `![<Dateiname>](asset:<id>)` an der Cursorposition
  ein, Preview wird nachgezogen, falls gerade sichtbar. Beide `markdownToHtml()`-Aufrufstellen
  (Vorschau-Umschalter, Entwurf-Wiederherstellung) bekommen jetzt `{ itemId:
  state.editingSnapshot.id }`; `showReadonlyItem()` bekommt `{ itemId: item.id }`.
- `webui/static/app.html` — neuer Knopf `#insert-image-button` (`data-md="image"` — bewusst,
  damit er automatisch an der bestehenden Preview-Disable-Schleife und am generischen
  No-Op-Klick-Listener teilnimmt, ohne beides zu duplizieren) + verstecktes `#insert-image-input`
  (`accept="image/png,image/jpeg,image/gif,image/webp"`), zwischen „Trennlinie" und dem
  Vorschau-Umschalter.
- `webui/static/app.css` — `.preview img { max-width: 100%; height: auto; }`.

**Zwei dokumentierte Abweichungen vom Plan-Wortlaut, keine Abweichung von der Absicht:**
1. Plan nennt die Zielklasse `.md-body` — diese Klasse existiert im Repo nicht, die echte
   Vorschau-Klasse heißt `.preview` (dieselbe Drift-Kategorie wie der frühere `--border`-Fund in
   P6 Step G1). Regel an `.preview` gehängt, Kommentar verweist auf die Abweichung.
2. Kein `<input type="file">` mit sichtbarem Dateiauswahl-Button im Sinne des Plantexts, sondern
   ein `hidden`-Input, den der Werkzeugleisten-Knopf per `.click()` auslöst — gleiche
   Nutzerinteraktion (ein Klick, ein Dateidialog), aber der sichtbare Knopf bleibt optisch
   konsistent mit den übrigen `toolbar-btn`-Elementen statt eines rohen Browser-Datei-Inputs.

**Advisor-Runde vor dem Commit, drei Funde, alle behoben, ein vierter dokumentiert statt
gefixt:**
1. **Update-Banner-DoD lief nur auf Argumentation, nicht auf einem echten Lauf.** Plan §3 Step
   B3 verlangt explizit „ein `asset:`-Link im Update-Banner crasht nicht" als eigene Zeile —
   ursprünglich mit dem (korrekten, aber unzureichenden) Argument übersprungen, derselbe
   `safeSrc()`/`walk()`-Pfad decke das schon ab. Dieselbe Fundklasse wie der G3-Skip im
   Deploy-Blocker (2026-08-19, „schon im Unit-Test abgedeckt" war dort auch falsch). Behoben:
   Wegwerf-Instanz bekommt jetzt ein eigenes, temporäres `UPDATE_LOG.md` (`UiSettings.
   update_log_path` überschrieben — Default hätte sonst das ECHTE `docs/UPDATE_LOG.md` des Repos
   geladen, dessen Banner-Text nichts mit diesem Test zu tun hat, wie der erste Lauf zeigte) mit
   einem Eintrag, der einen `asset:`-Marker enthält. Drei neue Prüfungen: kein `<img>` im
   Banner, Alt-/Fließtext sichtbar, keine Konsolenfehler.
2. **1×1-Testbild machte zwei Prüfungen wirkungslos.** `naturalWidth=1` bewies den echten
   Byte-Roundtrip, aber weder griff `.preview img { max-width: 100% }` bei einem 1px-Bild, noch
   war der Screenshot auswertbar (ein Farbfleck von 1×1px ist im Bild unsichtbar). Behoben:
   echtes 900×200-PNG (eigener kleiner PNG-Encoder im Skript, `zlib`/`struct`, keine neue
   Abhängigkeit), zwei neue Prüfungen (`naturalWidth == 900`, gerenderte Breite ≤ Panelbreite).
   Screenshot danach tatsächlich ausgewertet, nicht nur „geschrieben" behauptet — zeigt ein
   korrekt auf die Panelbreite begrenztes blaues Rechteck unter dem Absatztext.
3. **Tabu-Diff-Kommando war zu eng.** Lief bisher nur gegen `storage mcpserver phase4_auth`;
   `phase5_ui/webui/security.py` gehört ebenfalls zur Tabu-Liste dieser Phase (nur
   `static/**`/`api.py`/`serializers.py` sind für Bilder geöffnet) und fehlte im Kommando. Leer,
   aber jetzt mit dem vollständigen Satz geprüft.
4. **Dokumentiert, bewusst nicht behoben — kein Sicherheitsfund, aber ein falsches Plan-Modell:**
   `resolveAssetSrc()` schreibt ausschließlich `asset:<id>`-Marker um; ein händisch eingetragener
   Pfad wie `![x](/api/v1/items/itm_ANDERES/assets/ast_XYZ)` läuft an dieser Auflösung vorbei und
   besteht `safeSrc()`s Regex trotzdem, weil die Regex nur die **Form** prüft, nicht die
   Herkunft aus einem `asset:`-Marker. Das widerspricht dem Plan-Mentalmodell „`src` stammt immer
   aus einer Marker-Auflösung". **Kein Eskalationspfad:** `_assets_get_one` (Step B2) löst die
   ACL ausschließlich über die `item_id` **im Pfad** auf, nicht über das Item, in dessen Body der
   Link steht — ein Leser kann so nur Assets laden, für die er ohnehin schon `can_read_item_
   as_human()` besteht, und es gibt keinen Rückkanal, über den ein Autor das Ergebnis beobachten
   könnte (kein Exfil-Kanal). Vorgemerkt für B4/B5, falls dort eine Markdown-Erzeugung durch
   Claude selbst hinzukommt — dann würde die Form-statt-Herkunft-Lücke relevanter.

**Playwright gegen eine Wegwerf-Instanz (Standing Permission, Port 8799, `tmp`-`DATA_ROOT`,
eigene `AuthStore`/`DEK`, eigenes `UPDATE_LOG.md`, echter `uvicorn`-Prozess + echter Chromium,
kein Repo-Artefakt):** 13/13 grün — Einladung/TOTP/Login-Roundtrip, Update-Banner mit
`asset:`-Marker (drei Prüfungen, Fund 1 oben), Bild-Upload-Roundtrip (`201`, Marker in der
Textarea), Vorschau zeigt das Bild mit den echten Abmessungen, `max-width`-Begrenzung wirkt,
Screenshot geschrieben UND angesehen, `javascript:`/fremde Domain werden weder als `<img src>`
übernommen noch lösen sie einen Netzabruf aus, keine Konsolenfehler über den gesamten Lauf.
Skript liegt im Scratchpad (`/tmp/.../e2e_asset_upload.py`), kein Repo-Artefakt, P5-T gilt
unverändert (kein Unit-Test für JS).

**Tests:** `pytest` 818 unverändert (P5-T: JS bleibt unit-ungetestet, keine neue Python-Datei
in diesem Step). Tabu-Diff (`storage/**`, `mcpserver/**`, `phase4_auth/**`,
`phase5_ui/webui/security.py`) — jetzt mit dem vollständigen Satz geprüft (Advisor-Fund 3): leer.

**Verifiziert:** `pytest` 818/818 (Regressionsprobe, unverändert), Playwright 13/13 grün und
per Screenshot gesehen, Tabu-Diff (vollständiger Satz) leer, `git status` passt zur erwarteten
Step-B3-Berührungsfläche (`webui/static/{app.html,app.css,js/{markdown,editor}.js}`).

**Offen für die nächste Session:**
- Commit + Push (Nikinger-Freigabe ausstehend zum Zeitpunkt des Schreibens).
- Block B Step B4 (MCP-Asset-Tools, `mcpserver/tools.py`) ist der nächste Schritt — dort auch
  der `ItemNotFound`-Fehlertext-Fund aus B1, die `filename`-Persistenzfrage (zweimal vertagt)
  und Advisor-Fund 4 oben (Form-statt-Herkunft-Lücke in `safeSrc()`) mitdenken.
- Gate A→B (echte Connector-Probe für Block A) steht weiterhin aus, unverändert — Block B darf
  weitergebaut, aber nicht vor diesem Gate deployt werden.
- Bekannte Doku-Schuld (`phase6_shares/CLAUDE.md` Block-C-Text stale) und der
  `test_authctl.py`-Flake bleiben unverändert offen.
