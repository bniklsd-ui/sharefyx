---
status: live
purpose: Note from other project (eurofyx-fleet, 2026-11-08) — Stand der Ausführer-Pläne (z.ai abgelaufen und entfernt, MiniMax als M Plan Go verlängert), Ergebnis der Ausführer-Bewertung, geplante Harness-Re-Evaluation, Sharefyx-MCP in opencode
read-when: vor der Wahl des Ausführers oder Harness; bevor ein MiniMax-Modell benutzt wird; bei Fragen zum MiniMax-Kontingent
detail: L2
up: ../INDEX.md
updated: 2026-11-13 (committet mit INDEX-Zeile in der P11-Planungssitzung; Inhalt unverändert) | 2026-11-08 (angelegt von eurofyx-fleet auf Wunsch des Nikingers; §1/§2/§4/§5 am selben Abend nachgezogen: z.ai und `claude-glm` entfernt, MiniMax verlängert; nicht committet — Commit und INDEX-Zeile macht die Projekt-Session)
---

# eurofleet → Sharefyx: Stand Ausführer und Harness (2026-11-08)

> Fremder Text aus dem Infra-Projekt eurofyx-fleet, geschrieben auf Wunsch des Nikingers.
> Nichts davon ist eine Freigabe für Änderungen an Diensten oder an der opencode-Konfiguration.

## 1 Pläne (Nikinger, 2026-11-08)

- **z.ai Coding-Plan: gekündigt und abgelaufen, entfernt.** eurofleet hat am 2026-11-08 den Eintrag `zai-coding-plan` aus `~/.local/share/opencode/auth.json` gelöscht (diese VM und die Trading-Bot-VM) und den Wrapper `claude-glm` auf dieser VM entfernt. GLM steht nicht mehr zur Verfügung.
- **MiniMax: am 2026-11-08 verlängert als „M Plan Go“** (monatlich, nächste Verlängerung 2026-12-07, automatisch). Der frühere größere Plan war nicht mehr buchbar. Go hat das kleinste Kontingent der drei Stufen (Go/Explore/Build = 1×/3×/7,5×), gezählt im 5-Stunden- und im Wochenfenster. Die Herstellerdoku nennt als Textmodell nur `MiniMax-M3.1-Flash`; **gemessen** am 2026-11-08: `MiniMax-M3` und `MiniMax-M3.1-Flash` antworten beide mit dem bisherigen Key über `https://api.minimax.io/v1`. Der Key bleibt gleich, an der opencode-Konfiguration ändert sich nichts. Die Frist 2026-11-15 entfällt.

## 2 Ergebnis der Ausführer-Bewertung (eurofleet, aus den Rohdaten beider Repos)

Grundlage: Rohdaten aus Sharefyx (P10.5, Lock P10.5-B) und Trading-Bot (Phase 17, Plan §14.2). Eine vorab festgelegte Rubrik gab es nicht; das ist eine Bewertung aus Rohdaten, kein vorregistrierter Vergleich.

