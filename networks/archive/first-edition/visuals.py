"""Animated, locally generated networking diagrams for the eight episode storyboards.

Every diagram stays inside the shared stage and returns its complete visual group.
Labels describe textbook models; packet and timing examples are intentionally small.
"""
from __future__ import annotations

import math
import numpy as np
import manimgx as m

WHITE = "#E8F0FD"
MUTED = "#9FB2CD"
BLUE = "#58B7FF"
TEAL = "#50E3C2"
GOLD = "#FFCD70"
RED = "#FF718A"
VIOLET = "#B19AFF"
INK = "#14233B"
COLORS = (BLUE, TEAL, GOLD, VIOLET)


def label(value, x, y, size=22, color=WHITE, width=None):
    obj = m.Text(str(value), font="Noto Sans", font_size=size, color=color)
    if width and obj.width > width:
        obj.scale(width / obj.width)
    return obj.move_to([x, y, 0])


def card(value, x, y, width=1.65, height=0.62, color=BLUE, size=21):
    shape = m.RoundedRectangle(width=width, height=height, corner_radius=0.10,
                               color=color, stroke_width=1.6,
                               fill_color=INK, fill_opacity=1).move_to([x, y, 0])
    text = label(value, x, y, size, color, width - 0.16)
    return m.VGroup(shape, text)


def segment(a, b, color=MUTED, width=2):
    return m.Line([*a, 0], [*b, 0], color=color, stroke_width=width)


def arrow(a, b, color=BLUE, width=2.3):
    return m.Arrow([*a, 0], [*b, 0], buff=0.04, color=color, stroke_width=width,
                   max_tip_length_to_length_ratio=0.10)


def cross(x, y, radius=0.14):
    return m.VGroup(segment((x-radius, y-radius), (x+radius, y+radius), RED, 3),
                    segment((x-radius, y+radius), (x+radius, y-radius), RED, 3))


def reveal(scene, group, runtime=0.55):
    scene.play(m.FadeIn(group), run_time=runtime)


def pulse(scene, group, color=TEAL, runtime=0.6):
    scene.play(m.Indicate(group, color=color, scale_factor=1.06), run_time=runtime)


def travel(scene, group, a, b, text="DATA", color=BLUE, duration=0.85):
    packet = card(text, *a, width=1.25, height=0.43, color=color, size=18)
    group.add(packet)
    scene.add(packet)
    scene.play(packet.animate.move_to([*b, 0]), run_time=duration, rate_func=m.linear)
    return packet


def wave(x0, x1, y, frequency=3, amplitude=0.15, color=BLUE, phase=0):
    xs = np.linspace(x0, x1, 160)
    ys = y + amplitude * np.sin((xs-x0)/(x1-x0) * m.TAU * frequency + phase)
    curve = m.VMobject(color=color, stroke_width=2.5)
    curve.set_points_as_corners(np.column_stack((xs, ys, np.zeros_like(xs))))
    return curve


def website(scene, i, section):
    g = m.VGroup()
    if i==3:
        g.add(label("OSI: 7 LAYERS",.0,1.95,19,MUTED),label("TCP/IP: 4-LAYER MODEL",4.45,1.95,19,MUTED,3.7))
        osi=("Application","Presentation","Session","Transport","Network","Data link","Physical")
        for j,name in enumerate(osi):
            y=1.25-j*.5
            color=GOLD if j<3 else TEAL if j==3 else BLUE if j==4 else VIOLET
            g.add(card(name,.0,y,2.4,.43,color,18))
            destination=.75 if j<3 else -.25 if j==3 else -.75 if j==4 else -1.5
            g.add(arrow((1.3,y),(2.85,destination),color,1.7))
        for name,y,height,color in (("Application",.75,1.4,GOLD),("Transport",-.25,.43,TEAL),("Internet",-.75,.43,BLUE),("Link",-1.5,.94,VIOLET)):
            g.add(card(name,4.45,y,2.9,height,color,22))
        reveal(scene,g)
        pulse(scene,g[-4],GOLD);pulse(scene,g[-1],VIOLET)
        return g
    if i==14:
        g.add(label("BITS → PHYSICAL SIGNALS",2.3,1.9,21,MUTED))
        bits=(1,0,1,1,0,0,1,0)
        bitrow=m.VGroup(*[card(str(bit),-.65+j*.82,1.0,.67,.6,BLUE if bit else TEAL,24) for j,bit in enumerate(bits)])
        g.add(bitrow)
        points=[]
        for j,bit in enumerate(bits):
            x=-1.05+j*.82;y=.05 if bit else -.65
            points.extend(((x,y,0),(x+.82,y,0)))
        trace=m.VMobject(color=GOLD,stroke_width=3).set_points_as_corners(np.array(points))
        g.add(trace,label("Illustrative logic levels",2.3,-1.25,22,GOLD),
              label("Electrical, optical or radio signals carry encoded bits",2.3,-2.0,19,MUTED,7.7))
        reveal(scene,m.VGroup(g[0],bitrow,g[3],g[4]))
        scene.play(m.Create(trace),run_time=1.4)
        pulse(scene,bitrow[2],BLUE)
        return g
    if i in (10, 11, 12, 13, 19):
        levels = [("Application", "HTTP", GOLD), ("Transport", "TCP", TEAL),
                  ("Internet", "IP", BLUE), ("Link", "Ethernet", VIOLET)]
        g.add(label("ENCAPSULATION" if i != 19 else "DECAPSULATION", 2.3, 1.85, 19, MUTED))
        for j, (name, proto, color) in enumerate(levels):
            y = 1.1 - j * 0.8
            g.add(card(name, 0.0, y, 2.25, 0.59, color, 20))
            g.add(arrow((1.27, y), (2.0, y), color))
            widths = [2.15, 2.65, 3.15, 3.65]
            packet = card(("HTTP data", "TCP | HTTP", "IP | TCP | HTTP", "Frame | IP | TCP | HTTP")[j],
                          4.15, y, widths[j], 0.57, color, 18)
            g.add(packet)
        reveal(scene, g)
        order = range(3, -1, -1) if i == 19 else range(4)
        for j in order:
            pulse(scene, g[2 + j * 3], COLORS[j], 0.45)
        return g
    if i in (4, 5, 6):
        g.add(card("Browser", -0.65, 0.9), card("Resolver", 2.25, 0.9, color=TEAL),
              card("DNS authority", 5.2, 0.9, width=2.0, color=GOLD))
        g.add(segment((0.25, 0.9), (1.35, 0.9)), segment((3.1, 0.9), (4.15, 0.9)))
        g.add(label("Which address serves example.test?", 2.25, 1.85, 21, WHITE, 7.4))
        if i == 5:
            g.add(card("Root → TLD → authoritative", 2.3, -1.3, 6.5, 0.65, VIOLET, 23))
        elif i == 6:
            g.add(card("Cached answer • expires with TTL", 2.3, -1.3, 6.5, 0.65, TEAL, 23))
        else:
            g.add(card("DNS maps names to records", 2.3, -1.3, 6.5, 0.65, GOLD, 23))
        reveal(scene, g)
        travel(scene, g, (-0.65, 0.35), (2.25, 0.35), "QUERY")
        travel(scene, g, (2.25, -0.35), (-0.65, -0.35), "ANSWER", TEAL)
        return g
    if i == 8:
        return transport_timeline(scene, [("SYN  seq=100", "right", BLUE),
                                          ("SYN+ACK  seq=500  ack=101", "left", TEAL),
                                          ("ACK  ack=501", "right", GOLD)])
    if i == 22:
        g.add(card("HTTP/1.1 + TCP", 0.2, 0.9, 2.7, color=BLUE),
              card("HTTPS: protection", 4.4, 0.9, 3.3, color=TEAL),
              card("HTTP/3 uses QUIC / UDP", 2.3, -0.65, 6.3, 0.85, VIOLET, 25),
              label("Our walkthrough is one simplified model", 2.3, -1.65, 20, MUTED, 7.3))
        reveal(scene, g)
        pulse(scene, g[1])
        pulse(scene, g[2], VIOLET)
        return g
    g.add(card("Browser", -0.65, 0.65, 1.55, 0.8),
          card("Switch", 1.45, 0.65, 1.35, 0.8, TEAL),
          card("Router", 3.55, 0.65, 1.35, 0.8, GOLD),
          card("Server", 5.65, 0.65, 1.45, 0.8, VIOLET))
    if i in (0,2):
        old_nodes=list(g.submobjects)
        for j,(x,name,color) in enumerate(((-.65,"Browser",BLUE),(1.45,"Switch",TEAL),(3.55,"Router",GOLD),(5.65,"Server",VIOLET))):
            old=old_nodes[j]
            g.remove(old)
            device=m.Cube(side_length=.62,fill_color=color,fill_opacity=.8,stroke_color=color,stroke_width=1)
            device.rotate(.55,axis=m.RIGHT).rotate(-.55,axis=m.UP).move_to([x,.85,0])
            g.add(device,label(name,x,.18,18,color))
    for a, b in ((0.15, 0.75), (2.15, 2.85), (4.25, 4.9)):
        g.add(segment((a, 0.65), (b, 0.65)))
    captions = {0: "One request, many cooperating protocols", 1: "Simplified HTTP/1.1 over TCP", 2: "Local network → wider network → destination",
                7: "Ports identify application endpoints", 9: "HTTP request: GET /", 15: "Switch: forward a frame using MAC addresses",
                16: "Router: choose the next IP hop", 17: "A new link frame at every routed hop", 18: "Queues can delay or drop packets",
                20: "The HTTP response travels back", 21: "A page may need many resource requests", 23: "Names • transport • routing • link delivery"}
    g.add(label(captions.get(i, "Data moves through a layered network"), 2.3, -1.25, 22, MUTED, 7.7))
    if i==7:
        g.add(card("Client port 49152 → server port 80",2.3,-1.9,6.4,.5,TEAL,20))
    if i == 18:
        for j in range(5):
            g.add(card(str(j+1), 2.6 + j*0.48, -0.4, 0.4, 0.4, GOLD, 17))
        g.add(cross(5.3, -0.4))
    reveal(scene, g)
    if i in (20,):
        travel(scene, g, (5.6, -0.25), (3.5, -0.25), "HTTP", TEAL)
        travel(scene, g, (3.5, -0.25), (-0.65, -0.25), "REPLY", TEAL)
    else:
        packet = travel(scene, g, (-0.65, -0.25), (1.45, -0.25), "DATA")
        scene.play(packet.animate.move_to([3.55, -0.25, 0]), run_time=0.7, rate_func=m.linear)
        scene.play(packet.animate.move_to([5.65, -0.25, 0]), run_time=0.7, rate_func=m.linear)
    return g


