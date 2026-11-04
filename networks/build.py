#!/usr/bin/env python3
"""Render lessons and export their offline player, scripts, captions and clips."""
from __future__ import annotations

import argparse
import concurrent.futures
import html
import json
import math
import re
import subprocess
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FPS = 30


def read(path: Path) -> dict:
    data = json.loads(path.read_text())
    count = len(data["sections"])
    assert 12 <= count <= (18 if data.get("edition") == "focused-v2" else 24), path
    assert abs(sum(s["duration"] for s in data["sections"]) - data["duration"]) < 0.01
    assert 300 <= data["duration"] <= 600
    assert len({s["id"] for s in data["sections"]}) == count
    for s in data["sections"]:
        assert s["narration"] and s["title"] and s["takeaway"] and s["visual"]
        assert 10 <= s["duration"] <= (90 if data.get("edition") == "focused-v2" else 35)
        assert len(s["bullets"]) >= 1
    return data


def episode_paths() -> list[Path]:
    manifest = ROOT / "series.json"
    if not manifest.exists():
        return sorted((ROOT / "episodes").glob("*/storyboard.json"))
    series = json.loads(manifest.read_text())
    paths = [ROOT / e["folder"] / "storyboard.json" for e in series["episodes"]]
    assert len(paths) == len(set(paths)) == 8
    return paths


def stamp(seconds: float, milliseconds: bool = False) -> str:
    t = round(seconds * 1000)
    h, rest = divmod(t, 3600000)
    m, rest = divmod(rest, 60000)
    s, ms = divmod(rest, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}" if milliseconds else f"{h:02}:{m:02}:{s:02}"


def timeline(data: dict) -> dict:
    t = 0.0
    sections = []
    captions = []
    for s in data["sections"]:
        a = round(t * FPS) / FPS
        t += s["duration"]
        b = round(t * FPS) / FPS
        sections.append({"name": s["title"], "frame": round(a * FPS), "type": "default.normal",
                         "notes": s["narration"], "id": s["id"], "chapter": s["chapter"]})
        # Short guide captions are easier to read than a section-long paragraph.
        words = s["narration"].split()
        groups = [" ".join(words[i:i + 11]) for i in range(0, len(words), 11)]
        for j, text in enumerate(groups):
            ca = a + (b - a) * j / len(groups)
            cb = a + (b - a) * (j + 1) / len(groups)
            captions.append([ca, cb, textwrap.fill(text, 46)])
    return {"fps": FPS, "frames": round(t * FPS), "sections": sections,
            "captions": captions, "title": data["title"]}


