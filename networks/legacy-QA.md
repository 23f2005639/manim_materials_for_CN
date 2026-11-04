# Visual edition — final verification

The eight lessons were rebuilt around full-frame, persistent animated diagrams. Bullet sidebars, decorative panels and long narration holds were removed.

Narration: **6,769 words** across eight YouTube explainers. All 192 narration sections were revised in plain English for a general audience on 2026-11-04. Existing video order, duration and files are unchanged.

| Topic | Runtime | Native animation frame coverage | Section clips |
|---|---:|---:|---:|
| 01 — What Happens When You Open a Website? | 8:45 | 96.8% | 24 |
| 02 — Thousands of Messages, One Cable | 8:45 | 96.8% | 24 |
| 03 — Delivering Data When Packets Get Lost | 9:05 | 96.9% | 24 |
| 04 — When Computers Talk at Once | 9:05 | 96.0% | 24 |
| 05 — How Routers Find the Best Path | 8:30 | 95.8% | 24 |
| 06 — Subnetting You Can Actually See | 8:20 | 90.2% | 24 |
| 07 — TCP vs UDP: The Cost of Reliability | 8:50 | 96.8% | 24 |
| 08 — Sending Secrets Without Sharing a Secret First | 8:50 | 95.9% | 24 |

## Checks completed

- All 192 completed-section samples pass ManimGX layout inspection.
- Persistent state and protocol checks include next-expected ACK numbering, resetting the independent ACK-2 example, byte sequences, duplicate suppression, routing updates, and matching encryption keys.
- Native animation frames cover90–97% of each timeline before constant-frame-rate export; this measures the renderer’s animated output rather than padding a static picture to30fps. Each section ends with approximately0.75–1second of hold time.
- All8 full MP4s and192 numbered clips verified as1920×1080 H.264 at constant30fps; frame counts and clip durations match section boundaries.
- The first, middle and last clips of every lesson were independently decoded and compared with the corresponding full-video images:24 comparisons passed.
- All8 browser players passed local-file tests for next/previous/replay, pause/resume, automatic hold, section selection, fullscreen, captions, presenter notes and final-section state. No external requests or JavaScript errors were observed.
- Primary-source references remain beside each lesson. Independent numerical checks confirm all four /26 subnet ranges, host counts, Dijkstra distances and failed-link route cost.

## Evidence

- [Motion and script checks](motion-series-verification.json)
- [Browser checks](browser-verification.json)
- [Clip alignment checks](clip-alignment-verification.json)
- [Local HTTP access](http-verification.json)
- Per-episode `inspect.log`, `animation-timing.json`, `motion-verification.json`, and `media-verification.json`.

## Review limits

Review combines automated checks, completed-section contact sheets and selected mid-animation images; it does not claim every video frame was manually watched. These are original explanatory diagrams inspired by visual mathematics teaching. Voiceover remains for your recording; guide subtitle timing is provisional.


## Video-only player and YouTube scripts — 2026-11-04

All eight players passed browser checks for a video-only main window, keyboard scene navigation, fullscreen, pause/resume, replay, speed limits from 0.25× to 4×, speed retention across scenes, and automatic holds at the fastest supported speed. Presenter notes were checked against the revised script. See [browser checks](browser-verification.json).

All 192 scripts were rewritten and retain their existing scene alignment. All 201 network MP4 files passed byte-for-byte hash checks. See [script verification](script-verification.json), [editorial review](script-review.md), and [all eight YouTube scripts](youtube-scripts.md).

## HTTP scene-seeking fix

The previous plain Python HTTP server returned full-file 200 responses to byte-range requests. In Chromium, scene seeks then reset the video to time zero, even while the player selected later scenes. Offline file tests did not expose this.

`python3 networks/serve.py` now serves MP4 byte ranges with 206 responses, validates unsatisfiable ranges, and avoids caching stale player pages. The updated video URL also bypasses the earlier cached response.

All eight players passed controls checks through the live HTTP server. A separate regression played lesson 1 scenes 1–5 naturally, including scene 3 at 4× and scene 4 at 1×, and verified progress, correct final holds, and backward replay. See [HTTP playback checks](http-playback-verification.json). All 201 video files remain byte-for-byte unchanged.

## Lesson 1 queue cleanup

The boxed queue items 3 and 4 were split from their parent group when earlier packets were removed. Removing only the old group left these children in later rendered scenes. PacketDirector now removes the complete owned object family during cleanup.

The group-splitting regression failed before the fix and passes afterward. Lesson 1 and its 24 section clips were regenerated at 1080p30; media checks passed. Ten decoded MP4 samples across scenes 20–24 and all five corresponding clip holds contain no leftover cyan boxes. The video-only HTTP player also passed its controls checks. See [queue cleanup verification](episodes/01-website/queue-cleanup-verification.json).

Script text and scene timings are preserved. Only lesson 1 media was regenerated: the MP4 and six final clips changed; the other 194 protected video files retain their earlier hashes. Versioned media URLs prevent the browser from reusing the older render. The preceding lesson-1 render is archived in archive/before-queue-cleanup.
