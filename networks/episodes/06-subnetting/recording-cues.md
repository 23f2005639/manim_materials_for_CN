# Recording cues — Subnetting You Can Actually See

Record one section at a time, or narrate the click-through presentation live.

Guide subtitles use planned timing. Match final subtitles to your recording after editing.

| Section | Start | Length | What to show | Recording cue |
|---|---|---|---|---|
| 01 | 00:00:00 | 21.63s | One network, four smaller networks | Subnetting divides an existing address block into smaller prefix blocks. |
| 02 | 00:00:21 | 20.33s | IPv4 addresses contain thirty-two bits | Dotted decimal is a readable way to write the underlying bits. |
| 03 | 00:00:41 | 21.60s | A prefix marks the shared beginning | The prefix length counts leading network bits, not decimal digits. |
| 04 | 00:01:03 | 19.90s | The mask expresses the boundary | A contiguous subnet mask and its prefix length describe the same boundary. |
| 05 | 00:01:23 | 21.63s | Find the network with bitwise AND | Masking an address identifies the prefix block that contains it. |
| 06 | 00:01:45 | 19.47s | Count the parent block | Count all addresses before applying ordinary LAN host reservations. |
| 07 | 00:02:04 | 19.90s | Borrow two bits for four subnets | Extending a prefix creates smaller blocks within the original block. |
| 08 | 00:02:24 | 20.33s | Build the slash-twenty-six mask | Two leading ones in the last octet make the /26 boundary. |
| 09 | 00:02:44 | 20.33s | Six host bits make sixty-four addresses | The four /26 blocks exactly cover the original /24. |
| 10 | 00:03:05 | 21.17s | The four binary prefixes | Aligned /26 network starts are separated by 64 addresses. |
| 11 | 00:03:26 | 19.90s | Subnet one: zero through sixty-three | Subnet one contains 64 total addresses and 62 ordinary host addresses. |
| 12 | 00:03:46 | 21.63s | Subnet two: sixty-four through 127 | Network and broadcast roles depend on the prefix, not just the last octet. |
| 13 | 00:04:07 | 20.77s | Subnet three: 128 through 191 | Clear host bits while preserving the complete 26-bit network prefix. |
| 14 | 00:04:28 | 20.33s | Subnet four: 192 through 255 | Nonoverlapping contiguous ranges verify the subdivision. |
| 15 | 00:04:48 | 18.60s | Locate the host ending in seventy | A range check and a mask operation should identify the same subnet. |
| 16 | 00:05:07 | 20.77s | Same prefix or a different subnet? | Compare masked network prefixes, using the relevant mask. |
| 17 | 00:05:28 | 21.60s | Remote destinations use a router | A gateway connects networks that have different prefixes. |
| 18 | 00:05:49 | 21.20s | Choose a prefix for fifty hosts | Choose enough host bits for the requirement and reserved addresses. |
| 19 | 00:06:11 | 21.63s | More prefix bits, fewer addresses | Every additional fixed bit halves the number of address combinations. |
| 20 | 00:06:32 | 20.77s | The subtract-two rule has exceptions | The total-address formula is general; host usability depends on context. |
| 21 | 00:06:53 | 22.07s | A subnet is not a security policy | A prefix boundary does not replace a security policy. |
| 22 | 00:07:15 | 22.03s | CIDR replaces the classful shortcut | Read the actual prefix instead of guessing an old default class. |
| 23 | 00:07:37 | 19.90s | Check all four answers | Verify alignment, size, boundaries, and coverage before assigning addresses. |
| 24 | 00:07:57 | 22.53s | Move the boundary, solve the puzzle | Subnetting follows directly from fixed prefixes and variable address bits. |
