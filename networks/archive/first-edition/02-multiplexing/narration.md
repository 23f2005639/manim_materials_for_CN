# Thousands of Messages, One Cable

English narration for your own voice. Planned runtime: 00:08:45.

The browser pauses after each section. The timestamps below refer to the continuous MP4.


## 01. Three senders, one cable — 00:00:00

Suppose three cameras each need to send video, but only one long cable is available. Buying a separate cable for every camera is not our only option. We can organize a shared link so the receiver separates the streams again. The key question is what resource distinguishes one channel from another.

**On screen:** Several independent streams; One shared physical link.

**Visual cue:** multiplex_intro. Multiplexing lets independent channels share a physical resource.


## 02. A medium is not a channel — 00:00:21

A medium is the physical path, such as a wire or fiber. A channel is a communication allocation within that path. Drawing three colored lanes does not mean three cables exist. The colors identify channels whose signals can be separated by some rule, such as frequency, time, or optical wavelength.

**On screen:** Physical path versus logical channel; Sharing needs a separation rule.

**Visual cue:** channels. One physical medium can carry multiple logical channels.


## 03. Combine, carry, separate — 00:00:43

Place a multiplexer at the transmitting side and a demultiplexer at the receiving side. The first combines the inputs according to an agreed scheme; the second uses that scheme to separate them. This is an architectural diagram, not a claim that all real systems need identical boxes or processing at either end.

**On screen:** MUX combines inputs; DEMUX recovers outputs.

**Visual cue:** mux_demux. Sharing works only if the receiving end can separate the streams.


## 04. Read a frequency picture — 00:01:05

Before frequency-division multiplexing, read the axes. Time describes when a signal changes. Frequency describes repeating change per second. A signal generally occupies a range of frequencies, not one infinitely thin line. We will draw simplified frequency bands, with their widths representing the channel bandwidth allocated to different information streams.

**On screen:** Frequency measures cycles per second; Bandwidth spans frequencies.

**Visual cue:** frequency. A frequency plot shows where signal energy is allocated.


## 05. Give every stream a band — 00:01:26

Frequency-division multiplexing assigns distinct frequency ranges to channels. All three cameras can use the shared medium at the same time, provided their signals fit their allocations and the equipment separates them adequately. The animation stacks colored bands along the frequency axis. It does not alternate the channels into different time slots.

**On screen:** Channels occupy different bands; They can transmit simultaneously.

**Visual cue:** fdm. FDM separates simultaneously active channels in frequency.


## 06. Leave room between neighbors — 00:01:48

Real signals and filters are imperfect. Adjacent channels may therefore need unused separation called guard bands. Think of these as margins in our allocation plan, not protective walls blocking all interference. More guard space can simplify separation, but it consumes spectrum that cannot simultaneously be assigned to useful channel bandwidth.

**On screen:** Real filters have imperfect edges; Guard bands reduce interference.

**Visual cue:** fdm_guard. Guard bands trade usable spectrum for easier channel separation.


## 07. Filter at the receiver — 00:02:10

At the far end, a filter selects the frequency region for one channel. Appropriate demodulation then recovers that channel's information. Follow the blue band through its filter while orange and green take separate paths. A filter cannot recover arbitrary overlapping streams merely because our diagram has painted them in different colors.

**On screen:** Select the desired band; Reject neighboring energy.

**Visual cue:** fdm_filter. A receiver can extract one frequency allocation with suitable filtering.


## 08. Work an FDM allocation — 00:02:31

Here is a simplified allocation calculation. Three channels each require twenty kilohertz, and two internal guard gaps each require five kilohertz. The required span is three times twenty plus two times five: seventy kilohertz. We are excluding outer margins and other overhead. The assumptions matter as much as the arithmetic here.

**On screen:** 3 × 20 kHz channels; 2 × 5 kHz internal guards.

**Visual cue:** fdm_allocation. Three 20 kHz channels plus two 5 kHz gaps need 70 kHz.


