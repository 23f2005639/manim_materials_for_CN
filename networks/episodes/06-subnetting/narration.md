# Subnetting You Can Actually See

English narration for your own voice. Planned runtime: 00:08:20.

The browser pauses after each section. The timestamps below refer to the continuous MP4.


## 01. One block, four networks — 00:00:00

This block contains 256 addresses. We want four separate networks, with no gaps and no overlap. How can a few extra bits create all four boundaries? Watch what happens when we move one dividing line.


## 02. Unpack thirty-two bits — 00:00:21

An IPv4 address contains thirty-two bits, displayed as four decimal octets. Each octet represents eight bits. The familiar dotted form makes the number readable, but the block structure becomes much clearer when we expose the bits underneath.


## 03. Move the prefix boundary — 00:00:41

Slash twenty-four fixes the first twenty-four positions. The last eight may vary, so every address in this block shares the same beginning. A prefix describes that common part and tells us which remaining combinations belong together.


## 04. Build the mask — 00:01:03

A mask makes this boundary explicit: ones mark the fixed prefix positions; zeros mark the changing positions. For slash twenty-four, the mask is 255.255.255.0. The decimal form is simply another view of those thirty-two bits.


## 05. AND reveals the network — 00:01:23

To extract the network, apply bitwise AND. A mask one keeps the address bit; a zero clears it. Applying this mask to 192.168.1.42 leaves 192.168.1.0. The variable part disappears, exposing the common prefix.


## 06. Count every combination — 00:01:45

Eight variable bits allow two to the power of eight combinations: 256 addresses. In the last octet, that's zero through 255. This counts every address in the block, before assigning any special network or broadcast roles.


## 07. Borrow two bits — 00:02:04

Fix one more bit and the possibilities split in half. Fix a second and each half splits again. Four subnets require two extra prefix bits, moving our boundary from slash twenty-four to slash twenty-six.


## 08. Two ones become 192 — 00:02:24

The last octet of the new mask begins with two ones. Their values are 128 and sixty-four, totaling 192. Six zeros follow. That's why the complete slash-twenty-six mask becomes 255.255.255.192, rather than an arbitrary number to memorize.


## 09. Six bits remain — 00:02:44

Six bits remain free inside each subnet. They produce sixty-four addresses. Four times sixty-four gives the original 256, which is a useful consistency check: moving the boundary divides the existing space without changing its total size.


## 10. Cycle the subnet bits — 00:03:05

The two new subnet bits can be zero-zero, zero-one, one-zero, or one-one. With all host bits cleared, those prefixes begin at zero, sixty-four, 128, and 192. Four binary choices create four evenly spaced boundaries.


## 11. First block boundaries — 00:03:26

The first subnet covers last-octet values zero through sixty-three. On an ordinary LAN, zero identifies the network and sixty-three is broadcast. Hosts use one through sixty-two: sixty-two usable addresses within a sixty-four-address block.


## 12. Second block boundaries — 00:03:46

The second subnet starts at sixty-four and ends at 127. Hosts occupy sixty-five through 126. Notice the broadcast ends in 127 here. Its identity comes from all host bits being one, not from always ending in 255.


## 13. Third block boundaries — 00:04:07

The third prefix begins at 128 and covers through 191. Its ordinary host range is 129 through 190. The calculation hasn't changed; the fixed subnet bits have moved us into the next group of sixty-four combinations.


## 14. Fourth block boundaries — 00:04:28

The fourth block runs from 192 through 255, with hosts from 193 through 254. Together, the four ranges cover the parent exactly once. Their boundaries meet cleanly, and each address belongs to just one subnet.


## 15. Locate address seventy — 00:04:48

Where does seventy fit? Its binary last octet is 01000110. AND with 11000000 leaves 01000000: sixty-four. So 192.168.1.70 lies in 192.168.1.64 slash twenty-six. The mask finds the block directly, without searching a table.


## 16. Compare the masked prefixes — 00:05:07

Seventy and one hundred share that sixty-four prefix. Address 130 belongs to the block starting at 128. Similar decimal addresses can cross a subnet boundary; masking both addresses reveals whether their network portions actually match.


## 17. Local or routed? — 00:05:28

That boundary affects delivery. A host normally reaches a destination in its own subnet locally; another subnet needs a suitable next-hop router. This is a logical addressing decision, independent of whether the devices occupy different physical rooms.


## 18. Make room for fifty hosts — 00:05:49

Suppose the network needs fifty host addresses. Slash twenty-seven offers thirty usable addresses on an ordinary LAN, which isn't enough. Slash twenty-six offers sixty-two. Work backward from the required capacity to choose the smallest suitable block.


## 19. Longer prefix, smaller block — 00:06:11

Every extra fixed prefix bit halves the remaining combinations. Slash twenty-five gives 128 total addresses, slash twenty-six sixty-four, slash twenty-seven thirty-two. Longer prefixes mean smaller blocks because fewer positions remain free to change.


## 20. Know the exceptions — 00:06:32

Subtracting two is useful for ordinary LAN subnets, but isn't universal. Suitable slash-thirty-one point-to-point links can use both addresses; slash thirty-two identifies a single address. The address roles depend on the network's purpose and prefix.


## 21. A prefix is not security — 00:06:53

A subnet boundary doesn't itself encrypt traffic or forbid crossing. Routing and access policies determine which communication is allowed. Splitting an address block organizes delivery; protection requires the relevant security mechanisms as well.


## 22. Read the actual prefix — 00:07:15

Modern classless addressing uses the supplied prefix, rather than guessing a class from the first octet. Also, our 192.168.1 block uses private addresses. It illustrates internal network organization, rather than a globally routable public block.


## 23. Verify the four ranges — 00:07:37

Check the four starts: zero, sixty-four, 128, 192. Each broadcast sits one below the next boundary, ending at 255 for the last block. Equal block sizes and clean boundaries let us verify the entire split together.


## 24. The boundary explains everything — 00:07:57

Two bits created four prefixes; six remaining bits created sixty-four addresses per prefix. Masks, ranges, and host counts all follow from that same boundary. Once you see the division, the separate-looking rules become consequences of one picture.
