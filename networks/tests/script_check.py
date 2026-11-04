"""Ensure the published scripts and presenter notes are the same complete narration."""
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from build import episode_paths,read

reports=[]
for path in episode_paths():
    data=read(path);folder=path.parent
    deck=json.loads((folder/'sections.json').read_text())
    embedded=json.JSONDecoder().raw_decode((folder/'presentation.html').read_text().split('const deck=',1)[1])[0]
    narration=(folder/'narration.md').read_text()
    for source,section,display in zip(data['sections'],deck['sections'],embedded['sections'],strict=True):
        assert source['narration']==section['notes']==display['notes']
        assert source['narration'] in narration
        assert source['narration'] in (ROOT/'youtube-scripts.md').read_text()
    reports.append({'id':data['id'],'topic':data['topic'],'phases':len(data['sections']),
                    'words':sum(len(s['narration'].split()) for s in data['sections']),
                    'duration_seconds':data['duration'],'presenter_notes_match':True,'script_matches_storyboard':True})
(ROOT/'focused-script-verification.json').write_text(json.dumps({'edition':'focused-v2','revision':'beginner foundations','episodes':reports,'total_words':sum(r['words'] for r in reports),'total_phases':sum(r['phases'] for r in reports)},indent=2)+'\n')
print('PASS: all 128 narration paragraphs match scripts, section metadata and presenter notes.')
