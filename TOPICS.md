# Eight standalone networking stories

Each video answers one question with original YouTube narration, purposeful animation and intuitive mathematics. Every lesson has 16 self-paced phases, a continuous MP4 and separate phase clips. Record the narration in your own voice.

| # | Topic | Video | Runtime | Script |
|---|---|---|---|---|
| 01 | dns | Why Can Your Internet Work While Your Apps Don’t? | 9:08 | [Read](networks/episodes/v2-01-dns/narration.md) |
| 02 | bufferbloat | Why Fast Internet Can Still Feel Slow | 9:39 | [Read](networks/episodes/v2-02-bufferbloat/narration.md) |
| 03 | wdm | How One Fiber Carries So Many Conversations | 9:02 | [Read](networks/episodes/v2-03-wdm/narration.md) |
| 04 | packet-switching | Why the Internet Breaks Everything Into Pieces | 9:45 | [Read](networks/episodes/v2-04-packet-switching/narration.md) |
| 05 | dijkstra | The Shortest Route Can Have More Steps | 9:26 | [Read](networks/episodes/v2-05-dijkstra/narration.md) |
| 06 | subnetting | Move Two Bits, Create Four Networks | 8:45 | [Read](networks/episodes/v2-06-subnetting/narration.md) |
| 07 | tcp-slow-start | How Does a Download Discover Its Speed? | 9:45 | [Read](networks/episodes/v2-07-tcp-slow-start/narration.md) |
| 08 | rsa | A Lock Anyone Can Close, but Only You Can Open | 9:23 | [Read](networks/episodes/v2-08-rsa/narration.md) |

## The focus of each story

### 01. Why Can Your Internet Work While Your Apps Don’t?

Follow a name lookup, its referrals, cache reuse and TTL. No full website journey or transport tutorial.

[Player](networks/episodes/v2-01-dns/presentation.html) · [Video](networks/episodes/v2-01-dns/episode.mp4) · [Script](networks/episodes/v2-01-dns/narration.md) · [Sources](networks/episodes/v2-01-dns/references.md)

### 02. Why Fast Internet Can Still Feel Slow

Explain queueing delay under load through the waiting packet. No survey of TCP algorithms.

[Player](networks/episodes/v2-02-bufferbloat/presentation.html) · [Video](networks/episodes/v2-02-bufferbloat/episode.mp4) · [Script](networks/episodes/v2-02-bufferbloat/narration.md) · [Sources](networks/episodes/v2-02-bufferbloat/references.md)

### 03. How One Fiber Carries So Many Conversations

Combine and separate independent optical wavelength channels. No FDM/TDM comparison chapter.

[Player](networks/episodes/v2-03-wdm/presentation.html) · [Video](networks/episodes/v2-03-wdm/episode.mp4) · [Script](networks/episodes/v2-03-wdm/narration.md) · [Sources](networks/episodes/v2-03-wdm/references.md)

### 04. Why the Internet Breaks Everything Into Pieces

Use packet boundaries for shorter turns and pipelining. No routing or TCP tutorial.

[Player](networks/episodes/v2-04-packet-switching/presentation.html) · [Video](networks/episodes/v2-04-packet-switching/episode.mp4) · [Script](networks/episodes/v2-04-packet-switching/narration.md) · [Sources](networks/episodes/v2-04-packet-switching/references.md)

### 05. The Shortest Route Can Have More Steps

Settle distances, relax edges and reconstruct a least-cost route. No distance-vector, RIP or BGP lesson.

[Player](networks/episodes/v2-05-dijkstra/presentation.html) · [Video](networks/episodes/v2-05-dijkstra/episode.mp4) · [Script](networks/episodes/v2-05-dijkstra/narration.md) · [Sources](networks/episodes/v2-05-dijkstra/references.md)

### 06. Move Two Bits, Create Four Networks

Move an IPv4 prefix boundary to split one block into four. No NAT, IPv6 or classful-addressing chapter.

[Player](networks/episodes/v2-06-subnetting/presentation.html) · [Video](networks/episodes/v2-06-subnetting/episode.mp4) · [Script](networks/episodes/v2-06-subnetting/narration.md) · [Sources](networks/episodes/v2-06-subnetting/references.md)

### 07. How Does a Download Discover Its Speed?

Use ACK feedback to grow the congestion window. No TCP/UDP comparison or algorithm survey.

[Player](networks/episodes/v2-07-tcp-slow-start/presentation.html) · [Video](networks/episodes/v2-07-tcp-slow-start/episode.mp4) · [Script](networks/episodes/v2-07-tcp-slow-start/narration.md) · [Sources](networks/episodes/v2-07-tcp-slow-start/references.md)

### 08. A Lock Anyone Can Close, but Only You Can Open

Recover one message through modular public and private operations. No AES, TLS walkthrough or Shor lesson.

[Player](networks/episodes/v2-08-rsa/presentation.html) · [Video](networks/episodes/v2-08-rsa/episode.mp4) · [Script](networks/episodes/v2-08-rsa/narration.md) · [Sources](networks/episodes/v2-08-rsa/references.md)

## Playback

Run `python3 networks/serve.py` from the project folder, then open <http://127.0.0.1:8765/networks/>. The lesson window shows only the animation.

- Click or **→** starts fullscreen; **→/←** moves between phases.
- **↑/↓** changes speed from 0.25× to 4×. **P** pauses; **R** replays; **F** toggles fullscreen.
- **Shift+P** opens the current script in a separate presenter window.

## Earlier material

The previous series remains available in [the legacy index](networks/legacy-index.html), its [topic guide](TOPICS-legacy.md), and its [scripts](networks/legacy-scripts.md). Existing episode links remain valid. The [solar-system animation](SolarSystem.mp4) is a separate 30-second demonstration.