## 09. What happens when one is idle? — 00:02:53

Pause the green camera. Under our fixed FDM plan, its band stays reserved while the other bands continue. The unused band does not automatically belong to another camera. A more adaptive system could reassign resources, but that requires additional coordination. This simple example shows the tradeoff between predictable access and flexibility.

**On screen:** Fixed bands remain allocated; Idle capacity may go unused.

**Visual cue:** fdm_idle. A fixed allocation can waste capacity when its owner has nothing to send.


## 10. Now divide the time axis — 00:03:15

Instead of giving each camera a separate frequency band, let them take turns using the link. Time-division multiplexing separates transmissions along the time axis. The animation rotates the diagram: colored blocks now line up from left to right in time, rather than occupying stacked frequency bands at the same moment.

**On screen:** One shared frequency allocation; Different turns in time.

**Visual cue:** time_axis. TDM distinguishes channels by when they transmit.


## 11. Assign repeating time slots — 00:03:37

In synchronous TDM, a repeating schedule assigns slots to inputs. Camera A uses its turn, then B, then C, and the sequence begins again. During its slot, an input can use the relevant link capacity. The receiver must know the schedule to associate each arriving piece with the correct stream.

**On screen:** A, then B, then C; The pattern repeats.

**Visual cue:** tdm_slots. Synchronous TDM gives channels scheduled opportunities to transmit.


## 12. Understand a TDM frame — 00:03:58

One full cycle of slots is often called a TDM frame. That use of frame describes the multiplexing structure; do not confuse it automatically with an Ethernet frame. Our cycle contains one slot for each of three cameras. More elaborate systems may use unequal allocations, extra framing information, or multiple scheduling levels.

**On screen:** A frame contains one slot cycle; Frame here means a TDM cycle.

**Visual cue:** tdm_frame. A TDM frame groups the slots in one repeated schedule.


## 13. Keep the schedule aligned — 00:04:21

If the receiver loses track of slot boundaries, it may assign the wrong data to an output. Timing and framing mechanisms keep interpretation aligned. In our demonstration, deliberately shift the receiver's marker, notice the incorrect labels, then restore alignment. Sharing a clock picture is a teaching abstraction for that synchronization requirement.

**On screen:** Sender and receiver agree on slots; Framing supports correct alignment.

**Visual cue:** tdm_sync. Slot timing must be understood at both ends.


## 14. Work a TDM rate example — 00:04:42

Each camera produces two megabits per second continuously. Together they require six megabits per second of useful capacity. If the shared link serves three equal slots, each camera gets one third of its useful rate. Real framing and synchronization overhead mean the physical line rate may need to exceed that simple total.

**On screen:** 3 inputs × 2 Mb/s; At least 6 Mb/s before overhead.

**Visual cue:** tdm_rate. Three continuous 2 Mb/s streams require 6 Mb/s of useful link capacity.


## 15. The empty-slot problem — 00:05:05

Now camera B becomes idle. A fixed synchronous schedule can still preserve B's slot, creating an empty interval. Meanwhile, A may have data waiting. The schedule is simple and predictable, but not automatically efficient for bursty traffic. This is the time-domain counterpart of the unused fixed FDM band we saw earlier.

**On screen:** Scheduled turn may be empty; Other streams may still wait.

**Visual cue:** tdm_idle. Fixed TDM can leave a slot idle even when another input has data.


## 16. Allocate turns on demand — 00:05:27

Statistical multiplexing allocates resources according to demand instead of permanently reserving equal turns. In a simplified queue, active streams contribute labeled pieces that are scheduled onto the output. This can improve utilization for bursty sources, but queues and delays appear when demand exceeds capacity. Demand-based allocation does not create unlimited bandwidth.

**On screen:** Busy inputs get service; Labels or state identify the source.

**Visual cue:** statistical_tdm. Statistical sharing adapts to demand but needs coordination.


## 17. Move from copper to fiber — 00:05:49

