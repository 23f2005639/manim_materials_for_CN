# Topics covered in the video series

Eight original computer-networking explainers made with ManimGX. Each video has 24 scenes, a complete English narration script, a continuous MP4, and individual scene clips. The player lets you advance at your own pace; the runtimes below refer to the continuous silent videos.

| # | Video | Runtime | Main topic | Recording script |
|---|---|---|---|---|
| 1 | What Happens When You Open a Website? | 8:45 | A web request through the network layers | [Script](networks/episodes/01-website/narration.md) |
| 2 | Thousands of Messages, One Cable | 8:45 | Multiplexing: FDM, TDM, and WDM | [Script](networks/episodes/02-multiplexing/narration.md) |
| 3 | Delivering Data When Packets Get Lost | 9:05 | Reliable delivery and sliding windows | [Script](networks/episodes/03-reliable-delivery/narration.md) |
| 4 | When Computers Talk at Once | 9:05 | Shared-medium access and collisions | [Script](networks/episodes/04-channel-access/narration.md) |
| 5 | How Routers Find the Best Path | 8:30 | Routing algorithms and convergence | [Script](networks/episodes/05-routing/narration.md) |
| 6 | Subnetting You Can Actually See | 8:20 | IPv4 prefixes, masks, and address blocks | [Script](networks/episodes/06-subnetting/narration.md) |
| 7 | TCP vs UDP: The Cost of Reliability | 8:50 | Transport services and their trade-offs | [Script](networks/episodes/07-tcp-udp/narration.md) |
| 8 | Sending Secrets Without Sharing a Secret First | 8:50 | Encryption, key distribution, and authentication | [Script](networks/episodes/08-cryptography/narration.md) |

## 1. What Happens When You Open a Website?

Follow one browser request from a website name to the server and back.

- Local networks, wider networks, switches, routers, and next-hop forwarding.
- OSI and TCP/IP layer responsibilities.
- DNS resolution, referrals, caching, and answer lifetimes.
- IP addresses, application ports, and a TCP three-way handshake.
- HTTP requests and responses, encapsulation, link frames, and physical signals.
- Queues, packet loss, additional page resources, HTTPS, and the HTTP/3 distinction.

The animated journey uses HTTP/1.1 over TCP as a simplified first visit. It does not represent every modern browser connection.

[Open player](networks/episodes/01-website/presentation.html) · [Video](networks/episodes/01-website/episode.mp4)

## 2. Thousands of Messages, One Cable

Explore how several streams share one physical path while remaining distinguishable at the receiver.

- Physical media versus logical channels; multiplexers and demultiplexers.
- Frequency, bandwidth, frequency-division multiplexing, guard bands, and filtering.
- A worked FDM allocation: three 20 kHz channels plus two 5 kHz gaps use 70 kHz.
- Time-division multiplexing, repeating slots, synchronization, and idle-slot waste.
- Statistical TDM and allocating capacity to active sources.
- Optical wavelength-division multiplexing and a four-channel capacity example.
- Physical limits and choosing a sharing method for the traffic.

[Open player](networks/episodes/02-multiplexing/presentation.html) · [Video](networks/episodes/02-multiplexing/episode.mp4)

## 3. Delivering Data When Packets Get Lost

Build reliability from confirmations, saved copies, timers, and sequence numbers.

- Stop-and-wait operation and sender/receiver timelines.
- Transmission time versus propagation time; a link-utilization calculation.
- Lost data, lost acknowledgments, timeouts, retransmission, and duplicate detection.
- Alternating-bit sequencing and timeout trade-offs.
- Sliding windows, multiple outstanding packets, cumulative ACKs, and pipelining.
- A worked Go-Back-N loss and recovery sequence.

ACK numbers in this model identify the next expected **packet**. TCP's byte numbering is covered separately in video 7.

[Open player](networks/episodes/03-reliable-delivery/presentation.html) · [Video](networks/episodes/03-reliable-delivery/episode.mp4)

## 4. When Computers Talk at Once

Show why collisions happen and how access protocols coordinate senders on a shared medium.

- Pure ALOHA, slotted ALOHA, vulnerable intervals, and ideal throughput limits.
- Random retries, scheduling, and contention.
- Carrier sensing and the effect of propagation delay.
- One-persistent, nonpersistent, and p-persistent CSMA.
- CSMA/CD, collision detection, jam signals, frame duration, and binary exponential backoff.
- Differences between historical shared half-duplex Ethernet, switched full-duplex Ethernet, and Wi-Fi.

