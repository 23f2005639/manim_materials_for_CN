# Subnetting You Can Actually See

English narration for your own voice. Planned runtime: 00:08:20.

The browser pauses after each section. The timestamps below refer to the continuous MP4.


## 01. One network, four smaller networks — 00:00:00

Imagine four departments sharing one IPv4 address block. You need four separate, equally sized subnets without inventing new addresses. The puzzle is to divide 192.168.1.0 slash twenty-four correctly. We will solve it with moving bit boundaries, then verify the resulting network, host, and broadcast addresses rather than memorizing a shortcut.

**On screen:** Start with 192.168.1.0/24; Create four equal subnets.

**Visual cue:** subnets. Subnetting divides an existing address block into smaller prefix blocks.


## 02. IPv4 addresses contain thirty-two bits — 00:00:21

An IPv4 address contains thirty-two bits, usually written as four decimal octets. Each octet represents eight bits and therefore ranges from zero to 255. The dots are a writing convention, not additional bits. Every subnet calculation ultimately describes a boundary or pattern within these thirty-two binary positions.

**On screen:** 4 octets × 8 bits = 32; Each octet ranges from 0 to 255.

**Visual cue:** bits. Dotted decimal is a readable way to write the underlying bits.


## 03. A prefix marks the shared beginning — 00:00:41

The slash number tells us how many leading bits form the network prefix. In slash twenty-four, the first twenty-four bits are fixed for the block. The final eight vary across its addresses. A prefix is a bit count, so it need not stop neatly at one of the decimal dots.

**On screen:** /24 fixes the first 24 bits; The final 8 bits can vary.

**Visual cue:** bits. The prefix length counts leading network bits, not decimal digits.


## 04. The mask expresses the boundary — 00:01:03

A subnet mask writes ones in network positions and zeros in host positions. For slash twenty-four, that is three octets of ones followed by eight zeros: 255 dot 255 dot 255 dot zero. The mask and prefix notation express the same boundary in two different forms.

**On screen:** Network bits use mask value 1; /24 mask: 255.255.255.0.

**Visual cue:** mask. A contiguous subnet mask and its prefix length describe the same boundary.


## 05. Find the network with bitwise AND — 00:01:23

Bitwise AND keeps a bit only when both input bits are one. Applying the subnet mask preserves the prefix and clears the host positions. For 192.168.1.42 with a slash twenty-four mask, clearing its last eight bits gives 192.168.1.0. This is the block’s network address, not a host chosen at random.

**On screen:** Address AND mask = network; 192.168.1.42/24 → 192.168.1.0.

**Visual cue:** mask. Masking an address identifies the prefix block that contains it.


## 06. Count the parent block — 00:01:45

Thirty-two minus twenty-four leaves eight variable bits. Eight bits have two to the power eight combinations, so this block contains 256 addresses, from last octet zero through 255. That is a total-address count. Usable host counts require a separate decision about network and broadcast conventions.

**On screen:** 32 − 24 = 8 variable bits; 2^8 = 256 total addresses.

**Visual cue:** subnets. Count all addresses before applying ordinary LAN host reservations.


## 07. Borrow two bits for four subnets — 00:02:04

We want four equal blocks, and two additional prefix bits have four combinations: zero-zero, zero-one, one-zero, and one-one. Extend the prefix from twenty-four to twenty-six. Those two positions now distinguish subnets, leaving six positions to distinguish addresses within each subnet. No new addresses have been created.

**On screen:** 2 borrowed bits give 4 subnets; New prefix: /26.

**Visual cue:** bits. Extending a prefix creates smaller blocks within the original block.


## 08. Build the slash-twenty-six mask — 00:02:24

The final mask octet now starts with two ones and ends with six zeros. In binary it is 11000000, whose decimal value is 128 plus 64, or 192. Our new mask is 255 dot 255 dot 255 dot 192. The subnet boundary falls inside the last octet.

**On screen:** Last mask octet: 11000000; /26 mask: 255.255.255.192.

**Visual cue:** mask. Two leading ones in the last octet make the /26 boundary.


