# Eight networking stories, built from the basics

Each standalone video begins with a concrete picture and explains new terms as they appear. Simple English narration follows the animation from the first object to the final experiment. Each has 16 self-paced phases and a continuous silent MP4 for recording your own voice.

| # | Topic | Video | Runtime | Script |
|---|---|---|---|---|
| 01 | dns | DNS: How a Website Name Finds Its Address | 9:30 | [Read](networks/episodes/v2-01-dns/narration.md) |
| 02 | bufferbloat | Why Fast Internet Can Still Feel Slow | 9:43 | [Read](networks/episodes/v2-02-bufferbloat/narration.md) |
| 03 | wdm | How One Fiber Carries So Many Conversations | 9:33 | [Read](networks/episodes/v2-03-wdm/narration.md) |
| 04 | packet-switching | Why the Internet Breaks Everything Into Pieces | 9:42 | [Read](networks/episodes/v2-04-packet-switching/narration.md) |
| 05 | dijkstra | The Shortest Route Can Have More Steps | 9:34 | [Read](networks/episodes/v2-05-dijkstra/narration.md) |
| 06 | subnetting | Move Two Bits, Create Four Networks | 9:38 | [Read](networks/episodes/v2-06-subnetting/narration.md) |
| 07 | tcp-slow-start | TCP Slow Start: How a Download Learns to Speed Up | 9:45 | [Read](networks/episodes/v2-07-tcp-slow-start/narration.md) |
| 08 | rsa | A Lock Anyone Can Close, but Only You Can Open | 9:45 | [Read](networks/episodes/v2-08-rsa/narration.md) |

## How each story builds

### 01. DNS: How a Website Name Finds Its Address

Two computers and a photo → names and addresses → a helper → directories → saved answers.

DNS lookup, referrals, caching and expiry.

[Player](networks/episodes/v2-01-dns/presentation.html) · [Video](networks/episodes/v2-01-dns/episode.mp4) · [Script](networks/episodes/v2-01-dns/narration.md) · [Sources](networks/episodes/v2-01-dns/references.md)

### 02. Why Fast Internet Can Still Feel Slow

One message → a router doorway → bits per second → a waiting line → measured delay.

Why a busy connection can move plenty of data while small messages wait.

[Player](networks/episodes/v2-02-bufferbloat/presentation.html) · [Video](networks/episodes/v2-02-bufferbloat/episode.mp4) · [Script](networks/episodes/v2-02-bufferbloat/narration.md) · [Sources](networks/episodes/v2-02-bufferbloat/references.md)

### 03. How One Fiber Carries So Many Conversations

A 3D glass fiber and light pulse → bits → wave spacing → four independent conversations.

How wavelength channels combine, travel together and separate at the other end.

[Player](networks/episodes/v2-03-wdm/presentation.html) · [Video](networks/episodes/v2-03-wdm/episode.mp4) · [Script](networks/episodes/v2-03-wdm/narration.md) · [Sources](networks/episodes/v2-03-wdm/references.md)

### 04. Why the Internet Breaks Everything Into Pieces

One picture → small labeled pieces → a second message → bits and timing → overlapping link work.

Packet turns, sharing, store-and-forward timing and pipelining.

[Player](networks/episodes/v2-04-packet-switching/presentation.html) · [Video](networks/episodes/v2-04-packet-switching/episode.mp4) · [Script](networks/episodes/v2-04-packet-switching/narration.md) · [Sources](networks/episodes/v2-04-packet-switching/references.md)

### 05. The Shortest Route Can Have More Steps

Devices as dots → connections as lines → prices → two routes → a growing scorecard.

Find the route with the smallest total cost, then try a broken connection.

[Player](networks/episodes/v2-05-dijkstra/presentation.html) · [Video](networks/episodes/v2-05-dijkstra/episode.mp4) · [Script](networks/episodes/v2-05-dijkstra/narration.md) · [Sources](networks/episodes/v2-05-dijkstra/references.md)

### 06. Move Two Bits, Create Four Networks

Computers need addresses → a 0/1 bit → a shared beginning → halves → quarters.

Split one IPv4 address block into four subnets; derive masks and host counts.

[Player](networks/episodes/v2-06-subnetting/presentation.html) · [Video](networks/episodes/v2-06-subnetting/episode.mp4) · [Script](networks/episodes/v2-06-subnetting/narration.md) · [Sources](networks/episodes/v2-06-subnetting/references.md)

### 07. TCP Slow Start: How a Download Learns to Speed Up

A photo in pieces → a received-it reply → four spaces → room for more → doubling.

How acknowledgments grow the sending allowance during TCP slow start.

[Player](networks/episodes/v2-07-tcp-slow-start/presentation.html) · [Video](networks/episodes/v2-07-tcp-slow-start/episode.mp4) · [Script](networks/episodes/v2-07-tcp-slow-start/narration.md) · [Sources](networks/episodes/v2-07-tcp-slow-start/references.md)

### 08. A Lock Anyone Can Close, but Only You Can Open

A readable private message → public padlocks → counters and leftovers → primes → paired arithmetic.

An intentionally tiny RSA example: public encryption and private recovery.

[Player](networks/episodes/v2-08-rsa/presentation.html) · [Video](networks/episodes/v2-08-rsa/episode.mp4) · [Script](networks/episodes/v2-08-rsa/narration.md) · [Sources](networks/episodes/v2-08-rsa/references.md)

## Playback

Run `python3 networks/serve.py` from the project folder, then open <http://127.0.0.1:8765/networks/>. The lesson window shows only the animation.

- Click or **→** starts fullscreen; **→/←** moves between phases.
- **↑/↓** changes speed from 0.25× to 4×. **P** pauses; **R** replays; **F** toggles fullscreen.
- **Shift+P** opens the current script in a separate presenter window.

## Earlier material

The original series remains available in [the legacy index](networks/legacy-index.html), its [topic guide](TOPICS-legacy.md), and its [scripts](networks/legacy-scripts.md). The previous focused edition is preserved in Git commit `1608d6f`. The [solar-system animation](SolarSystem.mp4) is a separate 30-second demonstration.
