---
status: live
purpose: recommended plugins/tooling for automating Sichtprüfungen (Playwright + vision bridge) in Claude Code and OpenCode
read-when: setting up or improving the automated-visual-check workflow for any phase; before assuming OpenCode/M3 "can't see images"
detail: L2
up: ../INDEX.md
down: []
updated: 2026-09-09 (OpenCode-Vision-Plugin-Empfehlung von „spätere Session" auf „P8.6 first step (Nikinger-Vorgabe 2026-09-08)" verschärft, Begründung warum früh [Sichtungs-Reibung ohne Plugin — pro Bild ein Kontext-Sprung]; Verweis auf neue Konvention §4 der Schwester-Datei [Screenshots im Chat präsentieren sobald Plugin installiert]) | 2026-09-08 (erste Fassung, nach Phase-8.5-Sichtprüfungs-Sub-Session)
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

## Die eigentliche Asymmetrie

| | Claude Code (Sonnet/Opus) | OpenCode (mit MiniMax M3) |
|---|---|---|
| Kann der Agent selbst ein PNG sehen? | Ja, nativ (`Read`-Tool liefert Bildinhalt multimodal) | **Ja, das Modell kann es auch** — M3 hat einen echten ViT-Bildencoder, native Bild+Video-Eingabe über die Anthropic- oder OpenAI-kompatible API. **Kein Modell-Limit.** |
| Wo hakt es dann? | Nirgends — aber jeder Check kostet einen Skript-schreiben→ausführen→JSON-lesen-Umweg | **OpenCodes eigene Attachment-Pipeline** verdrahtet Bild-Uploads für bestimmte Modellfamilien (u. a. MiniMax) nicht automatisch durch — das ist ein Client-seitiges Verdrahtungsproblem, kein Fähigkeits-Problem des Modells |

Kurz: die Behauptung „OpenCode kann keine Bilder" aus der letzten Session war zu pauschal.
Richtig ist: *OpenCodes native Attachment-UI* verdrahtet es für M3 nicht automatisch durch. Es
gibt dafür bereits eine kleine Plugin-Landschaft, die genau diese Lücke schließt, indem sie das
Bild explizit per Dateipfad an einen Tool-Call statt an den nativen Attachment-Mechanismus
hängt.

## Empfehlung für OpenCode (Reihenfolge nach Passgenauigkeit)

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
