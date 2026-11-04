"""Check the actual local video-only players and keyboard controls in Chromium.

uv run --with playwright python networks/tests/player_check.py [episode number]
"""
import argparse
import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from build import episode_paths


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('episode', nargs='?', type=lambda v: v.zfill(2), choices=[f'{i:02}' for i in range(1, 9)])
    parser.add_argument('--base-url', help='Test the served player, e.g. http://127.0.0.1:8765/networks')
    args = parser.parse_args()
    executable = next((Path.home() / '.cache/ms-playwright').glob('chromium-*/chrome-linux64/chrome'))
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=str(executable), headless=True)
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        for storyboard in episode_paths():
            folder = storyboard.parent
            episode = json.loads(storyboard.read_text())
            if args.episode and episode['id'] != args.episode:
                continue
            if not (folder / 'episode.mp4').exists():
                continue
            errors = []
            on_error = lambda e: errors.append(str(e))
            page.on('pageerror', on_error)
            url = f'{args.base_url.rstrip("/")}/episodes/{folder.name}/presentation.html' if args.base_url else (folder / 'presentation.html').as_uri()
            page.goto(url)
            page.wait_for_function('window.lessonState && lessonState().loaded')
            page.mouse.move(720, 870)
            assert page.locator('button,select,nav,header,details').count() == 0, 'Only the video belongs in the main window'
            assert page.evaluate('document.documentElement.scrollHeight===innerHeight')
            rect = page.locator('#film').bounding_box()
            assert rect['width'] == 1440 and rect['height'] == 900
            assert not page.locator('#film').get_attribute('controls')
            assert page.locator('#error').is_hidden()
            page.keyboard.press('ArrowRight')
            page.wait_for_function("lessonState().state==='playing' && !!document.fullscreenElement")
            page.keyboard.press('ArrowUp')
            page.keyboard.press('ArrowUp')
            assert page.evaluate('lessonState().speed') == 1.5
            page.keyboard.press('ArrowDown')
            assert page.evaluate('lessonState().speed') == 1.25
            page.keyboard.press('ArrowRight')
            page.wait_for_function("lessonState().current===1 && lessonState().state==='playing'")
            assert page.evaluate('lessonState().speed') == 1.25, 'Speed must persist across scenes'
            page.wait_for_function('!document.getElementById("film").seeking && lessonState().time>=lessonState().start')
            page.keyboard.press('p')
            page.wait_for_function("lessonState().state==='paused'")
            paused = page.evaluate('lessonState().time')
            page.wait_for_timeout(100)
            assert abs(page.evaluate('lessonState().time') - paused) < .08
            page.keyboard.press('ArrowRight')
            page.wait_for_function("lessonState().current===2 && lessonState().state==='playing'")
            page.keyboard.press('ArrowLeft')
            assert page.evaluate("lessonState().current===1 && lessonState().state==='ready'")
            page.keyboard.press('r')
            page.wait_for_function("lessonState().state==='playing'")
            assert page.evaluate('lessonState().time-lessonState().start') < 2
            page.keyboard.press('p')
            # Keyboard limits and actual playback rate, rather than a display-only value.
            for _ in range(20):
                page.keyboard.press('ArrowDown')
            assert page.evaluate("document.getElementById('film').playbackRate") == .25
            for _ in range(20):
                page.keyboard.press('ArrowUp')
            assert page.evaluate("document.getElementById('film').playbackRate") == 4
            assert '4×' in page.title()
            page.keyboard.press('p')
            page.wait_for_function("lessonState().state==='playing'")
            # At the fastest supported speed, real playback still stops at this scene.
            page.evaluate("document.getElementById('film').currentTime=lessonState().motionEnd-1")
            page.wait_for_function("lessonState().state==='held'", timeout=5000)
            frozen = page.evaluate('lessonState().time')
            page.wait_for_timeout(150)
            assert abs(page.evaluate('lessonState().time') - frozen) < .04
            assert page.evaluate('Math.abs(lessonState().time-lessonState().end)') < .04
            page.keyboard.press('ArrowRight')
            page.wait_for_function("lessonState().current===2 && lessonState().state==='playing'")
            page.keyboard.press('f')
            page.wait_for_function('!document.fullscreenElement')
            page.keyboard.press('f')
            page.wait_for_function("document.fullscreenElement.id==='app'")
            page.keyboard.press('c')
            assert page.evaluate("document.getElementById('film').textTracks[0].mode") == 'showing'
            page.keyboard.press('c')
            with page.expect_popup() as popup:
                page.keyboard.press('Shift+p')
            presenter = popup.value
            presenter.wait_for_selector('#script')
            expected = json.loads((folder / 'sections.json').read_text())['sections'][2]['notes']
            presenter.wait_for_function('text => document.getElementById("script").textContent===text', arg=expected)
            presenter.keyboard.press('ArrowDown')
            assert page.evaluate('lessonState().speed') == 3.75
            presenter.locator('#scenes').select_option('10')
            assert page.evaluate('lessonState().current') == 10
            presenter.close()
            page.bring_to_front()
            page.keyboard.press('End')
            page.keyboard.press('ArrowRight')
            page.evaluate("document.getElementById('film').currentTime=lessonState().end-.15")
            page.wait_for_function("lessonState().state==='held'", timeout=5000)
            page.keyboard.press('ArrowRight')
            assert page.evaluate("lessonState().current===lessonState().count-1 && lessonState().state==='held'")
            page.keyboard.press('Home')
            page.keyboard.press('ArrowLeft')
            assert page.evaluate('lessonState().current') == 0
            page.keyboard.press('r')
            page.evaluate("document.getElementById('film').currentTime=lessonState().end-.15")
            page.wait_for_function("lessonState().state==='held'", timeout=5000)
            page.screenshot(path=str(folder / 'player-preview.png'))
            assert not errors, errors
            results.append({'episode': folder.name, 'transport': 'http' if args.base_url else 'file', 'video_only': 'passed', 'keyboard_navigation': 'passed',
                            'keyboard_speed_0.25_to_4': 'passed', 'fullscreen': 'passed',
                            'pause_at_boundary': 'passed', 'presenter_notes': 'passed', 'javascript_errors': errors})
            print(folder.name, 'PASS', flush=True)
            page.remove_listener('pageerror', on_error)
        assert len(results) == (1 if args.episode else 8)
        browser.close()
    name = f'browser-verification-{args.episode}.json' if args.episode else 'browser-verification.json'
    (ROOT / name).write_text(json.dumps(results, indent=2) + '\n')


if __name__ == '__main__':
    main()
