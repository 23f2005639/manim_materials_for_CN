"""One weighted graph, one shortest-path algorithm, and a changed connection."""
from .common import *

POSITIONS={'A':(-5.3,0),'B':(-2.6,1.45),'C':(-2.6,-1.35),'D':(.8,1.45),'E':(.8,-1.35),'F':(4.8,0)}
EDGES=[('A','B',4),('A','C',2),('B','C',1),('B','D',5),('C','D',8),('C','E',10),('D','E',2),('D','F',6),('E','F',3)]
FINAL={'A':0,'B':3,'C':2,'D':8,'E':10,'F':13}
BEST=['A','C','B','D','E','F']


class Director(VisualDirector):
    def node(self,name,distance=None,color=BLUE):
        x,y=POSITIONS[name]
        parts=[m.Circle(radius=.32,color=color,stroke_width=2.5,fill_color=BG,fill_opacity=1).move_to([x,y,0]),text(name,x,y,26,color)]
        if distance is not None:
            parts.append(m.VGroup(m.Rectangle(width=.9,height=.5,color=BG,stroke_width=0,fill_color=BG,fill_opacity=1).move_to([x,y+.65,0]),text(str(distance),x,y+.65,30,color,.8)))
        return m.VGroup(*parts).set_z_index(4)

    def graph(self,dist=None,settled=(),failed=False,weights=True):
        self.nodes={};self.edges={};self.values=dict(dist or {})
        for a,b,cost in EDGES:
            color=RED if failed and {a,b}=={'D','E'} else MUTED
            edge=self.own(line(POSITIONS[a],POSITIONS[b],color,2));self.edges[frozenset((a,b))]=edge;self.s.add(edge)
            if weights:
                x=(POSITIONS[a][0]+POSITIONS[b][0])/2;y=(POSITIONS[a][1]+POSITIONS[b][1])/2
                if (a,b) in (('B','C'),('D','E')):x+=.43
                elif (a,b)==('C','D'):x-=.27;y+=.04
                elif a in ('B','C') and b in ('D','E'):y+=.27 if a=='B' else -.27
                label=packet(str(cost),WHITE,.52,.38).move_to([x,y,0]);self.own(label);self.s.add(label)
        for name in POSITIONS:
            obj=self.own(self.node(name,None if dist is None else dist.get(name,'∞'),GREEN if name in settled else BLUE))
            self.nodes[name]=obj;self.s.add(obj)
        if failed:
            x,y=POSITIONS['D'][0],.05
            cross=self.own(m.VGroup(line((x-.18,y-.18),(x+.18,y+.18),RED,4),line((x-.18,y+.18),(x+.18,y-.18),RED,4)).set_z_index(6));self.s.add(cross)
        self.eq=None

    def equation(self,value,color=YELLOW):
        target=text(value,0,-2.65,29,color,12.5)
        if self.eq is None:
            self.eq=self.own(target);self.play(m.FadeIn(self.eq),run_time=.7)
        else:self.play(m.Transform(self.eq,target),run_time=.7)

    def change(self,name,value,color=YELLOW):
        self.values[name]=value
        self.play(m.Transform(self.nodes[name],self.node(name,value,color)),run_time=1)

    def settle(self,name):
        self.change(name,self.values[name],GREEN)
        circle=self.own(m.Circle(radius=.48,color=GREEN,stroke_width=3).move_to([*POSITIONS[name],0]))
        self.play(m.Create(circle),run_time=.7)
        self.play(m.FadeOut(circle),run_time=.5)

    def travel(self,path,color=GREEN,totals=False):
        dot=self.own(m.Dot([*POSITIONS[path[0]],0],radius=.105,color=color).set_z_index(1))
        self.play(m.FadeIn(dot),run_time=.3)
        total=0
        for a,b in zip(path,path[1:]):
            self.play(self.edges[frozenset((a,b))].animate.set_stroke(color,width=4),dot.animate.move_to([*POSITIONS[b],0]),run_time=1.5)
            total+=next(c for x,y,c in EDGES if {x,y}=={a,b})
            if totals:self.equation(f'Accumulated cost = {total}',color)
        self.play(m.FadeOut(dot),run_time=.3)

    def relax(self,a,b,cost,new,previous):
        dot=self.own(m.Dot([*POSITIONS[a],0],radius=.105,color=YELLOW).set_z_index(1))
        self.play(m.FadeIn(dot),run_time=.3)
        self.play(dot.animate.move_to([*POSITIONS[b],0]),self.edges[frozenset((a,b))].animate.set_stroke(YELLOW,width=3.5),run_time=1.5)
        self.equation(f'{self.values[a]} + {cost} = {new}   <   {previous}',YELLOW)
        self.change(b,new)
        self.play(m.FadeOut(dot),run_time=.3)

    def animate(self,index,section,budget):
        self.reset()
        stages={
            3:({'A':0},()),
            4:({'A':0},()),
            5:({'A':0,'B':4,'C':2},('A',)),
            6:({'A':0,'B':3,'C':2,'D':10,'E':12},('A','C')),
            7:({'A':0,'B':3,'C':2,'D':8,'E':12},('A','C','B')),
            8:({'A':0,'B':3,'C':2,'D':8,'E':10,'F':14},('A','C','B','D')),
            9: (FINAL,('A','C','B','D','E')),
        }
        if index<3:
            self.graph(weights=index>0)
            if index==0:
                self.travel(['A','B','D','F'],RED)
                self.equation('Three links: the tempting shortcut',RED)
                self.travel(BEST,GREEN)
            elif index==1:
                for key,e in self.edges.items():
                    self.play(e.animate.set_stroke(BLUE,width=3.5),run_time=.35)
                self.equation('Cost belongs to each connection')
            else:
                self.travel(['A','B','D','F'],RED,True)
                self.equation('4 + 5 + 6 = 15',RED)
                self.travel(BEST,GREEN,True)
                self.equation('2 + 1 + 5 + 2 + 3 = 13',GREEN)
        elif index in stages:
            dist,settled=stages[index];self.graph(dist,settled)
            if index==3:
                for n in 'ABCDEF':self.change(n,0 if n=='A' else '∞',BLUE)
                self.equation('Known distance: 0      Undiscovered: ∞')
            elif index==4:
                self.settle('A');self.relax('A','B',4,4,'∞');self.relax('A','C',2,2,'∞')
                self.equation('Next smallest unfinished estimate: C = 2')
            elif index==5:
                self.settle('C');self.relax('C','B',1,3,4);self.relax('C','D',8,10,'∞');self.relax('C','E',10,12,'∞')
            elif index==6:
                self.settle('B');self.relax('B','D',5,8,10)
                self.equation('Candidate = known distance + link cost')
            elif index==7:
                self.settle('D');self.relax('D','E',2,10,12);self.relax('D','F',6,14,'∞')
                self.equation('F = 14 is discovered, not settled',YELLOW)
            elif index==8:
                self.settle('E');self.relax('E','F',3,13,14)
            else:
                self.settle('F');self.travel(BEST,GREEN)
                self.equation('Settled distance to F = 13',GREEN)
        elif index==10:
            self.graph(FINAL,tuple('ACB'))
            frontier=self.own(m.RoundedRectangle(width=4.1,height=4.5,corner_radius=.3,color=GREEN,stroke_width=2).move_to([-3.8,.2,0]))
            self.play(m.Create(frontier),run_time=2)
            self.equation('Every remaining link adds a nonnegative cost')
            self.play(m.Indicate(self.nodes['D'],color=YELLOW),run_time=1.3)
        elif index==11:
            self.graph(FINAL,tuple(FINAL))
            self.equation('F  ←  E  ←  D  ←  B  ←  C  ←  A',GREEN)
            self.travel(list(reversed(BEST)),GREEN)
            self.equation('Reverse the predecessor chain',GREEN)
        elif index==12:
            self.graph(FINAL,tuple(FINAL));self.travel(BEST,GREEN,True)
            self.equation('A → C → B → D → E → F     cost 13',GREEN)
        elif index==13:
            self.graph(FINAL,tuple(FINAL),failed=True)
            self.equation('The old route crosses a missing connection',RED)
            self.travel(['A','C','B','D'],YELLOW)
            self.change('E','?',RED);self.change('F','?',RED)
        elif index==14:
            self.graph({'A':0,'B':3,'C':2,'D':8,'E':12,'F':14},tuple('ACBDE'),failed=True)
            self.travel(['A','C','E','F'],RED)
            self.equation('Via C and E: 2 + 10 + 3 = 15',RED)
            self.travel(['A','C','B','D','F'],GREEN)
            self.equation('Via C, B, D: 2 + 1 + 5 + 6 = 14',GREEN)
            self.settle('F')
        else:
            self.graph({'A':0,'B':3,'C':2,'D':8,'E':12,'F':14},tuple(FINAL),failed=True)
            self.travel(['A','C','B','D','F'],GREEN,True)
            self.equation('Small comparisons → a complete shortest route',GREEN)
        self.finish(budget)
