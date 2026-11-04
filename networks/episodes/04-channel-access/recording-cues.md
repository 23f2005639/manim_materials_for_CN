# Recording cues — When Computers Talk at Once

Record one section at a time, or narrate the click-through presentation live.

Guide subtitles use planned timing. Match final subtitles to your recording after editing.

| Section | Start | Length | What to show | Recording cue |
|---|---|---|---|---|
| 01 | 00:00:00 | 21.93s | One medium, several speakers | Medium access control decides how stations share a communication resource. |
| 02 | 00:00:21 | 23.23s | Make overlap visible | A collision concerns overlapping signals at a receiver. |
| 03 | 00:00:45 | 22.80s | Pure ALOHA: send when ready | Pure ALOHA allows a station to begin transmitting whenever data is ready. |
| 04 | 00:01:07 | 22.37s | A vulnerable interval of 2T | For equal-length pure ALOHA frames, the vulnerable interval spans 2T. |
| 05 | 00:01:30 | 22.37s | Why retry randomly? | Independent retry timing reduces the chance of repeated collisions. |
| 06 | 00:01:52 | 22.80s | Slotted ALOHA adds boundaries | Slotted ALOHA restricts transmission starts to common slot boundaries. |
| 07 | 00:02:15 | 22.80s | The vulnerable interval becomes T | Under the ideal slot model, the vulnerable interval is one slot. |
| 08 | 00:02:38 | 21.93s | Interpret the ideal efficiency result | The familiar ALOHA maxima depend on a specific ideal traffic model. |
| 09 | 00:03:00 | 22.80s | Scheduling or contention? | Collision reduction comes with assumptions or coordination costs. |
| 10 | 00:03:23 | 22.80s | Listen before transmitting | Carrier sensing can avoid transmissions that obviously conflict locally. |
| 11 | 00:03:45 | 23.67s | A distant sender can still start | Propagation delay allows collisions even with carrier sensing. |
| 12 | 00:04:09 | 22.80s | One-persistent CSMA | One-persistent stations transmit as soon as their sensed channel becomes idle. |
| 13 | 00:04:32 | 22.37s | Nonpersistent CSMA | Nonpersistent waiting reduces synchronized attempts but can add idle delay. |
| 14 | 00:04:54 | 22.37s | P-persistent CSMA | P-persistent CSMA makes a probabilistic choice at an idle slot. |
| 15 | 00:05:17 | 21.93s | Add detection on historical Ethernet | CSMA/CD belongs to shared half-duplex Ethernet, not all modern Ethernet links. |
| 16 | 00:05:38 | 23.63s | Detect, abort, and signal | Collision detection limits time wasted on an already failed transmission. |
| 17 | 00:06:02 | 23.23s | Why propagation affects frame length | Collision detection constrains the relation between frame time and network extent. |
| 18 | 00:06:25 | 22.80s | Widen the random retry range | Binary exponential backoff expands the retry-choice range after collisions. |
| 19 | 00:06:48 | 23.23s | Work two retry choices | After two collisions, this example draws independently from four slot choices. |
| 20 | 00:07:11 | 23.23s | Backoff does not reserve the cable | Finishing a backoff does not guarantee exclusive access. |
| 21 | 00:07:35 | 23.23s | Modern switched full duplex | Full-duplex switched Ethernet removes the shared-wire collision scenario. |
| 22 | 00:07:58 | 22.37s | Wi-Fi needs different feedback | Wi-Fi uses collision-avoidance mechanisms rather than Ethernet-style CSMA/CD. |
| 23 | 00:08:20 | 22.37s | Compare the added knowledge | Each improvement adds information while retaining physical limitations. |
| 24 | 00:08:43 | 21.97s | Explain the next collision | Medium-access behavior depends on both protocol rules and physical context. |
