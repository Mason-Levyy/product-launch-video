# Security Policy

## Reporting a vulnerability

Please report security issues privately. Use GitHub's
[private vulnerability reporting](https://github.com/Mason-Levyy/product-launch-video/security/advisories/new)
rather than a public issue.

Relevant reports include:

- A script in this repo that writes outside its output directory or runs
  unexpected commands.
- An instruction in `SKILL.md` or the references that could lead an agent to
  expose secrets from the product repo it scans for brand information.

Expect an acknowledgement within 7 days. A fix or mitigation plan should
follow within 30 days.

## Scope

The skill runs locally with your agent's permissions. It reads the product
repo only for brand and copy. The soundtrack script makes no network calls.
Setup steps install third-party packages from npm: Remotion and Remotion's
agent skills. Those packages are covered by their own security policies.
