---
status: snapshot
purpose: "Abschluss-Handover P8.6 → P9 — Status, Delta seit dem Partial-Closeout vom 2026-09-13, offene UND entschiedene Punkte für die P9-Planung (Nikinger-Feedback vom 2026-09-19 in §4.1, drei Entscheidungen im §4-Kopf, GPU-Dienst-Empfehlung in §4.8), [VERIFY]-Bilanz mit den zwei offenen Markern. Phase 8.6 ist abgeschlossen und als v3.0.2 live."
read-when: vor dem Entwurf des P9-Plans einmal ganz lesen — ersetzt das Nachlesen von Phase-Head und SESSIONS_ARCHIVE für alles außer der Detailhistorie
detail: L2
up: ../../ROADMAP.md
down:
  - ./phase8_6_ui_polish_plan2.md                   # Plan 2 — §9 ist der KANONISCHE Closeout der Phase (P8.6-W)
  - ./phase8_6_ui_polish_plan.md                    # Plan 1 (📕) — Historie der Blöcke A–D, §9 nur Zeiger
  - ../../phase8_6_ui_polish/CLAUDE.md              # Phase-Head — Modul-Status, Vormerkungen
  - ../../phase8_6_ui_polish/SESSIONS_ARCHIVE.md    # volle Phasenhistorie, verbatim, newest-first
  - ./p8x_ui_polish_notes.md                        # Inhaltsquelle §1–§10; P9 erbt §2/§2.5/§4/§7/§8/§9/§10.8/§10.9
  - ./PHASE8_5_CLOSEOUT_HANDOVER.md                 # Vorgänger — §4.7 das geerbte Ledger, weiter offen
  - ./sichtpruefung_automation_conventions.md       # §2 Visuelles ist Nikinger-Sache · §5 screenshots_latest
updated: 2026-09-19 (Abschluss-Handover P8.6 → P9; ersetzt den Partial-Closeout-Stand vom 2026-09-13, der in `373a431` erhalten bleibt. **Nachtrag desselben Tages: drei Nikinger-Entscheidungen eingearbeitet** — Domain als früher P9-Schritt (§4.2), Tailscaled-Watchdog freigegeben (§4.3, mit der Tabelle welcher der drei Ansätze den gemessenen Vorfall überhaupt deckt), und **neu §4.8**: die ungenutzte RTX 3060 bekommt einen eigenen internen CUDA-Dienst, der die CPU-only-Vision-Strecke ablöst — Empfehlung LXC auf dem 3060-Host, Form entscheidet die Planungssession)
---
# Phase 8.6 — Closeout-Handover (P8.6 → P9)

> **Phase 8.6 ist abgeschlossen und ausgeliefert.** `v3.0.2` läuft seit dem **2026-09-18** aus
> Release `20260918T183907.597248Z`, SHA **`1ad2665`**, `health_gate.sh` **9/9 grün**.
> Abnahme **45 ✅ · 5 ⚠️ · 0 ⬜ · 4 ersetzt** von 54 Zeilen, `pytest` **995 passed**.
>
> **Der kanonische Abschluss steht nicht hier, sondern in `phase8_6_ui_polish_plan2.md` §9**
> (Lock P8.6-W). Dieses Dokument ist der **Handover**: Status, Delta, offene Entscheidungen,
> Pfade. Es wiederholt keine Implementierungsdetails — Code ist die Wahrheit.

> **Dieses Dokument ersetzt den Partial-Closeout-Stand vom 2026-09-13** (gleicher Pfad, andere
> Aufgabe: damals Plan 1 → Plan 2, heute P8.6 → P9). Die alte Fassung ist erhalten:
> `git show 373a431:docs/concepts/PHASE8_6_CLOSEOUT_HANDOVER.md`. Zwei ihrer Abschnitte werden
> von ROADMAP, Phase-Head und Plan 2 namentlich zitiert und deshalb hier in einem Satz
> gesichert, damit die Verweise nicht ins Leere zeigen:
> **§4.5** = die vier Nikinger-Entscheidungen vom 2026-09-13 (Deploy-Ziel bleibt `v3.0.2` ·
> Block C wird einzeln gepusht · Ein-Block-Regel für die Wurzel-`CLAUDE.md` verworfen ·
> **Push ja, Deploy nein**).
> **§4.6** = der am Server gemessene Befund, dass von P8.6 zu diesem Zeitpunkt **nichts** live
> war — die Doku-Behauptung „Block A+D deployed, `health_gate` 8/8" war nie gelaufen.

---

## 1 Status in fünf Sätzen

1. **Die Phase hat zwei Pläne und drei Sichtungs-Revisionen gebraucht, und das war richtig so.**
   Plan 1 (Blöcke A–D) wurde am 2026-09-12 **nicht abgenommen** — die Nikinger-Sichtprüfung gab
   neun UX-Befunde zurück statt der Freigabe. Plan 2 arbeitete sie ab (E/F/G/H/J) und brauchte
   dafür selbst **G-R**, **H-R** und **H-R-3**: drei Runden, in denen erst die Pixel zeigten, was
   der Quelltext verdeckt hatte.
