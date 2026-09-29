---
name: product-launch-video
description: Concept, script, score and render marketing launch videos — beat-synced promo spots with kinetic typography, brand-native transitions, music and sound design — as code with Remotion, driven by a coding agent (Claude Code, goose). Use this skill whenever the user wants a launch video, promo, ad, teaser, sizzle reel, product announcement, Product Hunt / X / LinkedIn video, or "a video for my product", even if they don't mention Remotion. Also use it for follow-ups on an existing launch video (new concept, recut, new hook, music, new aspect ratio, shorter version).
---

# Product Launch Video

Make a **marketing spot**, not an animated website. The job is to make someone feel the problem,
remember one claim, and want the product — in 15–60 seconds, on mute or with sound. The product UI
is one ingredient, used as proof. Most of the runtime is concept, typography, brand graphics, and
rhythm.

The output is a Remotion project (React → MP4) the agent writes, previews and renders, plus an
original soundtrack. Everything stays editable in Remotion Studio.

Why the workflow looks like this:
1. **A literal brief gets a literal video.** "Show the features" produces a screen recording with
   captions. A concept — a joke, a metaphor, a visual gag built from the product's own verb — is what
   makes a launch memorable. So concept comes before script.
2. **Rhythm is what makes motion feel designed.** Cuts, slams and stamps that land on a beat grid read
   as intentional; the same animations at arbitrary times read as a slideshow. So music (with a known
   BPM) comes before build.
3. **The agent can't see or hear the result.** It will say "render succeeded" while text overflows or a
   cursor misses its target. So you render stills and look at them, and the human listens.

Follow the phases in order. There are two approval gates (after Phase 2 and Phase 3).

---

## Phase 0 — Setup

If you were invoked inside the user's product repo, do Phase 1a's scan first (so you read the product,
not the fresh Remotion scaffold), then create the Remotion project in its own folder
(`<slug>-launch/`) and mention it, so nothing else in their repo changes.

- Remotion project: `npx create-video@latest --yes --blank --no-tailwind <slug>-launch`, then `npm i`.
- Official agent skills: `npx skills add remotion-dev/skills`. Read the installed
  `remotion-best-practices` router and follow its links for markup, transitions, audio, sfx,
  text-highlights and interactivity before writing code — it has the current API.
- Packages: `npx remotion add @remotion/transitions @remotion/google-fonts @remotion/media @remotion/rough-notation`.
- Add `"exclude": [".agents", "agent", ".claude", "node_modules"]` to `tsconfig.json`.
- Copy this skill's `assets/kit/` into `src/kit/` (brand-agnostic components, see below).
- Python 3 with numpy + scipy for the soundtrack script (`pip install numpy scipy`), and ffmpeg for
  the contact sheet, waveform check and loudness pass.
- In goose (Block's agent): enable the Summon extension so it can load skills.

Remotion is free for individuals and companies of ≤3 people; larger companies need a license.

---

## Phase 1 — Guided intake

The goal is a video that feels made *for* this product, not a template. Do the homework first so the
user only answers questions a machine can't, then ask them all at once.

### 1a. Look around before asking (silently)

Check whether you're inside a product repository (`git rev-parse --show-toplevel`, or a
`package.json` / `pyproject.toml` / `README` at the working root). If you are, read it for the brand:

- **Colors:** CSS custom properties, Tailwind theme (`tailwind.config.*` or `@theme` in CSS), design
  tokens, theme files, `manifest.json` theme color.
- **Fonts:** `@font-face`, Google Fonts links, `next/font` calls, Tailwind `fontFamily`.
- **Logo + graphics:** `public/`, `assets/`, `static/`, favicon, and the OG image (it usually holds the
  claim, the palette and the typographic voice in one file).
- **Story:** README, landing-page copy, package description, changelog for what's new.

If you're not in a repo, pull the same things from the product URL or earlier conversation.

### 1b. Ask one round of guided questions

Ask in **one message**, never a drip of follow-ups. Mark your recommended option in each list and say
they can answer "defaults" to accept them all. Skip any question the conversation already answered.

If your environment has a structured question tool (e.g. `AskUserQuestion` in Claude Code), use it for
the multiple-choice items. These tools usually cap at about 4 questions of 2–4 options each plus a
free-text "Other", so drop question 3 (it defaults to the music mood) and trim options to the likeliest
for this product; put the story block (6) in your message text. Otherwise, number the questions and
letter the options so the user can reply "1b, 2a, 4c".

1. **Brand** — only if you found a brand in the repo. Show what you found in one line (hex codes,
   font names, logo path), then ask:
   (a) use this brand as-is, (b) use it but push it bolder for video (brighter accent, heavier type),
   (c) create a fresh look for this launch.
   If there's no repo brand: point me at a site/logo, or I'll propose a palette in Phase 2.
2. **Music mood** — (a) energetic / hype, (b) confident & minimal, (c) classy / elegant,
   (d) somber / cinematic, (e) playful, (f) I'll bring my own track. Default to the mood that fits the
   product; say which you picked and why in a few words.
3. **Overall vibe** for copy and motion — playful / confident-minimal / cinematic-hype /
   founder-sincere. Default: match the music mood.
