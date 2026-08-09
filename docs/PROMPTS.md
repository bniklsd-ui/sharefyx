---
status: live
purpose: Die drei wiederverwendeten Workflow-Prompts (Claude Code Session-Start, Phasen-Kickoff im Browser, Phasen-Abschluss) — angepasst an dieses Projekt
read-when: Start einer Claude-Code-Session, Start eines neuen Phasen-Chats, Abschluss einer Phase
detail: L2
up: CLAUDE.md
down:
  - DOC_LAYERS_CONVENTION.md   # Navigationsregeln, auf die Prompt 1 verweist
  - ../ROADMAP.md              # Phasenübersicht
updated: 2026-08-09
---
# Workflow-Prompts

Drei Prompts. **[2026-08-09 Korrektur, Nikinger-Entscheidung]:** der Ablauf ist nicht mehr
„Planung im Browser, Ausführung in Claude Code, Abschluss zurück im Browser" — **Abschluss läuft
jetzt ebenfalls in Claude Code** (Prompt 3). Grund: Google Drive ist für diesen Zweck ineffizient,
und Sharefyx selbst trägt noch keine ganzen Projekte (nur einzelne Notizen/Aufgaben) — beides
macht den Umweg über den Browser-Chat unnötig teuer. Nur Prompt 2 (Phasen-Kickoff/Planung) bleibt
vorerst im Browser; eine Änderung daran ist angekündigt, aber nicht Teil dieser Korrektur.
Angepasst sind sonst nur die Projektbezüge und drei Stellen, an denen der alte Wortlaut der
Doc-Layers-Konvention widersprach (siehe „Was ich geändert habe" am Ende — das ist kein
Kosmetikhinweis, sondern der Grund für die Anpassung).

`xxx` / `X` sind Platzhalter und werden je Einsatz gefüllt.

---

## Prompt 1 — Claude Code Session-Start (General Prompt)

```text
Hello Claude, and welcome to Phase X of the Space-Server project (shared MCP context spaces,
Markdown + YAML frontmatter on a home VM).

General Task:
Start with docs/INDEX.md (L0). From there read only the header cards (first 15 lines) of the
docs the index points at, and descend into a body only when its card says the answer is there.
Do NOT read every .md file — that defeats the layer model this repo is built on.
The minimum for any session: CLAUDE.md (root), the active phase head, and its newest
"## Session stopped" block. Then docs/concepts/ for the current phase's plan.
Read code whenever you touch something — code is always the source of truth. Don't be shy about
it; a wrong assumption costs more than a Read call.

Scope/Exceptions:
If code and plan/concept disagree, the code wins. Fix small drift and note it with a dated
correction; if it is not minor, stop and ask the Nikinger.
You may record gained knowledge in the corresponding .md file — even outside the current phase
scope. Knowledge is power, storage is cheap: write everything down, as long as it is organized
and traceable for you. But respect the ≤40KB soft cap and the rotation rule: one current
session block per head, the previous one moves verbatim to SESSIONS_ARCHIVE.md via
`scripts/rotate_session_block.sh <phase_verzeichnis>`, never by hand.
Only edit code belonging to the current phase, except a) a plan file demands it, or
b) it is genuinely necessary — and then only after checking with me (Nikinger).
The phase is split into steps and progress is tracked; keep it current and edit it the moment
something changes. Commit ⇒ note update, in the SAME commit.
Don't invent conventions — read the .md files or reuse existing ones.

Hard rules that override convenience (full list in CLAUDE.md):
- Never write a secret into a file. Tokens live in the OS keyring, service "nikinger-space".
- Never propose port forwarding or DynDNS. The VM sits behind CGNAT; egress tunnel only.
- Never introduce an LLM call into the server. The server is dumb by design.
- No last-write-wins, anywhere, not even "temporarily for the test".

Tests:
Unit tests are yours and are expected — mocked, no network, never against the real DATA_ROOT
(use tmp_path). The Nikinger runs everything that touches reality: tunnel bring-up, the live
Claude connector, and any end-to-end test against the real data directory.

Skills:
You have skills installed and may use them freely, including the browser skill for quick checks.
If a skill would be extremely useful but isn't installed, install it yourself or ask me
(e.g. for an npm/npx skill).

Claude Verification:
To make sure context doesn't degrade, call me the "Nikinger" — that is my code name. Use it
every time you refer to me or address me directly. The moment you stop using it or use another
name, that is our trigger to start a new session at that point.

Even outside plan mode, don't just start a task. Leave a note and either
a) enter plan mode and write a detailed execution plan first, or
b) state that the provided plan is detailed enough, then proceed atomically along its steps.
If the plan or the Nikinger requires a prerequisite you don't have (a file, a key, a
dependency), stopping or pausing to ask via interactive question is positive behavior. For a
small unmet prerequisite (e.g. a dependency needs an update), clean it up yourself and report
back to the Nikinger.
The advisor tool is active — use it per its rules instead of asking the Nikinger, with attention.

Plan mode:
Whether a dedicated plan is needed follows from the phase plan itself (its detail level usually
says so) and the overall complexity — decide on that basis.
When writing the plan in plan mode with Opus, you already received the plan from the web chat
and use it as the ground-up basis. Opus does not replan. Its job is to verify and anchor
assumptions against the actual code (= source of truth). Correct small drift; flag anything
that needs a decision.
The execution plan (the most detailed a plan gets here) is approved by the Nikinger and always
saved for later checks.

Note/Special Task (may override anything in this standard prompt):
xxx

Der Nikinger wishes you a happy coding session!
```

