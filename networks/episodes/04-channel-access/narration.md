# When Computers Talk at Once

English narration for your own voice. Planned runtime: 00:09:05.

The browser pauses after each section. The timestamps below refer to the continuous MP4.


## 01. Who may transmit now? — 00:00:00

Several devices share a medium, but none can instantly know what every other device is doing. When may one transmit? This local coordination problem lies behind access protocols, and the answer begins with a collision.


## 02. Signals meet and collide — 00:00:21

A and C start before either hears the other. Their signals overlap, making these transmissions fail. Watch the red disturbance spread. The useful question is how each station learns enough to decide what happens next.


## 03. Pure ALOHA starts immediately — 00:00:45

Begin with almost no coordination. Pure ALOHA lets a station send whenever data is ready. Simplicity comes at a cost: another transmission can overlap at many different starting times, forcing failed attempts to be repeated.


## 04. Why the vulnerable interval doubles — 00:01:07

Let a frame last T. Another frame can interfere if it starts within T before our start, or T afterward. Slide those possibilities together: the vulnerable interval spans two T, twice the frame's duration.


## 05. Avoid repeating the same collision — 00:01:30

If colliding stations wait exactly the same time, they can collide again on the retry. Random waits break that symmetry. They're no guarantee for an individual attempt, but reduce the chance of repeating the same overlap.


## 06. Only start at slot boundaries — 00:01:52

Now mark shared starting boundaries. Slotted ALOHA permits transmission only at those boundaries, with frames fitting the slots. Stations can still choose the same slot, but arbitrary partial overlaps no longer create additional collision opportunities.


## 07. One slot remains vulnerable — 00:02:15

Watch the vulnerable interval shrink. Only another attempt in the same slot conflicts with this frame. Coordinating the starts reduces the interval from two T to T, without changing the physical transmission rate.


## 08. Load changes useful throughput — 00:02:38

In the ideal model, pure ALOHA peaks near eighteen point four percent throughput; slotted ALOHA near thirty-six point eight. Push attempts past the peak and collisions dominate. More activity can actually produce less useful delivery.


## 09. Scheduling versus contention — 00:03:00

There are two broad ways to organize access: assign turns, or let stations compete under shared rules. A schedule needs coordination; contention needs a way to handle conflicting attempts. Both must divide finite capacity.


## 10. Listen before transmitting — 00:03:23

What if we listen first? Carrier sensing lets a station check whether the medium appears busy before transmitting. That information avoids some blind collisions, but a quiet local observation isn't perfect knowledge of the whole network.


## 11. Distance creates a collision window — 00:03:45

Here is the remaining problem: signals take time to travel. A distant station can start while the first signal is still approaching it. Both hear silence, both transmit, and neither has broken the listening rule.


## 12. Transmit as soon as idle — 00:04:09

One-persistent CSMA listens continuously and transmits as soon as the channel becomes idle. That eagerness limits waiting, but several waiting stations can react to the same silence together, producing another collision at the restart.


## 13. Wait before sensing again — 00:04:32

Nonpersistent CSMA waits a random interval after finding the channel busy, then checks again. Restart attempts become less synchronized. The trade-off is visible in the empty gap: everyone might still be waiting after the medium becomes free.


## 14. Transmit with probability p — 00:04:54

In a suitable slotted setting, p-persistent CSMA makes sending probabilistic. On an idle slot, transmit with probability p or defer. Adjusting that chance spreads competing attempts, balancing prompt use against the risk of simultaneous starts.


## 15. Historical shared Ethernet — 00:05:17

For the next mechanism, keep one historical setting in mind: shared, half-duplex Ethernet. CSMA/CD senses before sending and detects collisions during transmission. These rules describe that shared medium, rather than every Ethernet or wireless connection.


## 16. Detect, abort, then back off — 00:05:38

After detecting a collision, stop the frame, signal the collision with a jam, and back off. An unsuccessful transmission ends before wasting a whole frame. The stations then use different retry delays to separate their next attempts.


## 17. The collision must return in time — 00:06:02

A far-end collision needs time to become visible at the sender. The sender must still be transmitting when that indication returns. That's why minimum frame duration and the network's round-trip propagation delay are connected.


## 18. Grow the retry-choice range — 00:06:25

After repeated collisions, widen the random range: two choices, then four, then eight. Binary exponential backoff gives competing attempts more room to spread. It changes the distribution of waits, rather than guaranteeing a dedicated turn.


## 19. Count down different retry choices — 00:06:48

After the first collision, choose zero or one slot; after the second, zero through three. Follow the two choices in the picture. Different selections create different retry times, reducing the chance of another synchronized failure.


## 20. Backoff does not reserve a turn — 00:07:11

A completed backoff doesn't reserve the medium. Another station may already be transmitting when the wait ends. The sender still follows the channel rules. A timer tells it when to try, not that success is guaranteed.


## 21. Independent full-duplex flows — 00:07:35

Now replace the shared wire with switched full-duplex links. Separate sending and receiving paths allow opposite flows together. The old shared-medium collision mechanism no longer applies on these links, and CSMA/CD isn't used there.


## 22. Wireless needs different feedback — 00:07:58

Wi-Fi faces different observation limits. A station doesn't simply detect collisions during transmission in Ethernet's way. Contention, avoidance rules, and acknowledgments help coordinate access when different stations may hear different parts of the wireless network.


## 23. Each method adds information — 00:08:20

Compare what each station knows. ALOHA sends; CSMA first senses; CSMA/CD also detects collisions in its shared-wire setting. Adding information changes the rules, while propagation delay still limits how quickly that information can arrive.


## 24. Explain the next attempt — 00:08:43

Return to the collision. Ask what each sender could hear, when it could start, and how it chooses a retry. Those three questions turn a list of protocol names into understandable responses to one shared-medium problem.
