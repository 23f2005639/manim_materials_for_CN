# Delivering Data When Packets Get Lost

English narration for your own voice. Planned runtime: 00:09:05.

The browser pauses after each section. The timestamps below refer to the continuous MP4.


## 01. A packet vanishes — 00:00:00

Imagine sending four pieces of a file across a link. The second piece disappears. The receiver cannot rebuild the file correctly, and the sender cannot see the missing piece from its end. We will construct a reliable delivery method step by step, beginning with one packet and adding only what each failure demands.

**On screen:** A sender cannot see delivery; How can it know what arrived?.

**Visual cue:** stopwait_intro. Reliability requires feedback and carefully tracked state.


## 02. Read the timeline — 00:00:22

Our diagram places the sender on the left and receiver on the right, with time moving downward. A sloping arrow represents a packet taking time to cross the link. A return arrow represents feedback. We use packet numbers for this teaching model; they are not TCP byte sequence numbers in this episode.

**On screen:** Left: sender; Right: receiver; Time moves downward.

**Visual cue:** stopwait_timeline. A timeline separates transmission, arrival, and acknowledgment events.


## 03. Send one, then wait — 00:00:45

The simplest sender transmits packet zero, then waits. It keeps a copy because delivery has not yet been confirmed. When the receiver accepts that packet, it can return an acknowledgment. Only after suitable confirmation does the sender proceed. This discipline is easy to understand, but it leaves the link unused while feedback travels.

**On screen:** One outstanding packet; Wait before sending another.

**Visual cue:** stopwait_data. Stop-and-wait permits one unacknowledged packet at a time.


## 04. Choose an ACK convention — 00:01:07

We must define our numbers before continuing. In this video, acknowledgment one means the receiver next expects packet one, so packet zero has arrived. Acknowledgment four confirms packets zero through three. Some textbooks number acknowledgments by the last received packet instead. Both conventions can work, but mixing them would make this animation wrong.

**On screen:** ACK n means next expected n; ACK 1 confirms packet 0.

**Visual cue:** stopwait_ack. Every ACK number here identifies the next packet expected.


## 05. Notice the idle gap — 00:01:30

After packet zero finishes leaving the sender, its bits still need to reach the receiver, and an acknowledgment must travel back. The sender waits during that interval despite having more data ready. Watch the long empty portion of its timeline. Increasing the link's bit rate alone does not eliminate this round-trip delay.

**On screen:** Data crosses; Feedback returns; The sender waits.

**Visual cue:** stopwait_idle. Long feedback delay can leave a fast link mostly idle.


## 06. Separate two kinds of time — 00:01:52

Transmission time is packet length divided by link rate: how long the sender takes to place the packet onto the link. Propagation delay is how long a signal takes to cross the distance. They are different quantities. A short packet on a fast, distant link can finish transmission long before its first acknowledgment returns.

**On screen:** Transmission: L divided by R; Propagation: distance and signal speed.

**Visual cue:** stopwait_delay. Transmission time and propagation delay measure different things.


## 07. Calculate stop-and-wait use — 00:02:16

For a clean example, one packet takes one millisecond to transmit, while round-trip propagation takes twenty milliseconds. Ignore acknowledgment transmission, processing, and errors. One successful stop-and-wait cycle lasts twenty-one milliseconds. The sender transmits useful data for one of those milliseconds: approximately four point eight percent utilization. These numbers describe our assumed link only.

**On screen:** 1 ms transmission; 20 ms propagation round trip.

**Visual cue:** stopwait_utilization. With negligible ACK cost, utilization is 1 divided by 21, about 4.8 percent.


## 08. Lose the data packet — 00:02:38

Now lose packet zero before it reaches the receiver. No acknowledgment confirming that packet returns. The sender still has its saved copy, but waiting forever would prevent progress. Notice what the sender actually knows: it lacks confirmation. It cannot directly tell whether the packet, the acknowledgment, or something else was delayed or lost.

**On screen:** Data never arrives; No new ACK can confirm it.

**Visual cue:** stopwait_dataloss. A missing acknowledgment leaves the sender uncertain.


