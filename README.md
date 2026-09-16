# GitHub Launch Studio

**English** · [简体中文](./README.zh-CN.md)

A Codex skill for turning a working repository into a launch-ready open-source project.

It helps you sharpen positioning, improve the README and quickstart, plan convincing demo assets, and prepare Chinese/English release copy—without fake growth or noisy marketing.

[![30-second GitHub Launch Studio demo](./assets/launch-demo.gif)](./assets/launch-demo.mp4)

*30-second walkthrough: audit, Markdown report, launch package, benchmark map, and bilingual copy.*

![GitHub Launch Studio social card](./assets/social-card.png)

**Audit → Position → Benchmark → Package → Demo → Launch**

## When to use it

Use GitHub Launch Studio before:

- publishing a project on GitHub for the first time;
- preparing a major release;
- improving a repository that works but does not clearly communicate its value;
- creating a demo GIF, screenshots, social card, or release-page story;
- launching a Chinese-built project to an English-speaking audience.

### Example requests

```text
Audit this repository and tell me whether it is ready to launch.
Rewrite the README for an international GitHub launch.
Create a v1.0 release plan with GitHub, X, V2EX, and 即刻 posts.
Design a 30-second demo GIF storyboard for this CLI.
Give me a prioritized launch checklist for next week.
```

## What it produces

- Evidence-based launch-readiness scores across clarity, activation, proof, trust, distribution, and maintenance.
- A concise positioning statement, target user, five-minute promise, differentiator, and non-goals.
- A grounded benchmark map across README builders, release automation, changelog tools, analytics, and agent workflow kits.
- README and quickstart recommendations with a first-time-user test.
- Demo asset briefs for screenshots, GIFs, videos, and social cards.
- GitHub release notes and channel-specific Chinese/English announcement copy.
- A publishing checklist that keeps secrets, permissions, branch protection, CI, and feedback triage in scope.

## How it compares

GitHub Launch Studio is complementary to release automation, not a replacement for it:

| Tool type | Strong at | GitHub Launch Studio adds |
| --- | --- | --- |
| README editors | Filling and arranging README sections | Positioning, evidence, quickstart quality, and launch narrative |
| Profile README generators | Personal GitHub profile components | Project launch packaging rather than a personal profile |
| semantic-release / release-please / git-cliff / Changesets | Versioning, changelogs, release PRs, and package publishing | Human-facing launch story, demo plan, bilingual copy, and channel plan |
| Star History | Post-launch star trends | Pre-launch activation and distribution work |
| Agent spec/workflow kits | Structured development process | A specialized launch-growth workflow |

See the full [benchmark map](./docs/BENCHMARKS.md) / [中文对标说明](./docs/BENCHMARKS.zh-CN.md). Metrics are observed on a stated date and can be refreshed with the bundled script.

## Installation

After the repository is published:

```bash
git clone https://github.com/MJorgin/github-launch-studio.git \
  ~/.codex/skills/github-launch-studio
```

For local development, copy or symlink this folder into your Codex skills directory, then restart or reload Codex.

## Local repository audit

The bundled audit script works offline and never prints credential file contents. The scan itself is read-only; it writes a file only when `--output` is provided.

```bash
python3 ~/.codex/skills/github-launch-studio/scripts/repo_audit.py /path/to/repository --pretty
```

Generate a shareable Markdown report:

```bash
python3 scripts/repo_audit.py /path/to/repository \
  --format markdown \
  --output /path/to/repository/LAUNCH.md
```

It checks signals such as:

- README, LICENSE, docs, examples, lockfiles, manifests, and workflows;
- quickstart headings, code blocks, images, badges, and broken relative links;
- issue templates, contributor paths, security policy, and roadmap/changelog signals;
- likely secret-bearing filenames;
- simple 0-5 launch-readiness scores and prioritized findings.

The scores are heuristics for a first pass. The skill should still inspect the repository semantically before recommending product positioning or copy.

## Launch kit

- [30-second demo video](./assets/launch-demo.mp4) / [animated GIF](./assets/launch-demo.gif) — the rendered walkthrough included in the README.
- [30-second demo storyboard](./docs/demo-storyboard.md) — recording plan, captions, and pre-flight checks.
- [Draft launch posts](./docs/launch-posts.md) — X, V2EX, and 即刻 drafts for review before posting.

## Refresh benchmarks

```bash
python3 scripts/benchmark_github.py \
  --config benchmarks/representative-tools.json \
  --format markdown
```

The benchmark helper uses the public GitHub API. Set `GITHUB_TOKEN` to raise the rate limit; the script never prints token values.

## Regenerate the social card

The repository includes a rendered `assets/social-card.png`. To regenerate it locally:

```bash
python3 -m pip install pillow
python3 scripts/render_social_card.py --output assets/social-card.png
```

## Regenerate the demo

The deterministic demo requires [Pillow](https://pillow.readthedocs.io/) and `ffmpeg`:

```bash
python3 -m pip install pillow
python3 scripts/render_launch_demo.py
```

It writes `assets/launch-demo.mp4` and `assets/launch-demo.gif` without recording the desktop or exposing local terminal paths.

## How it works

1. Audit the repository using real file and Git metadata.
2. Define the target user, five-minute outcome, proof, and strongest alternative.
3. Improve activation surfaces: hero, quickstart, example, limits, and support path.
4. Plan the smallest demo asset that proves the value.
5. Prepare bilingual release notes and channel-specific posts.
6. Verify the clean-install path and publish only after explicit approval.

Read [SKILL.md](./SKILL.md) for the full operating rules and the [references](./references) directory for detailed playbooks.

## Safety and boundaries

- The audit script does not use the network.
- Drafts and local edits are separated from external publication.
- Creating GitHub releases, changing repository settings, posting on social platforms, commenting in communities, or sending DMs requires separate authorization.
- The skill explicitly avoids bought stars, fake testimonials, undisclosed paid promotion, mass outreach, scraped contact lists, or fabricated metrics.

## Roadmap

- Optional Markdown/link report rendering.
- More repository-language heuristics and clean-install probes.
- Example launch teardowns from high-quality open-source projects.
- Optional bilingual release-note templates for common ecosystems.

## Contributing and security

See [CONTRIBUTING.md](./CONTRIBUTING.md) and [SECURITY.md](./SECURITY.md).

## License

[MIT](./LICENSE)
