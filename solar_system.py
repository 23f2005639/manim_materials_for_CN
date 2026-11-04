"""A 30-second, textured 3D orrery for ManimGX.

Run: manimgx inspect solar_system.py
     manimgx render solar_system.py -r 1920x1080 --fps 30
All textures are generated locally. Orbits, scale and speeds are illustrative.
"""

import math

import manimgx as m
import numpy as np


m.config.background_color = "#030812"

# name, orbital radius, visible radius, color, visual period, phase, inclination
PLANETS = [
    ("Mercury", 1.03, 0.075, "#A6A09A", 4.0, 0.3, 7.0),
    ("Venus", 1.49, 0.12, "#E8BD78", 5.8, 2.2, 3.4),
    ("Earth", 2.02, 0.135, "#46A9EE", 8.0, 4.3, 0.0),
    ("Mars", 2.55, 0.10, "#D96B47", 10.2, 5.5, 1.9),
    ("Jupiter", 3.53, 0.33, "#DBB190", 14.0, 0.8, 1.3),
    ("Saturn", 4.55, 0.28, "#E8D19B", 18.0, 3.5, 2.5),
    ("Uranus", 5.49, 0.205, "#8AD9DD", 23.0, 5.1, 0.8),
    ("Neptune", 6.23, 0.20, "#527FEA", 28.0, 2.0, 1.8),
]


def texture(name: str, color: str) -> np.ndarray:
    """Stylized seamless planet maps, rather than externally sourced imagery."""
    u, v = np.meshgrid(np.linspace(0, 2 * np.pi, 512), np.linspace(0, np.pi, 256))
    detail = np.sin(17 * u + 5 * np.sin(7 * v)) * np.sin(23 * v - 3 * np.sin(4 * u))
    broad = np.sin(3 * u + 1.8 * np.sin(4 * v)) + 0.5 * np.cos(7 * u - 5 * v)
    base = np.array([int(color[i:i + 2], 16) for i in (1, 3, 5)])
    rgb = np.broadcast_to(base, (*u.shape, 3)).astype(float).copy()
    rgb *= (0.91 + 0.07 * detail + 0.07 * broad)[..., None]
    if name == "Earth":
        land = (broad + 0.3 * np.sin(11 * u + 8 * v) > 0.42) & (np.sin(v) > 0.3)
        rgb[land] = [67, 139, 98]
        ice = np.abs(np.cos(v)) > 0.94
        rgb[ice] = [218, 239, 245]
        clouds = np.clip((np.sin(9 * u + 6 * np.sin(3 * v)) + np.cos(14 * v - u) - 1.25) * 0.5, 0, 0.55)
        rgb = rgb * (1 - clouds[..., None]) + 245 * clouds[..., None]
    elif name in ("Jupiter", "Saturn"):
        bands = np.sin(24 * v + 0.6 * np.sin(5 * u) * np.sin(v))
        rgb *= (0.86 + 0.17 * bands)[..., None]
        if name == "Jupiter":
            spot = ((u - 4.3) / 0.32) ** 2 + ((v - 1.92) / 0.13) ** 2 < 1
            rgb[spot] = [172, 91, 65]
    elif name == "Sun":
        rgb *= (0.9 + 0.16 * np.sin(31 * u + 10 * np.sin(11 * v)) * np.sin(39 * v))[..., None]
    rgba = np.full((*u.shape, 4), 255, dtype=np.uint8)
    rgba[..., :3] = np.clip(rgb, 0, 255).astype(np.uint8)
    return rgba


def globe(name: str, radius: float, color: str) -> m.MeshMobject:
    nu, nv = 64, 32
    u, v = np.meshgrid(np.linspace(0, 2 * np.pi, nu + 1), np.linspace(0, np.pi, nv + 1))
    vertices = radius * np.column_stack((
        (np.sin(v) * np.cos(u)).ravel(),
        (np.sin(v) * np.sin(u)).ravel(),
        np.cos(v).ravel(),
    ))
    uv = np.column_stack((u.ravel() / (2 * np.pi), v.ravel() / np.pi))
    triangles = []
    for j in range(nv):
        for i in range(nu):
            a = j * (nu + 1) + i
            b = a + nu + 1
            triangles.extend(((a, b, a + 1), (a + 1, b, b + 1)))
    body = m.MeshMobject(
        vertices, np.array(triangles), uvs=uv, texture=texture(name, color),
        fill_opacity=1, stroke_width=0, shade_in_3d=name != "Sun",
    )
    if name != "Sun":
        body.set_material(m.Material(roughness=0.83, reflectance=0.22))
    return body


def orbital_point(radius: float, angle: float, inclination: float) -> np.ndarray:
    inc = math.radians(inclination)
    return np.array((radius * math.cos(angle), radius * math.sin(angle) * math.cos(inc),
                     radius * math.sin(angle) * math.sin(inc)))