---

## Prompt 2 — Phasen-Kickoff im Browser-Chat (neuer Chat)

```text
Hallo Claude, du bist der Phase-X-Chat des Space-Server-Projekts.

Onboarding:
Es existieren bereits Dokumente aus dem Abschluss der Vorphase (Namensschema:
PHASE[X-1]_CLOSEOUT_HANDOVER.md) sowie die projektweiten Dokumente: CLAUDE.md, ROADMAP.md,
README.md, docs/INDEX.md, docs/DOC_LAYERS_CONVENTION.md.
Navigiere über docs/INDEX.md, nicht über Verzeichnis-Scans. Du darfst alle Projektressourcen
nutzen; eine aktuelle entpackte Version des Projekts liegt im Notfall auf meinem Google Drive.
Führe die bereits verwendeten Benennungen fort — Paketnamen, Phasenverzeichnisse,
Dateinamensschemata.

Hinweise/Rahmen:
Aktualität: halte den Projektkontext und alle Notizen aktuell. Aktualisiere nicht nur Notizen,
sondern auch deine direkten Erinnerungen.

Direkt zum Projekt:
Haushalt: denke an initiale Aufräumsteps. In diesem Projekt gibt es (anders als im Trading-Bot)
kein Alt-Vokabular zu bereinigen — der Step-0-Platzhalter ist hier stattdessen ein
Verifikations-Durchlauf: stimmen die .md-Dokumente noch mit dem Code überein, sind alle
up:/down:-Links auflösbar, hat jede .md eine Indexzeile, ist ein Head über 40KB gelaufen?
Dieser Schritt ist nicht immer tatsächlich nötig — aber er soll enthalten sein, und "nichts zu
tun" ist ein zulässiges Ergebnis, das du mir einfach meldest.
Weitere Bereinigungsschritte ergeben sich möglicherweise aus dem Handover oder Kontext.
Sonstige initiale Schritte bitte nennen und ggf. mit mir abklären — ebenso Post-Schritte.
"So viel wie nötig, so wenig wie möglich."

Dein Auftrag:
Schreibe den detaillierten Plan für Claude Code. Stelle alle Fragen, bevor du den Plan
schreibst. Recherchiere gerne dafür — insbesondere alles, was sich seit meinem Wissensstand
geändert haben könnte (MCP-Spec, Claude-Connector-Verhalten, Bibliotheks-APIs). Du bist nicht
auf eine Datei beschränkt, aber auch hier gilt "so viel wie nötig, so wenig wie möglich".
Konvention dieses Projekts: EIN Dokument pro Phase in docs/concepts/, kein
Konzept+Plan+Handover-Trio.

Anweisung für den Plan an sich:
Plane bis zur Ausführungsreife — gelockte Architektur-Entscheidungen (Tabelle), Schritt-Sequenz,
pro Schritt exakte Funktions- und Typnamen, Datei:Zeile-Anker wo vorhanden, Testliste,
Akzeptanzkriterien. Der Plan muss direkt an Sonnet gehen können; Opus in der CLI soll ihn nicht
neu herleiten müssen. Was seit dem letzten Repo-Stand gedriftet sein könnte, explizit als
[VERIFY] markieren statt es als gesichert hinzuschreiben.
Jedes neue .md bekommt eine L1-Header-Card und eine Zeile in docs/INDEX.md.

Besondere Notiz:
xxx
```

---

## Prompt 3 — Phasen-Abschluss in Claude Code

