# The Shortest Route Can Have More Steps

English narration for your own voice. Planned runtime: 00:09:26.

The browser pauses after each section. The timestamps below refer to the continuous MP4.


## 01. The tempting shortcut — 00:00:00

Which route would you choose for this packet? The one with three connections looks shorter than the winding one with five. But a network does not pay for how tidy a route looks on a drawing. It pays the cost of every connection it uses. In a moment, that longer-looking path will beat the shortcut. The interesting question is how to discover it without trying every possible journey. That is the puzzle Dijkstra's algorithm solves.


## 02. Give the links a cost — 00:00:35

Here is our small world: six points, nine connections, and a positive number on each connection. A point could represent a router, but the algorithm only needs the graph. The numbers are illustrative costs, not automatically seconds or kilometers. We choose what they mean before asking for the cheapest route. Keep your eye on A, our starting point, and F, our destination. Everything else is a possible intermediate step in their journey.


## 03. Count costs, not connections — 00:01:09

Follow A to B, B to D, then D to F. The costs are four, five, and six, totaling fifteen. Now take A to C to B to D to E to F. Two, one, five, two, three: thirteen. More connections, smaller bill. Try predicting the winner from the picture alone and it is easy to get fooled. The numbers describe our objective, so the complete sum must decide which route is better.


## 04. Start with what is known — 00:01:43

Instead of guessing a complete route, we will grow a region of known shortest distances. A starts at zero because reaching the place where we already are costs nothing. Every other point begins at infinity, our shorthand for no route discovered yet. These are distance estimates, not numbers written on the links. The central rule is simple: choose the smallest unfinished estimate, settle it, and check whether going through it improves any neighbor.


## 05. Open the first possibilities — 00:02:17

A is the only point with a finite estimate, so it is settled first. Its connection to B offers a distance of four; its connection to C offers two. Write both as tentative results. Tentative matters: discovering a route to B does not mean we have discovered the cheapest route to B. We have only found the best one so far. Which unfinished point should we explore next? Choose the smallest estimate, not the closest-looking dot.


## 06. A cheaper way to B — 00:02:53

C wins with distance two. Explore its connections and something useful happens. Through C, reaching B costs two plus one: three. That improves B's earlier four, so replace the estimate and remember C as B's predecessor. Through C, we also discover D at ten and E at twelve. This repeated operation is called relaxation. The word sounds restful, but the job is simply comparing an old estimate with a newly discovered candidate.


## 07. Improve the route to D — 00:03:27

Now B has the smallest unfinished distance: three. Its connection to D costs five. Add that connection to the known cost of reaching B, and the candidate for D becomes eight. Eight beats ten, so update D and save B as its predecessor. Notice what the calculation includes. We are not choosing the cheapest outgoing connection in isolation. Every candidate includes the entire cost already spent getting to the point where this new step begins.


## 08. Finding F is not finishing — 00:04:02

D is next at eight. Through D, E improves from twelve to ten, and F appears with distance fourteen. We have reached the destination in our search. Should we stop? Hold that thought. Fourteen is still an unfinished estimate, and E is waiting with a smaller distance of ten. If the remaining link from E offers a better total, stopping now would miss it. Discovering the destination is different from proving its distance is final.


## 09. One last improvement — 00:04:37

Settle E at ten. Its connection to F costs three, making thirteen. That beats F's fourteen, so the estimate changes and its predecessor becomes E. This is the same small operation we have used all along: known distance plus link cost, compared with the current estimate. There is no special clever trick for the destination. The repeated local calculation is enough to uncover a complete route that our first visual guess failed to recognize.


## 10. The frontier reaches F — 00:05:12

F now has the smallest unfinished estimate, thirteen, so settle it. Our final distances from A are zero for A, three for B, two for C, eight for D, ten for E, and thirteen for F. Watch the green settled region finish growing. Each number was earned by a comparison, rather than copied from a completed answer. The destination's cost is now final because it has crossed the same settled boundary as the earlier points.


## 11. Why the smallest choice works — 00:05:47

Why can that boundary be trusted? Imagine a cheaper undiscovered route to the point we are about to settle. It must leave our settled region somewhere. But our frontier already contains the cheapest available unfinished estimate, and every remaining connection has a nonnegative cost. Continuing farther cannot secretly subtract distance. That is the intuition behind the rule. Negative links would break this argument, which is why the graph's cost assumptions are part of the algorithm, not fine print.


## 12. Recover the actual journey — 00:06:24

We have a cost, but a packet needs a route. Each improvement saved a predecessor: the point that gave us the better estimate. Begin at F and follow those clues backward: E, D, B, C, A. Reverse that chain and the forward route appears. The distance number tells us how much the best journey costs; the predecessor chain tells us which journey achieved it. Without those saved clues, the cheapest total alone would not draw the path for us.


## 13. Send a packet along the answer — 00:07:01

Now let the packet travel from A through C, B, D, E, and finally F. Add each link as it moves: two, three, eight, ten, thirteen. The arithmetic and the picture describe the same thing at different scales. A only needs C as its immediate next step toward this destination. We are showing a route on a small teaching graph; actual routing systems apply their own rules when they turn such calculations into forwarding decisions.


## 14. Take away a connection — 00:07:36

Suppose the connection between D and E fails. Our thirteen-cost route no longer exists. Keeping the old answer would be wonderfully efficient right up until the packet reaches the missing connection. So change the graph and ask the same question again. We are not changing the meaning of cheapest, and we do not need a new algorithm. We need to run the calculation against the connections that are actually available now, rather than the ones we remember.


## 15. Recalculate against the new graph — 00:08:12

Without that connection, A to C to B to D to F costs two plus one plus five plus six: fourteen. The route through C and E costs two plus ten plus three: fifteen. Fourteen wins. The updated distances keep E at twelve and reach F at fourteen. A failure does not mean every earlier number must change, but none should be trusted merely because it appeared in yesterday's answer. The graph determines what the calculation can justify today.


## 16. Answer the opening question — 00:08:49

Return to the two routes we started with. The shortest-looking line was never the right test. The useful question was which complete journey had the lowest sum, and Dijkstra answered by growing a trustworthy boundary of distances. Small comparisons produced a global result, then the same method adapted to a changed connection. That is the satisfying idea to keep: we did not need to guess the whole winning route. We built enough correct local knowledge to reveal it.
