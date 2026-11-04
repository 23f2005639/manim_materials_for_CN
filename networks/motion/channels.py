"""Full-canvas motion studies for multiplexing and shared-medium access.

The diagrams persist between related sections. Moving signals, sampled traffic,
receiver recovery and actual contention decisions carry the explanation.
"""
from __future__ import annotations
import math
import numpy as np
import manimgx as m

BG="#080A10"; BLUE="#58C4DD"; GREEN="#83C167"; YELLOW="#FFFF00"; RED="#FC6255"; WHITE="#F2F2F2"; DIM="#596273"
COLORS=(BLUE,GREEN,YELLOW,"#B68CFF")


def text(s,x,y,size=27,color=WHITE):
    obj=m.Text(str(s),font="Noto Sans",font_size=size,color=color).move_to([x,y,0])
    obj.annotation_anchor=(x,y)
    return obj


def line(a,b,color=DIM,width=2):
    return m.Line([*a,0],[*b,0],color=color,stroke_width=width)


def arrow(a,b,color=WHITE):
    return m.Arrow([*a,0],[*b,0],buff=.03,color=color,stroke_width=2,max_tip_length_to_length_ratio=.08)


def token(s,x,y,color=BLUE,width=.66):
    body=m.Rectangle(width=width,height=.44,color=color,stroke_width=1.8,fill_color=BG,fill_opacity=1).move_to([x,y,0])
    return m.VGroup(body,text(s,x,y,22,color)).set_z_index(5)


