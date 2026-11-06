from pathlib import Path
import json,hashlib,subprocess,urllib.request,io
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent
exe=next((Path.home()/'.cache/ms-playwright').glob('chromium-*/chrome-linux64/chrome'))
reports=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=str(exe),headless=True)
 page=browser.new_page(viewport={'width':1440,'height':810})
 for folder in (ROOT/'01-dns',ROOT/'02-bufferbloat'):
  data=json.loads((folder/'timing.json').read_text());deck=json.loads((folder/'sections.json').read_text())
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:8765/narrated-edition/'+folder.name+'/presentation.html')
  page.wait_for_function('window.lessonState && lessonState().loaded')
  assert page.locator('button,nav,header,select').count()==0
  assert page.evaluate('!document.querySelector("video").muted')
  assert page.evaluate('lessonState().count')==16
  page.keyboard.press('ArrowRight');page.wait_for_function('lessonState().state==="playing" && !!document.fullscreenElement')
  page.wait_for_timeout(700)
  page.keyboard.press('ArrowUp');assert page.evaluate('lessonState().speed')==1.25
  page.keyboard.press('ArrowDown');assert page.evaluate('lessonState().speed')==1
  page.keyboard.press('p');page.wait_for_function('lessonState().state==="paused"')
  page.keyboard.press('ArrowRight');page.wait_for_function('lessonState().current===1 && lessonState().state==="playing"')
  page.keyboard.press('ArrowLeft');assert page.evaluate('lessonState().current')==0
  page.keyboard.press('r');page.wait_for_function('lessonState().state==="playing"')
  page.evaluate('document.querySelector("video").currentTime=lessonState().motionEnd-.15')
  page.wait_for_function('lessonState().state==="held"',timeout=5000)
  assert page.evaluate('lessonState().time')>data[0]['speech_seconds']+.3
  page.screenshot(path=str(folder/'player-preview.png'))
  page.keyboard.press('f');page.wait_for_function('!document.fullscreenElement')
  assert not errors,errors
  for i,t in enumerate(data):
   assert t['duration']>=t['speech_seconds']+.7
   boundary=deck['sections'][i]['frame']
   assert deck['sections'][i]['animation_end_frame']==boundary+t['frames']-1
  reports.append({'episode':folder.name,'keyboard_fullscreen_speed_pause_replay':'passed','unmuted_audio':'passed','hold_after_narration':'passed','no_visible_toolbar':'passed','all16speech_durations_fit':True})
 browser.close()
for name,digest in json.loads((ROOT/'source-hashes.json').read_text()).items():assert hashlib.sha256((ROOT.parent/name).read_bytes()).hexdigest()==digest,name
(ROOT/'browser-verification.json').write_text(json.dumps(reports,indent=2)+'\n')
print('PASS:2narrated players,32clips,full narration fits; all original episode hashes unchanged.')
