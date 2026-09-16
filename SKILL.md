---
name: github-launch-studio
description: Plan and produce launch-ready GitHub open-source projects—positioning, README, demo assets, release notes, and bilingual announcement copy—for first launches, major releases, or growth-focused repository makeovers.
metadata:
  short-description: Launch-ready GitHub repository studio
---

# GitHub Launch Studio

Turn a working repository into a credible, understandable, and distributable open-source project. Optimize for real adoption: a visitor should quickly understand who the project is for, what outcome it delivers, why it is trustworthy, and how to try it.

Use this skill for:

- first public GitHub launches and major-version releases;
- repository audits focused on stars, activation, trust, or contributor readiness;
- README / quickstart / example / release-page makeovers;
- demo screenshot, GIF, video, and social-card planning;
- English, Chinese, or bilingual launch copy for GitHub, X, Hacker News, Product Hunt, V2EX, 即刻, 知乎, 公众号, and similar channels.

Do not use it for generic documentation unrelated to a launch, or for fake growth: bought stars, astroturfing, mass DMs, undisclosed paid promotion, fabricated metrics, or scraped outreach lists.

## Operating modes

1. **Audit** — inspect evidence, score launch readiness, and produce a prioritized fix list.
2. **Position** — sharpen target user, job-to-be-done, category, alternatives, proof, and non-goals.
3. **Benchmark** — compare adjacent tools and high-quality repositories without copying their strategy or metrics.
4. **Package** — improve the repository surfaces that turn curiosity into a trial: README, quickstart, examples, docs, license, issue templates, and release page.
5. **Demo** — plan real screenshots/GIFs/videos and social visuals; generate assets only when the user asks and the needed tooling is available.
6. **Launch** — prepare release notes, channel-specific copy, timing, and a post-launch triage plan.

Select only the references relevant to the current mode:

- `references/audit-and-positioning.md` — scorecard, evidence rules, positioning formula, and audit output format.
- `references/benchmarking.md` — adjacent-tool map, comparison rules, and GitHub metadata refresh workflow.
- `references/readme-and-demo.md` — README structure, first-run validation, and demo asset storyboards.
- `references/launch-copy.md` — message house, release notes, and Chinese/English channel packs.
- `references/publish-checklist.md` — verification, repository settings, release operations, and launch-day checklist.

## Workflow

1. **Establish scope.** Identify the repository, launch type, target user, maturity, preferred channels, languages, and whether the user wants analysis only, local edits, or a prepared pull request. Infer these from the repository when possible and state important assumptions.
2. **Audit before writing.** For a local repository, run `python3 scripts/repo_audit.py <repo-path> --format markdown --output <repo-path>/LAUNCH.md` when a shareable report is useful, or use JSON for machine-readable analysis. For a remote URL, either ask for a local checkout or obtain network permission before cloning. The scan is read-only; only explicit `--output` writes a report, and neither mode prints secret values.
3. **Position and benchmark before polishing.** Do not begin with decorative README wording. First decide the primary audience, the five-minute value path, the strongest proof, and the sharpest alternative. When useful, run `python3 scripts/benchmark_github.py --config benchmarks/representative-tools.json --format markdown`.
4. **Create the smallest convincing launch set.** Prefer a complete hero, copy-pasteable quickstart, one real example, visible proof, license, limitations, and support path over exhaustive documentation.
5. **Preserve truth and voice.** Support claims with repository evidence. Replace vague superlatives with concrete outcomes, constraints, benchmarks, or examples. For Chinese-origin projects, write natural English rather than translating idioms literally.
6. **Verify the activation path.** If code or installation instructions changed, run the relevant clean-install, lint, build, or test command that is safe and available. Check links, media paths, prerequisites, and setup/configuration steps.
7. **Keep publication explicit.** Drafts, local commits, and pull requests may be prepared when requested. Do not create a GitHub release, publish social posts, comment in communities, send DMs, or change repository settings unless the user separately authorizes that external action and identifies the account/channel.

## Quality bar

A launch-ready repository should let a new visitor answer all of these within one minute:

- Is this for me?
- What result can I get in five minutes?
- How is it different from what I already use?
- What proof exists that it works?
- What are the limits and costs?
- Where do I ask for help or report a bug?

Prefer specific, testable recommendations over generic advice. Every critical finding should include evidence from the repository, user impact, and a concrete next action.
