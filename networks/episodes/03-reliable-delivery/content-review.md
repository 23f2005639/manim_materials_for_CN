# Content review — Reliable delivery

Independent review of the narration, pilot storyboard sheet 3, and current diagram source.

- ACK n is consistently defined as the next expected packet. ACK 1 confirms 0; ACK 3 confirms 0–2; ACK 4 confirms 0–3.
- Stop-and-wait calculation independently checked: 1 ms transmit + 20 ms propagation round trip gives 1/21 ≈ 4.76% utilization, ignoring ACK transmission and processing.
- Lost data, lost ACK and delayed ACK are distinct. Duplicate arrival is not duplicate application delivery.
- Go-Back-N worked trace: send 0–3; lose 1; accept 0; discard 2 and 3; repeat ACK 1; retransmit outstanding 1,2,3; finish with ACK 4. New transmissions are explicitly paused for the example.
- Alternating-bit assumptions and the distinction between textbook frame numbering and TCP byte sequencing are stated.

Requested diagram corrections: ACK 3 label on cumulative slide; ACK 2 shifts window two positions; expiry represented as a local event rather than transmitted message; individual retransmission arrows for 1,2,3. Resolved in the visual source and confirmed by the visual agent; final-render inspection is a separate coordinator check.

Sources: checked MIT, Loyola, IIT Kanpur and TCP specification references are recorded in `storyboard.json`. No guarantee of progress through permanent link failure; this is a teaching ARQ model rather than a full protocol implementation.
