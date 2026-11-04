# Networks Studio

Eight complete computer-networking lessons for explaining and recording at your own pace.
Built with **ManimGX 0.1.1**. No account, paid service, voice service, or network connection
is needed to view the finished lessons.

## Start here

Open **[index.html](index.html)** in a browser, then choose a topic.

Each presentation starts paused. Click **Next**, click the animation, or press **Space / →**
to play one section. It stops on that section's final frame and waits indefinitely.
Use **Previous**, **Replay**, or the section selector to revisit an explanation.
Next is disabled during playback, so an accidental click cannot skip the animation.
Use **Pause/Resume** to stop within a section.

**Presenter notes** opens a separate window with the complete script for the current section.
Keep that window off the captured screen when recording. Notes are also available below
the main player, collapsed by default. Fullscreen hides the inline notes and page header.

Keyboard controls: Space/→ next, ← previous, R replay, P pause/resume, F fullscreen,
Shift+P presenter notes, C guide captions, Home/End first/last section.

If your browser restricts local file playback, serve these files locally:

```sh
cd /home/human/coputer_networdsproj
python3 -m http.server 8765 --bind 127.0.0.1
```

Then open `http://127.0.0.1:8765/networks/`. The server is local to your computer.

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

`engine.py` supplies shared typography and timing. `visuals.py` supplies the animated
packet paths, timelines, waveforms, graphs, binary addresses, and encryption diagrams.
All visual assets are generated locally. The original solar-system files are preserved.

## Record and edit

For a live explanation, screen-record the presentation and advance whenever you finish
speaking. Your recording may exceed ten minutes because you control the pauses.

For a tighter YouTube edit, record one script section at a time, align it with the matching
numbered clip, and trim or extend the final held frame as needed. Alternatively, record
over the continuous MP4. Scripts are paced around 140 words per minute and each continuous
video stays within five to ten minutes. There is no AI voiceover or background music.

The video animations finish early within each section to leave time for the spoken
explanation. The browser stops as soon as the visual motion finishes, so you do not
have to sit through the MP4's planned narration hold before clicking Next. Its indefinite
click-to-continue pauses do not extend the MP4.

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
