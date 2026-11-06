"""Resume local assembly as each complete lesson's audio arrives."""
from pathlib import Path
import json,subprocess,time,concurrent.futures
ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'manifest.json').read_text())
started=set();active={}
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 while len(started)<8 or active:
  for e in manifest['episodes']:
   if e['id'] in started:continue
   folder=ROOT/e['folder']
   if (folder/'verification.json').exists():started.add(e['id']);continue
   if len(active)<2 and all((folder/'audio'/f'{i:02}.mp3').exists() for i in range(1,17)):
    def build(e=e):
     with open('/tmp/narrated-build'+e['id']+'.log','w') as log:
      return subprocess.run(['python3',str(ROOT/'assemble.py'),e['id']],stdout=log,stderr=subprocess.STDOUT).returncode
    active[pool.submit(build)]=e['id'];started.add(e['id']);print('Building',e['id'],flush=True)
  for future in list(active):
   if future.done():
    id=active.pop(future);code=future.result();print('Finished',id,'exit',code,flush=True)
    if code:raise RuntimeError('Assembly failed: '+id)
  if len(started)<8 or active:time.sleep(3)
print('All8 narrated movies built',flush=True)
