# Computer Networks / Narrated Edition

A separate version of the eight ManimGX lessons with ElevenLabs male narration.
The original videos, sources, player settings and PDFs remain in their original folders.

## Open

From the repository root, run `python3 networks/serve.py`, then open:

http://127.0.0.1:8765/narrated-edition/

Each topic includes a continuous narrated MP4 and a fullscreen player with sixteen
phases. Right/Left advances or goes back, Up/Down changes speed, P pauses, R replays,
and Shift+P opens notes. The player holds after the complete spoken explanation.

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

The original phase clips are reused. Their moving portions keep their original speed.
Final holds are trimmed or extended to fit the actual audio, with a brief lead-in and
room after the spoken ending. Audio is normalized toward -16 LUFS with a -1.5 dBTP
ceiling and encoded as AAC. Clip boundaries match the resulting MP4 frames at 30fps.

Guide captions are proportional timings, not word-aligned subtitles. The script and
spoken recording should be checked before publishing a captioned YouTube release.

After audio has been downloaded, `python3 narrated-edition/assemble.py` resumes local
assembly without contacting ElevenLabs or spending more generation credits. Source
hashes are checked to verify original episode files were preserved.
