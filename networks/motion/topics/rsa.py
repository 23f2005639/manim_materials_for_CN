"""A small RSA construction connects public operations to modular arithmetic."""
from .common import *


class Director(VisualDirector):
    def show(self,obj,t=.7):
        self.own(obj);self.play(m.FadeIn(obj),run_time=t);return obj

    def equation(self,value,y=-2,color=WHITE):
        return self.show(text(value,0,y,31,color,12),.8)

    def clock(self,modulus=55,radius=1.7,center=(0,-.1)):
        x,y=center
        self.show(m.Circle(radius=radius,color=MUTED).move_to([x,y,0]),.7)
        for j in range(0,modulus,5):
            a=math.pi/2-2*math.pi*j/modulus
            self.show(text(str(j),x+(radius+.40)*math.cos(a),y+(radius+.40)*math.sin(a),17,MUTED,.6),.05)
        marker=self.show(m.Dot([x,y+radius,0],radius=.11,color=YELLOW),.4)
        return marker

    def residue(self,marker,value,center=(0,-.1),radius=1.7,duration=1):
        a=math.pi/2-2*math.pi*(value%55)/55
        self.play(marker.animate.move_to([center[0]+radius*math.cos(a),center[1]+radius*math.sin(a),0]),run_time=duration)

    def pair(self,a,b,label,color=BLUE):
        self.show(packet(str(a),color,2).move_to([-3,.4,0]),.6)
        self.show(packet(str(b),color,2).move_to([3,.4,0]),.6)
        self.show(m.Arrow([-1.7,.4,0],[1.7,.4,0],color=color,buff=.1),.8)
        self.show(text(label,0,1.4,29,color),.7)

    def animate(self,i,section,budget):
        self.reset()
        if i==0:
            self.show(host('You',-4.7,.5,BLUE),.7)
            self.show(host('Friend',4.7,.5,GREEN),.7)
            self.show(line((-4.2,.5),(4.2,.5)),.7)
            note=self.show(packet('meet at seven',BLUE,3.1,.7).move_to([-2.8,.5,0]),.7)
            self.play(note.animate.move_to([0,.5,0]),run_time=2)
            self.show(host('Someone else',-3,-1.8,RED),.7)
            self.show(m.Arrow([-2.5,-1.8,0],[-.4,-.1,0],color=RED,buff=.05),.7)
            warning=self.equation('readable here, too',2,RED)
            self.play(m.Transform(note,packet('? ? ?',YELLOW,3.1,.7).move_to([0,.5,0])),m.FadeOut(warning),run_time=1.2)
            self.play(note.animate.move_to([2.8,.5,0]),run_time=2)
            self.equation('change it before sending',-2.7,YELLOW)
        elif i==1:
            body=self.show(m.Rectangle(width=1.5,height=1.05,color=BLUE,fill_color=BG,fill_opacity=1).move_to([-2.8,.1,0]),.7)
            shackle=self.show(m.Arc(radius=.55,start_angle=0,angle=math.pi,color=BLUE).move_to([-2.55,.95,0]),.7)
            self.show(text('anyone can close',-2.8,2,27,BLUE,4.5),.6)
            self.play(shackle.animate.shift([-.25,-.3,0]),run_time=1.1)
            key=self.show(m.VGroup(m.Circle(radius=.25,color=GREEN).move_to([2.4,.5,0]),line((2.65,.5),(3.6,.5),GREEN,4),line((3.4,.5),(3.4,.2),GREEN,4)),.7)
            self.show(text('friend keeps opening key',2.8,2,27,GREEN,5.4),.6)
            self.show(text('public rule',-2.8,-1.05,28,BLUE,4),.6)
            self.show(text('private rule',2.8,-1.05,28,GREEN,4),.6)
            self.equation('our tiny message will be the number 7',-2.5)
        elif i==2:
            dots=[self.show(m.Dot([-4.5+j*.9,.75,0],radius=.13,color=BLUE),.12) for j in range(11)]
            for group in range(2):
                start=-4.5+group*4.5
                self.show(m.RoundedRectangle(width=4.2,height=.75,corner_radius=.15,color=MUTED).move_to([start+1.8,.75,0]),.8)
                self.show(text('5',start+1.8,-.1,29,MUTED),.5)
            self.play(dots[-1].animate.set_color(YELLOW).scale(1.4),run_time=.8)
            self.show(text('1 left',4.5,-.1,29,YELLOW,2),.6)
            self.equation('11 = 2 × 5 + 1',-1.35)
            self.equation('11 mod 5 = 1',-2.4,YELLOW)
        elif i==3:
            for y,count,color in ((1.4,5,BLUE),(.35,11,GREEN)):
                self.show(text(str(count),-5.1,y,31,color,1),.5)
                self.show(m.VGroup(*(m.Dot([-3.5+j*.6,y,0],radius=.11,color=color) for j in range(count))),.9)
            self.show(text('only divisible by 1 and itself',0,2.35,26,WHITE),.7)
            self.equation('5 × 11 = 55',-.9,YELLOW)
            self.equation('n = 55',-1.85,GREEN)
            self.show(text('n names the number used for remainders',0,-2.65,23,MUTED),.7)
        elif i==4:
            cells=[]
            for value in range(55):
                row,col=divmod(value,11);x=-3.75+col*.75;y=1.2-row*.6
                c=BLUE
                cells.append(m.VGroup(m.Rectangle(width=.62,height=.48,color=c).move_to([x,y,0]),text(str(value),x,y,19,c,.56)))
            self.show(m.VGroup(*cells),1.2)
            for divisor in (5,11):
                self.play(*(cells[v].animate.set_color(RED) for v in range(55) if v%divisor==0),run_time=1.5)
            self.equation('(5 − 1) × (11 − 1) = 40',-2.3,GREEN)
            self.equation('40 positions left',2.25,WHITE)
        elif i==5:
            self.show(packet('55',BLUE,2).move_to([-2,1.5,0]),.8)
            self.show(packet('3',BLUE,2).move_to([2,1.5,0]),.8)
            self.equation('message × message × message',.25,WHITE)
            self.equation('then keep the remainder after dividing by 55',-.8,YELLOW)
            self.equation('public key: (55, 3)',-1.8,BLUE)
            self.show(text('power e = 3',0,-2.65,25,MUTED),.7)
        elif i==6:
            label=self.equation('find a matching power',2.1)
            bars=[]
            for j,(length,color) in enumerate(((4,BLUE),(4,BLUE),(.1,GREEN))):
                x=(-2.1,2.0,4.15)[j]
                bars.append(self.show(m.Rectangle(width=length,height=.8,color=color,fill_color=color,fill_opacity=.2).move_to([x,0,0]),.6))
            self.equation('81 = 40 + 40 + 1',-1.25,YELLOW)
            self.equation('private power: d = 27',-2.4,GREEN)
        elif i==7:
            self.show(packet('message: 7',BLUE,2.8).move_to([-4,1,0]),.6)
            self.show(m.Arrow([-2.4,1,0],[2.4,1,0],color=YELLOW,buff=.1),.8)
            self.show(packet('encrypted: 13',YELLOW,2.8).move_to([4,1,0]),.6)
            self.equation('7³ = 343',-.35)
            self.equation('343 = 6 × 55 + 13',-1.35)
            self.equation('7³ mod 55 = 13',-2.4,YELLOW)
        elif i==8:
            values=(13,4,16,36)
            for j,value in enumerate(values):
                x=-4.5+j*3
                self.show(packet(str(value),BLUE,1.8).move_to([x,.5,0]),.5)
                self.show(text(('13','13²','13⁴','13⁸')[j],x,1.55,28,BLUE,2),.4)
                if j:self.show(m.Arrow([x-2,.5,0],[x-1,.5,0],color=MUTED,buff=.05),.4)
            self.equation('square → keep the remainder → square again',-1.3)
            self.equation('modulo 55 at every step',-2.4,YELLOW)
        elif i==9:
            powers=(16,8,2,1);values=(31,36,4,13)
            for j,(power,value) in enumerate(zip(powers,values)):
                x=-4.5+j*3
                self.show(packet(str(value),BLUE,1.8).move_to([x,.6,0]),.5)
                self.show(text(f'13^{power} mod 55',x,1.65,23,BLUE,2.7),.4)
            result=self.show(text('1',0,-1.0,37,YELLOW),.5);running=1
            for value in values:
                running=running*value%55
                self.play(m.Transform(result,text(str(running),0,-1,37,YELLOW)),run_time=.9)
            self.equation('13²⁷ mod 55 = 7',-2.4,GREEN)
        elif i==10:
            marker=self.clock(40,1.45,(0,0))
            self.equation('3 × 27 = 81 = 1 + 2 × 40',2.25,YELLOW)
            self.play(m.Rotate(marker,angle=-2*m.TAU,about_point=[0,0,0]),run_time=4)
            self.show(text('7',0,0,42,GREEN,2),.6)
            self.equation('(7³)²⁷ mod 55 = 7',-2.3,GREEN)
        elif i==11:
            self.show(packet('ciphertext 13',YELLOW,3).move_to([0,1.6,0]),.7)
            for x,exponent,value,color in ((-3.2,5,pow(13,5,55),RED),(3.2,27,7,GREEN)):
                self.show(m.Arrow([0,1.1,0],[x,.1,0],color=color,buff=.1),.8)
                self.show(packet(str(value),color,2).move_to([x,-.55,0]),.6)
                self.show(text(f'd = {exponent}',x,-1.6,30,color),.6)
            self.equation('the private rule must fit the public rule',-2.65)
        elif i==12:
            values=(('55',0,1.8,BLUE),('5 × 11',-3.2,.2,RED),('count: 40',0,-.7,YELLOW),('d = 27',3.2,-1.6,GREEN))
            for label,x,y,c in values:self.show(packet(label,c,2.6).move_to([x,y,0]),.7)
            for a,b in (((0,1.3),(-3.2,.7)),((-1.8,.2),(-.8,-.2)),((1.3,-.7),(2.3,-1.25))):self.show(m.Arrow([*a,0],[*b,0],color=MUTED,buff=.05),.6)
            self.equation('the factors let us build the private rule',-2.65)
        elif i==13:
            for y in (1,-.65):
                self.show(packet('7',BLUE,1.8).move_to([-4,y,0]),.5)
                self.show(m.Arrow([-2.8,y,0],[2.8,y,0],color=MUTED,buff=.1),.6)
                self.show(packet('13',YELLOW,1.8).move_to([4,y,0]),.5)
            self.equation('bare textbook RSA repeats the same mapping',-1.8,YELLOW)
            self.equation('real encryption needs a complete encoding scheme',-2.65,MUTED)
        elif i==14:
            self.show(text('shared secret',-3.2,2,30,YELLOW,5),.7)
            self.show(text('public + private',3.2,2,30,BLUE,5),.7)
            self.show(line((0,-1.8),(0,2),MUTED),.7)
            for x,label,color in ((-4.4,'secret',YELLOW),(-2,'secret',YELLOW),(2,'public',BLUE),(4.4,'private',GREEN)):
                self.show(packet(label,color,1.95,.8).move_to([x,.4,0]),.6)
            self.show(text('known to both',-3.2,-.85,26,YELLOW,5),.6)
            self.show(text('publish one; keep one',3.2,-.85,26,BLUE,5),.6)
            self.equation('the private rule must be hard to recover',-2.4)
        elif i==15:
            for x,label,color in ((-4.4,'7',BLUE),(0,'13',YELLOW),(4.4,'7',GREEN)):
                self.show(packet(label,color,2).move_to([x,.6,0]),.6)
            self.show(m.Arrow([-3,.6,0],[-1.4,.6,0],color=BLUE,buff=.05),.8)
            self.show(m.Arrow([1.4,.6,0],[3,.6,0],color=GREEN,buff=.05),.8)
            self.show(text('e = 3',-2.2,1.65,30,BLUE),.6)
            self.show(text('d = 27',2.2,1.65,30,GREEN),.6)
            self.equation('public rule → encrypted message → private rule',-1.1)
            self.equation('toy modulus 55 · mathematical demonstration only',-2.4,MUTED)
        self.finish(budget)
