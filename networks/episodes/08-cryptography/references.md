# References — Sending Secrets Without Sharing a Secret First

Sources checked while writing the teaching script; narration is original.

- [RFC 9180 — Hybrid Public Key Encryption](https://www.rfc-editor.org/rfc/rfc9180) — Introduces hybrid asymmetric/symmetric designs and KEM/KDF/AEAD composition. Episode distinguishes its conceptual wrapped-key teaching model from exact HPKE.
- [RFC 5116 — An Interface and Algorithms for Authenticated Encryption](https://www.rfc-editor.org/rfc/rfc5116) — AEAD confidentiality/integrity interface, authentication failure, and scheme-specific nonce requirements.
- [RFC 8446 — TLS 1.3](https://www.rfc-editor.org/rfc/rfc8446) — TLS1.3 uses authenticated key establishment and AEAD; static RSA key transport removed. Used to distinguish the simplified diagram from modern TLS.

Animation engine: [ManimGX instructions](https://manimgx.academa.ai/llms.txt).
