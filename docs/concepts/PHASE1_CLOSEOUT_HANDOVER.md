---
status: snapshot
purpose: Abschluss-Handover Phase 1 → Phase 2 — Status, Delta, Contract, offene Entscheidungen, [VERIFY]-Bilanz
read-when: Start des Phase-2-Chats, vor dem Entwurf des detaillierten Claude-Code-Plans
detail: L2
up: ../../ROADMAP.md
down:
  - ../../phase1_storage/CLAUDE.md          # Phase-Head, Modulstatus, Session-Blöcke
  - ./phase1_storage_plan.md                # Plan §1/§2 = der Contract im Wortlaut
  - ../../phase1_storage/SESSIONS_ARCHIVE.md # ältere Session-Blöcke, verbatim
updated: 2026-07-25
---
# Phase 1 — Closeout-Handover (P1 → P2)

> Für einen kalten Leser: den Phase-2-Chat, der daraus den Claude-Code-Plan schreibt.
> **Dieses Dokument wiederholt keine Implementierungsdetails.** Alles, was in Code, Tests oder
> `phase1_storage_plan.md` steht, wird hier nur verlinkt. Bei Widerspruch gewinnt der Code.

## Ergebnis in fünf Zeilen

1. Phase 1 ist **✅ live-verifiziert** — acht Module (Steps 0–7), 70 Tests grün, `space_cli.py`
   als Beweis, Lauf gegen den echten `DATA_ROOT` durch den Nikinger am 2026-07-25.
2. Der **Contract für P2 steht** und ist ab sofort fix: Frontmatter-Schema, die fünf Dataclasses,
   die `Store`-Signaturen. Änderung daran = Scope-Entscheidung, kein Refactoring.
3. **Alle fünf `[VERIFY]`-Marker der Phase sind aufgelöst.** Zwei davon gegen die ursprüngliche
   Annahme (siehe unten) — der Plan ist an diesen Stellen historisch, nicht gültig.
4. **Sechs Punkte sind vor dem P2-Plan zu entscheiden**, drei davon berühren Hard Rule 4
   (fremde Spaces read-only). Sie stehen unten als D1–D6.
5. P1 enthält **kein Netz, kein MCP, keine Auth** — das war Absicht und ist der Grund, warum
   der Konfliktfall überhaupt sauber beweisbar war.

## Delta seit dem letzten Handover

Es gibt **kein** `PHASE0_CLOSEOUT_HANDOVER.md`; P1 war die erste Phase. Der letzte Handover ist
der archivierte Planungs-Block (`phase1_storage/SESSIONS_ARCHIVE.md`, 2026-07-24). Sein Stand war
wörtlich: *„Es existiert noch kein Code und kein Repo."*

Delta seither: Code-Repo initialisiert, acht Module gebaut, 70 Tests, ein Datenverzeichnis-Repo
mit echtem Inhalt, zwei Advisor-Funde gefixt (Drift-Bump überlebt `rebuild_index`;
`.gitignore` auch für ein vorhandenes `DATA_ROOT`-Repo), Status in `ROADMAP.md` und
Root-`CLAUDE.md` auf ✅ gehoben.

## Was P2 als gegeben übernimmt

| Was | Wo es im Wortlaut steht |
|---|---|
| Frontmatter-Schema (11 Felder, Round-Trip-Treue für unbekannte Felder) | Plan §1 |
| `Item` · `ItemSummary` · `SpaceInfo` · `SearchResult` · `IndexStats` | `phase1_storage/storage/models.py` |
| `Store`-Signaturen (`list_spaces`/`search`/`get`/`create`/`update`/`append`/`archive`/`rebuild_index`) | Plan §2, real in `storage/store.py` |
| Fehlertypen inkl. `ConflictError.current` | `storage/errors.py` |
| Entscheidungen A–H | Plan §0 |
| Rahmenentscheidungen R1–R6 | Root-`CLAUDE.md`, „Current state" |
| P2-Scope (drin/draußen, sechs Tools, kein MCP-Resources) | `ROADMAP.md`, Abschnitt Phase 2 |

