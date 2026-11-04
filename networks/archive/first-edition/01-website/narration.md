# What Happens When You Open a Website?

English narration for your own voice. Planned runtime: 00:08:45.

The browser pauses after each section. The timestamps below refer to the continuous MP4.


## 01. One click, many conversations — 00:00:00

You click a link, and a page appears. Between those moments, your computer must find a destination, establish communication, and move information across several networks. We will follow one small request rather than every browser optimization. Watch the colored message: its journey will connect the layers in your syllabus.

**On screen:** Browser to server; Many protocols cooperate.

**Visual cue:** website. Opening a website is a sequence of coordinated network tasks.


## 02. Choose a clear teaching model — 00:00:21

Our example uses HTTP version one point one over TCP, with no useful cached answer and no existing connection. Real browsers often reuse connections, cache resources, and use HTTPS or newer HTTP versions. We will add those distinctions later. First, this stripped-down journey makes each network responsibility easier to see.

**On screen:** HTTP/1.1 over TCP; A simplified first visit.

**Visual cue:** website_model. This example explains one path, not every modern browser connection.


## 03. From LAN to WAN — 00:00:42

Imagine your laptop on a home local area network. The destination server sits in a different network. Your traffic reaches a local gateway, passes through provider networks, and eventually reaches the server's network. This is an internetwork: independent networks cooperate, rather than one enormous cable connecting every computer directly.

**On screen:** Local network first; Routers join networks.

**Visual cue:** packet_path. The Internet connects many separate networks.


## 04. Layers divide the work — 00:01:03

OSI names seven layers: application, presentation, session, transport, network, data link, and physical. TCP/IP groups application functions together, uses transport and Internet layers, and can combine local-link and physical functions in its link layer. These are conceptual models rather than exactly matching software boxes. Watch which responsibilities line up before our application message begins moving.

**On screen:** OSI: seven conceptual layers; TCP/IP: four-layer teaching model.

**Visual cue:** osi_tcpip_mapping. OSI and TCP/IP group related communication responsibilities differently.


## 05. Ask for an address — 00:01:25

The browser has a name, but the network needs addressing information. A resolver asks DNS for a suitable record, such as an IPv4 or IPv6 address. Our fictional domain is only a diagram label. A DNS answer can contain multiple addresses, and a name does not always identify one machine.

**On screen:** Name: example.test; DNS answers with records.

**Visual cue:** dns_query. DNS helps translate a useful name into addressing information.


## 06. Follow the DNS hierarchy — 00:01:46

In our uncached example, the recursive resolver consults the DNS hierarchy. Root servers direct it toward the relevant top-level domain; that level points toward the domain's authoritative servers. The resolver follows referrals and obtains an answer. Your laptop normally asks its configured resolver, rather than performing every step shown itself.

**On screen:** Root to domain authorities; Resolver follows referrals.

**Visual cue:** dns_hierarchy. An uncached DNS lookup may follow several referrals.


## 07. Reuse a cached answer — 00:02:08

A later visit may avoid most of that work. Resolvers cache answers for a limited lifetime indicated by time-to-live values. Watch the second query take the short path to the cache. Caching improves responsiveness and reduces repeated traffic, but it does not mean every answer remains valid forever without refreshing.

**On screen:** Cache avoids repeated lookups; TTL limits reuse.

**Visual cue:** dns_cache. A cached DNS answer can shorten the next visit.


## 08. Choose the receiving process — 00:02:29

The destination address gets us toward the server, but that server may run many services. A TCP destination port identifies the intended transport endpoint; the client also chooses a source port. Our unencrypted HTTP example uses port eighty. HTTPS commonly uses port four hundred forty-three, with additional security established before application requests.

**On screen:** IP identifies a host interface; Ports identify transport endpoints.

**Visual cue:** ports. An IP address alone does not select the receiving application.


## 09. Establish a TCP connection — 00:02:52

The client sends SYN. The server replies with SYN and an acknowledgment. The client acknowledges that reply. These messages synchronize sequence information and establish connection state. No physical wire is reserved across the Internet: subsequent packets still share links with other traffic. The arrows represent messages, not a dedicated circuit.

**On screen:** SYN → SYN-ACK → ACK; Synchronize sequence spaces.

**Visual cue:** handshake. The TCP handshake establishes connection state at both ends.


## 10. Build the HTTP request — 00:03:13

Now the browser can send an application request. A simple GET request identifies a resource, with fields such as Host supplying additional context. TCP carries the request's bytes; it does not interpret their web meaning. In the animation, keep the blue application message in sight as other layers add their information.

**On screen:** GET identifies a resource; Headers describe the request.

**Visual cue:** http_get. HTTP describes what the application wants.


## 11. Wrap the application bytes — 00:03:35

Each layer treats information from above as its payload and adds the information it needs. This wrapping is encapsulation. The boxes are conceptual: real headers contain specific fields and their sizes vary. A large application message can span multiple transport segments and packets, so one request is not necessarily one packet.

**On screen:** Headers carry layer information; Payload remains inside.

**Visual cue:** encapsulation_stack. Encapsulation packages one layer's data for the next layer.


## 12. Transport adds its information — 00:03:57

The transport layer adds information such as ports, sequence numbers, and acknowledgments. TCP provides an ordered byte-stream service when communication succeeds. It can retransmit missing data and reassemble arriving bytes. It does not preserve the browser's original write boundaries, and it cannot promise progress through a network that remains permanently unavailable.

**On screen:** Ports and sequence information; A stream can span segments.

