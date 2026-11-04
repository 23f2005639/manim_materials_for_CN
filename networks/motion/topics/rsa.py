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
            public=self.show(m.VGroup(m.Rectangle(width=2.5,height=1.2,color=BLUE).move_to([-3,0,0]),text('public',-3,0,31,BLUE)),.8)
            private=self.show(m.VGroup(m.Rectangle(width=2.5,height=1.2,color=GREEN).move_to([3,0,0]),text('private',3,0,31,GREEN)),.8)
            q=self.show(packet('message',YELLOW,2).move_to([-5,-1.5,0]),.5)
            self.play(q.animate.move_to([-3,-1.5,0]),run_time=1.5)
            self.play(m.Transform(q,packet('ciphertext',YELLOW,2.3).move_to([-3,-1.5,0])),run_time=1)
            self.play(q.animate.move_to([3,-1.5,0]),run_time=2)
            self.play(m.Transform(q,packet('message',GREEN,2).move_to([3,-1.5,0])),run_time=1)
            self.equation('one operation is public; its intended inverse is private',-2.65)
        elif i==1:
            self.pair('5 × 11','55','easy to multiply',BLUE)
            self.equation('55 → which prime factors?',-1.2,YELLOW)
            self.equation('small toy numbers reveal the mechanism',-2.4,MUTED)
        elif i==2:
            marker=self.clock()
            value=self.show(text('0',0,-.1,40,YELLOW,2),.5)
            for number in (1,10,54,55,56,111):
                self.residue(marker,number,duration=.9)
                self.play(m.Transform(value,text(str(number%55),0,-.1,40,YELLOW,2)),run_time=.3)
            self.equation('56 mod 55 = 1     ·     111 mod 55 = 1',-2.65)
        elif i==3:
            dots=self.show(m.VGroup(*(m.Dot([-3+j*.6,1.2-k*.6,0],radius=.1,color=BLUE) for k in range(5) for j in range(11))),1.5)
            self.equation('p = 5       q = 11',2.25,BLUE)
            self.equation('n = 5 × 11 = 55',-2.15,GREEN)
        elif i==4:
            cells=[]
            for value in range(55):
                row,col=divmod(value,11);x=-3.75+col*.75;y=1.2-row*.6
                c=BLUE
                cells.append(m.VGroup(m.Rectangle(width=.62,height=.48,color=c).move_to([x,y,0]),text(str(value),x,y,19,c,.56)))
            self.show(m.VGroup(*cells),1.2)
            for divisor in (5,11):
                self.play(*(cells[v].animate.set_color(RED) for v in range(55) if v%divisor==0),run_time=1.5)
            self.equation('φ(55) = (5 − 1)(11 − 1) = 40',-2.3,GREEN)
            self.equation('40 positions relatively prime to 55',2.25,WHITE)
        elif i==5:
            self.show(packet('n = 55',BLUE,3).move_to([-2,1,0]),.8)
            self.show(packet('e = 3',BLUE,3).move_to([2,1,0]),.8)
            self.equation('public key: (55, 3)',-.3,BLUE)
            self.equation('gcd(3, 40) = 1',-1.4,GREEN)
            self.equation('a matching modular inverse exists',-2.45,MUTED)
        elif i==6:
            label=self.equation('3 × d ≡ 1  (mod 40)',2.1)
            bars=[]
            for j,(length,color) in enumerate(((4,BLUE),(4,BLUE),(.1,GREEN))):
                x=(-2.1,2.0,4.15)[j]
                bars.append(self.show(m.Rectangle(width=length,height=.8,color=color,fill_color=color,fill_opacity=.2).move_to([x,0,0]),.6))
            self.equation('81 = 40 + 40 + 1',-1.25,YELLOW)
            self.equation('d = 27       3 × 27 = 81',-2.4,GREEN)
        elif i==7:
            self.show(packet('m = 7',BLUE,2.8).move_to([-4,1,0]),.6)
            self.show(m.Arrow([-2.4,1,0],[2.4,1,0],color=YELLOW,buff=.1),.8)
            self.show(packet('c = 13',YELLOW,2.8).move_to([4,1,0]),.6)
            self.equation('7³ = 343',-.35)
            self.equation('343 = 6 × 55 + 13',-1.35)
            self.equation('c = 7³ mod 55 = 13',-2.4,YELLOW)
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
            self.equation('(7³)²⁷ = 7⁸¹ ≡ 7  (mod 55)',-2.3,GREEN)
        elif i==11:
            self.show(packet('ciphertext 13',YELLOW,3).move_to([0,1.6,0]),.7)
            for x,exponent,value,color in ((-3.2,5,pow(13,5,55),RED),(3.2,27,7,GREEN)):
                self.show(m.Arrow([0,1.1,0],[x,.1,0],color=color,buff=.1),.8)
                self.show(packet(str(value),color,2).move_to([x,-.55,0]),.6)
                self.show(text(f'd = {exponent}',x,-1.6,30,color),.6)
            self.equation('the inverse is chosen, not guessed',-2.65)
        elif i==12:
            values=(('55',0,1.8,BLUE),('5 × 11',-3.2,.2,RED),('φ = 40',0,-.7,YELLOW),('d = 27',3.2,-1.6,GREEN))
            for label,x,y,c in values:self.show(packet(label,c,2.6).move_to([x,y,0]),.7)
            for a,b in (((0,1.3),(-3.2,.7)),((-1.8,.2),(-.8,-.2)),((1.3,-.7),(2.3,-1.25))):self.show(m.Arrow([*a,0],[*b,0],color=MUTED,buff=.05),.6)
            self.equation('factoring exposes the private construction',-2.65)
        elif i==13:
            for y in (1,-.65):
                self.show(packet('7',BLUE,1.8).move_to([-4,y,0]),.5)
                self.show(m.Arrow([-2.8,y,0],[2.8,y,0],color=MUTED,buff=.1),.6)
                self.show(packet('13',YELLOW,1.8).move_to([4,y,0]),.5)
            self.equation('bare textbook RSA repeats the same mapping',-1.8,YELLOW)
            self.equation('real encryption needs a complete encoding scheme',-2.65,MUTED)
        elif i==14:
            modulus=self.show(packet('public modulus',BLUE,3.7).move_to([-3.8,.5,0]),.8)
            secret=self.show(packet('private structure',GREEN,3.7).move_to([3.8,.5,0]),.8)
            arrow=self.show(m.Arrow([-1.7,.5,0],[1.7,.5,0],color=YELLOW,buff=.1),1)
            self.show(text('computational assumptions',0,1.65,30,YELLOW),.7)
            self.equation('future capabilities can change those assumptions',-1.3)
            self.equation('motivation for post-quantum migration',-2.4,MUTED)
        elif i==15:
            for x,label,color in ((-4.4,'7',BLUE),(0,'13',YELLOW),(4.4,'7',GREEN)):
                self.show(packet(label,color,2).move_to([x,.6,0]),.6)
            self.show(m.Arrow([-3,.6,0],[-1.4,.6,0],color=BLUE,buff=.05),.8)
            self.show(m.Arrow([1.4,.6,0],[3,.6,0],color=GREEN,buff=.05),.8)
            self.show(text('e = 3',-2.2,1.65,30,BLUE),.6)
            self.show(text('d = 27',2.2,1.65,30,GREEN),.6)
            self.equation('public operation → ciphertext → private inverse',-1.1)
            self.equation('toy modulus 55 · mathematical demonstration only',-2.4,MUTED)
        self.finish(budget)
