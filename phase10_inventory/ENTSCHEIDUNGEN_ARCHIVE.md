---
status: archive
purpose: L3-Archiv der Entscheidungsliste D-1–D-18 des Phase-10-Registers — jede Frage und die Antwort des Nikingers, verbatim. Das Register selbst führt nur noch die Baustellen und ihren Stand.
read-when: wenn eine Entscheidung nachgeschlagen werden soll, die im Register nicht mehr steht, oder wenn eine Registerzeile auf ihre Entscheidung verweist
detail: L3
up: ./BAUSTELLENREGISTER.md
down:
updated: 2026-10-22 (angelegt — P10.5 Block 0, Schritt 0.8: das Register stand bei 40.954 B gegen die harte Grenze 40.960 B, also 6 B Luft; §12 (Entscheidungsliste, 3.904 B, alle D-1–D-18 beantwortet) wanderte per `scripts/move_sections.py` verbatim hierher)
---
# Entscheidungsliste D-1–D-18 (Archiv)

> **Was hier steht:** die Entscheidungsliste des Phase-10-Registers, **verbatim** — jede Frage, ihre
> Zeilen, die Empfehlung und die Antwort des Nikingers mit Datum.

**Warum sie gewandert ist.** Das Register ist die Arbeitsliste der Phase 10.5: 76 Zeilen in elf
Themen, und jede Zeile wird während P10.5 abgehakt (Lock P10-B). Am 2026-10-21 stand die Datei bei
**40.954 B** gegen die harte Grenze **40.960 B** — 6 B Luft, und das erste Abhaken hätte die Datei
über die Grenze gehoben. Die Entscheidungsliste ist **abgeschlossen** (alle D-1–D-18 beantwortet, Stand
2026-10-20) und damit genau der Abschnitt, der nichts mehr zu entscheiden hat: Er wanderte per
`scripts/move_sections.py` hierher, die Überschrift bleibt im Register mit Zeiger stehen.

**Was das Register weiterhin trägt:** die 76 Baustellen mit Herkunft, Befund am Code, Größe, Risiko,
nötiger Entscheidung und Ziel. Die `Entsch.`-Spalte verweist weiter auf `D-n` — die Fragen selbst
stehen hier.

## 12 Entscheidungsliste (für P10 Step 3)

Antworten werden hier **mit Datum** eingetragen; erst dann wird das „Ziel" der Registerzeile verbindlich. **Stand 2026-10-20: alle D beantwortet** (D-3 nach M1, D-14 nach M8).

