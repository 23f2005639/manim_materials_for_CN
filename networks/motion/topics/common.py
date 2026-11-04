"""Small drawing helpers and explicit scene ownership for focused explainers."""
import math
import numpy as np
import manimgx as m

BG='#080A10'; BLUE='#58C4DD'; GREEN='#83C167'; YELLOW='#FFFF00'; RED='#FC6255'
WHITE='#F2F2F2'; MUTED='#8B93A6'; PURPLE='#B39DDB'


def text(value,x=0,y=0,size=26,color=WHITE,width=12):
    obj=m.Text(str(value),font='Noto Sans',font_size=size,color=color)
    if obj.width>width:obj.scale(width/obj.width)
    return obj.move_to([x,y,0]).set_z_index(5)


def line(a,b,color=MUTED,width=2):
    return m.Line([*a,0],[*b,0],color=color,stroke_width=width)


def packet(value,color=BLUE,width=None,height=.48):
    if width is None:width=max(.7,min(3.4,.13*len(str(value))+.4))
    return m.VGroup(m.Rectangle(width=width,height=height,color=color,stroke_width=2,
                     fill_color=BG,fill_opacity=1),text(value,size=21,color=color,width=width-.12)).set_z_index(6)


def host(value,x,y,color=BLUE):
    return m.VGroup(m.Circle(radius=.35,color=color,stroke_width=2.5,fill_color=BG,fill_opacity=1).move_to([x,y,0]),
                    text(value,x,y+.62,24,color,2.6))


class VisualDirector:
    def __init__(self,scene):
        self.s=scene;self.objects=[];self._began=scene.time;self.motion_end=scene.time

    def reset(self):
        # Scene.remove can split groups; explicitly remove all owned descendants.
        self.s.remove(*(member for obj in self.objects for member in obj.get_family()))
        self.objects=[];self._began=self.s.time;self.motion_end=self.s.time

    def own(self,obj):
        self.objects.append(obj)
        return obj

    def play(self,*animations,run_time=1,**kwargs):
        self.s.play(*animations,run_time=run_time,**kwargs)
        self.motion_end=self.s.time

    def wait(self,seconds):
        self.s.wait(seconds)

    def finish(self,budget):
        remaining=budget-(self.s.time-self._began)
        if remaining<-.05:raise ValueError(f'Animation exceeds phase budget by {-remaining:.2f}s')
        if remaining>0:self.s.wait(remaining)
