---
status: snapshot            # 📕-Snapshot gegen `main`@`2f752f9` — aktiver Plan, aber auf einen SHA fixiert (Muster: phase8_6_ui_polish_plan2.md)
purpose: "Ausführungsreifer P9-Plan — Härtungsphase: Domain über eigenen VPS, Tailscaled-Watchdog, Vision-Dienst auf der RTX 3060, INDEX-Rotation, zwei gemeldete Bugs, Karten-Reload, Schema-Fundament (neunte P1-Contract-Öffnung), Löschen nach _trash/. Infra-Steps als Coarbeit in opencode (P9-Q, §0.5.1). Locks P9-A–P9-T, Abnahme P9-1–P9-58, [VERIFY] V145–V172."
read-when: Arbeiten an Phase 9 — vor jedem Step einmal §0 und die Step-Sektion lesen; §1 ist die Lock-Tabelle, gegen die jede Abweichung geprüft wird
detail: L2
up: ../../ROADMAP.md
down:
  - ../../phase9_hardening/CLAUDE.md                # Phase-Head, Modulstatus + Session-Blöcke (§2.0)
  - ./PHASE8_6_CLOSEOUT_HANDOVER.md                 # Einstieg, §4 ist die Quelle der P9-Punkte
  - ./phase3_edge_plan.md                           # §0.3 P3-A (Funnel statt Cloudflare), §0.4 R4-Korrektur
  - ./phase6_shares_plan.md                         # §0.7(a)/§1.2 — Rechte-Grenze für Cross-Space
  - ./p8x_ui_polish_notes.md                        # §2 Karte, §10 Auswahl-Konvention — P10-Quelle
  - ./sichtpruefung_automation_conventions.md       # §2 Visuelles ist Nikinger-Sache, §5 screenshots_latest
updated: 2026-09-19 (Plan geschrieben — Claude-Code-Planungssession. Vier Nikinger-Entscheidungen aufgenommen: Härtung-only statt ROADMAP-UI-Umbau · Domain über eigenen VPS mit Funnel als Fallback · neunte P1-Contract-Öffnung für `doing`/`assignee` · Löschen nach `_trash/`, für Nutzer unsichtbar. Fünfte Vorgabe desselben Tages: die Infra-Steps A/B/C laufen als **Coarbeit in opencode** — M3 leitet an, der Nikinger führt aus (P9-Q, §0.5.1). Ein Handover-Weg widerlegt: Funnel kann keine eigene Domain, der CNAME-Pfad aus §4.2 existiert nicht.)
---

# Phase 9 — Härtung (`phase9_hardening/`)

