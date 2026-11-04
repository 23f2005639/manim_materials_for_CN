"""One name lookup, its reusable answer, and the cost of freshness."""
from .common import *
from .foundation import computer, photo


class Director(VisualDirector):
    def show(self,obj,duration=.65):
        self.own(obj);self.play(m.FadeIn(obj),run_time=duration);return obj

    def fly(self,label,a,b,color=BLUE,duration=2):
        q=self.show(packet(label,color).move_to([*a,0]),.3)
        delta=np.array(b,dtype=float)-np.array(a,dtype=float)
        distance=float(np.linalg.norm(delta))
        end=np.array(b)-delta/max(distance,1e-9)*min(q.width/2+.18,distance*.7)
        path=self.own(m.Arrow([*a,0],[*end,0],buff=.05,color=color,stroke_width=2.5))
        self.play(q.animate.move_to([*b,0]),m.Create(path),run_time=duration)
        self.play(m.FadeOut(q),run_time=.4)
        return path

    def network(self,count=5):
        xs=(-5.5,-2.75,0,2.75,5.5)
        names=('Computer','Resolver','Root','TLD directory','Record keeper')
        colors=(BLUE,GREEN,YELLOW,PURPLE,BLUE)
        nodes=[self.own(host(n,x,1,c)) for n,x,c in list(zip(names,xs,colors))[:count]]
        self.play(*(m.FadeIn(n) for n in nodes),run_time=1)
        return xs,nodes

    def cache(self,address='192.0.2.10',ttl=60):
        box=self.own(m.RoundedRectangle(width=5.4,height=1.6,corner_radius=.15,color=GREEN).move_to([0,0,0]))
        self.play(m.Create(box),run_time=.8)
        self.show(text('photos.orbit.example',0,.43,27,BLUE,4.8))
        self.show(text(address,0,-.25,30,GREEN,4.8))
        self.show(text('Cached answer',0,1.35,25,MUTED))
        timer=self.show(text(f'TTL = {ttl} s',0,-1.35,30,YELLOW))
        return box,timer

    def animate(self,index,section,budget):
        self.reset()
        if index==0:
            self.show(computer('Your computer',-4,.5))
            self.show(computer('Photo server',4,.5,GREEN))
            picture=self.show(photo(4,.5))
            self.show(text('A server stores and sends information',0,-1.3,28))
            path=self.own(line((-3,.5),(3,.5)))
            self.play(m.Create(path),run_time=1.5)
            self.show(text('Which address should we contact?',0,-2.4,30,YELLOW))
            question=self.show(packet('?',BLUE).move_to([-4,.5,0]))
            self.play(m.Indicate(question),m.Indicate(picture),run_time=1.4)
        elif index==1:
            name=self.show(packet('Friend',BLUE,3.7,.8).move_to([-3.2,.6,0]))
            addr=self.show(packet('Phone number',GREEN,3.7,.8).move_to([3.2,.6,0]))
            arrow=self.own(m.Arrow([-1.2,.6,0],[1.2,.6,0],buff=.05,color=YELLOW))
            self.play(m.Create(arrow),run_time=1.5)
            self.play(m.Transform(name,packet('photos.orbit.example',BLUE,4.6,.9).move_to([-3.3,.6,0])),
                      m.Transform(addr,packet('192.0.2.10',GREEN,3.6,.9).move_to([3.4,.6,0])),run_time=2)
            self.show(text('Website name',-3.3,1.7,27,BLUE,5))
            self.show(text('IP address',3.4,1.7,27,GREEN,4))
            self.show(text('DNS finds information for a name',0,-1.3,30,YELLOW))
            self.show(text('Domain Name System',0,-2.3,26,MUTED))
        elif index==2:
            self.show(computer('Your computer',-4,.5))
            helper=self.show(computer('Helper',3.5,.5,GREEN))
            self.fly('name?',(-3,-.8),(2.5,-.8),BLUE,2.5)
            self.show(text('Resolver = the helper that finds an answer',0,-2,28,GREEN))
            self.play(m.Indicate(helper),run_time=1.3)
        elif index==3:
            pieces=[('Root: the starting directory',YELLOW),('example',PURPLE),('orbit.example',GREEN),('photos.orbit.example',BLUE)]
            prev=None
            for j,(label,c) in enumerate(pieces):
                y=1.9-j*1.15
                self.show(packet(label,c,5.4,.65).move_to([0,y,0]))
                if prev is not None:
                    a=self.own(m.Arrow([0,prev-.4,0],[0,y+.4,0],buff=.02,color=MUTED))
                    self.play(m.Create(a),run_time=1.5)
                prev=y
            self.show(text('Smaller parts inside larger parts',0,-2.6,26,WHITE))
        elif index in (4,5,6,7,12,13):
            xs,nodes=self.network(index-1 if index in (4,5,6) else 5)
            if index in (4,5,6):
                target=index-2
                self.fly('name?',(xs[1],-.1),(xs[target],-.1))
                label='TLD referral' if index==4 else 'Zone referral' if index==5 else '192.0.2.10'
                self.fly(label,(xs[target],-1),(xs[1],-1),GREEN,2.6)
                self.play(m.Indicate(nodes[target]),run_time=1.5)
                self.show(text('Direction, not final address' if index<6 else 'Authoritative answer',0,-2.2,28,GREEN))
            elif index==7:
                self.fly('192.0.2.10',(xs[4],-.1),(xs[1],-.1),GREEN,3)
                self.fly('192.0.2.10',(xs[1],-1),(xs[0],-1),GREEN,2)
                self.show(text('Name resolution complete',0,-2.25,30,GREEN))
            elif index==12:
                self.show(text('TTL = 0',-2.75,2.15,29,RED))
                for target in (2,3,4):
                    self.fly('refresh?',(xs[1],-.1),(xs[target],-.1),BLUE,1.6)
                    self.fly('referral' if target<4 else '203.0.113.20',(xs[target],-1),(xs[1],-1),GREEN,1.6)
                self.show(text('A fresh answer replaces the old copy',0,-2.3,27,GREEN))
            else:
                self.fly('known address',(xs[0],-.1),(xs[4],-.1),GREEN,3)
                self.fly('name?',(xs[0],-1),(xs[1],-1),BLUE,2)
                mark=self.own(m.VGroup(line((-2.95,-1.2),(-2.55,-.8),RED,4),line((-2.95,-.8),(-2.55,-1.2),RED,4)))
                self.play(m.Create(mark),run_time=.7)
                self.show(text('Reachable path ≠ resolved name',0,-2.3,28,WHITE))
        elif index==8:
            labels=('Local','Root','TLD','Authority');values=(2,20,30,40)
            cumulative=0
            axis=self.own(line((-5.5,.2),(5.5,.2),MUTED));self.play(m.Create(axis),run_time=.8)
            total=self.show(text('0 ms',0,-1.7,36,YELLOW))
            for j,(label,value) in enumerate(zip(labels,values)):
                x=-5.5+11*cumulative/92;w=11*value/92
                rect=self.own(m.Rectangle(width=w,height=.6,color=(BLUE,GREEN,PURPLE,YELLOW)[j],fill_opacity=.55).move_to([x+w/2,.55,0]))
                self.play(m.GrowFromCenter(rect),run_time=2)
                self.show(text(f'{label}: {value} ms',-4.5+j*3,1.7,23,WHITE,2.8))
                cumulative+=value
                self.play(m.Transform(total,text(f'{cumulative} ms',0,-1.7,36,YELLOW)),run_time=1)
            self.show(text('2 + 20 + 30 + 40 = 92 ms',0,-.65,30,WHITE))
        elif index==9:
            for j,(name,value,color) in enumerate((('Uncached',92,BLUE),('Cached',2,GREEN))):
                y=1-j*1.8
                self.show(text(name,-4.6,y,28,color,2.8))
                bar=self.own(m.Rectangle(width=7*value/92,height=.65,color=color,fill_opacity=.55).move_to([-2.5+3.5*value/92,y,0]))
                self.play(m.GrowFromEdge(bar,m.LEFT),run_time=2)
                self.show(text(f'{value} ms',5.2,y,28,color,2))
            self.show(text('92 ÷ 2 = 46× faster lookup',0,-2.1,30,YELLOW))
        elif index==10:
            box,timer=self.cache()
            for seconds in (45,30,15):
                self.play(m.Transform(timer,text(f'TTL = {seconds} s',0,-1.35,30,YELLOW)),run_time=2)
                self.play(m.Indicate(box),run_time=.8)
            self.show(text('A cache hit does not reset the clock',0,-2.4,26,WHITE))
        elif index==11:
            for x,title,addr,col in ((-3,'Cached copy','192.0.2.10',BLUE),(3,'Authority','192.0.2.10',GREEN)):
                self.show(text(title,x,1.5,28,col,5))
                self.show(packet(addr,col,4,.85).move_to([x,.4,0]))
            q=self.objects[-1]
            self.play(m.Transform(q,packet('203.0.113.20',GREEN,4,.85).move_to([3,.4,0])),run_time=2)
            self.show(text('TTL remaining: 30 s',-3,-.8,27,YELLOW,5))
            for label in ('old reply','old reply'):
                self.fly(label,(-3,-1.6),(-5.5,-1.6),BLUE,1.6)
            self.show(text('Changed at the source ≠ changed everywhere',0,-2.5,25,WHITE))
        elif index==14:
            centers=((-4,1), (0,1), (4,1))
            for label,center,col in zip(('Hierarchy','Referrals','Cache + TTL'),centers,(BLUE,GREEN,YELLOW)):
                circle=self.own(m.Circle(radius=1.4,color=col).move_to([*center,0]))
                self.play(m.Create(circle),run_time=1.5)
                self.show(text(label,*center,27,col,3.5))
            for a,b in ((-2.5,-1.5),(1.5,2.5)):
                arrow=self.own(m.Arrow([a,1,0],[b,1,0],buff=.02,color=MUTED));self.play(m.Create(arrow),run_time=1.5)
            self.show(text('Divide responsibility → find answers → reuse briefly',0,-1.4,28,WHITE))
        else:
            self.show(host('Computer',-4,.8,BLUE));self.show(host('Destination',4,.8,GREEN))
            self.fly('192.0.2.10',(-4,-.35),(4,-.35),GREEN,3)
            self.show(text('A path',-2,-1.5,31,BLUE));self.show(text('+',0,-1.5,31,WHITE));self.show(text('Directions',2,-1.5,31,GREEN))
            self.show(text('Connected and resolved',0,-2.5,32,YELLOW))
        self.finish(budget)