**Nicht neu herleiten.** Wer eine dieser Zeilen anfassen will, hat eine Scope-Frage, keine
Implementierungsfrage.

## `[VERIFY]`-Bilanz der Phase

**Aufgelöst (5 von 5):**

| Marker | Herkunft | Ergebnis |
|---|---|---|
| `flock` auf dem Ziel-Dateisystem | Plan §3.2 | ext4 bestätigt, `flock` verlässlich. **Stehende Bedingung:** gilt nur, solange `DATA_ROOT` auf der virtuellen Platte liegt — Startup-Check in `index.py` schreibt sonst `critical`. |
| Round-Trip-Treue von `python-frontmatter` | Plan Step 1 | **Gegen die Annahme aufgelöst.** Bibliothek verworfen (sortiert Keys, castet Timestamps); eigener Parser über PyYAML. |
| Namenskollision `IndexError_` | Plan §1 | Umbenannt in `IndexCorrupt`. Bislang ungenutzt — `index.connect()` heilt Korruption still. |
| Dateisystem-Ermittlung unter Ubuntu | Plan Step 3 | `/proc/mounts` zeilenweise, tiefster passender Mountpoint. `os.statvfs` liefert den Typ tatsächlich nicht. |
| Listing-Größenziel 3 KB | Plan Step 6 | **Gegen die Annahme aufgelöst.** 3 KB war strukturell unerreichbar (Floor allein ~7 KB bei 30 Items). Kalibriert und getestet: **< 16 KB**. Nikinger-Entscheidung: ~2.500–3.000 Tokens sind okay, Feldsatz bleibt. |

**Offen, aber nicht P1-Eigentum** — P2 erbt sie und muss sie bei Ausführung prüfen:

- `[VERIFY]` **R2** — Custom Connectors auf Claude Pro, kein Owner-Gate (Root-`CLAUDE.md`).
- `[VERIFY]` **`fastmcp` über Streamable HTTP** (`ROADMAP.md`, Phase 2). Das ist der einzige
  Marker, der den P2-Plan direkt blockiert, wenn er falsch ist.
- `[VERIFY]` **OAuth-Callback-URLs / unterstützte Auth-Spec-Version** (`ROADMAP.md`, Phase 5).

## Offene Entscheidungen vor dem P2-Plan

Reihenfolge = Priorität. D1–D3 gehören in den Plan, nicht in die Implementierung.

**D1 — Zwei Contract-Felder sind Claude-Code-Eigenentscheidungen, nie formell bestätigt.**
`ItemSummary` (Plan §4 Step 1 nennt nur vier Dataclasses) und `SpaceInfo.name` / `.item_count`
(im Plan nicht spezifiziert) wurden beim Bau ergänzt, weil §2 sonst nicht umsetzbar war. Der
Phase-Head verlangt ausdrücklich Gegenprüfung, **bevor** P2 darauf aufbaut. Entscheidung: so
bestätigen oder jetzt ändern — nach dem ersten P2-Tool ist es teuer.
*Verweis: `phase1_storage/CLAUDE.md`, Session-Block, „Implementierungsentscheidung".*

**D2 — `Store.update(..., status=...)` validiert den Statuswert nicht.**
Die CLI hält das mit `argparse choices` ab, der Store selbst nicht. Ein MCP-`update_item` ist ein
**zweiter Eingang, der an dieser Absicherung vorbeigeht** — `status: bogus` landet dann im
Frontmatter und `search()` sortiert es still als „nicht offen" ein. Entscheidung: Validierung im
Store (= §2-Änderung, sauber, einmal) oder in der Tool-Schicht (= Duplikat, das beim dritten
Adapter in P4 wieder auftaucht). *Verweis: `storage/store.py`, `update()`; Step-7-Block, Fund 2.*

