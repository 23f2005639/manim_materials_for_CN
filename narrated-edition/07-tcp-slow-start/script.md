# TCP Slow Start: How a Download Learns to Speed Up

## 01. Send a photo in pieces

How does a download know how fast to send? There is no speed-limit sign waiting at the other end. Instead, the sender learns from small replies. Let's start with one piece of a photo. Watch one piece leave your computer and arrive at theirs. In this video we will follow TCP, a set of rules computers can use to deliver data reliably. A piece of TCP data is called a segment. Our question: how many pieces should we send before waiting to hear back?

## 02. How do we know it arrived?

Sending something is not the same as knowing it arrived. So the receiving computer sends a small reply meaning, I've received data up to this point. That reply is an acknowledgment, shortened to ACK. Watch blue data go right and a green reply return left. We will draw one reply for each piece to keep the idea clear. Actual TCP can acknowledge several pieces together. The returning replies give the sender evidence of progress instead of making it guess blindly.

## 03. Leave room for four pieces

Let's begin with an allowance of four pieces. The four empty boxes are spaces for data we have sent but haven't yet had confirmed. This allowance is called the congestion window, often written cwnd. Here, window means a limit, not something on your screen. We chose four for this demonstration; real starting values can differ. Also assume the receiver has plenty of room. That lets us focus on how the sender grows its allowance using feedback from the journey.

## 04. Four pieces, then wait

Send piece one. Fill the first box. Send piece two, then three, then four. All four spaces are now occupied. We call this data outstanding: sent, but not yet confirmed by a reply. The sender cannot keep adding pieces beyond its allowance. It waits for progress. That waiting isn't wasted caution. The sender doesn't yet know how much traffic the path can handle. The blue boxes show exactly what it is waiting to hear about.

## 05. One reply makes more room

Now the first green reply arrives. Two things happen. First, one piece is confirmed, so it no longer occupies a space. Second, during our version of slow start, this reply increases the allowance by one piece. Our limit rises from four to five, with three old pieces still unconfirmed. Five spaces minus three occupied spaces leaves room for two new pieces. Watch both spaces open. A reply both clears old work and gives us permission to try a little more.

## 06. Four replies grow the allowance

Let the other replies come back too. Under our one-reply-per-piece assumption, each adds one space. Starting with four spaces, four replies increase the limit to eight. That's the surprise: we added only one at a time, yet a complete round doubled the allowance. We haven't measured a perfect network speed. We've learned that this batch got through and cautiously allowed more data. The rule is called slow start because it begins with limited data, even though its growth soon becomes rapid.

## 07. Replies set the rhythm

Real replies don't have to arrive as one tidy pile at the end of a round. Watch them return separately. Each reply can make room for more sending immediately. This gives the data a rhythm: progress comes back, more data goes out. People call this the acknowledgment clock. It isn't a separate clock inside the cable. It describes how returning feedback helps pace the sender. Our arrows are deliberately slow so you can follow that cause and effect.

## 08. Watch four become eight

Now repeat the experiment with eight pieces. Eight replies can add eight more spaces, making sixteen. Sixteen can then become thirty-two. Look at the dots rising on the graph: four, eight, sixteen, thirty-two. Each step represents a complete ideal growth round, not a fixed second. Twice as many pieces can produce twice as many replies, which can create twice as much room. That's why adding one per reply produces such a fast-growing pattern over several rounds.

## 09. Write the doubling pattern

We can write what the picture already showed. Begin with four, then multiply by two once for every completed round. After k rounds, the allowance is four times two to the power k. That power just means repeated multiplication: after two rounds, four times two times two equals sixteen. At zero rounds we still have four. You don't need the formula to discover the pattern; it is a short way to describe the doubling we just watched.

## 10. How much per second?

Does an allowance of sixteen pieces tell us the download speed? Not by itself. We also need the time for data to go out and feedback to return. That's the round-trip time, or RTT. Suppose each piece carries one thousand bytes and a round trip takes one tenth of a second. Sixteen thousand bytes divided by that time gives one hundred sixty thousand bytes per second. Eight bits make a byte, so that's about 1.28 million bits per second.

## 11. Waiting longer changes the speed

Keep those same sixteen spaces, but make the round trip twice as long: two tenths of a second. Reusing the allowance now takes longer, so our estimated rate halves to 0.64 million bits per second. Nothing shrank the boxes. Feedback simply returned more slowly. This estimate assumes the window is the main limit and data keeps flowing. It helps explain why a window size and a rate are different things: one counts how much; the other also includes time.

## 12. Too much reaches the narrow link

Can we keep doubling forever? Watch the narrow link in the middle. A link is one connection along the route. This one can pass data more slowly than the sender now brings it. Pieces start waiting, just like people arriving faster than a door lets them through. This limiting connection is called a bottleneck. More data in the waiting line does not make that connection faster. Eventually the sender needs to change how it grows, rather than doubling without a boundary.

## 13. Growth needs a stopping point

TCP uses a boundary called the slow-start threshold. The short label on the diagram is ssthresh. Below that boundary, slow-start growth can continue. At the boundary, the sender moves to another growth phase. In our picture we chose thirty-two so you can see where the steep curve stops. This is a teaching value, not a number shared by every connection. Loss and other feedback can also change the behavior. Today we're following this opening growth idea, not every TCP rule.

## 14. Try a different starting allowance

Let's change just one starting condition. Begin with eight spaces instead of four. Our ideal sequence is now eight, sixteen, thirty-two. We reach thirty-two one round earlier. A bigger starting allowance can save early waiting, but it also places more data onto a path whose capacity we may not know. The two colored curves make that tradeoff visible. There isn't one magic starting number that makes every network behave the same way under every possible load.

## 15. Real downloads vary

If you record a real download, don't expect every curve to match our neat staircase. Perhaps the app has no more data ready. Perhaps replies confirm several pieces at once. Perhaps the receiver has limited space, or data gets lost along the way. Each changes the picture. Our demonstration deliberately kept these distractions out so one cause was visible: replies can grow the sending allowance. Now you can spot the idea without treating our drawing as a universal stopwatch.

## 16. Start small, listen, then grow

Return to that first photo. We began with small pieces, learned what a reply tells us, and used four spaces to track unconfirmed data. Each successful reply both released space and helped grow the allowance. Over ideal rounds, four became eight, then sixteen. The sender didn't need a sign announcing the perfect speed. It began with a limit and learned from feedback. That is the central idea of TCP slow start: start small, listen to progress, and grow.
