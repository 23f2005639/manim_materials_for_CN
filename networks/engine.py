"""A minimal frame around persistent visual explanations."""
from __future__ import annotations

import json
import os
from pathlib import Path

import manimgx as m

m.config.background_color = "#080A10"
m.config.frame_rate = 30


class LessonScene(m.Scene):
    storyboard_path: Path

    def construct(self) -> None:
        # Import only the selected director so topics can be authored independently.
        data = json.loads(self.storyboard_path.read_text())
        if data.get("edition") == "focused-v2":
            from networks.focused import construct
            construct(self, data)
            return
        if data["id"] in ("01", "03", "07"):
            from networks.motion.packets import PacketDirector
            director = PacketDirector(self, data["id"])
        elif data["id"] in ("02", "04"):
            from networks.motion.channels import ChannelDirector
            director = ChannelDirector(self, data["id"])
        else:
            from networks.motion.systems import SystemsDirector
            director = SystemsDirector(self, data["id"])

        title = None
        motion = []
        target = 0.0
        fps = float(m.config.frame_rate)
        limit = int(os.environ.get("NETWORKS_SECTION_LIMIT", "0"))
        for index, section in enumerate(data["sections"]):
            if limit and index >= limit:
                break
            start = self.time
            self.next_section(section["title"], notes=section["narration"])
            words = section.get("short_title", section["title"])
            heading = m.Text(words, font="Noto Sans", font_size=35, color="#F2F2F2")
            if heading.width > 12.5:
                heading.scale(12.5 / heading.width)
            heading.move_to([0, 3.27, 0])
            if title is None:
                title = heading
                self.play(m.FadeIn(title, shift=0.12 * m.UP), run_time=0.45)
            else:
                self.play(m.Transform(title, heading), run_time=0.4)

            target += float(section["duration"])
            end = round(target * fps) / fps
            budget = end - self.time - 0.75
            if budget <= 0:
                raise ValueError(f"No animation time remains for {section['id']}")
            began = self.time
            director.animate(index, section, budget)
            elapsed = self.time - began
            if elapsed < budget * 0.65:
                raise ValueError(f"{section['id']}: only {elapsed:.1f}s of {budget:.1f}s used for its visual explanation")
            remaining = end - self.time
            if remaining < -0.02:
                raise ValueError(f"{section['id']} exceeds its timing by {-remaining:.2f}s")
            motion.append({"name": section["title"], "animation_end_frame": round(self.time * fps),
                           "section_seconds": round(end - start, 3), "visual_seconds": round(elapsed, 3),
                           "visual_fraction": round(elapsed / (end - start), 3)})
            if remaining > 0:
                self.wait(remaining)

        self.storyboard_path.with_name("animation-timing.json").write_text(json.dumps({
            "fps": fps, "sections": motion, "duration": self.time, "edition": "visual",
        }, indent=2) + "\n")