4. **Where it's going** — X or LinkedIn (16:9), Reels / TikTok / Shorts (9:16), Product Hunt or site
   hero (16:9, silent-friendly), or several. And length: 15s teaser / 30s (default) / 45–60s.
5. **Voiceover** — none (default, text carries the story) / they'll record one / placeholder script
   only.
6. **Confirm the story you drafted** from the repo, as a short pre-filled block they can edit:
   - The repeatable claim (one sentence a viewer could say to a friend)
   - The pain, in the audience's words, and who feels it
   - The product's verb (what a user *does* with it: share, comment, search, transcribe…) — this
     becomes the concept
   - Real proof (numbers, users, logos) or "none". Never invent proof.
   - CTA + URL

Keep it to these six. If they reply "defaults" or "just go", proceed with your picks and list them
in one line so they can object.

### 1c. Lock the choices

Write the answers to `launch-brief.md` in the project (brand, mood, vibe, formats, length, VO, story).
Later phases read from it, and it makes follow-ups ("make it more somber") a one-line edit. If they
chose the repo brand, copy the exact tokens into `src/<product>/brand.ts` now.

---

## Phase 2 — Creative direction (GATE 1)

Read `references/creative-playbook.md`. Then propose **2–3 distinct concepts** that fit the brand,
mood and vibe from `launch-brief.md`, each as:

- **Concept name + one-line idea** (e.g. "Screenshot hell → the file comes alive").
- **The device:** the visual metaphor or gag that carries it. Best source: the product's own verb
  turned into the storytelling device (a commenting tool *marks up its own headline*; a search tool
  *finds the punchline*; a transcription tool *captions itself*).
- **Transition vocabulary:** 2–4 brand-native transitions (marker wipe, sticky slap, shutter,
  zoom-through into a logo, color-block cut) — not generic fades.
- **Sound:** tempo/energy and 3–5 signature SFX tied to actions.
- **Beat map:** acts mapped to bars (intro → drop → break → drop → outro).

Recommend one. Wait for the user to pick or mix. If they already gave clear creative direction,
present one concept and proceed unless they object.

---

## Phase 3 — Score + shot list (GATE 2)

**Score first.** Generate the soundtrack so the grid is exact:

```
python3 <skill>/scripts/make_soundtrack.py --bpm 120 --fps 30 \
  --sections "intro:2,drop:7,break:3,drop:2,outro:1" --key A --mode minor --out public/audio
```

It writes `music.wav` (original, royalty-free), `sfx/*.wav` (whoosh, riser, impact, pop, slap, tick,
shutter, stamp) and `beats.json` (frames per beat, section frame ranges). One bar lasts 240 ÷ BPM
seconds (2s at 120 BPM), so pick the bar count for the target length. Stick to BPMs that give whole
frames per beat at 30fps (90, 100, 120, 150); the script warns otherwise.

Start from the music mood in the brief:

| Mood | BPM | Mode | Sections (≈30s) |
|---|---|---|---|
| Energetic / hype | 120 | minor | `intro:2,drop:7,break:3,drop:2,outro:1` |
| Confident & minimal | 100 | minor | `intro:1,groove:6,break:2,groove:3,outro:1` |
| Classy / elegant | 100 | major | `intro:2,groove:5,break:3,groove:2,outro:1` |
| Somber / cinematic | 90 | minor | `intro:2,break:3,groove:4,break:1,outro:1` |
| Playful | 120 | major | `intro:1,drop:6,break:2,drop:5,outro:1` |

The built-in scorer is an electronic palette. For a truly acoustic, orchestral or jazz-lounge feel,
tell the user that and suggest bringing their own track rather than overpromising. If they supply a
track, ask for its BPM and the time of the first downbeat instead of generating one.

Then adjust sections so acts match the concept: a hook in the intro, the claim on the first drop (or
first groove), proof montage there, the "how/AI/why it matters" in the break, stamps + logo on the
final drop or groove. Scale bar counts for 15s or 60s versions.

Then write the shot list as a table:

| # | Frames (bars) | Scene type | On-screen text (exact) | Visual / device | Transition out | SFX |

Rules:
- **Scene types** (see playbook): kinetic type, metaphor graphic, color-block card, product glimpse,
  stamps/proof, end card. **Product UI ≤ ~40% of runtime.** If the list is mostly UI, rethink.
- Every cut, slam, stamp and reveal lands on a beat. Big moments land on bar downbeats and section
  changes (the drop is where the claim or the logo hits).
- 0–3s names the pain or makes the boldest claim. Never open on the logo.
- On-screen copy is final and short (≈3 words per second). The story must work on mute.
- Background color changes on cuts carry energy; keep 3–4 brand colors in rotation.
- End on the claim callback + URL. One CTA.
- Also draft the 2–3 sentence post copy.

Wait for approval.

---

## Phase 4 — Build

```
src/
  kit/            # from assets/kit: anim helpers, beat grid, Sfx, Grain, MarkerWipe, ShutterCut, StickySlap, Slam, Stamp, Annotation, NamedCursor, Cursor
  <product>/
    brand.ts      # colors + fonts: single source of truth
    scenes/       # one component per scene
    Launch.tsx    # TransitionSeries + Overlays + <Audio> music + <Sfx> list + <Grain>
  Root.tsx        # final composition + each scene as its own composition in a Folder
```

