"""Packet boundaries, shared turns, and a measurable store-and-forward pipeline."""
from .common import *
from .foundation import computer, photo


class Director(VisualDirector):
    def show(self,obj,duration=.6):
        self.own(obj);self.play(m.FadeIn(obj),run_time=duration);return obj

    def label(self,value,x=0,y=-2.5,color=WHITE,size=27,width=12):
        return self.show(text(value,x,y,size,color,width))

    def vanish(self,obj):
        self.play(m.FadeOut(obj),run_time=.35);self.s.remove(*obj.get_family())

    def box(self,value,x,y=.25,color=BLUE,width=.78,height=.5):
        return packet(value,color,width,height).move_to([x,y,0])

    def path(self, y=.65):
        xs=(-5.1,-1.7,1.7,5.1)
        for a,b in zip(xs,xs[1:]):
            self.show(line((a+.38,y),(b-.38,y)),.35)
        for j,x in enumerate(xs):self.show(host(('Source','Switch A','Switch B','Receiver')[j],x,y,(BLUE,MUTED,MUTED,GREEN)[j]),.35)
        return xs

    def fly(self,q,x,y=None,seconds=1.4):
        self.play(q.animate.move_to([x,q.get_y() if y is None else y,0]),run_time=seconds,rate_func=m.linear)

    def timeline(self, count=6, y=-.2):
        x0=-5.1;dx=1.7
        self.show(line((x0,y),(x0+count*dx,y)),.4)
        for i in range(count+1):
            self.show(line((x0+i*dx,y-.12),(x0+i*dx,y+.12)),.1)
            self.show(text(str(i),x0+i*dx,y-.45,23,MUTED,1),.1)
        return x0,dx

    def slot(self, row, start, value, color=BLUE):
        rect=self.own(m.Rectangle(width=1.55,height=.48,color=color,fill_color=color,fill_opacity=.6).move_to([-5.1+(start+.5)*1.7,1.7-row*.9,0]))
        lab=self.own(text(value,rect.get_x(),rect.get_y(),22,WHITE,1.3))
        self.play(m.GrowFromEdge(rect,m.LEFT),m.FadeIn(lab),run_time=.75)
        return rect

    def animate(self,index,section,budget):
        self.reset()
        if index==0:
            self.show(computer('Your computer',-4.5,.7),.8)
            self.show(computer('Your friend',4.5,.7,GREEN),.8)
            picture=self.show(photo(-4.5,.7),.7)
            self.play(m.Create(self.own(line((-3.5,.7),(3.5,.7)))),run_time=1.3)
            self.label('A link is a connection',0,2.1,YELLOW)
            block=self.show(self.box('picture data',0,-.8,BLUE,5.5,.9),.8)
            self.play(m.Indicate(picture),m.Indicate(block),run_time=1.5)
            self.label('How should this data take its turn?',0,-2.3)
        elif index==1:
            giant=self.show(m.Rectangle(width=9.5,height=.8,color=BLUE,fill_color=BLUE,fill_opacity=.25).move_to([0,.5,0]))
            self.label('One picture',0,1.8,BLUE)
            markers=[]
            for x in (-2.375,0,2.375):
                marker=self.own(line((x,-.05),(x,1.05),YELLOW,3));markers.append(marker)
                self.play(m.Create(marker),run_time=.6)
            self.play(m.FadeOut(giant),*(m.FadeOut(q) for q in markers),run_time=.5)
            for i in range(4):
                x=-3.75+i*2.5
                self.show(self.box(str(i+1),x,.5,BLUE,1.5,.7),.4)
                self.show(m.Rectangle(width=.3,height=.7,color=YELLOW,fill_color=YELLOW,fill_opacity=.65).move_to([x-.95,.5,0]),.3)
            self.label('Handling information + data = a packet',0,-1.1)
            self.label('Numbers help us follow the pieces',0,-2.3,MUTED,24)
        elif index==2:
            self.show(line((-5.8,.5),(5.8,.5)))
            self.label('One shared link, shorter turns',0,1.75)
            for j,(value,col) in enumerate((('B1',BLUE),('G',GREEN),('B2',BLUE),('B3',BLUE))):
                q=self.show(self.box(value,-5,.5,col,1));self.fly(q,5,seconds=1.8);self.vanish(q)
                self.show(self.box(value,-3.6+j*2.4,-1.1,col,1),.3)
            self.label('Possible interleaving, not guaranteed fairness',0,-2.5,MUTED,24)
        elif index==3:
            self.label('Inside a packet: bits',0,2,BLUE)
            cells=[self.show(self.box(value,-3.5+j*.9,.7,BLUE,.65),.3) for j,value in enumerate('10110010')]
            self.show(line((-5,-.3),(5,-.3)),.5)
            for bit in cells[:4]:
                self.play(bit.animate.move_to([4.5,-.3,0]),run_time=.8)
                self.vanish(bit)
            self.label('More bits → a longer turn',0,-1.4,WHITE)
            self.label('More bits each second → a shorter turn',0,-2.4,YELLOW)
        elif index==4:
            self.label('1,500 bytes × 8 = 12,000 bits',0,1.6,BLUE,31)
            for i in range(8):self.show(m.Rectangle(width=.65,height=.65,color=BLUE,fill_color=BLUE,fill_opacity=.45).move_to([-2.7+i*.78,.4,0]),.3)
            equation=self.label('12,000 bits ÷ 10,000,000 bits/s',0,-.75)
            self.play(m.Indicate(equation),run_time=1.3)
            self.label('L / R = 0.0012 s = 1.2 ms',0,-1.7,YELLOW,31)
            self.label('Transmission only; travel time excluded',0,-2.7,MUTED,23)
        elif index==5:
            xs=self.path(.8);self.label('Receive the complete packet, then forward',0,-2.4)
            q=self.show(self.box('1',xs[0],-.35))
            self.fly(q,xs[1],seconds=2)
            buffer=self.show(m.Rectangle(width=1.25,height=1,color=YELLOW).move_to([xs[1],-.35,0]))
            self.play(m.Indicate(buffer),run_time=.8)
            self.fly(q,xs[2],seconds=2);self.fly(q,xs[3],seconds=2);self.vanish(q)
            self.label('Store-and-forward model',0,2.25,YELLOW,25)
        elif index==6:
            self.label('Three store-and-forward links',0,2.45,WHITE,28)
            for row in range(3):
                self.label('link '+str(row+1),-6,1.7-row*.9,MUTED,22,1.2)
                self.slot(row,row,'packet 1')
            self.label('1.2 ms + 1.2 ms + 1.2 ms = 3.6 ms',0,-1.75,YELLOW,29)
            self.label('Three equal-rate links; other delays excluded',0,-2.7,MUTED,23)
        elif index==7:
            xs=self.path(1.1)
            q1=self.show(self.box('1',xs[0],-.2,BLUE));self.fly(q1,xs[1],seconds=1.8)
            q2=self.show(self.box('2',xs[0],-.2,GREEN))
            self.play(q1.animate.move_to([xs[2],-.2,0]),q2.animate.move_to([xs[1],-.2,0]),run_time=2,rate_func=m.linear)
            q3=self.show(self.box('3',xs[0],-.2,YELLOW))
            self.play(q1.animate.move_to([xs[3],-.2,0]),q2.animate.move_to([xs[2],-.2,0]),q3.animate.move_to([xs[1],-.2,0]),run_time=2,rate_func=m.linear)
            self.label('Different links can work at the same time',0,-1.65)
            self.label('Each packet still crosses every stage',0,-2.65,MUTED,24)
        elif index==8:
            for row,name in enumerate(('link 1','link 2','link 3')):self.label(name,-6.0,1.7-row*.9,MUTED,22,1.2)
            for slot in range(3):
                for row in range(slot+1):self.slot(row,slot,str(slot-row+1),(BLUE,GREEN,YELLOW)[slot-row])
            self.label('1 active link → 2 → 3',0,-1.6,YELLOW,31)
            self.label('Pipeline fill',0,-2.6)
        elif index==9:
            cols=(BLUE,GREEN,YELLOW,PURPLE)
            for col in range(6):
                for row in range(3):
                    packet_index=col-row
                    if 0<=packet_index<4:self.slot(row,col,str(packet_index+1),cols[packet_index])
            for j in range(6):self.show(text(str(j+1),-4.25+j*1.7,-1.0,23,MUTED,1),.15)
            self.label('6 transmission slots × 1.2 ms = 7.2 ms',0,-1.65,YELLOW,29)
            self.label('Same rates; useful overlap',0,-2.65,GREEN,26)
        elif index==10:
            self.label('First packet: H slots',0,1.7,BLUE,30)
            for i in range(3):self.show(self.box(str(i+1),-3+i*1.25,.65,BLUE,1),.4)
            self.label('Remaining packets: N − 1 slots',0,-.4,GREEN,30)
            for i in range(3):self.show(self.box('+1',1+i*1.25,.65,GREEN,1),.4)
            self.label('Total time = (N + H − 1) × L/R',0,-1.65,YELLOW,30)
            self.label('Equal links; no travel, processing, or competing traffic',0,-2.7,MUTED,22)
        elif index==11:
            self.show(line((-5.6,.2),(5.6,.2)))
            self.label('Sources send uneven bursts',0,1.8)
            arrivals=[('B1',BLUE),('B2',BLUE),('G1',GREEN),('B3',BLUE),('G2',GREEN)]
            for i,(value,col) in enumerate(arrivals):
                q=self.show(self.box(value,-5,.2,col,1),.3);self.fly(q,4.8,seconds=1.1);self.vanish(q)
                self.show(self.box(value,-4+i*2,-1.15,col,1),.2)
            self.label('Use available capacity when data is ready',0,-2.5,YELLOW,26)
        elif index==12:
            self.show(line((-5.8,.5),(5.8,.5)))
            for i in range(6):self.show(self.box(str(i+1),3-i*1,.5,BLUE,.75),.3)
            g=self.show(self.box('G',-4.5,.5,GREEN,1));self.fly(g,-3.2,seconds=2)
            self.show(m.Line([3.8,-.1,0],[3.8,1.15,0],color=YELLOW,stroke_width=4))
            self.label('Ready packets can still have to wait',0,-1.1)
            self.label('Packet boundaries do not create unlimited capacity',0,-2.35,MUTED,24)
        elif index==13:
            self.label('More pieces → more handling information',0,2,WHITE,28)
            for row,count in enumerate((3,6)):
                width=9/count
                for j in range(count):
                    x=-4.5+(j+.5)*width;y=.7-row*1.8
                    payload=self.own(m.Rectangle(width=width-.35,height=.6,color=BLUE,fill_color=BLUE,fill_opacity=.45).move_to([x+.12,y,0]))
                    head=self.own(m.Rectangle(width=.24,height=.6,color=YELLOW,fill_color=YELLOW,fill_opacity=.75).move_to([x-width/2+.12,y,0]))
                    self.play(m.FadeIn(payload),m.FadeIn(head),run_time=.4)
            self.label('Blue: useful content    Yellow: per-packet overhead',0,-2.7,YELLOW,25)
        elif index==14:
            self.path(1.3)
            for i,(value,col) in enumerate((('B1',BLUE),('G',GREEN),('B2',BLUE),('B3',BLUE))):
                q=self.show(self.box(value,-5,.1,col,1));self.fly(q,5,.1,1.3)
                self.fly(q,-1.8+i*1.25,-1.25,1.1)
            self.label('Shared journey; distinguishable pieces',0,-2.6)
        elif index==15:
            self.path(1.2)
            q1=self.show(self.box('B1',-5,-.15,BLUE,1));self.fly(q1,-1.7,seconds=1.2)
            q2=self.show(self.box('G',-5,-.15,GREEN,1))
            self.play(q1.animate.move_to([1.7,-.15,0]),q2.animate.move_to([-1.7,-.15,0]),run_time=1.5,rate_func=m.linear)
            self.label('Shorter turns + overlapping stages',0,-1.3,YELLOW,30)
            self.label('Many conversations, shared physical links',0,-2.55,GREEN,27)
        self.finish(budget)
