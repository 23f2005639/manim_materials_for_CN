"""Shared framing and narration timing; topic diagrams live in visuals.py."""
from __future__ import annotations

import json
import os
import textwrap
from pathlib import Path

import manimgx as m

from networks.visuals import animate_visual

m.config.background_color = "#07111F"
m.config.frame_rate = 30

WHITE = "#EDF4FF"
MUTED = "#93A9C4"
ACCENT = "#64D8EB"


def label(text: str, size: int = 22, color: str = WHITE, width: float | None = None) -> m.Text:
    obj = m.Text(text, font="Noto Sans", font_size=size, color=color)
    if width and obj.width > width:
        obj.scale(width / obj.width)
    return obj


class LessonScene(m.Scene):
    storyboard_path: Path

    def construct(self) -> None:
        data = json.loads(self.storyboard_path.read_text())
        previous = None
        motion_ends = []
        limit = int(os.environ.get("NETWORKS_SECTION_LIMIT", "0"))
        target = 0.0
        fps = float(m.config.frame_rate)
        for index, section in enumerate(data["sections"]):
            if limit and index >= limit:
                break
            self.next_section(section["title"], notes=section["narration"])
            if previous is not None:
                self.play(m.FadeOut(previous), run_time=0.25)
                self.remove(previous)

            series = label(f"NETWORKS / {data['id']}     •     {section['chapter'].upper()}", 16, ACCENT)
            series.move_to([-6.45 + series.width / 2, 3.58, 0])
            heading = label(section["title"], 32, width=12.7)
            heading.move_to([-6.45 + heading.width / 2, 2.99, 0])
            divider = m.Line([-6.45, 2.51, 0], [6.45, 2.51, 0], color="#233951", stroke_width=1)

            card = m.RoundedRectangle(width=8.35, height=4.65, corner_radius=0.13,
                                      color="#243B55", fill_color="#0C1B2D", fill_opacity=1,
                                      stroke_width=1).move_to([2.35, -0.13, 0])
            number = label(f"{index + 1:02d} / {len(data['sections']):02d}", 18, MUTED).move_to([-5.08, 1.92, 0])
            concept = label(textwrap.fill(section["visual"].get("label", section["chapter"]), 19),
                            27, WHITE, 3.5).move_to([-4.65, 1.12, 0])
            points = m.VGroup()
            for j, bullet in enumerate(section["bullets"][:3]):
                text = label(textwrap.fill(bullet, 25), 21, MUTED, 3.55)
                text.move_to([-6.25 + text.width / 2, -0.05 - j * 0.75, 0])
                points.add(text)
            note = label("YOUR PACE. YOUR EXPLANATION.", 17, MUTED, 3.6).move_to([-4.65, -2.15, 0])
            takeaway_box = m.RoundedRectangle(width=12.9, height=0.65, corner_radius=0.1,
                                              color="#153C47", fill_color="#102D38",
                                              fill_opacity=1, stroke_width=1).move_to([0, -3.08, 0])
            takeaway = label(section["takeaway"], 20, WHITE, 12.15).move_to([0, -3.08, 0])
            bars = m.VGroup(*[
                m.Line([-6.45 + j * 12.9 / 24, -3.66, 0],
                       [-6.45 + (j + 0.82) * 12.9 / 24, -3.66, 0],
                       color=ACCENT if j <= index else "#26374C", stroke_width=3)
                for j in range(24)
            ])
            chrome = m.VGroup(series, heading, divider, card, number, concept, points,
                              note, takeaway_box, takeaway, bars)
            self.play(m.FadeIn(chrome), run_time=0.45)
            visual = animate_visual(self, data["id"], index, section)
            previous = m.Group(chrome, visual)
            motion_ends.append({"name": section["title"], "animation_end_frame": round(self.time * fps)})
            target += float(section["duration"])
            # Round the cumulative target, rather than each section, to avoid drift.
            end = round(target * fps) / fps
            remaining = end - self.time
            if remaining < 0:
                raise ValueError(f"Section {section['id']} exceeded its time by {-remaining:.2f}s")
            self.wait(remaining)
        self.storyboard_path.with_name("animation-timing.json").write_text(json.dumps({
            "fps": fps, "sections": motion_ends, "duration": self.time,
        }, indent=2) + "\n")
