---
status: live
purpose: recommended tooling for automating Sichtprüfungen (Playwright + Bildpfad) in Claude Code and OpenCode; **ab 2026-09-11: M3 sieht Bilder nativ, das Vision-Plugin ist der Defekt**
read-when: setting up or improving the automated-visual-check workflow for any phase; before assuming OpenCode/M3 "can't see images"; before (re-)installing any opencode vision plugin
detail: L2
up: ../INDEX.md
down: []
updated: 2026-09-11 (**Messbefund, kehrt die Kernaussage dieser Datei um** — `minimax/MiniMax-M3` ist in OpenCodes Modellkatalog `attachment: true` + `modalities.input: [text,image,video]`; A/B/C/D mit `opencode run` beweist: **ohne** Plugin sieht M3 das Bild nativ (0 Tool-Calls), **mit** Plugin wird der FilePart gelöscht. Das Plugin ist nicht die Lösung, es ist der Defekt. Neue §Messbefund + §Empfehlung ersetzt die Plugin-Rangliste; Plugin-Kandidatenliste nach §Historisch verschoben) | 2026-09-09 (OpenCode-Vision-Plugin-Empfehlung von „spätere Session" auf „P8.6 first step (Nikinger-Vorgabe 2026-09-08)" verschärft, Begründung warum früh [Sichtungs-Reibung ohne Plugin — pro Bild ein Kontext-Sprung]; Verweis auf neue Konvention §4 der Schwester-Datei [Screenshots im Chat präsentieren sobald Plugin installiert]) | 2026-09-08 (erste Fassung, nach Phase-8.5-Sichtprüfungs-Sub-Session)
---

# Sichtprüfungs-Automatisierung — Werkzeug-Empfehlungen

> Entstanden aus einer Phase-8.5-Sub-Session (2026-09-08): fünf der neun Sichtprüfungs-Punkte
> aus `phase8_5_picker_release/SICHTPRUEFUNG_WALKTHROUGH.md` wurden per Playwright automatisiert
> statt vom Nikinger am Bildschirm geklickt (C4-0, C4-1, C3-1, C3-2, C3-3 — siehe
> `phase8_ui_graph/CLAUDE.md` für den fachlichen Befund). Diese Datei ist die Werkzeug-Seite
> davon: was gebraucht wurde, was fehlte, und was für die nächste Runde (in beiden CLIs)
> installiert werden sollte.

## Was diese Session tatsächlich benutzt hat (Baseline, funktioniert bereits)

- `~/.claude-code-tools/e2e-venv` — eigenes venv mit `playwright` (1.62.0) + `pyotp`, getrennt
  vom Projekt-`.venv` (Konvention aus den Test-Instruktionen: Test-Tooling nie im Projekt- oder
  System-Python).
- Playwright `addInitScript` zum Instrumentieren von `CanvasRenderingContext2D.prototype`
  (Tag-Kanten-Zählung, `phase8_ui_graph/scripts/p8_21d_tag_cutoff_probe.py`) — kein Eingriff in
  App-Code, patcht nur die Browser-Prototype-Kette vor dem Laden.
- CDP `Emulation.setEmulatedMedia` für `prefers-reduced-transparency`/`prefers-reduced-motion`
  (bereits etabliertes Muster aus `p8_16_glass_fallback_probe.py`).
- `health_gate.sh` — reine `curl`-GETs gegen die echte Production, kein Auth nötig, liefert ein
  dachiertes „live ist v3.0.1, SHA X" ohne jedes Risiko.

Das alles funktioniert für **beide** CLIs identisch — Python + Playwright ist agent-agnostisch.
Der Unterschied beginnt erst bei der Frage: *wer schaut sich das Ergebnis an.*

## Messbefund 2026-09-11 — M3 sieht Bilder nativ, das Plugin zerstört genau das

> **Diese Sektion kehrt die frühere Kernaussage dieser Datei um.** Der Satz „OpenCodes
> Attachment-Pipeline verdrahtet Bilder für MiniMax nicht durch" war für **M2.x** richtig und ist
> für **M3** falsch. Gemessen, nicht recherchiert.

### Was der Katalog sagt

