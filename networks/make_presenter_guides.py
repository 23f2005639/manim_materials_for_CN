"""Build eight recording companion PDFs from current video timings and authored notes.
Run: uv run --with reportlab --with pypdf python networks/make_presenter_guides.py
"""
from pathlib import Path
import json, subprocess, html, concurrent.futures, io
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/pdf'; TMP=ROOT/'tmp/pdfs'
OUT.mkdir(parents=True,exist_ok=True);TMP.mkdir(parents=True,exist_ok=True)
for name,file in [('Body','DejaVuSans.ttf'),('Bold','DejaVuSans-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+file))
C=colors.HexColor
NAVY=C('#12263b');TEAL=C('#147d91');MUTED=C('#506274');PALE=C('#edf5f7')
W,H=A4; WIDTH=W-84
styles={
 'title':ParagraphStyle('title',fontName='Bold',fontSize=27,leading=34,textColor=NAVY,spaceAfter=20),
 'head':ParagraphStyle('head',fontName='Bold',fontSize=16,leading=21,textColor=NAVY,spaceAfter=10),
 'clip':ParagraphStyle('clip',fontName='Bold',fontSize=12.4,leading=17,textColor=NAVY,spaceAfter=5),
 'body':ParagraphStyle('body',fontName='Body',fontSize=10.3,leading=15,textColor=NAVY,spaceAfter=8),
 'small':ParagraphStyle('small',fontName='Body',fontSize=8.5,leading=12,textColor=MUTED,spaceAfter=6),
 'table':ParagraphStyle('table',fontName='Body',fontSize=9,leading=12,textColor=NAVY),
}
def clean(t):
    return t.replace('\u2013','-').replace('\u2014','-').replace('\u2011','-')
def p(t,style='body'):return Paragraph(clean(t),styles[style])
def esc(t):return html.escape(str(t))
def stamp(t):
    ticks=round(t*10);return f'{ticks//600:02}:{ticks//10%60:02}.{ticks%10}'
def notes():
    result={};topic=None
    for line in (ROOT/'networks/presenter-guide-notes.txt').read_text().splitlines():
        if line.startswith('['):topic=line[1:-1];result[topic]=[]
        elif line.strip():
            row=line.split('|');assert len(row)==3
            result[topic].append(row)
    assert len(result)==8 and all(len(v)==16 for v in result.values())
    return result

def thumbnail(job):
    folder,i,frame=job;target=TMP/f'{folder.name}-{i:02}.jpg'
    if not target.exists():
        subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{frame/30:.9f}','-i',str(folder/'episode.mp4'),'-frames:v','1','-vf','scale=960:540','-threads','1','-q:v','2',str(target)],check=True)
    return target

def build(entry,rows):
    folder=ROOT/'networks'/entry['folder'];data=json.loads((folder/'storyboard.json').read_text());deck=json.loads((folder/'sections.json').read_text())
    sections=data['sections'];assert len(sections)==len(deck['sections'])==len(rows)==16
    output=OUT/f"{data['id']}-{data['topic']}-presenter-guide.pdf"
    jobs=[(folder,i,max(deck['sections'][i]['frame'],s['animation_end_frame']-1)) for i,s in enumerate(deck['sections'])]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:images=list(pool.map(thumbnail,jobs))
    url=f"http://127.0.0.1:8765/networks/{entry['folder']}"
    story=[Spacer(1,25),p(f"VIDEO {data['id']} / YOUR RECORDING COMPANION",'small'),p(esc(data['title']),'title'),p('Explain it in your own words','head'),
       p('Use this guide to understand each animation, choose your phrasing, and keep a natural YouTube delivery. Every clip has a matching frame, the idea behind the movement, and a specific delivery cue.'),
       p(f"<b>16 clips</b> &nbsp; | &nbsp; <b>{stamp(deck['frames']/30)}</b> continuous video &nbsp; | &nbsp; <b>10 guide pages</b>"),Spacer(1,18),
       p('A simple speaking rhythm','head'),
       p('<b>1. Set up:</b> Tell viewers what the objects represent and ask one small question.'),
       p('<b>2. Follow the change:</b> Point to what moves, grows, disappears or gets replaced.'),
       p('<b>3. Explain the cause:</b> Say why that change happened. Use the mechanism notes as your checklist.'),
       p('<b>4. Let it land:</b> Pause on the result, then connect it to the next question.'),Spacer(1,14),
       p('Use the timeline flexibly','head'),
       p('The next page gives exact clip boundaries in the current continuous MP4. Individual clip files begin at 00:00. In the self-paced player, a phase holds until you advance, so your own recording can be longer or shorter. These timestamps describe the video; delivery cues describe how you might explain it.'),
       p('Press Right / Left to move between phases, Up / Down to adjust speed, R to replay, and Shift+P for the separate script window. Rehearse the cause-and-effect in your own words before recording.'),
       p(f'<link href="{url}/presentation.html" color="#147d91">Open this video in the local player</link> &nbsp; | &nbsp; <link href="{url}/narration.md" color="#147d91">Full narration reference</link> &nbsp; | &nbsp; <link href="{url}/references.md" color="#147d91">Sources</link>','small'),PageBreak(),
       p('The complete timeline','head'),p('Find the clip, see the question being explained, and jump to its guide page. Times are MM:SS.t in the full MP4.','small')]
    grid=[[p('<b>CLIP / TIME</b>','table'),p('<b>WHAT YOU ARE EXPLAINING</b>','table'),p('<b>PAGE</b>','table')]]
    for i,s in enumerate(sections):
        start=deck['sections'][i]['frame']/30;end=(deck['sections'][i+1]['frame'] if i<15 else deck['frames'])/30
        grid.append([p(f"<b>{i+1:02}</b><br/>{stamp(start)} - {stamp(end)}",'table'),p(esc(s['short_title']),'table'),p(str(3+i//2),'table')])
    table=Table(grid,colWidths=[143,WIDTH-183,40],repeatRows=1)
    table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),PALE),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,C('#f5f8fa')]),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
    story+=[table,Spacer(1,14),p('Use the clip number as your anchor when recording. Matching frames show the completed diagram; watch the movement too, because the change is often the explanation.','small'),PageBreak()]
    for i,(s,(see,why,tone),img) in enumerate(zip(sections,rows,images,strict=True)):
        start=deck['sections'][i]['frame']/30;end=(deck['sections'][i+1]['frame'] if i<15 else deck['frames'])/30
        clipfile=next((folder/'clips').glob(f'{i+1:02}-*.mp4'))
        meta=f"{stamp(start)} - {stamp(end)} in full video  |  {end-start:.1f}s clip"
        pic=Image(str(img),width=220,height=123.75)
        obs=p('<b>What the viewer sees</b><br/>'+esc(see))
        panel=Table([[pic,obs]],colWidths=[230,WIDTH-230]);panel.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
        transition=('Next: '+sections[i+1]['short_title']) if i<15 else 'Close: return to the opening question and its answer.'
        card=[p(f"CLIP {i+1:02} / {esc(s['short_title'])}",'clip'),p(meta,'small'),panel,
              p('<b>What you need to explain - and why</b><br/>'+esc(why)),
              p('<b>Tone and emphasis</b><br/>'+esc(tone)),
              p(esc(transition),'small'),
              p(f'<link href="{url}/clips/{clipfile.name}" color="#147d91">Open clip {i+1:02}</link> &nbsp; | &nbsp; My phrasing: __________________________________','small')]
        height=sum(x.wrap(WIDTH,1000)[1] for x in card)+sum(getattr(x,'spaceAfter',0) for x in card)
        assert height<345,(data['topic'],i,height)
        story += [KeepTogether(card)]
        if i%2==0:story += [Spacer(1,22)]
        elif i<15:story += [PageBreak()]
    def page(canvas,doc):
        canvas.setStrokeColor(TEAL);canvas.setLineWidth(2);canvas.line(42,H-30,W-42,H-30)
        canvas.setFont('Body',8);canvas.setFillColor(MUTED)
        canvas.drawString(42,23,f"{data['id']} / {data['topic'].upper()} / Presenter guide")
        canvas.drawRightString(W-42,23,f'{doc.page} / 10')
    doc=SimpleDocTemplate(str(output),pagesize=A4,leftMargin=42,rightMargin=42,topMargin=45,bottomMargin=42,title=data['title']+' - Presenter Guide',author='Networks Studio')
    doc.build(story,onFirstPage=page,onLaterPages=page)
    pdf=PdfReader(output);assert len(pdf.pages)==10,(output,len(pdf.pages))
    for i in range(16):
        text=pdf.pages[2+i//2].extract_text();assert f'CLIP {i+1:02}' in text
        assert clean(rows[i][1]) in text.replace('\n',' ') or ' '.join(clean(rows[i][1]).split()) in ' '.join(text.split())
    print(output.relative_to(ROOT),'10 pages,16 clips verified',flush=True)
    return {'id':data['id'],'topic':data['topic'],'file':output.name,'pages':10,'clips':16,'timings':'current sections.json at 30fps','frames':'decoded current MP4'}

def main():
    authored=notes();series=json.loads((ROOT/'networks/series.json').read_text());reports=[]
    for entry in series['episodes']:reports.append(build(entry,authored[entry['topic']]))
    (OUT/'verification.json').write_text(json.dumps(reports,indent=2)+'\n')
    items=''.join(f'<li><a href="{r["file"]}">{r["id"]}. {r["topic"].replace("-"," ").title()}</a> - 16 clips, 10 pages</li>' for r in reports)
    (OUT/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Video presenter guides</title><style>body{font:18px/1.7 system-ui;max-width:820px;margin:50px auto;padding:24px;background:#f4f8fa;color:#12263b}a{color:#147d91}</style><h1>Your video presenter guides</h1><p>Each PDF includes a complete timeline, a matching frame for every clip, explanations of what happens and why, delivery cues, and room for your own phrasing.</p><ol>'+items+'</ol><p>Times match the continuous videos; your live narration can follow your own pace.</p><a href="../../networks/">Back to videos</a>')
if __name__=='__main__':main()
