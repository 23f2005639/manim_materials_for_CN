# Networks Studio — focused stories

Eight standalone computer-networking videos, each answering one question with an original
YouTube script, animated experiments and intuitive mathematics. Built with ManimGX 0.1.1.

## Watch and record

From the project folder:

```sh
python3 networks/serve.py
```

Open <http://127.0.0.1:8765/networks/>. Click a topic, then click the animation or press →
to enter fullscreen. The main lesson window shows only the video.

- **→ / Space / Enter:** start or advance, including during playback.
- **←:** previous phase. **R:** replay. **P:** pause/resume.
- **↑ / ↓:** change speed in 0.25× steps between 0.25× and 4×.
- **F:** toggle fullscreen. **Esc:** exit fullscreen.
- **Shift+P:** separate presenter window with script, scene selector and controls.
- **C:** guide captions. **Home / End:** first / last phase.

Every phase holds its final frame until you continue. The browser tab and presenter
window show speed without an overlay on the animation. The local server supports byte
ranges so phase jumps seek correctly. Media version URLs prevent stale renders.

Read [all eight scripts](youtube-scripts.md) or each episode's `narration.md`. The scripts
have 1,100–1,250 words per episode, aimed at a general YouTube audience. Their planned
9–10 minute timings assume approximately 135 words/minute plus brief pauses. Record a
read-through in your own voice before final editing; your delivery determines final timing.
There is no generated voiceover or background music.

## One topic per video

The active series is declared in [series.json](series.json): DNS, bufferbloat, WDM,
packet switching, Dijkstra, IPv4 subnetting, TCP slow start and RSA. See the root
[topic guide](../TOPICS.md) for each video's question, boundaries, runtime and script.
Each topic has 16 meaningful phases; the engine supports differing phase counts.

The previous mixed-topic series is preserved in [the legacy index](legacy-index.html)
and [legacy scripts](legacy-scripts.md). Its original episode URLs still work.

## Beginner progression

Every lesson starts with familiar objects and introduces each new word alongside its visual meaning.
The first four phases establish the building blocks before the central experiment and equations.
The fiber lesson opens with a real ManimGX 3D cylinder, moving light pulse, and camera rotation,
then returns to a flat view for readable diagrams. Other topics use 2D for addresses, graphs,
queues and arithmetic. See [TOPICS.md](../TOPICS.md) for each lesson’s progression.

## Files and animation timing

Every active episode folder includes:

- `storyboard.json`: canonical narration, topic, visual phase identifiers and durations.
- `scene.py`: ManimGX entrypoint; topic directors are in `motion/topics/`.
- `episode.mp4`: continuous 1080p30 silent video.
- `clips/`: separate frame-accurate MP4s and an index.
- `presentation.html`: fullscreen player with narration in separate presenter notes.
- `narration.md`, `recording-cues.md`, `chapters.txt`, `guide-subtitles.srt`, `references.md`.
- Storyboard images and verification reports.

Scenes show the visual idea before its mathematics. Object motions use purposeful
normal-speed steps. The continuous video includes deliberate holds for narration rather
than stretching object movement to fill speech. The self-paced player holds after useful
motion, so you can explain at your own pace. Guide-caption timing is provisional; align
final subtitles to your recorded voice in the edit.

## Rebuild

Rendering requires Python 3.14, uv, ManimGX, and FFmpeg/FFprobe. Follow the official
[ManimGX instructions](https://manimgx.academa.ai/llms.txt) on another machine.

```sh
uv tool install --python 3.14 manimgx

# Inspect, render, export and verify one active topic, without changing the landing page.
python3 networks/build.py 01 --no-index

# Build the entire active series and publish its local index.
python3 networks/build.py all

# Rebuild only scripts and players after editing narration.
python3 networks/build.py all --prepare-only

# Inspect only, or export clips from an existing final video.
python3 networks/build.py 01 --inspect-only --no-index
python3 networks/build.py 01 --exports-only --no-index
```

Stable topic identifiers select animation modules, independently of episode numbering.
The common director removes complete owned object families at transitions, including
children detached by animations. Only intentional state persists within a phase.

## Verify

```sh
python3 networks/tests/content_check.py
python3 networks/tests/clip_refresh_check.py
python3 networks/tests/script_check.py
python3 networks/tests/motion_check.py
python3 networks/tests/clip_alignment_check.py
uv run --with playwright python networks/tests/http_check.py
uv run --with playwright python networks/tests/entry_check.py
uv run --with playwright python networks/tests/player_check.py --base-url http://127.0.0.1:8765/networks
```

Browser checks use a separate headless Chromium. If it is missing:

```sh
uv run --with playwright playwright install chromium
```

Math checks independently verify DNS timing, queue delay, packet-pipeline time,
shortest-path results, subnet ranges and the RSA toy example. See [QA.md](QA.md)
for the completed release checks and their limits.

## PDF companions for your own narration

Open [the eight PDF guides](../output/pdf/index.html). Each 10-page guide has a complete
16-clip timeline, frames decoded from the current video, plain-English explanations of
what happens and why, delivery cues, and space for your phrasing. Times match the
continuous MP4; a live explanation can take a different amount of time.

Authored notes are in `presenter-guide-notes.txt`. To regenerate the PDFs after a video
or note change, run:

```sh
uv run --with reportlab --with pypdf python networks/make_presenter_guides.py
```

The generator requires FFmpeg and DejaVu Sans fonts. Remove `tmp/pdfs/` to refresh
cached frames after replacing a video. The PDFs link to the local player, clips and sources.