| Ausführer | Belege | Schwäche |
|---|---|---|
| **MiniMax M3** (opencode, Trading-Bot, Exec-Sessions #1–#18) | keine Rückfallregel ausgelöst, alle Suites grün, Plan-AKs je Block getroffen; das Opus-Review AK22 über 27 Code-Commits fand einen echten Code-Befund (R1), keinen in Order-Pfad, Breaker oder LLM-Verdrahtung | keine Modell-Trailer je Commit; Kontingent nicht erfasst |
| **MiniMax M3.1 Flash** (opencode, Sharefyx, Blöcke 0–12 und 14.0–14.6) | 61 Commits mit Trailer, fast überall 0 Eingriffe | Block 14.6: Bildurteil im Bericht falsch → Blöcke mit Sichtung danach bei Claude Code |
| **GLM 5.3 Flash / 5.3** (opencode, Sharefyx, 2026-10-18/19) | — | Kontingent leer, weil ohne Kontextgrenze nie kompaktiert wurde (Konfiguration, nicht Modell); mit 400-K-Grenze nie wiederholt, Plan inzwischen abgelaufen |

**Empfehlung eurofleet (Entscheidung beim Nikinger):** MiniMax-Plan verlängern (erledigt, §1); M3 für Code-Blöcke, M3.1 Flash für planbare Blöcke; Sichtungen und Reviews bleiben bei Claude Code. M3 gegen M3.1 Flash ist **kein** Gleichstandsvergleich (verschiedene Projekte und Aufgaben).

## 3 Bilder

Der opencode-Katalog führt `MiniMax-M3.1-Flash` und `MiniMax-M3` mit Bild- und Videoeingabe (`attachment: true`). opencode kann Bilder also nativ an das Modell geben. **Nicht gemessen:** ob der Ausführer in Sharefyx Block 14.6 die Bilder selbst angesehen hat oder das Urteil über den MCP `local_vision` (kleines lokales Vision-Modell) geholt hat.

## 4 Geplant: Harness-Re-Evaluation (Nikinger, 2026-11-08)

**MiniMax Code gegen opencode**, beide mit einem MiniMax-Modell als Ausführer, **Claude Code bleibt Planer**. Noch nicht entworfen und nicht gestartet; die Verlängerung des MiniMax-Plans ist erfolgt (§1). Die Anbindung (Installation, Auth, Konfiguration) macht eurofleet. Vorschlag für die Rubrik, **vor** dem ersten Lauf festzuschreiben: gleiche Aufgabe je Harness, Modell-Trailer je Commit, Wanduhr, Kontingent laut MiniMax-Konsole, Eingriffe, Befunde eines Opus-Reviews, eine Bildaufgabe mit **nativer** Bildeingabe (ohne `local_vision`). Wegen des Go-Kontingents gehört der Verbrauch je Lauf in die Rubrik.

**Bitte an diese Session:** bis dahin wie bisher arbeiten; Modell-Trailer in **jedem** Commit des Ausführers setzen; Kontingent je Block notieren, wenn sichtbar. Die opencode-Konfiguration (`~/.config/opencode/`, `auth.json`, `opencode.service`) ändert weiter nur eurofleet.

## 5 Sharefyx-spezifisch

- **Sharefyx-MCP in opencode:** auf der Sharefyx-VM seit 2026-11-07 live (`sharefyx connected`), auf der **Trading-Bot-VM seit 2026-11-08 ebenfalls** (`opencode mcp list`: `sharefyx connected`, Login durch den Nikinger am Desktop). Traktion-VM bleibt ohne (opencode 1.17.19). Der Eintrag `agent.build.tools` aus der Übergabe-Notiz ist weiter nicht nötig.
- **`claude-glm`** ist auf dieser VM seit 2026-11-08 entfernt (z.ai abgelaufen, siehe §1).
- Der Schreibtest der drei Modelle (Übergabe-Notiz §8) ist bei eurofleet dokumentiert; ob die Rückmeldung dazu in die Übergabe-Notiz kommt, entscheidet der Nikinger.

## 8 Nachtrag 2026-11-08 abends: Block 14.6 gemessen, Entwurf der Harness-Re-Evaluation

**Block 14.6 (beantwortet die offene Frage aus §3).** eurofleet hat am 2026-11-08 lesend in der opencode-Datenbank dieser VM nachgesehen, und zwar nur Sessions, Nachrichten und Tool-Aufrufe, keine Konten- oder Zugangstabellen:

- Die 14.6-Session (2026-10-28 19:43 bis 10-29 11:06) lief durchgehend mit `MiniMax-M3.1-Flash`.
- **Das Modell hat kein einziges Bild selbst bekommen:** Es gab keinen Bild-Anhang und kein `read` auf eine PNG-Datei. Die beiden 14.4-Sessions davor sahen genauso aus.
- Alle vier Bildurteile kamen über den MCP `local_vision`, also über das Standardmodell `qwen3-vl:8b` aus `phase8_6_ui_polish/scripts/mcp_local_vision_server.py`.
- Die letzte Antwort (2026-10-29 10:45, finale Karte) widersprach sich selbst. Sie nannte die Karte „ein zusammenhängendes Gehirn-ähnliches Gebilde“ und im selben Absatz „vier getrennte Bereiche“. Der Ausführer hat nicht nachgefragt und das Urteil in den Bericht übernommen.
- Ein früherer Aufruf (Vergleichsbild der fünf Varianten, 2026-10-28 21:06) kam leer zurück.

**Bewertung eurofleet:**
- 14.6 sagt nichts darüber aus, wie gut `MiniMax-M3.1-Flash` Bilder erkennt.
- Der Block zeigt zwei andere Schwächen: Das 8B-Vision-Modell ist für Gestalturteile („ein Körper oder mehrere Inseln“) unzuverlässig, und der Ausführer übernimmt widersprüchliche Tool-Antworten als Beleg.
- Ob die Bildeingabe direkt ans Modell funktioniert, ist noch nicht gemessen.
- Die Empfehlung aus §2 bleibt: Sichtungen gehören zu Claude Code oder zum Menschen.

**Harness-Re-Evaluation (§4): Entwurf liegt bei eurofleet.**
- **Rubrik:** Sie ist vor dem ersten Lauf festgeschrieben. Es gibt drei Aufgaben je Harness:
  - ein schon gelaufener Code-Block mit Abnahmetests;
  - eine Bildaufgabe mit vorher aufgeschriebener Lösung, darunter die 14.6-Karte, mit direkter Bildeingabe und ohne `local_vision`;
  - ein lesender Zugriff über den Sharefyx-MCP.
- **Kennzahlen:** Abnahme, Eingriffe, Wanduhr, Kontingent laut MiniMax-Konsole, Befunde eines Opus-Reviews, ob der Bericht des Ausführers stimmt, Betrieb.
- **Ort:** Die Läufe sollen nicht in dieser Arbeitskopie stattfinden, sondern auf einem Testgast mit einem Klon auf festem Commit. Das Ergebnis wird nicht gemergt.
- **Offen beim Nikinger:** welcher Block, Termin, und ob „Claude Code auf MiniMax“ als dritte Variante dazukommt.
- **MiniMax Code laut Herstellerdoku:**
  - Es gibt keinen Server-Modus wie `opencode serve`.
  - Remote-MCP ist nur mit festen Headern beschrieben, OAuth nicht. Das betrifft den Sharefyx-MCP mit Passwort und TOTP.
  - Der Key liegt im Klartext in der Konfiguration.
  - Ob der Go-Key funktioniert, ist nicht dokumentiert.
  - All das wird vor einem Lauf geprüft.

**Hinweis an diese Session, ohne Auftrag:** Bleibt `local_vision` im Einsatz, können zwei Dinge helfen:
- geschlossene Fragen, zum Beispiel „Anzahl getrennter Bereiche: Zahl“;
- eine Regel, dass widersprüchliche Tool-Antworten als „unklar“ in den Bericht gehen.

Wie diese Session das umsetzt, entscheidet sie selbst. eurofleet ändert nichts am Repo.