def write_documents(folder: Path, data: dict, deck: dict) -> None:
    video_path = folder / "episode.mp4"
    if video_path.exists():
        stream = next(s for s in probe(video_path)["streams"] if s["codec_type"] == "video")
        if stream["avg_frame_rate"] == "30/1" and abs(int(stream["nb_frames"]) - deck["frames"]) <= 1:
            deck["frames"] = int(stream["nb_frames"])
    timing_path = folder / "animation-timing.json"
    if timing_path.exists():
        timing = json.loads(timing_path.read_text())
        if len(timing["sections"]) == len(deck["sections"]) and abs(timing["duration"] - data["duration"]) < .1:
            for section, motion in zip(deck["sections"], timing["sections"]):
                assert section["name"] == motion["name"], "Animation timing is stale; inspect again"
                section["animation_end_frame"] = motion["animation_end_frame"]
    title = data["title"]
    narration = [f"# {title}\n", f"English narration for your own voice. Planned runtime: {stamp(data['duration'])}.\n",
                 "The browser pauses after each section. The timestamps below refer to the continuous MP4.\n"]
    cues = [f"# Recording cues — {title}\n", "Record one section at a time, or narrate the click-through presentation live.\n",
            "Guide subtitles use planned timing. Match final subtitles to your recording after editing.\n",
            "| Section | Start | Length | What to show | Recording cue |", "|---|---|---|---|---|"]
    chapter_rows = []
    last_chapter = None
    for i, (s, actual) in enumerate(zip(data["sections"], deck["sections"])):
        start = actual["frame"] / FPS
        end = (deck["sections"][i + 1]["frame"] if i + 1 < len(deck["sections"]) else deck["frames"]) / FPS
        narration.extend([f"\n## {i + 1:02}. {s.get('short_title', s['title'])} — {stamp(start)}\n",
                          s["narration"] + "\n"])
        cues.append(f"| {i + 1:02} | {stamp(start)} | {end-start:.2f}s | {s['title']} | {s['takeaway']} |")
        if s["chapter"] != last_chapter:
            # YouTube chapter syntax uses MM:SS rather than HH:MM:SS for short videos.
            chapter_rows.append(f"{int(start)//60:02}:{int(start)%60:02} {s['chapter']}")
            last_chapter = s["chapter"]
    (folder / "narration.md").write_text("\n".join(narration))
    (folder / "recording-cues.md").write_text("\n".join(cues) + "\n")
    (folder / "chapters.txt").write_text("\n".join(chapter_rows) + "\n")
    refs = [f"# References — {title}\n", "Sources checked while writing the teaching script; narration is original.\n"]
    for source in data["sources"]:
        refs.append(f"- [{source['title']}]({source['url']}) — {source.get('notes', '')}")
    refs.append("\nAnimation engine: [ManimGX instructions](https://manimgx.academa.ai/llms.txt).")
    (folder / "references.md").write_text("\n".join(refs) + "\n")
    srt = []
    for i, (a, b, text) in enumerate(deck["captions"], 1):
        srt.append(f"{i}\n{stamp(a, True)} --> {stamp(b, True)}\n{text}\n")
    (folder / "guide-subtitles.srt").write_text("\n".join(srt))
    (folder / "sections.json").write_text(json.dumps(deck, indent=2) + "\n")
    template = (ROOT / "templates/player.html").read_text()
    safe_deck = json.dumps(deck, ensure_ascii=False).replace("</", "<\\/")
    media_version = str(video_path.stat().st_mtime_ns) if video_path.exists() else "pending"
    page = template.replace("__TITLE__", html.escape(title)).replace("__DECK__", safe_deck).replace("__MEDIA_VERSION__", media_version)
    (folder / "presentation.html").write_text(page)
    scene = '''from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from networks.engine import LessonScene

class Episode(LessonScene):
    storyboard_path = Path(__file__).with_name("storyboard.json")
'''
    if data.get("topic") == "wdm":
        scene = scene.replace("from networks.engine import LessonScene", "from networks.engine import Lesson3DScene as LessonScene")
    (folder / "scene.py").write_text(scene)


def run(command: list[str], log: Path) -> None:
    print("  " + " ".join(command), flush=True)
    with log.open("w") as output:
        result = subprocess.run(command, cwd=ROOT.parent, stdout=output, stderr=subprocess.STDOUT)
    if result.returncode:
        detail = log.read_text()
        detail = "layout:" + detail.rsplit("layout:", 1)[1] if "layout:" in detail else detail[-3500:]
        raise RuntimeError(f"Command failed ({result.returncode}): {log}\n{detail}")


def inspect(folder: Path, data: dict) -> None:
    # One complete diagram from every section, rather than hundreds of animation endpoints.
    samples = []
    t = 0.0
    for s in data["sections"]:
        t += s["duration"]
        samples.append(f"{t-.25:.3f}")
    samples[-1] = "end"  # Complete construct(), including the recorded motion timings.
    run(["manimgx", "inspect", str(folder / "scene.py"), "-t", ",".join(samples),
         "-o", str(folder / "storyboard.png")], folder / "inspect.log")


