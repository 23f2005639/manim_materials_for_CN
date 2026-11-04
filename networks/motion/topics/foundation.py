"""Concrete opening objects, before the abstract networking diagrams."""
from .common import *


def computer(label, x, y=0, color=BLUE):
    screen=m.RoundedRectangle(width=1.65,height=1.05,corner_radius=.1,color=color,
                              fill_color=BG,fill_opacity=1).move_to([x,y,0])
    stand=line((x,y-.53),(x,y-.85),color,3)
    foot=line((x-.65,y-.85),(x+.65,y-.85),color,3)
    return m.VGroup(screen,stand,foot,text(label,x,y+1,25,color,3.6))


def photo(x=0,y=0):
    return m.VGroup(m.Rectangle(width=.95,height=.65,color=BLUE,fill_color=BG,fill_opacity=1),
                   m.Polygon([-.38,-.23,0],[-.08,.1,0],[.15,-.23,0],color=GREEN,fill_opacity=.6),
                   m.Dot([.26,.17,0],radius=.08,color=YELLOW)).move_to([x,y,0]).set_z_index(6)


def fiber_intro(d):
    """A real 3D strand and pulse, then a flat readable view for the hold."""
    s=d.s
    s.set_camera_orientation(phi=65*m.DEGREES,theta=-72*m.DEGREES,zoom=.9,focal_distance=30)
    strand=d.own(m.Cylinder(radius=.38,height=9,direction=m.RIGHT,show_ends=False,
                            resolution=(8,24),checkerboard_colors=[BLUE,BLUE],
                            fill_opacity=.16,stroke_width=0))
    rings=d.own(m.VGroup(*[m.Circle(radius=.38,color=BLUE,stroke_width=2)
                     .rotate(m.PI/2,axis=m.UP).move_to([x,0,0]) for x in (-4.5,4.5)]))
    d.play(m.FadeIn(strand),m.Create(rings),run_time=1.5)
    label=d.own(text('A glass fiber carries light',0,-2,30,WHITE))
    s.camera.add_fixed_in_frame_mobjects(label)
    d.play(m.FadeIn(label),run_time=.7)
    pulse=d.own(m.Sphere(radius=.19,resolution=(12,16),checkerboard_colors=[YELLOW,YELLOW],
                        fill_opacity=1,stroke_width=0).move_to([-4.5,0,0]))
    d.play(m.FadeIn(pulse),run_time=.4)
    d.play(pulse.animate.move_to([4.5,0,0]),s.camera.theta_tracker.animate.set_value(-100*m.DEGREES),run_time=4,rate_func=m.linear)
    d.play(m.FadeOut(pulse),run_time=.4)
    d.play(s.camera.phi_tracker.animate.set_value(0),s.camera.theta_tracker.animate.set_value(-m.PI/2),
           s.camera.zoom_tracker.animate.set_value(1),run_time=2)
    note=d.own(text('One change sent → one change detected',0,1.8,27,GREEN))
    d.play(m.FadeIn(note),run_time=.7)
    # A front view leaves the strand easy to connect to the next flat diagram.
    d.play(m.FadeIn(pulse.move_to([-4.5,0,0])),run_time=.3)
    d.play(pulse.animate.move_to([4.5,0,0]),run_time=2.5,rate_func=m.linear)
    s.set_camera_orientation(focal_distance=20)
