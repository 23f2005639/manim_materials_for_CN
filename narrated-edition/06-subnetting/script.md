# Move Two Bits, Create Four Networks

## 01. A device needs an address

Subnetting can look like a wall of numbers. But underneath, it starts with a beautifully small choice: zero or one. First, let's see why computers need addresses at all. Each needs an address, a little like a house number. Here we use IPv4 addresses, written as four numbers with dots between them. Watch a message go to the computer marked 192.168.1.20. Our question today is how to divide one collection of these addresses into smaller groups. That division is called subnetting.

## 02. Start with one tiny choice

Before dividing anything, meet the smallest building block: a bit. A bit can be zero or one. Think of a switch with just two positions. Put eight bits side by side and they can represent one of the numbers in our address. All four numbers together use thirty-two bits. The dots make the address easier for people to read; underneath, it is a row of zeros and ones. We will mostly watch the final eight positions.

## 03. Keep the beginning the same

Look at these addresses: they all start with 192.168.1, while the last number changes. Those first three numbers use twenty-four bits. If we keep those bits fixed, we get one group with eight positions left to change. We write the group as 192.168.1.0 slash twenty-four. The slash tells us how many beginning bits stay fixed. That shared beginning is called a prefix. It is simply the part every address in this group has in common.

## 04. Count the possible endings

One free bit has two choices: zero or one. Two free bits have four: zero-zero, zero-one, one-zero, one-one. Every extra free bit doubles the choices. Keep doubling until eight bits give two hundred and fifty-six possibilities. We write that as two to the power of eight. The final number can therefore run from zero through two hundred and fifty-five. Zero counts as a possibility too. Now we know the size of the group we are about to divide.

## 05. Split the group in half

Take the first of those eight free bits and use it to choose a side. Zero means the left half; one means the right half. Seven bits are still free inside each half, giving one hundred and twenty-eight addresses apiece. Each smaller group now shares twenty-five beginning bits, so we call it slash twenty-five. Nothing new has been added. The same addresses have been sorted into two groups, just as one drawer can be divided into two compartments.

## 06. Split each half again

Use one more bit to split each half. Now the group labels are zero-zero, zero-one, one-zero, and one-one. Two choices followed by two choices make four groups. These smaller address groups are our subnets. Each shares twenty-six beginning bits, so each is slash twenty-six. This is why moving the boundary just two places turns one network's address block into four smaller blocks. The labels may look technical, but underneath we have only made two yes-or-no choices.

## 07. Count what each group holds

We started with eight free positions and used two to choose a group. That leaves six positions to choose addresses inside each group. These are called host bits; a host is a device using an address. Six free bits give sixty-four combinations. Check our work: four groups times sixty-four addresses equals two hundred and fifty-six, exactly where we began. A longer shared beginning makes each individual group smaller, because fewer bits remain free to change.

## 08. Find where each group starts

Put zeros in all six positions inside each group. That gives its first address. Change only the two group bits and watch the starts appear: zero, sixty-four, one hundred and twenty-eight, one hundred and ninety-two. We only show the last number here; 192.168.1 stays the same throughout. Why do the starts jump by sixty-four? Each group occupies sixty-four places. The next group starts immediately after those places finish. We can count the spaces instead of memorizing four special numbers.

## 09. Make a stencil for the boundary

A computer needs a way to mark which bits belong to the shared beginning. We use a mask, like a stencil: ones mark the shared positions, zeros mark the changing positions. Our first twenty-four bits are shared, plus two more in the final group of eight. That last pattern is one-one followed by six zeros. The first two positions are worth one hundred and twenty-eight and sixty-four. Add them to get one hundred and ninety-two. Our mask is 255.255.255.192.

## 10. Where does address seventy belong?

Try the address ending in seventy. In bits, seventy is zero-one-zero-zero-zero-one-one-zero. Place our mask underneath it. Keep an address bit where the mask has a one; replace it with zero where the mask has a zero. This operation is called AND. The answer is zero-one followed by six zeros: sixty-four. So seventy belongs to the group starting at sixty-four. The mask has erased the individual device's part and left the group's starting address behind.

## 11. Two addresses have special jobs

Can we give all sixty-four addresses to computers? In this ordinary local network example, two have other jobs. The first address names the whole subnet. The last is the broadcast address, used for a message addressed to everyone in that subnet. That leaves sixty-two device addresses: sixty-four minus two. Remember what we counted before: total addresses, not just device addresses. Some special network arrangements use different rules, so we are applying this subtraction to our ordinary local network example.

## 12. Read the first two groups

The first group runs from zero to sixty-three. Reserve zero for the network and sixty-three for broadcast. Computers use one through sixty-two. The next group runs from sixty-four to one hundred and twenty-seven. Reserve those endpoints, leaving sixty-five through one hundred and twenty-six for computers. Follow the colored ends of each bar as we name their jobs. Broadcast does not always end in two hundred and fifty-five. It is the final address of the particular subnet we chose.

## 13. Finish the address map

The third group starts at one hundred and twenty-eight and ends at one hundred and ninety-one. Its device addresses sit between those endpoints. The fourth starts at one hundred and ninety-two and ends at two hundred and fifty-five, again with the middle addresses available for devices. Look across all four bars. They fit together without gaps or overlaps. Every address from our original group has a place, and each smaller group follows the same rule for its two endpoints.

## 14. Choose enough room for devices

Suppose one group needs fifty computers. How much room should we leave? Five free bits give thirty-two total addresses. After the two special ones, only thirty remain. Too small. Six free bits give sixty-four total and sixty-two for devices. That fits. An IPv4 address has thirty-two bits, so leaving six free means fixing twenty-six: slash twenty-six. We chose the size by counting the room needed. The slash number followed from that choice, rather than appearing from nowhere.

## 15. Check whether two devices match

Do addresses ending in seventy and one hundred belong together? Our mask sends both to the group starting at sixty-four, so yes. What about seventy and one hundred and thirty? The second one belongs to the group starting at one hundred and twenty-eight. They are in different subnets. This is why the mask matters alongside the address. Seeing the same first three dotted numbers is not enough: our smaller groups share two more bits after those first twenty-four.

## 16. One boundary explains the numbers

We started with computers needing addresses. Those addresses became rows of bits, and bits gave us simple choices. Keep a beginning fixed, then count the endings that can change. Using two more bits for group labels made four subnets, each with sixty-four addresses. The starts, the mask, and the device counts all came from that one division. Subnetting looks like a page of mysterious numbers until you see the picture underneath: one collection, a movable boundary, and smaller groups.
