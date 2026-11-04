# A Lock Anyone Can Close, but Only You Can Open

English narration for your own voice. Planned runtime: 00:09:44.

The browser pauses after each section. The timestamps below refer to the continuous MP4.


## 01. Who can read this message? — 00:00:00

Suppose you send a friend a private message: meet at seven. On its journey, someone else might see the data. If the message is readable, that person can read it too. So we want to change it into something they cannot understand, then let our friend change it back. That process is encryption. A simple approach uses a shared secret. But here is a puzzle: how do we send privately to someone before we have shared that secret?


## 02. A lock with two different jobs — 00:00:36

Picture your friend handing out open padlocks while keeping the opening key. Anyone can put a message in a box and snap a lock shut. Only your friend can open it. RSA uses a mathematical version of two different jobs: a public rule for encrypting and a private rule for recovering the message. Computers represent messages as numbers, so our tiny demonstration will protect the number seven. The padlock is an analogy; the real work will be arithmetic.


## 03. Keep what is left over — 00:01:13

Before any keys, we need one easy operation: a remainder. Put eleven counters into groups of five. Two full groups use ten counters, leaving one. Eleven divided by five has remainder one. The short mathematical name is modulo: eleven mod five equals one. We will later use groups of fifty-five, but the idea is identical. Keep what is left after removing complete groups. No mysterious new kind of number, just the leftover amount.


## 04. Build the number fifty-five — 00:01:47

Choose five and eleven. Both are prime numbers: whole numbers greater than one that divide evenly only by one and themselves. Primes act like building blocks for multiplication. Multiply our two choices and we get fifty-five. That becomes the number we will use when keeping remainders. We call it n, simply a short label. Our public instructions will include fifty-five. The two factors, five and eleven, help us build the private instructions. These tiny numbers are for seeing the idea.


## 05. Find a useful repeating structure — 00:02:24

Why did we keep those two factors? They help describe a repeating pattern in the remainder arithmetic. Look at the numbers from zero through fifty-four. Cross out multiples of five and multiples of eleven. Forty positions remain. None of those shares a factor with fifty-five except one. For these primes, we can count them as four times ten: forty. Keep that number nearby. We will use its repeating structure to choose two operations that work together, rather than guessing a secret.


## 06. The public rule repeats a multiplication — 00:03:02

Let our public instruction be: multiply three copies of the message number together, then keep the remainder after dividing by fifty-five. Three copies multiplied together is called the third power, or cubing. We label that power e, and choose e equal to three. The public key is just the pair fifty-five and three. Why this choice? Three and our count of forty share no factor above one, which lets us find a matching private power next.


## 07. Choose a matching private rule — 00:03:38

Now find a number which, when multiplied by three, leaves one after removing complete groups of forty. Twenty-seven works. Three times twenty-seven is eighty-one, and eighty-one is forty plus forty plus one. We label the matching private power d, so d is twenty-seven. Notice the important part: this number was chosen to fit the public operation. It is not an unrelated password. The relationship between three, twenty-seven, and forty is what will let the two operations cooperate.


## 08. Turn seven into thirteen — 00:04:14

Time to send our tiny message, seven. Follow the public rule: seven times seven times seven is three hundred and forty-three. Remove complete groups of fifty-five. Six groups account for three hundred and thirty, leaving thirteen. That leftover number is the encrypted result, also called ciphertext. Seven has become thirteen. Anyone with the public pair fifty-five and three can perform this forward calculation. We have now watched encryption happen, using only multiplication and keeping a remainder.


## 09. Keep the numbers manageable — 00:04:50

The private rule asks us to use a much bigger power. Must we write an enormous number first? Happily, no. We can keep remainders while calculating. Start with thirteen. Square it, meaning multiply it by itself: one hundred and sixty-nine leaves four after division by fifty-five. Square that four to get sixteen. Square sixteen and keep its remainder, thirty-six. Each step keeps the same useful remainder information while preventing the working numbers from growing without limit.


## 10. Bring the message back — 00:05:25

Now use the private power, twenty-seven. We can split it into sixteen plus eight plus two plus one. The boxes show the remainders of thirteen raised to those powers. Multiply those values together, keeping the remainder after each step. Watch the result settle on seven. We recovered the original message. Written compactly, thirteen to the power twenty-seven, mod fifty-five, equals seven. The arithmetic looks longer than encryption, but it uses the same two actions: multiply and keep a remainder.


## 11. Why the pair fits together — 00:06:02

The interesting question is why seven returns. For numbers such as seven, which share no factor with fifty-five except one, these powers have a repeating structure linked to our count of forty. Encrypting with power three and decrypting with power twenty-seven combines into power eighty-one. That is one plus two times forty. The matching construction brings us back to the original value. The circle illustrates repetition; it is not a claim that every message takes exactly forty steps to repeat.


## 12. Try the wrong private number — 00:06:40

What if we replace twenty-seven with a guess? Use five instead. The same encrypted number thirteen now produces forty-three, not seven. The right side uses twenty-seven and recovers seven. So the private rule is not simply any large number or any secret number. It must fit the public construction. This small experiment does not prove security. It shows what correctness requires: the intended pair must undo the message transformation, while an arbitrary guess generally does not.


## 13. What must remain hard? — 00:07:15

Our public key contains fifty-five, but not its two prime factors. If someone discovers five and eleven, they can repeat our private-key construction: calculate forty, then find the matching power twenty-seven. For fifty-five that is easy, which is why this example protects nothing. Real RSA uses far larger carefully generated primes. Multiplying them is practical, while recovering their factors from the product is intended to be difficult. The security depends on such mathematical assumptions and on correct implementation.


## 14. The tiny example needs boundaries — 00:07:52

There is another reason not to use our little calculation directly as real encryption. Encrypt seven twice with this bare rule and thirteen appears twice. That visible repetition can leak information. Practical encryption needs a complete, carefully designed encoding scheme that adds the right structure and randomness before the RSA operation. We are looking inside one mathematical mechanism, not building a safe messaging app. The small numbers let us understand the moving parts without pretending that understanding alone makes them secure.


## 15. Connect the two kinds of rules — 00:08:30

Step back from the arithmetic. With a shared-secret method, the people communicating must have a suitable secret in common. With this public-key arrangement, the receiving person can publish the encrypting instructions and keep the recovery instructions private. The private key is related to the public key, but should be impractical to derive from it. That last condition matters. Publishing an operation is useful only if seeing how to perform it does not make recovering the private operation easy.


## 16. Rebuild the idea from the start — 00:09:06

We wanted to send a private message without first handing the sender our opening secret. The lock picture suggested separate public and private jobs. Our tiny RSA example made those jobs concrete: seven became thirteen using the public pair fifty-five and three; thirteen returned to seven using the private power twenty-seven. Remainders kept the arithmetic inside a limited set of values. The carefully chosen relationship made recovery work. That is the idea beneath RSA: shared public instructions, paired with private recovery.