**Visual cue:** tcp_segment. TCP organizes a byte stream into segments for transmission.


## 13. Address the IP packet — 00:04:19

The Internet layer places the segment inside an IP packet. Source and destination addresses guide communication between networks. Routers examine destination information to choose a next hop, not an entire reserved end-to-end lane. Ordinary forwarding usually keeps these addresses, while mechanisms such as address translation can modify them in real deployments.

**On screen:** Source and destination IP; Forwarding happens hop by hop.

**Visual cue:** ip_packet. IP addressing supports delivery across interconnected networks.


## 14. Prepare the local frame — 00:04:41

To cross the first local link, the IP packet goes inside a link-layer frame. On an Ethernet example, link addresses identify local interfaces. If the server is outside this network, the next local destination is usually the gateway's interface. The server's distant IP address and the gateway's local MAC address have different jobs.

**On screen:** Link addresses for this hop; Frame carries the IP packet.

**Visual cue:** ethernet_frame. A link-layer frame serves one local link.


## 15. Turn bits into signals — 00:05:04

At the physical interface, bits become signals suitable for the medium: electrical changes, radio signals, or light. They do not travel as tiny written zeros and ones. Our moving dots are a visualization of information progressing. Each real link has its own rate, propagation delay, and signal characteristics to account for.

**On screen:** Electrical, radio or optical; Encoding represents bits.

**Visual cue:** physical_signal. Physical transmission carries encoded information over a medium.


## 16. The switch forwards a frame — 00:05:26

A switch can forward the local frame toward the gateway using its forwarding information. Ethernet switches learn associations from source addresses and use destination addresses for forwarding decisions; unknown destinations can require flooding. This is different from an IP router choosing a route between networks. The animation highlights the chosen outgoing port.

**On screen:** Local MAC-based forwarding; Learning associates ports and MACs.

**Visual cue:** switch_forward. A switch forwards within its link-layer domain.


## 17. The router chooses a next hop — 00:05:48

The gateway receives the frame, extracts its IP packet, and consults its forwarding table. It chooses an outgoing interface and next hop. A new link-layer frame then carries the packet onward. We are following one decision at a time; the router need not understand the HTTP request to forward ordinary traffic.

**On screen:** Remove the incoming frame; Consult the IP forwarding table.

**Visual cue:** router_forward. Routers connect networks by forwarding IP packets.


## 18. New frame, continuing packet — 00:06:10

As the packet crosses routers, its local envelope changes. Different links can use different technologies and addressing conventions. The IP packet continues toward its destination, with forwarding-related fields updated where appropriate. Watch the outer box change while the inner transport data persists. This distinction prevents confusing local delivery with end-to-end communication.

**On screen:** Link headers change by hop; IP forwarding continues.

**Visual cue:** hop_frames. Link-layer envelopes are replaced as a packet crosses routers.


## 19. Shared links can queue or lose — 00:06:32

Other users also need these links. A busy outgoing interface can queue our packet; a full queue can cause a drop. Delay is therefore not only distance divided by signal speed. Our example pauses at one router to distinguish transmission time, propagation, and queuing. TCP can recover from some resulting losses.

**On screen:** Queues introduce delay; Congestion can cause drops.

**Visual cue:** queue_loss. Packets share limited resources along the path.


## 20. Unwrap at the server — 00:06:54

At the server, processing moves upward. The interface handles the frame, the Internet layer handles the IP packet, and TCP associates the bytes with a connection and receiving endpoint. Once the necessary bytes are available, the HTTP application interprets the request. Each layer removes or processes its own information in turn.

**On screen:** Frame → IP → TCP → HTTP; Deliver bytes to the application.

**Visual cue:** decapsulation_stack. Decapsulation lets each receiving layer perform its own job.


## 21. Send an HTTP response — 00:07:16

The server sends an HTTP response containing status information, headers, and usually a representation such as HTML. Those bytes are encapsulated and forwarded back. The return route need not be identical to the outward route. An error status is still a valid HTTP response; receiving a response does not guarantee the requested resource exists.

**On screen:** Status, headers and content; The response takes a return path.

**Visual cue:** http_response. The server sends a new application message back.


## 22. A page can trigger more requests — 00:07:39

The browser interprets the HTML and discovers resources such as style sheets, scripts, and images. These can trigger more requests, sometimes to different servers. Resources may come from caches or content-delivery infrastructure. Our first request explains the basic pattern, but a complete page load is usually a collection of overlapping tasks.

**On screen:** HTML references other resources; Rendering and networking overlap.

**Visual cue:** page_assets. One visible page can require many resource transfers.


## 23. Add the modern distinctions — 00:08:01

Our cleartext HTTP example exposes the layering, but HTTPS protects application traffic using TLS. HTTP version three maps HTTP onto QUIC, which uses UDP rather than TCP. Neither fact removes addressing, forwarding, or physical links. Keep the responsibilities separate even when protocols combine or reorganize functions differently from our simplified picture.

**On screen:** HTTPS adds TLS protection; HTTP/3 uses QUIC over UDP.

**Visual cue:** https_http3. The web uses several protocol combinations, not only HTTP over TCP.


## 24. Retell the whole journey — 00:08:23

Return to the original click. We found addressing information, established the example's transport connection, formed a request, wrapped its data, crossed networks, and unpacked the response. Now explain the journey in your own words. If you can distinguish a name, IP address, port, and local link address, the picture is working.

**On screen:** Find → connect → request → return; Layers cooperate across the path.

**Visual cue:** website_recap. A page load succeeds because multiple protocols perform distinct jobs.
