"""Run with: python3 networks/tests/content_check.py"""
import ipaddress
import heapq
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from build import read, timeline, episode_paths


def main():
    paths = episode_paths()
    assert len(paths) == 8, f"Expected 8 complete lessons, found {len(paths)}"
    assert [read(p)["topic"] for p in paths] == ['dns','bufferbloat','wdm','packet-switching','dijkstra','subnetting','tcp-slow-start','rsa']
    assert len({read(p)["id"] for p in paths}) == 8
    total_words = 0
    for path in paths:
        data = read(path)
        deck = timeline(data)
        words = sum(len(s["narration"].split()) for s in data["sections"])
        total_words += words
        assert 1100 <= words <= 1250, (data["id"], words)
        for section in data["sections"]:
            assert len(section["narration"].split()) >= 40, section["id"]
            assert len(section["short_title"].split()) <= 6
        assert all(deck["sections"][i]["frame"] < deck["sections"][i+1]["frame"] for i in range(len(deck["sections"])-1))
        assert deck["frames"] == round(data["duration"] * 30)
        assert len(data["sources"]) >= 2
        assert all(s["url"].startswith("https://") for s in data["sources"])
        assert not any(x in json.dumps(data).lower() for x in ("todo", "lorem ipsum", "insert narration"))
        for a, b, _ in deck["captions"]:
            assert 0 <= a < b <= data["duration"] + .04
        print(f"{data['id']}:{len(data['sections'])}phases,{words}words,{data['duration']/60:.2f}min")
    subnets = list(ipaddress.ip_network("192.168.1.0/24").subnets(new_prefix=26))
    assert [str(s.network_address) for s in subnets] == [f"192.168.1.{n}" for n in (0,64,128,192)]
    assert [str(s.broadcast_address) for s in subnets] == [f"192.168.1.{n}" for n in (63,127,191,255)]
    assert all(len(list(s.hosts())) == 62 for s in subnets)
    routing = next(read(p) for p in paths if read(p)["topic"] == "dijkstra")
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
    assert 1_000_000*8/20_000_000 == .4
    assert abs((4+3-1)*1500*8/10_000_000 - .0072) < 1e-10
    assert pow(7,3,55) == 13 and pow(13,27,55) == 7
    assert (3*27-1) % 40 == 0
    assert sum((2,20,30,40)) == 92 and 92/2 == 46
    print(f"PASS:8 focused lessons,{sum(len(read(p)['sections']) for p in paths)}phases,{total_words}narration words; independent graph/subnet/queue/pipeline/RSA/DNS calculations pass")


if __name__ == "__main__":
    main()