def multiplex(scene, i, section):
    g = m.VGroup()
    if i in (0, 1, 2):
        for j in range(3):
            y = 1.3-j*1.1
            g.add(card("Source " + chr(65+j), -0.7, y, 1.5, 0.6, COLORS[j]))
            g.add(arrow((0.1,y), (1.35,0.2), COLORS[j]))
        g.add(card("MUX", 2.0, 0.2, 1.0, 1.6, VIOLET),
              card("DEMUX", 5.55, 0.2, 1.4, 1.6, VIOLET),
              segment((2.55,0.2),(4.8,0.2), MUTED, 7),
              label("ONE PHYSICAL MEDIUM", 3.8, -1.4, 18, MUTED, 4.8))
        reveal(scene,g)
        for j in range(3):
            travel(scene,g,(2.7,0.2+(j-1)*.58),(4.1,0.2+(j-1)*.58), chr(65+j), COLORS[j],0.6)
        return g
    if 3 <= i <= 8:
        g.add(label("FREQUENCY DIVISION",2.3,1.9,19,MUTED))
        for j in range(3):
            y=1.05-j*1.03
            g.add(label(chr(65+j),-1.05,y,22,COLORS[j]),wave(-.6,2.5,y,j+2,.20,COLORS[j]))
            g.add(card(["0–20 kHz", "25–45 kHz", "50–70 kHz"][j],4.65,y,2.25,.65,COLORS[j],21))
        if i == 5:
            g.add(label("5 kHz guard bands separate channels",2.3,-2.15,19,GOLD,7.4))
        elif i == 7:
            g.add(label("3 × 20 kHz + 2 × 5 kHz = 70 kHz",2.3,-2.15,21,GOLD,7.4))
        else:
            g.add(label("Different bands • same time",2.3,-2.15,20,MUTED))
        reveal(scene,g)
        for j in range(3):
            extra = wave(-.6,2.5,1.05-j*1.03,j+2,.20,COLORS[j],1)
            scene.play(m.Transform(g[2+3*j], extra), run_time=.65)
        pulse(scene,g[3+3*(i%3)],COLORS[i%3])
        return g
    if 9 <= i <= 15:
        g.add(label("TIME DIVISION",2.3,1.9,19,MUTED))
        xs=[-.95+j*.62 for j in range(12)]
        slots=m.VGroup()
        sequence=(0,0,2,0,2,2,0,0,2,0,2,0) if i==15 else tuple(j%3 for j in range(12))
        for j,x in enumerate(xs):
            source=sequence[j]
            idle=i==14 and source==1
            slot=card(chr(65+source),x,.55,.56,.72,MUTED if idle else COLORS[source],22)
            if idle:
                slot.remove(slot[1])
                slot.add(segment((x-.12,.55),(x+.12,.55),MUTED,2))
            slots.add(slot)
        g.add(slots,arrow((-1.35,-.2),(6.3,-.2),MUTED),label("time →",5.6,-.6,18,MUTED))
        for j in range(4):
            g.add(label(("group " if i==15 else "frame ") + str(j+1),-.33+j*1.86,1.2,18,MUTED))
        g.add(card("A",.1,-1.45,1,.55,BLUE),card("B",2.3,-1.45,1,.55,TEAL),card("C",4.5,-1.45,1,.55,GOLD))
        if i==13:
            g.add(label("3 × 2 Mb/s = 6 Mb/s, before overhead",2.3,-2.2,19,GOLD,7.6))
        elif i==15:
            g.add(label("Statistical TDM assigns slots to active sources",2.3,-2.2,19,GOLD,7.6))
        else:
            g.add(label("Each source gets a scheduled turn",2.3,-2.2,19,MUTED))
        reveal(scene,g)
        for j in range(3): pulse(scene,slots[(i+j)%12],COLORS[(i+j)%3],.5)
        return g
    if 16 <= i <= 20:
        g.add(label("WAVELENGTH DIVISION",2.3,1.9,19,MUTED))
        fiber=m.RoundedRectangle(width=5.6,height=1.35,corner_radius=.25,color=MUTED,
                                  fill_color="#172942",fill_opacity=.8).move_to([2.3,.2,0])
        g.add(fiber)
        count=4 if i==19 else 3
        for j in range(count):
            y=.65-j*.32 if count==4 else .6-j*.4
            g.add(wave(-.4,5.0,y,4+j,.09,COLORS[j]))
            g.add(label(["λ₁", "λ₂", "λ₃", "λ₄"][j],5.7,y,23,COLORS[j]))
        g.add(label("Several optical wavelengths inside one fiber",2.3,-1.3,21,MUTED,7.6))
        if i==19:g.add(label("4 wavelengths × 10 Gb/s = 40 Gb/s",2.3,-2.0,21,GOLD,7.6))
        elif i==20:g.add(label("Loss, dispersion and noise limit real links",2.3,-2.0,20,GOLD,7.6))
        reveal(scene,g)
        for j in range(count):
            y=.65-j*.32 if count==4 else .6-j*.4
            marker=m.Dot([-.3,y,0],radius=.075,color=COLORS[j],stroke_width=0)
            g.add(marker);scene.add(marker)
            scene.play(marker.animate.move_to([4.9,y,0]),run_time=.6,rate_func=m.linear)
        return g
    for j,(name,axis,detail) in enumerate((("FDM","Frequency","radio / electrical bands"),("TDM","Time","scheduled slots"),("WDM","Wavelength","optical fiber"))):
        x=.0+j*2.3
        g.add(card(name,x,.95,2,.8,COLORS[j],27),label(axis,x,-.05,23,COLORS[j]),label(detail,x,-.85,17,MUTED,2.2))
    g.add(label("Separate channels, then combine and recover them",2.3,-1.85,20,WHITE,7.6))
    reveal(scene,g)
    for j in range(3):pulse(scene,g[j*3],COLORS[j],.5)
    return g


