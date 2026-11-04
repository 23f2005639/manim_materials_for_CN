"""Check decoded later lesson-1 frames for the cyan queue boxes reported by the user."""
from pathlib import Path
import subprocess
import json

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / 'episodes/01-website'


def cyan_pixels(path, seconds):
    # At 1080p this covers both old boxes, stopping above the later cyan transport line.
    raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-ss', str(seconds), '-i', str(path),
                                   '-frames:v', '1', '-vf', 'crop=210:70:1230:610', '-f', 'rawvideo',
                                   '-pix_fmt', 'rgb24', '-threads', '1', '-'])
    return sum(g > 120 and b > 150 and g-r > 40 and b-r > 60
               for r, g, b in zip(raw[::3], raw[1::3], raw[2::3]))


def main():
    deck = json.loads((FOLDER / 'sections.json').read_text())
    old = ROOT / 'archive/before-queue-cleanup/01-website/episode.mp4'
    checks = []
    clips = sorted((FOLDER / 'clips').glob('*.mp4'))
    for index in range(19, 24):
        start = deck['sections'][index]['frame']/30
        end = (deck['sections'][index+1]['frame'] if index < 23 else deck['frames'])/30
        for seconds in ((start+end)/2, end-.25):
            before = cyan_pixels(old, seconds)
            after = cyan_pixels(FOLDER / 'episode.mp4', seconds)
            assert before > 100, (index, before)
            assert after < 10, (index, after)
            checks.append({'scene': index+1, 'time': round(seconds, 3),
                           'old_box_cyan_pixels': before, 'corrected_box_cyan_pixels': after})
        assert cyan_pixels(clips[index], end-start-.25) < 10
    (FOLDER / 'queue-cleanup-verification.json').write_text(json.dumps({
        'cleanup_regression': 'passed', 'decoded_frame_checks': checks,
        'clips_20_through_24': 'passed'}, indent=2)+'\n')
    print('PASS: no leftover queue boxes in 10 later MP4 frames and clips 20–24.')


if __name__ == '__main__':
    main()