def export_clips(folder: Path, deck: dict) -> None:
    target = folder / "clips"
    target.mkdir(exist_ok=True)
    jobs = []
    for i, section in enumerate(deck["sections"]):
        start = section["frame"]
        end = deck["sections"][i+1]["frame"] if i+1<len(deck["sections"]) else deck["frames"]
        slug = re.sub(r"[^a-z0-9]+", "-", section["name"].lower()).strip("-")
        output = target / f"{i+1:02}-{slug}.mp4"
        jobs.append((start, end, output))

    def encode(job: tuple[int, int, Path]) -> None:
        a, b, output = job
        # Accurate seek + re-encode; stream copying can start on the wrong keyframe.
        command = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{a/FPS:.9f}",
                   "-i", str(folder / "episode.mp4"), "-frames:v", str(b-a), "-an",
                   "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-threads", "2",
                   "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(output)]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode:
            raise RuntimeError(result.stderr)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        list(pool.map(encode, jobs))
    # Titles can change between editions; keep only the newly exported phase clips.
    expected = {output for _, _, output in jobs}
    for previous in target.glob("[0-9][0-9]-*.mp4"):
        if previous not in expected:
            previous.unlink()
    rows = []
    for i, (_, _, output) in enumerate(jobs):
        rows.append(f'<li><a href="{html.escape(output.name)}">{i+1:02}. {html.escape(deck["sections"][i]["name"])}</a></li>')
    (target / "index.html").write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Individual section clips</title><style>body{background:#07111f;color:#edf4ff;font:18px/1.8 system-ui;max-width:900px;margin:40px auto;padding:20px}a{color:#64d8eb}</style><a href="../presentation.html">← Presentation</a><h1>Individual section clips</h1><ol>' + ''.join(rows) + '</ol></html>')


def normalize_video(folder: Path, deck: dict) -> None:
    # ManimGX stores static holds as long VFR frames. Editors and frame-based clip
    # exports need an actual constant-rate stream, not just a nominal 30fps label.
    source = folder / "episode.mp4"
    video = next(s for s in probe(source)["streams"] if s["codec_type"] == "video")
    if video["avg_frame_rate"] == "30/1" and int(video["nb_frames"]) == deck["frames"]:
        return
    target = folder / "episode.cfr.mp4"
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(source),
         "-vf", "fps=30,tpad=stop_mode=clone:stop_duration=0.1", "-frames:v", str(deck["frames"]),
         "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-threads", "4",
         "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(target)], folder / "normalize.log")
    checked = next(s for s in probe(target)["streams"] if s["codec_type"] == "video")
    assert int(checked["nb_frames"]) == deck["frames"]
    assert checked["avg_frame_rate"] == "30/1"
    target.replace(source)


def probe(path: Path) -> dict:
    result = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
                            capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


def verify(folder: Path, data: dict, deck: dict, clips: bool = True) -> dict:
    info = probe(folder / "episode.mp4")
    video = next(s for s in info["streams"] if s["codec_type"] == "video")
    duration = float(info["format"]["duration"])
    assert (video["width"], video["height"]) == (1920, 1080)
    assert video["codec_name"] == "h264" and video["avg_frame_rate"] == "30/1"
    assert int(video["nb_frames"]) == deck["frames"]
    assert abs(duration - data["duration"]) < 0.15, (duration, data["duration"])
    assert 300 <= duration <= 600
    clip_count = 0
    if clips:
        files = sorted((folder / "clips").glob("*.mp4"))
        assert len(files) == len(deck["sections"])
        for i, file in enumerate(files):
            clip_info = probe(file)
            v = next(s for s in clip_info["streams"] if s["codec_type"] == "video")
            end = deck["sections"][i+1]["frame"] if i+1<len(deck["sections"]) else deck["frames"]
            expected = end - deck["sections"][i]["frame"]
            assert int(v["nb_frames"]) == expected, (file, v["nb_frames"], expected)
            assert v["avg_frame_rate"] == "30/1", file
            assert abs(float(clip_info["format"]["duration"]) - expected/FPS) <= 0.04, file
            assert (v["width"], v["height"]) == (1920, 1080)
        clip_count = len(files)
    words = sum(len(s["narration"].split()) for s in data["sections"])
    assert (1100 <= words <= 1250) if data.get("edition") == "focused-v2" else (500 <= words <= 900)
    report = {"episode": data["id"], "title": data["title"], "duration_seconds": duration,
              "resolution": "1920x1080", "fps": 30, "codec": "h264", "sections": len(data["sections"]),
              "section_clips_verified": clip_count, "narration_words": words,
              "automated_media_checks": "passed", "edition": data.get("edition", "visual"),
              "voiceover": "User records their own voice"}
    motion_path = folder / "motion-verification.json"
    if motion_path.exists():
        report["motion"] = json.loads(motion_path.read_text())
    (folder / "media-verification.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


def write_index() -> None:
    cards = []
    scripts = ["# YouTube narration scripts\n\nOriginal narration for eight visual networking explainers. Scene headings and timestamps are recording cues, not spoken lines. The scripts follow the existing animations; record in your own voice and use the scene holds for pauses.\n"]
    for path in episode_paths():
        data = read(path)
        folder = path.parent
        rel = folder.relative_to(ROOT).as_posix()
        available = (folder / "episode.mp4").exists()
        narration = folder / "narration.md"
        if narration.exists():
            scripts.append(narration.read_text())
        chapter_count = len({s["chapter"] for s in data["sections"]})
        cards.append(f'''<a class="card" href="{rel}/presentation.html"><span class="n">{data['id']}</span><div class="meta">{stamp(data['duration'])[3:]} · {len(data['sections'])} click-through phases · {chapter_count} chapters</div><h2>{html.escape(data['title'])}</h2><p>{html.escape(data['sections'][0]['takeaway'])}</p><span class="open">{'Open lesson →' if available else 'Preparing lesson…'}</span></a>''')
    page = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Networks Studio — 8 self-paced lessons</title><style>:root{color-scheme:dark;font-family:system-ui,sans-serif;background:#07111f;color:#edf4ff}*{box-sizing:border-box}body{margin:0}.wrap{max-width:1280px;margin:auto;padding:56px 28px}.eyebrow{color:#64d8eb;font-size:13px;letter-spacing:.18em}h1{font-size:clamp(36px,6vw,64px);line-height:1.04;letter-spacing:-.04em;max-width:950px;margin:18px 0}header p{font-size:18px;line-height:1.7;color:#a6bbd3;max-width:780px}.pill{display:inline-block;background:#112c38;border:1px solid #285369;color:#98e7ee;border-radius:25px;padding:8px 15px;font-size:13px;margin:12px 10px 24px 0}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px;margin:24px 0}.card{position:relative;text-decoration:none;color:inherit;border:1px solid #263d56;border-radius:18px;background:linear-gradient(135deg,#11253b,#0b192b);padding:28px;min-height:245px;transition:border-color .15s,transform .15s}.card:hover{border-color:#64d8eb;transform:translateY(-3px)}.card:focus-visible{outline:3px solid #64d8eb}.n{position:absolute;right:25px;top:18px;font-size:60px;font-weight:800;color:#29435c}.meta{font-size:12px;color:#a4bed6;max-width:80%;line-height:1.6}h2{position:relative;font-size:25px;max-width:85%;margin:20px 0 10px}.card p{color:#a6bbd3;line-height:1.5;max-width:85%;font-size:14px}.open{display:inline-block;margin-top:12px;color:#64d8eb;font-weight:700}footer{border-top:1px solid #263d56;padding-top:20px;color:#9db3cc;line-height:1.8;font-size:14px}footer a{color:#64d8eb}@media(max-width:720px){.grid{grid-template-columns:1fr}.wrap{padding:30px 18px}h2{font-size:23px}.n{font-size:48px}}</style><main class="wrap"><header><div class="eyebrow">COMPUTER NETWORKS / FOCUSED STORIES</div><h1>One question.<br>One discovery.</h1><p>Eight standalone visual stories. Start with everyday objects, build the picture one step at a time, then discover the mathematics behind it. Full recording scripts stay in a separate presenter window.</p><span class="pill">8 topics · one idea per video</span><span class="pill">From the basics · 1080p</span><span class="pill">Offline · no sign-in · no voiceover</span></header><section class="grid">__CARDS__</section><footer><strong>How it works:</strong> Open a topic and click the video or press → to start fullscreen. The lesson shows only the video. Press →/← for scenes, ↑/↓ to change speed (0.25×–4×), P to pause, R to replay, F to toggle fullscreen, and Shift+P for a separate presenter window. Each scene holds its final frame until you continue. Each lesson also includes its full MP4, script, guide subtitles, and individual clips.<br>Record at your own pace; continuous video timings are a guide. Read <a href="youtube-scripts.md">all eight YouTube scripts</a>, <a href="README.md">production instructions</a>, and <a href="QA.md">quality checks</a>. Earlier videos remain in <a href="legacy-index.html">the previous series</a>.</footer></main></html>'''
    (ROOT / "index.html").write_text(page.replace("__CARDS__", "".join(cards)))
    combined = "\n\n---\n\n".join(scripts)
    (ROOT / "youtube-scripts.md").write_text(combined)
    # Preserve links shared before the narration was revised for YouTube.
    (ROOT / "student-scripts.md").write_text(combined)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("episode", nargs="?", default="all", help="01 through 08, or all")
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--no-index", action="store_true", help="Keep the current landing page and combined script unchanged")
    parser.add_argument("--inspect-only", action="store_true")
    parser.add_argument("--draft", action="store_true", help="720p draft; no final export")
    parser.add_argument("--exports-only", action="store_true", help="Use an already rendered final MP4")
    parser.add_argument("--no-clips", action="store_true")
    args = parser.parse_args()
    paths = episode_paths()
    if args.episode != "all":
        paths = [p for p in paths if read(p)["id"] == args.episode.zfill(2) or read(p).get("topic") == args.episode]
    if not paths:
        parser.error("No matching storyboards")
    for path in paths:
        folder = path.parent
        data = read(path)
        deck = timeline(data)
        if args.exports_only and (folder / "sections.json").exists():
            recorded = json.loads((folder / "sections.json").read_text())
            assert len(recorded["sections"]) == len(deck["sections"])
            for planned, actual in zip(deck["sections"], recorded["sections"]):
                assert planned["name"] == actual["name"], "Storyboard changed; render again before exporting"
                planned["frame"] = actual["frame"]
            deck["frames"] = recorded["frames"]
        print(f"\n{data['id']} — {data['title']}", flush=True)
        write_documents(folder, data, deck)
        if args.prepare_only:
            continue
        if not args.exports_only:
            inspect(folder, data)
            if args.inspect_only:
                write_documents(folder, data, deck)
                continue
            if args.draft:
                run(["manimgx", "render", str(folder / "scene.py"), "-o", str(folder / "draft.mp4"),
                     "-r", "1280x720", "--fps", "30", "--preset", "veryfast"], folder / "draft-render.log")
                continue
            run(["manimgx", "present", str(folder / "scene.py"), "-o", str(folder / "episode.mp4"),
                 "-r", "1920x1080", "--fps", "30", "--no-open"], folder / "render.log")
            native = (folder / "episode.html").read_text()
            marker = "const deck = "
            actual, _ = json.JSONDecoder().raw_decode(native.split(marker, 1)[1])
            assert len(actual["sections"]) == len(deck["sections"])
            for planned, recorded in zip(deck["sections"], actual["sections"]):
                assert abs(planned["frame"] - recorded["frame"]) <= 1, (planned, recorded)
            # Store actual frame boundaries; narration/caption chunks remain storyboard-derived.
            for planned, recorded in zip(deck["sections"], actual["sections"]):
                planned["frame"] = recorded["frame"]
            deck["frames"] = actual["frames"]
            source_stream = next(s for s in probe(folder / "episode.mp4")["streams"] if s["codec_type"] == "video")
            fraction = int(source_stream["nb_frames"]) / deck["frames"]
            if data.get("edition") != "focused-v2":
                assert fraction >= 0.6, f"Only {fraction:.0%} of the native timeline has changing frames"
            timing = json.loads((folder / "animation-timing.json").read_text())
            assert timing.get("edition") == data.get("edition", "visual")
            assert all(s["visual_seconds"] > 0 for s in timing["sections"])
            if data.get("edition") != "focused-v2":
                assert all(s["visual_fraction"] >= .65 for s in timing["sections"])
            (folder / "motion-verification.json").write_text(json.dumps({
                "native_changing_frame_fraction": round(fraction, 4),
                "minimum_section_visual_fraction": min(s["visual_fraction"] for s in timing["sections"]),
                "longest_final_hold_seconds": max(s["section_seconds"] - s["visual_seconds"] - .4 for s in timing["sections"]),
            }, indent=2) + "\n")
            write_documents(folder, data, deck)
            (folder / "episode.html").unlink()  # The customized presentation.html is the entrypoint.
        if args.exports_only:
            source_stream = next(s for s in probe(folder / "episode.mp4")["streams"] if s["codec_type"] == "video")
            if source_stream["avg_frame_rate"] != "30/1":
                timing = json.loads((folder / "animation-timing.json").read_text())
                (folder / "motion-verification.json").write_text(json.dumps({
                    "native_changing_frame_fraction": round(int(source_stream["nb_frames"]) / deck["frames"], 4),
                    "minimum_section_visual_fraction": min(s["visual_fraction"] for s in timing["sections"]),
                    "longest_final_hold_seconds": max(s["section_seconds"] - s["visual_seconds"] - .4 for s in timing["sections"]),
                }, indent=2) + "\n")
        normalize_video(folder, deck)
        if not args.no_clips:
            print(f"  Exporting {len(deck['sections'])} frame-accurate phase clips…", flush=True)
            export_clips(folder, deck)
        write_documents(folder, data, deck)
        print("  " + json.dumps(verify(folder, data, deck, not args.no_clips)), flush=True)
        (folder / "episode.html").unlink(missing_ok=True)
    if not args.no_index:
        write_index()


if __name__ == "__main__":
    main()
