# Launch video prompt (standalone)

Paste into Claude Code or goose inside a Remotion project after `npx skills add remotion-dev/skills`
and `npx remotion add @remotion/transitions @remotion/google-fonts @remotion/media @remotion/rough-notation`.
Fill in the brackets; delete lines you don't know and the agent will ask.

---

```
Use the Remotion best practices skill. Read its markup, transitions, audio, sfx, text-highlights and
interactivity rules before writing code.

Make a MARKETING launch spot for [PRODUCT] ([URL]) — not an animated walkthrough of the website.
Product UI should be at most ~40% of the runtime; the rest is concept, kinetic typography, brand
graphics and rhythm.

INPUTS
- Claim (one sentence): [e.g. "Send the file, not a screenshot."]
- Audience + their pain: [..]
- The product's verb (what users DO): [..]
- Real proof or "none": [..]
- CTA + URL: [..]
- Format: [1920x1080 | 1080x1920], 30fps, [30]s. Tone: [playful | minimal | hype | sincere]
- Music mood: [energetic | confident-minimal | classy | somber | playful | my own track]
- Brand: pull colors, fonts and graphic devices from the site and its OG image.

STEP 1 — CONCEPTS (stop for my pick)
Pitch 2–3 distinct concepts. For each: the idea in one line, the visual device (best: the product's own
verb used to tell the story, e.g. a commenting tool marking up its own headline), 2–4 brand-native
transitions (no generic fades), the sound (tempo + signature SFX), and a beat map by bars.

STEP 2 — SCORE + SHOT LIST (stop for approval)
Make an original soundtrack at a fixed BPM (120 BPM @ 30fps = 15 frames/beat) with sections
intro → drop → break → drop → outro, plus SFX (whoosh, pop, slap, stamp, impact, shutter).
Shot list table: frames (bars) | scene type | exact on-screen text | visual/device | transition | SFX.
Every cut, slam and stamp on a beat; the claim hits on the first drop; logo on the last. 0–3s names
the pain. Works on mute. Also draft the post copy.

STEP 3 — BUILD
- TransitionSeries with hard cuts on the beat; brand-native transitions as TransitionSeries.Overlay so
  they hide the cut and don't change the total length. Try one zoom-through match cut.
- Kinetic type: slams (overshoot-settle ~8 frames), stamps, and @remotion/rough-notation strike-through,
  highlight, underline and box driven by progress={interpolate(...)}.
- One staged product glimpse (3D tilt-in, named cursors, a hand-drawn annotation), not a flat screen.
- Subtle animated grain over everything. Explicit background on every scene.
- <Audio> for music (volume ~0.7) + a [frame, src, volume] SFX list, one sound per action type.
- Interactive.Div with names + inline interpolate so I can tweak in Studio. No invented stats.

STEP 4 — CHECK YOUR WORK
You can't see or hear it. Render stills at the middle/end of every scene, the midpoint of every
transition, every cursor click and the final frame; tile them into a contact sheet and fix clipping,
overlaps, contrast and uncovered cuts. Render a waveform to confirm hits land on the beat. Then render,
loudnorm to -14 LUFS with ffmpeg, and open Studio for me.
```

---

## Follow-ups that work well
- "Pitch three new concepts — keep the music, change the device."
- "Swap the montage colors so blue lands on the drop."
- "Give me a 10s teaser: the hook, the claim rewrite, the end card. Regenerate the score as intro:1,drop:3,outro:1."
- "Make a 9:16 version — restack the layouts, keep the same beat map."