def transport_timeline(scene, messages, caption="Time flows downward", lost=None):
    g=m.VGroup(label("SENDER",-.65,1.9,20,BLUE),label("RECEIVER",5.4,1.9,20,TEAL),
               segment((-.65,1.4),(-.65,-1.8),MUTED,1.5),segment((5.4,1.4),(5.4,-1.8),MUTED,1.5),
               label(caption,2.3,-2.25,18,MUTED,7.5))
    reveal(scene,g,.4)
    count=len(messages)
    for j,(text,direction,color) in enumerate(messages):
        top=1.2-j*(2.75/max(count,1))
        if direction=="local":
            tick=m.Circle(radius=.13,color=color,stroke_width=2.5).move_to([-.65,top,0])
            badge=label(text,2.3,top,18,color,5.3)
            g.add(tick,badge)
            scene.play(m.FadeIn(tick),m.FadeIn(badge),run_time=.7)
            continue
        a=(-.65,top) if direction=="right" else (5.4,top)
        b=(5.4,top-.46) if direction=="right" else (-.65,top-.46)
        if lost==j:
            mid=((a[0]+b[0])/2,(a[1]+b[1])/2)
            path=arrow(a,mid,RED)
            mark=cross(*mid,.17)
            g.add(path,mark,label(text,2.3,top+.12,17,RED,5.5))
            scene.play(m.Create(path),m.FadeIn(mark),run_time=.7)
        else:
            path=arrow(a,b,color)
            g.add(path,label(text,2.3,top+.12,17,color,5.5))
            scene.play(m.Create(path),run_time=.7)
    return g


def reliability(scene,i,section):
    if i in (14,15,16,17,21):
        g=m.VGroup(label("SLIDING WINDOW • next-expected ACK",2.3,1.9,18,MUTED,7.6))
        left=0
        cells=m.VGroup()
        for j in range(8):
            x=-.85+j*.9
            cells.add(card(str(j),x,.75,.78,.72,TEAL if j<left else BLUE if j<left+4 else MUTED,24))
        window=m.Rectangle(width=3.58,height=.95,color=GOLD,stroke_width=3).move_to([.5+left*.9,.75,0])
        g.add(cells,window,label("Window size W = 4",2.3,-.15,24,GOLD),
              label({16:"ACK 3 confirms frames 0, 1, 2; next expected is 3",17:"ACK 2 confirms frames 0, 1; next expected is 2",21:"ACK 4 confirms frames 0–3; next expected is 4"}.get(i,"ACK 1 confirms frame 0; next expected is 1"),2.3,-1.1,19,TEAL,7.7),
              label("Multiple frames can be in flight",2.3,-1.9,20,MUTED,7.7))
        reveal(scene,g)
        pulse(scene,cells[left],BLUE)
        if i in (17,21):
            scene.play(window.animate.shift((3.6 if i==21 else 1.8)*m.RIGHT),run_time=1)
            g.add(label("Advance after a cumulative acknowledgment",2.3,-2.25,17,GOLD,7.7))
            scene.add(g[-1])
        else:
            for j in range(3):pulse(scene,cells[left+j],BLUE,.4)
        return g
    if i in (18,19,20):
        if i==18: msgs=[("DATA 0", "right",BLUE),("DATA 1 lost", "right",RED),("DATA 2 discarded", "right",GOLD),("ACK 1 (next expected)","left",TEAL)]
        elif i==19:msgs=[("DATA 2: out of order", "right",GOLD),("ACK 1: still missing 1","left",TEAL),("DATA 3: out of order","right",GOLD)]
        else:msgs=[("Retransmit DATA 1","right",BLUE),("Retransmit DATA 2","right",BLUE),("Retransmit DATA 3","right",BLUE)]
        return transport_timeline(scene,msgs,"Go-Back-N receiver discards out-of-order frames",lost=1 if i==18 else None)
    if i in (7,8):
        return transport_timeline(scene,[("DATA 0 lost", "right",RED)],"Timeout expires without ACK" if i==8 else "No ACK returns for the missing data",lost=0)
    if i==9:
        return transport_timeline(scene,[("Retransmit saved DATA 0","right",BLUE),("ACK 1","left",TEAL)],"Retry the same sequence number, not a new one")
    if i in (10,11):
        return transport_timeline(scene,[("DATA 0 delivered","right",BLUE),("ACK 1 lost","left",RED),("DATA 0 repeated • discard duplicate","right",GOLD),("ACK 1 repeated","left",TEAL)],"Sequence numbers prevent duplicate delivery",lost=1)
    if i==12:
        g=m.VGroup(label("ALTERNATING-BIT PROTOCOL",2.3,1.8,20,MUTED))
        for j in range(6):g.add(card(str(j%2),-.55+j*1.12,.55,.9,.8,COLORS[j%2],30))
        g.add(label("0 → 1 → 0 → 1",2.3,-.5,30,GOLD),label("One outstanding frame; recognize a repeated sequence bit",2.3,-1.65,19,MUTED,7.7))
        reveal(scene,g)
        for j in range(3):pulse(scene,g[j+1],COLORS[j%2],.5)
        return g
    if i in (4,5,6):
        g=m.VGroup(label("STOP-AND-WAIT UTILIZATION",2.3,1.9,19,MUTED))
        busy=card("Transmit: 1 ms",-.05,.7,2.1,.7,BLUE)
        idle=card("Wait for round trip: 20 ms",3.65,.7,4.9,.7,MUTED)
        g.add(busy,idle,label("U ≈ 1 / (1 + 20) = 4.76%",2.3,-.45,30,GOLD,7.3),
              label("Example ignores ACK transmission and processing time",2.3,-1.55,18,MUTED,7.6))
        reveal(scene,g)
        pulse(scene,busy,BLUE)
        pulse(scene,idle,RED)
        return g
    if i==13:
        return transport_timeline(scene,[("DATA 0", "right",BLUE),("Timer expires too early","local",RED),("Delayed ACK 1","left",TEAL)],"Timeout must allow for delay variation")
    if i==22:
        g=m.VGroup(card("Textbook Go-Back-N",.25,.7,3.0,1,BLUE,24),card("TCP byte stream",4.4,.7,3.0,1,TEAL,24),
                   label("Related ideas; different protocol details",2.3,-.5,24,GOLD,7.7),label("Do not equate a classroom frame number with a TCP byte offset",2.3,-1.6,18,MUTED,7.7))
        reveal(scene,g);pulse(scene,g[0],BLUE);pulse(scene,g[1],TEAL)
        return g
    return transport_timeline(scene,[("DATA 0","right",BLUE),("ACK 1 = next frame expected","left",TEAL)],"Send → acknowledge → advance")