`~/.cache/opencode/models.json` (models.dev-Cache, **Stand 2026-09-11**) trennt die Familie sauber:

| Modell | `attachment` | `modalities.input` |
|---|---|---|
| `minimax/MiniMax-M2` … `M2.7` | `false` | `[text]` |
| **`minimax/MiniMax-M3`** | **`true`** | **`[text, image, video]`** |

Provider `minimax` fährt über `npm: @ai-sdk/anthropic` gegen `https://api.minimax.io/anthropic/v1`
— also den Anthropic-kompatiblen Endpunkt, der Bild-Blöcke nativ transportiert.

> **Einschränkung zur Datierung:** Die Cache-Datei wurde am 2026-09-11 aktualisiert (mtime 14:51).
> Ob der M3-Eintrag am 2026-09-10 — als der Plugin-Pfad beschlossen wurde — schon `attachment: true`
> trug, ist nachträglich **nicht feststellbar**. Die damalige Entscheidung kann gegen den damaligen
> Katalogstand richtig gewesen sein; die Korrektur hier gilt für den Stand ab 2026-09-11.

### Der A/B-Beweis (`opencode run`, MiniMax-M3, derselbe Screenshot, dieselbe Frage)

Testfrage war bewusst **nur aus Pixeln** beantwortbar (Seitenleisten-Zähler „Notizen 6" +
orangefarbenes Badge „nur lesen" neben `gamma` in
`docs/screenshots/p8_6_block_a_picker_v3ritt.png`) — eine generische Antwort kann nicht durchrutschen.

