"""ACK-clocked slow start, with explicit illustrative round-trip assumptions."""
from .common import *
from .foundation import computer, photo


class Director(VisualDirector):
    def equation(self,value,color=YELLOW,y=-2.8):
        obj=self.own(text(value,0,y,29,color,12.6));self.play(m.FadeIn(obj),run_time=.7);return obj

    def network(self,bottleneck=False):
        nodes=self.own(m.VGroup(host('Sender',-5,.9),host('Receiver',5,.9,GREEN)))
        road=self.own(line((-4.6,.9),(4.6,.9),MUTED,2))
        neck=self.own(m.Rectangle(width=.75,height=.5,color=MUTED,stroke_width=2).move_to([0,.9,0]))
        name=self.own(text('bottleneck',0,1.65,23,MUTED,3))
        self.play(m.Create(road),m.FadeIn(nodes),run_time=.8)
        if bottleneck:self.play(m.FadeIn(neck),m.FadeIn(name),run_time=.7)

    def flight(self,value,direction='right',color=BLUE,seconds=1.4):
        y=.05 if direction=='right' else -.8
        a=(-4.6,y) if direction=='right' else (4.6,y)
        b=(4.6,y) if direction=='right' else (-4.6,y)
        obj=self.own(packet(value,color,.8 if value!='ACK' else 1.0,.42).move_to([*a,0]))
        trail=self.own(m.Arrow([*a,0],[*b,0],buff=.08,color=color,stroke_width=2,max_tip_length_to_length_ratio=.04))
        self.play(m.FadeIn(obj),run_time=.2)
        self.play(obj.animate.move_to([*b,0]),m.Create(trail),run_time=seconds)
        self.play(m.FadeOut(obj),m.FadeOut(trail),run_time=.2)

    def window(self,count,y=-1.8,active=None):
        active=count if active is None else active
        columns=min(count,16);step=.48
        cells=[]
        for i in range(count):
            x=(i%columns-(columns-1)/2)*step
            row_y=y-(i//columns)*.5
            cell=self.own(m.Rectangle(width=.4,height=.36,color=BLUE if i<active else YELLOW,
                         stroke_width=2,fill_color=BLUE if i<active else BG,fill_opacity=.25 if i<active else 1).move_to([x,row_y,0]))
            cells.append(cell)
        self.play(*(m.FadeIn(c) for c in cells),run_time=.8)
        return cells

    def count(self,value,y=2.35,color=BLUE):
        label=self.own(text(f'Allowance: {value} pieces',0,y,29,color,8));self.play(m.FadeIn(label),run_time=.6);return label

    def change_count(self,label,value):
        self.play(m.Transform(label,text(f'Allowance: {value} pieces',0,2.35,29,BLUE,8)),run_time=.65)

    def plot(self,values=(4,8,16,32),color=BLUE,axes=True,labels=True):
        if axes:
            self.s.add(self.own(line((-4.7,-2.0),(4.9,-2.0))),self.own(line((-4.7,-2.0),(-4.7,1.8))))
            for k in range(4):self.s.add(self.own(text(str(k),-4.2+2.8*k,-2.3,23,WHITE,1)))
            self.s.add(self.own(text('Growth rounds',0,-2.65,23,MUTED,5)))
            self.s.add(self.own(text('Window (segments)',-3,1.9,24,WHITE,5)))
        previous=None
        for k,value in enumerate(values):
            p=(-4.2+2.8*k,-1.9+value*.095)
            dot=self.own(m.Dot([*p,0],radius=.075,color=color))
            actions=[m.FadeIn(dot)]
            if previous is not None:
                segment=self.own(line(previous,p,color,3));actions.append(m.Create(segment))
            if labels:
                label=self.own(text(str(value),p[0],p[1]+.3,23,color,1.2));actions.append(m.FadeIn(label))
            self.play(*actions,run_time=1.3)
            previous=p
        return previous

    def animate(self,index,section,budget):
        self.reset()
        if index==0:
            sender=self.own(computer('Your computer',-4.8,.8))
            receiver=self.own(computer('Your friend',4.8,.8,GREEN))
            self.play(m.FadeIn(sender),run_time=.8)
            picture=self.own(photo(-4.8,.8));self.play(m.FadeIn(picture),run_time=.7)
            self.play(m.FadeIn(receiver),run_time=.8)
            wire=self.own(line((-3.8,.8),(3.8,.8)))
            self.play(m.Create(wire),run_time=1.3)
            self.play(m.FadeOut(picture),run_time=.4)
            pieces=[self.own(packet(str(i+1),BLUE,.65,.5).move_to([-5.8+i*.7,-.8,0])) for i in range(4)]
            self.play(*(m.FadeIn(q) for q in pieces),run_time=1)
            self.equation('A photo travels as smaller pieces',WHITE,y=-2)
            self.play(pieces[0].animate.move_to([4.8,-.8,0]),run_time=2.5)
            self.equation('TCP calls a data piece a segment',BLUE,y=-2.9)
        elif index==1:
            for obj in (computer('Sender',-5,.9),computer('Receiver',5,.9,GREEN)):
                self.play(m.FadeIn(self.own(obj)),run_time=.7)
            self.flight('1',seconds=2.3)
            meaning=self.equation('Received it!',GREEN,y=2.2)
            self.flight('ACK','left',GREEN,2.3)
            self.equation('ACK = acknowledgment = a receipt for data',GREEN)
        elif index==2:
            self.network();cells=self.window(4,active=0)
            self.equation('Room for 4 unconfirmed pieces',WHITE,y=2.35)
            for cell in cells:self.play(m.Indicate(cell),run_time=.65)
            self.equation('Congestion window (cwnd) = sending allowance',YELLOW)
        elif index==3:
            self.network();self.count(4);cells=self.window(4,active=0)
            for i,c in enumerate(cells):
                self.flight(str(i+1),seconds=1.2)
                self.play(c.animate.set_fill(BLUE,opacity=.35).set_stroke(BLUE),run_time=.4)
            self.equation('4 segments outstanding',BLUE)
        elif index==4:
            self.network();label=self.count(4)
            self.window(4)
            self.flight('ACK','left',GREEN,1.8)
            self.change_count(label,5)
            self.window(5,y=-2.4,active=3)
            self.equation('1 confirmed + 1 added = room for 2',GREEN,y=-3.15)
            self.flight('new 1',seconds=1);self.flight('new 2',seconds=1)
        elif index==5:
            self.network();label=self.count(4)
            for value in range(5,9):
                self.flight('ACK','left',GREEN,.9);self.change_count(label,value)
            self.window(8)
            self.equation('4 acknowledgments: 4 + 4 = 8',GREEN)
        elif index==6:
            self.network();label=self.count(4)
            for i in range(3):
                self.flight('ACK','left',GREEN,1.0);self.change_count(label,5+i)
                self.flight(str(5+i),seconds=1)
            self.equation('Returning ACKs help pace new sending',GREEN)
        elif index==7:
            self.plot()
            self.equation('W + W = 2W',YELLOW,y=2.55)
        elif index==8:
            self.plot()
            self.equation('W(k) = 4 × 2^k',YELLOW,y=2.55)
            for k,value in enumerate((4,8,16,32)):
                obj=self.own(text(f'k = {k}   →   {value}',3.8,1.95,25,YELLOW,3.5))
                self.play(m.FadeIn(obj),run_time=.5);self.play(m.FadeOut(obj),run_time=.5)
        elif index in (9,10):
            cells=self.window(16,y=1.5)
            a=self.equation('16 × 1000 bytes = 16000 bytes',BLUE,y=.65)
            clock=self.own(m.Circle(radius=.52,color=GREEN,stroke_width=3).move_to([-3.5,-.9,0]))
            hand=self.own(line((-3.5,-.9),(-3.5,-.46),GREEN,3))
            self.play(m.Create(clock),m.Create(hand),run_time=1)
            self.play(m.Rotate(hand,angle=-m.TAU,about_point=[-3.5,-.9,0]),run_time=2)
            delay=self.own(text('100 ms RTT',-3.5,-1.8,25,GREEN,3))
            rate=self.own(text('16000 B / 0.1 s = 160000 B/s',1.5,-.65,27,YELLOW,7.5))
            bits=self.own(text('× 8 = 1.28 Mb/s',1.5,-1.55,29,YELLOW,6.5))
            self.play(m.FadeIn(delay),m.FadeIn(rate),m.FadeIn(bits),run_time=1.5)
            if index==10:
                self.play(m.Transform(delay,text('200 ms RTT',-3.5,-1.8,25,GREEN,3)),
                          m.Transform(rate,text('16000 B / 0.2 s = 80000 B/s',1.5,-.65,27,YELLOW,7.5)),
                          m.Transform(bits,text('× 8 = 0.64 Mb/s',1.5,-1.55,29,YELLOW,6.5)),run_time=2)
            self.equation('Window-limited rate ≈ bytes / RTT',WHITE)
        elif index==11:
            self.network(bottleneck=True);self.count(32)
            queue=[]
            for j in range(8):
                q=self.own(packet(str(j+1),YELLOW,.43,.38).move_to([-4.6,.05,0]))
                self.play(m.FadeIn(q),run_time=.2)
                self.play(q.animate.move_to([-.6-j*.47,.05,0]),run_time=.9)
                queue.append(q)
            self.play(queue[0].animate.move_to([4.6,.05,0]),run_time=2)
            self.play(m.FadeOut(queue[0]),run_time=.3)
            self.flight('ACK','left',GREEN,2.2)
            self.equation('The bottleneck cannot serve unlimited arrivals',YELLOW)
        elif index==12:
            self.plot()
            threshold=self.own(line((-4.6,1.14),(4.85,1.14),RED,2))
            self.play(m.Create(threshold),run_time=1)
            self.equation('Illustrative threshold: ssthresh = 32',RED,y=2.45)
            self.equation('Reaching the boundary ends this growth phase',WHITE,y=-3.2)
        elif index==13:
            self.plot(labels=False)
            self.plot((8,16,32),GREEN,axes=False,labels=False)
            self.equation('Start at 8: reach 32 one round earlier',GREEN,y=2.4)
            a=self.own(text('Start 4',5.35,1.1,22,BLUE,1.8));b=self.own(text('Start 8',1.4,1.65,22,GREEN,1.8))
            self.play(m.FadeIn(a),m.FadeIn(b),run_time=.7)
        elif index==14:
            self.plot((4,8,16))
            p=(1.4,-1.9+16*.095)
            end=(4.2,p[1]);flat=self.own(line(p,end,MUTED,3))
            self.play(m.Create(flat),run_time=2)
            self.equation('No more application data: the ideal trace changes',WHITE,y=2.4)
        else:
            self.network();label=self.count(4)
            previous=4
            for target in (8,16):
                for value in range(previous+1,target+1):
                    self.flight('ACK','left',GREEN,.65)
                    self.change_count(label,value)
                self.flight('data',seconds=1.1)
                previous=target
            self.window(16)
            self.equation('Feedback → allowance → paced sending',GREEN)
        self.finish(budget)
