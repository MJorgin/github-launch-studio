# Benchmarks

Observed on 2026-09-15 using the public GitHub API. Star counts change over time; refresh with:

```bash
python3 scripts/benchmark_github.py \
  --config benchmarks/representative-tools.json \
  --format markdown
```

## Adjacent-tool map

| Category | Repository | Stars | Forks | Last push | License | Job it does well |
| --- | --- | ---: | ---: | --- | --- | --- |
| README builders | [octokatherine/readme.so](https://github.com/octokatherine/readme.so) | 4,628 | 362 | 2026-03-13 | MIT | Drag-and-drop README editor with a simple section-based activation path. |
| Profile README generators | [rahuldkjain/github-profile-readme-generator](https://github.com/rahuldkjain/github-profile-readme-generator) | 24,439 | 8,405 | 2025-10-28 | Apache-2.0 | Personal-profile README components and visual stats. |
| Release automation | [semantic-release/semantic-release](https://github.com/semantic-release/semantic-release) | 24,037 | 1,812 | 2026-09-14 | MIT | Automated versioning, changelog, package publishing, and release workflow. |
| Release automation | [googleapis/release-please](https://github.com/googleapis/release-please) | 7,496 | 588 | 2026-09-14 | Apache-2.0 | Conventional-commit release PR automation. |
| Changelog generation | [orhun/git-cliff](https://github.com/orhun/git-cliff) | 12,234 | 325 | 2026-09-13 | Apache-2.0 | Highly customizable changelog generation from Git history. |
| Release automation | [changesets/changesets](https://github.com/changesets/changesets) | 12,391 | 831 | 2026-09-14 | MIT | Versioning and changelog workflow focused on monorepos and packages. |
| GitHub analytics | [star-history/star-history](https://github.com/star-history/star-history) | 9,501 | 372 | 2026-09-12 | MIT | Star-history visualization and trend/social-proof analysis. |
| Agent workflow kits | [github/spec-kit](https://github.com/github/spec-kit) | 136,906 | 12,271 | 2026-09-14 | MIT | Structured agent-driven development workflow. |

## Job coverage

| Tool / workflow | Positioning and target user | Repository audit | README authoring | Demo/social asset planning | Version/changelog automation | Bilingual launch copy | Channel launch plan |
| --- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| readme.so | — | — | Strong | — | — | — | — |
| GitHub Profile README Generator | — | — | Profile only | Partial | — | — | — |
| semantic-release | — | — | — | — | Strong | — | — |
| release-please | — | — | — | — | Strong | — | — |
| git-cliff | — | — | — | — | Strong | — | — |
| Changesets | — | — | — | — | Strong | — | — |
| Star History | — | Analytics after launch | — | — | — | — | — |
| Spec Kit | Development specification | — | — | — | — | — | — |
| **GitHub Launch Studio** | **Strong** | **Strong** | **Guidance and edits** | **Strong** | Drafts notes; does not automate publishing | **Strong** | **Strong** |

## Positioning lessons

1. **README tools solve editing, not launch strategy.** A section builder helps fill in a README, but it does not identify the primary user, five-minute promise, proof, or differentiator.
2. **Release tools are complementary.** `semantic-release`, `release-please`, `git-cliff`, and Changesets automate version and changelog mechanics. GitHub Launch Studio can draft the human-facing release story and should interoperate with those tools rather than replace them.
3. **Profile README virality is a different job.** Profile generators benefit from personalization and embeddable widgets, while project launches need activation, trust, examples, limitations, and support paths.
4. **Analytics are post-launch.** Star History explains momentum after a project exists; it does not make a first-time visitor understand the product or complete quickstart.
5. **Agent workflow kits validate the format.** The adoption of structured agent toolkits supports packaging a repeatable launch workflow as a skill, but development specs and open-source launch packaging remain distinct jobs.

## Boundaries

GitHub Launch Studio does not currently:

- automatically bump versions or publish packages;
- replace maintainer judgment about roadmap, pricing, licensing, or community rules;
- guarantee stars, press, rankings, or Product Hunt results;
- create fake testimonials, metrics, outreach lists, or coordinated promotion.

The intended ecosystem position is:

> Release automation handles version mechanics; GitHub Launch Studio handles the launch decision layer—who it is for, why it matters, how a stranger can try it in five minutes, what proof to show, and how to distribute the launch in English and Chinese.
