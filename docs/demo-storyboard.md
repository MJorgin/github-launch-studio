# 30-second demo storyboard

Goal: prove that GitHub Launch Studio turns an ordinary repository into a launch-ready package. The demo should show a real audit, a readable report, benchmark context, and prepared launch copy—not a mock product UI.

## Recording setup

- Canvas: 1440×900 or 1512×982, exported as 1280×720 MP4/GIF when possible.
- Duration: 28-32 seconds.
- Terminal: dark theme, 15-16pt monospace, hidden shell prompt username if needed.
- Browser: repository homepage zoomed to 110-125%.
- Close unrelated windows and notifications.
- Use a repository with no secrets in the terminal, README, or file tree.
- Record two short takes if one live run is too risky.

## Storyboard

| Time | Scene | Visual | On-screen caption |
| --- | --- | --- | --- |
| 0-3s | Problem | Open a plain repository in GitHub or the file tree. | Your code is ready. Is your launch? |
| 3-8s | Run audit | Terminal runs `python3 scripts/repo_audit.py <repo> --format markdown --output LAUNCH.md`. | Offline launch-readiness audit |
| 8-13s | Show report | Scroll `LAUNCH.md`: score table, prioritized findings, repository signals. | Scores, gaps, and concrete fixes |
| 13-18s | Show semantic packaging | Switch to improved README sections or launch plan: hero, quickstart, proof, limits. | Positioning + README + quickstart |
| 18-22s | Show benchmarks | Open `docs/BENCHMARKS.md` or the benchmark config/table. | Compare adjacent tools, not just stars |
| 22-26s | Show bilingual launch pack | Open X/V2EX/即刻 draft headings. | English + Chinese release copy |
| 26-30s | CTA | Repository homepage with README/social card. | GitHub Launch Studio — review before you launch |

## Suggested commands

Run from a checked-out copy of this repository:

```bash
python3 scripts/repo_audit.py /path/to/your/repo \
  --format markdown \
  --output /tmp/LAUNCH.md

python3 scripts/benchmark_github.py \
  --config benchmarks/representative-tools.json \
  --format markdown
```

For the recording, it is fine to write the report to `/tmp/LAUNCH.md` so the target repository stays clean.

## Voiceover / caption script

1. "Your code is ready. Is your launch?"
2. "GitHub Launch Studio starts with an offline repository audit."
3. "It scores clarity, activation, proof, trust, distribution, and maintenance."
4. "Then it turns findings into positioning, README, demo, and release work."
5. "The benchmark map explains how it fits with README and release tools."
6. "It also prepares English and Chinese launch copy."
7. "No fake stars, mass DMs, or automatic posting."

## Pre-flight checks

- [ ] Repository URL is correct and public.
- [ ] CI is green.
- [ ] README and social card render correctly.
- [ ] Terminal history contains no tokens or private paths.
- [ ] The Markdown report is legible at 720p.
- [ ] The final frame holds for at least 1.5 seconds.
- [ ] The video/GIF is under the target platform's size limit, or an MP4 link is used.