class SolarSystem(m.ThreeDScene):
    def construct(self) -> None:
        self.set_camera_orientation(phi=62 * m.DEGREES, theta=-85 * m.DEGREES,
                                    zoom=0.82, focal_distance=28)
        self.add(m.AmbientLight(intensity=0.36),
                 m.PointLight(m.ORIGIN, color="#FFF1D1", intensity=24, radius=24))

        # A screen-fixed star field sits behind the depth-tested solar system.
        rng = np.random.default_rng(41)
        stars = m.VGroup(*[
            m.Dot([rng.uniform(-7, 7), rng.uniform(-3.9, 3.9), 0],
                  radius=rng.uniform(0.006, 0.016), color="#A6BCD5",
                  fill_opacity=rng.uniform(0.16, 0.65), stroke_width=0)
            for _ in range(155)
        ])
        self.add_fixed_in_frame_mobjects(stars)

        title = m.Text("THE SOLAR SYSTEM", font_size=35, color="#F0F5FF").move_to([0, 3.45, 0])
        subtitle = m.Text("Eight worlds. One star. Always in motion.", font_size=18,
                          color="#8FA5C1").move_to([0, 2.99, 0])
        footer = m.Text("Illustrative orbits • sizes, distances and speeds adjusted for visibility",
                        font_size=14, color="#8393AB").move_to([0, -3.65, 0])
        self.add_fixed_in_frame_mobjects(title, subtitle, footer)

        legend = m.VGroup()
        for i, (name, _, _, color, *_) in enumerate(PLANETS):
            x = -5.3 + (i % 4) * 3.35
            y = -2.9 - (i // 4) * 0.35
            dot = m.Dot([x, y, 0], radius=0.045, color=color, stroke_width=0)
            label = m.Text(name, font_size=17, color="#C9D5E6").next_to(dot, m.RIGHT, buff=0.13)
            legend.add(dot, label)
        self.add_fixed_in_frame_mobjects(legend)

        sun = globe("Sun", 0.48, "#FFD153")
        corona = m.VGroup(*[
            m.Circle(radius=0.51 + 0.025 * i, color="#FFAC42",
                     stroke_width=2.2, stroke_opacity=0.23 * (1 - i / 12))
            for i in range(12)
        ])
        self.play(m.FadeIn(sun), m.FadeIn(corona), run_time=1.2)

        clock = m.ValueTracker(0)
        self.add(clock)
        orbits = m.VGroup()
        worlds = m.Group()
        bodies = {}
        for name, radius, size, color, period, phase, inc in PLANETS:
            orbit = m.Circle(radius=radius, color=color, stroke_width=0.8,
                             stroke_opacity=0.26).rotate(inc * m.DEGREES, axis=m.RIGHT)
            orbits.add(orbit)
            body = globe(name, size, color)
            world = m.Group(body)
            if name == "Saturn":
                for inner, outer, ring_color in ((0.37, 0.45, "#B49B70"),
                                                  (0.46, 0.55, "#D7C391"),
                                                  (0.57, 0.64, "#9E8B6B")):
                    ring = m.Annulus(inner_radius=inner, outer_radius=outer,
                                     color=ring_color, fill_opacity=0.88, stroke_width=0)
                    ring.rotate(27 * m.DEGREES, axis=m.RIGHT)
                    world.add(ring)
            world.move_to(orbital_point(radius, phase, inc))

            # Absolute tracker time controls the orbits at every output frame.
            def follow(mob: m.Mobject, r=radius, p=period, a=phase, tilt=inc) -> None:
                mob.move_to(orbital_point(r, a + m.TAU * clock.get_value() / p, tilt))

            world.add_updater(follow)
            worlds.add(world)
            bodies[name] = world

        belt = m.VGroup(*[
            m.Dot(orbital_point(rng.uniform(2.95, 3.14), rng.uniform(0, m.TAU), 0),
                  radius=rng.uniform(0.006, 0.015), color="#8D8B83",
                  fill_opacity=0.5, stroke_width=0)
            for _ in range(165)
        ])
        self.play(m.LaggedStart(*[m.Create(o) for o in orbits], lag_ratio=0.07),
                  m.FadeIn(belt), run_time=1.6)
        self.play(m.LaggedStart(*[m.FadeIn(w) for w in worlds], lag_ratio=0.1), run_time=1.8)

        moon = globe("Moon", 0.038, "#CBCBD0")

        def lunar_orbit(mob: m.Mobject) -> None:
            angle = clock.get_value() * 2.4
            mob.move_to(bodies["Earth"].get_center() + orbital_point(0.25, angle, 16))

        moon.add_updater(lunar_orbit)
        lunar_orbit(moon)
        self.add(moon)

        self.move_camera(phi=68 * m.DEGREES, theta=-35 * m.DEGREES,
                         added_anims=[clock.animate.set_value(10)],
                         run_time=10, rate_func=m.linear)
        self.move_camera(phi=48 * m.DEGREES, theta=10 * m.DEGREES, zoom=0.73,
                         added_anims=[clock.animate.set_value(20)],
                         run_time=10, rate_func=m.linear)
        self.move_camera(phi=62 * m.DEGREES, theta=30 * m.DEGREES, zoom=0.82,
                         added_anims=[clock.animate.set_value(24)],
                         run_time=4, rate_func=m.linear)
        self.wait(1.4)