2. **Gemessen, nicht behauptet:** `pytest` **995 passed in 117,6 s**, `ui_budget.py` **5/5**
   (144,7 KB von 250 KB), 38 Commits, **930 / 256** Zeilen Produktcode über 12 Dateien,
   **1.556 / 44** in den Tests, Smoke **18/18** über zwei Browser.
3. **Keine neunte P1-Contract-Öffnung.** Der Tabu-Diff über die ganze Phase ist leer — mit
   **genau einer** vorher angekündigten, datierten Ausnahme (P8.6-AJ, Block J): zwei Dateien in
   `phase4_auth/authserver`, in `store.py` exakt zwei Zeilen.
4. **Zwei `[VERIFY]`-Marker gehen offen an P9 über**, nicht stillschweigend geschlossen:
   **V118** (Zwillingskanten-Linienzahl) und **V136** (Chip-Umstellung vs. Drag-and-Drop-Ziel) —
   letzterer hat durch das Nikinger-Feedback vom 2026-09-19 nachträglich einen realen Anlass
   bekommen, §4.1.
5. **Hard Rule 9 hat über die gesamte Phase gehalten:** kein `pkill -f`, kein `systemctl` durch
   einen Agenten; `sharefyx-mcp` (PID 991) wurde ausschließlich gelesen, jeder `systemctl`-Aufruf
   lief über den Nikinger, jede Wegwerf-Instanz über PID-Datei oder Port.

---

## 2 Delta seit dem Partial-Closeout (2026-09-13)

**23 Commits**, `bc2aa9f..860ed72`. Was davor lag, steht im alten Handover (`373a431`).

| Etappe | Ergebnis | Commit |
|---|---|---|
| Plan 2 geschrieben | sechs Nikinger-Entscheidungen N.7–N.12, Locks P8.6-W–AL, Abnahme 33–54, VERIFY V123–V139 | `ba31167` |
| **Block E — messen, nicht bauen** | **V125 geschlossen: 9a = 9b.** Die Plan-Annahme „Block C hat 9b eingeführt" war falsch; Auslöser ist die 140-px-Banner-Höhe, auf `v3.0.1` byte-identisch reproduziert | `f8e413c`, `cc3f342` |
| Block F — Layering | `--panel-meta*` verlieren den `--warn`-Bezug (gemessen: `rgba(229,169,60,.22)` **ist** `--warn` bei 22 %), drei rohe Flächen-Hex auf Token, zwei Wächter | `a56a30c` |
| Block G + G-R | `.shell` → `240px 480px 1fr` (P8.6-O2 ausgelöst **und entschieden**), Übersicht in den Listen-Slot, Karte allein im Detail-Slot, **ESC stellt sie wieder her**; Breakpoints 1200/1024, Layer-Ton vereinheitlicht, Editor-Head sticky | `081c432`, `6a43edf`, `7b4dc30` |
| Block H + H-R + H-R-3 | Rail-Umkehr (Abmelden bleibt äußerster Knopf), `.account-nav` mit Afford; OLED-BLACK für die drei Slots, YAML-Bündigkeit (27,14 → 0,86 px); 1024 ohne Map, Editor-Fullview, Listen-Slot exklusiv | `abed4c1`, `c615e3d`, `5d8bc4d`, `c734bd0`, `c9fcae0` |
| Block J | `pytest`-Flake an der **Wurzel**: `secrets.token_urlsafe(16)` liefert in **1,569 %** ein führendes `-`, `argparse` liest es als Optionsflag. `crypto.new_public_id()` mit Rejection-Sampling | `fdde9a4` |
| Gate GA1–GA4 | Wegwerf-Ritt, `p86_polish_smoke.py` (14 Stationen, 18/18), Nikinger-Sichtprüfung, Badge `v3.0.2` + `UPDATE_LOG`, Deploy, Health-Gate 9/9 | `4a07752`, `1ad2665`, `860ed72` |
| (nebenbei, P3-Eigentum) | Tailscale-Account-Migration: Funnel-Hostname gewechselt, Tunnel wiederhergestellt; Domain-Empfehlung als P9+-Vormerkung abgelegt | `d774876`, `782f046` |

**Ein Deploy-Blocker, der ohne den Deploy nie sichtbar geworden wäre:** `deploy.sh` brach beim
`git clone` mit `Invalid path '.../.git': Permission denied` ab. Eigentümer, Gruppe, Mountpunkt
und Plattenplatz waren alle in Ordnung — Ursache war ein **`umask 0177`** in der Nikinger-Shell:
`git clone` legt Verzeichnisse mit `0777 & ~umask` an, bei `0177` ergibt das `0600`, also kein
Execute-Bit und damit ein Verzeichnis, das nicht einmal sein Eigentümer betreten kann. `ls -la`
zeigt diese Klasse Fehler nicht, solange man nicht das neu angelegte Kind-Verzeichnis prüft.
Fix + Regressionstest: `phase5_ui/scripts/deploy.sh` (setzt jetzt selbst `umask 022`) und
`test_deploy_succeeds_under_a_restrictive_ambient_umask`.

