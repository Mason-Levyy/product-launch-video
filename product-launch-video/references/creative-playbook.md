# Creative playbook

How to turn a product into a marketing spot. Current launch-video craft leans on typography as the
main character, motion and cuts timed to the music, tactile textures (paper, tape, marker, grain), and
brand-native graphic devices — not screen recordings with captions.

## 1. Finding the concept

Start from the product's **verb** and its **enemy** (the old way).

| Pattern | How it works | Example |
|---|---|---|
| **The product does it to the ad** | The video uses the product's own action as its storytelling device. | A commenting tool strikes through "screenshot" in its own headline and writes "file." A search tool finds the punchline. A transcription tool captions its own voiceover. |
| **Enemy montage → release** | Beat-synced montage of the painful old way, escalating into a joke, then a hard cut to calm. | `dashboard_FINAL_final (1).png` piling up on every beat, "SCREENSHOTS SENT: 6". |
| **Before / after split** | Same task, two halves of the frame or two halves of the song. | Left: 14 tabs and a spreadsheet. Right: one query. |
| **One object, many lives** | A single brand object (a sticky note, a link, a file icon) travels through every scene and transforms. | The file icon becomes a link, a comment bubble, a sticky note, then the logo. |
| **Word as world** | Each feature is one giant word on its own color block; a small visual gag proves it. | "Link." / "Comment." / "Notes." / "Edit." on yellow / paper / blue / ink. |
| **Manifesto** | Short declarative lines, one per beat, building to the claim. Good for confident-minimal brands. | "Screenshots lie. / Files don't. / Send the file." |

Pick the concept that makes the claim *visible*. If you can describe the video without saying what the
product does, it's not a concept yet.

## 2. Scene types (mix them; UI ≤ ~40%)

- **Kinetic type** — a line or word that slams/stamps/strikes on the beat. The workhorse.
- **Metaphor graphic** — diagrams and objects that explain without UI: an orbit for a loop, a pile for
  chaos, a stamp for "free", a highlighter for emphasis.
- **Color-block card** — a full-bleed brand color, one huge word, one small proof visual. 1–2 beats each.
- **Product glimpse** — the real UI, staged: tilt-in in 3D, push-in, named multiplayer cursors,
  hand-drawn annotations pointing at the one thing that matters.
- **Proof / stamps** — "NO ACCOUNT · NOTHING TO INSTALL · FREE", real numbers counting up, logos.
- **End card** — logo slam + claim callback + URL, held for at least a bar.

## 3. Transition vocabulary

Choose 2–4 that come from the brand's world and reuse them; consistency reads as design.

| Transition | Built with | Feels like | Sound |
|---|---|---|---|
| Marker / highlighter wipe | `kit/Transitions.MarkerWipe` in an Overlay | editing, emphasis | whoosh ~8f early |
| Sticky-note slap & peel | `StickySlap` | collaborative, playful | slap on land, page-turn on peel |
| Shutter close/flash | `ShutterCut` | "snap", screenshots, cameras | shutter + impact on the drop |
| Zoom-through match cut | scale a logo detail ×60–80 until its color fills the frame; next scene starts on that color | premium, seamless | whoosh/riser into impact |
| Color-block hard cut | consecutive scenes with different backgrounds, cut on the beat | energy | pop per cut |
| Slide (Remotion `slide()`) | `TransitionSeries.Transition` | clean, product-y | whip |

Other ideas worth building per brand: tape strip wipe, page flip, ink blot, glitch frame (tech),
light leak (`@remotion/effects`, warm/cinematic), iris to a UI element.

## 4. Kinetic type recipes

- **Slam:** scale 1.3–2.0 → 1 with a few degrees of rotation, settle in ~8 frames, on a beat.
- **Stamp:** scale 1.5 → 1 in 6 frames + a 6-frame horizontal shake. Mono type, thick border.
- **Rewrite:** `StrikeThrough` (rough-notation, red, 2 iterations) across the old word over ~10 frames,
  then `Slam` the new word in a highlight box on the next beat. The single most "marketing" move for
  any product about change.
- **Hand marks:** `Highlight` behind a key phrase (switch text color when it lands on dark
  backgrounds), `Underline` under the payoff, `Box`/`Circle` around the URL at the end.
- **Counters:** a mono label that increments on each beat ("SCREENSHOTS SENT: 6") turns a montage into
  a joke.
- **Hierarchy:** one huge word (200–260px) + one small supporting line. Never two big things at once.

## 5. Sound design map

- **Music structure** mirrors the story: intro (tension, ticks, riser) → drop on the claim → break for
  the "how it works" or the AI/why beat → second drop for proof → outro stab on the logo.
- **One sound per action type**, used consistently: slam→pop, stamp→stamp, sticky→slap,
  wipe→whoosh, cursor→click, drop/zoom-through landing→impact, final logo→ding or chord stab.
- Start whooshes ~6–10 frames before the cut so the peak lands on it.
- SFX volume 0.4–0.8 under music at 0.7; the final mix gets `loudnorm` to −14 LUFS for social.
- Voiceover (optional): if the user provides a VO file, set bars around its phrases and duck music
  to ~0.35 under speech; burn in captions so it still works on mute.

## 6. Anti-patterns

- A video that's 80% screen recording with captions.
- Opening on the logo, or a slow fade-in from black.
- Generic fades and random easing; transitions unrelated to the brand.
- Cutting off the grid; SFX that don't match an on-screen action.
- Three generic feature cards with icons ("Fast / Secure / Simple").
- Effects added to fix a weak concept. If it's boring, change the concept.
