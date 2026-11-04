# The Shortest Route Can Have More Steps

English narration for your own voice. Planned runtime: 00:09:33.

The browser pauses after each section. The timestamps below refer to the continuous MP4.


## 01. First, send one message — 00:00:00

Imagine sending a photo to a friend. Your computer cannot jump straight into their computer. The photo travels through connected machines. We draw each machine as a dot and each connection as a line. A small piece of the photo, called a packet, moves along those lines. Some machines pass it onward; these are routers. For now, forget the big internet. We only need a starting dot, an ending dot, and a path between them.


## 02. Give each step a price — 00:00:35

Now give each connection a price. These numbers are made-up points, so a four costs twice as much as a two. Going straight from A to B costs four. But watch the other way: A to C costs two, then C to B costs one. Two plus one is three. Taking two steps was cheaper than taking one! That is our whole puzzle: find the route with the smallest total, rather than the fewest lines.


## 03. Grow a small map — 00:01:10

Let's add a few more machines. Our starting point is still A, but now we want to reach F. The red route costs four, then five, then six: fifteen altogether. The green route takes more steps, yet its prices add to thirteen. You can compare these two by eye. On a huge map, guessing every route would get messy. We need a repeatable recipe. That recipe has a name: Dijkstra's shortest-path algorithm.


## 04. Keep a little scorecard — 00:01:44

Start with a fresh scorecard beside our map. Each score means the cheapest total we have found so far from A. A starts at zero because we are already there. Everywhere else gets a question mark: we have not found a route yet. Books often use this sideways eight, called infinity, for those unknown scores. It does not mean the machines are impossibly far away. It means we still need to discover how to reach them.


## 05. Look one step from home — 00:02:19

Look at the lines leaving A. We can reach B for four points, so write four beside B. We can reach C for two points, so write two beside C. Which unfinished score is smaller? C, with two. That is where we look next. We always choose the smallest unfinished score, then check its neighboring dots. Green will mean a score is finished. Yellow will mean we have found an improvement worth writing down.


## 06. A better way to B — 00:02:54

We have reached C for two points. From here, B costs only one more. Add them: two plus one makes three. Our old score for B was four, so replace it with three. We just found the little shortcut from earlier! Also check C's other connections. D would cost two plus eight, or ten. E would cost two plus ten, or twelve. Write those down as possible routes. A score can improve before it becomes final.


## 07. Choose the cheapest unfinished dot — 00:03:30

Our unfinished scores are now three at B, ten at D, and twelve at E. Choose B because three is the smallest. From B, the connection to D costs five. We have already spent three getting to B, so the whole journey to D costs eight. Eight beats the old ten. Cross out ten and write eight. Notice that we are adding to the journey so far, not choosing a connection only because its own price looks small.


## 08. Find a first route to F — 00:04:06

D now has the smallest unfinished score: eight. Finish D and look outward. Reaching E through D costs eight plus two, which is ten. That improves E's old twelve. Reaching F through D costs eight plus six, which is fourteen. At last, we have found a route to our destination! But wait before celebrating. Fourteen is the best answer we have found so far. Another unfinished dot might still lead us to a cheaper route.


## 09. One last improvement — 00:04:42

The next smallest unfinished score is E at ten. Its connection to F costs three. Ten plus three is thirteen, beating the fourteen we just wrote down. Replace it. This is why finding the destination once was not enough. The first route we noticed was useful, but it was not the winner. Our rule stayed exactly the same: choose the smallest unfinished score, add the next connection's price, and keep the result only when it improves something.


## 10. Know when the answer is ready — 00:05:18

F now has the smallest unfinished score, thirteen. When we choose it, that score becomes final. We can stop if F was our only destination. If we wanted answers for every machine, we would keep following the same rule until all reachable dots were finished. The changing numbers were not random guesses. Each one described a real route we had found, and each replacement made that route cheaper. Green marks the point where we know it cannot improve.


## 11. Why the rule works — 00:05:54

Why trust the smallest unfinished score? Every connection in our picture adds a positive cost. Suppose the cheapest unfinished dot costs eight. A route that first goes through an unfinished dot costing ten cannot come back and beat eight; adding more positive prices only makes ten larger. That is the key idea behind the recipe. Zero-cost connections also work. Negative prices would break this reasoning, so this version of the algorithm requires costs that never go below zero.


## 12. Remember the way back — 00:06:31

A score tells us the price, but how do we recover the actual route? Whenever a score improves, remember which dot supplied that improvement. F remembers E. E remembers D. D remembers B. B remembers C, and C remembers A. Follow those reminders backward and you arrive home. Now reverse the list to get the travel directions. There is no need to try all the routes again. We saved just enough information while improving the numbers.


## 13. Walk the winning route — 00:07:06

Let's take the journey ourselves: A to C, C to B, B to D, D to E, and E to F. The connection prices are two, one, five, two, and three. Keep a running total as the packet moves: two, three, eight, ten, thirteen. Five steps beat the three-step route that cost fifteen. A drawing can make one line look short and another look long. The numbers, rather than the shape of our drawing, decide the winner.


## 14. What if a connection breaks? — 00:07:43

Now remove the connection between D and E. The old winning route runs straight into a missing line. We cannot repair it simply by pretending the old answer is still true. Update the map and run the same recipe again. Some scores may stay the same, because their routes never needed that connection. Others will change. This is a useful networking lesson: a good set of directions depends on an accurate picture of which connections are available.


## 15. Find the new winner — 00:08:19

With that line gone, try A to C to B to D to F. Its prices add to two plus one plus five plus six: fourteen. The route through C and E costs two plus ten plus three: fifteen. Fourteen wins. The updated calculation gives E a score of twelve and F a score of fourteen. We did not invent a special rule for broken connections. We changed the map, then let the same small comparisons find the new answer.


## 16. A big answer from small steps — 00:08:56

We began with one message and a few connected dots. A line had a price, a route added those prices, and a score remembered the best total found so far. Dijkstra's method chose the cheapest unfinished score and improved its neighbors, one step at a time. That simple routine revealed a whole route. So next time a winding path beats a tidy shortcut, it will not feel mysterious. More steps can cost less when the steps themselves are cheaper.