def channel(scene,i,section):
    g=m.VGroup()
    if i in (2,3,5,6,7):
        slotted=i in (5,6,7)
        g.add(label("SLOTTED ALOHA" if slotted else "PURE ALOHA",2.3,1.85,21,GOLD))
        for j,y in enumerate((.95,.0,-.95)):
            g.add(label(chr(65+j),-1.15,y,22,COLORS[j]),segment((-.7,y),(6.0,y),MUTED,1))
            if slotted:
                for k in range(7):g.add(segment((-.5+k*.95,y-.25),(-.5+k*.95,y+.25),"#33435B",1))
            start=[.45,.45,3.30][j] if slotted else [-.1,.7,3.1][j]
            center=start+.475 if slotted else start+1
            g.add(card("frame",center,y,.85 if slotted else 1.75,.48,COLORS[j],18))
        g.add(label("Vulnerable period: T" if slotted else "Vulnerable period: 2T",2.3,-1.85,23,RED))
        if i==7:g.add(label("Ideal model peaks: 1/e ≈ 36.8%; 1/(2e) ≈ 18.4%",2.3,-2.25,17,MUTED,7.5))
        reveal(scene,g)
        pulse(scene,g[2],BLUE)
        pulse(scene,g[-1],RED)
        return g
    if i in (17,18,19):
        g.add(label("BINARY EXPONENTIAL BACKOFF",2.3,1.9,20,MUTED,7.6))
        for j,(n,count) in enumerate(((1,2),(2,4),(3,8))):
            y=1-j*1.05
            g.add(label(f"collision {n}",-.4,y,19,MUTED))
            for k in range(count):g.add(card(str(k),1.0+k*.57,y,.48,.55,COLORS[j],18))
        g.add(label("Choose a random slot from 0 … 2ᵏ−1",2.3,-2.05,21,GOLD,7.6))
        reveal(scene,g)
        for j in (1,5,11):pulse(scene,g[j],TEAL,.5)
        return g
    if i in (20,21):
        g.add(card("Station A",-.45,1.0,1.65,.65,BLUE),card("Switch",2.3,.2,1.65,1.4,GOLD),
              card("Station B",5.05,1.0,1.65,.65,TEAL),
              arrow((.4,.95),(1.4,.55),BLUE),arrow((3.2,.55),(4.2,.95),TEAL),
              arrow((4.2,.45),(3.2,-.15),TEAL),arrow((1.4,-.15),(.4,.45),BLUE))
        g.add(label("Wi-Fi uses avoidance, not Ethernet collision detection" if i==21 else "Full-duplex links do not use CSMA/CD",2.3,-1.65,21,MUTED,7.6))
        reveal(scene,g);pulse(scene,g[1],GOLD);travel(scene,g,(.4,.2),(4.2,.2),"DATA",BLUE)
        return g
    bus=segment((-1.2,-.35),(6.1,-.35),MUTED,5)
    g.add(bus)
    for j,x in enumerate((-.45,2.3,5.05)):
        g.add(card("Host "+chr(65+j),x,1.0,1.65,.7,COLORS[j]),segment((x,.65),(x,-.35),COLORS[j]))
    collision=i in (0,1,10,14,15,16)
    captions={8:"Contention competes; a schedule reserves turns",9:"Listen before transmitting",10:"Propagation delay leaves a collision window",11:"1-persistent: transmit as soon as idle",12:"Nonpersistent: wait randomly after sensing busy",13:"p-persistent: probability p in an idle slot",14:"CSMA/CD: shared half-duplex Ethernet",15:"Detect → abort → jam → back off",16:"A frame must last long enough to detect collisions",22:"Access rules depend on the physical network",23:"Share • sense • detect or avoid • retry"}
    g.add(label(captions.get(i,"Two transmissions share the same medium"),2.3,-1.55,21,MUTED,7.7))
    reveal(scene,g)
    if collision:
        pa=card("A",-.45,-.35,.55,.4,BLUE,18);pb=card("C",5.05,-.35,.55,.4,GOLD,18)
        g.add(pa,pb);scene.add(pa,pb)
        scene.play(pa.animate.move_to([2.3,-.35,0]),pb.animate.move_to([2.3,-.35,0]),run_time=1.1,rate_func=m.linear)
        mark=cross(2.3,-.35,.25)
        g.add(mark)
        scene.play(m.FadeOut(pa),m.FadeOut(pb),m.FadeIn(mark),run_time=.3)
        scene.remove(pa,pb)
        g.remove(pa,pb)
    else:
        travel(scene,g,(-.45,-.35),(5.05,-.35),"DATA",BLUE)
        pulse(scene,g[3],TEAL)
    return g


GRAPH_POS={"A":(-.8,.0),"B":(.8,1.25),"C":(.8,-1.25),"D":(3.2,1.25),"E":(3.2,-1.25),"F":(5.6,.0)}
GRAPH_EDGES=[("A","B",4),("A","C",2),("B","C",1),("B","D",5),("C","D",8),("C","E",10),("D","E",2),("D","F",6),("E","F",3)]