An optical fiber carries light, with information encoded onto optical signals. We can exploit different carrier wavelengths to support separate channels. Our visible red, blue, and green beams are illustrations: practical optical channels often lie outside the visible spectrum. The colors help track wavelengths; they do not identify actual deployed channel colors.

**On screen:** Light carries encoded information; Fiber guides optical signals.

**Visual cue:** optical. Optical fiber supports channels carried on distinct wavelengths.


## 18. Combine different wavelengths — 00:06:11

Wavelength-division multiplexing combines several optical channels onto one fiber. Each channel has a different carrier wavelength and can carry an independent information stream. They coexist during transmission rather than waiting for our A, B, C time schedule. WDM is closely related to frequency division, expressed in the optical wavelength domain.

**On screen:** Independent optical carriers; One shared fiber.

**Visual cue:** wdm. WDM combines distinct wavelength channels on a fiber.


## 19. Separate the light again — 00:06:32

At the receiving end, wavelength-selective components separate the channels toward appropriate receivers. Follow each colored carrier into its output branch. The diagram shows the logical operation rather than a literal rainbow traveling down the fiber. Actual filters, transmitters, and receivers need suitable channel spacing and performance to recover the information reliably.

**On screen:** Wavelength-selective separation; Each output receives its channel.

**Visual cue:** wdm_demux. An optical demultiplexer separates wavelength channels at the destination.


## 20. Work a WDM capacity example — 00:06:54

Suppose four wavelength channels each carry ten gigabits per second. Their aggregate raw rate is forty gigabits per second. That sum assumes the channels and equipment can operate together as specified. Application throughput is lower after relevant overhead and operating constraints. One application's speed also depends on how traffic is assigned to channels.

**On screen:** 4 channels × 10 Gb/s; 40 Gb/s aggregate raw rate.

**Visual cue:** wdm_capacity. Four independent 10 Gb/s channels total 40 Gb/s before overhead.


## 21. Sharing has physical limits — 00:07:17

Adding more channels eventually encounters practical limits. Available spectrum, transmitter quality, receiver sensitivity, noise, and separation all matter; optical systems also have propagation and power-related constraints. Our clean diagrams suppress those details to reveal the organizing principle. Never interpret another colored stripe as a free capacity increase without engineering tradeoffs.

**On screen:** Noise and filtering still matter; Capacity is not unlimited.

**Visual cue:** multiplex_limits. Multiplexing organizes existing resources; it does not remove physical constraints.


## 22. Compare the three schemes — 00:07:38

Freeze the three diagrams together. FDM separates frequency allocations, TDM separates scheduled times, and WDM separates optical carrier wavelengths. Frequency and wavelength describe related physical properties, so WDM is not an unrelated miracle. These approaches can also be combined in a real system: a wavelength channel can itself carry time-multiplexed information.

**On screen:** FDM: frequency; TDM: time; WDM: optical wavelength.

**Visual cue:** multiplex_compare. Ask which dimension separates the channels.


## 23. Choose with the traffic in mind — 00:08:00

Return to our cameras. Continuous predictable streams may fit a fixed allocation well. Bursty traffic benefits from flexible sharing, provided buffering and scheduling are handled. Fiber makes optical wavelength choices possible, while other media have different constraints. No single technique wins every situation; compare the resources available and the traffic's requirements.

**On screen:** Predictable streams versus bursts; Medium and equipment constrain choices.

**Visual cue:** multiplex_choose. The useful choice depends on the medium, traffic, and coordination costs.


## 24. Retell the separation rule — 00:08:22

We started with several senders and one cable. The solution was not to merge their meanings into an unreadable mixture, but to preserve a recoverable separation rule. Point to each diagram and name that rule. Then solve the three numerical examples again, stating whether your result includes guards, framing, or other overhead.

**On screen:** Combine → transmit → separate; Identify the sharing dimension.

**Visual cue:** multiplex_recap. One cable can support several streams when their channels remain distinguishable.