**Stand von `main` gegen live:** live `1ad2665`, `main` **`860ed72`**. Die Differenz ist
`deploy.sh` + sein Test + Doku, **kein Anwendungs-Code**. Der nächste Deploy zieht sie nach.

---

## 3 Abnahmestand

**Vollständig in `phase8_6_ui_polish_plan2.md` §9.3**, Zeile für Zeile mit Beleg. Hier nur die
Bilanz und die fünf Zeilen, die *nicht* glatt ✅ sind — weil genau die ein P9-Planer kennen muss:

**45 ✅ · 5 ⚠️ · 0 ⬜ · 4 ersetzt** (von 54 Zeilen über beide Pläne).

| Zeile | Warum ⚠️ |
|---|---|
| **P8.6-15** | Der B4-Sweep fand statt, sein Ergebnis hält ein Test — eine *Zuordnungstabelle im Phase-Head*, wie die Zeile sie wörtlich fordert, wurde nie geschrieben. Das Kriterium war zu eng, nicht der Sweep zu dünn |
| **P8.6-17** | Token-Drift weg; vier `border-radius: 999px` bleiben — Pillenform, kein Token |
| **P8.6-20** | Kein sichtbares Label „Konto" mehr; Restvorkommen sind das deutsche Wort in Sperrmeldungen (`api.py:302`) |
| **P8.6-25** | `dedupeEdges()` ist per `node`-Probe belegt, die **visuelle** Bestätigung fehlt — **V118**, siehe §5 |
| **P8.6-44** | Die `--panel-meta*`-Tokens tragen keinen `--warn`-Bezug mehr (Befund 8 ist weg), aber `app.css:770`/`:1306` behalten `rgba(229,169,60,.10)` — beides **echte Warnungen** mit `border`/`color: var(--warn)`. Die Zeile forderte `grep = 0` und war damit zu breit |

**Eine ✅-Zeile mit einer Zahl, die man messen kann und die dann anders aussieht:** **P8.6-41**
fordert „Karte ist bei 1440 px ≥ 700 px breit". Der `.detail`-Slot **ist** 720 px (die
P8.6-X-Rechnung 1440 − 240 − 480). Die **Zeichenfläche** misst 654 × 810 px — die Differenz ist
`.detail__graph { padding: 16px 32px }`. Wer am Bildschirm nachmisst, misst 654. Die Zeile ist
erfüllt, aber sie meint den Slot; das gehört benannt, bevor es jemand als Abweichung entdeckt.

**Vier ersetzte Zeilen:** P8.6-21/-22 sind durch die Befunde 4 und 9 widerlegt (Nachfolger
P8.6-41/-50, so in Plan 2 §8.1 benannt). **P8.6-18/-19 sind zusätzlich still obsolet geworden** —
die Rail-Umkehr N.9/P8.6-AE hat sie umgedreht, Nachfolger ist P8.6-42. Plan 2 hatte nur die
ersten beiden als ersetzt gekennzeichnet; der Nachtrag steht in §9.3.

---

## 4 Entscheidungen für die P9-Planung — drei getroffen, der Rest offen

> **[2026-09-19, Nikinger-Entscheidungen — drei der hier gelisteten Punkte sind entschieden.]**
> **(1) Die Domain kommt als einer der ersten Schritte in P9** — nicht mehr „P9+ Kandidat",
> siehe §4.2. **(2) Der Tailscaled-Watchdog wird gebaut**, siehe §4.3. **(3) Neu und nicht aus
> P8.6 stammend: die ungenutzte RTX 3060 (12 GB) im Proxmox-Verbund bekommt einen eigenen
> Dienst**, der die CPU-only-Vision-Strecke ablöst — Entscheidung „ja, Form nach Empfehlung",
> die Ausarbeitung gehört in die Planungssession. **§4.8**, und sie beantwortet §4.6.

### 4.1 Neues Nikinger-Feedback vom 2026-09-19 — acht Punkte, drei Klassen

Übergeben mit dem Closeout-Auftrag, **nicht** in P8.6 bearbeitet. Bewusst nicht als flache
Feature-Liste abgelegt: drei der acht sind keine UI-Politur.

**(a) Zwei Bugs — mit einer ersten Messung, nicht bloß weitergereicht**

