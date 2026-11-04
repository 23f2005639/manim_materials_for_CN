# TCP vs UDP: The Cost of Reliability

English narration for your own voice. Planned runtime: 00:08:50.

The browser pauses after each section. The timestamps below refer to the continuous MP4.


## 01. Two transports, one unreliable network — 00:00:00

Both TCP and UDP carry application data across an IP network that can lose, duplicate, delay, or reorder packets. Yet they expose different services to applications. We will send a small message through each, introduce failures, and discover why choosing a transport is about required behavior rather than a simple fast-versus-slow label.

**On screen:** IP can lose or reorder packets; Transport defines the application service.

**Visual cue:** udp. Choose a transport by the behavior the application needs.


## 02. Ports identify application endpoints — 00:00:22

IP addresses identify network-layer endpoints, while transport port numbers help distinguish application endpoints on a host. A connection or datagram exchange also includes the transport protocol. Ports are not physical sockets in the drawing; they are numbered fields used for demultiplexing incoming traffic to the appropriate communication context.

**On screen:** IP address + transport port; Demultiplex to the application.

**Visual cue:** udp. Ports help a host deliver incoming transport data to the right endpoint.


## 03. UDP preserves datagram boundaries — 00:00:42

UDP sends individual datagrams. When an application submits a datagram, that boundary remains meaningful at the receiving UDP interface if the datagram arrives intact. UDP itself does not establish a TCP-style connection or promise delivery, ordering, or duplicate suppression. Its small transport service leaves those choices to the application and surrounding protocols.

**On screen:** Individual datagrams; No built-in delivery or order guarantee.

**Visual cue:** udp. UDP exposes datagrams without TCP’s reliable ordered byte-stream service.


## 04. TCP exposes a byte stream — 00:01:05

TCP instead provides a reliable, ordered stream of bytes between endpoints while the connection remains viable. It does not preserve the boundaries of application writes. Three writes might be read as one larger chunk or several smaller chunks. The application must define its own message framing, for example using lengths or delimiters.

**On screen:** Reliable ordered bytes; Write boundaries are not messages.

**Visual cue:** bytestream. TCP preserves byte order, not the application’s original write boundaries.


## 05. First establish a connection — 00:01:27

Before our ordinary TCP data exchange, the endpoints synchronize their initial sequence numbers. We will use one hundred for the client and five hundred for the server as small teaching values. Real sequence numbers are thirty-two-bit values, and practical implementations choose them carefully. The three-way handshake establishes shared connection state.

**On screen:** Client starts at sequence 100; Server starts at sequence 500.

**Visual cue:** handshake. The handshake synchronizes both directions of sequence space.


## 06. Step one: the client sends SYN — 00:01:49

The client sends a segment with SYN set and sequence number one hundred. SYN consumes one position in the client’s sequence space even though it is not an application-data byte. If the handshake succeeds, the first client data byte in this example will therefore have sequence number one hundred and one.

**On screen:** SYN: sequence 100; First client data will start at 101.

**Visual cue:** handshake. SYN consumes one sequence number.


## 07. Step two: SYN plus acknowledgment — 00:02:11

The server replies with its own SYN at sequence five hundred and an acknowledgment of one hundred and one. That acknowledgment means the server has received the client’s SYN and expects the next sequence position. TCP’s two directions have independent numbering; the server does not adopt the client’s starting number.

**On screen:** SYN-ACK: seq 500, ack 101; Each direction has its own numbering.

**Visual cue:** handshake. An acknowledgment names the next sequence position expected.


## 08. Step three: acknowledge the server — 00:02:32

The client sends an acknowledgment of five hundred and one, completing our basic handshake. The next client sequence position is one hundred and one, and the next server position is five hundred and one. An ACK flag by itself does not consume a new sequence number. Application data can now flow in either direction.

**On screen:** ACK: seq 101, ack 501; ACK alone consumes no sequence number.

**Visual cue:** handshake. Both endpoints now know the peer’s starting sequence space.


