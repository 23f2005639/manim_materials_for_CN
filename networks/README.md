# Networks Studio

Eight visual computer-networking lessons for explaining and recording at your own pace.
Built with **ManimGX 0.1.1**. No account, paid service, voice service, or network connection
is needed to view the finished lessons.

## Start here

Open **[index.html](index.html)** in a browser, then choose a topic.

Each lesson shows **only the video**, with no buttons, heading, toolbar, or script overlay.
Click the animation or press **→** to start in fullscreen. Each scene holds its final
frame until you advance, so you can record at your own pace.

- **→ / Space / Enter**: start or play the next scene, including during playback.
- **←**: go back one scene. **R**: replay it.
- **↑ / ↓**: raise or lower animation speed by **0.25×**, between **0.25× and 4×**.
  Speed is preserved across scenes and shown in the browser tab title.
- **P**: pause or resume. **F**: toggle fullscreen. **Esc**: exit fullscreen.
- **Shift+P**: open the separate presenter window with the current script, scene selector,
  playback controls and speed. Keep this window outside your recording.
- **C**: toggle guide captions. **Home / End**: first / last scene.

Read [all eight YouTube scripts](youtube-scripts.md), or open each episode's `narration.md`.
The original narration uses a visual question, a developing explanation, and a closing
answer. It follows the existing scenes and uses plain English for a general audience.
The videos have no voiceover; playback speed changes only the animation.

If your browser restricts local file playback, serve these files locally:

```sh
python3 networks/serve.py
```

Then open `http://127.0.0.1:8765/networks/`. This local server supports video byte ranges, which the player needs to seek between scenes.

## What's included

Every folder under `episodes/` contains:

- `presentation.html`: the self-paced browser player.
- `episode.mp4`: the continuous 1080p, 30 fps H.264 video, without voiceover.
- `clips/`: 24 numbered, frame-accurate MP4s and a clip index.
- `narration.md`: the complete English script for your own voice.
- `recording-cues.md`: section timings and visual cues.
- `guide-subtitles.srt`: planned captions; adjust timing after recording your voice.
- `chapters.txt`: chapter markers for the continuous edit.
- `storyboard.json`: the editable narration, visual instructions, and section durations.
- `scene.py`: the ManimGX scene entrypoint.
- `storyboard*.png`: 24 sampled diagrams, six per sheet.
- `references.md`: the sources checked for that lesson.
- `media-verification.json`: measured video and clip checks.

`engine.py` supplies the short heading and timing. The directors in `motion/` supply
persistent packet paths, evolving signals, graph relaxations, moving subnet boundaries,
buffers, timers, and encryption transformations. Diagrams use the full frame; explanatory
paragraphs and bullet panels stay out of the video. Narration is concise and kept in notes.
All visual assets are generated locally. The original solar-system files are preserved.

## Record and edit

For a live explanation, screen-record the presentation and advance whenever you finish
speaking. Your recording may exceed ten minutes because you control the pauses.

For a tighter YouTube edit, record one script section at a time, align it with the matching
numbered clip, and trim or extend the final held frame as needed. Alternatively, record
over the continuous MP4. Each continuous video stays within five to ten minutes. Short
scripts leave room to explain the evolving diagrams in your own words. There is no AI
voiceover or background music.

Most of each section contains changing diagrams and causal events. The browser stops
when its motion finishes and holds for as long as you need. There is only a short final
hold inside the continuous MP4. The browser's indefinite pauses do not extend that file.

The previous edition's detailed scripts and source are preserved in `archive/first-edition/`.

## Render and maintain

Requirements: Python 3.14, `uv`, ManimGX, and FFmpeg/FFprobe. They are installed on this
machine. Follow [ManimGX's instructions](https://manimgx.academa.ai/llms.txt) for another machine.

```sh
uv tool install --python 3.14 manimgx

# One episode: inspect, render, export clips, and verify.
python3 networks/build.py 03

# Entire series.
python3 networks/build.py all

# Inspect only, or make a 720p draft.
python3 networks/build.py 03 --inspect-only
python3 networks/build.py 03 --draft

# Rebuild scripts/player after editing text; animation changes need a new render.
python3 networks/build.py all --prepare-only

# Regenerate clips from an existing final render.
python3 networks/build.py 03 --exports-only

# Content/numerical checks and actual local-file browser controls regression.
python3 networks/tests/content_check.py
python3 networks/tests/motion_check.py
python3 networks/tests/clip_alignment_check.py
uv run --with playwright python networks/tests/player_check.py
```

Browser testing uses a separate headless Chromium, never your existing browser session.
Its executable is discovered in `~/.cache/ms-playwright/`. If absent, install it with
`uv run --with playwright playwright install chromium`.

Every section uses ManimGX's `next_section` and presenter notes. The generated player
uses the rendered frame boundaries to stop accurately and keeps all controls out of
the MP4 image. No changes to the installed ManimGX package are required.

## Teaching models

These lessons use clearly identified classroom models: HTTP/1.1 over TCP is one web
request example; CSMA/CD is shared, half-duplex Ethernet; Go-Back-N uses next-expected
packet acknowledgments rather than TCP byte offsets; subnet host counts refer to
ordinary LANs with `/31` and `/32` exceptions explained; hybrid encryption is a
simplified construction, not an implementation of modern TLS.

Videos and scripts are complete teaching assets. Your recorded voice, final voice-to-video
alignment, and YouTube publishing remain your editing steps.