class ChannelDirector:
    def __init__(self,scene,episode_id):
        self.scene=scene;self.episode=str(episode_id).zfill(2)
        self.group=None;self.stage=None;self.phase=m.ValueTracker(0)
        scene.add(self.phase)
        self.received=[[],[],[]];self.sequence=[0,0,0]

    def _switch(self,name,builder):
        if self.stage==name:return
        if self.group is not None:
            self.group.clear_updaters()
            self.scene.play(m.FadeOut(self.group),run_time=.3)
            self.scene.remove(self.group)
        self.phase.set_value(0)
        self.group=builder()
        self.stage=name
        self.scene.play(m.Create(self.group),run_time=1.0)

    def _wave(self,x0,x1,y,color,frequency=3,amplitude=.2,offset=0,noise=0):
        xs=np.linspace(x0,x1,96)
        curve=m.VMobject(color=color,stroke_width=2.6)
        def update(obj):
            t=self.phase.get_value()
            xx=(xs-x0)/(x1-x0)
            yy=y+amplitude*np.sin(m.TAU*(frequency*xx-t+offset))
            if noise:yy+=noise*np.sin(m.TAU*(19*xx-2.3*t))
            obj.set_points_as_corners(np.column_stack((xs,yy,np.zeros_like(xs))))
        update(curve);curve.add_updater(update)
        return curve

    def _phase_for(self,duration,speed=.45):
        if duration<=.001:return
        self.scene.play(self.phase.animate.set_value(self.phase.get_value()+duration*speed),run_time=duration,rate_func=m.linear)

    def _remaining(self,start,budget):
        return max(.001,budget-(self.scene.time-start))

    def animate(self,index,section,budget):
        start=self.scene.time
        if self.episode=="02":self._multiplex(index,section,budget,start)
        elif self.episode=="04":self._access(index,section,budget,start)
        else:raise ValueError("ChannelDirector handles only episodes 02 and 04")

    # ── Multiplexing: a single persistent physical path is used throughout. ──
    def _mux_network(self):
        g=m.VGroup()
        ys=(1.55,0,-1.55)
        for j,y in enumerate(ys):
            g.add(text(chr(65+j),-6.1,y,30,COLORS[j]))
            g.add(self._wave(-5.7,-2.8,y,COLORS[j],2+j,.2))
            g.add(self._wave(2.8,5.8,y,COLORS[j],2+j,.2))
            g.add(text(chr(65+j),6.15,y,30,COLORS[j]))
            g.add(line((-2.8,y),(-2.1,0),COLORS[j]),line((2.1,0),(2.8,y),COLORS[j]))
        g.add(m.Polygon([-2.65,1.0,0],[-1.7,0,0],[-2.65,-1.,0],color=WHITE,fill_color=BG,fill_opacity=1,stroke_width=2))
        g.add(m.Polygon([2.65,1.,0],[1.7,0,0],[2.65,-1.,0],color=WHITE,fill_color=BG,fill_opacity=1,stroke_width=2))
        xs=np.linspace(-1.6,1.6,144);curve=m.VMobject(color=WHITE,stroke_width=3)
        def combined(obj):
            q=(xs+1.6)/3.2;t=self.phase.get_value()
            yy=sum(.19*np.sin(m.TAU*((j+2)*q-t)) for j in range(3))
            obj.set_points_as_corners(np.column_stack((xs,yy,np.zeros_like(xs))))
        combined(curve);curve.add_updater(combined);g.add(curve)
        g.add(text("MUX",-2.2,-2.35,25),text("DEMUX",2.2,-2.35,25))
        return g

    def _fdm(self):
        g=m.VGroup()
        self.fdm_active=[1,1,1]
        g.add(arrow((-5.7,-1.25),(5.8,-1.25),WHITE),text("kHz",6.05,-1.7,23))
        def X(f):return -5.4+10.8*f/70
        self.bands=[]
        for j,(a,b) in enumerate(((0,20),(25,45),(50,70))):
            band=m.Rectangle(width=X(b)-X(a),height=1.5,color=COLORS[j],fill_color=COLORS[j],fill_opacity=.10,stroke_width=2).move_to([(X(a)+X(b))/2,-.45,0])
            self.bands.append(band);g.add(band,text(chr(65+j),(X(a)+X(b))/2,.65,32,COLORS[j]))
            xs=np.linspace(X(a)+.07,X(b)-.07,64);trace=m.VMobject(color=COLORS[j],stroke_width=2.7)
            def energy(obj,xs=xs,a=a,b=b,j=j):
                q=(xs-X(a))/(X(b)-X(a));t=self.phase.get_value()
                yy=-1.15+self.fdm_active[j]*(.45+.38*np.sin(np.pi*q)**2+.15*np.sin(2*m.PI*(3*q-t)))
                obj.set_points_as_corners(np.column_stack((xs,yy,np.zeros_like(xs))))
            energy(trace);trace.add_updater(energy);g.add(trace)
        for f in (0,20,25,45,50,70):g.add(line((X(f),-1.25),(X(f),-1.4),WHITE),text(str(f),X(f),-1.7,22))
        self.guards=m.VGroup(*[m.Rectangle(width=X(b)-X(a),height=1.5,color=DIM,fill_color=DIM,fill_opacity=.12,stroke_width=1).move_to([(X(a)+X(b))/2,-.45,0]) for a,b in ((20,25),(45,50))])
        g.add(self.guards)
        xs=np.linspace(-5.4,5.4,192);composite=m.VMobject(color=WHITE,stroke_width=2.2)
        def sumwave(obj):
            q=(xs+5.4)/10.8;t=self.phase.get_value()
            yy=1.6+sum(self.fdm_active[j]*.12*np.sin(m.TAU*((j+2)*q-t)) for j in range(3))
            obj.set_points_as_corners(np.column_stack((xs,yy,np.zeros_like(xs))))
        sumwave(composite);composite.add_updater(sumwave);g.add(composite)
        self.fdm_note=text("",0,2.25,25)
        self.formula=text("",0,-2.4,27,YELLOW)
        g.add(self.fdm_note,self.formula)
        return g

    def _change_text(self,obj,value,color=WHITE,size=26):
        target=text(value,*getattr(obj,"annotation_anchor",obj.get_center()[:2]),size,color)
        self.scene.play(m.Transform(obj,target),run_time=.4)

    def _tdm(self):
        g=m.VGroup()
        self.received=[[],[],[]];self.sequence=[0,0,0]
        self.tdm_ys=(1.4,0,-1.4)
        for j,y in enumerate(self.tdm_ys):
            g.add(text(chr(65+j),-6.1,y,30,COLORS[j]),text(chr(65+j),6.15,y,30,COLORS[j]))
            g.add(line((-5.75,y),(-2.4,0),COLORS[j]),line((3.,0),(5.65,y),COLORS[j]))
        g.add(line((-2.4,0),(3.,0),WHITE,3),text("MUX",-2.5,-2.45,24),text("DEMUX",3.,-2.45,24))
        self.slots=m.VGroup(*[token(chr(65+j%3),-1.8+j*.75,2.,COLORS[j%3],.65) for j in range(6)])
        self.slot_cursor=m.Rectangle(width=.73,height=.56,color=WHITE,stroke_width=2).move_to([-1.8,2.,0])
        g.add(self.slots,self.slot_cursor)
        self.tdm_formula=text("",0,-2.55,26,YELLOW);g.add(self.tdm_formula)
        return g

    def _tdm_send(self,source,slot,duration,idle=False):
        y=self.tdm_ys[source]
        if not idle:self.sequence[source]+=1
        value="" if idle else chr(65+source)+str(self.sequence[source])
        packet=token(value,-5.45,y,DIM if idle else COLORS[source],.73)
        self.group.add(packet);self.scene.add(packet)
        if len(self.received[source])>=3 and not idle:
            old=self.received[source].pop(0);self.group.remove(old);self.scene.remove(old)
        first=[packet.animate.move_to([-2.4,0,0]),self.slot_cursor.animate.move_to([-1.8+slot*.75,2.,0])]
        if not idle:
            for j,old in enumerate(self.received[source]):first.append(old.animate.move_to([4.1+j*.68,y,0]))
        self.scene.play(*first,run_time=duration*.25,rate_func=m.linear)
        self.scene.play(packet.animate.move_to([3.,0,0]),run_time=duration*.48,rate_func=m.linear)
        if idle:
            self.scene.play(m.FadeOut(packet),run_time=duration*.27)
            self.scene.remove(packet);self.group.remove(packet)
        else:
            target=4.1+len(self.received[source])*.68
            self.scene.play(packet.animate.move_to([target,y,0]),run_time=duration*.27,rate_func=m.linear)
            self.received[source].append(packet)

    def _wdm(self,count=3):
        g=m.VGroup();ys=np.linspace(1.65,-1.65,count)
        for j,y in enumerate(ys):
            col=COLORS[j]
            g.add(text("λ"+str(j+1),-6.15,y,26,col),text("λ"+str(j+1),6.15,y,26,col))
            g.add(self._wave(-5.65,-2.95,y,col,3+j,.16),self._wave(2.95,5.65,y,col,3+j,.16))
            g.add(line((-2.95,y),(-2.2,(j-(count-1)/2)*.19),col),line((2.2,(j-(count-1)/2)*.19),(2.95,y),col))
            g.add(self._wave(-2.2,2.2,(j-(count-1)/2)*.19,col,4+j,.055))
        fiber=m.RoundedRectangle(width=4.8,height=1.05,corner_radius=.2,color=DIM,stroke_width=2).move_to([0,0,0]);g.add(fiber)
        self.optical_note=text("",0,2.25,26,YELLOW);g.add(self.optical_note)
        return g

    def _comparison(self):
        g=m.VGroup();self.compare_markers=[]
        for j,(name,x) in enumerate((("FDM",-4.35),("TDM",0),("WDM",4.35))):g.add(text(name,x,2.15,32,COLORS[j]))
        for j in range(3):
            g.add(self._wave(-6.,-2.7,1-j*.8,COLORS[j],2+j,.18))
            g.add(self._wave(2.7,6.,(j-1)*.24,COLORS[j],3+j,.07))
        self.compare_slots=m.VGroup(*[token(chr(65+j%3),-1.05+(j%3)*.85,1.1-(j//3)*.85,COLORS[j%3],.65) for j in range(9)])
        marker=m.Dot([-1.05,1.5,0],color=WHITE,radius=.08)
        def step(obj):
            k=int(self.phase.get_value()*2)%9
            obj.move_to([-1.05+(k%3)*.85,1.5-(k//3)*.85,0])
        marker.add_updater(step);g.add(self.compare_slots,marker)
        g.add(text("frequency",-4.35,-2.1,25),text("time",0,-2.1,25),text("wavelength",4.35,-2.1,25))
        return g

    def _multiplex(self,i,section,budget,start):
        if i<=2:
            self._switch("mux",self._mux_network)
            self._phase_for(self._remaining(start,budget),.5)
        elif i<=8:
            self._switch("fdm",self._fdm)
            self.fdm_active=[1,1,1]
            if i==5:
                self.scene.play(self.guards.animate.set_fill(YELLOW,opacity=.28),run_time=.7)
                self._change_text(self.fdm_note,"5 kHz",YELLOW)
            elif i==6:
                self.fdm_active=[.12,1,.12]
                self._change_text(self.fdm_note,"B",GREEN,32)
            elif i==7:self._change_text(self.formula,"20 + 5 + 20 + 5 + 20 = 70 kHz",YELLOW,28)
            elif i==8:
                self.fdm_active=[1,0,1]
                self._change_text(self.fdm_note,"B: idle",DIM)
            self._phase_for(self._remaining(start,budget),.55)
        elif i<=15:
            self._switch("tdm",self._tdm)
            order=(0,0,2,0,2,2) if i==15 else (0,1,2,0,1,2)
            slots=m.VGroup(*[token(chr(65+k),-1.8+j*.75,2.,COLORS[k],.65) for j,k in enumerate(order)])
            self.scene.play(m.Transform(self.slots,slots),run_time=.45)
            if i==13:self._change_text(self.tdm_formula,"3 × 2 Mb/s = 6 Mb/s",YELLOW)
            if i==14:self._change_text(self.tdm_formula,"B: idle",DIM)
            if i==15:self._change_text(self.tdm_formula,"A  A  C  A  C  C",YELLOW)
            duration=self._remaining(start,budget)/len(order)
            for j,k in enumerate(order):self._tdm_send(k,j,duration,idle=(i==14 and k==1))
        elif i<=20:
            count=4 if i>=19 else 3
            self._switch("wdm"+str(count),lambda:self._wdm(count))
            if i==19:self._change_text(self.optical_note,"4 × 10 Gb/s = 40 Gb/s",YELLOW)
            elif i==20:self._change_text(self.optical_note,"attenuation · dispersion · noise",WHITE,25)
            self._phase_for(self._remaining(start,budget),.65)
        else:
            self._switch("comparison",self._comparison)
            self._phase_for(self._remaining(start,budget),.6)

    # ── Shared medium: arrivals and wavefronts determine the outcomes. ──
    def _bus(self):
        g=m.VGroup(line((-5.8,0),(5.8,0),WHITE,2))
        for x,name,col in ((-5,"A",BLUE),(0,"B",GREEN),(5,"C",YELLOW)):
            g.add(line((x,0),(x,1.5),DIM),m.Circle(radius=.23,color=col,fill_color=BG,fill_opacity=1).move_to([x,1.7,0]),text(name,x,2.17,27,col))
        return g

    def _remove(self,*objs):
        for obj in objs:
            obj.clear_updaters();self.scene.remove(obj);self.group.remove(obj)

    def _flight(self,duration,sender=-5,direction=1,color=BLUE):
        tracer=m.VMobject(color=color,stroke_width=4)
        dot=m.Dot([sender,0,0],color=color,radius=.10)
        local=m.ValueTracker(0);self.scene.add(local)
        def update(obj):
            t=local.get_value();front=sender+direction*10*t
            back=sender+direction*max(0,10*t-2.0)
            obj.set_points_as_corners(np.array([[back,0,0],[front,0,0]]))
        tracer.add_updater(update)
        dot.add_updater(lambda o:o.move_to([sender+direction*10*local.get_value(),0,0]))
        self.group.add(tracer,dot);self.scene.add(tracer,dot)
        self.scene.play(local.animate.set_value(1),run_time=duration,rate_func=m.linear)
        self._remove(tracer,dot);self.scene.remove(local)

    def _collision(self,duration,delay=.10):
        local=m.ValueTracker(0);self.scene.add(local)
        speed=12.;hit=(10/speed+delay)/2;point=-5+speed*hit
        a=m.VMobject(color=BLUE,stroke_width=4);c=m.VMobject(color=YELLOW,stroke_width=4)
        jam=m.VMobject(color=RED,stroke_width=5)
        cross=m.VGroup(line((point-.17,-.17),(point+.17,.17),RED,3),line((point-.17,.17),(point+.17,-.17),RED,3))
        def front(obj,side):
            t=min(local.get_value(),hit)
            if side==0:xs=(-5,max(-5,-5+speed*t))
            else:xs=(5,min(5,5-speed*max(0,t-delay)))
            obj.set_points_as_corners(np.array([[xs[0],0,0],[xs[1],0,0]]))
            obj.set_opacity(1 if local.get_value()<hit else .08)
        a.add_updater(lambda o:front(o,0));c.add_updater(lambda o:front(o,1))
        def red(obj):
            t=max(0,local.get_value()-hit);reach=12*t
            obj.set_points_as_corners(np.array([[max(-5.8,point-reach),0,0],[min(5.8,point+reach),0,0]]))
            obj.set_opacity(1 if t else 0)
        jam.add_updater(red);cross.add_updater(lambda o:o.set_opacity(1 if local.get_value()>=hit else 0))
        self.group.add(a,c,jam,cross);self.scene.add(a,c,jam,cross)
        self.scene.play(local.animate.set_value(1),run_time=duration,rate_func=m.linear)
        self._remove(a,c,jam,cross);self.scene.remove(local)

    def _aloha(self,slotted=False,vulnerable=False):
        g=m.VGroup();self.arrival_specs=[]
        starts=(2,2,8) if slotted else (2,3.2,8)
        for j,y in enumerate((1.35,0,-1.35)):
            g.add(text(chr(65+j),-6.,y,28,COLORS[j]),line((-5.3,y),(5.6,y),DIM))
            if slotted:
                for k in range(7):g.add(line((-5.2+k*1.8,y-.28),(-5.2+k*1.8,y+.28),DIM,1))
            box=m.Rectangle(width=.01,height=.54,color=COLORS[j],fill_color=COLORS[j],fill_opacity=.24,stroke_width=2)
            self.arrival_specs.append((box,starts[j],y,j))
            g.add(box)
        self.cursor=line((-5.2,-1.8),(-5.2,1.85),WHITE,1.5);g.add(self.cursor)
        if vulnerable:
            width=1.8 if slotted else 3.6;x=-5.2+starts[0]*.9
            center=x+.9 if slotted else x
            g.add(m.Rectangle(width=width,height=.28,color=YELLOW,fill_color=YELLOW,fill_opacity=.18).move_to([center,-2.2,0]),text("T" if slotted else "2T",center,-2.62,26,YELLOW))
        g.add(text("time",5.7,-2.2,24,DIM))
        return g

    def _play_arrivals(self,duration):
        local=m.ValueTracker(0);self.scene.add(local)
        for box,start,y,j in self.arrival_specs:
            def grow(obj,start=start,y=y,j=j):
                t=local.get_value();length=max(.001,min(2,t-start))*.9
                shape=m.Rectangle(width=length,height=.54,color=RED if j<2 and t>=max(self.arrival_specs[0][1],self.arrival_specs[1][1]) else COLORS[j],fill_color=COLORS[j],fill_opacity=.22,stroke_width=2).move_to([-5.2+start*.9+length/2,y,0])
                obj.become(shape);obj.set_opacity(1 if t>=start else 0)
            box.add_updater(grow)
        self.cursor.add_updater(lambda o:o.put_start_and_end_on([-5.2+.9*local.get_value(),-1.8,0],[-5.2+.9*local.get_value(),1.85,0]))
        self.scene.play(local.animate.set_value(12),run_time=duration,rate_func=m.linear)
        for obj,_,_,_ in self.arrival_specs:obj.clear_updaters()
        self.cursor.clear_updaters();self.scene.remove(local)

    def _throughput(self):
        g=m.VGroup(arrow((-5.3,-1.85),(5.5,-1.85)),arrow((-5.3,-1.85),(-5.3,2.0)),text("G",5.8,-1.85,27),text("S",-5.3,2.3,27))
        self.curve_dots=[]
        for j,factor in enumerate((2,1)):
            xs=np.linspace(0,3,160);yy=xs*np.exp(-factor*xs)
            path=m.VMobject(color=COLORS[j],stroke_width=3).set_points_as_corners(np.column_stack((-5.2+3.45*xs,-1.85+8*yy,np.zeros_like(xs))))
            dot=m.Dot([-5.2,-1.85,0],radius=.11,color=COLORS[j]);self.curve_dots.append((dot,factor));g.add(path,dot)
        g.add(text("1/(2e) ≈ 18.4%",-2,2.2,25,BLUE),text("1/e ≈ 36.8%",3,2.2,25,GREEN))
        return g

    def _move_throughput(self,duration):
        local=m.ValueTracker(0);self.scene.add(local)
        for dot,factor in self.curve_dots:
            dot.add_updater(lambda o,f=factor:o.move_to([-5.2+3.45*local.get_value(),-1.85+8*local.get_value()*math.exp(-f*local.get_value()),0]))
        self.scene.play(local.animate.set_value(3),run_time=duration,rate_func=m.linear)
        for dot,_ in self.curve_dots:dot.clear_updaters()
        self.scene.remove(local)

    def _sense(self,duration,persistence):
        local=m.ValueTracker(0);self.scene.add(local)
        cursor=line((-5.2,-1.7),(-5.2,-1.1),WHITE,2)
        busy=m.Rectangle(width=4.5,height=.32,color=RED,fill_color=RED,fill_opacity=.24).move_to([-2.95,-1.4,0])
        labels=m.VGroup(text("busy",-3,-2.,24,RED),text("idle",2,-2.,24,GREEN))
        moving=m.Dot([5,0,0],color=YELLOW,radius=.13)
        pending=token("A",-5,.8,BLUE)
        start={"one":.45,"non":.65,"p":.75}.get(persistence,.45)
        def sender(obj):
            t=local.get_value()
            if t<start:obj.move_to([-5,.8,0])
            else:obj.move_to([-5+10*min(1,(t-start)/(1-start)),0,0])
        pending.add_updater(sender)
        moving.add_updater(lambda o:o.move_to([5-10*min(1,local.get_value()/.45),0,0]).set_opacity(1 if local.get_value()<.45 else 0))
        cursor.add_updater(lambda o:o.move_to([-5.2+10.4*local.get_value(),-1.4,0]))
        self.group.add(cursor,busy,labels,moving,pending);self.scene.add(cursor,busy,labels,moving,pending)
        self.scene.play(local.animate.set_value(1),run_time=duration,rate_func=m.linear)
        self._remove(cursor,busy,labels,moving,pending);self.scene.remove(local)

    def _backoff(self):
        g=m.VGroup();self.backoff_cells=[]
        for j,count in enumerate((2,4,8)):
            y=1.4-j*1.15
            g.add(text("k="+str(j+1),-5.6,y,27,COLORS[j]))
            cells=m.VGroup(*[token(str(k),-3.5+k*.95,y,COLORS[j],.72) for k in range(count)])
            self.backoff_cells.append(cells);g.add(cells)
        g.add(text("0 … 2ᵏ − 1",0,-2.45,30,WHITE))
        return g

    def _choose_backoff(self,duration):
        dots=m.VGroup(m.Dot([-3.5,1.8,0],color=BLUE,radius=.12),m.Dot([-3.5,-1.3,0],color=RED,radius=.12))
        self.group.add(dots);self.scene.add(dots)
        paths=[(-3.5,1.8),(-2.55,1.8),(-3.5,.65),(-.65,.65),(-2.55,-.5),(2.2,-.5)]
        for j in range(3):
            self.scene.play(dots[0].animate.move_to([*paths[2*j],0]),dots[1].animate.move_to([*paths[2*j+1],0]),run_time=duration*.18,rate_func=m.linear)
            # Different choices count down along the row to the next attempt.
            self.scene.play(dots[0].animate.shift(.55*m.DOWN),dots[1].animate.shift(.55*m.DOWN),run_time=duration*(1/3-.18),rate_func=m.linear)
        self._remove(dots)

    def _duplex(self):
        g=m.VGroup(text("A",-5.7,0,32,BLUE),text("B",5.7,0,32,GREEN),m.Circle(radius=.45,color=WHITE).move_to([0,0,0]))
        for a,b,y,col in ((-5,-.5,.3,BLUE),(.5,5,.3,BLUE),(-.5,-5,-.3,GREEN),(5,.5,-.3,GREEN)):
            g.add(arrow((a,y),(b,y),col))
        self.duplex_dots=[]
        for j in range(8):
            dot=m.Dot([0,0,0],radius=.09,color=BLUE if j<4 else GREEN)
            def move(obj,j=j):
                f=(self.phase.get_value()*.25+(j%4)/4)%1
                x=-5+10*f if j<4 else 5-10*f
                obj.move_to([x,.3 if j<4 else -.3,0])
            dot.add_updater(move);g.add(dot)
        g.add(text("full duplex",0,-2.25,28))
        return g

    def _wireless(self):
        return m.VGroup(text("A",-5,1.3,32,BLUE),text("AP",0,1.3,32,WHITE),text("C",5,1.3,32,YELLOW),m.Circle(radius=.18,color=BLUE).move_to([-5,0,0]),m.Circle(radius=.18,color=WHITE),m.Circle(radius=.18,color=YELLOW).move_to([5,0,0]))

    def _wireless_exchange(self,duration):
        local=m.ValueTracker(0);self.scene.add(local)
        waves=m.VGroup(*[m.Arc(radius=.02,start_angle=-.32,angle=.64,color=BLUE,stroke_width=2) for _ in range(3)])
        self.group.add(waves);self.scene.add(waves)
        def update(obj,j):
            t=local.get_value();leg=min(2,int(t*3));f=(t*3)%1
            if t>=1:leg=2;f=1
            origin=-5 if leg==0 else 0 if leg==1 else 5
            angle=-.32 if leg==0 else math.pi-.32
            col=BLUE if leg==0 else GREEN if leg==1 else YELLOW
            r=max(.02,min(5.,5*f-j*.7))
            obj.become(m.Arc(radius=r,start_angle=angle,angle=.64,color=col,stroke_width=2).shift(origin*m.RIGHT))
            obj.set_opacity(1 if f>j*.14 else 0)
        for j,w in enumerate(waves):w.add_updater(lambda o,j=j:update(o,j))
        self.scene.play(local.animate.set_value(1),run_time=duration,rate_func=m.linear)
        self._remove(waves);self.scene.remove(local)

    def _roundtrip(self,duration):
        local=m.ValueTracker(0);self.scene.add(local)
        a=m.Dot([-5,0,0],color=BLUE,radius=.12);b=m.Dot([5,0,0],color=RED,radius=.12)
        axis=line((-5,-1.65),(5,-1.65),DIM)
        labels=m.VGroup(text("0",-5,-2.15,25),text("τ",0,-2.15,25),text("2τ",5,-2.15,25),text("T ≥ 2τ",0,-2.6,29,YELLOW))
        cursor=m.Dot([-5,-1.65,0],color=YELLOW,radius=.09)
        a.add_updater(lambda o:o.move_to([-5+10*min(1,2*local.get_value()),0,0]).set_opacity(1 if local.get_value()<.5 else 0))
        b.add_updater(lambda o:o.move_to([5-10*max(0,2*local.get_value()-1),0,0]).set_opacity(1 if local.get_value()>=.5 else 0))
        cursor.add_updater(lambda o:o.move_to([-5+10*local.get_value(),-1.65,0]))
        self.group.add(a,b,axis,labels,cursor);self.scene.add(a,b,axis,labels,cursor)
        self.scene.play(local.animate.set_value(1),run_time=duration,rate_func=m.linear)
        self._remove(a,b,axis,labels,cursor);self.scene.remove(local)

    def _access(self,i,section,budget,start):
        if i in (2,3,5,6):
            slotted=i>=5;vulnerable=i in (3,6)
            self._switch("aloha"+str(slotted)+str(vulnerable),lambda:self._aloha(slotted,vulnerable))
            self._play_arrivals(self._remaining(start,budget))
        elif i==7:
            self._switch("throughput",self._throughput)
            self._move_throughput(self._remaining(start,budget))
        elif i in (17,18,19):
            self._switch("backoff",self._backoff)
            self._choose_backoff(self._remaining(start,budget))
        elif i==20:
            self._switch("duplex",self._duplex)
            self._phase_for(self._remaining(start,budget),.8)
        elif i==21:
            self._switch("wireless",self._wireless)
            self._wireless_exchange(self._remaining(start,budget))
        else:
            self._switch("bus",self._bus)
            rem=self._remaining(start,budget)
            if i in (1,10,14,15):self._collision(rem,.12 if i==10 else .02)
            elif i==16:self._roundtrip(rem)
            elif i in (9,11,12,13):self._sense(rem,"non" if i==12 else "p" if i==13 else "one")
            elif i==4:
                self._collision(rem*.25)
                self._sense(rem*.75,"non")
            else:
                self._flight(rem*.5,-5,1,BLUE)
                self._flight(rem*.5,5,-1,YELLOW)
