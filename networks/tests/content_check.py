"""Run with: python3 networks/tests/content_check.py"""
import ipaddress
import heapq
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from build import read, timeline


def main():
    paths = sorted((ROOT / "episodes").glob("*/storyboard.json"))
    assert len(paths) == 8, f"Expected 8 complete lessons, found {len(paths)}"
    total_words = 0
    for path in paths:
        data = read(path)
        deck = timeline(data)
        words = sum(len(s["narration"].split()) for s in data["sections"])
        total_words += words
        assert 500 <= words <= 900, (data["id"], words)
        for section in data["sections"]:
            assert 20 <= len(section["narration"].split()) <= 38, section["id"]
            assert len(section["short_title"].split()) <= 6
        assert all(deck["sections"][i]["frame"] < deck["sections"][i+1]["frame"] for i in range(23))
        assert deck["frames"] == round(data["duration"] * 30)
        assert len(data["sources"]) >= 2
        assert all(s["url"].startswith("https://") for s in data["sources"])
        assert not any(x in json.dumps(data).lower() for x in ("todo", "lorem ipsum", "insert narration"))
        for a, b, _ in deck["captions"]:
            assert 0 <= a < b <= data["duration"] + .04
        print(f"{data['id']}:24sections,{words}words,{data['duration']/60:.2f}min")
    subnets = list(ipaddress.ip_network("192.168.1.0/24").subnets(new_prefix=26))
    assert [str(s.network_address) for s in subnets] == [f"192.168.1.{n}" for n in (0,64,128,192)]
    assert [str(s.broadcast_address) for s in subnets] == [f"192.168.1.{n}" for n in (63,127,191,255)]
    assert all(len(list(s.hosts())) == 62 for s in subnets)
    routing = read(ROOT / "episodes/05-routing/storyboard.json")
    edges = next(s["visual"]["edges"] for s in routing["sections"] if "edges" in s["visual"])
    def shortest(failed=None):
        graph = {}
        for a, b, cost in edges:
            if failed and {a, b} == set(failed):
                continue
            assert cost > 0
            graph.setdefault(a, []).append((b, cost))
            graph.setdefault(b, []).append((a, cost))
        distance = {"A": 0}
        queue = [(0, "A")]
        while queue:
            d, node = heapq.heappop(queue)
            if d != distance[node]:
                continue
            for neighbor, cost in graph[node]:
                new = d + cost
                if new < distance.get(neighbor, float("inf")):
                    distance[neighbor] = new
                    heapq.heappush(queue, (new, neighbor))
        return distance
    assert shortest() == {"A": 0, "B": 3, "C": 2, "D": 8, "E": 10, "F": 13}
    assert shortest(("D", "E"))["F"] == 14
    print(f"PASS:8lessons,192sections,{total_words}narrationwords; subnet example independently checked")


if __name__ == "__main__":
    main()
