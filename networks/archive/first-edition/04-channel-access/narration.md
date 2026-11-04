# When Computers Talk at Once

English narration for your own voice. Planned runtime: 00:09:05.

The browser pauses after each section. The timestamps below refer to the continuous MP4.


## 01. One medium, several speakers — 00:00:00

Put three computers on one shared communication medium. Each has a message ready, and none owns the whole resource permanently. Who gets to transmit now? This is a medium-access problem, separate from choosing an Internet route. We will follow the rules that turn uncoordinated attempts into more useful communication under contention.

**On screen:** Many senders share a resource; Who may transmit now?.

**Visual cue:** channel_intro. Medium access control decides how stations share a communication resource.


## 02. Make overlap visible — 00:00:21

Computer A begins sending, then computer B starts before A finishes. Their signals overlap at a receiver, making correct recovery of the frames impossible in our simple model. The glowing red region marks the conflict. Two drawn arrows crossing is only a visual symbol; actual collision behavior depends on the shared medium and receiver.

**On screen:** Overlapping transmissions interfere; A receiver may lose both frames.

**Visual cue:** collision. A collision concerns overlapping signals at a receiver.


## 03. Pure ALOHA: send when ready — 00:00:45

The simplest rule is to transmit whenever data is ready. This is pure ALOHA. If success is not confirmed, the station waits a random interval and tries again. There is no global turn-taking schedule in this model. At low demand, attempts can succeed easily; more simultaneous demand creates more overlaps and repeated attempts.

**On screen:** No slot boundaries; Retry after missing feedback.

**Visual cue:** aloha. Pure ALOHA allows a station to begin transmitting whenever data is ready.


## 04. A vulnerable interval of 2T — 00:01:07

Give every frame the same duration, T. Another frame beginning less than T before ours can still overlap its start; another beginning less than T after ours can overlap its end. Together, these possible interfering start times span two T. This vulnerable interval explains why even slightly offset attempts can cause trouble.

**On screen:** Equal frame duration T; Conflicts can start before or after.

**Visual cue:** aloha_vulnerable. For equal-length pure ALOHA frames, the vulnerable interval spans 2T.


## 05. Why retry randomly? — 00:01:30

After a collision, suppose both stations wait exactly one second. They may restart together and collide again. Choosing independent random retry delays makes repeated synchronization less likely. It does not guarantee that the next attempt succeeds. Follow two different waiting markers: one station gets a clear opportunity while the other continues waiting.

**On screen:** Identical waits can repeat a clash; Random choices break synchronization.

**Visual cue:** aloha_retry. Independent retry timing reduces the chance of repeated collisions.


## 06. Slotted ALOHA adds boundaries — 00:01:52

Now divide time into slots, each long enough for one of our equal-length frames. Stations may begin only at a slot boundary. They still compete: two choosing the same slot collide. But a station cannot begin halfway through an occupied slot. This extra timing agreement changes which transmission starts can overlap a frame.

**On screen:** Shared slots of duration T; Begin only at slot boundaries.

**Visual cue:** slotted_aloha. Slotted ALOHA restricts transmission starts to common slot boundaries.


## 07. The vulnerable interval becomes T — 00:02:15

With perfectly aligned slots and our ideal assumptions, another attempt must choose the same slot to overlap this frame. The vulnerable start interval is therefore one T rather than two T. Real systems need timing coordination and account for propagation. Our clean slot diagram isolates the benefit of restricting when stations may begin.

**On screen:** Only same-slot starts collide; Neighboring slots do not overlap.

**Visual cue:** slotted_vulnerable. Under the ideal slot model, the vulnerable interval is one slot.


## 08. Interpret the ideal efficiency result — 00:02:38

Under the classic equal-frame, Poisson-attempt model, pure ALOHA throughput is G times e to minus two G, while slotted throughput is G times e to minus G. Their maxima are approximately eighteen and thirty-seven percent. These are model results, not universal measurements for every wireless network or every offered traffic pattern.

**On screen:** Pure maximum: about 18.4%; Slotted maximum: about 36.8%.

**Visual cue:** aloha_efficiency. The familiar ALOHA maxima depend on a specific ideal traffic model.


