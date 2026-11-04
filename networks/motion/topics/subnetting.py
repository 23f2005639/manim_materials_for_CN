"""Subnet boundaries emerge directly from fixed and free binary positions."""
from .common import *
from .foundation import computer


class Director(VisualDirector):
    def show(self,obj,t=.7):
        self.own(obj);self.play(m.FadeIn(obj),run_time=t);return obj

    def bits(self,value,y=0,mask=None):
        chars=value if isinstance(value,str) else f'{value:08b}'
        n=len(chars);pitch=min(.84,11.5/n);left=-(n-1)*pitch/2
        cells=[]
        for j,c in enumerate(chars):
            col=BLUE if mask is None or j<mask else YELLOW
            cell=m.VGroup(m.Rectangle(width=pitch*.86,height=.66,color=col,fill_color=BG,fill_opacity=1).move_to([left+j*pitch,y,0]),text(c,left+j*pitch,y,25 if n<16 else 18,col,pitch*.8))
            cells.append(cell)
        group=self.show(m.VGroup(*cells),1)
        return group

    def blocks(self,count,labels=True):
        width=11/count
        groups=[]
        for j in range(count):
            x=-5.5+width*(j+.5);c=(BLUE,GREEN,YELLOW,PURPLE)[j%4]
            box=self.show(m.Rectangle(width=width-.08,height=1.5,color=c,fill_color=c,fill_opacity=.12).move_to([x,0,0]),.6)
            if labels:self.show(text(f'{j*256//count}–{(j+1)*256//count-1}',x,0,29,c,width-.15),.5)
            groups.append(box)
        return groups

    def animate(self,i,section,budget):
        self.reset()
        if i==0:
            for x,label in ((-4.5,'192.168.1.10'),(0,'192.168.1.20'),(4.5,'192.168.1.30')):
                self.show(computer(label,x,.7),.8)
            self.show(line((-4.5,-.7),(4.5,-.7)),1)
            q=self.show(packet('to .20',GREEN,1.4).move_to([-4.5,-.7,0]),.5)
            self.play(q.animate.move_to([0,-.7,0]),run_time=2)
            self.show(text('An address identifies where a message goes',0,-1.9,29),.7)
            self.show(text('Subnetting: divide an address group',0,-2.8,26,YELLOW),.7)
        elif i==1:
            bit=self.show(packet('0',BLUE,1,.8).move_to([0,.6,0]),.7)
            self.show(text('One bit: two possible choices',0,1.9,30),.7)
            for value in ('1','0','1'):
                self.play(m.Transform(bit,packet(value,BLUE,1,.8).move_to([0,.6,0])),run_time=.8)
            self.play(m.FadeOut(bit),run_time=.4)
            self.bits('00010100',.6)
            self.show(text('8 bits can represent the number 20',0,-.7,28,GREEN),.7)
            self.show(text('4 address numbers × 8 bits = 32 bits',0,-2,29),.7)
        elif i==2:
            examples=self.show(m.VGroup(*[text('192.168.1.'+n,0,1.8-j*.75,28,BLUE) for j,n in enumerate(('10','20','30'))]),1)
            self.play(m.Indicate(examples),run_time=1.3)
            self.play(m.FadeOut(examples),run_time=.6)
            self.bits('11000000101010000000000100000000',.3,24)
            self.show(text('192       .       168       .        1        .        0',0,1.45,26),.7)
            self.show(text('24 fixed',-2.1,-1.1,29,BLUE),.7)
            self.show(text('8 free',4.3,-1.1,29,YELLOW,2.5),.7)
            self.show(text('192.168.1.0/24 → keep the first 24 bits',0,-2.3,28),.7)
            x=-(31)*11.5/32/2+23.5*11.5/32
            self.play(m.Create(self.own(line((x,-.3),(x,1),RED,4))),run_time=1)
        elif i==3:
            self.show(text('1 free bit',-4,2,27,WHITE,3),.5)
            self.show(text('2 free bits',1.4,2,27,WHITE,3),.5)
            for j,parent in enumerate(('0','1')):
                y=1-j*1.6
                self.show(packet(parent,BLUE,1).move_to([-4,y,0]),.5)
                for k,child in enumerate(('0','1')):
                    yy=y+.42-k*.84
                    self.show(line((-3.4,y),(-.2,yy)),.35)
                    self.show(packet(parent+child,GREEN,1.1).move_to([.5,yy,0]),.4)
            self.show(text('2 choices → 4 choices',0,-1.8,30,YELLOW),.6)
            self.show(text('8 free bits: 2⁸ = 256 choices (0–255)',0,-2.8,28),.7)
        elif i==4:
            self.blocks(2)
            self.show(text('/24 → /25',0,1.7,32),.7)
            self.show(text('0',-2.75,1,33,BLUE),.5);self.show(text('1',2.75,1,33,GREEN),.5)
            self.show(text('2¹ groups × 2⁷ addresses = 256',0,-1.8,31),.8)
        elif i==5:
            self.blocks(4)
            self.show(text('/24 + 2 prefix bits = /26',0,2.05,32),.7)
            for j,b in enumerate(('00','01','10','11')):self.show(text(b,-4.125+j*2.75,1.2,30,(BLUE,GREEN,YELLOW,PURPLE)[j],2.3),.5)
            self.show(text('2² = 4 subnets',0,-1.8,32),.7)
        elif i==6:
            self.bits('000000',.7)
            self.show(text('6 free host bits',0,1.8,30,YELLOW),.6)
            self.show(text('2⁶ = 64 addresses per subnet',0,-.8,32),.8)
            self.show(text('4 × 64 = 256',0,-2,34,GREEN),.8)
        elif i==7:
            self.blocks(4,False)
            for j,(bits,start) in enumerate(zip(('00','01','10','11'),(0,64,128,192))):
                x=-4.125+j*2.75;c=(BLUE,GREEN,YELLOW,PURPLE)[j]
                self.show(text(bits+'000000',x,1.45,23,c,2.5),.6)
                self.show(text(str(start),x,0,34,c,2.5),.6)
            self.show(text('network starts are 64 apart',0,-1.8,30),.7)
        elif i==8:
            self.bits('11000000',.65,2)
            for j,v in enumerate((128,64,32,16,8,4,2,1)):self.show(text(str(v),-2.94+j*.84,1.65,19,BLUE if j<2 else MUTED,.75),.2)
            self.show(text('128 + 64 = 192',0,-.8,33,YELLOW),.7)
            self.show(text('/26 mask: 255.255.255.192',0,-2,32),.8)
        elif i==9:
            self.bits(70,1.35);self.bits('11000000',.1,2)
            self.show(text('70',-4.5,1.35,28,WHITE,1.5),.5)
            self.show(text('AND',-4.5,.1,25,WHITE,1.5),.5)
            row=self.bits('00000000',-1.15)
            target=self.own(text('01000000',0,-1.15,28,GREEN,6.5))
            self.play(m.Transform(row,self.bits_target('01000000',-1.15,GREEN)),run_time=2)
            self.show(text('192.168.1.70 → 192.168.1.64/26',0,-2.4,29,GREEN),.8)
        elif i==10:
            cells=m.VGroup(*(m.Rectangle(width=.15,height=.7,color=GREEN,fill_color=GREEN,fill_opacity=.2).move_to([-5.2+j*.165,.3,0]) for j in range(64)))
            self.show(cells,1)
            self.play(cells[0].animate.set_color(RED),cells[63].animate.set_color(RED),run_time=1)
            self.show(text('network',-4.7,1.45,26,RED,2.3),.5);self.show(text('broadcast',4.65,1.45,26,RED,2.6),.5)
            self.show(text('64 total − 2 special = 62 hosts',0,-1.45,32),.8)
            self.show(text('ordinary LAN example',0,-2.4,24,MUTED),.6)
        elif i in (11,12):
            starts=(0,64) if i==11 else (128,192)
            for j,start in enumerate(starts):
                y=1-j*2.3;c=(BLUE,GREEN) if i==11 else (YELLOW,PURPLE);color=c[j]
                self.show(m.Rectangle(width=10.5,height=.75,color=color).move_to([0,y,0]),.7)
                self.show(text(f'{start}     |     hosts {start+1}–{start+62}     |     {start+63}',0,y,28,color,10),.7)
                self.show(text(f'192.168.1.{start}/26',0,y+.75,27,color),.5)
            self.show(text('network                        broadcast',0,-2.55,23,MUTED),.5)
        elif i==13:
            self.show(text('Need 50 host addresses',0,2.1,31),.7)
            for y,n,prefix,col in ((.7,5,27,RED),(-1.05,6,26,GREEN)):
                self.show(m.Rectangle(width=(2**n)/18,height=.6,color=col,fill_color=col,fill_opacity=.2).move_to([-3.9,y,0]),.7)
                self.show(text(f'/{prefix}: 2^{n} − 2 = {2**n-2}',2.25,y,29,col,5.6),.8)
            self.show(text('choose /26: 62 usable addresses',0,-2.35,30,GREEN),.7)
        elif i==14:
            for j,start in enumerate((64,128)):
                x=-2.8+j*5.6;c=(GREEN,PURPLE)[j]
                self.show(m.Rectangle(width=4.5,height=.9,color=c).move_to([x,-1.2,0]),.6)
                self.show(text(f'.{start}/26',x,-1.2,30,c,4),.6)
            for value,x,target,c in ((70,-4.5,-3.6,GREEN),(100,0,-2.0,GREEN),(130,4.5,2.8,PURPLE)):
                q=self.show(packet(str(value),c,1.2).move_to([x,1.2,0]),.5)
                self.play(q.animate.move_to([target,-.25,0]),run_time=1.6)
            self.show(text('compare the masked prefixes',0,-2.4,29),.7)
        elif i==15:
            self.blocks(4)
            self.show(text('two subnet bits · six host bits',0,1.7,31),.7)
            self.show(text('4 × 64 = 256',0,-1.5,36,GREEN),.8)
            self.show(text('one boundary explains every range',0,-2.45,28),.7)
        self.finish(budget)

    def bits_target(self,chars,y,color):
        return m.VGroup(*(m.VGroup(m.Rectangle(width=.72,height=.66,color=color).move_to([-2.94+j*.84,y,0]),text(c,-2.94+j*.84,y,25,color,.65)) for j,c in enumerate(chars)))
