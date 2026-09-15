# Benchmarking

Benchmarks sharpen positioning; they are not permission to copy names, claims, visuals, or metrics. Compare the user job and workflow, not just stars.

## Categories to inspect

For a GitHub launch skill, inspect adjacent categories:

| Category | What to learn | What not to infer |
| --- | --- | --- |
| README editors/builders | Section structure, editor UX, activation speed. | They do not necessarily solve positioning or launch distribution. |
| Profile README generators | Viral component design and personalization. | Profile pages are a different job from project launches. |
| Release/changelog automation | Versioning rigor and release operational quality. | Generated release notes do not replace product positioning or demo planning. |
| Star/analytics tools | Social proof and trend visualization. | Analytics diagnose after launch; they do not make the repository understandable. |
| Agent/spec workflow kits | How agent instructions are packaged and trusted. | Development-process kits are not launch-growth tools unless they cover launch surfaces. |
| High-quality repositories in the same domain | Tone, proof, quickstart, issue handling, docs depth. | A mature project's structure may be too heavy for a v0.1 launch. |

## Evidence to collect

For every benchmark, record:

- repository and canonical URL;
- category and the exact user job it serves;
- public stars, forks, primary language, license, homepage, last push, and observation date;
- strongest activation surface;
- strongest proof or distribution mechanism;
- limitation or job it does not cover;
- one transferable lesson for the current project.

Prefer 4-8 carefully selected benchmarks over a long undifferentiated list.

## GitHub metadata helper

The repository includes a read-only metadata helper:

```bash
python3 scripts/benchmark_github.py \
  --config benchmarks/representative-tools.json \
  --format markdown
```

It uses the public GitHub REST API. If `GITHUB_TOKEN` is set, it is sent as a bearer token for a higher rate limit; the script never prints the token.

Treat star counts and last-push dates as observations, not permanent facts. Include the observation date when publishing numbers.

## Comparison rules

- Compare against the status quo as well as named products: “developer writes README and launch copy manually” is often the main competitor.
- Use feature coverage carefully: a small tool can win by focus, even if a mature tool has more features.
- Do not imply official partnership, endorsement, integration, or comparison testing.
- Do not copy screenshots, branding, testimonials, benchmarks, or launch claims.
- Phrase differences as scope boundaries: “focuses on X”, “does not currently cover Y”, not “better than”.
- If a benchmark is inactive or archived, note what can still be learned and avoid treating it as current best practice without qualification.

## Output format

1. Category map with 4-7 representative repositories or status-quo workflows.
2. Public metadata observed on a stated date.
3. Feature/job coverage matrix.
4. Three to five concrete positioning lessons.
5. Explicit non-goals learned from the comparison.

A good final statement is usually:

> Existing tools automate one part of the launch—README blocks, changelogs, versions, or star charts. GitHub Launch Studio covers the launch decision layer: who it is for, what proof matters, how to package activation, and how to distribute the launch in English and Chinese.
