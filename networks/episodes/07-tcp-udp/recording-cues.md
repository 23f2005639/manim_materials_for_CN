# Recording cues — TCP vs UDP: The Cost of Reliability

Record one section at a time, or narrate the click-through presentation live.

Guide subtitles use planned timing. Match final subtitles to your recording after editing.

| Section | Start | Length | What to show | Recording cue |
|---|---|---|---|---|
| 01 | 00:00:00 | 22.33s | Two transports, one unreliable network | Choose a transport by the behavior the application needs. |
| 02 | 00:00:22 | 20.60s | Ports identify application endpoints | Ports help a host deliver incoming transport data to the right endpoint. |
| 03 | 00:00:42 | 22.37s | UDP preserves datagram boundaries | UDP exposes datagrams without TCP’s reliable ordered byte-stream service. |
| 04 | 00:01:05 | 22.33s | TCP exposes a byte stream | TCP preserves byte order, not the application’s original write boundaries. |
| 05 | 00:01:27 | 21.47s | First establish a connection | The handshake synchronizes both directions of sequence space. |
| 06 | 00:01:49 | 21.90s | Step one: the client sends SYN | SYN consumes one sequence number. |
| 07 | 00:02:11 | 21.47s | Step two: SYN plus acknowledgment | An acknowledgment names the next sequence position expected. |
| 08 | 00:02:32 | 23.20s | Step three: acknowledge the server | Both endpoints now know the peer’s starting sequence space. |
| 09 | 00:02:55 | 23.63s | Number bytes, not whole packets | A segment’s sequence number identifies its first data byte. |
| 10 | 00:03:19 | 22.33s | Cumulative acknowledgment | TCP’s acknowledgment number identifies the next expected byte. |
| 11 | 00:03:41 | 21.90s | Packets arrive out of order | Receiving later data does not remove an earlier gap in an ordered stream. |
| 12 | 00:04:03 | 22.77s | Recover the missing byte range | Reliability comes from detecting gaps and retransmitting missing data. |
| 13 | 00:04:26 | 22.77s | A lost acknowledgment is not lost data | Sequence space supports duplicate detection as well as ordering. |
| 14 | 00:04:49 | 21.47s | Reliability adds state and delay | Reliability is a useful service with resource and timing costs. |
| 15 | 00:05:10 | 22.77s | Protect the receiver with flow control | Flow control addresses the receiver’s capacity. |
| 16 | 00:05:33 | 21.03s | Watch the receive window change | An advertised window can change as the application drains its buffer. |
| 17 | 00:05:54 | 23.20s | Congestion control protects the path | Flow control protects the receiver; congestion control protects the network. |
| 18 | 00:06:17 | 21.47s | UDP under the same packet loss | UDP does not add TCP’s retransmission and ordering behavior. |
| 19 | 00:06:39 | 22.33s | Applications can build above UDP | A UDP-based protocol can implement capabilities absent from UDP itself. |
| 20 | 00:07:01 | 20.20s | Faster is the wrong universal label | Transport choice does not create a universal speed ranking. |
| 21 | 00:07:21 | 22.77s | Choose a service for a file transfer | TCP reliability is transport delivery, not every application guarantee. |
| 22 | 00:07:44 | 22.33s | Choose a service for timely updates | A useful transport matches the meaning and timing of application data. |
| 23 | 00:08:06 | 21.90s | Connections also need an ending | Connection release is part of the transport’s state machine. |
| 24 | 00:08:28 | 21.50s | Answer the transport puzzle | Understand the service contract before choosing the transport. |