## 09. Scheduling or contention? — 00:03:00

Compare a reserved time schedule with ALOHA. Scheduled turns avoid collisions among compliant synchronized stations, but an idle station's reservation can waste an opportunity. Contention allows stations to compete when they have data, but collisions and retries consume resources. Different traffic loads and coordination constraints favor different tradeoffs; neither picture represents free bandwidth.

**On screen:** Reserved turns avoid this conflict; Contention shares opportunities.

**Visual cue:** access_compare. Collision reduction comes with assumptions or coordination costs.


## 10. Listen before transmitting — 00:03:23

Carrier Sense Multiple Access improves our rule by listening first. If a station senses the medium busy, it defers according to its protocol. If it appears idle, it may attempt transmission. This avoids some obvious overlaps, but the observation is local and signals take time to propagate. Listening alone cannot guarantee collision-free access.

**On screen:** Sense busy versus idle; Defer when the channel is busy.

**Visual cue:** csma. Carrier sensing can avoid transmissions that obviously conflict locally.


## 11. A distant sender can still start — 00:03:45

Place A and B far apart on the shared wire. A starts, but its signal has not reached B yet. B senses idle and starts too. Both followed the sensing rule, yet their signals collide. Animate the expanding signal fronts separately: a decision based on local silence is not instant knowledge of the entire cable.

**On screen:** Signals need time to travel; Both ends may initially sense idle.

**Visual cue:** csma_propagation. Propagation delay allows collisions even with carrier sensing.


## 12. One-persistent CSMA — 00:04:09

In one-persistent CSMA, a ready station keeps sensing while the medium is busy and transmits when it becomes idle. If several stations are waiting, they can all seize that moment and collide. The name describes eagerness after sensing an idle medium; it does not mean continuing to transmit through an already detected conflict.

**On screen:** Keep sensing while busy; Transmit when the medium becomes idle.

**Visual cue:** csma_persistent. One-persistent stations transmit as soon as their sensed channel becomes idle.


## 13. Nonpersistent CSMA — 00:04:32

A nonpersistent station that finds the medium busy waits a random interval before sensing again. This reduces the chance that every waiting station transmits at the exact instant the channel clears. The tradeoff is extra delay: the channel might become free while a station is still waiting before its next sensing attempt.

**On screen:** Busy? Wait a random interval; Then sense again.

**Visual cue:** csma_nonpersistent. Nonpersistent waiting reduces synchronized attempts but can add idle delay.


## 14. P-persistent CSMA — 00:04:54

In a slotted p-persistent model, a station seeing an idle channel transmits with probability p, or defers to another slot with probability one minus p. The choice spreads attempts, but selecting p requires assumptions about contention. Do not confuse these probability-based starts with the randomly chosen backoff interval after an Ethernet collision.

**On screen:** Idle slot: transmit with p; Otherwise defer to another slot.

**Visual cue:** csma_probability. P-persistent CSMA makes a probabilistic choice at an idle slot.


## 15. Add detection on historical Ethernet — 00:05:17

Historical shared, half-duplex Ethernet adds collision detection. A transmitting station monitors the medium and can detect a collision while sending. We will use that wired shared-medium setting for the next steps. Modern switched full-duplex Ethernet does not use this contention procedure, and Wi-Fi does not simply reuse wired Ethernet's collision-detection operation.

**On screen:** Shared, half-duplex Ethernet; Monitor while transmitting.

**Visual cue:** csma_cd. CSMA/CD belongs to shared half-duplex Ethernet, not all modern Ethernet links.


## 16. Detect, abort, and signal — 00:05:38

When the collision reaches a transmitting station, it stops the unsuccessful frame transmission and sends a jam signal according to the Ethernet procedure. Both stations then enter a retry process. The jam is not the original data successfully reaching its destination. Its purpose belongs to collision handling, not to acknowledging receipt of the intended payload.

**On screen:** Stop the unsuccessful transmission; A jam signal reinforces detection.

**Visual cue:** collision_jam. Collision detection limits time wasted on an already failed transmission.


## 17. Why propagation affects frame length — 00:06:02