- **Cuts and transitions:** use `TransitionSeries.Sequence` with hard cuts on the beat, and put
  brand-native transitions in `TransitionSeries.Overlay` (they hide the cut at their midpoint and
  don't change total length, so sequence durations sum exactly to the video length). Overlays can't be
  adjacent to each other or to a `Transition`. Avoid `fade()` — it stacks both scenes' text.
- **Match cuts** are the premium move: zoom through a logo element whose color is the next scene's
  background; wipe with a color that the next scene starts on.
- **Kinetic type:** `Slam` for beat hits, `Stamp` for proof labels, `@remotion/rough-notation`
  (`StrikeThrough`, `Highlight`, `Underline`, `Circle`, `Box`) for hand-drawn marks driven by
  `progress={interpolate(...)}`. Text easing: fast overshoot-settle (bezier 0.2,0,0,1) over ~8 frames.
- **Product glimpse:** real screen recording (`<Video>` from `@remotion/media`) or a simplified React
  rebuild of the one core interaction. Stage it (3D tilt-in, named multiplayer cursors, hand-drawn
  annotations) rather than showing a flat screen. Cursors travel on eased paths, never teleport.
- **Texture:** `Grain` at ~0.06 opacity over everything keeps flat color from looking sterile.
- **Audio:** `<Audio src={staticFile("audio/music.wav")} volume={0.7} />` plus an `Sfx` list
  `[frame, src, volume]` in `Launch.tsx`. Map each visual action to one sound: slam→pop,
  stamp→stamp, sticky→slap, wipe→whoosh (start ~8 frames early), drop→impact, cursor→click.
  Generic SFX from `https://remotion.media/` (mouse-click, page-turn, ding, shutter-modern, whip) are
  fine; avoid the meme sounds for brand work.
- **Studio-editable:** follow the `remotion-interactivity` skill — `Interactive.Div` with hardcoded
  `name`, inline `interpolate()` in `style`, `scale`/`translate`/`rotate` properties, inline named
  `durationInFrames` on every sequence.
- Explicit background color on every scene. Readability at 1080p: headlines ≥ 84px, body ≥ 44px;
  for 9:16 keep text ≥150px from top, ≥170px from bottom, ≥60px from the sides.
- No invented stats, testimonials, customer logos, or fake UI claims.

Build one scene at a time; render a still of each before moving on.

---

## Phase 5 — Look at it (self-review)

Render stills with `scripts/review_frames.sh <CompositionId> <fps> <seconds...>` at: the middle and
settled end of every scene, the midpoint of every overlay transition, every cursor click, the last
frame of a zoom-through, and the final frame. It also tiles them into `contact-sheet.png` (needs
ffmpeg); look at the sheet, then open suspicious frames full size. Check:

- [ ] The first second reads instantly and matches the post's promise
- [ ] Big type fits the frame; nothing clipped; contrast holds on every background color
- [ ] Transitions fully cover the cut at their midpoint (no half-revealed scenes, no muddy blends)
- [ ] Popovers, badges, cursor name-tags and notes don't cover the text they point at
- [ ] Cursor clicks land on target
- [ ] Zoom-throughs end fully covered by the next scene's color (match cut is seamless)
- [ ] No placeholder or invented copy

Audio: render a waveform (`ffmpeg ... showwavespic`) and confirm transients sit on the beat and the
drop lands where planned. The human still has to listen — say so.

---

## Phase 6 — Render + ship

- `npx remotion render <Id> out/<name>-raw.mp4` (don't pass `--concurrency` above `nproc`).
- Loudness for social: `ffmpeg -i raw.mp4 -c:v copy -af loudnorm=I=-14:TP=-1:LRA=11 -c:a aac -b:a 192k final.mp4`.
- Deliver the MP4, the shot list, the post copy. Offer the cut-down set (9:16, 1:1, silent hero loop,
  ~10s teaser from the hook + drop + end card).

## Iteration

"More creative" → go back to Phase 2 with new concepts, don't just add effects. "Make it shorter" →
drop bars, not frames (keep the grid; regenerate the score with fewer bars). Prefer editing the shot
list, then only the affected scenes. Fold every manual fix back into `brand.ts` or `src/kit/`.

## Reference files
- `references/creative-playbook.md` — concept patterns, scene types, transition vocabulary, kinetic
  type, sound-design map. Read in Phase 2 and 3.
- `references/craft-rules.md` — hooks, launch structures, what top launches on X do. Read in Phase 3.
- `references/prompt-template.md` — standalone prompt for running this without the skill.
- `scripts/make_soundtrack.py` — original score + SFX + beat grid.
- `scripts/review_frames.sh` — review stills + contact sheet.
- `assets/kit/` — reusable Remotion components (anim helpers, beat grid, SFX, grain, MarkerWipe, ShutterCut,
  StickySlap, Slam, Stamp, Annotation, NamedCursor, Cursor). Recolor via props; don't hardcode brands.
