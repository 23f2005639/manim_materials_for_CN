# Why Can Your Internet Work While Your Apps Don’t?

English narration for your own voice. Planned runtime: 00:09:07.

The browser pauses after each section. The timestamps below refer to the continuous MP4.


## 01. Connected, but not found — 00:00:00

Your connection says online. A download is still moving. Yet one app refuses to open. That sounds impossible until you separate two questions: can your computer reach the network, and does it know where this service lives? The second question belongs to DNS. Let's follow one name through a small imagined network, then break just the naming part. By the end, an apparently contradictory failure will make perfect sense.


## 02. A name is not an address — 00:00:32

We want photos.orbit.example. That name is convenient for a person, but the network needs an address. Imagine a contact name and its phone number: changing the number doesn't require changing what you call the person. DNS provides a structured way to find information associated with a name. Our made-up domain and addresses are teaching examples. The blue label is the question; the green address is the answer we hope to receive.


## 03. Read the name backward — 00:01:05

The dots have a job. Read the name from the right: the root, example, orbit, then photos. Each level belongs beneath a larger part of the naming tree. This organization lets responsibility be divided. One organization can manage its own branch without maintaining every other branch. Watch the address-like string become a tree. We haven't located a machine yet; we've uncovered the structure that will tell our search where to go next.


## 04. Meet the resolver — 00:01:39

Your computer usually asks a recursive resolver to do the search. Recursive describes the service being offered: please obtain an answer for me. The resolver may already know something useful. For our first pass, assume its relevant caches are empty. That deliberately removes the shortcuts so we can see the work. The resolver becomes our moving point of view, asking more specific questions while your application waits for one useful result.


## 05. The root gives a direction — 00:02:13

The resolver first asks a root service about the name. It doesn't receive the final photo-server address. Instead, it receives a referral toward the service responsible for the next branch. Watch the yellow arrow: it points to where the resolver should ask next. A referral is useful knowledge, even though it isn't the final answer. Think of each step as reducing the remaining search, rather than each server holding the entire directory.


## 06. A smaller branch — 00:02:47

The next service handles our example top-level branch. It directs the resolver toward the authoritative servers for orbit.example. The search is getting narrower. Notice who is doing the asking: the resolver contacts these services, rather than your browser personally visiting every box. The drawing shows logical roles, not one special physical computer per role. Real DNS infrastructure can distribute each role across many machines and locations while preserving this hierarchy of responsibility.


## 07. The authority answers — 00:03:21

Now the resolver reaches an authoritative server for our imagined zone. This is where the relevant record is maintained. In our example, the answer associates the photos name with 192.0.2.10. The green address finally appears. It's tempting to call every earlier server unhelpful because it didn't know this number. But their referrals made this last step possible. DNS scales by sharing responsibility and directions, instead of requiring every participant to know every answer.


## 08. Return the useful result — 00:03:55

The resolver returns the address to your computer. Keep the jobs separate: finding this address doesn't download the photos, prove the application is healthy, or promise that the destination will respond. It supplies information the application needs for its next action. Our story stops at that boundary. The original blue question has become a green result, and the rest of the network can now be used with a specific destination in mind.


## 09. Where the waiting comes from — 00:04:29

Let's attach clocks to the lookup. Suppose the local resolver exchange takes two milliseconds, and the three upstream round trips take twenty, thirty, and forty milliseconds. These are illustrative values, not Internet constants. Since each referral tells us where to ask next, these particular steps happen in sequence. Add the waits: two plus twenty plus thirty plus forty equals ninety-two milliseconds. The equation simply records the journey we just watched, one dependent step after another.


## 10. Repeat the same question — 00:05:04

Now ask the same question again while the answer is cached. The resolver can reply without repeating our three upstream exchanges. In this simplified example, only the two-millisecond local exchange remains. Ninety-two divided by two is forty-six: this lookup is forty-six times quicker. That doesn't mean the entire application becomes forty-six times faster. We measured one task. Still, reusing a valid answer can remove a surprising amount of repeated work from that task.


## 11. Give the memory a lifetime — 00:05:38

A saved answer needs an expiration rule. Our record's time to live, or TTL, is sixty seconds when this cache receives it. Watch the countdown shrink as the answer gets older. Reusing it doesn't restart the clock. If every hit renewed its lifetime indefinitely, a popular old address could remain around forever. The TTL limits how long this cached copy may normally be reused before the resolver needs fresh information for another query.


## 12. Change the address — 00:06:13

Now the authoritative record changes to 203.0.113.20. Does every cache change instantly? Predict the next reply before the colors move. Our cache still holds the earlier answer with thirty seconds remaining, so it may keep returning that old address until its permitted lifetime ends. The authority and cache can temporarily disagree without either ignoring its rules. Changing an authoritative record and replacing every cached copy are different events, separated here by a visible countdown.


## 13. Expiration causes new work — 00:06:47

At zero, the saved answer is no longer fresh. For our normal example, the next query triggers a new lookup and retrieves the changed record. We replay the referrals to make the refresh visible; real resolvers may retain other cached information and take a shorter route. The important change is the answer's freshness. The cache wasn't useless because it eventually expired. Its temporary nature is what lets yesterday's useful shortcut give way to today's information.


## 14. Break only the naming step — 00:07:23

Return to the opening puzzle. The network path is available, but this resolver cannot obtain the answer it needs. The app may fail before it even knows a destination address. Another task can continue because it already has a destination or a still-useful cached answer. That's how online and unable to open this service can coexist. Real outages can have additional causes; here, we deliberately broke only name resolution to isolate its contribution.


## 15. Responsibility, time, and memory — 00:07:57

Three ideas now fit together. Hierarchy divides responsibility, referrals lead the search, and caches save work for a limited time. Remove hierarchy and the directory becomes harder to distribute. Remove caching and repeat questions repeat the journey. Remove expiration and changes become harder to discover reliably. Follow the colored answer rather than memorizing the box names. Its movement, reuse, and replacement explain the mechanism much more clearly than calling DNS a mysterious Internet switch.


## 16. Resolve the opening contradiction — 00:08:32

A working connection and a successful name lookup are separate requirements. DNS turns a readable question into useful location information through a hierarchy, a resolver, and temporary memory. The small clocks explain why that answer can be fast, slow, or briefly old. So when one app stops while another keeps working, the situation isn't logically impossible. One journey may be missing a piece that another already has. The connection is alive; the directions may be missing.