| Meldung | Erster Befund (2026-09-19, read-only gemessen) |
|---|---|
| **„Drag and Drop aus selbst erstellten Ordnern geht nicht"** | `bindFolderDropTarget()` (`tree.js:119`) hat **genau eine** Aufrufstelle: `tree.js:205`, `if (space.own)` — auf Ordner-Buttons. Es gibt damit ein Drop-Ziel **in** einen Ordner hinein, aber **keines zurück auf die Space-Wurzel**. „Rein ja, raus nein" ist kein Glitch, sondern ein fehlendes Ziel. Der Menü-Pfad (`list.js`, `.list__row-move`) ist die bestehende Alternative. **Berührt V136** (§5), die genau diese Gegend betrifft und nie beantwortet wurde |
| **„Bei ESC geht die Vollbild-Version auf Mac aus; Item schließt sich trotzdem"** | Der globale Handler `app.js:204` (`document.addEventListener("keydown", …)`) prüft **nicht** auf `document.fullscreenElement`. Der Browser verlässt den Vollbildmodus und derselbe Tastendruck erreicht zusätzlich die App — zwei Aktionen auf einen Druck. **Relevanz erhöht:** P8.6 hat ESC an **drei** Stellen tragend gemacht (N.8 Karte-zurück, H-R.7 Editor-Fullview, H-R.8 Listen-Slot) — der Doppeleffekt trifft jetzt mehr Pfade als vor der Phase |

**(b) Ein Rechte-Thema, kein CSS-Thema**

**„Teilen / Verschieben in fremde, nicht-eigene Root-Spaces."** Heute gilt in der UI
durchgängig ein Eigentümer-Riegel: der Verschieben-Knopf erscheint nur für eigene, schreibbare
Items (`list.js`, `movable`), das Drop-Ziel nur `if (space.own)` (`tree.js:205`). Das ist
**absichtlich konservativer** als der Server. **Hard Rule 4 in ihrer P6-U-Neufassung** sagt:
Schreibrechte folgen der **Mitgliedschaft**, nicht dem Token — ein fremder Ziel-Space ist
zulässig, wenn er in einer `.share.yml` unter `write:` steht oder das Item `share_write` trägt.
Wer das plant, plant an der Rechte-Grenze, nicht an der Oberfläche: `docs/concepts/
phase6_shares_plan.md` §0.7(a)/§1.2 ist der Einstieg, **nicht** `app.css`.

**(c) Fünf gewöhnliche Feature-Wünsche für die P9-Planung**

| Wunsch | Anmerkung für den Planer |
|---|---|
| **Logo + einheitliche Design-Vorlage für alle künftigen UI-Elemente** | Es gibt bereits eine: die **Selection/Choice-Konvention v3** in `phase8_ui_graph/CLAUDE.md`, seit P8.6 Block A mit fünfter Kategorie „Vorsicht". Der Wunsch ist ihre Erweiterung zu einer vollen Vorlage (plus Logo), nicht ihr Ersatz — sonst entstehen zwei Konventionen für dieselbe Frage |
| **To-do-Checkboxen im Text** | Berührt `markdown.js` (Renderer) **und** den Schreibpfad; wer ein Häkchen klickbar macht, schreibt zurück — damit ist Hard Rule 3 (`version` bei jedem Write) im Spiel, nicht nur Darstellung |
| **„Ich arbeite gerade daran" markieren / auffällig highlighten** | Nikinger dazu: *„sowas wie ‚aktuelle Aufgabe' auf der Übersichtsseite"*. Die Übersicht liegt seit Block G im Listen-Slot — der Platz dafür existiert, die Datenfrage (Frontmatter-Feld? eigener Status?) nicht |
| **Eine Aufgabe sich selbst „assignen"** | Gehört zum vorigen Punkt; gemeinsam planen, sonst entstehen zwei Felder für einen Zustand |
| **Dateien vollständig löschen — nach zweifacher Rückfrage, human-only, kein Bulk, Namenseingabe als Gate** | Löschen steht seit P5 als **F2** im geerbten Ledger draußen. Der Wunsch ist explizit: kein Bulk, Name eintippen, nur Mensch. Das ist ein Sicherheits-Design, kein Knopf — und es berührt die Git-Historie im Datenverzeichnis (Hard Rule 5) |

### 4.2 Echte Domain statt `<node>.<tailnet>.ts.net` — **entschieden: früher P9-Schritt**

**[2026-09-19] Der Nikinger hat entschieden: die Domain wird als einer der ersten Schritte in
P9 eingebaut.** Damit ist der Punkt aus der „P9+"-Warteschleife heraus und hat eine Position in
der Build-Reihenfolge. Die Wahl des Weges (CNAME vs. eigener Reverse-Proxy) ist damit **nicht**
mitentschieden — das ist Planungsarbeit, und sie hängt daran, welche Domain beschafft wird.

**Warum früh und nicht spät:** eine Adressänderung zieht den Claude-Connector in **beiden**
Konten nach sich (der steht bis heute auf dem alten Hostnamen, siehe `phase3_edge/CLAUDE.md`).
Wer die Domain erst am Ende von P9 einzieht, macht diesen Schnitt zweimal — einmal jetzt und
einmal beim nächsten Tailnet-Wechsel.

