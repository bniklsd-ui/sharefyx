# screenshots_latest/ — Schnellzugriff auf die jüngsten Screenshots

**Stand: 2026-09-14, Phase 8.6 Block G-R.**

| Datei | Was ist zu sehen | Checkkriterium |
|---|---|---|
| `p86_block_g_r_01_1440_uebersicht.png` | 1440-Übersicht (Spaces + Zuletzt benutzt) mit Verknüpfungs-Karte rechts | Layer-Tone vereinheitlicht: kein schwarzer Ring rund um die Karte mehr (Befund 1-Fortsetzung) |
| `p86_block_g_r_02_1440_editor_offen.png` | 1440-Editor offen, Liste zeigt selektiertes Item | `.editor__head` sticky mit `--surface-raised`-Hintergrund, YAML-Kopfzeile bündig zur Suchzeile im Listen-Slot |
| `p86_block_g_r_03_1200_uebersicht.png` | 1200-Übersicht | Rail 240 px mit Labels sichtbar (kein Kollaps), Liste 380, Karte ~620 |
| `p86_block_g_r_04_1200_editor_offen.png` | 1200-Editor offen | sticky-Header-Logik bei mittlerer Breite konsistent |
| `p86_block_g_r_05_1024_uebersicht.png` | 1024-Übersicht | Rail 240, Liste oben, Karte darunter GESTAPELT — nicht weg (Block-G-Variante blendete die Karte aus) |
| `p86_block_g_r_06_1024_editor_offen.png` | 1024-Editor offen | Editor ersetzt die Karte im unteren Slot, gestapelter Modus funktioniert |

**Symlinks auf die Originale in `../screenshots/p86_block_g_r_*.png`.** Bei Block-Wechsel: alte Symlinks weg, neue anlegen, README ersetzen, `updated:`-Frontmatter ergänzen — alles im selben Commit wie die Block-Doku-Updates (Konvention **P8.6-AK**).
