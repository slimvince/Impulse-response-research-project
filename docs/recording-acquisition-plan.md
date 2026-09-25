# Recording acquisition plan

## Priority

The project currently has no registered SLB-200 recordings. Further acoustic/EUB analysis can characterize the pipeline, but it cannot answer the governing SLB-200-to-acoustic transformation question until SLB material exists.

## Highest-priority recordings

1. Multiple SLB-200 recordings from the same player and setup, with different takes.
2. SLB-200 recordings spanning low, middle, and high register.
3. SLB-200 recordings spanning soft, medium, and loud playing.
4. SLB-200 pizzicato and any available arco/articulation material.
5. At least one held-out SLB-200 take reserved before detector/feature tuning.

## Useful acoustic references

Acquire or register acoustic microphone recordings with comparable:

- player where known;
- register and musical material where practical;
- dynamics;
- articulation;
- microphone and placement;
- room and recording chain;
- sample rate and bit depth.

Exact sample synchronization is not required for the first conditional population analysis, but repeated controlled material is strongly preferred for validation.

## Capture protocol

Record original WAV files without normalization or destructive processing. Preserve:

- original file and SHA-256;
- player and instrument identity;
- strings/setup;
- pickup/DI chain and gain;
- microphone/placement/room for acoustic references;
- sample rate/bit depth/channels;
- take, phrase, register, dynamics, articulation;
- date and permission basis.

Keep originals outside Git unless redistribution is explicitly licensed. Register stable recording IDs in the external manifest and corpus catalogue.

## Analytical role

Use new SLB recordings first for:

1. recording/source-group quality checks;
2. event-quality auditing with the current pipeline;
3. conditional event-level feature distributions;
4. comparison against NS, Ergo, and acoustic groups;
5. held-out transformability tests.

Do not optimize an IR against one SLB recording or whole-file averages.

## Candidate SLB-200 sources found (2026-09-25 web search)

Prior ChatGPT-assisted search had found nothing usable. A follow-up web search (Bing/DuckDuckGo, browser-tool based, no fabricated URLs) surfaced the following **candidate** public sources. None of these are yet registered in the corpus — they are audio-visual content (mostly YouTube), so before any use we must (a) confirm license/permission basis, (b) extract audio only if permitted, (c) assess whether the signal chain is close to "unprocessed" (some are through combo amps/pedals, not DI), and (d) get explicit user go-ahead per source since this is third-party creator content, not our own recordings.

Best candidates (creator states no/minimal processing, or solo/DI-like signal chain):

1. [Sound sample data for Yamaha SLB200 (Electric Upright Bass)](https://www.youtube.com/shorts/2Tg8TK23Vg0) — creator explicitly states "No additional effects or preamp. Recorded directly in iPhone XR with Roland Go Mixer Pro." Closest to unprocessed DI/solo material found so far, but captured through a phone mic/mixer, not a clean line-level DI-to-interface chain.
2. ["Solo Blues: Just a Yamaha Silent Bass"](https://www.youtube.com/watch?v=PiVnrOfwnrY) — explicitly solo bass improvisation on SLB200, channel appears dedicated to solo bass performances (worth checking channel for more takes).
3. ["Have you met miss Jones" (Jazz), Yamaha Silent Bass SLB200](https://www.youtube.com/watch?v=AMgGc8_KdRE) — solo practice recording at home, informal setup (verify processing chain from video description/comments).
4. ["Come Together" solo bass, Silent Bass Yamaha SLB200](https://www.youtube.com/watch?v=urM3lm4F8aw) — solo performance, sound test framing suggests minimal processing but unverified.
5. ["But not for me" — EUB Yamaha SLB200 Silent Bass test](https://www.youtube.com/watch?v=8L9Cqh0lFGc) — explicit "test" recording, solo jazz standard.
6. ["SLB 200 silent bass Yamaha... Impro..."](https://www.youtube.com/watch?v=08-69yPJKCY) — solo improvisation.

Lower priority (through amp/effects, not representative of unprocessed signal, but useful as negative/contrast controls or for pitch-content reference only):

- [Yamaha SLB200 through a GK MB112](https://www.youtube.com/watch?v=tD6nIpjxhOg) — explicitly through a bass combo amp, not representative of a clean pickup signal.
- [Gear Review: Yamaha SLB-200LTD Silent Bass](https://www.youtube.com/watch?v=bqwEBYMPY8A) — press review/demo, mixed solo/talking content.
- [Yamaha SLB-200LTD SILENT Bass Review and Demo](https://www.youtube.com/watch?v=4BVFP7IQeg4) — same caveat.
- [Demo Yamaha SLB200 at Twinbemusic](https://www.youtube.com/shorts/L_Ik31u-kRo) — short demo clip, unclear chain.

### Constraints and next steps before use

- These are all third-party YouTube uploads. We have **not** downloaded, extracted, or registered any audio from them. Per the corpus protocol, using this material requires explicit permission or a clear applicable license (e.g., explicit reuse permission from the uploader, or content the uploader has marked reusable) — YouTube's default terms do not grant redistribution/derivative-analysis rights. This should be discussed with the user before any download/extraction, and ideally the uploader should be contacted for permission, or public-domain/CC-licensed alternatives sought first.
- Video audio (especially phone/room-captured or through-amp) is not equivalent to a clean DI/pickup signal — even the best candidate (#1) went through a phone mic and a small mixer, so it is at best a second-order proxy, likely weaker than the existing NS/Ergo EUB proxy material for isolating the SLB-200 transducer's own signature.
- No dedicated sample-library, forum-hosted, or direct-download WAV/audio-sample source for solo unprocessed SLB-200 material was found in this search. This reinforces that commissioning or requesting a fresh SLB-200 recording (per the existing capture protocol above) remains the most reliable path to acquiring usable, well-documented, permission-clear SLB-200 material.
