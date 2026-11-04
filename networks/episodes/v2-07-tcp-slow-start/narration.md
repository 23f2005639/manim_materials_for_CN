# How Does a Download Discover Its Speed?

English narration for your own voice. Planned runtime: 00:09:45.

The browser pauses after each section. The timestamps below refer to the continuous MP4.


## 01. An unknown road ahead — 00:00:00

A download is ready to send millions of bytes. Somewhere ahead is a connection that limits how quickly they can pass, but the sender does not begin with a map of its available capacity. Sending everything immediately could overwhelm it. Sending painfully little forever wastes an opportunity. So how does a sender start? Watch the first packets and their returning acknowledgments. They will do more than confirm delivery: they will help pace a growing experiment called TCP slow start.


## 02. Separate the limits — 00:00:37

Our picture has a sender, a receiver, and a bottleneck along the path. Assume the receiver has plenty of free buffer space, so its advertised window is not the limit in this story. We are focusing on the sender's congestion window, usually called cwnd. It bounds how many bytes may be outstanding without acknowledgment. That is a quantity of data, not a transmission speed printed on the cable. Keeping those two meanings separate will make the later equation much easier.


## 03. Begin with a small window — 00:01:14

For our illustration, begin with room for four full-size segments. Four is a teaching choice, not a claim that every TCP connection starts there. Initial-window choices have changed across specifications and implementations. We are also assuming one useful acknowledgment for each new segment and steady round-trip timing. These clean assumptions let us see the mechanism before real network variation blurs it. The sender has more data ready, but only these first four segments are allowed into the experiment.


## 04. The first packets leave — 00:01:50

One, two, three, four. The sender puts those segments onto the path, then waits for progress to be confirmed. At this point, there can be four segments of unacknowledged data in flight. They are not travelling on four new cables. They are sharing the same path at different positions. If the sender released its whole file just because the first segment had left its machine, it would be ignoring the very uncertainty slow start is trying to manage.


## 05. An acknowledgment opens space — 00:02:27

The first acknowledgment comes back. Part of its effect is straightforward: the confirmed data no longer counts as outstanding. There is now room to send a replacement segment within the old window. But slow start also increases the congestion window when new data is acknowledged, subject to its rules. In our simplified full-segment example, it adds one more segment of allowance. One acknowledgment therefore frees old space and helps create new space. That combination is what makes the next round grow.


## 06. Four acknowledgments become eight — 00:03:05

Repeat that process for the four initial segments. Each acknowledgment confirms progress and contributes one segment to our illustrative window growth. By the end of this round, cwnd has increased from four segments to eight. The sender can now have twice as much unacknowledged data outstanding. It did not ask a router for an exact bandwidth number. It used successful delivery feedback to expand cautiously from its starting point. The growth is emerging from the acknowledgment rule, not a stopwatch alone.


## 07. The acknowledgment clock — 00:03:43

Look closely at the returning arrows. Acknowledgments do not just arrive after an abstract round has finished; each one can permit new sending as it arrives. That is an ACK clock. The flow of feedback helps pace the outgoing flow of data. Our round-by-round grouping makes the count easier to follow, but a real sender does not have to wait for all acknowledgments in a batch before doing anything. It reacts as progress arrives.


## 08. Why the growth doubles — 00:04:18

After eight segments are acknowledged under our assumptions, the window grows by another eight, reaching sixteen. Then sixteen successful segment acknowledgments can take it to thirty-two. Why doubling? Start with W segments of allowance, add roughly W more over a round trip, and the next round has about two W. The exponential-looking graph is the accumulated result of many small increases. The name slow start sounds modest, but its early growth can become surprisingly quick across several rounds.


## 09. Turn the pattern into math — 00:04:54

We can now write the pattern instead of memorizing it. Starting from four, the idealized window after k complete growth rounds is four times two to the power k. Zero rounds gives four; one gives eight; two gives sixteen; three gives thirty-two. The equation describes the clean picture we just built. Delayed acknowledgments, different growth rules, losses, and application limits can change the actual trace. So use this model to understand the mechanism, rather than as a prediction for every download.


## 10. A window is not a rate — 00:05:32

Suppose each segment carries one thousand bytes, to keep the arithmetic visible. A sixteen-segment window holds sixteen thousand bytes of outstanding data. If that much data can be acknowledged every hundred milliseconds, the window supports an average of one hundred sixty thousand bytes per second. Multiply by eight and that is about one point two eight megabits per second. This is a window-limited approximation, not a promise that the path can deliver that rate.


## 11. Distance changes the result — 00:06:07

Keep the same sixteen thousand bytes, but double the round-trip time to two hundred milliseconds. The approximate rate halves, because replenishing the same allowance takes twice as long. Now the expression window divided by round-trip time has a visible meaning: an amount of outstanding data, renewed over a period of time. A larger window can help keep a longer path busy, but it cannot force more through a bottleneck than that connection can actually transmit.


## 12. When the path cannot keep up — 00:06:42

Our growing train eventually reaches a point where the bottleneck cannot serve arrivals as quickly as they build up. Packets wait, and the feedback reaches the sender later. Congestion may also lead to packet loss or explicit signals. Successful earlier rounds did not prove that unlimited growth would remain safe. They only justified increasing from the earlier operating point. Slow start explores available capacity through feedback; it does not receive advance permission to overfill every buffer on the path.


## 13. Give exponential growth a boundary — 00:07:19

TCP has a slow-start threshold, commonly called ssthresh. While the congestion window is below that threshold, slow-start growth can continue. Reaching the threshold or observing congestion changes what happens next. We will stop our explanation at that boundary, because slow start is one part of a larger congestion-control process. The point is that doubling is not meant to continue forever. The same graph that explains its speed also explains why it needs a stopping condition.


## 14. Starting larger changes the early trip — 00:07:54

Try starting with eight segments instead of four in the same idealized example. The growth sequence becomes eight, sixteen, thirty-two. That reaches the thirty-two-segment level one round earlier. A larger initial window can save an early round, but it also begins by placing more unconfirmed data on an unknown path. This is a trade-off, not free speed. Standards and implementations make practical initial-window choices; our animation isolates how that starting choice changes the first few rounds.


## 15. Read a real trace carefully — 00:08:30

Before turning this tidy curve into a universal rule, check the assumptions. Does the sender have enough data ready? Does the receiver have room? Are acknowledgments delayed or grouped? Is another bottleneck already limiting the flow? Each can alter what you observe. The congestion window is permission to have data outstanding, rather than an order to send at a smooth rate. The useful explanation survives those complications: confirmed progress helps the sender grow and pace its early traffic.


## 16. Answer the speed puzzle — 00:09:06

So the sender did not discover a perfect speed setting written somewhere inside the network. It began with limited outstanding data, used acknowledgments to make room and grow that allowance, and stopped the rapid growth when its rules required a transition. The math, the window, and the moving packets were three views of that same feedback process. Slow start is how a connection can begin exploring an uncertain path without treating either permanent caution or an immediate flood as its only option.
