"""Continuous, causal packet motion for website, ARQ, and transport lessons.

The director budgets every beat from the requested duration; packet flights,
receiver state, timers, and growing windows do the teaching rather than slides.
"""
from __future__ import annotations

import math
import numpy as np
import manimgx as m

BLUE='#58C4DD'; GREEN='#83C167'; YELLOW='#FFFF00'; RED='#FC6255'
WHITE='#F2F2F2'; MUTED='#8B93A6'; BG='#080A10'; PURPLE='#B39DDB'


def text(value,x=0,y=0,size=24,color=WHITE,width=11):
    obj=m.Text(str(value),font='Noto Sans',font_size=size,color=color)
    if obj.width>width: obj.scale(width/obj.width)
    return obj.move_to([x,y,0])


def wire(a,b,color=MUTED,width=2):
    return m.Line([*a,0],[*b,0],color=color,stroke_width=width)


def arrow(a,b,color=BLUE):
    return m.Arrow([*a,0],[*b,0],buff=.02,color=color,stroke_width=2.5,max_tip_length_to_length_ratio=.12)


def packet(value,color=BLUE,width=None,height=.48):
    if width is None: width=max(1.25,min(3.1,.13*len(str(value))+.4))
    return m.VGroup(m.Rectangle(width=width,height=height,color=color,stroke_width=2,fill_color=BG,fill_opacity=1),
                    text(value,size=20,color=color,width=width-.12)).set_z_index(5)


def host(value,x,y,color=BLUE):
    circle=m.Circle(radius=.36,color=color,stroke_width=2.8,fill_color=BG,fill_opacity=1).move_to([x,y,0])
    return m.VGroup(circle,text(value,x,y+.65,24,color,2.4))