| D | Frage | Zeilen | Empfehlung | Antwort |
|---|---|---|---|---|
| D-1 | Welcher Karten-Entwurf (A Landkarte · B Gehirn · C Gehirnkarte) oder welche Mischung? | KA-1, KA-3 | C mit der Aktivierung aus B, ohne „kürzlich geändert" (kein zehntes Feld) | **C** — Nikinger 2026-10-16 („Option C finde ich mega") |
| D-1b | Welcher Stil innerhalb C (C1 Flächen · C2 Nervenbahnen · C3 Höhenlinien) oder welche Mischung? | KA-1 | C1 als Grundbild, Aktivierung aus C2 nur beim Hover | **C2 Nervenbahnen** — Nikinger 2026-10-16 |
| D-2 | Einklappen der Karte (§2.5): verwerfen oder P11? | KA-4 | verwerfen | **verwerfen** — Nikinger 2026-10-18 |
| D-3 | Zielwerte Performance und welcher Weg für `/overview` | PF-1–PF-3, PF-5 | Ziele nach M1/M2 festlegen; Vorschlag zum Start: `/overview` serverseitig ≤ 300 ms bei Live-Last, Space-Wechsel gefühlt ≤ 1 s über die Domain | **Z1–Z4** (`messung/M1_browser.md` §D-3; Z1 unter Vorbehalt der Machbarkeit) — Nikinger 2026-10-20 |
| D-4 | Editor: Stufe 1 bauen (hebt P5-U auf)? Stufe 2 (elfte Öffnung)? | ED-1–ED-3 | Stufe 1 ja, mit Rohmodus; Stufe 2 nein | **Stufe 1 und Stufe 2** — Nikinger 2026-10-18 |
| D-5 | Tab-Titel deutsch oder englisch? | UI-3 | deutsch, wie die Oberfläche | **deutsch** — Nikinger 2026-10-18 |
| D-6 | Logo-Platzhalter: Wortmarke als SVG oder ein schlichtes Zeichen? | UI-2 | Wortmarke „sharefyx" als SVG, ein Austauschpunkt | **„S" + Teilen-Zeichen als Wortmarke** — Nikinger 2026-10-18 |
| D-7 | Kontrast 4,38:1 schließen? | UI-5 | ja: hellere Vorsichtfarbe nur für Text | **ja** — Nikinger 2026-10-18 |
| D-8 | Anbieter: welcher Abnahme-Client, gehören Web-Clients und CIMD dazu? | PA-1, PA-3, PA-4, PA-7 | opencode als Abnahme-Client; DCR für native Clients + Loopback; ChatGPT nur per Konfiguration, falls gewollt; CIMD → P11 | **native + Loopback; Abnahme opencode mit zwei Modellanbietern; kein ChatGPT; CIMD P11** — Nikinger 2026-10-18 |
| D-9 | Darf das MacBook den Relay-Port 8765 erreichen? | BT-3 | nein — nur `tag:sharefyx-edge` | **MacBook behält Zugriff** — Nikinger 2026-10-18 |
| D-10 | Caddy-Vorlage auf die Live-Werte nachziehen? | BT-1 | ja, nach V199 | **ja, ohne Fleet zu stören** — Nikinger 2026-10-18 |
| D-11 | `SuccessExitStatus=143` in die Relay-Unit? | BT-2 | ja | **ja** — Nikinger 2026-10-18 |
| D-12 | LAN-Ports: Sharefyx-Posten oder Fleet? | BT-4 | Fleet | **an Fleet** — Nikinger 2026-10-18 |
| D-13 | `mcp` exakt pinnen (auf den Live-Stand)? | BT-6 | ja, `mcp==1.30.0` nach Messung | **ja** — Nikinger 2026-10-18 |
| D-14 | Vision-Modell: Ersatz testen oder CT 111 stilllegen? | BT-11 | eine Frage bekannter Antwort an einen Kandidaten; fällt sie, stilllegen | **Recherche + Test (M8)** — Nikinger 2026-10-18 · **[2026-10-19, M8 gemessen]** Incumbent bestätigt gestrichen (echte Falle reproduziert); **Empfehlung: `qwen2.5vl:7b`** (besteht die echte Falle; Schwäche: `overlapping` synthetisch) oder CT 111 stilllegen — **ja, `qwen2.5vl:7b`** — Nikinger 2026-10-20 |
| D-15 | Übergangsfenster wieder befristen — wann? | BT-5 | Test am 2026-11-02, danach Datum setzen | **Test um den 2026-11-02** — Nikinger 2026-10-18 |
| D-16 | `created_by` (elfte Öffnung)? | RE-7 | nein | **ja** — Nikinger 2026-10-18 |
| D-17 | Ledger-Urteile: BT-10, PA-5, UI-4, RE-1, RE-3–RE-6, LG-1–LG-5, LG-7–LG-9, DO-2, DO-3 | s. Zeilen | je Zeile in der Spalte „Ziel" | **je Zeile eingetragen** — Nikinger 2026-10-18 |
| D-18 | Altlasten: P6/P6.5 mit späteren Belegen schließen, Rest als Termin führen, P9-⚠️ als ausreichend bestätigen? | AL-1, AL-2, AL-4, AL-5 | ja | **ja** — Nikinger 2026-10-18 |
