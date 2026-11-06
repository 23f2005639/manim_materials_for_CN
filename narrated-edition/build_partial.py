from pathlib import Path
import json,concurrent.futures
from assemble import clip,run,ROOT,index
folder=ROOT/'03-wdm';script=json.loads((folder/'script.json').read_text())
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 rows=list(pool.map(lambda p:clip(folder,p),script['phases'][:9]))
(folder/'partial-concat.txt').write_text(''.join(f"file 'clips/{r['number']:02}.mp4'\n" for r in rows))
run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(folder/'partial-concat.txt'),'-c','copy','-movflags','+faststart',str(folder/'preview.mp4')])
(folder/'partial-timing.json').write_text(json.dumps(rows,indent=2)+'\n')
index(json.loads((ROOT/'manifest.json').read_text()))
print('WDM preview:9of16clips',flush=True)
