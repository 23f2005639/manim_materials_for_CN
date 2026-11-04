"""Check measured native motion and the shortened visual-edition scripts."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    reports = []
    for folder in sorted((ROOT / "episodes").iterdir()):
        if not (folder / "storyboard.json").exists():
            continue
        data = json.loads((folder / "storyboard.json").read_text())
        previous = json.loads((ROOT / "archive/first-edition" / folder.name / "storyboard.json").read_text())
        current_words = sum(len(s["narration"].split()) for s in data["sections"])
        old_words = sum(len(s["narration"].split()) for s in previous["sections"])
        assert current_words <= old_words * .75
        timing = json.loads((folder / "animation-timing.json").read_text())
        measured = json.loads((folder / "motion-verification.json").read_text())
        assert timing["edition"] == "visual" and len(timing["sections"]) == 24
        assert measured["native_changing_frame_fraction"] >= .6
        assert min(s["visual_fraction"] for s in timing["sections"]) >= .65
        assert max(s["section_seconds"] - s["visual_seconds"] for s in timing["sections"]) < 2
        reports.append({"episode": data["id"], "script_reduction_percent": round(100*(1-current_words/old_words),1),
                        "native_changing_frame_fraction": measured["native_changing_frame_fraction"]})
        print(data["id"], reports[-1], flush=True)
    assert len(reports) == 8
    (ROOT / "motion-series-verification.json").write_text(json.dumps(reports, indent=2) + "\n")


if __name__ == "__main__":
    main()