**D3 — `get()` ist ein Writer, und das kollidiert mit Hard Rule 4.**
Bei erkannter Drift schreibt `get()` das `version`-Feld in die Datei zurück und erzeugt einen
Git-Commit `drift <id> [<space>]`. Der Store kennt keine Autorisierung — Rechte sind P2. Folge:
**ein Read-Tool auf den fremden Space schreibt in dessen Datei**, sobald der Kollege dort im
Editor editiert hat. Das ist Systemmetadatum, kein Inhalt — aber „Cross-Space-Writes existieren
architektonisch nicht" ist als Regel schärfer formuliert. Entscheidung explizit treffen, nicht
beim Debuggen entdecken. *Verweis: `storage/store.py`, `_reconcile_and_get_row()`.*

**D4 — Default-`limit` der MCP-Suche.**
`Store.search()` hat `limit: int = 50`. Gemessen sind ~345 B/Item realistisch, ~467 B/Item im
Ceiling. Ein Default-Listing liefert damit grob 17–23 KB, also deutlich über dem gemessenen
30-Item-Fall, den der Nikinger akzeptiert hat. Empfehlung: Default in der **Tool-Schicht**
senken, den Store nicht anfassen (Contract). *Verweis: Step-6-Block, Messung.*

**D5 — Archivierte Items sind im Default-Listing enthalten.**
`search()` filtert `status` nur, wenn der Aufrufer es verlangt; `rebuild_index()` indiziert
`_archive/` bewusst mit. Ein MCP-`search_items` ohne Default-Filter zeigt also Archiviertes.
Entscheidung: Tool-Default `status != archived` oder bewusst alles zeigen.

**D6 — `search()` liest jede indizierte Datei von der Platte.**
Gefiltert und sortiert wird in Python, nicht in SQL; der Index dient faktisch als Pfadverzeichnis.
Bei zwei Nutzern und einigen hundert Items unkritisch — aber P2 hängt das an einen Mobilfunk-
Uplink, an dem Claude auf jedes Tool-Result wartet. Entscheidung: bewusst so lassen und
dokumentieren, oder in P2 als contract-neutrale Optimierung mitnehmen (SQL filtert, Dateien nur
noch für die Snippets der Ergebnisseite lesen). *Kein Bug — eine Kostenfrage.*

## Initiale Vorbereitungsschritte (Step 0 des Phase-2-Chats)

Prompt 2 verlangt einen Verifikationsdurchlauf vor dem eigentlichen Plan. Hier ist er
vorbelegt. „Nichts zu tun" ist bei einzelnen Punkten ein zulässiges Ergebnis — aber A1–A3 sind
es nicht.

### A · Rotationsregel operationalisieren

Die Regel wurde in P1 formal eingehalten und faktisch unterlaufen: der Head trug zwei
Session-Blöcke, der zweite entging der Regel nur dadurch, dass er anders überschrieben war. Eine
Regel, die niemand mechanisch ausführen kann, wird beim nächsten Mal wieder von Hand ausgelegt.
Deshalb bekommt sie ein Werkzeug und alle Dokumente einen Verweis darauf.

**A1 — Überschrift des verbliebenen P1-Blocks auf das Schema bringen.** Aus
`## Phase 1 ist live-verifiziert (…)` wird
`## Session stopped — 2026-07-25 (Phase 1 live-verifiziert, Phase abgeschlossen)`.
Eine Zeile, kein Move. Muss **vor** A2 passieren, sonst findet das Skript nur einen Block.

**A2 — `scripts/rotate_session_block.sh` einchecken** (Root-`scripts/`, neben
`dev_install.sh`), `chmod +x`, danach für `phase1_storage` laufen lassen. Das Skript schneidet
ältere Blöcke per `sed -n 'A,Bp'` heraus, prüft die Reassemblierung mit `cmp` gegen das
Original, liest jeden Block nach dem Einfügen byte-identisch gegen und schreibt erst dann.
Erwartetes Ergebnis: Head von ~34 KB auf ~11 KB, Archiv mit drei Blöcken newest-first.

**A3 — Verweise setzen.** Alle Stellen, die die Rotationsregel erwähnen, nennen künftig das
Skript statt einer Handlungsanweisung. Der Wortlaut der Regel bleibt, nur das Werkzeug wird
benannt:

