"""The queue itself explains throughput, delay, and the Q/R calculation."""
from .common import *


class Director(VisualDirector):
    def show(self, obj, duration=.7):
        self.own(obj);self.play(m.FadeIn(obj),run_time=duration);return obj

    def label(self, value, x=0, y=-2.35, color=WHITE, size=27):
        return self.show(text(value,x,y,size,color,11.5))

    def vanish(self, obj):
        self.play(m.FadeOut(obj),run_time=.4)
        self.s.remove(*obj.get_family())

    def box(self, value, x, y=.35, color=BLUE, width=.7):
        return packet(value,color,width,.48).move_to([x,y,0])

    def track(self, rate='20 Mb/s'):
        self.show(line((-5.7,.35),(5.7,.35)),.6)
        self.show(m.VGroup(line((3.6,-.35),(3.6,1.05),YELLOW,4),
                           text(rate,4.65,1.45,26,YELLOW,2.6)),.6)
        self.show(text('arrivals',-4.8,1.5,24,MUTED,2.6),.3)
        self.show(text('waiting data',-.6,1.5,24,WHITE,4),.3)

    def queue(self, count=6, y=.35, spacing=.85):
        out=[]
        for i in range(count):
            q=self.show(self.box(str(i+1),2.9-i*spacing,y),.22)
            out.append(q)
        return out

    def depart(self, q, duration=1.6):
        self.play(q.animate.move_to([5.35,q.get_y(),0]),run_time=duration,rate_func=m.linear)
        self.vanish(q)

    def bar(self, value,x,y,width,color):
        rect=m.Rectangle(width=max(.03,width),height=.55,color=color,fill_color=color,fill_opacity=.7).move_to([x,y,0])
        return self.show(m.VGroup(rect,text(value,x,y-.7,23,color,5)),.7)

    def animate(self,index,section,budget):
        self.reset()
        if index==0:
            self.track();qs=self.queue(6)
            speed=self.label('Lots of data leaves',0,-1.4,BLUE)
            for q in qs[:3]:self.depart(q,1.2)
            green=self.show(self.box('ping',-4.7,color=GREEN,width=1.05))
            self.play(green.animate.move_to([-2.5,.35,0]),run_time=2)
            self.vanish(speed);self.label('A tiny packet can still wait',0,-1.5,GREEN)
        elif index==1:
            self.track();qs=self.queue(4)
            g=self.show(self.box('small',-5,color=GREEN,width=1.05))
            self.play(g.animate.move_to([-1,.35,0]),run_time=2)
            self.label('First in → first out',0,-1.1)
            for q in qs:self.depart(q,1.5)
            self.depart(g,2)
        elif index==2:
            self.track();self.label('One output, one departure rhythm',0,-1.35)
            for i in range(5):
                q=self.show(self.box(str(i+1),2.9),.25)
                self.depart(q,1.65)
                tick=self.own(line((-3.8+i*1.8,-1.9),(-3.8+i*1.8,-2.2),BLUE,3))
                self.play(m.Create(tick),run_time=.4)
            self.label('Each turn occupies transmission time',0,-2.7,MUTED,24)
        elif index==3:
            self.track();self.label('No data waiting ahead',0,-1.4,GREEN)
            for i in range(3):
                q=self.show(self.box('ping',-5,color=GREEN,width=1.05))
                self.play(q.animate.move_to([3,.35,0]),run_time=2)
                self.depart(q,1.1)
            self.label('Baseline delay still exists',0,-2.4,MUTED,24)
        elif index==4:
            self.track();qs=[]
            for i in range(7):
                q=self.show(self.box(str(i+1),-5),.2)
                self.play(q.animate.move_to([2.9-i*.85,.35,0]),run_time=.8)
                qs.append(q)
            self.label('Arrivals > departures → queue grows',0,-1.4)
            self.depart(qs[0],1.5)
            self.label('Busy link ≠ short delay',0,-2.5,YELLOW)
        elif index==5:
            self.track();qs=self.queue(6)
            g=self.show(self.box('ping',-5,color=GREEN,width=1.05));self.play(g.animate.move_to([-2.5,.35,0]),run_time=1.5)
            self.label('Small packet, large amount ahead',0,-1.4,GREEN)
            for q in qs[:4]:self.depart(q,1.5)
            self.label('Its own size did not change',0,-2.4,MUTED,24)
        elif index==6:
            self.track();outline=self.show(m.Rectangle(width=5.8,height=1.05,color=MUTED).move_to([-.05,.35,0]))
            qs=self.queue(5);self.label('More room to wait',0,-1.5)
            self.play(outline.animate.stretch_to_fit_width(10),run_time=2)
            for i in range(3):self.show(self.box(str(6+i),-1.35-i*.85),.4)
            self.label('Same exit rate',4.2,-.9,YELLOW,24)
            self.depart(qs[0],2)
        elif index==7:
            self.track();self.queue(6)
            brace=self.own(m.BraceBetweenPoints([-1.8,-.2,0],[3.25,-.2,0],direction=m.DOWN))
            self.play(m.Create(brace),run_time=1)
            self.label('Q = bits waiting ahead',0,-1.15,BLUE)
            self.label('R = bits leaving each second',0,-1.95,YELLOW)
            self.label('waiting time ≈ Q / R',0,-2.8,WHITE,32)
        elif index==8:
            units=self.show(m.VGroup(*[m.Rectangle(width=.5,height=.65,color=BLUE,fill_color=BLUE,fill_opacity=.4).move_to([-2.1+i*.6,.5,0]) for i in range(8)]))
            self.label('1 byte = 8 bits',0,1.7,BLUE,32)
            for cell in units:self.play(m.Indicate(cell),run_time=.55)
            self.label('1 MB = 1,000,000 bytes',0,-.6)
            self.label('= 8,000,000 bits',0,-1.55,YELLOW,32)
            self.label('Decimal MB in this example',0,-2.6,MUTED,23)
        elif index==9:
            self.track();qs=self.queue(8,spacing=.7)
            self.label('Each blue block represents 1 Mbit',0,-.55,MUTED,23)
            clock=self.show(text('elapsed: 0 ms',0,2.25,29,GREEN,6))
            equation=self.label('8,000,000 bits ÷ 20,000,000 bits/s',0,-1.2,WHITE,29)
            self.play(m.Indicate(equation),run_time=1.4)
            for i,q in enumerate(qs):
                self.depart(q,1.0)
                self.play(m.Transform(clock,text(f'elapsed: {(i+1)*50} ms',0,2.25,29,GREEN,6)),run_time=.35)
            self.label('= 0.4 seconds',0,-2,BLUE,32)
            self.label('= 400 milliseconds waiting',0,-2.9,GREEN,30)
        elif index==10:
            specs=[('propagation',1.7,MUTED),('processing',.75,PURPLE),('queue: 400 ms',5.0,BLUE),('transmission',.7,YELLOW)]
            cursor=-5.4
            for name,width,col in specs:
                rect=self.own(m.Rectangle(width=width,height=.65,color=col,fill_color=col,fill_opacity=.55).move_to([cursor+width/2,.4,0]))
                self.play(m.GrowFromEdge(rect,m.LEFT),run_time=1.1)
                self.show(text(name,(-4.6,-1.5,1.6,4.7)[specs.index((name,width,col))],-.65,24,col,2.7),.4);cursor+=width+.12
            self.label('One wait is only part of the journey',0,1.65)
            self.label('A round trip can meet more queues',0,-2,MUTED,25)
        elif index==11:
            self.track();qs=self.queue(3)
            for i in range(3):
                self.depart(qs.pop(0),1.2)
                self.play(*(q.animate.shift(.85*m.RIGHT) for q in qs),run_time=.7)
                q=self.show(self.box('new',-4.4,width=.7),.3)
                self.play(q.animate.move_to([1.2,.35,0]),run_time=1.2)
                qs.append(q)
            self.label('Arrivals = departures',0,-1.2)
            self.label('A long queue can stay long',0,-2.2,BLUE,29)
        elif index==12:
            self.track();self.label('One burst, then quiet',0,-1.2,GREEN)
            qs=self.queue(5)
            for q in qs:self.depart(q,1.15)
            g=self.show(self.box('ping',-4.8,color=GREEN,width=1.05));self.play(g.animate.move_to([5.2,.35,0]),run_time=2)
            self.vanish(g);self.label('Temporary buffer ≠ persistent delay',0,-2.3,YELLOW,26)
        elif index==13:
            self.track();self.queue(7)
            limit=self.show(m.Rectangle(width=6.35,height=.95,color=RED).move_to([.3,.35,0]))
            q=self.show(self.box('new',-5,width=.9));self.play(q.animate.move_to([-3.7,.35,0]),run_time=1.6)
            cross=self.own(m.VGroup(line((-4,-.1),(-3.4,.8),RED,4),line((-4,.8),(-3.4,-.1),RED,4)))
            self.play(m.Create(cross),m.FadeOut(q),run_time=.8)
            self.label('Full buffer → a new arrival may drop',0,-1.5,RED)
            self.label('Loss and delay describe different outcomes',0,-2.5,MUTED,24)
        elif index==14:
            self.show(text('Long standing queue',0,2,27,BLUE));self.show(text('Shorter controlled queue',0,-.3,27,GREEN))
            rows=[]
            for y,count,col in ((1,8,BLUE),(-1.2,2,GREEN)):
                qs=[self.show(self.box('',2.7-j*.78,y,BLUE,.6),.17) for j in range(count)]
                g=self.show(self.box('ping',-4.5,y,GREEN,1.0))
                self.play(g.animate.move_to([2.7-count*.78-.7,y,0]),run_time=1.6)
                rows.append({'y':y,'queue':qs,'ping':g})
            # Both exits serve one queued item per turn; the shorter line clears first.
            for turn in range(3):
                leaving=[]
                for row in rows:
                    leaving.append(row['queue'].pop(0) if row['queue'] else row['ping'])
                self.play(*(q.animate.move_to([5.2,row['y'],0]) for q,row in zip(leaving,rows)),run_time=1.8,rate_func=m.linear)
                self.play(*(m.FadeOut(q) for q in leaving),run_time=.4)
                self.s.remove(*(member for q in leaving for member in q.get_family()))
                movers=[q for row in rows for q in row['queue']]
                movers.extend(row['ping'] for row in rows if row['ping'] not in leaving)
                if movers:self.play(*(q.animate.shift(.78*m.RIGHT) for q in movers),run_time=.5)
            self.label('Same outgoing rate; different waiting',0,-2.65,WHITE,27)
        elif index==15:
            self.track();qs=self.queue(5);g=self.show(self.box('ping',-4.8,color=GREEN,width=1.05))
            self.play(g.animate.move_to([-1.7,.35,0]),run_time=1.5)
            self.label('Throughput: how much gets through',0,-1.2,BLUE)
            self.label('Delay: how long this packet waits',0,-2.1,GREEN)
            for q in qs[:3]:self.depart(q,1.1)
            self.label('Ask how much is waiting ahead',0,-2.95,YELLOW,26)
        self.finish(budget)
