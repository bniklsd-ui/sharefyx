# Lucide Icons (vendored subset)

Icons unter `icons/*.svg` stammen aus dem Lucide-Projekt
(https://github.com/lucide-icons/lucide), gepinnt auf den Release-Tag **`1.38.0`**
(2026-08-31). Quelle: `https://github.com/lucide-icons/lucide/archive/refs/tags/1.38.0.tar.gz`,
SHA-256 `d28944cfc633fbf1d4cb81ed290c000c5e2e4eda8edebb402f2b607705911c02`.

Lizenz: ISC (`LICENSE`, oberer Teil) plus MIT fuer die Icons, die historisch aus dem
Feather-Projekt (Cole Bemis, 2013-) uebernommen wurden -- das sind in unserem Subset:
`chevron-down`, `chevron-left`, `chevron-right`, `code`, `info`, `link`, `log-out`,
`minus`, `plus`, `search`, `x` (siehe Feather-Liste im `LICENSE`-Anhang).

## Subset (25 Icons)

Aktuell vendored, alphabetisch:

| Name | Verwendung |
|---|---|
| `chevron-down` | Baum-Twist offen (`tree.js`, ersetzt `▾`) |
| `chevron-left` | Zurueck-Knopf im Editor und in der Liste (`app.html`) —
  **[2026-10-25]** nachgetragen: das Symbol stand im Sprite, die Quelldatei war nie
  vendored (siehe unten) |
| `chevron-right` | Baum-Twist zu (`tree.js`, ersetzt `▸`) |
| `code` | Editor-Toolbar Code (`app.html`, ersetzt `</>`) — P10.5 Block 13.2 |
| `folder` | Uebersicht/Graph (D-Block, geplant) |
| `folder-input` | Verschieben-Knopf in der Liste (`list.js`, ersetzt `→`) |
| `heading` | Editor-Toolbar Ueberschrift (`app.html`, ersetzt `H`) — P10.5 Block 13.2 |
| `house` | Rail-Uebersicht (`app.html`, ersetzt `&#8962;`) |
| `image` | Editor-Toolbar Bild einfuegen (`app.html`, ersetzt `&#128444;`) |
| `info` | Info-Hinweise in Dialogen (geplant) |
| `link` | Editor-Toolbar Link einfuegen (`app.html`, ersetzt `&#128279;`) |
| `list` | Editor-Toolbar Liste (`app.html`, ersetzt `•`) — P10.5 Block 13.2 |
| `list-ordered` | Editor-Toolbar Nummerierung (`app.html`, ersetzt `1.`) — P10.5 Block 13.2 |
| `log-out` | Rail-Abmelden (`app.html`, ersetzt `&#9099;`) |
| `minus` | Editor-Toolbar Trennlinie (`app.html`, ersetzt `—`) — P10.5 Block 13.2 |
| `plus` | Rail-Anlegen + Liste (`app.html`, ersetzt `&#43;`) |
| `quote` | Editor-Toolbar Zitat (`app.html`, ersetzt `&#8221;`) |
| `refresh-cw` | Uebersicht-Refresh (D-Block, geplant) |
| `search` | Link-Picker-Knopf (`app.html`, bereits B4-verwendet) |
| `settings` | Rail-Konto (`app.html`, ersetzt `&#9881;`) |
| `share-2` | Freigeben-Knopf in der Liste (`list.js`, ersetzt `⇄`) |
| `trash-2` | Mülleimer-Knopf (Archivieren/Ablehnen) (`app.html`) |
| `triangle-alert` | Warn-Hinweise in Dialogen (geplant) |
| `waypoints` | Uebersicht/Graph (D-Block, geplant) |
| `x` | Schliessen-Buttons + Chip-X (`app.html`, `list.js`, ersetzt `&times;`/`×`) |

**[2026-10-25, P10.5 Block 13.2]** Die fuenf Icons `code`, `heading`, `list`, `list-ordered`,
`minus` kamen mit der **Knopfleiste nach Word** dazu: die Werkzeugleiste trug bis dahin die
HTML-Entity-Zeichen `</>`, `•` und `—` — die Verbotsliste (§0.3 Punkt 1 der Phase 8: „keine
Emoji und keine HTML-Entity-Zeichen als Icons — nur das Lucide-Sprite") war damit verletzt.
**Pin-Nachweis:** nicht nur gegen die Roh-URL geprueft, sondern aus dem **Tarball desselben
Release-Tags** entpackt, dessen SHA-256 oben eingetragen ist (`d28944cfc6…`) — damit ist
belegt, dass die Dateien aus genau dieser Version stammen.

## Update

```sh
# 1. Neue Version pinnen (Phase-Head-Session-Block dokumentiert das Ergebnis)
NEW=1.39.0
curl -sL "https://github.com/lucide-icons/lucide/archive/refs/tags/${NEW}.tar.gz" -o /tmp/lucide.tgz
sha256sum /tmp/lucide.tgz  # ins README uebernehmen + Phase-Head

# 2. Nur die gebrauchten Icons kopieren
ICON_NAMES="chevron-down chevron-left chevron-right code folder folder-input heading house image info link \
            list list-ordered log-out minus plus quote refresh-cw search settings share-2 \
            triangle-alert trash-2 waypoints x"
mkdir -p /tmp/lucide-extract && tar -xzf /tmp/lucide.tgz -C /tmp/lucide-extract "lucide-${NEW}/icons"
for n in $ICON_NAMES; do
  cp "/tmp/lucide-extract/lucide-${NEW}/icons/${n}.svg" "phase5_ui/vendor/lucide/icons/${n}.svg"
done
cp "/tmp/lucide-extract/lucide-${NEW}/LICENSE" phase5_ui/vendor/lucide/LICENSE

# 3. Sprite neu generieren + pruefen
python phase5_ui/scripts/build_icon_sprite.py
python phase5_ui/scripts/build_icon_sprite.py --check   # idempotent?
```

## V92 (Pin-Nachweis)

Alle 25 Icon-Namen aus dem Subset sind in Lucide 1.38.0 vorhanden (geprueft am 2026-09-01
gegen `https://raw.githubusercontent.com/lucide-icons/lucide/1.38.0/icons/<name>.svg`;
die fuenf neuen am 2026-10-25 aus dem Tarball desselben Tags, SHA-256 wie oben; das
nachgetragene `chevron-left` am selben Tag aus demselben Tarball,
SHA-256 `83b0681aa38bf55e9d52a1e4b4cced624abe1fe7678ecafda133a574f1161d93`).
  **Alle 25 vendored Dateien wurden am 2026-10-25 byteweise gegen den Tarball geprueft**
  (`cmp` je Datei: keine Unterschiede) — der Bestand ist damit belegt, nicht behauptet.
Lucide-Namen driften zwischen Releases (Renames, Deprecations) -- vor jedem Update die
Subset-Liste gegen die neue Version verifizieren und fehlende Namen hier dokumentieren,
bevor `build_icon_sprite.py` einen `MISSING`-Lauf produziert.
**[2026-10-25, P10.5 Block 13.2 — der Fund beim Sprite-Neubauen]** `chevron-left` stand im
Sprite (`i-chevron-left`, vier Verweise in `app.html`: die Zurueck-Knoepfe), **die Quelldatei
war aber nie vendored** — `git log -- phase5_ui/vendor/lucide/icons/chevron-left.svg` ist leer.
Das Sprite war damit **nicht aus dem Vendor-Bestand reproduzierbar**; es war von Hand
gepflegt. Der Beweis kam **erst beim Neubauen**: `build_icon_sprite.py` liess `i-chevron-left`
weg, und der Phase-9-Waechter `test_the_menu_label_is_centered_and_the_icon_button_is_named`
wurde rot („kein i-chevron-left im Sprite"). Ab jetzt ist die Datei vendored (24 Icons) und
der Sprite **wieder aus dem Bestand erzeugbar** — `build_icon_sprite.py --check` ist die
Gegenprobe: sie schlaegt fehl, sobald jemand am Sprite von Hand pfuscht.