| Datei | Was sich ändert |
|---|---|
| `CLAUDE.md` (Root), „Doku-Hygiene" | Halbsatz ergänzen: Durchführung über `scripts/rotate_session_block.sh`, nie von Hand |
| `phase1_storage/CLAUDE.md`, „Harte Regeln" | `sed -n 'A,Bp'` durch den Skriptaufruf ersetzen — das Skript *ist* das `sed` |
| `phase2_mcp/CLAUDE.md` (neu anzulegen) | Rotationsregel von P1 übernehmen, gleich mit Skriptverweis |
| `docs/PROMPTS.md`, Prompt 1 | „the previous one moves verbatim to SESSIONS_ARCHIVE.md" → Skriptaufruf nennen |
| `docs/PROMPTS.md`, Prompt 3, Punkt 4 | „mechanisch, nie abtippen" → Skriptaufruf nennen; der **Prüf**schritt bleibt bestehen, das Skript ersetzt nur die Ausführung |
| `README.md` | nichts. Das Skript ist Doku-Wartung, kein Setup-Schritt |

**A4 — zwei Dinge bewusst NICHT tun:**

- `docs/DOC_LAYERS_CONVENTION.md` **bleibt unangetastet.** Sie ist eine byte-identische Kopie
  aus dem Trading-Bot-Repo und bewusst projekt-agnostisch; ein Skriptpfad aus *diesem* Repo
  gehört dort nicht hinein. Wer das Werkzeug auch dort haben will, ändert die Datei im
  Trading-Bot-Repo und kopiert erneut — so steht es in der Root-`CLAUDE.md`.
- **Keine Indexzeile für die `.sh`.** `docs/INDEX.md` ist die Karte der `.md`-Dateien;
  `scripts/dev_install.sh` steht dort ebenfalls nicht. Wer Skripte indizieren will, ändert die
  Konvention bewusst und nimmt beide auf — nicht eines aus Reflex.

### B · Verifikationsdurchlauf (Prompt 2, Haushalt)

- `up:`/`down:`-Ziele aller Header-Cards auflösbar? Hat jede `.md` eine Indexzeile?
  `find . -name "*.md" -size +40k` — jeder Treffer muss 📕/📦 sein.
- **`files.rename_for_new_slug()` ist toter Produktivcode.** `store.py` ruft
  `files.move_file()` direkt; nur `test_files.py` benutzt die Funktion noch. Entfernen oder
  benutzen — nicht liegen lassen, sie steht in der Contract-Fläche.
- **Doku-Drift:** der Step-2-Session-Block nennt `rename_for_new_slug()` als Ergebnis, der Code
  nutzt `move_file()`. Eine Zeile mit Datum korrigieren.
- **Branchname:** `DATA_ROOT` steht auf `master`, das Code-Repo auf `main`. Kosmetisch, kein
  Remote — nur wissen, bevor jemand ein Backup-Skript gegen `main` schreibt.
- **Drei Schreibweisen für einen Namen:** Repo/Drive `sharefyx`, VM-Pfade `/home/savefyx/…`,
  Code-Repo-Verzeichnis `/home/savefyx/dev/savefxy` (Buchstabendreher). P3 schreibt
  systemd-Units mit absoluten Pfaden — das jetzt festzulegen ist billiger als danach.

## Was hier bewusst NICHT steht

Modulinterna, Testnamen, Signaturen, Schema-Spalten, Transkripte. Alles davon steht in
`phase1_storage/CLAUDE.md`, in den Tests und in `phase1_storage_plan.md`. Der Phase-2-Chat soll
mit **diesem** Dokument plus den zwei verlinkten Karten starten können — nicht mit einer zweiten
Kopie des Plans.

## Nächster Schritt

Browser-Planungssession Phase 2 (Prompt 2 in `docs/PROMPTS.md`). Ergebnis: **ein** Dokument
`docs/concepts/phase2_mcp_plan.md`, ausführungsreif für Claude Code, mit gelockter
Entscheidungstabelle und `[VERIFY]`-Markern für alles, was sich seit dem Wissensstand geändert
haben kann — insbesondere MCP-Spec und Connector-Verhalten.
