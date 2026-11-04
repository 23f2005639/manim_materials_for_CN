"""Regression for real HTTP scene seeking, including lesson 1 scenes 3 and 4.

uv run --with playwright python networks/tests/http_check.py
"""
from functools import partial
from http.server import ThreadingHTTPServer
import json
from pathlib import Path
import sys
from threading import Thread
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from serve import VideoHandler
from build import episode_paths


class QuietHandler(VideoHandler):
    def log_message(self, *args):
        pass


def main():
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT.parent)))
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f'http://127.0.0.1:{server.server_port}/networks'
    folder = episode_paths()[0].parent
    relative = folder.relative_to(ROOT).as_posix()
    source = folder / 'episode.mp4'
    data = source.read_bytes()
    media = base + '/' + relative + '/episode.mp4'
    try:
        for value, start, end in [('bytes=1000-1999', 1000, 1999), ('bytes=-128', len(data)-128, len(data)-1),
                                  (f'bytes={len(data)-2}-', len(data)-2, len(data)-1),
                                  (f'bytes={len(data)-2}-{len(data)+100}', len(data)-2, len(data)-1)]:
            with urlopen(Request(media, headers={'Range': value})) as response:
                assert response.status == 206
                assert response.headers['Content-Range'] == f'bytes {start}-{end}/{len(data)}'
                assert response.headers['Accept-Ranges'] == 'bytes'
                assert response.read() == data[start:end+1]
        for value in ['bytes=999999999-', 'bytes=100-50', 'bytes=-0', 'bytes=-']:
            try:
                urlopen(Request(media, headers={'Range': value}))
            except HTTPError as error:
                assert error.code == 416
                assert error.headers['Content-Range'] == f'bytes */{len(data)}'
            else:
                raise AssertionError(value)
        with urlopen(Request(media, method='HEAD', headers={'Range': 'bytes=1000-1999'})) as response:
            assert response.status == 206 and response.headers['Content-Length'] == '1000'
            assert response.read() == b''
        with urlopen(media) as response:
            assert response.status == 200 and response.read() == data
        results = []
        with sync_playwright() as p:
            executable = next((Path.home() / '.cache/ms-playwright').glob('chromium-*/chrome-linux64/chrome'))
            browser = p.chromium.launch(executable_path=str(executable), headless=True)
            page = browser.new_page()
            page.goto(base + '/' + relative + '/presentation.html')
            page.wait_for_function('window.lessonState && lessonState().loaded')
            page.wait_for_function('!document.getElementById("film").seeking')
            assert page.evaluate('Math.abs(lessonState().time-lessonState().end)') < .05
            page.keyboard.press('ArrowRight')
            for _ in range(12):
                page.keyboard.press('ArrowUp')
            for index in range(5):
                if index == 3:
                    for _ in range(12):
                        page.keyboard.press('ArrowDown')
                    assert page.evaluate('lessonState().speed') == 1
                if index == 4:
                    for _ in range(12):
                        page.keyboard.press('ArrowUp')
                page.wait_for_function('!document.getElementById("film").seeking && lessonState().time>lessonState().start+.5')
                before = page.evaluate('lessonState().time')
                page.wait_for_function('before => lessonState().time>before+1', arg=before, timeout=6000)
                page.wait_for_function("lessonState().state==='held'", timeout=60000)
                page.wait_for_function('!document.getElementById("film").seeking')
                state = page.evaluate('lessonState()')
                assert state['current'] == index
                assert abs(state['time'] - state['end']) < .05, state
                results.append({'scene': index+1, 'speed': state['speed'], 'natural_playback': 'passed', 'correct_hold_frame': 'passed'})
                print('HTTP lesson 1 scene', index+1, 'PASS at', state['speed'], flush=True)
                if index < 4:
                    page.keyboard.press('ArrowRight')
            # Backward seek and replay must start the requested scene rather than frame zero.
            page.keyboard.press('ArrowLeft')
            page.keyboard.press('r')
            page.wait_for_function('!document.getElementById("film").seeking && lessonState().time>lessonState().start+.5')
            assert page.evaluate('lessonState().current') == 3
            browser.close()
        (ROOT / 'http-playback-verification.json').write_text(json.dumps({'byte_range_cases': 'passed', 'lesson_1': results, 'backward_replay': 'passed'}, indent=2)+'\n')
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


if __name__ == '__main__':
    main()