def routing(scene,i,section):
    g=m.VGroup()
    v=section.get("visual",{})
    if v.get("mode")=="distancevector":
        if "count_to_infinity" in v:
            g.add(label("COUNTING TOWARD INFINITY",2.3,1.9,21,MUTED))
            for j,value in enumerate((3,4,5,6,16)):
                g.add(card(str(value),-.4+j*1.35,.7,1.1,.85,RED if value==16 else GOLD,30))
                if j<4:g.add(arrow((.2+j*1.35,.7),(.35+j*1.35,.7),MUTED))
            g.add(label("Stale neighbor claims can sustain a routing loop",2.3,-.45,22,RED,7.6),
                  label("RIP defines metric 16 as unreachable",2.3,-1.55,23,TEAL,7.6))
            reveal(scene,g)
            for j in (1,3,5,7,9):pulse(scene,g[j],RED if j==9 else GOLD,.35)
            return g
        if v.get("safeguard"):
            g.add(label("POISONED REVERSE",2.3,1.9,23,MUTED),
                  card("Router A",-.25,.75,2.4,.8,BLUE,25),card("Neighbor C",4.7,.75,2.4,.8,TEAL,25),
                  arrow((3.4,.75),(1.05,.75),TEAL),label("A's route learned through C",2.3,.0,22,TEAL,7.5),
                  arrow((1.05,-.75),(3.4,-.75),RED),label("Advertise ∞ back to that neighbor",2.3,-1.3,21,RED,7.5),
                  label("Helps prevent some loops; not a universal cure",2.3,-2.15,19,MUTED,7.5))
            reveal(scene,g);pulse(scene,g[4],TEAL);pulse(scene,g[6],RED)
            return g
        g.add(label("NEIGHBORS ADVERTISE ESTIMATES TO F",2.3,1.9,19,MUTED,7.6),
              card("A",-.65,.65,1,.8,BLUE,30),card("B: distance 10",4.1,1.0,3.2,.75,GOLD,23),
              card("C: distance 11",4.1,-.4,3.2,.75,TEAL,23),
              arrow((2.4,1.0),(.0,.65),GOLD),arrow((2.4,-.4),(.0,.65),TEAL),
              label("link A–B = 4",1.2,1.3,18,GOLD),label("link A–C = 2",1.2,-.3,18,TEAL),
              card("min(4 + 10, 2 + 11) = 13",2.3,-1.65,7.0,.75,BLUE,27))
        reveal(scene,g);pulse(scene,g[2],GOLD);pulse(scene,g[3],TEAL);pulse(scene,g[8],BLUE)
        return g
    # Same graph and numerical example throughout the episode.
    settled_order=["A","C","B","D","E","F"]
    stage=min(6,max(0,i-4)) if 4<=i<=10 else (6 if i>=11 else 0)
    settled=set(settled_order[:stage])
    distances=[{"A":0}, {"A":0,"B":4,"C":2}, {"A":0,"B":3,"C":2,"D":10,"E":12},
               {"A":0,"B":3,"C":2,"D":8,"E":12}, {"A":0,"B":3,"C":2,"D":8,"E":10,"F":14},
               {"A":0,"B":3,"C":2,"D":8,"E":10,"F":13}, {"A":0,"B":3,"C":2,"D":8,"E":10,"F":13}][stage]
    failed=i in (17,18)
    if failed:
        distances = dict(distances, E=12, F=14)
    cost_labels=[]
    for a,b,cost in GRAPH_EDGES:
        pa,pb=GRAPH_POS[a],GRAPH_POS[b]
        color=RED if failed and (a,b)==("D","E") else "#40516C"
        g.add(segment(pa,pb,color,2.3))
        mid=((pa[0]+pb[0])/2,(pa[1]+pb[1])/2)
        # Offset diagonal labels so crossings do not carry stacked numbers.
        if (a,b)==("C","D"):mid=(mid[0]+.25,mid[1]+.3)
        if (a,b)==("B","C"):mid=(mid[0]-.20,mid[1])
        if (a,b)==("D","E"):mid=(mid[0]+.20,mid[1])
        weight=card(str(cost),*mid,.44,.37,RED if failed and (a,b)==("D","E") else MUTED,18)
        cost_labels.append(weight)
        g.add(weight)
        if failed and (a,b)==("D","E"):g.add(cross(*mid,.18))
    node_groups={}
    for name,(x,y) in GRAPH_POS.items():
        color=TEAL if name in settled else BLUE
        box=card(name,x,y,.67,.62,color,25)
        value=distances.get(name,"∞")
        node_groups[name]=m.VGroup(box,card(f"d={value}",x,y-.5,.95,.38,color,18))
        g.add(node_groups[name])
    captions={0:"What makes a path best? Choose a metric first.",1:"Undirected example • positive link costs",2:"Path cost = sum of its link costs",3:"Routing computes paths; forwarding uses the table",4:"Initialize A = 0; all other distances = ∞",5:"Settle A: B = 4, C = 2",6:"Settle C: improve B to 3",7:"Settle B: improve D to 8",8:"Settle D: improve E to 10, F to 14",9:"Settle E: improve F to 13",10:"Settle F: every shortest distance is final",11:"A → C → B → D → E → F costs 13",12:"A's next hop toward F is C",13:"Distance vector: neighbors exchange distance estimates",14:"Toward F: min(4 + 10, 2 + 11) = 13",15:"Link state: flood link facts, compute locally",16:"Same goal; different information exchanged",17:"D–E fails: shortest A→F route now costs 14",18:"Updates take time to propagate",19:"Distance-vector loops may count toward infinity",20:"Poisoned reverse reduces some distance-vector loops",21:"Metric and policy determine the chosen path",22:"Hierarchy limits the routing information needed",23:"Discover • compute • forward • adapt"}
    g.add(label(captions.get(i,"Shortest paths from A"),2.3,-2.25,19,GOLD,7.8))
    reveal(scene,g)
    path=section.get("visual",{}).get("highlight_path", ["A","C","B","D","F"] if failed else ["A","C","B","D","E","F"])
    if v.get("mode")=="linkstate":
        for destination in ("B","E","F"):
            packet=travel(scene,g,GRAPH_POS["D"],GRAPH_POS[destination],"LINKS",GOLD,.45)
            scene.play(m.FadeOut(packet),run_time=.18)
            scene.remove(packet)
            g.remove(packet)
        for obj in cost_labels+list(node_groups.values()):scene.add(obj)
    elif i>=11 or section.get("visual",{}).get("highlight_path"):
        for a,b in zip(path,path[1:]):
            highlight=segment(GRAPH_POS[a],GRAPH_POS[b],TEAL,4)
            g.add(highlight);scene.play(m.Create(highlight),run_time=.25)
        # Restore node faces above path strokes.
        for obj in cost_labels+list(node_groups.values()):scene.add(obj)
    else:
        name=settled_order[max(0,stage-1)]
        pulse(scene,node_groups[name],TEAL,.75)
    return g


