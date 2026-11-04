# TCP vs UDP: The Cost of Reliability

English narration for your own voice. Planned runtime: 00:08:50.

The browser pauses after each section. The timestamps below refer to the continuous MP4.


## 01. Choose the service you need — 00:00:00

Lose one piece of data, and two transport services can react very differently. One may hold later bytes until the gap is repaired; the other may let later messages through. Which behavior does your application actually need?


## 02. Reach the correct application — 00:00:22

Start with the destination. IP reaches a network endpoint; a port helps identify the application endpoint there. Both TCP and UDP use port numbers, allowing different conversations and applications to share the same networked machine.


## 03. Keep datagrams as datagrams — 00:00:42

UDP carries separate datagrams. When a datagram arrives intact, its boundary remains visible to the application. UDP itself doesn't guarantee arrival, order, or freedom from duplicates. A message boundary and reliable delivery are independent properties.


## 04. Join an ordered byte stream — 00:01:05

TCP presents an ordered byte stream instead. HEL, LO, and an exclamation mark form continuous bytes, without preserving the original write boundaries. The application must define how to recognize complete messages within that stream.


## 05. Establish shared connection state — 00:01:27

To begin our TCP example, each endpoint needs starting sequence information and connection state. Three handshake messages establish that shared state. The result is a logical connection between endpoints, rather than a reserved route through the network.


## 06. The client sends SYN — 00:01:49

The client sends SYN with sequence number one hundred. SYN occupies one sequence position, so this side's first data byte starts at one hundred and one. That detail will make the following acknowledgment numbers fit together.


## 07. The server answers with both — 00:02:11

The server answers with SYN at five hundred and ACK one hundred and one. Two number spaces now appear: the server's own sequence, and its acknowledgment of the client. Each direction tracks a separate flow.


## 08. Complete the handshake — 00:02:32

The client acknowledges five hundred and one. Both sides now have the starting state for this exchange. The client's first data still begins at one hundred and one; the handshake has established how the counters line up.


## 09. Count bytes, not packets — 00:02:55

Now send one hundred bytes starting at one hundred and one. They occupy positions through two hundred. TCP numbers bytes, not whole packets, so those positions retain their meaning even when data is divided into different segment sizes.


## 10. Acknowledge the next missing byte — 00:03:19

ACK two hundred and one says the earlier bytes have arrived in order, and names the next expected position. This cumulative boundary reports the received prefix of the stream, rather than counting how many packets crossed the screen.


## 11. Let later bytes arrive first — 00:03:41

Later bytes arrive while the middle is missing. The receiver can buffer positions three hundred and one through four hundred, but still expects two hundred and one. Arriving later isn't enough to advance the ordered boundary.


## 12. Fill the missing range — 00:04:03

Retransmit the missing middle. Once it arrives, the stored later bytes connect to the earlier run, and ACK four hundred and one can advance. Repairing one gap makes an entire waiting stretch available in order.


## 13. Lose an acknowledgment — 00:04:26

What if an acknowledgment disappears after successful delivery? The sender may repeat those bytes. Sequence information lets the receiver recognize them and avoid delivering them twice. Lost feedback creates uncertainty, rather than necessarily indicating lost data.


## 14. See ordered delivery wait — 00:04:49

The recovered order comes with a cost. Later bytes may be physically present while the application waits for an earlier gap. Buffers hold them, and recovery takes time. This delay follows from the service TCP has promised.


## 15. Protect the receiver's buffer — 00:05:10

Flow control protects the receiver's limited storage. In a three-hundred-byte buffer, two hundred occupied bytes leave one hundred available. Advertising that remaining room tells the sender how much more it can accept before the application consumes data.


## 16. Free space changes permission — 00:05:33

Fill the remaining space and the receive window reaches zero. Then the application reads two hundred bytes, making space again. A new advertised window permits more sending. Receiver capacity changes as the application processes the stream.


## 17. Protect the network path — 00:05:54

But a receiver with free space can still sit beyond an overloaded router. Congestion control addresses pressure on the path; flow control addresses receiver space. The sender must respect both constraints, because they protect different resources.


## 18. Lose a UDP datagram — 00:06:17

Now lose a UDP datagram. UDP itself doesn't retry it or hold later datagrams behind it. The application sees whatever arrives and decides whether that missing information should be recovered, replaced, or simply left behind.


## 19. Build extra behavior above UDP — 00:06:39

Applications can build retries, acknowledgments, protection, and congestion control above UDP. Those capabilities belong to the protocol using UDP. Choosing a datagram service leaves room to define behavior, but doesn't provide those mechanisms automatically.


## 20. Avoid the universal speed claim — 00:07:01

This is why calling UDP universally faster misses the interesting question. Delay depends on the application, path, and recovery rules. Compare what information must arrive, and when it remains useful, before comparing the speed of two protocols.


## 21. Reassemble a complete file — 00:07:21

For a complete file, a missing range leaves the result incomplete. TCP's reliable ordered stream fits that requirement. The application still handles its own message framing and connection failures; a transport service doesn't remove every possible failure.


## 22. Prefer a fresh update when appropriate — 00:07:44

For some live updates, a newer position makes an older missing position less useful. Waiting to recover history may hurt the experience. That's an application-specific choice, not a blanket guarantee that UDP delivers fresher information.


## 23. Close each direction deliberately — 00:08:06

A TCP connection also closes through coordinated state changes. Each direction can end separately, and FIN occupies a sequence position. Acknowledgments confirm the close. The diagram shows one path through that process, rather than every possible timing.


## 24. Choose behavior, then transport — 00:08:28

Return to the lost piece. Is completeness essential, is order required, or can newer information replace it? TCP and UDP offer different starting services. The useful choice follows from what the application needs its receiver to know.
