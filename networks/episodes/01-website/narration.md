# What Happens When You Open a Website?

English narration for your own voice. Planned runtime: 00:08:45.

The browser pauses after each section. The timestamps below refer to the continuous MP4.


## 01. One click, many journeys — 00:00:00

A page appears after one click. But the server could be across an ocean, and your computer started with only a name. How does that tiny action become a complete journey? Follow this request.


## 02. Choose a simple example — 00:00:21

We'll slow down a first visit using HTTP version one point one over TCP. Browsers often reuse earlier work. Leaving those shortcuts aside lets us see the separate decisions hidden inside an ordinary page load.


## 03. Connect separate networks — 00:00:42

Our request first crosses a local network, then enters a chain of other networks. The Internet is this interconnection. No single cable stretches from every browser to every website; routers join the pieces together.


## 04. Match responsibilities, not boxes — 00:01:03

Notice how many different jobs are already appearing. Layers separate those jobs. OSI describes seven; this TCP/IP picture groups them into four. They're different ways to organize responsibilities, rather than physical floors inside the computer.


## 05. Find the server address — 00:01:25

The browser has a name, but packets need an address. DNS supplies that missing link. We ask a resolver to find the address associated with the name, turning something readable into something the network can use.


## 06. Follow the DNS referrals — 00:01:46

Without a cached answer, the resolver follows referrals: root, top-level domain, then the authoritative server. Each reply narrows the search. No single directory needs to store the complete answer for every name on the Internet.


## 07. Reuse an answer temporarily — 00:02:08

Now repeat the lookup. The saved answer avoids the earlier search, so the path gets shorter. A cache makes previous work useful again, but only within its allowed lifetime. Old directions can eventually become wrong.


## 08. Select an application endpoint — 00:02:29

Reaching the right computer is only part of delivery. Which application should receive the data? Ports distinguish endpoints there. Our client uses 49152; the server uses 80. The address and port answer different questions.


## 09. Synchronize the TCP connection — 00:02:52

Before the request, three TCP messages cross the link: SYN, SYN with ACK, then ACK. Each side establishes connection state. The connection is shared agreement between endpoints; the network hasn't reserved a private physical path.


## 10. Ask for the resource — 00:03:13

Now the browser can ask for the resource. GET supplies the HTTP meaning; TCP carries the bytes. Notice the separation: transporting a request successfully doesn't tell us whether the requested page exists.


## 11. Keep the message inside — 00:03:35

Watch the blue message stay inside as new information appears around it. This is encapsulation: each layer adds what its own job needs. A larger message can also be divided across several transport segments.


## 12. Add the TCP information — 00:03:57

TCP adds ports and sequence information, identifying the conversation and locating bytes within it. The application data remains inside. A boundary between application writes doesn't necessarily become a boundary between segments on the wire.


## 13. Add the Internet envelope — 00:04:19

Next come the IP source and destination. Routers can use the destination to choose where the packet goes next. The server remains our goal here, though mechanisms such as address translation can alter addresses.


## 14. Address the next local hop — 00:04:41

The outer frame answers a more immediate question: who receives this on the local link? For a distant server, that may be the gateway. The next local destination and the final IP destination serve different purposes.


## 15. Turn bits into signals — 00:05:04

All those headers and bytes must now become a physical signal. Copper, fiber, and radio do this differently. The travelling marks represent changing signals, not tiny printed digits being pushed through a cable.


## 16. Cross the local switch — 00:05:26

At the switch, the frame takes a local turn based on MAC forwarding information. Watch the selected output. This decision moves data within the local network; it doesn't calculate the entire route to the website.


## 17. Choose the next network hop — 00:05:48

The router removes the incoming frame and examines the IP destination. It chooses a next hop without needing to interpret GET. A useful network can move many kinds of application data using the same forwarding machinery.


## 18. Replace the local envelope — 00:06:10

Here is the detail to watch: the local frame changes, while our request continues toward the server. Each routed hop gets its own link information. One journey is being carried through several separate local deliveries.


## 19. Wait behind other traffic — 00:06:32

A shared outgoing link creates a bottleneck. Packets arrive faster than it can send them, so a queue grows. When the buffer fills, packets may be dropped. Connectivity alone doesn't promise immediate or successful delivery.


## 20. Unwrap at the destination — 00:06:54

At the server, the wrapping comes off in stages: link, IP, TCP, then HTTP. Each layer handles its own information and passes the useful contents upward. The application finally receives the request we started with.


## 21. Bring the response home — 00:07:16

The server returns status information and content. Those bytes need the same layered delivery in reverse. But reverse doesn't require an identical route: the response can cross a different sequence of networks on its way back.


## 22. Fetch the rest of the page — 00:07:39

That response may contain instructions to fetch images, styles, and other resources. So one apparent page load becomes several conversations, sometimes involving other servers or caches. The first arrival starts another round of work.


## 23. Keep modern protocols distinct — 00:08:01

Our example used HTTP over TCP. HTTPS adds TLS protection, while HTTP version three uses QUIC over UDP. Different protocols can fill these roles, but the underlying questions about names, endpoints, and delivery still remain.


## 24. Retell the moving story — 00:08:23

Return to the opening click. A name became an address, bytes gained headers, and routers connected local steps into one journey. The remarkable part is how many small agreements cooperate to produce something that feels immediate.
