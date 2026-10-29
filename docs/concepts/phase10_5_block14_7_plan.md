---
status: live
purpose: Plan P10.5 Block 14.7 — die Gehirnkarte wird kompakt und die Punkte verteilen sich: Anker dichter gepackt (Buchten weg), Items füllen ihre Region, Kontur ohne 8-px-Treppe. Ausführung Claude Code (Nikinger 2026-10-29).
read-when: vor dem Bau von 14.7, oder wenn die Karte wie ein Seestern mit leeren Buchten aussieht
detail: L2
up: ../../phase10_5_finishing/CLAUDE.md
down:
  - phase10_5_block14_6_plan.md                          # 📗 14.6 — der Körper (Schließen), Muster dieses Plans
  - phase10_5_block14_kartenlayout_plan.md               # 📗 Block 14 — L1–L4, Abnahme 65–71
  - ../../phase5_ui/webui/static/js/graph.js             # `computeRegions()`, `computeLobes()`, `chainEdges()`
  - ../../phase10_5_finishing/probes/p105_b14_karte_bilder.py  # Bilder-Probe (`--konstante`, `--bilder`, Messpflaster)
  - ../../phase10_5_finishing/probes/p105_b14_startwerte.py    # Varianten-Treiber (Muster für das Raster 14.7.2)
updated: 2026-10-29 (Schritt 14.7.0 (b): Ursache von B4 gemessen — **Kandidat (ii), Chaos**; STOPP) | 2026-10-29 (Entwurf, Claude Code — nach der Sichtung der 14.6-Bilder; freigegeben im Chat „schreibe den Plan, und setze ihn danach selber um")
---
# P10.5 Block 14.7 — Kompakt und verteilt: aus dem Seestern wird ein Gehirn

> **Auftrag (Nikinger, 2026-10-29, nach den Bildern `p105_b14_karte_0{1,2,3}` aus 14.6.3):**
> Vorbefund Claude Code „geordnet ja, gehirn-ähnlich nein" — „ja, da bin ich bei dir. ich bin
> außerdem dafür, die Punkte etwas mehr zu verteilen." Entschieden: ein Plan, **Ausführung durch
> Claude Code** (§6), Konturglättung als **eigener** Schritt mit eigenem Tor.

## §0 Befund (gemessen bzw. am Code gelesen — nicht vermutet)

| # | Befund | Quelle |
|---|---|---|
| B1 | Die Karte ist ein Seestern: ein Lappen in der Mitte, vier an **schmalen Hälsen**, große **leere Buchten**. | Bilder 14.6.3, Vorbefund im Head (2026-10-29) |
| B2 | Ursache der Buchten ist die **Anker-Regel**: die fremden Spaces liegen auf einer Goldwinkel-Spirale im Abstand `slot·√k` — bei 5 Spaces also **1 · 1,41 · 1,73 · 2** Slots vom Zentrum. Der äußerste Space sitzt doppelt so weit weg wie der innerste. | `graph.js :: computeRegions()` Schritt 4 |
| B3 | `slot = 2·maxR + REGION_GAP` = 2·154 + 40 = **348 px** (`maxR` = 22·√32 + 30). Die Items füllen ihre Region **nicht**: die Lappen im Bild sind deutlich kleiner als die reservierten 154 px. | `computeRegions()` Schritt 3; Bilder |
| B4 | **Stabilität ist der Engpass.** In 14.4 riss **jeder** Verteilungs-Hebel einzeln die Zelle `stabilitaet` (P10.5-68: Median ≤ 2 px **und** Maximum ≤ 3 px): `ITEM_STEP` 20 → Max **205,9 px**, `ISLAND_FACTOR` 0,75 → **287,2 px**, `ANCHOR_GRAVITY` 0,01 → **7,1 px**, `REGION_GAP` 0 → **28,3 px**, 100 → **224,3 px**. | `probes/p105_b14_startwerte_messung.json` |
| B5 | Die Kontur ist aus Zellkanten verkettet (`traceContour()` → `chainEdges()` → `simplifyLoop()`); `traceSmooth()` legt nur Kurven durch die Kantenmitten. Die **8-px-Treppe** bleibt sichtbar. | `graph.js` Z. ~1699–1800 |

**Zu B4 — was am Seed gerechnet ist, und was offen bleibt.** Der **Seed** ragt nicht über die
Region: die Saat legt jedes Item in einen von **vier** Ordnern (`ordner-1`–`4`, je ~8 Items;
`p105_b14_layout_probe.py` Z. ~497), die Inseln sitzen bei 0,55·154·√(j/4) = **42–85 px** vom
Anker, die Spirale darin reicht 14·√7 ≈ **37 px** (+ 4 px Jitter) ⇒ höchstens ≈ **126 px** < 154.
Auch `ITEM_STEP` 20 bleibt mit ≈ **138 px** darunter. **Die Brüche entstehen also erst in der
Entspannung (L4)** — zwei Kandidaten, **in 14.7.0 zu entscheiden, nicht als Tatsache zu verbauen**:
(i) die Abstoßung schiebt die Knoten nach dem Seed über die Region hinaus, und sie koppeln an den
Nachbar-Space; (ii) die Entspannung ist **chaotisch** — ein kleiner Unterschied im Seed ergibt eine
andere Endlage (dann hilft kein Abstand, nur weniger Energie oder ein anderer Seed-Abstand).
**Gilt (i)**, ist der Hebel, Item-Spreizung **und** Region-Radius **gemeinsam** zu skalieren (ein
Faktor) — der Abstand zwischen den Spaces wächst dann im selben Verhältnis wie die Lappen.

## §1 Das Prinzip — drei Hebel, jeder für sich abschaltbar

1. **Verteilen (`SPREAD`):** ein Faktor auf `ITEM_STEP`, `REGION_ITEM_STEP` und `REGION_PAD`
   gemeinsam. `SPREAD = 1` ist das heutige Bild.
2. **Dicht packen (`ANCHOR_LAYOUT`):** die Anker auf einem **Hexagonalgitter**, Ring für Ring,
   statt auf der √k-Spirale. `"spirale"` ist das heutige Bild.
3. **Glätten (`LOBE_SMOOTH_PASSES`):** die Kontur vor dem Zeichnen glätten. `0` ist das heutige
   Bild.

Jeder Hebel hat einen **Nullwert, der das heutige Bild byteweise ergibt** — die Regressionsprobe
und der Gegenlauf in einem (Muster: `LOBE_CLOSE_PX = 0` in 14.6.1).

**Warum nicht einfach die Gravitation senken:** 14.4 hat es gemessen (B4: 0,01 → 7,1 px, rot).
**Warum keine feste Gehirn-Silhouette:** das wäre nicht mehr „zufällig, aber geordnet" (Block 14,
Nikinger 2026-10-26) und der größte Umbau.

