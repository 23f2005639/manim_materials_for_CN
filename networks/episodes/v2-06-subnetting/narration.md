# Move Two Bits, Create Four Networks

English narration for your own voice. Planned runtime: 00:08:45.

The browser pauses after each section. The timestamps below refer to the continuous MP4.


## 01. One block, four networks — 00:00:00

Here is a block of two hundred and fifty-six addresses. We want four equal networks, with every address accounted for exactly once. Where should the boundaries go? Guessing decimal numbers makes this feel like a memorization exercise. But the boundaries come from a much simpler picture: some address bits stay fixed, and the others are free to change. We are going to move that dividing line and watch four networks appear.


## 02. Expose the thirty-two bits — 00:00:33

An IPv4 address contains thirty-two bits. We normally display them as four decimal numbers separated by dots, with eight bits represented by each number. Those eight-bit groups are called octets. Expand the final octet and the familiar address becomes a row of switches, each either zero or one. The dotted format is useful for reading. The bit view is useful for seeing which combinations belong to the same address block.


## 03. Fix the shared beginning — 00:01:06

In our example, the block is 192.168.1.0 slash twenty-four. Slash twenty-four says that the first twenty-four bit positions are fixed. Every address in the block shares that beginning. The final eight positions can change, giving us different addresses within the block. This boundary is what the prefix describes. It does not mean the address contains a slash bit; the slash is our way of stating how many positions are shared.


## 04. Count the free combinations — 00:01:39

Each free bit has two choices. Two free bits make four combinations; three make eight. Keep doubling until eight free bits give two to the power of eight, or two hundred and fifty-six combinations. In the final octet, they run from zero through two hundred and fifty-five. We have counted the entire block, including addresses with special roles. We will assign those roles after dividing the block into its smaller networks.


## 05. One new bit creates halves — 00:02:12

Move the boundary one position right. The first formerly free bit now identifies which half we mean: zero on one side, one on the other. Each half has seven free bits left, so each contains one hundred and twenty-eight addresses. The total has not changed. We have simply described the original space as two smaller blocks. A longer fixed prefix leaves fewer possibilities inside each individual block.


## 06. Two new bits create quarters — 00:02:44

Move the boundary once more. Each half splits in two, giving four groups identified by zero-zero, zero-one, one-zero, and one-one. Two additional fixed bits create two to the power of two subnets. Starting at slash twenty-four and adding two gives slash twenty-six. The prefix length, the number of groups, and the visible split are three views of the same operation. No address has been created or lost along the way.


## 07. Six bits remain inside each — 00:03:17

Each new subnet has six free host bits. Two to the power of six gives sixty-four addresses per subnet. Check the accounting: four subnets multiplied by sixty-four addresses equals our original two hundred and fifty-six. This is a useful way to catch a wrong boundary. If the groups overlap, leave gaps, or contain the wrong number of combinations, their totals will stop matching the space we started with.


## 08. Read the four starts — 00:03:49

Keep the six host bits at zero and change only the two subnet bits. Zero-zero begins at zero. Zero-one begins at sixty-four. One-zero begins at one hundred and twenty-eight. One-one begins at one hundred and ninety-two. Those are the four network starts in the final octet. Their spacing is sixty-four because each block contains sixty-four combinations. The decimal pattern comes directly from the binary positions, rather than a separate shortcut to memorize.


## 09. Turn the boundary into a mask — 00:04:23

A subnet mask marks fixed prefix positions with ones and the remaining positions with zeros. For slash twenty-six, the final octet begins one-one, followed by six zeros. The first two positions have values one hundred and twenty-eight and sixty-four. Add them and the mask's last octet is one hundred and ninety-two. The complete mask is 255.255.255.192. Now the mask and our moving boundary describe exactly the same division.


## 10. Find where seventy belongs — 00:04:55

Take the address 192.168.1.70. The final octet, seventy, is 01000110 in binary. Apply the mask 11000000 using bitwise AND. A mask one keeps the corresponding address bit; a zero clears it. The result is 01000000, or sixty-four. So this address belongs to 192.168.1.64 slash twenty-six. We did not search four separate lists. We removed the varying host part and exposed the subnet's shared beginning.


## 11. Give the endpoints their jobs — 00:05:25

On an ordinary LAN subnet, the address with all host bits zero identifies the network, and the address with all host bits one is its broadcast address. In a sixty-four-address block, those two roles leave sixty-two addresses for hosts. This is why total addresses and usable host addresses are different counts. We are applying the ordinary LAN convention in this example, rather than claiming that subtracting two is a universal rule for every possible prefix.


## 12. Read the first two ranges — 00:06:01

The first block spans zero through sixty-three. Its network is zero, its broadcast is sixty-three, and hosts use one through sixty-two. The second spans sixty-four through one hundred and twenty-seven. Its hosts use sixty-five through one hundred and twenty-six. Notice that this broadcast ends in one hundred and twenty-seven, not two hundred and fifty-five. Broadcast follows the host-bit pattern inside the chosen subnet, not a particular decimal ending.


## 13. Complete the remaining ranges — 00:06:33

The third block spans one hundred and twenty-eight through one hundred and ninety-one, with hosts between one hundred and twenty-nine and one hundred and ninety. The fourth spans one hundred and ninety-two through two hundred and fifty-five, with hosts from one hundred and ninety-three through two hundred and fifty-four. Watch their edges meet. Each block starts immediately after the previous block ends, covering the original parent without an overlap or a missing address.


## 14. Choose room for fifty hosts — 00:07:07

Suppose a network needs fifty host addresses. Five free bits give thirty-two total addresses, or thirty ordinary LAN host addresses, which is too small. Six free bits give sixty-four total and sixty-two usable, which fits. Thirty-two minus six leaves a slash-twenty-six prefix. Instead of starting with a memorized mask, we started with the required capacity and counted the combinations needed to accommodate it. The mask follows from that decision.


## 15. Check the boundary, not appearances — 00:07:40

Compare last-octet values seventy and one hundred. Masking each produces sixty-four, so they share this subnet. Now compare seventy with one hundred and thirty. The latter produces one hundred and twenty-eight, placing it in another subnet. Similar-looking decimal addresses are not the deciding evidence. Their fixed prefix bits are. When a result feels suspicious, return to the boundary and ask which bits were allowed to vary inside the block.


## 16. Four networks from two bits — 00:08:12

Return to the original block. Two borrowed positions created four subnet prefixes, and six remaining positions created sixty-four addresses in each. The starts, mask, broadcast boundaries, and host counts all came from that same division. They are not five unrelated rules. Subnetting becomes easier when the arithmetic stays connected to the picture: fix a longer beginning, count what remains free, and give each resulting address range its correct role.
