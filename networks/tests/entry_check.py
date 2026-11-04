"""Check the published index points to exactly the active series and opens its player."""
import json
from pathlib import Path
import sys
from urllib.request import urlopen
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from build import episode_paths


def main():
    base='http://127.0.0.1:8765/networks/'
    paths=episode_paths()
    with sync_playwright() as p:
        executable=next((Path.home()/'.cache/ms-playwright').glob('chromium-*/chrome-linux64/chrome'))
        browser=p.chromium.launch(executable_path=str(executable),headless=True)
        page=browser.new_page(viewport={'width':1440,'height':900})
        errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto(base)
        cards=page.locator('a.card')
        assert cards.count()==8
        assert cards.evaluate_all('(cards)=>cards.map(c=>c.getAttribute("href"))')==[
            f'{path.parent.relative_to(ROOT).as_posix()}/presentation.html' for path in paths]
        page.screenshot(path=str(ROOT/'series-preview.png'),full_page=True)
        cards.first.click()
        page.wait_for_function('window.lessonState && lessonState().loaded')
        assert page.locator('button,header,nav').count()==0
        page.keyboard.press('ArrowRight')
        page.wait_for_function("lessonState().state==='playing' && !!document.fullscreenElement")
        with page.expect_popup() as popup:page.keyboard.press('Shift+p')
        notes=popup.value;notes.wait_for_selector('#script')
        expected=json.loads(paths[0].read_text())['sections'][0]['narration']
        assert notes.locator('#script').text_content()==expected
        notes.close();browser.close()
        assert not errors,errors
    for path in paths:
        for name in ('narration.md','references.md','clips/index.html'):
            with urlopen(base+path.parent.relative_to(ROOT).as_posix()+'/'+name) as r:assert r.status==200
    for name in ('youtube-scripts.md','legacy-index.html','legacy-scripts.md'):
        with urlopen(base+name) as r:assert r.status==200
    (ROOT/'entry-verification.json').write_text(json.dumps({'active_cards':8,'index_to_fullscreen_to_notes':'passed',
        'scripts_references_clip_indexes':'passed','legacy_links':'passed','javascript_errors':errors},indent=2)+'\n')
    print('PASS: published index → active video → fullscreen → correct presenter notes; all asset links work.')


if __name__=='__main__':main()
