# Recording cues — How Routers Find the Best Path

Record one section at a time, or narrate the click-through presentation live.

Guide subtitles use planned timing. Match final subtitles to your recording after editing.

| Section | Start | Length | What to show | Recording cue |
|---|---|---|---|---|
| 01 | 00:00:00 | 21.60s | Which route should this packet take? | A route is best only relative to its chosen metric. |
| 02 | 00:00:21 | 20.77s | Turn the network into a graph | A graph makes route choices visible and calculable. |
| 03 | 00:00:42 | 21.17s | Add costs, not just hops | Path cost is the sum of the costs along that path. |
| 04 | 00:01:03 | 21.17s | Routing versus forwarding | Compute routes in the control plane; forward packets using the result. |
| 05 | 00:01:24 | 20.77s | Start Dijkstra at A | Dijkstra grows a tree of shortest paths from the source. |
| 06 | 00:01:45 | 20.73s | Settle A and inspect its neighbors | Relaxing a link means testing whether it improves a tentative route. |
| 07 | 00:02:06 | 21.17s | Settle C and improve B | A newly discovered detour can improve an earlier direct route. |
| 08 | 00:02:27 | 20.77s | Settle B and improve D | Always expand the smallest unvisited tentative distance. |
| 09 | 00:02:48 | 21.17s | Settle D and reach toward F | Discovery is not finalization: a cheaper route may still appear. |
| 10 | 00:03:09 | 21.17s | Settle E and improve F | Compare complete candidate costs, not just the last link. |
| 11 | 00:03:30 | 21.20s | Finalize F: thirteen is optimal | Final distances summarize the shortest-path tree rooted at A. |
| 12 | 00:03:51 | 21.17s | Follow the predecessors backward | Predecessor links reconstruct the actual route, not merely its cost. |
| 13 | 00:04:12 | 21.60s | Install the next hop | A forwarding decision chooses the next hop toward a destination. |
| 14 | 00:04:34 | 20.77s | Distance vector: ask the neighbors | Distance vectors exchange destination estimates with neighbors. |
| 15 | 00:04:55 | 20.30s | A numerical distance-vector update | The Bellman-Ford update combines a local link cost with a neighbor estimate. |
| 16 | 00:05:15 | 22.07s | Link state: distribute the map | Link-state protocols distribute topology, then compute routes locally. |
| 17 | 00:05:37 | 22.03s | Same goal, different information | Do not confuse the information exchanged with the forwarding action. |
| 18 | 00:05:59 | 21.17s | Break the D-to-E link | A shortest path is valid only for the topology used to calculate it. |
| 19 | 00:06:20 | 21.17s | Convergence takes time | Convergence is a process, not an instantaneous global switch. |
| 20 | 00:06:41 | 21.63s | Why bad news can travel slowly | Count-to-infinity is a distance-vector convergence failure mode. |
| 21 | 00:07:03 | 22.03s | Reduce loops, but know the limits | Convergence safeguards reduce specific problems; they are not magic. |
| 22 | 00:07:25 | 21.17s | A shortest path is not every policy | The algorithm solves the cost model you actually give it. |
| 23 | 00:07:46 | 21.63s | Scale through hierarchy | Hierarchy makes routing information manageable at larger scales. |
| 24 | 00:08:08 | 21.63s | Solve the opening puzzle | Best paths depend on costs, topology, and sufficiently current information. |