## §2 Entwurf

### 2.1 Das Hexagonalgitter der Anker (nur `computeRegions()`, Schritt 4)

- Gitterpunkte: Ring 0 = der Ursprung (eigener Space), Ring *r* hat 6·*r* Plätze im Abstand
  `slot` zum Nachbarn (axiale Koordinaten, Abstand zweier Nachbarn genau `slot`).
- **Feste Platzordnung:** die Plätze werden in einer Reihenfolge vergeben, die **nur** von *r*,
  dem Platzindex und `theta0` abhängt — nie von der Zahl der Spaces. Der *k*-te Space (Reihenfolge
  wie heute: eigener zuerst, dann Hash des Namens) bekommt den *k*-ten Platz.
- **Zwei Ordnungen als Variante** (`ANCHOR_HEX_ORDER`): `"fortlaufend"` (im Ring der Reihe nach
  um `theta0`) und `"gegenueber"` (im Ring abwechselnd gegenüberliegend: 0, 3, 1, 4, 2, 5). Bei 5
  Spaces ergibt die erste eine **Niere** (C-Form — selbst eine neue Bucht), die zweite ein
  **Kreuz/Rhombus**. Welche besser aussieht, entscheiden die Bilder (E1), nicht dieser Plan.
- Der Rest von `computeRegions()` (Inseln L2, Items L3) bleibt unverändert.

