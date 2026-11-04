# Computer Networks — self-paced animation series

Open **[Networks Studio](networks/index.html)** for all eight interactive lessons.
Each lesson includes a continuous video, 24 numbered clips, and a complete English
recording script. See [production and recording instructions](networks/README.md).

## Topics and scripts

See [TOPICS.md](TOPICS.md) for the subjects covered by each video, worked examples,
runtimes, and links to individual scripts. Read [all eight narration scripts](networks/youtube-scripts.md)
or press **Shift+P** inside a lesson to open its current script in a separate window.

## Run locally

From this project folder:

```sh
python3 networks/serve.py
```

Open <http://127.0.0.1:8765/networks/>. Click the video or press **→** to start fullscreen.
Use **→/←** for scenes, **↑/↓** for speed, **P** to pause, and **R** to replay.
The custom server supports the video seeking required by scene navigation.

Finished videos are included, so playback needs only Python and a browser. Rendering
requires the tools documented in [networks/README.md](networks/README.md).

## Push to GitHub

This folder is a Git repository on branch `main`. Create an empty repository on GitHub,
then run these commands from this folder, replacing the URL with your repository's URL:

```sh
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```

The initial commits are authored by Codex. Set your own author identity before making
future commits (these commands apply only to this repository):

```sh
git config user.name "Your Name"
git config user.email "YOUR_GITHUB_EMAIL"
```

For later changes:

```sh
git add .
git commit -m "Describe your change"
git push
```

Caches, local environments, secret environment files, and render logs are ignored.
The finished MP4s, clips, source, scripts, previews, and verification records are tracked.
The `networks/archive/` folder preserves earlier scripts and the reference render used
by the queue-cleanup regression check.

## Earlier project: 3D solar system — ManimGX

`SolarSystem.mp4` is a 30-second H.264 video at 1920×1080, 30 fps.
The scene includes eight textured planets, Earth's Moon, Saturn's rings,
an asteroid belt, and a moving 3D camera. The textures are generated locally.
Sizes, distances, orbital speeds, and circular paths are illustrative.

Created with ManimGX 0.1.1, following https://manimgx.academa.ai/llms.txt.

## Render and open again

```sh
./render_solar_system.sh
```

Or run each step:

```sh
uv tool install --python 3.14 manimgx
manimgx inspect solar_system.py -t 4,10,20,29,end
manimgx render solar_system.py -r 1920x1080 --fps 30 --crf 20
xdg-open SolarSystem.mp4
```

`SolarSystem.storyboard.png` contains rendered frames for visual review.
ManimGX skips automatic 2D layout checks for 3D scenes; the storyboard was
visually inspected before rendering.