## 09. Six host bits make sixty-four addresses — 00:02:44

Each new subnet has six variable address bits. Two to the power six equals sixty-four total addresses per block. Four blocks times sixty-four returns the parent’s 256 addresses. This conservation check is useful: a correct equal subdivision should neither overlap blocks nor leave gaps inside its parent.

**On screen:** 2^6 = 64 addresses per subnet; 4 × 64 = 256 addresses.

**Visual cue:** subnets. The four /26 blocks exactly cover the original /24.


## 10. The four binary prefixes — 00:03:05

Hold the first twenty-four bits steady and cycle the next two bits through their four combinations. With the remaining six bits all zero, the final octets become zero, sixty-four, 128, and 192. These are aligned network boundaries. Arbitrary numbers such as fifty or ninety are not slash-twenty-six network starts.

**On screen:** 00 → 0; 01 → 64; 10 → 128; 11 → 192.

**Visual cue:** bits. Aligned /26 network starts are separated by 64 addresses.


## 11. Subnet one: zero through sixty-three — 00:03:26

The first block is 192.168.1.0 slash twenty-six. Its six host bits range from all zero to all one, giving last-octet values zero through sixty-three. Under ordinary IPv4 LAN conventions, zero identifies this network and sixty-three is its directed broadcast address. Host addresses are one through sixty-two.

**On screen:** Network .0; broadcast .63; Hosts .1–.62.

**Visual cue:** hosts. Subnet one contains 64 total addresses and 62 ordinary host addresses.


## 12. Subnet two: sixty-four through 127 — 00:03:46

The second block is 192.168.1.64 slash twenty-six. The prefix’s borrowed bits are zero-one, while its six host positions vary. Its network address ends in sixty-four and broadcast ends in 127. Ordinary host addresses run from sixty-five through 126. Notice that a broadcast address does not have to end in 255.

**On screen:** Network .64; broadcast .127; Hosts .65–.126.

**Visual cue:** hosts. Network and broadcast roles depend on the prefix, not just the last octet.


## 13. Subnet three: 128 through 191 — 00:04:07

The third block begins at 192.168.1.128 slash twenty-six. Its network and broadcast addresses end in 128 and 191. Usable host values are 129 through 190 under our ordinary LAN assumptions. The network address clears only the six host bits; the borrowed subnet bits remain part of the prefix.

**On screen:** Network .128; broadcast .191; Hosts .129–.190.

**Visual cue:** hosts. Clear host bits while preserving the complete 26-bit network prefix.


## 14. Subnet four: 192 through 255 — 00:04:28

The final block is 192.168.1.192 slash twenty-six. Its network address ends in 192, its broadcast ends in 255, and ordinary hosts run from 193 through 254. Together, the four ranges cover zero through 255 exactly once. Adjacent blocks touch at consecutive addresses, never at the same address.

**On screen:** Network .192; broadcast .255; Hosts .193–.254.

**Visual cue:** hosts. Nonoverlapping contiguous ranges verify the subdivision.


## 15. Locate the host ending in seventy — 00:04:48

Where does 192.168.1.70 slash twenty-six belong? Seventy falls in the sixty-four-through-127 interval, so its network is 192.168.1.64. Binary AND confirms it: 01000110 AND 11000000 gives 01000000, or sixty-four. Its broadcast is 127, so seventy is an ordinary host address within the second subnet.

**On screen:** 70 lies inside .64–.127; 01000110 AND 11000000 = 01000000.

**Visual cue:** mask. A range check and a mask operation should identify the same subnet.


## 16. Same prefix or a different subnet? — 00:05:07

Compare hosts ending in seventy and one hundred, both using slash twenty-six. Their masked network addresses are both sixty-four, so their addresses belong to the same subnet. A host ending in 130 instead masks to 128. Prefix comparison determines the local-versus-remote decision; the decimal appearance alone does not.

**On screen:** .70 and .100 share .64/26; .130 belongs to .128/26.

**Visual cue:** hosts. Compare masked network prefixes, using the relevant mask.


## 17. Remote destinations use a router — 00:05:28

