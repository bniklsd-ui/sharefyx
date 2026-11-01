---
status: live
purpose: reusable recipe + lessons from the v4.0.0 launch film (Block 16, two rounds, accepted 2026-11-01) — how to build a code-generated, deterministic product film again, and what the Nikinger liked and disliked
read-when: before planning any new launch/intro film, product video or animated sequence for Sharefyx (or another project) — start here, then the Block-16 plan for details
detail: L2
up: ../INDEX.md
down:
  - ./phase10_5_launch_film_plan.md   # the full plan, answers Q1–Q7, notes 16.0–16.9 (numbers, gags, Gegenläufe)
updated: 2026-11-01 (first version, after Sichtung 2: "really great, i like the style")
---

# Launch film — what worked, what didn't (Block 16, 2026-10-31 → 2026-11-01)

> **Result:** `~/sharefyx-film/sharefyx-4.0.0-r2.mp4` — 48,4 s, 1080p60, H.264 + AAC, built in two
> rounds over one weekend, accepted at Sichtung 2 („Nice, that is really great, i like the style“).
> Source: `phase10_5_finishing/film/` (stage, capture, sound, render), guards in
> `phase10_5_finishing/tests/test_film_stage.py`.

## 1. The style the Nikinger accepted (keep it)

| Element | What it is | Why it worked |
|---|---|---|
| **Big-bang opening** | spark → flash → dots burst out → gather into the **whole** brand mark (icon + name + version) mid-screen → version digits roll old → new → mark lands in the UI rail | an event, not a zoom; nothing cut off |
| **Dot language as bookends** | the same dots open the film (form the logo) and close it (form „4.0.0“, then real type) | one visual idea carries the whole film |
| **One continuous camera** | all scenes are tiles on one plane laid out along the strokes of a „4“; the camera flies tile to tile, zooms out, tiles snap into the 4 | the version is *in* the structure, revealed at the end |
| **Quiet blue grid** | lines in the button blue `#3E8DF3`, alpha 0.14, parallax 0.5, constant density (LOD crossfade), wave on the bang, vignette | black looked „unfinished“ — the grid fixed it without noise |
| **Tiles in space** | tile ≈ 60 % width on one side, slight 3D tilt toward the text (rotateY 13° → 6°, rotateX 5° → 2°, drifting), 6 % push-in during the hold | killed the „static slideshow“ feel |
| **Text on the free side** | title + one line per scene, word by word with a short glow, appearing **with the light streak** that sweeps every tile | the streak (old UI → new) + text was the Nikinger's own suggestion — a hit |
| **Focus push** | search scenes zoom onto the hits/result list (≤ 2× of a 2× capture) | „some scenes don't get the effect across“ — now they do |
| **Neighbours in shadow** | inactive tiles darken to 35 % during a hold, bright again while travelling | eye stays on the scene; text side stays clean |
| **Pace** | ≈ 48 s; travels 45 frames, holds 95–150 (terminal 200) | shorter holds make the text unreadable |

**Disliked in round 1 (avoid):** zooming out of tiny UI text as the opening (read as a rendering
bug), plain black background, full-frame screenshots with only camera moves (slideshow), subtitles
at the bottom instead of designed text.

## 2. The recipe (reproducible = every frame is a pure function of its number)

1. **Stage** = HTML page + pure `zustand(n, geo)` in an ES module (no clock, no rAF, no transitions,
   no network). `geo` = sizes measured once at load (glyph ink, target points). Pure ⇒ Node guards.
2. **Real UI** comes as **stills from a throwaway instance** (Playwright, 2× capture, invented seed
   data); typing = a still per character. AI scene = a real MCP run recorded to JSON, replayed as a
   terminal tile.
3. **Render** = Playwright Chromium, per frame `renderFrame(n)` then CDP `Page.captureScreenshot`
   with `clip.scale = 2` (a context `device_scale_factor` alone still returns 1×) → PNG via
   `image2pipe` into ffmpeg (`imageio-ffmpeg` static binary has `libx264`) → `lanczos` to 1080p,
   CRF 17, `yuv420p`, `+faststart`. No frame files on disk. Grain overlay against 8-bit banding.
4. **Sound** in code (numpy, fixed seed): pad chord, chime per camera arrival, swell, glitter in the
   morph, boom on the bang; marks read **from the stage module via Node** — one source for picture
   and sound. Muxed as AAC.
5. **Timeline is relative** (`FAHRT`: hold + travel per tile, events counted from the hold) —
   change durations, never absolute frames. A refactor is proven neutral by diffing `zustand(n)`
   for **every** frame against the old file.

## 3. Lessons that cost time (check these first next time)

- **Judge on the decoded MP4, not the PNG.** `yuv420p` halves chroma: grid lines at alpha 0.075
  arrived at 8–12/255 (invisible); opacity-dimmed tiles let the grid shine through (only seen
  decoded) ⇒ dim with a black overlay *inside* the tile, keep it opaque.
- **Center on ink, not on the box.** The UI's brand box is wider than its ink — measure the ink.
- **Font subsets fail silently.** A missing glyph falls back to a system font. Guard every film
  text against the subset cmap (fontTools; here via the film venv). `ä` is in the Mono subset,
  `→` is in neither.
- **`perspective()` per tile**, not on the camera-scaled world. 3D under `clip.scale = 2` stays sharp.
- **Push-in ceiling** = source density: 2× stills ⇒ zoom × push ≤ 2.
- **Stale sound is trimmed silently** (`-shortest`): regenerate the WAV before every full render
  and compare audio vs. video duration afterwards. Keep the loudest event (boom) from dominating
  normalisation.
- **Long renders:** full dpr-2 run 23–50 min (0,47 s/frame here, VM load varies) — Bash timeout
  7 200 000 ms + shell `timeout`; 1× preview ≈ 8 min. Render timings on this VM are noisy; compare
  only same-run numbers.
- **Privacy pass again after any zoom change** — a push-in makes small UI text legible for the
  first time (names, dates, meta).
- **Review loop:** key stills before any full run → 1× preview → contact sheets every 1,5 s
  (`ffmpeg fps=1/1.5` + PIL grid, viewed via `Read`) → fix → dpr-2 full run → contact sheets of the
  final file. The Nikinger reviews the **whole** film, once per round.
- **Each guard gets a Gegenlauf** (break it on purpose, only that guard turns red).
