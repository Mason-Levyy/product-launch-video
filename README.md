# product-launch-video

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Gate](https://github.com/Mason-Levyy/product-launch-video/actions/workflows/gate.yml/badge.svg)](https://github.com/Mason-Levyy/product-launch-video/actions/workflows/gate.yml)

An agent skill that makes marketing launch videos as code. It writes the
concept, script and an original soundtrack, then builds and renders the video
in [Remotion](https://www.remotion.dev/). The result is a beat-synced promo
spot with kinetic typography and brand-matched transitions, not an animated
screen recording.

It works with Claude Code and with goose.

## Install

Copy the skill folder into your personal skills directory:

```bash
git clone https://github.com/Mason-Levyy/product-launch-video.git
mkdir -p ~/.claude/skills
cp -r product-launch-video/product-launch-video ~/.claude/skills/
```

To install it for a single project, copy it to `<project>/.claude/skills/`
instead. In goose, turn on the Summon extension so goose can load skills.

**Requirements**

- Node.js (current LTS) and npm, for Remotion
- Python 3 with `numpy` and `scipy` (`pip install numpy scipy`) for the soundtrack
- `ffmpeg` for the contact sheet, the waveform check and the loudness pass

## Quick start

Open your product's repo in Claude Code and ask:

```
Make a 30-second launch video for this product.
```

Other requests also trigger it: "promo", "teaser", "Product Hunt video",
"a video for my product". You don't need to mention Remotion.

The skill first scans the repo for brand colours, fonts, logo and copy. It
then asks **one** round of questions (brand, music mood, format, length,
voiceover, story), or you can answer "defaults". The Remotion project is
created in its own `<slug>-launch/` folder, so nothing else in your repo
changes.

## How it works

| Phase | What happens | Your input |
|---|---|---|
| 0. Setup | Scaffolds a Remotion project, installs Remotion's agent skills and packages, and copies in the kit | |
| 1. Intake | Reads the brand and story from your repo, then asks one round of questions; saves the answers to `launch-brief.md` | Answer once, or say "defaults" |
| 2. Creative direction | Pitches 2–3 concepts, each with its visual device, transitions, sound and beat map | **Gate 1:** pick or mix concepts |
| 3. Score + shot list | Generates an original soundtrack at an exact BPM, then writes a shot list where every cut lands on a beat | **Gate 2:** approve |
| 4. Build | Builds one scene at a time and renders a still of each | |
| 5. Self-review | Renders review frames, tiles them into a contact sheet, fixes clipping, overlaps and uncovered cuts, and checks the waveform | Listen to the audio |
| 6. Render + ship | Renders the MP4, loudness-normalises it to −14 LUFS, and delivers the post copy; offers 9:16, 1:1, silent-loop and teaser cuts | |

Three ideas shape that order:

1. **A literal brief gets a literal video.** The concept is built from the
   product's own verb (a commenting tool marks up its own headline), so the
   concept comes before the script.
2. **Rhythm makes motion look designed.** The music has a known BPM, so it is
   made before the build.
3. **The agent can't see or hear the result.** It renders stills and reviews
   them, and it asks you to do the listening.

### What's in the skill

```
product-launch-video/
├── SKILL.md                     # the workflow above
├── references/
│   ├── creative-playbook.md     # concept patterns, scene types, transitions, sound map
│   ├── craft-rules.md           # hooks, launch structures, anti-patterns
│   └── prompt-template.md       # standalone prompt for use without the skill
├── scripts/
│   ├── make_soundtrack.py       # original score + SFX kit + beats.json
│   └── review_frames.sh         # review stills + contact sheet
└── assets/kit/                  # brand-agnostic Remotion components
```

The kit contains the beat grid, easing helpers, `Slam`, `Stamp`,
`Annotation`, `NamedCursor`, `Cursor`, `Sfx`, `Grain`, and the `MarkerWipe`,
`ShutterCut` and `StickySlap` transitions. Colours come in as props, so
nothing is tied to a particular brand.

### The soundtrack

`make_soundtrack.py` synthesizes all music and SFX from scratch with numpy
and scipy. No samples are used, so there is nothing to license. Because the
tempo is exact, every beat falls on a known frame.

```bash
python3 make_soundtrack.py --bpm 120 --fps 30 \
  --sections "intro:2,drop:7,break:3,drop:2,outro:1" --key A --mode minor --out public/audio
```

It writes `music.wav`, eight SFX (whoosh, riser, impact, pop, slap, tick,
shutter, stamp) and `beats.json`, which holds frames per beat and the frame
range of each section. The sound is electronic. For an acoustic or orchestral
feel, bring your own track and give its BPM.

## Configuration

The skill needs no setup. Choices for each video live in the
`launch-brief.md` it writes, so you can change one with a one-line request
such as "make it more somber" or "give me a 9:16 version". To change the
defaults, edit `SKILL.md` (for example, the mood → BPM table in Phase 3) or
the kit components.

**Remotion licence:** Remotion is free for individuals and for companies of
three people or fewer. Larger companies need a
[company licence](https://www.remotion.dev/license). This skill's MIT licence
covers the skill, not Remotion.

## Development

```bash
npm ci
pip install pyyaml numpy scipy
python scripts/validate_skill.py     # SKILL.md frontmatter
python scripts/smoke_soundtrack.py   # soundtrack + beat grid
npm run typecheck                    # kit, strict TypeScript
shellcheck product-launch-video/scripts/*.sh
```

CI runs the same gate on every pull request. See
[CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE) © 2026 Mason Levy
