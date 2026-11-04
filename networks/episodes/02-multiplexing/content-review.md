# Content review — Multiplexing

Independent review of the narration and current diagram source.

- FDM worked allocation independently calculated: 3 × 20 kHz + 2 × 5 kHz = 70 kHz, excluding outer margins.
- TDM example independently calculated: three continuous 2 Mb/s sources need 6 Mb/s useful capacity before framing overhead.
- WDM example independently calculated: four 10 Gb/s channels total 40 Gb/s raw aggregate capacity, not guaranteed per-application throughput.
- Frequency/wavelength relationships, fixed reservations, statistical sharing, synchronization and non-visible optical wavelengths are distinguished explicitly.

Requested diagram corrections: replace previous 11 kHz FDM diagram with the script's 70 kHz allocation; show variable active-source slots for statistical TDM; show four wavelength channels in the four-channel worked example. Resolved in the visual source and confirmed by the visual agent; final-render inspection is a separate coordinator check.

Sources: checked Purdue/Washington teaching material and NPTEL/UCSB optical material are recorded in `storyboard.json`. Examples are deliberately idealized and do not claim deployed link specifications.