class PacketDirector:
    def __init__(self,scene,episode_id):
        self.scene=scene; self.episode_id=str(episode_id).zfill(2)
        self.kind=None; self.group=m.Group(); self.base=m.Group(); self.overlay=m.Group()
        self._roots=[]; self._temporary=[]; self.state={}

    def _own(self,obj,persistent=False):
        (self.base if persistent else self.overlay).add(obj)
        (self._roots if persistent else self._temporary).append(obj)
        return obj

    def _remove_family(self,*objects):
        # Removing an animated child splits scene groups; remove every owned descendant too.
        self.scene.remove(*(member for obj in objects for member in obj.get_family()))

    def _ensure(self,kind):
        if self.kind!=kind:
            self._remove_family(self.group,*self._roots,*self._temporary)
            self.kind=kind; self.base=m.Group(); self.overlay=m.Group()
            self.group=m.Group(self.base,self.overlay)
            self._roots=[]; self._temporary=[]; self.state={}
            return True
        self._remove_family(self.overlay,*self._temporary)
        self.group.remove(self.overlay); self.overlay=m.Group(); self.group.add(self.overlay)
        self._temporary=[]
        return False

    def _run(self,beats,budget):
        total=sum(weight for weight,_ in beats)
        for weight,make in beats:
            animations=make()
            if not isinstance(animations,(tuple,list)): animations=(animations,)
            self.scene.play(*animations,run_time=budget*weight/total,rate_func=m.linear)
            # FadeOut restores its source geometry; detach it from our persistent parents.
            for animation in animations:
                if isinstance(animation,(m.FadeOut,m.ReplacementTransform)):
                    old=animation.mobject
                    self._remove_family(old);self.overlay.remove(old);self.base.remove(old)
                    if old in self._temporary:self._temporary.remove(old)
                    if old in self._roots:self._roots.remove(old)

    def _draw(self,beats,obj,weight=.7):
        if obj not in self._roots and obj not in self._temporary: self._own(obj)
        beats.append((weight,lambda obj=obj:m.FadeIn(obj)))

    def _move(self,beats,obj,point,weight=1):
        beats.append((weight,lambda obj=obj,point=point:obj.animate.move_to([*point,0])))

    def _change(self,beats,obj,new,weight=.7):
        beats.append((weight,lambda obj=obj,new=new:m.Transform(obj,new)))

    def _flight(self,beats,value,a,b,color=BLUE,weight=1,lost=False,keep=False):
        q=self._own(packet(value,color).move_to([*a,0])); self._draw(beats,q,.15)
        stop=((a[0]+b[0])/2,(a[1]+b[1])/2) if lost else b
        delta=np.array(stop)-np.array(a)
        norm=float(np.linalg.norm(delta))
        trail_end=tuple(np.array(stop)-delta/max(norm,1e-8)*min(.65,norm*.25)) if keep else stop
        trail=self._own(arrow(a,trail_end,RED if lost else color).set_z_index(1))
        beats.append((weight,lambda q=q,stop=stop,trail=trail:(q.animate.move_to([*stop,0]),m.Create(trail))))
        if lost:
            x,y=stop; mark=self._own(m.VGroup(wire((x-.15,y-.15),(x+.15,y+.15),RED,4),wire((x-.15,y+.15),(x+.15,y-.15),RED,4)))
            beats.append((.2,lambda q=q,mark=mark:(m.FadeOut(q),m.Create(mark))))
        elif not keep: beats.append((.15,lambda q=q:m.FadeOut(q)))
        return q

    def _caption(self,beats,value,y=-2.55,color=WHITE,weight=.45):
        obj=self._own(text(value,0,y,24,color));self._draw(beats,obj,weight);return obj

    def _network(self,beats):
        fresh=self._ensure('network')
        if fresh:
            xs=(-5,-1.7,1.7,5)
            nodes=self._own(m.VGroup(*[host(n,x,.7,c) for n,x,c in zip(('Browser','Switch','Router','Server'),xs,(BLUE,GREEN,YELLOW,PURPLE))]),True)
            links=self._own(m.VGroup(*[wire((xs[j]+.4,.7),(xs[j+1]-.4,.7)) for j in range(3)]),True)
            self.state['nodes']=nodes;self.state['links']=links
            self._draw(beats,nodes);beats.append((.8,lambda:m.Create(links)))

    def _timeline(self,beats):
        fresh=self._ensure('timeline')
        if fresh:
            nodes=self._own(m.VGroup(host('Sender',-5,1.7),host('Receiver',5,1.7,GREEN)),True)
            lines=self._own(m.VGroup(wire((-5,1.15),(-5,-2.25)),wire((5,1.15),(5,-2.25))),True)
            self._draw(beats,nodes);beats.append((.6,lambda:m.Create(lines)))

    def _messages(self,beats,messages):
        n=len(messages)
        for j,(value,direction,color,lost) in enumerate(messages):
            y=1.0-j*2.7/max(n,1)
            if direction=='local':
                timer=self._own(m.Arc(radius=.28,start_angle=m.PI/2,angle=-m.TAU,color=color,stroke_width=5).move_to([-5,y,0]))
                note=self._own(text(value,-2.9,y,20,color,3.2))
                beats.append((1.1,lambda timer=timer,note=note:(m.Create(timer),m.FadeIn(note))))
            else:
                a=(-4.9,y) if direction=='right' else (4.9,y)
                b=(4.9,y-.42) if direction=='right' else (-4.9,y-.42)
                self._flight(beats,value,a,b,color,1.5,lost)
                note_text=text(value,0,y+.05,22,color,6.5)
                backing=m.Rectangle(width=note_text.width+.1,height=note_text.height+.08,
                                    fill_color=BG,fill_opacity=1,stroke_width=0).move_to(note_text)
                note=self._own(m.VGroup(backing,note_text).set_z_index(6))
                self._draw(beats,note,.22)

    def _envelope(self,beats,level):
        fresh=self._ensure('envelope')
        if fresh:
            payload=self._own(packet('HTTP data',BLUE,2.5,.75).move_to([1.7,0,0]),True)
            self.state['payload']=payload;self.state['headers']=[]
            self._draw(beats,payload)
        colors=(GREEN,YELLOW,PURPLE)
        names=('TCP','IP','LINK')
        for j in range(len(self.state['headers']),level):
            x=.15-j*1.45
            h=self._own(packet(names[j],colors[j],1.35,.75).move_to([x,-1.35,0]),True)
            wrap=self._own(m.Rectangle(width=4.0+j*1.45,height=1.05+j*.28,color=colors[j],stroke_width=2).move_to([.95-j*.725,0,0]),True)
            self._draw(beats,h,.4)
            beats.append((1.2,lambda h=h,x=x,wrap=wrap:(h.animate.move_to([x,0,0]),m.Create(wrap))))
            self.state['headers'].append((h,wrap))

    def _window(self,beats):
        fresh=self._ensure('window')
        if fresh:
            xs=[-4.55+j*1.3 for j in range(8)]
            cells=self._own(m.VGroup(*[packet(str(j),BLUE,.95,.65).move_to([x,1,0]) for j,x in enumerate(xs)]),True)
            outline=self._own(m.Rectangle(width=5.1,height=.9,color=YELLOW,stroke_width=3).move_to([-2.6,1,0]),True)
            receivers=self._own(m.VGroup(*[m.Rectangle(width=.95,height=.65,color=MUTED,stroke_width=1).move_to([x,-1.0,0]) for x in xs]),True)
            names=self._own(m.VGroup(text('sender window',-2.6,2.1,23,YELLOW)),True)
            self.state.update(cells=cells,outline=outline,receivers=receivers,xs=xs)
            self._draw(beats,cells);beats.append((.7,lambda:m.Create(outline)));self._draw(beats,receivers);self._draw(beats,names,.4)

    def animate(self,index,section,budget):
        if budget<=0: raise ValueError('Positive animation budget required')
        beats=[]
        if self.episode_id=='01': self._website(index,section,beats)
        elif self.episode_id=='03': self._arq(index,section,beats)
        elif self.episode_id=='07': self._transport(index,section,beats)
        else: raise ValueError(f'Unsupported packet episode {self.episode_id}')
        if not beats: raise AssertionError((self.episode_id,index))
        self._run(beats,budget)

    def _website(self,i,s,b):
        if i in (0,1,2,9,15,16,17,18,20,21,23):
            self._network(b)
            if i==2:
                lan=self._own(m.RoundedRectangle(width=5.9,height=2.4,corner_radius=.3,color=BLUE,stroke_width=2).move_to([-3.2,.7,0]));b.append((1,lambda:m.Create(lan)))
                self._caption(b,'LAN                         wider network',-1.25,MUTED)
            if i==17:
                ip=self._own(packet('IP: server',YELLOW,2.0).move_to([-5,-.7,0]));self._draw(b,ip)
                for j,x in enumerate((-1.7,1.7,5)):
                    outer=self._own(m.Rectangle(width=2.3,height=.8,color=(BLUE,GREEN,PURPLE)[j],stroke_width=3).move_to([ip.get_center()[0],-.7,0]))
                    self._draw(b,outer,.25)
                    b.append((1.3,lambda ip=ip,outer=outer,x=x:(ip.animate.move_to([x,-.7,0]),outer.animate.move_to([x,-.7,0]))))
                    b.append((.3,lambda outer=outer:m.FadeOut(outer)))
                self._caption(b,'IP destination persists; local envelopes change',-2.1,YELLOW)
                return
            if i==18:
                queue=self._own(m.VGroup(*[packet(str(j),BLUE,.65,.45).move_to([.1+j*.8,-.8,0]) for j in range(5)]));self._draw(b,queue)
                for j in range(3):
                    q=queue[j];self._move(b,q,(5,-.8),1.1);b.append((.3,lambda q=q:m.FadeOut(q)))
                self._flight(b,'overflow',(-5,-.8),(1.7,-.8),RED,1.2,True)
                self._caption(b,'Full queues can drop arriving packets',-2.1,RED)
                return
            count=3 if i==21 else 1
            for k in range(count):
                color=(BLUE,GREEN,YELLOW)[k]; word=('HTML','CSS','image')[k] if i==21 else ('GET /' if i==9 else '200 OK' if i==20 else 'request')
                if i==20:
                    for a,z in ((5,1.7),(1.7,-1.7),(-1.7,-5)): self._flight(b,word,(a,-.25-k*.6),(z,-.25-k*.6),color,1)
                else:
                    for a,z in ((-5,-1.7),(-1.7,1.7),(1.7,5)): self._flight(b,word,(a,-.25-k*.6),(z,-.25-k*.6),color,1)
            if i==15: self._caption(b,'Switch: choose an outgoing local port',-2.2,GREEN)
            elif i==16: self._caption(b,'Router: choose the next IP hop',-2.2,YELLOW)
            elif i==1:self._caption(b,'Teaching path: HTTP/1.1 over TCP',-2.2)
            return
        if i==3:
            self._ensure('layers')
            osi=['Application','Presentation','Session','Transport','Network','Data link','Physical']
            rows=[]
            for j,name in enumerate(osi):
                y=2.1-j*.66; obj=self._own(text(name,-3.5,y,24,(BLUE if j<3 else GREEN if j==3 else YELLOW if j==4 else PURPLE)))
                self._draw(b,obj,.3);rows.append(obj)
            for start,end,name,y,col in ((0,3,'Application',1.44,BLUE),(3,4,'Transport',.12,GREEN),(4,5,'Internet',-.54,YELLOW),(5,7,'Link',-1.53,PURPLE)):
                target=self._own(text(name,3.5,y,27,col));paths=self._own(m.VGroup(*[arrow((-1.6,rows[j].get_y()),(2,y),col) for j in range(start,end)]))
                b.append((1,lambda target=target,paths=paths:(m.FadeIn(target),m.Create(paths))))
            return
        if i in (4,5,6):
            fresh=self._ensure('dns')
            xs=(-5,-2.5,0,2.5,5)
            if fresh:
                nodes=self._own(m.VGroup(*[host(n,x,.9,c) for n,x,c in zip(('Browser','Resolver','Root','TLD','Authority'),xs,(BLUE,GREEN,YELLOW,PURPLE,BLUE))]),True)
                links=self._own(m.VGroup(*[wire((xs[j]+.4,.9),(xs[j+1]-.4,.9)) for j in range(4)]),True)
                self._draw(b,nodes);b.append((.7,lambda:m.Create(links)))
            self._flight(b,'name?',(-5,.1),(-2.5,.1),BLUE,1)
            if i==5:
                for x,label_ in ((0,'root?'),(2.5,'TLD?'),(5,'address?')):
                    self._flight(b,label_,(-2.5,-.45),(x,-.45),BLUE,.8)
                    self._flight(b,'referral' if x<5 else 'IP address',(x,-1.1),(-2.5,-1.1),GREEN,.8)
            elif i==6:
                cache=self._own(m.Circle(radius=.55,color=GREEN).move_to([-2.5,-1.3,0]));b.append((1,lambda:m.Create(cache)))
                expiry=self._own(m.Arc(radius=.64,start_angle=m.PI/2,angle=-m.TAU,color=YELLOW,stroke_width=5).move_to([-2.5,-1.3,0]));b.append((1.5,lambda:m.Create(expiry)))
                self._caption(b,'Cached answer: reuse until its lifetime expires',-2.45,GREEN)
            else:self._flight(b,'lookup',(-2.5,-.65),(5,-.65),BLUE,1.5)
            self._flight(b,'IP address',(-2.5,-1.85),(-5,-1.85),GREEN,1)
            return
        if i==7:
            self._ensure('ports')
            source=self._own(host('client:49152',-5,.8));dest=self._own(host('server',2,.8,GREEN));self._draw(b,source);self._draw(b,dest)
            for j,p in enumerate((22,80,443)):
                end=self._own(packet(str(p),YELLOW if p==80 else MUTED,.8).move_to([5,1.5-j*1.3,0]));self._draw(b,end,.4)
                ln=self._own(wire((2.4,.8),(4.6,1.5-j*1.3),MUTED));b.append((.4,lambda ln=ln:m.Create(ln)))
            self._flight(b,'dst:80',(-4.6,0),(2,0),BLUE,1.7)
            self._flight(b,'HTTP',(2,.0),(5,.2),YELLOW,1.5)
            self._caption(b,'IP selects the host; a port selects an endpoint',-2.25)
            return
        if i==8:
            self._timeline(b);self._messages(b,[('SYN 100','right',BLUE,False),('SYN 500 • ACK 101','left',GREEN,False),('ACK 501','right',YELLOW,False)]);return
        if i in (10,11,12,13):
            self._envelope(b,max(0,i-10))
            q=self.state['payload']
            if i==10:
                for y in (1.4,-1.2,0):self._move(b,q,(1.7,y),1)
            else:
                field=('49152 → 80    seq 101','source IP → destination IP','local source MAC → next-hop MAC')[i-11]
                self._caption(b,field,-2.25,(GREEN,YELLOW,PURPLE)[i-11],1)
                cursor=self._own(m.Line([-5.6,1.2,0],[3.0,1.2,0],color=(GREEN,YELLOW,PURPLE)[i-11],stroke_width=3))
                b.append((1.6,lambda:m.Create(cursor)))
            return
        if i==14:
            self._ensure('signal');bits=(1,0,1,1,0,0,1,0)
            row=self._own(m.VGroup(*[text(bit,-5.3+j*1.5,1.5,34,BLUE) for j,bit in enumerate(bits)]));self._draw(b,row)
            pts=[]
            for j,v in enumerate(bits):
                x=-6+j*1.5;pts.extend(((x,.1 if v else -1.1,0),(x+1.5,.1 if v else -1.1,0)))
            trace=self._own(m.VMobject(color=GREEN,stroke_width=4).set_points_as_corners(np.array(pts)))
            b.append((3,lambda:m.Create(trace)))
            cursor=self._own(m.Line([-6,1.9,0],[-6,-1.6,0],color=YELLOW));self._draw(b,cursor,.2)
            b.append((3,lambda:cursor.animate.shift(12*m.RIGHT)))
            self._caption(b,'Bits become encoded physical signals',-2.4)
            return
        if i==19:
            self._envelope(b,3)
            for h,wrap in reversed(self.state['headers']):
                b.append((1.3,lambda h=h,wrap=wrap:(h.animate.shift(1.7*m.DOWN),m.FadeOut(wrap))))
                b.append((.35,lambda h=h:m.FadeOut(h)))
            q=self.state['payload'];self._move(b,q,(0,1.0),1.2)
            self._caption(b,'The server application receives HTTP bytes',-2.4,BLUE)
            return
        if i==22:
            self._ensure('modern')
            for y,left,right,col in ((1.1,'HTTPS','TLS + TCP',GREEN),(-1.1,'HTTP/3','QUIC + UDP',BLUE)):
                l=self._own(host(left,-5,y,col));r=self._own(host(right,5,y,col));self._draw(b,m.Group(l,r))
                self._flight(b,'protected',(-4.6,y),(4.6,y),col,2)
            return

    def _utilization(self,b,compare=False):
        self._ensure('utilization')
        axis=self._own(m.VGroup(wire((-4.5,1.0),(5.5,1.0)),wire((-4.5,-1.8),(5.5,-1.8))))
        self._draw(b,axis,.5)
        if compare:
            for j,(w,u) in enumerate(((1,1/21),(4,4/21),(21,1))):
                y=1.4-j*1.5
                title=self._own(text(f'window {w}',-5.2,y,22,YELLOW,1.7));self._draw(b,title,.25)
                bar=self._own(m.Rectangle(width=.05,height=.45,color=GREEN,fill_color=GREEN,fill_opacity=.8).move_to([-3.9,y,0]));self._draw(b,bar,.2)
                final=m.Rectangle(width=8.8*u,height=.45,color=GREEN,fill_color=GREEN,fill_opacity=.8).move_to([-3.925+4.4*u,y,0])
                self._change(b,bar,final,1.4)
                result=self._own(text(f'{u*100:.1f}%',5.72,y,23,GREEN,1.5));self._draw(b,result,.3)
        else:
            busy=self._own(m.Rectangle(width=.45,height=.55,color=BLUE,fill_color=BLUE,fill_opacity=.8).move_to([-4.275,.3,0]))
            wait=self._own(m.Rectangle(width=9,height=.55,color=MUTED,fill_color=MUTED,fill_opacity=.15).move_to([.45,.3,0]))
            self._draw(b,busy,1);b.append((3,lambda:m.Create(wait)))
            marker=self._own(m.Line([-4.5,.8,0],[-4.5,-.2,0],color=YELLOW,stroke_width=3));self._draw(b,marker,.2)
            b.append((4,lambda:marker.animate.shift(9.45*m.RIGHT)))
            self._caption(b,'1 ms sending + 20 ms propagation round trip',-1.1,MUTED,.7)
            self._caption(b,'1 / 21 ≈ 4.8% useful sending time',-2.3,BLUE,.7)

    def _arq(self,i,s,b):
        if i in (4,5,6,22):
            self._utilization(b,i==22);return
        if i in (14,15,16,17):
            self._window(b);cells=self.state['cells'];xs=self.state['xs'];outline=self.state['outline']
            if i==14:
                narrow=outline.copy().stretch_to_fit_width(1.1).move_to([xs[0],1,0])
                self._change(b,outline,narrow,1)
                self._change(b,outline,m.Rectangle(width=5.1,height=.9,color=YELLOW,stroke_width=3).move_to([-2.6,1,0]),2)
                for j in range(4):
                    q=self._own(packet(str(j),BLUE,.95,.65).move_to([xs[j],1,0]));self._draw(b,q,.15)
                    self._move(b,q,(xs[j],-.15),.8)
                return
            if i==15:
                for j in range(4):self._flight(b,str(j),(xs[j],.6),(xs[j],-1),BLUE,1.2,keep=True)
                self._caption(b,'Data and feedback overlap in flight',-2.5)
                return
            if i==16:
                self._flight(b,'ACK 3',(4.5,-1.75),(-4.5,-1.75),GREEN,2)
                for j in range(3):b.append((.7,lambda j=j:(cells[j][0].animate.set_stroke(GREEN),cells[j][1].animate.set_color(GREEN))))
                self._caption(b,'0, 1, 2 confirmed; next expected is 3',-2.5,GREEN)
                return
            if i==17:
                # A new illustrative ACK-2 trace, not a regression after the previous ACK-3 example.
                for j in range(8):
                    b.append((.1,lambda j=j:(cells[j][0].animate.set_stroke(BLUE),cells[j][1].animate.set_color(BLUE))))
                self._change(b,outline,m.Rectangle(width=5.1,height=.9,color=YELLOW,stroke_width=3).move_to([-2.6,1,0]),.6)
                self._flight(b,'ACK 2',(4.5,-1.75),(-4.5,-1.75),GREEN,1.8)
                b.append((1.7,lambda:outline.animate.shift(2.6*m.RIGHT)))
                for j in (0,1):b.append((.6,lambda j=j:(cells[j][0].animate.set_stroke(GREEN),cells[j][1].animate.set_color(GREEN))))
                for j in (4,5):self._flight(b,str(j),(xs[j],.6),(xs[j],-1),BLUE,.8,keep=True)
                return
        if i==12:
            self._ensure('alternating')
            left=self._own(host('Sender',-5,1.4));right=self._own(host('Receiver',5,1.4,GREEN));self._draw(b,m.Group(left,right))
            state=self._own(text('expect 0',4,-1.2,28,GREEN));self._draw(b,state)
            for j in range(3):
                bit=j%2;self._flight(b,str(bit),(-4.6,.5),(4.6,.5),BLUE,1)
                self._change(b,state,text(f'expect {1-bit}',4,-1.2,28,GREEN),.5)
                self._flight(b,f'ACK {1-bit}',(4.6,-.2),(-4.6,-.2),GREEN,.8)
            return
        self._timeline(b)
        if i==0:
            self._messages(b,[('DATA 0','right',BLUE,False),('DATA 1','right',RED,True),('DATA 2','right',BLUE,False)])
            self._caption(b,'What confirms that the missing data arrived?',-2.6,RED)
        elif i==1:
            time=self._own(arrow((-6,1.2),(-6,-2.3),YELLOW));b.append((1.4,lambda:m.Create(time)))
            self._messages(b,[('DATA 0','right',BLUE,False),('ACK 1','left',GREEN,False)])
        elif i in (2,3):
            self._messages(b,[('DATA 0','right',BLUE,False),('ACK 1','left',GREEN,False)])
            state=self._own(text('next expected: 0',2.8,-2.15,24,GREEN));self._draw(b,state,.4)
            self._change(b,state,text('next expected: 1',2.8,-2.15,24,GREEN),1)
        elif i==7:
            self._messages(b,[('DATA 0','right',BLUE,True),('no confirmation','local',RED,False)])
        elif i==8:
            self._messages(b,[('DATA 0','right',BLUE,True),('timer expires','local',YELLOW,False),('retry needed','local',RED,False)])
        elif i==9:
            self._messages(b,[('saved DATA 0','right',BLUE,False),('ACK 1','left',GREEN,False)])
            self._caption(b,'Same logical data, same sequence number',-2.55,BLUE)
        elif i in (10,11):
            self._messages(b,[('DATA 0','right',BLUE,False),('ACK 1','left',GREEN,True),('DATA 0 again','right',YELLOW,False),('ACK 1 repeated','left',GREEN,False)])
            counter=self._own(text('application deliveries: 1',1.6,-2.45,24,GREEN));self._draw(b,counter,1)
        elif i==13:
            self._messages(b,[('DATA 0','right',BLUE,False),('too-early timeout','local',RED,False),('delayed ACK 1','left',GREEN,False)])
        elif i==18:
            self._messages(b,[('DATA 0','right',BLUE,False),('DATA 1','right',RED,True),('DATA 2','right',YELLOW,False),('DATA 3','right',YELLOW,False)])
            self._caption(b,'Gap at 1; only 0 is accepted',-2.55,RED)
        elif i==19:
            self._messages(b,[('DATA 2 discarded','right',YELLOW,False),('ACK 1','left',GREEN,False),('DATA 3 discarded','right',YELLOW,False),('ACK 1 again','left',GREEN,False)])
        elif i==20:
            self._messages(b,[('oldest unconfirmed: 1','local',YELLOW,False),('DATA 1 retry','right',BLUE,False),('DATA 2 retry','right',BLUE,False),('DATA 3 retry','right',BLUE,False)])
        elif i==21:
            self._messages(b,[('DATA 1 accepted','right',BLUE,False),('DATA 2 accepted','right',BLUE,False),('DATA 3 accepted','right',BLUE,False),('ACK 4','left',GREEN,False)])
        else:
            self._messages(b,[('DATA 0','right',BLUE,True),('timeout','local',YELLOW,False),('DATA 0 retry','right',BLUE,False),('ACK 1','left',GREEN,False)])

    def _bytes(self,b):
        fresh=self._ensure('bytes')
        if fresh:
            xs=(-3.3,0,3.3)
            slots=self._own(m.VGroup(*[m.Rectangle(width=2.6,height=.75,color=MUTED,stroke_width=2).move_to([x,-.4,0]) for x in xs]),True)
            labels=self._own(m.VGroup(text('sender byte ranges',0,2.15,25,BLUE)),True)
            self.state.update(xs=xs,slots=slots,arrived={})
            self._draw(b,labels);b.append((.7,lambda:m.Create(slots)))

    def _receive_bytes(self,b,j,weight=1.2):
        xs=self.state['xs'];a=(xs[j],1.35);z=(xs[j],-.4)
        value=f'{101+j*100}–{200+j*100}'
        q=self._own(packet(value,BLUE,2.35,.6).move_to([*a,0]),True)
        self._draw(b,q,.25);self._move(b,q,z,weight)
        self.state['arrived'][j]=q
        return q

    def _receive_capacity(self,b):
        fresh=self._ensure('receive-capacity')
        if fresh:
            nodes=self._own(m.VGroup(host('Sender',-5,1.4),host('Receiver',4.8,1.4,GREEN)),True)
            slots=self._own(m.VGroup(*[m.Rectangle(width=1.5,height=.75,color=GREEN,stroke_width=2).move_to([.5+j*1.8,0,0]) for j in range(3)]),True)
            counter=self._own(text('rwnd = 300 bytes',2.3,-1.35,28,GREEN),True)
            self.state.update(slots=slots,counter=counter,filled=[])
            self._draw(b,nodes);b.append((.7,lambda:m.Create(slots)));self._draw(b,counter)

    def _transport(self,i,s,b):
        if i==1:
            self._website(7,s,b);return
        if i in (4,5,6,7,22):
            self._timeline(b)
            if i==4:messages=[('SYN 100','right',BLUE,False),('SYN 500 / ACK101','left',GREEN,False),('ACK 501','right',YELLOW,False)]
            elif i==5:messages=[('SYN seq100','right',BLUE,False)]
            elif i==6:messages=[('SYN500 ACK101','left',GREEN,False)]
            elif i==7:messages=[('ACK seq101 ack501','right',YELLOW,False)]
            else:messages=[('FIN seq201','right',BLUE,False),('ACK 202','left',GREEN,False),('FIN seq501','left',BLUE,False),('ACK 502','right',GREEN,False)]
            self._messages(b,messages)
            if i in (5,6,7):
                before=('CLOSED','SYN-SENT','SYN-RECEIVED')[i-5];after=('SYN-SENT','SYN-RECEIVED','ESTABLISHED')[i-5]
                state=self._own(text(before,0,-2.5,27,MUTED));self._draw(b,state,.6)
                self._change(b,state,text(after,0,-2.5,27,GREEN),1.5)
            return
        if i in (3,8,9,10,11,13,20):
            if i==3:
                self._ensure('stream')
                chunks=self._own(m.VGroup(*[packet(v,c,1.65,.6).move_to([-3+j*3,1.3,0]) for j,(v,c) in enumerate((('HEL',BLUE),('LO',GREEN),('!',YELLOW)))]));self._draw(b,chunks)
                letters=self._own(m.VGroup(*[text(c,-3.5+j*1.4,-.25,40,BLUE) for j,c in enumerate('HELLO!')]));b.append((1.8,lambda:m.ReplacementTransform(chunks,letters)))
                delimiter=self._own(wire((-4.2,-1),(4.2,-1),GREEN,4));b.append((1.2,lambda:m.Create(delimiter)))
                self._caption(b,'One byte stream; original writes need not stay separate',-2.25)
                return
            self._bytes(b)
            if i==8:
                q=self._receive_bytes(b,0,2)
                start=self._own(text('101',-4.8,.4,28,YELLOW));end=self._own(text('200',-1.8,.4,28,YELLOW));self._draw(b,m.VGroup(start,end),.7)
                self._caption(b,'100 data bytes: 101 through 200',-2.3,BLUE,1)
            elif i==9:
                if 0 not in self.state['arrived']:self._receive_bytes(b,0)
                self._flight(b,'ACK 201',(4.5,-1.8),(-4.5,-1.8),GREEN,2)
                marker=self._own(text('next expected = 201',0,1.3,31,GREEN));self._draw(b,marker,1)
                q=self.state['arrived'][0];b.append((1,lambda:(q[0].animate.set_stroke(GREEN),q[1].animate.set_color(GREEN))))
            elif i==10:
                self._receive_bytes(b,2,1.8)
                gap=self._own(packet('201–300 ?',RED,2.35,.6).move_to([0,-.4,0]));self._draw(b,gap,.8)
                self._flight(b,'ACK 201',(4.5,-1.8),(-4.5,-1.8),GREEN,1.5)
                hold=self._own(text('301–400 waits behind the gap',2.2,.65,25,YELLOW,6));self._draw(b,hold,1)
            elif i in (11,20):
                for j in (0,2):
                    if j not in self.state['arrived']:self._receive_bytes(b,j,.8)
                self._receive_bytes(b,1,1.8)
                for j in range(3):
                    q=self.state['arrived'][j]
                    target=q.copy().shift(.7*m.DOWN)
                    target[0].set_stroke(GREEN);target[1].set_color(GREEN)
                    b.append((.9,lambda q=q,target=target:m.Transform(q,target)))
                self._flight(b,'ACK 401',(4.5,-1.9),(-4.5,-1.9),GREEN,1.6)
                self._caption(b,'Contiguous bytes can now reach the application',-2.6,GREEN,.8)
            else:
                # A separate head-of-line illustration begins with its own clean buffer.
                for j in (0,2):
                    if j not in self.state['arrived']:self._receive_bytes(b,j,1.3)
                gap=self._own(m.Rectangle(width=2.7,height=.85,color=RED,stroke_width=3).move_to([0,-.4,0]));b.append((1.5,lambda:m.Create(gap)))
                self._flight(b,'ACK 201',(4.5,-1.8),(-4.5,-1.8),GREEN,1.4)
                self._caption(b,'Later bytes wait for the missing range',-2.55,RED,1)
            return
        if i==12:
            self._timeline(b);self._messages(b,[('101–200 delivered','right',BLUE,False),('ACK 201','left',GREEN,True),('101–200 again','right',YELLOW,False),('ACK 201 repeated','left',GREEN,False)])
            self._caption(b,'One application delivery, despite duplicate arrival',-2.6,GREEN)
            return
        if i in (14,15):
            self._receive_capacity(b);counter=self.state['counter']
            if i==14:
                for j in range(2):
                    q=self._own(packet('100 B',BLUE,1.3,.55).move_to([-5,-.3,0]),True);self.state['filled'].append(q);self._draw(b,q,.2);self._move(b,q,(.5+j*1.8,0),1.4)
                    new=text(f'rwnd = {200-j*100} bytes',2.3,-1.35,28,GREEN);self._change(b,counter,new,.8)
                self._flight(b,'rwnd 100',(4.5,-2.05),(-4.5,-2.05),GREEN,1.5)
            else:
                if len(self.state['filled'])<2:
                    for j in range(2):
                        q=self._own(packet('100 B',BLUE,1.3,.55).move_to([.5+j*1.8,0,0]),True);self.state['filled'].append(q);self._draw(b,q,.4)
                q=self._own(packet('100 B',BLUE,1.3,.55).move_to([-5,0,0]),True);self.state['filled'].append(q);self._draw(b,q,.3);self._move(b,q,(4.1,0),1.3)
                self._change(b,counter,text('rwnd = 0 bytes',2.3,-1.35,28,RED),.7)
                for q in self.state['filled'][:2]:
                    self._move(b,q,(q.get_x(),-2.1),1);b.append((.4,lambda q=q:m.FadeOut(q)))
                self._change(b,counter,text('rwnd = 200 bytes',2.3,-1.35,28,GREEN),1)
            return
        if i==16:
            self._ensure('congestion')
            nodes=self._own(m.VGroup(host('Sender',-5,1.2),host('Router',0,1.2,YELLOW),host('Receiver',5,1.2,GREEN)));self._draw(b,nodes)
            slots=self._own(m.VGroup(*[m.Rectangle(width=.85,height=.6,color=MUTED).move_to([-1.5+j,0,0]) for j in range(4)]));b.append((.8,lambda:m.Create(slots)))
            receive=self._own(text('rwnd 1000',4.7,-1.3,24,GREEN));congestion=self._own(text('cwnd 400',-4.5,-1.3,24,YELLOW));self._draw(b,m.Group(receive,congestion))
            for j in range(4):self._flight(b,'100 B',(-5,0),(-1.5+j,0),BLUE,.8,keep=True)
            self._flight(b,'extra',(-3,.0),(3,.0),RED,1.1,True)
            self._change(b,congestion,text('cwnd 200',-4.5,-1.3,24,RED),1)
            self._caption(b,'Receiver space and path congestion are different limits',-2.45)
            return
        self._ensure('datagrams')
        nodes=self._own(m.VGroup(host('Application A',-5,1.5),host('Application B',5,1.5,GREEN)));self._draw(b,nodes,.5)
        if i==18:
            self._flight(b,'datagram 1',(-4.8,.8),(4.8,.8),BLUE,1.2,True)
            self._flight(b,'app retry',(-4.8,.0),(4.8,.0),YELLOW,1.5)
            self._flight(b,'app ACK',(4.8,-.8),(-4.8,-.8),GREEN,1.2)
            self._caption(b,'Applications can add reliability above UDP',-2.4)
        elif i==21:
            latest=self._own(text('latest position: ?',2.5,-1.7,28,GREEN));self._draw(b,latest,.5)
            for j in range(3):
                self._flight(b,f't={j+1}',(-4.8,.6-j*.65),(4.8,.6-j*.65),BLUE,1.1,j==0)
                if j:self._change(b,latest,text(f'latest position: t={j+1}',2.5,-1.7,28,GREEN),.6)
        elif i in (0,19,23):
            for j,(word,col,lost) in enumerate((('UDP data',BLUE,True),('TCP retry',GREEN,False))):
                self._flight(b,word,(-4.8,.6-j*1.3),(4.8,.6-j*1.3),col,2,lost)
            self._caption(b,'Choose required behavior, not a universal speed label',-2.4)
        else:
            for j,name in enumerate(('ONE','TWO','THREE')):
                self._flight(b,name,(-4.8,.7-j*.9),(4.8,.7-j*.9),BLUE,1.3,lost=(i==17 and j==1))
            if i==17:self._caption(b,'UDP itself does not retransmit the missing datagram',-2.6,RED)
