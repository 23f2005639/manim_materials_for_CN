"""Persistent, causal full-canvas animations for routing, subnetting, and cryptography.

These are mathematical teaching models. The cryptographic glyph transforms are
illustrations, never implementations of encryption algorithms.
"""
from __future__ import annotations

import math
import numpy as np
import manimgx as m

BG='#080A10'; BLUE='#58C4DD'; GREEN='#83C167'; YELLOW='#FFFF00'; RED='#FC6255'; WHITE='#F2F2F2'; GRAY='#687080'


def text(value, x=0, y=0, size=25, color=WHITE, width=12):
    t=m.Text(str(value),font='Noto Sans',font_size=max(23,size),color=color)
    if t.width>width:t.scale(width/t.width)
    return t.move_to([x,y,0]).set_z_index(5)


def pill(value,x,y,color=WHITE,width=1.1,height=.53,size=23):
    return m.VGroup(m.RoundedRectangle(width=width,height=height,corner_radius=.08,
                    color=color,stroke_width=1.6,fill_color=BG,fill_opacity=1).move_to([x,y,0]),
                    text(value,x,y,size,color,width-.12)).set_z_index(4)


def line(a,b,color=GRAY,width=2):
    return m.Line([*a,0],[*b,0],color=color,stroke_width=width)


def arrow(a,b,color=BLUE):
    return m.Arrow([*a,0],[*b,0],buff=.08,color=color,stroke_width=2.5,
                   max_tip_length_to_length_ratio=.1)


def cross(x,y,size=.18):
    return m.VGroup(line((x-size,y-size),(x+size,y+size),RED,3),
                    line((x-size,y+size),(x+size,y-size),RED,3))


def key(x,y,color=YELLOW,label='K'):
    ring=m.Circle(radius=.18,color=color,stroke_width=3).move_to([x-.24,y,0])
    shaft=line((x-.06,y),(x+.43,y),color,3)
    teeth=m.VGroup(line((x+.2,y),(x+.2,y-.17),color,3),line((x+.38,y),(x+.38,y-.17),color,3))
    return m.VGroup(ring,shaft,teeth,text(label,x,y-.43,18,color,1.6))


