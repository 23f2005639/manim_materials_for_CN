# Recording cues — TCP Slow Start: How a Download Learns to Speed Up

Record one section at a time, or narrate the click-through presentation live.

Guide subtitles use planned timing. Match final subtitles to your recording after editing.

| Section | Start | Length | What to show | Recording cue |
|---|---|---|---|---|
| 01 | 00:00:00 | 33.00s | Send a photo in pieces | Follow one data piece, then learn how replies help the sender grow. |
| 02 | 00:00:33 | 37.43s | How do we know it arrived? | An ACK is a reply confirming progress. |
| 03 | 00:01:10 | 37.00s | Leave room for four pieces | The congestion window limits sent data that is not yet confirmed. |
| 04 | 00:01:47 | 35.20s | Four pieces, then wait | Four occupied spaces mean the sender must wait for progress. |
| 05 | 00:02:22 | 37.43s | One reply makes more room | One reply clears a space and adds another: room for two new pieces. |
| 06 | 00:03:00 | 37.87s | Four replies grow the allowance | Four replies can grow a four-piece allowance to eight. |
| 07 | 00:03:37 | 36.53s | Replies set the rhythm | Returning replies help pace new sending. |
| 08 | 00:04:14 | 35.67s | Watch four become eight | Doubling emerges from adding one space per reply. |
| 09 | 00:04:50 | 36.10s | Write the doubling pattern | The formula records the doubling pattern we already watched. |
| 10 | 00:05:26 | 37.00s | How much per second? | Divide the allowed data by round-trip time to estimate a window-limited rate. |
| 11 | 00:06:03 | 37.00s | Waiting longer changes the speed | The same allowance can give a lower rate when replies take longer. |
| 12 | 00:06:40 | 37.87s | Too much reaches the narrow link | The narrowest link cannot clear unlimited arrivals. |
| 13 | 00:07:18 | 37.43s | Growth needs a stopping point | The threshold marks a boundary for slow-start growth. |
| 14 | 00:07:55 | 35.67s | Try a different starting allowance | A larger initial allowance changes how quickly the ideal curve grows. |
| 15 | 00:08:31 | 37.00s | Real downloads vary | Real data supply and feedback can change the tidy doubling picture. |
| 16 | 00:09:08 | 36.57s | Start small, listen, then grow | Start with limited data, listen to progress, and grow the allowance. |