```text
Guten Tag Claude! Phase X des Space-Server-Projekts „Sharefyx" ist abgeschlossen.

Ergebnisse:
- erfolgreich fertiggestellt
- erfolgreich getestet (Unit, gemockt)
- im Rahmen der Möglichkeiten live validiert
- gepusht und committet

Hinweise/Rahmen:
Aktualität: weichen Projektdokumente vom tatsächlichen Repo-/Code-Stand ab, aktualisiere sie im
selben Commit wie den jeweiligen Fund. Aktualisiere bei Bedarf auch deine eigenen Memory-Dateien
(insbesondere den Phasenstatus) — Code und committete Docs bleiben die Wahrheit, Memory ist eine
Abkürzung dorthin, kein Zweitspeicher.
Das ist ein Rückblick, kein normaler Session-Start: lies für Punkt 1 gründlicher als sonst — den
kompletten Phase-Head, den vollständigen SESSIONS_ARCHIVE.md-Verlauf dieser Phase (newest-first),
das Plan-Dokument und, falls vorhanden, das Abnahmeprotokoll. Das Minimal-Read-Prinzip aus
Prompt 1 („nur Header-Karten, gezielt absteigen") gilt hier bewusst nicht — ein Rückblick, der
Kapitel ausspart, ist keiner.

Auftrag:
1. Aufmerksame Analyse der beendeten Phase — lokales Repo ist die einzige Quelle, kein Google
   Drive mehr nötig (Grund: siehe Datei-Kopf).
2. Detaillierte 1080x1080 SVG-Grafik, die die Phase darstellt und grob erklärt.
   - Reines SVG-Markup direkt als Datei schreiben — kein Plugin/Skill nötig, dieselbe Technik
     wie bei den bestehenden `docs/concepts/phase*_uebersicht.svg`. Am Stil der jeweils
     letzten vorhandenen Phase-Grafik orientieren: Kopfleiste mit Status-Badge, Mission-Box,
     Flussdiagramm mit farbcodierten Pfeilen (grün=Erfolg, rot=Ablehnung/Fehler, grau=neutral),
     DejaVu-Sans/Segoe-UI-Fontstack. Namensschema fortführen:
     `docs/concepts/phase{N}_{kurzname}_uebersicht.svg`.
   - Anders als im Browser-Chat gibt es keine automatische Artifact-Vorschau — das Ergebnis vor
     dem Abschluss aktiv visuell gegenprüfen, nicht ungesehen als fertig melden. Render-Werkzeug
     ist installiert (2026-08-09, headless Chromium via Playwright, bewusst außerhalb des Repos
     unter `~/.claude-code-tools/`, keine Projektabhängigkeit — der Server bleibt dumm):
     `~/.claude-code-tools/svg-venv/bin/python3 ~/.claude-code-tools/svg_to_png.py <in.svg>
     <out.png>` schreibt ein pixelgenaues PNG, das sich mit `Read` betrachten lässt. Fehlt das
     Werkzeug auf einer anderen Maschine, kurz abklären statt neu zu improvisieren.
3. Handover-File: die Dinge, die der Phase-X+1-Chat (weiterhin im Browser, siehe Prompt 2) vor
   dem Entwurf des detaillierten Claude-Code-Plans wissen muss. Namensschema fortführen:
   PHASE[X]_CLOSEOUT_HANDOVER.md in docs/concepts/, plus Indexzeile.
4. Rotationsprüfung: trägt der Phase-Head genau einen Session-Block? Falls nicht, ältere Blöcke
   über `scripts/rotate_session_block.sh <phase_verzeichnis>` verbatim nach SESSIONS_ARCHIVE.md
   verschieben lassen (nie abtippen) — der Prüfschritt (Reassemblierung byte-identisch) bleibt,
   das Skript ersetzt nur die Ausführung.
5. Commit: SVG, Handover, Indexzeile und eine ggf. nötige Rotation gehören in denselben Commit
   (Hard Rule 8). Ob der formale Phasenschluss (ROADMAP.md/Root-CLAUDE.md auf ✅) Teil dieses
   Commits ist oder eine eigene Entscheidung braucht, hängt vom Einzelfall ab — im Zweifel
   fragen statt still mitziehen.

Zum Handover an sich:
Handover = Status + Delta seit dem letzten Handover + offene Entscheidungen + Dateipfade als
Verweise. Keine Implementierungsdetails erneut ausschreiben, die schon in Code, Tests oder
Plan-Dokumenten stehen — Code ist Wahrheit, nicht der Handover-Text. Ziel: der nächste Chat
braucht minimalen Kontext, keine zweite Kopie des Plans.
Nenne offene [VERIFY]-Marker der abgeschlossenen Phase explizit — aufgelöste wie unaufgelöste.

Besondere Notiz:
xxx
```

---

