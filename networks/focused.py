"""Narration-paced topic films; deliberate holds never slow down object motion."""
import importlib
import json
import manimgx as m

TOPICS=('dns','bufferbloat','wdm','packet-switching','dijkstra','subnetting','tcp-slow-start','rsa')


def construct(scene,data):
    topic=data['topic']
    if topic not in TOPICS:raise ValueError(f'Unknown focused topic: {topic}')
    cls=importlib.import_module('networks.motion.topics.'+topic.replace('-','_')).Director
    director=cls(scene);title=None;target=0;motion=[];fps=float(m.config.frame_rate)
    for index,section in enumerate(data['sections']):
        start=scene.time
        scene.next_section(section['title'],notes=section['narration'])
        director.reset()
        heading=m.Text(section['short_title'],font='Noto Sans',font_size=34,color='#F2F2F2')
        if heading.width>12.5:heading.scale(12.5/heading.width)
        heading.move_to([0,3.27,0])
        if isinstance(scene,m.ThreeDScene):
            scene.camera.add_fixed_in_frame_mobjects(heading)
        if title is None:
            title=heading;scene.play(m.FadeIn(title),run_time=.4)
        else:scene.play(m.Transform(title,heading),run_time=.4)
        target+=section['duration'];end=round(target*fps)/fps
        budget=end-scene.time-.75
        began=scene.time
        director.animate(index,section,budget)
        if scene.time>end+.05:raise ValueError(f'{section["id"]} exceeds its section duration')
        if scene.time<end:scene.wait(end-scene.time)
        elapsed=max(0,director.motion_end-began)
        motion.append({'name':section['title'],'animation_end_frame':round(director.motion_end*fps),
                       'section_seconds':round(end-start,3),'visual_seconds':round(elapsed,3),
                       'visual_fraction':round(elapsed/(end-start),3)})
    scene.storyboard_path.with_name('animation-timing.json').write_text(json.dumps({
        'fps':fps,'sections':motion,'duration':scene.time,'edition':'focused-v2'},indent=2)+'\n')
