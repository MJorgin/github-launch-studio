# 30-second demo storyboard

Goal: prove that GitHub Launch Studio turns an ordinary repository into a launch-ready package. The demo should show a real audit, a readable report, benchmark context, and prepared launch copy—not a mock product UI.

A rendered reference film is committed at `assets/launch-demo.mp4` (with `assets/launch-demo.gif` for the README). It is a deterministic Pillow/ffmpeg animation rather than a live desktop capture, so it never exposes local paths, shell history, or notifications, and it regenerates byte-identically in CI.

## Rendered reference film (shipped version)

- Concept: **launch preflight field manual**. The product performs a readiness check before public launch, so the film speaks the language of a paper checklist/manual instead of a generic dark dashboard; the core deliverable is itself a Markdown report.
- Visual language: warm paper background with subtle grain, ink text, a single cinnabar accent (plus ochre/pine status colors), near-sharp document sheets with hairline rules, tracked-caps mono labels. Deliberately avoids the default dark-neon AI palette.
- Persistent spine: a six-step preflight rail (`AUDIT → REPORT → PACKAGE → BENCHMARK → COPY → LAUNCH`) runs down the left edge of every scene and fills as the story progresses.
- Before/after score: the report scene shows **2.3/5 · NOT CLEARED**; the CTA scene shows **4.4/5** using the same five-segment gauge language, and ends with a distressed cinnabar **CLEARED FOR LAUNCH** stamp (the film's single hero effect).
- Motion discipline: one action per scene, human-paced terminal typing with short pauses, staggered entrances, ≥1s holds on results, paper-colored cross-fades between scenes.
- Specs: 1280×720, 20fps, 30.0s H.264 MP4 (~1.1 MB); README GIF at 1024×576, 12fps (~5.3 MB).
- Regenerate: `python3 scripts/render_launch_demo.py` (requires Pillow and ffmpeg; fonts resolve to system Avenir Next / Menlo / Hiragino Sans GB on macOS).

| Time | Scene | Frame |
| --- | --- | --- |
| 0-3s | Problem | Headline + preflight checklist sheet with mixed pass/warn/fail marks |
| 3-8s | Run audit | Dark terminal card; typed command, then `LAUNCH.md written` result line |
| 8-13s | Show report | `LAUNCH.md` sheet: 2.3/5, six five-segment gauges, two prioritized findings |
| 13-18s | Package | Numbered six-item "smallest convincing launch set" checklist |
| 18-22s | Benchmarks | Swiss-rule comparison table against adjacent tools |
| 22-26s | Bilingual pack | Two draft sheets (X/English, V2EX/中文) stamped READY FOR REVIEW |
| 26-30s | CTA | Headline, repo URL, 4.4/5 scorecard, CLEARED FOR LAUNCH stamp |

## Optional live-recording setup

The shipped film is generated, not recorded. These notes remain useful if you want a real-screen variant:

- Canvas: 1440×900 or 1512×982, exported as 1280×720 MP4/GIF when possible.
- Duration: 28-32 seconds.
- Terminal: dark theme, 15-16pt monospace, hidden shell prompt username if needed.
- Browser: repository homepage zoomed to 110-125%.
- Close unrelated windows and notifications.
- Use a repository with no secrets in the terminal, README, or file tree.
- Record two short takes if one live run is too risky.

The shipped scene-by-scene breakdown is the table above; suggested narration beats are listed under *Voiceover / caption script*.

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