def subnet(scene,i,section):
    g=m.VGroup()
    visual=section.get("visual",{})
    mode=visual.get("mode", "bits")
    prefix=int(visual.get("prefix",26 if i>=6 else 24))
    if "exceptions" in visual or i==19:
        g.add(label("THE SUBTRACT-TWO RULE HAS EXCEPTIONS",2.3,1.9,19,MUTED,7.8),
              card("/26 ordinary LAN",2.3,1.0,6.6,.65,BLUE,23),
              label("64 addresses; usually 62 host addresses",2.3,.4,22,BLUE,7.4),
              card("/31 point-to-point",2.3,-.3,6.6,.65,TEAL,23),
              label("2 endpoint addresses",2.3,-.9,22,TEAL),
              card("/32: one specific address",2.3,-1.7,6.6,.65,GOLD,23))
        reveal(scene,g);pulse(scene,g[3],TEAL);pulse(scene,g[5],GOLD)
        return g
    if mode in ("subnets","hosts"):
        if prefix==24 and i==5:
            g.add(label("THE PARENT BLOCK",2.3,1.9,21,MUTED),
                  card("192.168.1.0/24",2.3,.8,6.7,.9,BLUE,30),
                  label("32 − 24 = 8 host bits",2.3,-.1,26,GOLD),
                  label("2⁸ = 256 total addresses",2.3,-1.0,27,TEAL),
                  label("Range: 192.168.1.0 … 192.168.1.255",2.3,-1.95,21,MUTED,7.6))
            reveal(scene,g);pulse(scene,g[2],GOLD);pulse(scene,g[3],TEAL)
            return g
        g.add(label("192.168.1.0/24 → FOUR /26 NETWORKS",2.3,1.9,19,MUTED,7.8))
        focus=int(visual.get("selected", max(0,i-10)%4))
        for j,base in enumerate((0,64,128,192)):
            y=1.03-j*.86
            color=COLORS[j]
            g.add(card(f"192.168.1.{base}/26",.25,y,3.1,.62,color,20),
                  label(f"hosts .{base+1}–.{base+62}",3.0,y,18,color,2.3),
                  label(f"bcast .{base+63}",5.25,y,18,MUTED,1.7))
        reveal(scene,g)
        pulse(scene,g[1+focus*3],COLORS[focus],.7)
        bottom=visual.get("equation", "")
        if "required_hosts" in visual:bottom="50 hosts: /27 offers 30; /26 offers 62"
        elif "addresses" in visual:bottom=".70 and .100 share /26; .130 is in another subnet"
        elif visual.get("routing"):bottom=".70 → router → .130: different destination prefix"
        elif visual.get("security") is False:bottom="Address boundaries alone do not enforce access policy"
        if bottom:
            mark=label(bottom,2.3,-2.25,18,GOLD,7.6)
            g.add(mark);reveal(scene,mark,.4)
        else:pulse(scene,g[2+focus*3],COLORS[focus],.6)
        return g
    if mode=="mask":
        address=visual.get("address","192.168.1.0")
        mask=visual.get("mask","255.255.255.192" if prefix==26 else "255.255.255.0")
        result=visual.get("result", "192.168.1.0")
        g.add(label("BITWISE AND REVEALS THE NETWORK",2.3,1.9,19,MUTED,7.7))
        for j,(name,value,color) in enumerate((("Address",address,BLUE),("Mask",mask,GOLD),("Network",result,TEAL))):
            y=1.05-j*1.05
            g.add(label(name,-.45,y,22,color),card(value,3.0,y,4.5,.7,color,26))
        last=int(address.split(".")[-1]);masklast=int(mask.split(".")[-1]);resultlast=last&masklast
        g.add(label(f"{last:08b} AND {masklast:08b} = {resultlast:08b}",2.3,-2.25,19,MUTED,7.6))
        reveal(scene,g);pulse(scene,g[3],GOLD);pulse(scene,g[5],TEAL)
        return g
    g.add(label(f"IPv4 • 32 BITS • /{prefix}",2.3,1.9,21,MUTED))
    values=tuple(map(int,visual.get("address","192.168.1.0").split(".")))
    bit_groups=m.VGroup()
    for octet,value in enumerate(values):
        row=octet//2; col=octet%2
        x0=-1.05+col*3.95
        y=1.0-row*1.45
        for bit,char in enumerate(f"{value:08b}"):
            number=octet*8+bit
            color=BLUE if number<24 else GOLD if number<prefix else TEAL
            bit_groups.add(card(char,x0+bit*.43,y,.38,.5,color,20))
        g.add(label(str(value),x0+1.5,y-.53,22,MUTED))
    g.add(bit_groups,label("BLUE: /24 prefix     GOLD: borrowed     GREEN: host",2.3,-1.65,17,MUTED,7.8))
    bottom="Borrow 2 bits → 2² = 4 subnets; 6 host bits remain" if prefix==26 else "The prefix selects the shared network beginning"
    if "prefix_patterns" in visual:bottom="Borrowed-bit patterns: 00   01   10   11"
    if "prefix_sizes" in visual:bottom="/25: 128 addresses    /26: 64    /27: 32"
    if visual.get("private"):bottom="Use the stated CIDR prefix; first octet alone is insufficient"
    g.add(label(bottom,2.3,-2.25,19,GOLD,7.7))
    reveal(scene,g)
    for k in (24,25,31):pulse(scene,bit_groups[k],GOLD if k<prefix else TEAL,.5)
    return g


