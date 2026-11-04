# A Lock Anyone Can Close, but Only You Can Open

English narration for your own voice. Planned runtime: 00:09:22.

The browser pauses after each section. The timestamps below refer to the continuous MP4.


## 01. The public lock puzzle — 00:00:00

Imagine publishing a lock that anyone can use to protect a message for you, while keeping the ability to open it to yourself. That sounds backwards if locking and unlocking require exactly the same secret. RSA makes the two operations different. We will build a tiny numerical example, watch a message change, and then recover it. The numbers are deliberately small enough to see; they are a teaching model, not a secure encryption system.


## 02. Easy forward, difficult backward — 00:00:34

The public-key idea begins with an imbalance. Some calculations are easy to perform when you have the inputs, while reversing the result can be much harder without extra information. Multiplying two large primes is straightforward compared with recovering those primes from their product. RSA connects that hidden structure to a reversible message transformation. We will not pretend that multiplying numbers alone encrypts a message. The important part is how the product supports two related exponent operations.


## 03. Numbers that wrap around — 00:01:10

Before the keys, meet the arithmetic. On this circle, counting past the final position wraps back to zero. Modulo fifty-five means keeping the remainder after division by fifty-five. Fifty-six lands at one, and one hundred and eleven also lands at one. Very different ordinary numbers can occupy the same position after wrapping. RSA uses this kind of modular arithmetic, so enormous powers can be handled through their remainders rather than written out in full.


## 04. Choose two small primes — 00:01:45

Choose five and eleven as our two primes. Their product is fifty-five, which becomes the modulus, n. That number is public. The prime factors are the extra structure we keep private when constructing a real key. Our example is intentionally easy to factor, so do not confuse visible small numbers with actual security. They let us inspect the mechanism. Larger keys make the underlying problem harder, but correct schemes need more than large numbers alone.


## 05. Count the useful positions — 00:02:20

Between zero and fifty-four, some positions share a factor with fifty-five. Highlight multiples of five, then multiples of eleven. The positions left over are relatively prime to fifty-five: their greatest common divisor with it is one. There are forty such positions. For distinct primes, that count is five minus one, multiplied by eleven minus one: four times ten. This count, called phi of n, helps us choose the relationship between the two exponents.


## 06. Choose the public exponent — 00:02:54

Let the public exponent e be three. It must have a suitable inverse modulo our count of forty; three and forty are relatively prime, so that inverse exists. Publishing n and e gives the pair fifty-five and three. Someone protecting a message uses the public exponent operation with this modulus. Knowing the public numbers is expected. The system's intended security does not depend on keeping the public algorithm or the public key out of view.


## 07. Find the matching private exponent — 00:03:29

We need a private exponent d whose product with three leaves remainder one when divided by forty. Twenty-seven works: three times twenty-seven equals eighty-one, and eighty-one is one plus two times forty. So d is twenty-seven. Keep that relationship in view. The private operation is not an ordinary division by three. These exponents cooperate through modular arithmetic and the structure established by the prime factors, which is why the wrapping picture matters.


## 08. Encrypt the message seven — 00:04:03

Represent our message by the number seven. Raise it to the public exponent three: seven cubed is three hundred and forty-three. Divide by fifty-five and keep the remainder. Six lots of fifty-five make three hundred and thirty, leaving thirteen. That thirteen is our ciphertext in this toy example. Anyone with the public pair can perform this calculation. The interesting question is how the private exponent will recover seven from thirteen without ordinary cube-root arithmetic.


## 09. Keep the remainder as you go — 00:04:38

Huge exponents look intimidating if we imagine writing the entire power first. We do not have to. After a multiplication, keeping the remainder preserves what matters for subsequent modular multiplication. Follow the moving number around the fifty-five-position circle. It wraps, returns, and wraps again, while the remainder stays small. This is the intuition behind efficient modular exponentiation: repeatedly calculate with manageable remainders instead of carrying a giant ordinary integer all the way to the end.


## 10. Decrypt using twenty-seven — 00:05:13

Now apply the private exponent: thirteen to the power of twenty-seven, modulo fifty-five. The calculation returns seven. We have recovered the original message using a different exponent from the one that protected it. The public side used three; the private side used twenty-seven. Watch the ciphertext marker return to the message position. That reversal is the behavior our key construction was designed to produce, rather than an accidental property of one unconnected formula.


## 11. Why those exponents cooperate — 00:05:48

For our message, which is relatively prime to fifty-five, the modular powers follow a repeating structure tied to the forty valid positions. Because the two exponents multiply to one plus a multiple of forty, applying them together returns the starting message. The animation shows that return, while the equation summarizes it. This is intuition for the mechanism, not a full number-theory proof. Our choice of message seven lets the relationship appear cleanly in the small example.


## 12. Test the wrong exponent — 00:06:23

Replace the private exponent with a guess. The same ciphertext generally lands somewhere else, rather than returning to seven. This makes the relationship between the exponents visible: the private operation is carefully chosen, not simply any different calculation. In this tiny example someone could quickly try all the possibilities, which is another reason it offers no security. The drawing demonstrates a mathematical construction. It does not demonstrate resistance to a determined attacker using realistic equipment.


## 13. What the hidden factors reveal — 00:06:58

If someone factors fifty-five into five and eleven, they can calculate our count of forty and find a matching private exponent. That is why the factorization matters. In real RSA, the public modulus is vastly larger, and recovering its factors is intended to be computationally difficult for classical attackers using appropriate parameters. Factoring is a known way to recover the private information; we are not claiming every imaginable RSA attack must literally follow this exact route.


## 14. Textbook numbers are not enough — 00:07:34

Our calculation directly transformed a small message number. Real encryption requires a suitable, carefully specified encoding and padding scheme, along with correct implementations and secure key handling. Repeating these tiny textbook operations is not a recipe for protecting personal messages. Keep the mathematical insight without mistaking the demonstration for deployable cryptography. Publishing a pair of numbers safely depends on the complete scheme, not only on whether a cube followed by another power returns the expected remainder.


## 15. Why this mathematics still matters — 00:08:10

Interest in quantum-resistant cryptography makes these assumptions worth understanding. A sufficiently capable future quantum computer could threaten RSA's underlying problem, which is one reason organizations are preparing transitions. That does not mean our video has shown such a computer breaking a deployed key today. The lesson here remains RSA itself: identify what the public operation reveals, what the private structure enables, and which assumptions make the difference between an easy demonstration and a security claim.


## 16. Return to the public lock — 00:08:45

We can now replace the lock metaphor with something precise. The public pair fifty-five and three transformed seven into thirteen. The private exponent twenty-seven transformed thirteen back into seven. Prime factors helped construct the exponent relationship, and modular arithmetic made the two operations fit together. Anyone can perform the public calculation, while the intended private capability depends on information we keep. The remarkable idea is not hiding the instructions. It is publishing one useful operation without publishing its intended inverse.
