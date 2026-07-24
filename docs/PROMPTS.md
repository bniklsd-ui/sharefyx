---
status: live
purpose: Die drei wiederverwendeten Workflow-Prompts (Claude Code Session-Start, Phasen-Kickoff im Browser, Phasen-Abschluss) — angepasst an dieses Projekt
read-when: Start einer Claude-Code-Session, Start eines neuen Phasen-Chats, Abschluss einer Phase
detail: L2
up: CLAUDE.md
down:
  - DOC_LAYERS_CONVENTION.md   # Navigationsregeln, auf die Prompt 1 verweist
  - ../ROADMAP.md              # Phasenübersicht
updated: 2026-07-24
---
# Workflow-Prompts

Drei Prompts, unverändert im Ablauf gegenüber dem Trading-Bot-Projekt: **Planung im Browser,
Ausführung in Claude Code, Abschluss zurück im Browser.** Angepasst sind nur die Projektbezüge
und drei Stellen, an denen der alte Wortlaut inzwischen der Doc-Layers-Konvention widerspricht
(siehe „Was ich geändert habe" am Ende — das ist kein Kosmetikhinweis, sondern der Grund für
die Anpassung).

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
session block per head, the previous one moves verbatim to SESSIONS_ARCHIVE.md.
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

## Prompt 3 — Phasen-Abschluss im aktuellen Chat

```text
Guten Tag Claude! Phase X des Space-Server-Projekts ist abgeschlossen.

Ergebnisse:
- erfolgreich fertiggestellt
- erfolgreich getestet (Unit, gemockt)
- im Rahmen der Möglichkeiten live validiert
- gepusht und committet
- aktueller Stand auf Google Drive hochgeladen

Hinweise/Rahmen:
Aktualität: weichen Projektdokumente von den hier im Kontext hochgeladenen ab, aktualisiere
bitte. Aktualisiere nicht nur Notizen, sondern auch deine direkten Erinnerungen.
Du darfst Google Drive und den gesamten Projektkontext für diesen Auftrag nutzen.

Auftrag:
1. Aufmerksame Analyse der beendeten Phase (via Google Drive).
2. Detaillierte 1080x1080 SVG-Grafik, die die Phase darstellt und grob erklärt.
3. Handover-File: die Dinge, die der Phase-X+1-Chat vor dem Entwurf des detaillierten
   Claude-Code-Plans wissen muss. Namensschema fortführen: PHASE[X]_CLOSEOUT_HANDOVER.md in
   docs/concepts/, plus Indexzeile.
4. Rotationsprüfung: trägt der Phase-Head genau einen Session-Block? Falls nicht, ältere Blöcke
   verbatim nach SESSIONS_ARCHIVE.md verschieben (mechanisch, nie abtippen, Reassemblierung
   byte-identisch prüfen).

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