## 09. Expire a timer — 00:03:01

The sender starts a retransmission timer. If the required acknowledgment has not arrived before expiry, it attempts recovery. A timeout does not prove the data was destroyed: the network might simply be slow. The distinction matters because recovery can create duplicate arrivals. We therefore need identifiers as well as clocks in our protocol.

**On screen:** Start timer when sending; Expiry triggers a recovery attempt.

**Visual cue:** timeout. A timeout detects missing confirmation, not certain packet loss.


## 10. Retransmit the saved copy — 00:03:24

When the timer expires, the sender transmits its saved copy of packet zero. Its number stays zero because this is another attempt to deliver the same logical data. If it arrives correctly, the receiver returns acknowledgment one. The sender can then discard the saved copy and continue with the next new packet.

**On screen:** Reuse the original sequence number; Keep data until confirmed.

**Visual cue:** retransmit. Retransmission retries the same logical packet.


## 11. Lose the acknowledgment instead — 00:03:46

Change the failure. Packet zero arrives and is delivered, but acknowledgment one disappears. From the sender's perspective, confirmation is still missing, just as before. Its timer eventually expires, and packet zero is retransmitted. Without extra receiver state, the application might receive the same data twice, despite the original transmission having succeeded.

**On screen:** Data arrives successfully; Its ACK disappears.

**Visual cue:** ackloss. The sender may retry data that the receiver already has.


## 12. Recognize the duplicate — 00:04:08

The receiver remembers that it now expects packet one. When another packet zero arrives, it identifies the duplicate, avoids delivering its payload again, and sends acknowledgment one again. This time the acknowledgment reaches the sender. Watch delivery count and arrival count separately: two physical arrivals can still represent one accepted application data item.

**On screen:** Receiver already expects packet 1; Repeat ACK 1; Do not deliver data twice.

**Visual cue:** duplicate_seq. Sequence state distinguishes a duplicate from new data.


## 13. Why alternating bits can work — 00:04:31

For a basic stop-and-wait design, sequence labels can alternate between zero and one, since only one logical packet is outstanding. Correctness still depends on initialization and assumptions that prevent sufficiently old duplicates being mistaken for new packets after wraparound. We keep increasing labels in the remaining diagrams to make the flow easier to follow.

**On screen:** Stop-and-wait can alternate 0 and 1; Assumptions prevent old ambiguity.

**Visual cue:** alternating_bit. A small sequence space requires careful assumptions about delayed duplicates.


## 14. Choose a sensible timeout — 00:04:54

Set the timer too short, and an ordinary delayed acknowledgment can trigger an unnecessary retry. Set it too long, and actual loss stalls communication for longer than needed. Our visual timer is fixed for clarity. Practical protocols often estimate delay and adjust recovery behavior, rather than choosing one universally correct timeout for every network.

**On screen:** Too short: needless repeats; Too long: slow loss recovery.

**Visual cue:** timeout_tradeoff. A timer trades quick recovery against unnecessary retransmission.


## 15. Allow four packets in flight — 00:05:17

To reduce idle time, allow several packets to be outstanding. Our sender window has size four, initially covering packets zero, one, two, and three. The sender may transmit them without waiting after each packet. It still retains copies until confirmation. The window bounds what can be outstanding; it is not four separate physical links.

**On screen:** Window size W = 4; Bound outstanding unconfirmed data.

**Visual cue:** window_intro. A sender window permits several packets before confirmation.


## 16. Fill the pipeline — 00:05:40

Send zero, then one, then two, then three. While earlier packets travel and acknowledgments return, later packets use the link. This overlap is pipelining. A large enough window can improve use of a long-delay link, but errors, receiver capacity, and other limits still matter. A window cannot create capacity beyond the link rate.

**On screen:** Send 0, 1, 2, 3; ACKs travel while data continues.

**Visual cue:** window_pipeline. Pipelining overlaps useful transmission with feedback travel.


## 17. Use cumulative acknowledgments — 00:06:03

