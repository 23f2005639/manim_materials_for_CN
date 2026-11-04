# Recording cues — Delivering Data When Packets Get Lost

Record one section at a time, or narrate the click-through presentation live.

Guide subtitles use planned timing. Match final subtitles to your recording after editing.

| Section | Start | Length | What to show | Recording cue |
|---|---|---|---|---|
| 01 | 00:00:00 | 22.73s | A packet vanishes | Reliability requires feedback and carefully tracked state. |
| 02 | 00:00:22 | 22.33s | Read the timeline | A timeline separates transmission, arrival, and acknowledgment events. |
| 03 | 00:00:45 | 22.73s | Send one, then wait | Stop-and-wait permits one unacknowledged packet at a time. |
| 04 | 00:01:07 | 22.73s | Choose an ACK convention | Every ACK number here identifies the next packet expected. |
| 05 | 00:01:30 | 22.33s | Notice the idle gap | Long feedback delay can leave a fast link mostly idle. |
| 06 | 00:01:52 | 23.17s | Separate two kinds of time | Transmission time and propagation delay measure different things. |
| 07 | 00:02:16 | 22.73s | Calculate stop-and-wait use | With negligible ACK cost, utilization is 1 divided by 21, about 4.8 percent. |
| 08 | 00:02:38 | 22.77s | Lose the data packet | A missing acknowledgment leaves the sender uncertain. |
| 09 | 00:03:01 | 22.73s | Expire a timer | A timeout detects missing confirmation, not certain packet loss. |
| 10 | 00:03:24 | 22.30s | Retransmit the saved copy | Retransmission retries the same logical packet. |
| 11 | 00:03:46 | 21.90s | Lose the acknowledgment instead | The sender may retry data that the receiver already has. |
| 12 | 00:04:08 | 22.73s | Recognize the duplicate | Sequence state distinguishes a duplicate from new data. |
| 13 | 00:04:31 | 23.20s | Why alternating bits can work | A small sequence space requires careful assumptions about delayed duplicates. |
| 14 | 00:04:54 | 23.17s | Choose a sensible timeout | A timer trades quick recovery against unnecessary retransmission. |
| 15 | 00:05:17 | 23.17s | Allow four packets in flight | A sender window permits several packets before confirmation. |
| 16 | 00:05:40 | 22.73s | Fill the pipeline | Pipelining overlaps useful transmission with feedback travel. |
| 17 | 00:06:03 | 21.90s | Use cumulative acknowledgments | Cumulative ACKs confirm a contiguous prefix of received data. |
| 18 | 00:06:25 | 22.73s | Slide the sending window | Acknowledgments advance the window and permit new transmissions. |
| 19 | 00:06:48 | 23.17s | Go-Back-N: lose packet 1 | A gap prevents contiguous in-order acceptance in this Go-Back-N model. |
| 20 | 00:07:11 | 21.90s | Discard later arrivals | A basic Go-Back-N receiver discards out-of-order packets. |
| 21 | 00:07:33 | 23.60s | Retransmit from the gap | Go-Back-N retransmits outstanding packets starting at the oldest unconfirmed one. |
| 22 | 00:07:56 | 22.73s | Accept the repaired sequence | Once the gap is repaired, in-order acceptance and window movement resume. |
| 23 | 00:08:19 | 22.33s | Compare the mechanisms carefully | Modern TCP is related to ARQ ideas but is not this exact frame protocol. |
| 24 | 00:08:41 | 23.20s | Reconstruct reliability yourself | Recovery needs feedback and state; permanent link failure can still stop delivery. |