| Lauf | Kommando | Tool-Calls | Ergebnis |
|---|---|---|---|
| **A — Plugin aus** | `opencode run --pure -f shot.png -- "…"` | **0** | ✅ „1) 6 / 2) nur lesen" — nativ, sofort |
| **B — Plugin an** | `opencode run -f shot.png -- "…"` | **9** | ⚠️ FilePart gelöscht → `local_vision` **error** (2×) → M3 baut sich per `bash`/`curl`/`base64` selbst einen Ollama-Call (5 Fehlversuche, u. a. „Argument list too long") → am Ende dieselbe Antwort, ein Vielfaches an Zeit und Token |
| **C — mitten in der Session, Plugin aus** | `opencode run --pure` + „lies die Datei mit deinem `read`-Werkzeug" | **1** (`read`) | ✅ `read` liefert `Image read successfully`, M3 antwortet korrekt — **ohne** `-f`, **ohne** Ollama |
| **D — dasselbe, Plugin an** | `opencode run` (kein `--pure`) + derselbe Auftrag | **1** (`read`) | ✅ identisch korrekt — **das Plugin fasst Tool-Results nicht an** |

**Lauf C/D sind die für Sichtprüfungen wichtigsten:** der Agent kann einen Playwright-Screenshot, den
er gerade selbst geschrieben hat, mit dem eingebauten `read`-Tool anschauen. Genau die Schleife
„screenshotten → hingucken → bewerten" braucht damit *kein* Zusatzwerkzeug.

Lauf **D** ist der Grund, warum dieser Workflow **sofort** gilt und nicht erst nach dem Rückbau: der
Plugin-Hook greift nur die **letzte User-Nachricht** ab (`findLastUserMessage` → `isImageFilePart`).
Ein `read`-Ergebnis ist ein Tool-Part, kein User-FilePart — es läuft am Plugin vorbei. Gemessen, nicht
nur aus dem Quelltext geschlossen.

### Warum das Plugin schadet

`DavidEasden/opencode-vision` hängt sich in `experimental.chat.messages.transform` und macht in
`removeProcessedImageParts()` genau das, was der Name sagt: es **entfernt den FilePart** und
ersetzt ihn durch einen Text-Hinweis „ruf `local_vision` mit diesem Pfad auf". Für M2.1, wofür es
geschrieben wurde, ist das die Rettung. Für M3 ist es eine Amputation.

Verschärft wird es durch die hiesige Konfiguration `~/.config/opencode/opencode-vision.json` mit
`"models": ["*"]` — der Wildcard matcht **jedes** Modell, also auch das eine, das die Krücke nicht
braucht.

Dazu zwei Folgedefekte, beide in Lauf B beobachtet:

- **`local_vision` läuft im Tool-Call auf Fehler.** Der MCP-Server selbst ist in Ordnung — direkt
  über stdio angesprochen antwortet `phase8_6_ui_polish/scripts/mcp_local_vision_server.py`
  korrekt. Die Fehlermeldung selbst lag nie vor (der Stream liefert nur `status: error`,
  `output: None`) — **mit hoher Wahrscheinlichkeit** OpenCodes MCP-Client-Timeout gegen den
  46–180 s CPU-Cold-Start von `qwen3-vl:8b`; ein Schema- oder Framing-Fehler sähe von außen
  identisch aus und ist nicht ausgeschlossen. Ein 8-B-Vision-Modell auf CPU ist für
  den *synchronen* Tool-Pfad schlicht zu langsam — als CLI (`vision_ollama.py`) bleibt es brauchbar.
- **`~/.config/opencode/package.json` zeigt auf `file:../../../../tmp/opencode/opencode-vision-src`.**
  `/tmp` überlebt keinen Reboot; ein späteres `npm install` in dem Verzeichnis bricht. Bei den
  anstehenden Proxmox-Reboots relevant.

### Was das Plugin *nicht* verursacht: Bilder im Chat anzeigen

Die zweite Hälfte der Nikinger-Beschwerde („M3 kann Bilder nicht wie du im Chat präsentieren,
weder Host- noch Remote-WebUI") ist ein **anderer Mechanismus** und durch kein Plugin lösbar.

Das ausgelieferte Web-UI-Bundle (`/assets/index-*.js`, OpenCode 1.18.30) kennt genau diese
Attachment-Slots:

```
prompt-attachments*          user-message-attachment
user-message-attachments     user-message-attachment-image   ← das einzige <img>
user-message-attachment-file user-message-attachment-name
```

Alle tragen `prompt-` oder `user-message-`. **Es gibt keinen Assistant- oder Tool-Result-Slot, der
ein Bild rendert.** Die Daten wären da — ein `read` auf ein PNG liefert im Tool-State sauber
`attachments: [{mime: "image/png", url: "data:image/png;base64,…"}]` — nur rendert das UI sie
nicht; im Textpfad erscheinen sie als Platzhalter `[Attached image/png: …]`.

Konsequenz: **Bilder fließen in OpenCode nur in eine Richtung** — Mensch → Modell (Paste, `-f`,
`@pfad`) wird als `<img>` gerendert, Modell → Mensch nicht. Das ist eine UI-Grenze von OpenCode
1.18.30, kein Modell- und kein Plugin-Thema. Für Sichtprüfungen heißt das: der Nikinger öffnet den
Screenshot weiter selbst; **`sichtpruefung_automation_conventions.md` §4 ist mit OpenCode nicht
erfüllbar** und bleibt eine Claude-Code-Konvention. Der Gewinn liegt woanders und ist größer: M3
kann die Bilder jetzt selbst *auswerten* und muss nicht mehr fragen.

Der „Paste vom Remote-PC über die Webkonsole"-Teil erklärt sich damit ebenfalls: Paste läuft durch
denselben `messages.transform`-Hook, das Plugin hat den FilePart also auch dort gelöscht.
Nebenbei — solange Playwright den Screenshot ohnehin auf die Platte schreibt, ist Pasten
unnötig: `@pfad` bzw. `read` ist der kürzere Weg und überlebt jede Remote-Clipboard-Macke.

## Empfehlung (ersetzt die frühere Plugin-Rangliste)

**Der richtige Zug ist ein Rückbau, kein Zusatz-Plugin.** Es gibt keine
`provider.options.capabilities`-Flagge zu setzen, weil nichts zu reparieren ist: der Katalog führt
M3 bereits korrekt als bildfähig, und OpenCode liefert den FilePart aus, sobald ihn niemand
wegnimmt.

1. **Plugin deaktivieren** — Symlink weg, damit der native Pfad frei wird:
   ```bash
   rm ~/.config/opencode/plugins/opencode-vision.js   # OpenCode lädt dieses Verzeichnis automatisch
   ```
   Danach OpenCode neu starten. Gegenprobe: ein `opencode run -f <png> -- "…"` muss die Frage
   **ohne** Tool-Call beantworten.
   *Falls das Plugin je für ein M2.x-Modell gebraucht wird:* nicht löschen, sondern in
   `opencode-vision.json` `"models"` von `["*"]` auf `["*/MiniMax-M2*"]` verengen — dann greift es
   nur noch dort, wo es hilft.
2. **`local_vision`-MCP-Eintrag entfernen oder belassen** — er schadet nach Schritt 1 nicht mehr
   (M3 ruft ihn nicht mehr auf), ist aber auch nutzlos. `vision_ollama.py` bleibt als CLI-Fallback
   für den Fall „kein Netz / MiniMax-Konto leer" sinnvoll und kostet nichts.
3. **Keinen der anderen Plugin-Kandidaten installieren** (siehe §Historisch). Sie lösen alle
   dasselbe M2.x-Problem und würden bei M3 denselben Schaden anrichten.

## Historisch — die Plugin-Kandidaten von 2026-09-08 (überholt, nicht löschen)

> Die folgende Rangliste entstand unter der Annahme, OpenCode verdrahte Bilder für M3 nicht durch.
> Diese Annahme ist seit dem Messbefund oben widerlegt. Die Liste bleibt stehen, weil sie für
> **M2.x-Modelle** (`attachment: false`) weiterhin zutrifft — und damit dokumentiert, wann ein
> solches Plugin die richtige Antwort *wäre*.

1. **`DavidEasden/opencode-vision`** — https://github.com/DavidEasden/opencode-vision
   Explizit als Fork/Weiterentwicklung von `devadathanmb/opencode-minimax-easy-vision`
   gebaut — d. h. **für genau diese Modellfamilie geschrieben**, nicht generisch. Registriert
   sich als Plugin in `opencode.json`, gibt Modellen ohne native Bild-Verdrahtung die
   Fähigkeit, Bilder per Dateipfad zu lesen. Erster Kandidat zum Ausprobieren, weil er am
   direktesten auf die "M3 in OpenCode" Situation zielt.

2. **`JochenYang/opencode-vision`** — https://github.com/jochenyang/opencode-vision
   Andere Implementierung desselben Grundproblems: speichert eingefügte Bilder automatisch
   und leitet nicht-visuelle Modelle per Tool-Call-Anleitung dazu an, sie zu erkennen.
   Unterstützt explizit **mehrere Bilder gleichzeitig** — relevant, falls eine Sichtprüfung
   mehrere Screenshots im selben Zug vergleichen soll (z. B. Vorher/Nachher).

3. **`alfaoz/opencode-see-image`** — https://github.com/alfaoz/opencode-see-image
   Registriert ein `see_image`-Tool, das das Bild an ein separates vision-fähiges Modell
   schickt und eine Textbeschreibung zurückgibt, die das Hauptmodell weiterverarbeitet.
   Nützlich als Fallback, falls M3 selbst (aus Kosten-/Konfigurationsgründen) nicht als
   Vision-Backend laufen soll — dann läuft die Beschreibung über ein zweites Modell.

4. **`alvinunreal/oh-my-opencode-slim`** — https://github.com/alvinunreal/oh-my-opencode-slim
   Kein reines Vision-Plugin, sondern eine Multi-Agent-Suite mit einem **Observer**-Subagenten,
   der Bilder/Screenshots übernimmt, falls der Orchestrator-Agent selbst nicht multimodal ist.
   Architektonisch die schwergewichtigere Option — nur relevant, falls ohnehin ein
   Multi-Agent-Setup geplant ist, nicht als Erstlösung für das reine Bild-Problem.

**Nächster konkreter Schritt (verbindlich als P8.6 first step, Nikinger-Vorgabe 2026-09-08):**
`DavidEasden/opencode-vision` installieren, gegen genau eines der Screenshots aus der
Phase-8.5-Session testen (z. B. `c4_p8519_01_radiogruppe_im_dialog.png` — einfach zu
verifizieren: "sind zwei Radio-Buttons sichtbar, ist einer markiert?"), und danach entscheiden,
ob es das native `Read`-Äquivalent für OpenCode wird. Sobald installiert, gilt die neue
Sichtungs-Konvention aus der Schwester-Datei
[`sichtpruefung_automation_conventions.md`](./sichtpruefung_automation_conventions.md) §4:
Screenshots im Chat präsentieren, darunter eine kurze Zeile „Was zu validieren ist", und der
Nikinger sichtet direkt am Bild.

**Warum das Plugin P8.6 first step ist (nicht später):** solange M3 die Screenshots nicht
nativ im Chat zeigen kann, muss der Nikinger sie aus dem Dateisystem öffnen, was pro Bild
einen Kontext-Sprung kostet und die Sichtungs-Runde ungleich schwerer macht. Der Nikinger
hat 2026-09-09 explizit darauf bestanden, dass die Plugin-Installation **vor** dem ersten
P8.6-Schritt kommt — nicht weil P8.6 sonst blockiert wäre, sondern weil ohne das Plugin die
nächste Sichtungs-Runde (für P8.5-6 Vorschau-Beleg, für die ersten UI-Politur-Schritte aus
`p8x_ui_polish_notes.md`, für den Radiogruppe-Rückbau) jedes Mal denselben Reibungs-Verlust
hat.

## Empfehlung für Claude Code

Kein Fähigkeits-Gap — Bilder werden bereits nativ multimodal gelesen (siehe die acht
Screenshots, die in der Sitzung direkt gezeigt wurden). Der Gap ist **Reibung**: jeder Check in
dieser Session war Skript-schreiben → `Bash` ausführen → JSON-Ausgabe lesen, statt eines
direkten Tool-Calls mit sofortigem Bild-Ergebnis in der Konversation.

- **Playwright-MCP-Server** (z. B. Microsofts `@playwright/mcp` — Paketname zum Zeitpunkt dieser
  Notiz, bei Einrichtung aktuellen Wartungsstand prüfen) würde `browser_navigate`/
  `browser_click`/`browser_screenshot` als direkte Tool-Calls anbieten, Screenshot-Ergebnis
  landet inline im Gespräch statt als Datei, die erst per `Read` nachgeladen werden muss.
  Sinnvoll für **explorative** Checks ("sieht das jetzt richtig aus?").
- **Für die präzisen numerischen Assertions bleibt ein eigenständiges Skript die bessere Wahl**
  (z. B. `p8_21d_tag_cutoff_probe.py`s Frame-Teiler-Logik) — die Instrumentierungslogik muss über
  mehrere Schritte hinweg bestehen bleiben und unabhängig wiederholbar sein. Playwright-MCP
  ersetzt das nicht, ergänzt es nur für den visuellen Erstblick.

## Was NICHT gebraucht wird

- Keine Bildschirm-Terminal-Renderer (`chafa`/`viu`) für Claude Code — das Problem, das sie
  lösen (Terminal kann kein PNG anzeigen), existiert für Claude Code nicht.
- Kein Pixel-Diff-Tooling (`pixelmatch`/`odiff`) als Ersatz für die Vision-Plugins oben — Pixel-
  Diffs beantworten "hat sich was geändert", nicht "sieht das Neue richtig aus". Für Regressions-
  Checks auf einen bereits abgenommenen Zustand sind sie trotzdem sinnvoll, nur eine andere
  Kategorie als das hier beschriebene Problem.

## Quellen (Recherche 2026-09-08)

- [DavidEasden/opencode-vision](https://github.com/DavidEasden/opencode-vision)
- [JochenYang/opencode-vision](https://github.com/jochenyang/opencode-vision)
- [alfaoz/opencode-see-image](https://github.com/alfaoz/opencode-see-image)
- [alvinunreal/oh-my-opencode-slim](https://github.com/alvinunreal/oh-my-opencode-slim)
- [MiniMax M3 — MiniMax Research blog](https://www.minimax.io/blog/minimax-m3) — native ViT-basierte Bild-/Video-Eingabe, 1M-Token-Kontext, Anthropic-/OpenAI-kompatible SDK-Zugriffe
- [MiniMax M3 model card — build.nvidia.com](https://build.nvidia.com/minimaxai/minimax-m3/modelcard)
