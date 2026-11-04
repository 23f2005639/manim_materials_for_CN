# References — Delivering Data When Packets Get Lost

Sources checked while writing the teaching script; narration is original.

- [MIT 16.36 Lecture 18: ARQ Protocols](https://live.ocw.mit.edu/courses/16-36-communication-systems-engineering-spring-2009/9b06e175ee2b383dc35490581a45267a_MIT16_36s09_lec18.pdf) — Checked Go-Back-N receive-next acknowledgment convention, ordered acceptance, sender window and retransmission examples.
- [Loyola University: Abstract Sliding Windows](https://intronetworks.cs.luc.edu/current/uhtml/slidingwindows.html) — Checked retransmit-on-timeout and stop-and-wait/sliding-window concepts. This script explicitly uses next-expected ACK numbering instead of the text’s last-received convention.
- [IIT Kanpur CS425 Lecture 09](https://cse.iitk.ac.in/users/dheeraj/cs425/lec09.html) — Checked cumulative acknowledgment, sender windows and Go-Back-N receiver discard behavior.
- [RFC 9293: TCP](https://www.rfc-editor.org/rfc/rfc9293) — Checked caveat distinguishing this frame-numbered teaching ARQ model from TCP byte sequence numbers and modern behavior.

Animation engine: [ManimGX instructions](https://manimgx.academa.ai/llms.txt).
