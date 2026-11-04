# Rendered visual review

Review scope: rendered storyboard samples and the explicitly listed MP4 frames. This is **not** a claim that every frame or every complete video was watched. Protocol scripts and numerical checks have separate topic content-review reports.

## Reviewed outputs

| Topic | Actual rendered coverage | Result |
|---|---|---|
| 01 — Website journey | All four storyboard sheets, one completed-diagram sample from each of 24 sections; MP4 frames at 347.400 s and 435.067 s extracted independently with FFmpeg | Clear, readable labels and consistent stage layout. The OSI seven-layer to four-layer TCP/IP map is legible. Fictional domain `example.test`, endpoint ports 49152/80, TCP handshake numbering, signal illustration, HTTPS and HTTP/3 distinctions match the teaching model. |
| 02 — Multiplexing | All four storyboard sheets, one completed-diagram sample from each of 24 sections; revised sheets 1, 3 and 4 reviewed again after layout corrections | Intro packets remain clear of DEMUX text. FDM bands and 70 kHz calculation agree, synchronous TDM idle slots are visible, statistical TDM reallocates slots to active A/C sources, and the 40 Gb/s example shows four wavelength channels. WDM dots avoid label collisions. The rebuilt inspector reports no layout problems in 24 samples. |
| 03 — Reliable delivery | All four storyboard sheets, one completed-diagram sample from each of 24 sections | Sender/receiver directions, next-expected ACK convention, lost data versus lost ACK, local timeout event, alternating bits, utilization calculation, ACK 3 cumulative meaning, ACK 2 window movement, individual Go-Back-N retransmissions 1/2/3, and final ACK 4 are displayed clearly. |

| 04 — Channel access | All four rebuilt storyboard sheets, 24 completed-diagram samples | Collision cards disappear at impact, leaving an unambiguous X. Pure/slotted ALOHA alignment, vulnerable intervals, ideal efficiency caveats, retry ranges, and the historical half-duplex scope of CSMA/CD are readable. The Wi-Fi distinction is explicit in narration/captions; the endpoint sketch remains schematic. Inspector: no problems in 24 samples. |
| 05 — Routing | All four sheets via a two-by-two contact sheet; original sheet 1 additionally reviewed at full sheet size | Edge weights and node distances are legible after opaque-card and draw-order fixes. Dijkstra states, a 13-cost shortest path, the 14-cost replacement route after D–E failure, neighbor estimates, count-to-infinity and poisoned reverse are visibly distinct. Link-state markers no longer obscure router names. Inspector: no problems in 24 samples. |
| 06 — Subnetting | All four sheets via contact sheet; original sheet 3 additionally reviewed at full sheet size | Four /26 blocks have correct boundaries and host/broadcast ranges. The .70 AND-mask example yields .64, the 50-host example selects /26, and /31-/32 exceptions are identified. The bit rows, mask table and subnet table stay separate and readable. Inspector reported clean by the independent script reviewer. |
| 07 — TCP/UDP | All four sheets via contact sheet; original sheet 2 additionally reviewed at full sheet size | SYN/SYN-ACK/ACK numbering, ACK 201, missing bytes 201–300, retransmission and ACK 401 agree. Byte-stream writes are separated from UDP datagrams. Receiver and congestion windows are distinguished, and the loss example does not imply UDP reliability. Inspector reported clean by the independent script reviewer. |
| 08 — Cryptography | All four rebuilt sheets via contact sheet; original sheet 3 additionally reviewed at full sheet size | Encryption labels remain unobscured after packet arrival cleanup. Public/private keys, the small-key/bulk-data hybrid split, tag verification, nonce rules, key substitution and authentication distinctions are clearly separated. Every hybrid example is marked as a conceptual model rather than TLS 1.3. Inspector: no problems in 24 samples. |

## Additional observations

- The website contact sheet initially appeared to omit two diagrams at reduced display size. Actual final-video frames were inspected at those same timestamps: the section 16 network nodes/packet and section 20 decapsulation rows are present and readable. No source change was required.
- Text is separated from the left-side narration cues, and the final takeaway remains visible below the stage.
- The diagrams are schematic teaching models. The references and narration explicitly distinguish the HTTP/1.1 walkthrough from modern protocol combinations and textbook Go-Back-N from TCP byte sequencing.

## Source construction check

All 192 diagram configurations were instantiated against their actual storyboards. Each returned group remained within the allocated stage: x = −1.8…6.5, y = −2.45…2.15. This is a construction/bounds check, separate from rendered-frame review.

## Remaining verification scope

The table covers one completed-diagram sample from each of all 192 sections. This does not cover every intermediate animation frame. Full-video playback, navigation behavior, encoded duration, constant-frame-rate normalization and section-clip boundary checks belong to the coordinator's end-to-end checks.