## 09. Number bytes, not whole packets — 00:02:55

Now the client sends one hundred bytes starting at sequence one hundred and one. Those bytes occupy positions one hundred and one through two hundred. If all arrive contiguously, the receiver acknowledges two hundred and one. TCP numbers the bytes, so changing how the sender divides them into segments does not change their logical order.

**On screen:** 100 bytes: positions 101–200; Next expected byte: 201.

**Visual cue:** bytestream. A segment’s sequence number identifies its first data byte.


## 10. Cumulative acknowledgment — 00:03:19

An acknowledgment of two hundred and one says that every earlier byte in this direction has been received contiguously. It does not mean packet number 201 arrived. Cumulative acknowledgments let one message confirm a whole prefix of the stream. Selective acknowledgment is an additional extension, beyond the simple cumulative example shown here.

**On screen:** ACK 201 confirms through byte 200; Acknowledgments can cover many bytes.

**Visual cue:** bytestream. TCP’s acknowledgment number identifies the next expected byte.


## 11. Packets arrive out of order — 00:03:41

Suppose the byte range 201 through 300 is delayed, but 301 through 400 arrives. The receiver cannot expose the later bytes ahead of the missing range in TCP’s ordered stream. It may buffer them and keep acknowledging the gap at 201. The drawing separates network arrival order from application delivery order.

**On screen:** Bytes 201–300 are missing; Later bytes can wait in a buffer.

**Visual cue:** reorder. Receiving later data does not remove an earlier gap in an ordered stream.


## 12. Recover the missing byte range — 00:04:03

TCP can infer loss through a retransmission timeout and, in suitable circumstances, acknowledgment-based loss detection. It retransmits data covering the missing bytes. Once 201 through 300 arrives, the receiver can join it to the buffered later range and advance its cumulative acknowledgment to 401. Retransmission timing is adaptive, not a fixed universal delay.

**On screen:** Retransmit bytes 201–300; Contiguous receipt advances ACK to 401.

**Visual cue:** reorder. Reliability comes from detecting gaps and retransmitting missing data.


## 13. A lost acknowledgment is not lost data — 00:04:26

If an acknowledgment disappears, the sender may retransmit bytes the receiver already has. Sequence numbers let the receiver identify overlap and avoid delivering duplicate stream data to the application. Later cumulative acknowledgments may also cover earlier progress. This is why loss of a control message does not necessarily require restarting the whole connection.

**On screen:** ACK loss can cause retransmission; Duplicate bytes are not delivered twice.

**Visual cue:** reorder. Sequence space supports duplicate detection as well as ordering.


## 14. Reliability adds state and delay — 00:04:49

To maintain this service, TCP keeps connection state, sequence information, retransmission timers, and buffering. When a gap blocks ordered delivery, later stream bytes can wait even though their packets have arrived. That is stream-level head-of-line blocking. These costs can be worthwhile for applications that need a complete, correctly ordered transfer.

**On screen:** Timers, buffers, connection state; An early gap can delay later bytes.

**Visual cue:** reorder. Reliability is a useful service with resource and timing costs.


## 15. Protect the receiver with flow control — 00:05:10

A receiver can have less free buffer space than the sender would like to fill. TCP’s advertised receive window communicates how much sequence space the receiver is currently prepared to accept. The sender must respect that limit. Flow control protects the receiving endpoint; it does not by itself measure congestion in the network.

**On screen:** Receive window reflects receiver space; Avoid overrunning the receiver.

**Visual cue:** window. Flow control addresses the receiver’s capacity.


## 16. Watch the receive window change — 00:05:33

Imagine the receiver advertises room for three hundred bytes. The sender already has two hundred unacknowledged bytes within that allowance, leaving room for another hundred under this simplified view. As the receiving application consumes buffered data, the receiver can advertise more space. Window updates and acknowledgments coordinate continuing progress.

**On screen:** Allowance 300; in flight 200; Simplified remaining allowance: 100.