Consider the farthest possible competing sender. A collision caused near the far end must propagate back while the original sender is still transmitting if that sender is to detect it. This motivates a relationship between minimum frame transmission time and the collision domain's extent. Exact Ethernet limits depend on the standard and physical configuration.

**On screen:** A far-end clash must return in time; Keep transmitting during detection.

**Visual cue:** collision_minframe. Collision detection constrains the relation between frame time and network extent.


## 18. Widen the random retry range — 00:06:25

If both stations immediately restart after the jam, another clash is likely. Ethernet therefore uses randomized backoff. As repeated collisions occur, the choice range grows exponentially up to a cap. Each station independently chooses from the appropriate range. Waiting reduces synchronized retries, but it is a contention mechanism rather than a guaranteed reservation.

**On screen:** Repeated clashes widen choices; Choose independently after a collision.

**Visual cue:** backoff. Binary exponential backoff expands the retry-choice range after collisions.


## 19. Work two retry choices — 00:06:48

In our example, the first collision gives each station a choice of zero or one backoff slot. After a second collision, choices range from zero through three. Let A choose one and B choose three. Their different delays help separate the next attempts. These backoff slots are Ethernet timing units, not ALOHA packet slots.

**On screen:** First collision: choose 0 or 1; Second collision: choose 0 through 3.

**Visual cue:** backoff_numbers. After two collisions, this example draws independently from four slot choices.


## 20. Backoff does not reserve the cable — 00:07:11

Even after choosing a waiting interval, a station has not booked a private future turn. Other stations may transmit, so the access procedure still has to account for the medium's state before the retry. Our chosen numbers illustrate separation, not guaranteed success. Repeated failures can ultimately cause the frame transmission attempt to be abandoned.

**On screen:** Other stations may also transmit; Carrier sensing still matters.

**Visual cue:** backoff_resense. Finishing a backoff does not guarantee exclusive access.


## 21. Modern switched full duplex — 00:07:35

Replace the shared cable with separate full-duplex links to a switch. A host can transmit and receive at once on its link, without competing for the old shared half-duplex wire. CSMA/CD is not used on that full-duplex link. Queues, congestion, and dropped frames can still occur; removing collisions does not remove every network bottleneck.

**On screen:** Separate transmit and receive paths; No CSMA/CD on full-duplex links.

**Visual cue:** ethernet_switch. Full-duplex switched Ethernet removes the shared-wire collision scenario.


## 22. Wi-Fi needs different feedback — 00:07:58

Wireless stations cannot assume they can reliably detect another transmission's collision while transmitting their own strong signal. Stations can also hear different neighbors. Wi-Fi therefore uses collision-avoidance mechanisms and acknowledgments, with additional details beyond this episode. Carrier sensing remains useful, but wired CSMA/CD is not an accurate description of Wi-Fi medium access.

**On screen:** Wireless sensing is location-dependent; Avoidance and ACKs help manage access.

**Visual cue:** wifi_ca. Wi-Fi uses collision-avoidance mechanisms rather than Ethernet-style CSMA/CD.


## 23. Compare the added knowledge — 00:08:20

Line up the three strategies. ALOHA starts without carrier sensing. CSMA checks local channel activity before attempting transmission. CSMA/CD also detects collisions during transmission in its appropriate wired setting. Each uses more information, but none makes signal propagation instantaneous. Keep the assumptions beside the diagram whenever you compare their behavior or efficiency.

**On screen:** ALOHA: no sensing; CSMA: sense; CSMA/CD: detect.

**Visual cue:** mac_compare. Each improvement adds information while retaining physical limitations.


## 24. Explain the next collision — 00:08:43

Replay the opening clash. Now you can propose aligned slots, carrier sensing, or a wired detection-and-backoff procedure, and explain each approach's limits. Before answering an exam question, identify whether the system is shared half-duplex Ethernet, switched full duplex, or wireless. That context determines which collision story is physically and technically appropriate.

**On screen:** Timing, sensing and randomization; Always identify the medium.

**Visual cue:** mac_recap. Medium-access behavior depends on both protocol rules and physical context.
