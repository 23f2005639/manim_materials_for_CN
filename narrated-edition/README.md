# Computer Networks / Narrated Edition

A separate version of the eight ManimGX lessons with ElevenLabs male narration.
The original videos, sources, player settings and PDFs remain in their original folders.

## Open

From the repository root, run `python3 networks/serve.py`, then open:

http://127.0.0.1:8765/narrated-edition/

Each topic includes a continuous narrated MP4 and a fullscreen player with sixteen
phases. Right/Left advances or goes back, Up/Down changes speed, P pauses, R replays,
and Shift+P opens notes. The player holds after both the complete spoken explanation and the slowed animation finish. Leave the browser speed at1x to hear the narration normally; the animation is already slowed in the exported file.

## Voice and teaching approach

Voice: David - Clear, Friendly Explainer, selected from the connected ElevenLabs
voice library. Model: eleven_v4. This is an existing licensed library voice, not a
clone of a particular teacher. There is no institutional affiliation or endorsement.

The scripts use concrete examples, prediction questions, visual reasoning and short
mathematical explanations. Restrained `[curious]`, `[warmly]` and `[short pause]`
directions shape delivery. There are no theatrical sound effects or background music.

`script.md` is readable narration; `requests/` contains the exact tagged speech
requests. Two standard voice takes are saved when available. `selected-takes.json`
records which take is used. The first available complete take is selected for assembly.
`generation-jobs.json` and `audio-receipts.json` preserve generation provenance.

## Video assembly

The original phase clips are reused. Their moving portions run at **0.5x** speed. Narration remains at **1x** speed.
Final holds are trimmed or extended to fit the actual audio, with a brief lead-in and
room after the spoken ending. Audio is normalized toward -16 LUFS with a -1.5 dBTP
ceiling and encoded as AAC. Clip boundaries match the resulting MP4 frames at 30fps.

Guide captions are proportional timings, not word-aligned subtitles. The script and
spoken recording should be checked before publishing a captioned YouTube release.

After audio has been downloaded, `python3 narrated-edition/assemble.py` resumes local
assembly without contacting ElevenLabs or spending more generation credits. Source
hashes are checked to verify original episode files were preserved.

## Half-speed animation verification

The exports bake0.5x into the video frames; speech stays at1x. Keyboard playback
speed is left at1x by default. To verify matching frames at twice their source time
and unchanged decoded narration, run:

```sh
uv run --with pillow python narrated-edition/check_half_speed.py
```

Each clip has a render-settings record so assembly refreshes the outputs when the
video-speed setting or input media changes. No new ElevenLabs generation is needed.
