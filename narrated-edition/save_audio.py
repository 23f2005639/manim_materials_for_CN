"""Download completed MCP assets from a temporary JSON list; no API keys required."""
import json,sys,urllib.request,concurrent.futures,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def save(data):
 def fetch(d):
  folder=ROOT/(d['episode']+'-'+d['topic']);p=folder/'takes'/f"{d['phase']:02}-take{d['take']}.mp3"
  if not p.exists():urllib.request.urlretrieve(d['url'],p)
 with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:list(pool.map(fetch,data))
 for ep in {d['episode']+'-'+d['topic'] for d in data}:
  folder=ROOT/ep;selection=folder/'selected-takes.json';chosen=json.loads(selection.read_text()) if selection.exists() else {}
  for n in range(1,17):
   audio=folder/'audio'/f'{n:02}.mp3'
   if audio.exists():chosen.setdefault(str(n),1);continue
   takes=sorted((folder/'takes').glob(f'{n:02}-take*.mp3'))
   if takes:
    shutil.copyfile(takes[0],audio);chosen[str(n)]=int(takes[0].stem[-1])
  selection.write_text(json.dumps(chosen,indent=2)+'\n')
 return len(data)
if __name__=='__main__':print('Saved',save(json.loads(Path(sys.argv[1]).read_text())),'completed takes')
