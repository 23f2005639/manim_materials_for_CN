# Computer Networks — one question per video

Eight original ManimGX explainers: DNS, bufferbloat, WDM, packet switching, Dijkstra,
IPv4 subnetting, TCP slow start, and RSA. Each focuses on one story with visual intuition,
mathematics, and a complete YouTube narration script for your own voice.
The current edition starts from everyday examples and builds every topic from the basics.
The fiber lesson includes a 3D strand and moving light pulse.

See [TOPICS.md](TOPICS.md) for the full topic guide and scripts.

## Open the videos

From this folder:

```sh
python3 networks/serve.py
```

Open <http://127.0.0.1:8765/networks/>. Click the video or press **→** to start fullscreen.
Use **→/←** for phases, **↑/↓** for speed, **P** to pause, and **R** to replay.
**Shift+P** opens the current script in a separate window. Only the animation appears
in the audience window. Finished videos are included; playback needs Python and a browser.

[All scripts](networks/youtube-scripts.md) · [Rendering and recording](networks/README.md) ·
[Quality checks](networks/QA.md) · [Previous series](networks/legacy-index.html)

## Push to GitHub

The repository uses branch `main`. Create an empty GitHub repository, replace the URL,
and run:

```sh
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```

Codex authored the local build commits. Set your identity before future commits:

```sh
git config user.name "Your Name"
git config user.email "YOUR_GITHUB_EMAIL"
git add .
git commit -m "Describe your change"
git push
```

Finished media, scripts, source, and verification records are tracked. Caches, local
environments, secret environment files, and render logs are ignored. The old episode
URLs and their existing assets remain available alongside the new active series.

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