def tcp_udp(scene,i,section):
    g=m.VGroup()
    v=section.get("visual",{})
    mode=v.get("mode", "udp")
    if mode=="handshake":
        if v.get("closing"):
            return transport_timeline(scene,[("FIN: client has no more bytes","right",BLUE),("ACK","left",TEAL),("FIN: server finishes its stream","left",GOLD),("ACK","right",TEAL)],"Each direction can close independently")
        msgs=[("SYN  seq=100", "right",BLUE),("SYN+ACK  seq=500  ack=101", "left",TEAL),("ACK  seq=101  ack=501", "right",GOLD)]
        step=int(v.get("step",3))
        return transport_timeline(scene,msgs[:step] if step else msgs,"SYN consumes one sequence number")
    if mode=="bytestream" and "seq" in v:
        return transport_timeline(scene,[("100 data bytes: seq=101…200","right",BLUE),("ACK 201 = next byte expected","left",TEAL)],"Cumulative ACK confirms every preceding byte")
    if mode=="reorder":
        if v.get("lost_ack"):
            return transport_timeline(scene,[("Bytes 101–200 delivered","right",BLUE),("ACK 201 lost","left",RED),("Duplicate bytes 101–200","right",GOLD),("ACK 201 repeated","left",TEAL)],"Do not deliver the same stream bytes twice",lost=1)
        if "retransmit" in v:
            return transport_timeline(scene,[("Retransmit bytes 201–300","right",BLUE),("ACK 401 = next byte expected","left",TEAL)],"Receiver now has contiguous bytes 101–400")
        return transport_timeline(scene,[("Bytes 101–200 arrive","right",BLUE),("Bytes 201–300 missing","right",RED),("Bytes 301–400 buffered","right",GOLD),("ACK 201: the gap remains","left",TEAL)],"Later bytes wait behind the missing stream range",lost=1)
    if mode=="window":
        if "congestion_window" in v:
            g.add(label("TWO INDEPENDENT LIMITS",2.3,1.9,21,MUTED),
                  card("Receiver window: 1000 bytes",2.3,.95,6.8,.75,TEAL,24),
                  card("Congestion window: 400 bytes",2.3,-.05,6.8,.75,GOLD,24),
                  label("Send within both limits",2.3,-1.15,27,WHITE),
                  label("Receiver capacity ≠ network capacity",2.3,-2.05,20,MUTED,7.5))
            reveal(scene,g);pulse(scene,g[1],TEAL);pulse(scene,g[2],GOLD)
            return g
        g.add(label("ADVERTISED WINDOW: 300 BYTES",2.3,1.9,20,MUTED))
        buffers=m.VGroup()
        for j in range(3):buffers.add(card("100 bytes",.0+j*2.3,.65,2.0,.85,BLUE if j<2 else TEAL,23))
        g.add(buffers,label("200 bytes outstanding",1.15,-.25,23,BLUE),
              label("100 bytes left",4.6,-.25,21,TEAL),
              card("ACKs and window updates change the send budget",2.3,-1.45,7.2,.75,GOLD,21))
        reveal(scene,g);pulse(scene,buffers[2],TEAL);pulse(scene,g[4],GOLD)
        return g
    if mode=="bytestream":
        g.add(label("TCP IS AN ORDERED BYTE STREAM",2.3,1.9,20,MUTED))
        writes=v.get("writes",["HEL","LO","!"])
        for j,txt in enumerate(writes):
            g.add(card("Write: "+txt,.0,1-j*.9,2.3,.65,BLUE,21))
        g.add(arrow((1.3,.3),(3,.3),TEAL),card("Read: HELLO!",4.7,.3,2.7,1.05,TEAL,24),
              label("Reads may split or combine writes",2.3,-1.8,22,GOLD,7.6))
        reveal(scene,g);travel(scene,g,(1.4,.3),(3.0,.3),"BYTES",BLUE);pulse(scene,g[-2],TEAL)
        return g
    if "ports" in v:
        g.add(label("PORTS IDENTIFY TRANSPORT ENDPOINTS",2.3,1.9,19,MUTED,7.7),
              card("Client",-.25,.7,2.6,.8,BLUE,26),card("Server",4.75,.7,2.6,.8,TEAL,26),
              label("port 49152",-.25,-.1,24,BLUE),label("port 80",4.75,-.1,24,TEAL),
              arrow((1.2,.7),(3.3,.7),GOLD),
              label("Example application endpoints",2.3,-1.5,22,MUTED))
        reveal(scene,g);travel(scene,g,(1.2,.0),(3.3,.0),"DATA",GOLD)
        return g
    if "datagrams" in v:
        datagrams=v["datagrams"]
        g.add(label("UDP PRESERVES DATAGRAM BOUNDARIES",2.3,1.9,19,MUTED,7.7),
              card("Sender",-.65,1.0,1.55,.65,BLUE),card("Receiver",5.25,1.0,1.75,.65,TEAL))
        for j,name in enumerate(datagrams):
            y=.4-j*.75
            if v.get("lost")==j:
                g.add(arrow((-.65,y),(2.3,y),RED),cross(2.3,y),label(name,3.5,y,20,RED))
            else:
                g.add(arrow((-.65,y),(5.25,y),COLORS[j]),label(name,2.3,y+.18,18,COLORS[j]))
        g.add(label("The application decides whether late or lost data needs recovery",2.3,-2.15,18,MUTED,7.7))
        reveal(scene,g)
        for j,name in enumerate(datagrams):
            if v.get("lost")!=j:travel(scene,g,(-.65,.4-j*.75),(5.25,.4-j*.75),name,COLORS[j],.65)
        return g
    if "application_features" in v:
        g.add(label("APPLICATION PROTOCOLS CAN ADD FEATURES",2.3,1.9,19,MUTED,7.7))
        for j,(txt,color) in enumerate((("ACK + retransmission",BLUE),("Congestion control",TEAL),("Encryption",GOLD))):
            g.add(card(txt,2.3,1-j*1.05,6.7,.7,color,25))
        g.add(label("UDP itself does not provide these guarantees",2.3,-2.15,20,MUTED,7.6))
        reveal(scene,g)
        for j in (1,2,3):pulse(scene,g[j],COLORS[j-1],.5)
        return g
    g.add(label("SAME DATA • DIFFERENT TRANSPORT SERVICE",2.3,1.9,19,MUTED,7.8))
    for name,color,y in (("TCP",BLUE,.8),("UDP",GOLD,-.65)):
        g.add(card(name,-.65,y,1.1,.65,color,25),segment((.0,y),(5.6,y),MUTED,2))
        for k in range(3):g.add(card(str(k+1),1.0+k*1.25,y,.75,.52,color,21))
    g.add(label("Latency depends on the application and the network" if v.get("latency_caveat") else "TCP: built-in reliability • UDP: application chooses",2.3,-1.85,20,MUTED,7.6))
    reveal(scene,g)
    travel(scene,g,(1,.8),(5.6,.8),"BYTES",BLUE)
    travel(scene,g,(1,-.65),(5.6,-.65),"MSG",GOLD)
    return g


def key_icon(x,y,color=GOLD):
    return m.VGroup(m.Circle(radius=.16,color=color,stroke_width=3).move_to([x-.18,y,0]),
                    segment((x,y),(x+.4,y),color,3),segment((x+.22,y),(x+.22,y-.12),color,3),
                    segment((x+.37,y),(x+.37,y-.12),color,3))


