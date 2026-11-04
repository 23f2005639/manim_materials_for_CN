"""Check real decoded images, independently of container frame-count metadata."""
import io
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageChops, ImageStat

ROOT = Path(__file__).resolve().parents[1]


def frame(path, seconds):
    data = subprocess.check_output([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-ss", f"{seconds:.9f}",
        "-i", str(path), "-frames:v", "1", "-vf", "scale=640:360", "-threads", "1",
        "-f", "image2pipe", "-vcodec", "png", "-",
    ])
    return Image.open(io.BytesIO(data)).convert("RGB")


def main():
    results = []
    for folder in sorted((ROOT / "episodes").iterdir()):
        if not (folder / "media-verification.json").exists():
            continue
        deck = json.loads((folder / "sections.json").read_text())
        clips = sorted((folder / "clips").glob("*.mp4"))
        assert len(clips) == 24
        for index in (0, 11, 23):
            start = deck["sections"][index]["frame"] / 30
            original = frame(folder / "episode.mp4", start + 1)
            extracted = frame(clips[index], 1)
            error = max(ImageStat.Stat(ImageChops.difference(original, extracted)).mean)
            assert error < 4, (folder.name, index + 1, error)
            results.append({"episode": folder.name, "section": index + 1, "maximum_channel_mean_error": round(error, 4)})
        print(folder.name, "first/middle/last clips align", flush=True)
    assert len(results) == 24, "All 8 final episodes must be present"
    (ROOT / "clip-alignment-verification.json").write_text(json.dumps(results, indent=2) + "\n")


if __name__ == "__main__":
    main()
