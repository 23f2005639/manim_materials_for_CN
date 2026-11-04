"""Verify focused animation boundaries without requiring artificial slow motion."""
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from build import episode_paths,read


def main():
    reports=[]
    for path in episode_paths():
        data=read(path);folder=path.parent
        timing=json.loads((folder/'animation-timing.json').read_text())
        deck=json.loads((folder/'sections.json').read_text())
        measured=json.loads((folder/'motion-verification.json').read_text())
        assert timing['edition']=='focused-v2'
        assert len(timing['sections'])==len(deck['sections'])==len(data['sections'])
        for i,(motion,section) in enumerate(zip(timing['sections'],deck['sections'])):
            end=deck['sections'][i+1]['frame'] if i+1<len(deck['sections']) else deck['frames']
            assert section['frame']<motion['animation_end_frame']<end
            assert motion['visual_seconds']>0
        reports.append({'topic':data['topic'],'phases':len(data['sections']),
                        'native_changing_frame_fraction':measured['native_changing_frame_fraction'],
                        'deliberate_holds':'Narration-paced; the player holds after useful motion.'})
        print(data['topic'],'motion boundaries PASS')
    (ROOT/'motion-series-verification.json').write_text(json.dumps(reports,indent=2)+'\n')


if __name__=='__main__':main()