Hintergrund (Vormerkung `782f046`, Phase-Head §Vormerkungen): Anlass war ein **realer
Vorfall**, keine Kosmetik: eine Tailscale-Account-Migration hat den Funnel-Hostnamen komplett
gewechselt (`tail89fc2a.ts.net` → `tail4a8b49.ts.net`) — die zweite Adressänderung in der
Betriebsdauer. Zwei Wege, keiner entschieden: CNAME auf den Funnel-Hostnamen (klein, DNS
genügt, Funnel bleibt TLS-Terminierung) oder eigener Reverse-Proxy mit Let's Encrypt (groß,
löst die Tailscale-Kopplung). **Beide brauchen eine Domain — die Beschaffung bleibt
Nikinger-Sache, kein Agenten-Auftrag.** Herleitung: `phase3_edge/CLAUDE.md`,
Session-Block 2026-09-18.

### 4.3 Tailscaled-Watchdog — **entschieden: wird gebaut**

Vorfall 2026-09-15: nach ~4 h VM-Suspend kam `tailscaled` nicht mehr auf die Control-Plane,
`sharefyx-mcp` antwortete lokal weiter mit 200, das Node war extern aber **offline**. Die
vorhandene Restart-Logik deckt nur Crashes (`Restart=on-failure`), nicht „Dienst läuft,
Control-Plane klemmt". **[2026-09-19] Der Nikinger hat den Watchdog freigegeben.**

Drei Ansätze stehen im Phase-Head §Vormerkungen. **Nur einer davon deckt den gemessenen
Vorfall** — das ist keine Empfehlung, sondern eine Eigenschaft der Ansätze:

| Ansatz | Deckt „Dienst läuft, Control-Plane klemmt"? |
|---|---|
| 1 — `OnFailure=`-Hook auf eine zweite Unit | **Nein.** Feuert nur, wenn die Unit fehlschlägt; am 2026-09-15 lief `tailscaled` durchgehend |
| 2 — eigene `tailscaled-watchdog.service`, zyklische Prüfung (`tailscale netcheck` bzw. `curl` gegen die Control-Plane), bei Fehlschlag `systemctl restart tailscaled` | **Ja.** Der einzige Ansatz, der den beobachteten Zustand überhaupt sieht |
| 3 — Tailscale-eigenes Feature | **Unbekannt**, Recherche offen; vermutlich nicht ohne kommerzielles Add-on |

Die Planungssession entscheidet die Form; die Tabelle nimmt ihr die Messarbeit ab, nicht die
Wahl. Unverändert gilt: der Auslöser **muss** systemd sein, nicht ein Agent (Hard Rule 9), und
die Unit ist mit `User=`, `NoNewPrivileges=true`, `ProtectSystem=strict` zu härten.

### 4.4 `docs/INDEX.md` — die Rotation ist überfällig

Dritter Budget-Verstoß in einer Phase: bei Step-Z-Beginn **45.870 B** gegen das ≤-38-KB-
Kriterium. In diesem Commit wieder von Hand gestrafft. Die Ursache ist seit 2026-09-11 benannt
und unverändert: die **`updated:`-Frontmatter-Kette**, nicht der Body. Die Lösung —
`docs/INDEX_UPDATES_ARCHIVE.md` plus eine Rotation analog `scripts/rotate_session_block.sh` —
ist geplant, aber nie gebaut worden. **Empfehlung: in P9 bauen, nicht wieder vertagen** — die
Handarbeit hat jetzt dreimal nicht getragen.

**Konkreter Stand nach dieser Straffung: 38.756 B.** Das Kriterium liegt bei 38.912 B — das sind
**156 Byte Luft**, kein Spielraum. Die nächste neue `.md` mit INDEX-Zeile reißt das Kriterium
sofort wieder; wer eine anlegt, muss im selben Commit straffen oder die Rotation bauen. Allein
das Eintragen der drei Entscheidungen vom 2026-09-19 (§4.2/§4.3/§4.8) hat **229 B** gekostet und
musste durch das Straffen zweier abgeschlossener Phasen-Zeilen gegenfinanziert werden — genau
der Kreislauf, den die Rotation beenden soll.

### 4.5 Versionsziel und Nummerierung

