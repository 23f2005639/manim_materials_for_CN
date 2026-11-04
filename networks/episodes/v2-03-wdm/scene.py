from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from networks.engine import Lesson3DScene as LessonScene

class Episode(LessonScene):
    storyboard_path = Path(__file__).with_name("storyboard.json")
