# Focused-series verification

Eight standalone topics, each developed through a visual question and its mathematics. The active series is defined in `series.json`; the older lessons remain available through `legacy-index.html`.

| Topic | Runtime | Phases | Spoken words | Verified clips |
|---|---:|---:|---:|---:|
| dns | 9:08 | 16 | 1165 | 16 |
| bufferbloat | 9:39 | 16 | 1235 | 16 |
| wdm | 9:02 | 16 | 1151 | 16 |
| packet-switching | 9:45 | 16 | 1248 | 16 |
| dijkstra | 9:26 | 16 | 1206 | 16 |
| subnetting | 8:45 | 16 | 1114 | 16 |
| tcp-slow-start | 9:45 | 16 | 1249 | 16 |
| rsa | 9:23 | 16 | 1199 | 16 |

## Completed checks

- All 128 phase-end layout samples passed ManimGX inspection. Representative mid-motion samples were checked across all eight topics. Moving-token and label collisions found during review were corrected before the accepted exports.
- Source/editorial review checked all eight complete scripts for one-topic scope, narration/animation agreement, and misleading claims.
- Independent numerical checks passed DNS timing, queue delay, packet-pipeline time, Dijkstra distances, subnet ranges and host counts, slow-start window/rate arithmetic, and RSA recovery.
- All eight full videos and 128 clips are 1920×1080 H.264 at constant 30 fps, with matching frame counts and section durations.
- Real decoded first/middle/last samples from every episode passed clip/full-video image alignment checks: 24 comparisons.
- All eight players passed HTTP browser checks for video-only display, fullscreen, navigation, replay, pause/resume, 0.25×–4× speed, correct holds, and presenter scripts.
- A separate real-HTTP test played the first five DNS phases naturally and checked exact hold times and backward replay. The server passed byte-range and unsatisfiable-range checks.
- The legacy and focused object-cleanup regression checks passed, including groups split into detached child objects.

## Reports

- [Release summary](focused-release-verification.json)
- [Script and presenter-note agreement](focused-script-verification.json)
- [Published index to fullscreen and notes](entry-verification.json)
- [Browser checks](browser-verification.json)
- [HTTP playback](http-playback-verification.json)
- [Decoded clip alignment](clip-alignment-verification.json)
- [Animation boundaries](motion-series-verification.json)

## Timing and review limits

The videos contain deliberate holds for recording a complete narration. Object movements are not slowed to stretch the film. The self-paced player pauses after useful motion and seeks to the final diagram; the continuous MP4 uses planned narration timing. Native animation-frame measurements are retained per episode and describe changing frames rather than treating static holds as motion.

Scripts target approximately 135 spoken words/minute plus short pauses. They are ready for your own voice; final spoken timing and subtitle alignment require your recording. There is no generated voiceover.

Review combines source checks, endpoint samples, representative mid-animation frames, independent calculations and browser/media tests. It does not claim every frame was manually watched.

[Earlier verification notes](legacy-QA.md) · [Topic guide](../TOPICS.md) · [All scripts](youtube-scripts.md)