class SystemsDirector:
    def __init__(self,scene,episode_id):
        self.s=scene;self.episode=str(episode_id).zfill(2)
        self.kind=None;self.world=[];self.temp=[];self.steps=[]
        self.nodes={};self.edges={};self.weights={};self.distance={}
        self.bits=[];self.boundary=None;self.block=None;self.blocks=[];self.current_byte=0;self.scan=None

    def q(self,*animations,weight=1,after=None):
        if not animations:return
        def action(duration,animations=animations,after=after):
            self.s.play(*animations,run_time=duration)
            if after:after()
        self.steps.append((weight,action))

    def own(self,obj,*,temporary=False,animation=None,weight=.65):
        (self.temp if temporary else self.world).append(obj)
        self.q(animation or m.FadeIn(obj),weight=weight)
        return obj

    def remove_temporary(self):
        if self.temp:
            old=list(self.temp);self.temp=[]
            self.q(m.FadeOut(m.Group(*old)),weight=.25,after=lambda:self.s.remove(*old))

    def clear(self,kind):
        if self.kind==kind:return
        if self.world:
            old=list(self.world)
            self.q(m.FadeOut(m.Group(*old)),weight=.5,after=lambda:self.s.remove(*old))
        self.world=[];self.kind=kind
        self.nodes={};self.edges={};self.weights={};self.distance={}
        self.bits=[];self.boundary=None;self.blocks=[];self.block=None;self.scan=None

    def equation(self,value,color=YELLOW,y=-2.5):
        obj=text(value,0,y,27,color,12)
        return self.own(obj,temporary=True,animation=m.Write(obj))

    def fade(self,obj,weight=.3):
        self.temp=[item for item in self.temp if item is not obj]
        self.q(m.FadeOut(obj),weight=weight,after=lambda:self.s.remove(obj))

    def token(self,a,b=None,label='',color=YELLOW,weight=1,keep=False):
        token=m.VGroup(m.Dot([*a,0],radius=.085,color=color),text(label,a[0],a[1]+.3,17,color,2))
        self.own(token,temporary=True,weight=.3)
        if b is not None:
            self.q(token.animate.shift(np.array([b[0]-a[0],b[1]-a[1],0])),weight=weight)
            if not keep:self.fade(token,.2)
        return token

    def route(self,path,color=YELLOW,weight=1):
        p=self.P
        token=self.token(p[path[0]],label='',color=color)
        for a,b in zip(path,path[1:]):
            trail=line(p[a],p[b],color,3.7)
            self.own(trail,temporary=True,animation=m.Create(trail),weight=.2)
            self.q(token.animate.move_to([*p[b],0]),weight=weight)
        self.fade(token,.2)
        return token

    def graph(self):
        if self.kind=='graph':return
        self.clear('graph')
        self.P={'A':(-5.2,0),'B':(-2.6,1.35),'C':(-2.6,-1.25),'D':(.8,1.35),'E':(.8,-1.25),'F':(4.7,0)}
        self.E=[('A','B',4),('A','C',2),('B','C',1),('B','D',5),('C','D',8),('C','E',10),('D','E',2),('D','F',6),('E','F',3)]
        for a,b,w in self.E:
            edge=line(self.P[a],self.P[b],GRAY,2)
            self.edges[(a,b)]=edge
            self.own(edge,animation=m.Create(edge),weight=.18)
            x=(self.P[a][0]+self.P[b][0])/2;y=(self.P[a][1]+self.P[b][1])/2
            if (a,b)==('C','D'):x+=.3;y+=.25
            weight=pill(w,x,y,WHITE,.65,.43,23)
            self.weights[(a,b)]=weight;self.own(weight,weight=.12)
        for n,p in self.P.items():
            obj=self.node(n,'∞',BLUE)
            self.nodes[n]=obj;self.distance[n]='∞';self.own(obj,weight=.35)

    def node(self,n,d,color):
        x,y=self.P[n]
        return m.VGroup(m.Circle(radius=.32,color=color,fill_color=BG,fill_opacity=1,stroke_width=2).move_to([x,y,0]),
                        text(n,x,y,26,color),pill(d,x,y+.59,color,.9,.43,30)).set_z_index(5)

    def set_distance(self,n,value,color=BLUE,weight=.8):
        self.distance[n]=value
        self.q(m.Transform(self.nodes[n],self.node(n,value,color)),weight=weight)

    def relax(self,a,b,cost,value):
        token=self.token(self.P[a],label=str(cost),color=YELLOW)
        self.q(token.animate.move_to([*self.P[b],0]),weight=1.3)
        self.set_distance(b,value,YELLOW,weight=.9)
        self.fade(token,.3)

    def routing(self,i,v):
        if i in (13,14,19,20):
            self.routing_vector(i,v);return
        if i==22:
            self.routing_hierarchy();return
        self.graph()
        if i==0:
            self.route(['A','B','D','F'],RED,.8)
            self.equation('4 + 5 + 6 = 15',RED)
            self.route(['A','C','B','D','E','F'],GREEN,.7)
            return
        if i==1:
            # Reveal the graph as the mathematical abstraction of the network.
            for a,b,w in self.E:
                e=self.edges[(a,b)]
                self.q(e.animate.set_stroke(BLUE,width=3.5),weight=.6)
                self.q(m.Transform(self.weights[(a,b)],pill(w,*self.weights[(a,b)].get_center()[:2],YELLOW,.45,.33,17)),weight=.4)
            return
        if i==2:
            self.route(['A','B','D','F'],RED,.7)
            eq=self.equation('4',RED)
            for value in ('4 + 5 = 9','4 + 5 + 6 = 15'):
                self.q(m.Transform(eq,text(value,0,-2.5,30,RED)),weight=1)
            self.route(['A','C','B','D','E','F'],GREEN,.6)
            self.q(m.Transform(eq,text('2 + 1 + 5 + 2 + 3 = 13',0,-2.5,30,GREEN)),weight=1.2)
            return
        if i==3:
            for a,b,w in self.E:self.q(self.edges[(a,b)].animate.set_stroke(BLUE,width=2.5),weight=.25)
            self.equation('F  →  next hop C',GREEN)
            self.route(['A','C','B','D','E','F'],GREEN,1)
            return
        if i==4:
            for n in self.P:self.set_distance(n,0 if n=='A' else '∞',BLUE,weight=.6)
            self.equation('d(A)=0     d(other)=∞')
            return
        if 5<=i<=10:
            stage={5:('A',0,[('B',4,4),('C',2,2)]),6:('C',2,[('B',1,3),('D',8,10),('E',10,12)]),
                   7:('B',3,[('D',5,8)]),8:('D',8,[('E',2,10),('F',6,14)]),
                   9:('E',10,[('F',3,13)]),10:('F',13,[])}[i]
            a,d,neighbors=stage;self.set_distance(a,d,GREEN,weight=.7)
            for b,cost,result in neighbors:
                eq=self.equation(f'{d} + {cost} = {result}')
                self.relax(a,b,cost,result)
                self.fade(eq,.2)
            if not neighbors:
                for n,d in {'A':0,'C':2,'B':3,'D':8,'E':10,'F':13}.items():self.set_distance(n,d,GREEN,.4)
                self.route(['A','C','B','D','E','F'],GREEN,.7)
            return
        if i==11:
            for a,b in zip(['F','E','D','B','C'],['E','D','B','C','A']):
                self.token(self.P[a],self.P[b],label='predecessor',color=GREEN,weight=1)
            self.equation('A → C → B → D → E → F     13',GREEN)
            return
        if i==12:
            self.equation('F  →  C',GREEN)
            for e in [('A','B'),('A','C')]:self.q(self.edges[e].animate.set_stroke(GREEN if e[1]=='C' else GRAY,width=4 if e[1]=='C' else 1),weight=.5)
            self.route(['A','C','B','D','E','F'],GREEN,1)
            return
        if i in (15,16):
            self.equation('Link facts → shared map → shortest paths',BLUE)
            paths=[['D','B','A'],['D','E','C','A'],['D','F']]
            for j,path in enumerate(paths):self.route(path,[BLUE,YELLOW,GREEN][j],.75)
            for n,d in {'A':0,'B':3,'C':2,'D':8,'E':10,'F':13}.items():self.set_distance(n,d,GREEN,.3)
            return
        if i in (17,18):
            edge=self.edges[('D','E')]
            self.q(edge.animate.set_color(RED),weight=.6)
            mark=cross(.8,.05,.23);self.own(mark,temporary=True,weight=.4)
            self.set_distance('E','∞',RED,.6);self.set_distance('F','∞',RED,.6)
            self.route(['A','C','B','D','F'],GREEN,1)
            self.set_distance('E',12,GREEN,.7);self.set_distance('F',14,GREEN,.7)
            self.equation('2 + 1 + 5 + 6 = 14',GREEN)
            return
        if i==21:
            self.equation('Configured cost changes the best path',BLUE)
            w=self.weights[('B','D')];self.q(m.Transform(w,pill(20,*w.get_center()[:2],RED,.6,.4,20)),weight=1)
            self.route(['A','C','E','F'],GREEN,1)
            self.equation('2 + 10 + 3 = 15',GREEN,y=-2.1)
            return
        # Recap restores the original costs before replaying the two valid outcomes.
        w=self.weights[('B','D')];self.q(m.Transform(w,pill(5,*w.get_center()[:2],WHITE,.45,.33,17)),weight=.7)
        self.q(self.edges[('D','E')].animate.set_color(GRAY),weight=.4)
        self.route(['A','C','B','D','E','F'],GREEN,.8)
        self.set_distance('F',13,GREEN,.5)
        self.q(self.edges[('D','E')].animate.set_color(RED),weight=.5)
        self.route(['A','C','B','D','F'],YELLOW,.8)
        self.set_distance('F',14,YELLOW,.5)

    def routing_vector(self,i,v):
        self.clear(f'vector-{i}')
        a=(-4,0);b=(2.7,1.2);c=(2.7,-1.2)
        for name,pos,color in [('A',a,BLUE),('B',b,YELLOW),('C',c,GREEN)]:self.own(pill(name,*pos,color,1.1,.8,30),weight=.3)
        if i in (13,14):
            self.own(line(a,b,YELLOW),weight=.3)
            self.own(line(a,c,GREEN),weight=.3)
            self.token(b,a,'10',YELLOW,1.1);self.token(c,a,'11',GREEN,1.1)
            e1=self.equation('4 + 10 = 14',YELLOW,y=-2.3)
            self.q(m.Transform(e1,text('min(4 + 10, 2 + 11) = 13',0,-2.3,30,GREEN)),weight=1)
            self.token(a,c,'F',GREEN,1.3)
        elif i==19:
            dead=cross(*b,.4);self.own(dead,temporary=True,weight=.5)
            estimate=self.own(pill('3',0,0,YELLOW,1.1,.8,35),temporary=True,weight=.4)
            for value in (4,5,6,8,12,16):
                self.token(a,c,str(value-1),YELLOW,.65)
                self.q(m.Transform(estimate,pill(str(value),0,0,RED if value==16 else YELLOW,1.1,.8,35)),weight=.5)
                self.token(c,a,str(value),RED if value==16 else YELLOW,.65)
            self.equation('RIP: 16 = unreachable',RED)
        else:
            self.token(c,a,'route to F',GREEN,1.1)
            self.token(a,c,'∞',RED,1.1)
            stop=cross(-.5,-.6,.3);self.own(stop,temporary=True,weight=.5)
            self.equation('Learn through C → advertise ∞ back to C',RED)
            self.token(a,(-.5,-.6),'F',RED,1)

    def routing_hierarchy(self):
        self.graph()
        left=m.Circle(radius=2.2,color=BLUE,stroke_width=2).stretch(.85,1).move_to([-3.5,.1,0])
        right=m.Circle(radius=2.2,color=GREEN,stroke_width=2).stretch(.85,1).move_to([2.5,.1,0])
        self.own(left,temporary=True,animation=m.Create(left),weight=1)
        self.own(right,temporary=True,animation=m.Create(right),weight=1)
        self.equation('Many routers → fewer advertised regions',BLUE)
        old=list(self.world);self.world=[];self.kind='hierarchy'
        self.q(m.FadeOut(m.Group(*old)),weight=.8,after=lambda:self.s.remove(*old))
        self.q(m.Transform(left,pill('Area 1',-3,.1,BLUE,2,1,30)),m.Transform(right,pill('Area 2',3,.1,GREEN,2,1,30)),weight=1.5)
        self.token((-3,.1),(3,.1),'prefix',YELLOW,1.5)

    def bitcell(self,value,index,y=1.25,prefix=26,color=None):
        x=-5.27+index*.34
        c=color or (BLUE if index<24 else YELLOW if index<prefix else GREEN)
        return pill(value,x,y,c,.305,.45,17)

    def bitrow(self,octet=0,prefix=26):
        if self.kind=='bits':return
        self.clear('bits')
        self.current_byte=octet
        values=[int(c)for byte in (192,168,1,octet)for c in f'{byte:08b}']
        self.bits=[self.bitcell(v,j,prefix=prefix)for j,v in enumerate(values)]
        for chunk in range(0,32,4):
            group=m.VGroup(*self.bits[chunk:chunk+4]);self.own(group,weight=.3)
        x=-5.44+prefix*.34
        self.boundary=line((x,.8),(x,1.8),YELLOW,3)
        self.own(self.boundary,animation=m.Create(self.boundary),weight=.4)
        self.own(text('192',-4.08,2.0,21,BLUE),weight=.2)
        self.own(text('168',-1.36,2.0,21,BLUE),weight=.2)
        self.own(text('1',1.36,2.0,21,BLUE),weight=.2)
        self.lastdecimal=self.own(text(octet,4.08,2.0,21,GREEN),weight=.2)
        self.scan=m.Rectangle(width=.4,height=.57,color=WHITE,stroke_width=2).move_to([-5.27+24*.34,1.25,0])
        self.own(self.scan,animation=m.Create(self.scan),weight=.25)

    def byte(self,value,prefix=26,weight=.7):
        self.current_byte=value
        for k,char in enumerate(f'{value:08b}'):
            self.q(m.Transform(self.bits[24+k],self.bitcell(char,24+k,prefix=prefix)),
                   self.scan.animate.move_to([-5.27+(24+k)*.34,1.25,0]),weight=weight/8)
        self.q(m.Transform(self.lastdecimal,text(value,4.08,2.0,21,GREEN)),weight=.2)

    def prefix(self,value):
        self.q(self.boundary.animate.move_to([-5.44+value*.34,1.3,0]),weight=1)
        for j,char in enumerate(f'{self.current_byte:08b}',24):self.q(m.Transform(self.bits[j],self.bitcell(char,j,prefix=value)),weight=.1)

    def address_blocks(self,count=4):
        blocks=[]
        for j in range(count):
            w=11.2/count; x=-5.6+w*(j+.5)
            color=(BLUE,GREEN,YELLOW,WHITE)[j%4]
            blocks.append(pill(f'.{j*(256//count)}–.{(j+1)*(256//count)-1}',x,-.7,color,w-.08,.85,22))
        return blocks

    def show_blocks(self,count=4):
        new=self.address_blocks(count)
        if self.blocks:
            old=list(self.blocks)
            self.world=[item for item in self.world if not any(item is block for block in old)]
            for j,obj in enumerate(new):
                source=old[min(len(old)-1,j*len(old)//count)]
                self.own(obj,animation=m.TransformFromCopy(source,obj),weight=.6)
            self.q(m.FadeOut(m.Group(*old)),weight=.3,after=lambda:self.s.remove(*old))
        else:
            for obj in new:self.own(obj,weight=.5)
        self.blocks=new

    def and_bits(self,address,prefix):
        self.bitrow(address,prefix)
        if self.blocks:
            old=list(self.blocks);self.blocks=[]
            self.world=[item for item in self.world if not any(item is block for block in old)]
            self.q(m.FadeOut(m.Group(*old)),weight=.3,after=lambda:self.s.remove(*old))
        self.byte(address,prefix,.6);self.prefix(prefix)
        mask=[int(i<prefix)for i in range(32)]
        actual=[int(c)for byte in (192,168,1,address)for c in f'{byte:08b}']
        outputs=[]
        maskcells=[]
        for j in range(32):
            mc=self.bitcell(mask[j],j,y=.15,prefix=prefix,color=YELLOW)
            maskcells.append(mc)
            out=self.bitcell('?',j,y=-1.05,prefix=prefix,color=GRAY);outputs.append(out)
        self.own(m.VGroup(*maskcells),temporary=True,weight=.6)
        self.own(m.VGroup(*outputs),temporary=True,weight=.6)
        for start in range(0,32,2):
            animations=[]
            for j in range(start,start+2):
                animations.append(m.Transform(outputs[j],self.bitcell(actual[j]&mask[j],j,y=-1.05,prefix=prefix,color=GREEN)))
            self.q(*animations,weight=.6)
        net=address & (255<<(32-prefix)&255)
        return self.equation(f'192.168.1.{address}  AND  /{prefix}  =  192.168.1.{net}',GREEN)

    def subnet(self,i,v):
        if i in (0,5,6,8,9,10,11,12,13,18,22,23):
            self.bitrow(0,24 if i<6 else 26)
        if i==0:
            self.show_blocks(1);self.show_blocks(2);self.show_blocks(4)
            self.equation('/24 → four /26 blocks',GREEN)
        elif i==1:
            self.bitrow(0,24)
            self.byte(255,24,.8);self.byte(0,24,.8)
            self.equation('4 octets × 8 bits = 32 bits',BLUE)
        elif i==2:
            self.bitrow(0,24);self.prefix(24)
            for n in (0,1,42,127,255):self.byte(n,24,.8)
        elif i==3:
            self.and_bits(0,24)
        elif i==4:
            self.and_bits(42,24)
        elif i==5:
            self.byte(0,24,.6);self.show_blocks(1)
            for n in (1,15,31,63,127,255):self.byte(n,24,.8)
            self.equation('2⁸ = 256 addresses',GREEN)
        elif i==6:
            self.prefix(24);self.show_blocks(1)
            self.prefix(25);self.show_blocks(2)
            self.prefix(26);self.show_blocks(4)
        elif i==7:
            eq=self.and_bits(0,26)
            self.q(m.Transform(eq,text('128 + 64 = 192     mask: 255.255.255.192',0,-2.5,27,YELLOW)),weight=1)
        elif i==8:
            self.prefix(26)
            for n in (0,1,7,15,31,63):self.byte(n,26,.6)
            self.show_blocks(4);self.equation('2⁶ = 64 addresses per block',GREEN)
        elif i==9:
            self.show_blocks(4)
            for n in (0,64,128,192):self.byte(n,26,1)
            self.equation('00 → 0     01 → 64     10 → 128     11 → 192',YELLOW)
        elif 10<=i<=13:
            base=(i-10)*64;self.show_blocks(4)
            self.byte(base,26,1);self.byte(base+63,26,1)
            reserved=m.VGroup(pill(f'.{base}',-4,-1.8,RED,1.7,.65,25),pill(f'.{base+63}',4,-1.8,RED,1.7,.65,25))
            self.own(reserved,temporary=True,weight=.6)
            self.byte(base+1,26,.8);self.byte(base+62,26,.8)
            self.equation(f'Network .{base}     hosts .{base+1}–.{base+62}     broadcast .{base+63}',GREEN)
        elif i==14:
            self.and_bits(70,26)
        elif i==15:
            self.bitrow(70,26);self.byte(70,26,1)
            a=self.equation('.70 AND /26 = .64',GREEN,y=-1.4)
            self.byte(100,26,1);self.q(m.Transform(a,text('.100 AND /26 = .64',0,-1.4,29,GREEN)),weight=1)
            self.byte(130,26,1);self.q(m.Transform(a,text('.130 AND /26 = .128',0,-1.4,29,YELLOW)),weight=1)
        elif i==16:
            self.clear('subnet-routing')
            for label,pos,color in [('70',(-4,1),BLUE),('100',(-4,-1),BLUE),('Router',(0,0),WHITE),('130',(4,0),GREEN)]:self.own(pill('.'+label if label.isdigit()else label,*pos,color,1.8,.8,27),weight=.4)
            self.own(m.Circle(radius=1.75,color=BLUE).stretch(.7,0).move_to([-4,0,0]),weight=.4)
            self.token((-4,1),(-4,-1),'local',BLUE,1)
            p=self.token((-4,1),(0,0),'remote',YELLOW,1,keep=True)
            self.q(p.animate.move_to([4,0,0]),weight=1.3)
            self.fade(p,.3)
        elif i==17:
            self.clear('host-fit')
            dots=[]
            for j in range(50):
                x=-4.5+(j%10)*1.0;y=1.8-(j//10)*.65
                dots.append(m.Dot([x,y,0],radius=.09,color=GREEN if j<30 else RED))
            for start in range(0,50,10):self.own(m.VGroup(*dots[start:start+10]),weight=.7)
            eq=self.equation('/27: 30 usable < 50',RED)
            for start in range(30,50,5):self.q(*[d.animate.set_color(GREEN)for d in dots[start:start+5]],weight=.6)
            self.q(m.Transform(eq,text('/26: 62 usable ≥ 50',0,-2.5,31,GREEN)),weight=1)
        elif i==18:
            self.prefix(25);self.show_blocks(2)
            self.prefix(26);self.show_blocks(4)
            self.prefix(27);self.show_blocks(8)
            self.equation('/25: 128     /26: 64     /27: 32',YELLOW)
        elif i==19:
            self.clear('exceptions')
            pair=m.VGroup(pill('0',-2,0,RED,1.4,1,30),pill('1',2,0,RED,1.4,1,30))
            self.own(pair,weight=1)
            self.equation('/31 point-to-point: both are endpoints',GREEN)
            self.q(m.Transform(pair,m.VGroup(pill('0',-2,0,GREEN,1.4,1,30),pill('1',2,0,GREEN,1.4,1,30))),weight=1.4)
            self.token((-2,0),(2,0),'link',BLUE,1.2)
            self.q(m.Transform(pair,pill('/32',0,0,YELLOW,2,1,35)),weight=1.4)
        elif i==20:
            self.clear('subnet-security')
            left=m.Circle(radius=1.4,color=BLUE).move_to([-3.5,0,0]);right=m.Circle(radius=1.4,color=GREEN).move_to([3.5,0,0])
            self.own(left,animation=m.Create(left),weight=.8);self.own(right,animation=m.Create(right),weight=.8)
            self.own(text('/26',-3.5,0,30,BLUE),weight=.5);self.own(text('/26',3.5,0,30,GREEN),weight=.5)
            self.token((-3.5,0),(3.5,0),'routed traffic',YELLOW,2)
            self.equation('Address boundary ≠ access-control policy',RED)
        elif i==21:
            self.bitrow(0,24);self.prefix(24);self.byte(70,24,1)
            self.prefix(26);self.byte(70,26,1)
            self.equation('192 alone does not determine the prefix',YELLOW)
        elif i==22:
            self.prefix(26);self.show_blocks(4)
            for n in (0,63,64,127,128,191,192,255):self.byte(n,26,.65)
        else:
            self.prefix(24);self.show_blocks(1);self.prefix(26);self.show_blocks(4)
            self.equation('2² blocks × 2⁶ addresses = 256',GREEN)
            for n in (0,64,128,192):self.byte(n,26,.65)

    def actors(self):
        if self.kind=='crypto':return
        self.clear('crypto')
        self.alice=self.own(text('Alice',-5,1.9,27,BLUE),weight=.3)
        self.bob=self.own(text('Bob',5,1.9,27,GREEN),weight=.3)
        self.eve=self.own(text('Eve',0,-2.25,23,RED),weight=.3)

    def message(self,x=-4,y=.5,cipher=False,color=BLUE):
        chars=['8F','31','A9','7C','02','D6']if cipher else list('MEET9!')
        return m.VGroup(*[pill(c,x+(j-2.5)*.62,y,color,.57,.55,25)for j,c in enumerate(chars)])

    def cipher(self,obj,encrypted=True,color=BLUE,weight=1,position=None):
        center=position if position is not None else obj.get_center();target=self.message(center[0],center[1],encrypted,color)
        self.q(m.Transform(obj,target),weight=weight)

    def crypto(self,i,v):
        self.actors()
        if i==0:
            msg=self.own(self.message(-3,.5),temporary=True,weight=.6)
            self.q(msg.animate.move_to([0,.5,0]),weight=1.3)
            stolen=self.message(0,-1.4,color=RED);self.own(stolen,temporary=True,animation=m.TransformFromCopy(msg,stolen),weight=1)
            self.q(msg.animate.move_to([3,.5,0]),weight=1.3)
            return
        if i in (1,2,3,4,5):
            msg=self.own(self.message(-3,.5),temporary=True,weight=.5)
            k=self.own(key(-3,1.4,YELLOW,'K'),temporary=True,weight=.4)
            self.q(k.animate.shift([0,-.5,0]),weight=.7)
            self.cipher(msg,True,BLUE,1.2)
            self.q(msg.animate.move_to([3,.5,0]),weight=1.3)
            if i in (2,4):
                bad=self.own(key(3,1.4,RED,'K′'),temporary=True,weight=.6)
                stop=self.own(cross(3,.5,.4),temporary=True,weight=.6)
                self.q(bad.animate.shift([0,-.35,0]),weight=.7)
                self.fade(stop,.5)
                if i==2:self.fade(bad,.3)
                if i==4:
                    self.q(m.Transform(bad,key(3,1.4,YELLOW,'K')),weight=.8)
                    self.cipher(msg,False,GREEN,1,position=(3,.5))
            elif i==5:
                self.q(k.animate.move_to([0,-1.4,0]),weight=1.3)
                stolen=self.message(0,-1.25,True,RED);self.own(stolen,temporary=True,animation=m.TransformFromCopy(msg,stolen),weight=.7)
                self.cipher(stolen,False,RED,1.1)
                self.fade(k,.3)
            else:
                kb=self.own(key(3,1.4,YELLOW,'K'),temporary=True,weight=.7)
                self.q(kb.animate.shift([0,-.45,0]),weight=.8)
                self.cipher(msg,False,GREEN,1.1,position=(3,.5))
                self.fade(kb,.3)
            return
        if 6<=i<=9:
            pk=self.own(key(4,.95,BLUE,'PK_B'),temporary=True,weight=.6)
            sk=self.own(key(5,-.5,YELLOW,'SK_B'),temporary=True,weight=.6)
            self.q(pk.animate.move_to([-3,1,0]),weight=1.5)
            if i==7:
                publiccopy=key(0,-.1,BLUE,'PK_B');self.own(publiccopy,temporary=True,animation=m.TransformFromCopy(pk,publiccopy),weight=1.2)
            msg=self.own(self.message(-3,.1),temporary=True,weight=.5)
            self.q(pk.animate.move_to([-3,.65,0]),weight=.7);self.cipher(msg,True,BLUE,1.1)
            self.q(msg.animate.move_to([3,.1,0]),weight=1.3)
            if i in (6,9):
                self.q(sk.animate.move_to([3,1,0]),weight=1)
                self.cipher(msg,False,GREEN,1.2,position=(3,.1))
            else:
                seen=self.message(0,-1.3,True,RED);self.own(seen,temporary=True,animation=m.TransformFromCopy(msg,seen),weight=.9)
                self.own(cross(0,-1.3,.35),temporary=True,weight=.7)
            return
        if i in (10,11,12,13,14,15,23):
            k=self.own(key(-3,1.1,YELLOW,'K'),temporary=True,weight=.5)
            msg=self.own(self.message(-3,-.5),temporary=True,weight=.5)
            if i==11:
                for label in ('101…','011…','random K'):
                    self.q(m.Transform(k,key(-3,1.1,YELLOW,label)),weight=.6)
            pk=self.own(key(-.4,1.1,BLUE,'PK_B'),temporary=True,weight=.5)
            self.cipher(msg,True,BLUE,1.2)
            tag=self.own(pill('tag',-.7,-.5,GREEN,.7,.5,17),temporary=True,weight=.5)
            self.q(m.Transform(k,pill('Enc(PK_B,K)',-3,1.1,BLUE,2.5,.65,22)),weight=1.1)
            self.q(k.animate.move_to([3,1.1,0]),weight=1.4)
            self.q(msg.animate.move_to([2.8,-.5,0]),tag.animate.move_to([5.6,-.5,0]),weight=1.4)
            if i in (10,15,23):
                sk=self.own(key(4.7,1.4,YELLOW,'SK_B'),temporary=True,weight=.5)
                self.q(m.Transform(k,key(3,1.1,YELLOW,'K')),weight=1)
                self.q(k.animate.move_to([2.8,.25,0]),weight=.8)
                self.q(m.Transform(tag,pill('✓',5.6,-.5,GREEN,.7,.5,25)),weight=.5)
                self.cipher(msg,False,GREEN,1.1,position=(2.8,-.5))
            return
        if i in (16,17):
            msg=self.own(self.message(-3,.5,True),temporary=True,weight=.5)
            tag=self.own(pill('A7',-.7,.5,GREEN,.65,.5,20),temporary=True,weight=.5)
            self.q(msg.animate.move_to([0,.5,0]),tag.animate.move_to([2.35,.5,0]),weight=1.3)
            changed=pill('FF',-.24,.5,RED,.43,.5,17)
            self.q(m.Transform(msg[2],changed),weight=.8)
            self.q(msg.animate.move_to([2.8,.5,0]),tag.animate.move_to([5.6,.5,0]),weight=1.3)
            check=self.own(pill('D2',5.6,-.45,RED,.65,.5,20),temporary=True,weight=.6)
            self.equation('A7 ≠ D2',RED,y=-1.55)
            self.own(cross(2.8,.5,.55),temporary=True,weight=.7)
            return
        if i==18:
            k=self.own(key(-3,1.1,YELLOW,'K'),temporary=True,weight=.5)
            n1=self.own(pill('N₁',-3,-.1,BLUE,1,.6,25),temporary=True,weight=.5)
            msg=self.own(self.message(1,.5,True),temporary=True,weight=.5)
            self.q(n1.animate.move_to([1,-.1,0]),weight=1.2)
            duplicate=pill('N₁',1,-1.0,RED,1,.6,25)
            self.own(duplicate,temporary=True,animation=m.TransformFromCopy(n1,duplicate),weight=1)
            self.own(cross(2.2,-.55,.35),temporary=True,weight=.6)
            self.q(m.Transform(duplicate,pill('N₂',1,-1,GREEN,1,.6,25)),weight=1)
            self.q(msg.animate.move_to([3.5,.5,0]),weight=1.3)
            return
        if i==19:
            pk=self.own(key(4,1,BLUE,'PK_B'),temporary=True,weight=.5)
            self.q(pk.animate.move_to([0,1,0]),weight=1)
            self.q(m.Transform(pk,key(0,1,RED,'PK_E')),weight=1)
            self.q(pk.animate.move_to([-3,1,0]),weight=1)
            msg=self.own(self.message(-3,.1),temporary=True,weight=.5)
            self.cipher(msg,True,RED,1)
            self.q(msg.animate.move_to([0,-1.2,0]),weight=1.3)
            self.cipher(msg,False,RED,1.1,position=(0,-1.2))
            self.own(cross(4,.2,.5),temporary=True,weight=.6)
            return
        if i==20:
            for sender,color,y in [(-3,BLUE,.7),(0,RED,-1.2)]:
                msg=self.own(self.message(sender,y,True,color),temporary=True,weight=.5)
                self.q(msg.animate.move_to([3,y,0]),weight=1.3)
                self.cipher(msg,False,GREEN,1,position=(3,y))
            self.equation('Decryptable ≠ signed by Alice',YELLOW,y=1.3)
            return
        if i==21:
            a=self.own(pill('ephemeral a',-3,1,BLUE,2.1,.7,24),temporary=True,weight=.5)
            b=self.own(pill('ephemeral b',3,1,GREEN,2.1,.7,24),temporary=True,weight=.5)
            self.token((-3,.2),(3,.2),'public share A',BLUE,1.2)
            self.token((3,-.7),(-3,-.7),'public share B',GREEN,1.2)
            ka=key(-3,1,YELLOW,'K');kb=key(3,1,YELLOW,'K')
            self.temp=[obj for obj in self.temp if obj is not a and obj is not b];self.temp.extend([ka,kb])
            self.q(m.ReplacementTransform(a,ka),m.ReplacementTransform(b,kb),weight=1.2,after=lambda:self.s.remove(a,b))
            msg=self.own(self.message(-3,.1),temporary=True,weight=.5)
            self.cipher(msg,True,BLUE,1)
            self.q(msg.animate.move_to([3,.1,0]),weight=1.4)
            self.cipher(msg,False,GREEN,1,position=(3,.1))
            return
        # Verified identity → key establishment → protected delivery.
        identity=self.own(pill('Bob ✓',3,1,GREEN,2,.7,27),temporary=True,weight=.6)
        pk=self.own(key(3,.2,BLUE,'PK_B'),temporary=True,weight=.6)
        self.q(pk.animate.move_to([-3,.2,0]),weight=1.3)
        msg=self.own(self.message(-3,-.8),temporary=True,weight=.5)
        self.cipher(msg,True,BLUE,1.2)
        self.q(msg.animate.move_to([3,-.8,0]),weight=1.4)
        self.cipher(msg,False,GREEN,1.2,position=(3,-.8))

    def animate(self,index,section,budget):
        self.steps=[];self.remove_temporary()
        if self.episode=='05':self.routing(index,section.get('visual',{}))
        elif self.episode=='06':self.subnet(index,section.get('visual',{}))
        elif self.episode=='08':self.crypto(index,section.get('visual',{}))
        else:raise ValueError(f'Unsupported SystemsDirector episode {self.episode}')
        assert self.steps,(self.episode,index)
        total=sum(w for w,_ in self.steps)
        target=max(.1,float(budget)-.2)
        for weight,action in self.steps:action(target*weight/total)
