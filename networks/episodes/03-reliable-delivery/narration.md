# Delivering Data When Packets Get Lost

English narration for your own voice. Planned runtime: 00:09:05.

The browser pauses after each section. The timestamps below refer to the continuous MP4.


## 01. What if data disappears? — 00:00:00

A packet disappears, and the sender hears nothing. Was the message lost, or just the reply? That uncertainty is enough to cause duplicates, endless waiting, or missing data. Let's build a way out.


## 02. Read space and time — 00:00:22

Read this picture as a timeline. The sender is on the left, the receiver on the right, and time moves downward. Sloping arrows cross the distance; returning arrows carry acknowledgments, small messages that report progress.


## 03. Send once, then wait — 00:00:45

Start with the simplest rule: send one packet, keep a copy, and wait for confirmation before sending another. This is stop-and-wait. Keeping the copy gives the sender something to use if the attempt fails.


## 04. Define the acknowledgment number — 00:01:07

We need one precise convention. An ACK names the next packet expected. ACK one confirms packet zero; ACK four confirms zero through three. That number points to the first missing position in the ordered sequence.


## 05. Notice the empty sending time — 00:01:30

Notice the empty space after transmission. The packet is still travelling, and its acknowledgment must travel back. The sender could have more data ready, yet our rule leaves it idle until that round trip finishes.


## 06. Separate transmission from propagation — 00:01:52

Two delays explain this gap. Transmission time measures putting the bits onto the link; propagation time measures their travel. A faster transmitter reduces one delay without making the signal itself cross the distance instantly.


## 07. Measure the wasted opportunity — 00:02:16

Here, transmission takes one millisecond and round-trip propagation takes twenty. Ignoring other overhead, only one millisecond in twenty-one is spent sending useful data: about four point eight percent. The waiting dominates the work.


## 08. Lose the original packet — 00:02:38

Now lose the packet. No acknowledgment returns, but silence doesn't reveal the cause. The data might be missing, its acknowledgment might be missing, or either could simply be late. Waiting forever cannot resolve that uncertainty.


## 09. Let the timer expire — 00:03:01

A timer gives the sender a decision point. When enough time passes without confirmation, recovery begins. Notice what it hasn't established: a timeout is a reason to retry, not proof that the original packet vanished.


## 10. Retry the same logical data — 00:03:24

The saved copy is sent again with the same sequence number. This attempt reaches the receiver, and ACK one returns. With progress confirmed, the sender can release that copy and prepare the next packet.


## 11. Lose feedback instead — 00:03:46

Change just one event: deliver the data, but lose its acknowledgment. The sender sees the same silence and retries. Now a perfectly reasonable recovery creates a second arrival. How can the receiver avoid delivering the contents twice?


## 12. Deliver the payload only once — 00:04:08

The sequence number answers that question. The receiver expects one, so another zero is a duplicate. It repeats ACK one without delivering the data again. Repeating transmission doesn't have to mean repeating delivery to the application.


## 13. Reuse a small sequence space — 00:04:31

For basic stop-and-wait, alternating zero and one can distinguish successive packets under suitable initialization and old-duplicate assumptions. Our larger numbers make the examples easier to track, but sequence information needn't always be a large counter.


## 14. Choose a reasonable timeout — 00:04:54

Set the timer too short and late packets trigger unnecessary retries. Set it too long and actual losses cause long stalls. This delayed acknowledgment exposes the balance. Real protocols can estimate delays and adapt their timers.


## 15. Open a four-packet window — 00:05:17

Can we use the waiting time? Allow four unconfirmed packets instead of one. The sending window limits how much data may be outstanding. It changes the sender's permission to proceed, without adding another physical link.


## 16. Fill the pipeline — 00:05:40

Now zero, one, two, and three follow each other into the network. Earlier packets travel while later ones leave, and acknowledgments return behind them. The same link carries more useful work because we stopped waiting after every packet.


## 17. Confirm an entire prefix — 00:06:03

ACK three confirms the complete run through packet two. That's cumulative acknowledgment: one reply can report progress across several packets. The boundary can advance only through consecutive received data, leaving a gap as the stopping point.


## 18. Slide after confirmation — 00:06:25

In this separate example, ACK two confirms zero and one. The window moves forward two positions, allowing new packets at its far edge. Follow the boundary: the allowed range moves, while its size stays four.


## 19. Create a gap at one — 00:06:48

Now lose packet one after sending zero through three. Zero arrives, so the receiver asks for one. We pause new sends here to isolate the problem: the sender still lacks confirmation for one, two, and three.


## 20. Reject later packets in Go-Back-N — 00:07:11

Our basic Go-Back-N receiver discards two and three because one is missing. Each later arrival prompts ACK one again. Those packets reached the destination, but this protocol hasn't accepted them into the ordered sequence.


## 21. Go back to the oldest — 00:07:33

When packet one's timer expires, the sender retries one, two, and three. Zero remains confirmed. This explains Go-Back-N's extra work after a loss: recovery repeats the outstanding sequence starting at the gap.


## 22. Repair the contiguous sequence — 00:07:56

The repeated packets now arrive in order. ACK four advances the boundary past three, releasing the saved copies. The number still means the next packet wanted. Our convention stays consistent through both failure and recovery.


## 23. Grow overlap, not link capacity — 00:08:19

Compare windows of one, four, and twenty-one. More outstanding packets can fill the waiting time, but can't exceed the link's capacity. TCP uses related ideas with byte numbers and additional mechanisms beyond this simplified packet model.


## 24. Rebuild reliability from causes — 00:08:41

Reliability emerged from a few pieces working together: confirmations, saved copies, timers, sequence numbers, and a moving window. Each solves a different failure. Together, they let communication recover when the path can eventually carry data.
