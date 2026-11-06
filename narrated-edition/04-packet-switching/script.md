# Why the Internet Breaks Everything Into Pieces

## 01. Send one picture

A picture looks like one object on your screen. Should the network give that whole picture one enormous turn? Let's see what changes when we break the work into pieces. Here are two computers and a connection between them. Connected devices that exchange information form a network. We call a connection along the way a link. The computers send data: information represented electronically. Our blue rectangle stands for the picture's data. How should it take its turn on that link?

## 02. Meet a packet

Instead of sending that whole blue rectangle as one uninterrupted unit, divide its data into smaller pieces. Add a little handling information to each, including where it needs to go. That unit is called a packet. Think of several labeled parcels instead of one enormous delivery. The numbers in our drawing help us follow the pieces; they are not a claim that every network packet has a sequence number.

## 03. Share between packets

Now your friend sends a tiny green message while the blue picture is being sent. If the entire picture took one uninterrupted turn, green would wait for the whole thing. With packets, there is a choice between pieces. Send one blue packet, then green, then more blue. The link still sends one stream of data, but several conversations can share it. Dividing data creates chances to share; it does not guarantee every message an immediate turn.

## 04. Bits take time to send

Zoom inside one packet. Computers represent information using zeros and ones, called bits. Those bits take time to enter a link. A link's bit rate is how many it can send each second. So two things affect a turn: how many bits the packet contains, and how many bits the link sends per second. More bits mean a longer turn. A higher rate means a shorter one.

## 05. Amount divided by rate

A byte contains eight bits. Our example packet has fifteen hundred bytes, so multiply by eight to get twelve thousand bits. The link sends ten million bits each second. Divide twelve thousand by ten million and we get zero point zero zero one two seconds: one point two milliseconds. A millisecond is one thousandth of a second. The shorthand is L divided by R: length in bits divided by rate. This measures putting data onto the link; signal travel time is extra.

## 06. Receive, then send onward

Real journeys can pass through devices between the two computers. Add two forwarding devices, labeled switches, that pass data to the next link. In our model, each waits until a whole packet arrives before sending that packet onward. We call this store-and-forward. The name describes the action: receive it, then pass it on. Watch packet one finish the first step before starting the second. We will keep this path and rule for our experiment.

## 07. Three links, three turns

Our path now has three links of equal rate. One packet spends one point two milliseconds being sent on the first, then the second, then the third. Add those three turns: three point six milliseconds. For this little experiment, we ignore travel time, device processing, and any other traffic. Those things matter in real life, but hiding them briefly lets us see the pattern. With only one packet, the steps happen in order. What happens if we have several packets ready?

## 08. The next packet can follow

Packet one has reached the first switch. It is now being sent on link two. Look back at link one: it is free. Why leave it doing nothing? Send packet two there. A moment later, packet one uses link three, packet two uses link two, and packet three can use link one. Different parts of the path work at once. This is called a pipeline, like several parcels moving through different stations. Each parcel still visits every station in the proper order.

## 09. Watch the overlap grow

Let's draw that motion as a timetable. Each row is one link. Each column is one turn of one point two milliseconds. A colored box shows which packet uses that link during that turn. First, only the top row works. Next, two rows work. Then all three do. Follow one color diagonally: that is one packet moving through its three steps. Follow one column downward: those are different packets moving at the same time.

## 10. Six turns for four packets

Continue until all four packets arrive. The first packet takes three turns to reach the end. After that, another packet finishes each turn. There are three more packets, so add three more turns: six in total. Six times one point two milliseconds gives seven point two milliseconds. If we waited for each packet's whole journey before starting the next, we would need twelve turns. We simply let separate links do useful work at the same time.

## 11. Count first, write second

Now the formula is just a short version of our counting. Call the number of links H and the number of packets N. The first packet needs H turns. The remaining N minus one packets each add a turn. Together, that is H plus N minus one. Multiply by the time for one turn, L divided by R. That gives our total. It works for this clean model with equal packets and equal-rate links, without extra travel, processing, or traffic delays.

## 12. Conversations come and go

Bring back the green message. Real conversations are uneven. Someone sends a picture, another person pauses, then a new message arrives. Packet switching means the network handles and forwards individual packets, allowing shared links to serve different conversations. A quiet sender need not keep occupying a turn. A ready packet can use the next available opportunity when selected. Two useful effects: different conversations can share one link, and different links can work on different pieces together.

## 13. Packets can still wait

There is a limit. If packets arrive at a device faster than its outgoing link can send them, they form a waiting line, called a queue. Green can still get stuck behind blue. Splitting the picture does not create an endlessly fast connection or a perfectly fair order. If the waiting space fills, a packet may even be discarded. So our claim is modest and useful: packet boundaries give the network manageable turns to share, while actual capacity and queue choices still matter.

## 14. More pieces need more labels

Why not make every piece tiny? Short turns sound wonderful. But remember the handling information added to each packet. That information uses space too. Blue is useful picture data; yellow is the extra label, called a header. Divide the same blue data into more pieces and count the yellow labels. There are more of them. Devices also have more individual packets to handle. Smaller pieces can help sharing, but they are not free. We must balance shorter turns against this extra work.

## 15. The picture comes back together

At the destination, the blue pieces belong to the picture and green belongs to the little message. The receiving computer uses the arriving data to recover the content the application needs. Keeping things complete and in order involves other parts of the communication system; packet switching alone does not promise that. Here, all our pieces arrive successfully. Notice the useful trick: the network could move each piece along without giving the entire picture one enormous turn from beginning to end.

## 16. Small pieces, useful possibilities

We began with one picture on a screen. Breaking its data into packets gave us shorter turns on a shared link. Those pieces also let several links work at once, just like the stations in our parcel line. We still pay for headers, we can still wait in queues, and every link has a limit. But now a big picture and a tiny message can use the same network in manageable pieces. The Internet's useful trick starts with something simple: divide the work.