Suppose packets zero, one, and two arrive in order. The receiver sends acknowledgment three, meaning three is now the next expected number. That single acknowledgment confirms the entire contiguous prefix through packet two. If an earlier acknowledgment was lost, this newer one can still confirm its data, avoiding some needless retransmission.

**On screen:** ACK 3 confirms 0, 1 and 2; An earlier missing ACK may be covered.

**Visual cue:** window_cumulative. Cumulative ACKs confirm a contiguous prefix of received data.


## 18. Slide the sending window — 00:06:25

Receiving acknowledgment two moves the sender's base from zero to two. Packets zero and one leave the unconfirmed region, and new sequence positions become available at the right. The sender can transmit new packets as permitted. Receiving the same acknowledgment again does not repeatedly advance the window or create unlimited new sending permission.

**On screen:** ACK 2 moves base to 2; New slots become available.

**Visual cue:** window_advance. Acknowledgments advance the window and permit new transmissions.


## 19. Go-Back-N: lose packet 1 — 00:06:48

Now use a Go-Back-N sender with window four. It sends packets zero through three, but packet one is lost. The receiver accepts zero and returns acknowledgment one. It then waits for one. We freeze further new transmissions for this worked example so the outstanding set remains one, two, and three while we demonstrate recovery.

**On screen:** Send 0, 1, 2, 3; Packet 1 is lost.

**Visual cue:** goback_loss. A gap prevents contiguous in-order acceptance in this Go-Back-N model.


## 20. Discard later arrivals — 00:07:11

Packets two and three arrive, but this basic Go-Back-N receiver only accepts its next expected packet. It discards those later arrivals and repeats acknowledgment one. The receiver is not claiming that packets two and three never touched the interface; it is saying the contiguous accepted sequence still ends at packet zero.

**On screen:** Receiver expects 1; Discard 2 and 3; Repeat ACK 1.

**Visual cue:** goback_discard. A basic Go-Back-N receiver discards out-of-order packets.


## 21. Retransmit from the gap — 00:07:33

The timer for the oldest unconfirmed packet expires. Our sender retransmits packets one, two, and three: all the outstanding packets in this example, beginning at the gap. It does not resend confirmed packet zero. This can repeat data that previously reached the receiver but was discarded, which is the cost of this simple recovery strategy.

**On screen:** Oldest unconfirmed packet times out; Resend 1, 2 and 3.

**Visual cue:** goback_timeout. Go-Back-N retransmits outstanding packets starting at the oldest unconfirmed one.


## 22. Accept the repaired sequence — 00:07:56

This time packet one arrives correctly, followed by two and three. The receiver accepts each in sequence and eventually returns acknowledgment four. The sender advances its base to four and releases the confirmed copies. Trace the numbers aloud: the final acknowledgment indicates the next expected packet, not the last packet that was accepted.

**On screen:** Receive 1, then 2, then 3; ACK 4 permits progress.

**Visual cue:** goback_recovery. Once the gap is repaired, in-order acceptance and window movement resume.


## 23. Compare the mechanisms carefully — 00:08:19

Stop-and-wait emphasizes simple state but can waste a long-delay link. Sliding windows allow pipelining; Go-Back-N adds one particular receiver and retransmission policy. Selective-repeat designs can retain out-of-order arrivals instead. Modern TCP uses byte sequencing and additional mechanisms, so do not copy every rule from our frame-numbered teaching protocol into a TCP explanation.

**On screen:** Stop-and-wait: one outstanding; Go-Back-N: a bounded pipeline.

**Visual cue:** arq_compare. Modern TCP is related to ARQ ideas but is not this exact frame protocol.


## 24. Reconstruct reliability yourself — 00:08:41

We solved missing confirmation with acknowledgments and timers, then solved duplicate ambiguity with sequence state. Finally, windows overlapped data and feedback, while Go-Back-N supplied a clear recovery rule. Replay either loss case and predict the next acknowledgment before it appears. Recovery assumes communication eventually succeeds; no protocol can deliver through a permanently broken link.

**On screen:** Feedback + timer + sequence state; Windows improve overlap.

**Visual cue:** arq_recap. Recovery needs feedback and state; permanent link failure can still stop delivery.
