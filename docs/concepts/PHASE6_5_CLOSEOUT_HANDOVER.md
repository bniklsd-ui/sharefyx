---
status: snapshot
purpose: Abschluss-Handover P6.5→P7-Block-C — Status, Delta seit dem P6-Handover, Abnahmestand-Tabelle (P6.5-1–14), offene Entscheidungen, [VERIFY]-Bilanz V59–V70
read-when: vor Block C dieser Phase (Space-Verwaltung) einmal ganz lesen — schließt formal Phase 6.5 ab, während P7 selbst weiterläuft
detail: L2
up: ../../phase7_spaces_admin/CLAUDE.md
down:
  - ./phase6_5_tools_images_plan.md              # Entscheidungen P6.5-A–P6.5-V, §0.0 gelockte N1–N6 — Herkunft, nicht Ergebnis
  - ../../phase6_5_tools_images/CLAUDE.md         # laufender Abnahmestand, Modul-Status
  - ./PHASE6_CLOSEOUT_HANDOVER.md                 # Vorgänger; P6-Herkunft dieser Phase
updated: 2026-08-23
---
# Phase 6.5 — Closeout-Handover (P6.5 → Block C dieser Phase)

> **Für den kalten Leser, ohne Beschönigung.** Phase 6.5 ist **code-complete und live deployt**
> (`main`@`f96125e`, 2026-08-21), aber **nicht vollständig live-verifiziert**. Von 14 Abnahmezeilen
> sind **12 live bestanden** (Stand 2026-08-23, P7 Step A8.1). Zwei bleiben offen: **P6.5-12**
> (Entfernen-Knopf ist inzwischen gebaut — P7 Step A3 — aber kein Browser-Klick-Nachweis dieser
> Sitzung) und **P6.5-14** (Nikingers eigene Bewertung der Upload-Ankündigungsdisziplin — kein
> Kriterium, das ein Skript oder ein Testprincipal je selbst erfüllen kann).
>
> **Glyph bleibt 🟡, aus der gemessenen Zahl abgeleitet, nicht gewählt** (P7-Plan §A8.2:
> 14/14 ⇒ ✅, sonst 🟡) — 12/14 ist eindeutig, keine Nikinger-Entscheidung nötig wie beim
> 13/14-Grenzfall, den der Plan vorsorglich benennt.
>
> **Zwei Abnahmezeilen (P6.5-8/13) wurden über eine im P7-Plan §A8.1 ausdrücklich gebilligte
> Substitution geschlossen: `testnutzer-p7` statt Fabian.** Beide Zeilen prüfen einen
> Rechte-Mechanismus (Cross-Principal-Sichtbarkeit eines geteilten Bildes), nicht eine
> Fabian-spezifische Eigenschaft — derselbe serverseitige Code-Pfad (`can_read_item`/
> `can_write_item`, P6.5-M) gilt für jeden zweiten Principal. Herleitung, Skripte, Rohergebnisse:
> `phase7_spaces_admin/CLAUDE.md`s Session-Block 2026-08-23 (A8).

---

## 1 Status in vier Sätzen

1. **Block A (Werkzeug-Ergonomie) ist vollständig live bestätigt** — vier Abnahmezeilen, alle
   über den echten Connector, drei davon in getrennten Nikinger-Gesprächen.
2. **Block B (Bilder) ist zu 8 von 10 live bestätigt.** Der Store trägt Assets korrekt
   (`_assets/<item_id>/`, ein Commit je Upload, kein Binär im `.md`), die MCP-Rechtegrenze
   (`share_read` sieht nur Metadaten, `share_write` sieht Bytes) hält unter echter Probe.
3. **P6.5-12 ist kein „nicht baubar" mehr.** Der ursprüngliche Fund dieser Phase (Gate-A→B-
   Sitzung, 2026-08-23) — `editor.js` hatte keinen Entfernen-Knopf trotz vorhandenem
   `DELETE`-Endpunkt — ist mit P7 Step A3 geschlossen. Was fehlt, ist ausschließlich ein
   Browser-Klick-Nachweis, keine offene Werkzeug-Lücke mehr.
