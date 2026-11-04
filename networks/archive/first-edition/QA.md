# Final production verification

Verified on 2026-11-03. Built with ManimGX 0.1.1 and FFmpeg.

## Delivered media

| Episode | Continuous duration | Sections / clips | Narration words |
|---|---:|---:|---:|
| 01 — What Happens When You Open a Website? | 8:45 | 24 / 24 | 1226 |
| 02 — Thousands of Messages, One Cable | 8:45 | 24 / 24 | 1223 |
| 03 — Delivering Data When Packets Get Lost | 9:05 | 24 / 24 | 1270 |
| 04 — When Computers Talk at Once | 9:05 | 24 / 24 | 1267 |
| 05 — How Routers Find the Best Path | 8:30 | 24 / 24 | 1180 |
| 06 — Subnetting You Can Actually See | 8:20 | 24 / 24 | 1156 |
| 07 — TCP vs UDP: The Cost of Reliability | 8:50 | 24 / 24 | 1234 |
| 08 — Sending Secrets Without Sharing a Secret First | 8:50 | 24 / 24 | 1233 |

All eight continuous videos and all 192 clips are H.264, 1920×1080, constant 30 fps. Each complete video is between five and ten minutes. Combined runtime is approximately 70 minutes 10 seconds.

## Checks completed

- Content and timing: 8 complete scripts, 192 uniquely identified sections, 9,789 narration words, approximately 140 words per minute, valid guide captions and chapter markers.
- Numerical examples: independent Python checks of all four /26 subnet ranges and host counts, Dijkstra distances, and the changed route after a link failure.
- Layout: ManimGX inspection reports no problems in 24 completed-diagram samples per episode. Independent visual review covers all 192 sampled diagrams, with original-size checks of numerical and protocol examples. See [visual-review.md](visual-review.md).
- Media: FFprobe verified full-video resolution, codec, constant frame rate and duration; all 192 clips have the expected exact frame counts and durations. ManimGX static holds were normalized to constant-rate video before cutting.
- Clip alignment: independently decoded and compared first/middle/last clip images against the corresponding continuous-video positions for all eight lessons. All 24 image comparisons passed.
- Browser: all eight actual local-file presentations passed headless Chromium tests for loading paused, Next blocked during animation, pause/resume, automatic hold after visual motion, indefinite frozen final frame, Previous, Replay, section selection, fullscreen, captions, presenter notes, and the final-section state.
- Offline operation: tests observed no HTTP/HTTPS requests and no JavaScript errors. The browser tests used a separate headless process, not the user’s browser session.
- Original project: existing solar-system source and MP4 preserved.

## Evidence

- [Browser results](browser-verification.json)
- [Decoded clip comparisons](clip-alignment-verification.json)
- Each episode’s `media-verification.json`, `inspect.log`, references and content-review report.

## Review limits

Review used automated checks and sampled rendered frames; it did not consist of watching every frame of all 70 minutes. No voiceover is included, as requested. Guide subtitle timings are provisional until aligned with your recording. YouTube publishing is not performed.

## Re-run checks

```sh
python3 networks/tests/content_check.py
python3 networks/tests/clip_alignment_check.py
uv run --with playwright python networks/tests/player_check.py
```
