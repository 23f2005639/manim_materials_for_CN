# Content review — Website journey

Independent review of the original narration and draft storyboard sheets 2–3.

- DNS lookup is explicitly an uncached teaching example; cached answers expire by TTL. Fictional `example.test` is a diagram label.
- HTTP/1.1 over TCP is distinguished from HTTPS/TLS and HTTP/3 over QUIC. No universal claim that every browser uses this path.
- SYN sequence 100 → SYN+ACK sequence 500 / ACK 101 → ACK 501 is consistent with SYN consuming one sequence position.
- IP destination, transport port and per-hop link addresses have distinct stated roles. Ordinary routing is distinguished from NAT; response routing may differ.
- Section 04 now explicitly names all seven OSI layers and maps their responsibilities to the four-layer TCP/IP teaching model. Source update preserved the coordinator's timing.

Requested diagram corrections: use the same `example.test` name; add an explicit OSI/TCP-IP map rather than repeat encapsulation; make the physical-signal section visibly about encoding. Resolved in the visual source and confirmed by the visual agent; final-render inspection is a separate coordinator check.

Sources: the four checked RFC references are recorded in `storyboard.json` and generated `references.md`. Full browser optimization, live DNS, TLS internals and protocol conformance are outside this illustrative episode.