> **P9 beseitigt die letzten Schwächen des laufenden Sharefyx und legt das Fundament, auf dem
> die geplanten Features in P10 stehen können.** Es ist **keine** UI-Umbau-Phase — die
> ROADMAP-P9-Zeile („Obsidian-Map-Umbau + verbundene AI-Sessions, letzter großer UI-Umbau")
> wird durch **P9-A** ersetzt und nach P10 verschoben.
>
> **Quelle der Wahrheit ist der Code, nicht dieses Dokument.** Jeder `Datei:Zeile`-Anker hier
> ist gegen `main`@`2f752f9` gemessen; bei Abweichung gewinnt der Code, und dieses Dokument
> bekommt eine datierte Korrekturnotiz.
>
> Deploy-Ziel **`v3.1.0`**. Einstieg: `PHASE8_6_CLOSEOUT_HANDOVER.md`.

---

## §0 Rahmen

### 0.1 Auftrag in drei Sätzen

1. **Betrieb härten:** eine Adresse, die einen Tailnet-Wechsel überlebt; ein Watchdog, der den
   am 2026-09-15 gemessenen Ausfallmodus überhaupt sieht; ein Vision-Dienst, der die
   Sichtprüfung vom 46–180-s-Cold-Start befreit.
2. **Doku-Haushalt automatisieren:** die `docs/INDEX.md`-Rotation bauen, statt zum vierten Mal
   von Hand zu straffen; vier gemessene Doku-Defekte reparieren und den Scan als Test festnageln.
3. **Fundament legen:** die zwei gemeldeten Bugs beheben, den Karten-Reload entschärfen, das
   Item-Schema um `doing`/`assignee` erweitern und einen Löschpfad bauen — damit P10 Features
   baut statt erst Grundlagen.

### 0.2 Scope

**DRIN (acht Steps):**

| Step | Inhalt | Ausführung |
|---|---|---|
| **0** | Verifikations-Durchlauf, vier Doku-Defekte, INDEX-Rotation gebaut, `doc_health`-Test | Claude Code |
| **A** | Echte Domain: eigener VPS als TLS-Terminator, Funnel als dokumentierter Fallback | **Coarbeit** opencode/M3 + Nikinger (§0.5.1) |
| **B** | `tailscaled-watchdog.service` (zyklisch prüfend) | **Coarbeit** opencode/M3 + Nikinger |
| **C** | Vision-Dienst auf der RTX 3060 (eigener LXC) + zwei Skript-Ungereimtheiten | **Coarbeit** opencode/M3 + Nikinger |
| **D** | Zwei gemeldete Bugs: ESC/Fullscreen, Drop-Ziel Space-Wurzel · V136 schließen | opencode/M3 |
| **E** | Karte: Reload-Overload (§2.1) · V118 schließen | opencode/M3 |
| **F** | Schema-Fundament: `doing` + `assignee` — **neunte P1-Contract-Öffnung, angekündigt** | opencode/M3 |
| **G** | Löschen (F2) nach `_trash/`, für Nutzer unsichtbar | opencode/M3 |
| **H** | Abhängigkeits-Hygiene: `fastmcp` 3.4.4 → 3.4.7 | opencode/M3 |
| **Gate** | Wegwerf-Ritt, `p9_hardening_smoke.py`, Nikinger-Sichtprüfung, Deploy `v3.1.0` | Claude Code |
| **Z** | Closeout — Abnahmematrix, VERIFY-Bilanz, Grafik, Rotation | Claude Code |

**DRAUSSEN (P10 und später):** Karten-**Stil**umbau („Landkarte statt Netz", `p8x_ui_polish_notes.md`
§2.2) · Karte einklappen (§2.5) · verbundene AI-Sessions (§10.8) · Hochkant-/Handy-UI (§10.9) ·
Logo + Design-Vorlage · To-do-Checkboxen im Text · die **Darstellung** von „aktuelle Aufgabe" auf
der Übersicht (das **Feld** entsteht in Step F, seine Hervorhebung ist P10) · Verschieben in
fremde Spaces (Rechte-Thema, §0.6) · das geerbte Ledger (Q1 Body-Volltextsuche, P6-M, FastMCP 4
/ V79, Realtime, Light-Mode, Bulk-Append, Ordner umbenennen).

### 0.3 Tabu-Liste (Bereichs-Diff, nicht Working-Tree-Diff)

Diese Pfade werden in P9 **nicht** angefasst — mit **genau einer** angekündigten, datierten
Ausnahme (Step F, siehe P9-G):

```
phase2_mcp/mcpserver/permissions.py
phase2_mcp/mcpserver/server.py
phase4_auth/authserver/
phase6_shares/            (Code; Doku-Zeilen erlaubt)
phase7_spaces_admin/      (Code; Doku-Zeilen erlaubt)
```

**Probe, am Ende jedes Steps:**

```bash
git diff --stat <phase_start_sha>^..HEAD -- \
  phase2_mcp/mcpserver/permissions.py phase2_mcp/mcpserver/server.py \
  phase4_auth/authserver phase6_shares phase7_spaces_admin
```

**Als Bereichs-Diff laufen lassen, nie als Working-Tree-Diff** — der meldet bei sauberem Baum
vakuös leer und beweist über die Phase nichts (Lehre aus P8.6 Step Z).

**Step-F-Ausnahme (P9-G):** `phase1_storage/storage/{models.py,store.py,index.py}` und
`phase5_ui/webui/serializers.py`. Der Umfang ist in §8.2 zeilengenau vorgegeben; die enge Probe
in §8.7 ist Abbruchkriterium.

### 0.4 Selbstprüf-Checkliste (der Advisor-Ersatz, aus P8.6 §0.5 übernommen)

Nach **jedem** Step, vor dem Commit, in dieser Reihenfolge:

1. `.venv/bin/python -m pytest -q` — Baseline **995 passed** (gemessen 2026-09-18). Jede
   Abweichung nach unten ist Abbruchgrund, jede nach oben wird im Commit begründet.
2. `phase5_ui/scripts/ui_budget.py` — **5/5 im Korridor** (Baseline 144,7 KB von 250 KB). Nur
   nötig, wenn `phase5_ui/webui/static/**` berührt wurde.
3. `node --check` auf jede berührte `.js`-Datei.
4. Tabu-Bereichs-Diff aus §0.3 — leer (Step F: die enge Probe aus §8.7).
5. Doc-Update **im selben Commit**: Phase-Head-Modulstatus, `## Session stopped`-Block,
   `docs/INDEX.md`-Zeile bei neuer `.md`. Hard Rule 8, keine Ausnahme.
6. **Kein Service-Touch.** `sharefyx-mcp` wird gelesen, nie angefasst. Kein `pkill -f`, kein
   `systemctl` durch einen Agenten (Hard Rule 9). Wegwerf-Instanzen ausschließlich über
   PID-Datei oder eindeutigen Port stoppen.

### 0.5 Ausführungsteilung (P9-Q)

Handover §7 liest die zweimalige Durchbrechung der Teilung in P8.6 als **Muster, nicht
Ausnahme**. P9 schreibt sie deshalb pro Step fest, statt sie im Konfliktfall neu zu verhandeln:

- **Claude Code** führt aus: alles mit Pixel-Befund, Step 0, Gate, Step Z.
- **opencode/M3** führt aus: die Code-Blöcke D, E, F, G, H — **und leitet die Infra-Steps A, B
  und C als Coarbeit an** (§0.5.1).
- **Der Nikinger** führt aus: jeden `sudo systemctl`-Aufruf, jede Domain-/VPS-Beschaffung, jede
  Proxmox-Konsolen-Aktion, jede Sichtprüfung.

#### 0.5.1 Coarbeit — die Form der Infra-Steps A, B, C (Nikinger-Vorgabe 2026-09-19)

**Die Infra-Steps laufen nicht als Auftragsliste, sondern als geführte Sitzung in opencode:**
M3 leitet an, der Nikinger tippt. Dasselbe Muster, das die Proxmox-Migration und das
Ollama-Setup am 2026-09-10 getragen hat — es ist bewährt, nicht neu.

**Was das für den Ablauf bedeutet, und warum es nicht bloß Stil ist:**

- **Ein Schritt pro Runde.** M3 gibt **einen** Befehl oder eine Konsolen-Aktion aus, wartet auf
  die echte Ausgabe, liest sie, entscheidet den nächsten Schritt. Keine Blocklisten von zehn
  Befehlen — bei DNS, Zertifikaten und Treibern hängt Schritt *n+1* regelmäßig an der Ausgabe
  von *n*, und eine vorweg geschriebene Liste rät dort, wo sie messen müsste.
- **Die Ausgabe wird gelesen, nicht quittiert.** Der `umask 0177`-Deploy-Blocker aus P8.6 ist
  genau daran vier Stunden lang vorbeigelaufen: `ls -la` sah gesund aus, weil niemand das
  **neu angelegte Kind-Verzeichnis** geprüft hat. Wer eine Ausgabe nur als „ok" verbucht,
  findet diese Klasse Fehler nie.
- **Hard Rule 9 bleibt unberührt und wird dadurch sogar leichter einzuhalten:** M3 formuliert
  den `sudo`-Befehl, **der Nikinger führt ihn aus**. Der Agent ruft an keiner Stelle selbst
  `systemctl` auf — das ist in dieser Form kein Verzicht, sondern die Arbeitsteilung selbst.
- **Protokoll fällt nebenbei an.** Jede echte Ausgabe steht im Sitzungsverlauf und wandert in
  den Session-Block. Genau daran ist P8.6 einmal gescheitert: ein „`health_gate` 8/8 grün",
  das nie so gelaufen war, hat vier Wochen lang behauptet, eine Phase sei live.

**Die Grenze der Coarbeit:** Sichtprüfungen bleiben Nikinger-Sache (Konvention §2), und
Pixel-Befunde bleiben außerhalb von M3s Territorium (Handover §7). Coarbeit gilt für
Infrastruktur — Adressen, Dienste, Treiber —, nicht für Urteile über Bilder.

### 0.6 Eine Grenze, die P9 ausdrücklich nicht verschiebt

„Teilen / Verschieben in fremde Root-Spaces" (Handover §4.1b) ist ein **Rechte-Thema**, kein
UI-Thema. Gemessen 2026-09-19: `SharePolicy` **ist gebaut** (`phase1_storage/storage/acl.py`,
`phase5_ui/webui/shares.py`, `share_write`-Fixtures in `phase7_spaces_admin/scripts/`) — die
Maschinerie fehlt also **nicht**, das UI ist nur absichtlich konservativer als der Server
(`list.js:412` `movable`, `tree.js:205` `if (space.own)`). Das Thema ist damit **billiger als
der Handover vermutet**, aber es ist Hard-Rule-4-Arbeit und braucht eine eigene Entscheidung
über die Rechte-Anzeige. **P9 baut es nicht.** Es geht als benannter, nicht stillschweigend
abgeräumter Posten nach P10; Einstieg `phase6_shares_plan.md` §0.7(a)/§1.2.

---

## §1 Gelockte Entscheidungen

| Lock | Entscheidung | Begründung, in einem Satz |
|---|---|---|
| **P9-A** | **P9 ist eine Härtungsphase.** Der ROADMAP-P9-Inhalt (Karten-Stilumbau + AI-Sessions) wandert nach P10 | Nikinger-Entscheidung 2026-09-19: „die letzten Schwächen beseitigen, um eine stabile Grundlage für neue Features zu schaffen" — die ROADMAP-Zeile wird im selben Commit umgeschrieben, nicht still überholt |
| **P9-B** | Deploy-Ziel **`v3.1.0`** | Dreifach vorgemerkt (ROADMAP, Handover §4.5, `project_ui_version_scheme`); ein Minor-Bump ist Nikinger-Sache und war es schon |
| **P9-C** | **Domain über einen eigenen VPS als TLS-Terminator**, der per Tailscale im Tailnet hängt; der Funnel-Hostname bleibt betriebsbereit und dokumentiert als Fallback | Nikinger-Entscheidung 2026-09-19. Der VPS terminiert TLS für die eigene Domain und proxyt intern über das Tailnet — kein Port am Heim-Router, Hard Rule 6 unberührt. Die Adresse überlebt jeden künftigen Tailnet-Wechsel; das war der Anlass |
| **P9-D** | **P3-A wird nicht umgekehrt.** Cloudflare Tunnel kommt nicht zurück | `phase3_edge_plan.md` §0.4 hat R4 datiert korrigiert: bei Funnel terminiert die Node selbst TLS, die Relays reichen verschlüsselt durch. Cloudflare terminiert TLS und sieht Klartext — ein Wechsel dorthin wäre ein gemessener Rückschritt, kein neutraler Umbau |
| **P9-E** | **Der `<node>.<tailnet>.ts.net`-Weg ist für eine eigene Domain tot** — nicht „schwierig", sondern nicht vorgesehen | Tailscale-Doku: *„Funnel can only use DNS names in your tailnet's domain"*; ein CNAME darauf erzeugt einen TLS-Namens-Mismatch (tailscale/tailscale#16478). Handover §4.2 Option (a) ist damit erledigt, nicht offen |
| **P9-F** | **Watchdog = Ansatz 2** (eigene, zyklisch prüfende `tailscaled-watchdog.service`) | Als einziger der drei Ansätze sieht er den Zustand vom 2026-09-15 überhaupt: `tailscaled` lief durch, nur die Control-Plane klemmte — ein `OnFailure=`-Hook feuert dort nie |
| **P9-G** | **Neunte P1-Contract-Öffnung, angekündigt und datiert auf den 2026-09-19.** Umfang: `models.py` (2 Stellen), `store.py` (3 Stellen), `index.py` (3 Stellen). Nicht mehr | Das Muster, das der P8.6-Handover verlangt: *„wird angekündigt, nicht beim Bauen entdeckt."* Die enge Probe in §8.7 ist Abbruchkriterium, nicht Zielgröße |
| **P9-H** | **`doing` wird ein Statuswert, `assignee` ein erstklassiges Feld mit Index-Spalte** — nicht ein Tag, nicht ein `extra`-Schlüssel | Über `Item.extra` (`models.py:38`) ginge beides heute ohne Kernänderung, aber ohne Index: kein serverseitiges Filtern, kein erzwungenes Vokabular — ein Tippfehler im Tag erzeugt still einen zweiten Zustand. `_status_hint()` (`tools.py:133`) generiert das Vokabular bereits aus `STATUS_VALUES`, der neue Wert erreicht MCP also ohne Zusatzarbeit |
| **P9-I** | **Löschen = Verschieben nach `_trash/`**, nie `unlink` | Der Präzedenzfall steht im Code: `store.py:849 delete_asset()` verschiebt Assets nach `_trash/` statt sie zu entfernen (Lock N5), und `store.py:815` überspringt `_trash` beim Scannen. Ein zweites Löschkonzept danebenzustellen wäre teurer als das bestehende zu benutzen |
| **P9-J** | **`_trash/` bleibt für Nutzer unsichtbar.** Kein Papierkorb-Eintrag, keine Wiederherstellung im UI, kein API-Endpoint, der den Inhalt listet | Nikinger-Entscheidung 2026-09-19 („erstmal unsichtbar"). Das Item verschwindet aus jeder Nutzersicht; Wiederherstellung ist Dateisystem- und Git-Arbeit des Nikingers. Der Vorteil ist genau der: die sichere Semantik kostet keine zweite Oberfläche |
| **P9-K** | **Löschen ist human-only.** Kein MCP-Werkzeug, kein Bulk, kein Tastenkürzel. Gate: zweifache Rückfrage **und** Eintippen des Item-Titels | Nikinger-Vorgabe. Ein Löschwerkzeug im MCP-Pfad hieße: ein prompt-injiziertes fremdes Item könnte eigene Notizen löschen — Hard Rule 4 nennt fremde Bodies ausdrücklich potenzielle Befehle |
| **P9-L** | **Die `docs/INDEX.md`-Rotation wird gebaut**, nicht ein viertes Mal von Hand gestrafft | Drei Verstöße in einer Phase; §4.4 des Handovers: „die Handarbeit hat jetzt dreimal nicht getragen". Beim Schreiben dieses Plans waren **156 B** Luft — die Rotation ist Voraussetzung dieses Dokuments, nicht bloß ein Arbeitspunkt |
| **P9-M** | Der Karten-Reload wird **clientseitig** entschärft. Keine Änderung an `/api/v1/graph`, keine an `storage/linkscan.py` | Dieselbe Begründung wie P8.6-N für `dedupeEdges()`: eine Contract-Öffnung ist das teuerste Mittel für ein Ladeverhalten. Die achte Öffnung bleibt die letzte, die neunte gehört Step F |
| **P9-N** | **Vision-Dienst: eigener LXC-Container auf dem 3060-Host**, erreichbar als interner HTTP-Dienst auf der Proxmox-Bridge. Nie in der sharefyx-VM, kein PCIe-Passthrough in die Produktions-VM | Handover §4.8, „Form nach Empfehlung" delegiert. Das Bauprinzip „der Server ist dumm" bleibt physisch nachprüfbar statt ein Versprechen; und die sharefyx-VM bleibt zwischen den beiden Proxmox-Nodes migrierbar, weil genau **eine** Kiste auf den 3060-Host gepinnt ist — die, die stillstehen darf |
| **P9-O** | **Eskalationsregel P8.5-O gilt unverändert:** liegt die Ursache eines Symptoms in einer früheren Regel, wird eskaliert statt symptomatisch gepatcht | Hat über zwei Phasen getragen |
| **P9-P** | **Die fünf Feature-Wünsche bleiben draußen — außer Löschen.** Logo/Design-Vorlage, To-do-Checkboxen, „aktuelle Aufgabe" **anzeigen**, Assignen **anzeigen** sind P10 | P9-A. Step F baut das **Feld**, nicht seine Hervorhebung: der Zustand ist danach über Editor-YAML, REST und MCP setz- und lesbar, seine prominente Darstellung auf der Übersicht ist P10-Arbeit |
| **P9-Q** | **Die Infra-Steps A, B und C laufen als Coarbeit in opencode:** M3 leitet Schritt für Schritt an, der Nikinger führt aus und liefert jede echte Ausgabe zurück | Nikinger-Vorgabe 2026-09-19, und dasselbe Muster, das die Proxmox-Migration und das Ollama-Setup getragen hat. Bei DNS, Zertifikaten und Treibern hängt jeder Schritt an der Ausgabe des vorigen — eine vorweg geschriebene Befehlsliste rät dort, wo sie messen müsste. Form und Grenzen: §0.5.1 |
| **P9-R** | **`fastmcp` bleibt auf `3.4.x`.** FastMCP 4 / MCP-Revision `2026-07-28` ist und bleibt eine eigene Mini-Phase (V79) | Das Ledger hat das seit P5-C so festgelegt. FastMCP 4.0.0 (2026-08-31) bringt die neue Protokollrevision mit Per-Connection-Aushandlung, Alt-Clients laufen weiter — es gibt keinen Zwang, und eine Protokollmigration mitten in einer Härtungsphase ist genau die Vermischung, die P8.6 zwei Pläne gekostet hat |
| **P9-S** | **Hard Rule 9 unverändert.** Kein `pkill -f`, kein `systemctl` durch einen Agenten | Hat über die ganze P8.6 getragen, inklusive des Deploys |
| **P9-T** | **Ein Dokument pro Phase.** Dieser Plan ist das einzige P9-Konzeptdokument; Mini-Pläne für Revisionsrunden sind erlaubt, aber sie tragen `phase9_hardening_block_<X>_plan.md` und **im selben Commit** eine INDEX-Zeile | P8.6 hat drei Mini-Pläne produziert, von denen zwei ohne L1-Card blieben — genau der Defekt, den Step 0.3 repariert |

---

## §2 Step 0 — Verifikations-Durchlauf und Doku-Fundament

**Ausführung: Claude Code. Ein Commit.**

> **Der Scan ist am 2026-09-19 bereits gelaufen.** Was hier steht, sind **Befunde**, keine
> Prüfaufträge — Step 0 repariert sie und nagelt den Scan als Test fest. Nicht neu herleiten.

### 2.0 Phasenverzeichnis anlegen

```
phase9_hardening/
├── CLAUDE.md            # Phase-Head, L1-Card + Modul-Status-Tabelle + genau EIN Session-Block
├── SESSIONS_ARCHIVE.md  # L1-Card, leer bis zur ersten Rotation
├── scripts/
└── tests/
```

Beide `.md` bekommen im selben Commit eine `docs/INDEX.md`-Zeile (Hard Rule 8).

**Und eine Zeile in diesem Plan:** die `down:`-Liste der Header-Card oben bekommt
`../../phase9_hardening/CLAUDE.md`. Sie steht dort heute **nicht** — ein Verweis auf eine
Datei, die es noch nicht gibt, wäre genau der Defekt, den §2.3 `updown_links` verbietet, und
zwar im Dokument, das ihn vorschreibt.

### 2.1 Die INDEX-Rotation bauen (P9-L) — **zuerst, alles andere hängt daran**

Neu: `docs/INDEX_UPDATES_ARCHIVE.md` (L3-Archiv, L1-Card, newest-first) und
`scripts/rotate_index_updates.sh`.

**Vorbild ist `scripts/rotate_session_block.sh` (167 Zeilen) — dieselbe Mechanik, nicht eine
neue:** Blöcke per `sed -n 'A,Bp'` ausschneiden, Reassemblierung mit `cmp` gegen das Original
prüfen, jeden Block nach dem Einfügen byte-identisch gegenlesen, erst danach schreiben. Bei
jeder Abweichung abbrechen, ohne eine Zieldatei angefasst zu haben. Exit-Codes identisch:
`0` = rotiert · `1` = Abbruch, nichts geändert · `2` = nichts zu tun.

**Der Unterschied zum Vorbild, und warum er nicht trivial ist:** `rotate_session_block.sh`
schneidet an Zeilenanfängen (`^## Session stopped`). Die `updated:`-Kette der `INDEX.md` ist
**eine einzige physische Zeile** mit ` | `-getrennten Einträgen. Das Skript muss deshalb
innerhalb einer Zeile trennen, und die Trennung darf nicht an einem ` | ` innerhalb einer
Markdown-Tabellenzelle greifen. **Regel:** nur die `updated:`-Zeile der Frontmatter wird
angefasst (erkennbar an `^updated: ` und Lage zwischen dem ersten und zweiten `^---`), der
Body nie.

**Erhalten bleibt genau ein Eintrag** (der jüngste) plus ein Zeiger:
`… | ältere Einträge: docs/INDEX_UPDATES_ARCHIVE.md`.

**Vier Gegenproben, alle vor dem Schreiben** (analog Vorbild): (a) Zeilenzahl Quelle = Zeilenzahl
Rest + Zeilenzahl rotierte Einträge · (b) `cmp` der Reassemblierung gegen das Original ·
(c) jeder rotierte Eintrag byte-identisch im Archiv wiedergefunden · (d) der Frontmatter-Closer
`---` steht danach auf einer eigenen Zeile. **(d) ist kein Zierrat** — genau dieser Defekt trat
am 2026-09-13 real auf: der Closer klebte am Zeilenende, die Frontmatter war formal kaputt.

`[VERIFY] V145` — `docs/INDEX.md` nach der Rotation unter **38.912 B** (= 38 KB), mit den neuen
P9-Zeilen darin. Gemessener Ausgangsstand 2026-09-19: **38.756 B, 156 B Luft.**

### 2.2 Vier gemessene Doku-Defekte reparieren

| # | Befund (gemessen 2026-09-19) | Reparatur |
|---|---|---|
| **0-a** | `docs/concepts/phase8_6_ui_polish_block_h_r_3_escalation.md` — **5 kaputte `up:`/`down:`-Links**. Die Karte nutzt `../phase8_6_ui_polish/…` und `../docs/concepts/…`; die Datei liegt selbst in `docs/concepts/`, es braucht also `../../` bzw. den nackten Dateinamen | Alle fünf Pfade um eine Ebene korrigieren; anschließend Scan aus §2.3 grün |
| **0-b** | `phase8_6_ui_polish_block_g_r_plan.md` und `phase8_6_ui_polish_block_h_r_plan.md` — **keine L1-Header-Card**. Beide sind lebende Dokumente und damit kartenpflichtig | Je eine ≤15-Zeilen-Card mit `status/purpose/read-when/detail/up/down/updated`. `status: snapshot`, weil beide abgeschlossene Mini-Pläne sind |
| **0-c** | `docs/INDEX.md`s `ROADMAP.md`-Zeile ist **stale**: „📗 ~26KB · Phasen 1–8". Real **42.163 B** und die Datei enthält P9 | Größe und Inhaltsangabe nachziehen. **`ROADMAP.md` liegt damit über dem 40-KB-Softcap** — das nach dem Muster von P8-P **benennen**, nicht verstecken; die Straffung ist Step-Z-Arbeit, keine Step-0-Arbeit |
| **0-d** | **Zwei `screenshots_latest/`-Verzeichnisse**: `./screenshots_latest` und `./docs/screenshots_latest` | Eines ist das von Konvention §5 gemeinte. Feststellen, welches `sichtpruefung_automation_conventions.md` §5 und `P8.6-AK` benennen, das andere entfernen oder als Symlink darauf umbiegen. **Nicht raten** — erst die Konvention lesen, dann handeln |

### 2.3 Den Scan als Test festnageln

Neu: `scripts/doc_health.py` (stdout **nur** maschinenlesbares JSON, Logging nach stderr —
Hard Rule 7) und `phase9_hardening/tests/test_doc_health.py`.

Vier Prüfungen, exakt die, die den Scan am 2026-09-19 ausgemacht haben:

| Prüfung | Kriterium |
|---|---|
| `index_lines` | Jede `.md` außerhalb der vier dokumentierten Ausnahmen hat eine Zeile in `docs/INDEX.md` |
| `header_cards` | Jede lebende `.md` beginnt mit `---` und trägt `status`/`purpose`/`read-when`/`detail` |
| `updown_links` | Jeder `up:`/`down:`-Pfad in einer Frontmatter löst gegen das Dateisystem auf |
| `oversize` | Jede `.md` > 40 KB ist in `docs/INDEX.md` als 📕 oder 📦 markiert, nie als 📗/🔄 |

**Die Ausnahmeliste wird nicht erfunden** — `docs/INDEX.md` führt sie bereits („Harness-Dateien ·
Test-Fixtures · maschinell geparste Dateien · …"). `doc_health.py` liest sie aus einer
Konstante, die diesen vier Fällen namentlich entspricht; `.claude/RESUME.md`,
`phase6_shares/tests/golden/*.md`, `docs/UPDATE_LOG.md`, `phase5_ui/THIRD_PARTY_LICENSES.md`
und `phase5_ui/vendor/lucide/README.md` sind die heutigen Träger dieser Ausnahmen
(`[VERIFY] V146` — die Liste gegen `docs/INDEX.md` gegenlesen, nicht aus diesem Plan abtippen).

### 2.4 Baseline messen und im Commit festhalten

```bash
.venv/bin/python -m pytest -q                      # erwartet 995 passed
phase5_ui/scripts/ui_budget.py                     # erwartet 5/5, 144,7 KB von 250 KB
git rev-parse --short HEAD                         # Phasenstart-SHA für den Bereichs-Diff
```

`[VERIFY] V147` — `pytest` ist **995**, nicht 994 oder 996. Die Zahl ist die Referenz für jeden
weiteren Step; wer sie nicht misst, kann später keine Abweichung erkennen.

### 2.5 Abnahme Step 0

`P9-1` Phasenverzeichnis existiert, beide `.md` mit Card und INDEX-Zeile ·
`P9-2` `rotate_index_updates.sh` läuft, alle vier Gegenproben grün ·
`P9-3` `docs/INDEX.md` < 38.912 B **nach** Aufnahme aller neuen P9-Zeilen ·
`P9-4` Die fünf Links in `…_h_r_3_escalation.md` lösen auf ·
`P9-5` Beide Mini-Pläne tragen eine L1-Card ·
`P9-6` Die `ROADMAP.md`-INDEX-Zeile nennt die reale Größe und P9 ·
`P9-7` Genau ein `screenshots_latest/`-Pfad, begründet gewählt ·
`P9-8` `doc_health.py` läuft, `test_doc_health.py` grün, alle vier Prüfungen 0 Befunde ·
`P9-9` `pytest` ≥ 995 (Step 0 addiert die neuen `doc_health`-Tests).

---

## §3 Step A — Echte Domain über einen eigenen VPS

**Ausführung: Coarbeit in opencode (§0.5.1) — M3 leitet Schritt für Schritt an, der Nikinger
tippt und liefert jede echte Ausgabe zurück. Ein Commit für den Repo-Anteil.**

> **Nikinger-Vorlauf, ohne den Step A nicht startet:** eine **beschaffte Domain** und ein
> **erreichbarer VPS**. Beides ist ausdrücklich kein Agenten-Auftrag. Solange der Vorlauf
> aussteht, läuft **Step B und C weiter** — A blockiert die Phase nicht.

### 3.1 Warum dieser Weg, und was er nicht ist

Der Handover §4.2 nennt zwei Wege. **Einer davon existiert nicht:** Tailscale Funnel kann
ausschließlich Namen in der eigenen Tailnet-Domain bedienen; ein CNAME einer eigenen Domain auf
den Funnel-Hostnamen führt zum TLS-Namens-Mismatch, weil Funnel per SNI an die Node durchreicht
und diese ein Zertifikat für `*.ts.net` präsentiert. Das ist keine Konfigurationshürde, sondern
die Bauform (**P9-E**, `[VERIFY] V148` — gegen die aktuelle Tailscale-Doku gegenlesen, nicht aus
diesem Plan übernehmen).

Der billige Ersatz wäre Cloudflare Tunnel. **Er ist per P9-D ausgeschlossen**, und zwar mit
Beleg statt Geschmack: `phase3_edge_plan.md` §0.4 hat Rahmenentscheidung R4 datiert korrigiert,
weil bei Funnel **die Node selbst** TLS terminiert und die Relays den Strom verschlüsselt
durchreichen — bei Cloudflare terminiert Cloudflare und sieht Klartext. Der Wechsel wäre ein
gemessener Rückschritt bei genau der Eigenschaft, die P3 verbessert hat.

**Was gebaut wird:** ein kleiner VPS hängt per Tailscale im Tailnet, terminiert TLS für die
eigene Domain mit Let's Encrypt und proxyt die Anfragen **innerhalb des Tailnets** an die
Heim-VM weiter. Die Heim-VM öffnet keinen Port; sie baut wie bisher nur eine ausgehende
Tailscale-Verbindung auf. **Hard Rule 6 bleibt unberührt** — die Regel verbietet einen offenen
Port am Router, nicht einen Terminator, den man selbst betreibt.

**Was der Weg kostet, damit es niemanden überrascht:** eine Kiste mehr zu patchen, laufende
Kosten, und ein Terminator, der Klartext im Speicher sieht — der Unterschied zu Cloudflare ist
nicht „niemand sieht es", sondern „der, der es sieht, bist Du". Das ist eine echte, aber
kleinere Vertrauensfläche, und sie ist in der Root-`CLAUDE.md` R3 seit P2 als Option benannt
(„Migration auf VPS + WireGuard als P3-Option") — kein erfundener Weg.

### 3.2 Schritte

| # | Aktion | Wer |
|---|---|---|
| A1 | Domain beschaffen, DNS-Zone erreichbar | Nikinger |
| A2 | VPS beschaffen (klein reicht: 1 vCPU / 2 GB; der Reverse-Proxy rechnet nichts) | Nikinger |
| A3 | `tailscale up` auf dem VPS, Node in dasselbe Tailnet, **als Tagged Node** mit eigener ACL-Regel — nicht als Nutzergerät | Nikinger, ACL-Entwurf von M3 |
| A4 | Caddy auf dem VPS: `<domain> { reverse_proxy <heimvm-tailnet-name>:<port> }`, TLS automatisch über Let's Encrypt | M3 (Config), Nikinger (`sudo`) |
| A5 | DNS: A/AAAA der Domain auf die VPS-IP. **Kein CNAME auf `ts.net`** (P9-E) | Nikinger |
| A6 | Firewall am VPS: 80/443 offen, **alles andere zu**; SSH nur über Tailscale, nicht über die öffentliche IP | M3 (Entwurf), Nikinger |
| A7 | `SPACE_PUBLIC_BASE_URL` und die OAuth-`issuer`/`redirect_uri`-Werte auf die neue Domain ziehen | M3 |
| A8 | **Connector in beiden Claude-Konten** auf die neue Adresse umstellen | Nikinger |
| A9 | Funnel **bleibt aktiv** und wird im Runbook als Fallback dokumentiert, inklusive der Reihenfolge für den Rückfall | M3 |

### 3.3 Die Falle, die dieser Step vermeiden muss

**Der OAuth-`issuer` ist Teil der Client-Registrierung.** Die in beiden Konten registrierten
Clients kennen die alte Adresse; eine Adressänderung ohne Nachzug der
`authorization_server`-Metadaten führt zu einer Redirect-URI-Abweisung, die wie ein Auth-Bug
aussieht und keiner ist. **Reihenfolge deshalb: A7 vor A8**, und A8 erst, wenn `/.well-known/
oauth-authorization-server` unter der neuen Domain die neue `issuer` liefert.
`[VERIFY] V149` — welche Felder in `phase4_auth/authserver/metadata.py` aus der Basis-URL
abgeleitet werden und welche irgendwo fest stehen. **Lesen, nicht annehmen** — `phase4_auth/`
steht auf der Tabu-Liste, Step A darf dort nur lesen und konfigurieren.

`[VERIFY] V150` — hält der Anthropic-Connector nach dem Wechsel? Gegenprobe ist ein echter
`list_spaces`-Aufruf aus beiden Konten, nicht ein `curl`.

`[VERIFY] V151` — misst der Weg über den VPS eine relevante Latenz gegenüber dem Funnel?
Referenz: `/api/v1/overview` **372,9 ms** über Funnel (zweimal gemessen, P8.6). Wenn der VPS das
deutlich verschlechtert, ist das ein Befund für den Nikinger, kein stiller Hinnahmefall.

### 3.4 Abnahme Step A

`P9-10` `https://<domain>/healthz` antwortet 200 mit gültigem Let's-Encrypt-Zertifikat ·
`P9-11` `nmap` gegen die **Heim**-IP zeigt unverändert keinen offenen Port (Hard Rule 6) ·
`P9-12` `/.well-known/oauth-authorization-server` liefert die neue `issuer` ·
`P9-13` `list_spaces` aus **beiden** Claude-Konten über die neue Adresse liefert die echten
Spaces (V150) · `P9-14` Der Funnel-Hostname antwortet weiterhin; das Runbook beschreibt den
Rückfall in nummerierten Schritten · `P9-15` `/api/v1/overview`-Zeit gemessen und gegen 372,9 ms
verglichen (V151).

---

## §4 Step B — `tailscaled-watchdog.service`

**Ausführung: Coarbeit in opencode (§0.5.1). Unit, Skript und Tests schreibt M3; Installation
und `systemctl enable` führt der Nikinger aus. Ein Commit.**

### 4.1 Was genau versagt hat

Vorfall 2026-09-15: nach ~4 h VM-Suspend kam `tailscaled` nicht mehr auf die Control-Plane.
`sharefyx-mcp` antwortete lokal weiter mit 200 — von innen sah alles gesund aus, von außen war
das Node offline. `Restart=on-failure` deckt das nicht: der Dienst ist nie gefallen.

**Daraus folgt die Form:** die Prüfung muss von **außerhalb der Prozessgesundheit** kommen und
**zyklisch** laufen. Ein `OnFailure=`-Hook (Ansatz 1) feuert in diesem Zustand nie. Ansatz 3
(Tailscale-eigenes Feature) bleibt offen — `[VERIFY] V152`: kurz recherchieren, ob es das
mittlerweile ohne kommerzielles Add-on gibt; falls ja, ist der Eigenbau überflüssig und das
ist ein Befund, kein Gesichtsverlust.

### 4.2 Bauform

Neu: `phase3_edge/systemd/tailscaled-watchdog.service` + `.timer`, und
`phase3_edge/scripts/tailscaled_watchdog.sh`.

**Timer statt `while`-Schleife im Dienst.** Ein `Type=oneshot` + `OnUnitActiveSec=` ist
beobachtbar (`systemctl list-timers`), überlebt einen Fehler im Skript und braucht keinen
eigenen Prozess im Leerlauf.

**Prüflogik, drei Stufen, in dieser Reihenfolge — die Reihenfolge ist der Punkt:**

1. `tailscale status --json` → `Self.Online == true`. Billig, lokal, kein Netz.
2. Nur wenn (1) unklar ist: `tailscale netcheck` mit Timeout.
3. Nur wenn (1) und (2) fehlschlagen: `systemctl restart tailscaled`.

**Warum gestuft und nicht direkt `netcheck`:** ein Watchdog, der bei jedem Tick echtes Netz
erzeugt, ist selbst eine Last und produziert Fehlalarme bei jedem transienten Paketverlust.
Die billige lokale Prüfung filtert den Normalfall heraus, bevor irgendetwas gemessen wird.

**Rate-Limit, hart:** höchstens **ein** Restart pro 15 Minuten, Zustand in einer Datei unter
`/run/`. Ohne das baut ein Watchdog bei einem echten Ausfall eine Restart-Schleife, die den
Ausfall verlängert statt ihn zu beheben.

**Härtung (Handover §4.3, wörtlich übernommen):** `User=`, `NoNewPrivileges=true`,
`ProtectSystem=strict`. Der `systemctl restart tailscaled`-Aufruf braucht dafür eine eng
geschnittene Polkit-Regel oder ein `sudoers`-Fragment mit genau diesem einen Befehl —
`[VERIFY] V153`, welcher der beiden Wege auf dieser Ubuntu-24.04-VM der tragfähigere ist.

**Hard Rule 9:** Auslöser ist systemd, nie ein Agent. Installation und `systemctl enable` führt
**der Nikinger** aus.

### 4.3 Tests

`phase9_hardening/tests/test_tailscaled_watchdog.py` — kein Netz, kein echter Dienst:

| Test | Prüft |
|---|---|
| `test_online_node_triggers_no_restart` | Gemockte `status --json` mit `Self.Online=true` ⇒ 0 Restarts |
| `test_offline_node_triggers_restart` | `Online=false` + `netcheck` scheitert ⇒ genau 1 Restart |
| `test_restart_is_rate_limited_to_once_per_15_minutes` | Zwei Ausfälle in 5 min ⇒ 1 Restart |
| `test_netcheck_is_only_called_when_status_is_not_clearly_online` | Stufung aus §4.2 hält |
| `test_unit_file_has_the_three_hardening_directives` | Statischer Wächter auf die `.service` |

**Der Test-Harness erbt keine Umgebung** — `SHAREFYX_*`/`SFX_*` vor jedem Subprozess-Aufruf
strippen. Das hat einmal die Produktion 52× neu gestartet; die Regel ist nicht theoretisch.

### 4.4 Abnahme Step B

`P9-16` Unit + Timer existieren, `systemctl list-timers` zeigt den Timer (Nikinger) ·
`P9-17` 5 Tests grün · `P9-18` Härtungs-Direktiven per statischem Wächter belegt ·
`P9-19` Ein absichtlich herbeigeführter Offline-Zustand löst genau einen Restart aus, im Journal
belegt (Nikinger) · `P9-20` V152 beantwortet — mit „gibt es nicht" als zulässigem Ergebnis.

---

## §5 Step C — Vision-Dienst auf der RTX 3060

**Ausführung: Coarbeit in opencode (§0.5.1). Proxmox, LXC und Treiber macht der Nikinger unter
Anleitung; die Skript-Fixes schreibt M3. Ein Commit für den Repo-Anteil.**

### 5.1 Eine Präzisierung vorweg

Ersetzt wird **nicht das Plugin**. `DavidEasden/opencode-vision` ist seit dem 2026-09-11
gemessen zurückgebaut — es amputiert M3s nativen Bildpfad. Ersetzt wird das
**CPU-only-Ollama-Backend** auf der sharefyx-VM (Ollama 0.34.0 + `qwen3-vl:8b`,
`127.0.0.1:11434`) durch einen internen CUDA-Dienst auf dem 3060-Host.

### 5.2 Form (P9-N): eigener LXC auf dem 3060-Host

**Nicht in die sharefyx-VM.** Zwei Gründe, in der Reihenfolge ihres Gewichts:

1. **Das Bauprinzip bleibt physisch nachprüfbar.** „Der Server ist dumm" heißt: kein LLM-Call
   im Serverpfad. Das Vision-Modell bedient die Sichtprüfung des Agenten, nie eine
   sharefyx-Anfrage. Steht es in einer eigenen Kiste, kann jeder künftige Leser das
   nachsehen; steht es in der Produktions-VM, muss er dem Satz glauben.
2. **Die sharefyx-VM bleibt migrierbar.** Die Karte steckt in **einem** Host. Jedes
   Passthrough pinnt die empfangende VM auf genau diesen Host — die Proxmox-Vormerkung führt
   einen primären (i5-14600KF) und einen sekundären Node (Ryzen 7 5800X), und die Migration
   vom 2026-09-10 hat das bereits genutzt. Gepinnt wird genau die Kiste, die im Zweifel auch
   stillstehen darf.

**LXC statt voller VM mit PCIe-Passthrough**, mit zwei ausdrücklich budgetierten Preisen:

- **(a) „Der Treiber lebt auf dem Host" ist verkürzt.** Der Container braucht den Kernel-Teil
  nicht, aber **dieselbe Treiberversion im Userspace** (Installation im Container mit
  `--no-kernel-module`) **plus** cgroup-Device-Regeln für `/dev/nvidia*`. Host-Treiber allein
  reicht nicht; die Versionen müssen übereinstimmen.
- **(b) Kernel-Kopplung.** Ein Proxmox-Kernel-Upgrade, das dem Treiber davonläuft, legt den
  Container still, bis DKMS neu baut.

**Der Umschaltpunkt zur vollen VM**, damit er nicht im Bau improvisiert wird: `[VERIFY] V154` —
**ist IOMMU auf dem 3060-Host aktiv und der Slot sauber gruppiert?** Wenn ja und wenn die
Treiberpflege im Container als untragbar bewertet wird, ist die VM mit Passthrough die
Alternative; sie kapselt den Treiber vollständig, kostet dafür VFIO-Einrichtung. **Beide
Varianten pinnen die GPU-Kiste auf den 3060-Host — das ist gewollt, nicht der Unterschied.**

### 5.3 Die zwei Skript-Ungereimtheiten (Repo-Anteil, opencode/M3-tauglich)

Beide beißen **genau dann**, wenn der Endpoint nicht mehr `127.0.0.1` ist — also ab diesem Step:

| Datei:Zeile | Befund | Fix |
|---|---|---|
| `phase8_6_ui_polish/scripts/mcp_local_vision_server.py:223` | Loggt beim Start `DEFAULT_ENDPOINT`, während der echte Aufruf (`:195`) `LOCAL_VISION_ENDPOINT` auflöst. Mit gesetzter Variable behauptet die Startzeile `127.0.0.1:11434`, obwohl die Anfragen zur GPU-Kiste gehen | Den **aufgelösten** Endpoint loggen. Eine Zeile |
| `phase8_6_ui_polish/scripts/mcp_local_vision_server.py:274` | Das `--endpoint`-Flag wirkt nur auf `--check`; `serve()` liest `args.endpoint` nie | `serve()` nimmt den aufgelösten Endpoint als Parameter; Präzedenz `Umgebungsvariable < Flag`, wie in `vision_ollama.py:44` |

`[VERIFY] V155` — beide Zeilennummern gegen den aktuellen Stand prüfen; sie stammen aus dem
Handover, nicht aus einer eigenen Messung dieser Session.

### 5.4 Schritte

| # | Aktion | Wer |
|---|---|---|
| C1 | IOMMU-/Treiberstand des 3060-Hosts feststellen (V154) | Nikinger |
| C2 | LXC anlegen, NVIDIA-Userspace-Treiber in **Host-Version** mit `--no-kernel-module`, cgroup-Regeln für `/dev/nvidia*` | Nikinger |
| C3 | Ollama im Container, `qwen3-vl:8b` (Q4_K_M, 6,1 GB) pullen, Bindung **nur** auf die Proxmox-Bridge | Nikinger |
| C4 | Feste interne Adresse vergeben und dokumentieren | Nikinger + M3 |
| C5 | `LOCAL_VISION_ENDPOINT` in `~/.config/opencode/` setzen — **nicht im Repo**. Kein Geheimnis, aber hostspezifisch | opencode/M3 + Nikinger |
| C6 | Die zwei Skript-Fixes aus §5.3 | opencode/M3 |
| C7 | Cold-Start messen: vorher **46–180 s** (CPU, i5-14600KF), nachher erwartet Sekunden | opencode/M3 |
| C8 | Entscheiden, ob das CPU-Ollama auf der sharefyx-VM abgebaut wird | Nikinger |

`[VERIFY] V156` — bleibt es bei `qwen3-vl:8b`, oder wird die VRAM-Luft genutzt (praktische
Obergrenze ~12–14B bei Q4)? **Empfehlung: erst beim alten Modell bleiben.** Sonst ändern sich
Geschwindigkeit *und* Urteilsqualität gleichzeitig, und der gemessene Cold-Start-Gewinn ist
nicht mehr zuzuordnen.

### 5.5 Was dieser Step ausdrücklich **nicht** löst

Handover §4.6 nennt zwei Hälften. Die **Hardware**-Hälfte löst dieser Step. Die **inhaltliche**
Hälfte — *wer beurteilt das Bild, und mit welchem Prompt* — bleibt offen. P9 nutzt den Dienst
für die eigene Sichtprüfung im Gate; ein Urteilsverfahren, das die Nikinger-Sichtung ersetzt,
entsteht hier **nicht**. Konvention §2 gilt unverändert: **Visuelles ist Nikinger-Sache.**

### 5.6 Abnahme Step C

`P9-21` Der Dienst antwortet von der sharefyx-VM aus auf der internen Adresse ·
`P9-22` Von außen nicht erreichbar — kein Funnel, kein Port (Hard Rule 6) ·
`P9-23` Cold-Start gemessen und gegen 46–180 s gestellt · `P9-24` Beide Skript-Fixes aus §5.3
im Code, Startzeile zeigt den echten Endpoint · `P9-25` V154 und V156 beantwortet ·
`P9-26` Ein echter Sichtprüfungslauf gegen ein bestehendes Screenshot liefert dieselbe Aussage
wie der CPU-Lauf vom 2026-09-10 (`c4_p8519_01_radiogruppe_im_dialog.png`).

---

## §6 Step D — Die zwei gemeldeten Bugs

**Ausführung: opencode/M3. Ein Commit. Reiner Frontend-Step.**

### 6.1 D1 — ESC verlässt den Vollbildmodus **und** schließt das Item

**Befund (`app.js:204`):** der globale `keydown`-Handler prüft `document.fullscreenElement`
**nicht**. Auf dem Mac verlässt der Browser bei ESC den Vollbildmodus, und **derselbe**
Tastendruck erreicht zusätzlich die App — zwei Aktionen auf einen Druck.

**Relevanz ist seit P8.6 höher, nicht niedriger:** die Phase hat ESC an **drei** Stellen tragend
gemacht (N.8 Karte-zurück, H-R.7 Editor-Fullview, H-R.8 Listen-Slot). Der Doppeleffekt trifft
heute mehr Pfade als vor der Phase.

**Fix:** als **erste** Bedingung im `Escape`-Zweig (`app.js:204`):

```js
if (event.key === "Escape") {
  // Der Browser verlaesst bei ESC selbst den Vollbildmodus und liefert denselben
  // Tastendruck zusaetzlich an die App -- ohne diese Zeile loest ein Druck zwei
  // Aktionen aus (Nikinger-Meldung 2026-09-19, Mac).
  if (document.fullscreenElement) return;
  …
}
```

**Warum die Wurzel und nicht jeder Zweig:** ein Wächter an **einer** Stelle statt elf Kopien,
die auseinanderdriften. Dieselbe Begründung, die in P8.6 für `dedupeEdges()` galt.

**Warum vor `preventDefault()` und ohne es:** der Vollbild-Ausstieg ist Browserverhalten und
soll stattfinden; die App tut nur zusätzlich nichts.

`[VERIFY] V157` — `document.fullscreenElement` ist während des ESC-`keydown` noch gesetzt, oder
schon `null`? Die Spec lässt beide Reihenfolgen zu, und davon hängt ab, ob der Wächter greift.
**Messen, bevor gebaut wird**, in Chromium **und** WebKit — die Meldung kam von einem Mac.
Falls `null`: Ausweichweg ist ein `fullscreenchange`-Listener, der einen kurzen Zeitstempel
setzt, gegen den der ESC-Zweig prüft (≤ 100 ms). Der Ausweichweg ist der zweite Griff, nicht
der erste.

### 6.2 D2 — Kein Drop-Ziel zurück auf die Space-Wurzel

**Befund (gemessen 2026-09-19):** `bindFolderDropTarget()` (`tree.js:119`) hat **genau eine**
Aufrufstelle: `tree.js:205`, `if (space.own)`, auf Ordner-Buttons. Es gibt damit ein Drop-Ziel
**in** einen Ordner hinein, aber keines zurück heraus. „Rein ja, raus nein" ist kein Glitch,
sondern ein fehlendes Ziel.

**Fix:** die Space-Zeile selbst wird ein Drop-Ziel mit `folderPath = ""`. Anker:
`tree.js:232 renderSpaceNode(space)` — dort denselben `bindFolderDropTarget(button, "")` für
`space.own` setzen wie `:205` für Ordner.

**Die Falle, die hier lauert und `[VERIFY] V136` beantwortet:** Block G7 hat die Zähler-Chips der
Space-Zeile auf `<span role="button">` umgestellt (verschachtelte `<button>` sind ungültiges
HTML). Ein `drop`-Listener auf dem äußeren Button muss deshalb prüfen, dass das Ereignis nicht
aus einem Chip kommt, sonst hängt das Ziel an einem Element, das der Nutzer als Zähler liest.
**V136 ist damit nicht länger eine offene Frage, sondern eine Bauvorgabe** — sie ist in P8.6
durchgerutscht, nicht entschieden worden.

`[VERIFY] V158` — reicht `event.target.closest(".overview__space-open")` zur Unterscheidung, oder
braucht es eine explizite Chip-Klasse? Am echten DOM messen.

**Dazu gehört ein sichtbarer Zustand:** die Space-Zeile bekommt dieselbe
`--dragover`-Rückmeldung wie Ordner heute (`tree.js:123`,
`tree__realfolder--dragover`). Ein Drop-Ziel ohne sichtbaren Zustand ist kein Ziel, sondern
Raten — genau der Befund 6 aus P8.6, nur eine Ebene höher.

### 6.3 Tests

| Test | Datei | Prüft |
|---|---|---|
| `test_escape_handler_checks_fullscreen_element` | `phase5_ui/tests/test_static_routes.py` | Statischer Wächter: `document.fullscreenElement` steht im `Escape`-Zweig **vor** jeder anderen Bedingung |
| `test_space_row_is_a_drop_target_for_the_space_root` | dto. | `bindFolderDropTarget` hat **zwei** Aufrufstellen, eine mit leerem Pfad |
| `test_space_drop_target_ignores_the_counter_chips` | dto. | Die Chip-Ausnahme aus V136 ist im Code vorhanden |

**Warum statische Wächter und nicht nur der Smoke:** beide Bugs sind Regressionen, die ein
späterer Umbau still wieder einführt. P8.6 hat dafür den Mechanismus (`test_static_routes.py`),
und er hat mehrfach getragen.

### 6.4 Abnahme Step D

`P9-27` ESC im Vollbild verlässt den Vollbildmodus und schließt **nichts** — am echten Gerät
belegt (Nikinger) · `P9-28` ESC außerhalb des Vollbilds verhält sich unverändert wie vor P9 ·
`P9-29` Ein Item lässt sich aus einem Ordner auf die Space-Zeile zurückziehen ·
`P9-30` Der Drop-Zustand ist sichtbar · `P9-31` Ein Zug auf einen Zähler-Chip löst **kein**
Verschieben aus (V136) · `P9-32` 3 neue Tests grün, `ui_budget` 5/5.

---

## §7 Step E — Karte: Reload-Overload und V118

**Ausführung: opencode/M3. Ein Commit. Reiner Frontend-Step (P9-M).**

### 7.1 Befund

`loadGraph()` (`graph.js:150`) macht bei **jedem** Aufruf einen vollen `api("/graph")`-Abruf,
baut alle Knoten neu auf, verwirft die Positionen (`x: 0, y: 0`), sät neu
(`seedInitialPositions()`) und startet die Simulation neu (`runSimulation()`). Aufrufer sind
`app.js:116`, `app.js:156` und `app.js:264` — also praktisch jeder Wechsel in die Übersicht.

Das ist der gemeldete „Reload-Overload" (`p8x_ui_polish_notes.md` §2.1) und er ist seit P8.6
teurer geworden, nicht billiger: **ESC bringt die Karte zurück** (N.8), der Weg wird also
häufiger gegangen.

### 7.2 Fix, in zwei Teilen

**(a) Nicht neu holen, wenn sich nichts geändert hat.** `loadGraph()` merkt sich eine Signatur
der zuletzt geladenen Daten (Knotenzahl + Kantenzahl + höchstes `updated` — **keine** neue
Server-Antwort, alles ist schon im Payload). Bei Gleichheit: `draw()` statt vollem Neuaufbau.

**(b) Positionen überleben den Wiedereintritt.** Die Knoten behalten `x`/`y`, wenn ihre `id`
bereits bekannt ist; nur neue Knoten werden gesät. `seedJitter(id, salt)` (P8.6-D2, FNV-1a)
macht die Saat bereits deterministisch — der verbleibende Sprung kommt daher, dass die
Simulation nach jedem Eintritt von vorn beginnt, nicht aus der Saat.

**Warum kein `localStorage`-Snapshot:** das Projekt benutzt `localStorage` bewusst fast nicht
(V99: `sfx:draft:` ist `sessionStorage`); ein Layout-Snapshot wäre eine Eskalation gegenüber der
Projektkonvention für einen Effekt, den (b) im Speicher umsonst liefert. **Die Notiz §2.4 nennt
den Snapshot als Alternative — er wird hier bewusst nicht genommen, und das ist der Grund.**

**Was dieser Step ausdrücklich nicht anfasst:** `/api/v1/graph`, `storage/linkscan.py`,
`index.py :: replace_item_links` — P9-M. Die neunte Contract-Öffnung gehört Step F, und sie
bekommt keinen zweiten Anlass.

### 7.3 V118 schließen — Zwillingskanten

**Frage:** wird eine Tag-Kante **und** eine explizite Kante zwischen denselben zwei Knoten als
zwei Linien gezeichnet? `dedupeEdges()` (P8.6-D1) fasst `implicitEdges` bewusst nicht an; aus
Screenshot 13 war es nicht beantwortbar, weil die Karte ohne Hover keine Knoten-Labels zeigt.

**Weg (gegenüber dem Handover-Vorschlag konkretisiert):** `p9_hardening_smoke.py` bekommt eine
Station, die ein Knotenpaar mit **beiden** Beziehungen im Wegwerf-Datenstand erzeugt und danach
über CDP die gezeichneten Segmente zählt — eine Label-Capture ist nicht nötig, wenn das Paar
bekannt ist. **Erst messen, dann entscheiden**, ob zwei Linien gewollt sind; das ist eine
Nikinger-Frage, keine Bauentscheidung.

### 7.4 Tests

| Test | Prüft |
|---|---|
| `test_load_graph_skips_the_refetch_when_the_signature_is_unchanged` | Gemockter `api()`, zweiter Aufruf ⇒ 1 Fetch |
| `test_known_nodes_keep_their_position_across_reentry` | Bekannte ID behält `x`/`y`, neue wird gesät |
| `test_graph_module_does_not_touch_the_api_contract` | Statisch: keine neuen Endpunkte in `graph.js` |

### 7.5 Abnahme Step E

`P9-33` Zweiter Eintritt in die Übersicht ohne Datenänderung erzeugt **keinen** zweiten
`/graph`-Abruf · `P9-34` Die Karte springt beim Wiedereintritt nicht — im Screenshot-Paar belegt ·
`P9-35` Datenänderung führt weiterhin zum Neuladen · `P9-36` V118 beantwortet, mit
Nikinger-Entscheidung, falls es zwei Linien sind · `P9-37` Tabu-Diff leer, `ui_budget` 5/5.

---

## §8 Step F — Schema-Fundament (neunte P1-Contract-Öffnung)

**Ausführung: opencode/M3. Ein Commit — getrennt von jedem anderen Step.**

> **Dies ist die angekündigte, datierte neunte Öffnung (P9-G).** Der Umfang steht unten
> zeilengenau; die enge Probe in §8.7 ist **Abbruchkriterium**, nicht Zielgröße. Wer beim Bauen
> merkt, dass er mehr braucht, **hält an und legt vor** — er erweitert nicht.

### 8.1 Warum überhaupt der Kern

„Aktuelle Aufgabe markieren" und „Aufgabe assignen" sind zwei Wünsche für **einen** Zustand;
getrennt gebaut entstehen zwei Felder dafür — davor warnt der Handover ausdrücklich.

Über `Item.extra` (`models.py:38`) ginge beides **heute schon ohne Kernänderung**: unbekannte
Frontmatter-Felder überleben den Round-Trip unangetastet (`store.py:72` liest sie,
`store.py:120` schreibt sie zurück). Der Preis wäre: nicht im Index, also kein serverseitiges
Filtern oder Sortieren — und vor allem **kein erzwungenes Vokabular**. Ein Tippfehler in einem
`doing`-Tag erzeugt still einen zweiten Zustand, den niemand bemerkt.

**Nikinger-Entscheidung 2026-09-19: der Kern wird geöffnet** (P9-H). Der Ausschlag gab, dass
`_status_hint()` (`tools.py:133`) das Statusvokabular **aus `STATUS_VALUES` generiert** — der
neue Wert erreicht damit alle MCP-Werkzeuge, ohne dass irgendwo etwas abgetippt wird. Genau
dafür wurde die Funktion in P6.5-C gebaut.

### 8.2 Der genaue Umfang — neun Stellen, mehr nicht

| # | Datei:Zeile | Änderung |
|---|---|---|
| F1 | `phase1_storage/storage/models.py:108` | `STATUS_VALUES["task"]` → `frozenset({"open", "doing", "done", "archived"})`. **`note` bleibt unverändert** `{active, archived}` |
| F2 | `phase1_storage/storage/models.py:17` (`Item`) | Neues Feld `assignee: str = ""` nach `share_write` |
| F3 | `phase1_storage/storage/models.py:53` (`ItemSummary`) | Dasselbe Feld — sonst kennt jede Trefferliste den Zustand nicht |
| F4 | `phase1_storage/storage/store.py:38` (`_KNOWN_FIELDS`) | `"assignee"` aufnehmen, damit es nicht in `extra` landet |
| F5 | `phase1_storage/storage/store.py:519` (`create`) | `assignee = fields.pop("assignee", "")`, an den `Item(...)`-Aufruf durchreichen |
| F6 | `phase1_storage/storage/store.py:~118` (Frontmatter-Serialisierung) | `if item.assignee: fields["assignee"] = item.assignee` — **nur bei nicht-leer**, exakt nach dem Muster von `visibility`/`share_read` direkt darüber. Sonst bekäme jedes bestehende Item beim nächsten Write ein stilles `assignee: ""` |
| F7 | `phase1_storage/storage/index.py:33` (`_SCHEMA`) | Spalte `assignee TEXT NOT NULL DEFAULT ''` |
| F8 | `phase1_storage/storage/index.py:30` | `INDEX_SCHEMA_VERSION` **3 → 4** |
| F9 | `phase1_storage/storage/index.py:~251` (Upsert) | `assignee` in die Zeile aufnehmen |

**F8 ist der Grund, warum diese Öffnung billig ist.** `connect()` (`index.py:~73`) verwirft
einen Index mit abweichender `user_version` und legt ihn leer neu an, `Store.__init__` ruft
dann `rebuild_index()` — **es gibt keine Migration zu schreiben.** Genau das ist Hard Rule 2 in
Aktion: die Dateien sind die Wahrheit, der Index ist Ableitung. Wer hier eine
`ALTER TABLE`-Migration baut, hat die Regel missverstanden.

### 8.3 Die Schichten darüber (nicht im P1-Tabu)

| Datei | Änderung |
|---|---|
| `phase5_ui/webui/serializers.py:38/66/94` | `assignee` in `item_to_json`, `summary_to_json`, `overview_row_to_json` |
| `phase5_ui/webui/api.py` | `assignee` auf `POST /api/v1/items` und dem PATCH-Pfad annehmen |
| `phase2_mcp/mcpserver/tools.py` | `assignee` als optionaler Parameter von `create_item` und `update_item`. `_status_hint()` **nicht anfassen** — `doing` erscheint dort von selbst |
| `phase5_ui/webui/static/js/dialogs.js:323` | Liest die Statuswerte bereits aus `state.meta.status_values`; `doing` erscheint ohne Codeänderung. **`[VERIFY] V159` — gegenprüfen, nicht glauben** |

**Was dieser Step ausdrücklich nicht baut (P9-P):** keine Hervorhebung von `doing` auf der
Übersicht, kein Assignee-Picker, kein Filter-Knopf. Nach Step F ist der Zustand über
Editor-YAML, REST und MCP setz- und lesbar — **seine Darstellung ist P10.** Die Trennung ist
gewollt: das Fundament wird von einem echten Aufrufer geprüft (den MCP-Werkzeugen), ohne dass
eine UI-Entscheidung mit hineinverhandelt wird.

### 8.4 Eine Frage, die vor dem Bau beantwortet gehört

`[VERIFY] V160` — **was ist `assignee` inhaltlich?** Ein freier String, ein Space-Name, ein
Principal? Der Server darf keine Identität erfinden, und ein freier String erzeugt
`nikinger`/`Nikinger`/`niki` als drei Personen. **Empfehlung: Space-Name**, weil das die einzige
Kennung ist, die der Server ohnehin kennt und autorisiert — aber **nicht validiert**, denn eine
Validierung gegen die Space-Liste wäre eine zweite Contract-Öffnung. Nikinger entscheidet.

### 8.5 Tests

| Test | Prüft |
|---|---|
| `test_task_accepts_the_doing_status` | `create(type="task", status="doing")` geht durch |
| `test_note_still_rejects_doing` | `note` bleibt `{active, archived}` — die Trennung ist der Punkt |
| `test_assignee_round_trips_through_the_file` | Schreiben, lesen, Byte-Vergleich der Frontmatter |
| `test_empty_assignee_is_not_written_to_frontmatter` | F6 — kein stilles Feld in Altbestand |
| `test_assignee_survives_an_index_rebuild` | Index löschen, `rebuild_index()`, Wert steht |
| `test_index_schema_version_is_four` | Statischer Wächter auf F8 |
| `test_old_index_is_discarded_and_rebuilt` | `user_version=3` ⇒ Verwerfen + Neuaufbau, kein Fehler |
| `test_status_hint_lists_doing_without_being_edited` | `_status_hint()` nennt `doing`, `tools.py` unverändert |
| `test_assignee_is_not_swallowed_by_extra` | F4 — `assignee` landet nicht in `Item.extra` |

### 8.6 Datenbestand

**Kein Migrationsskript.** Bestehende Items haben kein `assignee` im Frontmatter und bekommen
keins (F6); der Index baut sich beim nächsten Start neu auf (F8). **`[VERIFY] V161`** — der
Neuaufbau über den echten `DATA_ROOT` dauert wie lange? Bei Items im niedrigen Tausenderbereich
unkritisch, aber **gemessen**, nicht geschätzt: der erste Start nach dem Deploy trägt die Zeit.

### 8.7 Enge Tabu-Probe — Abbruchkriterium

```bash
# GEGEN DEN STEP-F-COMMIT, nicht gegen einen Bereich ueber mehrere Steps:
git diff --stat HEAD~1..HEAD -- phase1_storage/storage     # nach dem Commit
git diff --stat -- phase1_storage/storage                  # davor, im Arbeitsbaum
```

**Die Eingrenzung ist Teil der Probe, nicht Formsache.** Step G fasst `store.py` erneut an
(`Store.trash()`, §9.3). Ein Bereichs-Diff ueber F **und** G misst beide Steps und kann den
Abbruch an einer voellig legitimen Step-G-Datei ausloesen. Die Probe gilt **dem Step-F-Commit
allein** — deshalb steht Step F vor Step G und bekommt einen eigenen Commit.

**Muss genau drei Dateien zeigen:** `models.py`, `store.py`, `index.py`. Jede vierte Datei,
jede Berührung von `acl.py`, `linkscan.py`, `patch.py`, `files.py`, `history.py`,
`frontmatter.py` ist **Abbruchgrund** — anhalten, vorlegen, nicht weiterbauen.

### 8.8 Abnahme Step F

`P9-38` Die enge Probe zeigt genau drei Dateien · `P9-39` 9 Tests grün ·
`P9-40` `_status_hint()` nennt `doing`, ohne dass `tools.py` es enthält ·
`P9-41` `note` akzeptiert `doing` nicht · `P9-42` Ein Altbestands-Item bekommt beim Write kein
leeres `assignee` · `P9-43` Index-Neuaufbau über den echten `DATA_ROOT` gelaufen, Zeit notiert
(V161) · `P9-44` V160 beantwortet und im Plan als Lock nachgetragen.

---

## §9 Step G — Löschen (F2) nach `_trash/`

**Ausführung: opencode/M3. Ein Commit.**

### 9.1 Semantik (P9-I, P9-J, P9-K)

**Löschen heißt Verschieben nach `_trash/`, nie `unlink`.** Der Präzedenzfall steht im Code:
`store.py:849 delete_asset()` macht es für Assets seit Lock N5 genau so, und `store.py:815`
überspringt `_trash` bereits beim Scannen — die Unsichtbarkeit ist also **vorhandenes
Verhalten**, kein neuer Mechanismus.

**Der Papierkorb bleibt unsichtbar (P9-J).** Kein Eintrag im Rail, keine Wiederherstellung im
UI, kein API-Endpunkt, der `_trash/` listet. Aus jeder Nutzersicht ist das Item weg;
Wiederherstellung ist Dateisystem- und Git-Arbeit des Nikingers. **Der Gewinn ist genau das:**
die sichere Semantik kostet keine zweite Oberfläche, und niemand verwechselt einen Papierkorb
mit einem Archiv — `archived` existiert bereits und meint etwas anderes.

**Human-only (P9-K):** kein MCP-Werkzeug, kein Bulk, kein Tastenkürzel. Ein Löschwerkzeug im
MCP-Pfad hieße, dass ein prompt-injizierter fremder Body eigene Notizen löschen kann — Hard
Rule 4 nennt fremde Inhalte ausdrücklich potenzielle Befehle.

### 9.2 Das Gate

Zwei Stufen, beide zwingend:

1. **Rückfrage 1:** „Dieses Item wird gelöscht. Es erscheint danach in keiner Liste mehr."
   Bestätigen / Abbrechen.
2. **Rückfrage 2:** Der **Titel des Items** muss eingetippt werden. Exakter Vergleich nach
   `trim()`; kein Fuzzy-Matching, keine Groß-/Kleinschreibungs-Toleranz — das Gate soll eine
   Sekunde Nachdenken erzwingen, und Toleranz entfernt genau diese Sekunde.

**Warum der Titel und nicht die ID:** eine ID tippt niemand ab, er kopiert sie — und ein
Copy-Paste-Gate prüft die Zwischenablage, nicht den Menschen.

**Nur eigene, schreibbare Items.** Dieselbe Bedingung wie `list.js:412` `movable`; kein neuer
Rechtebegriff.

### 9.3 Schichten

| Ebene | Änderung |
|---|---|
| `phase1_storage/storage/store.py` | Neu `Store.trash(item_id, *, version) -> None`. **`version` ist Pflicht** — Hard Rule 3 gilt für jeden Write, und Löschen ist der Write, bei dem ein verlorener Konflikt am teuersten ist. Bewegt die Datei nach `_trash/`, atomar (`tmp` + `os.replace` + `fsync`), und erzeugt einen Git-Commit `trash` — dasselbe Muster wie `asset_trash` (`store.py:863`) |
| `phase5_ui/webui/api.py` | `DELETE /api/v1/items/{id}` mit `If-Match`- bzw. `version`-Parameter; Konflikt ⇒ `ConflictError` wie jeder andere Write |
| `phase5_ui/webui/static/js/dialogs.js` | Zweistufiger Dialog; das Confirm-Muster existiert (`confirmDialogEl`, `app.js:205`) und wird wiederverwendet, nicht nachgebaut |
| `phase5_ui/webui/static/js/list.js` | Löschknopf in der Zeile, **nur** unter `movable` |
| `phase2_mcp/mcpserver/tools.py` | **Nichts.** P9-K |

**`store.py` wird hier ein zweites Mal berührt** (nach Step F). Das ist die einzige Überschneidung
und sie ist beabsichtigt: **Step F zuerst, dann Step G**, damit die enge Probe aus §8.7 sauber
gegen einen Commit läuft, der nur Step F enthält.

### 9.4 Tests

| Test | Prüft |
|---|---|
| `test_trash_moves_the_file_and_keeps_the_bytes` | Datei liegt unter `_trash/`, Inhalt byte-identisch |
| `test_trash_requires_the_current_version` | Falsche `version` ⇒ `ConflictError` |
| `test_trashed_item_disappears_from_list_and_search` | `store.py:815` deckt es — als Wächter festnageln |
| `test_trash_creates_a_git_commit` | Hard Rule 5 |
| `test_trash_refuses_a_foreign_item` | Rechte-Grenze |
| `test_no_mcp_tool_exposes_trash` | Statisch: kein `@mcp.tool` mit `trash`/`delete` im Namen (P9-K) |
| `test_delete_dialog_requires_the_exact_title` | Statisch auf `dialogs.js` |

### 9.5 Was benannt bleibt und nicht gebaut wird

**Die Räumung von `_trash/`.** Sie steht schon im geerbten Ledger und bekommt hier keinen Bau.
Das Verzeichnis wächst; bei zwei Personen und Notizen in Kilobyte-Größe ist das über Jahre
unkritisch, aber es ist **benannt**, nicht übersehen. `[VERIFY] V162` — wächst `_trash/` durch
die Asset-Verschiebungen seit N5 bereits messbar? Einmal nachsehen; falls ja, ist das ein
P10-Posten mit Zahl statt einer Vermutung.

### 9.6 Abnahme Step G

`P9-45` Ein eigenes Item lässt sich nach zweifacher Rückfrage löschen · `P9-46` Ohne exakten
Titel bleibt der Knopf gesperrt · `P9-47` Die Datei liegt unter `_trash/`, byte-identisch ·
`P9-48` Git-Commit im Datenverzeichnis vorhanden · `P9-49` Das Item erscheint in **keiner**
Liste, Suche, Karte oder Übersicht · `P9-50` Kein MCP-Werkzeug kann löschen ·
`P9-51` Ein fremdes Item lässt sich nicht löschen · `P9-52` 7 Tests grün.

---

## §10 Step H — Abhängigkeits-Hygiene

**Ausführung: opencode/M3. Kleiner eigener Commit.**

`phase2_mcp/pyproject.toml:10` pinnt `fastmcp>=3.4,<3.5`; installiert ist **3.4.4**, aktuell in
der 3.4-Linie ist **3.4.7** (2026-08-10). Die 3.4.7 trägt einen Security-Fix: Client-Assertions
werden gegen den exakt beworbenen Token-Endpunkt validiert (CIMD `private_key_jwt` bei
`OAuthProxy`-Aufbauten an nackten Origins).

**`[VERIFY] V163` — betrifft der Fix dieses Projekt überhaupt?** Erster Messbefund
(2026-09-19): sharefyx benutzt FastMCPs `OAuthProxy` **nicht**; die Authentifizierung läuft über
`phase2_mcp/mcpserver/asgi.py :: BearerAuthASGI` gegen den eigenen `phase4_auth/authserver`.
Der Fix greift damit **vermutlich ins Leere** — der Bump ist Hygiene, kein Brand. **Das ist eine
Vermutung aus dem Aufrufbild, keine Codemessung; vor dem Bump gegenprüfen.**

**Der Pin bleibt `<3.5` (P9-R).** FastMCP 4.0.0 (2026-08-31) bringt die MCP-Revision
`2026-07-28` — zustandslos, ohne `initialize`-Handshake, ohne `Mcp-Session-Id`, mit neuen
Pflicht-Headern. Alt-Protokoll-Clients laufen per Aushandlung weiter, es gibt also keinen Zwang.
Die Migration bleibt **V79**, eigene Mini-Phase, seit P5-C so festgelegt. **Eine
Protokollmigration mitten in einer Härtungsphase ist genau die Vermischung, die P8.6 zwei Pläne
gekostet hat.**

**Abnahme:** `P9-53` `fastmcp` 3.4.7 installiert, `pytest` unverändert grün ·
`P9-54` V163 beantwortet · `P9-55` Der Pin ist weiterhin `<3.5`, mit Kommentar und Verweis auf
V79.

---

## §11 Gate

**Ausführung: Claude Code. Der Nikinger führt jeden `systemctl`-Aufruf aus.**

| # | Aktion |
|---|---|
| GA1 | Wegwerf-Instanz auf **Port 18773**, Datenstand über `wegwerf_setup_*`-Muster. Stoppen **ausschließlich** über PID-Datei oder Port — nie `pkill -f` (Hard Rule 9) |
| GA2 | `phase9_hardening/scripts/p9_hardening_smoke.py` — Playwright, zwei Browser. Stationen: ESC im Vollbild · ESC außerhalb · Drop auf die Space-Wurzel · Drop auf einen Chip (muss **nicht** verschieben) · zweiter Übersichtseintritt ohne Refetch · Kartenposition stabil · V118-Kantenzählung · `doing` im Status-`<select>` · `assignee` im Editor-YAML · Löschdialog ohne Titel gesperrt · Löschen erfolgreich · gelöschtes Item in keiner Liste |
| GA3 | **Nikinger-Sichtprüfung** der Screenshots. Konvention §5: Dateiname **und** Checkkriterium in einem Satz im Chat, `screenshots_latest/` umgehängt (P8.6-AK, blockweise) |
| GA4 | Badge `app.html:20` `v3.0.2` → **`v3.1.0`** · `docs/UPDATE_LOG.md`-Eintrag (Format streng: `## <YYYY-MM-DD>`, jede Aussage **eine** `- `-Zeile, kein weicher Umbruch) · Deploy über `phase5_ui/scripts/deploy.sh` · `phase8_5_picker_release/scripts/health_gate.sh --expected-version=v3.1.0 --require-todays-update-log --expected-sha=<sha>` — **die echte Ausgabe gehört in den Commit**, nicht die Behauptung |

**Die Falle, die P8.6 hier zweimal erwischt hat:** `health_gate.sh` liest den Release-SHA aus
`/opt/sharefyx/current`. Eine „8/8 grün"-Zeile in der Doku, die nie so gelaufen ist, hat einmal
vier Wochen lang behauptet, eine Phase sei live, die es nicht war. **Ausgabe einfügen oder die
Zeile weglassen.**

`[VERIFY] V164` — läuft `deploy.sh` unter der neuen Domain-Konfiguration durch? Der `umask 022`-Fix
ist seit P8.6 drin, aber die Basis-URL ist neu.

---

## §12 Step Z — Closeout

Eigene Session, **kein** Produktcode-Touch.

1. Abnahmematrix P9-1 … P9-58 Zeile für Zeile mit Beleg — `✅`/`⚠️`/`⬜`/`ersetzt`.
2. `[VERIFY]`-Bilanz V145–V172 **plus die drei geerbten** (V118, V136, V120).
3. **Der kanonische Closeout steht in diesem Dokument, §12.** Ein Plan 2 entsteht nur, wenn die
   Sichtprüfung ihn erzwingt (P9-T).
4. `docs/concepts/phase9_hardening_uebersicht.svg` — **gerendert und angesehen**, nicht ungesehen
   gemeldet. Werkzeug: `~/.claude-code-tools/`.
5. Rotation per `scripts/rotate_session_block.sh phase9_hardening` — **nie von Hand**.
6. `docs/INDEX.md` per `scripts/rotate_index_updates.sh` — der erste echte Einsatz des in
   Step 0 Gebauten.
7. ROADMAP: P9-Zeile neu schreiben, Status ✅, **P10-Zeile anlegen** mit dem, was P9 benannt und
   nicht gebaut hat (§15).
8. `PHASE9_CLOSEOUT_HANDOVER.md` — **nur**, wenn der Nikinger es anordnet. Konvention ist ein
   Dokument pro Phase (P9-T); der Handover ist die Ausnahme, nicht der Normalfall.

**Die Anker-Falle aus P8.6, damit sie sich nicht wiederholt:** beim Patchen eines Phase-Heads
**nie** mit `str.index("## Nächste Session")` schneiden — die Frontmatter zitiert ihre eigenen
`## `-Namen, und der erste Treffer liegt in der `updated:`-Kette. Nur mit Zeilenumbruch-Ankern
schneiden und vorher die Trefferzahl prüfen. Der Fehler hätte einmal 66 KB entfernt.

---

## §13 `[VERIFY]`-Register

| # | Frage | Step |
|---|---|---|
| V145 | `docs/INDEX.md` nach der Rotation < 38.912 B, mit allen P9-Zeilen? | 0 |
| V146 | Ausnahmeliste in `doc_health.py` deckt sich mit der in `docs/INDEX.md` benannten? | 0 |
| V147 | `pytest`-Baseline wirklich 995? | 0 |
| V148 | Funnel-Custom-Domain-Ausschluss gegen die **aktuelle** Tailscale-Doku bestätigt? | A |
| V149 | Welche Felder in `authserver/metadata.py` leiten sich aus der Basis-URL ab, welche stehen fest? | A |
| V150 | Hält der Anthropic-Connector unter der neuen Domain, in **beiden** Konten? | A |
| V151 | Latenz über den VPS gegenüber 372,9 ms über Funnel? | A |
| V152 | Gibt es ein Tailscale-eigenes Watchdog-Feature ohne kommerzielles Add-on? | B |
| V153 | Polkit-Regel oder `sudoers`-Fragment für den einen `restart`-Aufruf? | B |
| V154 | IOMMU-Zustand des 3060-Hosts — LXC oder volle VM? | C |
| V155 | Zeilennummern `mcp_local_vision_server.py:223/274` gegen den aktuellen Stand | C |
| V156 | Bei `qwen3-vl:8b` bleiben oder VRAM-Luft nutzen? | C |
| V157 | Ist `document.fullscreenElement` während des ESC-`keydown` gesetzt? Chromium **und** WebKit | D |
| V158 | Reicht `closest()` zur Chip-Unterscheidung, oder braucht es eine eigene Klasse? | D |
| V159 | Erscheint `doing` im `<select>` ohne Codeänderung (`dialogs.js:323`)? | F |
| V160 | Was ist `assignee` — freier String, Space-Name, Principal? | F |
| V161 | Dauer des Index-Neuaufbaus über den echten `DATA_ROOT` | F |
| V162 | Wächst `_trash/` durch die Asset-Verschiebungen seit N5 messbar? | G |
| V163 | Betrifft der 3.4.7-Security-Fix dieses Projekt? (Erster Befund: vermutlich nein) | H |
| V164 | Läuft `deploy.sh` unter der neuen Domain-Konfiguration durch? | Gate |
| **V118** | *(geerbt)* Zwillingskanten — zwei Linien gewollt? | E |
| **V136** | *(geerbt)* Chip-Umstellung vs. `bindFolderDropTarget()` | D |
| **V120** | *(geerbt)* Dynamischer Tab-Titel — bleibt bewusst offen, außerhalb jedes Scopes | — |

---

## §14 Abnahmematrix

P9-1 – P9-9 (Step 0) · P9-10 – P9-15 (A) · P9-16 – P9-20 (B) · P9-21 – P9-26 (C) ·
P9-27 – P9-32 (D) · P9-33 – P9-37 (E) · P9-38 – P9-44 (F) · P9-45 – P9-52 (G) ·
P9-53 – P9-55 (H).

**Phasenweite Kriterien:**

`P9-56` Der Bereichs-Tabu-Diff `<start>^..HEAD` über §0.3 ist leer — mit **genau einer**
Ausnahme: der in P9-G angekündigte Step-F-Umfang, belegt durch die enge Probe §8.7 ·
`P9-57` Service-Touch durch einen Agenten **0**: kein `pkill -f`, kein `systemctl`; jede
Wegwerf-Instanz über PID-Datei oder Port gestoppt ·
`P9-58` `pytest` am Phasenende ≥ 995 + die neuen Tests, `ui_budget` 5/5, jeder Step-Commit mit
Doc-Update im selben Commit (Hard Rule 8).

---

## §15 Was P9 benennt und nicht baut — die P10-Liste

Damit Step Z die ROADMAP-P10-Zeile schreiben kann, ohne sie neu herzuleiten:

**Aus dem Nikinger-Feedback 2026-09-19:** Logo + einheitliche Design-Vorlage (Erweiterung der
Selection/Choice-Konvention v3 in `phase8_ui_graph/CLAUDE.md`, **nicht** ihr Ersatz) ·
To-do-Checkboxen im Text (`markdown.js` **und** Schreibpfad ⇒ Hard Rule 3) · Hervorhebung von
`doing` auf der Übersicht · Assignee-Picker und -Filter · Verschieben in fremde Spaces
(Rechte-Thema, §0.6).

**Aus `p8x_ui_polish_notes.md`:** Karten-Stilumbau §2.2 · Karte einklappen §2.5 · verbundene
AI-Sessions §10.8 · Hochkant-/Handy-UI §10.9 · die Radien-/Auswahl-Vereinheitlichung §10.1–§10.7.

**Aus dem geerbten Ledger, unverändert offen:** Q1 Body-Volltextsuche · P6-M Rechteverwaltung
über MCP-Werkzeuge · **V79 FastMCP 4 / MCP-Revision `2026-07-28`** (eigene Mini-Phase) ·
Realtime · Light-Mode (P5-X) · Bulk-Append-MCP-Werkzeug · Ordner umbenennen (die billige
Frontend-Fassung lässt die `.share.yml` eines geteilten Ordners still zurück — Analyse
`phase8_6_ui_polish_plan.md` §0.4.1) · Räumung von `_trash/` · `ROADMAP.md`-Straffung
(42.163 B über dem 40-KB-Softcap, in Step 0.2-c benannt).

**Offen gehalten, mit Absicht:** V120 (dynamischer Tab-Titel).
