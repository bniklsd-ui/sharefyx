# Lucide Icons (vendored subset)

Icons unter `icons/*.svg` stammen aus dem Lucide-Projekt
(https://github.com/lucide-icons/lucide), gepinnt auf den Release-Tag **`1.38.0`**
(2026-08-31). Quelle: `https://github.com/lucide-icons/lucide/archive/refs/tags/1.38.0.tar.gz`,
SHA-256 `d28944cfc633fbf1d4cb81ed290c000c5e2e4eda8edebb402f2b607705911c02`.

Lizenz: ISC (`LICENSE`, oberer Teil) plus MIT fuer die Icons, die historisch aus dem
Feather-Projekt (Cole Bemis, 2013-) uebernommen wurden -- das sind in unserem Subset:
`chevron-down`, `chevron-right`, `info`, `link`, `log-out`, `plus`, `search`, `x`
(siehe Feather-Liste im `LICENSE`-Anhang).

## Subset (18 Icons)

Aktuell vendored, alphabetisch:

| Name | Verwendung |
|---|---|
| `chevron-down` | Baum-Twist offen (`tree.js`, ersetzt `▾`) |
| `chevron-right` | Baum-Twist zu (`tree.js`, ersetzt `▸`) |
| `folder` | Uebersicht/Graph (D-Block, geplant) |
| `folder-input` | Verschieben-Knopf in der Liste (`list.js`, ersetzt `→`) |
| `house` | Rail-Uebersicht (`app.html`, ersetzt `&#8962;`) |
| `image` | Editor-Toolbar Bild einfuegen (`app.html`, ersetzt `&#128444;`) |
| `info` | Info-Hinweise in Dialogen (geplant) |
| `link` | Editor-Toolbar Link einfuegen (`app.html`, ersetzt `&#128279;`) |
| `log-out` | Rail-Abmelden (`app.html`, ersetzt `&#9099;`) |
| `plus` | Rail-Anlegen + Liste (`app.html`, ersetzt `&#43;`) |
| `quote` | Editor-Toolbar Zitat (`app.html`, ersetzt `&#8221;`) |
| `refresh-cw` | Uebersicht-Refresh (D-Block, geplant) |
| `search` | Link-Picker-Knopf (`app.html`, bereits B4-verwendet) |
| `settings` | Rail-Konto (`app.html`, ersetzt `&#9881;`) |
| `share-2` | Freigeben-Knopf in der Liste (`list.js`, ersetzt `⇄`) |
| `triangle-alert` | Warn-Hinweise in Dialogen (geplant) |
| `waypoints` | Uebersicht/Graph (D-Block, geplant) |
| `x` | Schliessen-Buttons + Chip-X (`app.html`, `list.js`, ersetzt `&times;`/`×`) |

## Update

```sh
# 1. Neue Version pinnen (Phase-Head-Session-Block dokumentiert das Ergebnis)
NEW=1.39.0
curl -sL "https://github.com/lucide-icons/lucide/archive/refs/tags/${NEW}.tar.gz" -o /tmp/lucide.tgz
sha256sum /tmp/lucide.tgz  # ins README uebernehmen + Phase-Head

# 2. Nur die gebrauchten Icons kopieren
ICON_NAMES="chevron-down chevron-right folder folder-input house image info link log-out \
            plus refresh-cw search settings share-2 triangle-alert waypoints x"
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

Alle 18 Icon-Namen aus dem Subset sind in Lucide 1.38.0 vorhanden (geprueft am 2026-09-01
gegen `https://raw.githubusercontent.com/lucide-icons/lucide/1.38.0/icons/<name>.svg`).
Lucide-Namen driften zwischen Releases (Renames, Deprecations) -- vor jedem Update die
Subset-Liste gegen die neue Version verifizieren und fehlende Namen hier dokumentieren,
bevor `build_icon_sprite.py` einen `MISSING`-Lauf produziert.