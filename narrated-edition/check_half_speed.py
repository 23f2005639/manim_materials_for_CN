"""Decoded-frame proof of half-speed video and unchanged normal-speed speech."""
import hashlib,io,json,subprocess,argparse
from pathlib import Path
from PIL import Image,ImageChops,ImageStat
ROOT=Path(__file__).resolve().parent

def frame(path,second):
 raw=subprocess.check_output(['ffmpeg','-v','error','-ss',f'{second:.9f}','-i',str(path),'-frames:v','1','-vf','scale=640:360','-threads','1','-f','image2pipe','-vcodec','png','-'])
 return Image.open(io.BytesIO(raw)).convert('RGB')
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--before',default=str(ROOT/'normal-speed-audio-baseline.json'));args=parser.parse_args()
 before=json.loads(Path(args.before).read_text());reports=[]
 for folder in sorted(ROOT.glob('[0-9][0-9]-*')):
  count_before=len(reports)
  script=json.loads((folder/'script.json').read_text())
  for phase in script['phases']:
   relative=Path('narrated-edition')/folder.name/'clips'/f"{phase['number']:02}.mp4"
   if str(relative) not in before:continue
   out=ROOT.parent/relative;previous=before[str(relative)];audio=folder/'audio'/f"{phase['number']:02}.mp3"
   assert hashlib.sha256(audio.read_bytes()).hexdigest()==previous['audio_source_sha256']
   raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(out),'-t',str(previous['prefix_seconds']),'-vn','-f','s16le','-acodec','pcm_s16le','-'])
   assert hashlib.sha256(raw).hexdigest()==previous['pcm_prefix_sha256'],f'Audio changed: {out}'
   source_time=min(2.0,phase['motion_seconds']*.35)
   old=frame(ROOT.parent/phase['source_clip'],source_time);new=frame(out,source_time*2)
   error=max(ImageStat.Stat(ImageChops.difference(old,new)).mean)
   assert error<.5,(out,error)
   setting=json.loads(out.with_suffix('.render.json').read_text());assert setting['video_speed']==.5 and setting['audio_speed']==1
   reports.append({'episode':folder.name,'clip':phase['number'],'source_audio_sha256':previous['audio_source_sha256'],'normal_speed_audio_pcm':'identical to previous version','half_speed_frame_error':round(error,4)})
  if len(reports)>count_before:print(folder.name,'PASS',flush=True)
 assert len(reports)==41,len(reports)
 (ROOT/'half-speed-verification.json').write_text(json.dumps({'video_speed':.5,'audio_speed':1,'clips_verified':len(reports),'checks':reports},indent=2)+'\n')
 print('PASS:41clips; half-speed frames match source at twice the time; all speech PCM unchanged.')
if __name__=='__main__':main()
