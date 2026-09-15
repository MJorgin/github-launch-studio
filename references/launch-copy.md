# Launch copy and channel packs

## Message house

Before writing posts, define:

- **One-sentence pitch:** what it is and who it helps.
- **Core outcome:** what the user can do after trying it.
- **Three proof points:** real feature, measurable result, integration/ecosystem, example output, or credible limitation handled well.
- **Primary hook:** saved time, removed friction, better quality, lower cost, new capability, or interesting build story.
- **Call to action:** star, try quickstart, read demo, request feedback, or join discussion.
- **Ask:** the one response that helps the project most, such as bug reports, adapters, or real use cases.

The first launch should usually ask for试用反馈 / real-world feedback rather than generic stars.

## Release notes

For a first release:

```markdown
# v0.1.0 — first public release

## What it does
- Capability 1 with user outcome
- Capability 2 with user outcome
- Capability 3 with user outcome

## Quick start
[copy-paste path or link]

## What is validated
- Platforms/runtimes/tests or real examples

## Known limitations
- Honest limitation 1
- Honest limitation 2

## Feedback
Issues/discussions link and the kind of feedback most useful now
```

For a major release, lead with the migration value: before/after, breaking changes, migration path, and compatibility.

## Hook patterns

- **Problem hook:** “Configuring X usually takes Y; this project turns it into Z.”
- **Before/after hook:** show the manual workflow, then the compressed workflow.
- **New capability hook:** “You can now do X without Y.”
- **Build-story hook:** explain a surprising technical or product lesson, then show the result.
- **Proof hook:** benchmark, generated sample, real workflow recording, or migration case study.

Avoid fake urgency, “I built the ultimate X”, unsupported benchmark claims, and open-ended “what do you all think?” without enough context.

## Channel adaptation

### GitHub

Use complete context: problem, solution, quickstart, screenshot/GIF, limitations, feedback ask. Visitors may arrive without seeing any external post.

### X / English

- 1-3 short posts, not a README dump.
- First post: hook + outcome + proof media + link.
- Second post: technical detail or build lesson.
- Third post: examples and feedback request.
- Use 2-4 relevant tags or none; avoid hashtag stuffing.

### Hacker News

Use the official title only when appropriate. Write in a calm, technical first comment: why it exists, how it works, trade-offs, comparison with alternatives, and roadmap. Read the rules and do not ask for upvotes.

### Product Hunt

Prepare a short tagline, six visual cards, maker comment, pricing/limits, supported platforms, launch-day responder plan, and FAQ. Do not launch without someone available for several hours.

### V2EX

Use a factual Chinese title and avoid marketing language. Include背景、解决的问题、快速试用、已知限制、希望反馈. Respect node rules and do not repost duplicates.

### 即刻

More personal and process-oriented: the observation, build process, interesting technical detail, demo, and what feedback would help. Multiple short updates can outperform one formal announcement.

### 知乎 / 公众号 / 少数派

Use a longer problem-solution article with real examples, screenshots, comparison, and lessons. Do not turn it into an ad; the article should be useful even if the reader does not use the project.

### Reddit / Discord / Slack communities

Only post where the project is relevant and allowed. Tailor the post to the community, disclose authorship, do not ask for upvotes, and prioritize learning from feedback over promotion.

## Bilingual post skeleton

Chinese source:

> 做了一个 [项目名]，给 [目标用户] 解决 [具体问题]。和 [现状方案] 不同，它 [差异点]。这里是 [演示/快速开始]，目前已知限制是 [限制]，欢迎大家试用反馈。

English version:

> I built [project] for [target user] who needs to [job]. Instead of [status quo], it [differentiator/outcome]. Here is a [demo/quickstart]. Current limitations: [limits]. Feedback and real-world reports are very welcome.

## Launch timing

- T-7: positioning, README, demo, install test, issue templates, license.
- T-3: release candidate, release notes, visual assets, channel drafts, responder plan.
- T-1: clean release, backup/rollback path, links checked, maintainer availability.
- Launch day: publish repository/release, primary post, follow-up technical comment, triage issues.
- T+1 to T+7: answer issues, document recurring questions, patch blockers, publish one build lesson or example.
- T+30: review activation signals and convert recurring feedback into docs or roadmap items.