`v3.1.0` für P9 ist vorgemerkt (Minor-Bump, „laut Nikinger voraussichtlich letzter großer
UI-Umbau"), **ein P8.7 existiert nicht** (entschieden 2026-09-09). Ein Minor- statt Patch-Bump
ist eine Nikinger-Entscheidung, nie die eines Agenten — P8.6 hat die Regel eingehalten
(P8.6-R bestätigt am 2026-09-13).

### 4.6 Sichtprüfungs-Werkzeug — die offene Wunde der Phase

Der Nikinger am 2026-09-14, nach der G-R-Sichtung: *„die Realität ist recht weit weg von dem
was du hier beschreibst."* Das ist der Kern: **opencode/M3 beschreibt seine eigenen Screenshots
geglättet**, und drei der fünf Revisionsrunden dieser Phase gehen darauf zurück. Zwei Optionen
liegen als Vormerkung bereit (Rückkehr zum manuellen Ollama-Adapter mit Batch-Aufruf gegen den
Cold-Start / zwei Modell-Instanzen als getrennte Phase), **keine ist entschieden**.

**[2026-09-19] Die Hardware-Hälfte dieser Frage ist beantwortet: §4.8.** Der Grund, warum
Option (A) bisher unattraktiv war, ist der **Cold-Start von 46–180 s auf CPU** — mit der
3060 fällt genau dieser Einwand weg. Die inhaltliche Hälfte („wer beurteilt das Bild, und mit
welchem Prompt") bleibt offen und gehört in die Planungssession. Das
OpenCode-Plugin ist kein Weg: gemessen (Befund 2c) zerstört es M3s nativen Bildpfad, und das
Web-UI hat keinen Tool-Result-Bild-Slot — Konvention §4 ist dort **dauerhaft unerfüllbar**.

### 4.7 Geerbtes Ledger — unverändert offen

P8.6 hat davon nichts angefasst und nichts still abgeräumt: Body-Volltextsuche (Q1),
Rechteverwaltung über MCP-Tools (P6-M), Löschen von Items (F2 — siehe aber §4.1c),
FastMCP-4 (V79), Realtime, Light-Mode (P5-X), Bulk-Append-MCP-Tool, Ordner umbenennen
(Analyse in `phase8_6_ui_polish_plan.md` §0.4.1 — die billige Fassung verliert still eine
`.share.yml`-Freigabe). Voller Stand: `PHASE8_5_CLOSEOUT_HANDOVER.md` §4.7.

### 4.8 GPU-Dienst für die Sichtprüfung — **entschieden: ja, Form nach Empfehlung**

**[2026-09-19, Nikinger-Entscheidung.]** Im Proxmox-Verbund hängt eine ungenutzte **RTX 3060
(12 GB)**. Sie bekommt einen eigenen, internen Dienst, der seine CUDA-Leistung anbietet und die
**CPU-only-Vision-Strecke ablöst**. Die genaue Form ist als Empfehlung erbeten und wird in der
P9-Planungssession festgelegt — was hier steht, ist Vorarbeit, keine Entscheidung.

**Eine Präzisierung vorweg, weil sie sonst in die Planung einwandert:** das *Plugin*
(`DavidEasden/opencode-vision`) ist bereits **seit dem 2026-09-11 zurückgebaut** — gemessen,
nicht vermutet: es amputiert M3s nativen Bildpfad. Was der GPU-Dienst ersetzt, ist also nicht
das Plugin, sondern das **CPU-only-Ollama-Backend** auf der sharefyx-VM (Ollama 0.34.0 +
`qwen3-vl:8b`, `127.0.0.1:11434`).

**Empfehlung: eigener LXC-Container auf dem 3060-Host, Ollama darin, erreichbar als interner
HTTP-Dienst auf der Proxmox-Bridge.** Nicht in die sharefyx-VM, und kein Passthrough in die
Produktions-VM. Fünf Gründe, in der Reihenfolge ihres Gewichts:

1. **Das Bauprinzip bleibt physisch, nicht bloß versprochen.** „Der Server ist dumm" heißt: kein
   LLM-Call im Serverpfad. Das Vision-Modell bedient die **Sichtprüfung des Agenten**, niemals
   eine sharefyx-Anfrage. Steht es in einer eigenen Kiste, ist diese Grenze nachprüfbar; steht es
   in der sharefyx-VM, muss jeder künftige Leser dem Satz glauben. Genau diese Unterscheidung ist
   der Grund, warum die Wurzel-`CLAUDE.md` „wer hier ein LLM einbauen will → stop" schreibt — der
   GPU-Dienst verletzt die Regel **nicht**, aber nur, solange er außerhalb steht.
2. **Die Client-Seite ist bereits verdrahtet und konfigurierbar — es ist kein Code-Änderung.**
   `mcp_local_vision_server.py:195` liest den Endpoint aus **`LOCAL_VISION_ENDPOINT`**,
   `vision_ollama.py:44` hat ein `--endpoint`-Flag. Der Umzug ist **eine Umgebungsvariable**.
   Wer stattdessen die Karte in die sharefyx-VM reicht, spart diese eine Variable und bezahlt mit
   einem Treiber-Stack in der Produktions-VM.
3. **Der Ops-Grund, der schwerer wiegt als das Prinzip: die sharefyx-VM bleibt migrierbar.**
   Die Karte steckt in **einem** Host; ein Passthrough — egal ob in die sharefyx-VM oder in eine
   VM daneben — **pinnt diese VM auf genau diesen Host**. Die Proxmox-Vormerkung führt
   ausdrücklich einen primären (i5-14600KF) **und** einen sekundären Node (Ryzen 7 5800X), und
   die Migration von 2026-09-10 hat das schon einmal genutzt. Steckt das Modell in einer eigenen,
   auf den 3060-Host gepinnten Kiste, ist genau **eine** Sache unbeweglich — die, die im
   Zweifelsfall auch stillstehen darf. Steckt es in der sharefyx-VM, verliert die Produktion ihre
   Beweglichkeit, um eine Sichtprüfung zu beschleunigen.
4. **LXC statt voller VM mit PCIe-Passthrough:** kein VFIO/IOMMU-Blacklisting, kein Risiko für
   die Host-Konsole, geringerer Overhead, Snapshots funktionieren. **Zwei bekannte Preise, damit
   sie in der Planung budgetiert werden und nicht überraschen:**
   **(a) „Treiber lebt auf dem Host" ist verkürzt** — der Container braucht den **Kernel**-Teil
   nicht, aber sehr wohl **dieselbe Treiberversion im Userspace** (Installation im Container mit
   `--no-kernel-module`) **plus** cgroup-Device-Regeln für `/dev/nvidia*`. Host-Treiber allein
   reicht **nicht**; Host- und Container-Version müssen übereinstimmen.
   **(b) Kernel-Kopplung:** der Container teilt den Host-Kernel — ein Proxmox-Kernel-Upgrade, das
   dem Treiber davonläuft, legt ihn still, bis DKMS neu baut.
   **Die Alternative**, wenn harte Isolation mehr zählt als Bequemlichkeit: volle VM mit
   PCIe-Passthrough — kostet IOMMU-Einrichtung, dafür ist der Treiber vollständig in der VM
   gekapselt und vom Host-Kernel unabhängig. Beide Varianten pinnen die **GPU**-Kiste auf den
   3060-Host; das ist gewollt (Punkt 3), nicht der Unterschied zwischen ihnen.
5. **Hard Rule 6 bleibt unberührt:** Bindung nur auf die interne Bridge, kein Funnel, kein Port
   am Router. Der Dienst ist von außen nicht erreichbar und soll es nicht sein.

**Was die 12 GB praktisch ändern:** `qwen3-vl:8b` liegt bei Q4_K_M **6,1 GB** und passt damit
vollständig in den VRAM — der heutige Cold-Start von **46–180 s** (gemessen, CPU-only auf dem
i5-14600KF) fällt auf Sekunden. Erst das macht die in §4.6 geparkte Option (A) überhaupt
benutzbar: ein Batch-Aufruf über mehrere Screenshots war bisher nur deshalb die einzige
brauchbare Form, weil man den Cold-Start nicht mehrfach zahlen wollte. Nebenbei entsteht Luft
für ein größeres Modell (praktische Obergrenze ~12–14B bei Q4), aber das ist eine
Planungsfrage, keine Empfehlung.

**Zwei Ungereimtheiten in den bestehenden Skripten, beim Nachsehen gefunden** — beide kosten
sonst eine Stunde Fehlersuche, sobald der Endpoint nicht mehr `127.0.0.1` ist:

- `mcp_local_vision_server.py:223` loggt beim Start `DEFAULT_ENDPOINT`, während der echte Aufruf
  (`:195`) `LOCAL_VISION_ENDPOINT` auflöst. Mit gesetzter Variable **behauptet die Startzeile
  `127.0.0.1:11434`, obwohl die Anfragen zur GPU-Kiste gehen.** Kosmetisch, aber irreführend.
- Dasselbe Skript hat ein `--endpoint`-Flag (`:274`), das **nur `--check` benutzt**; `serve()`
  liest `args.endpoint` nie. Für den Serverbetrieb zählt ausschließlich die Umgebungsvariable.

**Offene Fragen für die Planungssession** (benannt, nicht entschieden): LXC oder VM — hängt am
IOMMU-Zustand des Hosts und daran, wie viel Kernel-/Treiber-Pflege tragbar ist · welches Modell (auf `qwen3-vl:8b` bleiben oder die VRAM-Luft nutzen) ·
ob die sharefyx-VM ein CPU-Fallback behält oder ihr Ollama abgebaut wird · feste interne Adresse
für die Kiste und wo `LOCAL_VISION_ENDPOINT` gesetzt wird (`~/.config/opencode/`, **nicht** im
Repo — kein Geheimnis, aber hostspezifisch).

---

## 5 `[VERIFY]`-Bilanz

**Vollständig in `phase8_6_ui_polish_plan2.md` §9.6** (V97 / V103–V144).
**Bilanz: 37 geschlossen · 2 offen · 2 nachträglich bilanziert.**

**Aufgelöst und erwähnenswert, weil sie eine Annahme umgeworfen haben:**

- **V125** — 9a **ist** 9b, gleiche Ursache. Bei 1200 px mit Banner sind die Maße auf `main`
  und `v3.0.1` byte-identisch. Die Plan-Annahme „Block C hat den Befund eingeführt" war falsch.
- **V110, V113** — beide als **negative Befunde** geschlossen: „Übersicht" und „Alle Items" sind
  dieselbe Aktion (`navigateAll()`), und `.tree__space` setzt gar kein `aria-current`. Beide
  Male lag der Plan falsch und der Code richtig. V110 hat später H-R.8 Lesart a verworfen.
- **V134** (geerbt als V103) — der `sudo`-Prompt ist sichtbar, am 2026-09-18 live bestätigt.
  Nach **zwei** Phasen Wartezeit geschlossen.
- **V140, V141** — im H-R-Mini-Plan eröffnet, materiell durch die H-R-Sichtung beantwortet
  (sie lieferte die drei H-R-3-Befunde), aber nie unter ihrem Namen abgehakt. In §9.6 nachgeholt.

**Offen, bewusst übergeben:**

| Marker | Frage | Warum offen, und wie man sie schließt |
|---|---|---|
| **V118** | Tag-Kante **und** explizite Kante zwischen denselben Knoten — zwei Linien gewollt? | Aus Screenshot 13 nicht beantwortbar: ohne Hover zeigt die Karte keine Knoten-Labels. `dedupeEdges()` fasst `implicitEdges` bewusst nicht an. **Weg:** live nachklicken, oder `p86_polish_smoke.py` um eine Label-Capture erweitern |
| **V136** | Kollidiert die `<span role="button">`-Umstellung der Chips (G7) mit `bindFolderDropTarget()` (`tree.js:108/119`)? | Plan 2 §8.3 stellt die Frage für Block G; **kein Block-Protokoll greift sie auf** — sie ist durchgerutscht, nicht beantwortet worden. Seit dem Nikinger-Feedback (§4.1a) gibt es einen realen Anlass, sie zu Ende zu messen |
| **V120** | Welche Events sollen einen dynamischen Tab-Titel auslösen? | Offen **bewusst** — „would be cool"-Note, außerhalb jedes Scopes seit sie eröffnet wurde |

---

## 6 P1-Contract

**Keine neunte Öffnung, und keine angekündigt.** Die achte (`storage/linkscan.py` +
`Store.links_all()`) bleibt die letzte. V102 wurde im Frontend dedupliziert (N2), der
Ordner-Zähler clientseitig aus `state.items` gerechnet (P8.6-O) — beides bewusst gewählte
Umwege, um den Index nicht anzufassen.

**Die eine Ausnahme dieser Phase lag nicht bei P1, sondern bei P4** und war **angekündigt**:
P8.6-AJ, `phase4_auth/authserver/crypto.py` + zwei Zeilen `store.py`, datiert auf den
2026-09-13, mit einer eigenen engeren Prüfprobe (§6.4) — gemessen erfüllt. Das ist das Muster,
das der vorige Handover verlangt hat: *„wird angekündigt, nicht beim Bauen entdeckt."*

---

## 7 Arbeitsweise und Werkzeug-Stand

- **Claude Code plant, opencode/M3 führt aus, kein Advisor in der Ausführung** (N4). In P8.6
  ist diese Teilung **zweimal bewusst durchbrochen** worden, beide Male vom Nikinger angeordnet
  und beide Male aus demselben Grund: **Pixel-Befunde sind nicht M3s Territorium** (Block H-R-3
  und der Gate-Lauf liefen in Claude Code). Wer P9 plant, sollte das nicht als Ausnahme,
  sondern als Muster lesen.
- **Die §0.5-Selbstprüf-Checkliste ist der Advisor-Ersatz** und hat getragen: Tabu-Diff,
  `pytest`, `ui_budget`, `node --check`, Doc-Update im selben Commit, kein Service-Touch.
- **Eskalationsregeln.** **P8.5-O** (Ursache liegt in einer früheren CSS-Regel ⇒ eskalieren,
  nicht symptomatisch patchen) hat gehalten. **P8.6-O2** (`.shell`-Grid) wurde in P8.6
  eingeführt, in Block C **eingehalten**, und in Plan 2 bewusst ausgelöst, vorgelegt,
  entschieden (P8.6-X). Eine Eskalationsregel, die einmal greift, ist keine Bürokratie.
- **Konvention §5 gilt** (`screenshots_latest/` + Dateiname und Checkkriterium im Chat);
  **P8.6-AK** hat sie auf **blockweise** verschärft, nicht erst beim Phasenwechsel.
- **Hard Rule 9 durchgehend gehalten** — inklusive des Deploys: `systemctl restart` lief über
  den Nikinger, der Agent hat an keiner Stelle selbst `systemctl` aufgerufen.

---

## 8 Was dieser Handover nicht enthält

- **Den kanonischen Closeout.** `phase8_6_ui_polish_plan2.md` §9 — Abnahmematrix Zeile für
  Zeile, VERIFY-Register vollständig, Restdefekte, §9.5 („was die Phase über ihre eigene Doku
  gelernt hat").
- **Den Wortlaut der neun Befunde.** `phase8_6_ui_polish/SESSIONS_ARCHIVE.md`, Block
  „2026-09-12 (Block-C-Sichtung Nikinger)", und Commit `bc2aa9f`.
- **Die Implementierungsdetails.** Code, Plan 1 §3–§6, Plan 2 §2–§7, und die drei Mini-Pläne
  (`*_block_g_r_plan.md`, `*_block_h_r_plan.md`, `*_block_h_r_3_escalation.md`).
- **Den Partial-Closeout-Stand vom 2026-09-13.** `git show 373a431:docs/concepts/PHASE8_6_CLOSEOUT_HANDOVER.md`
  — die beiden zitierten Abschnitte sind oben im Kopf gesichert.
- **Einen P9-Plan.** Dieses Dokument benennt Entscheidungen; es trifft keine.
