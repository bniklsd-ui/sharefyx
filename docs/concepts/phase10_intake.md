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
updated: 2026-10-08 (Closeout P9: Zeiger auf `PHASE9_CLOSEOUT_HANDOVER.md` §4 in §3, Matrix-Stand 12 ⚠️ · 1 ⬜) | 2026-10-08 (angelegt — Nikinger-Auftrag nach dem Block feedback: P10 beendet **alle** Baustellen, damit P11 auf einem gehärteten Fundament neue Funktionen denken kann; Zweiteilung P10/P10.5; drei neue Themen: Responsivität/Performance, visuelle Kleinigkeiten, Editor ohne Vorschau/Bearbeiten-Modus)
---

# Phase 10 — Sammelstelle (kein Plan)

> **Das Bild des Nikingers (2026-10-08):** P9 war das Fundament, **P10 baut das Haus fertig und dämmt es**,
> damit P11 überhaupt erst über eine Garage nachdenken darf. Regel daraus: **Phase 10 endet erst, wenn es keine
> offene „Baustelle" mehr gibt.** Neue Funktionen (P11) sind in P10 ausdrücklich nicht Teil des Auftrags.

## 1. Zweiteilung (Vorschlag, Nikinger-Gedanke 2026-10-08)

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