def crypto(scene,i,section):
    g=m.VGroup()
    v=section.get("visual",{})
    mode=v.get("mode", "hybrid")

    def deliver(a,b,text,color,duration=.7):
        packet=travel(scene,g,a,b,text,color,duration)
        scene.play(m.FadeOut(packet),run_time=.2)
        scene.remove(packet)
        g.remove(packet)

    if mode=="symmetric" and i==0:
        g.add(card("Alice",-.65,.6,1.6,.85,BLUE),card("Public network",2.3,.6,3.1,.85,VIOLET,21),card("Bob",5.25,.6,1.6,.85,TEAL),
              arrow((.2,.6),(.7,.6),BLUE),arrow((3.9,.6),(4.4,.6),TEAL),
              card("Eve observes",2.3,-1.1,2.8,.7,RED),segment((2.3,.1),(2.3,-.7),RED,2),
              label("MEET AT NINE: visible if sent as plaintext",2.3,-2.15,20,MUTED,7.7))
        reveal(scene,g);deliver((-.65,-.15),(5.25,-.15),"MESSAGE",BLUE);pulse(scene,g[5],RED)
        return g
    if mode=="symmetric":
        ciphertext="8F 31 A9 7C" if i==1 else "Ciphertext"
        g.add(label("SYMMETRIC ENCRYPTION",2.3,1.9,21,MUTED),card("Plaintext",-.45,.35,1.8,.85,BLUE),
              card("Encrypt",2.0,.35,1.65,.85,GOLD),card(ciphertext,4.8,.35,2.1,.85,VIOLET,20),
              arrow((.5,.35),(1.08,.35),BLUE),arrow((2.9,.35),(3.65,.35),VIOLET),
              key_icon(2,1.1),label("K",2.6,1.1,23,GOLD))
        caption="Same secret key for encryption and decryption"
        if v.get("leaked"):caption="If the secret key leaks, the observer can decrypt"
        if v.get("random_key"):caption="Generate keys with cryptographic randomness"
        if v.get("algorithm_public"):caption="Protect the key; the algorithm may be public"
        g.add(label(caption,2.3,-1.1,21,RED if v.get("leaked") else TEAL,7.6),
              label("Illustrative ciphertext — not a working cipher" if i==1 else "Encryption is only one part of secure communication",2.3,-1.9,19,MUTED,7.6))
        reveal(scene,g);deliver((.4,.35),(1.1,.35),"DATA",BLUE);pulse(scene,g[6],GOLD)
        return g
    if mode=="publickey":
        g.add(label("BOB'S PUBLIC / PRIVATE KEY PAIR",2.3,1.9,20,MUTED,7.7),
              card("Public key PK_B",-.25,1.0,2.8,.65,TEAL),card("Private key SK_B",4.6,1.0,2.8,.65,GOLD),
              key_icon(-.25,.3,TEAL),key_icon(4.6,.3,GOLD),
              card("Anyone encrypts",-.25,-.65,2.65,.75,TEAL,21),card("Only Bob decrypts",4.6,-.65,3.0,.75,GOLD,21),
              arrow((1.25,-.65),(2.9,-.65),VIOLET),
              label("Public keys must still be authenticated",2.3,-1.95,22,RED,7.6))
        reveal(scene,g)
        pulse(scene,g[2] if v.get("decrypt") else g[1],GOLD if v.get("decrypt") else TEAL)
        pulse(scene,g[6] if v.get("decrypt") else g[5],GOLD if v.get("decrypt") else TEAL)
        return g
    if mode=="hybrid":
        g.add(label("SIMPLIFIED HYBRID ENCRYPTION",2.3,1.95,20,MUTED),
              card("Random session key K",-.2,1.0,2.9,.67,GOLD,20),
              card("Protect K using PK_B",4.35,1.0,3.3,.67,TEAL,20),
              arrow((1.3,1),(2.55,1),GOLD),
              card("Message data",-.2,-.45,2.9,.85,BLUE,22),
              card("Ciphertext + auth tag",4.35,-.45,3.3,.85,VIOLET,21),
              arrow((1.3,-.45),(2.55,-.45),BLUE))
        step=int(v.get("step",0))
        captions={0:"Use public-key operations for a small key; symmetric crypto for bulk data",1:"Generate fresh K with a cryptographic random generator",2:"Use K with authenticated encryption to protect the message",3:"Protect K for Bob using his authenticated public key",4:"Send protected K and the authenticated ciphertext",5:"Bob uses SK_B to recover K, then verifies and decrypts data"}
        g.add(label(captions[step],2.3,-1.65,19,WHITE,7.7),
              label("Conceptual model — not the TLS 1.3 key exchange",2.3,-2.25,18,MUTED,7.7))
        reveal(scene,g)
        if step in (0,1,3,4,5):deliver((1.4,1),(2.5,1),"KEY",GOLD,.7)
        if step in (0,2,4,5):deliver((1.4,-.45),(2.5,-.45),"DATA",BLUE,.7)
        pulse(scene,g[1] if step==1 else g[2] if step==3 else g[5],GOLD if step==1 else TEAL)
        return g
    if v.get("nonce"):
        g.add(label("FOLLOW THE ALGORITHM'S NONCE RULES",2.3,1.9,20,MUTED,7.7),
              card("Key K + nonce N₁",2.3,.95,6.8,.7,BLUE,25),
              card("Key K + nonce N₂",2.3,-.05,6.8,.7,TEAL,25),
              label("A nonce is not another secret key",2.3,-1.1,23,GOLD,7.7),
              label("For schemes requiring uniqueness: never repeat (K, nonce)",2.3,-2.1,19,RED,7.7))
        reveal(scene,g);pulse(scene,g[1],BLUE);pulse(scene,g[2],TEAL)
        return g
    if v.get("key_substitution"):
        g.add(label("WHO DOES THIS PUBLIC KEY BELONG TO?",2.3,1.9,20,MUTED,7.7),
              card("Bob's verified PK_B",2.3,.95,6.8,.75,TEAL,25),
              card("Eve's substituted public key",2.3,-.1,6.8,.75,RED,25),
              label("Encrypting to Eve's key lets Eve decrypt",2.3,-1.1,22,RED,7.7),
              label("Bind keys to identities using an authenticated mechanism",2.3,-2.05,19,MUTED,7.7))
        reveal(scene,g);pulse(scene,g[2],RED);pulse(scene,g[1],TEAL)
        return g
    if v.get("tamper"):
        g.add(label("AUTHENTICATED DECRYPTION",2.3,1.9,21,MUTED),
              card("Ciphertext + tag",-.25,.75,2.8,.85,VIOLET,22),
              card("Verify with key K",4.65,.75,2.8,.85,GOLD,22),
              arrow((1.3,.75),(3.15,.75),RED),
              card("Changed data → verification fails",2.3,-.65,6.8,.85,RED,25),
              label("Reject the modified message; do not trust its plaintext",2.3,-1.95,20,MUTED,7.7))
        reveal(scene,g);deliver((1.4,.75),(3.0,.75),"ALTERED",RED,.7);pulse(scene,g[4],RED)
        return g
    g.add(label("CONFIDENTIALITY ≠ AUTHENTICATION",2.3,1.9,20,MUTED,7.7))
    for j,(title,desc,color) in enumerate((("Privacy","Who can read?",BLUE),("Integrity","Was it changed?",TEAL),("Authentication","Who sent it?",GOLD))):
        x=.0+j*2.3
        g.add(card(title,x,.7,2.15,.8,color,22),label(desc,x,-.3,19,color,2.2))
    g.add(card("Use established protocols and vetted cryptographic libraries" if v.get("established_protocol") else "Encryption to Bob does not identify Alice as the sender",2.3,-1.5,7.4,.7,VIOLET,20))
    reveal(scene,g);pulse(scene,g[0],BLUE);pulse(scene,g[-1],VIOLET)
    return g


RENDERERS={"01":website,"02":multiplex,"03":reliability,"04":channel,"05":routing,"06":subnet,"07":tcp_udp,"08":crypto}


def animate_visual(scene: m.Scene, episode_id: str, index: int, section: dict) -> m.VGroup:
    """Draw and animate one section; caller owns its remaining narration hold time."""
    episode=str(episode_id).zfill(2)
    if episode not in RENDERERS:
        raise ValueError(f"Unknown networking episode: {episode_id}")
    if not 0<=index<24:
        raise ValueError(f"Section index must be 0–23, got {index}")
    group=RENDERERS[episode](scene,index,section)
    # Diagrams use an intentionally bounded stage; this catches accidental layout drift.
    if group.width>8.7 or group.height>4.85:
        raise ValueError(f"Diagram escaped its stage: episode {episode}, section {index+1}: {group.width:.2f} × {group.height:.2f}")
    return group
