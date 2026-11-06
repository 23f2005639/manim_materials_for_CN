# Resume audio production

ElevenLabs stopped at its40,000-credit account quota, reporting307credits remaining.
DNS and bufferbloat are complete. WDM has9completed clips. All8scripts and128tagged
requests are prepared.

Use generation-jobs.json to inspect existing jobs. WDM10and11were submitted but failed
for quota; check these runs before doing anything new. Completed jobs must be downloaded
or reused, never regenerated. Each lesson has its own existing flow in flows.json.

After account credits/quota are increased, continue the missing clip requests using
David/eleven_v4, and save completed audio/takes and provenance with save_audio.py.
The connector defaults to2takes. No further paid generation should start until the
account quota issue is resolved.

Run assemble.py after each lesson has16audio clips. It never calls ElevenLabs.