In a typical IPv4 LAN, a host treats a destination in its own subnet as locally reachable and resolves the destination’s link-layer address. For a remote subnet it normally sends toward an appropriate router, often its default gateway. Subnetting changes that forwarding decision; it does not physically move the computers.

**On screen:** Local subnet: reach the destination; Remote subnet: use a next-hop router.

**Visual cue:** subnets. A gateway connects networks that have different prefixes.


## 18. Choose a prefix for fifty hosts — 00:05:49

Suppose each department needs fifty ordinary IPv4 LAN host addresses. Five host bits give thirty-two total addresses and usually thirty usable hosts, which is insufficient. Six host bits give sixty-four total and sixty-two usable, enough for fifty. Therefore slash twenty-six is the smallest equal-sized block meeting this specific requirement.

**On screen:** /27 usually gives 30 hosts; /26 usually gives 62 hosts.

**Visual cue:** hosts. Choose enough host bits for the requirement and reserved addresses.


## 19. More prefix bits, fewer addresses — 00:06:11

Increase the prefix by one bit and the address block halves. Decrease it by one bit and the block doubles, provided alignment and the available parent block permit it. Slash twenty-five holds 128 addresses, slash twenty-six sixty-four, and slash twenty-seven thirty-two. The direction becomes intuitive when you count variable bits.

**On screen:** Longer prefix → smaller block; /25:128; /26:64; /27:32.

**Visual cue:** bits. Every additional fixed bit halves the number of address combinations.


## 20. The subtract-two rule has exceptions — 00:06:32

Our sixty-two-host count follows ordinary IPv4 LAN conventions. Do not apply two to the host-bit count minus two blindly to every prefix. On appropriately configured point-to-point links, slash thirty-one uses both addresses as endpoints. Slash thirty-two denotes one address, commonly a host route. Context determines the correct interpretation.

**On screen:** Ordinary LAN rules have exceptions; /31 point-to-point; /32 one address.

**Visual cue:** hosts. The total-address formula is general; host usability depends on context.


## 21. A subnet is not a security policy — 00:06:53

Dividing an address block organizes addressing and routing. It does not automatically encrypt traffic, prevent unauthorized access, or guarantee isolation between departments. Those outcomes require appropriate routing, firewall, switch, and security configuration. A subnet can support a design, but the mathematical prefix calculation is only one part of implementing that design.

**On screen:** Address planning is not encryption; Isolation needs actual configuration.

**Visual cue:** subnets. A prefix boundary does not replace a security policy.


## 22. CIDR replaces the classful shortcut — 00:07:15

Older lessons classify address ranges as class A, B, or C. Modern classless addressing uses the explicit prefix length, so an address’s first octet alone does not establish its subnet boundary. Our 192.168.1 block is private address space; using it here does not make those addresses publicly routable on the Internet.

**On screen:** Use the explicit prefix length; 192.168.0.0/16 is private space.

**Visual cue:** bits. Read the actual prefix instead of guessing an old default class.


## 23. Check all four answers — 00:07:37

Read the completed table aloud: networks zero, sixty-four, 128, and 192; broadcasts sixty-three, 127, 191, and 255. Each block contains sixty-four total addresses. Each ordinary host range excludes its own first and last address. The sizes add to 256, and none of the four ranges overlap.

**On screen:** Four blocks of 64 addresses; Each ordinary LAN has 62 host slots.

**Visual cue:** subnets. Verify alignment, size, boundaries, and coverage before assigning addresses.


## 24. Move the boundary, solve the puzzle — 00:07:57

We turned one slash-twenty-four block into four slash-twenty-six subnets by fixing two additional bits. Six variable bits remain, yielding sixty-four addresses per block. Binary AND locates a host’s network, and host usability depends on the link’s conventions. Subnetting is now a boundary you can reason about, rather than a list to memorize.

**On screen:** Borrow 2 bits; retain 6 host bits; Networks: .0, .64, .128, .192.

**Visual cue:** subnets. Subnetting follows directly from fixed prefixes and variable address bits.
