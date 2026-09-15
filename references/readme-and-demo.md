# README and demo packaging

## README flow

Adapt the order to the project; do not add sections that have no information.

1. **Hero:** project name, one-line outcome, primary platform/category, one visual if useful, and two CTAs (Quick Start / Demo or Docs).
2. **Social proof or proof strip:** real benchmark, badge, sample output, short quote, or production use. Badges should carry information, not decorate.
3. **Problem and solution:** explain the status quo and the project's specific answer.
4. **Use cases:** three concrete scenarios with expected outcomes.
5. **Quick start:** prerequisites, install, minimal configuration, run command, and expected result.
6. **Basic usage:** the smallest useful input/output and common option.
7. **How it works:** enough explanation to build trust without blocking activation.
8. **Deeper docs / recipes:** link rather than duplicating content.
9. **Limits and compatibility:** supported platforms, versions, costs, API dependencies, and non-goals.
10. **Contributing, roadmap, security, license:** as appropriate for maturity.

## Quickstart quality bar

The quickstart should be tested as if the reader has never seen the repository.

- Prerequisites are explicit: runtime, package manager, OS, service, API key, permissions, and hardware.
- Environment variables have names, where to get keys, and whether costs apply.
- The first path uses a stable example; avoid requiring the user to invent input.
- Commands are copy-pasteable and use the actual released package name.
- The expected result is shown, not just “it works”.
- Platform-specific alternatives are separated so macOS/Linux/Windows users can skip noise.
- The instructions work from a clean clone or temporary directory.

If the quickstart cannot be tested, label the audit or draft accordingly instead of implying verification.

## English and Chinese strategy

For a Chinese maintainer targeting an international launch:

- Keep the root README in concise English.
- Add `README.zh-CN.md` when Chinese users are a meaningful audience.
- Put a language link beside the intro, not a long note at the bottom.
- Do not word-for-word translate idioms; rewrite examples and explanations for the audience.
- Keep commands, config keys, API names, and error messages in their original form.
- Avoid claims that sound culturally overstated in English, such as “best”, “ultimate”, or “revolutionary”, unless backed by proof.

## Demo assets

Choose the smallest asset that proves the value.

| Asset | Best for |
| --- | --- |
| Screenshot | UI output, before/after, generated artifact, dashboard. |
| Short GIF | A workflow under 30 seconds with 2-4 meaningful steps. |
| Video with voice/captions | Complex setup, architectural workflow, or Product Hunt launch. |
| Sample input/output | CLI, API, library, data transformation, or model output. |
| Diagram | Multi-component systems or data flow where screenshots do not explain causality. |
| Social card | Link previews and announcements; it supplements rather than replaces product proof. |

## Screenshot/GIF storyboard

For a workflow demo, specify:

- audience and one claim the asset must prove;
- environment and sample data, avoiding private data;
- opening state;
- 2-4 actions;
- final visible result;
- captions for each step;
- duration, aspect ratio, and maximum file size.

Prefer a real result over a mocked UI. If a mock is necessary, label it clearly.

## Social visual brief

Provide this to a designer or image generator:

- project name and outcome headline;
- target viewer and platform;
- one visual metaphor, if needed;
- 3-5 feature chips tied to proof;
- brand colors, typography, and logo constraints;
- dimensions, safe margins, and accessibility contrast;
- forbidden elements: fake logos, fake testimonials, exaggerated charts, or unrelated stock imagery.

Good GitHub social images usually make the product outcome obvious at small size. Avoid dense screenshots and tiny code snippets.

## README anti-patterns

- Starts with implementation details before the user outcome.
- Uses badges without a maintainer-facing reason.
- Hides install instructions after a long essay.
- Provides many features but no example output.
- Claims compatibility without versions.
- Mixes maintainer notes, roadmap history, and user instructions in one section.
- Uses screenshots with secrets, private company names, or private user data.
- Gives no path for questions, bug reports, or unsupported platforms.
