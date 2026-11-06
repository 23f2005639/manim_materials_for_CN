"""Mux saved narration onto original Manim clips, preserving original project files."""
from pathlib import Path
import json,subprocess,math,html,re,hashlib,argparse,concurrent.futures
ROOT=Path(__file__).resolve().parent;PROJECT=ROOT.parent
FPS=30
VIDEO_SPEED=0.5

def probe(path):
 return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
def run(cmd):
 r=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 if r.returncode:raise RuntimeError(r.stderr.decode()[-2000:])
def clip(folder,phase):
 n=phase['number'];audio=folder/'audio'/f'{n:02}.mp3';out=folder/'clips'/f'{n:02}.mp4'
 assert audio.exists(),audio
 ad=float(probe(audio)['format']['duration']);duration=math.ceil(max(ad+.75,phase['motion_seconds']/VIDEO_SPEED+.75)*FPS)/FPS
 frames=round(duration*FPS)
 settings={'video_speed':VIDEO_SPEED,'audio_speed':1.0,'video_source_mtime_ns':(PROJECT/phase['source_clip']).stat().st_mtime_ns,'audio_mtime_ns':audio.stat().st_mtime_ns}
 stamp=out.with_suffix('.render.json')
 if not out.exists() or not stamp.exists() or json.loads(stamp.read_text())!=settings:
  temporary=out.with_suffix('.part')
  run(['ffmpeg','-v','error','-y','-i',str(PROJECT/phase['source_clip']),'-i',str(audio),'-filter_complex',
       f'[0:v]setpts=(PTS-STARTPTS)/{VIDEO_SPEED},fps=30,tpad=stop_mode=clone:stop_duration=120[v];[1:a]adelay=300:all=1,loudnorm=I=-16:TP=-1.5:LRA=11,apad[a]',
       '-map','[v]','-map','[a]','-frames:v',str(frames),'-t',str(duration),'-c:v','libx264','-preset','veryfast','-crf','20','-threads','2','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-ac','2','-movflags','+faststart','-f','mp4',str(temporary)])
  temporary.replace(out)
  stamp.write_text(json.dumps(settings,indent=2)+'\n')
 v=next(s for s in probe(out)['streams'] if s['codec_type']=='video')
 assert int(v['nb_frames'])==frames,(out,v['nb_frames'],frames)
 assert (v['width'],v['height'])==(1920,1080)
 return {'number':n,'duration':duration,'frames':frames,'speech_seconds':ad,'video_speed':VIDEO_SPEED,'audio_speed':1.0,'title':phase['title'],'text':phase['text'],'file':f'clips/{n:02}.mp4'}
def build(ep):
 folder=ROOT/ep['folder'];script=json.loads((folder/'script.json').read_text())
 if any(not (folder/'audio'/f'{i:02}.mp3').exists() for i in range(1,17)):return False
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:timings=list(pool.map(lambda p:clip(folder,p),script['phases']))
 concat=folder/'concat.txt';concat.write_text(''.join(f"file 'clips/{t['number']:02}.mp4'\n" for t in timings))
 movie=folder/'episode.mp4'
 if not movie.exists() or any((folder/t['file']).stat().st_mtime_ns>movie.stat().st_mtime_ns for t in timings):run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(concat),'-c','copy','-movflags','+faststart',str(movie)])
 deck={'fps':FPS,'frames':sum(t['frames'] for t in timings),'sections':[],'captions':[],'title':script['title']+' / narrated'}
 start=0
 for t in timings:
  deck['sections'].append({'name':t['title'],'id':f"{ep['id']}-{t['number']:02}",'frame':start,'animation_end_frame':start+t['frames']-1,'notes':t['text'],'type':'default.normal','chapter':'Narrated lesson'})
  words=t['text'].split();chunks=[' '.join(words[i:i+10]) for i in range(0,len(words),10)]
  for i,c in enumerate(chunks):deck['captions'].append([start/FPS+.3+t['speech_seconds']*i/len(chunks),start/FPS+.3+t['speech_seconds']*(i+1)/len(chunks),c])
  start+=t['frames']
 (folder/'sections.json').write_text(json.dumps(deck,indent=2)+'\n')
 (folder/'timing.json').write_text(json.dumps(timings,indent=2)+'\n')
 template=(PROJECT/'networks/templates/player.html').read_text()
 template=template.replace('__TITLE__',html.escape(script['title']+' / narrated')).replace('__DECK__',json.dumps(deck).replace('</','<\\/')).replace('__MEDIA_VERSION__',str(movie.stat().st_mtime_ns))
 (folder/'presentation.html').write_text(template)
 info=probe(movie);video=next(s for s in info['streams'] if s['codec_type']=='video');sound=next(s for s in info['streams'] if s['codec_type']=='audio')
 assert int(video['nb_frames'])==deck['frames']
 assert abs(float(video['duration'])-deck['frames']/FPS)<.05
 assert sound['codec_name']=='aac'
 report={'episode':ep['id'],'phases':16,'resolution':'1920x1080','fps':30,'video_codec':video['codec_name'],'audio_codec':sound['codec_name'],'duration_seconds':float(info['format']['duration']),'audio_present':True,'video_speed':VIDEO_SPEED,'audio_speed':1.0,'narration_fit':'Per clip;0.3s lead plus full unchanged-speed speech; animation runs at half speed','caption_timing':'Guide timings proportional to text; not forced word alignment','source_files_preserved':True}
 (folder/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(ep['id'],'complete',report['duration_seconds'],flush=True)
 return True

def index(manifest):
 rows=[]
 for e in manifest['episodes']:
  f=ROOT/e['folder'];ready=(f/'verification.json').exists()
  links=(f'<a href="{e["folder"]}/presentation.html">Self-paced narrated player</a> · <a href="{e["folder"]}/episode.mp4">Full video</a>') if ready else ('Partial: <a href="'+e['folder']+'/preview.mp4">watch clips1-9</a>; remaining audio awaits ElevenLabs credits' if (f/'preview.mp4').exists() else 'Script ready; audio awaits ElevenLabs credits')
  rows.append(f'<article><h2>{e["id"]}. {html.escape(e["topic"].replace("-"," ").title())}</h2><p>{links}</p><p><a href="{e["folder"]}/script.md">Script</a> · <a href="{e["folder"]}/takes/">Alternative voice takes</a></p></article>')
 (ROOT/'index.html').write_text('<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Networks / Narrated Edition</title><style>body{background:#080a10;color:#edf4ff;font:18px/1.7 system-ui;max-width:1000px;margin:50px auto;padding:24px}a{color:#58c4dd}article{border:1px solid #29384a;padding:18px;margin:18px 0}h2{margin:0}</style><h1>Networks: the narrated edition</h1><p>David - Clear, Friendly Explainer. Original Manim animations, natural male teaching narration, purposeful pauses. Animation:0.5×; narration:normal speed. Each complete topic has16phases. Production paused at the ElevenLabs account credit quota; see the status shown for each topic.</p><p>Right / Left: scenes. Up / Down: speed. P: pause. R: replay. Full videos play continuously. Guide captions use approximate timing.</p>'+''.join(rows))

def main():
 parser=argparse.ArgumentParser();parser.add_argument('episode',nargs='?',default='all');args=parser.parse_args()
 manifest=json.loads((ROOT/'manifest.json').read_text())
 for e in manifest['episodes']:
  if args.episode=='all' or e['id']==args.episode:build(e)
 index(manifest)
 for name,h in json.loads((ROOT/'source-hashes.json').read_text()).items():assert hashlib.sha256((PROJECT/name).read_bytes()).hexdigest()==h,name
if __name__=='__main__':main()
