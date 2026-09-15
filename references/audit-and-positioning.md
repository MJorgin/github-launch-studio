# Audit and positioning

## Evidence-first audit

Start from repository evidence, not assumptions. Use the script output plus direct file inspection. Separate:

- **Observed fact:** exact file, command, claim, or missing asset.
- **User impact:** why a first-time visitor, adopter, contributor, or sharer would care.
- **Recommendation:** a concrete change small enough to complete before launch.
- **Priority:** P0 launch blocker, P1 launch-quality item, or P2 post-launch improvement.

Never manufacture metrics, users, companies, benchmarks, testimonials, or comparisons.

## Score six dimensions

Score each dimension from 0 to 5. The script provides signals; the final score must account for semantic quality.

| Dimension | Strong state |
| --- | --- |
| Clarity | Name, one-line outcome, target user, category, and scope are understandable within a minute. |
| Activation | A new user can install, configure, run, and see a meaningful result with minimal decisions. |
| Proof | Real examples, screenshots/GIFs, sample output, benchmarks, tests, or recognizable use cases demonstrate credibility. |
| Trust | License, limitations, maintenance signals, security guidance, issue paths, and realistic claims are present. |
| Distribution | English and/or bilingual surfaces, shareable visuals, release notes, tags, and channel-specific hooks make the project portable. |
| Maintenance | Repository settings, docs, contributor path, roadmap, CI, release process, and triage plan are realistic. |

Use this interpretation:

- **0-1:** launch blocker or major misunderstanding risk.
- **2-3:** usable by an expert friend, not ready for public attention.
- **4:** ready for a targeted launch.
- **5:** ready for broad launch and contributor growth.

A high score does not require every asset. A small utility may not need a CONTRIBUTING guide, complex architecture docs, or a Product Hunt launch.

## Positioning formula

Use this as a working draft, not marketing text to paste verbatim:

> For **[target user]** who **[struggle or job-to-be-done]**, **[project]** is a **[category]** that delivers **[specific outcome]**. Unlike **[alternative or status quo]**, it **[sharp differentiator]**.

Then add:

- **Primary user:** one persona for the launch.
- **Five-minute promise:** what the user should see or accomplish after the quickstart.
- **Trigger moment:** when someone realizes they need this.
- **Strongest proof:** screenshot, GIF, benchmark, before/after, real output, or reference user.
- **Non-goals:** what the project intentionally does not do.
- **Adoption risk:** setup cost, API keys, platform limits, maturity, lock-in, or missing features.

The sharp differentiator should survive a “so what?” test. “Fast”, “modern”, or “AI-powered” alone is not a differentiator. Prefer measurable savings, workflow integration, a unique workflow, better defaults, or a capability that was previously impractical.

## Recommended audit response

1. Executive verdict in two or three sentences.
2. Scorecard table with the strongest evidence and biggest gap for each dimension.
3. P0/P1/P2 recommendations, each with evidence and expected impact.
4. Proposed positioning and five-minute promise.
5. Suggested launch package: exact files/assets to create or change.
6. Questions only when a missing answer changes the recommendation; otherwise state assumptions and proceed.

## Common high-leverage fixes

- Replace a technology-description headline with a user-outcome headline.
- Move the working example above long architecture or motivation sections.
- Add one screenshot or GIF when the value is visual.
- Make the first command copy-pasteable and list prerequisites separately.
- Replace a long feature list with three use cases and proof for each.
- Add “What it does not do” to reduce misunderstood issues.
- Pin supported versions, required API keys, environment variables, and expected costs.
- Ensure the README has one clear next action: install, view demo, read docs, or open an issue.