4. **P6.5-14 bleibt strukturell offen.** Es ist ein Verhaltenskriterium über Claude selbst
   („kündigt jeden Upload an"), keine Server-Eigenschaft — es kann durch keinen Testlauf
   dieser Phase abschließend erfüllt werden, nur durch wiederholte Beobachtung des Nikingers.

---

## 2 Delta seit dem P6-Handover

| Was | Wo im Code | Bemerkung |
|---|---|---|
| Achtes MCP-Tool `get_item_meta` | `mcpserver/tools.py` | Reine Metadaten-Antwort, kein Body — P6.5-E/F |
| Werkzeug-Beschreibungskorrekturen | `mcpserver/tools.py` | `list_spaces`-Falschaussage entfernt (P6.5-B), Statuswerte + Aufgabenteilung an vier Schreib-Tools benannt (P6.5-C/D/G) |
| `search_items(in_body=)` | `mcpserver/tools.py`, `storage/store.py` | Körpersuche als MCP-Opt-in, additiv zum P1-Contract (kein neues Modul) |
| Fünfte, benannte P1-Contract-Öffnung | `storage/{models,files,store}.py` | `AssetInfo`, `put_asset()`/`list_assets()`/`get_asset()`/`delete_asset()`, `move()` zieht das Asset-Verzeichnis mit |
| Neuntes/zehntes MCP-Tool | `mcpserver/tools.py` | `get_item_asset`/`put_item_asset`, `MAX_MCP_ASSET_BYTES = 1 MiB`, `AssetNotFound` |
| Web-UI-Fläche Bilder | `webui/api.py`, `webui/static/js/{editor,markdown}.js` | Upload/Anzeige/Cross-Space-Move; **Entfernen-Knopf fehlte bis P7 Step A3** |
| Sechstes Kriterium für Bild-Bytes (P6.5-M) | `mcpserver/tools.py :: get_item_asset()` | Bytes nur bei eigenem Space ODER Schreibrecht — strenger als reines Leserecht, Injektionskanal-Argument |

Kein Delta an `mcpserver/asgi.py`, `authserver/*` (Tabu-Diff blieb über die gesamte Phase leer).

---

## 3 Abnahmestand (P6.5-1–P6.5-14, Stand 2026-08-23)

**Statusregel wie in P4/P5/P6: ✅ heißt live-verifiziert durch einen Menschen (oder einen
gebilligt substituierten Testprincipal), nicht „gebaut".** Volle Beleg-Texte:
`phase6_5_tools_images/CLAUDE.md` §„Abnahmestand".

| # | Kriterium (Kurzform) | Block | Stand |
|---|---|---|---|
| P6.5-1 | Frische Instanz sagt NICHT „nur eigener Space" | A | ✅ |
| P6.5-2 | Nennt erlaubte `status`-Werte ohne Fehlversuch | A | ✅ |
| P6.5-3 | Nutzt `get_item_meta` vor einem Folge-Append | A | ✅ |
| P6.5-4 | Erklärt `patch_item`/`update_item`/`append_to_item`-Aufgabenteilung | A | ✅ |
| P6.5-5 | Bild-Upload sichtbar im UI-Dokument | B | ✅ |
| P6.5-6 | `.md`-Datei enthält nur `asset:`-Referenz, kein Binär/base64 | B | ✅ |
| P6.5-7 | Bilddatei unter `_assets/<item_id>/`, kein UI-Ordner | B | ✅ |
| P6.5-8 | Freigegebenes Bild sichtbar, ohne Freigabe kein Zugriff | B | ✅ (via `testnutzer-p7`) |
| P6.5-9 | Ein Upload = genau ein Git-Commit | B | ✅ |
| P6.5-10 | Cross-Space-Move nimmt Bild mit, ein Commit | B | ✅ |
| P6.5-11 | Fremde `<img>`-URLs/`javascript:` kein Netzabruf, kein `<img>` | B | ✅ |
| P6.5-12 | Bild entfernbar, Referenz rendert danach als Alt-Text | B | 🟡 gebaut (P7 A3), ungeprüft |
| P6.5-13 | Bild nur bei `share_write` sichtbar, nicht bei reinem `share_read` | B | ✅ (via `testnutzer-p7`) |
| P6.5-14 | Kündigt jeden Upload an, lädt nie unaufgefordert | B | offen — Nikingers eigene Bewertung |

**12 von 14 live bestanden.** Verbleibend: P6.5-12 (Browser-Nachweis, kein Blocker), P6.5-14
(strukturell nie durch einen Testlauf abschließbar, siehe §1 Punkt 4).

---

## 4 Offene Entscheidungen für die nächste Planung

### 4.1 P6.5-14 — wie wird „Nikingers eigene Bewertung" je geschlossen?

Zwei Datenpunkte liegen vor (Gate-A→B-Sitzung + eine weitere Sitzung, beide Male kündigte
Claude jeden `put_item_asset`-Aufruf vorher an). Ob das reicht, ist keine Claude-Code-
Entscheidung. Nicht blockierend für irgendeine andere Arbeit — bleibt offen stehen, bis der
Nikinger es explizit abhakt oder eine dritte Sitzung eine Abweichung zeigt.

### 4.2 `_trash/`-Räumung — weiterhin bewusst nicht automatisiert

N5 löst „Bild entfernen" als Verschieben nach `_assets/<item_id>/_trash/`, nie als echtes
Löschen (Entscheidung H bleibt formal unangetastet). Eine automatische Räumung ist explizit
draußen (Plan §5) — mittelfristig braucht `_trash/` eine eigene Lösung, kein Teil dieser Phase.

### 4.3 V64 — claude.ai-Verhalten bei `destructiveHint: True`

Bleibt unverändert offen (kein Deploy-Ereignis schließt Client-Verhalten). Falls eine künftige
Sitzung feststellt, dass claude.ai daraus **keine** wiederholte Rückfrage macht, ist das ein
Befund für den Nikinger, keine stille Hinnahme (P6.5-O bleibt dann die einzige Bremse).

---

## 5 `[VERIFY]`-Bilanz (V59–V70)

| # | Frage | Status |
|---|---|---|
| V59 | `fastmcp>=3.4,<3.5` kann `ImageContent` aus einem Tool zurückgeben | ✅ geschlossen (Planungssession, empirisch) |
| V60 | claude.ai-Custom-Connectors zeigen/verarbeiten `ImageContent` | ✅ geschlossen, 2026-08-21 (Gate-A→B-Sitzung, echter Connector-Rundlauf) |
| V61 | `os.replace` auf einem Verzeichnis ist auf `ext4` brauchbar | ✅ geschlossen (Planungssession, empirisch) |
| V63 | Werkzeug-Beschreibung als Funktionsdict auslesbar | ✅ geschlossen (gegen `fastmcp==3.4.4` geprüft) |
| V64 | Macht claude.ai aus `destructiveHint: True` eine wiederholte Rückfrage? | **offen** — Client-Verhalten, s. §4.3 |
| V65 | Reales ID-Format aus `files.generate_id()` (8 Hex) | ✅ geschlossen (gegen Code bestätigt) |
| V66 | `_require_csrf_json()` prüft Content-Type, passt das auf Rohbytes-Upload? | ✅ geschlossen (`require_csrf()` liest `Content-Type` nirgends) |
| V67 | `X-Content-Type-Options: nosniff` liegt auch auf `/api/v1/**` | ✅ geschlossen |
| V68 | *entfällt* (`assets:`-Zeile in `get_item`s Dateitext) | N/A — Liste steht ausschließlich in `get_item_meta` |
| V69 | `Image(format=…)`-MIME-Mapping für JPEG/WebP | ✅ geschlossen (empirisch geprüft) |
| V70 | Zeilennummern im Plan sind Stand `main`@`2a4d8ca` | erledigt (Snapshot-Hinweis, kein offener Punkt) |

V62 hat im laufenden Register keinen eigenen Eintrag (bei der Übernahme aus `IMAGES_PLAN.md`
in V59–V61/V65 aufgegangen) — kein offener Punkt, nur eine Nummerierungslücke, hier vermerkt
statt stillschweigend übersprungen.

---

## 6 P1-Contract

Die fünfte, benannte Öffnung (Bild-Assets, `put_asset()`/`list_assets()`/`get_asset()`/
`delete_asset()`) ist mit dieser Phase **geschlossen** — siehe `phase1_storage/CLAUDE.md`s
datierten Absatz, dort im selben Commit wie dieser Handover nachgezogen. Die **sechste** Öffnung
(P7, `storage/acl.py`-Schreibseite) ist zum Zeitpunkt dieses Handovers bereits angekündigt
(P7 Step 0.7) und bleibt ausdrücklich offen — dieser Handover schließt sie nicht mit, sie gehört
Block C derselben Phase, die diesen Handover schreibt.