CSMA/CD is presented in its historical shared-wire setting; it is not described as the access method for modern full-duplex Ethernet or Wi-Fi.

[Open player](networks/episodes/04-channel-access/presentation.html) · [Video](networks/episodes/04-channel-access/episode.mp4)

## 5. How Routers Find the Best Path

Use a weighted network graph to discover a least-cost route and respond to a failed link.

- Graphs, link costs, hop counts, routing, and forwarding.
- Dijkstra's algorithm, tentative distances, predecessor tracking, and next-hop selection.
- A worked route costing 13, changing to 14 after a link failure.
- Distance-vector updates and link-state information sharing.
- Convergence, stale information, counting to infinity, RIP's unreachable metric, and poisoned reverse.
- Routing metrics, policy, and hierarchy.

The graph uses illustrative positive costs, rather than measuring an actual Internet route.

[Open player](networks/episodes/05-routing/presentation.html) · [Video](networks/episodes/05-routing/episode.mp4)

## 6. Subnetting You Can Actually See

Turn subnetting into a visible change in the boundary between prefix and host bits.

- IPv4's 32-bit address, octets, CIDR prefixes, subnet masks, and bitwise AND.
- Splitting `192.168.1.0/24` into four equal `/26` subnets.
- The `/26` mask `255.255.255.192` and network starts at 0, 64, 128, and 192.
- Network addresses, broadcast addresses, and ordinary LAN host ranges.
- Determining a host's subnet, local delivery, and remote next hops.
- Choosing a block for 50 hosts and understanding `/31` and `/32` exceptions.
- Private addressing and why a subnet alone is not a security policy.

[Open player](networks/episodes/06-subnetting/presentation.html) · [Video](networks/episodes/06-subnetting/episode.mp4)

## 7. TCP vs UDP: The Cost of Reliability

Compare transport behavior by asking what the application needs when information goes missing.

- Ports, UDP datagrams, and TCP's ordered byte-stream service.
- The TCP handshake and independent sequence spaces in each direction.
- Byte sequence numbers, cumulative acknowledgments, gaps, retransmission, and duplicates.
- Buffering and the delay caused by ordered delivery.
- Receiver flow control, receive-window changes, and the separate role of congestion control.
- Application protocols above UDP; complete files versus timely updates.
- TCP connection closure and why neither transport is universally faster.

[Open player](networks/episodes/07-tcp-udp/presentation.html) · [Video](networks/episodes/07-tcp-udp/episode.mp4)

## 8. Sending Secrets Without Sharing a Secret First

Explore the key-distribution problem and how different cryptographic tools cooperate.

- Plaintext, ciphertext, public algorithms, and unpredictable key material.
- Symmetric encryption and the danger of exposing a shared key.
- Public/private key pairs and authenticating the recipient's public key.
- Hybrid protection: a fresh session key, protected key transport, and bulk data encryption.
- Authenticated encryption, integrity tags, nonce requirements, and tampering.
- Key-substitution attacks, sender authentication, and digital signatures.
- How the simplified model differs from TLS 1.3 and why established protocols matter.

The wrapped-key animation is a conceptual hybrid-encryption model, not an implementation of TLS or a cryptographic algorithm.

[Open player](networks/episodes/08-cryptography/presentation.html) · [Video](networks/episodes/08-cryptography/episode.mp4)

## Scripts, references, and playback

- [All eight narration scripts](networks/youtube-scripts.md).
- Each episode's `references.md` contains its technical sources.
- [Playback and rendering instructions](networks/README.md).
- [Verification notes](networks/QA.md).

Start the local player from the project folder:

```sh
python3 networks/serve.py
```

Then open <http://127.0.0.1:8765/networks/>. Use →/← for scenes, ↑/↓ for speed, and Shift+P for the current script in a separate presenter window.

## Additional animation in this repository

[The earlier solar-system animation](SolarSystem.mp4) is a separate 30-second 3D demonstration covering eight planets, Earth's Moon, Saturn's rings, and an asteroid belt. Its sizes, distances, and orbital speeds are illustrative. It is not part of the eight networking videos.