**Pflichteigenschaften — als Node-Tests am exportierten `computeRegions()`** (Harness wie
`probes/p105_b14_layout_probe.mjs`):

| # | Eigenschaft | Warum |
|---|---|---|
| H1 | Ein **neuer Space** verschiebt **keinen** vorhandenen Anker (sofern `maxR` gleich bleibt) | ein gleichmäßiger Ring (2π/*m*) fiele hier durch |
| H2 | Kein Ankerpaar liegt näher als `slot` | Goldwinkel-Schritte auf **einem** Ring fielen durch (zwei Nachbarn 52,5° auseinander) |
| H3 | Die Anker hängen von den Item-Zahlen **nur über `maxR`** ab | P10.5-68: ein Item im kleineren Space bewegt keinen Anker |
| H4 | `ANCHOR_LAYOUT = "spirale"` ⇒ die Positionen sind **bitgleich** zu heute | Regressionsprobe |
| H5 | Determinismus: zwei Aufrufe ⇒ dieselben Positionen | P10.5-65 |

### 2.2 `SPREAD` (nur `computeRegions()`, Schritte 3 und 6)

```js
const SPREAD = 1;  // Plan 14.7 §2.2 — skaliert ITEM_STEP, REGION_ITEM_STEP und REGION_PAD gemeinsam; 1 = Block 14
```

Radius = `SPREAD · (REGION_ITEM_STEP·√n + REGION_PAD)`, Item-Abstand = `SPREAD · ITEM_STEP·√t`.
`ISLAND_FACTOR`, `ITEM_JITTER_PX` und die L4-Kräfte bleiben. **Nur gebaut, wenn 14.7.0 Kandidat (i)
aus §0 stützt** — sonst STOPP und Bericht (§4).

### 2.3 Die Konturglättung (nur `computeLobes()`/`chainEdges()`)

- Auf der **unvereinfachten** Schleife (jeder Punkt eine Zellecke) `LOBE_SMOOTH_PASSES` Durchläufe
  des Binomialfilters `p'ᵢ = (pᵢ₋₁ + 2pᵢ + pᵢ₊₁) / 4`, geschlossen (Index modulo Länge); danach
  `simplifyLoop()` wie heute. Gilt für äußere **und** innere Kontur.
- **Falle:** die Furche zwischen zwei Lappen ist nur 1–2 Zellen breit; jeder Lappen wird **für sich**
  geglättet. Glätten zieht konvexe Stellen nach innen, aber konkave nach **außen** — zwei Konturen
  könnten sich berühren. Darum die Zelle `kontur_abstand` (§5).
- `traceContour()` (Rasterrand = draußen) bleibt; Wächter `tests/test_lobe_kontur_geschlossen.py`
  bleibt grün.

### 2.4 Was bleibt — nicht anfassen

`LOBE_REACH`, `LOBE_CELL_PX`, `LOBE_INNER_CELLS`, `FIT_MARGIN` (= 56), die L4-Kräfte
(`ANCHOR_GRAVITY`, `CROSS_SPRING_*`, `ALPHA_START_SEEDED`, `REPULSION_STRENGTH`), `fitView()`,
Beschriftungen, Farben, Bahnen, Server-Code, `app.css`. `LOBE_CLOSE_PX` (= 160) bleibt **außer**
die Varianten zeigen, dass es bei sich berührenden Lappen überfüllt (dann Teil von E1, gemessen).

### 2.5 Kosten und Rand

- Kompaktere Anker ⇒ kleinere Welt ⇒ kleineres Raster; Glätten ⇒ mehr Konturpunkte. Gemessen
  wird `computeLobes()` bei **152** und **201** Knoten (Messpflaster der Bilder-Probe), Grenze
  **50 ms** bei 201 (wie 14.6).
- Reach ≤ **52 px**, Luft > 0 (Block-14-Plan §2.5) — **> 52 px oder Luft ≤ 0 ⇒ STOPP**, nicht
  `FIT_MARGIN` ändern.

## §3 Entscheidungen des Nikingers

**E1 — Anordnung und Spreizung** (nach 14.7.2, mit Bildern je Variante). Vorher fällt jede Variante
heraus, deren `stabilitaet` rot ist — ihre Bilder werden gar nicht erst vorgelegt.
**Standardregel, wenn delegiert:** unter den Varianten mit **allen** alten Zellen grün (65–69, 71,
72) die mit der höchsten **Solidität** (§5); bei Gleichstand (± 0,02) die mit dem größeren
**Nachbarabstand**.

**E2 — Glättung** (nach 14.7.4). **Standardregel:** der kleinste Wert, bei dem die **Welligkeit**
≤ 50 % der Basislinie ist und `kontur_abstand` > 0 bleibt.

**Kein Lockern der Grenzen durch Claude Code.** Hält keine Variante die Stabilität (Median ≤ 2 px,
Max ≤ 3 px), ist das ein **Bericht** an den Nikinger — eine gelockerte Schwelle ist seine
Entscheidung und steht hier bewusst **nicht** als Option.

## §4 Schritte (je Schritt ein Commit, Head im selben Commit)

| Schritt | Inhalt | Fertig, wenn |
|---|---|---|
| **14.7.0** 🔄 **STOPP (b) 2026-10-29** | **Messung zuerst.** (a) Bilder-Probe: neue Zellen `fuelle`, `verteilung`, `kontur_welligkeit`, `kontur_abstand`, `kanten_aussen` (§5) — über das Messpflaster, **kein** Haken im Produktcode. (b) **Ursache von B4:** an `step20` und `insel0.75` (14.4) messen, **welche** Knoten sich bei der Stabilitätsprobe bewegen, wie weit sie **nach der Entspannung** von ihrem Anker liegen (relativ zu `radius`) und ob sie nahe am Nachbar-Space sitzen — Kandidat (i) — oder mitten im eigenen Lappen umspringen — Kandidat (ii). (c) Abnahmezeilen **P10.5-73/74** in den Head (⬜). | Basislinie steht als Zahl im Beleg; (i) oder (ii) aus §0 ist **mit Zahlen** gestützt. Nur (ii) ⇒ **STOPP**, Bericht — `SPREAD` allein löst es dann nicht. |
| **14.7.1** | Die Hebel `ANCHOR_LAYOUT`/`ANCHOR_HEX_ORDER` (§2.1) und `SPREAD` (§2.2) bauen, **Defaults = heute**. Node-Tests H1–H5. | Layout-Probe mit Defaults: **alle** Knotenpositionen gleich zu `p105_b14_layout_probe.json`; Bilder **byteweise** gleich zu denen im Repo. H1–H5 grün. |
| **14.7.2** | **Das Raster:** `ANCHOR_LAYOUT` {`spirale`, `hex`/`fortlaufend`, `hex`/`gegenueber`} × `SPREAD` {1 · 1,25 · 1,5} = 9 Läufe (Treiber nach dem Muster `p105_b14_startwerte.py`), je Lauf **alle** Layout-Zellen + `koerper` + die neuen Zellen + Reach/Luft + `computeLobes()`-Zeit; Bilder nach `~/p105_b14_7_varianten/<label>/` (**außerhalb** des Repos). | Tabelle; Stabilität zuerst gefiltert. **STOPP — E1.** |
| **14.7.3** | Den gewählten Wert setzen (Kommentar „gewählt vom Nikinger am <Datum>, gemessen in 14.7.2"). Wächter: Gegenläufe `anker` (`ANCHOR_LAYOUT` → `spirale`) und `spreizung` (`SPREAD` → 1) machen **genau** `fuelle` bzw. `verteilung` rot. **Die sechs Layout-Gegenläufe neu** (die Knoten haben sich bewegt — anders als in 14.6). | Alle Zellen 65–69, 71, 72 grün mit neuen Zahlen; jeder Gegenlauf rot an genau seiner Zelle. |
| **14.7.4** | **Glätten** (§2.3, eigenes Tor): `LOBE_SMOOTH_PASSES` {0 · 2 · 4 · 6}, Default 0 = heute. Varianten-Bilder außerhalb des Repos. **STOPP — E2.** Danach Wert setzen + Gegenlauf `glatt` (→ 0 macht `kontur_welligkeit` rot). | `kontur_abstand` > 0, Reach ≤ 52, Zeit ≤ 50 ms; `test_lobe_kontur_geschlossen.py` grün. |
| **14.7.5** | Belege neu: Layout-Probe, Bilder-Probe (Bilder ersetzen `docs/screenshots/p105_b14_karte_0{1,2,3}_*.png`), Karten-Probe `p105_b8_karte_probe.py`, C2-Probe, volle Suite, `doc_health`, `ui_budget`. Abnahme P10.5-73/74. Update-Log-Zeile (Z. 19) nachziehen, wenn sich die Aussage ändert. Deploy-Tabelle: D enthält 14.7. | Alles grün; **P10.5-70 neu beim Nikinger** (Sichtung der neuen Bilder). |

## §5 Abnahme — neue Zeilen P10.5-73 und P10.5-74

Bei 5 Spaces (30/32/30/30/30 = 152 Items, Saat der Abnahme):

**P10.5-73 — die Karte ist kompakt, die Punkte sind verteilt.**
- **Solidität** (`fuelle`) = Körperzellen ÷ Zellen der konvexen Hülle des Körpers ≥ **S**.
  S ist ein **Startwert 0,75**, bestätigt oder geändert bei E1, **nachdem** 14.7.0 die Basislinie
  gemessen hat.
- **Verteilung** (`verteilung`) = Median des Nächster-Nachbar-Abstands **innerhalb** eines Space
  ≥ **1,25 × Basislinie** (14.7.0).
- **Alle** alten Zellen grün: 65 (Determinismus), 66 (Regionen), 67 (Kamera), 68 (Stabilität),
  69 (Budget), 71 (Beschriftungen), 72 (Körper); Reach ≤ 52 px, Luft > 0; `computeLobes()` ≤ 50 ms
  bei 201 Knoten.
- Gegenläufe `anker` und `spreizung` machen **genau** ihre Zelle rot.

**P10.5-74 — die Kontur ist glatt.**
- **Welligkeit** (`kontur_welligkeit`) = Vorzeichenwechsel der Krümmung je 100 px gezeichneter
  Kontur ≤ **50 %** der Basislinie. (**Nicht** „Anteil achsenparalleler Segmente": der ist heute
  per Konstruktion 100 % und nach jedem Glätten ≈ 0 — er unterscheidet gutes von schlechtem
  Glätten nicht.)
- **`kontur_abstand`** = kleinster Abstand zweier Konturen **verschiedener** Lappen > 0 px.
- Gegenlauf `glatt` macht **genau** `kontur_welligkeit` rot.

**Nur berichtet, kein Tor:** `kanten_aussen` — Anteil der Bahnlänge zwischen zwei Spaces, die
außerhalb des Körpers verläuft (Vorbefund: viele lange Kanten laufen durch die Buchten).

**P10.5-70** (Sichtung) bleibt ⬜ und wird an den **neuen** Bildern entschieden. Summe im Head danach
**74 Zeilen**; `tests/test_head_rules.py` prüft sie gegen Head und `ABNAHME_ARCHIVE.md`.

## §6 Ausführung — Claude Code (datierte Nikinger-Entscheidung 2026-10-29)

**Abweichung von der P10.5-Konvention** (Ausführer = opencode/M3.1 Flash, Memory „Execution moves
to opencode"): der Nikinger hat am 2026-10-29 entschieden, dass Claude Code 14.7 **selbst**
umsetzt. **Begründung:** der Kern ist eine Schleife aus Varianten und **Bildurteil**, und genau
das Bildurteil ist am 14.6-Bericht gescheitert („gehirn-ähnlich" bei einem Seestern, alle Zellen
grün). Wer die Varianten erzeugt, sieht sie auch kritisch an, bevor sie beim Nikinger landen.

**Erlaubte Pfade:** `phase5_ui/webui/static/js/graph.js` (**nur** `computeRegions()`,
`computeLobes()`/`chainEdges()` und die drei neuen Konstanten) · `phase10_5_finishing/probes/**` ·
`phase10_5_finishing/tests/**` · `docs/screenshots/p105_b14_karte_0{1,2,3}_*.png` (14.7.5) · Doku:
dieser Plan, Phase-Head, `SESSIONS_ARCHIVE.md` (nur über das Skript), `docs/INDEX.md`,
`docs/UPDATE_LOG.md` (14.7.5).

**Regeln** (wie 14.6 §6): Proben **nur** an der Wegwerf-Instanz (eigener Port, tmp-`DATA_ROOT`,
tmp-`auth.sqlite3`, Playwright aus `~/.claude-code-tools/e2e-venv`) · Stopp **nur** über die
PID-Datei, **nie** `pkill -f`, **nie** `systemctl` (Hard Rule 9) · Umgebung ohne
`SHAREFYX_*`/`SFX_*` · ein Commit je Schritt, Head im selben Commit, volle Suite grün davor ·
Session-Block **ans Ende** des Heads, dann `scripts/rotate_session_block.sh phase10_5_finishing` ·
INDEX-Reserve 3.000 B (`test_register_archive.py`).

**STOPP-Punkte:** nur Kandidat (ii) gestützt (14.7.0) · E1 (14.7.2) · E2 (14.7.4) · keine Variante hält
die Stabilität · Reach > 52 px oder Luft ≤ 0 · `computeLobes()` > 50 ms bei 201 Knoten ·
`kontur_abstand` ≤ 0 bei jedem Glättungswert.

## Anmerkungen 14.7.0 — (b) die Ursache von B4 (2026-10-29, Claude Code)

**Ergebnis: Kandidat (ii).** Die Lappen **wandern nicht** — sie sortieren sich **innen** um.
Beleg `phase10_5_finishing/probes/p105_b14_7_ursache_b4.json` (Skript daneben), aus drei Läufen
der Layout-Probe an Wegwerf-Instanzen (einzeln — parallel kollidieren die Läufe im gemeinsamen
Wegwerf-Ordner `/tmp/opencode/sharefyx-wegwerf-b14/`, alle drei scheiterten mit Timeout).

| Lauf | Median / Max (px) | Knoten > 3 px | Schwerpunkt-Verschiebung je Space (px) | Rest-Median je Space (px) | Radius je Space (px) |
|---|---|---|---|---|---|
| Basislinie | 0,0 / 2,2 | 0 von 122 | 0,1–0,2 (epsilon 4,7) | 0,1–0,9 | 100–119 |
| `ITEM_STEP` 20 | 16,2 / 205,9 | 110 | 1,0–6,2 | 6,6–**67,2** (gamma) | 100–123 |
| `ISLAND_FACTOR` 0,75 | 72,7 / 287,2 | 120 | 2,6–3,7 | 9,9–**121,4** (gamma) | 109–138 |

- Die größten Springer sitzen **20–105 px** vom eigenen Schwerpunkt und **330–550 px** vom
  nächsten fremden Knoten — keine Berührung zweier Spaces. ⇒ **(i) ist widerlegt.**
- Ein Knoten springt bis **2×** den Lappenradius: der Lappen spiegelt/dreht sich **in sich**, ausgelöst
  von einem Item im **400 px entfernten** Space `epsilon` — das ist Chaos (ii).
- **Zweiter Befund:** der Radius der Lappen nach der Entspannung ist **fast gleich**, ob `ITEM_STEP`
  14 oder 20 (100–119 gegen 100–123 px). **Die Dichte bestimmt das Gleichgewicht der Kräfte**
  (Abstoßung gegen Anker-Gravitation und Federn), **nicht** der Seed. Ein größerer Seed verteilt
  die Punkte also gar nicht — er legt sie nur **weiter vom Gleichgewicht** weg, die Entspannung
  hat mehr zu tun und landet in einem anderen Minimum.

**Folge für den Plan:** `SPREAD` in der Form von §2.2 (nur Seed-Abstände) ist **wirkungslos und
instabil** — gebaut wird er nicht (§4, STOPP). Der Hebel für „mehr verteilt" ist das
**Gleichgewicht**; ein Vorschlag liegt beim Nikinger (Session-Block im Head). `ANCHOR_LAYOUT` und
die Glättung sind von diesem Befund **nicht** berührt.