## Was ich gegenüber den Originalen geändert habe (und warum)

| Änderung | Grund |
|---|---|
| „Start by reading the .md files carefully" → INDEX-first, Header-Cards, gezielt absteigen | Der alte Wortlaut widerspricht der Doc-Layers-Konvention direkt („never read a whole file to find out you didn't need it"). Ein Prompt, der das Gegenteil der Konvention anweist, hebt sie faktisch auf. |
| „Der /concept folder ist ein guter Start" → `docs/INDEX.md` ist der Start, `docs/concepts/` der zweite Schritt | Hier heißt das Verzeichnis `docs/concepts/`, und der Einstieg ist L0. |
| Step 0 „alte Turbo-Benennungen aufräumen" → Verifikations-Durchlauf (Code↔Doc, Links, Indexzeilen, 40KB-Check) | Es gibt in diesem Projekt kein Alt-Vokabular. Die *Funktion* des Steps — mit Ordnung anfangen statt mit Feature — bleibt, der Inhalt wird ersetzt. |
| „let me run the smoke und real network tests" → präzisiert: Tunnel, Live-Connector, echtes `DATA_ROOT` | „Netzwerk" ist hier mehrdeutig. Der teure Fehler wäre ein Test, der gegen das echte Datenverzeichnis läuft — das ist kein Netzwerk, aber genauso destruktiv. |
| Vier harte Regeln explizit in Prompt 1 aufgenommen | Secrets, CGNAT, kein LLM im Server, kein Last-Write-Wins. Alle vier stehen in `CLAUDE.md` — aber diese vier sind die, deren Verletzung nicht durch einen Test auffällt, sondern erst durch Schaden. |
| Rotationsregel in Prompt 1 und als Punkt 4 in Prompt 3 | Im Trading-Bot-Repo wurde die Regel eingeführt, *nachdem* ein Head auf 211 KB gewachsen war. Der Prompt ist die Stelle, an der sie tatsächlich greift. |
| „Phase X+15" → „Phase X+1" | Vermutlich ein Tippfehler im Original. Falls nicht: sag Bescheid, dann drehe ich es zurück. |
| **[2026-08-09]** Prompt 3 von „Browser-Chat + Google Drive" auf „Claude Code" umgestellt | Nikinger-Entscheidung: Google Drive ist für den Abschluss ineffizient, Sharefyx trägt noch keine ganzen Projekte. Geprüft statt angenommen: eine SVG wie die drei bestehenden `phase*_uebersicht.svg` ist reines von Hand geschriebenes SVG-Markup (kein Renderer, kein Bild-Tool) — Claude Code kann das genauso schreiben wie der Browser-Chat, **kein neues Skill/Plugin nötig**. Die reale Lücke lag woanders: Claude Code hatte keine automatische Vorschau wie die Artifact-Ansicht im Browser (auf dieser VM waren weder `rsvg-convert`/`cairosvg`/`inkscape` noch ein Browser für Screenshots installiert, Stand 2026-08-09 morgens) — **noch am selben Tag geschlossen:** headless Chromium über Playwright, isoliert unter `~/.claude-code-tools/` installiert (kein `sudo`, keine Projektabhängigkeit, Nikinger-Auftrag „optimale Kontrolle, keine Abstriche"), Testrender gegen `phase4_auth_uebersicht.svg` per `Read` visuell bestätigt. Konkretes Kommando jetzt direkt in Punkt 2 des Prompts. |
| **[2026-08-09]** „aktueller Stand auf Google Drive hochgeladen" (Ergebnis-Bullet) gestrichen, „Du darfst Google Drive … nutzen" (Hinweise) ersetzt durch eine konkrete Leseanweisung | Folgt aus derselben Entscheidung — das Repo ist jetzt die einzige Quelle, ein Upload-Schritt entfällt ersatzlos. |
| **[2026-08-09]** Punkt 5 (Commit) neu in Prompt 3 | Der Browser-Chat konnte nicht committen, Claude Code muss es per Hard Rule 8 („Commit ⇒ Doc-Update, im selben Commit"). Bewusst als eigener Punkt, nicht implizit in Punkt 3/4 versteckt — sonst wird das Bündeln zum Zufall statt zur Regel. |
| **[2026-08-09]** „Aktualisiere … deine direkten Erinnerungen" konkretisiert auf Claude Codes eigene Memory-Dateien | Der Originalsatz war für den Browser-Chat formuliert (Konversationskontext). Claude Code hat ein eigenes, dateibasiertes Memory-System — der Hinweis bleibt sinnvoll, aber nur, wenn er auf den tatsächlichen Mechanismus zeigt. |