**Visual cue:** window. An advertised window can change as the application drains its buffer.


## 17. Congestion control protects the path — 00:05:54

A network can be overloaded even when the destination has plenty of buffer space. TCP congestion control limits sending according to signals about the path, such as losses or explicit congestion notifications. Conceptually, both a congestion allowance and the receive window constrain sending. They solve different problems and should not share one ambiguous label.

**On screen:** Receiver capacity differs from path load; Both limits can constrain sending.

**Visual cue:** window. Flow control protects the receiver; congestion control protects the network.


## 18. UDP under the same packet loss — 00:06:17

Replay the loss with three UDP datagrams. If the middle datagram disappears, UDP does not automatically retransmit it or hold the later datagram for ordered delivery. The application receives whatever valid datagrams arrive through its socket, subject to platform behavior and buffering, and must decide what a missing message means.

**On screen:** Missing datagrams stay missing in UDP; The application decides how to react.

**Visual cue:** udp. UDP does not add TCP’s retransmission and ordering behavior.


## 19. Applications can build above UDP — 00:06:39

UDP’s limited service does not forbid reliable applications. A protocol built above UDP can add acknowledgments, retransmission, congestion control, encryption, or its own ordering rules. QUIC is a practical example of a richer transport carried in UDP datagrams. Compare the complete application stack rather than assuming UDP means an unreliable final product.

**On screen:** Reliability can exist above UDP; QUIC adds a richer transport service.

**Visual cue:** udp. A UDP-based protocol can implement capabilities absent from UDP itself.


## 20. Faster is the wrong universal label — 00:07:01

UDP avoids TCP’s built-in handshake and ordered byte-stream machinery, but that does not guarantee lower end-to-end latency for every application. Loss, application recovery, path conditions, protocol design, and buffering matter. A UDP program that reinvents reliability may pay similar costs. Measure the behavior the user actually experiences.

**On screen:** Less built-in machinery is not a guarantee; Application recovery can add delay.

**Visual cue:** udp. Transport choice does not create a universal speed ranking.


## 21. Choose a service for a file transfer — 00:07:21

For a file that must arrive completely and in order, TCP’s stream is a natural building block. The application still needs framing, error handling, and an appropriate security protocol. TCP does not prove who the peer is, encrypt the bytes, or guarantee that a failed machine saved the complete file to durable storage.

**On screen:** Complete ordered bytes are useful; Security and durable storage are separate.

**Visual cue:** bytestream. TCP reliability is transport delivery, not every application guarantee.


## 22. Choose a service for timely updates — 00:07:44

For a stream of rapidly changing position updates, a newer update may be more valuable than retransmitting an old one. An application may choose UDP and implement its own timing and recovery policy. That choice still requires responsible congestion behavior, security, and careful handling of loss. The application’s semantics guide the design.

**On screen:** Fresh updates may replace stale ones; Handle congestion and security explicitly.

**Visual cue:** udp. A useful transport matches the meaning and timing of application data.


## 23. Connections also need an ending — 00:08:06

TCP connections do not simply forget their state after the last data segment. An orderly close uses FIN to end one direction of the byte stream; each direction can close separately. FIN consumes sequence space like SYN. A reset instead aborts a connection. Applications must handle both clean endings and failures.

**On screen:** FIN ends one stream direction; RST aborts a connection.

**Visual cue:** handshake. Connection release is part of the transport’s state machine.


## 24. Answer the transport puzzle — 00:08:28

TCP offers a reliable ordered byte stream using sequence numbers, acknowledgments, retransmission, and control of sending. UDP offers datagrams without those built-in guarantees, allowing applications to choose additional behavior. Neither transport automatically supplies complete security or perfect application outcomes. Start with requirements, then select and measure the whole protocol design.

**On screen:** TCP: ordered reliable byte stream; UDP: datagrams with minimal guarantees.

**Visual cue:** udp. Understand the service contract before choosing the transport.
