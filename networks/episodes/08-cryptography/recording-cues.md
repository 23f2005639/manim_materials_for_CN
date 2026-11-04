# Recording cues — Sending Secrets Without Sharing a Secret First

Record one section at a time, or narrate the click-through presentation live.

Guide subtitles use planned timing. Match final subtitles to your recording after editing.

| Section | Start | Length | What to show | Recording cue |
|---|---|---|---|---|
| 01 | 00:00:00 | 22.37s | A secret on a public network | A public network needs more than a promise that nobody is listening. |
| 02 | 00:00:22 | 21.90s | Plaintext becomes ciphertext | Encryption conceals content through a keyed transformation. |
| 03 | 00:00:44 | 22.80s | The algorithm can be public | Protect the key rather than relying on an unknown algorithm. |
| 04 | 00:01:07 | 22.33s | Symmetric encryption uses a shared secret | A symmetric key must remain secret from unauthorized parties. |
| 05 | 00:01:29 | 22.80s | A key is not simply a memorable password | Use appropriate key generation rather than a memorable homemade key. |
| 06 | 00:01:52 | 21.90s | The key-distribution problem | Secure encryption still needs a sound way to establish or distribute keys. |
| 07 | 00:02:14 | 24.07s | Give Bob a pair of keys | A public/private key pair assigns different capabilities to each key. |
| 08 | 00:02:38 | 21.50s | Publish the encryption key | Public-key distribution and public-key authentication are different problems. |
| 09 | 00:02:59 | 22.80s | Encrypt to Bob’s public key | Use a suitable scheme and the intended recipient’s authenticated public key. |
| 10 | 00:03:22 | 21.90s | Decrypt with the private key | Protecting private keys is part of protecting the communication. |
| 11 | 00:03:44 | 20.63s | Why not encrypt every file this way? | Hybrid designs combine complementary capabilities. |
| 12 | 00:04:05 | 22.80s | Generate a fresh session key | A hybrid example begins with appropriate session key material. |
| 13 | 00:04:27 | 21.07s | Protect the data with the session key | Authenticated symmetric encryption protects the bulk message. |
| 14 | 00:04:48 | 22.33s | Protect the session key for Bob | Protect the session key separately from the bulk ciphertext. |
| 15 | 00:05:11 | 21.50s | Send the two protected pieces | Ciphertext can conceal content while revealing other communication patterns. |
| 16 | 00:05:32 | 21.93s | Bob recovers the key, then the message | A hybrid receiver verifies the protected data before accepting its contents. |
| 17 | 00:05:54 | 21.47s | Secrecy alone does not detect tampering | Encryption and integrity are related but distinct security goals. |
| 18 | 00:06:16 | 21.93s | An authentication tag checks the package | Authenticated encryption detects invalid protected packages. |
| 19 | 00:06:38 | 21.50s | Do not reuse nonces carelessly | Correct nonce handling is essential to secure authenticated encryption. |
| 20 | 00:06:59 | 21.50s | A substituted public key changes everything | A public key is useful only with an appropriate trust decision. |
| 21 | 00:07:21 | 22.77s | Confidentiality is not a sender’s signature | Recipient confidentiality does not automatically authenticate the sender. |
| 22 | 00:07:43 | 22.37s | How this differs from modern TLS | Use the hybrid idea to understand protocols without confusing their mechanisms. |
| 23 | 00:08:06 | 21.47s | Use established cryptographic protocols | A sound implementation must preserve the whole protocol’s security assumptions. |
| 24 | 00:08:27 | 22.40s | Solve the secrecy puzzle | Secure communication combines confidentiality, integrity, and sound key handling. |
