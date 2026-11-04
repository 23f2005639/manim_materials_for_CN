"""One optical sharing rule, developed through independent channels and wavelengths."""
from .common import *
from .foundation import fiber_intro

COLORS=(BLUE,GREEN,YELLOW,PURPLE)
YS=(1.8,.6,-.6,-1.8)


class Director(VisualDirector):
    def show(self,obj,t=1):
        self.own(obj);self.play(m.FadeIn(obj),run_time=t);return obj

    def wave(self,a,b,y,k,color):
        xs=np.linspace(a,b,140)
        return m.VMobject(color=color,stroke_width=2.5).set_points_as_corners([[x,y+.16*math.sin(k*(x-a)),0] for x in xs])

    def lanes(self,labels=True):
        for j,(y,c) in enumerate(zip(YS,COLORS)):
            self.show(line((-4.3,y),(4.8,y),c),.25)
            if labels:self.show(text(f'channel {j+1}',-5.35,y,21,c,1.5),.3)

    def pulse(self,x1,x2,y,c,value='101',duration=2):
        q=self.own(packet(value,c,1.05).move_to([x1,y,0]))
        self.s.add(q)
        self.play(q.animate.move_to([x2,y,0]),run_time=duration)
        self.s.remove(*q.get_family())
        self.wait(.25)

    def mux(self,reverse=False):
        left,right=(-2.0,2.0)
        for x,label in ((left,'IN'),(right,'OUT')):
            self.show(m.VGroup(m.Rectangle(width=1,height=2.8,color=WHITE).move_to([x,0,0]),text(label,x,0,20,WHITE,.85)),.5)
        self.show(text('combine',left,2.3,25,WHITE,3),.5)
        self.show(text('separate',right,2.3,25,WHITE,3),.5)
        self.show(m.RoundedRectangle(width=3,height=.7,corner_radius=.2,color=MUTED).move_to([0,0,0]),.5)
        for y,c in zip(YS,COLORS):
            self.show(line((-5.5,y),(left-.5,y*.6),c),.2)
            self.show(line((right+.5,y*.6),(5.5,y),c),.2)
        self.show(text('one fiber',0,-.85,25,MUTED,2.5),.4)
        for j,(y,c) in enumerate(zip(YS,COLORS)):
            q=self.show(m.Dot([-5.3,y,0],radius=.10,color=c),.15)
            self.play(q.animate.move_to([-1.5,y*.12,0]),run_time=1)
            self.play(q.animate.move_to([1.5,y*.12,0]),run_time=1.4)
            self.play(q.animate.move_to([5.3,y,0]),run_time=1)

    def animate(self,i,section,budget):
        self.reset()
        if i==0:
            fiber_intro(self)
        elif i==1:
            bulb=self.show(m.Circle(radius=.4,color=BLUE,fill_color=BLUE,fill_opacity=.1).move_to([-4.8,.5,0]),.7)
            self.show(text('light',-4.8,1.4,26,BLUE,2),.5)
            receiver=self.show(host('Reader',4.8,.5,GREEN),.5)
            self.show(line((-4.3,.5),(4.3,.5),MUTED),.7)
            for j,bit in enumerate('1011'):
                self.play(bulb.animate.set_fill(BLUE,opacity=.95 if bit=='1' else .08),run_time=.65)
                q=self.show(m.Dot([-4.3,.5,0],radius=.12,color=BLUE,fill_opacity=1 if bit=='1' else .12),.2)
                self.play(q.animate.move_to([4.3,.5,0]),run_time=.9)
                self.play(m.FadeOut(q),run_time=.2)
                self.show(packet(bit,BLUE,.75).move_to([-1.65+j*1.1,-.8,0]),.35)
            self.show(text('1 = bright     0 = dark',0,-1.75,29),.7)
            self.show(text('one choice = one bit',0,-2.55,26,YELLOW),.7)
        elif i==2:
            w=self.show(self.wave(-5.5,5.5,0,3,BLUE),1)
            marker=self.show(m.DoubleArrow([-5.5,-.65,0],[-5.5+2*math.pi/3,-.65,0],color=YELLOW,buff=0),.5)
            self.show(text('wavelength = crest spacing',0,1.3,30),.6)
            for k,c in ((5,GREEN),(7,YELLOW),(3,BLUE)):
                self.play(m.Transform(w,self.wave(-5.5,5.5,0,k,c)),m.Transform(marker,m.DoubleArrow([-5.5,-.65,0],[-5.5+2*math.pi/k,-.65,0],color=YELLOW,buff=0)),run_time=2)
            self.show(text('display colors represent optical wavelengths',0,-1.8,25,MUTED),.7)
        elif i==3:
            for j,(y,c) in enumerate(zip(YS,COLORS)):
                self.show(host(f'Sender {j+1}',-5,y,c),.4)
                self.show(line((-4.5,y),(4.8,y),c),.4)
                self.pulse(-3.8,4.2,y,c,('101','011','110','001')[j],1.4)
            self.show(text('4 separate channels',0,2.65,28,WHITE),.8)
        elif i==4:
            self.show(line((-5,-1.5),(5,-1.5)),.5)
            a=self.show(m.Rectangle(width=2,height=1.2,color=BLUE,fill_color=BLUE,fill_opacity=.2).move_to([-2,0,0]),.6)
            b=self.show(m.Rectangle(width=2,height=1.2,color=GREEN,fill_color=GREEN,fill_opacity=.2).move_to([2,0,0]),.6)
            self.play(a.animate.move_to([0,0,0]),b.animate.move_to([0,0,0]),run_time=2)
            self.show(text('same wavelength region',0,1.5,29,RED),.5)
            self.show(text('wavelength selection cannot distinguish them',0,-2.15,26,RED),.7)
        elif i in (5,12):
            self.show(line((-6,-1),(6,-1)),.6)
            self.show(text('range of wavelengths',0,-1.7,25,MUTED),.5)
            for j,c in enumerate(COLORS):
                x=-4.5+j*3
                self.show(m.Rectangle(width=1.7,height=1.5,color=c,fill_color=c,fill_opacity=.16).move_to([x,.3,0]),.6)
                self.show(text(f'{j+1}',x,1.4,32,c,1.4),.4)
            if i==5:self.show(text('different wavelengths → separate channels',0,2,27),.6)
            else:
                bars=[]
                for j in range(9):bars.append(self.show(m.Rectangle(width=.4,height=.7,color=RED).move_to([-5.6+j*1.4,.3,0]),.2))
                self.show(text('extra channels need usable spectrum',0,2,27,RED),.7)
        elif i in (6,8,15):
            self.mux(i==8)
            if i==15:self.show(text('4 channels · 1 fiber · 4 recovered streams',0,-2.65,25,BLUE),.7)
        elif i==7:
            self.show(m.RoundedRectangle(width=11,height=.9,corner_radius=.3,color=MUTED),.7)
            dots=[]
            for j,c in enumerate(COLORS):
                y=(j-1.5)*.19
                self.show(self.wave(-5,5,y,4+j,c),.4)
                dots.append(self.show(m.Dot([-4.8,y,0],radius=.12,color=c),.25))
            self.play(*(d.animate.shift(9.6*m.RIGHT) for d in dots),run_time=4)
            self.show(text('simultaneous, distinguishable channels',0,-1.65,29),.7)
        elif i==9:
            self.lanes(False)
            for j,(y,c) in enumerate(zip(YS,COLORS)):
                box=self.show(m.Rectangle(width=1.5,height=.65,color=c).move_to([4.7,y,0]),.3)
                if j!=1:self.play(box.animate.set_opacity(.15),run_time=.4)
            self.show(text('select channel 2',0,2.6,27,GREEN),.6)
            for _ in range(3):self.pulse(-4,4.2,.6,GREEN,'011',1.5)
        elif i in (10,13):
            rates=[100,100,100,100] if i==10 else [100,100,50,50]
            for j,(rate,c) in enumerate(zip(rates,COLORS)):
                x=-4.5+j*3
                self.show(m.VGroup(m.Rectangle(width=2,height=1.1,color=c).move_to([x,.7,0]),text(str(rate),x,.7,33,c,1.8)),.7)
                self.show(text('Gb/s',x,-.2,24,c,1.8),.3)
            total=self.show(text('0 Gb/s',0,-1.65,34),.5)
            for j in range(4):self.play(m.Transform(total,text(f'{sum(rates[:j+1])} Gb/s',0,-1.65,34,WHITE)),run_time=1)
            self.show(text('combined raw rate',0,-2.5,25,MUTED),.5)
        elif i==11:
            cells=self.show(m.VGroup(*(packet(str(j+1),BLUE,.65).move_to([-2.8+j*.8,.85,0]) for j in range(8))),1)
            brace=self.show(m.Brace(cells,m.DOWN,color=YELLOW),.7)
            self.show(text('8 bits = 1 byte',0,-.45,30,YELLOW),.6)
            self.show(text('400 Gb/s ÷ 8 = 50 GB/s',0,-1.65,34),1)
            self.show(text('raw rate; application throughput can be lower',0,-2.55,24,MUTED),.7)
        elif i==14:
            self.show(m.RoundedRectangle(width=11,height=.9,corner_radius=.3,color=MUTED),.7)
            channels=[]
            for j,c in enumerate(COLORS):
                channels.append(self.show(self.wave(-5,5,(j-1.5)*.19,4+j,c),.5))
            rate=self.show(text('400 Gb/s',0,-1.65,34,WHITE),.7)
            self.play(channels[1].animate.set_opacity(.08),run_time=1.4)
            self.show(text('green goes quiet',0,1.65,28,GREEN),.7)
            dots=[self.show(m.Dot([-4.8,(j-1.5)*.19,0],radius=.12,color=c),.2) for j,c in enumerate(COLORS) if j!=1]
            self.play(*(d.animate.shift(9.6*m.RIGHT) for d in dots),run_time=3)
            self.play(m.Transform(rate,text('300 Gb/s',0,-1.65,34,WHITE)),run_time=1.2)
            self.show(text('3 channels keep carrying their messages',0,-2.6,25,MUTED),.7)
        self.finish(budget)
