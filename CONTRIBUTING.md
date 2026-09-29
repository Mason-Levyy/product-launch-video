# Contributing

Issues and pull requests are welcome. The most useful contributions are:

- new brand-agnostic kit components, such as a transition or a type effect
- new concept patterns or hooks for the references
- new sounds or section types for the scorer
- fixes where the workflow breaks on a platform or a Remotion version

## Setup

```bash
git clone https://github.com/Mason-Levyy/product-launch-video.git
cd product-launch-video
npm ci
pip install pyyaml numpy scipy
```

To try your changes, copy or symlink `product-launch-video/` into
`~/.claude/skills/` and make a short video.

## Gate

Run all four checks before you open a PR. CI runs them on every pull request.

```bash
python scripts/validate_skill.py
python scripts/smoke_soundtrack.py
npm run typecheck
shellcheck product-launch-video/scripts/*.sh
```

## Guidelines

- Kit components stay brand-agnostic: colours and fonts come in as props.
- The soundtrack stays fully synthesized. Don't add samples or downloaded audio.
- Keep the two approval gates (concept, then score and shot list).
- The skill never invents stats, testimonials or customer logos. Keep it that way.

## Branches and pull requests

- Branch from `main` (`feat/…`, `fix/…`, `docs/…`); `main` is protected.
- One change per PR. Fill in the template's summary and test plan.
- PRs are squash-merged.

## Commit style

Use a short imperative subject with a type prefix, for example
`feat: add tape-strip wipe` or `fix: clamp riser length for short bars`.
