# Drittanbieter-Lizenzen

Self-gehostete Bibliotheken und Asset-Sammlungen, die unter `phase5_ui/` eingebunden sind.
Jede Quelle steht in einem eigenen Verzeichnis unter `phase5_ui/vendor/`, die Lizenztexte
liegen jeweils daneben (`LICENSE` oder `OFL.txt`).

## Lucide Icons

- **Quelle:** https://github.com/lucide-icons/lucide, Release-Tag `1.38.0` (2026-08-31)
- **Pfad:** `phase5_ui/vendor/lucide/` (Icons unter `icons/*.svg`, Lizenz in `LICENSE`)
- **Verwendung:** Vendored Inline-SVG-Sprite zwischen `<!-- ICONS:BEGIN -->` /
  `<!-- ICONS:END -->` in `phase5_ui/webui/static/app.html`, generiert durch
  `phase5_ui/scripts/build_icon_sprite.py`
- **Lizenz:** ISC-Lizenz fuer neue Icons; MIT-Lizenz (Cole Bemis, 2013-) als Erbe des
  Feather-Projekts fuer die Icons, die Lucide aus Feather uebernommen hat -- konkret in
  unserem Subset: `chevron-down`, `chevron-right`, `info`, `link`, `log-out`, `plus`,
  `search`, `x`. Volltext im vendored `LICENSE`.

## IBM Plex Sans + Mono

- **Quelle:** https://github.com/IBM/plex, Release `@ibm/plex-sans-variable@0.2.0` (Sans,
  variabel) und `@ibm/plex-mono@2.5.0` (Mono, statisch)
- **Pfad:** `phase5_ui/webui/static/fonts/` (gehashte WOFF2-Subsets, Lizenz in `OFL.txt`)
- **Verwendung:** `@font-face`-Bloecke in `phase5_ui/webui/static/app.css`, gebaut durch
  `phase5_ui/scripts/build_font_subset_plex.sh`
- **Lizenz:** SIL Open Font License 1.1 (OFL-1.1). Volltext im vendored `OFL.txt`.
  OFL-1.1 erlaubt Selbst-Hosting, Einbettung und kommerzielle Nutzung; Bedingung ist nur,
  dass der Lizenztext mit der Schrift mitgeliefert wird.