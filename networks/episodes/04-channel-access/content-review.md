# Content review — Channel access

Independent review of the narration and diagram source.

- Pure ALOHA vulnerable period 2T and slotted period T are stated only for the ideal equal-frame model.
- The ideal maxima 1/(2e) ≈ 18.4% and 1/e ≈ 36.8% are tied to Poisson attempts, not presented as measured Wi-Fi efficiency.
- Carrier sensing remains local and cannot eliminate propagation-delay collisions.
- One-persistent, nonpersistent and slotted p-persistent decisions are distinguished from Ethernet collision backoff.
- Binary exponential backoff choices are independently checked: after collision 1 choose 0..1; after collision 2 choose 0..3. These are Ethernet timing units, not ALOHA frame slots.
- CSMA/CD is explicitly historical shared half-duplex Ethernet. Switched full duplex and Wi-Fi avoidance are distinguished; no universal collision-detection claim.

Requested diagram correction: slotted ALOHA frame boxes must fit a single slot; colliding stations should use the same slot, with a later independent successful slot. Resolved in the visual source and confirmed by the visual agent; final-render inspection is a separate coordinator check.

Sources: checked university teaching references are recorded in `storyboard.json`. Efficiency assumptions and physical-context distinctions remain visible; exact hardware timing is outside the toy example.
